# Chapter pipeline — how to run a chapter and how to read what comes back

For the editorial team. Nothing here requires knowing how the knowledge base was built.

---

## What this produces

For one chapter: a ~4,000-word draft in which **every factual sentence carries a marker resolving to a specific passage in a specific source**, plus a package that lets you check any line without re-searching the corpus.

A worked example is complete at `chapters/C7/` — *Udayeśvara in Stone* — including its handoff package.

## The five stages

Each stage writes a file. You can stop after any of them and pick up later; `state.json` in the chapter folder records where things stand.

```
python chapter_pipeline.py retrieve C7      # 1. pull the chapter's evidence from the KB
python chapter_pipeline.py topup C7 "..."   # 1b. fill a specific gap (repeatable)
python chapter_pipeline.py outline C7       # 2. outline scaffold
python chapter_pipeline.py approve C7 outline   # ← GATE: a human approves the outline
python chapter_pipeline.py brief C7 3       # 3. drafting brief for section 3
                                            #    (the writer returns sections/03.md)
python chapter_pipeline.py verify C7        # 4. mechanical checks → qa_review.md
python chapter_pipeline.py approve C7 draft # ← GATE: a human approves the draft
python chapter_pipeline.py handoff C7       # 5. editor package
python chapter_pipeline.py status           # where every chapter stands
```

**The two gates are real.** `brief` refuses to run until the outline is approved; `handoff` refuses until the draft is approved, and `approve … draft` refuses until `verify` has run. The pipeline stops and waits for a person.

## What each file is for

| file | what it is | when you read it |
|---|---|---|
| `research.md` | the evidence dossier: every chunk bucketed to this chapter, grouped into sub-themes, ranked, with a **coverage note** | before approving the outline — it says what the chapter can and cannot be written from |
| `dossier.json` | the same evidence, machine-readable; the only ids the drafter may cite | rarely; the pipeline uses it |
| `outline.md` | through-line, sections, the evidence under each, and **named research gaps with decisions** | **this is your first checkpoint** |
| `sections/NN_brief.md` | what one section must do, plus only the evidence for it | if you want to see what the writer was given |
| `draft-vN.md` | successive drafts; nothing is overwritten | latest is the live one |
| `qa_review.md` | mechanical checks, then the structured editorial review (What works · Clarity · Flow · Evidence · Style · Line edits) | **your second checkpoint** |
| `handoff/C7_chapter.md` | the draft with markers converted to numbered endnotes, plus the source list | what you edit |
| `handoff/provenance_appendix.md` | every note resolved: chunk id, source, type, epistemic status, page, corroboration, quotability, and the passage itself | when you want to check a line |
| `handoff/coverage_and_caveats.md` | what the chapter rests on, what is single-sourced, what is not quotable, what the KB could not support | before you commit to a claim |

## How to read a marker

In a draft: `… the flagstaff was hoisted in 1080 CE (V.S. 1137) [src: patil-composite-inscriptions-00084].`
In the handoff copy that becomes `[3]`, and note 3 in the provenance appendix gives you the source, its type, its page where one exists, and the passage the sentence rests on.

`[ed]` marks a sentence that is the author's own framing and asserts nothing from the KB — a transition, or a judgement about the evidence as evidence. If you want a leaner voice, cut from these first: removing them costs no evidence.

`[GAP: …]` means the writer wanted to say something the KB could not support and refused to invent it. Treat a gap as a research task, not a typo.

## What `verify` actually checks

It is mechanical, local and reproducible; it does not ask a model's opinion.

- every factual-looking sentence carries a marker (or `[ed]`, or a gap)
- **every cited id exists in this chapter's dossier** — a fabricated citation cannot survive this check
- any quotation of six words or more appears **verbatim** in a cited chunk, and that chunk is quotable: AI-reworded text and OCR pages that failed their quality gate may lead to a fact but may never be quoted
- a sentence resting on an `inference` or `speculation` chunk attributes or hedges
- length within 3,600–4,400 words; text is clean NFC with no mojibake
- how concentrated the evidence is (it will tell you if one book supplies more than half the citations)

C7 finished at **3,673 words, 90 markers, 35 distinct chunks, 0 findings**.

## Things the pipeline deliberately will not do

- **It will not write from memory.** The drafter may cite only the dossier; anything else fails `verify`.
- **It will not quote unquotable text.** 455 chunks in the KB are AI-reworded, and 85 pages of the Rājamārtaṇḍa failed the OCR gate.
- **It will not invent a date.** Where a source has no date, the chapter says so.
- **It will not hide a disagreement.** Where sources conflict — the two published measurements of the Ravan Tol colossus, the 1059-versus-1080 dating — the chapter gives both.

## Known limits, honestly

- **Corroboration counts read low.** The KB's semantic corroboration detector is switched off because the current embedding model could not tell "same claim" from "same subject" (see `RETRIEVAL_VALIDATION.md`). A chunk marked single-source may well be corroborated; it means *not detected*, and the prose attributes rather than asserts.
- **Samarāṅgaṇa page numbers are unusable** — a stray page marker propagated to 1,499 chunks. The dossier shows "no reliable page" for that source; cite it by chunk id.
- **The writing model is not fixed.** Retrieval, verification and packaging are deterministic; the prose comes from whatever model the team uses, working from the brief. The guarantees hold either way because `verify` re-checks the finished text against the KB.
- **Date-sanity flags matter.** The dossier flags construction dates far outside the period — `adhikari-2013-un-00602` says the temple "was completed in A.D. 1880", an OCR corruption of 1080, and it is labelled factual and quotable. The KB cannot catch this; the writer must.

## The sourcebook is an input to drafting

`build_sourcebook.py` writes three things from the KB: `BOOK_SOURCEBOOK.md` (for
people), `source_codes.md` (the citation scheme), and `kb3/sourcebook_facts.json`
(for the pipeline). The chapter pipeline reads the JSON, never the markdown, so
the two cannot drift.

    python build_sourcebook.py            # refresh facts, codes and the sidecar
    python render_sourcebook_docx.js      # the shareable Word edition (~36 pp)
    python chapter_pipeline.py brief C7 2 # brief now carries C7's standing findings

What the sidecar feeds:

* **`brief`** prints the chapter's key facts grouped by status, each with the
  prose treatment that status demands (STYLE_GUIDE §11), plus the chapter's
  gaps and a single-source warning where one book supplies over 45% of the
  bucket. A writer sees what is already settled before writing a line.
* **`verify`** fails a draft that flattens a contested fact to one value, or
  that cites an unverified fact's evidence without carrying its flag.
* **`handoff`** prints each work's source code beside it, so chapter endnotes
  and the sourcebook cite under one scheme.

Rebuild the sourcebook whenever the KB changes; the facts and codes are
regenerated, and `curated_facts.yaml` is re-validated against the KB on every
run — a curated fact whose chunk id no longer resolves stops the build.

## Guards and the smoke test

`approve <cid> draft` refuses a draft that is not ready, and says why:

* the last `verify` ran on a different draft than the newest one on disk (stale);
* that `verify` left findings unfixed;
* the draft still carries `[GAP: …]` placeholders from `assemble --partial`.

`--force` overrides all three, prints the objections it is overriding, and
records `approved_draft_forced: true` in `state.json`, so a forced approval is
never silent.

    python test_pipeline.py

The smoke test checks what anchor-based patching breaks: that every CLI
subcommand is dispatched, that every dispatched handler exists, that no compiled
regex contains a literal backspace (a `` eaten by a shell heredoc — this has
happened three times in this project), that both outline formats parse and
resolve, that `assemble` preserves `[src:]` and `[ed]` markers, and that every
sourcebook status has a prose rule. It writes only to a temp folder and touches
no chapter. Run it after any edit to `chapter_pipeline.py`.

## Verifying the vector KB against the books

    python kb_inventory.py                 # table in the terminal, exit 1 on any problem
    python kb_inventory.py --html          # also writes kb_inventory.html (open in a browser)
    python kb_inventory.py --deep          # check every embedding, not a sample per book

It reconciles four things that can disagree without anyone noticing:

| source | what it holds |
|---|---|
| `Udaypur Reference Markdown Files/` | the books themselves |
| `kb_audit/source_registry.yaml` | what the project claims to hold |
| `kb3/kb_active.sqlite` | the chunk store Chroma is built from |
| `kb3/chroma` → `udaypur_kb` | the vectors retrieval actually reads |

A book counts as **verified** only when the file is on disk, the registry names it, the store has
chunks for it, and Chroma holds a usable vector — finite, non-zero, right dimension — for every
distinct passage. Anything short of that is named in the status column and the command exits 1, so
it can gate a rebuild.

`rows` are chunks in the store; `distinct` are unique passages. Where `rows > distinct` the book
repeats a passage and the builder keeps one vector per distinct text; that is reported as
de-duplication, not as loss.
