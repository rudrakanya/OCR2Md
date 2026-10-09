# Stage 2 build report

Built 2026-09-24T20:15:12 by `stage2_build.py` (stage2-build/1.0); dense relevance: True.

## Stores

- active (`kb3/kb_active.sqlite`): **14,702** chunks
- quarantine archive (`kb3/kb_quarantine.sqlite`): **4,730** chunks, never opened by retrieval

| quarantine reason | chunks |
|---|--:|
| irrelevant | 2,430 |
| non_claim | 2,275 |
| orphan | 25 |

Review queue (`kb3/review_queue.csv`): 2,510 chunks below the irrelevance threshold (80 kept active under the field-source safeguard).

*Jagta Hua Kasba* safeguard: 1,246 of 1,246 chunks active; quarantined only as non-claim: 0.

## Evidentiary mix per chapter bucket (active chunks)

| chapter | bucketed | welcome | admitted | primary | field | secondary | tertiary | contextual | folklore-tagged |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| C1 | 2,000 | 1,988 | 12 | 0 | 0 | 0 | 159 | 0 | 44 |
| C2 | 1,332 | 1,327 | 5 | 0 | 0 | 0 | 88 | 0 | 13 |
| C3 | 1,716 | 1,699 | 17 | 0 | 0 | 0 | 142 | 0 | 29 |
| C4 | 2,541 | 2,482 | 59 | 0 | 0 | 0 | 100 | 0 | 58 |
| C5 | 2,883 | 2,834 | 49 | 0 | 0 | 0 | 17 | 0 | 64 |
| C6 | 1,577 | 1,490 | 87 | 0 | 0 | 0 | 64 | 0 | 47 |
| C7 | 4,249 | 4,237 | 12 | 0 | 0 | 0 | 330 | 0 | 70 |
| C8 | 2,159 | 1,945 | 214 | 0 | 0 | 0 | 94 | 0 | 36 |
| C9 | 2,332 | 2,297 | 35 | 0 | 0 | 0 | 33 | 0 | 52 |
| C10 | 2,819 | 2,756 | 63 | 0 | 0 | 0 | 262 | 0 | 48 |
| C11 | 1,342 | 1,288 | 54 | 0 | 0 | 0 | 168 | 0 | 8 |
| C12 | 1,669 | 1,651 | 18 | 0 | 0 | 0 | 122 | 0 | 15 |
| C13 | 1,976 | 1,821 | 155 | 0 | 0 | 0 | 45 | 0 | 135 |
| C14 | 1,742 | 1,595 | 147 | 0 | 0 | 0 | 118 | 0 | 46 |
| C15 | 1,689 | 1,656 | 33 | 0 | 0 | 0 | 40 | 0 | 27 |
| C16 | 1,640 | 1,622 | 18 | 0 | 0 | 0 | 33 | 0 | 27 |
| AF | 1,414 | 1,384 | 30 | 0 | 0 | 0 | 14 | 0 | 20 |

Active claim-bearing chunks in no bucket (relevant to something, below 0.3 everywhere): 4,084

## Status and dating (active, claim-bearing)

| epistemic_status | chunks |
|---|--:|
| factual | 12,679 |
| inference | 1,023 |
| observation | 847 |
| speculation | 153 |

| event date_confidence | chunks |
|---|--:|
| undated-flagged | 10,866 |
| approximate | 2,890 |
| dated | 946 |

## Deduplication (links only; nothing removed)

| method | links |
|---|--:|
| minhash_jaccard | 6,726 |
| crosslingual_mutual_nn | 320 |
| dense_cosine | 204 |

Chunks marked `duplicate_of` another: 731

## Corroboration (independent works, duplicate clusters counted once)

| independent corroborating works | chunks |
|---|--:|
| 0 | 14,602 |
| 1 | 34 |
| 2 | 19 |
| 3 | 14 |
| 4 | 9 |
| 5+ | 24 |

`single_source` means no independent corroboration was DETECTED: by the dated entity-year keys, the semantic detector (bge-m3 cosine ≥ 0.85 plus a shared named entity), or the claims register. It is information for the writer, not a penalty (spec B3). Most general scholarship is legitimately single-source.

## Contested claims

65 chunks carry a contested claim; 2 superseded; 57 have contradiction_ids. See `kb3/claims_register.yaml`.
