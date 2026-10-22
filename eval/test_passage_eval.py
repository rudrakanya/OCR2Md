#!/usr/bin/env python3
"""Offline tests for eval/passage_metrics.py and eval/benchmark_passages_v1.yaml
(Phase 10). No OpenAI call, no model download, no ChromaDB read or write.

    python eval/test_passage_eval.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "Udaipur Books Markdown files"
sys.path.insert(0, str(ROOT))

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

from eval.passage_metrics import (  # noqa: E402
    build_evidence_groups, evidence_recall_at_k, first_evidence_rank,
    group_found_at_rank, passage_match, reciprocal_rank,
)

FAILED: list[str] = []


def check(name, cond, detail=""):
    print(f"  {'ok  ' if cond else 'FAIL'}  {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILED.append(name)


def passage(excerpt, **dup):
    d = {"file": "a.md", "heading": "H", "excerpt": excerpt}
    if dup:
        d["duplicate_ocr_of"] = [dup]
    return d


# ---------------------------------------------------------------------------
def test_basic_match():
    check("exact substring matches", passage_match("some text here and more", "text here"))
    check("whitespace differences are normalized",
          passage_match("some   text\nhere   ", "text here"))
    check("non-matching text does not match", not passage_match("totally different", "text here"))
    check("empty excerpt never matches", not passage_match("anything at all", ""))


def test_missing_evidence():
    # The expected passage simply never appears in any retrieved hit.
    spec = {"supporting_passages": [passage("the unique phrase nobody returned")]}
    groups = build_evidence_groups(spec)
    hits = ["irrelevant chunk one", "irrelevant chunk two", "irrelevant chunk three"]
    check("group_found_at_rank returns None when the excerpt is absent from all hits",
          group_found_at_rank(hits, groups[0]) is None)
    check("evidence_recall_at_k is 0.0, not None, when evidence exists but was not found",
          evidence_recall_at_k(hits, groups, k=3) == 0.0)
    check("first_evidence_rank is None when nothing was found",
          first_evidence_rank(hits, groups) is None)
    check("reciprocal_rank(None) is 0.0", reciprocal_rank(None) == 0.0)


def test_overlapping_chunks_duplicate_ocr():
    # Two chunks both carry (OCR-variant) copies of the same underlying
    # sentence -- they must count as ONE group found, not two.
    spec = {"supporting_passages": [
        {"file": "a.md", "heading": "H", "excerpt": "the parallelism of pinda and brahmanda",
         "duplicate_ocr_of": [{"file": "b.md", "heading": "H2",
                               "excerpt": "the parallelizm of pindaa and brahmaanda"}]}
    ]}
    groups = build_evidence_groups(spec)
    check("one supporting_passages entry with a duplicate_ocr_of forms exactly one group",
          len(groups) == 1 and len(groups[0]) == 2, str(groups))
    hits = ["chunk containing the parallelism of pinda and brahmanda, more text",
            "a second chunk, from the OTHER OCR pass, containing the parallelizm of pindaa and brahmaanda too"]
    recall = evidence_recall_at_k(hits, groups, k=2)
    check("recall is 1.0 (one group found), not inflated by matching twice", recall == 1.0, str(recall))
    rank = group_found_at_rank(hits, groups[0])
    check("the group is found at rank 1 (first matching hit, either OCR copy)", rank == 1, str(rank))


def test_multiple_required_passages_independent():
    # Two genuinely independent sources required (PL-12-style): both must be
    # found for full coverage; finding only one gives partial credit.
    spec = {"supporting_passages": [
        passage("sandstone used in the temple", file="x.md"),
        passage("geological definition of sandstone", file="y.md"),
    ]}
    groups = build_evidence_groups(spec)
    check("two independent passages form two separate groups", len(groups) == 2)
    hits_both = ["mentions sandstone used in the temple here", "mentions geological definition of sandstone here"]
    hits_one = ["mentions sandstone used in the temple here", "unrelated content"]
    check("both found -> recall 1.0", evidence_recall_at_k(hits_both, groups, k=2) == 1.0)
    check("only one found -> recall 0.5, not 1.0 and not 0.0",
          evidence_recall_at_k(hits_one, groups, k=2) == 0.5)


def test_uncertain_judgment_not_silently_certain():
    # A query marked review_marker: uncertain should still be computable
    # (metrics don't need to special-case it), but callers must be able to
    # identify and exclude it -- this test documents that the metric
    # functions carry no built-in opinion about review_marker; the caller
    # (not passage_metrics.py) is responsible for filtering by it, exactly
    # as src/evaluate.py's partition_queries/aggregate do for book-level.
    spec = {"review_marker": "uncertain",
            "supporting_passages": [passage("some uncertain fact")]}
    groups = build_evidence_groups(spec)
    hits = ["chunk with some uncertain fact in it"]
    check("metrics still compute normally for an uncertain-marked query",
          evidence_recall_at_k(hits, groups, k=1) == 1.0)
    check("review_marker is not read by passage_metrics.py at all -- caller's job",
          "review_marker" not in {"supporting_passages", "duplicate_ocr_of"})


def test_empty_eligible_subset_no_fabrication():
    # A confirmed-unanswerable query: zero evidence groups. Must be None,
    # never a fabricated 0.0 that looks like "evidence not found".
    spec = {"answerable": False, "supporting_passages": []}
    groups = build_evidence_groups(spec)
    check("zero supporting_passages -> zero groups", groups == [])
    check("evidence_recall_at_k(..., []) is None, not 0.0",
          evidence_recall_at_k(["anything"], groups, k=5) is None)
    check("first_evidence_rank(..., []) is None",
          first_evidence_rank(["anything"], groups) is None)
    # Also: an empty hit list against real groups must not crash.
    real_groups = build_evidence_groups({"supporting_passages": [passage("x")]})
    check("empty hit list does not crash and correctly reports 'not found'",
          evidence_recall_at_k([], real_groups, k=5) == 0.0)


def test_rank_beyond_k_not_counted():
    spec = {"supporting_passages": [passage("findable fact")]}
    groups = build_evidence_groups(spec)
    hits = ["irrelevant"] * 5 + ["this one has the findable fact in it"]
    check("found at rank 6 overall", group_found_at_rank(hits, groups[0]) == 6)
    check("evidence_recall_at_k(..., k=3) does not count a hit beyond the cutoff",
          evidence_recall_at_k(hits, groups, k=3) == 0.0)
    check("evidence_recall_at_k(..., k=10) does count it once within window",
          evidence_recall_at_k(hits, groups, k=10) == 1.0)


# ---------------------------------------------------------------------------
def _check_benchmark_excerpts(bench_path: Path):
    """Shared logic: every excerpt in a passage benchmark file must be a
    real, verbatim (whitespace-normalized) substring of its claimed source
    file. This is the single most important check for a passage-level
    benchmark -- it catches a fabricated or mistyped passage, not just a
    bad filename."""
    import yaml
    bench = yaml.safe_load(bench_path.read_text(encoding="utf-8"))
    corpus_files = {p.name for p in CORPUS_DIR.glob("*.md")}
    file_cache: dict[str, str] = {}

    def text_of(fname: str) -> str | None:
        if fname not in file_cache:
            fp = CORPUS_DIR / fname
            file_cache[fname] = fp.read_text(encoding="utf-8", errors="replace") if fp.is_file() else None
        return file_cache[fname]

    checked, bad_files, bad_excerpts = 0, [], []
    ids = [q["id"] for q in bench["queries"]]
    for spec in bench["queries"]:
        all_passages = list(spec.get("supporting_passages") or [])
        for p in list(all_passages):
            all_passages.extend(p.get("duplicate_ocr_of") or [])
        for p in all_passages:
            checked += 1
            fname = p["file"]
            if fname not in corpus_files:
                bad_files.append((spec["id"], fname))
                continue
            text = text_of(fname)
            if not passage_match(text, p["excerpt"]):
                bad_excerpts.append((spec["id"], fname, p["excerpt"][:60]))

    check(f"{bench_path.name}: all ids unique", len(ids) == len(set(ids)), str(ids))
    check(f"{bench_path.name}: checked {checked} passage excerpts across {len(bench['queries'])} queries",
          checked > 0)
    check(f"{bench_path.name}: every referenced filename exists in the corpus", not bad_files, str(bad_files))
    check(f"{bench_path.name}: every excerpt is a verbatim (whitespace-normalized) substring of its file",
          not bad_excerpts, str(bad_excerpts))


def test_benchmark_excerpts_exist_verbatim_in_corpus():
    _check_benchmark_excerpts(ROOT / "eval" / "benchmark_passages_v1.yaml")


def test_benchmark_v2_excerpts_exist_verbatim_in_corpus():
    _check_benchmark_excerpts(ROOT / "eval" / "benchmark_passages_v2.yaml")


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for t in tests:
        print(f"\n{t.__name__}")
        t()
    print("\n" + ("ALL CHECKS PASSED" if not FAILED else f"{len(FAILED)} FAILED: {FAILED}"))
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
