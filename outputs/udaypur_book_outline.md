# Udaypur — Book Outline (retrieval-grounded)

*Lead researcher–editor pass, 16 September 2026. Grounded in `kb/store.sqlite` (9,467 chunks, 24 sources) with the heritage profile as secondary orientation. Chunk ids below are `chunks.rowid` and are stable; every query string is runnable as `python kb_query.py "<query>" -k 8`.*

---

## 1. Front matter

**Working titles.** (1) *The Rising Lord: Udayeśvara and the Making of a Paramāra Town* (inherits the manuscript title in `book/`); (2) *A Small Town with a Long Memory: Udaypur, Vidisha*; (3) *Stone, Water, Word*.

**Thesis.** Udaypur is usually presented as one great building — the finest surviving Bhūmija temple and the only royal temple of the Paramāras still standing. This book argues it is one element of a deliberate act of place-making: town, tank and shrine founded together in 1059 by Udayāditya, a *bandhu* of Bhoja from a junior branch of the dynasty, against a sandstone hill already sacred for five centuries. It follows that ensemble through Tughluq, Mughal, colonial and ASI re-use, asking what it means for a place to survive as a monument while ceasing to be a city — and keeps evidence and interpretation apart throughout, because much of what circulates about Udaypur, the heritage profile included, is reconstruction presented as fact.

**Audience.** Serious general readers of Indian history and architecture; students of early medieval Malwa, temple architecture and epigraphy; heritage professionals and local readers in Vidisha.

**Projected length.** 18 chapters + afterword × ~4,500 words ≈ **85,500 words**, plus front/back matter.

### 1.1 How the KB was queried (and what that costs)

The **Chroma store is dead**: `chroma_db/` holds only a 12 KB embed cache, its collection was wiped, and `chromadb` is no longer importable. The environment has also lost `python-dotenv`, `mistralai`, `sentence-transformers`, `rank_bm25` and `langchain-text-splitters`, so **`retrieve.py`, `build_kb.py` and `src/query.py` all hard-fail** on import. The surviving path is `kb/store.sqlite` via `kb_store.py`, which imports none of them.

That store was built **2026-08-09** with `mistral-embed` (1024-dim, 1,800-char chunks, 270 overlap). Its dense side is unusable — no client installed, quota spent — so **all retrieval here was lexical**: FTS5/BM25 over four token streams (raw, folded, Devanagari, entity-expanded), via `KBStore.search_bm25`. Consequences the pipeline must respect:

- **Lexical retrieval rewards proper nouns and technical vocabulary and fails on paraphrase.** Query `kūṭastambha`, `praśasti`, `Udayasamudra` — not "how the tower was built". Where a chapter's subject has no distinctive lexis (C15, C18), recall drops sharply, and the GAP flags below reflect that as much as true absence.
- **Chunks are ~1,800 characters**, cut before the labelling layer existed, so a passage may straddle two; pull `-k 8` and read neighbours (`chunk` ±1 within the same `source`).
- **`Temple_Economics.md` is a false attractor** — a modern polemic that takes the top slot for C17 (3/3), C14, C15 and 3/9 of the Afterword. **Not evidence for medieval or modern Udaypur.**
- **Label filters help but do not solve it.** `content="geography_hydrology"` does return only the Betwa papers, and `"oral_testimony"` only *Jagta Hua Kasba* and *Raja Bhoj*. But **measured**: `"religion_ritual"` still puts Temple_Economics #3448 at rank 1, and `"economy"` returns #3018 — those chunks carry those labels legitimately. **Only explicit source exclusion works**: `kb_query.py --exclude Temple_Economics`. Label vocabulary: architecture, sanskrit_text, religion_ritual, political_history, iconography, historiography, society, measurement, chronology, economy, geography_hydrology, apparatus, inscription, oral_testimony, conservation, translation, epigraphy_meta. Also `evidence_role` (primary_witness, observation, interpretation, restatement, apparatus) and `structural`. Join: `chunk_labels.chunk_id = chunks.rowid`.
- 8,865 of 9,467 chunks are `retrievable=1`; the gate is on by default. An **entity index** exists (146 entities, 376 aliases, 27,296 mentions), including the authority note that Udayapura ≠ Udaipur, Rajasthan.

### 1.2 Coverage map and GAP summary

**Three of the 27 corpus books are not in the KB at all**, and they are not marginal:

| Absent book | What is lost | Chapters hit |
|---|---|---|
| **Geo-Heritage of Udaypur (INTACH vol. 2)** | fort (285 mentions), Shiva Pindi (75), Naṭarāja (16), petroglyph (15), Lajjā Gaurī (10), the whole geology survey | C3, C4, C11, C17, AW |
| **Anupa Pande, *The Udayeśvara Temple*** (full, 65,704 w) | śukanāsa (37), Śaiva Siddhānta (40), garbhagṛha (40), Bhūmija (18) | C8, C9, C12 |
| **Skanda-Purāṇa XIII** (120,410 w) | Purāṇic/scriptural register | C1, C12 |

Pande's **25-chunk summary** (`udayesvara-temple-art-architecture.md`) *is* indexed, so C8/C9/C12 are thin rather than empty — but the summary carries conclusions without the plates, measurements and argument.

| Chapter | KB strength | Carried by (measured) |
|---|---|---|
| C1 | Moderate | Raja_Bhoj ×3, Kramrisch I ×2 — but no Purāṇic source indexed |
| C2 | **Strong** | Betwa_Streamflow ×5, Long-term climate ×2 |
| C3 | **Thin** | no geology source; Geo-Heritage absent |
| C4 | Moderate | Intach ×3, gazetteer ×2 |
| C5 | Good | madhya-bharat-cultural-heritage ×4 |
| C6 | **Strong** | paramara-dynasty ×3, parmar-rajput-origins ×2 |
| C7 | **Strong** | paramara-dynasty ×4, madhya-bharat ×2, serpentine ×1 |
| C8 | Good | Hardy ×2, Some Paramāra ×2, Kramrisch ×2 |
| C9 | Good | Pande-summary ×3, Gupte ×2 |
| C10 | **Strong** | serpentine-scimitar ×3, Intach ×2, JHK ×2 |
| C11 | Good but **concentrated** | Intach 8 of 9 hits |
| C12 | Moderate | bhoja-paramara ×3, Pande-summary ×2 |
| C13 | Good | gazetteer ×4, bhoja-paramara ×3 |
| C14 | Good (after re-query) | gazetteer ×3, JHK ×2 |
| C15 | **Thin** | JHK only; Intach §1.1.2 Folk/Culture |
| C16 | Good | paramara-dynasty ×3 |
| C17 | **Thin — true GAP** | no ASI material; 5/9 hits were Temple_Economics |
| C18 | Moderate | Intach §1.1.1 Demography ×5, JHK |
| AW | **Thin — true GAP** | nothing post-survey; SS "toxic structures" is a vāstu text, not a condition report |

**Chapters needing source acquisition or fieldwork: C3, C15, C17, C18, AW.** The cheapest single intervention is **indexing the three absent books**, which would lift C3, C4, C8, C9, C11, C12, C17 and AW at once. That needs a lexical-only ingest path, since `build_kb.py` currently requires the dead embedding API.

### 1.3 Arc, seams and division of labour

Deep time → landscape → prehistory → Avanti/Malwa → Paramāra apogee → foundation → the monument (structure, sculpture, inscriptions) → later regimes → monumentalisation → the living town. Four seams to handle in prose, not by reordering: **C1 precedes C2–C4**, so write it as an overture posing a question, not chapter one; **C12–C15 interrupt the political chronology** between C7 and C16, so mark them as a deliberate "life of the town" block; **C11 holds post-Paramāra buildings**, grouped by fabric, with C16 supplying the politics; **C15 is atemporal**, so place it last in the block to bridge into C16's rupture.

**Division of labour** (each stated once): *Water* — C7 the founding of Udaysagar, C11 stepwells as fabric, C13 irrigation and revenue. *Naṭarāja* — C9 both images as iconography, C7 the abandoned second temple as an interrupted programme. *Bhūmija* — C6 why the dynasty chose it, C8 how the building works. *Inscriptions* — C10 the texts as texts, C7/C16 the events they record. *Śaiva ritual* — C9 the image programme, C12 the theology. *Conservation* — C17 the history of protection, AW the present condition.

---

## 2. Chapters

### C1 — Udaypur: A Small Town with a Long Memory

**Premise.** A town of six thousand carries a documentary and architectural record wildly out of proportion to its size; the gap between what Udaypur was and what it is now is the question the book sets out to answer.

| Sub-unit | Content | Words |
|---|---|---|
| **1.1 Arrival** | The ordinary town first: Basoda tehsil, 6,383 people, 1,247 households, 15 km from Ganj Basoda. Establishes the deflationary register — the monument is approached through the village, not the other way round. [profile: Part I › Demographics, Access — Documented] · `kb_query.py "kasba Udaypur inhabitants now" -k 8` → #846, #851, #852 Intach §1.1.1 Demography | 550 |
| **1.2 The inventory** | What survives, walked rather than listed: temple, Tughluq mosque, Shahi Mahal and Masjid, Qanungo Baoli, hill fort, ~50 listed sites. Develops the problem that these belong to five different regimes standing within one square kilometre. [profile: Part I › Key monuments] · `"Neelkantheshwar temple Udaypur monuments"` → #890, #993 Intach Appendix 1 | 700 |
| **1.3 Scriptural memory and its limits** | What Sanskrit literature does and does not say about this stretch of the Betwa. The honest finding is negative: **no indexed text names Udayapura before the 11th century**, and the Skanda-Purāṇa is not in the KB. Argues that the town's "long memory" is architectural and epigraphic, not scriptural. [GAP: Skanda-Purāṇa absent from KB] · **V25** — the Prashasti's alleged "expanded, fortified and renamed" wording is unquoted | 800 |
| **1.4 The name** | Udayapura against Udaipur, Rajasthan — a conflation that has corrupted the secondary literature, including the profile's own water-bodies research, which returned the Rajasthan lake. The KB's entity registry encodes the distinction as an authority note. [profile: Part IV › Water bodies — **V16**] · entity `E:PLC:001 Udayapura` | 700 |
| **1.5 What this book claims** | States the thesis and the method: evidence separated from interpretation, confidence tiers carried from the profile, conflicts surfaced rather than resolved. Sets the reader's expectations about provisionality. | 650 |
| **1.6 The shape of the argument** | Walks the arc — landscape, prehistory, dynasty, foundation, monument, decline, monumentalisation, present — so the reader knows why geology precedes kingship. | 600 |

**Key facts to preserve.** 6,383 people / 1,247 households (Census 2011); Basoda tehsil, Vidisha district; ASI-protected Udayeśvara; foundation 1059, flagstaff 1080; Udayapura ≠ Udaipur, Rajasthan.
**Connective tissue.** Opens the book. Hands to C2 by asking what kind of country produced this town.
**Verification.** Does any pre-11th-c. text name the settlement? **V25**. Confirm the census figures against the profile's own table before printing.

---

### C2 — The Betwa Valley: Land, Rivers and Seasons

**Premise.** Udaypur sits in a river basin that does not water it — a town dependent on tanks — and that contradiction shapes everything built here.

| Sub-unit | Content | Words |
|---|---|---|
| **2.1 The Vetravatī** | Rise in Raisen, south-to-north flow, Yamuna confluence at Hamirpur; the river as the district's organising line. `"Betwa Vetravati river basin drainage"` → Betwa_Streamflow ×5 | 700 |
| **2.2 An intermittent river** | The Betwa is intermittent in its upper reaches and perennial only in the lower ~85 km — the technical fact that makes the tank-and-stepwell landscape necessary rather than decorative. `filters={"content":"geography_hydrology"}` → #1647, #1680, #1704 | 800 |
| **2.3 A town without a river** | *Geo-Heritage* states "rivers in this landscape are absent" while also placing Udaypur on the Betwa's east bank; the Kewtan runs 1.8 km off. **Surface the contradiction, do not resolve it.** [GAP: Geo-Heritage not indexed — quote from the file directly] | 700 |
| **2.4 Monsoon and the working year** | Rainfall regime, kharif/rabi cycle, and the long-term climatic series for the basin; how season governs building, farming and festival alike. `"monsoon rainfall Malwa climate season"` → Long-term climate ×2 | 750 |
| **2.5 The plateau** | Vindhyan plateau with north-east spurs, elevation 340–480 m averaging 410 m; the Malwa–Bundelkhand transition that makes this a frontier. `"Malwa plateau Vindhya spur elevation"` → gazetteer | 700 |
| **2.6 Reading a landscape historically** | Weighs how far modern hydrological data (1901–2003 series) can speak to 11th-century conditions — a methodological set-piece the book needs early. [profile: Part III › Setting] | 700 |

**Key facts.** Betwa = Vetravatī; perennial only in lower ~85 km; Kewtan tributary 1.8 km from the hill; 340–480 m elevation.
**Connective tissue.** Opens from C1's "what country is this?" Hands to C3 by turning from water to the rock it runs over.
**Verification.** Resolve the river-adjacency contradiction inside *Geo-Heritage*. Only two hydrology papers are indexed — a third modern source would strengthen the chapter.

---

### C3 — Stones and Forests: Geology, Flora and Fauna

**Premise.** The rock that makes the hill makes the temple; quarry, fort and shrine are one geological story. **KB-thin: the geology survey is not indexed.**

| Sub-unit | Content | Words |
|---|---|---|
| **3.1 Upper Rewa sandstone** | Iron-pigmented, horizontally bedded Vindhyan sandstone — why the temple is red and why it could be cut at all. [GAP: Geo-Heritage §4.9–4.10 not in KB] | 750 |
| **3.2 Mesa, butte and pinnacle** | The hill as a decaying tableland: the mesa (Shiva Pindi, 567.66 m) and the butte ("Small Rock Hill", 582.31 m — *higher* despite the name), and the natural arch INTACH calls the Third Eye. [GAP: Geo-Heritage §4.11, §15.1] · **V21** — the profile's "Cap Hill / Murti Pahad" appears in neither KB nor Geo-Heritage | 800 |
| **3.3 Quarrying** | Bedding-plane reading and wedge-hole splitting; the live quarry beside Bhujariya Talab. The profile's five-step sequence is drawn from general studies, not Udaypur evidence. [profile: Part IV › Quarrying — Reported] · `"quarry stone cutting dressing blocks"` | 700 |
| **3.4 Stone as a building decision** | What sandstone permits and forbids — corbelling, lace-carving, the absence of true arches — linking geology forward to C8. `"sandstone building stone temple material"` → Hardy, madhya-bharat-inscriptions | 750 |
| **3.5 Forest and field** | Van Tulsi, Neem, Bel, Palash; vultures, langur, cave bats; the hill as reserved forest in revenue records. [GAP: Geo-Heritage §5.1–5.3] · `"forest flora fauna trees produce"` → gazetteer | 700 |
| **3.6 A landscape already used** | Argues the hill was a resource and a sanctuary before it was a fort — setting up C4. | 600 |

**Key facts.** Upper Rewa sandstone, Vindhyan; Shiva Pindi 567.66 m; butte 582.31 m; Third Eye arch; reserved-forest status.
**Connective tissue.** Opens from C2's water onto the rock beneath. Hands to C4 by asking who used this hill first.
**Verification.** **V28** — the profile calls the temple both mortarless and kankar-lime-filled and asserts basalt foundations; repeat neither without a conservation report. **Index Geo-Heritage before drafting** or this chapter is written from one un-retrievable file.

---

### C4 — Before Udaypur: Prehistory and Early Historic Vidisha

**Premise.** The hill was sacred and inhabited for centuries before Udayāditya; the Paramāra town intervened in an occupied landscape rather than founding on empty ground.

| Sub-unit | Content | Words |
|---|---|---|
| **4.1 Besnagar and Vidiśā** | The early historic city, the Heliodorus pillar, Śuṅga and Gupta horizons, and the shift across the river to Bhilsa. `"Besnagar Vidisha early historic excavation"` → Intach ×3, gazetteer ×2 | 800 |
| **4.2 The hill before the fort** | Rock-cut Saptamātṛkā and Navagraha panels attributed to the 6th century, a Jain Tīrthaṅkara cave with an undeciphered two-line inscription, a Lajjā Gaurī petroglyph. The chapter's strongest material — and **entirely un-indexed**. [GAP: Geo-Heritage §13–14, Annexure 7] | 850 |
| **4.3 Forest polities** | Bhil, Gond and Sahariya presence; Āṭavika Rājya in Maurya- and Gupta-era texts. The profile's account is generalised and its quoted phrases unverified. [profile: Part III › Indigenous communities — Verify, **V25**] · `"Bhil Gond tribe forest community"` | 700 |
| **4.4 The Udayagiri question** | A proposed artisanal and solar-ideological lineage from the Udayagiri Caves. Present as hypothesis. [profile: Part III — **V26**] · **conflict: the profile's geography is wrong — Udayagiri is near Vidisha town, not adjacent to Udaypur (V21)** | 700 |
| **4.5 Sanchi's shadow** | What a major Buddhist landscape 40 km away implies about routes, patronage and craft supply in the centuries before the Paramāras. `"Sanchi stupa Sunga patronage"` | 700 |
| **4.6 The state of the evidence** | Weighs comparative dating against excavation: the 6th-century attribution is INTACH's comparison with Pathari and Udayagiri, **not** a stratigraphic date. | 650 |

**Key facts.** Besnagar; Heliodorus pillar; Bhilsa named for Bhaillasvāmin; 6th-c. attribution of the hill panels; Jain cave inscription undeciphered.
**Connective tissue.** Opens from C3's "already-used landscape". Hands to C5 by widening from site to region.
**Verification.** **[GAP: ASI excavation/exploration reports for Basoda tehsil — absent from KB and profile alike.]** **V25**, **V26**, **V21**.

---

### C5 — From Avanti to Malwa: Dynasties, Trade Routes and Sacred Cities

**Premise.** Malwa's identity was assembled over a millennium, and Udaypur's frontier position — facing Chedi, astride a north–south route — explains why a king built *here*.

| Sub-unit | Content | Words |
|---|---|---|
| **5.1 Avanti to Mālava** | Ujjayinī, Dhārā and Vidiśā as successive poles; how a region acquires a name. `"Avanti Malwa Ujjayini Dhara capital"` → madhya-bharat-cultural-heritage ×4 | 750 |
| **5.2 The succession of powers** | Mauryas, Śuṅgas, Sātavāhanas, Guptas, Aulikaras, Gurjara-Pratihāras; Bhillasvāmin sun-worship at Bhilsa. [profile: Part III › Setting and eras — Reported] | 750 |
| **5.3 Routes** | Feeder lines linking Besnagar and Mathurā to the Deccan. The profile's "caravan staging post" is interpretive but consistent with the KB's quarry economy. `"trade route Deccan caravan merchant"` | 700 |
| **5.4 Sacred geography** | Ujjain as a tīrtha and a capital at once; how sanctity and administration reinforced each other in Malwa. `"tirtha sacred city pilgrimage Malwa"` | 700 |
| **5.5 The eastern frontier** | Facing the Kalachuris of Tripurī and the Chaulukyas of Gujarat — the strategic logic C7 makes concrete. [profile: Part IV › Strategic economy] | 700 |
| **5.6 Why frontiers get built on** | Argues the frontier is the *reason* for Udaypur's scale, against the assumption that grand temples mark capitals. | 700 |

**Key facts.** Avanti ≈ Mālava; Ujjayinī, Dhārā, Vidiśā; Bhillasvāmin; Kalachuri and Chaulukya neighbours.
**Connective tissue.** Opens from C4's regional prehistory. Hands to C6 by arriving at the dynasty that took the region.
**Verification.** The staging-post characterisation is the chapter's load-bearing claim and has no cited evidence in the KB.

---

### C6 — The Paramāras and Bhoja: Kingship, Learning and Temple Building

**Premise.** Bhoja made Malwa a centre of learning and left a treatise on architecture; the dynasty's adoption of the Bhūmija mode was deliberate self-distinction, and Udayāditya inherited both.

| Sub-unit | Content | Words |
|---|---|---|
| **6.1 Origins and the agnikula** | Vasiṣṭha's fire-pit on Mount Abu and the name "slayer of the enemy"; origin myth as dynastic argument. `"Paramara dynasty agnikula origin Mount Abu"` → parmar-rajput-origins ×2 | 700 |
| **6.2 To independence** | Upendra through Sīyaka II — the defeat of Khoṭṭiga and the sack of Mānyakheṭa, c. 972. `"Siyaka Khottiga Manyakheta Rashtrakuta"` → paramara-dynasty | 700 |
| **6.3 Muñja and Sindhurāja** | The poet-warrior's campaigns and death against Tailapa II; the succession to Bhoja. `"Munja Sindhuraja succession Tailapa"` | 650 |
| **6.4 Bhoja the scholar-king** | Patronage, the Bhojaśālā, and the *Samarāṅgaṇasūtradhāra* — with 1,220 indexed chunks the KB's single largest source. `"Bhoja scholar king Dhara patronage learning"` → paramara-dynasty ×3 | 850 |
| **6.5 Why Bhūmija** | Hardy: the Paramāras chose the mode "to distinguish themselves from rival dynasties patronising mainly Shekhari temples". The chapter's interpretive core. `"Bhumija Paramara favoured mode Shekhari"` → Hardy | 800 |
| **6.6 The crisis of 1055** | Bhoja's death amid a joint Chaulukya–Kalachuri attack; Jayasiṃha I's reign and death c. 1070; Malwa briefly lost. `"Jayasimha successor Bhoja Malwa recovery"` | 750 |

**Key facts.** Sīyaka II defeats Khoṭṭiga, sacks Mānyakheṭa c. 972; Muñja killed by Tailapa II; Bhoja son of Sindhurāja; *Samarāṅgaṇasūtradhāra*; Bhoja d. c. 1055; Jayasiṃha I c. 1055–1070.
**Connective tissue.** Opens from C5's regional frame. Hands to C7 at the dynasty's lowest point, from which Udayāditya rises.
**Verification.** **V4** — whether Jayasiṃha I stands in the Prashasti king list or only in other records. Bhoja's accession is given as 999, 1000, 1005 and 1010 across KB sources; pick one and footnote the range.

---

### C7 — Udayāditya's Foundation: Town, Temple and Tank

**Premise.** Town, temple and tank were founded as one endowment in 1059, more than a decade before Udayāditya became king — making Udaypur the base from which he recovered the dynasty, not a monument raised after the fact.

| Sub-unit | Content | Words |
|---|---|---|
| **7.1 Who Udayāditya was** | A *bandhu* — kinsman — of Bhoja, placed by careful readings in a junior branch. **Three incompatible relationships across sources**: Ganguly's "scion of a junior branch"; Intach's citation of Jain inscriptions calling Bhoja his *brother*; *Bhoja Paramara and His Times* calling him a nephew. [profile: Part IV — **V1**] · `"Udayaditya bandhu relation Bhoja"` → #809 Intach, paramara-dynasty ×4 | 850 |
| **7.2 The triple foundation** | Udayapura, Udayeśvara and Udayasamudra named together; construction begun VS 1116 (1059), flagstaff VS 1137 (1080). `"Udayaditya founded town temple tank"` → madhya-bharat-cultural-heritage (explicit: "founded a town, built a temple of Shiva, and excavated a tank") | 800 |
| **7.3 Founding before kingship** | Ganguly resolves the 1059-versus-accession problem by having Udayāditya build while ruling his paternal territory from Udayapura — the most useful interpretive move available, and the chapter's spine. `"Udayaditya paternal territory ruling 1059"` | 750 |
| **7.4 The tank** | Udaysagar as the third term of the endowment, 71 acres, beside the older Bhujariya Talab. **This repairs profile V16**, whose search returned the Rajasthan lake. [GAP: Geo-Heritage §9.1–9.2 for the measurements] | 700 |
| **7.5 The interrupted programme** | The colossal unfinished Naṭarāja and the pillar bases beside it, read as a second temple abandoned at Udayāditya's death — evidence that the foundation was a *programme*, not a building. [GAP: Geo-Heritage §8.1] · `"unfinished colossal Siva sculpture Udaypur"` → Intach | 700 |
| **7.6 A frontier capital** | Nine inscriptions of Udayāditya across Ujjain, Udaypur, Dhar, Un and Kamed; Udaypur as a sub-capital rather than a provincial shrine. `"nine inscriptions Udayaditya Ujjain Dhar Un"` → #832 Intach | 700 |

**Key facts.** 1059 (VS 1116) begun, 1080 (VS 1137) flagstaff; Udayapura / Udayeśvara / Udayasamudra; reign c. 1070–1093; Udaysagar 71 acres; Bhujariya Talab older.
**Connective tissue.** Opens from C6's crisis. Hands to C8 by entering the building itself.
**Verification.** **V2** reign dates (c. 1060 vs c. 1070; KB gives 1058–1087 and 1070–1093). **V3** whether Lakṣmadeva ruled between Udayāditya and Naravarman. **V25**. The Bhrangarajpur conquest legend is oral tradition, not record.

---

### C8 — Udayeśvara in Stone: Plan, Structure and Style

**Premise.** The temple has no surviving precedent yet arrives fully formed as the most elaborate Bhūmija ever built — which means the mode was developed elsewhere, in buildings now lost.

| Sub-unit | Content | Words |
|---|---|---|
| **8.1 Approach and ensemble** | East-facing red sandstone: *garbhagṛha*, *antarāla*, *gūḍhamaṇḍapa* with three *mukhamaṇḍapas*, a separate lattice-walled *vedī* on axis, on a lofty *jagatī*. **Conflict: Pande counts eight subsidiary shrines, Beglar's 1871–72 report seven.** `"garbhagriha mandapa plan stellate temple"` → Hardy ×2, Kramrisch ×2 | 800 |
| **8.2 The śikhara** | Four *latā*s in *gavākṣa* lacework; seven *bhūmi*s of five *kūṭastambha*s per sub-quarter; the serrated *skandha*; the figure climbing the north-west face, read as a flag-bearer. `"Bhumija sikhara lata kutastambha"` → #7077, #7226, #530 | 850 |
| **8.3 Hardy's verdict** | "Already the deluxe model": a 32-point star equivalent to seven orthogonal projections, seven *bhūmi*s; Nemawar's later attempt at nine failed. The argument that Udayeśvara is a terminus, not a beginning. `"deluxe model 32-point star seven bhumis"` → Hardy | 750 |
| **8.4 Geometry and the texts** | Rotation of the square (*parivartanā*) within a circle, and what the *Samarāṅgaṇasūtradhāra* actually prescribes for *prāsāda*s — the KB's largest source, 1,220 chunks. `"Samarangana Sutradhara prasada proportion"` · [profile: Part IV › Plan geometry — **V22**: the formulas were missing; the rotated-square method is a general reconstruction] | 800 |
| **8.5 Structure and material** | Corbelling, load paths, the *śukanāsa* over the vestibule — described, not asserted as engineering. [profile: Part IV › Structural components — **V28**] | 700 |
| **8.6 Comparison** | Against Un, Nemawar, Bijamandal and Bhojpur — the two dozen surviving Paramāra temples and the three "imperial" ones. `"Un Nemawar Bhojpur Paramara temple"` → Some Paramāra Temples ×2 | 700 |

**Key facts.** Founded 1059, consecrated 1080; red sandstone; 32-point star, seven *bhūmi*s; eight (or seven) subsidiary shrines; *sapta-ratha* sanctum.
**Connective tissue.** Opens from C7's foundation act. Hands to C9 by moving from structure to the figures on it.
**Verification.** **V17** — the profile's acoustic and thermal claims come from studies of *other* temples, and its "12–15 m platform above the water surface" belongs to a different building; "stays cool in summer" is visitor report. Measured plans needed. **Index Pande's full monograph** — the 25-chunk summary carries conclusions without evidence.

---

### C9 — Gods on the Walls: Sculpture, Iconography and Meaning

**Premise.** The image programme is a systematic Śaiva argument distributed across the building — and Naṭarāja appears twice at Udaypur, once atop the spire-front and once colossal and unfinished at the foot of the hill.

| Sub-unit | Content | Words |
|---|---|---|
| **9.1 The śukanāsa** | Naṭeśa Śiva dancing the *tāṇḍava* in *ūrdhvajānu karaṇa*, flanked by dancing goddesses including a rare dancing Sarasvatī, over a niche holding the syncretic Hariharārkapitāmaha. `"Nataraja tandava dancing Siva sculpture"` → Pande-summary ×3 | 800 |
| **9.2 The directional programme** | Dikpālas on the cardinal and intermediate faces; Mahābhairava, Sūrya, Umā-Maheśvara; Cāmuṇḍā concentrated in the northern quarter — a Paramāra habit also seen at Arthuna and Panaheda. `"dikpala iconography niche directional"` → Gupte ×2 | 800 |
| **9.3 The Mātṛkās and the fierce forms** | Saptamātṛkā, Cāmuṇḍā, Vīrabhadra strangling Dakṣa, Bhṛṅgī — reading a mythic narrative across wall surfaces. `"Saptamatrika Camunda Bhairava image"` | 750 |
| **9.4 The hill Naṭarāja** | A monolith on its back, trampling Apasmāra, unfinished. **Dimensions conflict**: Geo-Heritage 8.2 × 4.2 m; Intach ~9 × 3 × 1.5 m with six arms; elsewhere "more than 2 metres high". [profile: Part I — **V23**, "world's largest" sourced to a social-media post] | 750 |
| **9.5 Dress, ornament and daily life** | Sculpture as a sound primary source for costume where textual claims are not: *mekhalā*, *stanapaṭṭa*, *dhammilla*. [profile: Part IV › Women › Dress — **V13**: Bilhaṇa is Chalukya, not Paramāra, court poetry] | 700 |
| **9.6 Erotic and apotropaic sculpture** | Mithuna panels on the hall pillars, *kīrtimukha*, *vyāla*, *makara* — weighing decorative, protective and doctrinal readings against each other. `"mithuna erotic kirtimukha vyala"` | 700 |

**Key facts.** Naṭeśa in *ūrdhvajānu*; dancing Sarasvatī (rare); Hariharārkapitāmaha; Cāmuṇḍā with scorpion; monolith on Apasmāra.
**Connective tissue.** Opens from C8's fabric. Hands to C10 by turning from carved figures to carved words.
**Verification.** Do not repeat "world's largest Naṭarāja" (**V23**); obtain the ASI description and settle the dimensions by measurement. Iconographic identifications rest largely on Pande's summary — **index the full book**.

---

### C10 — Words in Stone: Inscriptions, Languages and the Serpentine Scimitar of Letters

**Premise.** Udaypur is an epigraphic archive running in Sanskrit, Arabic, Persian and Hindi across eight centuries — and one of its inscriptions is a grammar chart shaped like a sword.

| Sub-unit | Content | Words |
|---|---|---|
| **10.1 The Udaipur Prashasti** | The Paramāra genealogy in Nagari, the agnikula origin, the "rising sun" verse on Udayāditya. **Use the published translation**; the profile's long "new dawn" passage is a paraphrase presented as a quotation (**V5**). The KB carries Ganguly's actual rendering of the Nagpur verse — "his relation, Udayâditya, became king… he acted like the holy Boar". `"prasasti Nagari genealogy Paramara"` | 850 |
| **10.2 The foundation record and the porch archive** | The 22-line VS 1116 inscription; Devapāla's grants of 1229 and 1232 naming the treasurer Dhamadeyava; the 1323–24 elephant votive of Mādhava and Keśava; the VS 1394 (8 Jan 1338) *jātrā* of Harirāja; pilgrim records of 1377 and 1446. [profile: Part II, Part IV — Documented] · `"copper plate grant Devapala treasurer"` | 800 |
| **10.3 The serpentine scimitar** | The *varṇanāgakṛpāṇikā*: the alphabet coiled in a serpent's body, called a *siddhāsiputrikā*, with companions at Ujjain, Dhar and Un. `"serpentine scimitar grammar chart letters"` → #8930 and 2 more (the paper is only 14 chunks — read all of them) | 850 |
| **10.4 Reading a praśasti critically** | What panegyric can and cannot be made to yield: genealogy versus event, formula versus fact. Develops the book's central evidentiary discipline on its hardest case. `filters={"content":"inscription"}` → #7295, #7341, #7425 | 750 |
| **10.5 Four languages on one site** | Sanskrit, Arabic, Persian and Hindi; the 1645 Qanungo Baoli slab dated simultaneously in VS 1701, Śaka 1566 and Hijri 1054. [profile: Part V › 1645 trilingual inscription — Documented] | 700 |
| **10.6 The epigraphic corpus as a whole** | Nine inscriptions of Udayāditya; over ninety pilgrim records in ARIE 1961–62 (C 1611–1690) — against the profile's "more than sixty". **Conflict to state.** | 600 |

**Key facts.** VS 1116 = 1059; VS 1137 = 1080; 1229 and 1232 Devapāla grants; Dhamadeyava; VS 1394 = 8 Jan 1338; 1377, 1446 pilgrim records; 13 Jan 1645 trilingual baoli; builders Gokuladāsa and Dāmodaradāsa, Māthur Kāyasthas.
**Connective tissue.** Opens from C9's images. Hands to C11 by stepping outside the temple wall.
**Verification.** **V4**, **V5**, **V6** all land here. The profile calls the Prashasti 24 lines and in the Gujari Mahal Museum (both flagged unconfirmed) while the KB's 22-line count refers to the foundation inscription — **resolve whether these are one stone or two**. **[GAP: *Epigraphia Indica* vol. I; Trivedi, *CII* VII(2); ARIE 1961–62 — no edited inscription text is in the KB.]**

---

### C11 — Built Heritage: Fortifications, Mosques, Shrines and Stepwells

**Premise.** The temple is one building in a town of many, and the hill fort above it is older than the dynasty that made the town famous. **Concentration risk: 8 of 9 retrieved hits come from Intach alone.**

| Sub-unit | Content | Words |
|---|---|---|
| **11.1 The hill fort** | A 1,400 m dry-stone wall on three sides with the southern cliff as the fourth, enclosing 56 acres; one gate, 5.2 × 5.6 m; three-storey bastions, iron-clamped, with arrow slits. **Wall thickness conflicts**: Cunningham 18 ft, Intach 8–10 ft, Geo-Heritage ~4 m — cite none unresolved. [GAP: Geo-Heritage §9.6, §10.6–10.13] · `"fort fortification bastion wall gateway"` → Intach ×8 | 850 |
| **11.2 The town's gates and palace** | The fortified Mahal with its Teen Darwaza; Chanderi, Moti and Purana Bazaar gateways; chhatris and memorial structures. `"gateway darwaza palace mahal Udaypur"` → #890, #929, #932 | 750 |
| **11.3 Islamic architecture** | The Tughluq mosque west of the temple (AH 737, 739); the Shahi Mahal and Masjid east of it, 1616–1632, with two Persian inscriptions of June 1632. [profile: Part V — Documented] · `"mosque masjid Tughluq Persian inscription"` → #824 Intach | 800 |
| **11.4 Water architecture** | The Qanungo Baoli of 1645; Ghod Dod Baoli; the local reckoning of fifty-six stepwells, fifty-two wells and twelve and a half tanks. `"stepwell baoli vapi water structure"` → #938 Intach | 750 |
| **11.5 Jain and minor shrines** | The Jain Mandir, the hill cave Tīrthaṅkara, Hanuman and Gaṇeśa shrines — the religious plurality of a single small town. `"Jain mandir shrine temple Udaypur"` → #915 Intach | 650 |
| **11.6 Dating the undated** | Weighs oral tradition ("predates Udayāditya"), Intach's unexplained "early 10th century CE", and masonry typology against one another. | 700 |

**Key facts.** 1,400 m wall, 56 acres; single gate 5.2 × 5.6 m; Tughluq mosque AH 737/739; Shahi Mahal 1616–1632; Qanungo Baoli 1645; Teen Darwaza.
**Connective tissue.** Opens from C10's inscriptions on other buildings. Hands to C12 by asking what was believed inside them.
**Verification.** **V10** — Moti Darwaza and the Sher Khan Mosque stepwell are **Mandu** features the profile placed at Udaypur; do not carry them over. **V11** — the profile conflates the 14th-c. Tughluq mosque (west) with the 17th-c. Shahi Masjid (east). **V9** — Mughal channels and domed well covers unsourced. Seek a second source: this chapter currently rests on one book.

---

### C12 — Ritual and Knowledge: Śaiva Traditions and Intellectual Worlds

**Premise.** The temple was built inside a specific theology — Śaiva Siddhānta — and its iconographic programme can be read as a statement of that system.

| Sub-unit | Content | Words |
|---|---|---|
| **12.1 Śaiva Siddhānta at Udaypur** | Pande's central argument: the *śukanāsa* maps the *śuddha adhvā*, with Śiva, Śakti, Sadāśiva, Īśvara and Sadvidyā identifiable in its parts. `"Saiva Siddhanta tantra agama philosophy"` → Pande-summary ×2 · [GAP: Pande Parts II–III not indexed] | 850 |
| **12.2 Sects and lineages** | Pāśupata, Lākulīśa, Kāpālika and Siddhānta streams in Malwa; the Lakulīśa panel on the hill. `"matha ascetic Pasupata Lakulisa sect"` | 750 |
| **12.3 Bhoja's theology** | The *Tattvaprakāśa* — a king writing Śaiva metaphysics, and the link between the dynasty's learning and its building. `"Tattvaprakasa Bhoja Saiva"` | 700 |
| **12.4 Ritual practice** | *Pratiṣṭhā* and *dhvajārohaṇa*; daily and calendrical worship; Śilpaśāstra consecration prescriptions. `filters={"content":"religion_ritual"}` + `"pratistha consecration dhvaja"` | 750 |
| **12.5 The temple as a school** | The grammar charts are real; a Bhojaśālā-style institution at Udaypur is interpretive. [profile: Part IV › Education — Verify] | 700 |
| **12.6 Plural devotion** | Śaiva, Vaiṣṇava and Jain patronage side by side — the Garuḍāsana Viṣṇu in the later archway, the Jain cave, the Harihara image. | 650 |

**Key facts.** Śaiva Siddhānta; *śuddha adhvā*; *Tattvaprakāśa* of Bhoja; Lakulīśa panel; *dhvajārohaṇa* 1080.
**Connective tissue.** Opens from C11's plural fabric. Hands to C13 by moving from belief to subsistence.
**Verification.** **V18** — dispensaries, maternity wards and specific surgeries at Udaypur are unsourced, and the *Rājamārtāṇḍa* formulation counts come from a single journal article. Medicine belongs here only so far as Bhoja's attributed texts are attested; the rest is regional Ayurvedic history.

---

### C13 — Fields, Wells and Markets: Agriculture, Economy and Crafts

**Premise.** A temple town of this scale required a surplus; quarries, black soil, tanks and grain grants explain how it was made and where it went.

| Sub-unit | Content | Words |
|---|---|---|
| **13.1 Soil and crops** | Black cotton soil for cotton and oilseeds; wheat and barley in rabi, millets and pulses in kharif. `"agriculture crops land revenue grant"` → gazetteer ×4 (#8964, #9138, #9001) | 750 |
| **13.2 Water for fields** | Stepwells and wells in grants; rope-and-bucket lifts; sluice release from tanks. `"irrigation well tank field cultivation"` → #9001, #9002 gazetteer | 700 |
| **13.3 The quarry economy** | Sandstone quarries as the town's strategic asset on the Kalachuri frontier — the clearest economic argument the KB supports. `"sandstone quarry frontier economy"` → JHK | 750 |
| **13.4 Grants and revenue** | *Bhāga* and *bhoga*; *devadaya* land; Devapāla's 1229 grant and the treasurer Dhamadeyava. [profile: Part IV › Villages named — Verify, **V20**: Mahuāḍa, Mathurāpūra and Vāghāḍa lack a quoted reading] | 750 |
| **13.5 Crafts and guilds** | *Śilpin*s, *sūtradhāra*s, *takṣaka*s; weavers' guilds; madder and indigo dyeing. `"market merchant guild sreni craft"` → #5605 bhoja-paramara, #7887 SS | 700 |
| **13.6 The temple as an economic institution** | Endowment, kitchen, garland contracts, pilgrim traffic — how a shrine moved resources. **Do not source this from `Temple_Economics.md`**, a modern polemic. `filters={"content":"economy"}` | 700 |

**Key facts.** Black cotton soil; *bhāga* (often one-sixth) and *bhoga*; *devadaya*; Devapāla 1229 (VS 1286); Dhamadeyava.
**Connective tissue.** Opens from C12's institutions. Hands to C14 by turning from the economy to the people in it.
**Verification.** **V14** the *Kṛṣi-Parāśara* dating and library link; **V15** the Nagpur inscription's goods list and one-rupaka levy, quoted without a checked text; **V24** tools and rotation schedules reflect general agrarian history. **[GAP: the Paramāra land-grant corpus.]**

---

### C14 — People of the Plateau: Communities, Languages and Everyday Life

**Premise.** The people living at Udaypur now are not incidental to its history; the *mohallā* structure is the settlement pattern still in use.

| Sub-unit | Content | Words |
|---|---|---|
| **14.1 The town's quarters** | Shikari, Mahua, Chaudaryana, Sarenthi and Utranti *mohallā*s; the older settlement on the hill near Hajariya Mahadev. `"mohalla settlement quarter Udaypur"` → Intach §1.1–1.2 | 750 |
| **14.2 Communities** | Castes and communities of the district; Brahman, Rajput, and the artisan groups named in the gazetteer. `"Brahman Rajput caste occupation"` → #1095, #1097 JHK, #5289 bhoja-paramara | 750 |
| **14.3 Demography** | Population, households and literacy (54.28%); what a 2011 census says and cannot say about an eleventh-century town. `"population census village inhabitants"` → #9270, #9274, #8993 gazetteer | 700 |
| **14.4 Languages** | Hindi with Bundeli and Malvi; Sanskrit as the language of record against the vernacular of speech. `"language dialect spoken local"` → #8994 gazetteer, #6738–9 madhya-bharat | 700 |
| **14.5 Offices of the Paramāra town** | *Pattakila*, *Mahājana*s, *śreṣṭhi*s, *mālākāra*s, *devadāsī*s — standard early-medieval titles whose specific functions at Udaypur are **not** tied to named inscriptions. [profile: Part IV › Administration — Verify] | 750 |
| **14.6 Women** | Claims on queens as governors, *devadāsī* property and later seclusion are generalised; sculpture is the reliable source. [profile: Parts IV–V — **V19**] | 700 |

**Key facts.** Five named *mohallā*s; 54.28% literacy; Bundeli and Malvi; Hajariya Mahadev.
**Connective tissue.** Opens from C13's economy. Hands to C15 by moving from who people are to what they tell.
**Verification.** **V19** requires the Udaypur votive records themselves (ARIE 1961–62, C 1611–1690). The medieval and modern halves rest on different evidence — a 1979 gazetteer and a 2022 survey for the present, generic office-titles for the past — and neither may borrow authority from the other. **Discard `Temple_Economics` hits**, which dominate naive queries here.

---

### C15 — Stories of Udaypur: Festivals, Folklore and Oral Histories

**Premise.** What the town remembers differs from what the inscriptions record, and the difference is itself evidence. **KB-thin: essentially one source.**

| Sub-unit | Content | Words |
|---|---|---|
| **15.1 The living temple** | Morning and evening *āratī*; the *Ghariyālon kā Makān*, whose family struck the temple gong to keep ritual time; Śivarātri and the Mondays of Śrāvaṇa. [GAP: Pande's "Reports" section not indexed] · `"Sivaratri fair pilgrims temple festival"` → #848 Intach §1.1.2 Folk, Culture | 750 |
| **15.2 Founding legends** | Bhrangarajpur and the defeated chief; how a conquest becomes a origin story. `filters={"content":"oral_testimony"}` → #1311, #1314 JHK | 750 |
| **15.3 The dancer of Udaysagar** | The rope-walker promised half a kingdom and the king who had the rope cut — a tale that encodes a real anxiety about royal promises. `"legend tale king dancer story"` → #1225, #1226 JHK | 700 |
| **15.4 A town that talks about itself** | *Jagta Hua Kasba* as first-person reportage; the anchor text, in Hindi original and English translation, and the problems of using a partisan local source. `"oral history residents recollection"` → #1337 JHK | 800 |
| **15.5 Shared sites and shared stories** | The dargah on the middle hill; Jind Baba; Beglar's note that the temple was frequented by Hindus and Muslims alike, and the Aurangzeb legend he recorded — which Cunningham corrected. | 750 |
| **15.6 Memory against the record** | Sets folk chronology beside epigraphic chronology and asks what each is for. | 700 |

**Key facts.** *Ghariyālon kā Makān*; Śivarātri; Śrāvaṇa Mondays; Bhrangarajpur; the Udaysagar dancer; Jind Baba.
**Connective tissue.** Opens from C14's communities. Hands to C16 by moving from stories of continuity to the rupture that ended the Paramāra town.
**Verification.** Every legend needs attribution to a named teller or printed source. **[GAP: recorded oral-history interviews — none exist in KB or profile.]** Naive queries here return `Temple_Economics` and Kramrisch's "THE DOLMEN"; use the `oral_testimony` filter.

---

### C16 — Conquests and Regimes: Decline of the Socio-Economic Hub of Madhya Bharat

**Premise.** Udaypur outlasted the dynasty that made it; its demotion from royal town to *qasba* to village is the real subject of the book's second half.

| Sub-unit | Content | Words |
|---|---|---|
| **16.1 The later Paramāras** | Naravarman, Yaśovarman, Jayavarman, Vindhyavarman, Arjunavarman, Devapāla; wars with the Hoysalas, Yādavas and Chaulukyas. `"decline fall Paramara kingdom"` → #7447 paramara-dynasty "Fall of the Paramaras of Malwa", #2172 Some Paramāra | 850 |
| **16.2 The end of the dynasty** | Annexation by the Chaulukyas and then the Sultanate; the last Paramāra inscription at Udaypur in 1310; Delhi's control by 1338. `"Muslim invasion Malwa annexation"` | 750 |
| **16.3 Tughluq Udaypur** | The mosque of AH 737/739 under Muhammad bin Tughluq; reuse of carved material from subsidiary shrines; the temple **not** razed — local tradition says an order to demolish it was given in 1325 and not carried out. [profile: Part V — Documented, **V27**] · `"Tughluq conquest Malwa Sultanate invasion"` → #8958 | 800 |
| **16.4 Continuity under new rule** | The VS 1394 procession record of 1338 shows community religious life continuing alongside the new administration — the single most useful piece of evidence in the chapter. [profile: Part V › Changes in civic roles — **V27**] | 700 |
| **16.5 Sultanate and Mughal town** | A *qasba* in sarkar Chanderi of the Malwa subah; the Shahi Mahal and Masjid 1616–1632; the Qanungo Baoli of 1645 and its Māthur Kāyastha builders. `"Mughal qasba Chanderi subah"` → #6903, #1099, #824 | 750 |
| **16.6 Why the centre moved** | Weighs conquest, route-shift and the rise of Bhilsa/Chanderi as explanations for the town's contraction — refusing a single-cause story. | 700 |

**Key facts.** Paramāra inscription 1310; Delhi Sultanate by 1338; AH 737/739 mosque; VS 1394 procession; *qasba* in sarkar Chanderi; Shahi Mahal 1616–1632; baoli 1645.
**Connective tissue.** Opens from C15's living memory. Hands to C17 by arriving at the moment the town becomes an object of study.
**Verification.** **V27** — the Muqti/amil roles, the hadith quotation and the spolia attribution are not quoted from the inscriptions; published readings of the 1336–39 texts are needed. The profile's "important urban centre from the 14th to the 16th centuries" is asserted without evidence.

---

### C17 — Archaeologists, Laws and Repairs: Making Udaypur a "Monument"

**Premise.** Protection saved the temple and detached it from the town; the paperwork of preservation is also a history of separation. **True GAP: the KB holds no ASI documentation.**

| Sub-unit | Content | Words |
|---|---|---|
| **17.1 The antiquarians** | Cunningham's tours and Beglar's 1871–72 report — including Beglar's error attributing the mosque to Aurangzeb and Cunningham's correction: a case study in how site histories get fixed in print. [GAP: Pande's "Reports" chapter not indexed] · `"Cunningham Beglar report tour"` → weak; returns Kramrisch bibliography | 800 |
| **17.2 Scindia-era repair** | The brass *mukha* cover given to the liṅga by Khanderao Appaji, general of Mahadji Scindia, in 1775; the western gate attributed to the same period — repair as patronage, before "conservation" existed. [GAP: Pande ch. I] | 700 |
| **17.3 Becoming protected** | What ASI protection covers and what it leaves out — notably the hill fort, which is Forest Department land, and the unprotected rock sculptures, Jain cave and petroglyph on it. **[GAP: ASI notification, protected-area boundary.]** | 800 |
| **17.4 Documentation as an act** | INTACH Bhopal's two volumes: the listing of ~50 sites, then the drone and total-station survey of the fortification — "the first time that such extensive documentation… has been carried out". `filters={"content":"conservation"}` → #772, #782 Intach | 750 |
| **17.5 Udaypur in independent India** | Panchayat, Forest Department, State archaeology and ASI as overlapping jurisdictions; who is actually responsible for what. **[GAP: no post-1947 administrative source in KB.]** | 750 |
| **17.6 The costs of monumentalisation** | Argues that protection froze the temple and orphaned everything around it — the book's central irony, and the bridge to C18. | 700 |

**Key facts.** Beglar 1871–72; Cunningham's correction; brass *mukhaliṅga* cover 1775, Khanderao Appaji; INTACH listing ~50 sites; hill under Forest Department.
**Connective tissue.** Opens from C16's regime change. Hands to C18 by arriving in the present.
**Verification.** **[GAP: ASI notification, protected-area boundary, and post-1947 conservation or repair reports — absent from KB and profile alike.]** This chapter cannot be drafted from current sources; naive retrieval returns `Temple_Economics` 5 times in 9.

---

### C18 — Present Tense: How the Town Lives with Its Past Today

**Premise.** Several thousand people live beside a royal temple in a town that has been a village for six centuries; the closing question is what that costs them.

| Sub-unit | Content | Words |
|---|---|---|
| **18.1 A kasba on the margin** | The opening claim of *Jagta Hua Kasba*: a town of eight thousand with a thousand years of stories and nobody listening. **Conflict with the 2011 census figure of 6,383.** `"kasba Udaypur inhabitants now"` → #846 Intach, JHK | 750 |
| **18.2 Living in the fabric** | Dry-stone houses with courtyards; ancient gateways narrowed into lanes by encroaching houses; carved fragments lying in the streets. `"village today people live condition"` → #851, #852 Intach §1.1.1, #1155 JHK | 750 |
| **18.3 Services and livelihoods** | Roads, schools, water, electricity; agriculture and quarrying as employment; the young leaving. `"development road school electricity"` → #9244 gazetteer | 700 |
| **18.4 Custodians and officials** | The author of *Jagta Hua Kasba* writing to the Collector of Vidisha in 2019, and his charge that the archaeology department filled "the belly of papers with the budget" — one resident's testimony, attributed as such. `filters={"content":"oral_testimony"}` | 750 |
| **18.5 A working shrine** | Not a ruin: daily worship, Śivaratri crowds, a priesthood with continuing functions. (Cross-ref C15; here the emphasis is civic, not devotional.) | 700 |
| **18.6 Two Udaypurs** | The monument's visitors and the village's residents occupy the same ground and rarely meet — states the problem the Afterword answers. | 700 |

**Key facts.** 6,383 (2011) vs "eight thousand" (*Jagta Hua Kasba*); 1,247 households; 2019 letter to the Collector; Teen Darwaza lanes.
**Connective tissue.** Opens from C17's monumentalisation. Hands to the Afterword by naming the problem.
**Verification.** **[GAP: fieldwork — interviews with residents, the ASI custodian, the panchayat and the temple priests; current population and livelihood data.]** This chapter cannot be written responsibly from two indexed books.

---

### Afterword — Conservation today, the village's struggles, and how it can be improved

**Premise.** The hill fort is collapsing while the temple is protected, and the case for acting is strongest where the evidence is newest. **True GAP: nothing in the KB postdates the INTACH survey.**

| Sub-unit | Content | Words |
|---|---|---|
| **AW.1 Documented deterioration** | INTACH's own findings: collapsed bastions, slope erosion, a fortification wall whose decay "has now entered a critical phase". Weighs what a single survey can establish about rate of loss. [GAP: Geo-Heritage §10.14–10.17 not indexed] | 800 |
| **AW.2 The protection gap** | A protected temple beside an unprotected hill under a different department, carrying unprotected rock sculptures, a Jain cave and a petroglyph. The jurisdictional split is the mechanism of neglect, not an accident of it. `filters={"content":"conservation"}` → #772, #782 Intach | 800 |
| **AW.3 Proposals on the table** | INTACH's geo-tourism recommendations — interpretation boards, a defined pathway, the historic gate as entry. Report as INTACH's proposals, not the book's, and test each against the site's carrying capacity. [GAP: Geo-Heritage §15.3, §16] | 750 |
| **AW.4 What residents ask for** | The Kashi Vishwanath-corridor comparison proposed in *Jagta Hua Kasba*, and what is realistic at this scale. Sets local aspiration against conservation orthodoxy, which distrusts corridor-style clearance. | 750 |
| **AW.5 What conservation is for** | Fabric-first repair versus use-first continuity: the temple is a living shrine, so freezing it is itself an intervention. Positions the book against pure monument-preservation. | 700 |
| **AW.6 The argument** | What is owed to a place that was a capital and is now a village — the book's closing position, stated as advocacy and labelled as such. | 700 |

**Key facts.** Bastion collapse; wall decay "critical phase"; Forest Department tenure; INTACH geo-tourism proposals; 2019 Collector letter.
**Connective tissue.** Opens from C18's "two Udaypurs". Closes the book.
**Verification.** **[GAP: current ASI condition reports; status of any INTACH proposal; MP state archaeology and Forest Department positions.]** Naive retrieval here returns the *Samarāṅgaṇasūtradhāra*'s "toxic structures" chapter — an 11th-century vāstu text on inauspicious buildings, **not** a condition report. Do not let it into the draft.

---

## 3. Pipeline handoff

**Per chapter, the drafting step should receive:** the chapter block above in full — premise, the 5–6 sub-units with their word budgets, key facts, connective tissue, and the verification line — plus the front-matter thesis and the division-of-labour list (so it does not re-cover a neighbour's material).

**It must re-run retrieval rather than trust this outline's citations**, which are top-3 samples taken at outline time. For each sub-unit:

```bash
python kb_query.py "<the sub-unit's query string>" -k 12 --full
python kb_query.py "<query>" -k 12 --source "<book>"      # to isolate one source
```

Programmatic form, with the label filters that fix the false-attractor problem:

```python
import kb_store
st = kb_store.KBStore()
hits = st.search_bm25("Bhumija sikhara lata kutastambha", k=12,
                      filters={"content": "architecture"})
# each hit: rowid (=chunk id), source, chunk, trail, heading, page_start, text, score
```

**Rules the drafter must carry:**
1. **Exclude `Temple_Economics.md`** unless the subject is literally modern temple economics — use `--exclude Temple_Economics`, since label filters do *not* remove it (it holds genuine `religion_ritual` and `economy` labels). It is a false attractor for C14, C15, C17 and AW.
2. **Read neighbouring chunks.** Chunking predates the labelling layer; a passage often straddles `chunk` n and n+1 of the same `source`.
3. **Three books are absent** — Geo-Heritage, Pande's full monograph, Skanda-Purāṇa. Where a sub-unit is marked `[GAP: … not indexed]`, the drafter must read the file directly from `Udaypur Reference Markdown Files/` rather than report the topic as unsourced.
4. **Carry V-flags into the prose** as hedges, never silently as fact; never promote a "Verify before use" claim.
5. **Surface conflicts** (Udayāditya's relationship to Bhoja; Naṭarāja dimensions; subsidiary-shrine count; wall thickness; census vs "eight thousand") rather than choosing quietly.

**Before drafting C3, C8, C9, C12, C17 or AW, index the three missing books.** `build_kb.py` is currently unrunnable (`python-dotenv`, `mistralai` uninstalled) and its dense path needs a spent API; a lexical-only ingest that appends to `chunks` + `chunks_fts` would lift eight chapters at once and is the highest-value next action on this project.
