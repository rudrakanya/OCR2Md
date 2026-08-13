#!/usr/bin/env python3
"""
eval/ablate.py — the configuration sweep (§4.4).

The module that makes the whole plan accountable. It runs the gold set across
configurations and reports each with confidence intervals, so "we added hybrid
search" becomes "hybrid search moved Recall@20 from 0.71 to 0.84 ± 0.05".

    dense-only (v1 baseline)
      + BM25 + RRF
      + entity channel
      + reranker
      + contextualized chunks
      + all

Configurations are dict overlays, never code edits — that is what config.py's
`overlay` exists for, and it is why a results file can name the exact settings
that produced it.

Two disciplines the plan insists on, enforced here:

  Kill criteria. Each phase in §7 has a threshold below which the added
  complexity should be reverted rather than kept. `--check-kill` evaluates them
  against the measured deltas and says plainly whether a component earned its
  place. A sweep that cannot fail is not a measurement.

  Empty-pack accuracy is reported alongside every gain. §3.4 warns that this is
  the one place where a metric improvement can mask a capability regression, so
  a configuration that raises nDCG while leaking passages into expected-empty
  packs is flagged as a regression regardless of its headline number.

Usage:
    python -m eval.ablate --configs dense,hybrid,+entity,+rerank,all
    python -m eval.ablate --all --limit 30
    python -m eval.ablate --check-kill eval/results/ablation.json
"""
import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import config as config_mod                                         # noqa: E402
from config import CFG, overlay                                     # noqa: E402
from console import use_utf8                                        # noqa: E402

RESULTS = Path("eval/results")

# Each variant is an overlay onto the current config. Weights of 0 switch a
# channel off entirely — fusion.rrf skips zero-weighted channels, so this is a
# true ablation and not merely a down-weighting.
VARIANTS = {
    "dense": {
        "_desc": "v1 baseline: dense retrieval only, no rerank",
        "retrieval": {"rrf_weights": {"dense": 1.0, "sparse": 0.0, "entity": 0.0}},
        "rerank": {"backend": "none"},
    },
    "hybrid": {
        "_desc": "+ BM25 sparse channel, fused by RRF",
        "retrieval": {"rrf_weights": {"dense": 1.0, "sparse": 1.0, "entity": 0.0}},
        "rerank": {"backend": "none"},
    },
    "+entity": {
        "_desc": "+ entity-exact channel from the registry",
        "retrieval": {"rrf_weights": {"dense": 1.0, "sparse": 1.0, "entity": 1.0}},
        "rerank": {"backend": "none"},
    },
    "+rerank": {
        "_desc": "+ cross-encoder rerank and the relevance floor",
        "retrieval": {"rrf_weights": {"dense": 1.0, "sparse": 1.0, "entity": 1.0}},
    },
    "+reorder": {
        "_desc": "+ lost-in-the-middle pack reordering",
        "retrieval": {"lost_in_middle_reorder": True},
    },
    "no_reorder": {
        "_desc": "rerank without lost-in-the-middle reordering",
        "retrieval": {"lost_in_middle_reorder": False},
    },
    "all": {
        "_desc": "everything currently configured",
    },
}

# §7's kill criteria, as data. (metric, baseline_variant, min_gain, note)
KILL = {
    "+rerank": [("ndcg@10", "+entity", 0.05,
                 "§7 phase 1: if nDCG@10 gains < 5 pts or empty-pack accuracy drops, "
                 "revert to dense + ABS_FLOOR")],
    "hybrid": [("recall@20", "dense", 0.05,
                "§7 phase 1: hybrid must earn its complexity on recall")],
    "+entity": [("recall@20", "hybrid", 0.05,
                 "§7 phase 2: if Recall@20 gains < 5 pts, keep the registry (it pays for "
                 "itself in §5) but drop the retrieval channel")],
}


def run_variant(name, patch, limit, judge_facts, verbose):
    """Run one configuration end to end against the gold set."""
    from eval import eval_retrieval
    cfg = overlay(CFG, {k: v for k, v in patch.items() if not k.startswith("_")})

    # eval_retrieval and retrieve both read the module-level CFG, so the overlay
    # is installed there for the duration. Restored in `finally` — a sweep that
    # leaked config into later variants would silently compare the wrong things.
    import retrieve
    import rerank as rerank_mod
    saved = (config_mod.CFG, retrieve.CFG, rerank_mod.CFG, eval_retrieval.CFG)
    config_mod.CFG = retrieve.CFG = rerank_mod.CFG = eval_retrieval.CFG = cfg
    rerank_mod._cache.clear()
    retrieve._load_dense.cache_clear()
    try:
        t0 = time.time()
        res = eval_retrieval.run(limit=limit, judge_facts=judge_facts,
                                 verbose=verbose, label=name)
        res["variant"] = name
        res["description"] = patch.get("_desc", "")
        res["seconds"] = round(time.time() - t0, 1)
        return res
    finally:
        config_mod.CFG, retrieve.CFG, rerank_mod.CFG, eval_retrieval.CFG = saved
        rerank_mod._cache.clear()


def _get(res, metric):
    v = res["metrics"].get(metric)
    return v["mean"] if isinstance(v, dict) else v


def compare(results):
    """Table of variants with deltas against the previous row."""
    keys = ["recall@10", "recall@20", "ndcg@10", "mrr",
            "context_precision", "empty_pack_accuracy"]
    rows = []
    for i, r in enumerate(results):
        row = {"variant": r["variant"], "seconds": r.get("seconds")}
        for k in keys:
            row[k] = _get(r, k)
        if i:
            prev = results[i - 1]
            row["_delta"] = {k: (None if _get(r, k) is None or _get(prev, k) is None
                                 else round(_get(r, k) - _get(prev, k), 4)) for k in keys}
        rows.append(row)
    return rows


def check_kill(results):
    """Did each component clear its §7 threshold? Returns list of verdicts."""
    by_name = {r["variant"]: r for r in results}
    verdicts = []
    for variant, rules in KILL.items():
        if variant not in by_name:
            continue
        for metric, base, min_gain, note in rules:
            if base not in by_name:
                continue
            got, was = _get(by_name[variant], metric), _get(by_name[base], metric)
            if got is None or was is None:
                continue
            gain = got - was
            # The §3.4 override: a gain bought by leaking into expected-empty
            # packs is not a gain.
            emp_now = _get(by_name[variant], "empty_pack_accuracy")
            emp_was = _get(by_name[base], "empty_pack_accuracy")
            leaked = (emp_now is not None and emp_was is not None and emp_now < emp_was - 1e-9)
            verdicts.append({
                "component": variant, "metric": metric, "baseline": base,
                "from": round(was, 4), "to": round(got, 4), "gain": round(gain, 4),
                "threshold": min_gain,
                "verdict": ("REGRESSION (empty-pack accuracy fell)" if leaked
                            else "KEEP" if gain >= min_gain else "KILL"),
                "note": note,
            })
    return verdicts


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Sweep configurations against the gold set")
    ap.add_argument("--configs", help="comma-separated variant names")
    ap.add_argument("--all", action="store_true", help="the standard ladder")
    ap.add_argument("--limit", type=int, help="gold items per variant")
    ap.add_argument("--out", default=str(RESULTS / "ablation.json"))
    ap.add_argument("--no-judge", action="store_true")
    ap.add_argument("--check-kill", help="re-check kill criteria on an existing results file")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    if args.check_kill:
        data = json.loads(Path(args.check_kill).read_text(encoding="utf-8"))
        for v in check_kill(data["runs"]):
            print(f"{v['verdict']:34s} {v['component']:9s} {v['metric']:14s} "
                  f"{v['from']:.3f} -> {v['to']:.3f}  (+{v['gain']:.3f}, "
                  f"need +{v['threshold']})")
            print(f"    {v['note']}")
        return

    names = (["dense", "hybrid", "+entity", "+rerank", "all"] if args.all
             else [n.strip() for n in (args.configs or "dense,+rerank").split(",")])
    unknown = [n for n in names if n not in VARIANTS]
    if unknown:
        raise SystemExit(f"unknown variant(s) {unknown}; known: {sorted(VARIANTS)}")

    runs = []
    for name in names:
        print(f"\n=== {name}: {VARIANTS[name].get('_desc', '')} ===", flush=True)
        res = run_variant(name, VARIANTS[name], args.limit, not args.no_judge, args.verbose)
        from eval.eval_retrieval import print_report
        print_report(res)
        runs.append(res)

    table = compare(runs)
    verdicts = check_kill(runs)

    print("\n" + "=" * 96)
    hdr = ["variant", "recall@10", "recall@20", "ndcg@10", "mrr", "ctx_prec", "empty_acc"]
    print(f"{hdr[0]:12s}" + "".join(f"{h:>13s}" for h in hdr[1:]))
    for row in table:
        cells = [row.get(k) for k in
                 ["recall@10", "recall@20", "ndcg@10", "mrr",
                  "context_precision", "empty_pack_accuracy"]]
        print(f"{row['variant']:12s}" + "".join(
            f"{(f'{c:.3f}' if c is not None else '—'):>13s}" for c in cells))

    if verdicts:
        print("\nKill criteria (§7):")
        for v in verdicts:
            print(f"  {v['verdict']:34s} {v['component']:9s} {v['metric']:14s} "
                  f"{v['from']:.3f} -> {v['to']:.3f} (need +{v['threshold']})")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                               "table": table, "kill_criteria": verdicts, "runs": runs},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n-> {out}")


if __name__ == "__main__":
    main()
