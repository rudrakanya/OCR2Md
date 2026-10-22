"""Chapter 10, draft v1 (21 Oct 2026; in-session, no API) — configuration for drafting/_pipe.
Set UDAY_CFG to this file. Sections follow editorial/Udaypur_Book_Contents.md (12 units, one section each)."""
from pathlib import Path

CH = 10
VERSION = "v1"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch10"))
SECTIONS = [f"10.{i}" for i in range(1, 13)]
OUTLINE = D / "ch10_plan_v1.md"
PACK = D / "evidence_pack_v1.json"
LOG = D / "api_log_v1"
OUT = D / "ch10_draft_v1.md"
TITLE = "Political Change and Economic Decline: Udaypur under Successive Regimes"
DOCX_NAME = "Chapter 10 - Political Change and Economic Decline - Draft v1.docx"
SUBTITLE = "Political Change and Economic Decline: Udaypur under Successive Regimes"
WMIN, WMAX, TOTAL_TARGET = 0, 10**9, 0   # user 17 Oct: no word targets; each unit as long as its evidence carries
NO_LENGTH = True
BUDGET, RESERVE = 0.00, 0.00   # no API calls (user rule); in-session drafting and verification
BASELINE = None
BASELINE_MAP = {}
VOICE_SRC = None
OPEN_IN = ("Chapter 9 ended on the town's memory of its later centuries, to be tested against the record. Open on the V.S. 1220 stone naming the Caulukya Kumārapāla at Udaypur.")
CLOSE_OUT = ("Chapter 11 takes up archaeology and heritage administration. End on the Gazetteer's sentence as an official's description, leading into the officials and surveyors of Chapter 11.")
ALLOW_EXTRA = ['Nēmaka', 'Research', 'Register', 'HELD', 'RR', 'Candrāvatī', 'Gurjaras', 'Gujarat', 'Chapters', 'Chapter', 'Udayāditya', 'Paramāra', 'Paramāras', 'Udayeśvara', 'Udayapura', 'Udaypur', 'Vidisha', 'Bhilsa', 'Malwa', 'Mālava', 'Dhārā', 'Bhoja', 'Śiva', 'Viṣṇu', 'Brahmā', 'Sūrya', 'Pārvatī', 'Gaṇeśa', 'Bhūmija', 'Nāgara', 'Khajuraho', 'Deccan', 'Caulukya', 'Kalacuri', 'Candella', 'Candellas', 'Paramāra-era', 'Samarāṅgaṇasūtradhāra', 'Aparājitapṛcchā', 'Kāmikāgama', 'Śaiva', 'Siddhānta', 'Nīlakaṇṭheśvara', 'Udayeśvaradeva', 'Kramrisch', 'Pande', 'Hardy', 'Ganguly', 'Patil', 'Deva', 'Adhikari', 'Sharma', 'Tiwari', 'Cunningham', 'Beglar', 'Fergusson', 'Singh', 'Gupte', 'Indian', 'India', 'Central', 'Nimar', 'Onkar', 'Mandhata', 'Nemawar', 'Rajpurohit', 'Saraswati', 'Krishna', 'Nirṛti', 'Bühler', 'Kielhorn', 'Trivedi', 'Verma', 'Mahipāla', 'Śṛṅgavāsa', 'Devapāla', 'Naravarman', 'Kumārapāla', 'Rājyapāla', 'Lūṇapasāka', 'Ajayapāla', 'Amērā', 'Ujjain', 'Un', 'Ūn', 'Persian', 'Sanskrit', 'Prakrit', 'Nāgarī', 'Tughluq', 'Gwalior', 'Garde', 'Chittapa', 'Bhojaśālā', 'Vaidya', 'Ray', 'Sastri', 'Kharahi', 'Mount', 'Muñja', 'Sindhurāja', 'Vairisiṃha', 'Merutuṅga', 'Gāṅgeya', 'Abu', 'Padmagupta', 'Cedi', 'Chedi', 'Nagpur', 'Dhār', 'Pāṇini', 'Arjunavarman', 'Pārijātamañjarī', 'Kāmasūtra', 'Narasiṃha', 'Somēśvara', 'Nāmamālikā', 'Sarasvatīkaṇṭhābharaṇa', 'Prabandhacintāmaṇi', 'Bhāillasvāmin', 'Navasāhasāṅkacarita', 'Subhāṣitaratnasaṃdoha', 'Jayavarman', 'Al-Bīrūnī', 'Bīrūnī', 'Anahilapāṭaka', 'Indian Antiquary', 'Antiquary', 'INTACH', 'Udaysagar', 'Udayasamudra', 'Bhujariya', 'Barakhambi', 'Pisanhari', 'Pisanhārī', 'Bijamandal', 'Shahi', 'Masjid', 'Jahāngīr', 'Shāh Jahān', 'Ghiyās', 'Sher Khan', 'Mandu', 'Chanderi', 'Tīrthaṅkara', 'Muslim', 'Śeṣaśāyī', 'Lakulīśa', 'Ravan Tol', 'Naṭarāja', 'Vikrama', 'Dhāmadeva', 'Siṃhāsanadvātriṃśikā', 'Vikramāditya', 'Telangana', 'Lat Masjid', 'Benji', 'Maada', 'Bedni', 'Berni', 'Harijan', 'Gonds', 'Bhringraj', 'Bhringrajpur', 'Daulatpur', 'Gabbar', 'Ramgarh', 'Gyasuddin', 'Sundarkand', 'Jayasiṃha', 'Vālabha', 'Sāmavedins', 'Chāndogya', 'Lāṭa', 'Madhyadeśa', 'Magadha', 'Tailakas', 'Bundeli', 'Malwi', 'Bundelkhandi', 'Suvi', 'Bagdis', 'Bagdi', 'Sot', 'Raisen', 'Raṇipadra', 'Prāyaścittasamuccaya', 'Sīyaka', 'Lambakarṇa', 'Viśveśvara', 'Śambhu', 'Pūrvagrāma', 'Rāḍha', 'Nāṭana', 'Caṇḍikāśrama', 'Āūrakācārya', 'Siddheśvara', 'Mahākāla', 'Pārśvanātha', 'Tīrthaṅkaras', 'Kāpālika', 'Siddhāntasaṅgraha', 'Siddhāntins', 'Śivatattvaratnakalikā', 'Kālānana', 'Māheśvaras', 'Kālāmukhas', 'Śivajñānabodham', 'Kāyāvarohaṇa', 'Karvan', 'Jāvala', 'Ekalingji', 'Hathuṇḍī', 'Rajputs', 'Vasantotsava', 'Diwālī', 'Pavitraka', 'Cāmuṇḍarāja', 'Maṇḍaleśa', 'Chau-ju-kua', 'Gāṅgeyadeva', 'Pālhaṇadeva', 'Dhārāvarṣa', 'Memmaka', 'Bṛhatsaṃhitā', 'Mahānirvāṇa', 'Cāhamāna', 'Cāhamānas', 'Naḍḍula', 'Śākambharī', 'Santosh', 'Kumar', 'Umaratha', 'Rayakuka', 'Vasantapāla', 'Udaleśvara', 'Vaidyanātha', 'Bhiraṅgāvalī', 'Limbārvā', 'Carcikā', 'Tattvaprakāśa', 'Pāśupata', 'Pāśupatas', 'Mattamayūra', 'Śivarātri', 'Sendhavadeva', 'Arthuna', 'Śrīmāla', 'Rāma', 'Lakṣmaṇa', 'Sītā', 'Ghaḍiyālan-kā-makān', 'Mahāvīra', 'Ādinātha', 'Ghiyāth', 'Ghiyāth-ud-dīn', 'Mālwa', 'Khaljī', 'Khalji', 'Sultan', 'Sultans', 'Delhi', 'Muhammad', 'Arabic', 'Yaśovarman', 'Lakṣmīvarman', 'Hariścandra', 'Trailokyavarman', 'Udayavarman', 'Vindhyavarman', 'Subhaṭavarman', 'Jaitugi', 'Siddharāja', 'Madanavarman', 'Sallakṣaṇavarman', 'Mūlarāja', 'Ballāla', 'Mahlakadeva', 'Mahlak', 'Kokā', 'Iltutmish', 'Balban', 'Visaladeva', 'Vāghelā', 'Yādava', 'Yādavas', 'Siṃhaṇa', 'Augasī', 'Bhillasvāmipura', 'Avantīnātha', 'Avanti', 'Pathāri', 'Pathari', 'Māndhātā', 'Harsūd', 'Ujjayinī', 'Minhāj', 'Minhaj', 'Siraj', 'Ṭabaqāt', 'Ain-ul-Mulk', '‘Ain-ul-Mulk', 'Alauddin', 'Dilawar', 'Ghuri', 'Hoshang', 'Bahadur', 'Medini', 'Salhadi', 'Puranmal', 'Qadir', 'Humayun', 'Sher Shah', 'Baz', 'Babur', 'Akbar', 'Aurangzeb', 'Alamgirpur', 'Alamgirnagar', 'Auliya', 'Samad', 'Firdaus-Makani', 'Zilhijja', 'Hijri', 'qaziyat', 'Sironj', 'Gondwana', 'Dost', 'Bhopal', 'Berasia', 'Gyaraspur', 'Faruk', 'Kurwai', 'Basoda', 'Ganj', 'Diler', 'Ahsanullah', 'Peshwa', 'Pawar', 'Tukoji', 'Jeevaji', 'Dewas', 'Chimnaji', 'Girdhar', 'Ranoji', 'Malharrao', 'Holkar', 'Balaji', 'Bajirao', 'Panipat', 'Mahadji', 'Mahadaji', 'Scindia', 'Sindhia', 'Scindias', 'Khanderao', 'Khande', 'Appaji', 'Bappa', 'Saheb', 'Jankoji', 'Kamasdar', 'Kamasdars', 'Subah', 'Lashkar', 'Isagarh', 'Indore', 'Madhya', 'Bharat', 'Pradesh', 'Bareth', 'Baretha', 'Sumer', 'Gulabganj', 'Pabai', 'Kulhar', 'Bina', 'Pauvanala', 'Chappan', 'Bhoja-era', 'Bhojshala', 'Vijay', 'Mandir', 'Sardar', 'Nizamat', 'Daulat', 'Rao', 'Jaora', 'Ijardars', 'Mahādeva', 'Narayan', 'Vyas', 'Mughal', 'Mughals', 'Afghan', 'Afghans', 'Maratha', 'Marathas']
TIWARI_FULL_NAME = False      # named in full in Chapter 1; here "Tiwari"
GAZ_MODERN_ONLY = False       # the Gazetteer may carry dynastic claims here, phrased as its own
GAZ_MAX_SHARE = 0.40          # user 2026-10-14
AUTHORED = True
HOUSE_VOICE = True
CONSOLIDATE_NOTES = True

CONFLICTS = {}

CHAPTER_BRIEF = """Chapter 10: political change and economic decline, Udaypur the thread across regimes (later Paramāras 1093-1305, Caulukya overlordship U1, Delhi and Malwa sultans, Mughals, Afghans and Marathas, Gwalior State, railway). Political demotion kept apart from economic decline, which is undated. Gazetteer tier 7, at most 40% of a unit, its statements its own. Tiwari testimony. Brass cover date HELD (RR-2). Canon U1, R1-R4, D1. Boundaries: buildings Ch 7; foundation Ch 4; archaeology and heritage administration Ch 11."""


def extra_rules(text, P, smap):
    import re
    fails = []
    secs = re.split(r"(?m)^(?=## 10\.\d+)", text)
    for s in secs:
        m = re.match(r"## (10\.\d+)", s)
        sec = m.group(1) if m else "chapter"
        for sent in re.split(r"(?<=[.!?”\]}])\s+(?=[A-Z“{])", s):
            ids = re.findall(r"C\d\d-[A-Z0-9-]+", sent)
            plain = re.sub(r"\[[^\]]*\]", "", sent)
            unq = re.sub(r"“[^”]*”", "", plain)
            if re.search(r"\b1059\b", plain) and not re.search(r"read|reading|survey|claim|gives|caption|faulty|late|pedigree|1116|dates", plain):
                fails.append({"sec": sec, "rule": "canon R3", "detail": plain.strip()[:120]})
            if re.search(r"\bKarṇa\b", plain) and not re.search(r"Kalacuri|Caulukya|Gujarat|Chedi|Cedi|unspecified", plain):
                fails.append({"sec": sec, "rule": "canon R2", "detail": plain.strip()[:120]})
            if re.search(r"Mohammedan|Muhammadan|Mahomedan|Moslem", unq):
                fails.append({"sec": sec, "rule": "period term outside quotation", "detail": plain.strip()[:120]})
            if re.search(r"mahādvādaśaka|Bhṛṅgārikā|mahāsādhanika", plain) and not re.search(r"\b11[4-7]\d\b|\b12[23]\d\b|record|grant", plain):
                fails.append({"sec": sec, "rule": "canon R4 (term not dated to its record)", "detail": plain.strip()[:120]})
            if re.search(r"\b(116\d|117\d)\b", unq) and re.search(r"governor|governed|headquarters|seat of government", unq) and not re.search(r"Caulukya|Gujarat|Kumārapāla|Ajayapāla|Lūṇapasāka|Rājyapāla", plain):
                fails.append({"sec": sec, "rule": "U1 (twelfth-century Udaypur not framed as Caulukya)", "detail": plain.strip()[:140]})
            if re.search(r"\b1841\b|\b1784\b", plain) and not re.search(r"inscri|reads|read|give|gives|given|figure|reckon|pending|HELD|RR-2|verif|edition|states|record", plain):
                fails.append({"sec": sec, "rule": "brass-cover date stated as settled (RR-2 open)", "detail": plain.strip()[:140]})
            if any("TEMPLE-ECON" in i for i in ids):
                fails.append({"sec": sec, "rule": "Temple Economics excluded", "detail": plain.strip()[:140]})
            if any("SAMAR" in i for i in ids) and re.search(r"[“\"]", sent):
                fails.append({"sec": sec, "rule": "SAMAR never quoted", "detail": sent.strip()[:140]})
            if re.search(r"\b(soldiers|raiders|plunderers|priests|villagers|masons|builders|labourers|workmen|farmers|peasants|cultivators|traders|merchants|artisans)\b", unq, re.I) and not ids:
                fails.append({"sec": sec, "rule": "anonymous actors check", "detail": plain.strip()[:120]})
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
