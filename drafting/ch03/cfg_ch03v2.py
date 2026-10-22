"""Chapter 3, draft v2 (house voice; editor-in-chief audit and the user's decisions of 2026-10-14) — configuration for
drafting/_pipe. Set UDAY_CFG to this file. Plan: ch03_plan_v2.md (built in drafting/editorial/ first, copied here)."""
from pathlib import Path

CH = 3
VERSION = "v2"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch03"))
SECTIONS = ["3.1", "3.2", "3.3", "3.4", "3.5"]
OUTLINE = D / "ch03_plan_v2.md"
PACK = D / "evidence_pack_v3.json"
LOG = D / "api_log_v2"
OUT = D / "ch03_draft_v2.md"
TITLE = "Before Udaypur: Prehistory, Early Vidisha and the Historical Landscape of Central India"
DOCX_NAME = "Chapter 3 - Before Udaypur - Draft v2.docx"
SUBTITLE = "Draft v2 · October 2026"
WMIN, WMAX, TOTAL_TARGET = 3200, 4400, 3800   # sections 70–120%, chapter 3,200–4,400, never pad (user 2026-10-14)
BUDGET, RESERVE = 8.00, 1.00                  # approved 15 Oct (includes sunk spend)
BASELINE = D / "ch03_draft_v1.md"
BASELINE_MAP = {"3.1": "3.1", "3.2": "3.2", "3.3": "3.4", "3.4": "3.4", "3.5": "3.5"}
VOICE_SRC = None
OPEN_IN = ("Chapter 2 ended on the setting a founder found, and on a country used long before Udaypur had a name. "
           "Open on the oldest human traces in the valleys around Udaypur; the hill's caves are already known to the reader.")
CLOSE_OUT = ("Chapter 4 turns to the Paramāras' arrival in this frontier and the foundation of Udaypur. Hand on by content; "
             "do not re-introduce the Paramāras, Dhārā or Bhilsa as the kingdom's eastern limit (Chapter 1 has done so).")
ALLOW_EXTRA = ["Udayāditya", "Paramāra", "Paramāras", "Udayeśvara", "Vidisha", "Besnagar", "Bhilsa", "Betwa", "Malwa"]
TIWARI_FULL_NAME = False      # named in full in Chapter 1; here "Tiwari"
GAZ_MODERN_ONLY = False       # the Gazetteer may carry ancient history in this chapter, capped below
GAZ_MAX_SHARE = 0.40          # user 2026-10-14: the Gazetteer supplies at most 40% of any section's cited items
AUTHORED = True
HOUSE_VOICE = True
CONSOLIDATE_NOTES = True

CONFLICTS = {
    "3.4": [("Besnagar's end: date range seventh to tenth century", [r"Besnagar|old (?:city|town)", r"seventh|7th|eighth|8th|ninth|9th", r"tenth|10th"])],
}

CHAPTER_BRIEF = """You are writing Chapter 3, "Before Udaypur: Prehistory, Early Vidisha and the Historical Landscape of Central India", of a history of Udaypur (Vidisha district, Madhya Pradesh, India): the town founded by the Paramāra king Udayāditya, NOT Udaipur in Rajasthan. Udaypur is the centre of gravity. Early Vidisha and Central India enter only where they change what Udaypur means: the country it stands in, the old centre and roads it lay beside, the carved and sacred landscape around its hill, the town whose name its eleventh-century division would carry, and the frontier its own range had become by the tenth century.

CHAPTER CANON (binding):
- Stop before the Paramāra foundation (Chapter 4). Do not re-introduce the Paramāras as a polity, Dhārā, or Bhilsa as the kingdom's eastern limit (Chapter 1 did). Leave the founding question (founded or taken over?) to Chapter 1: the cave dated to the sixth century and the two-line inscription assigned to the eighth are the survey's proposals; state them as proposals, in their age, without re-arguing the question. Leave temple architecture to Chapter 5, epigraphy in detail to Chapter 6, the tanks to Chapter 7, rivers, rock and caves to Chapter 2 (refer back by content, never "as Chapter 2 showed").
- Compatibility is not identity: never connect the two-line inscription the survey reads tentatively with the cave inscription it says "remains to be deciphered"; never connect Udayagiri with Udaypur by name; never merge Badoh, Pathari, Gyaraspur or Udaypur, or two dynasties, or two dates.
- Prehistory is thin: the tools and the mound are district-level finds; nothing prehistoric is recorded on Udaypur's own hill. Say so once, plainly; never pad it.
- Ancient literature (epics, Purāṇas, Buddhist and Jain texts, Kālidāsa) gives tradition and literary memory, told as such; archaeology and inscriptions give dated evidence; keep the two apart. A royal inscription's claim is a claim.
- Dates as the evidence gives them; where items differ, a range around the object.
- *Jagta Hua Kasba* (JAGTA) is testimony by Vijay Manohar Tiwari, named in full in Chapter 1: here "Tiwari"; no gendered pronouns; never "a visitor"; never the source of an ancient fact or a measurement; pages approximate. Tiwari's surmises (Viṣṇu images from Muradpur to Sonari; the road of devotion) are Tiwari's reading, attributed.
- The district Gazetteer (GAZ) is the 1979 compilation. It may carry ancient history here, but supplies at most 40% of any section's cited items; where it is the only source for an ancient claim, keep the claim modest.
- Al-Bīrūnī's c. 1030 remark is used here only for the origin of Bhilsa's name in the Sun image; Bhilsa's political place belongs to Chapter 2 and Chapter 1.
- Temple Economics is excluded entirely."""

# ---- context retrieval (existing corpus only; user 2026-10-14)
KB_IN = D / "evidence_pack_v3_base.json"
KB_MAX_NEW = 30
KB_TOPIC = ("the country around Udaypur before the Paramāras: prehistoric traces near Basoda, the old centre at Vidisha and its roads, "
            "Gupta and post-Gupta rock-cut and temple sites near Udaypur, Bhilsa's origin and name, and the eighth-to-tenth-century "
            "frontier on Udaypur's own range (Gyaraspur, Pathari, Badoh)")
KB_SUBS = "S1 prehistory; S2 early Vidisha/Besnagar; S3 ancient regional names; S4 powers before the Paramāras; S5 routes, sacred places and Udaypur's neighbours"
KB_SECTIONS = SECTIONS
KB_GAP = {
    "3.1": ["prehistoric rock shelters or rock paintings in Vidisha district near Basoda",
            "stone age tools or microliths found near Ganj Basoda or Udaypur",
            "ancient mound excavated in Vidisha district chalcolithic site name and location"],
    "3.2": ["Vindhyan sandstone sculpture tradition at Besnagar and Sanchi, early stone carving in the Vidisha region",
            "early Shaiva images Ekamukha linga Besnagar Vidisha"],
    "3.3": ["Gupta period temples and rock-cut shrines near Udaypur, Pathari, Badoh, Gyaraspur",
            "sixth century cave on the hill at Udaypur with sculpture",
            "Udayagiri caves Gupta Varaha panel near Vidisha"],
    "3.4": ["Bhailasvamin Sun temple at Bhilsa, origin of the name Bhilsa",
            "inscription of the Rashtrakuta king Krishna III at Vidisha mentioning Bhillasvamin",
            "Bhailasvami mahadvadasaka mandala the province around Bhilsa"],
    "3.5": ["Gyaraspur temples Maladevi Bajramath date ninth tenth century",
            "Pathari pillar inscription of Parabala Rashtrakuta minister 861",
            "Gadarmal temple at Badoh date and patron",
            "Pratihara rule over Vidisha and eastern Malwa in the ninth and tenth centuries",
            "Udaypur before the Paramaras frontier post earlier settlement"],
}
KB_CONTRA = {"Besnagar's end": "Besnagar destroyed deluge abandoned Bhilsa founded eighth century tenth century",
             "Pathari pillar date": "Pathari pillar inscription date Parabala 861"}

SETTLED = [
    (r"(?:\d+|thirteen|sixteen)[^.]{0,40}(?:km|kilomet)[^.]{0,80}\bBasoda\b|\bBasoda\b[^.]{0,80}(?:\d+|thirteen|sixteen)[^.]{0,6}(?:km|kilomet)",
     r"13\s*[–-]\s*16|thirteen to sixteen|thirteen and sixteen", "Ganj Basoda 13–16 km"),
    (r"(?:\d+|fifty|seventy)[^.]{0,40}(?:km|kilomet)[^.]{0,80}\bVidisha\b|\bVidisha\b[^.]{0,80}(?:\d+|fifty|seventy)[^.]{0,6}(?:km|kilomet)",
     r"55\s*[–-]\s*70|fifty-five to seventy|fifty-five and seventy", "Vidisha 55–70 km"),
]

REPORT_OUTLINE_NOTES = ""
