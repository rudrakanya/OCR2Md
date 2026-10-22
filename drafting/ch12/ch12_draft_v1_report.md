# Chapter 12, draft v1: Udaypur Today (21 October 2026)

Drafted in-session from the contents file (`editorial/Udaypur_Book_Contents.md`, Chapter 12: 10 units). No API calls, Chroma queries or paid ledger runs. Verified in-session against the pack and the source Markdown, not by an independent model.

## 0. State before work

- **No Chapter 12 material existed:** no `ch12/` folder, plan, cfg, pack or draft, and no `run/ch12/` sections.
- **Contents file:** 10 units, from 12.1 (population and the census) to 12.10 (expectations of a tourist town).
- **Whole-book outline (`editorial/wholebook/ch12.md`):** 6 sections, 3,750-word target (not used as a target), rules R5–R8 and U7, wildlife moved in from Ch 2. Its item map, opening and closing were redistributed over the 10 units; no unit added, dropped, split or merged.
- **Evidence:** `ch12.jsonl`, 77 items (71 direct, 6 contextual).
- **Chapter 11** was drafted in parallel by another session (v1 delivered 21 Oct) while this work was in progress. Chapter 12 was then aligned to it: it opens from 11.8's close ("…its households, fields and quarries, to which the next chapter turns") and recalls 11.4, 11.6, 11.7 and 11.8 in clauses only.

## Files

| Item | Path |
|---|---|
| Plan | `ch12/ch12_plan_v1.md` |
| cfg | `ch12/cfg_ch12v1.py`: NO_LENGTH; Gazetteer share ≤ 0.40. Extra rules: residents/claimants named (U7) → fail; excluded passage used; lane house identified by signboard; testimony counts (R5); mining allegation in more than one sentence; anonymous people |
| Pack | `ch12/evidence_pack_v1.json` (140: the index, 47 borrowed recalls, 16 new corpus slices `C12-KBN-JAGTA-EN-001…016`) |
| Sections | `run/ch12/12.1–12.10.md` |
| Ledger | `run/ledger/ledger_ch12.json`, merged; the header now names Chapters 11 and 12 |

## Units

| Unit | Body words | Items | Notes |
|---|---|---|---|
| 12.1 Population and the census record | 246 | 11 | 3 |
| 12.2 Roads, stations, schools and the panchayat *(thin)* | 248 | 10 | 3 |
| 12.3 Living inside the old town *(thin; legal review)* | 197 | 8 | 3 |
| 12.4 Fields, the market and the quarries *(legal review)* | 303 | 13 | 4 |
| 12.5 The living hill | 397 | 15 | 4 |
| 12.6 The temple's visitors *(legal review)* | 331 | 11 | 3 |
| 12.7 The town becoming visible, 2020–21 *(legal review)* | 378 | 15 | 3 |
| 12.8 The lane to the temple, 2021 *(legal review)* | 312 | 13 | 3 |
| 12.9 Outsiders' views of residents and officials *(legal review)* | 355 | 18 | 3 |
| 12.10 Expectations of a tourist town | 435 | 19 | 4 |
| **Total** | **3,202** | **120 distinct** | **33** |

Length follows the evidence; nothing was padded. **Thin:**
- 12.2: the state's record of services stops in 1979, and the text says so.
- 12.3: two households and Vadnerkar's observation; the rest of the old town's fabric is Ch 7's.

**Direct items used: 62 of 71.** Set aside, with reasons:
- C12-JAGTA-HI-002, -012: testimony distances (150 km; temple visible at 5 km).
- C12-JAGTA-HI-008, -018: replaced by their English text (C12-KBN-JAGTA-EN-010, -012), so the quotations are the translation's, not my Hindi gloss.
- C12-JAGTA-HI-009: already used in 8.7.
- C12-JAGTA-HI-013: defaced images, Chapter 11.7.
- C12-JAGTA-HI-020: the signboard post, Chapter 11.6 (U7).
- C12-JAGTA-EN-003: Tiwari's network allegation. Chapter 11 (11.8) already gives the book's single mining-allegation sentence (U7); a second one here would break it.
- C12-JAGTA-EN-007: green cloths and a *pīr* (see legal list).

**Contextual set aside:** C12-GAZ-001, -002, -003 (district totals and rates; Gazetteer cap); C12-JAGTA-HI-010 (traders' wealth; location unclear and a count).

## Flagged for pre-publication legal review

1. **12.3 P3:** the two households living in front of the temple. They are not named, and Tiwari's word "encroachment" is not used. This matches Ch 11's LR-3 on 11.4.
2. **12.4 P3:** quarry wages from Saxena's ground report. Tiwari's allegation about who profits is not repeated (U7; LR-2 is held in 11.8).
3. **12.6 P2:** officials' VIP *darśan* (sub-divisional officers, tahsildars, collectors as offices; no one named).
4. **12.6 P3:** Tiwari's complaint about the ASI's staff at the temple.
5. **12.7 P1:** the Ganj Basoda volunteers. They are named in the source but not here; the returned image is recalled from 11.7.
6. **12.7 P3:** Saxena's film of the palace and its roof "kept as private property". The dispute is 11.6's, and no claimant is named.
7. **12.8 P2:** the shopkeeper who set back his shop first. The source names him in two spellings (RR-29); he is not named here. The volunteers named by Vadnerkar are not named either.
8. **12.8 P3:** the one house left jutting into the lane. The source identifies it by a mosque's signboard, which is withheld here, and the text gives no motive.
9. **12.9, all three paragraphs:** outsiders' verdicts on residents, panchayat representatives, officials and administrators, each attributed (Tiwari; Upadhyay as Tiwari reports him; Mishra as Tiwari reports him). Named: Madanmohan Upadhyay (INTACH convener, retired IAS), a living public figure, quoted on residents' "indifference".
10. **12.10 P2:** Upadhyay's prediction (named, attributed).
11. **Not used at all, for your ruling:** C12-JAGTA-EN-007 (also C09-JAGTA-HI-001). This is Tiwari's prediction about green cloths, a *pīr* and future *mazars*, aimed at a religious community and at officials. Ch 9 deferred it to Ch 12 or the Afterword. I judged it a contested present-day matter of the kind U7 keeps out, not an observation of the historic environment.

**Named living people, all treated factually and attributed:**
- Tiwari;
- Govind Saxena (journalist, already named in 2.10);
- Ajit Vadnerkar and Shivkumar Vivek (signed guest pieces);
- Madanmohan Upadhyay.

Suresh Mishra died in April 2021.

## U7, claimants, the present as evidence

- **U7 is honoured.**
  - No claimant from the 2021 signboard is named; the palace appears only as filmed and "kept as private property", with 11.6 pointed to.
  - The mining allegation keeps its single book-wide sentence in 11.8.
  - The cfg's living-resident and claimant rule passes, with 0 failures (`ch_rules.py`).
- **The present is told as evidence.**
  - Every present-day statement is cited to the survey, the Gazetteer, INTACH or a named witness.
  - "Today" is defined once (12.1): the early 2020s, the latest surveys, walks and posts, with dates of observation (January 2021; 20 February 2022) in the notes.
  - Verdicts and predictions are framed as attitudes ("Each of these is an attitude, recorded at a moment; none is yet a plan carried out").
  - There is no recommendation; the proposals are left to the Afterword.
- **R5 (testimony numbers):** none of Tiwari's counts, widths or distances is used. This excludes the eight thousand, the lane's widths, the "lakh" of viewers, the hundred in the hall, the forty traders, the four hundred police and the age.
- **Accepted checker flags (2):** "At the turn of 2021" (12.7) and "In early 2021" (12.8) trip the testimony-as-date check. They are dates of observation, which the brief asks for, and they are not historical facts. They are kept, and the exact day is open (RR-28). All other units are clean under `inhouse.py check`.

## Attribution finding (RR-30, partly resolved)

- **Who wrote pp. 161–166.** The Hindi pages 161–166 are not Tiwari's.
  - Pp. 161–162 are Shivkumar Vivek's Facebook post of 20 February 2022.
  - Pp. 163–166 are Ajit Vadnerkar's post.
  - Both are signed in the book.
- **How Ch 12 handles it.** C12-JAGTA-HI-007, -008, -018, -038, -039, C12-JAGTA-EN-014 and C13-JAGTA-HI-020 are therefore attributed to Vadnerkar. The "he" of C12-JAGTA-HI-017 / -EN-013 is Tiwari (Vivek's words).
- **Knock-on for Chapter 1 (not changed here).** §1.1 gives "cannot even be called a town (*kasba*) today" (C01-JAGTA-EN-015, p. 163) as Tiwari's; it is Vadnerkar's. The fix is a note change in 1.1, for your approval.

## Wildlife

Wildlife sits in 12.5, as the plan places it. It covers:
- the bats, now told as habitat (2.3 had the caves as geology);
- the survey's fifty-eight-plus bird species, the vultures and the winter migrants;
- the district's birds and mammals, labelled as district evidence;
- the 1968 "Udaipura" shooting block, not shown to be this hill (RR-27);
- poaching.

All of it is attributed in the notes.

## The through-line lands

- **The opening.** 12.1 opens from 11.8's close, below the hill, on the census count of houses.
- **The closing paragraph of 12.10** gathers the arc from the ledger without retelling it:
  - the town that bore Udayāditya's name (4.18);
  - Caulukya rule and Ajayapāla's record (6.18);
  - Tughluq's mosque from demolished shrines (6.20);
  - the 1979 judgement, "once a place of considerable importance", now "a large village" (1.1);
  - Vadnerkar's "sleeping sort of village".
- **It ends on a sentence of interpretation:** "A place whose meaning a king once fixed by founding it is now given its meaning between the people who live in it and the people who come to look." It then hands the question to the Afterword.

## A few quotations with IDs

- "a published page of the story of Udaipur" (C07-JAGTA-EN-037)
- "a necessary rite like offering flowers" (C12-JAGTA-EN-016)
- "Udaipur's perishing wealth" (C12-JAGTA-EN-006)
- "a distance filled with a kind of indifference" (C12-KBN-JAGTA-EN-015, Upadhyay as reported)
- "positive and inspiring" (C12-KBN-JAGTA-EN-002)
- "risen to its feet to bring back the glory and splendour lost over the centuries" (C12-KBN-JAGTA-EN-012, Vadnerkar)
- "once a place of considerable importance" … "a large village" (C01-GAZ-008)

## Checks

- **`inhouse.py check`:** 8 of 10 units are clean; 12.7 and 12.8 carry one accepted date-of-observation flag each.
- **`ch_rules.py`:** 0 failures. **Dynasty spelling:** clean. **`stitch.py 12 --check`:** equal.
- **`prose_checks.py`:**
  - no passive runs or narrator period terms;
  - shape markers per 1,000 words: "not X but Y" 0.3, triplets 0.6, colon reveals 0.3;
  - 12 minor word-repetition warnings remain.
- **Gazetteer share:** 12.1 and 12.2 are at 40%, the limit; all other units are under it.

## Editorial read (14 questions)

1. **Concrete openings:** the census's houses; a bus stand; a dwelling cleared from a ruin; wheat for the *mandi*; bats; daily *darśan*; walkers in the lanes; the narrow lane; a first sight of the town; residents' curiosity.
2. **One argument per unit:** yes.
3. **Place as subject; sources in the notes:** yes. 12.9 names its witnesses in prose because the unit is about whose view it is, at most one name per sentence.
4. **Calibrated verbs:** "may also hold", "by the survey's reckoning", "has seemed to visitors", "the record does not say".
5. **Conflicts side by side:** 928 against 1,619; Ganj Basoda against Bareth as the nearest station; the verdicts against the lane.
6. **Testimony marked:** yes, including the guest voices.
7. **Restraint:** no counts from testimony; no advocacy.
8. **No invented residents or scenes:** confirmed; people act only where an item names the act.
9. **Tradition and present practice told as observed:** yes.
10. **Boundaries:**
    - the social fabric is Ch 9's;
    - the administration, the palace, thefts and threats are Ch 11's, recalled in clauses;
    - the proposals are the Afterword's.
11. **Repetition:** the recalls of 1.1, 1.2, 2.3, 2.6, 2.10, 7.10, 8.7 and 11.4–11.8 are clauses.
12. **Opening from Ch 11:** yes.
13. **Close into the Afterword:** yes.
14. **Notes:** 33, about one per paragraph.

## Open

- RR-26: the 1901 figure.
- RR-27: the 1968 table.
- RR-28: the date of the widening.
- RR-29: the shopkeeper's name (withheld).
- RR-30: partly resolved; the 1.1 attribution fix is pending.
- The EN-007 ruling.
- Legal review of the passages listed above.

## Deliverables

- `ch12/ch12_plan_v1.md`
- `ch12/ch12_draft_v1.md` (working draft with every claim's IDs)
- `ch12/ch12_draft_v1_footnoted.md` (33 footnotes; 10 bibliography entries, still incomplete as in earlier chapters)
- `ch12/Chapter 12 - Udaypur Today - Draft v1.docx` (10 unit headings, none empty; ends on the bibliography)
- `ch12/ch12_draft_v1_report.md`
- `run/ledger/ledger_ch12.json` → `editorial/book_ledger.*`
