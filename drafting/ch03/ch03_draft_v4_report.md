# Chapter 3, draft v4: Udaypur-centred rewrite under the Gazetteer cap (21 October 2026)

No API calls were made. The work was verified in-session, and only free local tools were used.

## State before this pass
- The brief assumed `ch03_draft_v1.md`. That file is archived (`_archive/pre_contents_rebuild/ch03/`, 14 Oct, five sections).
- The live draft was **v3** (19 Oct). It had 11 units matching the contents file, 7,357 body words and 222 items.
- v3 was written to the "all evidence" instruction, with the Gazetteer cap switched off. Five units were over 40%:
  - 3.3: 73%
  - 3.4: 47%
  - 3.6: 44%
  - 3.7: 43%
  - 3.8: 56%
- v3 used *Temple Economics* once, in 3.6.
- Five units (3.3, 3.4, 3.6, 3.7, 3.8) had no stated stake in Udaypur.
- The v3 sections are kept in `ch03/v3_sections/`.

## Setup
- `ch03/cfg_ch03v4.py` sets `GAZ_MAX_SHARE = 0.40`. *Temple Economics* is excluded again, and the canon brief now says Udaypur is the centre of gravity.
- `Caṣṭana` was added to `ALLOW_EXTRA`.
- New items in the pack (`evidence_pack_v4.json`), all from the free corpus:
  - C03-KBN-GANGULY-001 (Udayapur north of Bhilsa);
  - C03-KBN-RAJABHOJ-001 (Devī's stupa at Ujjain);
  - C03-KBN-MADHYABHARAT-012/013 (Nahapāna; Caṣṭana and Rudradāman);
  - C03-KBN-MADHYABHARAT-014 (where the three *yakṣīs* went).
- C01-MADHYABHARAT-001 is borrowed from Chapter 1 (Udayāditya named the town, temple and tank after himself).

## Units

| Unit | Body words | Items | Gazetteer items | Gazetteer share | Stake in Udaypur |
|---|---|---|---|---|---|
| 3.1 Prehistory and ancient names | 566 | 19 | 7 | 37% | no find comes from Udaypur's hill; Daśārṇa as the country's old name |
| 3.2 Vidisha in literature | 420 | 18 | 7 | 39% | Udaypur appears in none of the old texts; only the Gazetteer lists it beside Besnagar |
| 3.3 Besnagar: the excavated city | 376 | 11 | 4 | 36% | the old capital of Udaypur's country, already a field of mounds when Udayāditya founded his town |
| 3.4 Mauryas and Śuṅgas | 645 | 17 | 6 | 35% | Ākara becomes a seat of kings; Vidisha "a larger and more ancient city than Udaipur" |
| 3.5 Roads, merchants, sacred centres | 718 | 25 | 10 | 40% | the Deccan road of devotion, with the Udayeśvara among its "beacon-towers" (Tiwari) |
| 3.6 Heliodoros's pillar | 726 | 24 | 9 | 38% | the oldest dated act of worship in Udaypur's country, by a named donor, as Udaypur's temple bears its founder's name |
| 3.7 Images and rites at Besnagar | 582 | 14 | 4 | 29% | the *liṅga* in stone centuries before the Udayeśvara; the rites themselves do not reach Udaypur |
| 3.8 Sātavāhanas to Guptas | 619 | 16 | 6 | 38% | the Guptas are the first kings with their own records (Udayagiri) in Udaypur's country |
| 3.9 Udayagiri and the Gupta shrines | 788 | 29 | 4 | 14% | Gupta Viṣṇu images near Udaypur; the hill caves (deep sacred past only) |
| 3.10 From Vidisha to Bhilsa | 848 | 29 | 10 | 34% | Bhilsa's province holds Udayapur in 1172, governed for the Caulukya king (U1) |
| 3.11 A contested frontier | 829 | 29 | 5 | 17% | no record says who held Udaypur's hill; leads into Ganguly's 808–812 reconstruction and Ch 4 |
| **Total** | **7,117** | **211 distinct** | | **all ≤ 40%** | |

- **Notes:** 40 reader-facing notes, one per paragraph at most.
- **Unused items (17):**
  - 15 Gazetteer items dropped to meet the cap: the excavation detail of 3.3, the duplicate Devī item, the museum Kubera, Vindhyaśakti, and "inscriptions and coins of both houses";
  - KRAM-2-001 (a bare cross-reference);
  - TEMPLE-ECON-001 (canon).
- **The 3.5 share is exactly 40%,** which is at the cap and passes.

## Thin units, flagged rather than padded
- **3.3 is now short (376 words).** Besnagar's stratigraphy, wall and coins rest on the Gazetteer alone; the excavation reports are not in the corpus.
  - These findings are given briefly, as the Gazetteer's claims, with a note saying so.
  - The detailed period-by-period finds were cut, not padded out with other material.
- **3.2 (420 words) is unchanged.** The literary record gives little more.
- **Prehistory (3.1) stays one developed treatment.** It says that none of the finds comes from Udaypur's hill.

## Some quotations used
- "a larger and more ancient city than Udaipur" (C03-JAGTA-EN-001, 3.4)
- "what happened to it afterwards is not known" (C03-MADHYABHARAT-017, 3.3)
- "might have emerged as an independent City State, temporarily" (C03-GAZ-012, 3.3, attributed)
- "till its final incorporation with the Gupta empire" (C03-KBN-MADHYABHARAT-013, 3.8)
- "the earliest known structure of Vasudeva sect" (C03-GAZ-029, 3.6)
- "scattered here and there in this region" (C03-JAGTA-EN-001, 3.8)

## Canon and boundaries
- **Before the foundation.** Chapter 3 stops before the Paramāra foundation, and Udayāditya enters only as the later founder.
- **U1.** Lūṇapasāka now governs "for the Caulukya king" (3.10).
- **R4.** The 1172 province is given only from the records that name it.
- **Ganguly's "thirty miles".** This distance conflicts with the ledger's 55–70 km. It stays in a note and is not used as a measurement in the text.
- **Spelling.** The dynasty spelling check passes.

## Checks
- `inhouse.py check` passes all 11 units, including the Gazetteer cap and the ledger.
- AI-shape per 1,000 words: "not X but Y" 0.3, triplets 0.6, colon reveals 0.1.
- The stitch check is equal, at 53,231 characters.
- **Editorial read (14 questions).** All units pass.
  - Every unit now ends on, or contains, its stake in Udaypur.
  - 3.5 and 3.10 sit at the high end of Gazetteer use, at 40% and 34%.

## Deliverables
- `ch03/ch03_draft_v4.md` (working draft, with IDs)
- `ch03/ch03_draft_v4_footnoted.md` (40 notes, 14 bibliography entries, still incomplete as before)
- `ch03/Chapter 3 - Before Udaypur - Draft v4.docx`: all 11 units present, ending on the bibliography, none empty or truncated
- `run/ledger/ledger_ch3.json`, merged into `editorial/book_ledger.json`
