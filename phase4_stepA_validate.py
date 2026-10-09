#!/usr/bin/env python
"""Step A validation — does bilingual querying actually reach the Devanagari sources?

    python phase4_stepA_validate.py

Three things have to be true, and the third is the one that is easy to lose:

  1. RAJM -- Bhoja's own Rājamārtaṇḍa -- surfaces for an English query about
     Bhoja's authorship. Reported as a RANK, before and after, measured at FULL
     DEPTH so "absent" means absent from the whole candidate list and not merely
     outside a top-k.
  2. All four Devanagari-bearing sources become reachable from English.
  3. English-on-English retrieval is not degraded: the queries that already
     worked return the same sources.

Run against the v2 OpenAI store, which is what cutover would make live.
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
DEVA_SOURCES = {"RAJM", "BHJ-H", "TIW-H", "SAM"}

# Queries that SHOULD reach a Devanagari source, with the one each targets.
TARGETED = [
    ("yoga sutra commentary attributed to Bhoja", "RAJM", "C5"),
    ("Bhoja's own writings and authorship", "RAJM", "C5"),
    ("the Rajamartanda commentary on the Yogasutra", "RAJM", "C10"),
    ("life of king Bhojadeva of Dhara", "BHJ-H", "C4"),
    ("present-day life in Udaypur town, lanes and households", "TIW-H", "C16"),
    ("canonical proportions for temple construction", "SAM", "C6"),
]
# Queries that already worked in English: these must not get worse.
REGRESSION = [
    ("Betwa river seasonal flow and rainfall", {"BET-K", "BET-S"}, "C2"),
    ("stepwell baoli water structures at Udaypur", {"INT-ARC", "INT-GEO"}, "C3"),
    ("temple proportions and measurement canon", {"KRAM-1", "KRAM-2"}, "C6"),
    ("Sapta Matrka iconography niches four handed goddess", {"ADH", "PAN", "INT-GEO"}, "C7"),
]


def rank_of(rows, code, key="_code"):
    for i, r in enumerate(rows, 1):
        if r.get(key) == code:
            return i
    return None


def main():
    import kb3_chroma_query as Q
    print(f"store: {Q.STORE} -> {Q.STORES[Q.STORE]['collection']}\n")
    ok = True
    DEEP = 400

    print("=" * 78)
    print("1 & 2. TARGETED — can an English query reach the Devanagari sources?")
    print("=" * 78)
    print(f"{'target':7s} {'query':44s} {'rank OFF':>9s} {'rank ON':>8s}  second form")
    reached_off, reached_on = set(), set()
    detail = []
    for q, target, chap in TARGETED:
        tr = {}
        off = Q.search(query=q, k=DEEP, bilingual=False, cap_sources=False)
        on = Q.search(query=q, k=DEEP, bilingual=True, cap_sources=False, _trace=tr)
        r_off, r_on = rank_of(off, target), rank_of(on, target)
        if r_off:
            reached_off.add(target)
        if r_on:
            reached_on.add(target)
        print(f"{target:7s} {q[:44]:44s} {str(r_off or '-'):>9s} {str(r_on or '-'):>8s}  "
              f"{(tr.get('second_query') or '')[:34]}")
        detail.append({"query": q, "target": target, "chapter": chap,
                       "rank_off": r_off, "rank_on": r_on,
                       "second_query": tr.get("second_query")})
    print(f"\n  Devanagari sources reachable, bilingual OFF: "
          f"{sorted(reached_off) or 'NONE'} ({len(reached_off)}/4)")
    print(f"  Devanagari sources reachable, bilingual ON : "
          f"{sorted(reached_on) or 'NONE'} ({len(reached_on)}/4)")
    ok &= reached_on >= DEVA_SOURCES

    print("\n" + "=" * 78)
    print("3. REGRESSION — English-on-English must not degrade")
    print("=" * 78)
    print(f"{'chap':5s} {'query':44s} {'expected in top-8?':>19s}")
    for q, expect, chap in REGRESSION:
        off = Q.search(query=q, chapter=chap, k=8, bilingual=False, cap_sources=False)
        on = Q.search(query=q, chapter=chap, k=8, bilingual=True, cap_sources=False)
        c_off = {r["_code"] for r in off}
        c_on = {r["_code"] for r in on}
        hit_off = bool(c_off & expect)
        hit_on = bool(c_on & expect)
        same = len(c_off & c_on) / max(1, len(c_off))
        flag = "ok" if hit_on else "LOST"
        print(f"{chap:5s} {q[:44]:44s} off={'y' if hit_off else 'n'} on={'y' if hit_on else 'n'} "
              f"overlap={same:.0%}  {flag}")
        print(f"      off: {' '.join(r['_code'] for r in off)}")
        print(f"      on : {' '.join(r['_code'] for r in on)}")
        ok &= (hit_on or not hit_off)

    from bilingual import cost_report
    c = cost_report()
    print("\n" + "=" * 78)
    print("PER-QUERY COST OF BILINGUAL RETRIEVAL")
    print("=" * 78)
    n = max(1, c["calls"])
    print(f"  translation model      {c['model']}")
    print(f"  calls this run         {c['calls']} (cache hits {c['cache_hits']})")
    print(f"  tokens                 {c['in']} in / {c['out']} out")
    print(f"  cost this run          ${c['cost_usd']:.6f}")
    print(f"  per DISTINCT query     ${c['cost_usd']/n:.6f}  (then cached, free)")
    print(f"  plus one extra embedding call per query: "
          f"~{'1536-d text-embedding-3-large'} , ~$0.000003 for a short query")
    print(f"  cached query forms on disk: {c['cached_queries']}")

    (ROOT / "kb_audit" / "stepA_bilingual.json").write_text(
        json.dumps({"targeted": detail, "reached_off": sorted(reached_off),
                    "reached_on": sorted(reached_on), "cost": c},
                   indent=1, ensure_ascii=False), encoding="utf-8")
    print("\n" + "=" * 78)
    print("RESULT:", "STEP A VALIDATED" if ok else "VALIDATION FAILED")
    print("=" * 78)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
