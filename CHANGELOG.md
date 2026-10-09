# CHANGELOG — knowledge base build (append-only)

Every OCR decision, taxonomy reassignment, dedup, archive and integration step.
Machine-readable copies of the same events are in `kb_audit/audit_log.jsonl` and `kb3/logs/*.jsonl`.

---

## 2026-09-24 — Phase 0: diagnosis

- Read Stage 1 artifacts (`KB_AUDIT.md`, `source_registry.yaml`, `classified_inventory.jsonl`) and the Stage 2 build (`KB_STAGE2.md`). No store was modified.
- Confirmed: old `kb/store.sqlite` (10,754 chunks) keeps a working BM25 path; its dense path stays dead — `embeddings.npy` covers 9,467 chunks and was built with an embedding API whose quota is gone.
- Confirmed the Stage 2 SQLite store (15,799 active / 3,390 archived) is sound and becomes the BM25 sidecar.
- Set aside 4,096 partial `bge-m3` vectors (`kb3/emb_parts/`): usable only in bge-m3's own vector space, and that run was killed twice for low memory. Kept on disk, not deleted.
- **Decision — embedding model:** `intfloat/multilingual-e5-small` (384-d, int8, already cached) over `BAAI/bge-m3` (1024-d). Measured: bge-m3 4–9 chunks/s and killed twice at ~3 GB RSS; e5-small ~8.5–14 chunks/s at ~0.5 GB. Quality trade recorded in `DIAGNOSIS.md`; the build script takes `--model` so bge-m3 can replace it on a larger machine.
- Wrote `DIAGNOSIS.md`.

## 2026-09-24 — Phase 1: OCR quality gate (Rājamārtaṇḍa)

- OCR was performed in the previous session with **Tesseract 5.4, `-l Devanagari --psm 3`, 400 dpi** — a real OCR engine. No LLM read, transcribed or reconstructed any text at any point.
- Ran `ocr_qc.py` over all 116 pages: per-word confidence from Tesseract TSV, gutter/edge analysis, baseline skew, printed-page sequence, CJK and script-mismatch checks. Rendered one JPEG per page beside the raw per-page OCR for eye-checking.
- **Authorship verified from the title-page image**, not the filename: भोजदेवकृत-राजमार्तण्डवृत्तिसमेतम् (commentary composed by Bhojadeva); introduction on धारेश्वरभोज (Bhoja of Dhārā); editor Ram Shankar Bhattacharya; publisher Bharatiya Vidya Prakashan, Varanasi.
- **No year on title page or imprint** → `publication_date: undated-flagged`, not guessed. **No closing colophon in the scan** (text ends mid-discussion on pdf p. 114 / printed p. 80; p. 115 blank; p. 116 publisher advertisement) → flagged.
- **Gutter threshold tightened from >18 to >12 points** after eye-checking pdf p. 64, whose line-ends are physically cropped in the scan. Result: 31 pass, 85 needs_recheck, 0 illegible (was 64/52/0 at the looser threshold). Decision recorded because it materially changes how much of this book is quotable.
- **Page order verified intact**: no gaps between adjacent pages; the single apparent decrease (pdf 63→64) is an OCR misread of the printed header [३०] as [२०], confirmed by eye.
- Gate stamped into every page marker of the markdown (`gate:`, `ocr confidence`), so chunks inherit quotability.
- Two process-hygiene notes: an earlier QC run wrote confidence 0.0 for every page because the custom `tessdata` directory had no `configs/` folder (fixed by copying it); a stale process from that run survived a kill and interleaved its output with the good run, so both were re-run cleanly to fresh paths.

## 2026-09-24 — Phases 2-5: taxonomy, classification, ChromaDB, validation

**Phase 2 — refined taxonomy.** All 26 existing sources reassigned from the five coarse types to the ten pointed ones; each entry keeps `source_type_coarse` for traceability; every change logged in `kb3/logs/taxonomy_reassignment.jsonl`. Notable: Patil 1952 `reference_tertiary` → `secondary_core`; the Patil inscriptions composite → `primary_epigraphic`; Krishna Deva → `secondary_comparative`; Kumar 2023 and Suryavanshi 2013 → `environmental_scientific`. The Rājamārtaṇḍa added as source 27 (`primary_authorial_paramara`, with its two layers declared). 17,583 chunks retyped at build time from the registry.

**Phase 3 — two-layer classification of the new book.** 243 chunks. Layer rule by pdf page, verified against the page images: 1-4 front matter (authorship evidence), 5-33 + 35 editor's introduction on Dhāreśvara Bhoja → `secondary_core`, 36-116 the commentary → `contextual_thematic` (`yoga_doctrine`), except passages naming Bhoja/Dhārā/Paramāra/Mālava, promoted to `primary_authorial_paramara`. Result: 60 authorship-layer chunks, 183 doctrine. Quotability inherited from the OCR gate.

**Phase 4 — ChromaDB.** `intfloat/multilingual-e5-small`, int8, mean-pooled, `passage:`/`query:` prefixes: 18,930 vectors in 24 min (bge-m3 would have taken hours and was killed twice). Persistent client at `kb3/chroma`; collection `udaypur_kb` (14,647) and separate `udaypur_kb_archive` (4,434). Ids frozen as `<content_hash>-<source_id>`; re-runs upsert in place. Chroma metadata is scalar-only, so lists are stored as joined strings plus `in_<chapter>` / `tag_<name>` booleans for `where` filtering, alongside all five 0-1 scores.

**Threshold recalibration (model-specific, measured).** Random claim-bearing pairs average cosine 0.811 under e5-small (p99 0.878), so the bge-m3-era 0.85 corroboration threshold produced 236,856 false pairs. Semantic corroboration disabled by default (`--corro-cos 0`); dated entity-year keys and the claims register carry it. Cross-lingual duplicate linking switched from a bare cutoff to **mutual nearest neighbour** inside a positional window: 320 Tiwari EN↔HI links.

**Phase 5 — validation.** All 17 chapters smoke-tested. 0 yoga-doctrine chunks outside C5/C10 (added a layer rule restricting that layer to those two chapters); 0 non-quotable results under `--quotable-only` across 340 results; 0 archived records in the active collection; Tiwari 10/10 in C13 and C16. Recorded limitation: with e5-small an English query reaches the new book's Hindi pages only at rank ~360/2,880, versus 34 for the same question in Devanagari — remedies documented in `RETRIEVAL_VALIDATION.md`.

## 2026-09-24 — Chapter-writing pipeline

- **Audited the existing attempt** (`draft_chapter.py` and its evidence/verify/sources modules) → `WRITING_PIPELINE_AUDIT.md`. Verdict: keep the design, replace the implementation. It retrieves rather than free-writes and its entailment gate is the best idea in the codebase, but it imports a dead API, reads the dead `mistral-embed` store (`grep -l chroma` across its five scripts returns nothing), carries **zero resolvable chunk ids** across nine drafts, mis-cites the serpentine paper as "Singh 2019, Zenodo" (registry: 2023), runs to 9,967 words on a 4,000-word target, and works to a 19-chapter scheme the KB no longer uses.
- **Wrote `STYLE_GUIDE.md`**: register, person/tense, how each evidence type appears in prose, epistemic discipline per `epistemic_status`, IAST rules, chapter shape, what to avoid, and the `[ed]` convention for authorial framing.
- **Built `chapter_pipeline.py`**: retrieve → topup → outline (gate) → brief → verify → approve (gate) → handoff, one folder per chapter, `state.json` for resumability. Sub-themes come from k-means over the KB's own vectors; the dossier leads with a Udaypur-specific "spine" and caps any one book at four rows per sub-theme.
- **KB defect found and worked around:** the Samarāṅgaṇa markdown has no page markers, so one stray "Page 320" line propagated to 1,499 chunks (7 distinct pages across 1,499). Citing those pages would send an editor to nothing. `kb3/pages_unreliable.json` records it; the dossier prints "no reliable page" for that source. **Fix at the next Stage-1 rebuild: a page marker must not propagate when a source has fewer than five of them.**
- **Date-sanity flags added** after `adhikari-2013-un-00602` ("completed in A.D. 1880" — OCR damage for 1080, labelled factual, quotable, single-source) turned up in the C7 dossier. Not cited; recorded in the outline's gap list and the README.
- **Worked example C7 end to end.** Dossier 4,199 bucketed chunks → 123 after four gap top-ups; outline with six named gaps and a decision for each; three drafts. v1: 3,258 words, 19 unsourced sentences, 1 inference asserted. v3: **3,673 words, 90 markers, 35 distinct chunks, 0 findings**, all quotations verified, 0 fabricated citations. Handoff package: chapter with numbered endnotes, provenance appendix, coverage note.
- **Two checker bugs fixed while running it**, both found by the draft: the `[GAP` counter used a malformed pattern, and the attribution regex required a lowercase "in", so "In Pande's reading…" was wrongly flagged as an asserted inference.
- **Wrote `PIPELINE_README.md`** for the editorial team: the five stages, what each file is for, how to read a marker, what `verify` checks, and the known limits.

## 2026-09-25 — Chapter 1 drafted end to end

- **Skills:** `docx` was installed and used to render the Word deliverable. `doc-coauthoring` was **not** installed; I fetched it from `anthropics/skills` into `~/.claude/skills/doc-coauthoring/` and it loaded, so its Reader Testing stage ran for real. `content-research-writer` is still not installed; its loop was implemented per the brief.
- **Decisions applied as instructed:** the 1070 accession uses the agreed wording and the Stance section shows the Panhera/Udaypur conflict rather than hiding it; the Qanungo Baoli claim is present but carries an inline `[UNVERIFIED — NOT IN KB]` flag and no `[src:]` marker, paired with the 1775 Scindia brass plate so the Maratha layer stands on real evidence.
- **Outline claims corrected against the evidence:** Tughluq mosque 1336–38 (not 1336–39); Mughal mosque begun under Jahāngīr and completed 1632 (1616 appears nowhere in the corpus); 1310 is Paramāra survival with the Sultanate holding the area by 1338, not a Khaljī conquest of Udaypur.
- **Reader Testing (doc-coauthoring Stage 3) caught three serious defects my own pass missed**, all fixed: a false claim inside the Stance section ("true on every reading" applied to a formulation two sources contradict); invented colour ("a Tuesday market's worth of shops", "two hours from a state capital", a "guildsman's hall"); and a five-regime spine that listed six regimes and then referred to a set of "five buildings" that did not exist. Six further fixes: the temple's two names identified at first mention, Udaypur distinguished from Udaipur (Rajasthan), "KB" jargon removed from the prose, the 900/1,000-year inconsistency resolved, the record-list completed, and V.S./A.H./INTACH/liṅga/qāzī glossed.
- **Three checker bugs found and fixed while drafting**, all of which had been silently degrading verification: sentence splitting orphaned trailing `[ed]`/`[src:]` markers from their sentences; the abbreviation guard was written with a literal backspace instead of `\b`, so "V.S. 1116" split mid-sentence; and the provenance appendix did not collapse newlines, which broke four table rows.
- **Final state:** 3,962 words, 111 provenance markers over 32 chunks, **0 fabricated citations, 0 unsourced factual sentences, 0 unverified quotations, 0 unhedged inference or speculation**. Handoff at `chapters/C1/handoff/`: Word file, chapter with numbered endnotes, provenance appendix, coverage note, and a must-resolve list headed by the Qanungo Baoli placeholder.
- **Not possible on this machine:** visual PDF proofing of the Word file (no LibreOffice, pandoc or pdftoppm). The .docx was verified structurally instead — 33 table rows, 111 endnote references, diacritics intact.

## 2026-09-25 — C1 draft-v6: opening retoned, references deduplicated

- `chapters/C1/draft-v6.md`: §1.1 Arrival rewritten so the opening paragraphs describe the
  approach without the narrator's disappointment. Tiwari's "heap of garbage" image and the
  "desolate junction" / "suffocating lane" wording are out of the prose; his advocacy with the
  shopkeepers, panchayat and officials is still reported, attributed to him. Every factual
  sentence kept its `[src:]` marker, the remaining quotations are still verbatim, and no
  positive colour was invented. 3,906 words, 0 mechanical findings.
- `chapter_pipeline.py handoff`: *Sources cited* now carries **one numbered entry per work**
  instead of one per chunk — C1 goes from 32 entries to 9 — with the pages cited listed on the
  entry. Repeated adjacent references to the same work are collapsed. The provenance appendix
  is unchanged in substance: it still has one row per chunk, now grouped under its work's number,
  and its intro says so.
- `chapters/C1/handoff/C1_Udaypur_chapter.docx` re-rendered (356 paragraphs, 8 headings,
  9 source entries, 33 appendix rows, diacritics intact).

## 2026-09-25 — C1 draft-v7: prose de-metaed, clean reading copy added

- `chapters/C1/draft-v7.md`: the chapter no longer narrates its own construction. "this book",
  "this chapter", "the sources assembled for this book", "the reader is entitled to know" and the
  rest are gone; §1.3 retitled *What is actually old here* and §1.5 *The evidence, and three dates*,
  both rewritten so the method is carried by how the evidence is stated rather than by commentary
  about the method. The cut method paragraph on quotation provenance survives in
  `coverage_and_caveats.md` and the provenance appendix, where it belongs.
- De-metaing cost ~410 words, so the chapter was brought back into its 3,600–4,400 band with
  sourced material rather than padding: where Udaypur actually is (`intach-geoheritage-00132`,
  `intach-2022-udaypur-00043`) and the Vidisha gazetteer's scripturally-attested district
  (`vidisha-gazetteer-1979-00001`), which sharpens §1.3's negative finding. 3,642 words, 0 findings.
- `chapter_pipeline.py handoff` now also writes `<cid>_chapter_reading.md`: the same text with
  `[ed]` and `[UNVERIFIED]` stripped and a plain author/title/page source list.
- `render_docx.js` renders both `C1_Udaypur_chapter.docx` (editor copy: markers + appendix) and
  `C1_Udaypur_chapter_reading.docx` (reading copy: chapter + sources), and now skips with a
  warning instead of crashing when a target file is open in Word.

## 2026-09-25 — C1 §1.5 rewritten to argue the accession from both sides

- The accession is no longer stated as "the likeliest reading" with the alternative as an aside.
  §1.5 now poses the question (in 1059, sovereign of Mālava or prince building in his own
  territory?) and makes both cases from the evidence: the early dating on the 1059 temple and tank,
  Patil's 1058–1087, Ganguly's own 1059–1086, INTACH's c. 1059–93 and the succession crisis
  (`ganguly-paramara-00284`); the later dating on the Panhera inscription of the same year
  (`ganguly-paramara-00262`), on Mālava being won from Karṇa, who was not yet king in 1059
  (`ganguly-paramara-00279`, `-00274`), and on INTACH's numismatic 1070–1093.
- Added the fixed points both sides share, which the section previously lacked: the Shikarpur
  record of 1077 and the Jhalrapatan inscription of Sam 1143 / 1086 CE (`ganguly-paramara-00293`,
  `-00290`). The disagreement is then confined to one decade, which is what it actually is.
- 4,066 words, 0 findings; 117 markers over 38 chunks; evidence spread evened out
  (INTACH 2022 8, Ganguly 8, Tiwari 7, INTACH geo 5, Patil 3, Patil composite 2).

## 2026-09-25 — C1 draft-v8: prose pass, and a reading copy with no apparatus

- `chapters/C1/draft-v8.md` (3,903 words, 0 findings). Prose-only pass: identical claims, identical
  sourcing, identical argument — asserted by test, the build refuses to write if the set of cited
  chunks changes (38 chunks, unchanged).
- Remaining self-commentary cut: "Two cautions belong with this", "The second caution is
  chronological, and it matters more than it looks", "That has to be put precisely, because the
  evidence is not silent", "the dispute deserves setting out in full", "His reading of the palace is
  an inference from the standing remains rather than a documented fact". Where one carried real
  epistemic weight it was moved into the phrasing: §1.4 now states that no record says the three
  namings were one act, then makes the place-making claim in its own voice.
- §1.2's ordinal bold heads ("**First, the Paramāras.**") and §1.5's bold method heads are now
  sentence openers, so both sections read as prose rather than as lists.
- Attribution untouched: Tiwari's palace reading, Ganguly's surmise and INTACH's inferences are all
  still credited. "on Ganguly's surmise" no longer repeats three times — "Ganguly argues",
  "in Ganguly's reading" and the surmise itself now carry it in turn.
- `handoff` now writes the reading copy to `chapters/C1/C1_chapter_reading.md` with **no citation
  markers at all** (previously numbered) and an unnumbered source list. Marker runs are stripped as
  a unit, so the commas that separated them do not strand against the punctuation.
  The `[UNVERIFIED]` flag is kept on purpose.
- Both Word files re-rendered and current: `C1_Udaypur_chapter.docx` (414 paragraphs, appendix
  table) and `C1_Udaypur_chapter_reading.docx` (60 paragraphs, no table, no markers).

## 2026-09-25 — C1 draft-v9: sources out of the prose, new opening

- `chapters/C1/draft-v9.md` (3,700 words, 0 findings). Same 38 chunks cited as v8, asserted by the
  build. In-prose source mentions go from 43 to 0: no personal bylines and, at the author's
  instruction, no institutional ones either. "INTACH records the Udaysagar tank as built by
  Udayāditya in 1059" becomes "the Udaysagar tank was built by Udayāditya in 1059"; a 2022 survey
  is "a heritage survey carried out in 2022"; the district gazetteer's account of Vidisha is given
  without naming it.
- Epistemics moved from attribution to hedging: "has been read as indicating", "appears to place",
  "probably not yet the paramount king", "offered as a surmise rather than a finding". All five
  inference/speculation chunks still pass the checker.
- §1.5's accession argument is now evidence against evidence rather than Patil against Ganguly;
  all four date-spans and the two-sided structure are unchanged.
- The four verbatim Tiwari quotations are gone, converted to reported description, since a
  quotation with no named speaker is worse than none.
- New opening: the chapter now begins on the six-foot lane, the stone doorway and the masterpiece
  behind it, in a village of six thousand. The Udaipur-of-Rajasthan comparison is cut.
- `HEDGE` in `chapter_pipeline.py` accepted "has been read" but not "have been read"; fixed.

## 2026-09-25 — C1 draft-v10: prose rewrite, and a draft-selection bug

- **Bug found and fixed first:** `verify`/`handoff` picked the draft with
  `sorted(glob("draft-v*.md"))[-1]`, which is lexicographic — `draft-v9` sorts after `draft-v10`.
  The first v10 run therefore verified and shipped v9 while reporting success. Added `drafts_of()`,
  which sorts by version number, and re-ran everything. Any chapter reaching v10 would have hit this.
- `chapters/C1/draft-v10.md` (3,727 words, 0 findings, same 38 chunks). Rewritten for prose rather
  than for coverage: scene first, evidence underneath. No source or author names in the body, no
  reportage-internal figures, and no authority-fog substituted for them — every hedge is tied to a
  named piece of evidence ("an inscription of the same year points the other way"), never to
  "scholars believe" or "it is said".
- Cut as method commentary: "Udaypur is documented by several incompatible kinds of record…",
  "Some of what is known rests on a single witness…", "It is a reconciliation rather than a proof…",
  "One volume cannot speak for the whole of Sanskrit literature".
- §1.5 restaged as argument rather than ledger: the building and the succession crisis against the
  Panhera inscription and the Karṇa problem, with the four date-spans folded into the side each
  supports instead of listed.
- Mined detail already inside cited chunks rather than padding to length: the temple's red
  sandstone, square courtyard with stone seating, *garbhagṛha*, *sabhāmaṇḍapa*, three porches
  (the east one being the shut door), seven-storeyed *śikhara* and the figure climbing the pinnacles
  (`patil-composite-inscriptions-00084/85`); the *jālīs* of the Shāhī Masjid; and — the find that
  matters most — the temple's own continuous epigraphic sequence in Sanskrit, Persian and Hindi
  across eight centuries, saṃvat 1137 to saṃvat 1985 (`singh-serpentine-00002`), which is direct
  evidence for §1.3's central claim and had not been used.

## 2026-09-25 — C1 endnote apparatus

- The reading copy now carries superscript note numbers (¹ ² ³) and nothing else; `[src: …]`,
  `[ed]` and the `[UNVERIFIED]` bracket are all gone from it. New `chapters/C1/C1_endnotes.md`
  holds the citations, generated from the master's markers so the two cannot drift.
- `reading_and_notes()` collapses markers so a note number tracks a **distinct source, not a
  sentence**: one note per work per paragraph, placed at the last marker of the run, with the
  number following the punctuation. 118 inline markers become 77 notes, 12 of which carry more
  than one work — the first time corroboration is visible to a reader.
- Numbering is assigned by anchor position after collapsing, so the sequence a reader meets
  ascends even when a paragraph alternates between works.
- The Qanungo Baoli gets note 31, which states that no ingested source supports the claim and
  that no citation should be supplied until one is produced. It is never given a fabricated cite.
- `render_docx.js` appends the endnotes to the reading .docx as back matter, with the internal
  `[kb: …]` chunk tags stripped; they remain in the .md for traceability.

## 2026-09-26 — C1 draft-v11: reviewer root-cause pass

**A. Transliteration, script, era.** Normalised to a house standard now written into
`STYLE_GUIDE.md` §5 and enforced by `translit_findings()` in `verify`. Substitutions: Mālava → Malwa
(×11), Dhārā → Dhar (×4); `Vikrama Saṃvat`/`saṃvat`/`Sam` → `V.S. NNNN (NNNN CE)` (×7 sites, incl.
V.S. 1985 → 1928 CE); Devanagari उदयपुर removed from running prose and said in words. The new check
finds 12 defects in v10 and none in v11.

**B. Time-bound observation.** The entrance lane is no longer asserted as narrow-and-current. §1.1's
opening was rebuilt around the stone doorway and the masterpiece behind it; the six-foot lane moves
into the past and the widening is flagged `[UNVERIFIED — editor-supplied]`, not silently asserted.
"the lane is as it was" → "for years nothing changed"; the closing snapshot is bound to its moment.
`STYLE_GUIDE.md` §10 now makes this a book-wide rule.

**C. Gaps and unresolved items.**
- The 1310–1338 interval is marked as a gap, not glossed: the dossier carries nothing on how the
  country changed hands, and the chapter now says so.
- **The Qanungo Baoli is resolved by verification.** 1645 appears nowhere in the corpus as a date;
  "trilingual" nowhere; "Qanungo/Kanungo" only as a revenue officer. But **`Kanongo`** hits once:
  an inscription found near the Kanongo Baoli, now on the Badi Mata Mandir wall — six lines,
  Nastaliq and Hindi, a Qur'anic verse, recording Ibrahim Lodhi son of Sikandar Lodhi, dated
  V.S. 1578 (1522 CE) (`intach-2022-udaypur-00100`, added to the dossier). Almost certainly the
  object behind the report, and Sultanate rather than Maratha.
- Subject restored: "The accession to the throne of Mālava probably falls…" → "Udayāditya's
  accession…"; "The chronology complicates it" given its referent.

**Apparatus.** An `[UNVERIFIED]` endnote now identifies the *flagged claim* from the flag's own
text, not the sourced sentence preceding it — note 4 previously read as though the sourced
six-feet detail were unverified.

3,852 words, 0 findings, 39 chunks, 79 endnotes.

## 2026-09-26 — C1 typography: section rules and small-caps lead-ins

- §1.2's five regimes are now separated by a short centred rule (`---` in the master, rendered as a
  paragraph bottom border indented 3600 DXA either side — never a table, per the docx rules).
  The marker is in the master so the reading copy carries it too.
- Each section opens with its first few words in small caps, the way a printed book sets a section
  opener: AT THE TOP…, WALK OUT OF…, UDAYPUR LOOKS…, UDAYĀDITYA DID…, THE TEMPLE'S DATES…
  `leadInRuns()` applies it to the first body paragraph after each H2, and only in the chapter
  bodies — never in the note lists, where it would look like an error.
- Prose, sourcing and word count untouched: 3,927 words, 0 findings, 39 chunks, 79 endnotes.
  Both .docx verified structurally (5 rules, 5 lead-ins each); no LibreOffice on this machine, so
  they have not been visually proofed.

## 2026-09-28 — C1 draft-v12: line-edit, first-mention context, expansion

- **Job 0 found nothing to fix.** None of the reported merge artifacts ("windingclimbing",
  "closedshut…openedchanged", "sharines", "V,.S.", "the an iconic form", "Sher Khan (   )") exists
  in draft-v11, the reading copy, or the rendered .docx. The 40 KB `C1_Udaypur_chapter.docx` dated
  Sep 27 09:51 is a Word re-save of the Sep 26 render; a paragraph-level diff against
  `handoff/C1_chapter.md` shows the only difference is that `[ed]` markers were stripped. No
  content edits, no tracked changes, no comments. The artifacts are in some other copy.
- **Job 1.** Sentences over 40 words: 22 → 5, and the five that remain are doing cumulative work.
  253 → 261 sentences from the same material. Splitting orphaned 25 citations, which were restored
  by inheriting the marker from the split run rather than by hand.
- **Job 2.** §1.2 keeps the architectural description where it is but now signposts it — "Before the
  inventory goes on, the building itself is worth a pause, because everything that follows happened
  around it" — and closes it back into the sequence. The five regimes still run
  Paramāra → Sultanate → Mughal → Maratha → modern. §1.5 was re-broken one step per paragraph:
  question → the building's case → the circumstances → the chronologies → the counter-record →
  the manner of accession → what both share → the reconciliation → the settled sequence.
- **Job 3.** Identifications added from the KB: Jayasiṃha as Bhoja's successor
  (`singh-1984-bhoja-00111`); the Panhera inscription as a dated feudatory record naming Jayasiṃha
  as overlord, with Mandalika's capture of Kanha to show the relationship was real
  (`ganguly-paramara-00262/00263/00275`); Karṇa as the Cauḷukya king of Gujarat
  (`ganguly-paramara-00279/00274`); Mahadji Scindia, 1761–94, head of the Gwalior house and the
  towering military figure of northern India (`patil-composite-inscriptions-00038`); Sher Khan's
  mosque built under Ghiyasuddin Khalji of the Malwa Sultanate (`intach-2022-udaypur-00292`).
  **Sher Khan's own identity is flagged `[CONTEXT NEEDED]`** — the KB names him only as the builder.
- **Job 4.** 3,927 → 4,428 words (reading copy 4,497), from sentence-splitting, the Job 3 clauses,
  and dossier detail not previously used: the temple's three *mukhamaṇḍapas* and inscribed porch
  pillars (`patil-1952-00385`), the Moti Masjid's trabeated hall and nine-fish roof motif
  (`intach-2022-udaypur-00292`), the Purana Bazaar Darwaza (`intach-2022-udaypur-00208`), and the
  regional frame for the Sultanate layer — Iltutmish 1233, Alauddin Khalji 1293
  (`intach-2022-udaypur-00071`). Stopped at 4,428 rather than reach 5,000 by padding.
- `WORDS_MIN, WORDS_MAX` raised to 4,000–5,200 to match the new chapter budget.

## 2026-09-28 — C1 accessibility pass; the named .docx is now the clean chapter

- **Skill inventory checked.** Installed: `doc-coauthoring` (user) and the official Anthropic set —
  `docs`, `docx`, `pdf`, `pptx`, `xlsx`, `skill-creator`, `import-memory`, `morning`. None does
  grammar, readability or accessibility checking; there is no Grammarly equivalent. `docx` governs
  the Word output and was already loaded this session, so the readability work was done directly
  and measured rather than delegated.
- **Glosses on first use** — the real accessibility barrier. Eight technical terms went past a
  non-specialist unexplained: *śikhara* (now "the spire"), *liṅga* (the aniconic-form gloss moved
  from its second appearance to its first), *jālī* ("the perforated stone screens"), panchayat
  ("the elected council"), Nastaliq ("the Nastaliq script"), mihrab ("the arched niche in the
  western wall that marks the direction of prayer"), trabeated ("carried on posts and beams rather
  than arches"). All are definitional, none adds a historical claim.
- Two passives turned active where the agent is known ("Masons cut Sanskrit inscriptions…",
  "He dug the Udaysagar tank…"). Three long sentences split, including one the mihrab gloss had
  itself pushed to 47 words.
- Final: 266 sentences, mean 16.4 words, 4 over 40 (all deliberate), 4,467 words, 0 findings.
- **`C1_Udaypur_chapter.docx` is now the clean chapter** — no `[src:]`, no `[ed]`, no provenance
  table, endnotes as back matter, section rules and small-caps lead-ins intact. The marked version
  moved to `C1_Udaypur_chapter_editor.docx` so provenance is not lost.

## 2026-09-28 — C1 back matter: one full entry per work

- The notes were reprinting each book's full citation every time it was used — "D. R. Patil
  (Part I) + unattributed additions, *Archaeological & Cultural Heritage of Madhya Bharat: Shrines,
  Architecture, and Inscriptions*" appeared about twenty times. Back matter is now two lists:
  **Works cited**, where each of the 11 works appears once in full with every page cited from it,
  and **Notes**, where each note points to a work by short form.
- Short forms are derived, not hand-written: surname alone where it is unambiguous (Ganguly, Pande,
  Tiwari); surname plus the fewest leading title words that disambiguate where an author has two
  works (Patil, *Archaeological* / Patil, *Cultural*; Singh, *Bhoja* / Singh, *Serpentine*;
  INTACH, *Architectural* / INTACH, *Geo-Heritage*); both surnames for a compiled work
  (Shrivastav & Verma); the title alone where the author is unnamed (*Skanda-Purāṇa*).
  Title truncation refuses to stop on a stop-word, so no short form ends in "of" or "and".
- `render_docx.js` renders both lists into the clean .docx. The works-cited label is emitted plain
  rather than bold-inside-italic, which the inline markdown parser was mangling.
- 11 works, 11 unique titles, no duplicates; 96 notes unchanged in number and content.

## 2026-09-29 — BOOK_SOURCEBOOK.md + source_codes.md

- `build_sourcebook.py` generates both files deterministically from Chroma, `source_registry.yaml`
  and `chapters.yaml`, so the sourcebook can be rebuilt and diffed. 27 codes; 501 excerpts across
  17 sections; 102 sub-themes; 313 KB.
- Citations carry code · book · page · chunk id. Page gate: 253 citations give a real page, 179
  give `p. —` because the KB holds none, 68 give a section trail for the Samarāṅgaṇa, whose page
  numbers are known corrupt. No page is ever invented.
- Quotability gate: 21 entries appear as marked paraphrase rather than quotation.
- **Two defects found and fixed during the build, both worth knowing about:**
  1. `ai-derived` — six model-written synthesis chunks (`AI-0001`–`AI-0006`), marked
     `is_quotable: true` and bucketed into ten chapters. Excluded from the sourcebook and flagged
     in its preamble. **These should be re-flagged `is_quotable: false` in the KB or removed**:
     as they stand, any chapter pipeline can quote model-written text as a source.
  2. Ranking by primacy first put the Samarāṅgaṇa's siege-engine chapter at the top of C7's
     temple-sculpture sub-theme. Relevance to the chapter now carries 0.55 of the score, and
     primacy orders only what already belongs.
- A per-source cap of 4 excerpts per chapter stops one large book crowding out the shelf: `SAM`
  fell from 118 excerpts to 68, and sources that had 1 each (Hardy, Adhikari, Deva) now show
  where they actually bear.

## 2026-09-29 — ai-derived chunks re-flagged not quotable

- **Root cause.** `build_chroma.py` derived `is_quotable` by excluding the tags `llm_regenerated`
  and `needs_recheck`. The six synthesis chunks carry the tag **`ai_derived`** (and
  `origin = "AI-derived"`), which was not on the list — a tag-name mismatch, so model-written text
  shipped as quotable into ten chapter buckets.
- **Fix, both layers.** The rule now also excludes `ai_derived` and any row whose `origin` is
  "AI-derived", so a rebuild cannot restore the flag. The six live rows in the Chroma store were
  updated in place: `is_quotable: false`, with `quarantine_reason` set to "model-written synthesis
  — not a source; never quote".
- **Reversible.** `kb_audit/ai_derived_pre_requote_backup.json` holds the full prior metadata and
  documents for those six rows (15 KB). No full store backup was taken: the change touches six
  rows and one boolean, and the dump reverses it exactly.
- **Verified.** 0 of 6 remain quotable; 14,110 chunks quotable overall. `is_quotable` has no
  column in `kb3/kb_active.sqlite` — it is derived only at Chroma build time, so those two places
  are the whole surface.
- No downstream damage: no `AI-*` chunk is in the C1 dossier, and C1 re-verifies at 4,467 words,
  0 findings. `BOOK_SOURCEBOOK.md` rebuilt; its preamble now records the fix rather than
  recommending it.

## 2026-09-29 — ai-derived chunks archived and removed from retrieval

- Setting `is_archived: true` alone would not have hidden them: the archive is a **separate
  collection**, and `load_bucket` filters on `in_<chapter>`, not on the flag. Archiving inside the
  active collection would have left them fully retrievable.
- So all three were done. The six rows now carry `is_archived: true`, `is_quotable: false`, empty
  `chapter_buckets`, every `in_<chapter>` false and every `rel_<chapter>` zero. Verified: **0
  ai-derived rows reachable through any of the 17 chapter buckets.**
- `build_chroma.py` reproduces this from source: anything with `origin = "AI-derived"` or the
  `ai_derived` tag is forced archived, gets no buckets and no `admitted_` flags.
- `chapter_pipeline.load_bucket` now filters `is_archived: false` in the Chroma query and skips
  archived rows again in the loop — the flag is authoritative even if a bucket is stale.
- Restore point unchanged: `kb_audit/ai_derived_pre_requote_backup.json` holds the pristine
  pre-change metadata for all six rows.
- Re-checked: C8 loads 2,150 rows with 0 archived and 0 ai-derived; C1 verifies at 4,467 words,
  0 findings; `BOOK_SOURCEBOOK.md` rebuilds identically at 500 excerpts.

## 2026-10-01 — Sourcebook v2: key-fact summaries, codes written back to the registry

- `source_registry.yaml` now carries a `code:` field on all 27 sources, inserted line-wise so the
  file's 41 comment lines and explanatory header survive (a yaml round-trip would have deleted
  them). No duplicate codes.
- Each chapter now opens with **Key facts the KB establishes** — 322 lines across 17 sections,
  each condensed from a cited passage (never composed) and tagged `[established]` 31,
  `[single-source]` 273, `[gap]` 16, `[unverified]` 2, `[contested]` 0.
- Excerpts capped to ~24 per chapter (6 sub-themes x 4, max 4 per source): 405 excerpts, 14 of
  them quotability-gated into marked paraphrase.
- **Three detector defects found and fixed while building:**
  1. Corroboration matched only near-identical wording, so 91% of facts came out
     `[single-source]`. Matching now also fires on a shared date plus three shared rare terms;
     `[established]` rose from 10 to 31.
  2. `[contested]` fired on books merely citing *different* years — a 1988 imprint against a 1981
     one. It now requires each side to commit to at most two years with no overlap.
  3. The bibliography filter meant to stop that was written through a shell heredoc, which turned
     its `` escapes into literal backspace bytes (``), so the pattern could never match —
     the same failure that corrupted `ABBREV` in `chapter_pipeline.py` earlier. Rewritten from a
     file; the builder is now checked to contain no backspace bytes.
- **Known limit, stated rather than tuned away:** the contested detector finds no numeric
  conflicts. The real one this project already knows about — Udayāditya's accession, 1058–1087 vs
  1059–1086 vs c.1059–93 vs 1070–1093 — is not caught, because those spans sit in sentences that
  share too little wording to group. Treat the count as a floor, not a census; `chapters/C1`
  must-resolve remains the record of that dispute.

## 2026-10-01 — Curated facts + a navigable sourcebook

- New `curated_facts.yaml`: hand-verified facts the extractor cannot see, merged into the chapter
  Key-facts lists and marked `[curated]`. **Every chunk id in it is validated against the KB at
  build time and the build stops if one does not resolve** — a curated fact with a dead citation
  would be worse than no fact at all.
- The **Udayāditya accession dispute** is now in it, placed in C1, C5 and C6: four competing spans
  (1058–1087 `PAT-CH`; 1059–1086 `GAN`; c. 1059–93 `INT-ARC`; 1070–1093 from the coinage
  `INT-ARC`), the Panhera counter-evidence, and a note that the usual reconciliation is labelled
  speculation in the KB and must not be asserted as settled.
- Readability: a **Contents table** (chapter, chunks, sources, key facts, excerpts, and a "watch"
  column flagging thin coverage), anchored headings, a back-to-contents link on every section, and
  links to the code table and coverage matrix. All 36 internal links verified to resolve.
- Three more extraction defects fixed: the sentence splitter cut inside "A. D." and produced
  fragments ending "…1215, A." (the ABBREV problem again, now handled by protecting abbreviation
  dots); author-year citations such as "(Trivedi 1978, 1989)" were being promoted to facts; and
  source table rows were being read as sentences. 0 of each remain.
- Final: 347 key facts (`[single-source]` 291, `[established]` 30, `[gap]` 17, `[contested]` 5,
  `[unverified]` 4), 405 excerpts, 14 quotability-gated, 327 KB.

## 2026-10-01 — BOOK_SOURCEBOOK.docx for circulation

- New `render_sourcebook_docx.js` renders the whole sourcebook to Word from the same markdown,
  so the .docx can never drift from the generated source: rebuild, re-render.
- Laid out for a reader who did not build it: **each chapter starts on its own page** (17 page
  breaks), Title/H1/H2 use built-in Word heading styles so the navigation pane and any TOC work,
  excerpts are indented with a grey left rule, citation lines are smaller and grey beneath them,
  and source codes and status markers are set in a monospace accent so they read as tags.
- Three real Word tables: Contents (18x7), source codes (28x4) and the coverage matrix (25x19).
  The matrix sits in a **second, landscape section** because nineteen columns do not fit portrait.
- Running header and page-numbered footer throughout.
- 195 KB, 2,038 paragraphs, 325 bullets; diacritics and Devanagari preserved; no markdown link
  syntax leaked into the text. Verified structurally — there is no LibreOffice on this machine,
  so it has not been visually proofed.

## 2026-10-01 — Sourcebook .docx compacted to ~36 pages

- `render_sourcebook_docx.js` rewritten for density: 9pt body / 8pt citations, tightened line
  spacing, **two-column chapter section**, and the per-chapter page break dropped (17 page breaks
  were costing up to half a page each). Front matter stays single-column for its tables; the
  19-column coverage matrix stays in its own landscape section.
- **Nothing load-bearing was cut.** All 347 key facts, all 17 coverage summaries, all 17 gaps
  notes, the full source-code table and every matrix cell are present. What is capped is the
  excerpt pool — 204 of 403, up to 12 per chapter, chosen by the same ranking — and the document
  states that on its first page with a pointer to the complete set in `BOOK_SOURCEBOOK.md`.
- **The page count is calculated, not observed.** There is no LibreOffice, pandoc or pdftoppm on
  this machine and docx-js does not populate `docProps/app.xml`, so pagination cannot be measured
  here. The renderer carries a line-budget estimator (66 lines/column, 54 chars/line at two
  columns) and prints its working: front 1.3 + chapters 33.7 + matrix 0.6 = **35.7 pages**. The
  excerpt cap was tuned against it — 8/chapter gave 29.7, 13 gave 37.2, 12 gave 35.7.
- The cap is the first CLI argument, so the length is re-tunable in one run:
  `node render_sourcebook_docx.js 10`.

## 2026-10-04 — The sourcebook becomes an input to chapter drafting

- `build_sourcebook.py` now also writes **`kb3/sourcebook_facts.json`** — per chapter: the key
  facts with status, codes and chunk ids, the coverage stats, the dominant source and the gaps,
  plus the project-wide code map. The pipeline reads this, never the markdown, so prose and data
  cannot drift.
- **`brief`** gained a "What the sourcebook already establishes for this chapter" block: facts
  grouped by status, each headed by the prose treatment that status demands, then the chapter's
  gaps, then a single-source warning where one book supplies over 45% of the bucket.
- **`verify`** gained two checks, both tested against a deliberately broken draft:
  `contested-flattened` (a draft giving one of a contested fact's competing values with no second
  value and no hedge in that paragraph) and `unverified-unflagged` (citing an unverified fact's
  evidence with no `[UNVERIFIED — …]` anywhere). The contested check matches on the **year span**,
  because a value may be dressed as "1070–1093 (from the coinage)", which no sentence contains.
- **`handoff`** prints each work's source code beside it, so chapter apparatus and sourcebook
  share one citation scheme.
- `STYLE_GUIDE.md` §11 states the status → prose mapping as a book-wide rule; `PIPELINE_README.md`
  documents the new input and the order of operations.
- Two more fact-quality filters: figure/plate captions and any parenthetical ending in a year were
  reaching the key-facts list and therefore the drafting brief. 0 of either remain.

**Known mismatch, not introduced here:** `brief` parses outlines written as `### Section N`, but
`chapters/C1/outline.md` is hand-written as `## 1.1 Arrival`, so C1 cannot drive `brief`. C1 was
drafted before the brief stage existed. Later chapters should take their outline from the
`outline` command, or `brief` needs a second parser.

## 2026-10-04 — brief now parses both outline formats

- `brief` understood only '### Section N Title', the form its own `outline` command writes, so
  C1 — whose outline was hand-written as '## 1.1 Arrival (~900 w) — Tiwari + INTACH' — could not
  drive the stage meant to draft it.
- New `outline_sections()` takes any `##`–`####` heading, keys a section by its number where it
  has one, and skips headings that are apparatus rather than sections (`NOT_A_SECTION`: drafting
  order, budgets, sources, evidence, coverage, gaps, contents, rules, appendix, notes). C1 yields
  five draftable sections and correctly drops "Drafting order and budgets".
- `resolve_section()` accepts three ways of naming one: its own number (`1.1`), its position in
  the outline (`1`), or a unique word from its name (`stance`). A name match must be unambiguous.
  A failed lookup now lists what is actually in the outline instead of "not in outline.md".
- `section_stem()` fixes the filename crash: `int("1.1")` raised ValueError, so a dotted section
  could not be written at all. Stems are now `1_1`, `02`, or a slug of the name.
- Backticks in an outline also hold filenames (`research.md`), so evidence ids are filtered
  against the dossier and de-duplicated before the brief counts them.
- Verified both ways: `brief C1 1.1` produces a brief with 7 evidence chunks, the sourcebook block
  and the contested accession fact; `brief C1 stance` resolves by name; `### Section N` still
  parses and still stems to `02`.
- The test briefs were generated under a temporary approval and then deleted, and `state.json` was
  restored: `approved_outline` for C1 is still `None`. Run `approve C1 outline` before drafting.

## 2026-10-05 — new stage: assemble

- There was nothing between `brief` (per-section) and `verify` (whole draft): sections had to be
  pasted together by hand, which is where marker loss and heading drift come from.
  `python chapter_pipeline.py assemble C1` now builds the next `draft-vN.md` from
  `sections/<stem>.md`, in outline order.
- Behaviour:
  * **Refuses an incomplete chapter by default**, naming every missing or empty file. `--partial`
    assembles what exists and writes a visible `` `[GAP: section not yet written — …]` `` for each
    absent section, which `verify` already counts.
  * **The writer's own heading wins.** If a section file opens with its own `##`, that is kept; the
    draft keeps "1.1 Through the Back Door: An Arrival at Udaypur" rather than reverting to the
    outline's working label. Where a file has no heading, one is synthesised from the outline with
    the word budget and the source hint stripped ("1.1 Arrival (~900 w) — Tiwari + INTACH" →
    "## 1.1 Arrival").
  * Takes the chapter title from the previous draft's first line, falling back to `chapters.yaml`.
  * Picks the next version **numerically**, never clobbering an existing draft; records
    `assembled_from` in `state.json`.
  * Output is NFC-normalised, so the encoding gate cannot fail on assembly alone.
- Tested on real marked prose, not a stub: C1's own §1.1 as a section file assembled to
  `draft-v13.md` with all 29 `[src:]` markers and both `[ed]` markers intact, 4 gap placeholders,
  and `verify` then reporting exactly one finding — the length gate at 735 of 4,000–5,200.
- Test artifacts removed afterwards (`draft-v13.md`, `sections/1_1.md`): a partial draft left in
  place would have become the newest draft and hijacked `verify` and `handoff` for the finished
  chapter. `draft-v12.md` is current again at 4,467 words, 0 findings.

## 2026-10-05 — the two risks flagged with `assemble`, closed

**1. A half-written chapter could be approved and handed off.** `approve <cid> draft` only checked
that `qa_review.md` existed. It now refuses, naming each objection, when:

* the last `verify` ran on a draft other than the newest on disk (stale approval);
* that `verify` left findings unfixed;
* the draft still carries `[GAP: …]` placeholders from `assemble --partial`.

`--force` overrides, prints what it is overriding, and sets `approved_draft_forced` in state so the
override is on the record. All four paths were tested against a real partial assembly: clean draft
approves; stale verify, findings and gaps each refuse; `--force` approves with warnings.

Found while testing: `assemble` was writing `draft=` into state, the same key `verify` uses to
record what it checked, which silently defeated the stale-verify guard. It now writes
`assembled_draft=`.

**2. Nothing caught a dispatch to a function that did not exist.** New `test_pipeline.py`, 36
checks: every subcommand dispatched, every dispatched handler present, no compiled regex carrying a
literal backspace (the ``-eaten-by-heredoc failure, which has happened three times here), both
outline formats parsing and resolving, `assemble` preserving `[src:]` and `[ed]`, every sourcebook
status having a prose rule, and curated chunk ids resolving. Writes only to a temp folder.

The test was mutation-checked rather than assumed: re-pointing the assemble dispatch at
`cmd_assemble_typo` makes it exit 1 with `FAIL cmd_assemble_typo exists`, and the file was restored
immediately afterwards.

C1 is back to its real state throughout: `draft-v12.md`, 4,467 words, 0 findings, approved without
force; test artifacts and test state keys removed.

## 2026-10-05 — retrieve C2, and the relevance defect it exposed

- `retrieve C2` ran, but the result was wrong for the chapter. C2 is "The Betwa Valley: Land,
  Rivers and Seasons"; the dossier led with 14 chunks of the Samarāṅgaṇa-sūtradhāra (an
  architectural treatise, mean `rel_C2` 0.39) and gave 4 each to the two Betwa hydrology and
  climate papers (mean `rel_C2` 0.82 and 0.72). Six of eight sub-themes were off-topic.
- **Cause:** `quality()` weighted claim credibility 0.35 and primacy 0.25 against chapter relevance
  0.20. Primacy is a property of the book; relevance is the only score that knows what the chapter
  is about. Re-weighted to relevance 0.45, credibility 0.25, reliability 0.20, primacy 0.10 — the
  same defect, and the same fix, as in `build_sourcebook.py`, but this one feeds drafting.
- Re-weighting alone moved mean relevance 0.548 → 0.594 only, because the dossier is built per
  sub-theme and the clusters form from the whole bucket — 43% of which is that one treatise. Added
  `--rel-floor`, which filters before clustering. C2 at 0.53: mean relevance **0.730**, Samarāṅgaṇa
  14 → 6, Betwa science 8 → **20**, and the sub-themes become catchment/streamflow, stations/trend,
  climatic parameters, plateau/Malwa.
- **The floor defaults to OFF, deliberately.** Checked against the finished chapter: **38 of the 47
  chunks C1 actually cites** — the porch inscriptions, Tiwari's lane, the census returns — score
  below 0.5 on `rel_C1`. A silent floor would have denied that chapter most of its evidence, and
  re-running `retrieve C1` under one would orphan those citations and make `verify` report them as
  fabricated. **Do not re-retrieve a finished chapter.**
- Instead `retrieve` now diagnoses the bucket and recommends a floor only when one source supplies
  over 25% at no better than median relevance:
  `NOTE samarangana supplies 43% of this bucket at mean relevance 0.39, against a bucket median of
  0.38 … consider: retrieve C2 --rel-floor 0.53`
- C2 now stands at 83 chunks, mean `rel_C2` 0.730, 19 sources, ready for the outline gate.

**Process note:** two patch scripts aborted mid-way on stale anchors, wrote nothing, and left
hand-edits referring to variables that did not exist — once producing a `NameError` only caught by
running the command. The smoke test checks dispatch, regexes and parsing, not names inside function
bodies. Patches to `chapter_pipeline.py` now verify by importing the module and inspecting the
changed function before claiming success.

## 2026-10-05 — kb_inventory.py: verify the books against the vectors

- New `kb_inventory.py` reconciles the books folder, `source_registry.yaml`, `kb_active.sqlite` and
  the Chroma collection, and checks the vectors themselves rather than trusting metadata rows:
  embedding dimension, and whether any sampled vector is all-zero or non-finite. `--deep` checks
  every embedding; `--html` writes a self-contained, filterable, sortable page; `--json` dumps the
  same data. Exit 1 on any problem so it can gate a rebuild.
- **Result: all 27 books verified.** 27 files on disk, 27 registry entries, a 1:1 match, every
  source carrying vectors at 384 dimensions, none degenerate.
- The five apparent shortfalls were diagnosed rather than reported as damage: ADH 48, GAN 3, SAM 2,
  SIN-T 1, TIW-H 1 fewer vectors than store rows, which matches the count of **duplicate
  content hashes exactly** in each case. The builder keeps one vector per distinct passage, so this
  is de-duplication working. ADH repeating 48 passages is worth a look at the source file, but it
  is not a KB fault.
- `ai-derived` (6 chunks) is reported as present in Chroma but absent from the registry, which is
  correct — it is the archived model-written synthesis, not a book.
- Negative-tested: hiding `Betwa_Streamflow.md` makes BET-K report "file missing from the books
  folder" and the command exit 1; restoring it returns 27 of 27 and exit 0.
