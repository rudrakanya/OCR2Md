# Retrieval validation (Phase 5)

Chapter-scoped smoke tests against the Chroma collection `udaypur_kb`, run by `validate_retrieval.py`. Every query is filtered with `where={"in_<chapter>": True}`, so only chunks bucketed into that chapter are candidates.

## 1. Every chapter, top 5

### C1 — "ancient Vidisha Besnagar Heliodorus early references"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| patil-composite-inscriptions | primary_epigraphic | factual | 0.93 | single_source | In the 2nd century B.C., the Shungas supplanted the Mauryas. Pushyamitra Shunga's son, Cro |
| rajpurohit-bhoj-en | secondary_core | factual | 0.91 | udaypur_specific, single_source | According to Bhoj's *Shringara-manjari-katha*, Bhailasvamipur is the name of one part of V |
| patil-1952 | secondary_core | factual | 0.9 | single_source | Archaeologically, Vaishnavism is the earliest recorded sect in Madhya Bharat, as is eviden |
| patil-composite-inscriptions | primary_epigraphic | factual | 0.89 | single_source | The physical site of ancient **Vidisha**, situated in the fork of the Betwa (*Vetravati*)  |
| patil-1952 | secondary_core | factual | 0.88 | udaypur_specific, single_source | The chronological distribution of these monuments is equally interesting and informative.  |

### C2 — "Betwa river catchment rainfall monsoon streamflow"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| intach-geoheritage | field_observation_survey | factual | 0.98 | single_source, udaypur_specific | The climate of Vidisha is characterized by a hot summer and generally dry rains, except du |
| intach-2022-udaypur | field_observation_survey | observation | 0.94 | single_source, udaypur_specific | Vidisha lies on the Vindhyachal Plateau with several spurs towards North and North-East. A |
| kumar-2023-betwa | environmental_scientific | factual | 0.94 | single_source | We setup the SWAT model to simulate the streamflow of the Betwa River catchment under the  |
| kumar-2023-betwa | environmental_scientific | factual | 0.94 | single_source | *2.1. Study Area* The Betwa River originates from Raisen district of Madhya Pradesh and jo |
| kumar-2023-betwa | environmental_scientific | factual | 0.93 | single_source | - A transition from wetter to drier hydro-climatic conditions is evident in the upper Betw |

### C3 — "geology sandstone mesa butte caves of the Udaypur hill"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| intach-geoheritage | field_observation_survey | observation | 1.07 | single_source, udaypur_specific | this report, we use empirical evidence from the Udaypur Hill sandstone tableland in Udaypu |
| intach-geoheritage | field_observation_survey | factual | 1.06 | single_source, udaypur_specific | The mesa of Udaypur typifies a hill where dissection is negligible. The entirely planar to |
| intach-geoheritage | field_observation_survey | factual | 1.06 | udaypur_specific, single_source | The present study on Udaypur's geo-heritage examines the region's unique geological and cu |
| intach-geoheritage | field_observation_survey | observation | 1.05 | single_source, udaypur_specific | The maximum part of Udaypur Village is covered by the Sandstone and quaternary deposits, a |
| intach-geoheritage | field_observation_survey | observation | 1.05 | single_source, udaypur_specific | Walking up the hill, which rises almost 270 meters from the level of Udaypur village, we c |

### C4 — "Avanti Malwa Ujjain Dhara dynasties trade routes"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| patil-composite-inscriptions | primary_epigraphic | factual | 0.98 | udaypur_specific | The Chinese pilgrim Hiuen Tsang (640 A.D.) recorded visiting *Molopo* (Western Malwa under |
| singh-1984-bhoja | secondary_core | factual | 0.98 | udaypur_specific, single_source | The region of Malwa occupies a place 6f pride in the political and cultural history of Ind |
| ganguly-paramara | secondary_core | factual | 0.96 | udaypur_specific, single_source | K (h) Yamakastuti, (i) Satapadîka or Praśnottara paddhatih, (j) Kala-saptatih. The above c |
| patil-1952 | secondary_core | factual | 0.95 | udaypur_specific, single_source | In the field of art and architecture also, Malwa had reached a high pitch of excellence, a |
| ganguly-paramara | secondary_core | factual | 0.95 | single_source | In this and the following chapters, I shall now try to narrate the history of all the know |

### C5 — "Bhoja's own works, learning and authorship"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| patil-composite-inscriptions | primary_epigraphic | factual | 1.0 | udaypur_specific | The Chinese pilgrim Hiuen Tsang (640 A.D.) recorded visiting *Molopo* (Western Malwa under |
| singh-1984-bhoja | secondary_core | factual | 1.0 | single_source, udaypur_specific | Bhoja the Paramara ruler of Dhara, himself an author, was always surrounded by a crowd of  |
| singh-1984-bhoja | secondary_core | factual | 0.98 | udaypur_specific, single_source | In this battle Bhoja was assisted by Satyaraja, the Paramara ruler of Vagada and who was B |
| singh-1984-bhoja | secondary_core | factual | 0.98 | single_source, udaypur_specific | His faith, it does mount to the feet of the husband of Parvatl, dau- ghter of the lord of  |
| singh-1984-bhoja | secondary_core | factual | 0.97 | udaypur_specific, single_source | Whatever might be the ease, it is cer(ain.lha( in this war, Bhoja ultimately emerged victo |

### C6 — "Udayaditya founded Udaypur temple and tank 1059 1080"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| patil-1952 | secondary_core | factual | 1.0 | contested, udaypur_specific | One of the many old Sanskrit inscriptions on this temple records that the Paramara king Ud |
| patil-composite-inscriptions | primary_epigraphic | factual | 0.99 | udaypur_specific, contested | A premier archeological town located 4 miles east of Bareth station. * **The Udayeshvara ( |
| ganguly-paramara | secondary_core | factual | 0.99 | single_source, udaypur_specific | An inscription, dated 1077 A. D., from Shikarpur Taluq, records that "he was the source of |
| ganguly-paramara | secondary_core | factual | 0.99 | single_source, udaypur_specific | 138 HISTORY OF THE PARAMARA DYNASTY by him in 1059 A. D, and was considered the most super |
| ganguly-paramara | secondary_core | factual | 0.99 | udaypur_specific, single_source | Udayaditya is reported to have erected many other temples, caused tanks to be excavated, p |

### C7 — "Udayesvara temple Bhumija plan shikhara sculpture"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| pande-udayesvara | secondary_core | factual | 1.03 | udaypur_specific, single_source | 2 / THE UDAYEŚVARA TEMPLE Pl. 1. View of the śikhara from the south-west side. The Art of  |
| pande-udayesvara | secondary_core | factual | 1.0 | folklore, udaypur_specific, single_source | Near the Udayeśvara temple is a small temple, later in date, plain and unostentatious, cal |
| hardy-2007 | secondary_comparative | factual | 1.0 | contested, udaypur_specific | 20.1 Udayeshvara temple, Udayapur (MP), founded 1059 The Paramaras, ambitious rulers of Ma |
| intach-2022-udaypur | field_observation_survey | observation | 0.99 | udaypur_specific, single_source | 33. Ravan Tol Chaturbhuji Shiva Murti It is located on the outskirts of Udaypur to the eas |
| pande-udayesvara | secondary_core | factual | 0.99 | single_source, udaypur_specific | ARCHITECTURE AND SCULPTURE OF THE UDAYEŚVARA TEMPLE / 65 Pl. 93. View of buttresses betwee |

### C8 — "inscriptions of Udaypur serpentine grammar prasasti"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| singh-serpentine | secondary_core | factual | 1.07 | udaypur_specific, single_source | **Saarthak Singh** This paper presents a newly-discovered inscription from Udaypur (distri |
| singh-serpentine | secondary_core | factual | 1.04 | udaypur_specific, single_source, contested | Udaypur, varṇṇanāgakṛpāṇikā, Paramāra, Malwa The Śiva temple of Udaypur in the Vidisha dis |
| singh-serpentine | secondary_core | factual | 1.04 | udaypur_specific, single_source | The grammatical inscription from Udaypur, together with those from Ujjain, Dhar, and Un, t |
| singh-serpentine | secondary_core | factual | 1.04 | udaypur_specific, single_source | - **Fig. 1–2.** Udayeśvara temple at Udaypur, view from the southeast locating the inscrip |
| ganguly-paramara | secondary_core | factual | 0.96 | udaypur_specific, single_source | An inscription, dated 1077 A. D., from Shikarpur Taluq, records that "he was the source of |

### C9 — "fortification wall gates stepwell baoli mosque"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| intach-geoheritage | field_observation_survey | observation | 1.06 | udaypur_specific, single_source | Image 71 A rear side gateway Image 72 Small niche made of stone at entrance of security th |
| intach-2022-udaypur | field_observation_survey | observation | 1.04 | udaypur_specific, single_source | The stepwell is an 11th century CE structure situated at GPS 23.53.48.04 N and 78.3.10.51  |
| intach-2022-udaypur | field_observation_survey | observation | 1.04 | folklore, single_source, udaypur_specific | The hill has two mounds, a large plateau and a vertical tower of natural rock. The fortifi |
| intach-geoheritage | field_observation_survey | observation | 1.04 | udaypur_specific, single_source | Image 81 Entrance gateway Gates are of strategic importance to fortification walls as they |
| intach-2022-udaypur | field_observation_survey | observation | 1.03 | opinion, single_source, udaypur_specific | There are various typologies found in Udaypurso to better understand the settlement patter |

### C10 — "Saiva Siddhanta ritual and the intellectual world of Malwa"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| pande-udayesvara | secondary_core | factual | 1.0 | single_source, udaypur_specific | The Udayeśvara temple is based on a Śaiva sect which derives from Śaiva Siddhānta. This te |
| pande-udayesvara | secondary_core | factual | 0.98 | prescriptive, udaypur_specific, single_source | Atharvaveda, the guardians of the directions are conceived as 'protectors' and 'arrows' or |
| pande-udayesvara | secondary_core | inference | 0.94 | single_source, udaypur_specific | It is interesting to note that the sculptural programme of the Udayeśvara temple reflects  |
| ganguly-paramara | secondary_core | factual | 0.92 | udaypur_specific, single_source | I to the deity. Sometimes he walked thrice round the sacred cow with other purificatory ce |
| pande-udayesvara | secondary_core | factual | 0.91 | single_source | The southern Śaiva Siddhānta derives from early sources, the most important of which were  |

### C11 — "agriculture markets stone quarrying crafts economy"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| intach-2022-udaypur | field_observation_survey | observation | 0.96 | udaypur_specific, single_source | The major population of Udaypur is engaged in agriculture and for further study and better |
| intach-2022-udaypur | field_observation_survey | observation | 0.92 | udaypur_specific, single_source | The construction period of this Darwaza looks to be 11$^{th}$ century CE. It is situated a |
| intach-geoheritage | field_observation_survey | factual | 0.91 | udaypur_specific, single_source | The major part of this report shows that physiological formation shows that these rocks ar |
| intach-geoheritage | field_observation_survey | factual | 0.9 | single_source, udaypur_specific | Udaypur is covered with 75% of black cotton soil. The other 25% is red-yellow mixed soils  |
| intach-2022-udaypur | field_observation_survey | factual | 0.86 | single_source, udaypur_specific | MAP B2.1 LISTED HERITAGE STRUCTURES IN UDAYPUR VILLAGE REMAINS OF FORT COMPLEX 1. Hill For |

### C12 — "communities castes dialects population of the district"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| intach-2022-udaypur | field_observation_survey | observation | 0.82 | single_source, udaypur_specific | The major population of Udaypur is engaged in agriculture and for further study and better |
| tiwari-jhk-en | field_observation_reportage | observation | 0.8 | single_source, udaypur_specific | We improved its packaging further. We did not even call it a presentation. We called it —  |
| tiwari-jhk-en | field_observation_reportage | factual | 0.8 | single_source, udaypur_specific | should be heard at least once. In any case, how few events are held on history! Pandit Man |
| tiwari-jhk-en | field_observation_reportage | factual | 0.8 | udaypur_specific, single_source | I said that this is quite right. My footfall in your locality has not been much. I am of a |
| samarangana | primary_authorial_paramara | factual | 0.79 | single_source, original_script | ``` # Chapter 50: The good and bad indication of Prāsādas CHAPTER 50 The good and bad indi |

### C13 — "legend folklore story told by villagers"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| tiwari-jhk-en | field_observation_reportage | observation | 0.94 | udaypur_specific, single_source | The biggest change that has come this year is that the aware people of Ganj Basoda have be |
| tiwari-jhk-en | field_observation_reportage | observation | 0.94 | udaypur_specific, single_source | — [the story of history's storms,] in whose excavation, decades ago, an old residence with |
| tiwari-jhk-en | field_observation_reportage | observation | 0.94 | single_source, udaypur_specific | Like Gwalior and Chanderi, the presence of Jain idols upon the hilly rocks tells us that t |
| tiwari-jhk-hi | field_observation_reportage | observation | 0.92 | single_source, udaypur_specific, embeds_primary_text | उदयदित्य ने उदयपुर में रहते हुए अपनी गौरवशाली राज परंपरा को ही बढ़ाया था। यही वजह है कि सद |
| tiwari-jhk-en | field_observation_reportage | factual | 0.92 | udaypur_specific, single_source | Udayaditya, while living in Udaipur, only advanced his glorious royal tradition. This is t |

### C14 — "Iltutmish Tughluq Mughal conquest and decline"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| ganguly-paramara | secondary_core | factual | 1.03 | contested, udaypur_specific | The great Nilakantheśvara temple at Udayapur was built by Udayaditya in Sam 1116 = 1059 A. |
| ganguly-paramara | secondary_core | factual | 0.97 | single_source, udaypur_specific | The Vikrama-ColanUla tells us that Vikrama Cola's general, who was a I Progress Report of  |
| patil-composite-inscriptions | primary_epigraphic | factual | 0.96 | udaypur_specific | The Chinese pilgrim Hiuen Tsang (640 A.D.) recorded visiting *Molopo* (Western Malwa under |
| ganguly-paramara | secondary_core | factual | 0.92 | single_source, udaypur_specific | FROM JAYASIMHA TO JAYAVARMAN I. Jayasimha I-reconquest of Malwa with the help of the Caluk |
| ganguly-paramara | secondary_core | factual | 0.92 | udaypur_specific, single_source | dark days of its rapid decline. Hence it was evident that Malwa was again going to suffer  |

### C15 — "Archaeological Survey protection repairs conservation"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| intach-2022-udaypur | field_observation_survey | observation | 0.99 | single_source, udaypur_specific | landscape along with built heritage which is scattered in and lying unprotected for centur |
| intach-2022-udaypur | field_observation_survey | observation | 0.98 | single_source, udaypur_specific | Further, it also describes the present condition and state of conservation of the monument |
| intach-geoheritage | field_observation_survey | factual | 0.97 | udaypur_specific, single_source | 6. Other Relevant Aspects- Investigating geo-tourism potential, conservation challenges, a |
| intach-geoheritage | field_observation_survey | factual | 0.97 | single_source, udaypur_specific | By recognizing and promoting Udaypur's geo-heritage, this study aims to contribute to its  |
| intach-2022-udaypur | field_observation_survey | observation | 0.95 | single_source | Figure 114: Sculpture of Bhairava on the outer of Garbhagriha Figure 115: Small shrine in  |

### C16 — "present-day village life lanes panchayat people"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| tiwari-jhk-en | field_observation_reportage | factual | 1.0 | udaypur_specific, single_source | From Udaipur up to Ganj Basoda and Vidisha, from the village panchayat up to the district  |
| tiwari-jhk-en | field_observation_reportage | factual | 1.0 | udaypur_specific, single_source | I had come here many times before this too, and each time this wretched lane taunted me. S |
| tiwari-jhk-en | field_observation_reportage | observation | 0.99 | udaypur_specific, single_source | We improved its packaging further. We did not even call it a presentation. We called it —  |
| tiwari-jhk-hi | field_observation_reportage | observation | 0.99 | udaypur_specific, single_source, embeds_primary_text | राजस्थान और दक्षिण भारत के ऐतिहासिक स्थानों की तरह चमका सकती है। यहां इतना कुछ देखने और सम |
| tiwari-jhk-en | field_observation_reportage | factual | 0.99 | single_source, udaypur_specific | Hear the matter from the start. This correspondent, in his daily rush-and-bustle of Vidish |

### AF — "conservation today encroachment neglect what can be done"

| source | type | status | score | flags | text |
|---|---|---|--:|---|---|
| intach-2022-udaypur | field_observation_survey | observation | 0.96 | single_source, udaypur_specific | Further, it also describes the present condition and state of conservation of the monument |
| intach-geoheritage | field_observation_survey | observation | 0.96 | udaypur_specific, single_source | 1) https://vidisha.nic.in/en/ 2) https://www.cambridge.org/core/terms The town of Udaypur  |
| tiwari-jhk-en | field_observation_reportage | observation | 0.95 | udaypur_specific, single_source | Neelkantheshwar Shankar Bhagwan does not sit only for the devotees who go to Udaipur with  |
| intach-geoheritage | field_observation_survey | factual | 0.95 | udaypur_specific, single_source | 6. Other Relevant Aspects- Investigating geo-tourism potential, conservation challenges, a |
| intach-2022-udaypur | field_observation_survey | observation | 0.95 | udaypur_specific, single_source | landscape along with built heritage which is scattered in and lying unprotected for centur |

## 2. Does the new book reach C5 and C10?

| test | result |
|---|---|
| C5 bucket contains the new book | **41 chunks**; best rank 360 of 2880 on an English query |
| C10 bucket contains the new book | **20 chunks**; best rank 557 of 2769 on an English query |
| C5, the same question asked in Devanagari | best rank **34** of 2880 |
| C5 filtered to the new book (`--source rajamartanda-bhoja`) | returns 5; top: `rajamartanda-bhoja-00043` (quotable=False) |

## 3. Does the yoga-doctrine layer stay out of unrelated chapters?

| chapter | new-book chunks bucketed | of which yoga-doctrine |
|---|--:|--:|
| C1 | 0 | 0 |
| C2 | 2 | 0 |
| C3 | 1 | 0 |
| C4 | 8 | 0 |
| C5 | 41 | 0 |
| C6 | 1 | 0 |
| C7 | 0 | 0 |
| C8 | 4 | 0 |
| C9 | 3 | 0 |
| C10 | 20 | 0 |
| C11 | 4 | 0 |
| C12 | 12 | 0 |
| C13 | 13 | 0 |
| C14 | 1 | 0 |
| C15 | 6 | 0 |
| C16 | 6 | 0 |
| AF | 3 | 0 |

Yoga-doctrine chunks bucketed outside C5/C10: **0**.

## 4. Is the Tiwari alias fix holding (C13, C16)?

| chapter | Tiwari chunks in top 10 |
|---|--:|
| C13 | 10 |
| C16 | 10 |

## 5. Is non-quotable text ever returned as quotable?

With `--quotable-only`, 340 results across all chapters, of which non-quotable: **0**.

## 6. Is the archive reachable?

- active collection: 14,647 records; archive collection: 4,434 records
- records flagged `is_archived` inside the active collection: **0**
- `kb3_chroma_query.py` names only `udaypur_kb`; the archive collection is never opened by the query path.

## 7. Source mix actually reaching the chapters

| chapter | source types in top 5 |
|---|---|
| C1 | secondary_core x3, primary_epigraphic x2 |
| C2 | environmental_scientific x3, field_observation_survey x2 |
| C3 | field_observation_survey x5 |
| C4 | secondary_core x4, primary_epigraphic x1 |
| C5 | secondary_core x4, primary_epigraphic x1 |
| C6 | secondary_core x4, primary_epigraphic x1 |
| C7 | secondary_core x3, secondary_comparative x1, field_observation_survey x1 |
| C8 | secondary_core x5 |
| C9 | field_observation_survey x5 |
| C10 | secondary_core x5 |
| C11 | field_observation_survey x5 |
| C12 | field_observation_reportage x3, field_observation_survey x1, primary_authorial_paramara x1 |
| C13 | field_observation_reportage x5 |
| C14 | secondary_core x4, primary_epigraphic x1 |
| C15 | field_observation_survey x5 |
| C16 | field_observation_reportage x5 |
| AF | field_observation_survey x4, field_observation_reportage x1 |

## 8. Verdict and limitations

**Passing**

- Chapter scoping is a metadata filter, so a chapter query can only see chunks bucketed into that chapter.
- The yoga-doctrine layer of the Rājamārtaṇḍa is bucketed into **C5 and C10 only**. Leakage elsewhere: 0 of 183 chunks.
- The Bhoja-authorship layer (61 chunks: title page, editor's introduction, passages naming Bhoja) reaches C5 (41) and C10 (20).
- `--quotable-only` returned **0** AI-reworded or OCR-needs_recheck chunks in 340 results.
- The archive holds 4,434 chunks in a separate collection; **0** archived records appear in the active collection, and the query module never names the archive.
- The Tiwari alias fix holds: 10 of 10 top results in both C13 and C16 come from *Jagta Hua Kasba*.
- Per-chapter source mixes match the chapter profiles: field surveys lead C3, C9, C11 and C15; reportage leads C13 and C16; environmental science leads C2; epigraphy and core scholarship lead C1, C4, C6, C8 and C14.

**The real limitation: cross-lingual retrieval with a small model**

The new book's introduction is in Hindi and its commentary in Sanskrit. With `multilingual-e5-small`:

| question | best rank of a new-book chunk in C5 (bucket = 2,880) |
|---|---|
| asked in English ("Bhoja's own works, learning and authorship") | 360 |
| the same question in Devanagari | **34** |
| filtered to the book (`--source rajamartanda-bhoja`) | 1 |

So the book is correctly classified, bucketed and reachable, but an **English** query will not pull its Hindi pages into a top-10 list. Three ways to work with that, in order of cost:

1. Ask chapter questions that touch Devanagari sources in Devanagari, or include key terms (भोज, राजमार्तण्ड) in the query.
2. Use `--source rajamartanda-bhoja --chapter C5` when drafting the Bhoja-authorship passages; it ranks the book's own chunks with all flags intact.
3. Re-embed with `BAAI/bge-m3` (`python embed_e5.py --model BAAI/bge-m3 --out kb3/emb_bge --prefix ""`, then `stage2_build.py --vectors kb3/emb_bge --model BAAI/bge-m3 --query-prefix ""`, then `build_chroma.py --reset`). bge-m3 aligns languages far better. It needs a machine with more free memory than this one: the run here was killed twice at ~3 GB.

**Also measured, and switched off:** the semantic corroboration detector. With e5-small, random claim-bearing pairs average cosine 0.811 (p99 0.878), so at 0.85 it produced 236,856 "corroborations" and at 0.92 it still paired unrelated survey prose with OCR garbage. A false corroboration tells the writer a claim is confirmed when it is not, so corroboration now rests on dated entity-year keys and the claims register. Re-enable with `--corro-cos 0.9` after moving to bge-m3.

**Quotability of the new book:** only 31 of its 116 pages passed the OCR gate, so most of its chunks are `is_quotable: false`. They are retrievable and citable by page, but the page image must be checked before any Sanskrit is quoted.
