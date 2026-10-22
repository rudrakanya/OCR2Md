"""Apply the editor's replacements for flagged sentences (in-session fixes; no API).

  set UDAY_CFG=<cfg>; python -I -X utf8 apply_fixes.py <sec> <fixes.json>
fixes.json: {"<sid>": "replacement sentence with its [IDs]" | "CUT", ...}; sids from run/chN/<sec>_verify.json.
Each flagged sentence is matched exactly in run/chN/<sec>.md. A replacement may not introduce an ID that is neither already in
the section nor assigned to it by the plan. Prints what was applied and what could not be matched.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from cfg import C  # noqa: E402
import validate as va  # noqa: E402
import pipeline3 as p3  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
sec, fx = sys.argv[1], json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
RUN = HERE.parent / "run" / f"ch{C.CH}"
f = RUN / f"{sec}.md"
t = f.read_text(encoding="utf-8")
v = json.loads((RUN / f"{sec}_verify.json").read_text(encoding="utf-8"))
rows = {x["sid"]: x for x in v["flagged"]}
_, secs, _, _ = va.load_outline()
allowed = set(va.ids_in(t)) | set(p3.roles(secs[sec]))
for sid, new in fx.items():
    if sid.startswith("raw:"):                       # free replacement: {"raw:<old text>": "<new text>"}
        old = sid[4:]
    else:
        old = rows[sid]["sentence"]
    if old not in t:
        print("NOT FOUND", sid, old[:90])
        continue
    if new != "CUT":
        bad = [i for i in va.ids_in(new) if i not in allowed]
        if bad:
            print("REFUSED (IDs not assigned to this section)", sid, bad)
            continue
    t = t.replace(old, "" if new == "CUT" else new, 1)
    print("applied", sid)
t = re.sub(r"[ \t]{2,}", " ", t).replace(" \n", "\n")
f.write_text(t, encoding="utf-8")
