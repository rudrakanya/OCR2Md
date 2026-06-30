#!/usr/bin/env python3
r"""
add_translit.py — insert IAST transliteration under every line that contains
Devanagari, in every .md file of a folder (in place).

Deterministic, local, no API tokens. For each line with Devanagari script, the
original line is kept and an italic transliteration line is added beneath it:

    देवनागरी पंक्ति
    *[IAST] devanāgarī paṅkti*

Requires: indic-transliteration
Usage:    python add_translit.py "remaining pdf\md"
"""
import glob
import os
import re
import sys

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

DEVA = re.compile(r"[ऀ-ॿ]")


def process(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    out, added = [], 0
    for ln in lines:
        out.append(ln)
        if DEVA.search(ln):
            iast = transliterate(ln, sanscript.DEVANAGARI, sanscript.IAST).strip()
            out.append(f"*[IAST] {iast}*")
            added += 1
    open(path, "w", encoding="utf-8").write("\n".join(out))
    return added


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    files = sorted(glob.glob(os.path.join(target, "**", "*.md"), recursive=True))
    if not files:
        print(f"No .md files under {target}"); sys.exit(1)
    total = 0
    for f in files:
        n = process(f)
        total += n
        print(f"  {os.path.basename(f)}: +{n} transliteration line(s)")
    print(f"Done. Added {total} IAST line(s) across {len(files)} file(s).")


if __name__ == "__main__":
    main()
