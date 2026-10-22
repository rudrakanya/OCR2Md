# Whole-book outline: what changed, and what was found

*16 October 2026.*
- **Deliverable:** `Udaypur_Complete_Book_Outline.md`, about 45,300 words, Chapter 1 to the Afterword. The v2 outline (`Chapter_4_to_Afterword_Master_Drafting_Outline_v2.md`) is unchanged as the record.
- **Sources and rebuild:** the sources are in `editorial/wholebook/`. The outline is rebuilt with `_tools/reconcile.py`, then `_tools/delivered_entries.py`, then `coverage_v2.py` for each unit (`UDAY_OUTLINE_DIR=wholebook`), then `_tools/assemble_wholebook.py`.
- **Method:** no API calls and no vector-store queries were made. The judgement work was verified in-session, not by an independent model.
- **The pause:** no chapter drafting or fixing was done during this task.

## 1. Corrections finished before the outline (step 1.1)

- **D1 (U10), IAST dynasty names:** Ch 1–4 were checked clean, including the footnoted outputs.
- **D2 (U11), "Bhoja's brother":** §1.2 was done earlier. **§4.3 P5 was still on the old canon and was finished now:**
  - the sentence now cites C04-CII-105 and C04-CII-086;
  - the Nagpur "kinsman" rendering moved to the note;
  - the free check is clean;
  - Ch 4's outputs were rebuilt (41 footnotes).
- **D4 (U13), the Nagpur Karṇa note in §1.2:** present in the text and in the footnoted output.
- **The in-flight D3 revision of Ch 4** was stopped at a section boundary:
  - the revised §4.1 is parked in `ch04/v2_work/4.1.md`;
  - the delivered five-section Ch 4 (v1) was restored as the text, and the builders point at the v1 config.

## 2. Reconciliation of Chapters 1–4: plan against text as written (step 1)

`editorial/wholebook/reconcile_report.md` holds the mechanical comparison. The entries for Ch 1–4 were derived from the text as written: its sections, the validator's word counts, each paragraph's cited items, and the opening and closing sentences. The divergences are below. They are **flagged, not decided**.

| Chapter | Divergence (content, not wording) | Handling |
|---|---|---|
| Ch 1 | §1.4: the plan's P1 and P2 were merged into one paragraph. The plan's "two fixed points, V.S. 1116 and V.S. 1137" became, in the text, 1116 as a reading and 1080 as the earliest known date. | The text follows U6. The entry follows the text. |
| Ch 1 | §1.2: the plan's "a kinsman of Bhoja" was superseded by U11, and U13 added the Nagpur note. §1.2–§1.3 cite borrowed Ch 8 and Ch 10 items for U1. | Decision-driven. The entry follows the text. |
| Ch 1 | Planned establishing items not cited: C01-JAGTA-EN-032 (the "kachahari" mosque; home §7.5), C01-GANGULY-015 (replaced under U1 by C08-GANGULY-016), and C01-KB-PARTEMPLES-005 (not found in any index; the plan cited an ID with no record). | Reasons recorded in the Appendix. |
| Ch 1 | ***mahāsādhanika* is used in §1.2 without a gloss.** The style sheet glosses at first use, and §10.1 had planned the book's first gloss. | **RR-42 (b):** a light-touch fix, for decision D6. |
| Ch 2 | §2.5 is 153 words (31% of target). Its planned closing paragraph, recalling the GEOHER items, became a two-sentence close with no IDs. The chapter is 2,608 words, below the floor. | RR-35, decision D5 |
| Ch 2 | **§2.1 P1 has a duplicated fragment:** "…far side of the Betwa. 1143–1155) fought Candellas advancing on the far side of the Betwa and drove them from the principality." It has been there since delivery, in the verified and footnoted versions. | **RR-36, RR-42 (a):** a light-touch fix, not made under the pause |
| Ch 2 | Planned items not cited: C02-GEOHER-003 (§2.3; cited in §2.1 instead), C02-GEOHER-028 (§2.4; cited in §2.1), and C02-GEOHER-001/-027 (§2.5; cited in §2.1 and §2.2). | none needed; the items are used elsewhere in the chapter |
| Ch 3 | §3.1 is at 64% of target, and the chapter is 2,557 words, below the floor. The plan's paragraphs were split into more, shorter ones (2→4, 2→4, 3→5, 2→4, 4→5). | RR-35, decision D5 |
| Ch 3 | Planned items not cited: C03-GAZ-050 (Udayagiri epigraphs; the Gupta presence is carried by other items) and C03-CII-008 (Bhilsa's name; carried by other items). | Reasons recorded |
| Ch 4 | The divergences already recorded in `ch04_report.md`: §4.2 P5 folded into P4; §4.4 gained "What rests on the choice"; §4.5 gained the Bhringrajpur paragraph. The D2 change in §4.3 P5 is new. | The entry follows the text |
| Ch 4 | The approved six-section structure (U12) is not in the text. The entry describes the five sections as written. The plan is held in `ch04/ch04_plan_v2.md`. | RR-40, decision D7 |

## 3. Continuity, chapter pair by chapter pair (step 3.1)

Each join was checked from the written closing and opening for Ch 1–4, and from the entries' planned openings and closings for Ch 5 onwards.

| Join | Result | Fix |
|---|---|---|
| 1 → 2 | Agrees: stone and water, then the river first | none |
| 2 → 3 | Agrees: the ground's silence, then the oldest traces | none |
| 3 → 4 | Agrees: who held the hill, then a kingdom's edge, with the gap kept open | none |
| 4 → 5 | Agrees: the dated temple, then the building as built | none |
| 5 → 6 | Agrees: the unread name, then its reading at the east door | none |
| 6 → 7 | Agrees: the inscribed, then the uninscribed wall | none |
| 7 → 8 | Agrees: water as merit, then land as a gift | none |
| 8 → 9 | Agrees: a family's service, then the community | none |
| 9 → 10 | Agrees: memory, then the record | none |
| 10 → 11 | Agrees. The Gazetteer phrase that closes Ch 10 is the one §1.1 quotes. | Ch 10 recalls it as an echo; recorded in Part III, H |
| 11 → 12 | Agrees: the people at the record's edges, then one household | none |
| 12 → AW | Agrees: plans, then the earliest dated plan | none |

**Continuity fixes made in the outline** (from the ledger cross-check, step 3.3, and the reference check, step 3.4):
1. **Ch 9 §9.5.** Berni Mata's string-dance and *samādhi* versions and Vyas's *yakṣa* reading are already told in §1.1. §9.5 now recalls them and adds only what §1.1 lacks.
2. **Ch 11 §11.2.** "Garde Sahib" was planned as "introduced here", but §1.3 has it already. It is now recalled as a lead (RR-33).
3. **Ch 10 §10.1.** The *mahāsādhanika* gloss is marked as late against §1.2 (RR-42).
4. **Ch 5 and Ch 7, "Builds on".** Both are completed with what Ch 1–3 actually told:
   - Ch 5: §1.1 P5, the east-facing temple in its court;
   - Ch 7: the cave in §3.3 P5, the hill inscription in §3.5 P4, and the flour-grinder's temple in §1.4 P3.

   The "Mothers panel" recall was dropped from Ch 7: that panel stands between Badoh and Pathari, not on Udaypur's hill (R6).
5. **Leftover v1 section numbers in role notes**, remapped to sections that exist:
   - Ch 8, the Lūṇapasāka date and the Bhṛṅgāri identification: §6.6;
   - Ch 9, the V.S. 1696 pilgrims: §6.7;
   - Ch 9, the fairs: §8.7.
6. **Ch 4 numbering.** References to the six-section plan (§4.4–§4.6) in Part I and Part III were replaced with the five sections as written (§4.3 P5, §4.4, §4.5). The reference check now finds no reference to a missing section.
7. **Part I, I.3–I.4, extended to Chs 1–3.**
   - New conflict homes: the distances (R10), the stream names, founded or taken over, the snake legend, the end of Besnagar, the climate trend.
   - New cluster homes: the village today, the polity, the triad, the governance terms, the later sequence, the Bhujariya Talab, quarries, Bhojpur, Vidisha and the roads, the Badoh–Pathari frontier.
   - New rules: R10 (the settled ranges) and R11 (present-day science stays present).
8. **Dynasty spelling.** One non-IAST form in the Ch 10 entry was corrected. The Appendix's sub-topic labels are normalised (U10).

**Ledger, book-wide (step 3.3).** Every person, term and place the ledger records as first introduced in Ch 1–4 was checked against the later entries. The only conflicts are fixes 2 and 3 above. Nothing a later entry relies on is unintroduced: the actors and terms that later entries introduce are listed in Part III, D–E.

## 4. Evidence coverage, all 13 units (step 4)

Every direct item has one status. None is unreasoned.

| Unit | Direct | Assigned | Cross-ref | Excluded |
|---|---|---|---|---|
| Ch 1 | 185 | 78 | 5 | 102 |
| Ch 2 | 146 | 68 | 11 | 67 |
| Ch 3 | 133 | 47 | 1 | 85 |
| Ch 4 | 221 | 90 | 18 | 113 |
| Ch 5 | 284 | 211 | 24 | 49 |
| Ch 6 | 223 | 186 | 5 | 32 |
| Ch 7 | 239 | 147 | 15 | 77 |
| Ch 8 | 44 | 35 | 3 | 6 |
| Ch 9 | 32 | 29 | 2 | 1 |
| Ch 10 | 61 | 37 | 1 | 23 |
| Ch 11 | 92 | 74 | 0 | 18 |
| Ch 12 | 71 | 56 | 4 | 11 |
| Afterword | 58 | 54 | 1 | 3 |
| **Total** | **1,789** | **1,112** | **90** | **587** |

**Chapters 1–3 backfill.** 251 direct items had no recorded reason (Ch 1: 102; Ch 2: 65; Ch 3: 84; three more already had automatic reasons). Each was reread in full and given one (`wholebook/excl_ch01–03.tsv`). The main reasons:
- **Ch 1:** testimony restating T1/T5 facts, distances or counts from testimony (R5), superlatives (R7), duplicates, and items another chapter tells.
- **Ch 2:** district-level or other-place geography and climate tables, and the teak-hill item, which is a different place.
- **Ch 3:** Vidisha and regional history without Udaypur bearing, under the chapter's own centre-of-gravity rule.

The four Ch 4 items found usable in the exclusion re-audit are recorded as held for the D3 revision (RR-40).

**Checks:**
- no item is primary (E) in two units;
- every section reference resolves;
- the target sums are correct;
- the R8 warnings for §8.5 and §10.5 stand, as accepted earlier.

For written chapters, an item that belongs to another unit, or that a later chapter tells in full, is marked C rather than E (R6).

## 5. Anything that needed the vector database

**Nothing.** Every gap was answered from the evidence index, the chapter packs, the evidence log, or free text search of the corpus Markdown. The D2 basis, for example, came from the CII Markdown, pp. 151–152, 157 and 324. No semantic search was needed, so no capped spend is requested. The open questions that free search could not settle stay in the Research Register as tasks (RR-1 to RR-42).

## 6. Decisions now needed (Part I, I.8)

- **D5:** Chs 2 and 3 below the floor: accept, restructure, or assign evidence?
- **D6:** the light-touch prose fixes (RR-42: the §2.1 duplicate; the *mahāsādhanika* gloss in §1.2).
- **D7:** resume the paused Ch 4 revision (U12), or hold it?
