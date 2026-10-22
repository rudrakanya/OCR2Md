# Shared brief for the Chapter 4 – Afterword master-outline pass

*For the chapter-outline subagents, 15 October 2026. Read all of this before opening the evidence.*

## 0. What you are producing

A **chapter outline draft** for the chapter(s) assigned to you. The editor will merge the drafts into the master drafting outline, `drafting/editorial/Chapter_4_to_Afterword_Master_Drafting_Outline.md`.

That document is the blueprint from which later model passes will draft the chapters, section by section. A drafting model reading your outline, the evidence items you cite and the style files must be able to write each section **without making structural decisions of its own**. Do not write chapter prose. Control architecture, evidence, argument, sequence and transitions; leave the sentences to the drafting stage.

Work only from files. **Never call any model API.** Don't run `drafting/_pipe/*.py` scripts that make calls (`inhouse.py judge|verify|reverify|finalread`, `chapter_flow.py`, `orchestrator.py`, `pipeline3.py`, `ledger.py build|update`, `kb.py`). Python for reading and splitting text is fine: run it with `python -I -X utf8`.

Project root: `C:\Users\User\Desktop\Anugrah\OCR2Md` (Windows; paths contain spaces, so quote them).

## 1. Your evidence sources, in this order

1. **The evidence maps, the user's principal source.** They are extracted from `Udaypur Evidence Mapping Documents/*.docx` into `drafting/editorial/outline_work/`:
   - `cNN_direct.txt`: items that bear directly on the chapter;
   - `cNN_contextual.txt`: wider context.

   Each item is a verbatim quote (lines starting `> `, or the paragraph above the ID line) followed by its ID line, for example `C04-JAGTA-EN-002   ≈ p. 140 (Hindi original)`. Read your chapter's files **closely and in full**: don't sample, and don't stop at headings. Books are grouped under `## Title (CODE, n)` headings.
2. **The per-chapter rendering of the same map:** `drafting/chNN_*.md`. It holds the same items with the same IDs, plus fields the Word documents drop:
   - sub-topic;
   - strength;
   - claim;
   - relevance note;
   - "also Ch N" cross-references.

   It also has sections:
   - `## 2. Evidence summary` and `### Sub-topic index`, the chapter's sub-topics S1…Sn with item IDs (direct first);
   - `## 4. Cross-references (items homed in other chapters)`;
   - `## 5. Conflicts and variant statements (side by side, unresolved)`;
   - `## 6. Gaps (to-do)`.

   Use these to find the sub-topic structure, the conflicts and the gaps, and to look an item up by ID (grep the ID).
3. **Structure and decisions** (in this order of authority):
   - `chapters.md`: **the single authority on chapter titles, scope and order.** No chapter is split or merged. The 13 units stand. Later Paramāra history (1093–1305) belongs in **Chapter 10**. Udaypur's tanks, *kund*s and stepwells **in detail**, and the lichen-dating proposal for the fort wall, belong in **Chapter 7**. The hill's wildlife (birds, bats in the caves, the 1968 shooting block) belongs in **Chapter 12**.
   - `drafting/editorial/ROADMAP.md`: the decisions log and the open issues, numbered 1–20.
   - `drafting/editorial/CH1-3_DELIVERY_REPORT_2026-10-15.md`: the latest state of Chapters 1–3 and their open issues.
   - `Detailed Udaypur Book Outline.md` (17 Sept 2026): the **older 18-chapter canon**. Its old chapters map onto the current ones; `chapters.md` gives the mapping in italics under each chapter, e.g. Ch 4 = "Remaining C5 + C6 + C7". Use its section ideas, committed measurements and gap notes, **but these parts are superseded and must not be followed:**
     - "Udayāditya … founded … 1059 … eleven years before he became king" stated as fact. Now **1059 (V.S. 1116) is a reading of the temple inscriptions**; the CII editor counts the 1080 (V.S. 1137) record as the earliest known date for Udayāditya. The accession is **c. 1070, the working position**. "Founding before kingship" is a real question to argue (see Ch 1 §1.2 and §1.4), never a settled premise.
     - "a nephew of Bhoja". The canon is now **"a kinsman of Bhoja; the exact relationship is disputed"**. Never write "nephew".
     - "the book … does not hedge". The current house voice uses **graded confidence** (see `style_profile.md` §D).
     - The **1310 Udaypur inscription** and the **1645 Qanungo Baoli slab** were dropped from Chapter 1. If your chapter's evidence uses them, check what the map actually says about them (date, provenance, reliability) and flag them; don't adopt the old canon's framing unexamined.
     - The canon's **"do not import Mandu's Moti Darwaza or Sher Khan stepwell"** note conflicts with Chapter 1 §1.3. That section, from items C07-MADHYABHARAT-011/012 and C01-KB-MADHYABHARAT-*, says that just outside Udaypur's eastern gate, Moti Darwaza, an agent of Sher Khan built a small mosque in the Mandu style in 1488. Flag this conflict where it touches your chapter.
4. **Style and conventions:**
   - `drafting/style/style_profile.md`: the house voice (binding);
   - `drafting/style/style_sheet.md`: copy conventions;
   - `drafting/ch01/ch01_plan_v5.md`, `drafting/ch02/ch02_plan_v3.md`, `drafting/ch03/ch03_plan_v2.md`: **the current plan format**. Each chapter has a historical question, a through-line and an arc; each section has a section statement ("By the end, the reader knows …"), a purpose and a paragraph plan; each paragraph has a **Point** (the historical work it must do) and **E / C / X** evidence roles.
   - **Delivered Chapters 1–3,** the final working drafts with evidence IDs: `drafting/run/ch1/1.1.md` … `1.5.md`, `drafting/run/ch2/2.1.md` … `2.5.md`, `drafting/run/ch3/3.1.md` … `3.5.md`. Read the sections that touch your chapter's material so you know exactly what the reader has already been told.
   - `drafting/editorial/book_ledger.md`: people, terms and places already introduced, with section of first mention; committed figures; open questions.

## 2. Binding rules (from the user)

- **Udaypur is the centre of gravity.** The Paramāra world and Central India are the frame. They enter where they change what Udaypur means.
- **Never invent evidence.** Cite only item IDs that exist in the maps; check every ID by grep. Never invent page numbers. Use the locator exactly as the item gives it ("p. 236", "≈ p. 140 (Hindi original)", "[page not recorded]").
- **Evidence tiers** (strongest first, for medieval events):
  1. contemporary inscriptions (CII VII.2), read critically;
  2. fabric and archaeology;
  3. later inscriptions;
  4. documents and normative texts;
  5. modern scholarship (Ganguly, Pande, Hardy, Kramrisch, Patil, Adhikari, Sharma, Mahesh Singh);
  6. colonial observation;
  7. modern survey and the 1979 Gazetteer (GEOHER, INTACH, GAZ);
  8. tradition and Tiwari's testimony (JAGTA-EN/-HI) and the Skanda-Purāṇa;
  9. popular or heritage accounts (RAJABHOJ-EN, BHOJDEV-HI, PARMAR-RAJPUT);
  10. the book's own inference.

  **CII outranks Ganguly** on dynastic facts. Where Ganguly interprets rather than reports, attribute it to him in a note.
- **Tiwari** (*Jagta Hua Kasba*, JAGTA): testimony and memory.
  - Never a medieval fact, a measurement, a distance, a count or a date.
  - Named in full only once in the book (Ch 1 §1.1); thereafter "Tiwari".
  - No gendered pronouns; never "a visitor".
- **SAMAR** (the *Samarāṅgaṇasūtradhāra*) items are ⚠ old OCR: never quote them, only paraphrase cautiously. It is a normative text, never a record of why Udaypur was built. Its attribution to Bhoja is doubted; say so where it is used.
- **Temple Economics is excluded entirely.** Its "Udaipur" is in Rajasthan. Watch for any Mewar, Rana, Rajasthan or Pichola leaks.
- **A praśasti is panegyric:** its claims are claims. **A tradition is evidence for memory,** not for the event it tells. **A survey's dates are proposals.**
- **Compatibility is not identity.** Never merge two inscriptions, buildings, tanks, traditions, rulers, places, layers or hypotheses unless an item says they are the same. In particular:
  - the hill's tentatively read two-line inscription (C01-KB-GEOHER-013, C03-KB-GEOHER-002) is not the cave's undeciphered lines (C01-KB-INTACH-002, C03-KB-INTACH-002);
  - the Udaysagar is not identified with the Udayasamudra unless an item says so;
  - Udayagiri (near Vidisha) is not Udaypur.
- **No fiction:** no thoughts, motives, scenes, weather, emotions, sensory detail, journeys or invented causation. No invented anonymous agents: no "builders" or "quarrymen" from a passive "was quarried". The land is a setting, never the cause.
- **Disagreements:** the text keeps the question; who argues what goes in a `{{note: …}}`. Minor numeric differences become ranges. Settled ranges:
  - 13–16 km from Ganj Basoda;
  - 55–70 km from Vidisha.
- **Spelling:** "Udaypur" for this town; "Udaipur" only for Rajasthan. Diacritics: Udayāditya, Udayeśvara, Paramāra, *praśasti*, Dhārā, Bhūmija. Narrator's voice uses "Muslim" (never "Mohammedan" outside a quotation).
- **Length:** chapters run 3,200–4,400 words. Sections are about 500–950 words each, typically 4–5 sections, landing at 70–120% of target. **Never pad:** if the evidence is thin, plan a shorter section and say so.

## 3. Already told in Chapters 1–3 (do not re-tell; recall in a clause at most)

**Chapter 1**
- **1.1:** the approach; the village and the 2011 census; the walled city and the gates; the time-keepers' house (Ghariyālon Kā Makān); the water tally (56 stepwells, 52 wells, 12½ lakes, as memory); Berni Mata and the dancer legend; the temple still in worship; the fair; Hindus and Muslims at the shrine in the 1870s; the name confused with Udaipur; the snake-and-fire founding legend.
- **1.2:** the Paramāras as a polity; Dhārā; the eastern reach to Bhilsa; Bhoja's death and the occupation; Jayasiṃha regains the throne with Chālukya help and dies; Udayāditya recovers the kingdom, c. 1070, a kinsman of Bhoja (with the note of readings); the Nagpur boar image; the realm to Jhalrapatan, Bhilsa and Nimar; Kalacuri records calling him king of Malwa; the triple naming (Udayapura, Udayeśvara, Udayasamudra) and Nīlakaṇṭheśvara; V.S. 1116 and V.S. 1137 read as dates; the question "lord's seat or new king's undertaking"; *maṇḍala*s, *bhoga*s and *pāṭhaka*s; the Bhāillasvāmi-mahādvādaśaka; Rājyapāla's eastern headquarters at Udayapura; the "house it names" (Nemak) reading.
- **1.3:** Yaśovarman and the Caulukya capture; Candella Madanavarman at Bhāillasvāmin, 1134; the *mahākumāra* branch; Lūṇapasāka's grant (early 1170s); Devapāla residing at Udayapura (1230s); Jayavarman at Bhilsa, 1263, and Pathari, 1269; Iltutmish; ʿAin-ul-Mulk and 1305; the mosque of 1336–38 replacing a corner shrine and the western hall; the main shrine surviving; the tradition dating a razing order to 1325; Hoshang Shah's move to Mandu, 1405; Sher Khan's agent's mosque at Moti Darwaza, 1488; the Shahi Masjid, 1632; the governor's mansion; Khande Rao Appaji's brass cover (V.S. 1841; the 1775 conversion is an open issue); Scindia maintenance ("Garde Sahib", in Tiwari's account); custody today; Udayeśvara as the fullest Bhūmija statement (Adhikari).
- **1.4:** the praśasti, its two slabs, the Gwalior museum, Garde's 1925–26 find, the agnikula origin, unconfirmed names and building claims; the 1080 record read three ways; the "1059—1080" caption; pilgrims' inscriptions in Sanskrit, Persian and Hindi; Turasadasa, V.S. 1696; Beglar, Cunningham and Bühler as first readers; the restoration-reset slab; the survival legends (Tughluq gunpowder, Aurangzeb, temples built in a night, treasure, the flour-grinder woman).
- **1.5:** the case for an older place (Bhujariya Talab, the 8th-century two-line inscription, reused columns, the 6th-century layers, the uncemented wall); the case for a new town (an absence, Tiwari's frontier-post idea); the Bhringraj and Gond traditions; what each answer would mean; the Udhapuram, sixteenth-century and 1513 records.

**Chapter 2**
- the Betwa and the Vētravatī; the Kewtan;
- the river's regime; groundwater; lakes and ponds in the hollows;
- monsoon, famine and soils; the kharif and rabi crops;
- the Garhi–Teonda range; trap and sandstone; the temple stone "quarried in the hill close by"; mesa and butte; caves; forest;
- Bhoja's Bhojpur dam (brief, comparative); the treatise's *jāṅgala*;
- Udaypur's made water at landscape level (tanks, *kund*s, stepwells, Bhujariya Talab), with **detail reserved for Ch 7**;
- a town of its own stone; quarries; illegal quarrying (Tiwari).

**Chapter 3**
- prehistory (district only); Daśārṇa, Ākara and Avanti;
- Vidisha and Besnagar; the routes; Sanchi; Heliodorus; early Śaiva images; Udayagiri (Gupta);
- Badoh, Pathari and the Seven Mothers panel; the 6th-century cave on Udaypur's hill, with figures "believed" to be Jain Tīrthaṅkaras (a proposal);
- Bhilsa and the Bhāillasvāmin Sun image; the province name;
- Rāṣṭrakūṭas at Pathari (861); Gyaraspur and Maladevi; Gadarmal; the Chandellas at Bhilsa (954); three rival houses.

Chapter 3 ends: "Who held the hill itself in those years is not known." **Chapter 4 must open by taking up the Paramāras' arrival in this frontier.**

**Open issues (ROADMAP 13–20)**
- Chs 2 and 3 are under length.
- V.S. 1841 ≠ 1775.
- 1059 is a reading; only 1080 is firm.
- GEOHER's geomorphology items read as borrowed text.
- The stream names are unresolved.
- The 608 grant's king is not named in its item.
- Lūṇapasāka 1172/1173.
- The Badoh items are linked only via their context excerpts.
- "Garde Sahib" may be M. B. Garde (a lead only).

**Staged and not yet ingested**
- Public-domain sources: Bühler, EI I; Beglar, ASR VII; Cunningham, ASR X; the Gwalior report of 1925–26.
- Research lead: ASR IX p. 109, a V.S. 1137 inscription of Udayāditya, provenance unstated.

These are **not** in the evidence maps. You may name them only as "to be added after ingest" in verification flags, never as evidence.

## 4. Output template (write exactly this structure, one file per chapter)

File: `drafting/editorial/outline_work/chNN_outline_draft.md`.

```
# Chapter N. <exact title from chapters.md>

## Evidence base at a glance
(sub-topics from the map's Sub-topic index with direct/contextual counts and strength; the 3–6 books that carry the chapter, with tier; what is thin)

## 1. Chapter Function
- Central question:
- Principal argument / intervention:
- What changes over the chapter (intellectually / narratively):
- How it develops Chapters 1–(N−1) (name what it builds on, and what it must NOT repeat):
- What it must establish for Chapter N+1:

## 2. Chapter Arc
(opening → … → close; why this order beats the alternatives; where scale shifts; where chronology runs and where it is suspended)
**Through-line (one sentence):** By the end, the reader knows …
**Opening move:** (the concrete thing the chapter opens on, which carries its question, and how it takes up the previous chapter's last line)

## 3. Sections
### N.1 <working title> *(<scope> · ~<words> w)*
- **Section statement:** By the end, the reader knows …
- **Purpose:**
- **Core claim / narrative movement:**
- **Paragraph plan** (3–5 paragraphs; for each):
  1. **P1 — <name>.** **Point:** <the historical work this paragraph must do>.
     - E: <IDs> · C: <IDs> · X: <IDs> · Note: <IDs, for a discursive note>
- **Evidence to deploy** (the specific evidence, with locators):
  - `[Evidence map: Direct|Contextual | <ID> | <BOOKCODE> | <locator exactly as given>]` — what it supplies (≤ 15 words); tier
- **Evidence sequence:** (order and why)
- **Analytical payoff:**
- **Drafting guidance:** (where to narrate closely, compress, give context, let a quotation carry, keep interpretation after evidence, introduce a person/term once, change scale, resist explaining; which items must never be quoted; which claims must carry graded confidence and how)
- **Classification:** documented / interpretive / organizational choice / gap — mark the section's main claims accordingly
- **Transition:** (the conceptual or narrative movement into the next section; never "the next section discusses")

(repeat for each section)

## 4. Chapter Conclusion
- What has been demonstrated:
- What remains unresolved:
- The tension or question carried forward:
- How the last paragraph leads into the next chapter by content (and what it must not do):

### Evidence Checklist
(principal evidence clusters the chapter must incorporate, with IDs)

### Research / Verification Flags
(unsupported propositions; gaps; facts to verify; contradictions, quoting the map's conflict tables; places where stronger primary evidence would help; claims to phrase cautiously, with suggested graded wording)

### Cross-chapter notes (for the editor)
- Evidence in this map that belongs elsewhere (ID → proposed home chapter, and why)
- Evidence homed elsewhere that this chapter needs (ID → recall / reinterpret / omit)
- Duplication risks with Chapters 1–3 (quote the earlier section number) and with later chapters
- People, terms and places introduced here for the first time (so later chapters assume them)
- Material in the map you deliberately did not use, and why (nothing silently dropped)
```

**Quality bar.**
- Every section names specific item IDs for its establishing evidence.
- Every paragraph has a Point that does historical work, not a topic label.
- Every conflict in the map's Conflicts section that touches the chapter is either handled (where, and how: range, note, or framed around the event) or explicitly deferred to a named chapter.
- No section exists only because a sub-topic exists. Merge or cut thin sub-topics and say so.
- Prefer 4–5 strong sections over 7 thin ones.
- Aim for an outline of **4,000–7,000 words per chapter**.

When done, reply with:
- the file path(s);
- section titles with word targets;
- the 5 most consequential structural decisions you made;
- the top verification flags.
