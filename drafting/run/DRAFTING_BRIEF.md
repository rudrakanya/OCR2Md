# Drafting brief: in-session drafting of one chapter (no API)

You draft and revise ONE chapter of a serious narrative history of Udaypur (Vidisha district, Madhya Pradesh; NOT Udaipur in Rajasthan). You work only with files and the free commands below. **You never call any model API.** Never run `inhouse.py judge|verify|reverify|finalread`, `chapter_flow.py`, `orchestrator.py`, `pipeline3.py`, `ledger.py build|update`, or anything that imports `run.Run`. The editor runs the paid checks.

Project root: `C:\Users\User\Desktop\Anugrah\OCR2Md`. Python: `python -I -X utf8`. Set `UDAY_CFG` to your chapter config:
- Ch 1: `drafting/ch01/cfg_ch01v5.py`
- Ch 2: `drafting/ch02/cfg_ch02v3.py`
- Ch 3: `drafting/ch03/cfg_ch03v2.py`

## Read once, first
- `drafting/style/style_profile.md` (the house voice) and `drafting/style/style_sheet.md` (conventions)
- your chapter plan: `drafting/ch01/ch01_plan_v5.md` / `drafting/ch02/ch02_plan_v3.md` / `drafting/ch03/ch03_plan_v2.md` (question, through-line, arc, each section statement and each paragraph's Point with E/C/X evidence)
- `drafting/editorial/GATE_FAIL_RCA_2026-10-15.md` (what went wrong last time)

## Per section, in order
1. `UDAY_CFG=<cfg> python -I -X utf8 drafting/_pipe/inhouse.py inputs <sec>` prints everything you need: through-line, chapter arc, section plan with Points and evidence roles, ledger digest, the previous section's full text, and the evidence block (each item's QUOTE, tier and role).
2. Write the section to `drafting/run/ch<N>/<sec>.md`. Sections 1.1, 1.2, 2.1, 2.2, 3.1 and 3.2 already exist there as **salvaged first drafts from the flagship model**: revise them, keeping what is good. Redraft only if one fails badly. The other sections are new.
3. `UDAY_CFG=<cfg> python -I -X utf8 drafting/_pipe/inhouse.py check <sec>` until `"clean": true`. Review any `figure may conflict` ledger notes and style warnings, and fix those that are real.
4. Create the empty file `drafting/run/ch<N>/<sec>.ready` and append one line to `drafting/run/ch<N>/drafting_log.md`: section, words, what you did. Then go on to the next section. The editor judges and verifies ready sections and may send you fixes.

## Format (working draft)
- The first line is the heading exactly as in the plan: `## <sec> <title>`.
- Every sentence that states a fact ends with its evidence ID(s) in square brackets, using only IDs that appear in that section's evidence block, e.g. `[C01-GAZ-007]` or `[C01-GAZ-007; C01-KB-GEOHER-004]`.
- **Do not put IDs on your own inference sentences.** An inference may follow from facts cited in the same or the previous paragraph, but it adds no fact and carries no ID.
- Disagreements, attributions of a scholar's reading, and minor variants go in a discursive note directly after the sentence: `{{note: explanation [IDs]}}`. Write the dispute around the event, not the source.
- Quotations: few and short, copied character for character from an item's QUOTE (English items only), in “curly quotes”, followed by the ID. Never quote an item flagged ⚠. Hindi items: paraphrase from the English rendering.

## Rules (binding)
- **Facts only from the evidence block:** the QUOTE or ENGLISH RENDERING of the items listed for that section. Nothing from your own knowledge: no dates, names, numbers or descriptions not in an item. CONTEXT excerpts help you read an item; they are not facts.
- **Write history, with Udaypur as the subject.** Sources stay in the brackets. Never "[source] says/writes/records", "according to [title]", or "the author".
- **People as subjects** only where an item describes that person or group acting. Never invent quarrymen, builders or masons from a passive "is quarried".
- **Vijay Manohar Tiwari's testimony** (*Jagta Hua Kasba*, JAGTA items) is memory, never the source of a measurement, a distance, a date or a medieval fact. Full name only at the first mention in the book (1.1); afterwards "Tiwari"; no gendered pronouns; never "a visitor".
- **Settled ranges:** Udaypur lies about 13–16 km from Ganj Basoda and 55–70 km from Vidisha. Never narrow either to one source's figure.
- **Canon:**
  - c. 1070 is the working position for Udayāditya's accession;
  - Udayāditya is "a kinsman of Bhoja; the exact relationship is disputed" (never "nephew");
  - a *praśasti* is panegyric: its claims are claims;
  - traditions are memory, never proof of the event they tell;
  - a survey's dates are proposals;
  - compatibility is not identity: never connect the tentatively read two-line inscription with the cave's "remains to be deciphered" lines, and never merge distinct places, buildings, tanks, inscriptions or dynasties;
  - the Gazetteer is the 1979 compilation (date-stamp modern facts);
  - Temple Economics is excluded.
  - In Ch 3, the Gazetteer supplies at most 40% of a section's cited items (the check enforces it).
- **Never fictionalise:** no thoughts, motives, scenes, weather, emotions, sensory detail, journeys or invented causation. The land is a setting, never the cause of a founding.
- **The RCA lessons:**
  - no run of three sentences with the same passive or hedged shape ("has been assigned… may belong… are provisionally dated…");
  - no restated facts;
  - no closing sentence that repeats its paragraph;
  - no method narration ("these figures are used here to…", "is a proposal, not…");
  - census-style or locational figures only where they serve the Point;
  - each paragraph does its Point's historical work, as a whole, without a summary sentence.
- **Continuity:** continue from the previous section, never repeat it. Use the ledger digest (no second gloss, no re-introduced full name). End each section by content that leads into the next, never by announcing it. Use the style sheet's conventions: British spelling, "Muslim", IAST diacritics, numbers.
- **Length:** aim at the section's target word count (IDs and notes excluded) using the evidence the plan assigns; 70% is a floor, not a target. Never pad: if the evidence cannot support more, write less and say so in your log.

## Report back (final message)
Sections written, with word counts; anything you could not support from the evidence; anything in the plan you think is wrong (do not change the plan yourself).
