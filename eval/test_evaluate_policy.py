#!/usr/bin/env python3
"""Offline regression tests for the Phase 9 policy-aware aggregation added to
src/evaluate.py (partition_queries, aggregate). Synthetic fixtures only --
no OpenAI call, no model download, no ChromaDB read or write.

    python eval/test_evaluate_policy.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.evaluate import aggregate, partition_queries  # noqa: E402

FAILED: list[str] = []


def check(name, cond, detail=""):
    print(f"  {'ok  ' if cond else 'FAIL'}  {name}" + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        FAILED.append(name)


def gold(*specs):
    return {"queries": list(specs)}


def row(qid, **kw):
    """A synthetic per_query row, same shape evaluate_queries() produces."""
    base = {"id": qid, "query": f"query {qid}", "n_hits": 3,
            "P@3": 0.0, "P@5": 0.0, "P@10": 0.0,
            "R@3": 0.0, "R@5": 0.0, "R@10": 0.0,
            "RR": 0.0, "nDCG@10": 0.0}
    base.update(kw)
    return base


K = [3, 5, 10]
NDCG_K = 10


def test_1_answerable_contributes():
    g = gold({"id": "Q1", "query": "x", "answerable": True, "relevant_books": ["a.md"]})
    rows = [row("Q1", **{"P@3": 1.0, "RR": 1.0, "nDCG@10": 1.0})]
    part = partition_queries(g)
    check("Q1 is eligible", part["eligible"] == ["Q1"], str(part))
    summ = aggregate(rows, part["eligible"], K, NDCG_K)
    check("eligible aggregate reflects the answerable query's own score",
          summ is not None and summ["P@3"] == 1.0 and summ["MRR"] == 1.0, str(summ))


def test_2_unanswerable_does_not_pull_down_mean():
    g = gold(
        {"id": "Q1", "query": "x", "answerable": True, "relevant_books": ["a.md"]},
        {"id": "Q2", "query": "y", "answerable": False, "relevant_books": []},
    )
    # Q2's raw row is the structural zero relevance() forces for an empty
    # relevant_books -- exactly what the real evaluator would produce.
    rows = [row("Q1", **{"P@3": 1.0, "RR": 1.0, "nDCG@10": 1.0}),
            row("Q2", **{"P@3": 0.0, "RR": 0.0, "nDCG@10": 0.0})]
    part = partition_queries(g)
    check("Q2 excluded, not eligible", part["eligible"] == ["Q1"] and part["excluded_unanswerable"] == ["Q2"])
    summ = aggregate(rows, part["eligible"], K, NDCG_K)
    check("eligible-only mean is Q1's score, not pulled to 0.5 by Q2's zero",
          summ is not None and summ["P@3"] == 1.0, str(summ))


def test_3_exclude_from_aggregate_respected():
    g = gold(
        {"id": "Q1", "query": "x", "answerable": True, "relevant_books": ["a.md"]},
        # answerable left absent (defaults True) but explicitly excluded anyway
        {"id": "Q2", "query": "y", "exclude_from_aggregate": True, "relevant_books": []},
    )
    rows = [row("Q1", **{"P@3": 1.0, "RR": 1.0}), row("Q2", **{"P@3": 0.0, "RR": 0.0})]
    part = partition_queries(g)
    check("Q2 excluded via exclude_from_aggregate alone (answerable absent/default True)",
          "Q2" in part["excluded_unanswerable"] and "Q2" not in part["eligible"], str(part))
    summ = aggregate(rows, part["eligible"], K, NDCG_K)
    check("Q2's zero does not enter the eligible mean",
          summ is not None and summ["P@3"] == 1.0, str(summ))


def test_4_answerable_with_no_labels_is_unresolved_not_zero():
    g = gold({"id": "Q1", "query": "x", "answerable": True, "relevant_books": []})
    part = partition_queries(g)
    check("Q1 goes to invalid_unresolved, not eligible and not excluded_unanswerable",
          part["invalid_unresolved"] == ["Q1"] and part["eligible"] == []
          and part["excluded_unanswerable"] == [], str(part))


def test_5_uncertain_sensitivity_subset():
    g = gold(
        {"id": "Q1", "query": "x", "answerable": True, "relevant_books": ["a.md"]},
        {"id": "Q2", "query": "y", "answerable": True, "relevant_books": ["b.md"],
         "review_marker": "uncertain"},
    )
    rows = [row("Q1", **{"P@3": 1.0}), row("Q2", **{"P@3": 0.0})]
    part = partition_queries(g)
    eligible = set(part["eligible"])
    uncertain_ids = {q["id"] for q in g["queries"] if q.get("review_marker") == "uncertain"}
    sensitivity_ids = eligible - uncertain_ids
    check("both Q1 and Q2 are eligible (uncertain != excluded)",
          eligible == {"Q1", "Q2"}, str(eligible))
    check("sensitivity subset drops only the uncertain query",
          sensitivity_ids == {"Q1"}, str(sensitivity_ids))
    main_summ = aggregate(rows, eligible, K, NDCG_K)
    sens_summ = aggregate(rows, sensitivity_ids, K, NDCG_K)
    check("main eligible mean is pulled down by the uncertain query's low score",
          main_summ["P@3"] == 0.5, str(main_summ))
    check("sensitivity (uncertain excluded) mean reflects only Q1",
          sens_summ["P@3"] == 1.0, str(sens_summ))


def test_6_dense_and_hybrid_share_eligible_ids():
    g = gold(
        {"id": "Q1", "query": "x", "answerable": True, "relevant_books": ["a.md"]},
        {"id": "Q2", "query": "y", "answerable": False, "relevant_books": []},
    )
    part = partition_queries(g)
    dense_rows = [row("Q1", **{"P@3": 0.6}), row("Q2", **{"P@3": 0.0})]
    hybrid_rows = [row("Q1", **{"P@3": 0.9}), row("Q2", **{"P@3": 0.0})]
    dense_summ = aggregate(dense_rows, part["eligible"], K, NDCG_K)
    hybrid_summ = aggregate(hybrid_rows, part["eligible"], K, NDCG_K)
    check("both runs aggregate over exactly {Q1} -- Q2 excluded from both identically",
          dense_summ["n_queries"] == 1 and hybrid_summ["n_queries"] == 1)
    check("dense and hybrid reflect only their own retrieval numbers, same eligible set",
          dense_summ["P@3"] == 0.6 and hybrid_summ["P@3"] == 0.9,
          f"dense={dense_summ}, hybrid={hybrid_summ}")


def test_7_empty_eligible_set_handled_explicitly():
    g = gold({"id": "Q1", "query": "x", "answerable": False, "relevant_books": []})
    rows = [row("Q1", **{"P@3": 0.0})]
    part = partition_queries(g)
    check("eligible set is empty", part["eligible"] == [])
    summ = aggregate(rows, part["eligible"], K, NDCG_K)
    check("aggregate() returns None, not a fabricated 0.0, for an empty eligible set",
          summ is None, str(summ))
    # also exercise aggregate() directly with an id set matching nothing in per_query
    summ2 = aggregate(rows, {"does-not-exist"}, K, NDCG_K)
    check("aggregate() returns None when no row matches the given ids at all",
          summ2 is None, str(summ2))


def test_8_evaluate_queries_unmodified_shape():
    # evaluate_queries()/relevance() are not imported or called here on
    # purpose -- Phase 9 made zero edits to either function. This test
    # instead confirms the NEW functions make no assumption that breaks on a
    # gold.yaml-shaped spec with none of the new fields at all.
    g = gold({"id": "G1", "query": "old-style", "relevant_books": ["a.md"]})
    part = partition_queries(g)
    check("a gold.yaml-style spec (no answerable/exclude_from_aggregate field) "
          "defaults to eligible, unchanged from pre-Phase-9 behaviour",
          part["eligible"] == ["G1"] and part["excluded_unanswerable"] == []
          and part["invalid_unresolved"] == [], str(part))


def test_9_legacy_warning_condition():
    # Phase 10: main() warns after a legacy (non --policy-aware) table only
    # when partition_queries finds something excluded/unresolved. This test
    # exercises exactly the boolean condition main() uses, without needing
    # to capture stdout or run a real evaluation.
    gold_legacy = gold({"id": "G1", "query": "x", "relevant_books": ["a.md"]})
    part = partition_queries(gold_legacy)
    excluded = part["excluded_unanswerable"] + part["invalid_unresolved"]
    check("gold.yaml-shaped input never triggers the legacy warning",
          not excluded, str(excluded))

    gold_v2 = gold(
        {"id": "Q1", "query": "x", "answerable": True, "relevant_books": ["a.md"]},
        {"id": "Q2", "query": "y", "answerable": False, "relevant_books": []},
    )
    part2 = partition_queries(gold_v2)
    excluded2 = part2["excluded_unanswerable"] + part2["invalid_unresolved"]
    check("a benchmark_v2-shaped input with an unanswerable query triggers the warning",
          excluded2 == ["Q2"], str(excluded2))


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for t in tests:
        print(f"\n{t.__name__}")
        t()
    print("\n" + ("ALL CHECKS PASSED" if not FAILED else f"{len(FAILED)} FAILED: {FAILED}"))
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
