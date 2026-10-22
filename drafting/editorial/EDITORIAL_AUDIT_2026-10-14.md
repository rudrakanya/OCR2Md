# Editor-in-Chief audit: the Udaypur book, its plan and its production system

*14 October 2026. This is an audit only. Nothing was launched or rewritten. The audit itself made no API calls: everything was done by reading the files, running free text searches over the corpus, and two research agents (one for external benchmarking, one for the book plan).*

---

## 1. Executive diagnosis

**What the system would produce if run unchanged.** Chapters 1 and 2 would be accurate, densely cited and well behaved, and they would read like an expert's annotated evidence file. Every fact would be traceable, but the reader would feel the machinery throughout. Measured on the current drafts (Ch1 v3, Ch2 v1, Ch3 v1):

- **Metronomic shape.**
  - Chapter 1's paragraphs average 143 words with a standard deviation of only 15, and 6.6 sentences each.
  - Sentences average 21–22 words; only 2–3% are ten words or fewer and 2–4% are 35 or more.
  - This uniformity of shape is the strongest "machine" signal in our prose. The binary templates ("not X but Y") are rare in the drafts and appeared mainly in calibration.
- **Footnote saturation.** One note every ~21 words, about 6.5 notes per paragraph, in all three drafts. A serious general history carries roughly one or two per paragraph. The reader experiences the apparatus, not the history.
- **No people.** Only 1–2% of sentences have a person as their subject (a king, a governor, a pilgrim, a priest, an archaeologist). The subjects are the village, the temple, the inscription, the survey.
- **The dynasty as an adjective.** "Paramāra" mostly modifies "temple", "style" and "gateways". The polity (Dhārā, Bhoja's collapse, Udayāditya's recovery, the eastern division, later governors, rival powers) is nearly absent from Chapter 1 and entirely absent from Chapter 2.
- **The reason is architectural, not stylistic.**
  - The evidence rubric classes Paramāra history in general as "contextual … background, not evidence" (`drafting/_runs/rubric.md`; `_master.md`: "the direct items carry the chapters").
  - The chapter packs were therefore drawn almost entirely from Udaypur-specific material.
  - Yet the corpus contains the full dynastic history: D. C. Ganguly's *History of the Paramāra Dynasty*, with chapters on Bhoja, "From Jayasiṃha to Jayavarman", the Mahākumāras, the fall of Malwa and administration (maṇḍala, viṣaya, pathaka). It also contains CII VII.2, *Inscriptions of the Paramāras, Chandellas, Kachchhapaghātas*.
  - The weakness is a retrieval and planning gap, not a corpus gap.
- **Paragraph-level control without book-level control.**
  - Sections are drafted in parallel, each blind to the others, and then "stitched". The stitch prompt literally says "the sections were drafted in parallel".
  - Every paragraph has been forced to produce a labelled interpretive sentence.
  - The result is locally argued paragraphs and a chapter with no arc.

**Greatest strengths (keep them).**
- Evidence discipline: verbatim quotes sliced by code, ID-level traceability, the fabrication and number checks, settled ranges, the canon rules on testimony, Gazetteer and praśasti, the verifier with targeted fixes, and the read-only corpus.
- The calibrated habit of not overclaiming, and the founded-or-renamed question kept open honestly.
- The cost controls.

**Greatest dangers.**
1. A book that is correct but unreadable.
2. A book about a temple-village that never shows the kingdom that made it.
3. A system whose quality signals (judge scores, check counts) reward compliance rather than history.

The fix is upstream: plan, evidence architecture and drafting order. More prose rules will not fix it.

---

## 2. External benchmark findings

These are the agent's findings, which I reviewed. I used only free, legitimate sources. Copies on Scribd, dokumen.pub, shadow libraries and archive.org uploads of in-copyright books were deliberately not opened.

| # | Author, title | What was accessible | URL | Why chosen | Read directly? |
|---|---|---|---|---|---|
| 1 | Anirudh Kanisetti, *Lords of Earth and Sea: A History of the Chola Empire* (2025) | Publisher preview PDF: the full Introduction, ~3,000 words (also excerpted by The Wire) | juggernaut.in/cdn/shop/files/Lord_of_Earth_and_Sea_Preview.pdf | Medieval dynasty, imperial temples, inscription archive, later myth; a general-reader success | Yes |
| 1b | Kanisetti, *Lords of the Deccan* (2022) | ThePrint excerpt (~1,900 words), **seen only through a summarising fetch**, not raw text | theprint.in/pageturner/excerpt/…/815169/ | Dynasty history for general readers; Tata Lit Live Book of the Year, Yuva Puraskar | Partial |
| 2 | Cynthia Talbot, *The Last Hindu Emperor* (2016) | Cambridge's official excerpt: Introduction pp. 1–10, with footnotes | assets.cambridge.org/97811071/18560/excerpt/9781107118560_excerpt.pdf | A king, a monument and 800 years of memory; structurally close to Udayāditya. AAS Coomaraswamy Prize 2018 | Yes |
| 3 | Richard M. Eaton, *A Social History of the Deccan, 1300–1761* (2005) | Cambridge's official excerpt: Introduction and opening of Ch. 1 (Pratāparudra) | assets.cambridge.org/97805212/54847/excerpt/9780521254847_excerpt.pdf | A senior historian writing medieval regional kings for wider readers | Yes |
| 4 | Manu S. Pillai, *Rebel Sultans* (2018) | Two permitted excerpts the author republished (~750 and ~1,200 words) | manuspillai.com/theprintrebelsultans/ ; manuspillai.com/firstpostrebelsultans/ | Bestselling Indian narrative history; mixed Sanskrit, Persian and European sources | Yes |
| 5 | William Dalrymple, *The Anarchy* (2019) | Scroll.in excerpt "with permission", ~1,900 words | scroll.in/article/934753/ | Narrative momentum from documents; Cundill finalist, Arthur Ross medal | Yes |
| 6 | Romila Thapar, "Somanatha and Mahmud", *Frontline* (1999); the precursor essay, **not the book** | ~7,000 words; about two-thirds read closely, via a Columbia teaching mirror | franpritchett.com/00islamlinks/txt_thapar_somnath.html | Temple, raid, inscriptions and contradictory memory: closest to Udayeśvara's reuse | Yes |
| 7 | Mary Beard, *SPQR* (2015) | **Reviews only** (NYRB; Lit Hub/NBCC) | nybooks.com/articles/2015/12/17/rome-inside-emperors-clothes/ | Fragmentary evidence, uncertainty in the open | No: second-hand |

**Not accessible:** Eaton's *India in the Persianate Age*, Dalrymple's *The Golden Road*, Thapar's *Somanatha* (the book), Upinder Singh, R. H. Davis, Khilnani. No claims are made about their prose, and no sales figures are claimed for any title.

**Craft principles observed in prose actually read** (general techniques, not voices):
1. **Open on a concrete thing in a place**, not a thesis: a floodplain, a statue plinth, a parade of treasure. *(Kanisetti, Talbot, Dalrymple, Eaton)*
2. **Let one object carry the argument.** Talbot reads one inscription phrase by phrase, and each phrase opens a later layer of memory. Thapar reads the 1264 bilingual inscription through who witnessed it and who sold land.
3. **Context comes before the event, briefly and materially** (taxes, trade, water), so that the event lands in a working world. *(Thapar, Kanisetti)*
4. **Conflicting evidence is organised by voice.** Thapar names five "representations" and walks through them. Eaton places each life on a biography–hagiography continuum, and says so once.
5. **Confidence is graded in verbs and adverbs, clause by clause** ("known to", "would seem", "may well have", "has little credibility"). There are no blanket disclaimers. *(Thapar, Dalrymple, Kanisetti)*
6. **Legend stays in the story under running attribution** ("the story goes", "it is said"): neither endorsed nor deleted. *(Pillai, Talbot)*
7. **Silence is treated as evidence, explicitly, and then reasoned from carefully.** *(Thapar; Kanisetti's footnote on the missing navy)*
8. **Disagreement and historiography go to the notes.** The text keeps the reader's question. Talbot settles a dispute over a king's death in a four-line note.
9. **Modern scholars are named in the text only when they are actors in the story** (Sastri building the Chola myth, Tod coining a label). Otherwise they live in the notes.
10. **The verdict comes right after the evidence, in one sentence, and then the narrative moves on.** *(Dalrymple; Talbot's "manifestly untrue")*
11. **Scale alternates on purpose.** A large claim is pinned at once to a countable or touchable detail. *(Kanisetti, Pillai, Dalrymple)*
12. **Rulers are made intelligible by function** (a hinge between state types; a working comparison), not by adjectives. *(Eaton, Talbot)*
13. **Landscape is a corridor or system along which things move**, not scenery. *(Eaton, Kanisetti, Thapar)*
14. **Dates are anchors**: exact dates for turning points, relative dates for flow, regnal dates once in brackets. *(Dalrymple, Eaton)*
15. **Paragraph openings carry the logic** ("Yet", "From now on", "Twelve months later"), so the closing sentence can simply deliver its fact. *(Dalrymple, Thapar)*
16. **Shape varies widely.** There are four-word pivots, 250-word accumulating paragraphs, and quotations left to stand.

**Failure modes these books avoid.** Our drafts show several of them:
- aphoristic paragraph endings (the weakest sentences in Kanisetti and Pillai are exactly their quips);
- reflexive rebuttal framing;
- source-led sentences;
- uniform paragraph shape;
- blanket hedging;
- announced interpretation ("this shows that");
- abstract nouns with no object attached;
- even-handed listing of every scholar's view in the main text.

**From reviews only (Beard):** the book opens on one datable crisis, moves back and forth in time, and keeps its inconsistencies visible. This is a second-hand observation.

---

## 3. Proposed house voice

The narrator is **a historian standing in Udaypur and looking outward**. The narrator knows the kingdom, reads stone and paper with equal care, and tells the reader what happened, to whom, and how we know, in that order of emphasis.

- **Grounded.** Each chapter and most sections begin in a place or with an object or a person: the hill seen from the Basoda road, the broken slab in Gwalior, Bhoja's dam. The argument grows out of the thing.
- **Narrative by default, analytical when it counts.** Events and changes are told in sequence with people as agents wherever the evidence names them: Udayāditya, the governor Lūṇapasāka, Devapāla, Muhammad Tughluq's men, the Scindia general Khande Rao Appaji, Cunningham, Garde, today's priests and quarrymen. Explicit interpretation is reserved for the places where the history turns. It is short, comes after the evidence, and is never repeated.
- **Two scales.** Udaypur is the centre of gravity. The Paramāra world (Dhārā, Bhoja's collapse, the eastern march at Bhilsa, rival powers, later governors) enters when it changes what Udaypur means, and then the narrative returns.
- **Confident and graded.** Established things are stated plainly ("was"). Probability and possibility are graded on the clause they qualify ("probably", "may"). Proposals carry their status ("has been read as"). Traditions are told as memory ("the village tells …"). Panegyric is read as a king's self-portrait.
- **Economical apparatus.** Normally one note per paragraph, or per distinct claim cluster. Scholars are named in the text only when they are actors or when their disagreement changes the answer.
- **Plain, varied English.** Concrete nouns and working verbs. Sentence and paragraph length follow the job. No house rhythm: no closing aphorisms, no colon-reversals, no stacked triplets.

**How it uses the benchmarks without imitating them.**
- It takes structural techniques, never voice, phrasing or mannerisms: object-led openings, context before event, voice-sorted evidence, verdict after evidence, graded verbs, running attribution for legend, notes for historiography.
- No author is named in any prompt.
- No external sentence enters the style brief. Its worked examples will be built only from our own Udaypur material.

**A short demonstration from our own material**, written by me from items already in the pack (IDs omitted for reading; not for the prompt):

> *Round 3:* "Udaypur was a place of considerable medieval importance, but its road and rail approaches now pass through neighbouring centres. […] The approach reveals a former centre now dependent on its neighbours."
>
> *House voice:* "Ten kilometres out on the road from Ganj Basoda, two of Udaypur's hills stand out among the hillocks on the horizon, and some five kilometres from the village the temple Udayāditya built comes into view. The village itself, when the road reaches it, is a large one in Basoda tahsil, 13–16 kilometres from the market town and its railway station, with a metalled road running east from Bareth on the line between Bina and Bhilsa. The compilers of the district gazetteer in 1979 called it 'once a place of considerable importance'. The order in which a traveller meets it (hill, then temple, then village) is the order of the problem this book has to explain."

The demonstration paragraph gets the hills, the temple, the distances, the railway and the gazetteer's phrase in front of the reader with a single interpretive move at the end. That move is the book's question, not a restatement of the paragraph. (If used in the book, the last clause would be recast without "this book", which the house rules ban.)

---

## 4. Pipeline audit

| Component | Verdict | Decision and reason |
|---|---|---|
| `run.py` (API runner, budget, retries, model pricing) | **KEEP** | Sound. |
| `cfg.py` per-chapter configs | **KEEP**, MODIFY content | Chapter briefs rewritten around historical purpose; canon corrections (see §13). |
| Corpus and Chroma (read-only), `kb.py` retrieval with verbatim slicing | **KEEP** retrieval method, **MODIFY** use | Add dynastic and regional retrieval from GANGULY and CII. Allow contextual items to be cited as evidence *for context*. Raise the per-chapter new-item cap for Chapter 1 (see §13). |
| Evidence rubric: Direct/Contextual, "contextual = background, not evidence" | **MODIFY** | This is the root cause of the dynasty appearing as an adjective. Contextual items become citable evidence for wider history. Direct items still carry claims about Udaypur. |
| Evidence-hierarchy rules (canon §1 source matrix; Reference doc categories) | **KEEP** and **MODIFY** | Consolidate into one explicit hierarchy that the writer, judge and verifier all receive (see §5). |
| Evidence packs (all items handed to the section writer) | **MODIFY** | Tier each paragraph's items as *establishing*, *corroborating* or *context*. The writer is told plainly that not every item needs to appear. |
| Outlines with paragraph plans and Points | **MODIFY** | Points become "historical work". Each section gets a statement of what the reader understands at its end. Each chapter gets an arc. See §6–7. |
| Interpretive briefs | **MERGE** into a single chapter plan | Thesis and claims live with the outline, not in a parallel document the writer must reconcile. |
| `pipeline2.py` drafting order: sections drafted in parallel, then stitched | **REPLACE** | Draft **sequentially**: each section is written with the chapter plan and the already-chosen text of the sections before it. Two candidates per section remain. This is the single biggest structural fix for continuity and voice. |
| Writer rules (AUTHORED_RULES 1–10) | **REPLACE** | A short set of principles (see §5): facts cited, inference tagged internally, debates to notes, Points as work, evidence hierarchy, no conflation, chronology visible. The interpretive-sentence quota, function labels, calibration examples and "one plan paragraph per paragraph" are removed. |
| `SUBJECT_RULES` | **MODIFY** | Becomes "sources are not the subject". The place, its people and the dynasty may all be subjects. The source-led detector stays as information for the judge. |
| `BASE_BRIEF` (120–200-word paragraphs; topic sentence about the place; facts and citation rules) | **MODIFY** | Keep the facts, citation, quotation and meta-commentary rules. Remove the paragraph length band and the topic-sentence template. |
| Judge | **MODIFY** | New criteria: historical narrative; historical work (Points delivered as a whole, section statement achieved); coherence with the preceding text; evidence discipline; voice; prose (including template frequency and uniform shape); fidelity below 6 cannot win. It also returns the Points missed and INT-TRIVIAL sentences, judged semantically. |
| Edit (judge improvements) | **KEEP** | It now also receives the chapter-so-far for continuity. |
| Stitch | **REMOVE** | Redundant once drafting is sequential. Its job (continuity, repetition across sections) moves into the author's pass. This saves about $0.3 per chapter. |
| Author's pass (flagship) | **MODIFY**, never cut | Becomes the developmental and voice pass: arc, transitions, people as agents, varied shape, removing templates and repetition. Same guards: no new facts, IDs unmoved, notes unchanged. |
| Verifier and fixer | **MODIFY** | Each tagged inference is judged with its whole paragraph, so INT-TRIVIAL is semantic. MISREPRESENTED gains: conflation of distinct objects, a proposal hardened into fact, tradition presented as the event it narrates, correlation presented as cause (environmental determinism), and praśasti claims presented as events. One fix round and re-verification stay. |
| Polish | **KEEP**, optional | First to be cut if needed. |
| `validate.py`: IDs, verbatim quotes, fabrication (names, numbers), uncited facts, settled ranges, meta-commentary, banned list, duplicates | **KEEP** | Essential safeguards. |
| `validate.py`: per-paragraph interpretive requirement, function labels | **REMOVE** | Actively harmful (see §5). |
| `validate.py`: fact-per-sentence, monotony, source-led counts | **KEEP as diagnostics** | Reported to the judge; not gates. |
| `validate.py`: section word bands of 90–110% | **MODIFY** | Section bands relax to 80–120% and the chapter total band stays. The tight band produced padding (Ch3 v1 repeated one fact five times). |
| `validate.py`: 6-gram check against the writing sample | **REMOVE** | The sample is a spiritual discourse and is no longer used. |
| `subject.py` | **KEEP** (diagnostic) | |
| `footnote.py` | **MODIFY** | **Consolidate notes**: one note per paragraph, or per distinct claim cluster where attribution must stay unambiguous, listing sources in text order with pages. IDs stay in HTML comments. Chicago style unchanged. This changes nothing in the evidence, only what the reader sees. |
| `make_docx.py` | **KEEP** | |
| `report.py` | **REPLACE** with `report2.py` | Points next to the passage that delivers them, verifier counts (including INT-TRIVIAL and INT-OVERREACH) before and after, template and shape statistics as diagnostics, notes per paragraph. |
| `refine.py`, `rhythm.py` | **REMOVE** from the authored path | They patched older pipeline failures, and their goals are now covered by the author's pass. |
| `style.py` (learning from a sample PDF) | **REMOVE** | Retired. The house voice is defined by the new brief. |
| `calib.py` | **MODIFY** | Redesigned per §10. |
| `[INT]` tag | **KEEP, internal only** | Marks uncited inference so the verifier can test it. It is never required, never function-labelled, and stripped from output. |

---

## 5. Style-rule audit

**Essential safeguards (keep):**
- facts only from supplied quotes;
- every factual claim traceable to IDs;
- verbatim quotations;
- no fabricated names or numbers;
- settled ranges;
- canon on testimony, the Gazetteer, panegyric and old-OCR items;
- debates to notes;
- no meta-commentary;
- the "Udaypur" spelling and the diacritics policy;
- Indic terms glossed once;
- no fictionalised thoughts, scenes, motives or sensory detail;
- conflation ban (generalised from the two-line inscription: compatibility is not identity);
- the evidence hierarchy (below).

**Useful preferences (keep as guidance, not gates):**
- at most about one named source per paragraph unless historiography is the point;
- quotations short and few;
- concrete nouns and working verbs;
- people as agents where named.

**Redundant:**
- the n-gram sample check;
- `refine.py` and `rhythm.py` passes;
- separate "subject" and "source-led" rules that duplicate each other;
- a 30-item banned-phrase list where about 10 do the work.

**Producing formulaic prose:**
- 120–200-word paragraphs, "each opening with a topic sentence about the place";
- "governing claim early, close on its consequence" and the four paragraph templates (style brief §2);
- "short sentences land a point, one or two per paragraph";
- the 90–110% section bands;
- "most sentences are about Udaypur" (it pushes the dynasty and people out).

**Actively harmful:**
- the per-paragraph interpretive-sentence requirement and its code check;
- function labels;
- "the Point appears as the [INT] sentence";
- calibration sentences embedded in prompts;
- parallel section drafting;
- per-sentence footnoting as the reader sees it;
- the rubric's "contextual = background, not evidence".

**AI-shape monitoring.** Template frequencies, sentence-length spread, paragraph-length spread and agent-subject share will be *reported* per chapter, against targets set loosely from our benchmarks. They are not enforced as gates.

**The new evidence hierarchy**, given to the writer, judge and verifier, strongest first for medieval events:
1. contemporary or near-contemporary inscriptions, read critically: a praśasti is also self-representation;
2. the standing fabric and archaeological observation;
3. later inscriptions (for example the 1513 record, retrospective);
4. documentary and administrative records;
5. modern scholarship (named when it disagrees);
6. colonial-era observation;
7. modern survey and the Gazetteer (the modern setting);
8. oral and local tradition and Tiwari's testimony: evidence for **memory**, not for the event narrated;
9. modern heritage narratives (never adopt their superlatives);
10. this book's own inference (tagged, verified).

---

## 6. Book map and chapter-architecture audit

### 6a. Book-level map

Based on `chapters.md`, the authoritative list of 13 units. The 19-unit Detailed Outline and the dossiers number differently: dossier "C04" is Before Udaypur, while ID prefix C04 is the Paramāras chapter.

| Ch | Central historical question | Chronology / geography | Principal actors | Main evidence | Paramāra context needed | Largest risks |
|---|---|---|---|---|---|---|
| 1 Historical Memory and the Making of a Place | How did today's village come to hold the remains, records and memories of a far more important place? | Present, with glances back to 1059–1080 and the layers since; the village and its approaches | residents, Tiwari (witness), Udayāditya (as named founder) | survey, testimony, Gazetteer, inscriptions (as objects) | the dynasty as a polity in outline: Dhārā, the eastern march, Bhoja's fall, Udayāditya | *Evidence:* lineage claims. *Structure:* a methods chapter in disguise (§6b) |
| 2 Betwa Valley | What could this country give and withhold to people who settled and built here? | Deep time to now; Betwa basin, Vidisha to Udaypur | almost none: the agents must be farmers, builders, Bhoja's engineers | Gazetteer (1979), GEOHER, hydrology papers, Bhoja material | Paramāra hydraulic and temple practice; Bhilsa as an eastern seat | *Evidence:* modern data projected backwards. *Structure:* a physical-geography report |
| 3 Before Udaypur | What lay on and around this ground before the eleventh century? | Prehistory to c. 1000; Vidisha, Besnagar, Udayagiri, the hill | Mauryas to Pratihāras (background) | Gazetteer, survey, dynastic | the setting the Paramāras inherited | Gazetteer-heavy (48–53% of 3.1–3.4); proximity claims are thin |
| 4 The Paramāras and the Foundation of Udaypur | Who were the Paramāras, and how, why and by whom was Udaypur founded or renamed? | c. 900–1093; Malwa, Dhārā, Bhilsa, Udaypur | Upendra … Muñja, Bhoja, Jayasiṃha, Udayāditya; Chaulukyas, Kalachuris, Cāhamānas | Ganguly, CII, praśasti, Bhoja books | the core of the book | *Evidence:* the lineage contradiction (see §13). *Structure:* **overloaded**: it merges three 19-unit chapters (C5 + C6 + C7) with 682 mapped items |
| 5 The Udayeśvara Temple | What did the temple say about its builder, and how was it made? | 1059–1080; the temple, against Un, Nemawar, Bhojpur | Udayāditya, craftsmen | Pande, Hardy, Kramrisch | Bhūmija as the dynasty's style; royal patronage | Becoming a temple monograph |
| 6 Inscriptions and Intellectual Life | What do Udaypur's stones record, and about whom? | 1059–1600s | kings, governors, pilgrims, masons | CII, SERPENT, Pande | praśasti as royal self-portrait; later Paramāra records | Becoming an epigraphic catalogue; no edited texts in the corpus |
| 7 Wider Built Heritage | What did later builders add and why? | pre-Udayāditya fort to 1632 | Tughluq, Mandu, Mughal officials | survey, Patil, JAGTA | the fort and walls in Paramāra context | Becoming an inventory |
| 8 Religion and the Material Life | How did worship, land and work sustain the place? | 11th c. to modern | Śaiva institutions, cultivators | Pande, Gazetteer, survey | land grants (corpus thin) | Projecting modern economy backwards |
| 9 Society and Cultural Life | Who lived here and how is the past remembered? | modern, looking back | residents, storytellers | JAGTA, survey | memory of the dynasty | Testimony treated as history |
| 10 Political Change and Economic Decline | What happened to Paramāra Udaypur as the dynasty weakened and new powers ruled? | 1093–1645 | Naravarman … Devapāla, Chaulukyas, Candellas, Khaljīs, Mandu sultans, Mughals | Ganguly, CII, Persian inscriptions (not edited in the corpus) | **later Paramāras: currently only a sub-topic** | *Evidence:* thin on Sultanate and Mughal. *Structure:* 160 years of later Paramāra history squeezed |
| 11 Udaypur in the Modern Period | How did the place become a "monument"? | 1775 to independence and after | Scindias, Cunningham, Beglar, Garde, ASI, Forest Dept | Pande, CII, survey | — | Colonial originals not in the corpus |
| 12 Udaypur Today | How does the town live with its past? | c. 2011–22 | residents, Tiwari, officials | JAGTA, Gazetteer | — | One-source chapter |
| 13 Afterword | — | present | — | survey, testimony | — | Advocacy tone |

**Assessment of the order.**
- **The sequence is defensible:** place (1), land (2), deep past (3), dynasty and foundation (4), the monument (5–7), society (8–9), after the kings (10–11), now (12–13).
- **It has three weaknesses.**
  1. The dynasty enters substantively only in Chapter 4. Chapters 1–2 must therefore make the Paramāras present as a polity in outline, or the first quarter of the book has no kings.
  2. Chapter 4 carries three chapters' worth of history.
  3. The later Paramāras (1093–1305) have no proper home.
- **Recommendation (does not block Chapters 1–2):** split Chapter 4 into two chapters.
  - **4 "Malwa and the Paramāras, to the death of Bhoja"**;
  - **5 "Udayāditya and the Founding of Udaypur"** (crisis, recovery, the foundation, the eastern division).
- Then give Chapter 11 (the present Ch10) a full opening section on the later Paramāras and the contested east.
- The book becomes 13 chapters plus the Afterword.

### 6b. Chapter 1 as a chapter

**Current order:** 1.1 Arrival, 1.2 Long memory, 1.3 Epistemic discipline, 1.4 Naming, 1.5 Stance.
- It is organised by kinds of evidence. Two of its section titles ("Epistemic discipline", "Stance") name methods, not history.
- The founded-or-renamed argument (1.3) comes before the name, the praśasti, the dates and the accession (1.4–1.5) on which it depends.
- The chapter ends on survival legends rather than on the question that the land (Chapter 2) begins to answer.

**Proposed arc.** Present puzzle, then what the place was, then how it changed through time, then how we know, then the open question, then the land.

| New § | Title (working) | Historical work | Draws on current | ~words |
|---|---|---|---|---|
| 1.1 | The village under the temple | Arrival; scale; houses inside the old town's gateways; memories pointing to the founder; the name now confused with Rajasthan's Udaipur | 1.1 P1–P6, 1.4 P5 | 850 |
| 1.2 | A king's town on Malwa's eastern edge | The Paramāras in outline as a polity centred on Dhārā; Bhoja's fall and Udayāditya's recovery; one name for town, temple and tank; a seat of the eastern division; the Nēmaka house. Ch4 has the full story | 1.4 P1–P3, 1.5 P4, 1.2 P1, **new context items** | 850 |
| 1.3 | Eight centuries in one precinct | Chronological layers: later Paramāra governors (1171–73, 1229); a Candella king at Bhāillasvāmin in 1134; 1305; the 1330s mosque in the court; Mandu and Mughal building; the Scindia brass; the state's custody | 1.2 P1–P5 | 850 |
| 1.4 | How Udaypur is known | The praśasti as the dynasty's self-portrait, broken and in Gwalior; two dates; scholarship since the 1870s; the pilgrims' inscriptions; the legends as memory | 1.5 P1–P3, P5, 1.2 P6, 1.3 P5 | 750 |
| 1.5 | Founded or taken over? | The open question: proposals against an absence and a tradition; what foundation versus appropriation would mean; closing on the ground both answers stand on (to Ch2) | 1.3 P1–P4 | 700 |

### 6c. Chapter 2 as a chapter

**Current order** (river, monsoon, rock, forest, site) is the order of a physical-geography textbook. People arrive only in 2.5, and 2.4 (wildlife, lichens) has little historical purpose.

**Proposed arc.** From what the land withheld, to what it offered, to what people (kings and villagers) made of it. It ends on the setting a founder found, without claiming that the land caused the founding.

| New § | Title (working) | Historical work | Draws on current | ~words |
|---|---|---|---|---|
| 2.1 | Where the water runs, and where it does not | The Vētravatī as Vidisha's river; the Kewtan a kilometre off; the upper Betwa runs mainly in season; wells fail in summer | 2.1 P1–P4 | 850 |
| 2.2 | The rains and the farming year | Four wet months; bad years in runs (1899–1900); black soil; kharif and rabi; wells and tanks; the doab comparison; the modern trend in a note | 2.2 P1, P3, P4; 2.3 P5; 2.5 P4 | 850 |
| 2.3 | A seam of stone | Trap worn back from sandstone; the hills as erosional remnants; dry heights and caves; forest on the slopes and its use; the temple's stone from the hill close by | 2.3 P1–P4; 2.4 P1–P2; 2.5 P5 | 900 |
| 2.4 | Water made by kings and villagers | Bhoja's dam and the Bhojpur temple; the treatise's ideal site; Udaypur's tanks, kunds and stepwells; tank water for fields and well water for drinking | 2.5 P1–P3; 2.1 P5 | 900 |
| 2.5 | A town of its own stone | Stone from the founding to today's quarries; the setting a founder found, and what it did and did not determine; to Ch3 | 2.5 P6 | 500 |

**Moved or cut:**
- wildlife (1968 shooting block, bird lists) goes to Ch12;
- the lichen dating proposal goes to Ch7 (the fort);
- heat and cold become a clause;
- the modern climate trend goes to a note.

---

## 7. Point audit

**Chapter 1 (27 Points).**
- **Retain:** 1.1 P2 (the scale puzzle), P3 (living inside the old town; rewritten with residents as agents); 1.2 P3 (partial survival against the legends), P4 (later builders added to the old town), P5 (patrons changed, worship continued); 1.3 P2, P3 and P4 (the founding debate and its stakes); 1.4 P1 (naming as the act), P2 (the dates and the founder's standing), P3 (Nēmaka house under the royal name), P4 (the names drifted, the place-name held); 1.5 P2 (vivid in praise, thin in fact), P5 (legends turn partial survival into deliverance).
- **Rewrite:**
  - 1.1 P1: the approach. Hill, then temple, then village is the order of the problem. It must stop duplicating P2.
  - 1.1 P6: no outline-revealing ending.
  - 1.2 P1: Udaypur as a seat in a polity, not a precinct.
  - 1.5 P4: the accession as the circumstance of the founding, the crisis after Bhoja, framed per the canon correction in §13.
- **Merge:** 1.1 P4 with P5 (memories pointing to the founder; Berni Mata as one instance); 1.5 P1 with P2 (the broken slab as a self-portrait); 1.3 P1 into the new 1.4 (records).
- **Move:** 1.2 P6 (pilgrims' inscriptions) and 1.3 P5 (a late archive) to the new 1.4; 1.4 P5 (name confusion) to 1.1.
- **Demote to a sentence:** 1.2 P2 (Ramgarh and Nemawar as followers), with the three named assessments reduced to the one that matters; 1.5 P3 (the two dates) folded into 1.4.
- **Delete:** none outright. Everything is evidenced. The gain is in fewer, larger paragraphs.
- **Missing Points (new):**
  - (a) the Paramāras as a polity: Dhārā, the extent of Udayāditya's kingdom "at least up to … Bhilsa on the east";
  - (b) Bhoja's fall and Udayāditya's recovery as the moment of the founding;
  - (c) the contested east after him: a Candella king residing at Bhāillasvāmin in 1134; Paramāra governors still at Udaypur in 1171–73 and 1229;
  - (d) 1305 as the end of the Paramāra state in Malwa (in outline).

**Chapter 2 (25 Points).**
- **Retain:** 2.1 P1 (Vidisha's river, not Udaypur's), P4 (the same rock gives stone and withholds water), P5 (as the hinge to storage); 2.2 P3 (bad years in runs), P4 (the rabi leans on held water); 2.3 P2 (the seam and the temple's stone); 2.5 P2 (made water ordered by use), P3 (Bhoja's dam), P6 (a town of its own stone).
- **Rewrite:**
  - 2.3 P1: remove the determinism ("rock and height before water");
  - 2.5 P1: present the treatise's norms as norms; attribution to Bhoja needs an item, see §9;
  - 2.4 P1–P2: forest as land use (grazing, felling, the plough).
- **Merge:** 2.1 P2 into P1; 2.1 P3 with 2.2 P1 (seasonality); 2.3 P3 with P4 (hills as remnants; dry heights); 2.5 P5 into 2.3 P2 (the temple stone, in one place); 2.5 P4 into the farming section.
- **Demote:** 2.2 P2 (heat) to a clause; 2.2 P5 (modern trend) to a note.
- **Move:** 2.4 P3 (wildlife) to Ch12; 2.4 P4 (lichens) to Ch7.
- **Missing Points (new):**
  - (a) Bhilsa and the Betwa in Paramāra political geography: why the eastern seat sat in this valley, as setting only;
  - (b) the Paramāra pairing of temple and reservoir (Bhojpur's temple and dam; Udaypur's town, temple and tank) as practice, not cause.

---

## 8. Paramāra-context audit

| Where needed | What the reader needs | Can the current evidence supply it? |
|---|---|---|
| Ch1 1.2 | Who the Paramāras were; Dhārā as the centre; the kingdom's eastern reach | **Yes, in the pack but unassigned:** C01-KB-GANGULY-004 (the kingdom reached "Bhilsa on the east"), C01-GANGULY-023 (feudatories at Udayapur), C01-BHOJA-TIMES-006 (towns that grew under the Paramāras), C01-GAZ-015 (the eastern boundary to Vidisha) |
| Ch1 1.2 | Bhoja's fall; Jayasiṃha; Udayāditya's recovery | **Partly** (C01-KB-GANGULY-008, C01-KB-CII-003, C01-KB-JAGTA-EN-012). Ganguly ch. V has the full account: retrievable |
| Ch1 1.2 | Udayāditya's relation to Bhoja | **Conflicting.** The canon's "nephew … junior branch" has **no primary witness in the corpus** (Reference doc §Ch4.3); CII rejects the 1562 genealogy. This must be framed as disputed (see §13) |
| Ch1 1.2–1.3 | How the kingdom governed the east (maṇḍala, mahādvādaśaka, pathaka) | Names only in the packs (C01-GANGULY-005, C01-CII-010). **Ganguly ch. VIII covers administration**: retrievable |
| Ch1 1.3 | The east after Udayāditya: Naravarman to Jayavarman; Candellas; Gujarat's annexation of Malwa; the Mahākumāra branch near Bhopal; Devapāla | **Thin in the packs; rich in the corpus** (Ganguly chs. V–VII: 32–43 mentions each of Naravarman, Jayavarman, Arjunavarman; CII: 50+) |
| Ch1 1.3 | 1305 and the Sultanate in Malwa | **Thin**: C10-PARTEMPLES-003 (borrowed), with scattered Gazetteer and Patil material |
| Ch2 2.4 | Paramāra water works; Bhojpur temple and dam | **Yes** (C02-BHOJDEV-HI-001, C02-RAJABHOJ-EN-003/004, C02-BHOJA-TIMES-001/002/003; RAJABHOJ-EN-004 is a modern popular account, so it must be attributed) |
| Ch2 2.4 | The Samarāṅgaṇasūtradhāra as Bhoja's | **No in-text item** says so; only the book's title does. Probably retrievable from BHOJA-TIMES and Ganguly |
| Ch2 2.1/2.5 | Bhilsa (Bhāillasvāmin) as the eastern seat; the Betwa route | **Partly** (Ch1 items; C02-RAJABHOJ-EN-004). Medieval routes are absent |

---

## 9. Research-gap report

| Rank | Gap | What the reader needs | Why current sources are insufficient | What would resolve it | Where used |
|---|---|---|---|---|---|
| **ESSENTIAL** | Dynastic narrative c. 1000–1093 and 1093–1305 in the packs | The polity behind Udaypur | The rubric excluded contextual items; the corpus has them | **In-corpus retrieval** from Ganguly chs. IV–VIII and CII VII.2 (no acquisition) | Ch1 1.2–1.3; Ch4; Ch10 |
| **ESSENTIAL** | Udayāditya's relationship to Bhoja and the accession date | Who the founder was and when he ruled | Conflicting secondary readings; "nephew" unsupported by any primary witness | Retrieval of the CII and Ganguly discussions now; **post-1933 scholarship** later (P. Bhatia, *The Paramāras*, 1970; K. C. Jain, *Malwa through the Ages*, 1972): in copyright, library access needed | Ch1 1.2; Ch4 |
| **ESSENTIAL** | Paramāra territorial administration | What a "seat of the eastern division" meant | Names only | Ganguly ch. VIII; CII grants (in corpus) | Ch1 1.2; Ch4; Ch8 |
| **DESIRABLE** | The treatise's attribution to Bhoja | Whether the treatise's norms are the dynasty's own | No item | BHOJA-TIMES or Ganguly retrieval (in corpus) | Ch2 2.4; Ch6 |
| **DESIRABLE** | Sultanate Malwa and 1305; Mandu; Mughal Sarkar Chanderi | What changed after the Paramāras | Scattered | External: U. N. Day, *Medieval Malwa* (1965; copyright); edited Persian inscriptions (Epigraphia Indica, Arabic & Persian Supplement) | Ch1 1.3 (outline only); Ch10 |
| **DESIRABLE** | Colonial reports (Cunningham ASR VII and X; Beglar 1871–72; Bühler's 1888 edition in EI I) | How Udaypur became a monument; the first readings | Known only through Pande and CII | **Public-domain originals, legally free on the Internet Archive and Digital Library of India.** They would need OCR and a *separate* collection, since `chroma_db` is read-only | Ch1 1.4; Ch6; Ch11 |
| **DESIRABLE** | Paramāra hydraulic works beyond Bhojpur | Whether temple and reservoir together was dynastic practice | Bhojpur only | Ganguly ch. VIII, Rajpurohit (in corpus), then external | Ch2 2.4; Ch7 |
| **OPTIONAL** | Medieval routes and trade around Bhilsa | Why the east mattered economically | Absent | External regional studies | Ch2; Ch8 |
| **OPTIONAL** | Scindia-era administration and records | The 1775 gift and later maintenance | Two items | Gwalior State records (external) | Ch11 |
| **OPTIONAL** | Udaypur excavation reports (IAR) | Pre-Paramāra occupation | Survey proposals only | *Indian Archaeology – A Review* (ASI; partly online) | Ch1 1.5; Ch3 |

No gap will be filled with unsourced knowledge. Where a gap remains, the text frames the question, or the matter is listed as open.

---

## 10. Revised round-4 calibration

It uses the same four paragraphs for comparability: 1.1 P1, 1.3 P2 (→ new 1.5), 2.1 P5 (→ new 2.1/2.4 hinge) and 2.3 P2 (→ new 2.3). The difference is that **each is written inside its host section**, because isolated paragraphs cannot show arc, transitions or voice.

1. **Prerequisites (editor work, no API):**
   - the approved chapter plans for both chapters: arc, section statements and revised Points with evidence tiers;
   - the new style brief with worked examples from our material;
   - the new writer, judge and verifier rules;
   - the targeted in-corpus context retrieval for the host sections.
2. **Draft the four host sections**: new 1.1, new 1.5, new 2.1 and new 2.3, each written once by the production writer (sequential mode). Each receives:
   - the chapter plan;
   - the preceding section's text (from the current draft, as a stand-in);
   - the section statement;
   - Points and tiered evidence.
3. **Code checks** (fidelity only) and **one repair pass** if a fidelity check fails.
4. **Production judge and verifier** run on each section. This tests whether the machinery sees what an editor sees (semantic INT-TRIVIAL, conflation, determinism).
5. **The editor's evaluation.** I extract the four target paragraphs and set each beside rounds 2–3 and the original. I score each against the user's 14 questions, plus a section-level read (arc, transitions, voice), and compare my findings with the judge's and verifier's.
6. **Launch rule.**
   - At least 3 of 4 pass all 14 questions;
   - none overreach;
   - the four host sections read as history in one voice;
   - the judge and verifier catch the failures I find.
   - If any of these fails, stop and report. Because the bar is editorial judgement, I will show you round 4 before launching even if it passes.

---

## 11. Files to change

| File | Change |
|---|---|
| `drafting/_pipe/pipeline2.py` | Sequential section drafting with chapter-so-far context; new writer principles; new judge criteria and outputs; stitch removed; developmental author's pass; verifier gets paragraph context and new categories; fixer updated |
| `drafting/_pipe/validate.py` | Remove the interpretive-sentence and label checks and the n-gram check; diagnostics (fact-per-sentence, monotony, template frequency, shape spread) reported but not enforced; section bands to 80–120% |
| `drafting/_pipe/footnote.py` | Note consolidation (per paragraph or per claim cluster); IDs kept in comments |
| `drafting/_pipe/kb.py` (+ chapter cfg KB lists) | Contextual dynastic retrieval from GANGULY and CII; contextual items citable for context |
| `drafting/_pipe/calib.py` | Round-4 design (section-embedded) |
| `drafting/_pipe/report2.py` (new) | Points next to their passages; verifier before/after counts including INT-TRIVIAL and INT-OVERREACH; shape and template diagnostics; notes per paragraph |
| `drafting/_pipe/refine.py`, `rhythm.py`, `style.py` | Removed from the authored path (files kept, not called) |
| `drafting/style/style_profile.md` | Rewritten as the house-voice brief, sections A–H, with worked examples from Udaypur material only |
| `drafting/ch01/cfg_ch01v4.py`, `drafting/ch02/cfg_ch02v2.py` | Chapter briefs rewritten around historical purpose; evidence hierarchy; canon corrections; Ch2 budget $8.25; section lists and targets for the new structure |
| `drafting/ch01/ch01_outline_v4.md` → `ch01_plan_v5.md`; `drafting/ch02/ch02_outline_v2.md` → `ch02_plan_v3.md` | Chapter arc, section statements, revised Points as historical work, evidence tiers. These absorb the interpretive briefs (kept for the record) |
| `drafting/ch01/evidence_pack_v5.json`, `drafting/ch02/evidence_pack_v4.json` (new) | Packs plus context items |
| `drafting/_runs/rubric.md` / `_master.md` note | Record that contextual items are citable evidence for wider history |
| Canon (Detailed Outline §3–4) | **Only with your approval:** the lineage wording (see §13) |

Not touched: `chroma_db/`, the corpus folders, `books_manifest.yaml`.

---

## 12. Cost

| Item | Projected API | Likely actual (55–65% of projection, as so far) | Paid external access |
|---|---|---|---|
| In-corpus context retrieval (Ch1 up to ~20 new items, Ch2 ~6) | $0.40–0.60 | $0.30–0.45 | none |
| Round 4 (4 sections written, judged and verified; one repair each at most) | $1.20–1.60 | $0.80–1.10 | none |
| Chapter 1 production (sequential sections, author's pass, verification, polish) | $6.8–7.3 | $4.0–4.8 | none |
| Chapter 2 production | $6.5–7.0 | $3.8–4.6 | none |
| **Total remaining for Chapters 1–2** | **$14.9–16.5** | **$8.9–11.0** | **none** |
| Optional: public-domain colonial reports (download free; OCR and a separate collection) | not costed; a separate decision | — | none (free sources) |
| Optional: post-1933 scholarship (Bhatia, Jain, Day) | — | — | library or purchase. **Not purchased** |

**Spent so far in this phase:** Ch1 $0.54, Ch2 $0.44, style $0.33.

**Ceilings** (budget minus the $1 reserve):
- Ch1 $8.50 → $7.50, leaving $6.96 after spend so far;
- Ch2 $8.25 → $7.25, leaving $6.81.

Production projections sit at or just above those ceilings on paper. Removing the stitch saves about $0.3. Exact dry-runs will be reported with round 4.

---

## 13. Decisions that need your approval

1. **Chapter structure for Chapters 1 and 2** as in §6b–6c: new section order and working titles. This replaces "Epistemic discipline" and "Stance". Wildlife goes to Ch12, lichens to Ch7, and the climate trend to a note.
2. **Production architecture:** sequential section drafting with the stitch removed; the author's pass becomes the developmental and voice pass; reader-facing notes consolidated to about one per paragraph or claim cluster.
3. **Evidence policy:** contextual dynastic items become citable evidence for wider history, and Chapter 1's new-item cap rises from about 25 to about 45 for this retrieval. All of it comes from the existing corpus.
4. **Canon correction on lineage:** replace "a nephew of Bhoja, through a junior branch" with "a kinsman of Bhoja whose exact relationship is disputed" (readings go to a note). No primary witness in the corpus calls him a nephew.
5. **Book-level (does not block Chapters 1–2):** split the current Chapter 4 into "Malwa and the Paramāras, to Bhoja" and "Udayāditya and the Founding of Udaypur", and give the later Paramāras (1093–1305) a full section at the opening of the political-change chapter.
6. **Optional, later:** acquire the public-domain colonial reports and Bühler's edition (free, legal) into a separate, new collection.
