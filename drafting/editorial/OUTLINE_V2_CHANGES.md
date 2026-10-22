# Master Drafting Outline v2: changes from v1

*16 October 2026. v2: `Chapter_4_to_Afterword_Master_Drafting_Outline_v2.md`, about 34,700 words. v1 is kept unchanged (last written 15 Oct, 17:55). Built with no API calls of any kind. The coverage and checks are scripted and free. The judgement work was verified in-session, not by an independent model.*

## 1. The six resolutions (recorded once in Part I; log in I.9)

| Flag | Resolution | Where |
|---|---|---|
| C1-A, the governors | Settled as **U1**. Rājyapāla (V.S. 1220 = 1163, under Kumārapāla) and Lūṇapasāka (early 1170s, under Ajayapāla) governed for the Caulukya kings. The mahākumāras held the region "at least up to 1157". No date is recorded for the Paramāra return. | I.1 U1 |
| C1-B, the late records | Evidence rule **R1**. Three records are kept separate and labelled: Record A, the 1513 record; Record B, the V.S. 1562 Udayapura pedigree; Record C, the 22-line V.S. 1116 inscription read by Verma and INTACH. | I.2 R1 |
| Ch 9 length | **U2** is kept as an approved exception at 2,800. A re-check found all 32 direct items assigned or reasoned, and no further Udaypur-specific material on the town's languages or quarters. | I.1 U2, I.6 |
| Karṇa | Evidence rule **R2**. Karṇa is always named by dynasty: Kalachuri (c. 1041–72) or Caulukya (1064–94). Where an item does not say which, he stays unspecified and the statement is attributed. The index has 24 Karṇa-the-king items: 10 Kalachuri, 6 Caulukya, 8 unspecified (Part V, RR-K). | I.2 R2; V RR-K |
| The V.S. 1116 records | Evidence rule **R3**. They stay distinct until checked against Bühler and Cunningham. This is a research task, RR-1, which waits on the staged sources. | I.2 R3; V RR-1 |
| Administrative geography | Evidence rule **R4**. No administrative term is used before its earliest attesting record: the Bhāillasvāmi-mahādvādaśaka and Bhṛṅgārikā in the 1170s; the "eastern division" in 1163; the Mahādvādaśaka-maṇḍala in the twelfth century. §4.6 is the model. | I.2 R4 |

## 2. Structural changes by chapter

Each chapter now has 4–8 sections, sized to its evidence. The full lists are in each entry's "Changes from v1".

| Unit | v1 sections → v2 | Target (v1 → v2) | Main change |
|---|---|---|---|
| Ch 4 | 5 → 6 | 4,150 → 5,000 (U9) | v1 4.3 P5 becomes §4.4 "Who Udayāditya was"; 4.4 → §4.5 (U6 wording); 4.5 → §4.6 |
| Ch 5 | 5 → 7 | 4,000 | the tower and the comparison split; the image programme split; §5.7 closes on the flag-bearer |
| Ch 6 | 5 → 8 | 4,050 | other early writing (§6.2) and the praśasti's reliability (§6.4) become their own sections; the porch archive runs 1163–1232 under U1; after 1232 (§6.7); the limits of the stones (§6.8, 200 w) |
| Ch 7 | 5 → 7 | 4,250 | the hill's sculpture becomes §7.2 (U4 is superseded in effect; §7.1 is back to 750); water is split into §7.6 and the tanks (§7.7) |
| Ch 8 | 5 → 7 | 3,800 | the Paramāra-era market and later trades split; worship and service split |
| Ch 9 | 4 → 6 | 2,800 (U2) | new §9.2 on the society the town was founded into; the tellers and Bhoja's fame split |
| Ch 10 | 5 → 6 | 4,200 | §10.6 "What 'decline' means" is split from §10.5; §10.1 opens on V.S. 1220 under U1 |
| Ch 11 | 5 → 6 | 4,250 | §11.5 "The palace and the order" (2021; U7, LR-1) is split from the record of loss (§11.6) |
| Ch 12 | 5 → 6 | 3,750 | visitors (§12.4) and the town becoming visible (§12.5) split |
| Afterword | 5 → 6 | 2,750 (U3) | AW.4 "Testing them against the book" is split from the proposals |

**Totals:** 49 → 65 sections. The targets are unchanged except Ch 4, which goes up by 850 words, to 38,850.

**Elsewhere in the document:**
- the sections are renumbered;
- the cross-references, Contents, Part I.3–I.5 and Parts III–VI are updated to the new numbers;
- Part III, A gives the new chain of chapters;
- Part III, H lists the redundancies removed (checked against v1).

## 3. Coverage by chapter (direct items)

Every direct item has one status, and none is unreasoned (`_tools/coverage_v2.py`). The per-sub-topic tables and the full exclusion lists (ID and reason) are in the Appendix.

| Unit | Direct | Assigned | Cross-ref | Excluded | Main exclusion reasons |
|---|---|---|---|---|---|
| Ch 4 | 221 | 89 | 18 | 114 | Verma's renderings via Tiwari (T8) of verses CII edits; Hindi originals; testimony restating T1/T5 facts (R5) |
| Ch 5 | 284 | 204 | 24 | 56 | Temple Economics (17); v1 reasons |
| Ch 6 | 223 | 186 | 5 | 32 | Hindi originals (10); v1 reasons |
| Ch 7 | 239 | 147 | 14 | 78 | Hindi originals (33); Temple Economics (5) |
| Ch 8 | 44 | 35 | 3 | 6 | — |
| Ch 9 | 32 | 29 | 2 | 1 | C09-GAZ-011 (Kham Baba is at Besnagar) |
| Ch 10 | 61 | 37 | 1 | 23 | v1 reasons; Hindi originals (2) |
| Ch 11 | 92 | 74 | 0 | 18 | v1 reasons; Hindi originals (3) |
| Ch 12 | 71 | 56 | 4 | 11 | v1 reasons |
| Afterword | 58 | 54 | 1 | 3 | v1 reasons |

**Scripted checks** (`_tools/checks_v2.py`; log in `plan_v2/qc_v2.md`):
- every ID exists;
- the quotations are verbatim;
- no item is primary (E) in two units;
- the section targets sum to the chapter targets;
- the hand-offs match Part III, A;
- the R1, R2 and R4 heuristics are clean.

Two Gazetteer warnings (R8) are accepted, because these subjects rest on the Gazetteer alone:
- §8.5, 4 of 5 items;
- §10.5, 26 of 35.

## 4. Corrections made to Chapters 1–3 (and the delivered Ch 4)

All factual. Each was checked again with the free checks after the edit. Outputs were rebuilt with `_pipe/build_outputs.py` (Ch 1–3 and the combined document, 88 footnotes; Ch 4 separately). Backups are in the session scratchpad (`v2_backup/`).

1. **§1.2 (R2):**
   - "drove Karṇa and Bhīma out" → "the Kalacuri Karṇa and the Caulukya Bhīma";
   - "Some fifteen years later Karṇa returned" → "the Kalacuri Karṇa returned" (C01-KB-CII-007).

   In `run/ch1/1.2.md` and `ch01/ch01_draft_v5.md`.
2. **Ch 1 plan, `ch01/ch01_plan_v5.md` (R4, R1/R3; 3 places plus a header note):**
   - the "eastern division" is dated to 1163;
   - "the work read as begun in V.S. 1116 (a reading)";
   - the province is dated to the 1170s record.
3. **Ch 2 plan, `ch02/ch02_plan_v3.md` (R4):** line 36 now reads "the province in which a record of the early 1170s, under Caulukya rule, places Udayapura".
4. **Delivered Ch 4 (R2, minimal):**
   - §4.3: "names Karṇa, whom the editor takes for the Kalachuri king"; "the Kalachuri Karṇa, the Caulukya Bhīma" (spelling aligned with Ch 4's own "Caulukya" in a second pass, re-checked clean, outputs rebuilt 13:15);
   - §4.4: "the Caulukya Karṇa whom, in his account…"; "the Caulukya Karṇa's dates".

   Ch 4 outputs rebuilt.
5. **Checked and compliant, no change:** §1.4, §1.5, §2.1, §3.4 (dated terms; Records A–C kept apart). The U1 correction to §1.2/§1.3 (15 Oct) is present in the sections and the `.docx`.

## 5. For the user's decision (Part I, I.8)

- **D1. Dynasty-name spelling.** Ch 1 uses Candella / Kalacuri / Caulukya, Ch 3 Chandella, and Ch 4 Chandella / Kalachuri / Caulukya ("Chālukya" for the Deccan house throughout). *Default if no ruling:* CII's forms, aligning Ch 1 at its next revision.
- **D2. The kinship canon.** CII's editor treats Udayāditya as "definitely" Bhoja's brother (C04-CII-076, -080, -083). The canon is "a kinsman of Bhoja; the exact relationship is disputed". Keep or revise?
- **D3. Ch 4 restructure.**
  - *Draft:* five sections (4.1 659 · 4.2 701 · 4.3 864 · 4.4 887 · 4.5 915 words).
  - *v2:* six sections. A revision would:
    - split draft 4.3 at its last paragraph group ("who Udayāditya was") into a new §4.4 bridge;
    - renumber 4.4 → §4.5 and 4.5 → §4.6;
    - rewrite the two transitions around the new section;
    - update the footnote order and cross-references.

    It needs no new evidence and adds no words, so the length stays about 4,030, still evidence-limited against 5,000. *The draft is not rewritten pending your decision.*
- **D4. Ch 1 interpretive items** (no change made):
  - §1.2's Nagpur paraphrase "Karṇa and the Karṇāṭas had seized" leaves Karṇa unspecified. R2 allows this because it is attributed, but the item is unspecified in its source (RR-K), so it could be glossed or left.
  - The D1 spelling in §1.2–§1.3.

## 6. Other changes

- **Front matter:**
  - purpose and how to read;
  - a generated status table (sections, targets, coverage, open tasks);
  - a full Contents;
  - the Ch 1–3 Baseline carried from v1, with the C1-A pointers replaced by U1.
- **Part I** is rewritten as:
  - decisions U1–U9 (dated);
  - rules R1–R9;
  - homes;
  - boundaries;
  - length bases;
  - the retired material (carried from v1);
  - the decisions still needed (D1–D4);
  - the resolution log.

  "Needs a ruling" now appears only for D1–D4.
- **Part II entries** are in the v1 component format, cite rules and decisions by number, and are free of merge and process notes. Each has its own short research list pointing to the register.
- **Part V** is a single Research Register: RR-1 to RR-33, LR-1 and LR-2, with owner, what each blocks, and status; and the RR-K item list. RR-9 (INTACH's 82 × 42 m) is closed as excluded.
- **New free tools:**
  - `_tools/index_evidence_maps.py`;
  - `coverage_v2.py`;
  - `v1_exclusions.py`;
  - `checks_v2.py`;
  - `fill_roles.py`;
  - `assemble_v2.py`, which rebuilds the whole document, the status table and the Appendix from `plan_v2/`.
