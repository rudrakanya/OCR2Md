# Chapter 6 — draft v2 report (22 Oct 2026)

**Scope.** Reviewer: the serpentine-scimitar inscription (6.9) was glazed over and partly wrong. v2 rewrites 6.9 from Saarthak Singh, "A serpentine scimitar of letters from Udaypur, district Vidisha, M.P." (`Udaypur Reference Markdown Files/serpentine-scimitar-inscription-udaypur.md`). It also makes small consistency fixes in 6.10, 6.15, 6.16 and 6.22. All other sections are unchanged from v1. No API spend and no re-embedding.

## Step 1: the source in the vector database
- `serpentine-scimitar-inscription-udaypur.md` is not in `udaypur_corpus_openai_large` under that name.
- The same paper is there as `A_serpentine_scimitar_of_letters_from_Ud.md`, in 5 chunks (indices 0–4). Those chunks hold about 1,804 of the paper's roughly 1,825 words: abstract, full body, references and figure captions.
- The word-level diff shows only OCR and format differences: italics, page markers, curly quotes, "Abstract:"/"Keywords:" labels, and a few diacritic slips in the OCR copy (varṇṇaṇāgakṛpānikā, krppānikām, siddhāṣiputrikā). There is no difference of content, so nothing was embedded and there is no cost.
- Database metadata faults on this source:
  - `author` is "Singh, A." where it should be Saarthak Singh.
  - `heading_path` on the body chunks is "Keywords:".
  - `primary_chapter` is C10, from the old 18-chapter plan.

## New evidence (pack v2 = pack v1 + 36 items)
- `C06-KBN-SERPENT-001…033`: verbatim slices of the reviewer's file. Each carries `chunk_id`/`chunk_index` (the Chroma chunk(s) holding the same text, matched by 4-word shingles at full overlap), `db_source_path` and the page from the ingested copy.
- `C06-KBN-CII-001…003`: CII VII.2 p. 141 n. 2 (Sircar's Bandhu, rejected) and p. 142 (the Ujjain base with the *anusvāra*; 21 + 18 endings).
- Chunk IDs were also added to C06-SERPENT-001…009, C06-CII-052, -055, -058 and -059.

## Corrections to v1 §6.9
1. **Five lines.** v1 said the five lines "name" the diagram. In fact they are two inscriptions: three lines near the middle, which are unread, and a two-line verse near the top. Only the verse names it.
2. **The object of protection.** v1 called it "lost". The source says it is "unclear", and the agent survives only as *–pālaḥ*.
3. **Noun endings.** v1 said "all seven cases". The source says "seven classes", the term CII also uses.
4. **The base.** v1 had "three aspirate sounds" only. Now it also notes the missing *anusvāra* and the repeated *ra, ya, u* of the left leg, which v1 had only in a note.
5. **Removed unsupported claim.** v1's "the only inscription at Udaypur that is itself a grammar" is in no source.
6. **The name.** v1 spelled it *varṇa-nāga-kṛpāṇikā*. It is now *varṇanāgakṛpāṇikā* (standard IAST) in 6.9 and 6.10, with the inscription's own *varṇna-nāga-kṛpāṇikāṃ* in the note. The ledger term was renamed to match.
7. **The author.** v1's notes said "A. Singh", copied from the bad database metadata. They now say Saarthak Singh in 6.9, 6.10, 6.15, 6.16 and 6.22. "Singh" alone is ambiguous with Mahesh Singh.
8. **Added from the source:**
   - the outer *prākāra* at the south projection;
   - the reversed setting, with the *vedikā* face outward;
   - the probable resetting in restorations;
   - the Ujjain verse "marked with Udayāditya's name" and the "friend of talented poets";
   - ll. 24–26 of the Ujjain inscription (*siddhāsiputrikā*, *varṇasthityai*);
   - the date after 1093, and the last decade of the century;
   - the triad of aurality, visuality and efficacy.
9. **Royal name.** New: the Udaypur verse, as read, names no king. Its royal name and date come from its fellows.
10. The palaeography detail now sits only in 6.15. 6.9 points to it, so it is no longer repeated.

## Knock-on fixes
- **6.10.** "Four temples of the kingdom carried the same chart under Udayāditya's name" was wrong twice over. The Dhār charts stand in the Bhojaśālā, not a temple, and the Udaypur verse names no king. The sentence is rewritten. The Ujjain-verse quotation that 6.9 now covers is cut to a recall clause, and the term is no longer glossed a second time.
- **6.22.** "a serpent of letters set up in the king's name" now reads "whose twins elsewhere carry the king's name".

## Reviewer claims and the corpus
- **Ujjain parallel.** In Singh, and independently in CII VII.2 (No. 25; C06-CII-052/-055, C06-KBN-CII-001/-002). CII agrees that "friend of talented poets" refers to Naravarman and rejects Sircar's Bandhu.
- **Dhār/Un.** In Singh as "three similar"; independently in CII (two Dhār charts, one Un) and in Adhikari.
- ***siddhāsiputrikā*.** Only in Singh, citing Sastri, EI XXXI (1960). That edition is not in the corpus, and CII does not use the word. Flagged in the note and in the ledger's open questions.
- **"Identical in all details".** CII's Ujjain base has the *anusvāra*; Singh's Udaypur base has none. Noted, not resolved.
- **Dynastic-power reading.** This is Singh's interpretation. CII, Ganguly and Adhikari hold the schoolroom view. It stays as a debate in 6.10, not as fact in 6.9.

## Checks (free)
- `inhouse.py check`: all 22 sections clean.
- `ch_rules.py`: 0 failures.
- The remaining ledger notes in 6.10 and 6.22 are "figure may conflict" heuristics. The 6.22 one was already raised on v1. The extra one in 6.10 is set off by the "6.9" cross-reference.
- Ledger: Ch 6 terms and figures added, plus three open questions; `ledger.py merge` run.
- Build: 53 footnotes, up from 50. The 15 incomplete bibliography entries are unchanged from v1.

## Files
- cfg `ch06/cfg_ch06v2.py`, plan `ch06/ch06_plan_v2.md`, pack `ch06/evidence_pack_v2.json`.
- Draft `ch06/ch06_draft_v2.md`, `ch06/ch06_draft_v2_footnoted.md`, `ch06/Chapter 6 - Inscriptions and Intellectual Life - Draft v2.docx`.
- v1 copies of the changed sections and the ledger are in `run/ch6/_v1/`.
- `stitch.py` and `build_outputs.py` now point Ch 6 at cfg v2.
