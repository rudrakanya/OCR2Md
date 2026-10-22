# In-line gate, 15 October 2026: failed (1 of 4). Root-cause analysis

*Run: `drafting/run/` (status.md, state_ch*.json, ch*/ section files at each stage). The chapters stopped at the gate; no author's pass, copyedit or outputs were run. Phase clock: started 12:49:33; run launched 12:57; gate failed 13:07 (17.5 min); all workers stopped 13:09.*

## Gate scores (verified text, before the author's pass)

| Paragraph | Score | Failing questions |
|---|---|---|
| 1.1 P1, the approach | **fail** (10/14) | **Q6 and canon:** "Vijay Manohar Tiwari recalled seeing the temple from 5 km away" uses testimony as a measurement. **Q4, Q9, Q11:** a list of locations (roads, the Bareth station, the 1979 village) instead of the approach the Point asks for. |
| 1.5 P1, the case for an older place | 12/14 | **Q11:** four passive proposals in a row again. **Q14:** "a survival noted in the 1979 Gazetteer"; "The description supplies no secure date". It does keep the two inscriptions apart, and the Point is delivered. |
| 2.1 P5, water held in the hollows | **fail** (9/14) | **Q1, Q4, Q10, Q11:** the fix round turned two inferences into restated facts. P5 repeats its own first sentence and ends on the 80 per cent statistic from P3; P4's last sentence repeats its first two. |
| 2.3 P2, the seam of stone | 14/14 | Kaimur/Rewa gone; the temple's stone is passive ("quarried in the hill close by"); no disclaimer. |

## Failures, classified

| # | Failure | Class | Mechanism | Remedy | Cost |
|---|---|---|---|---|---|
| 1 | The fix round restates facts (2.1 P4–P5, 7 changes) | **(a) pipeline** | The writer attaches IDs to inference sentences. The verifier treats a cited sentence as FACT, rates it FACT-PARTIAL, and FIX_SYS "narrows the claim to its cited evidence", restating a fact the paragraph already has. Nothing checks a fix for duplication. | (i) Verifier: a cited sentence that interprets its items is judged as inference (INT-SOUND or INT-OVERREACH), not FACT-PARTIAL. (ii) FIX_SYS: never restate a fact already in the section; trim the inference or cut it. (iii) Code guard: reject a fix whose sentence shares ≥60% of its content words with another sentence in the section. | Code only, $0, about 15 min |
| 2 | Testimony as a measurement (1.1 P1, "5 km") | **(b) plan**, plus (a) | The 1.1 P1 E item C01-JAGTA-EN-013 contains Tiwari's distance, and the Point doesn't forbid using it. No code check catches a number-and-unit sentence that cites only Tiwari. | Plan note: "Tiwari's sight of the temple, not his distance". Code check: a measurement sentence citing only JAGTA items is a problem. | $0 |
| 3 | 1.1 P1 reads as a location list | **(b) plan**, plus (c) | The P1 E list includes the Gazetteer's road and railway items, which invite a gazetteer paragraph. The writer at medium effort followed the evidence rather than the Point. | Move C01-GAZ-008 (railway) and the road item to X; keep hills, temple and village as E. Draft at higher effort (see 5). | $0 for the plan change; drafting as in 5 |
| 4 | Passive proposal runs (1.5 P1) | **(a) pipeline**, plus (c) | The passive-run check is a 1-point warning; the edit pass may ignore it. | Make a run of 3 or more a must-fix problem (4 points) with the rewrite instruction already in EDIT_SYS. | $0 |
| 5 | Sections short: 15 sections at 45–74% of target (3.4 at 293 of 650 words; 1.2 at 526 of 850) | **(c) model at medium effort**, plus (a) | Your time rule 4 dropped drafting to medium. Medium drafts are 20–40% shorter than high-effort drafts have been. After the edit, nothing restores length (the fix round now ignores length by design). | Draft on the flagship (below), or at high on the current model. Add a length-repair task when a section is under 70% after the edit, drawing on unused E and C items, never padding. | See below |
| 6 | Verifier timeout (1.3, 240 s), retried at low | **(a)** | 240 s is tight for verifying a full section at medium. | 360 s for verify calls only. | $0 |
| 7 | Unresolved flags: 1.1 kept 5 FACT-PARTIAL after the fix round | **(a)** | The fixes were rejected by the code gate (fault 1's interaction). | Covered by remedy 1. | $0 |

**What worked:**
- Judge scores rose to 82–93 of 110 against the old drafts' 44–76.
- The edit-repair path landed 7 edits that would have been discarded.
- The agent-noun, narrator-term and Gazetteer-share checks fired as intended. Ch3's sections stayed within the 40% cap.
- No invented quarrymen; the 2.3 stone sentence was fixed.

## For (c): the writer on the flagship model

Measured from this run's writer calls: 23,000–30,000 input tokens and about 1,500 output tokens per draft.

| | Current writer (gpt-6.1-sol, medium), actual | Flagship writer (gpt-6-astra, high), projected |
|---|---|---|
| Ch1 drafting | $0.39 | about $2.21 |
| Ch2 drafting | $0.32 | about $1.81 |
| Ch3 drafting | $0.30 | about $1.71 |
| Full rerun per chapter, through outputs | — | about $3.8–4.3 |

**Budgets after a full flagship rerun:**

| Chapter | Total spent so far | After the rerun | Budget (less reserve) |
|---|---|---|---|
| Ch1 | $3.16 | about $7.4 | $8.50 ($7.50) |
| Ch2 | $2.67 | about $6.7 | $8.25 ($7.25) |
| Ch3 | $1.53 | about $5.4 | $8.00 ($7.00) |

Ch1 would be close to the edge of its reserve.

**Time:** about 2–3 minutes per flagship draft puts the drafting chain at about 12–15 minutes and a full run at about 35–40 minutes. The prompt digest can be cut by about 40% (it currently lists all 137 committed figures), which lowers both cost and time.

## This run's spend

| Chapter | Spend |
|---|---|
| Ch1 | $1.69 (log total $3.16) |
| Ch2 | $1.43 (log total $2.67) |
| Ch3 | $1.24 (log total $1.53) |
| Pre-flight | $0.002 |
| **Total** | **$4.36** |
