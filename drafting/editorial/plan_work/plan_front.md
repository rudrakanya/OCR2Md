# Unified drafting plan: Chapter 4 to the Afterword

*Built 15 October 2026 from the evidence index (`drafting/evidence_index/`, parsed from the two evidence-map files) and the master outline (`Chapter_4_to_Afterword_Master_Drafting_Outline.md`). No API calls. This plan is what each chapter is drafted from. The master outline remains the reference for reasoning, evidence glosses and locators.*

**Authority:**
1. `chapters.md`;
2. the user's rulings (U1–U7, 15 Oct; `drafting/DRAFTING_PROGRESS.md`);
3. this plan;
4. the master outline (Part I rulings, then the chapter entry);
5. the style files.

**Format** (as in the Chapter 1–3 plans):
- each unit gives its historical question, through-line, arc and scope;
- each section gives its statement, purpose, word target and paragraph plan;
- each paragraph gives a **Point** and its evidence as **E** (establishing), **C** (corroborating) or **X** (context), each ID with its tier, e.g. `C04-CII-108 (T1)`;
- `Note:` items feed a `{{note: …}}`.

**Reading the evidence:** full quotations are in `evidence_index/chNN.jsonl`. Print them with `python -I -X utf8 drafting/_tools/quotes.py ID …`. Items from Chapters 1–3 are resolved by the same tool from the evidence log.

**Verification method for every chapter drafted from this plan:** verified in-session, not by an independent model (user ruling, 15 Oct: no API calls).

**QC (scripted, `drafting/_tools/plan_qc.py`; report in `plan_work/QC_REPORT.md`):**
- ID validity;
- one primary home (no item establishing in two units);
- Gazetteer share ≤ 40% per section;
- section targets summing to the unit's planned words;
- hand-offs present and matched.

## Status

{{STATUS}}
