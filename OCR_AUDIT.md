# Phase 1 — OCR faithfulness audit

**Date:** 2026-10-05 · **Scope:** 27 registered sources · **Method:** `audit_ocr.py`
**Constraint observed:** audit only — no re-embed, no store writes, no paid-API calls, no file restoration.

## Method

For each book with a source document in the repo, pages are sampled across the body
(front matter skipped) and read **independently** of the pipeline that produced the
markdown:

1. **Born-digital pages** — the PDF's own text layer is the ground truth.
2. **Scanned pages** — rendered at 400 dpi and read with Tesseract, language chosen
   from what the markdown contains (`Devanagari+eng` where the markdown carries more
   than 400 Devanagari characters, else `eng`).
3. **Token recall** is the headline metric: of the distinctive tokens on a sampled
   page, what fraction appear *anywhere* in that book's markdown. Recall catches
   dropped text — gutters, margins, footnotes — without needing page alignment.
4. **Script integrity** is measured separately, because a pipeline can score well on
   Latin text while mangling every Sanskrit word.

Recall is a **lower bound on fidelity, not an upper bound on quality**: it cannot see
text that was invented rather than dropped. That blind spot is what Phase 2 found in
ADH, and it is recorded in `EXTRACTION_FAILURES.md`.

## Results

| Grade | Count | Sources |
|---|---|---|
| pass | 10 | BET-K, BET-S, BHJ-H, DEV, KRAM-1, KRAM-2, RAJM, SAM, SIN-T, SKP-13 |
| needs-recheck | 2 | ADH (62%), INT-ARC (83%) |
| re-OCR | 1 | GUP (41%) |
| not-comparable | 1 | RAJ-E |
| unverifiable — source absent | 13 | GAN, GAZ-VID, HAR, INT-GEO, PAN, PAR, PAT-CH, PAT-INS, PAT-TEM, SIN-B, SIN-S, TIW-E, TIW-H |

### Per-book detail

| Code | Grade | Recall (mean / min) | Pages | Read via | Note |
|---|---|---|---|---|---|
| SKP-13 | pass | 98% / — | 8 | text layer | born-digital |
| BET-K | pass | 98% / — | 8 | text layer | born-digital |
| RAJM | pass | 97% / 94% | 12 | Devanagari+eng | the "bad binding" risk did not materialise |
| BET-S | pass | 96% / — | 8 | text layer | born-digital |
| DEV | pass | 94% / — | 8 | eng | |
| KRAM-2 | pass | 90% / — | 8 | eng | |
| SIN-T | pass | 88% / — | 8 | eng | |
| BHJ-H | pass | 87% / 78% | 12 | Devanagari+eng | 10,369 Devanagari chars on page vs 125,662 in markdown |
| KRAM-1 | pass | 86% / — | 8 | eng | |
| SAM | pass | 79% / 66% | 34 | text layer | 3 chapter extracts only; see caveat below |
| INT-ARC | needs-recheck | 83% / 54% | 8 | eng | one low page (p66, 401 chars — a plate) |
| ADH | needs-recheck | 62% / 51% | 8 | eng | all 51 pages stored sideways; see below |
| GUP | re-OCR | 41% / 2% | 8 | eng | prose is sound; plates and sideways tables are not |
| RAJ-E | not-comparable | 7% | 12 | eng | markdown is an English translation of Hindi pages |

### Notable per-page evidence

- **RAJM** (the source the brief singled out for bad binding) came back strongest of
  all scanned books: 94–99% recall across 12 pages, 14,239 Devanagari characters read
  off the pages against 139,123 in the markdown. Gutter loss did not occur.
- **ADH** p17 51%, p29 52%, p41 53% — the lowest three of eight. Every one of ADH's
  51 pages is stored rotated 270°, and the scan is 72 dpi effective.
- **GUP** splits cleanly: prose pages p22 95%, p54 82%, p173 81%; plate and sideways
  table pages p118 2%, p181 6%, p213 20%, p245 no text at all.
- **INT-ARC** p66 yielded 401 characters — a plate page, not lost prose.

### Caveats that are not defects

- **RAJ-E / TIW-E are translations.** Token recall compares page words with markdown
  words, so on a translation it measures translation distance. RAJ-E's 7% is a
  competent translation, not a broken OCR. These are graded `not-comparable`.
- **SAM is partial.** Only chapters 55–60, 66–67 and 71–72 are in the repo, so the
  sample cannot speak for the rest of the work. Its 79% is also depressed by roughly
  18% AI-reworded chunks already recorded against it.
- **13 sources cannot be verified at all** because no source document is in the repo.
  This is the provenance gap already written up in `PROVENANCE_GAP.md`; Phase 1 adds
  nothing to it beyond confirming it blocks verification.

## Ranked re-OCR list

| Rank | Source | Why | Recoverable? | Cost |
|---|---|---|---|---|
| 1 | **ADH** | 15% of its chunks are fabricated, not merely garbled (`EXTRACTION_FAILURES.md`) | Yes — the true rows read cleanly at native dpi + 270° rotation | 51 pages |
| 2 | **GUP** | sideways comparative tables (p118, p181) carry iconographic data that is absent from the markdown | Yes, with orientation correction | ~10–20 affected pages, not all 266 |
| 3 | INT-ARC | one sampled plate page; no evidence of prose loss | Low value | ~5 pages |
| — | all others | pass, or unverifiable for want of a source document | n/a | n/a |

**Recommendation:** re-OCR ADH in full and GUP's rotated/plate pages only. Do **not**
re-OCR the corpus. Nine of the ten `pass` books score 86%+ and a global re-run would
spend hours to change nothing.

## Settings finding, and a hypothesis I tested and discarded

Six of the fourteen available PDFs store exactly one pixel per point — a 72–100 dpi
effective scan (ADH, BET-S, DEV, GUP, INT-ARC, SIN-T). I expected the audit's 400 dpi
render to upscale those ~5× and understate their recall, which would have made ADH's
62% and GUP's 41% tool artifacts.

**That hypothesis is false.** Measured head to head on ADH, rendering at native
resolution with the page rotated upright scored *the same or slightly worse* than the
audit's own settings:

| ADH page | 400 dpi / psm 3 (audit) | native + rot270 / psm 3 | native + rot270 / psm 6 |
|---|---|---|---|
| 13 | 65% recall | 62% | 55% |
| 23 | 61% | 64% | 49% |
| 25 | 63% | 60% | 56% |
| 34 | 74% | 71% | 61% |
| 44 | 61% | 56% | 63% |

The reason is that **`--psm 3` detects and corrects page orientation by itself**, so
the audit was already reading these sideways pages right way up. Rotation does extract
~30% more characters per page (3,648 vs 2,644 on p13) at equivalent recall, so it is
worth using for a re-extraction, but it does not change any grade. ADH's ~60–70% is
the genuine ceiling for Tesseract on a 72-dpi scan of diacritic-dense prose.

## Corrections to earlier statements in this audit

1. **Six "re-OCR" verdicts were my own tooling failure.** An earlier run graded ADH,
   DEV, GUP, INT-ARC, KRAM-1, RAJ-E and SIN-T as `re-OCR — no readable text
   recovered`. `~/tessdata` held Devanagari, hin and san but not `eng`, and the auditor
   forced `TESSDATA_PREFIX` there, so every English scan returned rc=1 and zero
   characters. After copying `eng.traineddata` and `osd.traineddata` into that
   directory, five of the six pass and only GUP remains a genuine `re-OCR`. The auditor
   now reports `tool-error` instead of blaming the book.
2. **The 400 dpi upscaling concern, stated above as a likely cause, is withdrawn** —
   it was tested and did not hold.
3. **RAJM's "needs-recheck 65%"** reported earlier came from RapidOCR, whose default
   model has no Devanagari and returned 177 characters of stray Latin on a Sanskrit
   page. With Tesseract `-l Devanagari` RAJM scores 97% and passes.
4. **ADH is not "51 tables with one data row each."** 205 of its 226 pipe blocks belong
   to a single page. See `EXTRACTION_FAILURES.md`.

## Artefacts

- `kb_audit/ocr_audit.json` — per-page measurements for every audited book
- `kb_audit/adh_orientation.json` — OSD angle and confidence for all 51 ADH pages
- `kb_audit/reocr_feasibility.json` — the settings comparison above
- `kb_audit/adh_p25_osd.json`, `kb_audit/adh_p25_native.json` — ADH page 25 readings
