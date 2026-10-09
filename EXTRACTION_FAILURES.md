# Structured-content extraction failures

**Date:** 2026-10-05 · **Scope:** the 27 registered sources · **Companion to:** `OCR_AUDIT.md`
**Constraint observed:** audit only — nothing was re-embedded, no store was written to, no file restored.

Phase 1 measured whether text was *dropped*. This records what was dropped or
**invented** in content that is not running prose: tables, inventories, captions and
inscriptions. Two failures matter for a book that cites its knowledge base, and one of
them is worse than data loss.

---

## 1. ADH — a vision model collapsed on a sideways inventory table

**Source:** ADH · `adhikari-2013-un` · Swati Mondal Adhikari, *Some Paramāra Temples
From Madhya Pradesh: A Case Study of Village Un* · 51-page image-only scan, zero text
layer, 72 dpi effective, **every page stored rotated 270°**.

### What the page actually holds

PDF page 25 (printed pages 42–43) is a wide **Sapta Mātṛkā iconographic inventory**,
set sideways across the leaf. Read at native resolution with the page rotated upright,
it yields clean text and five deity rows, each with four hand attributes and a mount
column:

| Image | Location | Posture | Hands | Other |
|---|---|---|---|---|
| Vārāhī | niche in left side | lalitāsana | U.R. indistinct · U.L. indistinct · L.R. akṣamālā · L.L. indistinct | mount damaged |
| Maheśvarī | niche in the centre | lalitāsana | U.R. triśūla · U.L. sarpa · L.R. akṣamālā · L.L. indistinct | mount present |
| Vaiṣṇavī | next niche, right side | lalitāsana | U.R. damaged · U.L. cakra · L.R. akṣamālā · L.L. indistinct | mount present |
| Goddess (unidentified) | niche in right side | resting in lalitāsana | hands damaged | mount damaged |
| Śiva (four-handed) | — | padmāsana | U.R. triśūla · U.L. sarpa · L.R. & L.L. in dhyānamudrā | jaṭāmukuṭa, bejewelled, mount absent |

### What reached the markdown

The markdown's page-25 section contains **464 pipe lines, 259 with content — and only
8 of them distinct**:

| Count | Line |
|---|---|
| ×205 | the header `Image / Island / Attribution / Other features` |
| ×45 | `Siva (four handed) / Padmāraṇa / U.K. (rāhīna) U.L. (sarpa) / Jñābhadras, bhāyārāśa, manna dharm` |
| ×4 | the same row with `L.R. & L.L. - in dhyanamudra` appended |
| ×1 each | four single rows for Vārāhī, Maheśvarī, Vaiṣṇavī and the unidentified goddess |
| ×1 | an empty row followed by `[{"box_2d": [398, 500, 883, 777], "label": "text", "caption": "pīrāṇaṇaṃ (pīrāṇaṇaṇaṃ) (pīrāṇaṇaṇaṇaṃ) …` |

That last line is the diagnosis. `box_2d` is a **vision-language model's raw JSON
output**, and its caption field is a textbook degenerate-decoding loop
(`pīrāṇaṇaṃ` → `pīrāṇaṇaṇaṃ` → `pīrāṇaṇaṇaṇaṃ` …). ADH's markdown was not produced by
Tesseract at all; it was produced by a vision model which, handed a sideways wide
table, entered a repetition collapse — emitting the header 205 times and one row 45
times instead of the table's rows.

### Why this is worse than lost text

The four rows that *did* survive carry **fabricated iconographic attributes**. This is
not garbling a reader would notice; it reads as confident scholarly data:

| On the page | In the knowledge base |
|---|---|
| `Location` (column header) | `Island` |
| Vārāhī | `Vāraṇi` |
| Maheśvarī | `Māhukaraṇi` |
| Vaiṣṇavī | `Vayyāni` |
| lalitāsana | `Lalāśama` |
| akṣamālā, triśūla (distinct attributes) | both replaced by the invented token `(rāhīna)` |
| jaṭāmukuṭa, bejewelled, mount absent | `Jñābhadras, bhāyārāśa, manna dharm` |

`rāhīna`, `Jñābhadras`, `bhāyārāśa` and `manna dharm` are not words. Every hand
attribute in the surviving rows has been overwritten with the same invented token, so
the rows assert iconography the temple does not have.

### How much is in the store, and how exposed it is

| Measure | Value |
|---|---|
| ADH chunks total | 328 |
| chunks carrying the collapse | **50 (15% of ADH)** |
| `claim_bearing` | 1 on all 50 |
| `epistemic_status` | `factual` on all 50 |
| `is_quarantined` | 0 on all 50 |
| `review_status` | null on all 50 |
| chapter buckets (sqlite column) | **C7: 50 · C10: 49** · C2, C4, C8, C12: 1 each |
| **vectors in `udaypur_kb`** | **0 of 50** |
| `box_2d` JSON leaked into chunks | 0 — the chunker filtered it |

So the raw model JSON was caught, but the fabricated table rows were not. Fifty chunks
marked `factual` and claim-bearing, none quarantined or flagged for review, carry
C7 and C10 bucket values — the chapters most likely to describe sculpture.

**They are not retrievable, though.** None of the 50 has a vector in `udaypur_kb`:
Chroma holds 280 ADH rows against sqlite's 328, and the 48 missing are exactly the
duplicate-hash rows, so the embedding step collapsed each repeated row to a single
vector and the repetition never entered the vector space. A chapter brief, which
retrieves through Chroma, cannot surface them.

The residual risk is therefore narrower than it first appears, but it is not zero: the
rows remain in `kb_active.sqlite` labelled `factual`, `claim_bearing = 1`,
`is_quarantined = 0`, with C7/C10 bucket values, so **any tool that reads the sqlite
chunk table directly — a fact extractor, a coverage count, a sourcebook build — will
treat them as evidence.** That is why quarantining them still ranks first below.

**Recoverable:** **yes.** The true rows above were read in this audit from the original
page. Re-extraction needs the page rotated upright before OCR; `--psm 6` after rotation
preserves the column structure.

---

## 2. PAT — one Patil volume registered three times

Not an OCR failure, but a structured-provenance failure with the same consequence: the
knowledge base can present one source as several.

| Code | source_id | Title | Chunks |
|---|---|---|---|
| PAT-CH | `patil-1952` | The Cultural Heritage of Madhya Bharat | 387 |
| PAT-TEM | `patil-composite-temples` | …— temples and architecture (composite) | 214 |
| PAT-INS | `patil-composite-inscriptions` | Archaeological & Cultural Heritage of Madhya Bharat… | 143 |

Measured by exact `content_hash`:

| Overlap | Shared chunks | Share |
|---|---|---|
| PAT-CH ∩ PAT-TEM | **120** | 31% of PAT-CH, **56% of PAT-TEM** |
| PAT-CH ∩ PAT-INS | 6 | 2% / 4% |
| PAT-TEM ∩ PAT-INS | 6 | 3% / 4% |

- Median duplicated chunk: **533 characters** — substantive passages, not boilerplate
  (only 6 of the 120 cross-source groups are under 200 characters).
- `claim_bearing` is 1 on all 246 chunks in those groups.
- All three codes appear together in **every one of the 16 chapter buckets**.

**What is *not* wrong:** corroboration metadata is not inflated —
`corroboration_count` is 0 for 242 of the 246, and **no chunk cites its own duplicate
as corroboration**. I checked this specifically because it was the obvious risk.

**What is wrong:** the drafter cites by source code. A retrieval that returns the same
Patil passage under PAT-CH and PAT-TEM hands the drafter what looks like two
independent authorities for one claim, and more than half of PAT-TEM is exposed to
this. The sourcebook's coverage matrix counts them as separate works too.

**Recoverable:** yes, and without re-OCR — this is a registry and de-duplication fix,
not an extraction fix. It needs your decision, so nothing has been changed.

---

## 3. GUP — plates and sideways tables, prose intact

**Source:** GUP · *Iconography of Hindus, Buddhists and Jains* (Gupte) · 266 pages,
image-only.

GUP's 41% mean recall is not uniform loss. It splits by page type:

| Page type | Example pages | Recall |
|---|---|---|
| prose | 22, 54, 173 | 95%, 82%, 81% |
| sideways comparative tables | 118, 181 | **2%, 6%** |
| plates | 213, 245 | 20%, no text |

Pages 118 and 181 OCR'd to 1,162 and 1,317 characters of rotated-text soup
(`potest ue Bujpurrg`, `BesPpesy Uy SUNG`), and **no probe phrase from either page
appears anywhere in GUP's markdown**. Those are the book's comparative iconographic
tables, and their content is absent from the knowledge base.

**Captions, by contrast, survived**: 84 caption-style lines, 223 inline `Fig./Pl.`
references, 390 image references, and the plate deity names are present
(`Ratnasambhava` 12×, `Tara` 8×, `Samantabhadra` 4×, `Vajradhat…` 2×). The plate pages
are therefore not a silent loss — the figure is referenced even where the image is not
transcribed.

**Recoverable:** yes for the sideways tables, with orientation correction. Perhaps
10–20 pages, not the whole book.

---

## 4. Everything else — negligible

Within-source duplication across the whole corpus, by exact `content_hash`:

| Source | Redundant chunks | Of total |
|---|---|---|
| `adhikari-2013-un` (ADH) | 48 | 328 (15%) |
| `ganguly-paramara` (GAN) | 3 | 706 (0.4%) |
| `samarangana` (SAM) | 2 | 1,381 (0.1%) |
| `tiwari-jhk-hi` (TIW-H) | 1 | 609 |
| `singh-temple-economics` (SIN-T) | 1 | 1,453 |

No other source shows a repetition-collapse signature. The earlier finding that
**PAT-INS's seven tables held "zero data rows" was wrong and is withdrawn** — they are
ASCII-art tables whose logical rows span two printed lines, and the Un-cluster timeline
is fully present.

---

## Ranked remediation

| Rank | Action | Why it ranks here | Blocking? |
|---|---|---|---|
| 1 | Quarantine the 50 ADH collapse chunks | they assert fabricated iconography as `factual` and unquarantined in `kb_active.sqlite`; unretrievable today, but any sqlite-reading tool treats them as evidence | **yes — needs your go-ahead to write** |
| 2 | Re-extract ADH page 25 and its table pages, rotated upright | the true rows are recoverable and are the chapter's actual evidence | no |
| 3 | Resolve the three Patil registrations into one work with sections | 56% of PAT-TEM duplicates PAT-CH across all 16 buckets | no |
| 4 | Re-OCR GUP's rotated table pages | comparative iconographic tables absent from the KB | no |

Items 1 and 3 change the store or the registry, so neither has been done.

---

## Correction to an earlier claim in this audit

I previously reported that ADH was **the only one of 27 sources with repeated-chunk
runs**. That holds for *within-source* repetition (48 of the 55 such redundant chunks
are ADH's), but the figure I gave alongside it — a per-source tally of corpus-wide
duplicates showing `patil-1952` at 126 — was wrong. The query grouped by
`content_hash` while selecting `parent_source_id`, so SQLite returned an arbitrary
member of each group and attributed cross-source duplicates to whichever source it
happened to pick. Re-measured correctly: **10 duplicate groups fall within one source
(55 redundant chunks) and 120 span different sources (126 redundant chunks)**, and the
cross-source figure is the Patil triple-registration in §2 — a real finding, but a
different one from what that tally appeared to say.

## Artefacts

- `kb_audit/adh_page_tables.json` — pipe blocks attributed to each ADH source page
- `kb_audit/adh_p25_osd.json` — page 25 read at four orientations, with OSD angles
- `kb_audit/adh_orientation.json` — OSD angle and confidence for all 51 ADH pages
- `kb_audit/adh_p25_native.json` — native-resolution readings of pages 24–26
