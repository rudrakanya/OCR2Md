"""Reject every still-unjudged hit of one source, with one reason.

Only for use AFTER every chunk of that source has been dumped and read in full;
the dump is the record that it was read. Usage:
  python drafting/_tools/reject_rest.py C01 "<source_path>" "<reason>"
"""
import json
import sys
from pathlib import Path

RUNS = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "_runs"))
ch, source, why = sys.argv[1], sys.argv[2], sys.argv[3]
hits = [json.loads(l) for l in (RUNS / f"{ch}_hits.jsonl").open(encoding="utf-8")]
jp = RUNS / f"{ch}_judgments.jsonl"
done = {json.loads(l)["chunk_id"] for l in jp.open(encoding="utf-8")} if jp.exists() else set()
todo = sorted({h["chunk_id"] for h in hits if h["source_path"] == source} - done)
with jp.open("a", encoding="utf-8") as fh:
    for cid in todo:
        fh.write(json.dumps({"chunk_id": cid, "decision": "reject", "reason": why}, ensure_ascii=False) + "\n")
print(f"{source}: rejected {len(todo)}")
