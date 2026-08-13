#!/usr/bin/env python3
"""
eval/eval_retrieval.py — retrieval metrics (§4.2).

    Recall@k          did the funnel surface the relevant passages at all?
                      The ceiling on everything downstream: a claim cannot be
                      verified against evidence that was never retrieved.
    nDCG@10           are they ranked well? The reranker's job.
    MRR               how deep is the first good hit?
    context precision fraction of the delivered pack that is relevant
    context recall    fraction of reference facts the pack covers — the metric
                      that predicts the [GAP] rate
    empty-pack acc.   on expected_empty items, did it correctly return nothing?
                      §3.4's guarantee, and the one place where a metric
                      improvement can mask a capability regression

Confidence intervals are bootstrapped, because at n = 80 a 2-point nDCG
difference is not a result. Every run records the config hash, the reranker that
actually ran, and the gold set's verified fraction, so a number can never be
attributed to settings or labels other than the ones that produced it.

Usage:
    python -m eval.eval_retrieval                       # current config
    python -m eval.eval_retrieval --out eval/results/baseline.json
    python -m eval.eval_retrieval --limit 20            # quick smoke run
"""
import argparse
import json
import math
import random
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import CFG                                              # noqa: E402
from console import use_utf8                                        # noqa: E402
from eval.goldset import load as load_gold, status as gold_status   # noqa: E402
from retrieve import Retriever, kb_stamp                            # noqa: E402

RESULTS = Path("eval/results")


def dcg(rels):
    return sum(r / math.log2(i + 2) for i, r in enumerate(rels))


def ndcg_at(ranked_rel, k, n_relevant):
    if not n_relevant:
        return None
    actual = dcg(ranked_rel[:k])
    ideal = dcg([1.0] * min(k, n_relevant))
    return actual / ideal if ideal else 0.0


def bootstrap_ci(values, samples=None, ci=None, seed=11):
    """Percentile bootstrap. Returns (mean, lo, hi)."""
    vals = [v for v in values if v is not None]
    if not vals:
        return None, None, None
    samples = samples or CFG.eval.bootstrap_samples
    ci = ci or CFG.eval.ci
    rng = random.Random(seed)
    means = []
    n = len(vals)
    for _ in range(samples):
        means.append(sum(vals[rng.randrange(n)] for _ in range(n)) / n)
    means.sort()
    lo = means[int((1 - ci) / 2 * samples)]
    hi = means[min(samples - 1, int((1 + ci) / 2 * samples))]
    return statistics.fmean(vals), lo, hi


def fact_coverage(facts, passages, client, model):
    """Fraction of reference facts the pack supports. Uses a judge; batched once."""
    from llm import complete_json
    if not facts:
        return None
    if not passages:
        return 0.0
    listing = "\n\n".join(p["text"][:1500] for p in passages)
    msgs = [{"role": "system", "content":
             "For each fact, say whether the supplied passages support it. Judge ONLY what the "
             "passages say — not what you know to be true. Return JSON only: "
             '{"results": [{"i": 0, "supported": true}]}'},
            {"role": "user", "content":
             f"PASSAGES:\n{listing[:40000]}\n\nFACTS:\n"
             + json.dumps(list(enumerate(facts)), ensure_ascii=False)}]
    try:
        data = complete_json(client, model, msgs, max_tokens=800, temperature=0.0, quiet=True)
        got = {int(r["i"]): bool(r.get("supported")) for r in data.get("results", [])}
    except Exception:                                   # noqa: BLE001
        return None
    return sum(1 for i in range(len(facts)) if got.get(i)) / len(facts)


def evaluate(items, retriever, client=None, model=None, judge_facts=True, verbose=False):
    """Run every gold item through the funnel and collect per-item metrics."""
    ks = CFG.eval.recall_k
    per = []
    for it in items:
        t0 = time.time()
        pack = retriever.subtopic([it["question"]], question=it["question"])
        elapsed = time.time() - t0
        got = [h["rowid"] for h in pack.kept]
        gold = set(it.get("relevant_chunks") or [])

        rec = {"id": it["id"], "kind": it.get("kind"), "expected_empty": it.get("expected_empty"),
               "n_kept": len(got), "status": pack.status, "seconds": round(elapsed, 2),
               "floor": round(pack.floor, 4), "n_candidates": pack.n_candidates}

        if it.get("expected_empty"):
            # The §3.4 regression test. THIN counts as a pass: the system said
            # "there is barely anything here", which is the honest answer.
            rec["empty_correct"] = 1.0 if pack.status in ("GAP", "THIN") else 0.0
            rec["leaked"] = len(got) if pack.status not in ("GAP", "THIN") else 0
        else:
            # Recall is measured against the fused candidate pool as well as the
            # delivered pack: they answer different questions. Low pool recall
            # means retrieval never found it; low pack recall with high pool
            # recall means the floor or the cap threw it away.
            fused_ids = [h["rowid"] for h in pack.diagnostics.get("fused_ids", [])] \
                if isinstance(pack.diagnostics.get("fused_ids"), list) else []
            for k in ks:
                hit = len(gold & set(got[:k]))
                rec[f"recall@{k}"] = hit / len(gold) if gold else None
            rels = [1.0 if r in gold else 0.0 for r in got]
            rec["ndcg@10"] = ndcg_at(rels, 10, len(gold))
            rec["mrr"] = next((1 / (i + 1) for i, r in enumerate(got) if r in gold), 0.0)
            rec["context_precision"] = (sum(rels) / len(rels)) if rels else 0.0
            if judge_facts and client:
                rec["context_recall"] = fact_coverage(
                    it.get("reference_facts") or [], pack.kept, client, model)
        per.append(rec)
        if verbose:
            print(f"  {it['id']:7s} {rec['status']:14s} kept={rec['n_kept']:2d} "
                  f"{'EMPTY-OK' if rec.get('empty_correct') == 1.0 else ''}"
                  f"{'LEAK' if rec.get('empty_correct') == 0.0 else ''} "
                  f"{elapsed:5.1f}s", flush=True)
    return per


def aggregate(per):
    """Roll per-item records into headline metrics with confidence intervals."""
    pos = [r for r in per if not r.get("expected_empty")]
    neg = [r for r in per if r.get("expected_empty")]
    out = {"n_items": len(per), "n_positive": len(pos), "n_expected_empty": len(neg)}

    for key in [f"recall@{k}" for k in CFG.eval.recall_k] + \
               ["ndcg@10", "mrr", "context_precision", "context_recall"]:
        m, lo, hi = bootstrap_ci([r.get(key) for r in pos])
        if m is not None:
            out[key] = {"mean": round(m, 4), "lo": round(lo, 4), "hi": round(hi, 4)}

    if neg:
        m, lo, hi = bootstrap_ci([r.get("empty_correct") for r in neg])
        out["empty_pack_accuracy"] = {"mean": round(m, 4), "lo": round(lo, 4),
                                      "hi": round(hi, 4)}
        out["leaked_passages"] = sum(r.get("leaked", 0) for r in neg)

    statuses = {}
    for r in per:
        statuses[r["status"]] = statuses.get(r["status"], 0) + 1
    out["status_counts"] = statuses
    out["thin_rate"] = round(
        sum(1 for r in pos if r["status"] in ("THIN", "GAP")) / len(pos), 4) if pos else None
    out["median_seconds"] = round(statistics.median([r["seconds"] for r in per]), 2) if per else 0
    return out


def run(limit=None, judge_facts=True, verbose=False, label=None):
    gold = load_gold()
    items = [i for i in gold["items"] if i.get("question")]
    if limit:
        items = items[:limit]
    if not items:
        raise SystemExit("gold set is empty — run: python -m eval.goldset --bootstrap 60 "
                         "--negatives 15")

    from llm import get_client
    client = get_client() if judge_facts else None
    r = Retriever()
    per = evaluate(items, r, client, CFG.eval.judge_model, judge_facts, verbose)
    agg = aggregate(per)

    gs = gold_status(gold)
    result = {
        "label": label or "current",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "config_hash": CFG.hash(),
        "config_diff": __import__("config").diff(CFG),
        "kb": kb_stamp(),
        "reranker": r.reranker.name,
        "reranker_calibrated": r.reranker.calibrated,
        "goldset": {"n": len(items), "verified_frac": round(gs["verified_frac"], 3)},
        "metrics": agg,
        "per_item": per,
    }
    return result


def print_report(result):
    m = result["metrics"]
    print(f"\nconfig {result['config_hash']}  kb {result['kb']['hash']}  "
          f"reranker {result['reranker']}"
          f"{'' if result['reranker_calibrated'] else ' (UNCALIBRATED)'}")
    gf = result["goldset"]["verified_frac"]
    print(f"gold set: {result['goldset']['n']} items, {gf * 100:.0f}% human-verified"
          + ("   ← metrics on unverified labels measure agreement, not correctness"
             if gf < 0.5 else ""))
    print()
    for key in [f"recall@{k}" for k in CFG.eval.recall_k] + \
               ["ndcg@10", "mrr", "context_precision", "context_recall",
                "empty_pack_accuracy"]:
        v = m.get(key)
        if v:
            print(f"  {key:22s} {v['mean']:.3f}  [{v['lo']:.3f}, {v['hi']:.3f}]")
    if "leaked_passages" in m:
        print(f"  {'leaked passages':22s} {m['leaked_passages']}"
              f"   (passages returned for questions the corpus cannot answer)")
    print(f"  {'thin/gap rate':22s} {m.get('thin_rate')}")
    print(f"  {'median seconds/query':22s} {m.get('median_seconds')}")
    print(f"  statuses: {m.get('status_counts')}")


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Retrieval metrics against the gold set")
    ap.add_argument("--out", help="write results JSON here")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--label", help="name this run in the results file")
    ap.add_argument("--no-judge", action="store_true", help="skip context-recall judging")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    result = run(limit=args.limit, judge_facts=not args.no_judge,
                 verbose=args.verbose, label=args.label)
    print_report(result)

    out = Path(args.out) if args.out else RESULTS / f"retrieval_{result['config_hash']}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n-> {out}")


if __name__ == "__main__":
    main()
