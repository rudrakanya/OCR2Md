# Chapter 5, draft v1: drafted from the contents file (21 October 2026)

No API calls were made. The work was verified in-session, not by an independent model.

## State before this pass

- **No Chapter 5 plan or draft existed.** There was nothing in `drafting/ch05/`, nothing in `run/ch5/`, and nothing in `_archive/`.
- **The contents file** (`editorial/Udaypur_Book_Contents.md`) gives Chapter 5 twenty-eight units.
- **Earlier planning that no longer fits the contents file:**
  - The whole-book outline and the v2 outline (`editorial/wholebook/ch05.md`, `editorial/plan_v2/ch05.md`) planned a 7-section, 4,000-word chapter. The contents file has superseded both.
  - Their exclusion list (`excl_ch05.tsv`) was honoured where its reason still holds. Items excluded only because the 7-section plan had no room for them were reopened: the treatise, the norms, Śaiva doctrine and Kramrisch's symbolism now each have a unit.
- **The evidence map** (`ch05_udayesvara-temple.md` and `evidence_index/ch05.jsonl`) holds 982 items: 284 direct and 698 contextual. The brief's figure of about 204 refers to the subset the maps treat as core.

## Setup

- **Plan:** `ch05/ch05_plan_v1.md`. It has 28 units with paragraph evidence, the historical question for the chapter, the through-line, and the set-aside list.
- **Config:** `ch05/cfg_ch05v1.py`.
  - `NO_LENGTH`; `BUDGET 0`; Gazetteer cap 40%.
  - `extra_rules` enforce four things: SAMAR items are never quoted; 1059 appears only as a reading (R3); Karṇa is named by dynasty (R2); *Temple Economics* is excluded.
- **Pack:** `ch05/evidence_pack_v1.json`. It is the index without *Temple Economics*, plus C04-CII-108 and C04-CII-119 borrowed for the V.S. 1137 record.
- **Pande:** only `The Udayesvara Temple - Anupa Pande.md` is cited. The second OCR copy is the same book and is never cited alongside it.
- **Tools:** `_tools/stitch.py` and `_pipe/build_outputs.py` now include Chapter 5.

## Units

| Unit | Body words | Items | Direct items |
|---|---|---|---|
| 5.1 The parts of a northern temple | 481 | 15 | 2 |
| 5.2 Sanctum, vestibule, hall and porches | 462 | 17 | 15 |
| 5.3 The vedī | 373 | 9 | 8 |
| 5.4 The court and its attendant shrines | 411 | 16 | 13 |
| 5.5 The northern spire and its parts | 446 | 13 | 5 |
| 5.6 The star plan and the seven-tiered tower | 499 | 16 | 15 |
| 5.7 The Bhūmija style and its origins | 643 | 20 | 7 |
| 5.8 Udayeśvara among the Paramāra temples | 501 | 18 | 12 |
| 5.9 Khajuraho or the Deccan | 410 | 12 | 9 |
| 5.10 Base mouldings and wall | 467 | 11 | 9 |
| 5.11 Doorways, pillars and ceilings | 442 | 14 | 12 |
| 5.12 Ornament and attendant figures | 355 | 14 | 6 |
| 5.13 Stone, masons and workshops | 432 | 18 | 6 |
| 5.14 The dancing Śiva of the antefixes | 511 | 16 | 13 |
| 5.15 Guardians of the directions | 414 | 17 | 14 |
| 5.16 The Mother Goddesses | 422 | 13 | 10 |
| 5.17 Gods and goddesses of the hall walls | 444 | 18 | 18 |
| 5.18 Composite images | 376 | 12 | 10 |
| 5.19 Divine couples of the lower niches | 250 | 9 | 8 |
| 5.20 Porch balustrades and the hall interior | 329 | 12 | 12 |
| 5.21 The damaged images | 266 | 12 | 12 |
| 5.22 The sculptural style of Paramāra Malwa | 323 | 10 | 8 |
| 5.23 Images and the iconographic canons | 391 | 18 | 13 |
| 5.24 Building norms in the texts | 476 | 14 | 1 |
| 5.25 The Samarāṅgaṇasūtradhāra and its temple rules | 390 | 15 | 5 |
| 5.26 Śaiva Siddhānta doctrine | 375 | 11 | 3 |
| 5.27 Readings of the sculptural programme | 451 | 16 | 14 |
| 5.28 The temple as cosmos | 460 | 14 | 5 |
| **Total** | **11,800** | **330 distinct** | **205 of 284** |

- **Notes:** 80 reader-facing notes, one per paragraph.
- **Raw length:** the working draft, including IDs and notes, is 14,672 words.

**Short units, flagged rather than padded:**
- 5.19 and 5.21 rest on a few kinds of image and on testimony.
- 5.22 has few judgements on style that name Udaypur.

**Units built mostly from contextual items:** 5.1, 5.5, 5.24, 5.25, 5.26 and 5.28. The contents file sets these units on the type, the vocabulary, the norms and the doctrine. Each closes on Udaypur.

## Direct items: 205 used, 79 set aside

| Reason | Count | Items |
|---|---|---|
| The hill, its panels, petroglyphs and giant Naṭarāja, and the neighbouring villages (Ch 7) | 27 | GEOHER-002 to -017, INTACH-001 to -011, JAGTA-EN-003 |
| Hindi originals of English Tiwari items already used; Narayan Vyas's yakṣa (Ch 9); the name Nīlakaṇṭheśvara in the inscriptions (Ch 6); images in the museum and the villages (Ch 11/Ch 7) | 13 | JAGTA-HI-001, -003, -004, -005, -006, -008, -010 to -013; JAGTA-EN-014 to -016 |
| Restatements of features already cited from the primary describer | 16 | PANDE-015, -045, -046, -050, -072; KRAM-2-011, -023, -043; BHOJA-TIMES-003, -006, -010, -015; RAJABHOJ-EN-003; ARTPAR-013, -019, -021 (OCR-damaged) |
| 1059 as a fact: Record A's reading (R1/R3) | 5 | GANGULY-001, -003; KRAM-1-034, -081; KRAM-2-008 |
| Superlatives and evaluations (R7) | 6 | GEOHER-001, GAZ-004, GANGULY-002, BHOJA-TIMES-014, JAGTA-EN-008, and the duplicate JAGTA-HI-007 |
| Treatise texts quoted at length by Pande, not needed and not to be quoted | 4 | PANDE-056, -132, -135, -136 |
| Index entries and fragments | 4 | HARDY-006, KRAM-2-024, KRAM-1-031, KRAM-1-049 |
| Homed later | 3 | JAGTA-EN-002, -004 (survival memory, Ch 10); GANGULY-015 (brass sheath, Ch 10/11) |
| Another temple of the same name elsewhere | 1 | GAZ-003 |

## Architecture as history, not inventory

Each unit answers a historical question:
- **The type:** what kind of building the king commissioned (5.1).
- **The hall:** a building for assembled worshippers (5.2).
- **The vedī:** the rites at the door, with three readings left open (5.3).
- **The court:** one patron's design, now in ruin (5.4).
- **The star plan:** a figure fixed before building began (5.6).
- **The Bhūmija:** a dynasty's chosen emblem, in Hardy's reading (5.7).
- **Un:** a group of temples tied to the same king by an inscription (5.8).
- **The Deccan link:** explained politically by the Paramāras' frontiers (5.9).
- **Craft:** a royal workshop and the guilds behind it (5.10, 5.13).
- **Rule bent for symmetry:** a programme drawn up as a whole (5.15).
- **The Mothers:** a Śaiva set, matching the dynasty's habits in Vāgaḍa (5.16).
- **Composite images:** links to the image-making of Gujarat and Rajasthan (5.18).
- **Lamps and soot:** a temple in continuous use (5.20).
- **The damage:** blows aimed at the images, not the building, with the causes left to Ch 10 (5.21).
- **The treatise:** compatibility, not identity (5.25).
- **Śaiva doctrine:** recorded in Bhoja's book and on Udaypur's own stone (5.26).

Descriptions of the images give who stands where. Every reading of meaning is attributed and bounded:
- Pande's Śaiva Siddhānta reading, set against other explanations of the same facts (5.27);
- three readings of the figure near the summit (5.27);
- Kramrisch's cosmos against Granoff and Bafna (5.24, 5.28).

## Quotations used, with IDs

- "invariably *nirandhāra*" (C05-PANDE-003, 5.1)
- "still in excellent preservation after the lapse of eight centuries" (C05-PANDE-010, 5.3)
- "no surviving precedents … already the deluxe model" (C05-HARDY-005, 5.6)
- "no doubt to distinguish themselves from rival dynasties patronising mainly Shekhari temples" (C05-HARDY-017, 5.7)
- "affiliated more to the Deccani style than the Central Indian" (C05-TEMPLES-IND-014, 5.9)
- "appears as a deliberate attempt to give an exclusive Śaivite character" (C05-PANDE-115, 5.16)
- "now unfortunately coated with the grime and soot of the lamps burning in front of the image" (C05-PANDE-105, 5.20)
- "for the first time in an inscription pertaining to this house" (C05-CII-002, 5.26)
- "climbing up to heaven in virtue of the religious merit" (C05-MADHYABHARAT-008, 5.27)

## Canon and boundaries

- **R3.** 1059 appears only as Deva's start date, flagged as a reading (5.2, note); 1080 is the record.
- **R2.** The only Karṇa is "the Caulukya Karṇa of Gujarat" (5.13).
- **U1 and R4** do not arise in this chapter.
- **SAMAR.** No SAMAR item is quoted; SAMAR-2-083 (the Bhūmija pavilion) is paraphrased as a norm.
- **Pande.** The two OCR copies are never merged.
- **Handed on:**
  - inscriptions as texts and the name Nīlakaṇṭheśvara go to Ch 6;
  - the hill goes to Ch 7;
  - the damage, the shut east door and the mosque go to Ch 10;
  - the brass sheath and the temple's later care go to Ch 11.
- **The close.** The chapter ends on the temple's own inscribed words, leading into Chapter 6.

## Checks

- All 28 units are clean under `inhouse.py check`, including the ledger.
- The canon rules give 0 failures (`_tools/ch_rules.py`).
- The dynasty spelling check passes.
- The stitch check is equal, at 94,103 characters.
- **AI-shape** per 1,000 words: "not X but Y" 0.2, triplets 0.4, colon reveals 0.4 after the line edit.

**Verification in-session.** Every quotation was matched to its item, and claims were read against their items. Corrections made:
- **Vīrabhadra.** He strangles Dakṣa with his leg (he does not "crush" him), and there are Vīrabhadras on both the south and west spines.
- **Composite images.** "Never" was softened to "not", as the source has it.
- **The Nandi.** It is "looks modern", not "renewed".
- **Tiwari.** His height for the goddess's image was dropped, because testimony is not used as a measurement.
- **The sanctum doorway.** The quoted phrase "for the reader" was dropped because it tripped the meta-commentary check.
- **ARTPAR-012.** The evidence map's gloss renders the 1063 date of the Amareśvara as "Vikrama era", but the Hindi has ई० (A.D.). The text follows the Hindi and Deva, and a note says so.

## Editorial read (14 questions)

All units pass. Marginal points:
- 5.17 to 5.20 are the most descriptive units. Each is kept to the pattern (hierarchy, pairs, couples, continued worship) rather than niche by niche.
- 5.7 and 5.8 name scholars in the text because their identity is the point (competing datings).
- 5.13 P4 keeps Tiwari's round numbers as memory only, and the note says they contradict each other.

## For your decision

- **The ARTPAR-012 gloss.** It should be corrected in the evidence map: the Hindi reads 1063 A.D., not Vikrama.

## Deliverables

- `ch05/ch05_draft_v1.md`: the working draft, with IDs.
- `ch05/ch05_draft_v1_footnoted.md`: 80 notes and 17 bibliography entries, 16 of them still incomplete, as in earlier chapters.
- `ch05/Chapter 5 - The Udayeśvara Temple - Draft v1.docx`: all 28 units present, ending on the bibliography, none empty or truncated.
- Ledger: `run/ledger/ledger_ch5.json`, merged into `editorial/book_ledger.json`.
- Plan, config and pack: `ch05/ch05_plan_v1.md`, `ch05/cfg_ch05v1.py`, `ch05/evidence_pack_v1.json`.
