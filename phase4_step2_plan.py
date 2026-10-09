#!/usr/bin/env python
"""Step 2 planning — how much of a re-chunk is actually new?

    python phase4_step2_plan.py

Re-chunking moves chunk boundaries, so the per-chunk classifications in the live
store (epistemic_status, relevance_tags, chapter scores -- all from a paid Stage 1
pass) cannot be copied by chunk_id. They have to be inherited by CONTENT.

This measures, per source, how many fresh chunks are byte-identical to a live one
(`content_hash` = sha1(text)[:16], the same function stage2_build uses). Those
inherit their labels exactly and reuse their existing vector for free. The rest
need label inheritance by overlap, and a local embed.

Reads only. No writes, no model, no API.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
import sys
import types
from pathlib import Path

import yaml

# build_kb imports the Mistral client at module scope; only its chunker is used
# here and no API is called, so the module is stubbed rather than installed.
for _n in ("mistralai", "mistralai.client"):
    sys.modules.setdefault(_n, types.ModuleType(_n))
sys.modules["mistralai.client"].Mistral = object
sys.modules["mistralai"].Mistral = object

import build_kb  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
BOOKS = ROOT / "Udaypur Reference Markdown Files"
REGISTRY = ROOT / "kb_audit" / "source_registry.yaml"
SQLITE = ROOT / "kb3" / "kb_active.sqlite"
OUT = ROOT / "kb_audit" / "step2_plan.json"


def h(t):
    return hashlib.sha1(t.encode()).hexdigest()[:16]


def main():
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    sources = [s for s in reg["sources"] if (BOOKS / s.get("file", "")).exists()]

    db = sqlite3.connect(f"file:{SQLITE}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    live = {}
    for r in db.execute("select parent_source_id, content_hash from chunks"):
        live.setdefault(r["parent_source_id"], set()).add(r["content_hash"])

    import chromadb
    col = chromadb.PersistentClient(path=str(ROOT / "kb3" / "chroma")).get_collection("udaypur_kb")
    have_vec = set(col.get(limit=200000, include=[])["ids"])

    print(f"{'code':9s} {'v1':>6s} {'v2':>6s} {'delta':>6s} {'same':>6s} "
          f"{'new':>5s} {'reuse vec':>9s}")
    rows, tot_v1, tot_v2, tot_same, tot_new, tot_reuse = [], 0, 0, 0, 0, 0
    for s in sources:
        sid, code = s["source_id"], s.get("code", "?")
        fresh = build_kb.chunk_markdown(BOOKS / s["file"])
        fh = [h(c["text"]) for c in fresh]
        lh = live.get(sid, set())
        same = sum(1 for x in fh if x in lh)
        new = len(fh) - same
        reuse = sum(1 for x in fh if f"{x}-{sid}" in have_vec)
        rows.append({"code": code, "source_id": sid, "v1": len(lh), "v2": len(fresh),
                     "same": same, "new": new, "reuse_vectors": reuse})
        tot_v1 += len(lh); tot_v2 += len(fresh); tot_same += same
        tot_new += new; tot_reuse += reuse
        print(f"{code:9s} {len(lh):6d} {len(fresh):6d} {len(fresh)-len(lh):+6d} "
              f"{same:6d} {new:5d} {reuse:9d}")

    print(f"\n{'TOTAL':9s} {tot_v1:6d} {tot_v2:6d} {tot_v2-tot_v1:+6d} "
          f"{tot_same:6d} {tot_new:5d} {tot_reuse:9d}")
    print(f"\nfresh chunks byte-identical to a live chunk : {tot_same}/{tot_v2} "
          f"({tot_same/tot_v2:.1%})")
    print(f"fresh chunks whose vector can be reused     : {tot_reuse}/{tot_v2} "
          f"({tot_reuse/tot_v2:.1%})")
    print(f"fresh chunks needing a local embed          : {tot_v2-tot_reuse}")
    print(f"  at the measured 17.5 chunks/s             ≈ "
          f"{(tot_v2-tot_reuse)/17.5/60:.1f} min")
    OUT.write_text(json.dumps({"rows": rows, "totals": {
        "v1": tot_v1, "v2": tot_v2, "same": tot_same, "new": tot_new,
        "reuse_vectors": tot_reuse}}, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
