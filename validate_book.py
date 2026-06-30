#!/usr/bin/env python3
"""
validate_book.py — integrity check for the drafted chapters.

For each chapter in book_outline.py, reports: body word count, endnote-marker vs
notes consistency, Devanagari/IAST character counts, mojibake hits, first-person
pronoun hits (should be ~0 for a third-person book; quotes/roman-numerals may
show as false positives), and [GAP] flags. Missing chapters are reported, not
fatal.

Usage: python validate_book.py [--dir book]
"""
import argparse
import re
from pathlib import Path

from book_outline import CHAPTERS


def main():
    ap = argparse.ArgumentParser(description="Validate drafted chapters")
    ap.add_argument("--dir", default="book")
    args = ap.parse_args()
    d = Path(args.dir)

    hdr = f"{'ch':<4}{'body_w':>7}{'markers':>9}{'notes':>7}{'seq':>6}{'deva':>7}{'iast':>7}{'moji':>6}{'1st':>5}{'gaps':>6}"
    print(hdr)
    print("-" * len(hdr))
    for c in CHAPTERS:
        fp = d / f"chapter-{c['n']:02d}.md"
        if not fp.exists():
            print(f"{c['n']:<4}  MISSING ({fp})")
            continue
        t = fp.read_text(encoding="utf-8")
        parts = re.split(r"(?m)^##\s+Notes\s*$", t)
        body, notes = parts[0], (parts[1] if len(parts) > 1 else "")
        bmarks = [int(x) for x in re.findall(r"\[(\d+)\]", body)]
        nmarks = [int(m.group(1)) for m in re.finditer(r"(?m)^\[(\d+)\]", notes)]
        distinct = sorted(set(bmarks))
        seq = (distinct == list(range(1, len(distinct) + 1))
               and nmarks == list(range(1, len(nmarks) + 1))
               and len(distinct) == len(nmarks))
        deva = len(re.findall(r"[ऀ-ॿ]", t))
        iast = len(re.findall(r"[āīūṛṝḷṃḥṅñṭḍṇśṣ]", t))
        moji = len(re.findall(r"[ÃÂ][\x80-\xbf]|â€", t))
        fp_hits = len(re.findall(r"\bI\b|\bwe\b|\bus\b|\bour\b|\byou\b|\byour\b", body))
        gaps = body.count("[GAP")
        print(f"{c['n']:<4}{len(body.split()):>7}{len(bmarks):>9}{len(nmarks):>7}{str(seq):>6}"
              f"{deva:>7}{iast:>7}{moji:>6}{fp_hits:>5}{gaps:>6}")
    print("\nnote: 'seq' True = endnote markers and notes align 1..N (repeats allowed); "
          "'1st' counts may be false positives (roman numerals like 'Vakpati I', quotes).")


if __name__ == "__main__":
    main()
