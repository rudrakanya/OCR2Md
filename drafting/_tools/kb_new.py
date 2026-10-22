"""Add a gap-filling item from the corpus Markdown (free local search; no API). User rule, 15 Oct 2026.

The quotation is sliced verbatim from the source file by code (a line, optionally cut between two exact substrings);
the page is the `<!-- page N -->` marker in force at that line; the item is tagged kb-new with its evidence tier.

  python -I -X utf8 drafting/_tools/kb_new.py UNIT BOOKCODE "<file name>" LINE ["start substring" ["end substring"]]
  e.g. kb_new.py C10 MADHYABHARAT "The cultural heritage of madhya bharat.md" 386
Appends to drafting/evidence_index/kb_new.jsonl and prints the new ID (C10-KBN-MADHYABHARAT-001, …).
"""
import json
import re
import sys
from pathlib import Path

DR = Path(__file__).resolve().parent.parent
CORPUS = DR.parent / "Udaipur Books Markdown files"
OUT = DR / "evidence_index" / "kb_new.jsonl"
sys.path.insert(0, str(DR / "_pipe"))
import tiers  # noqa: E402


def main():
    unit, code, fname, line = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
    start = sys.argv[5] if len(sys.argv) > 5 else None
    end = sys.argv[6] if len(sys.argv) > 6 else None
    lines = (CORPUS / fname).read_text(encoding="utf-8").split("\n")
    text = lines[line - 1]
    if start:
        i = text.index(start)
        j = text.index(end, i) + len(end) if end else len(text)
        text = text[i:j]
    page = None
    for k in range(line - 1, -1, -1):
        m = re.search(r"<!--\s*page\s+(\d+)\s*-->", lines[k])
        if m:
            page = int(m.group(1))
            break
    existing = [json.loads(x) for x in OUT.open(encoding="utf-8")] if OUT.exists() else []
    n = 1 + sum(1 for e in existing if e["id"].startswith(f"{unit}-KBN-{code}-"))
    iid = f"{unit}-KBN-{code}-{n:03d}"
    tier = tiers.tier_of({"book_code": code})[0]
    item = {"id": iid, "unit": unit, "kind": "kb-new", "book_code": code, "page": f"p. {page}" if page else "no page",
            "source_file": fname, "line": line, "quote": text.strip(), "tier": tier, "flags": ["kb-new"]}
    with OUT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(iid, item["page"], f"T{tier}", text.strip()[:160])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
