"""Enforce one primary home: an item that is E in two units stays E only in its home unit (the ID prefix; else the
earliest unit) and becomes C (marked 'home Ch N') elsewhere. Free. Run plan_qc.py afterwards."""
import re, collections
from pathlib import Path
W = Path(__file__).resolve().parent.parent / "editorial" / "plan_work"
UN = ["04","05","06","07","08","09","10","11","12","13"]
ID = r"C\d\d-[A-Z0-9]+(?:-[A-Z0-9]+)*?-\d{3}"
def eids(line):
    m = re.match(r"^(\s*-\s*)E: (.*?)(?= · |$)", line)
    return re.findall(ID, m.group(2)) if m else []
texts = {n: (W / f"sections_ch{n}_edited.md").read_text(encoding="utf-8") for n in UN}
where = collections.defaultdict(set)
for n, t in texts.items():
    for line in t.split("\n"):
        for i in eids(line): where[i].add(n)
fixes = 0
for i, us in where.items():
    if len(us) < 2: continue
    home = i[1:3] if i[1:3] in us else min(us)
    for n in us - {home}:
        out = []
        for line in texts[n].split("\n"):
            if i in eids(line):
                m = re.match(r"^(\s*-\s*)E: (.*?)( · .*)?$", line)
                pre, elist, rest = m.group(1), m.group(2), m.group(3) or ""
                items = [x.strip() for x in re.split(r",\s*(?=C\d\d-)", elist)]
                moved = [x for x in items if x.startswith(i)]
                keep = [x for x in items if not x.startswith(i)]
                tag = moved[0] + f" (home Ch {int(home) if home != '13' else 'AW'}: cross-reference)"
                if " · C: " in rest:
                    rest = rest.replace(" · C: ", " · C: " + tag + ", ", 1)
                else:
                    rest = " · C: " + tag + rest
                line = (pre + "E: " + ", ".join(keep) + rest) if keep else (pre + rest.lstrip(" ·").lstrip())
                fixes += 1
            out.append(line)
        texts[n] = "\n".join(out)
for n, t in texts.items():
    (W / f"sections_ch{n}_edited.md").write_text(t, encoding="utf-8")
print("demoted", fixes)
