---
name: historical-nonfiction
description: >-
  House style for drafting a chapter of a source-grounded nonfiction history
  book (the Udaypur / Udayeśvara temple project). Load this before writing or
  revising any chapter prose so every chapter reads as one historian's work --
  covers chapter structure and arc, tone and evidentiary discipline, and
  citation/transliteration conventions. Every drafting call in
  src/gen_draft.py includes this file's body in its system prompt; this is
  also directly invocable for interactive chapter work in Claude Code.
---

# Historical nonfiction house style

This is the single place the book's voice is defined. If a drafting call's
system prompt duplicates any rule below instead of loading this file, that is
a bug — style drift comes from rules living in two places and drifting apart.

## Structure: how a chapter is built

**Opening.** Orient the reader in place and period before anything else — a
chapter should not open on an abstraction or a citation. Ground the first
paragraph in something concrete and visualizable (a monument, a landscape, an
inscription's physical presence) before moving to argument. The reader should
know *where* and roughly *when* within the first few sentences.

**Section order builds an argument, not a list.** Sections are not
independent essays glued together — each should leave the reader positioned
to understand the next. Order by argumentative necessity (what must be
established before what), not by the order sources happened to be retrieved
in. If two sections could swap order without loss, that's a sign the chapter
doesn't yet have a throughline — say so rather than papering over it with a
transition sentence.

**Evidence is woven into narrative, not listed.** A paragraph that reads as
"Source A says X. Source B says Y. Source C says Z." is a failure mode, not a
style choice — even when every claim is faithfully cited. Evidence should
support sentences that are *about* something (an event, a claim, a
disagreement), not be the subject of the sentence itself. Prefer "the temple's
foundation inscription places the event in [year][1], though a later gazetteer
account revises this to [year][2]" over "According to [1], the date is X.
According to [2], the date is Y."

**Transitions carry the argument forward**, not just the topic. A transition
should imply *why* the next section follows from this one ("Having established
X, the question becomes Y") rather than merely changing subject ("Turning now
to Y...").

**Closing.** A chapter closes by consolidating what it established and, where
apt, gesturing at the open question or tension the next chapter will take up
-- not a bare summary restating each section's topic sentence.

**Aim for a scholarly-but-readable arc.** This is narrative history, not a
literature review or a data dump. A reader should be able to follow the
chapter's argument on a single read without needing to reconstruct it from
disconnected facts.

## Tone

- **Third person, measured, authoritative without overclaiming.** No first
  person, no direct address, no diary voice, no rhetorical flourish for its
  own sake (no purple prose, no filler transitions like "It is fascinating
  to note that...").
- **Distinguish evidence from inference, explicitly and consistently.**
  Evidence gets a factual verb tied to its source: "the inscription
  records...", "the gazetteer documents...", "the survey measured...".
  Inference gets a hedging verb tied to the historian's reasoning: "this
  suggests...", "it seems likely that...", "one plausible reading is...".
  Never let an inference read as if it were a source's direct statement.
- **Attribute contested points to their source, and preserve disagreement.**
  When two sources diverge (a date, a measurement, an attribution), name both
  positions and their sources rather than silently picking one or averaging
  them. Scholarly disagreement is a fact about the evidence, not noise to be
  smoothed over.
- **No presentism or anachronism.** Do not judge past actors by present-day
  values, project modern political categories backward, or use anachronistic
  comparisons for color. Describe what the evidence shows about how things
  were understood at the time, not how a modern reader might editorialize
  about them.

## Format & conventions

- **Citations**: every substantive claim carries an endnote resolving to a
  real retrieved passage. Cite using the passage's bracketed id exactly as
  supplied in the evidence (e.g. `[P7]`) -- never write a source name, a
  filename, or a page number directly into the prose. The endnote resolution
  step (not the drafting call) renders the final citation with book, author,
  and **page number when the passage carries one**. If a retrieved passage
  has no page number, the endnote still resolves (book + heading trail) --
  it simply omits the page rather than inventing one.
- **Dates**: BCE/CE, not BC/AD. A date derived from an inscription's regnal
  year or an era conversion should say so briefly on first use in a chapter
  ("in Vikrama Saṃvat 1080, corresponding to 1023 CE") rather than presenting
  the converted date as if it were stated outright in the source.
- **Transliteration**: preserve correct IAST diacritics throughout (ā, ī, ū,
  ś, ṣ, ṇ, ṛ, ṃ, ḥ, etc.) -- never flatten to plain ASCII, never leave
  OCR-mangled forms (â/î/û) uncorrected. Use Devanagari where it is the apt
  form (quoting an inscription's original text, a Sanskrit verse) alongside
  its transliteration and translation, not as a substitute for either.
- **Sanskrit/technical terms**: italicize on every appearance (*śikhara*,
  *garbhagṛha*, *praśasti*) and gloss briefly in-line on first use in a
  chapter ("the *garbhagṛha*, or inner sanctum"). Do not re-gloss a term
  already glossed earlier in the same chapter.
- **Names**: render a place, dynasty, or person's name consistently within a
  chapter once a form is chosen (e.g. "Udayāditya" throughout, not
  alternating with "Udayaditya" or "Udayadeva" absent a source-attributed
  reason to distinguish them). If sources themselves disagree on a name form,
  say so once, pick one for consistency, and note the variant.

## Discipline

- **Never assert beyond what the sources support.** If the evidence is
  silent on a specific detail the section would otherwise want (a date, a
  measurement, a motive), write `[GAP -- not in sources]` in place of the
  detail rather than supplying it from general knowledge or plausible
  inference dressed as fact.
- **Hedge honestly where evidence is thin.** A single passage, a single
  source, or a source of lower reliability (a popular account vs. a critical
  edition) should be flagged as such where it matters to the reader's
  confidence in the claim -- not presented with the same certainty as a
  well-corroborated point.
- **Flag gaps rather than smoothing over them.** A chapter that cannot
  support a claim a reader would expect it to make (because the corpus is
  thin on that sub-topic) should say so plainly rather than let silence
  imply the claim wasn't worth making. This is a feature of an honest
  chapter, not a defect to be edited away.
