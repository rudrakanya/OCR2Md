#!/usr/bin/env python3
"""
retrieve.py — the hybrid retrieval funnel (§3.3-3.7). Replaces kb_search.py.

    5 queries x (dense top-30 + BM25 top-30)   ->  ~250 hits
            + entity-exact channel             ->  ~30 hits
            -> dedupe -> RRF                   ->  ~120 unique candidates
            -> cross-encoder rerank            ->  120 scored
            -> relevance floor on rerank score ->  variable
            -> source-diversity cap            ->  <= 50% per source, min 3
            -> keep_per_sub                    ->  8-12 passages

The empty-pack guarantee (§3.4)
-------------------------------
This is the property the migration is most likely to lose silently, and losing
it would do more damage to the manuscript than anything else in the plan. v1's
ABS_FLOOR = 0.76 is what stops a sub-topic with no regional coverage receiving
eight confidently-retrieved passages about Thanjavur. RRF scores cannot carry
that guarantee — a fused score of 0.03 says nothing about relevance — so the
floor moves to the reranker, which judges (query, passage) pairs directly.

Three rules keep it honest:

  1. The absolute floor applies only to a reranker that reports itself
     `calibrated`. An uncalibrated backend (LLM listwise, or the noop) falls
     back to v1's dense cosine floor rather than to no floor at all.
  2. An empty pack is a correct output. It flows to [GAP - not in sources],
     exactly as in v1. Nothing here back-fills a pack to look busy.
  3. `THIN_KEEP`/`THIN_SCORE` survive, but should now rarely fire. If they fire
     as often as they did in v1, hybrid retrieval has not improved recall and
     that is a finding, not a nuisance — `--report` prints the rate.

    from retrieve import Retriever
    r = Retriever()
    pack = r.subtopic(queries, question="...", filters={"kind": "primary"})
    pack.kept        # [{rowid, score, source, trail, text, ...}]
    pack.status      # OK | THIN | SINGLE-SOURCE | GAP
    pack.diagnostics # channel contributions, floor used, what was cut and why

CLI:
    python retrieve.py "the bhumija sikhara of the Udayesvara temple"
    python retrieve.py "..." --kind primary --explain
"""
import argparse
import collections
import hashlib
import json
import os
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np

from config import CFG
from entities import EntityIndex
from fusion import channel_report, rrf
from kb_store import KBStore
from textnorm import WORD_RE, fold

KB_DIR = Path(os.environ.get("KB_DIR", "kb"))


class KBError(RuntimeError):
    pass


@dataclass
class Pack:
    """One sub-topic's retrieved evidence, with the reasoning that produced it."""
    kept: list = field(default_factory=list)
    status: str = "GAP"
    note: str = ""
    floor: float = 0.0
    n_candidates: int = 0
    queries: list = field(default_factory=list)
    diagnostics: dict = field(default_factory=dict)

    def sources(self):
        return {h["source"] for h in self.kept}

    def words(self):
        return sum(len(h["text"].split()) for h in self.kept)


@lru_cache(maxsize=1)
def _load_dense():
    cfg_path = KB_DIR / "config.json"
    if not cfg_path.exists():
        raise KBError(f"Knowledge base not found in '{KB_DIR}/'. Build it first:\n"
                      f'    python build_kb.py "Udaypur Reference Markdown Files"')
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    emb = np.load(KB_DIR / "embeddings.npy")
    if emb.shape[0] != cfg.get("count"):
        raise KBError(f"KB inconsistent: {emb.shape[0]} vectors vs {cfg.get('count')} "
                      f"recorded chunks. Rebuild it.")
    return cfg, emb


# The config sections that actually determine what an evidence pack contains.
#
# Deliberately NOT the whole config. Stamping with CFG.hash() made every pack
# stale the moment any setting moved — raising a gap-marker cap in `verify`
# invalidated 19 evidence packs that no retrieval setting had touched, and the
# only way to draft again was to re-run retrieval for nothing. A staleness guard
# that cries wolf gets switched off, which would cost the real protection: packs
# that silently predate their KB.
PACK_SECTIONS = ("chunking", "embedding", "comprehension", "retrieval", "rerank")


def kb_stamp():
    """Identity of the current KB build + the settings that shaped a pack.

    v1 folded built_at and count into the hash after discovering that a
    fingerprint over source files alone stayed identical across a rebuild that
    recomputed every vector. v2 adds the retrieval-relevant config, so a pack
    can never be attributed to retrieval settings other than the ones that
    produced it — while generation, verification and eval settings move freely.
    """
    cfg, _ = _load_dense()
    conf = CFG.section_hash(*PACK_SECTIONS)
    ident = json.dumps({"fp": cfg.get("fingerprint", {}), "built_at": cfg.get("built_at"),
                        "count": cfg.get("count"), "model": cfg.get("model"),
                        "config": conf}, sort_keys=True, ensure_ascii=False)
    return {"built_at": cfg.get("built_at"), "count": cfg.get("count"),
            "model": cfg.get("model"), "config": conf,
            "full_config": CFG.hash(),      # recorded, but not part of staleness
            "contextualized": bool(cfg.get("contextualized")),
            "hash": hashlib.sha1(ident.encode("utf-8")).hexdigest()[:16]}


class Retriever:
    """The whole funnel, reusable across sub-topics."""

    def __init__(self, store=None, entities=None, reranker=None, cfg=None, client=None):
        self.cfg = cfg or CFG
        self.store = store or KBStore()
        self.entities = entities if entities is not None else EntityIndex.load()
        self.query_aliases = self.entities.query_alias_map()
        self._client = client
        self._reranker = reranker
        self._embed_cache = {}
        # EN/HI editorial pairing (§3.2): a translation and its original are one
        # testimony, so they share a diversity-cap budget. Without this a
        # sub-topic can be filled twice over with the same passage in two
        # languages and look well-sourced.
        self.source_group = {}
        for pair in self.cfg.retrieval.get("translation_pairs", []):
            head = pair[0]
            for s in pair:
                self.source_group[s] = head

    # -- lazily-built collaborators -----------------------------------------

    @property
    def client(self):
        if self._client is None:
            from llm import get_client
            self._client = get_client()
        return self._client

    @property
    def reranker(self):
        if self._reranker is None:
            from rerank import get_reranker
            self._reranker = get_reranker()
        return self._reranker

    def group_of(self, source):
        return self.source_group.get(source, source)

    # -- channels -------------------------------------------------------------

    def _embed(self, queries):
        want = [q for q in queries if q not in self._embed_cache]
        if want:
            from kb_search import embed_texts        # shared batching + retry
            cfg, _ = _load_dense()
            vecs = embed_texts(self.client, cfg["model"], want)
            for q, v in zip(want, vecs):
                a = np.asarray(v, dtype="float32")
                n = np.linalg.norm(a)
                self._embed_cache[q] = a / (n if n else 1.0)
        return [self._embed_cache[q] for q in queries]

    def dense(self, queries, k, allowed=None):
        """Cosine top-k per query. `allowed` masks the matrix for §3.6 filtering."""
        cfg, emb = _load_dense()
        out = []
        mask = None
        if allowed is not None:
            mask = np.zeros(emb.shape[0], dtype=bool)
            idx = np.fromiter(allowed, dtype=np.int64, count=len(allowed))
            idx = idx[(idx >= 0) & (idx < emb.shape[0])]
            mask[idx] = True
        for vec in self._embed(queries):
            sims = emb @ vec
            if mask is not None:
                sims = np.where(mask, sims, -np.inf)
            take = min(k, int(mask.sum()) if mask is not None else emb.shape[0])
            if take <= 0:
                out.append([])
                continue
            top = np.argpartition(-sims, take - 1)[:take]
            top = top[np.argsort(-sims[top])]
            rows = self.store.chunks_for([int(i) for i in top])
            out.append([{**rows[int(i)], "score": float(sims[i])}
                        for i in top if int(i) in rows])
        return out

    def sparse(self, queries, k, filters=None):
        return [self.store.search_bm25(q, k=k, filters=filters,
                                       alias_map=self.query_aliases)
                for q in queries]

    def entity_channel(self, text, k, filters=None):
        """Chunks naming the entities the sub-topic itself names."""
        ids, seen = [], set()
        for w in WORD_RE.findall(text or ""):
            eid = self.entities.resolve(w)
            if eid and eid not in seen:
                seen.add(eid)
                ids.append(eid)
        if not ids:
            return [], []
        return self.store.search_entities(ids, k=k, filters=filters), ids

    # -- funnel ---------------------------------------------------------------

    def subtopic(self, queries, question=None, filters=None, keep=None, explain=False):
        """Run the whole funnel for one sub-topic."""
        rcfg = self.cfg.retrieval
        keep = keep or rcfg.keep_per_sub
        queries = list(queries)
        question = question or (queries[0] if queries else "")

        # Always ask, even with no explicit filters: the label layer's
        # retrievable gate applies by default, and skipping the mask here would
        # let the dense channel return index pages and near-duplicates that the
        # sparse channel is already excluding.
        allowed = self.store.allowed_rowids(filters)
        if allowed is not None and not allowed:
            return Pack(status="GAP", queries=queries,
                        note="the metadata/label filter admits no chunks at all",
                        diagnostics={"filters": filters, "allowed": 0})

        dense_lists = self.dense(queries, rcfg.dense_k, allowed=allowed)
        sparse_lists = self.sparse(queries, rcfg.sparse_k, filters=filters)
        ent_hits, ent_ids = self.entity_channel(question, rcfg.entity_k, filters=filters)

        # Per-query lists are flattened into one ranked list per channel, keeping
        # each chunk's best rank across the queries that found it.
        def flatten(lists):
            best = {}
            for lst in lists:
                for rank, h in enumerate(lst, 1):
                    kid = h["rowid"]
                    if kid not in best or rank < best[kid][0]:
                        best[kid] = (rank, h)
            return [h for _, h in sorted(best.values(), key=lambda t: t[0])]

        channels = {"dense": flatten(dense_lists), "sparse": flatten(sparse_lists),
                    "entity": ent_hits}
        fused = rrf(channels, weights=rcfg.rrf_weights, k=rcfg.rrf_k,
                    limit=rcfg.rerank_candidates)

        diag = {"channels": channel_report(fused, top=20),
                "entity_ids": ent_ids, "filters": filters,
                "n_dense": len(channels["dense"]), "n_sparse": len(channels["sparse"]),
                "n_entity": len(ent_hits), "n_fused": len(fused)}

        if not fused:
            return Pack(status="GAP", queries=queries, n_candidates=0,
                        note="nothing retrieved on any channel", diagnostics=diag)

        scored, floor, mode = self._rerank_and_floor(question, fused)
        diag["rerank_backend"] = self.reranker.name
        diag["floor_mode"] = mode
        diag["n_above_floor"] = len(scored)

        kept, held = self._diversify(scored, keep)
        diag["capped_backfilled"] = len(held)

        if self.cfg.retrieval.lost_in_middle_reorder:
            kept = self._reorder_lost_in_middle(kept)

        pack = Pack(kept=kept, floor=floor, n_candidates=len(fused),
                    queries=queries, diagnostics=diag)
        pack.status, pack.note = self._assess(pack, mode)
        if explain:
            pack.diagnostics["cut"] = [
                {"source": p["source"], "trail": p.get("trail", "")[:60],
                 "rerank": round(p["score"], 4)}
                for p in [s for s in scored if s not in kept][:10]]
        return pack

    # -- floor (§3.4) ---------------------------------------------------------

    def _rerank_and_floor(self, question, fused):
        """Score with the cross-encoder, then cut. Returns (kept, floor, mode)."""
        rcfg = self.cfg.retrieval
        rr = self.reranker
        ranked = rr.score(question, fused)
        for p, s in ranked:
            p["score"] = float(s)
            p["rerank"] = float(s)
        passages = [p for p, _ in ranked]
        if not passages:
            return [], 0.0, "none"

        top = passages[0]["score"]
        floor_by = rcfg.get("rerank_floor_by_backend") or {}
        margin_by = rcfg.get("rel_margin_by_backend") or {}
        abs_floor = floor_by.get(rr.name, rcfg.rerank_floor)
        margin = margin_by.get(rr.name, rcfg.rel_margin)
        if rr.calibrated:
            # The floor the plan specifies: absolute, calibrated on the gold
            # set, plus a relative margin behind this sub-topic's own best hit.
            floor = max(abs_floor, top - margin)
            mode = "rerank-absolute" if rcfg.rerank_floor_calibrated else "rerank-provisional"
        else:
            # Uncalibrated backend: the absolute cut would be meaningless, so
            # fall back to v1's dense cosine floor on the dense channel's own
            # scores, plus the relative margin. This degrades to v1 behaviour —
            # never to "no floor".
            floor = top - margin
            mode = "relative-only (uncalibrated reranker)"
            dense_floor = 0.76
            passages = [p for p in passages
                        if p.get("scores", {}).get("dense", 1.0) >= dense_floor
                        or "dense" not in p.get("scores", {})]
        return [p for p in passages if p["score"] >= floor], float(floor), mode

    # -- diversity ------------------------------------------------------------

    def _diversify(self, hits, keep):
        """Best `keep`, but no source (or translation pair) may dominate."""
        rcfg = self.cfg.retrieval
        cap = max(rcfg.source_cap_min, int(keep * rcfg.source_cap))
        picked, held, used = [], [], collections.Counter()
        for h in hits:
            if len(picked) >= keep:
                held.append(h)
                continue
            g = self.group_of(h["source"])
            if used[g] >= cap:
                held.append(h)
                continue
            picked.append(h)
            used[g] += 1
        for h in held:                       # backfill rather than under-fill:
            if len(picked) >= keep:          # a genuinely single-source sub-topic
                break                        # should be reported, not starved
            if h not in picked:
                picked.append(h)
        picked.sort(key=lambda h: -h["score"])
        return picked, held

    @staticmethod
    def _reorder_lost_in_middle(kept):
        """Strongest passages at the head and tail, weakest in the middle (§3.7).

        Long-context attention degrades toward the middle of a prompt. Score
        order puts the second- and third-best passages exactly there. Costs
        nothing; measured in the ablation sweep like everything else.
        """
        if len(kept) < 4:
            return kept
        head, tail = [], []
        for i, h in enumerate(kept):         # kept is already score-sorted
            (head if i % 2 == 0 else tail).append(h)
        return head + list(reversed(tail))

    # -- assessment -----------------------------------------------------------

    def _assess(self, pack, mode):
        rcfg = self.cfg.retrieval
        kept = pack.kept
        if not kept:
            return "GAP", f"nothing cleared the relevance floor ({pack.floor:.3f}, {mode})"
        groups = {self.group_of(h["source"]) for h in kept}
        top = max(h["score"] for h in kept)
        if len(kept) < rcfg.thin_keep:
            return "THIN", f"only {len(kept)} passage(s) cleared the floor ({pack.floor:.3f})"
        if self.reranker.calibrated and top < rcfg.thin_score:
            return "THIN", (f"best match scores only {top:.3f} — nothing squarely "
                            f"on this sub-topic")
        if len(groups) == 1:
            return "SINGLE-SOURCE", f"all {len(kept)} passages come from {next(iter(groups))}"
        return "OK", (f"{len(kept)} passages from {len(groups)} sources, best {top:.3f}")


def main():
    from console import use_utf8
    use_utf8()
    ap = argparse.ArgumentParser(description="Query the hybrid retrieval funnel")
    ap.add_argument("query", nargs="+")
    ap.add_argument("-k", type=int, default=None)
    ap.add_argument("--kind", help="filter to primary|secondary|tertiary")
    ap.add_argument("--source", help="restrict to one source filename")
    ap.add_argument("--explain", action="store_true", help="show channels and what was cut")
    args = ap.parse_args()

    q = " ".join(args.query)
    filters = {}
    if args.kind:
        filters["kind"] = args.kind
    if args.source:
        filters["source"] = args.source

    try:
        r = Retriever()
        pack = r.subtopic([q], question=q, filters=filters or None,
                          keep=args.k, explain=args.explain)
    except KBError as e:
        print(f"ERROR: {e}"); sys.exit(1)

    print(f"status {pack.status} — {pack.note}")
    print(f"floor {pack.floor:.4f} ({pack.diagnostics.get('floor_mode')}), "
          f"{pack.n_candidates} candidates, reranker "
          f"{pack.diagnostics.get('rerank_backend')}\n")
    for h in pack.kept:
        print(f"  {h['score']:.4f}  [{h['source'][:40]}] {(h.get('trail') or '')[:44]}")
        print(f"          {h['text'][:150].replace(chr(10), ' ')}...")
    if args.explain:
        print("\nchannels (top 20):", json.dumps(pack.diagnostics["channels"]))
        print("entities:", pack.diagnostics["entity_ids"])
        if pack.diagnostics.get("cut"):
            print("\njust below the floor:")
            for c in pack.diagnostics["cut"]:
                print(f"  {c['rerank']:.4f}  [{c['source'][:38]}] {c['trail']}")


if __name__ == "__main__":
    main()
