# Chapter 4, draft v3: drafted fresh from the contents file (19 October 2026)

No API calls were made. The work was verified in-session, not by an independent model.

## State before this pass

- **Draft v1 was archived, not live.** It sits in `_archive/pre_contents_rebuild/ch04/` and had nothing in `run/ch4/`.
  - It had five sections, about 4,030 body words, 135 items and 28 notes.
  - It was complete, not truncated; it ends on its closing sentence about the V.S. 1137 record.
- **Why a fresh draft:** the contents file now gives Chapter 4 twenty units, so v1's structure no longer fits. Chapter 4 was drafted from the evidence up rather than redrafted from v1.
- **The unfinished six-section revision** (D3, `ch04/v2_work/4.1.md`) was superseded by the contents file and not used.

## Setup

- **Plan:** `ch04/ch04_plan_v3.md`, twenty units with their paragraph evidence.
- **Config:** `ch04/cfg_ch04v3.py`.
  - `NO_LENGTH`; `BUDGET 0`.
  - Canon rules in `extra_rules`: R2 (every Karṇa named by dynasty or marked unspecified), R4 (1170s terms only in 4.19), D2 ("nephew" never used of Udayāditya). Run them with the new free tool `_tools/ch_rules.py`.
- **Pack:** `ch04/evidence_pack_v3.json`.
  - It is the v2 pack plus three items borrowed for U1: C01-KB-GANGULY-016 and C08-GANGULY-015/016.
  - 118 Hindi-source items had their English glosses restored from the evidence index; the gloss had been missing from the pack copy.
- **Sections:** `run/ch4/4.1.md` to `4.20.md`. `_tools/stitch.py` and `_pipe/build_outputs.py` now point to the v3 config.

## Units, length and evidence

| Unit | Body words | Items |
|---|---|---|
| 4.1 The Origin of the Paramāras | 859 | 35 |
| 4.2 From Feudatories to Kings of Malwa | 999 | 49 |
| 4.3 Muñja and Sindhurāja | 953 | 34 |
| 4.4 The Branch Lines of the Dynasty | 647 | 21 |
| 4.5 Bhoja's Reign and Kingdom | 857 | 51 |
| 4.6 Bhoja's Wars | 699 | 25 |
| 4.7 Bhoja as Builder | 730 | 34 |
| 4.8 Bhoja's Learning, Faith and Court | 696 | 32 |
| 4.9 Bhoja in Udaypur's Praśasti and in Memory | 718 | 30 |
| 4.10 Bhoja's Last Years and the Reign of Jayasiṃha | 540 | 22 |
| 4.11 The Three-Sided War and the Recovery of Malwa | 709 | 23 |
| 4.12 Udayāditya's Descent | 487 | 22 |
| 4.13 Dating the Beginning: 1059 and 1080 | 642 | 28 |
| 4.14 Udayāditya's Reign and Realm | 591 | 22 |
| 4.15 The Royal Family and the Succession | 655 | 30 |
| 4.16 Royal Temple Building under the Paramāras | 507 | 20 |
| 4.17 Town Planning in Bhoja's Treatises | 761 | 28 |
| 4.18 The Name Udayapura and the Founding Claims | 489 | 17 |
| 4.19 Udayapura as a Seat of Government | 531 | 18 |
| 4.20 The Frontier Town in Local Testimony | 623 | 23 |
| **Total** | **13,693** | **506 distinct** |

- **Notes:** 69 reader-facing notes, one per paragraph.

**Evidence used:**
- 483 of the 682 items in the Chapter 4 evidence index are cited.
- **Exclusions reopened.** Thirteen items were excluded only because the retired five-section v1 had no place for them, and are now used: the agnikula verse, Muñja's praise, the Shergadh successor grant, the realm near Udaipur, Lōlārka, the Rās Mālā and Belava marriages, Śyāmaladēvī, the realm's extent, the strategic-border testimony and the "mini-capital".

**Not used (199 items):**
- **98 keep their recorded exclusions.** These are duplicates, garbled OCR, Tiwari's imagined scenes and conjectures, Verma's renderings superseded by CII's edition, distances from testimony, and items homed elsewhere: coins (Ch 8), the Vijay Mandir (Ch 10) and the Bhūmija detail (Ch 5).
- **About 85 cover the later Paramāras,** from Naravarman's wars through Yaśovarman, the Mahākumāras, Vindhyavarman, Devapāla and Jayavarman II. The brief gives 1093–1305 to Chapter 10.
- **The rest:**
  - the three *Temple Economics* items, excluded by canon;
  - two Hindi duplicates of verses already quoted;
  - an OCR-garbled date (BHOJA-TIMES-042);
  - an inscription whose site the item does not give (PARTEMPLES-008);
  - Tiwari's obscure note on an unfinished later monument (JAGTA-EN-065/066, HI-064);
  - Tiwari's restated reign dates, removed as testimony used for a date (JAGTA-HI-048);
  - the Belur paintings item, which calls Udayāditya Bhoja's nephew (D2).

**Thin units, flagged rather than padded:**
- 4.12 and 4.18 are short because their evidence is a few decisive records.
- 4.10 has little record of Jayasiṃha beyond one grant and the fact that the praśastis leave him out.

## Canon honoured, with examples

- **R2, Karṇa named by dynasty:**
  - "the Kalacuri Karṇa, of about 1041 to 1072, and the Caulukya Bhīma I" (4.10);
  - the Nagpur verse's Karṇa is "without saying which", with D4 in a note (4.11);
  - Arisiṃha's and Bhatia's Karṇas are flagged as unspecified (4.11, note).
- **R1 and R3, the records kept separate:** 4.13 sets out "three references to V.S. 1116, and they are three different things":
  - the 1513 fragment, "very perfunctorily executed";
  - the V.S. 1562 pedigree, "distinctly stated to have been ruling in Sam 1116";
  - the twenty-two-line temple inscription, "teeming with a plethora of errors".

  The pedigree and the long inscription share Śaka 981, but "No record says that they are one inscription, and they stay two."
- **R4, dated geography:** Bhāillasvāmi-mahādvādaśaka and Bhṛṅgārikā appear only in 4.19, as "records of the 1160s and 1170s". The Gazetteer's attribution of the 1173 record to Udayāditya, "who had died eighty years before", is corrected. The governors served the Caulukya kings (U1).
- **U6, the foundation date:** "So 1080 is the earliest firm date, and 1059 is a reading, carried by a late fragment, a sixteenth-century pedigree and a long, faulty inscription, none of them checked against the first editions" (4.13).
  - Whose reading 1059 is: the three records above, then Patil, the Gazetteer, Hardy and Kramrisch.
  - Ganguly's "paternal territory" hypothesis is shown to need both 1059 and the rejected pedigree.
  - The dated reign runs to 1093 (4.14, 4.15).
- **D2, the kinship:** "Udayāditya was Bhoja's brother", resting on the Dōngargāon and Jainād inscriptions (4.12). The dissent is in one note: Kielhorn and *bandhu*, Ray, Verma on *padānudhyāta*, and the silence of Bhoja's own records.
- **Boundaries:**
  - the temple's architecture is handed to Chapter 5;
  - the praśasti as a text to Chapter 6;
  - Udayasamudra and the walls to Chapter 7;
  - Naravarman and the province to Chapter 10.
- **Spelling:** the dynasty spelling check passes on the stitched and footnoted files.

## Some direct quotations used

- "purely legendary, a later creation" (C04-CII-020, 4.1);
- "his lotus-feet were coloured by the jewels on the heads of the Karnnāṭas, Lāṭas, Kéralas and Chōlas…" (C04-CII-129, 4.3);
- "this conquest probably continued to be celebrated at most of the places in the Paramāra kingdom for the whole year" (C04-CII-056, 4.6);
- "his glorious success against the lord of the Chēdīsa (Dāhalādhiśa) whom he routed completely" (C04-CII-112, 4.11);
- "Bhōja's brother Udayāditya, who uplifted the kingdom of Mālava which had sunk under the attacks of three enemies" (C04-CII-083, 4.12);
- "evidently after the name of its constructor" (C04-CII-119, 4.13 and 4.20);
- "The only geographical name mentioned in the record is Udayapura, which is said to be the capital town of the Nēmaka dynasty…" (C04-CII-113, 4.19).

## The hand-off to Chapter 5 (4.20)

- The Udayeśvara is the one royal work at Udaypur tied to the reign by a record of the time. Its flag was raised in V.S. 1137, A.D. 1080, and it is named "after the name of its constructor".
- **What the 1080 record does not establish:** when the temple was begun (1059 is a reading), that the town was founded in the same year, or that the Nēmaka temple is this one.

## Checks

- All twenty units are clean under `inhouse.py check`, including the ledger.
- The canon rules give 0 failures.
- **AI-shape** per 1,000 words: "not X but Y" 0.1, triplets 1.0, colon reveals 0, symmetrical contrast 0.1.
- **Verification in-session:** every quotation was matched against its item, and claims were read against their items. Corrections made:
  - an invented date for Ājaḍa's commentary was removed;
  - "a native chief" became "a local chief";
  - the 1086 record no longer "dates itself" from 1080 (the link is the editor's);
  - Jagaddēva's birth was moved to the Dōngargāon inscription;
  - a Tiwari-only reign date was dropped.
- **Ledger:** the Chapter 1 full names for Karṇa and Bhīma were changed so that the full-name check no longer conflicts with R2.

## Editorial read (14 questions)

All twenty units pass. Marginal points:
- 4.4 and 4.16: Central-India context, kept compact, each closing on Udaypur.
- 4.9 P2: a long run of memory material, with each item attributed.
- 4.20 P2: Tiwari's testimony is extensive, with the notes marking it as testimony.

## Deliverables

- `ch04/ch04_draft_v3.md`: the working draft, with IDs.
- `ch04/ch04_draft_v3_footnoted.md`: 69 notes and 19 bibliography entries, 17 still incomplete, as in earlier chapters.
- `ch04/Chapter 4 - The Paramāras and the Foundation of Udaypur - Draft v3.docx`: all twenty units present, none empty or truncated.
- The ledger: `run/ledger/ledger_ch4.json`, merged into `editorial/book_ledger.md`.
