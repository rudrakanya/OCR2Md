# Drafting progress (Chapter 4 to the Afterword)

*Resume file. Update after every unit or section. A fresh session reads this first, then `drafting/editorial/Udaypur_Complete_Book_Outline.md` (the whole-book outline supersedes v2, `PLAN_CH04-AW.md` and v1 for planning; v2 is kept as the record).*

## Chapter 1 rebuilt from the contents file: v6 DELIVERED (17 Oct; in-session; no API)

- **Archive.** The old Ch 1–4 drafts, outputs, run sections and ledgers are in `_archive/pre_contents_rebuild/` (README). Plans, cfgs and packs stay in place.
- **Canon carried forward.** U1, R1–R4, D1, D2 and D4, the evidence tiers, the one-home rule and the ledger are in `style/style_sheet.md` §13.
- **Ledger.** Rebuilt from the contents file and the Ch 1 v6 text: `run/ledger/ledger_ch1.json` → `editorial/book_ledger.md`. It was written by hand; `ledger.py update` is paid and was not used.
- **Ch 1 v6.**
  - 14 units, one per contents unit (`ch01/ch01_plan_v6.md`, cfg `ch01/cfg_ch01v6.py`, sections `run/ch1/1.1–1.14.md`).
  - **No word targets (user, 17 Oct):** `NO_LENGTH = True` in the cfg; `validate.py` and `inhouse.py` skip length when it is set, and the plan carries no "N w". Each unit is as long as its evidence carries.
  - Body 5,283 words (about 7,200 with notes), 303 items, 85 footnotes. All 14 units are clean under `inhouse.py check`.
  - Report: `ch01/ch01_draft_v6_report.md` (unit table, unused items with reasons, 14-question read).
  - Outputs: `ch01/ch01_draft_v6_footnoted.md` and `ch01/Chapter 1 - Udaypur - Draft v6.docx`. `_tools/stitch.py` and `build_outputs.py` point to the v6 cfg.
  - Short on evidence: 1.2 (all of its items used; the rest of the worship evidence is Ch 8's).
- **Tools changed.**
  - `validate.py`: multi-digit sections; NO_LENGTH.
  - `inhouse.py`: NO_LENGTH.
  - `ledger.py`: book-ledger header.
  - `_tools/show_items.py`: new; its regex was fixed.
- **Revision of 19 Oct (depth and craft; same 14 units).**
  - The body went from 5,283 to 6,264 words and from 303 to 332 items, including 27 new corpus items (`C01-KBN-*`, via `_tools/kb_new.py` and the new `_tools/pack_add_kbn.py`).
  - Reader-facing notes went from 85 to 62, one per paragraph, with at most one `{{note}}` per paragraph, placed at its end.
  - Familiar dynasty forms appear once, in 1.5; the first-mention rule is enforced in `_tools/dynasty_spelling.py`.
  - 1.14 now closes into Chapter 2. All 14 units are clean.
  - Report: `ch01/ch01_draft_v6_revision_report.md`.
- **Ch 2 v4 DELIVERED (19 Oct; in-session; no API; verified in-session, not by an independent model).**
  - Ten units from the contents file: plan `ch02/ch02_plan_v4.md`, cfg `ch02/cfg_ch02v4.py` (NO_LENGTH; SETTLED empty; Tiwari short name; canon rules on lichen and 1059), pack `ch02/evidence_pack_v5.json` (v4 plus 17 `C02-KBN-*`), sections `run/ch2/2.1–2.10.md`.
  - Body 5,376 words, 181 items, 36 notes (one per paragraph). All ten units are clean.
  - Closes on setting, not cause, into Ch 3. Report: `ch02/ch02_draft_v4_report.md`.
  - `stitch.py` and `build_outputs.py` point to the v4 cfg; ledger `run/ledger/ledger_ch2.json` merged (`ledger.py` header updated).
- **Ch 3 v3 DELIVERED (19 Oct; in-session; no API; verified in-session, not by an independent model).** User brief: same way, not shorter, all evidence direct and contextual.
  - Eleven units: plan `ch03/ch03_plan_v3.md`, cfg `ch03/cfg_ch03v3.py`, pack `ch03/evidence_pack_v4.json` (v3 + TEMPLE-ECON-001 + 14 `C03-KBN-*`), sections `run/ch3/3.1–3.11.md`.
  - All 156 index items and all 222 pack items cited. Body 7,357 words (v2: about 2,560), 41 notes. All units clean.
  - **For the user to confirm:** GAZ_MAX_SHARE (the 14 Oct 40% cap) is off, because all-evidence makes 3.3 (73%) and others exceed it. Temple Economics is used once (it was previously excluded).
  - Report: `ch03/ch03_draft_v3_report.md`; ledger `run/ledger/ledger_ch3.json` merged.
- **Ch 4 v3 DELIVERED (19 Oct; in-session; no API; verified in-session, not by an independent model).** Drafted fresh from the contents file (v1 archived: 5 sections, ~4,030 words, complete).
  - Twenty units: plan `ch04/ch04_plan_v3.md`, cfg `ch04/cfg_ch04v3.py` (canon rules R2/R4/D2 run by `_tools/ch_rules.py`), pack `ch04/evidence_pack_v3.json` (v2 + glosses restored from the index + 3 borrowed U1 items), sections `run/ch4/4.1–4.20.md`.
  - Body 13,693 words, 506 items (483 of 682 index items), 69 notes. All units clean; canon rules 0 failures.
  - Unused items are mostly the later Paramāras (Ch 10), plus recorded exclusions. Report: `ch04/ch04_draft_v3_report.md`; ledger `run/ledger/ledger_ch4.json` merged. The Ch 1 ledger full names for Karṇa/Bhīma were changed so they no longer clash with R2.
- **Ch 3 v4 DELIVERED (21 Oct; in-session; no API).** User brief: Udaypur-centred rewrite; the Gazetteer may supply at most 40% of any unit's items; Temple Economics is excluded again.
  - Config `ch03/cfg_ch03v4.py` (GAZ_MAX_SHARE 0.40). Five corpus items added (C03-KBN-GANGULY-001, C03-KBN-RAJABHOJ-001, C03-KBN-MADHYABHARAT-012/013/014); C01-MADHYABHARAT-001 borrowed.
  - Units 3.3, 3.4, 3.6, 3.7 and 3.8 were brought under the cap and given a stated stake in Udaypur; 3.3 was cut to 376 words (the excavation rests on the Gazetteer alone).
  - Body 7,117 words, 211 items, 40 notes; every unit at or under 40%. The v3 sections are kept in `ch03/v3_sections/`.
  - Outputs: `ch03_draft_v4.md`, `_footnoted.md`, `Chapter 3 - Before Udaypur - Draft v4.docx`, `ch03_draft_v4_report.md`. `stitch.py` and `build_outputs.py` now point to v4.
- **Ch 5 v1 DELIVERED (21 Oct; in-session; no API).** Drafted from the contents file: 28 units, body 11,800 words, 330 items (205 of 284 direct), 80 notes.
  - Plan `ch05/ch05_plan_v1.md`, cfg `ch05/cfg_ch05v1.py` (extra_rules: SAMAR never quoted, R3 1059, R2 Karṇa, Temple Economics out), pack `ch05/evidence_pack_v1.json` (index less TEMPLE-ECON, plus C04-CII-108/119).
  - Sections `run/ch5/5.1–5.28.md`; outputs `ch05_draft_v1.md`, `_footnoted.md`, `Chapter 5 - The Udayeśvara Temple - Draft v1.docx`, report `ch05_draft_v1_report.md`; ledger `run/ledger/ledger_ch5.json` merged.
  - Flag for the user: the map gloss of C05-ARTPAR-012 says Vikrama era, but the Hindi has A.D. (1063).
- **Ch 6 v1 DELIVERED (21 Oct; in-session; no API).** Dependency check: the Bühler (EI I) and Cunningham (ASR X) staged editions are uncorrected and not ingested (RR-1, RR-11, RR-12 and RR-23 open), so the hold-pending path was taken. 22 units, body 7,460 words, 262 items (152 of 223 direct), 50 notes.
  - HELD passages: 6.2 P1–P2 (RR-1), 6.4 P2 (RR-12), 6.19 (RR-11, RR-23), and the 6.22 note.
  - Files: cfg `ch06/cfg_ch06v1.py` (extra_rules: R2, R3, R4 limited to 6.18, U1, SAMAR never quoted); plan `ch06/ch06_plan_v1.md`; pack `ch06/evidence_pack_v1.json`; outputs `ch06_draft_v1*.md`, the docx and `ch06_draft_v1_report.md`; ledger merged.
- **Ch 7 v1 DELIVERED (21 Oct; in-session; no API).** Staged Beglar/Cunningham still uncorrected and not ingested; 7.2 note HELD (RR-15), 7.19 quote from the survey's text (RR-15); RR-13 (Moti Masjid) and RR-14 (V.S. 1625 pillar) open. 25 units, body 7,258 words, 220 items (160 of 239 direct), 52 notes. Plan `ch07/ch07_plan_v1.md`, cfg `ch07/cfg_ch07v1.py` (extra rule: anonymous labour; narrator 'Mohammedan'), pack `ch07/evidence_pack_v1.json` (378), sections `run/ch7/7.1–7.25.md`, outputs `ch07/ch07_draft_v1.md`, `_footnoted.md`, `Chapter 7 - The Wider Built Heritage of Udaypur - Draft v1.docx`, report `ch07/ch07_draft_v1_report.md`; ledger_ch7 merged.
- **Ch 8 v1 DELIVERED (21 Oct; in-session; no API).** Evidence-light: 14 units, body 4,753 words, 160 items (31 of 44 direct), 39 notes. Temple Economics used twice, both in 8.3, framed as south Indian comparison (cfg rule enforces). Thin units flagged: 8.5, 8.7, 8.8, 8.13. RR-17 (1163 gift, Ganguly only), RR-18 (kundies source), RR-19 (Bhilsa 878 rent) open. Plan `ch08/ch08_plan_v1.md`, cfg `ch08/cfg_ch08v1.py`, pack `ch08/evidence_pack_v1.json` (302), sections `run/ch8/8.1–8.14.md`, outputs `ch08/ch08_draft_v1.md`, `_footnoted.md`, `Chapter 8 - Religion and the Material Life of Udaypur - Draft v1.docx`, report `ch08/ch08_draft_v1_report.md`; ledger_ch8 merged; build_outputs registers 8.
- **Ch 9 v1 DELIVERED (21 Oct; in-session; no API).** 9 units, body 2,562 words (outline 2,800, U2; not padded), 75 items (26 of 31 direct), 22 notes. Oral tradition told as memory; no residents named (cfg rule); 9.1 and 9.2 flagged for the Ch 11–12 legal review. RR-20, RR-21 open. Plan `ch09/ch09_plan_v1.md`, cfg `ch09/cfg_ch09v1.py`, pack `ch09/evidence_pack_v1.json` (93), sections `run/ch9/9.1–9.9.md`, outputs `ch09/ch09_draft_v1.md`, `_footnoted.md`, `Chapter 9 - Society and Cultural Life - Draft v1.docx`, report `ch09/ch09_draft_v1_report.md`; ledger_ch9 merged.
- **Ch 10 v1 DELIVERED (21 Oct; in-session; no API).** Dependency RR-2 (V.S. 1841 brass cover) still OPEN, so 10.9 P2 is HELD: V.S. 1841 as reported vs 1775 set side by side, cfg rule bars a settled date. 12 units from the contents file (v2's six sections redistributed; opens from 9.9, closes into 11.1), body 6,307 words, 197 items (36 of 61 direct; 99 of 176 index), 39 notes; Gazetteer ≤40% in every unit (max 38%, 10.11). Later Paramāras (Ch 4 S6 items) in 10.1–10.2; U1 framing in 10.1; political demotion shown as a dated ladder, economic decline stated undatable (10.12). 6 new kb-new slices (C10-KBN-MADHYABHARAT-005–009, C10-KBN-JAGTA-EN-001). For the user: RR-2; the title word *qasba* (no period record uses it); Udaypur's pre-1948 state (Gwalior vs Nawab's Basoda) not stated. Plan `ch10/ch10_plan_v1.md`, cfg `ch10/cfg_ch10v1.py`, pack `ch10/evidence_pack_v1.json` (341), sections `run/ch10/10.1–10.12.md`, outputs `ch10/ch10_draft_v1.md`, `_footnoted.md`, `Chapter 10 - Political Change and Economic Decline - Draft v1.docx`, report `ch10/ch10_draft_v1_report.md`; ledger_ch10 merged; stitch/build_outputs register 10.
- **Ch 11 v1 DELIVERED (21 Oct; in-session; no API).** 8 units from the contents file (v2's six sections redistributed), body 3,550 words (about 4,750 with notes; outline 4,250, not a target), 125 items (75 of 92 direct), 27 notes. Staged Beglar/Cunningham/Bühler/Gwalior 1925–26 still uncorrected and not ingested: HELD notes in 11.1 P1 (RR-8, RR-15), 11.1 P4 (RR-1, RR-12, RR-32) and 11.2 P2–P3 (RR-32). Legal review: 11.3 (spending, new LR-3), 11.4 (two households), 11.6 (palace notice and 15 Jan 2021 order; LR-1, U7), 11.7 (theft, police), 11.8 (mining, LR-2: one attributed sentence, cfg-enforced). Found: Tiwari dates ASR VII to 1874–77 but it is Beglar's 1871–72 tour; **Ch 1 §1.11 repeats the error** (light fix). 11.6 keeps two reviewed flags (the order's own date). Plan `ch11/ch11_plan_v1.md`, cfg `ch11/cfg_ch11v1.py`, pack `ch11/evidence_pack_v1.json` (158; `build_pack_v1.py`), sections `run/ch11/11.1–11.8.md`, outputs `ch11/ch11_draft_v1.md`, `_footnoted.md`, `Chapter 11 - Udaypur in the Modern Period - Draft v1.docx`, report `ch11/ch11_draft_v1_report.md`; ledger_ch11 merged; stitch/build_outputs register 11.
- **Ch 12 v1 DELIVERED (21 Oct; in-session; no API).** 10 units from the contents file (v2's six sections redistributed), body 3,202 words (outline 3,750, not a target), 120 items (62 of 71 direct), 33 notes; opens from 11.8's close. Wildlife in 12.5. No residents or signboard claimants named (cfg rule); Tiwari's counts/widths/distances not used; mining allegation not repeated (book's one sentence is 11.8, U7); C12-JAGTA-EN-007 (green cloths, pīr) not used, for the user's ruling. Legal review: 12.3 P3, 12.4 P3, 12.6 P2–P3, 12.7 P1/P3, 12.8 P2–P3, 12.9 (all), 12.10 P2. RR-30 partly resolved: Hindi pp. 161–162 are Shivkumar Vivek's post (20 Feb 2022), pp. 163–166 Ajit Vadnerkar's; **Ch 1 §1.1 misattributes C01-JAGTA-EN-015 ('cannot even be called a town') to Tiwari** (light fix). Two accepted date-of-observation flags (12.7, 12.8; RR-28). 16 kb-new slices C12-KBN-JAGTA-EN-001–016. Plan `ch12/ch12_plan_v1.md`, cfg `ch12/cfg_ch12v1.py`, pack `ch12/evidence_pack_v1.json` (140), sections `run/ch12/12.1–12.10.md`, outputs `ch12/ch12_draft_v1.md`, `_footnoted.md`, `Chapter 12 - Udaypur Today - Draft v1.docx`, report `ch12/ch12_draft_v1_report.md`; ledger_ch12 merged (header names Ch 11–12); stitch/build_outputs register 12.
- **Afterword v1 DELIVERED (21 Oct; in-session; no API).** 12 units from the contents file (v2's AW.1–AW.6 redistributed), numbered 13.1–13.12 for the tools, printed unnumbered under "AFTERWORD" (cfg CHAPTER_LABEL / NUMBERED_HEADINGS, new optional settings in `make_docx.py`). Body 3,247 words (outline 2,750, U2; not padded), 125 items (55 of 58 direct), 26 notes. Reflective register bounded: proposals attributed; one test label (13.11) and one argument label (13.12, conservation by use); no new facts. Drafted against Chs 11–12 before they existed; Ch 11 v1 and Ch 12 v1 appeared mid-session and every recall was checked against them (notes say HELD: re-check when final). RR-30 resolved by the Ch 12 plan (Vivek pp. 161–162, 20 Feb 2022 = latest dated item; Vadnerkar pp. 163–167; p. 170 Tiwari) and all attributions corrected; RR-31 (survey date) open, inferred 2021 or later via C13-KBN-GEOHER-001. Legal review: 13.1, 13.2, 13.5 (LR-2), 13.7, 13.8, 13.10, 13.11 (LR-1). Files: plan `ch13/ch13_plan_v1.md`, cfg `ch13/cfg_ch13v1.py`, pack `ch13/evidence_pack_v1.json` (130), sections `run/ch13/13.1–13.12.md`, outputs `ch13/ch13_draft_v1.md`, `_footnoted.md`, `Afterword - Conserving Udaypur - Draft v1.docx`, report `ch13/ch13_draft_v1_report.md`; ledger_ch13 merged (header ends "and the Afterword (v1)"). For the user: Ch 11 ledger lists Suresh Mishra as living, but his death is recorded.
- **Ch 6 v2 (22 Oct; reviewer fix; no API, no embedding).** 6.9 rewritten from Saarthak Singh's serpentine-scimitar paper (already in production Chroma as `A_serpentine_scimitar_of_letters_from_Ud.md`, 5 chunks; same paper as `Udaypur Reference Markdown Files/serpentine-scimitar-inscription-udaypur.md`); new items C06-KBN-SERPENT-001–033 carry Chroma chunk IDs; knock-on fixes in 6.10/6.15/6.16/6.22. cfg `ch06/cfg_ch06v2.py`, pack v2, report `ch06/ch06_draft_v2_report.md`; stitch/build_outputs point at v2. Open: Sastri EI XXXI (source of *siddhāsiputrikā*) not in corpus; DB author for the paper is wrong ('Singh, A.').
- **Ch 6 v3 DELIVERED (22 Oct; in-session; no API).** All 22 units deepened from their own evidence (body 7,954 → 12,361 words; 498 distinct items; 179 new C06-KBN-<CODE>-<A–E>-NNN slices, kept in pack v3 and `ch06/_work/kbn_<G>.jsonl`), then joins/author's pass/line edit. 14 units FULL; LIMITED: 6.2 (HELD RR-1), 6.8 (Udaypur part), 6.16 (no porch catalogue), 6.19 (HELD), 6.20 (no Persian text), 6.21 older lines. 22/22 checks clean, ch_rules 0, ledger merged, 75 footnotes. Files: cfg_ch06v3, plan v3, pack v3, ch06_draft_v3*.md, docx v3, `ch06_v3_evidence_inventory.md`, `ch06_draft_v3_report.md`. stitch/build_outputs point at v3. Open: re-OCR CII p. 112/p. 130 and INTACH pp. 22–26; Sastri EI XXXI.
- **Next:** the user's review of Ch 1 v6, Ch 2 v4, Ch 3 v4, Ch 4 v3, Ch 5 v1, Ch 6 v1, Ch 7 v1, Ch 8 v1 and Ch 9 v1; legal review of 9.1–9.2 with Ch 11–12; the user's hand-correction of the staged Bühler, Cunningham and Beglar editions, which would release the HELD passages of Ch 6 and Ch 7. Ch 5 onwards are to be drafted the same way from the contents file when the user asks; the same NO_LENGTH change applies to their cfgs.

## PAUSED for outline consolidation (16 Oct, user brief "Pause drafting; build one whole-book outline")

- **No chapter drafting or fixing** until the user lifts the pause. Ch 5, 7, 8, 9 not started.
- **Finished before the pause (decisions of 16 Oct):**
  - D1 IAST dynasty names in Ch 1–4, familiar forms once in §1.2, rule in `style/style_sheet.md`, check `_tools/dynasty_spelling.py` (inside `inhouse.py check`);
  - D2 kinship "Bhoja's brother" (Dōngargāon 1112, Jainād; C04-CII-105, -086, -132) in §1.2 and §4.3, canon updated (book outline, cfg, pipeline3, style profile);
  - D4 Nagpur Karṇa note in §1.2 (C04-CII-094, -095);
  - outputs of Ch 1–4 rebuilt.
- **D3 (Ch 4 to six sections) paused mid-way, at a section boundary:** plan `ch04/ch04_plan_v2.md`, cfg `ch04/cfg_ch04v2.py`, revised §4.1 in `ch04/v2_work/4.1.md` (720 w, checked clean). The delivered Ch 4 stays draft v1 (five sections; `run/ch4/`, v1 cfg); v1 section backup in `ch04/v1_sections/`.
- **Exclusion spot-check (task 2) done:** error rates Ch 4 10.3% (re-audited all), Ch 7 5%, Ch 5 11.1% (re-audited all), Ch 10 0%; reassignments in the v2 entries and `excl_chNN.tsv`.
- **Not started:** local public-domain corpus (task 3), outline/register updates (task 4).
- **Team edition of the outline (16 Oct, user brief "cut the fluff"):** `editorial/Udaypur_Complete_Book_Outline.md` (+ `.docx`) is now a lean ~12,000-word team document: spine (Paramāra line, Udaypur timeline, chain of chapters, threads), house rules in plain words, 13 chapter entries in one shape (Chs 1–4 restructured to six sections each as the target for revision, D7), tasks and checklist. No item IDs or file references. The item-level version is kept at `editorial/wholebook/Udaypur_Complete_Book_Outline_detailed_16Oct.md`; `_tools/assemble_wholebook.py` would overwrite the team edition, so point its OUT at the detailed file before rerunning.
- **Whole-book outline (item-level) DONE (16 Oct):** `editorial/Udaypur_Complete_Book_Outline.md` (about 45,300 words; 13 entries; Ch 1–4 as written, Ch 5–AW planned), `editorial/ABOUT_THIS_BOOK.md` (474 words), `editorial/OUTLINE_WHOLEBOOK_CHANGES.md`.
  - Sources in `editorial/wholebook/` (`entry_text_ch01–04.md` hold the hand-reconciled points; `excl_chNN.tsv` the reasons).
  - Rebuild: `_tools/reconcile.py` → `_tools/delivered_entries.py` → `coverage_v2.py NN` with `UDAY_OUTLINE_DIR=wholebook` → `_tools/assemble_wholebook.py` (QC in `wholebook/qc_wholebook.md`).
  - Coverage: 1,789 direct items, 1,112 assigned / 90 cross-ref / 587 excluded, none unreasoned; no item primary in two units; all section references resolve.
  - Decisions now needed: D5 (Ch 2–3 below floor), D6 (light-touch fixes RR-42: §2.1 duplicated fragment; *mahāsādhanika* gloss in §1.2), D7 (resume the Ch 4 revision).
  - The v2 outline stays the record; do not run `assemble_v2.py` (it would overwrite it).

## Standing decisions (user, 15 Oct 2026)

- **U1 (done):** Ch 1 §1.2/§1.3 corrected. Rājyapāla and Lūṇapasāka governed for the Caulukya kings. `.docx` files rebuilt.
- **U6:** "1080 is the earliest firm date; 1059 is a reading". 4.4 must say whose reading 1059 is and why it is less secure.
- **U2–U4:** Ch 9 ~2,800 words; Afterword ~2,750; §7.1 ~1,050. Never pad.
- **U7:** one attributed sentence on Tiwari's mining allegation, naming no one accused; no claimants named from the 2021 signboard. Flag those passages in Chs 11–12 for legal review.
- **Budget: no OpenAI API calls of any kind** (no judge, verify, re-verify, final read or embeddings).
  - Gap-filling uses free local text or BM25 search over `Udaipur Books Markdown files\` only. Each new item is sliced verbatim by code, with its page taken from the marker in force, and tagged `kb-new` with its tier.
- **Verification is in-session:**
  - check each claim against its cited item;
  - match each quotation verbatim against its source file;
  - log anything unverifiable as a flag;
  - run the free code checks.

  Each chapter's deliverables must state "verified in-session, not by an independent model".
- **Order:** the unified plan (`PLAN_CH04-AW.md`) → the user's approval → Ch 4 drafted section by section → the following chapters in book order without further plan approvals unless the structure changes. Ch 10 needs the V.S. 1841 brass-cover check; flag it if still open.

## Done

- Master outline: `drafting/editorial/Chapter_4_to_Afterword_Master_Drafting_Outline.md` (15 Oct).
- U1 edits (15 Oct): `run/ch1/1.2.md` and `1.3.md`, plus `ch01/ch01_draft_v5.md`.
  - The pack was extended with C08-GANGULY-015/-016, C10-CII-002 and C10-PARTEMPLES-001.
  - Free checks: no problems.
  - `build_outputs.py` rebuilt the Ch 1–3 `.docx` and the combined document (88 footnotes).
  - Ledger entries updated.
  - Backups: scratchpad `u1_backup/`.
- Evidence index (15 Oct): `drafting/_tools/index_evidence_maps.py` → `drafting/evidence_index/ch04…ch13.jsonl` and `_summary.md`. Checks: all counts match the map tables, no duplicate IDs, all IDs are in the log (`BUILD_CHECKS.md`).

## In progress

- `PLAN_CH04-AW.md`: see its status table. Built by `drafting/_tools/plan_qc.py` from `editorial/plan_work/` (`head_chNN.md`, `sections_chNN_edited.md`, `tail_chNN.md`; the closing sections come from `plan_closing.md`).
  - Sections are generated by `_tools/build_plan.py` (→ `sections_chNN.md`) and edited into `_edited`.
  - Evidence tools: `_tools/quotes.py` (prints quotations) and `_tools/coverage.py NN [maxtier]` (direct items the plan does not use).
- **Ch 4 planned, QC passed (15 Oct).** The evidence pass added C04-CII-082 (CII's two lists of the three enemies), C04-BHOJA-TIMES-038 (Nagpur "kinsman"), the U6 instruction in 4.4 P2, and fixes to source-led guidance.

- **All 10 units planned (15 Oct).** QC is green except **Ch 10 §10.5: Gazetteer 27/42**, which needs the user's ruling R1 (default: accept).
  - 22 duplicate establishing uses were demoted by the home rule (`_tools/demote_dupes.py`).
  - kb-new: C10-KBN-MADHYABHARAT-001 to -004 (`evidence_index/kb_new.jsonl`).
  - Moved: C10-GAZ-041/-042/-045/-046/-047 to 11.2; C10-GAZ-052/-053 to 12.1; C10-GEOHER-001 to 7.1 P4.
  - **Do not rerun `build_plan.py` or `fill_unit.py`:** they would overwrite the hand edits in `sections_chNN_edited.md`. Edit `_edited` directly, then rerun `plan_qc.py`.

## Ch 4 drafting: DELIVERED (16 Oct; in-session; no API; verified in-session, not by an independent model)

- **Files:**
  - `ch04/ch04_draft_v1.md`, `_footnoted.md`, `.docx`, `ch04_report.md`, `ch04_flags.md`, `ch04_plan_v1.md`;
  - `cfg_ch04v1.py` (BUDGET 0); pack `evidence_pack_v1.json`;
  - sections in `run/ch4/`;
  - ledger `run/ledger/ledger_ch4.json`, merged.
- **Words:** 4,026 against the 5,000 target, below the 4,750 floor, not padded (4.1 659 · 4.2 701 · 4.3 864 · 4.4 887 · 4.5 915). The reason is in the report.
- **Checks:** all sections clean except 6 accepted source-led flags (the Gazetteer as its own by the user's rule; U6 in 4.4).
- **Tools changed:**
  - `_pipe/build_outputs.py --chapters N` builds one chapter without the combined document;
  - `_pipe/ledger.py` merge header now reads "Chapters 1–4".

  `ledger.py update` makes a model call: do not run it; write `ledger_chN.json` by hand and run `merge`.
- **Open for the user:** the length (accept or other); the kinship canon against CII's "definitely brother"; the 1059 witnesses (page-image check and staged sources).
- **Next:** Ch 5, from `PLAN_CH04-AW.md` (Ch 5 unit), following the same workflow, unless the user rules otherwise.


## Master outline v2 (done, 16 Oct)

- **Deliverable:** `editorial/Chapter_4_to_Afterword_Master_Drafting_Outline_v2.md` (about 34,700 words; v1 unchanged). Changes: `editorial/OUTLINE_V2_CHANGES.md`. QC log: `editorial/plan_v2/qc_v2.md`.
- **Sources:** `editorial/plan_v2/` holds `front.md`, `baseline.md`, `part1.md`, `chNN.md` (entries 04–13), `changes_v1.md`, `parts3_6.md`, `excl_chNN.tsv` and `coverage_chNN.json`.
- **Rebuild:** run `_tools/coverage_v2.py NN` for each unit, then `_tools/assemble_v2.py`. It writes the outline (with the generated status table, Contents and Appendix) and the QC log.
- **Structure:** 65 sections, 38,850 words (Ch 4 6/5,000 · Ch 5 7/4,000 · Ch 6 8/4,050 · Ch 7 7/4,250 · Ch 8 7/3,800 · Ch 9 6/2,800 · Ch 10 6/4,200 · Ch 11 6/4,250 · Ch 12 6/3,750 · AW 6/2,750).
- **Coverage:** every direct item is assigned, a cross-reference or excluded with a reason; none is unreasoned. `checks_v2.py` is clean, with two accepted R8 warnings (§8.5, §10.5).
- **Step 2 corrections** (logged in the changes file, §4):
  - §1.2 Karṇa named by dynasty;
  - the Ch 1 and Ch 2 plans dated (R4, R1/R3);
  - Ch 4 §4.3 and §4.4 R2 fixes (spelling aligned to "Caulukya" 13:15);
  - outputs rebuilt.
- **Waiting on the user:**
  - D1 (spelling);
  - D2 (kinship canon);
  - D3 (Ch 4 restructure to 6 sections: not done until decided);
  - D4 (Ch 1 interpretive items).
- **Next:** on D3, either revise Ch 4 to the v2 structure, or keep it and plan Ch 5 from the v2 entry (Part IV workflow, no API).

## Next (superseded by the user's 16 Oct brief: draft Ch 4)

1. **Wait for the user's approval** of the unified plan (the Ch 4 portion, the closing sections, the structural changes) and ruling R1.
2. Then draft Ch 4. Create `drafting/ch04/cfg_ch04v1.py` (model: `ch03/cfg_ch03v2.py`) and the evidence pack (`_pipe/extend_pack.py` from the plan's IDs). Write `run/ch4/4.1.md`… in order, with in-session verification. Do not run the paid `inhouse.py` commands.

## Open flags (book-wide; the single list is the v2 outline's Part V, Research Register: RR-1 to RR-33, RR-K, LR-1, LR-2)

- The V.S. 1841 brass cover (Ch 10).
- The V.S. 1366 record; the 1163 / V.S. 1220 record(s); the V.S. 1116 / "1513" / V.S. 1562 records.
- The farman; the 1901 census figure; the GEOHER survey's date.
- The speakers at Tiwari pp. 161–170.
- Legal review: Chs 11–12.
