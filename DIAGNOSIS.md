# Phase 0 — Diagnosis (health check, not a re-audit)

**Date:** 2026-09-24 · **Builds on:** `KB_AUDIT.md` (Stage 1 audit, verdict *rebuild*), `KB_STAGE2.md` (the rebuild already carried out in SQLite) · **Nothing was modified to produce this file.**

## 1. What exists right now

| store | state | verdict |
|---|---|---|
| `kb/store.sqlite` (old) | 10,754 chunks, ~1,800-char overlapping windows. FTS5/BM25 works. `embeddings.npy` covers 9,467 of them, built with `mistral-embed`. | **Dead for dense retrieval.** The external quota is gone and the client is uninstalled, so a query cannot be embedded. Keyword search is the only live path. Superseded, kept untouched as the archive of record. |
| `kb_audit/classified_inventory.jsonl` | **19,158** claim-coherent, non-overlapping chunks from **26** sources, with source type, epistemic status, tags, cues, provenance. | Sound. This is the input to the rebuild. |
| `kb3/kb_active.sqlite` | 15,799 active chunks, FTS5 with Devanagari + diacritic folding, all five 0–1 scores, chapter buckets, corroboration/contradiction links. | Works, keyword-only. Becomes the **BM25 sidecar** for exact Sanskrit terms and proper nouns. |
| `kb3/kb_quarantine.sqlite` | 3,390 archived chunks, separate file. | Correct design: unreachable by retrieval, reversible. Carries into Chroma as a separate collection. |
| `kb3/emb_parts/` | 4,096 of 14,514 bge-m3 vectors. | **Incomplete.** The run was killed twice for low memory. These vectors are in bge-m3's 1024-d space and cannot be mixed with another model's, so they are set aside, not deleted. |

**So the dense path is still dead.** Everything else from Stage 1–2 is reusable.

## 2. Does ChromaDB + a local embedder fix it? Yes, and here is why

| problem in the old store | Chroma + local embedder |
|---|---|
| queries can't be embedded (quota gone) | the embedding model runs on this machine; no account, no quota, works offline |
| vectors covered 9,467 of 10,754 chunks and drifted from the store | one persistent collection holds vector + document + metadata per id, so they cannot drift apart |
| no way to scope retrieval to a chapter | `where` filters on `chapter_buckets`, `source_type`, `epistemic_status`, `is_quotable` |
| quarantine merely down-ranked | a separate collection that the query layer never opens |
| ids shifted whenever chunking changed | ids frozen as `sha1(text)[:16] + source`, so re-ingest is an idempotent upsert |

**Embedding model — measured, not assumed.** The corpus mixes English, Devanagari and IAST, so the model must be multilingual:

| candidate | dims | measured on this machine | decision |
|---|---|---|---|
| `BAAI/bge-m3` | 1024 | 4–9 chunks/s int8, ~1.5 cores, ~3 GB RSS; **killed twice** by the OS at 28% | strongest quality, but this machine cannot finish it reliably |
| `intfloat/multilingual-e5-small` | 384 | 8.5 chunks/s fp32 and 14 chunks/s int8 *while bge-m3 was competing for the cores*; ~0.5 GB | **chosen**: finishes ~19k chunks in roughly 20–30 min, fits in memory, already cached |

E5-small is a genuine step down in retrieval quality from bge-m3, and it is the honest trade for a build that completes on 4 cores with ~3 GB free. The build script takes `--model`, so bge-m3 can be swapped in later on a bigger machine without touching anything else. Both handle Devanagari and IAST.

## 3. Defects that must be fixed in this rebuild

| # | defect | tally | how the rebuild handles it |
|---|---|---|---|
| D1 | AI-reworded text (`[cite: N]`) is not a transcription and must never be quoted | **455 chunks** — samarangana 229, gazetteer 222, patil-composite-inscriptions 4 | `is_quotable = false` in metadata; retrieval may use them for context, never as a quote |
| D2 | *Jagta Hua Kasba* writes "Udaipur", so the town's own chapters missed it | 316 chunks | source-scoped alias already applied at entity level; carried into Chroma as an `entities` field and into the BM25 sidecar |
| D3 | speculation stored as fact | ~129 estimated; 288 candidates hand-read, **36** genuine | statuses corrected in the inventory; `speculation` never enters a chapter bucket as `welcome` |
| D4 | inference vs speculation labels are weak (held-out precision 2/9) | — | treated as candidate pools; the 288 strongest were adjudicated by hand and are the only ones acted on |
| D5 | most chunks had no page number | old store 12% had one; **new inventory 78%**, 100% have a heading trail | `page` in metadata, heading trail as documented fallback |
| D6 | OCR damage | 979 chunks tagged | tagged, low credibility; the new book adds a per-page QC gate before ingestion |
| D7 | duplicates inflate corroboration | 393 linked; Patil composites 180, Adhikari self-repeats 158 | duplicate clusters count once; both copies stay retrievable |

## 4. What this phase changes

Nothing. No store was written. The plan is confirmed:
1. OCR the Rājamārtaṇḍa and gate it on quality (Phase 1).
2. Refine the source taxonomy from 5 coarse types to 10 pointed ones (Phase 2).
3. Classify the new book, splitting the Bhoja-authorship layer from the yoga-doctrine layer (Phase 3).
4. Build the Chroma store over all 27 sources with a local embedder (Phase 4).
5. Validate chapter-scoped retrieval (Phase 5).

**One correction to the brief:** the new book has already been OCR'd in the previous session with Tesseract (Devanagari script model, `--psm 3`, 400 dpi) — a real OCR engine, no LLM transcription. Phase 1 therefore runs the **quality gate** over that output and re-renders the page images to sit beside it, rather than starting the OCR again.
