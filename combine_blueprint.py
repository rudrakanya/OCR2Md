#!/usr/bin/env python3
"""
combine_blueprint.py — stitch the per-chapter blueprints into one document.

Reads book/_blueprint/INDEX.md and ch01..chNN.md and writes a single
BLUEPRINT.md: title page, the coverage index, a linked table of contents built
from each chapter's units, then every chapter in order.

The per-chapter files stay the source of truth — this is a derived artefact and
is safe to delete and rebuild. Chapter files keep their own '# Chapter N'
headings, so anchors and internal structure are unchanged.

Usage:
    python combine_blueprint.py                       # -> book/_blueprint/BLUEPRINT.md
    python combine_blueprint.py --out BOOK_PLAN.md
"""
import argparse
import re
from datetime import datetime, timezone
from pathlib import Path

from console import use_utf8

SRC = Path("book/_blueprint")


def anchor(text):
    """GitHub-style heading anchor."""
    a = text.strip().lower()
    a = re.sub(r"[^\w\s-]", "", a)
    return re.sub(r"\s+", "-", a)


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Combine the chapter blueprints into one document")
    ap.add_argument("--src", default=str(SRC), help="folder holding chNN.md and INDEX.md")
    ap.add_argument("--out", default=None, help="output path (default: <src>/BLUEPRINT.md)")
    args = ap.parse_args()

    src = Path(args.src)
    out = Path(args.out) if args.out else src / "BLUEPRINT.md"

    chapters = sorted(src.glob("ch[0-9][0-9].md"), key=lambda p: int(p.stem[2:]))
    if not chapters:
        print(f"ERROR: no chNN.md files in {src}/"); return

    index = (src / "INDEX.md")
    index_body = ""
    if index.exists():
        # Drop the file's own H1; it becomes a section of the combined document.
        index_body = re.sub(r"\A#\s+.*\n", "", index.read_text(encoding="utf-8")).strip()

    kb = ""
    m = re.search(r"<!--\s*kb ([0-9a-f]+),\s*(\d+) chunks", index_body or "")
    if m:
        kb = f"knowledge base `{m.group(1)}`, {int(m.group(2)):,} chunks"

    parts = [
        "# The Rising Lord — Research Blueprint",
        "",
        "*The Nīlakaṇṭheśvara (Udayeśvara) Temple of Udaypur "
        "and the World of the Paramāra Rajputs*",
        "",
        "A research architecture, not a manuscript: every chapter decomposed into units, "
        "sub-units, topics, research questions, required evidence, a reference mapping drawn "
        "from the project knowledge base, and a citation plan. Each unit is written to be "
        "researchable and drafted independently.",
        "",
        f"<!-- combined {datetime.now(timezone.utc).isoformat(timespec='seconds')} "
        f"from {len(chapters)} chapter blueprints -->",
        "",
        f"*Generated {datetime.now(timezone.utc).strftime('%d %B %Y')}"
        + (f" · {kb}" if kb else "") + f" · {len(chapters)} chapters*",
        "",
        "---",
        "",
        "## Coverage index",
        "",
        index_body,
        "",
        "---",
        "",
        "## Contents",
        "",
    ]

    # Table of contents: chapter, then its units, linked to their headings.
    bodies = []
    for p in chapters:
        text = p.read_text(encoding="utf-8").strip()
        bodies.append(text)
        title_m = re.match(r"#\s+(.+)", text)
        title = title_m.group(1).strip() if title_m else p.stem
        parts.append(f"- [{title}](#{anchor(title)})")
        for um in re.finditer(r"(?m)^##\s+(Unit\s+[\d.]+\s+—\s+.+)$", text):
            u = um.group(1).strip()
            parts.append(f"    - [{u}](#{anchor(u)})")

    parts += ["", "---", ""]
    parts.append("\n\n---\n\n".join(bodies))
    parts.append("")

    out.write_text("\n".join(parts), encoding="utf-8")
    words = len(out.read_text(encoding="utf-8").split())
    print(f"Combined {len(chapters)} chapters -> {out}")
    print(f"  {out.stat().st_size:,} bytes, ~{words:,} words")


if __name__ == "__main__":
    main()
