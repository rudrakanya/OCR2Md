"""Chapter 4, draft v1 (in-session drafting; no API calls, user ruling 2026-10-15) - configuration for drafting/_pipe.
Set UDAY_CFG to this file. Plan: ch04_plan_v1.md."""
from pathlib import Path

CH = 4
VERSION = "v1"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch04"))
SECTIONS = ["4.1", "4.2", "4.3", "4.4", "4.5"]
OUTLINE = D / "ch04_plan_v1.md"
PACK = D / "evidence_pack_v1.json"
LOG = D / "api_log_v1"
OUT = D / "ch04_draft_v1.md"
TITLE = "The Paramāras and the Foundation of Udaypur: Kingship, Patronage and Urban Formation"
DOCX_NAME = "Chapter 4 - The Paramāras and the Foundation of Udaypur - Draft v1.docx"
SUBTITLE = "Draft v1 · October 2026"
WMIN, WMAX, TOTAL_TARGET = 4750, 5250, 5000   # sections 70–120%, chapter 3,200–4,400, never pad (user 2026-10-14)
BUDGET, RESERVE = 0.00, 0.00                  # approved 15 Oct (includes sunk spend)
BASELINE = None
BASELINE_MAP = {}
VOICE_SRC = None
OPEN_IN = ("Chapter 3 ended: Who held the hill itself in those years is not known. Open on Siyaka II's eastern limit at Vidisha, keeping that gap open.")
CLOSE_OUT = ("Chapter 5 opens on the Udayesvara temple as a building. End on the temple as the one work at Udaypur a contemporary record gives to the reign.")
ALLOW_EXTRA = ["Udayāditya", "Paramāra", "Paramāras", "Udayeśvara", "Udayapura", "Vidisha", "Bhilsa", "Malwa", "Dhārā", "Bhoja", "Ujjain", "Gujarat", "Caulukya", "Caulukyas", "Rāṣṭrakūṭa", "Rāṣṭrakūṭas", "Chandellas", "Kalachuri", "Kalachuris", "Udaypur"]
TIWARI_FULL_NAME = False      # named in full in Chapter 1; here "Tiwari"
GAZ_MODERN_ONLY = False       # the Gazetteer may carry ancient history in this chapter, capped below
GAZ_MAX_SHARE = 0.40          # user 2026-10-14: the Gazetteer supplies at most 40% of any section's cited items
AUTHORED = True
HOUSE_VOICE = True
CONSOLIDATE_NOTES = True

CONFLICTS = {}

CHAPTER_BRIEF = """Chapter 4 of the Udaypur history. In-session drafting from ch04_plan_v1.md; no API calls."""

# ---- context retrieval (existing corpus only; user 2026-10-14)
KB_IN = D / "evidence_pack_v1.json"
KB_MAX_NEW = 30
KB_TOPIC = ("the country around Udaypur before the Paramāras: prehistoric traces near Basoda, the old centre at Vidisha and its roads, "
            "Gupta and post-Gupta rock-cut and temple sites near Udaypur, Bhilsa's origin and name, and the eighth-to-tenth-century "
            "frontier on Udaypur's own range (Gyaraspur, Pathari, Badoh)")
KB_SUBS = "S1 prehistory; S2 early Vidisha/Besnagar; S3 ancient regional names; S4 powers before the Paramāras; S5 routes, sacred places and Udaypur's neighbours"
KB_SECTIONS = SECTIONS
KB_GAP = {}
KB_CONTRA = {}

SETTLED = [
    (r"(?:\d+|thirteen|sixteen)[^.]{0,40}(?:km|kilomet)[^.]{0,80}\bBasoda\b|\bBasoda\b[^.]{0,80}(?:\d+|thirteen|sixteen)[^.]{0,6}(?:km|kilomet)",
     r"13\s*[–-]\s*16|thirteen to sixteen|thirteen and sixteen", "Ganj Basoda 13–16 km"),
    (r"(?:\d+|fifty|seventy)[^.]{0,40}(?:km|kilomet)[^.]{0,80}\bVidisha\b|\bVidisha\b[^.]{0,80}(?:\d+|fifty|seventy)[^.]{0,6}(?:km|kilomet)",
     r"55\s*[–-]\s*70|fifty-five to seventy|fifty-five and seventy", "Vidisha 55–70 km"),
]

REPORT_OUTLINE_NOTES = ""
