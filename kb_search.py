#!/usr/bin/env python3
"""
kb_search.py — query the local vector knowledge base built by build_kb.py.

As a module:
    from kb_search import search, search_batch
    hits = search("bhumija sikhara of the Udayesvara temple", k=8)
    # each hit: {score, source, heading, chunk, text}
    packs = search_batch(["query a", "query b"], k=8)   # one embed call, list per query

As a CLI:
    python kb_search.py "Udayaditya Paramara and the founding of Udayapur" -k 6
"""
import argparse
import json
import os
import sys
import time
from functools import lru_cache
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()
load_dotenv(Path(__file__).resolve().parent / ".env", override=False)
KB_DIR = Path(os.environ.get("KB_DIR", "kb"))


class KBError(RuntimeError):
    pass


def _require_key():
    key = os.environ.get("MISTRAL_API_KEY")
    if not key:
        raise KBError("MISTRAL_API_KEY is not set. Put it in a .env file (see .env.example).")
    return key


def get_client():
    return Mistral(api_key=_require_key())


@lru_cache(maxsize=1)
def _load():
    if not (KB_DIR / "config.json").exists():
        raise KBError(
            f"Knowledge base not found in '{KB_DIR}/'. Build it first:\n"
            f'    python build_kb.py "Udaypur Reference Markdown Files"'
        )
    cfg = json.loads((KB_DIR / "config.json").read_text(encoding="utf-8"))
    emb = np.load(KB_DIR / "embeddings.npy")
    chunks = [json.loads(l) for l in (KB_DIR / "chunks.jsonl").read_text(encoding="utf-8").splitlines()]
    if emb.shape[0] != len(chunks):
        raise KBError(f"KB is inconsistent: {emb.shape[0]} vectors vs {len(chunks)} chunks. Rebuild it.")
    return cfg, emb, chunks


def embed_texts(client, model, texts, attempts=5):
    """Embed a list of texts in one request, with retry/backoff."""
    delay = 5
    for n in range(1, attempts + 1):
        try:
            r = client.embeddings.create(model=model, inputs=texts)
            return [d.embedding for d in r.data]
        except Exception as e:                       # noqa: BLE001 - retry transient API/network errors
            if n == attempts:
                raise
            print(f"    embed retry {n}/{attempts - 1}: {type(e).__name__}", file=sys.stderr, flush=True)
            time.sleep(delay)
            delay = min(delay * 2, 60)


def _normalize(vec):
    v = np.asarray(vec, dtype="float32")
    nrm = np.linalg.norm(v)
    return v / (nrm if nrm else 1.0)


def search_batch(queries, k=8, client=None):
    """Return a list (one per query) of top-k hit lists."""
    cfg, emb, chunks = _load()
    client = client or get_client()
    vecs = embed_texts(client, cfg["model"], list(queries))
    results = []
    for vec in vecs:
        sims = emb @ _normalize(vec)
        idx = np.argsort(-sims)[:k]
        results.append([{"score": float(sims[i]), **chunks[i]} for i in idx])
    return results


def search(query, k=8, client=None):
    """Return the top-k hits for a single query."""
    return search_batch([query], k=k, client=client)[0]


def main():
    ap = argparse.ArgumentParser(description="Query the vector knowledge base")
    ap.add_argument("query", nargs="+")
    ap.add_argument("-k", type=int, default=8)
    args = ap.parse_args()
    try:
        hits = search(" ".join(args.query), k=args.k)
    except KBError as e:
        print(f"ERROR: {e}"); sys.exit(1)
    for r in hits:
        print(f"{r['score']:.3f}  [{r['source']}] {r['heading'][:70]}")
        snippet = r["text"].replace("\n", " ")
        print("   " + snippet[:220] + ("..." if len(snippet) > 220 else "") + "\n")


if __name__ == "__main__":
    main()
