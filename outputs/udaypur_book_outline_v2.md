# Udaypur — Book Outline (v2, updated)

*Lead researcher–editor, 17 September 2026. Chapter titles and order follow `chapters.md` exactly.*

**KB note (post-repair).** The dense side is dead — no embedding client, spent quota — so all retrieval is lexical BM25 over `kb/store.sqlite` via `python kb_query.py "<query>" -k 8 --exclude Temple_Economics`. **Repaired this session:** the three books that were never indexed are now indexed. An append-only ingest (`kb_append_lexical.py`) added **1,287 chunks** — Geo-Heritage 226, Pande's full monograph 401, Skanda-Purāṇa 660 — taking the store from 9,467 to **10,754 chunks across 27 sources**, the full corpus. All four token streams (raw, folded, Devanagari, entity) are populated and verified functionally; integrity `ok`; the original 9,467 rowids are untouched, preserving the rowid↔embedding-row invariant. Every chapter can now be sourced from the index; nothing needs reading around it.

---

## Thesis

Udaypur is usually presented as one great building. This book argues it is a single deliberate act of place-making: a town, a tank and a Śiva temple founded together in 1059 by Udayāditya — a nephew of Bhoja from a junior branch of the Paramāra house — on Malwa's eastern frontier, eleven years before he became king. That ensemble is the most complete statement the dynasty left in stone, and the book follows it from the sandstone it was cut from to the village living around it now, through Khaljī conquest, Tughluq and Mughal re-use, colonial antiquarianism and ASI protection.

## The frame: Malwa among its neighbours, c. 900–1305

The Paramāras began as Rāṣṭrakūṭa feudatories and ended as a name on a Khaljī casualty list. Between those points they held the plateau every other power wanted, because Malwa is the hinge between the Gangetic north and the Deccan, and between the Gujarat ports and the eastern forests. Neighbours pressed from every side: **Chaulukyas** of Gujarat west, holding the sea outlets; **Kalachuris** of Tripurī east, across the frontier Udaypur guards; **Chandelas** north-east; **Chāhamānas** of Śākambharī north-west — whose king Durlabha III sent the cavalry that let Udayāditya retake Malwa; **Western Cālukyas** of Kalyāṇa south, who killed both Muñja and Jayasiṃha I; later **Hoysalas** and **Yādavas** from the Deccan. Independence was won in 972 by sacking the Rāṣṭrakūṭa capital itself.

This is why a temple of this quality stands in a village of six thousand. Udaypur was a frontier seat facing Chedi, sited where sandstone, water and a defensible hill met a north–south road — and Ganguly's reading of the inscriptions puts Udayāditya's recovered kingdom as reaching Jhalrapatan in the north, Bhilsa in the east and Nimar in the south, "almost the whole of the territory over which his predecessor Bhoja ruled". The civilizational claim is specific: an eleventh-century regional dynasty on a contested plateau brought the Bhūmija mode to its most developed form, then lost the state that made it, leaving the building to outlive its makers by seven centuries.

---

## CANON 1 — SOURCE-ROLE MATRIX  *(for sign-off)*

Every claim routes to the source **type** competent for it. If a sub-unit's claim-type and its source-type disagree, the assignment is wrong.

| Type | Sources | Authoritative FOR | Must NOT be used for |
|---|---|---|---|
| **SURVEY** | **Geo-Heritage (INTACH vol. 2)** — drone + total-station survey, geomorphology, condition assessment | All measurements, dimensions, geology, site condition, fort fabric | Chronology; art-historical judgement; **its own superlatives** ("largest in the world") — never adopt |
| **MONOGRAPH** | **Pande, *The Udayeśvara Temple*** (architecture, sculpture, Śaiva Siddhānta, Śilpaśāstra translations); Hardy; Kramrisch; Gupte | Architecture, iconography, style, form-dating, the image programme. **Pande is primary on the temple** — plan, shrine count, iconography | Political chronology; site measurements (defer to SURVEY) |
| **DYNASTIC** | **Ganguly, *History of the Paramara Dynasty*** (standard); *Bhoja Paramara and His Times*; madhya-bharat-cultural-heritage | Chronology, genealogy, political events, reign spans | Architectural analysis; present-day conditions |
| **EPIGRAPHY** | Udayapur & Nagpur praśastis; Panhera, Jhalrapatan, Mandhata records; serpentine-scimitar paper (2023) | Dates, names, grants, titles — the check on DYNASTIC | Neutral fact: **a praśasti is panegyric**, read critically |
| **TESTIMONY** | **Jagta Hua Kasba (VMT)** — first-person heritage-walk reportage, self-described "a published work of opinion", c. 2021–22 | Folklore, oral tradition, present-day village life, named resident testimony — **always attributed** | **Never** a medieval fact or a physical measurement |
| **GAZETTEER** | Vidisha District Gazetteer | Administrative, demographic, agrarian, community baseline | Medieval events — **date-stamp it: a 1979 compilation** |
| **SCRIPTURE** | Skanda-Purāṇa (now indexed) | Mythic/scriptural register, labelled as such | Event-history |
| **EXCLUDED** | **Temple Economics (Sandeep Singh)** — *Arthvyavastha of Mandir* Vol. I, a contemporary policy tract opening on a "Ram Mandir Rate of Growth → Param Vaibhav" chart. **It never treats Udaypur** | Nothing | Everything. Known false attractor — `--exclude Temple_Economics`; label filters do not remove it |

## CANON 2 — CHAPTER → SOURCE-TYPE BINDING  *(for sign-off)*

| Chapters | Carried by | Checked against |
|---|---|---|
| C2, C3, C11 (fort fabric) | **SURVEY** | GAZETTEER (C2 climate), MONOGRAPH (C3 stone as design constraint) |
| C8, C9, C12 | **MONOGRAPH (Pande primary)** | SURVEY for measurements only |
| C5, C6, C7, C16 | **DYNASTIC** | **EPIGRAPHY** |
| C10 | **EPIGRAPHY** | DYNASTIC for context |
| C1 | SCRIPTURE + EPIGRAPHY | — (the finding is largely negative) |
| C4 | SURVEY (hill panels) + GAZETTEER | DYNASTIC |
| C13, C14 | GAZETTEER (date-stamped) + EPIGRAPHY (grants) | — |
| C15, C18 | **TESTIMONY**, attributed | GAZETTEER for demographic baseline |
| C17, Afterword | SURVEY + MONOGRAPH (antiquarian reports) | — |

## CANON 3 — CHRONOLOGY SPINE  *(for sign-off; identical dates in every chapter)*

| Date | Event | Authority |
|---|---|---|
| early 9th c. | Upendra, first Paramāra king, a subordinate chief of Rāṣṭrakūṭa Govinda III | DYNASTIC |
| **972** | Sīyaka II defeats Khoṭṭiga at Kalighatta and sacks Mānyakheṭa → independence | DYNASTIC |
| 973–995 | Vākpati-Muñja; captured and killed by Cālukya Tailapa II | DYNASTIC |
| 995–1000 | Sindhurāja | DYNASTIC |
| **1000–1055** | **Bhoja** | Ganguly on Merutuṅga (reign 55 y 7 m 3 d) |
| 1055–1070 | Jayasiṃha I; killed c. 1070 by Someśvara II and Karṇa | DYNASTIC |
| **1059** | **Udayāditya founds Udayapura, Udayeśvara, Udayasamudra** — as a territorial lord, *not* king (VS 1116) | EPIGRAPHY + Ganguly |
| **1070–1093** | **Udayāditya, king of Malwa** (see Canon 4) | DYNASTIC + EPIGRAPHY + Pande |
| **1080** | Flagstaff raised on the Udayeśvara (VS 1137) | EPIGRAPHY |
| 1086 | Jhalrapatan inscription (Sam. 1143), "in the victorious reign of Udayaditya" | EPIGRAPHY |
| 1094–1134 | Naravarman | EPIGRAPHY |
| 1218–1239 | Devapāla; grants 1229, 1232 | EPIGRAPHY |
| 1293 | Alāʾ al-Dīn Khaljī raids **Bhilsa** (a raid, not the conquest) | GAZETTEER |
| **1305** | **Khaljī conquest of Malwa** (AH 705); Mahlak Deo defeated → **the Paramāra state ends** | DYNASTIC |
| 1310 | A Paramāra inscription still at Udaypur → **residual local authority after the state's fall** | EPIGRAPHY |
| 1336–39 | Tughluq mosque inscriptions (AH 737, 739) | EPIGRAPHY |
| 1616–1632 | Shahi Mahal and Masjid | EPIGRAPHY |
| 13 Jan 1645 | Qanungo Baoli trilingual inscription | EPIGRAPHY |

**1305 vs 1310, reconciled once.** 1305 ends the Paramāra *state*; 1310 is a local record surviving in the north-east. Sequential, not contradictory. No chapter re-opens this.

## CANON 4 — UDAYĀDITYA, THE PROTAGONIST  *(for sign-off)*

**Lineage — committed: a nephew of Bhoja, through a junior branch of the Paramāra house.** Cited to *Bhoja Paramara and His Times* (Mahesh Singh), ch. on Economic Condition, in the passage on Belur wall-paintings: "some wall-paintings of the time of **Bhoja's nephew, Udayaditya** (1059-80)". The junior-branch half is Ganguly, *History of the Paramara Dynasty*, ch. IV: "Udayaditya, **a scion of a junior branch** of the Paramaras, stood gallantly for the liberation of his ancestral dominion." The two reconcile: the Udayapur praśasti gives him his own paternal line (Sauravīra → Jñātā → Udayāditya), so his father belonged to a collateral line and "nephew" is the generational relation to Bhoja, not descent from Bhoja's own father. **The narrative states this as fact; one endnote records the debate and still lands here.**

*Editorial caution for your ruling:* the explicit word "nephew" occurs once in the corpus for Udayāditya — an aside in a paragraph about painting style, not a genealogical argument — while the same book calls Bhoja "the nephew of king Munja", which may be the origin of the usage. Ganguly's junior-branch reading is argued from the praśasti pedigree and is the stronger evidential base. The committed formulation above carries both; override if you want the emphasis reversed.

**Reign — committed: c. 1070–1093.** The start is fixed by Ganguly's own reasoning: Karṇa of Gujarat acceded in **1063**, so Udayāditya "cannot be taken to have ruled in 1059 A.D. as a sovereign lord, because Karṇa had not yet assumed the kingly power" — he built the temple in 1059 "when he was ruling his paternal territory apparently from Udayapur", and the **Panhera inscription** shows Jayasiṃha still ruling Malwa that year. Pande independently states he "ascended the throne in 1070 CE". The end is fixed by Ganguly: Naravarman "began his reign some time before 1094 A.D.", while the Jhalrapatan record of Sam. 1143 = **1086** has Udayāditya still reigning. Variants (c. 1058–1087; the 1059–80 span in the Belur aside) go in **one endnote**.

**Life.** Born into a collateral line holding territory in eastern Malwa. Founded town, temple and tank as one endowment in **1059** while still a territorial lord under a collapsing kingdom. Took the throne **c. 1070** after Jayasiṃha I fell; appealed to the Cāhamāna Durlabha III of Śākambharī, whose cavalry let him break the Caulukya–Karṇāṭa occupation; the Nagpur praśasti likens him to the boar lifting a drowning earth. Recovered a kingdom reaching Jhalrapatan, Bhilsa and Nimar. Raised the flagstaff in **1080**; still reigning **1086**; the only Paramāra to strike gold coins; nine inscriptions survive across Ujjain, Udaypur, Dhar, Un and Kamed. Died **c. 1093**, cause unrecorded. Succeeded briefly by Lakṣmadeva, then **Naravarman (1094–1134)**.

**Authorial stance.** We write him as a builder-restorer, not a conqueror-hero and not a footnote to Bhoja. His most revealing act came *before* he had power: on a threatened frontier, with the dynasty broken, he laid out a town, a reservoir and a temple as one design — a man planning permanence while the centre burned. Where the sources are panegyric we read them as such; but the book knows who he was and does not hedge.

## CANON 5 — DISCREPANCY POLICY  *(for sign-off)*

1. **Measurements and counts of one object** — commit to the single most authoritative source (SURVEY for dimensions; Pande for the temple). **One figure in the text**, at most one endnote. *Several figures for one wall is a defect, not honesty.*
2. **Protagonist biography and lineage** — Canon 4. Settled.
3. **Dynastic chronology** — Canon 3. Identical everywhere.
4. **Context-resolvable contradictions** — reconcile by explanation. *Worked example:* the 2011 Census counts **6,383**; VMT (c. 2021–22) estimates **~8,000** ("of the eight thousand, 1,000–1,500 are Muslims"). The framing is **a decade of growth**, and a rounded authorial estimate against a decadal count — not a contradiction.
5. **Genuinely open interpretive questions only** — e.g. whether Bhoja joined an anti-Ghaznavid confederacy: state a working position, note the debate in a line. **Never applies to the protagonist's biography or to any measurement.**

**Committed measurements.** Naṭarāja **8.2 × 4.2 m** (Geo-Heritage #9536, corroborated by INTACH catalogue #33) · subsidiary shrines **eight** (Pande #9709: "surrounded by eight subsidiary shrines, quite a few now broken") · fort wall **1,400 m**, dry-stone sandstone with an earthen rampart stone-faced inside and **no binding material**, enclosing **56 acres** (Geo-Heritage #9491, #9589) · mesa **567.66 m**, butte **582.31 m** — the butte is the *higher* despite being the smaller (#9637) · temple **32-point star, seven bhūmis**, red sandstone (Hardy; Pande #9714).

**Signature objects — from the object, never the trope.** The hill Naṭarāja is **not** the familiar many-armed dancer in a ring of flame: **six arms** (triśūla, ḍamaru, two unidentified attributes, two hands in mudrā), over Apasmāra, **reclining on its back**, **unfinished with chisel marks visible**, carrying an undeciphered inscription, beside the pillar-bases of an abandoned structure. INTACH's catalogue titles it *Chaturbhuji* (four-armed) while its description says six — **we follow the description**. Same rule for every signature object: arm count, attributes, posture, scale and peculiarities from the plates; one set of dimensions from SURVEY.

---

# Chapters

### C1 Udaypur: A Small Town with a Long Memory (Ancient Scriptural References)
**Premise.** A village of six thousand carries a record out of all proportion to its size, and that gap is the book's question.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 1.1 Arrival | The ordinary town first; the monument approached through the village | GAZETTEER · `"Udaypur village panchayat Basoda demography"` | 900 |
| 1.2 The inventory | Five regimes standing within one square kilometre | SURVEY · `"listed heritage sites Udaypur grade"` | 900 |
| 1.3 What "long memory" means | The honest negative: the Purāṇic register is regional, not local — no text names Udayapura before the 11th c. | SCRIPTURE · `"Skanda Purana mahatmya tirtha glorification"` | 900 |
| 1.4 The name | Udayapura ≠ Udaipur, Rajasthan — a conflation that has corrupted the secondary literature | EPIGRAPHY · `"Udayapura ancient name ninth century"` | 750 |
| 1.5 Method and stance | Evidence separated from interpretation; what this book commits to and why | — | 800 |

**Committed:** 6,383 (Census 2011); foundation 1059; flagstaff 1080.
**Bridges:** opens the book → C2 asks what country produced this town.
**GAP:** no pre-11th-c. textual attestation exists — state the absence, don't fill it.

### C2 The Betwa Valley: Land, Rivers and Seasons (Geography)
**Premise.** Udaypur sits in a river basin that does not water it, and that contradiction shapes everything built here.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 2.1 The Vetravatī | Rise in Raisen, south-to-north flow, Yamuna confluence | GAZETTEER · `"Betwa Vetravati river basin drainage"` | 850 |
| 2.2 An intermittent river | Perennial only in the lower ~85 km — why tanks were necessary, not decorative | SURVEY · `filters={"content":"geography_hydrology"}` | 950 |
| 2.3 Monsoon and the working year | The kharif/rabi cycle governing building, farming and festival alike | GAZETTEER · `"monsoon rainfall Malwa climate season"` | 850 |
| 2.4 The plateau | Vindhyan plateau, 340–480 m; the Malwa–Bundelkhand transition that makes this a frontier | SURVEY · `"Malwa plateau Vindhya spur elevation"` | 800 |
| 2.5 Reading a landscape historically | How far a 1901–2003 climate series can speak to the eleventh century | SURVEY · `"long-term climatic change Betwa basin"` | 750 |

**Committed:** elevation 340–480 m, mean 410 m; Kewtan 1.8 km from the hill.
**Bridges:** from C1's question → C3 turns from water to rock.
**GAP:** none — Geo-Heritage §4 is now indexed.

### C3 Stones and Forests: Geology, Flora and Fauna (Geology and Landscape Report)
**Premise.** The rock that makes the hill makes the temple; quarry, fort and shrine are one geological story.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 3.1 Upper Rewa sandstone | Iron-pigmented, horizontally bedded — why the temple is red and why it could be cut | SURVEY · `"mesa butte caprock sandstone Rewa formation"` | 900 |
| 3.2 Mesa, butte, arch | A decaying tableland: the mesa and the higher butte, and the natural arch INTACH names the Third Eye | SURVEY · `"Shiva Pindi butte elevation perimeter"` | 900 |
| 3.3 Quarrying | Bedding-plane reading and wedge-hole splitting; the live quarry by Bhujariya Talab | SURVEY · `"quarry stone cutting dressing blocks"` | 850 |
| 3.4 What sandstone permits | Corbelling, lace-carving, no true arches — geology as design constraint | MONOGRAPH · `"sandstone building material temple"` | 850 |
| 3.5 Forest and fauna | Van Tulsi, Neem, Bel, Palash; vultures, langur, cave bats; reserved-forest status | SURVEY · `"flora fauna trees species forest produce"` | 750 |

**Committed:** mesa 567.66 m; butte 582.31 m; Upper Rewa sandstone, Vindhyan.
**Bridges:** from C2's water → C4 asks who used this hill first.
**GAP:** none — the geology survey is now indexed (226 chunks).

### C4 Before Udaypur: Prehistory and Early Historic Vidisha*
**Premise.** The hill was sacred and inhabited for centuries before Udayāditya; the Paramāra town intervened in an occupied landscape.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 4.1 Besnagar and Vidiśā | The early historic city, the Heliodorus pillar, Śuṅga and Gupta horizons, the shift to Bhilsa | GAZETTEER + DYNASTIC · `"Besnagar Vidisha early historic excavation"` | 900 |
| 4.2 The hill before the fort | 6th-c. Saptamātṛkā and Navagraha panels, a Jain Tīrthaṅkara cave, a Lajjā Gaurī petroglyph | SURVEY · `"Saptamatrika Navagraha panel Jain cave petroglyph"` | 950 |
| 4.3 Forest polities | Bhil, Gond and Sahariya presence; Āṭavika Rājya in early texts | GAZETTEER · `"Bhil Gond tribe forest community"` | 800 |
| 4.4 Sanchi's shadow | What a major Buddhist landscape 40 km off implies about routes, patronage and craft supply | DYNASTIC · `"Sanchi stupa Sunga patronage"` | 800 |
| 4.5 What comparative dating can bear | The 6th-c. attribution is comparison with Pathari and Udayagiri, **not** stratigraphy | SURVEY · — | 700 |

**Committed:** hill panels attributed 6th c. (comparative, not excavated); the fort predates Udayāditya (Geo-Heritage #9491).
**Bridges:** from C3's used landscape → C5 widens from site to region.
**GAP:** no excavation report for Basoda tehsil exists in any source. The profile places Udayagiri beside Udaypur — it is near Vidisha town; do not repeat.

### C5 From Avanti to Malwa: Dynasties, Trade Routes and Sacred Cities (Evolution over the Years)
**Premise.** Malwa's identity was assembled over a millennium, and Udaypur's frontier position explains why a king built *here*.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 5.1 Avanti to Mālava | Ujjayinī, Dhārā and Vidiśā as successive poles | DYNASTIC · `"Avanti Malwa Ujjayini Dhara capital"` | 850 |
| 5.2 The succession of powers | Mauryas to Gurjara-Pratihāras; Bhillasvāmin sun-worship at Bhilsa | DYNASTIC · `"Pratihara Rashtrakuta overlordship feudatory"` | 850 |
| 5.3 Routes | Feeder lines from Besnagar and Mathurā to the Deccan; Gujarat ports west | DYNASTIC · `"trade route Deccan caravan merchant"` | 800 |
| 5.4 Sacred geography | Ujjain as tīrtha and capital at once; sanctity and administration reinforcing each other | SCRIPTURE + DYNASTIC · `"tirtha sacred city pilgrimage Malwa"` | 800 |
| 5.5 The eastern frontier | Facing Kalachuri Tripurī and Chaulukya Gujarat — the logic C7 makes concrete | DYNASTIC · `"Kalachuri Chedi frontier Malwa border"` | 800 |

**Committed:** independence 972; Upendra a feudatory of Govinda III.
**Bridges:** from C4's prehistory → C6 arrives at the dynasty that took the region.
**GAP:** the "caravan staging post" characterisation is inference, not cited evidence — present as such.

### C6 The Paramāras and Bhoja: Kingship, Learning and Temple Building (How Udaypur was formed)
**Premise.** Bhoja made Malwa a centre of learning and left a treatise on architecture; the Bhūmija mode was deliberate self-distinction, and Udayāditya inherited both.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 6.1 Origins and independence | The agnikula myth as dynastic argument; Sīyaka II sacks Mānyakheṭa | DYNASTIC · `"Siyaka Khottiga Manyakheta independence"` | 850 |
| 6.2 Muñja and Sindhurāja | The poet-warrior's campaigns and death against Tailapa II | DYNASTIC · `"Munja Sindhuraja succession Tailapa"` | 750 |
| 6.3 Bhoja the scholar-king | Patronage, the Bhojaśālā, the *Samarāṅgaṇasūtradhāra* — the corpus's largest single source | DYNASTIC + MONOGRAPH · `"Bhoja scholar king Dhara patronage learning"` | 950 |
| 6.4 Why Bhūmija | Hardy: the mode chosen "to distinguish themselves from rival dynasties patronising mainly Shekhari temples" | MONOGRAPH · `"Bhumija Paramara favoured mode Shekhari"` | 900 |
| 6.5 The crisis of 1055 | Bhoja's death amid a joint Chaulukya–Kalachuri attack; Jayasiṃha I falls c. 1070 | DYNASTIC · `"Jayasimha successor Bhoja Malwa recovery"` | 850 |

**Committed:** Bhoja 1000–1055; Muñja 973–995; Sindhurāja 995–1000; Jayasiṃha I 1055–1070.
**Bridges:** from C5's region → C7 opens at the dynasty's lowest point.
**GAP:** the anti-Ghaznavid confederacy is genuinely open — state a working position in one line (Canon 5.5).

### C7 Udayāditya’s Foundation: Town, Temple and Tank
**Premise.** Town, temple and tank were founded as one endowment in 1059, eleven years before their founder became king.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 7.1 The man | The nephew from a junior branch: pedigree, position, the territory he already held (Canon 4 applied) | DYNASTIC + EPIGRAPHY · `"scion junior branch Paramara Udayaditya Sauravira"` | 900 |
| 7.2 The triple foundation | Udayapura, Udayeśvara, Udayasamudra named together; begun VS 1116 | EPIGRAPHY · `"Udayaditya founded town temple tank"` | 900 |
| 7.3 Founding before kingship | Building while ruling his paternal territory; the Panhera inscription has Jayasiṃha still ruling in 1059 | DYNASTIC · `"Panhera Jayasimha ruling 1059 paternal territory"` | 850 |
| 7.4 Recovering the kingdom | Durlabha III's cavalry; the Caulukya–Karṇāṭa occupation broken; a realm reaching Jhalrapatan, Bhilsa, Nimar | DYNASTIC · `"Durlabha Sakambhari cavalry Caulukya Karnata regained"` | 850 |
| 7.5 The interrupted programme | The abandoned second temple: pillar-bases and the unfinished colossus (described per Canon 5) | SURVEY · `"Natraj sculpture apasmara monolith incomplete pillars"` | 800 |

**Committed:** 1059 foundation; **1070 accession; d. c. 1093**; 1080 flagstaff; 1086 still reigning; Udaysagar 71 acres.
**Bridges:** from C6's crisis → C8 enters the building.
**GAP:** the Bhrangarajpur conquest legend is TESTIMONY only — attributed, never as event.

### C8 Udayeśvara in Stone: Plan, Structure and Style (Neelkantheshwar Temple Architecture)
**Premise.** The temple has no surviving precedent yet arrives fully formed as the most elaborate Bhūmija ever built — so the mode matured elsewhere, in buildings now lost.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 8.1 The ensemble | East-facing red sandstone: sanctum, vestibule, hall with three porches, separate *vedī*, lofty *jagatī* | MONOGRAPH · `"garbhagrha antarala gudhamandapa vedi jagati plan"` (#9709) | 900 |
| 8.2 The śikhara | Four *latā*s in *gavākṣa* lacework; seven *bhūmi*s of five *kūṭastambha*s per sub-quarter; the climbing flag-bearer | MONOGRAPH · `"Bhumija lata kutastambha bhumis sikhara"` (#9714) | 950 |
| 8.3 Hardy's verdict | "Already the deluxe model": a 32-point star; Nemawar's later attempt at nine bhūmis failed | MONOGRAPH · `"deluxe model 32-point star seven bhumis"` | 850 |
| 8.4 Geometry and the texts | Rotation of the square within a circle; what the *Samarāṅgaṇasūtradhāra* prescribes | MONOGRAPH · `"Samarangana Sutradhara prasada proportion"` | 850 |
| 8.5 Comparison | Un, Nemawar, Bijamandal, Bhojpur — the survivals and the three imperial monuments | MONOGRAPH · `"Un Nemawar Bhojpur Paramara temple"` | 800 |

**Committed:** **eight** subsidiary shrines; 32-point star; seven bhūmis; 1059–1080.
**Bridges:** from C7's foundation → C9 moves from structure to the figures on it.
**GAP:** none — Pande's monograph is now indexed (401 chunks).

### C9 Gods on the Walls: Sculpture, Iconography and Meaning (Deities and Symbolism)
**Premise.** The image programme is a systematic Śaiva argument across the building — and Naṭarāja appears twice at Udaypur, once on the spire-front and once colossal at the hill's foot.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 9.1 The śukanāsa | Naṭeśa in *ūrdhvajānu karaṇa*, flanked by dancing goddesses including a rare dancing Sarasvatī | MONOGRAPH · `"Natesa tandava urdhvajanu sukanasa medallion"` (#9718) | 900 |
| 9.2 The directional programme | Dikpālas, Mahābhairava, Sūrya, Umā-Maheśvara; Cāmuṇḍā in the northern quarter | MONOGRAPH · `"dikpala iconography niche directional"` | 900 |
| 9.3 The fierce forms | Saptamātṛkā, Vīrabhadra and Dakṣa, Bhṛṅgī — a mythic narrative across wall surfaces | MONOGRAPH · `"Saptamatrika Camunda Bhairava image"` | 800 |
| 9.4 **The hill Naṭarāja** | From the object: six arms, attributes, reclining, unfinished, over Apasmāra, inscribed | SURVEY + MONOGRAPH · `"Natraj 8.2 meters apasmara six hands trident damru"` (#9536) | 900 |
| 9.5 Dress and ornament | Sculpture as primary evidence for costume where texts are not | MONOGRAPH · `"mekhala ornament drapery sculpture"` | 750 |

**Committed:** Naṭarāja **8.2 × 4.2 m, six arms**, 11th c., state-protected. Never "world's largest".
**Bridges:** from C8's fabric → C10 turns from carved figures to carved words.
**GAP:** none.

### C10 Words in Stone: Inscriptions, Languages and the Serpentine Scimitar of Letters
**Premise.** Udaypur is an epigraphic archive in four languages across eight centuries — and one of its inscriptions is a grammar chart shaped like a sword.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 10.1 The Udaipur Prashasti | Genealogy, agnikula, the "rising sun" verse — read as panegyric, in the published translation | EPIGRAPHY · `"prasasti Nagari genealogy Paramara"` | 900 |
| 10.2 The porch archive | VS 1116; Devapāla's 1229/1232 grants and Dhamadeyava; the 1323–24 votive; the VS 1394 *jātrā*; pilgrims 1377, 1446 | EPIGRAPHY · `"copper plate grant Devapala treasurer"` | 900 |
| 10.3 The serpentine scimitar | The *varṇanāgakṛpāṇikā*, a *siddhāsiputrikā* of "kings Udayāditya and Naravarman", with kin at Ujjain, Dhar, Un | EPIGRAPHY · `"serpentine scimitar grammar chart letters"` | 900 |
| 10.4 Reading panegyric critically | What a praśasti yields and withholds: genealogy vs event, formula vs fact | EPIGRAPHY · `filters={"content":"inscription"}` | 850 |
| 10.5 Four languages, one site | Sanskrit, Arabic, Persian, Hindi; the 1645 slab dated in three eras at once | EPIGRAPHY · `"trilingual stepwell inscription 1645"` | 750 |

**Committed:** VS 1116 = 1059; VS 1137 = 1080; grants 1229, 1232; VS 1394 = 1338; baoli 13 Jan 1645.
**Bridges:** from C9's images → C11 steps outside the temple wall.
**GAP:** no edited inscription text in the corpus — EI vol. I, Trivedi's *CII* VII(2) and ARIE 1961–62 must be obtained for the readings.

### C11 Built Heritage: Fortifications, Mosques, Shrines and Stepwells (Other Structures besides the temple)
**Premise.** The temple is one building in a town of many, and the hill fort above it is older than the dynasty that made the town famous.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 11.1 The hill fort | Wall, bastions, single gate, enclosed area — one set of figures, from the survey | SURVEY · `"fortification wall bastion dry stone rampart"` (#9491, #9589) | 950 |
| 11.2 Gates and palace | The fortified Mahal and its Teen Darwaza; Chanderi, Moti and Purana Bazaar gateways; chhatris | SURVEY · `"gateway darwaza palace mahal Udaypur"` | 800 |
| 11.3 Islamic architecture | The Tughluq mosque west of the temple; the Shahi Mahal and Masjid east, 1616–1632 | EPIGRAPHY + SURVEY · `"mosque masjid Tughluq Persian inscription"` | 850 |
| 11.4 Water architecture | The Qanungo Baoli; Ghod Dod Baoli; fifty-six stepwells, fifty-two wells, twelve and a half tanks | SURVEY + TESTIMONY · `"stepwell baoli vapi water structure"` | 800 |
| 11.5 Dating the undated | Oral tradition, INTACH's "early 10th century", masonry typology — weighed, then a position taken | SURVEY · — | 750 |

**Committed:** wall **1,400 m**, dry-stone with earthen rampart, **no binding material**; **56 acres**; fort **predates Udayāditya**; Tughluq mosque AH 737/739; Shahi Mahal 1616–1632.
**Bridges:** from C10's inscriptions on other buildings → C12 asks what was believed inside them.
**GAP:** do not import Mandu's Moti Darwaza or Sher Khan stepwell — they are not Udaypur.

### C12 Ritual and Knowledge: Śaiva Traditions and Intellectual Worlds (Culture and Way of Life)
**Premise.** The temple was built inside a specific theology, and its image programme states that theology.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 12.1 Śaiva Siddhānta at Udaypur | Pande's argument that the *śukanāsa* maps the *śuddha adhvā* | MONOGRAPH · `"Saiva Siddhanta suddha adhva Sadasiva Isvara"` (#9857) | 950 |
| 12.2 Sects and lineages | Pāśupata, Lākulīśa, Kāpālika and Siddhānta streams; the Lakulīśa panel on the hill | MONOGRAPH · `"matha ascetic Pasupata Lakulisa sect"` | 850 |
| 12.3 Bhoja's theology | The *Tattvaprakāśa* — a king writing Śaiva metaphysics, joining learning to building | MONOGRAPH · `"Tattvaprakasa Bhoja Saiva"` | 800 |
| 12.4 Ritual practice | *Pratiṣṭhā* and *dhvajārohaṇa*; the Śilpaśāstra prescriptions for consecration | MONOGRAPH · `filters={"content":"religion_ritual"}` | 800 |
| 12.5 Plural devotion | Śaiva, Vaiṣṇava and Jain patronage side by side; the Harihara image; the hill's Jain cave | MONOGRAPH · `"Jain Vaishnava Harihara plural patronage"` | 750 |

**Committed:** consecration 1080; Śaiva Siddhānta affiliation.
**Bridges:** from C11's plural fabric → C13 turns from belief to subsistence.
**GAP:** none — Pande Parts II–III are now indexed. Medicine enters only so far as Bhoja's attributed texts are attested.

### C13 Fields, Wells and Markets: Agriculture, Economy and Crafts
**Premise.** A temple town of this scale required a surplus; quarries, black soil, tanks and grain grants explain how it was made.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 13.1 Soil and crops | Black cotton soil; wheat and barley in rabi, millets and pulses in kharif | GAZETTEER · `"agriculture crops land revenue grant"` | 850 |
| 13.2 Water for fields | Stepwells and wells in grants; lifts; sluice release from tanks | GAZETTEER + SURVEY · `"irrigation well tank field cultivation"` | 800 |
| 13.3 The quarry economy | Sandstone as the frontier town's strategic asset — the clearest economic argument available | SURVEY + TESTIMONY · `"sandstone quarry frontier economy"` | 850 |
| 13.4 Grants and revenue | *Bhāga* and *bhoga*; *devadaya* land; Devapāla's grant and the treasurer Dhamadeyava | EPIGRAPHY · `"bhaga bhoga devadaya grant revenue"` | 850 |
| 13.5 Crafts and guilds | *Śilpin*s, *sūtradhāra*s, *takṣaka*s; weavers' guilds; madder and indigo | DYNASTIC · `"market merchant guild sreni craft"` | 800 |

**Committed:** Devapāla's grant 1229 (VS 1286).
**Bridges:** from C12's institutions → C14 turns to the people in the economy.
**GAP:** the Paramāra land-grant corpus is absent; village names in the profile lack quoted readings. **Exclude Temple Economics here in particular** — it is this subject's false attractor.

### C14 People of the Plateau: Communities, Languages and Everyday Life
**Premise.** The people living at Udaypur now are not incidental to its history; the *mohallā* structure is the settlement pattern still in use.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 14.1 The town's quarters | Shikari, Mahua, Chaudaryana, Sarenthi, Utranti; the older settlement near Hajariya Mahadev | SURVEY · `"mohalla settlement quarter Udaypur"` | 850 |
| 14.2 Communities | Castes and communities of the district; the artisan groups the gazetteer names | GAZETTEER · `"Brahman Rajput caste occupation"` | 850 |
| 14.3 Demography | Population, households, literacy — what a 2011 count can and cannot say about an 11th-c. town | GAZETTEER · `"population census village inhabitants"` | 800 |
| 14.4 Languages | Hindi with Bundeli and Malvi; Sanskrit as the language of record against vernacular speech | GAZETTEER · `"language dialect spoken local"` | 750 |
| 14.5 Offices of the Paramāra town | *Pattakila*, *Mahājana*s, *śreṣṭhi*s — titles attested regionally, **not** at Udaypur by name | EPIGRAPHY · `"pattakila mahajana officials village"` | 800 |

**Committed:** 6,383 residents, 1,247 households, 54.28% literacy (Census 2011).
**Bridges:** from C13's economy → C15 moves from who people are to what they tell.
**GAP:** the medieval half rests on regional analogy, not Udaypur evidence — say so.

### C15 Stories of Udaypur: Festivals, Folklore and Oral Histories
**Premise.** What the town remembers differs from what the inscriptions record, and the difference is itself evidence.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 15.1 The living temple | Daily *āratī*; the *Ghariyālon kā Makān*, whose family struck the gong to keep ritual time; Śivarātri and the Śrāvaṇa Mondays | MONOGRAPH + TESTIMONY · `"Ghariyalon time-keepers gong aarti Sivaratri"` | 850 |
| 15.2 Founding legends | Bhrangarajpur and the defeated chief — how a conquest becomes an origin story | TESTIMONY · `filters={"content":"oral_testimony"}` | 800 |
| 15.3 The dancer of Udaysagar | The rope-walker promised half a kingdom; a tale encoding a real anxiety about royal promises | TESTIMONY · `"legend tale king dancer story"` | 800 |
| 15.4 A town that narrates itself | VMT's reportage as a source: partisan, first-person, invaluable — handled as testimony throughout | TESTIMONY · `"oral history residents recollection"` | 900 |
| 15.5 Memory against the record | Folk chronology beside epigraphic chronology; what each is for | TESTIMONY + EPIGRAPHY · — | 750 |

**Committed:** all material here is TESTIMONY, attributed to a named teller; no medieval fact rests on it.
**Bridges:** from C14's communities → C16 turns to the rupture that ended the Paramāra town.
**GAP:** no recorded oral-history interviews exist; the chapter rests on one book.

### C16 Conquests and Regimes: decline of the socio economic hub of Madhya Bharat
**Premise.** Udaypur outlasted the dynasty that made it; its demotion from royal town to *qasba* to village is the book's second subject.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 16.1 The later Paramāras | Naravarman to Devapāla; wars with Hoysalas, Yādavas and Chaulukyas | DYNASTIC · `"decline fall Paramara kingdom"` | 900 |
| 16.2 1305 — the state ends | Alāʾ al-Dīn Khaljī before Malwa's gates; Mahlak Deo defeated; the 1310 record as residual authority | DYNASTIC + EPIGRAPHY · `"Alauddin Khalji conquest Malwa Mahlak"` | 900 |
| 16.3 Tughluq Udaypur | The mosque of AH 737/739; reuse of carved material; the temple not razed | EPIGRAPHY · `"Tughluq mosque inscription Udaypur"` | 850 |
| 16.4 Continuity under new rule | The VS 1394 procession record — religious life continuing beside a new administration | EPIGRAPHY · `"procession jatra 1338 Hariraja"` | 800 |
| 16.5 Sultanate and Mughal town | A *qasba* in sarkar Chanderi; the Shahi Mahal; the Qanungo Baoli and its Kāyastha builders | EPIGRAPHY · `"Mughal qasba Chanderi subah"` | 800 |

**Committed:** 1293 Bhilsa raid; **1305 conquest**; 1310 residual inscription; AH 737/739; 1616–1632; 1645.
**Bridges:** from C15's living memory → C17 arrives when the town becomes an object of study.
**GAP:** published readings of the 1336–39 inscriptions are needed; the hadith text and spolia attribution are unquoted.

### C17 Archaeologists, Laws and Repairs: Making Udaypur a “Monument”, Udaypur in Independent India
**Premise.** Protection saved the temple and detached it from the town; the paperwork of preservation is also a history of separation.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 17.1 The antiquarians | Cunningham and Beglar; Beglar's Aurangzeb error and Cunningham's correction | MONOGRAPH · `"Beglar Cunningham report tour masjid Aurangzeb"` | 900 |
| 17.2 Scindia-era repair | The brass *mukha* cover given to the liṅga in 1775 — patronage before "conservation" existed | MONOGRAPH · `"brass cover mukha Khanderao Appaji Scindia"` | 800 |
| 17.3 Becoming protected | What ASI protection covers and what it omits — notably the hill, which is Forest Department land | SURVEY · `filters={"content":"conservation"}` | 900 |
| 17.4 Documentation as an act | INTACH's two volumes: ~50 listed sites, then the instrument survey of the fortification | SURVEY · `"drone total station survey documentation fortification"` | 850 |
| 17.5 The costs of monumentalisation | Protection froze the temple and orphaned everything around it — the book's central irony | — | 750 |

**Committed:** brass *mukhaliṅga* cover 1775 (Khanderao Appaji, general of Mahadji Scindia); Naṭarāja state-protected; hill under Forest Department.
**Bridges:** from C16's regime change → C18 arrives in the present.
**GAP:** **no ASI notification, protected-area boundary or post-1947 repair record exists in any source** — these must be obtained before drafting.

### C18 Present Tense: How the Town Lives with Its Past Today (based on Udaypur Jagta hua Kasba)
**Premise.** Several thousand people live beside a royal temple in a town that has been a village for six centuries.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| 18.1 A kasba on the margin | VMT's opening: a town of eight thousand with a thousand years of stories and nobody listening | TESTIMONY · `"kasba Udaypur inhabitants now"` | 850 |
| 18.2 Living in the fabric | Dry-stone houses and courtyards; gateways narrowed into lanes; carved fragments in the streets | SURVEY + TESTIMONY · `"village today people live condition"` | 850 |
| 18.3 Services and livelihoods | Roads, schools, water, power; agriculture and quarrying as work; the young leaving | GAZETTEER · `"development road school electricity"` | 800 |
| 18.4 Custodians and officials | The 2019 letter to the Collector; a resident's charge against the archaeology department — attributed | TESTIMONY · `filters={"content":"oral_testimony"}` | 850 |
| 18.5 Two Udaypurs | The monument's visitors and the village's residents share ground and rarely meet | — | 750 |

**Committed:** 6,383 (2011) **growing to** ~8,000 (VMT's estimate, c. 2021–22) — growth, not contradiction.
**Bridges:** from C17's monumentalisation → the Afterword names the remedy.
**GAP:** no fieldwork exists — interviews with residents, the ASI custodian, the panchayat and the priests are required.

### Afterword - (conservation attempts in present day, struggles of the village and how we can make it better)
**Premise.** The hill is collapsing while the temple is protected, and the case for acting is strongest where the evidence is newest.

| Sub-unit | Scope | Source-type · query | W |
|---|---|---|---|
| AW.1 Documented deterioration | Collapsed bastions, slope erosion, a wall whose decay "has entered a critical phase" | SURVEY · `"deterioration bastion collapse erosion critical"` | 900 |
| AW.2 Illegal mining | Dynamite blasts near the Naṭarāja and the wall; the Forest and Mining Acts already prohibit it | SURVEY · `"illegal mining dynamite blast threat geo heritage"` | 850 |
| AW.3 The protection gap | A protected temple beside an unprotected hill under another department, carrying unprotected sculpture | SURVEY · `filters={"content":"conservation"}` | 850 |
| AW.4 Proposals and their limits | INTACH's geo-tourism plan; the Kashi Vishwanath comparison VMT reports; what is realistic here | SURVEY + TESTIMONY · `"geo tourism pathway signage visitor centre"` | 800 |
| AW.5 The argument | What is owed to a place that was a capital and is now a village — advocacy, labelled as such | — | 750 |

**Committed:** illegal sandstone mining is the principal active threat (SURVEY).
**Bridges:** from C18's "two Udaypurs" → closes the book.
**GAP:** nothing postdates the INTACH survey; current ASI condition reports are needed.

---

## Pipeline handoff

Hand the drafter, per chapter: **the chapter block above** plus **all five CANON blocks in full**. The canon is binding, not reference. A drafter who re-opens a settled date, lineage or measurement has failed.

1. **Re-run retrieval** per sub-unit: `python kb_query.py "<query>" -k 12 --full --exclude Temple_Economics`. Programmatic: `kb_store.KBStore().search_bm25(q, k=12, filters={"content": "..."})` — each hit returns `rowid` (chunk id), `source`, `chunk`, `trail`, `text`, `score`.
2. **Always `--exclude Temple_Economics`.** Label filters do not remove it; only source exclusion does.
3. **Read neighbouring chunks** (`chunk` ±1 in the same `source`) — passages straddle boundaries.
4. **All 27 books are now indexed.** Nothing needs reading around the KB. (New rowids: Geo-Heritage 9467–9692, Pande 9693–10093, Skanda-Purāṇa 10094–10753.)
5. **Obey the matrix.** A measurement drafted from TESTIMONY, or a medieval fact from the GAZETTEER without a date-stamp, is a routing error — send it back.
6. **Describe signature objects from the object** (Canon 5), never from the generic trope.

---

## CANON DECISIONS REQUIRING SIGN-OFF

| # | Decision | Source | Reason |
|---|---|---|---|
| 1 | **Udayāditya was Bhoja's nephew, through a junior branch** | *Bhoja Paramara and His Times*, "Economic Condition" ch. ("Bhoja's nephew, Udayaditya"); Ganguly ch. IV ("a scion of a junior branch") | The two halves reconcile via the Udayapur praśasti pedigree (Sauravīra → Jñātā → Udayāditya). **See the caution in Canon 4** — "nephew" occurs once, in an aside |
| 2 | **Reign c. 1070–1093** | Ganguly ch. IV (Karṇa acceded 1063; Panhera has Jayasiṃha ruling in 1059; Naravarman "began his reign some time before 1094"); Pande ("ascended the throne in 1070 CE") | Two independent authorities converge; c. 1058–1087 to an endnote |
| 3 | **Bhoja 1000–1055** | Ganguly on Merutuṅga (55 y 7 m 3 d) | The standard history's own reconciliation; 1010 to an endnote |
| 4 | **1305 = fall of the state; 1310 = residual local authority** | Ganguly (AH 705); Udaypur inscription | Sequential, not contradictory — stated once |
| 5 | **Naṭarāja 8.2 × 4.2 m, six arms, reclining, unfinished** | Geo-Heritage #9536; INTACH catalogue #33 | Corroborated twice at survey grade; "~9 × 3 × 1.5 m" and the four-armed catalogue title to an endnote |
| 6 | **Fort wall 1,400 m, dry-stone, earthen rampart, no binder; 56 acres; predates Udayāditya** | Geo-Heritage #9491, #9589 | Instrument survey; **fabric description replaces the contested thickness figure** (18 ft / 8–10 ft / 4 m all in circulation) |
| 7 | **Eight subsidiary shrines** | Pande #9709 | The monograph on the temple is the authority; Beglar's seven to an endnote |
| 8 | **Population grew 6,383 (2011) → ~8,000 (c. 2021–22)** | Census; VMT | A rounded authorial estimate against a decadal count |
| 9 | **Temple Economics excluded entirely** | Characterised from the book itself | A contemporary policy tract that never treats Udaypur |
| 10 | **Succession: Lakṣmadeva briefly, then Naravarman (1094–1134)** | Ganguly; serpentine paper | Endnote the view that Naravarman succeeded directly |

**Still open for your ruling:** *Jagta Hua Kasba*'s printed year. No imprint page survives the OCR; internal evidence (a January 2021 heritage walk; INTACH's volume described as forthcoming) places it c. 2021–22. Decision 8 rests on it.
