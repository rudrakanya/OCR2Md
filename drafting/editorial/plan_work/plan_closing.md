# Cross-Chapter Architecture (updated by the evidence-grounded pass)

*The full architecture (threads, actors, terms, echoes, the duplication-risk table) is in the master outline, Part III. It still holds. This section records what the evidence pass changed or confirmed.*

## A. Chain of chapters (last move → first move)

| From → to | Last paragraph ends on | Next opens on |
|---|---|---|
| 3 → 4 | "Who held the hill itself in those years is not known." | Sīyaka II's eastern limit at Vidisha (C04-GAZ-001, C04-GANGULY-035) |
| 4 → 5 | The Udayeśvara as the one work a contemporary record assigns to the reign | The temple faces east but is entered from the west (C05-PANDE-002, -011) |
| 5 → 6 | The flag-bearer and the god's name at the east doorway (not read) | The six lines of V.S. 1137 and their named poet (C06-CII-006, C06-JAGTA-HI-008/-009) |
| 6 → 7 | Mosques and gates with Persian inscriptions: dated, not described | The nameless wall on the hill (C07-GEOHER-002) |
| 7 → 8 | Vikrama's tank and its stated uses (water as merit) | Dhāmadeva's four *biswa* given to the god, 1229 (C08-CII-020) |
| 8 → 9 | The time-keepers' family and its hereditary service | A lane of Hindu and Muslim neighbours (C09-JAGTA-HI-005) |
| 9 → 10 | The remembered deserted market of Daulatpur (memory only) | **The V.S. 1220 record naming a Gujarat king at Udaypur** (C10-PARTEMPLES-001, C10-CII-002) |
| 10 → 11 | The Gazetteer's "once a place of considerable importance" | Beglar's tour, 1871–72 (C07-PANDE-005) |
| 11 → 12 | The people at the record's edges | A family's house cleaned out of an excavation (C12-JAGTA-HI-014) |
| 12 → AW | Residents' hopes; outsiders' plans | Tiwari's 2019 letter (C13-JAGTA-EN-001) |
| AW → end | The village under the temple (1.1) | — |

The QC script prints each unit's Out beside the next unit's In (`plan_work/QC_REPORT.md`). All ten pairs were read and match.

## B. One primary home (rule applied by script, 15 Oct)

**Rule:** an item establishes (E) a claim in **one** unit only, its home. The home is the unit of its ID prefix; where neither unit is the prefix unit, the earlier unit is the home. Any other unit cites it as **C**, marked "(home Ch N: cross-reference)", and tells it in a clause, or reinterprets it for its own question (Part I, I.4 of the master outline).
- **22 duplicate establishing uses** were demoted (`_tools/demote_dupes.py`). They fall into four groups:
  - Ch 6 and Ch 10 shared the porch and political records. Ch 6 keeps the texts; Ch 10 keeps C10-PARTEMPLES-001 and C10-MADHYABHARAT-006.
  - Ch 7 and Chs 10–11 shared the mosques, buildings and protection rows. Ch 7 keeps them.
  - Ch 8 and Ch 10 shared Ganguly's governor items. Ch 8 keeps them.
  - Ch 11 and the Afterword shared the survey's condition items. Ch 11 keeps them; the Afterword keeps C13-GEOHER-004; Ch 12 keeps C12-JAGTA-HI-016.
- **Earlier hand fixes:**
  - C04-CII-119 → Ch 4;
  - C06-CII-011, -032 and -013 → Ch 6 (Ch 7 establishes the tank with C07-CII-003);
  - C07-MADHYABHARAT-011 and -012 → Ch 7;
  - C06-CII-037 and -038 → Ch 6;
  - C08-PANDE-011 → Ch 8;
  - C04-CII-131 → Ch 4;
  - C05-PANDE-008 and C05-GANGULY-012 → Ch 5 (the 11.1 paragraph is now recall-based).

## C. Evidence moved at plan stage

- **C10-GAZ-041, -042, -045, -046, -047** (1858–59; the Praja Mandal; Madhya Bharat, 1956): from 10.5 to 11.2. They also fill the master outline's flag that the state succession had no item.
- **C10-GAZ-052, -053** (census): from 10.5 to 12.1.
- **C10-GEOHER-001** (the survey's Paramāra attribution of the fort's antiquities): to 7.1 P4 as C.
- **The hill's sculpture:** home 7.1 P3a (from the merge).

## D. New evidence (kb-new, free local search)

- **C10-KBN-MADHYABHARAT-001 to -004** (Patil, *Cultural Heritage of Madhya Bharat*, pp. 15 and 43; T5): the Maratha settlement of Madhya Bharat from the 1730s to the 1790s, and the Maratha states under British paramountcy.
  - They are a regional frame for 10.5 P1, never Udaypur-specific.
  - They were sliced verbatim by `_tools/kb_new.py` and stored in `evidence_index/kb_new.jsonl`.

## E. Concepts introduced once (confirmed; see master outline Part III, E)

- **Glossed in Chs 1–3, never re-glossed:** *Bhūmija* (1.3), *kund* and *baoli* (2.4), *praśasti* (1.2).
- ***mahāsādhanika*:** first glossed in 10.1. The ledger shows 1.2 used it unexplained; 1.2 now adds the Caulukya master (U1) but still no gloss.
- ***biswa*:** unglossed in 6.4, glossed in 8.1 P2.
- ***pañcakula*:** glossed in 6.4, recalled in 8.1.

# Downstream Drafting Protocol (updated)

*The house voice, the failure table, evidence handling, chapter shape and continuity machinery are in the master outline, Part IV (P1–P10). They still bind. Updated here for the user's rulings of 15 October.*

1. **No paid API calls of any kind** for the rest of the project: no judge, verify, re-verify or final read, and no embeddings for knowledge-base search. The cost-guarded commands in `_pipe/inhouse.py` (judge, verify, reverify, finalread), `ledger.py build|update`, `kb.py`, `orchestrator.py`, `chapter_flow.py` and `pipeline3.py` are **not run**. Ledger updates are made by hand, or by a free script editing `book_ledger.md` and `book_ledger.json`.
2. **Sequence for each chapter:**
   1. read this plan's unit;
   2. print the quotations of every E and C item (`python -I -X utf8 drafting/_tools/quotes.py ID …`);
   3. write `drafting/run/chN/N.x.md` section by section, in order, each with the previous section's full text to hand;
   4. after each section, run the free checks (`UDAY_CFG=<cfg> python -I -X utf8 drafting/_pipe/inhouse.py check N.x`) and fix every "problem";
   5. after the chapter, run `build_outputs.py`, extended to the new chapter's cfg.

   Each new chapter needs a cfg (`drafting/chNN/cfg_chNNv1.py`, modelled on `ch03/cfg_ch03v2.py`) and an evidence pack built from this plan's IDs. Build the pack with `_pipe/extend_pack.py` from the evidence log, adding kb-new items from `evidence_index/kb_new.jsonl`.
3. **In-session verification** (replaces independent verification):
   - check every factual sentence against the quotations of the IDs it cites (the quotation, not a gloss);
   - match every quotation character for character against the source file in `Udaipur Books Markdown files\` (grep the exact string);
   - log anything unverifiable in the chapter report as a flag, never smoothed over;
   - re-read each paragraph after any cut (dangling "there", "its");
   - protect decimals ("1,229.9").
4. **Labelling:** every chapter report, `.docx` subtitle and progress entry states **"Facts verified in-session, not by an independent model"**, so the user can choose chapters for a later second check.
5. **Gap-filling:** free local search (grep or BM25 over the corpus Markdown) only. Each new item is sliced verbatim by `_tools/kb_new.py`, with its page from the marker in force, tagged `kb-new` with its tier. Gap-filling is used only where a section would otherwise land below 70% of its target, or where a flag names a gap the corpus can fill.
6. **Default rules for soft choices** (master outline P0):
   - items marked optional or "evidence pass" are omitted unless the section would land below 70%;
   - the first alternative wording is used;
   - "Note:" items never enter the running text.
7. **What needs the user:** any structural change (adding, removing, merging or reordering sections or chapters; moving evidence between chapters beyond this plan); any conflict this plan keeps open; anything touching the legal-review flags.
8. **Organizational changes to preserve:** master outline P10, plus this plan's:
   - the Ch 10 opening (V.S. 1220);
   - the Ch 8 opening (the gift);
   - 7.1 P3a;
   - the U2–U4 lengths;
   - the U6 instruction in 4.4 P2;
   - U7 in Chs 11–12.

# Global Evidence / Research Flags (updated)

**Needs the user's ruling:**
- **R1. Gazetteer share in 10.5** (Revenue, brass and the railway, 1720–1905): 27 of 42 cited items are from the 1979 Gazetteer (64%), above the 40% cap. For the district under Maratha and Gwalior rule, the corpus holds almost nothing else.
  - The plan already moved seven Gazetteer items to Chs 11–12 and added four Patil items (kb-new).
  - Options:
    - (a) accept the exception for 10.5;
    - (b) cut 10.5 to about 600 words, keeping P2 (the brass cover) and P5 (the verdict) at full length and compressing P1, P3 and P4;
    - (c) add the staged colonial sources after ingest.
  - Default if no ruling: (a), with the Gazetteer named in the notes only.

**Blocking checks:**
- **B1. The brass cover, V.S. 1841** (≈ 1784–85; sources say 1775). Must be checked before 10.5 is drafted (ROADMAP 14).
- **B2. The GEOHER survey's date.** Must be found before 12.1 and AW.1 state the evidence horizon.

**Legal review before publication (U7):**
- 11.4 (the 2021 eviction order and signboard: no names);
- 11.5 (illegal mining as a threat);
- 12.2 (Tiwari's mining-network allegation: one attributed sentence, no one accused named);
- 10.4 (the farman claim: claimants unnamed);
- any Afterword recall of these.

**Page-image checks (consolidated):**
- **Ch 4:** C04-CII-082 vs pp. 152/178; the "1513" / V.S. 1562 records; C04-GANGULY-101.
- **Ch 5:** C05-INTACH-002 (never used); the Amareśvara date.
- **Ch 6:** C06-JAGTA-EN-035 (gaḍh/gadya); C06-GANGULY-032 (V.S. 1366).
- **Ch 7:** INTACH pp. 54 and 58; C07-GAZ-004 and -007 (excluded).
- **Ch 8:** C08-GANGULY-016 in CII; C08-GAZ-014's source.
- **Ch 9:** Adhikari's footnote (C09-PARTEMPLES-001).
- **Ch 10:** C06-GANGULY-030.
- **Ch 11:** the Gwalior report years; the Land Revenue Code; GEOHER-008's site.
- **Ch 12:** GAZ p. 348 (1901); Tiwari pp. 161–170, p. 70, ≈ p. 63; the 1968 table.

**Staged public-domain sources** (leads only, `ocr_verify`; not evidence until hand-corrected and ingested):
- Bühler, *EI* I (Chs 4, 6);
- Beglar, ASR VII (Chs 5, 7, 11);
- Cunningham, ASR X (Chs 5, 6, 10, 11);
- the Gwalior report of 1925–26 (Ch 11).

**Research leads:** ASR IX p. 109, a V.S. 1137 inscription of Udayāditya of unstated provenance (Chs 4, 6). It is not evidence.

**Gaps to state in the text, not fill:** see master outline Part V.4, unchanged.

**Verification method:** all chapters from Ch 4 are verified in-session, not by an independent model. A later second check may be wanted for Ch 4 (dates, the three enemies), Ch 6 (readings) and Ch 10 (sequence).

# Continuity and Duplication Checklist (updated)

*Use the master outline's Part VI for every section, chapter and book-wide check. Add these:*

- [ ] **Per section:**
  - every cited ID's quotation has been printed and read (`quotes.py`);
  - every quotation has been matched verbatim against its source file;
  - the unverifiable items are logged.
- [ ] **Per section:** no item cited as E here is E in another unit (the home rule). Cross-references are a clause.
- [ ] **Per section:** the Gazetteer is ≤ 40% of cited items, or the section is 10.5 under the user's ruling R1.
- [ ] **Per chapter:**
  - the report carries the line "Facts verified in-session, not by an independent model";
  - the legal-review passages (Chs 10–12) are listed;
  - no API call was made.
- [ ] **Per chapter:** kb-new items, if any, are listed with source file, line, page marker and tier.
- [ ] **Book-wide after Ch 10:** Ch 1 §1.2/§1.3 (Caulukya governors, U1) and 10.1 agree in wording.
- [ ] **Book-wide:** run `plan_qc.py` again if the plan changes; the status table must stay green.
