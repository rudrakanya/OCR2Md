"""Hybrid retrieval: dense + BM25, fused with Reciprocal Rank Fusion (§9).

Why hybrid, concretely: this corpus turns on proper nouns and technical terms
that a dense encoder blurs — "Udayeśvara" vs "Udayapura", "Bhūmija" vs
"Nāgara", the name of one inscription among many. Lexical search catches the
exact string; dense search catches the paraphrase. RRF combines them without
needing the two score scales to be comparable, which they are not.
"""
from __future__ import annotations

import math
import pickle
from dataclasses import dataclass, field
from pathlib import Path

from . import settings as st
from .store import Store
from .textutil import fold, tokenize_folded


@dataclass
class Hit:
    chunk_id: str
    text: str
    metadata: dict
    dense_rank: int | None = None
    dense_score: float | None = None
    lexical_rank: int | None = None
    lexical_score: float | None = None
    fused: float = 0.0
    channels: list[str] = field(default_factory=list)

    @property
    def book(self) -> str:
        return self.metadata.get("book_title", "?")

    @property
    def heading(self) -> str:
        return self.metadata.get("heading_path", "") or "(no heading)"


class LexicalIndex:
    """BM25 over the folded text held in the sidecar (§5, §9).

    Built lazily and cached to disk: rebuilding over ~4,500 chunks takes a
    couple of seconds, which is fine once but not on every query.
    """

    def __init__(self, store: Store):
        self.store = store
        self.cache_path = Path(store.sidecar_path).with_suffix(".bm25.pkl")
        self.ids: list[str] = []
        self.bm25 = None

    def build(self, force: bool = False):
        from rank_bm25 import BM25Okapi

        ids, folded = self.store.folded_corpus()
        if not ids:
            raise RuntimeError("sidecar index is empty — run ingest first")
        stamp = (len(ids), ids[0], ids[-1])
        if not force and self.cache_path.exists():
            try:
                with self.cache_path.open("rb") as fh:
                    cached = pickle.load(fh)
                if cached.get("stamp") == stamp:
                    self.ids, self.bm25 = cached["ids"], cached["bm25"]
                    return self
            except Exception:
                pass  # a stale or truncated cache is rebuilt, not fatal
        corpus = [tokenize_folded(t) for t in folded]
        self.ids, self.bm25 = ids, BM25Okapi(corpus)
        with self.cache_path.open("wb") as fh:
            pickle.dump({"stamp": stamp, "ids": self.ids, "bm25": self.bm25}, fh)
        return self

    def search(self, query: str, k: int, allowed: set[str] | None = None
               ) -> list[tuple[str, float]]:
        if self.bm25 is None:
            self.build()
        tokens = tokenize_folded(query)
        if not tokens:
            return []
        scores = self.bm25.get_scores(tokens)
        pairs = [(cid, float(s)) for cid, s in zip(self.ids, scores) if s > 0]
        if allowed is not None:
            pairs = [p for p in pairs if p[0] in allowed]
        pairs.sort(key=lambda p: -p[1])
        return pairs[:k]


def rrf(rank: int, k: int) -> float:
    return 1.0 / (k + rank)


class Retriever:
    def __init__(self, cfg, store: Store | None = None, embedder=None):
        self.cfg = cfg
        self.store = store or Store(cfg, create=False)
        self._embedder = embedder
        self._lex: LexicalIndex | None = None

    @property
    def embedder(self):
        if self._embedder is None:
            from .embedder import get_embedder
            self._embedder = get_embedder(self.cfg)
        return self._embedder

    @property
    def lexical(self) -> LexicalIndex:
        if self._lex is None:
            self._lex = LexicalIndex(self.store).build()
        return self._lex

    def search(self, query: str, *, k: int | None = None, chapter: str | None = None,
               hybrid: bool | None = None, include_duplicates: bool = False
               ) -> list[Hit]:
        r = self.cfg["retrieval"]
        k = k or int(r.get("k", 10))
        depth = int(r.get("candidates_per_channel", 50))
        hybrid = r["hybrid"].get("enabled", True) if hybrid is None else hybrid

        where: dict | None = None
        if chapter:
            self._validate_chapter(chapter)
            where = {st.chapter_field(chapter): True}

        qvec = self.embedder.embed_queries([query])[0]
        dense = self.store.query(qvec, depth, where=where)

        pool: dict[str, Hit] = {}
        for i, d in enumerate(dense):
            pool[d["chunk_id"]] = Hit(
                chunk_id=d["chunk_id"], text=d["document"], metadata=d["metadata"],
                dense_rank=i + 1, dense_score=d["score"], channels=["dense"])

        if hybrid:
            # The lexical channel has no `where` clause of its own, so when a
            # chapter filter is active we restrict it to that chapter's ids —
            # otherwise --chapter would silently stop filtering half the funnel.
            allowed: set[str] | None = None
            if chapter:
                got = self.store.collection.get(where=where, include=[])
                allowed = set(got["ids"])
            for i, (cid, score) in enumerate(self.lexical.search(query, depth, allowed)):
                hit = pool.get(cid)
                if hit is None:
                    row = self.store.sidecar_row(cid)
                    if row is None:
                        continue
                    got = self.store.collection.get(ids=[cid], include=["metadatas"])
                    meta = (got["metadatas"] or [{}])[0] or {}
                    hit = Hit(chunk_id=cid, text=row["text"], metadata=meta,
                              channels=[])
                    pool[cid] = hit
                hit.lexical_rank = i + 1
                hit.lexical_score = score
                hit.channels.append("lexical")

        rrf_k = int(r["hybrid"].get("rrf_k", 60))
        w_dense = float(r["hybrid"].get("weight_dense", 1.0))
        w_lex = float(r["hybrid"].get("weight_lexical", 1.0))
        for hit in pool.values():
            total = 0.0
            if hit.dense_rank:
                total += w_dense * rrf(hit.dense_rank, rrf_k)
            if hit.lexical_rank:
                total += w_lex * rrf(hit.lexical_rank, rrf_k)
            # A flagged near-duplicate is demoted, not dropped: its twin is
            # already in the pool, and two copies of one passage should not
            # occupy two of your k slots.
            if hit.metadata.get("is_duplicate") and not include_duplicates:
                total *= 0.5
            hit.fused = total

        ranked = sorted(pool.values(), key=lambda h: -h.fused)
        return ranked[:k]

    def _validate_chapter(self, chapter: str) -> None:
        valid = {c["id"] for c in st.load_chapters(self.cfg)}
        if chapter not in valid:
            raise ValueError(
                f"unknown chapter {chapter!r}; valid ids: {', '.join(sorted(valid))}"
            )


def ndcg(relevances: list[float], k: int) -> float:
    def dcg(rs: list[float]) -> float:
        return sum(r / math.log2(i + 2) for i, r in enumerate(rs[:k]))
    ideal = dcg(sorted(relevances, reverse=True))
    return dcg(relevances) / ideal if ideal > 0 else 0.0
