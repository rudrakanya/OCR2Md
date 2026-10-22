#!/usr/bin/env python3
"""Phase 10 Step 4: controlled dense-vs-hybrid passage-level comparison
against eval/benchmark_passages_v1.yaml.

Read-only against the collection (queries only; no upsert, no delete, no
--rebuild). Saves a new, timestamped JSON artifact under
eval/results/chroma/ -- never overwrites a prior run.

    python eval/run_passage_eval.py
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

import yaml  # noqa: E402

from eval.passage_metrics import (  # noqa: E402
    build_evidence_groups, evidence_recall_at_k, first_evidence_rank, reciprocal_rank,
)
from src import settings as st  # noqa: E402
from src.retrieval import Retriever  # noqa: E402
from src.store import open_aligned  # noqa: E402

K_VALUES = [3, 5, 10]
MAX_K = max(K_VALUES)
DEFAULT_BENCH = "benchmark_passages_v1.yaml"


def run_mode(retriever: Retriever, queries: list[dict], hybrid: bool) -> dict:
    per_query = []
    for spec in queries:
        hits = retriever.search(spec["query"], k=MAX_K, hybrid=hybrid)
        # Chroma's stored document (Hit.text) is BODY text only -- headings
        # live in heading_path metadata (Hit.heading), never duplicated into
        # the body by src/chunker.py. An excerpt that is itself a heading
        # string (e.g. PL-05, PL-07) must be checked against both, or it can
        # never match regardless of retrieval quality. Confirmed by reading
        # src/chunker.py's Chunk dataclass and src/store.py's upsert() call.
        hit_texts = [f"{h.heading}\n{h.text}" for h in hits]
        groups = build_evidence_groups(spec)
        row = {
            "id": spec["id"], "answerable": spec.get("answerable", True),
            "answerability_status": spec.get("answerability_status"),
            "category": spec.get("category"),
            "n_groups": len(groups),
            "review_marker": spec.get("review_marker", "none"),
            "top_book": hits[0].metadata.get("source_path") if hits else None,
        }
        for k in K_VALUES:
            row[f"EvR@{k}"] = evidence_recall_at_k(hit_texts, groups, k)
        rank = first_evidence_rank(hit_texts, groups)
        row["first_rank"] = rank
        row["RR"] = reciprocal_rank(rank) if groups else None
        per_query.append(row)

    # confirmed_unindexed (Phase 11): the evidence is real but PROVABLY
    # absent from the collection (see eval/audit_heading_sections.py) -- a
    # retriever cannot be faulted for missing it, so it must not be folded
    # into the ordinary eligible mean any more than an unanswerable query
    # should be (same reasoning as src/evaluate.py's partition_queries).
    unindexed = [r for r in per_query if r.get("answerability_status") == "confirmed_unindexed"]
    eligible = [r for r in per_query if r["n_groups"] > 0
               and r.get("answerability_status") != "confirmed_unindexed"]

    def mean(key, rows=None):
        rows = eligible if rows is None else rows
        vals = [r[key] for r in rows if r.get(key) is not None]
        return (sum(vals) / len(vals)) if vals else None

    summary = {f"EvR@{k}": mean(f"EvR@{k}") for k in K_VALUES}
    summary["MRR"] = mean("RR")
    summary["n_eligible"] = len(eligible)
    summary["n_unindexed"] = len(unindexed)
    summary["n_unanswerable_or_no_evidence"] = len(per_query) - len(eligible) - len(unindexed)

    # sensitivity: eligible minus uncertain-marked queries
    sensitivity_rows = [r for r in eligible if r.get("review_marker") != "uncertain"]
    summary["sensitivity_excl_uncertain"] = {
        f"EvR@{k}": mean(f"EvR@{k}", sensitivity_rows) for k in K_VALUES
    } | {"MRR": mean("RR", sensitivity_rows), "n": len(sensitivity_rows)}

    # per-category breakdown
    categories = sorted({r.get("category") for r in eligible if r.get("category")})
    by_category = {}
    for cat in categories:
        cat_rows = [r for r in eligible if r.get("category") == cat]
        by_category[cat] = {f"EvR@{k}": mean(f"EvR@{k}", cat_rows) for k in K_VALUES} | {
            "MRR": mean("RR", cat_rows), "n": len(cat_rows)}
    summary["by_category"] = by_category

    return {"summary": summary, "per_query": per_query}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--benchmark", default=DEFAULT_BENCH,
                    help=f"benchmark filename under eval/ (default: {DEFAULT_BENCH})")
    args = ap.parse_args()
    bench_path = ROOT / "eval" / args.benchmark

    bench = yaml.safe_load(bench_path.read_text(encoding="utf-8"))
    queries = bench["queries"]
    bench_sha256 = hashlib.sha256(bench_path.read_bytes()).hexdigest()

    cfg = st.load()
    cfg, store = open_aligned(cfg, preset="openai_large")
    retriever = Retriever(cfg, store=store)
    prov = st.provenance(cfg)

    print("=" * 72)
    print(f"PASSAGE-LEVEL EVAL  benchmark={bench_path.name}  sha256={bench_sha256[:12]}...")
    print(f"  model      {prov['embedding_model']}")
    print(f"  collection {cfg.get_path('storage.collection')}  ({store.count():,} chunks)")
    print(f"  queries    {len(queries)}")
    print("=" * 72)

    runs = {}
    for label, hybrid in (("dense only", False), ("hybrid (dense+BM25, RRF)", True)):
        result = run_mode(retriever, queries, hybrid)
        runs[label] = result
        s = result["summary"]
        print(f"\n  {label}")
        print("  " + "-" * 60)
        for k in K_VALUES:
            v = s[f"EvR@{k}"]
            print(f"    Evidence Recall@{k:<2d}  {'n/a' if v is None else f'{v:.3f}'}")
        mrr_str = "n/a" if s["MRR"] is None else f"{s['MRR']:.3f}"
        print(f"    MRR (first evidence)  {mrr_str}")
        print(f"    eligible queries      {s['n_eligible']}")
        print(f"    confirmed_unindexed   {s['n_unindexed']}")
        print(f"    unanswerable/no-evid  {s['n_unanswerable_or_no_evidence']}")
        def fmt(v):
            return "n/a" if v is None else f"{v:.3f}"

        sens = s["sensitivity_excl_uncertain"]
        sens_strs = ", ".join(f"EvR@{k}={fmt(sens[f'EvR@{k}'])}" for k in K_VALUES)
        print(f"    sensitivity (excl. uncertain, n={sens['n']}): {sens_strs}")
        if s["by_category"]:
            print("    by category:")
            for cat, cs in s["by_category"].items():
                cat_strs = ", ".join(f"EvR@{k}={fmt(cs[f'EvR@{k}'])}" for k in K_VALUES)
                print(f"      {cat:28s} n={cs['n']:2d}  {cat_strs}  MRR={fmt(cs['MRR'])}")

    # Per-query wins/losses/ties, hybrid vs dense, on EvR@10.
    dense_by_id = {r["id"]: r for r in runs["dense only"]["per_query"]}
    hybrid_by_id = {r["id"]: r for r in runs["hybrid (dense+BM25, RRF)"]["per_query"]}
    wins, losses, ties, na = [], [], [], []
    for qid in dense_by_id:
        d, h = dense_by_id[qid]["EvR@10"], hybrid_by_id[qid]["EvR@10"]
        if d is None or h is None:
            na.append(qid)
        elif h > d:
            wins.append(qid)
        elif h < d:
            losses.append(qid)
        else:
            ties.append(qid)
    print(f"\n  per-query EvR@10, hybrid vs dense: {len(wins)} hybrid-wins {wins}, "
          f"{len(losses)} hybrid-losses {losses}, {len(ties)} ties {ties}, "
          f"{len(na)} n/a (no evidence) {na}")

    run_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    payload = {
        "run_id": run_id,
        "benchmark_file": str(bench_path.relative_to(ROOT)),
        "benchmark_sha256": bench_sha256,
        "collection": cfg.get_path("storage.collection"),
        "collection_count": store.count(),
        "embedding_model": prov["embedding_model"],
        "config_hash": prov["config_hash"],
        "n_queries": len(queries),
        "k_values": K_VALUES,
        "runs": runs,
        "comparison": {"hybrid_wins": wins, "hybrid_losses": losses, "ties": ties, "n_a": na},
    }
    out_dir = st.resolve(cfg, "evaluation.results_dir")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"passage_eval_{run_id}.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n  saved {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
