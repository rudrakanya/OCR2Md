# Chapter 2, draft v4: rebuilt from the contents file (19 October 2026)

Chapter 2 was rebuilt the same way as Chapter 1 v6, with the 19 October quality pass applied as it was drafted. It has ten units, one for each unit of `editorial/Udaypur_Book_Contents.md`, in that order. No API calls were made. The work was verified in-session, not by an independent model.

## Setup

- **Plan:** `ch02/ch02_plan_v4.md`. It sets out the historical question, the through-line and the arc, and gives each unit's paragraph evidence. It has no word targets.
- **Config:** `ch02/cfg_ch02v4.py`.
  - `NO_LENGTH = True`; `SETTLED = []`, since Chapter 2 gives no distances from Udaypur.
  - Tiwari is named in full in 1.1, so here he is "Tiwari".
  - Canon rules: no lichen dating, which belongs to Ch 7, and no adopted 1059 (U6).
- **Pack:** `ch02/evidence_pack_v5.json`. It is the v4 pack plus 17 items sliced verbatim from the local corpus with `_tools/kb_new.py` (`C02-KBN-*`), added with `_tools/pack_add_kbn.py`. The v4 pack is unchanged.
- **Sections:** `run/ch2/2.1.md` to `2.10.md`. `_tools/stitch.py` and `_pipe/build_outputs.py` now point to the v4 config.
- **The old v3** (five sections, 14 October) stays in `_archive/pre_contents_rebuild/ch02/`.

## Units

| Unit | Body words | Items | New corpus items used |
|---|---|---|---|
| 2.1 The Betwa and its streams | 594 | 23 | 0 |
| 2.2 Plateau, ranges and rocks | 422 | 14 | 0 |
| 2.3 The Udaypur hill: mesa, butte and caves | 567 | 21 | 4 |
| 2.4 The monsoon and its failures | 674 | 31 | 4 |
| 2.5 Black soil and the two harvests | 600 | 17 | 0 |
| 2.6 Forest, grass and grazing | 428 | 14 | 1 |
| 2.7 Water and the siting of settlement | 652 | 21 | 0 |
| 2.8 Bhoja's lake at Bhojpur | 624 | 24 | 5 |
| 2.9 Sandstone for building | 407 | 15 | 3 |
| 2.10 A town of its own stone | 408 | 18 | 1 |
| **Total** | **5,376** | **181 distinct** | **18** |

- **Comparison with v3:** v3 had five sections, about 2,600 body words, 108 items and 22 notes.
- **Notes:** 36 reader-facing notes, one per paragraph. The working draft keeps every claim's IDs.
- **Shorter units:** 2.2, 2.6, 2.9 and 2.10 are shorter because their evidence is narrower; none was padded.

## Unused pack items (54) and why

- **Belong to other chapters:**
  - wildlife (GAZ-033, -035, -036; GEOHER-022, -023) → Ch 12;
  - lichens (GEOHER-024, -025) → Ch 7 and Ch 11;
  - the fort wall (GEOHER-030; KB-GEOHER-004) → Ch 7;
  - laterite iron ore (GAZ-044) → Ch 8;
  - the Candella occupation (KB-GAZ-018) → Ch 4;
  - the route from Bareth (KB-MADHYABHARAT-002) → Ch 1;
  - irrigation projects (GAZ-058 to -060) → Ch 8;
  - population growth (BETWA-FLOW-015) → Ch 12.
- **Duplicates of items used:**
  - JAGTA-EN-002 and KB-JAGTA-EN-002;
  - KB-GAZ-010 and -011;
  - BETWA-FLOW-001, -002, -006 and -012;
  - INTACH-001 and -002 (garbled OCR of GEOHER-006).
- **Station-by-station detail of the climate trends** (BETWA-CLIM-002 to -014, -019, -020; BETWA-FLOW-007, -009): summarised in 2.4 and in the notes, not itemised.
- **Unreliable text:**
  - the land-use tables GAZ-056 and -057 (garbled);
  - GEOHER-012 (the survey's "moraine");
  - SAMAR-1-001 (old OCR, never quoted; the treatise is given from the Hindi summary in *Bhojadeva*).
- **Other:**
  - GEOHER-004 (the survey's statement of method);
  - KB-GEOHER-009, -014, -015 (overlap with items used);
  - KB-GEOHER-020 (the temple fragments in a baoli embankment, left to Ch 7 because the survey does not clearly say which structure it means);
  - KB-GAZ-002 (the item does not name its river).

## Craft

- **Openings:** each unit opens on something concrete: the Kewtan a kilometre off; the foothills of the Garhi–Teonda range; the skyline hill; the 360.2 mm day at Basoda in 1951; *kali-matti*; Van Tulsi on the hill; wells that fail in summer; Bhoja's illness and the 365 streams; Cunningham's sentence on the red stone; Tiwari's stone shops.
- **Handovers:** each unit hands on to the next. 2.3 ends on dry heights and a rock-cut tank, and 2.4 opens on the rain. 2.4 ends on runoff, and 2.5 opens on "what the rain leaves behind". 2.7 ends on made water, and 2.8 compares Bhoja's.
- **Close into Chapter 3:** 2.10 sets the land as setting, not cause. The town did not choose itself because of its stone, whatever Tiwari's view. The chapter ends on earlier users of the valley: the Bhujariya Talab, the canal from the dammed Bes at Vessanagar, and the Betwa valley road to Pataliputra.
- **Kept apart (compatibility is not identity):**
  - the survey's Kewtan and the Gazetteer's Keotan;
  - the survey's "Udaypur Hill" and its two named hills;
  - the Udayasamudra of the inscription and the Udaysagar.
- **Ranges where the sources differ, with both views attributed in notes:**
  - the survey's hill heights;
  - the lake's irrigation (Rajpurohit against Singh);
  - who broke the Bhojpur dam (Shah Hussain or Hoshang Shah).
- **U7:** one attributed sentence on the illegal-quarrying report (Govind Saxena's, cited by Tiwari), naming no one accused.
- **U6:** the survey's 1059 date for the Udaysagar is not adopted.

## Checks

- All ten units are clean under `inhouse.py check`, with no length checks. The check covers verbatim quotations, valid IDs, names and numbers, source-led sentences, agent nouns, narrator terms, passive runs, D1 spelling and the ledger.
- **AI-shape** for the stitched chapter, per 1,000 words: "not X but Y" 0.2, triplets 0.4, colon reveals 0.2, and 0 for each of the rest.
- The dynasty spelling check passes on the stitched and footnoted files.
- **Verified in-session:** every new detail was read against its item's full quotation. Fixes that came out of that:
  - an imperfectly printed rainfall table was moved to a note;
  - "the lake did not survive the dynasty by long" was replaced by "some four centuries" (Singh);
  - a claim that the temple's stone and the hilltop fragments are "the same" stone was dropped;
  - a stepwell's use was softened to the survey's "must sometimes have".

## Editorial read (the 14 questions)

All ten units pass. Marginal points:
- 2.4 P4, Q9: the modern trend paragraph is kept to today's regime, with projections in the note.
- 2.6 P2: the 1968 count is cited only for the range Udaipura sat in; its figures belong to Ch 12.
- 2.9 P3, Q11: Kramrisch's account of the texts is general and marked as not referring to Udaypur.

## Deliverables

- `ch02/ch02_draft_v4.md`: the working draft, with IDs.
- `ch02/ch02_draft_v4_footnoted.md`: 36 notes and 16 bibliography entries, 15 of them still incomplete, as in Ch 1.
- `ch02/Chapter 2 - The Betwa Valley - Draft v4.docx`: all ten units present, none empty.
- The ledger: `run/ledger/ledger_ch2.json`, merged into `editorial/book_ledger.md` (52 people, 42 terms, 27 places).
