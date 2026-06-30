#!/usr/bin/env python3
"""
build_kb.py — build a local vector knowledge base from Markdown sources.

Chunks every .md file in a source directory, embeds the chunks with Mistral
embeddings (mistral-embed), and persists a simple, dependency-light vector store
under ./kb/ :

    kb/embeddings.npy   float32 [N, dim], L2-normalized (cosine == dot product)
    kb/chunks.jsonl     one record per chunk: {source, heading, chunk, text}
    kb/config.json      {model, dim, count, source_dir}

Query it with kb_search.py.

Requires: mistralai, python-dotenv, numpy ; MISTRAL_API_KEY in .env.
Usage:    python build_kb.py ["Udaypur Reference Markdown Files"]
"""
import glob
import json
import os
import sys
import time
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()

MODEL = os.environ.get("MISTRAL_EMBED_MODEL", "mistral-embed")
KB_DIR = Path("kb")
MAX_CHARS = 1800          # target chunk size (~350-450 words)
MIN_FLUSH = int(MAX_CHARS * 0.6)
BATCH_TOKENS = 12000      # approx token budget per embed request (chars/4)
BATCH_ITEMS = 64


def chunk_markdown(path):
    """Split a markdown file into (heading_trail, body) chunks."""
    lines = Path(path).read_text(encoding="utf-8").split("\n")
    chunks, buf, buflen, heading = [], [], 0, ""

    def flush():
        nonlocal buf, buflen
        body = "\n".join(buf).strip()
        if body:
            chunks.append((heading, body))
        buf, buflen = [], 0

    for ln in lines:
        if ln.lstrip().startswith("#"):
            flush()
            heading = ln.lstrip("#").strip()
            continue
        if ln.strip() == "" and buflen > MIN_FLUSH:
            flush()
            continue
        buf.append(ln)
        buflen += len(ln) + 1
        if buflen >= MAX_CHARS:
            flush()
    flush()
    return chunks


def embed_all(client, texts):
    out, i = [], 0
    while i < len(texts):
        batch, toks = [], 0
        while i < len(texts):
            tt = len(texts[i]) // 4 + 1
            if batch and (toks + tt > BATCH_TOKENS or len(batch) >= BATCH_ITEMS):
                break
            batch.append(texts[i]); toks += tt; i += 1
        for attempt in range(5):
            try:
                r = client.embeddings.create(model=MODEL, inputs=batch)
                out.extend(d.embedding for d in r.data)
                break
            except Exception as e:                       # noqa: BLE001 retry transient
                if attempt == 4:
                    raise
                print(f"    embed retry {attempt+1}: {type(e).__name__}", flush=True)
                time.sleep(5 * (attempt + 1))
        print(f"  embedded {len(out)}/{len(texts)} chunks", flush=True)
    return out


def main():
    src_dir = sys.argv[1] if len(sys.argv) > 1 else "Udaypur Reference Markdown Files"
    key = os.environ.get("MISTRAL_API_KEY")
    if not key:
        print("ERROR: MISTRAL_API_KEY not set"); sys.exit(1)
    files = sorted(glob.glob(os.path.join(src_dir, "*.md")))
    if not files:
        print(f"No .md files in {src_dir}"); sys.exit(1)

    records, texts = [], []
    for f in files:
        for j, (heading, body) in enumerate(chunk_markdown(f)):
            name = os.path.basename(f)
            records.append({"source": name, "heading": heading, "chunk": j})
            # prepend source + heading context so retrieval is grounded
            texts.append(f"[{name}] {heading}\n{body}".strip())
    print(f"{len(files)} files -> {len(texts)} chunks; embedding with {MODEL} ...", flush=True)

    client = Mistral(api_key=key)
    embs = embed_all(client, texts)
    arr = np.asarray(embs, dtype="float32")
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    arr = arr / norms

    KB_DIR.mkdir(exist_ok=True)
    np.save(KB_DIR / "embeddings.npy", arr)
    with open(KB_DIR / "chunks.jsonl", "w", encoding="utf-8") as fh:
        for rec, txt in zip(records, texts):
            fh.write(json.dumps({**rec, "text": txt}, ensure_ascii=False) + "\n")
    json.dump({"model": MODEL, "dim": int(arr.shape[1]), "count": int(arr.shape[0]),
               "source_dir": src_dir},
              open(KB_DIR / "config.json", "w", encoding="utf-8"), indent=2)
    print(f"KB built: {arr.shape[0]} chunks, dim {arr.shape[1]} -> {KB_DIR}/", flush=True)


if __name__ == "__main__":
    main()
