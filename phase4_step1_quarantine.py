#!/usr/bin/env python
"""Step 1 — quarantine ADH's 50 vision-model-fabricated table rows.

    python phase4_step1_quarantine.py --dry-run
    python phase4_step1_quarantine.py --apply
    python phase4_step1_quarantine.py --undo kb_audit/phase4_step1_undo.json

These 50 chunks are the page-25 repetition collapse: three distinct texts (one
repeated 45 times) carrying invented iconography -- Vārāhī as "Vāraṇi", every
hand attribute overwritten with the non-word "(rāhīna)". They are marked
`factual` and claim-bearing, and they have no vectors, so retrieval cannot reach
them; but any tool reading the sqlite chunk table treats them as evidence.

WHICH FIELD ACTUALLY GATES THEM
-------------------------------
Setting `is_quarantined` alone would be a flag that looks right and changes
nothing downstream. `build_chroma.meta_of` derives quotability from
`quarantine_reason is None` -- not from `is_quarantined` -- and it excludes
model-written text from retrieval by ARCHIVING it and emitting NO chapter
buckets, because (its own comment) the query layer filters on `in_<chapter>`,
not on the archive flag. So this writes:

    is_quarantined   = 1      honoured by stage2_build and kb3_quarantine
    quarantine_reason= <why>  drives is_quotable=False in build_chroma
    review_status    = ...    audit trail

and `phase4_patch_build_chroma.py` teaches build_chroma to treat a quarantined
row the way it already treats synthetic text: archived, un-bucketed, unquotable.
Both halves are needed; either alone leaves a hole.

Reversible: the rows are never deleted, and every field this touches is written
to an undo file first.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import date
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
SQLITE = ROOT / "kb3" / "kb_active.sqlite"
UNDO = ROOT / "kb_audit" / "phase4_step1_undo.json"

REASON = ("vision-model fabrication - ADH page 25 iconographic table collapse: "
          "the extractor emitted this table header 205 times and one invented row "
          "45 times; deity names and hand attributes are not on the page "
          "(Vārāhī->Vāraṇi, akṣamālā/triśūla->'(rāhīna)'). Phase 4 Step 1, "
          f"{date.today().isoformat()}. See EXTRACTION_FAILURES.md §1.")
REVIEW = "quarantined-phase4-step1"

SELECT = """select chunk_id, is_quarantined, quarantine_reason, review_status,
                   epistemic_status, claim_bearing, chapter_buckets, text
            from chunks
            where parent_source_id='adhikari-2013-un'
              and (text like '%Island | Attribution%' or text like '%rāhīna%'
                   or text like '%Jñābhadras%')
            order by chunk_id"""


def select_rows(db):
    return list(db.execute(SELECT))


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--undo")
    a = ap.parse_args()

    if a.undo:
        prev = json.loads(Path(a.undo).read_text(encoding="utf-8"))
        db = sqlite3.connect(str(SQLITE))
        with db:
            for r in prev["rows"]:
                db.execute("""update chunks set is_quarantined=?, quarantine_reason=?,
                                     review_status=? where chunk_id=?""",
                           (r["is_quarantined"], r["quarantine_reason"],
                            r["review_status"], r["chunk_id"]))
        n = db.execute("""select count(*) from chunks where is_quarantined=1
                          and parent_source_id='adhikari-2013-un'""").fetchone()[0]
        db.close()
        print(f"restored {len(prev['rows'])} rows; ADH quarantined now {n}")
        return 0

    db = sqlite3.connect(f"file:{SQLITE}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    rows = select_rows(db)
    distinct = {r["text"] for r in rows}
    print(f"matched {len(rows)} chunks, {len(distinct)} distinct texts")
    print(f"already quarantined: {sum(1 for r in rows if r['is_quarantined'])}")

    # Ground truth guard: refuse to touch anything that reads like real prose.
    suspect = [r["chunk_id"] for r in rows
               if r["text"].count(". ") >= 2 and r["text"].count("|") < 6]
    if suspect:
        print("REFUSING: these look like genuine prose, not collapsed table rows:")
        for s in suspect:
            print("   ", s)
        return 1
    if len(rows) != 50:
        print(f"REFUSING: expected 50 chunks, matched {len(rows)}. "
              "The audit identified exactly 50; investigate before writing.")
        return 1
    db.close()

    if a.dry_run:
        print("\nwould set on all 50:")
        print(f"  is_quarantined   = 1")
        print(f"  quarantine_reason= {REASON[:90]}...")
        print(f"  review_status    = {REVIEW}")
        print("\nchunk_ids:", ", ".join(r["chunk_id"] for r in rows[:4]), "...",
              rows[-1]["chunk_id"])
        return 0

    # --- write, undo file first -------------------------------------------
    UNDO.write_text(json.dumps({
        "created": date.today().isoformat(),
        "step": "phase4 step1 ADH quarantine",
        "restore_with": f"python phase4_step1_quarantine.py --undo {UNDO.as_posix()}",
        "rows": [{"chunk_id": r["chunk_id"], "is_quarantined": r["is_quarantined"],
                  "quarantine_reason": r["quarantine_reason"],
                  "review_status": r["review_status"]} for r in rows],
    }, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"\nundo file written: {UNDO}")

    w = sqlite3.connect(str(SQLITE))
    ids = [r["chunk_id"] for r in rows]
    with w:
        w.executemany("""update chunks set is_quarantined=1, quarantine_reason=?,
                                review_status=? where chunk_id=?""",
                      [(REASON, REVIEW, i) for i in ids])
    after = w.execute("""select count(*) from chunks where is_quarantined=1
                         and quarantine_reason like 'vision-model fabrication%'""").fetchone()[0]
    total_q = w.execute("select count(*) from chunks where is_quarantined=1").fetchone()[0]
    w.close()
    print(f"applied: {after} rows now carry the fabrication quarantine "
          f"({total_q} quarantined in the whole store)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
