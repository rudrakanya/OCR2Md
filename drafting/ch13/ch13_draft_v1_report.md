# Afterword, draft v1: Conserving Udaypur: Community, Heritage and the Future (21 October 2026)

Drafted in-session from the contents file (`editorial/Udaypur_Book_Contents.md`, Afterword: 12 units). No API calls, Chroma queries or paid ledger runs were used. Verification was done in-session: every quotation was checked by script against its cited items, and every claim against the items it cites. It was not checked by an independent model.

## 0. State before work

- **No Afterword draft existed.** There was no `ch13/` folder, plan, cfg, pack or draft, and no `run/ch13/` sections. The only Afterword material was the 13 October evidence map (`drafting/ch13_afterword.md`, 11,514 words) and its index (`evidence_index/ch13.jsonl`: 67 items, 58 direct and 9 contextual).
- **Contents file:** 12 units, from 1 (Where the Record Stops) to 12 (Conservation by Use).
- **Plans:**
  - The v2 master outline and the whole-book outline give 6 sections (AW.1–AW.6) and a 2,750-word target (U2). Their item map, their opening (the 2019 letter) and their closing (the village under the temple) were carried over the 12 units. No unit was added, dropped, split or merged.
  - The v2 exclusions were honoured: EN-015 has no content; HI-035 and HI-039 are never used as the close.
- **Dependency:** Chapters 10–12 were not drafted when work began.
  - Parallel sessions delivered Ch 11 v1 and Ch 12 v1 during drafting. Every recall was then checked against them; see §5.
  - Ch 10 v1 was delivered later the same day; the Afterword makes no Ch 10 callback, so nothing depends on it.

## Files

| Item | Path |
|---|---|
| Plan | `ch13/ch13_plan_v1.md` |
| cfg | `ch13/cfg_ch13v1.py`: NO_LENGTH, CONSOLIDATE_NOTES, `CHAPTER_LABEL = "AFTERWORD"`, `NUMBERED_HEADINGS = False`. The extra rules are listed under §4 Checks. |
| Pack | `ch13/evidence_pack_v1.json`: 130 items, the index plus every cited cross-reference |
| Sections | `run/ch13/13.1–13.12.md` (numbered 13.N for the tools; the .docx prints them unnumbered) |
| Working draft (IDs kept) | `ch13/ch13_draft_v1.md` |
| Footnoted | `ch13/ch13_draft_v1_footnoted.md` |
| Word | `ch13/Afterword - Conserving Udaypur - Draft v1.docx` |
| Ledger | `run/ledger/ledger_ch13.json`, merged; the header now ends "…Chapter 12 (v1) and the Afterword (v1)" |

**New corpus items** (`_tools/kb_new.py`):
- C13-KBN-GEOHER-001: the survey's references, consulted 4 April 2021, which date the survey.
- C13-KBN-JAGTA-EN-001: the abandoned palace, "let it survive at its own peril…".

**Shared tools changed** (minimal, backward-compatible edits; other sessions were editing them at the same time):
- `_tools/stitch.py` and `_pipe/build_outputs.py`: entry 13 added.
- `_pipe/make_docx.py`: optional `CHAPTER_LABEL` and `NUMBERED_HEADINGS` settings, which default to the old behaviour.
- `_pipe/ledger.py`: header text.

## 1. Units

| Unit | Body words | Items cited | Afterword index items | Notes |
|---|---|---|---|---|
| 1 Where the record stops | 380 | 15 | 9 | 3 |
| 2 Agencies, owners and coordination | 242 | 15 | 4 | 2 |
| 3 Translating the inscriptions on site | 248 | 14 | 7 | 2 |
| 4 Guides, signs and heritage walks | 203 | 7 | 7 | 2 |
| 5 Clearing, excavating and recording | 277 | 13 | 7 | 2 |
| 6 Schools and the next generation | 240 | 10 | 8 | 2 |
| 7 Residents and citizens as keepers | 296 | 14 | 7 | 2 |
| 8 Professionals and researchers | 250 | 16 | 4 | 2 |
| 9 Tourism circuits and partnerships | 285 | 13 | 6 | 2 |
| 10 A heritage town | 197 | 8 | 5 | 2 |
| 11 Testing the proposals | 269 | 18 | 7 | 2 |
| 12 Conservation by use | 360 | 21 | 3 | 3 |
| **Total** | **3,247** | **125 distinct** | **62 of 67 (55 of 58 direct)** | **26** |

**Length.** The body is 3,247 words against the outline's 2,750 (118%). It follows the evidence: twelve contents units, each carrying proposals with their attributions and the book's own tests.
- Nothing was padded. The line edit cut, it did not add: the mosque detail repeated from Ch 12's close, a doubled "2021" and one unsupported clause.
- If the user holds the Afterword to 2,750, the candidates for compression are 13.9 P2 and 13.6 P2.

**Items cited, by chapter:** Ch 1: 11; Ch 2: 1; Ch 5: 1; Ch 6: 9; Ch 7: 8; Ch 8: 3; Ch 9: 3; Ch 11: 14; Ch 12: 11; Afterword: 64, of which 2 are new.

**Afterword items not used (5):**
- C13-JAGTA-EN-015: INTACH's introduction at the Bhopal presentation; no content.
- C13-JAGTA-HI-016: the princely states of Madhya Pradesh in general; outside Udaypur.
- C13-JAGTA-HI-026: the "job of a week" for volunteers, already carried by the clearing proposals of 13.5.
- C13-JAGTA-HI-035 and HI-039: exhortations ("resolve"); per the v2 rule, never used as the close.

## 2. The reflective register stays within the book's history

- **No new historical facts.** Every factual sentence carries IDs. The reflection uses only:
  - the Afterword's own items, which are the proposals;
  - Ch 11–12 items, recalled in a clause and checked against their v1 texts;
  - callbacks to Chs 1–9, which carry the IDs those chapters cite.
  The two new corpus items date the survey and describe the palace's condition; neither is a historical event.
- **What the reflections rest on:**
  - **13.3:** "the founder, its firmest date, its Caulukya and Paramāra masters and its pilgrims are all known first from these stones". Sources: C01-MADHYABHARAT-001, C06-CII-006, C08-CII-020, C06-GEOHER-008.
  - **13.8:** the research agenda is the book's own open questions, taken from the ledger, with chapter pointers.
  - **13.11:** the four tests come from the record:
    - the lane (12.8), with the officials' share acknowledged;
    - the kiosks and the 2021 order;
    - the damage on unprotected sites;
    - the monsoon urgency;
    - the shortage of readers.
  - **13.12:** the argument rests on the 1229 gift, the 1775 brass cover, daily *pūjā*, the inscriptions to V.S. 1985, the pilgrims of V.S. 1696, houses of reused stone, the nameless hill wall and the abandoned palace. It is calibrated against the costs of use: broken door figures and reused stone.
- **No invented futures.** Proposals are given in their authors' conditional ("would", "should"). A cfg rule fails any narrator sentence that predicts with "will become / will bring…". The narrator states only that "the record holds none with a budget or a timetable".
- **No motives attributed** to living people or institutions. Criticism of panchayats, departments and the district association is attributed and paraphrased, and names no one.

## 3. Passages flagged for legal review

| Unit | Matter | Treatment |
|---|---|---|
| 1, para. 2; 11, para. 1 | Revenue order of 15 January 2021 on the palace land (LR-1) | Administration only, in one clause; no party named; the claimant on the order and the signboard is never named |
| 2, para. 1 | The palace's status ("protected by no one") (LR-1) | Recalled from 11.3; marked as contested |
| 5, para. 2 | Illegal quarrying along the hill walls (LR-2, U7) | One sentence, attributed to the Geo-Heritage survey; no one named |
| 7, para. 1 | Panchayats reproached for unconcern; Upadhyay's judgement that residents keep a distance | Attributed opinions, paraphrased; no person or panchayat named |
| 7, para. 2 | Residents' and citizens' acts (lane, encroachments) | Described by group and act; the named citizens of Tiwari pp. 63–70 and 165 are not named (cfg rule) |
| 8, para. 1 | The district archaeology association "with no outcome anyone could report"; the departments' "stagnant minds" | Paraphrased neutrally, attributed to Tiwari, no one named |
| 10, para. 2 | Removal of "illegal kiosks" | The quotation is attributed; whose kiosks they were is stated as unknown, and no one is named |

## 4. Checks

- **Quotations:** 15 in the body, all found verbatim in their cited items (script check). At most two per unit.
- **`inhouse.py check`:** 8 of 12 units are clean. Four flags are accepted:
  - 13.1, the 2019 letter: the writer's own dated act, which the outline asks for (AW.1 P1).
  - 13.1, 20 February 2022: the printed date of a guest post, which is metadata, not testimony about a past event.
  - 13.11, "On the evidence of this book": the single test label the outline asks for.
  - 13.12, "This book argues": the single argument label the outline asks for.
- **`ch_rules.py`:** 0 failures. The rules cover:
  - HELD on every Ch 10–12 cross-reference;
  - no quoting of JAGTA-HI glosses;
  - living persons named (residents, claimants, the ASI official, the ground reporter);
  - the U7 mining attribution;
  - narrator predictions;
  - anonymous labour;
  - canon R2 and R3;
  - Temple Economics.
- **`prose_checks.py`:** no passive runs, narrator period terms or agent-noun problems; dynasty spelling clean; colon reveals 1.5 per 1,000 words.
- **Stitch:** `stitch.py 13 --check` reports equal.
- **Outputs:**
  - The footnoted text has 26 notes, one per paragraph.
  - The .docx has the AFTERWORD label, 12 unnumbered headings and 26 Word footnotes, each ending in its evidence IDs.
  - It ends on the book's last sentence ("…the temple keeps its morning and evening worship."). Nothing is empty or truncated.
  - The 10 bibliography entries are flagged incomplete by `footnote.py` (`…bibliography_todo.json`), as in Chs 9 and 12. This is a standing registry gap.

## 5. Corrections made after the parallel Ch 11–12 drafts appeared

- **RR-30 is resolved.** The Ch 12 plan identifies the guest voices from their bylines (C12-KBN-JAGTA-EN-004/-005):
  - pp. 161–162 are Shivkumar Vivek's post of 20 February 2022;
  - pp. 163–167 are Ajit Vadnerkar's post;
  - p. 170 is Tiwari's own closing.
  Every attribution was corrected: the Mishra plan (Vivek); the merchants, the first steps, the circuit and the PPP model, and the kiosks (Vadnerkar); "the historian's last dream" (Tiwari).
- **The horizon moved.** The latest dated item is Vivek's post (20 February 2022), not the survey, which is 2021 or later (RR-31 stays open).
- **The lane is dated** "early in the year" 2021, after Ch 12 v1 (C12-KBN-JAGTA-EN-003).
- **The protection map** adds the Barakhambi (ASI) and the Forest Department's Jain cave, after 11.3.
- **The close changed.** Ch 12 now ends on the 1979 verdict and the "sleeping village". The Afterword therefore ends on the approach of 1.1 (the temple seen before the houses) and the lane its residents widened, so the two endings do not repeat each other.

**For the user (other chapters; not changed here):**
- Ch 11's ledger lists Suresh Mishra as "living; legal review list", but his death is recorded (C13-JAGTA-EN-013; Tiwari's book, ≈ pp. 167–168).
- The Ch 12 plan reports that §1.1's "cannot even be called a town (*kasba*) today" (C01-JAGTA-EN-015, p. 163) is Vadnerkar's words, not Tiwari's.

## 6. The through-line is completed, not summarised

The Afterword does not recap chapters. It takes up the one movement the book has traced:
- a king's town, read through its stones, its gifts, its reuse and its decline;
- then a village visited as a monument (Ch 12's close);
- then the question of what the meaning of the place now asks for.

Callbacks are single clauses with pointers, each used to argue: the inscriptions (13.3), the open questions (13.8), survival by use and its costs (13.12). The ending returns to the book's first image, the temple seen from the road before the houses (1.1).

## 7. A few quotations with IDs

- "the history that had survived alive in this town" (C13-JAGTA-EN-001)
- "people come; they take *darshan*; they wander about a little; and, without any information, they simply drift off into the void." (C13-JAGTA-EN-008)
- "The tourists will not start coming in from day one." (C13-GEOHER-005)
- "Causes of problems must first be understood and treated before obvious effects are remedied." (C11-GEOHER-011)
- "Our ancestors could not save the Vijay Mandir; let us at least save Udaipur." (C13-JAGTA-EN-022)
- "let it survive at its own peril, let it fall at its own peril" (C13-KBN-JAGTA-EN-001)

## 8. Editorial read (14 questions)

1. **Concrete openings:** a letter to a Collector; buildings and their holders; six lines of 1080; visitors who leave; rubble and a mound; schoolchildren; calls against acts; readers wanted; a circuit; a historian's sentence; who pays; what lasted.
2. **One argument per unit:** yes. The book's own argument is made once, in 13.12.
3. **Place and proposals as subjects; attributions in notes:** yes. Two labels are accepted.
4. **Calibrated verbs:** proposals use "would" and "should"; "could give it a date"; "2021 or later".
5. **Conflicts side by side:** Upadhyay's verdict on residents is set against the residents' recorded acts (13.7).
6. **Testimony marked:** Tiwari, Vivek and Vadnerkar are identified in the notes. No counts or widths are taken from testimony.
7. **Restraint:** no exhortation, no rhetorical question, no superlatives in the narrator's voice.
8. **No invented actors or futures:** confirmed by cfg rule and by reading.
9. **Tradition as memory:** 13.6 sets memory against record.
10. **Boundaries:** the present state belongs to Ch 12 and administrative history to Ch 11; both are recalled in clauses only.
11. **Repetition:** no quotation from an earlier chapter is reused. "Famine of experts" (6.22) and "positive and inspiring" (12.8) are paraphrased.
12. **Opening from Ch 12:** Ch 12 ends "What should be done with it is the Afterword's"; the Afterword opens on the earliest dated proposal.
13. **Close:** the book ends on the temple seen from the road and its worship at the top of the lane.
14. **Notes:** 26, one per paragraph, each with its IDs.

## 9. Open

- RR-31: the survey's own date.
- LR-1 and LR-2: legal review, together with the Ch 11–12 review.
- HELD notes: re-check against Ch 11 and Ch 12 once those chapters are final.
- Bibliography entries to complete in the citation registry.
