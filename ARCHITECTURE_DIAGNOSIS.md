# Chapter-generation pipeline: architecture diagnosis and fixes

Date: 2026-08-22. Diagnostic case: Chapter 1 ("Udaypur: A Small Town with a
Long Memory"), local backend (`gpt-oss:20b` via Ollama, 16GB RTX 5080).

This document is the result of a systems-level diagnosis requested after
repeated, seemingly random `draft_chapter.py` failures (`Truncated` claim
decomposition, edits discarded for dropping/inventing citation ids, a
mid-run `RuntimeError`, an unhandled HTTP 500). The brief was explicit: trace
root causes with real instrumentation, don't guess, don't assume a bigger
model or context window is the fix. Everything below is backed by either
code inspection (file:line) or a live instrumented test — where a number is
quoted, it came from `logs/llm_calls.jsonl` or a direct API call, not an
estimate.

---

## A. Root cause

There was no single root cause. Five distinct, independent defects were
found, each contributing to a *different* symptom that had been getting
folded together under "the model is unreliable":

1. **`think=False` breaks gpt-oss:20b on real inputs.** The first fix
   attempted for `verify.py`'s claim-decomposition truncation was disabling
   the model's reasoning entirely, on the theory that mechanical extraction
   doesn't need it. Measured effect on a realistic ~450-word input: **15
   output tokens, empty content, `done_reason: "stop"`** — no error, just
   nothing where the JSON should be. gpt-oss is built around a multi-channel
   reasoning format; forcing reasoning off on anything past a trivial prompt
   leaves it unable to find the right channel to answer in.

2. **Two different failures were both called "Truncated."** `llm.py`'s
   `complete_json()` raises `Truncated` in two places: when Ollama reports
   `done_reason: "length"` (a genuine token-ceiling hit — the fix is a bigger
   budget), and, separately, inside `parse_json()`'s bracket-matching
   fallback, whenever the JSON string never closes **regardless of
   `done_reason`**. A live capture nailed the second case exactly: a
   452-word decompose window generated **27,123 characters of internal
   reasoning** (vs. 4,804 and 10,417 chars on same-sized windows moments
   before and after it — a 5.6x outlier), consumed 7,019 of its 8,000-token
   budget doing so, and left the JSON incomplete — while Ollama still
   reported `done_reason: "stop"`. Retrying with the *same* prompt has a real
   chance of success here, because the excess length is stochastic, not
   structural; the code was treating it as unrecoverable.

3. **`plan_chapter()` had no repair path.** Unlike every other structured-JSON
   call in the pipeline, chapter planning used a raw `complete()` call plus a
   local regex parser (`_parse_json`, since removed) with no retry-on-malformed-JSON
   logic. One bad generation (non-deterministic; temperature 0.3) failed the
   entire chapter at the earliest possible stage with `RuntimeError: planner
   returned no usable sections`.

4. **Ollama's HTTP 500 wasn't classified as retryable.** `llm.py`'s error
   classifier treated 502/503/504 as transient but not 500. A live run hit a
   real 500 from the local Ollama server during a JSON-repair follow-up call
   and the exception propagated as an unhandled crash instead of being
   retried.

5. **A failed decompose window vanished without a trace.** `decompose()`'s
   `on_error` callback returned `{"claims": []}` for a failed window — the
   same shape as a window that legitimately contains zero claims. That
   window's prose was never represented in *any* of the pipeline's
   supported/unsupported/contradicted/unverified counts. A section could
   report "100% faithful" after silently losing 400-500 words of coverage,
   with nothing in the output saying so.

6. **Application-level concurrency was sized for a cloud API, not this
   backend, and caused a real congestion collapse.** Found live during the
   final validation run, after items 1-5 were already fixed: `decompose()`
   fans internal work across `workers=3`, `entail()` across `workers=4`, and
   `draft_chapter.py`'s VERIFY stage additionally runs all of a chapter's
   sections' `verify_section()` calls concurrently (`--workers`, default 4)
   — a real fan-out of 15-30+ simultaneous logical requests. Every one of
   them funnels through `OLLAMA_MAX_CONCURRENT`'s single-concurrency gate
   (required for VRAM safety on this 16GB card), so nothing was ever
   double-loaded onto the GPU — but per-call latency climbed **monotonically**
   as the queue built faster than it drained: 328s, then 461s, 574s, 709s,
   768s, 881s, 988s, 1001s and still rising when three decompose windows
   ultimately failed outright (`LLMError`, not a clean retry). That is a
   congestion collapse, not stable backpressure: extra concurrency against a
   backend that can only run one request at a time adds queue depth, not
   throughput, and every failed call's retry piles more demand onto a queue
   that was already the problem. Fixed with `llm.safe_workers()` — a single
   function every caller of concurrent work now goes through, returning 1 on
   the Ollama backend regardless of what was requested (OpenRouter, which has
   real backend concurrency, is unaffected).

None of these are context-window or model-capacity problems in the sense the
initial hypothesis suggested. All six are fixable defects in retry
classification, error handling, concurrency sizing, and observability — not
reasons to switch models or blindly raise `num_ctx`.

---

## B. Current architecture (what already exists — read before assuming gaps)

The pipeline already implements several of the safeguards a from-scratch
design would call for. This matters because the brief asked me not to
"invent an architecture based solely on the description" — several requested
capabilities are already present:

```
book_outline.py (chapter specs: title, scope, sub-topics, constraints)
        |
query_gen.py (derives retrieval queries per sub-topic, LLM-paraphrased + deterministic)
        |
retrieve.py (hybrid funnel: dense + BM25 + entity-exact -> RRF -> cross-encoder
             rerank -> calibrated relevance floor -> source-diversity cap)
        |
make_evidence.py (builds book/_evidence/chNN.json: per-SUB-TOPIC evidence
                   packs with stable [E##] ids, coverage status GAP/THIN/OK)
        |
draft_chapter.py draft() -- 7 stages, each an artefact on disk:
   [1] KB access         - refuse a stale evidence pack (KB hash mismatch)
   [2] Retrieval surface - report what make_evidence.py already found
   [3] Evidence validate - verify.validate_pack(), deterministic, pre-prose
   [4] Formulation       - plan_chapter() (LLM outline) -> draft_section()
                           PER SECTION, each from ONLY its own sub-topics'
                           evidence slice (render_evidence()) -- this IS
                           the "section-level evidence packet" architecture
                           requested; it was not missing
   [5] Editorial         - stitch_section() revises for flow; citation_delta()
                           mechanically reverts any edit that drops/invents
                           a citation id or a gap marker
   [6] VERIFY/REPAIR     - decompose() (prose -> atomic claims) -> entail()
                           (claim x evidence -> verdict) -> repair()
                           (constrained rewrite, budget-capped) ->
                           cut_unsupported() (last-resort GAP substitution)
   [7] Citation resolve  - [E12] -> numbered endnotes; invented ids stripped
                           and reported, never silently accepted
        |
assemble_book.py -> manuscript; validate_book.py -> UNGROUNDED-term audit
```

`blueprint.py` additionally implements the "source coverage matrix" /
research-dossier concept requested in the brief (units -> sub-units ->
research questions -> reference mapping -> citation plan, with conflict and
gap detection) as a *pre-drafting* stage — it exists, was broken by an
earlier refactor (fixed this session, unrelated to the current diagnosis),
and can be run ahead of `draft_chapter.py` for chapters that need deeper
research planning.

Evidence integrity was already enforced mechanically in three places before
this diagnosis started: `resolve_citations()` strips any `[E##]` not present
in the evidence brief; `citation_delta()` reverts an editorial pass that
changes the citation set at all; `verify_section()`/`repair()`/`cut_unsupported()`
never delete a claim outright — unsupported claims become `[GAP — not in
sources]`, contradicted claims are flagged for correction (never silently
cut), and claims the verifier failed to judge are tracked as `unverified`,
explicitly excluded from the faithfulness denominator. This is a real,
working evidence-integrity architecture, not a gap needing a rewrite.

---

## C. Failure points (exact locations)

| # | File:function | What happens | Evidence |
|---|---|---|---|
| 1 | `llm.py` `_OllamaChat.complete()` via `think=False` | Empty output on realistic input | Live test: 15 tokens, empty content |
| 2 | `llm.py` `parse_json()` | Raises the same exception for a real ceiling-hit and a "model stopped early with incomplete JSON" | `logs/llm_calls.jsonl`: `done_reason: "stop"`, `completion_tokens: 7019/8000`, JSON still unclosed |
| 3 | `draft_chapter.py` `plan_chapter()` (pre-fix) | No repair round on malformed JSON | Reproduced live: `RuntimeError: planner returned no usable sections` |
| 4 | `llm.py` `_classify()` (pre-fix) | 500 not in the transient-error marker list | Reproduced live: `HTTPError: 500 Server Error` propagated unhandled |
| 5 | `verify.py` `decompose()` (pre-fix) `failed()` callback | Returns `{"claims": []}`, indistinguishable from "no claims in this text" | Code inspection; confirmed by design (no counter existed) |
| 6 | `draft_chapter.py` `draft()` stage 5 | 100% of a chapter's editorial edits discarded in one real run (citation ids dropped/invented on every section) | `s1..s5 edit discarded` warnings, that run's log |
| 7 | `draft_chapter.py` `draft()` stages 4-7 (pre-fix) | Drafted/edited section text held only in memory until stage 7's final write | Code inspection: no intermediate `Path.write_text()` for `texts` before this session |

\#6 deserves a note: the mechanism (mechanical citation-delta check,
revert-on-mismatch) worked exactly as designed every time. No bad edit
reached the manuscript. The finding is about *yield*, not correctness:
`gpt-oss:20b` could not reliably rewrite ~800-1,500 words while preserving
10-20 exact bracketed ids verbatim, in this run. That is a capability
observation about this specific model on this specific task, not a bug to
patch.

---

## D. Recommended architecture

**No redesign.** The section-level evidence-packet architecture, the
mechanical evidence-integrity checks, and the verify/repair gate are already
the right shape and already match what a from-scratch design in this
document's brief would ask for. The fixes below are targeted corrections to
retry/error-classification logic and two new pieces of missing
observability/recoverability — nothing structural changed.

Two genuinely new pieces were added because they were genuinely missing:

- **Section checkpointing** (`book/_sections/chNN_{drafted,edited}.json`,
  written after stages 4 and 5respectively). A failure in stage 6 or 7 no
  longer discards the most expensive, LLM-heaviest work in the pipeline.
  `draft_chapter.py --resume` reuses a checkpoint *only* if its section
  titles match the current plan, so a stale checkpoint from an edited
  outline is never silently served up.
- **Per-call LLM telemetry** (`logs/llm_calls.jsonl`) — every chat call now
  logs stage, model, `think`, requested `max_tokens`, prompt/completion
  token counts, `done_reason`, and latency, on both success and failure.
  This is what made the actual root cause (item 2 above) findable instead of
  guessed at, and it stays in place for the next time something looks wrong.

---

## E. Model recommendation: do not switch, and here is the measurement

The brief was explicit not to assume a bigger model helps. Tested directly
rather than assumed:

| Model | Params | Quant | Disk size | GPU/CPU split (measured) |
|---|---|---|---|---|
| `gpt-oss:20b` (current) | 20.9B (MoE, ~3.6B active) | MXFP4 | 13GB | **100% GPU** |
| `qwen3.5:27b` | 27.8B (dense) | Q4_K_M | 17GB | **20% CPU / 80% GPU** |
| `gemma4:26b` | 25.8B (dense) | Q4_K_M | 18GB | **26% CPU / 74% GPU** |

Method: loaded each model with a real generation request via
`curl`/`requests`, read `ollama ps`'s `PROCESSOR` column mid-generation. This
machine's GPU is a 16GB card also used for the desktop (browser, games) —
neither alternative fits fully in VRAM the way `gpt-oss:20b` does. CPU-offloaded
layers are typically several times slower than GPU-resident ones; switching
would trade an *uncertain* instruction-following improvement for a *certain*
slowdown on a pipeline that already runs 1-2+ hours per chapter.

Recommendation: keep `gpt-oss:20b`. If more VRAM becomes available later,
`qwen3.5:27b` (dense, all parameters active per token) is worth re-testing
specifically on the editorial citation-preservation task, since dense models
often hold precise verbatim constraints more reliably than a MoE model with
~3.6B active parameters — but that is a hypothesis for a future test, not a
finding from this one (this session did not have the VRAM headroom to test
it fully-GPU-resident).

---

## F. Evidence architecture

Kept as-is, deliberately. The brief raised whether inline `[E12]` markers
should move to a structured `Claim{claim_id, text, evidence_ids[], ...}`
representation. That representation **already exists**, one stage later than
drafting: `verify.decompose()`/`entail()` produce exactly this shape
internally (`{id, text, kind, verdict, passage_ids, missing, conflict}`) for
every claim in every section, every time a chapter is verified. Moving the
*drafting* stage itself to structured claims (rather than inline markers in
prose) would be a materially larger, riskier change for a benefit that's
already delivered by the existing two-representation design: inline markers
because the final output is prose and a marker ties a specific clause to
specific evidence for a human reader; structured claims one stage later
because that's what verification actually needs to reason over. The
integrity gap that existed wasn't the representation — it was that the
decomposition stage could silently lose coverage (§C.5), now fixed by
tracking and reporting `undecomposed_words` explicitly.

---

## G. Chapter-writing specification (already substantially encoded)

`draft_chapter.py`'s `VOICE` and `GROUNDING` system-prompt constants already
require: third-person scholarly register; every substantive claim cited to
an `[E##]` id; `[GAP — not in sources]` in place of anything the evidence
doesn't support rather than general knowledge; explicit handling of
disagreeing sources ("say so and cite both"); a ban on naming anything
(person, place, text, date) not present in the supplied evidence.
`book_outline.py` carries per-chapter `scope` and `constraints` (e.g. the
existing ban on caste-ranking language and sati content) that the drafting
prompt already includes verbatim. This covers most of sections 8.A-8.C and
8.G-8.I of the original brief already.

Not currently encoded, worth adding if scholarly rigor needs to go further:
an explicit instruction distinguishing established fact / interpretation /
tradition-or-legend (brief §8.B) — the current prompt says "ground every
claim" but doesn't ask the model to *label* a claim's epistemic status. This
is a prompt addition, not an architecture change, and was not implemented in
this session (out of scope for a reliability diagnosis) — flagged here as a
concrete, low-risk next step if wanted.

---

## H. Files changed

- **`llm.py`** — `think` parameter threaded through `complete()`/`complete_json()`;
  per-call telemetry (`_log_call()`, `logs/llm_calls.jsonl`); `IncompleteResponse`
  exception (subclass of `Truncated`) distinguishing a real ceiling-hit from
  an incomplete-but-`done_reason:"stop"` response, with a fresh-retry path
  for the latter; `500` added to the transient-error classifier; `_OllamaResponse`/
  `_OpenRouterChat` now carry real `usage` (prompt/completion tokens, `done_reason`,
  thinking length) instead of discarding it; new `safe_workers()` clamping
  application-level concurrency to what the active backend can actually run
  concurrently (1 for Ollama, unchanged for OpenRouter).
- **`verify.py`** — `decompose()`/`entail()` use `think=True` (not `False`);
  `decompose()`'s `max_tokens` raised 8000→12000; failed-window word counts
  tracked and returned (`undecomposed_words`) instead of silently discarded;
  `Report` dataclass carries the new field; call sites tagged with `stage=`
  for the telemetry log; `decompose()`'s `workers=3` and `entail()`'s
  `workers=4` now pass through `safe_workers()`.
- **`draft_chapter.py`** — `plan_chapter()` moved from a raw `complete()` +
  fragile local regex parser to the shared, repair-capable `complete_json()`
  (local `_parse_json()` removed as dead code); citation regex (`_EID_RE`)
  widened to tolerate model formatting drift (`[^E14]`, `[ E20 ]`) without
  matching bare fabricated numbers; `save_sections()`/`load_sections()`
  checkpointing after stages 4 and 5; `--resume` CLI flag; `undecomposed_words`
  surfaced in both the per-section and chapter-level verify summary; call
  sites tagged for telemetry (`plan_chapter`, `draft_section`, `stitch_section`,
  `repair`, and `:continue`/`:repair` sub-tags); `draft()`'s `workers` argument
  now passes through `safe_workers()` once, at entry, covering every
  downstream `_parallel()`/`ThreadPoolExecutor` call in stages 4-6 without
  each needing its own fix.

---

## I. Tests performed

All against the real pipeline and real chapter-1 evidence, not synthetic
stand-ins, once the initial isolated calibration tests (which is what
produced the *wrong* first fix, §A.1 — a lesson in itself) were superseded:

1. **Model VRAM/CPU-split test** — `gpt-oss:20b`, `qwen3.5:27b`, `gemma4:26b`
   each loaded with a real generation request; `ollama ps` read mid-call.
   Result in §E.
2. **`think` level comparison on realistic decompose-shaped input** (105,
   237, 450-word passages) — `False` vs `'low'` vs `'medium'` vs `True`.
   `False` failed catastrophically at realistic length; `True` was most
   complete and stayed well under budget. This motivated the (incomplete,
   later corrected) `think=True` fix.
3. **`plan_chapter()`'s tight budget vs `think=True`** — reproduced live:
   `think=True` on a 2000-token budget truncated; reverted to the model
   default for this one call specifically. Not a universal `think=True`
   policy — sized per call.
4. **End-to-end repro with real drafted content** (`repro_decompose.py`,
   plans + drafts one real chapter-1 section with real inline citations,
   then runs `decompose()` on its actual ~500-word windows with full
   telemetry) — caught the real failure (§A.2) with exact token accounting,
   not a guess.
5. **Five full or partial `draft_chapter.py 1` runs** across this session,
   each fixing the specific failure the previous one surfaced:
   `think=False` -> `RuntimeError` (no repair path) -> `Truncated` (`think=True`
   on too-tight a budget) -> reached VERIFY cleanly -> (user-directed stop for
   this diagnosis) -> final validation run (in progress as this document was
   written; see the session record for its outcome).
6. **Static verification** — every edited module (`llm.py`, `verify.py`,
   `draft_chapter.py`) re-imported clean after each change; `IncompleteResponse`
   confirmed to be a `Truncated` subclass (so existing broad `except Truncated`
   handlers elsewhere are unaffected).

---

## J. Remaining risks

(One item originally logged here — VERIFY-stage concurrency — turned out to
be an active failure, not just a tuning nit, and was fixed; see below rather
than in this list.)

- **A specific `plan_chapter()` JSON-repair payload deterministically 500s.**
  Reproduced twice, on two separate runs: 4 identical failures the first
  time, then **5 identical failures** on a second, independent run (same
  ~5,400-char payload each time, 0/9 combined successes). This is not a
  transient blip — retrying the identical broken payload doesn't help, and
  originally cost 10+ minutes per occurrence once "500" became retryable
  (§A.4) without also being bounded. Mitigated, not root-caused: `complete_json()`'s
  malformed-JSON repair path now caps its own retry budget at 3 attempts
  (`min(attempts, 3)`, independent of the caller's requested budget) instead
  of inheriting up to 8 — turning a 10+ minute hang into a sub-minute clean
  failure that `draft_chapter.py`'s existing per-section fallback handles.
  The actual byte-level cause (something about this repair payload's shape —
  the embedded previous malformed response plus a fix instruction — that
  Ollama's server chokes on) was not isolated; if this specific failure mode
  keeps recurring, the next step is inspecting the exact payload bytes at
  the moment of failure, not further retry-tuning.
- **Editorial stitch yield on `gpt-oss:20b` is low** (0-40% of sections kept
  their edit across observed runs). Not unsafe (the mechanical check
  prevents bad edits from shipping), but it means the stage's token/time
  cost is not currently buying much polish on this model. Worth deciding
  whether to keep it as-is (safe, sometimes wasteful), narrow its scope
  (smaller, more constrained edits), or make it conditional on backend.
- **VRAM headroom is generically tight** on this shared 16GB desktop GPU
  regardless of any fix in this document — closing other GPU-heavy
  applications before a long drafting run remains the single biggest lever
  the user has, independent of software fixes.
- **`--resume` requires the user to know to pass it.** There is no automatic
  detection-and-resume on a fresh invocation; a crashed run's checkpoints sit
  in `book/_sections/` until someone chooses to reuse them.
- **`sources.py` bibliography gaps are unrelated and pre-existing** (7 of the
  corpus's sources, including both newly-added books, have no bibliography
  entry, so their endnotes fall back to raw filenames). Cosmetic, not a
  correctness issue, not addressed in this diagnosis.

---

## K. How to run it

```powershell
# Fresh chapter, all fixes active by default (no flags needed):
python draft_chapter.py 1

# If a previous attempt got through drafting/editorial but failed later
# (VERIFY, citation resolution), reuse that work instead of paying for it again:
python draft_chapter.py 1 --resume

# Inspect what actually happened, call by call, after any run:
#   logs/llm_calls.jsonl   -- every LLM call: stage, tokens in/out, done_reason, latency
#   book/_sections/ch01_drafted.json, ch01_edited.json  -- checkpointed section text
#   book/_runs/ch01_<id>.json                            -- the existing structured run record
```
