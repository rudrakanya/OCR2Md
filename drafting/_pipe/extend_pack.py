"""Extend a chapter evidence pack: add items borrowed from other chapters' maps (taken verbatim from
drafting/_evidence_log.jsonl, tagged "borrowed") and tag every item with its evidence tier (tiers.py). Code only, no API.

  python -I drafting/_pipe/extend_pack.py <in.json> <out.json> [ID ...]
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import tiers  # noqa: E402

LOG = HERE.parent / "_evidence_log.jsonl"


def borrowed(ids, titles):
    want, out = set(ids), []
    for line in LOG.open(encoding="utf-8"):
        r = json.loads(line)
        if r["id"] not in want:
            continue
        pg = r.get("page")
        page = (f"p. {pg}" + (f"–{r['page_end']}" if r.get("page_end") not in (None, pg) else "")) if pg is not None else "no page"
        flags = ["borrowed"] + (["no page"] if pg is None else []) + (["≈ (Hindi original)"] if r["book_code"] == "JAGTA-EN" else [])
        out.append({"id": r["id"], "book_code": r["book_code"], "book_title": titles.get(r["book_code"], r.get("book_title", "")),
                    "page": page, "quote": r["quote"], "strength": r["strength"], "also": [], "flags": flags,
                    "sub": r.get("sub"), "note": r.get("note", ""), "gloss": r.get("gloss"), "claim": r.get("claim"),
                    "chunk_id": r.get("chunk_id"), "author": r.get("author"), "log_citation": r.get("citation"),
                    "language": r.get("language"), "origin_chapter": r.get("unit"), "log_check": "ok"})
    missing = want - {i["id"] for i in out}
    if missing:
        sys.exit(f"not in the evidence log: {sorted(missing)}")
    return out


def main(src, dst, ids):
    P = json.loads(Path(src).read_text(encoding="utf-8"))
    have = {i["id"] for i in P}
    titles = {i["book_code"]: i["book_title"] for i in P}
    P += [i for i in borrowed([x for x in ids if x not in have], titles)]
    tiers.tag(P)
    Path(dst).write_text(json.dumps(P, ensure_ascii=False, indent=1), encoding="utf-8")
    by = {}
    for i in P:
        by[i["tier"]] = by.get(i["tier"], 0) + 1
    print(f"{len(P)} items ({len(P) - len(have)} borrowed added); by tier {dict(sorted(by.items()))}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
