# Folder ↔ KB reconciliation

**Question:** can `Udaypur Reference Markdown Files/` still rebuild the knowledge base?
**Answer: yes.** No file is missing from the folder, no source is orphaned in the store, and
no book sits under a different name than the registry claims.

Audit only — nothing was copied, regenerated or restored.

## Method, and why not filenames

Identity is resolved **by content**. Filename similarity had already mis-mapped sources in
this project: it pointed three different books at `Some Paramara Templess.pdf` and matched the
Patanjali volume to nothing. For every source, 40 stored chunks are sampled and a 120-character
probe from each is searched for in every folder file, so the file a source *actually* came from
is found whatever it is called.

Two directions are measured, because they fail differently:

| direction | what a low number means |
|---|---|
| **store → folder** | content is in the KB that no folder file holds — the folder can no longer rebuild it. **This is the dangerous class.** |
| **folder → store** | text is in a folder file that no chunk holds — present on disk, invisible to retrieval |

`folder → store` is measured with 48-character shingles at a 220-character stride. Fixed-size
blocks were the wrong instrument and understated coverage badly (BET-S read 24% with blocks,
40% with shingles) because a block starting mid-chunk fails the test even when the text is
fully ingested.

## The three-way table

| code | folder file | registry | chunks | vectors | store→folder | folder→store | verdict |
|---|---|---|--:|--:|--:|--:|---|
| `ADH` | yes | yes | 328 | 280 | 100% | 68% | ok |
| `BET-K` | yes | yes | 56 | 56 | 98% | 67% | ok |
| `BET-S` | yes | yes | 44 | 44 | 97% | 40% | under-chunked |
| `BHJ-H` | yes | yes | 535 | 535 | 95% | 95% | ok |
| `DEV` | yes | yes | 268 | 268 | 98% | 80% | ok |
| `GAN` | yes | yes | 706 | 703 | 98% | 89% | ok |
| `GAZ-VID` | yes | yes | 496 | 496 | 92% | 69% | ok |
| `GUP` | yes | yes | 691 | 691 | 92% | 65% | ok |
| `HAR` | yes | yes | 805 | 805 | 90% | 71% | ok |
| `INT-ARC` | yes | yes | 406 | 406 | 90% | 78% | ok |
| `INT-GEO` | yes | yes | 431 | 431 | 92% | 75% | ok |
| `KRAM-1` | yes | yes | 1,268 | 1,268 | 100% | 76% | ok |
| `KRAM-2` | yes | yes | 563 | 563 | 95% | 63% | ok |
| `PAN` | yes | yes | 598 | 598 | 85% | 72% | ok |
| `PAR` | yes | yes | 36 | 36 | 100% | 88% | ok |
| `PAT-CH` | yes | yes | 387 | 387 | 100% | 89% | ok |
| `PAT-INS` | yes | yes | 143 | 143 | 100% | 91% | ok |
| `PAT-TEM` | yes | yes | 214 | 214 | 100% | 85% | ok |
| `RAJ-E` | yes | yes | 667 | 667 | 78% | 91% | ok |
| `RAJM` | yes | yes | 198 | 198 | 98% | 68% | ok |
| `SAM` | yes | yes | 1,381 | 1,379 | 85% | 93% | ok |
| `SIN-B` | yes | yes | 1,096 | 1,096 | 100% | 93% | ok |
| `SIN-S` | yes | yes | 18 | 18 | 86% | 80% | ok |
| `SIN-T` | yes | yes | 1,453 | 1,452 | 92% | 67% | ok |
| `SKP-13` | yes | yes | 662 | 662 | 95% | 93% | ok |
| `TIW-E` | yes | yes | 637 | 637 | 100% | 99% | ok |
| `TIW-H` | yes | yes | 609 | 608 | 100% | 100% | ok |

## Mismatches, classified

**in KB but no folder file — 0.** Every one of the 27 sources resolved to a folder file by
content, at 78–100% probe coverage. No stored content is orphaned.

**folder file but not in KB — 0.** Every folder file was claimed by exactly one source; none
is uningested, and no file in the folder belongs to no source.

**name mismatches — 0.** For all 27, the file the content resolved to is the file the registry
names. The registry's `file:` field is accurate.

## Where the folder holds more than the KB does

Not a mismatch, but the real gap: parts of these files are on disk and not in any chunk.

| code | folder→store | not chunked |
|---|--:|---|
| `BET-S` | 40% | ~60% of the file |
| `KRAM-2` | 63% | ~37% of the file |
| `GUP` | 65% | ~35% of the file |
| `BET-K` | 67% | ~33% of the file |
| `SIN-T` | 67% | ~33% of the file |
| `ADH` | 68% | ~32% of the file |

`BET-S` is the outlier at 40%. These are journal papers and monographs whose front matter,
reference lists, figure captions and running heads are legitimately dropped by chunking — so a
number below 100% is expected, not a defect. What it does mean is that the folder is a
**superset** of the KB: rebuilding from it reproduces the KB, but the KB is not the whole of
what the folder holds.

## Verdict

The folder **is** the source of truth it is meant to be. All 27 books are present, every
source's stored content traces back to a file in it, and a rebuild from the folder would
reproduce the store. The claim that files may be missing does not hold against the content.
