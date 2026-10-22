"""Embed every caption for semantic search (paid: OpenAI, approved by the user 22 Oct 2026; ~25k tokens, < $0.01).

  python -I -X utf8 drafting/image_store_hardy/_tools/embed.py [--dry-run]

One vector per label (the whole figure and its parts share their caption). The embedded text is
"<label ref> (<chapter title>; <image type>): <caption>", so that a query naming a chapter subject or an image type
("Bhumija tower drawings") finds the right figures. Model and dimensions match the project's knowledge base
(text-embedding-3-large at 1536-d). Output: caption_embeddings.npz (ids, labels, texts, unit vectors) and
caption_embeddings.json (model, date, token count, cost).
Re-running only re-embeds captions whose text changed (cached by text hash).
"""
import argparse
import datetime
import hashlib
import json
import os
import sys
from pathlib import Path

import numpy as np

STORE = Path(__file__).resolve().parents[1]
REPO = STORE.parents[1]
MODEL, DIM = "text-embedding-3-large", 1536
PRICE_PER_M = 0.13          # USD per 1M tokens, text-embedding-3-large


def load_key():
    k = os.environ.get("OPENAI_API_KEY", "").strip()
    if len(k) > 20:
        return k
    env = REPO / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8", errors="replace").split("\n"):
            line = line.strip()
            if line.startswith("OPENAI_API_KEY"):
                v = line.split("=", 1)[-1].strip().strip('"').strip("'")
                if len(v) > 20:
                    return v
    raise SystemExit("OPENAI_API_KEY not found in environment or .env")


def embed_text(r):
    ctx = "; ".join(x for x in (f"ch. {r['chapter']} {r['chapter_title']}" if r.get("chapter") else None,
                                r["image_type"]) if x)
    return f"{r['label_ref']} ({ctx}): {r['caption']}"


def items():
    seen, out = set(), []
    for l in (STORE / "image_manifest.jsonl").open(encoding="utf-8"):
        r = json.loads(l)
        if r["label"] in seen or not r.get("caption"):
            continue
        seen.add(r["label"])
        out.append((r["parent_id"] or r["id"], r["label"], embed_text(r)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    its = items()
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    ntok = sum(len(enc.encode(t)) for _, _, t in its)
    print(f"{len(its)} captions, {ntok} tokens, est. ${ntok * PRICE_PER_M / 1e6:.4f} with {MODEL}")
    if a.dry_run:
        return
    cache_p = STORE / "_work" / "embed_cache.npz"
    cache = {}
    if cache_p.exists():
        z = np.load(cache_p, allow_pickle=False)
        cache = dict(zip(z["hashes"].tolist(), z["vecs"]))
    h = [hashlib.sha256(f"{MODEL}|{DIM}|{t}".encode()).hexdigest() for _, _, t in its]
    todo = [i for i, x in enumerate(h) if x not in cache]
    sent_tokens = sum(len(enc.encode(its[i][2])) for i in todo)
    if todo:
        from openai import OpenAI
        client = OpenAI(api_key=load_key())
        for s in range(0, len(todo), 100):
            batch = todo[s:s + 100]
            resp = client.embeddings.create(model=MODEL, input=[its[i][2] for i in batch], dimensions=DIM)
            for i, d in zip(batch, resp.data):
                cache[h[i]] = np.array(d.embedding, dtype=np.float32)
            print(f"  embedded {min(s + 100, len(todo))}/{len(todo)}", flush=True)
        np.savez(cache_p, hashes=np.array(list(cache)), vecs=np.stack(list(cache.values())))
    V = np.stack([cache[x] for x in h]).astype(np.float32)
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    np.savez(STORE / "caption_embeddings.npz", ids=np.array([i for i, _, _ in its]),
             labels=np.array([l for _, l, _ in its]), texts=np.array([t for _, _, t in its]), vecs=V)
    meta = {"model": MODEL, "dimensions": DIM, "captions": len(its), "date": datetime.date.today().isoformat(),
            "tokens_total": ntok, "tokens_sent_this_run": sent_tokens,
            "cost_usd_this_run": round(sent_tokens * PRICE_PER_M / 1e6, 5),
            "embedded_text": "<label ref> (<chapter title>; <image type>): <caption>"}
    (STORE / "caption_embeddings.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(json.dumps(meta))


if __name__ == "__main__":
    main()
