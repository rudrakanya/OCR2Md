#!/usr/bin/env python3
"""
make_evidence.py — build a per-chapter evidence pack from the vector KB.

For each chapter defined in book_outline.py, runs that chapter's KB search
queries (batched into a single embedding call for efficiency), de-duplicates the
retrieved chunks, and writes them to book/_evidence/chNN.md. Those packs are the
grounded source material that draft_chapter.py writes each chapter from.

Prereqs: build_kb.py has been run (so kb/ exists). MISTRAL_API_KEY in .env.
Usage:   python make_evidence.py [--k 8] [--out book/_evidence]
"""
import argparse
import sys
from pathlib import Path

from book_outline import CHAPTERS
from kb_search import KBError, get_client, search_batch


def build_pack(chapter, k, client):
    """Retrieve and de-duplicate the chunks for one chapter."""
    seen, packed = set(), []
    for hits in search_batch(chapter["queries"], k=k, client=client):
        for r in hits:
            kid = (r["source"], r["heading"], r["chunk"])
            if kid not in seen:
                seen.add(kid)
                packed.append(r)
    return packed


def write_pack(path, chapter, packed):
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Evidence pack — Chapter {chapter['n']}: {chapter['title']}\n\n")
        for r in packed:
            f.write(f"## [{r['source']}] {r['heading']}  (score {r['score']:.2f})\n\n{r['text']}\n\n---\n\n")


def main():
    ap = argparse.ArgumentParser(description="Build per-chapter evidence packs from the vector KB")
    ap.add_argument("--k", type=int, default=8, help="chunks retrieved per query (default 8)")
    ap.add_argument("--out", default="book/_evidence", help="output directory")
    ap.add_argument("--chapters", help="comma-separated chapter numbers (default: all)")
    args = ap.parse_args()

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    wanted = ({int(x) for x in args.chapters.split(",")} if args.chapters else None)

    try:
        client = get_client()
        for ch in CHAPTERS:
            if wanted and ch["n"] not in wanted:
                continue
            packed = build_pack(ch, args.k, client)
            path = outdir / f"ch{ch['n']:02d}.md"
            write_pack(path, ch, packed)
            words = sum(len(r["text"].split()) for r in packed)
            print(f"ch{ch['n']}: {len(packed)} chunks, ~{words} words -> {path}")
    except KBError as e:
        print(f"ERROR: {e}"); sys.exit(1)
    print("Done. Next: python draft_chapter.py all")


if __name__ == "__main__":
    main()
