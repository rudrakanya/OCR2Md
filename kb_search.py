#!/usr/bin/env python3
"""
kb_search.py — query the local vector knowledge base built by build_kb.py.

As a module:
    from kb_search import search
    hits = search("bhumija sikhara of the Udayesvara temple", k=8)
    # each hit: {score, source, heading, chunk, text}

As a CLI:
    python kb_search.py "Udayaditya Paramara and the founding of Udayapur" -k 6
"""
import argparse
import json
import os
from functools import lru_cache
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()
KB_DIR = Path("kb")


@lru_cache(maxsize=1)
def _load():
    cfg = json.loads((KB_DIR / "config.json").read_text(encoding="utf-8"))
    emb = np.load(KB_DIR / "embeddings.npy")
    chunks = [json.loads(l) for l in (KB_DIR / "chunks.jsonl").read_text(encoding="utf-8").splitlines()]
    return cfg, emb, chunks


def search(query, k=8, client=None):
    cfg, emb, chunks = _load()
    client = client or Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    q = client.embeddings.create(model=cfg["model"], inputs=[query]).data[0].embedding
    qv = np.asarray(q, dtype="float32")
    n = np.linalg.norm(qv)
    qv = qv / (n if n else 1.0)
    sims = emb @ qv
    idx = np.argsort(-sims)[:k]
    return [{"score": float(sims[i]), **chunks[i]} for i in idx]


def main():
    ap = argparse.ArgumentParser(description="Query the vector knowledge base")
    ap.add_argument("query", nargs="+")
    ap.add_argument("-k", type=int, default=8)
    args = ap.parse_args()
    for r in search(" ".join(args.query), k=args.k):
        print(f"{r['score']:.3f}  [{r['source']}] {r['heading'][:70]}")
        snippet = r["text"].replace("\n", " ")
        print("   " + snippet[:220] + ("..." if len(snippet) > 220 else "") + "\n")


if __name__ == "__main__":
    main()
