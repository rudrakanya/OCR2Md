# Chapter 11, draft v1: Udaypur in the Modern Period (21 October 2026)

Drafted in-session from the contents file (`editorial/Udaypur_Book_Contents.md`, Chapter 11: 8 units). No API calls, Chroma queries or paid ledger runs were used. Verification was done in-session against the items' own text, not by an independent model.

## 0. State before work

- **No Chapter 11 draft existed.** There was no `ch11/` folder, plan, cfg, pack or `run/ch11/` sections. `drafting/ch11_modern-period.md` (13 Oct) is the evidence map only.
- **Contents file:** 8 units, from 11.1 (the first reports, 1871–1914) to 11.8 (quarrying, blasting and grazing). Used as listed: no unit added, dropped, split or merged.
- **v2 outline:** 6 sections, 4,250 words (not a target). Its item map, opening (Beglar's tour) and closing (the people at the record's edges) were carried over the 8 units: v2 §11.3 was divided between 11.3 and 11.4, and v2 §11.6 between 11.7 and 11.8.
- **Evidence:** `ch11.jsonl` holds 109 items (92 direct, 17 contextual). The pack (`ch11/evidence_pack_v1.json`, built by `ch11/build_pack_v1.py`) has 158: the index less the four Temple Economics items (R9), plus 53 borrowed recalls from Chapters 1, 2, 5, 6, 7, 10, 12 and the Afterword.
- **Parallel work:** other sessions were drafting Chapters 10, 12 and 13 at the same time. Ch 11 opens from Ch 10's planned close (cfg_ch10v1: the officials' "once a place of considerable importance") and closes into Ch 12's planned opening (below the hill, on the census). Shared files (`stitch.py`, `build_outputs.py`, the book ledger) were changed by one-line additions only.

## 1. The colonial editions: status and HELD passages

The staged editions in `public_domain_staging/` are unchanged since 14–15 October: Beglar (ASR VII), Cunningham (ASR X), Bühler (*EI* I) and the Gwalior report of 1925–26. They remain **uncorrected and not ingested** (R9). The reports are this chapter's subject, so they are told through the ingested sources that quote or cite them: Pande, Patil, Ganguly, Kramrisch, CII and Tiwari. Nothing is quoted from the staged copies.

**HELD notes (release when the editions are corrected and ingested):**

| Unit | What waits | Register |
|---|---|---|
| 11.1 P1 | Beglar's own text: the seven shrines and the plate (Pande's quotation used meanwhile) | RR-8, RR-15 |
| 11.1 P4 | Cunningham's page for the 1080 record (Tiwari cites p. 83; the staged Udaypur pages are 65–69); the year of Bühler's volume (Tiwari: 1888; the staged title page bears 1892) | RR-1, RR-12, RR-32 |
| 11.2 P2 | The Gwalior report of 1925–26 on the second slab (CII used) | RR-32 |
| 11.2 P3 | The scope of the 1923–29 restoration campaigns | RR-32 |

**Found in the author's pass:** Tiwari dates both the seventh and the tenth reports to 1874–75 and 1876–77, but the seventh is Beglar's tour of 1871–72 (Pande's citation). 11.1 now gives "Beglar's and Cunningham's" and explains in a note. **Chapter 1 §1.11 repeats Tiwari's dates** ("for 1874–75 and 1876–77") and needs the same light fix.

## Files

| Item | Path |
|---|---|
| Plan | `ch11/ch11_plan_v1.md` |
| cfg | `ch11/cfg_ch11v1.py`: NO_LENGTH; Gazetteer ≤ 0.40. Extra rules: claimants, residents or the junior official named → fail; the mining allegation in more than one body sentence → fail; Tiwari's figures (lakh, crore, hectares, 980, 42, "hundred inscriptions") in body text → fail; Temple Economics → fail; narrator period terms; anonymous agents; R2, R3. |
| Pack | `ch11/evidence_pack_v1.json` (158), built by `ch11/build_pack_v1.py` |
| Sections | `run/ch11/11.1–11.8.md` |
| Ledger | `run/ledger/ledger_ch11.json`, merged into `editorial/book_ledger.*` |
| Check helper | `ch11/chk.sh 11.N` (free `inhouse.py check`, condensed) |

## Units

| Unit | Body words | Items cited | Ch 11 items | Notes |
|---|---|---|---|---|
| 11.1 The First Archaeological Reports, 1871–1914 *(HELD notes)* | 719 | 24 | 6 | 5 |
| 11.2 Gwalior State Archaeology *(HELD notes)* | 482 | 14 | 8 | 4 |
| 11.3 Protection after Independence *(legal review)* | 495 | 26 | 17 | 4 |
| 11.4 The Temple's Clearance under the ASI *(thin; legal review)* | 208 | 6 | 6 | 2 |
| 11.5 The INTACH Documentation, 2020–21 | 528 | 24 | 15 | 4 |
| 11.6 The Palace and the 2021 Revenue Order *(legal review; U7)* | 387 | 21 | 17 | 3 |
| 11.7 Stolen and Defaced Sculpture *(thin; legal review)* | 294 | 7 | 7 | 2 |
| 11.8 Quarrying, Blasting and Grazing on the Hill *(legal review; U7)* | 437 | 12 | 10 | 3 |
| **Total** | **3,550** | **125 distinct** | **79 of 109** (75 of 92 direct) | **27** |

The body runs 3,550 words (about 4,750 with notes), under the outline's 4,250, because the evidence ends there. No unit was padded. **Thin units:** 11.4 rests on one officer's recollection; 11.7 on one theft and one survey's two paragraphs.

**Direct items set aside (17), with reasons:**
- C11-JAGTA-HI-003, -004: Hindi duplicates of EN-004, EN-005 (used).
- C11-JAGTA-HI-002: Tiwari's appeal for "a good person like Alexander Cunningham" (opinion; Afterword).
- C11-JAGTA-HI-023: "We are responsible" (opinion; Afterword).
- C11-JAGTA-HI-024: the notice with the claimants' names (U7).
- C11-JAGTA-HI-027, -028: the naib tehsildar named and praised; the claimant's status mocked (living persons; U7).
- C11-JAGTA-HI-031: abuse of officials ("dull-witted functionaries").
- C11-JAGTA-HI-034: duplicate of EN-036 (in the 11.3 note).
- C11-JAGTA-HI-036, C11-JAGTA-EN-037: "a madrasa came to occupy the palace" (contested; the legal reviewer to decide).
- C11-JAGTA-HI-037: the "so-called place of worship" and green cloths (Ch 12/Afterword, as in Ch 9).
- C11-JAGTA-EN-020: an archaeology official criticised by name (living person).
- C11-JAGTA-EN-023: polemic on the occupiers.
- C11-JAGTA-EN-034: ASI staff and visitors (Ch 12.6).
- C11-JAGTA-EN-035: the district archaeology association (opinion).
- C11-CII-002: the Amerā inscription (not Udaypur).

**Contextual set aside:** the four Temple Economics items (R9); C11-CII-003 (Nagpur Museum inscription), C11-CII-004/-005 (the Vidisha pillar inscription), none of them Udaypur; C11-JAGTA-EN-001/-002/-007 (Cunningham's career elsewhere; the ASI's founding year is testimony, R5); C11-JAGTA-HI-033 (party-political judgement); C11-JAGTA-HI-035 (Sonari village); C11-HARDY-001 (national documentation).

**One-home scan:** every chapter index was searched for unused items on archaeology, protection, museums and INTACH. Added from drafted chapters: C07-JAGTA-HI-064 (Upadhyay's tour), C07-JAGTA-HI-042 (the tank measured), C07-KRAM-1-001 (Kramrisch's eight-temple composition), C01-KRAM-1-001 (her plan taken from ASR VII Pl. VI), C06-JAGTA-HI-029 and -013 (the find-place and the Gwalior report reference). Items homed in the undrafted Chapters 10, 12 and 13 were recalled in clauses only.

## 2. Passages flagged for legal review

Each flag is also in the passage's own note ("For legal review").

| # | Unit / paragraph | Matter | Treatment |
|---|---|---|---|
| 1 | **11.3 P3** (LR-3, new) | Spending by the state department at Udaypur, from an unnamed official via Tiwari: 1.10 crore in five years, 67 lakh on one mosque, 76 lakh on two | No figure in the text; "more than half … went to one of them", attributed to "an officer who saw the budget files". Figures only in the note, as Tiwari's report, marked not adopted. |
| 2 | **11.3 P2** | The four state monuments, two of them mosques | Factual list, attributed in the note (Tiwari, INTACH). |
| 3 | **11.4 P2** (LR-3) | Two households living beside the temple | Not named. Tiwari's word "encroachment" and his guess at their motive are not adopted. |
| 4 | **11.4 P1** | Narayan Vyas (named; living, presumably) | His recollection only, attributed; year and depth in the note as memory. |
| 5 | **11.5 P1** | Madanmohan Upadhyay (named; living) | Factual: convener, offered a hall, inspected the town, deployed a team. Nothing evaluative. |
| 6 | **11.6 P1–P3** (LR-1; U7; RR-24) | The palace: the broken wall and gate, the private-property notice, the tehsildar's visit, the farman offered as support, the eviction order of 15 January 2021, the occupants' departure | The notice's names are never reproduced; no claimant or person named in the order is named; the naib tehsildar is not named. What the visit found inside the palace (a madrasa, per Tiwari) is not carried. The order's figures are in the note only. Suresh Mishra is named only as a walker. |
| 7 | **11.7 P1** (LR-3) | The theft of the Umā-Maheśvara; the police | The resident is not named; Tiwari's judgement of the local police is not adopted; only the FIR request, the report to police headquarters and the register entry. Suresh Mishra is named for asking for the FIR. |
| 8 | **11.8 P1** (LR-2; U7) | Illegal mining and blasting | The survey's own statements on illegal quarrying are given as the survey's (tier 7), naming no one. Tiwari's allegation is **one sentence**: "Some people believe that the ground-blasts of stone mining, legal and illegal, have put the temple itself in danger," attributed to him in its note, naming no one. Saxena's figure is recalled from 2.10 in the note only. Tiwari's network allegation (C12-JAGTA-EN-003) is not used (Ch 12). |

**U7 confirmed:** the cfg rule counts sentences in the body citing C11-JAGTA-EN-028, C12-JAGTA-EN-003 or C12-JAGTA-HI-011. The count is 1, and `ch_rules.py` reports 0 failures. The "living person named" rule (claimants, the naib tehsildar, the archaeology official, residents) also passes. **No living person is characterised beyond what the evidence attributes:** the three living people named (Vyas, Upadhyay, Suresh Mishra) appear only in acts the items name. Tiwari's judgements of officials, governments and residents are excluded or attributed in notes.

## 3. Rules, canon and tiers

- **U1, R1–R4:** nothing in this chapter touches the governors, the Records A–C or Karṇa. The R3 rule passes: "1059" appears only inside Kramrisch's caption, marked as a later scholar's dating.
- **D1:** `dynasty_spelling` is clean.
- **R5:** Tiwari gives no counts, figures or measures in the text. The exceptions are the publication references in 11.1 (in a note, as leads) and the order's own date in 11.6 (see Checks).
- **R7:** survey dates are proposals (11.5, 11.7).
- **R9:** staged sources are not used; Temple Economics is excluded.
- **Period terms:** none in the narrator's voice. "Masjid" appears only inside Beglar's quotation.
- **Tiers:**
  - the colonial reports as early scholarship, attributed, with the HELD and `ocr_verify` status noted;
  - the Gazetteer, INTACH and the Geo-Heritage survey as tier-7 surveys, phrased as their own;
  - the ASI's protection only as recorded (no notification in the sources, stated once);
  - Tiwari as testimony.
- **Agents:** Beglar, Cunningham, Garde, Bhandarkar, the Survey, Gwalior State, INTACH, Upadhyay, the tehsildar and the revenue court act only where an item names the act. No motive is invented.
- **Boundaries:** the buildings are Ch 7's (recalled: 7.1, 7.2, 7.13, 7.16); the regimes and the farman are Ch 10's (10.6 recalled); the residents, the lane and the visitors are Ch 12's (12.7 recalled); remedies and the translation proposal are the Afterword's.

## 4. A few quotations with IDs

- "surrounding the great temple stood at one time seven minor temples as at Pathari, but somewhat differently arranged" (C07-PANDE-005, Beglar via Pande)
- "the hall for reading the *beds*, or *vedas*" (C05-PANDE-008, Cunningham via Pande)
- "contrary to what we find in other well-preserved sections of the courtyard wall" (C11-SERPENT-001)
- "It has been in the ASI's records for quite a long time" (C11-JAGTA-EN-004)
- "completely ownerless, to be ruined" (C11-JAGTA-EN-009)
- "because this is a continuous stretch track off 1400 m" (C11-GEOHER-002)
- "there could again be a loss of human life" (C11-GEOHER-010)

## Checks

- **Unit checks:** `inhouse.py check` is clean for 11.1–11.5, 11.7 and 11.8.
  - 11.6 carries two reviewed flags on one sentence: "testimony as measurement" and "numeral under 100", both for the order's date, 15 January 2021.
  - The date is the order's own, printed by Tiwari as a document, not his recollection. It is kept because the unit is named for it. Accepted, as with earlier chapters' accepted flags.
- **Chapter rules:** `ch_rules.py` reports 0 failures.
- **Stitch:** `stitch.py 11 --check` reports equal.
- **`prose_checks`:**
  - no narrator period terms, passive runs or unsourced agent nouns;
  - colon reveals cut in the line edit, from 2.5 to 0.6 per 1,000 words.
- **Verification in-session.** Every sentence was checked against its items. Corrections made:
  - "first official description" → "first description in a survey report";
  - "near Bhilsa" → "the district's ancient ruined city" (the Gazetteer passage is Besnagar's);
  - Kramrisch's annual report was the ASI's, not Gwalior's;
  - "a princely department's work" → "an annual report of the 1920s";
  - "shakes" → "a threat to";
  - "the one modern repair" → "a modern repair";
  - "visitors cutting names" → "people writing names";
  - "in any language" → "No Hindi translation";
  - "spent a day" removed;
  - the seventh report's date (see §1).

## Editorial read (14 questions)

1. **Concrete openings:** a surveyor's platform, a brass sheath and a director, a state list, houses against the walls, a heritage walk reaching INTACH, a broken wall and a gate, a missing image, the quarries round the stone.
2. **One argument per unit:** yes. The whole chapter argues protection in pieces.
3. **Place as subject; sources in the notes:** yes. The reports are the subject in 11.1, as the brief asks. Named agents act; the attributions are in the notes.
4. **Calibrated verbs:** "most likely", "probably marks", "probable but unconfirmed", "may have been older", "some people believe".
5. **Conflicts side by side:** Beglar against Cunningham on the mosque; the find-place (CII against Tiwari's two pages); the board "the day before" against "for decades"; seven shrines against eight.
6. **Testimony marked:** yes; Vyas's year and Tiwari's figures are in the notes.
7. **Restraint:** no recommendations. The 11.3 interpretation ("protection brought maintenance to what was listed") is stated once.
8. **No invented actors or motives:** confirmed. The closing paragraph names the unnamed only as "those who quarry … whose herds graze".
9. **Tradition as memory:** the Aurangzeb legend is the report's carried legend; "Garde sahib" is memory.
10. **Boundaries:** kept (see §3).
11. **Repetition:** Ch 1's slab, cover, readers and legend, and Ch 7's monuments, are recalled in clauses with pointers.
12. **Opening from Ch 10:** opens on "the town the officials described as once important", then Beglar.
13. **Close into Ch 12:** the people at the record's edges; "its households, fields and quarries".
14. **Notes:** 27, about one per paragraph; the closing paragraph carries none.

## Deliverables

- `ch11/ch11_plan_v1.md`
- `ch11/ch11_draft_v1.md`: the working draft, with per-claim IDs
- `ch11/ch11_draft_v1_footnoted.md`: 27 footnotes; 11 bibliography entries, all still marked incomplete, as before
- `ch11/Chapter 11 - Udaypur in the Modern Period - Draft v1.docx`:
  - 8 unit headings and the bibliography, none empty;
  - 27 Word footnotes, none empty;
  - ends on the closing paragraph and then the bibliography
- `ch11/ch11_draft_v1_report.md`
- `run/ledger/ledger_ch11.json` → `editorial/book_ledger.*`

## Open for the user

- **Legal review:** LR-1, LR-2 and the new LR-3 (§2).
- **Hand-correction and ingest:** Beglar, Cunningham, Bühler and the Gwalior report (release the HELD notes).
- **Research Register:** RR-24 (the Land Revenue Code), RR-25 (the quarry site; Ch 2.10 asserts the Bhujariya tank while RR-25 is open), RR-32, RR-33.
- **Patil's volume:** its date.
- **Chapter 1 §1.11:** the seventh report's date.
