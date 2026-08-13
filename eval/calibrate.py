#!/usr/bin/env python3
"""
eval/calibrate.py — measure RERANK_FLOOR instead of guessing it (§3.4).

The floor is the load-bearing number in v2's retrieval layer. Set too low it
admits everything and the empty-pack guarantee is gone; set too high it starves
sub-topics the corpus genuinely covers. §3.4 says calibrate it on the gold set,
and this is that step.

The method is a sweep, not an optimisation, because the two errors are not
symmetric and must not be traded off blindly:

    leakage    a passage returned for a question the corpus cannot answer.
               This is the failure that reaches the manuscript as a fabricated
               claim with a valid-looking citation, so it is weighted hardest.
    starvation a passage withheld from a question the corpus can answer. Costs
               a thinner chapter — bad, but visible as a [GAP] rather than
               invisible as an error.

So the objective maximises F-beta with beta < 1 (precision-weighted), and the
report prints the whole curve rather than only the winner: a floor that is best
by a hair over a wide plateau should be chosen from the middle of the plateau,
not from the peak, because the peak is noise at n = 80.

The candidate floor is applied to the CURRENT reranker backend only. Backends
score on different scales (see config.rerank_floor_by_backend), so a floor
calibrated for jina must never be written to bge's entry.

Usage:
    python -m eval.calibrate                 # sweep and report
    python -m eval.calibrate --write         # ...and save into config.json
    python -m eval.calibrate --min 0.05 --max 0.60 --step 0.025
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import CFG, load as load_cfg                            # noqa: E402
from console import use_utf8                                        # noqa: E402
from eval.goldset import load as load_gold                          # noqa: E402
from retrieve import Retriever                                      # noqa: E402

CONFIG_JSON = Path("config.json")


def collect(items, retriever, keep=200):
    """Score every gold item once, keeping all reranked candidates.

    One retrieval pass serves the whole sweep: the floor is applied afterwards
    to scores already computed, so trying twenty thresholds costs no more API
    calls than trying one.
    """
    rows = []
    for it in items:
        pack = retriever.subtopic([it["question"]], question=it["question"], keep=keep)
        scored = [(h["rowid"], h["score"]) for h in pack.kept]
        rows.append({"id": it["id"], "expected_empty": bool(it.get("expected_empty")),
                     "gold": set(it.get("relevant_chunks") or []), "scored": scored})
        print(f"  {it['id']:7s} {len(scored):3d} candidates "
              f"{'(expected empty)' if it.get('expected_empty') else ''}", flush=True)
    return rows


def evaluate_floor(rows, floor, rel_margin, keep_per_sub):
    """Apply a candidate floor to pre-computed scores. Returns counts."""
    tp = fp = fn = 0
    leaked = empty_ok = n_empty = 0
    for r in rows:
        if not r["scored"]:
            kept = []
        else:
            top = max(s for _, s in r["scored"])
            cut = max(floor, top - rel_margin)
            kept = [i for i, s in r["scored"] if s >= cut][:keep_per_sub]
        if r["expected_empty"]:
            n_empty += 1
            if kept:
                leaked += len(kept)
            else:
                empty_ok += 1
        else:
            got = set(kept)
            tp += len(got & r["gold"])
            fp += len(got - r["gold"])
            fn += len(r["gold"] - got)
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    return {"floor": round(floor, 4), "precision": round(prec, 4), "recall": round(rec, 4),
            "empty_accuracy": round(empty_ok / n_empty, 4) if n_empty else None,
            "leaked": leaked, "tp": tp, "fp": fp, "fn": fn}


def fbeta(p, r, beta=0.5):
    if not p or not r:
        return 0.0
    b2 = beta * beta
    return (1 + b2) * p * r / (b2 * p + r)


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Calibrate the relevance floor on the gold set")
    ap.add_argument("--min", type=float, default=0.05)
    ap.add_argument("--max", type=float, default=0.60)
    ap.add_argument("--step", type=float, default=0.025)
    ap.add_argument("--beta", type=float, default=0.5,
                    help="<1 weights precision (leakage) over recall (starvation)")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--write", action="store_true", help="save the chosen floor to config.json")
    args = ap.parse_args()

    gold = load_gold()
    items = [i for i in gold["items"] if i.get("question")]
    if args.limit:
        items = items[:args.limit]
    if not items:
        raise SystemExit("gold set is empty — run: python -m eval.goldset --bootstrap 60 "
                         "--negatives 15")
    n_empty = sum(1 for i in items if i.get("expected_empty"))
    if n_empty < 5:
        print(f"WARNING: only {n_empty} expected_empty item(s). The floor cannot be "
              f"calibrated against leakage without them, and leakage is the error "
              f"that matters. Run: python -m eval.goldset --negatives 15\n")

    r = Retriever()
    backend = r.reranker.name
    if not r.reranker.calibrated:
        raise SystemExit(f"reranker '{backend}' reports itself uncalibrated — an absolute "
                         f"floor against its scores would be meaningless. Configure a "
                         f"hosted or bge backend first.")
    print(f"scoring {len(items)} gold item(s) once with backend '{backend}' ...", flush=True)
    rows = collect(items, r)

    rel = (CFG.retrieval.get("rel_margin_by_backend") or {}).get(
        backend, CFG.retrieval.rel_margin)
    keep = CFG.retrieval.keep_per_sub

    sweep, f = [], []
    x = args.min
    while x <= args.max + 1e-9:
        m = evaluate_floor(rows, x, rel, keep)
        m["f_beta"] = round(fbeta(m["precision"], m["recall"], args.beta), 4)
        sweep.append(m)
        f.append(m["f_beta"])
        x += args.step

    print(f"\n{'floor':>7s} {'prec':>7s} {'recall':>7s} {'F%.1f' % args.beta:>7s} "
          f"{'empty':>7s} {'leaked':>7s}")
    print("-" * 48)
    best = max(sweep, key=lambda m: (m["f_beta"], m["empty_accuracy"] or 0))
    for m in sweep:
        mark = "  <-- best" if m is best else ""
        print(f"{m['floor']:7.3f} {m['precision']:7.3f} {m['recall']:7.3f} "
              f"{m['f_beta']:7.3f} "
              f"{(m['empty_accuracy'] if m['empty_accuracy'] is not None else 0):7.3f} "
              f"{m['leaked']:7d}{mark}")

    # Prefer the middle of a plateau over the peak: at n = 80 a peak is noise.
    top = max(f)
    plateau = [sweep[i]["floor"] for i, v in enumerate(f) if v >= top - 0.01]
    chosen = plateau[len(plateau) // 2] if plateau else best["floor"]
    print(f"\nbest F{args.beta} at floor {best['floor']}; plateau within 0.01 spans "
          f"{min(plateau):.3f}-{max(plateau):.3f}")
    print(f"CHOSEN: {chosen:.3f} (middle of the plateau, not the peak)")
    if best["leaked"]:
        print(f"NOTE: {best['leaked']} passage(s) still leak into expected-empty packs at "
              f"the best floor. Raise --max, or accept that some negatives are genuinely "
              f"near-covered by the corpus.")

    out = Path("eval/results/calibration.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"backend": backend, "rel_margin": rel, "beta": args.beta,
                               "chosen": chosen, "plateau": [min(plateau), max(plateau)],
                               "goldset_n": len(items), "n_expected_empty": n_empty,
                               "sweep": sweep}, indent=1), encoding="utf-8")
    print(f"-> {out}")

    if args.write:
        cfg = json.loads(CONFIG_JSON.read_text(encoding="utf-8")) if CONFIG_JSON.exists() else {}
        ret = cfg.setdefault("retrieval", {})
        by = ret.setdefault("rerank_floor_by_backend",
                            dict(CFG.retrieval.get("rerank_floor_by_backend") or {}))
        by[backend] = round(chosen, 4)
        ret["rerank_floor_calibrated"] = True
        cfg.setdefault("version", CFG.get("version"))
        CONFIG_JSON.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
        print(f"wrote rerank_floor_by_backend['{backend}'] = {chosen:.3f} -> {CONFIG_JSON}")
        print("This changes the config hash, so evidence packs built before now are stale: "
              "python make_evidence.py --check")


if __name__ == "__main__":
    main()
