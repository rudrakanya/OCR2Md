"""Direct items of a unit not cited anywhere in the plan (sections_ch*.md or PLAN). Free.
  python -I -X utf8 drafting/_tools/coverage.py 04 [maxtier]"""
import json, re, sys
from pathlib import Path
DR = Path(__file__).resolve().parent.parent
n = sys.argv[1]; mt = int(sys.argv[2]) if len(sys.argv) > 2 else 9
used = set()
for f in list((DR / "editorial" / "plan_work").glob("*.md")) + [DR / "editorial" / "Chapter_4_to_Afterword_Master_Drafting_Outline.md"]:
    if f.name.startswith("sections_") or f.name.startswith("unit_"):
        used |= set(re.findall(r"C\d\d-[A-Z0-9-]+?-\d{3}", f.read_text(encoding="utf-8")))
outline_any = set(re.findall(r"C\d\d-[A-Z0-9-]+?-\d{3}", (DR / "editorial" / "Chapter_4_to_Afterword_Master_Drafting_Outline.md").read_text(encoding="utf-8")))
rows = [json.loads(l) for l in (DR / "evidence_index" / f"ch{n}.jsonl").open(encoding="utf-8")]
d = [r for r in rows if r["kind"] == "direct" and r["tier"] <= mt]
un = [r for r in d if r["id"] not in used]
print(f"C{n}: direct items tier<={mt}: {len(d)}; not in plan sections: {len(un)}; of these named somewhere in the outline (notes/'not used' lists): {sum(1 for r in un if r['id'] in outline_any)}")
for r in un:
    if r["id"] not in outline_any:
        print(" UNMENTIONED", r["id"], r["page"], re.sub(r"\s+", " ", r["quote"])[:150])
