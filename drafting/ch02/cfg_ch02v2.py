"""Chapter 2, draft v2 (authored history; chapters.md scope) — configuration for drafting/_pipe. Set UDAY_CFG to this file."""
from pathlib import Path

CH = 2
VERSION = "v2"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch02"))
SECTIONS = ["2.1", "2.2", "2.3", "2.4", "2.5"]
OUTLINE = D / "ch02_outline_v2.md"
PACK = D / "evidence_pack_v3.json"
LOG = D / "api_log_v2"
OUT = D / "ch02_draft_v2.md"
TITLE = "The Betwa Valley: Geography, Geology and Natural Environment"
DOCX_NAME = "Chapter 2 - The Betwa Valley - Draft v2.docx"
WMIN, WMAX, TOTAL_TARGET = 3800, 4200, 4000
BASELINE = D / "ch02_draft_v1.md"
# v1 had a different section plan; each v2 section is judged against the closest v1 section (None = no baseline)
BASELINE_MAP = {"2.1": "2.2", "2.2": "2.3", "2.3": "2.4", "2.4": None, "2.5": "2.5"}
VOICE_SRC = None
OPEN_IN = "Chapter 1 ended by turning to the country that produced the town. Open on a concrete scene or object of that country that carries the chapter's thesis."
CLOSE_OUT = "Chapter 3 turns to the landscape before Udaypur — prehistory, early Vidisha and the historical landscape of Central India."
ALLOW_EXTRA = ["Udayāditya", "Paramāra", "Udayeśvara", "Vidisha", "Betwa", "Bhoja"]
TIWARI_FULL_NAME = True
GAZ_MODERN_ONLY = True
CONFLICTS = {
    "2.1": [("Kewtan 1.8 km from the hill (committed)", [r"Kewtan", r"1\.8\s*km|1\.8 kilomet"])],
    "2.3": [("committed elevation 340–480 m, mean 410 m", [r"340", r"480", r"410"])],
}
CHAPTER_BRIEF = """You are writing Chapter 2, "The Betwa Valley: Geography, Geology and Natural Environment", of a history of Udaypur (Vidisha district, Madhya Pradesh, India) — the town founded by the Paramāra king Udayāditya, NOT Udaipur in Rajasthan. The chapter examines the valley's rivers, topography, seasons, geological formations, forests, flora and fauna, and explains how this environment shaped settlement, agriculture, access to resources and the materials available for building at Udaypur.

CHAPTER CANON (binding):
- The INTACH survey (Geo-Heritage, GEOHER) carries the land and the site; never adopt its superlatives. The district Gazetteer (GAZ) is for the modern setting only, the 1979 compilation — date-stamp it once.
- Committed figures: Udaypur's ground lies at 340–480 m, mean 410 m; the Kewtan runs 1.8 km from Shiva Pindi and 1 km from the village. One figure per measured thing; rival figures go to a {{note}}.
- *Jagta Hua Kasba* (JAGTA) is testimony: present-day observation and the author's views, never a measurement or a medieval fact; pages approximate. Its author is Vijay Manohar Tiwari: name him in full once, at his first mention in the chapter, then "Tiwari"; avoid gendered pronouns.
- Samarāṅgaṇasūtradhāra material is prescriptive norm, attributed to the text; SAMAR-* items are old OCR (never quote). Temple Economics is excluded.
- Leave the Udayasamudra tank and the fort fabric to later chapters (a clause at most); leave the region's human past before Udaypur to Chapter 3."""

# ---- authored-history run (Phase 2): facts cited, interpretation marked [INT], debates in {note: … [IDs]}
AUTHORED = True
BUDGET, RESERVE = 8.25, 1.00
INTERP_BRIEF = D / "ch02_interpretive_brief.md"
SAMPLE_TXT = D.parent / "style" / "sample_text.txt"          # the writing sample's full text (6-gram overlap check)
SUBTITLE = "Draft v2 · October 2026"
KB_IN = D / "evidence_pack_v2.json"
KB_MAX_NEW = 25
# targeted queries from the interpretive brief (where the argument needed support the pack lacked)
KB_TOPIC = "the Betwa valley around Udaypur: seasonal water and storage, the plateau's rock and quarries, forests, flora and fauna, and how they shaped the site"
KB_SUBS = "S1 rivers and hydrology; S2 topography and geology; S3 climate and seasons; S4 forests, flora and fauna; S5 environment and settlement (agriculture, resources, building stone, water supply)"
KB_GAP = {
    "2.1": ["Kewtan river dry in summer seasonal stream near Udaypur",
            "water scarcity in Udaypur village drinking water summer"],
    "2.2": ["monsoon rainfall and the agricultural calendar of Udaypur village irrigation from tanks and wells"],
    "2.3": ["Udaypur hill sandstone bedding layers colour iron red sandstone",
            "ancient quarry marks wedge holes on Udaypur hill quarrying",
            "Udaypur butte mesa height above the village"],
    "2.4": ["forest cover and trees on Udaypur hill reserved forest",
            "wildlife birds vultures bats Udaypur hill caves",
            "उदयपुर की पहाड़ी पर जंगल पेड़ और जानवर"],
    "2.5": ["construction and date of Udaypur tanks kunds and stepwells water harvesting",
            "Udaysagar tank built at the founding of Udaypur",
            "talav and baoli water harvesting tradition eastern Malwa villages",
            "live stone quarry beside Bhujariya talab Udaypur quarrying today"],
}
KB_CONTRA = {"perennial water at Udaypur": "Udaypur river perennial water flows all year",
             "wells at Udaypur": "wells at Udaypur water level summer"}

# settled ranges (never narrowed to one source's figure): (sentence trigger, required range wording, label)
SETTLED = [
    (r"(?:\d+|thirteen|sixteen)[^.]{0,40}(?:km|kilomet)[^.]{0,80}\bBasoda\b|\bBasoda\b[^.]{0,80}(?:\d+|thirteen|sixteen)[^.]{0,6}(?:km|kilomet)",
     r"13\s*[–-]\s*16|thirteen to sixteen|thirteen and sixteen", "Ganj Basoda 13–16 km"),
    (r"(?:\d+|fifty|seventy)[^.]{0,40}(?:km|kilomet)[^.]{0,80}\bVidisha\b|\bVidisha\b[^.]{0,80}(?:\d+|fifty|seventy)[^.]{0,6}(?:km|kilomet)",
     r"55\s*[–-]\s*70|fifty-five to seventy|fifty-five and seventy", "Vidisha 55–70 km"),
]
