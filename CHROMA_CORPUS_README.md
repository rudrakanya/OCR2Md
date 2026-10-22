# Udaypur ChromaDB Research Corpus

A local, offline-friendly ChromaDB vector store over the 25 reference books
for the Udaypur / Udayeśvara temple book project. Retrieves relevant
passages with source book + section attached, tags every passage by which
book chapter it supports, reports coverage gaps, and measures retrieval
accuracy against a labeled query set.

This is a **separate system** from this repo's existing SQLite-based
drafting pipeline (`kb_store.py`, `build_kb.py`, `draft_chapter.py`) — a
standalone, config-driven corpus for research/exploration, not wired into
chapter drafting.

## Layout

```
config.yaml            all tunables (chunking, embedding, tagging, retrieval)
books_manifest.yaml    filename -> title/author/year/kind (edit to correct)
chapters.yaml          chapter taxonomy + tagging descriptors (edit to retune tagging)
src/
  common.py            shared: config, chunking, Unicode, embedding fn, Chroma/sidecar helpers
  ingest.py            load, chunk, embed, tag, upsert
  tag.py               re-tag existing chunks without re-embedding
  query.py             CLI retrieval (dense / --chapter filter / --hybrid)
  evaluate.py          accuracy/precision harness against eval/gold.yaml
  report.py            coverage + gap-flag Markdown report
eval/
  gold.yaml            labeled test queries (seed set, unverified -- see below)
  results/             one JSON per evaluate.py run, named <timestamp>_<confighash>.json
chroma_db/             ChromaDB persistent store (created by ingest.py)
  sidecar.sqlite3       text_folded index for hybrid search (kept out of Chroma metadata)
  ingest_state.json     per-book content hash, for incremental re-ingest
coverage_report.md     written by report.py
```

## Setup

```
python -m pip install chromadb rank_bm25
```

Requires a local Ollama server with `bge-m3` pulled (`ollama pull bge-m3`) —
the embedding function in `src/common.py` calls it directly; no
sentence-transformers/torch install needed.

`config.yaml`'s `corpus_dir` points at `Udaipur Books Markdown files/` in
this repo (the 25-book set — confirmed against `books_manifest.yaml`).
Change it if your corpus lives elsewhere.

## 1. Ingest

```
python src/ingest.py --rebuild        # first run: wipes chroma_db/, sidecar,
                                       # ingest_state.json, eval/results/ first,
                                       # then embeds all 25 books from scratch
python src/ingest.py                  # later runs: incremental -- only
                                       # (re)processes a book if its file
                                       # content hash changed since last time
python src/ingest.py --dry-run        # chunk + report counts only, no
                                       # embedding, no writes -- safe to run
                                       # any time you tweak config.yaml's
                                       # chunking.* settings
python src/ingest.py --only "X.md" "Y.md"   # re-embed specific books only
```

Each chunk's *stored* text (what you see in query results) is the original
passage. What's actually *embedded* additionally has a contextual header
prepended (`[Book: <title> > <heading path>] <text>`) — this disambiguates
near-identical passages across books without polluting what you read.

IDs are deterministic (`sha1(filename:chunk_index)`), and `upsert` is always
used, so re-running never duplicates a chunk.

## 2. Tag (re-tuning without re-embedding)

Chapter tags are cosine similarity between each chunk and each chapter's
enriched descriptor in `chapters.yaml`. If you edit a chapter's `scope` or
`keywords`, or change `config.yaml`'s `tagging.*` thresholds, re-tag without
touching the embeddings:

```
python src/tag.py                 # recompute + write tags for the whole collection
python src/tag.py --dry-run       # report the cutoff distribution, write nothing
```

The cutoff isn't a single hardcoded number — for each chunk it's
`max(that chunk's own P-th percentile score across all 19 chapters, an
absolute floor)`, both set in `config.yaml`. `tag.py --dry-run` prints the
mean/median cutoff actually used across the corpus so you can see whether
your percentile/floor settings are behaving as intended.

Note: `ingest.py` already tags every chunk inline during ingest (no need to
run `tag.py` after a fresh `--rebuild`) — `tag.py` is for retagging
*existing* embeddings after a `chapters.yaml`/tagging-config change only.

## 3. Query

```
python src/query.py "how was the Udayeshvara temple's shikhara built"
python src/query.py "praśasti inscription" --chapter C10 --k 5
python src/query.py "Betwa river discharge" --hybrid
```

`--chapter Cxx` filters to chunks tagged `chap_Cxx=True` and prints how many
candidates that narrowed the pool to. `--hybrid` additionally runs BM25 over
the diacritic-folded sidecar index and fuses with dense results via
Reciprocal Rank Fusion (weights in `config.yaml`) — use it for exact proper
nouns/inscription names/acronyms an embedding might miss.

## 4. Evaluate

```
python src/evaluate.py
python src/evaluate.py --config config.yaml --config config_variant.yaml   # ablation
```

Prints precision@{3,5,10}, recall@{3,5,10}, MRR, nDCG@10, per-chapter tagging
precision, and a hard-negative/filter-sanity check, then saves the full
result (+ config hash) to `eval/results/`.

**Read this before trusting a number:** `eval/gold.yaml`'s `relevant_books`
were assigned from each book's declared scope in `books_manifest.yaml`, not
by a human checking actual retrieved passages — every item has
`verified: false`. Treat these numbers as a regression signal (did a config
change make retrieval better or worse?) rather than ground truth, until you
extend/correct the gold set and flip items to `verified: true`. See the
comment block at the top of `eval/gold.yaml` for how to add or correct an
item.

**Ablations across chunk sizes or embedding models:** `evaluate.py` compares
across *already-ingested* collections. To compare, say, 1000- vs 500-token
chunking: copy `config.yaml` to `config_500tok.yaml`, change
`chunking.target_tokens` and `collection_name` (so it doesn't overwrite the
main collection) in the copy, run `python src/ingest.py --config
config_500tok.yaml --rebuild`, then `python src/evaluate.py --config
config.yaml --config config_500tok.yaml` for the side-by-side table. Same
pattern for a different `embedding.model`.

## 5. Report

```
python src/report.py
```

Writes `coverage_report.md`: chunk counts and token distribution per book,
a chapter coverage table (chunk count + contributing books per chapter),
gap flags (chapters below a chunk-count floor, or resting on a single book),
and a cross-book concentration-risk note.

## Re-tuning workflow

| You changed... | Re-run |
|---|---|
| `chunking.*` in config.yaml | `ingest.py --rebuild` (chunk boundaries changed) |
| `embedding.*` (model/backend) | `ingest.py --rebuild` (vectors are now incompatible) |
| `chapters.yaml` scope/keywords | `tag.py` only |
| `tagging.*` thresholds | `tag.py` only |
| `retrieval.*` (k, hybrid weights) | nothing to re-run — `query.py`/`evaluate.py` read it live |
| `books_manifest.yaml` title/author/year | `ingest.py --rebuild` (metadata is baked into chunks) |

## Switching the embedding model

`config.yaml`'s `embedding.backend` is the single switch
(`get_embedding_function()` in `src/common.py` is the adapter point).
`ollama` (default) is implemented; the block has commented-out shapes for
`sentence_transformers` (`BAAI/bge-m3` loaded directly, if you'd rather not
depend on a running Ollama server) and `openai` (`text-embedding-3-large`,
requires an API key) — wire either up as a second branch in
`get_embedding_function()` following the same
`{model.name() -> __call__(texts) -> list[list[float]]}` shape, then
`ingest.py --rebuild` (a model change invalidates existing vectors).

## Reproducibility

Every `ingest`/`tag` run appends a line to `logs/pipeline_runs.jsonl` with
the config hash, library versions, and run stats, so you can tell which
settings produced which state of the collection. Every `evaluate.py` run's
saved JSON is named `<timestamp>_<confighash>.json` for the same reason.
