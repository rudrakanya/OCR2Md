#!/usr/bin/env python3
"""Phase 11 Step 3: offline, read-only audit of heading-only / empty-body
sections across the corpus.

Reuses the ACTUAL production chunking functions from src/chunker.py
(split_sections, _atomic_blocks, has_content, HEADING_RE) rather than
reimplementing an approximation -- the audit result is exactly what the
real ingest path would do, because it IS the real ingest path's own code,
called read-only, with no embedding and no collection write.

    python eval/audit_heading_sections.py
    python eval/audit_heading_sections.py --compare-collection   # also
        cross-checks each dropped heading against the live collection's
        stored metadata (read-only .get(), no embedding, no write)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

from src import settings as st  # noqa: E402
from src.chunker import (  # noqa: E402
    HEADING_RE, LETTER_RE, _atomic_blocks, _compile_junk, has_content, split_sections,
)
from src import textutil  # noqa: E402

DATE_RE = re.compile(r"\b(1[0-9]{3}|20[0-9]{2})\b")  # a bare 4-digit year


def raw_headings(text: str, split_levels: int, junk) -> list[tuple[int, int, str]]:
    """(line_no, level, title) for every heading src/chunker.py's own
    HEADING_RE would recognise at or under split_levels, skipping junk
    headings exactly as split_sections() does -- so this list is directly
    comparable to what split_sections() actually consumes."""
    out = []
    in_fence = False
    for i, line in enumerate(text.splitlines(), 1):
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        level, title = len(m.group(1)), m.group(2).strip()
        title = re.sub(r"<!--.*?-->", "", title).strip()
        if not title or any(p.search(title) for p in junk) or level > split_levels:
            continue
        out.append((i, level, title))
    return out


def classify(dropped_heading: str, body_lines: list[str]) -> str:
    """Classify a heading that split_sections() dropped (empty section)."""
    joined = "\n".join(body_lines)
    if not joined.strip():
        return "intentionally_empty_or_divider"
    if not LETTER_RE.search(joined):
        return "intentionally_empty_or_divider"  # markdown furniture / page markers only
    # Has some letters but was still dropped -- should be structurally
    # impossible given split_sections()'s own "any(l.strip())" check; flag
    # for manual review if it ever occurs.
    return "uncertain_requires_manual_review"


def audit_file(path: Path, cfg) -> dict:
    ck = cfg["chunking"]
    split_levels = len(ck.get("split_headers", ["#", "##", "###"]))
    junk = _compile_junk(ck.get("junk_heading_patterns", []))
    text = textutil.nfc(path.read_text(encoding="utf-8"))

    sections = split_sections(text, split_levels, junk)
    kept_headings = {tuple(s.heading_path) for s in sections if s.heading_path}
    # Also: for a KEPT section, did _atomic_blocks + has_content produce
    # zero blocks anyway (survived split_sections but lost at the next
    # filtering stage)?
    lost_after_split = []
    for s in sections:
        blocks = _atomic_blocks(s.lines, bool(ck.get("keep_tables_whole", True)),
                                bool(ck.get("attach_footnotes", True)))
        if s.heading_path and not blocks:
            lost_after_split.append(s.heading_path[-1] if s.heading_path else "(no heading)")

    raw = raw_headings(text, split_levels, junk)
    # Build stacked heading PATHS the same way split_sections() does, so we
    # can tell which raw heading occurrences correspond to which
    # (possibly-dropped) section.
    stack: list[str] = []
    seen_paths: list[tuple[tuple[int, int, str], tuple[str, ...]]] = []
    for (lineno, level, title) in raw:
        stack = stack[: level - 1]
        while len(stack) < level - 1:
            stack.append("")
        stack.append(title)
        seen_paths.append(((lineno, level, title), tuple(h for h in stack if h)))

    # A heading name survives, even if its OWN section was dropped, if some
    # KEPT section's heading_path contains it as an ancestor component (this
    # happens when the next heading is a deeper child level, not a sibling
    # that replaces it in the stack). Build that lookup once.
    names_in_any_kept_path: set[str] = {h for path in kept_headings for h in path}

    dropped = []
    for (lineno, level, title), hpath in seen_paths:
        if hpath and hpath not in kept_headings:
            # Recover the body lines actually assigned to this heading, to
            # classify it (not just report it as dropped).
            # Re-run a lightweight pass: find this heading's line and the
            # next heading's line at <= split_levels, take lines between.
            body = _body_between(text, lineno, split_levels, junk)
            cls = classify(title, body)
            has_meaningful_marker = bool(DATE_RE.search(title)) or bool(re.search(r"[A-Z][a-z]+\s+[A-Z][a-z]+", title))
            rescued = title in names_in_any_kept_path
            dropped.append({
                "heading": title, "level": level, "line": lineno,
                "path": " > ".join(hpath), "classification": cls,
                "heading_itself_looks_meaningful": has_meaningful_marker,
                "name_rescued_as_ancestor_elsewhere": rescued,
                "body_preview": "\n".join(body)[:120],
            })

    return {
        "file": path.name,
        "raw_heading_count": len(raw),
        "kept_section_count": len(sections),
        "dropped_heading_count": len(dropped),
        "lost_after_split_count": len(lost_after_split),
        "lost_after_split": lost_after_split,
        "dropped": dropped,
    }


def _body_between(text: str, heading_line: int, split_levels: int, junk) -> list[str]:
    lines = text.splitlines()
    start = heading_line  # 1-based; heading itself is at lines[heading_line-1]
    body: list[str] = []
    in_fence = False
    for line in lines[start:]:
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            body.append(line)
            continue
        if not in_fence:
            m = HEADING_RE.match(line)
            if m:
                lvl, title = len(m.group(1)), m.group(2).strip()
                title = re.sub(r"<!--.*?-->", "", title).strip()
                if title and not any(p.search(title) for p in junk) and lvl <= split_levels:
                    break  # next real section heading -- stop here
        body.append(line)
    return body


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit heading-only/empty-body sections (read-only)")
    ap.add_argument("--compare-collection", action="store_true",
                    help="also cross-check dropped headings against the live collection's "
                         "stored heading_path/text metadata (read-only .get(), no embedding)")
    args = ap.parse_args()

    cfg = st.load()
    corpus_dir = Path(cfg.get_path("project.corpus_dir"))
    files = sorted(corpus_dir.glob("*.md"))
    print(f"auditing {len(files)} files in {corpus_dir}\n")

    all_results = []
    total_dropped = 0
    total_lost_after_split = 0
    by_class: dict[str, int] = {}

    for f in files:
        r = audit_file(f, cfg)
        all_results.append(r)
        total_dropped += r["dropped_heading_count"]
        total_lost_after_split += r["lost_after_split_count"]
        for d in r["dropped"]:
            by_class[d["classification"]] = by_class.get(d["classification"], 0) + 1
        if r["dropped_heading_count"] or r["lost_after_split_count"]:
            print(f"  {f.name}: {r['raw_heading_count']} raw headings, "
                  f"{r['kept_section_count']} kept sections, "
                  f"{r['dropped_heading_count']} dropped (empty), "
                  f"{r['lost_after_split_count']} lost-after-split")

    print(f"\nTOTAL: {total_dropped} headings dropped as empty sections across the corpus")
    print(f"TOTAL: {total_lost_after_split} sections survived split_sections() but produced "
          f"zero retrievable blocks (has_content() filtered everything)")
    print(f"\nby classification: {by_class}")

    meaningful_flagged = [
        (r["file"], d) for r in all_results for d in r["dropped"]
        if d["heading_itself_looks_meaningful"]
    ]
    truly_lost = [(f, d) for f, d in meaningful_flagged if not d["name_rescued_as_ancestor_elsewhere"]]
    rescued = [(f, d) for f, d in meaningful_flagged if d["name_rescued_as_ancestor_elsewhere"]]
    if meaningful_flagged:
        print(f"\n{len(meaningful_flagged)} dropped heading(s) whose TEXT contains a "
              f"year or a capitalized-name-like pattern:")
        print(f"\n  {len(truly_lost)} with NO rescue -- the name appears nowhere else in this "
              f"file's surviving heading_path metadata (next heading was a sibling/same-level "
              f"heading that replaced it in the stack, not a deeper child):")
        for fname, d in truly_lost[:30]:
            print(f"    {fname}: {d['heading']!r}  (line {d['line']})")
        print(f"\n  {len(rescued)} RESCUED -- name survives as an ancestor component of a "
              f"kept section's heading_path elsewhere (next heading was a deeper child level), "
              f"so it IS present in metadata, just not as its own standalone section or as "
              f"embedded document body text:")
        for fname, d in rescued[:30]:
            print(f"    {fname}: {d['heading']!r}  (line {d['line']})")

    if args.compare_collection:
        _compare_collection(all_results, cfg)

    return 0


def _compare_collection(all_results, cfg):
    import chromadb
    from chromadb.config import Settings as ChromaSettings

    chroma_path = st.resolve(cfg, "storage.chroma_path")
    client = chromadb.PersistentClient(path=str(chroma_path),
                                       settings=ChromaSettings(anonymized_telemetry=False))
    collection = client.get_collection(cfg.get_path("storage.collection"))
    print(f"\ncross-checking against live collection {collection.name!r} "
          f"({collection.count():,} chunks) -- read-only .get(), no embedding, no write")

    checked, found_in_metadata = 0, 0
    for r in all_results:
        got = collection.get(where={"source_path": r["file"]}, include=["metadatas", "documents"])
        headings_in_store = {m.get("heading_path", "") for m in got["metadatas"]}
        texts_in_store = got["documents"]
        for d in r["dropped"]:
            checked += 1
            in_heading_meta = any(d["heading"] in h for h in headings_in_store)
            in_body_text = any(d["heading"] in t for t in texts_in_store)
            if in_heading_meta or in_body_text:
                found_in_metadata += 1
                print(f"  UNEXPECTED: {r['file']} dropped heading {d['heading']!r} "
                      f"actually found in store (heading_meta={in_heading_meta}, "
                      f"body_text={in_body_text}) -- audit/runtime mismatch, investigate")
    print(f"\nchecked {checked} dropped headings against the live store: "
          f"{found_in_metadata} unexpectedly present (should be 0 if the audit and the "
          f"actual ingest run used the same chunking config)")


if __name__ == "__main__":
    sys.exit(main())
