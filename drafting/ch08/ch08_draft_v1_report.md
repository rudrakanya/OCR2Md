# Chapter 8, draft v1: Religion and the Material Life of Udaypur (21 October 2026)

Drafted in-session from the contents file (`editorial/Udaypur_Book_Contents.md`, Chapter 8: 14 units). No API calls, Chroma queries or paid ledger runs were used.

## 0. State before work

- **No Chapter 8 material existed.** There was no `ch08/` folder, plan, cfg, pack or draft, and no `run/ch8/` sections.
- **Contents file:** 14 units, from 8.1 (the Udaypur endowments, 1163–1229) to 8.14 (the living temple).
- **v2 master outline:** 7 sections with a 3,800-word target, superseded by NO_LENGTH. Its item assignments, opening (Dhāmadeva's four *biswa*) and closing were redistributed over the 14 units, with no units added, dropped, split or merged.
- **Evidence:** `evidence_index/ch08.jsonl` holds 269 items: 44 direct and 225 contextual, of which 43 are Temple Economics.

## Plan and files

| Item | Path |
|---|---|
| Plan | `ch08/ch08_plan_v1.md` |
| cfg | `ch08/cfg_ch08v1.py`: NO_LENGTH; Gazetteer share capped at 0.40. New extra rules: Temple Economics tied to Udaypur, or not framed as contextual, fails; anonymous labour (farmers, traders, artisans, weavers and others in a sentence without IDs) fails; R4 terms must carry their record's date. |
| Pack | `ch08/evidence_pack_v1.json`: 302 items, i.e. the index plus 33 borrowed from Ch 1, 2, 4, 5, 6, 7, 9, 10, 11 and 12 |
| Sections | `run/ch8/8.1–8.14.md` |
| Ledger | `run/ledger/ledger_ch8.json`, merged; the header reads "Chapter 8 (v1)" |

## Units

| Unit | Body words | Items | Direct (ch08) | Temple Econ. |
|---|---|---|---|---|
| 8.1 The Udaypur endowments, 1163–1229 | 481 | 21 | 14 | 0 |
| 8.2 How Paramāra temples were endowed | 476 | 17 | 0 | 0 |
| 8.3 The temple as an institution | 339 | 12 | 2 | 2 |
| 8.4 Land, measure and water in the grants | 433 | 16 | 1 | 0 |
| 8.5 Stone, cloth and craft *(thin)* | 360 | 11 | 1 | 0 |
| 8.6 Markets, goods and money | 410 | 13 | 0 | 0 |
| 8.7 Farming and irrigation in the modern district *(thin)* | 272 | 11 | 0 | 0 |
| 8.8 Later trades and crafts *(thin)* | 202 | 10 | 5 | 0 |
| 8.9 What worship required | 311 | 10 | 0 | 0 |
| 8.10 Śaiva schools in Malwa | 292 | 14 | 0 | 0 |
| 8.11 Śaiva monasteries and ascetic lineages | 297 | 10 | 0 | 0 |
| 8.12 Gods beside Śiva | 294 | 12 | 0 | 0 |
| 8.13 Temple service at Udaypur *(thin)* | 345 | 7 | 5 | 0 |
| 8.14 The living temple | 241 | 9 | 8 | 0 |
| **Total** | **4,753** | **160 distinct** | **31 of 44** | **2** |

The chapter is shorter than Chapters 5–7 (7,000–9,000 words) because its evidence is. No unit was padded.

## Temple Economics: every use

Two items are used, both in 8.3, both framed as south Indian comparison in their own sentences, and the note says they say nothing of Malwa:

1. **C08-TEMPLE-ECON-016:** "In south India, generations of donors made the larger temples landlords and bankers, and their daily routine employed priests, musicians, florists and cooks."
2. **C08-TEMPLE-ECON-021:** "Royal grants in south India were of two kinds, a whole village made over, or the king's taxes assigned to the temple."

None of the 43 items concerns Udaypur. The new cfg rule checks every sentence that cites one: it fails if the sentence names Udaypur, and fails if it lacks a contextual marker. `ch_rules.py` reports 0 failures. The other 41 Temple Economics items are unused.

## Thin units: what cannot be said

- **8.5, craft.** The only Udaypur craft is one Gazetteer sentence on the red sandstone *kundies*, with no description, date, maker or traceable source (RR-18). The four builders' roles come from the treatises, not from Udaypur. No loom is recorded at Udaypur.
- **8.7, modern farming.** Ch 2 already covers the crops and soils, so the unit adds only the census share, irrigation under 1% and the *gaonti kharch*. These are twentieth-century district facts; nothing is recorded of Udaypur's medieval fields.
- **8.8, later trades.** These are district trades plus Udaypur's quarries. Between the Paramāras and the twentieth century the records name no trade of the town.
- **8.13, temple service.** The evidence is one possible drum-stone (Pande), the time-keepers' family claim (unconfirmed), the vedī tradition and an undated instrument fragment. No priest, cook, gardener or dancer of the Udayeśvara is recorded.
- **Also said plainly elsewhere:**
  - no founding endowment is known (8.1, 8.3);
  - the 1163 gift rests on Ganguly alone and went to Udaleśvara, which is kept apart from Udayeśvara (RR-17);
  - no Udaypur grant mentions a well, a wheel or an irrigated field (8.4);
  - no market list survives for Udaypur (8.6);
  - no monastery, school or teacher is recorded at Udaypur (8.10, 8.11);
  - Udaypur's Paramāra-era worship and festivals are unrecorded (8.9).

## No invented labour; no regional pattern as an Udaypur fact

- **Labour.** Named people act only where the record names them: Dhāmadeva, Vasantapāla, Lūṇapasāka, Memmaka, Pālhaṇadeva, Cāmuṇḍarāja, Purandara and Vyomaśiva, and the villagers who pledged grain per water-wheel (CII-025). No farmers, traders or artisans are put to work. 8.4 says that the grants rarely say who worked the land. The cfg anonymous-labour rule passes; the only agent nouns `prose_checks` reports are the census categories in 8.7.
- **Regional pattern.** Every regional or normative passage is labelled in the text, in phrases such as "none of them is at Udaypur" (8.2), "they come from elsewhere in it" (8.4), "the treatise on towns would have…" (8.5), "no list survives for Udaypur" (8.6), "the kingdom's, not Udaypur's" (8.9) and "Udaypur's own place in it is unrecorded" (8.11). The Śivarātri vow of 1217 is explicitly not read as evidence that Udaypur kept Śivarātri then (8.9).

## Canon and tiers

- **U1:** 1163 is framed under the Caulukya Kumārapāla's *mahāsādhanika* Rājyapāla, and the early 1170s under the Caulukya Ajayapāla.
- **R4:** Bhṛṅgārikā is dated to its record of 1172/1173.
- **R1–R3 and D1:** `ch_rules.py` reports 0 failures and `dynasty_spelling` is clean.
- **Tiers:**
  - CII for the grants, read through its editor ("if the reading is correct" on the *biswa*);
  - the Gazetteer as tier 7, its statements given as its own and capped at 40% per unit (8.7 and 8.8 were rebalanced with the INTACH, Geo-Heritage, Betwa and Pande items);
  - Tiwari as testimony; his police count and his conjectures about the plot are not used.
- **Boundaries:** epigraphy goes to Ch 6 (6.17, 6.18); the vedī and the Siddhānta doctrine to Ch 5 (5.3, 5.26); tanks to Ch 2 and Ch 7 (2.7, 7.24); people and the fair to Ch 9.

## A few quotations with IDs

- "taking water [in hand], donated 4 *biswa*" (C08-JAGTA-EN-010)
- "lands productive of gold and corn" (C08-GANGULY-013)
- "evidently in favour of the temple" (C08-CII-017)
- "Without these four nothing can be undertaken." (C08-KRAM-1-006)
- "the red sandstone kundies of Udaypura have a great local reputation" (C08-GAZ-014)
- "Irrigation does not ever seem to have been conspicuously used in farming in the District" (C08-GAZ-003)
- "The doctrine of the Buddha should be heard; that of the [Jain] should be practised; …" (C08-RAJABHOJ-EN-002)

All quotations are verbatim, case-sensitive. Two that repeated earlier chapters were unquoted in the line edit: "quarried in the hill close by" (2.9) and "evidently Udayeśvara" (6.18).

## Direct items set aside (13)

- C08-GAZ-011, -012 and -020: empty or partial tables.
- C08-JAGTA-HI-002, -004, -005, -007, -012, -013, -014 and -016: Hindi duplicates of the English items used.
- C08-JAGTA-EN-016 and -017: general rhetoric about prosperity and art, with no Udaypur fact.

## Checks

- **Unit checks:** all 14 units are clean under `inhouse.py`.
- **Stitch:** `stitch.py 8 --check` reports equal.
- **Canon rules:** `ch_rules.py` reports 0 failures.
- **`prose_checks.py`:**
  - no narrator period terms, passive runs or testimony measurements;
  - colon reveals were cut from 2.9 to 0.6 per 1,000 words in the line edit;
  - triplets are at 1.9 per 1,000.
- **Conflict:** the district farming share for 1961 is 75% in one Gazetteer table and 79.3% in another. Both are given in 8.7's note.

## Editorial read (14 questions)

1. **Concrete openings:** each unit opens on a gift, a rod, a basin, a lane of fields, a monastery inscription or a verse.
2. **One argument per unit:** yes.
3. **Place as subject; sources in the notes:** yes; the source-led check passes.
4. **Calibrated uncertainty:** the *biswa* reading, the 1163 gift, the drum-stone and the time-keepers' claim are each hedged once.
5. **Conflicts side by side:** 1172 vs 1173; 75% vs 79.3%; the two counts of Śaiva schools.
6. **Testimony marked:** Tiwari is marked as testimony throughout.
7. **Restraint:** every unit ends on what Udaypur's record does or does not show.
8. **No invented labour:** confirmed.
9. **Temple Economics:** contextual only (two uses).
10. **Boundaries:** handed off to Ch 5, 6, 7, 9, 10, 11 and 12.
11. **Repetition:** Chapter 1's living temple, time-keepers and brass cover are recalled in clauses.
12. **Opening from Ch 7:** the chapter opens on Dhāmadeva's water-sealed gift, after Ch 7 ended on Vikrama's tank given for merit.
13. **Close into Ch 9:** the chapter ends on the people of Udaypur.
14. **Notes:** 39 for 40 paragraphs; 8.3's last paragraph carries none.

## Deliverables

- `ch08/ch08_plan_v1.md`
- `ch08/ch08_draft_v1.md` (working draft with IDs)
- `ch08/ch08_draft_v1_footnoted.md` (39 footnotes; 18 bibliography entries, 17 still incomplete, as in earlier chapters)
- `ch08/Chapter 8 - Religion and the Material Life of Udaypur - Draft v1.docx` (14 unit headings, none empty; ends on the bibliography)
- `ch08/ch08_draft_v1_report.md` (this file)
- `run/ledger/ledger_ch8.json` → `editorial/book_ledger.*`
