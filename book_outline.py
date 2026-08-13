#!/usr/bin/env python3
"""
book_outline.py — the single source of truth for the book's structure.

Nineteen chapters, each with:

    n            chapter number
    title        the chapter title as it appears in the book
    theme        the one-line brief from the author's outline (may be None)
    scope        a paragraph telling the drafting model what this chapter covers
                 — and, by implication, what belongs to its neighbours instead
    subtopics    3-6 stable units of enquiry, each {key, question}

Sub-topics are deliberately *not* search queries. They are the questions the
chapter must answer; the retrieval queries are derived from them at run time by
query_gen.py. That indirection is the point: the old outline hard-coded a flat
list of query strings per chapter, which went stale the moment the corpus
changed and could never be re-derived. Edit the sub-topic here and the whole
retrieval layer follows.

`constraints`, where present, are editorial instructions that override
everything else at drafting time.

Consumed by query_gen.py, make_evidence.py, draft_chapter.py, assemble_book.py
and validate_book.py.
"""

BOOK_TITLE = "The Rising Lord"
BOOK_SUBTITLE = ("The Nīlakaṇṭheśvara (Udayeśvara) Temple of Udaypur "
                 "and the World of the Paramāra Rajputs")

# Regional anchors mixed into derived queries so a generic sub-topic ("crafts",
# "festivals") retrieves *this* region's material rather than the corpus's
# general treatments of the subject.
BOOK_ANCHORS = ["Udayapur Udaypur Vidisha", "Betwa Vetravati valley",
                "Malwa Avanti plateau", "Paramara"]

# Communities/caste and sati constraints are the author's standing editorial
# policy for the social chapters.
_SOCIAL_CONSTRAINTS = (
    "Do NOT include inflammatory, derogatory, or hierarchy-ranking references to caste; describe "
    "communities and occupations neutrally and respectfully, without endorsing any social ranking. "
    "Do NOT mention or describe the practice of sati (widow-burning) or similar practices at all."
)

CHAPTERS = [
    {
        "n": 1,
        "title": "Udaypur: A Small Town with a Long Memory",
        "theme": "Ancient Scriptural References",
        "scope": (
            "Open the book by introducing Udaypur as it is encountered today — a small town in the "
            "Basoda tahsil of Vidisha district, ringed by an old fortification wall, with an "
            "eleventh-century Śiva temple at its centre that has survived very nearly intact. "
            "Establish the town's names and identity, and reach back into the deep literary memory "
            "of this country: the references to Vidiśā, the Vetravatī and the Avanti region in "
            "Sanskrit scripture and poetry. Explain why this particular monument repays a whole "
            "book — its intactness, its dated inscriptions, its status as both building and "
            "archive — and sketch the arc the following chapters will follow. Do not yet narrate "
            "the Paramāra dynasty, the architecture, or the iconography in detail; those are "
            "chapters of their own."
        ),
        "subtopics": [
            {"key": "the-town-today",
             "question": "the town of Udaypur in Vidisha district today: its situation, fortification wall, "
                         "size, administrative setting and how it is reached"},
            {"key": "names-and-identity",
             "question": "the names of the town and the temple — Udayapur, Udaypur, Udayeśvara, "
                         "Nīlakaṇṭheśvara — and what those names mean and commemorate"},
            {"key": "scriptural-references",
             "question": "ancient scriptural and literary references to Vidiśā, the Vetravatī river and the "
                         "Avanti country in the Purāṇas, the epics and Sanskrit poetry such as the Meghadūta"},
            {"key": "why-it-matters",
             "question": "why the Udayeśvara temple is historically significant: its state of preservation, "
                         "its dated foundation inscriptions, and its importance among Indian temples"},
            {"key": "the-books-arc",
             "question": "the principal themes of the temple's story — dynasty, founder-king, architecture, "
                         "sculpture, inscriptions, decline and survival"},
        ],
    },
    {
        "n": 2,
        "title": "The Betwa Valley: Land, Rivers and Seasons",
        "theme": "Geography",
        "scope": (
            "A geographical portrait of the country in which Udaypur sits. Trace the Betwa "
            "(Vetravatī) from its rise in the Vindhyan escarpments through its catchment and "
            "tributaries; describe the drainage of the Vidisha district, the topography of the "
            "plateau and its ranges, and the seasonal regime — monsoon, the cold-weather rabī "
            "months, the hot season — including what the streamflow and climate records show about "
            "the river's behaviour and its long-term change. Close on how water and terrain "
            "determined where people settled. Keep soils, rock and vegetation for Chapter 3, and "
            "agriculture and irrigation works for Chapter 13."
        ),
        "subtopics": [
            {"key": "betwa-course",
             "question": "the course of the Betwa or Vetravatī river, its source in the Vindhyas, its "
                         "tributaries and the extent of its catchment basin"},
            {"key": "drainage-and-relief",
             "question": "the topography, relief and drainage of the Vidisha district and the eastern Malwa "
                         "plateau, its ranges, valleys and escarpments"},
            {"key": "streamflow",
             "question": "the streamflow, discharge and hydrology of the Betwa river and its seasonal variation"},
            {"key": "climate-and-seasons",
             "question": "the climate of the Betwa valley: monsoon rainfall, temperature, the cycle of seasons "
                         "and long-term historic changes in climatic variables"},
            {"key": "water-and-settlement",
             "question": "how rivers, seasonal water availability and terrain shaped where towns and villages "
                         "were sited in this region"},
        ],
    },
    {
        "n": 3,
        "title": "Stones and Forests: Geology, Flora and Fauna",
        "theme": "Geology and Landscape Report",
        "scope": (
            "The physical substance of the region. Describe the geology — the Vindhyan sandstones, "
            "the Deccan trap basalts, and the black cotton soil (regur) that covers so much of the "
            "plateau — and then the building stone in particular: where the fine-grained red "
            "sandstone of the temple was quarried and what its working properties are. Follow with "
            "the vegetation and forest cover of the district, its characteristic trees and "
            "cultivated flora, and its wildlife. End with how the landscape has changed. This is "
            "the material chapter: the temple's fabric as geology, not yet as architecture."
        ),
        "subtopics": [
            {"key": "regional-geology",
             "question": "the geology and rock formations of the Vidisha and Malwa region: Vindhyan sandstone, "
                         "Deccan trap basalt and their stratigraphy"},
            {"key": "soils",
             "question": "the soils of the Malwa plateau, especially the black cotton soil or regur, its "
                         "composition and properties"},
            {"key": "building-stone",
             "question": "the building stone used in the temples of this region: sandstone quarries, the "
                         "properties of the stone and how it was extracted and worked"},
            {"key": "forests-and-flora",
             "question": "the forests, trees and vegetation of the Vidisha district and the Betwa valley"},
            {"key": "fauna",
             "question": "the wild animals, birds and fauna of the Malwa plateau and the Vidisha forests"},
        ],
    },
    {
        "n": 4,
        "title": "Before Udaypur: Prehistory and Early Historic Vidisha",
        "theme": None,
        "scope": (
            "What stood in this country before Udaypur existed. Begin with prehistoric and stone-age "
            "traces in the region, then turn to Vidiśā/Besnagar as one of the great early historic "
            "cities of central India — its Mauryan and Śuṅga associations, the Heliodorus pillar, "
            "and its commercial importance. Survey the monumental landscape within a short radius: "
            "Sanchi, Udayagiri and its cave-shrines, Gyaraspur, Badoh-Pathari. Carry the account "
            "through the Gupta period, and close by asking what, if anything, occupied the Udaypur "
            "site itself before the eleventh century. Stop before the Paramāras."
        ),
        "subtopics": [
            {"key": "prehistory",
             "question": "prehistoric, stone age and chalcolithic remains, rock shelters and early settlement "
                         "in the Vidisha and Malwa region"},
            {"key": "vidisha-besnagar",
             "question": "the ancient city of Vidiśā or Besnagar: its history, importance, excavations and its "
                         "Mauryan and Śuṅga period remains"},
            {"key": "heliodorus-and-early-cults",
             "question": "the Heliodorus pillar at Besnagar, early Vaiṣṇava and Nāga cults, and the religious "
                         "life of early historic Vidisha"},
            {"key": "sanchi-udayagiri-gyaraspur",
             "question": "the Buddhist and early Hindu monuments near Vidisha — Sanchi, the Udayagiri caves, "
                         "Gyaraspur and Badoh-Pathari — and their sculpture"},
            {"key": "gupta-period",
             "question": "the Gupta period in the Vidisha region: its temples, sculpture, inscriptions and "
                         "political history"},
        ],
    },
    {
        "n": 5,
        "title": "From Avanti to Malwa: Dynasties, Trade Routes and Sacred Cities",
        "theme": "Evolution over the Years",
        "scope": (
            "The long middle passage between early historic Vidisha and the Paramāra ascendancy. "
            "Trace the succession of powers over Avanti and the plateau — Mauryas, Śuṅgas, "
            "Sātavāhanas, Kṣatrapas, Guptas, Hūṇas, and then the Rāṣṭrakūṭas and Gurjara-Pratihāras "
            "whose rivalry shaped the tenth century. Describe Ujjain and the sacred geography of "
            "the region, the pilgrimage centres, and the great arterial trade routes that crossed "
            "the plateau linking north to Deccan and east to the western ports. Show how the "
            "regional identity called 'Malwa' emerged from the older 'Avanti'. Leave the Paramāras "
            "themselves to Chapter 6."
        ),
        "subtopics": [
            {"key": "avanti-and-ujjain",
             "question": "Avanti as an ancient janapada and Ujjayinī or Ujjain as its capital: their history, "
                         "sanctity and place in Indian tradition"},
            {"key": "dynastic-succession",
             "question": "the succession of dynasties ruling Malwa before the Paramāras — Mauryas, Śuṅgas, "
                         "Sātavāhanas, Kṣatrapas, Guptas, Hūṇas, Rāṣṭrakūṭas and Gurjara-Pratihāras"},
            {"key": "trade-routes",
             "question": "the ancient trade routes crossing the Malwa plateau linking Mathurā and the north to "
                         "the Deccan, and Pāṭaliputra to the western ports"},
            {"key": "sacred-cities",
             "question": "the sacred cities, tīrthas and pilgrimage centres of Malwa and central India"},
            {"key": "malwa-identity",
             "question": "how the region came to be called Malwa, its boundaries, and its emergence as a "
                         "distinct political and cultural identity"},
        ],
    },
    {
        "n": 6,
        "title": "The Paramāras and Bhoja: Kingship, Learning and Temple Building",
        "theme": "How Udaypur was formed",
        "scope": (
            "The dynasty into which Udaypur was born. Begin with Paramāra origins — the Agnikula "
            "fire-birth legend on Mount Abu and the political work that myth performed — and the "
            "early rulers from Upendra through Sīyaka. Give Vākpati Muñja his due as warrior and "
            "patron, then centre the chapter on Bhoja: his reign and wars, his administration, and "
            "above all his standing as a scholar-king, with the corpus attributed to him — the "
            "Samarāṅgaṇasūtradhāra, the Sarasvatīkaṇṭhābharaṇa, the Tattvaprakāśa — and the "
            "authorship questions that corpus raises. Cover Paramāra building at Dhārā, Bhojpur, Un "
            "and elsewhere. Close with the collapse after Bhoja's death that made Udayāditya's "
            "recovery necessary. Udayāditya's own reign belongs to Chapter 7."
        ),
        "subtopics": [
            {"key": "origins-agnikula",
             "question": "the origin of the Paramāra dynasty: the Agnikula fire-birth legend at Mount Abu, "
                         "Vasiṣṭha, and the dynasty's claimed descent"},
            {"key": "early-rulers",
             "question": "the early Paramāra rulers — Upendra, Vairisiṃha, Sīyaka, Vākpati Muñja, Sindhurāja — "
                         "and the dynasty's rise from vassalage to sovereignty"},
            {"key": "bhoja-reign",
             "question": "the reign of Bhoja Paramāra: his campaigns, conquests, administration and political "
                         "achievements"},
            {"key": "bhoja-learning",
             "question": "Bhoja as scholar and author: the Samarāṅgaṇasūtradhāra, Sarasvatīkaṇṭhābharaṇa, "
                         "Tattvaprakāśa and the works attributed to him, and the question of their authorship"},
            {"key": "paramara-temple-building",
             "question": "Paramāra temple building and patronage: Dhārā, Bhojpur and its lake, Un, Nemawar and "
                         "other Paramāra temples"},
            {"key": "decline-after-bhoja",
             "question": "the decline of Paramāra power after Bhoja's death: the Cālukya and Kalacuri "
                         "invasions and the dismemberment of Malwa"},
        ],
    },
    {
        "n": 7,
        "title": "Udayāditya's Foundation: Town, Temple and Tank",
        "theme": None,
        "scope": (
            "The founding act itself. Narrate Udayāditya's accession in the crisis following Bhoja's "
            "death, his recovery of the kingdom and his victory over the Cālukya Karṇa. Then the "
            "threefold foundation that gives this chapter its title: the town of Udayapur laid out "
            "with its wall and gates; the Udayasamudra, the great tank; and the temple of "
            "Nīlakaṇṭheśvara/Udayeśvara itself, with its dated records — V.S. 1116/1059 and "
            "V.S. 1137/1080 — and the Udayapur praśasti with its play on the king's solar name. "
            "Where the dates disagree, say so plainly. Describe the foundation as an event; the "
            "building's architecture is Chapter 8 and its inscriptions Chapter 10."
        ),
        "subtopics": [
            {"key": "accession",
             "question": "Udayāditya's accession to the Paramāra throne and his recovery of the kingdom after "
                         "the disasters that followed Bhoja's death"},
            {"key": "founding-the-town",
             "question": "the founding of the town of Udayapur by Udayāditya: its layout, fortification wall "
                         "and situation"},
            {"key": "udayasamudra",
             "question": "the Udayasamudra tank or lake at Udaypur: its construction, dimensions, embankment "
                         "and water supply"},
            {"key": "temple-foundation",
             "question": "the foundation of the Nīlakaṇṭheśvara or Udayeśvara temple by Udayāditya, its "
                         "foundation dates in Vikrama Saṃvat 1116 and 1137, and the disagreement over them"},
            {"key": "udayapur-prasasti",
             "question": "the Udayapur praśasti inscription: its content, its genealogy of the Paramāras and "
                         "its imagery of the rising sun"},
        ],
    },
    {
        "n": 8,
        "title": "Udayeśvara in Stone: Plan, Structure and Style",
        "theme": "Neelkantheshwar Temple Architecture",
        "scope": (
            "A full architectural reading of the temple. Place the Bhūmija mode within the Nāgara "
            "tradition and explain what distinguishes it. Work through the building: the "
            "rotated-square, stellate plan and its saptaratha/saptabhūmi scheme; the sequence of "
            "garbhagṛha, antarāla and gūḍhamaṇḍapa with its porches; the jagatī platform and the "
            "enclosure. Then the elevation — the mouldings of the vedībandha and maṇḍovara, the "
            "jaṅghā, and the śikhara above with its latās, kūṭastambhas, stacked miniature spires, "
            "āmalaka and kalaśa. Set the design against the prāsāda taxonomy of the "
            "Samarāṅgaṇasūtradhāra and against comparable Bhūmija and Paramāra temples. Explain "
            "every technical term on first use. Iconography belongs to Chapter 9."
        ),
        "subtopics": [
            {"key": "bhumija-style",
             "question": "the Bhūmija style of temple architecture: its definition, its place within the Nāgara "
                         "tradition, its characteristic śikhara and its geographical distribution"},
            {"key": "ground-plan",
             "question": "the ground plan of the Udayeśvara temple: garbhagṛha, antarāla, gūḍhamaṇḍapa, "
                         "porches, jagatī platform, and the stellate saptaratha or saptabhūmi scheme"},
            {"key": "elevation-mouldings",
             "question": "the elevation and wall mouldings of the temple: the pīṭha, vedībandha, maṇḍovara and "
                         "jaṅghā and their sequence of courses"},
            {"key": "sikhara",
             "question": "the śikhara or superstructure of the temple: its latās, kūṭastambhas, stacked "
                         "miniature spires, āmalaka, kalaśa and the flag-bearer figure"},
            {"key": "sastraic-taxonomy",
             "question": "the classification of prāsāda or temple types in the Samarāṅgaṇasūtradhāra and other "
                         "vāstuśāstra texts, and their prescriptions for proportion and measurement"},
            {"key": "comparanda",
             "question": "other Bhūmija and Paramāra temples comparable to the Udayeśvara temple and how they "
                         "relate to it in plan, style and date"},
        ],
    },
    {
        "n": 9,
        "title": "Gods on the Walls: Sculpture, Iconography and Meaning",
        "theme": "Deities and Symbolism",
        "scope": (
            "The carved population of the temple and how to read it. Work around the walls: the "
            "Dikpālas holding the directions; the forms of Śiva — Naṭeśa, Tripurāntaka, "
            "Mṛtyuñjaya, Ardhanārīśvara, Bhairava, Lakulīśa; the goddesses, surasundarīs and "
            "attendant figures; the Vaiṣṇava, Brahmanical and syncretic images including Harihara. "
            "Cover the ornamental programme too — kīrtimukha, vyāla, foliate bands, ceilings — and "
            "explain the iconographic conventions by which attributes identify a deity. Throughout, "
            "treat the sculpture as a designed scheme carrying meaning, not a catalogue. The "
            "theology behind it is developed in Chapter 12; the structure that carries it is "
            "Chapter 8."
        ),
        "subtopics": [
            {"key": "dikpalas",
             "question": "the Dikpālas or guardians of the directions in temple sculpture: their identities, "
                         "attributes and placement on the outer walls"},
            {"key": "forms-of-siva",
             "question": "the forms of Śiva in sculpture — Naṭeśa or Naṭarāja, Tripurāntaka, Mṛtyuñjaya, "
                         "Ardhanārīśvara, Bhairava, Lakulīśa — and their iconography"},
            {"key": "goddesses-and-surasundaris",
             "question": "goddesses, surasundarīs, apsaras, nāyikās and mithuna figures in the sculpture of "
                         "central Indian temples"},
            {"key": "syncretic-and-vaisnava",
             "question": "Vaiṣṇava, Brahmā and syncretic images such as Harihara in Śaiva temple sculpture, and "
                         "rare or unusual images"},
            {"key": "ornament",
             "question": "the decorative and ornamental programme of the temple: kīrtimukha, vyāla, foliate "
                         "and geometric bands, ceilings and pillar carving"},
            {"key": "reading-iconography",
             "question": "the conventions of Hindu iconography: how attributes, mounts, gestures and "
                         "proportions identify deities and convey meaning"},
        ],
    },
    {
        "n": 10,
        "title": "Words in Stone: Inscriptions, Languages and the Serpentine Scimitar of Letters",
        "theme": None,
        "scope": (
            "The temple as a written archive accumulating over eight centuries. Survey the corpus "
            "of inscriptions on the building: the foundation records, the praśasti, the later "
            "additions, the pilgrim graffiti. Give particular attention to the "
            "varṇanāgakṛpāṇikā — the 'serpentine scimitar of letters' — its form, its reading, its "
            "kin elsewhere, and the political-Śaiva meaning it carries. Describe the languages and "
            "scripts represented: Sanskrit in Nāgarī, later Persian, later still Hindi. Close on "
            "what this epigraphic layer tells the historian that literary sources cannot. The "
            "foundation event itself is Chapter 7."
        ),
        "subtopics": [
            {"key": "inscription-corpus",
             "question": "the inscriptions of the Udayeśvara temple at Udaypur: how many, of what dates, and "
                         "where they are cut on the building"},
            {"key": "serpentine-scimitar",
             "question": "the varṇanāgakṛpāṇikā or serpentine scimitar of letters inscription at Udaypur: its "
                         "form, its decipherment and its meaning"},
            {"key": "languages-and-scripts",
             "question": "the languages and scripts of the inscriptions — Sanskrit, Nāgarī, Persian, Arabic "
                         "and later Hindi — and their palaeography"},
            {"key": "later-records",
             "question": "later inscriptions, pilgrim records and graffiti added to the temple in subsequent "
                         "centuries"},
            {"key": "epigraphy-as-evidence",
             "question": "what inscriptions reveal about medieval Indian history, land grants, genealogy and "
                         "religious patronage that literary texts do not"},
        ],
    },
    {
        "n": 11,
        "title": "Built Heritage: Fortifications, Mosques, Shrines and Stepwells",
        "theme": "Other structures besides the temple",
        "scope": (
            "Everything at Udaypur that is not the great temple. The town wall of huge uncemented "
            "blocks and its gateways; the Bijamandal or Ghaḍiyālan-kā-makān; the Bāra-khambī; the "
            "Pisnārī-kā-mandir; the Shāhī Masjid and the palace; Sher Khan's mosque — including "
            "those built of reused temple stone. Then the water architecture: stepwells, wells, "
            "ghats and the embankments of the tank. Finally the smaller shrines and the loose "
            "sculpture scattered through the town. Treat these as a built ensemble in their own "
            "right. The conquest that produced the mosques is narrated in Chapter 16; conservation "
            "is Chapter 17."
        ),
        "subtopics": [
            {"key": "fortifications",
             "question": "the fortification wall, ramparts and gateways of the town of Udaypur and other forts "
                         "of the region"},
            {"key": "hindu-structures",
             "question": "the other Hindu monuments at Udaypur — the Bijamandal or Ghaḍiyālan-kā-makān, the "
                         "Bāra-khambī, the Pisnārī-kā-mandir — and subsidiary shrines"},
            {"key": "mosques",
             "question": "the mosques and Islamic buildings at Udaypur: the Shāhī Masjid, Sher Khan's mosque, "
                         "the palace, and the reuse of temple stone in their construction"},
            {"key": "stepwells-and-water",
             "question": "stepwells, baodīs, wells, ghats and tank embankments in Udaypur and the Malwa region, "
                         "and their architecture"},
            {"key": "loose-sculpture",
             "question": "loose and reused sculpture, architectural fragments and minor shrines scattered "
                         "through the town of Udaypur"},
        ],
    },
    {
        "n": 12,
        "title": "Ritual and Knowledge: Śaiva Traditions and Intellectual Worlds",
        "theme": "Culture and Way of Life",
        "scope": (
            "The religious and intellectual world the temple was built to serve. Set out Śaiva "
            "Siddhānta as a system — pati, paśu and pāśa, the tattvas — and Bhoja's Tattvaprakāśa "
            "as its Malwa expression. Describe temple ritual: installation and consecration, daily "
            "pūjā and abhiṣeka, the festival calendar, the priesthood and those who served the "
            "shrine. Cover the institutional side — maṭhas, ascetic lineages, Pāśupata and Lakulīśa "
            "traditions — and the wider culture of Sanskrit learning, courts and libraries under "
            "Paramāra patronage. Close on the relation between king, temple and religious "
            "authority. Popular festival and folk practice belongs to Chapter 15."
        ),
        "subtopics": [
            {"key": "saiva-siddhanta",
             "question": "Śaiva Siddhānta philosophy: pati, paśu and pāśa, the tattvas, and the Tattvaprakāśa "
                         "of Bhoja"},
            {"key": "temple-ritual",
             "question": "temple ritual and worship: consecration and installation of images, daily pūjā, "
                         "abhiṣeka, offerings and the ritual calendar"},
            {"key": "priesthood-and-mathas",
             "question": "the priesthood, temple servants, maṭhas, ascetic orders and Pāśupata or Lakulīśa "
                         "Śaiva lineages and their patronage"},
            {"key": "sanskrit-learning",
             "question": "Sanskrit learning, scholarship, courts, poets and libraries under Paramāra patronage "
                         "in Malwa"},
            {"key": "king-and-temple",
             "question": "the relationship between kingship, temple foundation and religious authority in "
                         "medieval India, and the temple as an instrument of royal legitimacy"},
        ],
    },
    {
        "n": 13,
        "title": "Fields, Wells and Markets: Agriculture, Economy and Crafts",
        "theme": None,
        "scope": (
            "The material economy that sustained town and temple. The black cotton soil and what it "
            "grew — the rabī dominance of wheat, gram and linseed, the kharīf crops, the "
            "agricultural calendar and its implements. Water for cultivation: wells, tanks and the "
            "Udayasamudra, and later irrigation works. Trade and markets: the routes, the mandis, "
            "the commodities, the fairs. The temple economy of land grants, endowments and coinage. "
            "And the crafts — stone-carving above all, but also metalwork, weaving, pottery — whose "
            "practitioners made the monuments possible. Treat occupational communities descriptively "
            "and with dignity."
        ),
        "constraints": _SOCIAL_CONSTRAINTS,
        "subtopics": [
            {"key": "soil-and-crops",
             "question": "the soils, crops and agriculture of the Vidisha and Malwa region: wheat, gram, "
                         "linseed, jowār, the rabī and kharīf cycle and the agricultural calendar"},
            {"key": "irrigation",
             "question": "irrigation, wells, tanks and reservoirs in the Malwa region, the Udayasamudra, and "
                         "later irrigation projects"},
            {"key": "trade-and-markets",
             "question": "trade, markets, mandis, commodities and commercial routes of Malwa and the Vidisha "
                         "district"},
            {"key": "temple-economy",
             "question": "the temple economy: land grants, devadāna and endowments, coinage, revenue and "
                         "religious patronage in medieval India"},
            {"key": "crafts-and-artisans",
             "question": "crafts and artisans of the region: stone carving, metalwork and bell casting, "
                         "weaving, pottery, and the organisation of craft communities"},
        ],
    },
    {
        "n": 14,
        "title": "People of the Plateau: Communities, Languages and Everyday Life",
        "theme": None,
        "scope": (
            "A portrait of ordinary life beneath the great history. The communities that made up "
            "the society of the plateau and their callings, including the forest and hill "
            "communities; the demography and settlement pattern of the district. The languages: "
            "Malvi and its neighbours Bundelī and Nimāḍī, alongside Sanskrit and later tongues. The "
            "texture of religious life across Śaiva, Vaiṣṇava, Jaina and Muslim traditions as "
            "lived rather than as doctrine. And the everyday world — dress, food, dwellings, custom "
            "and the rhythm of the year. Present communities descriptively and respectfully."
        ),
        "constraints": _SOCIAL_CONSTRAINTS,
        "subtopics": [
            {"key": "communities",
             "question": "the communities, peoples and occupational groups of the Malwa plateau and Vidisha "
                         "district, including forest and hill communities such as the Bhils and Gonds"},
            {"key": "demography",
             "question": "the population, demography and settlement pattern of the Vidisha district: villages, "
                         "towns and their distribution"},
            {"key": "languages",
             "question": "the languages and dialects of Malwa — Malvi, Bundelī, Nimāḍī, Hindi, Urdu and "
                         "Sanskrit — and their distribution and literature"},
            {"key": "lived-religion",
             "question": "the lived religious life of the region across Śaiva, Vaiṣṇava, Jaina and Muslim "
                         "communities, their shrines and observances"},
            {"key": "everyday-life",
             "question": "everyday life in the villages and towns of Malwa: dress, food, dwellings, household "
                         "customs and the rhythm of the year"},
        ],
    },
    {
        "n": 15,
        "title": "Stories of Udaypur: Festivals, Folklore and Oral Histories",
        "theme": None,
        "scope": (
            "The town's own account of itself, as distinct from the documentary record. The "
            "festival life of the temple — the Śivarātri fair in Phālguna, the Śrāvaṇa pilgrimage, "
            "the fairs held beside it and the commerce and performance they draw. The legends: "
            "stories of the temple's founding and its builders, tales attached to particular images "
            "and stones, traditions about the mosque, the defacement, and buried treasure. The folk "
            "songs and the popular memory of Bhoja that survives in Malvi verse. And the oral "
            "testimony of residents. Where a story is legend rather than record, say so — but take "
            "it seriously as evidence of what the town believes."
        ),
        "subtopics": [
            {"key": "temple-festivals",
             "question": "festivals and fairs at the Udayeśvara temple and in the region: the Śivarātri mela in "
                         "Phālguna, Śrāvaṇa pilgrimage, and the commerce and performance around them"},
            {"key": "foundation-legends",
             "question": "legends and traditions about the founding of the Udaypur temple, its builders, its "
                         "images and the stones of the town"},
            {"key": "folk-memory-of-bhoja",
             "question": "folk songs, Malvi verse and popular memory of Raja Bhoja and the Paramāra kings"},
            {"key": "oral-histories",
             "question": "oral histories, local testimony and the stories residents of Udaypur tell about their "
                         "town and its monuments"},
            {"key": "performance-traditions",
             "question": "folk performance, dance, song and theatrical traditions of Malwa such as the Rai "
                         "dance and their performers"},
        ],
    },
    {
        "n": 16,
        "title": "Conquests and Regimes: Decline of the Socio-Economic Hub of Madhya Bharat",
        "theme": None,
        "scope": (
            "How Udaypur ceased to be a place of consequence. Begin with the end of Paramāra rule — "
            "the Cālukya and Kalacuri pressure, the final collapse — then the Delhi Sultanate and "
            "the Tughluq conquest of Malwa, including the conversion of temple fabric to other uses "
            "and the damage done to images. Follow the succeeding regimes: the Malwa Sultanate and "
            "Mandu, the Mughals, the Marathas and the Scindias. Throughout, track the economic "
            "story — the shifting of trade routes, the decline of the old markets, and the "
            "reduction of a regional hub to a country town. Write the religious violence as a "
            "historian: specific, evidenced and without polemic."
        ),
        "subtopics": [
            {"key": "end-of-paramaras",
             "question": "the end of Paramāra rule in Malwa: the later Paramāra kings, Cālukya and Kalacuri "
                         "invasions and the final collapse of the dynasty"},
            {"key": "sultanate-conquest",
             "question": "the Delhi Sultanate and Tughluq conquest of Malwa and Vidisha, and the destruction, "
                         "defacement or conversion of temples in the region"},
            {"key": "malwa-sultanate-mandu",
             "question": "the Malwa Sultanate, Mandu, and the Muslim rulers of Malwa and their monuments"},
            {"key": "mughals-marathas",
             "question": "Mughal, Maratha and Scindia rule over the Vidisha and Malwa region and its "
                         "administration"},
            {"key": "economic-decline",
             "question": "the economic decline of the region: the shifting of trade routes, the decay of old "
                         "markets and towns, and the coming of the railway"},
        ],
    },
    {
        "n": 17,
        "title": "Archaeologists, Laws and Repairs: Making Udaypur a \"Monument\"",
        "theme": "Udaypur in Independent India",
        "scope": (
            "How a living shrine became a protected monument. Start with pre-modern repair — the "
            "Maratha-period restoration and the brass-faced liṅga of 1775 — as a form of care that "
            "preceded archaeology. Then the colonial encounter: Cunningham and the Archaeological "
            "Survey, the surveys and reports that first described the temple, and the "
            "photographic and epigraphic record they made. Follow the development of monument "
            "legislation and the apparatus of protection, and the conservation interventions "
            "actually carried out on the fabric. Close with the administration of the site in "
            "independent India. Present-day conditions belong to Chapter 18."
        ),
        "subtopics": [
            {"key": "premodern-repair",
             "question": "pre-modern repair and restoration of the temple: the Maratha and Scindia period "
                         "intervention and the brass-faced liṅga or mukhaliṅga of 1775"},
            {"key": "colonial-survey",
             "question": "Alexander Cunningham, the Archaeological Survey of India and the early colonial "
                         "surveys, reports and photographs of the Udaypur temple"},
            {"key": "monument-law",
             "question": "legislation for the protection of ancient monuments in India and the declaration and "
                         "listing of protected sites"},
            {"key": "asi-conservation",
             "question": "Archaeological Survey of India conservation work on the Udayeśvara temple: repairs, "
                         "clearance, structural intervention and maintenance"},
            {"key": "independent-india",
             "question": "the administration, custody and management of the monument in independent India"},
        ],
    },
    {
        "n": 18,
        "title": "Present Tense: How the Town Lives with Its Past Today",
        "theme": "based on Udaypur Jagta Hua Kasba",
        "scope": (
            "Udaypur now, as a town rather than a monument — drawing above all on the testimony "
            "assembled in *Udaypur: Jagta Hua Kasba*. Describe the town's present shape and daily "
            "life: the bazaar, the streets, the houses built against and among the old fabric, the "
            "people who live there and what they do. Set out the relationship between residents and "
            "the temple: who worships, who visits, what the monument means to those beside it. "
            "Confront the condition of the built heritage — encroachment, neglect, reuse, loss — and "
            "give space to the voices recorded in the source. This chapter should read as reportage "
            "grounded in testimony, not as administrative summary."
        ),
        "subtopics": [
            {"key": "town-today",
             "question": "the present-day town of Udaypur: its bazaar, streets, houses, population and daily "
                         "life around the monuments"},
            {"key": "people-and-temple",
             "question": "the relationship between the residents of Udaypur and the temple: worship, visitors, "
                         "custodianship and what the monument means locally"},
            {"key": "condition-of-heritage",
             "question": "the present condition of the historic fabric of Udaypur: encroachment, neglect, "
                         "reuse of old structures, damage and loss"},
            {"key": "living-among-ruins",
             "question": "the communities living among the historic structures of Udaypur and how the old "
                         "buildings are used in ordinary life today"},
            {"key": "voices",
             "question": "the testimony, recollections and voices of residents of Udaypur about their town, its "
                         "history and its changes"},
        ],
    },
    {
        "n": 19,
        "title": "Afterword",
        "theme": "Conservation attempts in present day, struggles of the village, and how it can be improved",
        "scope": (
            "A closing reflection that is also an argument. Assess conservation as it currently "
            "stands at Udaypur — what has been attempted, by whom, and with what result — and be "
            "candid about its limits. Set out the difficulties the town faces: funding, the "
            "pressures and absence of tourism, access, the competing needs of residents and "
            "monument, and the livelihoods at stake. Review what INTACH and others have documented "
            "and proposed. Then say what might be done, tying the recommendation back to what the "
            "book has shown about the place. End on the temple itself. Where the sources do not "
            "support a recommendation, mark it as the author's judgement rather than evidence."
        ),
        "subtopics": [
            {"key": "conservation-today",
             "question": "current conservation efforts at Udaypur and comparable sites, what has been attempted "
                         "and the condition of the monument"},
            {"key": "struggles",
             "question": "the difficulties facing the town and village of Udaypur: livelihood, funding, "
                         "tourism, access, and conflict between residents and monument protection"},
            {"key": "documentation-and-proposals",
             "question": "heritage documentation, listing and proposals by INTACH and other bodies for Udaypur "
                         "and its monuments"},
            {"key": "ways-forward",
             "question": "approaches to conserving and reviving historic towns and temple sites: community "
                         "involvement, adaptive reuse, heritage management and interpretation"},
        ],
    },
]

# Convenience lookups
BY_NUMBER = {c["n"]: c for c in CHAPTERS}
NUMBERS = [c["n"] for c in CHAPTERS]


def get(n):
    """Return the chapter dict for number n (raises KeyError if absent)."""
    return BY_NUMBER[n]


def subtopics(n):
    """Return the sub-topic list for chapter n."""
    return BY_NUMBER[n]["subtopics"]
