"""In-memory retrieval engine for the drafting evidence map (read-only on chroma_db).

One read of the collection (embeddings + metadata + documents), one BM25 build,
one batched embedding call for every query. Scoring is matrix arithmetic:

  dense  = Q x N cosine (normalised vectors)
  lex    = Q x N BM25 (rank_bm25 over the sidecar's folded text, same tokenizer)
  fused  = w_d / (rrf_k + dense_rank) + w_l / (rrf_k + lex_rank)   (src/retrieval.py)
           x 0.5 when the chunk is a flagged near-duplicate         (src/retrieval.py)

Ranks are computed over the whole collection (global) or within one book's
chunks (per-book sweep = boolean mask over the same matrices), so per-book
sweeps need no extra queries. Lexical ranks only count chunks with BM25 > 0,
as in LexicalIndex.search. Nothing is written under chroma_db/: the snapshot
lives in drafting/_tools/corpus_snapshot.npz, query vectors in
drafting/_tools/query_cache.sqlite3.
"""
from __future__ import annotations

import json
import os
import pickle
import sqlite3
import sys
from pathlib import Path

import numpy as np

ROOT = Path(str(Path(__file__).resolve().parents[2]))
TOOLS = ROOT / "drafting" / "_tools"
RUNS = ROOT / "drafting" / "_runs"
COLLECTION = "udaypur_corpus_openai_large"
SNAP = TOOLS / "corpus_snapshot.npz"
META = TOOLS / "corpus_meta.pkl"
RRF_K, W_D, W_L = 60, 1.0, 1.0  # config.yaml retrieval.hybrid, asserted at load


def _cfg():
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT))
    os.environ["COLLECTION"] = COLLECTION
    from src import settings as st
    from src.store import open_aligned
    cfg = st.load()
    assert cfg["storage"]["collection"] == COLLECTION
    cfg["embedding"]["cache_path"] = str(TOOLS / "query_cache.sqlite3")
    cfg, store = open_aligned(cfg, verbose=False)
    cfg["embedding"]["cache_path"] = str(TOOLS / "query_cache.sqlite3")
    h = cfg["retrieval"]["hybrid"]
    assert (int(h["rrf_k"]), float(h["weight_dense"]), float(h["weight_lexical"])) == (RRF_K, W_D, W_L)
    return cfg, store


def _cfg_ro():
    """Config aligned to the collection's embedding stamp WITHOUT opening the Chroma client.
    Opening chromadb.PersistentClient rewrites chroma.sqlite3's bookkeeping (its mtime moved on every KB step,
    content unchanged); query embedding only needs the model stamp, read here over a read-only SQLite URI."""
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT))
    os.environ["COLLECTION"] = COLLECTION
    from src import settings as st
    cfg = st.load()
    assert cfg["storage"]["collection"] == COLLECTION
    db = sqlite3.connect(f"file:{ROOT / 'chroma_db' / 'chroma.sqlite3'}?mode=ro", uri=True)
    try:
        cid = db.execute("select id from collections where name = ?", (COLLECTION,)).fetchone()[0]
        meta = dict((k, s if s is not None else i) for k, s, i in
                    db.execute("select key, str_value, int_value from collection_metadata where collection_id = ?", (cid,)))
    finally:
        db.close()
    model, dim = meta.get("embedding_model"), meta.get("embedding_dim")
    if not (cfg["embedding"].get("model") == model and int(cfg["embedding"].get("dim") or 0) == int(dim or 0)):
        match = next((k for k, v in cfg["embedding"].get("alternatives", {}).items() if v.get("model") == model), None)
        assert match, f"collection stamped {model} ({dim}d) is not in config.embedding or its alternatives"
        cfg = st.apply_overrides(cfg, embed_preset=match)
    assert cfg.get_path("embedding.model") == model and int(cfg.get_path("embedding.dim")) == int(dim)
    cfg["embedding"]["cache_path"] = str(TOOLS / "query_cache.sqlite3")
    h = cfg["retrieval"]["hybrid"]
    assert (int(h["rrf_k"]), float(h["weight_dense"]), float(h["weight_lexical"])) == (RRF_K, W_D, W_L)
    return cfg


class Corpus:
    def __init__(self):
        if SNAP.exists() and META.exists():
            z = np.load(SNAP)
            self.E = z["E"]
            with META.open("rb") as fh:
                m = pickle.load(fh)
        else:
            cfg, store = _cfg()
            got = store.collection.get(include=["embeddings", "metadatas", "documents"])
            order = sorted(range(len(got["ids"])), key=lambda i: got["ids"][i])
            E = np.asarray(got["embeddings"], dtype=np.float32)[order]
            E /= np.clip(np.linalg.norm(E, axis=1, keepdims=True), 1e-12, None)
            ids = [got["ids"][i] for i in order]
            db = sqlite3.connect(f"file:{ROOT / 'chroma_db' / 'sidecar.sqlite3'}?mode=ro", uri=True)
            side = {r[0]: (r[1], r[2]) for r in db.execute("select chunk_id, text, text_folded from chunks")}
            m = {"ids": ids,
                 "meta": [got["metadatas"][i] or {} for i in order],
                 "text": [side[c][0] for c in ids],
                 "folded": [side[c][1] for c in ids]}
            np.savez(SNAP, E=E)
            with META.open("wb") as fh:
                pickle.dump(m, fh)
            self.E = E
        self.ids, self.meta, self.text, self.folded = m["ids"], m["meta"], m["text"], m["folded"]
        self.idx = {c: i for i, c in enumerate(self.ids)}
        self.src = np.array([mm["source_path"] for mm in self.meta])
        self.books = sorted(set(self.src))
        self.dup = np.array([bool(mm.get("is_duplicate")) for mm in self.meta])
        self._bm25 = None

    # -- lexical --------------------------------------------------------------
    def bm25(self):
        if self._bm25 is None:
            sys.path.insert(0, str(ROOT))
            from rank_bm25 import BM25Okapi
            from src.textutil import tokenize_folded
            self._tok = tokenize_folded
            self._bm25 = BM25Okapi([tokenize_folded(t) for t in self.folded])
        return self._bm25

    def lex_scores(self, queries: list[str]) -> np.ndarray:
        b = self.bm25()
        out = np.zeros((len(queries), len(self.ids)), dtype=np.float32)
        for i, q in enumerate(queries):
            t = self._tok(q)
            if t:
                out[i] = b.get_scores(t)
        return out

    # -- dense ----------------------------------------------------------------
    @staticmethod
    def embed(queries: list[str]) -> np.ndarray:
        cfg = _cfg_ro()
        cfg["embedding"]["batch_size"] = 2048
        from src.embedder import get_embedder
        emb = get_embedder(cfg)
        assert str(emb.cache.path).startswith(str(TOOLS))
        return emb.embed_queries(queries)


def ranks_desc(scores: np.ndarray, valid: np.ndarray | None = None) -> np.ndarray:
    """1-based rank of each column per row (descending); 0 where not valid."""
    order = np.argsort(-scores, axis=1, kind="stable")
    r = np.empty_like(order)
    rows = np.arange(scores.shape[0])[:, None]
    r[rows, order] = np.arange(1, scores.shape[1] + 1)[None, :]
    if valid is not None:
        # rank among valid entries only
        v = valid.astype(np.int64)
        vs = np.take_along_axis(v, order, axis=1).cumsum(axis=1)
        rv = np.empty_like(order)
        rv[rows, order] = vs
        r = np.where(valid, rv, 0)
    return r


def fuse(D: np.ndarray, L: np.ndarray, dup: np.ndarray, mask: np.ndarray | None = None) -> np.ndarray:
    """RRF fused scores over the columns selected by mask (others = -inf)."""
    if mask is not None:
        D = np.where(mask[None, :], D, -np.inf)
        L = np.where(mask[None, :], L, 0)
    rd = ranks_desc(D, None if mask is None else np.broadcast_to(mask, D.shape))
    rl = ranks_desc(L, L > 0)
    f = np.where(rd > 0, W_D / (RRF_K + rd), 0) + np.where(rl > 0, W_L / (RRF_K + rl), 0)
    f = np.where(dup[None, :], f * 0.5, f)
    if mask is not None:
        f = np.where(mask[None, :], f, -np.inf)
    return f.astype(np.float32)
