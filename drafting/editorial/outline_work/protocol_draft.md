# Downstream Drafting Protocol

*These are the conventions of this book as they stand after the editor-in-chief audit (14 October 2026) and the delivery of Chapters 1–3 (15 October 2026). Every rule below is observed in, or decided by, a named project file. Where a rule is an inference from practice rather than a written decision, it is marked **(inferred)**.*

## P1. Authority order

When project materials conflict, follow this order:
1. **`chapters.md`.** Titles, scope, order, and what moved where. No chapter is split or merged.
2. **The user's decisions,** recorded in `drafting/editorial/ROADMAP.md` (decisions log) and in the delivery reports.
3. **This master outline** (sections, Points, evidence roles, homes of shared evidence).
4. **`drafting/style/style_profile.md`** (house voice) and **`drafting/style/style_sheet.md`** (conventions).
5. **`Detailed Udaypur Book Outline.md`** (17 Sept 2026), only where the rules above don't supersede it.

Superseded parts of the canon outline include:
- 1059 stated as the founding fact;
- "nephew";
- "does not hedge";
- the 1310 and 1645 records as committed facts;
- the 18-chapter numbering.

## P2. The unit of drafting: plan → section → paragraph Points

- **Each chapter is drafted from a plan** in the format of `drafting/ch01/ch01_plan_v5.md`:
  - historical question;
  - through-line;
  - arc;
  - for each section: a section statement ("By the end, the reader knows …"), a purpose and a paragraph plan;
  - for each paragraph: a **Point** (the historical work it must do) with **E / C / X** evidence roles (establishing / corroborating / context) and a **Note** list for discursive notes.
- **The master outline's section entries convert directly into such plans.** The drafting pass should first write `chNN_plan.md` from this outline, validate every ID against the chapter's evidence pack, then draft.
- **Sections are drafted in order within a chapter.** Each receives the full text of the previous section and the ledger digest. A chapter's first section receives the previous chapter's planned or actual closing.
- **Length:**
  - sections about 450–950 words; chapters 3,200–4,400;
  - a section lands at 70–120% of its target, and 70% is a guard, not a target;
  - **never pad**: if the assigned evidence is exhausted, the section is short and the shortfall is reported.

  Chapters 2 and 3 were delivered under the floor for exactly this reason; that is accepted practice pending the user's ruling (ROADMAP issue 13).

## P3. Voice (house voice, binding)

- **The narrator** is a historian standing in Udaypur and looking outward. Udaypur is the centre of gravity; the Paramāra world and Central India enter only where they change what Udaypur means.
- **The text tells history:** events, changes and decisions in sequence. People are subjects wherever an item describes them acting: a king, a governor, a general, a pilgrim, an archaeologist, today's priests. **Anonymous labour is never invented** from a passive mention ("is quarried" stays passive).
- **Sections usually start from a thing in a place** (a hill, a slab, a dam, a gateway, a named person), and the argument grows out of it.
- **Context comes before the event, briefly and materially,** then the text returns to Udaypur.
- **Interpretation is short, comes after the evidence, and is said once.** Often it lives in the construction of the paragraph (what is set beside what, in what order) rather than in a sentence announcing it.
- **Time is always visible:** before Udayāditya / his lifetime / later Paramāras / Sultanate / Mughal / Scindia / colonial / modern village.
- **A mental map:** distances, directions and heights, used selectively, where they explain something.
- **Plain, exact British English.** Sentence and paragraph lengths vary with the job: some paragraphs run 60 words, some 250.

## P4. Failures to avoid (each observed in earlier drafts; each has a code check)

| Failure | Example from this project | Check |
|---|---|---|
| Source-led prose | "The Gazetteer gives…", "according to…", "the author" | `subject.source_led`; the exemption is only "in Tiwari's account / telling / recollection / testimony / memory" |
| Restated facts / INT-TRIVIAL | 2.1 P5 after run 1's fix round repeated its own first sentence | `prose_checks.duplicates_other`; verifier INT-TRIVIAL |
| Inference carrying citations | IDs bolted onto an interpretive sentence, then "fixed" into a restated fact | Writer rule: IDs only on factual sentences; verifier judges cited inference as INT |
| Closing aphorism | "Village and farmland therefore share more than a boundary." | `prose_checks.ai_shape` (paragraph-final aphorism) |
| Method narration | "These figures are used here to describe the modern regime…" | META patterns |
| Passive or hedged runs | four proposals in a row ("has been assigned… may belong… are provisionally assigned… have been read") | `prose_checks.passive_runs` (MUST FIX) |
| Testimony supplying a measure | Tiwari's "5 km", "thousands", the "five hundred years" | `prose_checks.testimony_measures`; verdict TESTIMONY-AS-MEASURE |
| Invented agents | "quarrymen extracted it" | `prose_checks.agent_nouns`; verdict AGENT-INVENTED |
| Narrator terms | "Mohammedan" in the narrator's voice | `prose_checks.narrator_terms` |
| Digression | Kaimur/Rewa sandstone classes; the list of forest produce | judge criterion "digression" |
| Gazetteer dominance (Ch 3 rule) | more than 40% of a section's cited items | `GAZ_MAX_SHARE` |

## P5. Evidence handling

- **Every factual sentence ends with its evidence IDs** in the working draft. Inference carries no IDs. Discursive notes are `{{note: … [IDs]}}`.
- **Reader-facing notes are consolidated** (`footnote.py convert_consolidated`): one note per paragraph or claim cluster, Chicago style, hidden IDs.
- **Evidence tiers:**
  1. contemporary inscriptions (CII VII.2), read critically;
  2. fabric and archaeology;
  3. later inscriptions;
  4. documents and normative texts;
  5. modern scholarship;
  6. colonial observation;
  7. modern survey and the 1979 Gazetteer;
  8. tradition and Tiwari's testimony;
  9. popular or heritage accounts;
  10. the book's own inference.

  **CII outranks Ganguly** on dynastic facts. **Ganguly's interpretations are attributed to him** in a note.
- **Graded confidence, attached to the clause:**
  - established: "was";
  - probable: "probably";
  - possible: "may", "could";
  - proposed: "has been read as", "is assigned to";
  - traditional: "the village tells", "is said to";
  - unknown: say so once.

  Never stack hedges.
- **Compatibility is not identity:** never merge inscriptions, buildings, tanks, traditions, rulers, places, layers or hypotheses unless an item says they are one.
- **A praśasti** gives what the dynasty claimed. **A tradition** is evidence for memory. **A survey's dates** are proposals.
- **Tiwari** (JAGTA) is testimony: never a medieval fact, measurement, count, distance or date. Named in full once in the book (§1.1); "Tiwari" thereafter; no gendered pronouns; never "a visitor".
- **SAMAR** items: ⚠ old OCR, never quoted. The text is normative, not a record. Bhoja's authorship is doubted (note).
- **Temple Economics** is excluded.
- **Quotations:**
  - few and short;
  - copied character for character from an item's QUOTE (English items only), in curly quotes;
  - Hindi items are paraphrased from their English rendering;
  - about two quotations per section at most (from the earlier writing rules; inferred to still apply).
- **Disagreements:** the text keeps the question and what hangs on it; who argues what goes in a note. Minor numeric differences become ranges. Settled ranges:
  - 13–16 km from Ganj Basoda;
  - 55–70 km from Vidisha.

  The 70 km end rests on Tiwari; that is open issue 3 in the delivery report.

## P6. Chapter and section shape

- **A chapter opens on something concrete that carries its question.** It takes up the previous chapter's last line by content, never by recap.
- **Each section ends by content** that leads into the next. No announcements ("the next section…"), no summaries, no rhetorical questions, no "this chapter".
- **A chapter's last paragraph leads into the next chapter by content.** Observed endings:
  - 1.5: "had to make terms with that stone and that water";
  - 2.5: "whether anyone had used it before Udaypur had its name, the ground itself does not say";
  - 3.5: "Who held the hill itself in those years is not known."

  **(Inferred:)** endings land on an open, concrete question or condition, not on a verdict.
- **Thematic chapters still move through time** where their material allows. Architecture is evidence (patronage, resources, craft, conquest, reuse, worship, memory), never an inventory.
- **Scale shifts on purpose,** from the village to Malwa and back, and each shift earns its place by changing what the reader understands about Udaypur.
- **Signposting is minimal:** no metadiscourse. The section titles and statements carry the structure.
- **Historiography stays mostly in the notes.** A scholar is named in the text only when an actor in the story (Beglar, Cunningham, Bühler, Garde as first readers) or when the disagreement changes the answer.

## P7. Continuity machinery

- **`drafting/editorial/book_ledger.md`** records what the reader has already been told. Check it for:
  - first mentions and glosses (gloss a term once, at its first appearance in the book);
  - full names (introduced once);
  - committed figures (never contradicted, ranges never narrowed);
  - open questions.

  `ledger.py digest <section>` gives the section-relevant subset; `ledger.py check` flags second glosses, re-introduced names and conflicting figures.
- **Each item of evidence has one home chapter** (the evidence maps' "home unit"); other chapters recall it in a clause or reinterpret it. The master outline's Cross-Chapter Architecture assigns homes for every shared cluster and every recurring conflict.

## P8. Process (credit-limited regime, 15 October 2026)

Drafting is done in-session, with up to three subagents, one per chapter, working from:
- the section's plan entry, Points and through-line;
- the cached evidence block;
- the ledger digest;
- the style files;
- the previous section's full text.

Free checks run after every edit:
- `drafting/_pipe/inhouse.py check <sec>` (validator, prose checks, ledger);
- `apply_fixes.py`.

Paid calls, all on the default model under a hard cap:
- **judge and verify:** one call each per section, medium effort;
- **re-verify** changed sentences: one call per chapter, low effort;
- **final independent read:** one call per chapter, medium effort.

Then the in-session author's pass, copyedit and line edit, and `build_outputs.py`. A calibration gate on named paragraphs scores them against the user's 14 questions, at mid-run and again after the line edit.

**Lessons that must survive:**
- the verifier sees sentences out of paragraph context during re-verification, so its "new fact" flags on inference need judgement;
- sentence-boundary regexes must not split decimals ("1,229.9");
- cutting a sentence can leave a dangling "there", "its" or "the shaft": re-read the paragraph after every cut.
