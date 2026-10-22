# Unified drafting plan: Chapter 4 to the Afterword

*Built 15 October 2026 from the evidence index (`drafting/evidence_index/`, parsed from the two evidence-map files) and the master outline (`Chapter_4_to_Afterword_Master_Drafting_Outline.md`). No API calls. This plan is what each chapter is drafted from. The master outline remains the reference for reasoning, evidence glosses and locators.*

**Authority:**
1. `chapters.md`;
2. the user's rulings (U1–U7, 15 Oct; `drafting/DRAFTING_PROGRESS.md`);
3. this plan;
4. the master outline (Part I rulings, then the chapter entry);
5. the style files.

**Format** (as in the Chapter 1–3 plans):
- each unit gives its historical question, through-line, arc and scope;
- each section gives its statement, purpose, word target and paragraph plan;
- each paragraph gives a **Point** and its evidence as **E** (establishing), **C** (corroborating) or **X** (context), each ID with its tier, e.g. `C04-CII-108 (T1)`;
- `Note:` items feed a `{{note: …}}`.

**Reading the evidence:** full quotations are in `evidence_index/chNN.jsonl`. Print them with `python -I -X utf8 drafting/_tools/quotes.py ID …`. Items from Chapters 1–3 are resolved by the same tool from the evidence log.

**Verification method for every chapter drafted from this plan:** verified in-session, not by an independent model (user ruling, 15 Oct: no API calls).

**QC (scripted, `drafting/_tools/plan_qc.py`; report in `plan_work/QC_REPORT.md`):**
- ID validity;
- one primary home (no item establishing in two units);
- Gazetteer share ≤ 40% per section;
- section targets summing to the unit's planned words;
- hand-offs present and matched.

## Status

| Unit | Planned words | Planned | QC passed | Notes |
|---|---|---|---|---|
| Ch 4 | 4150 | yes | yes |  |
| Ch 5 | 4000 | yes | yes |  |
| Ch 6 | 4050 | yes | yes |  |
| Ch 7 | 4250 | yes | yes |  |
| Ch 8 | 3800 | yes | yes |  |
| Ch 9 | 2800 | yes | yes |  |
| Ch 10 | 4200 | yes | no | Gazetteer share 27/42 in 10.5 Revenue, brass and the railway:  |
| Ch 11 | 4250 | yes | yes |  |
| Ch 12 | 3750 | yes | yes |  |
| Afterword | 2750 | yes | yes |  |

---

# Chapter 4. The Paramāras and the Foundation of Udaypur: Kingship, Patronage and Urban Formation

**Planned words:** 4,150 (4.1: 700 · 4.2: 800 · 4.3: 900 · 4.4: 850 · 4.5: 900). **Evidence:** `evidence_index/ch04.jsonl` (682 items: 221 direct, 461 contextual); the plan also borrows from C01, C06 and C07, as marked.

**Historical question.** How did a frontier ridge on Malwa's eastern edge come to carry a king's name? And what can the record say about whether Udayāditya made Udaypur before he was king, as king, or by putting his name on a place others held?

**Through-line.** At the start the reader knows Udaypur as a king's town, founded, the common account says, in 1059. By the end the reader understands:
- that the Paramāras reached this frontier as Rāṣṭrakūṭa feudatories who made themselves kings, held it as their eastern limit under Bhoja and nearly lost the kingdom after him;
- that the town carries the name of the kinsman who recovered it, a man whose temple at Udaypur bore his name by 1080;
- that "founded in 1059, before he was king" is Ganguly's reading of late records, which the dated record of 1080 cannot confirm.

**Arc.**
1. The frontier and the house that took it (4.1).
2. Bhoja's kingdom at its height, and Udaypur's stone carrying his praise (4.2).
3. The broken succession and the recovery: who Udayāditya was (4.3).
4. The dates tested: 1059 against 1080, and the dated reign (4.4).
5. What Udayapura was in his kingdom, ending on the temple as the one work a contemporary record gives to the reign (4.5, into Ch 5).

Chronology runs through 4.1–4.3 and is suspended in 4.4.

**Scope.**
- *Chronological:* c. 900 (Bappaiparāja) to 1094 (Naravarman's accession: succession facts only; everything after belongs to Ch 10).
- *Geographical:* from Gujarat (Harsola) and Malwa (Dhārā, Ujjain) to the eastern limit at Bhilsa; Udaypur is the focus in 4.2 (its praśasti), 4.4 and 4.5.
- *The dynasty as a polity:* 4.1–4.2 present the Paramāras as a kingdom with a capital, provinces and a frontier, building on 1.2 rather than repeating it.

**Conventions for this chapter.**
- Recall Chapters 1–3 in clauses only, using the "Must NOT repeat" list in the master outline's Ch 4 entry.
- Scholars stay in the notes, except in 4.4 P2 (U6).
- Canon wording: "a kinsman of Bhoja; the exact relationship is disputed"; accession c. 1070; 1080 firm; 1059 a reading.

## 4.1 From feudatories to kings of Malwa *(c. 800–1000; regional, then dynastic · ~700 w)*

**Word target:** 700

- **Section statement:** By the end, the reader knows that the Paramāras entered Malwa as subordinates of the Rāṣṭrakūṭas, made themselves independent under Sīyaka in the 970s, and by the end of the tenth century held a kingdom whose eastern limit was set at Bhilsa. The reader also knows that nothing in the record yet names Udaypur.
- **Purpose:** To answer Chapter 3's open line with the house that eventually took the frontier, briefly and on the strongest evidence, and to show the dynasty's own self-account (genealogy, fire-birth) as a later construction set against earlier grants.
- **Paragraph plan:**
  1. **P1 — The claim on the east.** **Point:** pick up 3.5's last line. Later writers credit Sīyaka II with ousting the Chandellas from Malwa and with a kingdom bounded on the east by Vidisha. Say plainly that this gives a frontier, not a holder of Udaypur's hill.
     - E: C04-GAZ-001 (T7), C04-GANGULY-035 (T5) · C: C04-PARTEMPLES-002 (T5) · X: (3.5 recalled in a clause: the Chandella claim to Bhāsvat, 954) · Note: C04-GAZ-001 (T7) (Gazetteer's statement, tier 7; date "972" is "known date")
  2. **P2 — Feudatories in Gujarat.** **Point:** the earliest records place the family not in Malwa but in Gujarat as Rāṣṭrakūṭa subordinates. The Harsola grants of 949 call Sīyaka "crest-jewel among the feudatories" while giving him a sovereign's title. The editor reconstructs a three-generation move from Gujarat into Malwa, capturing Ujjain probably from a Pratīhāra governor.
     - E: C04-CII-002 (T1), C04-CII-003 (T1), C04-CII-007 (T1) · C: C04-CII-006 (T1), C04-GANGULY-015 (T5), C04-GANGULY-027 (T5) · Note: C04-GANGULY-011 (T5), C04-GANGULY-013 (T5) (Ganguly's Rāṣṭrakūṭa-origin argument); C04-BHOJA-TIMES-001 (T5) (Harsola names Bappairāja first)
  3. **P3 — Independence by war.** **Point:** the title provoked a Rāṣṭrakūṭa expedition, and the Paramāras answered by sacking Mānyakheṭa in 972–73, a date fixed independently by Dhanapāla's colophon. The first charter issued from Malwa itself follows in 975.
     - E: C04-CII-004 (T1), C04-CII-042 (T1), C04-GANGULY-032 (T5) · C: C04-GANGULY-033 (T5), C04-CII-012 (T1), C04-CII-009 (T1) · Note: C04-PARTEMPLES-002 (T5) (Adhikari: Sīyaka "real founder"); C04-GANGULY-035 (T5)
  4. **P4 — Muñja and Sindhurāja, briefly.** **Point:** under Vākpati-Muñja the kingdom pressed in every direction, but its eastern claim (Tripurī) is unproven, and Muñja died a prisoner of Tailapa between 993 and 998. Sindhurāja is known mainly from a poet, and closed his reign before 1011. Two sentences each at most; this is the prelude to Bhoja.
     - E: C04-CII-024 (T1), C04-CII-129 (T1), C04-CII-025 (T1) · C: C04-CII-026 (T1), C04-GANGULY-045 (T5), C04-GANGULY-040 (T5) · Note: C04-CII-129 (T1) (editor: "we have no evidence in support of this assertion")
  5. **P5 — A genealogy written later.** **Point:** one sentence only. The dynasty's own account (fire-born hero, unbroken line from Upendra) is the work of its later records, above all the Udaypur praśasti (1.4). Its first names are not in the early grants, which is why this section has followed the grants.
     - E: C04-CII-020 (T1), C04-CII-021 (T1) · C: C04-CII-023 (T1), C04-GANGULY-019 (T5) · X: 1.4 (agnikula; first four names missing elsewhere) recalled in a clause · Note: C04-CII-020 (T1) (editor: "purely legendary, a later creation")
- **Drafting guidance:**
  - Compress. This is the most "Central India" section of the chapter; Udaypur must be named in P1 and P5 and nowhere invented elsewhere.
  - Introduce Sīyaka (II), Vākpati-Muñja, Sindhurāja, Rāṣṭrakūṭas of Mānyakheṭa, Harsola once each. Sīyaka I is already in the ledger (1.4); call this ruler "Sīyaka II" at first mention.
  - Rāṣṭrakūṭa origin of the family: Ganguly's argument, in a note only.
  - "Ousted the Chandellas" is a tier-7 claim. Frame it as a later attribution (e.g. "Sīyaka II is credited with ousting…"), with the Gazetteer named in the note, never in the sentence (house rule: sources in notes). *[Plan change from the outline: the outline's wording was source-led.]*
  - Do not narrate Muñja's capture as a scene. Do not use the Merutuṅga grass-baby story (GANGULY-038) or PARMAR-RAJPUT's "16 times" (PARMAR-RAJPUT-006). Both are tradition, and neither touches Udaypur.
- **Transition:** Within a generation the eastern limit set under Sīyaka belonged to a king whose reputation would outrun his kingdom. The first royal grant in the Bhopal country shows Bhoja holding it by 1018, which is where 4.2 begins.

---

## 4.2 Bhoja's kingdom and Bhoja's name *(c. 1000–1055; dynastic, with the eastern frontier in view · ~800 w)*

**Word target:** 800

- **Section statement:** By the end, the reader knows Bhoja's dated reign (1011–1047 in his own records, dead before 1055). They know that his kingdom reached the Bhopal country by 1018 and had Bhilsa as its eastern limit c. 1030. They know he rebuilt Dhārā and patronised building and learning on a scale his successors measured themselves against, though defeats marked his later years. They also know that much of his praise reaches us through the praśasti found at Udaypur, which is panegyric, and that the books credited to him, including the architectural treatise, are attributed and partly doubted.
- **Purpose:** To give Bhoja his due in a book about Udaypur without making him its founder. He matters here for three things: the frontier he held, the model of royal building he set, and the way the town's memory and popular writing attach him to Udaypur.
- **Paragraph plan:**
  1. **P1 — The reign in its own records.** **Point:** Bhoja's grants run from 1011 to 1047; he died some time before 1055, when his successor's first grant appears. One sentence on the longer traditional reign (55 years, 7 months, 3 days) as tradition, with the range in a note.
     - E: C04-CII-072 (T1), C04-CII-071 (T1), C04-GANGULY-070 (T5) · C: C04-CII-075 (T1) · Note: C04-BHOJDEV-HI-006 (T9), C04-RAJABHOJ-EN-007 (T9) (traditional reign length; tier 9), C04-BHOJA-TIMES-015 (T5), C04-BHOJA-TIMES-016 (T5) (accession c. 1000 or c. 1010)
  2. **P2 — The eastern edge under Bhoja.** **Point:** this is the only paragraph of Bhoja's politics the town strictly needs. The first Paramāra grant issued in the Bhopal territory (1018) puts that region inside his kingdom. Al-Bīrūnī, as Ganguly reads him, gives Bhilsa as the eastern limit in 1030. Udaypur lay at or just beyond that edge; write "on the eastern edge", never "inside", on this evidence.
     - E: C04-CII-049 (T1), C04-GANGULY-051 (T5) · C: C04-GANGULY-022 (T5) · Note: C04-GANGULY-051 (T5) (Al-Bīrūnī via Ganguly)
  3. **P3 — The builder and his reverses.** **Point:** Bhoja rebuilt Dhārā and moved the royal residence there. He had the Vāgdevī image made in 1034. He began, and did not finish, a colossal temple at Bhojpur tied to a dam (Chapter 2's comparison recalled in a clause only). His later reign also saw defeats: Candella and Kacchapaghāta reverses in the north, and Someśvara I sacking Dhārā. This prepares the crisis without narrating it again.
     - E: C04-GANGULY-052 (T5), C04-CII-063 (T1), C04-HARDY-001 (T5) · C: C04-GANGULY-055 (T5), C04-GANGULY-056 (T5), C04-GANGULY-068 (T5), C04-GANGULY-069 (T5) · X: Ch 2 §2.4 (Bhojpur dam), recall only
  4. **P4 — The praise from Udaypur.** **Point:** the fullest eulogy of Bhoja, his victories over Chedi, Gurjara, Lāṭa, Karṇāṭa and Turuṣka, and his temples "all around" to Kedāra, Rāmeśvara and Somanātha, is in the praśasti found at Udaypur. Its editor calls the geographical boast worthless for history, and agrees with Bühler that the temple claim cannot be corroborated. The town's own stone is thus a main witness to Bhoja's reputation, and a partisan one.
     - E: C04-CII-069 (T1), C04-CII-070 (T1) · C: C04-JAGTA-EN-019 (T8), C04-JAGTA-EN-020 (T8), C04-JAGTA-EN-021 (T8), C04-BHOJDEV-HI-008 (T9) · X: 1.4 (praśasti as object; Ray's doubt), recall in a clause · Note: C04-CII-070 (T1) (Bühler/editor)
  5. **P5 — King, patron, attributed author; and a remembered presence.** **Point:**
     - Works were composed "by Bhoja himself and his protégés" (editor). The *Tattvaprakāśa* on Śaiva Siddhānta is ascribed to him. Doubts about the whole list of works go in a note.
     - The *Samarāṅgaṇasūtradhāra* is named once, as a treatise on building attributed to him, normative, and its attribution doubted.
     - Close on memory: Tiwari supposes Bhoja "must have been well aware" of Udaypur's development, and popular writers credit him with re-founding Vidisha. These show how strongly the region attaches its past to Bhoja; they are not evidence that he acted at Udaypur.
     - E: C04-CII-069 (T1), C04-PANDE-003 (T5) · C: C04-GANGULY-104 (T5) (the praśasti credits Bhoja with many temples; few traces survive), C04-JAGTA-EN-024 (T8), C04-RAJABHOJ-EN-012 (T9), C04-BHOJDEV-HI-003 (T9) · X: C06-BHOJA-TIMES-046 (T5), C06-SAMAR-1-002 (T4) (doubts; homed Ch 6) · Note: C04-SAMAR-1-001 (T4) (⚠ old OCR; paraphrase only: 84 works per a later commentator), C04-JAGTA-EN-059 (T8) (Tiwari treats the treatise as testimony to Bhoja's patronage; quote not used)
- **Drafting guidance:**
  - Do not list Bhoja's conquests beyond the praśasti's one verse.
  - Do not use the following, all tier 9 and irrelevant to Udaypur: the "nine gems"; the 104 buildings and the 84 crossroads (BHOJDEV-HI-020, -022, -023; RAJABHOJ-EN-036); the Mongolian text; the iron-pillar story (RAJABHOJ-EN-019).
  - Never quote any SAMAR item. Paraphrase only, cautiously, and say "attributed to Bhoja".
  - Graded wording for authorship: "credited with", "ascribed to", "a work bearing his name".
  - Write "Tiwari" (named in full in 1.1). Do not give JAGTA-EN-024's "must have prepared himself under his protection" as fact.
  - One sentence at most on the Bhojpur dam (Chapter 2 has it).
- **Transition:** The same praśasti that crowns Bhoja passes from his death straight to his successor rising "like the sun" over a darkened earth [C04-CII-081]. The panegyrist left out the decade and a half between the two.

---

## 4.3 The broken succession and the recovery *(c. 1055–c. 1075; dynastic, read against rival records · ~900 w)*

**Word target:** 900

- **Section statement:** By the end, the reader knows four things.
  - The dynasty's own praśastis leave Jayasiṃha out. He is known from his own grant of 1055 and from others' records, so the line from Bhoja to Udayāditya was not a smooth succession.
  - One record of V.S. 1116 suggests a struggle for the throne in which Udayāditya may have been Jayasiṃha's adversary; this is the editor's presumption.
  - The second invasion was a coalition of three enemies, whose identities the CII editor and Ganguly reconstruct differently. Ganguly's Cāhamāna cavalry is his reading, not a recorded fact.
  - Udayāditya's relation to Bhoja remains "kinsman, exact relationship disputed". The "junior branch" view rests on a sixteenth-century pedigree that the editor rejects.
- **Purpose:** To tell the recovery that Chapter 1 promised ("Chapter 4 tells the full story") by deepening, not repeating, 1.2: what each source says, where they part, and what the reader can trust.
- **Paragraph plan:**
  1. **P1 — The missing king.** **Point:** recall in one clause that Jayasiṃha was restored with Chālukya help (1.2). Then the new fact: the Udaypur and Nagpur praśastis, which list almost every king, omit him. He is known from his own Māndhātā grant of 1055 and the editor places him "between 1047 and 1080". The panegyric's silence is a choice, and the reader should see it as one.
     - E: C04-CII-076 (T1), C04-CII-092 (T1), C04-CII-075 (T1) · C: C04-JAGTA-EN-050 (T8) · X: 1.2 (restoration), clause only · Note: C04-CII-092 (T1) (Kielhorn: omitted because the reign was short)
  2. **P2 — A rival for the throne?** **Point:** the Pānāhedā inscription of V.S. 1116 shows a Vāgaḍa branch devoted to Jayasiṃha. The editor presumes the branch's next ruler helped him against "his adversary Udayāditya or some other person … then struggling … for the throne". The Nagpur verse's hint of turmoil "in the family" (1.2, clause) points the same way. Present this as a possibility the editor raises. It bears on 4.4: the record dates Jayasiṃha's rule to the very year read as Udayapura's beginning.
     - E: C04-CII-106 (T1) · C: C04-CII-093 (T1) · X: 1.2 (internal disturbance), clause only · Note: C04-CII-106 (T1) (editor's presumption, worded "presuming … may have")
  3. **P3 — Three enemies, two reconstructions.** **Point:**
     - Udayāditya's own son's record says Mālava sank under the attack of three enemies. The CII editor names them as the Kalachuri Karṇa, the Chālukya Someśvara II (through his general the Gaṅga Udayāditya) and the Hoysala Ereyaṅga. The editor holds Jayasiṃha "possibly also killed".
     - Ganguly instead has Caulukyas and Karṇāṭas occupying Dhārā and Udayāditya, "a scion of a junior branch", calling in cavalry from the Cāhamāna Durlabha III of Śākambharī.
     - Bhatia, cited by Pande, puts Karṇa's invasion in 1079, defeated by Udayāditya "and his allies".
     - The text keeps the event (a coalition repulsed). The identities and the Cāhamāna help go to a note, with CII's reading given first.
     - E: C04-CII-083 (T1), C04-CII-114 (T1), C04-CII-095 (T1), C04-CII-096 (T1), C04-CII-082 (T1) · C: C04-GANGULY-074 (T5), C04-GANGULY-076 (T5), C04-GANGULY-078 (T5), C04-PANDE-006 (T5) · Note: C04-GANGULY-076 (T5), C04-GANGULY-078 (T5) (Durlabha III: Ganguly's account); C04-PANDE-006 (T5) (Bhatia's 1079); C04-CII-107 (T1) (two invasions of Karṇa, fifteen years apart); **C04-CII-082 (T1) vs C04-CII-114 (T1)/C04-CII-096 (T1): the CII editor's own lists differ.** At p. 135 the three are the Kalachuri Karṇa, the Chaulukya Bhīma and the Hoysala Ereyaṅga; at pp. 152 and 178 they are Karṇa, the Chālukya Someśvara II (through the Gaṅga Udayāditya) and Ereyaṅga, with Bhīma placed in the first invasion. The text follows the fuller discussion (pp. 152, 178); the note records the variance. *[Added in the evidence pass.]*
  4. **P4 — Udaypur's stone on the victory.** **Point:** the second slab of the Udaypur praśasti, legible only at its opening, praises Udayāditya's rout of the lord of Chedi, which the editor reads as the Kalachuri Karṇa. Its last full verse says that for one who had lifted the earth, restoring the "Primeval Boar" was easy. The editor takes this as a hint that Udayāditya restored a temple of the Boar, recorded in the lost part. This is new to the reader; 1.2 gave only the Nagpur boar simile, which must not be quoted again. Close the narrative with the recovered realm as 1.2 left it (Jhalrapatan, Bhilsa, Nimar), in one clause. The CII statement (Jhālrapāṭan and Kōṭā north, part of Vidishā north-east) is the authority, and Ganguly's wider limits are recalled only.
     - E: C04-CII-112 (T1), C04-CII-130 (T1), C04-CII-111 (T1) · C: C04-JAGTA-EN-048 (T8), C04-JAGTA-EN-052 (T8) · X: 1.2 (boar simile; realm), recall only; C04-GANGULY-095 (T5) · Note: C04-CII-130 (T1) (Bühler's doubt answered by the editor from the second slab; the Boar-temple hint is the editor's)
  5. **P5 — Who he was.** **Point:**
     - Restate the canon in one sentence: a kinsman of Bhoja; the exact relationship is disputed (1.2 holds the note of readings; do not repeat it).
     - Deepen with what 1.2 does not give. The "junior branch" view that Ganguly built, and that Tiwari's source Verma follows, comes from a pedigree (Śūravīra → Gondala → Gyātā → Udayāditya) in an inscription at Udaypur dated V.S. 1562. Ganguly drew from it a line of feudatories ruling at Udayapura; the editor rejects the pedigree against the Dōngargāon and Jainad records.
     - Verma also argues that the *pādānudhyāta* formula ("meditating at the feet of") is praise, not proof of direct succession.
     - Tiwari asks why a brother would wait from 1055 to 1070 for the throne, and notes that no record of Bhoja's time names him. These are good questions and remain questions.
     - E: C04-GANGULY-079 (T5), C04-GANGULY-081 (T5), C04-CII-131 (T1), C04-CII-132 (T1) · C: C04-JAGTA-EN-026 (T8), C04-JAGTA-EN-028 (T8), C04-JAGTA-EN-027 (T8), C04-JAGTA-EN-029 (T8), C04-JAGTA-EN-037 (T8), C04-JAGTA-HI-032 (T8), C04-JAGTA-EN-038 (T8) · C: C04-BHOJA-TIMES-038 (T5) (the Nagpur inscription's "Udayāditya, a kinsman of Bhoja": the source of the canon phrase) · X: C01-CII-014 (T1) (16th-c. genealogy as given in 1.2's note) · Note: C04-CII-086 (T1), C04-CII-080 (T1), C04-CII-082 (T1) (Jagaddeva's record makes Bhoja his paternal uncle; CII, citing Dōngargāon, calls Udayāditya Bhoja's brother; recalled only as 1.2's note has them, with no new verdict); C04-CII-084 (T1) (Kielhorn: *bandhu* = relative in general); C04-JAGTA-EN-038 (T8) (Kielhorn and Ganguly vs H. C. Ray, as Tiwari reports)
- **Drafting guidance:**
  - Never write "nephew" (BHOJA-TIMES-029 is the only source of it; see flags).
  - Never state "brother" as fact. Cite the Dōngargāon/Jainad readings only via 1.2's note.
  - Do not quote the Nagpur boar passage again.
  - Name Durlabha III only in the note, attributed to Ganguly ("Ganguly has Udayāditya appeal to…").
  - "Karṇa" is ambiguous (Kalachuri Karṇa vs Caulukya Karṇa of Gujarat). CII identifies the Chedi enemy as Kalachuri; Ganguly's "Gurjara Karṇa" (GANGULY-078) is the Caulukya. Say which in each sentence, and flag the ambiguity in a note.
  - Introduce once: Pānāhedā, Vāgaḍa, Someśvara II, the Gaṅga Udayāditya (spell out that this is a Chālukya general of the same name, not our king), Ereyaṅga, Dōngargāon, Jainad, Verma (Santosh Kumar Verma, as Tiwari's source, first named in this chapter if not earlier; check the ledger).
  - Graded confidence goes on the clause ("may have", "is presumed", "has been reconstructed"). The names (the CII editor, Ganguly, Verma) go in the notes. *[Plan change: the outline put the scholars in the sentence; house rule P6.]*
- **Transition:** Ganguly's junior branch did more than make Udayāditya a cousin. It gave him a territory before he had a throne, and Udayapura as its seat, and with it a date, V.S. 1116, eleven years before his accession. 4.4 tests that date.

---

## 4.4 Before the throne? The dates and what rests on them *(1059 / c. 1070 / 1080–1093; evidential, chronology suspended · ~850 w)*

**Word target:** 850

- **Section statement:** By the end, the reader knows four things.
  - "Founding before kingship" depends on the year V.S. 1116 (1059). That year reaches the literature through late or error-ridden records at Udaypur, and through survey readings of temple inscriptions not yet edited in the corpus.
  - Ganguly's reconciliation (a territorial lord building in 1059 from Udayapura) rests on the same rejected pedigree as the junior branch.
  - In the CII record, the earliest known date for Udayāditya is the Udaypur temple record of 1080.
  - His reign is dated in his own and his sons' records from 1080 to the latter part of 1093. The accession c. 1070 is the working position, and the 1059 founding remains possible but unproven.
- **Purpose:** To argue, as the brief requires, the question 1.2 and 1.4 raised ("lord's seat or new king's undertaking"; "claims more than the stones settle") instead of assuming it. This is the section where the old canon's "founded … 1059 … eleven years before he became king" is formally retired.
- **Paragraph plan:**
  1. **P1 — The case for 1059, at its strongest.** **Point:** several modern works say construction began in V.S. 1116 and the flag-staff went up in V.S. 1137: Patil, the Gazetteer, Hardy ("founded … 1059 and consecrated in 1080"), Kramrisch's caption, the INTACH and GEOHER surveys. Ganguly found the year in a record stating that Udayāditya was "ruling in Sam 1116". Because the Caulukya Karṇa had not yet come to power, Ganguly concluded that Udayāditya built the temple "when he was ruling his paternal territory apparently from Udayapur". Tiwari pictures a prince sent to the frontier, planning the town before he was king. Give this fairly, in one paragraph.
     - E: C04-GANGULY-092 (T5), C04-GANGULY-094 (T5) · C: C04-GAZ-005 (T7), C04-GAZ-006 (T7), C04-MADHYABHARAT-009 (T5), C04-HARDY-003 (T5), C04-KRAM-2-001 (T5), C04-GEOHER-003 (T7), C04-JAGTA-EN-044 (T8) · X: 1.2 (Ganguly's resolution, already in a note); 1.4 ("1059—1080" caption), recall only · Note: C04-JAGTA-EN-042 (T8), C04-JAGTA-HI-040 (T8) (Tiwari's prince-on-the-frontier picture; testimony)
  2. **P2 — Where the year comes from.** **Point:** trace the supports. **U6 (user ruling, 15 Oct): the text itself, not only a note, must say whose reading 1059 is and why it is less secure than 1080.** Write that the year comes from Ganguly's reading of late records: a fragmentary record he dates 1513, which he himself calls "very perfunctorily executed" and full of "gross mistakes", and a pedigree record that the CII editor dates V.S. 1562 (1505/06) and whose genealogy he rejects. Modern surveys and handbooks then repeated the year. 1080, by contrast, stands in a record on the temple itself, dated V.S. 1137 and naming the temple after its constructor. This is the one place in the chapter where scholars are named in the running text, because here the disagreement *is* the answer (P6).
     - (a) Ganguly himself calls the record giving 1116 for the temple "very perfunctorily executed" and full of "gross mistakes". 1.5 dates it 1513; recall in a clause.
     - (b) The "ruling in Sam 1116" statement comes in the pedigree record that makes Udayāditya son of Gyātā (4.3). The CII editor dates that record V.S. 1562 and rejects its genealogy.
     - (c) The modern surveys and handbooks repeat the year. They do not add independent witnesses, and the in-situ inscriptions they cite await an edition (Chapter 6).
     - Conclude, graded: the 1059 beginning is a reading carried by late testimony, not a contemporary date.
     - E: C04-GANGULY-093 (T5), C04-GANGULY-094 (T5), C04-CII-131 (T1), C04-CII-132 (T1) · C: C04-GAZ-006 (T7), C04-INTACH-003 (T7) · X: C01-GANGULY-020 (T5) (1513 record, 1.5); C06-JAGTA-EN-011 (T8), C06-INTACH-001 (T7) (the V.S. 1116 temple inscription(s) as read by Verma and INTACH; homed Ch 6) · Note: whether Ganguly's "perfunctory" record, the V.S. 1562 pedigree record, and the 22-line V.S. 1116 inscription Verma reads are one record or several is not settled by any item. **Do not merge them** (see flags).
  3. **P3 — The other side of the scale.** **Point:**
     - The CII editor states that the Udaypur record of 1080 "supplies the earliest known date for the king Udayāditya".
     - The Pānāhedā inscription of V.S. 1116 shows the Vāgaḍa branch devoted to Jayasiṃha in that same year (4.3 P2).
     - Ganguly's own Karṇa argument shows Udayāditya could not then have been sovereign.
     - None of this disproves a lord building on his own ground before his accession. It shows that the only contemporary dated evidence places Udayāditya at Udaypur in 1080, as king, with the temple bearing his name.
     - Leave the question open, in the house's graded voice: "possible, on a late record; not shown".
     - E: C04-CII-108 (T1), C04-CII-106 (T1), C04-CII-119 (T1) · C: C04-CII-076 (T1), C04-GANGULY-092 (T5), C04-PARTEMPLES-007 (T5) (the in-situ record of the flag-hoisting in 1080) · X: 1.4 (three readings of the 1080 record), recall in a clause · Note: C04-JAGTA-EN-061 (T8) (Tiwari's "30 March 1080" flag-hoisting equivalence; Verma's calculation, see Ch 6)
  4. **P4 — The dated reign.** **Point:** with the 1059 question set aside, the records give a reign that can be followed year by year:
     - 1080, the Udaypur temple record;
     - 1081, an image consecrated at Dhārā in the reign;
     - 1082, Naravarman's gift for a lamp for his dead brother Lakṣmadeva, while Udayāditya was camped near Ujjain;
     - 1086/87, a *paṭṭakila* of an oilman's lineage building a Śambhu temple at Jhālrapāṭan "when Udayāditya was prosperous in the region";
     - a royal endowment to Somanātha on the fort of Kōśavardhana;
     - a Chālukya campaign "of terror to the king of Dhārā" in 1077 (Ganguly).
     - He died in the latter part of 1093; Naravarman made the first annual funeral gift in V.S. 1152.
     - The working accession c. 1070 rests on Pande and Adhikari, and on the 1.2 note's other datings (one clause; do not repeat the list).
     - E: C04-CII-108 (T1), C04-CII-109 (T1), C04-CII-078 (T1), C04-CII-120 (T1), C04-CII-121 (T1), C04-CII-089 (T1), C04-CII-091 (T1) · C: C04-GANGULY-096 (T5), C04-GANGULY-112 (T5), C04-CII-110 (T1), C04-CII-087 (T1), C04-PANDE-005 (T5), C04-PARTEMPLES-005 (T5) · Note: C04-MADHYABHARAT-005 (T5) (Patil's 1058–87, already in the ledger from 1.2; recall, not a new date); C04-GANGULY-098 (T5) ("closed his reign shortly after 1086", superseded by CII-089/091); C04-JAGTA-EN-051 (T8) (1070–1093)
- **Drafting guidance:**
  - This is the one place where the chapter stops narrating. Keep the tone even, not triumphant.
  - Do not call 1059 "wrong". Call it "a reading", "a late record's date", "not shown".
  - Do not repeat 1.4's three readings of 1080; refer to them in a clause.
  - Every modern work that repeats 1059 goes into one note, not the text.
  - "Jhālrapāṭan", "Kōśavardhana" and "Dhavalī" are introduced once. Lakṣmadeva is introduced here as Udayāditya's son who died before him; his Nagpur campaigns belong to Chapter 10.
  - Graded wording: "in the CII record, the earliest known date…"; "Ganguly inferred…"; "a late record states…".
- **Transition:** If the dates make Udayāditya king of Malwa first and patron of Udaypur in the record second, the next question is what Udaypur was to that king. Was it a capital in miniature, a provincial seat, or a place he gave to others to hold?

---

## 4.5 A town with a king's name *(Udayāditya's reign and after; scale shifts to Udaypur · ~900 w)*

**Word target:** 900

- **Section statement:** By the end, the reader knows four things.
  - The contemporary record ties Udayāditya to Udaypur through a temple named after its constructor. The eponymous town–temple–tank triad reaches us through an inscription reported by Patil and Ganguly.
  - The CII editor reads Udayapura as the capital town of a subordinate Nēmaka house under Udayāditya, with a temple built by or under one of its princes. This leaves open whether the king or his subordinate built.
  - The administrative geography often attached to Udayapura (a *maṇḍala*, a sixty-four-village *pāṭhaka*, Rājyapāla's eastern headquarters) comes from a record of the 1170s, not from his reign.
  - Nothing in this chapter's evidence dates the walls, streets or palace. Udaypur's "urban formation" in his reign is a naming, an endowment and a seat of local rule, while the physical town is Chapter 7's to date.
- **Purpose:** To bring the chapter home to Udaypur and to answer honestly the "urban formation" in the chapter title: say what is known, mark what is inferred, and refuse what is invented.
- **Paragraph plan:**
  1. **P1 — What the name proves.** **Point:**
     - Recall the triple naming in one clause (1.2).
     - The text of the 1080 record calls the temple Udayeśvaradeva, which its editor reads as "after the name of its constructor".
     - The triad is reported by Patil and Ganguly from an inscription on the temple. Ganguly suggested Udayeśvara "is perhaps the same as" Nīlakaṇṭheśvara, and could not trace the Udayasamudra.
     - Ganguly also cites "a contemporary inscription" for the city's building by Udayāditya, against the snake legend (1.1).
     - The point: an eponymous name is good evidence of a royal claim on a place. It is not, by itself, evidence of a new foundation (1.5's two answers stand).
     - E: C04-CII-119 (T1), C04-MADHYABHARAT-006 (T5), C04-GANGULY-106 (T5), C04-GANGULY-101 (T5) · C: C04-PARTEMPLES-006 (T5), C04-PARTEMPLES-009 (T5) (Adhikari: the temple as the reign's signal work, completed 1080), C04-GANGULY-105 (T5), C04-PANDE-007 (T5), C04-INTACH-002 (T7), C04-JAGTA-EN-049 (T8) · X: 1.2 (triad), 1.5 (founded or taken over), clauses only; C07-GANGULY-005 (T5) (Udayasamudra unidentified; homed Ch 7) · Note: C04-JAGTA-EN-049 (T8) (Tiwari's argument from name + absence, already weighed in 1.5)
  2. **P2 — A seat for a subordinate house.** **Point:**
     - Deepen 1.2's Nemak sentence with the editor's fuller reading. Line 6 names Udayapura as the capital town of the Nēmaka dynasty, "subordinate to Udayāditya". The record's object "appears to be" that Udaipur was placed in charge of a Nēmaka king, under whom a temple was built.
     - That king's father Śūdraka is said to have beaten a king of Gujarāt, possibly the Caulukya Karṇa (1064–94) or Bhīma. This puts the house in Udayāditya's time or just after.
     - Tiwari's puzzlement ("since Udaypur was under direct Paramāra rule…") and his surmise that the house supervised the temple's building go in a note.
     - Leave the temple-builder question open; which temple is meant is uncertain (1.2's note).
     - E: C04-CII-113 (T1), C04-CII-122 (T1) · C: C04-JAGTA-HI-059 (T8), C04-JAGTA-EN-062 (T8) · X: 1.2 (Nemak reading), recall · Note: C04-CII-122 (T1) (editor's identification of the Gujarāt king, "possibly"); C04-JAGTA-EN-062 (T8), C04-JAGTA-HI-060 (T8) (Tiwari's surmise)
  3. **P3 — The province, and a correction of dates.** **Point:**
     - 1.2 placed Udayapura in the Bhāillasvāmi-mahādvādaśaka and gave Rājyapāla's eastern headquarters there, "for a time". The map shows both come from the Lūṇapasāka record of the 1170s.
     - The same record names the Bhṛṅgārikā *pāṭhaka* of sixty-four villages under a *daṇḍanāyaka* "probably" at Udayapura (Gazetteer).
     - That record is eighty years after Udayāditya. It shows what Udayapura later became in the province; it must not be read back into his reign.
     - Of his own time, the records say only that his son Lakṣmadeva governed "some of the eastern part" of the dominions. No item names Udaypur as Lakṣmadeva's seat, so say so.
     - E: C04-GAZ-007 (T7), C04-CII-077 (T1) · C: C04-BHOJDEV-HI-011 (T9) · X: C01-GANGULY-010 (T5), C01-GANGULY-015 (T5) (Lūṇapasāka record and Rājyapāla, as used in 1.2; homed Ch 1/Ch 10) · Note: Lūṇapasāka's date is "early in the 1170s" here (the conflict's home is 6.4; Part I, I.3). Rājyapāla and Lūṇapasāka governed for the Caulukyas (U1): this province evidence belongs to the 1160s–70s and must be dated in a clause if used for Udayāditya's time; C01-GAZ-010 (T7) (Gazetteer misattributes the 1173 record to Udayāditya)
  4. **P4 — The town as later writers imagine it.** **Point:**
     - Ganguly lists Udayapura among the towns that rose under the Paramāras, and Mahesh Singh among those that "developed" under them.
     - Royal temples were a form of royal giving, bringing merit to the giver and prosperity to the community (Hardy). That is the frame in which a king's temple becomes a town's centre.
     - Tiwari goes further. He sees a square walled town with a palace, laid out on Bhoja's lines, a Paramāra *sabhā-maṇḍapa* at its centre, a "mini capital" where a future king lived in his youth. He also says, in another place, that palace, stepwells, gates and courthouse "were built over centuries".
     - The treatise attributed to Bhoja prescribes where each class of townsman should live and which rites precede a town's founding. No item says Udaypur was laid out to it.
     - Conclude, graded: the evidence supports a royal temple and a royal name, and later a seat of local rule. The town's plan and walls are not dated in this chapter's sources and are taken up in Chapter 7.
     - E: C04-GANGULY-108 (T5), C04-BHOJA-TIMES-044 (T5), C04-HARDY-002 (T5) · C: C04-JAGTA-EN-056 (T8), C04-JAGTA-EN-045 (T8), C04-JAGTA-EN-058 (T8), C04-JAGTA-HI-039 (T8), C04-BHOJDEV-HI-029 (T9), C04-RAJABHOJ-EN-027 (T9) · X: C07-GEOHER-052 (T7), C07-GEOHER-003 (T7) (palace and wall attributions, homed Ch 7) · Note: C04-SAMAR-1-006 (T4), C04-SAMAR-1-009 (T4) (⚠ old OCR; normative; attribution doubted; paraphrase only)
  5. **P5 — The king's death, and what Udaypur keeps.** **Point:**
     - Udayāditya died in the latter part of 1093.
     - His eldest son Lakṣmadeva had died before him. Naravarman succeeded in V.S. 1151. A third son, Jagaddeva, is praised for declining to outshine his brother. Their reigns and the long decline belong to Chapter 10 (one clause).
     - End on content, at Udaypur. Of all that was said of him (recovery, boar, kinship, founding), the stones of the town keep one contemporary statement in his own reign: a temple bearing his name, with a record of V.S. 1137 on it. That building is what remains to be read.
     - E: C04-CII-089 (T1), C04-CII-077 (T1), C04-CII-087 (T1), C04-CII-085 (T1) · C: C04-CII-079 (T1), C04-GANGULY-085 (T5) · X: Ch 10 (Lakṣmadeva's campaigns, Naravarman, decline) · Note: C04-GANGULY-088 (T5) (Ganguly's conjecture that Jagaddeva and Lakṣmadeva were one person, not adopted)
- **Drafting guidance:**
  - Never write that Udayāditya "laid out" streets, built the palace or the walls. Never call Udaypur a "mini capital" except as Tiwari's phrase, attributed.
  - Do not identify the Udayasamudra with the Udaysagar (brief §2; Chapter 7).
  - Do not identify the Nēmaka temple with the Udayeśvara.
  - Do not quote SAMAR. Name the treatise once as "attributed to Bhoja", and state that its prescriptions are norms, not a record.
  - Do not use Tiwari's distances ("500 km from Dhar"; "500 metres"), his imagined consecration festival (JAGTA-HI-052) or the dancer's waiting (JAGTA-EN-061; 1.1 has the dancer).
  - Do not use the Bhopal *sabhā-maṇḍapa* claim (JAGTA-EN-041, -045) as fact; it is unsupported and about Bhopal.
  - The final paragraph must not summarise the chapter or announce Chapter 5. It ends on the building, by content.
- **Transition:** (Into Chapter 5, by content.) The chapter closes on the temple as the one work at Udaypur that a contemporary record gives to Udayāditya's reign. Chapter 5 opens on that building.

## Chapter 4: conflicts to present, unresolved

| Conflict | Where | How the text holds it |
|---|---|---|
| Udayāditya's relation to Bhoja: kinsman (Nagpur, C04-BHOJA-TIMES-038), brother (Dōngargāon/Jainad per CII, C04-CII-082, -083), Bhoja as paternal uncle of Jagaddeva (C04-CII-086); the "junior branch" pedigree (C04-GANGULY-079/-081 against C04-CII-131/-132) | 4.3 P5 | Canon phrase in the text; the readings stay in 1.2's note; new here: the pedigree's provenance and why CII rejects it |
| The three enemies: CII p. 135 (Karṇa, Bhīma, Ereyaṅga) vs CII pp. 152, 178 (Karṇa, Someśvara II via the Gaṅga Udayāditya, Ereyaṅga); Ganguly's Caulukyas, Karṇāṭas and Cāhamāna cavalry | 4.3 P3 | Text: a coalition of three, repulsed; identities in a note, the fuller CII reading first, the variance stated |
| "Karṇa": Kalachuri (CII) vs Caulukya (Ganguly, C04-GANGULY-078) | 4.3 | Name the dynasty every time |
| 1059 (V.S. 1116) vs 1080 (V.S. 1137) | 4.4 P1–P3 | **U6:** whose reading (Ganguly's, from late records) and why it is weaker, in the text |
| Reign dates: 1058–87 (Patil, in the ledger), 1059–86, 1060–87, c. 1070–c. 1093 | 4.4 P4 | Dated range 1080–1093 from the records; accession c. 1070 working; the others in one note |
| Temple builder: the king (the name, C04-CII-119) or a Nēmaka prince "or during his reign" (C04-CII-122) | 4.5 P2 | Open; "the temple that bears Udayāditya's name" |
| Founded or renamed (1.5's question) | 4.5 P1 | Name ≠ foundation; sharpened, not closed |
| Ganguly's "contemporary inscription" that the city was built by Udayāditya (C04-GANGULY-101) | 4.5 P1 | "Ganguly cites a contemporary inscription" goes in a note; the item does not say which record |

## Chapter 4: hand-offs

- **In (from 3.5, delivered):** "Who held the hill itself in those years is not known." Ch 4 opens on Sīyaka II's eastern limit at Vidisha (C04-GAZ-001, C04-GANGULY-035) and keeps the same gap: an eastern edge, not a holder of the hill.
- **Out (to Ch 5):** the last paragraph ends on the Udayeśvara as the single work at Udaypur that a contemporary record assigns to the reign. Ch 5 opens on the building facing east but entered from the west (C05-PANDE-002, -011). The ending must not describe the architecture, quote the 1080 record, or detail the tanks and walls.

## Chapter 4: changes from the master outline (none structural)

1. **4.1 guidance:** "The district Gazetteer credits…" (source-led) is replaced by framing as an attribution, with the source in a note.
2. **4.3 P3:** added C04-CII-082 and the note on the CII editor's two differing lists of the three enemies. The map shows the variance; the outline had not.
3. **4.3 P5:** added C04-BHOJA-TIMES-038 (the Nagpur "kinsman" wording, the source of the canon phrase) and the C04-CII-086/-080/-082 note items.
4. **4.3 guidance:** scholars' names moved from sentences to notes (P6).
5. **4.4 P2:** the U6 instruction (whose reading 1059 is, and why it is weaker, in the text).
6. **4.4 P3 and P4; 4.2; 4.5 P1:** added corroborating items from the evidence pass: C04-PARTEMPLES-007, C04-MADHYABHARAT-005 (note), C04-GANGULY-104, C04-PARTEMPLES-006 and -009.
7. **4.5 P3 note:** updated for U1 (Caulukya governors) and the conflict homes (Lūṇapasāka → 6.4).

## Chapter 4: research and verification flags

**Page-image checks (before drafting the paragraph):**
- C04-CII-082 (p. 135) against pp. 152 and 178 (the three enemies).
- C04-GANGULY-093 / C01-GANGULY-020 (the "1513" record, *JAOS* VII p. 35) and C04-CII-131 (V.S. 1562): possibly two records.
- C04-GANGULY-101: which "contemporary inscription".
- C04-ARTPAR-004: garbled OCR crediting Bhoja; not used.
- C04-MADHYABHARAT-006 / C04-GANGULY-106: the triad inscription, which is not among the CII items.

**Staged public-domain sources (leads only, `ocr_verify`; not evidence until hand-corrected and ingested):**
- Bühler, *EI* I: the praśasti text and the triad inscription;
- Beglar, ASR VII; Cunningham, ASR X;
- the Gwalior report of 1925–26.

**ASR IX p. 109 (lead):** Cunningham records "an inscription of Udayâditya dated in Samvat 1137, or A.D. 1080", provenance unstated, and gives "[A.D. 1059 to 1080]". This bears on 4.4. Reconcile with CII's citation. Not evidence.

**Claims to phrase cautiously:**
- Durlabha III and the Cāhamāna help: Ganguly only.
- The Pānāheḍā rivalry: the editor's presumption.
- The Boar-temple hint: the editor's inference from a mostly illegible slab.
- The Nēmaka seat: the editor's reading of an abraded slab.
- The province of Bhilsa: a 1170s record, under the Caulukyas (U1).

**Old canon superseded here:**
- "founded 1059" as fact;
- "nephew";
- "does not hedge";
- the interrupted programme (now in 7.1 P3a);
- "Why Bhūmija" (now in 5.2).

---

# Chapter 5. The Udayeśvara Temple: Architecture, Sculpture and Religious Iconography

**Planned words:** 4,000 (5.1: 800 · 5.2: 900 · 5.3: 600 · 5.4: 950 · 5.5: 750). **Evidence:** `evidence_index/ch05.jsonl`.

**Historical question.** What does the building itself (its plan, its star-shaped tower, its carved surfaces and the order of its images) show about the foundation that raised it, and how much of the meaning scholars have found in it can the stone carry?

**Through-line.** By the end, the reader knows that Udayeśvara, as it stands, is a complete and precisely ordered Bhūmija temple with no surviving precursor, whose geometry, craft and image programme are the best evidence for what Udayāditya's foundation commanded, and that the Śaiva meanings read into it are scholars' readings laid over an arrangement that is itself documented.

**Arc.** Opening on the court as it now stands → (5.1) the ensemble as designed: platform, enclosure, attendant shrines, the separate *vedī*, the hall with three porches, and what has gone → (5.2) the generating geometry and the tower: rotated square, 32-point star, seven *bhūmi*s, and where this stands in the Malwa series → (5.3) the surfaces: mouldings, wall niches, doorways, pillars and ceilings as evidence of craft → (5.4) the image programme described from the building: what stands where, by quarter and by buttress → (5.5) what the programme has been made to mean, Pande's Śaiva Siddhānta reading set beside its limits; close on the flag-bearer figure and the temple's own written name, handing to Chapter 6.

**Scope.** The building itself: plan, platform and court, tower, surfaces and images. Its fabric is dated only by the 1080 record (Ch 4/6) and by proposals. Its later losses (the court's shrines, the western hall) are recalled from 1.3 as fabric. *Geographical:* the temple, with comparisons in the Malwa Bhūmija series (Un, Nemawar, Onkar Mandhata, Jamli) and the Deccan (Sinnar, Ambarnath) only where they place Udayeśvara. The hill's sculpture belongs to 7.1 P3a (one forward clause in 5.4).

**Editor's merge rulings carried into this plan** (from the master outline):
> **Editor's merge rulings for Chapter 5** (these override the entry below where they differ)
> - **Hill Naṭarāja and the hill's rock panels:** the entry sends them to Chapter 7. **Confirmed.** They are now in **7.1 P3a**. 5.4 keeps exactly one forward clause and gives no dimension.
> - **C05-JAGTA-EN-003** (Tiwari: a rock temple "like Ellora's", stopped at the initial stage) moves with the hill to 7.1 P3a, as a note.
> - **Shrine count:** home here, in **5.1** (Part I, I.3). No other chapter gives a number.
> - **Doctrine boundary:** 5.5 states Pande's Śaiva Siddhānta reading, attributed. Chapter 8 (8.5) cites 5.5 in a clause and does not re-describe the programme.
> - **Last paragraph:** ends on the flag-bearer and the name at the east doorway; it does not read the record (Chapter 6 opens there).
> - **Length:** ~4,000 words planned.

## 5.1 The court and the building it holds *(plan, platform, enclosure, attendant shrines, the vedī; what is missing · ~800 w)*

**Word target:** 800

- **Section statement:** By the end, the reader knows the temple as a designed ensemble and as it survives:
  - a red-sandstone shrine facing east on a high platform: sanctum, vestibule, a covered hall with three porches;
  - a separate, low, flat-roofed *vedī* on the same axis;
  - a square court with a low carved wall lined inside with seats, and stepped, guarded entrances;
  - eight attendant shrines, of which six stand in ruin;
  - and the place at the back where one of the court's structures has been replaced.
- **Purpose:** Give the reader the whole before its parts. Fix the canon's count (eight attendant shrines, Pande) and account for the missing fabric without re-telling the mosque.
- **Paragraph plan:**
  1. **P1 — The design's own axis.** **Point:** Re-orient the reader from today's western entrance to the temple's eastern axis. The temple faces east. It consists of *garbhagṛha*, *antarāla*, a *gūḍhamaṇḍapa* with three *mukhamaṇḍapa*s (east, north, south) and a separate low *vedī* on the same axis, all on an extensive, lofty *jagatī*. Its original approach was a stair flanked by over-life-size Śaiva door-guardians. Material: red sandstone, recalled in a clause from Ch 2 §2.3, not re-quoted. The sanctum has no internal ambulatory (*nirandhāra*), the rule for temples of its class.
     - E: C05-PANDE-001 (T5), C05-PANDE-002 (T5), C05-PANDE-003 (T5) · C: C05-MADHYABHARAT-005 (T5), C05-GANGULY-004 (T5), C05-TEMPLES-IND-005 (T5) · X: C05-ARTPAR-001 (T5), C05-KRAM-1-033 (T5) · Note: —
  2. **P2 — Hall and porches.** **Point:** The hall is the building's public interior. Three porches project as balconies, each with its own stepped entrance and door-guardians. The main entrance is the east porch, reached by a flight of steps. The porches carry seats (*kakṣāsana*s). The roof of the hall is a bell-roof (*saṃvaraṇā*) of tiers, pyramidal outside. Inside, four heavily carved main pillars carry a ceiling of concentric cusped rings in an octagonal frame (detail in 5.3). The great gable over the vestibule (*śukanāsa*) binds the two differently shaped roofs of sanctum and hall into one design.
     - E: C05-PANDE-004 (T5), C05-PANDE-005 (T5), C05-PANDE-006 (T5), C05-PARTEMPLES-001 (T5) · C: C05-KRAM-2-044 (T5), C05-GANGULY-005 (T5), C05-BHOJA-TIMES-006 (T5) · X: C05-KRAM-1-032 (T5) · Note: C05-GANGULY-005 (T5) (Ganguly counts eight pillars and four pilasters; Pande four main pillars. Keep Pande in the text and Ganguly in the note.)
  3. **P3 — The *vedī*.** **Point:** In front of the temple, on its axis, stands a separate square building: low and flat-roofed, its walls entirely of stone grilles, its roof on four massive pillars, with seats raised in two closed balconies. It survives in excellent condition. *What it was for is not settled*: Cunningham called it a hall for reading the Vedas; Ganguly reports it as built for a sacrifice after the temple's completion; Patil gives either a sacrificial hall or a shelter for a Nandi that no longer exists. The text keeps the question and gives the attributions in a note. Cunningham's dimensions (23 ft square inside; pillars 8½ ft) may be given with attribution, since they are the only measurements of any part of the ensemble in the map.
     - E: C05-PANDE-007 (T5), C05-PANDE-008 (T5), C05-PANDE-010 (T5) · C: C05-GANGULY-006 (T5), C05-GANGULY-007 (T5), C05-MADHYABHARAT-004 (T5) · X: C05-SAMAR-2-083 (T5) (normative only: the treatise prescribes a pavilion before a Bhūmija temple; paraphrase cautiously, never as the *vedī*'s purpose) · Note: C05-PANDE-008 (T5), C05-GANGULY-006 (T5), C05-MADHYABHARAT-004 (T5)
  4. **P4 — The court and its shrines, counted.** **Point:**
     - The temple stands in a spacious square court with a rectangular projection in the middle of each side, enclosed by a low wall carved outside and lined inside with seats with backrests. It probably had four entrances, each a flight of steps between door-guardians; all but the principal one are now closed.
     - Eight attendant shrines surrounded the temple (Pande). Six stand in various stages of ruin; two have gone entirely (Patil, the Gazetteer, Sharma).
     - Ch 1 §1.3 has already told the court as Cunningham saw it, with a shrine at each corner and a hall for the Vedas in the middle of each side. This paragraph does not re-tell it. It states the canon's figure and puts the variant counts in one note: Sharma's "six now, eight or nine at construction"; Krishna Deva's seven; Beglar's seven (Ch 7 item); Cunningham's four corner shrines and four *vedī*s.
     - **Compatibility is not identity.** Do not equate "eight shrines" with "four shrines + four *vedī*s".
     - E: C05-PANDE-001 (T5), C05-PANDE-009 (T5), C05-MADHYABHARAT-002 (T5), C05-MADHYABHARAT-003 (T5) · C: C05-GAZ-001 (T7), C05-GAZ-002 (T7), C05-ARTPAR-004 (T5) · X: C05-KRAM-2-004 (T5), C05-HARDY-003 (T5) (the five-shrine plan as the common pattern Udayeśvara exceeds) · Note: C05-ARTPAR-004 (T5), C05-TEMPLES-IND-006 (T5), C05-GANGULY-008 (T5), C07-PANDE-005 (T5)
  5. **P5 — What is missing, as fabric.** **Point:**
     - At the back of the temple, in the position matching the *vedī* in front, stood either a second *vedī* or an attendant shrine. It has been cleared, and a mosque stands there (Patil). Recall Ch 1 §1.3 in a clause: "the mosque already described". No dates, inscriptions or builder here.
     - Account for the lost corner shrine as one of the two missing structures in the count above. Do not decide which corner (Ch 1 §1.3 already notes NW vs NE).
     - The sanctum is entered today from the west side. In Tiwari's account the west doorway was raised from the rubble of broken *maṇḍapa*s and the east door has long been shut. This is memory, tier 8: attribute it, and give no date or agent.
     - Close by turning back to the sanctum, the one part of the ensemble that is complete.
     - E: C05-MADHYABHARAT-004 (T5), C05-PANDE-002 (T5) · C: C05-ARTPAR-003 (T5) (gateway on the west side of the enclosure) · X: — · Note: C05-JAGTA-HI-003 (T8), C05-JAGTA-EN-005 (T8), C05-JAGTA-EN-001 (T8)
- **Drafting guidance:**
  - Narrate closely along the axis. Compress the counts into one sentence plus one note.
  - No arrival scene, no visitor. "Today it is entered from the west" is a fact, not an experience.
  - Do not invent agents ("builders", "workmen").
  - Do not give the courtyard as "210 × 210": ARTPAR-003's units are missing and its OCR is damaged.
  - The *vedī*'s purpose must carry graded confidence ("was called…", "has been taken as…").
  - Introduce *jagatī*, *gūḍhamaṇḍapa*, *mukhamaṇḍapa*, *vedī* and *nirandhāra* once each, glossed in English.
  - The JAGTA items are testimony: "in Tiwari's account".
- **Transition:** From the one complete part of the ensemble, the sanctum, to the rule that generates it. The section's last sentence should leave the reader at the sanctum's star-shaped wall, so that 5.2 begins with why it is a star.

---

## 5.2 A star of seven tiers: the Bhūmija rule and where Udayeśvara stands *(geometry, tower, comparison · ~900 w)*

**Word target:** 900

- **Section statement:** By the end, the reader knows:
  - how the sanctum's plan is generated: a square rotated about its centre within a circle, with the four cardinal projections laid out square to the sanctum;
  - that this gives a 32-point star (seven projections a side, *saptaratha*);
  - that the wall-buttresses continue upward as chains of miniature spires (*kūṭastambha*), seven tiers of five in each quarter, between four flat bands (*latā*) of arch-lattice;
  - that a great antefix (*śukanāsa*) seals the east face and smaller ones the other three;
  - that the style appears in Malwa with no surviving precursor, so Udayeśvara is already its fullest version;
  - and how its neighbours compare: Un contemporary and simpler; the Amareśvara and Jamli later; Nemawar loftier but judged less well proportioned.
- **Purpose:** Turn "Bhūmija" from a label (Ch 1) into a rule the reader can see, and use the series of Malwa temples to say what the building shows about the workshop and patron behind it.
- **Paragraph plan:**
  1. **P1 — The rotating square.** **Point:**
     - The plan is not divided as a grid. The square is turned about its centre and stopped at regular intervals; its points describe a circle within which the intermediate buttresses are set.
     - The four main projections face the cardinal points and stay parallel to the sanctum's square.
     - The result is stellate-cum-circular, *saptaratha*: Hardy's "32-point star (equivalent to seven orthogonal projections)". This is the canon's figure.
     - Kramrisch's plan caption may be cited for the plan, but **not** its "1059–1080" span as fact (Ch 1 §1.4).
     - E: C05-PANDE-014 (T5), C05-PANDE-002 (T5), C05-HARDY-005 (T5) · C: C05-KRAM-2-007 (T5), C05-KRAM-2-019 (T5), C05-KRAM-1-033 (T5), C05-BHOJA-TIMES-012 (T5) · X: C05-PARTEMPLES-013 (T5) (the treatise's *parivartanā* rule, normative) · Note: C05-KRAM-1-034 (T5)
  2. **P2 — Wall becomes tower.** **Point:**
     - The buttresses read as pillars in the wall and continue in the same vertical lines as *kūṭastambha*s in the spire, so that the building appears to rise from the ground. This is one of Pande's readings of "Bhūmija"; give the others in one sentence: "earth-born", "country-born", "born of storeys".
     - Between the four *latā*s, each laced with *gavākṣa* lattice, are seven *bhūmi*s of five *kūṭastambha*s in every quarter. The shoulder repeats the star, and the *āmalaka*'s cogged rim answers its points.
     - The sources word the counts differently (Pande: "five rows vertically and seven horizontally"; Ganguly: thirty-five in five rows; Krishna Deva: seven vertical and five horizontal rows). All give 35 per quarter. State "seven tiers of five" and put the wording differences in a note.
     - E: C05-PANDE-015 (T5), C05-PANDE-017 (T5), C05-PANDE-018 (T5), C05-PANDE-020 (T5), C05-KRAM-2-020 (T5), C05-KRAM-2-021 (T5), C05-KRAM-2-022 (T5) · C: C05-PANDE-012 (T5), C05-PANDE-016 (T5), C05-KRAM-2-019 (T5), C05-HARDY-012 (T5), C05-BHOJA-TIMES-015 (T5) · X: C05-KRAM-2-108 (T5) (the same correspondence of wall and spire on non-stellate temples) · Note: C05-GANGULY-009 (T5), C05-TEMPLES-IND-006 (T5)
  3. **P3 — The antefixes.** **Point:**
     - The east face is sealed by a great *śukanāsa*: a blind arch over the vestibule, its lower part a pillared miniature shrine between dancing goddesses, its upper medallion a dancing Śiva. Name it here; describe its figures in 5.4.
     - On the other three faces smaller *śūrasenaka*s sit at the foot of the *latā*s, closer to the spire's curve.
     - A five-storeyed "celestial mansion" encases each side of the vestibule's superstructure.
     - E: C05-PANDE-003 (T5), C05-PANDE-028 (T5), C05-PANDE-048 (T5), C05-KRAM-2-009 (T5), C05-KRAM-2-084 (T5) · C: C05-KRAM-2-011 (T5), C05-PANDE-045 (T5), C05-ARTPAR-007 (T5) · X: C05-HARDY-015 (T5) · Note: —
  4. **P4 — No precedent, and what follows.** **Point:**
     - Hardy finds no surviving precedent: Udayeśvara is "already the deluxe model". The Bhūmija springs up ready-made, in styles new to the region, worked by specialist guilds, and it was the Paramāras' favoured mode.
     - Where it came from is disputed: born in Malwa (Krishna Deva, from the earliest nucleus at Onkar Mandhata); Deccani in design though Khajuraho-like in mouldings (Sarasvati, Mahesh Singh); possibly the lower Deccan, though Malwa's are the finest (Hardy).
     - The text keeps the question and states the inference with graded confidence: the maturity of the work implies a practised workshop whose earlier buildings do not survive.
     - The treatise attributed to Bhoja lists Bhūmija types (sixteen) and is often taken to show the court's interest. Say it is normative, and that its attribution to Bhoja is doubted. Never say the temple follows it.
     - E: C05-HARDY-005 (T5), C05-HARDY-012 (T5), C05-HARDY-013 (T5), C05-HARDY-019 (T5) · C: C05-HARDY-017 (T5), C05-PANDE-013 (T5), C05-PANDE-140 (T5), C05-PARTEMPLES-006 (T5) · X: C05-HARDY-018 (T5), C05-HARDY-021 (T5), C05-TEMPLES-IND-016 (T5), C05-TEMPLES-IND-014 (T5), C05-BHOJA-TIMES-011 (T5), C05-BHOJA-TIMES-013 (T5), C05-KRAM-1-063 (T5) · Note: C05-TEMPLES-IND-016 (T5), C05-BHOJA-TIMES-011 (T5), C05-HARDY-021 (T5), C05-JAGTA-EN-009 (T8) (the "9th–10th century" claim, as memory/report only)
  5. **P5 — Neighbours and successors.** **Point:**
     - **Un:** contemporary (an inscription of Udayāditya in the Chaubārā Ḍerā), with the same plan and spire design, simpler, and plain walls except the cardinal niches.
     - **The Amareśvara at Onkar Mandhata:** later, comparable in plan and form, dated 1063 by inscription (era flag; see Verification).
     - **Jamli:** about a decade later, the only non-stellate Bhūmija temple in Malwa.
     - **Nemawar's Siddheśvara:** later; its spire loftier, with nine rows, more ornate, but judged to lack Udayeśvara's grace and proportion. That is a judgement; attribute it.
     - **Further off:** Menal (contemporary, five storeys) and Ramgarh (about half a century later). In the Deccan, the Gondeśvara at Sinnar and Ambarnath.
     - **Udaypur's own rank:** Adhikari's verdict is already in Ch 1 §1.3; recall it in a clause and cite the evidence that supports it, Adhikari's claim that Un's artisans inspired Udayeśvara's (a direction of influence to attribute).
     - **Bhojpur:** enters only as Bhoja's own temple in a heritage account; the map gives no architectural comparison, so keep it to a clause or omit.
     - E: C05-TEMPLES-IND-017 (T5), C05-ARTPAR-010 (T5), C05-ARTPAR-011 (T5), C05-ARTPAR-012 (T5), C05-TEMPLES-IND-018 (T5), C05-ARTPAR-009 (T5), C05-PARTEMPLES-008 (T5) · C: C05-ARTPAR-005 (T5), C05-PARTEMPLES-002 (T5), C05-MADHYABHARAT-012 (T5), C05-TEMPLES-IND-019 (T5), C05-GANGULY-009 (T5), C05-KRAM-1-052 (T5) · X: C05-GANGULY-011 (T5), C05-PARTEMPLES-010 (T5), C05-RAJABHOJ-EN-001 (T9) · Note: C05-PARTEMPLES-010 (T5), C05-ARTPAR-013 (T5)
  - **Evidence pass (C, optional by default; P0):** C05-PANDE-019 (T5), C05-KRAM-2-023 (T5), C05-KRAM-2-043 (T5) — the śikhara's four latās and the bands of the central offset (Pande, Kramrisch), for P2–P3 if needed
- **Drafting guidance:**
  - Explain the geometry once, plainly, as a rule; no symbolism here.
  - Never "the largest Bhūmija temple" (C05-GEOHER-001 (T7)'s superlative is a survey's claim; omit it or put it in a note as the survey's).
  - Never quote SAMAR. If used, paraphrase: "a treatise on architecture attributed to Bhoja, though the attribution is doubted, describes…".
  - Comparisons are dated relatively ("contemporary", "a decade later"); no new absolute dates for Udayeśvara.
  - Hardy's "three imperial monuments" was a Ch 1 note. Do not reuse it as a discovery.
- **Transition:** From the rule to the hand: the same star that sets the spire sets every facet of the wall. Those facets are where the craft and the images are, which leads to 5.3.

---

## 5.3 Surfaces: mouldings, doorways, pillars and ceilings *(craft as evidence · ~600 w)*

**Word target:** 600

- **Section statement:** By the end, the reader knows that the temple's surfaces follow an ordered sequence from base to cornice and from door-frame to ceiling, executed with a precision every observer remarks on, and what that order shows about the workshop: a programme fixed in advance, in which plain surfaces were set against carved ones by design.
- **Purpose:** Give the craft its evidence without an inventory. Choose the four places where the stone shows the most about method: the base, the wall-niches, the doorways and the hall pillars.
- **Paragraph plan:**
  1. **P1 — Base and wall.** **Point:**
     - Five mouldings make the base: two plinth courses, the lotus-shaped *jāḍyakumbha*, the knife-edged *karṇaka* and a band of devouring faces (*grāsapaṭṭī*).
     - Above, on every buttress, small niches (*khattikā*) on the base and larger niches (*khattaka*) on the wall house the gods.
     - The recesses between the buttresses are carved with lotus scrolls and celestial women.
     - The pattern is the same on sanctum and hall.
     - Adhikari's comparison: Udayeśvara has more, and more varied, mouldings than Un, and even its recesses are ornamented.
     - E: C05-PANDE-026 (T5), C05-PANDE-025 (T5), C05-PANDE-027 (T5), C05-PANDE-029 (T5), C05-PANDE-053 (T5) · C: C05-KRAM-2-040 (T5), C05-KRAM-2-081 (T5), C05-PARTEMPLES-011 (T5), C05-KRAM-1-081 (T5) · X: C05-HARDY-024 (T5), C05-HARDY-027 (T5) · Note: C05-KRAM-2-042 (T5), C05-BHOJA-TIMES-013 (T5) (Khajuraho-like mouldings, Deccani design)
  2. **P2 — Doorways.** **Point:**
     - The porch doorways carry many bands (lotus scroll, flying figures, pillarets, figural bands), with river goddesses and guardians of the directions at the foot. Most are now broken or defaced.
     - The sanctum door has five jambs a side, the outermost with horsemen, Gaṇeśa and Śiva on the lintel, and five goddesses on the frieze above (Ganguly).
     - What the river goddesses at a door signify (purification) belongs to the general theory; keep it to a clause, attributed, or omit.
     - E: C05-PANDE-032 (T5), C05-PANDE-033 (T5), C05-GANGULY-013 (T5) · C: C05-PANDE-031 (T5) · X: C05-KRAM-2-028 (T5), C05-TEMPLES-IND-022 (T5) · Note: —
  3. **P3 — Pillars and ceilings.** **Point:**
     - The four main hall pillars are square to about mid-height, then octagonal, then round, under four-sided bracket capitals: the "mixed" (*miśraka*) type.
     - Two measurements agree: Kramrisch's square of 2 ft 9 in at the base with sections of 5 ft 6 in, 3 ft 8 in and 1 ft 3 in, and Sharma's total of 10 ft 5 in. Give them with attribution: the only interior measurements in the map.
     - Flying *vidyādhara*s with swords and shields circle the round section.
     - The hall ceiling is of concentric cusped rings in an octagonal frame (*nābhicchanda*), with devouring faces at the corners; Sharma adds supporting bracket-figures. The *vedī*'s ceiling closes by overlapping slabs on a lotus stone (from 5.1; do not repeat).
     - The Nandi now in the hall has been judged modern from its style (Sharma). Note that it is not evidence for the original programme.
     - E: C05-PANDE-034 (T5), C05-KRAM-2-045 (T5), C05-ARTPAR-014 (T5), C05-PANDE-035 (T5) · C: C05-PANDE-138 (T5), C05-ARTPAR-018 (T5), C05-GANGULY-005 (T5) · X: C05-KRAM-1-031 (T5) · Note: C05-ARTPAR-020 (T5), C05-KRAM-2-012 (T5)
  4. **P4 — What the craft shows.** **Point:**
     - Beglar's judgement (via Ganguly) is the one quotation this section carries: the floral ornament is fine and free, and plain surfaces are interposed so that carved and plain enhance each other. Let it carry the point that restraint was designed. Fergusson's "few temples of its class give a better idea of the style" may follow in a clause.
     - Then state the inference: a programme this uniform across sanctum and hall implies a single design carried through. Do not claim duration. Construction-time claims (three years; over twenty) are Tiwari's and are not evidence; omit them or note them as memory.
     - E: C05-GANGULY-012 (T5) · C: C05-MADHYABHARAT-009 (T5), C05-TEMPLES-IND-025 (T5), C05-BHOJA-TIMES-006 (T5) · X: C05-MADHYABHARAT-013 (T5) · Note: C05-JAGTA-HI-004 (T8), C05-JAGTA-HI-005 (T8) (construction time as memory only)
  - **Evidence pass (X, optional by default; P0):** C05-PANDE-030 (T5), C05-KRAM-2-041 (T5), C05-PANDE-038 (T5) — moulding sequence, the pillar fillet, the lotus-bud necklace (dating by style: 11th–12th c., proposal)
- **Drafting guidance:**
  - Compress: name each moulding once in a single sentence; do not walk every band.
  - One quotation only (Beglar).
  - No "skilled artisans", no "thousands of craftsmen": the evidence is the work, not the workers.
  - Sharma's "surpasses ivory carving" is a judgement; omit or attribute.
  - The Konārka *mithuna* comparison (C05-ARTPAR-019 (T5)) is a passing remark; omit (listed in unused).
- **Transition:** The niches are frames, and frames placed by rule. Who stands in each is the next question, and the answer is as ordered as the geometry.

---

## 5.4 Who stands where: the image programme described *(description only, no symbolism · ~950 w)*

**Word target:** 950

- **Section statement:** By the end, the reader knows the programme as it is placed on the building:
  - dancing Śiva at the head of every face: the great *śukanāsa* on the east and the three *śūrasenaka*s;
  - on the east antefix, a rare dancing Sarasvatī and a composite image of Sūrya, Viṣṇu, Śiva and Brahmā;
  - the eight guardians of the directions, always on the central or second buttress, paired by their mounts;
  - on the sanctum, eight Mothers (*aṣṭamātṛkā*) gathered round Vīrabhadra on the south and west and round Cāmuṇḍā on the north;
  - fierce forms by the side porches; Umā-Maheśvara repeated through the lower niches;
  - Viṣṇu present but rare, with one Lakṣmī-Nārāyaṇa in a shadowed niche;
  - Mothers and the nine planets over the south door;
  - and almost every image broken.
- **Purpose:** Fulfil the chapters.md requirement: description of the programme kept apart from interpretation. 5.5 depends on it.
- **Paragraph plan:**
  1. **P1 — The dancer at the head of each face.** **Point:**
     - **East *śukanāsa*:** in its upper medallion a many-armed Naṭeśa dances the *tāṇḍava* in the raised-knee pose (*ūrdhvajānu*), with dancing goddesses and *gaṇa*s. The broken Sarasvatī among them is shown dancing, not playing the vīṇā, which Pande calls rare.
     - **Below:** a pillared shrine holds a composite image of Sūrya with Viṣṇu and Śiva (Hariharārkapitāmaha).
     - **The three *śūrasenaka*s:** each again has Naṭeśa. On the north, the main arm crosses the body like an elephant's trunk. Below each is a seated Śiva: on the west, a six-armed figure of particular finesse; on the south, with Nandi.
     - **North-west face of the spire:** a human figure climbs, apparently holding a flag-staff. Describe it here; its readings go to 5.5.
     - **Forward pointer:** the hill Naṭarāja (Ch 7), one clause.
     - E: C05-PANDE-037 (T5), C05-PANDE-039 (T5), C05-PANDE-043 (T5), C05-PANDE-048 (T5), C05-PANDE-051 (T5), C05-PANDE-052 (T5), C05-PANDE-049 (T5) · C: C05-KRAM-2-084 (T5), C05-ARTPAR-016 (T5), C05-ARTPAR-025 (T5), C05-PANDE-036 (T5), C05-GANGULY-014 (T5) · X: C05-ARTPAR-007 (T5) · Note: C05-PANDE-044 (T5) (composite images common in the region's Śaiva temples), C05-PANDE-041 (T5) (Nāṭyaśāstra context, Pande's)
  2. **P2 — Guardians in their quarters, set by rule.** **Point:**
     - On the hall, the guardians of the directions (*dikpāla*s) always occupy the niches of the central or second buttress: Indra facing east with his elephant, Varuṇa on his crocodile to the west, Vāyu with his consort, Īśāna with his bull.
     - On the sanctum, the central buttress again holds them (Agni and Nirṛti).
     - The elephant-mounted Indra and Kubera are set on the second buttresses south-east and north-east. The bull-mounted Yama and Īśāna face each other south and north.
     - Kubera's and Īśāna's places appear exchanged. Pande explains it by symmetry: give the observation as fact and her reason as hers.
     - Ardhanārīśvara on the south-east balances Hariharārkapitāmaha on the north-east, which the morning sun lights entire (Pande).
     - Patil's and the Gazetteer's summary ("guardians in their proper positions; Śiva and Durgā predominate") corroborates in a clause.
     - E: C05-PANDE-057 (T5), C05-PANDE-058 (T5), C05-PANDE-076 (T5), C05-PANDE-075 (T5), C05-PANDE-082 (T5), C05-PANDE-085 (T5) · C: C05-PANDE-070 (T5), C05-PANDE-069 (T5), C05-PANDE-071 (T5), C05-PANDE-060 (T5), C05-PANDE-080 (T5), C05-PANDE-083 (T5) · X: C05-MADHYABHARAT-015 (T5), C05-GAZ-006 (T7), C05-KRAM-1-084 (T5) · Note: C05-PANDE-075 (T5)
  3. **P3 — Mothers round the sanctum; goddesses to the north.** **Point:**
     - Each of the sanctum's three spines is encircled by the eight Mothers. On the south and west, six surround Vīrabhadra striking Dakṣa, with two more on the flanking buttresses (Nandikeśvarī, Kaumārī, Gaṇeśānī). On the north, Cāmuṇḍā stands emaciated on a corpse with a scorpion on her belly, with Māheśvarī as the eighth.
     - The bovine-headed Nandikeśvarī takes the place usually given to the boar-headed Vārāhī. Give this as fact; the "deliberate" reading goes to 5.5.
     - Cāmuṇḍā is concentrated in the northern quarter, as on Paramāra temples in Vāgaḍa.
     - Mahābhairava with his dog by the south porch and Cāmuṇḍā by the north stand as a matched pair. Mahiṣāsuramardinī is by the north porch.
     - Kārttikeya on the west has six faces and twelve arms.
     - E: C05-PANDE-095 (T5), C05-PANDE-086 (T5), C05-PANDE-094 (T5), C05-PANDE-084 (T5), C05-PANDE-024 (T5), C05-PANDE-054 (T5) · C: C05-PANDE-115 (T5), C05-PANDE-077 (T5), C05-PANDE-072 (T5), C05-PANDE-087 (T5), C05-PANDE-134 (T5) · X: C05-ARTPAR-015 (T5) · Note: C05-PANDE-024 (T5) (Vāgaḍa parallels)
  4. **P4 — The many and the few.** **Point:**
     - Umā-Maheśvara, seated in two standard types, fills most of the lower niches. With them are Gaṇeśa, Brahmā-Brahmāṇī and Sarasvatī with book and lotus.
     - The hall's upper registers (*tilaka*) carry four ten-armed seated Śivas between two Śakti images, on both sides.
     - Viṣṇu is rare: a single niche figure, the Harihara, and the temple's only Lakṣmī-Nārāyaṇa tucked into a shadowed niche.
     - Inside the hall, pillar niches carry Śiva and an ascetic Pārvatī with *liṅga*, Gaṇeśa and fire-pits.
     - Over the south door are nine goddesses and above them the nine planets, Rāhu, Ketu and probably Saturn grouped together.
     - On the east porch rail, an unusual woman with a staff and a camel (identity disputed; Pande reads Nirṛti).
     - The CII editor notes that the *praśasti* invokes Pārvatī and Gaṇeśa after Śiva, the first time in this house's records. This is a point of agreement between word and stone, for Ch 6 to develop; one clause here.
     - E: C05-PANDE-065 (T5), C05-PANDE-064 (T5), C05-PANDE-063 (T5), C05-PANDE-096 (T5), C05-PANDE-098 (T5), C05-PANDE-114 (T5), C05-PANDE-100 (T5), C05-PANDE-102 (T5) · C: C05-PANDE-059 (T5), C05-PANDE-089 (T5), C05-PANDE-093 (T5), C05-PANDE-103 (T5), C05-PANDE-104 (T5), C05-PANDE-099 (T5) · X: C05-CII-002 (T1) · Note: C05-PANDE-117 (T5) (Nirṛti identification)
  5. **P5 — Broken images.** **Point:**
     - Nearly every figure is mutilated: arms, heads and attributes struck away. Pande notes the losses image by image, and identifications often rest on mounts and surviving attributes.
     - State this as the condition of the evidence, with no agent or date. Tiwari's account of a beheaded, ten-armed goddess (and its rhetoric of the attackers' motives) is memory; at most attribute one sentence, without the imputed motives.
     - E: C05-PANDE-032 (T5), C05-PANDE-077 (T5), C05-PANDE-090 (T5) · C: — · X: — · Note: C05-JAGTA-EN-010 (T8), C05-JAGTA-EN-011 (T8), C05-JAGTA-HI-011 (T8)
  - **Evidence pass (X, optional by default; P0):** C05-PANDE-061 (T5), C05-PANDE-067 (T5), C05-PANDE-073 (T5), C05-PANDE-079 (T5), C05-PANDE-088 (T5), C05-PANDE-097 (T5), C05-PANDE-101 (T5), C05-PANDE-055 (T5), C05-PANDE-047 (T5) — further images in the programme (Naṭeśa near the south porch, Umā-Maheśvara and Gaṇeśa on the vedībandha, the multi-armed goddess, the tilaka images, Kaumārī and Kumāra, the three-faced Brahmā, the Mothers with Navagraha above, Sūrya, Gaurī with iguana); use for positions only, never symbolism
- **Drafting guidance:**
  - **This section uses no symbolic vocabulary.** No "pure path", "creation", "cosmos" or "victory". Śiva "dances", not "dances creation".
  - Not a catalogue: each paragraph's Point is a regularity, and images are cited as instances of it. Choose two or three per paragraph.
  - Introduce *dikpāla*, *aṣṭamātṛkā*, *śūrasenaka* and *tilaka* once.
  - Pande's text-matches (Aparājitapṛcchā, Kāmikāgama, SAMAR) belong to 5.5, not here.
  - Never quote SAMAR.
  - "Pande identifies…" wherever identification rests on a broken image.
- **Transition:** The regularities ask to be explained: why the dancer at every summit, why goddesses to the north, why Nandikeśvarī for Vārāhī. 5.5 sets out the explanation that has been offered, and its limits.

---

## 5.5 What the programme has been made to mean *(interpretation, attributed and bounded · ~750 w)*

**Word target:** 750

- **Section statement:** By the end, the reader knows:
  - the principal reading of the programme, Pande's: the temple as an expression of Śaiva Siddhānta, the east antefix as the five "pure" principles and Śakti placed on the left because the feminine is "left";
  - the narrower readings attached to single images (Mṛtyuñjaya and "a temple built for victory"; the deliberate Śaiva Mothers; the flag-bearer as victor, architect or king);
  - the general theories it draws on (Kramrisch's temple as manifestation) and the critique of them (Granoff, through Hardy);
  - what of all this the stone itself supports.
- **Purpose:** Give interpretation its own space, attributed throughout. Decide how much theology Ch 5 needs: only enough to state Pande's reading intelligibly (Śiva, Śakti and the "pure path" in one sentence each). Doctrine, ritual and Bhoja's *Tattvaprakāśa* are Ch 8's.
- **Paragraph plan:**
  1. **P1 — Pande's reading.** **Point:**
     - Pande holds that the temple rests on Śaiva Siddhānta, the Paramāras' Śaivism (Bhoja's authorship of a treatise on it is recalled in a clause and left to Ch 8), and that she decoded the images from the Āgamas and *śilpa* texts of the period.
     - The east antefix shows the five components of the "pure path" (*śuddha adhvā*): Śiva and Śakti in the dance, Īśvara as the dancing creator, Sadvidyā as Sarasvatī, and the composite image as an aid to meditation on Sadāśiva.
     - Śakti dominates the left (north) because the feminine is *vāmā*.
     - Give the doctrine minimally: one sentence for the pure path.
     - E: C05-PANDE-110 (T5), C05-PANDE-116 (T5), C05-PANDE-121 (T5), C05-PANDE-109 (T5) · C: C05-PANDE-120 (T5), C05-PANDE-123 (T5) · X: C05-KRAM-2-075 (T5) (Kramrisch independently reads such a composite Sūrya as a support of meditation on Sadāśiva on a Śiva temple) · Note: C05-PANDE-118 (T5), C05-PANDE-125 (T5)
  2. **P2 — Readings of single images.** **Point:** Several readings attach to single images, each a different kind of claim. Each must be marked as Pande's inference:
     - Nandikeśvarī replacing Vārāhī as "a deliberate attempt" at an exclusively Śaiva character;
     - the six-armed Mṛtyuñjaya as fitting "since this temple was built for victory". The premise is hers, not an inscription's; say so;
     - the staff-and-camel figure as Nirṛti, with the camel as delusion and the reins as the bond (*pāśa*);
     - Agni's book as the Vedas and the fire rite.

     Where an image matches a text she cites (Harihara and the *Devatāmūrtiprakaraṇa*; Kārttikeya's twelve arms and the treatise attributed to Bhoja, which prescribes twelve arms for a town; the *vidyādhara*s' swords and shields), state the match as hers. These texts are normative and say nothing about Udaypur's intent. The twelve-arm "town" prescription sits uneasily with the Kāmikāgama rule Pande cites for "village" Śiva temples; keep it to a note.
     - E: C05-PANDE-115 (T5), C05-PANDE-111 (T5), C05-PANDE-117 (T5), C05-PANDE-112 (T5) · C: C05-PANDE-129 (T5), C05-PANDE-087 (T5), C05-PANDE-138 (T5), C05-PANDE-139 (T5), C05-PANDE-136 (T5) · X: C05-PANDE-143 (T5) (⚠ SAMAR via Pande, paraphrase only), C05-ARTPAR-024 (T5) · Note: C05-PANDE-095 (T5), C05-PANDE-143 (T5)
  3. **P3 — The frame behind the reading, and its critics.** **Point:**
     - Kramrisch's influential view treats the temple as the manifest body of the god: images projected outward from the sanctum, the devotee's circling as comprehension.
     - Hardy reports Granoff's objection: placement often lacks such logic, and temples match the Purāṇas' heavens better. He also reports Bafna's doubt about the site-diagram as a blueprint.
     - The point is not to adjudicate. Udayeśvara is a case where placement *is* highly ordered (5.4), which gives Pande's reading more purchase than the general theory has elsewhere, but no more than the order itself proves.
     - Sharma's phrase, "a religious poem written in stone", may close the paragraph as an attributed judgement.
     - E: C05-HARDY-032 (T5), C05-HARDY-030 (T5) · C: C05-KRAM-2-046 (T5), C05-KRAM-2-085 (T5), C05-HARDY-037 (T5) · X: C05-HARDY-035 (T5), C05-TEMPLES-IND-026 (T5) · Note: C05-ARTPAR-023 (T5)
  4. **P4 — The flag-bearer and the name.** **Point:**
     - The climbing figure on the spire has been read three ways:
       - a flag-bearer hoisting the flag of victory (Pande, who adds a modern Dwarka analogy as hers);
       - "probably a statue of Udayāditya" holding the staff (Ganguly);
       - the architect, or the royal builder climbing to heaven by merit (Patil reports both).
     - None is documented. The figure is real, and its readings are claims; the text keeps the question.
     - It links to the temple's record of a completed flag-hoisting in V.S. 1137 and to the god's name, Udayeśvara, carved at the east doorway. Recall in a clause: the 1080 record's three readings are Ch 1 §1.4's, its text is Ch 6's.
     - Close on the temple as a carrier of words as well as images, handing to Ch 6.
     - E: C05-PANDE-036 (T5), C05-GANGULY-014 (T5), C05-MADHYABHARAT-008 (T5) · C: C05-PANDE-106 (T5) · X: C06-CII-006 (T1), C04-CII-119 (T1) (recall only) · Note: C05-PANDE-106 (T5), C05-GANGULY-014 (T5)
- **Drafting guidance:**
  - Every interpretive sentence carries its author ("Pande reads…", "in Kramrisch's account…").
  - No "the temple symbolises" in the narrator's voice.
  - Theology at minimum (flag the overlap with Ch 8 below).
  - Never quote SAMAR, even through Pande: paraphrase and add the attribution doubt once.
  - Kramrisch's metaphysics (Kīrtimukha, Vāstupuruṣa, Bindu) stays out except as one sentence of the general theory.
  - Do not reuse the founding date; do not call 1080 "consecration".
- **Transition (out of the chapter):** The flag-bearer's meaning is argued; the record of the flag-hoisting is written. The next chapter turns from carved figures to carved words.

## Chapter 5: conflicts to present, unresolved

| Conflict | Where | How held |
|---|---|---|
| Shrine count: eight (Pande, Patil), seven (Beglar, Krishna Deva), "eight or nine" (Sharma), four corner shrines + four *vedī*s (Ganguly; 1.3) | **5.1 (home)** | Pande's eight in the text, as "eight attendant shrines"; the variants in one note; never contradict 1.3's description of the court |
| Hall pillars: Pande's four main pillars vs Ganguly's "eight pillars and four pilasters" | 5.1 / 5.3 | Note only; no reconciliation without a plan |
| Tower wording ("five rows vertically and seven horizontally" vs "seven *bhūmi*s of five") | 5.2 | "Seven tiers of five", with Krishna Deva's wording in the note |
| Bhūmija origin: Malwa / Deccan / lower Deccan | **5.2 P4 (home)** | Open; attributed in a note |
| Amareśvara's "1063" (era unclear) | 5.2 | No comparative date unless verified (flag) |
| Identifications of broken images; the Kubera/Īśāna exchange | 5.4 | "Probably", per Pande; the alternatives in a note |
| What the programme means (Pande's Śaiva Siddhānta reading, Kramrisch's general symbolism) | **5.5 (home)** | Attributed; bounded; said once |
| Builder and date | Ch 4 / Ch 6 | Not restated; 1059 is never a founding date here |

## Chapter 5: hand-offs

- **In:** Chapter 4 hands over to the building. Open on a plain, checkable fact that carries the chapter's question: the temple faces east, and its main approach was a stair from the east flanked by over-life-size Śaiva door-guardians, but today it is entered from the west (C05-PANDE-002; C05-PANDE-011). The building has to be read against the way it is now met. The first paragraph re-orients the reader to the design's own axis, east to west: stair, porch, hall, vestibule, sanctum. It does not narrate an arrival.
- **Out:** The last paragraph moves from the disputed flag-bearer to the written record of the flag-hoisting and the god's name at the east doorway. Then, in one sentence, it notes that the temple's pillars, seats and parapet carry other writing, from pilgrims' lines to a lettered slab. It must **not**: - read or translate any inscription; - restate the date debate; - mention the mosque's inscriptions; - end on a superlative or a moral.

## Chapter 5: changes from the master outline

1. **Evidence pass:** optional corroborating and context items added to 5.2, 5.3 and 5.4 (direct Pande and Kramrisch items not used in the outline). Omitted by default (P0) unless a section lands short.
2. No structural change. The hill's sculpture is confirmed in 7.1 P3a.

## Chapter 5: research and verification flags

- Hill Naṭarāja: the canon's object details are not in this map.
- Shrine count.
- Amareśvara "1063".
- Hall pillars.
- Tower counts wording.
- Bhūmija origin
- Builder and date
- Survival legend
- "Bijamandal" in the comparison list.
- Bhojpur.
- SAMAR items
- Kārttikeya "town" vs Gaurī "village" rule
- Stronger evidence wanted:
- Graded wording, suggested:
- **Page-image checks:** INTACH's "82 × 42 meters" (C05-INTACH-002), never used; the Amareśvara date (C05-ARTPAR-012, C05-TEMPLES-IND-018).
- **Staged sources (leads, `ocr_verify`):** Beglar, ASR VII and Cunningham, ASR X, for a measured description; to be added after ingest only.
- **SAMAR:** ⚠ old OCR; paraphrase only after re-OCR check; the attribution to Bhoja is doubted.

---

# Chapter 6. Inscriptions and Intellectual Life: Epigraphy, Languages and Literary Culture

**Planned words:** 4,050 (6.1: 800 · 6.2: 900 · 6.3: 900 · 6.4: 800 · 6.5: 650). **Evidence:** `evidence_index/ch06.jsonl`.

**Historical question.** What do Udaypur's inscriptions say, in what language and form, and who made them say it? What can these words establish about authority, patronage and learning, and what can they not?

**Through-line.** By the end, the reader knows that Udaypur's inscriptions are several archives made by different hands for different ends. They show kings, officials and *paṇḍita*s using Sanskrit learning to make authority visible, and a new order later writing itself onto the same stones in Persian. They establish claims, gifts, names and dates, but not a school, a court or a reading public in the town.

**Arc.** The signed six lines of 1080 at the east door (6.1) → the king's poem of descent (6.2) → the serpentine scimitar of letters (6.3) → the porch archive, 1163–1639, where the register falls from verse to prose to local speech (6.4) → Persian as a new language of authority, and the limits of an archive largely unpublished (6.5).

**Scope.** *Chronological:* the founding generation's texts (the V.S. 1116 text, the 1080 record, the praśasti, the serpent charts; c. 1059–c. 1100), the porch records 1163–1232, later royal records to V.S. 1366, pilgrims to V.S. 1696 (1639), and Persian inscriptions 1336–1632. *Geographical:* the temple's east door, porches and pillars; Amērā (about 3 km south); Vidisha (Chhittapa's eulogy) as the province's court standard; the royal Śiva temples of Ujjain, Dhār and Ūn for the serpent charts. Bhoja's Dhārā is the frame, never the subject.

**Editor's merge rulings carried into this plan** (from the master outline):
> **Editor's merge rulings for Chapter 6** (these override the entry below where they differ)
> - **Opening:** confirmed. Chapter 5's last paragraph ends at the east doorway with the flag-hoisting and the god's name. Chapter 6 alone opens at the east door (Part I, I.5). The entry's "(editor: confirm its last line)" is answered.
> - **6.4 is the home of every porch record as text:** place on the stone, script, register, date conversion and the Lūṇapasāka 1172/1173 note. Chapter 8 (8.1) uses the 1229 and 1232 records for what was given; Chapter 10 uses them for who governed. Neither converts dates or discusses wording.
> - **Inscription count:** home in 6.4 P1 and 6.5 P3. No figure from Tiwari ("more than a hundred").
> - **Kumārapāla 1163 (C06-GANGULY-034) and V.S. 1220 (C10-PARTEMPLES-001)** are cited together and never merged. Chapter 10 opens on the V.S. 1220 record (I.5), so 6.4 P2 must give that record's *text and place* only, briefly, and leave the political reading to 10.1.
> - **The V.S. 1366 Jayasiṃha record:** 6.4 P5 may list it as a later royal record. Its meaning (the last Paramāra-titled trace) is 10.3 P1's.
> - **Locator corrected at merge:** C06-CII-007 is p. 131 in the map, not p. 113.
> - **Length:** ~4,050 words planned.

## 6.1 Six lines at the door *(the 1080 record, its writer, and the other early writing on this ground · ~800 w)*

**Word target:** 800

- **Section statement:** By the end, the reader knows that the temple's first dated words are a short, mostly prose Sanskrit record that names its own poet: Paṇḍita Mahipāla, son of Paṇḍita Śṛṅgavāsa. Within a generation, verse was also being composed and cut for a Brāhmaṇa's tank 3 km away, by a *paṇḍita* whose son engraved it. Court Sanskrit of a far higher polish had already been carved in the province, at Vidisha. The reader also knows that the V.S. 1116 text, the other "founding" record, is by its readers' account a poor and error-filled one, and that this matters for what it can carry.
- **Purpose:** Begin "intellectual life" with people, not with Bhoja: name the literate men whom Udaypur's own early records name, and set the registers side by side.
- **Paragraph plan:**
  1. **P1 — A signed record.** **Point:** Show what the V.S. 1137 record *is* as a text. Six lines to the right of the east doorway; Sanskrit in eleventh-century Nāgarī; prose with a single *anuṣṭubh* verse. It opens *svasti* with the wish that King Udayāditya make the earth "one umbrella" (a single sovereignty). It names the verse's maker, Paṇḍita Mahipāla, son of Paṇḍita Śṛṅgavāsa, then gives the date and states that the flag-hoisting of Śrī Udayeśvaradeva "is complete", closing "*maṅgalaṃ mahāśrīḥ*". The date's three readings are recalled in a clause (1.4), not re-argued. Quote the two short phrases (the umbrella wish; "flag-hoisting … complete") from the edited line where CII has it; the rest is paraphrase.
     - E: C06-CII-006 (T1), C06-JAGTA-HI-001 (T8), C06-JAGTA-HI-008 (T8), C06-JAGTA-HI-009 (T8), C06-JAGTA-HI-010 (T8), C06-JAGTA-EN-034 (T8) · C: C06-JAGTA-EN-004 (T8), C06-JAGTA-EN-007 (T8), C06-JAGTA-EN-009 (T8), C06-JAGTA-EN-010 (T8), C06-PARTEMPLES-003 (T5) · X: C06-CII-025 (T1), C06-CII-029 (T1) · Note: C06-JAGTA-EN-006 (T8), C06-JAGTA-HI-003 (T8) (Verma's reading and his day-equivalent, 30 March 1080, a Monday; the record gives no weekday)
  2. **P2 — What the form says about authority.** **Point:** Read the form as evidence. The king appears only in a conventional wish of universal rule. The temple is named after him, Udayeśvara, "evidently after the name of its constructor" in the editor's words. The ritual is recorded as *completed*. The person named as maker is the poet, not a donor or an official. So the record establishes a royal temple's name and a completed rite in V.S. 1137; it does not say who paid, who built, or who stood at the ceremony. Add that no contemporary record calls the temple Nīlakaṇṭheśvara: the name the village uses is not the name its stones use.
     - E: C06-JAGTA-HI-028 (T8), C06-JAGTA-EN-030 (T8) · C: C04-CII-119 (T1) (home Ch 4: the editor's "after the name of its constructor"), C06-JAGTA-EN-027 (T8), C06-JAGTA-HI-007 (T8) · X: C04-CII-108 (T1) · Note: C06-PARTEMPLES-003 (T5) (Adhikari calls the record a *praśasti* with construction and consecration details; the six lines as transcribed carry neither)
  3. **P3 — Court verse in the province.** **Point:** Change scale once, to show the register that Udaypur's record is *not*. A eulogy of the Sun-god from Vidisha was composed by Paṇḍita Chhittapa, who bore the title *mahākavi-cakravartin*. It was commissioned by Śrīcandra, a *daṇḍanāyaka* probably in charge of the country around Bhilsa. Sircar placed the slab in the temple of Bhāillasvāmin, and later anthologies quote Chhittapa as a poet of Bhoja's time. In this province, then, officials commissioned court-standard verse in stone. One paragraph only; do not retell the Bhāillasvāmin temple (Ch 3).
     - E: C06-CII-075 (T1), C06-CII-073 (T1), C06-CII-076 (T1) · C: C06-CII-074 (T1), C03-CII-007 (T1) · X: C06-GAZ-004 (T7) · Note: C06-GAZ-004 (T7) (the Gazetteer dates the Sun temple "V.S. 935 (A.D. 992)", an internally inconsistent pair; CII's plate list gives the eulogy as "(Date lost?)" [C06-CII-048 (T1)]; follow CII and give no date)
  4. **P4 — A Brāhmaṇa's tank, a paṇḍita's verse.** **Point:** The nearest other early writing is not royal. A slab found in 1923–24 beside a ruined tank at Amērā, about 3 km south of Udaypur, records that a Brāhmaṇa named Vikrama built the tank in Naravarman's reign. It is Sanskrit verse, apparently fifteen stanzas, followed by three prose lines of date, writer and engraver. The writer, a Paṇḍita whose name survives only as its last two syllables, *-pāla*, composed it, and his son Saumatika cut it. Its Nāgarī is of the late eleventh or early twelfth century. Its engraving was poor enough that the record went unedited until CII. Point to draw: by the 1090s men of letters near Udaypur wrote verse for private patrons, and the craft passed from father to son. Graded: "suggests", from one record. Date: V.S. 1151, with the editor's note that it "does not admit of verification"; give 1094 as the editor's working equivalent, with the alternatives in a note. The tank's cost and construction belong to Ch 7.
     - E: C06-CII-032 (T1), C06-CII-011 (T1), C06-CII-012 (T1), C06-CII-061 (T1) · C: C06-CII-031 (T1), C06-CII-013 (T1), C06-CII-060 (T1) · X: C07-CII-003 (T1) · Note: C06-CII-010 (T1), C04-CII-087 (T1) (V.S. 1151 = 1093, 1094 or 1095 by reckoning; the editor reconciles it with Naravarman's succession)
  5. **P5 — The other founding text.** **Point:** Treat the V.S. 1116 record *as a text*, not as a date (the date question is 1.4/1.5 and Ch 4). As reported, it runs to twenty-two lines and is "teeming with errors": its language and grammar are faulty and its execution poor, which makes a meaningful translation hard. It opens with Śiva's worship and then turns to Udayāditya. Contrast it with the 1080 record's clean formula and Chhittapa's polish. Its quality is evidence about how it was made, and a reason for caution before it carries the founding date. Do **not** identify it with the "perfunctorily executed" sixteenth-century record Ganguly and the CII editor discuss: no item says they are one stone (flag). Do **not** link it with the Pānāheḍā record, which also bears V.S. 1116 [C06-CII-022 (T1); C06-PARTEMPLES-008 (T5)]: same year, different place.
     - E: C06-JAGTA-EN-011 (T8), C06-JAGTA-HI-043 (T8) · C: C06-JAGTA-HI-011 (T8), C06-INTACH-001 (T7) · X: C06-MADHYABHARAT-001 (T5) · Note: C01-GANGULY-020 (T5), C01-CII-014 (T1) (the 1059 date's dependence on a late record; recall only)
  - **Evidence pass (C, optional by default; P0):** C06-GANGULY-027 (T5) — Ganguly: two short inscriptions in the temple, one dated Sam. 1137
- **Drafting guidance:**
  - Narrate closely in P1: it is the opening object. Mahipāla and Śṛṅgavāsa are introduced here, once, with full names; thereafter "Mahipāla".
  - Verma's readings: name Verma only in the note ("as read by S. K. Verma, reported by Tiwari").
  - Do not use Tiwari's "byline"/newspaper analogy [C06-JAGTA-EN-005 (T8)] or "as if out of a printer" [C06-JAGTA-EN-033 (T8)]: these are modern similes, not evidence.
  - Never give 30 March 1080 in the text; the conversion is Verma's.
  - Amērā: give "-pāla" exactly; do **not** suggest any identification with Mahipāla (see Flags).
- **Transition:** These are short texts by men who sign their work. Udaypur also held a long text whose maker is lost: the king's poem of his ancestors.

---

## 6.2 A poem of descent *(the Udaypur praśasti read as composition and claim · ~900 w)*

**Word target:** 900

- **Section statement:** By the end, the reader knows how the *praśasti* works as a poem. It is Sanskrit verse throughout after one obeisance, it opens with benedictions to Śiva, and it builds each ancestor out of images and puns. It makes learning a royal virtue, rising to "Bhoja the poet-king" and to Udayāditya as "another sun". The reader also knows what its editors credit and doubt, and why it is set at Udaypur. Who composed it is not known.
- **Purpose:** Do the work 1.4 deferred: read the text's language, metre and rhetoric. Show that its value for intellectual history lies in what it *claims* about kingship and learning, not in the events it lists (Ch 4).
- **Paragraph plan:**
  1. **P1 — Form.** **Point:** Establish the text's physical and literary form from CII, recalling the two slabs in a clause (1.4). The language is Sanskrit. Apart from a short opening obeisance to Śiva, the whole is metrical. Twenty-two unnumbered verses survive on the first slab, and the inscription breaks off ten syllables into the next. The second slab's 27 lines are largely obliterated. The script is eleventh-century Nāgarī, sharing a hooked head-stroke with other records of the time. The record is undated and its purpose is lost; the editor takes it as a *praśasti* "intended to be put in a part of the temple", which is where such poems were usually set.
     - E: C06-CII-008 (T1), C06-CII-009 (T1), C06-CII-007 (T1) · C: C06-JAGTA-HI-014 (T8), C06-CII-066 (T1), C06-CII-024 (T1) · X: C06-JAGTA-EN-014 (T8), C06-JAGTA-HI-029 (T8)
  2. **P2 — Benediction and image.** **Point:** Show how the poem speaks. Its opening verses ask Śiva's blessing through images: the crescent like a wish-granting creeper; the serpent garland wet with Gaṅgā water; Nandī drumming, Nārada singing and *apsaras*es dancing before him. Its kings are built from figures. Vākpati I is "a sun for the water-lilies, the eyes of the maidens of Avanti". Vairisiṃha "indicated" Dhārā with the *edge* of his sword, a pun on *dhārā*, edge. Udayāditya is "another sun" whose sword-rays scatter the darkness of his foes. Quote one image only (the Avanti water-lilies or the "another sun"). The theology of the benedictions belongs to Ch 8: one sentence here.
     - E: C06-JAGTA-EN-017 (T8), C06-JAGTA-HI-016 (T8), C06-GANGULY-006 (T5), C06-GANGULY-007 (T5), C06-PANDE-001 (T5) · C: C06-JAGTA-HI-015 (T8), C06-GANGULY-020 (T5) · X: C06-RAJABHOJ-EN-002 (T9)
  3. **P3 — Learning as a royal virtue.** **Point:** The poem's own picture of intellectual life. It credits Vākpati with eloquence, lofty poetry, reasoning and command of the *śāstra*s. It gives Bhoja the title *kavirāja*, "king of poets", in a verse whose translation runs "he achieved, he gave, he knew". It sets beside that a single verse of conquests won "by his mercenaries alone", and a list of temples covering the world. The dynasty presents itself as warriors who are also poets and scholars. This is the earliest *Udaypur* evidence for the Bhoja of learning, and it is a claim in a eulogy. Do not list the conquests as events (Ch 4); cite the catalogue as rhetoric.
     - E: C06-GANGULY-025 (T5), C06-BHOJA-TIMES-025 (T5), C06-BHOJA-TIMES-022 (T5), C06-BHOJA-TIMES-031 (T5) · C: C06-GANGULY-026 (T5), C06-BHOJA-TIMES-029 (T5), C06-PARTEMPLES-004 (T5) · X: C04-JAGTA-EN-021 (T8), C06-BHOJA-TIMES-023 (T5)
  4. **P4 — Whose poem?** **Point:** Its composer is unknown: the closing lines that would name him are lost or illegible, and no item names him. Tiwari's statement that Udayāditya "had it prepared" is a reasonable inference from its content, not a reading. Set it beside the family's other long poem of descent, the Nagpur *praśasti*. That is 58 verses in the ornate *gauḍī* style, rich in figures, and composed, by its own verse 55, by King Naravarman himself. Kielhorn found its style "highly bombastic and artificial", and its editor judges its historical content slight. Adhikari judges the Udaypur poem's style a mark of the age's high literary standard. Point to draw: such poems were the work of court poets and, at least once, of a king. The Udaypur poem belongs to that court culture, wherever its author sat.
     - E: C06-CII-071 (T1), C06-CII-072 (T1), C06-GANGULY-022 (T5) · C: C06-PARTEMPLES-001 (T5), C06-GANGULY-056 (T5), C06-CII-015 (T1), C04-JAGTA-HI-027 (T8) · Note: C06-JAGTA-HI-012 (T8), C06-JAGTA-EN-012 (T8) (Tiwari's attribution to Udayāditya); C06-CII-084 (T1), C06-CII-079 (T1) (other Paramāra *praśasti*s that do name composer, scribe and engraver: what the Udaypur text lacks)
  5. **P5 — Reading it as a claim, and why here.** **Point:** What the editors credit and doubt. The CII editor uses it as the one complete genealogy, but suspects two names with no deeds attached may be a scribal repetition. He notes that it is the first inscription to tell the cow-and-fire-altar legend; that detail was told in 1.4, so recall it, do not retell. Vaidya preferred the dynasty's official grants to this "much later" poem; Ganguly answers him from Padmagupta (one note). The temple list shows how convention shapes content. Ganguly placed all those temples in Malwa. Trivedi read the first three as the famous shrines of north, south and west and supposed the fourth was in the east: a conquest of the quarters in architecture. The poem therefore tells what the dynasty wished to be. The book's inference, graded "it may be no accident": the fullest account the house gave of itself stood at a frontier town that bore its king's name. Close on the limit: the second slab, where Udaypur itself would have entered, is mostly gone. Its building claim is homed in Ch 4 [C01-CII-012 (T1)]: recall, do not read.
     - E: C06-CII-007 (T1), C06-CII-002 (T1), C06-CII-021 (T1), C06-PARTEMPLES-002 (T5) · C: C06-BHOJA-TIMES-017 (T5), C06-GANGULY-004 (T5), C06-GANGULY-023 (T5), C06-BHOJA-TIMES-008 (T5), C06-BHOJA-TIMES-012 (T5) · X: C06-CII-020 (T1), C06-CII-022 (T1) · Note: C06-GEOHER-001 (T7) (the survey's statement that the *praśasti* gives 1059 and the lake is not supported by the edition, which finds no date [C06-CII-007 (T1)]); C06-GANGULY-021 (T5), C06-GANGULY-001 (T5) (Ganguly's "early in the reign", "about 1072", recalled from 1.4 only if needed)
  - **Evidence pass (X, optional by default; P0):** C06-GANGULY-017 (T5), C06-CII-005 (T1), C06-BHOJA-TIMES-007 (T5), C06-BHOJA-TIMES-011 (T5), C06-GANGULY-015 (T5) — the praśasti's conquest catalogue and its conventional praise of early kings, as later historians read it; use only to show what the poem claims
- **Drafting guidance:**
  - CII's readings and descriptions outrank Ganguly's; use Ganguly and Mahesh Singh only for verse translations CII does not give, attributed in a note ("as translated by Ganguly").
  - Verse numbers differ between sources (Bhoja's verse is "18", "19" or "20" in different authors): give no verse numbers in the text.
  - Bühler's EI edition is not in the corpus: never cite it as read.
  - Do not quote Mahesh Singh's English verse at length; at most the three-verb phrase.
  - Grade: "the poem claims", "it presents"; never "Bhoja conquered".
- **Transition:** The *praśasti* claims that the dynasty's kings were masters of letters. On a slab in the temple's courtyard wall the same claim is made in another form: a weapon made of the alphabet itself.

---

## 6.3 A serpentine scimitar of letters *(the grammar-serpent as a learned royal object · ~900 w)*

**Word target:** 900

- **Section statement:** By the end, the reader knows that a slab from the courtyard wall carries the whole Sanskrit sound-system and the endings of nouns and verbs, laid out in the body of a serpent shaped as a sword. Its verse calls it a "serpentine scimitar of letters". Identical charts at Ujjain, Dhār and Ūn tie it to Udayāditya and Naravarman in the late eleventh century. Scholars disagree whether such charts taught boys grammar or served as emblems of a king who protected "letters and social order"; at Udaypur the evidence favours the emblem.
- **Purpose:** The chapter's centrepiece: the one Udaypur object in which learning itself is the content. Tie Bhoja-era grammar culture to Udaypur through this object, not through a survey of Bhoja.
- **Paragraph plan:**
  1. **P1 — The diagram.** **Point:** Describe it as SERPENT does, as a text to be read top to bottom. The hood holds the fourteen vowels in short and long pairs. The neck and knotted body hold the semivowels and the five classes of stops, and one leg holds the sibilants. *Ha* stands at both ends of the consonant series, as in Pāṇini's Śiva-sūtras. The base holds three aspirate signs, but not the *anusvāra*. In the tail, triads give 21 noun endings rising and 18 present-tense verb endings, active and middle, falling. Recall in a clause that this is the slab 1.4 mentioned as reset in restoration. The block belonged to the parapet but originally faced into the courtyard.
     - E: C06-SERPENT-003 (T5), C06-SERPENT-002 (T5), C06-SERPENT-004 (T5) · C: C01-KB-SERPENT-001 (T5) · X: C06-GANGULY-043 (T5), C06-BHOJA-TIMES-040 (T5) (the Dhār single-serpent chart has the same 21 and 18 endings; compatible, not to be called identical)
  2. **P2 — The words beside it.** **Point:** The short inscriptions name and empower the diagram. A two-line verse asks that "the protector cause this serpentine sword of letters to protect" (the object of protection is lost). The name *varṇa-nāga-kṛpāṇikā* fuses three things: the alphabet heard, a serpent seen, a sword that acts. The palaeography matches local records of the late eleventh century: inch-high, rectilinear letters whose verticals bend sharply right. The orthography shows the period's habits (*va* for *ba*, *sa* for *śa*, a doubled consonant after *r*).
     - E: C06-SERPENT-005 (T5), C06-SERPENT-006 (T5), C06-SERPENT-004 (T5) · C: C06-SERPENT-002 (T5) · X: C06-CII-015 (T1) (*b* written as *v* in the Nagpur poem too)
  3. **P3 — Four temples, one device.** **Point:** Change scale to the kingdom. An identical diagram at the Mahākāla temple of Ujjain is accompanied by three *anuṣṭubh* stanzas. They dedicate the "alphabetical snake-scimitar" to Udayāditya. They call it the sword of kings Udayāditya and Naravarman, worshippers of Śiva, guarding the *varṇa*s in both senses (classes of society and letters of the alphabet), and a badge "for poets and kings". The verses were composed by "the friend of talented poets", taken to be Naravarman. Related charts stand on two pillars of the Bhojaśālā at Dhār, now the Kamāl Maulā mosque, and at Ūn, where the same verse naming Udayāditya appears. SERPENT places the Udaypur slab with these in the last decade of the eleventh century, perhaps just after Udayāditya's death (1093). Graded: "probably", resting on the identity of the diagrams.
     - E: C06-CII-052 (T1), C06-SERPENT-008 (T5), C06-SERPENT-007 (T5) · C: C06-CII-059 (T1), C06-CII-056 (T1), C06-CII-057 (T1), C06-PARTEMPLES-005 (T5), C04-PARTEMPLES-008 (T5) · X: C06-CII-047 (T1), C06-CII-048 (T1), C06-CII-053 (T1), C06-CII-055 (T1), C06-ARTPAR-002 (T5), C06-GANGULY-038 (T5)
  4. **P4 — Schoolroom or sword?** **Point:** Set out the dispute and take a position. Lele, Trivedi and Ganguly read the charts as teaching aids. For Dhār, the reading rests on the tradition that the mosque was Bhoja's Sanskrit school; for Ūn, the editor infers that the temple was used as a school for young boys. Singh argues the charts were devices of royal power at the kingdom's leading Śiva temples, not tools for schoolboys. The Ujjain verse's pun on *varṇa* (letters and social order) and its "badge for poets and kings" support him. Position, graded: at Udaypur nothing points to a school. The slab is best read as a learned emblem of the king's claim to guard language and order. Whether anyone learned grammar from it is not known. The Dhār school is a tradition about a building (tier 8 for the event), and the Bhojaśālā's conversion belongs to Ch 10.
     - E: C06-SERPENT-009 (T5), C06-CII-068 (T1), C06-CII-070 (T1) · C: C06-CII-069 (T1), C06-GANGULY-041 (T5), C06-GANGULY-042 (T5), C06-BHOJA-TIMES-039 (T5), C06-PARTEMPLES-006 (T5) · X: C06-BHOJA-TIMES-037 (T5), C06-BHOJA-TIMES-043 (T5) · Note: C06-SERPENT-009 (T5) (Singh names Trivedi 1978 and Pollock 2006 as holding the school reading; neither Pollock nor Salomon is in the corpus)
  5. **P5 — The learning it advertises.** **Point:** One framing paragraph, no more than ~180 words. The emblem points to a grammar culture centred on Dhārā. The grammar called *Sarasvatīkaṇṭhābharaṇa* is attributed to Bhoja and named in his Yoga commentary's opening verse. The same name was given to halls of learning at Dhārā and Ujjain. Ganguly and Munshi doubted that Bhoja wrote everything under his name, and the "five hundred poets" of his court is a later tradition. No work attributed to Bhoja mentions Udaypur. What reached Udaypur was the dynasty's emblem of that learning. That Udayāditya grew up among scholars is Tiwari's surmise, not evidence. Bhoja as king and author belongs to Ch 4, and his Śaiva *Tattvaprakāśa* to Ch 8.
     - E: C06-BHOJA-TIMES-059 (T5), C06-YOGASUTRA-002 (T5), C06-YOGASUTRA-003 (T5), C06-GANGULY-055 (T5) · C: C06-BHOJA-TIMES-046 (T5), C06-BHOJDEV-HI-020 (T9), C06-RAJABHOJ-EN-004 (T9), C06-BHOJA-TIMES-057 (T5) · X: C06-GANGULY-054 (T5), C06-BHOJDEV-HI-008 (T9), C06-SAMAR-1-001 (T4), C06-SAMAR-1-002 (T4) · Note: C06-JAGTA-EN-036 (T8) (Tiwari's surmise)
- **Drafting guidance:**
  - SERPENT is by A. Singh: give "Singh" in notes only.
  - Explain *sarpabandha/nāgabandha* once.
  - Do not adopt SERPENT's "temple and tank … founded and named after king Udayāditya in 1080" [C06-SERPENT-009 (T5)]: canon holds 1080 as the dated record, with the founding question open (1.4, Ch 4).
  - Keep P5 to one paragraph; no list of Bhoja's works beyond the grammar and the Yoga commentary.
  - SAMAR items: never quote; mention only as "attributed, doubtfully".
- **Transition:** The serpent and the *praśasti* belong to the founding generation and its court. Most of what the porches hold was written later, by officials, governors and visitors, and in plainer words.

---

## 6.4 The porch archive *(grants, governors and pilgrims, 1163–1639 · ~800 w)*

**Word target:** 800

- **Section statement:** By the end, the reader knows that the pillars and seats of the three porches hold a long series of records: a dozen or so of historical weight and many pilgrims' notes. They are listed in reports far more fully than they are published. Read as texts, the edited ones show the register falling from court verse to working prose: a governor's and a prince's gifts, a treasury officer's four *biswa* of land, a king given imperial titles that his other records do not give, the town under more than one name, and at last visitors writing in Nāgarī and their own speech.
- **Purpose:** Turn from the founding generation to the centuries. Show what kind of writing the porches hold and what it records about authority and patronage, without retelling the politics (1.3, Ch 10) or the economy of gifts (Ch 8).
- **Paragraph plan:**
  1. **P1 — An archive known from lists.** **Point:** The porches' pillars and seats carry numerous Sanskrit inscriptions: some historical, others pilgrims' records, which show worship continuing. Almost all were copied into the Gwalior State reports (1923–29) and the ASI epigraphy reports (1961–83). Only a selection has been published. Counts in the sources range from eleven or a dozen to "around a hundred" or "more than a hundred". They count different things (one series, the doorways, everything traced on the site), so give the range in a note and no single figure in the text.
     - E: C06-MADHYABHARAT-003 (T5), C06-GAZ-003 (T7), C06-SERPENT-001 (T5) · C: C06-ARTPAR-001 (T5), C06-JAGTA-EN-021 (T8) · Note: C06-JAGTA-EN-025 (T8), C06-JAGTA-EN-028 (T8), C06-JAGTA-EN-031 (T8), C06-JAGTA-EN-026 (T8) (the count conflict, quoting the map's table)
  2. **P2 — Records of possession, 1160s–1170s.** **Point:** In the twelfth century the porch registers whoever held the town. Ganguly's list has a record of the Caulukya Kumārapāla at Udayapur, 1163, and Adhikari cites a V.S. 1220 inscription naming Kumārapāla's governor Rājyapāla. These two are probably one record, but no item says so. Within a decade Lūṇapasāka's grant to the god Vaidyanātha names Bhṛṅgārikā as a *pathaka*. Recall both in clauses (1.2, 1.3); the point here is that rival powers wrote their claims on the same stones.
     - E: C06-GANGULY-034 (T5), C06-CII-038 (T1) · C: C10-PARTEMPLES-001 (T5) (home Ch 10: cross-reference), C06-RAJABHOJ-EN-003 (T9) · Note: C06-RAJABHOJ-EN-003 (T9), C06-CII-038 (T1), C06-GAZ-001 (T7) (Lūṇapasāka 1171/1172/1173, as a range "early 1170s" (canon); the Gazetteer wrongly gives the record to Udayāditya)
  3. **P3 — A treasury officer's gift, 1229.** **Point:** Read the V.S. 1286 record as a working text. It is fourteen lines on a pillar right of the east door, in Sanskrit and mostly prose, in thirteenth-century Nāgarī whose letters are "quite crude". It opens with *siddham*, gives the year in numerals, and is set "before the god Udayeśvara". Its subject is a gift of four *biswa* of land, with water poured, by Dhāmadeva, an official of the treasury, "in the victorious reign" of Devapāla. Name the officer's office as Verma reads it (*pañcakula*; *mahāmudrā*), with a note. Contrast it with the founding generation's verse: this is the language of administration. The gift's meaning belongs to Ch 8: one clause.
     - E: C06-CII-037 (T1), C06-JAGTA-HI-032 (T8), C06-JAGTA-HI-033 (T8), C06-JAGTA-EN-035 (T8) · C: C06-JAGTA-HI-034 (T8), C06-JAGTA-EN-029 (T8), C08-CII-020 (T1), C08-JAGTA-HI-013 (T8), C08-JAGTA-HI-014 (T8) · X: C06-CII-036 (T1), C06-GANGULY-028 (T5) · Note: C08-JAGTA-EN-012 (T8) (Verma on *pañcakula*)
  4. **P4 — Titles and names, 1232.** **Point:** The second Devapāla record, three years later, gives land in villages: Kharahi, Umarata, a place in Bhṛṅgārikā-64, and Devadharmapurī, which the editor takes, "if the reading is correct", to be Udaypur itself. Elsewhere the editor reads Pañcamukha-pattana as the town named after the Śiva temple, "one place with two names". The record gives Devapāla *Paramabhaṭṭāraka* and *Mahārājādhirāja*. The editor calls it the only epigraphic claim to imperial titles for him, since his other records style him *Mahāraja* or *Mahākumāra*. Its unit figure was altered by the scribe himself. Point: even a grant is a claim, and the town was written under more than one name. Devapāla's residence is told (1.3); do not retell it.
     - E: C06-CII-040 (T1), C06-CII-039 (T1), C06-CII-082 (T1), C06-CII-043 (T1) · C: C06-CII-041 (T1), C06-CII-042 (T1), C06-CII-033 (T1), C06-GANGULY-029 (T5) · X: C06-CII-034 (T1), C06-CII-035 (T1)
  5. **P5 — Later rulers, lost stones, and pilgrims.** **Point:** After 1232 the royal record thins. A V.S. 1311 record "from Udaipur" was lost before it could be edited (Kielhorn read the name Jayasiṃha in it, "with but little doubt"). Ganguly lists an inscription inside the east entrance naming Mahārājādhirāja Jayasiṃha ruling in Sam. 1366 (1309), known from his handlist only. The register then becomes the visitors'. In V.S. 1696 pilgrims from Ranthambhor left notes in Nāgarī and the local dialect. One names Turasadasa and the mason Suvi (recall, 1.4). Another is read as Ustonatha's, "written by him". Inscriptions on the hillock record pilgrims from Rajasthan. Point: by the seventeenth century the stones carry the speech of their visitors, cut by a mason or written by the pilgrim himself.
     - E: C06-CII-044 (T1), C06-GANGULY-032 (T5), C06-GEOHER-007 (T7), C06-GEOHER-008 (T7) · C: C06-GANGULY-030 (T5), C06-GANGULY-031 (T5), C06-GANGULY-037 (T5), C06-GEOHER-003 (T7) · X: C06-GEOHER-002 (T7) · Note: C06-GEOHER-006 (T7) (the survey's "almost 500 years ago" does not fit V.S. 1696); C06-CII-044 (T1) (the footnote does not say which Udaipur)
  - **Evidence pass (C, optional by default; P0):** C06-GANGULY-036 (T5), C06-GANGULY-035 (T5) — Ganguly's handlist rows (the 1229 record, *IA* XX; an Udayapur inscription in *EI* I p. 214): how the porch archive is known, from lists
- **Drafting guidance:**
  - Compress P2 hard: it exists to show rival hands on one surface, not to narrate 1160–1173.
  - "Dhāmadeva": use this form; JAGTA's "Dhamdev" and CII's "Dhāmadēya" go in a note.
  - The 1309 record: "Ganguly lists", never "an inscription records", since no edition is in the corpus.
  - Ustonatha and Turasadasa: present as two readings or two records, as the survey has them; do not merge.
  - Pilgrims: no motives, journeys or feelings; only names, places, dates, language.
- **Transition:** One script and one sacred language had served every record so far. In the fourteenth century a new language of authority arrived on the same ground.

---

## 6.5 New languages of authority, and the limits of the stones *(Persian inscriptions, 1336–1632; what the archive cannot say · ~650 w)*

**Word target:** 650

- **Section statement:** By the end, the reader knows that Persian came to Udaypur's stones as the language of a new order's building records: under Muhammad bin Tughluq in A.H. 737–39 (1336–38), in a bilingual Persian-and-Sanskrit record of 1488, and in the Shahi Masjid record of 1632. These texts establish who built and in whose reign; they do not establish who damaged what. The reader also knows how much of the whole archive remains unread or unpublished, and so what the chapter's conclusions cannot reach.
- **Purpose:** Decide what Ch 6 says about the Persian inscriptions *as texts*: their language, who they name, what they can and cannot carry. Leave the buildings (Ch 7) and the politics (Ch 10) to their chapters. End on the limits of the evidence.
- **Paragraph plan:**
  1. **P1 — A sultan's name on the temple's stones.** **Point:** The two Persian inscriptions of the mosque built against the temple's rear are dated A.H. 737–39 (1336–38) and name Muhammad bin Tughluq. They stand in doorways put together from the temple's own broken pieces. Recall the building in a clause (1.3). As texts they are building records in a language not used on these stones before. In Tiwari's account the name was read for Dr Mishra by an unnamed reader. No edited text is in the corpus. What they establish: construction in that sultan's reign. What they do not: who broke the shrines, and when. Tiwari concedes as much: "it is not proved, from an inscription alone".
     - E: C06-JAGTA-HI-019 (T8), C07-PANDE-006 (T5) · C: C10-MADHYABHARAT-006 (T5) (home Ch 10: cross-reference), C06-JAGTA-EN-020 (T8), C06-JAGTA-EN-024 (T8), C06-JAGTA-HI-027 (T8) · Note: C06-JAGTA-EN-037 (T8) (Tiwari's legal caveat); C06-JAGTA-HI-019 (T8) (Tiwari's "Arabic or Persian": the only source to allow Arabic)
  2. **P2 — Two languages on one wall, then one.** **Point:** The mosque outside the eastern gate bears Persian *and* Sanskrit inscriptions recording its building by an agent of Sher Khan under Ghiyas Shah Khalji of Mandu, A.H. 894 (1488). It is the one Udaypur record in the corpus that sets the two languages side by side, matching Tiwari's report of inscriptions where Sanskrit and Persian "stand together". The Shahi Masjid's Persian inscription records work begun under Jahangir and finished under Shah Jahan, A.H. 1041 (1632). Graded point: by the fifteenth to seventeenth centuries Persian had become the language in which the new order recorded its building, while Sanskrit could still stand beside it. The Persian *farman* in Hindi translation is a document, not an inscription, and goes to Chs 10–11.
     - E: C06-JAGTA-EN-031 (T8) · C: C07-MADHYABHARAT-012 (T5), C07-MADHYABHARAT-011 (T5) (primary home 7.4; cited here only for the inscriptions' languages and dates, and they carry the claim over Tiwari's T8 item), C07-GAZ-005 (T7), C06-JAGTA-HI-035 (T8) · X: C06-JAGTA-HI-023 (T8)
  3. **P3 — What the stones cannot say.** **Point:** Close on the limits. Much of the archive is unread or unpublished. Translations made long ago lie in the ASI's files, and Upadhyay notes a famine of epigraph readers in the state. Inscriptions on the hill remain undeciphered: one on the great Śiva image, the lines beside a sculpture that INTACH first noticed, and a cave record in tenth- to eleventh-century Sanskrit. None of these is to be identified with the tentatively read eighth-century two-line record (1.5). One door frame holds an eight-line Sanskrit inscription beside an empty frame of the same size, either never written or scraped. Then state the conclusions plainly. The inscriptions establish names, dates, gifts, titles and claims. They do not establish a school at Udaypur, a court of poets there, who read these texts, or who composed the *praśasti*. End on the Persian-inscribed mosques and gates standing outside the temple wall: the content that carries the reader into Chapter 7.
     - E: C06-SERPENT-001 (T5), C06-JAGTA-EN-002 (T8), C13-JAGTA-HI-027 (T8), C06-JAGTA-EN-019 (T8) · C: C06-GEOHER-004 (T7), C06-INTACH-002 (T7), C06-GEOHER-009 (T7) · X: C06-JAGTA-HI-036 (T8), C06-GEOHER-005 (T7)
- **Drafting guidance:**
  - Use "Muslim" in the narrator's voice; quote "Mohammedan" only inside a quotation.
  - Do **not** use C06-JAGTA-HI-020 (T8): a first-person narration in which the temple's goddess speaks. It is fiction, not testimony, and it contains invented speech.
  - Do not use C06-JAGTA-EN-023 (T8) ("hangs … like a threat"): an image, not evidence.
  - The 1488 mosque's location "outside the eastern gate, Moti Darwaza" is canon from 1.3; the old canon's "do not import Mandu's Moti Darwaza" note conflicts with it (brief §1.3). Ch 6 follows 1.3.
  - No "four languages": say Sanskrit, Persian and the local Hindi speech in Nāgarī. Arabic only as Tiwari's uncertainty, in the note.
- **Transition (out of the chapter):** see §4.

---

## Chapter 6: conflicts to present, unresolved

| Conflict | Where | How held |
|---|---|---|
| The praśasti: location, date (undated in CII; "about 1072" Ganguly; 1059 survey), reliability | **6.2 (home)** | "The undated praśasti"; the editors' credit and doubt in P5; variants in a note |
| Verse numbering of the praśasti | 6.2 | Give none |
| The V.S. 1116 text vs Ganguly's "1513" record vs CII's V.S. 1562 pedigree | 6.1 P5 | Three records not identified with one another; the date question stays with 4.4 |
| Lūṇapasāka 1172 (Ganguly) / 1173 (CII) | **6.4 (home)** | "Early in the 1170s"; both dates in the note |
| Kumārapāla 1163 (C06-GANGULY-034) and V.S. 1220 (C10-PARTEMPLES-001) | 6.4 P2 | Cite both; never merge; the political reading is 10.1's |
| Turasadasa and Ustonatha, same place and date | 6.4 P5 | Kept apart |
| Inscription count | **6.4 P1 / 6.5 P3 (home)** | What is edited, listed or only reported; no Tiwari totals |
| "Arabic" (one "Arabic or Persian") | 6.5 | Not stated as a language of the stones |
| "In the fort (*gaḍh*)" vs the pillar by the east door | 6.4 | Probable misreading of *gadya*; check the page image |
| SERPENT line counts ("5 lines" / "two lines") | 6.3 | "Short inscriptions, one a two-line verse" |
| Chhittapa's date (Gazetteer "V.S. 935 (A.D. 992)" vs CII "Date lost?") | 6.1 P3 | No date |

## Chapter 6: hand-offs

- **In:** Chapter 5 ends inside the Udayeśvara (confirmed at merge: Chapter 5 ends at the east doorway). Chapter 6 opens at the east door, on the six lines of V.S. 1137 to its right: - the wish that Udayāditya make the earth "one umbrella"; - the statement that Udayeśvara's flag-hoisting "is complete"; - the name of the verse's maker, Paṇḍita Mahipāla, son of Paṇḍita Śṛṅgavāsa [C06-CII-006; C06-JAGTA-HI-008; C06-JAGTA-HI-009].
- **Out:** The last paragraph ends on the mosques and gates that carry the Persian inscriptions: the mosque built against the temple's rear, the bilingual mosque outside the eastern gate, the Shahi Masjid to the east. These are buildings with dates but not yet descriptions, which is Chapter 7's ground. It must not announce Chapter 7, summarise Chapter 6, describe the mosques' architecture, or narrate the Tughluq conquest (Ch 10).

## Chapter 6: changes from the master outline

1. **Evidence pass:** added optional items: C06-GANGULY-027 (two short inscriptions in the temple, one of 1080) to 6.1; C06-GANGULY-036 (Ganguly's handlist row for the 1229 record) to 6.4; Ganguly's and Mahesh Singh's catalogue of the praśasti's conquest claims to 6.2, as evidence of what the poem asserts, never as events.
2. **Locator corrected at merge:** C06-CII-007 is p. 131.
3. No structural change.

## Chapter 6: research and verification flags

- Old-canon porch dates are absent from every map.
- The old canon's "1310" record
- The gap "No edited text in the corpus" is now only partly true.
- "-pāla" at Amērā and Mahipāla.
- "In the fort (*gaḍh*)"
- The V.S. 1116 text
- Adhikari
- SERPENT's "temple and tank … founded … in 1080"
- SERPENT line counts.
- Chhittapa's date.
- Conflicts from the map's §5:
- Kumārapāla, 1163
- "Arabic"
- Turasadasa and Ustonatha
- Verse numbers of the *praśasti
- Graded wording:
- **Page-image checks:** C06-JAGTA-EN-035 (gaḍh/gadya); C06-GANGULY-032 (V.S. 1366; OCR "1909").
- **Staged sources (leads, `ocr_verify`):** Bühler, *EI* I (the praśasti text; needs a Sanskrit reader); Cunningham, ASR X; the Gwalior reports (1923–24, 1925–26, 1928–29; "V.S. 1974"). Not evidence until hand-corrected and ingested.
- **ASR IX p. 109 (lead):** a V.S. 1137 record of Udayāditya, provenance unstated. Reconcile with CII's citation before 6.1 cites the 1080 record's publication history.

---

# Chapter 7. The Wider Built Heritage of Udaypur: Fortifications, Shrines, Mosques and Water Structures

**Planned words:** 4,250 (7.1: 1050 · 7.2: 750 · 7.3: 700 · 7.4: 800 · 7.5: 950). **Evidence:** `evidence_index/ch07.jsonl`.

**Historical question.** What do Udaypur's buildings other than the great temple (the wall on the hill, the town's gates and palace, the lesser shrines, the mosques and tombs, the tanks and stepwells) record about who held the town, when, and for what, and how much of that can actually be dated?

**Through-line.** By the end, the reader knows that Udaypur's buildings beyond the temple record a long sequence of holders (a fortified hill no record names, a palace enclosure used for centuries, shrines built after Udayāditya, mosques dated 1336–38, 1488 and 1632, and water works of several ages), but that only the mosques and one tank carry dates of their own, so most of the town's built history is an order of layers, not a calendar.

**Arc.** **Opening → close.**
- 7.1 starts on the highest and least documented work, the wall on the hill: its fabric, its gate and bastions, what lies inside it, and why no one can yet date it, ending on the lichen proposal.
- 7.2 comes down to the walled town: its gates, the palace enclosure and the stone houses, a fabric used and rebuilt by successive holders.
- 7.3 turns to the shrines other than Udayeśvara, which show building for Śiva, the Sun, Rāma and the Jinas continuing long after the eleventh century.
- 7.4 reads the mosques and tombs as the only dated sequence in the town: the temple court (1336–38), the eastern gate (1488), the governor's quarter (1632), and the undated dargahs and graves on the hill.
- 7.5 ends on water: the hill's reservoirs and stepwells, the town's stepwells, the tanks, and the one Paramāra-period tank whose purpose a contemporary record states.

**Scope.** *Chronological:* from the undated wall on the hill (the survey proposes the tenth century) to the Shahi Masjid (A.H. 1041 = 1632) and the later shrines and stepwells (16th–18th c. proposals); the hill's rock panels as proposed earlier layers (7.1 P3a). *Geographical:* the hill south of the town (with its middle and upper levels), the walled town and its gates, the temple court only where the mosque stands, the tanks and stepwells, and Amērā about 3 km south. Measurements come from the survey only, once each.

**Editor's merge rulings carried into this plan** (from the master outline):
> **Editor's merge rulings for Chapter 7** (these override the entry below where they differ)
> - **Added at merge: 7.1 P3a, "Images on the rock, and a colossus left lying".** Both parallel drafts sent the hill's sculpture to the other chapter, so it had no home. Chapter 7 is now its home. 7.1's target rises to ~1,050 words; if that is too long, see Part I, I.7.
> - **The entry's §"Cross-chapter notes" line is superseded where it sends the hill's sculpture to Chapter 5.** C07-GEOHER-023, -029, C07-INTACH-005 (the cave and the Tīrthaṅkaras), C07-MADHYABHARAT-005 and C07-GAZ-009 (Ravan Tol and the Seven Mothers), and the rock-temple items C07-JAGTA-EN-006, -010 and C07-JAGTA-HI-019 to -022 now serve 7.1 P3a. C07-PANDE-004 (the archways of the converted rear, the Garuḍāsana Viṣṇu) stays with Chapter 5.
> - **Opening** on the colonial observer's nameless wall: confirmed. It follows Chapter 6's last paragraph (the inscribed mosques) by contrast.
> - **Moti Darwaza:** the 1488 mosque stays at Udaypur (Part I, C1-E). No stepwell is attributed to Sher Khan.
> - **Udayasamudra:** home here (7.5). Treating the Udaysagar as the Udayasamudra stays a proposal.
> - **Palace founder:** 7.2 gives the fabric only, with "its builder is disputed" and no note. The farman is 10.4's.
> - **Last paragraph:** Vikrama's tank and its stated uses. Chapter 8 opens on a gift of land (I.5).
> - **Length:** ~4,250 words planned.

## 7.1 A wall without a name *(the fortified hill and its carvings · ~1,050 w; raised from ~900 for P3a)*

**Word target:** 1050

- **Section statement:** By the end, the reader knows what the wall on the hill south of the town is (a dry-stone sandstone wall of about 1,400 m with bastions, a main gate and a rear gate, enclosing about 56 acres on the north, east and west), what lay inside it on the middle and upper levels, and why its date is open: the survey proposes both "before Udayāditya" and "in his time", its list assigns it to the tenth century, no record names it, and a study of the lichens on its stones has been proposed but not made.
- **Purpose:** Give the fabric once, from the survey, in a single set of figures; turn the old canon's "the fort predates Udayāditya" into the open question it is; place the lichen proposal (moved from Ch 2) where it belongs, as one possible route to a date.
- **Paragraph plan:**
  1. **P1 — The unnamed wall.** **Point:** Establish the object and its silence: a wall of huge uncemented stones with several gates, partly enclosing the hill south of the town, found deserted, nameless and unexplained by the townspeople when a colonial observer saw it; the 1979 Gazetteer took its traces, running about 1 km south to a rocky hill, as evidence that Udaypur is an ancient place; Patil saw the town's own fortifications continue south to join a hill whose top was also fortified. On that reading the hill's defences and the town's wall were parts of one system. Recall 1.5's "uncemented wall" in a clause, without re-arguing the older-place case.
     - E: C07-GEOHER-002 (T7), C07-MADHYABHARAT-003 (T5) · C: C07-GAZ-001 (T7) · X: C07-JAGTA-EN-001 (T8) · Note: C07-GEOHER-002 (T7), C07-GEOHER-003 (T7), C07-GEOHER-010 (T7) (how much of the hill the wall encloses: "only a portion, in the form of a circular sector" in the colonial account; "from all side" and "three sides, North, East, and West" in the survey)
  2. **P2 — Fabric: one set of figures.** **Point:** Describe the wall as built: red sandstone of the hill itself, laid dry as rubble masonry, a dressed outer face with smaller stones packed into the core, no binder; about 1,400 m long, divided by the entry gate (at about 463 m above sea level) into a western run of about 810 m and an eastern of about 600 m; height about 4.3–5.2 m; seven circular and four rectangular bastions, some in three storeys with coping blocks clamped with iron, and loopholes; a broad-topped rampart walk; a small rear gate on the western edge with a 2.3 m sandstone lintel on two posts; the south side, too steep to climb, left unwalled; enclosed area about 56 acres. One clause of context: the survey classes the work as a *giri-durga*, the hill fort of the Indian typology of forts. Give no wall thickness (see guidance).
     - E: C07-GEOHER-010 (T7), C07-GEOHER-011 (T7), C07-GEOHER-012 (T7), C07-GEOHER-013 (T7), C07-GEOHER-014 (T7), C07-GEOHER-015 (T7), C07-GEOHER-009 (T7) · C: C07-GEOHER-006 (T7), C02-GEOHER-030 (T7), C07-GEOHER-003 (T7), C07-INTACH-002 (T7) · X: C07-GEOHER-008 (T7) · Note: C07-GEOHER-009 (T7), C07-GEOHER-004 (T7) (area: 56 acres, from a perimeter of 1,788 m and 226,593 sq m, against a "169-acre complex")
  3. **P3 — What the wall enclosed.** **Point:** The wall guarded a lived-in hill, not an empty refuge. On the middle level (about 520 m): remnants of an inner boundary wall with bastion-like formations, a possible second fortification level, stone cells with traces of lime mortar laid out around a central reservoir (read by the survey as a planned habitation), carved temple fragments, and mounds of collapsed structures along the old path to the top. On the upper level (about 567 m): broken pieces of a Śiva temple with its *liṅga*, a man-made reservoir, and a lime-plastered chamber with pillars that the survey reads as a water structure and villagers remember as a prison. The water works are described in 7.5; here they establish only that people lived and worshipped inside the wall. The later Muslim graves and shrines on the hill belong to 7.4.
     - E: C07-GEOHER-019 (T7), C07-GEOHER-053 (T7), C07-GEOHER-054 (T7), C07-GEOHER-030 (T7), C07-GEOHER-025 (T7), C07-GEOHER-036 (T7) · C: C07-GEOHER-016 (T7), C07-GEOHER-026 (T7), C07-GEOHER-027 (T7) · X: C02-GEOHER-029 (T7) (recall only: 2.4 used it)
  3a. **P3a — Images on the rock, and a colossus left lying** *(added by the editor at merge: the hill's sculpture had no home, because the Ch 5 draft sent it to Ch 7 and the Ch 7 draft sent it to Ch 5. **Ruling: Chapter 7 is its home**, as part of the hill.)* **Point:** The hill was carved as well as walled, and at more than one time.
     - **The rock panels.** On the east face of the middle hill a Navagraha panel is cut into the sandstone, about 1.8 × 0.7 m, some 3 m above the platform's base; the survey judges it pre-Paramāra. Beside it, on the same east-facing rock, is a Saptamātṛkā panel in two parts: the Mothers are seated, not standing as elsewhere, with Gaṇeśa at either end. The survey assigns both panels to the sixth century by comparison with Pathari and Udayagiri. That is a proposal; it also offers "9th-century" for the rock site. Chapter 3 has already used the Mothers panel, so recall it in a clause and add only the Navagraha and the seated posture.
     - **Lajja Gaurī.** Also on the east side of the middle hill is a petroglyph of a seated woman, about 60 × 55 cm, read as Lajja Gaurī. The survey calls it unique because it has a head.
     - **Images on the slopes and in the cave.** The hill's rock surfaces also carry Śiva, Lakṣmī, Bhairava and Gaṇeśa, and Tīrthaṅkara figures in two places. Chapter 3 told the cave with its seated Tīrthaṅkara (sixth century, on the survey's dating): recall in a clause. Near the wall, a Śeṣaśāyī Viṣṇu and a door panel centred on Lakulīśa were found and moved to the site museum in the village. On the lower hill lie a decorated red sandstone pillar, a massive capital of red sandstone and an eleven-petalled *āmalaka* from some large temple. No item ties them to Udayeśvara (compatibility is not identity).
     - **The colossus.** On a boulder near the fort lies a huge unfinished image, a Śiva in the older accounts and a dancing Naṭarāja in the survey, lying on its back. Locally it is called Ravan Tol. The 1979 Gazetteer and Patil describe it together with the Mothers panel "in the side of an adjoining hill" shaped like a stūpa.
     - **Why it was left.** Two readings are on record, both proposals: the survey's, that the project was abandoned under attack by neighbouring rulers, and "the common belief" that the Paramāras' sudden decline stopped it. Who began it, and when, is unknown. Tiwari's rock-temple idea (a hill cut "on the model of Ellora", a liṅga-shaped piece cut from the rock, a later Paramāra king wishing to outdo Udayāditya, "possibly an episode of the later period of the Paramaras") goes in a note as memory and opinion.
     - E: C05-GEOHER-012 (T7), C05-GEOHER-009 (T7), C05-GEOHER-008 (T7), C05-GEOHER-016 (T7), C07-GEOHER-023 (T7), C05-GEOHER-013 (T7), C05-GEOHER-014 (T7), C05-GEOHER-002 (T7), C05-GEOHER-003 (T7), C07-MADHYABHARAT-005 (T5), C07-GAZ-009 (T7), C05-GEOHER-015 (T7), C05-GEOHER-004 (T7) · C: C05-GEOHER-011 (T7) (sixth-century proposal), C05-GEOHER-017 (T7) (the head), C05-GEOHER-005 (T7) ("Ravan Tol" as the local name), C07-GEOHER-029 (T7) (Tīrthaṅkaras at two places), C07-INTACH-005 (T7) (the cave, sixth century; Forest Department ownership) · Note: C05-GEOHER-006 (T7) (the "9th-century" alternative), C07-JAGTA-EN-006 (T8), C07-JAGTA-EN-010 (T8), C05-JAGTA-EN-003 (T8), C07-JAGTA-HI-019 (T8), C07-JAGTA-HI-020 (T8), C07-JAGTA-HI-021 (T8), C04-JAGTA-EN-065 (T8), C04-JAGTA-EN-066 (T8) (Tiwari's rock-temple reading), C05-INTACH-002 (T7) (INTACH's impossible "82 meters in length and 42 meters in width")
     - **Guidance:**
       - **Give no dimension for the colossus.** INTACH's figure (C05-INTACH-002 (T7)) is impossible for a sculpture; the old canon's "8.2 × 4.2 m" has no item (Ch 5 flag 1); Tiwari's "27-foot" is testimony. Its iconography is also unsettled: Śiva in a boulder (Patil, Gazetteer), dancing Naṭarāja (survey). Write "a huge unfinished image of Śiva, which the survey identifies as a dancing Naṭarāja". The old canon's six arms and Apasmāra have no item.
       - **Omit or attribute in a note** the survey's superlatives: "largest … of the medieval era", "anywhere in the world", "probably the largest" Lajja Gaurī, "one of its kind".
       - **Do not link** the colossus to Udayāditya, to Naravarman or to the Udayeśvara's workshop. The "interrupted programme" is a question, not a narrative.
       - **Keep apart** the cave's "two-line inscription" (C07-GEOHER-023 (T7)) and the hill's tentatively read two-line inscription of 1.5 (C01-KB-GEOHER-013 (T7)): no item says they are one.
       - **Keep the panels' dates as proposals:** the panels are proposed as pre-Paramāra, and the colossus is attributed to the Paramāras only by belief and survey reading. The paragraph says only that the hill was carved more than once.
     - **Classification:** objects documented (survey, Gazetteer, Patil); dates: proposals; the abandonment and its cause: interpretation and belief; patron: gap.
  4. **P4 — Before Udayāditya, or his?** **Point:** Weigh the dating. The survey offers two readings in one sentence (a fort that existed before Udayāditya, or a garrison he built on the most defensible hill) and elsewhere calls for research into a dynasty that held the land before the Paramāras; its monument list assigns the wall to the tenth century. Temple fragments fitted into the wall make at least those stretches later than a temple whose stone they reused, but which temple, and when, is not known. The survey's argument from the wars of Paramāras, Caulukyas and Kalacuris is an argument from setting, not evidence of date. Conclude once: the wall may be older than Udayāditya; no item establishes it. The old canon's "the fort predates Udayāditya" is withdrawn.
     - E: C07-GEOHER-003 (T7), C07-GEOHER-022 (T7), C07-GEOHER-061 (T7), C07-GEOHER-007 (T7) · C: C10-GEOHER-001 (T7) (evidence pass: the survey assigns the fort's antiquities to the Paramāra period; a proposal), C07-GEOHER-005 (T7), C07-GAZ-001 (T7) · X: C07-MADHYABHARAT-002 (T5) (forts held the chief and garrison, civilians lived below and were admitted in a siege: a general Madhya Bharat pattern, tier 5) · Note: C07-JAGTA-HI-004 (T8), C07-JAGTA-HI-002 (T8) (Tiwari's "in the time of the Paramāras" and his frontier garrison, as readings), C07-INTACH-026 (T7) (list row garbled to "1956 Century")
  5. **P5 — The lichen proposal.** **Point:** End on the one dating route the survey itself proposes. Lichens grow over the wall and elsewhere on the hill; the survey had them identified with the help of the National Institute of Lichens, observes that lichens take hundreds of years to grow on stone, and suggests that their study "can also help in identifying the age" of the places studied; it asks for systematic study by expert bodies. No such study is reported. Say so once: the wall's date waits on research not yet done. (The lichens' part in the wall's decay is Chapter 11's.)
     - E: C02-GEOHER-024 (T7) · C: C02-GEOHER-025 (T7) · Note: C11-GEOHER-009 (T7) (cross-reference only, for Ch 11)
- **Drafting guidance:**
  - Fabric figures come only from GEOHER and appear once, in P2, as ranges or "about" figures. **No wall thickness:** the old canon replaced the contested thickness figures (the colonial "18 feet", the survey's "almost 5 m", its "4.5–5 m at entrance / 2.5–3 m") with the fabric description. Do not quote the "18 feet" sentence of C07-GEOHER-002 (T7).
  - The old canon's "earthen rampart stone-faced inside" is **not in the evidence**. C07-GEOHER-010 (T7) describes a dressed outer face with a core of smaller stones: describe that.
  - Never adopt the survey's superlatives or rhetoric: "architectural marvel", "maybe the longest one anywhere in Madhya Pradesh", "not been breached even at a single place", "1000 years", "a mystery". "Military cantonment" and "the army was staying inside this fortification" (C07-GEOHER-003 (T7), -005) are the survey's readings: attribute them in a note or omit.
  - *Giri-durga*: one clause, as the survey's classification. The Arthaśāstra and the *Samarāṅgaṇasūtradhāra*'s praise of the hill fort (C07-SAMAR-1-018 (T4)) are normative; they may appear only in a note, paraphrased, never quoted; SAMAR is ⚠ old OCR and its attribution to Bhoja is doubted.
  - Do not use the popular claim that Paramāra bastions were square and that round ones came with cannon (C07-RAJABHOJ-EN-006 (T9), -011) to date Udaypur's mixed bastions: tier 9 and untested (flagged).
  - Graded wording: "may be older than Udayāditya" (possible); "the survey assigns it to the tenth century" (proposed); "no record names it" (said once).
  - Tiwari appears only in the note, as a reading. Do not use his picture of Hindus sheltering behind the rampart (C07-JAGTA-HI-009 (T8)): narrative, unsourced.
- **Transition:** The colonial account and Patil both saw the hill's defences running down to the town's own wall; follow that wall down to the gates through which the town is still entered.

---

## 7.2 Gates, palace and houses *(the walled town · ~750 w)*

**Word target:** 750

- **Section statement:** By the end, the reader knows the town's named gates and what their names record; that the palace enclosure is a building of more than one period (the survey lists it as eleventh-century, compares a temple's style to it to propose the thirteenth, and describes pointed arches and iron joists inside it), and that whether it is the early-Mughal mansion Patil described is not established; and that the town's stone houses reuse older carved stone and show their layers in the walls, but cannot be dated from what has been written about them.
- **Purpose:** Read the town's secular fabric as evidence of continuous use and rebuilding by successive holders, building on 1.1 (walled city, Teen Darwaza, houses pressed against gateways) without re-describing it.
- **Paragraph plan:**
  1. **P1 — Gates named for roads.** **Point:** The town is still entered through gateways that stand around its centre. The survey lists five by name, the Chanderi, Moti Masjid, Purani Basti, Chattuaa (Chatua) and Purana Bazaar *darwāza*s, all still in use and in poor repair, all assigned to the eleventh century (a blanket proposal). The Chanderi Darwaza on the north faces the road to Chanderi: in Madhya Bharat a fort's gates were often named after the towns they faced, so the names record the roads the town looked to rather than the date of the masonry. The eastern gate, Moti Darwaza, is the one outside which a mosque was built in 1488 (7.4); in the survey list the Moti Masjid stands beside the gate that now bears its name. Recall the Teen Darwaza of 1.1 in a clause only.
     - E: C07-INTACH-001 (T7), C07-GEOHER-061 (T7), C07-GEOHER-060 (T7) · C: C07-INTACH-003 (T7), C07-MADHYABHARAT-003 (T5), C07-GEOHER-063 (T7) · X: C07-MADHYABHARAT-001 (T5) · Note: C07-JAGTA-EN-002 (T8) (Tiwari's same explanation of the Chanderi gate's name, as a reading), C07-INTACH-003 (T7) (OCR "Chamber Darwaza" at the Chanderi Darwaza's coordinates; government ownership)
  2. **P2 — The palace enclosure: one building, several periods.** **Point:** The Raja Mahal stands in ruins inside the walled city, held by the state administration. The survey calls it an undated fortified residential palace that "had been the seat of power for centuries with different rulers", and repeats the local saying that Udayāditya built it. Its own descriptions do not fit one period: an eastern entrance with pointed arches, colonnades and decorated columns, corner projections with arrow slits, relief carving, floral inlay, calligraphy, a highly ornamented pillared hall, and a room roofed on now-corroded iron joists with pillars whose capitals are carved in the *caumukha* manner. The survey dates the building to the eleventh century in its list, while elsewhere it dates a Rāma temple to the thirteenth century by its likeness to the palace. Interpretation, once: the fabric records occupation and rebuilding over a long period; no part of it is securely dated.
     - E: C07-GEOHER-052 (T7), C07-GEOHER-060 (T7), C07-INTACH-019 (T7), C07-GEOHER-056 (T7), C07-GEOHER-057 (T7), C07-INTACH-009 (T7) · C: C07-GEOHER-055 (T7), C07-INTACH-022 (T7) · Note: C07-GEOHER-052 (T7), C07-GEOHER-055 (T7) (the Udayāditya attribution: "It is said" in one passage, stated flatly in another)
  3. **P3 — Paramāra palace or Mughal mansion?** **Point:** Keep two buildings apart until an item joins them. Patil and the Gazetteer describe, close to the Shahi Masjid, the ruins of a spacious mansion in the simple, elegant early-Mughal style with good *jālī* work, probably the Mughal governor's residence, the mosque and graveyard being its adjuncts. Tiwari, walking the Raja Mahal's ruins, reads its pillars, doorways and wall niches as Paramāra work and the stone walls raised between corridor pillars as later encroachment. Whether Patil's mansion is the Raja Mahal, or a separate building of the Mughal period near it, the items do not say. Recall 1.3's note on the founder dispute in a clause; the legal and political history of the claim (farman, 2021 claimant, madrasa) is Chapter 10's and Chapter 11's.
     - E: C07-MADHYABHARAT-019 (T5), C07-GAZ-012 (T7) · C: C07-JAGTA-EN-033 (T8), C07-JAGTA-EN-030 (T8) · Note: C07-JAGTA-EN-016 (T8), C07-JAGTA-EN-018 (T8) (Tiwari's reading that a mosque inside the palace enclosure was once part of the palace, cross-referenced to 7.4)
  4. **P4 — Houses built of older houses and temples.** **Point:** The town reused itself. Pieces of carved stone are built into houses lane after lane, and the houses round the temple are built of old architectural material. One family's house, cleared out of a mound, proved to contain rooms of finely carved stone, one like a temple sanctum set with carved images; behind the Bijamandal the back walls of a Rāma temple and of old shops show stones of several periods, the temple's the oldest. The survey records havelis still held by families (one by the sixth generation of the Daulat Rai Mathur family), and lists the Purana Bazaar and Purani Basti as precincts. Set against this Patil's general judgement that no ancient palaces or houses survive in Madhya Bharat, which he thought were built of perishable wood: Udaypur's stone houses are old, but how old is a reading, not a finding. Do not repeat 1.1's courtyards or the twelve-courtyard house.
     - E: C07-JAGTA-EN-005 (T8), C07-JAGTA-EN-039 (T8), C07-JAGTA-EN-036 (T8), C07-JAGTA-EN-035 (T8), C07-JAGTA-EN-038 (T8), C07-INTACH-022 (T7) · C: C07-GEOHER-059 (T7), C07-GEOHER-065 (T7), C07-JAGTA-EN-040 (T8) · X: C07-MADHYABHARAT-017 (T5) (contextual, tier 5)
- **Drafting guidance:**
  - Tiwari supplies no measurement: omit his "twenty-foot" walls, "four bigha", "three and a half bigha", "500-metre radius", "more than five hundred years", "eight thousand", and his 90° street grid (Ch 4's, as his reading).
  - "Pointed arches" as a sign of work after the Sultanate conquest is the book's inference (tier 10): state it once, lightly ("pointed arches of a kind not used in the eleventh century"), or let the juxtaposition carry it. Iron joists likewise signal recent repair; do not date them.
  - Do not say the Raja Mahal and Patil's mansion are the same; do not say they differ either. Keep the 1.3 note's ruling.
  - Name the gates once; do not list GPS coordinates or grades.
  - The private-property signboard, the broken wall and the iron gate (C07-JAGTA-HI-001 (T8), -003, -052) are Chapter 11's: do not use here.
- **Transition:** Among the reused stones and carved rooms, some buildings were never secular: the Bijamandal, a temple-like house beside the great temple, leads into the town's other shrines.

---

## 7.3 Shrines after the great temple *(Hindu, Jain and memorial buildings · ~700 w)*

**Word target:** 700

- **Section statement:** By the end, the reader knows that shrine-building at Udaypur did not stop with Udayeśvara: the Bijamandal (probably contemporary with it, with an unfinished inscription praising the Sun), the Barakhambi hall of a lost eleventh-century temple (with a pillar inscription of V.S. 1625), the plain and later Pisanhari temple, a Rāma temple proposed as thirteenth-century, a shrine assigned by its images to the eleventh–fifteenth centuries, a Jain precinct with broken images, and memorial *chhatrī*s and sati stones; and that the survey's blanket "11th century" for the town's temples is a proposal its own text contradicts.
- **Purpose:** Show by the lesser shrines that the town kept building for worship long after its founder, and that worship was not Śaiva only. Defer the temple and its court to Chapter 5; the hill's rock-cut sculpture is in 7.1 P3a.
- **Paragraph plan:**
  1. **P1 — The Bijamandal.** **Point:** Beside the temple stands the remnant of a two-storeyed house, probably contemporary with it, called the Bijamandal or Ghariyālon kā makān; an unfinished Sanskrit inscription on it opens with praise of the Sun, which Patil took to support the name's sense of a time-keeper's house. Today it is lived in, its temple-like doorway, pillars and empty sanctum used for cattle and fodder. Do not repeat 1.1's time-keepers' family; the inscription's text is Chapter 6's.
     - E: C07-MADHYABHARAT-018 (T5), C07-GAZ-011 (T7) · C: C07-JAGTA-EN-029 (T8), C07-JAGTA-HI-016 (T8), C07-GEOHER-059 (T7) · Note: C07-CII-001 (T1), C07-GANGULY-002 (T5), C07-HARDY-001 (T5) (Vidisha's Bijamandal, a temple converted to a mosque, is a different building: do not confuse the two)
  2. **P2 — A hall without its temple; a plain later shrine.** **Point:** On the village's edge the Barakhambi survives as the *sabhāmaṇḍapa* of a ruined eleventh-century temple: twelve pillars on a high platform, raised seats with backrests, a ceiling of one massive slab. It is centrally protected, and a pillar carries an inscription of V.S. 1625 (c. 1568), later than the hall, evidence that the building was still visited five centuries on. The Pisanhari temple near Udayeśvara is plain, with a finely carved entrance; Patil judged from its style that it is much later than the great temple, which belies the grinder-woman tradition told in 1.4 (recall in a clause).
     - E: C07-MADHYABHARAT-004 (T5), C07-GAZ-002 (T7), C07-GAZ-003 (T7), C07-INTACH-007 (T7), C07-INTACH-006 (T7), C07-PANDE-002 (T5), C07-MADHYABHARAT-006 (T5) · C: C07-JAGTA-EN-009 (T8), C07-GEOHER-060 (T7), C07-GEOHER-059 (T7)
  3. **P3 — Building went on.** **Point:** The survey lists about a dozen temples still in use and assigns almost all to the eleventh century, but its own descriptions date a Rāma temple to the thirteenth century by its likeness to the palace and a shrine near the Chatua Darwaza to between the eleventh and fifteenth by its images; the list itself puts a Badi Main Mandir in the sixteenth century and the Jain temple in the eighteenth. Shrine-building continued through the Sultanate and Mughal centuries. Tiwari's "missile temple" in a ruined precinct belongs here as testimony, its date only in a note.
     - E: C07-GEOHER-059 (T7), C07-GEOHER-062 (T7), C07-GEOHER-063 (T7), C07-INTACH-008 (T7), C07-INTACH-009 (T7), C07-INTACH-010 (T7), C07-INTACH-011 (T7) · C: C07-JAGTA-EN-011 (T8), C07-JAGTA-EN-012 (T8) · Note: C07-JAGTA-EN-013 (T8) (Narayan Vyas's assessment from photographs, as Tiwari reports it; see flags)
  4. **P4 — Jinas, memorials and the dead.** **Point:** Not all worship was Śaiva. A Jain precinct in the town holds broken Tīrthaṅkara images; broken Jain sculptures lie with a Śiva-Pārvatī group under a pipal by the Bhujariya Talab; the hill's Tīrthaṅkara figures are recalled from Chapter 3. Commemoration left its own buildings: an octagonal *chhatrī* with carved columns near the large tank, other *chhatrī*s in the list, and, near the Chanderi gate, *samādhi*s and sati stones now hemmed in by houses. The hill's rock panels and the Ravan Tol colossus were told in 7.1 P3a: do not repeat them.
     - E: C07-JAGTA-EN-008 (T8), C07-GEOHER-045 (T7), C07-INTACH-020 (T7), C07-JAGTA-EN-003 (T8) · C: C07-GEOHER-029 (T7), C07-GEOHER-060 (T7), C07-GEOHER-063 (T7)
- **Drafting guidance:** V.S. 1625 → c. 1568 (subtract 57; one-year range acceptable: "1568–69"); flag for checking. "Probably contemporary" is Patil's: keep the hedge. Never call any of these temples "Paramāra" unless an item does. Tiwari's "missile" comparison, "seven-foot platform" and Vyas's date stay out of the text. Do not quote Tiwari's "smashed to smithereens" (C07-JAGTA-EN-007 (T8)): no date or agent is known; violence against images is Chapter 10's question.
- **Transition:** The same centuries that saw new shrines also saw the first mosques, and those carry the town's only dated building inscriptions.

---

## 7.4 Three mosques and the graves on the hill *(Islamic buildings · ~800 w)*

**Word target:** 800

- **Section statement:** By the end, the reader knows the town's three dated mosques as buildings, each placed differently: one built into the temple court from its own demolished parts (1336–38), one built outside the eastern gate in the Mandu manner with Persian and Sanskrit inscriptions (1488), one set beside a governor's mansion and a platform of tombs (begun under Jahangir, finished 1632); and the undated Muslim layer of smaller mosques, a mausoleum, dargahs, a woman's tomb and graves, some of them on the fortified hill, whose north gate shows Muslim repair.
- **Purpose:** Add to 1.3's dated sequence what the fabric shows (material, placement, inscriptions, style), without re-telling the conquest. Resolve the old canon's Moti Darwaza conflict.
- **Paragraph plan:**
  1. **P1 — In the temple court.** **Point:** In Madhya Bharat the first mosques were made from converted temples, their material adjusted to the needs of a mosque; Udaypur's first followed that pattern. Beyond 1.3's dates and pillar rows, the fabric shows how: masons' marks and short lines on the reused pillars, which Beglar took as proof of their Hindu origin; a western gateway off-centre and built of old materials, judged contemporary with the mosque; two small archways either side of the sanctum, perhaps symbolic entrances to the mosque and now functionless. The main shrine stood. Do not re-tell the 1336–38 dates beyond a clause, the north-west/north-east note, or the Aurangzeb legend.
     - E: C07-PANDE-007 (T5), C07-PANDE-009 (T5), C07-PANDE-004 (T5) · C: C07-ARTPAR-001 (T5), C07-GANGULY-003 (T5), C07-PANDE-006 (T5) · X: C07-MADHYABHARAT-007 (T5) · Note: C07-PANDE-008 (T5) (Beglar's error over Aurangzeb, already noted in 1.3: cross-reference only), C07-JAGTA-EN-019 (T8) (Tiwari's reading of "half-finished walls" as a plan to cover the temple: testimony, note only if used)
  2. **P2 — Outside the eastern gate, 1488.** **Point:** A century and a half later the next mosque stood outside the town. Just beyond the eastern gate, Moti Darwaza, a small mosque with a graveyard on a common raised plinth was built, as its Persian and Sanskrit inscriptions record, by an agent of Sher Khan in the reign of Ghiyas Shah Khalji, sultan of Mandu, A.H. 894 (1488); its architecture follows the buildings of Mandu. The survey adds an inscription at the top of the *mihrāb* naming Sher Khan and Ghiyasuddin, finely bordered niches and a roof stone carved with nine fishes. A mosque by the gate, inscribed in the town's old language as well as the court's, marks a new holder building beside the town rather than inside its temple. Recall 1.3's sentence in a clause; the fabric is new here.
     - E: C07-MADHYABHARAT-003 (T5), C07-MADHYABHARAT-012 (T5), C07-GAZ-005 (T7), C07-INTACH-013 (T7), C07-INTACH-014 (T7) · C: C07-MADHYABHARAT-022 (T5), C07-GEOHER-061 (T7) · Note: C07-GEOHER-063 (T7) (the survey list's "Moti Masjid", state-protected, beside the Moti Masjid Darwaza, is dated "18th Century"; no item says whether it is Sher Khan's mosque), C07-JAGTA-EN-003 (T8) (a different, tiny mosque-like structure of temple rubble outside the *Chanderi* gate: not this building)
  3. **P3 — The governor's quarter, 1632.** **Point:** About a furlong east of the great temple stands the largest mosque, the Shahi Masjid, an imposing building, begun in Jahangir's reign and finished in Shah Jahan's in A.H. 1041 (1632), as its Persian inscription records. With it went the early-Mughal mansion of 7.2 and a large platform of tombs in front; Patil read mosque and graveyard as adjuncts of the mansion. Ruined in 1952, it is now protected by the state and in very good condition. In the town's memory one of its two mosques was a *kachahrī*, a court-house, long so called and so signboarded, remembered by Jahangir's name; no item says which mosque. The farman and the property claim are Chapter 10's.
     - E: C07-MADHYABHARAT-011 (T5), C07-MADHYABHARAT-019 (T5), C07-INTACH-012 (T7) · C: C07-GEOHER-063 (T7), C07-JAGTA-HI-065 (T8) · Note: C07-JAGTA-EN-017 (T8), C07-JAGTA-EN-018 (T8) (the *kachahrī* memory and Tiwari's reading that it was part of the palace), C10-JAGTA-EN-018 (T8) (farman: Ch 10)
  4. **P4 — The undated Muslim layer.** **Point:** Other Muslim buildings carry no inscription in the maps: smaller mosques in the lanes (one listed as sixteenth-century, one as seventeenth, one undated and ruined), an unknown mausoleum assigned to the eighteenth century, and, on the hill, a dargah with Hardol figures kept beside it that villagers still visit, the dry-masonry tomb of a woman with an arched entrance, stone-covered burial chambers on the middle level, and the mazar of Jind Baba. The colonial observer found the hill fort's north gate "repaired or altered by the Muhammadans", with a dargah of an unnamed Pir beside it, little regarded by the mostly Hindu villagers. That repair is the only sign in the maps that the hill was held and maintained after the conquest. The survey's "10th Century" for Jind Baba's mazar shows how far its period column can be trusted.
     - E: C07-GEOHER-031 (T7), C07-GEOHER-032 (T7), C07-GEOHER-033 (T7), C07-GEOHER-034 (T7), C07-GEOHER-063 (T7), C07-GEOHER-065 (T7) · C: C07-GEOHER-061 (T7), C07-MADHYABHARAT-008 (T5) · X: C07-MADHYABHARAT-009 (T5)
- **Drafting guidance:** "Muslim" in the narrator's voice; "Muhammadans" only inside the colonial quotation. Do not describe the 1336–38 conversion's violence or motive; regime change is Chapter 10's. Give A.H. dates once with the Common Era year. INTACH-012's "at the time of accession of Shah Jahan in 1632" conflicts with the known accession (1628): use Patil's wording (finished in Shah Jahan's reign). Tiwari's two "about 300 years old" mosques: no date from Tiwari. The 2021 Jama Masjid board and plywood minarets (C07-JAGTA-EN-015 (T8)) and restoration spending are Chapter 11's.
- **Transition:** A short way east of one of these mosques, Patil found a broad stepwell running down to the water; the town's water works are the last layer to read, and they run through every period.

---

## 7.5 Water of many ages *(tanks, kunds and stepwells in detail · ~950 w)*

**Word target:** 950

- **Section statement:** By the end, the reader knows Udaypur's water works structure by structure, from the reservoirs and stepwells inside the hill wall, through the stepwells of the slopes and town (two of them carrying unread inscriptions), to the tanks; that the Udaysagar is identified with the inscription's Udayasamudra only by proposal; and that the one tank near Udaypur whose builder, cost and purposes a contemporary record states was a Brahmin's work of merit in Naravarman's reign.
- **Purpose:** Deliver the detail that 2.4 reserved for this chapter (`chapters.md`, 14 Oct), building on 2.4's landscape account (tanks for fields and animals, wells and stepwells for drinking, *kund*s between settlement and tank) and 1.5's dating of the Bhujariya Talab, without repeating either.
- **Paragraph plan:**
  1. **P1 — Water inside the wall.** **Point:** The fortified hill held its own water. On the middle level a reservoir of about 11 × 15.5 m with four upright members in it lies among the stone cells of 7.1; a large stepwell built against the hill face on one side and walled on three, with steps added over time, is assigned by the survey to the later Paramāra period and read as the garrison's supply; it is dry now. On the top level a rectangular structure with steps down, four pillar-like members and thick lime plaster throughout is an enclosed underground reservoir whose purpose the survey leaves open. Lower down, a basin of about 1.5 × 3 m cut into the sandstone bed held storm water near carved panels assigned to the eighth–tenth centuries, and a drain of stone slabs runs unexcavated. Recall 2.4's *kund*s in a clause.
     - E: C07-GEOHER-019 (T7), C07-GEOHER-040 (T7), C07-GEOHER-041 (T7), C07-GEOHER-042 (T7), C07-GEOHER-050 (T7), C07-GEOHER-039 (T7) · C: C07-GEOHER-053 (T7) · X: C02-GEOHER-029 (T7) · Note: C07-GEOHER-036 (T7), C07-GEOHER-042 (T7) (whether the top-level "chamber" and the "underground reservoir" are one structure: not stated)
  2. **P2 — Stepwells on the slopes.** **Point:** Beyond 2.4's three-sided stepwell on Pindi Hill, the survey records its fabric: well-chiselled sandstone, the natural rock as its fourth side, projecting stones on the steps that the survey reads as signs of heavy religious use, the frame broken, the steps collapsed, the water gone. Separately it describes a rectangular stepped tank of about 24.5 × 44.5 m with some twenty steps laid in interlocking blocks, best preserved on the north; a *baoli* on the eastern side of the fortification; and carved fragments round a *baoli* that fit together into a pillar. Antiquities on stepwell bunds are assigned to the eighth century: reuse again (1.5), not a date for the stepwell.
     - E: C07-GEOHER-047 (T7), C07-GEOHER-048 (T7), C07-GEOHER-049 (T7), C07-GEOHER-046 (T7), C07-GEOHER-028 (T7) · C: C07-GEOHER-024 (T7) · Note: C07-GEOHER-047 (T7), C07-GEOHER-049 (T7) (both have about twenty steps; no item says they are one structure)
  3. **P3 — Stepwells in the town.** **Point:** In the town, the Ghoddaud-ki-baodi east of a mosque has a broad, easy flight of steps down which, as its name says, horses could run to the water; the survey list puts it in the seventeenth century. The Setho ki Banjya baoli has a shaft with occasional carved animals and flowers and paired brackets carrying slabs for drawing water; a Devanagari inscription on the inner lintel of a pavilion, at a stepwell still used for household water, has not been read in the maps. The list's other *baoli*s (Sambhu ji ki, Puttal, Tulsi Mahadev) and the Karna well are assigned to the eleventh century and mostly still in use (2.4, recall only). Tiwari adds a stepwell near a brick kiln with curving steps and an inscription, and on the Ghatera road another reached by a ramp. Elsewhere in Madhya Bharat stepwells carry inscriptions naming their builder and the sovereign; Udaypur's unread lintels are the best written route to a date after the lichens.
     - E: C07-MADHYABHARAT-016 (T5), C07-GAZ-009 (T7), C07-INTACH-018 (T7), C07-INTACH-016 (T7), C07-INTACH-017 (T7) · C: C07-JAGTA-EN-022 (T8), C07-JAGTA-EN-021 (T8), C07-GEOHER-064 (T7), C07-GEOHER-065 (T7) · X: C07-MADHYABHARAT-014 (T5)
  4. **P4 — The tanks.** **Point:** North of the village the Udaysagar, about 71 acres, is now a ruin, listed as eleventh-century; its masonry is finely cut, unlike the less evolved bund of the Bhujariya Talab, an 8.04-acre natural water body to the south-east beside a working quarry (its proposed date is 1.5's: do not repeat). The carved stone steps of the Udaysagar's *ghāṭ*s now go down into wheat fields (Tiwari's observation; 1.1 has the fields: recall only). The survey and Tiwari take it for the tank the temple inscription credits to Udayāditya, the Udayasamudra, whose ruins Patil placed a short way north-east of the town; Ganguly held that the Udayasamudra could not be traced. The identification is probable at most: say so once. A further ruined tank near Pathar Khandan is in the list.
     - E: C07-GEOHER-043 (T7), C07-GEOHER-037 (T7), C07-GEOHER-038 (T7), C07-MADHYABHARAT-015 (T5), C07-GANGULY-007 (T5) · C: C07-GAZ-008 (T7), C07-GEOHER-065 (T7), C07-INTACH-015 (T7), C07-JAGTA-EN-024 (T8) · Note: C07-GANGULY-005 (T5), C07-GANGULY-007 (T5), C07-MADHYABHARAT-015 (T5), C07-GEOHER-044 (T7) (the identification conflict, map §5)
  5. **P5 — A Brahmin's tank, V.S. 1151.** **Point:** Close the chapter on the one written record of a Paramāra tank near Udaypur. In Naravarman's reign, in V.S. 1151 (1093–95; the editor finds the day unverifiable), a Brahmin named Vikrama built a tank; the inscribed slab was found in 1923–24 by a ruined tank at Amērā, about 3 km south of the village; he spent 2,500 coins stamped with the royal effigy, money earned by just means, on a tank of dressed stone with wide banks, for bathing, prayer, the worship of gods and sages and libations to the dead, for the merit of providing water. Similar records elsewhere in Paramāra Malwa show kings and private donors digging tanks and stepped wells beside temples, and villagers pooling money for a stepwell's drinking water. The one securely documented tank by Udaypur is not the founder's, and its stated purposes are ritual as much as practical. End on that content, which carries Chapter 8's subject (ritual and the material life).
     - E: C07-CII-003 (T1) · C: C06-CII-011 (T1), C06-CII-032 (T1) (findspot), C06-CII-013 (T1) (date) (Ch 6 items: the record's text is 6.1 P4's; here the tank) , C06-CII-048 (T1), C06-CII-010 (T1) (V.S. 1151 = 1093, 1094 or 1095) · Note: C07-GANGULY-006 (T5) (Ganguly: a V.S. 1151 tank record of Naravarman's reign found by a tank "about a mile to the south"; that it is the Amērā record is probable but not stated) · X: C07-CII-002 (T1), C07-CII-004 (T1), C07-GANGULY-008 (T5), C07-MADHYABHARAT-013 (T5), C07-HARDY-002 (T5)
- **Drafting guidance:** Survey dimensions once each, as "about". No measurement, count or angle from Tiwari: omit "980 metres", "45-degree", "five or six" stepwells; the shells and copper coin found in shallow digging may appear only in a note, as his report. Never adopt "unique and found nowhere else in MP" (C07-GEOHER-041 (T7)) or "intelligent and durable technique". Do not identify Vikrama's tank with the Bhujariya Talab, the Pathar Khandan tank or any listed tank; follow CII for findspot and date; Ganguly's "about a mile to the south" stays in the note, and the two descriptions are not merged in the text. Do not identify the Udaysagar with the Udayasamudra in the narrator's voice; "has been taken for" is the right grade. The normative tank and stepwell types of the popular account (C07-RAJABHOJ-EN-022 (T9), -023) are not used. The 56/52/12½ tally is 1.1's.
- **Transition (into Chapter 8):** The record's purposes (bathing, worship, offerings to the dead, water for people and fields) are the matter of the next chapter.

## Chapter 7: conflicts to present, unresolved

| Conflict | Where | How held |
|---|---|---|
| The wall's date: before Udayāditya or his (the survey gives both), tenth century in its list | **7.1 P4 (home)** | Open; "may be older than Udayāditya"; the lichen route last |
| Area: 56 acres vs a "169-acre complex"; the wall's extent (circular sector / all sides / three sides) | 7.1 | 56 acres in the text; the variants in a note |
| The colossus: Śiva in a boulder (Patil, Gazetteer) vs dancing Naṭarāja (survey); abandoned under attack (survey) vs by dynastic decline ("common belief") | 7.1 P3a | Both identifications attributed; both causes as proposals; no dimension |
| The Moti Masjid: 18th c. (survey list) vs Sher Khan inscription (INTACH) | 7.4 | Possibly two buildings; not merged (flag) |
| Shahi Masjid "1616" (old canon) vs begun under Jahangir, finished A.H. 1041 (1632) | 7.4 | 1632; "1616" retired; INTACH's "accession of Shah Jahan in 1632" not followed |
| The Udayasamudra vs the Udaysagar | **7.5 (home)** | Not identified; a proposal |
| Palace founder | 7.2 (fabric) / **10.4 (home)** | "Its builder is disputed"; no note here |
| Pairs kept apart | 7.2, 7.4, 7.5 | Raja Mahal / Patil's mansion; the two twenty-step structures (C07-GEOHER-047, -049); the two four-pillar reservoirs (C07-GEOHER-036, -042); Udaypur's Bijamandal / Vidisha's |

## Chapter 7: hand-offs

- **In:** Chapter 6 has read the town's inscribed stones; Chapter 7 opens on the largest work at Udaypur that carries no inscription at all. A colonial-era observer, quoted but not dated in the survey (C07-GEOHER-002; probably Beglar's tour of 1871–72, but the item does not say so: name and date only after the ASR VII ingest), found on the hill south of the town a wall of huge uncemented stones with several gates, the place deserted, and "it has not even a name that I could hear of". Open on that wall and that silence: the contrast with Chapter 6's written record carries the chapter's question (what can unwritten buildings tell?). Do not give the visitor's thickness figure (see 7.1 guidance).
- **Out:** it ends on Vikrama's tank and its stated uses (bathing, worship, offerings to ancestors, water as merit), material that Chapter 8 takes up as ritual and agriculture. It must not summarise the chapter, announce Chapter 8, or close on an aphorism about stone and water (1.5 already ends that way).

## Chapter 7: changes from the master outline

1. **7.1 P3a (added at merge; the user accepted §7.1 at about 1,050 words, U4):** the hill's rock panels, Lajja Gaurī, the museum pieces and the Ravan Tol colossus.
2. **7.3 P4:** the cross-reference line to Ch 5 was removed (the items are now in 7.1 P3a).
3. **Evidence pass:** the direct-item coverage is complete (no unused tier ≤ 5 item of substance). No structural change.

## Chapter 7: research and verification flags

- "The fort predates Udayāditya" (old canon) is not established.
- "Earthen rampart stone-faced inside" (old canon) has no item.
- Thickness figures withheld
- Area conflict:
- Extent of the wall:
- Moti Darwaza / Sher Khan conflict with the old canon: recommend retiring the canon note.
- Moti Masjid date:
- Shahi Masjid "1616–1632" (old canon):
- The palace/mansion identity
- V.S. 1625 on a Barakhambi pillar
- Udaysagar = Udayasamudra:
- The "1059" in C07-GEOHER-035, -044
- Vikrama's tank:
- Unread inscriptions
- Survey "period" column
- Mis-homed Gazetteer items:
- Vidisha's Bijamandal ≠ Udaypur's Bijamandal.
- Bastion typology
- Colonial observer's identity
- Measurements from Tiwari excluded:
- SAMAR items
- **Page-image checks:** INTACH pp. 54 and 58 (the pointed-arch building and the V.S. 1625 pillar inscription, tied to buildings only by context); C07-GAZ-004 and -007 (p. 340, outside the Udaypur entry: excluded).
- **Staged sources (leads, `ocr_verify`):** Beglar, ASR VII, probably the unnamed colonial observer of C07-GEOHER-002 (name and date only after ingest).
- **Tiwari's figures excluded:** twenty-foot walls, "four bigha", "980 m", the "45-degree" ramp, "five or six" stepwells, the "27-foot" Naṭarāja.

---

# Chapter 8. Religion and the Material Life of Udaypur: Ritual, Agriculture, Trade and Craft

**Planned words:** 3,800 (8.1: 850 · 8.2: 750 · 8.3: 600 · 8.4: 750 · 8.5: 850). **Evidence:** `evidence_index/ch08.jsonl`.

**Historical question.** What did the god of Udaypur's temple live on, and who served him? That is: what can actually be shown of the endowments, the land, the crafts and the trade that kept a royal Śaiva temple going at Udaypur, and of the people who performed its worship?

**Through-line.** By the end, the reader knows that Udaypur's temple is known to have been provisioned by gifts of village and plot from the countryside around it rather than by any recorded foundation estate, that the means and the people a Paramāra temple needed are visible only regionally, and that the one service still traceable at Udaypur is carried by a family's memory.

**Arc.** Opening on the Dhāmadeva pillar record at the temple's eastern gate → 8.1 the three Udaypur endowments and the missing foundation endowment → 8.2 the regional menu of means (scale shift out to the Paramāra kingdom and its branches, with Vidisha and Bhilsa as the nearest instances) → 8.3 what the grants' language says about land, measure and water (scale down to the field, still regional, with the Udaypur *biswa* as the anchor) → 8.4 stone, cloth and markets (Udaypur's one named craft; regional trade; the modern district as baseline) → 8.5 the god's servants and the god's doctrine (back inside the temple; from the eleventh century to today) → close on the time-keepers' family, which hands to Ch 9.

**Scope.** *Chronological:* the dated Udaypur endowments, 1163–1232. The regional pattern of Paramāra temple endowment runs from the 10th to the 13th century (labelled regional). Service and worship run from the eleventh century to the last record (c. 2021). *Geographical:* Udaypur's temples and the Bhṛṅgārikā group of villages (Bhiraṅgāvalī, about 6 km north-east, CII's identification); Vidisha and Bhilsa as the nearest comparisons; Abu and Chandrāvatī only as labelled western branches. Each section states once what it cannot show for Udaypur itself.

**Editor's merge rulings carried into this plan** (from the master outline):
> **Editor's merge rulings for Chapter 8** (these override the entry below where they differ)
> - **Opening (replaces the entry's "Opening move" and its "Editor: align with Ch 7's last line"):** open on the **gift**: Dhāmadeva, Devapāla's treasury officer, giving four *biswa* of land to the god, "taking water in hand", in 1229. The doorway and pillar are **not** the opening image, because Chapter 6 opened at the east door. The pillar location is one clause in 8.1 P1. The link to Chapter 7's last paragraph is by content: Vikrama's tank was water given as merit; this is land given to a god.
> - **The 1229 and 1232 records:** 8.1 uses them for what was given, from where and in what measure. Text, register and date conversion are 6.4's: give "1229" and recall the alternative only if 6.4 does.
> - **Vasantapāla, 1163:** "who ruled the province then belongs to Ch 10" is confirmed. Chapter 8 says only "in 1163, when Rājyapāla governed from Udayapura", and the Caulukya overlordship is stated in 10.1 (Part I, C1-A).
> - **8.5:** doctrine in one paragraph, citing 5.5. Practice and service (the time-keepers' family) carry the section.
> - **Length:** ~3,800 words planned. 8.3 and 8.4 may land short ("accept ~550 / ~650"); never pad.

## 8.1 Four *biswa* at the eastern gate *(the Udaypur endowments, 1163–1229 · ~850 w)*

**Word target:** 850

- **Section statement:** By the end, the reader knows the three endowments recorded for Udaypur's temples, what each gave and from where, that two of them drew on the same group of villages to the north-east, and that no record of the temple's original endowment has been found.
- **Purpose:** Put the chapter's only dated, Udaypur-specific material evidence first, and fix the scale of what it shows.
- **Paragraph plan:**
  1. **P1 — The pillar record.** **Point:** Establish the 1229 gift as an act: in Devapāla's reign, on a Friday in the bright half of Kārttika, V.S. 1286, Dhāmadeva, the king's treasury officer, gave plots of land, four *biswa*, before the god of the temple, pouring water as the rite of gift; since no donee is named, the editor takes the god as the recipient. The record names the god "Udalmēśvara", which CII reads as Udayeśvara. The record is on the pillar right of the eastern gate. One clause recalls that this is the earlier of Devapāla's two records already met in 1.3.
     - E: C08-CII-020 (T1), C08-JAGTA-EN-008 (T8) · C: C06-CII-037 (T1) (home 6.4: the date), C08-JAGTA-EN-009 (T8), C08-JAGTA-EN-010 (T8), C08-JAGTA-HI-015 (T8) · Note: C08-JAGTA-HI-013 (T8) (Hindi original of the date), C06-CII-036 (T1) (alternative calendar reckoning to October 1230)
  2. **P2 — How small, and where.** **Point:** Give the measure its meaning without inflating it: if the reading *visvē* is right, it is the local *biswa*, a twentieth of a *bigha*, possibly from Sanskrit *viṃśatika*; the unit was current locally in the Bhopal region. The record's Bhṛṅgāri is the Bhṛṅgārikā of Lūṇapasāka's grant, probably the village Bhiraṅgāvalī about 6 km north-east of Udaypur, here "the principal village of the group of 64". The record also mentions a *panchakula*, a body that in other records means a local council of elders (one clause; the epigraphy is Ch 6's).
     - E: C08-CII-039 (T1) · C: C06-CII-038 (T1) (home 6.4: the Bhṛṅgāri identification), C08-JAGTA-EN-011 (T8), C08-JAGTA-HI-014 (T8) · X: C08-JAGTA-EN-012 (T8) · Note: C08-JAGTA-EN-012 (T8) (Verma's gloss of *panchakula*, via Tiwari)
  3. **P3 — The earlier gifts.** **Point:** Set 1229 in sequence. In 1163, when Rājyapāla held the eastern division from Udayapura, Vasantapāla made donations for the maintenance of the temple Ganguly calls Udaleśvara at Udayapura; who ruled the province then belongs to Ch 10 (note: Ganguly places this under Kumārapāla's governor, i.e. Caulukya rule). In the early 1170s Lūṇapasāka gave the village of Umaratha in the Bhṛṅgārikā *pāṭhaka* to the god Vaidyanātha at Udayapura (recall 1.3 in one clause: do not retell; the new point is the shared Bhṛṅgārikā). The same group of villages thus supplied two Udaypur endowments sixty years apart, one a whole village, one a plot. Do not identify Udaleśvara, Vaidyanātha and Udayeśvara as one god or one temple: the items name three.
     - E: C08-GANGULY-016 (T5), C08-GANGULY-015 (T5) · C: C06-CII-038 (T1), C01-CII-010 (T1) · Note: C08-GANGULY-016 (T5) (Ganguly's report only; not yet found in the CII items in the map), the Lūṇapasāka date range (1172 Ganguly / 1173 CII: "early 1170s", ROADMAP 18)
  4. **P4 — What is missing.** **Point:** State the gap once, as a limit of the evidence. Ganguly reports that Udayāditya erected temples, had tanks dug, performed ceremonies and "granted lands productive of gold and corn to the Brahmans": a general report (attribute to Ganguly in a note; it is very probably drawn from praśasti language, which is claim, not record). No grant endowing the Udayeśvara temple at its founding is known, and Tiwari, who looked for one, says none has been found. The temple's first provisioning is therefore unknown; the dated gifts are additions, by officials and a governor, to an institution already running. Then one sentence on the small gift: a plot of four *biswa* recorded on so great a temple puzzles; comparable small religious grants exist in Cāhamāna and Caulukya records (Verma via Tiwari), so smallness need not mean a special plot. Tiwari's speculations (a water source, a stepwell, a priest's house) go in a note, marked as conjecture, or are omitted.
     - E: C08-GANGULY-013 (T5), C08-JAGTA-HI-012 (T8) · C: C08-JAGTA-EN-007 (T8), C08-JAGTA-EN-013 (T8) · Note: C08-JAGTA-HI-017 (T8) (Verma comparison; Tiwari's "two decades" construction claim must NOT be carried: see flags), C08-JAGTA-EN-014 (T8) / C08-JAGTA-HI-016 (T8) (Tiwari's conjectures about the plot)
- **Drafting guidance:** Narrate P1 closely: it is the chapter's only scene-like object, but no scene (no crowd, no priest, no weather). Let "taking water in hand" carry the rite; quote it once from the CII-backed reading (C08-JAGTA-EN-010 (T8) is a translation of the text, quotable as such). Name Dhāmadeva once with his office; do not call him "treasurer" loosely (he is "an officer in charge of the treasury"). Do not explain the *panchakula* beyond one clause. Keep Tiwari out of the subject position: "the record's own phrase", not "Tiwari writes". Graded confidence: *biswa* "probably" (CII says "if the reading is correct"); Bhiraṅgāvalī "probably"/"is identified with"; Vasantapāla's gift "is reported". **Never** state "the temple was built over two decades" (C08-JAGTA-HI-017 (T8)) or "three years": the construction span is disputed (map Conflicts, "temple foundation/consecration date") and only 1080 is firm.
- **Transition:** If Udaypur's own stones show only three gifts, the Paramāra kingdom's other temples show what such gifts could be: by turning outward, the reader sees the range from which Udaypur's donors chose.

---

## 8.2 What kept a Paramāra temple *(the regional pattern of endowment · ~750 w)*

**Word target:** 750

- **Section statement:** By the end, the reader knows the kinds of income Paramāra-period temples in Malwa and its branches are recorded as receiving (villages, plots, flower gardens, shops, oil-mills, cash, tolls on bull-loads, levies on market goods and houses), that a toll of this kind was laid at Vidisha in the twelfth century and that Bhilsa's bazaars paid rent to a Sun temple in 878, and that temple land was lightly taxed rather than wholly exempt. The reader also knows that none of this is recorded at Udaypur.
- **Purpose:** Supply the frame that Udaypur's three gifts need, at the nearest scale the evidence allows, and say plainly what it can and cannot show for Udaypur.
- **Paragraph plan:**
  1. **P1 — Nearest first: Vidisha and Bhilsa.** **Point:** In Udaypur's own province, a king Trailokyavarman laid a tax of one *viṃśopaka* on every load carried on a bull, "evidently in favour of the temple" (the Vidisha record; he is called king but his house is not named); and in 878 two bazaars of Bhāillasvāmin (Bhilsa) were let out and their rent of 130 *dramma*s given to the Sun temple. A temple could be fed by traffic and trade, not only by fields. Keep Trailokyavarman's dynastic identity for Ch 10 (C01/C10 items); do not resolve it here.
     - E: C08-CII-017 (T1), C08-CII-018 (T1), C08-RAJABHOJ-EN-007 (T9) · C: C08-CII-043 (T1) (*āvāsanikā*, "stall or shop", in a Bhilsa record of V.S. 935) · Note: C08-PARTEMPLES-001 (T5) (Vidisha V.S. 1216 and Gyaraspur records: temples built, images installed and villages granted for worship, in a regency period)
  2. **P2 — The range of a gift.** **Point:** Across the kingdom and its branches the same kinds of income recur: whole villages to temples and Brāhmaṇas (with the king ordering villagers to render cash taxes, the crop share and other dues to the donee); land for flower gardens with fourteen merchants' shops, oil-mills and fourteen *dramma*s for worship, *abhiṣeka*, offerings and festivals at a Jain temple in Bhoja's time; a Śiva temple at Pānāhedā assigned a *viṃśopaka* on every bull passing on the road, land, a garden and rice fields; and, at Arthūnā in the Vāgaḍa branch, levies on traders' houses at festivals, braziers' shops, distillers, a gambling house and loads of sugar, cotton, salt, oil and cloth, collected monthly. In Udayāditya's own reign at Jhalrapatan a Śiva temple was promised four *pala*s of oil and a ball of sweets yearly. Compress: one sentence per kind, not a catalogue; the Jain example shows the same means served all faiths.
     - E: C08-CII-007 (T1), C08-CII-011 (T1), C08-CII-026 (T1), C08-CII-045 (T1), C08-CII-046 (T1), C08-CII-012 (T1) · C: C08-CII-010 (T1), C08-GANGULY-011 (T5), C08-GANGULY-012 (T5), C08-GANGULY-022 (T5), C08-BHOJA-TIMES-030 (T5) · X: C08-CII-047 (T1) (*dramma* as a silver coin) · Note: C08-CII-004 (T1) (980: village for worship and repairs at Ujjain), C08-CII-009 (T1) (grant to a Śaiva ascetic for Ghaṇṭeśvara), C08-CII-025 (T1) (Girvaḍ: grain per water-wheel and well, custom-duty)
  3. **P3 — Who gave, and how.** **Point:** Gifts were made by kings, queens, governors, officials and merchants, typically after a ritual bath and on eclipses, *saṅkrānti*s and anniversaries, publicly, in front of the village headman and people, with the land first inspected and shown to the donee. Temple land was not always free of tax: lands granted to temples could still be taxed, if lightly. This is how the Udaypur gifts of 8.1 should be imagined procedurally, and no further.
     - E: C08-CII-006 (T1), C08-CII-007 (T1), C08-BHOJA-TIMES-021 (T5), C08-BHOJA-TIMES-026 (T5) · C: C08-BHOJA-TIMES-024 (T5), C08-BHOJA-TIMES-025 (T5), C08-CII-034 (T1) (a Paramāra queen's golden cupola, 1118), C08-HARDY-005 (T5) (merchants and guilds as temple donors) · Note: C08-CII-001 (T1) (Harsaudā, 1218: the merchant Keśava's temple, tank and images: a mercantile patron in Devapāla's reign; "Undapura" is NOT identified with Udaypur, see flags)
  4. **P4 — What this can and cannot show for Udaypur.** **Point:** One short paragraph. The pattern shows that a temple like Udayeśvara *could* have drawn on tolls, shops and levies as well as land; the Udaypur records show only land and unspecified donations. Whether the town's own bazaar (Ch 7) paid the god anything is unrecorded. A later echo of the practice: until the early twentieth century, a village rebate on assessed revenue (*gaonti kharch*) still covered "charitable grants to temples" and festival expenses in this district: continuity of the habit, not of any medieval arrangement.
     - E: C08-GAZ-001 (T7) · C: C08-JAGTA-HI-008 (T8) (Tiwari's general point that running a temple was a separate administrative task) · X: C08-HARDY-003 (T5) (temples as landowners, employers and moneylenders: general, tier 5)
- **Drafting guidance:** Compress hard; this is context and must return to Udaypur in P4. No place outside the province is described; each is a single clause naming the place and the means. Never import a Rajasthan grant as if it were Malwa's: Arthūnā, Bhinmāl, Girvaḍ, Abu and Pānāhedā are Paramāra-branch records; say "in the dynasty's western branches" once. No TEMPLE-ECON. No modern-temple analogies (Nathdwara etc.). Do not convert *dramma* values to modern money.
- **Transition:** Every gift in this repertoire was, in the end, a claim on what the ground produced; the grants' own language shows how that ground was measured and worked.

---

## 8.3 The field behind the offering *(land, measure and water in the grants · ~600 w)*

**Word target:** 600

- **Section statement:** By the end, the reader knows how Paramāra-period grants measured and described the land they gave (the *hala*, the *nivartana*, the measuring rod of 96 parts, the fallow boundary strip, the threshing floor), what crops a grant could name, that wells and water-wheels were themselves gifts and taxable, and that none of this is recorded at Udaypur except the *biswa*. The reader also knows what the 1979 district record adds as a modern baseline and what it cannot say about the eleventh century.
- **Purpose:** Answer "agriculture" in the chapter's title without re-describing Udaypur's land (Ch 2). The question here is what religious institutions took from the land, in the grants' own terms.
- **Paragraph plan:**
  1. **P1 — Counting land.** **Point:** In the grants, a *hala* was as much land as one plough could work in a season; the editor works one out at about 20 *bigha*s, which Malwa still takes as a plough's season. Land was measured with a rod of 96 parts, as bamboo rods still are in Malwa, and two rods could be left fallow as the boundary between fields, known in Malwa as *meda*. Against this, four *biswa* (a fifth of a *bigha*, if CII's reading holds) is a very small holding. Recall 8.1 in a clause; do not reargue the plot's purpose.
     - E: C08-CII-036 (T1), C08-CII-038 (T1), C08-CII-037 (T1) · C: C08-CII-016 (T1), C08-CII-015 (T1) · X: C08-CII-039 (T1) (recall)
  2. **P2 — What the land grew and owed.** **Point:** A grant of Bhoja's time gave two *hala*s fit for *kodrava* (a coarse grain "eaten by the poor"), *mudga*, paddy and sesamum, with the corn on the threshing floor beside the houses; donees received the cash tax, the crop share and the extra cesses. Ganguly's report that Udayāditya gave "lands productive of gold and corn" uses the same vocabulary of yield (recall 8.1; one clause). This is the only window on what a medieval field near a temple grew in this kingdom; do not map these crops onto Udaypur's present *kharif*/*rabi* (Ch 2 has those).
     - E: C08-CII-035 (T1), C08-CII-007 (T1) · C: C08-GANGULY-013 (T5) · Note: C08-BHOJA-TIMES-032 (T5) (a Kṣatriya, Memmaka, cultivating a field near Gwalior in Bhoja's time: cultivators were not of one caste; tier 5)
  3. **P3 — Water as a gift.** **Point:** Wells and water-wheels were endowed and taxed: in the dynasty's western branches a prince gave an *araghaṭṭa*, a wheel of pots for lifting water; villagers gave grain from each wheel and each well to a god; a temple's levies included barley on a water-wheel. Small irrigation works were made by private persons. At Udaypur no such gift is recorded; its wells, stepwells and tanks are Ch 7's subject, and their landscape was told in 2.4. One sentence of modern baseline: in the district as the 1979 Gazetteer saw it, irrigation had never been conspicuous and reached under one per cent of the cropped area, with three-quarters of workers in agriculture in 1951–61. The baseline says the winter crop lived largely on stored moisture and rain; it says nothing of medieval irrigation.
     - E: C08-CII-040 (T1), C08-CII-041 (T1), C08-CII-025 (T1), C08-CII-042 (T1), C08-GAZ-003 (T7) · C: C08-BHOJA-TIMES-033 (T5), C08-GAZ-002 (T7), C08-GAZ-006 (T7) · X: C08-GAZ-004 (T7), C08-GAZ-005 (T7) (only if Ch 2 has not used them: check; C02-KB-GAZ-005 (T7)/-006 already carry them in 2.2) · Note: C08-GAZ-008 (T7) (Third Plan: 972 wells built, 340 repaired, 4 tanks repaired in the district: Ch 12's material if anywhere)
  - **Evidence pass (X, optional by default; P0):** C08-GAZ-011 (T7), C08-GAZ-012 (T7) — district crop area and production tables (1979), as district context only
- **Drafting guidance:** Short section; **accept ~550 words** rather than pad. No land description. Name the western branches once as such. Do not call the *araghaṭṭa* a "Persian wheel" (the CII editor rejects the term). Do not use Tiwari for any measure. 1979 figures are "in the district" and "by 1961", never "at Udaypur".
- **Transition:** Udaypur's ground gave stone as well as grain, and stone is the one craft the records name for the town.

---

## 8.4 Stone, cloth and the market *(craft and trade · ~750 w)*

**Word target:** 750

- **Section statement:** By the end, the reader knows that the only craft the records name for Udaypur is stone (red sandstone *kundies* of local reputation in the Gazetteer's day, dressed stone exported today), how temple building organised stone-workers in this period (master architect, surveyor, carver, fitter; hereditary families; guilds) as normative and regional evidence, and what Malwa traded in the Paramāra period. The reader also knows that no medieval craftsman, guild or market at Udaypur is named.
- **Purpose:** Answer "trade and craft" honestly: one named Udaypur craft, a regional picture of crafts and trade, and the modern district as a separate layer.
- **Paragraph plan:**
  1. **P1 — The craft the record names.** **Point:** The 1979 Gazetteer, citing an earlier source, says the red sandstone *kundies* (stone basins/troughs) of Udaypura had "a great local reputation", alongside the floor-cloths (*jajam*) of Basoda. This is the only craft product the evidence assigns to Udaypur by name. Today Udaypur and Pathari are a stone-quarrying area whose stone is cut, dressed and exported (recall 2.5 in a clause; do not retell). Do not invent who made the *kundies*.
     - E: C08-GAZ-014 (T7) · C: C08-JAGTA-EN-015 (T8) (recall only; told in 2.5 via C02-JAGTA-EN-002 (T8)/C02-JAGTA-HI-004 (T8)) · Note: C08-GAZ-014 (T7) (its footnote source is not given in the item: flag)
  2. **P2 — How temple stone was worked, in the norms.** **Point:** Treatises and modern scholarship describe the temple workshop as four roles: the *sthapati* with overall charge, the *sūtragrāhin* who laid out and measured, the *takṣaka* who cut and carved, the *vardhakin* who fitted, plastered and painted. These were hereditary family vocations, moving from site to site, organised in guilds that could levy a cess on members for a temple's upkeep. The quarry itself was a ritual place: the *sthapati* propitiated the spirits of the stone before cutting. Patil holds that the medieval temples of northern Madhya Bharat employed a class of stone carvers now called Patharphod. **None of this is recorded at Udaypur**; it says what any temple of this kind required, not who worked here. Masons' marks or names at Udayeśvara, if any, are Ch 5's (C08-KRAM-2-004 (T5) is Khajuraho's Duladeo, not Udaypur: do not use).
     - E: C08-HARDY-007 (T5), C08-KRAM-1-006 (T5), C08-KRAM-1-005 (T5) · C: C08-KRAM-1-007 (T5), C08-MADHYABHARAT-009 (T5), C08-BHOJA-TIMES-037 (T5) · Note: C08-MADHYABHARAT-009 (T5) (Patil's claim that Islam dealt carving "a fatal blow" by the 12th century: his interpretation; attribute or omit), C08-KRAM-1-002 (T5) (stone the most meritorious material: normative)
  3. **P3 — What Malwa traded.** **Point:** In the Paramāra period villages and towns had markets with traders' houses and traders' associations; the goods named are candied sugar, jaggery, madder, thread, cotton, coconuts, butter, oil, salt, areca-nuts, cloth, grain and cattle fodder. Malwa's cotton cloth was common enough to be exported, carried to Gujarat for shipment onward, by one report, on 2,000 oxen. Merchants were temple patrons (recall Keśava, 8.2 note). Tiwari calls Paramāra Udaypur one of the dynasty's busiest commercial centres and reads the rubble-filled shop rows by the old gates as its bazaar (recall 1.1; Ch 7 owns the fabric): one clause, as his reading, tier 8. The treatise attributed to Bhoja prescribes market streets and quarters for weavers, leather-workers, cloth-printers and guilds: normative, never evidence for Udaypur's plan (Ch 7 decides whether to use it).
     - E: C08-GANGULY-025 (T5), C08-BHOJA-TIMES-034 (T5), C08-BHOJA-TIMES-036 (T5) · C: C01-JAGTA-HI-006 (T8), C07-JAGTA-HI-007 (T8) · X: C08-RAJABHOJ-EN-009 (T9), C08-RAJABHOJ-EN-011 (T9) · Note: C08-SAMAR-1-002 (T4), C08-SAMAR-1-003 (T4) (paraphrase only, ⚠ old OCR; attribution to Bhoja doubted)
  4. **P4 — The modern layer.** **Point:** Mark the jump in time. In the district of the nineteenth and twentieth centuries the trades that mattered were others: Bhilsa tobacco, judged in the mid-nineteenth century the finest in India and grown on 1,326 acres of the old Bhilsa district in 1906–07; in 1969 the district's small industries made *bidi*s, *dari*s, country shoes, bricks and agricultural implements; today Ganj Basoda, the nearest town, is the market for grain, cloth and stone. Udaypur appears in this layer only through its stone. Keep to two or three sentences; Ch 12 owns livelihoods today.
     - E: C08-GAZ-013 (T7), C08-GAZ-018 (T7), C08-GAZ-019 (T7), C08-GAZ-020 (T7) · C: C08-JAGTA-EN-015 (T8) · Note: C08-GAZ-015 (T7), C08-GAZ-016 (T7) (district counts of leather-workers, smiths, carpenters, 1961: Ch 12 if anywhere), C08-GAZ-017 (T7) (retail traders: Ch 12)
- **Drafting guidance:** No invented anonymous agents: never "the carvers of Udaypur" or "Udaypur's masons" for the medieval period; the norms are "the treatises describe", "temple workshops of the period". "2,000 oxen" is a single report: keep it attributed in the note. Tiwari's "busiest commercial centre" is a claim, tier 8, one clause, not the paragraph's subject. The Gazetteer's *kundies* sentence is itself second-hand ("It is stated that"): keep that hedge. Mark the time jump in P4 by naming the century. **Accept ~650 words** if P3 cannot be filled without padding.
- **Transition:** The stone, the land and the gifts all served one purpose inside the temple: the god's daily worship and the people who performed it.

---

## 8.5 The god's servants and the god's doctrine *(ritual, sect and service, eleventh century to today · ~850 w)*

**Word target:** 850

- **Section statement:** By the end, the reader knows:
  - what Paramāra-period temple worship required (worship three times a day; bathing and anointing; fire offerings, food and flowers; gardens for flowers; music and dance);
  - that the Śaiva Siddhānta was the dominant school in Malwa and that Bhoja wrote its principal northern text;
  - that Pāśupata communities and Śaiva monasteries are recorded in the region but no monastery or ascetic order is recorded at Udaypur;
  - that the dynasty's Śaivism coexisted with patronage of other faiths;
  - what of the temple's service is visible at Udaypur itself: a hereditary time-keepers' family, a stone that may have held the drum, a *vedī* that tradition gives to the king, an instrument fragment, and worship continuing into the twenty-first century.
- **Purpose:** Give "ritual" and "Śaiva traditions" their due without inventing an Udaypur clergy, and end the chapter on living evidence.
- **Paragraph plan:**
  1. **P1 — What worship required.** **Point:** In the temples of the kingdom, worship was done three times a day; images were bathed and anointed with perfumes; fire offerings of holy wood, *kuśa*, sesamum and rice were made, with food and flowers; grants often provided flower gardens attached to temples; Bhoja listed the articles to be offered to each deity. Dancers thronged temple courtyards as well as palaces (a practice some contemporaries opposed: note). The needs (oil, flowers, food, cloth) are the same ones 8.2's endowments paid for; let the construction show it.
     - E: C08-BHOJA-TIMES-013 (T5), C08-GANGULY-007 (T5), C08-BHOJA-TIMES-016 (T5) · C: C08-BHOJA-TIMES-014 (T5), C08-BHOJA-TIMES-015 (T5), C08-CII-011 (T1) (flower-garden land, recall) · Note: C08-BHOJA-TIMES-020 (T5) (opposition to temple dancing girls: Mahesh Singh's reading), C08-BHOJA-TIMES-023 (T5) (temple posts by function, a Cālukya record of 1054: not Paramāra), C08-HARDY-006 (T5) (a Deccan temple's staff, incl. a stone-cutter: comparison only)
  2. **P2 — Which Śaivism.** **Point:** Between the eighth and twelfth centuries the Śaiva schools took distinct form; from Malwa southward the Śaiva Siddhānta dominated, and Bhoja's *Tattvaprakāśa* became the most important text of its northern school, made near-canonical by two commentaries. The Paramāra kings styled themselves devotees of Maheśvara and are said to have taken Siddhānta teachers. Pāśupata communities, the sect that traced itself to Lakulīśa, are recorded in the dynasty's western branches; in Devapāla's reign a merchant set a Nakulīśa image beside the temple he built at Harsaudā. Monasteries of the Mattamayūra Śaiva order stand at Kadwaha, Terahi and Ranod. **At Udaypur no monastery, ascetic line or sectarian record is known.** The reading of the temple's imagery as a statement of Siddhānta doctrine is Ch 5's: one recalling clause at most.
     - E: C08-PANDE-002 (T5), C08-PANDE-008 (T5), C08-BHOJA-TIMES-007 (T5), C08-BHOJA-TIMES-011 (T5) · C: C08-CII-003 (T1), C08-CII-002 (T1), C08-CII-001 (T1), C08-MADHYABHARAT-002 (T5), C08-MADHYABHARAT-004 (T5) · X: C08-BHOJA-TIMES-005 (T5), C08-BHOJA-TIMES-006 (T5), C08-GANGULY-004 (T5), C08-GANGULY-003 (T5) · Note: C05-PANDE-121 (T5) (Pande: the temple based on a Siddhānta sect; homed Ch 5), C08-PANDE-005 (T5) / C08-SKANDA-003 (T8) (Lakulīśa's Gujarat origin and Ujjain sermon: tradition), C08-MADHYABHARAT-005 (T5), C08-MADHYABHARAT-006 (T5) (the Mattamayūra lineage's monasteries and inscriptions)
  3. **P3 — Other gods beside Śiva.** **Point:** The dynasty's Śaivism did not exclude: a verse attributed to Bhoja bids one hear the Buddha's doctrine, practise the Jain, follow the Vedic in conduct and meditate on Śiva; Paramāra-period grants endowed Jain temples with the same means as Śaiva ones (recall 8.2); yet a Jain chronicler remembered that when Mahākāla's flag rose at Ujjain the Jains' flags were lowered. In the kingdom Śiva was worshipped under many names, Nīlakaṇṭheśvara and Udaleśvara among them. At Udaypur a Jain precinct with mutilated Tīrthaṅkara images is known (Ch 7 owns it; recall in a clause). Do not mention Harihara (Ch 5). Do not size the Jain community (Ch 9).
     - E: C08-RAJABHOJ-EN-005 (T9), C08-GANGULY-005 (T5), C08-GANGULY-002 (T5) · C: C08-RAJABHOJ-EN-002 (T9), C08-BHOJA-TIMES-010 (T5), C07-JAGTA-HI-015 (T8) · Note: C07-JAGTA-HI-017 (T8) (Tiwari's inference that Jain patrons lived in the town), C08-MADHYABHARAT-001 (T5), C08-MADHYABHARAT-003 (T5) (Madhya Bharat temple counts: about 240 Śaiva, 87 Vaiṣṇava, 89 Jain, of about 750 recorded)
  4. **P4 — Service at Udaypur.** **Point:** Bring the reader back inside Udayeśvara. In the closed hall a stone basin with a lotus-scroll border, its first purpose a water outlet, may also have held the drum; the time-keeper, in Pande's account, was an important member of the temple's retinue who struck it at fixed intervals. Recall in one clause the family of the Ghariyālon Kā Makān and its claim of centuries (1.1); the family's account, as Tiwari reports it, adds that the building may also have housed someone in charge of the temple's management or rites (note). Tradition holds that the king ordered the *vedī* built after the temple's completion for sacrifices; its ventilation and raised benches fit ritual use; music and dance with the rites is Pande's possibility. A wooden fragment of a stringed instrument found in a buried room led Tiwari to infer resident musicians (note; inference). The service is evidenced by one family's memory and by objects whose use is inferred.
     - E: C08-PANDE-009 (T5), C08-PANDE-012 (T5), C08-PANDE-010 (T5) · C: C08-JAGTA-EN-001 (T8), C09-JAGTA-HI-014 (T8) · Note: C08-JAGTA-EN-002 (T8) (musicians: Tiwari's inference), C08-JAGTA-HI-002 (T8) (the family's account, Hindi), C08-RAJABHOJ-EN-006 (T9) (a normative temple layout with dance halls, a sacrifice pavilion and a monastery: paraphrase, not evidence for Udaypur)
  5. **P5 — The living temple (closing).** **Point:** Worship has not stopped: morning and evening *pūjā* and *ārtī* into the twenty-first century, special *pūjā*s (Rudrāṣṭaka, Śiva Mahimā, Śiva Abhiṣeka) on request, and most visitors come only for the god in the sanctum. The temple's draw is still a material fact on Śivarātri (Ch 9 owns the fair and the festival calendar: one clause here). End on the time-keepers' family: the one group at Udaypur whose service to the god is remembered as hereditary, and whose memory reaches further than any record of it.
     - E: C08-PANDE-011 (T5), C08-JAGTA-HI-001 (T8) · C: C08-MADHYABHARAT-007 (T5) (Udaypur among the region's temples whose *liṅga*s are still worshipped) · Note: C08-JAGTA-HI-003 (T8) (daily *darśan* continued through the calamities: Tiwari's view; avoid his word "kafirs"), C08-JAGTA-EN-004 (T8) (crowds on Śivarātri: **never give Tiwari's count of police**)
- **Drafting guidance:** Never "the priests of Udaypur performed …" for the medieval period: no item names them. Introduce the *Tattvaprakāśa* once (Ch 4 or Ch 5 may introduce it first: check the ledger after those chapters; if so, recall). Doctrine gets one paragraph; no exposition of *pati–paśu–pāśa*. Never quote SAMAR. Pande's drum-stone "may also have held"; the *vedī* "tradition holds"; the family's "centuries" is their claim. End on content (the family), not on an aphorism about memory.
- **Transition (into Ch 9):** The time-keepers are a family with a memory of its place in the town; Chapter 9 asks who else lives in Udaypur and what each remembers.

## Chapter 8: conflicts to present, unresolved

| Conflict | Where | How held |
|---|---|---|
| Vasantapāla's donation, 1163: Ganguly only; to "Udaleśvara" | 8.1 P3 | Reported; Udaleśvara, Vaidyanātha and Udayeśvara not identified as one god or temple |
| The 1229 date: Chaitrādi 1229 vs Kārttikādi October 1230 | 8.1 P1 | "1229"; the alternative only if 6.4 gives it |
| The *biswa* reading ("if the reading is correct") | 8.1 P2 | Hedged once |
| Construction span ("two decades" in Tiwari vs "three years") | — | Neither carried |
| "Undapura" (Harsaudā 1218) | 8.2 | Not Udaypur; compatibility is not identity |
| Bhilsa rent of 878 (tier 9 report) | 8.2 | "A record from Bhilsa, as reported" until checked against CII |

## Chapter 8: hand-offs

- **In:** Open on the gift: in 1229 Dhāmadeva, Devapāla's treasury officer, gave four *biswa* of land to the god, "taking water in hand" (C08-CII-020, C06-CII-037, C08-JAGTA-EN-008). This takes up Ch 7's last paragraph (Vikrama's tank and its uses: water given as merit) by moving to land given to a god. The pillar by the eastern gate is one clause; the doorway is not the opening image (Ch 6 opened there).
- **Out:** it ends on the time-keepers' family as people who remember a hereditary service. It must not announce Ch 9, summarise Ch 8, or retell the fair or the gong story from 1.1.

## Chapter 8: changes from the master outline

1. **Opening (Part I, I.5):** open on the gift of land (Dhāmadeva's four *biswa*, "taking water in hand", 1229), not on the doorway, which Ch 6 used. The pillar's location is one clause.
2. **Merge correction:** the C06-CII-034…038 citations were shifted one place in the outline draft and corrected at merge.
3. **Evidence pass:** the coverage is complete. The district crop tables (C08-GAZ-011, -012; tier 7) are available for 8.3 only as district context, and only if 2.2's figures are not repeated. No structural change.

## Chapter 8: research and verification flags

- Vasantapāla, 1163 (C08-GANGULY-016)
- Dhāmadeva's date.
- The *biswa* reading
- Bhṛṅgāri = Bhiraṅgāvalī, ~6 km NE
- Construction span.
- Rhetoric of prosperity.
- "Undapura" (C08-CII-001).
- Bhilsa 878 rent (C08-RAJABHOJ-EN-007)
- Trailokyavarman (C08-CII-017/-018):
- Mewar leaks:
- GAZ "kundies" (C08-GAZ-014)
- Tiwari as measurement:
- SAMAR items
- Mahesh Singh locators
- Staged sources
- **Page-image checks:** C08-GANGULY-016 (find the 1163 record in CII VII.2); C08-GAZ-014 ("kundies": the older source in its footnote 1).
- **Staged sources (leads, `ocr_verify`):** the Gwalior Annual Report, Samvat 1974, no. 121 (cited by Tiwari for the pillar records).

---

# Chapter 9. Society and Cultural Life: Communities, Languages, Festivals and Oral Traditions

**Planned words:** 2,800 (9.1: 750 · 9.2: 450 · 9.3: 650 · 9.4: 950). **Evidence:** `evidence_index/ch09.jsonl`.

**Historical question.** Who lives in Udaypur, what do they speak and celebrate, and who keeps which memories of the town?

**Through-line.** By the end, the reader knows that Udaypur's people can be counted only at district scale and described only through one writer's testimony, but that the town keeps a dense body of stories which remember its founder through worshipped objects and its later centuries as loss, stories that are evidence of memory rather than of events.

**Arc.** Opening on a lane outside the temple → 9.1 communities (today's neighbours, back to the Paramāra social order, forward through remade identities to the district baseline) → 9.2 languages (speech in the census, record in stone) → 9.3 the year (Śivarātri and the fair's place in the district; other rites; Paramāra festival culture as distant frame) → 9.4 the town that narrates itself (tellers; the founder's tales against the record; Bhoja and Udayāditya in folk memory; the Garhi's threads) → close on the deserted village of Daulatpur, which hands to Ch 10.

**Scope.** *Chronological:* Paramāra-period Malwa society (as described in scholarship, labelled regional) set beside the village at the last record (c. 2021); festivals and the fair as kept now; oral tradition as told now about every period. *Geographical:* the village and its lanes, the temple, the Bhujariya Talab and the Garhi shrine; the district (the 1979 Gazetteer) where the village has no item. The chapter is short by design (U2: about 2,800 words; never pad).

**Editor's merge rulings carried into this plan** (from the master outline):
> **Editor's merge rulings for Chapter 9** (these override the entry below where they differ)
> - **Length:** ~2,800 words, below the 3,200 floor by design. This needs the user's ruling (Part I, I.7). **Never pad.**
> - **C09-GAZ-011 (Kham Baba) is not Udaypur:** it is the Gazetteer's Bes/Besnagar entry. It is excluded.
> - **No counts from Tiwari:** the "eight thousand", the Muslim share "one to one-and-a-half thousand", "three Jain families" and the police are all excluded. Households are described by community, never by residents' names.
> - **Survival legends** are not retold or analysed here (tested in 10.3). The Berni Mata versions are this chapter's (9.4 P2).
> - **Last paragraph:** the remembered deserted market of Daulatpur, as memory, with no location.

## 9.1 Neighbours in one lane *(communities, then and now · ~750 w)*

**Word target:** 750

- **Section statement:** By the end, the reader knows that Udaypur is a village of several faiths (Hindu, Muslim and a dwindling Jain presence), how the Paramāra-period society the town was founded into is described regionally (varṇa categories, Kāyastha scribes, Brāhmaṇa migrants from distant regions), that some local families remember identities remade in later centuries (a Muslim family claiming Paramāra descent; the Bagdi tradition of Rajput resistance), and that the only figures for religion and caste are the district's, for 1941 and 1961.
- **Purpose:** Describe the town's communities as far as evidence allows, with each layer marked, and say plainly where the record stops.
- **Paragraph plan:**
  1. **P1 — The lane and the claim.** **Point:** Open on the lane (above). Tiwari argues that the Muslims of Udaypur descend from the same people (craftsman, guard, trader, courtier, priest) who shaped the town under Udayāditya, and that "identity too was broken" like the images. Give this as his argument about belonging (a claim about descent that no record tests); the survey's plainer statement is that people of all religions live in the village, among Jain, Muslim and Hindu antiquities. Do not give Tiwari's population or Muslim headcount (map conflict "population of Udaypur": the census figure, told in 1.1, stands).
     - E: C09-JAGTA-HI-005 (T8), C09-GEOHER-001 (T7) · C: C09-JAGTA-HI-002 (T8) · Note: C09-JAGTA-EN-001 (T8) (English version of the claim; its figures are not to be used)
  2. **P2 — The society the town was founded into.** **Point:** Paramāra-period Malwa is described as a society of Brāhmaṇas, Kṣatriyas, Kāyasthas, Vaiśyas, Śūdras and Tailakas, with the Brāhmaṇa highest. Kings granted land to Brāhmaṇa families who had come from distant regions (Bengal foremost in one grant, also Magadha, Lāṭa and Madhyadeśa), and Kāyasthas of the Valabha subcaste wrote royal charters. Udayāditya and Naravarman declared their swords ready to protect *varṇa*: a dynastic claim, told as such. The treatise attributed to Bhoja assigns each *varṇa* a quarter of the town: a norm, not Udaypur's plan. At Udaypur itself the one local institution named in a record is the *panchakula* of Dhāmadeva's gift (recall 8.1 in a clause). The town's medieval population is otherwise unknown.
     - E: C09-GANGULY-001 (T5), C09-CII-001 (T1), C09-CII-002 (T1), C09-BHOJA-TIMES-003 (T5), C09-GANGULY-002 (T5) · C: C09-BHOJA-TIMES-002 (T5), C09-BHOJA-TIMES-004 (T5), C09-RAJABHOJ-EN-001 (T9) · X: C08-JAGTA-EN-012 (T8) (recall) · Note: C09-BHOJA-TIMES-001 (T5) (Alberuni's sixteen castes), C09-SAMAR-1-001 (T4) (house sizes by *varṇa*: ⚠ old OCR, paraphrase only, attribution doubted)
  3. **P3 — Identities remade.** **Point:** Two remembered changes of identity, both from testimony. A Muslim family told Tiwari that it descends from the Paramāras of Dhārā by way of a branch that went to Uttar Pradesh; when and why an ancestor became Muslim is not known (Tiwari supplies a general explanation of conversion under Muslim rule: keep that out of the narrator's voice). And Tiwari records a tradition of the Bagdis as a branch of local Rajputs who refused Muslim rulers' orders and lived here "in an organized way"; their descendants are still in the area. These are memories of descent and resistance, not dated events; Ch 10 owns the regimes. Omit Tiwari's remarks on the Bagdis' present caste registration (his opinion on a living community; see flags).
     - E: C09-JAGTA-HI-003 (T8), C09-JAGTA-EN-007 (T8) · C: C09-JAGTA-HI-006 (T8), C09-JAGTA-HI-007 (T8) · Note: C09-JAGTA-HI-003 (T8) (the family's claim; homed also Ch 10)
  4. **P4 — The district's numbers and the Jain thread.** **Point:** The only figures are the district's. In 1961 about 89 per cent of the district returned as Hindu, 9 per cent Muslim and 1.5 per cent Jain; the 1941 census listed Teli, Chamar, Rajput, Kachhi and Brahman as the largest castes, after which caste was no longer enumerated; Scheduled Castes and Tribes were about 21 and 4 per cent in 1961. Udaypur's own composition is not recorded. One thread runs from stone to people: the town's Jain precinct (Ch 7) and a resident's statement to Tiwari that only a few Jain families remain (give no number; note). A shrine shared by Hindus and Muslims in the 1870s is already told (1.1): recall in a clause only if the paragraph needs the turn.
     - E: C09-GAZ-001 (T7), C09-GAZ-002 (T7) · C: C09-JAGTA-EN-002 (T8), C07-JAGTA-HI-015 (T8) · Note: C09-JAGTA-HI-004 (T8) (the resident's statement, Hindi), C01-PANDE-004 (T5) (recall: 1870s shared worship)
- **Drafting guidance:** No counts from Tiwari (population, Muslim share, number of Jain families). Graded confidence: "Tiwari argues"/"a family remembers" in notes; in the text, "is remembered as", "the village tells". Use "Muslim" in the narrator's voice; quote Tiwari's "kafir"/"slavery" vocabulary nowhere. Treat the *varṇa* claim as a claim. District figures always "in the district". Do not invent the town's quarters.
- **Transition:** These communities share a speech whose census names have changed more than the speech itself, and a record written in other tongues.

---

## 9.2 Speech and the written word *(languages · ~450 w)*

**Word target:** 450

- **Section statement:** By the end, the reader knows that the district's people speak Hindi (with Urdu the main minority language in 1961), that the local speech has been returned in censuses as Bundeli in 1908 and as Malwi from 1921, Malwi then all but vanishing from the returns after 1951, that the town stands where Bundeli and Malwi meet on Patil's dialect map, and that Udaypur's own record was cut in Sanskrit and later in Persian and in Hindi in Nagari. The reader also knows that no item records how Udaypur itself speaks.
- **Purpose:** A short bridge that states the evidence and its limit; the epigraphic languages are Ch 6's subject.
- **Paragraph plan:**
  1. **P1 — Speech in the census.** **Point:** In 1961 Hindi was the mother tongue of about 91 per cent of the district, Urdu of about 8 per cent, Marathi a small remainder, and thirty-three other speeches among under one per cent. The colloquial dialect was returned as Bundeli in 1908, as Malwi (most widely) in 1921 and still second in 1931 and 1941, and almost not at all in 1951 and 1961. Patil places Bundeli in the centre of northern Madhya Bharat and Malwi, a southern form of Rajasthani, as once the speech of almost the whole plateau. Udaypur, on the plateau's north-eastern edge, lies where the two meet (graded: "lies near the meeting of"; a reading of the map, not a record of its speech). The collapse of Malwi in the returns probably says more about how answers were classified than about what people spoke (interpretive; one clause).
     - E: C09-GAZ-003 (T7), C09-GAZ-004 (T7), C09-MADHYABHARAT-001 (T5)
  2. **P2 — The languages of record.** **Point:** At Udaypur the written record speaks other tongues: the praśasti and the grants in Sanskrit, pilgrims' notes in Sanskrit, Persian and Hindi, one of them in Nagari and the local dialect (recall 1.4 in a clause; Ch 6 owns them); a nineteenth-century school at Vidisha taught Hindi, English, Sanskrit, Urdu, Persian and Marathi, the languages of the district's administrations and faiths. The speech of daily life enters the record at Udaypur only through Tiwari's Hindi and the dialect phrases in pilgrims' notes. The Malwi oral literature about Bhoja (9.4) is the nearest record of the regional vernacular as literature.
     - E: C09-GAZ-005 (T7) · C: C06-GEOHER-007 (T7), C06-GEOHER-008 (T7) (the V.S. 1696 pilgrims' records, kept apart; home 6.4), C01-SERPENT-002 (T5) (recall, as cited in 1.4) (Sanskrit, Persian and Hindi across eight centuries), C01-GEOHER-010 (T7) (Turasadasa's note in Nagari and the local dialect, with C01-KB-GEOHER-006 (T7) in 1.4)
- **Drafting guidance:** **Accept ~400 words.** Do not assert that Udaypur speaks Bundeli or Malwi: no item says so (the old canon's "Hindi with Bundeli and Malvi" is unsupported at village level). Percentages rounded once, "in the district", with the census year. No discussion of scripts (Ch 6).
- **Transition:** In whatever speech, the town gathers on fixed days, and the greatest of them is the god's.

---

## 9.3 The god's days and the town's year *(festivals and fairs · ~650 w)*

**Word target:** 650

- **Section statement:** By the end, the reader knows Udaypur's ritual year as far as the evidence records it: the Śivarātri, the main festival, with a seven-day fair in February or March counted among the district's most important; the four Mondays of Śrāvaṇa; the Bhujariya rites after Rakṣābandhan, which may have given a tank its name; recitations of the Sundarkand at a village shrine on the Garhi. The reader also knows how the Paramāra court's festival culture is known (regionally, and not as Udaypur's), and that the Gazetteer's picture of festivals without caste distinction is a district generalisation.
- **Purpose:** Turn the fair already seen in 1.1 into a subject: its scale in the district, its calendar, its companions; and keep the medieval festival world in its place.
- **Paragraph plan:**
  1. **P1 — Śivarātri and the fair.** **Point:** The main festival of the year is the Śivarātri, when villagers from Udaypur and its neighbours line up before the temple from morning to evening; the Gazetteer lists a seven-day Śivarātri fair at Udaypur in February or March among the district's important religious fairs, and the "Shivratri Mahadeo Mela" at Udaypur among the most important of its 23 fairs, alongside Vidisha's Ramlila and the cattle fairs of Lateri and Ganj Basoda. In Tiwari's account people come from neighbouring districts and the day now requires large-scale policing (no number). Recall the yearly fair of 1.1 in one clause; the new content is its duration, its rank and its calendar. The four Mondays of Śrāvaṇa, around July, are the other days of Śiva's worship.
     - E: C09-GAZ-008 (T7), C09-GAZ-009 (T7) · C: C08-PANDE-011 (T5) (home 8.5: the fairs held at the temple), C08-JAGTA-HI-005 (T8) · Note: C08-JAGTA-EN-004 (T8) (crowd and police: never the count), C12-JAGTA-HI-035 (T8) (same scene, homed Ch 12)
  2. **P2 — Other days.** **Point:** The village also keeps rites that are not the temple's. The survey proposes that the Bhujariya Talab takes its name from the Bhujariya rites held the day after Rakṣābandhan, a festival of weight in central India and especially in parts of Bundelkhand ("probably", as the survey says). At a small shrine on the Garhi, installed by a local officer (Tiwari's account), groups from the villages gather to recite the Sundarkand, in the belief that remembering "Gadhi wale Babba" averts trouble. In the district at large the Gazetteer saw all castes take part alike in bathing festivals, bathing in and drinking the same water: a 1979 generalisation, to be given as the compilers' observation. Do not place the Bhujariya Talab (told 1.5/2.4; Ch 7 owns it).
     - E: C09-GEOHER-002 (T7), C09-JAGTA-HI-011 (T8) · C: C09-GAZ-006 (T7) · Note: C09-GAZ-007 (T7) (district marriage customs: omit unless needed), C09-JAGTA-HI-001 (T8) (recently laid green cloths and news of a *pīr*'s appearance: a new devotional practice reported by Tiwari with hostility; defer to Ch 12/Afterword, see flags)
  3. **P3 — The court's festivals, at a distance.** **Point:** The festival culture of the Paramāra court is known from texts and records elsewhere: the spring festival with plays, Diwali, eclipses and other observances; Bhoja's own works list folk and royal festivals of vows, seasons and crops; and a record of 1217 in a Śiva temple of the dynasty's Abu branch shows men vowing two days' festivity from the Śivarātri. None is recorded at Udaypur. The 1217 vow is the earliest dated Śivarātri festivity in the evidence, and it is not Udaypur's; do not imply continuity from it to the modern fair.
     - E: C09-RAJABHOJ-EN-002 (T9), C08-GANGULY-008 (T5), C08-GANGULY-009 (T5) · Note: C08-GANGULY-010 (T5) (a play staged at the investiture of a god with the sacred thread, Abu branch)
- **Drafting guidance:** No scene of the fair (1.1 did the approach; no crowds described beyond the record). Use the Gazetteer's own "Udaipur" spelling only inside quotation; narrator writes "Udaypur". "Probably" for the Bhujariya name, once. No Tiwari numbers. The Gazetteer's "no caste or sectarian differences" is the compilers' claim: attribute in the construction ("as the district's compilers saw it in 1979").
- **Transition:** The days are kept by the living; the past is kept by what the living tell, and Udaypur tells a great deal.

---

## 9.4 The town that narrates itself *(oral traditions and memory · ~950 w)*

**Word target:** 950

- **Section statement:** By the end, the reader knows who keeps Udaypur's memories (a family, the villagers whose folklore the survey recorded, the district's compilers, and one writer whose book is itself the town's fullest self-account), how the founder's stories attach to worshipped objects and how their versions differ, that one founding tale has twins elsewhere, that the Paramāra king of regional folk memory is Bhoja while Udaypur's tales name Udayāditya, and that the town remembers its later centuries through the Garhi as a place of extraction, rebellion, desertion and buried treasure.
- **Purpose:** Make memory the subject: not retelling legends but asking who tells them, what they attach to, and what they choose to explain.
- **Paragraph plan:**
  1. **P1 — The tellers.** **Point:** Name the kinds of keeper and what each keeps: the time-keepers' family (its own service, recalled from 8.5 in a clause); the villagers whose folklore the heritage survey recorded (the dancer, the Gond and Bhringraj traditions, a prison on the hill); the district's compilers, who recorded the Pisanhari tradition and noted that the building is much later (recall 1.4 in a clause; the point here is the Gazetteer correcting a tradition); and Tiwari, who gathers stories "heard from elders in the family … for generations" and says that from them one "can weave the fabric of an original story". His book is both the chief witness and an act of the town's narration. Say this once, plainly; no meta-commentary about "the book" beyond it.
     - E: C09-JAGTA-HI-010 (T8), C09-GAZ-012 (T7), C09-GEOHER-005 (T7) · C: C08-PANDE-012 (T5) (recall) · Note: C09-JAGTA-HI-010 (T8) (Tiwari's method in his words), C13-JAGTA-HI-036 (T8) (his invitation to writers to make the dynasties' stories into fiction and song: homed Afterword; useful for the note only)
  2. **P2 — The founder in the stories.** **Point:** The founding tales (the snake and the treasure, 1.1; Bhringraj's defeat and the Gond hills, 1.5) all give the place to Udayāditya, as the inscriptions do, but by conquest, rescue or reward rather than by a royal act of building (one clause each, no plots). The dancer tale (1.1) shows how versions grow: in the shortest, a thread across a reservoir, a fall, a *samādhi*, no king, and no telling how long the story has been current; in the survey's version, the court of Udayāditya, a promise of half a kingdom, spells that bind the soldiers' weapons, and the rope finally cut by a man of a low caste; one report gives the name as "Benji Maada" by a temple near the Udaysagar; and an expert who examined the image read it as a *yakṣa*. The tale has attached itself to a worshipped image and to a tank; the king enters only in the fuller version. Do not identify the tank as the Udayasamudra (map conflict; Ch 7). The Un parallel: an author studying Un notes that legends identical to Un's founding tale are current at Lalitpur and Udaypur, which makes it hard to credit any of them; founding tales travel.
     - E: C09-JAGTA-EN-003 (T8), C09-JAGTA-EN-004 (T8), C09-GEOHER-006 (T7), C09-GEOHER-007 (T7), C09-PARTEMPLES-001 (T5) · C: C09-INTACH-001 (T7), C09-GANGULY-004 (T5), C09-GEOHER-003 (T7), C09-GEOHER-004 (T7) · Note: C05-JAGTA-HI-012 (T8) (Narayan Vyas: a *yakṣa*), C09-JAGTA-HI-008 (T8) (Hindi version), C09-GANGULY-003 (T5), C09-GANGULY-005 (T5) (the snake legend's middle and end: recall only), name variants Berni/Bedni/Benji (ledger uses "Berni Mata", 1.1)
  3. **P3 — Bhoja's fame and Udayāditya's town.** **Point:** Across Malwa the Paramāra king of proverb, folk song and tale is Bhoja: he became the hero of stories in his lifetime; Malwi sayings ("Where is King Bhoj, and where is Gangu the oilman") and devotional songs name him; Dhārā has its own folk explanations of stones and pillars as the oil-woman's weights; "Bhoja-vidyā" came to mean conjuring. Udaypur's tales, by contrast, name Udayāditya and no one else. The town's memory is local in its king. Keep to the contrast; the proverb's etymology (Gāṅgeyadeva, Telaṅga) is Rajpurohit's interpretation: note only.
     - E: C09-RAJABHOJ-EN-003 (T9), C09-RAJABHOJ-EN-005 (T9), C09-BHOJDEV-HI-002 (T9), C09-BHOJDEV-HI-004 (T9) · C: C09-RAJABHOJ-EN-004 (T9), C09-RAJABHOJ-EN-006 (T9), C09-RAJABHOJ-EN-008 (T9), C09-BHOJDEV-HI-003 (T9) · Note: C09-RAJABHOJ-EN-007 (T9) (the proverb read as history: Rajpurohit's view)
  4. **P4 — The Garhi's threads (closing).** **Point:** The later centuries are remembered through the Garhi, and Tiwari gathers the tellings as "threads": the Garhi as a dacoits' stronghold whose demands were met at once; a village named Daulatpur below it, now deserted, where markets were once held, with other vanished villages known only by name; the Bagdis' defiance (recall 9.1); a tax-taking ruler whom Tiwari conjectures from a worn name may have been a "Gyasuddin", seen by villagers as a looter rather than a king (his conjecture: note); treasure-seekers who dug the Garhi and mostly went mad, with tales of a few who found wealth. The survey adds a tradition that the hill served various dynasties as a prison, with chains, which it says needs confirmation. These memories share a subject: power as demand and refuge, and places emptied. They name no date and no checkable ruler. End on Daulatpur's vanished market: the memory of decline that Ch 10 tests against the record of regimes.
     - E: C09-JAGTA-EN-005 (T8), C09-JAGTA-EN-006 (T8), C09-JAGTA-HI-012 (T8), C09-GEOHER-005 (T7) · C: C09-JAGTA-EN-008 (T8), C09-JAGTA-HI-013 (T8) · Note: C09-JAGTA-EN-008 (T8) (the "Gyasuddin" conjecture), C09-JAGTA-HI-009 (T8) (treasure-hunting belief; Tiwari's view that inscriptions have nothing to do with treasure: Ch 11/12)
- **Drafting guidance:** Recall each Ch 1 legend in a clause at most; the analytical move (versions, attachment to objects, travelling tales) is new. "The village tells", "is said to", "Tiwari gathers": graded for tradition; never a tradition stated as event. The dancer version's "Harijan" is the survey's word: paraphrase as "a man of a low caste" or omit; do not reproduce it in the narrator's voice. Never write that the hill *was* a prison. Do not link the dancer to the district's *ral* dancers called *bednis* (C09-GAZ-015 (T7)): compatibility is not identity; the name echo is for the editor's flag only. No aphorism on "memory versus history" to close; end on Daulatpur.
- **Transition (into Ch 10):** The deserted market below the Garhi is the town's own account of decline; Chapter 10 sets it against what the record shows of the regimes that followed the Paramāras.

## Chapter 9: conflicts to present, unresolved

| Conflict | Where | How held |
|---|---|---|
| Berni / Bedni Mata versions: court dancer, thread-dancer, *yakṣa* (Vyas), "Benji Maada" | **9.4 P2 (home)** | Versions side by side; the *yakṣa* reading in a note; ledger spelling "Berni Mata" |
| The dancer and the district's *bednis* (*ral* dance) | 9.3/9.4 | Not linked |
| The founder in the stories vs the inscriptions | 9.4 | The traditions give the place to Udayāditya by other means; Bhoja is the folk hero of the region, not of Udaypur's own tales |
| Udaysagar / Udayasamudra (the dancer's tank) | 9.4 | Not named the Udayasamudra (7.5's question) |
| Survival legends | 1.4 told / 10.3 tests | Not used here |

## Chapter 9: hand-offs

- **In:** The lane on the left as one leaves the temple: in Tiwari's account, a Muslim household, then others, Hindu and Muslim, side by side, and Tiwari's claim that the ancestors of all of them together built the monuments a thousand years ago (C09-JAGTA-HI-005). It takes up Ch 8's last line (the time-keepers' family and its hereditary claim) by moving from one family's memory of its place to a whole lane's. **Do not list the residents' first names**; describe the households by community only (privacy; the names add nothing historical). Tiwari's claim is testimony about belonging, not a fact about the eleventh century.
- **Out:** it ends on the deserted village of Daulatpur where markets were once held. It must not announce Ch 10, summarise the chapter, or moralise about memory.

## Chapter 9: changes from the master outline

1. **Length (U2):** about 2,800 words, accepted.
2. **Exclusions:** C09-GAZ-011 (Kham Baba is Besnagar), and Tiwari's counts ("eight thousand", the Muslim share, "three Jain families", the police). Households are described by community, never by residents' names.
3. **The green-cloth / *mazār* passage:** not used here (Part I: 12.4 at most, omitted by default).
4. **Evidence pass:** the coverage is complete. No structural change.

## Chapter 9: research and verification flags

- C09-GAZ-011 (Kham Baba) is not Udaypur.
- Tiwari's counts.
- Bagdi remarks (C09-JAGTA-HI-007).
- Green cloths and the *pīr* (C09-JAGTA-HI-001).
- The dancer's name and the *bednis*.
- Map conflict "Bedni/Berni Mata legend"
- Map conflict "Udayasamudra tank: identification":
- Map conflict "temple survival legend":
- Map conflict "town founder / foundation":
- C09-PARTEMPLES-001:
- The quarters (old canon 14.1: Shikari, Mahua, Chaudaryana, Sarenthi, Utranti; Hajariya Mahadev)
- Languages of Udaypur itself:
- C09-GANGULY-002
- Staged sources
- **Page-image check:** Adhikari's footnote on "identical legends" at Udaypur (C09-PARTEMPLES-001).
- **Gaps (state, do not fill):** no item on the languages of the village itself; no item naming the town's quarters.
- **Free local search (`kb-new`, if the section lands short):** the corpus Markdown for Udaypur festivals and fairs beyond the Gazetteer's district lists.

---

# Chapter 10. Political Change and Economic Decline: Udaypur under Successive Regimes

**Planned words:** 4,200 (10.1: 800 · 10.2: 850 · 10.3: 900 · 10.4: 800 · 10.5: 850). **Evidence:** `evidence_index/ch10.jsonl`.

**Historical question.** What did each change of regime between the 1090s and the 1900s actually alter in Udaypur's rank as a seat of government, as a recipient of patronage, and as a settlement? And is "decline" a description the evidence supports, or one the town's later smallness reads back into its past?

**Through-line.** By the end, the reader knows that Udaypur was not destroyed by one conquest but lowered in rank, step by step over six centuries, from eastern seat and royal residence to *qasba* to large village, while each new power still invested in it, and that the town's economic decline, as distinct from its political demotion, is an inference the surviving evidence cannot yet date.

**Arc.** **Arc:**
- **10.1** A seat that changed hands (c. 1093–c. 1190): Udaypur's administrative function survives the Paramāra collapse and passes to Chandella and Caulukya hands.
- **10.2** A king's residence on a shrinking frontier (c. 1190–1305): the reunited house uses Udaypur as residence and endows its land, while Delhi, the Yādavas and Gujarat erode the kingdom.
- **10.3** An end that took decades (1305–c. 1530): the last Paramāra-titled record, the Tughluq mosque and the Malwa Sultanate. New rulers install themselves *in* the town; Hindu patronage and record-making go on.
- **10.4** A *qasba* of Sarkar Chanderi (1528–c. 1720): the Mughal town is integrated, endowed and demoted at once.
- **10.5** Revenue, brass and the railway (c. 1720–1905), and what "decline" means: Maratha and Gwalior administration, the brass cover, famine, the railway, and the Gazetteer's sentence. The chapter's verdict on decline closes the section.

**Scope.** *Chronological:* from Naravarman's accession (1094) to the Gazetteer's description (1979), with the sequence c. 1093–1905 carrying the argument: the later Paramāras and the Caulukya interval (10.1), the reunited house to 1305 (10.2), the Sultanate to c. 1530 (10.3), the Mughal *qasba* to c. 1720 (10.4), and Maratha and Gwalior administration to the railway (10.5). *Geographical:* Udaypur's temple and town, the Bhilsa district, Malwa, and the Mughal *sarkār* of Chanderi; the chapter widens where the documents stop naming Udaypur, and says so.

**Editor's merge rulings carried into this plan** (from the master outline):
> **Editor's merge rulings for Chapter 10** (these override the entry below where they differ)
> - **Opening (replaces the entry's "Opening move" and 10.1 P1):** **10.1 P1, "A Gujarat king named at Udaypur."**
>   - **Point:** Open on the inscription at Udaypur dated V.S. 1220 (1163). It shows the place governed by the *mahāsādhanika* Rājyapāla while Kumārapāla of Aṇahilapāṭaka, a Caulukya king of Gujarat, was reigning. It is the first stone at Udaypur to name a king of another house, about seventy years after the founder's last dated record.
>   - Pose the chapter's question from it: who held Udaypur after its founder's line, and did the town's rank change with its masters?
>   - Then step back to the 1090s (P2).
>   - Keep to ~120 words. 1.2 mentioned Rājyapāla without this context (Part I, C1-A), so the new information is the Caulukya reigning king. Do not retell 1.2.
>   - E: C10-PARTEMPLES-001, C10-CII-002 · C: C08-GANGULY-016 · Note: C06-GANGULY-034 (Ganguly's Kumārapāla record of 1163; possibly the same stone; not merged), C01-GANGULY-015 (Ganguly's "eastern division" framing, attributed).
> - **10.1 P4:** drop its first two bullets (now in P1); keep Vasantapāla's donation, Lūṇapasāka, Bhiraṅgāvalī and the Point ("the Caulukyas governed through it").
> - **10.3 P1:** introduce the V.S. 1366 Jayasiṃha record **fresh**, not as a "return to the opening doorway". Say once that it is inside the temple's east entrance (Ganguly's report).
> - **10.2:** Devapāla's two records appear in one clause each (texts in 6.4; the gift in 8.1).
> - **Survival legends:** this chapter is their testing ground (one cross-period paragraph in 10.3), against the record of the mosque and the surviving cult. C05-JAGTA-EN-003 (Vyas's "land of heroes") belongs with them, as memory.
> - **Palace founder and the farman:** home in 10.4.
> - **Brass cover:** home in 10.5; V.S. 1841, no conversion.
> - **Last paragraph:** the Gazetteer's "once a place of considerable importance". It must not mention Beglar.
> - **Length:** ~4,200 words planned.

## 10.1 A seat that changed hands *(c. 1093–c. 1190 · ~800 w)*

**Word target:** 800

- **Section statement:** By the end, the reader knows the following about the twelfth century.
  - Udaypur passed through at least four hands: the Paramāras of Dhārā, the Chandellas around Bhilsa, the Paramāra *mahākumāra* branch, and the Caulukya kings of Gujarat.
  - Under the Caulukyas it remained a provincial headquarters: Kumārapāla's *mahāsādhanika* Rājyapāla governed from it in 1163, and Ajayapāla's governor Lūṇapasāka granted a village to a god there in 1172/73.
  - The first great political defeat after the founding therefore changed Udaypur's master, but not its function.
- **Purpose:**
  - Open the chapter on its dated question (the east doorway; see Opening move).
  - Give the later-Paramāra twelfth century that chapters.md assigns here, but only as it touches Udaypur's rank.
  - Correct the impression left by §1.2/§1.3 that the governors at Udayapura in the 1160s–70s were Paramāra officers (see Flags).
- **Paragraph plan:**
  1. **P1 — A Gujarat king named at Udaypur.** **Point:** Open on the inscription at Udaypur dated V.S. 1220 (1163), which shows the place governed by the *mahāsādhanika* Rājyapāla while Kumārapāla of Aṇahilapāṭaka, a Caulukya king of Gujarat, was reigning: the first stone at Udaypur to name a king of another house, some seventy years after the founder's last dated record. Pose the chapter's question from it (who held Udaypur after its founder's line, and did the town's rank change with its masters?), then step back to the 1090s. About 120 words; 1.2 now names Rājyapāla with his Caulukya master (U1), so recall in a clause and add the question.
     - E: C10-PARTEMPLES-001 (T5), C10-CII-002 (T1) · C: C08-GANGULY-016 (T5) · Note: C06-GANGULY-034 (T5) (Ganguly's Kumārapāla record of 1163; possibly the same stone; not merged), C01-GANGULY-015 (T5) (Ganguly's "eastern division" framing, attributed)

  2. **P2 — A kingdom fraying at its eastern edge.** **Point:**
     - Naravarman's reign (known dates V.S. 1151–1190, 1094–1133) is where Paramāra disintegration begins, on Ganguly's reading.
     - The Betwā region, Udaypur's region, was "a bone of contest" with the Chandellas, and Madanavarman's Augasī grant issued from Bhilsa (1133/34) shows a Chandella court in residence beside Udaypur.
     - Recall 1.3's 1134 grant in a clause; the new work is the Betwā-frontier framing and the dates.
     - Grade: "on Ganguly's reading" for disintegration; CII for the dates.
     - E: C04-CII-133 (T1), C04-CII-136 (T1), C04-CII-135 (T1) · C: C04-GANGULY-125 (T5), C04-PARTEMPLES-012 (T5), C04-GANGULY-122 (T5) · X: C04-CII-142 (T1), C04-CII-148 (T1), C01-GANGULY-005 (T5) · Note: C04-GANGULY-123 (T5) (Ganguly's "degeneration of its military strength", attributed)
  3. **P3 — The branch that held the east.** **Point:**
     - After Jayasiṃha Siddharāja's capture of Malwa (1138 by CII; Ganguly dates the annexation between V.S. 1191 and 1193), Yaśovarman's sons fell back on the eastern districts around Bhopal and took territory back from the Chandellas.
     - The *mahākumāra* line that stayed there (Lakṣmīvarman, Hariścandra, Trailokyavarman as regent) issued grants from Vidisha itself in V.S. 1214 and 1216 (1157–59). It held the Mahādvādaśaka region (parts of Vidisha and Bhopal districts) "at least up to 1157".
     - Point for Udaypur: for some two decades the town's district was ruled by a junior Paramāra house with lesser titles, not by Dhārā. Rank of overlord falls; the district stays Paramāra.
     - Recall 1.3's names in a clause; new material is the location, the dates and the lower title.
     - E: C04-CII-146 (T1), C04-CII-149 (T1), C04-CII-150 (T1), C10-CII-002 (T1) · C: C04-CII-151 (T1), C06-CII-046 (T1), C04-PARTEMPLES-015 (T5), C01-KB-CII-008 (T1) · X: C04-CII-141 (T1), C04-GANGULY-129 (T5), C10-CII-001 (T1) · Note: C04-CII-141 (T1) vs C04-CII-176 (T1), C10-GANGULY-008 (T5) (1138 vs 1145 for the conquest; a range "1138–45")
  4. **P4 — A Caulukya headquarters.** **Point:** This is the section's core.
     - (P1 has given the V.S. 1220 record.) In 1163 one Vasantapāla made donations for the upkeep of a temple of Udaleśvara in the town.
     - After Kumārapāla's death, under Ajayapāla, Lūṇapasāka governed the province and granted Umaratha in the Bhṛṅgārikā *pathaka* to the god Vaidyanātha at Udayapura. An inscription of Ajayapāla stands at Udaipur (V.S. 1229).
     - Bhṛṅgārikā is probably modern Bhiraṅgāvalī, about 6 km north-east.
     - Point: the Caulukyas did not raze or abandon the Paramāra seat. They governed through it, and endowments to its temples continued under them.
     - **Documented** (tiers 1/5). State the Caulukya overlordship plainly. That Rājyapāla held "the eastern division" is Ganguly's framing: attribute it.
     - E: C10-PARTEMPLES-001 (T5), C10-CII-002 (T1) · C: C08-GANGULY-015 (T5) (home Ch 8: cross-reference), C08-GANGULY-016 (T5) (home Ch 8: cross-reference), C01-GANGULY-010 (T5), C06-CII-038 (T1), C01-GANGULY-015 (T5) · X: C04-ARTPAR-005 (T5), C04-PARTEMPLES-013 (T5) · Note: Lūṇapasāka's year, 1171/1172/1173 (C06-RAJABHOJ-EN-003 (T9), C01-GANGULY-010 (T5), C01-CII-010 (T1)), and the Gazetteer's attribution of a 1173 Bhṛṅgārikā record to Udayāditya (C01-GAZ-010 (T7)), which the book does not follow.
  5. **P5 — Recovered, and reunited.** **Point:**
     - After about a quarter of a century, Vindhyavarman restored Paramāra rule from Gujarat's hold (Ganguly; CII's "Gurjarocchheda").
     - Early in the thirteenth century a member of the *mahākumāra* branch, Devapāla, succeeded the main line at Dhārā. The house that had held the east in adversity now held the throne.
     - Close on the hinge: when the reunited kingdom next appears at Udaypur, it is with the king himself in residence (into 10.2).
     - No date for Udaypur's actual return to Paramāra hands exists in the evidence; say so in a clause.
     - E: C04-GANGULY-135 (T5), C04-CII-161 (T1), C04-GANGULY-134 (T5) · C: C04-CII-162 (T1), C04-CII-163 (T1) · X: C04-GANGULY-131 (T5), C04-GANGULY-133 (T5)
- **Drafting guidance:**
  - Compress the dynastic names hard. The reader met Yaśovarman, Lakṣmīvarman and Hariścandra in §1.3; give them as "the house's junior line" with one name each where a date needs an agent.
  - Narrate closely only P4.
  - Never call Rājyapāla or Lūṇapasāka Paramāra officers.
  - "Udaleśvara" is Ganguly's form: do not identify it with Udayeśvara (compatibility is not identity); flag.
  - Grade:
    - the Caulukya overlordship: established;
    - "headquarters of the eastern division": Ganguly's description;
    - Bhiraṅgāvalī: "probably".
  - No battle scenes.
- **Transition:** The house that kept the east through Gujarat's occupation took Dhārā early in the thirteenth century. Its king then resided at Udaypur and gave its land to the god, on a frontier now threatened from the north.

---

## 10.2 A king's residence on a shrinking frontier *(c. 1190–1305 · ~850 w)*

**Word target:** 850

- **Section statement:** By the end, the reader knows the following about Udaypur in the thirteenth century.
  - Udaypur reached its highest documented royal standing after the founding generation: the reigning king of Dhārā resided there and his reign endowed land to its temple (1229, c. 1232). An Udaypur record of 1255 also exists.
  - Over the same decades the kingdom's frontier was breached from every side: Iltutmish at Bhilsa (1233–34), Balban to Chanderi (c. 1250), Yādava and Vāghela attacks, and Alauddin Khalji's capture of Bhilsa in the early 1290s.
  - Udaypur's rank rose as the realm contracted.
- **Purpose:** Fill the century §1.3 passed through in four sentences, using the evidence §1.3 did not use: what the Devapāla records give, and how the frontier moved around Udaypur. Show that before 1305 the town was a frontier asset, not a casualty.
- **Paragraph plan:**
  1. **P1 — From prince's line to king.** **Point:**
     - Devapāla, of the *mahākumāra* line, succeeded Arjunavarman at Dhārā by 1218, perhaps uniting the two houses.
     - His earliest record bears both a feudatory's and a sovereign's titles.
     - The house whose base had been the east now ruled the whole, and Ganguly's reading of his and Arjunavarman's records puts the kingdom's eastern limit "at least as far as Udayapur".
     - Recall Devapāla in a clause (§1.3). New: the succession and the eastern boundary.
     - E: C04-CII-162 (T1), C04-CII-163 (T1), C04-GANGULY-137 (T5) · C: C04-CII-165 (T1) · Note: Tiwari's inference that Devapāla served at Udaypur as *mahākumāra* before his accession, making Udaypur a "centre" that produced two kings (C04-JAGTA-EN-071 (T8), C04-JAGTA-HI-068 (T8)). Attribute it as Tiwari's reading; it conflicts with Ganguly's report that the Udaypur record styles him Mahārājādhirāja (C01-GANGULY-016 (T5)). Not adopted.
  2. **P2 — What the king's records give.** **Point:** The section's core.
     - The 1229 record, in Tiwari's reading, gives four *biswa* of land to Udayeśvara by the treasury officer Dhamadeva.
     - The c. 1232 record, issued while the king resided in Udayapura, grants plots in villages, one probably "Dēvadharmapurī", which CII takes to be Udaipur itself, and another in Bhṛṅgārikā-64. Bhṛṅgārī is now named as the head village of the sixty-four, where the 1170s grant called it a *pathaka*.
     - Point: royal officers and the king endow the temple from the surrounding villages. The administrative grid of the 1170s is still working, and the grid itself had been reorganised.
     - Grade: the 1229 donor is reported only by Tiwari, from an inscription (tier 8 reporting tier 1): "according to Tiwari's reading". The c. 1232 content is CII (established). "Dēvadharmapurī = Udaipur": "probably".
     - E: C01-GANGULY-016 (T5) · C: C06-CII-040 (T1) (home Ch 6: cross-reference), C06-CII-038 (T1) (home Ch 6: cross-reference), C08-JAGTA-HI-013 (T8), C06-CII-046 (T1) · X: C01-KB-CII-012 (T1) · Note: C01-KB-CII-012 (T1) (the unit digit of 128[9] is indistinct)
  3. **P3 — Bhilsa lost and retaken.** **Point:**
     - In 1233–34 Iltutmish took the fort of Bhilsa and marched to Ujjain.
     - Devapāla's son's Māndhātā grant (1274) and a Vidisha inscription (1263) claim that Devapāla killed the "lord of the Mlecchas" near Bhilsa. CII reads this as the recapture of the town, which then stayed Paramāra for about half a century.
     - CII calls Iltutmish's operations "of a temporary nature"; Patil says they had "only a temporary effect".
     - Point: the district centre changed hands twice in a few years; the frontier, not the heartland, was where Udaypur lay.
     - Recall Iltutmish in a clause (§1.3). New: the recapture and its source.
     - Note: the "lord of the Mlecchas" is the praśasti's phrase; a panegyric claim, attributed.
     - E: C10-CII-003 (T1), C10-CII-007 (T1), C10-PARTEMPLES-002 (T5) · C: C06-CII-045 (T1), C10-GANGULY-002 (T5), C10-MADHYABHARAT-001 (T5) · X: C10-GANGULY-003 (T5) · Note: the date of Iltutmish's raid, 1233–34 (CII), 1234 (C10-GAZ-002 (T7)), 1235 (C10-JAGTA-EN-003 (T8)), 1239 (C10-GAZ-013 (T7)): use "1233–34"; Tiwari's statement that the raid fell in Mahlakdeva's time (C10-JAGTA-HI-014 (T8)) is an error, not followed.
  4. **P4 — Pressed from three sides.** **Point:**
     - About 1250 Balban overran the land up to Chanderi and Narwar, "the northern fringe of the Paramāra dominions". Yādava Kṛṣṇa attacked from the south, and the Vāghela Visaladeva sacked Dhārā.
     - CII proposes that the kings withdrew to Mandu as a stronger seat.
     - Jayavarman II still held Bhilsa in 1263 and Pathari in 1269 (recall in a clause).
     - An inscription of Sam. 1311 (1255) found at Udayapur is known only from Kielhorn's mention (Ganguly's footnote): content unknown.
     - Point: as the frontier closed in, the dynasty's centre itself moved; Udaypur lay between the new northern frontier and the new capital.
     - Grade: Mandu as refuge, "it is possible to hold" (CII's own phrase).
     - E: C10-CII-004 (T1), C04-CII-166 (T1) · C: C10-GANGULY-004 (T5), C01-KB-CII-014 (T1), C06-GANGULY-030 (T5) · X: C04-GANGULY-138 (T5), C10-PARMAR-RAJPUT-001 (T9) (omit in text; tier 9)
  5. **P5 — Bhilsa falls again.** **Point:**
     - In the early 1290s, under Mahlak Deva, Alauddin Khalji captured Bhilsa and sent its bronze images to Delhi in carts.
     - Ganguly and Patil both frame 1305, Mahlak Deva's defeat and ʿAin-ul-Mulk's governorship, as the formal end. Recall 1305 in one clause; §1.3 told it.
     - Close on what the sources do *not* say: no item records what happened at Udaypur in 1293 or 1305. Ganguly notes the Paramāra army still numbered thirty to forty thousand horse "on the point of extinction".
     - E: C10-GAZ-003 (T7), C10-MADHYABHARAT-002 (T5) · C: C10-GANGULY-005 (T5), C04-GANGULY-141 (T5) · X: C10-GAZ-013 (T7) · Note: the Bhilsa raid date, 1290 (C10-GAZ-013 (T7)), 1291 (C10-JAGTA-EN-003 (T8)), 1293 (C10-GAZ-003 (T7)): "early 1290s"; C10-TEMPLE-ECON-002 (T5)'s "1292" is excluded (Temple Economics is barred).
- **Drafting guidance:**
  - P2 is the paragraph to narrate closely; the rest compress.
  - Do not reuse Tiwari's polemical vocabulary about Iltutmish or Alauddin, and never quote it ("Islamic terrorist", "plunderers").
  - The narrator says "Muslim governor", "Delhi's sultan".
  - Minhaj's 105-*gaz* temple belongs to Bhilsa and to Chapter 3/7 context; not here.
  - Never say Udaypur was "spared" or "untouched": say the record is silent.
  - Introduce Balban, the Yādavas and Visaladeva once, by function, not with biographies.
- **Transition:** The formal end came at Mandu in 1305. The next records in the temple show that at Udaypur the end was neither formal nor quick.

---

## 10.3 An end that took decades *(1305–c. 1530 · ~900 w)*

**Word target:** 900

- **Section statement:** By the end, the reader knows that Paramāra Udaypur did not end in one stroke.
  - A Mahārājādhirāja Jayasiṃha was still recorded in the temple c. 1309–10.
  - The Tughluq mosque of 1336–38 inserted a new institution into the sacred precinct but left the main shrine in worship.
  - Under the Malwa Sultanate Bhilsa became a provincial capital. Udaypur received a mosque from an official in 1488, while Sanskrit record-making at the temple continued into the sixteenth century.
- **Purpose:** Replace "1305, then ruin" with a sequence of coexisting authorities. Do the analytical work on the mosque that §1.3 (fabric and dates) and §1.4 (legends) did not: what it shows about the new regime's presence and the old institution's survival.
- **Paragraph plan:**
  1. **P1 — The record after the end.** **Point:**
     - Introduce the record inside the temple's east entrance (fresh, not a return to an opening): Ganguly reads the V.S. 1366 record as Jayasiṃha (III), "probably the successor of Mahlak Deo", keeping "the banners of its independence … unfurled in Bhilsa", and adds "we know nothing further".
     - Point: some Paramāra-titled authority over the Bhilsa district outlived 1305 by at least four or five years, and it chose Udaypur's temple to record it.
     - Grade: "probably" for the succession. The record's existence rests on Ganguly's report; CII's edition is not in the map (flag).
     - This is the old canon's "1310 residual inscription": usable, but only as Ganguly's report.
     - C: C06-GANGULY-032 (T5) (home Ch 6: cross-reference), C10-MADHYABHARAT-002 (T5) · X: C10-JAGTA-HI-003 (T8) (Tiwari's guess that Paramāra kin held out last at Udaypur; memory, note only)
  2. **P2 — A mosque in the temple court.** **Point:**
     - Recall in one clause that a mosque with two Persian inscriptions of A.H. 737 and 739 (1336–38) replaced a corner shrine and the western hall (§1.3).
     - Then do the new work. Malwa was a Tughluq province until about 1401. The mosque was set *inside* the temple's own court, built of its demolished subsidiary shrines, with the main shrine left standing.
     - Read with Hardy's model: in conquest, desecration "set the seal" on rule, and later Muslim temple destruction was "largely a continuation" of that practice rather than iconoclasm. Islamic rulers also "initially adopted feudal structures similar to those of their predecessors".
     - The seal was set, and the shrine's cult continued.
     - Grade: the inscriptions and fabric are established; Hardy's frame is attributed as a general model, not applied by any source to Udaypur.
     - E: C10-MADHYABHARAT-006 (T5), C10-GAZ-014 (T7), C10-GAZ-004 (T7) · C: C07-PANDE-009 (T5), C07-GANGULY-003 (T5), C10-HARDY-002 (T5), C10-HARDY-001 (T5) · Note: the 1325 tradition and the survival legends (C10-PANDE-001 (T5), C10-GANGULY-006 (T5), C10-PANDE-002 (T5), C10-GANGULY-009 (T5), C09-MADHYABHARAT-002 (T5)), recalled from §1.4 in a note only. Tiwari's own caveat that one inscription does not prove who did the damage (C10-JAGTA-HI-005 (T8); C06-JAGTA-EN-037 (T8)) is the fairest summary of the attribution question.
  3. **P3 — Mandu's province.** **Point:**
     - Dilawar Khan declared Malwa independent c. 1401, and Hoshang Shah moved the capital to Mandu in 1405 (recall in a clause).
     - Under the sultans "Bhilsa was one of the provincial capitals … in charge of a governor". Udaypur is not named as one.
     - An agent of Sher Khan built a Mandu-style mosque outside Udaypur's eastern gate in 1488, under Ghiyas Shah Khalji (recall from §1.3).
     - New point: an official of the sultanate still found Udaypur worth a dated foundation with Persian *and Sanskrit* inscriptions, a bilingual public act.
     - Patil places Udaypur in a list of places whose Muslim monuments show the period's impact (Chanderi, Basoda, Udaypur, Bhilsa).
     - E: C10-MADHYABHARAT-005 (T5) · C: C07-MADHYABHARAT-012 (T5) (home Ch 7: cross-reference), C10-GAZ-004 (T7), C07-MADHYABHARAT-008 (T5), C07-INTACH-013 (T7), C01-KB-MADHYABHARAT-010 (T5) · Note: this "Sher Khan" is not Sher Shah Sūr (1540s); never merge them (Tiwari's sequence C10-JAGTA-EN-010 (T8) lists Sher Shah among the raiders). The canon's "do not import" warning conflicts with §1.3: §1.3 stands (see Flags).
  4. **P4 — The other track.** **Point:**
     - Sanskrit record-making and Hindu building at Udaypur continued under the sultans.
     - An inscription of V.S. 1562 (1505) at Udaipur gives Udayāditya a genealogy the CII editor rejects.
     - A sixteenth-century inscription calls the temple the most beautiful in India.
     - An archaeologist, from photographs, dates an unfinished rock-cut temple on the hill to the sixteenth century; this is Narayan Vyas's assessment as reported by Tiwari.
     - Point: the temple was a living destination, and the patrons of the sultanate period include people still inscribing in Sanskrit at Udaypur.
     - Recall §1.5's mention in a clause. The new work is the date and what it implies for patronage.
     - Grade: Vyas's date is "proposed".
     - E: C10-GANGULY-007 (T5) · C: C04-CII-131 (T1) (home 4.4: the V.S. 1562 record), C04-CII-132 (T1), C07-JAGTA-HI-027 (T8) · X: C10-PARTEMPLES-004 (T5) (Adhikari: with Paramāra decay temple building "suffered", small temples in a "degenerated style"; set against the Udaypur evidence)
  5. **P5 — Fought over, not named.** **Point:**
     - Between 1518 and 1561 the Bhilsa territory passed among Medini Rai and Salhadi, Bahadur Shah of Gujarat (who sacked Bhilsa in 1532), Qadir Shah, Puranmal, Sher Shah's armies (three months to cross the 120 miles from Chanderi to Bhilsa, 1543), Shujaat Khan's son and Baz Bahadur.
     - Give this as one sentence of succession, not a narrative.
     - Point: in half a century of documented struggle for the district, no item names Udaypur. The silence is itself evidence that Udaypur was now below the level at which chroniclers counted places.
     - E: C10-GAZ-005 (T7), C10-GAZ-006 (T7), C10-GAZ-010 (T7), C10-GAZ-012 (T7) · C: C10-GAZ-016 (T7), C10-GAZ-007 (T7), C10-GAZ-008 (T7), C10-GAZ-009 (T7), C10-GAZ-011 (T7), C10-MADHYABHARAT-003 (T5), C10-MADHYABHARAT-004 (T5)
- **Drafting guidance:**
  - P2 must not redescribe the mosque (Chapter 7) or retell the gunpowder or dream legends (§1.4); one note suffices.
  - Never quote Tiwari's characterisations of the Tughluq forces (C10-JAGTA-HI-028 (T8), -029, -006) or the "first introduction to Islam" claim; they are polemic.
  - P5 is a list compressed into one or two sentences. Resist explaining each ruler.
  - Hardy is cited for a frame, with "on Hardy's account".
- **Transition:** When Udaypur next appears by name in an administrative document, it is as a small unit of an empire's revenue map: a town of Sarkar Chanderi.

---

## 10.4 A *qasba* of Sarkar Chanderi *(1528–c. 1720 · ~800 w)*

**Word target:** 800

- **Section statement:** By the end, the reader knows the following about Mughal Udaypur.
  - Under the Mughals Udaypur was a *qasba* in Sarkar Chanderi of Suba Malwa, "the border of Gondwana", according to the only document that names it, a farman known through a modern translation.
  - In those decades it received a congregational mosque (begun under Jahangir, finished 1632) and, probably, a governor's residence.
  - A qazi family was given (or later claimed) rights over 84 villages.
  - The Mughal state integrated the town into its revenue and religious order at a lower rank than Bhilsa, which was itself reduced to a mahal headquarters.
- **Purpose:** Give the Mughal town its institutional shape (rank, office, endowment) without redescribing buildings (Chapter 7) or narrating the modern dispute (Chapter 11).
- **Paragraph plan:**
  1. **P1 — The empire's map.** **Point:**
     - Under Akbar the present district lay in the sarkars of Raisen and Chanderi, Suba Malwa.
     - Bhilsa was only the headquarters of a mahal of Raisen sarkar (40,816 *bigha*s; 60,94,970 dams; 480 horse and 1,000 foot); Sironj a mahal of Chanderi sarkar paying nearly twice as much.
     - Todarmal's settlement was extended here, and land divided into *khālsa* and *jāgīr*.
     - Point: the region's revenue centres are named and measured; Udaypur is not among them. Udaypur's own assessment is unknown (gap).
     - E: C10-GAZ-017 (T7), C10-GAZ-020 (T7), C10-GAZ-025 (T7) · C: C10-GAZ-034 (T7), C10-MADHYABHARAT-005 (T5), C10-MADHYABHARAT-004 (T5) · X: C10-GAZ-021 (T7)
  2. **P2 — The farman and its provenance.** **Point:**
     - First establish what the document is: a one-page Hindi translation, made in 2008, of a Persian text, headed "Documents of the Jama Masjid and Mahal Qubba Udaipura", presented by a lawyer before the tehsildar and passed to Tiwari.
     - Then what it says, as reported:
       - in Jahangir's time Auliya Ibn Abdul Samad laid the foundations of the mosque and the Mahal Qubba of "Udaipur, Sarkar Chanderi, Suba Malwa, the border of Gondwana";
       - both were half-built at the emperor's death;
       - worshippers were to remember Babur (Firdaus-Makani) and pray for the reigning emperor;
       - dated 10 Zilhijja 1041.
     - Grade throughout: "according to the farman as Tiwari reports it". Never as fact.
     - E: C10-JAGTA-EN-015 (T8), C10-JAGTA-EN-018 (T8), C10-JAGTA-EN-017 (T8) · C: C06-JAGTA-HI-023 (T8), C10-JAGTA-HI-037 (T8) · Note: C10-JAGTA-EN-018 (T8) vs C10-JAGTA-HI-033 (T8)/C10-JAGTA-EN-014 (T8) (founder: Auliya Ibn Abdul Samad per the farman, vs Jahangir himself per the 2021 claimant), and C07-GAZ-012 (T7) (mansion probably a local governor's residence)
  3. **P3 — Corroboration in stone.** **Point:**
     - The farman's A.H. 1041 matches the Persian inscription of the Shahi Masjid: begun under Jahangir, completed under Shah Jahan in 1632.
     - The mansion beside it is in early Mughal style, "probably" the local governor's residence (recall §1.3 in a clause).
     - Point: the one documentary claim that can be checked against an independent source checks out on date and reigns. This raises, without settling, the farman's credibility as a source for Udaypur's sarkar.
     - Udaypur's Chanderi Darwaza, the north gate named for the town it faces, is a fabric echo of the same orientation (Tiwari; Chapter 7 owns the gate).
     - E: C10-GAZ-023 (T7) · C: C07-MADHYABHARAT-011 (T5) (home Ch 7: cross-reference), C01-KB-MADHYABHARAT-002 (T5), C07-GAZ-012 (T7), C07-JAGTA-HI-008 (T8) · X: C07-GEOHER-031 (T7) (north gate altered "by the Muhammadans"; Chapter 7)
  4. **P4 — An office with land.** **Point:**
     - The claimant family's account, as Tiwari reports it: the mahal was given to the qazi's family so that they would lead prayers in the mosque, "along with the qaziyat of 84 villages".
     - That claim was the basis of possession into the twenty-first century.
     - Point: if any part is true, Mughal Udaypur's surviving institution was a religious office endowed with rights over a rural hinterland, which is the shape of the town's standing in the empire: a local centre of worship and adjudication, not of government.
     - Stop there; the eviction and the revenue record belong to Chapter 11.
     - Grade: "claimed"; no Mughal document for the 84 villages is in the evidence.
     - E: C10-JAGTA-HI-033 (T8), C10-JAGTA-EN-014 (T8) · C: C10-JAGTA-HI-032 (T8), C10-JAGTA-EN-020 (T8) · X: C07-JAGTA-HI-052 (T8) (revenue record: not private property; Chapter 11)
  5. **P5 — Aurangzeb at Bhilsa, and at Udaypur only in legend.** **Point:**
     - The documented Aurangzeb act in the district is at Bhilsa (1682): Vijay Mandir converted, the town renamed Alamgirpur, a name used only in official papers.
     - At Udaypur, Aurangzeb appears only in the survival legend (§1.4), which Patil and Pande set aside in favour of Tughluq.
     - Point: the record of Mughal-period destruction at Udaypur is empty. What the Mughals left there is a mosque, a mansion and an office.
     - E: C10-GAZ-018 (T7), C10-MADHYABHARAT-005 (T5) · C: C10-GAZ-024 (T7) · Note: C10-PANDE-002 (T5), C10-GANGULY-009 (T5), C10-MADHYABHARAT-006 (T5) (legend vs record; recall only)
- **Drafting guidance:**
  - P2 must describe the document's chain of custody before quoting any of it.
  - Quote at most the place-formula ("Sarkar Chanderi, Suba Malwa, the border of Gondwana"), attributed.
  - Never call it "the Shahi Mahal" (the canon's name). Use "the mahal" or "the Mahal Qubba (as the farman calls it)".
  - Tiwari's framing of Mughal officials as "occupiers" and "plunderers" (C10-JAGTA-HI-038 (T8)/-039) is not used.
  - Introduce *qasba*, *sarkar*, *mahal*, *khālsa*, *jāgīr* and qazi once each, with glosses.
- **Transition:** The Mughal order around Udaypur dissolved within a generation of Aurangzeb's death. The district passed through Afghan adventurers and Maratha generals to the Scindia state, whose patronage reached the shrine itself.

---

## 10.5 Revenue, brass and the railway: what "decline" means *(c. 1707–1905, and the verdict · ~850 w)*

**Word target:** 850

- **Section statement:** By the end, the reader knows the following.
  - In the eighteenth century the Bhilsa tract changed hands repeatedly among Bhopal's Afghan founders, the Kurwai nawabs (who held Basoda from 1713) and the Marathas, until it settled in Scindia's hands by 1775.
  - A Scindia general's gift of a brass cover to the *liṅga* shows a new regional power patronising a working shrine.
  - Under Gwalior, Udaypur lay inside a pargana-and-zila revenue machine.
  - In 1905 Udaypur was still the end-point of one of the district's only two metalled roads. Trade then moved to the railway stations, and Ganj Basoda grew.
  - The evidence supports a story of lost rank and shifted routes, not a datable economic collapse.
- **Purpose:**
  - Give the modern political sequence at the district scale where the evidence lies, compressed hard.
  - Then gather the chapter's four questions (rank, patronage, settlement, institutions) into a verdict on "decline".
- **Paragraph plan:**
  1. **P1 — Afghans, nawabs and Marathas.** **Point:**
     - After 1707: Dost Muhammad Khan took Bhilsa's fort by ruse.
     - Muhammad Diler Khan seized Kurwai in 1713, and his family held Basoda and Muhammadgarh by 1753.
     - The Marathas took Bhilsa in 1737 and 1745; it passed back and forth with Bhopal; it was firmly Maratha by 1765 and Scindia's by 1775.
     - Point: Udaypur sat on the seam between a nawabi Basoda and a Maratha Bhilsa. Which held the village is not stated in any item (flag). The Scindia gift (P2) suggests Gwalior: "probably".
     - E: C10-GAZ-027 (T7), C10-GAZ-028 (T7), C10-GAZ-032 (T7), C10-GAZ-033 (T7) · C: C10-GAZ-026 (T7), C10-GAZ-030 (T7), C10-GAZ-031 (T7), C10-MADHYABHARAT-008 (T5), C10-KBN-MADHYABHARAT-001 (T5), C10-KBN-MADHYABHARAT-002 (T5) · X: C10-GAZ-029 (T7), C10-KBN-MADHYABHARAT-003 (T5), C10-KBN-MADHYABHARAT-004 (T5) *(kb-new: Patil's regional account of the Maratha settlement of Madhya Bharat, 1730s–1790s, and the Maratha states under British paramountcy; free local search, verbatim, tier 5; regional frame only, never Udaypur-specific)*
  2. **P2 — A general's brass.** **Point:**
     - Recall the gift in one clause (§1.3): the brass cover with a face, given by Khande Rao Appaji, a general of Mahadji Scindia, "the local ruler".
     - New work: this is the first datable act of ruling-power patronage at the temple since the Paramāras, and it treats Udayeśvara as a living *mukhaliṅga* shrine. Patronage did not end with the Paramāras; it changed patrons.
     - Tiwari's "Garde Sahib" maintenance is recalled only as Tiwari's account.
     - E: C10-PANDE-003 (T5), C10-GAZ-038 (T7) · C: C08-MADHYABHARAT-008 (T5), C10-ARTPAR-001 (T5) · Note: the date conflict, V.S. 1841 (C08-MADHYABHARAT-008 (T5)) vs "1775" (C10-PANDE-004 (T5), C10-GAZ-038 (T7)), and the donor variant "Bappa Saheb" (C10-INTACH-001 (T7)). Keep §1.3's handling: V.S. 1841 as inscribed; flag that V.S. 1841 ≈ 1784–85, not 1775 (ROADMAP open issue).
  3. **P3 — Inside Gwalior's machine.** **Point:**
     - Mughal coinage persisted, the Marathas minting in the emperor's name.
     - The *jāgīr* system decayed; *ijāradārī* revenue farming gave way to zamindari contracts after 1843 and to 12-year leases from 1853.
     - Bhilsa zila was run by a *subah* with a *kamāsdār* in each pargana.
     - Bhilsa became a district in 1904 with Vidisha and Basoda tahsils.
     - Point: Udaypur now figures only as a village inside units named after other towns.
     - Compress to ~120 words.
     - E: C10-GAZ-019 (T7), C10-GAZ-035 (T7), C10-GAZ-050 (T7), C10-GAZ-039 (T7) · C: C10-GAZ-036 (T7), C10-GAZ-051 (T7), C10-GAZ-034 (T7), C08-GAZ-009 (T7) · X: C10-GAZ-037 (T7), C10-GAZ-040 (T7), C10-GAZ-044 (T7) *(evidence pass: C10-GAZ-041/-042 (1858–59) and -045/-046/-047 (Praja Mandal, Madhya Bharat, 1956) moved to Ch 11, per the outline's own cross-chapter notes)*
  4. **P4 — Famine, the railway and a feeder road.** **Point:**
     - The famine of 1899–1900 (*chappan kā sāl*) left empty houses in every village and diminished the labour supply. Gwalior's irrigation department (1905) was born of it.
     - The GIP railway (1905) put stations at Bareth and Basoda.
     - The district's only metalled roads were two feeder roads, one of them from Bareth station to Udayapura (6.4 km). Udaypur still drew a road.
     - With the railway, "trade centres … shifted to railway stations", and Ganj Basoda became a main trade centre. Sironj's prosperity had already declined with the Mughal empire.
     - Basoda pargana had 65,896 people in 1901.
     - Point: this is the only *documented* economic re-routing in the evidence, and it is late. Its beneficiary was Ganj Basoda, 13–16 km away.
     - E: C10-GAZ-049 (T7), C10-GAZ-055 (T7), C10-GAZ-054 (T7) · C: C10-GAZ-048 (T7) *(C10-GAZ-052/-053 census items moved to 12.1, per the outline's notes)*
  5. **P5 — "Once a place of considerable importance."** **Point:** The verdict. Suspend chronology. Lay out what the chapter has shown, under the four heads:
     - **rank:** lost in steps (Caulukya province → royal residence → post-1305 outlier → unnamed under the sultans → *qasba* → village);
     - **patronage:** never ceased, but changed hands (Caulukya governors, Paramāra king, Tughluq and Malwa officials, Mughal founders, a Scindia general);
     - **settlement:** undocumented until 1901;
     - **institutions:** the temple's cult and a qazi's office both outlasted every regime.
     - Set against this:
       - Tiwari's metaphor of an "orphaned" town (C10-JAGTA-HI-001 (T8)), given as memory;
       - Adhikari's decline of Paramāra patronage, true of the dynasty's art;
       - Hardy's report of the feudalism model (contracting trade, declining cities, land grants), a general hypothesis no source tests on Udaypur.
     - Land on the Gazetteer's sentence, with Patil's "a place of considerable importance … as is evidenced by the existing remains". Point: by the twentieth century Udaypur's importance had become something read off its ruins, which is where Chapter 11 begins.
     - E: C10-GAZ-056 (T7), C10-MADHYABHARAT-010 (T5) · C: C10-ARTPAR-002 (T5), C10-PARTEMPLES-004 (T5), C10-HARDY-003 (T5), C10-JAGTA-HI-001 (T8) · X: C10-JAGTA-EN-016 (T8), C12-JAGTA-HI-008 (T8)
- **Drafting guidance:**
  - P1 and P3 are compression paragraphs; resist the Gazetteer's battle narrative (Dost Muhammad on the elephant).
  - 1857–59 (Adil Muhammad Khan), the Praja Mandal, Madhya Bharat 1948 and the 1956 reorganisation get at most one clause, or are left to Chapters 11–12.
  - Do not quote Tiwari's "orphan" in a way that endorses it; present it as how the town's decline is remembered.
  - Graded wording: "probably under Gwalior".
- **Transition:** see Chapter Conclusion.

## Chapter 10: conflicts to present, unresolved

| Conflict | Where | How held |
|---|---|---|
| Udaypur under the Caulukyas (Rājyapāla, Lūṇapasāka): Ch 1 now corrected (U1) | 10.1 P1, P4 | Stated plainly; the political reading is this chapter's |
| The Caulukya conquest of Malwa: 1138 (CII) vs V.S. 1191–93 (Ganguly) vs 1145 | 10.1 P3 | "1138–45" |
| The 1163 Kumārapāla record (Ganguly) and V.S. 1220 (Adhikari) | 10.1 P1 | Cited together; not merged |
| Devapāla's title at Udaypur: Mahārājādhirāja residing at Udayapura (Ganguly reporting the record) vs "Mahakumar" (Tiwari) | 10.2 | Ganguly outranks; Tiwari in a note |
| The V.S. 1366 Jayasiṃha record (Ganguly only; OCR "1909") | 10.3 P1 | "probably" for the succession; Ganguly's report |
| The 1293 Bhilsa raid (1290/1291/1293) | 10.2 | "Early 1290s"; a Bhilsa event |
| Iltutmish (1233–34 CII vs 1234/1235/1239) | 10.2 | 1233–34 |
| Survival legends vs the record (the mosque of 1336–38, the surviving cult) | **10.3 (home of the test)** | One cross-period paragraph; legends as memory |
| Palace founder: the 1632 farman (a 2008 translation reported by Tiwari) vs the governor's mansion | **10.4 (home)** | The claim reported and attributed; claimants unnamed (U7) |
| Brass cover: Khande Rao Appaji vs "Bappa Saheb"; V.S. 1841 (not 1775) | **10.5 (home)** | V.S. 1841, no conversion |
| Who held Udaypur 1713–1948 (Gwalior vs Basoda/Kurwai) | 10.5 | "Probably within Gwalior's territory, to judge by the Scindia gift" |

## Chapter 10: hand-offs

- **In:** Open on the inscription at Udaypur dated V.S. 1220 (1163), which shows the place governed by the *mahāsādhanika* Rājyapāla while the Caulukya Kumārapāla of Aṇahilapāṭaka reigned (C10-PARTEMPLES-001, C10-CII-002): a dated record, after Ch 9's last paragraph ends in memory (the remembered deserted market of Daulatpur). The east door is not used (Ch 6 opened there). It must not open on a legend.
- **Out:** End on the Gazetteer's "once a place of considerable importance" as an official's *description*. Chapter 11 opens with the officials who made description their business: survey, protection, and the courts that would weigh the qazi's farman. - It must not narrate Beglar, Cunningham, ASI protection or the 2021–22 eviction. Those are Chapter 11's.

## Chapter 10: changes from the master outline

1. **Opening (Part I, I.5):** 10.1 P1 is now "A Gujarat king named at Udaypur" (the V.S. 1220 record). The east-door opening was dropped, since Ch 6 opens there. 10.1 P4 lost its first two bullets; 10.3 P1 introduces the V.S. 1366 record fresh.
2. **U1:** 1.2 and 1.3 now name the Caulukya governors, so 10.1 P1 recalls them in a clause and adds the question.
3. **U7:** no claimants named from the 2021 signboard (10.4).
4. **Evidence pass:** coverage complete; C10-GEOHER-001 (the fort's antiquities as Paramāra, a proposal) moved to 7.1 P4 as corroborating. No structural change.

## Chapter 10: research and verification flags

- Chapter 1 correction (high).
- The V.S. 1366 record
- Not in any map, do not use:
- The 1293 Bhilsa raid:
- Iltutmish's date:
- The farman
- Moti Darwaza mosque:
- Brass cover date:
- Who held Udaypur 1713–1948
- Tiwari vs Ganguly on Devapāla's title at Udaypur:
- "Udaleśvara"
- Kielhorn's Sam. 1311 (1255) record at Udayapur
- Gaps to state in text:
- Errors in sources, not followed:
- **BLOCKING CHECK before drafting 10.5: the brass cover's date, V.S. 1841** (≈ 1784–85, not 1775). The inscription or a reliable edition must be checked (ROADMAP 14). Flag it if still outstanding when Ch 10 is reached.
- **Page-image checks:** C06-GANGULY-032 (V.S. 1366, OCR "1909"); C06-GANGULY-030 (Kielhorn's Sam. 1311 record at Udayapura; content unknown).
- **Staged sources (leads, `ocr_verify`):** Beglar, ASR VII and Cunningham, ASR X, on the mosque inscriptions; after ingest only.
- **Legal review (U7):** the farman claim and the palace claimants (10.4): no names.

---

# Chapter 11. Udaypur in the Modern Period: Archaeology, Heritage Administration and Conservation

**Planned words:** 4,250 (11.1: 800 · 11.2: 850 · 11.3: 900 · 11.4: 800 · 11.5: 900). **Evidence:** `evidence_index/ch11.jsonl`.

**Historical question.** How did Udaypur become something that offices know, list, repair and own, and what did each of those acts do to the fabric, to the way the place is read, and to what is left out of the record?

**Through-line.** By the end, the reader knows that Udaypur was made known and protected in pieces: the temple first and best, the rest late, partly and by other hands. The shape of that custody explains both what scholarship says about Udaypur and what has been lost from it.

**Arc.** 11.1 (the 1870s–1880s: the temple enters print, and the first attribution is corrected) → 11.2 (the 1910s–1920s: a princely department finds, removes, restores and resets, and writes the description later scholars copy) → 11.3 (after 1947: who holds what; the one remembered clearance; what protection does not record) → 11.4 (2020–21: the first count of the whole town, and what kind of document it is) → 11.5 (the record of loss in the same years: encroachment, a revenue order, theft, vandalism, quarrying, a cracked repair) → close on what the archive of protection still lacks.

**Scope.** *Chronological:* from Beglar's tour (1871–72) to the INTACH documentation and the conditions recorded c. 2015–2021 (the evidence horizon is early 2021). *Geographical:* Udaypur's monuments and hill; Gwalior (the state department and museum); the ASI's Bhopal circle; the district administration. The chapter tells acts and findings, not remedies.

**Editor's merge rulings carried into this plan** (from the master outline):
> **Editor's merge rulings for Chapter 11** (these override the entry below where they differ)
> - **Opening:** Beglar, 1871–72, confirmed. Chapter 10's last line is the Gazetteer's 1979 description, not the brass cover. Chapter 11 does not restate the cover and begins directly with Beglar (the entry's contingency, now settled).
> - **The second slab's find-place:** home here, 11.2 P2 (Part I, I.3).
> - **No remedies:** illegal mining, the protection gaps and the missing translations are recorded as facts and threats to 2021. Proposals belong to the Afterword (AW.3).
> - **The 2021 lane widening:** one clause pointing forward. It is 12.5's.
> - **"Garde Sahib":** the lead only (open issue 20). M. B. Garde is introduced in full here, as Gwalior's Director of Archaeology, for the 1925–26 find.
> - **Last paragraph:** the people the record meets at its edges, with no recommendation.
> - **Length:** ~4,250 words planned.

## 11.1 Into the reports *(the antiquarian tours, 1871–1888 · ~800 w)*

**Word target:** 800

- **Section statement:** By the end, the reader knows that Udaypur first entered the written record of the state through two survey reports and an epigraphic edition. The first report described the temple's surroundings as already broken up and attributed the mosque to Aurangzeb. The second read the mosque's inscriptions and moved it to Muhammad Tughluq's time. Through these reports the temple became a standard example in later scholarship, so the attributions and plans of the 1870s still shape how Udaypur is read.
- **Purpose:** Ch 1 §1.4 gives one sentence to this ("Beglar … whose account Cunningham corrected … then Bühler's edition"). Turn it into an account of *what the reports did*: the record they made, the error they made and corrected, and the chain by which their plans and judgements passed into Kramrisch and Pande.
- **Paragraph plan:**
  1. **P1 — What Beglar set down.** **Point:** The 1871–72 tour report records the temple on a paved, raised platform. The walls with seats around the platform had long disappeared, except in the mosque at the back. Minor temples once stood around the great one, and "all of them" had "disappeared or been converted into" dwellings. This is the earliest dated condition record in the corpus. It shows the precinct already broken up and lived in, generations before any department protected it. Do not adopt Beglar's count of seven minor temples; Pande's eight is the canon figure and belongs to Ch 5. Say "minor temples" and put the count in a note.
     - E: C07-PANDE-005 (T5), C01-PANDE-012 (T5) · C: C11-PANDE-001 (T5) · Note: C07-PANDE-005 (T5) (Beglar's "seven") vs Pande's eight (Ch 5, canon)
  2. **P2 — An attribution, and its correction.** **Point:** Beglar's report tied the mosque behind the temple to Aurangzeb. This is the village tradition's attribution, told in Ch 1 §1.4. Cunningham's report of 1874–77 assigned the mosque instead to Muhammad Tughluq's time, on the strength of two inscriptions over the side doorways dated A.H. 737 and 739. He judged the west gateway, built of old materials, to be of the same date. The historical work has two parts. The correction came from reading inscriptions on site. It did not displace the tradition: Patil, writing later, still had to set the inscriptions against it. Recall the legend in a clause and do not re-tell it. The mosque as an event is Ch 10's.
     - E: C07-PANDE-008 (T5) · C: C07-PANDE-009 (T5) (home Ch 7: cross-reference), C10-MADHYABHARAT-006 (T5), C01-PANDE-003 (T5) · X: C11-GAZ-002 (T7) (Cunningham's survey of 1874–77 in the district) · Note: C07-PANDE-008 (T5) (the judgement that Beglar "made an error" is Pande's; attribute it)
  3. **P3 — Readings that became fixtures.** **Point:** Cunningham also gave the precinct a function. He called the *vedī* halls halls "for reading the Vedas" and recorded their dimensions. Beglar's praise of the floral carving, and Fergusson's of the temple's perfection, entered the standard history (Ganguly). One example, the *vedī*, is enough to show a survey's proposal hardening into description. The function itself is for Ch 5 to assess.
     - C: C05-GANGULY-012 (T5), C05-PANDE-008 (T5) (both homed in Ch 5; this paragraph recalls them as transmission, with no establishing item of its own) · Note: C05-PANDE-008 (T5) (the reading is Cunningham's; Ch 5 decides the hall's function)
  4. **P4 — From report to model.** **Point:** Through these reports the temple became a standard reference. Kramrisch's *Hindu Temple* (1946) cites Cunningham's volumes VII and X and the ASI annual report for 1923–24. Her plan of the temple, captioned "1059—1080", follows the survey plate, and she took the Udaypur temple as her model of the Bhūmija type. The plan, the dates and the type by which the literature knows Udaypur therefore run back to the survey of the 1870s and the epigraphy that followed (Bühler's edition of the *praśasti* in *EI* I, recalled from Ch 1 §1.4). Payoff: the town entered scholarship as one temple.
     - E: C11-KRAM-2-001 (T5), C05-KRAM-1-034 (T5), C05-PARTEMPLES-003 (T5) · C: C11-JAGTA-HI-005 (T8) (Tiwari's list of early notices: Cunningham VII and X; Bühler, *EI* I, 1888) · Note: C05-KRAM-1-034 (T5) (the "1059—1080" caption is a later scholar's dating, already flagged in Ch 1 §1.4; refer to it, do not reopen it)
- **Drafting guidance:**
  - Narrate P1–P2 closely. Let one short phrase of Beglar's ("converted into" dwellings) and Cunningham's dated inscriptions carry the paragraph.
  - Compress P3 to one example. P4 widens the scale from the reports to the field of scholarship.
  - Do not tell the Tughluq legend, the Aurangzeb dream or Bühler's content (Ch 1 §1.4, Ch 6, Ch 10).
  - Quote Beglar and Cunningham only through Pande's quotations until the staged ASR VII and X are ingested.
  - Fergusson is new: introduce him as the item does ("the well-known authority upon Eastern architecture"), in a note if the text cannot carry it.
  - The narrator writes "Muslim", never "Mohammedan", except inside quoted words.
- **Transition:** The reports read the stones where they stood. The next hands to reach Udaypur belonged to a princely state's own department, which did more than read: it lifted stones, carried one away and set others back in the wall.

---

## 11.2 A princely department at work *(Gwalior State, 1910s–1940s · ~850 w)*

**Word target:** 850

- **Section statement:** By the end, the reader knows that Gwalior State's archaeology department, under M. B. Garde, was the first agency to act on the fabric:
  - it found a second slab of the *praśasti* in a house in the town and took it to the Gwalior museum;
  - it noticed the town's inscriptions in its annual reports;
  - it ran restoration campaigns at the temple in the 1920s, one of which left its own inscription (V.S. 1985) and probably reset an inscribed slab inside out.

  Garde's descriptions passed, through his successor Patil, into the standard post-independence account. Before the department, care of the temple had been devotional patronage: the brass cover of V.S. 1841, recalled only.
- **Purpose:** Show the first *physical* interventions and the first *institutional* lineage of description, and settle what is and is not known about "Garde Sahib".
- **Paragraph plan:**
  1. **P1 — Before conservation.** **Point:** The last recorded act of care before the department was a gift, not a repair: the brass face-cover on the *liṅga*, given by Khande Rao Appaji in V.S. 1841. Give it one clause; Ch 1 §1.3 told it. The historical work is a contrast of kinds. Patronage added to the object of worship. From the 1910s the department would act on the fabric and on the record. Do not give 1775 (open issue 14).
     - E: C01-MADHYABHARAT-013 (T5) (recall) · C: C01-PANDE-011 (T5) · Note: C01-INTACH-006 (T7) (the survey names a different donor); the V.S. 1841 / 1775 discrepancy, with no conversion stated
  2. **P2 — Finding and removing.** **Point:** Gwalior's department noticed Udaypur's inscriptions in its annual reports; Tiwari cites the report for V.S. 1974 for the 1080 record. In the working season of 1925–26 Garde found the second slab of the *praśasti* "in a Dhimar's house near the Chatua Daruwāzā". He removed it to the Archaeological Museum at Gwalior, where it remains. The historical work is what removal did: it preserved and published the slab and also separated it from the town, so the dynasty's genealogy, carved at Udaypur, is now read in Gwalior. Ch 1 §1.4 told the find of 1925–26; the new material here is *where* the slab was found and *what moving it meant*. Add one clause of context: in 1923–24 the same department found an inscribed stone at Amera, about three kilometres south. The department was combing the neighbourhood, not only the temple.
     - E: C11-CII-001 (T1) · C: C11-JAGTA-HI-004 (T8) (report citations, as a lead), C11-CII-002 (T1) (Amera, as context) · X: C11-GAZ-001 (T7) (the department's 1914 excavations at Vidisha, with finds sent to Gwalior: the same pattern of removal) · Note: the find-place conflict (CII "Dhimar's house"; Tiwari "temple courtyard"; Ganguly "lying in front of the temple", the last probably the first slab). See Flags.
  3. **P3 — Restoring and resetting.** **Point:** The department ran restoration campaigns at the temple. Singh cites its reports for 1923–24, 1925–26 and 1928–29, followed by work under the ASI. The restoration of V.S. 1985 is recorded in the temple's own epigraphic sequence, which runs from the consecration of V.S. 1137 to that restoration. One inscribed slab in the outer parapet sits with its inscription turned inwards and its carved balustrade outwards, the reverse of the intact sections. Singh judges it likely that the stone was reset during one of these campaigns. The historical work: restoration made new evidence (a dated record) and altered old evidence (a slab's orientation and context). Ch 1 §1.4 gave the reset one sentence; here, explain what it means for reading the parapet.
     - E: C11-SERPENT-001 (T5), C01-SERPENT-002 (T5) · Note: C11-SERPENT-001 (T5) ("likely" is Singh's word; keep it). The equation V.S. 1985 ≈ 1928–29 is the book's inference; mark it as such.
  4. **P4 — "Garde Sahib" and the department's voice.** **Point:** In Tiwari's account the temple was maintained "under Garde sahib's supervision in the time of the Scindia royal house". Tiwari calls Garde Sahib "the archaeology officer of Gwalior's Scindia State". That supports the identification with M. B. Garde but does not prove it (open issue 20). More securely, Patil, Garde's successor, says his descriptions of Udaypur and nine other places were "substantially drawn" from Garde's *Archaeology in Gwalior*. The account of Udaypur that post-independence readers received is therefore, at one remove, a princely department's account. End on the bridge to 11.3: Madhya Bharat's list put Udaypur among the important monument places of Bhilsa district (told in 11.3).
     - E: C11-MADHYABHARAT-001 (T5) · C: C11-JAGTA-EN-010 (T8), C11-JAGTA-HI-011 (T8), C11-JAGTA-EN-003 (T8) · Note: C11-JAGTA-HI-001 (T8) vs C11-JAGTA-EN-003 (T8) (the interval "since Garde" differs between the Hindi and the translation; use neither)
  - **Evidence pass (X, optional by default; P0):** C10-GAZ-041 (T7), C10-GAZ-042 (T7) (1858–59 in the district), C10-GAZ-045 (T7), C10-GAZ-046 (T7), C10-GAZ-047 (T7) (the Praja Mandal, Madhya Bharat, 1956): moved from 10.5 at plan stage; state succession context for 11.2–11.3 (master outline flag: the Gwalior → Madhya Bharat → Madhya Pradesh transition had no item; these supply it)
- **Drafting guidance:**
  - Introduce him in full here, in CII's wording: "M. B. Garde, the Director of Archaeology in the former State of Gwalior". Ch 1 called him "Garde".
  - Keep "Garde Sahib" in Tiwari's words, in quotation marks, and say once that the identification is likely but unconfirmed.
  - Do not tell the *praśasti*'s content.
  - Do not call the brass cover a repair.
  - Keep Singh's "likely" on the reset.
  - State the department's reports only as CII and Singh cite them; the reports themselves are staged, not ingested.
  - The Amera stone is context only. Do not describe its content (Ch 6), and do not merge Amera with Udaypur.
- **Transition:** The department served a princely state. When that state was folded into Madhya Bharat and then Madhya Pradesh, its lists and its temple passed to new owners, and custody of Udaypur began to divide.

---

## 11.3 Protected in parts *(after 1947: lists, custodians and one clearance · ~900 w)*

**Word target:** 900

- **Section statement:** By the end, the reader knows four things.
  - After 1947 Udaypur appeared first on a successor state's list of monuments.
  - The temple came under the ASI at a date no source records. The one post-independence intervention any witness remembers is a clearance of houses and rubble around it, recalled by Narayan Vyas.
  - By 2021 custody had divided among the Centre (the temple; the Barah Khambi), the state archaeology department (a mosque, the Pisanhārī temple, the Naṭarāja), the forest department (the hill and its cave) and the revenue department (the palace ground).
  - Much of what the offices knew, above all the inscriptions, stayed in their files.
- **Purpose:** Replace the old canon's single "becoming protected" claim ("ASI protection covers the temple, not the hill") with the more complicated pattern the survey tables document. State the gap plainly.
- **Paragraph plan:**
  1. **P1 — On a new state's list.** **Point:** Patil's *Cultural Heritage of Madhya Bharat* counts 1,783 monuments on the State Archaeology Department's list. The 145 most important had been declared of national importance under the Ancient Monuments Preservation (Declaration of National Monuments) Act. His table for Bhilsa district (142 monuments in 26 places) names Udaypur among its places. The historical work: Udaypur's first post-independence status the corpus records came from a successor state's list, compiled by Garde's successor, before any central notification the corpus records. (That the list continued Gwalior's is a reasonable inference, not an item's statement: keep it as inference or omit it.) Say what the table shows (Udaypur among the listed places) and no more. It does not say which Udaypur buildings were listed or declared.
     - E: C11-MADHYABHARAT-003 (T5) · X: C11-MADHYABHARAT-002 (T5) · Note: the Act's name exactly as Patil gives it; the date of Patil's volume to be supplied from its title page (Flags)
  2. **P2 — The temple under the ASI, and the clearance.** **Point:** The temple is protected by the ASI; the survey volumes say so, and nothing in the corpus says when protection began. In Narayan Vyas's recollection, as Tiwari reports it, Vyas was sent to Udaypur at the start of his ASI service. Houses decades old then stood right against the temple on three sides. Their occupants were moved out with compensation, and rubble was cleared along those sides to expose the temple's foundation, which is visible today. Vyas called this the first major visible work since the ASI took the temple in. Two houses in front stayed and are still lived in. The historical work: the only remembered post-independence intervention *subtracted* the town from the temple. It also produced the cleared, raised platform visitors now see. Set Beglar's 1871–72 note of minor temples "converted into" dwellings (11.1) beside it as a comparison. The items do not say the houses Vyas saw were those structures: never merge them.
     - E: C11-GEOHER-001 (T7), C01-GEOHER-005 (T7), C11-JAGTA-EN-011 (T8), C11-JAGTA-EN-012 (T8) · C: C11-JAGTA-HI-012 (T8), C11-JAGTA-HI-013 (T8), C11-JAGTA-HI-032 (T8) (= C11-JAGTA-EN-033 (T8)) · X: C07-PANDE-005 (T5) (comparison only) · Note: Vyas's year (1972) and depth ("four feet") as his recollection via Tiwari, unconfirmed by any ASI record
  3. **P3 — Who holds what.** **Point:** The 2021 survey tables record protection building by building:
     - the Nīlakaṇṭheśvara (Udayeśvara) temple: ASI, condition "very good";
     - the Barah Khambi: ASI, centrally protected;
     - the Shahi Masjid: the state archaeology department, a mosque "restored with parapet stones in the past";
     - the Pisanhārī temple: the state archaeology department;
     - the palace: under "state administration" and protected by neither Centre nor state;
     - most other temples, the five gates and the precinct streets: unprotected;
     - the rock-cut cave: forest-department property, inside a protected forest where forest, archaeology, tourism and panchayat departments are all stakeholders;
     - the Naṭarāja on the hill: the survey calls it "protected".

     Tiwari's list of the state's four protected monuments (two mosques, the Pisanhārī temple, the Naṭarāja) matches the tables in kind. His count stays in a note. The historical work: custody followed building types and land titles, not the town. This corrects the old canon's "the temple, not the hill" (the Centre also holds the Barah Khambi; the state holds a figure *on* the hill). Recall Ch 1 §1.3's custody sentence in a clause and go beyond it with the table.
     - E: C07-INTACH-027 (T7), C07-INTACH-028 (T7), C11-INTACH-001 (T7), C07-INTACH-005 (T7) · C: C13-GEOHER-004 (T7) (home Ch AW: cross-reference), C07-GEOHER-059 (T7) (home Ch 7: cross-reference), C07-INTACH-006 (T7) (home Ch 7: cross-reference), C11-GEOHER-013 (T7) (Naṭarāja "protected"), C11-JAGTA-HI-006 (T8) / C11-JAGTA-EN-006 (T8) (palace unprotected), C07-JAGTA-HI-065 (T8) · Note: C11-JAGTA-EN-009 (T8) (Tiwari's four state monuments and the spending figures he reports from an unnamed official; give no figure in the text)
  4. **P4 — Knowledge in the files.** **Point:** Protection kept records more than it shared them. The inscriptions had long been "in the ASI's records". The historian Suresh Mishra retrieved Udaypur inscriptions, with English translations made long before, from the ASI archive. No Hindi translation of the Sanskrit inscriptions was displayed in the precinct. The ASI's regional director in Bhopal had charge of three states. In Tiwari's account, the district archaeology association met at Vidisha once in two to four years. Close on the gap, stated as a finding: the corpus contains no notification, no protected-area boundary, no date of central protection and no record of any repair to the temple after 1947 beyond Vyas's memory. Tiwari's verdict that independent India's governments should have read every inscription from 15 August 1947 is his and goes in a note. The proposals that follow from it (display of translations, staffing) belong to the Afterword.
     - E: C11-JAGTA-HI-003 (T8) (= C11-JAGTA-EN-004 (T8)), C06-JAGTA-HI-026 (T8), C11-JAGTA-HI-029 (T8) · C: C11-JAGTA-EN-008 (T8), C11-JAGTA-EN-035 (T8) · Note: C11-JAGTA-HI-010 (T8), C11-JAGTA-HI-033 (T8) (Tiwari's judgements on post-1947 governments, attributed), C11-JAGTA-EN-034 (T8) (ASI staff do not direct visitors to other sites)
- **Drafting guidance:**
  - Narrate P2 closely, but keep Vyas's memory framed as memory ("in Narayan Vyas's recollection, as Tiwari reports it"). Vyas was introduced in Ch 1 §1.1; give his ASI role here.
  - No date, depth or count from Tiwari in the text: not 1972, not "four feet", not "four monuments", not the rupee figures.
  - Lay out P3 as one orderly survey sentence or two, not a list in prose.
  - Do not describe the buildings (Ch 7).
  - Do not adopt Tiwari's or anyone's charge that funds were misdirected to mosques. If the editor wants the spending pattern in the book at all, it goes in a note, attributed to Tiwari's unnamed official, with a verification flag.
  - Keep "Udaysagar under cultivation" and the madrasa claim (C11-JAGTA-HI-036 (T8)) out of this section.
- **Transition:** The offices held their separate pieces. The first attempt to see the whole town at once came from outside them, from a citizens' campaign and a non-governmental trust.

---

## 11.4 Counting the town *(the INTACH documentation, 2020–2021 · ~800 w)*

**Word target:** 800

- **Section statement:** By the end, the reader knows that in 2020–21 INTACH's Bhopal chapter documented Udaypur as a whole for the first time, prompted by a citizens' campaign rather than by any department. It produced two volumes: *The Architectural Splendor of Udaypur* (2021), a listing of about fifty heritage sites with protection status, condition and grade, and *Geo-Heritage of Udaypur*, a survey of the hill. It recommended, and said it had begun to seek, notification of the hill complex as a protected site. The reader also knows what kind of document this is: a survey whose dates are proposals and whose counts vary between tellings.
- **Purpose:** Present documentation as itself an intervention, the old canon's "documentation as an act", and establish the 2021 volumes as the source that the rest of the book's survey evidence comes from.
- **Paragraph plan:**
  1. **P1 — A campaign, not a programme.** **Point:** The survey began with a campaign. Early in 2021 the historian Suresh Mishra and Tiwari (as a state information commissioner) walked the town and published what they found. News of the effort reached INTACH, a non-governmental trust for monuments, whose Bhopal convener, Madanmohan Upadhyay, was a retired IAS officer. INTACH hosted a presentation on Udaypur in Bhopal and then sent a team. The historical work: the first whole-town documentation was occasioned by publicity, not by any listing process. That shaped what it attended to, beginning with the palace. Keep Tiwari's role factual and brief. He is the author of the testimony, so name the campaign without letting it narrate itself as heroic.
     - E: C11-JAGTA-HI-038 (T8), C11-JAGTA-EN-013 (T8), C11-JAGTA-HI-015 (T8), C11-JAGTA-HI-021 (T8) · C: C13-JAGTA-HI-021 (T8) (the Bhopal presentation), C11-JAGTA-HI-017 (T8) · Note: C11-JAGTA-HI-001 (T8) / C11-JAGTA-EN-003 (T8) (Tiwari's judgement that this was the first attention "at this level" since Garde, attributed)
  2. **P2 — The fieldwork.** **Point:** A small, technically trained team camped in Udaypur until the work was done. The district administration was told the team would need local revenue officers: listing ruins meant reading land records. The team measured the palace's underground chamber. In Tiwari's account it went into every lane and ruin, identified remains from every period of the town's history and counted and documented the inscriptions. The historical work: documentation required the revenue map as well as the measuring tape. That links the listing to the land question in 11.5.
     - E: C11-JAGTA-EN-014 (T8), C11-JAGTA-EN-015 (T8) · C: C11-JAGTA-HI-016 (T8), C11-JAGTA-HI-018 (T8), C11-JAGTA-HI-020 (T8) · Note: team size and days on site are Tiwari's figures; keep them out of the text
  3. **P3 — What the volumes record.** **Point:** INTACH's documentation identified about fifty heritage sites "built more than 1000 years ago" (the survey's own phrase; mark it as the survey's dating). It was published in 2021 as *The Architectural Splendor of Udaypur*. That book's appendix tabulates each site with category, period, protection status, condition and grade, and the *Geo-Heritage* volume uses it as its base document. The second volume surveyed the hill: drone flights to see caves that could not be reached on foot, and lichens identified with the National Institute of Lichens. The historical work: the tables are the first official-looking record of the whole town's condition. They are also the source of 11.3's custody map. Give the counts of new monuments and inscriptions that Tiwari attributes to INTACH in a note only. The inscription-count conflict is Ch 6's.
     - E: C11-GEOHER-005 (T7), C11-GEOHER-006 (T7), C07-INTACH-026 (T7) · C: C07-GEOHER-059 (T7) (home Ch 7: cross-reference), C02-GEOHER-018 (T7) (drone), C02-GEOHER-024 (T7) (lichens; the dating proposal is Ch 7's) · Note: C11-JAGTA-HI-019 (T8), C01-JAGTA-EN-022 (T8) (Tiwari: "more than a hundred" inscriptions, "42 new monuments")
  4. **P4 — A list is not a notification.** **Point:** The survey argued that the hill's antiquities, along a 1,400 m stretch of fortification, should be conserved as a protected monument by notification. It reported that INTACH's Bhopal chapter had "initiated steps" to notify the complex as of national importance. No item records a notification. The historical work: the documentation did what the offices had not done (it saw the whole) but could not do what only they can do (protect). Its proposals for a geo-heritage park, guides, parking and monitoring are for the Afterword. Close the section on the survey's own words for the hill sites: "not protected".
     - E: C11-GEOHER-002 (T7), C11-GEOHER-003 (T7) · C: C11-GEOHER-008 (T7) · Note: tier reminder: a survey's dates are proposals (the "1000 years" and the period column)
- **Drafting guidance:**
  - Introduce INTACH once, in full ("the Indian National Trust for Art and Cultural Heritage"). Introduce Suresh Mishra (historian) and Madanmohan Upadhyay (INTACH Bhopal convener, a retired IAS officer) here for the first time.
  - Refer to Tiwari only as "Tiwari"; his full name was given in Ch 1 §1.1. His office as state information commissioner may be given once if needed, from C11-JAGTA-HI-038 (T8). No gendered pronouns.
  - Compress P1, the campaign's story, to a few sentences: Ch 12 and the Afterword use it too.
  - Do not quote the survey's superlatives.
  - "About fifty" is the survey's figure and may stand in the text; Tiwari's figures may not.
  - Keep the GEOHER volume's date unstated unless its title page gives one (Flags).
- **Transition:** The volumes listed what survived. In the same months, they and Tiwari's reports recorded what was being lost, and the one office that acted quickly was a revenue court.

---

## 11.5 The record of loss *(conditions c. 2015–2021, by kind of threat · ~900 w)*

**Word target:** 900

- **Section statement:** By the end, the reader knows what the record of 2020–21 documents as being lost, and through which gaps in custody:
  - the palace ground, claimed by a private-property board, recovered through the Land Revenue Code and still unprotected;
  - sculpture, stolen or defaced;
  - the hill and its fortification, damaged by quarrying, blasting, grazing and drainage failure, where the one recorded modern repair had already cracked.
- **Purpose:** This is the "conservation history from the afterword" that `chapters.md` moves here: the old Afterword's "documented deterioration", "illegal mining" and "protection gap" (AW.1–AW.3), treated as history up to the survey date. Remedies stay in the Afterword.
- **Paragraph plan:**
  1. **P1 — The palace and the revenue court.** **Point:** The palace's stone wall had been broken for a cement frame and an iron gate, under a signboard declaring "Private Property, Udaipur Palace, Ward No. 14, Khasra No. 822" in the names of a family of qazis. The board had hung for a long time. After the walk was publicised in January 2021, a tehsildar from Ganj Basoda visited. By the tehsildar's statement, the revenue record makes the palace ground no one's private property. A naib tehsildar's order of 15 January 2021, under Section 248 of the Land Revenue Code, evicted the occupant from 20 × 40 ft of Khasra 822, imposed a fine and set daily penalties. Within about two weeks the occupants handed over the keys. The historical work: the most effective intervention at Udaypur in the period was a land-revenue action, because the palace has no heritage status; it recovered ground, not protection. The order's text is a document that Tiwari prints (tier 4 via 8): give its date and section as the order's, attributed. Do not name the individuals beyond "a family of qazis" (C11-JAGTA-EN-022 (T8)). Who built the palace, and the Mughal *farmān* the claimants cite, belong to Ch 7 and Ch 10 (the "palace founder" conflict). The madrasa and the households belong to Ch 12.
     - E: C11-JAGTA-EN-016 (T8), C11-JAGTA-EN-017 (T8) (**U7: the signboard's names are never reproduced; say only that a private-ownership notice was hung**), C11-JAGTA-EN-019 (T8), C11-JAGTA-EN-024 (T8), C11-JAGTA-EN-025 (T8), C11-JAGTA-EN-026 (T8), C11-JAGTA-EN-027 (T8), C11-JAGTA-EN-021 (T8) · C: C11-JAGTA-HI-025 (T8), C11-JAGTA-EN-018 (T8), C11-JAGTA-EN-022 (T8), C07-JAGTA-HI-052 (T8), C11-JAGTA-HI-026 (T8) · Note: "Indian Land Revenue Code" as Tiwari prints it (verify: probably the Madhya Pradesh Land Revenue Code); the area of 3½ bighas as the tehsildar's statement
  2. **P2 — Sculpture: theft and defacement.** **Point:** During INTACH's visit an Uma-Maheśvara image had gone from its place. It was reported, and a theft report was entered in the police station's daily register only after the district police chief's office intervened. Tiwari describes images lying unowned in fields, forests and mounds around the town. Elsewhere in the district a Viṣṇu image had been recovered from smugglers and is now in the Vidisha museum (context, a different village). The survey records two kinds of vandalism: names scratched on carvings and the petroglyph, and older mutilation of figures in the Jain cave and on the Lajja Gaurī petroglyph. It also records new concrete steps cut into the reserve forest. The historical work: loss of movable sculpture is recorded only when a person reports it, and the unprotected hill shows both the old pattern of damage and the new.
     - E: C11-JAGTA-EN-029 (T8), C11-JAGTA-EN-031 (T8), C11-GEOHER-012 (T7), C11-GEOHER-013 (T7) · C: C11-JAGTA-HI-030 (T8), C11-JAGTA-EN-030 (T8) · X: C11-JAGTA-HI-035 (T8) (Sonari, context only) · Note: Interpol and repatriation figures (C11-JAGTA-EN-032 (T8)) not used
  3. **P3 — Quarrying, blasting and grazing.** **Point:** The survey names illegal sandstone mining as the most serious threat on the hill. It damages landscape and heritage. Quarries worked along the walls and bedding are a main cause of the fortification's decay, which decades of mining and lichen had begun and the last decade "dramatically accelerated". No mine exists on record, but blasts are heard, and they threaten the Naṭarāja and the wall. One hill site lies beside a privately owned quarry. Some residents fear blasts also endanger the temple (a belief, attributed). Livestock graze to the hilltop, damaging antiquities and causing erosion. Recall Ch 2 §2.5's illegal quarrying in a clause; the scale Tiwari reports (2,500 ha of forest land) goes in a note. The historical work: the hill's threats fall on land where the forest department, not any heritage office, is owner, and the protected Naṭarāja is exposed to an activity no heritage authority controls.
     - E: C11-GEOHER-007 (T7), C11-GEOHER-009 (T7), C11-GEOHER-013 (T7) · C: C11-GEOHER-008 (T7), C11-GEOHER-014 (T7), C11-JAGTA-EN-028 (T8) · Note: C02-JAGTA-EN-003 (T8) (Tiwari's figure, from a ground report by Govind Saxena)
  4. **P4 — A repair already cracking.** **Point:** The only modern repair to the fabric in the corpus is to the fortification. The INTACH team observed masons repairing a collapsed section of pitching, replacing original stone with new stone aligned to the old coursing. A crack had already appeared in a recently repaired section at the south-west corner. The survey's diagnosis: causes (water, in a wall built dry for an arid regime) had not been treated before effects. It urged clearing the drains before the monsoon and shoring precarious sections, warning of a risk to life. Report the urgency as the survey's finding; the programme is the Afterword's. The historical work: the hill's one documented repair repeats, on a small scale, the chapter's pattern of acting on the visible object rather than its setting.
     - E: C11-GEOHER-004 (T7), C11-GEOHER-011 (T7) · C: C11-GEOHER-010 (T7) · X: C07-GEOHER-018 (T7) (dry construction and seepage; Ch 7 describes the wall)
- **Drafting guidance:**
  - Tiwari's tone in these pages is polemical: on mosques and spending, on "erasure of identity", on green cloths and the madrasa. **Do not adopt it, quote it or paraphrase it as fact.** The text keeps to acts and documents: the board, the visit, the record, the order, the keys. A note may say that Tiwari's account frames the episode as a recovery of the Paramāra palace.
  - No Tiwari figure in the text except the order's own figures, attributed to the order.
  - The survey's "illegal" is the survey's word; attribute it.
  - Never invent agents: no "quarrymen", no "thieves" beyond what the items say.
- **Transition:** to the Chapter Conclusion. The record ends in 2021 with a list, a recovered plot of land and a cracked repair. What the archive of protection still lacks is the subject of the close.

## Chapter 11: conflicts to present, unresolved

| Conflict | Where | How held |
|---|---|---|
| The second slab's find-place: a Dhimar's house near the Chatua Darwaza (CII) vs the temple courtyard (Tiwari) vs Ganguly | **11.2 P2 (home)** | CII in the text; the variants in a note |
| Beglar's Aurangzeb attribution of the mosque vs Cunningham's reading | 11.1 | The historiographic layer only; the events are 10.3's |
| Who protects what: the temple (ASI), the Barah Khambi (ASI, per INTACH), the Naṭarāja (state, per the survey and Tiwari) | 11.3 | Stated as reported; no notification exists in the corpus (gap) |
| "Garde Sahib" = M. B. Garde? | 11.2 | A lead (open issue 20); "Tiwari's 'Garde Sahib'" |
| GEOHER-008's unprotected "site" (unnamed) | 11.5 | "One hill site" until checked |

## Chapter 11: hand-offs

- **In:** Open on the first printed description: Beglar's tour of 1871–72 and what he set down, a paved platform, minor temples "now disappeared or converted into" dwellings, and a mosque he attributed to Aurangzeb (C07-PANDE-005, C01-PANDE-012, C07-PANDE-008). This carries the chapter's question at once: the first official account both *recorded* the place and *mis-attributed* part of it, and the correction came from the next official account. It takes up Chapter 10's close by content: Chapter 10 should end with the town under Maratha (Scindia) rule, and Chapter 11 opens when that town is first written about by a government survey. (Settled at merge: Chapter 10 ends on the Gazetteer's description; begin directly with Beglar.)
- **Out:** End on the people the record keeps meeting at its edges: the households cleared from the temple's sides, the occupants who handed over the keys, the residents who report a stolen image. Chapter 12 takes them up as residents, not as encroachers or witnesses. The paragraph must **not** recommend anything (the Afterword's task), must not narrate the residents' lane-clearing of February 2021 (Ch 12, C12-JAGTA-EN-008/-014), and must not end on Tiwari's rhetoric of awakening.

## Chapter 11: changes from the master outline

1. **U7 (legal review):** the 2021 signboard is told as administration only, with no claimants named. Tiwari's mining allegation is not used in Ch 11 (it is Ch 12's one attributed sentence). The passages touching the eviction order and illegal mining are flagged for legal review.
2. **Merge correction:** the drone survey item is C02-GEOHER-018 (p. 140).
3. **Boundary:** the 2021 lane widening is one forward clause (12.5); remedies are the Afterword's.
4. **Evidence pass:** coverage complete. No structural change.

## Chapter 11: research and verification flags

- Gap: no ASI notification, boundary, date of protection or post-1947 repair record
- Brass cover date (open issue 14).
- "Garde Sahib" (open issue 20).
- Find-place of the second slab
- CII items that are not about Udaypur's temple.
- Gwalior report years.
- Staged sources, to be added after ingest:
- The Aurangzeb/Tughluq attribution
- Tiwari's figures and dates are kept out of the text:
- The eviction order
- Barah Khambi as ASI-protected
- GEOHER-008, "The site is not protected"
- State succession.
- Dates of the volumes.
- "Built more than 1000 years ago"
- Timing of the 2021 events.
- Excluded source.
- **LEGAL REVIEW before publication:** 11.4 (the eviction order, the signboard) and 11.5 (illegal mining as a threat).
- **Page-image checks:** the Gwalior report years (1923–24, 1925–26, 1928–29; "V.S. 1974"); the state Land Revenue Code cited in the 2021 order; GEOHER-008's site.
- **Staged sources (leads, `ocr_verify`):** Beglar, ASR VII; Cunningham, ASR X; Bühler, *EI* I; the Gwalior report of 1925–26. Until ingest, 11.1 quotes the reports only through Pande.
- **Gap:** no ASI notification, boundary or post-1947 repair record (say so once, 11.3).

---

# Chapter 12. Udaypur Today: A Living Community and Its Historic Environment

**Planned words:** 3,750 (12.1: 750 · 12.2: 650 · 12.3: 700 · 12.4: 800 · 12.5: 850). **Evidence:** `evidence_index/ch12.jsonl`.

**Historical question.** How do the people of Udaypur live with a thousand-year-old town that others visit as a monument, and whose account of that life does the evidence give us?

**Through-line.** By the end, the reader knows that Udaypur in the early 2020s was a working village living inside and on top of its medieval town and hill, that the temple's visitors and the town's residents rarely met, and that when residents did act on their heritage the record mostly describes them through outsiders' eyes.

**Arc.** Opening on one house → 12.1 living inside the fabric (the house, the numbers across seventy years, the ruins become homes) → 12.2 work: fields, the market town, the quarries → 12.3 the hill as a living environment (bats, vultures, birds; the 1968 shooting block; grazing, pilgrims, trekkers, blasts) → 12.4 the temple's Udaypur: worshippers, officials and the first walkers in the lanes → 12.5 the lane of 2021 and the question of who speaks for the town → close on residents' own hopes, handing the "what next" to the Afterword.

*Why this order:* it begins at the smallest scale (a household), widens to the village economy and then to the hill, then turns to the outsiders' view and finally lets the two views meet in one dated episode. Putting the wildlife third (not last) keeps the hill inside the chapter's argument about use and pressure rather than letting it read as a natural-history appendix; putting the lane last gives the chapter a dated event to end on and the Afterword a concrete hinge. The alternative order of the old canon (opening on Tiwari's "kasba on the margin") was rejected: it would make the chapter open on an outsider's lament and repeat 1.1's approach.

*Scale shifts:* household (12.1) → village and *tahsīl* economy, Ganj Basoda *mandi* (12.2) → the hill and the district's 1968 forest ranges (12.3) → Bhopal and the district officials (12.4) → back to one lane (12.5).

*Chronology:* runs only in 12.1 (1901 → 1950–51 → 1963–64 → 1971 → 2011) and in 12.3 (1948 → 1968 → 1979 → the survey). 12.4–12.5 are anchored in a dated cluster (January–March 2021). Elsewhere chronology is suspended; the present is "at the last record".

**Scope.** *Chronological:* the settlement as counted from 1901 to 2011, and life at the last record (January–March 2021; the evidence horizon, stated once in 12.1). The wildlife record runs 1948–1979, then the survey. *Geographical:* the old town's houses and lanes, the fields and the Ganj Basoda market, the hill (wildlife, grazing, pilgrims, quarry blasts), and the temple as visitors meet it. Communities are Ch 9's; recommendations are the Afterword's.

**Editor's merge rulings carried into this plan** (from the master outline):
> **Editor's merge rulings for Chapter 12** (these override the entry below where they differ)
> - **The 2021 lane widening:** home here (12.5), confirmed. Chapter 11 recalls it in a clause.
> - **Communities:** not described here (Chapter 9's). Livelihoods, use of the fabric, visitors and tensions only.
> - **The green-cloth / *mazār* passage:** the entry says it is "homed in Chapter 9"; Chapter 9's entry sends it here. **Ruling:** 12.4 may carry one neutral, attributed sentence (Part I, I.4), or omit it. It is omitted by default (Part IV, P0).
> - **Wildlife (12.3):** the "Udaipura" shooting block of 1968 is in the Gyaraspur Range and is **not** equated with Udaypur's hill. Check the table's columns before printing any number.
> - **Evidence horizon:** "today" means the last record, c. early 2021. Say so once, in 12.1.
> - **No recommendations.** The last paragraph ends on residents' hopes and outsiders' plans.
> - **Length:** ~3,750 words planned.

## 12.1 Living inside the old town *(the settlement, 1901 to c. 2021 · ~750 w)*

**Word target:** 750

- **Section statement:** By the end, the reader knows that Udaypur grew from a village of under two thousand people in 1901 to more than six thousand by 2011 inside the footprint of the medieval town, that it is governed as a gram panchayat, schooled since the 1950s–60s, and that much of its housing stands on, in or out of the old fabric.
- **Purpose:** Establish the present settlement as the latest layer of a town that has been continuously lived in and remade, without re-touring 1.1.
- **Paragraph plan:**
  1. **P1 — A home made from a ruin.** **Point:** Open on a household that cleaned out an old dwelling, found in an excavation decades ago and carrying fine carved work, and made it their home. Present it as the act of residents, not of any department, and as a pattern the rest of the section generalises. Attribute to Tiwari's account in one clause; do not name the family (the item does not); no invented details of rooms or carving.
     - E: C12-JAGTA-HI-014 (T8) · X: C01-KB-INTACH-001 (T7) (recall only: 1.1's twelve-courtyard house, one clause at most)
  2. **P2 — Seventy years of growth.** **Point:** Give the village's trajectory as documented: the 1979 Gazetteer records about 1,966 hectares and a population of 2,025 in 1971, against a 1901 figure printed both as 928 and 1,619; the 2011 census counted 6,383 (recall 1.1 in a clause, do not repeat sex ratio, literacy or houses). The village roughly trebled between 1971 and 2011. Set the district frame in one sentence only: rural population up 169% in 1901–71, district growth of 34.59% in 1961–71 (above the state average), put down by the Gazetteer to falling death rates. The 1901 discrepancy goes in a note.
     - E: C12-GAZ-008 (T7), C12-GEOHER-001 (T7) · C: C12-INTACH-002 (T7) (area 1,966 ha; 6,383 via villageinfo.in) · X: C12-GAZ-002 (T7), C12-GAZ-004 (T7) · Note: C12-GAZ-008 (T7) (928 vs 1,619 printed for 1901)
  3. **P3 — A village with an office and a school.** **Point:** Say what kind of place the state sees: a gram panchayat in the Basoda *tahsīl*, its primary school raised to a middle school in 1950–51 and to a higher secondary school in 1963–64, bringing the district's higher secondary schools to thirteen. This is the modern administrative layer laid over the old town (1.1 gave the 1979 school list; here only the upgrade dates are new). The Kurwai assembly constituency (Tiwari) may be stated, attributed.
     - E: C12-GAZ-005 (T7), C12-GAZ-006 (T7), C12-JAGTA-HI-005 (T8) · C: C12-INTACH-001 (T7) · X: C12-JAGTA-HI-004 (T8) (constituency only; **no distances from it**)
  4. **P4 — Patches of old and new.** **Point:** Generalise P1: in Tiwari's account history lies in the foundations of nearly the whole village; many ruins have been turned into pucca houses, and the joins between old and new are plain to any eye. Pair with the "living fabric" claim (C07-JAGTA-HI-051 (T8), homed Ch 7) only as a recall that the town still keeps its old plan. Close the section on the implication, labelled as the book's inference: the people of Udaypur have been its main builders since the eleventh century, and their houses are both the monument's encroachment and its continuity.
     - E: C12-JAGTA-HI-007 (T8) · C: C12-JAGTA-HI-006 (T8) (survival of old buildings "to a considerable extent"; **drop the "eight thousand"**) · X: C07-JAGTA-HI-051 (T8) (recall)
  - **Evidence pass (C, optional by default; P0):** C10-GAZ-052 (T7), C10-GAZ-053 (T7) (census items, moved from 10.5 at plan stage)
- **Drafting guidance:** Narrate P1 closely but briefly (it carries the chapter's question). Compress P2 to two or three sentences of figures; never "population grew from 6,383 to about 8,000". Introduce no new people. Do not use Tiwari's 150 km, 16 km, 22 km, 70 km or 5 km. Do not re-describe gates, lanes or shops (1.1). Avoid "encroachment" in the narrator's voice except as the official term, quoted.
- **Transition:** From where people live to how they live: the houses stand in a village whose fields and quarries, not its monuments, earn its bread.

---

## 12.2 Fields, a market town and the quarries *(livelihoods at the last record · ~650 w)*

**Word target:** 650

- **Section statement:** By the end, the reader knows that Udaypur's living is farming, chiefly wheat sold through the Ganj Basoda *mandi*, alongside quarry work on the stone-rich land around it, some of it on illegal quarries; that wealth from cloth, grain and stone sits in the market towns rather than the village; and that village growth and farming press on the reserved forest next door.
- **Purpose:** Give the economy of the living village, honestly thin, so that the conservation tensions of 12.3–12.5 have their material basis.
- **Paragraph plan:**
  1. **P1 — Wheat for the *mandi*.** **Point:** The survey describes an agrarian economy growing wheat for the large market at Ganj Basoda; this matches the district picture (in 1961 three-quarters of the district's workers were in agriculture) and the kharif–rabi year already set out in 2.2 (recall in a clause). Udaypur lives as a satellite of a market town; that also explains why Ganj Basoda people reappear in 12.4–12.5.
     - E: C12-GEOHER-002 (T7) · X: C08-GAZ-006 (T7), C08-GAZ-007 (T7) (homed Ch 8; one clause, do not duplicate Ch 8's treatment)
  2. **P2 — "Nothing beyond livelihood and farming".** **Point:** Tiwari judges that most residents think of nothing beyond their livelihood and farming, even the better-off. Quote or paraphrase once, attributed, and then qualify by construction: this is a visitor's view of a farming village, and it is evidence for what outsiders expected of residents, not for residents' minds. Tiwari's further remark that the cloth, grain and stone merchants of the area could raise large sums for Udaypur in one sitting (no number) places the region's wealth in its trading towns, not in the village.
     - E: C12-JAGTA-HI-009 (T8) · C: C12-JAGTA-EN-006 (T8) (second half only) · X: C12-JAGTA-HI-010 (T8) (contextual; **no "hundred crorepatis", no "two–four crore"**)
  3. **P3 — Quarry work.** **Point:** Recall 2.5 in one clause (Udaypur and Pathari rich in stone; Govind Saxena's report of illegal quarries on forest-department land). The new material is about people: in that report, men from local villages work the quarries for wages barely enough to live on, while the stone's owners blast without restraint. Tiwari goes further, alleging a network that ties the illegal sand and stone trade to local party agents, the forest department, the police and the administration; this is his allegation and must be attributed as such, with no names. Some people, in Tiwari's report, believe the ground blasts endanger the temple itself (homed Ch 11; recall only).
     - E: C12-JAGTA-HI-011 (T8) · C: C12-JAGTA-EN-003 (T8) (**U7: one attributed sentence; no one accused is named; legal review**) · X: C02-JAGTA-EN-003 (T8) (recall), C11-JAGTA-EN-028 (T8) (recall) · Note: C12-JAGTA-HI-011 (T8) (the "2,500 hectares" figure is Saxena's, via Tiwari; **omit from text**, keep in note only if the editor allows a reported figure attributed to a named report)
  4. **P4 — Fields against the forest.** **Point:** The survey reads the growth of the village and of farming as a rising pressure on community resources and a threat to the reserve forest that adjoins the hill. Link back to 12.1's numbers (documented growth) and forward to 12.3 (the hill as a habitat). Mark clearly that "threat" is the surveyors' framing.
     - E: C12-GEOHER-004 (T7) · X: C02-GEOHER-021 (T7) (recall: grazing and illegal felling, told in 2.3)
- **Drafting guidance:** This section is **honestly short**; do not pad with district statistics. Never present Tiwari's mining-network passage as fact; one sentence, attributed, no names, no adjectives beyond his ("plunderers" may appear only inside a quotation). No figures from testimony. Do not explain the monsoon or soils again (2.2).
- **Transition:** The same pressures, fields edging into forest, quarries blasting near the wall, meet on the hill, which is also a habitat with its own residents.

---

## 12.3 The living hill *(wildlife, grazing, pilgrims and blasts · ~700 w)*

**Word target:** 700

- **Section statement:** By the end, the reader knows that the hill above Udaypur is a habitat as well as a monument: its caves hold thousands of bats over deep guano, it shelters vultures and, by the survey's count, more than 58 bird species with winter migrants on the water; that in 1968 a forest shooting block named "Udaipura" still reported tiger, sambar and chital; and that the same hill is grazed, climbed by pilgrims and trekkers, and shaken by quarry blasts.
- **Purpose:** Carry the wildlife material moved from Chapter 2 (14 Oct 2026) as part of the living environment, and show that the hill's non-human residents share the pressures of 12.2.
- **Paragraph plan:**
  1. **P1 — The caves' residents.** **Point:** Chapter 2 (2.3) described the hill's caves as geology; here they are habitat. The survey found the caves around the hill home to thousands of bats; in Cave I, on the western side, the floor of the entry passage lay under bat guano 500–600 mm deep, measured on site. Cave IV, high on the south-east face, could be seen only by drone and may be used by scavenging birds (the survey's "possibility"). Mark the survey's "for millions of years" as a claim not to be repeated.
     - E: C02-GEOHER-022 (T7), C02-GEOHER-017 (T7) · C: C02-GEOHER-020 (T7) (bats only; the 270 m was told in 2.3) · X: C02-GEOHER-018 (T7) (possible scavenger birds, graded "may")
  2. **P2 — Vultures and birds.** **Point:** The survey saw vultures, monkeys, squirrels, pigeons, parrots, bees and red ants in abundance on the hill (2.3 used only the plants of this item), and reports more than 58 bird species at Udaypur, among them the Oriental white-backed, long-billed and red-headed vultures, with sarus cranes and painted storks on the water bodies in winter; it places Udaypur in the Indo-Malayan tropical dry zone and credits it with 33 of the biome's 59 species identified by BirdLife International. Grade it: the count and the biome claim are the survey's. Set the 1979 Gazetteer's district list (peafowl, jungle fowl, sandgrouse, quail, green pigeon; geese, pochards and teals in winter) beside it only as the earlier district picture, not as a record for the hill. The survey also names the hill a storehouse of bryophytes and lichens needing systematic study (lichen *dating* belongs to Ch 7; here only the living micro-flora).
     - E: C02-GEOHER-019 (T7) (animals), C02-GEOHER-023 (T7) · C: C02-GEOHER-025 (T7) · X: C02-GAZ-033 (T7)
  3. **P3 — The 1968 shooting block.** **Point:** The Gazetteer's table of wild animals reported in 1968, by forest range and shooting block, lists under the Gyaraspur Range a block named "Udaipura", with entries under tiger, sambar, chital and "other" (verify the column alignment before giving any number; see Flags). Whether this block took in Udaypur's hill is not stated; say "a block named Udaipura" and do not identify it with the town. Frame with the Gazetteer's own account of decline: princely and *jāgīrdārī* shooting before 1948, reserves opened to permit-holders under Madhya Bharat, poaching rising in the 1950s with more gun licences and jeeps, then government suppression. The blackbuck "very rare" through poaching (district list) may close the paragraph.
     - E: C02-GAZ-034 (T7), C02-GAZ-031 (T7) · C: C02-GAZ-035 (T7) · X: —
  4. **P4 — A hill in use.** **Point:** Return to people: local villagers go up to the religious sites on the hill, and the survey asks for a defined track for pilgrims' safety; the survey also expects trekkers drawn by the abandoned hill fort. Cattle, goats and sheep graze the hilltop (homed Ch 11 as damage; here as use, one clause), and occasional dynamite blasts are still heard around the lower hill (Ch 11/Afterword; one clause). End on the shared condition: bats, vultures, herders, pilgrims and quarry crews all use the same hill, and the survey that counted the birds also counted the threats. Do not make the land the cause of anything.
     - E: C12-GEOHER-003 (T7), C12-GEOHER-005 (T7) · X: C11-GEOHER-014 (T7) (recall), C11-GEOHER-013 (T7) (recall, blasts only), C02-KB-GEOHER-012 (T7) (recall: reserved forest, 2.3)
- **Drafting guidance:** Describe from the items; no sensory scene (no "the air at dusk", no "wingbeats"). Keep species names as the source gives them. Every number here is a survey's or the Gazetteer's, never Tiwari's. "Udaipura" block: name it, do not equate it. Do not repeat 2.3's plants, heights or cave geology. "Vulnerable/endangered" status of vultures is **not in the evidence**: do not add it.
- **Transition:** Pilgrims climb the hill; far more people come only to the temple below it, and what they see of Udaypur is the subject of the next turn.

---

## 12.4 The temple's Udaypur *(visitors, officials and the first walkers in the lanes · ~800 w)*

**Word target:** 800

- **Section statement:** By the end, the reader knows that most outsiders know Udaypur only as its temple: worshippers come for Nīlakaṇṭheśvara Mahādeva, make their vows and photographs and leave; officials make VIP visits to the sanctum; the custodial staff send no one into the town; and that from about 2020–21 a small circle from Ganj Basoda and Bhopal began, for the first time in the record, to walk the lanes, film the ruins and carry Udaypur's story to the capital.
- **Purpose:** Describe the "second Udaypur", the one visitors see, and the first modern attempt to join it to the town, without re-telling Chapter 11's institutional story.
- **Paragraph plan:**
  1. **P1 — Darśan and departure.** **Point:** Recall 1.1 (daily worship; the fair) in a clause and add what is new. In Tiwari's account Indian visitors' interest is in the deity rather than the building: they go straight in for worship and *abhiṣeka*, hang their wishes on Śiva (a son's job, a daughter's marriage, court cases, land disputes), photograph the temple, and leave Udaypur without delay. Photography has become "a necessary rite like offering flowers". Few look at the architecture; next to none at the history. Chapter 8 owns the ritual; here only the visitors' path through the town.
     - E: C12-JAGTA-EN-015 (T8), C12-JAGTA-EN-016 (T8) · C: C12-JAGTA-HI-027 (T8), C12-JAGTA-HI-029 (T8) · X: C01-JAGTA-EN-025 (T8) (recall), C08-PANDE-011 (T5) (recall)
  2. **P2 — Officials in the sanctum.** **Point:** In Tiwari's account each sub-divisional officer and *tahsīldār* at Ganj Basoda brings senior officers and their families for VIP darśan straight to the sanctum; hardly any notices the condition around the temple or walks into the lanes. Some officials who had been to Udaypur knew it only as "an ancient grand temple". The point is not to mock officials but to show the same pattern at the top: Udaypur known as a shrine, not as a town.
     - E: C12-JAGTA-HI-031 (T8) · C: C12-JAGTA-HI-033 (T8) · X: C12-JAGTA-HI-028 (T8) (Suresh Mishra's first sight of the temple and its neglected surroundings; one clause, attributed)
  3. **P3 — No one to show the way; one night when the town is full.** **Point:** Tiwari complains that no one tells visitors about Rāvaṇaṭol or Pisanhārī, and that the ASI staff at the temple neither direct visitors to the town's other sites nor give even ten minutes of facts. Keep it to one or two sentences on what the visitor experiences; Chapter 11 (C11-JAGTA-EN-034 (T8)) carries the custodial critique. On Mahāśivarātri, by contrast, the town is full: a long column of devotees, a large police deployment and, in 2021, the local heritage team in the field beside officials (no numbers).
     - E: C12-JAGTA-HI-036 (T8) · C: C12-JAGTA-HI-035 (T8) (qualitative only) · X: C11-JAGTA-EN-034 (T8) (recall)
  4. **P4 — Walking the lanes.** **Point:** From about 2020–21 people from Ganj Basoda began looking anew at the "sad town" next door. A group of young people walked around Udaypur every few days. A farmer and social worker, Praveen Sharma, went into ruins, old houses and thickets, photographed stones and images, put them back in their places and posted them online; he had returned a missing image to its place four days before INTACH's team arrived. Visitors who had once gone "only to the temple, like other tourists" came back to walk the lanes. State Tiwari's own role once, attributed: taking Suresh Mishra to Udaypur, and a band of youths organising monthly visits.
     - E: C12-JAGTA-HI-015 (T8), C12-JAGTA-EN-004 (T8) · C: C12-JAGTA-HI-034 (T8), C12-JAGTA-EN-013 (T8), C12-JAGTA-HI-017 (T8) · X: C11-JAGTA-HI-030 (T8) (the image returned; recall)
  5. **P5 — Udaypur reaches Bhopal.** **Point:** The outside world learned of the town through the media, not through its custodians. Govind Saxena rode to Udaypur to film the palace's verandas, halls, stairs and cellars, including the padlocked roof claimed as private property; his video appeared on *Patrika*'s portal and was widely watched. A presentation on Udaypur filled a hall at the Tribal Museum in Bhopal. Recall Chapter 11's palace episode (Tiwari's post of 5 January 2021; the tahsildar's visit; the order) in one clause. Close on Udaypur seen from Bhopal as a place one may set out for in the morning and return from by evening (Tiwari's phrase): near, yet unknown.
     - E: C12-JAGTA-HI-032 (T8), C12-JAGTA-EN-017 (T8), C12-JAGTA-EN-018 (T8) · C: C12-JAGTA-HI-020 (T8) · X: C12-JAGTA-EN-019 (T8), C11-JAGTA-EN-022 (T8) (recall), C13-JAGTA-HI-021 (T8) (the INTACH offer and the 2 March booking; homed in the Afterword; recall only for the date)
- **Drafting guidance:**
  - Almost wholly testimony: attribute once per paragraph ("in Tiwari's account").
  - Avoid the source's satirical register. "Poison of endless desires", "Kohinoor" and "24-carat" may appear only inside quotation marks, if at all.
  - Introduce Praveen Sharma here. Govind Saxena was introduced in 2.5: recall him. Suresh Mishra: check the ledger; if this is his first mention, "the historian Suresh Mishra".
  - Do not name the archaeology functionary named in C11-JAGTA-EN-020 (T8).
  - No counts: "more than a lakh", "more than a hundred", "four hundred police" and "thousands" are excluded.
  - "Tiwari" only; the full name is spent in 1.1.
- **Transition:** Walking the lanes was not only looking. Within weeks the lane to the temple itself was cut back, and residents had to decide what to give up.

---

## 12.5 The lane to the temple, 2021 *(conservation and everyday life; whose voice · ~850 w)*

**Word target:** 850

- **Section statement:** By the end, the reader knows what happened when the lane to the temple was widened in early 2021: house and shop fronts on both sides were taken back and rebuilt, one shopkeeper gave more than was asked without waiting for an order, others followed, a few buildings were left standing, and a path was laid by public cooperation. The reader also knows that residents saw in this the hope of trade and visitors, while the outsiders who chronicled it judged residents distant from their heritage. The record keeps residents' acts and outsiders' words.
- **Purpose:** Give the chapter's one dated episode where conservation met daily life, and use it to weigh the record's voices: the brief's "practical tensions" and "local aspirations".
- **Paragraph plan:**
  1. **P1 — Fronts taken back.** **Point:** The narrow lane leading to the temple, which in Tiwari's account had once been a broad road and had shrunk as shops and houses were built out over the decades, was widened in February 2021. The front portions of houses and shops on both sides were removed, and owners began building again behind the new line. Give no widths or counts (Tiwari's ten feet, eight feet, thirty-foot road, 40 businessmen are testimony measurements). Recall C07-JAGTA-EN-026 (T8) (the single old lane of shops) and 1.1 (lanes narrowed against the gates) in a clause; recall Ch 11 for the 1972 ASI clearance of houses against the temple, which was done with compensation (C11-JAGTA-EN-011 (T8)), as the precedent.
     - E: C12-JAGTA-EN-008 (T8), C12-JAGTA-EN-009 (T8) · C: C12-JAGTA-HI-024 (T8), C12-JAGTA-EN-011 (T8) (process only, no figures) · X: C07-JAGTA-EN-026 (T8), C11-JAGTA-EN-011 (T8) (recall)
  2. **P2 — What residents gave.** **Point:** One shopkeeper beside the temple gate, Raja Miyan, did not wait for a government order. He took back more of his own frontage than was asked and called it his share of merit (*savāb*) for Udaypur's good; in Tiwari's account his example opened the way for other traders to set back their buildings. A guest account in the same book credits local people with first removing encroachments themselves and then clearing the path, on the initiative of named citizens of Ganj Basoda, Udaypur and Mandi Bamora, so that a cemented path was ready "in no time" by public cooperation. Give the one Udaypur name, and the Ganj Basoda names only in a note if at all. Resolve the "Raja Mishra / Raja Miyan" spelling in a note (the map's translator flags both).
     - E: C12-JAGTA-EN-010 (T8), C12-JAGTA-HI-025 (T8) · C: C12-JAGTA-EN-014 (T8), C12-JAGTA-HI-018 (T8) · X: C13-JAGTA-HI-020 (T8) (homed in the Afterword; same passage) · Note: C12-JAGTA-EN-011 (T8) (name variant)
  3. **P3 — What was left standing.** **Point:** Not every building moved. One house projecting into the lane, carrying a Jama Masjid signboard, was left untouched while its neighbours were cut back; two houses in front of the temple were also left and remain occupied (Ch 11). State this flatly, without motive: the record does not say why, and the book does not supply a reason. This is the tension in its plainest form: a widening that depended on consent stopped where consent, or authority, stopped.
     - E: C12-JAGTA-EN-009 (T8), C12-JAGTA-HI-024 (T8) · X: C11-JAGTA-EN-033 (T8) (recall)
  4. **P4 — Hopes of trade.** **Point:** The people the walkers met along the way were curious. In Tiwari's account they took the work as the start of a development that would bring outsiders and make their businesses shine, "on the whole, a matter of their own benefit". A guest writer reports local enthusiasm that the monuments would "come alive", and residents, knowing a little of the town's history, "girding themselves" to serve as tourism attendants. Present these as the record's only statements of residents' aspirations: modest, economic and reasonable. Do not echo the source's disapproval.
     - E: C12-JAGTA-EN-012 (T8), C12-JAGTA-HI-026 (T8) · C: C12-JAGTA-HI-039 (T8), C12-JAGTA-HI-038 (T8) (Vadnerkar)
  5. **P5 — Whose account.** **Point:** Set the outsiders' verdicts side by side, each attributed. For Tiwari, residents are "cut off from the past, careless of the present" and wait on governments for everything. In his account no panchayat member, official, teacher or citizen took any initiative for decades, and the dawn of independence never reached the fort's fallen walls. For Upadhyay, residents live in "a separate world", at a distance from their heritage, and outside effort will fail until they feel attached to it. Then make the book's observation, labelled as inference: these are visitors' judgements, and the same record shows residents rebuilding on ruins (12.1), working fields and quarries (12.2) and giving up frontage unasked (P2). Residents themselves speak in it only in a sentence or two. The present cannot be fully written from this evidence, and the gap is part of the history. End by content: the residents' hope of visitors and the outsiders' plans for them are the same question seen from two sides, and the Afterword takes it up. No summary, no question mark.
     - E: C12-JAGTA-HI-021 (T8), C12-JAGTA-HI-016 (T8) · C: C12-JAGTA-EN-006 (T8), C12-JAGTA-HI-019 (T8), C12-JAGTA-EN-005 (T8), C12-JAGTA-HI-003 (T8) · X: C12-JAGTA-HI-022 (T8) (one phrase at most) · Note: C12-JAGTA-HI-016 (T8) (Upadhyay as INTACH convener; Ch 11 introduces him)
- **Drafting guidance:**
  - Narrate P1–P3 closely; this is the one place where the present moves.
  - P3 is sensitive: no motive, no communal framing, no adjectives. The narrator says "Muslim" only if needed, never "Mohammedan". Do not import Tiwari's green-cloth/*mazār* passage (C12-JAGTA-EN-007 (T8)): it is homed in Chapter 9, and it is polemic, not evidence of the lane.
  - P5 must keep each verdict in its speaker's mouth; the book's own judgement comes last and is marked as inference ("the record shows", "the evidence allows"), never as a rebuke of the sources.
  - No figures from testimony anywhere.
  - Pages 161–170 of the book are guest pieces: attribute C12-JAGTA-HI-018 (T8), -038, -039 and C12-JAGTA-EN-014 (T8) to "a contributor to Tiwari's book" (name Vadnerkar where the map does) until verified.
- **Transition (to the Afterword):** The lane was widened on outsiders' initiative and with residents' consent. What should come next, and who should decide, is the question the Afterword takes up.

## Chapter 12: conflicts to present, unresolved

| Conflict | Where | How held |
|---|---|---|
| Population: 6,383 (2011) vs "about 8,000" (Tiwari) | **12.1 (home)** | Documented counts only (1901, 1971, 2011) |
| 1901 printed twice (928 / 1,619) | 12.1 | "Under two thousand in 1901"; both figures in a note unless the scan settles it |
| The "Udaipura" shooting block (Gyaraspur Range) vs Udaypur's hill | 12.3 | Not equated; check the table's columns |
| Lane widths (3-foot path vs ten feet each side; testimony) | 12.5 | No widths |
| "Raja Miyan" / "Raja Mishra" | 12.5 | "Raja Miyan" unless the Hindi page (p. 70) says otherwise |
| Date of the widening (16 Feb 2021 in a relevance note only) | 12.5 | "Early 2021" unless verified |

## Chapter 12: hand-offs

- **In:** A family's house in Udaypur that had lain buried in an excavation decades earlier, with fine old carving, was cleaned out "with devotion and effort" and is now their home (C12-JAGTA-HI-014, p. 73). Chapter 11 ends (by its own plan) with official and institutional attention arriving in 2021; Chapter 12 opens on the opposite scale, a household that had already made the old town its home without any department. The first paragraph must not restage 1.1's approach to the village; it begins inside.
- **Out:** It ends on the two sides of one hope: residents expecting visitors and trade, outsiders drawing up plans to bring them. The Afterword opens on those plans. It must not summarise the chapter, preview the Afterword, ask a rhetorical question, or end on a lament ("waiting to wake", "gasping") borrowed from the sources.

## Chapter 12: changes from the master outline

1. **U7 (legal review):** Tiwari's allegation of a mining network (C12-JAGTA-EN-003) gets one attributed sentence, naming no one accused (12.2), flagged for legal review.
2. **Green-cloth / *mazār* passage:** 12.4 at most one neutral, attributed sentence; omitted by default (Part I).
3. **Evidence pass:** coverage complete (the unused items are named in the outline's "not used" lists). No structural change.

## Chapter 12: research and verification flags

- Population: 6,383 (2011) vs "about 8,000" (Tiwari).
- 1901 figure printed twice (928 and 1,619) in GAZ p. 348
- INTACH's census figures are quoted from villageinfo.in
- The 1968 shooting block "Udaipura"
- GEOHER's bird and biome claims
- "Millions of years"
- Guest voices in *Jagta Hua Kasba*.
- Lane widths conflict and are testimony.
- "Raja Mishra" / "Raja Miyan"
- Date of the widening:
- Tiwari's mining-network allegation
- Old canon C18.4's "a resident's charge against the archaeology department"
- Old canon C18.3's "the young leaving"
- "Today" means c. 2021.
- Distances.
- Mahāśivarātri 2021 numbers
- Stronger evidence wanted:
- **LEGAL REVIEW before publication:** 12.2 (the mining allegation); any sentence touching the palace claimants (none should name them).
- **Page-image checks:** GAZ p. 348 (1901 figure); Tiwari pp. 161–170 (guest contributors: Shivkumar Vivek, Ajit Vadnerkar, a tribute); p. 70 (Raja Miyan); ≈ p. 63 (the widening's date).
- **Free local search (`kb-new`, only if a section lands short):** the corpus Markdown for Udaypur's 2011 census details beyond GEOHER and INTACH.

---

# Afterword. Conserving Udaypur: Community, Heritage and the Future

**Planned words:** 2,750 (AW.1: 500 · AW.2: 600 · AW.3: 650 · AW.4: 550 · AW.5: 450). **Evidence:** `evidence_index/ch13.jsonl`.

**Historical question.** Given what the book has shown about how Udaypur was made, used, remade and recorded, what would conserving it mean, who would have to do it, and which of the proposals on record fit the place as it actually is?

**Through-line.** By the end, the reader knows where the record of Udaypur stops, which parts of the town and hill were protected and which were not at that point, which proposals are realistic and who would have to carry them out, and why the book argues that Udaypur should be conserved as a lived-in town and hill rather than as a temple with surroundings.

**Arc.** AW.1 where the record stops (dated, flat) → AW.2 what is at stake and who answers for which part (the protection map) → AW.3 the proposals on record, sorted by scale and by who bears the cost → AW.4 roles: residents, professionals, researchers, administrators, visitors, each tied to evidence of what they have done → AW.5 the argument, labelled, ending on the village under the temple.

-

**Scope.** *Chronological:* from Tiwari's 2019 letter to the last record (early 2021, and a survey made after 2021 whose date must be found before AW.1 is drafted). The Afterword argues from the whole book; it claims no present condition beyond the last record. *Geographical:* Udaypur's town and hill as one place; the institutions that answer for its parts (ASI, the state department, the Forest Department, the district administration).

**Editor's merge rulings carried into this plan** (from the master outline):
> **Editor's merge rulings for the Afterword** (these override the entry below where they differ)
> - **The Afterword is a substantive argument,** not a summary. AW.1 fixes the evidence horizon. AW.2 maps jurisdiction and risk **in compressed form, recalling Chapter 11 without re-describing it**. AW.3 tests every proposal on record against the book's evidence. AW.4 assigns roles by what parties have done. AW.5 is the one place where the book argues, labelled once as advocacy.
> - **Opening:** Tiwari's 2019 letter to the Collector, confirmed. It takes up Chapter 12's last paragraph.
> - **The survey's date** (GEOHER) must be found before AW.1 is drafted. Until then: "a survey made after 2021".
> - **Temple Economics** items cross-referenced into the Afterword map (C11-TEMPLE-ECON-002, -004) are excluded.
> - **The last paragraph** returns to the village under the temple (1.1) by content. No exhortation, no question, no claim beyond the last record.
> - **Length:** ~2,750 words planned; the user to confirm (Part I, I.7).

## AW.1 Where the record stops *(2019 to the survey · ~500 w)*

**Word target:** 500

- **Section statement:** By the end, the reader knows the last dated events in the evidence and the book's horizon:
  - the 2019 letter;
  - the January–March 2021 cluster (palace order, lane, Bhopal presentation, the meeting with the ASI regional director);
  - INTACH's 2021 documentation and the geo-heritage survey that followed it;
  - Suresh Mishra's death in the COVID-19 period, and a grassroots plan in his memory that was still "under consideration".

  Everything said about present conditions is said as of then.
- **Purpose:** Conclude the historical narrative honestly. It ends not on a resolution but on a set of proposals in motion and a survey's warnings, with no record of what followed.
- **Paragraph plan:**
  1. **P1 — A letter to a Collector.** **Point:** Open on the 2019 letter: suggestions and requests to look after "the history that had survived alive" in Udaypur, and the proposal that work on the model of the Kashi Vishwanath corridor could put Udaypur, close to Bhopal, on Madhya Pradesh's tourism map. Give the date, the addressee (a Collector, unnamed) and the model; assess nothing yet. Tiwari's later demand that the Collector come and see for himself and act "before the next transfer" may follow as the letter-writer's frustration (attributed).
     - E: C13-JAGTA-EN-001 (T8) · C: C13-JAGTA-HI-002 (T8) · X: C13-JAGTA-HI-004 (T8)
  2. **P2 — 2021 in one sentence each.** **Point:** Recall, without retelling, the dated sequence the reader already knows: the palace notice and the eviction order (January 2021, Ch 11); the lane widened by consent (February 2021, Ch 12); INTACH's offer and the presentation in Bhopal on 2 March (Ch 12); and, new here, the March 2021 meeting at which Tiwari and Mishra put to the ASI's regional director in Bhopal the proposal to display Hindi and English translations of selected inscriptions in the temple precinct. Then INTACH's documentation and book of 2021, and the geo-heritage survey built on it (C11-GEOHER-006 (T7)).
     - E: C13-JAGTA-EN-008 (T8), C13-JAGTA-HI-021 (T8) · C: C13-JAGTA-HI-007 (T8), C13-JAGTA-EN-014 (T8) · X: C11-JAGTA-EN-027 (T8) (recall: the order's date, 15 Jan 2021), C12-JAGTA-EN-008 (T8) (recall), C11-GEOHER-006 (T7)
  3. **P3 — A historian's death and a plan under consideration.** **Point:** Suresh Mishra, who had said the whole town could be developed as a heritage town, died in the COVID-19 period. A contributor to Tiwari's book (Shivkumar Vivek, per the map) reports a plan "under consideration" for grassroots work in his memory, to look after the heritage nearby and awaken a consciousness of history. It is the last forward-looking fact in the record, and it is only a plan. Hold Mishra's "heritage town" vision for AW.3/AW.5; here only his death and the plan.
     - E: C13-JAGTA-EN-013 (T8), C13-JAGTA-HI-018 (T8) · X: C13-JAGTA-HI-038 (T8) (the tribute's phrase "a historian's last dream"; quote at most once in the book, preferably in AW.5)
  4. **P4 — The horizon.** **Point:** State once, plainly, that nothing in the evidence is later than the survey. Whether the translations were mounted, the hill notified, the monitoring installed or the circuit begun, the record does not say. The rest of the Afterword describes conditions as the survey found them and proposals as they stood. Do not dramatise the silence.
     - C: C11-GEOHER-006 (T7) (as the dating anchor) (home Ch 11: cross-reference) · Note: the survey's own date is not recorded in the map (see Flags)
- **Drafting guidance:** Compress P2 hard: each Chapter 11/12 event gets a clause, never a scene. Name the ASI "regional director" by office only (the HI item names P. K. Mishra; do not confuse him with Suresh Mishra, and do not name him unless the editor wants it). The pandemic: "the COVID-19 period", no dates. No adjectives of mourning beyond the source's.
- **Transition:** What the last surveyors found at stake, and which authority answered for which part of it.

---

## AW.2 What is at stake, and who answers for it *(the protection map at the last record · ~600 w)*

**Word target:** 600

- **Section statement:** By the end, the reader knows in one view which parts of Udaypur were protected and by whom at the last record, and which were not:
  - the temple, by the ASI;
  - four monuments by the state: two mosques, Pisanhārī's temple and the Naṭarāja at Rāvaṇaṭol;
  - the hill, as reserved forest under the Forest Department;
  - the palace, with no protection at all;
  - the fortification stretch, for which notification was proposed.

  The reader also knows the survey's own short list of what threatens each: mining blasts, an accelerating decay of the wall, new cracks in fresh repairs, monsoon drainage, grazing and graffiti.
- **Purpose:** Give the implications that emerge from the book as a whole in institutional form: Udaypur is one historic place divided among several authorities, and the gaps between them are where the damage is reported.
- **Paragraph plan:**
  1. **P1 — One place, several owners.** **Point:** Lay out jurisdiction at the last record:
     - the Nīlakaṇṭheśvara/Udayeśvara temple is ASI-protected;
     - the state protects four monuments: two mosques, Pisanhārī's temple and the 27-foot Naṭarāja at Rāvaṇaṭol (Tiwari reports state spending on these four; give no sums here, since Ch 11 has them);
     - the palace is protected by neither Centre nor state (Tiwari);
     - the hill is reserved forest (2.3);
     - the survey lists among the site's stakeholders the forest, archaeology, tourism, and panchayat and rural development departments and the Geological Survey of India.

     The point is structural: no single authority holds the town, the hill and the temple together.
     - E: C11-JAGTA-EN-009 (T8), C11-JAGTA-EN-006 (T8), C13-GEOHER-004 (T7) · C: C11-GEOHER-001 (T7) (home Ch 11: cross-reference) · X: C02-KB-GEOHER-012 (T7) (recall)
  2. **P2 — Where the survey found damage.** **Point:** In a compressed list, recalled from Chapter 11 and not retold, give what the survey recorded:
     - illegal sandstone mining as "the most significant issue": no mine on record, but occasional dynamite blasts that threaten both the protected Naṭarāja and the fortification wall;
     - the wall's deterioration "dramatically accelerated over the past decade";
     - a new crack in a recently repaired section of pitching at the south-west corner, as evidence that causes had not been treated;
     - the monsoon emergency (drainage, shoring, netting) and its warning of risk to life;
     - grazing, graffiti and concrete steps cut into the reserve forest;
     - the hill's antiquities lying unprotected beside a privately owned quarry.

     Every item is the survey's finding as of its date.
     - C: C11-GEOHER-011 (T7) (home Ch 11: cross-reference), C11-GEOHER-009 (T7) (home Ch 11: cross-reference), C11-GEOHER-013 (T7) (home Ch 11: cross-reference), C11-GEOHER-010 (T7), C11-GEOHER-008 (T7), C11-GEOHER-012 (T7), C11-GEOHER-014 (T7) · X: C07-GEOHER-048 (T7) (dried tank, collapsed steps; one clause, optional)
  3. **P3 — The gap made visible.** **Point:** Draw the book's inference, labelled: the dangers the survey lists concentrate where protection does not reach (the hill, the wall, the palace, the scattered sculpture) or where two authorities meet (a state-protected sculpture on forest land beside a quarry). The survey's own remedies point the same way: notification of the continuous 1,400 m stretch as a protected monument; INTACH's steps toward notifying the whole complex as a site of national importance; and, as first measures, an engineering-geological map of the fort to identify priority areas of risk and a monitoring system for movement of stone and soil. Callback: Chapter 11's finding that protection saved the temple and detached it from its town is here a map of present risk.
     - E: C13-GEOHER-001 (T7) · C: C11-GEOHER-003 (T7) (home Ch 11: cross-reference), C11-GEOHER-002 (T7) (home Ch 11: cross-reference) · X: Ch 11 conclusion (recall by content)
- **Drafting guidance:** This section must **not** become Chapter 11 again. Each threat gets a clause, and the paragraph carries no narrative of discovery. Never "is collapsing", "critical phase" or "collapsed bastions" (not in the maps). Use the tense of the record: "the survey found", "was protected". "Naṭarāja" with diacritics in the narrator's voice; "Natraj" only in quotation.
- **Transition:** The survey's remedies are one set of proposals among many; the record holds others, from a signboard to a statewide circuit, and they differ most in who would bear their cost.

---

## AW.3 The proposals on record *(sorted by scale and by who bears the cost · ~650 w)*

**Word target:** 650

- **Section statement:** By the end, the reader knows the full range of what has been proposed for Udaypur, sorted into three kinds:
  - **small and local:** translations of the inscriptions at the temple; interested, skilled staff; Sunday heritage walks with printed material; clearing of overgrowth and rubbish; village guides; signage;
  - **institutional:** the geo-heritage plan led by the Collector and piloted by INTACH; one coordinating effort across agencies; documentation of every panchayat; school heritage visits;
  - **transformative:** a corridor on the Kashi Vishwanath model; a "heritage town"; a Paramāra temple circuit with Bhojpur and Khajuraho, under public–private partnership.

  The reader also knows what the book's evidence says about the cost and feasibility of each.
- **Purpose:** Turn the map's long list of appeals (S1, S3, S4) into an analysis. This is the Afterword's main "realistic interventions" work, as the chapters.md brief asks.
- **Paragraph plan:**
  1. **P1 — Telling the story where it stands.** **Point:** Tiwari's most persistent proposal ties the book's Chapter 6 to the present. The inscriptions have been read, yet visitors and villagers leave "without any information". He proposes:
     - Hindi and English translations of selected inscriptions, displayed in the precinct, not "on worn tin pieces";
     - ideally, translations carved on stone from Udaypur's own quarries.

     He put this to the ASI regional director in March 2021. Add, in a clause each, the other low-cost measures on record:
     - skilled, interested staff at such sites;
     - a declared Sunday heritage walk with printed material, "very cheap", which Centre, state, district association or panchayat could support;
     - weekly clearing of overgrowth by the local heritage team;
     - from the survey: guides drawn from the villages and trained by INTACH, and signage and an interpretation board at the hill's entrance.

     Callbacks: Ch 6 (the inscriptions themselves), 2.5 (a town of its own stone).
     - E: C13-JAGTA-EN-006 (T8), C13-JAGTA-EN-007 (T8), C13-JAGTA-EN-008 (T8) · C: C13-JAGTA-HI-005 (T8), C13-JAGTA-EN-002 (T8), C13-JAGTA-EN-016 (T8), C13-JAGTA-EN-004 (T8), C13-JAGTA-HI-012 (T8), C13-GEOHER-002 (T7), C13-GEOHER-005 (T7) · X: C13-JAGTA-HI-006 (T8), C13-JAGTA-HI-003 (T8)
  2. **P2 — Joining the authorities.** **Point:** The institutional proposals answer AW.2's gap:
     - the survey's plan makes the District Collector the overall team leader, with INTACH's Bhopal chapter piloting the geo-conservation plan from preparation to implementation, and an operational plan defining every stakeholder's role;
     - INTACH's stated aim, as Tiwari reports it, is to bring together the ASI, the state archaeology department, the district administration, the panchayat, private institutions, corporate companies and local society;
     - Upadhyay proposes documenting every panchayat's heritage across the state, as INTACH says it is doing in 10–12 districts (his figure, attributed; it is not a measurement of Udaypur), a task he calls a week's work for trained local volunteers;
     - heritage visits for schools and colleges at least twice a year, through simple tourist circuits.

     Note what is missing: no item records any of these being adopted.
     - E: C13-GEOHER-003 (T7), C13-JAGTA-EN-017 (T8) · C: C13-JAGTA-HI-025 (T8), C13-JAGTA-EN-009 (T8), C13-JAGTA-HI-026 (T8), C13-JAGTA-EN-010 (T8) · X: C13-JAGTA-HI-008 (T8), C13-JAGTA-HI-009 (T8), C13-JAGTA-EN-012 (T8)
  3. **P3 — The large visions.** **Point:** Set out the transformative proposals, each in its speaker's voice:
     - Tiwari's corridor on the Kashi Vishwanath model;
     - Mishra's "heritage town", with the corollary that "now is the time to remove the illegal kiosks";
     - a contributor's Paramāra temple circuit joining the regions of the state, with Bhojpur "already established" and foreign visitors drawn on from Khajuraho, by public–private partnership or local cooperation;
     - Upadhyay's view that sites with a tenth of Udaypur's potential are busier only because of policy, and that Udaypur could be "a model";
     - the survey's geo-heritage reserve "in harmony with" a larger tourism plan for "this 11th-century CE Parmar capital city" (the survey's phrase; "capital" is its claim, not the book's: see Flags).

     Callback: Bhojpur appears in 2.4 as comparative evidence of Paramāra water engineering; here it is a tourism model. Say so in one clause so the reader does not merge the two uses.
     - E: C13-JAGTA-EN-001 (T8), C13-JAGTA-EN-023 (T8), C13-JAGTA-EN-020 (T8), C13-JAGTA-EN-021 (T8) · C: C13-JAGTA-HI-037 (T8), C13-JAGTA-HI-033 (T8), C13-JAGTA-HI-034 (T8), C13-JAGTA-HI-032 (T8), C13-JAGTA-HI-031 (T8), C01-GEOHER-019 (T7) · X: C12-JAGTA-HI-037 (T8), C12-JAGTA-HI-030 (T8), C12-INTACH-004 (T7)
  4. **P4 — Testing them against the book.** **Point:** This is the book's assessment, labelled as such ("on the evidence of this book"). Make four points:
     - **Who pays.** A corridor or the removal of "kiosks" means clearing frontage. The only clearance in the record (Ch 12, 2021) went ahead by residents' consent, at their cost, and stopped where consent stopped.
     - **Is the ground ready.** The survey itself expected the site to develop "over a period", with visitors not arriving "from day one". It also warned of risk to life on unstable structures, and it sited its parking area between the blast-threatened Naṭarāja and the wall. Note that tension without mockery.
     - **What the premise rests on.** The claim that much of the heritage is in "relatively good condition" (INTACH) is the premise of every tourism plan. The survey's findings for the wall (AW.2) qualify it.
     - **The source's own warning.** Tiwari himself warned that polishing a temple to attract visitors would be "superficial".

     Conclude that the small measures and the gap-closing institutional ones are realistic on the record's own terms; the transformative ones depend on decisions about residents that no proposal in the record addresses.
     - E: C13-GEOHER-005 (T7), C13-JAGTA-EN-019 (T8) · C: C11-GEOHER-010 (T7), C12-INTACH-004 (T7), C13-JAGTA-HI-030 (T8) · X: C12-JAGTA-EN-011 (T8) (recall, no figures)
- **Drafting guidance:**
  - Every proposal belongs to its speaker. Never "Udaypur should…" in the narrator's voice until P4, and in P4 only as "the evidence of this book suggests".
  - No exclamation, no "treasure", "24-carat" or "Kohinoor" outside quotation.
  - Do not use Tiwari's or contributors' numbers as facts (10–12 districts, "a week") except attributed as the speaker's claim inside a proposal.
  - Do not describe the Kashi Vishwanath corridor itself: the corpus has nothing on it beyond the name. Say only that it is the model Tiwari named.
- **Transition:** Every proposal names someone who should act. The record shows who has acted, and the gap between the two lists is the next subject.

---

## AW.4 Who keeps Udaypur *(roles: residents, professionals, researchers, administrators, visitors · ~550 w)*

**Word target:** 550

- **Section statement:** By the end, the reader knows, for each party the chapters.md brief names, what the record shows it has done, what the proposals ask of it, and what remains unknown:
  - **residents:** they lived in and rebuilt the town and gave up frontage; they are asked to be guides and attendants and not to disturb the hill;
  - **regional citizens and organisations:** the Ganj Basoda volunteers acted; merchants and organisations are asked to give money and a day a month;
  - **professionals:** the ASI keeps the temple; there is a shortage of people who can read inscriptions;
  - **researchers:** they are asked to come, clear mounds and excavate, and the book's own open questions are named;
  - **administrators:** the Collector is to lead, the district association to meet, and action is wanted before the next transfer;
  - **visitors:** they worship and leave; students and writers are invited.
- **Purpose:** Answer the brief's "roles" directly, and make the Afterword architectural rather than summary. It shows how the book's whole evidence (not only the advocacy) bears on who should do what, including the book's own research agenda.
- **Paragraph plan:**
  1. **P1 — Residents and the region.** **Point:** Upadhyay's judgement that nothing will succeed without local attachment, and his wider claim that such heritage needs a social campaign with active local participation, stand beside Tiwari's insistence that preserving Udaypur belongs not only to its panchayat's residents but to "every citizen of the area". Set these against what residents did (Ch 12 recall: the house made from a ruin, the lane) and what is proposed for them:
     - village guides;
     - tourism attendants (a contributor's report);
     - care not to disturb the geo-heritage.

     The regional public is asked for the most: district organisations to give "one day every month", merchants of Vidisha, Ganj Basoda and Mandi Bamora to come forward as guardians, and schools to send groups. Note the panchayats: a contributor laments their unconcern, and Tiwari argues heritage could be "an income-yielding means" for them. That is the one proposal in the record that ties conservation to residents' livelihood (callback 12.2).
     - E: C13-JAGTA-HI-015 (T8) · C: C12-JAGTA-HI-016 (T8) (home Ch 12: cross-reference), C13-JAGTA-HI-016 (T8), C13-JAGTA-HI-010 (T8), C13-JAGTA-HI-019 (T8), C13-JAGTA-HI-011 (T8), C13-JAGTA-HI-018 (T8), C13-JAGTA-HI-028 (T8), C13-GEOHER-002 (T7) · X: C12-JAGTA-HI-039 (T8) (recall), C13-JAGTA-HI-014 (T8)
  2. **P2 — Professionals and administrators.** **Point:** Upadhyay reports a "famine" of people in Madhya Pradesh, even in departments and universities, who can read new inscriptions. This is the professional bottleneck behind P1 of AW.3 and behind Chapter 6's dependence on a few editors (callback). Tiwari's other targets are:
     - stagnant minds in history departments and in the culture and archaeology department;
     - a District Archaeology Association that, in his account, met at long intervals over tea with no known result;
     - Collectors who should act before their transfer.

     The survey gives the administrator the decisive role: the Collector as team leader. Keep each criticism attributed and brief. The point is structural: the proposals depend on a few officials whose tenure is short (Tiwari's observation).
     - E: C13-JAGTA-EN-018 (T8), C13-GEOHER-003 (T7) · C: C13-JAGTA-HI-027 (T8), C13-JAGTA-HI-024 (T8), C13-JAGTA-HI-022 (T8), C13-JAGTA-HI-004 (T8)
  3. **P3 — Researchers, and what this book leaves open.** **Point:** Tiwari's appeal to historians and archaeologists to leave "books and files", clear the mounds and excavate the ruins is the one call the book itself can answer, by listing what remains unknown:
     - whether Udaypur was founded or taken over, and what the V.S. 1116 reading is worth beside the firm 1080 record (Chs 1, 4, 6);
     - the hill's tentatively read two-line inscription and the cave's undeciphered lines, kept distinct (Chs 3, 6);
     - the age of the fortification wall and the lichen proposal (Ch 7);
     - the tanks and their names (Ch 7);
     - the identity of the 1968 "Udaipura" shooting block (Ch 12);
     - the residents' own account, which no source records (Ch 12).

     Add Tiwari's further ask, that each discovery be explained to local people in simple language and books be updated, as the standard this book tries to meet.

     This paragraph is the Afterword's main **callback structure**. Name chapters by number and keep each item to a clause. Material still to be ingested (Bühler, Beglar, Cunningham, the Gwalior report of 1925–26; ASR IX p. 109) may be named only as sources the book has not yet used, if the editor wants it.
     - E: C13-JAGTA-EN-005 (T8), C13-JAGTA-HI-023 (T8) · C: C13-JAGTA-HI-024 (T8) · X: callbacks by chapter (no new IDs; if the pipeline needs anchors, use the inscription pairs named in OUTLINE_BRIEF §2, kept distinct)
  4. **P4 — Visitors.** **Point:** Visitors are the largest group, and the proposals ask most of the least-invested ones. Most come to worship and leave (Ch 12). Tiwari would make repeated visits compulsory for schools and colleges, with questions answered and "documentary evidence" given; he imagines the lanes awaiting students, and the town as material for writers and poets. A visiting writer's resolve to "preserve, awaken, face true history" closes this part of the record. Give it in a clause as an instance of the visitor the proposals hope for, not as the book's own call.
     - E: C13-JAGTA-EN-003 (T8), C13-JAGTA-EN-011 (T8) · C: C13-JAGTA-HI-013 (T8), C13-JAGTA-HI-036 (T8), C13-JAGTA-HI-035 (T8)
- **Drafting guidance:**
  - Keep the criticism of officials and institutions attributed and short; no satire.
  - Do not name individual officials, except Upadhyay (INTACH convener; introduced in Ch 11).
  - P3 must not re-argue any chapter: one clause per open question, in graded wording ("is read as", "remains undeciphered", "is not known").
  - Never merge the two inscriptions, the two tanks, or Udayagiri with Udaypur.
  - "Nephew of Bhoja" must not appear; if Udayāditya is mentioned, "a kinsman of Bhoja".
- **Transition:** Proposals sorted and roles weighed, the book can say plainly what it thinks.

---

## AW.5 What the history argues *(advocacy, labelled · ~450 w)*

**Word target:** 450

- **Section statement:** By the end, the reader knows the book's own case:
  - Udaypur survived because it was used, worshipped in and lived in, not because it was set apart;
  - conservation that separates the temple from its town and hill would repeat the separation that left the hill, the wall and the palace exposed;
  - the realistic future is the one the record already points to: small measures, a closed protection gap, and residents treated as the town's keepers.
- **Purpose:** The interpretive movement the evidence justifies, and the book's close. The movement goes from Udaypur as a capital or a monument to Udaypur as a continuously inhabited town whose layers are all its history.
- **Paragraph plan:**
  1. **P1 — The register, and the lesson of the long view.** **Point:** Say in one plain sentence that what follows is the book's argument, not a finding. Then draw the interpretive movement from the chapters (callbacks by content, no summary):
     - a king's undertaking on a frontier hill (Chs 1, 4–6);
     - kept in worship while its corner shrine and hall were replaced and its town passed through other hands (1.3, Ch 10);
     - remembered by legends of how it survived (1.4);
     - protected, at last, as a temple apart from its town (Ch 11);
     - lived in by people who built on its ruins (Ch 12).

     The constant is use. Avoid "capital": the canon's "a place that was a capital" is not established (1.2 records Udayapura as Rājyapāla's eastern headquarters only; Devapāla resided there). Use "a royal town" or "a king's town".
     - E: (callbacks; no new items) · X: C13-JAGTA-HI-014 (T8) (Tiwari's question whether the temple is only carved stone for governments; quote at most a phrase, attributed)
  2. **P2 — The case.** **Point:** The book's advocacy, labelled ("this book argues"):
     - conserve the town and the hill as inhabited and working places;
     - close the gap that leaves the hill, wall and palace outside the temple's protection, as the survey proposed;
     - begin with the measures that cost residents nothing and tell visitors the town's history where it stands;
     - make any clearance a matter of residents' consent and benefit, as the one clearance on record was.

     Mishra's vision of a "heritage town" is endorsed only in that sense: a heritage *town*, still a town. His dream may be quoted once here ("a historian's last dream"), attributed to the tribute in Tiwari's book.
     - E: C13-JAGTA-HI-038 (T8) · C: C13-JAGTA-EN-022 (T8), C11-GEOHER-002 (T7), C13-JAGTA-EN-019 (T8) · X: C12-JAGTA-EN-010 (T8) (recall)
  3. **P3 — The close.** **Point:** Return to the village under the temple, the first image of the book (1.1), by content: the temple still in daily worship, the houses built on and out of the old town, the hill above with its bats and vultures and its broken wall. End on a concrete statement of what Udaypur is at the last record, not on an exhortation. Do not end on Tiwari's "resolve" (C13-JAGTA-HI-039 (T8)) or on "waiting to wake"; those are the sources' cadences, and the book's last word is its own.
     - E: (recall only) · X: C12-JAGTA-HI-014 (T8) (the house), C01-PANDE-010 (T5) (worship continuing; 1.1's item, recall)
- **Drafting guidance:**
  - Advocacy must be **visibly labelled** once at the start of the section ("This book's view is…") and must not leak into AW.1–AW.4.
  - Graded confidence still applies: the case rests on documented patterns, and P1's chain must use the chapters' own grades (for instance, "the temple has been read as begun in 1059").
  - No rhetorical questions, no imperatives addressed to the reader, no "we".
  - "Udaypur", never "Udaipur", except inside a quotation.
  - Keep the section the shortest in the Afterword.
- **Transition:** None; the book ends.

## Afterword: conflicts to present, unresolved

| Conflict | Where | How held |
|---|---|---|
| The evidence horizon: the GEOHER survey's date unknown | **AW.1 (home)** | "A survey made after 2021" until the date is found |
| Protection of the Naṭarāja ("protected" per the survey; state-protected per Tiwari via an official): no notification in the corpus | AW.2 | "Reported as protected by the state" |
| The hill as reserved forest (C02-KB-GEOHER-012) vs "unprotected" | AW.2 | Forest, not archaeological protection |
| "Parmar capital city" (survey) | AW.5 | Only inside quotation marks; never in the narrator's voice |
| Guest voices at Tiwari pp. 161–170 | AW.3 | Each proposal attributed only after the speaker is checked |
| Suresh Mishra (historian) / P. K. Mishra (ASI director) | AW.3–AW.4 | Never conflated |

## Afterword: hand-offs

- **In:** The letter Tiwari wrote in 2019 to a Collector of Vidisha, asking that the history "surviving alive in this town" be looked after and proposing work on the model of the Kashi Vishwanath corridor (C13-JAGTA-EN-001). It takes up Chapter 12's last turn: residents hoping for visitors, outsiders drawing up plans. It is the earliest dated proposal in the record, and it carries the Afterword's whole question: conservation of what, for whom, and at whose cost. The opening states the letter and its date only; its model is assessed later (AW.3).
- **Out:** There is no next chapter. The last paragraph returns to the opening image of 1.1, the village under the temple, by content. It must not summarise the book, exhort the reader, quote a source's rallying cry, ask a question, or claim any present condition beyond the last record.

## Afterword: changes from the master outline

1. **Boundary (Part I, I.6):** AW.2 compresses Ch 11 into a jurisdiction map in a few sentences and does not re-describe the survey's findings.
2. **Exclusions:** C11-TEMPLE-ECON-002 and -004 (Temple Economics is excluded).
3. **Length (U3):** about 2,750 words, accepted.
4. **Evidence pass:** coverage complete. No structural change.

## Afterword: research and verification flags

- Evidence horizon.
- The old canon's AW.1 wording is not in the maps.
- "Natraj" protection.
- The hill as reserved forest
- "Capital."
- Voices at pp. 161–170
- Two Mishras.
- "Raja Miyan"
- Figures inside proposals
- The Kashi Vishwanath corridor
- Bhojpur's double use.
- C11-TEMPLE-ECON-002/-004
- Stronger evidence wanted:
- **Before AW.1:** find the GEOHER survey's date (title page or preface).
- **Page-image checks:** Tiwari pp. 161–170 (speakers); C13-JAGTA-HI-007 (P. K. Mishra).
- **Legal review:** any recall of the mining allegation or the palace claim (U7); recall only, never re-tell.

---

# Cross-Chapter Architecture (updated by the evidence-grounded pass)

*The full architecture (threads, actors, terms, echoes, the duplication-risk table) is in the master outline, Part III. It still holds. This section records what the evidence pass changed or confirmed.*

## A. Chain of chapters (last move → first move)

| From → to | Last paragraph ends on | Next opens on |
|---|---|---|
| 3 → 4 | "Who held the hill itself in those years is not known." | Sīyaka II's eastern limit at Vidisha (C04-GAZ-001, C04-GANGULY-035) |
| 4 → 5 | The Udayeśvara as the one work a contemporary record assigns to the reign | The temple faces east but is entered from the west (C05-PANDE-002, -011) |
| 5 → 6 | The flag-bearer and the god's name at the east doorway (not read) | The six lines of V.S. 1137 and their named poet (C06-CII-006, C06-JAGTA-HI-008/-009) |
| 6 → 7 | Mosques and gates with Persian inscriptions: dated, not described | The nameless wall on the hill (C07-GEOHER-002) |
| 7 → 8 | Vikrama's tank and its stated uses (water as merit) | Dhāmadeva's four *biswa* given to the god, 1229 (C08-CII-020) |
| 8 → 9 | The time-keepers' family and its hereditary service | A lane of Hindu and Muslim neighbours (C09-JAGTA-HI-005) |
| 9 → 10 | The remembered deserted market of Daulatpur (memory only) | **The V.S. 1220 record naming a Gujarat king at Udaypur** (C10-PARTEMPLES-001, C10-CII-002) |
| 10 → 11 | The Gazetteer's "once a place of considerable importance" | Beglar's tour, 1871–72 (C07-PANDE-005) |
| 11 → 12 | The people at the record's edges | A family's house cleaned out of an excavation (C12-JAGTA-HI-014) |
| 12 → AW | Residents' hopes; outsiders' plans | Tiwari's 2019 letter (C13-JAGTA-EN-001) |
| AW → end | The village under the temple (1.1) | — |

The QC script prints each unit's Out beside the next unit's In (`plan_work/QC_REPORT.md`). All ten pairs were read and match.

## B. One primary home (rule applied by script, 15 Oct)

**Rule:** an item establishes (E) a claim in **one** unit only, its home. The home is the unit of its ID prefix; where neither unit is the prefix unit, the earlier unit is the home. Any other unit cites it as **C**, marked "(home Ch N: cross-reference)", and tells it in a clause, or reinterprets it for its own question (Part I, I.4 of the master outline).
- **22 duplicate establishing uses** were demoted (`_tools/demote_dupes.py`). They fall into four groups:
  - Ch 6 and Ch 10 shared the porch and political records. Ch 6 keeps the texts; Ch 10 keeps C10-PARTEMPLES-001 and C10-MADHYABHARAT-006.
  - Ch 7 and Chs 10–11 shared the mosques, buildings and protection rows. Ch 7 keeps them.
  - Ch 8 and Ch 10 shared Ganguly's governor items. Ch 8 keeps them.
  - Ch 11 and the Afterword shared the survey's condition items. Ch 11 keeps them; the Afterword keeps C13-GEOHER-004; Ch 12 keeps C12-JAGTA-HI-016.
- **Earlier hand fixes:**
  - C04-CII-119 → Ch 4;
  - C06-CII-011, -032 and -013 → Ch 6 (Ch 7 establishes the tank with C07-CII-003);
  - C07-MADHYABHARAT-011 and -012 → Ch 7;
  - C06-CII-037 and -038 → Ch 6;
  - C08-PANDE-011 → Ch 8;
  - C04-CII-131 → Ch 4;
  - C05-PANDE-008 and C05-GANGULY-012 → Ch 5 (the 11.1 paragraph is now recall-based).

## C. Evidence moved at plan stage

- **C10-GAZ-041, -042, -045, -046, -047** (1858–59; the Praja Mandal; Madhya Bharat, 1956): from 10.5 to 11.2. They also fill the master outline's flag that the state succession had no item.
- **C10-GAZ-052, -053** (census): from 10.5 to 12.1.
- **C10-GEOHER-001** (the survey's Paramāra attribution of the fort's antiquities): to 7.1 P4 as C.
- **The hill's sculpture:** home 7.1 P3a (from the merge).

## D. New evidence (kb-new, free local search)

- **C10-KBN-MADHYABHARAT-001 to -004** (Patil, *Cultural Heritage of Madhya Bharat*, pp. 15 and 43; T5): the Maratha settlement of Madhya Bharat from the 1730s to the 1790s, and the Maratha states under British paramountcy.
  - They are a regional frame for 10.5 P1, never Udaypur-specific.
  - They were sliced verbatim by `_tools/kb_new.py` and stored in `evidence_index/kb_new.jsonl`.

## E. Concepts introduced once (confirmed; see master outline Part III, E)

- **Glossed in Chs 1–3, never re-glossed:** *Bhūmija* (1.3), *kund* and *baoli* (2.4), *praśasti* (1.2).
- ***mahāsādhanika*:** first glossed in 10.1. The ledger shows 1.2 used it unexplained; 1.2 now adds the Caulukya master (U1) but still no gloss.
- ***biswa*:** unglossed in 6.4, glossed in 8.1 P2.
- ***pañcakula*:** glossed in 6.4, recalled in 8.1.

# Downstream Drafting Protocol (updated)

*The house voice, the failure table, evidence handling, chapter shape and continuity machinery are in the master outline, Part IV (P1–P10). They still bind. Updated here for the user's rulings of 15 October.*

1. **No paid API calls of any kind** for the rest of the project: no judge, verify, re-verify or final read, and no embeddings for knowledge-base search. The cost-guarded commands in `_pipe/inhouse.py` (judge, verify, reverify, finalread), `ledger.py build|update`, `kb.py`, `orchestrator.py`, `chapter_flow.py` and `pipeline3.py` are **not run**. Ledger updates are made by hand, or by a free script editing `book_ledger.md` and `book_ledger.json`.
2. **Sequence for each chapter:**
   1. read this plan's unit;
   2. print the quotations of every E and C item (`python -I -X utf8 drafting/_tools/quotes.py ID …`);
   3. write `drafting/run/chN/N.x.md` section by section, in order, each with the previous section's full text to hand;
   4. after each section, run the free checks (`UDAY_CFG=<cfg> python -I -X utf8 drafting/_pipe/inhouse.py check N.x`) and fix every "problem";
   5. after the chapter, run `build_outputs.py`, extended to the new chapter's cfg.

   Each new chapter needs a cfg (`drafting/chNN/cfg_chNNv1.py`, modelled on `ch03/cfg_ch03v2.py`) and an evidence pack built from this plan's IDs. Build the pack with `_pipe/extend_pack.py` from the evidence log, adding kb-new items from `evidence_index/kb_new.jsonl`.
3. **In-session verification** (replaces independent verification):
   - check every factual sentence against the quotations of the IDs it cites (the quotation, not a gloss);
   - match every quotation character for character against the source file in `Udaipur Books Markdown files\` (grep the exact string);
   - log anything unverifiable in the chapter report as a flag, never smoothed over;
   - re-read each paragraph after any cut (dangling "there", "its");
   - protect decimals ("1,229.9").
4. **Labelling:** every chapter report, `.docx` subtitle and progress entry states **"Facts verified in-session, not by an independent model"**, so the user can choose chapters for a later second check.
5. **Gap-filling:** free local search (grep or BM25 over the corpus Markdown) only. Each new item is sliced verbatim by `_tools/kb_new.py`, with its page from the marker in force, tagged `kb-new` with its tier. Gap-filling is used only where a section would otherwise land below 70% of its target, or where a flag names a gap the corpus can fill.
6. **Default rules for soft choices** (master outline P0):
   - items marked optional or "evidence pass" are omitted unless the section would land below 70%;
   - the first alternative wording is used;
   - "Note:" items never enter the running text.
7. **What needs the user:** any structural change (adding, removing, merging or reordering sections or chapters; moving evidence between chapters beyond this plan); any conflict this plan keeps open; anything touching the legal-review flags.
8. **Organizational changes to preserve:** master outline P10, plus this plan's:
   - the Ch 10 opening (V.S. 1220);
   - the Ch 8 opening (the gift);
   - 7.1 P3a;
   - the U2–U4 lengths;
   - the U6 instruction in 4.4 P2;
   - U7 in Chs 11–12.

# Global Evidence / Research Flags (updated)

**Needs the user's ruling:**
- **R1. Gazetteer share in 10.5** (Revenue, brass and the railway, 1720–1905): 27 of 42 cited items are from the 1979 Gazetteer (64%), above the 40% cap. For the district under Maratha and Gwalior rule, the corpus holds almost nothing else.
  - The plan already moved seven Gazetteer items to Chs 11–12 and added four Patil items (kb-new).
  - Options:
    - (a) accept the exception for 10.5;
    - (b) cut 10.5 to about 600 words, keeping P2 (the brass cover) and P5 (the verdict) at full length and compressing P1, P3 and P4;
    - (c) add the staged colonial sources after ingest.
  - Default if no ruling: (a), with the Gazetteer named in the notes only.

**Blocking checks:**
- **B1. The brass cover, V.S. 1841** (≈ 1784–85; sources say 1775). Must be checked before 10.5 is drafted (ROADMAP 14).
- **B2. The GEOHER survey's date.** Must be found before 12.1 and AW.1 state the evidence horizon.

**Legal review before publication (U7):**
- 11.4 (the 2021 eviction order and signboard: no names);
- 11.5 (illegal mining as a threat);
- 12.2 (Tiwari's mining-network allegation: one attributed sentence, no one accused named);
- 10.4 (the farman claim: claimants unnamed);
- any Afterword recall of these.

**Page-image checks (consolidated):**
- **Ch 4:** C04-CII-082 vs pp. 152/178; the "1513" / V.S. 1562 records; C04-GANGULY-101.
- **Ch 5:** C05-INTACH-002 (never used); the Amareśvara date.
- **Ch 6:** C06-JAGTA-EN-035 (gaḍh/gadya); C06-GANGULY-032 (V.S. 1366).
- **Ch 7:** INTACH pp. 54 and 58; C07-GAZ-004 and -007 (excluded).
- **Ch 8:** C08-GANGULY-016 in CII; C08-GAZ-014's source.
- **Ch 9:** Adhikari's footnote (C09-PARTEMPLES-001).
- **Ch 10:** C06-GANGULY-030.
- **Ch 11:** the Gwalior report years; the Land Revenue Code; GEOHER-008's site.
- **Ch 12:** GAZ p. 348 (1901); Tiwari pp. 161–170, p. 70, ≈ p. 63; the 1968 table.

**Staged public-domain sources** (leads only, `ocr_verify`; not evidence until hand-corrected and ingested):
- Bühler, *EI* I (Chs 4, 6);
- Beglar, ASR VII (Chs 5, 7, 11);
- Cunningham, ASR X (Chs 5, 6, 10, 11);
- the Gwalior report of 1925–26 (Ch 11).

**Research leads:** ASR IX p. 109, a V.S. 1137 inscription of Udayāditya of unstated provenance (Chs 4, 6). It is not evidence.

**Gaps to state in the text, not fill:** see master outline Part V.4, unchanged.

**Verification method:** all chapters from Ch 4 are verified in-session, not by an independent model. A later second check may be wanted for Ch 4 (dates, the three enemies), Ch 6 (readings) and Ch 10 (sequence).

# Continuity and Duplication Checklist (updated)

*Use the master outline's Part VI for every section, chapter and book-wide check. Add these:*

- [ ] **Per section:**
  - every cited ID's quotation has been printed and read (`quotes.py`);
  - every quotation has been matched verbatim against its source file;
  - the unverifiable items are logged.
- [ ] **Per section:** no item cited as E here is E in another unit (the home rule). Cross-references are a clause.
- [ ] **Per section:** the Gazetteer is ≤ 40% of cited items, or the section is 10.5 under the user's ruling R1.
- [ ] **Per chapter:**
  - the report carries the line "Facts verified in-session, not by an independent model";
  - the legal-review passages (Chs 10–12) are listed;
  - no API call was made.
- [ ] **Per chapter:** kb-new items, if any, are listed with source file, line, page marker and tier.
- [ ] **Book-wide after Ch 10:** Ch 1 §1.2/§1.3 (Caulukya governors, U1) and 10.1 agree in wording.
- [ ] **Book-wide:** run `plan_qc.py` again if the plan changes; the status table must stay green.
