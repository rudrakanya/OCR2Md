#!/usr/bin/env python
"""Step 1 validation — prove the 50 fabricated ADH rows are unreachable.

    python phase4_step1_validate.py

Four readers matter, and they consult different things, so each is tested
against the actual store rather than inferred from the flag:

  A. build_chroma.meta_of   what a REBUILD would emit for these rows. This is
                            the one that decides whether Step 2 re-admits them.
  B. Chroma retrieval       chapter-scoped reads for C7 and C10.
  C. sqlite-direct readers  a bucket/fact query straight off the chunk table.
  D. the sourcebook path    build_sourcebook's own filter predicate.

A control chunk of genuine ADH prose is carried through every test, because a
quarantine that also silences real evidence is a different bug, not a fix.
"""
from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
SQLITE = ROOT / "kb3" / "kb_active.sqlite"
CONTROL = "adhikari-2013-un-00143"      # genuine prose: DECORATIVE MOTIFS paragraph

FAB = """parent_source_id='adhikari-2013-un'
         and (text like '%Island | Attribution%' or text like '%rāhīna%'
              or text like '%Jñābhadras%')"""


def main():
    db = sqlite3.connect(f"file:{SQLITE}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    fab = list(db.execute(f"select * from chunks where {FAB} order by chunk_id"))
    ctl = db.execute("select * from chunks where chunk_id=?", (CONTROL,)).fetchone()
    fab_ids = {r["chunk_id"] for r in fab}
    ok = True

    print("=" * 70)
    print("STEP 1 VALIDATION")
    print("=" * 70)
    print(f"fabricated rows: {len(fab)} | control (genuine prose): {CONTROL}")

    # ---- flags actually written -------------------------------------------
    q = sum(1 for r in fab if r["is_quarantined"] == 1)
    wr = sum(1 for r in fab if (r["quarantine_reason"] or "").startswith("vision-model fabrication"))
    print(f"\nflags: is_quarantined=1 on {q}/{len(fab)} | "
          f"quarantine_reason set on {wr}/{len(fab)}")
    ok &= (q == len(fab) == wr)
    total_q = db.execute("select count(*) from chunks where is_quarantined=1").fetchone()[0]
    print(f"       quarantined in the whole store: {total_q} "
          f"({'only these 50 — no collateral' if total_q == len(fab) else 'OTHERS TOO'})")
    ok &= total_q == len(fab)
    print(f"       control still clean: is_quarantined={ctl['is_quarantined']}, "
          f"reason={ctl['quarantine_reason']}")
    ok &= not ctl["is_quarantined"]

    # ---- A. what a rebuild would emit --------------------------------------
    print("\n--- A. build_chroma.meta_of (what Step 2's rebuild would write) ---")
    import build_chroma
    bad = 0
    for r in fab:
        m = build_chroma.meta_of(r, archived=False)
        buckets = [k for k in m if k.startswith("in_") and m[k]]
        if not (m["is_archived"] and m["is_quotable"] is False and not buckets):
            bad += 1
    sample = build_chroma.meta_of(fab[0], archived=False)
    print(f"   is_archived  : {sample['is_archived']}")
    print(f"   is_quotable  : {sample['is_quotable']}")
    print(f"   chapter buckets emitted: "
          f"{[k for k in sample if k.startswith('in_') and sample[k]] or 'NONE'}")
    print(f"   rows failing the rule: {bad}/{len(fab)}")
    ok &= bad == 0

    mc = build_chroma.meta_of(ctl, archived=False)
    cb = [k for k in mc if k.startswith("in_") and mc[k]]
    print(f"   CONTROL -> archived={mc['is_archived']}, quotable={mc['is_quotable']}, "
          f"buckets={len(cb)} ({', '.join(sorted(cb)[:6])}{'...' if len(cb) > 6 else ''})")
    ok &= (not mc["is_archived"]) and mc["is_quotable"] and bool(cb)

    # ---- B. live Chroma retrieval ------------------------------------------
    print("\n--- B. Chroma retrieval (live collection) ---")
    import chromadb
    col = chromadb.PersistentClient(path=str(ROOT / "kb3" / "chroma")).get_collection("udaypur_kb")
    present = col.get(ids=sorted(fab_ids), include=[])["ids"]
    print(f"   of the 50, vectors present in udaypur_kb: {len(present)}")
    ok &= len(present) == 0
    from kb3_chroma_query import search
    for chap in ("C7", "C10"):
        hits = search(query="temple sculpture iconography attributes of the goddess",
                      chapter=chap, k=60)
        got = [h for h in hits if h.get("chunk_id") in fab_ids]
        adh = [h for h in hits if h.get("parent_source_id") == "adhikari-2013-un"]
        print(f"   {chap}: top-60 -> {len(got)} fabricated, "
              f"{len(adh)} legitimate ADH chunks still retrievable")
        ok &= len(got) == 0

    # ---- C. sqlite-direct readers ------------------------------------------
    print("\n--- C. sqlite-direct bucket/fact read ---")
    for chap in ("C7", "C10"):
        naive = db.execute(
            f"""select count(*) from chunks
                where parent_source_id='adhikari-2013-un'
                  and chapter_buckets like '%{chap}%' and claim_bearing=1""").fetchone()[0]
        gated = db.execute(
            f"""select count(*) from chunks
                where parent_source_id='adhikari-2013-un'
                  and chapter_buckets like '%{chap}%' and claim_bearing=1
                  and is_quarantined=0""").fetchone()[0]
        print(f"   {chap}: claim-bearing ADH rows — ungated {naive}, "
              f"gated on is_quarantined=0 -> {gated} (excludes {naive - gated})")
        ok &= (naive - gated) > 0

    # ---- D. the sourcebook predicate ---------------------------------------
    print("\n--- D. build_sourcebook filter predicate ---")
    import build_sourcebook as bs
    # it drops a row when is_archived or the source is synthetic
    kept = 0
    for r in fab:
        m = build_chroma.meta_of(r, archived=False)
        if not (m.get("is_archived") or m.get("parent_source_id") in bs.SYNTHETIC):
            kept += 1
    print(f"   fabricated rows that would survive the sourcebook filter: {kept}/{len(fab)}")
    ok &= kept == 0
    mkept = not (mc.get("is_archived") or mc.get("parent_source_id") in bs.SYNTHETIC)
    print(f"   CONTROL survives the sourcebook filter: {mkept}")
    ok &= mkept

    # ---- E. kb3_query, the drafting retrieval path -------------------------
    # Tested at FULL depth on purpose. A shallow top-k proves nothing here: the
    # fabricated rows always ranked low, so k=80 showed zero of them while 49
    # were still reachable from a C7 bucket read.
    print("\n--- E. kb3_query.search (the drafting path), full depth ---")
    import kb3_query
    for chap, expect_adh in (("C7", 182), ("C10", None)):
        hits = kb3_query.search(chapter=chap, k=100000)
        ids = [h.get("chunk_id") for h in hits]
        got = len(set(ids) & fab_ids)
        adh = sum(1 for i in ids if i and i.startswith("adhikari"))
        in_sqlite = db.execute(
            f"""select count(*) from chunks where parent_source_id='adhikari-2013-un'
                and chapter_buckets like '%"{chap}%' and is_quarantined=0""").fetchone()[0]
        print(f"   {chap}: {len(hits)} candidates | fabricated {got} | "
              f"legitimate ADH {adh} (sqlite says {in_sqlite})")
        ok &= got == 0 and adh == in_sqlite

    print("\n" + "=" * 70)
    print("RESULT:", "STEP 1 VALIDATED" if ok else "VALIDATION FAILED")
    print("=" * 70)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
