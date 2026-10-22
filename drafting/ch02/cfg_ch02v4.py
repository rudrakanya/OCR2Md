"""Chapter 2, draft v4 (fresh draft from the contents rebuild; in-session, no API) — configuration for drafting/_pipe.
Set UDAY_CFG to this file. Sections follow editorial/Udaypur_Book_Contents.md (10 units, one section each)."""
from pathlib import Path

CH = 2
VERSION = "v4"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch02"))
SECTIONS = [f"2.{i}" for i in range(1, 11)]
OUTLINE = D / "ch02_plan_v4.md"
PACK = D / "evidence_pack_v5.json"
LOG = D / "api_log_v4"
OUT = D / "ch02_draft_v4.md"
TITLE = "The Betwa Valley: Geography, Geology and Natural Environment"
DOCX_NAME = "Chapter 2 - The Betwa Valley - Draft v4.docx"
SUBTITLE = "Draft v4 · October 2026"
WMIN, WMAX, TOTAL_TARGET = 0, 10**9, 0   # user 17 Oct 2026: no word targets; each unit as long as its evidence carries
NO_LENGTH = True
BUDGET, RESERVE = 0.00, 0.00   # no API calls (user rule); in-session drafting and verification
BASELINE = None
BASELINE_MAP = {}
VOICE_SRC = None
OPEN_IN = "Chapter 1 ended on the ground both answers to the founding question stand on. Open on the stream a kilometre from the village and the river it joins."
CLOSE_OUT = "Chapter 3 turns to the people who used this country long before Udaypur: prehistory, early Vidisha and the historical landscape of Central India."
ALLOW_EXTRA = ["Udayāditya", "Paramāra", "Paramāras", "Udayeśvara", "Vidisha", "Betwa", "Bhoja", "Bhilsa", "Malwa", "Udaypur", "Udayapura",
               "Vētravatī", "Bhojpur", "Dhārā", "Kewtan", "Keotan", "Shiva", "Pindi", "Garhi", "Teonda", "Basoda", "Kaimur", "Rewa", "Candellas"]
TIWARI_FULL_NAME = False      # introduced in full in 1.1 (book ledger); "Tiwari" here
GAZ_MODERN_ONLY = True
AUTHORED = True
HOUSE_VOICE = True
CONSOLIDATE_NOTES = True      # footnote.py: one reader-facing note per paragraph; IDs in hidden comments

CONFLICTS = {
    "2.1": [("Kewtan 1.8 km from the hill (committed)", [r"Kewtan", r"1\.8\s*km|1\.8 kilomet"])],
    "2.2": [("committed elevation 340–480 m, mean 410 m", [r"340", r"480", r"410"])],
    "2.8": [("who breached the dam", [r"Hoshang", r"Hussain"])],
}

CHAPTER_BRIEF = """You are writing Chapter 2, "The Betwa Valley: Geography, Geology and Natural Environment", of a history of Udaypur (Vidisha district, Madhya Pradesh, India): the town founded by the Paramāra king Udayāditya, NOT Udaipur in Rajasthan. The land is the setting people worked with: never say or imply that it caused the founding.

CHAPTER CANON (binding):
- The survey (Geo-Heritage, GEOHER) carries the land and the site; never adopt its superlatives. The district Gazetteer (GAZ) is the 1979 compilation, for the modern setting. Modern climate and flow data describe the present regime; never project them back to the eleventh century as fact.
- Committed figures: Udaypur's ground lies at 340–480 m, mean 410 m; the Kewtan runs 1.8 km from Shiva Pindi and 1 km from the village. Rival figures go to a {{note}}.
- Tiwari (introduced in full in 1.1): testimony; no gendered pronouns; never a measurement or a medieval fact. U7: one attributed sentence on the illegal-quarrying report, naming no one.
- Samarāṅgaṇasūtradhāra material is prescriptive norm, attributed to the treatise, never a record of why Udaypur was chosen; SAMAR items are old OCR (never quote).
- Bhoja's dam is comparison only. Udaypur's tanks at landscape level (detail: Chapter 7). Wildlife: Chapter 12; lichen dating: Chapter 7. The human past before Udaypur: Chapter 3.
- U6: 1059 is a reading, not a date; do not adopt the survey's 1059 for the tank.
- Compatibility is not identity: never merge two tanks, streams, structures, observations or hypotheses unless an item says they are the same."""


def extra_rules(text, P, smap):
    import re
    fails = []
    for pat, what in ((r"\blichen", "lichen dating (Ch 7)"), (r"\b1059\b", "1059 adopted as a date (U6)")):
        if re.search(pat, re.sub(r"\{\{note:.*?\}\}", "", text, flags=re.S)):
            fails.append({"sec": "chapter", "rule": "canon", "detail": what})
    return fails


# ---- context retrieval (not used in v4; kept for the pipeline's imports)
KB_IN = D / "evidence_pack_v4_base.json"
KB_MAX_NEW = 0
KB_TOPIC = ""
KB_SUBS = "S1 rivers and hydrology; S2 topography and geology; S3 climate and seasons; S4 forests and land use; S5 environment and settlement"
KB_SECTIONS = SECTIONS
KB_GAP = {}
KB_CONTRA = {}

SETTLED = []   # Ch 2 gives no distances from Udaypur to Basoda or Vidisha
