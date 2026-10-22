"""Print a unit's UNREASONED direct items compactly, for in-session exclusion review (free).
  UDAY_OUTLINE_DIR=wholebook python -I -X utf8 drafting/_tools/unreasoned_dump.py NN [plan_file]
Columns: ID | page | tier | sub | P (named in the chapter plan) / - | 'also' tags | quote (English gloss for Hindi items), 260 chars.
"""
import json
import os
import re
import sys
from pathlib import Path

DR = Path(__file__).resolve().parent.parent
W = DR / "editorial" / os.environ.get("UDAY_OUTLINE_DIR", "plan_v2")
n = sys.argv[1]
plan = Path(sys.argv[2]).read_text(encoding="utf-8") if len(sys.argv) > 2 else ""
cov = json.loads((W / f"coverage_ch{n}.json").read_text(encoding="utf-8"))
q = {json.loads(l)["id"]: json.loads(l) for l in (DR / "evidence_index" / f"ch{n}.jsonl").open(encoding="utf-8")}
for i, s in cov["status"].items():
    if s[0] != "UNREASONED":
        continue
    r = q[i]
    t = r["quote"]
    if "Gloss" in t:
        t = t[t.index("Gloss"):].replace("Gloss [my translation]:*", "").strip()
    t = re.sub(r"\s+", " ", t)
    print(f"{i} | {r['page']} | T{r['tier']} | {r.get('sub')} | {'P' if i in plan else '-'} | {','.join(r.get('also') or [])} | {t[:260]}")
