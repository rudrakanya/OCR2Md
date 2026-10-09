"""Embedding adapters (§8).

Switching models is three lines in config.yaml (`backend`, `model`, `dim`) plus
the optional e5-style prefixes; nothing outside this module knows which encoder
is in use.

One deliberate choice: we do NOT register a Chroma `EmbeddingFunction`. Chroma
has changed that interface across releases, and pinning to it means an upgrade
can silently alter how documents are encoded. Instead we compute vectors here
and hand them to Chroma explicitly on both `upsert` and `query`, which is the
strongest possible guarantee that ingest and retrieval share one pipeline — the
thing §8 actually asks for.
"""
from __future__ import annotations

import hashlib
import os
import sqlite3
import struct
import sys
from pathlib import Path
from typing import Sequence

import numpy as np


class EmbeddingError(RuntimeError):
    pass


# ---------------------------------------------------------------------------
# Cache: content hash -> vector. Keeps re-chunking cheap and makes an
# interrupted ingest resumable (§8: "make it resumable").
# ---------------------------------------------------------------------------
class VectorCache:
    def __init__(self, path: Path, model: str, dim: int):
        self.path, self.model, self.dim = Path(path), model, dim
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(self.path))
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS vectors ("
            " key TEXT PRIMARY KEY, model TEXT, dim INTEGER, vec BLOB)"
        )
        self.db.commit()
        self.hits = self.misses = 0

    @staticmethod
    def key(model: str, text: str) -> str:
        return hashlib.sha1(f"{model}\x00{text}".encode("utf-8")).hexdigest()

    def get_many(self, texts: Sequence[str]) -> dict[int, np.ndarray]:
        out: dict[int, np.ndarray] = {}
        keys = [self.key(self.model, t) for t in texts]
        lookup: dict[str, list[int]] = {}
        for i, k in enumerate(keys):
            lookup.setdefault(k, []).append(i)
        for batch_start in range(0, len(keys), 900):  # SQLite variable limit
            batch = list(dict.fromkeys(keys[batch_start:batch_start + 900]))
            qs = ",".join("?" * len(batch))
            rows = self.db.execute(
                f"SELECT key, vec FROM vectors WHERE model=? AND dim=? AND key IN ({qs})",
                [self.model, self.dim, *batch],
            ).fetchall()
            for k, blob in rows:
                vec = np.frombuffer(blob, dtype=np.float32)
                for i in lookup.get(k, []):
                    out[i] = vec
        self.hits += len(out)
        self.misses += len(texts) - len(out)
        return out

    def put_many(self, texts: Sequence[str], vecs: np.ndarray) -> None:
        rows = [(self.key(self.model, t), self.model, self.dim,
                 np.asarray(v, dtype=np.float32).tobytes())
                for t, v in zip(texts, vecs)]
        self.db.executemany(
            "INSERT OR REPLACE INTO vectors (key, model, dim, vec) VALUES (?,?,?,?)",
            rows,
        )
        self.db.commit()

    def clear(self) -> int:
        n = self.db.execute("SELECT COUNT(*) FROM vectors").fetchone()[0]
        self.db.execute("DELETE FROM vectors")
        self.db.commit()
        return n


# ---------------------------------------------------------------------------
class Embedder:
    name = "base"

    def __init__(self, cfg):
        e = cfg["embedding"]
        self.model_name = e["model"]
        self.dim = int(e["dim"])
        self.normalize = bool(e.get("normalize", True))
        self.batch_size = int(e.get("batch_size", 16))
        self.query_prefix = e.get("query_prefix", "") or ""
        self.passage_prefix = e.get("passage_prefix", "") or ""
        cache_path = e.get("cache_path")
        self.cache = (VectorCache(Path(cache_path), self.model_name, self.dim)
                      if cache_path else None)

    # -- subclasses implement -------------------------------------------------
    def _encode(self, texts: Sequence[str]) -> np.ndarray:
        raise NotImplementedError

    def token_len(self, text: str) -> int:
        raise NotImplementedError

    # -- shared ---------------------------------------------------------------
    def _finish(self, vecs: np.ndarray) -> np.ndarray:
        vecs = np.asarray(vecs, dtype=np.float32)
        if vecs.ndim == 1:
            vecs = vecs.reshape(1, -1)
        if vecs.shape[1] != self.dim:
            raise EmbeddingError(
                f"{self.model_name} returned dim {vecs.shape[1]}, config says {self.dim}. "
                "Fix `embedding.dim` in config.yaml — a mismatch corrupts the index."
            )
        if self.normalize:
            norms = np.linalg.norm(vecs, axis=1, keepdims=True)
            vecs = vecs / np.clip(norms, 1e-12, None)
        return vecs

    def embed(self, texts: Sequence[str], *, prefix: str = "",
              use_cache: bool = True, progress: bool = False) -> np.ndarray:
        if not texts:
            return np.zeros((0, self.dim), dtype=np.float32)
        keyed = [prefix + t for t in texts]
        out = np.zeros((len(texts), self.dim), dtype=np.float32)

        cached: dict[int, np.ndarray] = {}
        if use_cache and self.cache is not None:
            cached = self.cache.get_many(keyed)
            for i, v in cached.items():
                out[i] = v

        todo = [i for i in range(len(texts)) if i not in cached]
        if todo:
            done = 0
            for start in range(0, len(todo), self.batch_size):
                idx = todo[start:start + self.batch_size]
                vecs = self._finish(self._encode([keyed[i] for i in idx]))
                for j, i in enumerate(idx):
                    out[i] = vecs[j]
                if use_cache and self.cache is not None:
                    self.cache.put_many([keyed[i] for i in idx], vecs)
                done += len(idx)
                if progress:
                    _bar(done, len(todo), f"embed[{self.name}]")
            if progress:
                sys.stderr.write("\n")
        elif progress:
            sys.stderr.write(f"  embed: all {len(texts)} vectors served from cache\n")
        return out

    def embed_passages(self, texts: Sequence[str], progress: bool = False) -> np.ndarray:
        return self.embed(texts, prefix=self.passage_prefix, progress=progress)

    def embed_queries(self, texts: Sequence[str]) -> np.ndarray:
        return self.embed(texts, prefix=self.query_prefix)


class SentenceTransformersEmbedder(Embedder):
    name = "sentence_transformers"

    def __init__(self, cfg):
        super().__init__(cfg)
        from sentence_transformers import SentenceTransformer
        threads = cfg["embedding"].get("torch_threads")
        if threads:
            import torch
            torch.set_num_threads(int(threads))
        device = cfg["embedding"].get("device", "auto")
        if device == "auto":
            try:
                import torch
                device = "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                device = "cpu"
        self.device = device
        self.model = SentenceTransformer(self.model_name, device=device)
        max_seq = cfg["embedding"].get("max_seq_length")
        if max_seq:
            self.model.max_seq_length = int(max_seq)
        self._tok = self.model.tokenizer

    def _encode(self, texts: Sequence[str]) -> np.ndarray:
        return self.model.encode(list(texts), batch_size=len(texts),
                                 show_progress_bar=False,
                                 convert_to_numpy=True,
                                 normalize_embeddings=False)

    def token_len(self, text: str) -> int:
        if not text:
            return 0
        return len(self._tok(text, add_special_tokens=False)["input_ids"])


class OpenAIEmbedder(Embedder):
    name = "openai"

    def __init__(self, cfg):
        super().__init__(cfg)
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise EmbeddingError("pip install openai to use the openai backend") from exc
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            raise EmbeddingError("OPENAI_API_KEY is not set")
        self.client = OpenAI(api_key=key)
        try:
            import tiktoken
            self._enc = tiktoken.get_encoding("cl100k_base")
        except ImportError:
            self._enc = None

    def _encode(self, texts: Sequence[str]) -> np.ndarray:
        resp = self.client.embeddings.create(model=self.model_name, input=list(texts))
        return np.array([d.embedding for d in resp.data], dtype=np.float32)

    def token_len(self, text: str) -> int:
        if self._enc is not None:
            return len(self._enc.encode(text))
        return max(1, len(text) // 4)  # crude, but only used for chunk sizing


_BACKENDS = {
    "sentence_transformers": SentenceTransformersEmbedder,
    "openai": OpenAIEmbedder,
}


def get_embedder(cfg) -> Embedder:
    backend = cfg["embedding"].get("backend", "sentence_transformers")
    if backend not in _BACKENDS:
        raise EmbeddingError(
            f"unknown embedding backend {backend!r}; available: {sorted(_BACKENDS)}"
        )
    return _BACKENDS[backend](cfg)


def _bar(done: int, total: int, label: str, width: int = 32) -> None:
    frac = done / max(1, total)
    filled = int(width * frac)
    sys.stderr.write(
        f"\r  {label} [{'█' * filled}{'·' * (width - filled)}] {done}/{total} ({frac:5.1%})"
    )
    sys.stderr.flush()
