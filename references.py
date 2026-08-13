#!/usr/bin/env python3
"""
references.py — what each source contains, and which works it was built from.

Two records per source, both of which the pipeline has so far had no way to
produce:

  CONTENTS   what this text entails — its structural make-up, what kinds of
             evidence it carries, which entities it is actually about, what
             periods it covers, and where its substance is concentrated.
             Assembled from the labeling layer, the entity index and the
             dossier, so it is observed rather than asserted.

  PROVENANCE which published works this text was built from, and how heavily
             it leans on each. Extracted from the source's own bibliography and
             its in-text citations, then linked into a graph:

                 source --cites--> work <--cites-- other source

This is the layer that answers questions the corpus otherwise cannot: which of
these twenty-four books rest on Cunningham, and which went back to the stone;
whether two accounts agree because they are independent or because both are
reading the same 1933 monograph; which cited authority appears everywhere in the
corpus and has never been consulted directly.

That last question matters for a history. Two sources agreeing is only evidence
when they are independent, and a citation graph is the only thing in this
pipeline that can tell the difference.

Extraction is deliberately two-track:

    deterministic   bibliography entries and in-text citation markers are found
                    by pattern. Cheap, exhaustive, and it never invents a
                    citation that is not on the page.
    model-assisted  parsing a messy OCR'd bibliography line into author / title
                    / year / publisher, and resolving 'ibid.' or 'op. cit.' to
                    what they point at. Only ever applied to text the
                    deterministic pass already located.

A citation is never inferred from a model's memory of the literature. If the
page does not carry it, it does not exist here.

Usage:
    python references.py --extract              # bibliography + in-text markers
    python references.py --resolve              # parse entries into works (LLM)
    python references.py --graph                # who depends on whom
    python references.py --source bhojdev.md    # one source's full record
    python references.py --contents             # what each source entails
    python references.py --shared               # works cited by 2+ sources
"""
import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

from config import CFG
from console import use_utf8
from kb_store import KBStore
from textnorm import fold

OUT = Path("book/_provenance")

# ---------------------------------------------------------------------------
# Deterministic extraction
# ---------------------------------------------------------------------------

# A line that STARTS a new bibliography entry.
#
# Three shapes, all of which occur in these books and two of which a naive
# "starts with a capital" rule misses entirely:
#   Surname, Firstname, *Title* ...     the ordinary case
#   —*Another Title by the same author* the repeated-author em-dash convention
#   [12] Author, Title ...              numbered reference lists
# The em-dash form alone accounted for most of the misses: 367 lines carried a
# bibliographic signal and only 48 matched.
BIB_START_RE = re.compile(
    r"^\s*(?:\[\d{1,3}\]\s*)?"
    r"(?:(?P<dash>[—–]{1,2}|-{2,})\s*"
    r"|(?P<author>[A-ZĀĪŪŚṢṆṬḌÑṚ][\w’'.-]+(?:\s+[A-Z][\w’'.-]*)*\s*,)"
    r"|(?P<quoted>['\"“‘]))")

# A wrapped continuation: no entry-start shape, and the previous line did not
# look finished. Bibliographies in this corpus wrap mid-title constantly
# ("Chandra, Pramod (ed), *Studies in" / "Indian Temple Architecture*"), and
# treating each physical line as an entry loses both halves.
_ENDS_ENTRY_RE = re.compile(r"[)\]}]\s*\.?\s*$|\b\d{4}\s*\)?\.?\s*$|[.;]\s*$")

_HAS_BIB_SIGNAL = re.compile(
    r"(?:\(\s*(?:1[5-9]\d{2}|20[0-2]\d)\s*\)"          # (1933)
    r"|,\s*(?:1[5-9]\d{2}|20[0-2]\d)\b"                # , 1933
    r"|\bvol\.\s*[IVXL0-9]"
    r"|\bpp?\.\s*\d"
    r"|\b(?:ed|eds|trans|repr|rev)\.\b"
    r"|\b(?:University|Press|Publishers?|Journal|Society|Survey|Institute)\b)", re.I)

# In-text citation shapes, in the order they should be tried.
CITE_PATTERNS = [
    ("author_year", re.compile(
        r"\(\s*(?P<a>[A-ZĀĪŪŚṢṆṬḌÑṚ][\w’'-]+(?:\s+(?:and|&)\s+[A-Z][\w’'-]+)?)"
        r",?\s*(?P<y>1[5-9]\d{2}|20[0-2]\d)\s*(?::\s*[\d–\-—,\s]+)?\)")),
    ("narrative_year", re.compile(
        r"\b(?P<a>[A-ZĀĪŪŚṢṆṬḌÑṚ][\w’'-]{2,})\s*\(\s*(?P<y>1[5-9]\d{2}|20[0-2]\d)\s*\)")),
    ("op_cit", re.compile(
        r"\b(?P<a>[A-ZĀĪŪŚṢṆṬḌÑṚ][\w’'-]{2,})\s*,\s*op\.\s*cit\.", re.I)),
    ("ibid", re.compile(r"\bibid\b\.?(?:\s*,\s*p{1,2}\.\s*[\d–\-—]+)?", re.I)),
    ("footnote_ref", re.compile(r"(?<=[a-z\)\"”])\s*\[(?P<n>\d{1,3})\]")),
]

# Authorities this corpus repeatedly leans on. Used only to normalise surface
# forms of names ALREADY found on the page — never to add a citation.
KNOWN_AUTHORS = {
    "cunningham": "Alexander Cunningham",
    "kramrisch": "Stella Kramrisch",
    "hardy": "Adam Hardy",
    "ganguly": "D. C. Ganguly",
    "patil": "D. R. Patil",
    "gupte": "R. S. Gupte",
    "meister": "Michael W. Meister",
    "dhaky": "M. A. Dhaky",
    "burgess": "James Burgess",
    "fergusson": "James Fergusson",
    "kielhorn": "F. Kielhorn",
    "fleet": "J. F. Fleet",
    "bhandarkar": "D. R. Bhandarkar",
    "sircar": "D. C. Sircar",
    "majumdar": "R. C. Majumdar",
    "marshall": "John Marshall",
    "coomaraswamy": "Ananda K. Coomaraswamy",
}

SCHEMA = """
-- A published work, deduplicated across the corpus by a normalised key.
CREATE TABLE IF NOT EXISTS works (
    work_id    TEXT PRIMARY KEY,
    author     TEXT,
    title      TEXT,
    year       INTEGER,
    publisher  TEXT,
    raw        TEXT,          -- the bibliography line it was parsed from
    kind       TEXT,          -- book | article | report | edition | inscription | unknown
    in_corpus  TEXT           -- filename, if this work is ITSELF one of our sources
);

-- source --cites--> work
CREATE TABLE IF NOT EXISTS citations (
    source     TEXT NOT NULL,
    work_id    TEXT NOT NULL,
    chunk_id   INTEGER,
    kind       TEXT,          -- bibliography | author_year | op_cit | footnote_ref ...
    surface    TEXT,          -- what actually appeared on the page
    page_start INTEGER,
    PRIMARY KEY (source, work_id, chunk_id, surface)
);
CREATE INDEX IF NOT EXISTS cite_source ON citations(source);
CREATE INDEX IF NOT EXISTS cite_work   ON citations(work_id);

-- Raw bibliography lines, kept even when unparseable, so nothing is silently lost.
CREATE TABLE IF NOT EXISTS bib_entries (
    entry_id  TEXT PRIMARY KEY,
    source    TEXT NOT NULL,
    chunk_id  INTEGER,
    raw       TEXT NOT NULL,
    work_id   TEXT,           -- set once resolved
    -- 0 = not yet attempted, 1 = parsed into a work, -1 = attempted and
    -- DECLINED. The third state is load-bearing: the signal-density candidate
    -- pass deliberately over-collects, so ~210 of these are footnote prose that
    -- merely cites things ("also 'Ep. Ind.', vols. VI. p. 202") rather than
    -- bibliography entries. Without recording the attempt they re-enter every
    -- run and the pass never converges — it looked like failure when it was the
    -- resolver working correctly.
    resolved  INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS bib_source ON bib_entries(source);
"""


def ensure_schema(store):
    store.db.executescript(SCHEMA)
    store.db.commit()


def _as_text(v):
    """Coerce a model-supplied field to a string.

    Multi-author entries come back as a list ("author": ["Smith, A.", "Jones,
    B."]), which reached fold() and crashed the whole resolve pass after 204
    entries. Normalising at the boundary is cheaper than defending every
    downstream call.
    """
    if v is None:
        return ""
    if isinstance(v, (list, tuple)):
        return "; ".join(str(x).strip() for x in v if x)
    return str(v).strip()


def work_key(author, title, year):
    """Stable id from normalised author + title + year."""
    author, title = _as_text(author), _as_text(title)
    a = fold(author or "")[:24]
    t = fold(title or "")[:48]
    return "W:" + hashlib.blake2b(f"{a}|{t}|{year or ''}".encode("utf-8"),
                                  digest_size=8).hexdigest()


def normalise_author(surface):
    return KNOWN_AUTHORS.get(fold(surface or ""), (surface or "").strip())


# ---------------------------------------------------------------------------
# Pass 1 — locate bibliography lines and in-text citations (deterministic)
# ---------------------------------------------------------------------------

def iter_bib_entries(text):
    """Yield (entry_text, inherited_author) from a bibliography chunk.

    Physical lines are NOT entries. Entries wrap, and the em-dash convention
    means an entry may carry no author of its own — it inherits the previous
    one. Both are resolved here so the resolver sees whole, attributed entries.
    """
    lines = [l.rstrip() for l in text.split("\n")]
    entries, buf, last_author = [], [], None

    def flush():
        if not buf:
            return
        joined = " ".join(x.strip() for x in buf if x.strip())
        joined = re.sub(r"\s{2,}", " ", joined).strip(" -*·•\t")
        if len(joined) >= 24 and _HAS_BIB_SIGNAL.search(joined):
            entries.append(joined)
        buf.clear()

    for line in lines:
        s = line.strip(" *·•\t")
        if not s:
            flush()
            continue
        m = BIB_START_RE.match(s)
        starts = bool(m)
        if starts and buf and not _ENDS_ENTRY_RE.search(" ".join(buf)):
            # Looks like a start, but the entry so far is unfinished — a wrapped
            # title beginning with a capitalised word would otherwise split here.
            if not m.group("dash") and len(" ".join(buf)) < 60:
                starts = False
        if starts:
            flush()
            if m.group("author"):
                last_author = m.group("author").rstrip(",").strip()
            elif m.group("dash") and last_author:
                s = f"{last_author}, {s.lstrip('—–- ')}"
        buf.append(s)
    flush()

    out = []
    for e in entries:
        am = BIB_START_RE.match(e)
        author = am.group("author").rstrip(",") if am and am.group("author") else None
        out.append((e[:600], author))
    return out


def extract(store, sources=None):
    ensure_schema(store)
    where, params = "", []
    if sources:
        where = f" AND c.source IN ({','.join('?' * len(sources))})"
        params = list(sources)

    # Candidates come from two places. The labeling layer's `bibliography` and
    # `footnote` chunks are the precise set — but a long bibliography spans many
    # chunks and only some of them trip the structural rule, so restricting to
    # the label found 75 entries in a corpus that plainly holds thousands.
    #
    # The second source is signal density: any chunk with several lines that
    # look bibliographic, whatever its label. False positives are cheap here
    # because the resolver discards what it cannot parse; missed entries are
    # invisible, which is the expensive direction.
    labelled = store.db.execute(
        f"SELECT c.rowid, c.source, c.text, c.page_start FROM chunks c "
        f"JOIN chunk_labels l ON l.chunk_id=c.rowid "
        f"WHERE l.structural IN ('bibliography','footnote'){where}", params).fetchall()
    seen_ids = {r["rowid"] for r in labelled}

    dense = []
    for r in store.db.execute(
            f"SELECT c.rowid, c.source, c.text, c.page_start FROM chunks c WHERE 1=1{where}",
            params):
        if r["rowid"] in seen_ids:
            continue
        hits = sum(1 for ln in r["text"].split("\n")
                   if len(ln.strip()) >= 24 and _HAS_BIB_SIGNAL.search(ln))
        if hits >= 3:
            dense.append(r)
    bib_rows = list(labelled) + dense
    print(f"  candidates: {len(labelled)} labelled + {len(dense)} signal-dense chunks")

    n_entries = 0
    with store.db:
        for r in bib_rows:
            for raw, prev_author in iter_bib_entries(r["text"]):
                eid = "B:" + hashlib.blake2b(f"{r['source']}|{raw}".encode("utf-8"),
                                             digest_size=8).hexdigest()
                store.db.execute(
                    "INSERT OR IGNORE INTO bib_entries (entry_id, source, chunk_id, raw)"
                    " VALUES (?,?,?,?)", (eid, r["source"], r["rowid"], raw))
                n_entries += 1

    # In-text citations, across the whole corpus.
    all_rows = store.db.execute(
        f"SELECT c.rowid, c.source, c.text, c.page_start FROM chunks c WHERE 1=1"
        f"{where.replace('c.source IN', 'c.source IN')}", params).fetchall()

    hits = collections.Counter()
    pending = []
    for r in all_rows:
        for kind, pat in CITE_PATTERNS:
            for m in pat.finditer(r["text"]):
                surface = m.group(0).strip()
                author = m.groupdict().get("a")
                year = m.groupdict().get("y")
                if kind == "footnote_ref" and not author:
                    # A bare [12] is a pointer to apparatus, not yet a work. It
                    # is recorded so the density is measurable, but it cannot be
                    # resolved to anything without the footnote text.
                    pass
                pending.append((r["source"], r["rowid"], kind, surface,
                                normalise_author(author) if author else None,
                                int(year) if year else None, r["page_start"]))
                hits[kind] += 1
    return n_entries, hits, pending


def store_citations(store, pending):
    """Attach in-text citations to works, creating stub works where needed."""
    made = 0
    with store.db:
        for source, chunk_id, kind, surface, author, year, page in pending:
            if not author:
                continue                     # unresolvable without footnote text
            wid = work_key(author, "", year)
            store.db.execute(
                "INSERT OR IGNORE INTO works (work_id, author, title, year, raw, kind)"
                " VALUES (?,?,?,?,?,?)",
                (wid, author, None, year, surface, "unknown"))
            store.db.execute(
                "INSERT OR IGNORE INTO citations "
                "(source, work_id, chunk_id, kind, surface, page_start)"
                " VALUES (?,?,?,?,?,?)",
                (source, wid, chunk_id, kind, surface[:200], page))
            made += 1
    return made


# ---------------------------------------------------------------------------
# Pass 2 — parse bibliography lines into works (model-assisted)
# ---------------------------------------------------------------------------

RESOLVE_SYSTEM = """You parse bibliography entries from OCR'd scholarly books on Indian history \
and architecture.

For each raw entry, extract the fields that are ACTUALLY PRESENT. Use null for anything the line \
does not state — do NOT complete a reference from your own knowledge of the literature, and do \
NOT correct a title you think is wrong. OCR noise is expected; recover what you can and leave the \
rest null.

`kind`: book | article | report | edition | inscription | thesis | unknown
  edition    = an edition or translation of a primary text
  report     = a survey or government report (ASI reports, gazetteers)
  inscription = an epigraph published as such

Return JSON only:
{"results": [{"i": 0, "author": "...", "title": "...", "year": 1933,
              "publisher": "...", "kind": "book"}]}"""


def resolve(store, batch=8, workers=3, limit=None):
    from llm import complete_json, get_client, parallel
    ensure_schema(store)
    rows = [dict(r) for r in store.db.execute(
        "SELECT entry_id, source, chunk_id, raw FROM bib_entries WHERE resolved=0")]
    if limit:
        rows = rows[:limit]
    if not rows:
        print("no unresolved bibliography entries"); return 0

    client = get_client()
    model = CFG.comprehension.model
    groups = [rows[i:i + batch] for i in range(0, len(rows), batch)]
    print(f"resolving {len(rows):,} entries in {len(groups)} batch(es)", flush=True)

    def one(g):
        items = [{"i": k, "raw": e["raw"][:320]} for k, e in enumerate(g)]
        return g, complete_json(client, model,
                                [{"role": "system", "content": RESOLVE_SYSTEM},
                                 {"role": "user", "content": json.dumps(items, ensure_ascii=False)}],
                                max_tokens=4000, temperature=0.0, quiet=True)

    def failed(g, e):
        print(f"    batch failed: {type(e).__name__}", file=sys.stderr)
        return g, {"results": []}

    made = declined = 0
    for start in range(0, len(groups), 15):
        window = groups[start:start + 15]
        for g, data in parallel(one, window, workers=workers, on_error=failed):
            got = {int(r["i"]): r for r in (data or {}).get("results", []) if "i" in r}
            with store.db:
                for k, e in enumerate(g):
                    d = got.get(k)
                    if not d or not (_as_text(d.get("author")) or _as_text(d.get("title"))):
                        # Attempted and declined — not a bibliography entry.
                        # Recorded so the next run does not re-try it forever.
                        if k in got:
                            store.db.execute(
                                "UPDATE bib_entries SET resolved=-1 WHERE entry_id=?",
                                (e["entry_id"],))
                            declined += 1
                        continue
                    author = _as_text(d.get("author"))
                    title = _as_text(d.get("title"))
                    year = d.get("year") if isinstance(d.get("year"), int) else None
                    wid = work_key(author, title, year)
                    store.db.execute(
                        "INSERT OR IGNORE INTO works "
                        "(work_id, author, title, year, publisher, raw, kind)"
                        " VALUES (?,?,?,?,?,?,?)",
                        (wid, author or None, title or None, year,
                         _as_text(d.get("publisher")) or None, e["raw"][:400],
                         _as_text(d.get("kind")) or "unknown"))
                    store.db.execute(
                        "UPDATE bib_entries SET work_id=?, resolved=1 WHERE entry_id=?",
                        (wid, e["entry_id"]))
                    store.db.execute(
                        "INSERT OR IGNORE INTO citations "
                        "(source, work_id, chunk_id, kind, surface, page_start)"
                        " VALUES (?,?,?,?,?,?)",
                        (e["source"], wid, e["chunk_id"], "bibliography",
                         e["raw"][:200], None))
                    made += 1
        print(f"  {made:,} resolved, {declined:,} declined (not bibliography entries)",
              flush=True)
    link_corpus_works(store)
    return made, declined


_STOPWORDS = {"the", "of", "a", "an", "and", "in", "on", "its", "his", "her",
              "india", "indian", "study", "studies", "history", "vol", "volume",
              "part", "new", "delhi", "press", "university", "temple", "temples"}


def _title_tokens(text):
    """Content tokens of a title — the stopwords here are domain-specific.

    'Temple' and 'India' are worthless discriminators in this corpus: half the
    bibliography contains both. Leaving them in is what let a work titled merely
    "Architecture'" match Hardy's monograph.
    """
    toks = {fold(t) for t in re.findall(r"[^\W\d_]{3,}", text or "", re.UNICODE)}
    return {t for t in toks if t and t not in _STOPWORDS and len(t) >= 4}


def _surname(author):
    """Surname of the first author, in whatever order the citation used it."""
    a = _as_text(author).split(";")[0].strip()
    if "," in a:                       # "Kramrisch, Stella"
        return fold(a.split(",")[0])
    parts = [p for p in re.split(r"\s+", a) if len(p) > 1]
    return fold(parts[-1]) if parts else ""


def _title_contained(a, b, min_len=12):
    """Is one folded title essentially the other? Substring either way."""
    if not a or not b or min(len(a), len(b)) < min_len:
        return False
    return a in b or b in a


def corpus_identities(store):
    """Everything known about each corpus source that a citation might name.

    Four independent signals, in descending authority:
      sources.py   hand-curated short and full citation forms — the only place
                   in the project where a human has written down what these
                   files actually are
      dossiers     the model's reading of each document's own title page
      entities     a source that IS a named text (the Samarāṅgaṇasūtradhāra)
                   carries every alias the registry knows for it
      filename     last resort, and never sufficient on its own
    """
    import sources as src_mod
    try:
        from doc_understanding import load_all
        dossiers = load_all()
    except Exception:                              # noqa: BLE001
        dossiers = {}
    try:
        from entities import EntityIndex
        ents = EntityIndex.load()
    except Exception:                              # noqa: BLE001
        ents = None

    out = {}
    for r in store.db.execute("SELECT DISTINCT source FROM chunks"):
        s = r["source"]
        titles, authors, years = [], [], set()

        short, full = src_mod.SOURCES.get(s, (None, None))
        for form in (short, full):
            if not form:
                continue
            m = re.search(r"\*([^*]{6,})\*", form)   # the italicised title
            if m:
                titles.append(m.group(1))
            head = form.split("*")[0].strip(" .,")
            if head and not head.startswith("*"):
                authors.append(head)
            for y in re.findall(r"\b(1[5-9]\d{2}|20[0-2]\d)\b", form):
                years.add(int(y))

        d = dossiers.get(s) or {}
        ident = d.get("identity") or {}
        if ident.get("title"):
            titles.append(str(ident["title"]))
        if ident.get("author"):
            authors.append(str(ident["author"]))
        if isinstance(ident.get("year"), int):
            years.add(ident["year"])

        aliases = []
        if ents is not None:
            for t in titles + [Path(s).stem]:
                eid = ents.resolve(t)
                if eid:
                    aliases += ents.by_id[eid]["aliases"]

        titles.append(Path(s).stem.replace("-", " ").replace("_", " "))
        # The longest curated title is the identity's canonical form: the
        # sources.py entry if there is one, else the dossier's, else the stem.
        canonical = max(titles, key=len) if titles else ""
        out[s] = {
            "source": s,
            "title_fold": fold(canonical),
            "title_tokens": set().union(*[_title_tokens(t) for t in titles]) if titles else set(),
            "aliases": {fold(a) for a in aliases if a},
            "surnames": {x for x in (_surname(a) for a in authors) if x and len(x) >= 4},
            "years": years,
        }
    return out


def token_document_frequency(identities):
    """How many corpus identities each title token appears in.

    A token in one identity names that source; a token in five names nothing.
    """
    df = collections.Counter()
    for ident in identities.values():
        for t in ident["title_tokens"]:
            df[t] += 1
    return df


def match_work(work, identities, min_score=2, df=None):
    """Is this cited work one of our sources? Returns (source, score, why).

    Evidence is scored rather than matched, because no single signal is
    trustworthy: an author surname alone confuses Kramrisch vol. 1 with vol. 2,
    a year alone is meaningless, and a title fragment alone is what produced
    "Architecture'" matching Hardy. Two independent signals are required.
    """
    title = _as_text(work.get("title") if isinstance(work, dict) else work["title"])
    author = _as_text(work.get("author") if isinstance(work, dict) else work["author"])
    year = (work.get("year") if isinstance(work, dict) else work["year"])
    wt = _title_tokens(title)
    ws = _surname(author)
    wfold = fold(f"{author} {title}")
    df = df if df is not None else token_document_frequency(identities)

    best = (None, 0, [])
    for src, ident in identities.items():
        score, why = 0, []
        if ident["aliases"] and any(a and len(a) >= 8 and a in wfold
                                    for a in ident["aliases"]):
            score += 3; why.append("entity-alias")
        if wt and ident["title_tokens"]:
            # Only DISCRIMINATIVE tokens count. A token shared by several corpus
            # identities identifies none of them: 'climate' and 'basin' appear
            # in both hydrology sources, and 'english'/'translation' in every
            # bilingual edition, so matching on them linked a paper about Asian
            # climate change to the Betwa streamflow study and the Bṛhatsaṃhitā
            # to Raja Bhoj. Document frequency across identities settles it.
            shared = wt & ident["title_tokens"]
            unique = {t for t in shared if df.get(t, 0) == 1}
            narrow = {t for t in shared if df.get(t, 0) == 2}
            # Whole-title containment is the only title evidence strong enough
            # to stand alone. Topic overlap is not identity: "Asia climate
            # change 2007" and "Streamflow of the Betwa River under climate
            # change" share every discriminative token this corpus has for
            # hydrology and are entirely different papers. Containment, by
            # contrast, is how "Bhoja Paramāra and his Times" recognises itself.
            if ident["title_fold"] and len(ident["title_fold"]) >= 12 and \
                    _title_contained(fold(title), ident["title_fold"]):
                score += 3; why.append("title-match")
            elif len(unique) >= 2:
                score += 2; why.append(f"title!{','.join(sorted(unique)[:3])}")
            elif len(unique) == 1 or len(narrow) >= 2:
                score += 1
                why.append(f"title~{','.join(sorted(unique or narrow)[:2])}")
        if ws and ws in ident["surnames"]:
            score += 2; why.append(f"author:{ws}")
        if year and year in ident["years"]:
            score += 1; why.append(f"year:{year}")
        if score > best[1]:
            best = (src, score, why)

    return best if best[1] >= min_score else (None, best[1], best[2])


def link_corpus_works(store, min_score=2, verbose=False):
    """Mark works that ARE one of our own sources — the corpus citing itself.

    This is the most valuable edge in the graph: when Patil's survey cites
    Kramrisch and we hold Kramrisch, the dependency stops being a name on a page
    and becomes something checkable.
    """
    identities = corpus_identities(store)
    df = token_document_frequency(identities)
    linked, cleared = 0, 0
    with store.db:
        store.db.execute("UPDATE works SET in_corpus=NULL")
        for w in store.db.execute("SELECT work_id, author, title, year FROM works").fetchall():
            src, score, why = match_work(dict(w), identities, min_score, df)
            if src:
                store.db.execute("UPDATE works SET in_corpus=? WHERE work_id=?",
                                 (src, w["work_id"]))
                linked += 1
                if verbose:
                    print(f"  {src[:38]:40s} <- {(w['author'] or '?')[:22]:24s}"
                          f" {(w['title'] or '')[:30]:32s} [{score}: {','.join(why)}]")
            else:
                cleared += 1
    return linked


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def source_contents(store, source):
    """What this text entails — observed, not asserted."""
    row = store.db.execute(
        "SELECT COUNT(*) n, SUM(LENGTH(text)) chars FROM chunks WHERE source=?",
        (source,)).fetchone()
    struct = {r["structural"]: r["n"] for r in store.db.execute(
        "SELECT l.structural, COUNT(*) n FROM chunk_labels l JOIN chunks c ON c.rowid=l.chunk_id"
        " WHERE c.source=? GROUP BY l.structural", (source,))}
    roles = {r["evidence_role"]: r["n"] for r in store.db.execute(
        "SELECT l.evidence_role, COUNT(*) n FROM chunk_labels l JOIN chunks c ON c.rowid=l.chunk_id"
        " WHERE c.source=? AND l.evidence_role IS NOT NULL GROUP BY l.evidence_role", (source,))}
    content = collections.Counter()
    for r in store.db.execute(
            "SELECT l.content FROM chunk_labels l JOIN chunks c ON c.rowid=l.chunk_id"
            " WHERE c.source=? AND l.content IS NOT NULL", (source,)):
        for cat in json.loads(r["content"] or "[]"):
            content[cat] += 1
    ents = [(r["entity_id"], r["n"]) for r in store.db.execute(
        "SELECT m.entity_id, COUNT(*) n FROM entity_mentions m JOIN chunks c ON c.rowid=m.chunk_id"
        " WHERE c.source=? GROUP BY m.entity_id ORDER BY n DESC LIMIT 12", (source,))]
    meta = store.db.execute("SELECT * FROM sources WHERE source=?", (source,)).fetchone()
    cites = store.db.execute(
        "SELECT COUNT(DISTINCT work_id) n FROM citations WHERE source=?", (source,)).fetchone()["n"]
    return {"source": source, "chunks": row["n"], "chars": row["chars"] or 0,
            "structural": struct, "evidence_role": roles,
            "content": dict(content.most_common(8)), "top_entities": ents,
            "kind": (meta["kind"] if meta else None),
            "genre": (meta["genre"] if meta else None),
            "period": [meta["period_from"], meta["period_to"]] if meta else None,
            "stance": (meta["stance"] if meta else None),
            "cites_works": cites}


def graph(store):
    """source -> works, and which works are shared."""
    edges = collections.defaultdict(collections.Counter)
    for r in store.db.execute("SELECT source, work_id FROM citations"):
        edges[r["source"]][r["work_id"]] += 1
    works = {r["work_id"]: dict(r) for r in store.db.execute("SELECT * FROM works")}
    shared = collections.Counter()
    for src, ws in edges.items():
        for w in ws:
            shared[w] += 1
    return edges, works, shared


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Citation extraction and provenance")
    ap.add_argument("--extract", action="store_true")
    ap.add_argument("--resolve", action="store_true")
    ap.add_argument("--graph", action="store_true")
    ap.add_argument("--contents", action="store_true")
    ap.add_argument("--shared", action="store_true")
    ap.add_argument("--source", help="one source's full record")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--link", action="store_true",
                    help="re-link cited works to corpus sources, showing evidence")
    ap.add_argument("--min-score", type=int, default=2)
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    store = KBStore()
    ensure_schema(store)

    if args.extract:
        n_entries, hits, pending = extract(store)
        made = store_citations(store, pending)
        print(f"bibliography entries found : {n_entries:,}")
        print(f"in-text citation markers   : {sum(hits.values()):,}")
        for k, v in hits.most_common():
            print(f"    {k:16s} {v:6,}")
        print(f"citation edges stored      : {made:,}")
        print("\nNext: python references.py --resolve   (parses entries into works)")

    if args.link:
        n = link_corpus_works(store, min_score=args.min_score, verbose=True)
        total = store.db.execute("SELECT COUNT(*) n FROM works").fetchone()["n"]
        print(f"\n{n} of {total} cited works linked to a corpus source "
              f"(min_score={args.min_score})")

    if args.resolve:
        n, declined = resolve(store, limit=args.limit)
        left = store.db.execute(
            "SELECT COUNT(*) n FROM bib_entries WHERE resolved=0").fetchone()["n"]
        print(f"{n:,} resolved into works; {declined:,} declined as non-entries; "
              f"{left:,} still unattempted")

    if args.source:
        rec = source_contents(store, args.source)
        print(json.dumps(rec, ensure_ascii=False, indent=1))
        rows = store.db.execute(
            "SELECT w.author, w.title, w.year, COUNT(*) n FROM citations c "
            "JOIN works w ON w.work_id=c.work_id WHERE c.source=? "
            "GROUP BY c.work_id ORDER BY n DESC LIMIT 25", (args.source,)).fetchall()
        print(f"\nbuilt from ({len(rows)} most-cited works):")
        for r in rows:
            print(f"  {r['n']:4d}x  {r['author'] or '?'}, {(r['title'] or '')[:60]} "
                  f"{r['year'] or ''}")

    if args.contents:
        Path(args.out).mkdir(parents=True, exist_ok=True)
        recs = []
        for r in store.db.execute("SELECT DISTINCT source FROM chunks ORDER BY source"):
            rec = source_contents(store, r["source"])
            recs.append(rec)
            print(f"{rec['source'][:44]:46s} {rec['chunks']:5,} chunks  "
                  f"{rec['kind'] or '?':10s} cites {rec['cites_works']:4,} works")
        Path(args.out, "contents.json").write_text(
            json.dumps(recs, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n-> {args.out}/contents.json")

    if args.graph or args.shared:
        edges, works, shared = graph(store)
        if not works:
            print("no works yet — run --extract then --resolve"); return
        if args.graph:
            print(f"{len(works):,} distinct works cited by {len(edges)} source(s)\n")
            for src in sorted(edges):
                top = edges[src].most_common(5)
                names = ", ".join(
                    f"{(works[w]['author'] or '?').split(',')[0]}"
                    f"{' ' + str(works[w]['year']) if works[w]['year'] else ''}"
                    for w, _ in top)
                print(f"  {src[:44]:46s} {len(edges[src]):4,} works | top: {names}")
        if args.shared:
            print("\nworks cited by MORE THAN ONE source "
                  "(shared dependencies — agreement between these sources "
                  "may not be independent):\n")
            for w, n in shared.most_common(30):
                if n < 2:
                    continue
                k = works[w]
                mark = f"  [IN CORPUS: {k['in_corpus']}]" if k.get("in_corpus") else ""
                print(f"  {n} sources  {k['author'] or '?'}, "
                      f"{(k['title'] or '')[:54]} {k['year'] or ''}{mark}")

    if not any([args.extract, args.resolve, args.graph, args.contents,
                args.shared, args.source]):
        for t in ("works", "citations", "bib_entries"):
            n = store.db.execute(f"SELECT COUNT(*) n FROM {t}").fetchone()["n"]
            print(f"  {t:14s} {n:6,}")


if __name__ == "__main__":
    main()
