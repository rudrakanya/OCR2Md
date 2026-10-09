#!/usr/bin/env python
"""Step 2 planning, part 2 — can every v2 chunk inherit its labels?

    python phase4_step2_overlap.py

Only 3.2% of fresh chunks are byte-identical to a live one, so labels have to be
inherited by CONTENT overlap, not by id. This measures how well that will work,
per source, before anything is built:

    full      >=60% of the chunk's shingles map to live chunks -> inherit safely
    partial   some overlap -> inherit, but the chunk also holds new text
    orphan    no overlap at all -> nothing to inherit from

Orphans are expected and are the point of the exercise: the 362 recovered table
rows never existed as live chunks. The question is whether they are a handful
needing a documented conservative default, or a large fraction.

Shingles (40 chars, stride 20) rather than offsets, because the old pipeline
cleaned text slightly differently and absolute positions do not line up.

Reads only. Processes one source at a time to stay inside this machine's memory.
"""
from __future__ import annotations

import collections
import json
import re
import sqlite3
import sys
import types
import unicodedata
from pathlib import Path

import yaml

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
OUT = ROOT / "kb_audit" / "step2_overlap.json"

W, STRIDE = 32, 16


def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s or "")).strip().lower()


def ref_index(texts):
    """Every window of the reference text, at stride 1.

    This must be stride 1. Indexing the reference at a stride and querying at the
    same stride looks symmetric and is not: the two texts are cut at different
    boundaries, so sampled offsets never line up and real matches are missed.
    An earlier version of this script did exactly that and reported 64% of fresh
    chunks as orphans, against the 79% mean coverage the Phase 1 reconciliation
    measured. Hashes, not substrings, keep the set small enough to hold.
    """
    idx = set()
    for t in texts:
        n = norm(t)
        for i in range(max(1, len(n) - W + 1)):
            idx.add(hash(n[i:i + W]))
    return idx


def probe_shingles(t, stride=STRIDE):
    """The query side may sample: any window that exists in the reference will be
    found there regardless of where it starts."""
    t = norm(t)
    if len(t) < W:
        return {hash(t)}
    return {hash(t[i:i + W]) for i in range(0, len(t) - W + 1, stride)}


def main():
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    sources = [s for s in reg["sources"] if (BOOKS / s.get("file", "")).exists()]
    db = sqlite3.connect(f"file:{SQLITE}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row

    print(f"{'code':9s} {'v2':>6s} {'full':>6s} {'part':>6s} {'orph':>6s} "
          f"{'orphan chars':>12s}")
    rows, T = [], collections.Counter()
    for s in sources:
        sid, code = s["source_id"], s.get("code", "?")
        idx = ref_index(r["text"] for r in db.execute(
            "select text from chunks where parent_source_id=?", (sid,)))

        fresh = build_kb.chunk_markdown(BOOKS / s["file"])
        full = part = orph = 0
        orph_chars = 0
        orphans = []
        for c in fresh:
            sh = probe_shingles(c["text"])
            hit = sum(1 for x in sh if x in idx)
            frac = hit / max(1, len(sh))
            if frac >= 0.60:
                full += 1
            elif hit:
                part += 1
            else:
                orph += 1
                orph_chars += len(c["text"])
                if len(orphans) < 3:
                    orphans.append(c["text"][:110])
        rows.append({"code": code, "source_id": sid, "v2": len(fresh), "full": full,
                     "partial": part, "orphan": orph, "orphan_chars": orph_chars,
                     "orphan_samples": orphans})
        T["v2"] += len(fresh); T["full"] += full; T["partial"] += part; T["orphan"] += orph
        T["orphan_chars"] += orph_chars
        print(f"{code:9s} {len(fresh):6d} {full:6d} {part:6d} {orph:6d} {orph_chars:12d}")
        del idx

    print(f"\n{'TOTAL':9s} {T['v2']:6d} {T['full']:6d} {T['partial']:6d} {T['orphan']:6d} "
          f"{T['orphan_chars']:12d}")
    print(f"\ninheritable (full or partial): {T['full']+T['partial']}/{T['v2']} "
          f"({(T['full']+T['partial'])/T['v2']:.1%})")
    print(f"orphans needing a default    : {T['orphan']} ({T['orphan']/T['v2']:.2%})")

    print("\n--- what the orphans look like ---")
    for r in rows:
        if r["orphan"]:
            print(f"\n  {r['code']} ({r['orphan']} orphans)")
            for t in r["orphan_samples"]:
                print("     ", repr(t))
    OUT.write_text(json.dumps({"rows": rows, "totals": dict(T)}, indent=1,
                              ensure_ascii=False), encoding="utf-8")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
