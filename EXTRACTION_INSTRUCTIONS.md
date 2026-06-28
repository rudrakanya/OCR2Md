# Samaranganasūtradhāra — Verse Extraction Instructions

## Overview

Extract every Sanskrit verse from three scanned PDF segments of **Samaranganasūtradhāra Volume 2** (Mahārājādhirāja Śrī Bhojadeva Paramāra), translated into English by Sudarshan Kumar Sharma.

Produce **three separate Markdown files** — one per PDF.

---

## Source Files

| File | PDF Name | Chapters | Output |
|------|----------|----------|--------|
| 1 | `Samarangan_Vol2_Chapters_55-60.pdf` | 55–60 | `File1_Ch55-60.md` |
| 2 | `Samarangan_Vol2_Chapters_66-67.pdf` | 66–67 | `File2_Ch66-67.md` |
| 3 | `Samarangan_Vol2_Chapters_71-72.pdf` | 71–72 | `File3_Ch71-72.md` |

---

## Chapter Titles

| Chapter | Title |
|---------|-------|
| 55 | The definition of Meru and other sixteen modes of mansions |
| 56 | The Illustration of sixty four Prasadas headed by Rucaka |
| 57 | A twenty counting of Meru and others |
| 58 | The panegyric of palaces |
| 59 | The Definition of vimanas amounting sixty four |
| 60 | The Definition of Thirty six Prasadas headed by Sri Kuta |
| 66 | The Definition of a Mandapa i.e. a Pavilion |
| 67 | The definition of 27 pavilions (Mandapas) |
| 71 | Cittroddesa — The Painting Art |
| 72 | Bhūmibandha — Seasoning of the wall of painting |

---

## CRITICAL: Scanned Book — Visual Reading Required

These PDFs were produced via Adobe Scan. The OCR text layer is **garbled for Devanagari** — it outputs nonsense characters instead of actual Sanskrit. **You must visually read every page image. Do not rely on the embedded text layer for Devanagari under any circumstance.** Verify the English translation against the page image as well.

---

## Content Structure of Each Page

Each page contains:

1. **Devanagari** — the original Sanskrit text in bold Devanagari script
2. **English Translation** — printed directly below each verse in Roman type

There is **no IAST transliteration** in the source. The extractor generates it.

Verses typically span two lines of Devanagari (one pāda per line). Verse numbers appear as Devanagari numerals within double daṇḍas (e.g. ॥२४॥). Use the running headers on each page ("Chapter XX" and book page number) to identify chapter boundaries.

Each file may include a few buffer pages from adjacent chapters at the start or end. **Ignore those.** Extract only the chapters listed above for that file.

---

## Output Format

Structure each Markdown file exactly like this:

```markdown
# Chapter [X] — [Chapter Title]

---

### Verse [X].[Y]

**Sanskrit (Devanagari):**

[Exact Devanagari as it appears — do not alter]

**IAST Transliteration:**

[IAST transliteration of the above]

**English Translation:**

[Exact translation as it appears — do not alter]

> **Footnote [N]:** [footnote text, if any footnote is attached to this verse]

---

### Verse [X].[Y+1]
[...next verse...]
```

Repeat for every verse. Begin each new chapter with a `# Chapter` heading. Continue until every verse in every target chapter is extracted.

---

## IAST Transliteration Rules

| Devanagari | IAST |
|---|---|
| अ आ इ ई उ ऊ | a ā i ī u ū |
| ऋ ॠ ऌ | ṛ ṝ ḷ |
| ए ऐ ओ औ | e ai o au |
| क ख ग घ ङ | k kh g gh ṅ |
| च छ ज झ ञ | c ch j jh ñ |
| ट ठ ड ढ ण | ṭ ṭh ḍ ḍh ṇ |
| त थ द ध न | t th d dh n |
| प फ ब भ म | p ph b bh m |
| य र ल व | y r l v |
| श ष स ह | ś ṣ s h |
| ं | ṃ |
| ः | ḥ |
| ँ | m̐ |
| ् (virāma) | suppresses inherent vowel |
| ॐ | oṃ |

### Rules

- Preserve **sandhi** as written — do not split or resolve compounds.
- Transliterate **conjunct consonants** (samyuktākṣara) correctly without breaking them.
- The inherent vowel **a** is present unless a virāma (्) explicitly suppresses it.
- Anusvāra (ं) is always **ṃ** — do not context-assimilate it to ṅ, ñ, ṇ, n, or m.
- Visarga (ः) is always **ḥ**.
- Daṇḍa (।) and double daṇḍa (॥) are punctuation — reproduce as-is, do not transliterate.
- Convert Devanagari numerals in verse markers to Arabic numerals in the verse label.

---

## Constraints

1. **Visually read every page.** The OCR is broken for Devanagari. Do not use it.
2. **Extract only target chapters.** Skip buffer pages from adjacent chapters.
3. **Devanagari — verbatim.** Do not normalize, correct, or reorder. Flag unclear characters as `[UNCLEAR: …]`.
4. **Translation — verbatim.** Do not paraphrase or editorialize. Preserve the translator's exact wording.
5. **IAST — flag uncertainty.** If unsure about a character or conjunct, write `[IAST UNCERTAIN: …]` inline.
6. **Verse numbering** — use the format `Chapter.Verse` (e.g. 55.1, 55.2).
7. **Footnotes** — include at the end of the verse they annotate, as blockquotes.
8. **Preserve `(?)`** marks (editor uncertainty) and **`+++`** marks (manuscript damage) exactly as they appear.
9. **Do not skip any verse.** Every single verse must be extracted. No summaries, no omissions.
10. **No commentary.** Do not insert your own notes unless flagging a genuine ambiguity with `[FLAG: …]`.

---

## Handling Page Boundaries

- If a verse starts on a previous page and only the English translation is visible at the top of the current page, note `[FLAG: English continuation from previous page]` and include it with the previous verse.
- If a verse's Devanagari is visible but its English continues on the next page, include the Devanagari and note `[FLAG: English continues on next page]`.
- Chapter headings appear as `CHAPTER XX` in the source. When you see one, start a new `# Chapter [X] — [Title]` section.

---

## Completion Checklist

After finishing each file, append this summary table:

```markdown
## Extraction Summary

| Chapter | Title | Verses Extracted | Flags/Issues |
|---------|-------|-----------------|--------------|
| ... | ... | ... | ... |
```

---

## Automation Script Usage

The `extract_verses.py` script automates the extraction:

### Prerequisites

```bash
pip install anthropic pdf2image Pillow
# poppler-utils must be installed:
# macOS: brew install poppler
# Ubuntu/Debian: sudo apt-get install poppler-utils
```

### Run

```bash
export ANTHROPIC_API_KEY="sk-ant-..."

# Process all three files:
python extract_verses.py --pdf-dir . --output-dir ./output

# Process only one file:
python extract_verses.py --file 1 --pdf-dir . --output-dir ./output

# Resume after interruption:
python extract_verses.py --resume-file 1 --resume-page 25
```

### What the script does

For each PDF page:
1. Rasterizes the page to JPEG at 200 DPI
2. Base64-encodes the image
3. Sends it to `claude-sonnet-4-6` with the extraction system prompt
4. Appends the response to the output Markdown file
5. Saves a checkpoint file for resume capability
6. Rate-limits to avoid API throttling

### Estimated cost and time

- ~176 total pages across 3 files
- ~$2–4 in API costs (Sonnet 4.6 pricing)
- ~45–90 minutes runtime (with 2-second delays between requests)

---

## File-Specific Notes

### File 1 — Chapters 55–60 (141 pages)

This is by far the largest file. Chapter breakdown within the PDF:

| Chapter | Approximate PDF pages | Est. verses |
|---------|----------------------|-------------|
| 55 | 1–23 | ~160 |
| 56 | 24–65 | ~250 |
| 57 | 66–93 | ~170 |
| 58 | 94–97 | ~24 |
| 59 | 98–128 | ~186 |
| 60 | 129–141 | ~78 |

### File 2 — Chapters 66–67 (25 pages)

- Chapter 66: ~pages 1–10
- Chapter 67: ~pages 11–25
- The first page may contain tail-end content from Chapter 65 — skip it.

### File 3 — Chapters 71–72 (10 pages)

- Chapter 71: ~pages 1–4
- Chapter 72: ~pages 5–10
- The first page may contain tail-end content from Chapter 70 — skip it.
