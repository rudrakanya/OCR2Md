"""Phase 1: extract every Chapter 3 item from the two evidence-map .docx files into
evidence_pack.json, and cross-check each against drafting/_evidence_log.jsonl (shared key: item ID).

  python -I "drafting/ch01/build_pack.py"
"""
import json
import re
import sys
from pathlib import Path

import docx

ROOT = Path(str(Path(__file__).resolve().parents[2]))
MAPS = ROOT / "Udaypur Evidence Mapping Documents"
OUT = ROOT / "drafting" / "ch03"
FILES = {"direct": MAPS / "Udaypur Evidence Map - Direct Evidence.docx",
         "contextual": MAPS / "Udaypur Evidence Map - Contextual Evidence.docx"}
# Items borrowed from other chapters' maps for Chapter 1 (user decision, 2026-10-13): tagged "borrowed"
BORROW = []
CIT = re.compile(r"^(C\d\d-[A-Z0-9-]+-\d{3})\s+(.*)$")


def style(p):
    try:
        return p.style.name
    except Exception:
        return ""


def book_codes(d):
    t = d.tables[1]
    return {r.cells[0].text.strip(): r.cells[1].text.strip() for r in t.rows[1:]}


def extract(path, strength, borrow=()):
    d = docx.Document(str(path))
    codes = book_codes(d)
    items, inside, book, quote = [], False, None, []
    for p in d.paragraphs:
        st, tx = style(p), p.text
        if st == "Heading 1":
            if inside and not borrow:
                break
            inside = tx.startswith("Chapter 3.") if not borrow else tx.startswith(("Chapter", "Afterword"))
            chapter = tx
            continue
        if not inside:
            continue
        if st == "Heading 2":
            m = re.search(r"\(([A-Z0-9-]+), \d+\)\s*$", tx)
            book = m.group(1) if m else None
            continue
        if st == "Evidence Quote":
            quote.append(tx)
            continue
        if st == "Evidence Citation":
            m = CIT.match(tx.strip())
            assert m, tx
            iid, rest = m.group(1), m.group(2)
            if borrow and iid not in borrow:
                quote = []
                continue
            parts = [x.strip() for x in re.split(r"\s{3,}", rest) if x.strip()]
            page = parts[0] if parts else ""
            also = [x for x in parts[1:] if x.startswith("also ")]
            flags = []
            if "⚠" in tx or any("⚠" in q for q in quote):
                flags.append("⚠")
            if page.startswith("≈"):
                flags.append("≈ (Hindi original)")
            if page.startswith("no page"):
                flags.append("no page")
            for a in also:
                flags.append(a)
            items.append({"id": iid, "book_code": book, "book_title": codes.get(book, ""),
                          "page": page, "quote": "\n".join(quote), "strength": strength,
                          "also": [c.strip() for a in also for c in a[5:].split(",")],
                          "flags": flags + (["borrowed"] if borrow else []),
                          **({"origin_chapter": chapter} if borrow else {})})
            quote = []
    return items


def norm(s):
    return " ".join(s.split())


def main():
    pack = []
    for strength, f in FILES.items():
        pack += extract(f, strength)
    for strength, f in (FILES.items() if BORROW else ()):
        pack += extract(f, strength, set(BORROW))
    got = {i["id"] for i in pack}
    assert all(b in got for b in BORROW), [b for b in BORROW if b not in got]
    log = {}
    for l in (ROOT / "drafting" / "_evidence_log.jsonl").open(encoding="utf-8"):
        r = json.loads(l)
        log[r["id"]] = r
    # cross-check against the structured log
    issues = []
    for it in pack:
        r = log.get(it["id"])
        if r is None:
            issues.append((it["id"], "id not in _evidence_log.jsonl"))
            it["log_check"] = "missing"
            continue
        qd, ql = norm(it["quote"]), norm(r["quote"])
        same_q = qd == ql or qd.replace("…", "").strip() in ql or ql in qd
        it["log_check"] = "ok" if same_q else "quote differs"
        if not same_q:
            issues.append((it["id"], "quote differs from log"))
        if r["strength"] != it["strength"]:
            issues.append((it["id"], f"strength {it['strength']} vs log {r['strength']}"))
        it.update(sub=r["sub"], note=r["note"], gloss=r.get("gloss"), claim=r.get("claim"),
                  chunk_id=r["chunk_id"], author=r.get("author"), log_citation=r["citation"],
                  language=r.get("language"))
    ids = [i["id"] for i in pack]
    assert len(ids) == len(set(ids)), "duplicate ids in pack"
    (OUT / "evidence_pack.json").write_text(json.dumps(pack, ensure_ascii=False, indent=1), encoding="utf-8")
    n_d = sum(i["strength"] == "direct" for i in pack)
    n_c = sum(i["strength"] == "contextual" for i in pack)
    print(f"direct {n_d}, contextual {n_c}, total {len(pack)} (borrowed {sum('borrowed' in i['flags'] for i in pack)})")
    print("flags:", {f: sum(f in i["flags"] for i in pack) for f in ("⚠", "≈ (Hindi original)", "no page")})
    print("log cross-check issues:", len(issues))
    for x in issues[:30]:
        print("  ", x)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
