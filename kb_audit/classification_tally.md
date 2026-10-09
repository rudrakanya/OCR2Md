# Stage 1B — Classification tally

Generated from `kb_audit/classified_inventory.jsonl` by `stage1_classify.py` (19,158 chunks, 26 sources). Regenerate by re-running the script.

**Read with the validation results** (`kb_audit/classifier_validation.md`): on a held-out sample, `factual` labels were right 7/8 times, `observation` 6/9, `inference` 4/9, `speculation` 2/9. The speculation and inference columns below are *candidate* counts, not findings.

## Chunks by source type × epistemic status (claim-bearing only)

| source_type | factual | observation | inference | speculation | total | non-claim (apparatus/garbage) |
|---|--:|--:|--:|--:|--:|--:|
| primary | 2,134 | 1 | 50 | 8 | 2,193 | 19 |
| field_observation | 1,086 | 829 | 125 | 62 | 2,102 | 121 |
| secondary_scholarship | 6,860 | 2 | 792 | 266 | 7,920 | 1,948 |
| reference_tertiary | 2,417 | 0 | 124 | 62 | 2,603 | 151 |
| contextual_background | 1,892 | 3 | 146 | 50 | 2,091 | 10 |
| **all** | **14,389** | **835** | **1,237** | **448** | **16,909** | **2,249** |

## By source

| source_id | type | chunks | factual | obs. | inf. | spec. | non-claim | mixed-status | median chars |
|---|---|--:|--:|--:|--:|--:|--:|--:|--:|
| skanda-xiii | primary | 713 | 666 | 1 | 30 | 3 | 13 | 284 | 1052 |
| hardy-2007 | secondary_scholarship | 1,819 | 818 | 1 | 103 | 60 | 837 | 131 | 258 |
| kumar-2023-betwa | secondary_scholarship | 104 | 53 | 0 | 3 | 1 | 47 | 18 | 300 |
| singh-1984-bhoja | secondary_scholarship | 1,240 | 951 | 1 | 184 | 58 | 46 | 360 | 528 |
| bhojdev-hi | secondary_scholarship | 561 | 536 | 0 | 25 | 0 | 0 | 37 | 461 |
| intach-geoheritage | field_observation | 549 | 228 | 146 | 38 | 22 | 115 | 205 | 331 |
| gupte-1972 | reference_tertiary | 872 | 815 | 0 | 10 | 9 | 38 | 65 | 382 |
| intach-2022-udaypur | field_observation | 428 | 218 | 184 | 12 | 8 | 6 | 221 | 361 |
| tiwari-jhk-en | field_observation | 637 | 311 | 226 | 75 | 25 | 0 | 430 | 556 |
| tiwari-jhk-hi | field_observation | 609 | 329 | 273 | 0 | 7 | 0 | 378 | 487 |
| suryavanshi-2013-betwa | secondary_scholarship | 93 | 58 | 0 | 8 | 1 | 26 | 17 | 469 |
| patil-1952 | reference_tertiary | 438 | 367 | 0 | 46 | 24 | 1 | 72 | 516 |
| patil-composite-inscriptions | reference_tertiary | 150 | 145 | 0 | 5 | 0 | 0 | 4 | 685 |
| patil-composite-temples | reference_tertiary | 238 | 204 | 0 | 21 | 12 | 1 | 34 | 488 |
| ganguly-paramara | secondary_scholarship | 782 | 591 | 0 | 98 | 47 | 46 | 245 | 595 |
| parmar-2025-origins | secondary_scholarship | 38 | 32 | 0 | 4 | 1 | 1 | 4 | 473 |
| rajpurohit-bhoj-en | secondary_scholarship | 718 | 627 | 0 | 69 | 7 | 15 | 147 | 530 |
| samarangana | primary | 1,499 | 1,468 | 0 | 20 | 5 | 6 | 68 | 956 |
| singh-serpentine | secondary_scholarship | 31 | 13 | 0 | 4 | 2 | 12 | 4 | 227 |
| adhikari-2013-un | secondary_scholarship | 630 | 307 | 0 | 138 | 13 | 172 | 202 | 275 |
| singh-temple-economics | contextual_background | 2,101 | 1,892 | 3 | 146 | 50 | 10 | 328 | 415 |
| deva-1969-temples | reference_tertiary | 353 | 273 | 0 | 24 | 7 | 49 | 40 | 475 |
| kramrisch-1946-v1 | secondary_scholarship | 1,630 | 1,475 | 0 | 91 | 37 | 27 | 157 | 471 |
| kramrisch-1946-v2 | secondary_scholarship | 898 | 719 | 0 | 29 | 19 | 131 | 57 | 434 |
| pande-udayesvara | secondary_scholarship | 1,324 | 680 | 0 | 36 | 20 | 588 | 144 | 268 |
| vidisha-gazetteer-1979 | reference_tertiary | 703 | 613 | 0 | 18 | 10 | 62 | 42 | 446 |

## Tags

Tags are orthogonal to status (spec: folklore and opinion are tags, never speculation).

| tag | chunks | meaning |
|---|--:|---|
| contextual | 2,101 | contextual_background source |
| content_kind:apparatus | 1,963 | index / TOC / bibliography / notes (non-claim) |
| ocr_damaged | 979 | visible OCR corruption |
| embeds_primary_text | 847 | quotes original-script primary text |
| prescriptive | 732 | deontic śāstra language ("should be made") |
| scriptural_register | 713 | Purāṇic register |
| content_kind:verse | 460 | verse/fenced block kept atomic |
| llm_regenerated | 455 | contains `[cite: N]` markers — AI-restated, not transcription |
| content_kind:table | 404 | table kept atomic |
| original_script | 394 | primary text in original script |
| secondhand_history | 368 | field source reporting pre-modern history it did not witness |
| content_kind:ocr_garbage | 286 | unreadable OCR (non-claim) |
| folklore | 251 | reports legend / tradition / oral testimony |
| opinion | 170 | normative recommendation or judgement |

## Pre-processing removals (logged line-by-line in `preprocessing_log.jsonl`)

| removed | count |
|---|--:|
| page_furniture | 5,302 |
| image_ref | 1,674 |
| ocr_commentary | 407 |
| html_comment | 22 |

OCR-model commentary stripped, by source: gupte-1972 152, kramrisch-1946-v1 100, kramrisch-1946-v2 97, hardy-2007 49, pande-udayesvara 8, intach-geoheritage 1

## Chunk geometry

- chunks: 19,158 (old store: 10,754 incl. 1,287 appended)
- length p05/p25/median/p95/max: 36/286/444/1304/6107 chars
- overlap between adjacent chunks: none by construction (old store: 62.5% of pairs)
- chunks over 1,700 chars: 9 (single unsplittable lines: bibliography run-ons, wide table rows)
- chunks under 150 chars: 1,857, of which non-claim 1,716
- mixed-status chunks (more than one sentence status present): 3,694
