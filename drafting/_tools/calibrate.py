"""Calibrate the pre-filter threshold on hand-judged Chapter 1 chunks.

Uses every C01 chunk judged by hand in the pilot (keep/reject, read in full),
scored against all C01 queries in queries.jsonl. Writes drafting/_runs/calibration.json
with the band table, the chosen threshold, and a 60-chunk stratified sample
(12 per score band) with the hand decision and reason.
"""
from pathlib import Path
import json
import random
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "drafting" / "_tools"))
from engine import RUNS, Corpus, fuse  # noqa: E402

MARGIN = 0.02
RESCUE = 10
DEEPEN_PRECISION = 0.30  # deepening "relevant": lowest dense where >= 30% of hand-judged chunks were kept


def main():
    C = Corpus()
    rows = [json.loads(l) for l in (RUNS / "queries.jsonl").open(encoding="utf-8")]
    rows = [r for r in rows if r["unit"] == "C01"]
    Q = Corpus.embed([r["q"] for r in rows])
    D = Q @ C.E.T
    L = C.lex_scores([r["q"] for r in rows])
    F = fuse(D, L, C.dup)
    order = np.argsort(-F, axis=1, kind="stable")
    gr = np.empty_like(order)
    gr[np.arange(len(rows))[:, None], order] = np.arange(1, len(C.ids) + 1)[None, :]
    J = {}
    for l in (RUNS / "C01_judgments.jsonl").open(encoding="utf-8"):
        d = json.loads(l)
        J[d["chunk_id"]] = d
    ids = list(J)
    ix = np.array([C.idx[c] for c in ids])
    y = np.array([J[c]["decision"] == "keep" for c in ids])
    d = D[:, ix].max(0)
    rk = gr[:, ix].min(0)
    T = float(np.floor((d[y].min() - MARGIN) * 100) / 100)
    rel = (d >= T) | (rk <= RESCUE)
    table = []
    for t in [0.30, 0.32, 0.34, 0.36, 0.38, 0.40, 0.42, 0.45]:
        m = (d >= t) | (rk <= RESCUE)
        table.append({"T": t, "pass": int(m.sum()), "keeps_lost": int((y & ~m).sum()),
                      "rejects_dropped": int((~y & ~m).sum())})
    bands = [(0, 0.30), (0.30, T), (T, 0.42), (0.42, 0.48), (0.48, 1)]
    rnd = random.Random(13)
    sample = []
    band_stats = []
    for lo, hi in bands:
        sel = [i for i in range(len(ids)) if lo <= d[i] < hi]
        band_stats.append({"band": f"{lo:.2f}-{hi:.2f}", "n": len(sel), "keeps": int(y[sel].sum()) if sel else 0})
        for i in rnd.sample(sel, min(12, len(sel))):
            m = C.meta[ix[i]]
            sample.append({"band": f"{lo:.2f}-{hi:.2f}", "chunk_id": ids[i], "source": m["source_path"],
                           "page": m.get("page_start"), "dense_max": round(float(d[i]), 4),
                           "best_global_rank": int(rk[i]), "hand_decision": J[ids[i]]["decision"],
                           "reason": J[ids[i]]["reason"]})
    curve = []
    for t in np.arange(0.36, 0.62, 0.02):
        m = d >= t
        curve.append({"T": round(float(t), 2), "n": int(m.sum()), "keeps": int((y & m).sum()),
                      "precision": round(float((y & m).sum() / max(m.sum(), 1)), 3),
                      "recall": round(float((y & m).sum() / y.sum()), 3)})
    TD = next(c["T"] for c in curve if c["precision"] >= DEEPEN_PRECISION)
    out = {"judged": len(ids), "keeps": int(y.sum()), "min_keep_dense": round(float(d[y].min()), 4),
           "keep_dense_quantiles": dict(zip(["min", "p05", "p10", "p25", "p50"],
                                            [round(float(x), 4) for x in np.quantile(d[y], [0, .05, .1, .25, .5])])),
           "threshold_dense": round(T, 2), "threshold_deepen": TD, "deepen_precision_target": DEEPEN_PRECISION,
           "precision_curve": curve, "rescue_rank": RESCUE, "margin": MARGIN,
           "at_threshold": {"pass": int(rel.sum()), "keeps_lost": int((y & ~rel).sum()),
                            "rejects_dropped": int((~y & ~rel).sum())},
           "table": table, "bands": band_stats, "sample": sample}
    (RUNS / "calibration.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in out.items() if k != "sample"}, indent=1))
    print("sample:", len(sample), "hand keeps in sample:", sum(s["hand_decision"] == "keep" for s in sample))


if __name__ == "__main__":
    main()
