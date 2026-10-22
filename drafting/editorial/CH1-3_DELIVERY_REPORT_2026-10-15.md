# Chapters 1–3: delivery report

*15 October 2026. This is the credit-limited production. Drafting, revision, fixes, the author's pass, the copyedit and the line edit were done in-session. The OpenAI default model (gpt-6.1-sol) did the judging, the verification, the re-verification and the final reads. Status: `drafting/run/status.md`. State: `drafting/run/inhouse_state.json`. Data: `drafting/run/summary_data.json`.*

## Deliverables

| Item | Path |
|---|---|
| Working drafts (IDs and `{{note}}` blocks) | `drafting/ch01/ch01_draft_v5.md`, `drafting/ch02/ch02_draft_v3.md`, `drafting/ch03/ch03_draft_v2.md` |
| Footnoted versions (Chicago, consolidated notes, hidden IDs) | the same names with the suffix `_footnoted.md` |
| `.docx` (A4, 1-inch margins, Georgia, real footnotes, CHAPTER label, "Draft vN · October 2026", bibliography page, page numbers) | `drafting/ch01/Chapter 1 - Udaypur - Draft v5.docx`; `drafting/ch02/Chapter 2 - The Betwa Valley - Draft v3.docx`; `drafting/ch03/Chapter 3 - Before Udaypur - Draft v2.docx` |
| Combined document | `drafting/Udaypur - Chapters 1-3 - Draft.docx` (88 footnotes, numbered within each chapter; 19 books in one bibliography; 79,873 characters, 8% of the Google Docs limit) |
| Book ledger | `drafting/editorial/book_ledger.md` (from the final texts; the version built from the plans is kept as `book_ledger_from_plans.md`) |
| Style sheet | `drafting/style/style_sheet.md` |

## Gates

- **In-line gate: pass, 4 of 4.** The failures were prose only, and line fixes took all four paragraphs to 14/14:
  - 1.5 P1 had a hardened transition (Q8);
  - 2.1 P5 had two awkward constructions (Q4, Q11);
  - 2.3 P2 repeated a word.
- **Judge's second opinion (before the fixes):** 1.1: 81; 1.5: 84; 2.1: 74; 2.3: 79, out of 110.
- **Final gate, after the line edit: pass, 4 of 4.** The four paragraphs were re-read after every later edit, and all four pass all 14 questions. The last changes were "lean" for a repeated "point" in 1.5 P1, and "their" for "its" in 2.3 P2.

## Per chapter

| | Ch 1 | Ch 2 | Ch 3 |
|---|---|---|---|
| Words, by section | 1.1: 770 · 1.2: 599 · 1.3: 690 · 1.4: 626 · 1.5: 545 | 2.1: 591 · 2.2: 587 · 2.3: 629 · 2.4: 632 · 2.5: **153** | 3.1: **343** · 3.2: 442 · 3.3: 633 · 3.4: 476 · 3.5: 644 |
| Chapter total (validator count) | **3,249** (within 3,200–4,400) | **2,608** (below the floor) | **2,557** (below the floor) |
| Judge (first drafts, out of 110) | 81 · 74 · 69 · 75 · 84 | 74 · 86 · 79 · 71 · 72 | 68 · 78 · 72 · 65 · 75 |
| Verifier on first drafts: supported or sound / all sentences | 21/33 · 24/37 · 30/38 · 25/34 · 20/28 | 19/31 · 20/26 · 22/31 · 25/30 · 6/18 | 11/20 · 16/22 · 23/34 · 23/26 · 23/30 |
| Re-verification of changed sentences, round 1 / round 2 | 18 of 55 / 11 of 68 flagged | 11 of 41 / 7 of 47 flagged | 7 of 36 / 8 of 44 flagged |
| Final independent read: problems listed | 26 | 22 | 25 |
| Notes per paragraph (reader-facing) | 1.0–3.0 | 0.5–2.0 | 1.2–1.5 |
| People as subject | 0–22% | 0–4% | 0–5% |
| AI-shaped prose per 1,000 words | triplets 0.6 · colon reveals 1.5 · final aphorisms 0 | 1.5 · 1.1 · 0.4 | 0.4 · 0.8 · 0.4 |

**Flags handling.** Every flag was fixed in-session except two kinds:
- **Context artefacts:** re-verification sees sentences one at a time, so an inference whose support is in its paragraph comes back "new fact". Examples are 1.4-18, 3.3-14 and 2.4-15.
- **Readings that conflict with the plan:** for example, removing 3.3's "Śaiva images… many centuries before the Paramāras", which is that paragraph's Point.

All fixes went through the validator. No "not X but Y", no "this mattered because", no passive runs and no narrator-term violations remain in any chapter.

## Spend

| | Ch 1 | Ch 2 | Ch 3 | Total |
|---|---|---|---|---|
| Sunk before the credit-limited plan (calibration, retrieval, run 1, run 2 to the freeze) | $4.47 | $3.76 | $2.50 | $10.73 |
| New since the freeze, logged (salvaged drafts, judges, verification, re-verification, final reads, ledger update) | $1.87 | $1.37 | $1.26 | $4.51 |
| Possible unlogged orphans at the freeze (worst case) | $0.12 | $0.92 | $0.07 | $1.11 |
| Log total against budget (incl. sunk) | $6.34 / $9.00 | $5.13 / $8.25 | $3.77 / $8.00 | |

- **Against the $12 cap:** new spend is **$5.62 conservative**, leaving $6.38 of headroom. The last $4 was never approached.
- **Credit remaining:** about **$10.4** of the $16, if every orphan was billed.
- **Never used:** the faster processing tier, the flagship model, and any expansion call after the freeze.

## Wall clock (credit-limited phase)

| Stage | Window | Duration |
|---|---|---|
| Freeze and salvage | 13:27–13:33 | about 6 min |
| Subagent drafting | 13:34–13:45 | about 11 min; the Ch 1 subagent hit its usage limit after drafting 1.5 |
| Judge and verify, as sections became ready | 13:36–14:00 | |
| Fixes | 13:37–14:08 | |
| Gate | 14:10 | |
| Author's pass, copyedit, line edit | 14:10–14:14 | |
| Re-verification | 14:14 | |
| Final reads | 14:15 | |
| Final-read fixes and round-2 re-verification | 14:15–14:21 | |
| Ledger update | 14:17–14:19 | |
| Outputs | 14:20 | |

## Line-edit changelog (summary)

The full record is in `drafting/run/ch*/` (the `pre_finalread/` snapshots), the fix files and this report.

- **Hardened proposals made proposals again:**
  - the bund dating;
  - the erosion sequence;
  - the gullies;
  - "earliest evidence" without a stated region;
  - the 8th–9th-century desertion of Besnagar;
  - the slab "moved" in restoration.
- **Testimony and traditions:**
  - Testimony no longer supplies measurements: Tiwari's 5 km, the fair's "thousands", the inscription counts and "five hundred years" are gone.
  - Testimony is attributed once per paragraph. Tiwari's memory framings are exempted from the source-led check.
  - Traditions are marked as such: Berni Mata "in folklore", "In one legend", and the Haihayas "said to have ruled".
- **Inventions removed:** the arrival sequence in 1.1, "the river itself became a frontier", "the range was crowded with temple towns" and the Chandellas "at the edge of the range".
- **Repetition and endings:**
  - Restated facts and closing aphorisms were cut, in about 30 places.
  - Cross-chapter repetitions were cut or reduced to a clause: the province of Bhilsa, the water tally, the Bhujariya Talab, the Tughluq legend and the crop figures.
  - Digressions were reduced: Lakholi peak, Kaimur/Rewa, the tank list at Dhārā, the forest-produce list and the Bhiraṅgāvalī gloss.
- **Continuity:**
  - Dangling references left by cuts were repaired ("there", "Its colossal statues", "the shaft").
  - A broken sentence in 1.3 ("When Hoshang Shah…") and a tense error were fixed.
  - The Nemawar and roads sentences were moved into the roads paragraph.
  - "Dhār" became "Dhārā" throughout.
- **Damage found and repaired:** a decimal point in "1,229.9 mm" was misread as a full stop, and an inserted sentence split the number. It was repaired, and a scan of all sections confirmed no other split.

## Top open issues

**Chapter 1**
1. **The brass cover's date is unconverted.** The source pairs "V.S. 1841" with 1775, but V.S. 1841 is about 1784–85. The text now gives only V.S. 1841; the inscription or a reliable edition needs checking. The plans say 1775.
2. **The span "1059–1080".** Under the canon "1059" is now presented as a reading ("read as dating the start of the work"); 1.4 shows that only 1080 is firm. The book needs one ruling on how the founding dates are stated.
3. **The settled Vidisha range rests on Tiwari at its upper end.** The 70 km figure comes from Tiwari, which conflicts with the rule that testimony never supplies a measurement (carried from the RCA). Section 1.4's maintenance under "one Garde Sahib" (Tiwari) may also be M. B. Garde; that's a lead, not a fact.

**Chapter 2**
1. **The chapter is 2,608 words, below 3,200.** 2.5 is a 153-word coda because its three assigned items are exhausted once repetition is removed. 2.1–2.4 sit at 70%. The options are to accept a short closing, fold 2.5 into 2.4 (a structural change, which is your decision), or assign more evidence.
2. **The INTACH Geo-Heritage geomorphology items read like borrowed text, and their heights don't agree.** They should be checked against the survey before they are relied on.
3. **Names and attributions:**
   - The streams Kewtan, Keothan, Keotan and Kethan are kept separate, since nothing shows they are one.
   - Tiwari's teak-hill item (C02-JAGTA-HI-001) describes a hill fort 15 km away; the plan should drop it.
   - The BHOJDEV verses are not tied in any item to the *Samarāṅgaṇasūtradhāra*.

**Chapter 3**
1. **The chapter is 2,557 words, below 3,200.** 3.1, at 343 words, is the honest size of the prehistory and names evidence.
2. **Dates and names:** the 608 grant names no king in its own item (Buddharāja appears only in context), and the Lūṇapasāka grant is 1172 in Ganguly but 1173 in CII. The text now says "the early 1170s" in both 1.3 and 3.4.
3. **Badoh:** two items (C03-KB-MADHYABHARAT-004 and -005) tie the Gadarmal phases and the Daśāvatāra group to Badoh only through their context excerpts. 3.2 is at 38% Gazetteer, close to the cap.

**All chapters:** the bibliography data is incomplete; most books lack place and publisher in the manifest (`*_footnoted.bibliography_todo.json`). This is for you or the title pages; nothing has been invented.
