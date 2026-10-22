# Chapter 1, draft v6: report (17 October 2026)

**Udaypur: Historical Memory and the Making of a Place.** Drafted in-session from `ch01_plan_v6.md` (14 units, one per unit of `editorial/Udaypur_Book_Contents.md`). No API calls. Evidence comes from `evidence_pack_v6.json`: the ch01 index, the free-corpus KB items and borrowed C04/C07/C08/C10 items.

## Length now follows evidence

Word targets were removed on 17 October at the user's instruction:
- `cfg_ch01v6.py` now has `NO_LENGTH = True` and no WMIN/WMAX.
- `ch01_plan_v6.md` no longer carries the "· N w" targets.
- `validate.py` skips the section and chapter length checks when NO_LENGTH is set.
- `inhouse.py` reports no share and prints no target.

Every non-length check still runs. Each unit was then redrafted from its full evidence list: the plan's items, the unit's ch01 items and the unused KB items, with the one-home rule applied.

| Unit | Before (body words / items) | Now (body words / items) | quotations | notes |
|---|---|---|---|---|
| 1.1 The village today | 270 / 18 | 353 / 26 | 6 | 6 |
| 1.2 The living temple | 182 / 10 | 183 / 10 | 2 | 3 |
| 1.3 The walled town and its memories | 364 / 16 | 443 / 18 | 3 | 2 |
| 1.4 The names of the place | 230 / 12 | 284 / 20 | 8 | 5 |
| 1.5 Udayāditya and the Paramāra kingdom | 333 / 18 | 348 / 29 | 3 | 4 |
| 1.6 The foundation of town, temple and tank | 185 / 9 | 309 / 18 | 5 | 2 |
| 1.7 The date of the foundation | 292 / 16 | 563 / 34 | 11 | 6 |
| 1.8 Udaypur in the eastern province | 250 / 16 | 458 / 28 | 2 | 5 |
| 1.9 Later rulers and patrons | 283 / 20 | 447 / 29 | 1 | 5 |
| 1.10 The Udaypur praśasti | 274 / 14 | 416 / 26 | 3 | 4 |
| 1.11 The inscriptions and their first readers | 193 / 9 | 347 / 19 | 4 | 3 |
| 1.12 Stories of the temple's survival | 213 / 13 | 363 / 18 | 4 | 4 |
| 1.13 Udaypur among Paramāra monuments | 192 / 10 | 426 / 33 | 9 | 6 |
| 1.14 An earlier settlement? | 300 / 12 | 343 / 16 | 2 | 2 |
| **Total** | **3,561** | **5,283** body words (≈ 7,200 with notes) | **63** | **57** |

Across the chapter, 303 distinct evidence items are cited.

- **Short on evidence:**
  - **1.2** has nine assigned items, and all of them are used. The rest of the worship evidence (rituals, festivals, priests) belongs to Chapter 8, so 1.2 stays short and is not padded.
  - **1.5's body** grew little because, under D2, the kinship evidence goes into one dissent note. That note now carries eleven items.
- **Unused items, each for a stated reason:**
  - population history (GAZ-009) belongs to Ch 12, soils to Ch 2, the monument list to Ch 7, and the Lavanya Sundari dance to Ch 9;
  - INTACH-002/-003/-004, BHOJA-TIMES-001, GANGULY-003 and GANGULY-017 duplicate items already cited;
  - BHOJA-TIMES-010 is garbled;
  - GEOHER-007, KB-PARTEMPLES-005 and RAJABHOJ-EN-004 have an unclear referent;
  - GEOHER-016/-023, PANDE-009, JAGTA-EN-038 and JAGTA-EN-028 repeat a verdict or carry no fact;
  - JAGTA-EN-007 is a counterfactual;
  - KB-JAGTA-EN-009 belongs to Ch 12, KB-PANDE-003 to Ch 10, and KB-GANGULY-018 is off-topic.

## What the redraft added

- **1.7, the date of the foundation** (now the longest unit). It covers:
  - the 1080 record: two short inscriptions, one dated, naming no place (KB-GANGULY-005, KB-CII-005);
  - the four separate routes to 1059, kept apart under R1/R3: the 1513 fragment, "very perfunctorily executed" and abounding "in gross mistakes" (GANGULY-020); the V.S. 1116 / Śaka 981 inscription (JAGTA-EN-048, KB-GANGULY-007); Patil, the Gazetteer and Sharma; and the Geo-Heritage survey's error (GEOHER-006 against CII-008);
  - how the 1059–1080 span hardened in the surveys;
  - the three readings of 1080;
  - the reign, c. 1070–1093;
  - the prince's-seat view, and local memory of crown princes.
- **1.8:**
  - the frontier and the quarries;
  - the Nēmaka capital "subordinate to Udayāditya" (CII-002) and Śūdraka (KB-CII-006);
  - Lūṇapasāka's grant as a 1171–73 range;
  - Bhiraṅgāvalī, about 6 km NE (CII-010);
  - Devapāla residing at Udayapura (GANGULY-016), his *mahākumāra* title (note), and Jayavarman.
- **1.13:** Hardy's "deluxe model" with no surviving precedents, the verdicts (attributed), comparisons, and the building country.
- **Other units:**
  - 1.1: the Bareth range, 6–6.5 km;
  - 1.4: the spellings, and the "Astpur" pun;
  - 1.6: the Udayasamudra problem;
  - 1.9: the Candellas, the *mahākumāra*s, the Malwa sultans and the Chanderi *sarkar*;
  - 1.10: the genealogy's claims;
  - 1.11: the inscription counts, the Hoysaḷa "Udhapuram", and the 1888 edition;
  - 1.12: the resistance reading, attributed;
  - 1.14: the stepwell's 7th–8th-century column elements and Bhringraj.

## Sample quotations

- “supplies the earliest known date for the king Udayāditya” [C01-CII-007]
- “very perfunctorily executed” … “abounds in gross mistakes” [C01-GANGULY-020]
- “The Udayeshvara, which has no surviving precedents, is already the deluxe model” [C01-HARDY-003]
- “subordinate to Udayāditya” [C01-CII-002]
- “a glittering diamond had been placed on a heap of garbage, and no one had any care for it” [C01-KB-JAGTA-EN-008]

## Verification and checks

- **Verification.** Every unit was verified in-session, claim by claim, against the full quotations of its cited items. This is not an independent model's verification.
- **Checks.** `inhouse.py check` is clean for all 14 units: verbatim quotations, valid IDs, supported names and numbers, no source-led sentences, no invented agents, IAST dynasty names, no testimony-as-measurement, no passive runs, and no ledger re-introductions. The only ledger flags are keyword-match "figure" review items, which were checked and are false positives.
- **AI-shape** (per 1,000 words): "not X but Y" 0.2, triplets 0.7, colon reveals 0.6 (cut from 2.2 in the line edit), and 0 for each of the rest.

## Editorial read against the 14 questions

- **Pass on all 14:** 1.1, 1.2, 1.4, 1.6, 1.10, 1.11, 1.12 and 1.14.
- **Marginal, counted as pass:**
  - 1.3, Q9: the undated palace sentence;
  - 1.5, Q9: the list of borders;
  - 1.7, Q11: the three parallel "in one / another / a third" sentences, which are deliberate;
  - 1.8, Q9: the paragraph glossing the terms of government;
  - 1.9, Q9: the Malwa sultans sentence, which leans towards Ch 10;
  - 1.13, Q11: the run of attributed verdicts.

## Open issues

1. **The V.S. 1116 witnesses.** They still need checking against Bühler (EI I) and Cunningham, as R3 requires.
2. **The brass cover.** V.S. 1841 is given in the accounts as A.D. 1775; this is to be checked in Ch 10.
3. **The bibliography.** 15 of 17 entries lack place and/or publisher (`ch01_draft_v6_footnoted.bibliography_todo.json`).

## Deliverables

- `drafting/ch01/ch01_draft_v6.md`: the working draft, with IDs.
- `drafting/ch01/ch01_draft_v6_footnoted.md`: the Chicago version, with 85 notes.
- `drafting/ch01/Chapter 1 - Udaypur - Draft v6.docx`
- The sections are in `drafting/run/ch1/1.1.md`–`1.14.md`; the pre-redraft sections are backed up in the session scratchpad.
- The ledger is `drafting/run/ledger/ledger_ch1.json`, merged into `editorial/book_ledger.md`.
