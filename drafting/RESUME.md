# RESUME: Udaypur drafting evidence map (handoff, 2026-10-13)

> **Status: COMPLETE.** All 221 packets are judged. The map is assembled, verified (99.97%) and rendered; see `drafting/_master.md`. The rest of this file is the historical handoff, kept as a record of the run. To regenerate the outputs: `assemble.py` → `make_status.py` → `render.py`.

State when the previous session stopped: all 20 judging subagents died together at the account's session limit (HTTP 429). Nothing was lost. Every packet that passes the checker is final.

## Rules (non-negotiable, from the user)
- Query only `udaypur_corpus_openai_large`. Treat `chroma_db/`, the corpus folders and `books_manifest.yaml` as read-only. No git commit or push.
- Never fabricate. Quotes are verbatim; the scripts slice them from stored chunks. Never invent or interpolate pages: use "scan p. N", "[page not recorded]", or "≈ Hindi-original scan p. N (derived)" for Jagta EN.
- Mark every Samarāṅgaṇa item ⚠ "old OCR, pending re-OCR". The Yogasūtra carries an ⚠ OCR warning. Temple Economics is contextual only; its Udaipur is in Rajasthan.
- Cite the Pande monograph copy only; the twin copy was dropped before reading.
- Add no historical claims of your own. Present conflicts side by side, unresolved. Each item has one home unit, with xrefs elsewhere.
- Glosses are labelled "[my translation]".
- Required in the final report: a "Run status & test report" in `_master.md`, and the folder check (below).

## Pipeline (all scripts in `drafting/_tools/`, run from the project root with `python -I`)

| Step | Script | Status |
|---|---|---|
| Queries: 13 units × 25 passes + 69 hypothetical-answer queries = 394 | `make_queries.py` → `_runs/queries.jsonl`, `_runs/units.json` | done |
| Corpus snapshot, in memory (6,813 chunks) | `engine.py` → `_tools/corpus_snapshot.npz`, `corpus_meta.pkl` | done |
| Calibration on the 1,527 hand-judged C01 chunks: floor dense ≥ 0.36 (0 of 125 keeps lost); deepening "relevant" dense ≥ 0.50 per query; rescue = global rank ≤ 10 | `calibrate.py` → `_runs/calibration.json` (includes the 60-chunk stratified sample) | done |
| Retrieval + per-query adaptive deepening + pre-filter (8 s) | `retrieve_all.py` → `retrieval_log`, `deepening_log`, `prefilter_log`, `candidates.jsonl`, `retrieval_summary.json` | done: 5,096 to read, plus 77 "extra" chunks in early packets built before the per-query deepening fix |
| Packets (221 × ~25 chunks, numbered sentences) | `build_packets.py` → `_runs/packets/` (P0001–P0030 frozen) | done |
| **Judging (subagents)** | rubric `_runs/rubric.md`; output `_runs/judgments/<P>.jsonl`; validator `check_judgments.py <P>` | **91 / 221 done. 130 to do.** |
| Assembly: slice spans, pin pages, verify | `assemble.py` → `drafting/_evidence_log.jsonl`, `_runs/judgment_summary.json`, `assembly_failures.jsonl` | rerun at the end |
| Render 13 chapters + `_master.md` | `render.py` (or `--by subtopic`) | rerun at the end |

## Next steps
1. `python -I drafting/_tools/packet_status.py --batches 6` lists the to-do packets in groups of 6. Partial files (P0109, P0115) are simply overwritten.
2. Launch one judging subagent per group, as many in parallel as the concurrency cap allows (it was 20; the session limit was the real constraint, so consider ~8–10 at a time). Use model `sonnet`, `general-purpose`, run in background, with the prompt below. As each one finishes, launch the next group. Report status every ~25%.
3. Re-judge chunk `2327639630` in P0025. A transient checker crash made the judge reject a valid C05-S6 item: a hall without an alinda is "praiseworthy in a devālaya". See `_runs/qc_followups.jsonl`.
4. `python -I drafting/_tools/check_judgments.py --all` must print "221 of 221 packets OK".
5. `python -I drafting/_tools/assemble.py`, then check the verification pass rate and `assembly_failures.jsonl`. Fix or drop the failures and log them.
6. Write `drafting/_runs/run_status.md`; `render.py` appends it to `_master.md`. It must contain:
   - passes run (394);
   - chunks retrieved, pre-filtered, read, kept and rejected (`retrieval_summary.json`, `judgment_summary.json`);
   - the verification pass rate;
   - the calibration (threshold, band table, 60-chunk sample);
   - **15 spot-checks**: pick 15 random items from `_evidence_log.jsonl` and check each by hand against the source file at the cited page, for quote, page and relevance;
   - "incomplete" flags: none expected, since no caps were used;
   - QC findings (below);
   - the folder check (below);
   - time and token use.
7. `python -I drafting/_tools/render.py`, then give the user the final report:
   - the path to `_master.md`;
   - items per unit;
   - the verification pass rate;
   - the weakest units and their gaps;
   - books that went unused;
   - total time and tokens;
   - anything flagged incomplete.

## Judging subagent prompt (replace the packet list)
```
You are a careful evidence judge for a history-book drafting project. Working directory: C:\Users\User\Desktop\Anugrah\OCR2Md

1. Read the rubric in full first: drafting/_runs/rubric.md
2. Your packets: PXXXX, ... (files drafting/_runs/packets/<PACKET>.md). For each packet, in order:
   a. Read the whole packet file. If it is large, read it in parts with offset/limit, but read every line. Every chunk must be read in full.
   b. Judge every chunk against all 13 units, following the rubric exactly.
   c. Write drafting/_runs/judgments/<PACKET>.jsonl with one JSON line per chunk (overwrite any existing partial file).
   d. Run: python -I drafting/_tools/check_judgments.py <PACKET>
      Fix any problems and re-run until it prints OK. If the checker itself crashes (e.g. KeyError), do NOT change your judgments to work around it; report the crash in your final reply instead.
3. Do not write, edit or delete any other file. Do not touch chroma_db, the corpus or any other folder. Do not use git.
4. Never invent content. Spans point at the chunk's own numbered sentences. Notes explain relevance only; add no facts of your own.

When finished, reply with one line per packet: packet id, chunks judged, kept, items.
```

## Facts for the final report
- **Folder check:**
  - `samarangana-sutradhara.md` (3,804,459 bytes, 2026-10-12 18:10) is in `Udaipur Books Markdown files/` and `Udaypur Reference Markdown Files/`. It is the re-OCR, also kept as `backups/2026-10-13_samarangana_reocr/samarangana-sutradhara_ASSEMBLED.md`.
  - The old two volumes were retired to `backups/2026-10-13_samarangana_reocr/` (`retired_*.md`, plus copies in its `Udaipur Books Markdown files/`). The database still indexes the old volumes, so items keep the ⚠ and must be re-verified against the re-OCR. `assemble.py` verifies against the retired copies.
  - The legacy orphan is `backups/2026-10-13_samarangana_reocr/samarangana-sutradhara_legacy_orphan.md`.
  - The re-OCR'd Yogasūtra is the active `Udaipur Books Markdown files/patanjala-yogasutra-rajamartanda-bhoja.md` (2026-10-12 16:06, same as `backups/2026-10-12_ocr_pagerefs/yogasutra_reocr_final.md`). The old one is in `Udaypur Reference Markdown Files/` (2026-10-09 11:24).
- **QC findings:**
  1. The first deepening rule used the unit-wide max score, which inflated global depth to over 2,000 ranks. It was fixed to per-query, which cut 1,020 chunks; the 77 chunks already packed were read anyway and are flagged `extra` in `candidates.jsonl`.
  2. In the C01 pilot, some Jagta EN chunks were bulk-rejected although relevant (e.g. 5029e6cf, 323b642e, eb80b269); their Hindi twins were kept.
  3. `bhoja-paramara-and-his-times.md` has no page markers, so its items are `[page not recorded]` + heading.
  4. A transient checker KeyError happened while `candidates.jsonl` was being rewritten (see step 3 above).
- **Timing so far:** retrieval 8 s. Judging: about 1.5–5 minutes per 6-packet batch, about 200–380k subagent tokens per batch.
