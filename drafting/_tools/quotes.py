"""Print quotations for evidence IDs from drafting/evidence_index (and the evidence log for other units). Free.
  python -I -X utf8 drafting/_tools/quotes.py [--n 300] ID ...   |   --roles E <sections_chNN.md>"""
import json, re, sys
from pathlib import Path
DR = Path(__file__).resolve().parent.parent
idx = {}
for f in list((DR / "evidence_index").glob("ch*.jsonl")) + [DR / "evidence_index" / "kb_new.jsonl"]:
    for l in f.open(encoding="utf-8"):
        r = json.loads(l); idx[r["id"]] = (r["book_code"], r["page"], r["quote"])
args = sys.argv[1:]; n = 300
if args[:1] == ["--n"]: n = int(args[1]); args = args[2:]
if args[:1] == ["--roles"]:
    role, f = args[1], args[2]; t = Path(f).read_text(encoding="utf-8"); ids = []
    for m in re.finditer(r"- " + role + r": (.*?)(?: · [CXN][a-z]*:|$)", t, re.M):
        ids += [i for i in re.findall(r"C\d\d-[A-Z0-9-]+?-\d{3}", m.group(1)) if i not in ids]
    args = ids
log = None
for i in args:
    if i not in idx:
        if log is None:
            log = {json.loads(l)["id"]: json.loads(l) for l in (DR / "_evidence_log.jsonl").open(encoding="utf-8")}
        r = log.get(i)
        if r: idx[i] = (r["book_code"], r.get("page"), r["quote"])
    b = idx.get(i)
    q = re.sub(r"\s+", " ", b[2])[:n] if b else ""
    print(f"{i} | {b[0]} {b[1]} | {q}" if b else f"{i} | NOT FOUND")
