"""Chapter 9, draft v1 (21 Oct 2026; in-session, no API) — configuration for drafting/_pipe.
Set UDAY_CFG to this file. Sections follow editorial/Udaypur_Book_Contents.md (9 units, one section each)."""
from pathlib import Path

CH = 9
VERSION = "v1"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch09"))
SECTIONS = [f"9.{i}" for i in range(1, 10)]
OUTLINE = D / "ch09_plan_v1.md"
PACK = D / "evidence_pack_v1.json"
LOG = D / "api_log_v1"
OUT = D / "ch09_draft_v1.md"
TITLE = "Society and Cultural Life: Communities, Languages, Festivals and Oral Traditions"
DOCX_NAME = "Chapter 9 - Society and Cultural Life - Draft v1.docx"
SUBTITLE = "Draft v1 · October 2026"
WMIN, WMAX, TOTAL_TARGET = 0, 10**9, 0   # user 17 Oct: no word targets; each unit as long as its evidence carries
NO_LENGTH = True
BUDGET, RESERVE = 0.00, 0.00   # no API calls (user rule); in-session drafting and verification
BASELINE = None
BASELINE_MAP = {}
VOICE_SRC = None
OPEN_IN = ("Chapter 8 ended on the temple still visited by the people of Udaypur. Open on a lane of neighbours beside the temple, described by community, never by residents' names.")
CLOSE_OUT = ("Chapter 10 tests the town's memory of its later centuries against the record. End on the remembered deserted market of Daulatpur, as memory only.")
ALLOW_EXTRA = ["Udayāditya", "Paramāra", "Paramāras", "Udayeśvara", "Udayapura", "Udaypur", "Vidisha", "Bhilsa", "Malwa", "Mālava", "Dhārā", "Bhoja", "Śiva", "Viṣṇu", "Brahmā", "Sūrya", "Pārvatī", "Gaṇeśa", "Bhūmija", "Nāgara", "Khajuraho", "Deccan", "Caulukya", "Kalacuri", "Candella", "Candellas", "Paramāra-era", "Samarāṅgaṇasūtradhāra", "Aparājitapṛcchā", "Kāmikāgama", "Śaiva", "Siddhānta", "Nīlakaṇṭheśvara", "Udayeśvaradeva", "Kramrisch", "Pande", "Hardy", "Ganguly", "Patil", "Deva", "Adhikari", "Sharma", "Tiwari", "Cunningham", "Beglar", "Fergusson", "Singh", "Gupte", "Indian", "India", "Central", "Nimar", "Onkar", "Mandhata", "Nemawar", "Rajpurohit", "Saraswati", "Krishna", "Nirṛti", "Bühler", "Kielhorn", "Trivedi", "Verma", "Mahipāla", "Śṛṅgavāsa", "Devapāla", "Naravarman", "Kumārapāla", "Rājyapāla", "Lūṇapasāka", "Ajayapāla", "Amērā", "Vidisha", "Dhārā", "Ujjain", "Un", "Ūn", "Persian", "Sanskrit", "Prakrit", "Nāgarī", "Tughluq", "Gwalior", "Garde", "Chittapa", "Bhojaśālā", "Vaidya", "Ray", "Sastri", "Kharahi", "Mount", "Muñja", "Sindhurāja", "Vairisiṃha", "Merutuṅga", "Gāṅgeya", "Abu", "Padmagupta", "Cedi", "Chedi", "Nagpur", "Dhār", "Pāṇini", "Arjunavarman", "Pārijātamañjarī", "Kāmasūtra", "Narasiṃha", "Somēśvara", "Nāmamālikā", "Sarasvatīkaṇṭhābharaṇa", "Prabandhacintāmaṇi", "Bhāillasvāmin", "Navasāhasāṅkacarita", "Subhāṣitaratnasaṃdoha", "Jayavarman", "Al-Bīrūnī", "Bīrūnī", "Anahilapāṭaka", "Indian Antiquary", "Antiquary", "Beglar", "INTACH", "Udaysagar", "Udayasamudra", "Bhujariya", "Barakhambi", "Pisanhari", "Pisanhārī", "Bijamandal", "Shahi", "Masjid", "Tughluq", "Jahāngīr", "Shāh Jahān", "Ghiyās", "Sher Khan", "Mandu", "Chanderi", "Tīrthaṅkara", "Muslim", "Śeṣaśāyī", "Lakulīśa", "Ravan Tol", "Naṭarāja", "Vikrama", "Amērā", "Dhāmadeva", "Siṃhāsanadvātriṃśikā", "Vikramāditya", "Telangana", "Lat Masjid", "Benji", "Maada", "Bedni", "Berni", "Harijan", "Gonds", "Bhringraj", "Bhringrajpur", "Daulatpur", "Gabbar", "Ramgarh", "Gyasuddin", "Sundarkand", "Jayasiṃha", "Vālabha", "Sāmavedins", "Chāndogya", "Lāṭa", "Madhyadeśa", "Magadha", "Tailakas", "Bundeli", "Malwi", "Bundelkhandi", "Suvi", "Nāgarī", "Bagdis", "Bagdi", "Sot", "Raisen", "Raṇipadra", "Prāyaścittasamuccaya", "Sīyaka", "Lambakarṇa", "Viśveśvara", "Śambhu", "Pūrvagrāma", "Rāḍha", "Nāṭana", "Caṇḍikāśrama", "Āūrakācārya", "Siddheśvara", "Merutuṅga", "Mahākāla", "Pārśvanātha", "Tīrthaṅkaras", "Kāpālika", "Siddhāntasaṅgraha", "Siddhāntins", "Śivatattvaratnakalikā", "Kālānana", "Māheśvaras", "Kālāmukhas", "Śivajñānabodham", "Kāyāvarohaṇa", "Karvan", "Jāvala", "Ekalingji", "Hathuṇḍī", "Rajputs", "Vasantotsava", "Diwālī", "Pavitraka", "Cāmuṇḍarāja", "Maṇḍaleśa", "Chau-ju-kua", "Gāṅgeyadeva", "Pālhaṇadeva", "Dhārāvarṣa", "Memmaka", "Bṛhatsaṃhitā", "Mahānirvāṇa", "Cāhamāna", "Cāhamānas", "Naḍḍula", "Śākambharī", "Santosh", "Kumar", "Ajayapāla", "Lūṇapasāka", "Rājyapāla", "Umaratha", "Rayakuka", "Devapāla", "Vasantapāla", "Udaleśvara", "Vaidyanātha", "Bhiraṅgāvalī", "Kumārapāla", "Anahilapāṭaka", "Limbārvā", "Carcikā", "Tattvaprakāśa", "Lakulīśa", "Pāśupata", "Pāśupatas", "Mattamayūra", "Śivarātri", "Sendhavadeva", "Arthuna", "Śrīmāla", "Rāma", "Lakṣmaṇa", "Sītā", "Ghaḍiyālan-kā-makān", "Mahāvīra", "Pārśvanātha", "Ādinātha", "Jahāngīr", "Ghiyāth", "Ghiyāth-ud-dīn", "Mālwa", "Khaljī", "Khalji", "Sultan", "Sultans", "Delhi", "Muhammad", "Arabic"]
TIWARI_FULL_NAME = False      # named in full in Chapter 1; here "Tiwari"
GAZ_MODERN_ONLY = False       # the Gazetteer may carry dynastic claims here, phrased as its own
GAZ_MAX_SHARE = 0.40          # user 2026-10-14
AUTHORED = True
HOUSE_VOICE = True
CONSOLIDATE_NOTES = True

CONFLICTS = {}

CHAPTER_BRIEF = """Chapter 9: society and cultural life, evidence-light. Communities and language are district-level or one writer's testimony; the centre is memory. Oral tradition told as memory, never as proof. No residents named. Canon U1, R1-R4, D1. Tiers: Tiwari testimony (no counts); Gazetteer and surveys tier 7. Boundaries: ritual Ch 8; modern institutions Ch 11-12; future Afterword."""


def extra_rules(text, P, smap):
    import re
    fails = []
    secs = re.split(r"(?m)^(?=## 9\.\d+)", text)
    for s in secs:
        m = re.match(r"## (9\.\d+)", s)
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
            if re.search(r"Raja Miyan|Hamid|Bashir|Ramesh|Rajkumar|Mallu|Khan Sahib", plain):
                fails.append({"sec": sec, "rule": "living resident named", "detail": plain.strip()[:140]})
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
