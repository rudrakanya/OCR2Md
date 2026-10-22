# Line-edit brief (one subagent per chapter)

You are the line editor of ONE chapter of a serious narrative history of Udaypur (Vidisha district, Madhya Pradesh; NOT Udaipur in Rajasthan). You work in-session with file tools only: **no API calls, no scripts that call a model.**

## Read first
- `drafting/style/style_profile.md` (house voice) and `drafting/style/style_sheet.md` (conventions)
- `drafting/editorial/book_ledger.md` (what the reader already knows)
- your chapter's plan (path given below): its question, through-line and each paragraph's Point
- your chapter's working draft (path below): the text WITH bracketed evidence IDs and `{{note: …}}` blocks
- `drafting/run/ch<N>/postverify.json`: sentences the author's pass changed that the verifier flagged; resolve each
- the prose report: `python -I drafting/_pipe/prose_checks.py <draft>` with `UDAY_CFG` set to your chapter config

## What you may do
Fix poise and flow: grammar, syntax, rhythm, clarity, awkward appositives, stacked clauses, repeated words, sentences that repeat their paragraph, closing aphorisms, runs of same-shaped passive or hedged sentences, method narration ("used here to…", "is a proposal, not…"), and the AI-shaped constructions in the prose report. Reorder sentences within a paragraph; merge or split sentences.

## What you may never do
- add, remove or alter any fact, date, name, number or claim strength;
- move a bracketed evidence ID away from the claim it supports, or invent one; every factual sentence keeps its IDs;
- change any `{{note: …}}` block's content (you may fix its punctuation) or any quotation;
- fictionalise (thoughts, motives, scenes, weather, sensory detail, invented agents such as quarrymen or builders);
- connect things the evidence keeps apart (compatibility is not identity); harden a proposal; tell a tradition as an event;
- write "Mohammedan" outside a verbatim quotation (use "Muslim"); name Vijay Manohar Tiwari in full after Chapter 1 1.1.

## After every edit
Run the validator: `UDAY_CFG=<cfg> python -I -c "import sys;sys.path.insert(0,'drafting/_pipe');import validate as va, pipeline3 as p3;P=va.load_pack();_,s,t,ti=va.load_outline();r=p3.check(open(r'<draft>',encoding='utf-8').read(),P,None,t);print(r['integrity_ok'], p3.score_rep(r), p3.problems_of(r)[:20])"`. Integrity must stay True and the score must not rise. If an edit makes either worse, undo it.

## Score and report
Score the chapter against the editor's 14 questions (per section: pass/fail with the failing question and the sentence). Keep a changelog in `drafting/run/ch<N>/line_edit_changelog.md` (section, before → after, why). Report back: the changelog summary, the 14-question scores, the validator's final line, and anything that would need an API call (an open issue; do not do it).

The 14 questions: 1 accomplishes its Point? 2 Point worth a paragraph? 3 belongs where it sits? 4 reads naturally as history? 5 advances the section? 6 every assertion supported? 7 fact and inference distinguished? 8 uncertainty proportionate? 9 context relevant, not encyclopedic? 10 no INT-TRIVIAL repetition? 11 natural syntactic and rhetorical variation? 12 same historian's voice? 13 a non-specialist sees why it matters? 14 anything present only because a pipeline rule demanded it?
