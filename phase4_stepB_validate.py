#!/usr/bin/env python
"""Step B validation — does the source cap break SAM's grip without losing evidence?

    python phase4_stepB_validate.py

The vector map measured SAM as the top source in all sixteen chapter buckets at
26-38%, and overall source purity at 80.7%: the space is organised by book, so a
chapter drafted straight from retrieval gets written out of one treatise.

The cap must do two things and not a third:
  * bring the dominant source down to its configured share,
  * let other sources surface in the space that frees up,
  * and NOT lose evidence -- a capped chunk is demoted to the tail, so it stays
    in the candidate list and stays citable. That is checked explicitly.
"""
from __future__ import annotations

import collections
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("KB_STORE", "v2-openai")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
CASES = [
    ("C2", "the Betwa river, its seasons and the land around Udaypur"),
    ("C3", "water structures, tanks and stepwells"),
    ("C7", "sculpture and iconography on the temple exterior"),
    ("C6", "the form of the temple superstructure"),
]


def shares(rows, k):
    c = collections.Counter(r["_code"] for r in rows[:k])
    return c, {s: n / max(1, min(k, len(rows))) for s, n in c.items()}


def main():
    import kb3_chroma_query as Q
    from bilingual import config
    cfg = config()["source_cap"]
    print(f"store: {Q.STORE} -> {Q.STORES[Q.STORE]['collection']}")
    print(f"caps: default {cfg['default']}, per_chapter {cfg.get('per_chapter')}")
    print(f"      per_source {cfg.get('per_source')}\n")
    ok = True
    K = 20
    out = []

    for chap, q in CASES:
        off = Q.search(query=q, chapter=chap, k=K, cap_sources=False)
        on = Q.search(query=q, chapter=chap, k=K, cap_sources=True)
        c_off, s_off = shares(off, K)
        c_on, s_on = shares(on, K)
        top_off = c_off.most_common(1)[0] if c_off else ("-", 0)
        limit = float((cfg.get("per_chapter") or {}).get(chap, cfg["default"]))
        per_src = ((cfg.get("per_source") or {}).get(chap) or {})

        print("=" * 78)
        print(f"{chap}  ·  {q}")
        print(f"  cap for this chapter: {limit:.0%}"
              + (f"  (per-source: {per_src})" if per_src else ""))
        print(f"  OFF: {' '.join(r['_code'] for r in off)}")
        print(f"  ON : {' '.join(r['_code'] for r in on)}")
        print(f"  top source OFF: {top_off[0]} {top_off[1]}/{K} = {top_off[1]/K:.0%}"
              f"   ON: {c_on.most_common(1)[0][0]} "
              f"{c_on.most_common(1)[0][1]}/{K} = {c_on.most_common(1)[0][1]/K:.0%}")
        print(f"  distinct sources  OFF {len(c_off)}  ->  ON {len(c_on)}")
        new = sorted(set(c_on) - set(c_off))
        print(f"  sources that surfaced because of the cap: {new or 'none'}")

        # every capped source must respect its ceiling
        for code, n in c_on.items():
            cap = float(per_src.get(code, limit))
            allowed = max(1, int(round(cap * K)))
            if n > allowed:
                print(f"  !! {code} has {n} of {K}, above its ceiling {allowed}")
                ok = False

        # nothing lost: everything in the uncapped top-K must still be SOMEWHERE
        full_on = Q.search(query=q, chapter=chap, k=5000, cap_sources=True)
        ids_on = {r["chunk_id"] for r in full_on}
        missing = [r["chunk_id"] for r in off if r["chunk_id"] not in ids_on]
        print(f"  chunks from the uncapped top-{K} still present in the capped "
              f"candidate list: {K - len(missing)}/{K}"
              + (f"  MISSING {missing}" if missing else "  (none lost)"))
        ok &= not missing
        out.append({"chapter": chap, "query": q, "cap": limit,
                    "off": dict(c_off), "on": dict(c_on), "new_sources": new,
                    "lost": missing})

    (ROOT / "kb_audit" / "stepB_source_cap.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print("\n" + "=" * 78)
    print("RESULT:", "STEP B VALIDATED" if ok else "VALIDATION FAILED")
    print("=" * 78)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
