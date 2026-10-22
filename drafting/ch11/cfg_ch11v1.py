"""Chapter 11, draft v1 (21 Oct 2026; in-session, no API) — configuration for drafting/_pipe.
Set UDAY_CFG to this file. Sections follow editorial/Udaypur_Book_Contents.md (8 units, one section each)."""
from pathlib import Path

CH = 11
VERSION = "v1"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch11"))
SECTIONS = [f"11.{i}" for i in range(1, 9)]
OUTLINE = D / "ch11_plan_v1.md"
PACK = D / "evidence_pack_v1.json"
LOG = D / "api_log_v1"
OUT = D / "ch11_draft_v1.md"
TITLE = "Udaypur in the Modern Period: Archaeology, Heritage Administration and Conservation"
DOCX_NAME = "Chapter 11 - Udaypur in the Modern Period - Draft v1.docx"
SUBTITLE = "Draft v1 · October 2026"
WMIN, WMAX, TOTAL_TARGET = 0, 10**9, 0   # user 17 Oct: no word targets; each unit as long as its evidence carries
NO_LENGTH = True
BUDGET, RESERVE = 0.00, 0.00   # no API calls (user rule); in-session drafting and verification
BASELINE = None
BASELINE_MAP = {}
VOICE_SRC = None
OPEN_IN = ("Chapter 10 ends on rank lost in steps and a decline that cannot be dated. Open on the town re-entering writing as an object of survey: Beglar's tour of 1871-72.")
CLOSE_OUT = ("Chapter 12 turns to the living community. End on the herds, quarries and climbers on the hill as the people the record meets at its edges; no recommendation.")
ALLOW_EXTRA = ["Udayāditya", "Paramāra", "Paramāras", "Udayeśvara", "Udayapura", "Udaypur", "Vidisha", "Bhilsa", "Malwa", "Bhoja", "Śiva",
               "Bhūmija", "Nāgara", "Kramrisch", "Pande", "Patil", "Ganguly", "Tiwari", "Cunningham", "Beglar", "Fergusson", "Singh",
               "Bühler", "Kielhorn", "Bhandarkar", "Garde", "Vyas", "Upadhyay", "Mishra", "Suresh Mishra", "Madanmohan", "Narayan",
               "Gwalior", "Scindia", "Scindias", "Mahadji", "Khande Rao Appaji", "Chatua", "Darwaza", "Dhīmar", "Dhimar", "Gujari Mahal",
               "Pathari", "Aurangzeb", "Tughluq", "Muhammad", "Deccan", "Persian", "Sanskrit", "Hindi", "English", "Nāgarī",
               "INTACH", "Bhopal", "Ganj Basoda", "Basoda", "Patrika", "Pisanhārī", "Barakhambi", "Naṭarāja", "Ravan Tol", "Udaysagar",
               "Uday Samudra", "Bhujariya", "Lajja Gauri", "Umā-Maheśvara", "Shahi Masjid", "Bijamandal", "Muslim", "Jain", "Hindu",
               "Epigraphia Indica", "Indica", "Archaeological Survey", "Survey", "Western Circle", "Madhya Pradesh", "Madhya Bharat",
               "Vikrama", "Jahangir", "Jahāṅgīr", "Prime Minister", "Chief Minister", "Collector", "Forest Department", "Rajasthan",
               "Neelkantheshwar", "Nīlakaṇṭheśvara", "Kalacuri", "Karṇa", "Mahādeva", "Bundelkhand", "Central Provinces", "India",
               "Indian", "Annual", "Report", "Ancient Monuments Preservation", "Declaration", "National Monuments", "Act",
               "Section", "Land Revenue Code", "Indian Land Revenue Code", "Tribal Museum", "Shyamla Hills", "Udayeśvaradeva",
               "Melamalai", "Pudukottai", "Nikaraṇāyesvara", "Geological Survey", "Bhumi-ja", "Un", "Chanderi", "Mughal", "Bhilsā",
               "National Institute of Lichens", "Mahakal", "Bhojpur", "Interpol", "Vidishā", "Udaipur", "Gwalior State", "State Archaeology", "Afterword", "LR", "RR", "HELD", "LEGAL", "REVIEW", "Legal"]
TIWARI_FULL_NAME = False      # named in full in Chapter 1; here "Tiwari"
GAZ_MODERN_ONLY = False
GAZ_MAX_SHARE = 0.40          # user 2026-10-14
AUTHORED = True
HOUSE_VOICE = True
CONSOLIDATE_NOTES = True

CONFLICTS = {}

CHAPTER_BRIEF = """Chapter 11: how Udaypur was recorded, protected and administered, 1871-2021. The colonial reports are the subject but staged (uncorrected, not ingested): told through Pande, Patil, Ganguly, Kramrisch, CII and Tiwari, with HELD notes. Surveyors, the ASI, Gwalior State and INTACH act where items name the act. U7: the mining allegation one attributed sentence naming no one; the 2021 notice's names never reproduced. No resident, claimant or junior official named. Tiwari testimony: no counts, figures or dates in the text (R5). Boundaries: the buildings Ch 7; regimes Ch 10; community and the future Ch 12/AW."""


def extra_rules(text, P, smap):
    import re
    fails = []
    secs = re.split(r"(?m)^(?=## 11\.\d+)", text)
    mining = 0
    for s in secs:
        m = re.match(r"## (11\.\d+)", s)
        sec = m.group(1) if m else "chapter"
        body = re.sub(r"\{\{note:.*?\}\}", "", s, flags=re.S)
        for sent in re.split(r"(?<=[.!?”\]}])\s+(?=[A-Z“{])", s):
            ids = re.findall(r"C\d\d-[A-Z0-9-]+", sent)
            plain = re.sub(r"\[[^\]]*\]", "", sent)
            unq = re.sub(r"“[^”]*”", "", plain)
            if any("SAMAR" in i for i in ids) and re.search(r"[“\"]", sent):
                fails.append({"sec": sec, "rule": "SAMAR never quoted", "detail": sent.strip()[:140]})
            if re.search(r"\b1059\b", plain) and not re.search(r"read|reading|caption|later|dating|1080", plain):
                fails.append({"sec": sec, "rule": "canon R3", "detail": plain.strip()[:120]})
            if re.search(r"\bKarṇa\b", plain) and not re.search(r"Kalacuri|Caulukya|Gujarat|Chedi|Cedi", plain):
                fails.append({"sec": sec, "rule": "canon R2", "detail": plain.strip()[:120]})
            if re.search(r"Mohammedan|Muhammadan|Mahomedan", unq):
                fails.append({"sec": sec, "rule": "period term outside quotation", "detail": plain.strip()[:120]})
            if re.search(r"Irfan|Mehboob|Mahboob|Ahmed Ali|Ahmad Ali|Mubarik|Qazi Syed|Syed|Ahirwar|Dauji|Praveen|Raja Miyan|Malukdas|Malluk", plain):
                fails.append({"sec": sec, "rule": "U7 / living person named", "detail": plain.strip()[:140]})
            if any("TEMPLE-ECON" in i for i in ids):
                fails.append({"sec": sec, "rule": "Temple Economics excluded (R9)", "detail": plain.strip()[:140]})
            if re.search(r"\b(masons|builders|quarrymen|labourers|workmen|craftsmen|traders|merchants|thieves|smugglers|miners)\b", unq, re.I) and not ids:
                fails.append({"sec": sec, "rule": "anonymous agent check", "detail": plain.strip()[:120]})
        mining += len(re.findall(r"\[[^\]]*(?:C11-JAGTA-EN-028|C12-JAGTA-EN-003|C12-JAGTA-HI-011)[^\]]*\]", body))   # body sentences only; notes excluded
        for para in body.split("\n\n"):
            if re.search(r"\b(lakh|crore)s?\b|\bhectares?\b|\b980\b|\bhundred inscriptions\b|\b42\b", para, re.I):
                fails.append({"sec": sec, "rule": "Tiwari figure in body text (R5)", "detail": para.strip()[:140]})
    if mining > 1:
        fails.append({"sec": "chapter", "rule": "U7: mining allegation in more than one sentence", "detail": str(mining)})
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
