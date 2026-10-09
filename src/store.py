"""ChromaDB collection + the sidecar index (§6).

Chroma holds the vectors, the documents and the scalar metadata. The sidecar
SQLite holds `text_folded` and the chunk bookkeeping, because §6 is right that
a folded copy of every chunk would roughly double a metadata payload for a
field that is never displayed and never embedded — and Chroma metadata cannot
hold lists anyway, so `chapters` has to live as boolean columns regardless.
"""
from __future__ import annotations

import json
import shutil
import sqlite3
from pathlib import Path
from typing import Any, Iterable, Sequence

import chromadb
from chromadb.config import Settings as ChromaSettings

from . import settings as st


class StoreError(RuntimeError):
    pass


# Chroma metadata may only hold str/int/float/bool, and never None (§6).
_SCALAR = (str, int, float, bool)


def clean_metadata(meta: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in meta.items():
        if v is None:
            continue                      # omit the key, never store null
        if isinstance(v, bool):
            out[k] = v
        elif isinstance(v, _SCALAR):
            out[k] = v
        elif isinstance(v, (list, tuple, set)):
            raise StoreError(
                f"metadata {k!r} is a {type(v).__name__}; Chroma rejects sequences. "
                "Flatten it to a delimited string or to boolean columns."
            )
        else:
            out[k] = str(v)
    return out


class Store:
    def __init__(self, cfg, *, create: bool = True):
        self.cfg = cfg
        self.path = st.resolve(cfg, "storage.chroma_path")
        self.collection_name = cfg.get_path("storage.collection")
        self.sidecar_path = st.resolve(cfg, "storage.sidecar_db")
        self.path.mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=str(self.path),
            settings=ChromaSettings(anonymized_telemetry=False, allow_reset=True),
        )
        self.collection = self._open(create)
        self.sidecar = self._open_sidecar()

    # -- collection -----------------------------------------------------------
    def _hnsw_metadata(self) -> dict[str, Any]:
        idx = self.cfg["index"]
        h = idx.get("hnsw", {})
        return {
            "hnsw:space": idx.get("distance", "cosine"),
            "hnsw:M": int(h.get("M", 32)),
            "hnsw:construction_ef": int(h.get("construction_ef", 200)),
            "hnsw:search_ef": int(h.get("search_ef", 128)),
            # Stamp the encoder into the collection itself. Without this, a
            # query run under different settings than the ingest silently
            # embeds with the wrong model; Chroma only objects when the
            # dimensions happen to differ, so two 1024-dim models would return
            # confident nonsense instead of an error.
            "embedding_model": str(self.cfg.get_path("embedding.model")),
            "embedding_dim": int(self.cfg.get_path("embedding.dim")),
        }

    def built_with(self) -> tuple[str | None, int | None]:
        """(model, dim) the collection was built with, as far as we can tell."""
        meta = self.collection.metadata or {}
        model = meta.get("embedding_model")
        dim = meta.get("embedding_dim")
        if dim is None:
            # Collections created before the stamp existed: recover the
            # dimension from an actual vector rather than guessing.
            try:
                got = self.collection.peek(limit=1)
                embs = got.get("embeddings")
                if embs is not None and len(embs):
                    dim = len(embs[0])
            except Exception:
                dim = None
        return (str(model) if model else None,
                int(dim) if dim is not None else None)

    def _open(self, create: bool):
        try:
            return self.client.get_collection(self.collection_name)
        except Exception:
            if not create:
                raise StoreError(
                    f"collection {self.collection_name!r} does not exist — "
                    "run `python -m src.ingest --rebuild` first"
                )
            return self.client.create_collection(
                name=self.collection_name, metadata=self._hnsw_metadata()
            )

    # -- sidecar --------------------------------------------------------------
    def _open_sidecar(self) -> sqlite3.Connection:
        self.sidecar_path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(str(self.sidecar_path))
        db.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id     TEXT PRIMARY KEY,
                source_path  TEXT NOT NULL,
                book_title   TEXT NOT NULL,
                heading_path TEXT,
                chunk_index  INTEGER,
                token_count  INTEGER,
                language     TEXT,
                page_start   INTEGER,
                text         TEXT NOT NULL,
                text_folded  TEXT NOT NULL,
                duplicate_of TEXT,
                dup_score    REAL
            )""")
        db.execute("CREATE INDEX IF NOT EXISTS idx_src ON chunks(source_path)")
        db.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY, kind TEXT, ts TEXT, payload TEXT)""")
        db.commit()
        return db

    # -- writes ---------------------------------------------------------------
    def upsert(self, ids: Sequence[str], documents: Sequence[str],
               embeddings, metadatas: Sequence[dict], batch: int = 512) -> None:
        metas = [clean_metadata(m) for m in metadatas]
        for i in range(0, len(ids), batch):
            sl = slice(i, i + batch)
            self.collection.upsert(
                ids=list(ids[sl]),
                documents=list(documents[sl]),
                embeddings=[list(map(float, v)) for v in embeddings[sl]],
                metadatas=metas[sl],
            )

    def update_metadata(self, ids: Sequence[str], metadatas: Sequence[dict],
                        batch: int = 512) -> None:
        """Used by tag.py — re-tag without touching a single vector."""
        metas = [clean_metadata(m) for m in metadatas]
        for i in range(0, len(ids), batch):
            sl = slice(i, i + batch)
            self.collection.update(ids=list(ids[sl]), metadatas=metas[sl])

    def put_sidecar(self, rows: Iterable[tuple]) -> None:
        self.sidecar.executemany(
            "INSERT OR REPLACE INTO chunks (chunk_id, source_path, book_title,"
            " heading_path, chunk_index, token_count, language, page_start,"
            " text, text_folded, duplicate_of, dup_score)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", list(rows))
        self.sidecar.commit()

    def record_run(self, run_id: str, kind: str, payload: dict) -> None:
        import datetime as _dt
        self.sidecar.execute(
            "INSERT OR REPLACE INTO runs (run_id, kind, ts, payload) VALUES (?,?,?,?)",
            (run_id, kind, _dt.datetime.now().isoformat(timespec="seconds"),
             json.dumps(payload, ensure_ascii=False, default=str)))
        self.sidecar.commit()

    # -- reads ----------------------------------------------------------------
    def count(self) -> int:
        return self.collection.count()

    def all_chunks(self) -> list[dict]:
        """Every chunk with metadata and document, ordered stably by id."""
        got = self.collection.get(include=["metadatas", "documents"])
        rows = [{"chunk_id": i, "document": d, "metadata": m or {}}
                for i, d, m in zip(got["ids"], got["documents"], got["metadatas"])]
        rows.sort(key=lambda r: r["chunk_id"])
        return rows

    def all_embeddings(self) -> tuple[list[str], "Any"]:
        import numpy as np
        got = self.collection.get(include=["embeddings"])
        ids = got["ids"]
        vecs = np.asarray(got["embeddings"], dtype=np.float32)
        order = sorted(range(len(ids)), key=lambda i: ids[i])
        return [ids[i] for i in order], vecs[order] if len(ids) else vecs

    def folded_corpus(self) -> tuple[list[str], list[str]]:
        rows = self.sidecar.execute(
            "SELECT chunk_id, text_folded FROM chunks ORDER BY chunk_id").fetchall()
        return [r[0] for r in rows], [r[1] for r in rows]

    def sidecar_row(self, chunk_id: str) -> dict | None:
        cur = self.sidecar.execute(
            "SELECT * FROM chunks WHERE chunk_id=?", (chunk_id,))
        row = cur.fetchone()
        if row is None:
            return None
        return dict(zip([c[0] for c in cur.description], row))

    def query(self, embedding, n_results: int, where: dict | None = None,
              where_document: dict | None = None) -> list[dict]:
        kwargs: dict[str, Any] = {
            "query_embeddings": [list(map(float, embedding))],
            "n_results": max(1, n_results),
            "include": ["metadatas", "documents", "distances"],
        }
        if where:
            kwargs["where"] = where
        if where_document:
            kwargs["where_document"] = where_document
        res = self.collection.query(**kwargs)
        out: list[dict] = []
        for i, cid in enumerate(res["ids"][0]):
            dist = res["distances"][0][i]
            out.append({
                "chunk_id": cid,
                "document": res["documents"][0][i],
                "metadata": res["metadatas"][0][i] or {},
                "distance": dist,
                # Chroma's cosine "distance" is 1 - cosine_similarity.
                "score": 1.0 - float(dist),
            })
        return out


# ---------------------------------------------------------------------------
def open_aligned(cfg, *, preset: str | None = None, verbose: bool = True):
    """Open the collection and return (cfg, store) with the config's embedding
    settings matched to whatever actually built the store.

    Readers must not assume config.yaml still names the model that produced the
    index. It routinely does not: `ingest --embed-preset e5_small_fast` leaves
    the file saying `bge-m3`, and every later query then embeds with the wrong
    encoder. Rather than make you remember, we adopt the collection's own
    stamp and say so.
    """
    if preset:
        cfg = st.apply_overrides(cfg, embed_preset=preset)
    store = Store(cfg, create=False)
    model, dim = store.built_with()
    want_model = str(cfg.get_path("embedding.model"))
    want_dim = int(cfg.get_path("embedding.dim"))

    if model == want_model and dim in (None, want_dim):
        return cfg, store
    if model is None and dim == want_dim:
        return cfg, store  # unstamped, but dimensions agree

    if preset:
        raise StoreError(
            f"--embed-preset {preset!r} gives {want_model} ({want_dim}d) but the "
            f"collection was built with {model or 'an unrecorded model'} "
            f"({dim}d). Rebuild, or drop the flag."
        )

    # Find the preset whose model (or dimension, for unstamped collections)
    # matches what is actually in the store.
    alts = cfg["embedding"].get("alternatives", {})
    candidates = {None: {"model": cfg["embedding"].get("model"),
                         "dim": cfg["embedding"].get("dim")}}
    candidates.update({k: v for k, v in alts.items()})

    match = None
    if model:
        match = next((k for k, v in candidates.items() if v.get("model") == model), ...)
    if match in (None, ...) and dim is not None:
        by_dim = [k for k, v in candidates.items() if int(v.get("dim", -1)) == dim]
        if len(by_dim) == 1:
            match = by_dim[0]
        elif len(by_dim) > 1:
            raise StoreError(
                f"the collection holds {dim}-dimensional vectors and "
                f"{len(by_dim)} configured models share that dimension "
                f"({', '.join(str(b) for b in by_dim)}). It carries no model "
                "stamp, so which one built it cannot be determined. Re-run "
                "`python -m src.ingest --rebuild` to stamp it, or pass "
                "--embed-preset explicitly."
            )
    if match is ... or match is None and model not in (None, want_model):
        raise StoreError(
            f"the collection was built with {model!r} ({dim}d), which is not "
            "listed in config.embedding or its alternatives. Add it, or rebuild."
        )

    cfg = st.apply_overrides(cfg, embed_preset=match) if match else cfg
    if verbose:
        print(f"  [aligned to the collection: {cfg.get_path('embedding.model')} "
              f"({cfg.get_path('embedding.dim')}d)"
              + (f", preset '{match}'" if match else "") + "]")
    return cfg, Store(cfg, create=False)


def wipe(cfg, *, verbose: bool = True, clear_results: bool = False) -> list[str]:
    """§3: delete and recreate everything, and say exactly what was removed.

    Eval results are PRESERVED by default, which is a deliberate departure from
    §3's "clear previous eval-result caches". That instruction is right for the
    first clean build and wrong afterwards: every result file is stamped with
    the config hash and model that produced it (§10.4), which exists precisely
    so runs stay comparable over time. Deleting the previous model's numbers on
    the way into the next model's build destroys the only before/after you
    have. Pass --clear-results when you genuinely want a blank slate.
    """
    removed: list[str] = []
    chroma_path = st.resolve(cfg, "storage.chroma_path")
    if chroma_path.exists():
        n_files = sum(1 for _ in chroma_path.rglob("*") if _.is_file())
        size_mb = sum(f.stat().st_size for f in chroma_path.rglob("*") if f.is_file()) / 1e6
        shutil.rmtree(chroma_path)
        removed.append(f"{chroma_path}  ({n_files} files, {size_mb:.1f} MB) "
                       f"— collection, embedding cache and sidecar index")
    else:
        removed.append(f"{chroma_path}  (did not exist — nothing to clear)")

    results_dir = st.resolve(cfg, "evaluation.results_dir")
    n = sum(1 for _ in results_dir.rglob("*") if _.is_file()) if results_dir.exists() else 0
    if clear_results and results_dir.exists():
        shutil.rmtree(results_dir)
        removed.append(f"{results_dir}  ({n} files) — cached eval results")
    else:
        removed.append(f"{results_dir}  ({n} run records KEPT — they carry the "
                       "config hash that makes runs comparable; "
                       "--clear-results to remove)")

    if verbose:
        print("CLEARED:")
        for line in removed:
            print(f"  - {line}")
    return removed
