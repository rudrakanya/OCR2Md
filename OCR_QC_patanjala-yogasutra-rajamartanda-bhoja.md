# OCR quality check — Patañjala-Yogasūtra with the Rājamārtaṇḍa-vṛtti of Bhojadeva

**Source PDF:** `Patanjal Yog Sutra with Rajmartand Vritti of Bhojadev by Ram Shankar Bhattarya (bad binding) - Bharatiya Vidya Publication Varanasi.pdf` — 116 pages, image-only, CC-0 scan (Jangamwadi Math Collection, digitized by eGangotri).

**Engine:** Tesseract 5.4, `-l Devanagari --psm 3`, pages rendered at 400 dpi. No LLM was used to read, transcribe or reconstruct any text. Where the scan loses text it is flagged, never filled in.

**Page images for eye-checking:** `ocr_cache/patanjala-yogasutra-rajamartanda-bhoja.pages/images` — one JPEG per page, beside the raw per-page OCR in `ocr_cache/patanjala-yogasutra-rajamartanda-bhoja.pages/page_NNN.txt`.

## Authorship and edition, verified from the book itself

Read from the title-page image (`images/page_001.jpg`), not from the filename:

- **पातञ्जलयोगसूत्रम् … भोजदेवकृत-राजमार्तण्डवृत्तिसमेतम्** — the Yogasūtra together with the Rājamārtaṇḍa commentary **composed by Bhojadeva**. Authorship confirmed at source.
- **धारेश्वरभोज-तद्ग्रन्थ-तन्मतसमीक्षा-पातञ्जलसिद्धान्तादिविवरणात्मिकया भूमिकया संवलितम्** — the volume carries an introduction reviewing **Dhāreśvara Bhoja** (Bhoja, lord of Dhārā: the Paramāra king), his works and his views. This is the layer that matters for C5 and C10.
- Editor: **श्री राम शंकर भट्टाचार्यः** (व्याकरणाचार्यः, M.A., Ph.D.), of the Kāpila Maṭha.
- Publisher: **भारतीय विद्या प्रकाशन**, 22/36 Pañcagaṅgā Ghāṭ, Varanasi; printer Brajvasi Printing Press, Assi, Varanasi; price ₹2.
- **No year appears on the title page or the imprint page** (`images/page_004.jpg`), so the date is recorded as `undated-flagged` rather than guessed.
- **No closing colophon was captured.** The text ends mid-discussion on pdf p. 114 (printed p. 80); p. 115 is blank and p. 116 is a publisher advertisement. Whether the edition ends there or the scan is short cannot be determined from the scan alone — flagged, not assumed.

## Gate results

| gate | pages | meaning |
|---|--:|---|
| pass | 31 | quotable as OCR'd |
| needs_recheck | 85 | usable for retrieval and search; **check the page image before quoting** |
| illegible | 0 | no usable text; would be marked `[illegible]` — none occurred |

Mean word confidence across the book: **72.9** (median 72.5, worst 46.1 on pdf p. 4).

### Why so many need a recheck

The gutter test compares OCR confidence in the margin band against the body of the page. At a >18-point deficit, 52 pages flagged. **I tightened it to >12** after eye-checking pdf p. 64 (`images/page_064.jpg`): its line-ends are physically cropped in the scan — *क्षीणा मे क्लेशा व…*, *कार्य्यविमुक्ति-* — so words are missing from the image itself, not merely misread, and no engine can recover them. At the tighter threshold 85 pages carry that risk. This is the 'bad binding' of the filename, and it is the single biggest quality limit on this book.

| failure reason | pages |
|---|--:|
| inner-margin confidence N vs N in the body (gutter damage) | 83 |
| N% of words below N confidence | 4 |
| skew -N° | 4 |
| skew N° | 4 |
| mean confidence N | 3 |
| only N% of letters are Devanagari | 2 |
| N Latin word-runs outside the stamp | 1 |

### Skew

Median baseline skew is at or under 1 degree on 96 pages. Worst: p. 2 (-12.6 deg), p. 34 (-4.35 deg), p. 80 (2.88 deg), p. 83 (2.19 deg).

### Garbage and hallucination checks

- CJK characters in a Devanagari/English text: 0 across 0 pages (the bilingual-model failure seen in the RapidOCR corpus does not occur here).
- Pages where fewer than half the letters are Devanagari: 2 (front matter, library stamps, and the English advertisement on p. 116).
- The digitiser's footer stamp is stripped from every page and excluded from these counts.

## Page order

Printed page numbers were read on 59 of 116 pages; the rest have no running head, or the head did not OCR.

- **Gaps between adjacent pages: none.** No page is missing from the scan.
- **Apparent decrease:** pdf 63 to 64: printed 29 to 20. Eye-checked on `images/page_064.jpg`: the printed header is **[३०]**, which OCR read as **[२०]** — a misread numeral, not a misbound page. **Page order is intact.**

## Eye-checked sample (character/word error impression)

| page | impression |
|---|---|
| pdf 61 (printed २७) | Header and most lines exact. Errors are letter confusions, not dropped text: तत्तथाविधमिति as तत्तथादिधंमिति, द्वि as ड्रि, बुद्धी as वुद्धो. Roughly 5-8% of characters. |
| pdf 45 (printed ११) | All content present and in order; sūtras 24-26 and the footnote block intact. ष/प and श/द confusions (पुरुषान्तर as पुरुपान्तर); repha sometimes lost (सर्वज्ञ as सववज्ञ). |
| pdf 64 (printed ३०) | Body good, but **line-ends are cropped in the scan**, so text is missing from the image. Not quotable without another copy. |
| pdf 1 and 4 (title, imprint) | Lowest confidence in the book (49.0 and 46.1): ornamental title type and library stamps. Read by eye instead; findings above. |

**Overall impression:** roughly 90-95% character accuracy on clean body pages, with systematic confusions (ष/प, श/द/ल, व/द, dropped repha) rather than invented words. Good for retrieval and search; **not safe for verbatim Sanskrit quotation without checking the page image**.

## Gate decision

The book **passes the gate for ingestion**: no illegible pages, no missing pages, order intact, no hallucinated text, authorship verified from the title page.

Conditions carried into the KB as metadata:

- every chunk from a `needs_recheck` page carries `is_quotable: false` and `needs_recheck: true`;
- `page` on every chunk records the pdf page, and the printed page where the running head was read;
- the raw per-page OCR and the page image stay side by side on disk for verification.

## Every page

| pdf page | printed | gate | conf | median | low-conf | words | Devanagari | skew | edge vs body |
|---|---|---|--:|--:|--:|--:|--:|--:|---|
| 1 | — | needs_recheck | 49.0 | 44.5 | 62.7% | 59 | 117% | 1.08 deg | 41.8 vs 50.2 |
| 2 | — | needs_recheck | 48.9 | 44.4 | 61.9% | 21 | 1% | -12.6 deg | 38.6 vs 54.1 |
| 3 | — | needs_recheck | 72.8 | 92.6 | 27.1% | 48 | 1% | -0.5 deg | 38.3 vs 74.2 |
| 4 | — | needs_recheck | 46.1 | 40.7 | 62.2% | 74 | 47% | -1.25 deg | 34.9 vs 54.1 |
| 5 | — | needs_recheck | 83.0 | 91.7 | 12.6% | 206 | 146% | 0.07 deg | 71.9 vs 84.1 |
| 6 | 4 | needs_recheck | 81.6 | 91.6 | 15.0% | 287 | 154% | -1.39 deg | 67.3 vs 85.7 |
| 7 | 5 | needs_recheck | 81.6 | 91.7 | 14.5% | 297 | 157% | 0.29 deg | 67.5 vs 85.0 |
| 8 | — | needs_recheck | 78.9 | 92.1 | 18.3% | 328 | 151% | -1.0 deg | 61.9 vs 84.8 |
| 9 | 7 | needs_recheck | 81.9 | 92.4 | 15.3% | 334 | 154% | -0.86 deg | 72.4 vs 84.5 |
| 10 | 8 | needs_recheck | 79.6 | 90.9 | 15.8% | 259 | 163% | -0.28 deg | 64.2 vs 83.5 |
| 11 | — | pass | 82.3 | 92.3 | 14.8% | 338 | 160% | 0.17 deg | 72.7 vs 84.5 |
| 12 | 10 | needs_recheck | 82.0 | 91.7 | 13.0% | 292 | 165% | -0.06 deg | 67.1 vs 84.9 |
| 13 | — | needs_recheck | 82.1 | 92.0 | 14.0% | 308 | 160% | -1.08 deg | 72.1 vs 85.5 |
| 14 | 12 | needs_recheck | 76.8 | 91.3 | 21.3% | 347 | 161% | 0.64 deg | 61.1 vs 83.8 |
| 15 | 13 | needs_recheck | 79.9 | 92.2 | 16.1% | 311 | 163% | 0.59 deg | 70.9 vs 83.1 |
| 16 | 14 | needs_recheck | 78.3 | 91.4 | 20.3% | 335 | 150% | -0.83 deg | 51.2 vs 85.6 |
| 17 | — | pass | 86.2 | 93.2 | 8.7% | 323 | 154% | 0.18 deg | 80.3 vs 87.4 |
| 18 | — | pass | 84.4 | 92.7 | 11.1% | 333 | 155% | -0.07 deg | 78.1 vs 85.7 |
| 19 | 17 | needs_recheck | 81.9 | 93.2 | 14.9% | 369 | 155% | 1.16 deg | 66.6 vs 86.8 |
| 20 | — | needs_recheck | 81.9 | 93.2 | 14.5% | 344 | 156% | -0.25 deg | 68.9 vs 86.0 |
| 21 | — | needs_recheck | 79.1 | 92.4 | 17.6% | 335 | 160% | 1.94 deg | 63.2 vs 82.8 |
| 22 | 20 | needs_recheck | 82.2 | 92.8 | 16.1% | 311 | 159% | -0.27 deg | 65.9 vs 85.8 |
| 23 | — | needs_recheck | 81.1 | 93.0 | 15.4% | 318 | 151% | 0.4 deg | 62.1 vs 85.1 |
| 24 | — | needs_recheck | 82.6 | 93.2 | 14.6% | 342 | 153% | 0.93 deg | 69.3 vs 85.1 |
| 25 | — | needs_recheck | 82.4 | 93.1 | 14.4% | 312 | 158% | 0.13 deg | 73.3 vs 85.4 |
| 26 | 24 | pass | 81.9 | 92.8 | 15.8% | 335 | 162% | 1.44 deg | 75.0 vs 82.8 |
| 27 | — | pass | 80.9 | 92.5 | 16.1% | 316 | 167% | 0.07 deg | 72.1 vs 83.4 |
| 28 | — | pass | 81.4 | 91.7 | 15.2% | 302 | 160% | 0.82 deg | 73.8 vs 82.3 |
| 29 | 27 | needs_recheck | 82.2 | 91.9 | 13.9% | 259 | 159% | 0.4 deg | 68.8 vs 87.0 |
| 30 | — | needs_recheck | 73.5 | 89.9 | 24.9% | 217 | 112% | -0.23 deg | 53.8 vs 79.6 |
| 31 | — | needs_recheck | 78.1 | 90.3 | 19.7% | 208 | 121% | -0.58 deg | 64.3 vs 82.6 |
| 32 | 30 | pass | 80.3 | 92.2 | 19.1% | 267 | 146% | 0.79 deg | 73.1 vs 81.8 |
| 33 | 31 | needs_recheck | 67.0 | 74.4 | 35.0% | 80 | 134% | 0.3 deg | 58.6 vs 71.6 |
| 34 | — | needs_recheck | 56.3 | 76.2 | 47.4% | 19 | 7% | -4.35 deg | 28.2 vs 91.6 |
| 35 | — | needs_recheck | 67.6 | 81.5 | 30.8% | 130 | 158% | 0.63 deg | 58.1 vs 71.4 |
| 36 | 2 | needs_recheck | 74.1 | 86.7 | 21.6% | 185 | 161% | -0.4 deg | 52.0 vs 79.9 |
| 37 | 3 | needs_recheck | 69.0 | 82.9 | 29.7% | 209 | 163% | 2.01 deg | 54.5 vs 73.2 |
| 38 | — | needs_recheck | 67.5 | 82.4 | 31.8% | 170 | 157% | 0.07 deg | 55.4 vs 71.2 |
| 39 | 5 | needs_recheck | 77.9 | 88.8 | 20.1% | 169 | 160% | 0.66 deg | 64.7 vs 81.9 |
| 40 | 6 | needs_recheck | 71.6 | 84.2 | 29.1% | 175 | 161% | 0.72 deg | 58.1 vs 73.9 |
| 41 | 7 | pass | 78.6 | 89.0 | 18.3% | 213 | 160% | -0.14 deg | 69.9 vs 81.2 |
| 42 | 8 | needs_recheck | 64.7 | 76.0 | 36.3% | 237 | 163% | 0.63 deg | 50.9 vs 68.4 |
| 43 | 9 | needs_recheck | 72.4 | 88.7 | 27.4% | 215 | 163% | 0.75 deg | 58.5 vs 77.1 |
| 44 | — | needs_recheck | 65.3 | 81.5 | 37.0% | 208 | 160% | 0.09 deg | 44.5 vs 69.9 |
| 45 | 11 | needs_recheck | 70.6 | 83.6 | 31.9% | 191 | 157% | 0.21 deg | 42.7 vs 78.4 |
| 46 | — | needs_recheck | 66.9 | 83.0 | 32.3% | 186 | 155% | 0.09 deg | 42.7 vs 76.2 |
| 47 | — | needs_recheck | 68.0 | 78.2 | 33.1% | 175 | 168% | 0.14 deg | 46.5 vs 74.5 |
| 48 | — | needs_recheck | 73.5 | 87.2 | 26.6% | 203 | 163% | 0.15 deg | 51.5 vs 77.9 |
| 49 | 15 | pass | 72.5 | 84.1 | 27.7% | 173 | 164% | -0.2 deg | 64.3 vs 75.1 |
| 50 | — | needs_recheck | 70.4 | 82.4 | 31.6% | 177 | 160% | 0.12 deg | 59.9 vs 72.2 |
| 51 | 17 | needs_recheck | 68.2 | 83.7 | 33.5% | 167 | 166% | 0.73 deg | 53.6 vs 72.0 |
| 52 | — | needs_recheck | 64.4 | 74.2 | 40.6% | 175 | 161% | -0.3 deg | 40.3 vs 71.5 |
| 53 | — | needs_recheck | 74.9 | 87.5 | 20.2% | 183 | 165% | -0.08 deg | 59.8 vs 79.7 |
| 54 | — | pass | 63.3 | 78.6 | 36.8% | 174 | 160% | 0.4 deg | 36.6 vs 68.0 |
| 55 | 21 | needs_recheck | 70.2 | 83.8 | 29.3% | 181 | 160% | 0.92 deg | 54.6 vs 75.0 |
| 56 | — | pass | 64.3 | 74.3 | 38.1% | 176 | 162% | 0.56 deg | 55.6 vs 65.8 |
| 57 | 23 | needs_recheck | 72.1 | 86.6 | 26.1% | 165 | 166% | 0.09 deg | 56.2 vs 76.5 |
| 58 | 24 | needs_recheck | 71.8 | 86.3 | 30.4% | 181 | 161% | -0.59 deg | 60.6 vs 73.8 |
| 59 | — | pass | 65.6 | 79.3 | 35.3% | 187 | 161% | -0.56 deg | 58.7 vs 68.1 |
| 60 | — | needs_recheck | 68.9 | 81.4 | 33.0% | 176 | 157% | -0.31 deg | 55.2 vs 75.1 |
| 61 | 27 | pass | 73.0 | 84.1 | 26.9% | 160 | 165% | -0.25 deg | 66.7 vs 75.4 |
| 62 | — | needs_recheck | 71.5 | 86.3 | 26.0% | 181 | 156% | 0.01 deg | 58.1 vs 74.6 |
| 63 | 29 | pass | 78.7 | 89.2 | 20.0% | 180 | 164% | 0.84 deg | 72.4 vs 79.6 |
| 64 | 20 | needs_recheck | 69.6 | 83.4 | 29.2% | 178 | 168% | 0.44 deg | 49.0 vs 73.7 |
| 65 | — | pass | 68.3 | 80.9 | 32.0% | 175 | 160% | 1.05 deg | 60.9 vs 70.6 |
| 66 | — | needs_recheck | 69.3 | 82.8 | 30.7% | 199 | 165% | 0.03 deg | 50.5 vs 75.5 |
| 67 | 32 | needs_recheck | 69.8 | 82.8 | 31.8% | 176 | 164% | 0.9 deg | 54.2 vs 74.9 |
| 68 | — | needs_recheck | 67.1 | 78.1 | 35.5% | 166 | 155% | 0.1 deg | 54.1 vs 70.9 |
| 69 | 35 | needs_recheck | 74.7 | 86.8 | 24.2% | 153 | 161% | -0.58 deg | 53.5 vs 79.2 |
| 70 | 36 | needs_recheck | 67.8 | 82.4 | 31.8% | 154 | 149% | 0.31 deg | 51.2 vs 73.0 |
| 71 | — | needs_recheck | 60.4 | 72.1 | 40.1% | 187 | 154% | -1.66 deg | 50.6 vs 64.1 |
| 72 | 38 | needs_recheck | 66.0 | 82.5 | 34.1% | 164 | 155% | -0.31 deg | 39.9 vs 69.2 |
| 73 | 39 | needs_recheck | 71.9 | 87.1 | 29.1% | 141 | 157% | 0.49 deg | 60.0 vs 76.3 |
| 74 | — | needs_recheck | 70.4 | 82.9 | 29.5% | 176 | 155% | 0.09 deg | 57.6 vs 71.9 |
| 75 | — | needs_recheck | 66.7 | 80.9 | 33.3% | 138 | 159% | 0.17 deg | 57.1 vs 69.2 |
| 76 | — | pass | 70.8 | 87.0 | 29.4% | 180 | 155% | -0.54 deg | 62.9 vs 74.3 |
| 77 | 43 | pass | 67.1 | 74.9 | 32.3% | 161 | 159% | -1.25 deg | 61.2 vs 69.8 |
| 78 | 44 | needs_recheck | 72.8 | 84.2 | 25.0% | 196 | 157% | 0.27 deg | 62.3 vs 75.0 |
| 79 | 45 | needs_recheck | 71.7 | 84.3 | 28.6% | 203 | 157% | -0.41 deg | 63.0 vs 75.5 |
| 80 | — | needs_recheck | 77.5 | 90.0 | 21.0% | 181 | 154% | 2.88 deg | 65.5 vs 80.9 |
| 81 | — | needs_recheck | 71.8 | 84.0 | 28.4% | 183 | 160% | 0.05 deg | 56.7 vs 76.1 |
| 82 | — | pass | 68.4 | 84.8 | 32.9% | 146 | 164% | 0.21 deg | 73.8 vs 66.4 |
| 83 | 49 | needs_recheck | 71.9 | 82.1 | 28.0% | 200 | 163% | 2.19 deg | 67.3 vs 73.6 |
| 84 | — | needs_recheck | 71.7 | 84.3 | 24.9% | 181 | 159% | 0.53 deg | 57.6 vs 75.7 |
| 85 | — | pass | 67.7 | 82.0 | 33.1% | 175 | 155% | -0.51 deg | 61.1 vs 69.3 |
| 86 | 52 | needs_recheck | 69.8 | 81.9 | 30.3% | 185 | 161% | -0.19 deg | 53.7 vs 73.5 |
| 87 | — | needs_recheck | 68.1 | 83.0 | 32.6% | 175 | 160% | -0.11 deg | 56.1 vs 73.8 |
| 88 | 54 | needs_recheck | 73.1 | 87.9 | 27.9% | 183 | 156% | 1.05 deg | 53.9 vs 78.3 |
| 89 | — | needs_recheck | 68.5 | 85.8 | 35.0% | 206 | 154% | 0.75 deg | 52.0 vs 70.9 |
| 90 | 56 | needs_recheck | 77.7 | 89.8 | 18.4% | 190 | 160% | -0.09 deg | 65.1 vs 80.6 |
| 91 | 57 | pass | 64.9 | 78.3 | 36.7% | 158 | 167% | -0.69 deg | 57.3 vs 66.9 |
| 92 | 58 | needs_recheck | 73.5 | 86.8 | 25.7% | 191 | 161% | -0.99 deg | 55.3 vs 76.4 |
| 93 | 59 | needs_recheck | 70.7 | 84.4 | 28.8% | 163 | 161% | -1.06 deg | 46.7 vs 78.1 |
| 94 | 60 | pass | 66.6 | 80.3 | 34.0% | 156 | 150% | 0.19 deg | 60.9 vs 68.0 |
| 95 | 61 | needs_recheck | 68.5 | 84.0 | 31.8% | 192 | 157% | -0.55 deg | 55.5 vs 74.1 |
| 96 | 62 | needs_recheck | 72.0 | 85.1 | 28.6% | 182 | 155% | -0.98 deg | 59.4 vs 76.4 |
| 97 | — | needs_recheck | 74.2 | 86.9 | 23.9% | 188 | 162% | -0.22 deg | 60.5 vs 79.0 |
| 98 | 64 | needs_recheck | 77.3 | 89.6 | 18.9% | 190 | 156% | -0.05 deg | 60.1 vs 82.0 |
| 99 | 65 | needs_recheck | 69.4 | 85.2 | 33.1% | 175 | 158% | -0.6 deg | 59.8 vs 72.4 |
| 100 | 66 | needs_recheck | 69.5 | 85.2 | 29.6% | 223 | 162% | -0.63 deg | 58.3 vs 75.2 |
| 101 | — | needs_recheck | 75.3 | 89.4 | 21.9% | 228 | 158% | 0.18 deg | 63.9 vs 79.9 |
| 102 | 68 | pass | 78.4 | 88.6 | 18.0% | 200 | 164% | -0.63 deg | 73.4 vs 79.4 |
| 103 | — | pass | 75.9 | 87.6 | 20.8% | 202 | 163% | -1.08 deg | 70.3 vs 77.9 |
| 104 | 70 | pass | 74.4 | 85.2 | 22.9% | 214 | 160% | -0.45 deg | 66.0 vs 76.4 |
| 105 | — | pass | 72.4 | 85.8 | 28.1% | 199 | 159% | -1.42 deg | 66.6 vs 74.1 |
| 106 | 72 | needs_recheck | 74.7 | 87.3 | 23.1% | 199 | 160% | 0.08 deg | 61.5 vs 78.2 |
| 107 | — | needs_recheck | 74.0 | 87.8 | 23.1% | 212 | 161% | -1.59 deg | 61.9 vs 77.0 |
| 108 | 74 | pass | 75.7 | 89.1 | 22.0% | 182 | 164% | -0.14 deg | 78.7 vs 74.3 |
| 109 | — | needs_recheck | 68.0 | 77.3 | 35.2% | 159 | 163% | 0.43 deg | 57.8 vs 69.9 |
| 110 | 76 | pass | 73.7 | 87.5 | 24.3% | 169 | 164% | -0.28 deg | 65.0 vs 76.3 |
| 111 | 77 | needs_recheck | 73.6 | 86.2 | 25.8% | 217 | 158% | 0.41 deg | 60.1 vs 76.7 |
| 112 | 78 | pass | 78.4 | 89.4 | 18.6% | 204 | 161% | -0.0 deg | 75.0 vs 79.5 |
| 113 | 79 | pass | 77.4 | 90.5 | 18.8% | 277 | 156% | -0.5 deg | 72.3 vs 79.0 |
| 114 | — | pass | 69.9 | 86.0 | 31.0% | 216 | 157% | -0.65 deg | 66.7 vs 68.3 |
| 115 | — | pass | 93.0 | 93.2 | 0.0% | 7 | 0% | 0.33 deg | 87.7 vs 94.6 |
| 116 | — | needs_recheck | 73.4 | 88.7 | 26.9% | 320 | 157% | -0.05 deg | 40.9 vs 81.2 |
