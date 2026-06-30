#!/usr/bin/env python3
"""
assemble_book.py — stitch the drafted chapters + bibliography into one manuscript.

Reads book/chapter-NN.md for every chapter in book_outline.py and writes
book/<title>_manuscript.md with a title page and contents. Missing chapters are
reported and skipped (with a placeholder) rather than crashing.

Usage: python assemble_book.py [--dir book]
"""
import argparse
import re
from pathlib import Path

from book_outline import BOOK_TITLE, BOOK_SUBTITLE, CHAPTERS


def main():
    ap = argparse.ArgumentParser(description="Assemble drafted chapters into one manuscript")
    ap.add_argument("--dir", default="book", help="folder holding chapter-NN.md (default: book)")
    args = ap.parse_args()
    d = Path(args.dir)

    contents = "".join(f"{c['n']}. {c['title']}\n" for c in CHAPTERS) + f"{len(CHAPTERS) + 1}. Bibliography\n"
    parts = [
        f"# {BOOK_TITLE}\n## {BOOK_SUBTITLE}\n\n"
        "*A working draft, written in third-person narrative history and grounded, via a vector "
        "knowledge base, in the Udaypur reference corpus.*\n",
        "\n## Contents\n\n" + contents,
    ]

    body_words, missing = 0, []
    for c in CHAPTERS:
        fp = d / f"chapter-{c['n']:02d}.md"
        if fp.exists():
            txt = fp.read_text(encoding="utf-8").strip()
            body_words += len(txt.split())
            parts.append("\n\n---\n\n" + txt)
        else:
            missing.append(c["n"])
            parts.append(f"\n\n---\n\n# Chapter {c['n']} — {c['title']}\n\n*[Not yet drafted.]*")

    bib = d / "Bibliography.md"
    if bib.exists():
        parts.append("\n\n---\n\n" + bib.read_text(encoding="utf-8").strip())

    out = d / f"{BOOK_TITLE.replace(' ', '_')}_manuscript.md"
    out.write_text("\n".join(parts), encoding="utf-8")
    print(f"Assembled {out}  (~{body_words} words across {len(CHAPTERS) - len(missing)}/{len(CHAPTERS)} chapters"
          + (f"; MISSING {missing}" if missing else "; complete") + ")")


if __name__ == "__main__":
    main()
