# Plan: assembling the complete evidence & excerpt map

Written 2026-10-13, at 127 of 221 packets judged.

## Interim numbers

| Measure | Value |
|---|---|
| Chunks judged | 3,012 (1,383 kept) |
| Verified items | 2,456 |
| Verification pass rate | 98.6% (33 failures) |

Projected at completion: about 4,300 items. C04 and C05 will hold about 700–800 each, and roughly 70% of those are contextual. C08, C09, C12 and C13 are thin on direct evidence.

## Phase A: finish judging
Run the remaining groups, 8–10 judges in parallel. Done when `check_judgments.py --all` reports 221/221.

## Phase B: evidence clean-up (scripted, then reviewed by me)
1. **Fix the 33 verification failures.** Most look like anchor misses: the quote sits in the source just before the point where the chunk was located. Fallback: search the whole file for the verbatim segment; accept it only if it occurs exactly once; record `v_note: located before anchor`. Anything still failing is dropped and logged.
2. **De-duplicate.** Merge near-identical items. Two cases:
   - overlapping chunks of the same book that produce the same sentence (one quote contains the other, same book);
   - the Jagta Hindi and English twins, which carry the same claim.

   Keep one item with an "also at …" line, so every original citation survives.
3. **Normalise claim keys and values.**
   - Map free-text keys onto the canonical list; for example, "Udayeśvara: date" becomes "temple foundation/consecration date".
   - Tag the C01 pilot items that sit on known conflicts, so they join the tables: 1059 vs 1080, the brass cover, the survival legends, the reign dates, and the other pilot conflicts.
   - Build the tables in `_runs/conflicts_curated.json` (item IDs per key). I review this file by hand; values are only ever what each source says, never resolved.
4. **Check home units.** List items where the home unit is doubtful, e.g. a C01 item that is really Paramāra history (C04). Move only clear cases, keep the original unit as an xref, and log every move.
5. **Normalise and check the gap list.**
   - Merge variant spellings of cited works into one list, e.g. "Cunningham ASR X" and "ASI vol. X".
   - Mark each work as "in library" or "not in library" against the 29 titles.
   - Add sub-topics with no or thin direct evidence.
6. **Run rule checks (automated).**
   - Every SAMAR item is ⚠.
   - All TEMPLE-ECON items are contextual.
   - No "Udaipur, Rajasthan" leaks: grep for Mewar, Rana, Rajasthan, Pichola.
   - Every Hindi/Sanskrit quote has a "[my translation]" gloss.
   - No page appears without a marker.
   - Item IDs are unique.

## Phase C: document design (`render.py`)
One file per unit (`ch01 … ch13_afterword.md`), plus `_master.md`. Each chapter file has these sections:
1. **Header.** Title, unit brief, sub-topics, ⚠ notes (Samarāṅgaṇa re-verification, the Pande twin, Jagta page approximation).
2. **Coverage proof.**
   - 31-row pass table: query, depth, deepenings, chunks.
   - 29-row source sweep: retrieved / pre-filtered / read / kept / items.
   - Incomplete flags.
3. **Evidence summary.** Per sub-topic: direct and contextual counts, number of books, and a one-line strength rating (strong / adequate / thin / none), computed from the counts.
4. **Sub-topic index.** Item IDs per sub-topic; direct items listed first.
5. **Evidence by book.** Books are ordered by count, each headed "*Title* (n excerpts)". Within each book, items are ordered by sub-topic, then page. **Direct items come in full first.** Contextual items follow under "Context from this book", also in full, so nothing is hidden or dropped.
   - Each item gives: ID, sub-topic, type, strength, the verbatim quote, the gloss labelled [my translation], the citation (scan p. / [page not recorded] / ≈), the chunk ID, the relevance note, xrefs, the claim, and any works the passage cites.
6. **Cross-references.** Items homed in other chapters that also serve this one.
7. **Conflicts.** Side-by-side tables from the curated claims file, with no resolution.
8. **Gaps.** A to-do checklist: thin or empty sub-topics, and cited works not in the library.
9. **Source-coverage line.**

`_master.md` contains:
- the contents table, with item and direct counts per unit;
- a source × chapter matrix;
- a global conflicts register;
- a global gaps register;
- a list of books with no or few items;
- the **Run status & test report** (`make_status.py`): passes, retrieval and pre-filter counts, calibration with its 60-chunk sample, chunks read/kept/rejected, verification pass rate, **15 hand spot-checks**, incomplete flags (none), QC findings, folder check, time and tokens.

An alternative view, ordered by sub-topic instead of by book, is `render.py --by subtopic`. Optional: an HTML version of `_master.md` plus the chapters, for browsing.

## Phase D: QC and handover
1. **Hand spot-checks.** Take 15 random items (`make_status.py --sample 15`). Check each against the source file at the cited page: quote, page and relevance. Record them in `_runs/spotchecks.json`.
2. **Targeted checks.** Read 10 more items from the riskiest buckets: Hindi OCR glosses, Samarāṅgaṇa, `[page not recorded]` items, and claim-tagged items.
3. **Regenerate and report.** Run `make_status.py`, then `render.py`. Report the final numbers to the user: path, items per unit, pass rate, weakest units and their gaps, unused books, time and tokens, incomplete flags.

Estimated time after judging: about 30–45 minutes, mostly the claim curation and the hand spot-checks. The scripts themselves run in seconds.
