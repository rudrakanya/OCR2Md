# Phase 3 — retrieval readiness

**Date:** 2026-10-05 · **Collection:** `udaypur_kb` (14,702 sqlite chunks / 14,647 vectors)
**Model:** `intfloat/multilingual-e5-small`, 384-d, int8-quantised, already cached locally
**Constraint observed:** audit only — no re-embed, no store writes, no paid-API calls.

Two questions, because they fail differently: is a chunk a usable unit of evidence
(coherence), and does the right chunk come back (behaviour).

## Headline

The knowledge base is **usable for drafting today**. Three quarters of chunks are clean
units, the defects Phases 1–2 found do not reach a drafter through the Chroma path, and
the gating in `chapter_pipeline.load_bucket` holds. The one real retrieval defect is
**language asymmetry**: an English query cannot reach the Devanagari and Hindi sources,
so four of the corpus's richest primary works are invisible to the way chapters are
actually drafted. That is a model limitation, and it is the only finding here that
justifies a re-embed.

---

## 1. Chunk coherence

Every chunk in the store, tested as a quotable unit:

| Flag | Chunks | Share |
|---|---|---|
| **clean** | **11,103** | **75.5%** |
| ends mid-sentence | 1,948 | 13.2% |
| starts mid-sentence | 1,101 | 7.5% |
| shorter than 200 chars | 455 | 3.1% |
| table fragment | 389 | 2.6% |
| mostly non-letters | 143 | 1.0% |
| running head only | 9 | 0.1% |

Median chunk 526 characters (p10 271, p90 1,247). A 13% mid-sentence tail rate is
normal and largely benign
— `build_kb` deliberately carries a sentence-level overlap bridge between chunks, so a
thought split at a boundary stays retrievable from both sides.

Worst sources by flagged share: SIN-B (41% clean), GUP (54%), ADH (56%), BET-S (57%),
GAN (63%), INT-ARC (67%). ADH's and GUP's figures are the table fragments already
documented in `EXTRACTION_FAILURES.md` and `ASSET_AUDIT.md`.

### Correction to a figure I reported mid-audit

I first measured **26.1% clean** and said so. That number was wrong: my
"starts mid-sentence" test matched any chunk beginning with the word *the*, which
flagged thousands of perfectly good openings. Restricted to genuinely lower-case or
punctuation-initial starts, the real figure is **75.5% clean**. The corpus is in much
better shape than that first pass suggested.

---

## 2. Retrieval behaviour

Twelve queries drawn from what the book actually has to answer, top-8 each (96 slots).

### Does the Phase 1–2 damage reach a drafter? No.

| Test | Result |
|---|---|
| queries returning a fabricated ADH chunk | **0 / 12** |
| ADH collapse chunks with vectors | **0 of 50** — Chroma holds 280 ADH rows to sqlite's 328 |
| archived `ai-derived` chunks in a chapter-scoped top-40 | **0** (C7 and C10, with and without `quotable_only`) |
| queries where two Patil registrations shared one top-8 | **1 / 12** |
| the same text returned twice in one top-8 | **1 / 12** |

The embedding step deduplicated by content hash, which is why the ADH repetition
collapse never entered the vector space: the 48 duplicate rows became one vector each.
Five sources show the same benign sqlite-vs-Chroma gap, and in every case it equals
that source's within-source duplicate count (ADH 48, GAN 3, SAM 2, SIN-T 1, TIW-H 1).

The Patil co-occurrence did fire once, and it is worth seeing — *"Paramara dynasty
genealogy Bhoja successors"* returned **PAT-CH, PAT-INS and PAT-TEM in a single top-8**,
with one duplicated passage appearing twice. That is the false-corroboration risk from
`EXTRACTION_FAILURES.md` §2 occurring in practice, in the chapter area where
genealogy and dates matter most.

### The real defect: English queries cannot reach the Devanagari sources

Eight of 27 sources never appeared in any of the twelve top-8 lists:

> BET-S, BHJ-H, GUP, PAR, RAJ-E, RAJM, SKP-13, TIW-H

Four of those — **RAJM** (Bhoja's own *Rājamārtaṇḍa*), **BHJ-H**, **TIW-H** and
**RAJ-E** — are the Hindi and Sanskrit works, and they are among the most evidentially
valuable things in the corpus. They are fully embedded and perfectly retrievable; they
just cannot be reached in English. The same corpus, queried in Hindi:

| Query | Top-8 sources |
|---|---|
| `मूर्ति लक्षण और प्रतिमा विज्ञान` | TIW-H · TIW-H · GAN · BHJ-H · KRAM-2 · SAM · TIW-H · **RAJM** |
| `Vishnu avatars iconographic description` | SIN-B · SIN-B · INT-ARC ×4 · TIW-E · INT-ARC |

This confirms empirically what `kb3_chroma_query.py` already warns about in a comment:
`multilingual-e5-small` aligns English and Devanagari weakly. The chapter-scoped path
mitigates it deliberately — it scores the whole bucket and weights chapter relevance at
0.65 against 0.35 for query similarity, precisely so a Devanagari passage is not ranked
out — but any unscoped English query misses these works entirely.

**GUP is a separate case.** It has 691 chunks and 691 vectors and is not missing
anything, yet it never surfaced, even for *"Sapta Matrka iconography…"* or
*"iconography of Hindu deities attributes and symbols"*. Its text is dense tabular
iconography, which embeds poorly as prose. Also noted: I briefly reported GUP as having
zero Chroma rows; that was my own error — I queried `gupte-iconography` when its
`source_id` is `gupte-1972`. GUP is fully embedded.

### Source concentration

INT-ARC takes **28 of 96 slots (29%)**. Two queries are effectively single-source:
*"Betwa river seasonal flow and rainfall"* returned BET-K 8/8, and *"stepwell baoli
water structures at Udaypur"* returned INT-ARC 7/8. Five of twelve queries drew on
only two or three distinct sources.

For a book whose standard is that claims be corroborated, single-source topics are
where to expect `[single-source]` status markers — not a defect, but worth knowing
before drafting C2 and C3.

---

## 3. Re-embed recommendation

| Option | Cost | What it buys | Verdict |
|---|---|---|---|
| **Do nothing** | — | base is usable; 75.5% clean, defects not retrievable | **viable** |
| **Re-chunk + re-embed, same model** | ~14 min CPU, zero API | recovers 362 substantive table rows incl. GAN's epigraphic concordance (`ASSET_AUDIT.md` §1) | **recommended** |
| **Re-embed with `bge-m3`** | hours CPU, zero API; ~1024-d index | fixes the English↔Devanagari asymmetry — the only defect found here | **worth it, but validate first** |
| **Re-OCR the corpus** | many hours | nothing; 10 of 14 verifiable books already pass | **no** |

Measured throughput for the current model on this machine: **17.5 chunks/s**, so a full
14,702-chunk re-embed is **≈14 minutes** and costs nothing but CPU.

### One caution on re-chunking

Re-chunking is a clear win for structured content but **not** a uniform win for
coherence. Comparing the live store against a fresh `build_kb.chunk_markdown` run:

| Source | Live clean | Fresh clean |
|---|---|---|
| GAN | 63% | **75%** |
| GUP | 54% | **64%** |
| INT-GEO | 73% | 72% |
| INT-ARC | 67% | **54%** |
| BET-S | 57% | **41%** |
| ADH | 56% | **37%** |
| SIN-B | 41% | **32%** |

So re-chunking recovers every lost table row (0 missing after a fresh run, against
116/131/107 missing today) while degrading chunk-boundary quality for INT-ARC, SIN-B,
ADH and BET-S. Those four should be inspected before a wholesale re-chunk, or
re-chunked and checked per source rather than in one pass.

### On `bge-m3`

`kb3_embed.py` already targets it and was paused. It is the right fix for the language
asymmetry, but note the machine constraint: roughly 3 GB of free RAM and no native
bf16, so it needs to run resumably and be checked for memory before being started.

---

## 4. What is sound, and should not be touched

- 27 of 27 sources have vectors; 384-d throughout; none degenerate or zero-norm.
- Content-hash deduplication at embed time is working and has already neutralised the
  ADH repetition collapse in the vector space.
- `chapter_pipeline.load_bucket` filters `is_archived: False` **and** re-checks the flag
  per row. The archived `ai-derived` chunks are correctly excluded.
- Chapter-scoped retrieval scores the whole bucket rather than a top-N, which is what
  keeps Devanagari passages reachable in the drafting path.

### One latent risk worth closing

The six `ai-derived` chunks are flagged `is_quotable: false` and `is_archived: true`,
and the archive collection holds 0 of them — they are still **in the active collection
with all 17 bucket flags set** (`in_C1` … `in_C16`, `in_AF`). Nothing retrieves them
today because `load_bucket` filters on `is_archived`, and they rank nowhere near a
top-40. But a future query path that filters only on `in_<chapter>` would pick them up.
Earlier in this work I described them as archived *and un-bucketed*; the flags were set
but **the bucket membership was not removed**, so that description was half right.
Clearing the bucket flags is a one-line store write and has not been done.

## Artefacts

- `kb_audit/retrieval_readiness.json` — coherence tally and per-query results
- `audit_retrieval.py` — the Phase 3 harness
