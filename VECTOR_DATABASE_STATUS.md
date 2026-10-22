# Vector Database Status, Structure, Commands, and Metrics

Snapshot as of 2026-10-10, branch `work/rag-pipeline-isolation`. This
document covers the **`src/` ChromaDB pipeline** — the one actually in
active use. There is also an older, unrelated NumPy/JSONL knowledge base
under `./kb/` (built by the root-level `build_kb.py`); it is not covered
here except where noted for disambiguation.

---

## 1. Status at a glance

`./chroma_db/` (892 MB on disk) holds **five** collections. All were built
from the corpus at:

```
Udaipur Books Markdown files/        <- 26 source .md files
```

| Collection | Chunks | Embedding model | Dim | Purpose |
|---|---|---|---|---|
| `udaypur_corpus` | 3,623 | `BAAI/bge-m3` (local, sentence-transformers) | 1024 | Default-config build |
| `udaypur_corpus_bge_m3` | 3,623 | `BAAI/bge-m3` (local) | 1024 | Ablation variant, same model, kept for comparison |
| `udaypur_corpus_chunk500` | 6,504 | `BAAI/bge-m3` (local) | 1024 | Ablation: 500-token chunks |
| `udaypur_corpus_chunk1500` | 2,503 | `BAAI/bge-m3` (local) | 1024 | Ablation: 1500-token chunks |
| **`udaypur_corpus_openai_large`** | **5,862** | **`text-embedding-3-large` (OpenAI)** | **3072** | **Current production collection** |

**`udaypur_corpus_openai_large` is the one to use.** It is the only
collection stamped with its embedding model/dimension in Chroma's own
collection metadata (the other four predate that stamping and must be
treated as `bge-m3`/1024-dim by convention, not by metadata). All five are
confirmed independent and intact — nothing in this doc's history ever
deleted or merged any of them.

**Known limitation**: `config.yaml`'s own `embedding.model` default is
still `BAAI/bge-m3` / sentence-transformers. Every command below that
targets the OpenAI collection must pass `--embed-preset openai_large`
explicitly, or use `open_aligned()`'s auto-detection (query/evaluate do this
automatically; see §4).

---

## 2. Architecture

```
Udaipur Books Markdown files/*.md   (26 files, read-only source)
        │
        ▼
books_manifest.yaml                  bibliographic metadata, keyed by filename
chapters.yaml                        the 19-chapter outline (C01-C18, AW) for tagging
config.yaml                          single source of truth for chunking/embedding/retrieval tuning
        │
        ▼
src/ingest.py  ──►  src/chunker.py  ──►  src/embedder.py  ──►  src/store.py  ──►  chroma_db/
   (CLI entry)      (markdown-aware,      (sentence_transformers         (PersistentClient,
                     heading-based         or openai backend,             one collection per
                     splitting)            VectorCache for reuse)         embedding config)
        │
        ▼
src/tag.py      (chapter tagging, embedding-based, no LLM call)
src/query.py    (CLI: single-query retrieval)
src/retrieval.py (hybrid dense+BM25 RRF fusion, used by both query.py and evaluate.py)
src/evaluate.py  (book-level accuracy harness against eval/gold.yaml or a benchmark file)
src/reconcile.py (read-only stale-chunk diagnostic; --delete exists but is never auto-run)
```

Chunk IDs are **deterministic and positional**: `sha1(f"{source_path}:{chunk_index}")`.
Re-running ingest on unchanged input is a safe no-op (same IDs, upsert
overwrites identically). Editing, renaming, or deleting a source file
leaves its old chunks as **orphans** with no automatic cleanup — use
`src/reconcile.py` to detect this (see §5).

---

## 3. Directory and file structure

```
chroma_db/
├── chroma.sqlite3            Chroma's own vector/metadata store (shared by all 5 collections)
├── <uuid>/                   per-collection HNSW index segments (one dir per collection)
├── sidecar.sqlite3           text_folded + chunk bookkeeping for the default collection
├── sidecar_bge_m3.sqlite3    sidecar for the bge_m3 ablation variant
├── sidecar_chunk500.sqlite3  sidecar for the 500-token ablation variant
├── sidecar_chunk1500.sqlite3 sidecar for the 1500-token ablation variant
├── embed_cache.sqlite3       content-hash -> vector cache, SHARED across all models/presets
└── *.bm25.pkl                cached BM25 lexical index (one per sidecar, built lazily)

config.yaml                   chunking/embedding/retrieval/evaluation settings (single source of truth)
books_manifest.yaml           filename -> {title, author, year, kind, language, ...}
chapters.yaml                 the 19-chapter outline used for tagging

eval/
├── gold.yaml                 53-query book-level gold set — PROVISIONAL, FILENAME MISMATCHES (see §6)
├── benchmark_v1.yaml          30-query book-level benchmark, filenames verified against this collection
├── benchmark_v2.yaml          same 30 queries, 4 relevance fixes + duplicate-OCR/unanswerable policy notes
├── benchmark_v2_notes.md      change log and annotation policy for v2
├── benchmark_passages_v1.yaml 12-query PASSAGE-level benchmark (exact excerpts, not just book titles)
├── benchmark_passages_v2.yaml 15 more passage-level queries (short-fact / multi-source / control)
├── passage_metrics.py         Evidence Recall@k / reciprocal-rank implementation
├── run_passage_eval.py        dense-vs-hybrid runner for the passage benchmarks
├── audit_heading_sections.py  read-only audit: which headings get dropped as empty sections
├── validate_benchmark.py      offline validator (filenames exist, quotes verbatim, v1 unchanged)
├── test_*.py                  offline regression tests for all of the above
└── results/chroma/            timestamped JSON artifacts from every eval/ingest/tag run
```

---

## 4. Commands

All commands assume the working directory is the repo root and that
`OPENAI_API_KEY` is set in `.env` (confirmed present). Every command below
targets the **production collection** via two environment variables that
`src/settings.py` reads (both are a no-op if unset, defaulting to whatever
`config.yaml` says):

```bash
export CORPUS_DIR="Udaipur Books Markdown files"     # overrides config.yaml's project.corpus_dir
export COLLECTION="udaypur_corpus_openai_large"      # overrides config.yaml's storage.collection
```

### Query it (single question, from the CLI)

```bash
python -m src.query "your question here" --embed-preset openai_large --k 5
python -m src.query "your question" --embed-preset openai_large --chapter C08   # restrict to one chapter
python -m src.query "your question" --embed-preset openai_large --no-hybrid     # dense-only, for comparison
python -m src.query "your question" --embed-preset openai_large --json          # machine-readable
```

### View it (inspect collections, counts, metadata — read-only, no API call)

```python
import chromadb
from chromadb.config import Settings as ChromaSettings
client = chromadb.PersistentClient(path="chroma_db", settings=ChromaSettings(anonymized_telemetry=False))
for c in client.list_collections():
    col = client.get_collection(c.name)
    print(c.name, col.count(), col.metadata)
```

```bash
python -m src.report        # writes ./corpus_report.md — sourcing-gap report
python -m src.report --stdout
```

### Rebuild / re-ingest (⚠ changes the collection — see §7 for safety notes)

```bash
python -m src.ingest --embed-preset openai_large              # idempotent upsert, safe to re-run
python -m src.ingest --embed-preset openai_large --dry-run     # chunk + report only, no embedding, no cost
python -m src.ingest --embed-preset openai_large --rebuild     # deletes ONLY this collection + its own
                                                                 # sidecar first (scoped since Phase 6's fix;
                                                                 # sibling collections and the shared embed
                                                                 # cache are left untouched)
```

### Re-tag chapters (no re-embedding)

```bash
python -m src.tag
python -m src.tag --explain C08      # see exactly what matched chapter C08
```

### Diagnose stale/orphaned chunks (read-only by default)

```bash
python -m src.reconcile --embed-preset openai_large             # report only, no write
python -m src.reconcile --embed-preset openai_large --delete    # ⚠ actually removes stale ids — never
                                                                   # run this without reviewing the report first
```

### Audit the chunking pipeline for lost headings (fully read-only)

```bash
python eval/audit_heading_sections.py
python eval/audit_heading_sections.py --compare-collection   # also cross-checks against the live collection
```

---

## 5. Evaluation commands

### Book-level (Precision/Recall/MRR/nDCG against a list of expected source books)

```bash
# against the frozen, provisional 53-query gold set (46/53 have filename mismatches -- see §6)
python -m src.evaluate --compare

# against the corrected 30-query benchmark, with Phase 9's policy-aware aggregation
export GOLD_PATH="eval/benchmark_v2.yaml"
python -m src.evaluate --compare --policy-aware --worst 10
```

`--policy-aware` reports TWO extra tables beyond the legacy one: an
**eligible-only** aggregate (excludes queries marked `answerable: false` /
`exclude_from_aggregate: true` / lacking any relevance label) and a
**sensitivity** aggregate (also excludes `review_marker: uncertain`
queries). Without `--policy-aware`, a warning now prints automatically if
the legacy table silently folded in any such queries.

### Passage-level (does retrieval surface the exact supporting excerpt, not just the right book)

```bash
python eval/run_passage_eval.py --benchmark benchmark_passages_v1.yaml
python eval/run_passage_eval.py --benchmark benchmark_passages_v2.yaml
```

Reports Evidence Recall@3/5/10, reciprocal rank, a per-category breakdown
(`short_embedded_fact` / `multi_source` / `control_*`), and an
uncertain-label sensitivity view — for both dense-only and hybrid, on the
identical query set.

### Validate a benchmark file offline (no API call, no collection access)

```bash
python eval/validate_benchmark.py                 # checks benchmark_v2.yaml
python eval/test_passage_eval.py                  # checks both passage benchmarks + metric logic
python eval/test_evaluate_policy.py                # checks the policy-aware aggregation logic
python eval/test_audit_heading_sections.py         # checks the heading-audit logic
python test_pipeline.py                            # unrelated chapter_pipeline.py smoke test
```

---

## 6. Metrics used, and exactly what each one means

### Book-level metrics (`src/evaluate.py`)

| Metric | Definition | Caveat |
|---|---|---|
| **Precision@k** | fraction of the top-k hits whose `source_path` is in the query's `relevant_books` (or scores >0 via `graded`/`relevant_chunks`) | A chunk from the right book about the wrong subject still counts as a hit — this is a **book-level upper bound**, not passage accuracy. |
| **Recall@k (book-level)** | fraction of the *expected books* found anywhere in the top-k | Not true recall over all possible relevant chunks (unknowable by hand) — "did we find each expected book" instead. |
| **MRR** | 1/rank of the first hit with relevance > 0, averaged | |
| **nDCG@10** | standard nDCG using `graded` weights (0–3) where given, else binary | |
| **top-1 tagged expected / top-1 primary == expected** | does the #1 hit's chapter tag match the query's declared `chapter` | Tests the *tagging* pipeline, not retrieval quality per se. |

**Policy-aware correction (Phase 9)**: a query with `relevant_books: []`
(deliberately unanswerable) forces P/R/MRR/nDCG to exactly 0 under the
legacy formula — folding that into a mean silently understates quality on
the answerable subset. `partition_queries()` + `aggregate()` recompute the
same metrics over only the eligible subset; `None` (not a fabricated `0.0`)
is returned when nothing is eligible.

### Passage-level metrics (`eval/passage_metrics.py`)

| Metric | Definition |
|---|---|
| **Evidence Recall@k** | fraction of distinct **evidence groups** (not raw passages) found in the top-k. A duplicate-OCR pair of the same underlying fact is ONE group — finding either copy counts once, never twice. |
| **Reciprocal rank (first evidence)** | 1/rank of the first hit matching *any* evidence group |
| **Per-category breakdown** | the same two metrics computed separately for `short_embedded_fact`, `multi_source`, and `control_*` queries |

A hit "matches" an evidence group if the group's recorded `excerpt`
(whitespace-normalized) is a verbatim substring of `heading + "\n" + text`
for that hit — **both** fields are checked, because Chroma's stored
`document` is body text only; headings live in separate `heading_path`
metadata and are never duplicated into the body (confirmed by reading
`src/chunker.py`'s `Chunk` dataclass).

### A third answerability state unique to the passage benchmarks

| State | Meaning |
|---|---|
| `confirmed_answerable` | fact exists in the corpus AND is indexed |
| `confirmed_unanswerable` | fact does not exist anywhere in this corpus |
| **`confirmed_unindexed`** | fact exists in the raw `.md` file, read directly, but is **provably absent** from every chunk's text and metadata in the live collection (verified both via `audit_heading_sections.py` and a direct collection query) |

A retriever cannot be faulted for missing a `confirmed_unindexed` fact —
`run_passage_eval.py` excludes these from the main eligible mean, the same
way an unanswerable query is excluded.

---

## 7. Known limitations and open findings (as of this snapshot)

- **`eval/gold.yaml`** (the original 53-query set): 21/53 queries reference
  filenames that don't exist in this collection at all (always score
  recall=0 regardless of retrieval quality); 25/53 are partially valid. Only
  7/53 are fully trustworthy. Left untouched and documented, not repaired.
- **Measured baseline (book-level, `benchmark_v2.yaml`, 26 eligible
  queries)**: hybrid P@3=0.822, MRR=0.867 (all 30) / MRR=1.000 (26 eligible,
  excluding unanswerable traps).
- **Measured baseline (passage-level, 23 eligible queries across both
  passage benchmarks)**: substantially lower than the book-level numbers —
  confirms that finding the right *book* is much easier than finding the
  right *passage*. Hybrid EvR@10 ≈ 0.60–0.65 vs. dense ≈ 0.45–0.58.
- **Category-specific pattern** (now a 2-phase, repeated finding): hybrid
  clearly **wins** on `short_embedded_fact` queries (exact numbers/terms
  that dense embedding blurs, rescued by BM25) but **loses or ties** on
  `multi_source` queries (5 examples across two benchmarks; RRF fusion does
  not reliably surface two independent sources together). Not yet root-caused
  to a specific mechanism — recommended next step is a targeted diagnostic
  (does the second source rank low, or is it absent even at k=20+), not a
  retrieval-algorithm change.
- **Chunking coverage gap**: 495 headings corpus-wide are dropped as empty
  sections by `src/chunker.py`'s `split_sections()`; most are junk (page
  numbers, copyright lines), but at least one confirmed case
  (`"Mahārājādhirāja Śrī Bhojadeva Paramāra"`, duplicated across two files)
  is a real, citable identifier that is currently unindexed anywhere.
- **Duplicate-OCR sources exist** (e.g. three separate OCR passes of one
  Anupa Pande book under three filenames) — demoted at query time
  (`src/retrieval.py` halves a flagged duplicate's fused score), never
  merged or deleted; always treated as one piece of evidence, not
  independent corroboration, in every benchmark's annotation policy.

---

## 8. Quick-reference cheat sheet

```bash
# always set these first
export CORPUS_DIR="Udaipur Books Markdown files"
export COLLECTION="udaypur_corpus_openai_large"

python -m src.query "a question" --embed-preset openai_large --k 5     # ask it something
python -m src.evaluate --compare                                       # legacy book-level eval (gold.yaml)
GOLD_PATH=eval/benchmark_v2.yaml python -m src.evaluate --compare --policy-aware   # corrected eval
python eval/run_passage_eval.py --benchmark benchmark_passages_v2.yaml  # passage-level eval
python -m src.reconcile --embed-preset openai_large                    # check for orphaned chunks
python eval/audit_heading_sections.py                                  # check for lost headings
python -m src.ingest --embed-preset openai_large --dry-run             # safe check before any real ingest
```
