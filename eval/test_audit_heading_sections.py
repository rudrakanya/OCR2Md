#!/usr/bin/env python3
"""Offline tests for eval/audit_heading_sections.py's pure functions, using
synthetic markdown text. No corpus read, no collection access.

    python eval/test_audit_heading_sections.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

from eval.audit_heading_sections import classify, raw_headings  # noqa: E402
from src.chunker import _compile_junk, split_sections  # noqa: E402

FAILED: list[str] = []


def check(name, cond, detail=""):
    print(f"  {'ok  ' if cond else 'FAIL'}  {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILED.append(name)


SPLIT_LEVELS = 3
JUNK = _compile_junk([])


def test_truly_empty_sibling_heading_is_dropped():
    text = "## Title Page Heading\n\n## Real Content\n\nThis is a real paragraph with actual words.\n"
    sections = split_sections(text, SPLIT_LEVELS, JUNK)
    kept = {tuple(s.heading_path) for s in sections}
    check("the empty sibling heading is dropped (no section for it alone)",
          ("Title Page Heading",) not in kept, str(kept))
    check("the following heading with real content is kept",
          ("Real Content",) in kept, str(kept))


def test_child_heading_rescues_parent_name_in_path():
    text = "## Parent Divider\n### Child With Content\n\nSome real body text under the child.\n"
    sections = split_sections(text, SPLIT_LEVELS, JUNK)
    kept = {tuple(s.heading_path) for s in sections}
    check("parent name survives as an ancestor component of the child's heading_path",
          any("Parent Divider" in path for path in kept), str(kept))
    check("no standalone section exists for the parent alone",
          ("Parent Divider",) not in kept, str(kept))


def test_classify_empty_body():
    check("whitespace-only body classifies as intentionally_empty_or_divider",
          classify("H", ["", "   ", ""]) == "intentionally_empty_or_divider")


def test_classify_furniture_only_body():
    check("markdown furniture with no letters classifies as intentionally_empty_or_divider",
          classify("H", ["---", "***", "|---|---|"]) == "intentionally_empty_or_divider")


def test_raw_headings_skips_junk_and_over_level():
    junk = _compile_junk([r"(?i)library stamp"])
    text = ("# Kept H1\n"
            "## Library Stamp Here\n"
            "#### Too Deep For split_levels=3\n"
            "## Also Kept\n")
    found = raw_headings(text, split_levels=3, junk=junk)
    titles = [t for (_, _, t) in found]
    check("level-1 heading is included", "Kept H1" in titles)
    check("junk-pattern heading is excluded", "Library Stamp Here" not in titles)
    check("a heading deeper than split_levels is excluded", "Too Deep For split_levels=3" not in titles)
    check("a normal level-2 heading is included", "Also Kept" in titles)


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for t in tests:
        print(f"\n{t.__name__}")
        t()
    print("\n" + ("ALL CHECKS PASSED" if not FAILED else f"{len(FAILED)} FAILED: {FAILED}"))
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
