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

    payload = {"run_id": run_id, "provenance": prov,
               "gold_meta": gold.get("meta", {}),
               "n_queries": len(gold["queries"]),
               "runs": {k: v["summary"] for k, v in runs.items()},
               "per_query": main_result["per_query"],
               "tag_precision": tp}
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
