# Phase 2 — asset audit: tables, captions, plates and inscriptions

**Date:** 2026-10-05 · **Scope:** 27 registered sources + 2 un-ingested PDFs in the repo
**Constraint observed:** audit only — no re-chunk, no re-embed, no store writes, no paid-API calls.

Markdown extraction keeps prose and quietly loses the rest. For a knowledge base that
is the sole source of truth for a book, that matters: plate captions carry iconographic
identifications, tables carry measurements and inventories, and an inscription
reproduced as a photograph is a fact that never entered the base at all.

## Headline

**The single most consequential finding in this phase is not an extraction failure at
all — it is a chunking loss, and it is fully repairable from files already on disk.**
362 substantive table rows are present in the markdown but missing from the live
knowledge base, including Ganguly's epigraphic concordance. Re-chunking the existing
markdown with today's code recovers them. No OCR, no source PDFs, no API spend.

---

## 1. Table rows present in the markdown but absent from the store

Measured by taking every distinct pipe-table row in each book's markdown and asking
whether its longest cell appears in that source's chunk text (matching on the longest
cell rather than the whole line, so a row that was merely reformatted at chunk time is
not miscounted as lost).

| Source | Distinct rows | Missing from store | Share | Of which substantive |
|---|---|---|---|---|
| GAZ-VID | 811 | 107 | 13% | **87** |
| KRAM-1 | 371 | 131 | 35% | 41 |
| GAN | 272 | 116 | 43% | **116** |
| SIN-T | 528 | 84 | 16% | 49 |
| DEV | 100 | 38 | 38% | 0 |
| ADH | 165 | 37 | 22% | 12 |
| GUP | 1,219 | 33 | 3% | 32 |
| PAT-CH | 17 | 9 | 53% | 9 |
| PAT-TEM | 17 | 9 | 53% | 9 |
| KRAM-2 | 18 | 8 | 44% | 4 |
| BET-S, BET-K, RAJ-E | 153 / 20 / 28 | 3 / 1 / 2 | 2–7% | 1 each |
| INT-ARC, INT-GEO, SAM, PAT-INS | — | 0 | 0% | 0 |

**Totals: 578 rows missing, of which 216 are tables of contents or lists of plates and
362 are substantive.** The navigational ones are no loss — arguably a gain.

### What the substantive losses actually are

- **GAN — 116 rows: an epigraphic concordance.** The highest-value loss in the corpus.
  Each row carries an inscription's name, place, type, Vikrama/Śaka year, converted CE
  year, the ruling king, and a citation to *Epigraphia Indica* or *Indian Antiquary*:

  > `11 | Mandhata | C. | 1112 | 1055 | Jayasimha | R. | E. I., Vol. III, p. 46.`
  > `9 | Tilakwada | C. | 1103 | 1047 | Bhoja | P. | Proc. 1st Oriental Conf. 1919, p. 319.`

  This is the primary-source apparatus for Paramāra chronology — exactly the material
  the book's contested-date work depends on — and none of it is retrievable.

- **GAZ-VID — 87 rows:** gazetteer statistical series (grain prices by year, birth and
  death rates per mille, school enrolment, co-operative share capital). Socio-economic
  evidence for the town chapters.

- **SIN-T — 49 rows:** temple-economy tables (palkhi counts by district, per-head
  Warkari expenditure).

- **KRAM-1 — 41 rows, KRAM-2 — 4 rows:** Kramrisch's architectural and iconometric
  proportion tables — storey-by-storey *vedi* and *jaṅghā* measurements in hastas, and
  the 7-to-10 *tāla* image-proportion table.

- **GUP — 32 rows:** iconographic attribute tables ("Objects in hands / Six-armed /
  thunderbolt, spear, protection pose…") and the key expanding the abbreviations GUP
  uses for its cited Sanskrit texts — without which its own citations are unreadable.

- **PAT-CH and PAT-TEM — the same 9 rows** (the duplication recorded in
  `EXTRACTION_FAILURES.md` §2): a district monument inventory, including the row that
  names the town this book is about:

  > `6 | Bhilsa | 26 | 142 | Badoh, Besnagar, Bhilsa, Gyaraspur, Pathari, Udaypur, Udaygiri`

- **ADH — 12 rows:** the collapsed inventory headers covered in `EXTRACTION_FAILURES.md` §1.

### Cause: a legacy chunker, not the current one

`build_kb.chunk_markdown` folds any chunk under `MIN_CHARS` (200) into a neighbour in
the same section, and `_absorb_short` (`build_kb.py:195`) **drops** a fragment that has
no room either side — by design, to keep 40-character stubs out of the vector space. A
table row is short, so rows are the natural casualty.

But the current code is not the culprit. Re-chunking the same markdown with today's
`chunk_markdown` recovers essentially everything:

| Source | Rows missing from live store | Rows missing after a fresh re-chunk |
|---|---|---|
| GAN | 116 | **0** |
| PAT-CH | 9 | **0** |
| KRAM-1 | 131 | **1** |
| GAZ-VID | 107 | **0** |

The live `kb3/kb_active.sqlite` was therefore built by an **older pipeline**. (Chunk
counts differ too: GAN has 706 chunks live against 446 fresh, so the old chunker split
smaller *and* dropped tables.)

**Remediation:** re-chunk and re-embed from the markdown already in the folder.
Recovers 362 substantive rows. Needs no source PDF — which matters, because GAN and
GAZ-VID have no source document in the repo at all, so this is the *only* way their
tables can be recovered. This is Phase 4 work and has not been done.

---

## 2. Captions and images

| Source | Caption lines | In store | Image refs | With alt text |
|---|---|---|---|---|
| INT-ARC | 283 | 220 (78%) | 268 | 268 |
| PAN | 120 | 106 (88%) | 130 | 130 |
| GUP | 84 | 58 (69%) | 390 | 390 |
| HAR | 3 | 1 | 444 | 444 |
| INT-GEO | 10 | 10 (100%) | 243 | 243 |
| BET-S | 13 | 12 | 10 | 10 |
| KRAM-2 / KRAM-1 | 0 / 0 | — | 89 / 36 | 89 / 36 |
| RAJ-E | 0 | — | 36 | 36 |
| ADH | 0 | — | 26 | 26 |
| BHJ-H | 0 | — | 2 | 2 |

Captions are in reasonable health: where a book has them, 69–100% reach the store, and
**every image reference in the corpus carries alt text** (no bare `![](…)`). The
caption shortfall in GUP (26 of 84) and INT-ARC (63 of 283) is the same `_absorb_short`
loss as the tables — a caption is a short line — and the same re-chunk fixes it.

Note that `audit_assets.py`'s `plate_pages` count is **not meaningful for image-only
scans** and should not be read as a plate inventory: in a scanned PDF every page is one
full-page image with no text layer, so the metric reports "40 plates" for essentially
every scanned book. It only discriminates on born-digital files (SAM: 0 plates in 40
pages; SKP-13: 3).

---

## 3. Untranscribed inscriptions — two PDFs in the repo, neither in the knowledge base

### `Inscriptions Corpus.pdf` — 496 pages, 39.8 MB, image-only, **entirely absent**

Fifteen probe phrases OCR'd from pages 40, 120 and 300 return **zero matches anywhere
in the 14,702-chunk store**. The pages carry exactly the primary epigraphic material
this book argues from:

| Page | Heading read off the page |
|---|---|
| 40 | UJJAIN GRANT OF VAKPATIRAJADEVA |
| 120 | **JHALRAPATAN STONE INSCRIPTION OF THE TIME OF UDAYADITYA** |
| 300 | MODI STONE INSCRIPTION OF THE TIME OF JAYAVARMADEVA |

The page-120 heading is the significant one. Udayāditya's accession is recorded in
`curated_facts.yaml` as a **contested fact** with four competing date ranges, and a
dated inscription from his reign is first-order evidence for it. A 496-page corpus of
Paramāra inscriptions is sitting in the repo unread.

This also answers an open question from the reconciliation: `Inscriptions Corpus.pdf`
is confirmed **not** part of PAT-INS or SIN-S, and not part of the KB in any form.

### `Art of Paramaras.pdf` — 62 pages, 72.8 MB, image-only, **absent**

Zero of ten probes found in the store. Page 45 shows the same sideways-text signature
as ADH (`poorid Ajsoru pjn nud YNMDIDF B JO WO`), so it needs orientation correction
too. Previously recorded as "OCR stopped at p.28/62, never ingested" — confirmed.

---

## 4. Ranked remediation for Phase 2

| Rank | Action | Recovers | Needs |
|---|---|---|---|
| 1 | Re-chunk + re-embed from existing markdown | 362 substantive table rows (incl. GAN's concordance) + ~90 captions | no OCR, no PDFs, no API |
| 2 | OCR `Inscriptions Corpus.pdf` and ingest | 496 pages of Paramāra epigraphy, incl. a Udayāditya-reign inscription | 496-page OCR run |
| 3 | OCR `Art of Paramaras.pdf` with orientation correction | 62 pages | 62-page OCR run |
| 4 | Re-extract ADH's table pages | the Sapta Mātṛkā inventory | see `EXTRACTION_FAILURES.md` |

Item 1 is the best return in the entire audit: it needs no new OCR and no missing
source document, and it is the only route to GAN's and GAZ-VID's tables, since neither
book has a source PDF in the repo.

**Nothing above has been executed.** All four items are Phase 4.

## Artefacts

- `kb_audit/asset_audit.json` — per-source caption, image and table counts
- `audit_assets.py` — the Phase 2 collector
