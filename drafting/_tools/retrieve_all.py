"""All retrieval for all 13 units in one in-memory pass.

Outputs (drafting/_runs/):
  retrieval_log.jsonl   one row per (unit, pass, scope, chunk) actually taken, with ranks/scores
  deepening_log.jsonl   one row per deepening step (rule fired, window, relevant count)
  prefilter_log.jsonl   one row per (unit, chunk) dropped before reading, with reason and score
  candidates.jsonl      union of surviving chunks: units/sub-topics/passes that retrieved each
  retrieval_summary.json counts per unit and per book

Pre-filter floor: r(chunk, unit) >= T (calibrated: no hand-kept C01 chunk below it).
Deepening rules use a stricter "relevant" = r >= T_deepen (precision-calibrated), where r is the
max dense cosine of the chunk over that unit's queries, OR the chunk reached
global fused rank <= RESCUE for one of the unit's queries (lexical/RRF rescue).
T and RESCUE come from calibrate.py (drafting/_runs/calibration.json).
"""
from __future__ import annotations
from pathlib import Path

import collections
import json
import sys
import time

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "drafting" / "_tools"))
from engine import RUNS, Corpus, fuse  # noqa: E402

GLOBAL_K, BOOK_K = 40, 5
# Same Anupa Pande monograph under two filenames (books_manifest.yaml rows 403/412):
# cite the Pande copy, drop the twin before reading, note it in every chapter.
TWIN_COPY = {"The Udayesvara Temple Art, Architecture and Philosophy of the Saiva Siddhanta.md":
             "The Udayesvara Temple - Anupa Pande.md"}


def load_queries():
    return [json.loads(l) for l in (RUNS / "queries.jsonl").open(encoding="utf-8")]


def score_all(C: Corpus, rows):
    qs = [r["q"] for r in rows]
    t = time.time()
    Q = Corpus.embed(qs)
    t_emb = time.time() - t
    t = time.time()
    D = (Q @ C.E.T).astype(np.float32)
    L = C.lex_scores(qs)
    F = fuse(D, L, C.dup)
    order = np.argsort(-F, axis=1, kind="stable")
    t_score = time.time() - t
    return Q, D, L, F, order, t_emb, t_score


def main():
    cal = json.loads((RUNS / "calibration.json").read_text(encoding="utf-8"))
    T, RESCUE, TD = cal["threshold_dense"], cal["rescue_rank"], cal["threshold_deepen"]
    t0 = time.time()
    C = Corpus()
    rows = load_queries()
    Q, D, L, F, order, t_emb, t_score = score_all(C, rows)
    N = len(C.ids)
    gr = np.empty_like(order)
    gr[np.arange(len(rows))[:, None], order] = np.arange(1, N + 1)[None, :]  # global fused rank

    book_cols = {b: np.where(C.src == b)[0] for b in C.books}
    # per-book fused ranking: RRF recomputed within the book's columns
    book_order = {}
    for b, cols in book_cols.items():
        Fb = fuse(D[:, cols], L[:, cols], C.dup[cols])
        book_order[b] = cols[np.argsort(-Fb, axis=1, kind="stable")]

    by_unit = collections.defaultdict(list)
    for i, r in enumerate(rows):
        by_unit[r["unit"]].append(i)

    rlog, dlog, plog = [], [], []
    cands: dict[str, dict] = {}
    summary = {"T": T, "T_deepen": TD, "RESCUE": RESCUE, "queries": len(rows), "units": {}}
    for u, qi in by_unit.items():
        qi = np.array(qi)
        rmax = D[qi].max(0)
        best_rank = gr[qi].min(0)
        relevant = (rmax >= T) | (best_rank <= RESCUE)          # pre-filter floor
        taken: dict[int, list] = collections.defaultdict(list)
        n_deep_g = n_deep_b = 0
        for i in qi:
            r = rows[i]
            # deepening relevance is judged per query: this query's dense score, or top-RESCUE for it
            strong = (D[i] >= TD) | (gr[i] <= RESCUE)
            # ---- global list with deepening --------------------------------
            depth = GLOBAL_K
            win = order[i, 29:40]
            if strong[win].any():
                depth = 80
                n_deep_g += 1
                dlog.append({"unit": u, "pass": r["pass_id"], "scope": "global", "rule": "relevant in ranks 30-40",
                             "relevant_in_window": int(strong[win].sum()), "extend_to": 80})
                while strong[order[i, depth - 10:depth]].any() and depth < N:
                    dlog.append({"unit": u, "pass": r["pass_id"], "scope": "global",
                                 "rule": f"relevant in ranks {depth - 9}-{depth}",
                                 "relevant_in_window": int(strong[order[i, depth - 10:depth]].sum()),
                                 "extend_to": depth + 40})
                    depth += 40
            for k, c in enumerate(order[i, :depth]):
                taken[int(c)].append((r["pass_id"], r["sub"], "global", k + 1))
            # ---- per-book sweep with deepening --------------------------------
            for b, bo in book_order.items():
                bo_i = bo[i]
                depth = min(BOOK_K, len(bo_i))
                if strong[bo_i[:5]].sum() >= 4 and len(bo_i) > 5:
                    n_deep_b += 1
                    nxt = min(depth + 10, len(bo_i))
                    dlog.append({"unit": u, "pass": r["pass_id"], "scope": b, "rule": ">=4 of top 5 relevant",
                                 "relevant_in_window": int(strong[bo_i[:5]].sum()), "extend_to": nxt})
                    depth = nxt
                    while depth < len(bo_i) and strong[bo_i[depth - 10:depth]].sum() >= 8:
                        nxt = min(depth + 10, len(bo_i))
                        dlog.append({"unit": u, "pass": r["pass_id"], "scope": b,
                                     "rule": f">=8 of book ranks {depth - 9}-{depth} relevant",
                                     "relevant_in_window": int(strong[bo_i[depth - 10:depth]].sum()),
                                     "extend_to": nxt})
                        depth = nxt
                for k, c in enumerate(bo_i[:depth]):
                    taken[int(c)].append((r["pass_id"], r["sub"], "book", k + 1))
        kept = dropped = dups = 0
        for c, hits in taken.items():
            cid = C.ids[c]
            m = C.meta[c]
            base = {"unit": u, "chunk_id": cid, "source_path": m["source_path"],
                    "dense_max": round(float(rmax[c]), 4), "best_global_rank": int(best_rank[c])}
            for p, s, sc, rk in hits:
                rlog.append({"unit": u, "pass": p, "sub": s, "scope": sc, "rank": rk, "chunk_id": cid,
                             "source_path": m["source_path"]})
            if not relevant[c]:
                plog.append(dict(base, reason=f"below threshold (dense_max {rmax[c]:.4f} < {T}, best global rank {best_rank[c]} > {RESCUE})"))
                dropped += 1
                continue
            if m["source_path"] in TWIN_COPY:
                plog.append(dict(base, reason=f"second copy of the Pande monograph; cited copy is {TWIN_COPY[m['source_path']]}"))
                dups += 1
                continue
            if m.get("is_duplicate") and m.get("duplicate_of") in C.idx:
                plog.append(dict(base, reason=f"is_duplicate twin of {m['duplicate_of']}", twin_of=m["duplicate_of"]))
                dups += 1
                continue
            e = cands.setdefault(cid, {"chunk_id": cid, "source_path": m["source_path"], "units": {}})
            subs = sorted({s for _, s, _, _ in hits})
            e["units"][u] = {"subs": subs, "passes": sorted({p for p, _, _, _ in hits}),
                             "dense_max": round(float(rmax[c]), 4), "best_global_rank": int(best_rank[c])}
            kept += 1
        summary["units"][u] = {"queries": len(qi), "retrieved_unique": len(taken), "prefiltered_out": dropped,
                               "duplicate_twins_dropped": dups, "to_read": kept,
                               "global_deepenings": n_deep_g, "book_deepenings": n_deep_b}
    # notes: originals of dropped twins
    for name, data in (("retrieval_log", rlog), ("deepening_log", dlog), ("prefilter_log", plog)):
        with (RUNS / f"{name}.jsonl").open("w", encoding="utf-8") as fh:
            for x in data:
                fh.write(json.dumps(x, ensure_ascii=False) + "\n")
    with (RUNS / "candidates.jsonl").open("w", encoding="utf-8") as fh:
        for e in sorted(cands.values(), key=lambda e: (e["source_path"], C.meta[C.idx[e["chunk_id"]]].get("chunk_index", 0))):
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")
    allret = {x["chunk_id"] for x in rlog}
    summary.update(union_retrieved=len(allret), union_to_read=len(cands),
                   embed_seconds=round(t_emb, 2), score_seconds=round(t_score, 2),
                   total_seconds=round(time.time() - t0, 2))
    (RUNS / "retrieval_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
