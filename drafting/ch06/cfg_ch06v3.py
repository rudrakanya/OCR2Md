"""Chapter 6, draft v3 (22 Oct 2026; every unit deepened from its own evidence and the chapter smoothed; in-session, no API) — configuration for drafting/_pipe.
Set UDAY_CFG to this file. Sections follow editorial/Udaypur_Book_Contents.md (22 units, one section each)."""
from pathlib import Path

CH = 6
VERSION = "v3"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch06"))
SECTIONS = [f"6.{i}" for i in range(1, 23)]
OUTLINE = D / "ch06_plan_v3.md"
PACK = D / "evidence_pack_v3.json"
LOG = D / "api_log_v3"
OUT = D / "ch06_draft_v3.md"
TITLE = "Inscriptions and Intellectual Life: Epigraphy, Languages and Literary Culture"
DOCX_NAME = "Chapter 6 - Inscriptions and Intellectual Life - Draft v3.docx"
SUBTITLE = "Draft v3 · October 2026"
WMIN, WMAX, TOTAL_TARGET = 0, 10**9, 0   # user 17 Oct: no word targets; each unit as long as its evidence carries
NO_LENGTH = True
BUDGET, RESERVE = 0.00, 0.00   # no API calls (user rule); in-session drafting and verification
BASELINE = None
BASELINE_MAP = {}
VOICE_SRC = None
OPEN_IN = ("Chapter 5 ended on the temple's own inscribed words: the flag record naming it Udayeśvaradeva and the praśasti invoking Śiva, Pārvatī and Gaṇeśa. Open on the six lines at the east door.")
CLOSE_OUT = ("Chapter 7 describes the wider built heritage. End on what the stones cannot say, handing the dated mosques and the hill to Chapter 7.")
ALLOW_EXTRA = ["Udayāditya", "Paramāra", "Paramāras", "Udayeśvara", "Udayapura", "Udaypur", "Vidisha", "Bhilsa", "Malwa", "Mālava", "Dhārā", "Bhoja", "Śiva", "Viṣṇu", "Brahmā", "Sūrya", "Pārvatī", "Gaṇeśa", "Bhūmija", "Nāgara", "Khajuraho", "Deccan", "Caulukya", "Kalacuri", "Candella", "Candellas", "Paramāra-era", "Samarāṅgaṇasūtradhāra", "Aparājitapṛcchā", "Kāmikāgama", "Śaiva", "Siddhānta", "Nīlakaṇṭheśvara", "Udayeśvaradeva", "Kramrisch", "Pande", "Hardy", "Ganguly", "Patil", "Deva", "Adhikari", "Sharma", "Tiwari", "Cunningham", "Beglar", "Fergusson", "Singh", "Gupte", "Indian", "India", "Central", "Nimar", "Onkar", "Mandhata", "Nemawar", "Rajpurohit", "Saraswati", "Krishna", "Nirṛti", "Bühler", "Kielhorn", "Trivedi", "Verma", "Mahipāla", "Śṛṅgavāsa", "Devapāla", "Naravarman", "Kumārapāla", "Rājyapāla", "Lūṇapasāka", "Ajayapāla", "Amērā", "Vidisha", "Dhārā", "Ujjain", "Un", "Ūn", "Persian", "Sanskrit", "Prakrit", "Nāgarī", "Tughluq", "Gwalior", "Garde", "Chittapa", "Bhojaśālā", "Vaidya", "Ray", "Sastri", "Kharahi", "Mount", "Muñja", "Sindhurāja", "Vairisiṃha", "Merutuṅga", "Gāṅgeya", "Abu", "Padmagupta", "Cedi", "Chedi", "Nagpur", "Dhār", "Pāṇini", "Arjunavarman", "Pārijātamañjarī", "Kāmasūtra", "Narasiṃha", "Somēśvara", "Nāmamālikā", "Sarasvatīkaṇṭhābharaṇa", "Prabandhacintāmaṇi", "Bhāillasvāmin", "Navasāhasāṅkacarita", "Subhāṣitaratnasaṃdoha", "Jayavarman", "Al-Bīrūnī", "Bīrūnī", "Anahilapāṭaka", "Indian Antiquary", "Antiquary", "Saarthak", "Sircar", "Bandhu", "Mahākāla", "Sastri", "Pāñcajanya", "Murāri"]
TIWARI_FULL_NAME = False      # named in full in Chapter 1; here "Tiwari"
GAZ_MODERN_ONLY = False       # the Gazetteer may carry dynastic claims here, phrased as its own
GAZ_MAX_SHARE = 0.40          # user 2026-10-14
AUTHORED = True
HOUSE_VOICE = True
CONSOLIDATE_NOTES = True

CONFLICTS = {}

CHAPTER_BRIEF = """Chapter 6 of the Udaypur history: the inscriptions as evidence of intellectual and literary life, not a catalogue. In-session drafting from ch06_plan_v3.md; no API calls. Canon: style/style_sheet.md §13 (U1, R1–R4, D1). CII VII.2 (Trivedi) is the primary authority; Ganguly and Verma (via Tiwari, testimony) are attributed. The staged Bühler and Cunningham editions are uncorrected and nothing rests on them (RR-1, RR-12). The V.S. 1116 records stay separate and labelled. 1170s porch terms belong to the twelfth century; the twelfth-century records are Caulukya overlordship (U1). Architecture is Ch 5, endowments' economics Ch 8, the political narrative Ch 4 and Ch 10."""


def extra_rules(text, P, smap):
    import re
    fails = []
    secs = re.split(r"(?m)^(?=## 6\.\d+)", text)
    for s in secs:
        m = re.match(r"## (6\.\d+)", s)
        sec = m.group(1) if m else "chapter"
        for sent in re.split(r"(?<=[.!?”\]])\s+(?=[A-Z“{])", s):
            ids = re.findall(r"C\d\d-[A-Z0-9-]+", sent)
            if any("SAMAR" in i for i in ids) and re.search(r"[“\"]", sent):
                fails.append({"sec": sec, "rule": "SAMAR never quoted", "detail": sent.strip()[:140]})
            plain = re.sub(r"\[[^\]]*\]", "", sent)
            if re.search(r"\b1059\b", plain) and not re.search(r"read|reading|survey|claim|gives|caption|faulty|late|pedigree|1116", plain):
                fails.append({"sec": sec, "rule": "canon R3", "detail": plain.strip()[:120]})
            if re.search(r"\bKarṇa\b|\bKarna\b", plain) and not re.search(r"Kalacuri|Caulukya|Gujarat|Chedi|Cedi|unspecified|which Karṇa", plain):
                fails.append({"sec": sec, "rule": "canon R2", "detail": plain.strip()[:120]})
            if re.search(r"Lūṇapasāka|Rājyapāla", plain) and not re.search(r"Caulukya|Kumārapāla|Gujarat|Ajayapāla", plain):
                fails.append({"sec": sec, "rule": "canon U1", "detail": plain.strip()[:120]})
            if sec not in ("6.18", "chapter") and re.search(r"mahādvādaśaka|Mahādvādaśaka|Bhṛṅgārikā|Bhāillasvāmi-", re.sub(r"\{\{note:.*?\}\}", "", plain, flags=re.S)):
                fails.append({"sec": sec, "rule": "canon R4", "detail": plain.strip()[:120]})
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
