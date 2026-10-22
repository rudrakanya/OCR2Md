"""Chapter 2, draft v3 (house voice; editor-in-chief audit approved 2026-10-14) — configuration for drafting/_pipe.
Set UDAY_CFG to this file. Sections follow chapters.md (Plan changes, 14 Oct 2026)."""
from pathlib import Path

CH = 2
VERSION = "v3"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch02"))
SECTIONS = ["2.1", "2.2", "2.3", "2.4", "2.5"]
OUTLINE = D / "ch02_plan_v3.md"
PACK = D / "evidence_pack_v4.json"
LOG = D / "api_log_v3"
OUT = D / "ch02_draft_v3.md"
TITLE = "The Betwa Valley: Geography, Geology and Natural Environment"
DOCX_NAME = "Chapter 2 - The Betwa Valley - Draft v3.docx"
SUBTITLE = "Draft v3 · October 2026"
WMIN, WMAX, TOTAL_TARGET = 3200, 4400, 4000   # user 2026-10-14: sections 70–120%, chapter 3,200–4,400, never pad
BUDGET, RESERVE = 8.25, 1.00
BASELINE = D / "ch02_draft_v1.md"
# the closest v1 section for each v3 section ("before" metrics; judge baseline)
BASELINE_MAP = {"2.1": "2.2", "2.2": "2.3", "2.3": "2.4", "2.4": "2.5", "2.5": "2.5"}
VOICE_SRC = None
OPEN_IN = "Chapter 1 ended on the ground both answers to the founding question stand on. Open on the river named in the inscriptions and the town it does not reach."
CLOSE_OUT = "Chapter 3 turns to the people who used this country long before Udaypur: prehistory, early Vidisha and the historical landscape of Central India."
ALLOW_EXTRA = ["Udayāditya", "Paramāra", "Udayeśvara", "Vidisha", "Betwa", "Bhoja", "Bhilsa", "Malwa"]
TIWARI_FULL_NAME = True
GAZ_MODERN_ONLY = True
AUTHORED = True
HOUSE_VOICE = True
CONSOLIDATE_NOTES = True
CONFLICTS = {
    "2.1": [("Kewtan 1.8 km from the hill (committed)", [r"Kewtan", r"1\.8\s*km|1\.8 kilomet"])],
    "2.3": [("committed elevation 340–480 m, mean 410 m", [r"340", r"480", r"410"])],
}
CHAPTER_BRIEF = """You are writing Chapter 2, "The Betwa Valley: Geography, Geology and Natural Environment", of a history of Udaypur (Vidisha district, Madhya Pradesh, India): the town founded by the Paramāra king Udayāditya, NOT Udaipur in Rajasthan. The chapter moves from what the land withheld (a river that does not reach the town, wells that fail in summer), to what it offered (four wet months, black soil, a seam of building stone), to what people made of it (kings' reservoirs and villagers' tanks, a town built from its own hill). The land is the setting people worked with: never say or imply that it caused the founding.

CHAPTER CANON (binding):
- The INTACH survey (Geo-Heritage, GEOHER) carries the land and the site; never adopt its superlatives. The district Gazetteer (GAZ) is the 1979 compilation, for the modern setting: date-stamp it once. Modern climate and flow data describe the present regime; never project them back to the eleventh century as fact.
- Committed figures: Udaypur's ground lies at 340–480 m, mean 410 m; the Kewtan runs 1.8 km from Shiva Pindi and 1 km from the village. One figure per measured thing; rival figures go to a {{note}}.
- *Jagta Hua Kasba* (JAGTA) is testimony by Vijay Manohar Tiwari: name in full once, at the first mention in the chapter, then "Tiwari"; no gendered pronouns; never "a visitor"; never a measurement or a medieval fact.
- Samarāṅgaṇasūtradhāra material is prescriptive norm, attributed to the treatise, never a record of why Udaypur was chosen; SAMAR items are old OCR (never quote). Temple Economics is excluded.
- Bhoja's dam and the Bhojpur temple appear only briefly, as comparative evidence of Paramāra water engineering. Udaypur's own tanks are treated at landscape level here; their detail belongs to Chapter 7.
- Wildlife belongs to Chapter 12 and the lichen dating of the fort wall to Chapter 7: leave both out. Leave the region's human past before Udaypur to Chapter 3.
- Compatibility is not identity: never merge two tanks, structures, observations or hypotheses unless an item says they are the same."""

# ---- context retrieval (approved; existing corpus only)
KB_IN = D / "evidence_pack_v4_base.json"
KB_MAX_NEW = 12
KB_TOPIC = "the Betwa valley in Paramāra political geography and Paramāra water engineering: Bhilsa as the eastern seat, the treatise's authorship, reservoirs built with temples"
KB_SUBS = "S1 rivers and hydrology; S2 topography and geology; S3 climate and seasons; S4 forests and land use; S5 environment and settlement (agriculture, resources, building stone, water supply)"
KB_SECTIONS = ["2.1", "2.2", "2.3", "2.4", "2.5"]
KB_GAP = {
    "2.1": ["Bhilsa Bhailasvamin Vidisha on the Betwa as the eastern centre of the Paramara kingdom",
            "the Betwa valley as a route between Malwa and Bundelkhand in the eleventh and twelfth centuries"],
    "2.4": ["Samarangana Sutradhara composed by king Bhoja, treatise on architecture and town planning, its authorship",
            "Paramara kings built lakes and tanks together with temples, reservoirs at Dhara and elsewhere in Malwa"],
}
KB_CONTRA = {}

SETTLED = [
    (r"(?:\d+|thirteen|sixteen)[^.]{0,40}(?:km|kilomet)[^.]{0,80}\bBasoda\b|\bBasoda\b[^.]{0,80}(?:\d+|thirteen|sixteen)[^.]{0,6}(?:km|kilomet)",
     r"13\s*[–-]\s*16|thirteen to sixteen|thirteen and sixteen", "Ganj Basoda 13–16 km"),
    (r"(?:\d+|fifty|seventy)[^.]{0,40}(?:km|kilomet)[^.]{0,80}\bVidisha\b|\bVidisha\b[^.]{0,80}(?:\d+|fifty|seventy)[^.]{0,6}(?:km|kilomet)",
     r"55\s*[–-]\s*70|fifty-five to seventy|fifty-five and seventy", "Vidisha 55–70 km"),
]
