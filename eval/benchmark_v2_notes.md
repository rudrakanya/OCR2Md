# benchmark_v2 — annotation policy and change log

This file documents how `eval/benchmark_v2.yaml` was produced from
`eval/benchmark_v1.yaml`, what changed, what remains uncertain, and the
limitations of treating either file as authoritative. Read this before
citing a metric computed from v2.

## Status

Spot-checked by a single reviewer. **Not expert-validated. Not fully
independent of the system under evaluation** for the 4 entries marked
`source_discovery: system-assisted` below — their candidate source was
first seen in Phase 7's retrieval output, then independently re-verified by
reading the raw corpus file directly (not by trusting the retrieval rank,
score, or snippet). The other 26 entries are unchanged from v1, which was
itself built by reading/grepping the raw files with no retrieval run first.

## What changed from v1, and why

| ID | Change | Why |
|---|---|---|
| BV-02 | Added `The cultural heritage of madhya bharat.md`, graded 3 | Read lines 1022-1035 directly: states the founding inscription's content and both V.S./A.D. construction dates in one passage — direct evidence, not tangential. v1 had only listed 2 of several legitimate sources. |
| BV-11 | Added `The Hindu Temple Vol 2.md`, graded 3 | Read line ~1757 directly: a real architectural-iconographic account of the 8 Dikpalas' placement in temple design, not a passing mention. |
| BV-13 | Added `Intach Udaypur (1).md`, graded 2 | Read its heritage-inventory table directly: names specific baolis (Puttal Baoli, Santbhu ji Ki Baoli, etc.) with coordinates — a different but equally direct kind of evidence (concrete inventory vs. Geo-Heritage's general taxonomy). |
| BV-19 | Added `The cultural heritage of madhya bharat.md`, graded 3 | Read lines 1035-1050 directly: a full physical description of the Udayeshvara temple in non-garbled English — directly answers the query. |
| BV-23 | Lowered the serpentine paper's grade 2 → 1; marked `review_marker: uncertain` | Re-reading confirms its Naravarman content is one clause (a dating aside), not a genealogical treatment. Still on-topic, but minor. Phase 7 found it absent from the actual top-10 for this query; that absence is noted as context, not treated as proof the label is wrong. |
| BV-24 | No relevance change; added an explicit duplicate-OCR policy note | See "Duplicate OCR handling" below. |
| BV-27–30 | Added `exclude_from_aggregate: true` | See "Unanswerable queries" below. |
| BV-30 | Downgraded from implicitly-certain to `review_marker: uncertain` | "No birth date found in the passages read" is not the same claim as "confirmed absent from the whole book." |

**26 of 30 queries carry no content change** — their v1 judgments, after
re-examination, still hold: BV-01, 03–10, 12, 14–18, 20–22, 25, 26.

Every v1 query ID is preserved unchanged. No query was deleted, renumbered,
or reworded. `eval/benchmark_v1.yaml` was not opened for writing at any
point in this phase.

## Direct evidence vs. tangential mention — how the line was drawn

Applied consistently when deciding whether to add a candidate source:

- **Direct evidence**: the passage states the fact the query asks about, in
  its own right (e.g., Patil's inscription-content paragraph for BV-02;
  Kramrisch's Dikpala-placement passage for BV-11).
- **Tangential mention**: the term appears, but only as part of an unrelated
  list or aside, with no explanation of the thing itself. Example: Patil's
  Udaypur chapter lists "the eight Guardians of the Quarters" once, inside a
  general sculpture inventory — this was considered for BV-11 (dikpala
  iconography) and explicitly **not added**, because the passage names
  dikpalas without saying anything about their iconography.
- Retrieval rank or cosine/BM25 score was never used as the relevance
  criterion by itself — every addition above required reading the actual
  passage first.

## Duplicate-OCR handling (policy, applied to BV-24)

Two files in the corpus (`The Udayesvara Temple - Anupa Pande.md` and `The
Udayesvara Temple Art, Architecture and Philosophy of the Saiva
Siddhanta.md`) are confirmed, by matching tables of contents, to be two
separate OCR passes of the *same* underlying book. (A third copy,
`udayesvara-temple-art-architecture.md`, is referenced in `eval/gold.yaml`
but does not exist in this corpus directory.)

**Policy**: when a query's relevant evidence lives in a confirmed duplicate
pair, both filenames are listed (because the evaluator operates on
`source_path`, and both really are valid rows in the collection), but the
query's `why` field states explicitly that they are the same underlying
work, not two independent corroborating sources. A reviewer reading a
high book-level recall score for such a query should not interpret it as
"the system found two different confirming sources" — it found one source,
twice. This is a labelling/interpretation discipline, not an evaluator
change; `src/retrieval.py`'s existing near-duplicate penalty (halving a
flagged duplicate's fused score) is the system-side mechanism for this and
was not touched.

## Unanswerable queries — the metric-distortion problem (confirmed, not fixed)

Traced through `src/evaluate.py`'s actual code (`relevance()` and
`evaluate_queries()`): for a query with `relevant_books: []` and no `graded`
or `relevant_chunks`, **every** retrieved hit scores relevance 0 by
construction — `want_books` is empty, so `R@k` takes the explicit
`else: 0.0` branch (not a division by zero); `binary` is all zeros, so `RR`
falls through its generator's default of `0.0`; `ideal` in `ndcg()` is 0, so
it returns the explicit `else: 0.0`. This happens regardless of whether the
retriever behaved *well* (returned appropriately low-confidence, off-topic
content, as it did for BV-29 in Phase 7's actual run) or *badly* (confidently
returned something wrong). When `evaluate_queries()`'s `mean()` folds these
four queries into every aggregate (P@k, R@k, MRR, nDCG) alongside the 26
answerable ones, **it silently understates retrieval quality on the
answerable subset** — there is no way under the current metric for an
unanswerable query to contribute anything but a guaranteed zero, which is
mathematically indistinguishable from "the retriever failed."

**This is a genuine metric-definition problem, not fixed in this phase**, per
the task's instruction to document and propose rather than implement.
Proposed minimal fix (separate, future change, not applied): compute the
headline P/R/MRR/nDCG means over `answerable: true` queries only, and report
the unanswerable subset under a distinct metric that doesn't require a
`relevant_books` list at all — e.g., mean top-1 cosine/BM25 score, or a
binary "did a human judge the top result to be clearly off-topic" label.
`exclude_from_aggregate: true` is added to BV-27–30 in v2 as a machine-
readable marker of this *intent* — it is inert today; `src/evaluate.py` does
not read it, and no evaluator code was changed this phase.

## Queries still marked uncertain (need a second reviewer)

- **BV-23**: is a single incidental clause ("...and his son Naravarman
  (1094-1134)") enough to credit a source for a genealogy-framed query?
  Judged "weakly yes" here; a second reviewer might reasonably drop it to 0.
- **BV-30**: "no birth date found in the passages read" is a limited-search
  claim, not a whole-book claim. A second reviewer with more time should
  either confirm the absence more thoroughly or find the date.

## Limitations of this benchmark (v1 and v2 both)

- **Single reviewer.** Every judgment above, including the "system-assisted"
  ones, passed through one person's reading. No second opinion was sought.
- **No chunk-level (`relevant_chunks`) labels anywhere.** Verifying exact
  chunk boundaries would require running retrieval first, which conflicts
  with staying independent; this is a real, acknowledged coverage gap, not
  an oversight.
- **Only a fraction of each source book was read.** "Direct evidence"
  findings are grounded in the specific passages quoted in `evidence:` — the
  absence of a fact elsewhere in a ~400-page book (e.g. BV-30) is not
  something a grep-based review can responsibly claim.
- **30 queries is a small, hand-picked sample** biased toward topics the
  reviewer could locate quickly via heading structure and `grep` — it is not
  a random or stratified sample of real user queries.
- **This is not a replacement for `eval/gold.yaml`.** That file's 53-query
  set and its filename mismatches are reported, not fixed, in
  `eval/benchmark_v1.yaml`'s own header; v2 does not touch `gold.yaml` either.
