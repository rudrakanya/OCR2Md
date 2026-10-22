"""Write the human-readable side of the image store from image_manifest.jsonl (free).

  python -I -X utf8 drafting/image_store/_tools/publish.py
Writes image_index.md (every image: label, caption, page, file), list_of_plates.md (the authors' List of Plates in
both OCR readings, with the Contents numbers) and PROVENANCE.md.
"""
import collections
import datetime
import json
from pathlib import Path

STORE = Path(__file__).resolve().parents[1]
WORK = STORE / "_work"


def esc(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def main():
    recs = [json.loads(l) for l in (STORE / "image_manifest.jsonl").open(encoding="utf-8")]
    auth = json.loads((WORK / "authorities.json").read_text(encoding="utf-8"))
    plates = [r for r in recs if r["kind"] == "plate"]
    images = [r for r in recs if r["kind"] == "image"]
    types = collections.Counter(r["image_type"] for r in images)
    flagged = [r for r in recs if r.get("ocr_verify")]
    serious = [r for r in flagged if any(not x.startswith("diacritics") for x in r["ocr_verify_reasons"])]

    L = ["# Image store: *Corpus Inscriptionum Indicarum* VII.2, *Inscriptions of the Paramāras*", "",
         f"{len(plates)} plate records ({sum(1 for r in plates if r.get('file'))} with a file; "
         f"{sum(1 for r in plates if not r.get('file'))} missing from the scan), {len(images)} separated images, "
         f"{sum(1 for r in recs if r['kind'] == 'emblem')} emblem. Image types: "
         + ", ".join(f"{k} {v}" for k, v in types.most_common()) + ".", "",
         f"Flagged for review (`ocr_verify`): {len(flagged)} records; {len(serious)} for reasons other than "
         "unconfirmed diacritics. Flags are marked ⚑ below; see `image_manifest.jsonl` for the reasons.", "",
         "Query: `python -I -X utf8 drafting/image_store/query.py \"Plate XXI\"` (also `--no 19`, `--page 114`, "
         "`--text sarpa`, `--flagged`).", "",
         "| ID | Label | Caption (List of Plates, checked against the scan) | List of Plates | No. | PDF p. | Type | File |",
         "|---|---|---|---|---|---|---|---|"]
    for r in recs:
        cap = r.get("caption_final") or r.get("caption") or (f'(plate caption) {r.get("plate_caption")}' if r.get("plate_caption") else "")
        flag = " ⚑" if r.get("ocr_verify") else ""
        f = f'[{Path(r["file"]).name}]({r["file"]})' if r.get("file") else "—"
        L.append(f'| {r["id"]} | {esc(r["label"])}{flag} | {esc(cap)} | {esc(r.get("list_of_plates"))} | '
                 f'{", ".join(map(str, r.get("inscription_nos") or []))} | {r.get("page")} | {esc(r.get("image_type"))} | {f} |')
    (STORE / "image_index.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    M = ["# List of Plates (CII VII.2, PDF pp. 12–15) and Contents numbers", "",
         "Two independent OCR readings of the authors' List of Plates. The first (table) is the existing layout-model "
         "OCR of the PDF (it keeps most IAST diacritics); the second (verbatim blocks) is Tesseract's reading of the "
         "same pages. Neither is guaranteed: check the page image (`_work/pages/p0012.png`–`p0015.png`) before quoting. "
         "Label corrections are noted where an OCR'd label fell out of the List's own ascending order.", "",
         "| Plate (as read) | Corrected | Title | Location | List page |", "|---|---|---|---|---|"]
    for e in auth["list_of_plates"]:
        c = e.get("label_correction", {}).get("corrected_to", "")
        M.append(f'| {esc(e["label_as_printed"])} | {esc(c)} | {esc(e["title"])} | {esc(e["location"])} | {e["list_page"]} |')
    M += ["", "## Tesseract reading of the same pages", ""]
    for p, txt in sorted(auth["list_of_plates_tesseract"].items(), key=lambda x: int(x[0])):
        M += [f"### PDF page {p}", "", "```", txt.strip(), "```", ""]
    M += ["## Contents (PDF pp. 8–11): inscription No. → Plate", "", "| No. | Plate | Title | Contents page |", "|---|---|---|---|"]
    for c in auth["contents"]:
        M.append(f'| {esc(c["nos"])} | {esc(c["plate"])} | {esc(c["title"])} | {c["page"]} |')
    M += ["", "## Edition headings (‘No. N; PLATE …’) found in the text", "", "| PDF page | Heading |", "|---|---|"]
    for h in auth["headings"]:
        M.append(f'| {h["page"]} | {esc(h["text"])} |')
    (STORE / "list_of_plates.md").write_text("\n".join(M) + "\n", encoding="utf-8")

    P = ["# Provenance", "",
         "- **Source PDF:** `PDF Originals/Inscriptions of the Paramaras.pdf` (39.8 MB, 496 pages; producer libtiff/tiff2pdf, "
         "creator ScanFix, 2013; RC4-encrypted for permissions only).",
         "- **Book:** *Corpus Inscriptionum Indicarum*, Vol. VII, Part 2: *Inscriptions of the Paramāras, Chandēllas, "
         "Kachchapaghātas and Two Minor Dynasties*, ed. Harihar Vithal Trivedi (Archaeological Survey of India); "
         "this part: Inscriptions of the Paramāras, “96 texts with 92 plates”.",
         f"- **Extracted:** {datetime.date.today().isoformat()}, locally, with no paid API: PyMuPDF (embedded page "
         "images), OpenCV/NumPy (region detection), Pillow (lossless PNG), Tesseract 5.4 (`Latin` script model from "
         "tessdata_best for captions, `eng` as the cross-reading). The List of Plates, Contents and edition headings "
         "also use the layout-model OCR already in `kb/_layout/Inscriptions Corpus.layout.jsonl`.",
         "- **Scan:** image-only (no text layer), one bilevel scan per page, about 2,650–2,750 × 3,960–4,050 px "
         "(≈ 290–300 dpi at the 9.25 × 13.8 in page). Files keep that native resolution: rasterising at 300–400 dpi "
         "would only resample the same scan.",
         "- **Plate LXVII** (Ajhārī Stone Inscription of the Time of Yaśōdhavala, “Facing page 238”) is a blank page "
         "(PDF p. 357) in this scan.",
         "- **Library marks** (a Delhi library's accession stamps and slip on pp. 4, 6, 7, 92, 493, 496) are not part "
         "of the book and are not extracted.", ""]
    (STORE / "PROVENANCE.md").write_text("\n".join(P) + "\n", encoding="utf-8")
    print("index rows", len(recs), "flagged", len(flagged), "serious", len(serious), dict(types))


if __name__ == "__main__":
    main()
