# Round 4b: production edit pass and verifier fix round on the four calibration sections

*14–15 October 2026. Drafts, edit raw output, verifier results, judge reading and consolidated footnoted versions: `drafting/editorial/round4b/`. Logs: `round4b_ch01.log`, `round4b_ch02.log`. Runner: `_pipe/calib4b.py`.*

## Verdict: stop. Chapters 1 and 2 are not launched.

None of the four paragraphs passes all 14 questions (round 4: 0 of 4; round 4b: 0 of 4). Your rule was to launch on 3 of 4 plus editorial judgement, so production has not started. Two paragraphs improved, one stayed the same, and one is slightly worse.

| Paragraph | Round 4 | Round 4b | Fails in 4b |
|---|---|---|---|
| 1.1 P1, the approach | 12/14 | 12/14 | **Q4/Q11:** "a landmark in Vijay Manohar Tiwari's testimony, *Jagta Hua Kasba*" is an awkward appositive. **Q14:** "Hindu and Mohammedan monuments" is still there, because the edit pass that removed it was discarded (see below). The Q6 misreading is fixed: "roughly ten kilometres before Udaypur". |
| 1.5 P1, the case for an older place | 12/14 | 13/14 | **Q11:** four proposals in a row with the same passive shape ("has been assigned… may belong… are provisionally assigned… have also been read"). The trailing "They leave open…" sentence is gone. |
| 2.1 P5, water held in the hollows | 10/14 | 11/14 | **Q1/Q5:** the paragraph stops on "The hollows collect water; the wider Betwa basin is mostly dry outside the southwest monsoon" without completing the Point (water held from one monsoon to the next). **Q6:** "mostly dry" goes beyond the source, which says about 80% of runoff falls in the monsoon; the re-verifier accepted it. **Q4:** abrupt clipped ending. "More dependable" and "share more than a boundary" are fixed. |
| 2.3 P2, the seam of stone | 12/14 | 13/14 | **Q9:** the Kaimur/Rewa sentence is still there, shortened. The temple's stone is now passive, as your new rule asks ("quarried in a nearby hill"); the compatibility disclaimer is gone; and Patil's explanation is attributed in a note. |

**Beyond the four paragraphs, the host sections are not ready either:**
- **1.1:**
  - a signpost ("What needs explaining is the scale of the older town…");
  - a closing disclaimer in P4;
  - an overreaching last sentence.
- **1.5:** a restated conditional ("He would have appropriated or reorganised…").
- **2.1:**
  - a method sentence ("These figures are used here to describe the modern regime, not to reconstruct…");
  - aphorisms ("Proximity alone leaves the essential problem unresolved");
  - **invented quarrymen** ("even as quarrymen extracted it widely"). This breaks your new people rule. The verifier flagged it as fiction, but the fix was rejected.
- **2.3:**
  - "This is a proposed sequence, not an established history of every hill";
  - a dangling last sentence;
  - **597 words, 66% of target**, below your 70% floor.

## What happened, step by step

| Section | Edit pass | Verifier flags → after the fix round | Judge (4b vs 4, out of 70) |
|---|---|---|---|
| 1.1 | **discarded** (new source-led sentence, subject check) | 6 → 1 | 45 vs 47 |
| 1.5 | kept | 2 → 2 (both fixes lost; see faults 1 and 4) | 59 vs 58 |
| 2.1 | **discarded** (two false positives plus length) | 7 → 1 (the quarrymen fix rejected) | 48 vs 47 |
| 2.3 | kept | 3 → 1 (one fix lost; see fault 1) | 54 vs 44 |

The fix round did what it was designed to do wherever its fixes could land. It corrected the 1.1 misreading, the Beglar tense, the 2.1 partial facts and the 2.3 attribution. **The failures come mostly from pipeline faults that stopped good edits and fixes from landing, not from the writer.**

## Pipeline faults found and fixed in code (no API spend)

1. **Fixes lost to "text not found"** (1.5-15, 2.3-18).
   - **Cause:** the sentence splitter did not split after a note placeholder. "…[ID] {{note}} Next sentence" became one row, and once the note was stripped that text no longer existed in the draft.
   - **Fix:** split at the placeholder (`pipeline3.rows_of`).
   - **Test:** on all four 4b drafts, rows not found went from 1 to 0 in 1.5 and in 2.3.
2. **Whole edit passes discarded over one or two new problems** (1.1, 2.1).
   - **Fix:** before discarding, `edit_gate` makes one targeted repair call, listing only the problems the edit introduced and quoting the previous version so cut material can be restored. The gate is as strict as before.
   - **Cost:** about $0.03 a call, only when an edit fails.
   - **Test:** offline, on 2.1.
3. **Two false positives in our checks** (both behind the 2.1 rejection):
   - "after 96 km it enters Vidisha district", the Betwa's course, was read as narrowing the Udaypur–Vidisha range. The range check now requires the sentence to be about Udaypur.
   - "Betwa-fed" was read as an unknown name "fed". The name check now ignores the lower-case half of a compound.
   - **Test:** both fixed; the real case is still caught.
4. **The length floor reverted a cut of a repeated sentence** (1.5-18: 495 → 481 words, under 490).
   - **Fix:** the fix round's gate ignores length; the edit pass manages length.
5. **Method narration not detected.**
   - **Fix:** the meta check now catches "used here", "not to reconstruct", "not an established", "should not be confused", "cannot safely be", "what needs explaining" and "is a proposed sequence/model/reading". These are now problems the edit and fix passes must clear.
   - **Test:** it catches all four sentences of this kind in the 4b drafts and nothing else.

Faults 1, 2, 4 and 5 also apply to production. Production would have had the same losses.

## What the code fixes do not touch

Two weaknesses are about prose, not the pipeline:
- **Sections come in short.** The writer lands at 67–79% of target, and every edit shortens. Under the 70% floor that you approved, 2.3 now fails on length.
- **Some aphorisms and clipped endings survive both judge and verifier**, for example 2.1's last sentence.

## Cost

- **Round 4b:** $0.98 (Ch1 $0.51, Ch2 $0.47; 19 calls). My earlier estimate was $0.40–0.60; the difference is the fresh judge reading and the fix and re-verify calls.
- **Spend recorded in each log:** Ch1 $1.46 of $8.50; Ch2 $1.18 of $8.25.

## Metrics, round 4 → 4b

| Section | Words | Notes / paragraph | People as subject | Paragraph sd | Sentence sd | Colons / 1,000 w |
|---|---|---|---|---|---|---|
| 1.1 | 666 → 650 | 1.2 → 1.2 | 18% → 19% | 34 → 33 | 7.3 → 6.9 | 1.5 → 0 |
| 1.5 | 467 → 495 | 2.2 → 2.2 | 7% → 8% | 33 → 39 | 4.5 → 6.0 | 4.3 → 0 |
| 2.1 | 609 → 594 | 1.2 → 1.2 | 0% → 0% | 28 → 34 | 6.8 → 6.3 | 4.9 → 3.4 |
| 2.3 | 776 → 597 | 1.0 → 1.2 | 3% → 0% | 49 → 36 | 9.7 → 6.9 | 9.0 → 5.0 |

## Options

1. **Round 4c (recommended; about $1.0).** Rerun 4b on the same four round-4 drafts with the five fixes in place. This shows whether the edits and fixes that were lost now land. Same gate: launch only on at least 3 of 4 full passes plus my judgement. This needs your approval: your rule was to stop here.
2. **Address length first.** Tell the writer to aim at the target rather than the floor, using more of each paragraph's E and C evidence. This is not padding, because the plans hold more establishing evidence than the drafts use. Then run 4c.
3. **Accept 13/14 with named residuals** for 1.5 and 2.3 and launch. I don't recommend it: 2.1 still has an invented agent, and 1.1 still has the forced term.
