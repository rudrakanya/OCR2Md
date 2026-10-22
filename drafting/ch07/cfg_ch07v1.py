"""Chapter 7, draft v1 (21 Oct 2026; in-session, no API) — configuration for drafting/_pipe.
Set UDAY_CFG to this file. Sections follow editorial/Udaypur_Book_Contents.md (25 units, one section each)."""
from pathlib import Path

CH = 7
VERSION = "v1"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch07"))
SECTIONS = [f"7.{i}" for i in range(1, 26)]
OUTLINE = D / "ch07_plan_v1.md"
PACK = D / "evidence_pack_v1.json"
LOG = D / "api_log_v1"
OUT = D / "ch07_draft_v1.md"
TITLE = "The Wider Built Heritage of Udaypur: Fortifications, Shrines, Mosques and Water Structures"
DOCX_NAME = "Chapter 7 - The Wider Built Heritage of Udaypur - Draft v1.docx"
SUBTITLE = "Draft v1 · October 2026"
WMIN, WMAX, TOTAL_TARGET = 0, 10**9, 0   # user 17 Oct: no word targets; each unit as long as its evidence carries
NO_LENGTH = True
BUDGET, RESERVE = 0.00, 0.00   # no API calls (user rule); in-session drafting and verification
BASELINE = None
BASELINE_MAP = {}
VOICE_SRC = None
OPEN_IN = ("Chapter 6 ended on what the stones cannot say, handing the walls, shrines, mosques and water works to Chapter 7. Open on a wall without a name, counted in the surveys.")
CLOSE_OUT = ("Chapter 8 takes up religion and material life, beginning with gifts. End on the water given for merit, leading into the gifts of Chapter 8.")
ALLOW_EXTRA = ["Udayāditya", "Paramāra", "Paramāras", "Udayeśvara", "Udayapura", "Udaypur", "Vidisha", "Bhilsa", "Malwa", "Mālava", "Dhārā", "Bhoja", "Śiva", "Viṣṇu", "Brahmā", "Sūrya", "Pārvatī", "Gaṇeśa", "Bhūmija", "Nāgara", "Khajuraho", "Deccan", "Caulukya", "Kalacuri", "Candella", "Candellas", "Paramāra-era", "Samarāṅgaṇasūtradhāra", "Aparājitapṛcchā", "Kāmikāgama", "Śaiva", "Siddhānta", "Nīlakaṇṭheśvara", "Udayeśvaradeva", "Kramrisch", "Pande", "Hardy", "Ganguly", "Patil", "Deva", "Adhikari", "Sharma", "Tiwari", "Cunningham", "Beglar", "Fergusson", "Singh", "Gupte", "Indian", "India", "Central", "Nimar", "Onkar", "Mandhata", "Nemawar", "Rajpurohit", "Saraswati", "Krishna", "Nirṛti", "Bühler", "Kielhorn", "Trivedi", "Verma", "Mahipāla", "Śṛṅgavāsa", "Devapāla", "Naravarman", "Kumārapāla", "Rājyapāla", "Lūṇapasāka", "Ajayapāla", "Amērā", "Vidisha", "Dhārā", "Ujjain", "Un", "Ūn", "Persian", "Sanskrit", "Prakrit", "Nāgarī", "Tughluq", "Gwalior", "Garde", "Chittapa", "Bhojaśālā", "Vaidya", "Ray", "Sastri", "Kharahi", "Mount", "Muñja", "Sindhurāja", "Vairisiṃha", "Merutuṅga", "Gāṅgeya", "Abu", "Padmagupta", "Cedi", "Chedi", "Nagpur", "Dhār", "Pāṇini", "Arjunavarman", "Pārijātamañjarī", "Kāmasūtra", "Narasiṃha", "Somēśvara", "Nāmamālikā", "Sarasvatīkaṇṭhābharaṇa", "Prabandhacintāmaṇi", "Bhāillasvāmin", "Navasāhasāṅkacarita", "Subhāṣitaratnasaṃdoha", "Jayavarman", "Al-Bīrūnī", "Bīrūnī", "Anahilapāṭaka", "Indian Antiquary", "Antiquary", "Beglar", "INTACH", "Udaysagar", "Udayasamudra", "Bhujariya", "Barakhambi", "Pisanhari", "Pisanhārī", "Bijamandal", "Shahi", "Masjid", "Tughluq", "Jahāngīr", "Shāh Jahān", "Ghiyās", "Sher Khan", "Mandu", "Chanderi", "Tīrthaṅkara", "Muslim", "Śeṣaśāyī", "Lakulīśa", "Ravan Tol", "Naṭarāja", "Vikrama", "Amērā", "Rāma", "Lakṣmaṇa", "Sītā", "Ghaḍiyālan-kā-makān", "Mahāvīra", "Pārśvanātha", "Ādinātha", "Jahāngīr", "Ghiyāth", "Ghiyāth-ud-dīn", "Mālwa", "Khaljī", "Khalji", "Sultan", "Sultans", "Delhi", "Muhammad", "Arabic"]
TIWARI_FULL_NAME = False      # named in full in Chapter 1; here "Tiwari"
GAZ_MODERN_ONLY = False       # the Gazetteer may carry dynastic claims here, phrased as its own
GAZ_MAX_SHARE = 0.40          # user 2026-10-14
AUTHORED = True
HOUSE_VOICE = True
CONSOLIDATE_NOTES = True

CONFLICTS = {}

CHAPTER_BRIEF = """Chapter 7 of the Udaypur history: the built heritage beyond the great temple, used as evidence for a history (who held the hill, the walled town, worship after the temple, several faiths on one ground, water across the ages), not as a gazetteer. In-session drafting from ch07_plan_v1.md; no API calls. Canon: style/style_sheet.md §13 (U1, R1–R4, D1). Tiers: CII for inscriptions; Gazetteer and INTACH/GEOHER as tier-7 survey, their statements phrased as theirs; Tiwari as testimony. The staged Beglar/Cunningham editions are uncorrected and not used directly; where Pande or the survey quotes them, the quotation is attributed. No anonymous builders or labour from passive mentions. 'Mohammedan' only inside quotations. Boundaries: the great temple Ch 5; landscape water and geology Ch 2; the later regimes' politics Ch 10; inscriptions as texts Ch 6."""


def extra_rules(text, P, smap):
    import re
    fails = []
    secs = re.split(r"(?m)^(?=## 7\.\d+)", text)
    for s in secs:
        m = re.match(r"## (7\.\d+)", s)
        sec = m.group(1) if m else "chapter"
        for sent in re.split(r"(?<=[.!?”\]])\s+(?=[A-Z“{])", s):
            ids = re.findall(r"C\d\d-[A-Z0-9-]+", sent)
            if any("SAMAR" in i for i in ids) and re.search(r"[“\"]", sent):
                fails.append({"sec": sec, "rule": "SAMAR never quoted", "detail": sent.strip()[:140]})
            plain = re.sub(r"\[[^\]]*\]", "", sent)
            unq = re.sub(r"“[^”]*”", "", plain)
            if re.search(r"\b1059\b", plain) and not re.search(r"read|reading|survey|claim|gives|caption|faulty|late|pedigree|1116|dates", plain):
                fails.append({"sec": sec, "rule": "canon R3", "detail": plain.strip()[:120]})
            if re.search(r"\bKarṇa\b", plain) and not re.search(r"Kalacuri|Caulukya|Gujarat|Chedi|Cedi|unspecified", plain):
                fails.append({"sec": sec, "rule": "canon R2", "detail": plain.strip()[:120]})
            if re.search(r"Mohammedan|Muhammadan|Mahomedan", unq):
                fails.append({"sec": sec, "rule": "period term outside quotation", "detail": plain.strip()[:120]})
            if re.search(r"mahādvādaśaka|Bhṛṅgārikā", re.sub(r"\{\{note:.*?\}\}", "", plain, flags=re.S)):
                fails.append({"sec": sec, "rule": "canon R4", "detail": plain.strip()[:120]})
            if re.search(r"\b(masons|builders|quarrymen|labourers|workmen|craftsmen)\b", unq) and not ids:
                fails.append({"sec": sec, "rule": "anonymous labour check", "detail": plain.strip()[:120]})
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
