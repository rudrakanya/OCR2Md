#!/usr/bin/env python
"""Embed the v2 store. Two backends, one collection each, never mixed.

    python phase4_embed_v2.py --backend openai --plan
    python phase4_embed_v2.py --backend openai --run
    python phase4_embed_v2.py --backend local  --run

    openai -> text-embedding-3-large at 1536 dimensions -> udaypur_kb_v2_openai
    local  -> intfloat/multilingual-e5-small (384)      -> udaypur_kb_v2

A Chroma collection holds exactly one vector space. Mixing two embedding models
in one collection makes every distance meaningless, so each backend gets its own
collection and the v1 collection (udaypur_kb) is never touched.

MEMORY. This machine has roughly 3 GB free and long jobs get reaped. An earlier
version pulled all 14,647 v1 vectors back through Chroma as Python lists to
reuse 356 of them and reached 4.3 GB before being killed. The reuse is not worth
it: vectors are held here as one float32 array (10,620 x 1536 = 65 MB) and
everything is embedded fresh.

RESUMABLE. Vectors are checkpointed to kb3/vectors_v2_<backend>.npz after every
few batches. A re-run loads the checkpoint and embeds only what is still
missing, so a reap costs minutes, not the whole job.

THE KEY is read from .env and used only to call the embeddings endpoint. It is
never printed, logged, or written to any output file.
"""
from __future__ import annotations

import argparse
import collections
import os
import random
import sqlite3
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
K3 = ROOT / "kb3"
V2 = K3 / "kb_active_v2.sqlite"
V2Q = K3 / "kb_quarantine_v2.sqlite"
CHROMA = K3 / "chroma"

BACKENDS = {
    "openai": {"model": "text-embedding-3-large", "dim": 1536,
               "active": "udaypur_kb_v2_openai", "archive": "udaypur_kb_v2_openai_archive"},
    "local": {"model": "intfloat/multilingual-e5-small", "dim": 384,
              "active": "udaypur_kb_v2", "archive": "udaypur_kb_v2_archive"},
}


def load_key():
    k = os.environ.get("OPENAI_API_KEY", "").strip()
    if len(k) > 20:
        return k
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8", errors="replace").split("\n"):
            line = line.strip()
            if line.startswith("OPENAI_API_KEY"):
                v = line.split("=", 1)[-1].strip().strip('"').strip("'")
                if len(v) > 20:
                    return v
    raise SystemExit("OPENAI_API_KEY not found in environment or .env")


def all_texts():
    """content_hash -> text, over the active and quarantine v2 stores."""
    out = {}
    for p in (V2, V2Q):
        db = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
        for h, t in db.execute("select content_hash, text from chunks"):
            if t and t.strip():
                out.setdefault(h, t)
        db.close()
    return out


def load_ckpt(path, dim):
    if not path.exists():
        return {}
    try:
        z = np.load(path, allow_pickle=True)
        hs, V = list(z["hashes"]), z["V"]
        if V.shape[1] != dim:
            print(f"  checkpoint has dim {V.shape[1]}, need {dim}; ignoring it")
            return {}
        return {h: V[i] for i, h in enumerate(hs)}
    except Exception as e:
        print(f"  checkpoint unreadable ({e}); starting fresh")
        return {}


def save_ckpt(path, vecs, dim):
    if not vecs:
        return
    hs = list(vecs)
    V = np.zeros((len(hs), dim), dtype=np.float32)
    for i, h in enumerate(hs):
        V[i] = vecs[h]
    tmp = path.with_suffix(".tmp.npz")
    np.savez(tmp, hashes=np.array(hs, dtype=object), V=V)
    tmp.replace(path)


class TokenLimiter:
    """Sliding-window tokens-per-minute budget.

    The org limit is 1,000,000 TPM for this model. Eight workers x 128 texts put
    roughly 450k tokens in flight per wave and completed fast enough to breach it,
    so the first run died on a 429 after exhausting its retries. Pacing against a
    measured budget is better than retrying into a wall: requests wait only as
    long as the window actually requires.
    """

    def __init__(self, budget_per_min):
        self.budget = budget_per_min
        self.events = collections.deque()   # (when, tokens)
        self.lock = threading.Lock()

    def acquire(self, tokens):
        while True:
            with self.lock:
                now = time.time()
                while self.events and now - self.events[0][0] > 60:
                    self.events.popleft()
                used = sum(t for _, t in self.events)
                if used + tokens <= self.budget or not self.events:
                    self.events.append((now, tokens))
                    return
                wait = 60 - (now - self.events[0][0]) + 0.05
            time.sleep(max(0.05, min(wait, 5)))


def token_counts(hashes, texts):
    """Exact token counts where tiktoken is available, else a measured ratio."""
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return {h: len(enc.encode(texts[h])) for h in hashes}
    except Exception:
        # 0.363 tokens/char, measured on a 1,200-text sample of this corpus
        return {h: int(len(texts[h]) * 0.363) + 1 for h in hashes}


def embed_openai(todo, texts, cfg, ckpt, vecs, batch, workers, tpm=820_000):
    """Batched, concurrent, paced under the TPM budget. Returns wall time."""
    from openai import OpenAI
    client = OpenAI(api_key=load_key(), max_retries=0)
    model, dim = cfg["model"], cfg["dim"]

    tks = token_counts(todo, texts)
    # batches capped by BOTH text count and tokens: one request must stay well
    # inside the per-request ceiling as well as the per-minute one
    batches, cur, cur_tok = [], [], 0
    for h in todo:
        t = tks[h]
        if cur and (len(cur) >= batch or cur_tok + t > 120_000):
            batches.append((cur, cur_tok)); cur, cur_tok = [], 0
        cur.append(h); cur_tok += t
    if cur:
        batches.append((cur, cur_tok))
    print(f"  {len(batches)} requests | {sum(t for _, t in batches):,} tokens | "
          f"paced at {tpm:,} tokens/min, {workers} concurrent")

    limiter = TokenLimiter(tpm)
    lock = threading.Lock()
    done = [0]
    t0 = time.time()

    def work(bt, ntok):
        for attempt in range(9):
            limiter.acquire(ntok)
            try:
                r = client.embeddings.create(model=model, input=[texts[h] for h in bt],
                                             dimensions=dim)
                return bt, [d.embedding for d in r.data]
            except Exception as e:
                if attempt == 8:
                    raise
                wait = min(90, 3 * 2 ** attempt) + random.uniform(0, 1.5)
                with lock:
                    print(f"    retry {attempt+1}/8 after {type(e).__name__}, "
                          f"waiting {wait:.0f}s", flush=True)
                time.sleep(wait)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(work, bt, nt): bt for bt, nt in batches}
        since = 0
        for f in as_completed(futs):
            bt, embs = f.result()
            with lock:
                for h, v in zip(bt, embs):
                    vecs[h] = np.asarray(v, dtype=np.float32)
                done[0] += len(bt)
                since += len(bt)
                el = time.time() - t0
                rate = done[0] / max(el, 1e-9)
                print(f"  {done[0]}/{len(todo)} | {rate:.0f}/s | "
                      f"eta {(len(todo)-done[0])/max(rate,1e-9)/60:.1f} min", flush=True)
                if since >= 2000:
                    save_ckpt(ckpt, vecs, dim)
                    since = 0
                    print("    checkpointed", flush=True)
    save_ckpt(ckpt, vecs, dim)
    return time.time() - t0


def embed_local(todo, texts, cfg, ckpt, vecs, batch):
    """Batched by TOKEN BUDGET, not by text count.

    `encode` pads a batch to its longest sequence, so cost is
    longest x batch_size, not batch_size. Passing 256 texts per call blew up to
    4.3 GB on this machine and was killed -- v2's chunks are 2.4x larger than
    v1's (median 1,249 vs 526 chars), so the same count costs far more than it
    used to. embed_e5 already ships `token_batches` with a TOKEN_BUDGET for
    exactly this; using it keeps the job inside a few hundred MB.
    """
    from embed_e5 import load_model, encode, token_batches
    tok, model = load_model(cfg["model"])
    dim = cfg["dim"]
    items = [(h, texts[h]) for h in todo]
    t0 = time.time()
    done = 0
    nb = 0
    for bt in token_batches(items, tok, "passage: "):
        V = encode([t for _, t in bt], tok, model, "passage: ")
        for (h, _), v in zip(bt, V):
            vecs[h] = np.asarray(v, dtype=np.float32)
        done += len(bt)
        nb += 1
        el = time.time() - t0
        rate = done / max(el, 1e-9)
        if nb % 10 == 0 or done == len(todo):
            print(f"  {done}/{len(todo)} | {rate:.1f}/s | "
                  f"eta {(len(todo)-done)/max(rate,1e-9)/60:.1f} min", flush=True)
        if nb % 60 == 0:
            save_ckpt(ckpt, vecs, dim)
    save_ckpt(ckpt, vecs, dim)
    return time.time() - t0


def build_collections(cfg, vecs):
    """Stream rows from sqlite into Chroma in batches; metadata from build_chroma."""
    import chromadb
    import build_chroma as bc
    client = chromadb.PersistentClient(path=str(CHROMA))
    for name in (cfg["active"], cfg["archive"]):
        try:
            client.delete_collection(name)
        except Exception:
            pass
    col = client.get_or_create_collection(cfg["active"], metadata={"hnsw:space": "cosine"})
    arc = client.get_or_create_collection(cfg["archive"], metadata={"hnsw:space": "cosine"})

    for path, target, archived, label in ((V2, col, False, cfg["active"]),
                                          (V2Q, arc, True, cfg["archive"])):
        db = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        db.row_factory = sqlite3.Row
        ids, docs, metas, embs = [], [], [], []
        seen, miss, n = set(), 0, 0
        for r in db.execute("select * from chunks"):
            v = vecs.get(r["content_hash"])
            if v is None:
                miss += 1
                continue
            fid = f"{r['content_hash']}-{r['parent_source_id']}"
            if fid in seen:
                continue
            seen.add(fid)
            ids.append(fid); docs.append(r["text"])
            metas.append(bc.meta_of(r, archived)); embs.append(v.tolist())
            if len(ids) >= 500:
                target.upsert(ids=ids, documents=docs, metadatas=metas, embeddings=embs)
                n += len(ids)
                ids, docs, metas, embs = [], [], [], []
        if ids:
            target.upsert(ids=ids, documents=docs, metadatas=metas, embeddings=embs)
            n += len(ids)
        db.close()
        print(f"  {label}: {n} records (skipped {miss} without a vector)")
    return col.count(), arc.count()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backend", choices=sorted(BACKENDS), required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--plan", action="store_true")
    g.add_argument("--run", action="store_true")
    ap.add_argument("--batch", type=int, default=0)
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--tpm", type=int, default=820_000,
                    help="tokens-per-minute budget to pace under (org limit is 1M)")
    a = ap.parse_args()

    cfg = BACKENDS[a.backend]
    batch = a.batch or (128 if a.backend == "openai" else 256)
    ckpt = K3 / f"vectors_v2_{a.backend}.npz"

    texts = all_texts()
    vecs = load_ckpt(ckpt, cfg["dim"])
    todo = sorted(h for h in texts if h not in vecs)
    chars = sum(len(texts[h]) for h in todo)

    print(f"backend  {a.backend}: {cfg['model']} at {cfg['dim']}-d -> {cfg['active']}")
    print(f"texts    {len(texts)} distinct | already embedded {len(vecs)} | to do {len(todo)}")
    print(f"chars    {chars:,} | ~{chars//4:,} tokens (chars/4; Devanagari runs denser)")
    if a.backend == "openai":
        print(f"cost     ~${chars/4/1e6*0.13:.2f} at $0.13/M tokens "
              f"(ceiling ~${chars/2/1e6*0.13:.2f} if tokens run 2x the estimate)")
        print(f"requests {(len(todo)+batch-1)//batch} of up to {batch} texts, "
              f"{a.workers} concurrent, exponential backoff on rate limits")
    else:
        print(f"cost     none (local model, CPU only)")
    if a.plan:
        return 0

    if todo:
        if a.backend == "openai":
            wall = embed_openai(todo, texts, cfg, ckpt, vecs, batch, a.workers, a.tpm)
        else:
            wall = embed_local(todo, texts, cfg, ckpt, vecs, batch)
        print(f"\nembedded {len(todo)} texts in {wall/60:.1f} min "
              f"({len(todo)/max(wall,1e-9):.1f} texts/s)")
    else:
        print("\nnothing to embed; using the checkpoint")

    # sanity before writing a collection
    V = np.stack([vecs[h] for h in list(texts) if h in vecs])
    norms = np.linalg.norm(V, axis=1)
    print(f"vectors  {V.shape} | finite {bool(np.isfinite(V).all())} | "
          f"non-zero {int((norms > 1e-6).sum())}/{len(norms)} | "
          f"norm mean {norms.mean():.3f}")
    del V

    print("\nbuilding collections...")
    na, nq = build_collections(cfg, vecs)
    print(f"\ncounts: {cfg['active']}={na} {cfg['archive']}={nq}")
    w = sqlite3.connect(str(V2))
    with w:
        w.execute("insert or replace into meta values (?,?)",
                  (f"dense_{a.backend}", f"{cfg['model']} @ {cfg['dim']}d -> {cfg['active']}"))
    w.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
