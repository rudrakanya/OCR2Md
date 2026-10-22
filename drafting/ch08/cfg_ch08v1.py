"""Chapter 8, draft v1 (21 Oct 2026; in-session, no API) — configuration for drafting/_pipe.
Set UDAY_CFG to this file. Sections follow editorial/Udaypur_Book_Contents.md (14 units, one section each)."""
from pathlib import Path

CH = 8
VERSION = "v1"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch08"))
SECTIONS = [f"8.{i}" for i in range(1, 15)]
OUTLINE = D / "ch08_plan_v1.md"
PACK = D / "evidence_pack_v1.json"
LOG = D / "api_log_v1"
OUT = D / "ch08_draft_v1.md"
TITLE = "Religion and the Material Life of Udaypur: Ritual, Agriculture, Trade and Craft"
DOCX_NAME = "Chapter 8 - Religion and the Material Life of Udaypur - Draft v1.docx"
SUBTITLE = "Draft v1 · October 2026"
WMIN, WMAX, TOTAL_TARGET = 0, 10**9, 0   # user 17 Oct: no word targets; each unit as long as its evidence carries
NO_LENGTH = True
BUDGET, RESERVE = 0.00, 0.00   # no API calls (user rule); in-session drafting and verification
BASELINE = None
BASELINE_MAP = {}
VOICE_SRC = None
OPEN_IN = ("Chapter 7 ended on Vikrama's tank, water given for merit, handing the gifts to Chapter 8. Open on Dhāmadeva's four biswa, given taking water in hand, in 1229.")
CLOSE_OUT = ("Chapter 9 takes up communities, languages, festivals and oral traditions. End on the living temple and its fair, leading into the people of Udaypur.")
ALLOW_EXTRA = ["Udayāditya", "Paramāra", "Paramāras", "Udayeśvara", "Udayapura", "Udaypur", "Vidisha", "Bhilsa", "Malwa", "Mālava", "Dhārā", "Bhoja", "Śiva", "Viṣṇu", "Brahmā", "Sūrya", "Pārvatī", "Gaṇeśa", "Bhūmija", "Nāgara", "Khajuraho", "Deccan", "Caulukya", "Kalacuri", "Candella", "Candellas", "Paramāra-era", "Samarāṅgaṇasūtradhāra", "Aparājitapṛcchā", "Kāmikāgama", "Śaiva", "Siddhānta", "Nīlakaṇṭheśvara", "Udayeśvaradeva", "Kramrisch", "Pande", "Hardy", "Ganguly", "Patil", "Deva", "Adhikari", "Sharma", "Tiwari", "Cunningham", "Beglar", "Fergusson", "Singh", "Gupte", "Indian", "India", "Central", "Nimar", "Onkar", "Mandhata", "Nemawar", "Rajpurohit", "Saraswati", "Krishna", "Nirṛti", "Bühler", "Kielhorn", "Trivedi", "Verma", "Mahipāla", "Śṛṅgavāsa", "Devapāla", "Naravarman", "Kumārapāla", "Rājyapāla", "Lūṇapasāka", "Ajayapāla", "Amērā", "Vidisha", "Dhārā", "Ujjain", "Un", "Ūn", "Persian", "Sanskrit", "Prakrit", "Nāgarī", "Tughluq", "Gwalior", "Garde", "Chittapa", "Bhojaśālā", "Vaidya", "Ray", "Sastri", "Kharahi", "Mount", "Muñja", "Sindhurāja", "Vairisiṃha", "Merutuṅga", "Gāṅgeya", "Abu", "Padmagupta", "Cedi", "Chedi", "Nagpur", "Dhār", "Pāṇini", "Arjunavarman", "Pārijātamañjarī", "Kāmasūtra", "Narasiṃha", "Somēśvara", "Nāmamālikā", "Sarasvatīkaṇṭhābharaṇa", "Prabandhacintāmaṇi", "Bhāillasvāmin", "Navasāhasāṅkacarita", "Subhāṣitaratnasaṃdoha", "Jayavarman", "Al-Bīrūnī", "Bīrūnī", "Anahilapāṭaka", "Indian Antiquary", "Antiquary", "Beglar", "INTACH", "Udaysagar", "Udayasamudra", "Bhujariya", "Barakhambi", "Pisanhari", "Pisanhārī", "Bijamandal", "Shahi", "Masjid", "Tughluq", "Jahāngīr", "Shāh Jahān", "Ghiyās", "Sher Khan", "Mandu", "Chanderi", "Tīrthaṅkara", "Muslim", "Śeṣaśāyī", "Lakulīśa", "Ravan Tol", "Naṭarāja", "Vikrama", "Amērā", "Dhāmadeva", "Raṇipadra", "Prāyaścittasamuccaya", "Sīyaka", "Lambakarṇa", "Viśveśvara", "Śambhu", "Pūrvagrāma", "Rāḍha", "Nāṭana", "Caṇḍikāśrama", "Āūrakācārya", "Siddheśvara", "Merutuṅga", "Mahākāla", "Pārśvanātha", "Tīrthaṅkaras", "Kāpālika", "Siddhāntasaṅgraha", "Siddhāntins", "Śivatattvaratnakalikā", "Kālānana", "Māheśvaras", "Kālāmukhas", "Śivajñānabodham", "Kāyāvarohaṇa", "Karvan", "Jāvala", "Ekalingji", "Hathuṇḍī", "Rajputs", "Vasantotsava", "Diwālī", "Pavitraka", "Cāmuṇḍarāja", "Maṇḍaleśa", "Chau-ju-kua", "Gāṅgeyadeva", "Pālhaṇadeva", "Dhārāvarṣa", "Memmaka", "Bṛhatsaṃhitā", "Mahānirvāṇa", "Cāhamāna", "Cāhamānas", "Naḍḍula", "Śākambharī", "Santosh", "Kumar", "Ajayapāla", "Lūṇapasāka", "Rājyapāla", "Umaratha", "Rayakuka", "Devapāla", "Vasantapāla", "Udaleśvara", "Vaidyanātha", "Bhiraṅgāvalī", "Kumārapāla", "Anahilapāṭaka", "Limbārvā", "Carcikā", "Tattvaprakāśa", "Lakulīśa", "Pāśupata", "Pāśupatas", "Mattamayūra", "Śivarātri", "Sendhavadeva", "Arthuna", "Śrīmāla", "Rāma", "Lakṣmaṇa", "Sītā", "Ghaḍiyālan-kā-makān", "Mahāvīra", "Pārśvanātha", "Ādinātha", "Jahāngīr", "Ghiyāth", "Ghiyāth-ud-dīn", "Mālwa", "Khaljī", "Khalji", "Sultan", "Sultans", "Delhi", "Muhammad", "Arabic"]
TIWARI_FULL_NAME = False      # named in full in Chapter 1; here "Tiwari"
GAZ_MODERN_ONLY = False       # the Gazetteer may carry dynastic claims here, phrased as its own
GAZ_MAX_SHARE = 0.40          # user 2026-10-14
AUTHORED = True
HOUSE_VOICE = True
CONSOLIDATE_NOTES = True

CONFLICTS = {}

CHAPTER_BRIEF = """Chapter 8 of the Udaypur history: religion and material life, evidence-light. Three dated gifts at Udaypur (1163, Ganguly only; early 1170s; 1229); everything wider is the regional or normative pattern, labelled as such. Temple Economics is contextual only, never evidence for Udaypur. Canon U1, R1-R4, D1. Tiers: CII for grants; Gazetteer tier 7; Tiwari testimony. No invented farmers, traders or artisans. Boundaries: epigraphy Ch 6; building Ch 5; water Ch 2/7; social life Ch 9."""


def extra_rules(text, P, smap):
    import re
    fails = []
    secs = re.split(r"(?m)^(?=## 8\.\d+)", text)
    for s in secs:
        m = re.match(r"## (8\.\d+)", s)
        sec = m.group(1) if m else "chapter"
        for sent in re.split(r"(?<=[.!?”\]}])\s+(?=[A-Z“{])", s):
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
            if re.search(r"mahādvādaśaka|Bhṛṅgārikā", plain) and not re.search(r"\b11[67]\d\b|\b12[23]\d\b|record", plain):
                fails.append({"sec": sec, "rule": "canon R4 (term not dated to its record)", "detail": plain.strip()[:120]})
            if any("TEMPLE-ECON" in i for i in ids) and re.search(r"Udaypur|Udayeśvara|Udayapura", plain):
                fails.append({"sec": sec, "rule": "Temple Economics tied to Udaypur", "detail": plain.strip()[:140]})
            if any("TEMPLE-ECON" in i for i in ids) and not re.search(r"south|South|Chola|Tamil|elsewhere|compar|general|Nathdwara|Varanasi|Jwalamukhi|Tirumal|India|modern|today", plain):
                fails.append({"sec": sec, "rule": "Temple Economics not framed as contextual", "detail": plain.strip()[:140]})
            if re.search(r"\b(masons|builders|quarrymen|labourers|workmen|craftsmen|farmers|peasants|cultivators|traders|merchants|artisans|weavers|potters)\b", unq, re.I) and not ids:
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
