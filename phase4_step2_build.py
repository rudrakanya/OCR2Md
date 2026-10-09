#!/usr/bin/env python
"""Step 2 — re-chunk the 27 sources into a v2 store, inheriting labels by content.

    python phase4_step2_build.py --sqlite-only     # chunks + labels, no vectors
    python phase4_step2_build.py                   # also embed + build chroma

WHY INHERITANCE, NOT A RE-RUN
-----------------------------
The live store's per-chunk judgements (epistemic_status, relevance_tags,
chapter_scores, cues) come from a paid Stage 1 classification pass over the OLD
chunk boundaries. Re-chunking moves every boundary -- only 3.2% of fresh chunks
are byte-identical to a live one -- so labels cannot be copied by chunk_id, and
re-classifying would mean either an LLM pass (forbidden: it is what produced the
`llm_regenerated` fabrications the audit condemned) or inventing judgements.

So each fresh chunk inherits from the live chunks whose TEXT it overlaps. 93% of
fresh chunks overlap at least one live chunk; the 7% that do not are front
matter, plate lists and contents pages the old pipeline deliberately dropped,
and they are stored inert (not claim-bearing, no chapter bucket, flagged for
review) rather than given invented labels.

INHERITANCE RULES (each chosen to fail safe, not to look tidy)
--------------------------------------------------------------
  epistemic_status   the MOST CAUTIOUS of the constituents. A fresh chunk can
                     span factual prose and a speculative aside; whoever quotes
                     it could quote either, so the chunk takes the weaker claim.
                     speculation > inference > observation > factual
  claim_bearing      true if ANY constituent was
  is_quarantined     true if ANY constituent was -- this is what carries Step 1's
                     ADH quarantine across the rebuild
  relevance_tags     union        chapter_buckets  union
  chapter_scores     max per chapter
  credibility        hit-weighted mean of the constituents
  entities, dates    RECOMPUTED from the fresh text with stage2_build's own
                     deterministic regexes -- no inheritance needed, no model
  source-level       source_type, title, author, scores: from the registry
  provenance         fresh page/heading span, plus the ids inherited from

Quarantined chunks go to a SEPARATE FILE (kb_quarantine_v2.sqlite) and never
enter kb_active_v2.sqlite, which is how the original design made quarantine
unreachable. The in-place flag from Step 1 stays as belt and braces.

Writes only new files. The live store is never opened for writing.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import re
import sqlite3
import sys
import types
import unicodedata
from pathlib import Path

import yaml

for _n in ("mistralai", "mistralai.client"):
    sys.modules.setdefault(_n, types.ModuleType(_n))
sys.modules["mistralai.client"].Mistral = object
sys.modules["mistralai"].Mistral = object

import build_kb                      # noqa: E402  the chunker
import stage2_build as s2            # noqa: E402  entity/date regexes, reused verbatim

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
BOOKS = ROOT / "Udaypur Reference Markdown Files"
K3 = ROOT / "kb3"
REGISTRY = ROOT / "kb_audit" / "source_registry.yaml"
LIVE = K3 / "kb_active.sqlite"
V2 = K3 / "kb_active_v2.sqlite"
V2Q = K3 / "kb_quarantine_v2.sqlite"
REPORT = ROOT / "kb_audit" / "step2_build.json"
NOW = dt.datetime.now().isoformat(timespec="seconds")

W, STRIDE = 32, 16
CAUTION = ["factual", "observation", "inference", "speculation"]   # ascending caution

COLS = ["chunk_id", "parent_source_id", "work_id", "origin", "source_type", "epistemic_status",
        "status_basis", "claim_bearing", "title", "author", "publication_date",
        "publication_date_confidence", "event_date", "event_year_min", "event_year_max",
        "date_confidence", "event_date_basis", "chapter_scores", "chapter_buckets",
        "relevance_tags", "entities", "corroboration_ids", "corroboration_count",
        "contradiction_ids", "contested_claims", "duplicate_of", "superseded_by",
        "is_quarantined", "quarantine_reason", "review_status", "score_primacy",
        "primacy_basis", "score_source_reliability", "score_claim_credibility",
        "credibility_basis", "score_recency", "inference_confidence", "supports",
        "provenance", "cues", "text", "content_hash", "n_chars"]
JSONC = {"chapter_scores", "chapter_buckets", "relevance_tags", "entities", "corroboration_ids",
         "contradiction_ids", "contested_claims", "credibility_basis", "supports",
         "provenance", "cues"}


def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s or "")).strip().lower()


def h16(t):
    return hashlib.sha1(t.encode()).hexdigest()[:16]


def jload(v, d):
    try:
        return json.loads(v) if v else d
    except (TypeError, ValueError):
        return d


def fresh_index(fresh):
    """hash(window) -> set of fresh chunk indices, at STRIDE 1.

    Stride 1 on the indexed side is the whole point: the two chunkings cut the
    text at different places, so sampling both sides at the same stride misses
    real matches. An earlier measurement did that and reported 64% of chunks as
    unmatched, against the 79% coverage the Phase 1 reconciliation had already
    established independently.
    """
    idx = collections.defaultdict(set)
    for i, c in enumerate(fresh):
        t = norm(c["text"])
        for j in range(max(1, len(t) - W + 1)):
            idx[hash(t[j:j + W])].add(i)
    return idx


def build_source(sid, code, reg_entry, scores_entry, live_rows, fresh):
    """Return (records, stats) for one source."""
    idx = fresh_index(fresh)
    votes = collections.defaultdict(collections.Counter)      # fresh idx -> live id -> hits
    for lr in live_rows:
        t = norm(lr["text"])
        probes = [hash(t[j:j + W]) for j in range(0, max(1, len(t) - W + 1), STRIDE)] \
            if len(t) >= W else [hash(t)]
        for p in probes:
            for fi in idx.get(p, ()):
                votes[fi][lr["chunk_id"]] += 1
    del idx

    by_id = {lr["chunk_id"]: lr for lr in live_rows}
    pub = reg_entry.get("publication_date") or reg_entry.get("year")
    recs, n_orphan, n_inherit, n_quar, n_split = [], 0, 0, 0, 0

    for i, c in enumerate(fresh):
        text = c["text"]
        cons = votes.get(i, collections.Counter())
        rows = [(by_id[cid], hits) for cid, hits in cons.most_common() if cid in by_id]
        rec = {k: None for k in COLS}
        rec.update(
            chunk_id=f"{sid}-{i:05d}", parent_source_id=sid,
            work_id=reg_entry.get("work_id") or sid,
            source_type=reg_entry.get("source_type"),
            title=reg_entry.get("title"), author=reg_entry.get("author"),
            publication_date=str(pub) if pub else None,
            score_source_reliability=scores_entry.get("reliability"),
            text=text, content_hash=h16(text), n_chars=len(text),
            corroboration_ids=[], corroboration_count=0, contradiction_ids=[],
            contested_claims=[], supports=None,
            entities=sorted(s2.entity_set(text)),
        )
        # deterministic date extraction, reusing stage2_build's own regexes.
        # event_years returns (lo, hi, confidence, basis) or None.
        ey = s2.event_years(text)
        if ey:
            lo, hi, conf, basis = ey
            rec["event_year_min"], rec["event_year_max"] = lo, hi
            rec["event_date"] = s2.fmt_years(lo, hi)
            rec["date_confidence"] = conf
            rec["event_date_basis"] = "dates in chunk text: " + ", ".join(basis)
        else:
            rec["date_confidence"] = "undated"

        if rows:
            n_inherit += 1
            tot = sum(hits for _, hits in rows) or 1
            # most cautious status wins
            st = max((r["epistemic_status"] or "factual" for r, _ in rows),
                     key=lambda s: CAUTION.index(s) if s in CAUTION else 0)
            tags, buckets, cues = set(), set(), set()
            contested = {}          # contested_claims are dicts: dedup by serialisation
            scores = {}
            for r, _ in rows:
                tags |= set(jload(r["relevance_tags"], []))
                buckets |= set(jload(r["chapter_buckets"], []))
                cues |= set(jload(r["cues"], []))
                for cc in jload(r["contested_claims"], []):
                    contested[json.dumps(cc, sort_keys=True, ensure_ascii=False)] = cc
                for k, v in jload(r["chapter_scores"], {}).items():
                    scores[k] = max(scores.get(k, 0.0), v)
            cred = sum((r["score_claim_credibility"] or 0) * hits for r, hits in rows) / tot
            quar = [(r, hits) for r, hits in rows if r["is_quarantined"]]
            rec.update(
                origin=rows[0][0]["origin"],
                epistemic_status=st, claim_bearing=int(any(r["claim_bearing"] for r, _ in rows)),
                relevance_tags=sorted(tags), chapter_buckets=sorted(buckets),
                chapter_scores={k: round(v, 3) for k, v in sorted(scores.items())},
                cues=sorted(cues), contested_claims=[contested[k] for k in sorted(contested)],
                score_claim_credibility=round(cred, 3),
                credibility_basis=[f"inherited hit-weighted mean over {len(rows)} v1 chunk(s)"],
                score_primacy=rows[0][0]["score_primacy"],
                primacy_basis=rows[0][0]["primacy_basis"],
                score_recency=rows[0][0]["score_recency"],
                inference_confidence=rows[0][0]["inference_confidence"],
                superseded_by=rows[0][0]["superseded_by"],
                status_basis=("inherited from v1 chunks "
                              + ",".join(cid for cid, _ in cons.most_common(4))
                              + f" (most cautious of {sorted({r['epistemic_status'] for r,_ in rows})})"),
            )
            if quar:
                n_quar += 1
                rec["is_quarantined"] = 1
                rec["quarantine_reason"] = quar[0][0]["quarantine_reason"]
                rec["review_status"] = quar[0][0]["review_status"]
            else:
                rec["is_quarantined"] = 0
            prov_src = jload(rows[0][0]["provenance"], {})
        else:
            # No overlap with any classified chunk: front matter, contents pages,
            # plate lists. Stored inert rather than given invented judgements.
            n_orphan += 1
            rec.update(
                epistemic_status="factual", claim_bearing=0,
                relevance_tags=["needs_recheck"], chapter_buckets=[], chapter_scores={},
                cues=[], is_quarantined=0,
                score_primacy=s2.PRIMACY.get(reg_entry.get("source_type"), 0.5),
                primacy_basis=f"source_type {reg_entry.get('source_type')} (v2 orphan default)",
                score_claim_credibility=s2.CRED_BASE.get("factual", 0.8),
                credibility_basis=["no classified v1 chunk overlaps this text"],
                score_recency=0.0, review_status="v2-unclassified",
                status_basis=("no overlap with any classified v1 chunk; unclassified in v2 "
                              "(front matter / contents / plate list). Not claim-bearing, "
                              "no chapter bucket, tagged needs_recheck so it is never quoted."),
            )
            prov_src = {}

        rec["publication_date_confidence"] = reg_entry.get("publication_date_confidence") \
            or prov_src.get("date_confidence") or "approximate"
        rec["provenance"] = {
            "file": reg_entry.get("file"), "title": reg_entry.get("title"),
            "author": reg_entry.get("author"),
            "publication_date": str(pub) if pub else None,
            "heading_trail": c.get("trail") or "", "page_start": c.get("page_start"),
            "page_end": c.get("page_end"),
            "printed_page": prov_src.get("printed_page"),
            "v2_inherited_from": [cid for cid, _ in cons.most_common(6)],
            "v2_overlap_hits": sum(cons.values()),
        }

        # Quarantine the fabrication, not the prose beside it. ADH's damage is
        # entirely in markdown table rows, and one chunk held the genuine
        # decorative-motifs paragraph alongside a collapsed table -- it would
        # have been quarantined with it and lost from the active store. Where a
        # quarantined chunk also carries real prose, split it: prose stays
        # active, the table rows go to quarantine under the same reason.
        if rec["is_quarantined"]:
            keep = "\n".join(l for l in text.split("\n")
                             if not l.lstrip().startswith("|")).strip()
            drop = "\n".join(l for l in text.split("\n")
                             if l.lstrip().startswith("|")).strip()
            if len(keep) >= 120 and drop:
                clean = dict(rec)
                clean.update(text=keep, content_hash=h16(keep), n_chars=len(keep),
                             is_quarantined=0, quarantine_reason=None, review_status=None,
                             entities=sorted(s2.entity_set(keep)),
                             status_basis=(rec["status_basis"] +
                                           "; split from a quarantined chunk - "
                                           "fabricated table rows removed"))
                recs.append(clean)
                rec = dict(rec)
                rec.update(chunk_id=rec["chunk_id"] + "-q", text=drop,
                           content_hash=h16(drop), n_chars=len(drop))
                n_split += 1

        recs.append(rec)
    return recs, {"code": code, "source_id": sid, "v1": len(live_rows), "v2": len(fresh),
                  "inherited": n_inherit, "orphan": n_orphan, "quarantined": n_quar,
                  "split": n_split}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sqlite-only", action="store_true")
    a = ap.parse_args()

    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    registry = {s["source_id"]: s for s in reg["sources"]}
    scores = yaml.safe_load((K3 / "source_scores.yaml").read_text(encoding="utf-8"))["sources"]

    db = sqlite3.connect(f"file:{LIVE}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row

    sources = [s for s in reg["sources"] if (BOOKS / s.get("file", "")).exists()]
    print(f"re-chunking {len(sources)} sources\n")
    print(f"{'code':9s} {'v1':>6s} {'v2':>6s} {'inherit':>8s} {'orphan':>7s} {'quar':>5s}")

    all_recs, stats = [], []
    for s in sources:
        sid, code = s["source_id"], s.get("code", "?")
        live_rows = list(db.execute("select * from chunks where parent_source_id=?", (sid,)))
        fresh = build_kb.chunk_markdown(BOOKS / s["file"])
        recs, st = build_source(sid, code, s, scores.get(sid, {}), live_rows, fresh)
        all_recs += recs
        stats.append(st)
        print(f"{code:9s} {st['v1']:6d} {st['v2']:6d} {st['inherited']:8d} "
              f"{st['orphan']:7d} {st['quarantined']:5d}")

    T = {k: sum(x[k] for x in stats) for k in ("v1", "v2", "inherited", "orphan", "quarantined", "split")}
    print(f"\n{'TOTAL':9s} {T['v1']:6d} {T['v2']:6d} {T['inherited']:8d} "
          f"{T['orphan']:7d} {T['quarantined']:5d}")

    # ---- write the two stores ---------------------------------------------
    for p in (V2, V2Q):
        p.unlink(missing_ok=True)
    act, qua = sqlite3.connect(str(V2)), sqlite3.connect(str(V2Q))
    ddl = "create table chunks (rowid integer primary key, " + ", ".join(f'"{k}"' for k in COLS) + ")"
    act.execute(ddl)
    qua.execute(ddl.replace("chunks (", "chunks (quarantined_at, "))
    act.execute("create virtual table chunks_fts using fts5(text, aliases, "
                "tokenize='unicode61 remove_diacritics 2')")
    act.execute("create table meta (k primary key, v)")
    act.execute("create table links (a, b, kind, basis)")

    def row(c):
        return [json.dumps(c.get(k), ensure_ascii=False) if k in JSONC else c.get(k) for k in COLS]

    ph = ",".join("?" * len(COLS))
    cols_q = ",".join(f'"{k}"' for k in COLS)
    n_act = n_qua = 0
    for c in all_recs:
        if c["is_quarantined"]:
            qua.execute(f"insert into chunks (quarantined_at, {cols_q}) values (?, {ph})",
                        [NOW] + row(c))
            n_qua += 1
        else:
            cur = act.execute(f"insert into chunks ({cols_q}) values ({ph})", row(c))
            act.execute("insert into chunks_fts (rowid, text, aliases) values (?,?,?)",
                        (cur.lastrowid, c["text"], " ".join(c["entities"])))
            n_act += 1
    for k, v in (("built_at", NOW), ("version", "phase4-step2/v2"),
                 ("dense", "pending"),
                 ("note", "v2 store: re-chunked from markdown, labels inherited by content "
                          "overlap from kb_active.sqlite. Quarantine lives in "
                          "kb_quarantine_v2.sqlite, which retrieval never opens.")):
        act.execute("insert into meta values (?,?)", (k, v))
    act.commit(); qua.commit()
    act.close(); qua.close()
    print(f"\nwrote {V2.name}: {n_act} active | {V2Q.name}: {n_qua} quarantined")

    REPORT.write_text(json.dumps({"built_at": NOW, "rows": stats, "totals": T,
                                  "active": n_act, "quarantined": n_qua},
                                 indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
