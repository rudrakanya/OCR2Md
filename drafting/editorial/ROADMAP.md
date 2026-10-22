# Udaypur book: roadmap and tracker

*Maintained by the production lead. Updated at the start and end of every phase and at every decision. Last update: 16 October 2026, whole-book outline; drafting paused.*

## Now

| Work | Stage | Elapsed vs target | Spend vs budget |
|---|---|---|---|
| **Drafting PAUSED** (user, 16 Oct) for outline consolidation | No chapter drafting or fixes. D1, D2, D4 finished in Ch 1–4; D3 (Ch 4 six sections) paused at §4.1 | — | $0 API |
| Whole-book outline, Ch 1 – Afterword | **Done** 16 Oct: `Udaypur_Complete_Book_Outline.md` (13 entries; Ch 1–4 reconciled as written), `ABOUT_THIS_BOOK.md`, `OUTLINE_WHOLEBOOK_CHANGES.md`. Coverage 1,789 direct items, none unreasoned. Waiting on D5–D7 | — | $0 API (free scripts; no vector queries) |
| Master drafting outline v2, Ch 4 – Afterword | **Done** 16 Oct: `Chapter_4_to_Afterword_Master_Drafting_Outline_v2.md` (about 34,700 words; 65 sections, 38,850 words planned; every direct item assigned, cross-referenced or excluded with a reason). Changes: `OUTLINE_V2_CHANGES.md`. Sources and rebuild: `plan_v2/`, `_tools/assemble_v2.py`. Waiting on decisions D1–D4 | — | $0 API (in-session; free scripts) |
| Chapter 4 | **Delivered** 16 Oct, about 4,030 words (evidence-limited against 5,000); R2 fixes applied 16 Oct; restructure to v2 awaits D3 | — | $0 API |
| Master drafting outline v1, Ch 4 – Afterword (kept as the record) | **Done** 15 Oct: `Chapter_4_to_Afterword_Master_Drafting_Outline.md` (about 115,000 words; Parts I–VI; 49 sections planned, about 38,000 words of prose). IDs checked by script (1,522 distinct, none missing), and every evidence locator matched to the maps. The alignment check found and fixed 5 mis-cited items. Working files are in `outline_work/` | — | $0 API (in-session) |
| Chapters 1–3 | **Delivered** 14:25 (drafts, footnoted, .docx, combined .docx, ledger, report: `CH1-3_DELIVERY_REPORT_2026-10-15.md`); both gates passed 4/4 | credit-limited phase about 58 min | new spend $5.62 conservative of the $12 cap; about $10.4 credit left |

## Next (ordered)

0. ~~The user's decisions D1–D4~~ *Decided 16 Oct (U10–U13).* **Now: decisions D5–D7** from the whole-book outline (Part I, I.8): Chs 2–3 below the floor; the light-touch fixes RR-42; resuming the Ch 4 revision. Drafting (Ch 5, 7, 8, 9) resumes only when the user lifts the pause.

1. **The user's read-through of the combined Ch 1–3 document** and rulings on the open issues (chapter length, the brass-cover date, the founding dates, the Vidisha range).
2. **Any revision round** that follows, in-session, with API judge/verify only.
3. **Phase D corrections.** Apply the user's hand corrections to the staged OCR (see My tasks).
4. **Page markers and ingest.** Rewrite the staged markers to `<!-- page N -->`, clean lines beginning with `#`, and ingest the public-domain sources into a trial collection, then production on approval. Before Ch 4 and Ch 6. Plan: `public_domain_staging/INGEST_PLAN.md`.
5. ~~Unified plan `PLAN_CH04-AW.md` built (15 Oct); awaiting the user's approval and ruling R1.~~ *Superseded 16 Oct: Ch 4 drafted; the v2 outline now governs.* Then draft Ch 4 with in-session verification, with no API calls (user ruling, 15 Oct). Earlier step, done: plan Ch 4 from the master outline (Part IV, P0): `ch04_plan.md`, then the evidence pack, then drafting. First: the user's rulings U1 (Ch 1 Caulukya governors) and U6 (founding-date wording) from the outline's Part V.

## My tasks (the user's)

| Task | Estimate | Unblocks |
|---|---|---|
| Phase D hand-correction worklist (`public_domain_staging/HAND_CORRECTION_WORKLIST.md`): Beglar, Cunningham and the Gwalior prose first, then Bühler's English pages | about 9 h in all (Beglar, Cunningham and the Gwalior prose 125 min; Bühler's English 173 min; the Gwalior tables 34 min; Bühler's Devanagari 210 min) | Quoting the colonial sources; ingest (Next 4) |
| Find a Sanskrit reader for Bühler's Devanagari transcript (EI I, pp. 233–236) | about 3.5 h of their time | Using the praśasti text itself in Ch 4 and Ch 6 |
| Verify the Gwalior report's printing year and its attribution to M. B. Garde | about 30 min | Citing the second-slab report (para 71) with a full reference |
| Read the combined Ch 1–3 document | about 2 h | Ch 4 planning; any revision round |

## Decisions log

| Date | Decision | Recorded in |
|---|---|---|
| 14 Oct | Ch 1–2 structure approved; wildlife moved to Ch 12 and lichen dating to Ch 7 | `chapters.md` (Plan changes) |
| 14 Oct | No chapter splits or merges; 1093–1305 is treated inside Ch 10 | `chapters.md`; memory `udaypur-book-plan` |
| 14 Oct | Lineage canon: "a kinsman of Bhoja; the exact relationship is disputed" | `Detailed Udaypur Book Outline.md` |
| 14 Oct | Evidence tiers; CII outranks Ganguly on dynastic facts | `_pipe/tiers.py` |
| 14 Oct | Sections at 70–120% of target, chapters 3,200–4,400 words, never pad | plans; `validate.py` |
| 14 Oct | People may be the subject only where an item describes them | `pipeline3.py` WRITER_RULES; `style_profile.md` |
| 14 Oct | The Gazetteer supplies at most 40% of any Ch 3 section | `cfg_ch03v2.py` (GAZ_MAX_SHARE) |
| 14 Oct | Public-domain items 1–4 approved: staged, not ingested | `public_domain_staging/README.md` |
| 15 Oct | Ch 3 plan v2 approved | `chapters.md`; `ch03/ch03_plan_v2.md` |
| 15 Oct | Production is the calibration test (in-line gate); no separate round 4c | `GATE_FAIL_RCA_2026-10-15.md` |
| 15 Oct | Run 1 gate failed, 1 of 4; all chapters stopped | `GATE_FAIL_RCA_2026-10-15.md` |
| 15 Oct | Run 2 approved: code fixes (a); plan notes (b); shorter digest; flagship drafting | this file |
| 15 Oct | Drafting never below high effort; one length-repair call if a section is under 85% of target | this file; `chapter_flow.py` |
| 15 Oct | Budgets including sunk spend: Ch 1 $9.00, Ch 2 $8.25, Ch 3 $8.00, each with a $1.00 reserve | chapter configs |
| 15 Oct | Run 2 stopped after the first flagship drafts: actual $0.45–0.84 a draft projected every chapter past its cap; three in-flight drafts salvaged; possible unlogged orphan calls ≤ $1.11 | ROADMAP Spend; `drafting/run/inhouse_state.json` |
| 15 Oct | Credit-limited plan: $16 credit left; hard stop at $12 new spend; drafting, fixes, author's pass, copyedit and line edit in-session; API only for judge, verify, re-verify and final read on the default model | `drafting/_pipe/inhouse.py`; `drafting/run/DRAFTING_BRIEF.md` |
| 15 Oct | 40-minute target; reduce copyedit, then judge, then author (not below medium); 50-minute report line; no faster tier | `orchestrator.py` |
| 15 Oct | Credit-limited delivery: 9 sections drafted in-session (3 subagents), 6 salvaged flagship drafts revised; gate 4/4 pass at 14:10; final gate 4/4 pass after the line edit; outputs built 14:20 | `CH1-3_DELIVERY_REPORT_2026-10-15.md` |
| 15 Oct | Revised gate: an accuracy failure (Q6, Q7 or Q8) stops; a prose-only failure continues; a final gate after the line edit | this file; `chapter_flow.py` |
| 15 Oct | U1–U7: Caulukya governors (U1); Ch 9 2,800 (U2); Afterword 2,750 (U3); §7.1 1,050 (U4, superseded in effect by v2's §7.2); no API calls (U5); 1080 firm, 1059 a reading (U6); legal handling (U7) | v2 outline, Part I, I.1 |
| 16 Oct | Tier-7 claims phrased as the source's own (U8); Ch 4 target 5,000 (U9) | v2 outline, Part I, I.1 |
| 16 Oct | Master outline v2: evidence rules R1–R9; flexible 4–8-section structures; single Research Register | `OUTLINE_V2_CHANGES.md` |
| 16 Oct | D1–D4 decided: IAST dynasty names (U10); "Bhoja's brother" from Dōngargāon and Jainād (U11); Ch 4 to six sections (U12, paused); Nagpur Karṇa glossed from evidence (U13) | whole-book outline, Part I, I.1 |
| 16 Oct | Drafting paused; one whole-book outline built from Ch 1–4 as written and v2 for Ch 5–AW | `OUTLINE_WHOLEBOOK_CHANGES.md` |

## Research leads (not evidence)

- **ASR IX p. 109** (Cunningham, 1879; archive.org `in.ernet.dli.2015.35534`, PDF index 117). Cunningham records "an inscription of Udayâditya dated in Samvat 1137, or A. D. 1080" (V.S. 1137 = 1080 CE) without saying where it came from. The same page gives Udayāditya "[A.D. 1059 to 1080]". **A lead for Ch 4 and Ch 6, not evidence.** Bühler's EI I p. 232 footnote cites ASR IX p. 107: check that page too.
- **CII's citation** "ASR vol. IX, p. 109" for the 1080 record: reconcile it with the lead above.

## Spend

| Chapter | Sunk before run 2 (calibration, retrieval, run 1) | Run 2 | Total | Budget (reserve) |
|---|---|---|---|---|
| Ch 1 | $3.16 | $0 | $3.16 | $9.00 ($1.00) |
| Ch 2 | $2.67 | $0 | $2.67 | $8.25 ($1.00) |
| Ch 3 | $1.53 | $0 | $1.53 | $8.00 ($1.00) |

**Run 2 (flagship, stopped):** logged $5.44 (Ch 1 $2.20, Ch 2 $1.72, Ch 3 $1.52), of which $2.09 was logged after the freeze at 13:27:09 (the three salvaged drafts plus small calls), plus up to $1.11 in four orphaned calls that may have been billed without being logged.

**Credit-limited plan, actual:** new logged $4.51 (Ch 1 $1.87, Ch 2 $1.37, Ch 3 $1.26) + up to $1.11 unlogged orphans = $5.62 conservative of the $12 cap; log totals incl. sunk: Ch 1 $6.34 / $9.00, Ch 2 $5.13 / $8.25, Ch 3 $3.77 / $8.00; about $10.4 of the $16 credit left.

**Credit-limited plan (from the freeze):** cap $12 new spend, counting the in-flight calls; status in `drafting/run/status.md`; command `python -I -X utf8 drafting/_pipe/inhouse.py spend`.

The sunk figures are the totals in each chapter's API log. They include round 4, round 4b, the Ch 3 retrieval ($0.21), the ledger build and the failed run 1 ($4.36).


## Open issues (carried until resolved)

**Resolved 15 Oct:** 1 (verifier and fix-round fault: fixed in code; duplicate guard), 2 (testimony as measurement: code check + verdict + text fixed), 3 (passive runs: must-fix + rewritten), 5 (1.1 P1 evidence list: plan note), 6 (digest scoped to the section), 10 (`build_outputs` tested and used).

**Resolved 16 Oct (v2 outline):** 15 (U6), 18 ("early 1170s"; R4), 21 (U1, Ch 1 corrected), 22 (U2, U3), 23 (v2 §7.2), 24 (U7; LR-1, LR-2), 25 (folded into the v2 Research Register). The remaining primary checks are tracked in the v2 Part V.

**New from the delivery (details in the delivery report):**
13. Ch 2 (2,608 words) and Ch 3 (2,557) are below the 3,200 chapter floor; 2.5 (153) and 3.1 (343) exhausted their evidence. *Needs the user's ruling (accept, restructure, or assign evidence).*
14. Brass cover: "V.S. 1841 (1775)" does not convert (V.S. 1841 is about 1784–85); text now gives V.S. 1841 only. *Check the inscription; plans say 1775.*
15. Founding dates: only 1080 is firm; 1059 is a reading. *Book-wide ruling on how "1059–1080" is stated.*
16. INTACH Geo-Heritage geomorphology items read as borrowed text, with inconsistent heights. *Check against the survey.*
17. Stream names Kewtan/Keothan/Keotan/Kethan kept separate; C02-JAGTA-HI-001 (teak hill) is a different place: drop from the Ch 2 plan.
18. 608 grant's king unnamed in its item; Lūṇapasāka 1172 (Ganguly) vs 1173 (CII): text says "early 1170s".
19. Badoh items C03-KB-MADHYABHARAT-004/-005 tied to Badoh only via context excerpts.
20. Tiwari's "Garde Sahib" (maintenance under the Scindias) may be M. B. Garde: research lead only.

**New from the master outline (15 Oct; details in the outline's Part I and Part V):**
21. **Ch 1 correction, high priority:** §1.2 and §1.3 present Rājyapāla and Lūṇapasāka as Paramāra presence; both governed for the Caulukya kings (C10-PARTEMPLES-001, C10-CII-002, C08-GANGULY-015/-016). *Needs the user's ruling before Ch 10.*
22. Ch 9 is planned at about 2,800 words, below the floor (as issue 13). The Afterword's length (about 2,750) needs confirming.
23. 7.1 is at about 1,050 words after the hill's sculpture was added at merge (it was orphaned between Chs 5 and 7).
24. Legal sensitivity: Tiwari's mining-network allegation (C12-JAGTA-EN-003), and the claimants named on the 2021 palace signboard.
25. Primary checks listed in the outline, Part V.2 (S1–S18): among them the V.S. 1366 record, the 1163 / V.S. 1220 record(s), the V.S. 1116 / "1513" / V.S. 1562 records, the farman, the 1901 census figure, the GEOHER survey's date and the speakers at Tiwari pp. 161–170.

1. Verifier treats cited inference as FACT-PARTIAL, and the fix round restates facts. *Run 2 fix (a).*
2. Testimony used as a measurement (Tiwari's "5 km"). *Run 2 fix (a) and (b).*
3. Passive proposal runs (1.5). *Run 2 fix (a).*
4. Sections short at medium effort. *Run 2: flagship drafting plus length repair.*
5. The 1.1 P1 evidence list invites a location list. *Run 2 fix (b).*
6. The ledger digest is too long (all 137 figures in every call). *Run 2.*
7. The 70 km end of the settled Vidisha range rests on Tiwari's testimony (C01-JAGTA-EN-011/015). This conflicts with the canon that Tiwari never supplies a measurement. *Needs the user's ruling.*
8. The Gwalior report's year and authorship are unverified. *User task.*
9. Bühler's Devanagari text needs a Sanskrit reader. *User task.*
10. ~~`build_outputs.py` untested~~ Tested 15 Oct on run 1 sections: 84 footnotes, restart per chapter, 19 bibliography books, 8% of the Google Docs limit.
11. Bibliography data incomplete: most books lack place and publisher in the manifest (footnote.py bibliography_todo). Needs the user or the title pages; never invented.
12. Dry-run cost estimator is worst-case for the flagship (11,000 reasoning tokens a call). Run 2 re-projects from actual spend.
