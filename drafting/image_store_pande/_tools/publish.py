"""Publish the Pande image store from _work/build_records.json (free, local).

Writes image_manifest.jsonl, image_index.md, review_flags.md, list_of_illustrations.md, PROVENANCE.md.

Captions: `caption` is the List of Illustrations wording (transcribed by eye, list_of_illustrations.py). The
on-page caption is kept as `caption_on_page`: read by eye where the OCR readings disagreed with the List
(ON_PAGE_BY_EYE below), otherwise the List wording confirmed by OCR agreement (similarity >= 0.95, folded).
`ocr_verify` is set generously; `review_priority` sorts the flags (high / medium / low).
"""
import json
import re
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "_work"
TODAY = date(2026, 10, 22).isoformat()

# On-page captions read by eye from the page photos (label stripped), for every caption whose OCR readings
# scored < 0.95 against the List. Kept verbatim; CE is printed in small capitals.
ON_PAGE_BY_EYE = {
    "Fig. 1": "Plan of the Udayeśvara Temple, c. 11th century CE, Udayapur, Madhya Pradesh.",
    "Pl. 1": "View of the śikhara from the south-west side.",
    "Pl. 8": "View of buttresses and their crowning members (south-east side of the gūḍhamaṇḍapa).",
    "Pl. 9": "View of the samvarṇā roof of the gūḍhamaṇḍapa.",
    "Pl. 10": "View of the east, north and south mukhamaṇḍapas.",
    "Pl. 11": "View of the śukanāsa at the base of the eastern latā.",
    "Pl. 13": "View of the miniature niche on the lower half of the śukanāsa enshrining the image of the Hariharārkapitāmaha.",
    "Pl. 14": "Dancing devī on the right side of the miniature niche of the śukanāsa.",
    "Pl. 15": "Dancing Sarasvatī on the left side of the miniature niche of the śukanāsa.",
    "Pl. 16": "Dancing Sarasvatī, 9th century CE.",
    "Pl. 19": "View of the five-storeyed celestial mansion on the southern side of the śukanāsa.",
    "Pl. 25": "General view of the south-east side of the gūḍhamaṇḍapa.",
    "Pl. 28": "Sūrya enshrined in a khattaka on the south-east side of the gūḍhamaṇḍapa.",
    "Pl. 33": "Harihara housed in a khattaka on the south-east side of the gūḍhamaṇḍapa.",
    "Pl. 40": "Seated Uma-Maheśvara housed in a khattikā on the vedībandha of the south-east side of gūḍhamaṇḍapa.",
    "Pl. 41": "Seated Umā-Maheśvara housed in a khattikā on the vedībandha of the south-east side of gūḍhamaṇḍapa.",
    "Pl. 44": "View of the buttresses on the south-west side of the gūḍhamaṇḍapa.",
    "Pl. 49": "Tripurāntaka Śiva enshrined in a khattaka on the south kapilī.",
    "Pl. 50": "Tripurāntaka Śiva enshrined in a khattaka on the north kapilī.",
    "Pl. 52": "Haṁsavatī depicted on the tilaka of the south-west side of gūḍhamaṇḍapa.",
    "Pl. 59": "Varuṇa housed in a khattaka on the north-west side of the gūḍhamaṇḍapa.",
    "Pl. 61": "Brahmā depicted in a khattaka on the north-west side of the gūḍhamaṇḍapa.",
    "Pl. 63": "Śiva Naṭeśa enshrined in a khattaka near the north mukhamaṇḍapa.",
    "Pl. 69": "Mahiṣāsuramardinī enshrined in a khattaka near the north mukhamaṇḍapa (east side).",
    "Pl. 79": "Seated Umā-Maheśvara enshrined in a khattikā on the vedībandha of the north-east side of gūḍhamaṇḍapa.",
    "Pl. 85": "Nirṛti enshrined in a khattaka between the south latā and west latā.",
    "Pl. 86": "Viṣṇu enshrined in a khattaka between the south latā and west latā.",
    "Pl. 87": "Śiva enshrined in a khattaka between the south latā and west latā.",
    "Pl. 90": "Vīrabhadra enshrined in the khattaka of the west latā.",
    "Pl. 92": "Kārttikeya enshrined in the khattaka at the bottom of the west latā.",
    "Pl. 95": "Śiva enshrined in a khattaka between the west latā and north latā.",
    "Pl. 97": "Vāyu enshrined in a khattaka between the west latā and north latā.",
    "Pl. 99": "Brahmā-Brahmāṇi enshrined in a khattikā on the vedībandha between the west latā and north latā.",
    "Pl. 100": "Brahmā-Brahmāṇi enshrined in a khattikā on the vedībandha between the west latā and north latā.",
    "Pl. 102": "Sarasvatī enshrined in a khattikā on the vedībandha between the west latā and north latā.",
    "Pl. 103": "Cāmuṇḍā enshrined in the khattaka of the north latā.",
    "Pl. 105": "Umā-Maheśvara enshrined in a khattikā on the vedībandha between the north latā and north kapilī.",
    "Pl. 107": "Brahmā-Brahmāṇi enshrined in a khattaka below the north kapilī.",
    "Pl. 112": "View of the doorway of the south mukhamaṇḍapa.",
    "Pl. 114": "Rāhu, Ketu and Saturn on the upper lintel of the doorway of the south mukhamaṇḍapa.",
    "Pl. 118": "Tapasvinī Pārvatī enshrined in a niche on a pillar of the gūḍhamaṇḍapa.",
    "Pl. 124": "View of the ceiling of the antarāla.",
    "Pl. 129": "Pisanhārī kā Mandir, Udayapur, Vidisha, Madhya Pradesh.",
}

# Notes from the review of crops and captions
WORDING_CONFLICT = {
    "Pl. 49": "WORDING CONFLICT: the List says 'on the south-west side of the gūḍhamaṇḍapa'; the caption under the "
              "photo says 'on the south kapilī'. The List's wording for Pl. 50 ('on the south kapilī') matches this "
              "page caption, so the List may have the two entries shifted. The body text supports the page captions: book p. 39 "
              "(PDF p. 42) says 'the north kapilī too, has a beautiful Tripurāntaka Śiva image (pls. 50, 58)'. "
              "Label kept from the List as instructed; the on-page caption is likely the correct one.",
    "Pl. 50": "WORDING CONFLICT: the List says 'on the south kapilī'; the caption under the photo says 'on the north "
              "kapilī'. The body text (book p. 39: 'the north kapilī too, has a beautiful Tripurāntaka Śiva image "
              "(pls. 50, 58)') agrees with the page caption. See Pl. 49.",
}
BLURRED_PAGES = {31: "page photo motion-blurred", 47: "page photo out of focus", 64: "page photo out of focus",
                 73: "page photo motion-blurred"}
CROP_NOTES = {
    "Pl. 67": "pale sky: the top edge was set by hand at the printed frame; the bottom edge runs close to the "
              "running footer. Check the crop.",
    "Pl. 128": "the right side of the print is washed out and its frame edge is not visible; the right side was "
               "set by hand at the end of the top rule. Check the crop.",
}
MISSING_OPENINGS = ["8-9", "34-35", "58-59", "82-83"]


def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    return re.sub(r"\s+", " ", "".join(c for c in s if not unicodedata.combining(c))).lower().strip()


def has_marks(s):
    return any(unicodedata.combining(c) for c in unicodedata.normalize("NFD", s or ""))


def main():
    R = json.loads((W / "build_records.json").read_text(encoding="utf-8"))
    out = []
    for r in R:
        lab = r["label"]
        reasons, prio = [], "low"
        if r.get("not_in_pdf"):
            r["caption_on_page"] = None
            r["ocr_verify"] = False
            r["review_priority"] = None
            r["ocr_verify_reasons"] = []
            r["image_type"] = "photograph"
            out.append(r)
            continue
        sim = r.get("list_vs_page_similarity")
        if lab in ON_PAGE_BY_EYE:
            r["caption_on_page"] = ON_PAGE_BY_EYE[lab]
            r["caption_on_page_source"] = "read by eye from the page photo (OCR readings disagreed with the List)"
        else:
            r["caption_on_page"] = r["caption"]
            r["caption_on_page_source"] = (f"List wording, confirmed by Tesseract on the page (similarity {sim}, "
                                           "diacritics folded)")
        # List vs page wording
        if fold(r["caption_on_page"]) != fold(r["caption"]):
            lst, pg = r["caption"], r["caption_on_page"]
            if lab in WORDING_CONFLICT:
                reasons.append(WORDING_CONFLICT[lab]); prio = "high"
            elif "Courtesy" in lst and "Courtesy" not in pg:
                r["variant_note"] = ("on-page caption omits the credit line ('" + lst[lst.index("Courtesy"):].rstrip(".")
                                     + "') that the List gives")
                reasons.append("List and on-page caption differ: credit line only in the List (label kept from the List)")
                prio = max(prio, "medium", key=["low", "medium", "high"].index)
            else:
                r["variant_note"] = "on-page wording differs from the List"
                reasons.append("List and on-page caption differ"); prio = max(prio, "medium", key=["low", "medium", "high"].index)
        else:
            r["variant_note"] = None
        if sim is None or sim < 0.95:
            reasons.append(f"OCR could not confirm the caption (best on-page OCR similarity {sim}); the on-page "
                           "caption was read by eye")
            prio = max(prio, "medium", key=["low", "medium", "high"].index)
        if r.get("caption_anchor_source", "").startswith("caption box set by hand"):
            reasons.append("no OCR reading found the label on the page; caption located by hand")
        if r["page"] in BLURRED_PAGES:
            reasons.append(BLURRED_PAGES[r["page"]] + ": diacritics in the caption could not be confirmed at full "
                           "resolution")
            prio = max(prio, "medium", key=["low", "medium", "high"].index)
        if lab in CROP_NOTES:
            reasons.append("CROP: " + CROP_NOTES[lab]); prio = "high"
        if has_marks(r["caption"]):
            reasons.append("IAST diacritics transcribed by eye from a phone photo; Tesseract does not read them "
                           "reliably")
        r["ocr_verify"] = bool(reasons)
        r["ocr_verify_reasons"] = reasons
        r["review_priority"] = prio if reasons else None
        out.append(r)

    order = ["id", "book", "label", "label_long", "kind", "number", "sub_label", "file", "file_rectified",
             "caption", "caption_source", "caption_on_page", "caption_on_page_source", "variant_note",
             "book_page", "page", "pdf_page", "image_type", "colour", "pixels", "extraction", "extraction_rectified",
             "ocr_verify", "review_priority", "ocr_verify_reasons", "caption_on_page_ocr", "caption_on_page_ocr_eng",
             "caption_on_page_text_layer", "caption_ocr_conf", "list_vs_page_similarity", "caption_anchor_source",
             "caption_box", "caption_image", "page_image", "quad", "box", "tilt_deg", "region_source",
             "region_note", "sides_from_run", "sides_by_hand", "edge_scores", "nearest_anchor", "not_in_pdf", "notes"]
    with (ROOT / "image_manifest.jsonl").open("w", encoding="utf-8") as f:
        for r in out:
            rec = {k: r.get(k) for k in order if k in r}
            rec.update({k: v for k, v in r.items() if k not in rec and k not in ("anchor_xy",)})
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # ---- index
    have = [r for r in out if r.get("file")]
    L = ["# Image index: Anupa Pande, *The Udayeśvara Temple*", "",
         f"{len(have)} images extracted ({sum(r['image_type'] == 'photograph' for r in have)} photographs, "
         f"{sum(r['image_type'] == 'plan' for r in have)} plan); {len(out) - len(have)} listed plates are on "
         f"openings that were not photographed (book pp. {', '.join(MISSING_OPENINGS)}). Captions are the List of "
         "Illustrations wording; ⚑ = flagged for checking (see review_flags.md). PDF p. = page of the scanned PDF.", "",
         "| Label | Caption (List of Illustrations) | Book p. | PDF p. | Type | File | |", "|---|---|---|---|---|---|---|"]
    for r in out:
        f = f"[{r['file']}]({r['file']})" if r.get("file") else "*not in PDF*"
        flag = "⚑" + ("!" if r.get("review_priority") == "high" else "") if r.get("ocr_verify") else ""
        L.append(f"| {r['label']} | {r['caption']} | {r['book_page']} | {r.get('page') or '—'} | "
                 f"{r['image_type']}, {r.get('colour') or '—'} | {f} | {flag} |")
    (ROOT / "image_index.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---- review flags
    L = ["# Captions and crops to check", "",
         "Every record with `ocr_verify: true`, grouped by priority. Paths are relative to this folder; "
         "`_work/pages/pNNN.png` is the full page photo, `_work/cap/<name>.png` the caption crop.", ""]
    for pr, head in (("high", "High: wording conflicts and uncertain crops"),
                     ("medium", "Medium: List and page differ, or OCR could not confirm the caption"),
                     ("low", "Low: diacritics only (List transcribed by eye; worth a glance against the scan)")):
        rs = [r for r in out if r.get("review_priority") == pr]
        L += [f"## {head} ({len(rs)})", ""]
        for r in rs:
            L.append(f"- **{r['label']}** (PDF p. {r['page']}, book p. {r['book_page']}) — {r['caption']}")
            if r.get("caption_on_page") and fold(r["caption_on_page"]) != fold(r["caption"]):
                L.append(f"  - on page: {r['caption_on_page']}")
            for why in r["ocr_verify_reasons"]:
                L.append(f"  - {why}")
            L.append(f"  - page image: `{r['page_image']}`" + (f"; caption crop: `{r['caption_image']}`"
                                                                 if r.get("caption_image") else ""))
        L.append("")
    miss = [r for r in out if r.get("not_in_pdf")]
    L += [f"## Listed but not in the PDF ({len(miss)})", ""]
    for r in miss:
        L.append(f"- **{r['label']}** (book p. {r['book_page']}) — {r['caption']}")
    L += ["", "## Unreadable captions", "", "None: every extracted image's caption was read (by OCR or by eye).", "",
          "## Regions that were not figures", "",
          "- PDF pp. 134–137 (Appendix: Samarāṅgaṇasūtradhāra translation): the detector picked up dimly lit text "
          "blocks; no figures there, nothing extracted.",
          "- Every page photo also shows desk, fingers and the facing page around the book page; only printed "
          "pictures inside the page were cropped.",
          "- No library stamps, slips or marginalia were found in this copy."]
    (ROOT / "review_flags.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---- list of illustrations (readable)
    lst = json.loads((ROOT / "list_of_illustrations.json").read_text(encoding="utf-8"))
    L = ["# List of Illustrations (book pp. xi–xiv = PDF pp. 4–7)", "",
         "Transcribed by eye from the page photos; wording, spelling and transliteration as printed (italics not "
         "marked). Cross-checked against two independent OCR readings (Tesseract `Latin` on level-corrected bands, "
         "and the PDF's own Tesseract `eng` text layer): see `_work/list_ocr.json`.", "",
         "## List of Figures", ""]
    for e in lst["entries"]:
        if e["kind"] == "figure":
            L.append(f"{e['number']}. {e['list_caption']} — p. {e['book_page']}")
    L += ["", "## List of Plates", "", f"*{lst['plates_note']}*", ""]
    for e in lst["entries"]:
        if e["kind"] == "plate":
            L.append(f"{e['number']}. {e['list_caption']} — p. {e['book_page']}")
    (ROOT / "list_of_illustrations.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---- provenance
    P = f"""# Provenance

- **Source PDF:** `PDF Originals/The Udayesvara Temple - Anupa Pande (scanned).pdf` (199 pages, 519 MB). Each page is
  one phone photograph of the open book (JPEG, 4624 × 3468 px, placed rotated 90°) with an invisible OCR text layer
  (Tesseract `eng`, added when the PDF was assembled locally from the photographs).
- **Book:** Anupa Pande, *The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta*. The
  photographed copy is from the Archaeological Survey of India, Bhopal Circle Library (books_manifest.yaml); no
  year is stated in the copy.
- **Coverage:** front matter from the List of Illustrations onwards and book pp. 1–197. Four openings were not
  photographed: book pp. {', '.join(MISSING_OPENINGS)}, so Pl. 7, 43, 83, 116 and 117 are listed but have no image.
- **Stable ID:** `PANDE-UDT-FIG01`, `PANDE-UDT-PL001` … `PANDE-UDT-PL130`.
- **Extracted:** {TODAY}, locally, no paid API: PyMuPDF (page photos pulled as stored, decoded once, turned upright
  by an exact 90° pixel rotation), OpenCV/NumPy (picture detection, edge snapping), Pillow (lossless PNG),
  Tesseract 5 (`Latin` and `eng`, tessdata_best) for caption anchors and cross-readings.
- **Resolution:** the photos have no scan dpi. The printed text block (about 6 in wide) spans roughly 2,600–2,900 px,
  so the effective resolution is about 430–480 px per inch, varying page to page with camera distance and tilt.
- **Files:** `plates/` holds the bounding-box crop of each picture from the decoded photo (not resampled; because
  the page was photographed at an angle, the crop is not rectangular to the print and carries slivers of paper at
  the corners). `rectified/` holds the same picture perspective-corrected to a rectangle (Lanczos resampling at the
  picture's own pixel size), the better copy for viewing and publication.
- **Captions:** `caption` is the List of Illustrations, transcribed by eye; on-page captions are checked against it
  (OCR, and by eye wherever OCR disagreed). See review_flags.md.
"""
    (ROOT / "PROVENANCE.md").write_text(P, encoding="utf-8")
    from collections import Counter
    print(len(out), "records;", len(have), "images;", Counter(r.get("review_priority") for r in out))


if __name__ == "__main__":
    main()
