#!/usr/bin/env python
"""Step 0 — a restorable backup, taken before Phase 4 writes anything.

    python phase4_backup.py
    python phase4_backup.py --verify-only kb3/backup/<stamp>

Two restore paths are kept deliberately, because they fail differently:

  1. A byte copy of `kb3/chroma` and `kb_active.sqlite`. Fastest restore, but a
     Chroma directory is only guaranteed readable by the version that wrote it.
  2. A portable export of the `udaypur_kb` collection — ids, documents and
     metadata as JSONL, vectors as a float32 .npy. Survives a library upgrade
     and can rebuild the collection from scratch.

The sqlite copy goes through sqlite's own backup API rather than a file copy, so
it is consistent even if something holds the database open.

Nothing here is destructive: it only reads the live store and writes into a new
timestamped directory.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
LIVE_SQLITE = ROOT / "kb3" / "kb_active.sqlite"
LIVE_CHROMA = ROOT / "kb3" / "chroma"
COLLECTION = "udaypur_kb"
EXTRA = [ROOT / "kb_audit" / "source_registry.yaml",
         ROOT / "kb3" / "chapters.yaml",
         ROOT / "curated_facts.yaml",
         ROOT / "kb3" / "source_scores.yaml"]


def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f}{u}"
        n /= 1024
    return f"{n:.1f}TB"


def sha256(path, cap=None):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        read = 0
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
            read += len(b)
            if cap and read >= cap:
                break
    return h.hexdigest()[:16]


def backup_sqlite(src: Path, dst: Path):
    """A consistent copy via sqlite's online backup API, not a file copy."""
    s = sqlite3.connect(f"file:{src}?mode=ro", uri=True)
    d = sqlite3.connect(str(dst))
    with d:
        s.backup(d)
    n = d.execute("select count(*) from chunks").fetchone()[0]
    s.close()
    d.close()
    return n


def export_collection(out_dir: Path):
    """Portable export: vectors to .npy, everything else to JSONL."""
    import chromadb
    import numpy as np
    col = chromadb.PersistentClient(path=str(LIVE_CHROMA)).get_collection(COLLECTION)
    total = col.count()
    got = col.get(limit=total + 1000, include=["documents", "metadatas", "embeddings"])
    ids = got["ids"]
    V = np.asarray(got["embeddings"], dtype="float32")
    np.save(out_dir / "udaypur_kb.vectors.npy", V)
    with open(out_dir / "udaypur_kb.rows.jsonl", "w", encoding="utf-8") as f:
        for i, doc, m in zip(ids, got["documents"], got["metadatas"]):
            f.write(json.dumps({"id": i, "document": doc, "metadata": m},
                               ensure_ascii=False) + "\n")
    return total, len(ids), V.shape


def verify(stamp_dir: Path, manifest: dict):
    """Read every artefact back. A backup that was written but cannot be read is
    not a backup."""
    ok = True
    print("\n--- verification (reading the backup back) ---")

    db = stamp_dir / "kb_active.sqlite"
    try:
        c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        n = c.execute("select count(*) from chunks").fetchone()[0]
        cols = len(list(c.execute("PRAGMA table_info(chunks)")))
        integ = c.execute("PRAGMA integrity_check").fetchone()[0]
        c.close()
        good = n == manifest["sqlite_chunks"] and integ == "ok"
        print(f"  sqlite      : {n} chunks, {cols} columns, integrity_check={integ} "
              f"{'OK' if good else 'MISMATCH'}")
        ok &= good
    except Exception as e:
        print(f"  sqlite      : UNREADABLE — {e}")
        ok = False

    try:
        import chromadb
        col = chromadb.PersistentClient(path=str(stamp_dir / "chroma")).get_collection(COLLECTION)
        n = col.count()
        probe = col.get(limit=3, include=["embeddings", "metadatas"])
        dim = len(probe["embeddings"][0]) if len(probe["embeddings"]) else 0
        good = n == manifest["chroma_count"] and dim == manifest["dim"]
        print(f"  chroma copy : collection '{COLLECTION}' {n} rows, dim {dim} "
              f"{'OK' if good else 'MISMATCH'}")
        ok &= good
    except Exception as e:
        print(f"  chroma copy : UNREADABLE — {e}")
        ok = False

    try:
        import numpy as np
        V = np.load(stamp_dir / "udaypur_kb.vectors.npy")
        rows = sum(1 for _ in open(stamp_dir / "udaypur_kb.rows.jsonl", encoding="utf-8"))
        finite = bool(np.isfinite(V).all())
        nonzero = int((np.linalg.norm(V, axis=1) > 1e-6).sum())
        good = rows == manifest["chroma_count"] and V.shape[0] == rows and finite \
            and nonzero == rows
        print(f"  portable    : {rows} rows, vectors {V.shape}, all finite={finite}, "
              f"non-zero {nonzero}/{rows} {'OK' if good else 'MISMATCH'}")
        ok &= good
    except Exception as e:
        print(f"  portable    : UNREADABLE — {e}")
        ok = False

    for name in manifest["extra"]:
        p = stamp_dir / "config" / name
        good = p.exists() and p.stat().st_size > 0
        print(f"  {name:24s}: {'OK' if good else 'MISSING'}")
        ok &= good
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify-only")
    a = ap.parse_args()

    if a.verify_only:
        d = Path(a.verify_only)
        man = json.loads((d / "MANIFEST.json").read_text(encoding="utf-8"))
        print(f"verifying {d}")
        ok = verify(d, man)
        print("\nRESULT:", "backup is readable and complete" if ok else "BACKUP FAILED VERIFICATION")
        return 0 if ok else 1

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = ROOT / "kb3" / "backup" / f"phase4-{stamp}"
    (out / "config").mkdir(parents=True, exist_ok=True)
    print(f"backup -> {out}")

    t0 = time.time()
    print("\n--- 1. sqlite (online backup API) ---")
    n_sqlite = backup_sqlite(LIVE_SQLITE, out / "kb_active.sqlite")
    print(f"  kb_active.sqlite: {n_sqlite} chunks, "
          f"{human((out / 'kb_active.sqlite').stat().st_size)}")

    print("\n--- 2. chroma directory (byte copy) ---")
    shutil.copytree(LIVE_CHROMA, out / "chroma")
    import chromadb
    col = chromadb.PersistentClient(path=str(LIVE_CHROMA)).get_collection(COLLECTION)
    n_chroma = col.count()
    probe = col.get(limit=1, include=["embeddings"])
    dim = len(probe["embeddings"][0]) if len(probe["embeddings"]) else 0
    size = sum(p.stat().st_size for p in (out / "chroma").rglob("*") if p.is_file())
    print(f"  chroma: {n_chroma} rows in '{COLLECTION}', dim {dim}, {human(size)}")

    print("\n--- 3. portable export of the collection ---")
    total, got, shape = export_collection(out)
    print(f"  exported {got}/{total} rows, vectors {shape}")

    print("\n--- 4. config files ---")
    names = []
    for p in EXTRA:
        if p.exists():
            shutil.copy2(p, out / "config" / p.name)
            names.append(p.name)
            print(f"  {p.name} ({human(p.stat().st_size)})")
        else:
            print(f"  {p.name} — not present, skipped")

    manifest = {
        "created": stamp,
        "purpose": "Phase 4 pre-write backup",
        "live_sqlite": str(LIVE_SQLITE.relative_to(ROOT)),
        "live_chroma": str(LIVE_CHROMA.relative_to(ROOT)),
        "collection": COLLECTION,
        "sqlite_chunks": n_sqlite,
        "chroma_count": n_chroma,
        "dim": dim,
        "extra": names,
        "sqlite_sha256_16": sha256(out / "kb_active.sqlite"),
        "restore": {
            "sqlite": "copy config/.. and kb_active.sqlite back over kb3/kb_active.sqlite",
            "chroma_fast": "delete kb3/chroma, then copy this chroma/ directory to kb3/chroma",
            "chroma_portable": ("recreate the collection and add() from "
                                "udaypur_kb.rows.jsonl + udaypur_kb.vectors.npy "
                                "(same row order)"),
            "config": "copy files in config/ back to their original paths",
        },
    }
    (out / "MANIFEST.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")

    readme = f"""# Phase 4 backup — {stamp}

Taken before any Phase 4 write. Live state at this point:

  kb_active.sqlite   {n_sqlite} chunks
  udaypur_kb         {n_chroma} vectors, {dim}-d

## Restore

Fast (same chroma version):
    cp kb3/backup/phase4-{stamp}/kb_active.sqlite        kb3/kb_active.sqlite
    rm -rf kb3/chroma && cp -r kb3/backup/phase4-{stamp}/chroma kb3/chroma
    cp kb3/backup/phase4-{stamp}/config/*.yaml           (to their original paths)

Portable (if the chroma directory will not open):
    rebuild the collection from udaypur_kb.rows.jsonl and udaypur_kb.vectors.npy;
    row order in the two files matches.

Verify this backup at any time:
    python phase4_backup.py --verify-only kb3/backup/phase4-{stamp}
"""
    (out / "README.md").write_text(readme, encoding="utf-8")

    ok = verify(out, manifest)
    print(f"\ntotal {human(sum(p.stat().st_size for p in out.rglob('*') if p.is_file()))} "
          f"in {time.time()-t0:.0f}s")
    print("RESULT:", "BACKUP VERIFIED" if ok else "BACKUP FAILED VERIFICATION — do not proceed")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
