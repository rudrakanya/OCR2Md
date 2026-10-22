"""Append kb-new items (evidence_index/kb_new.jsonl) for one unit to a chapter pack (free; no API).
  python -I -X utf8 drafting/_tools/pack_add_kbn.py <pack.json> <UNIT e.g. C01>
Book title is copied from an existing pack item of the same book code."""
import json
import sys
from pathlib import Path

DR = Path(__file__).resolve().parent.parent
pack_p, unit = Path(sys.argv[1]), sys.argv[2]
pack = json.loads(pack_p.read_text(encoding="utf-8"))
have = {x["id"] for x in pack}
titles = {x.get("book_code"): x.get("book_title") for x in pack if x.get("book_title")}
added = []
for line in (DR / "evidence_index" / "kb_new.jsonl").open(encoding="utf-8"):
    it = json.loads(line)
    if it["id"].startswith(unit + "-KBN-") and it["id"] not in have:
        it.setdefault("book_title", titles.get(it["book_code"], ""))
        it.setdefault("kind", "kb-new")
        pack.append(it)
        added.append(it["id"])
pack_p.write_text(json.dumps(pack, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"added {len(added)}: {', '.join(added)}")
