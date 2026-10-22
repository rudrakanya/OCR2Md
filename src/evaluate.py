"""Retrieval accuracy and precision harness (§10).

    python -m src.evaluate                       # full run on eval/gold.yaml
    python -m src.evaluate --no-hybrid           # dense only, for comparison
    python -m src.evaluate --ablate              # sweep chunk sizes x models

Every run writes {evaluation.results_dir}/eval_<timestamp>.json carrying the
config hash and library versions, so two runs are always comparable.

A caveat that belongs next to the numbers, not in a footnote: gold.yaml judges
at BOOK level. A chunk from the right book about the wrong subject scores as a
hit, so precision here is an upper bound. It is still the right tool for
answering "did this change help?", which is what you will actually use it for.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import statistics
import sys
from pathlib import Path

import yaml

from . import settings as st
from .retrieval import Retriever, ndcg
from .store import Store, open_aligned


def load_gold(cfg) -> dict:
    path = st.resolve(cfg, "evaluation.gold_path")
    if not path.is_file():
        raise FileNotFoundError(f"gold set not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not data.get("queries"):
        raise ValueError(f"{path} contains no queries")
    return data


def relevance(hit, spec: dict) -> float:
    """Graded relevance for one hit, 0..3."""
    chunk_ids = set(spec.get("relevant_chunks") or [])
    if chunk_ids:
        return 3.0 if hit.chunk_id in chunk_ids else 0.0
    src = hit.metadata.get("source_path", "")
    graded = spec.get("graded") or {}
    if src in graded:
        return float(graded[src])
    return 1.0 if src in set(spec.get("relevant_books") or []) else 0.0


def evaluate_queries(cfg, retriever: Retriever, gold: dict, *,
                     hybrid: bool | None, k_values: list[int], ndcg_k: int,
                     verbose: bool = True) -> dict:
    per_query = []
    max_k = max(max(k_values), ndcg_k)

    for spec in gold["queries"]:
        hits = retriever.search(spec["query"], k=max_k, hybrid=hybrid)
        rels = [relevance(h, spec) for h in hits]
        binary = [1 if r > 0 else 0 for r in rels]

        # Recall's denominator is the number of relevant items retrievable in
        # principle. With book-level labels we cannot know how many relevant
        # chunks exist, so we use "did we find each expected book?" — a
        # book-level recall, which is the honest quantity for this labelling.
        want_books = set(spec.get("relevant_books") or [])
        row: dict = {"id": spec["id"], "query": spec["query"],
                     "chapter": spec.get("chapter"), "n_hits": len(hits)}

        for k in k_values:
            top = hits[:k]
            row[f"P@{k}"] = (sum(binary[:k]) / k) if k else 0.0
            found = {h.metadata.get("source_path") for h in top} & want_books
            row[f"R@{k}"] = (len(found) / len(want_books)) if want_books else 0.0

        rr = next((1.0 / i for i, b in enumerate(binary, 1) if b), 0.0)
        row["RR"] = rr
        row[f"nDCG@{ndcg_k}"] = ndcg(rels, ndcg_k)

        # Tagging check: is the top hit tagged to the chapter we expected?
        if spec.get("chapter") and hits:
            field = st.chapter_field(spec["chapter"])
            row["top_tagged_expected"] = bool(hits[0].metadata.get(field))
            row["primary_matches"] = (
                hits[0].metadata.get("primary_chapter") == spec["chapter"])

        # §10.2 hard negatives.
        violations = []
        for bad in spec.get("must_not_return") or []:
            for rank, h in enumerate(hits[:max(k_values)], 1):
                if h.metadata.get("primary_chapter") == bad:
                    violations.append({"chapter": bad, "rank": rank,
                                       "book": h.metadata.get("source_path"),
                                       "heading": h.heading[:60]})
        row["violations"] = violations
        row["top_book"] = hits[0].metadata.get("source_path") if hits else None
        per_query.append(row)

    def mean(key: str) -> float:
        vals = [r[key] for r in per_query if key in r]
        return statistics.fmean(vals) if vals else 0.0

    summary = {f"P@{k}": mean(f"P@{k}") for k in k_values}
    summary.update({f"R@{k}": mean(f"R@{k}") for k in k_values})
    summary["MRR"] = mean("RR")
    summary[f"nDCG@{ndcg_k}"] = mean(f"nDCG@{ndcg_k}")
    tagged = [r for r in per_query if "top_tagged_expected" in r]
    summary["top1_tagged_expected"] = (
        statistics.fmean([float(r["top_tagged_expected"]) for r in tagged])
        if tagged else 0.0)
    summary["top1_primary_matches"] = (
        statistics.fmean([float(r["primary_matches"]) for r in tagged])
        if tagged else 0.0)
    summary["queries_with_zero_hits"] = sum(1 for r in per_query if r["n_hits"] == 0)
    summary["hard_negative_violations"] = sum(len(r["violations"]) for r in per_query)
    return {"summary": summary, "per_query": per_query}


def partition_queries(gold: dict) -> dict:
    """Classify every query by the Phase 8 answerability policy
    (eval/benchmark_v2_notes.md), without changing evaluate_queries() or
    relevance() at all.

    Fields read -- `answerable`, `exclude_from_aggregate` -- are optional and
    default to the pre-existing behaviour (every query is eligible) when
    absent, so this is a no-op for eval/gold.yaml, which has neither field.

    An "answerable" query (the default when the field is absent) with no
    relevance annotation at all (`relevant_books`, `graded`, and
    `relevant_chunks` all empty) is NOT silently folded into the eligible
    set as an ordinary zero -- it has no evidence to score against, which is
    a benchmark-authoring gap, not a retrieval result. It goes to
    `invalid_unresolved` instead.

    Returns {"eligible": [ids], "excluded_unanswerable": [ids],
             "invalid_unresolved": [ids]}, every id appearing in exactly one
    list.
    """
    eligible, excluded, invalid = [], [], []
    for spec in gold["queries"]:
        qid = spec["id"]
        answerable = spec.get("answerable", True)
        exclude = bool(spec.get("exclude_from_aggregate", False))
        has_labels = bool(spec.get("relevant_books") or spec.get("graded")
                         or spec.get("relevant_chunks"))
        if answerable is False or exclude:
            excluded.append(qid)
        elif not has_labels:
            invalid.append(qid)
        else:
            eligible.append(qid)
    return {"eligible": eligible, "excluded_unanswerable": excluded,
            "invalid_unresolved": invalid}


def aggregate(per_query: list[dict], ids, k_values: list[int], ndcg_k: int) -> dict | None:
    """Recompute the summary means over only `per_query` rows whose id is in
    `ids`, reusing rows evaluate_queries() already produced -- no retrieval
    is re-run here.

    Returns None, never a fabricated 0.0, when no row matches -- an empty
    eligible set must be visibly "no data", not indistinguishable from
    "every query failed".
    """
    ids = set(ids)
    rows = [r for r in per_query if r["id"] in ids]
    if not rows:
        return None

    def mean(key: str):
        vals = [r[key] for r in rows if key in r]
        return statistics.fmean(vals) if vals else None

    summary = {f"P@{k}": mean(f"P@{k}") for k in k_values}
    summary.update({f"R@{k}": mean(f"R@{k}") for k in k_values})
    summary["MRR"] = mean("RR")
    summary[f"nDCG@{ndcg_k}"] = mean(f"nDCG@{ndcg_k}")
    summary["n_queries"] = len(rows)
    return summary


def print_policy_table(summary: dict | None, k_values: list[int], ndcg_k: int, label: str) -> None:
    print(f"\n  {label}")
    print("  " + "─" * 60)
    if summary is None:
        print("  (no eligible queries -- N/A, not 0.000)")
        return
    header = f"  {'metric':24s}" + "".join(f"{f'@{k}':>10s}" for k in k_values)
    print(header)
    def fmt(v):
        return f"{v:>10.3f}" if v is not None else f"{'n/a':>10s}"
    print(f"  {'Precision':24s}" + "".join(fmt(summary[f'P@{k}']) for k in k_values))
    print(f"  {'Recall (book-level)':24s}" + "".join(fmt(summary[f'R@{k}']) for k in k_values))
    print("  " + "─" * 60)
    print(f"  {'MRR':24s}{fmt(summary['MRR'])}")
    print(f"  {f'nDCG@{ndcg_k}':24s}{fmt(summary[f'nDCG@{ndcg_k}'])}")
    print(f"  {'n_queries':24s}{summary['n_queries']:>10d}")


def tag_precision(cfg, store: Store, gold: dict, verbose: bool = True) -> dict:
    """§10.2 per-chapter tagging precision, via the gold spot-check lists."""
    spec = gold.get("tag_spotcheck") or {}
    plausible = spec.get("plausible_books") or {}
    n = int(spec.get("sample_per_chapter", 25))
    rng = random.Random(0)  # fixed seed so the number is reproducible
    out = {}
    for cid, books in plausible.items():
        field = st.chapter_field(cid)
        got = store.collection.get(where={field: True}, include=["metadatas"])
        metas = got["metadatas"] or []
        if not metas:
            out[cid] = {"tagged": 0, "sampled": 0, "precision": None}
            continue
        sample = rng.sample(metas, min(n, len(metas)))
        ok = sum(1 for m in sample if (m or {}).get("source_path") in set(books))
        out[cid] = {"tagged": len(metas), "sampled": len(sample),
                    "precision": ok / len(sample)}
    return out


def print_table(result: dict, k_values: list[int], ndcg_k: int, label: str) -> None:
    s = result["summary"]
    print(f"\n  {label}")
    print("  " + "─" * 60)
    header = f"  {'metric':24s}" + "".join(f"{f'@{k}':>10s}" for k in k_values)
    print(header)
    print(f"  {'Precision':24s}" + "".join(f"{s[f'P@{k}']:>10.3f}" for k in k_values))
    print(f"  {'Recall (book-level)':24s}" + "".join(f"{s[f'R@{k}']:>10.3f}" for k in k_values))
    print("  " + "─" * 60)
    print(f"  {'MRR':24s}{s['MRR']:>10.3f}")
    print(f"  {f'nDCG@{ndcg_k}':24s}{s[f'nDCG@{ndcg_k}']:>10.3f}")
    print(f"  {'top-1 tagged expected':24s}{s['top1_tagged_expected']:>10.1%}")
    print(f"  {'top-1 primary == expected':24s}{s['top1_primary_matches']:>10.1%}")
    print(f"  {'hard-negative violations':24s}{s['hard_negative_violations']:>10d}")
    print(f"  {'queries with zero hits':24s}{s['queries_with_zero_hits']:>10d}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Evaluate retrieval accuracy and precision")
    ap.add_argument("--hybrid", dest="hybrid", action="store_true", default=None)
    ap.add_argument("--no-hybrid", dest="hybrid", action="store_false")
    ap.add_argument("--compare", action="store_true",
                    help="run both dense-only and hybrid and print both")
    ap.add_argument("--ablate", action="store_true",
                    help="sweep evaluation.ablation.chunk_sizes x models (§10.3)")
    ap.add_argument("--worst", type=int, default=5,
                    help="show the N worst-performing queries")
    ap.add_argument("--no-save", action="store_true")
    ap.add_argument("--embed-preset", default=None,
                    help="force a model; by default the collection's own is used")
    ap.add_argument("--policy-aware", action="store_true",
                    help="also report aggregates restricted to answerable, "
                         "non-excluded queries (Phase 9); default run is unchanged")
    args = ap.parse_args(argv)

    cfg = st.load()
    gold = load_gold(cfg)
    k_values = [int(k) for k in cfg.get_path("evaluation.k_values", [3, 5, 10])]
    ndcg_k = int(cfg.get_path("evaluation.ndcg_k", 10))
    run_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S")

    if args.ablate:
        return run_ablation(cfg, gold, k_values, ndcg_k, run_id, save=not args.no_save)

    cfg, store = open_aligned(cfg, preset=args.embed_preset)
    retriever = Retriever(cfg, store=store)
    prov = st.provenance(cfg)

    print("=" * 68)
    print(f"EVALUATE  run {run_id}   config {prov['config_hash']}")
    print(f"  model      {prov['embedding_model']}")
    print(f"  gold set   {len(gold['queries'])} queries  "
          f"(status: {gold.get('meta', {}).get('status', 'unknown')}, "
          f"judging: {gold.get('meta', {}).get('judging', 'book_level')})")
    print(f"  collection {store.count():,} chunks")
    print("=" * 68)

    runs: dict[str, dict] = {}
    if args.compare:
        runs["dense only"] = evaluate_queries(cfg, retriever, gold, hybrid=False,
                                              k_values=k_values, ndcg_k=ndcg_k)
        runs["hybrid (dense+BM25, RRF)"] = evaluate_queries(
            cfg, retriever, gold, hybrid=True, k_values=k_values, ndcg_k=ndcg_k)
    else:
        label = ("hybrid (dense+BM25, RRF)" if args.hybrid is not False
                 else "dense only")
        runs[label] = evaluate_queries(cfg, retriever, gold, hybrid=args.hybrid,
                                       k_values=k_values, ndcg_k=ndcg_k)

    for label, result in runs.items():
        print_table(result, k_values, ndcg_k, label)

    # Cheap, retrieval-free check (Phase 10), computed once and reused below
    # for --policy-aware too: warn when the table just printed silently
    # folded forced-zero unanswerable/unresolved queries into its mean, so a
    # legacy-mode run can't be mistaken for the policy-aware corrected view.
    # For eval/gold.yaml, which has neither `answerable` nor
    # `exclude_from_aggregate` on any query, this is always empty and the
    # warning never fires -- verified in eval/test_evaluate_policy.py's test_8.
    partition = partition_queries(gold)
    legacy_excluded = partition["excluded_unanswerable"] + partition["invalid_unresolved"]
    if legacy_excluded and not args.policy_aware:
        print(f"\n  NOTE: the aggregate(s) above are the LEGACY mean — "
              f"{len(legacy_excluded)} query(ies) marked answerable:false / "
              f"exclude_from_aggregate / lacking any relevance label were forced to a "
              f"zero score and folded in: {legacy_excluded}. "
              f"Re-run with --policy-aware for the corrected, eligible-only view.")

    main_result = list(runs.values())[-1]

    if args.worst:
        ranked = sorted(main_result["per_query"], key=lambda r: (r["RR"], r["P@3"]))
        print(f"\n  worst {args.worst} queries (by MRR then P@3):")
        for r in ranked[: args.worst]:
            print(f"    {r['id']:8s} RR={r['RR']:.2f} P@3={r['P@3']:.2f} "
                  f"R@10={r['R@10']:.2f}  top={str(r['top_book'])[:40]}")
            print(f"             {r['query'][:70]}")

    violations = [(r["id"], v) for r in main_result["per_query"] for v in r["violations"]]
    if violations:
        print(f"\n  hard-negative violations ({len(violations)}):")
        for qid, v in violations[:12]:
            print(f"    {qid:8s} rank {v['rank']:2d} tagged {v['chapter']} "
                  f"— {str(v['book'])[:38]}")
    else:
        print("\n  hard negatives: no violations")

    print("\n  per-chapter tagging precision (spot-check against gold lists):")
    tp = tag_precision(cfg, store, gold)
    for cid in sorted(tp):
        row = tp[cid]
        p = row["precision"]
        bar = "" if p is None else "█" * int(round(p * 20))
        print(f"    {cid:4s} tagged {row['tagged']:5d}  "
              f"precision {'  n/a' if p is None else f'{p:5.1%}'}  {bar}")

    policy: dict | None = None
    if args.policy_aware:
        part = partition
        eligible = set(part["eligible"])
        uncertain_ids = {q["id"] for q in gold["queries"] if q.get("review_marker") == "uncertain"}
        sensitivity_ids = eligible - uncertain_ids

        print("\n" + "=" * 68)
        print("  POLICY-AWARE AGGREGATES (Phase 9 — eligible answerable queries only)")
        print("=" * 68)
        print(f"  eligible:            {len(part['eligible'])}  {part['eligible']}")
        print(f"  excluded (unanswerable / exclude_from_aggregate): "
              f"{len(part['excluded_unanswerable'])}  {part['excluded_unanswerable']}")
        print(f"  invalid/unresolved (answerable, no relevance labels): "
              f"{len(part['invalid_unresolved'])}  {part['invalid_unresolved']}")

        policy = {"partition": part, "eligible_by_run": {}, "sensitivity_by_run": {}}
        for label, result in runs.items():
            elig_summary = aggregate(result["per_query"], eligible, k_values, ndcg_k)
            print_policy_table(elig_summary, k_values, ndcg_k,
                               f"{label} — eligible only (n={len(eligible)})")
            policy["eligible_by_run"][label] = elig_summary

            sens_summary = aggregate(result["per_query"], sensitivity_ids, k_values, ndcg_k)
            print_policy_table(sens_summary, k_values, ndcg_k,
                               f"{label} — eligible, excluding {len(uncertain_ids)} uncertain-label "
                               f"quer{'y' if len(uncertain_ids) == 1 else 'ies'} "
                               f"(n={len(sensitivity_ids)})")
            policy["sensitivity_by_run"][label] = sens_summary

        if part["invalid_unresolved"]:
            print(f"\n  WARNING: {len(part['invalid_unresolved'])} query(ies) are answerable but "
                  f"carry no relevance annotation at all -- excluded from the eligible aggregate "
                  f"above as unresolved, not scored as zero: {part['invalid_unresolved']}")

    payload = {"run_id": run_id, "provenance": prov,
               "gold_meta": gold.get("meta", {}),
               "n_queries": len(gold["queries"]),
               "runs": {k: v["summary"] for k, v in runs.items()},
               "per_query": main_result["per_query"],
               "tag_precision": tp}
    if policy is not None:
        payload["policy_aware"] = policy
    if not args.no_save:
        results = st.resolve(cfg, "evaluation.results_dir")
        results.mkdir(parents=True, exist_ok=True)
        out = results / f"eval_{run_id}.json"
        # default=str: gold.yaml's `seeded_on:` parses to a datetime.date,
        # which json cannot serialise on its own.
        out.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str),
                       encoding="utf-8")
        print(f"\n  saved {out}")
    return 0


def run_ablation(cfg, gold, k_values, ndcg_k, run_id, save=True) -> int:
    """§10.3 — re-ingest and re-evaluate across settings, then compare.

    Each combination is a full rebuild into a throwaway collection, because
    changing the chunk size or the model changes every vector; anything less
    would compare against a stale index.
    """
    from .ingest import main as ingest_main

    ab = cfg["evaluation"]["ablation"]
    sizes = [int(s) for s in ab.get("chunk_sizes", [1000])]
    models = list(ab.get("models", [cfg.get_path("embedding.model")]))
    alts = cfg["embedding"].get("alternatives", {})
    by_model = {v.get("model"): k for k, v in alts.items()}
    by_model.setdefault(cfg.get_path("embedding.model"), None)

    rows = []
    print(f"ablation: {len(sizes)} chunk sizes x {len(models)} models "
          f"= {len(sizes)*len(models)} full rebuilds\n")
    for model in models:
        preset = by_model.get(model)
        if model not in by_model:
            print(f"  ! {model} is not in config.embedding.alternatives — skipping")
            continue
        for size in sizes:
            print(f"\n{'='*68}\nABLATION  model={model}  chunk={size}\n{'='*68}")
            argv = ["--rebuild", "--chunk-tokens", str(size)]
            if preset:
                argv += ["--embed-preset", preset]
            ingest_main(argv)
            sub = st.apply_overrides(st.load(), embed_preset=preset,
                                     chunk_tokens=size)
            store = Store(sub, create=False)
            res = evaluate_queries(sub, Retriever(sub, store=store), gold,
                                   hybrid=True, k_values=k_values, ndcg_k=ndcg_k)
            s = res["summary"]
            rows.append({"model": model, "chunk_tokens": size,
                         "chunks": store.count(),
                         "config_hash": st.config_hash(sub), **s})

    print("\n\n" + "=" * 96)
    print("ABLATION COMPARISON")
    print("=" * 96)
    hdr = (f"{'model':34s} {'chunk':>6s} {'chunks':>7s} "
           f"{'P@5':>7s} {'R@10':>7s} {'MRR':>7s} {'nDCG@10':>8s} {'viol':>5s}")
    print(hdr)
    print("-" * 96)
    for r in rows:
        print(f"{r['model'][:34]:34s} {r['chunk_tokens']:6d} {r['chunks']:7d} "
              f"{r['P@5']:7.3f} {r['R@10']:7.3f} {r['MRR']:7.3f} "
              f"{r[f'nDCG@{ndcg_k}']:8.3f} {r['hard_negative_violations']:5d}")
    if rows:
        best = max(rows, key=lambda r: r[f"nDCG@{ndcg_k}"])
        print(f"\nbest by nDCG@{ndcg_k}: {best['model']} @ {best['chunk_tokens']} tokens")
        print("NOTE: the store now holds whichever combination ran last. "
              "Re-run `python -m src.ingest --rebuild` with your chosen settings.")
    if save and rows:
        results = st.resolve(cfg, "evaluation.results_dir")
        results.mkdir(parents=True, exist_ok=True)
        (results / f"ablation_{run_id}.json").write_text(
            json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
