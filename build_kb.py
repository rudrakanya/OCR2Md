#!/usr/bin/env python3
"""
build_kb.py — build a local vector knowledge base from Markdown sources.

Chunks every .md file in a source directory, embeds the chunks with Mistral
embeddings (mistral-embed), and persists a simple, dependency-light vector store
under ./kb/ :

    kb/embeddings.npy   float32 [N, dim], L2-normalized (cosine == dot product)
    kb/chunks.jsonl     one record per chunk: {source, heading, chunk, text}
    kb/config.json      {model, dim, count, source_dir, fingerprint}

It is idempotent: if the sources, model, and chunk settings are unchanged since
the last build, it skips (no re-embedding). Use --force to rebuild anyway.

Query it with kb_search.py.

Requires: mistralai, python-dotenv, numpy ; MISTRAL_API_KEY in .env.
Usage:    python build_kb.py ["Udaypur Reference Markdown Files"] [--force]
"""
import argparse
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
load_dotenv(Path(__file__).resolve().parent / ".env", override=False)

MODEL = os.environ.get("MISTRAL_EMBED_MODEL", "mistral-embed")
KB_DIR = Path(os.environ.get("KB_DIR", "kb"))
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


def fingerprint(files):
    """A signature of the inputs + settings; identical => KB is still current."""
    stat = [[os.path.basename(f), os.path.getsize(f), int(os.path.getmtime(f))] for f in sorted(files)]
    return {"model": MODEL, "max_chars": MAX_CHARS, "files": stat}


def embed_all(client, texts):
    out, i = [], 0
    while i < len(texts):
        batch, toks = [], 0
        while i < len(texts):
            tt = len(texts[i]) // 4 + 1
            if batch and (toks + tt > BATCH_TOKENS or len(batch) >= BATCH_ITEMS):
                break
            batch.append(texts[i]); toks += tt; i += 1
        delay = 5
        for attempt in range(5):
            try:
                r = client.embeddings.create(model=MODEL, inputs=batch)
                out.extend(d.embedding for d in r.data)
                break
            except Exception as e:                       # noqa: BLE001 retry transient
                if attempt == 4:
                    raise
                print(f"    embed retry {attempt+1}: {type(e).__name__}", flush=True)
                time.sleep(delay); delay = min(delay * 2, 60)
        print(f"  embedded {len(out)}/{len(texts)} chunks", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser(description="Build the vector knowledge base from a Markdown folder")
    ap.add_argument("src_dir", nargs="?", default="Udaypur Reference Markdown Files")
    ap.add_argument("--force", action="store_true", help="rebuild even if sources are unchanged")
    args = ap.parse_args()

    key = os.environ.get("MISTRAL_API_KEY")
    if not key:
        print("ERROR: MISTRAL_API_KEY not set (put it in .env or the environment)"); sys.exit(1)

    files = sorted(glob.glob(os.path.join(args.src_dir, "*.md")))
    if not files:
        print(f"ERROR: no .md files in '{args.src_dir}'"); sys.exit(1)

    fp = fingerprint(files)
    cfg_path = KB_DIR / "config.json"
    if cfg_path.exists() and not args.force:
        try:
            old = json.loads(cfg_path.read_text(encoding="utf-8"))
            if old.get("fingerprint") == fp:
                print(f"KB is up to date ({old.get('count')} chunks); nothing to rebuild. Use --force to override.")
                return
        except Exception:
            pass  # unreadable/old config -> rebuild

    records, texts = [], []
    for f in files:
        for j, (heading, body) in enumerate(chunk_markdown(f)):
            name = os.path.basename(f)
            records.append({"source": name, "heading": heading, "chunk": j})
            texts.append(f"[{name}] {heading}\n{body}".strip())
    if not texts:
        print("ERROR: sources produced no text chunks"); sys.exit(1)
    print(f"{len(files)} files -> {len(texts)} chunks; embedding with {MODEL} ...", flush=True)

    client = Mistral(api_key=key)
    arr = np.asarray(embed_all(client, texts), dtype="float32")
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    arr = arr / norms

    KB_DIR.mkdir(parents=True, exist_ok=True)
    np.save(KB_DIR / "embeddings.npy", arr)
    with open(KB_DIR / "chunks.jsonl", "w", encoding="utf-8") as fh:
        for rec, txt in zip(records, texts):
            fh.write(json.dumps({**rec, "text": txt}, ensure_ascii=False) + "\n")
    json.dump({"model": MODEL, "dim": int(arr.shape[1]), "count": int(arr.shape[0]),
               "source_dir": args.src_dir, "fingerprint": fp},
              open(KB_DIR / "config.json", "w", encoding="utf-8"), indent=2)
    print(f"KB built: {arr.shape[0]} chunks, dim {arr.shape[1]} -> {KB_DIR}/", flush=True)


if __name__ == "__main__":
    main()
