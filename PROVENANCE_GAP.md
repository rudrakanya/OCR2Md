# Provenance gap — books whose originals are not in the repo

**This is not the folder gap.** The markdown for all 27 books is present and in the KB
(see `FOLDER_KB_RECONCILIATION.md`). What is missing for the books below is the **source PDF**,
so their extracted text cannot be compared against the original pages. Their fidelity is not
bad — it is *unknown*, and cannot be established from what is in the repo.

**13 of 27 books.**

| code | book | chunks in KB | AI-reworded chunks | note |
|---|---|--:|--:|---|
| `GAN` | History of the Paramāra Dynasty | 706 | 0 |  |
| `GAZ-VID` | Madhya Pradesh District Gazetteers: Vidisha | 496 | 185 (37%) | ~36% AI-reworded chunks |
| `HAR` | The Temple Architecture of India | 805 | 0 |  |
| `INT-GEO` | Geo-Heritage of Udaypur: The Third Eye | 431 | 0 |  |
| `PAN` | The Udayeśvara Temple: Art, Architecture and Philoso | 598 | 0 |  |
| `PAR` | History of the Parmar Rajput Dynasty | 36 | 0 |  |
| `PAT-CH` | The Cultural Heritage of Madhya Bharat | 387 | 0 |  |
| `PAT-INS` | Archaeological & Cultural Heritage of Madhya Bharat: | 143 | 4 (3%) | composite; inscriptions may be images in the original |
| `PAT-TEM` | The Cultural Heritage of Madhya Bharat — temples and | 214 | 0 |  |
| `SIN-B` | Bhoja Paramara and His Times | 1,096 | 0 |  |
| `SIN-S` | A serpentine scimitar of letters from Udaypur, distr | 18 | 0 |  |
| `TIW-E` | Jagta Hua Kasba / कथा उदयपुर (English translation) | 637 | 0 | translation of the Hindi original |
| `TIW-H` | कथा उदयपुर (Jagta Hua Kasba) — Hindi original | 609 | 0 | Devanagari throughout |

## The highest-risk source

**`GAZ-VID` — Madhya Pradesh District Gazetteers: Vidisha** is both unverifiable *and* partly non-faithful by
construction: 185 of its 496 chunks (37%) are tagged `llm_regenerated`, meaning the
text is a model's restatement rather than a transcription. Those chunks are correctly marked
`is_quotable: false`, so the pipeline will not quote them — but with no PDF there is no way to
check the restatement against the page it came from. A fact taken from this book is a fact on
trust, twice over.

`SAM` carries the same reworded-chunk defect but is partly checkable: three chapter extracts
of it are in the repo (chs 55–60, 66–67, 71–72), so part of it was auditable.

## What would close this

Supplying any of these PDFs makes Phase 1 fidelity measurable for that book immediately —
`audit_ocr.py` reads the mapping from `kb_audit/source_pdfs.yaml`, so adding a `pdf:` line and
re-running is the whole operation. In priority order:

1. **`GAZ-VID`** — unverifiable and 36% reworded; the worst combination in the corpus.
2. **`PAN`** — Pande on the Udayeśvara temple, the single most-cited source for C7.
3. **`PAT-INS`** — `primary_epigraphic`, the highest-primacy class, and C1's core citations.
4. **`TIW-H` / `TIW-E`** — the Devanagari original and its translation; the only present-day
   eyewitness material in the corpus, and the translation cannot be checked against the
   original either, since both are markdown-only.
5. `GAN`, `HAR`, `INT-GEO`, `PAT-CH`, `PAT-TEM`, `SIN-B`, `SIN-S`, `PAR` — ordinary secondary
   works; lower stakes.

Until then these books are usable but uncheckable, and the book's apparatus should not imply
that their readings were verified against pages. They were not.
