# Chapter 7, draft v1: The Wider Built Heritage of Udaypur (21 October 2026)

Drafted in-session from the contents file (`editorial/Udaypur_Book_Contents.md`, Chapter 7: 25 units). No API calls, Chroma queries or paid ledger runs were used.

## 0. State before work, and the staged editions

- **Before work:** Chapter 7 had no `ch07/` directory, plan, cfg, pack or draft. The only material was the evidence maps (`ch07.jsonl`, 357 items).
- **Staged Beglar and Cunningham editions:** still uncorrected and not ingested. Beglar p. 87 carries one correction; his plate of the fort is an image only. These editions were not used for any reading.
- **Held passages:**
  - **7.2 (RR-15).** The Geo-Heritage survey quotes a colonial observer without naming him. The words match Beglar's report in the staged copy. The passage is quoted from the survey's text and its note is marked HELD, pending your corrected Beglar.
  - **7.19 (RR-15).** The same holds for the dargah by the north gate ("respected vaguely by the people").
  - No other passage depends on the staged editions.
- **Open conflicts kept open:**
  - RR-13: which mosque is the inventory's 18th-century Moti Masjid (7.17).
  - RR-14: where the V.S. 1625 pillar inscription stands (7.13).

## Plan and files

| Item | Path |
|---|---|
| Plan | `ch07/ch07_plan_v1.md`: 25 units, each with its paragraph items, the historical question and the arc |
| cfg | `ch07/cfg_ch07v1.py`: NO_LENGTH; Gazetteer share capped at 0.40; extra rules for SAMAR, R2, R3, R4, "Mohammedan" and anonymous labour |
| Pack | `ch07/evidence_pack_v1.json`: 378 items, i.e. `ch07.jsonl` plus 21 items borrowed from Ch 1, 2, 4, 5, 6, 10 and 11 |
| Sections | `run/ch7/7.1–7.25.md` |
| Ledger | `run/ledger/ledger_ch7.json`, merged into `editorial/book_ledger.*`; the header now reads "Chapter 7 (v1)" |

## Units

| Unit | Body words | Items | Direct |
|---|---|---|---|
| 7.1 The monuments counted | 320 | 13 | 13 |
| 7.2 The hill wall *(HELD note, RR-15)* | 532 | 19 | 18 |
| 7.3 Inside the wall | 299 | 11 | 9 |
| 7.4 Dating the hill wall | 271 | 9 | 5 |
| 7.5 Forts and towns in Bhoja's treatise | 474 | 15 | 2 |
| 7.6 The Jain cave and the rock panels | 350 | 14 | 5 |
| 7.7 The unfinished colossus and the cut hill | 264 | 12 | 7 |
| 7.8 The walled town and its gates | 253 | 7 | 6 |
| 7.9 The palace and the governor's mansion | 377 | 11 | 10 |
| 7.10 Lanes, gateways and the old bazaar | 251 | 6 | 6 |
| 7.11 Houses built of older buildings | 261 | 9 | 8 |
| 7.12 The Bijamandal | 243 | 10 | 7 |
| 7.13 The Barakhambi and the Pisanhari temple | 227 | 9 | 9 |
| 7.14 Later Hindu shrines | 244 | 10 | 10 |
| 7.15 Jain images, chhatris and memorial stones | 252 | 7 | 6 |
| 7.16 The mosque in the temple court, 1336–38 | 324 | 9 | 8 |
| 7.17 The bilingual mosque of 1488 | 211 | 6 | 6 |
| 7.18 The Shahi Masjid, 1632 | 237 | 6 | 5 |
| 7.19 The undated Muslim monuments *(RR-15 note)* | 280 | 9 | 9 |
| 7.20 Water on the hill | 274 | 12 | 11 |
| 7.21 Stepwells and wells in the town | 279 | 10 | 10 |
| 7.22 The Udaysagar and the Udayasamudra | 254 | 11 | 9 |
| 7.23 The Bhujariya Talab and other tanks | 219 | 5 | 5 |
| 7.24 Vikrama's tank at Amērā | 281 | 9 | 2 |
| 7.25 Water structures in the treatise and the region | 281 | 9 | 0 |
| **Total** | **7,258** | **220 distinct** | **160 of 239** |

- **Units with no word target.** 7.17, 7.23 and 7.13 are the shortest because their evidence is thin.
  - 7.23 has five items, and the Bhujariya's date rests on a single survey's reading of its masonry.
  - None was padded.
- **Units built mainly on contextual items.** 7.5 and 7.25 (the treatise) and 7.24 (Amērā) draw mostly on items in the region, the treatise and CII. That is by design: their direct items for Udaypur are few.

## Direct items set aside (79), with reasons

| Group | Count | Reason |
|---|---|---|
| Tiwari's Hindi (JAGTA-HI-001…067) | 55 | Hindi originals of the English items used. They are set aside to avoid duplication, apart from JAGTA-HI-012, -016, -034, -044, -052, -056 and -065, which add facts the English lacks. |
| Tiwari's scenes and rhetoric (JAGTA-EN-004, -007, -016, -020, -023, -025, -028, -032, -037; HI-005, -008, -061) | 12 | These are scenes he imagines (the town's splendour, massacres, the "durbar" hall), superlatives, or editorial asides with no fact about a structure. JAGTA-EN-015 (the plywood minarets) belongs to Ch 11's present. |
| Geo-Heritage repeats and claims (GEOHER-006, -017, -020, -021, -039, -046, -056) | 7 | Each one either restates the wall length and masonry already cited, is a reserve-planning proposal (-020), or is a superlative ("excellent example … 1000 years") with no support. |
| Index and caption lines (KRAM-1-001, KRAM-2-001, PANDE-001, -003) | 4 | Index entries and plate captions. |
| PANDE-005 | 1 | The seven minor temples are Ch 5's (the temple court). |
| MADHYABHARAT-020 | 1 | A district overview, used in Ch 1. |
| INTACH-024 | 1 | A table row whose names and dates repeat GEOHER-062. |

## History, not catalogue

- **Questions, not types.** The units are grouped by what each body of evidence can answer:
  - who held the hill, and when (7.2–7.7);
  - what the walled town was (7.8–7.12);
  - who else worshipped here, and who built after the Paramāras (7.13–7.15);
  - how three dated mosques mark three changes of master, Delhi in 1336–38, Mandu in 1488 and the Mughals in 1632 (7.16–7.18), and what undated Muslim graves say about a resident population (7.19);
  - how the town was supplied with water, and who paid for it (7.20–7.25).
- **Survey dates as proposals.** Blanket "11th Century" listings are read as proposals (7.1). Where the fabric gives a bracket, the bracket is used instead:
  - temple pieces reused in the stepwell bund (7.20);
  - pointed arches in the palace (7.9);
  - INTACH's dating by iconography and by likeness to the palace (7.14).
- **Minor items set aside with reasons:**
  - the inventory's long lists of temples (7.14) and stepwells (7.21) are summarised, not enumerated;
  - the "missile temple" is kept for the one fact it carries, a sixteenth-century date.
- **Kept apart:**
  - the Raja Mahal and the Mughal governor's mansion (7.9);
  - Udaypur's Bijamandal and Vidisha's (7.12);
  - the Udaysagar and the inscription's Udayasamudra (7.22).

## No invented labour

- No anonymous builders, masons or quarrymen are introduced. The `extra_rules` anonymous-labour check and the agent-noun check both passed.
- Each agent noun comes from a cited item:
  - "workmen", in the Pisanhārī tradition (MADHYABHARAT-006);
  - "masons' marks" (PANDE-007);
  - Tiwari's "Ellora's craftsmen", reported as his speculation (7.7).
- Named people act where the record names them:
  - Vikrama and the engraver's family at Amērā;
  - Sher Khan's agent;
  - Auliya Ibn Abdul Samad (from the farman);
  - Jannaka;
  - the donors of Bhundipada.

## Canon honoured

- **U1, R1–R4 and D1:** `ch_rules.py` reports 0 failures.
  - R3: "1059" appears only as the survey's reading (7.22).
  - R2: no unqualified Karṇa.
  - R4: no 1170s terms.
- **Period term:** "Mohammedan" and "Muhammadan" appear in no narrator sentence. The quotations that contain them (PANDE-006 and -007, GEOHER-031) are paraphrased or quoted only around the term.
- **Tiers:**
  - CII for the Amērā record;
  - the Gazetteer and INTACH as tier-7 survey; the Gazetteer is at most 40% of any unit;
  - Tiwari as testimony, never as a measurement. The 27 feet and 980 metres are kept as his reports or left out.
- **Boundaries:**
  - the temple: Ch 5;
  - inscriptions as texts: Ch 6, pointed to in 7.13, 7.16, 7.17, 7.18 and 7.24;
  - the farman and Mughal administration: Ch 10;
  - the palace ownership dispute: Ch 11;
  - landscape water: Ch 2.
  - Lichen dating sits in 7.4.
- **Excluded:** SAMAR items are never quoted, and Temple Economics is excluded.

## Quotations used, with IDs

- 7.1: "the traces of an old fortification wall of great uncemented stone blocks" (C07-GAZ-001); "full of Paramāra-period architecture" (C07-MADHYABHARAT-021); inventory labels "10th Century", "1956 Century", "6th Century", "11th Century", "Not Known" (C07-GEOHER-059/060/061/063/064, C07-INTACH-026)
- 7.2: "The entire place is deserted, … not even a name that I could hear of." (C07-GEOHER-002, HELD RR-15); "the exact appearance of a fortified castle"; "a wall built of huge uncemented stones, 18 feet thick at the present crest"; "in the form of a circular sector" (C07-GEOHER-002); "more research needs to be done …" (C07-GEOHER-022); "has not been breached even at a single place" (C07-GEOHER-005)
- 7.3: "a very significant Hindu pilgrims' site" (C07-GEOHER-054)
- 7.4: "existed prior to Udayaditya"; "a mystery" (C07-GEOHER-003); "hundreds of years of time"; "can also help in identifying the age of these locations" (C02-GEOHER-024)
- 7.6: "unlike the standing images found at other locations in the country" (C05-GEOHER-009); "or maybe even earlier" (C05-GEOHER-011)
- 7.7: "a huge but unfinished image of Shiva carved in boulder" (C07-MADHYABHARAT-005); "The common belief"; "one of the tallest temples of Shiva" (C05-GEOHER-004); "at the very initial stage" (C07-JAGTA-EN-006)
- 7.8: "pierced with a number of gates" (C07-MADHYABHARAT-003); "As the Delhi Darwaza in Chanderi, so the Chanderi Darwaza in Udaipur." (C07-JAGTA-EN-002)
- 7.9: "is all shrouded in layers of history" (C07-GEOHER-052); "encroachments of a later period" (C07-JAGTA-EN-033); "probably the residence of the local governor during the Mughal rule"; "are evidently adjuncts of the mahal" (C07-MADHYABHARAT-019); "Mahal Qubba of Udaipur" (C10-JAGTA-EN-018)
- 7.10: "part of a lively bazaar" (C07-JAGTA-EN-034); "must then have been made, cutting one another at 90 degrees" (C07-JAGTA-EN-031)
- 7.11: "anywhere at all" (C07-JAGTA-EN-005); "exactly like the sanctum of some temple" (C07-JAGTA-EN-036)
- 7.16: "some attempt at a symmetrical arrangement of the dissimilar pillars appears to have been made with partial success" (C07-PANDE-007)
- 7.19: "respected vaguely by the people" (C07-GEOHER-031, RR-15); "10th Century" (C07-INTACH-027)
- 7.20: "later Parmar era" (C07-GEOHER-041)
- 7.22: "1059 CE" (C07-GEOHER-035, an R3 reading); "at a short distance to the north-east of the town" (C07-MADHYABHARAT-015); "cannot be identified" (C07-GANGULY-005); "cannot now be traced" (C07-GANGULY-007)
- 7.24: "considering the great merit of making provision for water" (C07-CII-003); "throughout ages been regarded as a meritorious cause" (C07-MADHYABHARAT-013)

Every quotation passed the verbatim check, which is case-sensitive. No quotation repeats one used in another unit or chapter: "of every kind", "is said to have been built" and the "chappan baoli" saying were unquoted in the line edit.

## Checks

- **Unit checks:** all 25 units are clean under `inhouse.py check`, covering verbatim quotes, names and numbers, source-led sentences, passive runs, meta language, agent nouns, testimony, ⚠ items, the ledger and the Gazetteer share.
- **Stitch:** `stitch.py 7 --check` reports equal (58,572 = 58,572).
- **Canon rules:** `ch_rules.py` reports 0 failures.
- **`prose_checks.py`:**
  - no narrator period terms, passive runs or testimony measurements;
  - the remaining agent nouns are all sourced;
  - colon reveals were cut from 1.6 to 0.7 per 1,000 words in the line edit;
  - triplets are at 1.6 per 1,000.
- **Spelling:** `dynasty_spelling.py check` is clean.

## Editorial read (14 questions)

1. **Concrete openings:** yes. Each unit opens on a wall, a hall, a lane, a stepwell or a stone. 7.25 opens on the treatise's named tank shapes.
2. **One argument per unit:** yes. The heading names the question.
3. **Place as subject; sources in the notes:** yes, enforced by the source-led check.
4. **Ranges and proposals for dates:** yes. Survey dates are flagged as proposals, and brackets are given where the fabric supports them.
5. **Conflicts stated, not resolved by fiat:** area (7.2), dating (7.4, 7.20), Moti Masjid (RR-13), the V.S. 1625 pillar (RR-14), north-west vs north-east (7.16) and Udaysagar vs Udayasamudra (7.22).
6. **Testimony marked:** Tiwari's readings are attributed in the notes, and his figures are not used as measurements.
7. **No catalogue:** inventory lists are summarised and minor items are set aside with reasons.
8. **No invented labour:** confirmed (see above).
9. **Muslim monuments as history:** three dated changes of master and a resident population, told without the period term.
10. **Boundaries:** pointers to Ch 1, 4, 5, 6, 8, 10 and 11, with no re-telling.
11. **Repetition:** checked against Chapters 1–6. Recalls are made in clauses (the Pisanhārī legend, the twelve-courtyard house, the 1059 reading).
12. **Opening from Ch 6:** 7.1 opens on the counted monuments, after Ch 6 ended on what the stones cannot say.
13. **Close into Ch 8:** 7.24–7.25 end on Vikrama's tank as water given for merit, handing the gifts to Chapter 8.
14. **Notes:** about one per paragraph, 52 in all. Each note gives attribution, conflicts or pointers.

## Deliverables

- `ch07/ch07_plan_v1.md`
- `ch07/ch07_draft_v1.md` (working draft with IDs)
- `ch07/ch07_draft_v1_footnoted.md` (52 footnotes; 14 bibliography entries, 13 of them still incomplete, as in earlier chapters)
- `ch07/Chapter 7 - The Wider Built Heritage of Udaypur - Draft v1.docx` (25 unit headings, none empty; ends on the bibliography)
- `ch07/ch07_draft_v1_report.md` (this file)
- `run/ledger/ledger_ch7.json` → `editorial/book_ledger.json` / `.md`
