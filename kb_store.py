#!/usr/bin/env python3
"""
kb_store.py — SQLite store: FTS5 sparse index, source metadata, entities, claims.

Why SQLite rather than a search dependency: FTS5 ships with CPython, provides
BM25 via `bm25()`, and gives a relational home for the entity registry (§2.3)
and claim store (§2.4) in the same file. That preserves v1's "dependency-light,
no infrastructure" principle exactly — one file under kb/, no daemon, no ops.

Four parallel token streams per chunk (§3.1), each an FTS5 column:

    raw     the passage as written, lowercased
    folded  transliteration-folded (textnorm.fold) — 'Vidiśā' and 'Vidisha' meet
    deva    the Devanagari lines only, for the bilingual sources
    ents    canonical names + every alias of each entity detected in the chunk

Stream `ents` is the payoff for the entity registry. A passage that says only
'Nīlakaṇṭheśvara' becomes retrievable by 'Udayeśvara' — an identity no BM25
tokenizer and no bi-encoder can be relied on to know. For a manuscript
organised around named persons, places and monuments, that is most of what
retrieval has to do.

Note on bm25(): SQLite returns *more negative is better*. Every score leaving
this module is negated, so callers everywhere see higher-is-better.

    from kb_store import KBStore
    st = KBStore()
    st.build(chunks, mentions=...)           # full rebuild, transactional
    st.search_bm25("bhumija sikhara", k=30)  # [{rowid, score, source, ...}]
    st.search_entities(["E:MON:001"], k=30)

CLI:
    python kb_store.py --stats
    python kb_store.py --search "udayesvara mandapa dimensions" -k 10
"""
import argparse
import json
import os
import re
import sqlite3
from pathlib import Path

from textnorm import devanagari_only, fold, fold_text

KB_DIR = Path(os.environ.get("KB_DIR", "kb"))
DB_PATH = KB_DIR / "store.sqlite"

# FTS5 column weights for bm25(). Order matches the virtual table below.
# `ents` is weighted hardest: an entity-alias hit is a near-certain topical
# match, where a `folded` hit can be an artefact of digraph collapse.
BM25_WEIGHTS = (1.0, 0.7, 0.8, 2.0)

SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS chunks (
    rowid       INTEGER PRIMARY KEY,
    source      TEXT NOT NULL,
    chunk       INTEGER NOT NULL,
    trail       TEXT,
    heading     TEXT,
    page_start  INTEGER,
    page_end    INTEGER,
    text        TEXT NOT NULL,
    context     TEXT,                -- §2.2 situating preamble, embed-time only
    UNIQUE (source, chunk)
);
CREATE INDEX IF NOT EXISTS chunks_source ON chunks(source);

-- Per-source metadata from the dossiers (§2.1); drives filtering (§3.6).
CREATE TABLE IF NOT EXISTS sources (
    source       TEXT PRIMARY KEY,
    kind         TEXT,               -- primary | secondary | tertiary
    genre        TEXT,
    period_from  INTEGER,
    period_to    INTEGER,
    geography    TEXT,               -- JSON array
    stance       TEXT,
    reliability  TEXT,               -- JSON array
    summary      TEXT
);

CREATE TABLE IF NOT EXISTS entities (
    entity_id      TEXT PRIMARY KEY,
    canonical      TEXT NOT NULL,
    type           TEXT NOT NULL,
    first_attested TEXT,
    notes          TEXT,
    curated        INTEGER DEFAULT 0  -- 1 once a human has confirmed the row
);

CREATE TABLE IF NOT EXISTS entity_aliases (
    entity_id  TEXT NOT NULL REFERENCES entities(entity_id) ON DELETE CASCADE,
    alias      TEXT NOT NULL,
    folded     TEXT NOT NULL,
    PRIMARY KEY (entity_id, alias)
);
CREATE INDEX IF NOT EXISTS alias_folded ON entity_aliases(folded);

CREATE TABLE IF NOT EXISTS entity_mentions (
    entity_id  TEXT NOT NULL,
    chunk_id   INTEGER NOT NULL,
    n          INTEGER DEFAULT 1,
    PRIMARY KEY (entity_id, chunk_id)
);
CREATE INDEX IF NOT EXISTS mention_chunk ON entity_mentions(chunk_id);

-- §2.4 claim store. `scope` separates claims extracted from the corpus from
-- claims extracted from the drafted manuscript (§5.3), which are compared
-- against each other but must never be confused.
CREATE TABLE IF NOT EXISTS claims (
    claim_id       TEXT PRIMARY KEY,
    scope          TEXT NOT NULL DEFAULT 'corpus',   -- corpus | manuscript
    subject_entity TEXT,
    predicate      TEXT,
    object         TEXT,
    qualifiers     TEXT,             -- JSON
    claim_type     TEXT,             -- date_event|attribution|measurement|
                                     -- identification|interpretation|quotation
    source         TEXT,
    page_start     INTEGER,
    page_end       INTEGER,
    chunk_id       INTEGER,
    chapter        INTEGER,          -- manuscript scope only
    confidence     REAL
);
CREATE INDEX IF NOT EXISTS claim_subject ON claims(scope, subject_entity, predicate);
CREATE INDEX IF NOT EXISTS claim_source  ON claims(source);

-- Data labeling layer. Structural labels use Unlimited-OCR's <|det|> taxonomy
-- so a future GPU re-ingest can populate them directly; content and
-- evidence_role are corpus-specific. `retrievable` is the gate: apparatus and
-- badly damaged chunks stay in the store (a bibliography is useful for citation
-- checking) but are excluded from the candidate pool.
CREATE TABLE IF NOT EXISTS chunk_labels (
    chunk_id      INTEGER PRIMARY KEY,
    structural    TEXT,
    content       TEXT,             -- JSON array of content categories
    evidence_role TEXT,
    period_from   INTEGER,
    period_to     INTEGER,
    quality       REAL,
    issues        TEXT,             -- JSON array
    retrievable   INTEGER DEFAULT 1,
    labeled_by    TEXT,             -- heuristic | ocr-det | llm | human
    confidence    REAL,
    reviewed      INTEGER DEFAULT 0 -- 1 once a human has confirmed the row
);
CREATE INDEX IF NOT EXISTS labels_structural  ON chunk_labels(structural);
CREATE INDEX IF NOT EXISTS labels_role        ON chunk_labels(evidence_role);
CREATE INDEX IF NOT EXISTS labels_retrievable ON chunk_labels(retrievable, quality);

CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
"""

FTS_SCHEMA = """
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
    raw, folded, deva, ents,
    content='',
    tokenize="unicode61 remove_diacritics 2"
);
"""


def _connect(path=None):
    db = sqlite3.connect(path or DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys=ON")
    return db


# FTS5 query syntax treats punctuation as operators; a raw sub-topic question is
# full of it. Everything is quoted per-token instead of escaped.
#
# The mark ranges are load-bearing. Python's \w excludes combining marks
# (category Mn), so a bare [^\W_]+ splits 'राजा' into the two single-codepoint
# consonants 'र' and 'ज' — both then dropped by the length filter, leaving the
# Devanagari stream unreachable by any Devanagari query. A token may not *start*
# with a mark, but must be allowed to continue with one.
_MARKS = ("̀-ͯ"          # Latin/IAST combining diacritics
          "ऀ-ःऺ-ॏ॑-ॗॢ-ॣ"   # Devanagari
          "‌‍")          # ZWNJ / ZWJ, used in conjunct spelling
_FTS_TOKEN_RE = re.compile(rf"[^\W_][\w{_MARKS}]*", re.UNICODE)


def _quote(t):
    return '"' + t.replace('"', '""') + '"'


def fts_query(text, mode="OR", alias_map=None):
    """Turn free text into a safe FTS5 MATCH expression, folded per stream.

    Every token is double-quoted, so punctuation, hyphens and stray operators in
    a research question can never be parsed as syntax.

    The query must be normalised the *same way each column was*, or a column is
    simply unreachable: the `folded` and `ents` streams hold digraph-collapsed,
    transliterated keys, so matching a raw token against them finds nothing.
    'Nilakantheshwar' returned zero hits against a corpus that says
    'Neelkantheshwar' on every other page for exactly this reason. So the
    expression is split by column group:

        {raw deva} : ("nilakantheshwar")  OR  {folded ents} : ("nilakantesvar")

    When `alias_map` is supplied, a token that resolves to a known entity also
    contributes that entity's id to the `ents` clause, which is what lets a
    query for 'Udayeśvara' reach a passage that only ever says
    'Nīlakaṇṭheśvara'.

    Returns '' when the text has no usable tokens — callers must treat that as
    "no sparse results", never as "match everything".
    """
    toks = [t for t in _FTS_TOKEN_RE.findall(text or "") if len(t) > 1]
    if not toks:
        return ""

    literal = " OR ".join(_quote(t) for t in dict.fromkeys(toks))
    folded, ids = [], []
    for t in toks:
        f = fold(t)
        if f and f not in folded:
            folded.append(f)
            for eid in (alias_map or {}).get(f, ()):
                tok = eid.replace(":", "_")
                if tok not in ids:
                    ids.append(tok)

    parts = [f"{{raw deva}} : ({literal})"]
    ent_side = folded + ids
    if ent_side:
        parts.append(f"{{folded ents}} : ({' OR '.join(_quote(x) for x in ent_side)})")
    return " OR ".join(parts)


class KBStore:
    """The SQLite side of the knowledge base."""

    def __init__(self, path=None):
        self.path = Path(path or DB_PATH)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = _connect(self.path)
        self.db.executescript(SCHEMA)
        self.db.executescript(FTS_SCHEMA)
        self.db.commit()

    # -- build ----------------------------------------------------------------

    def build(self, chunks, contexts=None, alias_map=None, stamp=None):
        """(Re)build chunks + FTS index from the chunk records.

        `chunks`    the same dicts build_kb.py writes to chunks.jsonl, in order;
                    the list index becomes the rowid, so it is the join key to
                    the embedding matrix's row order. That correspondence is the
                    one invariant this store must never break.
        `contexts`  optional per-chunk situating preamble (§2.2).
        `alias_map` {folded_alias: [entity_id, ...]} — used to populate the
                    `ents` stream and entity_mentions in the same pass.
        """
        db = self.db
        with db:                                  # one transaction, all or nothing
            db.execute("DELETE FROM chunks")
            db.execute("DELETE FROM entity_mentions")
            # A contentless FTS5 table (content='') rejects DELETE, so a full
            # rebuild drops and recreates it rather than clearing it in place.
            db.execute("DROP TABLE IF EXISTS chunks_fts")
            db.executescript(FTS_SCHEMA)
            for i, c in enumerate(chunks):
                ctx = (contexts or {}).get(i) or c.get("context") or ""
                db.execute(
                    "INSERT INTO chunks (rowid, source, chunk, trail, heading,"
                    " page_start, page_end, text, context) VALUES (?,?,?,?,?,?,?,?,?)",
                    (i, c["source"], c.get("chunk", i), c.get("trail", ""),
                     c.get("heading", ""), c.get("page_start"), c.get("page_end"),
                     c["text"], ctx))

                body = c["text"]
                # The heading trail is indexed with the body: a passage under
                # "Udayeśvara temple > the maṇḍapa" is about the maṇḍapa even
                # where the word never appears in its own sentences.
                searchable = f"{c.get('trail','')}\n{ctx}\n{body}"
                ents, ids = self._entity_stream(searchable, alias_map)
                db.execute(
                    "INSERT INTO chunks_fts (rowid, raw, folded, deva, ents)"
                    " VALUES (?,?,?,?,?)",
                    (i, searchable.lower(), fold_text(searchable),
                     devanagari_only(body), ents))
                for eid, n in ids.items():
                    db.execute("INSERT OR REPLACE INTO entity_mentions"
                               " (entity_id, chunk_id, n) VALUES (?,?,?)", (eid, i, n))
            if stamp:
                db.execute("INSERT OR REPLACE INTO meta (key, value) VALUES ('stamp', ?)",
                           (json.dumps(stamp, ensure_ascii=False),))
        return self.count()

    @staticmethod
    def _entity_stream(text, alias_map):
        """Expand every detected alias into all its siblings.

        A chunk containing 'Nīlakaṇṭheśvara' is indexed under 'Udayeśvara' and
        'Udayesvara' too, so any of the three retrieves it.
        """
        if not alias_map:
            return "", {}
        folded = fold_text(text).split()
        hits, counts = [], {}
        for tok in folded:
            for eid in alias_map.get(tok, ()):
                counts[eid] = counts.get(eid, 0) + 1
                hits.append(eid)
        if not counts:
            return "", {}
        # Index the entity ids themselves plus every alias, so both an id lookup
        # and a natural-language name hit the same column.
        names = set()
        for eid in counts:
            names.add(eid.replace(":", "_"))
        for tok, eids in alias_map.items():
            if any(e in counts for e in eids):
                names.add(tok)
        return " ".join(sorted(names)), counts

    def set_source_meta(self, source, **fields):
        """Upsert a source's dossier-derived metadata (drives §3.6 filtering)."""
        for k in ("geography", "reliability"):
            if isinstance(fields.get(k), (list, dict)):
                fields[k] = json.dumps(fields[k], ensure_ascii=False)
        cols = ["source"] + list(fields)
        vals = [source] + list(fields.values())
        ph = ",".join("?" * len(cols))
        with self.db:
            self.db.execute(
                f"INSERT INTO sources ({','.join(cols)}) VALUES ({ph}) "
                f"ON CONFLICT(source) DO UPDATE SET "
                + ",".join(f"{c}=excluded.{c}" for c in cols[1:]), vals)

    # -- filtering (§3.6) -----------------------------------------------------

    def _filter_sql(self, filters):
        """Build a WHERE fragment restricting the candidate pool before scoring.

        Source-level keys: kind, genre, source, exclude_source (scalar or list),
        period_from / period_to (inclusive overlap against the source's span).

        Chunk-level label keys (labels.py / label_chunks.py):
            structural      one or more Unlimited-OCR element types
            evidence_role   primary_witness | observation | interpretation | ...
            content         a content category the chunk carries
            min_quality     float
            include_junk    True to disable the retrievable gate entirely

        The retrievable gate is ON BY DEFAULT, and that default is the point of
        the whole labeling layer: a table of contents, an index page or a
        near-duplicate can no longer be returned as evidence for a research
        question. It is a default rather than a hard rule because citation
        checking legitimately needs to reach a bibliography.
        """
        filters = dict(filters or {})
        clauses, params = [], []

        if not filters.pop("include_junk", False):
            # LEFT JOIN semantics matter: a chunk with no label row yet is
            # admitted. Labeling is optional and incremental, so an unlabelled
            # KB must behave exactly as it did before this layer existed.
            clauses.append("(lb.retrievable IS NULL OR lb.retrievable = 1)")

        for key, col in (("structural", "lb.structural"),
                         ("evidence_role", "lb.evidence_role")):
            if filters.get(key):
                v = filters.pop(key)
                vals = list(v) if isinstance(v, (list, tuple, set)) else [v]
                clauses.append(f"{col} IN ({','.join('?' * len(vals))})")
                params += vals
        if filters.get("content"):
            v = filters.pop("content")
            vals = list(v) if isinstance(v, (list, tuple, set)) else [v]
            # `content` is a JSON array; match on the quoted token so
            # 'inscription' cannot match 'inscription_meta'.
            clauses.append("(" + " OR ".join(["lb.content LIKE ?"] * len(vals)) + ")")
            params += [f'%"{x}"%' for x in vals]
        if filters.get("min_quality") is not None:
            clauses.append("(lb.quality IS NULL OR lb.quality >= ?)")
            params.append(float(filters.pop("min_quality")))

        if not filters and not clauses:
            return "", []
        if not filters:
            return (" AND " + " AND ".join(clauses)) if clauses else "", params

        def as_list(v):
            return v if isinstance(v, (list, tuple, set)) else [v]

        for key, col in (("kind", "s.kind"), ("genre", "s.genre"), ("source", "c.source")):
            if filters.get(key):
                vals = list(as_list(filters[key]))
                clauses.append(f"{col} IN ({','.join('?' * len(vals))})")
                params += vals
        if filters.get("exclude_source"):
            vals = list(as_list(filters["exclude_source"]))
            clauses.append(f"c.source NOT IN ({','.join('?' * len(vals))})")
            params += vals
        # Overlap, not containment: a source spanning 1000-1300 is relevant to a
        # query about 1050-1100. A source with no recorded span is kept — absent
        # metadata must never silently exclude evidence.
        if filters.get("period_from") is not None:
            clauses.append("(s.period_to IS NULL OR s.period_to >= ?)")
            params.append(int(filters["period_from"]))
        if filters.get("period_to") is not None:
            clauses.append("(s.period_from IS NULL OR s.period_from <= ?)")
            params.append(int(filters["period_to"]))
        return (" AND " + " AND ".join(clauses)) if clauses else "", params

    # -- search ---------------------------------------------------------------

    _SELECT = ("c.rowid AS rowid, c.source, c.chunk, c.trail, c.heading,"
               " c.page_start, c.page_end, c.text, c.context")

    def search_bm25(self, query, k=30, filters=None, alias_map=None):
        """BM25 over the four streams. Higher score is better."""
        expr = fts_query(query, alias_map=alias_map)
        if not expr:
            return []
        where, params = self._filter_sql(filters)
        sql = (f"SELECT {self._SELECT}, bm25(chunks_fts, ?, ?, ?, ?) AS bm"
               f" FROM chunks_fts JOIN chunks c ON c.rowid = chunks_fts.rowid"
               f" LEFT JOIN sources s ON s.source = c.source"
               f" LEFT JOIN chunk_labels lb ON lb.chunk_id = c.rowid"
               f" WHERE chunks_fts MATCH ?{where}"
               f" ORDER BY bm LIMIT ?")
        args = [*BM25_WEIGHTS, expr, *params, k]
        rows = self.db.execute(sql, args).fetchall()
        return [{**dict(r), "score": -r["bm"]} for r in rows]

    def search_entities(self, entity_ids, k=30, filters=None):
        """Chunks mentioning any of these entities, most-mentions first.

        This is the exact-match channel. It cannot rank by topical fit — only by
        how often the entity is named — so it enters the funnel as one RRF
        channel among three rather than as a scorer in its own right.
        """
        if not entity_ids:
            return []
        where, params = self._filter_sql(filters)
        ph = ",".join("?" * len(entity_ids))
        sql = (f"SELECT {self._SELECT}, SUM(m.n) AS hits, COUNT(DISTINCT m.entity_id) AS ents"
               f" FROM entity_mentions m JOIN chunks c ON c.rowid = m.chunk_id"
               f" LEFT JOIN sources s ON s.source = c.source"
               f" LEFT JOIN chunk_labels lb ON lb.chunk_id = c.rowid"
               f" WHERE m.entity_id IN ({ph}){where}"
               f" GROUP BY c.rowid ORDER BY ents DESC, hits DESC LIMIT ?")
        rows = self.db.execute(sql, [*entity_ids, *params, k]).fetchall()
        return [{**dict(r), "score": float(r["ents"]) + float(r["hits"]) / 100.0} for r in rows]

    def chunk(self, rowid):
        r = self.db.execute(f"SELECT {self._SELECT} FROM chunks c WHERE c.rowid=?",
                            (rowid,)).fetchone()
        return dict(r) if r else None

    def chunks_for(self, rowids):
        if not rowids:
            return {}
        ph = ",".join("?" * len(rowids))
        rows = self.db.execute(
            f"SELECT {self._SELECT} FROM chunks c WHERE c.rowid IN ({ph})", list(rowids))
        return {r["rowid"]: dict(r) for r in rows}

    def allowed_rowids(self, filters):
        """The rowids a filter admits — for masking the dense channel, which is
        a numpy matrix and cannot join against SQL.

        None means "no mask needed". Note that an EMPTY filter is not the same
        as no filter: the retrievable gate still applies, because otherwise the
        sparse channel (which always goes through _filter_sql) would exclude
        index pages while the dense channel happily returned them — one funnel,
        two different corpora.
        """
        filters = dict(filters or {})
        if filters.get("include_junk") and len(filters) == 1:
            return None                  # genuinely unfiltered; skip the mask
        where, params = self._filter_sql(filters)
        rows = self.db.execute(
            f"SELECT c.rowid FROM chunks c LEFT JOIN sources s ON s.source=c.source"
            f" LEFT JOIN chunk_labels lb ON lb.chunk_id=c.rowid"
            f" WHERE 1=1{where}", params)
        return {r["rowid"] for r in rows}

    # -- housekeeping ---------------------------------------------------------

    def count(self):
        return self.db.execute("SELECT COUNT(*) n FROM chunks").fetchone()["n"]

    def stamp(self):
        r = self.db.execute("SELECT value FROM meta WHERE key='stamp'").fetchone()
        return json.loads(r["value"]) if r else None

    def stats(self):
        q = lambda s: self.db.execute(s).fetchone()[0]          # noqa: E731
        return {
            "chunks": q("SELECT COUNT(*) FROM chunks"),
            "with_context": q("SELECT COUNT(*) FROM chunks WHERE context <> ''"),
            "sources": q("SELECT COUNT(*) FROM sources"),
            "entities": q("SELECT COUNT(*) FROM entities"),
            "curated_entities": q("SELECT COUNT(*) FROM entities WHERE curated=1"),
            "aliases": q("SELECT COUNT(*) FROM entity_aliases"),
            "mentions": q("SELECT COUNT(*) FROM entity_mentions"),
            "claims_corpus": q("SELECT COUNT(*) FROM claims WHERE scope='corpus'"),
            "claims_manuscript": q("SELECT COUNT(*) FROM claims WHERE scope='manuscript'"),
        }

    def close(self):
        self.db.close()


def main():
    from console import use_utf8
    use_utf8()
    ap = argparse.ArgumentParser(description="Inspect or query the SQLite KB store")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--search")
    ap.add_argument("-k", type=int, default=10)
    ap.add_argument("--kind", help="filter: primary|secondary|tertiary")
    args = ap.parse_args()

    if not DB_PATH.exists():
        print(f"No store at {DB_PATH}. Build it: python build_kb.py"); return
    st = KBStore()
    if args.stats or not args.search:
        for k, v in st.stats().items():
            print(f"  {k:20s} {v:>8,}")
        print(f"\n  stamp: {st.stamp()}")
    if args.search:
        filters = {"kind": args.kind} if args.kind else None
        for h in st.search_bm25(args.search, k=args.k, filters=filters):
            print(f"{h['score']:7.3f}  [{h['source']}] {(h['trail'] or '')[:60]}")
            print("   " + h["text"].replace("\n", " ")[:180] + "\n")


if __name__ == "__main__":
    main()
