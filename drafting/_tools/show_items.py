"""Print full quotations of evidence items from a chapter pack (free). Usage: show_items.py PACK.json ID [ID ...] | --kb (list KB items, 140 chars)"""
import json, re, sys
P = {x["id"]: x for x in json.load(open(sys.argv[1], encoding="utf-8"))}
if sys.argv[2] == "--kb":
    for i, x in P.items():
        if "-KB-" in i:
            print(i, "|", x.get("page"), "|", re.sub(r"\s+", " ", x["quote"])[:140])
    sys.exit()
for a in sys.argv[2:]:
    i = a if re.match(r"C\d\d-", a) else "C01-" + a
    x = P.get(i)
    if not x:
        print("##", i, "NOT IN PACK"); continue
    q = re.sub(r"\s+", " ", x["quote"])
    print(f"## {i} | {x.get('book_code')} | {x.get('page')} | T{x.get('tier')}\n{q}\n")
