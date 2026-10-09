#!/usr/bin/env python
"""Step 2, embed stage — vectors for the v2 store and the udaypur_kb_v2 collection.

    python phase4_step2_embed.py --plan      # report scope, embed nothing
    python phase4_step2_embed.py --run

MODEL: the LOCAL intfloat/multilingual-e5-small, the same one that embedded v1.
A collection must be all-local or all-OpenAI; mixing two embedding spaces in one
collection makes every distance meaningless. The OpenAI decision is Step 4's, so
nothing here touches a key and nothing leaves this machine.

REUSE: vectors are keyed by CONTENT HASH, not by chunk id or source id. Text is
all an embedding depends on, and the Patil merge changed parent_source_id on 516
chunks, so a source-keyed reuse would have needlessly re-embedded them. Whatever
v1 already embedded is reused verbatim; only genuinely new text is encoded.

Metadata comes from build_chroma.meta_of, unchanged, so v2 inherits the same
rules -- including the Step 1 fix that makes a quarantined row archived AND
un-bucketed rather than merely unquotable.
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
K3 = ROOT / "kb3"
V2 = K3 / "kb_active_v2.sqlite"
V2Q = K3 / "kb_quarantine_v2.sqlite"
CHROMA = K3 / "chroma"
V1_COLL = "udaypur_kb"
V2_COLL = "udaypur_kb_v2"
V2_ARCH = "udaypur_kb_v2_archive"
MODEL = "intfloat/multilingual-e5-small"


def rows_of(db_path):
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    return db, list(db.execute("select * from chunks"))


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--plan", action="store_true")
    g.add_argument("--run", action="store_true")
    ap.add_argument("--batch", type=int, default=256)
    a = ap.parse_args()

    import chromadb
    client = chromadb.PersistentClient(path=str(CHROMA))

    _, act = rows_of(V2)
    _, qua = rows_of(V2Q)
    print(f"v2 active {len(act)} chunks | v2 quarantine {len(qua)} chunks")

    # existing vectors, keyed by content hash (ids are "<hash>-<source_id>")
    # ids are "<content_hash>-<source_id>"; the hash is hex with no hyphen, so
    # the first hyphen is the boundary (splitting on the LAST one would break,
    # because source ids contain hyphens).
    old = client.get_collection(V1_COLL)
    got = old.get(limit=200000, include=["embeddings"])
    need = {r["content_hash"] for r in act} | {r["content_hash"] for r in qua}
    byhash = {}
    for i, v in zip(got["ids"], got["embeddings"]):
        h = i.split("-", 1)[0]
        if h in need:
            byhash[h] = v
    reuse = set(byhash) & need
    print(f"v1 collection: {len(got['ids'])} vectors | reusable for v2: {len(reuse)}")
    todo = sorted(need - reuse)
    print(f"\nscope:")
    print(f"  distinct texts in v2        : {len(need)}")
    print(f"  reuse existing vectors      : {len(reuse)}")
    print(f"  to embed locally ({MODEL.split('/')[-1]}): {len(todo)}")
    print(f"  measured local rate 17.5/s  -> ~{len(todo)/17.5/60:.1f} min")
    print(f"  API calls / cost             : none (local model)")
    if a.plan:
        return 0

    # ---- embed what is missing --------------------------------------------
    from embed_e5 import load_model, encode
    tok, model = load_model(MODEL)
    text_of = {}
    for r in act:
        text_of.setdefault(r["content_hash"], r["text"])
    for r in qua:
        text_of.setdefault(r["content_hash"], r["text"])

    t0 = time.time()
    done = 0
    for s in range(0, len(todo), a.batch):
        batch = todo[s:s + a.batch]
        V = encode([text_of[h] for h in batch], tok, model, "passage: ")
        for h, v in zip(batch, V):
            byhash[h] = v.astype("float32").tolist()
        done += len(batch)
        el = time.time() - t0
        print(f"  embedded {done}/{len(todo)} | {done/max(el,1e-9):.1f}/s | "
              f"eta {(len(todo)-done)/max(done/max(el,1e-9),1e-9)/60:.1f} min", flush=True)
    wall = time.time() - t0
    print(f"\nlocal embed: {len(todo)} chunks in {wall/60:.1f} min "
          f"({len(todo)/max(wall,1e-9):.1f} chunks/s)")

    # ---- build the v2 collections -----------------------------------------
    import build_chroma as bc
    for name in (V2_COLL, V2_ARCH):
        try:
            client.delete_collection(name)
        except Exception:
            pass
    meta_common = {"hnsw:space": "cosine"}
    col = client.get_or_create_collection(V2_COLL, metadata=meta_common)
    arc = client.get_or_create_collection(V2_ARCH, metadata=meta_common)

    for name, target, rows, archived in ((V2_COLL, col, act, False),
                                         (V2_ARCH, arc, qua, True)):
        ids, docs, metas, embs, miss = [], [], [], [], 0
        seen = set()
        for r in rows:
            v = byhash.get(r["content_hash"])
            if v is None:
                miss += 1
                continue
            fid = f"{r['content_hash']}-{r['parent_source_id']}"
            if fid in seen:
                continue
            seen.add(fid)
            ids.append(fid)
            docs.append(r["text"])
            metas.append(bc.meta_of(r, archived))
            embs.append(v)
        for s in range(0, len(ids), 1000):
            target.upsert(ids=ids[s:s + 1000], documents=docs[s:s + 1000],
                          metadatas=metas[s:s + 1000], embeddings=embs[s:s + 1000])
        print(f"{name}: {len(ids)} records (skipped {miss} without a vector)")

    print(f"\ncounts: {V2_COLL}={col.count()} {V2_ARCH}={arc.count()}")
    w = sqlite3.connect(str(V2))
    with w:
        w.execute("insert or replace into meta values (?,?)",
                  ("dense", f"{MODEL} (local), embedded {len(todo)} new + reused {len(reuse)}"))
    w.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
