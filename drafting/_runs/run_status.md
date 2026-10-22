## Run status & test report

### Retrieval

- Queries/passes run: **394**: 13 units × 25 phrase passes = 325, plus 69 hypothetical-answer queries (one per sub-topic). Embedding 0.77 s, scoring 5.99 s, total 7.64 s, in memory.
- Union of chunks retrieved (global top-40/80+ and per-book top-5 with deepening): **6062** of 6,813.
- Pre-filtered out (below floor, or a duplicate twin): **966**. Every drop is logged with its reason and score in `_runs/prefilter_log.jsonl`.
- To read: **5096**, plus 77 chunks read in early packets built before the per-query deepening fix.
- Adaptive deepening: 552 global extensions; 849 per-book extensions (`_runs/deepening_log.jsonl`).

| Unit | Retrieved | Pre-filtered out | Duplicate twins | To read | Global deepenings | Book deepenings |
|---|---|---|---|---|---|---|
| C01 | 2078 | 485 | 29 | 1564 | 17 | 46 |
| C02 | 1900 | 1050 | 8 | 842 | 7 | 37 |
| C03 | 1894 | 429 | 35 | 1430 | 10 | 39 |
| C04 | 2642 | 472 | 31 | 2139 | 27 | 81 |
| C05 | 2807 | 161 | 79 | 2567 | 24 | 116 |
| C06 | 2544 | 361 | 46 | 2137 | 19 | 55 |
| C07 | 1790 | 437 | 38 | 1315 | 15 | 40 |
| C08 | 2155 | 501 | 47 | 1607 | 8 | 32 |
| C09 | 2058 | 1332 | 11 | 715 | 1 | 22 |
| C10 | 2048 | 654 | 27 | 1367 | 10 | 37 |
| C11 | 1811 | 587 | 27 | 1197 | 11 | 31 |
| C12 | 2133 | 1475 | 15 | 643 | 1 | 34 |
| C13 | 1899 | 1359 | 3 | 537 | 3 | 35 |

### Calibration

- Calibrated on all **1527** Chapter 1 chunks that were hand-judged in the pilot (125 kept).
- **Pre-filter floor:** max dense cosine ≥ **0.36**, or global fused rank ≤ 10. The lowest kept chunk scored 0.3802; the floor sits 0.02 below it. Keeps lost at the floor: **0**.
- **Deepening "relevant":** dense ≥ **0.5** for the query in question: the lowest score at which at least 30% of hand-judged chunks were kept.

| Dense band | Judged | Kept |
|---|---|---|
| 0.00-0.30 | 152 | 0 |
| 0.30-0.36 | 275 | 0 |
| 0.36-0.42 | 399 | 8 |
| 0.42-0.48 | 347 | 22 |
| 0.48-1.00 | 354 | 95 |

Stratified sample, 12 per band and 60 in all: `_runs/calibration.json` → `sample`. It contains 5 hand-kept chunks, all above the floor.

### Judging

- Packets: 221 / 221, all passing `check_judgments.py`.
- Chunks read and judged by subagents: **5173**. Kept **2103**, rejected **3070**. Every decision and reason is in `_runs/judgments/*.jsonl` and `_runs/decisions.json`.
- Chapter 1 pilot: 1527 chunks hand-judged (125 kept). Its 210 items are carried over and re-verified.
- Items: **3717** verified; 1 failed verification and were excluded (`_runs/assembly_failures.jsonl`); 0 exact duplicates dropped.
- **Verification pass rate: 99.97%**. Each quote is checked verbatim against the chunk and the source Markdown, and its page is taken from the `<!-- page N -->` marker in force.
- Items per unit: C01 219, C02 159, C03 156, C04 682, C05 982, C06 400, C07 346, C08 269, C09 75, C10 176, C11 109, C12 77, C13 67

### 15 spot-checks (by hand, against the source file)

| Item | Quote verbatim at cited page? | Page correct? | Relevance sound? | Note |
|---|---|---|---|---|
| C03-MADHYABHARAT-002 | yes | yes | yes | Vidiśā under Aśoka; direct for C03-S2 |
| C05-BHOJDEV-HI-002 | yes | yes | weak | door terminology (Samarāṅgaṇa via Hindi); generic C05-S3 context; gloss faithful |
| C05-SAMAR-2-008 | yes | yes | weak | generic Haṃsa prāsāda prescription; ⚠ old OCR |
| C05-SAMAR-2-046 | yes | yes | weak | layout of entourage abodes around a king's palace; closer to town planning (C04-S5/C07) than C05-S6 |
| C07-GEOHER-006 | yes | yes | yes | 1400 m dry-stone fortification wall; direct C07-S1 |
| C11-JAGTA-EN-036 | yes | yes | yes | author's view on neglect; page marked approximate as required |
| C03-GAZ-031 | yes | yes | yes | quote was cut at 'A.' by the sentence splitter; slicer fixed to carry 'A. D.', now complete |
| C12-JAGTA-HI-012 | yes | yes | yes | gloss faithful (source says महाराणा) |
| C04-GANGULY-108 | yes | yes | yes | Udayapura in Ganguly's list of towns of the period; quote includes the source's HTML table |
| C13-JAGTA-EN-011 | yes | yes | weak | rhetorical; serves the Afterword only loosely |
| C06-JAGTA-EN-004 | yes | yes | yes | VS 1137 = 30 March 1080 inscription; translator's bracket note is in the source |
| C06-MADHYABHARAT-006 | yes | yes | yes | general description of dated sati-stone inscriptions; contextual |
| C06-BHOJDEV-HI-017 | yes | yes | yes | Bhoja's works and their commentaries; gloss faithful |
| C05-KRAM-2-050 | yes | yes | weak | generic stance classification (samabhaṅga etc.) |
| C08-TEMPLE-ECON-040 | yes | yes | weak | generic temple-craft statement; contextual only as required |

Result: 15/15 verbatim at the cited page. One quote (C03-GAZ-031) had been cut at 'A.' by the sentence splitter; the slicer was fixed and every item re-sliced. Relevance: 9/15 clearly relevant; 6/15 weak (generic contextual background, acceptable under the rubric). **Implication:** read contextual items as background, not evidence; the direct items carry the chapters.

### Incomplete flags

**None.** No cap stopped retrieval, deepening or reading: per-book deepening ran until relevance dropped or the book ran out, and global deepening ran until the last ten ranks held no relevant chunk.

### QC findings

1. **Deepening rule fixed mid-run.** The first version judged "relevant" by a chunk's best score across *all* of a unit's queries. This pushed global depth past 2,000 ranks for some passes. It was changed to per-query relevance: each query's own dense score ≥ 0.50, or its top-10. That cut 1,020 chunks from the reading set. The 77 such chunks already in packets P0001–P0030 were read anyway and are flagged `extra` in `candidates.jsonl`; their items stay in the map.
2. **Chapter 1 pilot under-kept the English translation.** In the pilot, several *Jagta Hua Kasba* English chunks were bulk-rejected although relevant (e.g. 5029e6cf, 323b642e, eb80b269); their Hindi twins were kept instead. In this run those chunks were re-read for Chapters 2–13.
3. **`bhoja-paramara-and-his-times.md` has no `<!-- page -->` markers.** All its items are cited as `[page not recorded]` with the section heading. No page numbers were inferred.
4. **Transient checker crash.** While `candidates.jsonl` was being rewritten, `check_judgments.py` briefly raised KeyErrors. One judge rejected a valid item to work around it (chunk 2327639630, P0025). The item was restored by hand (C05-S6, span [8,8]), and the judge prompt now forbids such workarounds.
5. **Session-limit interruption.** All 20 judges died at once at 91/221 packets (HTTP 429). Two partial files (P0109, P0115) failed the checker and were re-judged from scratch. Nothing was lost, because a packet only counts once its file passes the checker.
6. **Rajasthan check.** Every item whose quote or note mentions Mewar, Rana, Rajasthan, Rajputana, Pichola, Sisodia or Chittor was reviewed by hand. That was 46 items in the final set, all reviewed. All are legitimate context: Paramāra branches and conquests, the spread of the Bhūmija style, Jain and Śaiva parallels, administrative history, and the author's own contrast between the two Udaipurs. None uses Udaipur, Rajasthan as evidence for Udaypur. One C01 item records that a cited "Udaipur Praśasti" edition was published by the Mewar State Press; its note flags this as a caution.
7. **Judging granularity varies.** Some judges split chunks into many small items (up to 86 items from 25 chunks); others kept only the strongest sentence. Both are valid under the rubric. Overlapping quotes from the same book were merged automatically (see `overlapping_items_merged`).
8. **Targeted checks.** 10 more items were checked by hand from the riskiest groups (`_runs/targeted_sample.json`). All quotes are verbatim and every claim value matches its quote.
   - Three Hindi glosses were checked: all faithful, including one on damaged Yogasūtra OCR.
   - Three `[page not recorded]` items (bhoja-paramara) were checked: correctly unpaged, with the section heading given.
   - Two claim-tagged items were checked: the values match the quotes.
   - Two Samarāṅgaṇa items were checked: correctly ⚠-flagged, but generic.
   - One relevance *note* (C04-BHOJA-TIMES-023) names the Ā'īn-i Akbarī as the source of a statement whose quoted span does not name it. The attribution comes from the footnote apparatus around the span. Notes are written by the judges and should be treated as aids, not evidence. Only the quote is evidence.
9. **Two missing glosses added.** Two Samarāṅgaṇa colophon items had Sanskrit with no gloss. Glosses labelled [my translation] were added by the orchestrator, with the chapter titles checked against the volume's contents list.
10. **Three mis-keyed claim tags removed** (`_runs/claim_overrides.json`) after a hand review of all 340 claim-tagged items.


### Folder check (report only; nothing moved)

- **`samarangana-sutradhara.md`** (the Samarāṅgaṇa re-OCR, 3,804,459 bytes, modified 2026-10-12 18:10) is in **both** `Udaipur Books Markdown files/` and `Udaypur Reference Markdown Files/`. An identical copy is kept as `backups/2026-10-13_samarangana_reocr/samarangana-sutradhara_ASSEMBLED.md`.
  - The legacy orphan is at `backups/2026-10-13_samarangana_reocr/samarangana-sutradhara_legacy_orphan.md` (2026-10-12 17:11).
  - The old two-volume OCR (`Samrangana Sutradhar Vol 1.md`, `Samarangan Vol 2 (a)_combined.md`, 2026-08-18) was retired to `backups/2026-10-13_samarangana_reocr/`. **The database still indexes these old volumes**; the re-OCR has not been ingested. Every Samarāṅgaṇa item is therefore marked ⚠ "old OCR, pending re-OCR", is verified against the retired copies, and must be re-verified against the re-OCR before use.
- **Yogasūtra:** the re-OCR is the active `Udaipur Books Markdown files/patanjala-yogasutra-rajamartanda-bhoja.md` (472,922 bytes, 2026-10-12 16:06), identical to `backups/2026-10-12_ocr_pagerefs/yogasutra_reocr_final.md`. The old OCR is `Udaypur Reference Markdown Files/patanjala-yogasutra-rajamartanda-bhoja.md` (468,836 bytes, 2026-10-09 11:24).


### Time and tokens

- Retrieval (all 13 units, 394 queries, in memory): ≈ 8 s per run (embedding 0.7–4.6 s, scoring ≈ 6 s)
- Judging, wall clock: judgment files written between 08:38 and 09:05 on 13 Oct 2026 (file timestamps; the pauses for the two account interruptions are not counted). Individual 6-packet batches took 1.5–10 min.
- Judging, subagent tokens: ≈ 10–11 M in total. The ~45 subagent runs, including runs cut off by the session-limit and credit interruptions, reported 108k–380k tokens each, ≈ 240k on average.
- Corpus text read by judges: 5,173 chunks ≈ 3.9 M tokens of chunk text (sentence-numbered packets)
- Assembly + verification + rendering: seconds per run (scripted, no model calls)
- Chapter 1 pilot (before this run): 1,527 chunks hand-judged in the earlier session
