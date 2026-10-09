# The Udaypur book — sourcebook

Chapter by chapter, the evidence the knowledge base holds, grouped by sub-theme and cited in full. It gathers and cites; it contains no chapter prose.

**How to use this.** Every excerpt carries its source code, book, page and KB chunk id, so any line can be checked without searching the corpus. Codes resolve in the table below and in `source_codes.md`. Quotations are gated: a chunk the KB marks `is_quotable: false` — AI-reworded or OCR-damaged text — never appears as a quotation, only as a marked paraphrase. Page numbers appear only where the KB actually holds one; otherwise `p. —`, and for the Samarāṅgaṇa-sūtradhāra a section trail, because its page numbers are known to be corrupt. Nothing here is invented, and thin coverage is flagged rather than filled.

**Excluded by design.** The knowledge base contains six model-written synthesis chunks under the source id `ai-derived` (`AI-0001`–`AI-0006`), bucketed into ten chapters. They are not a source and do not appear anywhere below. They shipped marked quotable; they were re-flagged `is_quotable: false` and archived on 2026-09-29, their chapter buckets cleared, and `build_chroma.py` now archives and un-buckets anything tagged `ai_derived` so a rebuild cannot restore them.

**Selection.** Each chapter's bucket is clustered into 6 sub-themes on the KB's own embeddings; the top 4 excerpts per sub-theme are kept, ranked by primacy, then claim credibility, then source reliability, then relevance to that chapter. Excerpts are trimmed to about 480 characters, marked `…` where trimmed. No source may supply more than 4 excerpts to one chapter, so a large book cannot crowd out the rest of the shelf.

<a id="contents"></a>
## Contents

| § | chapter | chunks | sources | key facts | excerpts | watch |
|---|---|--:|--:|--:|--:|---|
| [C1](#c1--udaypur-and-early-vidisha-a-small-town-with-a-long-memory) | Udaypur and Early Vidisha: A Small Town with a Long Memory | 1,998 | 25 | 20 | 24 |  |
| [C2](#c2--the-betwa-valley-land-rivers-and-seasons) | The Betwa Valley: Land, Rivers and Seasons | 1,330 | 25 | 19 | 24 |  |
| [C3](#c3--stones-and-forests-geology-flora-and-fauna) | Stones and Forests: Geology, Flora and Fauna | 1,715 | 24 | 19 | 22 |  |
| [C4](#c4--from-avanti-to-malwa-dynasties-trade-routes-and-sacred-cities) | From Avanti to Malwa: Dynasties, Trade Routes and Sacred Cities | 2,538 | 25 | 19 | 24 |  |
| [C5](#c5--the-paramāras-and-bhoja-kingship-learning-and-temple-building) | The Paramāras and Bhoja: Kingship, Learning and Temple Building | 2,877 | 25 | 20 | 24 |  |
| [C6](#c6--udayādityas-foundation-town-temple-and-tank) | Udayāditya's Foundation: Town, Temple and Tank | 1,570 | 25 | 20 | 24 |  |
| [C7](#c7--udayeśvara-in-stone-architecture-sculpture-and-iconography) | Udayeśvara in Stone: Architecture, Sculpture and Iconography | 4,197 | 23 | 18 | 24 | few sources |
| [C8](#c8--words-in-stone-inscriptions-languages-and-the-serpentine-scimitar-of-letters) | Words in Stone: Inscriptions, Languages and the Serpentine Scimitar of Letters | 2,150 | 26 | 19 | 24 |  |
| [C9](#c9--built-heritage-fortifications-mosques-shrines-and-stepwells) | Built Heritage: Fortifications, Mosques, Shrines and Stepwells | 2,330 | 24 | 19 | 24 |  |
| [C10](#c10--ritual-and-knowledge-śaiva-traditions-and-intellectual-worlds) | Ritual and Knowledge: Śaiva Traditions and Intellectual Worlds | 2,769 | 24 | 19 | 24 |  |
| [C11](#c11--fields-wells-and-markets-agriculture-economy-and-crafts) | Fields, Wells and Markets: Agriculture, Economy and Crafts | 1,338 | 25 | 19 | 24 |  |
| [C12](#c12--people-of-the-plateau-communities-languages-and-everyday-life) | People of the Plateau: Communities, Languages and Everyday Life | 1,667 | 26 | 19 | 23 |  |
| [C13](#c13--stories-of-udaypur-festivals-folklore-and-oral-histories) | Stories of Udaypur: Festivals, Folklore and Oral Histories | 1,972 | 26 | 19 | 24 |  |
| [C14](#c14--conquests-and-regimes-decline-of-the-socio-economic-hub-of-madhya-bharat) | Conquests and Regimes: Decline of the Socio-Economic Hub of Madhya Bharat | 1,739 | 25 | 19 | 24 |  |
| [C15](#c15--archaeologists-laws-and-repairs-making-udaypur-a-monument-udaypur-in-independent-india) | Archaeologists, Laws and Repairs: Making Udaypur a 'Monument'; Udaypur in Independent India | 1,685 | 25 | 19 | 23 |  |
| [C16](#c16--present-tense-how-the-town-lives-with-its-past-today) | Present Tense: How the Town Lives with Its Past Today | 1,637 | 26 | 19 | 24 |  |
| [AF](#af--afterword-conservation-today--struggles-of-the-village-and-how-to-help) | Afterword: Conservation Today — Struggles of the Village and How to Help | 1,412 | 24 | 19 | 24 |  |

[Source codes](#source-codes) · [Coverage matrix](#coverage-matrix--sources--chapters)

## Source codes

| code | book | author | source type |
|---|---|---|---|
| `ADH` | Some Paramāra Temples From Madhya Pradesh: A Case Study of Village Un | Swati Mondal Adhikari | secondary_comparative |
| `BET-K` | Streamflow of the Betwa River under the Combined Effect of LU-LC and Climate Change | Amit Kumar et al. | environmental_scientific |
| `BET-S` | Long-term historic changes in climatic variables of Betwa Basin, India | Shakti Suryavanshi, Ashish Pandey, Umesh Chandra Chaube, Nitin Joshi | environmental_scientific |
| `BHJ-H` | भोजदेव (Bhojadeva) | Not named in file | secondary_core |
| `DEV` | Temples of North India | Krishna Deva | secondary_comparative |
| `GAN` | History of the Paramāra Dynasty | D. C. Ganguly | secondary_core |
| `GAZ-VID` | Madhya Pradesh District Gazetteers: Vidisha | P. N. Shrivastav, Rajendra Verma | reference_tertiary |
| `GUP` | Iconography of the Hindus, Buddhists and Jains | R. S. Gupte | reference_tertiary |
| `HAR` | The Temple Architecture of India | Adam Hardy | secondary_comparative |
| `INT-ARC` | The Architectural Splendor of Udaypur | INTACH Bhopal Chapter | field_observation_survey |
| `INT-GEO` | Geo-Heritage of Udaypur: The Third Eye | INTACH Bhopal Chapter | field_observation_survey |
| `KRAM-1` | The Hindu Temple, Volume I | Stella Kramrisch | secondary_comparative |
| `KRAM-2` | The Hindu Temple, Volume II | Stella Kramrisch | secondary_comparative |
| `PAN` | The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta | Anupa Pande | secondary_core |
| `PAR` | History of the Parmar Rajput Dynasty | Not captured in extraction | secondary_core |
| `PAT-CH` | The Cultural Heritage of Madhya Bharat | D. R. Patil | secondary_core |
| `PAT-INS` | Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions | D. R. Patil (Part I) + unattributed additions | primary_epigraphic |
| `PAT-TEM` | The Cultural Heritage of Madhya Bharat — temples and architecture (composite) | D. R. Patil + Swati Mondal Adhikari (bundled) | secondary_comparative |
| `RAJ-E` | King Bhoj and Paramara-period Town Architecture (English translation) | Bhagwatilal Rajpurohit | secondary_core |
| `RAJM` | Pātañjala-Yogasūtram with the Rājamārtaṇḍa-vṛtti of Bhojadeva (ed. Ram Shankar Bhattacharya) | Bhojadeva (Bhoja Paramāra), commentary; Patañjali, sūtras; Ram Shankar Bhattacharya, editor | primary_authorial_paramara |
| `SAM` | Samarāṅgaṇa-sūtradhāra | Traditionally attributed to Bhoja (not stated in file) | primary_authorial_paramara |
| `SIN-B` | Bhoja Paramara and His Times | Mahesh Singh | secondary_core |
| `SIN-S` | A serpentine scimitar of letters from Udaypur, district Vidisha, M.P. | Saarthak Singh | secondary_core |
| `SIN-T` | Temple Economics: Arthvyavstha of Mandir (Vol. I) | Sandeep Singh | contextual_thematic |
| `SKP-13` | The Skanda-Purāṇa, Part XIII (AITM series) | Not named in file (Motilal Banarsidass, AITM series translation) | primary_scriptural |
| `TIW-E` | Jagta Hua Kasba / कथा उदयपुर (English translation) | Tiwari (VMT) | field_observation_reportage |
| `TIW-H` | कथा उदयपुर (Jagta Hua Kasba) — Hindi original | Tiwari (VMT) | field_observation_reportage |

## C1 — Udaypur and Early Vidisha: A Small Town with a Long Memory

[↑ contents](#contents)

**Coverage.** 1,998 chunks from 25 sources (`ADH`, `BET-S`, `BHJ-H`, `DEV`, `GAN`, `GAZ-VID`, `GUP`, `HAR`, `INT-ARC`, `INT-GEO`, `KRAM-1`, `KRAM-2`, `PAN`, `PAR`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `SAM`, `SIN-B`, `SIN-S`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: primary_authorial_paramara 519, secondary_core 489, primary_scriptural 273, secondary_comparative 253, field_observation_reportage 195, reference_tertiary 159, field_observation_survey 76, primary_epigraphic 30, contextual_thematic 3, environmental_scientific 1. The largest single contributor is `SAM` with 519 chunks (26% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- The date of Udayāditya's accession to the throne of Malwa is not settled: four reckonings in the corpus give four different spans, and a record of 1059 places the paramount throne with Jayasiṃha in the year the Udaypur foundation inscription shows Udayāditya building. — competing values: **1058–1087** (`PAT-CH`); **1059–1086** (`GAN`); **c. 1059–93** (`INT-ARC`); **1070–1093 (from the coinage)** (`INT-ARC`) `[contested]` `[curated]`
  - The counter-evidence is the Panhera inscription of V.S. 1116 (1059 CE), issued by Jayasiṃha's feudatory Mandalika, which reports Jayasiṃha ruling Malwa at that date; the reconciliation offered in the literature is that Udayāditya held his paternal territory and built at Udaypur in 1059 without yet being sovereign. That reconciliation is labelled speculation in the KB and must not be asserted as settled.
  - traceable to: `ganguly-paramara-00262`, `ganguly-paramara-00275`, `ganguly-paramara-00274`, `patil-1952-00095`, `ganguly-paramara-00568`, `intach-2022-udaypur-00127`, `intach-2022-udaypur-00075`
- In the Bhailasvami Mahadvadashaka province, the provincial governor of Udaipur in 1171 CE was Lunapasaka;² this is clear from the inscription of Vikram Samvat 1229. — `RAJ-E` `[single-source]`
- The Shunga hold over Vidisha is verified by the famous Besnagar column inscription of Heliodoros, an ambassador sent by the Indo-Greek King Antialcidas of Taxila to the court of King Bhagabhadra. — `PAT-INS` `[single-source]`
- The Paramara king Bhoja Deva (1000–1055 A.D.) ruled over Bhilsa, and his successor Udayaditya built the magnificent **Nilkanthesvar temple at Udaypur**. — `GAZ-VID` `[single-source]`
- Notable structural remains include the rock-cut Chaturbhuja temple (875 A.D.) at Gwalior Fort and Krishna temple pillar at Pathari (861 A.D.), totaling 87 shrines across the territory. — `PAT-TEM` `[single-source]`
- Pushyamitra Shunga's son, Crown Prince Agnimitra, ruled as Viceroy at Vidisha, an event immortalized in Kalidasa's *Malavikagnimitra*. — `PAT-INS` `[single-source]`
- The town features the **Lohangi Rock**, a lone sandstone peak housing the tomb of Lohangi Pir, an old covered masonry tank, and a ruined mosque built under Sultan Mahmud Khilji I (1457 A.D.). — `PAT-INS` `[single-source]`
- The inscription states that a Greek ambassador from Taxila at the court of the Shunga King of Vidisha (Bhilsa) had become a convert to the Bhagavata sect and raised a Garuda pillar in honour of the god Vasudeva. — `PAT-CH` `[single-source]`
- Kumarapala died in 1172 A. D., and was succeeded by Ajayapala (1172-1176 A. D.). — `GAN` `[single-source]`
- The prosperity of Madhya Bharat territories under the Guptas is well reflected in the few monuments left at Pawaya, Tumain (Guna District), Besnagar, and Udaygiri (Bhilsa), Mandsor, and in the famous caves and paintings of Bagh. — `PAT-TEM` `[single-source]`
- The towns of Ujjain, Dhara, Dasapura, VidiSa, Bhojpur, Gyaraspur, Udaypur, On, Onkar-Mandhata, Chandriivatj and several others developed during the rule of the Paramaras. — `SIN-B` `[single-source]`
- Amidst the eastern part of the Vindhyachal range is located a village named Udaypur with a total geographical area of 1966 hectares/ 19.66 Square Kilometers (km2). — `INT-ARC` `[single-source]`
- April 17, 2022 Madan Mohan Upadhyay, IAS(Retd) State Convenor-INTACH, MP Umashankar Bhargav, IAS Vidisha district has been known for ages for the rich and diverse heritage it possesses. — `INT-ARC` `[single-source]`
- О beautiful lady, all the Tirthas of the earth are present there, such as Dharmaranya, Phalgu Tirtha, Puskara, Naimi§a, Gaya, Prayaga, Kuruksetra, Kedara and Amaresvara. — `SKP-13` `[single-source]`
- All the holy rivers, viz. Candrabhaga, Vipasa, Sarayu, Devika, Kuhii, Godavari, Satadru, Bahuda and Vetravati are in confluence with Ganga. — `SKP-13` `[single-source]`
- Livelihoods, Mobility, and Housing: In Search of Missing Links in Indian Towns. — `INT-GEO` `[single-source]`
- Tri-bhadra, Catur-bhadra, & Pañca-bhadra Clusters * **Tri-bhadra (56 Options)**: Advanced models including *Aindra, Viloma, Āyāma, Vadha, Ekākṣa, Antika, Prakāśa,* and *Paitra* matrices [cite: 6456, 6462, 6468]. — `SAM` `[single-source]`
- Then Rama went to Mahendra, Malaya, Sahya, Himalaya and the beautiful and meritorios Badarikasrama. — `SKP-13` `[single-source]`
- Uttare£vara Index PURANA m B ook V: AVANTYAKHANDA S ection II: CATURASITI-LINGA-MAh ATMYA GLORIFICATION OF EIGHTYFOUR LINGA SHRINES IN AVANTl1 CHAPTER ONE Agastyesvara2 + _ + Obeisance to Sri Ganesa. — `SKP-13` `[single-source]`
- Barely represented in this bucket, so anything resting on them is a thin reed: `BET-S`, `PAR`, `SIN-S`, `SIN-T` — `[gap]`

### C1.6 — created, having, deserves, create, parts

> Arjuna). Añjāna (collyrium) Kadara¹ (white catchu) Aśoka, Tiniśa² and red sandal. शिरीषसर्जन्यग्रोधवेणवः कीलकर्मणि। पुन्नामानो द्रुमाः शस्ताः स्त्रीनामानो विगर्हिताः ॥३॥ Śirīşa, Sarja, Nyagrodha (Indian Fig tree or Vata) (Banyan tree) and Venu (bamboo or cane or ratton) in the work of pegs the masculine named tees are excellent and the feminine named are abhorable. अश्वत्थः खदिरश्चैतौ विप्राणां वृद्धिकारकौ। रक्तचन्दनवेणूत्थकीलौ क्षत्रस्य पूजितौ ।।४।। The Banyan and Catchu are…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 37: Kīlaka Sūtrapāta (the insertion of nails and threads) · `samarangana-00535`

> [paraphrase — not a verbatim quote; source text unreliable] The magazine (*Koşthāgāra*)⁵ and the armoury⁶ or arsenal, a container of commodities or a tool for weighing or store for manufactured articles by their establishments and by the (construction) of Fountains, for bath or ablution, (Halls) for music, dance and physical exercise. [cite: 525] शय्यावासगृहप्रेक्षावेश्मादर्शगृहैः पृथक्। क्रीडादोलाश्रयारिष्टगृहान्तः पुरवेश्मभिः॥२४।। And by separately (created) a mirror house, a theatre hall, a toilet makeup pavilion, and a sleeping lo…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. SAMARĀNGANA-SŪTRADHĀRA > CHAPTER 2: The Conversation Between Viśvakarmā and His Sons (Mānasa Putras) > FOOTNOTES & TEXTUAL CRITICAL NOTES > Chapter 2 Footnotes · `samarangana-00058`

> रतिक्रीडापरा नार्यो नायकस्तु यदृच्छया। आपाण्डुदेहच्छवयः स्वल्पचारुविभूषणाः ।।३३॥ Variegated normed sprouted creepers deserve to be painted on the walls interior as well as exterior. Swans, ducks,2 and ruddy geese, possessing lotus petals and stalks, accompanied by lads playing along, having lovely arms, are introduced within the pleasure chamber clad in costumes and of variegated ornaments, the ladies engaged in love sports and a Hero, in voluntary mood, having, grace of the …
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 33: The Equery of Steeds (and Chapter 34: Practicable and impracticable materials) · `samarangana-00511`

> Chapter 35 occurs as Chapter 20 in Dr. D.N. Shukla's text, pp. 81-83 and 85-88. 2. Matsya Purāņa says the rite of Bali-puja before the construction वास्तूपशमनं कुर्यात्समिद्भिर्बलिकर्मणा। जीर्णोद्धारे तथोद्याने तथा गृहनिवेशने। वास्तूपशमनं कुर्यात्पूर्वमेव विचक्षणः । एकाशीतिपदं लिख्य वास्तुमध्ये च पृष्ठतः॥ होमस्त्रिमण्डले कार्यः कुण्डे हस्तप्रमाणके। यवैः कृष्णतिलैस्तद्वत्समिद्भिः क्षीरवृक्षजैः॥ पालाशैः खादिरैश्चापि मधुसर्पिः समन्वितैः । कुशदूर्वामयैर्वापि मधुसर्पिः समन्वितैः।।…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 35: The Rite named the laying of Foundation Stones · `samarangana-00527`

### C1.3 — vidisha, district, india, village, temple

> 2100 years later, suddenly coming to Vidisha, Heliodorus is dumbfounded... His joy is [there], but his sorrow is more than his joy. The joy is that in the memories of Vidisha he is preserved to this day — otherwise the Taxila, in the capacity of whose ambassador he had come here, there no one is left to take its name. That Taxila, lost somewhere in the ruins near Rawalpindi, is now not even a part of that India. He loves Vidisha, because in Vidisha's memory he is Khamba Baba.…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00215`

> This part of Madhya Pradesh is historically the most significant area in Central India. It is home to Bhimbetka and Sanchi, both of which are UNESCO-recognised world heritage monuments. Looking at the unique history of Vidisha from the time of Buddha and Ashoka, this area has an immense archaeological treasure.
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 150 · `intach-geoheritage-00469`

> has passed; may the children's tomorrow be set right." Life entangled in the everyday needs. Whether it is Vidisha or Mathura — what difference does it make? Heliodorus is amazed. While going inside, Heliodorus stands, halted, at the Raisen Gate... He is looking at the badly-scraped images. On one side someone has smeared green colour and tied cloths. This is the introduction of Islam — a new introduction for Heliodorus. Before coming to Vidisha he had heard this name in Taxi…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00218`

> 1) https://vidisha.nic.in/en/ 2) https://www.cambridge.org/core/terms The town of Udaypur in Vidisha district has very rich pre-medieval culture 3) https://villageinfo.in/Madhya-pradesh/vidisha/basoda/Udaypur.html 4) https://www.researchgate.net/publications/347842644_Study_On_the_Sanchi_Stupa_Ruins. 5) https://villageinfo.in/madhya-pradesh/vidisha/basoda/Udaypur.html 6) https://www.cambridge.org/core/terms 7) Mitra, S. (2022). Livelihoods, Mobility, and Housing: In Search of…
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 183 · `intach-geoheritage-00546`

### C1.2 — iast, purāṇa, aura, śiva, haiṃ

> *[IAST] śṛṃgāramaṃjarīkathā meṃ ina snehī rājāoṃ (praṇayibhiḥ nṛpatibhiḥ) kī bhojagoṣṭhī meṃ bhī upasthiti batāyī gayī hai| saikar̤oṃ rājā usake adhīna the| yaha bhoja kī racanāoṃ se jñāta hotā hai| spaṣṭa hī ve racanāe~ isa samarāṃgaṇasūtradhāra se bāda kī haiṃ| vaise vidiśā se bhopāla kṣetra meṃ bārahavīṃ śatī meṃ 'mahādvādaśakamaṇḍala' thā| parantu vaha eka hī maṇḍala kā nāma thā| dhāra jile kā baramaṇḍala kasbā bhī aise hī prācīna maṇḍala kā nāmāvaśeṣa pratīta hotā hai| a…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 4 · `bhojdev-hi-00020`

> The round Garbhagṛha is the general form in the indigenous temples and also occurs in Śiva temples, at Malabar. Gopinatha Rao op. cit., Pt. II. I. p. 91, note however says that the central shrines of all Śiva temples are square in shape. $^{53}$ The term cube is used here to designate a 4-sided prism approximating the shape of a cube. The Buddhist Temple No. 17, Sāñcī; Viṣṇu Temple at Eran, near Bhilsa (Percy Brown, op. cit., Pl. XXXIV). Kaṅkālī Devi Temple at Tigawa, C. P. T…
> — **KRAM-1** · *The Hindu Temple, Volume I* · p. 161 · `kramrisch-1946-v1-00816`

> Vasiṣṭha: Br. S. Comm.; 'Agni Purāṇa'; 'Devī Purāṇa', LXXII. 1-4. Viśvakarman: 'Bṛhat Saṃhitā', 'Agni Purāṇa'. Maya: 'Bṛhat Saṃhitā'; 'Īśānaśivagurudevapaddhati'. Nārada: 'Agni Purāṇa'; 'Mānasāra'. Nagnajit: 'Bṛhat Saṃhitā'; 'Citralakṣaṇa'. Nandiśa (Nandin): Br. S. Comm.
> — **KRAM-2** · *The Hindu Temple, Volume II* · p. 138 · `kramrisch-1946-v2-00707`

> $^{26}$ This story is told in other versions in the 'Viṣṇu Purāṇa', I. Ch. XIII. and in other Purāṇas. $^{27}$ S. B. VII. 4. 2. 6-7. Earth, the wide, the broad one, is Pṛthivī; Earth, as substance, is Bhū; Earth, as ground, is Bhūmi. $^{28}$ In the last verse of the Vanaparva, LXXXI, of the 'Mahābhārata', the sacred site of Kuruṣetra is known as the Uttara Vedi of Brahmā (p. 4). Its four corners bear the names of the resident Yakṣas, Ratna, and so on. The Yakṣas are held to b…
> — **KRAM-1** · *The Hindu Temple, Volume I* · p. 24 · `kramrisch-1946-v1-00091`

### C1.4 — temple, town, architecture, vidisha, king

> Proximity to the fertile Gangetic plains made the region about Bhilsa prosperous—a fact reflected in the richness of its monuments, second to none in Madhya Bharat. In ancient geography, it was called Dasharna, known from the days of the Buddha to those of Kalidasa (c. 5th century A.D.). The name lives on in the modern Dhasan river. In late historical times, it came to be known as part of Gondwana, ruled by the Gonds. Ancient Vidisha and its successor Bhilsa have always been …
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00016`

> In the 2nd century B.C., the Shungas supplanted the Mauryas. Pushyamitra Shunga's son, Crown Prince Agnimitra, ruled as Viceroy at Vidisha, an event immortalized in Kalidasa's *Malavikagnimitra*. The Shunga hold over Vidisha is verified by the famous Besnagar column inscription of Heliodoros, an ambassador sent by the Indo-Greek King Antialcidas of Taxila to the court of King Bhagabhadra. Heliodoros converted to the Bhagavata sect and erected the *Garudadhvaja* pillar in hono…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00024`

> The physical site of ancient **Vidisha**, situated in the fork of the Betwa (*Vetravati*) and Bes rivers. It was a major trading capital from the time of the Buddha down to the Guptas. Its mounds have yielded premier free-standing colossal sculptures: three *Yakshinis*, a colossal structural figure of *Kubera*, and early Gupta images of Durga and Vishnu. Its central monument is the **Heliodoros Pillar**, a free-standing monolithic stone column known locally as *Khamb Baba*. T…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00082`

> But that inscription of Heliodorus can still be read on that pillar today. Returning from Vidisha, I wrote this memorable heritage walk of a whole tiring day in an altogether different way. On my page, the title of this post of 20 January 2021 was — "The Return of Heliodorus in Vidisha."
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00214`

### C1.1 — excellent, devas, lord, linga, will

> The mode of expiation for those who slay persons having Skanda Purina trust in them, is known from Puranas and different Agamas indeed: uThe sin of Brahmana-slaughter perishes through a horse-sacrifice or if the sinner sits in the same posture (Ekdsya1) or in the same seat continuously for twelve years. But many living beings were ruthlessly killed by me again and again— persons having full trust in me, erring ones and those in the wombs. Women, old men and boys were repeated…
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 103 · `skanda-xiii-00207`

> In the meantime, О goddess, accompanied by you, I came here to see my own city. I was surrounded by the multitudes of Bhutas. Thereupon all these too came: All the groups of Devas, Kinnaras, great Serpents, Yak$as, Rak$asas and Gandharvas, Siddhas, Vidyadharas, Uragas (reptiles, serpents), Bhutas, Pretas, Pisacas, all the other beings moving in the sky, the four oceans, the salt sea, the milk-ocean and other oceans, Ganga, Yamuna, Sindhu, Candrabhaga, Sarasvati, Carmanvad, Bh…
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 278 · `skanda-xiii-00586`

> Heliodorus quietly set off toward the banks of the Vetravati... Nothing around is known or recognized. For a moment he feels that the other name of a directionless and distraught crowd is India itself. This is not that India. This is not that Vidisha either. He crossed the river and went far off, and stands before a rock. Something recognized has appeared. Recognizing Vishnu on that vast rock, he felt some relief. Vishnu stands, in his majestic posture, hand on hip, splendidl…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00222`

> The deity is well-known in all the three worlds by the name Gahgesvara because he was propitiated by Ganga and is the bestower of the benefit desired. At that time Ganga, the divine river, was eulogized by Devas, Gandharvas, by Valakhilyas and other sages and saints joyously. 31-41. Samudra came there and that great river was honoured. Ganga was told by the Linga: “May a sixteenth fraction (of Ganga) stay here near the Linga that is highly meritorious, as long as the earth st…
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 147 · `skanda-xiii-00301`

### C1.5 — rājā, iast, aura, gayī, apane

> विदिशा से लौटकर मैंने एक थका देने वाले दिन भर की इस यादगार हैरिटेज वॉक को बिल्कुल ही अलग ढंग से लिखा। मेरे पेज पर 20 जनवरी 2021 की इस पोस्ट का शीर्षक था-"विदिशा में हेलिओडोरस की वापसी।" 2100 साल बाद अचानक विदिशा आकर हेलिओडोरस हक्का-बक्का है... उसे खुशी जितनी है, उससे ज्यादा गम है। खुशी यह कि विदिशा की स्मृतियों में वह आज तक सहेजा हुआ है वरना जिस तक्षशिला के राजदूत की हैसियत से वह यहां आया था, वहां कोई नामलेवा नहीं बचा। रावलपिंडी के पास कहीं खंडहरों में गुम वह तक्षशिला ही अब उ…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00200`

> मेरी राय में यहां जनहित में चेतावनी का एक साइनबोर्ड बाहर ही लगाया जाना चाहिए कि कमजोर दिल के इंसान इस स्मारक को देखने अपने जोखिम पर ही जाएं। यहां के दृश्य आपको विचलित कर सकते हैं! विजय मंदिर के बाद हम पुराने विदिशा की गलियों में घूमे, जिसे किले अंदर कहा जाता है। हालांकि वहां अब किसी किले का नामोनिशान नहीं है। लेकिन आबादी के दबाव के बीच कहीं से भी झांकिए किले की गुमशुदा दीवार और किले के भीतर पुरानी इमारतों के बचे खूचे नामोनिशान बस आखिरी सांसें लेते हुए कसमसाते नजर आएंगे। रायसे…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00199`

> आज हेलियोडोरस एक बार फिर अपने प्रिय नगर में लौटा है... लेकिन वो विदिशा कहाँ है? सदियों के थपेड़ों के निशान इस पुराने शहर के चेहरे पर कितने गहरे हैं। थका हुआ सा, हैरान-परेशान, दौड़ता-भागता सा, एक किस्म की दिशाहीनता, अवसाद, धूमिल आकांक्षाओं का एक ऐसा शहर, जो अपनी लंबी आयु में तरह-तरह के तजुर्बों से होकर गुजरा हो और अब उदासीनता में दिन काट रहा है। ऐसे उपेक्षित बूढ़े आदमी की तरह, जिसे इस्तेमाल करके घर के उजाड़ कोने में बैठा दिया गया हो। उसे जिंदगी के शानदार और सम्मानित दौर रह-रहक…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00201`

> हेलियोडोरस को बेसनगर के उस भव्य समारोह की याद आई... जब उसने वैष्णव धर्म की दीक्षा ली थी। विदिशा की वह वैभव से भरी शांति भंग हो चुकी है। यूँ बेलगाँव भीड़ से भरे बाजारों में आधुनिकता की चमकदमक है, लेकिन वह फीकी है। कुहासे से रोशनी के संघर्ष जैसी। कुहासा सदियों का है। गहरा और पुराना। वह सिर्फ नजरों में नहीं है। वह सोच में भी गहरा उतरा हुआ है। गांवों से अच्छे दिनों की आस में आए लोगों की आंखों में कोई आशा है, जो शेष है। हमारी
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00202`

**Gaps.** barely represented here: `BET-S`, `PAR`, `SIN-S`, `SIN-T`.

## C2 — The Betwa Valley: Land, Rivers and Seasons

[↑ contents](#contents)

**Coverage.** 1,330 chunks from 25 sources (`ADH`, `BET-K`, `BET-S`, `BHJ-H`, `DEV`, `GAN`, `GAZ-VID`, `GUP`, `HAR`, `INT-ARC`, `INT-GEO`, `KRAM-1`, `KRAM-2`, `PAN`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `RAJM`, `SAM`, `SIN-B`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: primary_authorial_paramara 567, secondary_core 255, field_observation_survey 97, environmental_scientific 93, secondary_comparative 91, reference_tertiary 88, primary_scriptural 78, field_observation_reportage 38, primary_epigraphic 18, contextual_thematic 5. The largest single contributor is `SAM` with 566 chunks (43% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- Furthermore, the mean Indian Summer Monsoon Rainfall (ISMR) over Central India has declined by 10–20% from 1950–2015 [7,8]. — `BET-K` `[single-source]`
- Study Area* The Betwa River originates from Raisen district of Madhya Pradesh and joins the Yamuna River in Hamirpur district of Uttar Pradesh, India. — `BET-K` `[single-source]`
- We observed that before the year 2000, the driest (SPI = −1.2) year was 1981, and the wettest (SPI = 1.9) year was 1999. — `BET-K` `[single-source]`
- In the north of Nila mountain and to the south of Śveta mountain, the fifth varșa, highly gorgeous, is known as Ramyaka [cite: 857, 861, 863]. — `SAM` `[single-source]`
- Heat map illustrates the projected change in mean monsoon streamflow and rainfall of Upper Betwa River during (a) 2023–2060 and (b) 2061–2100 with respect to 1982–2020.]* — `BET-K` `[single-source]`
- In Kuru varșa, the men and women subsist upon wish-fulfilling trees that shower fruits cherished by them [cite: 925]; they live twelve and a half thousand years, bearing white complexions like the gods' progenies [cite: 926, 928]. — `SAM` `[single-source]`
- Nayak [6] noticed that in Central India, open forest and vegetation cover has diminished by 0.7% and 0.3% however, agricultural land has increased by 0.5% during 1981–2006. — `BET-K` `[single-source]`
- Betwa Basin is located in Central India and lies between 77°10'E and 80°20'E (longitude) and 22°54' and 26°05'N (latitude) (Fig. 1). — `BET-S` `[single-source]`
- Amidst the eastern part of the Vindhyachal range is located a village named Udaypur with a total geographical area of 1966 hectares/ 19.66 Square Kilometers (km2). — `INT-ARC` `[single-source]`
- The cumulative rainfall during the Indian summer monsoon shows a declining trend of 2 mm from 1980–2020 (Figure 6). — `BET-K` `[single-source]`
- In the forepart of the Malyavān mountain are Nīla and Nișadha in between [cite: 868]: Bhadrāśva varșa, the eighth one, stands stretched upto the ends of the eastern ocean [cite: 871]. — `SAM` `[single-source]`
- The total area of the basin is about 43,500 km² and the total length of the river from its origin to its confluence with the Yamuna River is 590 km, out of which 232 km lies in Madhya Pradesh and the rest 358 km in Uttar Pradesh. — `BET-S` `[single-source]`
- In between the Hemakūta and Nişadha mountains, "Harivarsa" is proclaimed as the third varșa, the best one [cite: 853, 856]. — `SAM` `[single-source]`
- To the west of Gandhamādana mountain and to the east of the western ocean, the Ācāryas call as Ketumāla, the ninth varșa [cite: 872, 873]. — `SAM` `[single-source]`
- We used the in-situ measured streamflow of the Betwa River at Kurwai gauging site for the model calibration and validation using the SWAT Calibration Uncertainty Program (SWAT-CUP). — `BET-K` `[single-source]`
- Their age is ten thousand autumns (*Śarads*), and they feed on *Panasa* (breadfruit) [cite: 915, 917]. — `SAM` `[single-source]`
- The daily mean temperature ranges from a maximum of 42.3 °C to a minimum of 8.1 °C. The daily mean relative humidity varies from a minimum of 18 % (April and May) to a maximum of 90 % (August). — `BET-S` `[single-source]`
- The maximum and minimum streamflow during 1982–2000 is 1079 and 139 m³s⁻¹, which has decreased during 2001–2020 to 673 and 127 m³s⁻¹ respectively. — `BET-K` `[single-source]`
- Barely represented in this bucket, so anything resting on them is a thin reed: `RAJM` — `[gap]`

### C2.1 — having, created, deserves, create, norm

> ग्रीष्मर्तो सप्तमं भागं शीतकाले च पञ्चमम्।।५।। Of the rice grains with husk² the proportion deserves to be mixed up the way it has been prescribed. In the summer season seventh part and in the winter season fifth part. षष्ठं शरदि वर्षासु चतुर्थ भागमानयेत्। वर्तिकाबन्धनार्था (दार्च) मायान्ति तेन ता (:) ।।६।। The sixth part in Autumn and in the rains one may bring fourth part.³ For the preparation of the brush they attain to hardness. (अग्राया शालिवक्क्राभा यवं यव्यां सुखगृहम्।…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra > Architectural Treatise of Mahārājādhirāja Śrī Bhojadeva > [Original Page Source: 14] · `samarangana-01381`

> वर्षाकाले हि भागेन प्रदद्यादिति निश्चयः। पञ्चभागप्रमाणेन ग्रीष्मसं + + + + + + + + + + + + + + ।।२१।। In rainy season by a part alone one may provide, this is the factual norm. By the extent of 5 parts one may take to the development in summer. (बन्धानेन च प्रकुर्वीत पूर्वोक्तर्विधानाक्षितो ?)। लेपयेद् रोमकूर्चेण शुष्कां शुष्कामनुक्रमात् ॥२२॥ In the preparation of the paste one may act the way it has been told above and may glue with a hair brush getting dried up in due order…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra > Architectural Treatise of Mahārājādhirāja Śrī Bhojadeva > [Original Page Source: 14] · `samarangana-01384`

> 2. A hold of the size of nişpāva or black grains and blue in colour was called कोलाक्षा 3. Śūkara nayana was uneven, colourless and extends over 11 joints. 4. Vatsanābha devoted of a breach covering one point. 5. Kālaka the black hole. 6. Dhundhuka also dark and cut. 7. But a hole of the same colour as wood was not deemed as inauspicious. पातितान् वर्जयेद् वृक्षान् द्विपाश्वाग्निजलानिलैः। प्रभूतपक्षिनिलयान् काककौशिकसेवितान्।। ११२।। One may evade the trees felled by elephants,…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 47: The pre-requisites of a Vedi · `samarangana-00694`

> CHAPTER 73 Lepyakarma and the like (moulding, modelling, making models)¹ or plastering लेप्यकर्म समुल्लक्ष्य (लेखा?) लक्ष्म च कथ्यते। वापीकूपतटाकानि पद्मिन्यो दीर्घिकास्तथा ।।१।। The Lepyakarma (plastering) along with the marks of clay and the marks of lining are being illustrated. The oblong tanks, the wells, the ponds and the like, the lotus lakes and the puddles, likewise. वृक्षमूलं नदीतीरं गुल्ममध्यं तथैव च। मृत्तिकानामिति क्षेत्राण्युक्तान्येतानि तत्त्वतः।।२।। The root o…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra > Architectural Treatise of Mahārājādhirāja Śrī Bhojadeva > [Original Page Source: 14] · `samarangana-01390`

### C2.6 — rainfall, betwa, temperature, monsoon, trend

> The climate of Vidisha is characterized by a hot summer and generally dry rains, except during the southwest monsoon season. It can be estimated that the average annual rainfall of Udaypur village is around 800 mm, which is the same as the average rainfall of the agro-climatic. The rainfall distribution is uneven and erratic, and the area often faces droughts and floods. The rainfall is influenced by the south-west monsoon winds, which bring moisture from the Arabian Sea and …
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 23 · `intach-geoheritage-00137`

> Vidisha is on the Vindhyanchal plateau, which has a number of spurs that point to the north and northeast. Vidisha district forms part of the Malwa plateau and the Vindhya hill range with undulating topography. The district is primarily an agricultural district occupying the Betwa Basin valley, having a predominantly agricultural economy.
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 21 · `intach-geoheritage-00134`

> 1. Collapsed bastions and pitching: There is an immediate need for urgent short-term action to repair the collapsed bastions and pitching and to strengthen the surrounding walls as a safeguard against the progressive collapse of vulnerable adjacent structures. 2. Effects of the monsoon: Special precautions need to be taken to prepare for the upcoming monsoon. Work that has begun to clean the mori and drainage channels must be continued so that all outlets are opened to ensure…
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 101 · `intach-geoheritage-00350`

> *2.1. Study Area* The Betwa River originates from Raisen district of Madhya Pradesh and joins the Yamuna River in Hamirpur district of Uttar Pradesh, India. The upstream of this river is largely intermittent and becomes perennial in the downstream (85 km) before its confluence to the Yamuna River [21]. We have selected the upper reach of the Betwa River to conduct this study. The Upper Betwa flows through a single thread channel having a total length of 127 km and a catchment…
> — **BET-K** · *Streamflow of the Betwa River under the Combined Effect of LU-LC and Climate Change* · p. 2 · `kumar-2023-betwa-00009`

### C2.3 — lord, devas, after, great, will

> 146 HISTORY OF THE PARAMARA DYNASTY elephants rested after the fatigue of the battle, bathing in the waters of the river. Lakşmadeva is reported to have come into conflict with the armies of Anga and Kalinga. Verse 43 of the Nagpur inscription records that "even the troops of elephants of Anga and Kalinga, kindred to the elephants of the quarters, and bulky like mountains set in motion by the storm at the destruction of the universe, and rivalling rain-clouds, dark like herds…
> — **GAN** · *History of the Paramāra Dynasty* · p. 60 · `ganguly-paramara-00313`

> PARAMARA MAHAKUMARAS Vindhya. An inscription of his reign has been discovered. In Sam. $1200=1144$ A. D., on the occasion of the eclipse of the moon, he re-affirmed the grant made by Yasovarman in Sam. 1191, with a view to increasing the religious merit of his father. Of the localities mentioned in the record, the village Vadauda may be identical with Vadauda of the Man2 dhata plate of Jayavarman II, where it is described as a village in Mahaudapathaka. Professor Kielhorn is …
> — **GAN** · *History of the Paramāra Dynasty* · p. 99 · `ganguly-paramara-00396`

> V.ii.23.11-20 О great goddess, Yoga and Ksema (acquisition and security of things acquired), and good rainfall have kings as their cause. The subjects, pestilences, death, fears, Krtayuga, Treta, Dvapara, and Kaliyuga—all these have kings at their root. A king is the basic cause of Dharma, О Parvatl. Once in this world there was a king named Madandha. He was wicked and egotistic. He was a thorn unto Devas and Brahmanas. He ruled during the period of transition between Dvapara…
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 75 · `skanda-xiii-00146`

> Before this can be done the fitness of the soil has to be ascertained by several tests. A pit is dug and the earth which has been taken out is put back again. In a descending degree of its quality, it then either exceeds the pit in quantity, is level with it or lower; or, water is put into the pit over night: the quality of the soil is judged according to the quantity of the water found there in the morning; or, a flame put into the pit burns, or else is extinguished, in the …
> — **KRAM-1** · *The Hindu Temple, Volume I* · p. 25 · `kramrisch-1946-v1-00093`

### C2.2 — cite, english, sanskrit, translation, śloka

> Proximity to the fertile Gangetic plains made the region about Bhilsa prosperous—a fact reflected in the richness of its monuments, second to none in Madhya Bharat. In ancient geography, it was called Dasharna, known from the days of the Buddha to those of Kalidasa (c. 5th century A.D.). The name lives on in the modern Dhasan river. In late historical times, it came to be known as part of Gondwana, ruled by the Gonds. Ancient Vidisha and its successor Bhilsa have always been …
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00016`

> The physical features of this land are characterized by the three river systems of the Chambal, Betwa, and Narmada, and by the mountain systems of the Vindhyas and the Satpuras. These features divide the State into five natural divisions: 1. **The Northern Madhya Bharat (Gwalior, Morena, Bhind, Shivapuri, and Guna districts):** Most of it is hilly and mountainous due to the northern offshoots of the Vindhyas encroaching upon it, leaving a small flat low-lying tip at the north…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00015`

> Situated picturesquely on the bank of the Hathni stream, facing east. * **Structure:** A five-storeyed (*pañcabhūma*) *pañcaratha* circular-stellate structural temple. The *vedībandha* preserves a complete sequence of moldings: *khuraka*, *kumbha*, *antarapatta*, *cippika*, *kalaśa*, *antarapatta*, and *kapotapālikā*. The *shikhara* retains its side quadrants, showing three vertical rows of five *kūṭastambhas* each, though the crowning *amalaka* is missing. The floor of the s…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00105`

> The entire District lies in the drainage basin of the Yamuna. The general slope is from south to north. * **The Betwa (Betrawati):** Rises in the extreme south-west of Raisen district. It enters Vidisha 6 km south of the town and flows for about 112 km within the district. Significant western tributaries include the Besh, Bah, Sagar, and Kethan; eastern tributaries include Nion, Parasri, and Bina. * **The Bes (Besh / Halali):** Rises near Parawalia in Sehore district, flows n…
> — **GAZ-VID** · *Madhya Pradesh District Gazetteers: Vidisha* · p. — · `vidisha-gazetteer-1979-00022`

### C2.4 — temple, hands, right, left, śiva

> Another datable source is an inscription from Holal, Bellary District.$^{92}$ This Western Cālukyan inscription speaks of 4 types of buildings, called Nāgara, Kāliṅga, Drāviḍa and Vesara. These three sources belong to the Deccan and the South. A South Indian Āgama further clarifies the designations by explicit definitions. In chapter XLIX, 1-2, the 'Kāmikāgama' assigns the Nāgara temples to the country from the Himālaya to the Vindhya; Vesara from the Vindhya to the river Kṛṣ…
> — **KRAM-1** · *The Hindu Temple, Volume I* · p. 302 · `kramrisch-1946-v1-01571`

> Following the 'Īśānaśivagurudevapaddhati' III. ch. XXX, 41 f., the 'diminutive temple' (Kṣudra-alpa Vimāna), the High Temple, of the type Nāgara is square or rectangular, its quality is 'sāttvika', its locality is the country between the Himālayas and Vindhya hills; Drāviḍa is 'rājasa'; the Drāviḍa country and none else is suitable for the chapel-type Drāviḍa. This is described as six sided or eight sided, of even sides, a regular octagon, etc., or an oblong octagon, or the s…
> — **KRAM-1** · *The Hindu Temple, Volume I* · p. 308 · `kramrisch-1946-v1-01613`

> 1) https://vidisha.nic.in/en/ 2) https://www.cambridge.org/core/terms The town of Udaypur in Vidisha district has very rich pre-medieval culture 3) https://villageinfo.in/Madhya-pradesh/vidisha/basoda/Udaypur.html 4) https://www.researchgate.net/publications/347842644_Study_On_the_Sanchi_Stupa_Ruins. 5) https://villageinfo.in/madhya-pradesh/vidisha/basoda/Udaypur.html 6) https://www.cambridge.org/core/terms 7) Mitra, S. (2022). Livelihoods, Mobility, and Housing: In Search of…
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 183 · `intach-geoheritage-00546`

> Our knowledge of the names of all the units of the kingdom is by no means exhaustible, being limited in fact to the following, collected from the available records. 1. Avanti. 2. Mahadvâdaśaka 3. Nilagiri. 4. Pûrņapathaka. 7. Vindhya. 8. Vyapura. 9. Upendrapura. 10, Selluka. 5. Samgamakheța, 11. Uparahada. 6. Sthalî. 1. Gardabhapânîya. 2. Ghaghradora (in the Sthalî mandala). 3. Rajaśayana (,, Mahadvadaśaka mandala). 1. Audrahadi in Selluka (containing 1500 villages). 2. Mohad…
> — **GAN** · *History of the Paramāra Dynasty* · p. 102 · `ganguly-paramara-00513`

### C2.5 — iast, aura, haiṃ, tathā, para

> *[IAST] 146 ityamī kathitāḥ samyag ye yathādiṅmukhāḥ surāḥ |* दिक्षु दिक्षु बहिर्ये स्युस्तानिदानीं प्रचक्ष्महे ॥114 *[IAST] dikṣu dikṣu bahirye syustānidānīṃ pracakṣmahe ||114* 147 विष्णोर्दिनाधिनाथस्य सहस्रनयनस्य च । *[IAST] 147 viṣṇordinādhināthasya sahasranayanasya ca |* धर्मस्य च विधातव्यं दिशि प्राच्यां निकेतनम् ॥115 *[IAST] dharmasya ca vidhātavyaṃ diśi prācyāṃ niketanam ||115* 147 सनत्कुमारसावित्र्योर्मरुतां मारुतस्य च । *[IAST] 147 sanatkumārasāvitryormarutāṃ mārutas…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 41 · `bhojdev-hi-00162`

> 15-12 *[IAST] prasiddha śāstroṃ aura dṛṣṭāntoṃ se vāstujñāna prāpta kareṃ| vāstu kī nāliyoṃ, bā~soṃ, niścita marmavedha dvārā vāstu, dvāra ādi saba śāstroṃ se jāna letā hai| jo śāstra ko jāne binā prayoktā sthapati (kārīgara) bana jātā hai use rājā svayaṃ hī māra ḍāleṃ| kyoṃki vaha rājahiṃsaka (sākṣāt) mṛtyu jaisā hai| jisane śāstra par̤hane meṃ śrama nahīṃ kiyā aura mithyā-jñāna se ahaṃkārī hai vaha to dharā para loka kā akāla-mṛtyu (banakara) ghūmatā hai| jo kevala śāstra j…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 95 · `bhojdev-hi-00426`

> 18 *[IAST] āśreṇīpuruṣā śakyasāmantā devamātṛkā || 18* 11 धान्या हस्तिवनोपेता सुरक्षा चेति षोडश । *[IAST] 11 dhānyā hastivanopetā surakṣā ceti ṣoḍaśa |* भुवः संज्ञाभिरुद्दिष्टा लक्ष्मासामथ कथ्यते ॥ 19 *[IAST] bhuvaḥ saṃjñābhiruddiṣṭā lakṣmāsāmatha kathyate || 19* ● ● 12 धातुस्यन्दोल्लसत्कुञ्जगुल्मदुमलतावृतैः । *[IAST] 12 dhātusyandollasatkuñjagulmadumalatāvṛtaiḥ |* उत्सङ्गिताः पृथुशिलैः समन्तादवनिधरैः ॥ 127 *[IAST] utsaṅgitāḥ pṛthuśilaiḥ samantādavanidharaiḥ || 127* 13 तीर्था…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 26 · `bhojdev-hi-00121`

> 191 काष्ठकैर्यत्र रचितं स्थूणयोरधिरोहणम् । *[IAST] 191 kāṣṭhakairyatra racitaṃ sthūṇayoradhirohaṇam |* सा निःश्रेणिरिति प्रोक्ता सोपानैर्विपुलैः पदैः ॥११ *[IAST] sā niḥśreṇiriti proktā sopānairvipulaiḥ padaiḥ ||11* 192 स्मृतः काष्ठविटङ्कोऽसौ यत् काष्ठैः संवृतं गृहम् । *[IAST] 192 smṛtaḥ kāṣṭhaviṭaṅko'sau yat kāṣṭhaiḥ saṃvṛtaṃ gṛham |* सुधालिप्तलं हर्म्यं सौधं स्यात् कुट्टिमं च तत् ॥१२ *[IAST] sudhāliptalaṃ harmyaṃ saudhaṃ syāt kuṭṭimaṃ ca tat ||12* 193 वर्षाभयेन या छन्ना ताल-…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 58 · `bhojdev-hi-00265`

**Gaps.** barely represented here: `RAJM`.

## C3 — Stones and Forests: Geology, Flora and Fauna

[↑ contents](#contents)

**Coverage.** 1,715 chunks from 24 sources (`ADH`, `BHJ-H`, `DEV`, `GAN`, `GAZ-VID`, `GUP`, `HAR`, `INT-ARC`, `INT-GEO`, `KRAM-1`, `KRAM-2`, `PAN`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `RAJM`, `SAM`, `SIN-B`, `SIN-S`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: primary_authorial_paramara 619, secondary_core 260, field_observation_survey 259, secondary_comparative 197, reference_tertiary 142, field_observation_reportage 137, primary_scriptural 55, primary_epigraphic 34, contextual_thematic 12. The largest single contributor is `SAM` with 619 chunks (36% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- Image 123 Image showing Cave I Image 124 Interiors of the Cave I Bat guano Depth- 400 mm Cave dimensions- Inner Height- 5.14 meters Entrance Width- 2.25 mtrs. — `INT-GEO` `[single-source]`
- Notable structural remains include the rock-cut Chaturbhuja temple (875 A.D.) at Gwalior Fort and Krishna temple pillar at Pathari (861 A.D.), totaling 87 shrines across the territory. — `PAT-INS` · `PAT-TEM` `[established]`
- Udaypur village produces Soybean, Pigeon pea, and Maize in Kharif and Wheat, Gram, and Lentil in Rabi season. — `INT-GEO` `[single-source]`
- The Upper Rewa Sandstone Formation of the Rewa Group in the Vindhyan basin is composed mainly of medium- to very fine-grained, iron-pigmented arenaceous rocks, which are variously interpreted as fluvial, marine, or continental deposits. — `INT-GEO` `[single-source]`
- Contemporary Sanskrit inscriptions on its porches record that it was founded by the Paramara King **Udayaditya**; construction commenced in **1059 A.D.** (*V.S. 1116*) and the flagstaff was hoisted in **1080 A.D.** (*V.S. 1137*). — `PAT-INS` `[single-source]`
- The Hill Fort in Udaypur has a massive boundary wall made of sandstone running along the periphery of the hill with a total length of about 1400 m. — `INT-GEO` `[single-source]`
- Image 122 Way on the hill towards the caves - Cave I - Cave II - Cave III - Cave IV — `INT-GEO` `[single-source]`
- Gateway to the Geo Heritage Reserve: Udaypur Hill Fort site already has a well-defined historical gate, existed there for more than 1000 years. — `INT-GEO` `[single-source]`
- The entry gate to the fortification complex is located at 463 meters above mean sea level, and it divides the fortification wall into two parts, the west side being about 810 meters, and the east side is about 600 meters. — `INT-GEO` `[single-source]`
- Waterymuhūrtta- Presided over by Varuņa, p.845, 869 (BS of Varahamihira) Samarangapa-sūtradhara Tula (Beam) having surface even as such projected as such gone into the central spot. — `SAM` `[single-source]`
- Geological Formations- Understanding the composition, structure, and evolution of Udaypur's rock formations, including its butte and mesa landforms, caves, and sedimentary layers. — `INT-GEO` `[single-source]`
- He is a good knower of wildlife too, along with history — because between 1960 and 1997, during the teaching of history in colleges, between 1983 and '86 he was an Interpretation Officer at Kanha National Park. — `TIW-E` `[single-source]`
- Image 116 Showing Butte Formation The dis set are per of roy est the rel di ric m w C v: re b b d I g r a F Image 117 Showing Butte from lower hill. — `INT-GEO` `[single-source]`
- Image 5 Diagram explaining formation chart of Mesa-Butte-Pinnacle — `INT-GEO` `[single-source]`
- Udayaditya (1058–1087 A.D.) restored family fortunes and built the spectacular Nilakanteshvar temple at Udaypur. — `PAT-INS` `[single-source]`
- The petroglyph of Lajja Gowri- The other most significant finding is the petroglyphs of relatively Lajja Gori, probably the largest one anywhere in India. — `INT-GEO` `[single-source]`
- Natural Rock Arch: (THE THIRD EYE)- Natural arches are formed in sandstone by a combination of erosion and stress. — `INT-GEO` `[single-source]`
- And with peaks made of Hema (i.e. gold), Hemakūța, this one was known as the mountain [cite: 827], to which serve perennially or to which keep occupied perennially Cāraṇas (heavenly charioteers⁶) and Guhyakas [cite: 828, 830]. — `SAM` `[single-source]`
- Barely represented in this bucket, so anything resting on them is a thin reed: `RAJM` — `[gap]`

### C3.1 — having, created, deserves, create, norm

> **English Translation:** *By a single part its upper part, with the roof of the space of the caves on broad by six* parts and elevated by five parts. **Sanskrit (Śloka):** `शूरसेनं प्रकुर्वीत मध्यवर्तालितोरणम्।` **Sanskrit (Śloka):** `वराहग्रासमकरैर्वराहराजसुण्डकैः(:?)||१६३||` **English Translation:** *One may create Śūrasena having an arched portal existing within the central rows* having Rhinoceroses, elephants, boars, crocodiles and alligators and swans (painted) as such).…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 56: The Illustration of Sixty-Four Prāsādas Headed by Rucaka > 4. Deity Placement and Architectural Vulnerabilities (*Marmavedha*) > Avoiding Vulnerable · `samarangana-00899`

> आरण्यैः शकुनैरेतत् स्याद् वर्षाद् धर्षणे फलम्। यूनां च जायते मृत्युर्मध्वासङ्गे धनक्षयः ।।१७।। By the (predominance) of sylvan birds spraying forth, within the span of one year, the demise of young people becomes the outcome or the loss of wealth by liquor addiction. दुःस्वप्नदर्शनं घूके बालानां मरणं तथा। त्रस्तभीते निलीने तु राजा शून्यं हरेद् गृहम् ।। १८ ।। An owl (appearing as such) results in the inception of bad dreams and the death of children. In the event of the lying …
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 41: Cayavidhih - The edifice laying · `samarangana-00611`

> By the torsos or trunks stationed within the vulnerable points, the body of the owner becomes compressed or tortured and by the Sandhipalas (The joint preservers) one may indicate the death of allies. गृहपीडा नागदन्तैर्नागपाशैर्धनक्षयः । कापिच्छकैस्तु प्रेष्याणां क्षयं मर्मस्थितैर्वदेत्।। १२० ।। By pegs' obstruction of vulnerable points there ensues trouble to the house, and by snake-snares, the loss of wealth and by Kapicchakas¹ entangling the vulnerable points result in the…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 47: The pre-requisites of a Vedi · `samarangana-00696`

> [paraphrase — not a verbatim quote; source text unreliable] As sole quarry of learning or knowledge, the way you are choosing us by way of help (i.e. helping hands), by that we do not deem ourselves as highly esteemed² or by that we are deeming ourselves as highly honoured. [cite: 408] तदिदानीं हितार्थे नः प्रजानामपि च प्रभो !। अप्रमेयप्रभावस्त्वं सर्वमाख्यातुमर्हसि ।। ३ ।। Therefore, now for the sake of well being of the subjects also of ours or descendants or progenies of ours. Aye Lord! you being one as having power of unmeasurable…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. SAMARĀNGANA-SŪTRADHĀRA > CHAPTER 2: The Conversation Between Viśvakarmā and His Sons (Mānasa Putras) > FOOTNOTES & TEXTUAL CRITICAL NOTES > Chapter 2 Footnotes · `samarangana-00053`

### C3.4 — temple, cave, temples, century, architecture

> A long sandstone hill containing **20 rock-cut caves** excavated during the Gupta period. * **Cave No. 1:** A Jain cave representing the earliest phase of structural Hindu-Jain temple evolution, consisting of a small rock-cut cell fronted by a structural porch on four columns. * **Cave No. 4:** Enshrines a *Shivalinga* and is called *Bina Cave* due to a porch relief of a man playing the lute (*veena*). * **Cave No. 5 (The Varaha Cave):** The premier artistic monument of the G…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00083`

> A series of **nine rock-cut Buddhist caves** excavated into a sandstone cliff on the Bagni river, serving as a Mahayana monastery from the 4th to 6th centuries A.D. * **Cave No. 2:** A large structural *vihara* consisting of a central pillared hall surrounded by 20 residential cells for monks, fronted by a portico; the rear sanctuary enshrine a stone *Stupa*. The central columns are massive, covered in spiral fluting. * **Cave No. 4 (Rang Mahal - Palace of Colours):** The lar…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00098`

> The primary resource quarry was **Chirakhan**, a rocky sandstone highland located directly north of Un. The name derives from local words meaning "stone cutting" (*chira*) and "quarry" (*khan*). Marks of medieval stone-splitting are still present on the rock surfaces. The quarry yields a coarse-grained sandstone of relatively low durability, explaining why the Un cluster suffered rapid structural decay compared to temples built with high-quality pink sandstone.
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00117`

> Image 129 Image showing Cave IV Jain Caves: Jain cave temples built from the 5th to 10th century CE exhibit the distinctive Jain style of sculpture and architecture belonging the Kankaliya caves and Udayagiri caves in Madhya Pradesh are known for their intricately carved Jain Tirthankaras.
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 140 · `intach-geoheritage-00424`

### C3.2 — hands, lotus, right, pose, sword

> ``` +----------------------------------------------------------------------------+ | CHRONOLOGICAL TIMELINE OF THE UN TEMPLE CLUSTER | +----------------------------------------------------------------------------+ | 1. Chaubara Dera No. 1 | c. 1000-1055 A.D. | Peak of King Bhoja's reign. | | | | Circular-stellate Bhumija. | +--------------------------+-------------------+-----------------------------+ | 2. Mahākāleśvara No. 2 | c. 1030-1060 A.D. | Built slightly later; matchi…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00119`

> | No. | Name Of The Structure | Unique ID | Category | Time Period (in A.D.) | Protection Status | Usage | Condition | Grade | GPS coordinates | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | 1 | Hill Fortress wall | UD/HIL/WA/01 | Monument(Wall) | 10th Century | Unprotected | Not in Use | Poor | I | 23.53.41.99 N and 78.3.23.63 E | | 2 | Jain Cave | UD/HIL/JC/02 | Religious(Jain Cave) | 6th Century | Unprotected | Not in Use | Moderate | II | 23.53.25.89 N a…
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 155 · `intach-geoheritage-00487` · also **INT-ARC** · `intach-2022-udaypur-00420`

> Saruftna, Kantfa Vydnda, Коротка, Smmsim, Mandalavafi. Nowhere does any bird has the skill of moving in the sky in the same way as I have, О my beloved. Take it easy. Why worry when I am alive and active, О my beloved?” 34-44a. On hearing his words, the chaste one kept mum like a dumb person. The next day also, the vulture came and sat on the rock as if he was very happy; he was a little away from the perching place of the birds. After sitting there an Ayama1 away from them, …
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 158 · `skanda-xiii-00324`

### C3.5 — udaipur, people, udaypur, history, udayaditya

> Udaypur is covered with 75% of black cotton soil. The other 25% is red-yellow mixed soils derived from the sandstone and shale; laterite, Vindhyan sandstones, Basalts, raw metals, and clay are also found. Udaypur village produces Soybean, Pigeon pea, and Maize in Kharif and Wheat, Gram, and Lentil in Rabi season. The Kharif area is 90% rainfed, and the Rabi area is 34% rainfed.
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 23 · `intach-geoheritage-00138`

> Udaypur is covered with 75% of black cotton soil. The other 25% is red-yellow mixed soils derived from the sandstone and shale, laterite, Vindhyan Sandstones, Basalts, raw metals and clay are also found. The district's forest forms part of Raisen Forest Division, which is further divided into two sub-divisions and four ranges. Sanchi and Sironj are the two sub divisions, whereas Gyaraspur, Shamshabad, Lateri, and Sironj are the four ranges. Udaypur is located in the Gyaraspur…
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 14 · `intach-2022-udaypur-00046`

> 5. To survey & measure all dimensions of all the unreported cave structures, such as the Jain Caves built on the vertical slopes of the hill, including the Saptamatrika sculpture on the upper hill. 6. To study the geographical formations on the slope of the hill with respect to the artifacts and their dimensions inside. 7. To document the flora and fauna of the Udaypur upper middle and the top hill. 8. To study the local history of the Pre-Parmar period in Udaypur, particular…
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 44 · `intach-geoheritage-00204`

> उदयपुर पत्थर की खदानों से मालामाल इलाका है। गोविंद सक्सेना की एक ग्राउंड रिपोर्ट ने बताया कि ढाई हजार हेक्टेयर से ज्यादा वन विभाग की जमीन पर नाजायज खदानें चल रही हैं, जिनमें से लाखों रुपए का पत्थर हर दिन निकाला जाता है। स्थानीय गांवों के लोग जिंदा रहने लायक दिहाड़ी पर मजदूरी के लिए लगाए जाते हैं। पत्थर के मालदार लुटेरे बेददी से खदानों में धमाके करते हैं। धरती के भीतर धमाकों को सुनकर उदयपुर अपने स्वर्णिम इतिहास को बगल में दबा डरकर और ज्यादा सहम जाता है। उसे आठ सदीयों पुराने धम…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00298`

### C3.3 — hill, udaypur, geological, sandstone, natural

> The lake near the stone quarry is a natural water body located to the southeast of the village of the Udaypur at GPS 23.53.29.4 N and 78.03.53.9 E. This is a large water reservoir on the site of a live stone quarry which is a threat to the ecology of the lake.
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 92 · `intach-2022-udaypur-00312`

> Most of it is hilly and mountainous due to the northern offshoots of the Vindhyas encroaching upon it but leaving a small flat low-lying tip at the north for the rivers to meet and join ultimately with the great river system of the Gangetic plain. In history, these physical aspects are very well reflected in the numerous forts and fortresses such as those of Gwalior, Narwar, Chanderi, and others, and in the numerous stone-built temples, materials for which were available read…
> — **PAT-CH** · *The Cultural Heritage of Madhya Bharat* · p. — · `patil-1952-00026` · also **PAT-TEM** · `patil-composite-temples-00026`

> [paraphrase — not a verbatim quote; source text unreliable] [cite: 2726, 2727, 2728] Mines and quarries extract minor minerals like clay, sandstone, murram, and *chhuimitti* [cite: 2749].
> — **GAZ-VID** · *Madhya Pradesh District Gazetteers: Vidisha* · p. — · `vidisha-gazetteer-1979-00121`

### C3.6 — iast, aura, haiṃ, tathā, para

> वाले बब्बा को याद कर लीजिए, कुछ नहीं होगा। ऐसा अटूट विश्वास है। गढ़ी की एक पुरानी चार फुट से ज्यादा चौड़ी दीवार पर पहुंचिए। सब कुछ घने जंगल में खोया है। जमीन पर इतनी घनी घास है कि कुछ नजर नहीं आता। गढ़ी की मजबूत प्राचीर कहीं-कहीं से झांकती है। कोई दरका हुआ सा बुर्ज, जाने कब ढह
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00557`

> उरश्व हृदयं चैव कुशिहस्ताङ्गुलीयकम् ॥४॥ ऊर जानू जङ्गदेशं पादं पादाङ्गुलीयकम् । भूवो च अस्थिमांसं च मेदोमजान्नरक्तकम् ॥५॥ त्वत्स्नेयवो २ नवद्वारा एकाशीतिपदे स्थिताः । पट्काणं इवेतवर्णं स्याद्वसुकोणं तु शुभ्रकम् ॥६॥ चतुष्कोणं रक्तवर्णं कौसुम्भं वसुकोणकम् । विशाल्कोणं पीतवर्णं इयामं पट्कोणमेव च ॥७॥ कृष्णं द्वाविंशतिश्चैव विशन्नीलं तथैव च । अष्टकोणं पितृ (पीत) वर्णं रक्तपीतं वसुस्तथा ॥८॥ पीतनीलं तु पट्कोणं हारोतं नवमं तथा । एकविंशं द्वितयं विद्यात्पाटलद्वितयं तथा ॥९॥ एवं वर्णानि …
> — **KRAM-2** · *The Hindu Temple, Volume II* · p. 141 · `kramrisch-1946-v2-00720`

> कोकिल की कूक और मतवाले भ्रमरों से अनुगुंजित, विचित्र फलों और पुष्पों से सम्पन्न वनों से सुशोभित हों। 29 *[IAST] kokila kī kūka aura matavāle bhramaroṃ se anuguṃjita, vicitra phaloṃ aura puṣpoṃ se sampanna vanoṃ se suśobhita hoṃ| 29* विकसित होते कुवलय (नीलकमलिनी), गूँजते भ्रमर, पोखर-देव-खात (खदान) आदि के साथ ही प्रचुर जल से शोभित हों। 30 *[IAST] vikasita hote kuvalaya (nīlakamalinī), gū~jate bhramara, pokhara-deva-khāta (khadāna) ādi ke sātha hī pracura jala se śobhita hoṃ| 30…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 29 · `bhojdev-hi-00131`

> 116 | THE UDAYESVARA TEMPLE साधिकराजसतामसभेदेन स जायते पुनरत्रेधा । स च वैकारिकतैजसभूतादिकनामभिः समुच्छ्रसिति ॥५४॥ तैजसतस्तत्र मनो वैकारिकतो भवन्ति चाक्षाणि । भूतादेस्तन्मात्राण्येषां सर्गोऽयमेतस्मात् ॥५५॥ इच्छारूपं हि मनो व्यापारस्तस्य भवति सङ्कल्पः । बुध्यक्षाणि श्रोत्रं त्वग्दृग्जिह्वा च नासा च ॥५६॥
> — **PAN** · *The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta* · p. 115 · `pande-udayesvara-00622`

**Gaps.** barely represented here: `RAJM`.

## C4 — From Avanti to Malwa: Dynasties, Trade Routes and Sacred Cities

[↑ contents](#contents)

**Coverage.** 2,538 chunks from 25 sources (`ADH`, `BHJ-H`, `DEV`, `GAN`, `GAZ-VID`, `GUP`, `HAR`, `INT-ARC`, `INT-GEO`, `KRAM-1`, `KRAM-2`, `PAN`, `PAR`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `RAJM`, `SAM`, `SIN-B`, `SIN-S`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: secondary_core 1235, primary_authorial_paramara 614, secondary_comparative 338, reference_tertiary 100, field_observation_reportage 90, primary_scriptural 58, primary_epigraphic 58, field_observation_survey 38, contextual_thematic 7. The largest single contributor is `SAM` with 610 chunks (24% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- His successor Vakpati II Munja (974–995 A.D.) was a great general, poet, and literary patron who defeated the Cholas, Chalukyas, and Chedis before losing his life to Taila II. — `GAN` · `PAT-INS` `[established]`
- During the reign of Nagabhata's successor Ramabhadra (A. D. 833-835), Gwalior formed the southern boundary of the Pratihâra kingdom of Kanauj. — `GAN` `[single-source]`
- His successor was Cacca, also known as Kakka 4 or Kańka, a contemporary of Siyaka-Harşa of Malwa (948-972 A. D.). — `GAN` `[single-source]`
- The decimal date recorded is **Māgha vadi 30, Wednesday, 1005 (Vikrama Samvat)**, which regularly corresponds to **31st January, 949 A.C.** — `PAT-INS` `[single-source]`
- Karna's successor, Jayasimha -Siddharaja (1096-1145 A. D.), was very young when he ascended the throne of Anhilwar, in 1196 A. D. His mother, Mayaņalladevî, became regent and managed the affairs of the state for some time. — `GAN` `[single-source]`
- His descendant, Sihada (1220-1234 A. D.), issued an inscription from Vâgadavatapadraka.4 The war between Siyaka II of Malwa and the Râstrakûta Khottiga took place in 970-971 A. D. The prince — `GAN` `[unverified]`
- Balban invested the town in 1251, and in 1304-5, Ain-ul-Mulk, the general of Alauddin Khilji, completed the final conquest of Malwa, including Chanderi. — `PAT-CH` · `PAT-INS` · `PAT-TEM` `[established]`
- Around 124 A.D., the Satavahana King Gautamiputra Satakarni revived southern fortunes, conquering Anupa (Nimar), Akara (East Malwa), and Avanti (West Malwa) from Nahapana. — `PAT-INS` `[single-source]`
- The Kalacuri Soma waged successful wars against the Mâlavas and the Gurjaras between 1167 and 1172 A. D. At this period, as has been pointed out, the Gurjaras occupied, by force of arms, the northern divisions of Malwa. — `GAN` `[single-source]`
- The Chinese pilgrim Hiuen Tsang (640 A.D.) recorded visiting *Molopo* (Western Malwa under the Buddhist prince Shiladitya), Ujjayini, and Maheshwarapura. — `PAT-INS` `[single-source]`
- The Ghori line was replaced in 1436 A.D. by the Khilji dynasty under **Sultan Mahmud Shah I (1436–1469 A.D.)**, a soldier-sultan under whom the Malwa Sultanate reached its maximum territorial extent. — `PAT-INS` `[single-source]`
- Vastupâla (1219-1233 A. D.), the minister of the Caulukya Viradhavala, when he went on a pilgrimage, was attended by the "Sanghapatis" (heads of the organised associations) from Lata, Gauda, Maru, Kaccha, Dahala, Avanti, and Vanga. — `GAN` `[single-source]`
- The last-mentioned king was apparently a contemporary of Mahîpala, the king of Kanauj (914-931, A. D.), who was the grand-son of Bhoja. — `GAN` `[single-source]`
- Tri-bhadra, Catur-bhadra, & Pañca-bhadra Clusters * **Tri-bhadra (56 Options)**: Advanced models including *Aindra, Viloma, Āyāma, Vadha, Ekākṣa, Antika, Prakāśa,* and *Paitra* matrices [cite: 6456, 6462, 6468]. — `SAM` `[single-source]`
- The Dharmapariksa was composed in Sam 1070 = 1013 A. D. I Sa jayati Vâkpati-rajaḥ sakalarthi-manorathaika-kalpataruḥ | Pratyarthi bhûta-parthiva-laksmî-hatha-harana-durlalitaḥ Edited by Visvanatha Sâstrî, Calcutta, 1874, (Bibl. — `GAN` `[single-source]`
- Mûtâ Nensî relates that the Guhila Sâmantasimha (1172-1179 A. D.), having established his supremacy in Vagada, brought all the surrounding territory under his control. — `GAN` `[unverified]`
- He was defeated by Dhruva II, the Râstrakûta chief of Lâta, some time before 867 A. D. 3 That Malwa still formed a part of the Râstrakûta dominion is shown by several epigraphic records. — `GAN` `[single-source]`
- The Bijolian inscription of Someśvara, dated 1169 A. D., reports that Jayadeva captured the dandanayaka Sulhana in battle, tied him to the back of a camel, and brought him to Ajmer. — `GAN` `[single-source]`
- Barely represented in this bucket, so anything resting on them is a thin reed: `SIN-S` — `[gap]`

### C4.6 — having, created, deserves, create, norm

> and rotater (cakra and bhramaraka). शृङ्गावली च नाराचः स्वबीजान्यौवर विदुः। ताप उत्तेजनं स्तोभः क्षोभश्च जलसङ्गजः ॥२८॥ The array of syringes, the sharp arrow normed instruments or clippers and choppers are the constituent elements they know in Aurvara i.e. a fertile track or Śrigāvalī and Nārāca are the two Aurvaras¹ or fertilising elements heating and boiling (tāpah and Uttejanam) of water, mixing and dissolving, pouring of and filling with water and providing of a belt of w…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 31: Named Yantravidhānaṁ i.e. The Chapter dealing with the Preparation of Mechanical Contrivances · `samarangana-00376`

> (ताम्रयाम्यासौम्यासु ?) शालाः स्युर्यदि वंशगाः। प्रिया स्यात् सर्वदेवानां तदा चूडा (मणिः प्रभाः ? ) ।॥६४॥ In east, south and north if śālās may be projected diagonally, then they may be dear to all gods then the light may be of the crest jewel. चतुरश्रीकृते क्षेत्रे चतुरश्रः समन्ततः । दशांशः (स्यादुभायान्ता ?) मध्ये प्रासादनायकः ।॥६५॥ In a field square shaped as such square shaped all around, may be in the centre Prāsāda nayaka on both the sides. पुरतः पृष्ठतश्चैव पार्श्वयोरु…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra > Architectural Treatise of Mahārājādhirāja Śrī Bhojadeva > [Original Page Source: 14] · `samarangana-01318`

> कुर्यात् त्रिभागिकं कूटं चतुर्धा प्रविभाजिते । भागिक्यो भित्तयः कार्यास्तथा गर्भो द्विभागिकः ।।६०।। One may create a Kūța of part-triad divided into four parts; the bhittis (walls) deserve to be created and likewise the garbha as part-twained. इत्येष सर्वतोभद्रस्तलच्छन्दो विधीयते । एते प्रोक्ता निरन्धाराः सान्धारांस्तु प्रचक्ष्महे ।।६ १।। This way this Sarvatobhadra Talacchanda is provided as such. These have been illustrated as Nirandhäras¹. Now we shall talk of Sandhāras2. …
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra > Architectural Treatise of Mahārājādhirāja Śrī Bhojadeva > [Original Page Source: 14] · `samarangana-01067`

> Even other towns fascinating ones, of these bearing the lokas i.e. kings, have been built by this one. Having seen your image (i.e. face) having been organised into a field² or locality or having been occupied or taken possession of or having been levelled by you having mountains and trees (included), he will establish the unions³ or areas of puras (i.e. towns), grāmas⁴ and nagaras.⁵ Then proceed, Oh Child! for the desire of beneficence of the people, from here. भयोज्झिता त्व…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra — Chapter 27 > CHAPTER 27¹ > Footnotes · `samarangana-00030`

### C4.4 — bhoja, inscription, king, paramara, reign

> I shall now endeavour to trace the course of events which led the Paramara family to depart from its ancient home and to establish numerous settlements in the north of the Narmada. It is an established fact that the main branch of the family ruled in Malava or Avanti. This country, prior to the establishment of the Paramaras, was ruled by a Pratihara branch of the Gurjara race, whose royal residence was fixed at Ujjain. The kingdom of this Pratihara family seems to have exten…
> — **GAN** · *History of the Paramāra Dynasty* · p. — · `ganguly-paramara-00038`

> Subsequently, Nagabhata made another attempt to regain his lost dominion of Mâlava, and apparently succeeded in capturing an outlying fortress of that country. But the effect of this achievement was but temporary. During the reign of Nagabhata's successor Ramabhadra (A. D. 833-835), Gwalior formed the southern boundary of the Pratihâra kingdom of Kanauj. 1 E. I., Vol. XVIII, p. 112. 2 J. Dep. L, Vol. X, p. 40. 3 Ibid., E. I., Vol. XVIII, p. 112, V. 10. 4 Vatsaraja is describe…
> — **GAN** · *History of the Paramāra Dynasty* · p. — · `ganguly-paramara-00052`

> E. I, Vol. XIV, pp. 117, v. 13. 6 Banglar Itihas, by R. D. Banerji, Vol. I, pp. 99 ff. 7 The Life of Harsa, by Dr. R. K. Mukherjee. 8 Cf. author's "Malava in the 6th and 7th C. A. D.", to be published in J. B. O. R. S. A C D ii INTRODUCTION in Kanauj became virtually extinct. Harsavardhana transferred his capital to Kanauj, and tried to establish paramount sovereignty over Northern India. It has not yet been definitely established how far he was able to realise his ambition. …
> — **GAN** · *History of the Paramāra Dynasty* · p. — · `ganguly-paramara-00001`

> I., Vol. IX, p. 76, v. 26.) 4 Prabandhacintamani, pp. 87, 15. 5 I. A., Vol. VI, pp. 191. the lord of Avanti (Avanti-natha). Mahadeva, son of Damda Dadaka of the Nagara race, was appointed governor of the province of Avanti by Siddharâja. A. stone inscription of Jayasimha, dated V. S. $1195=1138~A.$ D., found at Ujjain, tells us that the king, having defeated Yasovarman, was holding Avanti-mandala by force, and that Mahadeva was administering it on his behalf. As regards Yasov…
> — **GAN** · *History of the Paramāra Dynasty* · p. 82 · `ganguly-paramara-00361`

### C4.3 — temple, temples, form, hands, left

> She was so impressed that she condemned even Svargaloka and the city in Patala. Oh! In fact, that lady was not so much delighted after getting Amitrajit as her husband as she was delighted on seeing Avanti that bestows great bliss. That lofty-minded lady considered herself as one who had successfully realized all her desires. Along with her husband, she attained the greatest pleasure in Ujjayini. After getting Malayagandhini as his wife, Amitrajit engaged in love (making) wit…
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 174 · `skanda-xiii-00358`

> Mandasor) to Allahabad in the east, holds an intermediate position artistically too, in the history of medieval sculpture.^ Here products, from the 10th to the 13th centuries turned out under the aegies and Patronage of the Chandellas of Jejakbhukti and the Paramaras of Dhara reflect an admixture of both east Indian tradition of Bihar and Bengal and that of Rajputana and Gujarat, where the medi- eval trends found their most congenial home. Garhwal, Mahoba and Khajuraho preser…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-01052`

> | No. | Chapter | Subject | Page No. | | --- | --- | --- | --- | | 1 | — | Editorial | 13 | | 2 | — | Invocation to Shri Ganesha (Sanskrit poem) | 19 | | 3 | — | To Kalidasa's Ujjayini (poem) | 20 | | 4 | One | Ujjayini | 21 | | 5 | Two | Mahakal | 75 | | 6 | Three | The Mahakal Forest | 104 | | 7 | Four | Shipra, Beloved of Shiva | 109 | | 8 | Five | Vision of Shakti | 141 | | 9 | Six | King Bhartrihari–Vikramaditya | 163 | | 10 | Seven | The Temples of Ujjayini | 188 | | 11…
> — **RAJ-E** · *King Bhoj and Paramara-period Town Architecture (English translation)* · p. 189 · `rajpurohit-bhoj-en-00570`

> In terms of style all these lie along the spectrum of Dravida architecture that runs between that of the broad Tamil tradition and the continuing Karnata Dravida still centred on the former Chalukya heartland. This statement needs to be qualified, as the Badami region, no longer the political centre that it had been, produced mainly modest works during this period, but these form a conduit between the monuments of the Early Chalukyas and the 11th-century explosion of temple a…
> — **HAR** · *The Temple Architecture of India* · p. 226 · `hardy-2007-00919`

### C4.5 — town, temple, bhoj, architecture, temples

> The Chinese pilgrim Hiuen Tsang (640 A.D.) recorded visiting *Molopo* (Western Malwa under the Buddhist prince Shiladitya), Ujjayini, and Maheshwarapura. The decline of the Pratiharas and Rashtrakutas in the late 10th century cleared the way for two major regional Rajput dynasties: the **Paramaras** in Malwa and the **Kacchavahas** in Gwalior. * **The Paramaras of Malwa:** Originating as Rashtrakuta feudatories in Gujarat, they shifted to Malwa under Siyaka II, who plundered …
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00031`

> Proximity to the fertile Gangetic plains made the region about Bhilsa prosperous—a fact reflected in the richness of its monuments, second to none in Madhya Bharat. In ancient geography, it was called Dasharna, known from the days of the Buddha to those of Kalidasa (c. 5th century A.D.). The name lives on in the modern Dhasan river. In late historical times, it came to be known as part of Gondwana, ruled by the Gonds. Ancient Vidisha and its successor Bhilsa have always been …
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00016`

> In the *Geography* of Ptolemy, written about 150 A.D. with materials collected a few years earlier, Ozene, i.e., Ujjaini, capital of Avanti, is mentioned as the headquarter of Tiastenes, the Greek corruption of Chastana. In the Junagarh rock inscription, Rudradaman is represented as the lord of many countries including Akara, Avanti, and Anupa. This region continued to be a Shaka possession, excepting perhaps some portions of western Malwa, till its final incorporation with t…
> — **PAT-CH** · *The Cultural Heritage of Madhya Bharat* · p. — · `patil-1952-00073`

> The charter records that while staying in the strategic eastern territory of **Pūrṇa-pathaka** (modern Punasa, near Mandhata on the Narmada), Vakpati donated the village of **Kadahichchhakā** (modern Karcha, north of Narwal in the Ujjain District), which was situated within the **Maddhuka-bhukti** of the **Ujjayanī vishaya** in the **Avantī-mandala**.
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00144`

### C4.1 — malwa, kingdom, under, empire, ujjain

> By the 6th century B.C., Avanti emerged as an independent kingdom under the Pradyota dynasty. Its greatest ruler, Chanda Pradyota, a contemporary of the Buddha, ruled from Ujjain, making it a powerful commercial hub linking the Gangetic plains to western ports like Bharukaccha (Bharuch) and Surparaka (Sopara). Ajatashatru of Magadha feared Pradyota's military might so much that he fortified his capital, Rajagriha. The Pradyotas were eventually subverted by the Shaishunagas of…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00023`

> - Mauryan Dynasty (Ashoka) - Sunga Dynasty (Pushyamitra) - Gupta Dynasty (Chandragupt, Samundragupt) - Parmars Dynasty - Chalukya Dynasty - Khalji Dynasty - Tughlaq and Ghuri Dynasty
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 16 · `intach-2022-udaypur-00051`

> In the field of art and architecture also, Malwa had reached a high pitch of excellence, as is witnessed in the magnificent temples at Udaypur, Nemawar, Jamli, Badnawar, and Un, which undoubtedly rank high among the best specimens of ancient Indian architecture. Bhoja rebuilt the old town of Dhara, which had already become the capital of the Paramaras, and raised it to the status of the great cities of his age. Of the few remnants of that glorious city which are now left, the…
> — **PAT-CH** · *The Cultural Heritage of Madhya Bharat* · p. — · `patil-1952-00098`

> The region of Malwa occupies a place 6f pride in the political and cultural history of India. The kingdom of Avanti (ancient name of Malwa) was counted among the major kingdoms {mabnjanapadas) with Ujjayini as its capital. The Vcdic-puranic traditions and the Buddhist and Jalna works refer to the supre- macy of Chanda Pradyota of Avanti during the time of the Buddha. The archaeological excavations and explorations conducted at sites likd Maheshwar, Navadatoli. Kayatha, Nagda,…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00001`

### C4.2 — iast, aura, para, haiṃ, rājā

> राजा भोज के समय से मालवा में निर्माण-क्रांति आ गयी थी। प्रासाद, मन्दिर, तालाब, प्रतिमाएँ बनती रहीं और पूरा मालवा इन अनोखी कलाकृतियों से भर गया। मन्दसौर जिला इस दृष्टि से अधिक समृद्ध है। वहाँ का हिंगलाजगढ़ तो तत्कालीन अप्रतिम प्रतिमाओं का अकृत खजाना है। आज मालवा में जो कुछ निर्मितियों के प्राचीन रूप दिखाई देते हैं, उनमें से बहुधा परमारकालीन हैं। *[IAST] rājā bhoja ke samaya se mālavā meṃ nirmāṇa-krāṃti ā gayī thī| prāsāda, mandira, tālāba, pratimāe~ banatī rahīṃ aura pūrā māla…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 6 · `bhojdev-hi-00028`

> राजा भोज ने शारदा सदन या सरस्वती कण्ठाभरण बनवाये थे। वात्स्यायन ने कामसूत्र में संकेत किया था कि प्रत्येक नगर में सरस्वती भवन होना चाहिए। वहाँ गोष्ठियाँ, नाटक आदि हर पन्द्रह दिन में होते रहने चाहिए। राजा भोज ने सम्भवतः उसी परम्परा का निर्वाह कर धार, माण्डव तथा उज्जैन में सरस्वतीकण्ठाभरण नामक भवन बनवाये थे। भोज ने जो अनेक मन्दिर बनवाये थे उनमें केदार, रामेश्वर, सोमनाथ, मुण्डीर आदि भारत की चारों दिशाओं में थे और मध्य में महाकाल! इसकी पुष्टि उदयपुरा शिलालेख और धार से प्राप्त प्र…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 6 · `bhojdev-hi-00029`

> राजा भोज ने अपने युग में प्रचलित ज्ञान की प्रायः सभी धाराओं को अपनी रचनाओं *[IAST] rājā bhoja ne apane yuga meṃ pracalita jñāna kī prāyaḥ sabhī dhārāoṃ ko apanī racanāoṃ* में समेटा है। इस प्रकार भोज का समय साहित्य मिलकर उस समय का विश्वकोप ही हो जाता है। ज्ञान के विश्वकोप की कुछ वानगी प्रस्तुत करने-करवाने के लिए मैं स्वराज संस्थान संचालनालय का आभारी हूँ। इस बहाने मालवा की एक विभूति से एक बार फिर उसके साहित्य के माध्यम से रूबरू होने का अवसर मिल रहा है - महाराजाधिराज परमेश्वर श्…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 23 · `bhojdev-hi-00116`

> *[IAST] śṛṃgāramaṃjarīkathā meṃ ina snehī rājāoṃ (praṇayibhiḥ nṛpatibhiḥ) kī bhojagoṣṭhī meṃ bhī upasthiti batāyī gayī hai| saikar̤oṃ rājā usake adhīna the| yaha bhoja kī racanāoṃ se jñāta hotā hai| spaṣṭa hī ve racanāe~ isa samarāṃgaṇasūtradhāra se bāda kī haiṃ| vaise vidiśā se bhopāla kṣetra meṃ bārahavīṃ śatī meṃ 'mahādvādaśakamaṇḍala' thā| parantu vaha eka hī maṇḍala kā nāma thā| dhāra jile kā baramaṇḍala kasbā bhī aise hī prācīna maṇḍala kā nāmāvaśeṣa pratīta hotā hai| a…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 4 · `bhojdev-hi-00020`

**Gaps.** barely represented here: `SIN-S`.

## C5 — The Paramāras and Bhoja: Kingship, Learning and Temple Building

[↑ contents](#contents)

**Coverage.** 2,877 chunks from 25 sources (`ADH`, `BHJ-H`, `DEV`, `GAN`, `GAZ-VID`, `GUP`, `HAR`, `INT-ARC`, `INT-GEO`, `KRAM-1`, `KRAM-2`, `PAN`, `PAR`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `RAJM`, `SAM`, `SIN-B`, `SIN-S`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: secondary_core 1791, primary_authorial_paramara 600, secondary_comparative 178, field_observation_reportage 144, primary_scriptural 80, field_observation_survey 39, primary_epigraphic 27, reference_tertiary 17, contextual_thematic 1. The largest single contributor is `SIN-B` with 658 chunks (23% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- The date of Udayāditya's accession to the throne of Malwa is not settled: four reckonings in the corpus give four different spans, and a record of 1059 places the paramount throne with Jayasiṃha in the year the Udaypur foundation inscription shows Udayāditya building. — competing values: **1058–1087** (`PAT-CH`); **1059–1086** (`GAN`); **c. 1059–93** (`INT-ARC`); **1070–1093 (from the coinage)** (`INT-ARC`) `[contested]` `[curated]`
  - The counter-evidence is the Panhera inscription of V.S. 1116 (1059 CE), issued by Jayasiṃha's feudatory Mandalika, which reports Jayasiṃha ruling Malwa at that date; the reconciliation offered in the literature is that Udayāditya held his paternal territory and built at Udaypur in 1059 without yet being sovereign. That reconciliation is labelled speculation in the KB and must not be asserted as settled.
  - traceable to: `ganguly-paramara-00262`, `ganguly-paramara-00275`, `ganguly-paramara-00274`, `patil-1952-00095`, `ganguly-paramara-00568`, `intach-2022-udaypur-00127`, `intach-2022-udaypur-00075`
- His successor Vakpati II Munja (974–995 A.D.) was a great general, poet, and literary patron who defeated the Cholas, Chalukyas, and Chedis before losing his life to Taila II. — `GAN` · `PAT-INS` · `SIN-B` `[contested]` — figures differ: `GAN` 972, 995; `PAT-INS` 974, 995; `SIN-B` 970, 974
- On the basis of Munja’s earliest grant dated 974 A.D., scholars have speculated his reign from about C 970 A.D. to 977 A.-'D. — `SIN-B` `[single-source]`
- The Dharmapariksa was composed in Sam 1070 = 1013 A. D. I Sa jayati Vâkpati-rajaḥ sakalarthi-manorathaika-kalpataruḥ | Pratyarthi bhûta-parthiva-laksmî-hatha-harana-durlalitaḥ Edited by Visvanatha Sâstrî, Calcutta, 1874, (Bibl. — `GAN` `[single-source]`
- The Betma plates® of Bhojadeva dated V.S. 1076 (A.D. 1020) record that Bhoja granted properly to Brahmana, including 1. — `SIN-B` `[single-source]`
- Gaurishankar Ojha® on the authority of Vadnagar Prasasti of Kumarapala dated •V.S. 1108 or 1151 A.D “ assigns 1010 A.D, as the date of Sindhu- raja’s death, which he thinks took place in a fight with Camunda- 1. — `GAN` · `SIN-B` `[established]`
- The question now arises as to why Kirtane should have taken A.D 994 and not A.D 997 when A.D 997^ is given as the maximum limit for the reign of Munja. — `SIN-B` `[single-source]`
- His successor was Cacca, also known as Kakka 4 or Kańka, a contemporary of Siyaka-Harşa of Malwa (948-972 A. D.). — `GAN` `[single-source]`
- The contemporary Cola kings was Madhurantaka-Uttamacola (969-985 A. D.) and Rajaraja I (985-1012 A. D.). — `GAN` `[single-source]`
- Karna's successor, Jayasimha -Siddharaja (1096-1145 A. D.), was very young when he ascended the throne of Anhilwar, in 1196 A. D. His mother, Mayaņalladevî, became regent and managed the affairs of the state for some time. — `GAN` `[single-source]`
- In that predicament Vijayaditya VII, the younger brother of the deceased Rajaraja, took up the cause of his nephew, and appealed to Cola Virarajendra (A. D. 1062-1069) for assistance. — `GAN` `[single-source]`
- Ind.) and by Kedaranatha and Panashikar, Bombay, 1908, (Kavyamála Series, No. 91) 2 Subhasita-ratna-samdoha, Kavyamâlâ series, No. 82. — `GAN` `[single-source]`
- The record is dated 1218 V. S. = 1161 A. D. Here Sindhuraja is described as the earliest member of the family, whose son and successor was Dûsala. — `GAN` `[single-source]`
- The Chinese pilgrim Hiuen Tsang (640 A.D.) recorded visiting *Molopo* (Western Malwa under the Buddhist prince Shiladitya), Ujjayini, and Maheshwarapura. — `PAT-INS` `[single-source]`
- If King Bhoj ruled up to 1055, then subtracting 55 years, 7 months and 3 days from that makes his accession possible around 999 CE. — `GAZ-VID` · `RAJ-E` · `SIN-B` `[established]`
- A Hoysala grant from Belur, dated 1117 A. D., records that "Dhara was made prosperous by Bhoja." Since his reign, it had enjoyed the position of the chief city of Malwa, even down to the time of the Muhammadan rule. — `GAN` `[single-source]`
- Tri-bhadra, Catur-bhadra, & Pañca-bhadra Clusters * **Tri-bhadra (56 Options)**: Advanced models including *Aindra, Viloma, Āyāma, Vadha, Ekākṣa, Antika, Prakāśa,* and *Paitra* matrices [cite: 6456, 6462, 6468]. — `SAM` `[single-source]`
- King Bhoj and Paramara-period Town Architecture / 95 In the Vairaja family: Meru, Mandara, Vimana, Bhadra, Sarvatobhadra, Ruchaka, Nandaka or Nandana, Vardhamana-Nandi or Nandivardhana, and Shrivatsa. — `RAJ-E` `[single-source]`
- He is also mentioned as a contemporary of the Caulukya Bhîma II (1178-1239 A.D.) and the Câhamâna Prthviraja III, son of Someśvara, the king of Ajmer (1179-1193 A, D.). — `GAN` `[single-source]`
- Barely represented in this bucket, so anything resting on them is a thin reed: `SIN-T` — `[gap]`

### C5.4 — temple, they, times, temples, siva

> 4- Udaipur frasasti, E.I.I. p, 238, V. 20, 340 Bhoja ParaniHra and his Times opine that the reference seems to be to Kalagni-Rudra, one of the terrible forms of Siva, mentioned by Somadeva in the Ya^astiJaka, Book I, p. 151.* Bhojapur Temple One of the most significant specimens of the Paramara Tem- ples of Malvva, is the Siva Temple known as Bhojesvara temple at Bhojpur. It is situated 20 miles south of the modern city of Bhopal. The exact date being unknown, the temple is p…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-01005`

> Bhoja, I, the Paramara ruler of Malwa, was not only a follower but also an exponent of Saivism.- One of his works, the Tattvaprakasa deals with Saivism. In his Samarangana Satradhara he has devoted a separate chapter for the treatment of lihgas, the emblematical phallus of S-va. It introduces a novelty by its description of the Lokapala lingas, like Agneya, Aindreya, Yamya, Varuna, Vayanya etc etc.® Though traditional it is unique in the sense that it gives the relative merit…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00491`

> god. The beneficiery forms of Rudra (Siva) are known as Aghora, or the milder (Saumya) forms of Saivism. The Samaraiigana 1 . Tantraloka. I. p, 34, XIl, p. 397, 2, EHI, IJ, I. Introduction, p. 29, 148 Bhoja ParcitnSra and his Times Sutradhara of Bhoja also deals in detail with these two forms cf Siva. Srikantha, Ananta, Lakulisa and Goraksa were the Saiva teachers who later on rose to the position of deities. II. KSpoUka School The epigraphio references prove the wide popular…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00455`

> Amitagati was the disciple of Madhavasena, whose preceptor was Nemişena, the head of the Jaina ascetics 2 of the Mathurasamgha. He was a scholar of great fame, and flourished in Malava at the end of the tenth century A. D. and the beginning of the eleventh. He completed his work, "Subhasita-ratna-samdoha", in Sam. 1050 = 993 A. D., when the king Muñja was ruling. His other books are: (a) Sravakacara 4 (b) Dharmapariksa 5 (c) Dvâtrimsatika. The Dharmapariksa was composed in Sa…
> — **GAN** · *History of the Paramāra Dynasty* · p. 102 · `ganguly-paramara-00621`

### C5.1 — malwa, inscription, dynasty, paramara, reign

> 80 HISTORY OF THE PARAMARA DYNASTY relaxation of their supremacy over Mount Abu and Southern Marwar, which eventually culminated in the temporary overthrow of the Paramara rule in the former province, in the third decade of the 11th century A. D. Side by side with his political activities, Sindhuraja energetically fostered the literary movement, which had been vigorously carried on in Malwa under the patronage of his predecessors. Padmagupta tells us that, "The seal which Vak…
> — **GAN** · *History of the Paramāra Dynasty* · p. — · `ganguly-paramara-00202`

> with the father of Pûrņapala of the Vasantgadh inscription. As no king named Kanhada is found in the genealogy of the Paramara rulers of Mount Abu, as stated by the Vasantgadh inscription, it appears probable that he preceded Utpalarâja. We have ample evidence to prove that the names Kanhada and Krsnaraja are synonymous. In the two Mount Abu inscriptions, both dated 1287 V. S., the Paramara Somasimha's son and successor is mentioned in one place as Kanhada and in another plac…
> — **GAN** · *History of the Paramāra Dynasty* · p. — · `ganguly-paramara-00072`

> 168 HISTORY OF THE PARAMARA DYNASTY Saurâstra and Malava into prison. The Vadnagar prasasti of Kumarapala, dated 1151 A. D., states that Jayasimha fettered the proud king of Malava. The Prabandha caturviñjati relates that Jayasimha, after his conquest of Mâlava, subdued the kingdoms of the south viz, Maharastra, Tilanga, Karnata, and Pandya. The Sundha hill inscription of Câcigadeva records that Jayasimha secured assistance from the Cahamâna, Asaraja, chief of Nadul, in his w…
> — **GAN** · *History of the Paramāra Dynasty* · p. 82 · `ganguly-paramara-00360`

> rama) {Samv.tt) 1161 El. Vol. II., p. 180. 5. E. I. Vol. II, p. 181. 6. E. I. Vol. XVIII, p. 324. 2 Blioja Paramara and his Times with Harsa of Udaipur-prasasti,’ Ssyaka of the Nagpor-prasasti," Slyakaharsa Vadaja of the Navasahasahkacarita” and Slyaka of the landgrants of Vakpati'“ and Bhoja.^' After Siyakadeva there follow the names of his later successors viz. Vakpatiraja- deva or Vakpati II, alias Munja, Sindhurajadeva and Bhoja.
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00035`

### C5.3 — created, having, deserves, create, norm

> SAMARĀNGAŅA-SŪTRADHĀRA of Mahārājādhirāja Śrī Bhojadeva Paramāra The foundation of shrines एवं नृपस्य प्रासादे कृते क्लृप्तेऽथवा भुवि। तस्यानुजीविनः कुर्युः प्रासादान् परिधौ यदि ।।१।। This way the palace of the king having been built or well laid on the ground, if his entourage may create abodes on the surrounding premises or periphery. तदा दिग्भागविन्यासस्थानमानान्यनुक्रमात्। तेषामिहाभिधीयन्ते सर्वेषां वृद्धिहेतवे ।।२।।
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. CHAPTER 51 · `samarangana-00772`

> [paraphrase — not a verbatim quote; source text unreliable] ``` # SAMARĀNGANA-SŪTRADHĀRA ### of Mahārājādhirāja Śrī Bhojadeva Paramāra ## CHAPTER 3: Praśna (A Questionnaire) तस्मादुवाच मुनिर्वत्साः ! विदितं वो यथा पुरा... *(Note: Transition text from Chapter 2 concluding elements)* The abodes of castes or orders of society, the constituent elements of the state $(Prakrti)^{1}$ or subjects and the Institutes or Institutions by demarcation deserve to be created in every village, town and pattana. [cite: 394] तानित्यमात्मतनयानभिधाय सम्यक…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. SAMARĀNGANA-SŪTRADHĀRA > CHAPTER 2: The Conversation Between Viśvakarmā and His Sons (Mānasa Putras) > FOOTNOTES & TEXTUAL CRITICAL NOTES > Chapter 2 Footnotes · `samarangana-00052`

> [paraphrase — not a verbatim quote; source text unreliable] ``` # SAMARĀNGANA-SŪTRADHĀRA ### of Mahārājādhirāja Śrī Bhojadeva Paramāra ## CONCLUSION OF CHAPTER 4: Mahadādi-Sarga ज्ञात्वैनां पुरुषः पुण्यां भवति स्वर्गभाजनम्। भुवनभूजलवह्निमरुद्वियत्प्रमुख एष भवस्तव कीर्त्तितः। वसुमतीपरिमाणविनिश्चयं कथयतः शृणु सम्प्रति वत्स ! मे।॥३८॥ Having known this the sacred one the man becomes an object of Heaven [cite: 741]. The universe, the earth or ground, the water, the fire, the wind and the sky or atmosphere headed by these this creativity fo…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. SAMARĀNGANA-SŪTRADHĀRA > CHAPTER 4: Sṛṣṭi-Varṇana (The Description of Creation / Mahadādi Sarga¹) > CHAPTER 4 FOOTNOTES · `samarangana-00101`

> ``` # Samarāṅgaṇa-sūtradhāra ## Architectural Treatise of Mahārājādhirāja Śrī Bhojadeva ### English Translation with Sanskrit Typology Matrix ### [Original Page Source: 1] #### **Chapter 57** #### **CHAPTER 57** #### **A twenty counting of Meru and others** **Sanskrit (Śloka):** `अथान्यान् कथयिष्यामः समासात् सूक्ष्मलक्षणान्।` **Sanskrit (Śloka):** `पञ्चाशतमिहोत्कृष्टान् प्रासादाञ् श्रीधरादिकान् ।।१।।` **English Translation:** *Now we shall talk of others having minuter pre-re…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 56: The Illustration of Sixty-Four Prāsādas Headed by Rucaka > 4. Deity Placement and Architectural Vulnerabilities (*Marmavedha*) > Avoiding Vulnerable · `samarangana-00863`

### C5.5 — bhoj, town, architecture, king, paramara

> The Chinese pilgrim Hiuen Tsang (640 A.D.) recorded visiting *Molopo* (Western Malwa under the Buddhist prince Shiladitya), Ujjayini, and Maheshwarapura. The decline of the Pratiharas and Rashtrakutas in the late 10th century cleared the way for two major regional Rajput dynasties: the **Paramaras** in Malwa and the **Kacchavahas** in Gwalior. * **The Paramaras of Malwa:** Originating as Rashtrakuta feudatories in Gujarat, they shifted to Malwa under Siyaka II, who plundered …
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00031`

> There are many *Bhoja-prabandhas* (भोजप्रबन्ध) concerning King Bhoj, of which Ballala's (बल्लाल) is the most popular. Along with the *Bhoja-charita*, *Bhoja-raso*, *Bhojarajanka-rupaka* and others, there is a long tradition of works concerning Bhoj. Among the works composed by King Bhoj himself, the following are published: *Vagdevi-stotra*, *Avanikurma-shatam*, *Champu-ramayana*, *Subhashita-prabandha*, *Shringara-manjari-katha*, *Sarasvati-kanthabharana*, *Shringara-prakash…
> — **RAJ-E** · *King Bhoj and Paramara-period Town Architecture (English translation)* · p. 16 · `rajpurohit-bhoj-en-00057`

> "Where the Paramara, there Dhar." "Where Dhar, there the Paramara. Without Dhar, no Paramara. Without the Paramara, no Dhar." Collections of folk-current tales relating to Bhoj kept being made, many, in various languages. There are several *Bhoja-prabandhas*. The Sanskrit *Bhoja-prabandhas* of Ballala, Shubhashilagani, Ratna-mandanagani, Satyarajagani, Rajashekhara and others are well known; of them, Ballala's *Bhoja-prabandha* is the most famous. Rajavallabha's *Bhoja-charit…
> — **RAJ-E** · *King Bhoj and Paramara-period Town Architecture (English translation)* · p. 161 · `rajpurohit-bhoj-en-00472`

> King Bhoj and Paramara-period Town Architecture / 161 in the fourteenth century at Vardhamanapura (present Badnawar) in the Dhar district of Malwa. These stories, though brief, are interesting, factual, and various folk-facts relating to Bhoj. In the various *Bhoja-prabandhas*, different aspects of Bhoj's personality and achievement are revealed. In Ballala's famous *Bhoja-prabandha*, presenting Bhoj together with the circle of poets, his love of poetry and his tenderness of …
> — **RAJ-E** · *King Bhoj and Paramara-period Town Architecture (English translation)* · p. 161 · `rajpurohit-bhoj-en-00473`

### C5.2 — bhoja, king, times, time, over

> The names of various kings of the Paramara dynasty, such as Upendra (उपेन्द्र), are found. Among them, Siyak (सीयक) or Shriharsha (श्रीहर्ष) is the first Paramara king whose tenth-century copper-plate grants are found. He had two sons: Vakpatiraja Munj (वाक्पतिराज मुंज) and Sindhuraja (सिन्धुराज) or Sindhul (सिन्धुल). Munj was himself a king and a poet, and a patron of poets. Among those he patronized were several scholars: Padmagupta "Parimal" (पद्मगुप्त परिमल), Dhananjaya (…
> — **RAJ-E** · *King Bhoj and Paramara-period Town Architecture (English translation)* · p. 2 · `rajpurohit-bhoj-en-00004`

> Bhoja was famous as a great scholar, and as a patron of art and literature. Bhojaśālā, an institution for learning Sanskrit, was built by him at his capital, Dhāra. To help the students in the process of learning, many inscriptions containing alphabetical charts, grammatical rules etc. were engraved on the wall and pillars of Bhojaśālā. These alphabetical charts were displayed within twin snake coils. Scholars refer to this peculiar mode of presenting grammatical charts by in…
> — **ADH** · *Some Paramāra Temples From Madhya Pradesh: A Case Study of Village Un* · p. 45 · `adhikari-2013-un-00606`

> With the accession of Bhoja (c.A.D.1000-c.A.D.1055), the son and successor of Sindhuraja, a brilliant chapter was opened in the history of the art and architecture of Mālavā. Epigraphical evidence eloquently testifies his participation in a vigorous temple building activity. For example v.20 of the Udaypur *Prakasti* of Udayāditya eulogies Bhoja for beautifying the world with temples dedicated to Śiva under such names as Kedāreśvara, Rāmeśvara, Somanābha, Sundra, Kāla, Anāja …
> — **ADH** · *Some Paramāra Temples From Madhya Pradesh: A Case Study of Village Un* · p. 9 · `adhikari-2013-un-00045`

> The wish to see the changed form of the narrow lane once again drew, on the day of Vasant Panchami, the twin-pair of a knower of history and a seeker to Udaipur. On the way itself, I searched out, on the mobile, an old article of mine. It was centred on Raja Bhoj. In the Saraswati-kanthabharana of Bhoj's capital Dhar, the liveliness of this day's occasion must have been decked out for who knows how long. On my Facebook page I posted that old article. We were on the way to Uda…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00227`

### C5.6 — iast, aura, rājā, haiṃ, para

> राजा भोज परमार राजवंश में उत्पन्न हुआ था। यह परमार राजवंश मालवा में शासन करता था। सीयक द्वितीय (दसवीं शती) तक परमार राष्ट्रकूटों के प्रतिनिधि के रूप में शासन करता था। इसका पुत्र वाकपति मुंज (974-997 ई.) मालवा का स्वतंत्र शासक हो गया। इसने अपने पड़ोसी क्षेत्रों पर अधिकार कर पर्याप्त राज्य विस्तार किया। मुंज का अनुज सिन्धुराज (997-999 ई.) था। इसने कुन्तल तैलप द्वितीय को पराजित किया। हूणों को पराजित कर उसने वागड़ (वाँसवाड़ा-डूँगरपुर) क्षेत्र पर विजय प्राप्त की। तदनन्तर उसने कौशल…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 3 · `bhojdev-hi-00012`

> राजा भोज (999-1055 ई.) इसी सिन्धुराज का पुत्र था। उसके 1010 से 1055 ई. तक के कई ताम्रपत्र, शिलालेख या मूर्तिलेख प्राप्त होते हैं। एक ताम्रपत्र के अन्त में लिखा गया है - स्वहस्तोंय श्रीभोजदेवस्य। अर्थात् यह (ताम्रपत्र) भोजदेव ने अपने हाथ से लिखा (और दिया) है। भोज के बरिह ताम्रपत्र या शिलालेख प्राप्त हैं। अन्य समकालीन तथा परवर्ती अनेक अभिलेखों में भी उनके उल्लेख प्राप्त होते हैं। राजा भोज ने परम्परानुसार 55 वर्ष 7 मास 3 दिन तक गौड़ देश और दक्षिणापथ सहित विस्तृत क्षेत्र पर राज्य…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 3 · `bhojdev-hi-00013`

> ताम्रपत्रों में भोज के ग्रन्थों की पुष्पिकाओं में उन्हें 'महाराजाधिराज परमेश्वर श्रीभोजदेव' कहा गया है। स्पष्ट ही राजा भोज राजाओं के भी राजा थे। समरांगणसूत्रधार (31/224) में स्वयं भोज ने कहा है कि उस राजचूडामणि भोज की इच्छा पर पूरा द्वादश राजसमूह नाचता था क्योंकि उनकी वृत्ति इस राजाधिराज के भुजास्तम्भ से बँधी थी - *[IAST] tāmrapatroṃ meṃ bhoja ke granthoṃ kī puṣpikāoṃ meṃ unheṃ 'mahārājādhirāja parameśvara śrībhojadeva' kahā gayā hai| spaṣṭa hī rājā bhoja rājāoṃ ke bhī rājā t…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 4 · `bhojdev-hi-00018`

> राजा भोज ने शारदा सदन या सरस्वती कण्ठाभरण बनवाये थे। वात्स्यायन ने कामसूत्र में संकेत किया था कि प्रत्येक नगर में सरस्वती भवन होना चाहिए। वहाँ गोष्ठियाँ, नाटक आदि हर पन्द्रह दिन में होते रहने चाहिए। राजा भोज ने सम्भवतः उसी परम्परा का निर्वाह कर धार, माण्डव तथा उज्जैन में सरस्वतीकण्ठाभरण नामक भवन बनवाये थे। भोज ने जो अनेक मन्दिर बनवाये थे उनमें केदार, रामेश्वर, सोमनाथ, मुण्डीर आदि भारत की चारों दिशाओं में थे और मध्य में महाकाल! इसकी पुष्टि उदयपुरा शिलालेख और धार से प्राप्त प्र…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 6 · `bhojdev-hi-00029`

**Gaps.** barely represented here: `SIN-T`.

## C6 — Udayāditya's Foundation: Town, Temple and Tank

[↑ contents](#contents)

**Coverage.** 1,570 chunks from 25 sources (`ADH`, `BHJ-H`, `DEV`, `GAN`, `GAZ-VID`, `GUP`, `HAR`, `INT-ARC`, `INT-GEO`, `KRAM-1`, `KRAM-2`, `PAN`, `PAR`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `RAJM`, `SAM`, `SIN-B`, `SIN-S`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: secondary_core 645, primary_authorial_paramara 373, field_observation_reportage 195, secondary_comparative 115, field_observation_survey 93, primary_scriptural 72, reference_tertiary 64, primary_epigraphic 12, contextual_thematic 1. The largest single contributor is `SAM` with 373 chunks (24% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- The date of Udayāditya's accession to the throne of Malwa is not settled: four reckonings in the corpus give four different spans, and a record of 1059 places the paramount throne with Jayasiṃha in the year the Udaypur foundation inscription shows Udayāditya building. — competing values: **1058–1087** (`PAT-CH`); **1059–1086** (`GAN`); **c. 1059–93** (`INT-ARC`); **1070–1093 (from the coinage)** (`INT-ARC`) `[contested]` `[curated]`
  - The counter-evidence is the Panhera inscription of V.S. 1116 (1059 CE), issued by Jayasiṃha's feudatory Mandalika, which reports Jayasiṃha ruling Malwa at that date; the reconciliation offered in the literature is that Udayāditya held his paternal territory and built at Udaypur in 1059 without yet being sovereign. That reconciliation is labelled speculation in the KB and must not be asserted as settled.
  - traceable to: `ganguly-paramara-00262`, `ganguly-paramara-00275`, `ganguly-paramara-00274`, `patil-1952-00095`, `ganguly-paramara-00568`, `intach-2022-udaypur-00127`, `intach-2022-udaypur-00075`
- Contemporary Sanskrit inscriptions on its porches record that it was founded by the Paramara King **Udayaditya**; construction commenced in **1059 A.D.** (*V.S. 1116*) and the flagstaff was hoisted in **1080 A.D.** (*V.S. 1137*). — `ADH` · `DEV` · `GAN` · `GAZ-VID` · `HAR` · `INT-ARC` · `KRAM-1` · `KRAM-2` · `PAT-CH` · `PAT-INS` · `PAT-TEM` · `TIW-E` `[established]`
- His successor Vakpati II Munja (974–995 A.D.) was a great general, poet, and literary patron who defeated the Cholas, Chalukyas, and Chedis before losing his life to Taila II. — `GAN` · `PAT-INS` `[established]`
- She restored an ancient temple of the sun (Bhanu) in that locality, and excavated there a tank in Sam 1099 = 1042 A. D. The inscription was composed by the Brahman Matrsarman, son of Hari. — `GAN` `[single-source]`
- The sanctum enshrine a large *Shivalinga* covered in a historic brass face plate presented in 1775 A.D. by Khande Rao Appaji (a general of Mahadji Scindia). — `GAZ-VID` · `PAT-INS` `[established]`
- Udayāditya (c.A.D.1070-c.A.D.1093), who became the Paramāra king after Jayasimha's tragic end in the war against Someśvara II of the Western Cālukya dynasty, was an able general. — `ADH` `[single-source]`
- Udayaditya is represented as the son of the last; and he is distinctly stated to have been ruling in Sam 1116, or Saka 981. — `GAN` `[single-source]`
- In yet another inscription of the Udaipur temple itself, the date Vikram Samvat 1116 and Shak Samvat 981 is inscribed. — `TIW-E` `[single-source]`
- The exterior walls are covered in multi-figured relief carvings of the Hindu Pantheon (Brahma, Vishnu, Ganesha, Kartikeya, and Durga), with Shaiva forms predominating. — `PAT-INS` `[single-source]`
- The second was the daughter of Sidh Raj Jesingh Dev (Jayasimha Siddharaja), the king of Gujarat, and the third was a princess of the house of Raja Phool of Bhojnagar. — `GAN` `[single-source]`
- THE JAINAD STONE INSCRIPTION OF JAGADDEVA The stone slab containing the inscription is lying in the court-yard of a temple in the village of Jainad, six miles from Edalabad in the Nizam's Dominions. — `GAN` `[single-source]`
- When King Udayaditya laid the foundation for the city of Udaypur and Udayeshwar, also known as Neelkantheshwar Temple, in the 11th century CE, it is also mentioned in the Udaypur Prashasti that he built a lake called Udaysagar. — `INT-GEO` `[single-source]`
- The misfortune of the Paramāras continued to grow before it assumed serious proportion when Naravarmana (c.A.D. 1093, 1134) came to power. — `ADH` `[single-source]`
- In Samvat 1077 (1020) King Bhoj's son Viranarayana founded Sevana. — `RAJ-E` `[single-source]`
- The 2 large water bodies relevant to Udaypur are the Udaysagar Talab, built by Udaya Aditya in 1059 CE, and the Bhujariya Talab, which existed before his time. — `INT-GEO` `[single-source]`
- The first was the daughter of Raja Raj, the Dâk Chowra king of Took-Toda, which, since Raja Raj himself was blind, had been under the regency of his son Beerj (Virya). — `GAN` `[single-source]`
- An inscription, dated 1077 A. D., from Shikarpur Taluq, records that "he was the source of a great fever of terror to the king of Dhara," These reverses, however did not materially disturb the peaceful continuance of the Paramara rule. — `GAN` `[single-source]`
- The Candella Madanavarman made a grant of land in 1134 A. D., while residing in Bhaillasvami.* Sallaksanavarman entered into hostilities with Naravarman and won a victory over him. — `GAN` `[single-source]`
- Naravarman also had great veneration for the Jaina teacher, Vallabha, at whose feet he is said to have bowed down his head.2 Jainism found a new life in Gujarat under the patronage of the Caulukya Kumarapala (1145-1172 A. D.). — `GAN` `[single-source]`
- Barely represented in this bucket, so anything resting on them is a thin reed: `PAR`, `RAJM`, `SIN-T` — `[gap]`

### C6.1 — paramara, bhoja, inscription, dated, reign

> Jug Dev could not have ruled for fifty-two years, since Udayaditya's second son, Naravarman, began his reign some time before 1094 A. D. According to the early Jaina Chroniclers, Jayasimha-Siddharaja ascended the throne in 1094 A. D. If this is true, and as there is no valid reason for disbelieving it, he could not have been a contemporary of Udayaditya. But notwithstanding these discrepancies, it cannot be denied that Udayaditya had a son named Jagaddeva, who, for some time,…
> — **GAN** · *History of the Paramāra Dynasty* · p. 54 · `ganguly-paramara-00299`

> 2. THE JAINAD STONE INSCRIPTION OF JAGADDEVA The stone slab containing the inscription is lying in the court-yard of a temple in the village of Jainad, six miles from Edalabad in the Nizam's Dominions. This is a record of the reign of the king Jagaddeva. It registers that Padmavatî, the wife of Lolarka, a chief under the king Jagaddeva, founded a temple of Nimvaditya in the agrahāra. Lolarka was the son of Gunaraja and the grand-son of Mahendu. They belong to the Dâhima famil…
> — **GAN** · *History of the Paramāra Dynasty* · p. 102 · `ganguly-paramara-00778`

> Narasimha and Jayasimha were sons of Gayakarna and Alhaņa Devî.² Udayaditya closed his reign shortly after 1086 A. D.3 The tradition runs that Jug Deb was his immediate successor to the throne, but a contemporary Paramâra record states that Laksmadeva became king of Malwa after Udayaditya's death. Jagaddeva's name is not mentioned in any Paramara inscription. But that he ruled in Malwa for some years, about this time, is borne out by the two Hoysala inscriptions referred to a…
> — **GAN** · *History of the Paramāra Dynasty* · p. 56 · `ganguly-paramara-00303`

> 158 HISTORY OF THE PARAMARA DYNASTY Laksmadeva closed his reign some time before 1094 A. D., and was succeeded by his younger brother Naravarman. NARAVARMAN. Naravarman assumed the epithet of NirvanaNârâyaņa, Six inscriptions of his reign have so far been discovered. (i) A slab of stone containing an inscription was found near a tank, situated about a mile to the south of Udayapur, in the Bhilsa District. It records the construction of a tank in V. S. $1151=1094$ A. D., when …
> — **GAN** · *History of the Paramāra Dynasty* · p. 72 · `ganguly-paramara-00339`

### C6.2 — created, having, deserves, create, norm

> Of that same the eighteenth part when may there be in height as more elevated the 1. Monier Williams Dictionary, p. 466. 2. GOSE, p. 158 verse 50 fn. 1 has दण्डं for दण्डत्र्यंशेन । Udaya (may be an equivalent of Chadya) the utensil keeping room named Tilaka the belauded one in the architectural structuring (lit. the house building work). द्वाभ्यामुच्चतरः पूर्वो मण्डलः कुमुदस्त्रिभिः। अभित्तिस्थे (स्थं) भवेच्छाद्ये (द्यं) चन्द्ररेखाविभूषितम् ।।५ ३।। The first one Mandala may …
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. SAMARĀNGANA-SŪTRADHĀRA > THE CORE MATHEMATICAL REVENUE FRACTIONS (*ĀYA*) > The Golden Rule of Siting Balances · `samarangana-00311`

> स्कन्धावारनिवेशेषु पुरग्रामनिवेशने। देवालयक्षितिपवेश्मनिवेशनेषु प्रोक्तान् बलीन् प्रवितरेत् प्रयतः सुरेभ्यः । प्रारम्भमन्यमपि वास्तुगतं चिकीर्षुः कुर्वन्निमं विधिमभीप्सितभाजनं स्यात् ।। २८।। In the establishments of the army camp and in founding down of town, village (and the city), and in foundations of the temples, the palaces of kings, one may allocate offerings, the disciplined one, for the gods. And desirous of other allied foundation laying also, dealing with Architectu…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 35: The Rite named the laying of Foundation Stones · `samarangana-00531`

> SAMARĀNGAŅA-SŪTRADHĀRA of Mahārājādhirāja Śrī Bhojadeva Paramāra The foundation of shrines एवं नृपस्य प्रासादे कृते क्लृप्तेऽथवा भुवि। तस्यानुजीविनः कुर्युः प्रासादान् परिधौ यदि ।।१।। This way the palace of the king having been built or well laid on the ground, if his entourage may create abodes on the surrounding premises or periphery. तदा दिग्भागविन्यासस्थानमानान्यनुक्रमात्। तेषामिहाभिधीयन्ते सर्वेषां वृद्धिहेतवे ।।२।।
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. CHAPTER 51 · `samarangana-00772`

> breadth of the mansion or temple. And from the personal breadth of the Mandapa or hall or pavilion, the ground may be two fold on the outer side. कर्णप्रासादकाः कार्याः प्रासादस्यार्थतोऽपि वा। तेषामध्यर्धतः कुर्याद् वलभीनां निवेशनम् ।।११५ ।। The Karņa Prasadakas (or sidereal chambers) deserve to be created from half the dimension of the Prāsāda and from their additional or one and half extent one¹ may create the establishment of halls. अनेन क्रमयोगेन बाह्याद् वाह्यं सुसंवृतम्…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. CHAPTER 54 · `samarangana-00843`

### C6.6 — devas, goddess, thus, linga, form

> B. LAKULISA R. G. Bhandarkar regards LakulTsa as the founder of the Pasupata school ^ Bagchi suggests, “Lakullsa” was probably Srikantha’s disciple and that these two were responsible for the foundation of Pasupata religion.^ But Lakulisa does not seem to be an immediate disciple of Srskantha, because the accounts of Srikantha and Lakulisa available through literature and inscriptions do not represent them as teacher and disciple. Moreover, in the Agama quoted by Abhinavagupt…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00448`

> Commissioner Office Directorate of Archaeology, Archaic and Museum Bhopal (M.P.) Reference Library Acc. No. 2182...1218... style, before it achieved its distinctiveness, are unfortunately not present. In Nīlakantheśvara, temple at Udaypur (Vidya District). This temple emerges before us embodying all the characteristic features of the Bhūmija temple architecture in its fully developed form. The construction of this saptaratha and saptabhūma temple is known from its dedicatory …
> — **ADH** · *Some Paramāra Temples From Madhya Pradesh: A Case Study of Village Un* · p. 14 · `adhikari-2013-un-00071`

> who had four disciples (i) Akshapada, the founder of Nyaya School (ii) Kanada, the founder of Vaiseshika School (iii) Uluka, a teacher of logic, someiimcs identified with Kanada and tiv) Vat'^a.^ The Prabhiisa Palana inseription records that Soma had constructed a golden temple of Somanafha at Prabhasa and after originating his cult at the instance of Siva gave the place to the Piisupatas - During this period, Somasiddhanta was prevalent in Nepal and Gujarat. The Umfi-Sahita-…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00460`

> ``` +----------------------------------------------------------------------------+ | CHRONOLOGICAL TIMELINE OF THE UN TEMPLE CLUSTER | +----------------------------------------------------------------------------+ | 1. Chaubara Dera No. 1 | c. 1000-1055 A.D. | Peak of King Bhoja's reign. | | | | Circular-stellate Bhumija. | +--------------------------+-------------------+-----------------------------+ | 2. Mahākāleśvara No. 2 | c. 1030-1060 A.D. | Built slightly later; matchi…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00119`

### C6.3 — udaipur, udayaditya, udaypur, temple, heritage

> The water body is situated in the outskirts of the village at GPS 23.54.46.45 N and 78.3.28.85 E. The kingdom of Udaypur is said to have been a region abundant in water. This structure is located in khasra no. 427 with an area of 1.71 hectares. It is currently in government ownership. The locals recall that Udaypur had water from “chap- pan baoli, bawan kue aur saadhe baarah talab” (56 stepwells, 52 wells and 12 and a half lakes) and the Udaysagar is one of these lakes. The U…
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 91 · `intach-2022-udaypur-00309`

> Bhujariya Talab is a natural water body located to the southeast of the village Udaypur. This large water reservoir is located on the outskirts of the village near a live stone quarry covering an area of 8.04 acres. This talab is one of the "chappan baoli, bavan kuae and saadhe barah talab", or 56 stepwells, 52 wells and 12 and half lakes, according to the locals. When King Udayaditya laid the foundation for the city of Udaypur and Udayeshwar, also known as Neelkantheshwar Te…
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 49 · `intach-geoheritage-00214`

> One of the many old Sanskrit inscriptions on this temple records that the Paramara king Udayaditya of Malwa founded a town, built a temple of Shiva, and excavated a tank, designating all three works after his own name as Udayapura, Udayeshvara, and Udayasamudra respectively. The temple is the present monument, and the ruins of the tank Udayasamudra are seen a short distance to the north-east of the town. Two other inscriptions on this temple record that construction commenced…
> — **PAT-CH** · *The Cultural Heritage of Madhya Bharat* · p. — · `patil-1952-00382`

> Figure 202: Aerial view of Udayasagar The Udaysagar is said to cover an area of 1km x 1km. Currently, the steps of the only western bank can be seen which run for approximately 800m. The farmers now use the bed of the lake for agriculture. Only a flight of 12 steps is visible. The steps are made in dressed stones of rectangular slabs. The rectangular slabs also carry repetitive mason marks. The steps are in a dilapidated state in parts of the bank and need maintenance and saf…
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 91 · `intach-2022-udaypur-00311`

### C6.5 — bhoj, town, architecture, king, period

> A premier archeological town located 4 miles east of Bareth station. * **The Udayeshvara (Nilkantheshvara) Temple:** The absolute masterpiece of the *Bhumija* style of temple architecture in India, built entirely of red sandstone. Contemporary Sanskrit inscriptions on its porches record that it was founded by the Paramara King **Udayaditya**; construction commenced in **1059 A.D.** (*V.S. 1116*) and the flagstaff was hoisted in **1080 A.D.** (*V.S. 1137*). The temple stands i…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00084`

> Look at shloka 32 of the Nagpur Prashasti of Narvarman, the successor of Udayaditya— > **तस्मिन्वामसव व(ब)न्धुतामुपगते राज्ये च कुल्याकुले भगनस्वामिनि तस्य** > **व(ब)न्धुरुदयादित्यो भवद्भूपतिः ।** > **येनोद्भूत्य महार्णवोपममिलत्कर्णाट कर्ण प्रभृत्युर्वीपालकदर्शिता भूमिमा** > **श्रीमद्वराहपतिः ॥ 32 ॥** > > *[Sanskrit as in source; the OCR contains numerous errors.]* > > That is — "On that one's (Bhojdev's) attaining the kinship of Indra (i.e., passing away), and the kinsmen (*…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00491`

> **Saarthak Singh** This paper presents a newly-discovered inscription from Udaypur (district Vidisha, Madhya Pradesh). Engraved on a rectangular sandstone slab in the parapet wall of the Udayeśvara temple, this inscription features a serpent's knotted body comprising letters of the Sanskrit alphabet along with the grammatical endings of nouns and verbs. It is accompanied by 5 lines of writing on one side that refer to the diagram as *varṇnanāgakṛpāṇikā,a* "serpentine scimitar…
> — **SIN-S** · *A serpentine scimitar of letters from Udaypur, district Vidisha, M.P.* · p. — · `singh-serpentine-00000`

> In the Jainad writing, Jagdev wrote King Udayadity as his father and King Bhojdev as [his] uncle (*pitrivya*), whereas in the Dongargaon inscription Jagdev has written his father Udayadity as Bhojdev's 'brother' (*bhrata*). Jagdev was the third and youngest prince of his father Udayadity (as his inscriptions tell us). Older than him were two brothers, Lakshmadeva and Narvarman.
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00497`

### C6.4 — iast, aura, haiṃ, para, rājā

> *[IAST] gujarāta kā vastupāla svayaṃ ko laghu bhojarāja tathā bhoja ke samāna rājamārtaṇḍa aura sarasvatīkaṇṭhābharaṇa kahalānā pasanda karatā thā| use samarāṃgaṇa praṇayī bhī kahā gayā hai| rājā bhoja mahārājādhirāja parameśvara to thā hī kyoṃki usake granthoṃ se bhī jñāta hotā hai ki usake adhīnastha bāraha rājā the| yaha upādhi usake tāmrapatroṃ, śilālekhoṃ tathā granthoṃ kī puṣpikāoṃ meṃ prāpta hotī hai| mālavamaṇḍana, mālavādhīśa, mālavacakravartī, sārvabhauma, avantināy…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 15 · `bhojdev-hi-00077`

> क्षीरस्वामी, सायण और महीप ने उसे वैयाकरण तथा *[IAST] isake paryāpta pramāṇa haiṃ ki rājā bhoja vidvānoṃ kā apratima āśrayadātā thā, anokhā kāvyarasika thā tathā adbhuta akādemika pratibhā kā dhanī thā| parantu svayaṃ bhoja kā ina kṣetroṃ meṃ racanātmaka yogadāna rahā athavā nahīṃ? isakā uttara rājā bhoja ke vividha viṣayaka upalabdha aura jñāta grantha sakārātmaka rūpa se de rahe haiṃ| sarasvatīkaṇṭhābharaṇa ke ṭīkākāra ajar̤a ke anusāra bhoja ne svayaṃ caurāsī grantha race t…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 12 · `bhojdev-hi-00060`

> *[IAST] śṛṃgāramaṃjarīkathā meṃ ina snehī rājāoṃ (praṇayibhiḥ nṛpatibhiḥ) kī bhojagoṣṭhī meṃ bhī upasthiti batāyī gayī hai| saikar̤oṃ rājā usake adhīna the| yaha bhoja kī racanāoṃ se jñāta hotā hai| spaṣṭa hī ve racanāe~ isa samarāṃgaṇasūtradhāra se bāda kī haiṃ| vaise vidiśā se bhopāla kṣetra meṃ bārahavīṃ śatī meṃ 'mahādvādaśakamaṇḍala' thā| parantu vaha eka hī maṇḍala kā nāma thā| dhāra jile kā baramaṇḍala kasbā bhī aise hī prācīna maṇḍala kā nāmāvaśeṣa pratīta hotā hai| a…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 4 · `bhojdev-hi-00020`

> सूत्रधारमहिरसुतमणथलेणघटितं । विस्वेलिकसिवदेवेनलिखितमिति । संवत् 1091 *[IAST] sūtradhāramahirasutamaṇathaleṇaghaṭitaṃ | visvelikasivadevenalikhitamiti | saṃvat 1091* इस लेख के कुछ अक्षर अस्पष्ट होने से श्लोक पूरा स्पष्ट नहीं हो पाता है। तब भी जो अंश स्पष्ट है उससे यह तो ज्ञात हो ही जाता है कि यह लेख संवत् 1091 या 1034 ई. में लिखा गया। राजा भोज की नगरी (धारा) की विद्याधरी (विद्या धारण करने वाली) अप्सरासी जो शाम्भवी (शक्ति संपन्न) है। जो स्मरण करता है उसे सुख प्राप्त होता है। मा…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 7 · `bhojdev-hi-00036`

**Gaps.** barely represented here: `PAR`, `RAJM`, `SIN-T`.

## C7 — Udayeśvara in Stone: Architecture, Sculpture and Iconography

[↑ contents](#contents)

**Coverage.** 4,197 chunks from 23 sources (`ADH`, `BHJ-H`, `DEV`, `GAN`, `GAZ-VID`, `GUP`, `HAR`, `INT-ARC`, `INT-GEO`, `KRAM-1`, `KRAM-2`, `PAN`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `SAM`, `SIN-B`, `SIN-S`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: secondary_comparative 1689, primary_authorial_paramara 789, secondary_core 745, primary_scriptural 337, reference_tertiary 330, field_observation_survey 180, field_observation_reportage 61, primary_epigraphic 54, contextual_thematic 12. The largest single contributor is `SAM` with 789 chunks (19% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- Contemporary Sanskrit inscriptions on its porches record that it was founded by the Paramara King **Udayaditya**; construction commenced in **1059 A.D.** (*V.S. 1116*) and the flagstaff was hoisted in **1080 A.D.** (*V.S. 1137*). — `HAR` · `PAT-CH` · `PAT-INS` `[established]`
- One of them contains the date V. S. 1182 or 1192 = 1125 or 1135 A. D. A small fane, dedicated to Siva, lies to the north of the main temple, the mandapa and front porch of which are now in ruins. — `GAN` `[single-source]`
- From the West; Udayapur, Gwalior; built by the Paramāra King Udayāditya (c. 1059-1087 A.D.); Red sandstone. — `KRAM-2` `[single-source]`
- I and III), 954 A.D. ↑ Vedibandha ↑ Adhiṣṭhāna Profile of socle and lowermost part of wall*, Nilakanthesvara Temple, Udayapur, Gwalior (cf. Pl. XLIII), 1059-1080 A.D. — `KRAM-1` `[single-source]`
- The sanctum enshrine a large *Shivalinga* covered in a historic brass face plate presented in 1775 A.D. by Khande Rao Appaji (a general of Mahadji Scindia). — `PAT-INS` `[single-source]`
- Through the southern direction of Himalaya, surrounded by the salt ocean from the other side [cite: 846, 847], is the Varșa named "Bhārata", the very primeval one, having the shape of an arc or bow [cite: 848, 851]. — `SAM` `[single-source]`
- The last, known as the temple of Nilakantheshwara or Udayeshwara after its royal author Udayaditya, is the grandest specimen of Paramara architecture and was started in 1059 and completed in 1080. — `ADH` · `DEV` `[established]`
- THE KARNATA DRAVIDA TRADITION CONTINUED 229 25.16 Ishvara temple, Arsikere, 1220 stellate shrine (vimana), semi-stellate closed hall (gudha-mandapa) and stellate open hall (ranga-mandapa). — `HAR` `[single-source]`
- Uttare£vara Index PURANA m B ook V: AVANTYAKHANDA S ection II: CATURASITI-LINGA-MAh ATMYA GLORIFICATION OF EIGHTYFOUR LINGA SHRINES IN AVANTl1 CHAPTER ONE Agastyesvara2 + _ + Obeisance to Sri Ganesa. — `SKP-13` `[single-source]`
- A short votive inscription on the pedestal of the left image states it was dedicated by the Jain Acharya **Yashakirti**, dated in **1206 A.D.** (*V.S. 1263*). — `PAT-INS` · `PAT-TEM` `[established]`
- For Siva-Mahadeva, we get the names Kedara, Ramesvara, Somanatha, Supdira, Kala, Rudra, DhaneSvara, Amaresvara, Udayesvara, Ballalesvara, Samidhes- vara, Ekalladeva, etc. — `SIN-B` `[single-source]`
- The great Nilakantheśvara temple at Udayapur was built by Udayaditya in Sam 1116 = 1059 A. D. An ART AND CULTURE 259 inscription of the sixteenth century A. D. describes it as the most beautiful temple in India. — `GAN` `[single-source]`
- They have been taken to represent the 'Kadamba Style' (Moraes, 'The Kadamba Kula', Part VII); temples of this kind are also in Aihole (Cousens, 'The Chālukya Architecture', Pl. XXV; temples of Galagnāth and Nos. — `KRAM-1` `[single-source]`
- SCULPTURES BETWEEN THE SOUTH KAPILĪ AND SOUTH LATĀ (pl. 80) The sculptures in the khattakas between the south kapilī and south latā are of Śiva, Gaṇeśa and Gaṇeśāṇī (pl. 80). — `PAN` `[single-source]`
- She restored an ancient temple of the sun (Bhanu) in that locality, and excavated there a tank in Sam 1099 = 1042 A. D. The inscription was composed by the Brahman Matrsarman, son of Hari. — `GAN` `[single-source]`
- Śiva having a Kirttimukha in the Jaṭāmukuṭa, see Daśavatāra cave, Elura; a Kirttimukha figures also in the Karaṇḍamukuṭa of a Dvārapāla from South India, Coomaraswamy, ‘Yakṣas’, I. — `KRAM-2` `[single-source]`
- The exterior walls are covered in multi-figured relief carvings of the Hindu Pantheon (Brahma, Vishnu, Ganesha, Kartikeya, and Durga), with Shaiva forms predominating. — `PAT-INS` `[single-source]`
- The story of the architectural development is carried forward by the Trinetreshwara Temple near Than (District Surendranagar) since demolished, and the Shiva Temple at Kerakot and the Sun Temple at Kotai in Kutch, dating from c. 950. — `DEV` `[single-source]`

### C7.6 — garbhagṛha, temple, sikhara, superstructure, prāsāda

> containing exquisitely sculpted images of Śiva and other divinities (pl. 11). At the base of each of the other three latās, i.e. on the north, south and west, there is a prominent sculpted medallion within a large caitya window, viz. śūrasenaka (pl. 1). In between each latā are seven bhūmis of five kūṭastambhas in each sub-quarter (pl. 1). While the ubiquitous motif of the latā is the gavākṣa, the basic motif of the sub-quarters of the śikhara is the kūṭastambha or a miniatur…
> — **PAN** · *The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta* · p. 14 · `pande-udayesvara-00166`

> Pl. 3. View of one of the eight subsidiary shrines surrounding the main temple. Pl. 4. View of Śaiva pratihāras flanking the eastern entrance. Pl. 5. View of the śikhara and garbhagṛha showing its stellate-cum-circular plan.
> — **PAN** · *The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta* · p. 12 · `pande-udayesvara-00164`

> The Uttareśvar temple at Bhuvaneśvar, whose Maṇḍapa and Prāsāda were planned and set up at the same time and are contemporary with the Paraśurāmeśvar temple shows the problem which confronted the Sthapati.⁴⁸ A century or more had to pass before he arrived at the perfect solutions showing the Prāsāda as the main building and temple proper, with the Maṇḍapa as the lesser part of the sacred structure, following its rhythm in the particularities of its own form. In Orissan temple…
> — **KRAM-1** · *The Hindu Temple, Volume I* · p. 267 · `kramrisch-1946-v1-01398`

> The Nilakaṇṭheśvara temple shows the themes of its perpendicular walls continued on the curvilinear Sikhara. The close correspondence of the structure and superstructure of the temple brought about by the theme of the pillar is however not particular only to the Nilakaṇṭheśvara temple at Udayapur, Gwalior; nor to 'star shaped' Prāsādas in general. Temples with orthogonal buttresses are similarly ordered,* the composition moreover follows the same vision whether the temples be…
> — **KRAM-2** · *The Hindu Temple, Volume II* · p. 104 · `kramrisch-1946-v2-00531`

### C7.1 — created, having, deserves, create, norm

> (शतपत्रा ?) कपोताली सार्धभागं समुच्छ्रिता ।।९।। Two parted Vedikābandha and Jangha deserves to be created as four parted one. A hundred petalled is the Kapotalī³ elevated by a part and a half. 1. दिग्भद्रलक्षणम् fn.6, p.500, verse 4. 2. A moulding of the entablature (EOHНА, р.339). 3. Cyma recta cornice moulding, PS., p.148. सार्धभागसमुच्छ्राया कार्या प्रथमभूमिका। द्वितीया भूमिका ज्ञेया सार्धभागत्रयोदया।।१०।। The first storey deserves to be created as having elevation of a pa…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra > Architectural Treatise of Mahārājādhirāja Śrī Bhojadeva > [Original Page Source: 14] · `samarangana-01170`

> स्थानेषु शूरसेना पुरोरेखात्रयं भवेत्। शुकनासां च घण्टां च स्कन्धं शिखरमेव च ।।१९१।। In spots proper may be Śūrasenas and in front may be the rekha triad and Sukanāsā and ghanţă Skandha and Sikhara. कूटा+स्तम्भिका कुम्भं पूर्ववत् परिकल्पयेत्। य इमं कारयेद् धन्यः प्रासादं मण्डनं भुवः॥१९२॥ Kūță may be Stambhikā and Kumbha one may create as of earlier norm. All the blessed one may create this Prāsāda, the ornament of the Earth. विद्याधराधिपः श्रीमान् स भवेन्नात्र संशयः। भुङ्गे च …
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra > Architectural Treatise of Mahārājādhirāja Śrī Bhojadeva > [Original Page Source: 14] · `samarangana-01240`

> remaining as per talked of earlier. This way may be the Padmaka Stambha a lotus like pillar by the reasonable fundamental forms of suitable norm. 1. The various parts surrounding the doorway or windows or moulding round exterior of arch p. 59. The Concise Oxford Dictionary, fifth edition revised by I. Macintosh Oxford at the Clarendon Press, 1964. 2. Dr. Ajay Mitra Sastri in IASITBSOVM p. 380, 381 has referred to the eight components of a pillar i.e. Vahana, ghața, padma, Utt…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. SAMARĀNGANA-SŪTRADHĀRA > THE CORE MATHEMATICAL REVENUE FRACTIONS (*ĀYA*) > The Golden Rule of Siting Balances · `samarangana-00305`

> यथा सिंहासनं राज्ञां शोभते मणिदीप्तिभिः ॥४७॥ On the pithas of the Prāsādas for fascination the skilled one may create the way the lion seat of the kings gleam forth by bejeweled lamps. तथा प्रासादराजस्य पीठं कर्मभिरुत्तमैः। पट्टस्योर्ध्वं विधातव्यमुत्कृष्टं राजसेनकम्।।४८॥ That very way of the Prāsādarāja may be Pitha by excellent structuring norms. Above pațța deserves to be created the excellent Rājasenakas. पुष्पितैः कमलैर्युक्तं शोभितं भारपुत्रकैः । तदर्धं वेदिका देया नाना…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra > Architectural Treatise of Mahārājādhirāja Śrī Bhojadeva > [Original Page Source: 14] · `samarangana-01299`

### C7.5 — śiva, hands, right, left, lotus

> The Paramāras of Vāgaḍa seem to have depicted Cāmuṇḍā as the deity in the northern quarters. She is depicted in the northern *khattakas* in the Maṇḍaleśvara temple, Panaheda as also the Śiva temple, nos. 1, 2, 3 at Arthuna and shrine no. 9 of Nīlakaṇṭha Mahādeva at Arthuna.⁶⁸ It is interesting that at the Udayeśvara temple, too, the prominent depictions of Cāmuṇḍā may be seen in the northern quarter, for eg., the above mentioned sculpture and another major sculpture depicted …
> — **PAN** · *The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta* · p. 54 · `pande-udayesvara-00280`

> ARCHITECTURE AND SCULPTURE OF THE UDAYEŚVARA TEMPLE | 65 Pl. 93. View of buttresses between the west *latā* and north *latā* of the *garbhagṛha*. bearded and wears heavy *kuṇḍalas*. He holds a ladle in his upper right hand and a book in his upper left hand. His lower left arm is around Brahmāṇi. The attribute in his lower right hand is not
> — **PAN** · *The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta* · p. 66 · `pande-udayesvara-00324`

> The sculpture shown in (Figure 237) is of Lord Shiva and Goddess Figure 237: Sculpture showing Uma Maheshwara 2 Parvati. The figures are carved in sitting position over a plain rock with a decorative back panel. This kind of sculpture is also known as Uma-Maheshwara sculpture where Uma is used to symbolize the mother of this Universe and Maheshwara is the supreme god.
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 105 · `intach-2022-udaypur-00372`

> It is interesting to note that the Nilakantheśvara is adorned with Śaiva, Śiśāra and Vaśnava images. However the repetition of the image of various forms of Śiva on it is in keeping with the Śaiva affiliation of the temple. Among the images embellishing the Nilakantheśvara, several may be found needed by the miniature niches of the kumbha moulding of the vedībandha. They include Śiva, Ganeśa, Vāmana incarnation of Viṣṇa, Kubera and Devi on her buffalo mount. In the southern s…
> — **ADH** · *Some Paramāra Temples From Madhya Pradesh: A Case Study of Village Un* · p. 31 · `adhikari-2013-un-00389`

### C7.3 — century, temple, temples, found, india

> 33. Ravan Tol Chaturbhuji Shiva Murti It is located on the outskirts of Udaypur to the east at GPS 23.53.16.8 N and 78.03.14.8 E. The structure is an unestablished 8.2 meters in length and 4.2 meters in width long sculpture of Shiva in the dancing form. Nataraj on apusmāra, a dwarf who represents spiritual ignorance and nonsensical speech. An incomplete structure with stone pillars is also located near the sculpture. It is believed that Raja Udayaditya had planned to build an…
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 79 · `intach-2022-udaypur-00276`

> ``` +----------------------------------------------------------------------------+ | CHRONOLOGICAL TIMELINE OF THE UN TEMPLE CLUSTER | +----------------------------------------------------------------------------+ | 1. Chaubara Dera No. 1 | c. 1000-1055 A.D. | Peak of King Bhoja's reign. | | | | Circular-stellate Bhumija. | +--------------------------+-------------------+-----------------------------+ | 2. Mahākāleśvara No. 2 | c. 1030-1060 A.D. | Built slightly later; matchi…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00119`

> $^{74}$ Cousens, 'Mediaeval Temples of the Dakhan' op. cit. Plates, passim. Essentially however there is no difference in type between a temple like the Nilakanṭheśvara at Udayapur of the 11th century (Gwalior; Pl. XLIII) and the temple at Jhodga, Nasik (Cousens, ib. Pl. LIII), although in plan the Udayapur temple is stellate, of the 'Bhūmija' variety (S.S. LXV), its buttresses and vertical rows of Sṛṅgas being placed on edge, and not parallel with the main buttresses. Kūtas …
> — **KRAM-1** · *The Hindu Temple, Volume I* · p. 229 · `kramrisch-1946-v1-01228`

> PLAN OF NĪLAKAṆṬHEŚVARA TEMPLE (1059—1080 A.D.). Udayapur, Gowalior (Pls. LII—III). from Cunningham, ASR, vol. VII. Pl. VI. The very substantial walls of this stellate Nirandhāra temple extend from its perimeter to the Garbhagṛha and Mahāmaṇḍapa, etc. as outlined in the plan. In this type of temple, the buttresses project radiately, and not axially, as usual.
> — **KRAM-1** · *The Hindu Temple, Volume I* · p. 269 · `kramrisch-1946-v1-01409`

### C7.2 — shikhara, sanctum, temple, temples, plan

> A large *pañcabhūma* *pañcaratha* circular-stellate temple built on the modern ground level near Chaubara Dera No. 1, indicating a later chronological date. * **Structure:** The low plinth basement (*pīṭha*) is fully exposed, showing a sequence of *jadyakumbha*, *karnikā* (knife-edge molding), and *grāsapaṭṭikā* (grotesque lion-face bands). The *shikhara* is partially intact, showing that internally it was divided into four cells of diminishing size built one over another. * …
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00106`

> A rare **pañcaratha orthogonal (caturaśra)** structural temple, facing east. * **Structure:** The original *shikhara* spire has collapsed and was replaced in the 18th century by a plain Maratha brick dome. The plinth and base moldings display sharp, well-preserved linear lines. The *garbhagriha* contains a built-in stone water tank in its northeastern corner for storing ablution water. * **Iconography:** The *jangha* wall contains a single horizontal row of image sculptures r…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00112`

> Situated picturesquely on the bank of the Hathni stream, facing east. * **Structure:** A five-storeyed (*pañcabhūma*) *pañcaratha* circular-stellate structural temple. The *vedībandha* preserves a complete sequence of moldings: *khuraka*, *kumbha*, *antarapatta*, *cippika*, *kalaśa*, *antarapatta*, and *kapotapālikā*. The *shikhara* retains its side quadrants, showing three vertical rows of five *kūṭastambhas* each, though the crowning *amalaka* is missing. The floor of the s…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00105`

> the one with the cluttered replicas of it around (katna). The happy balance between the two lent to the *Bhūmija* temple a charming grace above the *mandavara*. It is in harmonious proportion with the *śikkara*. angled ratha projections between the bhadras. It may be assumed that the Bhūmija temples had a pañacratha plan before the development of their saptaratha drama. In the extant temples of Mālavā, however, both the pañacratha and saptaratha plans occur simultaneously. Th…
> — **ADH** · *Some Paramāra Temples From Madhya Pradesh: A Case Study of Village Un* · p. 13 · `adhikari-2013-un-00065`

### C7.4 — linga, goddess, great, will, devas

> V.ii.24.1-8 seen. The ten quarters shone with thick dense darkness overspreading them. They were delighted with the greatness of the Lord of Devas. The Devas attained great happiness. All those excellent ones appeared as though they imbibed nectar. Thereafter the clouds disappeared reducing the darkness. Cool breezes blew. The ten quarters became calm. The brilliant constellations of pure lustre circumambulated the Moon. The Planets ceased to be malefic. The seas became calme…
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 77 · `skanda-xiii-00150`

> * and mental purity, shall have everlasting celestial residence. By glorifying the Linga one is rid of sins; by seeing the Linga one realizes the good. By touching the Linga the devotee sanctifies his family upto the seventh generation. 31-36. He obtains all the desired things in abundance. When one visits Simhesa, the deity redeeming devotees from the ocean of worldly existence, one becomes liberated from births, old age and miseries. By seeing Sri Simhesvara, one averts the…
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 204 · `skanda-xiii-00421`

> When the great Isvara, the meritorious Mahalayesvara, is adored with great devotion, О blessed one, all the Devas too are worshipped, because he is worshipped by them also. CHAPTER TWENTYFIVE Muktlsvara 1. О my beloved goddess, know that Muktlsvara Linga is the twenty-fifth deity. Merely by seeing it, О Parvati, one gets liberated. 2-8. Formerly in the Rathantara Kalpa, there was an excellent Brahmapa named Mukti. О blessed one, he was a person of consecrated soul with all th…
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 79 · `skanda-xiii-00155`

> By touching that Linga, he (Vadala) became handsome and powerful. He regained his sight and he was able to walk well and hear clearly in an instant. О Parvati, on seeing that great miracle, Manibhadra became delighted. He named the deity after the name of his son. “By the power of this Linga Vadala regained his vision. Hence this deity will be named Vadalesvara from today. It will become well-known in all the three worlds as the bestower of eyes. Those who adore the deity nam…
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 283 · `skanda-xiii-00599`

**Gaps.** no structural gap detected: the bucket is broad and no single source dominates..

## C8 — Words in Stone: Inscriptions, Languages and the Serpentine Scimitar of Letters

[↑ contents](#contents)

**Coverage.** 2,150 chunks from 26 sources (`ADH`, `BET-S`, `BHJ-H`, `DEV`, `GAN`, `GAZ-VID`, `GUP`, `HAR`, `INT-ARC`, `INT-GEO`, `KRAM-1`, `KRAM-2`, `PAN`, `PAR`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `RAJM`, `SAM`, `SIN-B`, `SIN-S`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: secondary_core 765, primary_authorial_paramara 672, secondary_comparative 231, field_observation_reportage 147, reference_tertiary 94, field_observation_survey 86, primary_scriptural 76, primary_epigraphic 60, contextual_thematic 18, environmental_scientific 1. The largest single contributor is `SAM` with 671 chunks (31% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- Contemporary Sanskrit inscriptions on its porches record that it was founded by the Paramara King **Udayaditya**; construction commenced in **1059 A.D.** (*V.S. 1116*) and the flagstaff was hoisted in **1080 A.D.** (*V.S. 1137*). — `ADH` · `GAN` · `KRAM-2` · `PAT-CH` · `PAT-INS` `[established]`
- The plates were found in the possession of a Visnagara Brahmana named Bhatta Magan MotiRam, a resident of the village **Harsōlā** in the Prantija taluka of the Ahmedabad District, Gujarat. — `PAT-INS` `[single-source]`
- In the Bhailasvami Mahadvadashaka province, the provincial governor of Udaipur in 1171 CE was Lunapasaka;² this is clear from the inscription of Vikram Samvat 1229. — `RAJ-E` `[single-source]`
- The decimal date recorded is **Māgha vadi 30, Wednesday, 1005 (Vikrama Samvat)**, which regularly corresponds to **31st January, 949 A.C.** — `PAT-INS` `[single-source]`
- She restored an ancient temple of the sun (Bhanu) in that locality, and excavated there a tank in Sam 1099 = 1042 A. D. The inscription was composed by the Brahman Matrsarman, son of Hari. — `GAN` `[single-source]`
- Both grants were issued by the same king on the same day to two Brahmanas who were related as father and son: **Grant A (No. 1)** to the father, Lallopadhyaya, and **Grant B (No. 2)** to the son, Nina Dikshita. — `PAT-INS` `[single-source]`
- If King Bhoj ruled up to 1055, then subtracting 55 years, 7 months and 3 days from that makes his accession possible around 999 CE. — `RAJ-E` · `SIN-B` `[established]`
- The roof and *shikhara* have collapsed, but historic data (including a 1931 Holkar State plate) shows it originally carried a five-storeyed (*pañcabhūma*) spire. — `PAT-INS` `[single-source]`
- The plates were formally delivered on the **thirteenth day of the dark half of Māgha, V.S. 1043** (**31st December, 986 A.C.**), constituting the latest known epigraphical date for Vakpati Munja's rule. — `PAT-INS` `[single-source]`
- In yet another inscription of the Udaipur temple itself, the date Vikram Samvat 1116 and Shak Samvat 981 is inscribed. — `TIW-E` `[single-source]`
- The inscription features a striking visual composition of serpentine form and isolated letters, known in scholarly literature as nāgabandha or sarpabandha (Salomon 1998, 125-127), along with two short inscriptions on one side. — `SIN-S` `[single-source]`
- The Dharmapariksa was composed in Sam 1070 = 1013 A. D. I Sa jayati Vâkpati-rajaḥ sakalarthi-manorathaika-kalpataruḥ | Pratyarthi bhûta-parthiva-laksmî-hatha-harana-durlalitaḥ Edited by Visvanatha Sâstrî, Calcutta, 1874, (Bibl. — `GAN` `[single-source]`
- King Munjadeo (973-972 CE) on the occasion of a lunar eclipse. — `INT-ARC` `[single-source]`
- On this inscription the date is written as Samvat 1286 (1229 CE), Kartik Sudi ___, Friday. — `TIW-E` `[single-source]`
- The sanctum enshrine a large *Shivalinga* covered in a historic brass face plate presented in 1775 A.D. by Khande Rao Appaji (a general of Mahadji Scindia). — `PAT-INS` `[single-source]`
- Engraved by (silavata) mason Suvi of Gaurajation Samvat 1698 Chaitravadi 11. — `INT-GEO` `[single-source]`
- The misfortune of the Paramāras continued to grow before it assumed serious proportion when Naravarmana (c.A.D. 1093, 1134) came to power. — `ADH` `[single-source]`
- Sanskrit English Dictionary, V.S. Apte, for 505 on Vāstu, also MW, p.948. — `SAM` `[single-source]`
- Barely represented in this bucket, so anything resting on them is a thin reed: `BET-S` — `[gap]`

### C8.6 — having, created, deserves, create, norm

> ``` # Samarāṅgaṇa-sūtradhāra ## Architectural Treatise of Mahārājādhirāja Śrī Bhojadeva ### English Translation with Sanskrit Typology Matrix ### [Original Page Source: 1] #### **Chapter 57** #### **CHAPTER 57** #### **A twenty counting of Meru and others** **Sanskrit (Śloka):** `अथान्यान् कथयिष्यामः समासात् सूक्ष्मलक्षणान्।` **Sanskrit (Śloka):** `पञ्चाशतमिहोत्कृष्टान् प्रासादाञ् श्रीधरादिकान् ।।१।।` **English Translation:** *Now we shall talk of others having minuter pre-re…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 56: The Illustration of Sixty-Four Prāsādas Headed by Rucaka > 4. Deity Placement and Architectural Vulnerabilities (*Marmavedha*) > Avoiding Vulnerable · `samarangana-00863`

> **Sanskrit (Śloka):** `हस्तिमुण्डैः समाकीर्णमध (प्स) रोगणभूषितम्।` **Sanskrit (Śloka):** `ईदृशं श्रीधरं कुर्यात् सर्वालङ्कारभूषितम् ।।४७।।` **English Translation:** *Overspread by elephant crests and decorated by the bevy of nymphs, such a one* Śrīdhara one may create adorned by all the ornaments or decorations. **Sanskrit (Śloka):** `श्रीधरं कारयेद् यस्तु किर्त्यर्थमपि मानवः।` **Sanskrit (Śloka):** `इहैव लभते (वसतः ?) सौख्यममुत्रेन्द्रत्वमाप्नुयात् ।।४८।।` **English Translat…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 56: The Illustration of Sixty-Four Prāsādas Headed by Rucaka > 4. Deity Placement and Architectural Vulnerabilities (*Marmavedha*) > Avoiding Vulnerable · `samarangana-00873`

> ### [Original Page Source: 12] #### **Samarāṅgaṇa-sūtradhāra** **Sanskrit (Śloka):** `ग्रीवा सार्धपदा प्रोक्तो (क्ता) विस्तारादष्टभागिका(:?)||` **Sanskrit (Śloka):** `अण्डकं द्विपदोत्सेधमेकादशपदायतम्||८४||` **English Translation:** *Griva is spoken of as of one and a half parts octagonal digited one as compared with the* breadth and Aṇḍaka as of two digited elevation. **Sanskrit (Śloka):** `दण्डिका सार्धभागो च(च्चा)विस्तारा न(त्र)वभागिका।` **Sanskrit (Śloka):** `त्रिपदः कलशः …
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 56: The Illustration of Sixty-Four Prāsādas Headed by Rucaka > 4. Deity Placement and Architectural Vulnerabilities (*Marmavedha*) > Avoiding Vulnerable · `samarangana-00881`

> breadth of the Skandha of that one, may there be by parts two and a half (ardhapañcaka). **Sanskrit (Śloka):** `ग्रीवार्धभागमुत्सेधाद् भागेनामू(म)लसारकम्।` **Sanskrit (Śloka):** `चन्द्रिका चार्थभागेन कलशो भागमुच्छ्रितः।।१३६।।` **English Translation:** *From the elevation, the Amalasāraka may be by a part with a half part of the Grīvā.* Candrikā may be by a half part and Kalaśa elevated by a part. **Sanskrit (Śloka):** `द्वितीया कर्णशृङ्गस्य स्यादूर्ध्वं मूलमञ्जरी।` **Sanskrit…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 56: The Illustration of Sixty-Four Prāsādas Headed by Rucaka > 4. Deity Placement and Architectural Vulnerabilities (*Marmavedha*) > Avoiding Vulnerable · `samarangana-00893`

### C8.2 — inscription, bhoja, dated, king, paramara

> (iii) The Ujjain plate, dated 1021 A. D. 3 The inscription was found by a peasant when ploughing near a small stream called Nagajhari, which is included in the sacred Pañcakroşî of Ujjain. that in Samvat 1078, Magha 1021 A. D., January, Bhoja, having worshipped the lord of Bhavânî, from his residence of Dhara granted the village Virâņaka, situated within the District to the west of Nagadraha, to a Brahman named Dhanapati Bhatta, son of Bhatta Govinda, a Rgvedi Brahman, who wa…
> — **GAN** · *History of the Paramāra Dynasty* · p. — · `ganguly-paramara-00211`

> Even in the dark days of the decline of their power, the Paramara kings did not withdraw their support from ART AND CULTURE 281 those devoted to learning. Bhoja II is said to have been a great patron of poets, like his predecessor of the same name. During the period under review, many educational institutions were established in Malwa for the cultural development of the people. The modern Kamalmaula mosque at Dhara, as we have already noticed, is believed to have been a schoo…
> — **GAN** · *History of the Paramāra Dynasty* · p. 102 · `ganguly-paramara-00603`

> King Munjadeo (973-972 CE) on the occasion of a lunar eclipse. The copper plate mentioned about the grant given at Gunapura by minister Rudraditya$^{19}$ The inscriptions of Banswara and Betma of Bhoja, Udaypur-Prasasti of Udayaditya, Nagpur-Prasasti of Lakshmadeva can be mentioned. The most important of these is the commendation which is engraved on a stone slab of the Neelkantheshwar temple near Bhilsa, Udaypur. 'The knowledge of the history of the Parmar dynasty from vario…
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 20 · `intach-2022-udaypur-00083`

> the temple of Raja-Bhoja himself in Sarfivat 1091 (A.D 1035) exists in the British Museum and its facsimile has been published in Rupam.2 The two pillars bearing the incriptions are among those that support the dome of the prayer hall. The one near the pulpit containing the Sanskrit alphabet faces the east. The other, at a distance from the pulpit to the south, contains the Sanskrit verbal terminations facing the south with two Sanskrit verses incribed over it containing the …
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-01177`

### C8.1 — sanskrit, temple, king, bhoj, structural

> *Inscriptions of the Paramāras of Malwa — Edited by Harihar Vitthal Trivedi (Archaeological Survey of India, New Delhi)* * **On Spelt Names and Epigraphical Terms:** Standardizes the reading of classical terms (e.g., changing *Brahmana* to *Brāhmaṇa*, *evam* to *ēvam*, and *Samvat* to *Samvat*). * **On Plate Interpretation (Page 42, para 2):** Emphasizes that each copper-plate in the early Paramara grants is strictly inscribed on **one side only**, containing approximately fi…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00121`

> These twin copper-plate grants represent the **earliest known epigraphical records** of the Paramāra house of Malwa. They were noticed by D. B. Diskalkar in the *Annual Report of the Watson Museum, Rajkot (1922-23)*, and subsequently edited in the *Epigraphia Indica (Vol. XIX)* jointly with K. N. Dikshit. The plates were found in the possession of a Visnagara Brahmana named Bhatta Magan MotiRam, a resident of the village **Harsōlā** in the Prantija taluka of the Ahmedabad Dis…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00122`

> The largest structural temple at Un, situated within the village habitation area, belonging to the *nirandhara* (lacking internal circumambulatory passage) class, facing east. * **Plan and Elevation:** It features a *pañcaratha* circular-stellate ground plan (*vṛtta* variety) with an inner square *garbhagriha*, fronted by a rectangular *antarala* (vestibule) and a large square *sabhamandapa* with open side balconies (*parsvamandapas*). The roof and *shikhara* have collapsed, …
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00103`

> This single copper plate represents the final half of a separate bilateral charter issued by **Siyaka**. It was obtained around 1920 A.C. by a pleader of Kaira, Gujarat, and presented to Muni Jinavijayaji of the Puratattva Mandir, Ahmedabad (now preserved in the L. D. Institute of Indology). The plate measures 34 cm by 19 cm, featuring two horizontal ring holes and raised rims. The lower right corner displays a human-shaped flying Garuda with wings, holding a hooded snake in …
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00129`

### C8.4 — hands, serpent, lotus, right, temple

> The inscription features a striking visual composition of serpentine form and isolated letters, known in scholarly literature as nāgabandha or sarpabandha (Salomon 1998, 125-127), along with two short inscriptions on one side. The characters are worn off in several places due to the flaking of the sandstone, as seen in the photograph reproduced here, but are fairly well preserved to enable an understanding of the record. The palaeography bears close comparison to local record…
> — **SIN-S** · *A serpentine scimitar of letters from Udaypur, district Vidisha, M.P.* · p. — · `singh-serpentine-00005`

> 1. bhāradvāṃ jīvihitv=ēmāṃ varṇna-nāga-kṛpāṇikāṃ [|] hitvāpāshaṇicāṇālā_ 2. pālaḥ pālayatu gām || 1 || ja°abha The action specified by the imperative verb pālayatu follows a causative construction, having as its agent of causation *–pālaḥ* and its agent of action, *varṇna-nāga-kṛpāṇikāṃ*, giving the following sense: "may the protector cause this serpentine sword of letters to protect..." The object of protection is unclear but the main agent along with its pronoun, *imāṃvarṇn…
> — **SIN-S** · *A serpentine scimitar of letters from Udaypur, district Vidisha, M.P.* · p. — · `singh-serpentine-00010`

> (2nd ed.) pp. 183-87. 4. Hultzch, Parijatamaniari-natika, by Madana, R. I. VIII, pg. 96-122 (rtr) (5it) t:4r 5, J.B.O. Br. Vol. XXI, pp. 350-51. Lifcradirc and Learning 303 is engraved the Sanskrit alphabet in the 'Nagari’ characters of (he lllh and 12th centuries A D. The tail contains the inflectional terminations of nouns and verbs. There are altogether 53 letters and 21 nomin3l and 18 verbal inflectional terminations in it. The second chart is formed by the intertwining o…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00892`

> ⁷⁸ "The temple resembling a mountain shines white." Mandasor (in Lāṭa) Inscr., A.D. 473-74, line 16, 'Indian Antiquary', Vol. XV, p. 196. This temple was consecrated to Sūrya. An inscription from the Lakṣmaṇa Temple, Khajuraho, dated in the Vikrama year 1011, or 954 A.D., praises this temple in verse 42 as a "charming, splendid house of Viṣṇu which rivals the peaks of the mountains of snow"; 'Epigraphia Indica', Vol. I, p. 121.—An inscription of the early 13th century speaks …
> — **KRAM-1** · *The Hindu Temple, Volume I* · p. 134 · `kramrisch-1946-v1-00665`

### C8.3 — inscription, inscriptions, udaypur, temple, udaipur

> Udaypur, varṇṇanāgakṛpāṇikā, Paramāra, Malwa The Śiva temple of Udaypur in the Vidisha district of Madhya Pradesh, also known as Nīlakaṇṭheśvara or Udayeśvara, is a celebrated example of India's medieval architecture, built around 1080 in the novel bhūmija style associated with the Paramāra dynasty of Malwa, c. 972–1305 (Deva 1975). Less well known is its status as an extraordinary epigraphic archive with a continuous sequence of inscriptions in Sanskrit, Persian, and Hindi s…
> — **SIN-S** · *A serpentine scimitar of letters from Udaypur, district Vidisha, M.P.* · p. — · `singh-serpentine-00002`

> - **Fig. 1–2.** Udayeśvara temple at Udaypur, view from the southeast locating the inscription on the parapet wall. - **Fig. (top inscription).** Detail and eye-copy of the short inscription at the top. - **Fig.** Inscription on the parapet wall of the Udayeśvara temple, Udaypur. - **Fig. 3.** Detail of the serpentine graph. - **Fig. 4.** Detail of the short inscription in the middle.
> — **SIN-S** · *A serpentine scimitar of letters from Udaypur, district Vidisha, M.P.* · p. — · `singh-serpentine-00030`

> a plain exterior except for the basement, plinth and the podium. “The proximity to Udaypur, where the Udaypur Prasasti was first found, and the style of the building and sculpture, which is unmistakably from the eleventh century, allows us to reasonably conclude that the Udaypur prasasti is from Muratpur and that the tablet was the dedicatory inscription of this building.”
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 100 · `intach-2022-udaypur-00334`

> Figure 25: Inscription installed in Setho ki Baniya Baoli This inscription is situated in the Setho ki Baniya Baoli near Chatua Darwaza in the village Udaypur. The inscription stone is installed in the Jarokha of the Baoli (Figure 25). This inscription is $^{29}$ Ibid a six-line inscription written in Devanagari script. The date and text of the inscription is not known.
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 26 · `intach-2022-udaypur-00119`

### C8.5 — iast, aura, haiṃ, rājā, tathā

> राजा ने आदेश दिया कि धारा नगरी में जो कविता नहीं करता हो उसका घर *[IAST] citrapa, halāyudha, bhaṭṭalakṣmīdhara, dhanapāla, amitagati ādi kitane hī vidvān sāhityakāra isa yuga ko apanī jñānasādhanā se samṛddha kara rahe the| isī samaya ujjaina meṃ ubbaṭa ne veda kī vyākhyā kī aura mahākāla ke pujārī purāṃtaka ne śyamalādaṇḍaka nāmaka vikhyāta stotra kī racanā kī| isa samaya kitane hī jaina vidvān aura saṃta hue| rājā bhoja ne unakā bhī hṛdaya se svāgata kiyā| isa prakāra tatkā…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 9 · `bhojdev-hi-00046`

> सूत्रधारमहिरसुतमणथलेणघटितं । विस्वेलिकसिवदेवेनलिखितमिति । संवत् 1091 *[IAST] sūtradhāramahirasutamaṇathaleṇaghaṭitaṃ | visvelikasivadevenalikhitamiti | saṃvat 1091* इस लेख के कुछ अक्षर अस्पष्ट होने से श्लोक पूरा स्पष्ट नहीं हो पाता है। तब भी जो अंश स्पष्ट है उससे यह तो ज्ञात हो ही जाता है कि यह लेख संवत् 1091 या 1034 ई. में लिखा गया। राजा भोज की नगरी (धारा) की विद्याधरी (विद्या धारण करने वाली) अप्सरासी जो शाम्भवी (शक्ति संपन्न) है। जो स्मरण करता है उसे सुख प्राप्त होता है। मा…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 7 · `bhojdev-hi-00036`

> अखिलेपि जगद्गङ्गे नृत्यन्ती ललितैः पदैः । *[IAST] akhilepi jagadgaṅge nṛtyantī lalitaiḥ padaiḥ |* नर्तयत्यखिलं विश्वं या नः सा पातु भारती ॥ 24 *[IAST] nartayatyakhilaṃ viśvaṃ yā naḥ sā pātu bhāratī || 24* धार से प्राप्त और ब्रिटिश संग्रहालय में प्रदर्शित वाग्देवी की प्रतिमा के पादपीठ पर जो लेख उत्कीर्ण है उसमें एक अस्पष्ट श्लोक और कलाकार का नाम तथा संवत् है। वह लेख इस प्रकार प्रायः होगा - *[IAST] dhāra se prāpta aura briṭiśa saṃgrahālaya meṃ pradarśita vāgdevī kī pratimā ke p…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 7 · `bhojdev-hi-00034`

> In Roman Samvat 1696 vrashe Chaitra vadi 11lishata (likhita)sila vadi 11lishata (likhita)sila sra (Sri) Dasasuta Toshaputra Turasadasa..Ranathabhore.. In Devanagari संवत 1696 ब्रसैचैत्र वदी 11 लीप्रतसीला वदपूववगौरजाततउसःउ त्सासौदारनसतचोषाःपुववक.(च) तुरसाहासरणतंभोरगढवचं Gataka Image 112 Original Image of Inscription III
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 125 · `intach-geoheritage-00397`

**Gaps.** barely represented here: `BET-S`.

## C9 — Built Heritage: Fortifications, Mosques, Shrines and Stepwells

[↑ contents](#contents)

**Coverage.** 2,330 chunks from 24 sources (`ADH`, `BHJ-H`, `DEV`, `GAN`, `GAZ-VID`, `GUP`, `HAR`, `INT-ARC`, `INT-GEO`, `KRAM-1`, `KRAM-2`, `PAN`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `RAJM`, `SAM`, `SIN-B`, `SIN-S`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: primary_authorial_paramara 545, secondary_core 543, secondary_comparative 495, field_observation_survey 321, field_observation_reportage 271, primary_epigraphic 68, contextual_thematic 35, reference_tertiary 33, primary_scriptural 19. The largest single contributor is `SAM` with 545 chunks (23% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- Sacked by Alauddin Khilji in 1305 A.D., its extensive 23-mile stone wall fortifications and gates were engineered primarily by Hoshang Shah Ghori from 1405 A.D. onward. — `PAT-INS` `[single-source]`
- Vaishnavism is represented by 87 shrines, including the rock-cut Chaturbhuja temple (875 A.D.) on Gwalior Fort, the Pathari column (861 A.D.), and the Varaha relief at Udaygiri. — `PAT-CH` · `PAT-INS` · `PAT-TEM` `[established]`
- The mosque is built in the Mandu style and bears Persian and Sanskrit inscriptions referring to its construction by an agent of Sher Khan during the reign of Ghiyas Shah Khilji, Sultan of Mandu, in A.H. 894 (A.D. 1488). — `GAZ-VID` · `PAT-CH` `[established]`
- The great Nilakantheśvara temple at Udayapur was built by Udayaditya in Sam 1116 = 1059 A. D. An ART AND CULTURE 259 inscription of the sixteenth century A. D. describes it as the most beautiful temple in India. — `GAN` `[single-source]`
- The fort contains Sikandar Lodi's mosque, the tomb of Madar Shah, a Roman Catholic chapel and cemetery of 17th-century European gunners, and massive old inscribed cannons (e.g., *Shatru Samhar*, *Ram Ban*). — `PAT-INS` `[single-source]`
- Five internal inscriptions record that its construction was initiated by the Bhadoria Rajput chief Badan Singh in **1644 A.D.** and completed by Maha Singh in **1068 A.D.**, who designated the stronghold as *Devagiri*. — `PAT-CH` · `PAT-INS` · `PAT-TEM` `[established]`
- Gateway to the Geo Heritage Reserve: Udaypur Hill Fort site already has a well-defined historical gate, existed there for more than 1000 years. — `INT-GEO` `[single-source]`
- A foundational inscription records its excavation in **875 A.D.** by Alla, a local governor under King Ramadeva of the Imperial Gurjara-Pratihara dynasty of Kanauj. — `PAT-CH` · `PAT-INS` `[established]`
- When King Udayaditya laid the foundation for the city of Udaypur and Udayeshwar, also known as Neelkantheshwar Temple, in the 11th century CE, it is also mentioned in the Udaypur Prashasti that he built a lake called Udaysagar. — `INT-GEO` `[single-source]`
- The 2 large water bodies relevant to Udaypur are the Udaysagar Talab, built by Udaya Aditya in 1059 CE, and the Bhujariya Talab, which existed before his time. — `INT-GEO` `[single-source]`
- The larger temple was completed in **1093 A.D.** by the Kacchavaha Rajput Prince Mahipala, as recorded on its entrance porch inscription. — `PAT-INS` `[single-source]`
- In the time of Emperor Jahangir, Auliya Ibn Abdul Samad had laid the foundation of this mosque and the Mahal Qubba of Udaipur — Sarkar Chanderi, Suba Malwa, the border of Gondwana. — `TIW-E` `[single-source]`
- The Hill Fort in Udaypur has a massive boundary wall made of sandstone running along the periphery of the hill with a total length of about 1400 m. — `INT-GEO` `[single-source]`
- The Shahi Masjid of Udaypur is located inside the palace of Raja Udayaditya at GPS 23.54.1.08 N and 78.3.34.79 E. — `INT-ARC` `[single-source]`
- The Vishnusagar, Purushottama (Sola) Sagar, Govardhan Sagar, Kshirsagar, Dabri, Dudhtalai, the Pushkar tank of Rangbavdi, and Rudrasagar — successively, forming a series of mutually adjoining circles — reach up to the bank of the Sipra. — `RAJ-E` `[single-source]`
- Other significant structures of this area are the Udaypur Mahal, Bhujariya Talab, Udaysagar Talab, Ganesh Temple, etc. — `INT-GEO` `[single-source]`
- The internal area contains four fortified enclosures: *Maj-loka* (the central core), *Madar Ahata*, *Gujar Ahata*, and *Dhola Ahata*. — `PAT-INS` `[single-source]`
- A brief description of these is as follows: Shesh Saiya- This is a Vishnu culture measuring 900 mm in length and 400 mm in width. — `INT-GEO` `[single-source]`
- Barely represented in this bucket, so anything resting on them is a thin reed: `RAJM`, `SIN-S` — `[gap]`

### C9.1 — built, town, temple, shikhara, architecture

> The pinnacles are climbed by a carved human figure representing either the architect or the royal builder. The compound originally housed eight minor attendant shrines; a mosque was built at the back of the main temple by Sultan Muhammad Tughlaq between **1336 and 1338 A.D.** (*A.H. 737–739*) using stone blocks from a dismantled attendant shrine, recorded on two Persian inscriptions. * **Other Monuments:** The *Bijamandal* (a contemporary two-storeyed stone house of the templ…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00085`

> * **Kamal Maula Mosque or Bhoja Shala:** A large Islamic compound constructed out of the remains of the **Bhoja Shala**, the premier Sanskrit college founded by the Paramara King Bhoja in the 11th century. The mosque consists of a large court enclosed by colonnades of reused carved columns and a rear prayer hall with fine temple ceilings. The stone pavement of the prayer hall contains numerous slabs of black slate whose surfaces were scraped; several retrieved slabs preserve …
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00092`

> The ancient *Nalapura*, traditional capital of King Nala of the *Mahabharata*. The fort is situated on a flat hilltop rising 500 feet above the plain, its circuit walls running 5 miles along the ridge. It was held by the Kacchawahas, Tomars, and Jajapellas. The eastern approach features a series of historic gates, culminating in the *Hawapaur*, built under Daulat Rao Scindia. The internal area contains four fortified enclosures: *Maj-loka* (the central core), *Madar Ahata*, *…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00073`

> Two adjacent historical villages containing a vast cluster of ruins around a common tank, anciently named *Vatanagara*. * **Gadarmal Temple:** A massive structural temple visible from miles away due to its height. It is composite, consisting of a lower 9th-century basement and porch of the original temple, surmounted by a later *shikhara* built of heterogeneous stone pieces collected from nearby ruins. The plan is oblong, consisting of a wide sanctum and a porch without a hal…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00088`

### C9.4 — shrine, temple, temples, century, form

> A folklore has it that that there was a milkman Keshav and Goddess Mahamaya paid him a visit in the form of a beautiful lady and suggested to him the idea of stepwell and later people of the village built this structure. The site is located inside the Badi Mata Mandir complex at GPS 23.53.55.71 N and 78.3.45.98 E. This structure is located in khasra no. 677/2. It is currently in government ownership. The whole structure is made of stone slabs and bricks and is incomplete ruin…
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 93 · `intach-2022-udaypur-00314`

> Figure 61: View Moti Masjid Darwaza from outside Figure 62: Plan of Moti Masjid Darwaza Figure 64: Horse placed near gate by people Figure 63: View of Moti Masjid Darwaza from inside The gate is similar to the Chanderi Darwaza in architectural style and features. It is approximately 15ft tall and 8ft wide. It has a trabeated structural system dressed with a corbelled point arch. The arch has ornamented brackets. The colonnade to the north exhibits terracotta animal figures ex…
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 48 · `intach-2022-udaypur-00204`

> This structure is situated on the hill in the South of the village at location GPS 23.53.30.9 N and 78.03.28.1 E. The Jind Baba ki Mazar is a religious shrine located between the larger and Figure 56: The bird's eye view of the Jind Baba ki mazar smaller hills. This structure is under Forest Department ownership. It is approached by a series of steps that climb up till the hillock. The lintel at the entrance reads Darbar e Auliya Hazrat Maula Ali Mushkil Kusha. The site consi…
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 46 · `intach-2022-udaypur-00197`

> 1. Gwalior Fort, Partial View 2. Larger Sas Bahu Temple, Gwalior Fort 3. Kakan Madh Temple, Suhania 4. A Temple in Gadhi, Padhavli 5. An excavated Brick Platform, Pawaya 6. A lintel showing scene of dance from Pawaya 7. Carved Ceiling of a Temple, Surwaya 8. Mahadeva Temple, Kadwaha 9. A Torana Gateway, Terahi 10. A Carved Mihrab of a Muslim Tomb, Chanderi 11. Caves Nos. 5 and 6, General View, Udaygiri 12. Heliodoros Pillar (Khamb-Baba), Besnagar 13. Hindola Torana Gateway, G…
> — **PAT-CH** · *The Cultural Heritage of Madhya Bharat* · p. — · `patil-1952-00011`

### C9.5 — udaipur, udaypur, udayaditya, history, after

> The construction of this darwaza was carried out in 11th century CE. It is situated at GPS 23.54.12.78 N and 78.3.28.53 E. The Chanderi Darwaza is located in the northwest of the Udaypur Village near the Bijasen Mandir. This structure is located in khasra no. 128 having an area of 0.158 ha. It is currently in Government ownership. The gate is a trabeated structure built in stone. The high lintel is supported by carved brackets projected from the fort walls. The gateway also h…
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 48 · `intach-2022-udaypur-00202`

> Bhujariya Talab is a natural water body located to the southeast of the village Udaypur. This large water reservoir is located on the outskirts of the village near a live stone quarry covering an area of 8.04 acres. This talab is one of the "chappan baoli, bavan kuae and saadhe barah talab", or 56 stepwells, 52 wells and 12 and half lakes, according to the locals. When King Udayaditya laid the foundation for the city of Udaypur and Udayeshwar, also known as Neelkantheshwar Te…
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 49 · `intach-geoheritage-00214`

> These have all been captured in the book "The Architectural Splendor of Udaypur"; the most significant and biggest of them is the Udayeshwar Mandir, also known as Neelkantheshwar temple, a monument protected by the Archaeological Survey of India. Other significant structures of this area are the Udaypur Mahal, Bhujariya Talab, Udaysagar Talab, Ganesh Temple, etc. A list of significant historical sites is given in Annexure 2. The Topo sheet of the entire terrain is attached as…
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 10 · `intach-geoheritage-00089`

> One morning, he reached Udaipur with his experts. We had thought that in four to five hours he would get to see, very quickly, every necessary place that needs immediate care. Praveen Sharma was ready as the local guide, who had to arrange a photographer. Upadhyay-ji roamed for seven or eight hours. His team went and saw, from every corner, the thousand-year-old tanks, stepwells, the Nataraja Shiva present on a 27-foot rock in Ravan Toll, the Pisanhari temple, the hill's fort…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00317`

### C9.3 — fortification, hill, udaypur, wall, structure

> Walking along this hill fortification wall, we see bastions of different dimensions, the semicircular bastion, the rectangular bastion, and gateways on both sides of the entry gate. This entire fort complex is a mystery because historical records are silent about it. It is also an architectural marvel that is standing undisturbed over a span of 1400 meters, maybe the longest one anywhere in Madhya Pradesh. The fortification wall is built in such a manner that it uses one face…
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 19 · `intach-geoheritage-00127`

> Image 71 A rear side gateway Image 72 Small niche made of stone at entrance of security the Udaypur with 2300 mm shelter end. window or charge of with which Image 73 Slit holes/arrowheads on fortification walls Watchtowers: A watchtower in a fortification wall is a high and safe place from which guards keep watch over the surrounding area. It's like a rectangular bastion. Udaypur hill fortification wall has two watchtowers, each located on the opposite side of the fortificati…
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 92 · `intach-geoheritage-00328`

> The north-west corner temple and the western bedi were knocked down in the time of Muhammad Tughlak and a masjid was erected in their place, as recorded in the two inscriptions over the two small doorways to the right and left of the temple, which are dated respectively in 737 and 739 of the Hijira. The gateway on the west is not in the middle, and, as it is built of old materials, I have no doubt that it was built at the same time as the masjid.'¹³²
> — **PAN** · *The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta* · p. 91 · `pande-udayesvara-00404`

> मजारों पर फूँका जाता रहा। भारत की सारी आन, बान, शान इन कब्रों और मकबों पर सेकुलर ब्रश से पोत दी गई। लोग बेवजह बीजेपी को मुस्लिम विरोधी पार्टी करार देते हैं, जबकि तथ्य कुछ और ही इशारा करते हैं। उदयपुर में मिले तथ्यों के हिसाब से देखें तो सच्चाई कुछ और ही है। उदयपुर में मध्यप्रदेश की सरकार ने पिछले पांच साल में एक करोड़ 10 लाख रूपए खर्च किए। चार संरक्षित स्मारकों में हाई-तीन सौ साल पुरानी दो मस्जिदें भी राज्य सरकार के जिम्मे में हैं। बाकी दो में एक पिसनहारी का मंदिर और रावणटोल …
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00352`

### C9.6 — created, deserves, create, breadth, parts

> The fort is called as of six types for kings desiring victory. The water fort, the slime fort, the forest fort, the desert fort likewise. The mountain or Hill fort of a huge norm, this way should be created by the kings. Of all the forts the Hill fort is acclaimed as best. दुर्गस्थानविभागोऽत्र पोडशाख्येन कीर्तितः । मध्ये तु ब्रह्मणः स्थानमसम्बाधं विधीयते ।।४१।। The division of the space of a fort stands allocated by the enumeration of sixteen (padas) or (squares). In the cent…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 45: The definition of Eight Components · `samarangana-00656`

> ``` # Chapter 32: The Elephant Stud or Equery for Tuskers Chapter 32 CHAPTER 32 The Elephant Stud or Equery for Tuskers लक्षणं गजशालानामिदानीमभिदध्महे। चतुरश्रीकृते क्षेत्रे भागैर्भक्ते ततोऽष्टभिः ।।१।। Now we shall illustrate the definition of the elephant stables. In an area square shaped created and divided into eight parts. मध्ये द्विभागविस्तारं स्थानं कुर्वीत् हस्तिनः। कल्प्याः प्रासादवद् भागा ज्येष्ठमध्याधमाः क्रमात् ।।२।। In the centre having breadth of two parts a spa…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 31: Named Yantravidhānaṁ i.e. The Chapter dealing with the Preparation of Mechanical Contrivances · `samarangana-00475`

> eight cubited equipped as such in the tenth part broad at the gate. विस्तारो मण्डपस्तम्भद्वारोच्छ्रायसमोच्छ्रितिः । गर्भव्यासो मण्डपस्य साष्टांशः सांश एव च।।६२।। The breadth, and elevation equal to the elevation of the gate and columns of the pavilion eight cubited equipped with a bhrama on the ten digits broad on the gate. Garbhavyāsa of the Mandapa having eight digits on one digit may be there. सार्थो वा मण्डपस्यायं गर्भे +++++।।६३।। The garbha of the pavilion may be of 1 e…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra > Architectural Treatise of Mahārājādhirāja Śrī Bhojadeva > [Original Page Source: 14] · `samarangana-01255`

> ``` SAMARĀNGAŅA-SŪTRADHĀRA of Mahārājādhirāja Śrī Bhojadeva Paramāra # CHAPTER 51 The foundation of shrines एवं नृपस्य प्रासादे कृते क्लृप्तेऽथवा भुवि। तस्यानुजीविनः कुर्युः प्रासादान् परिधौ यदि ।।१।। This way the palace of the king having been built or well laid on the ground, if his entourage may create abodes on the surrounding premises or periphery. तदा दिग्भागविन्यासस्थानमानान्यनुक्रमात्। तेषामिहाभिधीयन्ते सर्वेषां वृद्धिहेतवे ।।२।। Then of those here are being illustrat…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. CHAPTER 51 · `samarangana-00778`

### C9.2 — having, house, well, those, even

> राजा भोज के समय से मालवा में निर्माण-क्रांति आ गयी थी। प्रासाद, मन्दिर, तालाब, प्रतिमाएँ बनती रहीं और पूरा मालवा इन अनोखी कलाकृतियों से भर गया। मन्दसौर जिला इस दृष्टि से अधिक समृद्ध है। वहाँ का हिंगलाजगढ़ तो तत्कालीन अप्रतिम प्रतिमाओं का अकृत खजाना है। आज मालवा में जो कुछ निर्मितियों के प्राचीन रूप दिखाई देते हैं, उनमें से बहुधा परमारकालीन हैं। *[IAST] rājā bhoja ke samaya se mālavā meṃ nirmāṇa-krāṃti ā gayī thī| prāsāda, mandira, tālāba, pratimāe~ banatī rahīṃ aura pūrā māla…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 6 · `bhojdev-hi-00028`

> f, ' „;a„ dwellinBS, and deals with the plan- literally, an ^ifclutcc ofof houses, halls and places as nine of towns and villages. buMinas o| iruclion of cities, places expression tolu'me eonsists of 83 .idhyay as and tirihcdeseription of prasudas pertaining to Devas. i^vrjic with the diverse subjects of secular taterS'sI".:::tion'or building and seleetion of sites, aril: clcs of furniture, precious stones etc. SECULAR ARCHITECTURE . T el- tn this ocriod too, almost every tow…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-01031`

> Dancers thronged in the temple court-yard and the palace of the kings •In the plan of palace, Bhoja included, inter alia, the construction of a dancing hall, a theatre and a gymnasium.® The SamgUamakaranda, attributed to Narada, perhaps, belongs to the 11th C.A.D. It deals with music and dance in two separate parts.® In the Aparajita-pfcchu, another 1. 5.5. II, p. 11. 2. c.g. Managoli inscription, E.T.V., p. 23. 3. Rnshirakxifas and their Times, p, 350. 4. 5 5. C/m/7/. 15, V.…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00692`

> Kaha, the Magadhi’ Prakrita Jain legends (A. D 1038) which show that even such pictures were drawn in which the presence of human figure was not always necessary. The TrisasjhiSalaka purusa- caritra of Hemchandra states that each palace had a picture-hall containing the wall-paintings. Moreover, the work of painting was allocated among the painters who had their own assemblies. The Kathasaritsagara narrates that once a painter drew a picture on a smooth pillar and then a scul…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-01140`

**Gaps.** barely represented here: `RAJM`, `SIN-S`.

## C10 — Ritual and Knowledge: Śaiva Traditions and Intellectual Worlds

[↑ contents](#contents)

**Coverage.** 2,769 chunks from 24 sources (`ADH`, `BHJ-H`, `DEV`, `GAN`, `GAZ-VID`, `GUP`, `HAR`, `INT-ARC`, `KRAM-1`, `KRAM-2`, `PAN`, `PAR`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `RAJM`, `SAM`, `SIN-B`, `SIN-S`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: secondary_core 998, primary_authorial_paramara 778, secondary_comparative 396, reference_tertiary 262, primary_scriptural 257, contextual_thematic 46, field_observation_reportage 16, primary_epigraphic 15, field_observation_survey 1. The largest single contributor is `SAM` with 774 chunks (28% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- Puraścaryārṇava of Mahārājādhirāja Pratāpasiṇha of Nepal ; Kashmir Sanskrit Series, 1901-1904. — `KRAM-2` `[single-source]`
- RcUsioiis Conditiom 145 Lists of these schools occur in the Vuniana’ and J^iva Puranas,^ the Agamn-Pramfinya^ of Yumunachnrya, the Sri Bhashya* of Ramanuja, the commentary'* of Vachaspali Misrn on the Sarlraka- bhashya. — `SIN-B` `[single-source]`
- Kulārṇava Tantra ; Tantrik Texts Series, Calcutta, 1917. — `KRAM-2` `[single-source]`
- Samūrtārcanādhikaraṇa ; Śrī Venkaṭeśvara Oriental Series, Tirupati, 1943. — `KRAM-2` `[single-source]`
- His successor Vakpati II Munja (974–995 A.D.) was a great general, poet, and literary patron who defeated the Cholas, Chalukyas, and Chedis before losing his life to Taila II. — `GAN` · `PAT-INS` `[established]`
- Contemporary Sanskrit inscriptions on its porches record that it was founded by the Paramara King **Udayaditya**; construction commenced in **1059 A.D.** (*V.S. 1116*) and the flagstaff was hoisted in **1080 A.D.** (*V.S. 1137*). — `PAT-INS` `[single-source]`
- The commentators on Śaṅkarācārya mention four distinct Śaiva schools- Pāśupata, Māheśvara, Śaiva Siddhāntis and Kālāmukhas. — `PAN` `[single-source]`
- Vaishnavism is represented by 87 shrines, including the rock-cut Chaturbhuja temple (875 A.D.) on Gwalior Fort, the Pathari column (861 A.D.), and the Varaha relief at Udaygiri. — `PAT-INS` · `PAT-TEM` `[established]`
- The names of the eight *vidyeśvaras* are given as Ananta, Sūkṣma, Śivottama, Ekanetra, Ekarudra, Trimutri, Śrīkaṇṭha and Śikhandī. — `PAN` `[single-source]`
- An explanation of Prāsāda from the Śaiva point of view is given below, based mainly on the 'Īśānasivagurudevapaddhati', a compendium dating from about 1000 A.D. The rhythmic formula, the Prāsāda (mantra) is Nāda ('Tantrasamuccaya', I. — `KRAM-1` `[single-source]`
- Narpati Nalh composed the *Bisaldev-raso* in Samvat 1272, in which the marriage of Bhoj's daughter with Bisaldev is discussed. — `RAJ-E` `[single-source]`
- The book is usually an attribute of Brahmā and it may be noted that according to the Kāraṇāgama, Agni should be made similar to Brahmā.⁴⁰ The figure of Agni stands in abhaṅga and is bejewelled. — `PAN` `[single-source]`
- We may see the components of Śiva, Śakti, Sadāśiva, Īśvara and Sadvidyā in the śukanāsa.¹⁹ In the upper medallion of the śukanāsa, the components of Śiva and Śakti are seen. — `PAN` `[single-source]`
- Just as for the Southern school of Śaiva Siddhāntins, the *Śivajñānabodham* of Meyakaṇdeva became the authoritative source, the *Tattvaprakāśa* of Bhoja was the most important text — `PAN` `[single-source]`
- In the north of Nila mountain and to the south of Śveta mountain, the fifth varșa, highly gorgeous, is known as Ramyaka [cite: 857, 861, 863]. — `SAM` `[single-source]`
- THE METAPHYSICS OF ŚAIVISM AND ŚAIVA SIDDHĀNTA In Śaiva Siddhānta, the *jīva* has powers belonging to his own nature but covered by *mala*, *karma* and the *kañcukas* of *māyā*. — `PAN` `[single-source]`
- The Saiva Siddhanta School The inscriptions mention Guhavasi of Daruvana as the preacher of Saiva Siddhanta doctrine. — `SIN-B` `[single-source]`
- And with peaks made of Hema (i.e. gold), Hemakūța, this one was known as the mountain [cite: 827], to which serve perennially or to which keep occupied perennially Cāraṇas (heavenly charioteers⁶) and Guhyakas [cite: 828, 830]. — `SAM` `[single-source]`
- Barely represented in this bucket, so anything resting on them is a thin reed: `INT-ARC`, `PAR`, `SIN-S` — `[gap]`

### C10.2 — having, created, deserves, create, norm

> shrubs and creeping plants fascinating for the mind owing to cuckoos, bees, swarms, and rows of swans. प्रवहत्सकलस्त्रोतः सुश्लिष्टनिविष्टनाडिकं मध्ये। सच्छिद्रनाडिकयुतं नानाविधरूपरमणीयम् ।।१२९॥ Having all currents or streams flowing, and in the middle having a water-clock¹ equipped with water-clock having fine holes good looking owing to many fold forms. सुश्लिष्टनाडिकाग्रे स्तम्भतुलाभित्तिसंश्रिते परितः। सम्यक् कृत्वा दृढतरविलेपनं वज्रलेपाद्यौः ।।१३०।। In front of the well …
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 31: Named Yantravidhānaṁ i.e. The Chapter dealing with the Preparation of Mechanical Contrivances · `samarangana-00424`

> ``` # Chapter 42: The Ritual of Propitiatory Rites CHAPTER 42 The Ritual of Propitiatory Rites इदानीमभिधास्यामो विधानं शान्तिकर्मणः। यथावदिष्वा दिक्पालान् हुत्वा शान्तीर्यथाक्रमम् ।।१।। Now we shall talk about the arrangements for the propitiatory rites.. Having offered sacrifices for the gods as per routine and offered oblations as per ritual, for the Pacificatory Rites. स्नपयेत् कर्णिकां कुम्भैः सहिरण्यैर्विचक्षणः। सर्वगन्धानुलिप्तां च माल्यदामविभूषिताम्।। २ ।। (The Archite…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 41: Cayavidhih - The edifice laying · `samarangana-00608`

> By the Priests officiating at a sacrifice and Brahmaņas the valiant or Heroic architect accompanied by chaplains at night may offer offering at a sacrificial performance in the capital in all the four quarters. कर्णचत्वरशृङ्गाटेष्ववनीपालवेश्मनि। स्थानेष्वेतेषु विप्राद्यैर्वेदि निष्पाद्य साक्षताम् ।।७।। On the corners, squares quadrangles within the palace of the protector of the Earth i.e. King on such spots by Brāhmaņas and others, having got erected a raised platform or enc…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 45: The definition of Eight Components · `samarangana-00660`

> Then dangers of fire one may pronounce for the country as well as for the capital. (Then) he may organise the ritual by the Brahmaņas on the outskirts as well as interior areas. नते वा शीर्णभग्ने वा व्याधिपीडां विनिर्दिशेत्। होमं बलिं च कुर्वीत पुनः संस्कारमस्य च।।१२।। (The arched portal) getting bent or broken or getting torn as under he may enjoin the anguish of disease. (He) may take to the task of sacrificial offering as well as sacrificial ritual and a repeated reconstru…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 45: The definition of Eight Components · `samarangana-00661`

### C10.4 — śiva, hands, lotus, left, right

> Atharvaveda, the guardians of the directions are conceived as 'protectors' and 'arrows' or weapons of the directions.³⁷ Agni was accorded a very high status in the Vedic pantheon. In the Rg Veda, Agni is both the means as well as the end. He is both the sacrificial fire as well as an exalted deity.³⁸ He is called a knowledgeable Brahmin.³⁹ As such, it is not surprising that here at Udayeśvara temple, the book is shown in the hand of Agni. It symbolizes both the Vedic sacrific…
> — **PAN** · *The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta* · p. 32 · `pande-udayesvara-00220`

> By the 11th century CE and later, we have two important Śaiva writers, viz. Nāmpiyandār and Sekkilār. Śaiva-Siddhānta blossomed fully in the 13th century with the works of the great Śaiva teachers (santānācāryas). The most important was Meyakaṇḍadeva as also his pupils, Aruṇandi and Umāpati. Of the Nāyanār saints, the work of Māṇikkavācakar has received special significance through the commentary of Umāpati. Indeed, the meaning of his name is “he whose utterances are rubies”.…
> — **PAN** · *The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta* · p. 110 · `pande-udayesvara-00594`

> Pl. 16. Dancing Sarasvati, 9th century CE. Pl. 17. View of the śukanāsa from the south-east. Visou and Śiva are indicative of the sun, moon and fire of which elements these gods are the adhiṣṭhātri devatās. Such an image greatly assists in the meditation of Sadāśiva.¹⁸ The composition of the śukanāsa, thus, may be related to the elements of Śaiva Siddhānta philosophy. It is seen to reflect the śuddha addhvā of the Śaiva Siddhānta philosophy. We may see the components of Śiva,…
> — **PAN** · *The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta* · p. 22 · `pande-udayesvara-00191`

> *Āgama and Tantra* Gandharva Tantra, see Tantrasāra. Hayaśīrṣapañcarātra ; Chapters I-XIV (title page missing). Īśānaśivagurudevapaddhati ; T.S.S., Trivandrum, 1920-1924. Jñānārṇava Tantra ; A.S.S., Poona, 1912. Kālottara Āgama, quoted in Īśānaśivagurudevapaddhati. Kāmikāgama ; Ms. No. D. 5431, Government Oriental Manuscript Library, Madras. Kiraṇāgama, quoted in Īśānaśivagurudevapaddhati. Kaulāvalī Tantra, see Tantrasāra. Kulārṇava Tantra ; Tantrik Texts Series, Calcutta, 19…
> — **KRAM-2** · *The Hindu Temple, Volume II* · p. 152 · `kramrisch-1946-v2-00751`

### C10.6 — bhoja, paramara, learning, india, literature

> Between the 8th and 12th centuries, several distinct schools of Śaiva worship and philosophy came to be formulated. The commentators on Śaṅkarācārya mention four distinct Śaiva schools- Pāśupata, Māheśvara, Śaiva Siddhāntis and Kālāmukhas. Of these, it is the Śaiva Siddhāntis who dominated Central India and the South, i.e. from Malwa to the south. In the 11th century CE, Bhoja Paramāra wrote his Tattvaprakāśa expounding the tenets of Śaiva Siddhānta. In the 14th century CE, M…
> — **PAN** · *The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta* · p. 100 · `pande-udayesvara-00541`

> prevalence of (his cult in early and late mediaeval periods. It may, therefore, be concluded that the cult of the five deities as envisaged by the Smartas came into vogue by the llth C. A. D. and that it indicates the reapproachment of the Vedic and Agamic tendencies The view that Pancadevopasand was introduced by Samkaracharya does not seem to be right. Inscriptions thus describe three Saiva movements. The earliest movement was started by Srikantha who founded the Pa^upata s…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00480`

> Saivism (a) Saiva (b) Kalanana (c) Siva Sasana and (d) Pasupata. 1 . tfei fri^r' F^«ir Tmqff i ZTStPar fiTST' rriOTcT F? I Kiirma Ptirana 2. ^tritriririmT F^ra^iTRRFrTrr i FTirtf'mt II VisveSavara, the Saiva pontiff had sanctioned a land grant for providing meals and clothes to the students and ascetics belonging to these four sects. J.A.H.R.A.S. IV., p 147 ff. RcUsioiis Conditiom 145 Lists of these schools occur in the Vuniana’ and J^iva Puranas,^ the Agamn-Pramfinya^ of Yum…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00443`

> B. LAKULISA R. G. Bhandarkar regards LakulTsa as the founder of the Pasupata school ^ Bagchi suggests, “Lakullsa” was probably Srikantha’s disciple and that these two were responsible for the foundation of Pasupata religion.^ But Lakulisa does not seem to be an immediate disciple of Srskantha, because the accounts of Srikantha and Lakulisa available through literature and inscriptions do not represent them as teacher and disciple. Moreover, in the Agama quoted by Abhinavagupt…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00448`

### C10.1 — iast, aura, haiṃ, tathā, para

> राजा भोज से एक वृद्धा की बातचीत मालवी के *[IAST] rājā bhoja ne usa kubinda kavi kā bhī māna kiyā| ballāla ke anusāra rājā bhoja kī sabhā meṃ pā~ca sau kavi the| ballāla ke atirikta bhī vibhinna kaviyoṃ ne samaya-samaya para aneka bhojaprabaṃdha racakara usa apratima rājā ke prati apanī āsthā prakaṭa kī| śubhaśīla ke bhojaprabaṃdha meṃ katipaya kathāe~ ballāla kī pustaka jaisī bhī haiṃ| ratnanaṃdana gaṇi (1340 ī.) yā ratnamaṃdira gaṇi (1460 ī.) ke bhojaprabaṃdha meṃ sāta khaṃḍ…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 10 · `bhojdev-hi-00050`

> सूत्रधारमहिरसुतमणथलेणघटितं । विस्वेलिकसिवदेवेनलिखितमिति । संवत् 1091 *[IAST] sūtradhāramahirasutamaṇathaleṇaghaṭitaṃ | visvelikasivadevenalikhitamiti | saṃvat 1091* इस लेख के कुछ अक्षर अस्पष्ट होने से श्लोक पूरा स्पष्ट नहीं हो पाता है। तब भी जो अंश स्पष्ट है उससे यह तो ज्ञात हो ही जाता है कि यह लेख संवत् 1091 या 1034 ई. में लिखा गया। राजा भोज की नगरी (धारा) की विद्याधरी (विद्या धारण करने वाली) अप्सरासी जो शाम्भवी (शक्ति संपन्न) है। जो स्मरण करता है उसे सुख प्राप्त होता है। मा…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 7 · `bhojdev-hi-00036`

> ज्योतिषी और पुरोहित द्वारा शान्ति आदि अनुष्ठानों के बाद शास्त्रज्ञ शिल्पविद् स्थपति कर्म करें। 174 *[IAST] jyotiṣī aura purohita dvārā śānti ādi anuṣṭhānoṃ ke bāda śāstrajña śilpavid sthapati karma kareṃ| 174* पुरोहित अग्नि में हवन करें, ज्योतिषी स्थिरता दें, स्थपति भेंट पूजा करें - इस प्रकार शान्ति की योजना करें। 175 *[IAST] purohita agni meṃ havana kareṃ, jyotiṣī sthiratā deṃ, sthapati bheṃṭa pūjā kareṃ - isa prakāra śānti kī yojanā kareṃ| 175*
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 50 · `bhojdev-hi-00215`

> स्थपति को आठ प्रकार के कर्मों का सदा ज्ञान रहना चाहिए - आलेख (चित्र), लेखन, काष्ठकर्म, चय (सामग्री, भवन, द्वार, प्राचीर आदि), पापाण सिद्ध (पत्थर के काम में सिद्धि), स्वर्णकर्म, यान्त्रिक या ललितकला और कर्म (कारीगरी) - इन समस्त गुणों से स्थपति पूजा जाता है ॥20-21 *[IAST] sthapati ko āṭha prakāra ke karmoṃ kā sadā jñāna rahanā cāhie - ālekha (citra), lekhana, kāṣṭhakarma, caya (sāmagrī, bhavana, dvāra, prācīra ādi), pāpāṇa siddha (patthara ke kāma meṃ siddhi), svarṇakarma, yānt…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 96 · `bhojdev-hi-00433`

### C10.3 — architecture, bhoj, town, temple, king

> There are many different Shaiva sects, the oldest known being that of the Pashupatas, its teachings attributed to Shiva via an incarnation, the sage Lakulisha (2nd century AD). The esoteric, proto-Tantric Bhairava cult of the Kapalikas is another early form. Puranic orthodoxy distanced itself from all these Shaiva cults,$^{10}$ but Shiva looms large in the Puranas, especially as divine Lord of Mount Kailasa, with wife Parvati and sons Ganesha and Karttikeya. The texts called …
> — **HAR** · *The Temple Architecture of India* · p. 56 · `hardy-2007-00218`

> 6 David Gordon White, *Kiss of the Yogini: 'Tantric Sex' in its South Asian Contexts* (Chicago and London: University of Chicago Press, 2003), p 3. 7 Ibid, p 11. 8 Flood, *An Introduction to Hinduism*, pp 187-9. 9 Doris M Srinivasan, 'Śaiva Temple forms: Loci of God's Unfolding Body' in *Investigating Indian Art*, ed M Taldiz and W Labo (Berlin, 1987), pp 335-347 (p 337); also Doris M Srinivasan 'From transcendency to materiality: Para Śiva, Sādaśiva and Maheśa in Indian Art'…
> — **HAR** · *The Temple Architecture of India* · p. 59 · `hardy-2007-00232`

> The Shaiva Siddhanta ('fully completed') school spread far and wide; it is associated with important medieval temples, and in Tamil Nadu remains firmly rooted today. It represents a respectable face of Tantric Shaivism, an integration of formerly antagonistic Brahminic and Tantric views into a 'composite Tantric-Puranic religion'.$^{12}$ The Agamas followed by this school teach a meticulously structured cosmogony, in which transcendent Shiva, remaining whole and unaffected by…
> — **HAR** · *The Temple Architecture of India* · p. 56 · `hardy-2007-00219`

> King Bhoj and Paramara-period Town Architecture / 7 every city should have a Sarasvati (learning) hall, in which artists' performances are urged to be held every month or fortnight. King Bhoj continually inspired his scholars to write, according to their competence, treatises on various subjects. The self-acknowledgements of several such scholars and poets are known from their books. Among them, Ubbata (उब्बट), Dhanapala, Chhittapa (छित्तप), Amitagati, Keshava (केशव), Nichula…
> — **RAJ-E** · *King Bhoj and Paramara-period Town Architecture (English translation)* · p. 7 · `rajpurohit-bhoj-en-00024`

### C10.5 — linga, excellent, will, goddess, thus

> The following Mantra is to be recited: “O Vidya (Learning) conversant with the structure of the universe, performing diverse activities, grant me a son who will cause welfare. О goddess delighted due to this excellent Vrata, grant a son.” After devoutly feeding a thousand Brahmanas the devotee should have the Parana (formal ritualistic breakfast) with the food left over after their meal. О Lord, thus the Vrata is to be performed. I wish to perform it by your permission. Kindl…
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 176 · `skanda-xiii-00361`

> CHAPTER EIGHTYTWO Kayavarohanesvara1 Mahddeva said: 1-8. О Parvati, listen also to the origin of Kayavarohana. Merely by listening to it, a man ceases to be embodied. While Brahma was desirous of creation at the beginning of Vaivasvata Manvantara, Daksa, the Prajapati, was born from his right thumb. The wife of the noble-souled one came forth from the left thumb. The Lord begot of her fifty daughters. All those were 1. K&y&varohana (Mod. Karvan, Earoda District, Gujarat) was …
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 313 · `skanda-xiii-00668`

> By the power of what penance was such a capacity acquired? Today my very birth has become fruitful. Today my learning has borne fruit. The working of my mind has become fruitful by the sight of both of you." 3Sb-41. On hearing his words Kapila spoke these words: "O king, there is an excellent LiAga in Mahakalavana. It is wellknown by the name Siddhesvara. It is always adored by Siddhas. It is stationed to the east of Saubhagyesvara and it bestows conjugal bliss and freedom fr…
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 216 · `skanda-xiii-00447`

> If your husband can be administered different kinds of medicines and powders, if some great efficacious Mantras capable of enchantment can be uttered, if different kinds of unguents can be smeared over him, he will behave like a slave. Thereupon believing in their words, I hurriedly went ahead and procured the powder and Mantra. Back at the husband’s place, I administered the powder dissolved in milk to my husband. The Mantra (written on plaques and tablets) was used on his n…
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 294 · `skanda-xiii-00625`

**Gaps.** barely represented here: `INT-ARC`, `PAR`, `SIN-S`.

## C11 — Fields, Wells and Markets: Agriculture, Economy and Crafts

[↑ contents](#contents)

**Coverage.** 1,338 chunks from 25 sources (`ADH`, `BET-K`, `BET-S`, `BHJ-H`, `DEV`, `GAN`, `GAZ-VID`, `GUP`, `HAR`, `INT-ARC`, `INT-GEO`, `KRAM-1`, `KRAM-2`, `PAN`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `RAJM`, `SAM`, `SIN-B`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: primary_authorial_paramara 528, secondary_core 335, reference_tertiary 168, field_observation_reportage 114, field_observation_survey 60, contextual_thematic 54, secondary_comparative 48, environmental_scientific 13, primary_scriptural 10, primary_epigraphic 8. The largest single contributor is `SAM` with 526 chunks (39% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- A sample survey executed by the Reserve Bank of India's *All India Rural Credit Survey Committee* between November 1951 and July 1952 detailed heavy agricultural debt [cite: 2991, 2992]. — `GAZ-VID` `[single-source]`
- Inspite of the dependence on one crop, namely wheat, the District showed a diminution of this crop from the average of 5,54,339 acres for the five years from 1934-35 to 1938-39 to only 2,08,269 acres in 1943-44 [cite: 2223]. — `GAZ-VID` `[single-source]`
- The Ganga king, Narasimha I (1253-1286 A. D.), married I Sîtâdevî, the daughter of a Malava king A Gujarat 2 prince married a princess of the Paramara dynasty. — `GAN` `[single-source]`
- Gram gave an outturn of 43.3 thousand metric tons in 1967-68, which more than doubled to 79.5 thousand metric tons in 1972-73 [cite: 2242]. — `GAZ-VID` `[single-source]`
- The area devoted to cultivation of wheat was 1,94,656 hectares in 1967-68 and increased to 235.5 thousand ha in 1972-73 [cite: 2225]. — `GAZ-VID` `[single-source]`
- The entire work deals with the Hindu Science of Architecture (Vāstuśāstra) but the title translates to *"The Architect of the Battle Field"*. — `SAM` `[single-source]`
- Waterymuhūrtta- Presided over by Varuņa, p.845, 869 (BS of Varahamihira) Samarangapa-sūtradhara Tula (Beam) having surface even as such projected as such gone into the central spot. — `SAM` `[single-source]`
- Their duties comprised performance of sacrifices (*Yajana*), studying (*Adhyayana*), giving charity (*Dāna*), officiating over sacrifices for others (*Yājana*), and teaching (*Adhyāpana*) [cite: 2776, 2777]. — `SAM` `[single-source]`
- Some portions of some works are connected with this subject — for example, the *Matsya Purana*, *Agni Purana*, *Garuda Purana*, *Vishnudharmottara Purana*, Kautilya's *Arthashastra*, the *Shukra-niti-sara* and so on. — `RAJ-E` `[single-source]`
- In the north of Nila mountain and to the south of Śveta mountain, the fifth varșa, highly gorgeous, is known as Ramyaka [cite: 857, 861, 863]. — `SAM` `[single-source]`
- Total outward shipments from Sironj Mandi in 1970-71 included: wheat 41,953 qtls; gram 52,512 qtls; juar 34,116 qtls; and linseed (*alsi*) 20,301 qtls [cite: 3396]. — `GAZ-VID` `[single-source]`
- In the varṣa named Kimpuruşa, the ladies and gents are inured to eating *Plakṣa*⁷ [cite: 893, 894], and live upto the span of ten thousand years, being by complexion of burnished gold colour [cite: 895, 897]. — `SAM` `[single-source]`
- In Bhadrāśva, the men and women have a complexion like the hollow of a white lotus [cite: 908, 909]; they feed on blue mango fruit and live an age equal to twenty thousand years [cite: 910, 911]. — `SAM` `[single-source]`
- To plan, survey, construct and maintain the irrigation works in the District there is an office of the Executive Engineer, Irrigation Division, Vidisha, functioning since 20th June, 1964. — `GAZ-VID` `[single-source]`
- State procurement operates under the *MP Wheat Procurement (Levy) Order of 1965* and *1968*, imposing a 50 per cent levy on licensed dealers [cite: 3486, 3498]. — `GAZ-VID` `[single-source]`
- In the Ilāvrta varșa, the men emerge with topaz or ruby-like complexions [cite: 902]; they have food from the rose-apple fruit juice (*Jambū-phala*) and live up to twelve and a half thousand years [cite: 903, 905]. — `SAM` `[single-source]`
- Important annual fairs include the Lateri Mela (December), Sankrant fair at Rajghat Barat, and the Ramlila fairs at Basoda and Gyaraspur. — `GAZ-VID` `[single-source]`
- Mahāvrata festival referred to the Tândya Brāhmaņa (V.5-1.9-21, p.155-157 by Cinnasvami Śāstri and Kātyāyana-śrauta Sūtra (XIII.2.21-27, p.28-29). — `SAM` `[single-source]`
- Barely represented in this bucket, so anything resting on them is a thin reed: `BET-K` — `[gap]`

### C11.6 — having, created, create, deserves, norm

> central latā is to be created as equipped with the framework of Śūrasena. **Sanskrit (Śloka):** `ग्रीवा सार्धपदोत्सेधा कार्या द्विपदमण्डकम्।` **Sanskrit (Śloka):** `भागेन च(म)ण्डिकां कुर्यात् कलशं तु चतुष्पदम्।।१९८।।` **English Translation:** *Grīvā may be having an elevation of one and half padas required to be created as such* and Aṇḍaka of pada twain. By a single pada one may create Maṇḍikā¹ and Kalaśa of four padas. **Sanskrit (Śloka):** `एकोनत्रिंशदण्डोऽयं प्रासादः शुभलक…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 56: The Illustration of Sixty-Four Prāsādas Headed by Rucaka > 4. Deity Placement and Architectural Vulnerabilities (*Marmavedha*) > Avoiding Vulnerable · `samarangana-00907`

> [paraphrase — not a verbatim quote; source text unreliable] And likewise, those subsisting upon agriculture or husbandry, balance beams (i.e. weighing), Arts¹³ (fine or mechanical arts) and crafts, practical arts commodities or vendible articles, or saleable goods or trade and those subsisting on killing i.e. butchers and hunters or savages or shamble keepers or subsisting on slaughtering in slaughter houses, (persons of such sorts) should be settled and wherein and how possibly. [cite: 573] निवेशाः कीदृशाश्चैषां कियन्तो वा भवन्ति ते।…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. SAMARĀNGANA-SŪTRADHĀRA > CHAPTER 2: The Conversation Between Viśvakarmā and His Sons (Mānasa Putras) > FOOTNOTES & TEXTUAL CRITICAL NOTES > Chapter 2 Footnotes · `samarangana-00060`

> Chapter 35 occurs as Chapter 20 in Dr. D.N. Shukla's text, pp. 81-83 and 85-88. 2. Matsya Purāņa says the rite of Bali-puja before the construction वास्तूपशमनं कुर्यात्समिद्भिर्बलिकर्मणा। जीर्णोद्धारे तथोद्याने तथा गृहनिवेशने। वास्तूपशमनं कुर्यात्पूर्वमेव विचक्षणः । एकाशीतिपदं लिख्य वास्तुमध्ये च पृष्ठतः॥ होमस्त्रिमण्डले कार्यः कुण्डे हस्तप्रमाणके। यवैः कृष्णतिलैस्तद्वत्समिद्भिः क्षीरवृक्षजैः॥ पालाशैः खादिरैश्चापि मधुसर्पिः समन्वितैः । कुशदूर्वामयैर्वापि मधुसर्पिः समन्वितैः।।…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 35: The Rite named the laying of Foundation Stones · `samarangana-00527`

> ``` # Chapter 48: The observations on the defects of building constructions CHAPTER 48 The observations on the defects of building constructions¹ अतः परं गृहादीनामप्रशस्तसमुच्छ्रितम्। क्रियते कथितं यस्मादेकत्र सुसमं भवेत् ।।१।। After this we shall dilate upon the eruption of indecent norms of the buildings and the like whereby is being given an account the way it may assume a temperate norm. रक्षोम्बुनाथकीनाशमरुद्दहनदिक्प्लवा। मध्यप्लवा च भूर्व्याधिदारिद्यमरकावहा।। २ ।। वह्नि…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 47: The pre-requisites of a Vedi · `samarangana-00673`

### C11.2 — town, temple, people, market, period

> The construction period of this Darwaza looks to be 11$^{th}$ century CE. It is situated at GPS 23.54.00.1 N and 78.03.27.8 E. Purana Bazaar Darwaza that is located inside the Udaypur village towards the southeast of Neelkantheshwar Temple. This structure is located in khasra no. 735/3 having an area of 0.042 ha. It is currently in Government ownership. The gateway is ascended from the south and is on higher ground. It acts as an access to the Purana Bazaar area. The eastern …
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 52 · `intach-2022-udaypur-00208`

> They arc raja, mahanlja, mahe^vara, kshatrapa and mahaksha- trapa.2 We shall now try to give a clear picture of the revenue and expenditure of the stale of Bhoja. I'cr this we arc to depend mainly upon the statements of the cpigraphic records, the infor- mation supplied by the contemporary smriti-writers and the accounts of the foreign travellers. The principal sources of revenue to the Paramara government known to us were : 1. Share of the product of the fields. 2. House lax…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00383`

> * **CHAPTER I: GENERAL** (Pages 1-20) Location and extent; Origin of the name; Topography; Drainage; Geology; Economic minerals; Flora; Fauna; Climate. * **CHAPTER II: HISTORY** (Pages 21-53) Prehistory; The Mauryas; Vidisha as a City State; The Kanvas; The Nagas; The Vakatakas; The Imperial and Later Guptas; The Kalachuris of Mahishmati; Paramars; Sultans of Malwa; The Mughals; The Marathas; Amir Khan Pindari; Great Revolt of 1857; Freedom Movement, Representative Government…
> — **GAZ-VID** · *Madhya Pradesh District Gazetteers: Vidisha* · p. — · `vidisha-gazetteer-1979-00005`

> In the Paramara Bhoj's source-work on the science of architecture, the *Samarangana-sutradhara*, the facts relating to it, sanctioned by all the shastras, are presented. According to it, when the dwelling-ground of gods, humans, elephants, cattle, horses and so forth is constructed of brick, stone, wood, iron, nails and the like, the craft-knowers call it *vastu*. Under this craft alone are constructed the village (*grama*), town (*puri*), *kheta*, *karvataka*, fort (*durga*)…
> — **RAJ-E** · *King Bhoj and Paramara-period Town Architecture (English translation)* · p. 23 · `rajpurohit-bhoj-en-00086`

### C11.5 — iast, aura, haiṃ, tathā, para

> श्रेष्ठियों तथा देश के महान् लोगों को दक्षिण में बसायें। कसाई, जल्लाद आदि को *[IAST] śreṣṭhiyoṃ tathā deśa ke mahān logoṃ ko dakṣiṇa meṃ basāyeṃ| kasāī, jallāda ādi ko* नैऋत्य दिशा में कर दें। 197 *[IAST] naiṛtya diśā meṃ kara deṃ| 197* कोपपाल, महामात्र (राज्य का बड़ा अधिकारी), आदेशिक (ज्योतिषी या सेनापति), *[IAST] kopapāla, mahāmātra (rājya kā bar̤ā adhikārī), ādeśika (jyotiṣī yā senāpati),* कारीगर, नियामक (सारथि, महावत) आदि को पश्चिम दिशा में बसायें। 198 *[IAST] kārīgara, n…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 52 · `bhojdev-hi-00227`

> पश्चिमाभिमुख घर का द्वार कुसुम हो तथा शाला गावी हो तो उसे सारभ समझे। सौरभ में निवास करते हुए गृहस्थ सदा प्रसन्न रहता है। कृषि और वाणिज्य सफल होता है तथा पुत्र वश में रहते हैं। 39-40 *[IAST] paścimābhimukha ghara kā dvāra kusuma ho tathā śālā gāvī ho to use sārabha samajhe| saurabha meṃ nivāsa karate hue gṛhastha sadā prasanna rahatā hai| kṛṣi aura vāṇijya saphala hotā hai tathā putra vaśa meṃ rahate haiṃ| 39-40*
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 80 · `bhojdev-hi-00358`

> [paraphrase — not a verbatim quote; source text unreliable] ` अभ्यस्यमाने हि प्रत्याहारे तथा वश्यानि आयत्तानीन्द्रियाणि सम्प यथा बाह्यविषयाभिमुखतां नीयमानात्यपि न यान्ति इत्यथः ॥ ५५ ॥ Lt निष्पद्यते (पाठा० | 0 a t विषयापेक्षको (पाठा०), विषयदयापेक्षको (पग i तदेवं शप्रथमपादोक्तयोगस्याङ्गभूतक्लेशतनूकरणफलं क्रियायोगमभिधाय _ कलेशानामुद्देशं स्वरूपं कारणं क्षेत्रं फलञ्चोक्त्वा, कर्मणामपि भेदं कारणं स्वरूपं \ फृहञ्चाभिघाय, विपाकस्य कारणं स्वरूपञ्चाभिहितम ; ततस्त्याज्यत्वात ब्ञेशादीनां ज्ञानव्यतिरेकेण त्यागस्य अशक्यत्वाज्‌ ज्ञानस्य च शास्त्राय…
> — **RAJM** · *Pātañjala-Yogasūtram with the Rājamārtaṇḍa-vṛtti of Bhojadeva (ed. Ram Shankar Bhattacharya)* · p. 38 · `rajamartanda-bhoja-00138`

> 314 पूर्वामुखं गृहं यत्तुं द्वारं माहेन्द्रसंयुतम् । *[IAST] 314 pūrvāmukhaṃ gṛhaṃ yattuṃ dvāraṃ māhendrasaṃyutam |* हस्तिनी च भवेच्छाला तद् गृहं भद्रसंज्ञितम् ।। 135 *[IAST] hastinī ca bhavecchālā tad gṛhaṃ bhadrasaṃjñitam || 135* 315 भद्रं भद्रकरं भर्तुर्यशोबलविवर्धनम् । *[IAST] 315 bhadraṃ bhadrakaraṃ bharturyaśobalavivardhanam |* सिध्यन्ति चास्य कार्याणि भद्राख्ये वसतो गृहे ।। 136 *[IAST] sidhyanti cāsya kāryāṇi bhadrākhye vasato gṛhe || 136* 316 दक्षिणाभिमुखं वेश्म द्वार…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 77 · `bhojdev-hi-00338`

### C11.4 — district, village, land, revenue, government

> Under the current and projected circumstances, we expect agricultural water demand to increase in the catchment. Since agriculture in the catchment is primarily rainfed [50] therefore, any deviation in the rainfall will eventually affect the yield of crops. Mall et al. [52] also found that the monsoon rainfall has a high correlation (0.8) with Kharif crop production anomalies. Therefore, Rabi crops in the winter season may be affected due to lower rainfall in this season and …
> — **BET-K** · *Streamflow of the Betwa River under the Combined Effect of LU-LC and Climate Change* · p. 12 · `kumar-2023-betwa-00050`

> Insc). Econo mic Condition The paddy was amongst the chief crops throughout northern India. Different kinds of rice were produced there. The pros- perity of the people mainly depended upon the richness of this crop. Suearcane was largely produced. This was one of the most important commercial crops. Candy Sugar and J^8!-y are referred to in the contemporary inscriptions.^ The cultivation of su.ar-cane is mentioned in the inscriptions of central India* and Mjputana.* Kalhaija …
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00719`

> (watered by rain\ The term ‘Kshetra’ is very often recorded in the inscriptions of this period. 2 It generally means a field. But Basak® and Pargiter^ interpret ‘kshetra’ as cultivable field. In the Amarakosa also it is defined as a special type of land capable of producing all kinds of crops.® There were, however, two types of cultivable lands, viz the dry land which required ample irrigation, and the wet land which required less water. The latter type referred to in the gra…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00715`

> The major population of Udaypur is engaged in agriculture and for further study and better livelihood opportunities, people relocate to the different nearby cities like Vidisha, Bhopal, Indore etc a section of the village population is engaged in the stone mining occupation as well which creates new opportunities for the local people and better livelihood.
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 37 · `intach-2022-udaypur-00165`

### C11.3 — cite, total, wheat, jowar, gram

> Vidisha is fundamentally a **Rabi crop area** (Rabi to Kharif ratio is 65:35). * **Wheat:** The primary crop, occupying 50% of the entire cropped area due to the nutrient-rich black alluvial soil. * **Gram & Jowar:** Command 18% and 8% of the area, respectively. Jowar is the largest Kharif crop. * **Poppy Discontinuance:** Opium poppy cultivation, which once formed a thriving commercial trade in Bhilsa during the 19th century, was completely phased out after Independence, rel…
> — **GAZ-VID** · *Madhya Pradesh District Gazetteers: Vidisha* · p. — · `vidisha-gazetteer-1979-00051`

> **AGRICULTURE** 1. FOOD CROPS — Dr. M. S. Swaminathan, Director, Indian Agricultural Research Institute, New Delhi. **ARCHAEOLOGY** 2. THE STORY OF INDIAN ARCHAEOLOGY — Shri O. P. Tandon, Banaras Hindu University. **BOTANY** 3. COMMON INDIAN FERNS — Dr. S. C. Verma, Department of Botany, Punjab University.
> — **DEV** · *Temples of North India* · p. 127 · `deva-1969-temples-00333`

> Irrigation historically played a minor role due to the naturally high moisture-retention capacity of the black cotton soil (*mar*). However, intense cultivation has accelerated irrigation projects. * **Canals & Tanks:** Canal systems have rapidly overtaken traditional well irrigation. Major projects include the **Kethan Medium Irrigation Project** (envisaging an 18-meter high dam to irrigate 5,000 acres) and the **Halali Major Irrigation Project** (designed to irrigate 81,600…
> — **GAZ-VID** · *Madhya Pradesh District Gazetteers: Vidisha* · p. — · `vidisha-gazetteer-1979-00050`

> | Seed and Crop | Year of Introduction | Nature and Quality | | :--- | :--- | :--- | | **Wheat** | | | | C. 591 | 1950-51 | Old variety, high yielding, good market value, partially rust-resistant. | | Hy. 65 | 1958-59 | Drought resistant with high yield | | No. 281 | 1959-60 | High yielding, high market value | | Mexican varieties (Larma & Sonora-64) | 1966-67 | Rust-resistant, high yielding variety | | Sonalika, R.R.-21, S-227 | 1967-68 | High market value and yield | | **Gr…
> — **GAZ-VID** · *Madhya Pradesh District Gazetteers: Vidisha* · p. — · `vidisha-gazetteer-1979-00080`

### C11.1 — general

> हर दिन दूर-दूर से लोग उदयपुर आते हैं। ज्यादातर सिर्फ 11 वीं सदी के मंदिर के दर्शन करने आते हैं और वे भी सिर्फ महादेव की पूजा-अर्चना के लिए। गर्भगृह से बाहर आकर वे हक्के-बक्के से गर्दन ऊंची करके मंदिर के स्थापत्य को देखते हैं। मोबाइल आजकल सबके पास हैं तो फोटो खींचना फूल चढ़ाने जैसी आवश्यक रस्म बन गई है ताकि सोशल मीडिया पर प्रसारित कर सकें। इक्का-दुक्का ही कोई पत्थरों पर उकेरे इस चमत्कार की डिटेल्स में जाना चाहता होगा। न के बराबर। उन्हें इतिहास में कोई रुचि नहीं है। उदयपुर या आ…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00054`

> हेलियोडोरस दर्शक दीर्घा में अकेला बैठा है चुपचाप... देखते ही देखते विदिशा एक रंगमंच में बदल गया है, जहां बारी-बारी से किरदार आ और जा रहे हैं। वह मजे से प्रेम के नमकीन का स्वाद चख रहा है। कमल की कड़क उबली चाय ने उसे तरोताजा कर दिया है। वह कांच मंदिर से दौड़ लगाकर भीड़ भरे बाजारों में धक्के खाता हुआ रायसेन गेट से टकराते हुए काला पहाड़ नाम के पत्थरों के एक ढेर तक पहुंच गया है, जहां एक ध्वस्त मंदिर के अवशेष बाहर आने को बेचैन हैं। यहां जमीन के भीतर खुदाई नहीं करनी है। बस जमीन पर र…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00209`

> एक राम मंदिर के पिछवाड़े के पत्थर सबसे पुराने थे, जिनके पास बड़े बाजार की पुरानी दुकानों की इमारतें शायद बाद में खड़ी की जाती रही होंगी। लेकिन ये सब भी पांच सौ साल से ज्यादा ही पुराने रहे होंगे। मैंने सुझाया कि हर हफ्ते उदयपुर की हेरिटेज टीम इन झड़ियों की सफाई करने का काम हाथ में ले। हम केवल ये जटाजूट ही साफ कर दें तो उदयपुर का साफ चेहरा सामने आ सकता है। हमें हर काम सरकार पर छोड़कर नहीं रखना चाहिए। भारत स्वच्छता अभियान का एक स्थानीय चरण यहां शुरू किया जाए, जिसमें कूड़ा साफ नह…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00329`

> देश भर में ऐसे तमाम किले और गढ़ियां गुमनामी की हालत में ढह रही हैं, जिनके लिखित इतिहास कहीं नहीं हैं। जहां कोई शिलालेख नहीं हैं और जो पूरी तरह से जंगलों और वीरानों में गुम हैं। इतने मजबूत निर्माण पीढ़ियों ने किए होंगे। सदियों तक जीवन यहां पनपा होगा। जहां कारोबारी होंगे, बाजार होंगे और सांस्कृतिक रौनक भी रही ही होगी। खंडित मूर्तियां गवाह हैं कि मंदिर रहे होंगे। स्थापत्य के जानकार रहे होंगे, जो ऐसे शानदार मंदिर बना रहे थे। इनमें धन लगाने वाले राजवंश और दानवीर व्यापारी रहे होंगे…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00563`

**Gaps.** barely represented here: `BET-K`.

## C12 — People of the Plateau: Communities, Languages and Everyday Life

[↑ contents](#contents)

**Coverage.** 1,667 chunks from 26 sources (`ADH`, `BET-K`, `BHJ-H`, `DEV`, `GAN`, `GAZ-VID`, `GUP`, `HAR`, `INT-ARC`, `INT-GEO`, `KRAM-1`, `KRAM-2`, `PAN`, `PAR`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `RAJM`, `SAM`, `SIN-B`, `SIN-S`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: primary_authorial_paramara 697, secondary_core 483, primary_scriptural 153, reference_tertiary 122, secondary_comparative 107, field_observation_reportage 43, field_observation_survey 30, contextual_thematic 18, primary_epigraphic 13, environmental_scientific 1. The largest single contributor is `SAM` with 694 chunks (42% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- The agricultural and landed gentry in the countryside includes various Rajput families (Tomars, Bhadorias, Kacchawahas, Jadhos, Sikarwars, Khichis, Chandellas, Bundelas, Pawars, etc.), alongside the Gujars, Jats, and Ahirs in the north. — `PAT-INS` `[single-source]`
- Historically, *Bundeli* was the dominant dialect in 1908, shifting to *Malwi* in the 1921–1941 censuses, before standard Hindi became widely returned. — `GAZ-VID` `[single-source]`
- In Kuru varșa, the men and women subsist upon wish-fulfilling trees that shower fruits cherished by them [cite: 925]; they live twelve and a half thousand years, bearing white complexions like the gods' progenies [cite: 926, 928]. — `SAM` `[single-source]`
- The Hindu population contains nearly 11,11,716 Adivasis (scheduled aboriginal tribes) and 13,23,981 Harijans. — `PAT-INS` `[single-source]`
- Other tribes include the Korkus, Mundas, Gonds (inhabiting the eastern belt near Bhilsa/Gondwana), and Meenas (in the northern Chambal tracts of Shivapuri). — `PAT-INS` `[single-source]`
- Their age is ten thousand autumns (*Śarads*), and they feed on *Panasa* (breadfruit) [cite: 915, 917]. — `SAM` `[single-source]`
- During the period under survey, they, like the Brahma- nas, came to be known as Ganda, Kayasthavam§a, Mathuranvaya Kayastha Katariyanvaya, Srivastava and Nigama Kayastha, 1. — `SIN-B` `[single-source]`
- Waterymuhūrtta- Presided over by Varuņa, p.845, 869 (BS of Varahamihira) Samarangapa-sūtradhara Tula (Beam) having surface even as such projected as such gone into the central spot. — `SAM` `[single-source]`
- The whole of northern Madhya Bharat is included in the sphere of Western Hindi, with its respectable dialects of Brij-Bhasha prevalent in the northern extremities and Bundeli spoken in the central parts of northern Madhya Bharat. — `PAT-CH` · `PAT-INS` · `PAT-TEM` `[established]`
- In the varṣa named Kimpuruşa, the ladies and gents are inured to eating *Plakṣa*⁷ [cite: 893, 894], and live upto the span of ten thousand years, being by complexion of burnished gold colour [cite: 895, 897]. — `SAM` `[single-source]`
- In Bhadrāśva, the men and women have a complexion like the hollow of a white lotus [cite: 908, 909]; they feed on blue mango fruit and live an age equal to twenty thousand years [cite: 910, 911]. — `SAM` `[single-source]`
- In the Ilāvrta varșa, the men emerge with topaz or ruby-like complexions [cite: 902]; they have food from the rose-apple fruit juice (*Jambū-phala*) and live up to twelve and a half thousand years [cite: 903, 905]. — `SAM` `[single-source]`
- Through the southern direction of Himalaya, surrounded by the salt ocean from the other side [cite: 846, 847], is the Varșa named "Bhārata", the very primeval one, having the shape of an arc or bow [cite: 848, 851]. — `SAM` `[single-source]`
- Engraved by (silavata) mason Suvi of Gaurajation Samvat 1698 Chaitravadi 11. — `INT-GEO` `[single-source]`
- Narpati Nalh composed the *Bisaldev-raso* in Samvat 1272, in which the marriage of Bhoj's daughter with Bisaldev is discussed. — `RAJ-E` `[single-source]`
- Their dialect is a mixture of Gujarati, Malwi, and Marathi, with Munda words. — `PAT-INS` `[single-source]`
- Important annual fairs include the Lateri Mela (December), Sankrant fair at Rajghat Barat, and the Ramlila fairs at Basoda and Gyaraspur. — `GAZ-VID` `[single-source]`
- Tri-bhadra, Catur-bhadra, & Pañca-bhadra Clusters * **Tri-bhadra (56 Options)**: Advanced models including *Aindra, Viloma, Āyāma, Vadha, Ekākṣa, Antika, Prakāśa,* and *Paitra* matrices [cite: 6456, 6462, 6468]. — `SAM` `[single-source]`
- Barely represented in this bucket, so anything resting on them is a thin reed: `BET-K`, `PAR`, `SIN-S` — `[gap]`

### C12.5 — thus, great, said, lord, will

> and a section known as "Guguli" Of the Ksatriya and the other castes, the following families are known :- (a) Hathundi of the Rathor tribe. (b) Devada-a branch of the Cahamânas, 3 (c) Pragvâța, (c) Ûesavalas or Oisavalas. (e) Srîmâlas. (f) Dharkatas. (g) Pratihara Rajputs. 4 The Bhils, who were aboriginals, formed an important section of the population. Their chief occupations were the cultivation of the soil, painting and gambling, and they sometimes acted as guides in the h…
> — **GAN** · *History of the Paramāra Dynasty* · p. 102 · `ganguly-paramara-00704`

> As a caste, Kayasthas appear first in the inscriptions of the llth C.A D, Prior to this they were s’mply ranked as govern- ment officials and not as a caste. In the Rewa inscription dated K. S. 8C0/1048-49 A. D., the origin and pedigree of the Kayasthas is given. During the period under survey, they, like the Brahma- nas, came to be known as Ganda, Kayasthavam§a, Mathuranvaya Kayastha Katariyanvaya, Srivastava and Nigama Kayastha, 1. i?.7’.,p. 77. 2. Kane : H.D.S. II, 175-76,…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00578`

> 6. dory that ivui- Gurjaradesa, p. 425. 7. Chapt.XVU. 8. 11,3.4. 216 Bl.oja ParafnSra and his Times Baudhayana* allow freely iater-caste dinners. But the custom had begun to decline in the period under survey, for a number of later Smritis either restrict or condemn it. Angiras® prohibits the dinner with a Siidra and permits one with a Kshattriya only on days of religious festivity and with a Vaishya when in distress.' Yama and Vyasa* declare that a Brahmana should beg cooked…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00656`

> three high castes) much earlier than the period under survey, the approximation of the Vaisyas to the Sudras began as early as Manu' and Baudhayana Dharmasutra.“ H.C. Rawlinson observes that during the 11th C. A.D., the Vaisya caste was disappearing and there was a growing tendency to regard the Vaisyas as Sudras and religious rites were confined to the two higher castes.’ Altekar and Ghurye rightly hold that the Vaisyas were levelled' down to the position of the Sudras.^ Thu…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00565`

### C12.4 — population, vidisha, people, town, state

> The Hindu population contains nearly 11,11,716 Adivasis (scheduled aboriginal tribes) and 13,23,981 Harijans. The aboriginal tribes inhabit the hilly tracts of the Vindhyas and Satpuras in the south and south-west. Among them, the Bhilalas claim Rajput-Bhil lineage and follow mainstream Hindu customs. The Bhils constitute the bulk of the tribal populace, divided occupationally into settled cultivators and forest hill-men. The typical Bhil is short-statured, dark-complexioned,…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00020`

> The whole of northern Madhya Bharat is included in the sphere of Western Hindi, with its respectable dialects of Brij-Bhasha prevalent in the northern extremities and Bundeli spoken in the central parts of northern Madhya Bharat. Of these, the letters have a good literature to their credit. The last census returns have shown nearly 59 lakhs of the population speaking Western Hindi, indicating that even parts of Malwa proper have now aligned themselves with this group. It will…
> — **PAT-CH** · *The Cultural Heritage of Madhya Bharat* · p. — · `patil-1952-00055` · also **PAT-TEM** · `patil-composite-temples-00055`

> 100 / King Bhoj and Paramara-period Town Architecture Between south and west there should be one road. In it there may or may not be a rampart. The Chaturmukha village should be quadrangular, and the rampart likewise. The length should run east-west. All around there should be a great avenue and two footpaths. In the four directions there should be four avenues, with a gate at their ends — one great gate and the rest sub-gates. There should be many small avenues (lanes). On t…
> — **RAJ-E** · *King Bhoj and Paramara-period Town Architecture (English translation)* · p. 100 · `rajpurohit-bhoj-en-00347`

### C12.6 — created, deserves, parts, create, half

> ``` Chapter 74 CHAPTER 74 Aņdaka Pramaņa parabola and the measurement specified for the drawings for the human face and torso. अथात्र प्रक्रमायाता कथ्यते ऽण्डकवर्तना। कायप्रमाणमपि च जातिभावादिसंश्रयम्।। १।। Now come to the fore in serial order is being illustrated Andakavartana, the measurement of the body based on the nature of the species or caste. अथ (मधोतिरालिख्य तोरका सन्निवेशयेत्। तारका ?) त्रयमालेख्य तत्रान (न) समायति ।। २ ।। Having drawn a circle immediately one may i…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra > Architectural Treatise of Mahārājādhirāja Śrī Bhojadeva > [Original Page Source: 14] · `samarangana-01397`

> The parts that are spoken of as of $15\frac{1}{2}$ parts, to these one may divide by ten. And Garbha and the breadth of the wall and likewise Khuravarandikā may there be. जड्डोत्सेधः क्षितिश्चाद्या रेखोच्छ्रायश्च पूर्ववत्। विंशत्या शिखरं भाज्यं पादहीनाश्युक्तया ।।४२।। The elevation of the Jangha and the first storey, and the height of Rekha as before and by a twenty may the Śikhara be divided by 8% parts. पञ्चभागसमुत्सेधा द्वितीया भूमिका भवेत्। पदपादविही (नाः स्युस्तिस्त्रोऽन…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra > Architectural Treatise of Mahārājādhirāja Śrī Bhojadeva > [Original Page Source: 14] · `samarangana-01199`

> करमात्रसमुत्सेधं कर्तव्यं मत्तवारणम्।।५३।। ve to the mind deserves to be Kūtāgāra³ by a part triad above the Vedī being attr created and having elevation of a single cubit deserves to be created the Matta Väraņaka (railing or aisle). सुखलीलाशनार्थं तत् सप्रवेशं सनिर्गमम् । (मन्द्राग्रे सुकाग्रे ?) च प्रतोल्यत्रे तथैव च। तोरणं त्रिविधं ज्ञेयं कनीयोमध्यमोत्तमम्।।५ ४।। For the purpose of food taking, sport and comfort, that may be equipped with entrance, and exit in front of Man…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra > Architectural Treatise of Mahārājādhirāja Śrī Bhojadeva > [Original Page Source: 14] · `samarangana-01300`

> Chapter 29 आयामार्थेन विस्तारं सर्वं शय्यासु कल्पयेत्। यद्वा निजाष्टभागेन षड्भागेनाथवाधिकम् ।।१२।। The width may be by a half of the length, completely, in all the couches one may create or by the one eighth part or by one sixth part or more. विप्राणां शस्यते शय्या दैर्येणाङ्गुलसप्ततिः। द्वाभ्यां द्वाभ्यामङ्गुलाभ्यां हीना स्याच्छेषवर्णिनाम् ।। १३ ।। Of Brahmaņas is appreciated the couch in length as seventy Angulas i.e. 52.5 inches and lessened by two angulas each i.e. 68 ang…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 29: Śayanāsana Lakşaņa · `samarangana-00317`

### C12.1 — having, house, apte, those, being

> यथा - ब्रह्मा तथा विश्वकर्मा की उपस्थिति, प्रलय के बाद सृष्टि, भुवनकोश, युगों में मानवस्थिति, वर्णाश्रम, भूपरीक्षा, हस्तलक्षण, पुरानिवेश, वास्तुत्रय, नालियाँ, वास्तुपुरुष, राजनिवेश, वनप्रवेश, इन्द्रध्वज, नगरादिसंज्ञा, चतुश्शाल, निम्नोच्चादिफल, 72 त्रिशाललक्षण, द्विशाल, एकशाल, द्वार-पीठ-भित्तिमान, समस्त गृह, आयादि निर्णय, सभाष्टक, गृहद्रव्यप्रमाण, शयनासन, राजगृह, यन्त्रविधान, गजशाला, अश्वशाला, अप्रयोज्य-प्रयोज्य, शिलान्यासविधि, वास्तुपूजा, कीलकसूत्र, वास्तुसंस्थान, द्वारगुणदोष…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 22 · `bhojdev-hi-00107`

> *[Sanskrit line as in source; the OCR contains errors and breaks (___). English of the Hindi gloss follows each.]* > **1. ओं ॥ संवत् १२८६ वर्षे कार्ति[क] शुदि ____** > *May there be accomplishment. In the year Samvat 1286, Kartik Shudi ____* > > **2. शुक्रे देव श्री उदयेश्वर ____** > *On Friday, Dev Shri Udayeshvar ____* > > **3. सन्निधौ समस्त प्रशस्तोपेत ____** > *in the presence [of], endowed with all renown ____* > > **4. समधिगत पंचशब्दालंका(र) ____** > *who has attained t…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00553`

> [paraphrase — not a verbatim quote; source text unreliable] * **Āmalaka (आमलक):** A massive, ribbed or serrated circular stone disc crowning the summit of a northern (*Nagara*) *shikhara* spire [cite: 6749, 8272]. * **Aṅgabhāva (अङ्गभाव):** The stylized bodily posture, gesture, or stance expressing distinct emotional states (*rasas*) in both classical dance and sculpture [cite: 7957]. * **Antarāla (अन्तराल):** A small intermediate chamber, vestibule, or ante-chamber connecting the dark inner sanctum with the pillared assembly hall [ci…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00146`

> one fourth (i. c, 9 ft) in width. Every city was to have an cfTicicnt system of public drainage and drains were always to be covered cither with stone-pieces or wooden planks,^ The profession and caste of a particular person determined his place of residence in a city, which the Samarahgana-Sutradhara refers to by the expres- sion ‘Jativarnfidhivasa’. According to it, Ghee and fruit-sellers
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-01034`

### C12.2 — iast, aura, haiṃ, tathā, para

> और जो भी विभिन्न जातियों (वस्तुओं/प्राणियों) की चेष्टाएँ और जो जाति विरुद्ध हों *[IAST] aura jo bhī vibhinna jātiyoṃ (vastuoṃ/prāṇiyoṃ) kī ceṣṭāe~ aura jo jāti viruddha hoṃ* वे सब भी यन्त्र के साधन से सम्यक् सिद्ध हो जाती हैं। 132 *[IAST] ve saba bhī yantra ke sādhana se samyak siddha ho jātī haiṃ| 132*
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 89 · `bhojdev-hi-00393`

> *[IAST] 353 ucchrāyastu jalasya syāt kvacid bhūje'pi śasyate |* गीतं नृत्यं च वाद्यं च पटहो वंश एव च । 129 *[IAST] gītaṃ nṛtyaṃ ca vādyaṃ ca paṭaho vaṃśa eva ca | 129* 354 वीणा च कांस्यतालश्च तृमिला करटापि च । *[IAST] 354 vīṇā ca kāṃsyatālaśca tṛmilā karaṭāpi ca |* यत्किञ्चिदन्यदप्यत्र वादित्रादि विभाव्यते । 130 *[IAST] yatkiñcidanyadapyatra vāditrādi vibhāvyate | 130* 355 समस्तमपि तद् यन्त्राज्जायते कल्पनावशात् । *[IAST] 355 samastamapi tad yantrājjāyate kalpanāvaśāt |* नृत्…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 83 · `bhojdev-hi-00368`

> प्रथम का विभाग, प्रमाण, लक्षण और जाति-वर्ण के निवास को यहाँ यथावत् बताते हैं 188 *[IAST] prathama kā vibhāga, pramāṇa, lakṣaṇa aura jāti-varṇa ke nivāsa ko yahā~ yathāvat batāte haiṃ 188* सुवर्णकार सहित सभी अग्निजीवी और अन्य मजदूरों को आग्नेय (पूर्व-दक्षिण) दिशा में बसायें 189 *[IAST] suvarṇakāra sahita sabhī agnijīvī aura anya majadūroṃ ko āgneya (pūrva-dakṣiṇa) diśā meṃ basāyeṃ 189*
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 51 · `bhojdev-hi-00222`

> Trinetra (Bhairava), 76. Tri-Tirthankara, 174. Trailokyamohana, 83. Trimukha Yaksha, 177. Tripiṭaka, 112. Triple Umbrella, 175. Tripurabhairavi, 103. Tripurāntaka (Bhairava), 70, 76. Tripurāntaka-mūrti, 41. Trivikrama, 31, 32, 92, 93, 96, 97. Tulasā-Devī, 103.
> — **GUP** · *Iconography of the Hindus, Buddhists and Jains* · p. 258 · `gupte-1972-00854`

### C12.3 — cite, sanskrit, earth, humans, buddha

> शौचं द्विविघं-वाह्यमास्यन्तरञ्च ; वाह्यं मृज्जलादिभिः कायादिप्रक्षालनम्‌, _ ° नियमः ( पाठा० ) । * केषुचित्‌ संस्करणेषु एते तु जातिः इति पठ्यते, सोऽपपाठः । ¦ ‡ उच्यन्ते (पाठा०) । () परकीयेति क्वचिन्न । E = पातञ्जलयोगसूत्र-भोजवृत्ति :र आम्यन्तरं मैत्यादिभिश्चित्तमलानां प्रक्षालनम्‌ । सन्तोपस्तुष्टिः । शेषाः प्राग ग (२।१) कृतव्याख्यानाः । एते शौचादयो नियमदव्दवाच्या ॥३२॥ ग्रो कथमेषां योगाङ्ग त्वमित्याह-- ; दुः वितकंबाधने प्रतिपक्षभावनम्‌ ।॥ ३२ ॥ ग वितव्थन्ते इति वितर्का योगवरिपन्…
> — **RAJM** · *Pātañjala-Yogasūtram with the Rājamārtaṇḍa-vṛtti of Bhojadeva (ed. Ram Shankar Bhattacharya)* · p. 65 · `rajamartanda-bhoja-00123`

> > पृथिव्यां श्रीभोजदेवो धर्मसंरक्षणाय च । > देशमालवकोत्पन्नः श्रीराजगृहमेत्य च ॥ > भोजदेवो जयद्वेष्यान्सर्वेषां च प्रमूर्धनि । > न तत्तुल्यो जगत्यस्ति न भूतो न भविष्यति ॥ > x x x > अथर्ववेदे विहिता महाशान्तिरनेकशः । > कारापिता तेन यथा चोक्षा विहितदक्षिणा ॥ > x x x > श्रीमद्भोजपुरे विद्वानासीत्सोमेश्वरो द्विजः । > तत्पुत्रकेशवेनैषा कृता कौशिकपद्धतिः ॥ > > *(Sanskrit verses — in sense: "On earth, Shri Bhojadeva, born in the land of Malwa, came to the royal house for the protect…
> — **RAJ-E** · *King Bhoj and Paramara-period Town Architecture (English translation)* · p. 164 · `rajpurohit-bhoj-en-00483`

> [paraphrase — not a verbatim quote; source text unreliable] इन भ्रान्तियों के उद्भव में अन्ध श्रद्धा का भी वहुत कुछ हाथ यवां रहा है विभिन्न संप्रदायों की गुरुपरम्परा की ऐतिहासिकता मी ऐसी ही विपर्यस्त हे। + द्र० कल्पना ( फरवरी ६३ अंक ) में प्रकाशित मेरा लेख “कौटल्य के भाष्य ` कौटिल्य रूपान्तर का कारणः । पारणा ३--१।३४ वृत्ति में प्राणायाम की महत्ता के प्रसंग में भोज कहते ह “समस्तदोपक्षयकारित्वं चास्य आगमे श्रूयते” । यह मत स्मृति-पुराणादि में है- “'प्राणायासैदहेद्‌ दोपान्‌” ( मनु० ६।७२ ) । ४-विन्ध्यवासी का एक मत ( सत्त्वतप्यत्वमेव पुरुपत…
> — **RAJM** · *Pātañjala-Yogasūtram with the Rājamārtaṇḍa-vṛtti of Bhojadeva (ed. Ram Shankar Bhattacharya)* · p. 7 · `rajamartanda-bhoja-00009`

> इस ठोस दौलत से सब दमकते हैं। बस उदयपुर नहीं बनते। वैसे भी उदयपुर में रखा ही क्या है? खंडहर। उजाड़ टीले। बर्बाद तालाब और बावड़ियां। अपनी किस्मत पर रोते हुए पत्थरों के उजाड़ ढेरा। धूल और पत्थरों से भरी झारड़ियां। खदानों पर अपने दांत और पंजे गड़ाने वाले हर जाति और राजनीतिक वर्ग के इन लालची लकड़बग्घों में खदानों के मालिक, सब प्रजातियों के नेता, विदिशा से लेकर बासौदा तक के बड़े-छोटे अफसर सब एक कतार से शामिल हैं। लूट का यह एक शानदार टीम वर्क है।
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00305`

**Gaps.** barely represented here: `BET-K`, `PAR`, `SIN-S`.

## C13 — Stories of Udaypur: Festivals, Folklore and Oral Histories

[↑ contents](#contents)

**Coverage.** 1,972 chunks from 26 sources (`ADH`, `BET-K`, `BHJ-H`, `DEV`, `GAN`, `GAZ-VID`, `GUP`, `HAR`, `INT-ARC`, `INT-GEO`, `KRAM-1`, `KRAM-2`, `PAN`, `PAR`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `RAJM`, `SAM`, `SIN-B`, `SIN-S`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: field_observation_reportage 545, secondary_core 533, primary_authorial_paramara 340, primary_scriptural 188, secondary_comparative 148, field_observation_survey 84, contextual_thematic 71, reference_tertiary 45, primary_epigraphic 16, environmental_scientific 2. The largest single contributor is `SAM` with 338 chunks (17% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- Singh, Abhilash Khandekar, Anand Pandey, Girish Upadhyay, Shivkumar Vivek, and the word-scholar Ajit Vadnerkar — came to hear Katha Udaipur. — `TIW-E` `[single-source]`
- Santosh Kumar Verma is an assistant professor of history at the Girls' College of Ganj Basoda itself, whose Facebook page I got the chance to visit when the fresh tremors of Udaipur, on the Richter scale of history, reached him. — `TIW-E` `[single-source]`
- One day before Shivratri, the phone-call of Pragya Pravah's Deepak Sharma came. — `TIW-E` `[single-source]`
- Knowers of history and archaeology like Dr. Narayan Vyas and Pooja Saxena; the water expert Anil Agarwal; Deepak Sharma of Pragya Pravah; the former chairman of the M.P. — `TIW-E` `[single-source]`
- According to the Udaipur Prashasti (उदयपुर प्रशस्ति), King Bhoj defeated the Chedi king, Indraratha, Toggala, Bhima, and the kings of Karnata, Lata and Gurjara, as well as the Turushkas (Turks). — `RAJ-E` `[single-source]`
- The great Nilakantheśvara temple at Udayapur was built by Udayaditya in Sam 1116 = 1059 A. D. An ART AND CULTURE 259 inscription of the sixteenth century A. D. describes it as the most beautiful temple in India. — `GAN` `[single-source]`
- The great poet Padmagupta was a contemporary of both the kings, Vakpati-Muñja (A. D. 972-995) and his successor Sindhuraja. — `GAN` `[single-source]`
- Both the *'Udaipur Prashasti'* (a Sanskrit inscription) and *'Navasahasankacharitra'* (Shastri, 1867, Sarga 11, Śloka 14) mention King Upendra as the first great king. — `PAR` `[single-source]`
- She too was among the listeners of Katha Udaipur, and had, ever since, been determined that, before joining a new job afresh in Delhi, she must go to Udaipur and see what is there and what is happening. — `TIW-E` `[single-source]`
- Mahāvrata festival referred to the Tândya Brāhmaņa (V.5-1.9-21, p.155-157 by Cinnasvami Śāstri and Kātyāyana-śrauta Sūtra (XIII.2.21-27, p.28-29). — `SAM` `[single-source]`
- INTACH BHOPAL UDAYPUR INTACH Indian National Trust for Art and Cultural Heritage Bhopal Chapter Manjul Publishing House Udaypur. — `INT-ARC` `[single-source]`
- In the varṣa named Kimpuruşa, the ladies and gents are inured to eating *Plakṣa*⁷ [cite: 893, 894], and live upto the span of ten thousand years, being by complexion of burnished gold colour [cite: 895, 897]. — `SAM` `[single-source]`
- In Bhadrāśva, the men and women have a complexion like the hollow of a white lotus [cite: 908, 909]; they feed on blue mango fruit and live an age equal to twenty thousand years [cite: 910, 911]. — `SAM` `[single-source]`
- After I returned from Udaipur on the day of Mahashivratri, Deepak Sharma of Pragya Pravah sent me the link to his fresh post. — `TIW-E` `[single-source]`
- And with peaks made of Hema (i.e. gold), Hemakūța, this one was known as the mountain [cite: 827], to which serve perennially or to which keep occupied perennially Cāraṇas (heavenly charioteers⁶) and Guhyakas [cite: 828, 830]. — `SAM` `[single-source]`
- In the Ilāvrta varșa, the men emerge with topaz or ruby-like complexions [cite: 902]; they have food from the rose-apple fruit juice (*Jambū-phala*) and live up to twelve and a half thousand years [cite: 903, 905]. — `SAM` `[single-source]`
- According to a Jain text, in 1020 CE King Bhoj's son Viranarayana (वीरनारायण) founded Sevana (सेवाणा). — `RAJ-E` `[single-source]`
- Before the freedom-struggle of 1857 (in 1855–56 CE), Raja Shivprasad was an Inspector in the Education Department. — `RAJ-E` `[single-source]`
- Barely represented in this bucket, so anything resting on them is a thin reed: `BET-K`, `PAR` — `[gap]`

### C13.3 — bhoja, tradition, temple, paramara, india

> ART AND CULTURE 257 conversation, proceeded immediately to profit by the information she received, and administered the suggested dose to the king, whereupon he at once brought up the snake dead, as had been foretold; after which he proceeded to pour oil down the hole of the other snake, and having thus killed that also, took possession of the treasure. To commemorate this event, he built there a city and a temple and named them after himself. The above story is no doubt an a…
> — **GAN** · *History of the Paramāra Dynasty* · p. 102 · `ganguly-paramara-00559`

> which are less connected with King Vikramaditya and more with the conduct of women. The second folk-famous story is that of a cowherd boy who grazed cows. This story was written in detail, in English, about 125 years ago, by an Irish woman, Sister Nivedita, under the title "The Judgment Seat of Vikramaditya." According to the story, in Ujjayini, when an innocent cowherd boy, in play, went and sat on an earthen mound, his manner would change and his speech would become grave. …
> — **RAJ-E** · *King Bhoj and Paramara-period Town Architecture (English translation)* · p. 210 · `rajpurohit-bhoj-en-00691`

> to pay his obeisance at the Buddhist caves on the opposite shore. The Bhojpur lake stands to day as a testimony to the extent of the engineering skill and workmanship achieved by the people of Malwa under the magnificent rule of the Paramaras. The king Udayaditya founded the city of Udayapur, thirty miles to the north of Bhilsa. Tradition gives a legendary story in connection with the establishment of this city. It runs as follows:- One day the king, in the course of a huntin…
> — **GAN** · *History of the Paramāra Dynasty* · p. 102 · `ganguly-paramara-00557`

> As regards Navasahasanka-carita, we have also sufficient reason to believe that it represents a solid historical fact in the garb of a romantic story. The poet expressly tells us that the object of his narrative is to record the life-story of Sindhuraja, which he has undertaken, not from motives of poetic pride, but at the command of his master. That the book has something of an historical character, and is not purely fantastic panegyric, is further proved by the fact that th…
> — **GAN** · *History of the Paramāra Dynasty* · p. — · `ganguly-paramara-00177`

### C13.6 — having, created, norm, create, deserves

> Standing at the bottom of the oblong tank, and cowed down out of shame, having the protuberance of breasts covered up with sprout like hands, the fortunate one, looks at the beloved folk, herein in the process of splashes of or spraying of waters harnessed as such, (the beloved folk) having garments tightly fastened. रथदोलादिविधानं दारवमभिदध्महे वयं सम्यक्। यन्त्रभ्रमणककर्म प्रकीर्तितं पञ्चमं यत् तत् ।।१७३।। The wooden mechanism of the Rathadolā¹ (lit. a chariot hammock or sw…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 31: Named Yantravidhānaṁ i.e. The Chapter dealing with the Preparation of Mechanical Contrivances · `samarangana-00445`

> nail then being stroked he may speculate over the omens. गोविप्ररथनागाढ्याः कन्या नृपवरस्त्रियः। शङ्खदुन्दुभिवंशानां तथा गीतस्य च ध्वनिः ।।५०।। Richer kine, the Brahmaņas, and elephants, and chariots, the girls and the coquettes of the kings and likewise the sound of the conches, kettle drums, and flutes as also of the song. आविर्भवति यद्यस्मिन् हन्यमाने प्रभुस्तदा। सततं सुखमाप्नोति शान्त्यैश्वर्यैश्च वर्धते ।।५ १।। If gets into provenance herein, on its being stroked then th…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 37: Kīlaka Sūtrapāta (the insertion of nails and threads) · `samarangana-00550`

> देवयोनिगणस्तद्वत् पुरुषाश्च विनिन्दिताः ।॥४३॥ All those salubrious as such, deserve to be employed in all the equipments. And that very way the groups of the breeds of divinities and men uncensured ones. साक्रन्दाश्च न शस्यन्ते पीठशय्यासनादिषु। पुरस्तात् कीर्तितान्यत्र प्रयोक्तव्यानि यानि च।।४४॥ Crying along are not belauded on the backs, couches and seats. Those illustrated earlier deserve to be employed elsewhere also. तानि शस्तानि कक्षासु सभादेवकुलेषु च। दिव्यमानुषसम्बद्धा…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 33: The Equery of Steeds (and Chapter 34: Practicable and impracticable materials) · `samarangana-00513`

> [paraphrase — not a verbatim quote; source text unreliable] And which one modicum of organisation stands established by factual representation and what (work) regarding the (creation) of ramparts, turrets, and balconies or upper-storeyed apartments, the moats, mounds or the gates of fortified towns or ditches, has been undertaken. [cite: 466, 471] तमङ्गनिर्गमद्वारप्रतोल्यट्टालकादिभिः । कीदृशः प्रविभागश्च रथ्याचत्वरवर्त्मभिः ।।१५।। By the platforms¹ and exit gates the Broad ways or Principal roads through towns and villages and the upp…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. SAMARĀNGANA-SŪTRADHĀRA > CHAPTER 2: The Conversation Between Viśvakarmā and His Sons (Mānasa Putras) > FOOTNOTES & TEXTUAL CRITICAL NOTES > Chapter 2 Footnotes · `samarangana-00056`

### C13.2 — bhoj, king, temple, town, architecture

> Who had this Garhi built? Of what date is it? Any inscription, any story? The answers to all these questions are hardly to be found anywhere in all the documents written on this region; but in folk [memory], everywhere, there are many stories about any such place. Here too there are. Stories heard from the elders in the family. Tales heard across generations. From these tales you can weave the warp and weft of the original story. In the Garhi of Gyasi — who is this Gyasi? Bel…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00578`

> On one such delightful tale there was the ancient, now-unavailable, play *Vikranta-shudraka*; its story is nowadays found in Malwi relating to King Vikramaditya. Sometimes, combining several persons, the personality of a folk-hero is embellished. In known history, the beginning of the first millennium of the Vikram Samvat is with the folk-hero Vikramaditya, and the beginning of the second millennium is with the folk-hero King Bhoj; the beginning of the third millennium is wit…
> — **RAJ-E** · *King Bhoj and Paramara-period Town Architecture (English translation)* · p. 155 · `rajpurohit-bhoj-en-00445`

> 14 / King Bhoj and Paramara-period Town Architecture a great builder, a poet devoted to the public good, a patron of scholars and artists, a supreme donor, a foremost hero, and a votary of the virtues. Even in his own lifetime he became the hero of tales and stories. Thereafter a world of fascinating stories relating to King Bhoj kept being woven continually. In various languages of India and abroad, strange tales, poetic narratives and stories about his generosity are especi…
> — **RAJ-E** · *King Bhoj and Paramara-period Town Architecture (English translation)* · p. 14 · `rajpurohit-bhoj-en-00052`

> King Bhoj, in his *Shringara-prakasha* and *Sarasvati-kanthabharana*, has discussed various festivals which, along with being folk-festivals, were also royal festivals. Of these, some were vow-festivals, some of the season, and some crop-festivals. Noteworthy among such festivals are: Ashtami-chandraka, Kunda-chaturthi, Suvasantaka, Andolana-chaturthi, Dola-vilasa, Shalmali, Madanotsava, Udaka-kshvedika, Ashokotsika, Chuta-bhanjika, Pushpavachayanika, Amralatika, Bhutamatrika…
> — **RAJ-E** · *King Bhoj and Paramara-period Town Architecture (English translation)* · p. 148 · `rajpurohit-bhoj-en-00424`

### C13.4 — udaipur, udaypur, heritage, history, temple

> Everyone was awaiting Mahashivratri. Every year on this day a big fair is held in Udaipur, in which thousands of people come for the Shiva temple, from even the surrounding districts. This time Udaipur was somewhat bright and open. The newly-made three-foot-wide road was ready like some highway. One day before Shivratri, the phone-call of Pragya Pravah's Deepak Sharma came. By who-knows-what inspiration, he was desirous of going to Udaipur with immediate effect. In the fast o…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00341`

> The biggest change that has come this year is that the aware people of Ganj Basoda have begun to look, afresh and with a new vision, at this sad city of their neighbourhood. They have begun to ask after its condition. A band of youths is roaming around Udaipur every second or third day. Everywhere, Udaipur is giving some new information about itself. The social worker Praveen Sharma is, every single day, going into some ruin, some old house, some scrub, and turning the pages …
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00348`

> Like Gwalior and Chanderi, the presence of Jain idols upon the hilly rocks tells us that this whole region held within itself religious traditions of every kind. After [the region's] coming into the grip of the Sultans and emperors of Delhi, the mosques of the Muslim period, too, add some new pages to the story of Udaipur. Upon this statement of Dr. Upadhyay, my own belief is that every broken idol of Udaipur — whether of Hindu gods and goddesses or of the Tirthankaras — tell…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00567`

> Local social organizations celebrate festivals like Holi, Rangpanchmi, Makar Sankranti, etc., on a community basis. The whole village participates in social religious festivals as a compact unit. “A 7-day Shivaratri fair in February-March is organized in Udaypur. At the Neelkantheshwar Temple, an annual fair is held in the nearby ‘Ganpuri Bagh’.$^{2}$ The periodical fairs are an important gathering place, especially the Shivaratri Mahadev Festivals at Udaypur being very popul…
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 37 · `intach-2022-udaypur-00164`

### C13.1 — iast, rājā, aura, gayī, bhoja

> उदयदित्य ने उदयपुर में रहते हुए अपनी गौरवशाली राज परंपरा को ही बढ़ाया था। यही वजह है कि सदियां बीतने के बावजूद वे अब तक इस पूरे क्षेत्र की स्मृतियों मैं जगमगा रहे हैं... जब भी किसी त्योहार की रौनक देखता हूँ, मेरी आँखें नम हुए बिना नहीं रहतीं। कभी-कभी तो बरबस रोने लगता हूँ। ये दुख के आँसू नहीं बल्कि खुशी के आँसू होते हैं। हमेशा की तरह इस साल होली पर यही लगा कि भारत की पिछली कई सदियाँ बिल्कुल ही बेरंग बीती हैं। बेरंग ही नहीं, खून के लाल रंग से रंगी हुई। आज दिवाली पर उन अंधेरी र…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00340`

> फिलहाल प्राप्त जानकारी के मुताबिक राजमहल के खंडहरों में मदरसा संचालित है, जहां मुस्लिम बच्चों को मजहबी तालीम दी जाती होगी। मुमकिन है उन्हें उदयपुर के दूर सदियों तक पीछे फैले इतिहास के इतिहास के बारे में भी कुछ ज्ञान दिया जाता होगा। पता नहीं मौलवी को खुद उदयपुर का कितना असल इतिहास पता होगा और कितना वे जहांगीर से शुरू होकर काजी साहब पर खत्म कर देते होंगे। डॉ. मिश्र ने कहा कि उदयपुर का इतना पुरातन स्वरूप मदरसा वालों के मन में क्या अंकित करता होगा? क्या उदयपुर का पुराना वैभव उनके…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00098`

> कहानी है, जिसकी खुदाई में दशकों पहले शानदार कलाकृतियों वाला एक पुराना आवास दफन था। श्रद्धा और परिश्रम से उसकी सफाई की गई थी। वही अब उनका घर है, जो कथा उदयपुर का एक प्रकाशित पृष्ठ है। उदयपुर की इस करवट को निकट से देखने देश के प्रसिद्ध इतिहासकार डॉ. सुधीश मिश्र डेढ़ महीने में दूसरी बार आए तो सबसे ताजा कहानी राजा मिश्रा ने सुनाई।
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00248`

> महाशिवरात्रि का इंतजार सबको था। हर साल इस दिन एक बड़ा मेला उदयपुर में लगता है, जिसमें आसपास के जिलों तक से हजारों लोग शिव मंदिर के लिए आते हैं। इस बार उदयपुर कुछ उजला-उजला और खुला-खुला सा था। नई बनी तीन फुट चौड़ी सड़क किसी राजमार्ग की तरह तैयार थी। शिवरात्रि के एक दिन पहले प्रज्ञा प्रवाह के दीपक शर्मा का फोन आया। पता नहीं किस प्रेरणा से वे तत्काल प्रभाव से उदयपुर जाने के इच्छुक थे। महाशिवरात्रि के व्रत में उन्हें नीलकंठेश्वर ने दर्शन के लिए बुला लिया था। अगली सुबह उनके साथ उद…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00330`

### C13.5 — goddess, excellent, thus, linga, lady

> V.ii.69.38-51 I was carried off by the current of the three rivers and cast out of water surface. You seized me by the head, О beautiful lady, and tore me with your claws. О fair one, I was brought to the presence of Lord Sangamesvara by you. Simultaneously, 0 lady of excellent countenance, you met with your death at the hands of the fishermen (along with me). I visited thus Lord Sangamesvara at the time of death. I had a perfect ablution in the waters of Sipra, Ganga and Nil…
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 255 · `skanda-xiii-00532`

> Here the author states the geographical location of every shrine, the name of the &iva-Linga thereof and a legend to explain the name, 'history’ and importance of that Linga. The author modifies a Puranic legend to suit his purpose an d /o r attributes a new legend with mythological names, thus giving them a semblance of a real Puranic story. As this Section describes the €iva shrines in Mah&kalavana area, some duplication of the sacred places mentioned in the previous Sectio…
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 7 · `skanda-xiii-00007`

> Skanda Purana It is crowded with lordly elephants leading the herds of elephants, tigers, lions and Sambaras. It shone with animals like bears, monkeys, jackals etc., and also with peacocks, serpents, cats, mice etc. I am eager to know this.” 9-15. Thus I was asked by you, О fair lady, to reveal the reason of your preference of Mahakalavana to Mandara abounding in beautiful caves. О my beloved, (being) highly pleased, I then told you that the beautiful Mahakalavana was my Pat…
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 114 · `skanda-xiii-00229`

> On hearing their words Brahma, the grandfather of the worlds, became compassionate. He came to the place on Mandara where I was stationed. 46-57. After eulogizing me, he made this statement: T h e earliest Devas named Tu$itas have been deprived of their bodies by Bhadrakali, О Mahadeva. The Vasus have been overpowered and shattered, the Bhaskaras have been injured in the battle. The remaining ones have fled in various directions. How shall the Kayavarohana (growing of the bod…
> — **SKP-13** · *The Skanda-Purāṇa, Part XIII (AITM series)* · p. 316 · `skanda-xiii-00674`

**Gaps.** barely represented here: `BET-K`, `PAR`.

## C14 — Conquests and Regimes: Decline of the Socio-Economic Hub of Madhya Bharat

[↑ contents](#contents)

**Coverage.** 1,739 chunks from 25 sources (`ADH`, `BHJ-H`, `DEV`, `GAN`, `GAZ-VID`, `GUP`, `HAR`, `INT-ARC`, `INT-GEO`, `KRAM-1`, `KRAM-2`, `PAN`, `PAR`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `RAJM`, `SAM`, `SIN-B`, `SIN-S`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: secondary_core 789, primary_authorial_paramara 272, field_observation_reportage 212, secondary_comparative 148, reference_tertiary 118, contextual_thematic 59, primary_epigraphic 58, field_observation_survey 50, primary_scriptural 33. The largest single contributor is `GAN` with 313 chunks (18% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- The Ghori line was replaced in 1436 A.D. by the Khilji dynasty under **Sultan Mahmud Shah I (1436–1469 A.D.)**, a soldier-sultan under whom the Malwa Sultanate reached its maximum territorial extent. — `PAT-INS` `[single-source]`
- The great Nilakantheśvara temple at Udayapur was built by Udayaditya in Sam 1116 = 1059 A. D. An ART AND CULTURE 259 inscription of the sixteenth century A. D. describes it as the most beautiful temple in India. — `GAN` `[single-source]`
- Despite the Maratha reverse at Panipat in 1761, **Mahadji Scindia (1761–1794 A.D.)** arose as the towering military personality of northern India, controlling the Mughal Emperor at Delhi and creating a powerful modernized army. — `PAT-INS` `[single-source]`
- Following the Third Anglo-Maratha War in 1818, the Maratha states concluded treaties with the British, ruling as premier princely states until Indian independence in 1947. — `PAT-INS` `[single-source]`
- Karna's successor, Jayasimha -Siddharaja (1096-1145 A. D.), was very young when he ascended the throne of Anhilwar, in 1196 A. D. His mother, Mayaņalladevî, became regent and managed the affairs of the state for some time. — `GAN` `[single-source]`
- His successor, Ghiyas-ud-din (1469–1500 A.D.), enjoyed a peaceful 31-year reign focused on cultural pursuits and the arts, building the Jahaz Mahal for his vast harem. — `PAT-INS` `[single-source]`
- Balban invested the town in 1251, and in 1304-5, Ain-ul-Mulk, the general of Alauddin Khilji, completed the final conquest of Malwa, including Chanderi. — `PAT-CH` · `PAT-INS` · `PAT-TEM` `[established]`
- The Paramara kingdom was finally destroyed in 1305 A.D. when Alauddin Khilji's general, Ain-ul-Mulk, smashed the Hindu forces at Mandu, killing Mahlakadeva and converting Malwa into a province of the Delhi Empire. — `GAN` · `PAT-CH` · `PAT-INS` `[established]`
- His son, Alp Khan, assumed the name **Hoshang Shah (1405–1432 A.D.)** and transferred the capital permanently to fortified Mandu. — `PAT-CH` · `PAT-INS` · `PAT-TEM` `[established]`
- Mohammad Ghori reduced the principality, and Qutb-ud-din Aibak captured it in 1197 A.D. Gwalior was temporarily liberated but was reconquered by Shams-ud-din Iltutmish in 1231 A.D. after a desperate 11-month siege. — `PAT-CH` · `PAT-INS` · `PAT-TEM` `[established]`
- By 1733, Malharrao Holkar and Ranoji Scindia forced Raja Jaisingh of Amber (the Mughal governor) to sue for peace and yield *chauth* (tribute). — `PAT-INS` `[single-source]`
- His successor Vakpati II Munja (974–995 A.D.) was a great general, poet, and literary patron who defeated the Cholas, Chalukyas, and Chedis before losing his life to Taila II. — `GAN` · `PAT-INS` `[established]`
- The Kalacuri Soma waged successful wars against the Mâlavas and the Gurjaras between 1167 and 1172 A. D. At this period, as has been pointed out, the Gurjaras occupied, by force of arms, the northern divisions of Malwa. — `GAN` `[single-source]`
- The Candella Dhanga (950-1001 A. D.), the successor of Yasovarman, conquered Râdha and Anga (E. — `GAN` `[single-source]`
- His descendant, Sihada (1220-1234 A. D.), issued an inscription from Vâgadavatapadraka.4 The war between Siyaka II of Malwa and the Râstrakûta Khottiga took place in 970-971 A. D. The prince — `GAN` `[unverified]`
- Contemporary Sanskrit inscriptions on its porches record that it was founded by the Paramara King **Udayaditya**; construction commenced in **1059 A.D.** (*V.S. 1116*) and the flagstaff was hoisted in **1080 A.D.** (*V.S. 1137*). — `HAR` · `PAT-INS` `[established]`
- In 1728, the Mughal governor Girdhar Bahadur was routed and killed near Mandu by Chimnaji Appa. — `PAT-INS` `[single-source]`
- According to Memoirs of Babur, Silhadi Rajput was the ruler of this place in 1527 A. D. Bahadur Shah of Gujarat looted the town in 1532 and compelled the ruler to embrace Islam. — `GAZ-VID` `[single-source]`
- Barely represented in this bucket, so anything resting on them is a thin reed: `KRAM-2`, `RAJM`, `SIN-S` — `[gap]`

### C14.1 — paramara, bhoja, malwa, dynasty, inscription

> Vindhyavarman, son of Jayavarman-reconquest of Malwa. War with the Hoysalas and the Yadavas, Subhatavarman. Invasion of Gujarat and annexation of Lata. A C D iv Arjunavarman- War with Jayasimha, the king of Gujarat. Parijatamañjarî. War with the Yadavas. Devapala son of the mahakumara Hariścandra. Sankha, ruler of Lâţa. Invasion of Gujarat. Invasion of Malwa by the Moslems, JaitugidevaWar with the Yadavas and the Vaghelas of Dholka. Jayavarman IIHis fight with the Cahamans of…
> — **GAN** · *History of the Paramāra Dynasty* · p. — · `ganguly-paramara-00015`

> The riches of Ujjain and Dhara were no less glittering than those of Ajmer, Kanauj and Anhilwar; the idol of Mahakala was of no less repute than that of 1 I. A., Vol. XX, . 84. Somanatha; yet these adventurers did not attempt any invasion of Malwa. They must have been attracted by its wealth, but the armaments of the Paramaras probably dashed to the ground all their hopes of successful plunder. It was from one of its western neighbours that the structure of the Paramara gover…
> — **GAN** · *History of the Paramāra Dynasty* · p. 102 · `ganguly-paramara-00509`

> The Vikrama-ColanUla tells us that Vikrama Cola's general, who was a I Progress Report of the Archaeological Survey of India, Western Circle, 1914, p. 59. 2 Ibid. 3 E. I., Vol. I, p. 326. 4 I. A., Vol. XXII, p. 143. 162 HISTORY OF THE PARAMARA DYNASTY Pallava chief (1118-1133 A. D.), defeated the kings of Simhala, Końkaņa, and Malava. WAR WITH THE CAULUKYAS OF GUJARAT. After Udayaditya's victory over the Caulukya Karņa there was a temporary cessation of the struggles between …
> — **GAN** · *History of the Paramāra Dynasty* · p. 75 · `ganguly-paramara-00346`

> of his daughter with a Varman king of East Bengal. Naravarman-his war with the Candellas, the Colas and the Caulukyas of Gujarat. YasovarmanDismemberment of the Paramâra kingdom, Invasion of the Cahamânas of Sakambharî. Defeat and capture of Yasovarman by the Caulukya Jayasimha-Siddharaja of Gujarat. Conquest and annexation of Malwa by Jayasimha. Jayavarman I-reconquest of Malwa by Jayavarman. His war with the Candella Madanavarman. His defeat by the Câļukya Jagadekamalla II …
> — **GAN** · *History of the Paramāra Dynasty* · p. — · `ganguly-paramara-00014`

### C14.2 — architecture, town, bhoj, built, temple

> The Ghori line was replaced in 1436 A.D. by the Khilji dynasty under **Sultan Mahmud Shah I (1436–1469 A.D.)**, a soldier-sultan under whom the Malwa Sultanate reached its maximum territorial extent. He fought the rulers of Gujarat, the Deccan, and Delhi, and raised a seven-storeyed tower of victory at Mandu to commemorate his successes over the Rana of Mewar. His successor, Ghiyas-ud-din (1469–1500 A.D.), enjoyed a peaceful 31-year reign focused on cultural pursuits and the …
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00035`

> The Marathas secured complete sovereignty over the territories between the Chambal and Narmada, and the great houses of Scindia (at Gwalior), Holkar (at Indore), and Pawar (at Dhar and Dewas) carved out their historic principalities. Despite the Maratha reverse at Panipat in 1761, **Mahadji Scindia (1761–1794 A.D.)** arose as the towering military personality of northern India, controlling the Mughal Emperor at Delhi and creating a powerful modernized army. Following the Thir…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00038`

> * **Art of Stone Carving:** Practiced traditionally by the *Pattharphod* class in northern Madhya Bharat. Reorienting their ancient image-carving skills after the 12th-century Islamic conquest, they mastered the art of carving delicate stone screens (*jalis*) in intricate geometric and floral patterns, visible on Gwalior Fort, the tomb of Muhammad Ghaus, and at Mandu. This tradition survives in the trellis work on modern buildings in Lashkar and Gwalior. * **Ceramics:** Datin…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00054`

> * **Kaliadeh Water Palace:** Built around **1500 A.D.** by Sultan Nasir Shah Khilji of Malwa on an island in the Kshipra river, anciently known as *Brahma Kund*. The palace is an excellent example of Mandu style secular architecture. Its outstanding feature is an ingenious hydro-engineering network by which the river water is directed through stone conduits into a series of internal tanks and allowed to discharge over sculptured stone curtains into cooling chambers built on a…
> — **PAT-INS** · *Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions* · p. — · `patil-composite-inscriptions-00090`

### C14.5 — they, bhoja, times, these, india

> - Mauryan Dynasty (Ashoka) - Sunga Dynasty (Pushyamitra) - Gupta Dynasty (Chandragupt, Samundragupt) - Parmars Dynasty - Chalukya Dynasty - Khalji Dynasty - Tughlaq and Ghuri Dynasty
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 16 · `intach-2022-udaypur-00051`

> [paraphrase — not a verbatim quote; source text unreliable] * *Caitra*: Plunges the master landlord into persistent grief and emotional distress [cite: 7282, 7284]. * *Jyeṣṭha*: High-risk window predicting early mortality for the householder [cite: 7283, 7285]. * *Āṣāḍha (Śucau)*: Destroys livestock and causes the quick decline of agricultural cattle [cite: 7283, 7285]. * *Bhadrapada (Nabhasya)*: The house owner will suffer displacement and fail to live in the home [cite: 7286, 7288]. * *Āśvin*: Triggers heavy litigation, localized di…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. SAMARĀNGANA-SŪTRADHĀRA > THE CALENDAR WINDOW FOR GROUND BREAKING (*SŪTRAPĀTA*) > Prohibited Months (To Be Avoided) · `samarangana-00290`

> Udaypur, varṇṇanāgakṛpāṇikā, Paramāra, Malwa The Śiva temple of Udaypur in the Vidisha district of Madhya Pradesh, also known as Nīlakaṇṭheśvara or Udayeśvara, is a celebrated example of India's medieval architecture, built around 1080 in the novel bhūmija style associated with the Paramāra dynasty of Malwa, c. 972–1305 (Deva 1975). Less well known is its status as an extraordinary epigraphic archive with a continuous sequence of inscriptions in Sanskrit, Persian, and Hindi s…
> — **SIN-S** · *A serpentine scimitar of letters from Udaypur, district Vidisha, M.P.* · p. — · `singh-serpentine-00002`

> 1. B. Mazumdar, Guide to Saranath, 2nd Ed. p. 22. 2. The Struggle for Empire, p. 421. 3. Ibid, p., 425. 138 Bhoja Paramtra and his Times Somanath by Mahmud of Ghazni.* Vimala'founded the town of Chandravati also and built the temple of Rishabhadeva on the Arbudachalam, for the promotion of Jainism.^ Vimala had the approval of his master Bhima, for all these activities. Thus, it seems probable that Jainism, in Gujarat, was in ascendancy. In Malwa too, it was not discarded. Had…
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00420`

### C14.6 — having, created, deserves, norm, create

> [paraphrase — not a verbatim quote; source text unreliable] ततस्तेषां अभूद् दोषरोगशोकाकुलं वपुः। मनश्च कामक्रोधेष्र्ष्यादैन्यासूयादिदूषितम्।। ३ ३।। आधिदैवकमुष्णाम्बुशीतादिजनितं महत्। आधिभौतिकमप्यासीद् दुःखं व्यालमृगादिजम्।।३४।। Mortals found their physical frames invaded by diseases, systemic functional imbalances, and grief, while their minds became heavily polluted by lust, blinding rage, jealousy, and despair [cite: 1329]. They were assaulted by massive cosmic miseries (*Ādhidaivika*) brought on by scorching summer heat, freezing m…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. SAMARĀNGANA-SŪTRADHĀRA > THE BIRTH OF ARCHITECTURE: BUILDING THE FIRST HOMES · `samarangana-00133`

> covered or surrounded by twelve poles and equipped with twenty rafters (varas) may be the second verandah or balcony as such. स्यादष्टाविंशतिस्तम्भस्तृतीयश्चाप्यलिन्दकः । ष‌ट्त्रिंशता चतुर्थश्च स्तम्भानां परिकीर्तितः ।।५।। The third balcony or verandah may also be of twenty eight poles or columns. By thirty six pillars the fourth balcony stands illustrated. एवं स्तम्भशतं मध्ये प्रोक्तं पृथ्वीजये बुधैः। द्वाराणि चास्य चत्वारि पञ्चशाखानि जायते (?) ।।६।। This way a centum of pol…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 29: Śayanāsana Lakşaņa · `samarangana-00338`

> तस्माल्लोकस्य कृपया शास्त्रमेतदुदीर्यते ।।५।। Barring aside the science of Architecture¹ (the site of a house, building ground, site; a house, an abode, a dwelling place) of that there may not be any definite conclusion regarding the auspicious marks. Hence out of gracefulness for the populace this science is being dilated upon. अथैकदा जगज्जन्महेतुमम्बुरुहासनम्। पृथ्वी पृथुभयभ्रान्ता चकिताक्षी समाययौ।।६।। Once, however, unto the one having seat for a lotus (i.e. Brahma), gone…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra — Chapter 27 > CHAPTER 27¹ > Footnotes · `samarangana-00027`

> THE TATTVAPRAKĀŚA OF BHOJA PARAMĀRA | 113 मलामायाकर्मयुतः सकलस्तेषु द्विधा भवेदाद्यः । आद्यः समाप्तकलुषोऽसमाप्तकलुषो द्वितीयः स्यात् ॥६॥ आध्याननुगृह्य शिवो विद्येशत्वे नियोजयत्यष्टौ । मन्त्राश्च करोत्यपरान् ते चोक्ताः कोटयः सप्त ॥१०॥ प्रलयाकलेषु येषां पको मलकर्मणी व्रजन्त्यन्ये । पुर्यष्टकदेहयुताः योनिषु निखिलासु कर्मवशात् ॥११॥
> — **PAN** · *The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta* · p. 112 · `pande-udayesvara-00607`

### C14.4 — gwalior, bharat, madhya, mandu, under

> From the time of the Pratihara king, Chanderi came into historical prominence. Balban invested the town in 1251, and in 1304-5, Ain-ul-Mulk, the general of Alauddin Khilji, completed the final conquest of Malwa, including Chanderi. In 1401, Dilawar Khan Ghori, the Malwa governor, declared independence, and Chanderi became one of the most important *Shikkas* or provinces of the kingdom of the Malwa Sultans. It was during this regime that Chanderi rose to prosperity, as reflect…
> — **PAT-CH** · *The Cultural Heritage of Madhya Bharat* · p. — · `patil-1952-00369`

> The Maratha incursions into Malwa continued unabated and were more intensified during the years 1728 to 1740 A.D. In 1728, the Mughal Governor, Girdhar Bahadur, was routed and killed in battle near the fort of Mandu by Chimnaji, the younger brother of the Peshwa. Five years later, Malharrao Holkar and Ranoji Scindia appeared again on the scene to face Raja Jaisingh of Amber, who was specially commissioned by the Emperor to stem the tide of this recurring menace. But the resul…
> — **PAT-CH** · *The Cultural Heritage of Madhya Bharat* · p. — · `patil-1952-00122`

> Historically, the existence of most of these important States may be traced to the conquest of the whole territory by the Marathas of the Deccan in the 18th century. The confederate chiefs of the Marathas, such as the Scindias, Holkars, and the Pawars, had carved out principalities for themselves north of the Vindhyas under the central control of the Peshwas of Poona on the decline of the Mughal Empire of Delhi. With the final emergence of the British as the only paramount po…
> — **PAT-CH** · *The Cultural Heritage of Madhya Bharat* · p. — · `patil-1952-00016`

> In 1740, Bajirao died, succeeded by his son Balaji as Peshwa, who through the agency of the Nizam secured from the Mughal emperor a sort of formal or legal sanction for the otherwise *de facto* occupation of the Malwa territory by the Marathas through rather an interesting device of getting himself ceremoniously appointed as the emperor's humble Deputy Governor of Malwa. The Maratha chiefs acted as agents of the Peshwa in the north, where they wielded considerable influence i…
> — **PAT-CH** · *The Cultural Heritage of Madhya Bharat* · p. — · `patil-1952-00126`

### C14.3 — udaipur, come, after, they, people

> This is an episode 258 years after Raja Udayaditya. This inscription gives us a clear indication of an event when we see the presence of Tughlaq's plunderers in Udaipur. Of course, they must have come not to worship in the temple or to view the splendid sculpture, but only to seize the town and to plunder it. By this time the Paramaras' splendour was ending.
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00088`

> Take the proof of this from the archaeologist Dr. Narayan Vyas, or ask Dr. Suresh Mishra. At the other end of time, they take [us] only up to the Paramaras. Even after all these tragedies, every day thousands of *kafirs* kept coming for the darshan of Neelkantheshwar Mahadev. They too must not all be devoid of astuteness. Countless dignitaries who stayed for three or five years on the high chairs of politics and administration in Vidisha kept coming there continually, but no …
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00190`

> After the Paramaras, there is a long dark-moon (*amavas*) period of India's history, when the endless storms of the plunderers made stubborn efforts to erase Indian identity from the root. In this region are, in sequence, the attacks, loot and occupations of Shamsuddin Iltutmish, Alauddin Khilji, Mohammad Tughlaq, Sher Shah Suri. After the Mughals, there are the ambushes of new occupiers by the name of nawabs. Babur's attack on Chanderi took place in 1528, and by then Udaipur…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00254`

> With Ibrahim Lodi's star sinking in Agra and Delhi into the clutches of the foreign plunderers, the Mughals' pounce had begun in 1526. In this era, the Paramaras' splendid Udaipur appears as a remote town lodged, as it were, in the Chanderi suba, where, according to this *farman*, a mosque was built in the time of Babur's great-grandson Jahangir. For those offering *namaz* in the mosque, an order is now made to keep Babur in remembrance with the Fatiha prayer. Not only that —…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00180`

**Gaps.** barely represented here: `KRAM-2`, `RAJM`, `SIN-S`.

## C15 — Archaeologists, Laws and Repairs: Making Udaypur a 'Monument'; Udaypur in Independent India

[↑ contents](#contents)

**Coverage.** 1,685 chunks from 25 sources (`ADH`, `BHJ-H`, `DEV`, `GAN`, `GAZ-VID`, `GUP`, `HAR`, `INT-ARC`, `INT-GEO`, `KRAM-1`, `KRAM-2`, `PAN`, `PAR`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `RAJM`, `SAM`, `SIN-B`, `SIN-S`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: primary_authorial_paramara 497, field_observation_reportage 417, secondary_core 372, field_observation_survey 190, secondary_comparative 108, reference_tertiary 40, contextual_thematic 33, primary_epigraphic 24, primary_scriptural 4. The largest single contributor is `SAM` with 495 chunks (29% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- INTACH BHOPAL UDAYPUR INTACH Indian National Trust for Art and Cultural Heritage Bhopal Chapter Manjul Publishing House Udaypur. — `INT-ARC` · `INT-GEO` `[established]`
- Udaipur's next guest was the archaeologist Dr. Narayan Vyas, who had begun his services in the Archaeological Survey of India (ASI) in 1972 and, at the start of his job, had been sent directly to Udaipur. — `TIW-E` `[single-source]`
- The big tank No. 178 at Bahur near of 1902 Pondicherry, A.D. 985 to 1013, Villages agreed to contribute to the re- venue of the tank. — `SIN-B` `[single-source]`
- April 17, 2022 Madan Mohan Upadhyay, IAS(Retd) State Convenor-INTACH, MP Umashankar Bhargav, IAS Vidisha district has been known for ages for the rich and diverse heritage it possesses. — `INT-ARC` `[single-source]`
- Anupa Pande Professor and Head Department of History of Art Director/Pro Vice Chancellor National Museum Institute of History of Art Conservation and Museology National Museum New Delhi x | THE UDAYEŚVARA TEMPLE — `PAN` `[single-source]`
- The site is well maintained and centrally protected by the Archaeological Survey of India which has also carried out a restoration assignment in 1985 CE. — `INT-ARC` `[single-source]`
- The convener of the Indian National Trust for Art and Cultural Heritage (INTACH), Dr. Madanmohan Upadhyay, has minutely inspected Udaipur with his technical team. — `TIW-E` `[single-source]`
- After retiring from the post of Principal Secretary, he is at the Atal Bihari Vajpayee Good-Governance Institute (*Sushasan Sansthan*). — `TIW-E` `[single-source]`
- One day, the news of these ordinary efforts of ours going on in Udaipur reached the Indian National Trust for Art and Cultural Heritage (INTACH). — `TIW-E` `[single-source]`
- Bose, 'Canons of Orissan Architecture', Calcutta, 1932); Nāradaśilpaśāstra ('Two Chapters on Painting in the Nārada Śilpa Śāstra', by V. — `KRAM-2` `[single-source]`
- April 5th, 2022 Umashankar Bhargav, IAS Collector & District Magistrate Vidisha, Madhya Pradesh — `INT-ARC` `[single-source]`
- On the wall of one of these temples there is an inscription of the Paramara Udayaditya (1059-1086 A. D.), which gives a definite clue to the age of these buildings. — `GAN` `[single-source]`
- The Jagamohan or Maṇḍapam of the Simhanātha Temple, Baramba State, Cuttack, is a Trichādya building (ASI, Bihar and Orissa photograph, No. 5504 of the year 1941-42). — `KRAM-1` `[single-source]`
- Waterymuhūrtta- Presided over by Varuņa, p.845, 869 (BS of Varahamihira) Samarangapa-sūtradhara Tula (Beam) having surface even as such projected as such gone into the central spot. — `SAM` `[single-source]`
- Here is a part of the Report of the CAG on Performance Audit of Preservation and Conservation of Monuments and Antiquities, Union Government (Civil) Ministry of Culture Report No. 18 of 2013. — `SIN-T` `[single-source]`
- Before departing from Udaipur, we went toward that Uday Samudra, where a week earlier INTACH's team had already worked and had measured its length as 980 metres. — `TIW-E` `[single-source]`
- Through the southern direction of Himalaya, surrounded by the salt ocean from the other side [cite: 846, 847], is the Varșa named "Bhārata", the very primeval one, having the shape of an arc or bow [cite: 848, 851]. — `SAM` `[single-source]`
- On retiring as a Major General at the age of 47, he first wrote and sent his scheme regarding India's archaeological wealth to Viceroy Lord Canning. — `TIW-E` `[single-source]`
- Barely represented in this bucket, so anything resting on them is a thin reed: `GUP`, `PAR` — `[gap]`

### C15.6 — having, created, deserves, create, norm

> कुर्यादम्भोजवतीं वापीमाहार्ययोगेन ।। १६ ३ ।। Also equipped with water born birds i.e. aquatic birds, fishes and female crocodiles¹ or female of a monster mechanically devised (the architect) may create an oblong tank endowed with lotuses by the application of an adventitious² norm. सामन्तमुख्यपुरुषा राजाज्ञालब्धसंश्रयास्तत्र । परराष्ट्रागतदूतास्तिष्ठेयुर्निहितमिह निभृताः ।।१६४।। The Chief functionaries such as subsidiary vassals having resorts received as per command of the k…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 31: Named Yantravidhānaṁ i.e. The Chapter dealing with the Preparation of Mechanical Contrivances · `samarangana-00442`

> > पृथिव्यां श्रीभोजदेवो धर्मसंरक्षणाय च । > देशमालवकोत्पन्नः श्रीराजगृहमेत्य च ॥ > भोजदेवो जयद्वेष्यान्सर्वेषां च प्रमूर्धनि । > न तत्तुल्यो जगत्यस्ति न भूतो न भविष्यति ॥ > x x x > अथर्ववेदे विहिता महाशान्तिरनेकशः । > कारापिता तेन यथा चोक्षा विहितदक्षिणा ॥ > x x x > श्रीमद्भोजपुरे विद्वानासीत्सोमेश्वरो द्विजः । > तत्पुत्रकेशवेनैषा कृता कौशिकपद्धतिः ॥ > > *(Sanskrit verses — in sense: "On earth, Shri Bhojadeva, born in the land of Malwa, came to the royal house for the protect…
> — **RAJ-E** · *King Bhoj and Paramara-period Town Architecture (English translation)* · p. 164 · `rajpurohit-bhoj-en-00483`

> ``` # SAMARĀNGANA-SŪTRADHĀRA ### of Mahārājādhirāja Śrī Bhojadeva Paramāra ## CHAPTER 1: Mahāsamāgamana ### (The Insurgence of Mahāsamā (Pṛthivī)¹) ।। श्रीगणेशाय नमः ।। *(Obeisance be to Gaņeśa)* देवः स पातु भुवनत्रयसूत्रधारस्त्वां बालचन्द्रकलिकाङ्कितजूटकोटिः । एतत् समग्रमपि कारणमन्तरेण कार्य्यादसूत्रितमसूत्र्यत येन विश्वम् ।।१।। May that god, the architect of the triad of worlds, having the tip of the crest knot marked by the digit of the New Moon, protect you, by whom, was …
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra — Chapter 27 > CHAPTER 27¹ > Footnotes · `samarangana-00026`

> How shall I organise over it this much, this way mind has gone apprehensive- this way was reported to by Prthu, the adorable lotus born one. उवाच बोधयन्नेनं कृत्वा भूमिं च निर्भयाम्। इयं मही महीपाल ! विधिवत् पालिता सती ।।१७।। Spoke out making this understood that having rendered the earth free of terror this earth, Oh protector of the Earth (i.e. king)! having been guarded as per legal implications. सस्यैरुत्पाद्य निष्पन्नैस्तव भोग्या भविष्यति। यच्च ते स्यादभिप्रेतं स्थानादिव…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra — Chapter 27 > CHAPTER 27¹ > Footnotes · `samarangana-00029`

### C15.5 — iast, aura, tathā, haiṃ, syāt

> अजित वडनेरकर - लगता है, एक सोयी हुई बस्ती उनींदेपन से बाहर आ रही है... उदयपुर (विदिशा) के दिन फिरने वाले हैं। - इतिहास, पुरातत्व व सांस्कृतिक निधियों के संरक्षण-संवर्धन में रुचि रखने वाले लोग लगातार यहाँ आ रहे हैं। स्थानीय लोगों में उत्साह है कि सदियों की उपेक्षा के शिकार रहे उदयपुर के स्मारक अब जी उठेंगे... इस नाचीज ने खुद इस क्षेत्र की दो बार यात्राओं में इसे जाँचा-परखा।
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00582`

> शिलालेख हैं, जो उस समय की महत्वपूर्ण जानकारी देते हैं। यह तब की बात है जब जहांगीर तो छोड़िए बाबर के बापदादों के फरगाना में भी अते-पते नहीं होंगे। यह ग्यारहवीं सदी की बात है। पत्रिका अखबार में प्रमुखता से मसला सामने आने के बाद विदिशा शहर के प्रबुद्ध लोगों ने कलेक्टर के नाम एक ज्ञापन दिया। मुझे लगता है कि किसी ज्ञापन की प्रतीक्षा के बगैर कलेक्टर को खुद जाकर देखना चाहिए और कानूनी कार्रवाई केवल कागजों पर नहीं करनी चाहिए। उदयपुर के चप्पे-चप्पे के प्राचीन स्मारकों के संरक्षण की कार…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00104`

> इंडियन नेशनल ट्रस्ट फॉर आर्ट एंड कल्चरल हेरिटेज (INTACH) के कन्वीनर डॉ. मदनमोहन उपाध्याय ने अपनी तकनीकी टीम के साथ उदयपुर का बारीकी से मुआयना किया है। उनकी टीम एक लंबा कैंप करने वाली है। यह उदयपुर के लिए कई दर्शकों बाद मिला एक शुभ समाचार है। शायद सिंधिया राजघराने के समय गर्दे साहब की निगरानी में किए गए मंदिर के रखरखाव के बाद पहली बार इस स्तर पर किसी की दस्तक हुई है। यह सिर्फ उदयपुर के लिए ही नहीं बल्कि चप्पे-चप्पे में ऐतिहासिक रूप से समृद्ध इस पूरे क्षेत्र के लिए एक स्वागत यो…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00337`

> किस नियम से आर्कियोलॉजिकल सर्वे ऑफ इंडिया के मातहत एक महान पुरातात्विक स्मारक के पास यह सब हो रहा है, यह कौन बताएगा? कलेक्टर एसडीएम को कहेंगे। एसडीएम तहसीलदार को घसीटेंगे और पटवारी से होकर कागजों पर कुछ रिपोर्ट ऊपर आ जाएगी। मध्यप्रदेश, भोपाल या विदिशा के लोगों को देश भर में लगातार होते रहे अपने बरबाद स्मारकों का अंतिम हश्र देखना हो तो उन्हें अयोध्या, मथुरा और वाराणसी जाने की जरूरत नहीं है। वे विदिशा के किले अंदर कहलाने वाले पुराने शहर के विजय मंदिर के अवशेषों पर जाकर देखें कि…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00068`

### C15.3 — temple, temples, india, gwalior, architecture

> Figure 114: Sculpture of Bhairava on the outer of Garbhagriha Figure 115: Small shrine in the temple complex architectural mass, is the finest specimen of the Bhumija temples. The temple is a living heritage with devotees pouring in from afar. The site is well maintained and centrally protected by the Archaeological Survey of India which has also carried out a restoration assignment in 1985 CE. There is still scope for improvement in terms of visitor management and installati…
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 64 · `intach-2022-udaypur-00241`

> Udaypur, varṇṇanāgakṛpāṇikā, Paramāra, Malwa The Śiva temple of Udaypur in the Vidisha district of Madhya Pradesh, also known as Nīlakaṇṭheśvara or Udayeśvara, is a celebrated example of India's medieval architecture, built around 1080 in the novel bhūmija style associated with the Paramāra dynasty of Malwa, c. 972–1305 (Deva 1975). Less well known is its status as an extraordinary epigraphic archive with a continuous sequence of inscriptions in Sanskrit, Persian, and Hindi s…
> — **SIN-S** · *A serpentine scimitar of letters from Udaypur, district Vidisha, M.P.* · p. — · `singh-serpentine-00002`

> This stone is evidently not in its original position, for its flat inscribed surface is turned inside out while its carved face with an ornamental balustrade (*vedikā*) is turned outside in, contrary to what we find in other well-preserved sections of the courtyard wall. It is likely that the stone was reset into its present position during one of the restoration campaigns at the temple complex carried out under the Gwalior State (1923-24, 5; 1925-26, 5-6; 1928-29, 5-6) and t…
> — **SIN-S** · *A serpentine scimitar of letters from Udaypur, district Vidisha, M.P.* · p. — · `singh-serpentine-00004`

> **By Dr. D. R. Patil, M.A., LL.B., Ph.D.** *Department of Archaeology, Government of Madhya Bharat, Gwalior* *Published: 28th December, 1952* In this small book on the *Cultural Heritage of Madhya Bharat*, I have attempted to present the various aspects of the age-old culture of the territory now comprising Madhya Bharat, mainly as they are reflected in her numerous and varied ancient monuments. A companion volume containing the list of monuments in the State, classified and …
> — **PAT-CH** · *The Cultural Heritage of Madhya Bharat* · p. — · `patil-1952-00000` · also **PAT-INS** · `patil-composite-inscriptions-00000`

### C15.1 — udaipur, come, people, some, history

> Udaipur's next guest was the archaeologist Dr. Narayan Vyas, who had begun his services in the Archaeological Survey of India (ASI) in 1972 and, at the start of his job, had been sent directly to Udaipur. He remembers well that then, on three sides of the temple, people had built their houses stuck completely [against it]. They were several decades old. We cannot even imagine in what condition it must have lain, and since when. Then those people were removed by being given co…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00356`

> On the basis of this intensive ground work, INTACH's future plan is that, to raise Udaipur into prominence, the Archaeological Survey of India, the State Archaeology Department, the district administration, the panchayat, private institutions, corporate companies, and the aware local society be brought together. In the past year Upadhyay went to Udaipur several times. He believes that the local people have a separate world, and that their living connection with their priceles…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00568`

> One day, the news of these ordinary efforts of ours going on in Udaipur reached the Indian National Trust for Art and Cultural Heritage (INTACH). It is a capable non-governmental organization of the country that looks after archaeological monuments, known by the name INTACH; its Hindi rendering is "Bharatiya Sanskritik Nidhi." Its Bhopal convener is Dr. Madanmohan Upadhyay. He is a long-familiar name in Madhya Pradesh. He has been an officer of the Indian Administrative Servi…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00267`

> The talented Cunningham had come to India with a different vision. Certainly it must have been some inborn quality of his. On retiring as a Major General at the age of 47, he first wrote and sent his scheme regarding India's archaeological wealth to Viceroy Lord Canning. He wrote that there is much that is old in India, which we ought to know. We have neither to do excavation nor conservation; we should only do a survey. He used the word "survey," which was a low-budget task.…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00304`

### C15.2 — udaypur, village, structure, century, udayaditya

> INTACH BHOPAL UDAYPUR INTACH Indian National Trust for Art and Cultural Heritage Bhopal Chapter Manjul Publishing House Udaypur. The field survey findings were very interesting and we see clear the layered history of the village from 6th century CE to 18th century CE (when a brass metal cap for the Shivalinga inside the Neelkantheshwar temple was offered by the commander Bappa Saheb of Gwalior state). This book is a comprehensive report on the village Udaypur and its nearby r…
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 1 · `intach-2022-udaypur-00000`

> landscape along with built heritage which is scattered in and lying unprotected for centuries. This book is divided into three sections. The first section is about the geographical and historic context of the region. This section also deals with the origin of Parmars and their expansion over time. The second section is about the listed heritage structure of the region. These structures are clubbed together according to the building typology and placed in chronological order f…
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 7 · `intach-2022-udaypur-00009`

> The journeys of discovery of the geo heritage in Udaypur began about 3 years ago. INTACH Bhopal was carrying out the documentation on the heritage sites in Udaypur village. It explored and identified about 50 heritage sites built more than 1000 years ago. Going outward toward the village, we saw a hill at a distance which had a long wall made of dry-stone machinery. We recorded this, too, as a hill fort at that time.
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 18 · `intach-geoheritage-00120`

> The Geo Heritage of Village Udaypur is a project to carry out an investigation into the geological formations and Geo heritage sites in Udaypur. Geo-heritages are not a new phenomenon. Globally, we can find them all over the, in Rajasthan Baraan district, we have the Ramgarh crater, which is almost 3500 m wide, and it was created millions of years ago by the impact of meteorite falling from outer Galaxy, the Geo heritage of volcanoes, the formations of glaciers, the great Can…
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 18 · `intach-geoheritage-00118`

### C15.4 — heritage, conservation, site, sites, monuments

> Further, it also describes the present condition and state of conservation of the monument and provide with suggestion for protecting and preserving the same. 1 Introduction to Village Udaypur 2 Architectural Significance - Settlement Pattern - Neighbourhood & Clusters - Building Typology 3 Discovered Heritage Sites in the Village
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 10 · `intach-2022-udaypur-00034`

> 6. Other Relevant Aspects- Investigating geo-tourism potential, conservation challenges, and strategies for sustainable preservation of Udaypur's geo-heritage. 3.3 3.
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 16 · `intach-geoheritage-00113`

> By recognizing and promoting Udaypur's geo-heritage, this study aims to contribute to its long-term preservation and sustainable development as a heritage tourism destination.
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 17 · `intach-geoheritage-00117`

**Gaps.** barely represented here: `GUP`, `PAR`.

## C16 — Present Tense: How the Town Lives with Its Past Today

[↑ contents](#contents)

**Coverage.** 1,637 chunks from 26 sources (`ADH`, `BET-K`, `BHJ-H`, `DEV`, `GAN`, `GAZ-VID`, `GUP`, `HAR`, `INT-ARC`, `INT-GEO`, `KRAM-1`, `KRAM-2`, `PAN`, `PAR`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `RAJM`, `SAM`, `SIN-B`, `SIN-S`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: field_observation_reportage 893, primary_authorial_paramara 293, secondary_core 209, field_observation_survey 99, secondary_comparative 63, reference_tertiary 33, primary_epigraphic 20, primary_scriptural 15, contextual_thematic 11, environmental_scientific 1. The largest single contributor is `TIW-H` with 454 chunks (28% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- Singh, Abhilash Khandekar, Anand Pandey, Girish Upadhyay, Shivkumar Vivek, and the word-scholar Ajit Vadnerkar — came to hear Katha Udaipur. — `TIW-E` `[single-source]`
- Udaipur's next guest was the archaeologist Dr. Narayan Vyas, who had begun his services in the Archaeological Survey of India (ASI) in 1972 and, at the start of his job, had been sent directly to Udaipur. — `TIW-E` `[single-source]`
- Knowers of history and archaeology like Dr. Narayan Vyas and Pooja Saxena; the water expert Anil Agarwal; Deepak Sharma of Pragya Pravah; the former chairman of the M.P. — `TIW-E` `[single-source]`
- After the enthusiastic event of Katha Udaipur, the title of the post of 03 March 2021 is — "History Follows Us." For the past twenty years I have been continually wandering, from this corner of India to that, in the tunnels of history. — `TIW-E` `[single-source]`
- Prashant Sharma of Dewas — who had had darshan of the Udaipur temple several times — came to the Tribal Museum at the very name of Udaipur. — `TIW-E` `[single-source]`
- April 17, 2022 Madan Mohan Upadhyay, IAS(Retd) State Convenor-INTACH, MP Umashankar Bhargav, IAS Vidisha district has been known for ages for the rich and diverse heritage it possesses. — `INT-ARC` `[single-source]`
- The former sarpanch of Naroda, a neighbouring village of Udaipur, Praja Yadav, had been informed by her son, who is studying in Bhopal, that "Katha Udaipur" is being held in Bhopal — you too come. — `TIW-E` `[single-source]`
- Public Service Commission, Ashok Kumar Pande; and the RSS regional co-secretary Hemant Muktibodh too came. — `TIW-E` `[single-source]`
- In his list were these names — Rahatgarh, Garhakota, Ajaygarh, Panna, Dhubela, Chhatarpur, Garh Kundar. — `TIW-E` `[single-source]`
- The seventh post, of 15 January 2021 — "The Invitation of Unknown and Untouched Udaipur." After the truth of Udaipur of Vidisha district came to the fore in social media and the media, there is much stir. — `TIW-E` `[single-source]`
- From Udaipur up to Ganj Basoda and Vidisha, from the village panchayat up to the district panchayat, from the Assembly up to Parliament, there are many brave and valiant people's representatives out on a political journey. — `TIW-E` `[single-source]`
- On INTACH's initiative, after our story centred on the Udaipur heritage walk was heard for the first time at the Tribal Museum, now, at the Bhopal level, the groundwork of INTACH's team began. — `TIW-E` `[single-source]`
- Santosh Kumar Verma is an assistant professor of history at the Girls' College of Ganj Basoda itself, whose Facebook page I got the chance to visit when the fresh tremors of Udaipur, on the Richter scale of history, reached him. — `TIW-E` `[single-source]`
- Managing their raw survival on the residual *Bhūrasa* locked within these stalks [cite: 1277], and now missing the great *Kalpatarus*, they began to seek crude shelter beneath the branches of ordinary trees [cite: 1282]. — `SAM` `[single-source]`
- We called it — "Katha Udaipur" (The Story of Udaipur). — `TIW-E` `[single-source]`
- On the cover we chose two splendid photos of the Udaipur temple, which Praveen Sharma and Saurabh Tamedhari had sent. — `TIW-E` `[single-source]`
- Its convener in Bhopal, Dr. Madanmohan Upadhyay, is a sensitive history-lover and a retired IAS officer of Madhya Pradesh itself. — `TIW-E` `[single-source]`
- Waterymuhūrtta- Presided over by Varuņa, p.845, 869 (BS of Varahamihira) Samarangapa-sūtradhara Tula (Beam) having surface even as such projected as such gone into the central spot. — `SAM` `[single-source]`
- Barely represented in this bucket, so anything resting on them is a thin reed: `BET-K`, `GUP`, `KRAM-1`, `PAR`, `SIN-S` — `[gap]`

### C16.3 — having, created, norm, deserves, create

> [paraphrase — not a verbatim quote; source text unreliable] ततो विलपतां भूरि स्वैरमाहारहेतवे ।। २० ।। प्राणत्राणार्थमेतेषामभूत् पर्यटको भुवि। भूरसेनैव तेनैते कुर्वाणाः प्राणरक्षणम् ।।२१।। विना कल्पद्रुमैर्वासमन्यवृक्षेषु चक्रिरे। As they wandered voluntarily in search of food to survive, a secondary baseline vegetation known as the *Parpaṭaka* tree grew up on the earth [cite: 1276]. Managing their raw survival on the residual *Bhūrasa* locked within these stalks [cite: 1277], and now missing the great *Kalpatarus*, they began to seek …
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. SAMARĀNGANA-SŪTRADHĀRA > THE LOSS OF DIVINITY AND THE FALL FROM THE TREES · `samarangana-00126`

> [paraphrase — not a verbatim quote; source text unreliable] अथैषां पश्यतामेव कदाचिद् भाग्यसंक्षयात्।।२२।। विपर्ययाच्च कालस्य भूमेः पर्पटकोऽप्यगात्। ततः पर्यटके नष्टे तुषशूककणोज्झिताः ।॥२३॥ अकृष्टपच्या मेदिन्यास्तस्मिन्न्भवञ् शालितण्डुलाः। Eventually, due to the continuous depletion of their good fortune and the relentless degeneration of cyclic time, the *Parpaṭaka* stalks also became extinct [cite: 1285]. Once the *Parpaṭaka* vanished, there emerged a new form of grain growing wildly in the unploughed soil—*Śāli* rice grains, natural…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. SAMARĀNGANA-SŪTRADHĀRA > THE EMERGENCE OF GREED, PROPERTY, AND CLIMATIC EXTREMES · `samarangana-00127`

> *[Sanskrit line as in source; the OCR contains errors and breaks (___). English of the Hindi gloss follows each.]* > **1. ओं ॥ संवत् १२८६ वर्षे कार्ति[क] शुदि ____** > *May there be accomplishment. In the year Samvat 1286, Kartik Shudi ____* > > **2. शुक्रे देव श्री उदयेश्वर ____** > *On Friday, Dev Shri Udayeshvar ____* > > **3. सन्निधौ समस्त प्रशस्तोपेत ____** > *in the presence [of], endowed with all renown ____* > > **4. समधिगत पंचशब्दालंका(र) ____** > *who has attained t…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00553`

> 2. Dr. D.N. Shukla renders *क्षेत्रीकृताम्* as *समीकृता* i.e. rendered even or levelled as such MW p.1153 समीकरण - Levelling the act of making even. 3. VSA, p. 584 *सन्निवेशान्*. 4. **Pura / Kheta / Kharvaṭa**: A place containing large buildings surrounded by a ditch and extending not less than a Kośa in length 2 ft., it extended for half the distance, it is called a Kheta, if less then that a Kharvața or small market town : any smaller cluster of houses is called a grāma or …
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Samarāṅgaṇa-sūtradhāra — Chapter 27 > CHAPTER 27¹ > Footnotes · `samarangana-00032`

### C16.4 — udaipur, some, history, come, heritage

> We improved its packaging further. We did not even call it a presentation. We called it — "Katha Udaipur" (The Story of Udaipur). The duet of a knower of history and a seeker. A powerful heritage walk. On the cover we chose two splendid photos of the Udaipur temple, which Praveen Sharma and Saurabh Tamedhari had sent. These were such throbbing frames as though Udaipur, coming out of the frame, is eager to talk to you in a royal manner. Four days before the event, a cover was …
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00269`

> I was astonished to see the listeners and viewers of Katha Udaipur. For the INTACH team too, this was a living experience. Prashant Sharma of Dewas — who had had darshan of the Udaipur temple several times — came to the Tribal Museum at the very name of Udaipur. Two retired bank officers, Harvansh Dua and [another], too felt that to hear the voice of history once
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00274`

> On INTACH's initiative, after our story centred on the Udaipur heritage walk was heard for the first time at the Tribal Museum, now, at the Bhopal level, the groundwork of INTACH's team began. This was the next chapter of Katha Udaipur, which will be joined to some next story. Dr. M. M. Upadhyay, without wasting time, fixed a one-day tour of Udaipur. He himself wanted to see, with his own eyes, what is in Udaipur, and from where INTACH could begin some work.
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00316`

> The field work was conducted in two phases. The first survey was conducted from 14$^{th}$ to 27$^{th}$ March 2021 CE to explore Udaypur village and the second field survey was organized on 3$^{rd}$ to 5$^{th}$ July 2021 CE to visit the nearby villages of the Udaypur. In this survey each of the heritage structures were identified, visited and listed. All the structures have been listed by keeping a note of their GPS coordinates. Observations made on site have been documented, …
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 7 · `intach-2022-udaypur-00012`

### C16.1 — intach

> राजस्थान और दक्षिण भारत के ऐतिहासिक स्थानों की तरह चमका सकती है। यहां इतना कुछ देखने और समझने लायक है। उदयपुर के अनुभव के आधार पर वे कहते हैं कि राज्य सरकार पंचायतों का व्यापक अभिलेखीकरण कराए तो यह एक बड़ी पहल होगी। यह काम हम 10-12 जिलों में कर रहे हैं। अगर सरकार प्रदेश की सभी पंचायतों में यह काम कराती है तो तय है कि हमारे संज्ञान में पहली ही बार कई बेशकीमती चीजें एक साथ आ जाएंगी। पंचायतों में और गांवों में पुरातात्विक महत्व का क्या है, यह पता चलेगा। यह काम बहुत ज्यादा समय का…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00545`

> मैं इससे पहले भी कई बार यहां आया था और हर बार यह बदहाल गली मुझे चिढ़ाती थी। गली से होकर मंदिर के बेमिसाल स्थापत्य को देखकर लगता था कि जैसे एक चमचमाता हुआ हीरा कूड़े के ढेर पर रखा गया हो और किसी को इसकी कोई परवाह न हो। मैं आम लोगों से लेकर, गली के कारोबारियों, तीन स्तरीय पंचायत के नुमाइंदों से लेकर दूसरे नेताओं और सरकारी कारिंदों को खरी-खोटी सुनाते हुए ही लौटता था। किसी की आंखों में यह खोई हुई चमक चुभती नहीं थी। सबके सब काम बेफिक्री से चल रहे थे। दुनिया का कारोबार बदस्तूर चल र…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00021`

> ... और सचमुच कुछ जागरूक नागरिक सक्रिय हो गये...गंजबासौदा के उत्साही प्रवीण शर्मा, कौस्तुभ शिरहोणकर, कमलेश शर्मा, गगन दुबे, अमित शुक्ला। उदयपुर के राजा मियाँ। मंडी बामोरा के रमिस्कान्त श्रीवास्तव...और भी अनेक लोग... इन सबकी पहल पर सबसे पहले तो स्थानीय लोगों ने ही अतिक्रमण हटाने शुरू किए। उसके बाद मन्दिर तक पहुँचने का अवश्रुद्ध मार्ग प्रशस्त करने का बीड़ा उठा लिया।...और देखते ही देखते एक छोटे से कस्बे में जनसहयोग से करीब तीन फुट चौड़ी सीमेंटेड सड़क बन तैयार हो गयी।
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00592`

> उदयपुर के अगले मेहमान थे पुरातत्ववेता डॉ. नारायण व्यास, जिन्होंने आर्कियोलॉजिकल सर्वे ऑफ इंडिया (एसआई) में अपनी सेवाएं 1972 में शुरू की थीं और अपनी नौकरी की शुरुआत में सीधे उदयपुर भेजे गए थे। उन्हें अच्छी तरह याद है कि तब मंदिर के तीन तरफ लोगों ने बिल्कुल ही सटकर अपने मकान बना रखे थे। वे कई दशकों पुराने थे। हम सोच भी नहीं सकते कि यह किस हाल में कब से पड़ा रहा होगा। तब उन लोगों को मुआवजा देकर हटाया गया था। तीनों तरफ चार फुट मलबा हटाया तो मंदिर की शानदार बुनियाद बाहर निकली थी, …
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00341`

### C16.2 — town, temple, paramara, architecture, built

> The other players in this will be: 1. Forest apartment 2. Madhya Pradesh Eco-Tourism Development Board 3. The district administration (with the collector as the head), 4. The local panchayat 5. Indian National Trust for Arts and Cultural Heritage (INTACH), Bhopal chapter
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 142 · `intach-geoheritage-00429`

> The gateway to the hillside: This has already been there for the past 1000 years, and the same will be used as the entrance to the Geo site. The approach road to the fortification wall needs to have proper access. 2. Development of a space for parking: We also need a small space for parking, which can be developed between the Natraj sculpture and the 1400-meter-long fortification wall. Since full development of the site is going to take some time and we do not expect it to ha…
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 150 · `intach-geoheritage-00472`

> The conservation of Geo heritage sites is an entirely new area for work in India. Madhya Pradesh and other states of the country have a huge number of heritage destinations and thousands of unprotected monuments of natural and built heritage that need attention from the community. Geo Heritage conservation and development is an area towards which the local community, such as the gram panchayat for the municipal corporation of the Zila Panchayat, and other communities at the l…
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 146 · `intach-geoheritage-00451`

> It is a project that needs very extensive, sustained effort at many levels. Located inside a protected forest, there are many stakeholders, like: - Forest Department, - Archaeology department, - Tourism department, - Panchayat and rural development, - Geological Survey of India and
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 153 · `intach-geoheritage-00484`

### C16.6 — village, udaypur, temple, area, found

> April 17, 2022 Madan Mohan Upadhyay, IAS(Retd) State Convenor-INTACH, MP Umashankar Bhargav, IAS Vidisha district has been known for ages for the rich and diverse heritage it possesses. This place has seen several dynasties in the past 2000 years and each of these dynasties and its rulers has left their imprint on this soil. The most notable dynasty of this region of Central India had been the Parmar, the most famous being Raja Bhoj of the 11th century CE. The significant bui…
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 3 · `intach-2022-udaypur-00001`

> All the records of the village were kept under his custody.* Since very ancient times, the village headman enjoyed the rent-free lands in reward of his services,' as is stated by Kautilya and Manu.* The village headman enjoyed taxes in kind from 1. v.p. 17. 2. The liashtrakutos mid their Times p 189. 3. The Restrakutas and Their Times, p 1 89. 4. Ibid, The Village Communities. 45,54-5s. 5. £C. VIII, SoRab, No. 234. 6. Rashtrakutas and Their Times, p. 193, 7. Arth. chapt. II. …
> — **SIN-B** · *Bhoja Paramara and His Times* · p. — · `singh-1984-bhoja-00351`

> 330 HISTORY OF THE PARAMARA DYNASTY enjoyed a very happy existence. Sometimes they undertook corporate work for the welfare of the villagers. A number of the inhabitants of the village of Bhundipadra united in contributing various sums of money for the construction of a step-well, with the object of providing pure drinking water for the people of the locality. The donors are described as realising that one can remain alive even for a month without food, but that without water…
> — **GAN** · *History of the Paramāra Dynasty* · p. 102 · `ganguly-paramara-00705`

> B Near the temple is a house called Ghariyālon Kā Makān, i.e. the house of the time-keepers of the temple, who claim to have been there for centuries. Their vocation had been to strike the enormous gong in the temple to keep time. Thus, the various rituals would be performed on time. This temple is a living one, where right up to the 21st century, there are the usual morning and evening pūja and aarti. The priests also perform, on request, special pūjas like Rudrāṣṭaka, Śiva …
> — **PAN** · *The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta* · p. 92 · `pande-udayesvara-00406`

### C16.5 — iast, aura, haiṃ, para, hotā

> नगर के सब ओर, नदियों, सागरों, वनों तथा पर्वतों पर सर्वत्र उमापति का स्थान पहुँचे *[IAST] nagara ke saba ora, nadiyoṃ, sāgaroṃ, vanoṃ tathā parvatoṃ para sarvatra umāpati kā sthāna pahu~ce* है ॥122 *[IAST] hai ||122* अपनी-अपनी दिशा में इस प्रकार देवोत्तम प्रतिष्ठित करने पर वह नगर सम्प्रदाय समृद्धि *[IAST] apanī-apanī diśā meṃ isa prakāra devottama pratiṣṭhita karane para vaha nagara sampradāya samṛddhi* और आनन्द-प्रशंसा प्राप्त करता है ॥123 *[IAST] aura ānanda-praśaṃsā prāpta …
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 54 · `bhojdev-hi-00244`

> राजा भोज के समय से मालवा में निर्माण-क्रांति आ गयी थी। प्रासाद, मन्दिर, तालाब, प्रतिमाएँ बनती रहीं और पूरा मालवा इन अनोखी कलाकृतियों से भर गया। मन्दसौर जिला इस दृष्टि से अधिक समृद्ध है। वहाँ का हिंगलाजगढ़ तो तत्कालीन अप्रतिम प्रतिमाओं का अकृत खजाना है। आज मालवा में जो कुछ निर्मितियों के प्राचीन रूप दिखाई देते हैं, उनमें से बहुधा परमारकालीन हैं। *[IAST] rājā bhoja ke samaya se mālavā meṃ nirmāṇa-krāṃti ā gayī thī| prāsāda, mandira, tālāba, pratimāe~ banatī rahīṃ aura pūrā māla…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 6 · `bhojdev-hi-00028`

> वास्तु, यज्ञ, देवालय से युक्त तथा आराम-उद्यान से भरपूर, तालाब, बावड़ी के स्थानों से जो चारों ओर अलंकृत हो। 42 *[IAST] vāstu, yajña, devālaya se yukta tathā ārāma-udyāna se bharapūra, tālāba, bāvar̤ī ke sthānoṃ se jo cāroṃ ora alaṃkṛta ho| 42* वाहनों के लिए जो सुगम हो, मिथुनों को रतिप्रद हो, श्री-लक्ष्मी उत्पन्न करने वाली हो, ऐसी भूमियाँ नगर के लिए प्रशस्त होती हैं। 43 *[IAST] vāhanoṃ ke lie jo sugama ho, mithunoṃ ko ratiprada ho, śrī-lakṣmī utpanna karane vālī ho, aisī bhūmiy…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 30 · `bhojdev-hi-00136`

> पृथ्वी से उत्पन्न जल का कहीं उच्छ्राय (सायफन द्वारा उठाना) प्रशंसनीय होता है। *[IAST] pṛthvī se utpanna jala kā kahīṃ ucchrāya (sāyaphana dvārā uṭhānā) praśaṃsanīya hotā hai|* गीत, नृत्य, वाद्य, पटह (ढोल), वंश (बंसी), वीणा, काँसे के ताल (ताशे), तुमिला, करंट *[IAST] gīta, nṛtya, vādya, paṭaha (ḍhola), vaṃśa (baṃsī), vīṇā, kā~se ke tāla (tāśe), tumilā, karaṃṭa* (ताली) और जिन अन्य भी वाद्यों की कल्पना की जाये वह सब यन्त्र से प्रकट हो जाता *[IAST] (tālī) aura jina anya bhī vādyoṃ…
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 89 · `bhojdev-hi-00391`

**Gaps.** barely represented here: `BET-K`, `GUP`, `KRAM-1`, `PAR`, `SIN-S`.

## AF — Afterword: Conservation Today — Struggles of the Village and How to Help

[↑ contents](#contents)

**Coverage.** 1,412 chunks from 24 sources (`ADH`, `BET-K`, `BHJ-H`, `GAN`, `GAZ-VID`, `GUP`, `INT-ARC`, `INT-GEO`, `KRAM-1`, `KRAM-2`, `PAN`, `PAR`, `PAT-CH`, `PAT-INS`, `PAT-TEM`, `RAJ-E`, `RAJM`, `SAM`, `SIN-B`, `SIN-S`, `SIN-T`, `SKP-13`, `TIW-E`, `TIW-H`). Source-type mix: primary_authorial_paramara 562, field_observation_reportage 430, secondary_core 183, field_observation_survey 160, contextual_thematic 23, primary_scriptural 21, reference_tertiary 14, secondary_comparative 13, primary_epigraphic 5, environmental_scientific 1. The largest single contributor is `SAM` with 561 chunks (40% of the bucket).

**Key facts the KB establishes.** Each line is condensed from the cited passage, not composed; the status is derived from how many distinct sources carry it and whether their figures agree. `[single-source]` means no second source was matched by that test, which is deliberately conservative — it under-reports corroboration rather than claiming it. Read it as "attribute, do not assert", not as proof that no other book says this.

- INTACH BHOPAL UDAYPUR INTACH Indian National Trust for Art and Cultural Heritage Bhopal Chapter Manjul Publishing House Udaypur. — `INT-ARC` · `INT-GEO` `[established]`
- Udaipur's next guest was the archaeologist Dr. Narayan Vyas, who had begun his services in the Archaeological Survey of India (ASI) in 1972 and, at the start of his job, had been sent directly to Udaipur. — `TIW-E` `[single-source]`
- After retiring from the post of Principal Secretary, he is at the Atal Bihari Vajpayee Good-Governance Institute (*Sushasan Sansthan*). — `TIW-E` `[single-source]`
- Anupa Pande Professor and Head Department of History of Art Director/Pro Vice Chancellor National Museum Institute of History of Art Conservation and Museology National Museum New Delhi x | THE UDAYEŚVARA TEMPLE — `PAN` `[single-source]`
- The convener of the Indian National Trust for Art and Cultural Heritage (INTACH), Dr. Madanmohan Upadhyay, has minutely inspected Udaipur with his technical team. — `TIW-E` `[single-source]`
- One day, the news of these ordinary efforts of ours going on in Udaipur reached the Indian National Trust for Art and Cultural Heritage (INTACH). — `TIW-E` `[single-source]`
- Waterymuhūrtta- Presided over by Varuņa, p.845, 869 (BS of Varahamihira) Samarangapa-sūtradhara Tula (Beam) having surface even as such projected as such gone into the central spot. — `SAM` `[single-source]`
- In Madhya Pradesh, the government has begun — as it did years ago — exactly the same efforts for the restoration of two Jyotirlingas, Ujjain and Omkareshwar, as we saw in Uttar Pradesh at Kashi Vishwanath and Ayodhya. — `TIW-E` `[single-source]`
- April 17, 2022 Madan Mohan Upadhyay, IAS(Retd) State Convenor-INTACH, MP Umashankar Bhargav, IAS Vidisha district has been known for ages for the rich and diverse heritage it possesses. — `INT-ARC` `[single-source]`
- The Udaypur story was captured in "The Architectural Splendor of Udaypur", a publication brought out by the Bhopal chapter of INTACH. — `INT-GEO` `[single-source]`
- Livelihoods, Mobility, and Housing: In Search of Missing Links in Indian Towns. — `INT-GEO` `[single-source]`
- And with peaks made of Hema (i.e. gold), Hemakūța, this one was known as the mountain [cite: 827], to which serve perennially or to which keep occupied perennially Cāraṇas (heavenly charioteers⁶) and Guhyakas [cite: 828, 830]. — `SAM` `[single-source]`
- Mahāvrata festival referred to the Tândya Brāhmaņa (V.5-1.9-21, p.155-157 by Cinnasvami Śāstri and Kātyāyana-śrauta Sūtra (XIII.2.21-27, p.28-29). — `SAM` `[single-source]`
- Geo Heritage conservation and development is an area towards which the local community, such as the gram panchayat for the municipal corporation of the Zila Panchayat, and other communities at the local level, need to be sensitized. — `INT-GEO` `[single-source]`
- Conservation of the site as a protected monument by a notification will be a very significant part of this because this is a continuous stretch track off 1400 m. — `INT-GEO` `[single-source]`
- Before departing from Udaipur, we went toward that Uday Samudra, where a week earlier INTACH's team had already worked and had measured its length as 980 metres. — `TIW-E` `[single-source]`
- The external concentric islands (*Dvīpas*) are: **Śāka, Kuśa, Krauñca, Śālmali, Gomeda, and Puṣkara** [cite: 956, 965]. — `SAM` `[single-source]`
- They are surrounded respectively by concentric oceans of: **Kṣīra** (milk), **Ājya** (clarified butter), **Dadhi** (curd), **Madya** (wine), **Ikṣurasa** (sugarcane juice), and **Svādvambha** (sweet water) [cite: 966, 967]. — `SAM` `[single-source]`
- Barely represented in this bucket, so anything resting on them is a thin reed: `ADH`, `BET-K`, `GUP`, `PAR`, `PAT-CH`, `PAT-TEM`, `RAJM`, `SIN-S` — `[gap]`

### AF.1 — udaipur, temple, some, people, history

> — **Ajit Vadnerkar** - It seems a sleeping settlement is coming out of its drowsiness… The days of Udaipur (Vidisha) are about to turn [for the better]. - People interested in the conservation and promotion of history, archaeology and cultural treasures are coming here continually. There is enthusiasm among the local people that the monuments of Udaipur — victims of centuries of neglect — will now come alive… This humble one himself examined and appraised it over two journeys…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00606`

> INTACH BHOPAL UDAYPUR INTACH Indian National Trust for Art and Cultural Heritage Bhopal Chapter Manjul Publishing House Udaypur. The field survey findings were very interesting and we see clear the layered history of the village from 6th century CE to 18th century CE (when a brass metal cap for the Shivalinga inside the Neelkantheshwar temple was offered by the commander Bappa Saheb of Gwalior state). This book is a comprehensive report on the village Udaypur and its nearby r…
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 1 · `intach-2022-udaypur-00000`

> One day, the news of these ordinary efforts of ours going on in Udaipur reached the Indian National Trust for Art and Cultural Heritage (INTACH). It is a capable non-governmental organization of the country that looks after archaeological monuments, known by the name INTACH; its Hindi rendering is "Bharatiya Sanskritik Nidhi." Its Bhopal convener is Dr. Madanmohan Upadhyay. He is a long-familiar name in Madhya Pradesh. He has been an officer of the Indian Administrative Servi…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00267`

> Neelkantheshwar Shankar Bhagwan does not sit only for the devotees who go to Udaipur with desires of wealth, position-and-power, and progeny. There are some duties too of the citizens, which have not been done. The organizations that have now stood up aware — let them shake their people's representatives too a little, and take a procession of theirs to Udaipur. Let groups from schools and colleges keep reaching there continually. Let the educational institutions too run some …
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00124`

### AF.3 — created, deserves, parts, half, breadth

> एवं धराणां सर्वेषां भवेत् षष्ठं शतत्रयम् ।।४१।। Two centums of epistyle pillars may be added by sixteen. This way of all the dharas or ground floors there may be a hexagon having triad of centums digited as such. पृथ्वीजयवदत्रापि शेषनिर्माणमिष्यते। तृतीयभूमिकामूर्छिन निर्गमेष्वखिलेष्वपि।॥४२॥ प्राङ्ग‌णानि विधेयानि विशेषोऽत्रैष कीर्तितः । सर्वतोभद्रसंज्ञेऽथ शत्रुमर्दननामपि (नि) ।।४३।। Like the land encroachment here also the remaining construction here is introduced. On the roo…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 29: Śayanāsana Lakşaņa · `samarangana-00345`

> Samarāngaņa-sūtradhara On verses 117-118, Chapter 31, referring to Pravarşaņa as shower, Pranala as pipe, Jalamagna as subaquatic and Nandyāvarta as being in a special design, fit to be constructed in palaces for the king's pleasure. Regarding their construction Bhoja says :- (1) They are to be in the proximity of big reservoirs. (2) They should occupy a site with good scenic possibilities. (3) Pipes have to be prepared to double and treble the height and other requirements o…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 31: Named Yantravidhānaṁ i.e. The Chapter dealing with the Preparation of Mechanical Contrivances · `samarangana-00426`

> ``` # Chapter 32: The Elephant Stud or Equery for Tuskers Chapter 32 CHAPTER 32 The Elephant Stud or Equery for Tuskers लक्षणं गजशालानामिदानीमभिदध्महे। चतुरश्रीकृते क्षेत्रे भागैर्भक्ते ततोऽष्टभिः ।।१।। Now we shall illustrate the definition of the elephant stables. In an area square shaped created and divided into eight parts. मध्ये द्विभागविस्तारं स्थानं कुर्वीत् हस्तिनः। कल्प्याः प्रासादवद् भागा ज्येष्ठमध्याधमाः क्रमात् ।।२।। In the centre having breadth of two parts a spa…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 31: Named Yantravidhānaṁ i.e. The Chapter dealing with the Preparation of Mechanical Contrivances · `samarangana-00475`

> The Prasadas (the palaces) of these very shapes by (materials) such as stones and baked bricks and the like for the purpose of decoration or ornamentation of the towns he built as वैराजं चतुरश्नं स्याद् वृत्तं कैलाससंज्ञितम्। चतुरश्रायताकारं विमानं पुष्पकं भवेत्।।७।। Vairāja may be a square shaped and Kailāśa may be globular in structure, square and rectangular or oblong the aerial car or a palace may be the Puşpaka (by name). वृत्तायतं च मणिकमष्टानि स्यात् त्रिविष्टपम्। तद्भ…
> — **SAM** · *Samarāṅgaṇa-sūtradhāra* · sec. Chapter 49: The definition of Prāsādas such as Rucaka · `samarangana-00705`

### AF.5 — having, house, well, becomes, apte

> *[Sanskrit line as in source; the OCR contains errors and breaks (___). English of the Hindi gloss follows each.]* > **1. ओं ॥ संवत् १२८६ वर्षे कार्ति[क] शुदि ____** > *May there be accomplishment. In the year Samvat 1286, Kartik Shudi ____* > > **2. शुक्रे देव श्री उदयेश्वर ____** > *On Friday, Dev Shri Udayeshvar ____* > > **3. सन्निधौ समस्त प्रशस्तोपेत ____** > *in the presence [of], endowed with all renown ____* > > **4. समधिगत पंचशब्दालंका(र) ____** > *who has attained t…
> — **TIW-E** · *Jagta Hua Kasba / कथा उदयपुर (English translation)* · p. — · `tiwari-jhk-en-00553`

> * See p. 11, 'Vastuvidhāna'. १। रेखा। २। तन्न। ३। चतुष्कोणं। ४। कण्ठां च। ५। वदान्यत्र। ६। विख्यातं। ७। स्थलादीनि। ८। तु। ९। देवतान्तत्र। १०। मार्गशेह। ११। प्रादेशान्ते एवं पद्मकृ १२ संमृतं पञ्चमृतं च संभवम् । मूलाधारादिपद्भेदं शब्दस्पर्शादिसंभवम् ॥२५॥ अन्यत्सर्वं भावनया कल्पितं वास्तुपूर्वम् । एतत्सर्वं समालोक्य १३ यन्त्रं रूपं च साधयेत् ॥२६॥ स्वगुरोर्मुखतः कार्यं १४ बुध्या शास्त्रेण चार्जुन । सम्प्रदायेन कर्त्तव्यमिदं प्रस्तारमार्गतः ॥२७॥ श्रीचक्रं कथितं देवर्मू कलासनगोत्तम…
> — **KRAM-2** · *The Hindu Temple, Volume II* · p. 140 · `kramrisch-1946-v2-00718`

> Figure 195: Sculptures around the door The structure has a courtyard in the centre. The inner parts of the house have carvings on the walls and an intricately carved threshold that resembles the entrance to a garbhagriha in other historic temples of the village. The threshold has numerous human forms and other motifs with Shiva in the centre of the lintel.
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 89 · `intach-2022-udaypur-00305`

> १ । भित्ते । २ । भित्तुच्छ्रायं । ३ । तदुर्ध्वं तु भवेदीशकस्यामलसासकम् ॥ विस्तारं द्विगुणं द्वारं ४ कर्तव्यं तु सुशोभनम् । जातरूपं सरे कुर्यात् चक्रं वा स्वरुदुःस्वरेः ॥३२८॥ औडुम्बरकृतस्वणं दत्त्वा शालां न्यसेद् बुधः । तूय्यमङ्गलघोषेण ब्राह्मणान् स्वस्तिवाच्य च ॥३२९॥ द्वारस्य तु चतुर्थांशे कार्य्या चण्डप्रचण्डकी । दण्डहस्तौ तु कर्तव्यो विश्ववस्नोपमातुमौ ॥३३०॥ शालाद्वै न्यस्य रत्नानि न्यसेदूर्ध्वमुदुम्बरम् । तस्य मध्ये स्थिता देवी शाङ्कलक्ष्मी सुरेश्वरी ॥३३१॥ कर्तव्या दिग्गजैः…
> — **KRAM-2** · *The Hindu Temple, Volume II* · p. 142 · `kramrisch-1946-v2-00725`

### AF.2 — iast, aura, cite, thus, period

> > पृथिव्यां श्रीभोजदेवो धर्मसंरक्षणाय च । > देशमालवकोत्पन्नः श्रीराजगृहमेत्य च ॥ > भोजदेवो जयद्वेष्यान्सर्वेषां च प्रमूर्धनि । > न तत्तुल्यो जगत्यस्ति न भूतो न भविष्यति ॥ > x x x > अथर्ववेदे विहिता महाशान्तिरनेकशः । > कारापिता तेन यथा चोक्षा विहितदक्षिणा ॥ > x x x > श्रीमद्भोजपुरे विद्वानासीत्सोमेश्वरो द्विजः । > तत्पुत्रकेशवेनैषा कृता कौशिकपद्धतिः ॥ > > *(Sanskrit verses — in sense: "On earth, Shri Bhojadeva, born in the land of Malwa, came to the royal house for the protect…
> — **RAJ-E** · *King Bhoj and Paramara-period Town Architecture (English translation)* · p. 164 · `rajpurohit-bhoj-en-00483`

> नगर की वृद्धि (उन्नति), शोभा और संरक्षण के लिए सब ओर तिर्मिजली पोल सहित विशाल द्वार बनवाने चाहिए। 147 *[IAST] nagara kī vṛddhi (unnati), śobhā aura saṃrakṣaṇa ke lie saba ora tirmijalī pola sahita viśāla dvāra banavāne cāhie| 147* प्रतोली के दक्षिण भाग से ऊँचा वाम की ओर गया द्वितीय तक उसके पास में बाहर एक बनवाना चाहिए। 148 *[IAST] pratolī ke dakṣiṇa bhāga se ū~cā vāma kī ora gayā dvitīya taka usake pāsa meṃ bāhara eka banavānā cāhie| 148*
> — **BHJ-H** · *भोजदेव (Bhojadeva)* · p. 48 · `bhojdev-hi-00198`

> | 39 | Shahi Masjid | UD/REL/MO/05 | Religious(Monroe) | 17th Century | State Archaeological Department | In Use | Very Good | I* | 23.54.1.08 N and 78.3.34.79 E | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | 49 | Ulaol Dad Bauli | UD/WS/SW/03 | Water Structure(Bauli) | 17th Century | Unprotected | In Use | Moderate | II | 23.53.56.94 N and 78.3.44.32 E | | 50 | Tulsi Mahadev Bauli | UD/WS/SW/05 | Water Structure(Bauli) | 11th Century | Unprotected | In Use…
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 115 · `intach-2022-udaypur-00426`

> The construction period of this Darwaza looks to be 11$^{th}$ century CE. It is situated at GPS 23.54.00.1 N and 78.03.27.8 E. Purana Bazaar Darwaza that is located inside the Udaypur village towards the southeast of Neelkantheshwar Temple. This structure is located in khasra no. 735/3 having an area of 0.042 ha. It is currently in Government ownership. The gateway is ascended from the south and is on higher ground. It acts as an access to the Purana Bazaar area. The eastern …
> — **INT-ARC** · *The Architectural Splendor of Udaypur* · p. 52 · `intach-2022-udaypur-00208`

### AF.4 — intach

> इंडियन नेशनल ट्रस्ट फॉर आर्ट एंड कल्चरल हेरिटेज (INTACH) के कन्वीनर डॉ. मदनमोहन उपाध्याय ने अपनी तकनीकी टीम के साथ उदयपुर का बारीकी से मुआयना किया है। उनकी टीम एक लंबा कैंप करने वाली है। यह उदयपुर के लिए कई दर्शकों बाद मिला एक शुभ समाचार है। शायद सिंधिया राजघराने के समय गर्दे साहब की निगरानी में किए गए मंदिर के रखरखाव के बाद पहली बार इस स्तर पर किसी की दस्तक हुई है। यह सिर्फ उदयपुर के लिए ही नहीं बल्कि चप्पे-चप्पे में ऐतिहासिक रूप से समृद्ध इस पूरे क्षेत्र के लिए एक स्वागत यो…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00337`

> राजधानी भोपाल की नाक के नीचे सिर्फ़ डेढ़ सौ किलोमीटर दूर एक पूरा पुराना नगर अपने एक हजार साल पुराने वैभव में बचा हुआ जैसे दम तोड़ रहा हो। लेकिन ग्राम पंचायत से लेकर संसद तक की यात्रा करने वाले जनता के प्रतिनिधियों और प्रशासनिक पराक्रमियों ने अब तक इसे बेशर्मी से घूरे की तरह रखकर छोड़ा है। जैसा कि सब जानते हैं, उनकी प्राथमिकताओं में खदानें, कब्जे, निर्माण, बजट, कमीशन, सेटिंग, तबादले, प्रमोशन, टिकट, चुनाव जैसे पराक्रम और पुरुषार्थ सबसे ऊपर रहे हैं। दृष्टि होती तो दूरदृष्टि की अ…
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00059`

> व्यो-व्यो में घुमा सकते हैं और उन्हें बार-बार आने के लिए मजबूर कर सकते हैं। वे नौकरी के कारण यहां रहने की मजबूरी को एक सार्थक कार्य में बदल सकते हैं। वे सोशल मीडिया पर उदयपुर को उभार सकते हैं। हर रविवार की एक घोषित यादगार हेरिटेज वॉक में सैलानियों को लुभाने के लिए कुछ छपी हुई सामग्री भी तैयार हो सकती थी। इस बेहद सस्ते और कम बजट के काम में केंद्र, राज्य सरकार, जिला पुरातत्व संघ या स्थानीय पंचायत ही कुछ हाथ बढ़ा देते। विदिशा के जिला मुख्यालय पर जिला पुरातत्व संघ की बैठक दो-चार …
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00362`

> हमने वहीं तय किया कि हम दोनों मध्य प्रदेश के कुछ ऐसे ऐतिहासिक ठिकानों की होरेज वॉक पर निकलेंगे, जहां आमतौर पर लोग जाते नहीं है। आम लोगों की नजरों और दिलचस्पियों से दूर ऐसे बीरान और उजाड़ इलाके, जिनकी तरफ या तो मूर्ति चोर ही जाते रहे हैं या रात के अंधेरों में गड़े हुए खजाने के जांबाज खोजकर्ता और अगर पत्थर की खदानें आसपास हैं तो पत्थर के गैरकानूनी खनन से पैसा बनाने वाले आधुनिक भारत के राजनीतिक संरक्षण प्राप्त लुटेरे। यह एक द्विपक्षीय समझौता था कि हम एक साथ जाएंगे। मेरा लालच यह …
> — **TIW-H** · *कथा उदयपुर (Jagta Hua Kasba) — Hindi original* · p. — · `tiwari-jhk-hi-00010`

### AF.6 — udaypur, conservation, heritage, hill, fortification

> The conservation of Geo heritage sites is an entirely new area for work in India. Madhya Pradesh and other states of the country have a huge number of heritage destinations and thousands of unprotected monuments of natural and built heritage that need attention from the community. Geo Heritage conservation and development is an area towards which the local community, such as the gram panchayat for the municipal corporation of the Zila Panchayat, and other communities at the l…
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 146 · `intach-geoheritage-00451`

> Geo-heritage conservation is essential to: - Preserves unique geological formations that tell the story of Earth's past. - Protect ancient cultural and religious sites from degradation and encroachment. - Promote geo-tourism, which can provide sustainable economic benefits to local communities. - Enhance scientific research and education by offering real-world examples of geological processes. - Prevent threats such as illegal mining, deforestation, and urbanization, which co…
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 17 · `intach-geoheritage-00116`

> INTACH can be a fascinating partner by way of developing guides from the villages and properly educating them, giving them literature, and defining their roles. Cultural activities in the village can also help develop plans. How the villagers can help conservation and sustenance of the geo heritage by not disturbing it further.
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 142 · `intach-geoheritage-00430`

> Conservation of the site as a protected monument by a notification will be a very significant part of this because this is a continuous stretch track off 1400 m. The basic documentation work has been carried out now. Detailed conservation of what intervention is needed at what level will be carried out in the future.
> — **INT-GEO** · *Geo-Heritage of Udaypur: The Third Eye* · p. 143 · `intach-geoheritage-00433`

**Gaps.** barely represented here: `ADH`, `BET-K`, `GUP`, `PAR`, `PAT-CH`, `PAT-TEM`, `RAJM`, `SIN-S`.

## Coverage matrix — sources × chapters

Excerpts selected per chapter, by source code. A blank cell means the source contributed no selected excerpt to that chapter; it does not always mean the source is absent from the bucket.

| code | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 | C9 | C10 | C11 | C12 | C13 | C14 | C15 | C16 | AF | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `SAM` | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 3 | 3 | 4 | 66 |
| `BHJ-H` | 1 | 4 | 1 | 4 | 4 | 4 |  | 3 | 1 | 4 | 3 | 4 |  |  |  | 4 | 1 | 38 |
| `PAT-INS` | 3 | 3 | 4 | 4 | 1 | 2 | 4 | 4 | 4 |  |  | 2 |  | 4 | 1 |  |  | 36 |
| `TIW-E` | 4 |  |  |  | 1 | 2 |  |  | 1 |  |  | 1 | 4 | 4 | 4 | 4 | 4 | 29 |
| `INT-ARC` |  |  | 3 | 1 |  | 2 | 2 | 3 | 4 |  | 2 |  | 1 | 1 | 4 | 2 | 4 | 29 |
| `INT-GEO` | 2 | 4 | 4 |  |  | 1 |  | 1 | 4 |  |  |  |  |  | 4 | 4 | 4 | 28 |
| `TIW-H` | 4 |  | 2 |  |  |  |  |  | 1 |  | 4 | 1 | 4 |  | 4 | 4 | 4 | 28 |
| `GAN` |  | 3 |  | 4 | 4 | 4 |  | 2 |  |  |  | 1 | 3 | 4 |  | 1 |  | 26 |
| `SIN-B` |  |  |  | 2 | 4 | 2 |  | 2 | 3 | 3 | 3 | 4 |  | 1 |  | 1 |  | 25 |
| `SKP-13` | 3 | 1 | 1 | 1 |  |  | 4 |  |  | 4 |  |  | 4 |  |  |  |  | 18 |
| `RAJ-E` |  |  |  | 1 | 4 |  |  |  |  | 1 | 1 | 2 | 4 |  | 1 |  | 1 | 15 |
| `PAN` |  |  | 1 |  |  |  | 4 |  | 1 | 4 |  |  |  | 1 |  | 1 |  | 12 |
| `PAT-CH` |  |  | 1 | 2 |  | 1 |  |  | 1 |  |  | 1 |  | 4 | 1 |  |  | 11 |
| `KRAM-1` | 2 | 3 |  |  |  |  | 3 | 1 |  |  |  |  |  |  |  |  |  | 9 |
| `SIN-S` |  |  |  |  |  | 1 |  | 4 |  |  |  |  |  | 1 | 2 |  |  | 8 |
| `KRAM-2` | 1 |  | 1 |  |  |  | 1 |  |  | 1 |  |  |  |  |  |  | 2 | 6 |
| `GAZ-VID` |  | 1 | 1 |  |  |  |  |  |  |  | 4 |  |  |  |  |  |  | 6 |
| `ADH` |  |  |  |  | 2 | 1 | 2 |  |  |  |  |  |  |  |  |  |  | 5 |
| `HAR` |  |  |  | 1 |  |  |  |  |  | 3 |  |  |  |  |  |  |  | 4 |
| `RAJM` |  |  |  |  |  |  |  |  |  |  | 1 | 2 |  |  |  |  |  | 3 |
| `BET-K` |  | 1 |  |  |  |  |  |  |  |  | 1 |  |  |  |  |  |  | 2 |
| `PAT-TEM` |  |  | 1 |  |  |  |  |  |  |  |  | 1 |  |  |  |  |  | 2 |
| `DEV` |  |  |  |  |  |  |  |  |  |  | 1 |  |  |  |  |  |  | 1 |
| `GUP` |  |  |  |  |  |  |  |  |  |  |  | 1 |  |  |  |  |  | 1 |

404 excerpts and 325 key-fact lines in total; 14 entries were blocked from quotation by the quotability gate and appear as marked paraphrase.

Key-fact status tally: `[single-source]` 274, `[established]` 28, `[gap]` 16, `[contested]` 4, `[curated]` 3, `[unverified]` 3.
