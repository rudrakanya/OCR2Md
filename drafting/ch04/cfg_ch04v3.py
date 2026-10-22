"""Chapter 4, draft v3 (contents rebuild, 19 Oct 2026; in-session, no API) — configuration for drafting/_pipe.
Set UDAY_CFG to this file. Sections follow editorial/Udaypur_Book_Contents.md (20 units, one section each)."""
from pathlib import Path

CH = 4
VERSION = "v3"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch04"))
SECTIONS = [f"4.{i}" for i in range(1, 21)]
OUTLINE = D / "ch04_plan_v3.md"
PACK = D / "evidence_pack_v3.json"
LOG = D / "api_log_v3"
OUT = D / "ch04_draft_v3.md"
TITLE = "The Paramāras and the Foundation of Udaypur: Kingship, Patronage and Urban Formation"
DOCX_NAME = "Chapter 4 - The Paramāras and the Foundation of Udaypur - Draft v3.docx"
SUBTITLE = "Draft v3 · October 2026"
WMIN, WMAX, TOTAL_TARGET = 0, 10**9, 0   # user 17 Oct: no word targets; each unit as long as its evidence carries
NO_LENGTH = True
BUDGET, RESERVE = 0.00, 0.00   # no API calls (user rule); in-session drafting and verification
BASELINE = None
BASELINE_MAP = {}
VOICE_SRC = None
OPEN_IN = ("Chapter 3 ended on the open question of who held Udaypur's hill, and on Ganguly's reconstruction of the Paramāra founder "
           "as a vassal of the Rāṣṭrakūṭas. Open on the dynasty's own claim about itself, first told on Udaypur's stone.")
CLOSE_OUT = ("Chapter 5 opens on the Udayeśvara temple as a building. End on the temple as the one work at Udaypur a contemporary record "
             "gives to the reign: named after its builder, dated V.S. 1137 by its flag-staff record, its start a reading.")
ALLOW_EXTRA = ["Udayāditya", "Paramāra", "Paramāras", "Udayeśvara", "Udayapura", "Udaypur", "Vidisha", "Bhilsa", "Malwa", "Dhārā", "Bhoja",
               "Ujjain", "Gujarat", "Caulukya", "Caulukyas", "Rāṣṭrakūṭa", "Rāṣṭrakūṭas", "Candella", "Candellas", "Kalacuri", "Kalacuris",
               "Cālukya", "Cālukyas", "Pratihāra", "Pratihāras", "Shergadh", "Dōngargāon", "Jainād", "Pathari", "Muñja", "Sīyaka",
               "Sindhurāja", "Jayasiṃha", "Naravarman", "Lakṣmadeva", "Jagaddēva", "Karṇa", "Bhīma", "Vākpati", "Upendra", "Karṇāṭa", "Karṇāṭas", "Deccan", "Koṅkaṇa", "Lāṭa", "Chēdi", "Gūrjara"]
TIWARI_FULL_NAME = False      # named in full in Chapter 1; here "Tiwari"
GAZ_MODERN_ONLY = False       # the Gazetteer may carry dynastic claims here, phrased as its own
GAZ_MAX_SHARE = 0.40          # user 2026-10-14
AUTHORED = True
HOUSE_VOICE = True
CONSOLIDATE_NOTES = True

CONFLICTS = {
    "4.13": [("1059 a reading, 1080 the firm date (U6)", [r"\b1059\b", r"\b1080\b", r"reading|read"])],
    "4.12": [("kinship: brother, dissent in a note (D2)", [r"brother", r"bandhu|relative|kinsman"])],
}

CHAPTER_BRIEF = """Chapter 4 of the Udaypur history: the Paramāras as a polity and the foundation of Udaypur within their history. In-session drafting from ch04_plan_v3.md; no API calls. Canon: style/style_sheet.md §13 (U1, R1–R4, D1, D2, D4)."""


def extra_rules(text, P, smap):
    import re
    fails = []
    secs = re.split(r"(?m)^(?=## 4\.\d+)", text)
    for s in secs:
        m = re.match(r"## (4\.\d+)", s)
        sec = m.group(1) if m else "chapter"
        plain = re.sub(r"\[[^\]]*\]", "", s)
        for sent in re.split(r"(?<=[.!?”])\s+", re.sub(r"[“\"][^”\"]*[”\"]", "", plain)):
            if re.search(r"\bnephew\b", sent) and re.search(r"Udayāditya", sent):
                fails.append({"sec": sec, "rule": "canon D2", "detail": "'nephew' used of Udayāditya: " + sent.strip()[:120]})
        if sec not in ("4.19", "chapter") and re.search(r"mahādvādaśaka|Mahādvādaśaka|Bhṛṅgārikā|Bhāillasvāmi-", re.sub(r"\{\{note:.*?\}\}", "", plain, flags=re.S)):
            fails.append({"sec": sec, "rule": "canon R4", "detail": "a 1170s territorial term outside 4.19"})
        for sent in re.split(r"(?<=[.!?”])\s+", re.sub(r"\{\{note:.*?\}\}", "", plain, flags=re.S)):
            if re.search(r"\bKarṇa\b", sent) and not re.search(r"Kalacuri|Caulukya|Gujarat|Gurjara|Dāhal|Chedi|Cedi|does not say|unspecified|which Karṇa|without saying|not say", sent):
                fails.append({"sec": sec, "rule": "canon R2", "detail": "Karṇa without dynasty or an explicit 'unspecified': " + sent.strip()[:120]})
    return fails


# ---- context retrieval (not used in v3; kept for the pipeline's imports)
KB_IN = D / "evidence_pack_v2.json"
KB_MAX_NEW = 0
KB_TOPIC = ""
KB_SUBS = ""
KB_SECTIONS = SECTIONS
KB_GAP = {}
KB_CONTRA = {}
SETTLED = [
    (r"(?:\d+|thirteen|sixteen)[^.]{0,40}(?:km|kilomet)[^.]{0,80}\bBasoda\b|\bBasoda\b[^.]{0,80}(?:\d+|thirteen|sixteen)[^.]{0,6}(?:km|kilomet)",
     r"13\s*[–-]\s*16|thirteen to sixteen|thirteen and sixteen", "Ganj Basoda 13–16 km"),
]
REPORT_OUTLINE_NOTES = ""
