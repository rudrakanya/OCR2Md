# Chapter 1, draft v6: revision of 19 October 2026 (depth and craft)

The units were not restructured: the 14 units still follow `editorial/Udaypur_Book_Contents.md`. No API calls were made. The new evidence was sliced verbatim from the local corpus Markdown with `_tools/kb_new.py` (27 kb-new items) and added to `evidence_pack_v6.json` with the new tool `_tools/pack_add_kbn.py`. The pack before this pass is backed up in the session scratchpad.

## Fuller use of evidence

| Unit | 17 Oct (body words / items) | 19 Oct (body words / items) | new corpus items |
|---|---|---|---|
| 1.1 The village today | 353 / 26 | 372 / 26 | 0 |
| 1.2 The living temple | 183 / 10 | 297 / 15 | 5 |
| 1.3 The walled town and its memories | 443 / 18 | 495 / 19 | 1 |
| 1.4 The names of the place | 284 / 20 | 293 / 22 | 0 |
| 1.5 Udayāditya and the Paramāra kingdom | 348 / 29 | 463 / 30 | 0 |
| 1.6 The foundation of town, temple and tank | 309 / 18 | 432 / 23 | 5 |
| 1.7 The date of the foundation | 563 / 34 | 562 / 34 | 0 |
| 1.8 Udaypur in the eastern province | 458 / 28 | 491 / 28 | 0 |
| 1.9 Later rulers and patrons | 447 / 29 | 540 / 31 | 0 |
| 1.10 The Udaypur praśasti | 416 / 26 | 468 / 31 | 4 |
| 1.11 The inscriptions and their first readers | 347 / 19 | 416 / 25 | 6 |
| 1.12 Stories of the temple's survival | 363 / 18 | 498 / 23 | 4 |
| 1.13 Udaypur among Paramāra monuments | 426 / 33 | 492 / 35 | 2 |
| 1.14 An earlier settlement? | 343 / 16 | 445 / 19 | 1 |
| **Total** | **5,283 / 303** | **6,264 / 332** | **27** |

- **Notes.** The reader-facing notes went from 85 to 62, one per paragraph. The working draft keeps every claim's IDs.
- **Units with little to add:**
  - 1.1, 1.4 and 1.7 already used nearly all their evidence. They gained particulars from items already cited (the literacy split; the six-line record, its *karaṇa* and the sun's transit; the place of the 1513 fragment's publication) rather than new items.
  - 1.2 is still the shortest unit. The rest of the worship evidence belongs to Ch 8.

## Examples of detail brought in

**From the corpus:**
- Śivarātri: “an unending stream of devotees lines up in front of the temple from the morning to the evening” [C01-KBN-PANDE-001].
- The *liṅga* Beglar saw: “a large black stone lingam now enclosed in a shell of highly polished yellow metal said to be gold” [C01-KBN-PANDE-002].
- The full snake legend, including the site “at that time only a tiny village” [C01-KBN-GANGULY-001–004]. The source note points to Cunningham's reports [C01-KBN-GANGULY-005].
- The first slab: 22 unnumbered verses that break off ten syllables into the 23rd [C01-KBN-CII-001]. Bhoja “covered the world all around with temples” [C01-KBN-CII-002], and the closing verse on the Boar [C01-KBN-CII-003].
- The serpentine slab, 70 cm of pinkish sandstone: “may the protector cause this serpentine sword of letters to protect” [C01-KBN-SERPENT-001–003]. Its Ujjain twin is “marked with Udayāditya’s name” [C01-KBN-SERPENT-004, -006].
- Beglar's version of the Aurangzeb legend: the dream, the illness, the gunpowder taken out, and the order to revere Mahadeva before praying in the mosque [C01-KBN-PANDE-004–007].
- Hardy's three imperial monuments [C01-KBN-HARDY-001, -002].

**From items already cited:**
- the Kalacuri records at Bheraghat and Karnbel that call Udayāditya king of Malwa and lord of Dhārā [C01-KB-GANGULY-004];
- Beglar's description of the mosque: four rows of twelve pillars and the masons' marks [C01-KB-PANDE-003];
- the granted village, Umaratha [C01-GANGULY-010];
- the bilingual Persian–Sanskrit inscriptions of the 1488 mosque [C07-MADHYABHARAT-012].

## Craft

- **Openings.** Each unit now opens on something concrete: the road, the Śivarātri crowd, Teen Darwaza, the Boar verse, the six-line record, the Nēmaka inscription, the mosque's pillared hall, the broken slab, the serpent slab, the gunpowder, the spire, Bhujariya Talab.
- **Context** comes just before it is needed (the kingdom's divisions before the Caulukya governors, for example).
- **Handovers.** Each unit hands over to the next: 1.7 ends on the prince's seat and 1.8 opens on a seat for others; 1.9 ends with Garde and 1.10 opens with his find; 1.11 points ahead to the mosque dispute in 1.12.
- **The close into Chapter 2.** 1.14 now ends on the ground both founding answers stand on: sandstone quarried beside the older tank, black cotton soil, and water held [C01-KB-GEOHER-008; C01-KB-GEOHER-005; C01-JAGTA-EN-012].

## Spelling at first mention

The familiar forms are given once, in the body, at the first mention of each house in 1.5: Kalacuris (Kalachuris), Candellas (Chandelas), Caulukya (Chaulukya), Cālukyas (Chalukyas). The IAST forms follow everywhere else. `_tools/dynasty_spelling.py` now accepts a bracketed familiar form only at the first mention of that name in the text checked, and still blocks stray forms. It passes on the stitched chapter and on the footnoted version.

## Checks

- **All 14 units are clean** under `inhouse.py check`, with no length checks. The checks cover verbatim quotations, valid IDs, names and numbers, source-led sentences, agent nouns, narrator terms, testimony-as-measurement, passive runs, D1 spelling and the ledger.
- **AI-shape** (per 1,000 words): "not X but Y" 0.2, triplets 0.6, colon reveals cut from 1.6 to 0.3, and 0 for each of the rest.
- **Verification.** Every new detail was checked in-session against its item's full quotation. Two fixes came out of that: an OCR-garbled phrase ("Premial Boar") was paraphrased rather than quoted, and an unsupported journal-title expansion was replaced by the source's abbreviation.

## Editorial read against the 14 questions

- **All 14 units pass.**
- **Marginal points:**
  - 1.8 P3, Q9: the paragraph glossing the terms of government is kept short;
  - 1.9 P3, Q9: the Malwa sultans sentence leans towards Ch 10;
  - 1.13 P3, Q11: the run of attributed verdicts.

## Deliverables

- `drafting/ch01/ch01_draft_v6.md`: the working draft, with IDs.
- `drafting/ch01/ch01_draft_v6_footnoted.md`: 62 notes and 17 bibliography entries.
- `drafting/ch01/Chapter 1 - Udaypur - Draft v6.docx`: all 14 units present, none empty, 297–562 words each.
- The ledger: `run/ledger/ledger_ch1.json`, merged into `editorial/book_ledger.md`.
