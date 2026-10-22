# Chapter 10, draft v1: Political Change and Economic Decline (21 October 2026)

I drafted this chapter in-session from the contents file (`editorial/Udaypur_Book_Contents.md`, Chapter 10, 12 units). I used no API calls, Chroma queries or paid ledger runs. **I verified it in-session; no independent model has checked it.**

## 0. Dependency: the V.S. 1841 brass-cover check

- **Status: OPEN.** RR-2 is still open in the Research Register of both the v2 master outline and the item-level whole-book outline. It asks for the inscription or a reliable edition.
- **Path taken: HELD.** Unit 10.9 gives the date only as the sources give it:
  - V.S. 1841 as reported from the inscription, rendered by the same report (Patil) as A.D. 1775;
  - 1775 in Pande and the Gazetteer.
- **The two figures are set side by side.** By the reckoning the Udaypur records themselves follow (V.S. 1220 = 1163, V.S. 1320 = 1263), the two figures are nine years too far apart. The text also notes that 1775 is the year by which, in the Gazetteer, Vidisha had come into Scindia's hands.
- **Nothing is settled.** The paragraph's note is marked `HELD (RR-2)`. A cfg rule fails any sentence that gives 1841 or 1784 without a hedge. The usual conversion (about 1784–85) is not printed, because no evidence item states it; it stays in the Register.
- **Other held items, recalled from Chapter 6:** the Sam. 1366 record (RR-11) in 10.3 and the V.S. 1311 record (RR-23) in 10.2. The farman's original (RR-22) is recorded in 10.6.

## 1. State before work

- **No Chapter 10 material existed.** There was no `ch10/` folder, plan, cfg, pack or draft, and no `run/ch10/` sections.
- **Contents file:** 12 units, from 10.1 (the Caulukya seat, c. 1093–1190) to 10.12 (what decline means).
- **v2 master outline:** six sections and a 4,200-word target, which NO_LENGTH supersedes. Its item assignments, its opening ruling (open on the V.S. 1220 Kumārapāla record) and its closing (the Gazetteer's sentence) were redistributed over the 12 units. No unit was added, dropped, split or merged.
- **Evidence:** `evidence_index/ch10.jsonl` holds 176 items, 61 direct and 115 contextual. The later-Paramāra items are homed here by `chapters.md` (Chapter 4's unused S6 items).
- **Neighbouring chapters:** Ch 9 v1 and Ch 11 v1 had been drafted by other sessions. 10.1 opens from 9.9's close, and 10.12 hands over to 11.1's opening ("The town the officials described as once important…").

## Files

| Item | Path |
|---|---|
| Plan | `ch10/ch10_plan_v1.md` |
| cfg | `ch10/cfg_ch10v1.py`: NO_LENGTH; GAZ_MAX_SHARE 0.40 |
| Pack | `ch10/evidence_pack_v1.json` (341 items) |
| Sections | `run/ch10/10.1–10.12.md` |
| Working draft (per-claim IDs) | `ch10/ch10_draft_v1.md` |
| Footnoted | `ch10/ch10_draft_v1_footnoted.md` (39 notes) |
| Word | `ch10/Chapter 10 - Political Change and Economic Decline - Draft v1.docx` (39 Word footnotes) |
| Ledger | `run/ledger/ledger_ch10.json`, merged |

**The cfg's extra rules fail:**

- R2, R3 and R4 (*mahādvādaśaka*, Bhṛṅgārikā and *mahāsādhanika* must carry their record's date);
- U1 (twelfth-century governors must be framed as Caulukya);
- an unhedged brass-cover date;
- any Temple Economics citation;
- narrator "Mohammedan", "Muhammadan" or "Moslem";
- soldiers, raiders, priests or villagers in a sentence with no IDs.

**The pack** is:

- the index less its 8 Temple Economics items;
- the later-Paramāra items of Chapter 4;
- recall items from Chapters 1, 3, 5, 6, 7, 8, 9 and 12;
- 10 kb-new items. Four already existed (C10-KBN-MADHYABHARAT-001 to -004). I sliced six new ones verbatim with `_tools/kb_new.py`: C10-KBN-MADHYABHARAT-005 to -009 (Patil on Gujarat's hold to 1534, Aurangzeb's death in the Deccan, the Madhya Bharat union, the Maratha and Muslim-ruled states, and British interference after Mahadji) and C10-KBN-JAGTA-EN-001 (Tiwari's guess of commercial buildings).

**Tools touched:** `_tools/stitch.py` and `_pipe/build_outputs.py` register Ch 10, and the merge header in `_pipe/ledger.py` now includes Chapter 10.

## Units

Words are body words, without notes or IDs. Items are distinct IDs cited in the unit. The Gazetteer share is the share of a unit's distinct cited items that come from the 1979 Gazetteer (cap 40%).

| Unit | Words | Items | Gazetteer share |
|---|---|---|---|
| 10.1 A Caulukya seat on the eastern frontier, c. 1093–1190 | 815 | 41 | 2 of 41 (5%) |
| 10.2 Devapāla's line and the Delhi raids, c. 1190–1305 | 812 | 40 | 3 of 40 (8%) |
| 10.3 Udaypur after 1305 | 629 | 18 | 2 of 18 (11%) |
| 10.4 Temples turned to mosques across Malwa | 504 | 21 | 3 of 21 (14%) |
| 10.5 Bhilsa under the Malwa sultans, 1401–1562 | 497 | 20 | 7 of 20 (35%) |
| 10.6 A qasba of Sarkar Chanderi | 603 | 19 | 5 of 19 (26%) |
| 10.7 Aurangzeb at Bhilsa, and at Udaypur in legend | 400 | 11 | 4 of 11 (36%) |
| 10.8 Afghans, nawabs and Marathas, 1708–1775 | 449 | 11 | 4 of 11 (36%) |
| 10.9 The brass cover of the liṅga *(HELD, RR-2)* | 283 | 10 | 2 of 10 (20%) |
| 10.10 Bhilsa district in Gwalior State and after, 1827–1956 | 439 | 11 | 4 of 11 (36%) |
| 10.11 Famine, the railway and a feeder road | 327 | 8 | 3 of 8 (38%) |
| 10.12 What decline means | 549 | 24 | 4 of 24 (17%) |
| **Total** | **6,307** | **197 distinct** | every unit ≤ 40% |

**Coverage:** 99 of the 176 index items are cited, including 36 of the 61 direct items. Length follows the evidence. The two later-Paramāra units are the longest because CII carries them. 10.7–10.11 are short because the regional record barely names Udaypur, and none of them was padded.

## Gazetteer handling

- **10.5, 10.8, 10.10 and 10.11 were Gazetteer-heavy in the v2 assignments.** In the v2 plan §10.5 alone drew 27 of its 42 items from the Gazetteer.
- **Each was brought under 40%** in two ways:
  - Patil (Madhya Bharat), Tiwari, Chapter 1's Patil and Tiwari railway items, and Chapter 3's route items were added for the same facts;
  - Gazetteer-only detail was cut: the Bhopal–Maratha back-and-forth of 1745–61, the Shujaat Khan and Puranmal grants, the education conjecture, the duplicate subah and kamasdar description, and the 1858–59 fighting, which v2 moves to Ch 11.
- **The Gazetteer is named as the source wherever a stretch rests on it.** The text says so directly ("As the Gazetteer tells it", "These are the Gazetteer's descriptions of the state's whole machine") or in the unit's note.
- **10.11's famine paragraph rests on one Gazetteer item** (itself quoting an older report). It is kept to four sentences and says outright that Udaypur is not named.

## Decline shown, not asserted

- **Political demotion is shown as a dated ladder,** with an ID on every rung (10.12 P1):
  - 1163: Caulukya governor's headquarters (U1);
  - 1232: a Paramāra king residing at Udayapura;
  - Sam. 1366: the last Paramāra title in the porch;
  - 1336–38: the sultan's mosque in the temple court;
  - 1488: a mosque built by an agent of a lord;
  - 1632: the Shahi Masjid and probably a governor's house, in a town of Sarkar Chanderi;
  - the Scindia general's brass, date HELD;
  - 1905: the end of a feeder road;
  - the Gazetteer's "large village in Basoda Tahsil".
- **Economic decline is kept separate,** and the text says it cannot be dated:
  - no population, revenue or trade figure for Udaypur survives from before the twentieth century, and the Mughal accounts name Bhilsa's *maḥal*, not the town;
  - what survives is ruin (Sharma), visitors' guesses and estimates (Tiwari), village memory (Daulatpur, 9.9), and two general models that the text says are not evidence for Udaypur (Adhikari; Hardy's summary of the feudalism model).
- **The famine and the railway are dated district events.** For each, the text says it does not name Udaypur and that "whether there was trade there to lose, no record says".
- **The temple's survival is treated as a separate question (10.4).** The record shows that the temples that fell stood in the new rulers' seats (Bhilsa, Dhār, Mandu). Linking this to Udaypur's lost rank is offered once, as a possibility and not a finding, with Hardy's reading attributed in the note.

## Canon, tiers and boundaries

- **U1:** the twelfth century is Caulukya overlordship at Udaypur: the V.S. 1220 stone, Rājyapāla, Lūṇapasāka under Ajayapāla, and the return under Vindhyavarman "not recorded" for Udaypur. This is consistent with 1.8, 6.18 and 8.1.
- **R1 and R3, records kept separate:**
  - the 1163 Ganguly notice and the V.S. 1220 fragment;
  - the V.S. 1562 record, the sixteenth-century pedigree and the inscription praising the temple;
  - the two governors' records.
- **R2:** no Karṇa appears.
- **R4:** *mahādvādaśaka*, Bhṛṅgārikā and *mahāsādhanika* are each tied to their dated record. No record of the period calls Udaypur a *qasba*. The contents title keeps the word, and the 10.6 note says it is the modern chronicler's term.
- **D1:** IAST dynasty names; `dynasty_spelling` is clean.
- **Period terms:** "Mohammedan" and "Muhammadan" appear only inside verbatim quotations (Beglar via Pande; Patil). The narrator says "Muslim".
- **Tiers:**
  - CII for the inscriptions;
  - the Gazetteer as tier 7 and attributed;
  - Patil and Ganguly as early scholarship, with interpretations attributed ("Ganguly's judgement", "Ganguly's phrase");
  - Tiwari as testimony. The validator's testimony-as-measurement rule moved his figures (1528, 2008, 2021, 1707, 105 *gaz*) into notes.
- **U7:** no claimant or presenter of the farman is named; the 2021 order goes to 11.6.
- **Boundaries:** mosque fabric goes to 7.16–7.18; the palace and mansion to 7.9; foundation and descent to Chapter 4 (4.12, 4.20); Garde and Gwalior archaeology to 11.2; the census to Chapter 12.

## Conflicts set side by side

- the Caulukya conquest, 1138 vs 1145 (range 1138–45);
- Madanavarman's grant, 1133 vs 1134;
- Lūṇapasāka's grant, 1171, 1172 or 1173;
- Ballāla killed by Kumārapāla's army vs by Yaśodhavala;
- Arjunavarman's end: killed by Siṃhaṇa, dead without an heir, or succeeded by a son-in-law;
- Iltutmish at Bhilsa, 1233–34, 1234, 1235 or 1239;
- the Khalji capture of Bhilsa, 1290, 1291 or 1293;
- the corner shrine replaced by the mosque, north-west (Beglar) vs north-east (Ganguly);
- the 1325 legend vs the inscriptions of 1336–38;
- the Vijay Mandir destroyed in the 1230s and again in 1682;
- the height in Minhāj, "5 Gaz" vs 105 *gaz*;
- the founder of the mosque and Mahal Qubba, Auliya Ibn Abdul Samad (farman) vs Jahāngīr (the claimant);
- the brass-cover donor, Khande Rao Appaji vs Bappa Saheb;
- the brass-cover date, V.S. 1841 vs 1775 (HELD).

## A few quotations with IDs

All are verbatim and case-sensitive against their items; the validator checks every one.

- "took away the fortunes of the Mālavas along with those of the Chēdis" (C04-CII-135)
- "at least up to 1157 A.C." (C10-CII-002)
- "by his sword, cut off into two (the body of) the arrogant lord of the Mlechchhas, in a battle fought near Bhillasvāmipura" (C10-CII-007)
- "It is not proved, from an inscription alone, that Mohammad Tughlaq did this or had it done." (C06-JAGTA-EN-037)
- "Udaipur — Sarkar Chanderi, Suba Malwa, the border of Gondwana." (C10-JAGTA-EN-018)
- "the numerous empty houses to be seen in every village and referred to laconically as the results of Chappan ka sal (V. S. 1956)" (C10-GAZ-054)
- "Udayapur, once a place of considerable importance is a large village in Basoda Tahsil." (C10-GAZ-056)

## Direct items set aside (25)

- **Hindi duplicates of English items used (10):** C10-JAGTA-HI-001, -002, -003, -004, -033, -035, -036, -038, -041 and -042.
- **Surmise, polemic or imagined scenes with no record content (7):** C10-JAGTA-HI-006, -007, -020, -024, -028, -029 and -044.
- **The 2021 eviction, the occupiers' departure and an ASI official's view (5), which belong to §11.6:** C10-JAGTA-HI-034, -039 and -040, and C10-JAGTA-EN-020 and -021.
- **Gazetteer items left out (3):**
  - C10-GAZ-037: an education conjecture, off-subject;
  - C10-GAZ-040: administrative divisions, which would push 10.10 over the cap;
  - C10-GAZ-050: duplicates GAZ-051.
- **Temple Economics:** all 8 items are excluded, as in Chapters 3–9.

## Checks

- **Unit checks:** all 12 units are clean under `inhouse.py check` (validator, prose checks and ledger). The only remaining flags are the noisy "figure" review notes, which do not count against cleanliness.
- **Canon rules:** `ch_rules.py` reports 0 failures. During drafting it flagged two U1 false positives, which I fixed by narrowing the rule.
- **Stitch:** `stitch.py 10 --check` reports equal.
- **Gazetteer cap:** every unit is at or under 40% (table above).
- **Outputs:**
  - both the footnoted `.md` and the `.docx` contain all 12 headings;
  - there are 39 notes, one per paragraph, each ending on a complete sentence;
  - the `.docx` has 68 non-empty paragraphs and about 6,570 words, ending on the bibliography.
- **Bibliography:** 12 entries are incomplete in `ch10_draft_v1_footnoted.bibliography_todo.json` (place and publisher gaps from the manifest). This is the same book-wide issue as Chapters 8 and 9.

## Editorial read (14 questions)

1. **Concrete openings:** each unit opens on a stone, a raid, a title in the porch, a temple at Vidisha, a sultan's declaration, Babur at Chanderi, a dated act at Bhilsa, an Afghan's arrival, a brass face, a power changing hands, a famine, or the dated ladder.
2. **One argument per unit:** yes.
3. **Place as subject, sources in notes:** yes. The source-led check passes in every unit, and Udaypur is named in each unit's close.
4. **Calibrated uncertainty:** "may", "probably", "is said", "not recorded" and "no record says", each used once at the point of doubt.
5. **Conflicts side by side:** see the list above.
6. **Testimony marked:** Tiwari is marked as testimony throughout, and his inferences carry "must have" in the notes.
7. **Restraint:** no regime's regional history stands without its Udaypur question. 10.5, 10.8 and 10.10 each say plainly that Udaypur is not named.
8. **Interpretation:** made once, and attributed or labelled as a possibility (10.2 on residence vs capital; 10.4 on survival).
9. **Transitions:** from 9.9 into 10.1, then each unit into the next by date, and from 10.12 into 11.1.
10. **Paragraph shape:** varied; the passive-run checks were cleared by rewriting.
11. **Numbers:** ranges where the sources differ; testimony figures sit in notes.
12. **People act only where named:** Rājyapāla, Lūṇapasāka, Devapāla, Iltutmish, ‘Ain-ul-Mulk, Dilawar Khan, Mahmud Shah, the agent of Sher Khan, Auliya Ibn Abdul Samad, Dost Mohammad, the Pawar brothers, Khande Rao Appaji and Garde. Unnamed actors appear only where an item gives them.
13. **No general knowledge:** the V.S./A.D. offset is derived from the chapter's own records; Ganguly's 1933 date was removed.
14. **Ending:** the Gazetteer's sentence as an official's description, handed to Chapter 11.

## For the user

- **RR-2 (blocking for a settled 10.9):** provide the inscription or a reliable edition of the brass cover. Once it is read, 10.9 P2, the 10.12 ladder rung and §1.9 can be finalised.
- **The title word *qasba* (10.6):** no period record uses it for Udaypur. I kept the contents title and explain this in the note. Confirm, or retitle in `chapters.md`.
- **Udaypur's pre-1948 state (Gwalior's Basoda tahsil vs the Nawab's Basoda):** not stated in the corpus, and left open.
