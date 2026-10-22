"""Query the Pande (Udayeśvara Temple) image store (free, local).

  python -I -X utf8 drafting/image_store_pande/query.py "Plate 12"      by the author's label ("Pl. 12", "12", "Fig. 1")
  python -I -X utf8 drafting/image_store_pande/query.py --page 33       by PDF page
  python -I -X utf8 drafting/image_store_pande/query.py --book-page 28  by the book's printed page
  python -I -X utf8 drafting/image_store_pande/query.py --text "natesa" caption substring (diacritic- and case-insensitive;
                                                                       searches the List caption, the on-page caption
                                                                       and the OCR readings)
  add --json for raw records, --flagged for records marked ocr_verify, --high for high-priority flags only.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent


def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def load():
    return [json.loads(l) for l in (HERE / "image_manifest.jsonl").open(encoding="utf-8")]


def parse_label(q):
    """'Plate 12' / 'Pl. 12' / '12' -> ('plate', 12); 'Fig. 1' / 'Figure 1' -> ('figure', 1)."""
    m = re.match(r"^\s*(fig(?:ure)?\.?|pl(?:ate)?\.?)?\s*(\d{1,3})\s*$", q.strip(), re.I)
    if not m:
        return None
    kind = "figure" if (m.group(1) or "").lower().startswith("fig") else "plate"
    return kind, int(m.group(2))


def search(recs, a):
    out = recs
    if a.label:
        pl = parse_label(a.label)
        if not pl:
            sys.exit(f"not a label: {a.label!r}")
        out = [r for r in out if (r["kind"], r["number"]) == pl]
    if a.page is not None:
        out = [r for r in out if r.get("page") == a.page]
    if a.book_page is not None:
        out = [r for r in out if str(a.book_page) in re.split(r"-", str(r.get("book_page")))]
    if a.text:
        q = fold(a.text)
        out = [r for r in out if q in fold(" ".join(str(r.get(k) or "") for k in
                                                   ("caption", "caption_on_page", "caption_on_page_ocr",
                                                    "caption_on_page_ocr_eng", "caption_on_page_text_layer", "label")))]
    if a.flagged:
        out = [r for r in out if r.get("ocr_verify")]
    if a.high:
        out = [r for r in out if r.get("review_priority") == "high"]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("label", nargs="?")
    ap.add_argument("--page", type=int)
    ap.add_argument("--book-page", type=int)
    ap.add_argument("--text")
    ap.add_argument("--flagged", action="store_true")
    ap.add_argument("--high", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    res = search(load(), a)
    for r in res:
        if a.json:
            print(json.dumps(r, ensure_ascii=False))
            continue
        print(f'{r["id"]}  {r["label"]}  book p.{r.get("book_page")}  PDF p.{r.get("page") or "-"}  '
              f'{r.get("file") or "(not in PDF)"}')
        print(f'    caption: {r["caption"]}')
        if r.get("caption_on_page") and fold(r["caption_on_page"]) != fold(r["caption"]):
            print(f'    on page: {r["caption_on_page"]}')
        if r.get("file_rectified"):
            print(f'    rectified: {r["file_rectified"]}   type: {r.get("image_type")}, {r.get("colour")}')
        if r.get("ocr_verify"):
            print(f'    [CHECK ({r.get("review_priority")}): ' + "; ".join(r.get("ocr_verify_reasons") or []) + "]")
    print(f"{len(res)} record(s)")


if __name__ == "__main__":
    main()
