# Chapter 6 — draft v3 report (22 Oct 2026)

**Brief.** Bring every unit to the depth of the revised serpentine unit (6.9) from its own direct and contextual evidence, then smooth the whole chapter. In-session; no API calls; no embedding.

## Method
- **6.9.** Checked against Saarthak Singh's paper. It already adapted the full explanation. It was deepened with the source's own technical terms (*svara*, *antaḥstha*, *sparśa*, *ūṣman*; labial/guttural). Singh's point that the Ujjain inscription praises Śiva as language itself went to 6.10, where the debate lives.
- **Mapping.** The 159 unused pack items were auto-mapped to units (`run/ch6/_inventory/candidates.md`).
- **Workers.** Five parallel workers each read every cited item, every candidate and the primary corpus passages for their units:
  - A: 6.1–6.3; B: 6.4–6.8; C: 6.10–6.14; D: 6.15–6.19; E: 6.20–6.22.
  - Each wrote an inventory, added verbatim corpus slices (179 new `C06-KBN-<CODE>-<A–E>-NNN` items), rewrote and verified its units, and ran the free check.
  - Each worked in an isolated cfg and pack (`ch06/_work/`).
- **Merge and line edit (lead session).** Packs merged into pack v3 (631 items) and cfg/plan v3. Then an author's pass and line edit across all 22 units:
  - joins: 6.3→6.4, 6.8→6.9, 6.11→6.12, 6.14→6.15, 6.19→6.20;
  - repetition: the Māndhātā grant reduced to a recall in 6.14 (home 6.17); a repeated *kavirāja* point in 6.12; a repeated "reached print" in 6.4;
  - a reader-facing draft-history note in 6.7;
  - a banned phrase in 6.12;
  - a long sentence in 6.21;
  - the R3 wording in 6.2.

The full inventory is in `ch06_v3_evidence_inventory.md`.

## Units: before (v2) → after (v3)

| Unit | Words | Distinct IDs cited | New KBN items cited | Paragraphs | Depth |
|---|---|---|---|---|---|
| 6.1 | 333 → 368 | 12 → 22 | 9 | 2 | FULL (six-line record) |
| 6.2 | 342 → 528 | 11 → 20 | 9 | 2 | LIMITED (HELD RR-1) |
| 6.3 | 298 → 603 | 9 → 23 | 14 | 3 | FULL |
| 6.4 | 320 → 551 | 12 → 19 | 6 | 3 | FULL |
| 6.5 | 375 → 680 | 16 → 36 | 18 | 5 | FULL |
| 6.6 | 438 → 658 | 17 → 33 | 14 | 4 | FULL |
| 6.7 | 424 → 649 | 22 → 39 | 16 | 4 | FULL |
| 6.8 | 335 → 526 | 12 → 23 | 9 | 3 | FULL for the house; LIMITED for Udaypur |
| 6.9 | 846 → 875 | 40 → 40 | 36 | 5 | FULL (checked; terms added) |
| 6.10 | 441 → 858 | 18 → 33 | 12 | 4 | FULL |
| 6.11 | 326 → 624 | 13 → 26 | 9 | 4 | FULL for Dhār; Udaypur has no hall |
| 6.12 | 360 → 571 | 17 → 28 | 4 | 4 | FULL, all contextual |
| 6.13 | 406 → 576 | 19 → 33 | 10 | 3 | FULL |
| 6.14 | 335 → 589 | 12 → 22 | 11 | 4 | FULL |
| 6.15 | 343 → 508 | 14 → 24 | 8 | 4 | FULL |
| 6.16 | 308 → 336 | 14 → 16 | 1 | 3 | LIMITED (no catalogue in corpus) |
| 6.17 | 351 → 656 | 8 → 22 | 10 | 3 | FULL |
| 6.18 | 453 → 761 | 21 → 40 | 16 | 4 | FULL |
| 6.19 | 141 → 275 | 7 → 11 | 4 | 3 | LIMITED (HELD RR-11/23) |
| 6.20 | 248 → 432 | 9 → 13 | 4 | 3 | LIMITED (no Persian text in corpus) |
| 6.21 | 236 → 380 | 9 → 14 | 6 | 2 | FULL for 1639; LIMITED for older lines |
| 6.22 | 295 → 357 | 13 → 19 | 3 | 3 | FULL as synthesis |
| **Total** | **7,954 → 12,361** | **498 distinct** | | | |

The 6.9 count of 36 "new" items is the C06-KBN-SERPENT items added in v2. "New KBN items cited" counts all kb-new items.

## Corrections to earlier drafts surfaced by the inventory
- 6.3: the date is fixed by the edition at Friday 23 June 1094 (v2 left three equivalents).
- 6.5: the two Vairisiṃhas, merged in v1, are separated (v. 8 pillars; v. 11 Dhārā).
- 6.6: the "queen's name in v. 11" belongs to another record and is moved to a note.
- 6.7: the Hūṇa victory goes to Sindhurāja (v. 16), not Sīyaka.
- 6.8: Somēśvara's praśasti is a Maru-mandala branch record.
- 6.12: the copper-plate verse pair is cut (home 6.17).
- 6.14: the Śrīkaṇṭha sentence is cut (duplicated 6.8).
- 6.16: the eight-line frame is at the Bija Mandal, not the temple porch; Tiwari's counts moved to notes.
- 6.20: "four centuries of Persian" (unsupported) is removed.
- 6.22: "Persian doorways known through single readers" is corrected.

## Flagged, not asserted
- *siddhāsiputrikā*: Singh only; Sastri, EI XXXI is not in the corpus.
- 6.2: the 22-line record matches the V.S. 1562 pedigree. It is kept apart (R1) and recorded for RR-1.
- 6.4: the first slab's find and size (CII p. 130 missing from the OCR).
- 6.8: the Udaypur poet's name. Tiwari's "got prepared by Udayaditya" names a patron.
- 6.6/6.7: verse-number disagreements; the Hūṇa discrepancy inside CII.
- 6.11: the Mandu hostel keeper (Tiwari only).
- 6.13: the date of Purantaka's grant, 1001 (Rajpurohit only).
- 6.18: *Mahākumāra* (Tiwari) against *Mahārāja* (CII); CII followed.
- 6.19: Jayasiṃha II or III; the 1366 record unedited in the corpus.
- 6.20: the INTACH appendix needs re-OCR.
- 6.21: the survey's "500 years" against its own 1639; the INTACH/survey cave lines are kept apart.

## Checks
- `inhouse.py check`: 22/22 clean. The remaining ledger notes are "figure may conflict" review heuristics.
- `ch_rules.py`: 0 failures.
- Ledger: Ch 6 terms 37, figures 22, open questions 17; `ledger.py merge` run.
- Build: 75 footnotes (v2: 53), all defined and referenced, none empty. The docx carries all 22 headings and the final hand-off sentence. The 15 incomplete bibliography entries are unchanged.

## Files
- cfg `cfg_ch06v3.py`, plan `ch06_plan_v3.md`, pack `evidence_pack_v3.json`.
- `ch06_draft_v3.md`, `ch06_draft_v3_footnoted.md`, `Chapter 6 - Inscriptions and Intellectual Life - Draft v3.docx`.
- Inventory `ch06_v3_evidence_inventory.md`.
- Backups of the v2 sections: `run/ch6/_v1/<sec>_v2.md`.
- New items are also kept per worker in `_work/kbn_<G>.jsonl`. They are not appended to the shared `evidence_index/kb_new.jsonl`; pack v3 is their record.
