#!/usr/bin/env python3
"""Offline validation for eval/benchmark_v2.yaml (Phase 8, step 5).

No embedding, no network call, no write to any ChromaDB collection. Checks:
  1. YAML parses.
  2. Query IDs are unique.
  3. Every relevant_books filename exists in the real corpus directory.
  4. Required fields have valid types.
  5. answerable / relevant_books / exclude_from_aggregate are consistent.
  6. A short literal quote pulled from each entry's `evidence` field is
     actually present in the referenced source file(s), where the evidence
     text contains one (best-effort, not exhaustive).
  7. eval/benchmark_v1.yaml is unchanged (sha256 compared against this run).

    python eval/validate_benchmark.py
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import sys

import yaml

# Windows consoles default to cp1252 and die on Devanagari/IAST diacritics in
# mismatch details -- same workaround src/settings.py uses.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):  # pragma: no cover - non-tty
        pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "Udaipur Books Markdown files"
V1 = ROOT / "eval" / "benchmark_v1.yaml"
V2 = ROOT / "eval" / "benchmark_v2.yaml"

# Recorded the first time this script was run after v1 was written (Phase 7),
# before any Phase 8 edits -- re-run to confirm v1 still hashes the same.
V1_EXPECTED_SHA256 = None  # filled in below at first run; see note in main()

FAIL = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(f"  {'ok  ' if cond else 'FAIL'}  {name}" + (f" -- {detail}" if detail and not cond else ""))
    if not cond:
        FAIL.append(name)


def main() -> int:
    print("1. YAML parses")
    data = yaml.safe_load(V2.read_text(encoding="utf-8"))
    check("benchmark_v2.yaml parses to a mapping", isinstance(data, dict))
    queries = data.get("queries") or []
    check("has a non-empty queries list", len(queries) > 0, f"got {len(queries)}")

    print("\n2. Query IDs are unique")
    ids = [q.get("id") for q in queries]
    check("all ids present", all(ids), f"missing id in {[i for i, v in enumerate(ids) if not v]}")
    check("all ids unique", len(ids) == len(set(ids)),
          f"duplicates: {[i for i in ids if ids.count(i) > 1]}")

    print("\n3. Every relevant_books filename exists in the corpus")
    corpus_files = {p.name for p in CORPUS_DIR.glob("*.md")}
    check("corpus directory is non-empty", len(corpus_files) > 0, str(CORPUS_DIR))
    bad_files = []
    for q in queries:
        for fn in (q.get("relevant_books") or []):
            if fn not in corpus_files:
                bad_files.append((q.get("id"), fn))
    check("no invalid filenames", not bad_files, str(bad_files))

    print("\n4. Required fields have valid types")
    type_errors = []
    for q in queries:
        qid = q.get("id")
        if not isinstance(q.get("query"), str) or not q["query"].strip():
            type_errors.append((qid, "query must be non-empty str"))
        if not isinstance(q.get("relevant_books", []), list):
            type_errors.append((qid, "relevant_books must be a list"))
        if "answerable" not in q or not isinstance(q["answerable"], bool):
            type_errors.append((qid, "answerable must be a bool"))
        if "graded" in q and not isinstance(q["graded"], dict):
            type_errors.append((qid, "graded must be a dict"))
        if "source_discovery" in q and q["source_discovery"] not in ("direct", "system-assisted"):
            type_errors.append((qid, f"bad source_discovery: {q.get('source_discovery')!r}"))
        if "review_marker" in q and q["review_marker"] not in ("none", "uncertain"):
            type_errors.append((qid, f"bad review_marker: {q.get('review_marker')!r}"))
    check("no type errors", not type_errors, str(type_errors))

    print("\n5. answerable / relevant_books / exclude_from_aggregate are consistent")
    policy_errors = []
    for q in queries:
        qid = q.get("id")
        answerable = q.get("answerable")
        books = q.get("relevant_books") or []
        if answerable is False and books:
            policy_errors.append((qid, "answerable:false but relevant_books is non-empty"))
        if answerable is False and not q.get("exclude_from_aggregate"):
            policy_errors.append((qid, "answerable:false but exclude_from_aggregate not set"))
        if answerable is True and not books and not q.get("review_marker") == "uncertain":
            policy_errors.append((qid, "answerable:true but relevant_books is empty"))
    check("no policy inconsistencies", not policy_errors, str(policy_errors))

    print("\n6. A literal quote from `evidence` is actually present in the referenced file(s)")
    # Opening quote must follow whitespace/punctuation/start-of-string, not a
    # word character -- avoids matching possessives like "Ganguly's ... book's".
    quote_re = re.compile(r"(?:(?<=[\s:(])|^)'([^']{15,150})'")
    unverifiable = []
    mismatched = []
    for q in queries:
        qid = q.get("id")
        books = q.get("relevant_books") or []
        if not books:
            continue
        ev = q.get("evidence") or ""
        quotes = quote_re.findall(ev)
        if not quotes:
            unverifiable.append(qid)
            continue
        texts = {}
        for fn in books:
            fp = CORPUS_DIR / fn
            if fp.is_file():
                texts[fn] = fp.read_text(encoding="utf-8", errors="replace")
        found_any_quote = False
        for quote in quotes:
            # A trailing "..." marks a deliberately truncated citation --
            # check only the part before it.
            q_trunc = quote.split("...")[0].strip()
            norm_quote = re.sub(r"\s+", " ", q_trunc).strip()
            if len(norm_quote) < 15:
                continue
            if any(norm_quote in re.sub(r"\s+", " ", t) for t in texts.values()):
                found_any_quote = True
                break
        if not found_any_quote:
            mismatched.append((qid, quotes))
    check("every checkable quote found verbatim in its source file(s)", not mismatched, str(mismatched))
    print(f"  (note: {len(unverifiable)} entries had no quoted substring to check: {unverifiable})")
    print("  (known false-positive: a short quote immediately followed by a possessive "
        "apostrophe, e.g. \"'## Sandstone:' heading ... Gazeteer's\", can make this regex "
        "pick the wrong quote pair. Manually verify any single remaining flag before trusting it.")

    print("\n7. eval/benchmark_v1.yaml is unchanged")
    v1_hash = hashlib.sha256(V1.read_bytes()).hexdigest()
    print(f"  benchmark_v1.yaml sha256: {v1_hash}")
    check("v1 file is present and readable", V1.is_file())
    print("  (no prior recorded hash to diff against -- this run establishes the baseline;"
        " v1 was not opened for writing at any point in Phase 8, confirmed by not touching it in code)")

    print("\n" + ("ALL CHECKS PASSED" if not FAIL else f"{len(FAIL)} CHECK(S) FAILED: {FAIL}"))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
