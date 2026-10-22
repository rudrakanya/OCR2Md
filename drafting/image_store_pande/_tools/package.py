"""Package the Pande image store for a shared Google Drive folder (free, local; no API).

  python -I -X utf8 drafting/image_store_pande/_tools/package.py

Same scheme as the CII store (drafting/image_store/_tools/package.py, whose PNG-chunk and xlsx helpers are reused):
1. Files are copied under readable names into for_drive/<folder>/..., the caption embedded as PNG iTXt chunks and
   an XMP packet, inserted before IEND; the image data (IDAT) is copied byte for byte.
2. Two copies per plate: 'Plates' (perspective-corrected, the viewing copy) and 'Original crops' (the unresampled
   crop from the page photograph).
3. Writes the index (.xlsx and index.md), 'Captions to check.md', 'List of Illustrations.md', a README, and records
   the Drive file names in image_manifest.jsonl (drive_file, drive_file_original).
"""
import importlib.util
import json
import re
from datetime import date
from pathlib import Path

STORE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cii_package", STORE.parent / "image_store" / "_tools" / "package.py")
cii = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cii)

DRIVE_NAME = "Udaypur — Udayesvara Temple Plates (Pande)"
OUT = STORE / "for_drive" / DRIVE_NAME
SUB_MAIN = "Plates"
SUB_ORIG = "Original crops (unresampled)"
SOURCE = ("Anupa Pande, The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta "
          "(photographed copy: ASI Bhopal Circle Library)")
cii.SOURCE = SOURCE   # tag_png writes cii.SOURCE into the XMP packet
INDEX_NAME = "Index — Udayesvara Temple Plates (Pande).xlsx"


def short_caption(cap):
    t = re.sub(r",?\s*Courtesy .*$", "", cap)          # credit lines stay in the metadata and the index
    t = cii.ascii_fold(t)
    t = re.sub(r'[\\/:*?"<>|]', "", t)
    t = re.sub(r"\s+", " ", t).strip(" ,.")
    if len(t) > 95:
        t = t[:95].rsplit(" ", 1)[0]
    return t


def check_text(r):
    if not r.get("ocr_verify"):
        return ""
    return f"{r['review_priority']}: " + "; ".join(r["ocr_verify_reasons"])


def main():
    R = [json.loads(l) for l in (STORE / "image_manifest.jsonl").open(encoding="utf-8")]
    for d in (OUT / SUB_MAIN, OUT / SUB_ORIG):
        d.mkdir(parents=True, exist_ok=True)
    rows = []
    for r in R:
        lab = r["label"]
        tag = f"Fig. {r['number']:02d}" if r["kind"] == "figure" else f"Pl. {r['number']:03d}"
        if not r.get("file"):
            r.update({"drive_file": None, "drive_file_original": None})
            rows.append(["", "", lab, r["number"] if r["kind"] == "plate" else 0, r["caption"], "", "",
                         r["book_page"], "", "not photographed", "", "", "listed in the book; its page was not "
                         "photographed", r["id"]])
            continue
        fname = f"{tag} — {short_caption(r['caption'])}.png"
        fields = {
            "Title": f"{lab} — {r['caption']}", "Description": r["caption"]
            + (f" | On page: {r['caption_on_page']}" if r.get("variant_note") or
               (r["caption_on_page"] != r["caption"]) else ""),
            "Label": lab, "Caption": r["caption"], "CaptionOnPage": r.get("caption_on_page") or "",
            "SourcePage": f"book p. {r['book_page']}; PDF page {r['page']}", "ImageType": r["image_type"],
            "StableID": r["id"], "Source": SOURCE, "Check": check_text(r),
        }
        cii.tag_png(STORE / r["file_rectified"], OUT / SUB_MAIN / fname, dict(fields, Copy="perspective-corrected"),
                    fields["Title"], fields["Description"], r["id"])
        cii.tag_png(STORE / r["file"], OUT / SUB_ORIG / fname, dict(fields, Copy="unresampled crop of the page photo"),
                    fields["Title"], fields["Description"], r["id"])
        for p in (OUT / SUB_MAIN / fname, OUT / SUB_ORIG / fname):   # pixels must be untouched
            src = STORE / (r["file_rectified"] if p.parent.name == SUB_MAIN else r["file"])
            assert cii.idat(p) == cii.idat(src), p
        r.update({"drive_file": f"{SUB_MAIN}/{fname}", "drive_file_original": f"{SUB_ORIG}/{fname}"})
        pg = r.get("caption_on_page") or ""
        rows.append([SUB_MAIN, fname, lab, r["number"] if r["kind"] == "plate" else 0, r["caption"],
                     pg if pg != r["caption"] else "(same as List)", r.get("variant_note") or "", r["book_page"],
                     r["page"], r["image_type"], r.get("colour") or "", r.get("review_priority") or "",
                     check_text(r), r["id"]])
    with (STORE / "image_manifest.jsonl").open("w", encoding="utf-8") as f:
        for r in R:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    header = ["Folder", "Filename", "Label", "Plate no. (sort; Fig. = 0)", "Caption (List of Illustrations)",
              "On-page caption", "Variant note", "Book page", "PDF page", "Image type", "Colour", "Check priority",
              "Check notes", "Stable ID"]
    cii.write_xlsx(OUT / INDEX_NAME, header, rows, [10, 70, 9, 10, 80, 60, 50, 9, 8, 16, 14, 10, 80, 20])

    esc = lambda s: str(s if s is not None else "").replace("|", "\\|")
    n_img = sum(1 for r in R if r.get("file"))
    md = [f"# {DRIVE_NAME}", "",
          f"Figure and plates from *{SOURCE}*. Captions are the author's List of Illustrations wording, with the "
          "author's spelling and diacritics; where the caption printed under the photo differs, it is given too. "
          "Each image file also carries its label and caption in its embedded metadata.", "",
          f"Built {date.today().isoformat()}: {n_img} images. Pl. 7, 43, 83, 116 and 117 are listed in the book but "
          "their pages were not photographed. ⚑ = check (see 'Captions to check.md').", "",
          "| Label | Caption (List of Illustrations) | On-page caption | Book p. | File (in Plates/) | Check |",
          "|---|---|---|---|---|---|"]
    for x in rows:
        md.append(f"| {esc(x[2])} | {esc(x[4])} | {esc(x[5])} | {esc(x[7])} | {esc(x[1]) or '*not photographed*'} | "
                  f"{'⚑ ' + x[11] if x[11] else ''} |")
    (OUT / "index.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    # captions to check: review_flags without the local-only page paths
    fl = (STORE / "review_flags.md").read_text(encoding="utf-8")
    fl = re.sub(r"\n  - page image: `[^\n]*", "", fl)
    fl = fl.replace("Paths are relative to this folder; `_work/pages/pNNN.png` is the full page photo, "
                    "`_work/cap/<name>.png` the caption crop.",
                    "PDF p. = page of the photographed PDF (PDF Originals/The Udayesvara Temple - Anupa Pande "
                    "(scanned).pdf), where each flag can be checked.")
    (OUT / "Captions to check.md").write_text(fl, encoding="utf-8")
    (OUT / "List of Illustrations.md").write_text(
        (STORE / "list_of_illustrations.md").read_text(encoding="utf-8").replace(
            " Cross-checked against two independent OCR readings (Tesseract `Latin` on level-corrected bands, and the "
            "PDF's own Tesseract `eng` text layer): see `_work/list_ocr.json`.",
            " Cross-checked against two independent OCR readings."), encoding="utf-8")
    (OUT / "README.txt").write_text(
        f"{DRIVE_NAME}\n\n"
        f"Source: {SOURCE}.\n\n"
        f"{SUB_MAIN}/  Fig. 1 and the plates, straightened to a rectangle (the book was photographed at an angle).\n"
        f"           Use these for viewing and publication. {n_img} files.\n"
        f"{SUB_ORIG}/  the same pictures cut from the page photographs without resampling (not straightened;\n"
        f"           slivers of paper at the corners). Same file names.\n\n"
        "File names: 'Pl. <number> — <caption>' (numbers zero-padded so they sort; diacritics dropped from file\n"
        "names only). The full caption with diacritics, the on-page caption, book and PDF page, and a stable ID are\n"
        f"in '{INDEX_NAME}' and inside each PNG (iTXt/XMP fields).\n\n"
        "Captions to check.md  - wording conflicts (Pl. 49/50), crops to check (Pl. 67, 128), credit lines that\n"
        "                        appear only in the List, and captions whose diacritics need a glance.\n"
        "List of Illustrations.md - the author's List, as printed.\n"
        "Not photographed: Pl. 7, 43, 83, 116, 117 (book pp. 8-9, 34-35, 58-59, 82-83 missing from the photographs).\n",
        encoding="utf-8")
    print("rows", len(rows), "images", n_img)


if __name__ == "__main__":
    main()
