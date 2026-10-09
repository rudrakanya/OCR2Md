# KB Rebuild — Stage 2

**Date:** 2026-09-22 · **Builds on:** `KB_AUDIT.md` (Stage 1) · **Auto-generated tallies:** `kb3/STAGE2_REPORT.md` · **Retrieval check:** `kb3/eval_results.md`

**Status: built and usable, with the semantic (dense) layer incomplete.**
- The embedding run was stopped by the system for low memory at 4,096 of 14,514 chunks. Those vectors are saved; resuming continues from there.
- The current build therefore scores chapter relevance from seed terms + source priors only, and runs with every safeguard that assumption needs.
- Nothing in the old store (`kb/store.sqlite`) was changed or deleted.

---

## 1. Findings that affect the book (read first)

**1. "Nephew" is contradicted by the primary evidence** (claims register K1). The earlier outline commits to Udayāditya as Bhoja's *nephew through a junior branch*. No primary witness in the corpus calls him a nephew; only Singh 1984 does. The three inscriptions quoted in the corpus say:
- **Udaipur praśasti:** "*bandhu*" (kinsman); his father is Gyata/Jñāta, not Sindhurāja.
- **Jainad inscription of his son Jagaddeva:** Bhoja is Jagaddeva's "*pitṛvya*".
- **Dongargaon inscription:** Udayāditya is Bhoja's "*bhrātā*".

The reading that fits all three is a **kinsman from a collateral (junior) branch, styled "brother"**. The junior-branch part of your wording holds; "nephew" does not.
- The Singh chunk is flagged `contested` with lowered credibility.
- `AI-0001` sets out the reconciliation with citations.

**2. The reign span "1070–1093" is one of two defensible readings** (K2). A dated Udaipur inscription of VS 1116 (1059 CE) shows Udayāditya already ruling at Udaypur. The same year the Panhera inscription is issued under Jayasiṃha as sovereign. Suggested wording: *"ruled Malwa c. 1070–93; already active at Udaypur by 1059."* Neither side is penalised. `AI-0003` gives the inference that Udaypur was his base before accession, at confidence 0.6.

**3. Temple dates** (K3). Begun by 1059 (VS 1116); flagstaff/consecration 30 March 1080 (VS 1137 Vaiśākha sudi 7), so at least 21 years (`AI-0002`).
- Singh 2023's "built around 1080" dates the consecration; it doesn't dispute 1059.
- Tiwari's statement that the 1080 record is Udaypur's *oldest* inscription is contradicted by the VS 1116 inscription, which Tiwari himself reports later in the book. Credibility is lowered for that claim only.
- Ganguly says the flagstaff was *repaired* in 1080, where everyone else says *erected*. Left open: check the inscription text.

**4. The mosque behind the temple is Tughluq-period, AH 737–739 / 1336–38 CE** (K4, `AI-0004`).
- Beglar's Aurangzeb story is marked `superseded_by` the mosque's own inscriptions. It is kept and tagged folklore for C13, not quarantined (rule C6).
- Aurangzeb's 1682 conversion of the Vijay Mandir at **Vidisha** is a different building and is not part of this dispute.

**5. The agnikula origin** (K7, `AI-0005`). The Paramāras' own inscriptions attest the *belief*. Parmar 2025, and INTACH's "confirmed by the Udaypur prashasti", present it as validated *history*; those chunks are flagged `contradicted`. Narrations of the legend are kept and tagged folklore.

**6. Open, no penalty either way:** Bhoja's regnal dates (K5; c. 999/1010 to 1050/1055, from different anchor records) and the date of the Udayasamudra tank (K6; 1059 vs 1080, neither from an inscription on the tank).

## 2. How contradictions are handled (spec B3, C4, D)

- **`kb3/claims_register.yaml`** holds 7 contested claims and 67 chunk entries, with the evidence note, search patterns and a disposition per position:
  - `supported`
  - `open`: contradiction recorded both ways, no penalty
  - `contradicted`: −0.25 claim credibility
  - `superseded`: also sets `superseded_by`
- **The register is protected against drift.** Every entry is pinned to a verbatim snippet. The build refuses to run if a snippet no longer matches its chunk, so a re-chunk can't silently re-point a contradiction.
- **Contradiction is information, not a penalty, unless the other side is stronger evidence.** 57 chunks carry `contradiction_ids` (310 links in `kb3/logs/contradiction.jsonl`); only the `contradicted` and `superseded` positions lose credibility.
- **Superseded folklore is retained.** Pande's Aurangzeb legend is superseded but active, tagged folklore.
- **Limit: this is a curated register, not an automatic contradiction detector.** It covers the disputes I found by searching the corpus for the book's core claims. Add entries as drafting surfaces new ones; the format is documented in the file header.

## 3. What was built

| file | purpose |
|---|---|
| `stage2_build.py` | the build: metadata, scores, relevance, buckets, dedup, corroboration, contradictions, quarantine |
| `kb3/kb_active.sqlite` | **the only store retrieval may open**. FTS5 with Devanagari and diacritic folding; one row per chunk carrying every spec-A field |
| `kb3/kb_quarantine.sqlite` | the archive. A separate file that no retrieval code names, so quarantined chunks are structurally unreachable (spec E) |
| `kb3_query.py` | retrieval for drafting: evidence/prose profiles, chapter scoping, flags, provenance, `--json` |
| `kb3_quarantine.py` | list / show / restore / quarantine; decisions persist across rebuilds via `kb3/quarantine_overrides.jsonl` |
| `kb3_embed.py` | resumable bge-m3 int8 embedder |
| `kb3/chapters.yaml` | chapter profiles: seed terms, preferred types, epistemic tolerance, anchors, and the relevance formula |
| `kb3/source_scores.yaml` | source reliability with a stated basis for each source, plus chapter priors (**review these**) |
| `kb3/claims_register.yaml` | contested claims (§2) |
| `kb3/speculation_adjudication.yaml` | 288 hand-read speculation candidates (§5) |
| `kb3/derived_inferences.yaml` | 6 AI-derived inference chunks citing their supports (spec C8) |
| `kb3/logs/*.jsonl` | dedup (6,726), corroboration (446), contradiction (310), quarantine (3,390), status overrides (336), scoring params, build |
| `kb3/review_queue.csv` | 4,102 low-relevance chunks for human review (spec C1) |

**Schema (spec A).** Each active chunk carries:
- identity and dating: `title`, `author`, `publication_date` (+confidence), `event_date` (+`event_year_min/max`, `date_confidence`, `event_date_basis`)
- relevance: `chapter_scores` (all 17 chapters), `chapter_buckets` (`C7` or `C8:admitted`), `relevance_tags`, `entities`
- evidence links: `corroboration_ids`, `corroboration_count`, `contradiction_ids`, `contested_claims`, `duplicate_of`, `superseded_by`
- quarantine: `is_quarantined`, `quarantine_reason`, `review_status`
- scores and their stated bases: `score_primacy`, `score_source_reliability`, `score_claim_credibility`, `score_recency`
- Stage 1 fields and full provenance

**Scores are stored separately and combined only in `kb3_query.py`** (spec B):

| score | how it is set |
|---|---|
| primacy | primary 1.0, field 0.9, secondary 0.6, tertiary 0.3, contextual 0.2. A field source retelling pre-modern history drops to 0.5; secondary text quoting primary script rises to 0.7. |
| source reliability | per source, with a written basis in `source_scores.yaml`. Never reads a chunk. |
| claim credibility | base by status. −0.20 for AI-restated text, −0.10 for OCR damage, −0.10 for no locator, −0.25 if contradicted by stronger evidence. Capped at 0.6 for mythic register. **Single-source is never penalised.** |
| recency | secondary and tertiary tiers only, and only as a tie-breaker at 2 decimals. Primary and field chunks sort ahead of any tie. |

**Relevance.** Your spec was cut off at the relevance formula, so this one is mine; it's documented at the top of `chapters.yaml`:

  r(c,k) = 0.40·lexical + 0.45·dense + 0.15·prior

- **lexical:** seed terms weighted by inverse document frequency, with saturation
- **dense:** bge-m3 cosine to the chapter description, calibrated per chapter
- **prior:** the source's chapter prior
- **Bucket rule:** r ≥ 0.30 and the chunk's status is within the chapter's tolerance, plus `anchor` rules where a chapter is defined by a source (C16 ← *Jagta Hua Kasba* observation; AF ← field-source opinion).
- **Current mode:** without vectors, the lexical and prior terms are reweighted to 0.73 / 0.27.

## 4. Tallies (current build)

- **Active 15,799 · quarantined 3,390**:

| quarantine reason | chunks |
|---|--:|
| non-claim apparatus / garbage / figure lists | 2,275 |
| Temple_Economics below every chapter threshold | 1,090 |
| orphans of the deleted Pande summary (from the old store) | 25 |

- **Nothing was quarantined as speculation.** Details in §5.
- ***Jagta Hua Kasba*:** all 1,246 chunks active. None were quarantined on relevance, speculation or opinion.
- **Status (active, claim-bearing):** factual 13,471 · inference 1,312 · observation 847 · speculation 169.
- **Event dating:** dated 958 · approximate 3,686 · **undated-flagged 11,155 (70%)**. That's an honest figure: most scholarship discusses undated matters, and no date was invented.
- **Dedup:** 393 chunks linked `duplicate_of`; nothing removed or deranked.

| duplicate link | chunks |
|---|--:|
| Patil composites → Patil 1952 | 180 |
| Adhikari repeating its own text (an OCR/extraction defect in that file) | 158 |
| smaller internal repeats | ~40 |
| INTACH 2022 passages copied from Kramrisch vol. 2 | 5 |

  The last row means INTACH and Kramrisch are not independent on those points, and they now count once.
- **Corroboration** is counted by independent work, with duplicate clusters counted once. Only 100 chunks have any detected corroboration, because the detectors running now need dated entity-year matches or register membership. The semantic detector (cosine ≥ 0.85 plus a shared named entity) needs the full vectors. Until then, `single_source` means "none detected", not "none exists".

## 5. Speculation: adjudicated, not auto-quarantined

Stage 1's own validation measured the lexicon's speculation labels as right only 2 times in 9, so I read all 288 strongest candidates (`kb3/speculation_adjudication.yaml`):

| verdict | chunks | what they were |
|---|--:|---|
| inference | 158 | scholars' hedges anchored in evidence they are discussing |
| factual | 76 | perceptual "seems", legal "could not", narrative, reported belief |
| observation | 17 | on-site description with an interpretive hedge |
| speculation | **36** | honest, clearly flagged guesses; kept and labelled |
| non-claim | 1 | OCR garbage |

**None met your quarantine bar** (rule C6: genuinely unsupported conjecture, or for Tiwari, an unsupported claim *presented as established history*).
- The Tiwari conjectures (Naravarman living at Udaypur, Bhoja visiting) are openly hedged, so they are kept.
- **Correction to `KB_AUDIT.md`:** its headline speculation-as-fact example (old #961, now `intach-2022-udaypur-00365`: Shiva worshipped only outside settlements before the 6th c. BCE) carries a footnote. It is doubtful but traceable, so it is kept, tagged `verify_before_use`.

## 6. Other fixes made in Stage 2

- **Udaipur/Udaypur (audit D9):** entity aliasing at sentence level; "Udaipur" is excluded when the same sentence mentions Rajasthan, Mewar, Ahar or Guhila. Tiwari now surfaces for Udaypur queries.
- **Footnote rescue:** 11 footnote blocks that Stage 1 filed as apparatus actually carry argument, including Ganguly's notes on Paramāra origins. They are claim-bearing again.
- **Figure lists:** 36 caption runs moved to non-claim.
- **Seed-term calibration:**
  - Generic terms ("now", "road", "tree", "Hindi", "should be") had put 373 śāstra chunks into C16. Removed.
  - The town's name had pulled 323 Hindi Tiwari chunks into C6. Removed from C6's seeds.
  - Temple_Economics is only ever "admitted", with a higher bar.

## 7. Retrieval check vs. the Stage 1 audit (`kb3/eval_results.md`)

| chapter | Stage 1 (old store) | Stage 2 (lexical-only) |
|---|---|---|
| C8 | serpentine paper absent; AI-regenerated text on top | serpentine paper at ranks 1–3 |
| C16 | 0 Tiwari | Tiwari + INTACH field observation |
| C13 | 1 good legend | Bhrangarajpur legend first; folklore-tagged field material |
| C15 | Temple_Economics in top 3 | INTACH/Cunningham on top, no Temple_Economics |
| C9 | apparatus list first | stepwells and fortifications, all on-site observation |
| C7 | orphan summary #1, garbage #4 | no orphans or garbage, but footnotes and caption runs still rank high. **Weakest chapter until the dense layer lands.** |
| C6, C3, C2 | good | good |

## 8. Embedding: what happened and what's left

- **bf16 was the wrong choice for this CPU.** bf16 bge-m3 ran at 3.7–7 chunks/s on ~1 core, because the i7-1185G7 has no native bf16. On your go-ahead I switched to int8 with a skip list of 4,167 chunks.
- **int8 gained about 1.5×, not the 3–4× I estimated.** It still used only ~1.5 cores, and swap was in play (~3 GB free).
- **The system then stopped the run for low memory** at 4,096 of 14,514 chunks, while the session was idle. The saved vectors are intact, and I have not restarted it.
- **To finish:**
  1. `python kb3_embed.py` (resumes; roughly 45–60 min on this machine, ideally with other apps closed)
  2. `python stage2_build.py` (dense relevance, the semantic corroboration detector, and Tiwari EN↔HI translation linking all switch on automatically)
  3. `python kb3/eval_chapter_queries.py --dense > kb3/eval_results.md`

## 9. Decisions still yours

1. **Resume the embedding** (§8), preferably with other applications closed.
2. **Review `kb3/source_scores.yaml`.** The reliability numbers are my judgements with stated bases.
3. **The outline's "nephew" wording** (§1.1) and reign span (§1.2).
4. **The rest of the spec:** the relevance formula (§F onward) and the LOGGING section never arrived. I built both to my own design (§3, `kb3/logs/`); send yours if they differ.
5. **Still open from Stage 1:** restore the deleted Pande summary (its 25 chunks are in quarantine and restorable with `kb3_quarantine.py restore`), and the *Art of Paramaras* OCR.
