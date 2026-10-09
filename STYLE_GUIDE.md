# House style — *Udaypur: town, temple, dynasty*

The book must read as one hand. This file is the contract: every chapter conforms, and the QA pass checks what can be checked mechanically. Where a rule can be enforced by the pipeline, the check is named.

---

## 1. Register

Serious narrative non-fiction for a general reader who is intelligent but not a specialist — the register of a good trade history, not a journal article and not a guidebook.

- **Lead with the concrete.** A carved bracket, a dated line of Sanskrit, a stone seat worn by backs. Abstraction earns its place after the thing itself.
- **Explain without condescending.** Technical vocabulary (*bhūmija*, *jaṅghā*, *praśasti*) is used precisely and glossed once, at first use, in the flow of the sentence.
- **The evidence is part of the story.** Say who recorded a thing and when. "The inscription on the porch records…" is better than "It is known that…".
- **Sentences vary.** A long, subordinated sentence followed by a short one. Avoid a paragraph of uniform mid-length sentences.
- **No throat-clearing.** Do not open a section by announcing what the section will do.

## 2. Person and tense

- Third person throughout. No authorial "I", no "we" for the reader.
- **Past tense** for events; **present tense** for what still stands ("the śikhara rises in seven storeys"); present for what a source says ("Ganguly argues", "the praśasti records").
- Fieldwork by a named observer is attributed, not absorbed: "INTACH's surveyors found the stepwell choked with silt", not "the stepwell is choked with silt".

## 3. How sources appear in prose

The reader should always be able to tell **what kind of evidence** a statement rests on.

**No source or author names in the reading prose.** The book speaks in one voice. Scholars, surveys,
institutions and book titles belong in the endnotes and the provenance apparatus, never in the
running text. Attribution is satisfied by naming the **evidence**, not the **authority**.

| evidence | how it reads |
|---|---|
| primary inscription | "The foundation inscription of V.S. 1116 (1059 CE) records…" |
| primary text by a Paramāra author | "The *Samarāṅgaṇa-sūtradhāra* prescribes…" |
| field observation | "A 2022 survey fixed the mosque by GPS…" (and see §10 — it is dated) |
| modern scholarship, uncontested | "The temple was begun in 1059." (plain assertion; citation in the marker) |
| modern scholarship, interpretive | name the evidence and hedge to it: "An inscription of the same year points the other way…", "the walled plan suggests…" |
| single-source claim | never present as settled; let the note carry the single source |
| contested | set the evidence against itself: "One chronology gives 1058–1087; the coinage gives 1070–1093." |

**Banned as a substitute for a name.** Removing the surname does not license authority-fog:
*scholars believe*, *it is thought*, *some historians argue*, *tradition holds*, *is said to be*.
Specificity replaces the name — an inscription, a date, a stone, a tank, a census return.

**Provenance markers.** Every factual sentence carries `[src: chunk_id]` immediately before its terminal punctuation. Several sources: `[src: a, b]`. The handoff pass converts markers to numbered endnotes and builds the provenance appendix; the marker is what an editor resolves. *Checked by the pipeline: every id must exist in that chapter's dossier.*

**Quotation.** Quote only from chunks with `is_quotable: true`. Quoted words must match the source exactly. Never quote AI-reworded (`llm_regenerated`) or OCR `needs_recheck` text — use it as a lead, verify the fact elsewhere, and paraphrase with attribution. *Checked by the pipeline: any quoted span of six or more words must appear verbatim in a cited quotable chunk.*

## 4. Epistemic discipline

The KB labels every chunk. The prose must honour the label.

| status | how it may be written |
|---|---|
| `factual` | assert it |
| `observation` | assert as sourced firsthand detail, with the observer named |
| `inference` | attribute and hedge: "suggests", "points to", "Ganguly infers" — never a bare assertion |
| `speculation` | **never asserted.** Either omit, or present explicitly as conjecture with its author named |

Two further rules:

- **Uncertainty is stated, not smoothed.** "No inscription dates the tank; both 1059 and 1080 are inferred from the temple's own dates."
- **Corroboration is information.** Where independent sources agree, say so once ("both the temple inscriptions and Patil's survey…"). Where they conflict, give the conflict. Historians earn trust by showing the seams.

*Checked by the pipeline: a sentence citing a `speculation` chunk must contain hedging or attribution; so must a sentence citing `inference`.*

## 5. Names, script, transliteration and era

This is a house standard, not a preference. A term takes diacritics everywhere or nowhere; there is
no half-and-half. *Checked by the pipeline: `verify` fails on mixed spellings, on Devanagari in
running prose, and on any era form but the house one.*

- **Anglicised geographic names go bare** — Udaypur, Vidisha, Bhopal, Malwa, Betwa, Ganj Basoda,
  Bareth, Dhar, Mandu, Vindhyachal. These are ordinary English forms; no diacritics, ever. Not
  *Mālava*, not *Dhārā*.
- **Sanskrit technical terms and Sanskrit proper names take full IAST, every occurrence** —
  bhūmija, śikhara, garbhagṛha, sabhāmaṇḍapa, praśasti, liṅga, dhvaja; Udayeśvara, Nīlakaṇṭheśvara,
  Udayāditya, Jayasiṃha, Vetravatī, Daśārṇa; dynasty and people names likewise — Paramāra,
  Cauḷukya, Karṇāṭa. Italicise a technical term on first use, roman thereafter.
- **Persian and Arabic follow the same logic** — Muḥammad Tughluq, Jahāngīr, Shāh Jahān, qāzī,
  jālī, Shāhī Masjid keep their diacritics throughout; naturalised English words (mosque, sultan,
  Qur'an) take none.
- **No bare Devanagari in running prose.** Transliterate. Devanagari belongs only in a set-off
  block quotation, a glossary, or a citation of a title in its own script. Where the point is that
  a name was searched in its Indian scripts, say so in words — "not under its Sanskrit name, not
  under its Hindi one" — rather than dropping a raw string into the sentence.
- **One era form: `V.S. 1116 (1059 CE)`** on the first Vikrama year of a passage, `V.S. 1116`
  thereafter. Never *saṃvat*, *Saṃvat* or *Sam* in running text, whatever the source prints.
  Hijri years follow the same shape: `A.H. 737–39 (1336–38 CE)`. Use CE/BCE, never AD/BC, except
  inside a quotation.
- **Regnal spans carry their uncertainty**: "c. 1070–1093" where contested, with the competing
  span given once in the chapter.

## 6. Shape of a chapter

~4,000 words (accepted range 3,600–4,400), in this shape:

1. **Opening (250–400 words).** A scene, an object or a document — something concrete the chapter will pay off. Not a summary of what follows.
2. **Four to seven sections**, each with its own argument or movement, each opening on something specific rather than on a signpost sentence.
3. **A bridge out (150–250 words).** Close the chapter's own argument and turn the reader toward the next chapter's subject. Not a recap.

Paragraphs run 80–150 words; vary them. Sections run 500–900 words. Use subheadings that name the thing under discussion, not the function ("The seven-storeyed spire", not "Architectural analysis").

## 7. What to avoid

- **Unsourced superlatives.** "The finest temple in central India" needs a source that says so, and an attribution.
- **False certainty.** No "clearly", "undoubtedly", "it is well known that".
- **Anachronism.** No "Hindu revival", "medieval India" as a value, no modern nationhood projected onto the eleventh century. Call polities what the sources call them.
- **Filler.** "It is important to note", "plays a vital role", "rich tapestry", "stands as a testament".
- **Orientalist register.** No "timeless", "mystical East", "exotic".
- **Numbers without provenance.** Any measurement, count or date carries a marker.
- **Undated present tense.** "Today the temple is protected" needs the year of the observation.

## 8. The bar for handoff

A chapter is ready for the editorial team when: it is ~4,000 words; every factual sentence carries a resolvable marker; no quotation comes from an unquotable chunk; contested points are presented as contested; the coverage note states honestly what the KB could not support; and an editor can resolve any line to a page image or a source file without asking the pipeline's author.

## 9. The `[ed]` marker

A sentence that carries the author's own framing — a transition, a statement about how the chapter proceeds, a judgement about the evidence as evidence — asserts nothing from the KB and cannot carry a chunk id. Mark it `[ed]`.

It is not an escape hatch. `[ed]` is for sentences that make **no factual claim about the past or the building**. "The other building worth walking to makes the opposite point" is `[ed]`. "The temple stands in a spacious square courtyard" is not: that is a fact and it needs a source. The QA pass counts `[ed]` sentences and lists them, so an editor can see at a glance where the author is speaking rather than the sources.

## 10. Observation is dated evidence

A survey, a heritage walk, a photograph and a census are **snapshots**, true as of the year they
were made. A town changes. Writing an observation in the timeless present asserts that it has not.

- **Every present-state detail drawn from an observation source carries an implicit "as of
  [year of that source]."** Where a section rests on such detail, bind it to its moment once, in
  the prose — "this is the town as the early 2020s found it" — and keep the physical details
  consistent with that frame.
- **Where a detail is known to have changed, do not assert the old state as current.** Move it into
  the past ("until a few years ago the way in was a lane barely six or seven feet wide") and treat
  the change itself as a claim needing a source like any other.
- **A change known to the author but not to the knowledge base is editor-supplied**, and is flagged
  inline exactly as an unverified claim is:
  `[UNVERIFIED — editor-supplied: …; awaiting a source]`. It is never quietly asserted as sourced,
  and it is listed in the handoff's must-resolve items.
- **Beware the opening image.** Arrival scenes lean hardest on observed physical detail and are the
  first thing to go stale. If the fact an opening depends on has changed, the opening is rebuilt,
  and the handoff says so, because a rebuilt hook is an editorial decision and not a copy-edit.

## 11. The sourcebook decides how a fact may be stated

`BOOK_SOURCEBOOK.md` carries every chapter's standing findings, and each one is
tagged with a status. The status is not a note on confidence — it is an
instruction about how the sentence may be written. The drafting brief prints
these, and `verify` enforces the two that can be broken without anyone noticing.

| status | how it may appear on the page |
|---|---|
| `[established]` | assert it plainly; more than one source carries it |
| `[single-source]` | attribute it, do not assert it as settled — name the evidence, not the book |
| `[contested]` | show the disagreement: give the competing values, never only the preferred one |
| `[unverified]` | keep the `[UNVERIFIED — …]` flag; it may never harden into an asserted fact |
| `[gap]` | do not fill it — write `[GAP: what is missing]`, or leave the claim out |

*Checked by the pipeline:* a draft that gives one of a contested fact's competing
values, with no second value and no hedge in that paragraph, fails as
`contested-flattened`. A draft that cites a chunk behind an unverified fact
without an `[UNVERIFIED — …]` flag anywhere fails as `unverified-unflagged`.

**One citation scheme.** The source codes in `source_codes.md` are the project
standard. They appear in the sourcebook, in the drafting briefs, and beside each
work in a chapter's Works-cited list, so a reader moving between the sourcebook
and a chapter is reading one set of names.
