"""Chapter 5, draft v1 (21 Oct 2026; in-session, no API) — configuration for drafting/_pipe.
Set UDAY_CFG to this file. Sections follow editorial/Udaypur_Book_Contents.md (28 units, one section each)."""
from pathlib import Path

CH = 5
VERSION = "v1"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch05"))
SECTIONS = [f"5.{i}" for i in range(1, 29)]
OUTLINE = D / "ch05_plan_v1.md"
PACK = D / "evidence_pack_v1.json"
LOG = D / "api_log_v1"
OUT = D / "ch05_draft_v1.md"
TITLE = "The Udayeśvara Temple: Architecture, Sculpture and Religious Iconography"
DOCX_NAME = "Chapter 5 - The Udayeśvara Temple - Draft v1.docx"
SUBTITLE = "Draft v1 · October 2026"
WMIN, WMAX, TOTAL_TARGET = 0, 10**9, 0   # user 17 Oct: no word targets; each unit as long as its evidence carries
NO_LENGTH = True
BUDGET, RESERVE = 0.00, 0.00   # no API calls (user rule); in-session drafting and verification
BASELINE = None
BASELINE_MAP = {}
VOICE_SRC = None
OPEN_IN = ("Chapter 4 ended on the Udayeśvara as the one royal work at Udaypur tied to the reign by a record of the time (V.S. 1137, A.D. 1080), "
           "named after its builder, its start a reading, its sanctum stellate-cum-circular of seven projections and seven storeys. Open on the building itself.")
CLOSE_OUT = ("Chapter 6 reads the inscriptions as texts. End on how far meaning can be read into the building, and on the meanings the temple's own "
             "inscribed words state, which Chapter 6 reads.")
ALLOW_EXTRA = ["Udayāditya", "Paramāra", "Paramāras", "Udayeśvara", "Udayapura", "Udaypur", "Vidisha", "Bhilsa", "Malwa", "Mālava", "Dhārā", "Bhoja", "Śiva", "Viṣṇu", "Brahmā", "Sūrya", "Pārvatī", "Gaṇeśa", "Bhūmija", "Nāgara", "Khajuraho", "Deccan", "Caulukya", "Kalacuri", "Candella", "Candellas", "Paramāra-era", "Samarāṅgaṇasūtradhāra", "Aparājitapṛcchā", "Kāmikāgama", "Śaiva", "Siddhānta", "Nīlakaṇṭheśvara", "Udayeśvaradeva", "Kramrisch", "Pande", "Hardy", "Ganguly", "Patil", "Deva", "Adhikari", "Sharma", "Tiwari", "Cunningham", "Beglar", "Fergusson", "Singh", "Gupte", "Indian", "India", "Central", "Nimar", "Onkar", "Mandhata", "Nemawar", "Rajpurohit", "Saraswati", "Krishna", "Nirṛti"]
TIWARI_FULL_NAME = False      # named in full in Chapter 1; here "Tiwari"
GAZ_MODERN_ONLY = False       # the Gazetteer may carry dynastic claims here, phrased as its own
GAZ_MAX_SHARE = 0.40          # user 2026-10-14
AUTHORED = True
HOUSE_VOICE = True
CONSOLIDATE_NOTES = True

CONFLICTS = {}

CHAPTER_BRIEF = """Chapter 5 of the Udaypur history: the Udayeśvara temple read as historical evidence, not an inventory. In-session drafting from ch05_plan_v1.md; no API calls. Canon: style/style_sheet.md §13 (U1, R1–R4, D1). Architectural and art-historical sources (Pande, Hardy, Kramrisch, Adhikari, Sharma, Deva) are secondary scholarship; interpretive claims are attributed. The Samarāṅgaṇasūtradhāra is a norm attributed to the treatise, never a record of this temple, and SAMAR items are never quoted. The two Pande OCR copies are one book (only `The Udayesvara Temple - Anupa Pande.md` is cited). Inscriptions as texts belong to Chapter 6, the wider built heritage and the hill to Chapter 7, dates and dynasty to Chapter 4, the damage's authors to Chapter 10. Temple Economics is excluded."""


def extra_rules(text, P, smap):
    import re
    fails = []
    secs = re.split(r"(?m)^(?=## 5\.\d+)", text)
    for s in secs:
        m = re.match(r"## (5\.\d+)", s)
        sec = m.group(1) if m else "chapter"
        body = re.sub(r"\{\{note:.*?\}\}", lambda n: n.group(0), s, flags=re.S)
        for sent in re.split(r"(?<=[.!?”\]])\s+(?=[A-Z“{])", body):
            ids = re.findall(r"C0\d-[A-Z0-9-]+", sent)
            if any("SAMAR" in i for i in ids) and re.search(r"[“\"]", sent):
                fails.append({"sec": sec, "rule": "SAMAR never quoted", "detail": sent.strip()[:140]})
            plain = re.sub(r"\[[^\]]*\]", "", sent)
            if re.search(r"\b1059\b", plain) and not re.search(r"read|reading|caption|pedigree|faulty|late record", plain):
                fails.append({"sec": sec, "rule": "canon R3", "detail": "1059 without 'reading': " + plain.strip()[:120]})
            if re.search(r"\bKarṇa\b", plain) and not re.search(r"Kalacuri|Caulukya|Gujarat|unspecified", plain):
                fails.append({"sec": sec, "rule": "canon R2", "detail": plain.strip()[:120]})
            if re.search(r"Temple Economics|TEMPLE-ECON", sent):
                fails.append({"sec": sec, "rule": "excluded source", "detail": plain.strip()[:120]})
    return fails


KB_IN = PACK
KB_MAX_NEW = 0
KB_TOPIC = ""
KB_SUBS = ""
KB_SECTIONS = SECTIONS
KB_GAP = {}
KB_CONTRA = {}
SETTLED = []
REPORT_OUTLINE_NOTES = ""
