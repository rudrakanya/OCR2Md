# Provenance

- **Source PDF:** `PDF Originals/Inscriptions of the Paramaras.pdf` (39.8 MB, 496 pages; producer libtiff/tiff2pdf, creator ScanFix, 2013; RC4-encrypted for permissions only).
- **Book:** *Corpus Inscriptionum Indicarum*, Vol. VII, Part 2: *Inscriptions of the Paramāras, Chandēllas, Kachchapaghātas and Two Minor Dynasties*, ed. Harihar Vithal Trivedi (Archaeological Survey of India); this part: Inscriptions of the Paramāras, “96 texts with 92 plates”.
- **Extracted:** 2026-10-22, locally, with no paid API: PyMuPDF (embedded page images), OpenCV/NumPy (region detection), Pillow (lossless PNG), Tesseract 5.4 (`Latin` script model from tessdata_best for captions, `eng` as the cross-reading). The List of Plates, Contents and edition headings also use the layout-model OCR already in `kb/_layout/Inscriptions Corpus.layout.jsonl`.
- **Scan:** image-only (no text layer), one bilevel scan per page, about 2,650–2,750 × 3,960–4,050 px (≈ 290–300 dpi at the 9.25 × 13.8 in page). Files keep that native resolution: rasterising at 300–400 dpi would only resample the same scan.
- **Plate LXVII** (Ajhārī Stone Inscription of the Time of Yaśōdhavala, “Facing page 238”) is a blank page (PDF p. 357) in this scan.
- **Library marks** (a Delhi library's accession stamps and slip on pp. 4, 6, 7, 92, 493, 496) are not part of the book and are not extracted.

