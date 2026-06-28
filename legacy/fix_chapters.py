#!/usr/bin/env python3
"""
Post-process the extracted Markdown files using POSITION-BASED chapter
assignment.

The per-page extractor sometimes can't see a chapter header (mid-chapter pages
emit placeholder labels like [CHAPTER]) and sometimes misreads the chapter
number outright (a stray "### Verse 60.x" in the middle of chapter 56). So
per-verse chapter numbers are unreliable.

The reliable signal is the first-occurrence `# Chapter N` heading for each
chapter: across the document these appear in strict monotonic order at
positions that match the known chapter sizes. We use them as boundaries and
assign every verse to the chapter whose bracket its line falls in. This:
  * fills placeholder chapters,
  * corrects stray misread chapter numbers,
  * collapses the repeated per-page headings to one canonical heading/chapter.

Verses before the first in-range heading (buffer verses from an adjacent
chapter, e.g. 65.x or 70.x) are left untouched. Verse NUMBERS are never
changed — only the chapter component of the label. Reads/writes UTF-8.
"""

import re
import sys

from extract_verses import FILES

HEADING_RE = re.compile(r"^#\s+Chapter\s+(\d+)\b")
VERSE_RE = re.compile(r"^(### Verse\s+)(.+?)(\.\d.*)$")


def fix_file(file_config: dict, output_dir: str):
    path = f"{output_dir}/{file_config['output']}"
    valid = set(file_config["chapters"].keys())
    titles = {ch: f"# Chapter {ch} — {t}" for ch, t in file_config["chapters"].items()}

    lines = open(path, encoding="utf-8").read().split("\n")

    # Pass 1 — first-occurrence, monotonically increasing headings = boundaries.
    boundaries = []  # list of (line_index, chapter), in document order
    seen = set()
    cur = None
    for i, l in enumerate(lines):
        m = HEADING_RE.match(l)
        if not m:
            continue
        ch = int(m.group(1))
        if ch in valid and ch not in seen and (cur is None or ch > cur):
            boundaries.append((i, ch))
            seen.add(ch)
            cur = ch
    boundary_set = set(boundaries)

    missing = sorted(valid - seen)
    if missing:
        print(f"  WARNING: no heading found for chapter(s) {missing} in {file_config['output']}")

    def chapter_for(line_idx: int):
        ch = None
        for li, c in boundaries:
            if line_idx >= li:
                ch = c
            else:
                break
        return ch

    first_heading_idx = boundaries[0][0] if boundaries else None

    # Pass 2 — rewrite.
    out = []
    relabeled = 0
    dropped_headings = 0
    buffer_dropped = 0
    started = False
    for i, l in enumerate(lines):
        # Everything before the first target chapter heading is adjacent-chapter
        # buffer (+ its flags/blanks). Keep only the leading file-header comments.
        if not started and first_heading_idx is not None and i < first_heading_idx:
            if l.strip().startswith("<!--"):
                out.append(l)
            elif l.strip():
                buffer_dropped += 1
            continue

        m = HEADING_RE.match(l)
        if m:
            ch = int(m.group(1))
            if (i, ch) in boundary_set:
                if not started:
                    out.append("")           # blank line after header comments
                out.append(titles[ch])       # canonical heading, once per chapter
                started = True
            else:
                dropped_headings += 1         # duplicate / stray / out-of-order
            continue

        mv = VERSE_RE.match(l)
        if mv:
            pos_ch = chapter_for(i)
            tok = mv.group(2).strip()
            if tok != str(pos_ch):
                l = f"{mv.group(1)}{pos_ch}{mv.group(3)}"
                relabeled += 1
            out.append(l)
            continue

        out.append(l)

    open(path, "w", encoding="utf-8").write("\n".join(out))
    print(f"{file_config['output']}: {len(boundaries)} chapter boundaries "
          f"{[c for _, c in boundaries]}; relabeled {relabeled} verse chapters; "
          f"dropped {dropped_headings} redundant headings; "
          f"dropped {buffer_dropped} buffer lines")


def main():
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "./output"
    for fc in FILES:
        fix_file(fc, output_dir)


if __name__ == "__main__":
    main()
