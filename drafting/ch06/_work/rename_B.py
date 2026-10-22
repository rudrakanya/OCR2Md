"""Worker B: rename C06-KBN-<CODE>-B<NN> to C06-KBN-<CODE>-B-0<NN> (validator needs a -ddd ending) in pack_B, kbn_B and units 6.4-6.8."""
import json, re
from pathlib import Path
W = Path(__file__).resolve().parent
DR = W.parent.parent
pat = re.compile(r"(C06-KBN-[A-Z0-9-]+?)-B(\d{2})\b")
fix = lambda s: pat.sub(lambda m: f"{m.group(1)}-B-0{m.group(2)}", s)
p = W / "pack_B.json"
P = json.loads(p.read_text(encoding="utf-8"))
for x in P:
    x["id"] = fix(x["id"])
    if x["id"].startswith("C06-KBN-JAGTA-EN-B-") and not x["page"].startswith("≈"):
        x["page"] = "≈ " + x["page"] + " (Hindi original)"
p.write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")
j = W / "kbn_B.jsonl"
L = [json.loads(l) for l in j.read_text(encoding="utf-8").splitlines() if l.strip()]
byid = {x["id"]: x for x in P}
L = [byid[fix(x["id"])] for x in L]
j.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in L), encoding="utf-8")
for s in ("6.4", "6.5", "6.6", "6.7", "6.8"):
    f = DR / "run" / "ch6" / f"{s}.md"
    t = f.read_text(encoding="utf-8")
    f.write_text(fix(t), encoding="utf-8")
print(len(L), sorted(x["id"] for x in L)[:3])
