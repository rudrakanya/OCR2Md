"""Query the CII VII.2 image store (free, local).

  python -I -X utf8 drafting/image_store/query.py "Plate XXI"        by the authors' label (roman or arabic: "Plate 21")
  python -I -X utf8 drafting/image_store/query.py "XXI-B"            a sub-plate
  python -I -X utf8 drafting/image_store/query.py --no 19            by inscription number ("No. 19")
  python -I -X utf8 drafting/image_store/query.py --page 114         by PDF page
  python -I -X utf8 drafting/image_store/query.py --text "sarpa"     caption substring (diacritic- and case-insensitive;
                                                                     searches the on-page caption, both OCR readings and
                                                                     the List of Plates entry)
  add --plates-only to list whole plates only, --json for raw records, --flagged for records marked ocr_verify.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent


def roman(n):
    s = ""
    for a, r in [(90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while n >= a:
            s += r
            n -= a
    return s


ROMAN = {roman(i): i for i in range(1, 100)}


def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def load():
    return [json.loads(l) for l in (HERE / "image_manifest.jsonl").open(encoding="utf-8")]


def parse_label(q):
    """'Plate XXI-B' / 'plate 21b' / 'XXI' -> ('XXI', 'B' or None)."""
    m = re.match(r"^\s*(?:pl(?:ate)?\.?\s*)?([IVXLC]+|\d+)\s*[-‐–]?\s*([AB])?\s*$", q.strip(), re.I)
    if not m:
        return None
    num = m.group(1).upper()
    if num.isdigit():
        num = roman(int(num))
    return (num, m.group(2).upper() if m.group(2) else None) if num in ROMAN else None


def search(recs, a):
    out = recs
    if a.label:
        pl = parse_label(a.label)
        if not pl:
            sys.exit(f"not a plate label: {a.label!r}")
        num, sub = pl
        out = [r for r in out if r.get("plate_roman") == num and (not sub or r.get("kind") == "plate" or
                                                                    (r.get("sub_label") or "").upper().startswith(sub))]
    if a.no is not None:
        out = [r for r in out if a.no in (r.get("inscription_nos") or [])]
    if a.page is not None:
        out = [r for r in out if r.get("page") == a.page]
    if a.text:
        q = fold(a.text)
        out = [r for r in out if q in fold(" ".join(str(r.get(k) or "") for k in
                                                   ("caption", "caption_ocr_eng", "plate_caption", "list_of_plates",
                                                    "caption_layout_ocr", "label", "source_notes")))]
    if a.plates_only:
        out = [r for r in out if r.get("kind") == "plate"]
    if a.flagged:
        out = [r for r in out if r.get("ocr_verify")]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("label", nargs="?")
    ap.add_argument("--no", type=int)
    ap.add_argument("--page", type=int)
    ap.add_argument("--text")
    ap.add_argument("--plates-only", action="store_true")
    ap.add_argument("--flagged", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    res = search(load(), a)
    for r in res:
        if a.json:
            print(json.dumps(r, ensure_ascii=False))
            continue
        flag = "  [CHECK: " + "; ".join(r.get("ocr_verify_reasons") or []) + "]" if r.get("ocr_verify") else ""
        print(f'{r["id"]}  {r["label"]}  p.{r.get("page")}  {r.get("file") or "(no file)"}')
        cap = r.get("caption") or r.get("plate_caption")
        if cap:
            print(f'    caption: {cap}')
        if r.get("list_of_plates"):
            print(f'    List of Plates: {r["list_of_plates"]}')
        if r.get("inscription_nos"):
            print(f'    inscription No.: {", ".join(map(str, r["inscription_nos"]))}   type: {r.get("image_type")}')
        if flag:
            print("   " + flag)
    print(f"{len(res)} record(s)")


if __name__ == "__main__":
    main()
