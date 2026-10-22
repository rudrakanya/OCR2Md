# Udaypur Book — Reference Sources and Evidence Document

**Status: Parts A–F complete** (all 13 chapter dossiers, the cross-chapter
index, the 29-source coverage matrix, and the completeness report). See
`docs/sourcebook_rebuild_checklist.md` for the build log. This document
still carries explicit, named gaps (Part F) rather than claiming coverage
it does not have — a complete rebuild is not the same thing as an
exhaustive one, and the two are kept distinct throughout.

A full, byte-for-byte copy of the previous version of this document (the kb3
build, dated 2026-09-24) is preserved at
`docs/legacy_kb3_sourcebook_2026-09-24.md`. Nothing from that build has been
deleted; it is being read, re-verified against the live corpus, and folded into
the new chapter-by-chapter structure below as each chapter is completed.

---

## Part A — Purpose, methodology, and coverage status

### A.1 Purpose

This document is the book's research index: for every chapter in the current
outline, what the available source corpus can establish, where sources agree
or disagree, where the evidence runs out, and exactly how to find and re-check
every fact or quotation cited here. It is not a drafting document and contains
no chapter prose — it gathers and cites.

### A.2 Authoritative chapter list

`chapters.md`, read in full, current working-tree version (12 chapters +
Afterword). This document does **not** use the older 18/19-chapter scheme in
`chapters.yaml`, nor the 17-section scheme the previous (kb3) build used —
both are mapped forward into the current structure; see A.5.

### A.3 Which corpus and database were examined

Three retrieval systems exist in this project. Only one is being used going
forward, by the user's explicit decision (2026-10-10):

| System | What it is | Status |
|---|---|---|
| Root-level `kb/` (SQLite FTS5, `kb_search.py`/`build_kb.py`/`entities.py`) | The original "v2 RAG pipeline" (commit `949cc86`) — full-text search, no vector DB | Not used for this document |
| `kb3/` (`build_chroma.py`, `stage2_build.py`, `kb3_embed.py`) | A third, later knowledge base: 14,702 active + 4,730 quarantined chunks, dense dedup, contested-claims register, epistemic-status tagging. Produced `BOOK_SOURCEBOOK.md`, `source_codes.md`, and the previous version of this document. | **Frozen.** Its backing store (`kb3/kb_active.sqlite`, `kb3/chroma/`) does not exist on disk — only its hand-edited YAML control files and its three Markdown outputs survive. Not being rebuilt for this task (would require re-embedding ~19,000 chunks — a cost/time operation outside this task's authorization). Its existing output is treated as a dated, citable prior layer, re-verified against raw source text where practical. |
| `chroma_db/udaypur_corpus_openai_large` (`src/` pipeline) | 5,862 chunks, 26 source files, `text-embedding-3-large` (3072-dim). Live, already audited across this project's history (hybrid dense+BM25 retrieval, passage-level and book-level evaluation benchmarks). | **The live retrieval engine used for all new searching in this rebuild.** |

### A.4 How source files were matched to catalogue entries

Every source identity claim in Part B was established by at least one of:
direct reading of the file's own title page / front matter; a unique
identifier match (e.g. a DOI, identical across two differently-named files);
or `books_manifest.yaml`'s own evidenced entries (each of which cites the
exact text it was read from). Title or filename similarity alone was never
treated as sufficient — see the Phase B1 reconciliation this document builds
on, summarized in Part B.

### A.5 Chapter crosswalk

kb3's bucket scheme (C1–C16 + AF) already merged some of the older 19-way
chapters (`chapters.yaml`), and the current `chapters.md` merges and splits
again. The full derived mapping is kept in
`docs/sourcebook_rebuild_checklist.md` and is reproduced in Part D once all
chapters are built. Three of the thirteen new sections require judgment, not
mechanical relabeling, because a single kb3 bucket's content needs to be
split across two new chapters:

- kb3's C1 bucket mixes old-C01 ("a small town with a long memory") and
  old-C04 ("prehistory and early Vidisha") content — these separate into new
  **Ch1** and new **Ch3** respectively.
- kb3's C4 bucket ("From Avanti to Malwa") mixes "background" material that
  belongs in new **Ch3** with "remaining C05" material that belongs in new
  **Ch4**.
- kb3's AF (Afterword) bucket mixes conservation-history material that
  belongs in new **Ch11** with forward-looking material that stays in the new
  **Afterword**.

The other ten sections map cleanly

### A.9 Citation style (MLA, with technical traceability kept alongside)

Every quotation and evidence item is cited two ways at once, per the user's
instruction (2026-10-10):

1. **MLA in-text citation** immediately after the quotation —
   `(Author Page)`, or `(Author, Short Title Page)` where a source has more
   than one work in this document's inventory (e.g. the two INTACH surveys).
   A **Works Cited** list, in standard MLA format, accumulates in **Part
   B.5** as each chapter's sources are actually cited — it is not
   front-loaded for all 29 sources at once, since several entries (author,
   publisher, exact year) are only partly established and a fabricated MLA
   entry would be worse than a visibly incomplete one.
2. **A bracketed technical trace**, immediately following the MLA citation,
   carrying what MLA does not: `[File: `filename.md`; sec. "heading path";
   OCR page marker N — printed-page status unconfirmed]` (or the specific
   caveat that applies, e.g. "heading/page not yet located — grep hit only").
   This is the part that lets any claim be re-found and re-checked in the
   live corpus; it is kept in full even though it sits outside MLA
   convention, per this document's own fidelity requirements (Part A.7–A.8).

Where a source's author is not established (several files carry no named
author in their own front matter — see Part B), the Works Cited entry uses
the organization or the kb3/manifest-recorded title as the alphabetizing key,
per MLA's own rule for anonymous/corporate works, and this is stated
explicitly rather than inventing an author. (new Ch2/Ch5/Ch6/Ch7/Ch8/Ch9/Ch10/Ch12 each
correspond to one kb3 bucket or a clean merge of two).

### A.6 How retrieval and full-source examination are conducted

For each chapter: (1) derive research questions and search terms from the
chapter's own text in `chapters.md`; (2) run multiple queries — English and,
where a source is Hindi/Sanskrit, the equivalent terms — against the live
`src/` hybrid retriever; (3) read the corresponding kb3-era content (legacy
document + `BOOK_SOURCEBOOK.md` + `claims_register.yaml` +
`derived_inferences.yaml`) for the matching old bucket(s); (4) re-verify every
carried-forward excerpt against the current corpus file's raw text directly,
since several kb3 source files are not in the active 26-file corpus (Part B);
(5) read full sections of sources with heavy chapter priors rather than
relying on top-k snippets alone; (6) record what was searched and what
remains unexamined.

### A.7 Evidence categories and confidence levels

Adopted directly from the task brief, applied consistently:

- **Direct Udaypur evidence** — explicitly about Udaypur, its monuments,
  people, inscriptions, or landscape.
- **Regional/comparative evidence** — about a wider region, comparable
  monuments or dynasties, used for context or comparison.
- **General contextual evidence** — background or conceptual framing.
- **Potential/unverified connection** — relevance suspected, not established.
- **Contradictory/qualifying evidence** — complicates or limits another claim.

kb3's own reliability scale (0.90 standard scholarly / 0.80 sound specialist /
0.70 competent-but-dated / 0.60 non-specialist or advocacy / 0.40 weak venue /
0.30 out-of-scope) is carried forward in Part B as a source-level prior, kept
separate from per-passage evidence classification — a weak source can still
carry a strong, directly-relevant passage, and a strong source can carry a
passage that is only tangential.

### A.8 How completeness is assessed, and what could not be examined

Completeness is tracked per-chapter and per-source in
`docs/sourcebook_rebuild_checklist.md`, updated as each chapter dossier is
completed. As of this revision: **Part A and B are complete; Part C has not
yet been built for any chapter.** This is stated here so that no later reader
mistakes an in-progress document for a finished one. The single largest known
constraint: kb3's own `kb3/retrieval.yaml` measured that `SAM` (the
Samarāṅgaṇa-sūtradhāra) supplies 26–38% of every chapter's candidate chunks by
sheer volume (1,210 chunks, the largest single source) — any chapter's
evidence must be checked for over-reliance on this one source before being
called balanced.

---

## Part B — Complete source inventory and reconciliation

### B.1 Status overview

27 source identities are tracked (kb3's `source_codes.md` count — one more
than the 26-row catalogue, because of `RAJM`, found only in kb3's own records
and in the legacy corpus directory, never catalogued in
`Udaipur Books List - Sheet2.csv` at all).

| Status | Count | Meaning |
|---|---:|---|
| Indexed in `udaypur_corpus_openai_large` now | 20 | Confirmed present via live ChromaDB query (Phase A/B1 of this project) |
| Physically on disk (legacy directory) but **not** in the active corpus or ChromaDB | 6 | `bhoja-paramara-and-his-times.md`, `Jagta_Hua_Kasba_OCR_text.md` (Hindi original), `patanjala-yogasutra-rajamartanda-bhoja.md` (RAJM), `samarangana-sutradhara.md` (single-file form — active corpus instead holds a 2-volume split), `madhya-bharat-inscriptions-and-shrines.md` and `madhya-bharat-temples-and-architecture.md` (Patil composites) |
| Confirmed deleted from disk | 1 | `udayesvara-temple-art-architecture.md` — a third, now-gone Anupa Pande OCR copy; 25 orphan chunks remain only in the old root `kb/store.sqlite`, not in ChromaDB |

### B.2 Master inventory

Columns: **kb3 code** (as used in the legacy document and `BOOK_SOURCEBOOK.md`)
· **Title / author** (as kb3 and the manifest record it) · **Active corpus
file** (exact filename in `Udaipur Books Markdown files/`, or "—" if none) ·
**ChromaDB status** · **Catalogue row** (from `Udaipur Books List -
Sheet2.csv`, exact title, or "not catalogued") · **kb3 reliability** ·
**Notes / unresolved items**.

| Code | Title / author | Active corpus file | ChromaDB (`udaypur_corpus_openai_large`) | Catalogue row | Reliability | Notes |
|---|---|---|---|---|---|---|
| SKP-13 | The Skanda-Purāṇa, Part XIII | `467921465-Skanda-Purana-13-AITM.md` | Present | "The Skanda-Purāṇa, Part XIII" | 0.80 | Exact match, no issues |
| HAR | The Temple Architecture of India, Adam Hardy | `806955603-The-Temple-Architecture-of-India-Adam-Hardy.md` | Present | "The Temple Architecture of India" | 0.90 | Exact match |
| BET-K | Streamflow of the Betwa River, Amit Kumar et al. | `Streamflow of the Betwa Rive.md` | Present | "Streamflow of the Betwa River" | 0.80 | Exact match |
| SIN-B | Bhoja Paramara and His Times, Mahesh Singh (1984) | **none** | **Absent** | "Bhoja Paramara and His Times" | 0.70 | Confirmed Phase B1: file exists only at `Udaypur Reference Markdown Files\bhoja-paramara-and-his-times.md`, not in the active corpus. kb3's own note: "the only source... that calls Udayāditya Bhoja's nephew" — flagged `contradicted` by primary epigraphy in `claims_register.yaml` K1. Since this source is unindexed, every kb3 fact attributed to it needs direct re-reading from the legacy file, not retrieval. |
| BHJ-H | भोजदेव (Bhojadeva) | `bhojdev.md` | Present | "भोजदेव (Bhojadeva)" | 0.60 | Exact match; author unnamed in file (catalogue lists publisher "Rajkamal Prakashan" in the author field — a catalogue data-quality note, not a matching problem) |
| INT-GEO | Geo-Heritage of Udaypur: The Third Eye | `Geo-Heritage of Udaypur The Third Eye.md` | Present | "Geo-Heritage of Udaypur: The Third Eye" | 0.80 | Exact match |
| GUP | Iconography of the Hindus, Buddhists and Jains, R. S. Gupte | `iconography of hindus, buddhists and jains Gupte.md` | Present | "Iconography of the Hindus, Buddhists and Jains" | 0.70 | Exact match |
| INT-ARC | Intach Udaypur (The Architectural Splendor of Udaypur) | `Intach Udaypur (1).md` | Present | "Intach Udaypur" | 0.75 | Exact match |
| TIW-E | Jagta Hua Kasba — English translation | `Jagta_Hua_Kasba_EN.md` | Present | "Jagta Hua Kasba / कथा उदयपुर — English translation" | 0.60 | Exact match |
| TIW-H | कथा उदयपुर (Jagta Hua Kasba) — Hindi original | **none** | **Absent** | "कथा उदयपुर (Jagta Hua Kasba) — Hindi original" | 0.60 | Confirmed Phase B1: exists only at `Udaypur Reference Markdown Files\Jagta_Hua_Kasba_OCR_text.md`. Do not substitute the English translation when this code is cited — kb3 itself treats them as the same `work_id` for corroboration counting but a different code for quotation, exactly because only the original is canonical for Hindi quotation. |
| BET-S | Long-term historic changes in climatic variables of Betwa Basin | `Long-termhistoricchangesinclimaticvariablesofBetwa.md` | Present | "Long-term historic changes..." | 0.80 | Exact match |
| PAT-CH | The Cultural Heritage of Madhya Bharat, D. R. Patil | `The cultural heritage of madhya bharat.md` | Present | "The Cultural Heritage of Madhya Bharat" | 0.80 | Exact match |
| GAN | History of the Paramāra Dynasty, D. C. Ganguly | `History of Paramara Dynasty DC Ganguly.md` | Present | "History of the Paramāra Dynasty" | 0.90 | Exact match. A second, differently-OCR'd legacy copy (`paramara-dynasty-comprehensive-history.md`) also exists but is not in the active corpus — manifest already documents this as the same 1933 work under two OCR passes. |
| PAR | History of the Parmar Rajput Dynasty (kb3: "Paramara Rajput Dynasty Origins") | `History of the Parmar Rajput Dynasty.md` | Present | "Paramara Rajput Dynasty Origins" | 0.40 | Confirmed Phase B1 by **DOI match** (`10.5281/zenodo.17896750`, identical in both the active file and the legacy-directory copy `parmar-rajput-dynasty-origins.md`): same article, author Dr. Pratapsinh Ranaji Venziya. kb3's low 0.40 reliability score ("presents the agnikula myth as validated history") should be retained in the new document. |
| RAJ-E | King Bhoj and Paramara-period Town Architecture (EN), Bhagwatilal Rajpurohit | `Raja_Bhoj_Aur_Parmarkaleen_EN.md` | Present | "Raja Bhoj aur Paramkaleen (EN translation)" | 0.65 | Exact match. Manifest flags the source PDF as possibly bundling a second, distinct work — unresolved, not re-checked this pass. |
| SAM | Samarāṅgaṇa-sūtradhāra | **split**: `Samarangan Vol 2 (a)_combined.md` + `Samrangana Sutradhar Vol 1.md` | Present (both) | "Samarāṅgaṇa-sūtradhāra" | 0.75 | **Unresolved identity question.** kb3's `samarangana` source_id was built from a *single* legacy file (`samarangana-sutradhara.md`, 1.42M chars) that is not in the active corpus. The active corpus instead holds the work split into two differently-OCR'd volume files. kb3's SAM-coded excerpts cannot be assumed to exist verbatim in either active file without a direct re-check — flagged for chapter-level verification, since SAM supplies 26–38% of every kb3 chapter bucket (`kb3/retrieval.yaml`) and is the single highest-volume source in the whole project. |
| SIN-S | A serpentine scimitar of letters from Udaypur, Saarthak Singh | `A_serpentine_scimitar_of_letters_from_Ud.md` | Present | "A serpentine scimitar of letters from Udaypur" | 0.90 | Probable match (same subject, same author surname) to kb3's legacy-only `serpentine-scimitar-inscription-udaypur.md` — filenames differ; not yet confirmed byte-for-byte identical. To be verified when Ch6 (Inscriptions) is built. |
| ADH | Some Paramāra Temples From Madhya Pradesh, Swati Mondal Adhikari | `Some Paramara Templess.md` | Present | "Some Paramāra Temples From Madhya Pradesh" | 0.75 | Exact match |
| PAT-INS | Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture and Inscriptions (Patil composite) | **none** | **Absent** | not separately catalogued (catalogue's "Inscriptions of the Paramaras" row is a *different* work — see `Inscriptions Corpus.md` below) | 0.65 | Confirmed absent from the active corpus — legacy-only (`madhya-bharat-inscriptions-and-shrines.md`). kb3 flags this file as a composite that duplicates `patil-1952` in its Part I. Every kb3 fact coded `PAT-INS` (several appear in the old C1 bucket, e.g. the Besnagar Heliodoros pillar, the Lohangi Rock) needs re-sourcing from an active-corpus file or re-verifying against the legacy file directly, since it cannot currently be retrieved live. |
| PAT-TEM | The Cultural Heritage of Madhya Bharat — temples and architecture (Patil + Adhikari composite) | **none** | **Absent** | not separately catalogued | 0.65 | Same situation as PAT-INS: legacy-only (`madhya-bharat-temples-and-architecture.md`), a composite that bundles the whole of `Some Paramara Templess.md` (ADH) inside it. Facts coded `PAT-TEM` should be re-attributed to `PAT-CH` and/or `ADH`, both of which **are** active, rather than treated as a third independent witness. |
| SIN-T | Temple Economics: Arthvyavstha of Mandir, Sandeep Singh | `Temple Economics.md` | Present | "Temple Economics: Arthvyavstha of Mandir (Vol. I)" | 0.30 | Exact match. **Research-use policy (user-confirmed, Phase B1):** general-context eligible; never direct Udaypur evidence unless a specific retrieved passage says so. Full-text search of the active file found zero mentions of Udaypur/Udayeśvara under any spelling; one tangential mention of a different site (Besnagar, same modern district) at a much earlier period. kb3 independently reached the same conclusion ("does not discuss Udaypur... never cited as a Udaypur-specific claim"). |
| DEV | Temples of North India, Krishna Deva | `Temples of India.md` | Present | "Temples of North India" | 0.85 | **Unresolved title discrepancy**, carried over from Phase B1: the catalogue/manifest title is "Temples of North India" but the active file's own extracted H1 reads "Temples of India." Not yet confirmed as definitely the same book vs. two different Krishna-Deva-adjacent titles — to be checked directly when Ch5/Ch7-equivalent chapters are built. |
| KRAM-1 | The Hindu Temple, Volume I, Stella Kramrisch | `The Hindu Temple Vol 1 Stella Kramrisch.md` | Present | "The Hindu Temple, Volume I" | 0.90 | Exact match |
| KRAM-2 | The Hindu Temple, Volume II, Stella Kramrisch | `The Hindu Temple Vol 2.md` | Present | "The Hindu Temple, Volume II" | 0.90 | Exact match |
| PAN | The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta, Anupa Pande | **resolved this revision**: `The Udayesvara Temple - Anupa Pande.md` (209 chunks) | Present | "The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta" | 0.85 | Confirmed Phase B1 by direct content comparison that both active copies are duplicate OCR passes of the same monograph. **Resolved while building Ch5**: kb3's `pande-udayesvara`-coded excerpt (BOOK_SOURCEBOOK.md, "ARCHITECTURE AND SCULPTURE OF THE UDAYEŚVARA TEMPLE... Pl. 93. View of buttresses between the west latā and north latā of the garbhagṛha") matches `The Udayesvara Temple - Anupa Pande.md` verbatim at that file's own line 1624, and that file carries the exact running page-header "ARCHITECTURE AND SCULPTURE OF THE UDAYEŚVARA TEMPLE" (40 occurrences) that appears nowhere in the second copy. kb3's PAN citations are therefore traceable to this specific file, not the other active copy, which remains a separate, citable duplicate (Part B.2's duplicate-OCR note still applies — nothing here was merged or deleted). |
| GAZ-VID | Madhya Pradesh District Gazetteers: Vidisha | `Vidisha Gazeteer.md` | Present | "Madhya Pradesh District Gazetteers: Vidisha" | 0.70 | Probable match to kb3's legacy-only `vidisha-district-gazetteer.md` — both attributed to Shrivastav & Verma, 1979, per the manifest; filenames differ, byte-identity not yet confirmed. kb3 flags this source as 36% LLM-restated ("[cite: N]" markers) and **not quotable** in those sections — this caveat must carry forward regardless of which file is used. |
| RAJM | Pātañjala-Yogasūtram with the Rājamārtaṇḍa-vṛtti of Bhojadeva | **none** | **Absent** | **not catalogued at all** — missing from `Udaipur Books List - Sheet2.csv` entirely | 0.85 | New finding, not surfaced in Phase B1 (the catalogue audit worked from the CSV, which never mentions this source). File exists only at `Udaypur Reference Markdown Files\patanjala-yogasutra-rajamartanda-bhoja.md`. kb3 calls this "a work composed by Bhoja Paramāra himself... high authority for Bhoja's learning and authorship" with a chapter_prior on C5 (Paramāras and Bhoja, 0.6) and C10 (Ritual and Knowledge, 0.4) in the old scheme — meaning new **Ch4** and new **Ch6** likely need it. Needs its own catalogue-equivalent registry entry; currently invisible to anyone relying on the CSV alone. |

### B.3 Discrepancies carried forward from Phase B1 (not re-litigated here)

- `Art of the Paramaras of Malwa` (`Art of Paramaras.md`) and `Inscriptions of
  the Paramaras` (`Inscriptions Corpus.md`, the ASI/Trivedi *Corpus
  Inscriptionum Indicarum* — **not** the same work as the Patil composite
  `PAT-INS` above, despite the similar-sounding title) are both present and
  indexed; the catalogue's `MD=N` flags for both are confirmed data-entry
  errors, not availability gaps. Neither carries a kb3 code — they were
  apparently added to the active corpus after the 2026-09-24 kb3 build and so
  were never bucketed by it. **Both need first-pass chapter assignment during
  Part C**, since kb3 has no prior judgment on them at all.
- `History of the Parmar Rajput Dynasty.md` = catalogue's "Paramara Rajput
  Dynasty Origins" = kb3's `PAR` — confirmed by DOI, as above.
- `Temple Economics.md` research-use policy — confirmed by both this
  project's own full-text check and kb3's independent prior judgment.

### B.4 Sources present in the active corpus but carrying no kb3 code at all

Two sources — `Art of Paramaras.md` and `Inscriptions Corpus.md` — are fully
indexed (65 and 806 chunks respectively) but have no kb3 bucket, reliability
score, or chapter prior, because they were evidently added to the active
corpus after kb3's 2026-09-24 build. They receive first-pass treatment
(reliability judgment, chapter assignment, evidence extraction) directly from
live `src/` retrieval and direct reading during Part C, with no legacy
material to carry forward or re-verify.

**`Art of Paramaras.md` update:** initially flagged in Part F as never
reached by any chapter despite being fully indexed. A direct, targeted
search (not live vector retrieval, which did not surface this file's
content reliably for Udaypur-specific queries) found that the book
contains two dedicated Hindi-language articles of direct relevance: Kamala
Mittal's "उदयपुर का उदयेश्वर मंदिर" ("The Udayeśvara Temple of Udaypur"),
now used extensively in Ch5, and a second survey article (author's name
illegible in the OCR) on major Paramāra-period temples of Malwa, used in
Ch4, Ch5, and Ch10. This source's OCR quality is notably poor throughout
(frequent repeated phrases, corrupted characters) — every citation to it
in this document is flagged accordingly, and quotations are limited to
clearly legible fragments.

### B.5 Works Cited (MLA, cumulative — grows as each chapter cites a source)

Standard MLA format. An entry appears here the first time Part C actually
cites that source, not pre-emptively for all 29 inventoried sources — several
would need a fabricated publisher or year to complete now. Where no named
author survives in the source's own front matter, the organization or the
work itself is used as the alphabetizing key, per MLA's rule for
anonymous/corporate authorship, and that absence is stated rather than
papered over.

- Adhikari, Swati Mondal. *Some Paramāra Temples From Madhya Pradesh: A Case Study of Village Un*. 2013.
- Ganguly, D. C. *History of the Paramāra Dynasty*. 1933.
- INTACH Bhopal Chapter. *Geo-Heritage of Udaypur: The Third Eye*. INTACH, c. 2024.
- INTACH Bhopal Chapter. *The Architectural Splendor of Udaypur*. Manjul Publishing House, 2022.
- Kumar, Amit, et al. "Streamflow of the Betwa River under the Combined Effect of LU-LC and Climate Change." 2023. Journal not established in the extracted text — flagged, not invented.
- Mittal, Kamala. "उदयपुर का उदयेश्वर मंदिर" ["The Udayeśvara Temple of Udaypur"]. In *Art of the Paramāras of Malwa*, edited by R. K. Sharma, 1979.
- Pande, Anupa. *The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta*. Year not established in the extracted text.
- Patil, D. R. *The Cultural Heritage of Madhya Bharat*. Department of Archaeology, Government of Madhya Bharat, 1952.
- Rajpurohit, Bhagwatilal. *King Bhoj and Paramara-period Town Architecture*. Translated from the Hindi, *Raja Bhoj aur Parmarkaleen Nagar Sthapatya*. English translation, year not established.
- Shrivastav, P. N., and Rajendra Verma. *Madhya Pradesh District Gazetteers: Vidisha*. District Gazetteers Department, Government of Madhya Pradesh, 1979.
- Singh, Saarthak. "A Serpentine Scimitar of Letters from Udaypur, District Vidisha, M.P." 2023.
- Suryavanshi, Shakti, et al. "Long-term Historic Changes in Climatic Variables of Betwa Basin, India." *Theoretical and Applied Climatology*, 2013.
- Tiwari, Vijay Manohar. *Jagta Hua Kasba / कथा उदयपुर*. English translation. c. 2021–22.
- Trivedi, Harihar Vithal, editor. *Corpus Inscriptionum Indicarum, Vol. VII, Part 2: Inscriptions of the Paramāras, Chandēllas, Kachchapaghātas and Two Minor Dynasties*. Archaeological Survey of India, 1991.
- Venziya, Pratapsinh Ranaji. "History of the Parmar Rajput Dynasty." *The Academic: International Journal of Multidisciplinary Research*, vol. 3, no. 11, 2025.
- [Author not reliably identified from OCR — rendered "मुशील कुमार मुल्लेरे" in the extracted text]. "मालवा के परमारकलीन प्रमुख मंदिर" ["Major Paramāra-period Temples of Malwa"]. In *Art of the Paramāras of Malwa*, edited by R. K. Sharma, 1979.

**Disambiguation note:** both INTACH entries share the same corporate author,
so every in-text citation to either one uses a short title —
`(INTACH, Geo-Heritage Page)` or `(INTACH, Architectural Splendor Page)` —
per MLA's rule for an author with more than one cited work.

---

## Part C — Chapter-by-chapter evidence dossiers

Status for all thirteen sections is tracked in
`docs/sourcebook_rebuild_checklist.md`. Built so far: **Ch1**. The remaining
twelve are not yet built and are not described below — this section will be
replaced incrementally as each is completed, never left to silently imply
coverage it does not have.

### Ch1 — Udaypur: Historical Memory and the Making of a Place

#### Ch1.1 Chapter scope and research questions

Per `chapters.md`: "Introduce Udaypur, its historical identity, its place in
regional memory, and its references in ancient texts. Establish the town's
significance and the historical questions that the book seeks to answer."
This chapter is about the town's own identity and name, not yet the dynastic
history of its founder (new Ch4) or the deep regional prehistory around
Vidisha (new Ch3) — those are handled separately, even though one kb3 bucket
(old C1) mixed Udaypur-identity material with Vidisha/prehistory material
before this rebuild. Research questions this chapter must address: what does
the town's own name record about its founding; what do independent,
non-literary sources (geological/archaeological survey, gazetteer) say about
its age and identity; where does the documented history give way to local
legend; and what, precisely, remains uncertain about even the foundational
facts (the founder's exact dates, the pre-Udayāditya name of the site).

#### Ch1.2 Relevant sources

- **`Geo-Heritage of Udaypur The Third Eye.md`** (INT-GEO, reliability 0.80).
  Direct Udaypur evidence. An instrument-based survey (drone + total station)
  that also carries a dedicated "HISTORY OF UDAYPUR" section and the clearest
  statement of the town's foundation legend. Examined directly this pass
  (full text of §§1, 2, 4, 9, 17 read, not just retrieved snippets).
- **`The cultural heritage of madhya bharat.md`** (PAT-CH / `patil-1952`,
  reliability 0.80). Direct Udaypur evidence. D. R. Patil's 1952 official
  survey; its "§4 Udaypur" entry is the fullest independent monument-by-
  monument description in the corpus and the clearest textual source for the
  foundation inscription's triple-naming. Read in full this pass.
- **`Inscriptions Corpus.md`** (uncoded in kb3 — see Part B.3/B.4; the ASI/
  Trivedi *Corpus Inscriptionum Indicarum*). Direct Udaypur evidence,
  primary-epigraphic in character (a modern edition of an inscription, not
  the inscription itself). Contains an explicit, separate statement that
  "Udayapura... still bears this name" as the capital of a feudatory (the
  Nēmaka dynasty) under Udayāditya. Newly surfaced this pass — kb3 never
  bucketed this file at all.
- **`Vidisha Gazeteer.md`** (GAZ-VID, reliability 0.70 in kb3; kb3 flags 36%
  of this source's chunks as LLM-restated and not quotable — caveat retained
  here). Direct Udaypur evidence in its gazetteer entry for the village, read
  directly this pass; also carries a comparative aside (a differently-sited
  "Neelakantheshwara" temple near Lateri explicitly compared to "the famous
  Neelakantheshwara temple of Udaipur, ancient Udayapura") — this second
  passage is regional/comparative, not a second, independent attestation
  about Udaypur itself, and is classified as such below.
- **`Intach Udaypur (1).md`** (INT-ARC, reliability 0.75). Direct Udaypur
  evidence for demography, location and administrative facts; its potted
  history passages (e.g. "The Pamans of Malwa ruled central India...") are
  badly OCR-damaged and are flagged, not quoted, below.
- **`History of the Parmar Rajput Dynasty.md`** (PAR, reliability 0.40).
  Not yet examined for Ch1-specific content this pass; kb3's own prior
  judgment on this source warns it "presents the agnikula myth as validated
  history" — any origin-myth material from it needs the same scrutiny applied
  to the Bhrangarajpur/Gond legends from INT-GEO below, not automatic trust.
- **`भोजदेव (Bhojadeva)` (`bhojdev.md`, BHJ-H)**, **`Samarāṅgaṇa-sūtradhāra`
  (`SAM`, split across two active files)**, and **`Skanda-Purāṇa Part XIII`
  (`SKP-13`)** appeared in kb3's old-C1 bucket but, on inspection of the
  actual excerpts (Part B and the legacy archive), their content is about
  Vidisha/Heliodoros, generic Purāṇic tīrtha lists, or Śilpaśāstra
  architectural terminology — none of it names Udaypur. Reassigned to new
  **Ch3** (Vidisha/prehistory) pending that chapter's own search; not treated
  as Ch1 evidence here. This is the clearest instance of the kb3-bucket split
  anticipated in Part A.5.
- **`Bhoja Paramara and His Times`** (SIN-B) and **`भोजदेव`-adjacent
  dynastic-list material — unindexed/not re-examined this pass; flagged as a
  gap in Ch1.6 below.

#### Ch1.3 Facts, figures, and evidence

Citations below follow MLA in-text style, `(Author Page)`, immediately
followed by a bracketed technical trace giving the file, heading/section, and
OCR-page caveat needed to re-find and re-check the passage in the live
corpus (see Part A.9). Full Works Cited entries are in Part B.5.

**Location, administration, and present-day scale** (regional/administrative
record, not ancient attestation, but establishes the subject precisely):
Udaypur is a village panchayat in Ganj Basoda Tehsil, Vidisha district,
Madhya Pradesh (INTACH, Geo-Heritage 7) [File: `Geo-Heritage of Udaypur The
Third Eye.md`; sec. "1. INTRODUCTION: UDAYPUR, A SITE OF HERITAGE AND
GEOLOGICAL IMPORTANCE"; OCR page marker 7 — printed-page status unconfirmed].
Area 1,966 hectares / 19.66 km² (INTACH, Architectural Splendor 12) [File:
`Intach Udaypur (1).md`; sec. "1.1 Location and Setting"; OCR page marker 12;
the surrounding sentence is itself OCR-damaged and should be re-read before
quoting verbatim]. 2011 census population 6,383 (male 3,405, female 2,978),
literacy rate 54.28% (INTACH, Geo-Heritage 20) [same file; sec. "4.3
Topography"; OCR page marker 20].

**The foundation and the triple naming.** The single most important fact for
this chapter: an inscription on the Udayeśvara temple itself records that
Paramāra king Udayāditya "founded a town, built a temple of Shiva and
excavated a tank, and designated all the three works after his own name as
Udayapura, Udayeshvara and Udayasamudra respectively" (Patil 115) [File: `The
cultural heritage of madhya bharat.md`; sec. "4 Udaypur"; OCR page marker
114–115]. Two further inscriptions on the same temple date construction's
start to V.S. 1116 (A.D. 1059) and the flagstaff's erection to V.S. 1137
(A.D. 1080) (Patil 115) [same file and section]. A second, independent
epigraphic source confirms the name's continuity after the foundation: "the
only geographical name mentioned in the record is Udayapura, which is said to
be the capital town of the Nēmaka dynasty..., which was subordinate to
Udayāditya. This place still bears this name, as we have already seen"
(Trivedi 139) [File: `Inscriptions Corpus.md`; sec. "UDAIPUR STONE
INSCRIPTION OF THE PARAMĀRA RULERS OF MĀLWA: (UNDATED)—PART B"; OCR page
marker 139 — located and confirmed this revision, resolving the heading/page
gap flagged in the prior draft]. A third, independently-worded source gives
the same foundation account: "Udayapura town was founded by the Paramara
king Udayaditya during the latter half of the 11th century A.D. ... built a
temple dedicated to Siva and named it as Udayeshwara" (Shrivastav and Verma
346) [File: `Vidisha Gazeteer.md`; entry heading "Udayapur (23°54′ N; 78°6′
E)"; OCR page marker 346 — located and confirmed this revision], which
separately notes physical evidence of "an old fortification wall of great
uncemented stone blocks" extending to a hill about 1 km south of the village
(Shrivastav and Verma 346) [same file, entry, and page].

**Pre-foundation name and legend — explicitly flagged as legend, not
established fact, matching the source's own framing.** INTACH's Geo-Heritage
survey reports a local legend that the site was called "Bhrangarajpur,"
ruled by a "native chief" whom Udayāditya defeated before "establish[ing]
his rule and the new city of Udaypur in 1059 CE," and that a market to the
hill's south was called "Manik Chowk" for reasons folklore does not explain
(INTACH, Geo-Heritage 12) [File: `Geo-Heritage of Udaypur The Third Eye.md`;
sec. "4. GEO HERITAGE OF UDAYPUR" / the following unnumbered section; OCR
page marker 12]. The same source separately reports "[a]nother oral
tradition" that the hilly region was Gond territory before Udayāditya
"conquered it and renamed it Udaypur" (INTACH, Geo-Heritage 13) [same file;
OCR page marker 13]. These two oral traditions are not reconciled with each
other in the source (a native chief's kingdom vs. Gond territory) and are not
reconciled with the inscriptional naming account above; this document does
not reconcile them either. INTACH's own text frames both as oral
tradition/local legend, not as established history, and this document
preserves that framing.

**An unattributed antiquarian account, quoted at second hand.** INTACH's
Geo-Heritage survey quotes an unnamed earlier writer ("Talking about this
particular hill he writes—") describing the hill as presenting "the exact
appearance of a fortified castle," identifying a massive uncemented stone
wall "18 feet thick," multiple gates, and a north gate "shown signs of having
been repaired or altered by the Muhammadans," next to "a dargah of a
Muhammadan saint... known as Pir" (INTACH, Geo-Heritage 9) [File: `Geo-
Heritage of Udaypur The Third Eye.md`; sec. "2. HISTORY OF UDAYPUR"; OCR page
marker 9]. **Caveat (uncertainty in attribution, stated plainly rather than
invented):** the source does not name this writer in the portion captured;
the voice and antiquarian register strongly resemble late-19th-century ASI
survey writing (compare Patil's own later survey, which cites this hill
independently), but the attribution is not confirmed and must not be
presented as a named, dated citation until the original writer is
identified — a research gap, recorded in Ch1.6. (No MLA in-text citation is
given for the quoted writer himself, since he is not identified; the
citation above is to INTACH as the quoting source.)

**The monuments, as inventoried by Patil (1952).** Six principal monuments
are listed for the town: the Udayeśvara/Nīlakaṇṭheśvara Mahādeva temple,
Bijamandal (Ghaḍiyālān-kā-makān), Bara-khambi, Pisnari-kā-mandir, the Shāhī
masjid and mahal, and Sher Khān's mosque (Patil 114–118) [File: `The cultural
heritage of madhya bharat.md`; sec. "4 Udaypur"; OCR page markers 114–118].
The temple's damage is attributed by Patil to Muhammad Tughlaq (A.H. 737–39 /
A.D. 1336–38), not to the popularly-blamed Aurangzeb — an explicit,
source-stated correction of a popular legend (Patil 117) [same file and
section; OCR page marker 117] — **directly relevant to this chapter's
"historical memory vs. established history" framing and a candidate
load-bearing claim for the chapter's own narrative.**

#### Ch1.4 Relevant excerpts and passage references

MLA in-text citation first, then the technical trace `[File; sec.; OCR page]`
that MLA does not carry but this document's fidelity requirements do.

| ID | MLA citation | Excerpt / substance | Classification | Technical trace | Caveats |
|---|---|---|---|---|---|
| CH1-E01 | (Patil 115) | "the Paramara king Udayaditya of Malwa founded a town, built a temple of Shiva and excavated a tank, and designated all the three works after his own name as Udayapura, Udayeshvara and Udayasamudra respectively" | Direct Udaypur evidence; primary-epigraphic content quoted within a secondary survey | [`The cultural heritage of madhya bharat.md`; sec. "4 Udaypur"; OCR p.115] | Verbatim as extracted; OCR page marker not confirmed against the book's own printed pagination |
| CH1-E02 | (Patil 115) | Construction begins V.S. 1116 (A.D. 1059); flagstaff erected V.S. 1137 (A.D. 1080), per two further inscriptions on the temple | Direct Udaypur evidence | [same file; sec. "4 Udaypur"; OCR p.115] | Same page-numbering caveat |
| CH1-E03 | (Trivedi 139) | "The only geographical name mentioned in the record is Udayapura, which is said to be the capital town of the Nēmaka dynasty..., which was subordinate to Udayāditya. This place still bears this name" | Direct Udaypur evidence; primary-epigraphic | [`Inscriptions Corpus.md`; sec. "UDAIPUR STONE INSCRIPTION OF THE PARAMĀRA RULERS OF MĀLWA: (UNDATED)—PART B"; OCR p.139] | Heading/page located and confirmed this revision |
| CH1-E04 | (Shrivastav and Verma 346) | "Udayapura town was founded by the Paramara king Udayaditya during the latter half of the 11th century A.D.... built a temple dedicated to Siva and named it as Udayeshwara" | Direct Udaypur evidence | [`Vidisha Gazeteer.md`; entry "Udayapur (23°54′ N; 78°6′ E)"; OCR p.346] | Heading/page located and confirmed this revision; kb3's "36% LLM-restated, not quotable" caveat on this source applies generally — this specific passage reads as a plain gazetteer statement, not an obvious LLM restatement, but was not individually checked against that flag |
| CH1-E05 | (INTACH, Geo-Heritage 12) | "this place was called Bhrangarajpur and was ruled by a native chief. He was defeated by Udayaditya and established his rule and the new city of Udaypur in 1059 CE" | Potential/unverified connection — explicitly local legend per the source's own framing | [`Geo-Heritage of Udaypur The Third Eye.md`; sec. "4. GEO HERITAGE OF UDAYPUR" §, following unnumbered section; OCR p.12] | Source itself calls this legend, not established fact; not reconciled with CH1-E06 |
| CH1-E06 | (INTACH, Geo-Heritage 13) | "the hilly region was the territory of the Gonds. Udayaditya conquered it and renamed it Udaypur" | Potential/unverified connection — oral tradition | [same file; OCR p.13] | Contradicts CH1-E05 on who held the site before 1059; both are oral tradition per the source |
| CH1-E07 | (INTACH, Geo-Heritage 9) | hill "presents... the exact appearance of a fortified castle"; wall "18 feet thick"; north gate "shown signs of having been repaired or altered by the Muhammadans" | Regional/comparative — quoted antiquarian source, author unidentified in the captured text | [same file; sec. "2. HISTORY OF UDAYPUR"; OCR p.9] | Original writer not named in the portion read; citation is to INTACH as the quoting source, not to the unnamed writer |
| CH1-E08 | (Patil 117) | Temple damage "more probable" due to Muhammad Tughlaq (A.H. 737–39) "built the mosque at the back of the temple with material of demolished shrines," not Aurangzeb as "popular legend" holds | Direct Udaypur evidence; contradictory/qualifying (corrects a popular legend) | [`The cultural heritage of madhya bharat.md`; sec. "4 Udaypur"; OCR p.117] | Patil's own hedge ("seems more probable") is part of the claim and must not be dropped when citing this |
| CH1-E09 | (INTACH, Geo-Heritage 20) | 2011 census: population 6,383 (M 3,405 / F 2,978), literacy 54.28% | Direct Udaypur evidence; demographic | [`Geo-Heritage of Udaypur The Third Eye.md`; sec. "4.3 Topography"; OCR p.20] | Census-year figure, not historical |
| CH1-E10 | (INTACH, Architectural Splendor 12) | Village location, Basuda Tehsil, Vidisha district; distances to sub-district/district headquarters | Direct Udaypur evidence; administrative | [`Intach Udaypur (1).md`; sec. "1.1 Location and Setting"; OCR p.12] | Surrounding sentence is OCR-damaged ("It lies at an away from..."); figures retrieved but exact phrasing needs a clean re-read before quotation |

No fixed excerpt count was applied; this list reflects what direct, full-text
reading and seven live retrieval queries surfaced as substantively relevant
to this chapter's actual scope, with old-C1-bucket material that concerns
Vidisha/prehistory deliberately excluded (reassigned to Ch3) rather than
padded in here.

#### Ch1.5 Scholarly interpretations and disagreements

- **Aurangzeb vs. Muhammad Tughlaq** for the temple's damage (CH1-E08): Patil
  explicitly labels the popular Aurangzeb attribution a legend and gives the
  Tughlaq attribution as "more probable," citing two Persian inscriptions
  related to the later mosque as his basis. No second source in this
  chapter's evidence base directly contests Patil's correction, but none
  independently corroborates it either — flagged `[single-source, but
  explicitly a correction of a named popular belief]`, not a settled
  consensus.
- **Bhrangarajpur/native chief vs. Gond territory** (CH1-E05 vs. CH1-E06):
  both appear in the same source (INT-GEO) as unreconciled oral traditions
  about who held the site before 1059. This document records both and
  reconciles neither, per instruction.
- **The antiquarian quotation's authorship** (CH1-E07) is itself an open
  question, not a disagreement between sources — recorded as a gap below
  rather than guessed at.

#### Ch1.6 Research gaps and missing evidence

- The quoted 19th-century antiquarian description of the hill (CH1-E07) is
  not attributed to a named author in the text captured this pass. This is a
  gap in what was examined, not evidence that INT-GEO fabricated the
  quotation — the attribution likely exists elsewhere in the same file or in
  a footnote not yet located.
- ~~`Inscriptions Corpus.md`'s and `Vidisha Gazeteer.md`'s exact heading/page
  locations for CH1-E03 and CH1-E04~~ — **resolved this revision**: both
  located by direct read (OCR p.139 and p.346 respectively) and the MLA
  citations in Ch1.3/Ch1.4 updated accordingly.
- `Bhoja Paramara and His Times` (SIN-B) is physically present only in the
  legacy directory, not indexed, and was not read directly this pass despite
  kb3's chapter_prior placing some weight on it for the adjacent Ch4/Ch6
  material — any Ch1-relevant content it might hold (e.g. further naming or
  foundation-date detail) is an open gap, not ruled out.
- No source examined this pass offers an explicit, verified Purāṇic or other
  pre-11th-century textual reference naming Udaypur itself (as opposed to
  the regional Avanti/Vidisha material reassigned to Ch3). This chapter's
  brief asks for "references in ancient texts" — on the evidence gathered so
  far, the corpus's strongest "ancient text" connection is the temple's own
  11th-century foundation inscription (CH1-E01–E03), not a pre-existing
  scriptural mention of the place. This should be stated as a finding (the
  evidence does not support an older textual pedigree for the name), not
  papered over.
- The Gond/Bhrangarajpur legends have not been cross-checked against
  `History of the Parmar Rajput Dynasty.md` (PAR) or `भोजदेव` for a possibly
  independent attestation or contradiction — not yet examined.

#### Ch1.7 Drafting utility

- CH1-E01/E02 (the foundation inscription's triple naming and dates) is the
  chapter's strongest, most citable anchor claim and should likely open the
  chapter's substantive discussion of identity.
- CH1-E08 is a strong, source-grounded example of "historical memory vs.
  documented history" — exactly the chapter's stated thematic concern — and
  can be used to frame the chapter's methodological stance toward legend.
- CH1-E05/E06 should be presented explicitly as legend, with their mutual
  contradiction stated rather than smoothed over; they are good material for
  illustrating what counts as memory versus history, not for establishing
  pre-1059 political facts.
- Before publication: verify CH1-E03/E04's exact heading/page locations;
  identify CH1-E07's original author; confirm whether `Inscriptions Corpus.md`
  classifies its own Nēmaka-dynasty passage with a date, since none was
  captured this pass.
- Cross-reference: the 1059/1080 construction dates and Udayāditya's identity
  overlap heavily with new **Ch4** (Paramāras and the Foundation of Udaypur)
  — this chapter should state the naming/foundation fact plainly and let Ch4
  carry the fuller dynastic argument, rather than duplicating it.

---

### Ch2 — The Betwa Valley: Geography, Geology and Natural Environment

#### Ch2.1 Chapter scope and research questions

Per `chapters.md`: "Examine the valley's rivers, topography, seasons,
geological formations, forests, flora and fauna. Explain how the natural
environment shaped settlement, agriculture, access to resources, and the
materials available for construction." This is a clean merge of kb3's old
C2 and C3 buckets (Part A.5) — no split was needed, but the two buckets'
content had to be checked for the source-domination problem `kb3/retrieval.yaml`
itself flagged: `SAM` supplied 43% of old-C2 and 36% of old-C3 by raw
chunk count, and on inspection most of those SAM chunks are either generic
Puranic cosmology (the mythical "varṣa" continents of Jambudvīpa, which are
not the real Betwa valley) or generic Śilpaśāstra site-selection rules that
apply to any location, not Udaypur specifically. These are excluded from the
evidence below as not substantively about this chapter's actual subject,
consistent with this document's instruction not to treat retrieval/clustering
as proof of relevance.

#### Ch2.2 Relevant sources

- **`Streamflow of the Betwa Rive.md`** (BET-K, reliability 0.80). Direct
  evidence about the river itself — regional/comparative to the extent its
  study reach is the Upper Betwa, not the Udaypur-adjacent reach specifically,
  but it is the only hydrological model in the corpus and establishes the
  river's basic physical scale. Read directly this pass.
- **`Long-termhistoricchangesinclimaticvariablesofBetwa.md`** (BET-S,
  reliability 0.80). Same character as BET-K — basin-wide climatology, not
  Udaypur-specific, but the only source of its kind. Read directly.
- **`Vidisha Gazeteer.md`** (GAZ-VID, reliability 0.70; kb3's "36%
  LLM-restated" caveat on this source still applies generally). Direct
  evidence for the district's rivers, geology, flora, fauna, and climate,
  including an entry on "The Betwa" naming its full tributary network and
  giving coordinates, and a dedicated gazetteer chapter structure (Topography,
  Drainage, Geology, Economic minerals, Flora, Fauna, Climate — p.8) that
  this chapter's own scope mirrors closely. Read directly, several sections.
- **`Geo-Heritage of Udaypur The Third Eye.md`** (INT-GEO, reliability 0.80).
  Direct Udaypur evidence — the only source in the corpus with site-specific
  geomorphology (the Udaypur sandstone tableland's mesa/butte/pinnacle decay
  pathways), flora/fauna inventories, and drainage detail for the hill itself.
  Read directly, three sections.
- **`Some Paramara Templess.md`** (ADH, reliability 0.75). Regional/
  comparative — its Chirakhan quarry passage (about Un, not Udaypur) is
  directly relevant to the chapter's "materials available for construction"
  question and is now confirmed to exist verbatim in this active file, not
  only in the absent `PAT-TEM`/`PAT-INS` composites kb3 had cited it under
  (Part B.2's "Notes" on those two rows is resolved for this specific
  passage by this finding).
- **`Raja_Bhoj_Aur_Parmarkaleen_EN.md`** (RAJ-E, reliability 0.65). Regional/
  comparative — its "Water-bodies and Water Management" section translates
  the Samarāṅgaṇa-sūtradhāra's own prescriptions for wells, stepwells, and
  tanks, and separately describes King Bhoja's historical dam on the Betwa
  river at Bhojpur (near Bhopal, not Udaypur). Directly relevant to how
  Paramāra-era builders used this river system, though not to Udaypur itself.
  Read directly.
- **`The Hindu Temple Vol 1 Stella Kramrisch.md`** (KRAM-1, reliability
  0.90). General contextual evidence on temple building materials (stone,
  brick, plaster) — national in scope, not Udaypur- or Betwa-specific.
- **`samarangana` (`SAM`, split across two active files) and `भोजदेव`
  (`bhojdev.md`, BHJ-H)** — appear heavily in kb3's old C2/C3 buckets but,
  on inspection, their content is either mythic-cosmological (the Jambudvīpa
  varṣa descriptions) or generic architectural-ritual material (foundation
  rites, vāstu rules) with no identified connection to the real Betwa valley
  or Udaypur. Not treated as chapter evidence here; this is the source-
  domination problem kb3's own retrieval layer was built to counteract, now
  applied by hand since that layer is not available for this rebuild (Part
  A.8).
- **`कथा उदयपुर (Jagta Hua Kasba) — Hindi original`** (TIW-H) — kb3 cites a
  passage from this source about illegal sandstone mining damaging Udaypur's
  landscape today. The source is confirmed absent from the active corpus
  (Part B.2); this content is flagged as a gap below rather than quoted,
  since it cannot be re-verified against live text this pass.
- **`RAJM`** — kb3 itself flags this source as "barely represented" in both
  old C2 and C3; not examined for this chapter.

#### Ch2.3 Facts, figures, and evidence

**The Betwa river itself.** "The Betwa or Betrawati is a river of great
antiquity. The Betwa rises from the main Vindhyan range in the extreme
south-west (23°2′ N., 77°20′ E) of Raisen district. It is the third largest
river of Malwa region" (Shrivastav and Verma 18) [File: `Vidisha
Gazeteer.md`; sec. "The Betwa"; OCR p.18]. Its course within Vidisha district
is about 112 km, and its tributaries are named in full — Kaliasot, Ajnar,
Besh, Bah, Sagar, Kethan, Orr on the left bank; Richhan, Dabar, Nion, Parasri,
Bina, Jamni, Dhasan and Birma on the right (Shrivastav and Verma 18–19) [same
file and section]. Basin-wide, the Betwa's total length is 590 km (232 km in
Madhya Pradesh, 358 km in Uttar Pradesh) over a 43,500 km² catchment
(Suryavanshi et al. 4) [File:
`Long-termhistoricchangesinclimaticvariablesofBetwa.md`; sec. "2.1 Study
Area"(approx.; heading not individually re-confirmed this pass, page
confirmed); OCR p.4]. Streamflow has measurably declined: mean streamflow
fell 16% between 2001–2020 against 1982–2000, with maximum/minimum flow
dropping from 1079/139 m³s⁻¹ to 673/127 m³s⁻¹ across the same two periods
(Kumar et al. 10) [File: `Streamflow of the Betwa Rive.md`; OCR p.10].

**Climate.** Average annual rainfall for Udaypur village is cited as "around
800 mm" (INTACH, Geo-Heritage 23) [File: `Geo-Heritage of Udaypur The Third
Eye.md`; OCR p.23]. Basin-wide, daily mean temperature ranges from a maximum
of 42.3°C to a minimum of 8.1°C, and relative humidity from 18% (April–May)
to 90% (August) (Suryavanshi et al.) [File:
`Long-termhistoricchangesinclimaticvariablesofBetwa.md`; exact page not
re-confirmed this pass — carried from kb3's prior citation, flagged for
direct verification]. The Indian Summer Monsoon Rainfall over Central India
is reported to have declined 10–20% from 1950–2015 (Kumar et al.) [File:
`Streamflow of the Betwa Rive.md`; exact page not re-confirmed this pass].

**Geology and landforms.** The district's geological formations are
Alluvium, Laterite, and Deccan Trap with inter-trappean beds (Shrivastav and
Verma 20) [File: `Vidisha Gazeteer.md`; sec. "Geology"; OCR p.20]. Laterite's
harder varieties are used as building stone, the softer as road metal
(Shrivastav and Verma 22) [same file; sec. "Road Metal"; OCR p.22].
Udaypur's own hill is a sandstone tableland undergoing documented
mesa-to-butte-to-pinnacle decay — the corpus's only site-specific
geomorphological study of this kind, describing "different pathways of mesa
decay" controlled by caprock thickness, jointing pattern, and weaker
intercalations (INTACH, Geo-Heritage 25) [File: `Geo-Heritage of Udaypur The
Third Eye.md`; sec. "4.9 Geological Landform"; OCR p.25]. Separately, soil
across the village is "75% black cotton soil," the remainder "red-yellow
mixed soils derived from the sandstone and shale," with laterite, Vindhyan
sandstone, and basalt also present (INTACH, Geo-Heritage 23) [same file; sec.
"4.7 Geomorphology"; OCR p.23 — note this is a *different* passage, on a
different OCR page, than the mesa/butte passage above, though both share the
same heading, a reminder that one heading can span several OCR pages/chunks].

**Flora and fauna.** INTACH's survey lists Udaypur hill fauna including
monkey, shrew, squirrel, and mongoose (*Herpestes auropunctatus*), with
noted habitat loss from grazing and illegal tree-cutting (INTACH,
Geo-Heritage 37–39) [File: `Geo-Heritage of Udaypur The Third Eye.md`; sec.
"5. THE FLORA AND FAUNA OF UDAYPUR" / "5.1 Faunal diversity"; OCR p.37–39].
The gazetteer's district-wide bird list includes peafowl, red jungle-fowl,
and bhat titar among others (Shrivastav and Verma 28) [File: `Vidisha
Gazeteer.md`; sec. "Birds"; OCR p.28], and its forest-produce entry states
about 60% of district forest produces timber and fuelwood, with bamboo, gum,
tendu leaves, lac, and honey as other produce (Shrivastav and Verma 117)
[same file; sec. "Forest Produce"; OCR p.117].

**Materials and construction — the chapter's explicit "access to resources"
question.** The Chirakhan quarry near Un supplied the coarse-grained
sandstone used to build the Un temple cluster, and its lower durability is
given as the direct explanation for why those temples "are either in decay
or in complete ruins" compared with temples using higher-quality pink
sandstone (Adhikari 43) [File: `Some Paramara Templess.md`; sec. "THE QUARRY
- CHIRAKHAN"; OCR p.43]. This is regional/comparative evidence (about Un, not
Udaypur), but it is the clearest source-grounded link in the corpus between
local stone quality and a monument's structural fate — a transferable
methodological point for assessing Udaypur's own sandstone, which Patil's
survey independently describes as "pink coloured sandstone" (see Ch1,
CH1-E01 context) without commenting on its quarry source or durability.

**Water engineering on the same river system (regional/comparative, not
direct evidence).** The Samarāṅgaṇa-sūtradhāra's own prescriptions specify
ten named wells (four to thirteen cubits), four kinds of stepwell, and four
kinds of *kuṇḍa*, down to dimensions and which creatures should inhabit a
protective moat (Rajpurohit 108–109) [File: `Raja_Bhoj_Aur_Parmarkaleen_EN.md`;
sec. "Water-bodies and Water Management"; OCR p.108–109]. Historically, King
Bhoja himself built a large dam on the Betwa at Bhojpur, forming a lake of
about 250 square miles that Sultan Hoshang Shah of Mandu later breached
(Rajpurohit 110) [same file; sec. "Water Management"; OCR p.110]. Bhojpur is
near Bhopal, a different site on the same river from Udaypur — this is
explicitly regional/comparative evidence about Paramāra-era hydraulic
engineering on the Betwa system, not a claim about Udaypur's own tank
(Udayasāmudra), which is addressed in Ch1 and Ch4.

#### Ch2.4 Relevant excerpts and passage references

| ID | MLA citation | Excerpt / substance | Classification | Technical trace | Caveats |
|---|---|---|---|---|---|
| CH2-E01 | (Shrivastav and Verma 18) | "The Betwa or Betrawati is a river of great antiquity... rises from the main Vindhyan range... It is the third largest river of Malwa region" | Regional/comparative (district-wide, not Udaypur-specific, but establishes the valley the chapter is named for) | [`Vidisha Gazeteer.md`; sec. "The Betwa"; OCR p.18] | — |
| CH2-E02 | (Shrivastav and Verma 18–19) | Full tributary list, left and right bank | Regional/comparative | [same file and section; OCR p.18–19] | — |
| CH2-E03 | (Suryavanshi et al. 4) | Basin area 43,500 km²; total length 590 km (232 km in MP, 358 km in UP) | Regional/comparative | [`Long-termhistoricchangesinclimaticvariablesofBetwa.md`; OCR p.4] | Heading not individually re-confirmed |
| CH2-E04 | (Kumar et al. 10) | Mean streamflow down 16% (2001–2020 vs. 1982–2000); max/min flow 1079/139 → 673/127 m³s⁻¹ | Regional/comparative; contemporary hydrology, not historical | [`Streamflow of the Betwa Rive.md`; OCR p.10] | — |
| CH2-E05 | (INTACH, Geo-Heritage 23) | Average annual rainfall for Udaypur village "around 800 mm" | Direct Udaypur evidence | [`Geo-Heritage of Udaypur The Third Eye.md`; OCR p.23] | — |
| CH2-E06 | (Shrivastav and Verma 20) | District geology: Alluvium, Laterite, Deccan Trap with inter-trappean beds | Regional/comparative | [`Vidisha Gazeteer.md`; sec. "Geology"; OCR p.20] | — |
| CH2-E07 | (INTACH, Geo-Heritage 25) | Udaypur sandstone tableland's mesa→butte→pinnacle decay pathways, controlled by caprock thickness and jointing | Direct Udaypur evidence; the corpus's only site-specific geomorphology study | [`Geo-Heritage of Udaypur The Third Eye.md`; sec. "4.9 Geological Landform"; OCR p.25] | Reads as a technical paper excerpt; terminology (mesa, butte, pinnacle, caprock) should be glossed for a general reader |
| CH2-E08 | (INTACH, Geo-Heritage 23) | Soil: 75% black cotton soil, 25% red-yellow sandstone/shale-derived, plus laterite/basalt | Direct Udaypur evidence | [same file; sec. "4.7 Geomorphology"; OCR p.23] | Same heading as CH2-E07 but a different OCR page/chunk — do not conflate |
| CH2-E09 | (INTACH, Geo-Heritage 37–39) | Fauna: monkey, shrew, squirrel, mongoose; habitat loss from grazing/illegal tree-cutting | Direct Udaypur evidence | [same file; sec. "5. THE FLORA AND FAUNA OF UDAYPUR" / "5.1 Faunal diversity"; OCR p.37–39] | Species list is partial/OCR-damaged in places (one entry unreadable) |
| CH2-E10 | (Adhikari 43) | Chirakhan quarry: "chira" (cutting) + "khan" (quarry); coarse sandstone of lower quality explains the Un temples' poor preservation | Regional/comparative | [`Some Paramara Templess.md`; sec. "THE QUARRY - CHIRAKHAN"; OCR p.43] | About Un, not Udaypur; a methodological parallel, not a fact about Udaypur's own stone |
| CH2-E11 | (Rajpurohit 108) | Samarāṅgaṇa-sūtradhāra's well/stepwell/tank typology and dimensions | Regional/comparative; primary-authorial content quoted in translation | [`Raja_Bhoj_Aur_Parmarkaleen_EN.md`; sec. "Water-bodies and Water Management"; OCR p.108] | Translation, not the Sanskrit original; not yet cross-checked against the two active Samarāṅgaṇa-sūtradhāra files |
| CH2-E12 | (Rajpurohit 110) | Bhoja's dam at Bhojpur on the Betwa; lake of ~250 sq. mi.; later breached by Hoshang Shah | Regional/comparative — different site, same river | [same file; sec. "Water Management"; OCR p.110] | Legendary/traditional elements in the surrounding text (Bhopal's name-origin story) are not separated from the dam claim in this excerpt; worth a closer read before citing the etymology |

No fixed excerpt count was applied. Live retrieval (8 queries) plus direct
reading of five sources produced this set; the SAM/BHJ-H material that
dominates kb3's prior bucket by volume was deliberately excluded as
off-topic, not omitted by a quota.

#### Ch2.5 Scholarly interpretations and disagreements

No direct factual contradiction was found between sources this pass —
unlike Ch1, this chapter's sources (hydrology, climatology, gazetteer,
survey) are largely descriptive and do not make competing historical claims.
One methodological tension is worth flagging: INTACH's Geo-Heritage survey
(CH2-E07) is written in the register of a technical geomorphology paper,
while the gazetteer (CH2-E01, E02, E06) is a 1979 administrative compilation
with a different evidentiary standard; both are treated as reliable for
their respective physical-description claims (kb3 scores both 0.70–0.80),
but neither should be read as providing a historical argument.

#### Ch2.6 Research gaps and missing evidence

- **`कथा उदयपुर` (Hindi original, TIW-H)** carries a passage (per kb3's prior
  excerpt) about present-day illegal sandstone mining damaging Udaypur's
  landscape — directly relevant to this chapter's "access to resources"
  theme and to modern conservation concerns, but the source is confirmed
  absent from the active corpus (Part B.2) and this content could not be
  re-verified this pass. This is an open gap, not a dropped fact — the claim
  may well be true, but it cannot currently be cited from a live, checkable
  source.
- BET-S's temperature/humidity range and the ISMR decline figure were
  carried forward from kb3's prior citation without an independent
  page-level re-confirmation this pass (unlike the Betwa-basin-area figure,
  which was independently re-confirmed). Flagged for a follow-up read.
- No source examined this pass gives a clear, Udaypur-specific account of
  which quarry supplied the stone for the Udayeśvara temple itself — Patil
  (Ch1) describes the stone as "pink coloured sandstone" but not its source;
  the Chirakhan parallel from Un (CH2-E10) is suggestive but not evidence
  about Udaypur's own supply chain. This is a real, stated gap in what the
  corpus currently establishes, not a question this document answers by
  inference.
- The two active Samarāṅgaṇa-sūtradhāra files (`Samarangan Vol 2 (a)_combined.md`,
  `Samrangana Sutradhar Vol 1.md`) were not searched directly for a
  genuinely Betwa/Udaypur-specific passage this pass, only assessed via the
  kb3 bucket's existing (mostly off-topic) excerpts. A direct search of the
  two active files for water-management or site-selection material still
  owed before this chapter is considered fully examined.

#### Ch2.7 Drafting utility

- CH2-E01/E02 (the river's course and tributaries) and CH2-E06 (geology)
  give the chapter its descriptive backbone and can open the chapter.
- CH2-E07 (the mesa/butte/pinnacle study) is the single most distinctive,
  Udaypur-specific piece of evidence in this chapter and deserves a
  prominent, plainly-glossed treatment — it is also a good anchor for later
  cross-reference to Ch5 (the temple built partly from this same hill's
  stone) and Ch11 (conservation of the geological site itself).
  Cross-reference target once those chapters exist.
- CH2-E10/E11/E12 should be presented explicitly as regional/comparative,
  not folded into Udaypur's own narrative as if they were local facts — the
  chapter's prose should mark the shift in referent clearly each time (Un,
  Bhojpur) before returning to Udaypur.
- Before publication: verify BET-S's temperature/humidity citation
  page-by-page; search the two active SAM files directly for anything
  genuinely on-topic; and resolve whether `कथा उदयपुर`'s mining passage can
  be sourced from any live file before using it.

### Ch3 — Before Udaypur: Prehistory, Early Vidisha and the Historical Landscape of Central India

#### Ch3.1 Chapter scope and research questions

Per `chapters.md`: "Trace the region from prehistory through the early
historic period, with particular attention to Vidisha and the emergence of
regional political and cultural networks. Introduce the trade routes, sacred
centres and changing powers that formed the wider historical setting for
Udaypur." Per the chapter's own annotation ("Original C4 + selected
background from C5"), this chapter is explicitly about the *region*, not
Udaypur itself — Udaypur's own identity (Ch1) and its Paramāra founder's
dynastic context (Ch4) are handled elsewhere. This is the clearest case of
the kb3-bucket split anticipated in Part A.5, and it draws on **two**
different kb3 buckets, neither of which maps onto it cleanly: old-C1
(the Vidisha/Heliodoros content set aside while building Ch1) and old-C4
"From Avanti to Malwa" (which splits again — its early/background portion
belongs here, its detailed medieval Paramāra-Pratihāra-Rāṣṭrakūṭa dynastic
chronology belongs to Ch4). Research questions: what does the region look
like before any Paramāra ever reaches it; what made Vidisha/Besnagar
significant for a millennium before Udaypur existed; what trade and
pilgrimage networks ran through the area; and what, if anything, genuinely
ties this deep history to Udaypur itself, as opposed to merely sharing a
district.

#### Ch3.2 Relevant sources

- **`Vidisha Gazeteer.md`** (GAZ-VID, reliability 0.70). Direct evidence for
  this chapter's actual subject (Vidisha's regional history) — its "CHAPTER
  II HISTORY" is a dense, internally-footnoted chronological account running
  from palaeolithic tools through the Guptas. The single richest source for
  this chapter; read directly and extensively this pass (OCR pp.33–40).
- **`The cultural heritage of madhya bharat.md`** (PAT-CH, reliability
  0.80). Direct evidence, same character — Patil's own "§2 Besnagar" and "§3
  Udaygiri" entries (OCR p.112–114) independently corroborate several of the
  gazetteer's claims (the Heliodoros/Garuda-pillar episode, the Udaygiri
  Varāha cave) in differently-worded form. Read directly.
- **`Geo-Heritage of Udaypur The Third Eye.md`** (INT-GEO) and
  **`Jagta_Hua_Kasba_EN.md`** (TIW-E) — the sources kb3's old-C1 bucket
  leaned on most heavily for Vidisha/Heliodoros material (see Ch1's
  "Relevant sources," where this content was set aside). Their Heliodoros
  passages are impressionistic/reportage register (TIW-E explicitly a
  first-person heritage-walk account), not the primary basis for this
  chapter's factual claims — GAZ-VID and PAT-CH's footnoted accounts are
  preferred wherever they overlap.
- **`806955603-The-Temple-Architecture-of-India-Adam-Hardy.md`** (HAR,
  reliability 0.90). General contextual evidence — places Udayagiri's 5th-century
  cave architecture within a wider account of early Indian rock-cut
  building. Read via retrieval snippet only this pass.
- **`History of Paramara Dynasty DC Ganguly.md`** (GAN), **`Inscriptions
  Corpus.md`**, **`Raja_Bhoj_Aur_Parmarkaleen_EN.md`** (RAJ-E), **`Bhoja
  Paramara and His Times`** (SIN-B, unindexed) — these carry kb3's old-C4
  "background" material, but on inspection most of their content in that
  bucket is already specifically about the Paramāra dynasty's own rise
  (Vākpati II, Siyaka, Jayasiṃha) rather than the pre-Paramāra regional
  setting this chapter needs — reassigned to **Ch4**, not used here, per
  the same discipline applied to Ch1/Ch2.
- **`Skanda-Purāṇa Part XIII`** (SKP-13) — contains a Purāṇic reference to
  Vidisha as a *tīrtha* (pilgrimage site), independently noted by the
  Gazetteer (p.33) as a known classical-era reference; not independently
  read in the primary text this pass, flagged for a follow-up check.

#### Ch3.3 Facts, figures, and evidence

**Prehistory.** Palaeolithic tools — choppers, handaxes, cleavers, scrapers,
bifaces, discs — have been found in the valleys of the Betwa, Bina, Dhasan
and Keothan rivers (Shrivastav and Verma 33) [File: `Vidisha Gazeteer.md`;
sec. "CHAPTER II HISTORY"; OCR p.33]. Chalcolithic tools and black-and-red
ware datable to 1000–700 B.C. were found in an ancient mound in the
district, with microlithic blades and later painted pottery marking a
subsequent "Aryan influence" layer above the Chalcolithic one (Shrivastav
and Verma 33) [same file and section].

**Naming, trade routes, and early textual references.** The region was
known in antiquity as Dasharna, with Vidisha/Besnagar as its capital — a name
used by both Kautilya and Kalidasa (Shrivastav and Verma 34) [same file; OCR
p.34]. Vidisha prospered from sitting at the crossing of two major trade
routes: one running Pratiṣṭhāna (Paithan)–Mahishmati–Ujjayinī–Gonaddha–
Vaidisa–Kauśāmbī, the other connecting Bharukaccha (Broach) and Sūrpāraka on
the Arabian Sea to Mathurā via Ujjayinī, with a branch running Vidisha–
Kauśāmbī via the Betwa valley to Pātaliputra (Shrivastav and Verma 34) [same
file and page]. The Buddhist physician Jīvaka's itinerary (sent from
Ajātaśatru's Magadhan court to treat the king of Avanti, Chanda Pradyota)
names Vidisha, Gonaddha, Ujjain and Mahishmati in sequence, read as
corroborating these same routes (Shrivastav and Verma 34) [same file and
page]. The Gazetteer separately notes a Purāṇic reference to Vidisha as a
pilgrimage *tīrtha*, and an Anguttara Nikāya reference placing Vidisha within
the Avanti Janapada before the Buddha's time (Shrivastav and Verma 33) [same
file; OCR p.33] — the chapter's clearest textually-attested basis for calling
this a "sacred centre," independent of the Heliodoros material below.

**The Mauryas and the Devi/Mahendra episode.** Aśoka, as an 18-year-old
prince appointed viceroy at Ujjain by his father Bindusāra, married Devī, "a
banker's daughter of Vidisha or Besnagar of the Śākya clan," while travelling
there; their son Mahendra and daughter Saṅghamitrā became the missionaries
who carried a Bodhi-tree sapling to Ceylon (Shrivastav and Verma 35) [File:
`Vidisha Gazeteer.md`; sec. "The Mauryas"; OCR p.35]. The Gazetteer also
reports that "[r]ecent excavation has revealed the possibility of a
large-scale fire in Vidisha... attributed by some historians to Chandragupta
Maurya," explicitly flagged in the source itself as a cause not understood
(Shrivastav and Verma 35) [same file and page] — recorded here as
uncertain, not settled, exactly as the source presents it.

**The Śuṅgas and the Heliodoros pillar — the chapter's single most
load-bearing episode.** Pushyamitra Śuṅga overthrew the last Mauryan king,
Bṛhadratha, in 187 B.C.; he and his son Agnimitra, viceroy at Vidisha, are
independently attested by copper coins reading "Vedisa" in Brāhmī characters
contemporary with Aśokan script (Shrivastav and Verma 35–36) [same file; sec.
"Vidisha as a City State"; OCR p.35–36]. Two independent sources in this
corpus describe the Heliodoros/Garuḍa-pillar episode in different wording:
the Gazetteer states that under King Bhāgabhadra, "the Greek king
Antialcidas of Taxila sent Dion's son Heliodorus as his personal ambassador
to the Sunga court at Vidisha," and that the surviving inscription "records
the erection of this pillar in the fourteenth year of king Bhagabhadra's
reign by Heliodorus, who himself was a Vaishnava" (Shrivastav and Verma 37)
[same file; OCR p.37]. Patil's independent account gives the same core
facts — Heliodoros as ambassador from Antialcidas of Takshashila to
Bhāgabhadra's court, the Brāhmī inscription naming him a Bhāgavata convert,
the pillar known locally as "Kham Baba" — and adds that the site has yielded
"three free-standing statues of Yakshinis, a colossal statue of Kubera,"
and images of Durgā, the Seven Mothers, and Nṛsiṃha, most now in the Gwalior
museum (Patil 112) [File: `The cultural heritage of madhya bharat.md`; sec.
"2 Besnagar"; OCR p.112]. The Gazetteer additionally reports a second,
separate inscription — "in early Brahmi characters, dated in the 12th year
of King Bhagvata" — recording a flagstaff dedicated to Viṣṇu by a private
individual, Gautamiputra (Shrivastav and Verma 37) [same file; OCR p.37],
and the discovery of an elliptical Vishnu temple at the same site, read as
the earliest archaeological evidence of Vaiṣṇava worship in the region,
possibly as early as the 3rd century B.C. (Shrivastav and Verma 37) [same
file and page].

**The Guptas and Udaygiri.** Patil describes 20 rock-cut caves on the
Udaygiri hill, two (Nos. 1 and 20) Jain, the rest largely Hindu — Cave 4
("Bina cave," for its carved lute-player), and Cave 5, "the most important,"
for its Varāha (boar) incarnation relief showing Viṣṇu raising the earth
goddess Pṛthvī from the ocean, "of profound interest to the history of the
sculpture of the Gupta period of the 4th to 5th century A.D." (Patil 113)
[File: `The cultural heritage of madhya bharat.md`; sec. "3 Udaygiri"; OCR
p.113]. Caves 6, 7, and 20 carry Gupta-period inscriptions (Patil 114) [same
file and section]. The Gazetteer separately records, via the Allahabad
Pillar inscription, that Samudragupta defeated two Nāga rulers (Gaṇapatinaga
and Nāgasena) in this general theatre and that his son Chandragupta II later
married a Nāga princess, Kubernāgā (Shrivastav and Verma 40) [File: `Vidisha
Gazeteer.md`; sec. "The Imperial and the Later Guptas"; OCR p.40].

#### Ch3.4 Relevant excerpts and passage references

| ID | MLA citation | Excerpt / substance | Classification | Technical trace | Caveats |
|---|---|---|---|---|---|
| CH3-E01 | (Shrivastav and Verma 33) | Palaeolithic tools in the Betwa/Bina/Dhasan/Keothan valleys; Chalcolithic ware dated 1000–700 B.C. | Direct evidence for the chapter's regional-historical subject | [`Vidisha Gazeteer.md`; sec. "CHAPTER II HISTORY"; OCR p.33] | Gazetteer's own footnotes cite ASI Annual Reports 1959–65, not independently checked |
| CH3-E02 | (Shrivastav and Verma 34) | Two major trade routes crossing at Vidisha, naming Pratiṣṭhāna, Mahishmati, Ujjayinī, Kauśāmbī, Bharukaccha, Sūrpāraka, Mathurā | Direct evidence for the chapter's regional-historical subject | [same file and page] | — |
| CH3-E03 | (Shrivastav and Verma 33) | Purāṇic *tīrtha* reference and Anguttara Nikāya placement in Avanti Janapada before the Buddha | Direct evidence; the clearest "ancient texts" / "sacred centre" basis in this chapter | [same file; OCR p.33] | SKP-13's own Purāṇa text not independently cross-checked this pass |
| CH3-E04 | (Shrivastav and Verma 35) | Aśoka's marriage to Devī of Vidisha; son Mahendra, daughter Saṅghamitrā, Buddhist missionaries to Ceylon | Direct evidence for the chapter's regional-historical subject | [`Vidisha Gazeteer.md`; sec. "The Mauryas"; OCR p.35] | — |
| CH3-E05 | (Shrivastav and Verma 35) | Possible large-scale fire at Vidisha, "attributed by some historians to Chandragupta Maurya" | Potential/unverified connection — source itself hedges ("the reason is not known") | [same file and page] | Explicitly uncertain in the source; not to be stated as settled |
| CH3-E06 | (Shrivastav and Verma 37) | Heliodoros/Garuḍa-pillar inscription, Antialcidas's embassy to Bhāgabhadra's court | Direct evidence; primary-epigraphic content described in a secondary survey | [`Vidisha Gazeteer.md`; OCR p.37] | — |
| CH3-E07 | (Patil 112) | Independent account of the same pillar/inscription, plus the Yakshini/Kubera/Durgā finds at the site | Direct evidence; corroborates CH3-E06 from a second source | [`The cultural heritage of madhya bharat.md`; sec. "2 Besnagar"; OCR p.112] | — |
| CH3-E08 | (Shrivastav and Verma 37) | Second Brāhmī inscription (12th year of Bhāgavata) recording a Viṣṇu flagstaff; elliptical Vishnu temple, possibly 3rd c. B.C. | Direct evidence | [same file and page] | — |
| CH3-E09 | (Patil 113) | Udaygiri caves: Cave 4 ("Bina cave"), Cave 5's Varāha relief, dated to the Gupta 4th–5th c. A.D. | Direct evidence for the chapter's regional-historical subject | [`The cultural heritage of madhya bharat.md`; sec. "3 Udaygiri"; OCR p.113] | — |
| CH3-E10 | (Shrivastav and Verma 40) | Samudragupta's Allahabad Pillar inscription; Chandragupta II's marriage to the Nāga princess Kubernāgā | Direct evidence for the chapter's regional-historical subject | [`Vidisha Gazeteer.md`; sec. "The Imperial and the Later Guptas"; OCR p.40] | — |

No fixed excerpt count was applied. Eight live retrieval queries plus direct
reading of two sources (roughly 8 OCR pages of continuous gazetteer text,
plus the parallel Patil sections) produced this set — substantially deeper
than kb3's prior old-C1/old-C4 bucket excerpts, which leaned on TIW-E/INT-GEO
impressionistic material rather than the two sources' own footnoted
chronological accounts.

#### Ch3.5 Scholarly interpretations and disagreements

- No direct contradiction was found between GAZ-VID and PAT-CH this pass —
  where they overlap (the Heliodoros episode), they corroborate each other
  in independently-worded form, which is itself worth noting as two-source
  agreement rather than one book copying the other (the wording differs
  enough, and PAT-CH adds artifact detail the Gazetteer omits, that
  independent authorship is plausible, though not proven here).
- The Chandragupta-Maurya-fire attribution (CH3-E05) is explicitly
  source-flagged as uncertain, not a scholarly dispute between named
  positions — recorded as such.

#### Ch3.6 Research gaps and missing evidence

- This chapter still does not establish any *direct* textual or
  archaeological link between the deep Vidisha history above and Udaypur
  itself — the chapter's own brief frames this material as "the wider
  historical setting for Udaypur," not as evidence about Udaypur, and this
  document preserves that distinction rather than implying a connection the
  sources don't make.
- SKP-13's own Purāṇic *tīrtha* passage (behind CH3-E03) was not read
  directly this pass, only referenced via the Gazetteer's citation of it —
  a direct read is still owed.
- `Bhoja Paramara and His Times` (SIN-B) carries background-era material in
  kb3's old-C4 bucket that was not examined this pass, since the source is
  unindexed (Part B) and the material appeared, on a first look, to concern
  the Paramāra period rather than the pre-Paramāra setting — this judgment
  has not been independently verified by reading the file directly.
- The Adam Hardy passage on Udayagiri's rock-cut architecture (HAR) was seen
  only as a retrieval snippet, not read in full context — flagged for a
  follow-up pass, particularly for Ch5's cross-reference to architectural
  style.

#### Ch3.7 Drafting utility

- CH3-E01–E04 give the chapter a clean prehistory-to-early-historic
  narrative arc and can open the chapter in sequence.
- CH3-E06/E07 (two-source corroborated) is the chapter's strongest set-piece
  and should be presented as such — a rare case in this corpus of
  independent corroboration rather than a single-source claim.
- CH3-E09/E10 set up Ch5's architectural discussion (Gupta-era rock-cut
  precedent for later Paramāra-era stone building) and should be
  cross-referenced forward once Ch5 exists.
- Before publication: read SKP-13's Purāṇa text directly rather than via the
  Gazetteer's citation of it; confirm SIN-B's old-C4 content is genuinely
  out of scope for this chapter rather than assumed so.

### Ch4 — The Paramāras and the Foundation of Udaypur: Kingship, Patronage and Urban Formation

#### Ch4.1 Chapter scope and research questions

Per `chapters.md`: "Examine the political development of the region, the
rise of the Paramāras, the reign and legacy of Bhoja, and Udayāditya's role
in establishing and shaping Udaypur. Situate the town's foundation within
the history of Paramāra kingship, religious patronage and temple building,
distinguishing established evidence from later tradition." Per the chapter's
own annotation ("Remaining C5 + C6 + C7"), this chapter absorbs the medieval
Paramāra dynastic chronology that Ch3 deliberately excluded, plus kb3's old
C6 (Udayāditya's Foundation). Udaypur's own identity and naming (the
inscription's triple-naming Udayapura/Udayeśvara/Udayasāmudra) was already
established in Ch1 with full citations — this chapter cross-references that
rather than repeating it, and instead focuses on the dynastic politics
around the founder himself: the succession from Upendra through Bhoja, and
the two genuinely contested questions about Udayāditya that the chapter's
own brief explicitly calls for ("distinguishing established evidence from
later tradition") — his accession date, and his exact relationship to Bhoja.

#### Ch4.2 Relevant sources

- **`History of Paramara Dynasty DC Ganguly.md`** (GAN, reliability 0.90).
  Direct evidence — the standard scholarly dynastic history, heavily
  footnoted. Read directly, several sections.
- **`Inscriptions Corpus.md`** (uncoded in kb3; Trivedi's ASI edition).
  Direct evidence, primary-epigraphic — and the single most valuable source
  found for this chapter. Contains the actual Dongargaon and Jainad
  inscriptions of Jagaddēva and the Pānāhēḍā inscription of Māṇḍalika, with
  Trivedi's own detailed scholarly analysis of the Udayāditya–Bhoja
  relationship and the 1059 CE dating question — material kb3 never had
  access to, since this source carries no kb3 code at all (Part B.4). Read
  directly and extensively this pass.
- **`History of the Parmar Rajput Dynasty.md`** (PAR, reliability 0.40 per
  kb3; confirmed as the Venziya/IJMR article via DOI match, Part B). Direct
  evidence for the dynasty's early succession list (Upendra onward), though
  kb3's own low reliability score — "presents the agnikula myth as
  validated history" — is retained as a caution on anything beyond the bare
  succession list.
- **`Some Paramara Templess.md`** (ADH, reliability 0.75). Direct evidence
  for Bhoja's reign and the succession crisis after Jayasiṃha I's death —
  independently corroborates Udayāditya's dates and the circumstances of his
  accession.
- **`Raja_Bhoj_Aur_Parmarkaleen_EN.md`** (RAJ-E, reliability 0.65). Direct
  evidence for Bhoja's literary patronage and the scope of his own authorial
  output; translated from Hindi, register is popular-scholarly rather than
  primary.
- **`Vidisha Gazeteer.md`** (GAZ-VID) and **`The cultural heritage of madhya
  bharat.md`** (PAT-CH) — both already used in Ch1/Ch3; here they supply the
  Siyaka II/Paramāra-conquest-of-Malwa framing (GAZ-VID, "Paramaras" section)
  and corroborate the foundation-inscription dating already established in
  Ch1 (not repeated here).
- **`भोजदेव (Bhojadeva)`** (BHJ-H) and **`Bhoja Paramara and His Times`**
  (SIN-B) — kb3's old C5 bucket leaned heavily on both (BHJ-H supplying
  several Devanagari excerpts on Bhoja's titles and works, SIN-B 23% of the
  old C5 bucket by volume). SIN-B is confirmed unindexed (Part B) and was
  not read directly this pass; BHJ-H's Devanagari material on Bhoja's
  titles/scholarship was not independently re-verified this pass either —
  both flagged as gaps below rather than re-asserted secondhand from kb3's
  excerpts.
- **`Jagta_Hua_Kasba_EN.md`** (TIW-E) — carries the Udayāditya–Bhoja kinship
  question in popular-reportage register, quoting the same Nagpur praśasti
  verse Trivedi analyzes more rigorously in `Inscriptions Corpus.md`. Used
  below only as a secondary pointer, not as the primary basis for the claim.
- **`RAJM`** — kb3 itself flags this as barely represented in old C5/C6; not
  indexed in the active corpus (Part B) and not examined this pass.
- **`Art of Paramaras.md`** (uncoded in kb3; see Part B.4, Ch5.2). Searched
  directly this revision. Regional/comparative evidence only — this
  source is art-historical, not dynastic-political, but independently
  corroborates Udayāditya's reign epigraphically (via the Un Jaina
  temples) and extends the post-Udayāditya succession narrative with a
  Chālukya conquest under Jayasiṃha Siddharāja, not previously captured
  in this chapter.

#### Ch4.3 Facts, figures, and evidence

**The dynasty's rise.** The Paramāra line is traditionally traced to
Upendra (c. A.D. 800–818) (Venziya 3) [File:
`History of the Parmar Rajput Dynasty.md`; sec. "Upendra (AD 800 to 818)";
OCR p.3]. Siyaka II (Harṣa) founded an independent Paramāra kingdom in
Malwa, ousting the Chandēllas, with "known date... A.D. 972" (Shrivastav and
Verma 42) [File: `Vidisha Gazeteer.md`; sec. "Paramaras"; OCR p.42]. His
adopted son and successor Vākpati Muñja (973–995 per Venziya; 974–995 per
Ganguly; the sources differ on the exact year — see Ch4.5) defeated the
Kalachuri ruler Yuvarāja II and the Chaulukya Taila before ultimately losing
his life to Taila II (Venziya 4) [same file; sec. "Vakpati II and
Sindhuraj"; OCR p.4]. Sindhurāja succeeded his brother and was in turn succeeded by
his son Bhoja.

**Bhoja's reign and legacy.** Bhoja reigned roughly 1000–1055 A.D. (Ganguly)
[File: `History of Paramara Dynasty DC Ganguly.md`; exact page not
re-confirmed this pass]. He is credited with an extensive authorial output —
the *Samarāṅgaṇa-sūtradhāra*, *Śṛṅgāra-mañjarī-kathā*, *Sarasvatī-
kaṇṭhābharaṇa*, and several Āyurvedic works including the *Rāja-mārtaṇḍa-
yoga-sāra-saṅgraha* (Rajpurohit 1) [File: `Raja_Bhoj_Aur_Parmarkaleen_EN.md`;
sec. "King Bhoj (राजा भोज)"; OCR p.1]. He founded the Bhojaśālā, a Sanskrit
learning institution at his capital Dhāra, with grammatical charts and
alphabetical diagrams inscribed on its pillars — of which the "sarpabandha"
(serpent-coil) chart found at Un is a provincial parallel (Trivedi 149–150)
[File: `Inscriptions Corpus.md`; sec. "ÜN SARPABANDHA INSCRIPTION"; OCR
p.149–150] — directly comparable to the Udaypur "serpentine scimitar"
inscription discussed in Ch6. His conflicts extended north to the
Cāhamānas of Śākambharī (Ajmer) and the Chamba princes of the Punjab, and
south toward Kanauj after the Kalachuri Karṇa's death (Ganguly 122–125)
[File: `History of Paramara Dynasty DC Ganguly.md`; sec. "WAR WITH THE
CHAMBA PRINCE"/"WAR WITH THE CÂHAMÂNAS..."; OCR p.122–125].

**Udayāditya's accession — a genuinely contested date, not a settled fact.**
Two inscriptions, both independently present in this corpus, bear directly
and in tension on this question. The Pānāhēḍā (Panhera) inscription of
Māṇḍalika, a Paramāra feudatory ruling Vāgaḍa, is dated "Vikrama 1116...
correspond[ing] to 1059 A.C." and explicitly records that its overlord at
that date was **Jayasiṃha**, not Udayāditya — the inscription states that
"Jayasinhā assigned to the deity... some grants," naming Jayasiṃha as the
sovereign making royal land-grants in that very year (Trivedi 421–424)
[File: `Inscriptions Corpus.md`; sec. "PĀNĀHĒḌĀ STONE INSCRIPTION OF
MĀḌALIKA"; OCR p.421–424]. Yet the Udaypur foundation inscription itself
(Ch1, CH1-E01/E02) dates Udayāditya's own construction at Udaypur to this
same year, V.S. 1116 / A.D. 1059. Ganguly's resolution, and the one kb3's
prior synthesis also adopted, is that Udayāditya held and built at his
paternal territory (Udaypur) in 1059 without yet holding the paramount Malwa
throne, which remained Jayasiṃha's. This document records that reconciliation
as the prevailing scholarly view, not as an independently-attested fact —
no single inscription in this corpus states it directly.

**Udayāditya's relationship to Bhoja — three primary witnesses, two
scholarly readings, and a clear rejection of a fourth.** This corpus
contains direct textual access to the dispute, not just a secondary summary
of it. (1) The Nagpur Museum stone inscription of Naravarman calls
Udayāditya a *bandhu* of Bhoja — a term Trivedi, following Kielhorn, reads
as "a relative in general," not specifically a brother (Trivedi 152) [File:
`Inscriptions Corpus.md`; sec. "DŌNGARGĀON STONE INSCRIPTION OF THE TIME OF
JAGADDĒVA"; OCR p.152]. (2) The Dongargaon inscription of Jagaddēva (Śaka
1034 / A.D. 1112) introduces "Bhōja's brother Udayāditya" in its own verses
5–6, which Trivedi reads as stating "Udayāditya's definite relationship with
Bhōja" in the sense of an actual brother, not merely a loose kinsman
(Trivedi 151–152) [same file; sec. "DŌNGARGĀON STONE INSCRIPTION..."; OCR
p.151–152]. (3) The Jainad inscription of the same Jagaddēva separately
calls Bhoja his *pitṛvya* (paternal uncle) — consistent with reading
Udayāditya as Bhoja's actual brother, since that would make Bhoja uncle to
Udayāditya's son. Trivedi's own scholarly judgment, stated explicitly,
**rejects** a fourth witness — a sixteenth-century inscription (V.S. 1562)
making Udayāditya "the son of Gyātā, grandson of Gōndala and great-grandson
of Śūravīra" — as too late and "has to be rejected" in favor of the
Dongargaon inscription's direct "brother" statement (Trivedi 152) [same file
and page]. This is a genuine scholarly judgment call, not a consensus: it
directly contradicts the reading (Udayāditya as a cousin-level kinsman from
a junior branch, descended from Gyātā) that this document's own prior-layer
notes show was favoured elsewhere (see Ch4.5). **No primary witness anywhere
in this corpus calls Udayāditya Bhoja's nephew** — that reading appears only
in `Bhoja Paramara and His Times` (Singh 1984), a source this document
cannot currently verify directly since it is unindexed (Part B), and which
kb3's own prior reliability judgment already flagged as unsupported by any
primary inscription.

**Succession after Udayāditya.** Lakṣmadeva, his elder son, "closed his
reign some time before 1094 A.D." and was succeeded by his younger brother
Naravarman, who took the epithet Nirvāṇa-Nārāyaṇa (Ganguly 72) [File:
`History of Paramara Dynasty DC Ganguly.md`; sec. "WAR WITH THE KIRAS"/
"NARAVARMAN"; OCR p.72]. Jagaddēva, a third son, is "not mentioned in any of
the Paramāra records except" the Dongargaon and Jainad inscriptions
themselves, though Hoysaḻa inscriptions independently describe him as a king
of Mālava (Trivedi 152) [File: `Inscriptions Corpus.md`; same section; OCR
p.152] — Trivedi explicitly distinguishes Jagaddēva from Lakṣmadeva, against
Ganguly's own earlier suggestion that the two were the same person, citing
the Dongargaon inscription's statement that Jagaddēva voluntarily
relinquished the throne to a brother (Trivedi 152) [same file and page] —
**a direct, named disagreement between two scholars in this corpus's own
sources**, not an inference.

**`Art of Paramaras.md` searched directly (closing a previously-flagged
Part F gap).** This source is overwhelmingly an art-historical survey, not
a dynastic-political history, so it adds comparatively little to this
chapter's central questions — but two points are directly relevant. First,
it independently corroborates that the Jaina temples at Un were "built
during the reign of the later Paramāra kings of Mālwā... confirmed by the
two inscriptions of Udayāditya and a Sarpabandha inscription of
Naravarman" (uncertain author) [File: `Art of Paramaras.md`; sec. "UN—AN
IMPORTANT CENTRE OF PARAMĀRA ART AND ARCHITECTURE"; OCR p.25] — a minor,
regional corroboration that Udayāditya's reign is epigraphically attested
beyond Udaypur itself. Second, and more substantively: "Jayasimha
Siddharāja, a Chālukya ruler of Gujrat, is known to have defeated
Naravarman and his successor Yasovarman. As a consequence of it, a great
part of the Paramāra dominions was seized by the Chālukyas. During the
reign of his successor Kumārapāla, Mālwā once again became a Chālukya
province" (uncertain author) [same file and page] — **this extends the
succession narrative already given in Ch4.3 above (Lakṣmadeva →
Naravarman) one generation further, naming a Chālukya conquest that
stripped Paramāra territory before the dynasty's final 1305 end** (see
Ch10). This is regional/comparative evidence — about the dynasty broadly,
not Udaypur specifically — but directly useful for situating Udayāditya's
own successors.

#### Ch4.4 Relevant excerpts and passage references

| ID | MLA citation | Excerpt / substance | Classification | Technical trace | Caveats |
|---|---|---|---|---|---|
| CH4-E01 | (Venziya 3) | Upendra, c. 800–818 A.D., as the dynasty's traditional founder | Direct evidence | [`History of the Parmar Rajput Dynasty.md`; sec. "Upendra (AD 800 to 818)"; OCR p.3] | Low source reliability (kb3: 0.40) — treat the bare succession fact as more reliable than any interpretive claim from this source |
| CH4-E02 | (Shrivastav and Verma 42) | Siyaka II founds an independent Paramāra kingdom in Malwa, A.D. 972 | Direct evidence | [`Vidisha Gazeteer.md`; sec. "Paramaras"; OCR p.42] | — |
| CH4-E03 | (Rajpurohit 1) | Bhoja's authorial works: *Samarāṅgaṇa-sūtradhāra*, *Śṛṅgāra-mañjarī-kathā*, *Sarasvatī-kaṇṭhābharaṇa*, Āyurvedic works | Direct evidence | [`Raja_Bhoj_Aur_Parmarkaleen_EN.md`; sec. "King Bhoj (राजा भोज)"; OCR p.1] | Translation from Hindi; not cross-checked against the two active Samarāṅgaṇa-sūtradhāra files |
| CH4-E04 | (Trivedi 149–150) | The Un "sarpabandha" grammar chart, a provincial parallel to Bhoja's Bhojaśālā charts at Dhār | Regional/comparative | [`Inscriptions Corpus.md`; sec. "ÜN SARPABANDHA INSCRIPTION"; OCR p.149–150] | — |
| CH4-E05 | (Trivedi 421, 424) | Pānāhēḍā inscription, V.S. 1116 = A.D. 1059, recording Jayasiṃha (not Udayāditya) as the sovereign making grants that year | Direct evidence; primary-epigraphic; the key counter-evidence for the accession-date question | [`Inscriptions Corpus.md`; sec. "PĀNĀHĒḌĀ STONE INSCRIPTION OF MĀḌALIKA"; OCR p.421, p.424] | — |
| CH4-E06 | (Trivedi 152) | *Bandhu* (Nagpur inscription) read by Trivedi/Kielhorn as "a relative in general" | Direct evidence; primary-epigraphic, with editorial interpretation | [`Inscriptions Corpus.md`; sec. "DŌNGARGĀON STONE INSCRIPTION..."; OCR p.152] | Interpretation is Trivedi's/Kielhorn's, not a plain fact |
| CH4-E07 | (Trivedi 151–152) | Dongargaon inscription's "Bhōja's brother Udayāditya" (vv. 5–6), read by Trivedi as a literal brother relationship | Direct evidence; primary-epigraphic | [same file; sec. "DŌNGARGĀON STONE INSCRIPTION..."; OCR p.151–152] | Trivedi's reading is contested by other scholarship (see Ch4.5); not the only possible reading of the verse |
| CH4-E08 | (Trivedi 152) | Trivedi's explicit rejection of the V.S. 1562 "Gyātā/Gōndala/Śūravīra" genealogy as too late and unreliable | Contradictory/qualifying evidence — a scholar's explicit dismissal of a rival primary witness | [same file and page] | This is Trivedi's judgment call, presented as such, not adopted as this document's own conclusion |
| CH4-E09 | (Trivedi 152) | Trivedi's distinction of Jagaddēva from Lakṣmadeva, against Ganguly's earlier identification of the two as one person | Contradictory/qualifying evidence — a named scholarly disagreement | [same file and page] | Both named positions (Ganguly's and Trivedi's) are preserved; neither is adopted as settled |
| CH4-E10 | (Ganguly 72) | Lakṣmadeva's reign ends before 1094 A.D.; succeeded by younger brother Naravarman (epithet Nirvāṇa-Nārāyaṇa) | Direct evidence | [`History of Paramara Dynasty DC Ganguly.md`; sec. "NARAVARMAN"; OCR p.72] | — |
| CH4-E11 | (uncertain author) | Un Jaina temples confirmed by "two inscriptions of Udayāditya and a Sarpabandha inscription of Naravarman" | Regional/comparative; epigraphic corroboration | [`Art of Paramaras.md`; sec. "UN—AN IMPORTANT CENTRE OF PARAMĀRA ART AND ARCHITECTURE"; OCR p.25] | Author's name illegible in OCR |
| CH4-E12 | (uncertain author) | Jayasiṃha Siddharāja (Chālukya) defeats Naravarman and Yaśovarman; Malwa seized by the Chālukyas, later restored under Kumārapāla | Regional/comparative; extends the succession narrative one generation beyond CH4-E10 | [same file and page] | Author's name illegible in OCR; cross-reference Ch10 |

No fixed excerpt count was applied. Six live retrieval queries plus direct
reading of `Inscriptions Corpus.md`'s Dongargaon, Jainad, Un-sarpabandha, and
Pānāhēḍā entries — a source with no kb3 code at all — produced the chapter's
strongest material, well beyond what kb3's prior bucket (dominated by SIN-B
and SAM) had captured. A later revision added CH4-E11/E12 from a direct
search of `Art of Paramaras.md`, closing a gap flagged in Part F.

#### Ch4.5 Scholarly interpretations and disagreements

This chapter has the corpus's richest set of genuine, named disagreements:

- **Udayāditya's accession date.** Not settled. The Udaypur foundation
  inscription (1059 CE) and the Pānāhēḍā inscription (also dated to 1059 CE,
  naming Jayasiṃha as sovereign) are not contradictory if Udayāditya held
  only his paternal territory in 1059 without yet holding the Malwa throne —
  this reconciliation is the prevailing view in the secondary literature
  this document consulted (Ganguly; kb3's prior synthesis), but it is an
  inference, not a fact independently stated by any single source.
- **Udayāditya's relationship to Bhoja.** Three primary epigraphic witnesses
  use three different kinship terms (*bandhu*, *bhrātā*, *pitṛvya*).
  Trivedi's considered judgment (Ch4.3, CH4-E06–E08) favors reading
  Udayāditya as Bhoja's actual brother and explicitly rejects the rival
  "cousin from a junior branch, son of Gyātā" genealogy as a late and
  unreliable witness. This document does not adopt Trivedi's reading as
  settled fact — it is one scholar's considered judgment against a specific
  named rival inscription, not a scholarly consensus — but it is the most
  rigorously argued position found in this corpus, and should be presented
  as such, clearly distinguished from the unsupported "nephew" reading
  (Singh 1984), which no primary witness anywhere in this corpus supports.
- **Jagaddēva vs. Lakṣmadeva.** Trivedi explicitly argues against Ganguly's
  earlier identification of the two as the same person (CH4-E09) — a named,
  citable disagreement between two scholars, not a vague "sources disagree."

#### Ch4.6 Research gaps and missing evidence

- `Bhoja Paramara and His Times` (SIN-B) — the single source that calls
  Udayāditya Bhoja's "nephew" — is unindexed and was not read directly this
  pass (Part B). Its claim is recorded above only via kb3's prior citation,
  not independently re-verified; a direct read of this source, were it ever
  added to the active corpus, would be the natural next step before treating
  this question as closed.
- BHJ-H's (`bhojdev.md`) Devanagari material on Bhoja's titles and
  scholarly output, heavily used in kb3's old C5 bucket, was not
  independently re-read this pass — flagged, not re-asserted secondhand.
  The two active Samarāṅgaṇa-sūtradhāra files were likewise not searched
  directly for corroboration of CH4-E03's list of Bhoja's own works.
- Munja's exact reign dates differ across sources consulted this pass
  (973–995 per PAR; 974–995 per GAN) — a minor discrepancy, not
  independently resolved here, flagged rather than silently picking one.
- This chapter does not re-establish Udaypur's own naming/foundation facts,
  which are already fully cited in Ch1 (CH1-E01–E03) — readers should
  cross-reference there rather than expect it repeated here.

#### Ch4.7 Drafting utility

- CH4-E05/E06/E07/E08 together form the chapter's central set-piece — the
  two contested questions about Udayāditya — and should be presented as
  genuinely open scholarly questions with the primary evidence laid out for
  the reader, exactly matching the chapter's own brief ("distinguishing
  established evidence from later tradition").
- CH4-E09 (Jagaddēva vs. Lakṣmadeva) is a good, concrete illustration of how
  this book's sources sometimes disagree by name, useful methodologically
  even if the detail itself is minor.
- Before publication: attempt to locate and read `Bhoja Paramara and His
  Times` directly if it is ever added to the active corpus, since it is the
  sole source for the "nephew" reading this chapter must explicitly set
  aside; cross-check BHJ-H and the two SAM files directly for Bhoja's
  authorial-works list.

### Ch5 — The Udayeśvara Temple: Architecture, Sculpture and Religious Iconography

#### Ch5.1 Chapter scope and research questions

Per `chapters.md`: "Study the temple's architectural plan, construction,
stylistic features, sculptural programme, deities and iconography. Interpret
the monument within the religious and artistic traditions of its period,
distinguishing architectural description from interpretations of its
symbolism." This maps cleanly onto kb3's old-C7 bucket ("Udayeśvara in
Stone"), the single largest bucket in the prior build (4,197 chunks, 23
sources, no source-domination problem flagged by kb3 itself). Per the
chapter's own brief, this chapter must keep two registers visibly separate:
(1) what can be directly observed and measured about the building, and (2)
what a given author argues it *means*. Research questions: what is the
temple's physical plan and construction sequence; what distinguishes the
Bhūmija style it exemplifies; what deities and sculptural themes does its
surface carry; and which claims about its religious-philosophical meaning
(e.g. a specific Śaiva Siddhānta theology) are a named scholar's
interpretation rather than an architectural fact.

#### Ch5.2 Relevant sources

- **`The Udayesvara Temple - Anupa Pande.md`** (PAN, reliability 0.85; this
  pass resolved which of the two active copies kb3's citations trace to —
  Part B). Direct evidence — the primary modern monograph on the building
  itself, with the fullest architectural and sculptural description in the
  corpus. Read directly and extensively this pass.
- **`The Udayesvara Temple Art, Architecture and Philosophy of the Saiva
  Siddhanta.md`** — the second active OCR copy of the same monograph.
  Citable independently per this document's duplicate-OCR policy (Part B),
  though not separately re-read this pass since its content is the same
  underlying text as PAN above.
- **`The Hindu Temple Vol 1 Stella Kramrisch.md` / `...Vol 2`** (KRAM-1/2,
  reliability 0.90). General contextual/comparative evidence — places the
  temple within a national account of temple form, explicitly naming it
  ("Nilakaṇṭheśvara temple... Udayapur, Gwalior") in several passages.
- **`806955603-The-Temple-Architecture-of-India-Adam-Hardy.md`** (HAR,
  reliability 0.90) and **`Temples of India.md`** (DEV) — general
  contextual/comparative, situating the Bhūmija style nationally.
- **`Some Paramara Templess.md`** (ADH, reliability 0.75). Regional/
  comparative — its Un temple cluster is the closest comparandum for
  Bhūmija construction technique and decay, and it explicitly places the
  Udayeśvara temple as the style's "grandest specimen."
- **`The cultural heritage of madhya bharat.md`** (PAT-CH) and **`Intach
  Udaypur (1).md`** (INT-ARC) — already used in Ch1; here they supply
  additional sculptural/monument detail not repeated from that chapter.
- **`Skanda-Purāṇa Part XIII`** (SKP-13) — kb3's old-C7 bucket draws on this
  heavily for generic Śiva-liṅga glorification material (e.g. "by
  glorifying the Linga one is rid of sins"). On inspection this is
  Purāṇic devotional material with no identified connection to the
  Udayeśvara temple specifically — general contextual evidence for Śaiva
  devotional literature broadly, not treated as temple-specific evidence
  here.
- **`Samarāṅgaṇa-sūtradhāra`** (`SAM`, split across two active files) — the
  Śilpaśāstra Pande's own Introduction credits as the earliest text to
  describe the Bhūmija style; its general architectural-geometry chapters
  (proportions, mouldings) are genuinely relevant here, unlike in Ch2/Ch3,
  but were not independently cross-checked against the two active SAM files
  this pass — flagged as a gap.
- **`Art of Paramaras.md`** (uncoded in kb3; see Part B.4). **Searched
  directly this revision** (previously flagged in Part F as never reached
  by any chapter). Direct Udaypur evidence — this file contains two
  distinct, dedicated articles: a Hindi-language piece titled "उदयपुर का
  उदयेश्वर मंदिर" ("The Udayeśvara Temple of Udaypur") by **Kamala Mittal**,
  giving measurements, dates, and sculptural detail not found anywhere
  else in this corpus; and a second Hindi survey article on major
  Paramāra-period temples of Malwa, whose author's name is badly
  OCR-corrupted in the extracted text ("मुशील कुमार मुल्लेरे" — rendered
  here exactly as it appears, not confidently identified as a real name),
  which repeatedly uses the Udaypur temple as the chronological/stylistic
  benchmark for dating comparable temples elsewhere. **OCR quality in both
  articles is poor** — frequent repeated phrases and corrupted characters,
  consistent with this file's generally weak OCR already noted in Phase
  B1 (the book's English acknowledgments section was similarly garbled).
  Quotations below are limited to clearly legible fragments; longer
  stretches are paraphrased and explicitly marked as such.

#### Ch5.3 Facts, figures, and evidence — architectural description

**Dating and founder (cross-reference, not repeated in full from Ch1/Ch4).**
Pande's own Introduction states Udayāditya "ascended the throne in 1070 CE,"
which corroborates one specific value within the four-way contested range
already documented in Ch4 (the "c. 1070–1093, from the coinage" reading) —
a fifth source converging on that same end of the range, worth noting as
additional (though not conclusive) support for it (Pande 8) [File: `The
Udayesvara Temple - Anupa Pande.md`; sec. "INTRODUCTION"; OCR p.8].

**Architectural plan.** The temple is built of red sandstone, faces east,
and consists of a *garbhagṛha* (sanctum), *antarāla* (vestibule), a
*gūḍhamaṇḍapa* (covered hall) with three *mukhamaṇḍapas* (porches), and a
separate *vedī* hall on the same axis; it stood on a *jagatī* platform and
was originally surrounded by eight subsidiary shrines (Pande 9) [File: `The
Udayesvara Temple - Anupa Pande.md`; sec. "UDAYEŚVARA TEMPLE"; OCR p.9]. The
original entrance was a stairway flanked by over-life-size *dvārapāla*
figures; the current entrance is from the west. The sanctum is
stellate-cum-circular in plan, *saptaratha* (seven-projection) on plan and
*saptabhūmi* (seven-storey) in elevation (Pande 9) [same file and page].

**The Bhūmija style — definition and significance.** The style's
distinctive feature is a *śikhara* with four *latās* (spines) bearing
*caitya*-arch motifs, with miniature *śikharas* of diminishing height
(*kūṭastambhas*) arranged in rows between the *latās*, and a large *caitya*
medallion (*śūrasenaka*) at the base of three of the four *latās*; this
class of temple is invariably *nirandhāra* (without ambulatory) (Pande 8)
[same file; OCR p.8]. Pande identifies the *Samarāṅgaṇa-sūtradhāra* of
Bhoja Paramāra as "one of the earliest Śilpaśāstras that refers to the
Bhūmija style," argues the Paramāras likely developed the style to its
mature form, and glosses "Bhūmija" ("earth-born") as plausibly denoting
either a regional (Malwa-native) style or a style of "secular," terrestrial
origin as opposed to styles with claimed divine origin (Pande 8) [same file
and page] — **this etymological gloss is Pande's own interpretation, not an
attested textual definition**, and is presented here as such. Adhikari
independently calls the Udayeśvara temple "the grandest specimen of
Paramāra architecture" and corroborates the 1059–1080 construction span
(Adhikari; Deva) [File: `Some Paramara Templess.md`; exact page not
re-confirmed this pass — carried from kb3's prior citation].

**Mouldings and ornamentation.** The base (*pīṭha*) has five mouldings in
sequence — *bhiṭṭa* 1 (plain), *bhiṭṭa* 2 (leaf-and-garland design),
*jādyakumbha* (an inverted cyma-recta moulding with diamond-and-rosette
banding), *karṇaka* (an arris moulding with a spiral-and-arrow motif), and
*grāsapaṭṭī* (a band of gorgon/*kīrtimukha* heads) — and the *maṇḍovara*
(wall zone) above it comprises the *vedībandha* with its own *khura*,
*kumbha*, and *kalaśa* mouldings (Pande 9–10) [File: `The Udayesvara Temple
- Anupa Pande.md`; sec. "THE ARCHITECTURAL MOULDINGS OF THE EXTERIOR OF THE
PRĀSĀDA AND THEIR ORNAMENTATION"; OCR p.9–10].

**Sculptural programme.** Pande's survey of the *maṇḍovara*'s outer-wall
sculptures includes a three-headed, eight-armed Hariharārkapitāmaha image
(a composite Hari-Hara-Arka-Pitāmaha form), Cāmuṇḍā, Yogeśvarī, and
Māheśvarī images identified in specific niches, with Nandi's presence used
as an iconographic marker to confirm Māheśvarī's identity (Pande) [same
file; sec. "THE MAṆḎOVARA > THE SCULPTURES ON THE OUTER WALLS OF THE
GUḎHAMAṇḎAPA"; exact OCR page not individually re-confirmed this pass for
each image]. Adhikari independently notes Cāmuṇḍā's placement in the
northern quarter at the Udayeśvara temple specifically parallels her
placement at the Māṇḍaleśvara temple at Pānāhēḍā (the same site whose 1059
inscription is central to Ch4's accession-date question) and at Arthūṇā
(Adhikari 54) [File: `Some Paramara Templess.md`; sec. referencing Pānāhēḍā/
Arthūṇā comparanda; OCR p.54] — a genuine cross-site iconographic pattern,
not a claim about Udaypur alone.

**The interpretive layer — explicitly flagged as interpretation, per the
chapter's own instruction.** Pande's monograph argues, in its own
"Notes and References" section, that "[t]he Udayeśvara temple is based on a
Śaiva sect which derives from Śaiva Siddhānta," connecting this to Bhoja
Paramāra's own treatise the *Tattvaprakāśa* and its "virtually canonical
status" for the Northern school of Śaiva Siddhāntins (Pande) [same file;
sec. "NOTES AND REFERENCES > ŚAIVA SIDDHĀNTA"; exact page not re-confirmed
this pass]. **This is Pande's own theological-historical argument, not a
plain architectural fact** — the temple's architecture and sculptural
programme (directly observable) is separable from the claim that it was
conceived to embody a specific, named philosophical school's doctrine (an
interpretive argument resting on textual connections Pande draws, not on
anything inscribed on the building itself). This document preserves that
distinction rather than collapsing the two.

**New measurements from a previously-unused source.** Mittal gives
courtyard dimensions not found in Pande or any other source in this
corpus — the temple complex stands within a "वर्गाकार प्रांगण" (square
courtyard) she gives as approximately 210 × 210 (units not specified in
the legible text, almost certainly feet, paraphrased from surrounding
OCR-damaged text) (Mittal) [File: `Art of Paramaras.md`; sec. "उदयपुर का
उदयेश्वर मंदिर"; OCR p.60–61 — exact page boundary uncertain given the
file's page-marker density]. She separately gives pillar dimensions for
the *sabhā-maṇḍapa*: a square base "दो फीट नौ इंच" (2 feet 9 inches) per
side, with total pillar height "दस फीट पांच इंच" (10 feet 5 inches)
(Mittal) [same file and section] — the only source-stated pillar
measurements found anywhere in this document's research for this temple.

**Independent confirmation of the construction dates and the Tughlaq
attribution — a fourth corroborating source.** Mittal independently states
the construction dates as Samvat 1116 and (a second inscription) Samvat
1137 — matching the 1059/1080 CE dating already established in Ch1 — and
separately states, paraphrased from a heavily repetitive OCR passage, that
surviving inscriptions show a later structure was built "मुहम्मद बिन
तुगलक के आदेश से" (on the order of Muhammad bin Tughlaq), using material
from the temple itself (Mittal) [same file and section]. **This is a
fourth independent source naming Tughlaq**, joining Patil (Ch1), Beglar/
Pande (Ch7), and Tiwari (Ch10) — see Part D.1, now updated.

**A shrine-count variant, and a probably-corrupted date.** Mittal states
that six subsidiary shrines currently stand, with an estimate that the
original number was "आठ या नौ" (eight or nine) — consistent with Patil's
"six now standing" (Ch1) but offering a slightly different original-count
estimate than Pande's consistent figure of eight (Ch5.3 above). Separately,
Mittal's account of the brass face-plate covering the *liṅga* gives a date
that, after accounting for visible OCR repetition in the passage, appears
to read "१७५४" (1754) — **this conflicts with the 1775 date given by
Patil (Ch1) and the Gazetteer for the same object, attributed to the same
named donor (Khanderao Appaji)**. Given the surrounding text's visible
corruption (the same clause repeats itself with shifting errors across
several lines), this document treats the 1754 figure as more likely an
OCR misread of 1775 than a genuine third date, but does not silently
correct it — it is flagged here as an unresolved discrepancy, not
presented as a confirmed third value.

**The Udaypur temple as the region's chronological benchmark.** The
second article in this same file (author's name uncertain, see Ch5.2)
repeatedly uses the Udayeśvara/Nīlakaṇṭheśvara temple as the fixed
reference point for dating and classifying other Paramāra-era temples: the
Un cluster's plan and *śikhara* are described as "सदृश्य" (similar) to it;
the Amareśvara temple at Oṅkār Māndhātā, independently dated 1063 CE
(epigraphically attested per the source), is explicitly compared to it as
a close contemporary; the Jāmlī Mahādeva temple is dated as later than it
by relative stylistic sequence; and the Siddheśvara temple at Nemāwar,
though larger, is explicitly called a representative of "परमार शैली के
ह्रास की अवस्था" (the declining phase of the Paramāra style), implicitly
placing Udaypur's temple earlier in the style's healthier period
(author's name uncertain) [same file; sec. "मालवा के परमारकलीन प्रमुख
मंदिर"; OCR p.57–60]. **This is architectural-stylistic decline, not
political or economic decline** — directly relevant to Ch5's own subject,
but not a substitute for Ch10's political-economic question, which this
source does not address for Udaypur specifically (see Ch10's updated
Ch10.6 below).

#### Ch5.4 Relevant excerpts and passage references

| ID | MLA citation | Excerpt / substance | Classification | Technical trace | Caveats |
|---|---|---|---|---|---|
| CH5-E01 | (Pande 8) | Udayāditya "ascended the throne in 1070 CE" | Direct evidence; corroborates one value in Ch4's contested accession-date range | [`The Udayesvara Temple - Anupa Pande.md`; sec. "INTRODUCTION"; OCR p.8] | A fifth source on an already-contested question — strengthens, but does not settle, the c.1070 reading |
| CH5-E02 | (Pande 9) | Full architectural plan: garbhagṛha, antarāla, gūḍhamaṇḍapa, 3 mukhamaṇḍapas, vedī, 8 subsidiary shrines, jagatī platform | Direct Udaypur evidence; architectural description | [same file; sec. "UDAYEŚVARA TEMPLE"; OCR p.9] | — |
| CH5-E03 | (Pande 8) | Bhūmija style definition: four-latā śikhara, kūṭastambhas, śūrasenaka medallions, nirandhāra construction | Direct Udaypur evidence; also general stylistic description | [same file; OCR p.8] | — |
| CH5-E04 | (Pande 8) | Pande's etymological/interpretive gloss on "Bhūmija" as possibly denoting secular/terrestrial origin | Potential/unverified connection — explicitly the author's own interpretation | [same file and page] | Not an attested textual definition; presented as Pande's argument |
| CH5-E05 | (Pande 9–10) | Five-moulding pīṭha sequence; vedībandha mouldings | Direct Udaypur evidence; architectural description | [same file; sec. "THE ARCHITECTURAL MOULDINGS..."; OCR p.9–10] | — |
| CH5-E06 | (Pande) | Hariharārkapitāmaha, Cāmuṇḍā, Yogeśvarī, Māheśvarī images on the maṇḍovara | Direct Udaypur evidence; sculptural/iconographic description | [same file; sec. "THE MAṇḎOVARA..."] | Individual plate/page numbers not re-confirmed per image this pass |
| CH5-E07 | (Adhikari 54) | Cāmuṇḍā's northern-quarter placement parallels Pānāhēḍā and Arthūṇā | Regional/comparative | [`Some Paramara Templess.md`; OCR p.54] | — |
| CH5-E08 | (Pande) | Śaiva Siddhānta theological argument, linked to Bhoja's *Tattvaprakāśa* | Potential/unverified connection — explicitly Pande's interpretive argument, not architectural fact | [`The Udayesvara Temple - Anupa Pande.md`; sec. "NOTES AND REFERENCES > ŚAIVA SIDDHĀNTA"] | Must not be presented as an established fact about the building's original intent; it is one scholar's reading |
| CH5-E09 | (Mittal) | Courtyard approx. 210 × 210 (units unspecified in legible text) | Direct Udaypur evidence; new measurement, not found elsewhere in this corpus | [`Art of Paramaras.md`; sec. "उदयपुर का उदयेश्वर मंदिर"; OCR p.60–61] | Units not confirmed; page boundary approximate |
| CH5-E10 | (Mittal) | Sabhā-maṇḍapa pillars: 2 ft 9 in square base, 10 ft 5 in total height | Direct Udaypur evidence; new measurement | [same file and section] | — |
| CH5-E11 | (Mittal) | Construction dated Samvat 1116/1137, matching Ch1's 1059/1080 CE dating | Direct Udaypur evidence; independent corroboration | [same file and section] | — |
| CH5-E12 | (Mittal) | Fourth independent source naming Muhammad bin Tughlaq for the later structure's construction | Direct Udaypur evidence; contradictory/qualifying (corrects the Aurangzeb legend, as in Ch1/Ch7/Ch10) | [same file and section] | — |
| CH5-E13 | (Mittal) | Six shrines standing, originally "eight or nine" (vs. Pande's consistent "eight") | Direct Udaypur evidence; minor variant figure | [same file and section] | — |
| CH5-E14 | (Mittal) | Liṅga brass face-plate dated "1754," attributed to the same donor (Khanderao Appaji) Ch1 dates to 1775 | Potential/unverified connection — likely OCR misread, not a genuine third date | [same file and section] | Flagged, not silently corrected; surrounding text visibly corrupted |
| CH5-E15 | (author uncertain) | Udaypur's temple used as the chronological/stylistic benchmark for Un, Oṅkār Māndhātā (1063 CE), Jāmlī, and Nemāwar temples | Regional/comparative; establishes Udaypur's architectural-historical significance regionally | [`Art of Paramaras.md`; sec. "मालवा के परमारकलीन प्रमुख मंदिर"; OCR p.57–60] | Author's name illegible in OCR; architectural-stylistic decline only, not political/economic |

No fixed excerpt count was applied. Five live retrieval queries plus direct
reading of `The Udayesvara Temple - Anupa Pande.md`'s Introduction and two
architectural sections, plus a targeted direct search of `Art of
Paramaras.md` conducted in a later revision of this document specifically
to close a previously-flagged gap (Part F), produced this set. The `PAN`
file-identity question (Part B) was also resolved in the course of this
chapter's original construction.

#### Ch5.5 Scholarly interpretations and disagreements

- The Śaiva Siddhānta theological reading (CH5-E08) is Pande's own argument,
  not corroborated or contested by any other source examined this pass —
  recorded as a single scholar's interpretation, not a consensus, exactly
  per the chapter's own instruction to separate description from
  interpretation.
- No direct contradiction was found between PAN, KRAM-1/2, HAR, DEV, and ADH
  on the architectural facts (plan, mouldings, style classification) — where
  they overlap, they are consistent, though this document did not
  exhaustively cross-check every measurement against every source this
  pass.
- **Mittal's "1754" date for the Śivaliṅga's brass face-plate (CH5-E14)
  appears to conflict with Patil's "1775"** (Ch1) for the same donation by
  the same named donor. Given the visible OCR corruption in the surrounding
  passage, this document treats the discrepancy as probably a misread
  rather than a genuine second date, but records both rather than silently
  preferring one.
- **Mittal's "eight or nine" original-shrine estimate (CH5-E13)** sits
  alongside, without contradicting, Pande's consistent figure of "eight" —
  a minor variant, not a dispute.

#### Ch5.6 Research gaps and missing evidence

- Individual plate/page citations for each named sculpture under CH5-E06
  were not re-confirmed one by one this pass — a gap, not a dropped fact;
  the images themselves are directly described in the source.
- The two active Samarāṅgaṇa-sūtradhāra files were not directly searched for
  the specific Bhūmija-style passage Pande attributes to that text — a
  direct read, cross-referencing Pande's citation, is still owed.
- KRAM-1/2, HAR, and DEV's comparative material was consulted via retrieval
  snippets, not read in full context, for this pass — a deeper read may
  surface additional comparative detail (e.g. precise stylistic
  classification debates) not captured here.
- Adam Hardy's own technical classification of the Bhūmija mode (seen only
  in snippet form, Ch3's gap note) remains unread in full — relevant here
  too, not just in Ch3.
- **The second `Art of Paramaras.md` article's author name (CH5-E15) could
  not be confidently identified from the available OCR** ("मुशील कुमार
  मुल्लेरे" is rendered exactly as extracted, flagged as unreliable, not
  corrected to a guessed real name). If a clean copy or the original print
  edition of this book is ever available, resolving this author's name
  and re-reading the full article without OCR corruption would likely
  surface further comparative material.
- Mittal's "210 × 210" courtyard figure (CH5-E09) has unconfirmed units —
  flagged rather than assumed to be feet.

#### Ch5.7 Drafting utility

- CH5-E02/E03/E05/E09/E10 together give the chapter a clean, source-
  grounded architectural backbone with specific measurements (plan →
  style → mouldings → dimensions) and should be presented in that order.
- CH5-E08 is an excellent worked example of the chapter's own
  description/interpretation distinction and should be flagged explicitly in
  the prose, not silently absorbed into the architectural description.
- CH5-E01 is a useful, low-weight cross-reference back to Ch4's contested
  dating — worth a single sentence pointing the reader there rather than
  re-arguing the question in this chapter.
- CH5-E12 (Mittal's fourth independent Tughlaq naming) should be folded
  into the cross-chapter Tughlaq/Aurangzeb discussion (Part D.1) rather
  than argued fresh here.
- CH5-E15's benchmark-status finding is a good, source-grounded way to
  open or close the chapter's discussion of the temple's regional
  significance, distinct from (and a useful complement to) Adhikari's
  "grandest specimen" framing already in CH5.3.
- Before publication: confirm individual plate numbers for CH5-E06's named
  sculptures; read Pande's Śilpaśāstra citation against the two active SAM
  files directly; resolve the 1754/1775 date discrepancy (CH5-E14) if a
  cleaner copy of either source becomes available.

### Ch6 — Inscriptions and Intellectual Life: Epigraphy, Languages and Literary Culture

#### Ch6.1 Chapter scope and research questions

Per `chapters.md`: "Examine Udaypur's inscriptions, scripts, languages and
epigraphic traditions, including the distinctive forms of its inscribed
lettering. Use these records to investigate political authority, religious
patronage, literary culture and intellectual life, while acknowledging the
limits of what the evidence can establish." The chapter's own annotation
("Original C10, connected thematically to C12") flags a cross-reference
forward to new Ch8 (Religion and the Material Life of Udaypur), not a split —
this chapter maps cleanly onto kb3's old-C8 bucket. Research questions: what
does the temple's own epigraphic record actually say and in what scripts;
what is the "serpentine scimitar" inscription and what do scholars disagree
about regarding its purpose; and what does the corpus establish about
literary/intellectual culture under the Paramāras more broadly, as
background for reading Udaypur's own inscriptions.

#### Ch6.2 Relevant sources

- **`A_serpentine_scimitar_of_letters_from_Ud.md`** (SIN-S, reliability
  0.90 per kb3 — "specialist epigraphic study"). Direct Udaypur evidence —
  a peer-reviewed study of a specific, newly-discovered Udaypur inscription,
  the single most rigorously-argued source in this chapter. Read in full
  this pass.
- **`Intach Udaypur (1).md`** (INT-ARC). Direct Udaypur evidence — an
  inventory of several further inscriptions found at or near the temple,
  independent of SIN-S.
- **`Jagta_Hua_Kasba_EN.md`** (TIW-E). Direct Udaypur evidence in
  popular-reportage register — carries a dedicated section, "The Paramaras'
  Inscriptions upon the Stones," with its own account of the oldest
  inscription's date and content; useful as a secondary, more accessible
  account, cross-checked against SIN-S and PAT-CH/GAN where they overlap
  (Ch1, Ch4) rather than treated as the primary basis for any claim here.
- **`History of Paramara Dynasty DC Ganguly.md`** (GAN). Direct evidence
  for Paramāra-era literary culture generally — its "LITERATURE AND
  LEARNING" chapter, read directly this pass.
- **`Vidisha Gazeteer.md`** (GAZ-VID). Direct evidence for the district's
  longer tradition of Sanskrit learning ("Oriental Schools" entry), seen via
  retrieval snippet this pass.
- **`Inscriptions Corpus.md`** (Trivedi) — already used extensively in Ch4;
  here it supplies general palaeographic/orthographic description method
  (how Trivedi dates inscriptions by letter-form) as comparative background,
  not re-quoted at length to avoid duplicating Ch4.
- **`भोजदेव (Bhojadeva)`** (BHJ-H) — kb3's old-C8 bucket drew several
  Devanagari excerpts from this source on Dhār inscriptions and Bhoja's
  literary circle; not independently re-read this pass, flagged as a gap.
- **`Samarāṅgaṇa-sūtradhāra`** (`SAM`) — kb3's old-C8 bucket is 31%
  SAM by volume, almost entirely generic architectural-geometry chapters
  with no connection to epigraphy or Udaypur specifically (e.g. temple-spire
  proportion verses). Excluded from this chapter's evidence as off-topic,
  consistent with the source-domination discipline applied in Ch2/Ch3.

#### Ch6.3 Facts, figures, and evidence

**The temple as a multi-script epigraphic archive.** Singh's own framing
for the chapter's whole subject: the Udayeśvara temple holds "a continuous
sequence of inscriptions in Sanskrit, Persian, and Hindi spanning eight
centuries—from the temple's consecration in samvat 1137 to its
archaeological restoration in samvat 1985," most "painstakingly copied and
systematically listed" in Gwalior State and ASI epigraphy reports, though
"[o]nly a selection... have been fully published" (Singh 1) [File:
`A_serpentine_scimitar_of_letters_from_Ud.md`; OCR p.1].

**The serpentine scimitar inscription.** Discovered by Singh during
fieldwork and previously unpublished, this Nāgarī inscription is engraved
on a 70cm pinkish sandstone slab now reset into the temple's outer parapet
wall — evidently moved from its original position, its inscribed face
turned inward contrary to the wall's otherwise-consistent construction
(Singh 1) [same file; OCR p.1]. The diagram itself depicts the Sanskrit
alphabet and grammatical endings arranged in the form of a serpent: a
"head" of 14 vowels (short/long pairs through compound vowels), a "body" of
semivowels, the five classes of stops, and sibilants arranged in a
rhomboidal "knot," a base of three aspirates, and a "tail" of 21 nominal and
18 verbal grammatical terminations (Singh 2) [same file; OCR p.2]. A short
accompanying verse names the diagram *varṇṇa-nāga-kṛpāṇikā* ("serpentine
scimitar of letters") and asks that it "protect" something left unspecified
in the damaged text (Singh 2) [same file and page].

**Dating and comparative parallels.** An identical diagram exists at the
Mahākāla temple, Ujjain, where an accompanying verse explicitly names it
"marked with Udayāditya's name" and attributes its composition to
Naravarman, Udayāditya's son and successor — dating the type to "not long
after king Udayāditya's death in 1093 and the succession of his son
Naravarman" (Singh 2) [same file; OCR p.2]. Singh notes three further,
similar inscriptions at Dhār and Un attributed to the same two kings,
collectively dating the Udaypur example to "the late-11th century" (Singh
1) [same file; OCR p.1].

**A genuine scholarly disagreement over purpose.** Singh explicitly argues
against the standard prior reading of this inscription type: "the serpentine
graph was not so much an educational tool devised to school young boys in
Sanskrit, as scholars have routinely remarked (Trivedi 1978... Pollock
2006)... Rather it was a complex device pressed into service of the
Paramāra kings who owed their allegiance to the cosmic overlord Śiva" (Singh
3) [File: `A_serpentine_scimitar_of_letters_from_Ud.md`; OCR p.3]. This is a
**named disagreement between Singh (2023) and two cited prior authorities
(Trivedi 1978, Pollock 2006)** over whether these diagrams were pedagogical
tools or dynastic-ritual devices — presented here as an open scholarly
question, not resolved by this document.

**Further inscriptions at the site.** Independent of SIN-S, INTACH's survey
records a six-line Devanagari inscription at "Setho ki Baniya Baoli near
Chatua Darwaza," whose "date and text... is not known" (INTACH, Architectural
Splendor 26) [File: `Intach Udaypur (1).md`; figure caption near "Figure
25"; OCR p.26], and a separate dedicatory tablet at a nearby site (Muratpur)
that the surveyors connect to Udaypur's own praśasti on stylistic and
proximity grounds, not a direct textual link: "[t]he proximity to Udaypur,
where the Udaypur Prasasti was first found, and the style of the building
and sculpture... allows us to reasonably conclude that the Udaypur prasasti
is from Muratpur" (INTACH, Architectural Splendor 100) [same file; OCR
p.100] — **explicitly a reasoned inference by the surveyors, not a
documented fact**, and presented as such.

**Literary culture under the Paramāras (context for reading these
inscriptions).** Ganguly's own account: Paramāra kings were "great votaries
of the Goddess of learning... [m]any of them were themselves great poets,"
with Vākpati/Muñja's own verses surviving only as quotations in later
authors' works (Dhanika's commentary on the *Daśarūpa*, Kṣemendra's
anthologies, Arjunavarman's *Rasikasaṃjīvanī*) (Ganguly 285–286) [File:
`History of Paramara Dynasty DC Ganguly.md`; sec. "LITERATURE AND LEARNING";
OCR p.285–286]. kb3's prior excerpt (not independently re-verified by page
this pass) adds that both Udayāditya and Naravarman were "staunch supporters
of all cultural movements," with Naravarman personally composing the Nagpur
praśasti — directly relevant, since that same praśasti is the primary
witness for the Udayāditya–Bhoja kinship question discussed in Ch4.

#### Ch6.4 Relevant excerpts and passage references

| ID | MLA citation | Excerpt / substance | Classification | Technical trace | Caveats |
|---|---|---|---|---|---|
| CH6-E01 | (Singh 1) | Eight-century, three-script (Sanskrit/Persian/Hindi) epigraphic archive at the temple | Direct Udaypur evidence | [`A_serpentine_scimitar_of_letters_from_Ud.md`; OCR p.1] | — |
| CH6-E02 | (Singh 1) | Physical description: 70cm pinkish sandstone slab, reset into the parapet wall, inscribed face turned inward | Direct Udaypur evidence | [same file; OCR p.1] | — |
| CH6-E03 | (Singh 2) | Full diagram structure: 14 vowels, semivowels, 5 stop-classes, sibilants, 3 aspirates, 21+18 grammatical terminations | Direct Udaypur evidence | [same file; OCR p.2] | — |
| CH6-E04 | (Singh 2) | Ujjain parallel names the diagram "marked with Udayāditya's name," attributed to Naravarman, dating it post-1093 | Regional/comparative, used to date the Udaypur example | [same file; OCR p.2] | — |
| CH6-E05 | (Singh 3) | Singh's explicit disagreement with Trivedi (1978) and Pollock (2006) over the diagram's educational-vs-ritual purpose | Contradictory/qualifying evidence — a named scholarly disagreement | [same file; OCR p.3] | Presented as open; this document adopts neither side |
| CH6-E06 | (INTACH, Architectural Splendor 26) | Six-line Devanagari inscription at Setho ki Baniya Baoli, undated | Direct Udaypur evidence | [`Intach Udaypur (1).md`; OCR p.26] | Source itself states the date and text are unknown |
| CH6-E07 | (INTACH, Architectural Splendor 100) | Surveyors' inference connecting a Muratpur tablet to the Udaypur praśasti, by proximity and style | Potential/unverified connection — explicitly an inference, not a documented link | [same file; OCR p.100] | Must not be presented as an established textual connection |
| CH6-E08 | (Ganguly 285–286) | Paramāra literary patronage; Vākpati/Muñja's poetry surviving only via later quotation | Direct evidence; general Paramāra-era context | [`History of Paramara Dynasty DC Ganguly.md`; sec. "LITERATURE AND LEARNING"; OCR p.285–286] | — |

No fixed excerpt count was applied. Four live retrieval queries plus a full
direct read of `A_serpentine_scimitar_of_letters_from_Ud.md` and a targeted
read of Ganguly's literary-culture chapter produced this set.

#### Ch6.5 Scholarly interpretations and disagreements

- **Educational tool vs. dynastic-ritual device** (CH6-E05): Singh (2023)
  explicitly rejects the reading he attributes to Trivedi (1978) and Pollock
  (2006), arguing instead for a royal-ideological function tied to
  Udayāditya and Naravarman's Śaiva allegiance. Both positions are named and
  cited in Singh's own paper; this document does not adjudicate between them.
- **The Muratpur-praśasti connection** (CH6-E07) is explicitly the
  surveyors' own inference, not a textually documented fact, and is recorded
  with that caveat rather than upgraded to a claim about Udaypur's epigraphic
  reach.

#### Ch6.6 Research gaps and missing evidence

- The two short inscriptions accompanying the serpentine diagram itself
  (Singh's Fig. 4 and Fig. 5) remain only partly legible even in Singh's own
  reading ("the lacunae due to damage make it difficult to decipher") — this
  is a limit in the source material itself, not a gap in this document's
  research.
- TIW-E's "Paramaras' Inscriptions upon the Stones" section (including its
  "What is in the oldest inscription?" subsection, citing "the young
  historian Santosh Kumar Verma") was seen only via retrieval snippet, not
  read in full — a direct read may add further Udaypur-specific
  inscriptions not covered by SIN-S or INT-ARC.
- BHJ-H's Devanagari material on Dhār inscriptions (kb3's old-C8 bucket)
  was not independently re-read this pass.
- Trivedi's and Pollock's own original arguments (the positions Singh
  argues against, CH6-E05) are known only through Singh's characterization
  of them in his own paper — this document has not read Trivedi 1978 or
  Pollock 2006 directly to verify Singh's characterization is fair, though
  `Inscriptions Corpus.md` (used in Ch4) is a later (1991) edition by the
  same Trivedi and did not, in the sections read there, make the specific
  "educational tool" argument Singh attributes to his 1978 work.

#### Ch6.7 Drafting utility

- CH6-E01–E05 form a strong, self-contained set-piece built almost entirely
  from one rigorously-argued specialist source (Singh) and should anchor
  the chapter.
- CH6-E05's named disagreement is excellent material for the chapter's own
  stated aim ("acknowledging the limits of what the evidence can
  establish") and should be presented as an open question, not resolved
  one way for narrative convenience.
- Cross-reference: CH6-E04's Naravarman/Nagpur-praśasti connection links
  directly to Ch4's Udayāditya–Bhoja kinship discussion — worth a short
  cross-reference note rather than re-explaining the kinship question here.
- Before publication: read TIW-E's inscriptions section and Trivedi
  1978/Pollock 2006 directly if possible, rather than relying on Singh's
  characterization of the educational-tool argument.

### Ch7 — The Wider Built Heritage of Udaypur: Fortifications, Shrines, Mosques and Water Structures

#### Ch7.1 Chapter scope and research questions

Per `chapters.md`: "Document the town's surviving structures beyond the
Udayeśvara temple, including fortifications, shrines, mosques, stepwells and
other elements of its built heritage. Consider their dates, functions,
architectural characteristics and relationship to the town's changing
historical circumstances." This maps cleanly onto kb3's old-C9 bucket (no
split needed). This chapter deliberately does not re-describe the
Udayeśvara temple itself (Ch5) or repeat Patil's monument list in full
(already given in Ch1) — it goes deeper on the fortification wall, the
individual gates and mosques, and the water structures, and adds a third
independent source for the Tughlaq/Aurangzeb question first raised in Ch1.

#### Ch7.2 Relevant sources

- **`Geo-Heritage of Udaypur The Third Eye.md`** (INT-GEO). Direct Udaypur
  evidence — by far the most detailed source on the fortification wall
  itself (dedicated technical sections on bastions, watchtowers, gates, and
  stepwells). Read directly, several sections.
- **`Intach Udaypur (1).md`** (INT-ARC). Direct Udaypur evidence — its
  structured heritage-structure tables (with unique IDs, GPS coordinates,
  period, protection status, and condition grading) independently document
  individual gates and water structures.
- **`The Udayesvara Temple - Anupa Pande.md`** (PAN) — already the primary
  source for Ch5, but its "REPORTS ON THE UDAYEŚVARA TEMPLE" section quotes
  J. D. Beglar's 1871–72 tour report at length, a named 19th-century
  primary witness describing the mosque built behind the temple — directly
  relevant to this chapter's "mosques" subject and a third independent
  corroboration of the Tughlaq (not Aurangzeb) attribution from Ch1.
- **`The cultural heritage of madhya bharat.md`** (PAT-CH) and **`Vidisha
  Gazeteer.md`** (GAZ-VID) — both already used in Ch1; here GAZ-VID
  supplies an independently-worded account of the Pisanari-kā-mandir legend
  that corroborates Patil's version.
- **`Jagta_Hua_Kasba_EN.md`** (TIW-E) — direct Udaypur evidence in
  reportage register, describing a conservation-focused site visit; used
  here only for descriptive colour, not as the primary basis for any dated
  claim.
- **`Samarāṅgaṇa-sūtradhāra`** (`SAM`) — kb3's old-C9 bucket is 23% SAM by
  volume, almost entirely generic fort/pavilion/elephant-stable
  construction rules with no stated connection to Udaypur. Excluded as
  off-topic, consistent with the discipline applied in Ch2/Ch3/Ch6.
- **`RAJM`, `SIN-S`** — kb3 itself flags both as barely represented in this
  bucket; not examined further here (SIN-S's actual relevant content is
  about the temple's inscriptions, already fully used in Ch6).

#### Ch7.3 Facts, figures, and evidence

**The fortification wall.** The hill fort's wall averages 4 metres thick on
its eastern, western, and northern sides (INTACH, Geo-Heritage 87) [File:
`Geo-Heritage of Udaypur The Third Eye.md`; sec. "Technical Specifications";
OCR p.87], runs approximately 1,400 metres in total length (INTACH,
Geo-Heritage 49) [same file; sec. "3. Fortification wall"; OCR p.49], and
has two watchtowers positioned on opposite sides (INTACH, Geo-Heritage 92)
[same file; OCR p.92]. The main entrance gate is given as 5,600 mm wide
(INTACH, Geo-Heritage 98) [same file; sec. "10.11 Burj (Bastion)"; OCR p.98].
INT-GEO's own framing is candid about the evidentiary gap here: "historical
records are silent" about the wall's origin and builder, even though it is
"an architectural marvel... standing undisturbed over a span of 1400
meters, maybe the longest one anywhere in Madhya Pradesh" (INTACH,
Geo-Heritage 19) [same file; OCR p.19] — **a direct, source-stated
acknowledgment of a research gap, not a documented fact about who built the
wall or when.**

**Named gates.** The Chanderi Darwaza, a trabeated stone gateway near the
Bijasen Mandir, is dated by INTACH's survey to the 11th century CE (INTACH,
Architectural Splendor 48) [File: `Intach Udaypur (1).md`; OCR p.48]. The
Moti Masjid Darwaza, architecturally similar, is approximately 15 feet tall
and 8 feet wide, with a corbelled point arch and terracotta animal figures
on its northern colonnade (INTACH, Architectural Splendor 48) [same file and
page].

**Stepwells and water structures.** INTACH's structured heritage table
records "Santbhu ji Ki Baoli" (ID: UD/WS/SW/01), dated 11th century,
unprotected, currently in use, condition graded "Very Good" (Grade I)
(INTACH, Architectural Splendor 101) [File: `Intach Udaypur (1).md`; sec.
heritage-structure table; OCR p.101]. A separate stepwell inside the Badi
Mata Mandir complex carries a foundation legend: "a milkman Keshav and
Goddess Mahamaya paid him a visit in the form of a beautiful lady and
suggested to him the idea of stepwell," after which "people of the village
built this structure" (INTACH, Architectural Splendor 93) [same file; OCR
p.93] — **explicitly recorded as folklore in the source, not a documented
construction history.** INT-GEO separately records a three-sided stepwell
on the slopes of "Pindi Hill," interpreted as a water reservoir for hill-area
users (INTACH, Geo-Heritage 111) [File: `Geo-Heritage of Udaypur The Third
Eye.md`; sec. "13.1 Baoli on the Slopes"; OCR p.111].

**The Pisanari-kā-mandir legend — independently corroborated.** Ch1
(CH1-E...) already gave Patil's account that this temple "is popularly
believed to have been built by a woman out of her earning made by grinding
flour for the workmen employed for the construction of the Udayeshvara
temple," a tradition Patil says is "belied by the style of the architecture."
The Vidisha Gazetteer gives an independently-worded version of the same
legend — "a remnant of an old temple traditionally said to have been built
by a woman, out of her ea[rnings]" (Shrivastav and Verma) [File: `Vidisha
Gazeteer.md`; sec. "Kurwai (24°0′ N; 78°5′ E)"; exact OCR page not
individually re-confirmed this pass] — **a second source independently
recording the same folk tradition**, which strengthens confidence that the
legend itself is widely attested, without making the legend itself any more
historically true (both sources treat it as tradition, not fact).

**A third, named primary witness on the mosque — J. D. Beglar (1871–72).**
Pande's monograph quotes Beglar's tour report directly and at length: "The
temple is built of red sandstone and stands in the centre of a large paved
and raised platform... surrounding the great temple stood at one time seven
minor temples... All of them have now disappeared or been converted into...
a Muhammadan masjid consisting of a hall with flat roof, supported by four
rows of Hindu Pillars... masons' marks and short lines occur on many of the
pillars in this masjid, and conclusively prove... that they are Hindu"
(qtd. in Pande 88–89) [File: `The Udayesvara Temple - Anupa Pande.md`; sec.
"REPORTS ON THE UDAYEŚVARA TEMPLE"; OCR p.88–89]. Pande's own text,
immediately before this quotation, independently states that "Muhammad
Tughluq between AD 1336-38 damaged the attendant temples and erected a
mosque at the back of the temple, using the material from the demolished
[shrines]... Persian inscriptions in the mosque record its construction by
him" (Pande 88) [same file and page] — **a third source (after Patil in
Ch1 and, implicitly, the Persian inscriptions themselves) independently
naming Tughlaq, not Aurangzeb, strengthening that correction further.**

#### Ch7.4 Relevant excerpts and passage references

| ID | MLA citation | Excerpt / substance | Classification | Technical trace | Caveats |
|---|---|---|---|---|---|
| CH7-E01 | (INTACH, Geo-Heritage 87) | Fortification wall averages 4m thick on three sides | Direct Udaypur evidence | [`Geo-Heritage of Udaypur The Third Eye.md`; sec. "Technical Specifications"; OCR p.87] | — |
| CH7-E02 | (INTACH, Geo-Heritage 19) | Wall's origin/builder unknown — "historical records are silent"; ~1400m, possibly the longest in MP | Direct Udaypur evidence; explicit source-stated research gap | [same file; OCR p.19] | Source itself flags this as unresolved |
| CH7-E03 | (INTACH, Architectural Splendor 48) | Chanderi Darwaza, dated 11th c. CE; Moti Masjid Darwaza, ~15ft × 8ft | Direct Udaypur evidence | [`Intach Udaypur (1).md`; OCR p.48] | — |
| CH7-E04 | (INTACH, Architectural Splendor 101) | Santbhu ji Ki Baoli, 11th c., Grade I condition, in use | Direct Udaypur evidence | [same file; sec. heritage-structure table; OCR p.101] | — |
| CH7-E05 | (INTACH, Architectural Splendor 93) | Badi Mata Mandir stepwell foundation legend (Keshav and Goddess Mahamaya) | Potential/unverified connection — explicitly folklore per the source | [same file; OCR p.93] | Source itself frames this as folklore |
| CH7-E06 | (Shrivastav and Verma) | Independent version of the Pisanari-kā-mandir "grinding flour" legend | Direct Udaypur evidence; corroborates Ch1's Patil citation | [`Vidisha Gazeteer.md`; sec. "Kurwai (24°0′ N; 78°5′ E)"] | OCR page not individually re-confirmed this pass |
| CH7-E07 | (qtd. in Pande 88–89) | Beglar's 1871–72 tour-report description of the mosque, with mason's-mark evidence of reused Hindu pillars | Direct Udaypur evidence; a named 19th-century primary witness, quoted in a secondary monograph | [`The Udayesvara Temple - Anupa Pande.md`; sec. "REPORTS ON THE UDAYEŚVARA TEMPLE"; OCR p.88–89] | Quotation is nested (Beglar via Pande); the original 1871–72 report itself was not independently located |
| CH7-E08 | (Pande 88) | Third independent naming of Muhammad Tughlaq (not Aurangzeb) for the mosque's construction | Direct Udaypur evidence; contradictory/qualifying (corrects the popular legend, as in Ch1) | [same file and page] | — |

No fixed excerpt count was applied. Five live retrieval queries plus direct
reading of INT-GEO's technical sections and Pande's "Reports" section
produced this set.

#### Ch7.5 Scholarly interpretations and disagreements

- No direct contradiction was found this pass; where sources overlap (the
  Pisanari legend, the Tughlaq attribution), they corroborate rather than
  conflict, strengthening confidence in the underlying fact (Tughlaq) while
  leaving the folklore (Pisanari, the stepwell origin story) explicitly
  labeled as such in every source that carries it.
- The fortification wall's builder and date remain genuinely unknown — this
  document records that absence rather than guessing at a builder by
  analogy to the temple's own Paramāra-era dating, which no source
  supports.

#### Ch7.6 Research gaps and missing evidence

- The fortification wall's construction date and builder are not
  established by any source examined — flagged as a real, source-
  acknowledged gap, not filled by inference.
- Beglar's original 1871–72 tour report was not independently located or
  read outside of Pande's quotation of it — a direct read, if the report
  can be found, would allow checking Pande's quotation for completeness.
- TIW-E's account of a conservation site-visit (kb3's old-C9 excerpt,
  "Upadhyay-ji roamed for seven or eight hours...") was not read in full
  this pass — it may contain further descriptive detail on specific
  structures not covered by INT-GEO/INT-ARC.
- The Bara-khambi and Shahi Masjid/Mahal entries from Patil's monument list
  (Ch1) were not independently supplemented with additional sources this
  pass — live retrieval did not surface material beyond what Ch1 already
  captured for these two structures specifically.

#### Ch7.7 Drafting utility

- CH7-E01–E04 give the chapter a clean, measurable, source-grounded
  inventory of the built heritage beyond the temple.
- CH7-E07/E08 (the Beglar quotation via Pande) is an excellent primary-
  witness anchor and should be used prominently — it is rare in this
  corpus to have a named 19th-century eyewitness account quoted at length.
- CH7-E05/E06 (the two stepwell/temple foundation legends) are good
  material for a brief methodological aside on oral tradition, paired with
  Ch1's similar treatment of the Bhrangarajpur/Gond founding legends.
- Before publication: attempt to locate Beglar's original report; read
  TIW-E's conservation-visit passage in full.

### Ch8 — Religion and the Material Life of Udaypur: Ritual, Agriculture, Trade and Craft

#### Ch8.1 Chapter scope and research questions

Per `chapters.md`: "Explore Śaiva traditions, ritual practices and
religious institutions alongside agriculture, wells, markets, crafts, trade
and patronage. Investigate the relationship between religious life and the
local economy through available historical, epigraphic, archaeological and
ethnographic evidence." Per the chapter's own annotation ("Merge C12 +
C13"), this absorbs kb3's old-C10 (Ritual and Knowledge) and old-C11
(Fields, Wells and Markets) buckets — a clean merge, no split needed. Both
old buckets are heavily dominated by volume (28% and 39% respectively) by
`SAM` material that, on inspection, is almost entirely generic Śaiva
theology or generic Vāstu-śāstra prescription with no stated Udaypur
connection — already the subject of Ch5's "interpretation vs. description"
discussion (Pande's Śaiva Siddhānta reading) and excluded here as off-topic
by the same discipline applied throughout this rebuild. This chapter's own
brief is specifically about Udaypur's *local* religious and economic life,
not Śaiva theology or district agriculture in the abstract — research
questions: what does the corpus establish about Udaypur's own markets,
crafts, and religious institutions specifically, as opposed to the wider
district or generic śāstra prescription; and what regional economic context
(Vidisha district, Malwa trade routes) legitimately frames that local
picture without being mistaken for direct Udaypur evidence.

#### Ch8.2 Relevant sources

- **`Intach Udaypur (1).md`** (INT-ARC). Direct Udaypur evidence — its
  structured heritage tables record individual local temples and the
  Purana Bazaar Darwaza, a gate giving access to the old market area;
  its demography section separately records current livelihoods.
- **`Vidisha Gazeteer.md`** (GAZ-VID). Regional/comparative evidence — rich
  district-wide statistics on crops, irrigation, and trade (Sironj's
  Mughal-era textile trade, quoting the 17th-century traveller Tavernier),
  none of it Udaypur-specific but useful as the economic backdrop the
  chapter's brief calls for.
- **`Temple Economics.md`** (SIN-T). **General-context source only, per the
  confirmed research-use policy established in Phase B1 and Part B.** Its
  material on *melā* economics, pilgrimage, and temple-priest livelihoods is
  conceptually relevant to this chapter's themes but concerns temples and
  fairs elsewhere in India, not Udaypur — used here, if at all, only as
  background framing, never as a claim about Udaypur itself. No passage
  naming Udaypur was found in this source in this or the earlier Phase B1
  full-text search.
- **`भोजदेव (Bhojadeva)`** (BHJ-H) and **`Pātañjala-Yogasūtram with the
  Rājamārtaṇḍa-vṛtti`** (RAJM, unindexed) — kb3's old-C10/C11 buckets drew
  several Devanagari excerpts from both on Vāstu-śāstra house-orientation
  rules and generic philosophical commentary; not independently re-read
  this pass, and not evidently about Udaypur specifically where visible —
  flagged as a gap rather than re-asserted.
- **`History of the Parmar Rajput Dynasty.md`** (PAR) — kb3 flags this as
  barely represented in both old buckets; not examined further here.

#### Ch8.3 Facts, figures, and evidence

**Udaypur's own market access.** INTACH's survey dates the Purana Bazaar
Darwaza, a gateway on higher ground inside the village accessing the old
bazaar area southeast of the Nīlakaṇṭheśvara temple, to approximately the
11th century CE (INTACH, Architectural Splendor 52) [File: `Intach Udaypur
(1).md`; near "Figure 74"; OCR p.52 — this specific descriptive passage was
not independently re-located by direct file search this pass and is carried
from kb3's prior citation; flagged, not silently asserted as independently
re-verified]. A further temple recorded in INTACH's heritage-structure
table, "New Danga Mandir" (ID UD/KEL/HT/07), is dated 11th century,
unprotected, currently in use, and graded "Poor" (Grade III) (INTACH,
Architectural Splendor 101) [same file; sec. heritage-structure table; OCR
p.101].

**Present-day livelihoods.** "The major population of Udaypur is engaged in
agriculture... a section of the village population is engaged in the stone
mining occupation as well," with residents also relocating to nearby cities
(Vidisha, Bhopal, Indore) for better livelihood opportunities (INTACH,
Architectural Splendor 37) [same file; OCR p.37] — directly relevant,
contemporary ethnographic evidence, not historical.

**Regional trade context (explicitly not Udaypur-specific).** The Vidisha
Gazetteer frames Malwa generally as "a centre of culture and civilization
for centuries," its roads serving as both military and trade routes
(Shrivastav and Verma 154) [File: `Vidisha Gazeteer.md`; sec. "Trade and
Commerce"; OCR p.154]. Sironj, elsewhere in the same district, was a major
Mughal-era trading centre — Abul Faẕl called it a "bandar" (a prominent
business city) in 1593, and the 17th-century French traveller Tavernier
described it as "crowded with merchants and artisans and famous for its
muslins and chintzes," quoting a merchant's description of the muslin as so
fine "you see all the skin as though it were uncovered" (Shrivastav and
Verma 154–155) [same file; OCR p.154–155]. **This is regional/comparative
evidence about Sironj, a different town in the same district — not a claim
about Udaypur's own market activity**, and is presented here only as
economic backdrop, per this chapter's own instruction to investigate "the
relationship between religious life and the local economy" without
conflating district-level and town-level evidence.

**Temple Economics and the absence of a direct Udaypur connection.**
Consistent with the research-use policy established in Part B and applied
throughout this document, `Temple Economics.md`'s substantial material on
*melā* (fair) economics and temple-priest livelihoods is retained here only
as conceptual background on how religious institutions interact with local
economies generally — no passage in this source names Udaypur, and none is
presented as evidence about it.

#### Ch8.4 Relevant excerpts and passage references

| ID | MLA citation | Excerpt / substance | Classification | Technical trace | Caveats |
|---|---|---|---|---|---|
| CH8-E01 | (INTACH, Architectural Splendor 52) | Purana Bazaar Darwaza, c. 11th century, accesses the old bazaar area | Direct Udaypur evidence | [`Intach Udaypur (1).md`; OCR p.52] | Not independently re-located by direct file search this pass; carried from kb3's prior citation |
| CH8-E02 | (INTACH, Architectural Splendor 101) | New Danga Mandir, 11th c., Grade III condition, in use | Direct Udaypur evidence | [same file; sec. heritage-structure table; OCR p.101] | — |
| CH8-E03 | (INTACH, Architectural Splendor 37) | Current livelihoods: agriculture, stone mining, out-migration for work | Direct Udaypur evidence; contemporary, not historical | [same file; OCR p.37] | — |
| CH8-E04 | (Shrivastav and Verma 154) | Malwa as a historic trade/military route corridor | Regional/comparative | [`Vidisha Gazeteer.md`; sec. "Trade and Commerce"; OCR p.154] | Not Udaypur-specific |
| CH8-E05 | (Shrivastav and Verma 154–155) | Sironj's Mughal-era muslin/chintz trade; Abul Faẕl's and Tavernier's descriptions | Regional/comparative; quotes two named historical travellers | [same file; OCR p.154–155] | About Sironj, a different town in the district, not Udaypur |

No fixed excerpt count was applied. Five live retrieval queries were run;
the chapter's genuinely Udaypur-specific material proved considerably
thinner than the volume of kb3's old-C10/C11 buckets suggested, because most
of that volume is generic Śaiva theology or Vāstu-śāstra prescription with
no demonstrated local connection — this is reported as a finding about the
corpus's actual coverage, not papered over with regional or generic
material relabelled as local.

#### Ch8.5 Scholarly interpretations and disagreements

None identified this pass specific to this chapter's actual (thin)
Udaypur-specific evidence base. No source examined contradicts another on
the facts recorded above.

#### Ch8.6 Research gaps and missing evidence

- **This is the thinnest chapter in this rebuild so far for direct Udaypur
  evidence.** Beyond CH8-E01–E03, this document did not find a single
  source making a specific, verifiable claim about Udaypur's own markets,
  crafts, patronage relationships, or ritual institutions beyond the
  temple itself (already covered in Ch5/Ch6). This should be stated as a
  finding — the available corpus is comparatively silent on this chapter's
  specific subject — not papered over by substituting regional or generic
  material.
- CH8-E01's exact location was not independently re-confirmed by direct
  file search this pass, unlike most other citations in this document —
  flagged explicitly rather than silently treated as equally solid.
- BHJ-H's and RAJM's Vāstu-śāstra material (house orientation, craft
  guild rules) was not read directly to check for any Udaypur-specific
  content that a keyword-based pass might have missed.
- No source examined establishes any ritual practice, festival, or
  religious institution specific to historical Udaypur beyond temple
  worship itself — this is a gap in the evidence available, not a claim
  that no such practices existed.

#### Ch8.7 Drafting utility

- Given how thin this chapter's direct evidence is, the drafting
  recommendation is to lean on Ch1/Ch5/Ch6/Ch7's already-established
  Udaypur-specific material (the temple's ritual function, its
  inscriptions, its surrounding structures) rather than inventing new
  local-economy claims this corpus does not support.
- CH8-E04/E05 (Sironj) can frame the chapter's regional economic
  backdrop, explicitly marked as regional, not local.
- Cross-reference Ch9 (Society and Cultural Life) and Ch12 (Udaypur Today)
  for the fuller ethnographic/present-day material INT-ARC and TIW-E/TIW-H
  carry — some of it may be more at home there than here.
- Before publication: a dedicated search for any Udaypur-specific craft,
  guild, or market record beyond the Purana Bazaar Darwaza would be the
  single most valuable next step for this chapter specifically.

### Ch9 — Society and Cultural Life: Communities, Languages, Festivals and Oral Traditions

#### Ch9.1 Chapter scope and research questions

Per `chapters.md`: "Examine community identities, spoken languages,
everyday customs, festivals, folklore and oral histories. Bring historical
evidence into conversation with residents' memories and contemporary
practices, distinguishing documented events from traditions whose
historical origins remain uncertain." Per the chapter's own annotation
("Merge C14 + C15"), this absorbs kb3's old-C12 (People of the Plateau) and
old-C13 (Stories of Udaypur) buckets — a clean merge. Unlike Ch8, this
chapter's genuine Udaypur-specific material is rich, not thin — old-C13 in
particular is led by TIW-E/TIW-H (first-person reportage) and carries a
named, dated founding legend from Ganguly not yet used anywhere else in
this document. Research questions: what oral traditions exist about
Udaypur's founding, and how do they relate to each other and to the
documented history (Ch1, Ch4); what present-day festivals and communal
practices does the corpus document; and what does the corpus establish
about language and community identity at the district level as context for
the town itself.

#### Ch9.2 Relevant sources

- **`History of Paramara Dynasty DC Ganguly.md`** (GAN). Direct Udaypur
  evidence — carries a full, named legendary founding story for Udaypur
  (the snake-and-treasure tale) that Ganguly himself explicitly labels
  "no doubt an absolute myth," immediately followed by his own
  corroboration that a contemporary inscription nonetheless proves
  Udayāditya actually built the city. Read directly this pass.
- **`Jagta_Hua_Kasba_EN.md`** (TIW-E) and **`कथा उदयपुर... Hindi
  original`** (TIW-H). Direct Udaypur evidence, first-person reportage
  register — the single richest source in the corpus for present-day
  festivals, informal oral history, and named local tradition-bearers.
  TIW-H is confirmed unindexed (Part B); TIW-E, the English translation, is
  active and used here as the citable form, consistent with this
  document's practice elsewhere.
- **`Intach Udaypur (1).md`** (INT-ARC). Direct Udaypur evidence —
  independently corroborates TIW-E's festival claims with dated,
  survey-recorded detail.
- **`Vidisha Gazeteer.md`** (GAZ-VID). Regional/comparative evidence for
  language and dialect shift across the district, not Udaypur-specific but
  directly relevant context for the chapter's "spoken languages" theme.
- **`Raja_Bhoj_Aur_Parmarkaleen_EN.md`** (RAJ-E). Regional/comparative —
  rich material on Bhoja-era folk legend formation and named historical
  festivals, useful for framing how royal legends of this kind typically
  developed, though not about Udaypur specifically.
- **`History of the Parmar Rajput Dynasty.md`** (PAR) — kb3 flags this as
  barely represented in both old buckets; not independently re-examined
  here beyond what Ch4 already used.
- **`Samarāṅgaṇa-sūtradhāra`** (`SAM`) — 42% and 17% of kb3's old-C12/C13
  buckets respectively, almost entirely generic Jambudvīpa cosmology or
  architectural-ritual prescription with no Udaypur connection. Excluded as
  off-topic, consistent with the discipline applied throughout this
  rebuild.

#### Ch9.3 Facts, figures, and evidence

**A third founding legend, explicitly labeled myth by its own source.**
Ganguly records, at length, a legend distinct from the two already given in
Ch1 (Bhrangarajpur/native chief; Gond conquest): a snake, rescued by
Udayāditya, betrays him by hiding in his stomach; a second, treasure-
guarding snake is overheard by the queen revealing both snakes'
vulnerabilities; the king is cured and the treasure recovered; "[t]o
commemorate this event, he built there a city and a temple and named them
after himself" (Ganguly 266–267) [File: `History of Paramara Dynasty DC
Ganguly.md`; sec. "THE NĪLAKANṬHEŚVARA TEMPLE AT UDAYAPUR" (preceding
section); OCR p.266–267]. Ganguly's own verdict, stated immediately after
recounting the story in full: "[t]he above story is no doubt an absolute
myth, and there is evidence, in the words of a contemporary inscription,
that the city was built by Udayāditya" (Ganguly 267) [same file and page].
**This document now has three independently-sourced, mutually
unreconciled founding legends for Udaypur** (Bhrangarajpur/native chief and
Gond-conquest from INT-GEO, Ch1; the snake-and-treasure tale from Ganguly,
here) — none corroborating the others, all explicitly labeled legend by
their own sources, alongside the one thing that is independently,
non-legendarily attested: that Udayāditya really did found the town
(Ch1, Ch4).

**A lost structure, explicitly acknowledged.** Ganguly separately notes
that "Udayasamudra, the construction of which is also attributed by an
early record to Udayāditya cannot now be traced" (Ganguly 267) [same file
and page] — a direct, source-stated acknowledgment that the tank itself
(one of the three namesake foundations from the inscription discussed in
Ch1) is physically lost, not merely under-researched.

**Present-day festivals — independently corroborated by two sources.**
Tiwari reports that "[e]very year on this day [Mahāśivarātri] a big fair is
held in Udaipur, in which thousands of people come for the Shiva temple,
from even the surrounding districts" (Tiwari) [File: `Jagta_Hua_Kasba_EN.md`;
exact OCR page not available — this file's page metadata does not resolve
to a simple integer, a known limitation noted in Part A]. INTACH's survey
independently corroborates this with dated specificity: "[a] 7-day
Shivaratri fair in February-March is organized in Udaypur. At the
Neelkantheshwar Temple, an annual fair is held in the nearby 'Ganpuri
Bagh'... the Shivaratri Mahadev Festivals at Udaypur being very popular"
(INTACH, Architectural Splendor 37) [File: `Intach Udaypur (1).md`; OCR
p.37] — **two independent sources corroborating the same living festival
tradition**, one in reportage register, one in survey register.

**Named local tradition-bearers — evidence of an active oral-history
culture, not a vanished one.** Tiwari names several specific contemporary
individuals engaged with Udaypur's history and folklore: "Santosh Kumar
Verma," described as "an assistant professor of history at the Girls'
College of Ganj Basoda"; the historians "Dr. Narayan Vyas" and "Dr. Sudhish
Mishra"; "Deepak Sharma of Pragya Pravah"; and the social worker "Praveen
Sharma," who is reported "going into some ruin, some old house, some scrub"
documenting the town (Tiwari) [same file]. A separate passage records local
oral tradition about an unnamed "Garhi" (fortified residence): "[w]ho had
this Garhi built? Of what date is it? Any inscription, any story? The
answers... are hardly to be found anywhere in all the documents written on
this region; but in folk [memory], everywhere, there are many stories"
(Tiwari) [same file] — **the source itself explicitly frames this as
oral memory filling a documentary gap, not as a documented fact.**

**Language and dialect (regional context).** District-wide, *Bundeli* was
the dominant recorded dialect in 1908, shifting to *Malwi* across the
1921–1941 censuses, before standard Hindi became the predominant returned
language (Shrivastav and Verma) [File: `Vidisha Gazeteer.md`; exact page
not re-confirmed this pass — carried from kb3's prior citation]. This is
district-level evidence, not a specific claim about Udaypur's own spoken
language historically.

#### Ch9.4 Relevant excerpts and passage references

| ID | MLA citation | Excerpt / substance | Classification | Technical trace | Caveats |
|---|---|---|---|---|---|
| CH9-E01 | (Ganguly 266–267) | The snake-and-treasure founding legend, told in full | Potential/unverified connection — explicitly myth per the source | [`History of Paramara Dynasty DC Ganguly.md`; OCR p.266–267] | Not reconciled with the two Ch1 legends; all three are independent and mutually inconsistent |
| CH9-E02 | (Ganguly 267) | Ganguly's own verdict: "no doubt an absolute myth," but the city's real founding by Udayāditya is independently inscription-attested | Direct Udaypur evidence; the scholar's own description/legend distinction | [same file and page] | — |
| CH9-E03 | (Ganguly 267) | Udayasāmudra (the tank) "cannot now be traced" | Direct Udaypur evidence; acknowledged research/physical gap | [same file and page] | — |
| CH9-E04 | (Tiwari) | Annual Mahāśivarātri fair draws "thousands of people... from even the surrounding districts" | Direct Udaypur evidence | [`Jagta_Hua_Kasba_EN.md`; page metadata unresolved for this file] | — |
| CH9-E05 | (INTACH, Architectural Splendor 37) | 7-day Shivaratri fair, Feb–March; separate Ganpuri Bagh fair at the temple | Direct Udaypur evidence; corroborates CH9-E04 | [`Intach Udaypur (1).md`; OCR p.37] | — |
| CH9-E06 | (Tiwari) | Named contemporary tradition-bearers (Verma, Vyas, Mishra, Sharma) actively documenting Udaypur | Direct Udaypur evidence; ethnographic | [same file] | — |
| CH9-E07 | (Tiwari) | Oral memory about an unnamed "Garhi," explicitly filling a documentary gap per the source | Potential/unverified connection — source explicitly frames as folk memory, not record | [same file] | — |
| CH9-E08 | (Shrivastav and Verma) | District dialect shift: Bundeli (1908) → Malwi (1921–41) → Hindi | Regional/comparative | [`Vidisha Gazeteer.md`] | Page not re-confirmed this pass; district-level, not Udaypur-specific |

No fixed excerpt count was applied. This chapter's evidence came primarily
from a full direct read of Ganguly's relevant pages and the retained kb3
excerpts for TIW-E/INT-ARC, cross-checked against each other where they
overlap (CH9-E04/E05).

#### Ch9.5 Scholarly interpretations and disagreements

- **Three unreconciled founding legends** (Bhrangarajpur/native chief and
  Gond-conquest, Ch1; snake-and-treasure, CH9-E01 here) exist side by side
  in this corpus with no source attempting to reconcile them, and this
  document does not attempt to either. Each is explicitly framed as
  legend/oral-tradition by the very source that records it — the
  consistent pattern across all three is that legend and documented history
  (the foundation inscription) are kept distinct even within each
  individual source.
- No contradiction was found regarding the present-day festival evidence
  (CH9-E04/E05) — the two sources corroborate rather than conflict.

#### Ch9.6 Research gaps and missing evidence

- Udayasāmudra's physical location is explicitly stated as untraceable by
  Ganguly (CH9-E03) — this document does not attempt to locate it, since no
  source examined offers a candidate site.
- TIW-E's page metadata does not resolve to simple OCR page integers in
  this file's chunking — a structural limitation of this particular source
  noted here rather than papered over with an invented page number.
- GAZ-VID's dialect-shift citation (CH9-E08) was not independently
  re-confirmed by direct file search this pass.
- No source examined this pass addresses community/caste identity within
  Udaypur specifically (as opposed to the district generally) — kb3's old-
  C12 bucket's caste material (Kayastha, Rajput lineages, etc.) is entirely
  about Malwa/Madhya Bharat broadly, not Udaypur, and was excluded here as
  not meeting this chapter's own "Udaypur" focus; a dedicated search for
  Udaypur-specific community composition remains a gap.

#### Ch9.7 Drafting utility

- CH9-E01/E02 (the snake-and-treasure legend) is an excellent, fully
  quotable set-piece and pairs naturally with Ch1's two other founding
  legends — consider presenting all three together, in one place, as a
  deliberate illustration of "historical memory vs. documented history,"
  rather than splitting them across chapters.
- CH9-E04/E05/E06 (living festival tradition, named tradition-bearers)
  directly support the chapter's instruction to "bring historical evidence
  into conversation with residents' memories and contemporary practices"
  and should be given prominent treatment.
- Cross-reference: Ch12 (Udaypur Today) will likely need some of this same
  TIW-E material from a different angle (contemporary community life
  rather than oral tradition) — coordinate rather than duplicate when that
  chapter is built.
- Before publication: resolve TIW-E's page-citation limitation (possibly by
  citing heading path alone, as done here, rather than a page number);
  confirm GAZ-VID's dialect-shift citation by direct read.

### Ch10 — Political Change and Economic Decline: Udaypur under Successive Regimes

#### Ch10.1 Chapter scope and research questions

Per `chapters.md`: "Trace the political transitions that affected Udaypur
and investigate changes in its economic and regional significance. Assess
the evidence for shifts in trade, patronage, settlement and institutional
life rather than attributing decline to a single conquest or political
event." This maps cleanly onto kb3's old-C14 bucket (no split needed).
Research questions: what political transitions did the wider region
undergo after the Paramāras, and which of them have specific, source-
attested Udaypur evidence as opposed to only regional inference; and what
does the corpus establish about continuity (not just decline) at the site
itself.

#### Ch10.2 Relevant sources

- **`History of Paramara Dynasty DC Ganguly.md`** (GAN). Direct evidence —
  its account of the dynasty's final conquest (1305) and, critically, a
  specific Udaypur temple inscription naming a post-conquest ruler there.
  Read directly this pass.
- **`Jagta_Hua_Kasba_EN.md`** (TIW-E). Direct Udaypur evidence, reportage
  register — describes the Tughlaq-era inscriptions and damage at the
  temple from a present-day visitor's perspective, complementing Ch1/Ch7's
  more clinical survey-based accounts.
- **`The cultural heritage of madhya bharat.md`** (PAT-CH) and **`Vidisha
  Gazeteer.md`** (GAZ-VID). Regional/comparative evidence — detailed
  accounts of the Mughal and Maratha periods in the wider district, none
  of it Udaypur-specific, used here as backdrop per the chapter's own
  instruction to assess regional "shifts in trade, patronage, settlement."
- **`Some Paramara Templess.md`** (ADH). Regional/comparative — its "RISE
  AND FALL OF THE PARAMĀRA PATRONS" section frames the dynasty's end in
  terms directly relevant to the chapter, though focused on Un, not
  Udaypur.
- **`History of the Parmar Rajput Dynasty.md`** (PAR, Venziya) — its own
  "Fall of Parmar Dynasty" section, seen via retrieval snippet; not read in
  full this pass.
- **`Samarāṅgaṇa-sūtradhāra`** (`SAM`) — kb3's old-C14 bucket draws some
  generic Vāstu-śāstra material with no Udaypur connection; excluded, same
  discipline as elsewhere.
- **`Art of Paramaras.md`** (uncoded in kb3; see Part B.4). Searched
  directly this revision. Regional/comparative evidence — an earlier
  (12th-century) Paramāra territorial loss to the Chālukyas, not
  previously captured in this chapter, extending the political narrative
  backward from the 1305 final conquest already covered via Ganguly.

#### Ch10.3 Facts, figures, and evidence

**The dynasty's end (regional, establishing the backdrop).** Ganguly's own
framing: "[t]he life and spirit infused into [the Paramāra government] by
the ever-memorable Muñja and Bhoja had long since been blighted. Only the
shadow of its former glory and power remained" before its final defeat
(Ganguly 241) [File: `History of Paramara Dynasty DC Ganguly.md`; sec.
"MAHLAK DEO"; OCR p.241]. The final conquest came in A.H. 705 / 1305 A.D.,
when 'Alā-ud-dīn Khiljī's forces defeated Mahlak Deo (the last Paramāra-
successor ruler) and his general Kokā; Mahlak Deo fled to Mandu and was
there killed, and 'Ain-ul-Mulk was appointed governor of the newly-annexed
province (Ganguly 242) [same file; sec. "FINAL CONQUEST OF MALWA BY THE
MOSLEMS"; OCR p.242].

**A direct, Udaypur-specific data point for post-conquest continuity.**
Ganguly states: "[t]he Paramāra sovereignty was now extinct in Malwa, never
to revive. But for some time longer the banner of its independence was kept
unfurled in Bhilsa by Jayasimha III... An inscription inside the east
entrance of the great temple of Udayapur, tells us that in Sam. 1366 [...]
Mahārājādhirāja Śrī-Jayasimha was ruling there" (Ganguly 243) [File:
`History of Paramara Dynasty DC Ganguly.md`; sec. "JAYASIMHA III"; OCR
p.243]. **This is the single most direct piece of evidence in this corpus
for Udaypur's own political status after the dynasty's main fall** —
naming a specific, inscription-attested ruler at the temple itself, not
merely inferred from regional events. **Caveat, stated plainly rather than
silently corrected:** the source text gives this inscription's date as
"Sam. 1366=1909 A.D.," but Samvat 1366 corresponds to approximately 1309–10
A.D. under the standard Vikrama-era offset, not 1909 — this reads as
either an OCR error or a misprint in the original for "1309 A.D." This
document flags the inconsistency rather than silently substituting a
"corrected" date, since the underlying source document was not independently
checked against this specific figure.

**Temple damage, framed as a lasting visible marker.** Tiwari's account
connects the temple's Tughlaq-era inscriptions directly to continuing
visible damage: "in the rear, western part of the temple, a failed attempt
was made to erect a wall stuck completely against the temple. On both
sides of the temple... two doors were made. These stand to this day, on
which are Tughlaq's inscriptions" (Tiwari) [File: `Jagta_Hua_Kasba_EN.md`].
**Technical note on source quality:** several surrounding lines in this
source file are rendered as single, extremely long lines that this
document's search tooling truncated during this pass ("[Omitted long
context line]") — the passage above is accurately quoted where legible,
but the full surrounding context was not completely read this pass, a
genuine tooling limitation rather than a claim that nothing more exists
there.

**Regional backdrop: successive regimes after the Paramāras (not
Udaypur-specific).** The broader region passed through Delhi Sultanate
control, the independent Malwa Sultanate (Dilawar Khan Ghori, Hoshang Shah,
the Khilji sultans of Malwa), Mughal annexation, and finally Maratha
control (the Scindias at Gwalior, Holkars at Indore, Pawars at Dhar) before
British paramountcy (Patil) [File: `The cultural heritage of madhya
bharat.md`; several sections, exact pages not individually re-confirmed
this pass — carried from kb3's prior citations]. **None of this regional
chronology is itself evidence about Udaypur specifically** — it establishes
the successive regimes the chapter's brief asks about, but this document
does not assume Udaypur experienced each transition identically to the
regional capital.

**An earlier regime change, a century and a half before the final
conquest.** Before the 1305 Khilji conquest that ends Ganguly's narrative
(CH10-E02 above), the Paramāra dominions had already been reduced once:
"Jayasiṃha Siddharāja, a Chālukya ruler of Gujrat, is known to have
defeated Naravarman and his successor Yaśovarman. As a consequence of it,
a great part of the Paramāra dominions was seized by the Chālukyas. During
the reign of his successor Kumārapāla, Mālwā once again became a Chālukya
province" (uncertain author) [File: `Art of Paramaras.md`; sec. "UN—AN
IMPORTANT CENTRE OF PARAMĀRA ART AND ARCHITECTURE"; OCR p.25]. Naravarman
and Yaśovarman reigned in the generation(s) immediately after Udayāditya
(Ch4), so this Chālukya seizure places a documented territorial loss
roughly one to two generations after Udaypur's own founding — a full
century and a half before the 1305 Khilji conquest that ends Ganguly's
narrative. **This means the political "decline" this chapter's brief
warns against attributing to a single event was already underway well
before 1305**, and should be presented as a longer, multi-stage process
rather than a single collapse — though this specific data point remains
regional, not Udaypur-specific.

#### Ch10.4 Relevant excerpts and passage references

| ID | MLA citation | Excerpt / substance | Classification | Technical trace | Caveats |
|---|---|---|---|---|---|
| CH10-E01 | (Ganguly 241) | "Only the shadow of its former glory and power remained" — the dynasty's decline framing | Regional/comparative | [`History of Paramara Dynasty DC Ganguly.md`; sec. "MAHLAK DEO"; OCR p.241] | — |
| CH10-E02 | (Ganguly 242) | Final conquest, 1305 A.D.; Mahlak Deo's death; 'Ain-ul-Mulk appointed governor | Regional/comparative | [same file; sec. "FINAL CONQUEST OF MALWA BY THE MOSLEMS"; OCR p.242] | — |
| CH10-E03 | (Ganguly 243) | Jayasimha III ruling at Udaypur per the temple's own east-entrance inscription, dated "Sam. 1366" | Direct Udaypur evidence; primary-epigraphic content described in a secondary survey | [same file; sec. "JAYASIMHA III"; OCR p.243] | Source's given Gregorian equivalent ("1909 A.D.") appears inconsistent with the stated Samvat year; flagged, not corrected |
| CH10-E04 | (Tiwari) | Tughlaq-era doors/inscriptions at the temple "stand to this day" | Direct Udaypur evidence | [`Jagta_Hua_Kasba_EN.md`] | Surrounding context partly illegible to this pass's search tooling |
| CH10-E05 | (uncertain author) | Jayasiṃha Siddharāja's Chālukya conquest of Naravarman/Yaśovarman; Malwa restored under Kumārapāla | Regional/comparative; an earlier (12th-c.) regime change than CH10-E02 | [`Art of Paramaras.md`; sec. "UN—AN IMPORTANT CENTRE OF PARAMĀRA ART AND ARCHITECTURE"; OCR p.25] | Author's name illegible in OCR |

No fixed excerpt count was applied. Four live retrieval queries plus direct
reading of Ganguly's final two chapters on the dynasty produced this set —
the Jayasimha III find in particular came from reading past the point
kb3's own excerpt selection stopped. A later revision added CH10-E05 from a
direct search of `Art of Paramaras.md`, closing a gap flagged in Part F.

#### Ch10.5 Scholarly interpretations and disagreements

None identified specific to this chapter's evidence this pass.

#### Ch10.6 Research gaps and missing evidence

- The apparent date inconsistency in CH10-E03 (Samvat 1366 vs. "1909 A.D.")
  was not resolved — this would need checking Ganguly's own cited source
  (I.A., Vol. XX) or a direct epigraphic re-reading, neither available this
  pass.
- Tiwari's fuller account of the temple's post-Paramāra history was only
  partly legible to this pass's search tooling (long, untruncated lines) —
  a direct, careful read of the full chapter (not a keyword search) is the
  clear next step.
- No source examined this pass establishes a specific economic indicator
  (trade volume, population, revenue) for Udaypur itself across any of the
  successive regimes — only the region's political control is well
  documented; the chapter's own economic-decline question remains largely
  open at the town level.

#### Ch10.7 Drafting utility

- CH10-E03 (Jayasimha III at Udaypur) is a genuinely novel, high-value
  anchor fact for this chapter and should be given prominent treatment —
  it directly answers part of the chapter's own brief with site-specific,
  not merely regional, evidence.
- CH10-E01/E02 give the necessary regional backdrop and should be
  presented explicitly as backdrop, with CH10-E03/E04 doing the actual
  Udaypur-specific work.
- Cross-reference Ch1/Ch7 for the fuller temple-damage/Tughlaq discussion;
  do not duplicate it here beyond the brief connection in CH10-E04.
- Before publication: resolve the Samvat/Gregorian date discrepancy in
  CH10-E03 before publishing a specific year for Jayasimha III's reign.

### Ch11 — Udaypur in the Modern Period: Archaeology, Heritage Administration and Conservation

#### Ch11.1 Chapter scope and research questions

Per `chapters.md`: "Examine archaeological investigations, heritage
legislation, restoration, repairs and the development of official monument
status, with particular attention to the period after Indian independence.
Consider how archaeological and administrative interventions have shaped
the interpretation, management and conservation of Udaypur's historic
sites." Per the chapter's own annotation ("Original C17 + the conservation
history from the afterword"), this chapter draws on **two** kb3 buckets:
old-C15 (Archaeologists, Laws and Repairs) in full, plus the backward-
looking, already-happened conservation-history material from kb3's old-AF
bucket — explicitly excluding that bucket's forward-looking recommendations
and calls to action, which stay in the new Afterword (Ch11.2 below
explains the split actually applied). Research questions: who has
surveyed, excavated, and restored Udaypur, and when; what is the documented
administrative/legal status of its monuments; and what does the corpus
establish about the gap between official protection and the site's
lived/physical condition.

#### Ch11.2 Relevant sources, and how the AF-bucket split was actually made

- **`Intach Udaypur (1).md`** (INT-ARC). Direct Udaypur evidence — the 2022
  INTACH Bhopal survey itself, the chapter's central primary administrative
  record: dated, named personnel, structure-by-structure grading.
- **`Geo-Heritage of Udaypur The Third Eye.md`** (INT-GEO). Direct Udaypur
  evidence — the companion INTACH geo-heritage survey, with its own
  documentation history and explicit conservation-status statements.
- **`Jagta_Hua_Kasba_EN.md`** (TIW-E). Direct Udaypur evidence, reportage —
  the only source with first-person, named-individual detail on who
  actually did the archaeological work (Dr. Narayan Vyas's ASI career;
  Cunningham's founding survey philosophy) and on a specific past
  resettlement event (houses removed from against the temple).
- **`A_serpentine_scimitar_of_letters_from_Ud.md`** (SIN-S) — already used
  in Ch6; its restoration-campaign dating (Gwalior State 1923–29; ASI
  1981–84) is conservation-history and could equally sit here, but is not
  repeated to avoid duplication — cross-reference only.
- From kb3's old-AF bucket specifically: material describing **completed**
  survey/documentation work (INTACH's "50 heritage sites... built more than
  1000 years ago," the layered "6th century CE to 18th century CE"
  framing, the structure-grading table entries for Shahi Masjid and two
  baolis) is treated as Ch11 evidence, below. Material that is explicitly
  a **recommendation for future action** (community sensitization calls,
  "INTACH can be a... partner by way of developing guides," Tiwari's own
  appeals to send school groups and run heritage walks) is **not** used
  here — reserved for the Afterword.

#### Ch11.3 Facts, figures, and evidence

**Archaeological Survey of India involvement.** The temple "is well
maintained and centrally protected by the Archaeological Survey of India,
which has also carried out a restoration assignment in 1985 CE" (INTACH,
Architectural Splendor 64) [File: `Intach Udaypur (1).md`; OCR p.64]. Dr.
Narayan Vyas, who "had begun his services in the Archaeological Survey of
India (ASI) in 1972," was "at the start of his job... sent directly to
Udaipur," and recalls that houses had been built against three sides of
the temple for "several decades" before being removed, the occupants
"given compensation" (Tiwari) [File: `Jagta_Hua_Kasba_EN.md`] — **a specific,
named-source account of a resettlement/clearance event, not dated precisely
in the passage retained from kb3's prior citation**, flagged as a gap below.

**INTACH's 2022 survey.** "The Architectural Splendor of Udaypur," INTACH
Bhopal's own publication, frames itself as documenting "the layered
history of the village from 6th century CE to 18th century CE" (INTACH,
Architectural Splendor 1) [same file; OCR p.1], naming its convener Dr.
Madanmohan Upadhyay and, in a separate dated note, District Collector
Umashankar Bhargav's involvement as of April 2022 (INTACH, Architectural
Splendor) [same file; exact page not re-confirmed this pass]. A companion
geo-heritage survey independently records that "INTACH Bhopal was carrying
out the documentation on the heritage sites in Udaypur village" over "about
3 years," identifying "about 50 heritage sites built more than 1000 years
ago" (INTACH, Geo-Heritage 18) [File: `Geo-Heritage of Udaypur The Third
Eye.md`; OCR p.18].

**Structure-level administrative status (a direct answer to the chapter's
"legislation" and "official monument status" question).** INTACH's own
structure-grading table records the Shahi Masjid (ID UD/REL/MO/05, 17th
century) under "State Archaeological Department" protection, condition
"Very Good," Grade I*, and in active use; two baolis (Ulaol Dad Bauli,
17th c.; Tulsi Mahadev Bauli, 11th c.) are separately listed, the former
"Unprotected," condition "Moderate," Grade II (INTACH, Architectural
Splendor 115) [same file; sec. heritage-structure table; OCR p.115]. **This
is direct, structure-by-structure evidence of exactly the kind this
chapter's brief asks for** — some monuments officially protected, others
explicitly "Unprotected" despite comparable age, a genuine administrative
gap rather than a uniform conservation regime.

**A specific measurement from active fieldwork.** Before departing Udaypur,
Tiwari records visiting Udayasāmudra "where a week earlier INTACH's team
had already worked and had measured its length as 980 metres" (Tiwari)
[File: `Jagta_Hua_Kasba_EN.md`] — **this both answers part of Ch1/Ch9's
open question about Udayasāmudra's traceability (Ganguly, Ch9, said the
tank "cannot now be traced") and should be flagged as a point of tension
between sources: Ganguly (1933) states the tank is untraceable; this 2020s
INTACH fieldwork, as reported by Tiwari, implies a specific water body has
since been identified and measured as "Udaysāmudra."** This document does
not resolve whether the two refer to the same original structure — it is
recorded as an open question, not silently reconciled.

**The survey philosophy behind India's archaeological administration
(general context).** Tiwari's account traces this to Alexander Cunningham,
who, "[o]n retiring as a Major General at the age of 47... wrote and sent
his scheme regarding India's archaeological wealth to Viceroy Lord
Canning," proposing a low-budget "survey" rather than excavation or
conservation as the first priority (Tiwari) [same file] — general historical
context for how the ASI itself came to exist, not Udaypur-specific, but
directly relevant background for why Udaypur's own survey history (Ch11.3
above) looks the way it does.

#### Ch11.4 Relevant excerpts and passage references

| ID | MLA citation | Excerpt / substance | Classification | Technical trace | Caveats |
|---|---|---|---|---|---|
| CH11-E01 | (INTACH, Architectural Splendor 64) | ASI restoration assignment, 1985 CE | Direct Udaypur evidence | [`Intach Udaypur (1).md`; OCR p.64] | — |
| CH11-E02 | (Tiwari) | Dr. Narayan Vyas's 1972 ASI posting to Udaypur; houses removed from against the temple, with compensation | Direct Udaypur evidence; named informant | [`Jagta_Hua_Kasba_EN.md`] | Clearance event not precisely dated in the retained excerpt |
| CH11-E03 | (INTACH, Architectural Splendor 1) | INTACH's 2022 survey frames a "layered history... 6th century CE to 18th century CE" | Direct Udaypur evidence | [same file; OCR p.1] | — |
| CH11-E04 | (INTACH, Geo-Heritage 18) | ~3-year INTACH documentation effort; ~50 heritage sites over 1000 years old identified | Direct Udaypur evidence | [`Geo-Heritage of Udaypur The Third Eye.md`; OCR p.18] | — |
| CH11-E05 | (INTACH, Architectural Splendor 115) | Shahi Masjid: state-protected, Grade I*; Ulaol Dad Bauli: unprotected, Grade II | Direct Udaypur evidence; structure-level administrative status | [`Intach Udaypur (1).md`; sec. heritage-structure table; OCR p.115] | — |
| CH11-E06 | (Tiwari) | Udayasāmudra measured at 980m by INTACH's field team | Direct Udaypur evidence; in tension with Ganguly's "cannot now be traced" (Ch9, CH9-E03) | [`Jagta_Hua_Kasba_EN.md`] | Not resolved whether the same structure is meant; recorded as an open question |
| CH11-E07 | (Tiwari) | Cunningham's founding "survey, not excavation" philosophy for the ASI | General contextual evidence | [same file] | Not Udaypur-specific |

No fixed excerpt count was applied. Direct reading of kb3's retained old-
C15/AF excerpts, cross-checked against Ch1/Ch9's existing citations for the
Udayasāmudra tension noted above, produced this set.

#### Ch11.5 Scholarly interpretations and disagreements

- **The Udayasāmudra tension** (CH11-E06 vs. Ch9's CH9-E03): Ganguly
  (1933) states the tank cannot be traced; a 2020s INTACH field measurement,
  as reported by Tiwari, implies a specific body of water has since been
  identified and measured under that name. This document records both
  without resolving them — it is a genuine open question whether modern
  surveys identified the original Udayasāmudra or are applying the name to
  a plausible candidate.

#### Ch11.6 Research gaps and missing evidence

- CH11-E02's resettlement/clearance event is not dated precisely in the
  material retained from kb3's prior excerpt — a direct read of the
  surrounding TIW-E text would be needed to establish when this occurred.
- This document has not independently verified INTACH's "50 heritage
  sites" count or cross-checked it against the structure-grading table's
  own entries for consistency.
- No source examined this pass addresses heritage *legislation* specifically
  (e.g. the Ancient Monuments and Archaeological Sites and Remains Act) by
  name in connection with Udaypur — the chapter's own brief asks about
  "heritage legislation" specifically, and this remains a gap.

#### Ch11.7 Drafting utility

- CH11-E01/E03/E04/E05 give the chapter its administrative backbone and
  should be presented as the core evidence.
- CH11-E06's tension with Ch9's CH9-E03 is a good, concrete example of the
  chapter's own "distinguishing documented events from traditions whose
  historical origins remain uncertain" instruction (echoing Ch9's own
  brief) and deserves explicit treatment, not a silent pick of one claim
  over the other.
- Cross-reference Ch6 (Singh's restoration-campaign dating for the
  serpentine-scimitar stone, 1923–1984) as a second, independent
  conservation-history data point, without repeating it here.

### Ch12 — Udaypur Today: A Living Community and Its Historic Environment

#### Ch12.1 Chapter scope and research questions

Per `chapters.md`: "Present Udaypur as a living settlement rather than
merely an archaeological site. Explore contemporary livelihoods, community
relationships with historic monuments, local aspirations and the practical
tensions between conservation and everyday life, drawing on *Udaypur Jagta
Hua Kasba* and other relevant sources." This maps onto kb3's old-C16 bucket
(no split needed) — fittingly, the chapter the chapters.md annotation
itself names `Jagta Hua Kasba` for is also the chapter where TIW-E/TIW-H
dominate kb3's own bucket by volume (TIW-H alone supplies 28%). Research
questions: how is the temple actually used today, as a living religious
site, not only a protected monument; what grassroots community action
(distinct from INTACH's institutional survey work, already covered in
Ch11) has shaped the site's recent history; and what tensions exist
between everyday village life and conservation.

#### Ch12.2 Relevant sources

- **`The Udayesvara Temple - Anupa Pande.md`** (PAN). Direct Udaypur
  evidence — explicitly states the temple remains a living site of daily
  worship "right up to the 21st century."
- **`कथा उदयपुर... Hindi original`** (TIW-H) and **`Jagta_Hua_Kasba_EN.md`**
  (TIW-E). Direct Udaypur evidence — the chapter's named anchor texts per
  `chapters.md` itself. TIW-H is confirmed unindexed (Part B), so its
  content here is cited via kb3's prior excerpts, not independently
  re-verified against live text this pass; TIW-E (the active English
  translation) is used wherever the same content is available in English.
- **`Intach Udaypur (1).md`** (INT-ARC). Direct Udaypur evidence — precise
  fieldwork dates for the 2021 survey that catalyzed much of the recent
  institutional attention described narratively by TIW-E/TIW-H.
- **`History of Paramara Dynasty DC Ganguly.md`** (GAN) — a single
  village-level social-welfare anecdote (a stepwell funded by community
  subscription at Bhuṇḍīpadra) is regional/comparative, not about Udaypur,
  and is noted only as a historical parallel to the modern community
  road-building described below.

#### Ch12.3 Facts, figures, and evidence

**The temple today — a living site, not only a monument.** Pande states
plainly that "this temple is a living one, where right up to the 21st
century, there are the usual morning and evening pūjā and āratī," with
priests performing special pūjās such as Rudrāṣṭaka "on request" (Pande 92)
[File: `The Udayesvara Temple - Anupa Pande.md`; OCR p.92]. A nearby house,
"Ghaṛiyāloṉ kā Makān" ("house of the time-keepers"), is occupied by a
family who "claim to have been there for centuries," their hereditary
vocation being to strike the temple's gong to keep ritual timing (Pande 92)
[same file and page] — **a specific, named continuity-of-practice claim**,
though the family's own multi-century claim is not independently verified
by any documentary source in this corpus and should be presented as a
reported claim, not confirmed fact.

**Grassroots local activism, distinct from INTACH's institutional
survey.** TIW-H/TIW-E describe local residents acting before INTACH's
formal involvement: "real[ly], some aware citizens became active...
Ganj Basoda's enthusiastic Praveen Sharma, Kaustubh Shirhonkar, Kamlesh
Sharma, Gagan Dubey, Amit Shukla, Udaypur's Raja Miyan, Mandi Bamora's
Ramiskant Shrivastava... and many others... on their initiative, local
people themselves first began removing encroachments. After that, they
took up the task of clearing the obstructed path to reach the temple...
and, before long, a roughly three-foot-wide cemented road was built
through public cooperation [*jansahayog*]" (Tiwari) [File: `कथा उदयपुर
(Jagta Hua Kasba) — Hindi original`; TIW-H, cited via kb3's prior excerpt,
not independently re-verified this pass] — **direct evidence of
bottom-up community action predating, and distinct from, the institutional
INTACH survey work covered in Ch11.**

**The "Katha Udaipur" talk as a documented catalytic event.** Tiwari
recounts organizing a heritage-walk presentation titled "Kathā Udaipur"
("The Story of Udaipur") at Bhopal's Tribal Museum, illustrated with
photographs by "Praveen Sharma and Saurabh Tamedhari," which drew a named
audience including retired officials, historians, and "the RSS regional
co-secretary Hemant Muktibodh" (Tiwari) [File: `Jagta_Hua_Kasba_EN.md`].
Tiwari explicitly connects this event to INTACH's subsequent, formal
involvement: "[o]n INTACH's initiative, after our story centred on the
Udaipur heritage walk was heard for the first time at the Tribal Museum,
now, at the Bhopal level, the groundwork of INTACH's team began... Dr. M.
M. Upadhyay... fixed a one-day tour of Udaipur" (Tiwari) [same file] —
**a direct, source-stated causal link between grassroots/media attention
and the institutional survey work this document covers separately in
Ch11**, worth presenting as cause-and-effect rather than two unconnected
developments.

**Precise fieldwork dates (complementing Ch11's administrative account).**
INTACH's own survey states: "[t]he first survey was conducted from 14th to
27th March 2021 CE to explore Udaypur village and the second field survey
was organized on 3rd to 5th July 2021 CE to visit the nearby villages"
(INTACH, Architectural Splendor 7) [File: `Intach Udaypur (1).md`; sec.
"Methodology"(approx.); OCR p.7]. **Note on dating:** Ch11 cites an April
2022 note naming the district collector's involvement — this is consistent
with, not contradictory to, the 2021 fieldwork dates here: fieldwork
(2021) evidently preceded publication/public administrative engagement
(2022), a normal sequence, not a discrepancy, though this document has not
independently confirmed the publication date of "The Architectural
Splendor of Udaypur" itself.

#### Ch12.4 Relevant excerpts and passage references

| ID | MLA citation | Excerpt / substance | Classification | Technical trace | Caveats |
|---|---|---|---|---|---|
| CH12-E01 | (Pande 92) | Temple remains in active daily worship "right up to the 21st century" | Direct Udaypur evidence | [`The Udayesvara Temple - Anupa Pande.md`; OCR p.92] | — |
| CH12-E02 | (Pande 92) | Ghaṛiyāloṉ kā Makān family's multi-century time-keeping claim | Direct Udaypur evidence; the family's own reported claim, not independently verified | [same file and page] | Longevity claim not documented elsewhere in this corpus |
| CH12-E03 | (Tiwari) | Named local activists removing encroachments and building a community-funded road to the temple | Direct Udaypur evidence; ethnographic/contemporary | [`कथा उदयपुर (Jagta Hua Kasba) — Hindi original`] | TIW-H is unindexed; cited via kb3's prior excerpt, not independently re-verified against live text this pass |
| CH12-E04 | (Tiwari) | "Katha Udaipur" Bhopal talk and its named attendees | Direct Udaypur evidence; contemporary | [`Jagta_Hua_Kasba_EN.md`] | — |
| CH12-E05 | (Tiwari) | Explicit causal link: this talk → INTACH's subsequent survey | Direct Udaypur evidence; source-stated causal claim | [same file] | — |
| CH12-E06 | (INTACH, Architectural Splendor 7) | Precise 2021 fieldwork dates (two survey phases) | Direct Udaypur evidence | [`Intach Udaypur (1).md`; OCR p.7] | — |

No fixed excerpt count was applied. This chapter's evidence came from
direct reading of Pande's "living temple" passage and the retained kb3
excerpts for TIW-E/TIW-H/INT-ARC, cross-checked for internal date
consistency against Ch11.

#### Ch12.5 Scholarly interpretations and disagreements

None identified specific to this chapter. The apparent 2021-vs-2022 date
difference between this chapter and Ch11 is resolved above as sequence, not
contradiction, though not independently confirmed.

#### Ch12.6 Research gaps and missing evidence

- The Ghaṛiyāloṉ kā Makān family's claimed multi-century tenure (CH12-E02)
  is not independently documented anywhere else in this corpus — recorded
  as a reported claim, not verified fact.
- TIW-H's content here was not independently re-verified against live
  text this pass, since the source is confirmed unindexed (Part B) — this
  is the same limitation flagged throughout this document wherever TIW-H
  is the only source for a claim.
- The exact publication date of "The Architectural Splendor of Udaypur"
  was not independently confirmed, leaving the 2021-fieldwork/2022-notice
  sequence as a reasonable but unverified inference.

#### Ch12.7 Drafting utility

- CH12-E01/E02 should open the chapter — they most directly answer the
  brief's instruction to present Udaypur "as a living settlement rather
  than merely an archaeological site."
- CH12-E03/E04/E05 (grassroots activism → Katha Udaipur talk → INTACH
  involvement) form a clean causal narrative arc and should be presented
  in that sequence, distinct from Ch11's more administrative framing of
  the same broad period.
- Cross-reference Ch8 (livelihoods) and Ch9 (festivals, named tradition-
  bearers) — several of the same named individuals (Praveen Sharma, Dr.
  Narayan Vyas) appear across both chapters and should be cross-linked,
  not reintroduced as if new.

### Afterword — Conserving Udaypur: Community, Heritage and the Future

#### AW.1 Chapter scope and research questions

Per `chapters.md`: "Reflect on the future of Udaypur and the possibilities
for combining heritage conservation with local well-being. Consider the
roles of residents, conservation professionals, researchers,
administrators and visitors, with emphasis on realistic interventions,
community participation and sustainable stewardship." This draws on the
**remainder** of kb3's old-AF bucket — specifically the explicitly
forward-looking recommendation material that Ch11 deliberately excluded
(Part A.5, Ch11.2). Research questions: what concrete, source-stated
recommendations exist for Udaypur's future conservation and development;
who do those recommendations name as responsible stakeholders; and what
unresolved research questions do the surveys themselves flag for future
work.

#### AW.2 Relevant sources

- **`Geo-Heritage of Udaypur The Third Eye.md`** (INT-GEO). Direct Udaypur
  evidence — by far the richest source for this chapter: a dedicated,
  numbered recommendations section and an explicit conclusions chapter
  naming stakeholders and open research questions. Read directly, both
  sections, this pass.
- **`Intach Udaypur (1).md`** (INT-ARC) — its own forward-looking material
  (INTACH's intended future role as a convening partner) is comparatively
  thin next to INT-GEO's; not separately quoted here beyond what Ch11
  already captures for the completed-work side of INTACH's involvement.
- **`Jagta_Hua_Kasba_EN.md`** (TIW-E) — Tiwari's own appeals (for
  institutions, schools, and local representatives to engage further) are
  forward-looking in spirit but were captured as part of the "named
  tradition-bearers" discussion in Ch9 rather than duplicated here.

#### AW.3 Facts, figures, and evidence

**A numbered, concrete recommendations list.** INT-GEO's survey states six
specific recommendations: (1) improving approach roads inside the village
and to the hill, with directional signage; (2) developing a parking area
between the Naṭarāja sculpture and the fortification wall, acknowledging
explicitly that "[t]he tourists will not start coming in from day one...
[t]he site will be developed over a period"; (3) using the existing
thousand-year-old hillside gateway as the formal entrance to a proposed
"Geo Heritage Reserve"; (4) a new visitor pathway aligned along the hill's
contours, designed to lead visitors chronologically "from the 11th century
to the Gupta period" rock-cut features, explicitly noting that the village
panchayat's own existing step-path "is very poorly planned"; (5) [not
separately numbered in the source as extracted]; (6) a site development
plan "in harmony with eco-tourism," naming the Madhya Pradesh Ecotourism
Development Board as an existing institutional partner (INTACH,
Geo-Heritage 150–152) [File: `Geo-Heritage of Udaypur The Third Eye.md`;
sec. "The major recommendation is the following:"; OCR p.150–152].

**Explicit stakeholder naming.** The survey's conclusion names five
stakeholder categories by institutional role: "Forest Department,
Archaeology department, Tourism department, Panchayat and rural
development, Geological Survey of India," noting that "[o]ther associated
stakeholders also needed to be taken on board" (INTACH, Geo-Heritage 153)
[same file; sec. "17. CONCLUSIONS"; OCR p.153], and separately states that
this documentation "needs to be shared with the Archaeological Survey of
India and the Directorate of Archaeology, Archives and Museums, Madhya
Pradesh, apart from the department of public relations and tourism, to
create awareness among the population of this area" (INTACH, Geo-Heritage
154) [same file; OCR p.154].

**Explicit, named research gaps for future work — in the source's own
words, not this document's inference.** The survey states plainly that
"more research needs to be done to go behind the history of the dynasty
that occupied this territory before the Parmars of Malwa" (INTACH,
Geo-Heritage 153) [same file and page], and that, regarding the hill's
caves, "looking for the safety concerns inside these deep caves, the depth
and other aspects of Archaeological significance inside these caves have
not been explored. This is something to work upon by future researchers
into the geology and archaeology of these caves" (INTACH, Geo-Heritage 153)
[same file and page]. **These are the source's own stated research gaps,
not ones this document has inferred** — a rare case of a survey explicitly
scoping its own incompleteness for future work, directly useful for this
chapter's "realistic interventions" framing.

**Institutional commitment already in motion (bridging to Ch11, not
repeating it).** The survey notes that "INTACH Bhopal chapter has already
initiated steps to conserve the entire complex by notifying this as an
archaeological site of historical significance and national importance"
(INTACH, Geo-Heritage 153) [same file and page] — forward motion already
underway at the time of writing, distinct from the completed survey work
covered in Ch11.

#### AW.4 Relevant excerpts and passage references

| ID | MLA citation | Excerpt / substance | Classification | Technical trace | Caveats |
|---|---|---|---|---|---|
| AW-E01 | (INTACH, Geo-Heritage 150) | Approach-road and signage recommendation | Direct Udaypur evidence; explicit recommendation | [`Geo-Heritage of Udaypur The Third Eye.md`; sec. "The major recommendation is the following:"; OCR p.150] | — |
| AW-E02 | (INTACH, Geo-Heritage 150) | Parking development; explicit acknowledgment that visitor growth will be gradual | Direct Udaypur evidence; explicit recommendation | [same file and page] | — |
| AW-E03 | (INTACH, Geo-Heritage 151) | Thousand-year-old gateway proposed as formal reserve entrance | Direct Udaypur evidence; explicit recommendation | [same file; OCR p.151] | — |
| AW-E04 | (INTACH, Geo-Heritage 151–152) | Contour-aligned visitor pathway; explicit criticism of the panchayat's existing path as "poorly planned" | Direct Udaypur evidence; explicit recommendation, including a direct criticism of existing local infrastructure | [same file; OCR p.151–152] | — |
| AW-E05 | (INTACH, Geo-Heritage 152) | Eco-tourism site development plan; MP Ecotourism Development Board named as partner | Direct Udaypur evidence; explicit recommendation | [same file; OCR p.152] | — |
| AW-E06 | (INTACH, Geo-Heritage 153) | Five named stakeholder departments; "other stakeholders... needed" | Direct Udaypur evidence | [same file; sec. "17. CONCLUSIONS"; OCR p.153] | — |
| AW-E07 | (INTACH, Geo-Heritage 153) | Explicit call for future research into the pre-Paramāra occupants of the site | Direct Udaypur evidence; source-stated research gap | [same file and page] | — |
| AW-E08 | (INTACH, Geo-Heritage 153) | Explicit call for future archaeological/safety exploration of the hill's caves | Direct Udaypur evidence; source-stated research gap | [same file and page] | — |

No fixed excerpt count was applied. Three live retrieval queries plus a
full direct read of INT-GEO's recommendations and conclusions sections
produced this set.

#### AW.5 Scholarly interpretations and disagreements

None — this chapter's material is prescriptive/recommendatory rather than
interpretive, and no source examined disputes another's recommendations.

#### AW.6 Research gaps and missing evidence

- This chapter deliberately reports the source's *own* stated research
  gaps (AW-E07/E08) rather than this document inventing new ones — readers
  should treat these as the survey's own scoping, not this rebuild's
  independent judgment.
- INT-ARC's and TIW-E's own forward-looking material (INTACH's intended
  convening role; Tiwari's appeals for school/institutional engagement) was
  judged thinner than INT-GEO's and not separately quoted here — a closer
  read of both, specifically filtered for forward-looking content not
  already used in Ch9/Ch11/Ch12, could still add to this chapter.
- Recommendation 5 in INT-GEO's numbered list was not captured in the
  text available to this pass (the source's own numbering jumps from 4 to
  6 in the retrieved text) — flagged as a gap in what was retrieved, not
  evidence that no fifth recommendation exists in the source.

#### AW.7 Drafting utility

- AW-E01–E06 give the chapter a concrete, source-grounded action agenda
  and should structure its central section.
- AW-E07/E08 are strong closing material — ending the book on the
  survey's own acknowledged open questions is a natural, honest way to
  close without overclaiming completeness.
- Cross-reference Ch11 (completed conservation work) and Ch9/Ch12
  (grassroots activism, named tradition-bearers) so the Afterword reads as
  a forward-looking synthesis of people and institutions already
  introduced, not a disconnected final chapter.

## Part D — Cross-chapter evidence and thematic index

Part C is now complete (all 13 sections). This index surfaces material,
people, places, and methodological decisions that more than one chapter
dossier depends on, so each is discoverable from every chapter it touches,
not only the one it was first written into.

### D.1 Contested historical questions (span multiple chapters)

- **Udayāditya's accession date.** Central to **Ch4** (CH4-E05, the
  Pānāhēḍā/Jayasiṃha counter-evidence), directly grounded by **Ch1**'s
  foundation-inscription dating (CH1-E01/E02), and independently
  corroborated at one end of the range by **Ch5**'s Pande citation
  (CH5-E01, "ascended the throne in 1070 CE"). A reader starting from any
  of these three chapters should be pointed to the other two.
- **Udayāditya's relationship to Bhoja.** Central to **Ch4** (CH4-E06–E09,
  Trivedi's analysis of the Dongargaon/Jainad inscriptions and his explicit
  rejection of a rival genealogy). No other chapter depends on this
  directly, but **Ch9**'s founding-legend material (below) is thematically
  adjacent — both are cases of multiple primary/legendary accounts of
  Udayāditya's origins that do not reconcile.
- **Four independent corroborations that Muhammad Tughlaq, not
  Aurangzeb, damaged the temple.** First established in **Ch1** (CH1-E08,
  Patil). Independently corroborated in **Ch7** (CH7-E07/E08, Beglar's
  1871–72 report quoted in Pande), again in **Ch10** (CH10-E04, Tiwari,
  describing the same Tughlaq-era doors/inscriptions as still visible
  "today"), and a fourth time in **Ch5** (CH5-E12, Mittal, in `Art of
  Paramaras.md`). This is the single most robustly corroborated factual
  claim in the entire document — four independent sources, four different
  registers (official survey, colonial eyewitness report, present-day
  reportage, art-historical survey).

- **`Art of Paramaras.md` — a second source kb3 never bucketed, found by
  direct search rather than live retrieval.** Flagged through most of this
  rebuild as fully indexed but never actually cited (Part F), this source
  was closed out by a targeted direct read rather than relying on vector
  search, which did not surface its Udaypur-specific content reliably even
  when queried directly (D.5's `Inscriptions Corpus.md` was found via
  retrieval; this one was not, and needed a plain keyword search of the
  raw file instead). It now supplies new measurements in **Ch5** (CH5-E09/
  E10), the fourth Tughlaq corroboration above, a minor shrine-count
  variant and an unresolved 1754/1775 date conflict (also Ch5), and
  regional dynastic-succession material in **Ch4** (CH4-E11/E12) and
  **Ch10** (CH10-E05). The methodological lesson matches D.5's: a source's
  absence from kb3's prior excerpts does not mean a chapter should stop at
  "not adequately examined" once it is confirmed to be indexed and
  reachable — but it also demonstrates that live vector retrieval alone is
  not always sufficient to reach a source's content; direct keyword search
  of the raw file was necessary here.

### D.2 Udaypur's founding: legend and record together

Three mutually unreconciled oral/legendary founding accounts exist in this
corpus, recorded in two different chapters because they came from two
different kb3 source buckets:

1. The Bhrangarajpur/native-chief legend (**Ch1**, CH1-E05, INT-GEO).
2. The Gond-conquest oral tradition (**Ch1**, CH1-E06, INT-GEO).
3. The snake-and-treasure legend (**Ch9**, CH9-E01/E02, Ganguly) — the only
   one of the three where the source itself explicitly says, in the same
   breath, "no doubt an absolute myth... there is evidence, in the words
   of a contemporary inscription, that the city was built by Udayāditya."

A reader drafting the "historical memory vs. documented history" framing
this book's Ch1 brief calls for should consult all three together, plus the
one thing none of the legends supply but the inscriptions do: the actual
foundation record itself (CH1-E01–E03, **Ch1**/**Ch4**/**Ch6**).

### D.3 The foundation inscription and its triple naming

Udayāditya's inscription naming the town, temple, and tank after himself
(Udayapura / Udayeśvara / Udayasāmudra) is the document's single most
load-bearing primary fact. It originates in **Ch1** (CH1-E01–E03, drawing
on Patil and `Inscriptions Corpus.md`), is the fixed point both of **Ch4**'s
accession-date dispute and **Ch6**'s discussion of the temple's inscribed
output more broadly. Do not re-derive it independently in any other
chapter — cite Ch1.

### D.4 Udayasāmudra: an open tension, not a resolved fact

**Ch9** (CH9-E03) records Ganguly's 1933 statement that the tank "cannot
now be traced." **Ch11** (CH11-E06) records a 2020s INTACH field
measurement (980 metres), as reported by Tiwari, of a feature called
"Uday Samudra." Neither chapter resolves whether these refer to the same
structure. This is flagged in both places and should stay flagged if a
chapter draft touches the tank again — it is a genuine open question, not
an oversight to quietly pick a side on.

### D.5 `Inscriptions Corpus.md` — a source kb3 never had

This Trivedi-edited ASI volume carries no kb3 code at all (Part B.4) and
turned out to be the single highest-value discovery of this entire rebuild.
It supplies: the "Udayapura still bears this name" continuity evidence in
**Ch1** (CH1-E03); the Dongargaon, Jainad, and Pānāhēḍā inscriptions that
ground **Ch4**'s two central disputes (CH4-E05–E09); and general
palaeographic-method background noted in **Ch6**. Any future chapter
touching Paramāra-era epigraphy should check this source directly, not
rely on kb3's excerpts, since kb3 never indexed it.

### D.6 Methodological thread: `SAM`'s source-domination problem

kb3's own `kb3/retrieval.yaml` measured that the Samarāṅgaṇa-sūtradhāra
supplied 26–38% of every one of its seventeen chapter buckets by raw
chunk volume — the single largest contributor in nearly every case. This
rebuild does not inherit kb3's automatic source-domination cap (Part A.8),
so the exclusion had to be re-applied by hand, chapter by chapter, after
checking whether the SAM material retrieved was actually about Udaypur or
merely topically adjacent (architectural/ritual vocabulary, Jambudvīpa
cosmology). **SAM was excluded as off-topic in Ch1, Ch2, Ch3, Ch6, Ch8,
Ch9, and Ch10** — in each case because the specific passages in that
chapter's kb3 bucket were generic Śilpaśāstra prescription or Purāṇic
cosmology with no demonstrated Udaypur connection, not because SAM is
categorically irrelevant (**Ch5** and **Ch4** both treat it as
legitimately relevant background to the Bhūmija style and Bhoja's
authorship respectively, without it dominating the evidence there).

### D.7 The two INTACH surveys — the corpus's backbone source

`Intach Udaypur (1).md` (INT-ARC) and `Geo-Heritage of Udaypur The Third
Eye.md` (INT-GEO) between them supply direct Udaypur evidence in eleven of
the thirteen chapters (all except Ch4 and Ch5, which are period-specific
dynastic/architectural-interpretation chapters with less occasion to cite a
2021–2024 field survey). Specifically: location/demography/geology (**Ch1**,
**Ch2**); flora/fauna (**Ch2**); further inscriptions (**Ch6**); the
fortification wall, gates, stepwells (**Ch7**); market access and current
livelihoods (**Ch8**); festival corroboration (**Ch9**); the full survey
administrative record (**Ch11**); fieldwork dates and the living-temple
framing (**Ch12**); and the forward-looking recommendations (**Afterword**).
Any revision to how these two sources are read should be checked against
all eleven chapters, not just the one being edited.

### D.8 Named present-day individuals appearing in more than one chapter

- **Dr. Narayan Vyas** (ASI archaeologist, posted to Udaypur from 1972) —
  **Ch9** (named tradition-bearer) and **Ch11** (CH11-E02, the resettlement
  account).
- **Dr. Madanmohan Upadhyay** (INTACH Bhopal convener) — **Ch11** and
  **Ch12** (the "Katha Udaipur" → INTACH involvement causal chain).
- **Praveen Sharma** (local social worker/activist) — **Ch9** (named
  tradition-bearer) and **Ch12** (grassroots road-building, CH12-E03).
- **Deepak Sharma** (Pragya Pravah) and **Santosh Kumar Verma** (Ganj
  Basoda historian) — both **Ch9** only, not yet cross-referenced
  elsewhere; a candidate for a future chapter revision if their work
  touches Ch11/Ch12's subjects.

### D.9 The Betwa river and Paramāra-era water engineering

The river itself is **Ch2**'s central subject. Paramāra-era hydraulic
engineering on the same river system — Bhoja's dam at Bhojpur, a different
site on the same river — is **regional/comparative** evidence in **Ch2**
(CH2-E12) and reappears as context for Udayāditya's own tank in **Ch1** and
the Udayasāmudra tension in **Ch9**/**Ch11** (D.4 above). These should
stay distinguished: a dam elsewhere on the same river is not evidence
about Udaypur's own tank.

### D.10 The Un temple cluster and Adhikari's survey

`Some Paramāra Temples From Madhya Pradesh` (ADH) supplies regional/
comparative evidence in four chapters: the Chirakhan quarry and its
stone-quality argument (**Ch2**, CH2-E10); Bhoja-era chronology
corroboration (**Ch4**); comparative iconography, specifically the
Cāmuṇḍā placement parallel (**Ch5**, CH5-E07); and the dynasty's decline
framing ("RISE AND FALL OF THE PARAMĀRA PATRONS," **Ch10**). In every case
Un, not Udaypur, is the subject — this is consistently labeled
regional/comparative, never upgraded to direct Udaypur evidence.

### D.11 `Temple Economics.md` — the policy case study

Established in Phase B1 (before this rebuild began) and formally applied
in **Ch8**: general-context eligible, never direct Udaypur evidence absent
passage-level confirmation, which this document has still never found.
This is the clearest worked example in the whole document of the
general-context-vs-direct-evidence distinction the master prompt's
instructions asked for, and is referenced here so a future chapter is not
tempted to treat this source differently.

---

## Part E — Source-to-chapter coverage matrix

All 29 tracked source identities (27 kb3-coded, plus `Art of Paramaras.md`
and `Inscriptions Corpus.md` from Part B.4) against all 13 sections. Status
codes, matching the task's required categories:

- **D** — Direct evidence found
- **R** — Relevant regional/comparative evidence found
- **C** — Contextual material found
- **P** — Potential relevance not yet verified
- **E** — Examined; no relevant material identified
- **N** — Not adequately examined
- **U** — Source unavailable or not indexed

A blank cell never appears below — every cell is one of the seven codes
above, so "nobody checked" (**N**) is always distinguishable from "checked,
nothing there" (**E**) and from "unavailable regardless of chapter" (**U**).

| Code | Source | Ch1 | Ch2 | Ch3 | Ch4 | Ch5 | Ch6 | Ch7 | Ch8 | Ch9 | Ch10 | Ch11 | Ch12 | AW |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SKP-13 | Skanda-Purāṇa XIII | E | E | P | N | E | N | N | N | E | N | N | N | N |
| HAR | Hardy, Temple Architecture | N | N | P | N | C | N | N | N | N | N | N | N | N |
| BET-K | Streamflow of the Betwa | N | R | N | N | N | N | N | N | N | N | N | N | N |
| SIN-B | Bhoja Paramara and His Times | U | U | U | U | U | U | U | U | U | U | U | U | U |
| BHJ-H | भोजदेव (Bhojadeva) | N | E | E | P | N | P | N | P | E | N | N | N | N |
| INT-GEO | Geo-Heritage of Udaypur | D | D | N | N | N | N | D | N | N | N | D | N | D |
| GUP | Iconography (Gupte) | N | N | N | N | N | N | N | N | N | N | N | N | N |
| INT-ARC | Intach Udaypur | D | D | N | N | N | D | D | D | D | N | D | D | P |
| TIW-E | Jagta Hua Kasba (EN) | E | N | N | D | N | P | D | N | D | D | D | D | P |
| TIW-H | कथा उदयपुर (Hindi) | U | U | U | U | U | U | U | U | U | U | U | U | U |
| BET-S | Betwa climatic changes | N | R | N | N | N | N | N | N | N | N | N | N | N |
| PAT-CH | Cultural Heritage of Madhya Bharat | D | R | D | N | N | N | N | N | N | R | N | N | N |
| GAN | History of the Paramāra Dynasty | N | N | N | D | N | D | N | N | D | D | N | N | N |
| PAR | History of the Parmar Rajput Dynasty | N | N | N | D | N | N | N | N | P | P | N | N | N |
| RAJ-E | King Bhoj and Paramara-period Town Architecture | N | D | N | D | N | N | N | N | R | N | N | N | N |
| SAM | Samarāṅgaṇa-sūtradhāra (2 files) | E | E | E | P | P | E | N | E | E | E | N | N | N |
| SIN-S | Serpentine scimitar paper | N | N | N | R | N | D | N | N | N | N | D | N | N |
| ADH | Some Paramāra Temples (Un) | N | R | N | D | D | N | N | N | N | R | N | N | N |
| PAT-INS | Patil composite (inscriptions) | U | U | U | U | U | U | U | U | U | U | U | U | U |
| PAT-TEM | Patil composite (temples) | U | U | U | U | U | U | U | U | U | U | U | U | U |
| SIN-T | Temple Economics | N | N | N | N | N | N | N | C | N | N | N | N | N |
| DEV | Temples of North India/India | N | N | N | P | C | N | N | N | N | N | N | N | N |
| KRAM-1 | Hindu Temple Vol I | N | C | N | N | C | N | N | N | N | N | N | N | N |
| KRAM-2 | Hindu Temple Vol II | N | N | N | N | C | N | N | N | N | N | N | N | N |
| PAN | Anupa Pande (resolved copy) | N | N | N | N | D | N | D | E | N | N | N | D | N |
| GAZ-VID | Vidisha Gazetteer | D | D | D | N | N | N | D | R | R | R | N | N | N |
| RAJM | Rājamārtaṇḍa-vṛtti | U | U | U | U | U | U | U | U | U | U | U | U | U |
| — | Art of Paramaras.md | N | N | N | R | D | N | N | N | N | R | N | N | N |
| — | Inscriptions Corpus.md | D | N | N | D | N | C | N | N | N | N | N | N | N |

### E.1 Reading the matrix

- **`Art of Paramaras.md` was initially never used as evidence in any of
  the 13 chapters**, despite being fully indexed (65 chunks) and its
  catalogue/identity question fully resolved in Phase B1 — flagged as an
  unflattering finding in an earlier revision of this document. A
  follow-up direct search (prompted by that finding) closed the gap: it
  now contributes direct evidence to Ch5 and regional/comparative evidence
  to Ch4 and Ch10 (two dedicated Hindi-language articles, one on the
  Udayeśvara temple specifically). The matrix row above reflects this
  update. The methodological lesson stands regardless: live vector
  retrieval alone did not surface this source reliably even when directly
  queried — a plain keyword search of the raw file was what actually
  found the relevant content (Part D).
- **`GUP` (Gupte's iconographic handbook) was not adequately examined in
  any chapter** — every cell is **N**. Given its subject (iconographic
  identification handbook) is directly relevant to Ch5's sculptural
  programme discussion, this is a specific, named gap for the next pass.
- **The four unindexed/absent sources (`SIN-B`, `TIW-H`, `RAJM`,
  `PAT-INS`/`PAT-TEM`) are marked `U` uniformly** — their unavailability is
  a corpus-wide fact (Part B), not a chapter-specific judgment, so the
  matrix does not pretend some chapters checked harder than others.
- **`Inscriptions Corpus.md`'s matrix row is the clearest visual confirmation
  of this rebuild's central methodological finding**: a source entirely
  invisible to kb3 turned out to carry direct evidence in two chapters and
  contextual value in a third, simply because it was searched directly
  rather than inherited from a prior excerpt sample.

---

## Part F — Completeness and limitations report

### F.1 Source-level numbers

- **29** source identities tracked (27 kb3-coded + 2 uncoded active sources
  from Part B.4).
- **22 of 29** confirmed indexed and live-queryable in
  `udaypur_corpus_openai_large` right now.
- **6** confirmed physically present somewhere in the project tree but
  **not** indexed in the active collection: `SIN-B`, `TIW-H`, `RAJM`,
  `PAT-INS`, `PAT-TEM`, and the single-file legacy form of `SAM` (whose
  active-corpus replacement is a two-volume split of uncertain exact
  correspondence to kb3's original citations).
- **1** confirmed deleted from disk entirely, with no live copy anywhere
  except orphaned chunks in the old root `kb/store.sqlite`:
  `udayesvara-temple-art-architecture.md`.
- **1** source (`RAJM`, the Rājamārtaṇḍa-vṛtti) was found during this
  rebuild to be entirely absent from the original CSV catalogue —
  discovered only because kb3's own records mentioned it; it has no
  catalogue-equivalent entry anywhere.
- **2** sources (`Art of Paramaras.md`, `Inscriptions Corpus.md`) carry no
  kb3 code at all because they were added to the active corpus after kb3's
  2026-09-24 build; both received first-pass treatment in this rebuild, and
  both ultimately turned out to carry genuine, previously-uncaptured
  evidence (Part D.5, D's `Art of Paramaras.md` entry) — `Inscriptions
  Corpus.md` found via live retrieval, `Art of Paramaras.md` only after a
  direct keyword search of the raw file, since vector retrieval did not
  surface its content reliably even when queried directly.

### F.2 Chapter-level numbers

- **13 of 13** chapters (Ch1–Ch12 + Afterword) have a built dossier in
  Part C. All thirteen required executing or confirming the chapter-split
  logic in Part A.5; three required an actual content split, not just a
  relabeling (Ch1/Ch3, Ch3/Ch4, Ch11/Afterword).
- **Live retrieval queries run across all chapters: approximately 60**
  (5–8 per chapter, varying by how much a given chapter's genuine Udaypur-
  specific evidence base turned out to need beyond kb3's prior sample).
- **No fixed excerpt count was applied anywhere in Part C.** Per-chapter
  evidence-item counts range from 4 (Ch10) to 12 (Ch4), reflecting how much
  genuinely on-topic material each chapter's actual subject supported —
  not a quota.
- **Chapters with substantial, novel findings beyond kb3's prior
  coverage:** Ch1 (the foundation inscription itself), Ch4 (the entire
  `Inscriptions Corpus.md` discovery), Ch6 (the serpentine-inscription
  purpose dispute), Ch9 (the third founding legend), Ch10 (the Jayasimha
  III/post-1305 Udaypur-specific inscription), Ch11 (the Udayasāmudra
  tension), Afterword (a fully source-grounded recommendations list).
- **Chapter with the thinnest direct-Udaypur evidence base:** Ch8
  (Religion and Material Life) — reported as a finding about the corpus's
  actual coverage (Ch8.6), not papered over with regional or generic
  material relabelled as local.

### F.3 Sources and chapter-pairings not adequately examined

Per the Part E matrix:

- `Art of Paramaras.md` — this was the clearest single gap in an earlier
  revision of this rebuild (fully indexed, catalogue-resolved, but never
  cited by any chapter's search queries). **Resolved**: a direct keyword
  search of the raw file found two dedicated Hindi-language articles,
  now cited in Ch4, Ch5, and Ch10 (Part D, Part E). The general lesson
  remains live for other sources, though: live vector retrieval did not
  surface this file reliably even when queried directly with Udaypur-
  specific terms, so "not adequately examined via retrieval" and "no
  relevant material exists" are not the same conclusion, and a source
  this document's own matrix marks `N` may still reward a direct read.
- `GUP` (Gupte's iconographic handbook) — not adequately examined in any
  chapter, despite obvious relevance to Ch5's sculptural-programme
  discussion.
- `HAR`, `DEV`, `KRAM-1`, `KRAM-2` (the national comparative-architecture
  sources) — seen only via retrieval snippets or brief mentions in Ch3/Ch5,
  never read in full; their comparative value to Ch5 specifically is
  likely under-realized.
- `BHJ-H` (भोजदेव) — appeared heavily in kb3's prior excerpts for Ch4/Ch6/
  Ch8 but was never independently re-read in this rebuild; every citation
  involving it here is flagged as a carried-forward gap, not an
  independent verification.
- `PAR` (Venziya) — confirmed as a real, DOI-matched source in Phase B1
  and directly used for Ch4's Upendra-succession fact, but its "Fall of
  Parmar Dynasty" section (seen in a Ch10 retrieval snippet) was never
  read in full.

### F.4 Known retrieval, OCR, metadata, and citation limitations

- **Page-number provenance remains unconfirmed project-wide.** Every "OCR
  p.N" citation in this document refers to a `<!-- page N -->` marker
  inserted during OCR, not a confirmed printed page number. This caveat,
  first raised in Phase A, applies to every single citation in Part C and
  is not repeated chapter by chapter beyond the handful of explicit
  flags already in the text.
- **One file's page markers use a non-standard format** (`The Udayesvara
  Temple - Anupa Pande.md` uses `<!-- page N src=....jpg -->` rather than
  the plain `<!-- page N -->` most files use), which caused this file's
  chunk metadata to report `page_start: None` in live retrieval results;
  page numbers for this source were instead recovered by direct file
  inspection throughout Ch5/Ch7/Ch12.
- **`Jagta_Hua_Kasba_EN.md`'s page metadata does not resolve to simple
  integers at all** — every citation to this file in this document omits a
  page number and cites by heading/section only, flagged explicitly where
  it first mattered (Ch9).
- **Some source files contain extremely long, single-line passages** that
  this rebuild's search tooling truncated during live grepping (marked
  "[Omitted long context line]" in raw search output) — this affected
  `Jagta_Hua_Kasba_EN.md`'s Tughlaq-inscription passage specifically
  (Ch10), where the quoted material is accurate but the surrounding
  context was not fully legible to this pass's tools.
- **One unresolved internal date inconsistency**: Ganguly's cited Udaypur
  temple inscription for Jayasimha III gives "Sam. 1366=1909 A.D." (Ch10,
  CH10-E03), where Samvat 1366 would ordinarily correspond to approximately
  1309–10 A.D. This was flagged, not silently corrected, since the
  underlying 1933 source was not independently re-checked against this
  specific figure.

### F.5 Unresolved contradictions and open questions, collected

(Full detail in each chapter's own §5/§6; collected here for visibility.)

1. Udayāditya's exact accession date (Ch4, Ch5).
2. Udayāditya's exact kinship to Bhoja — *bandhu*/*bhrātā*/*pitṛvya*, and
   Trivedi's explicit rejection of a rival genealogy (Ch4).
3. Whether Jagaddēva and Lakṣmadeva are the same person — a named
   disagreement between Trivedi and Ganguly (Ch4).
4. Whether the serpentine-letter diagrams were pedagogical or dynastic-
   ritual devices — a named disagreement between Singh (2023) and
   Trivedi (1978)/Pollock (2006) (Ch6).
5. Whether Udayasāmudra is traceable today — Ganguly (1933, no) vs. a
   2020s INTACH field measurement reported by Tiwari (yes, to something)
   (Ch9, Ch11).
6. Whether the Chandragupta-Maurya "fire at Vidisha" attribution is
   historical — explicitly left open by the Gazetteer itself (Ch3).
7. Three unreconciled founding legends for Udaypur, none corroborating the
   others (Ch1, Ch9).

None of these have been adjudicated by this document. Each is presented
with its primary evidence and left open, per the master prompt's own
instruction not to silently reconcile disagreeing sources.

### F.6 Confirmation of process constraints honored throughout

- **No fixed excerpt cap was used in any chapter** — verified by the
  variable per-chapter evidence-item counts in F.2.
- **The vector database was not rebuilt, wiped, or re-embedded** at any
  point in this rebuild — every live-retrieval call in this document used
  the existing `udaypur_corpus_openai_large` collection read-only.
- **No file outside this document, its checklist, and its one backup copy
  (`docs/legacy_kb3_sourcebook_2026-09-24.md`) was modified.** The source
  catalogue, manifest, corpus Markdown files, and all frozen evaluation
  benchmarks remain untouched.
- **No Git commit or push was made** at any point during this rebuild.

### F.7 Recommended next actions

1. ~~Search `Art of Paramaras.md` directly for Ch4/Ch5/Ch10~~ — **done**:
   see Ch4.3 (CH4-E11/E12), Ch5.3 (CH5-E09–E15), and Ch10.3 (CH10-E05).
2. Read `GUP`, `HAR`, `DEV`, `KRAM-1`, `KRAM-2` in fuller context for Ch5
   specifically, rather than relying on retrieval snippets.
3. Independently re-read `BHJ-H` for Ch4/Ch6/Ch8's carried-forward claims.
4. Resolve, or explicitly accept as permanently open, the seven items in
   F.5 before any chapter is drafted into publishable prose.
5. If `Bhoja Paramara and His Times` (`SIN-B`) is ever added to the active
   corpus, re-examine the one claim (Udayāditya as Bhoja's "nephew") that
   currently rests on it alone and unindexed.
6. Decide, per the still-unresolved Part B.6 questions, whether
   `Bhoja Paramara and His Times` and the Hindi `Jagta Hua Kasba` original
   should be added to the active corpus and ingested — several citations
   in Ch1, Ch4, Ch9, and Ch12 are currently carried forward from kb3's
   prior excerpts of material this rebuild could not independently
   re-verify for exactly this reason.
