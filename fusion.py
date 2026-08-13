#!/usr/bin/env python3
"""
fusion.py — Reciprocal Rank Fusion across the dense, sparse and entity channels.

    score(d) = Σ_c  w_c / (k + rank_c(d)),    k = 60

RRF is rank-based, which is the whole point: a cosine similarity in [0.7, 0.95]
and a BM25 score in [0, 40] have no shared scale, and any attempt to normalise
one onto the other bakes in an assumption about their distributions that changes
the moment the corpus does. Ranks are comparable by construction.

The cost is that the fused score has no absolute meaning. An RRF score of 0.03
says nothing about whether a passage is relevant — which is why the relevance
floor cannot live here and moves downstream to the reranker (§3.4). Nothing in
this module should ever be used as a relevance threshold.

    from fusion import rrf
    fused = rrf({"dense": dense_hits, "sparse": bm25_hits, "entity": ent_hits},
                weights={"dense": 1.0, "sparse": 1.0, "entity": 1.0}, k=60)
    # -> [{rowid, rrf, channels: {...}, ranks: {...}, ...merged fields}]
"""
import collections


def rrf(channels, weights=None, k=60, key="rowid", limit=None):
    """Fuse ranked hit lists. Input order within each list IS its ranking.

    `channels`  {channel_name: [hit, ...]} — each hit a dict carrying `key`.
    `weights`   {channel_name: float}; missing channels default to 1.0.
    Returns hits sorted by fused score, each annotated with:
        rrf       the fused score
        ranks     {channel: 1-based rank} for every channel that found it
        channels  the list of channels that found it
        scores    {channel: that channel's own raw score}
    """
    weights = weights or {}
    acc = collections.defaultdict(float)
    ranks = collections.defaultdict(dict)
    scores = collections.defaultdict(dict)
    merged = {}

    for cname, hits in channels.items():
        w = float(weights.get(cname, 1.0))
        if w == 0:
            continue
        for rank, h in enumerate(hits, start=1):
            kid = h[key]
            acc[kid] += w / (k + rank)
            ranks[kid][cname] = rank
            if "score" in h:
                scores[kid][cname] = float(h["score"])
            # Keep the fullest record seen: channels return the same columns,
            # but the entity channel adds `hits`/`ents` and the dense channel
            # may carry only ids.
            if kid not in merged or len(h) > len(merged[kid]):
                merged[kid] = h

    out = []
    for kid, s in acc.items():
        rec = dict(merged[kid])
        rec.pop("score", None)          # a channel-local score; would mislead downstream
        rec["rrf"] = s
        rec["ranks"] = ranks[kid]
        rec["channels"] = sorted(ranks[kid])
        rec["scores"] = scores[kid]
        out.append(rec)

    out.sort(key=lambda r: (-r["rrf"], r[key]))
    return out[:limit] if limit else out


def channel_report(fused, top=None):
    """How much each channel contributed to the top of the fused list.

    Read this before tuning weights. If the entity channel never appears in the
    top 20, either the registry is thin for this sub-topic or the weight is
    wrong — and those have different fixes.
    """
    window = fused[:top] if top else fused
    counts = collections.Counter()
    solo = collections.Counter()
    for r in window:
        for c in r["channels"]:
            counts[c] += 1
        if len(r["channels"]) == 1:
            solo[r["channels"][0]] += 1
    return {"n": len(window), "present": dict(counts), "unique_to": dict(solo)}
