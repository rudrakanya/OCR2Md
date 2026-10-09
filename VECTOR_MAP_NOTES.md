# What the v2 vector map shows

**Map:** `VECTOR_MAP.html` — self-contained, offline, no external requests
**Collection:** `udaypur_kb_v2_openai` · 10,324 chunks · `text-embedding-3-large` at 1536-d
**Measurements:** `kb_audit/vector_map_v2_openai.json` · probes: `kb_audit/phase4_probe.json`
**Date:** 2026-10-07 (regenerated after near-duplicate collapse)

## Read this first: a projection is not evidence

The map reduces 1,536 dimensions to two. Distances in it are approximate, and a
cluster that looks tight may not be. **Every claim below is measured on the real
vectors, not read off the picture** — the usual test is k-nearest-neighbour
purity at k=15: of a chunk's fifteen true nearest neighbours, what share carry
the same label. The map is the lens that makes those numbers legible; it is not
the proof. Treat it as a way to form questions, then check them against the
store, exactly as the audit did.

## How it was built, and why

Chroma ships no offline explorer, so the projection is built locally:
cosine-normalised vectors → PCA to 50 components (explaining 53.6% of variance)
→ UMAP (`n_neighbors=15`, `min_dist=0.12`, cosine). The PCA step is not
cosmetic: UMAP on raw 1,536-d needs more memory than this machine has spare, and
reducing first is standard practice. Nothing was sent anywhere; `umap-learn`
and `scikit-learn` were installed locally for this.

The page colours and filters by **source code, source type, epistemic status,
chapter bucket, is_quotable, and script**, has a text search, and shows the full
metadata plus a text excerpt on hover. Devanagari and IAST render from system
fonts (`Nirmala UI` / `Noto Sans Devanagari`), with no webfont fetch.

---

## 1. Language asymmetry — measured, then fixed

**The embedding space does cluster by language. The retrieval consequence has
since been fixed query-side; both halves are below.**

| Measure | Value |
|---|---|
| Devanagari chunks | 1,894 of 10,324 (18.3%) |
| A Devanagari chunk's 15 nearest neighbours that are also Devanagari | **86.6%** |
| Base rate if neighbours were random | **18.3%** |
| Over-representation | **4.8×** |
| Latin chunks whose neighbours are Latin | 97.9% (base rate 81.7%) |

On the map, switch **Colour by → script**. The Devanagari chunks form their own
territory. They are not scattered among the English chunks that discuss the same
subjects; they sit together, because the model places them by language first and
topic second.

### What that cost in retrieval

In the **top 8** of twelve English questions, v1 returned none of the four
Devanagari sources and v2 returned only BHJ-H (3 of 96 slots).

**A correction to how that was first reported.** Those were top-8 figures, and
they were described as the sources being *unreachable*. At full depth they were
always present — RAJM at rank 73, TIW-H at 166, BHJ-H at 30. The defect was
never reachability; it was that they ranked far below anything a drafter sees.
The distinction matters because it points at the real fix: re-ranking, not
re-indexing.

### Verdict for Step 4 — settled by a controlled experiment

Both v2 collections held the **identical chunk set** (10,559 at the time of the
experiment; 10,324 after the near-duplicate collapse in §4b), differing only in
the embedding model. So the model effect and the query effect separate cleanly.
Rank of the target Devanagari source, full depth:

| | local e5, no bilingual | **local e5 + bilingual** | OpenAI, no bilingual | **OpenAI + bilingual** |
|---|---|---|---|---|
| target in top-8 (of 6 queries) | 1 | **4** | 1 | **4** |

**The bilingual query fixed the asymmetry. The model upgrade did not.** With
bilingual on, the free local model matches OpenAI on this measure and ranks RAJM
*first* for the yoga-sūtra query where OpenAI ranks it third.

That does not make the OpenAI embed a waste — it means it bought something else.
On ordinary **English** questions over the same chunks, counting hits from the
source that should answer each:

| | local e5 | OpenAI 3-large |
|---|---|---|
| expected-source hits in top-8, over 8 questions (64 slots) | **29** | **49** |

Two cases carry it: *"the mosque built behind the temple"* goes 0/8 → 6/8, and
*"Paramāra dynasty genealogy"* 1/8 → 6/8.

**So: keep OpenAI for general retrieval quality, and credit the bilingual query
for the Devanagari fix.** The ~$0.60 was worth spending; it was simply pitched at
the wrong problem, and anyone expecting the model alone to reach the Hindi and
Sanskrit sources should not plan on it.

The cause is structural, not a model defect: 82% of the corpus is Latin-script,
so an English query's nearest neighbours are overwhelmingly English chunks however
good the multilingual alignment is.

### What was built, and what it achieved

Bilingual querying is now implemented in **both** retrieval paths — the vector
path (`kb3_chroma_query`) and the lexical BM25 path (`kb3_query`) — in
`bilingual.py`. Each query is also issued in the other script, generated at query
time by `gpt-4.1-nano` and cached on disk, and the two candidate sets are merged.

**Rank of the target source, before → after, at full depth:**

| Target | Query | vector path | BM25 path |
|---|---|---|---|
| **RAJM** | yoga sutra commentary attributed to Bhoja | 73 → **3** | 144 → **1** |
| **RAJM** | Bhoja's own writings and authorship | absent → **31** | absent → **26** |
| **RAJM** | the Rājamārtaṇḍa commentary on the Yogasūtra | 5 → **1** | — |
| BHJ-H | life of king Bhojadeva of Dhara | 30 → **5** | 13 → **2** |
| TIW-H | present-day life in Udaypur town | 166 → **2** | absent → **2** |
| SAM | canonical proportions for temple construction | 26 → **9** | — |

English-on-English retrieval is unchanged (C2, C3 and C7 return identical lists).

**One design detail that decided whether this worked at all.** Each query's
similarities are normalised *within that query* before the two sets are compared.
Raw cosines from different queries are not on a shared scale — the Hindi form's
best match scored 0.573 where the English form's best was 0.594 — so a naive
`max()` demoted every Devanagari chunk and the first implementation changed
nothing (1/6 → 1/6 at top-8). With per-query normalisation it is 1/6 → 4/6. The
same error and the same fix apply to BM25 scores on the lexical path.

**Cost:** ~$0.000016 per distinct query for the translation plus ~$0.000003 for
the second embedding, then free from cache — about **$0.00002 per new query**.

A further re-embed would be the wrong lever: 3-large is already the stronger
multilingual model and on its own it moved this by three slots in ninety-six.

---

## 2. Quarantine, visually confirmed

| Check | Result |
|---|---|
| Chunks carrying an ADH fabrication marker (`rāhīna`, `Island \| Attribution`) | **0** |
| `ai-derived` chunks | **0** |
| Chunks flagged `is_archived` | **0** |

There is no island of fabricated or archived material on the map because none of
it is in the collection. In v2 the quarantine is a **separate file**
(`kb_quarantine_v2.sqlite`, 462 chunks) whose contents are embedded into a
separate collection (`udaypur_kb_v2_openai_archive`, 371 records), so the
plotted space cannot contain them by construction — stronger than v1, where the
50 fabricated rows sat in the active store behind a flag.

Colour by **is_quotable** to see the remaining non-quotable material: these are
the AI-reworded gazetteer and Samarāṅgaṇa chunks and the unclassified front
matter, retained as context but never quotable.

---

## 3. Source domination — one book swamps every chapter

**The space is organised by book, not by topic.** Source purity is **80.4%**:
four out of five of a chunk's nearest neighbours come from the same volume.

Per chapter bucket, the largest source's share:

| Bucket | Chunks | Top source | Share | Distinct sources |
|---|---|---|---|---|
| AF | 2,217 | **SAM** | **38%** | 22 |
| C11 | 2,501 | SAM | 34% | 23 |
| C2 | 2,596 | SAM | 33% | 23 |
| C12 | 2,951 | SAM | 31% | 24 |
| C3 | 2,931 | SAM | 30% | 22 |
| C15 | 2,550 | SAM | 30% | 23 |
| C16 | 2,142 | SAM | 28% | 24 |
| C8 | 3,559 | SAM | 26% | 24 |

**SAM (Samarāṅgaṇa-sūtradhāra) is the top source in every single bucket**, at
26–38%. It is the largest book in the corpus (1,210 chunks) and its chapter
priors are broad, so it is a plausible neighbour almost everywhere.

### A correction: this is bucket MEMBERSHIP, not what retrieval returns

SAM dominating every bucket is a statement about which chunks are *eligible* for
a chapter, not about what a query actually gets back. Measured directly:
**SAM is 0% of the top 200 for both C2 and C3**, because ranking already filters
it out once a well-formed question is asked. The earlier framing — that C2/C3
would be "written out of SAM" — overstated it, and the SAM-specific caps in
`kb3/retrieval.yaml` are a safeguard rather than a fix for an observed problem.

The over-representation that is real at retrieval time is a different source:
**INT-GEO took 18 of the top 20 for C3 (90%)**, and INT-ARC 61 of the top 200
for C2.

### The cap, and what it did

`kb3/retrieval.yaml` sets a per-chapter ceiling on any one source's share of a
chapter's candidates, applied on the full ranked list before truncation. Excess
chunks are **demoted to the tail, never removed**, so capped evidence stays
retrievable and citable.

| Chapter | Top source before | after | Distinct sources | Newly surfaced |
|---|---|---|---|---|
| **C3** | INT-GEO **90%** | **20%** | 2 → **6** | GAN, PAT, RAJ-E, TIW-E |
| C2 | BET-S 30% | 20% | 4 → **8** | GAN, GAZ-VID, PAT, TIW-E |
| C7 | PAN 80% | 45% (its own raised cap) | 4 → 6 | DEV, HAR |
| C6 | GAN 45% | 40% | 6 → 6 | — |

Nothing was lost: **20/20** chunks from each uncapped top-20 remain in the
capped candidate list. C7 and C6 carry deliberately higher ceilings (0.45, 0.40)
because their dominant sources genuinely are their subject.

Still worth knowing: SAM carries **272 `llm_regenerated` chunks**, the largest
block of AI-reworded text in the corpus, so its breadth of bucket membership and
its lowest-confidence text overlap.

On the map, colour by **source** and isolate SAM to see how far it reaches.

---

## 4. Chapter buckets are broad, not incoherent

Bucket purity is **41.1%** — of a chunk's fifteen nearest neighbours, about six
share its primary chapter. Against seventeen buckets with heavy multi-membership
(most chunks sit in several), that is reasonable rather than alarming: it says
the buckets are *topically broad*, which they are by design — C8 holds 3,565
chunks, a third of the corpus.

What it does mean: **a chapter bucket is not a topic cluster**, so bucket
membership alone is weak evidence that a chunk belongs in a section. The
section-level briefs should keep leaning on `rel_<chapter>` scores and the
cited-chunk discipline rather than on bucket membership.

---

## 4b. Near-duplicate text, and book indexes in the evidence pool

Exact-hash dedup could not see passages that re-chunking gave different
neighbours, so near-duplicates were measured with the project's own detector
(5-word shingles, 64-perm MinHash, 16 bands, then exact Jaccard):

| Jaccard band | pairs | within-source | cross-source |
|---|---|---|---|
| >= 0.95 | 538 | 538 | **0** |
| 0.80-0.95 | 1,361 | 1,361 | 0 |
| 0.50-0.80 | 861 | 861 | 0 |

**No corroboration was inflated.** Zero clusters span more than one work, and no
chunk cited a near-duplicate of itself as corroboration — the thing that would
actually corrupt the evidence base never happened. The 46 clusters at >= 0.95
were collapsed anyway (235 copies moved to the quarantine file, canonical keeps
a `near_duplicates_collapsed` provenance list); 0 of the 235 had more than 10%
of their shingles absent from their canonical, so nothing distinct was lost.

**What the duplication actually turned out to be:** book index pages. 219 of the
281 chunks in the >= 0.95 band are alphabetical index entries ("Abhanga 26-27,
30, 34-35...", "Vasu(s), 34, 41, 83..."), in consecutive near-identical windows
of the same index block.

That exposes a bigger issue than the duplication: **348 chunks (3.3% of v2) are
book index pages, and 152 of them are `claim_bearing = 1` with 140 sitting in at
least one chapter bucket.** Alphabetical index apparatus can therefore reach a
draft as evidence. 196 of the 348 are already inert (`v2-unclassified` +
`needs_recheck`); the other 152 are not. Concentrated in HAR (136), PAN (86),
KRAM-2 (77), DEV (19).

**Not acted on** — marking 348 chunks non-evidentiary is a judgement about what
counts as evidence, not a bug fix, so it is flagged for your decision. The
cheapest root-cause fix is a `md_clean` rule recognising index pages, which
would then apply to every future rebuild.

## 5. Honest limits of this map

- **PCA keeps 53.6% of variance.** Nearly half the structure is discarded before
  UMAP ever runs. Clusters are real but their shapes and separations are not.
- **UMAP distances are not metric.** Cluster *membership* is meaningful; the gap
  between two clusters is not a measure of anything.
- The purity numbers at k=15 are computed on the full vectors and are sound, but
  they are averages: a mean of 86.6% does not mean every Devanagari chunk is
  isolated, and the map will show mixed regions.
- `script` is assigned by a simple test (more than 20 Devanagari characters in
  the chunk), so a mostly-English chunk quoting a Sanskrit verse counts as
  Devanagari.
- One source, **SIN-S**, has only 14 chunks; its position on the map is not
  statistically meaningful.

## Artefacts

- `VECTOR_MAP.html` — the interactive map (3.4 MB, offline)
- `kb_audit/vector_map_v2_openai.json` — purity, domination and quarantine numbers
- `kb_audit/phase4_probe.json` — the per-query retrieval results behind §1
- `phase4_vector_map.py`, `phase4_probe.py` — both re-runnable
