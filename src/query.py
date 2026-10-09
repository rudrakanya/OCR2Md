"""Retrieval CLI (§9).

    python -m src.query "Bhumija sikhara of the Udayesvara temple"
    python -m src.query "praśasti of Udayāditya" --chapter C10 --k 5
    python -m src.query "Betwa monsoon" --no-hybrid --json
"""
from __future__ import annotations

import argparse
import json
import sys

from . import settings as st
from .retrieval import Retriever
from .store import open_aligned
from .textutil import snippet


def format_hit(i: int, hit, snippet_chars: int, show_channels: bool = True) -> str:
    m = hit.metadata
    year = f" {m['book_year']}" if m.get("book_year") else ""
    author = f" — {m['author']}" if m.get("author") else ""
    chapters = m.get("chapters_str", "")
    primary = m.get("primary_chapter", "?")
    dup = ""
    if m.get("is_duplicate"):
        dup = f"  [duplicate of {str(m.get('duplicate_of',''))[:8]}, demoted]"

    lines = [
        f"{i:2d}. {hit.book}{author}{year}",
        f"    {hit.heading}",
        f"    chapters: {primary} (primary) · all: {chapters or '—'}{dup}",
    ]
    scores = [f"fused {hit.fused:.4f}"]
    if hit.dense_score is not None:
        scores.append(f"dense #{hit.dense_rank} cos={hit.dense_score:.4f}")
    if hit.lexical_score is not None:
        scores.append(f"bm25 #{hit.lexical_rank}={hit.lexical_score:.2f}")
    if show_channels:
        lines.append(f"    {' · '.join(scores)}")
    page = f"  (p.{m['page_start']})" if m.get("page_start") else ""
    lines.append(f"    {snippet(hit.text, snippet_chars)}{page}")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Query the Udaypur corpus")
    ap.add_argument("query", help="the search text")
    ap.add_argument("--chapter", help="restrict to a chapter, e.g. C08")
    ap.add_argument("--k", type=int, default=None)
    ap.add_argument("--hybrid", dest="hybrid", action="store_true", default=None)
    ap.add_argument("--no-hybrid", dest="hybrid", action="store_false")
    ap.add_argument("--include-duplicates", action="store_true",
                    help="do not demote chunks flagged as near-duplicates")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--snippet", type=int, default=None)
    ap.add_argument("--embed-preset", default=None,
                    help="force a model; by default the collection's own is used")
    args = ap.parse_args(argv)

    cfg, store = open_aligned(st.load(), preset=args.embed_preset, verbose=False)
    retriever = Retriever(cfg, store=store)
    try:
        hits = retriever.search(args.query, k=args.k, chapter=args.chapter,
                                hybrid=args.hybrid,
                                include_duplicates=args.include_duplicates)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([{
            "chunk_id": h.chunk_id, "book": h.book, "heading": h.heading,
            "primary_chapter": h.metadata.get("primary_chapter"),
            "chapters": h.metadata.get("chapters_str"),
            "fused": h.fused, "dense_score": h.dense_score,
            "lexical_score": h.lexical_score, "channels": h.channels,
            "text": h.text,
        } for h in hits], indent=2, ensure_ascii=False))
        return 0

    mode = "hybrid (dense+bm25, RRF)" if any(
        h.lexical_rank for h in hits) else "dense only"
    filt = f"  filter chap_{args.chapter}=True" if args.chapter else ""
    print(f"\nquery: {args.query!r}   [{mode}]{filt}")
    print(f"{len(hits)} hits\n" + "─" * 78)
    snip = args.snippet or int(cfg.get_path("retrieval.snippet_chars", 320))
    for i, h in enumerate(hits, 1):
        print(format_hit(i, h, snip))
        print()
    if not hits:
        print("  (nothing matched — if you used --chapter, try without it)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
