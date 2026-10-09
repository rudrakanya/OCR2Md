# System Design v2 — Comprehensive RAG Pipeline

*Rebuild plan for the Udaypur / Paramāra book pipeline: hybrid retrieval, cross-encoder reranking, corpus comprehension, and a measured evaluation layer.*

Companion to `SYSTEM_DESIGN.md` (v1, 8 Aug 2026). This document proposes what changes, what stays, and in what order.

---

## 0. The framing argument

The v1 doc states its own governing principle:

> Anything the model could get wrong by guessing should be data instead.

v2 extends that principle one step further:

> **Anything the pipeline could get wrong by assuming should be measured instead.**

This matters for sequencing. You have asked for hybrid search, reranking, evaluation metrics, and deep text understanding. Three of those four are retrieval-quality interventions, and none of them can be justified — or tuned — without a measurement harness. Right now there is no way to answer "did hybrid search help?" except by reading chapters and forming an impression.

So the recommended order inverts the intuitive one. **The evaluation layer is built first, against the current pipeline, to establish a baseline.** Everything after that ships behind a measured improvement.

A second framing note, offered as honest pushback: complexity is not the objective. The v1 system is unusually well-designed for what it does, and several of its choices (flat `.npy` over a vector DB, bibliography as lookup table, provenance stamping) are correct and should survive untouched. The proposal below adds roughly 10 modules. Each one carries a **kill criterion** — a threshold below which the added complexity should be reverted rather than kept.

---

## 1. What v1 already gets right (do not rebuild)

| Keep | Why it survives v2 |
|---|---|
| `book_outline.py` as single source of truth | Every downstream artefact derives from it. Unchanged. |
| `sources.py` citation authority | Lookup table beats inference. v2 *extends* it, doesn't replace it. |
| Passage-ids → mechanical endnotes | The only citation scheme that is verifiable. Load-bearing for v2's verification gate. |
| Flat `.npy` + JSONL, no vector DB | 9,467 × 1024 is 39 MB. Still true. A DB would add ops burden, not capability. |
| Cleaning before embedding (`md_clean.py`) | Page furniture pollutes vectors, not just display. Correct layer. |
| Fingerprint-based idempotence | Extends cleanly to the new artefacts. |
| Incremental per-chapter writes | Long runs get longer in v2. This becomes more important, not less. |
| Source-diversity cap | Survives reranking; see §3.5. |
| IAST transliteration pass | Load-bearing for the sparse index too (§3.1). |

The v1 relevance floor (`ABS_FLOOR = 0.76`) is the one component that v2 genuinely breaks, and §3.4 explains how its guarantee is preserved by other means. That guarantee — *a sub-topic with no regional coverage must return nothing rather than eight passages about Thanjavur* — is the single most important property of the current retrieval layer and must not be lost in the rebuild.

---

## 2. Layer 1 — Corpus comprehension (the "deep understanding" layer)

This is the most substantial addition and, I'd argue, the highest-value one. The corpus is 24 sources and ~11 MB. That is small enough to **read every document in full with an LLM**, once, and store the understanding as data. Most RAG systems can't afford this. You can.

### 2.1 Source dossiers — `doc_understanding.py`

One pass per source, cached to `kb/_docs/<source>.json`, hand-editable, never silently regenerated (following the `blueprint.py` hierarchy-cache precedent).

Each dossier records:

```json
{
  "source": "cunningham-asi-reports-vol-x.md",
  "identity":   { "author", "title", "year", "publisher", "edition" },
  "kind":       "primary | secondary | tertiary",
  "genre":      "survey report | epigraphic corpus | temple monograph | Sanskrit śilpa text | gazetteer | conservation report",
  "coverage":   { "period_from", "period_to", "geography": [...], "monuments": [...] },
  "stance":     "colonial-era survey; attributions often superseded; measurements reliable",
  "reliability_notes": [...],
  "structure":  [ { "trail", "page_start", "page_end", "summary" } ],
  "summary":    "≤400 words, whole document",
  "key_claims": [ "claim_id", ... ],
  "caveats":    [ "OCR quality poor pp. 88–140", "plates not captured" ]
}
```

The `stance` and `reliability_notes` fields are not decoration. In a corpus mixing 19th-century ASI surveys, a Sanskrit śilpa treatise, modern epigraphy, and an INTACH conservation report, *who is asserting a thing* determines how it should be weighed and presented. Currently that judgement lives only in the drafting model's general knowledge, which is exactly the kind of thing the v1 principle says should be data.

**Feeds:** `sources.py` (auto-proposes the `(kind, contribution)` entries it currently holds by hand), `blueprint.py` (conflict adjudication gains a "which source is more authoritative here" axis), and the drafter's prompt.

### 2.2 Contextual chunk enrichment — `contextualize.py`

The known highest-leverage change to chunk quality. Before embedding, each chunk receives a 1–3 sentence situating preamble generated from the document summary, its section summary, and its heading trail:

> *From Cunningham's 1880 ASI report on the Bhilsa region, in the section describing the Udayeśvara temple's plan; this passage gives the measured dimensions of the maṇḍapa.*

The preamble is prepended at embed time only (the v1 heading-trail pattern — stored once, not twice), then dropped from what the drafter sees as evidence text.

**Critical constraint:** the preamble may only restate information already present in the dossier, the heading trail, or the chunk itself. It must never introduce a fact. Enforce with a post-generation check that every proper noun and numeral in the preamble appears in one of those three sources — reusing the machinery `unevidenced_terms()` already has. Otherwise you have introduced a fabrication vector *into the index itself*, which would be considerably worse than the problem it solves.

**Cost:** ~9,467 preambles. With document-level prompt caching, the marginal cost per chunk is small; the whole pass is roughly a single full read of the corpus plus generation. Budget one overnight run.

### 2.3 Entity registry — `entities.py`

A canonical entity table with alias resolution. This is, for *this* corpus specifically, probably the most useful single artefact in the whole plan.

```
entity_id | canonical (IAST) | type | aliases[]                                    | first_attested | notes
E:PLC:001 | Udayapura        | place | Udaypur, Udaipur (Vidisha), उदयपुर, Udayapura | 1059 CE       | not Udaipur, Rajasthan
E:PER:004 | Udayāditya       | person| Udayaditya, उदयादित्य, Udayāditya-deva        | c. 1059–1087  | Paramāra
E:MON:001 | Udayeśvara       | monument | Nīlakaṇṭheśvara, Udayesvara, नीलकण्ठेश्वर   | 1059–1080     | same structure
```

Types: person, dynasty, place, monument, inscription, text, deity, title, date-event.

This directly retires several v1 workarounds:

- `difflib` fuzzy matching at cutoff 0.86 in `unevidenced_terms()` becomes an exact lookup. The `Udayāditya's` / `Udayapur` / `Udaypur` false-flag problem disappears by construction rather than by threshold tuning.
- Diacritic folding and possessive stripping become alias-table entries, not heuristics.
- The `Udayeśvara` / `Nīlakaṇṭheśvara` identity — which a lexical matcher cannot know — becomes explicit.
- The Rajasthani-Udaipur disambiguation becomes enforceable.

Build by LLM extraction over the dossier pass, then **human curation**. For a scholarly manuscript this table is worth an afternoon of your attention; it is the closest thing the system will have to an authority file.

### 2.4 Claim store — `claims.py`

Extract structured claims into SQLite:

```sql
claims(claim_id, subject_entity, predicate, object, qualifiers_json,
       claim_type, source, page_start, page_end, chunk_id, confidence)
```

`claim_type ∈ {date_event, attribution, measurement, identification, interpretation, quotation}`.

This upgrades v1's conflict detection. The current 116 conflicts are found by numeric divergence across sources on the same sub-unit — a good heuristic that cannot distinguish *two sources disagreeing about the temple's completion date* from *two sources measuring different things*. Claim-typed conflicts can:

- group by `(subject_entity, predicate)` rather than by sub-unit proximity;
- separate genuine contradiction from apparent contradiction (different referents, different units, different eras);
- attach each side to its source's `reliability_notes` from §2.1, so the historian adjudicating gets a briefed decision rather than two bare numbers.

The output is still **candidates for judgement, not adjudications**. v1's limitation #3 is correct and stays correct; this just makes the candidate list better.

### 2.5 Optional: hierarchical summary nodes

RAPTOR-style: cluster chunks, summarize each cluster, embed the summaries as additional retrievable nodes. Helps sub-topics whose answer is diffuse ("the dynasty's architectural patronage as a whole") and which no single 1,800-character chunk can serve.

Deferred to Phase 5. It is the least certain win here and the §2.1–2.3 layers may already cover it via section summaries, which are retrievable at no extra cost.

---

## 3. Layer 2 — Hybrid retrieval and reranking

### 3.1 Sparse index — SQLite FTS5

Rather than adding a search dependency, use **SQLite FTS5**, which ships in the Python standard library and provides BM25 ranking via `bm25()`. This preserves the v1 "dependency-light, no infrastructure" principle exactly, and gives you a relational store for §2.3–2.4 in the same file.

The tokenizer is where the domain work is. Index each chunk under **four parallel token streams**:

1. raw text, lowercased;
2. **diacritic-folded** IAST (`Udayāditya` → `udayaditya`) — so a query typed without diacritics still matches;
3. Devanagari as-is, for the bilingual sources;
4. **alias-expanded entity mentions** from the registry — so a chunk saying `Nīlakaṇṭheśvara` is retrievable by `Udayeśvara`.

Stream 4 is the payoff for building §2.3. It gives exact-match recall on named entities that neither BM25 nor dense embedding can guarantee on its own, which for a manuscript organised around named persons, places, and monuments is most of what retrieval needs to do.

### 3.2 Dense index

Unchanged in mechanism; rebuilt over contextualized chunk text (§2.2). Same flat `.npy`, same L2-normalization, same cosine-as-dot-product.

Worth testing during Phase 2: whether a multilingual embedding model changes the status of `Jagta_Hua_Kasba_OCR_text.md`. v1 notes that this Hindi source is never retrieved and calls that correct, since its English translation stands in. With a multilingual embedder plus the sparse Devanagari stream, it becomes retrievable — and useful as *corroboration* of the translation rather than as a substitute for it. Whether that is desirable is an editorial call, not a technical one; flag it for a decision rather than assuming.

### 3.3 Fusion — `fusion.py`

Reciprocal Rank Fusion over three channels:

```
score(d) = Σ_channels  w_c / (k + rank_c(d)),   k = 60
```

Channels: dense (per query), BM25 (per query), entity-exact (per sub-topic, from the registry). RRF is rank-based, so it sidesteps the problem of normalizing a cosine similarity against a BM25 score — two quantities with no shared scale. Start with equal weights; tune `w_c` on the eval set (§4), not by intuition.

**Funnel shape** (per sub-topic, 5 queries as in v1):

```
5 queries × (dense top-30 + BM25 top-30)   →  ~250 hits
        + entity-exact channel             →  ~30 hits
        → dedupe → RRF                     →  ~120 unique candidates
        → cross-encoder rerank             →  120 scored
        → relevance floor on rerank score  →  variable
        → source-diversity cap             →  ≤ 50% per source, min 3
        → KEEP_PER_SUB                     →  8–12 passages
```

### 3.4 Preserving the "return nothing" guarantee

This is the migration's main risk. v1's `ABS_FLOOR = 0.76` is what stops a sub-topic with no regional coverage from receiving eight confidently-retrieved irrelevant passages. RRF produces rank-fused scores with no absolute meaning — an RRF score of 0.03 says nothing about whether the passage is relevant.

**The floor moves downstream to the reranker.** A cross-encoder outputs a calibrated relevance judgement for a (query, passage) pair, which is a strictly better signal than bi-encoder cosine for this purpose. So:

- `RERANK_FLOOR` — absolute cut on reranker score, **calibrated on the gold set** (§4), not guessed. This replaces `ABS_FLOOR`.
- `REL_MARGIN` — retained in spirit, applied to reranker scores.
- The `THIN_KEEP` / `THIN_SCORE` fallback is retained but should now *rarely fire*; if it fires as often as it does today, hybrid retrieval has not actually improved recall and that is a signal worth acting on.
- **An empty pack remains a valid, correct output.** It flows to `[GAP — not in sources]`, exactly as now.

Regression test this explicitly: keep a set of known-uncovered sub-topics in the eval suite and assert they return empty or near-empty. This is the one place where a metric improvement could mask a capability regression.

### 3.5 Reranking — `rerank.py`

Pluggable interface, one function: `rerank(query, passages) -> [(passage, score)]`.

| Option | Pros | Cons |
|---|---|---|
| **BGE-reranker-v2-m3 (local)** | No new API key; multilingual (handles Devanagari/IAST); free at your volume; reproducible | ~2 GB model; CPU inference; new heavyweight dependency (`torch`) |
| **Hosted reranker API** | No local dependency; strong quality | New vendor + key; per-call cost; network dependency in an otherwise-offline stage |
| **LLM listwise rerank (Mistral)** | Single vendor, no new key; can be prompt-instructed with domain criteria | Slower; costlier at 11k pairs/run; less calibrated scores; non-deterministic |

**Recommendation: local BGE-reranker-v2-m3 as default**, hosted as a config flag. Volume is ~93 sub-topics × 120 candidates ≈ 11k pairs per full run — minutes on CPU, and it keeps the retrieval stage offline and reproducible, which matters for the ablation harness. Multilingual capability is the deciding factor given the Sanskrit and Hindi content; verify it on IAST-heavy passages during Phase 1 before committing.

---

### 3.6 Metadata filtering

v1 achieves scoping through *anchored query variants* — pairing a sub-topic question with `Udayapur Vidisha`, `Betwa valley`, `Malwa Avanti`, `Paramara`. That works, but it is a soft steer: it biases the embedding, it doesn't constrain the candidate set.

The dossiers (§2.1) make hard filtering possible. Restrict the candidate pool before scoring by:

- `kind` — primary / secondary / tertiary, so a sub-unit that needs inscriptional evidence can retrieve only from primary sources;
- `period_from` / `period_to` — a chapter on 11th-century patronage should not surface 19th-century conservation material;
- `genre` — retrieve from the śilpa treatise only where architectural terminology is at issue;
- `source` — explicit include/exclude for a specific sub-topic.

Filtering composes with all three retrieval channels and costs nothing. It should be declarable per sub-topic in `book_outline.py`, alongside the existing `constraints` field, so scoping stays in the single source of truth rather than migrating into retrieval code.

### 3.7 Context assembly order

Long-context models attend unevenly, degrading toward the middle of a long prompt. The evidence pack is currently assembled in score order, which puts the second- and third-strongest passages exactly where attention is weakest.

Reorder the final pack so the highest-ranked passages sit at the **start and end**, weakest in the middle. This is a few lines of code with no cost and no downside, and it belongs in the ablation sweep (§4.4) like everything else — measure it, keep it if the faithfulness number moves.

---

## 4. Layer 3 — Evaluation (build this first)

### 4.1 The gold set — `eval/goldset.py`

There is no way around this: **RAG metrics without labels are self-referential.** An LLM judge scoring an LLM's retrieval against an LLM's notion of relevance measures agreement, not correctness.

Target 60–100 labelled items, drawn to mirror the outline's shape:

```json
{
  "id": "G-047",
  "chapter": 6,
  "subtopic": "economy-crafts",
  "question": "What evidence exists for craft specialisation at Udayapura?",
  "relevant_chunks": ["c:4471", "c:4472", "c:8810"],
  "reference_facts": [
    "Inscription of 1080 CE names a guild of stone-carvers",
    "Cunningham records mason's marks on the maṇḍapa piers"
  ],
  "expected_empty": false,
  "notes": "thin coverage; two sources only"
}
```

Bootstrap: LLM-generate candidate questions from chunks, then **human-verify every label**. Budget a working week. Include 10–15 `expected_empty: true` items — sub-topics you know the corpus does not cover — to test §3.4.

### 4.2 Retrieval metrics — `eval/eval_retrieval.py`

| Metric | Measures | Target direction |
|---|---|---|
| Recall@k (k = 10, 20, 50) | Did the funnel surface the relevant passages at all? | ↑ — the ceiling on everything downstream |
| nDCG@10 | Are they ranked well? | ↑ — the reranker's job |
| MRR | How deep is the first good hit? | ↑ |
| Context precision | Fraction of the delivered pack that is relevant | ↑ — noise degrades generation |
| Context recall | Fraction of reference facts covered by the pack | ↑ — the metric that predicts `[GAP]` rate |
| Empty-pack accuracy | On `expected_empty` items, did it correctly return nothing? | ↑ — the §3.4 guarantee |

### 4.3 Generation metrics — `eval/eval_generation.py`

| Metric | Method |
|---|---|
| **Faithfulness** | Decompose output into atomic claims; check each for entailment against the retrieved pack. The primary metric. |
| **Citation correctness** | Does the E-id attached to a sentence actually support that sentence? Verifiable mechanically, since citations resolve from passage IDs. |
| Citation completeness | Fraction of factual sentences carrying any citation |
| Answer relevance | Does the section address its sub-topic question? |
| Ungrounded-term rate | v1's existing check, retained as a cheap tripwire |

**Run cheap deterministic checks before expensive LLM judges.** Citation correctness, ungrounded terms, truncation, and repetition are all mechanical. Only faithfulness and relevance need a judge.

### 4.4 Ablation harness — `eval/ablate.py`

The module that makes the whole plan accountable. Runs the gold set across configurations:

```
dense-only (v1 baseline)
  + BM25 + RRF
  + entity channel
  + reranker
  + contextualized chunks
  + all
```

Report per-configuration metrics **with confidence intervals**. At n = 80 the noise is real; a 2-point nDCG difference is not a result. This is what turns "we added hybrid search" into "hybrid search moved Recall@20 from 0.71 to 0.84 ± 0.05."

### 4.5 Judge discipline

LLM judges drift and are position-biased. Fix the judge model and prompt version, record both in the results file, randomize candidate order, and re-run a held-out slice against human labels periodically to check the judge hasn't decoupled from ground truth.

---

## 5. Layer 4 — Verification gate (fixing limitation #2)

v1 states the problem precisely: *grounding is a report, not a gate*, and *nothing prevents* spontaneous fabrication. The Chapter 1 experiment — suppressing specific fabricated terms, only for different ones to appear and the ungrounded count to rise from 9 to 17 — is the clearest possible evidence that lexical suppression cannot work. You cannot enumerate what the model might invent.

The structural fix inverts the burden. Rather than blocking a denylist, require every assertion to carry a warrant.

### 5.1 Revised generation stages — `draft_chapter.py`

```
PLAN → DRAFT → STITCH → VERIFY → REPAIR* → CITE
                          ↑__________|  (max 2 iterations)
```

**VERIFY** — `verify.py`:
1. Decompose the drafted section into atomic claims (one assertion each).
2. For each claim, check entailment against the section's own evidence pack.
3. Classify: `supported` / `unsupported` / `contradicted` / `not-a-factual-claim`.
4. Every proper noun and numeral must trace to a passage in the pack.

**REPAIR** — a *constrained revision*, not a redraft. The flagged claims are fed back with instruction to remove or hedge each one specifically, and — importantly, learning from v1's stitch-budget finding — with a word budget tied to the input, since an unconstrained revision pass has already been observed to overshoot by 59% and invent comparanda while doing it. Re-verify after each iteration.

After two iterations, remaining unsupported claims are **cut and replaced with `[GAP — not in sources]`** rather than shipped. That is the gate.

### 5.2 Strictness as policy

`validate_book.py --strict` already exists as a flag. In v2, make it the default for assembly, with an explicit `--allow-ungrounded` escape hatch for work-in-progress. The current default — assemble regardless — is what lets a chapter that "cites correctly, reads well, and is still wrong" reach the manuscript.

Chapter 1, per v1's limitation #4, predates the current pipeline entirely and should be regenerated under v2 as the first real test of the gate.

### 5.3 Cross-chapter coherence — `coherence.py`

**This is a gap in v1 that the v2 plan as first drafted did not close, and it is arguably the most consequential one for a manuscript rather than a Q&A system.**

Nineteen chapters totalling ~148,000 words are drafted independently, four workers in parallel, each scoped to its own evidence brief. Nothing in the pipeline compares chapter 7 against chapter 12. The consequences are structural, not incidental:

- **Contradiction.** Two chapters can date the temple's completion differently, both correctly cited, because each retrieved a different source and neither knows the other exists. The claim store (§2.4) detects conflicts *within the corpus*; nothing detects conflicts *within the manuscript*.
- **Redundancy.** `validate_book.py`'s `rep` check catches ten-word phrases recurring across sections — within a chapter. The Paramāra genealogy or the temple's dating controversy can be explained from scratch in six chapters with no overlap in phrasing and no detection.
- **Broken reference chains.** A chapter can say "as discussed above" about material that ends up in a later chapter, or introduce a term the reader met three chapters ago as though it were new.
- **Voice drift.** Nineteen independent generation runs produce nineteen slightly different registers.

Proposed as a post-draft pass, after all chapters exist:

1. **Manuscript claim index.** Run §2.4 extraction over the *drafts* rather than the sources. Group by `(subject_entity, predicate)` across chapters. Divergence between two chapters on the same predicate is a manuscript contradiction, and unlike a source conflict it is not a matter for historical judgement — one of them is simply wrong, or they need explicit reconciliation in the text.
2. **Concept-introduction ledger.** First substantive treatment of each registry entity, by chapter and section. Flags: entities explained substantively in three or more chapters (redundancy), and entities used before their first explanation (forward dependency).
3. **Cross-reference resolution.** Every "as we saw", "discussed below", "the previous chapter" checked against the ledger and the outline order.
4. **Style exemplar set.** A small set of hand-approved passages in the target register, retrieved into each chapter's DRAFT prompt as voice anchors. This is the one idea that transfers cleanly from creative-writing RAG, where retrieving style samples is the entire point — the mechanism is identical, only the target register differs.

Steps 1–3 are reports for your review, not automated repairs. A redundancy the pipeline flags may be deliberate reinforcement; only you can tell. Step 4 is a generation-time change.

### 5.4 Config-driven variants

Every tunable in the plan — chunk size, `RERANK_FLOOR`, RRF weights, funnel widths, `KEEP_PER_SUB`, reranker choice, repair-loop iterations — should live in a single versioned config file, not scattered across module constants as in v1.

The ablation harness (§4.4) then sweeps configs rather than editing code, results record which config produced them, and the KB stamp folds in the config hash so a metrics run can never be silently attributed to the wrong settings.

The feature-flag / A/B-testing infrastructure that vendor tutorials propose for this — serving different pipeline variants to different user segments, monitoring cost per tier, rolling back a bad variant in production — solves a problem you do not have. This is a batch pipeline with one operator producing one manuscript. There are no user segments, no production traffic, and no rollback urgency. A config file plus the ablation harness gives you the entire benefit (compare variants, attribute results, revert cleanly) at none of the cost.

---

## 6. Module inventory

**New (~10 modules, est. 2,200–2,800 lines):**

| Module | Role | Est. lines |
|---|---|---|
| `doc_understanding.py` | Per-source dossiers: structure, summaries, stance | 380 |
| `entities.py` | Canonical entity registry + alias resolution | 290 |
| `claims.py` | Claim extraction, SQLite store, typed conflict detection | 340 |
| `contextualize.py` | Chunk situating preambles + no-new-facts check | 220 |
| `kb_store.py` | SQLite FTS5 sparse index; entity/claim tables | 310 |
| `fusion.py` | RRF across dense / sparse / entity channels | 180 |
| `rerank.py` | Pluggable cross-encoder | 200 |
| `verify.py` | Claim decomposition + entailment gate | 330 |
| `coherence.py` | Cross-chapter contradiction, redundancy, reference chains | 300 |
| `config.py` | Single versioned config; hashed into the KB stamp | 90 |
| `eval/goldset.py` | Gold set build + validation | 180 |
| `eval/eval_retrieval.py` | Retrieval metrics | 200 |
| `eval/eval_generation.py` | Faithfulness, citation, relevance | 260 |
| `eval/ablate.py` | Configuration sweep + CIs | 170 |

**Changed:**

| Module | Change |
|---|---|
| `build_kb.py` | Emits contextualized embeddings + FTS index; fingerprint extended to cover dossier and context versions |
| `kb_search.py` → `retrieve.py` | Full hybrid funnel; `kb_stamp()` folds in the new artefacts |
| `make_evidence.py` | Consumes reranked packs; `unevidenced_terms()` backed by the entity registry instead of `difflib` |
| `blueprint.py` | Conflicts sourced from the claim store; reference mapping gains dossier metadata |
| `draft_chapter.py` | VERIFY / REPAIR stages; dossier stance in prompt context |
| `validate_book.py` | Metrics replace heuristics; `--strict` becomes default |
| `sources.py` | Dossier-derived, human-confirmed; `unmapped()` retained |

**Unchanged:** `book_outline.py`, `query_gen.py`, `md_clean.py`, `add_translit.py`, `ocr_to_markdown.py`, `combine_blueprint.py`, `assemble_book.py`, `console.py`.

---

## 7. Phasing, with kill criteria

Each phase ships independently and is measured before the next begins.

| Phase | Ships | Measure | Kill criterion |
|---|---|---|---|
| **0. Instrumentation** | Gold set (80 items); retrieval + generation metrics; baseline run on v1 | Baseline Recall@20, nDCG@10, faithfulness, empty-pack accuracy | — (non-negotiable prerequisite) |
| **1. Hybrid + rerank** | FTS5 index, RRF, cross-encoder, `RERANK_FLOOR` calibration | Recall@20, nDCG@10, empty-pack accuracy | If nDCG@10 gains < 5 pts *or* empty-pack accuracy drops, revert to dense + `ABS_FLOOR` |
| **2. Comprehension** | Dossiers, contextual chunks, entity registry, entity channel | Recall@20, context precision, `unevidenced_terms` false-flag rate | If Recall@20 gains < 5 pts, keep the entity registry (it pays for itself in §5) and drop contextualization |
| **3. Claim store** | Extraction, typed conflicts, dossier-briefed adjudication | Conflict precision judged against a 30-item human-reviewed sample | If conflict precision doesn't beat the current numeric heuristic, keep entities and drop claims |
| **4. Verification gate** | VERIFY / REPAIR loop; strict-by-default assembly | Faithfulness; ungrounded terms per chapter; `[GAP]` rate | If ungrounded terms don't fall by half, the loop isn't working — investigate before shipping |
| **5. Coherence** | Manuscript claim index, concept ledger, cross-reference check, style exemplars | Contradictions and redundancies found across the 19 chapters, judged by review | If it surfaces nothing you didn't already know, drop it — but check the full manuscript once first |
| **6. Optional** | Hierarchical summary nodes; multilingual embedder decision | Recall@20 on diffuse sub-topics | Default to not building it |

Phase 4 is the phase that addresses the problem you actually have. Phases 1–3 are, in large part, in service of making Phase 4 possible: you cannot verify claims against an evidence pack that doesn't contain the relevant evidence.

---

## 8. Risks

**The gold set is the bottleneck and the least interesting work.** It is also the thing that makes every other number meaningful. If it gets skipped, this plan degrades into adding complexity on faith — which is the failure mode it exists to prevent.

**Contextual enrichment can inject fabrication into the index.** The §2.2 no-new-facts check is mandatory, not optional. A hallucinated preamble is worse than no preamble, because it is invisible at draft time and carries the index's authority.

**Reranker quality on IAST and Sanskrit is unverified.** BGE-m3 is multilingual, but "multilingual" rarely means "trained on transliterated Sanskrit epigraphy." Test on a 20-item IAST-heavy slice in Phase 1 before building on it.

**RRF discards calibration.** Covered in §3.4, but it bears repeating: the empty-pack guarantee is the property most likely to be silently lost, and the one whose loss would do the most damage to the manuscript.

**The entity registry needs human curation.** Auto-extraction will conflate `Udayapura` with `Udaipur`, and will not know that `Udayeśvara` and `Nīlakaṇṭheśvara` are one temple. Budget the review time.

**Verification is not infallible.** An entailment check can be fooled by a claim that is *supported in form* but subtly misattributed. The gate lowers the fabrication rate; it does not reach zero. `validate_book.py` remains the honest layer, and human review remains necessary.

**Rebuild cost.** Re-embedding 9,467 contextualized chunks plus one full comprehension pass over ~11 MB is roughly one overnight run and a modest one-off spend — but the fingerprint changes, so every downstream artefact (evidence briefs, blueprint, drafts) becomes stale simultaneously. Plan for a full regeneration at the end of Phase 2, not a piecemeal one.

---

## 9. Estimated shape

| | v1 | v2 |
|---|---|---|
| Modules | 15 | ~25 |
| Lines of Python | ~4,000 | ~7,000 |
| Storage | 39 MB `.npy` + JSONL | ~45 MB `.npy` + JSONL + ~60 MB SQLite |
| New dependencies | — | `torch` + `sentence-transformers` (reranker), `rank_bm25` optional; SQLite is stdlib |
| Retrieval channels | 1 | 3 + rerank |
| Grounding | measured post-hoc | measured, gated, repaired |
| Corpus knowledge | chunk-local | document-level dossiers + entity/claim graph |

---

## 10. Immediate next steps

1. **Write 20 gold-set items by hand** across three chapters with differing coverage density (one well-covered, one thin, one uncovered). Run them against the current pipeline. This takes a day and will tell you more about where v1 actually fails than any amount of further design.
2. **Build the entity registry stub** — persons, places, monuments, with aliases. This is useful immediately, independent of everything else, and retires the `difflib` heuristic.
3. **Decide the reranker.** Local vs hosted determines whether `torch` enters the dependency tree, which is the largest single change to the project's operational footprint.
4. Then build Phase 0 properly.

---

## Appendix A — Reference articles assessed

Three tutorials were supplied as complexity calibration: LaunchDarkly's *LLM RAG Tutorial* (Sep 2025), Pragati Rana's *Building a Reusable RAG-Based Automation Pipeline* (Medium, Feb 2026), and Nam Tran's *Build Your Own AI Story Generator with RAG, Part 1* (dev.to, Jan 2026).

**Assessment: all three describe systems substantially simpler than v1 already is.** The dev.to piece states outright that it uses basic similarity search with no reranking and single-query retrieval with no query expansion — v1 has query expansion, and its relevance floor is a more disciplined instrument than plain top-k. The Medium piece is a FAISS index over spreadsheet rows with one static prompt. The LaunchDarkly piece is the substantive one, and its "advanced techniques" section is the source of most of the requested feature list.

Component-by-component:

| Component named in the articles | Status |
|---|---|
| Load → chunk → embed → store → retrieve → generate | v1, more carefully (heading trails, page provenance, bilingual script separation) |
| Chunk overlap, sentence-boundary splitting | v1, with scholarly-abbreviation handling and daṇḍa support |
| Vector database (Pinecone / FAISS / ChromaDB) | v1 deliberately declines — 39 MB does not need one |
| Query refinement / expansion | v1 `query_gen.py`, anchored variants + LLM paraphrase |
| Hybrid retrieval (BM25 + semantic) | v2 §3.1–3.3 |
| Cross-encoder reranking | v2 §3.5 |
| Evaluation: Recall@k, MRR, context precision, faithfulness, hallucination rate | v2 §4.2–4.3 |
| Knowledge graph / GraphRAG | v2 §2.3–2.4, scoped to entities and claims |
| Agentic RAG: Planner / Retriever / Synthesizer / Verifier | v1 already implements all four as pipeline stages — see below |
| Metadata filtering | **New** → v2 §3.6 |
| "Lost in the middle" context reordering | **New** → v2 §3.7 |
| Multi-chapter consistency via summaries | **New** → v2 §5.3, the most valuable of the three |
| Feature flags / A/B testing / per-tier monitoring | Declined → v2 §5.4 (config file instead) |
| Real-time / streaming index updates | Not applicable — a fixed 24-source corpus |
| Caching, rate limiting, streaming responses, observability | Partly v1 (OCR cache, classified backoff); the rest is production-service concern, not batch-pipeline concern |

**On "agentic RAG."** The four-role framing — Planner, Retriever, Synthesizer, Verifier — maps onto v1 exactly: `blueprint.py` plans, `make_evidence.py` retrieves, `draft_chapter.py` synthesizes, `validate_book.py` verifies. The difference is that v1 wires them as a static pipeline rather than a dynamic agent loop, and for this workload that is the better choice: runs are resumable, artefacts are inspectable and hand-editable, costs are predictable, and the same inputs produce the same outputs. An agent loop would trade all of that for autonomy you do not need on a fixed corpus and a fixed outline. v2's only structural addition to the four roles is closing the Verifier's loop back into the Synthesizer (§5.1) — which is the one thing the static pipeline was actually missing.