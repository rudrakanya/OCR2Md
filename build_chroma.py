#!/usr/bin/env python
"""Phase 4 — build the ChromaDB store from the scored Stage 2 stores.

    python build_chroma.py                 # idempotent upsert of all 27 sources
    python build_chroma.py --reset         # drop the collections and rebuild

Reads:
    kb3/kb_active.sqlite      scored, bucketed, live chunks
    kb3/kb_quarantine.sqlite  the archive
    kb3/emb_e5/               local multilingual vectors (384-d, e5-small int8)

Writes:
    kb3/chroma/               persistent Chroma client
      collection "udaypur_kb"          everything retrieval may see
      collection "udaypur_kb_archive"  quarantined chunks: same schema, never queried

IDS ARE FROZEN: "<content_hash>-<parent_source_id>". Ordinal chunk ids shift
whenever chunking changes, so they are metadata, not identity. Re-running this
script upserts in place instead of duplicating.

CHROMA METADATA holds scalars only, so every list is stored twice: as a joined
string a human can read, and as booleans a `where` filter can use —
`in_C5: true`, `tag_folklore: true`. That is what makes chapter-scoped
retrieval a filter rather than a re-rank.

QUARANTINE IS A SEPARATE COLLECTION (spec E). The query layer never names it,
so archived chunks are unreachable rather than down-ranked. `is_archived` is
also carried on every record as a hard flag.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
K3 = ROOT / "kb3"
CHROMA = K3 / "chroma"
ACTIVE, ARCHIVE = "udaypur_kb", "udaypur_kb_archive"
CHAPTERS = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10",
            "C11", "C12", "C13", "C14", "C15", "C16", "AF"]
FLAG_TAGS = ["folklore", "opinion", "llm_regenerated", "ai_derived", "thematic", "yoga_doctrine",
             "bhoja_authorship", "editor_introduction", "needs_recheck", "single_source",
             "udaypur_specific", "contested", "original_script", "embeds_primary_text",
             "prescriptive", "scriptural_register", "ocr_damaged", "footnote", "verify_before_use"]


def load_vectors():
    vec = {}
    for f in sorted((K3 / "emb_e5").glob("part_*.json")):
        hs = json.loads(f.read_text())
        arr = np.load(f.with_suffix(".npy")).astype(np.float32)
        vec.update(zip(hs, arr))
    return vec


def rows(db_path: Path):
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    yield from db.execute("select * from chunks")


def meta_of(r, archived: bool):
    prov = json.loads(r["provenance"] or "{}")
    # Model-written synthesis is archived and un-bucketed: it is not a source, so
    # it must not reach chapter retrieval at all. `is_archived` alone would not do
    # it — the query layer filters on in_<chapter>, not on the flag.
    synthetic = ((r["origin"] or "").strip().lower() == "ai-derived"
                 or "ai_derived" in json.loads(r["relevance_tags"] or "[]"))
    # A quarantined row must leave retrieval by the same door synthetic text
    # does. Marking it unquotable is not enough: ADH's 50 fabricated table rows
    # were `factual` and claim-bearing with C7/C10 buckets, and a rebuild would
    # have re-admitted them to those buckets as non-quotable "evidence".
    quarantined = bool(r["is_quarantined"]) or r["quarantine_reason"] is not None
    excluded = synthetic or quarantined
    if excluded:
        archived = True
    buckets = [] if excluded else [b.split(":")[0] for b in json.loads(r["chapter_buckets"] or "[]")]
    admitted = set() if excluded else {
        b.split(":")[0] for b in json.loads(r["chapter_buckets"] or "[]") if b.endswith(":admitted")}
    tags = set(json.loads(r["relevance_tags"] or "[]"))
    scores = json.loads(r["chapter_scores"] or "{}")
    page = prov.get("printed_page") or prov.get("page_start")
    # Model-written text is never quotable as a source. The tag is `ai_derived`
    # (origin "AI-derived"); it was missing from this list, so six synthesis
    # chunks shipped as quotable into ten chapter buckets.
    quotable = (not archived
                and "llm_regenerated" not in tags
                and "ai_derived" not in tags
                and "needs_recheck" not in tags
                and (r["origin"] or "").strip().lower() != "ai-derived"
                and r["quarantine_reason"] is None)
    m = {
        "chunk_id": r["chunk_id"],
        "parent_source_id": r["parent_source_id"],
        "work_id": r["work_id"] or r["parent_source_id"],
        "source_type": r["source_type"],
        "epistemic_status": r["epistemic_status"] or "",
        "claim_bearing": bool(r["claim_bearing"]),
        "title": (r["title"] or "")[:300],
        "author": (r["author"] or "")[:300],
        "publication_date": str(r["publication_date"] or ""),
        "event_date": str(r["event_date"] or ""),
        "date_confidence": r["date_confidence"] or "undated-flagged",
        "page": int(page) if isinstance(page, int) else (str(page) if page else ""),
        "provenance": f"{prov.get('file', '')} | {(prov.get('heading_trail') or '')[:160]}",
        "page_image": prov.get("page_image") or "",
        "chapter_buckets": ",".join(buckets),
        "relevance_tags": ",".join(sorted(tags)),
        "corroboration_count": int(r["corroboration_count"] or 0),
        "contradiction_count": len(json.loads(r["contradiction_ids"] or "[]")),
        "duplicate_of": r["duplicate_of"] or "",
        "superseded_by": r["superseded_by"] or "",
        "is_quotable": bool(quotable),
        "is_archived": bool(archived),
        "quarantine_reason": r["quarantine_reason"] or "",
        "ocr_gate": (r["status_basis"] or "")[:120] if False else "",
        "score_primacy": float(r["score_primacy"] or 0),
        "score_source_reliability": float(r["score_source_reliability"] if r["score_source_reliability"] is not None else 0.5),
        "score_claim_credibility": float(r["score_claim_credibility"] or 0),
        "score_recency": float(r["score_recency"]) if r["score_recency"] is not None else -1.0,
        "layer": r["origin"] if "origin" in r.keys() and r["origin"] else "",
    }
    for ch in CHAPTERS:
        m[f"in_{ch}"] = ch in buckets
        m[f"rel_{ch}"] = float(scores.get(ch, 0.0))
        if ch in admitted:
            m[f"admitted_{ch}"] = True
    for t in FLAG_TAGS:
        if t in tags:
            m[f"tag_{t}"] = True
    return m


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--reset", action="store_true")
    ap.add_argument("--batch", type=int, default=1000)
    a = ap.parse_args(argv)
    import chromadb

    vec = load_vectors()
    print(f"{len(vec):,} vectors")
    client = chromadb.PersistentClient(path=str(CHROMA))
    if a.reset:
        for n in (ACTIVE, ARCHIVE):
            try:
                client.delete_collection(n)
            except Exception:
                pass
    meta_common = {"hnsw:space": "cosine"}
    col = client.get_or_create_collection(ACTIVE, metadata=meta_common)
    arc = client.get_or_create_collection(ARCHIVE, metadata=meta_common)

    totals = {}
    for name, target, db, archived in ((ACTIVE, col, K3 / "kb_active.sqlite", False),
                                       (ARCHIVE, arc, K3 / "kb_quarantine.sqlite", True)):
        ids, docs, metas, embs, missing = [], [], [], [], 0
        for r in rows(db):
            h = r["content_hash"]
            v = vec.get(h)
            if v is None:
                missing += 1
                continue
            ids.append(f"{h}-{r['parent_source_id']}")
            docs.append(r["text"])
            metas.append(meta_of(r, archived))
            embs.append(v.tolist())
        # frozen ids can repeat when the same text appears twice in one source
        seen, u_ids, u_docs, u_meta, u_emb = set(), [], [], [], []
        for i, d, m, e in zip(ids, docs, metas, embs):
            if i in seen:
                continue
            seen.add(i)
            u_ids.append(i); u_docs.append(d); u_meta.append(m); u_emb.append(e)
        for s in range(0, len(u_ids), a.batch):
            target.upsert(ids=u_ids[s:s + a.batch], documents=u_docs[s:s + a.batch],
                          metadatas=u_meta[s:s + a.batch], embeddings=u_emb[s:s + a.batch])
            print(f"  {name}: {min(s + a.batch, len(u_ids)):,}/{len(u_ids):,}", flush=True)
        totals[name] = (len(u_ids), missing, len(ids) - len(u_ids))
    print()
    for n, (k, miss, dup) in totals.items():
        print(f"{n}: {k:,} records (skipped {miss} without a vector, {dup} duplicate frozen ids)")
    print(f"counts in store: active={col.count():,} archive={arc.count():,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
