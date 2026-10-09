#!/usr/bin/env python
"""Smoke test for the chapter pipeline and the sourcebook build.

    python test_pipeline.py

`chapter_pipeline.py` is now large enough that patching it by matching anchor
strings is fragile: a patch that half-applies can leave the CLI dispatching to a
function that does not exist, and nothing notices until someone runs that
subcommand. This checks the wiring and the pure helpers, reads nothing from the
network, writes nothing outside a temp folder, and touches no chapter.
"""
from __future__ import annotations

import inspect
import json
import pathlib
import re
import shutil
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

FAILED: list[str] = []


def check(name, cond, detail=""):
    print(f"  {'ok  ' if cond else 'FAIL'}  {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILED.append(name)


def main():
    import chapter_pipeline as cp

    print("CLI wiring")
    src = (ROOT / "chapter_pipeline.py").read_text(encoding="utf-8")
    declared = set(re.findall(r'sub\.add_parser\("([\w-]+)"\)', src))
    dispatched = set(re.findall(r'n\.cmd == "([\w-]+)"', src))
    check("every subcommand is dispatched", declared <= dispatched,
          f"declared but never dispatched: {sorted(declared - dispatched)}")
    check("no dispatch for a missing subcommand", dispatched <= declared,
          f"dispatched but never declared: {sorted(dispatched - declared)}")
    for fn in sorted(set(re.findall(r"return (cmd_\w+)\(", src)) |
                     set(re.findall(r"^\s+(cmd_\w+)\(", src, re.M))):
        check(f"{fn} exists", hasattr(cp, fn) and callable(getattr(cp, fn)))

    print("\nregexes compile and carry no control characters")
    for name, val in vars(cp).items():
        if isinstance(val, re.Pattern):
            check(f"{name} is clean", "\x08" not in val.pattern and "\x01" not in val.pattern,
                  "contains a literal backspace or SOH — a \\b escape was eaten by a shell")

    print("\noutline parsing, both formats")
    pipe = "### Section 1 Opening\nEvidence: `a`\n\n### Section 2 Middle\nEvidence: `b`\n\n### Sources\nx\n"
    hand = '## 1.1 Arrival (~900 w) — Tiwari\n\ntext `x`\n\n## 1.2 The inventory (~900 w)\n\nmore\n\n## Drafting order and budgets\n\nz\n'
    a, b = cp.outline_sections(pipe), cp.outline_sections(hand)
    check("pipeline format parses two sections", len(a) == 2, f"got {len(a)}")
    check("hand-written format parses two sections", len(b) == 2, f"got {len(b)}")
    check("apparatus headings are skipped",
          not any("Sources" in s["label"] or "Drafting order" in s["label"] for s in a + b))
    check("resolve by number", cp.resolve_section(b, "1.2")["key"] == "1.2")
    check("resolve by position", cp.resolve_section(b, "1")["key"] == "1.1")
    check("resolve by name", cp.resolve_section(b, "inventory")["key"] == "1.2")
    check("unknown section resolves to None", cp.resolve_section(b, "9.9") is None)
    check("dotted stem is filename-safe", cp.section_stem(b[0]) == "1_1", cp.section_stem(b[0]))
    check("integer stem keeps zero padding", cp.section_stem(a[1]) == "02", cp.section_stem(a[1]))
    check("word budget stripped from a synthesised heading",
          cp.clean_heading(b[0]) == "## 1.1 Arrival", cp.clean_heading(b[0]))

    print("\nsentence splitting keeps markers and abbreviations intact")
    s = cp.sentences("Built in V.S. 1116 (1059 CE) [src: x]. It stood. [ed]")
    check("abbreviation does not split a sentence", len(s) == 2, f"{len(s)}: {s}")
    check("trailing marker stays with its sentence", "[ed]" in s[-1], str(s))

    print("\nstatus rules and the sourcebook sidecar")
    check("every status has a prose rule",
          set(cp.STATUS_RULE) >= {"established", "single-source", "contested", "unverified", "gap"})
    sb = cp.load_sourcebook("C1")
    if sb:
        check("C1 sidecar carries facts", bool(sb.get("facts")))
        check("every fact has a known status",
              all(f["status"] in cp.STATUS_RULE for f in sb["facts"]),
              str({f["status"] for f in sb["facts"]} - set(cp.STATUS_RULE)))
        check("source codes are loaded", len(sb.get("codes", {})) > 20, str(len(sb.get("codes", {}))))
    else:
        print("  skip  no kb3/sourcebook_facts.json — run build_sourcebook.py")

    print("\ncurated facts resolve against the KB")
    cur = ROOT / "curated_facts.yaml"
    if cur.exists():
        import yaml
        data = yaml.safe_load(cur.read_text(encoding="utf-8")) or {}
        ids = []
        for fct in data.get("facts", []):
            ids += list(fct.get("supporting_chunks") or []) + list(fct.get("chunks") or [])
            for pos in fct.get("positions", []):
                ids += list(pos.get("chunks") or [])
        dossiers = list((ROOT / "chapters").glob("*/dossier.json"))
        known = set()
        for d in dossiers:
            known |= set(json.loads(d.read_text(encoding="utf-8")))
        unknown = [i for i in ids if i not in known] if known else []
        check("curated chunk ids appear in some dossier", not unknown,
              f"not found in any dossier (may still be in the KB): {unknown[:4]}")
    else:
        print("  skip  no curated_facts.yaml")

    print("\nassemble writes into a temp folder and preserves markers")
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="pipetest-"))
    try:
        (tmp / "sections").mkdir()
        (tmp / "handoff").mkdir()
        (tmp / "outline.md").write_text("## 1.1 Opening (~100 w)\n\nwrite it `z`\n", encoding="utf-8")
        (tmp / "sections" / "1_1.md").write_text(
            "First line [src: z]. Second line. [ed]\n", encoding="utf-8")
        (tmp / "dossier.json").write_text("{}", encoding="utf-8")
        real_folder, real_state = cp.folder, cp.state
        cp.folder = lambda cid: tmp
        cp.state = lambda cid, **u: {"approved_outline": "t"}
        try:
            cp.cmd_assemble("C1")
            out = sorted(tmp.glob("draft-v*.md"))[0].read_text(encoding="utf-8")
            check("assembled draft keeps its [src:] marker", "[src: z]" in out)
            check("assembled draft keeps its [ed] marker", "[ed]" in out)
            check("heading synthesised without the word budget", "## 1.1 Opening" in out
                  and "(~100 w)" not in out)
        finally:
            cp.folder, cp.state = real_folder, real_state
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    if FAILED:
        print(f"{len(FAILED)} check(s) FAILED: " + ", ".join(FAILED))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
