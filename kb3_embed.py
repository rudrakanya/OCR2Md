#!/usr/bin/env python
"""Embed Stage 1 chunks with BAAI/bge-m3 (dense, CLS-pooled, L2-normed), int8.

    python kb3_embed.py                    # claim-bearing, Udaypur-relevant chunks
    python kb3_embed.py --include-skipped  # also embed the skip list (see below)

Why bge-m3: it is multilingual, so the Hindi original of *Jagta Hua Kasba*
and its English translation land near each other. That is what lets the dedup
pass link a translation to its original (spec D), which no lexical method can.
It is already in the local Hugging Face cache; nothing is downloaded.

SPEED (measured 2026-09-22 on this i7-1185G7, 4 cores, ~3 GB free RAM)
  * The first version ran in bfloat16 to save memory. This CPU has no native
    bf16 (no AVX512-BF16), so PyTorch fell back to slow kernels on ~1 core:
    3.7–7 chunks/s, 60–120 min projected. Abandoned; its vectors are kept in
    kb3/emb_parts_bf16_discarded/ and never mixed with these.
  * Now: fp32 weights memory-mapped from safetensors, then every nn.Linear is
    dynamically quantized to int8 (torch quantize_dynamic, in place). Tiger
    Lake has AVX-512 VNNI, so int8 matmuls run multi-threaded on all cores.
    The 250k-token vocabulary table stays fp32 (~1 GB); the rest ~0.6 GB.
  * Batches are built to a TOKEN budget, not a fixed count, so the long
    Devanagari-heavy chunks do not pad a whole batch or spike memory.

SKIP LIST (not embedded by default; embed later with --include-skipped)
  * non-claim chunks (index, TOC, bibliography, OCR garbage): they go to the
    quarantine archive as apparatus and are never retrieved.
  * contextual_background (Temple_Economics): relevance is scored lexically
    only; it is never cited as a Udaypur claim (spec C5).

Resumable: vectors are written per part and keyed by content_hash. A killed
run loses at most one part; a re-chunk re-uses every unchanged vector. The
manifest pins the model setting so parts from different settings never mix.
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
OUT = ROOT / "kb3"
PARTS = OUT / "emb_parts"
MODEL = "BAAI/bge-m3"
SETTING = "bge-m3|cls|l2|int8-dynamic-linear|maxlen512"
MAX_LEN, TOKEN_BUDGET, PART_SIZE, THREADS = 512, 6144, 512, 4


def skipped(r: dict) -> str | None:
    if not r["claim_bearing"]:
        return "non_claim"
    if r["source_type"] == "contextual_background":
        return "contextual_background"
    return None


def load_model():
    import torch
    from transformers import AutoModel, AutoTokenizer
    torch.set_num_threads(THREADS)
    tok = AutoTokenizer.from_pretrained(MODEL, local_files_only=True)
    model = AutoModel.from_pretrained(MODEL, local_files_only=True, dtype=torch.float32,
                                      low_cpu_mem_usage=True, use_safetensors=True).eval()
    torch.ao.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8, inplace=True)
    return tok, model


def token_batches(items, tok):
    """items sorted by length -> lists whose (n × longest) stays within budget."""
    lens = [min(MAX_LEN, len(ids)) for ids in
            tok([t for _, t in items], truncation=True, max_length=MAX_LEN)["input_ids"]]
    batch, longest = [], 0
    for item, n in zip(items, lens):
        if batch and max(longest, n) * (len(batch) + 1) > TOKEN_BUDGET:
            yield batch
            batch, longest = [], 0
        batch.append(item)
        longest = max(longest, n)
    if batch:
        yield batch


def encode(texts, tok, model):
    import torch
    with torch.inference_mode():
        enc = tok(texts, padding=True, truncation=True, max_length=MAX_LEN, return_tensors="pt")
        out = model(**enc).last_hidden_state[:, 0]          # CLS pooling (bge-m3 dense)
        out = torch.nn.functional.normalize(out.float(), dim=-1)
    return out.numpy().astype(np.float16)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--include-skipped", action="store_true")
    args = ap.parse_args(argv)

    PARTS.mkdir(parents=True, exist_ok=True)
    manifest = PARTS / "manifest.json"
    if manifest.exists() and json.loads(manifest.read_text())["setting"] != SETTING:
        sys.exit(f"{PARTS} holds vectors from another setting; move them aside first.")
    manifest.write_text(json.dumps({"model": MODEL, "setting": SETTING}))

    done = set()
    for f in PARTS.glob("part_*.json"):
        done.update(json.loads(f.read_text()))
    todo, seen, skip = [], set(), {}
    for line in open(INV, encoding="utf-8"):
        r = json.loads(line)
        h = r["content_hash"]
        if h in done or h in seen:
            continue
        seen.add(h)
        why = skipped(r)
        if why and not args.include_skipped:
            skip[why] = skip.get(why, 0) + 1
            continue
        todo.append((h, r["text"][:4000]))
    print(f"{len(done):,} already embedded, {len(todo):,} to go, skipped {skip}", flush=True)
    if not todo:
        return 0
    todo.sort(key=lambda x: len(x[1]))
    t_load = time.time()
    tok, model = load_model()
    print(f"model loaded + quantized in {time.time() - t_load:.0f}s", flush=True)

    t0 = time.time()
    part_no = len(list(PARTS.glob("part_*.json")))
    for p in range(0, len(todo), PART_SIZE):
        part = todo[p:p + PART_SIZE]
        hashes, vecs = [], []
        for b in token_batches(part, tok):
            vecs.append(encode([t for _, t in b], tok, model))
            hashes += [h for h, _ in b]
        np.save(PARTS / f"part_{part_no:04d}.npy", np.vstack(vecs))
        (PARTS / f"part_{part_no:04d}.json").write_text(json.dumps(hashes))
        part_no += 1
        n = p + len(part)
        rate = (time.time() - t0) / n
        print(f"  {n:,}/{len(todo):,}  {1 / rate:.1f} chunks/s  eta {rate * (len(todo) - n) / 60:.1f} min",
              flush=True)
    print(f"done in {(time.time() - t0) / 60:.1f} min", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
