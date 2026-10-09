#!/usr/bin/env python
"""Embed the classified inventory with a local multilingual model, for ChromaDB.

    python embed_e5.py                  # resumable; writes kb3/emb_e5/part_*.npy
    python embed_e5.py --model BAAI/bge-m3 --out kb3/emb_bge --prefix ""

Default model: intfloat/multilingual-e5-small (384-d). Chosen in DIAGNOSIS.md
over bge-m3 because this machine (4 cores, ~3 GB free) killed the bge-m3 run
twice; e5-small is several times faster at ~0.5 GB. Both handle English,
Devanagari and IAST, which this corpus mixes.

e5 models expect "passage: " on documents and "query: " on queries; the prefix
is applied here and must match in the query path (kb3_chroma_query.py).

int8 dynamic quantization: this CPU has AVX-512 VNNI, so int8 matmuls run
multi-threaded; it has no native bf16, which is why the earlier bf16 attempt
crawled on one core.

Resumable: parts of 1,000 vectors keyed by content_hash. Nothing is embedded
twice, and a killed run resumes where it stopped.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
INV = ROOT / "kb_audit" / "classified_inventory.jsonl"
MAX_LEN, TOKEN_BUDGET, PART, THREADS = 512, 8192, 1000, 4


def load_model(name: str):
    import torch
    from transformers import AutoModel, AutoTokenizer
    torch.set_num_threads(THREADS)
    tok = AutoTokenizer.from_pretrained(name, local_files_only=True)
    model = AutoModel.from_pretrained(name, local_files_only=True, dtype=torch.float32,
                                      low_cpu_mem_usage=True, use_safetensors=True).eval()
    torch.ao.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8, inplace=True)
    return tok, model


def encode(texts, tok, model, prefix=""):
    import torch
    with torch.inference_mode():
        enc = tok([prefix + t for t in texts], padding=True, truncation=True,
                  max_length=MAX_LEN, return_tensors="pt")
        out = model(**enc).last_hidden_state
        mask = enc["attention_mask"].unsqueeze(-1).float()
        pooled = (out * mask).sum(1) / mask.sum(1).clamp(min=1e-9)     # mean pooling (e5)
        pooled = torch.nn.functional.normalize(pooled.float(), dim=-1)
    return pooled.numpy().astype(np.float16)


def token_batches(items, tok, prefix):
    lens = [min(MAX_LEN, len(x)) for x in
            tok([prefix + t for _, t in items], truncation=True, max_length=MAX_LEN)["input_ids"]]
    batch, longest = [], 0
    for item, n in zip(items, lens):
        if batch and max(longest, n) * (len(batch) + 1) > TOKEN_BUDGET:
            yield batch
            batch, longest = [], 0
        batch.append(item)
        longest = max(longest, n)
    if batch:
        yield batch


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="intfloat/multilingual-e5-small")
    ap.add_argument("--out", default="kb3/emb_e5")
    ap.add_argument("--prefix", default="passage: ")
    a = ap.parse_args(argv)

    out = ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    manifest = out / "manifest.json"
    setting = f"{a.model}|mean|l2|int8|maxlen{MAX_LEN}|prefix={a.prefix.strip()}"
    if manifest.exists() and json.loads(manifest.read_text())["setting"] != setting:
        sys.exit(f"{out} holds vectors from another setting; move them aside first.")
    manifest.write_text(json.dumps({"model": a.model, "setting": setting, "dim": None}))

    done = set()
    for f in out.glob("part_*.json"):
        done.update(json.loads(f.read_text()))
    todo, seen = [], set()
    for line in open(INV, encoding="utf-8"):
        r = json.loads(line)
        h = r["content_hash"]
        if h in done or h in seen:
            continue
        seen.add(h)
        todo.append((h, r["text"][:4000]))
    print(f"{len(done):,} embedded, {len(todo):,} to go", flush=True)
    if not todo:
        return 0
    todo.sort(key=lambda x: len(x[1]))
    t0 = time.time()
    tok, model = load_model(a.model)
    print(f"model loaded in {time.time() - t0:.0f}s", flush=True)
    t0, n_part = time.time(), len(list(out.glob("part_*.json")))
    for p in range(0, len(todo), PART):
        part = todo[p:p + PART]
        hashes, vecs = [], []
        for b in token_batches(part, tok, a.prefix):
            vecs.append(encode([t for _, t in b], tok, model, a.prefix))
            hashes += [h for h, _ in b]
        np.save(out / f"part_{n_part:04d}.npy", np.vstack(vecs))
        (out / f"part_{n_part:04d}.json").write_text(json.dumps(hashes))
        n_part += 1
        n = p + len(part)
        rate = (time.time() - t0) / n
        print(f"  {n:,}/{len(todo):,}  {1 / rate:.1f} chunks/s  eta {rate * (len(todo) - n) / 60:.1f} min", flush=True)
    dim = int(np.load(out / f"part_{n_part - 1:04d}.npy").shape[1])
    manifest.write_text(json.dumps({"model": a.model, "setting": setting, "dim": dim}))
    print(f"done in {(time.time() - t0) / 60:.1f} min, dim={dim}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
