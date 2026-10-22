"""Append keep/reject judgments (and extracted items) for a chapter.

stdin: JSON list of
  {"id": <chunk_id prefix or full>, "d": "k"|"r", "why": "...",
   "items": [{"sub":"S1","type":"quote","str":"direct","q":"verbatim","gloss":"","note":"..."}]}
Chunk-id prefixes (>= 8 chars) are expanded against the chapter's hits file.
"""
import json
import sys
from pathlib import Path

RUNS = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "_runs"))
ch = sys.argv[1]
hits = {json.loads(l)["chunk_id"] for l in (RUNS / f"{ch}_hits.jsonl").open(encoding="utf-8")}
jp = RUNS / f"{ch}_judgments.jsonl"
done = set()
if jp.exists():
    done = {json.loads(l)["chunk_id"] for l in jp.open(encoding="utf-8") if l.strip()}
rows = json.loads(sys.stdin.buffer.read().decode("utf-8"))
out_j, out_i, errs = [], [], []
for r in rows:
    m = [h for h in hits if h.startswith(r["id"])]
    if len(m) != 1:
        errs.append(f"{r['id']}: {len(m)} matches")
        continue
    cid = m[0]
    if cid in done:
        # "add": attach further items to a chunk already judged keep (e.g. a
        # passage noticed later as one side of a conflict). Never flips a decision.
        if r.get("add"):
            for it in r.get("items", []):
                out_i.append(dict(it, chunk_id=cid))
        continue
    assert r["d"] in ("k", "r"), r
    if r["d"] == "k" and not r.get("items"):
        errs.append(f"{cid}: keep without items")
        continue
    out_j.append({"chunk_id": cid, "decision": "keep" if r["d"] == "k" else "reject", "reason": r["why"]})
    for it in r.get("items", []):
        assert it["type"] in ("quote", "excerpt", "fact", "figure", "date", "inscription", "architectural detail"), it
        assert it["str"] in ("direct", "contextual"), it
        out_i.append(dict(it, chunk_id=cid))
    done.add(cid)
if errs:
    print("ERRORS (nothing written):", *errs, sep="\n  ")
    sys.exit(1)
with jp.open("a", encoding="utf-8") as fh:
    for j in out_j:
        fh.write(json.dumps(j, ensure_ascii=False) + "\n")
with (RUNS / f"{ch}_items.jsonl").open("a", encoding="utf-8") as fh:
    for i in out_i:
        fh.write(json.dumps(i, ensure_ascii=False) + "\n")
print(f"judged +{len(out_j)} (keep {sum(j['decision']=='keep' for j in out_j)}), items +{len(out_i)}; total judged {len(done)}")
