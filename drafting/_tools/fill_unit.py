"""Fill a unit's TODO fields and append evidence-pass items to sections (free). Usage: fill_unit.py NN spec.json"""
import json, re, sys
from pathlib import Path
DR = Path(__file__).resolve().parent.parent
W = DR / "editorial" / "plan_work"
sys.path.insert(0, str(DR / "_tools")); sys.path.insert(0, str(DR / "_pipe"))
import tiers
n, spec = sys.argv[1], json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
log = {}
for l in (DR / "_evidence_log.jsonl").open(encoding="utf-8"):
    r = json.loads(l); log[r["id"]] = r
def tg(i):
    r = log.get(i); return f"{i} (T{tiers.tier_of(r)[0]})" if r else i
h = (W / f"head_ch{n}.md").read_text(encoding="utf-8")
h = h.replace("**Scope.** TODO", "**Scope.** " + spec["scope"])
(W / f"head_ch{n}.md").write_text(h, encoding="utf-8")
t = (W / f"tail_ch{n}.md").read_text(encoding="utf-8")
t = t.replace("unresolved\n\nTODO", "unresolved\n\n" + spec["conflicts"], 1)
t = t.replace("master outline\n\nTODO", "master outline\n\n" + spec["changes"], 1)
t = t.rstrip() + "\n" + spec.get("flags_extra", "") + "\n"
for k, v in spec.get("handoff", {}).items():
    t = re.sub(r"- \*\*" + k + r":\*\*.*", "- **" + k + ":** " + v.replace("\\", "\\\\"), t, count=1)
(W / f"tail_ch{n}.md").write_text(t, encoding="utf-8")
s = (W / f"sections_ch{n}.md").read_text(encoding="utf-8")
for a, b in spec.get("replace", []):
    assert a in s, a[:60]; s = s.replace(a, b, 1)
for sec, (role, ids, why) in spec.get("add", {}).items():
    m = re.search(r"^## " + re.escape(sec) + r" .*?(?=\n- \*\*Drafting guidance|\n- \*\*Transition)", s, re.S | re.M)
    assert m, sec
    line = f"\n  - **Evidence pass ({role}, optional by default; P0):** " + ", ".join(tg(i) for i in ids) + f" — {why}"
    s = s[:m.end()] + line + s[m.end():]
(W / f"sections_ch{n}_edited.md").write_text(s, encoding="utf-8")
print("filled", n)
