# KB Audit — Stage 1A (existing knowledge base) and Stage 1B (classification)

**Date:** 2026-09-21 · **Scope:** `kb/store.sqlite` as it stands, and the 26 source files on disk in `Udaypur Reference Markdown Files/` · **Backup taken before any change:** `kb/store.sqlite.bak-20260917-133105`

**Status: Stage 1 complete. Paused for your review. Stage 2 has not been started.**

**Verdict: rebuild.** The source text is worth keeping. Everything built on top of it has to be rebuilt:
- the chunking
- the labels
- the provenance fields
- the chapter layer, which does not exist yet

For the metadata and scoring layer in your spec (dual dating, five scores, chapter vectors, corroboration clusters, quarantine), this is effectively a **first build**: none of it exists in the current store.

Stage 1 changed nothing in the store. It only wrote new files, listed in §9.

---

## 1. System map (what exists now)

| component | state |
|---|---|
| `kb/store.sqlite` → `chunks` | **10,754** chunks from 27 source names. Fixed ~1,800-char windows with 270-char overlap. |
| `chunks_fts` (FTS5, BM25) | Works. Four streams: raw, diacritic-folded, Devanagari, entities. It is the **only working retrieval path** (`kb_query.py`). |
| Dense vectors (`embeddings.npy`, mistral-embed) | **Dead.** Covers 9,467 chunks, not 10,754. The Mistral client and quota are gone, so queries cannot be embedded. `retrieve.py`, `build_kb.py` and `src/query.py` are broken for the same reason. |
| `chunks.jsonl` / meta stamp | Say 9,467. The store says 10,754. Three artifacts disagree about how big the KB is. |
| `chunk_labels` | `evidence_role` ∈ primary_witness / observation / interpretation / restatement / apparatus, plus period, quality and issues. **0 of 10,754 human-reviewed.** 1,287 chunks have no label at all. |
| `claims` table | **0 rows.** No claim layer exists. |
| Source dossiers | 18 of 27. |
| Chapter layer | **None.** 0 chunks bucketed to any chapter. |
| Entities | Alias map for places and people. `E:PLC:001` deliberately excludes bare "Udaipur" (see D9). |

Composition of the old store by the new `source_type` taxonomy (mapping in `kb_audit/source_registry.yaml`):

| source_type | old-store chunks |
|---|--:|
| secondary_scholarship | 4,828 |
| primary | 1,880 |
| reference_tertiary | 1,851 |
| field_observation | 1,107 |
| contextual_background | 1,063 (all Temple_Economics) |
| not in registry (orphan) | 25 |

The old store has no `epistemic_status` field. Its nearest equivalent, `evidence_role`, mixes up *what kind of source* a chunk comes from with *what kind of claim* it makes (D3). The new status tallies are in §7.

## 2. Defects, with tallies and examples

**D1. Overlap stores claims twice.** 62.5% of adjacent chunk pairs (6,705 of 10,727) share their overlap text. Any claim near a boundary exists twice, so a naive corroboration count double-counts it.

**D2. Chunks cut mid-claim.** 12.0% of chunks start mid-sentence (1,287) and 27.5% end without terminal punctuation.
- 673 of the mid-sentence starts come from `kb_append_lexical.py`, which I wrote in an earlier session to add the three missing books. That is my defect, and I'm reporting it with the rest.
- Chunk length: p05 262, median 1,252, max 1,799.

**D3. Source reliability and claim type are conflated.**
- `primary_witness` is applied to 2,360 chunks, many of them secondary scholarship restating a primary text.
- Example: #7891 is labelled a primary witness, but it is an AI-generated glossary.
- Your principle to rate the source and the claim separately is not implemented anywhere.

**D4. Speculation filed as fact.** 143 chunks labelled primary_witness or observation contain an epistemic hedge. I adjudicated 10 by hand: 9 are genuine, so roughly 129 in total.
- Most are anchored inference mislabelled as witness: Ganguly #7310, #7364, #7453–4; Temples_of_India #3564–5; Adhikari #2357, #2385, #2466.
- The dangerous kind cannot be caught by a word list because it contains no hedge. Example: Intach #961, "Before the 6 century BCE, Lord Shiva … worshipped outside the Human settlement only". It has zero corroboration, is stated as fact, and is labelled `restatement`. The same chunk also carries a genuine sculpture observation.
- The earlier "hedge-dominant" flag (144 chunks) is 94% false positives. 135 of them are śāstra deontics ("the width *may be* six digits"), which prescribe rather than doubt.

**D5. AI-regenerated text passes as transcription.** `[cite: N]` markers show text restated by a model, not OCR'd:

| source | affected chunks | markers |
|---|--:|--:|
| gazetteer | 185 of 508 (36%) | 815 |
| samarangana | 218 of 1,220 (18%) | 936 |
| patil-composite-inscriptions | 5 | 37 |

Quotation from these chunks is unsafe until checked against page images.

**D6. OCR-model commentary treated as source text.** 164 chunks contain chatter such as "The OCR has hallucinated text…": Gupte 77, Kramrisch I 51, JHK_EN 16, Rajpurohit 16, Pande 3, Skanda 1. One chatter chunk (#4473, Kramrisch) has **72 near-copies**, which is why it is the top duplicate target.

**D7. Orphans.** 25 chunks from `udayesvara-temple-art-architecture.md` (the Pande summary). The file has been deleted from disk, but its chunks are still retrievable, and one ranks **#1** for the C7 query. *Needs your decision:* restore it with `git checkout -- "Udaypur Reference Markdown Files/udayesvara-temple-art-architecture.md"`, or leave it deleted and quarantine the 25 chunks in Stage 2.

**D8. Undated and uncitable chunks.**
- 61% (6,528) carry no event date.
- 88% have a null `page_start`, so a claim cannot be cited to a page.
- There is no publication date or `date_confidence` on any chunk. Book-level dates now live in the registry.

**D9. A spelling defect hides Tiwari's book.** *Jagta Hua Kasba* spells the town "Udaipur" in 250 of its 348 chunks and never "Udaypur". The place entity excludes bare "Udaipur", correctly, to keep Udaipur (Rajasthan) out.
- Query "… Udaypur": 0 Tiwari chunks in the top 8.
- Query "… Udaipur": 7 of 8.
- Your main source for C13 and C16 is effectively invisible to the book's own spelling.
- Fix in Stage 2: a source-scoped alias (for `tiwari-jhk-*` only, "Udaipur" = E:PLC:001).

**D10. Irrelevant material retrievable by default.**
- 117 apparatus chunks (index, TOC, bibliography). Example: Hardy INDEX #699.
- All 1,063 Temple_Economics chunks. Two of them took top-3 slots for the C15 query.

**D11. Duplicates and the honest source count.**
- 563 chunks are flagged as near-duplicates, clustering on 153 targets. Most are OCR-chatter copies.
- Cross-source near-duplicate pairs: 159.

| source pair | near-dup pairs | note |
|---|--:|---|
| Patil 1952 ↔ composite *Temples* | 117 | |
| composite *Inscriptions* ↔ *Temples* | 13 | |
| Patil 1952 ↔ *Inscriptions* | 8 | |
| Kramrisch I ↔ Gupte | 6 | all OCR chatter |
| Pande full ↔ summary | 2 | |
| **Kramrisch I ↔ II** | **0** | Textually distinct, contrary to the spec's expectation. They share a work_id for authorship, not because text is repeated. |
| Tiwari EN ↔ HI | not measured | Translation cannot be detected lexically; the pairing is declared in the registry instead. |

**D12. The store is internally inconsistent.** As listed in §1:
- 10,754 chunks vs 9,467 vectors, labels and dossier coverage
- 0 claims
- 0 reviewed labels

## 3. Sampled fact-checks (12)

| chunk | source (type) | what it is | status reasoning | corroboration / contradiction | action |
|---|---|---|---|---|---|
| #7891 | samarangana (primary) | AI-written glossary, `[cite:]` | not a witness at all | n/a | flag llm_regenerated; not quotable |
| #10456 | Skanda XIII (primary), pp. 210–11 | mythic narrative | factual *within a scriptural register* | n/a | tag scriptural_register |
| #9654 | Geo-Heritage (field), p. 146 | legal-protection advocacy | opinion | n/a | tag opinion |
| #961 | Intach 2022 (field) | mixed: Shiva-worship claim + sculpture observation | claim is speculation stated as fact | 0 | split; flag claim |
| #1344 | Tiwari EN (field) | memoir (Dr Suresh Mishra's death) | observation | n/a | retain; low relevance |
| #7285 | Ganguly (SS) | Harsola grant VS 1005 = 949 CE, cites EI XIV p. 299 | factual, cited | "corroborated" by madhya-bharat #7056–9 (AI-regenerated) and Intach #807, but **all descend from one EI edition, so effectively 1 independent source** | count once |
| #9820 | Pande (SS) | quotes Beglar's Aurangzeb legend | folklore | **contradicted** by the Tughluq mosque inscriptions AH 737/739 (#7024, #7534, and Pande's own correction) | retain as folklore; attribution superseded |
| #699 | Hardy (SS) | index page | apparatus | n/a | non-claim |
| #8931 | serpentine paper (SS) | reference list | apparatus | n/a | non-claim |
| #9242 | gazetteer (ref.) | panchayat finance 1965–73 table | factual data, but labelled "observation" | n/a | relabel |
| #6839 | Patil (SS) | "maybe Yoginīs" plus evidence-backed argument | inference (old label "interpretation" is correct) | n/a | keep |
| #3417 | Temple_Economics (context) | Sabarimala | off-topic | n/a | contextual; exclude by default |

## 4. Retrieval and bucketing quality (chapter-scoped test queries, top 5)

| chapter | result |
|---|---|
| C3 Stones and Forests | **excellent**: all Geo-Heritage |
| C6 Udayāditya's Foundation | **good**: Patil #6914, Ganguly #7380 |
| C2 Betwa Valley | good, but apparatus/references #741 and #758 intrude |
| C8 Words in Stone | poor: Intach restatements and AI-regenerated madhya-bharat. The serpentine paper and Ganguly are both absent. |
| C7 Udayeśvara in Stone | poor: orphan summary at #1 and #5; Pande garbage chunk #9708 ("^{}[] enig^{}[]") at #4 |
| C9 Built Heritage | apparatus list #860 ranks top |
| C13 Stories | one good legend (#9481); rest off-target; **no Tiwari** (D9) |
| C14 Conquests and Regimes | Ganguly #7504 at rank 3; a TOC at rank 4 |
| C15 Archaeologists, Laws | Temple_Economics #3297 and #3296 in the top 3 |
| C16 Present Tense | Geo-Heritage/Intach only; **0 Tiwari** (D9) |

Seed-vocabulary coverage for the new chapter list (rough lexical counts of chunks and distinct sources, Temple_Economics excluded):

| chapter | chunks / sources | | chapter | chunks / sources |
|---|---|---|---|---|
| C1 | 764 / 22 | | C9 | 1,197 / 22 |
| C2 | 161 / 15 | | C10 | 442 / 22 |
| C3 | 365 / 22 | | C11 | 426 / 20 |
| C4 | 542 / 22 | | C12 | 351 / 20 |
| C5 | 1,892 / 23 | | C13 | 359 / 24 |
| C6 | 200 / 13 | | C14 | 373 / 20 |
| C7 | 982 / 21 | | C15 | 187 / 18 |
| C8 | 931 / 21 | | C16 | **60 / 4 (thinnest)** |
| | | | AF | 78 / 14 |

C16 is thin partly because of D9. Expect it to improve once the alias is fixed.

## 5. Stage 1B — what was built

**`kb_audit/source_registry.yaml`: book-level defaults.** Each of the 26 sources is declared once, openly: `source_type`, author (with confidence and basis), `publication_date` + `date_confidence` + `date_basis`, `observation_date` for field sources, `event_date` for primary texts, `register`, `work_id`, language, provenance notes.
- Type assignments:

| source_type | sources |
|---|---|
| primary | Skanda XIII, Samarāṅgaṇa |
| field_observation | both INTACH volumes, both Tiwari editions |
| reference_tertiary | Gupte, the three Patil files, Krishna Deva, gazetteer |
| contextual_background | Temple_Economics |
| secondary_scholarship | the rest |

- Duplicate clusters:
  - `tiwari-jhk`: EN is canonical for quotation, HI is kept for verification
  - `kramrisch-1946`: v1 + v2
  - `patil-1952`: 3 files
- Two items are excluded and listed as such: the deleted Pande summary, and the unconverted *Art of Paramaras.pdf* (its OCR run was killed at page 28 of 62 by memory pressure; not restarted).
- **Please check the registry first.** Every chunk inherits these fields, so a wrong date or type there is wrong 1,000 times.

**`stage1_classify.py`: deterministic, offline chunker and classifier.** No model calls.
- Chunks: paragraph- and sentence-aware, **no overlap**, never crosses a heading. Target ~900 chars, max 1,600.
- Tables, verse and apparatus are kept atomic, split only at line boundaries.
- A paragraph is split where it crosses from certain {factual, observation} to uncertain {inference, speculation} language. That happened 1,773 times.
- Page furniture, running headers, HTML comments, image references and OCR commentary are stripped before chunking. **Every removal is logged.**
- Each sentence is labelled from recorded cue phrases. The chunk status is then derived:
  - speculation if speculation is ≥ 1/3 of its characters
  - otherwise inference if speculation + inference is ≥ 1/3
  - otherwise the observation/factual majority
- A hedge anchored by citations or evidence nouns counts as inference.
- In a field source, a firsthand passage with no pre-modern history counts as observation.
- Folklore, opinion, prescriptive, llm_regenerated, secondhand_history and similar are **tags**, never statuses.
- Every chunk carries: file, heading trail, page range, char offsets, work_id, content hash and its cue phrases. `classification_log.jsonl` has the per-sentence decisions and the rule that fired.

## 6. Chunk geometry: old vs new

| | old store | new inventory |
|---|--:|--:|
| chunks | 10,754 | **19,158** (16,909 claim-bearing, 2,249 non-claim) |
| overlap between neighbours | 62.5% of pairs | **0** |
| median length | 1,252 | 426 |
| page-locatable | 12% | wherever the source markdown carries page markers (see limits) |

The new chunks are smaller because they now follow the claim, not a fixed window. Nine chunks exceed 1,700 characters because they are single unsplittable lines: bibliography run-ons and wide table rows.

## 7. Classification tally (claim-bearing chunks)

| source_type | factual | observation | inference | speculation | total |
|---|--:|--:|--:|--:|--:|
| primary | 2,134 | 1 | 50 | 8 | 2,193 |
| field_observation | 1,086 | 829 | 125 | 62 | 2,102 |
| secondary_scholarship | 6,860 | 2 | 792 | 266 | 7,920 |
| reference_tertiary | 2,417 | 0 | 124 | 62 | 2,603 |
| contextual_background | 1,892 | 3 | 146 | 50 | 2,091 |
| **all** | **14,389** | **835** | **1,237** | **448** | **16,909** |

Per-source tables, tag counts and pre-processing counts are in `kb_audit/classification_tally.md`. Pre-processing removed:
- 407 OCR-commentary lines: Gupte 152, Kramrisch I 100, Kramrisch II 97, Hardy 49, Pande 8, Geo-Heritage 1. Repeated chatter lines were also caught as running headers.
- 5,302 page-furniture lines (running headers, bare page numbers)
- 1,674 image references
- 22 HTML comments

## 8. How far to trust the classification (full detail in `kb_audit/classifier_validation.md`)

Measured against hand labels on a **held-out** sample of 36 that no rule was tuned on:

| predicted | precision | share of corpus |
|---|--:|--:|
| factual | 7/8 | 84% |
| observation | 6/9 | 6% |
| inference | 4/9 | 7% |
| **speculation** | **2/9** | 3% |

That is about **81% prevalence-weighted accuracy**. It is carried by the easy factual class. **The speculation and inference labels are candidate pools, not findings.** Most false speculation is actually anchored inference, where the anchor is the object being described or the preceding argument, which a word list cannot see. There is also perceptual "seem" in art-historical description.

The Hindi lexicon is thin, so the Tiwari pair should be classified from the English edition.

## 9. Files written by Stage 1

| file | what |
|---|---|
| `KB_AUDIT.md` | this report |
| `kb_audit/source_registry.yaml` | book-level provenance, type, dating, work clusters |
| `stage1_classify.py` | chunker + classifier (re-runnable, ~8 min) |
| `kb_audit/classified_inventory.jsonl` / `.csv` | every chunk: id, parent source, type, status, tags, provenance, cues, text (CSV omits text) |
| `kb_audit/classification_log.jsonl` | per-sentence labels, cues, rule fired, adjustments |
| `kb_audit/preprocessing_log.jsonl` | every stripped line (OCR chatter, headers, comments, images) |
| `kb_audit/classification_tally.md` | tallies |
| `kb_audit/classifier_validation.md`, `validation_gold_*.json`, `score_validation.py` | validation |
| `kb_audit/audit_log.jsonl` | run log (params, registry hash, counts, timings) |

## 10. Known limits of Stage 1

- Page numbers are only as good as the page markers in each markdown file. Several sources have none, so provenance falls back to heading trail + char offsets. That is still exact, but not a printed page.
- Chunk ids are ordinal (`{source_id}-{nnnnn}`) and change whenever the chunking changes. Use `content_hash` + source for stable references. I recommend Stage 2 freezes ids at build time.
- Cross-language duplicates (Tiwari EN/HI) and model-restated text are declared or tagged, not detected.
- The claim-level fact-checks in §3 are a sample of 12, not a census.

## 11. Decisions needed from you before Stage 2

1. **Review the registry** (`kb_audit/source_registry.yaml`), especially the dates marked inferred: Ganguly 1933, Tiwari c. 2021–22, Geo-Heritage ≥2024, Pande ≥2009, Temple_Economics ≥2024.
2. **Deleted Pande summary:** restore it, or quarantine its 25 orphan chunks?
3. **Speculation labels:** option A (adjudicate the ~1,700 uncertain candidates), B (accept them and let the credibility score carry the uncertainty) or C (another lexicon round). See the validation file.
4. **Chapter list mismatch:** `chapters.md` on disk still has the old 18-chapter list plus Afterword, and a `chapters.yaml` exists from the earlier pipeline. Stage 2 will write `chapters.yaml` for the new C1–C16 + AF list unless you say otherwise.
5. ***Art of Paramaras.pdf*:** resume the OCR? The script needs to be made resumable first; it currently writes only at the end, which is why the killed run left nothing.
6. **The spec was cut off** at "Relevance score for chunk `c` against chapter `k`:". §F's formula, the LOGGING section and anything after it did not arrive. Please re-send before Stage 2.
