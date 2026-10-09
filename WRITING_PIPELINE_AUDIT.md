# Writing-pipeline audit

**Date:** 2026-09-24 · **Scope:** the existing chapter-drafting attempt on disk — `draft_chapter.py`, `make_evidence.py`, `retrieve.py`, `verify.py`, `sources.py`, `coherence.py`, `claims.py`, `validate_book.py`, `assemble_book.py`, and the drafts in `book/`.

**Verdict: keep the design, replace the implementation.** The existing pipeline is a serious piece of work whose architecture anticipates most of what the new spec asks for. It cannot run today, it reads from a knowledge base that no longer exists, and its drafts cannot be verified line-by-line by an editor. The new pipeline should inherit its ideas and be rebuilt on ChromaDB.

---

## 1. What exists

| component | what it does | state |
|---|---|---|
| `make_evidence.py` | builds a per-chapter evidence pack (`book/_evidence/chNN.json`) via `retrieve.py`'s hybrid funnel | **dead**: retrieves from the old `kb/store.sqlite` + `mistral-embed` vectors |
| `retrieve.py` | dense + BM25 + entity fusion, with a KB stamp so stale packs are refused | **dead** dense half; the stamp mechanism is worth keeping |
| `draft_chapter.py` (48 KB) | 7 stages: KB access → retrieval surfacing → evidence validation → section-by-section formulation → editorial refine → claim entailment verify/repair → citation resolution | **dead**: imports `mistralai`, which is uninstalled, against a quota that is gone |
| `verify.py` | decomposes sections into atomic claims, checks entailment against that section's own pack, keeps `contradicted` distinct from `unsupported`, cuts survivors to `[GAP — not in sources]` | **the best idea in the codebase**; reimplement |
| `sources.py` | resolves passage ids (E1, E2…) to numbered endnotes, audits invented ids | reimplement against chunk ids |
| `book/_runs/chNN_<id>.json` | per-run record: stages, timings, warnings, sources, KB stamp | good practice; keep |
| `book/chapter-*.md` | 9 drafts (chapters 1–7, 13, 14) | **artefacts of an older version**; see §3 |

## 2. Does it retrieve from the KB, or free-write?

**It retrieves.** This is not a model writing from memory: `make_evidence.py` pulls passages, `draft_chapter.py` refuses a stale pack, each section is written from its own evidence slice, and the system prompt forbids naming any dynasty, place or date not present in the evidence. I spot-checked claims from `chapter-07.md` against the current KB and they hold up — the courtyard with its dwarf compound wall, stone seats with backrests and four gateways is supported independently by Pande and by Patil 1952.

**But it retrieves from a knowledge base that no longer exists.** The run record for chapter 1 stamps the KB as:

```
"kb": {"built_at": "2026-08-09", "count": 9467, "model": "mistral-embed", "hash": "3b26ecee9433d2a4"}
```

That is the dead store: 9,467 chunks, embedded with an API whose quota is gone. Nothing in the writing pipeline mentions ChromaDB — `grep -l chroma` across `draft_chapter.py`, `make_evidence.py`, `retrieve.py`, `verify.py`, `sources.py` returns **zero files**. It also predates every quality signal the KB now carries: `epistemic_status`, `is_quotable`, `chapter_buckets`, `corroboration_count`, the five scores, the claims register. None are consumed.

## 3. Where it breaks down

**a. It cannot run at all.** `import mistralai` → `ModuleNotFoundError`. Every model-driven stage (formulation, editorial, entailment verification) is inert.

**b. The drafts on disk are not the output of the current code.** The newest draft is dated 2026-08-05; the only run record is 2026-08-12. The drafts were produced by an earlier version, so they carry none of the guarantees the current stages claim.

**c. No resolvable provenance — the disqualifying defect.** Across all nine drafts there are **zero** KB chunk ids. Citations look like this:

> [49] Singh, "A serpentine scimitar of letters," on the foundation record of saṃvat 1137 (Singh 2019, Zenodo)…

An editor cannot resolve that to a passage without re-searching the corpus by hand. And the detail is wrong: the registry records that paper as **2023**, verified from the file. A plausible-looking year and venue attached to a real source is exactly the failure mode the new spec forbids.

**d. Length control is poor.** Target ~4,000 words:

| draft | words |
|---|--:|
| chapter-01 | 9,967 (2.5×) |
| chapter-07 | 5,448 |
| chapter-14 | 3,327 |

**e. The evidence packs were thin, and the pipeline said so.** The chapter-1 run warned: `11 duplicate passage(s) in the pack`, three editorial edits discarded for dropping citations, and — most telling — **`127 claim(s) still unsupported after repair; cut to [GAP — not in sources]`**. The machinery caught the problem honestly. But the shipped `chapter-01.md` contains only 6 GAP markers, because it came from the earlier version: the honest failure never reached the page.

**f. Chapter scheme mismatch.** `book_outline.CHAPTERS` has **19** chapters under the title "The Rising Lord"; the KB is bucketed into the current **C1–C16 + AF**. `chapter-07.md` ("An Archive in Stone: Inscriptions, Conquest, and Afterlife") straddles what are now C8 and C14. Old drafts cannot be mapped onto the new buckets one-to-one.

**g. No `is_quotable` discipline.** The KB now flags 455 AI-reworded chunks and the 85 `needs_recheck` pages of the Rājamārtaṇḍa. The old pipeline has no such concept, so it would quote reworded text verbatim as if it were a source.

**h. Human checkpoints are optional.** `--stage plan` can stop after planning, but nothing *requires* a human to approve an outline, and there is no per-chapter state file recording where a chapter stands.

## 4. What is salvageable

Worth carrying into the new pipeline, as design rather than code:

1. **The entailment gate** (`verify.py`): decompose a drafted section into atomic claims, check each against that section's evidence, and cut what fails to an explicit gap marker. Keeping `contradicted` separate from `unsupported` is right.
2. **The staleness stamp**: a draft built against an older KB should refuse to run, not silently disagree with the store.
3. **Discarding an edit that drops a citation** — the editorial pass may improve prose, never quietly remove provenance.
4. **Per-run records** with stages, warnings and timings.
5. **Section-by-section drafting from its own evidence slice**, which is why length was additive rather than capped.
6. **The prose itself is a useful register sample.** The existing chapters read like serious trade history; `STYLE_GUIDE.md` should codify that voice rather than invent a new one.

## 5. What must be replaced

| must change | why |
|---|---|
| retrieval layer → `kb3_chroma_query.py` | the old store's dense path is dead; Chroma carries buckets, quotability and scores |
| the 19-chapter outline → C1–C16 + AF | the KB is bucketed to the new scheme |
| endnote-only citations → `[src: chunk_id]` resolving to a provenance appendix | an editor must verify a line without re-searching |
| no quotability rule → `is_quotable=false` may be used as a lead, never quoted | 455 AI-reworded chunks are in the corpus |
| no epistemic discipline → assert `factual`, attribute `inference`, never assert `speculation` | the KB records status per chunk; the drafter must honour it |
| optional stops → **gated** human review at outline and full draft, with a state file | the spec requires checkpoints that are not optional |
| flat `book/` output → per-chapter folder with `research.md`, `outline.md`, `draft-vN.md`, `qa_review.md`, `handoff/` | inspectable and resumable |
| model dependency on a dead API | the drafting model must be whatever is available; retrieval and verification stay deterministic and local |

## 6. One caveat about the rebuild

The old pipeline's model-driven stages ran on a Mistral API that no longer has quota, and this machine has no local model capable of writing publishable narrative history. The rebuilt pipeline is therefore built so that **retrieval, evidence assembly, gap analysis, verification and packaging are deterministic and local**, while the drafting and editorial-review steps are explicit, inspectable prompts that can be executed by whatever model the team has — including me, in-session, for the worked example. That keeps the guarantees (every sentence traceable, nothing quoted that may not be quoted) independent of which model writes the prose.
