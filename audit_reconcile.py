#!/usr/bin/env python
"""Job 1 — can the markdown folder still rebuild the knowledge base?

    python audit_reconcile.py

Reconciles three things that are assumed to agree:

    1. the .md files actually in Udaypur Reference Markdown Files/
    2. the 27 sources named in source_registry.yaml
    3. the sources that have chunks in kb_active.sqlite and vectors in udaypur_kb

Identity is resolved BY CONTENT, never by filename: filename similarity already
mis-mapped sources in this project (it matched three different books to
"Some Paramara Templess.pdf" and the Patanjali volume to nothing). For every
source this samples its stored chunks and asks whether that text is present in a
folder file — and if the registry's named file does not contain it, every other
file in the folder is tried before the source is called orphaned.

Two directions matter, and they fail differently:

    store -> folder   content in the KB that no folder file holds. The dangerous
                      class: the folder can no longer rebuild that content.
    folder -> store   text in a folder file that no chunk holds. Un-ingested
                      material: present on disk, invisible to retrieval.

Reads only. No PyMuPDF, so it is safe to run beside the OCR audit.
"""
from __future__ import annotations

import json
import random
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
BOOKS = ROOT / "Udaypur Reference Markdown Files"
REGISTRY = ROOT / "kb_audit" / "source_registry.yaml"
SQLITE = ROOT / "kb3" / "kb_active.sqlite"
DATA = ROOT / "kb_audit" / "folder_reconciliation.json"
SAMPLE = 40            # chunks sampled per source for the store -> folder test
PROBE = 120            # characters of a chunk used as the probe
WINDOW = 1400          # folder text block size for the folder -> store test
BLOCKS = 25            # blocks sampled per file


def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s or "")).strip()


def main():
    random.seed(11)
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    sources = reg["sources"]

    folder_files = {p.name: norm(p.read_text(encoding="utf-8", errors="replace"))
                    for p in sorted(BOOKS.glob("*.md"))}
    print(f"folder: {len(folder_files)} .md files | registry: {len(sources)} sources")

    db = sqlite3.connect(f"file:{SQLITE}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    store_counts = dict(db.execute("select parent_source_id, count(*) from chunks group by 1"))

    import chromadb
    col = chromadb.PersistentClient(path=str(ROOT / "kb3" / "chroma")).get_collection("udaypur_kb")
    vec_counts = {}
    for m in col.get(limit=500000, include=["metadatas"])["metadatas"]:
        vec_counts[m["parent_source_id"]] = vec_counts.get(m["parent_source_id"], 0) + 1

    rows, claimed = [], set()
    for s in sources:
        sid, code, named = s["source_id"], s.get("code", "?"), s.get("file", "")
        texts_all = [r["text"] for r in db.execute(
            "select text from chunks where parent_source_id=?", (sid,))]
        texts = [t for t in texts_all if len(t) > 240]
        picks = random.sample(texts, min(SAMPLE, len(texts))) if texts else []
        probes = [norm(t)[:PROBE] for t in picks if norm(t)[:PROBE]]

        # which folder file actually holds this source's content?
        best, best_hits = None, -1
        for fname, body in folder_files.items():
            hits = sum(1 for p in probes if p in body)
            if hits > best_hits:
                best, best_hits = fname, hits
        coverage = (best_hits / len(probes)) if probes else None
        resolved = best if coverage and coverage >= 0.5 else None
        if resolved:
            claimed.add(resolved)

        # folder -> store, measured with SHINGLES. Fixed-size blocks were the
        # wrong instrument: a block that starts mid-chunk fails the membership
        # test even when the text is fully ingested, which understated coverage
        # badly (BET-S showed 24%). Short shingles at a stride are insensitive
        # to where chunk boundaries happen to fall.
        rev = None
        if resolved:
            body = folder_files[resolved]
            allchunks = norm(" ".join(norm(x) for x in texts_all))
            sh = [body[i:i + 48] for i in range(0, max(1, len(body) - 48), 220)]
            sh = [s for s in sh if len(s.strip()) >= 40]
            if sh:
                sel = random.sample(sh, min(300, len(sh)))
                found = sum(1 for s in sel if s in allchunks)
                rev = round(found / len(sel), 3)

        rows.append({
            "code": code, "source_id": sid, "title": s.get("title", "?"),
            "registry_file": named,
            "file_present": named in folder_files,
            "resolved_file": resolved,
            "name_mismatch": bool(resolved and named and resolved != named),
            "store_chunks": store_counts.get(sid, 0),
            "vectors": vec_counts.get(sid, 0),
            "probes": len(probes),
            "store_to_folder": round(coverage, 3) if coverage is not None else None,
            "folder_to_store": rev,
        })

    unclaimed = sorted(set(folder_files) - claimed)
    out = {"folder_files": len(folder_files), "sources": len(sources),
           "rows": rows, "files_claimed_by_no_source": unclaimed}
    DATA.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"\n{'code':9s} {'file':>5s} {'reg':>4s} {'chunks':>7s} {'vecs':>6s} "
          f"{'store→folder':>13s} {'folder→store':>13s}  verdict")
    for r in rows:
        v = []
        if not r["resolved_file"]:
            v.append("IN KB, NO FOLDER FILE")
        elif not r["file_present"]:
            v.append(f"registry names a missing file; content is in {r['resolved_file']}")
        elif r["name_mismatch"]:
            v.append(f"content actually lives in {r['resolved_file']}")
        if r["store_chunks"] and not r["vectors"]:
            v.append("no vectors")
        if r["folder_to_store"] is not None and r["folder_to_store"] < 0.5:
            v.append(f"only {r['folder_to_store']:.0%} of the file is chunked")
        pct = lambda x: f"{x:.0%}" if x is not None else "-"
        print("{:9s} {:>5s} {:>4s} {:7d} {:6d} {:>13s} {:>13s}  {}".format(
            r["code"], "yes" if r["file_present"] else "NO", "yes",
            r["store_chunks"], r["vectors"],
            pct(r["store_to_folder"]), pct(r["folder_to_store"]),
            "; ".join(v) if v else "ok"))
    if unclaimed:
        print("\nfolder files no source's content resolved to:")
        for f in unclaimed:
            print("  " + f)
    print(f"\nwrote {DATA}")


if __name__ == "__main__":
    main()
