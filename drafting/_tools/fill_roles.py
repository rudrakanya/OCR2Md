"""Fill {{S:Pn}} placeholders in a v2 entry template with the evidence-role lines of v1 paragraph S Pn
(from editorial/plan_work/sections_chNN_edited.md). Free.

  python -I -X utf8 drafting/_tools/fill_roles.py NN template.md   -> writes editorial/plan_v2/chNN.md
A placeholder may add items: {{7.5:P4|C: C07-X-001 (T7)}} appends to that role.
"""
import re
import sys
from pathlib import Path

DR = Path(__file__).resolve().parent.parent
n, tpl = sys.argv[1], Path(sys.argv[2]).read_text(encoding="utf-8")
src = (DR / "editorial" / "plan_work" / f"sections_ch{n}_edited.md").read_text(encoding="utf-8")
roles = {}
for sec in re.split(r"\n(?=## (?:\d+|AW)\.\d )", src):
    m = re.match(r"## ((?:\d+|AW)\.\d)", sec)
    if not m:
        continue
    for para in re.split(r"\n(?=  \d+a?\. \*\*P)", sec):
        pm = re.match(r"  (\d+a?)\. \*\*P(\d+a?)", para)
        if not pm:
            continue
        lines = [l.strip() for l in para.split("\n") if re.match(r"\s*- (?:E|C|X):", l)]
        if lines:
            roles[f"{m.group(1)}:P{pm.group(2)}"] = lines[0]


def rep(mm):
    key, extra = mm.group(1), mm.group(2)
    line = roles[key]
    if extra:
        for part in extra.split(";"):
            r, ids = part.split(":", 1)
            r = r.strip()
            if f" · {r}: " in line or line.startswith(f"- {r}: "):
                line = re.sub(rf"((?:^- | · ){r}: )", rf"\g<1>{ids.strip()}, ", line, count=1)
            else:
                line += f" · {r}: {ids.strip()}"
    return "     " + line


out = re.sub(r"^\s*\{\{((?:\d+|AW)\.\d+:P\d+a?)(?:\|([^}]*))?\}\}\s*$", rep, tpl, flags=re.M)
(DR / "editorial" / "plan_v2" / f"ch{n}.md").write_text(out, encoding="utf-8")
print("written", n, "placeholders left:", len(re.findall(r"\{\{(?:\d|AW)", out)))
