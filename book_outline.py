#!/usr/bin/env python3
"""
book_outline.py — the single source of truth for the book's structure.

Everything about the seven chapters lives here: title, scope (the brief given to
the drafting model), and the knowledge-base search queries used to gather each
chapter's evidence. `make_evidence.py`, `draft_chapter.py`, and `assemble_book.py`
all import from this file, so editing the outline in one place keeps the whole
pipeline consistent.

To change the book: edit BOOK_TITLE / BOOK_SUBTITLE, or add/edit entries in
CHAPTERS (each needs `n`, `title`, `scope`, and `queries`). Then re-run
make_evidence.py and draft_chapter.py.
"""

BOOK_TITLE = "The Rising Lord"
BOOK_SUBTITLE = ("The Nīlakaṇṭheśvara (Udayeśvara) Temple of Udaypur "
                 "and the World of the Paramāra Rajputs")

CHAPTERS = [
    {
        "n": 1,
        "title": "The Rising Lord: An Introduction to the Nīlakaṇṭheśvara (Udayeśvara) Temple and Its World",
        "scope": ("Introduce the temple and its world: the town of Udaypur in Vidisha and the Betwa (Vetravatī) "
                  "country; the Malwa plateau / Avanti as a historical region; why this 11th-century Śiva temple "
                  "matters; and a preview of the book's arc (dynasty, founder-king, architecture, "
                  "sculpture/philosophy, inscriptions/afterlife)."),
        "queries": [
            "Udayapur town Vidisha district geography setting and the Betwa river",
            "significance and importance of the Udayesvara Nilkantheshwara temple",
            "Malwa plateau as a historical region Avanti overview",
        ],
    },
    {
        "n": 2,
        "title": "The Fire-Born: Origins and Rise of the Paramāra Rajputs",
        "scope": ("The Agnikula ('fire-born') origin legend on Mount Abu and its political work; Avanti/Malwa with "
                  "Ujjain and Dhārā; the earliest rulers (Upendra, Vairisiṃha, Sīyaka) and the rise from vassalage; "
                  "Vākpati Mūñja the warrior-poet, his southern wars and patronage and fall. End on the threshold of Bhoja."),
        "queries": [
            "origin of the Paramara Rajput dynasty Agnikula fire myth Mount Abu Vasistha",
            "early Paramara rulers Upendra Vairisimha Siyaka Vakpati rise to power",
            "Avanti Malwa Dhara Ujjain Paramara capital and titles",
            "Munja Vakpati warrior poet patron campaigns against the Calukyas",
        ],
    },
    {
        "n": 3,
        "title": "The Golden Noon: Bhoja and the Paramāra Zenith",
        "scope": ("Bhoja the scholar-king as the apogee of Paramāra power and culture; his vast attributed works "
                  "(incl. the Samarāṅgaṇasūtradhāra) and the authorship debate; his building and engineering (Dhārā, "
                  "Bhojpur and its lake); court and legend; then the unravelling and decline after his death that "
                  "sets up Udayāditya's recovery."),
        "queries": [
            "Bhoja Paramara the scholar king reign and achievements",
            "literary and scientific works of Bhoja Samaranganasutradhara Sarasvatikanthabharana",
            "Bhojpur lake Dhara cultural patronage learning",
            "decline of the Paramaras after Bhoja invasions Calukyas of Gujarat",
        ],
    },
    {
        "n": 4,
        "title": "Udayāditya and the Founding of Udayapur",
        "scope": ("Udayāditya's accession amid post-Bhoja crisis and his consolidation; the founding of the city "
                  "Udayapur with the Udayasamudra tank; the building of the Nīlakaṇṭheśvara/Udayeśvara temple with "
                  "its dated inscriptions (V.S. 1116/1059 and V.S. 1137/1080); the Udayapur Praśasti and its "
                  "sun-imagery. Flag date disagreements."),
        "queries": [
            "Udayaditya Paramara accession and consolidation of the kingdom",
            "founding of the city of Udayapur and the Udayasamudra tank",
            "Udayapur Prasasti inscription temple foundation and dates 1059 1080",
            "Udayaditya builds the Siva temple Nilakanthesvara at Udayapur",
        ],
    },
    {
        "n": 5,
        "title": "The Bhūmija Vision: Plan and Architecture",
        "scope": ("The Bhūmija style within Nāgara architecture and the Samarāṅgaṇasūtradhāra's temple taxonomy; the "
                  "rotated-square plan (saptaratha/saptabhūmi); the parts (garbhagṛha, antarāla, gūḍhamaṇḍapa and "
                  "porches, jagati, Vedī); the elevation — maṇḍovara mouldings rising into the śikhara with its "
                  "stacked miniature spires. Explain terms."),
        "queries": [
            "Bhumija style of architecture sikhara superstructure",
            "Udayesvara temple ground plan garbhagrha mandapa jagati saptaratha saptabhumi",
            "mandovara mouldings spire kutastambha latas of the tower",
            "Samaranganasutradhara prasada temple types classification",
        ],
    },
    {
        "n": 6,
        "title": "Stone Made Speech: Sculpture, Iconography, and the Śaiva Vision",
        "scope": ("The sculptural programme of the outer walls (Dikpālas; Śiva as Naṭeśa, Tripurāntaka, Mṛtyuñjaya; "
                  "goddesses and surasundarīs; syncretic Harihara/Ardhanārīśvara) AND the theology it embodies — "
                  "Śaiva Siddhānta and Bhoja's Tattvaprakāśa — reading the carved walls as theology made visible."),
        "queries": [
            "iconography of the outer walls Dikpalas guardians of directions",
            "forms of Siva Natesa Tripurantaka Mrtyunjaya sculpture at the temple",
            "syncretic and rare images Harihara Ardhanarisvara goddesses surasundaris",
            "Saiva Siddhanta philosophy Tattvaprakasa of Bhoja pati pasu pasa tattvas",
        ],
    },
    {
        "n": 7,
        "title": "An Archive in Stone: Inscriptions, Conquest, and Afterlife",
        "scope": ("The temple as an eight-century epigraphic archive; the 'serpentine scimitar of letters' "
                  "(varṇanāgakṛpāṇikā) and its kin and political-Śaiva meaning; the Tughluq-era mosque of temple "
                  "stone; later defacement traditions; the Maratha brass-faced liṅga (1775) and modern ASI "
                  "conservation; a brief closing reflection. Flag disagreements."),
        "queries": [
            "serpentine scimitar of letters inscription varnanagakrpanika Udaypur",
            "inscriptions of the Udayesvara temple across centuries Sanskrit Persian Hindi",
            "Tughluq mosque conversion temple destruction at Udayapur",
            "brass lingam mukhalinga Scindia Maratha restoration and ASI conservation",
        ],
    },
]

# Convenience lookups
BY_NUMBER = {c["n"]: c for c in CHAPTERS}
NUMBERS = [c["n"] for c in CHAPTERS]


def get(n):
    """Return the chapter dict for number n (raises KeyError if absent)."""
    return BY_NUMBER[n]
