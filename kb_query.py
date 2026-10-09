#!/usr/bin/env python
"""Minimal re-runnable KB query helper for the book-writing pipeline.

Why this exists: `kb_store.py --search` prints source + snippet but NOT the
chunk id, and the outline (and the downstream chapter drafter) must cite
passages by a stable identifier. `KBStore.search_bm25` already returns the
rowid; this is a thin CLI over it, nothing more.

It deliberately depends on nothing but kb_store, because the environment has
lost python-dotenv, mistralai, chromadb, sentence-transformers and rank_bm25 —
so retrieve.py, build_kb.py and src/query.py are all currently unrunnable.
This path is lexical (FTS5/BM25) and entirely offline.

    python kb_query.py "Bhumija sikhara lata kutastambha" -k 8
    python kb_query.py "Udayaditya tank" -k 5 --source Intach
    python kb_query.py "Nataraja tandava" -k 5 --full
    python kb_query.py "prasasti Nagari" -k 5 --json
"""
from __future__ import annotations

import argparse
import json
import sys

import kb_store

try:                                            # Devanagari reaches stdout
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass


def search(query, k=8, source=None, exclude=None, snippet=220, full=False):
    """exclude: substrings of source filenames to drop.

    This exists because label filters do NOT suppress an off-topic source.
    Measured: content="religion_ritual" still returns Temple_Economics.md #3448
    at rank 1, and content="economy" returns #3018 — those chunks genuinely
    carry those labels. Only an explicit source exclusion removes them.
    """
    st = kb_store.KBStore()
    # Over-fetch when filtering client-side so -k still returns k rows.
    widen = bool(source or exclude)
    hits = st.search_bm25(query, k=k * 6 if widen else k)
    if source:
        needle = source.lower()
        hits = [h for h in hits if needle in str(h.get("source", "")).lower()]
    for bad in (exclude or []):
        b = bad.lower()
        hits = [h for h in hits if b not in str(h.get("source", "")).lower()]
    hits = hits[:k]
    out = []
    for h in hits:
        text = str(h.get("text") or "")
        out.append({
            "chunk_id": h.get("rowid"),
            "source": h.get("source"),
            "chunk": h.get("chunk"),
            "trail": h.get("trail"),
            "page_start": h.get("page_start"),
            "score": round(float(h.get("score", 0.0)), 3) if h.get("score") is not None else None,
            "text": text if full else " ".join(text.split())[:snippet],
        })
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Query the Udaypur KB (offline BM25/FTS5)")
    ap.add_argument("query")
    ap.add_argument("-k", type=int, default=8)
    ap.add_argument("--source", help="substring filter on the source filename")
    ap.add_argument("--exclude", action="append", default=[],
                    help="drop sources matching this substring (repeatable); "
                         "e.g. --exclude Temple_Economics")
    ap.add_argument("--full", action="store_true", help="print whole chunk text")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    rows = search(args.query, k=args.k, source=args.source,
                  exclude=args.exclude, full=args.full)
    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return 0
    if not rows:
        print("(no hits)")
        return 1
    for r in rows:
        page = f" p.{r['page_start']}" if r["page_start"] else ""
        score = f"{r['score']:>8.2f}  " if r["score"] is not None else ""
        print(f"{score}#{r['chunk_id']:<6} [{r['source']}]{page}")
        if r["trail"]:
            print(f"          {str(r['trail'])[:96]}")
        print(f"          {r['text']}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
