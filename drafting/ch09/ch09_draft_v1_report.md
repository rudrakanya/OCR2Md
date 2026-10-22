# Chapter 9, draft v1: Society and Cultural Life (21 October 2026)

Drafted in-session from the contents file (`editorial/Udaypur_Book_Contents.md`, Chapter 9: 9 units). No API calls, Chroma queries or paid ledger runs were used.

## 0. State before work

- **No Chapter 9 material existed.** There was no `ch09/` folder, plan, cfg, pack or draft, and no `run/ch9/` sections.
- **Contents file:** 9 units, from 9.1 (communities today) to 9.9 (the memory of decline).
- **v2 outline:**
  - 6 sections, with a 2,800-word target approved as an exception (U2); length followed the evidence, not that number.
  - Its item map, opening (the lane by the temple, described by community) and closing (Daulatpur as memory, no location) were carried over the 9 units, with no units added, dropped, split or merged.
  - C09-GAZ-011 (Kham Baba, which is Besnagar) stays excluded.
- **Evidence:** `ch09.jsonl` holds 75 items, 32 direct and 43 contextual. The pack has 93 items, adding recalls from Chapters 1, 5, 6, 8 and 12 and the Afterword.

## Files

| Item | Path |
|---|---|
| Plan | `ch09/ch09_plan_v1.md` |
| cfg | `ch09/cfg_ch09v1.py`: NO_LENGTH; Gazetteer share ≤ 0.40. Extra rules: living residents named → fail; anonymous labour; Temple Economics; R2/R3/R4. |
| Pack | `ch09/evidence_pack_v1.json` |
| Sections | `run/ch9/9.1–9.9.md` |
| Ledger | `run/ledger/ledger_ch9.json`, merged; the header reads "Chapter 9 (v1)" |

## Units

| Unit | Body words | Items | Direct (ch09) |
|---|---|---|---|
| 9.1 Communities today *(legal review)* | 245 | 9 | 5 |
| 9.2 Identities remade *(thin; legal review)* | 212 | 4 | 1 |
| 9.3 Society in Paramāra Malwa | 249 | 10 | 1 |
| 9.4 Languages of the district *(thin)* | 219 | 6 | 0 |
| 9.5 Festivals, fairs and everyday life | 373 | 13 | 2 |
| 9.6 The founder and the temple in local stories | 397 | 9 | 7 |
| 9.7 The legend of Berni Mata | 339 | 8 | 6 |
| 9.8 Bhoja in proverb and song | 287 | 11 | 2 |
| 9.9 The memory of decline | 241 | 9 | 4 |
| **Total** | **2,562** | **75 distinct** | **26 of 31** |

The body runs 2,562 words, under the outline's 2,800, because the evidence ends there. No unit was padded.

**Direct items set aside (5):**
- C09-GANGULY-003: the snake legend's middle, already told in 1.6;
- C09-GAZ-009: its fact is kept in a note, to hold 9.5's Gazetteer share under 40%;
- C09-JAGTA-HI-001: Tiwari's hostile passage on green cloths and a *pīr*, deferred to Ch 12 and the Afterword per the outline;
- C09-JAGTA-HI-004 and -014: Hindi duplicates of English items used.

## Oral tradition as memory; regional patterns labelled

- **Every tradition carries its standing in the sentence:** "it is said", "the story goes", "local folklore keeps", "a claim that … needs to be confirmed", "the town's own memory".
  - 9.6 states that the stories "are evidence of memory … not of the events they tell".
  - 9.7 sets the three Berni Mata versions side by side and shows the fuller one gaining a king, a wager and a caste. The name link Bedni/*bednī* is marked as a coincidence, not a derivation.
  - 9.8 marks Rajpurohit's reading of the Gaṅgī Telan proverb as interpretation.
  - 9.9 ends with the remembered decline handed to Chapter 10 to test.
- **Regional and district evidence is labelled where it is used:**
  - "This is the kingdom's society … the town's records do not say" (9.3);
  - census figures given as the district's, with no Udaypur counts (9.1, 9.4);
  - "Whether Udaypur kept any of these, the record does not say" (9.5, court festivals);
  - "Everyday life is known for the modern district" (9.5).
- **No counts from Tiwari:** not the population, the Muslim share, the Jain families or the police.

## Flagged for legal review (Chapters 11–12 schedule)

- **9.1:** Tiwari's lane names six residents. None is named here; the households are described by community. Tiwari's claim of shared ancestry is attributed as "a claim about belonging, made by a visitor".
- **9.2:**
  - A living family's claim of Paramāra descent and an ancestor's conversion. The person and the family name are not given, and Tiwari's general remarks on conversion are not carried.
  - The Bagdi tradition. Tiwari's account of the community's caste registration "for the benefit of reservation", and his phrase "remnants of the era of slavery to Muslim rule", are not carried; only the neutral fact that the descendants are recorded in different categories in two districts remains.
- **Enforcement:** the cfg "living resident named" rule passes.

## Thin units

- **9.2:** two traditions from one writer, untestable from the sources.
- **9.4:** the census counts the district, not the village; the village's own speech is undocumented, which the unit states.
- **Also stated plainly:** no record gives the numbers of Udaypur's communities (9.1), or who first lived there (9.3).

## Canon and tiers

- **Canon:** `ch_rules.py` reports 0 failures; `dynasty_spelling` is clean.
- **Tiwari:** named in full in 1.1 and plain "Tiwari" here, with no gendered pronouns; testimony throughout.
- **Gazetteer and surveys:** tier 7, phrased as their own statements.
- **Boundaries:** ritual and the fair's size go to Ch 8; modern institutions to Ch 11–12; Tiwari's invitation to writers to the Afterword.

## A few quotations with IDs

- "identity too was broken" (C09-JAGTA-EN-001)
- "Theirs was an organized power." (C09-JAGTA-EN-005)
- "fourth thread" (C09-JAGTA-EN-007)
- "Kathe Raja Bhoj ne kathe Gangu Teli" (C09-RAJABHOJ-EN-005)
- "Kathe Raja Bhoj ne kathe Gangi Telan" (C09-RAJABHOJ-EN-005)
- "The doctrine …" verse: not repeated here (8.12)

Two repeats of earlier chapters were unquoted in the line edit: the snake legend's last line (1.6) and the shared-reverence line (1.2).

## Checks

- **Unit checks:** all 9 units are clean under `inhouse.py`.
- **Stitch:** `stitch.py 9 --check` reports equal.
- **Canon rules:** 0 rule failures.
- **`prose_checks.py`:**
  - no narrator period terms, passive runs or testimony measurements;
  - the agent nouns are all sourced (craftsmen, mason, workmen);
  - colon reveals were cut from 3.1 to 0.8 per 1,000 words in the line edit.

## Editorial read (14 questions)

1. **Concrete openings:** a lane, a claim at a meeting, the castes of the grants, the census, the fair, the tellers, a vermilion figure, a proverb, a shrine at the *gaḍhī*.
2. **One argument per unit:** yes.
3. **Place as subject; sources in the notes:** yes.
4. **Calibrated verbs:** "probably", "may preserve", "it is alleged".
5. **Conflicts side by side:** the three Berni Mata versions; Malwi against Bundeli across the censuses.
6. **Testimony marked:** yes.
7. **Restraint:** yes.
8. **No invented communities or customs:** confirmed.
9. **Tradition as memory:** yes.
10. **Boundaries:** kept.
11. **Repetition:** recalls of Ch 1 legends are made in clauses.
12. **Opening from Ch 8:** opens on the people beside the temple, after Ch 8 ended on the temple still visited.
13. **Close into Ch 10:** the memory of decline, to be tested.
14. **Notes:** 22, about one per paragraph; 9.8's last paragraph carries none.

## Deliverables

- `ch09/ch09_plan_v1.md`
- `ch09/ch09_draft_v1.md`
- `ch09/ch09_draft_v1_footnoted.md` (22 footnotes; 13 bibliography entries, 12 still incomplete, as before)
- `ch09/Chapter 9 - Society and Cultural Life - Draft v1.docx` (9 unit headings, none empty; ends on the bibliography)
- `ch09/ch09_draft_v1_report.md`
- `run/ledger/ledger_ch9.json` → `editorial/book_ledger.*`
