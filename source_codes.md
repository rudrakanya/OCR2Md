# Source codes — the code of record

Every citation in `BOOK_SOURCEBOOK.md` uses a code from this table, and codes are defined here and nowhere else. One code per source; no code covers two sources. A translation and its original carry different codes, because they cannot substitute for one another in a quotation.

| code | book | author | lang | source type | source_id (KB) | notes |
|---|---|---|---|---|---|---|
| `ADH` | Some Paramāra Temples From Madhya Pradesh: A Case Study of Village Un | Swati Mondal Adhikari | en | secondary_comparative | `adhikari-2013-un` | Includes the author's own field survey at Un; first-person survey passages read as observation. |
| `BET-K` | Streamflow of the Betwa River under the Combined Effect of LU-LC and Climate Change | Amit Kumar et al. | en | environmental_scientific | `kumar-2023-betwa` | Peer-reviewed hydrological analysis of measured data. |
| `BET-S` | Long-term historic changes in climatic variables of Betwa Basin, India | Shakti Suryavanshi, Ashish Pandey, Umesh Chandra Chaube, Nitin Joshi | en | environmental_scientific | `suryavanshi-2013-betwa` |  |
| `BHJ-H` | भोजदेव (Bhojadeva) | Not named in file | hi | secondary_core | `bhojdev-hi` |  |
| `DEV` | Temples of North India | Krishna Deva | en | secondary_comparative | `deva-1969-temples` |  |
| `GAN` | History of the Paramāra Dynasty | D. C. Ganguly | en | secondary_core | `ganguly-paramara` | Standard dynastic history; cites Epigraphia Indica throughout. Hedged reconstructions are anchored inference,  |
| `GAZ-VID` | Madhya Pradesh District Gazetteers: Vidisha | P. N. Shrivastav, Rajendra Verma | en | reference_tertiary | `vidisha-gazetteer-1979` | The FILE is largely an LLM restatement of the gazetteer (815 '[cite: N]' markers; 36% of chunks). Not quotable |
| `GUP` | Iconography of the Hindus, Buddhists and Jains | R. S. Gupte | en | reference_tertiary | `gupte-1972` | Contains 77 chunks of leaked OCR-model commentary (stripped at chunking, logged). |
| `HAR` | The Temple Architecture of India | Adam Hardy | en | secondary_comparative | `hardy-2007` |  |
| `INT-ARC` | The Architectural Splendor of Udaypur | INTACH Bhopal Chapter | en | field_observation_survey | `intach-2022-udaypur` | Heritage listing with GPS points. Its general-mythology background passages are unsourced and must be judged c |
| `INT-GEO` | Geo-Heritage of Udaypur: The Third Eye | INTACH Bhopal Chapter | en | field_observation_survey | `intach-geoheritage` | Instrument survey (drone + total station). Its superlatives ('largest in the world') are advocacy, not survey  |
| `KRAM-1` | The Hindu Temple, Volume I | Stella Kramrisch | en | secondary_comparative | `kramrisch-1946-v1` | Two volumes of one work share work_id (count once for corroboration). Textually distinct: 0 near-duplicate pai |
| `KRAM-2` | The Hindu Temple, Volume II | Stella Kramrisch | en | secondary_comparative | `kramrisch-1946-v2` |  |
| `PAN` | The Udayeśvara Temple: Art, Architecture and Philosophy of the Śaiva Siddhānta | Anupa Pande | en | secondary_core | `pande-udayesvara` | Primary authority on the temple. Quotes Beglar/Cunningham reports (1870s) — nested primary witnesses. |
| `PAR` | History of the Parmar Rajput Dynasty | Not captured in extraction | en | secondary_core | `parmar-2025-origins` | Recent article in a multidisciplinary journal; low citation depth. |
| `PAT-CH` | The Cultural Heritage of Madhya Bharat | D. R. Patil | en | secondary_core | `patil-1952` |  |
| `PAT-INS` | Archaeological & Cultural Heritage of Madhya Bharat: Shrines, Architecture, and Inscriptions | D. R. Patil (Part I) + unattributed additions | mixed | primary_epigraphic | `patil-composite-inscriptions` | Composite. Part I duplicates patil-1952. Contains LLM-regeneration markers '[cite: N]' (37 in file). |
| `PAT-TEM` | The Cultural Heritage of Madhya Bharat — temples and architecture (composite) | D. R. Patil + Swati Mondal Adhikari (bundled) | en | secondary_comparative | `patil-composite-temples` | Composite; 117 chunks near-duplicate patil-1952. Adhikari portion duplicates adhikari-2013-un. |
| `RAJ-E` | King Bhoj and Paramara-period Town Architecture (English translation) | Bhagwatilal Rajpurohit | en | secondary_core | `rajpurohit-bhoj-en` | Machine-assisted translation of a Hindi original; contains 16 chunks of OCR commentary (stripped, logged). |
| `RAJM` | Pātañjala-Yogasūtram with the Rājamārtaṇḍa-vṛtti of Bhojadeva (ed. Ram Shankar Bhattacharya) | Bhojadeva (Bhoja Paramāra), commentary; Patañjali, sūtras; Ram Shankar Bhattacharya, editor | sa | primary_authorial_paramara | `rajamartanda-bhoja` | CC-0 scan, Jangamwadi Math Collection, digitized by eGangotri; the digitiser's footer stamp is stripped. No cl |
| `SAM` | Samarāṅgaṇa-sūtradhāra | Traditionally attributed to Bhoja (not stated in file) | mixed | primary_authorial_paramara | `samarangana` | **cite by section, never page — page numbers in this source are unreliable.** Period text in translation, BUT interleaved with LLM-generated glossaries/summaries carrying '[cite: N]' marke |
| `SIN-B` | Bhoja Paramara and His Times | Mahesh Singh | en | secondary_core | `singh-1984-bhoja` |  |
| `SIN-S` | A serpentine scimitar of letters from Udaypur, district Vidisha, M.P. | Saarthak Singh | en | secondary_core | `singh-serpentine` | Epigraphic study that embeds the primary inscription text; those passages are flagged embeds_primary_text. |
| `SIN-T` | Temple Economics: Arthvyavstha of Mandir (Vol. I) | Sandeep Singh | en | contextual_thematic | `singh-temple-economics` | Contemporary policy tract; does not discuss Udaypur. Background only — never cited as a Udaypur-specific claim |
| `SKP-13` | The Skanda-Purāṇa, Part XIII (AITM series) | Not named in file (Motilal Banarsidass, AITM series translation) | en | primary_scriptural | `skanda-xiii` | Period text in translation. Mythic/scriptural register: evidence of what the text narrates, never of events. |
| `TIW-E` | Jagta Hua Kasba / कथा उदयपुर (English translation) | Tiwari (VMT) | en | field_observation_reportage | `tiwari-jhk-en` | First-person heritage-walk reportage, self-described as opinion. Retain observation, folklore and opinion — ne |
| `TIW-H` | कथा उदयपुर (Jagta Hua Kasba) — Hindi original | Tiwari (VMT) | hi | field_observation_reportage | `tiwari-jhk-hi` | Original of tiwari-jhk-en. Same work: counts once for corroboration. Canonical for verifying the translation. |

27 sources carry codes.

## Known to exist, not in the corpus

- **udayesvara-temple-art-architecture.md** — Deleted from disk (git: staged deletion, still in HEAD). 25 chunks remain in kb/store.sqlite as orphans. Condensation of pande-udayesvara. Awaiting the user's decision: restore or purge.
- **Art of Paramaras.pdf** — Image-only scan; RapidOCR conversion stopped by the harness at page 28/62 (low memory), nothing written. Not yet in the corpus.
