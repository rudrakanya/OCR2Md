"""Chapter tagging (§7b) — embedding-based, no per-chunk LLM call.

    python -m src.tag                 # re-tag using stored vectors
    python -m src.tag --explain C08   # what is C08 actually pulling in?

Separate from ingest on purpose (§7b.4): re-tagging reads the chunk vectors
back out of Chroma and only re-embeds the 19 chapter descriptors, so tuning
descriptors or thresholds costs seconds rather than a full re-embed.
"""
from __future__ import annotations

import argparse
import json
import sys

import numpy as np

from . import settings as st
from .embedder import get_embedder
from .store import Store, open_aligned


def descriptor_text(chapter: dict) -> str:
    """The string that is actually embedded for a chapter.

    Title + scope + descriptor + keywords, because the descriptor alone misses
    exact technical vocabulary ('adhiṣṭhāna', 'तडाग') that appears verbatim in
    the corpus and carries most of the discriminating signal.
    """
    parts = [chapter.get("title", ""), chapter.get("scope", ""),
             " ".join(str(chapter.get("descriptor", "")).split())]
    kws = chapter.get("keywords") or []
    if kws:
        block = ", ".join(str(k) for k in kws)
        parts.extend([block] * max(1, int(chapter.get("_keyword_weight", 1))))
    return "\n".join(p for p in parts if p)


def normalize_scores(scores: np.ndarray, method: str) -> np.ndarray:
    """Correct for anisotropy before ranking chapters (§7b.3).

    Raw cosine in these embedding spaces is badly compressed — on the first
    real run the whole 4,338 x 19 score matrix had mean 0.845 and sd 0.019, and
    90% of chunks had their top two chapters within 0.02 of each other. In that
    regime a chapter whose descriptor happens to sit near the centre of the
    space wins almost everywhere: C06 collected 2,466 chunks, 57% of the corpus,
    while C10 tagged epigraphy at 4% precision.

    Standardising each chapter's column across chunks removes exactly that
    blanket advantage, so a chunk is tagged to the chapter it is UNUSUALLY
    close to rather than the one that is close to everything.

    Note that row (per-chunk) centring cannot change the ranking within a row —
    it subtracts a constant from every entry — so it only affects how the
    cutoff is read, never which chapters win.
    """
    if method == "none":
        return scores
    out = scores.astype(np.float64, copy=True)
    if method in ("chapter", "both"):
        mu = out.mean(axis=0, keepdims=True)
        sd = out.std(axis=0, keepdims=True)
        out = (out - mu) / np.clip(sd, 1e-9, None)
    if method in ("chunk", "both"):
        mu = out.mean(axis=1, keepdims=True)
        sd = out.std(axis=1, keepdims=True)
        out = (out - mu) / np.clip(sd, 1e-9, None)
    return out


def calibrate_cutoff(scores: np.ndarray, cfg) -> tuple[float, dict]:
    """§7b.3: derive the cutoff from the observed distribution.

    A fixed cosine threshold is meaningless across models — bge-m3 and e5 do
    not put their similarities on the same scale — so we never hardcode one.
    """
    t = cfg["tagging"]
    method = t.get("cutoff_method", "percentile")
    flat = scores.reshape(-1)
    stats = {
        "method": method,
        "mean": float(flat.mean()),
        "std": float(flat.std()),
        "p50": float(np.percentile(flat, 50)),
        "p90": float(np.percentile(flat, 90)),
        "p97": float(np.percentile(flat, 97)),
        "p99": float(np.percentile(flat, 99)),
        "max": float(flat.max()),
    }
    if method == "percentile":
        cutoff = float(np.percentile(flat, float(t.get("cutoff_percentile", 97.0))))
    elif method == "zscore":
        cutoff = stats["mean"] + float(t.get("cutoff_zscore_k", 2.0)) * stats["std"]
    elif method == "knee":
        # Largest drop in the sorted score curve, sampled to stay cheap.
        s = np.sort(flat)[::-1]
        s = s[: max(100, len(s) // 20)]
        d2 = np.diff(s, 2)
        cutoff = float(s[int(np.argmin(d2)) + 1])
    else:
        raise ValueError(f"unknown tagging.cutoff_method {method!r}")
    stats["cutoff"] = cutoff
    return cutoff, stats


def run_tagging(cfg, *, store: Store | None = None, embedder=None,
                run_id: str = "adhoc", verbose: bool = True) -> dict:
    store = store or Store(cfg, create=False)
    embedder = embedder or get_embedder(cfg)
    chapters = st.load_chapters(cfg)

    ids, vecs = store.all_embeddings()
    if len(ids) == 0:
        raise RuntimeError("collection is empty — run `python -m src.ingest --rebuild`")

    if verbose:
        print(f"tagging {len(ids):,} chunks against {len(chapters)} chapters")

    desc = [descriptor_text(c) for c in chapters]
    dvecs = embedder.embed_queries(desc)

    # Both sides are L2-normalised, so the dot product IS cosine similarity.
    raw = vecs @ dvecs.T                          # (n_chunks, n_chapters)

    t = cfg["tagging"]
    norm = str(t.get("score_normalization", "chapter"))
    scores = normalize_scores(raw, norm)

    top_n = int(t.get("top_n", 3))
    max_ch = int(t.get("max_chapters_per_chunk", 6))
    margin = float(t.get("low_confidence_margin", 0.02))
    cutoff, stats = calibrate_cutoff(scores, cfg)
    stats["normalization"] = norm
    if verbose:
        rf = raw.reshape(-1)
        print(f"  raw cosine:  mean {rf.mean():.4f}  sd {rf.std():.4f}  "
              f"min {rf.min():.4f}  max {rf.max():.4f}")
        print(f"  normalization: {norm}")
        print(f"  scored space: mean {stats['mean']:.4f}  sd {stats['std']:.4f}  "
              f"p90 {stats['p90']:.4f}  p99 {stats['p99']:.4f}  max {stats['max']:.4f}")
        print(f"  calibrated cutoff ({stats['method']}): {cutoff:.4f}")

    chapter_ids = [c["id"] for c in chapters]
    order = np.argsort(-scores, axis=1)
    metas: list[dict] = []
    counts = {cid: 0 for cid in chapter_ids}
    primary_counts = {cid: 0 for cid in chapter_ids}
    low_conf = 0

    for row in range(len(ids)):
        ranked = order[row]
        chosen = list(ranked[:top_n])
        for j in ranked[top_n:]:
            if scores[row, j] >= cutoff and len(chosen) < max_ch:
                chosen.append(j)
            else:
                break
        best = int(ranked[0])
        second = float(scores[row, ranked[1]]) if len(ranked) > 1 else 0.0
        is_low = (float(scores[row, best]) - second) < margin

        m: dict = {cid: False for cid in (st.chapter_field(c) for c in chapter_ids)}
        for j in chosen:
            m[st.chapter_field(chapter_ids[j])] = True
            counts[chapter_ids[j]] += 1
        m["primary_chapter"] = chapter_ids[best]
        m["chapters_str"] = ",".join(chapter_ids[j] for j in sorted(chosen))
        # Raw cosine is what a human can interpret; the normalised score is
        # what the ranking actually used. Keep both — reporting only one of
        # them makes the other impossible to reconstruct.
        m["chap_score_primary"] = round(float(raw[row, best]), 5)
        m["chap_z_primary"] = round(float(scores[row, best]), 5)
        m["chap_margin"] = round(float(scores[row, best]) - second, 5)
        m["chap_low_confidence"] = bool(is_low)
        primary_counts[chapter_ids[best]] += 1
        low_conf += int(is_low)
        metas.append(m)

    store.update_metadata(ids, metas)

    payload = {
        "run_id": run_id,
        "provenance": st.provenance(cfg),
        "tagging": {k: t.get(k) for k in
                    ("top_n", "cutoff_method", "cutoff_percentile", "cutoff_zscore_k",
                     "max_chapters_per_chunk", "low_confidence_margin")},
        "score_stats": stats,
        "tagged_counts": counts,
        "primary_counts": primary_counts,
        "low_confidence_chunks": low_conf,
        "chunks": len(ids),
    }
    store.record_run(f"{run_id}-tag", "tag", payload)
    results = st.resolve(cfg, "evaluation.results_dir")
    results.mkdir(parents=True, exist_ok=True)
    (results / f"tag_{run_id}.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    if verbose:
        print(f"\n  {'chapter':6s} {'tagged':>7s} {'primary':>8s}  title")
        for c in chapters:
            cid = c["id"]
            flag = "  <-- thin" if counts[cid] < int(
                cfg.get_path("reporting.thin_chapter_chunks", 40)) else ""
            print(f"  {cid:6s} {counts[cid]:7d} {primary_counts[cid]:8d}  "
                  f"{c['title'][:44]:44s}{flag}")
        print(f"\n  low-confidence (top-2 within {margin}): {low_conf:,} "
              f"({low_conf/len(ids):.1%})")
        if t.get("llm_verification", {}).get("enabled"):
            print("  llm_verification is enabled but not implemented — "
                  "see the hook in verify_low_confidence()")
    return payload


def verify_low_confidence(cfg, store, chunks) -> None:
    """§7b.5 hook: an optional LLM pass over low-confidence chunks.

    Intentionally unimplemented and off by default. When you want it, this is
    where it goes: select chunks where chap_low_confidence is True, ask a model
    to pick from the chapter list given the chunk text, and write the answer
    back with store.update_metadata. Everything it needs is already in place.
    """
    raise NotImplementedError(
        "LLM tag verification is a documented hook, not a built feature. "
        "Set tagging.llm_verification.enabled=false (default) to skip it."
    )


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="(Re)compute chapter tags without re-embedding")
    ap.add_argument("--explain", metavar="CHAPTER",
                    help="show the top chunks tagged to this chapter")
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--embed-preset", default=None,
                    help="force a model; by default the collection's own is used")
    args = ap.parse_args(argv)
    cfg, store = open_aligned(st.load(), preset=args.embed_preset,
                              verbose=not args.explain)

    if args.explain:
        field = st.chapter_field(args.explain)
        rows = store.collection.get(where={field: True},
                                    include=["metadatas", "documents"])
        if not rows["ids"]:
            print(f"no chunks tagged {args.explain}")
            return 1
        ranked = sorted(zip(rows["ids"], rows["documents"], rows["metadatas"]),
                        key=lambda r: -(r[2] or {}).get("chap_score_primary", 0))
        print(f"{len(rows['ids'])} chunks tagged {args.explain}; top {args.n} by score:\n")
        for cid, doc, meta in ranked[: args.n]:
            meta = meta or {}
            print(f"  {meta.get('chap_score_primary', 0):.4f}  "
                  f"[{meta.get('primary_chapter')}] {meta.get('book_title', '')[:40]}")
            print(f"          {meta.get('heading_path', '')[:80]}")
            print(f"          {' '.join(doc.split())[:150]}…\n")
        return 0

    run_tagging(cfg, store=store)
    return 0


if __name__ == "__main__":
    sys.exit(main())
