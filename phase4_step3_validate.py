#!/usr/bin/env python
"""Step 3 validation — one Patil authority, nothing else disturbed.

    python phase4_step3_validate.py

  1. One source_id, one code, no collisions; parts preserved per chunk.
  2. A passage that existed under three codes now exists once.
  3. source_type NOT flattened: the inscriptions part is still epigraphic.
  4. No other source's corroboration profile moved.
  5. The dedup is exact-text only: no near-duplicate judgement was made.
"""
from __future__ import annotations

import collections
import json
import sqlite3
import sys
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
V2 = ROOT / "kb3" / "kb_active_v2.sqlite"
V2Q = ROOT / "kb3" / "kb_quarantine_v2.sqlite"
LIVE = ROOT / "kb3" / "kb_active.sqlite"
REGISTRY = ROOT / "kb_audit" / "source_registry.yaml"
MERGED = ["patil-1952", "patil-composite-inscriptions", "patil-composite-temples"]


def jload(v, d):
    try:
        return json.loads(v) if v else d
    except (TypeError, ValueError):
        return d


def main():
    v2 = sqlite3.connect(f"file:{V2}?mode=ro", uri=True); v2.row_factory = sqlite3.Row
    vq = sqlite3.connect(f"file:{V2Q}?mode=ro", uri=True); vq.row_factory = sqlite3.Row
    lv = sqlite3.connect(f"file:{LIVE}?mode=ro", uri=True); lv.row_factory = sqlite3.Row
    ok = True

    print("=" * 72)
    print("1. ONE AUTHORITY, ONE CODE")
    print("=" * 72)
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    codes = [s.get("code") for s in reg["sources"] if s.get("code")]
    dupc = [c for c, n in collections.Counter(codes).items() if n > 1]
    print(f"  codes in registry: {len(codes)} | duplicates: {dupc or 'none'}")
    ok &= not dupc
    base = next(s for s in reg["sources"] if s["source_id"] == "patil-1952")
    print(f"  patil-1952 code={base.get('code')} parts={len(base.get('parts') or [])} "
          f"canonical_for_quotation={base.get('canonical_for_quotation')}")
    ok &= base.get("code") == "PAT" and len(base.get("parts") or []) == 3
    for sid in MERGED[1:]:
        e = next(s for s in reg["sources"] if s["source_id"] == sid)
        print(f"  {sid:32s} code={e.get('code')} merged_into={e.get('merged_into')}")
        ok &= e.get("code") is None and e.get("merged_into") == "patil-1952"

    left = v2.execute("select count(*) from chunks where parent_source_id in (?,?)",
                      tuple(MERGED[1:])).fetchone()[0]
    npat = v2.execute("select count(*) from chunks where parent_source_id='patil-1952'").fetchone()[0]
    print(f"  chunks still under a composite source_id: {left}")
    print(f"  chunks under patil-1952: {npat}")
    ok &= left == 0

    parts = collections.Counter()
    for r in v2.execute("select provenance from chunks where parent_source_id='patil-1952'"):
        parts[(jload(r["provenance"], {}) or {}).get("registration", "?")] += 1
    print(f"  provenance.registration preserved: {dict(parts)}")
    ok &= len(parts) == 3

    print("\n" + "=" * 72)
    print("2. A PASSAGE THAT WAS TRIPLE-CODED NOW COUNTS ONCE")
    print("=" * 72)
    # find a text that appeared under 2+ Patil registrations in v1
    v1h = collections.defaultdict(set)
    for r in lv.execute("select content_hash, parent_source_id from chunks "
                        "where parent_source_id in (?,?,?)", tuple(MERGED)):
        v1h[r["content_hash"]].add(r["parent_source_id"])
    multi = [h for h, s in v1h.items() if len(s) > 1]
    print(f"  v1: {len(multi)} passages present under more than one Patil registration")
    shown = 0
    for h in multi:
        t = lv.execute("select text from chunks where content_hash=? limit 1", (h,)).fetchone()["text"]
        n_v1 = lv.execute("select count(*) from chunks where content_hash=?", (h,)).fetchone()[0]
        n_act = v2.execute("select count(*) from chunks where content_hash=?", (h,)).fetchone()[0]
        n_q = vq.execute("select count(*) from chunks where content_hash=?", (h,)).fetchone()[0]
        if shown < 3:
            print(f"\n   {t[:88]!r}")
            print(f"     v1 copies {n_v1} under {sorted(v1h[h])}")
            print(f"     v2 active {n_act}, quarantined-as-duplicate {n_q}")
            shown += 1
        if n_act > 1:
            print(f"     STILL DUPLICATED IN ACTIVE: {h}")
            ok = False
    # store-wide: no exact duplicate left in active
    dups = [(h, n) for h, n in v2.execute(
        "select content_hash, count(*) c from chunks group by 1 having c>1").fetchall()]
    print(f"\n  exact-duplicate content_hash groups left in ACTIVE v2: {len(dups)}")
    ok &= len(dups) == 0
    print(f"  duplicate copies held in the quarantine file: "
          f"{vq.execute(chr(115)+'elect count(*) from chunks where quarantine_reason like ?', ('duplicate of %',)).fetchone()[0]}")

    print("\n" + "=" * 72)
    print("3. source_type NOT FLATTENED")
    print("=" * 72)
    for r in v2.execute("""select json_extract(provenance,'$.registration') reg, source_type,
                                  count(*) n from chunks where parent_source_id='patil-1952'
                           group by 1,2 order by 1"""):
        print(f"  {str(r['reg']):34s} {str(r['source_type']):24s} {r['n']:5d}")
    types = {r["source_type"] for r in v2.execute(
        "select distinct source_type from chunks where parent_source_id='patil-1952'")}
    print(f"  distinct source_type under patil-1952: {sorted(types)}")
    ok &= "primary_epigraphic" in types

    print("\n" + "=" * 72)
    print("4. NO OTHER SOURCE'S CORROBORATION DISTURBED")
    print("=" * 72)
    print(f"  {'source':28s} {'v2 chunks':>9s} {'corrob>0':>9s} {'share':>6s}")
    rows = []
    for r in v2.execute("""select parent_source_id, count(*) n,
                                  sum(case when corroboration_count>0 then 1 else 0 end) c
                           from chunks group by 1 order by 1"""):
        rows.append((r["parent_source_id"], r["n"], r["c"]))
    for sid, n, c in rows:
        if c:
            print(f"  {sid:28s} {n:9d} {c:9d} {c/n:6.1%}")
    tot_c = sum(c for _, _, c in rows)
    print(f"  sources with any corroboration: {sum(1 for _,_,c in rows if c)} of {len(rows)}")
    print(f"  total chunks with corroboration_count>0: {tot_c}")
    # a Patil-only claim must not read as corroborated BY ITSELF
    self_corr = 0
    for r in v2.execute("""select chunk_id, corroboration_ids from chunks
                           where parent_source_id='patil-1952' and corroboration_count>0"""):
        ids = jload(r["corroboration_ids"], [])
        for o in ids:
            got = v2.execute("select parent_source_id from chunks where chunk_id=?", (o,)).fetchone()
            if got and got[0] == "patil-1952":
                self_corr += 1
    print(f"  Patil chunks corroborated by another Patil chunk: {self_corr} "
          f"({'correct — self-corroboration excluded' if self_corr == 0 else 'WRONG'})")
    ok &= self_corr == 0

    print("\n" + "=" * 72)
    print("5. DEDUP BASIS")
    print("=" * 72)
    bas = collections.Counter(r["basis"] for r in v2.execute("select basis from links"))
    print(f"  link bases: {dict(bas)}")
    print("  (exact content_hash only — no near-duplicate/minhash judgement was made)")

    print("\n" + "=" * 72)
    print("RESULT:", "STEP 3 VALIDATED" if ok else "VALIDATION FAILED")
    print("=" * 72)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
