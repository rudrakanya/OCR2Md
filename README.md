# Udaypur research corpus — ChromaDB pipeline

A local, single-user vector store over 25 reference books for the Udaypur /
Udayeśvara book project. It retrieves passages with their source clearly
identified, tags every passage by which of your 19 chapters it supports, tells
you which chapters are thinly sourced, and measures its own retrieval accuracy.

Everything runs offline once the embedding model is downloaded. There is no
server, no container, and no cloud dependency.

---

## Quick start

```bash
# one-time
pip install chromadb sentence-transformers rank_bm25 langchain-text-splitters pyyaml indic-transliteration

# build (clean rebuild — clears the collection, caches and sidecar first)
python -m src.ingest --rebuild

# ask it something
python -m src.query "Bhumija sikhara of the Udayesvara temple" --chapter C08

# how good is it?
python -m src.evaluate --compare

# where are my sourcing gaps?
python -m src.report
```

---

## The four things this does

### 1. Ingest — `src/ingest.py`

```bash
python -m src.ingest --rebuild                 # clean build (§3)
python -m src.ingest                           # idempotent upsert, no wipe
python -m src.ingest --dry-run                 # chunk + report, embed nothing
python -m src.ingest --embed-preset e5_small_fast
python -m src.ingest --limit 3                 # smoke test on 3 books
```

Load → chunk → embed → tag → upsert.

- **Chunking** splits on Markdown headings first, then recursively inside each
  section to a ~1000-token target with 150-token overlap. Fragments under 200
  tokens are merged into a neighbour. Tables and fenced Sanskrit blocks are kept
  whole. Each chunk's *embedded* text is prefixed with
  `[Book: … > heading path]`, which disambiguates near-identical passages
  across books; the *stored* text is the original, untouched.
- **Chunk IDs** are `sha1("<filename>:<chunk_index>")`, so re-running upserts
  in place and never duplicates. `--rebuild` is the deliberate override.
- **Near-duplicates** are detected by hashed 8-gram shingles and flagged with
  `duplicate_of`, not deleted. This matters here: three files reproduce D. R.
  Patil's 1952 text, and without the flag one passage would occupy several of
  your top-10 slots while looking like corroboration from three sources.
- **Fails loudly** on an empty file, non-UTF-8 bytes, a book that yields zero
  chunks, or a corpus file missing from `books_manifest.yaml`.

### 2. Query — `src/query.py`

```bash
python -m src.query "praśasti of Udayāditya"
python -m src.query "temple economy" --chapter C13 --k 5
python -m src.query "Betwa streamflow" --no-hybrid      # dense only
python -m src.query "Nagari palaeography" --json
```

Prints book title, heading path, primary/all chapters, similarity, and a
snippet for each hit.

**Hybrid retrieval** is on by default: a dense channel (Chroma, cosine) and a
BM25 channel over the folded text, combined with Reciprocal Rank Fusion. RRF
merges by *rank*, so the two scales never have to be made comparable. Dense
search finds the paraphrase; lexical search finds the exact string — and this
corpus turns on exact strings (`Udayeśvara` vs `Udayapura`, one inscription
among many). `--chapter` applies `where={"chap_C08": True}` to the dense channel
*and* restricts the lexical channel to the same ids, so the filter narrows the
whole funnel rather than half of it.

### 3. Evaluate — `src/evaluate.py`

```bash
python -m src.evaluate --compare      # dense-only vs hybrid, side by side
python -m src.evaluate --worst 10     # which queries are failing
python -m src.evaluate --ablate       # sweep chunk sizes x models (§10.3)
```

Reports Precision@k and Recall@k for k ∈ {3,5,10}, MRR, nDCG@10, per-chapter
tagging precision, and hard-negative violations (a geology query must not
surface iconography). Each run is saved to `eval/results/chroma/` with the
config hash and library versions, so any two runs are comparable.

**Read this before quoting a number.** `eval/gold.yaml` judges at *book* level:
a chunk from the right book about the wrong subject counts as a hit, so
precision is an upper bound. The 53 seed queries are mine, written from
scanning the corpus rather than reading it — they are a **regression baseline**
("did my change help?"), not an absolute measure. To tighten a query, add
`relevant_chunks` with specific chunk ids from `--json` output; the harness
prefers those over book labels when present.

### 4. Report — `src/report.py`

```bash
python -m src.report              # writes ./corpus_report.md
python -m src.report --stdout
```

Chunk counts and token distribution per book; a chapter coverage table; **gap
flags** (too few chunks, too few books, nothing primarily about it, or >60% of
evidence from a single source); and cross-book concentration. This is the
report to read *before* drafting a chapter, not after.

---

## Re-tuning without re-embedding

Chapter tagging is deliberately a separate step, because tuning it is the thing
you will do most often:

```bash
python -m src.tag                 # re-tag using the vectors already stored
python -m src.tag --explain C15   # what did C15 actually catch?
```

`src/tag.py` reads the chunk vectors back out of Chroma and re-embeds only the
19 chapter descriptors — seconds, not hours. So:

1. Edit a descriptor or keyword list in `chapters.yaml`.
2. `python -m src.tag`
3. `python -m src.tag --explain C15` to see what changed.
4. `python -m src.report` to see the new coverage.

**How tagging works.** Each chapter's title + scope + descriptor + keywords is
embedded and compared to every chunk by cosine similarity. Each chunk is tagged
with its top-3 chapters *plus* any chapter above a cutoff **calibrated from the
observed score distribution** — never a hardcoded threshold, because cosine
scales differ between models and a number tuned for bge-m3 is meaningless for
e5. The method (`percentile` / `zscore` / `knee`) and its parameter live in
`config.yaml`, and the chosen cutoff is printed and saved on every run.

Descriptors are written as *prose in the register of the corpus* rather than as
labels. A descriptor is really a query, and one that reads like the passages it
should match retrieves far better than a bare chapter title.

An optional LLM verification pass over low-confidence chunks is specified and
left as a clean hook (`tagging.llm_verification`, off by default,
`tag.verify_low_confidence`). It is not implemented.

---

## Switching embedding models

Three lines in `config.yaml`:

```yaml
embedding:
  backend: sentence_transformers    # or: openai
  model: BAAI/bge-m3
  dim: 1024
```

Presets are pre-wired under `embedding.alternatives` and selectable per run
without editing the file:

```bash
python -m src.ingest --rebuild --embed-preset e5_small_fast
```

| Preset | Model | Dim | Notes |
|---|---|---:|---|
| *(default)* | `BAAI/bge-m3` | 1024 | Multilingual, handles Devanagari + IAST, 8192-token context. ~2.3 GB. |
| `e5_large` | `intfloat/multilingual-e5-large` | 1024 | Needs `query:`/`passage:` prefixes (already configured). 512-token limit. |
| `e5_small_fast` | `intfloat/multilingual-e5-small` | 384 | ~8× faster on CPU. **512-token limit truncates 1000-token chunks at half** — use for pipeline validation, not for final quality. |
| `openai_large` | `text-embedding-3-large` | 3072 | Needs `OPENAI_API_KEY`; `pip install openai`. |

**Switching models invalidates the index.** Vectors from two models are not
comparable, so always `--rebuild` after a change. The embedding cache is keyed
by model name, so switching back and forth does not re-pay for work already
done.

We deliberately do *not* register a Chroma `EmbeddingFunction`; vectors are
computed here and passed explicitly to both `upsert` and `query`. Chroma has
changed that interface across releases, and this way ingest and retrieval
provably share one code path.

---

## Layout

```
config.yaml            every tunable; nothing in src/ hardcodes a number
books_manifest.yaml    filename -> title/author/year/language/script
chapters.yaml          19 chapter descriptors, keywords, negative keywords
corpus_report.md       generated by src/report.py

src/settings.py        config load, hashing, provenance
src/textutil.py        NFC, Devanagari->IAST folding, language detection
src/chunker.py         heading-aware + recursive splitting
src/dedupe.py          shingle near-duplicate detection
src/embedder.py        model adapters + on-disk vector cache
src/store.py           Chroma collection + SQLite sidecar
src/ingest.py          the build driver
src/tag.py             chapter tagging (re-runnable without re-embedding)
src/retrieval.py       dense + BM25 + RRF
src/query.py           retrieval CLI
src/evaluate.py        metrics harness + ablations
src/report.py          coverage and gap report

eval/gold.yaml         53 seed labelled queries — extend this
eval/results/chroma/   one JSON per run, stamped with the config hash

chroma_db/             the store (gitignored)
  chroma.sqlite3         vectors, documents, scalar metadata
  sidecar.sqlite3        text_folded, chunk bookkeeping, run records
  sidecar.bm25.pkl       cached BM25 index
  embed_cache.sqlite3    content-hash -> vector
```

### Metadata on every chunk

`source_path`, `book_title`, `author`*, `book_year`*, `kind`*, `heading_path`,
`chunk_index`, `token_count`, `language` (`en`/`hi`/`sa`/`mixed`), `page_start`*,
`is_duplicate`, `duplicate_of`*, `dup_score`*, `chap_C01`…`chap_C18`, `chap_AW`
(booleans), `primary_chapter`, `chapters_str`, `chap_score_primary`,
`chap_margin`, `chap_low_confidence`.

*\* omitted entirely when unknown — Chroma rejects `None`, and metadata values
must be scalars, which is why chapters are boolean columns rather than a list.*

`text_folded` lives in the sidecar, not in Chroma: it is never displayed and
never embedded, and storing a folded copy of every chunk would roughly double
the metadata payload for no retrieval benefit.

---

## Unicode

The corpus is English, Hindi (Devanagari), Sanskrit and IAST — 10 of the 25
files carry Devanagari, `samarangana-sutradhara.md` alone has 331k Devanagari
characters. So:

- Everything is normalised to **NFC** on load.
- Stored and displayed text keeps **every diacritic and every Devanagari
  codepoint**. Nothing is ever stripped from what you read or cite.
- A **separate folded copy** (`text_folded`) is lowercased and reduced to ASCII
  purely for BM25, so searching `Udayaditya` matches `Udayāditya` and
  `उदयादित्य`. Folding routes Devanagari through IAST transliteration first —
  NFKD-then-strip would delete Devanagari outright, leaving every Hindi passage
  with an empty folded string.
- `src/settings.py` forces UTF-8 on stdout at import. Windows consoles default
  to cp1252 and will kill a run the first time a Devanagari character is
  printed.

---

## Notes and known limits

- **`books_manifest.yaml` is a draft.** 17 of 25 rows are marked
  `needs_review: true`, each with an `_evidence` note quoting the text the
  entry came from. Nothing was supplied from outside the files. Missing
  authors/years affect citation display and the report only — not retrieval.
- **Three files overlap** (`madhya-bharat-*` reproduce Patil 1952; one also
  contains all of *Some Paramāra Temples*). Handled by duplicate flagging, and
  documented at the foot of the manifest.
- **`Jagta_Hua_Kasba` appears twice**, Hindi original and English translation,
  linked by `translation_of`. Both will legitimately surface for C15/C18.
- **The gold set is provisional** — see the header of `eval/gold.yaml`.
- **This is independent of the v2 pipeline** in the repo root (`build_kb.py`,
  `kb/`, `retrieve.py`). Nothing here reads or writes that store. The `eval/`
  directory is shared, so results are namespaced under `eval/results/chroma/`.
