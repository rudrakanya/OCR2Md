"""Afterword, draft v1 (21 Oct 2026; in-session, no API) — configuration for drafting/_pipe.
Set UDAY_CFG to this file. Sections follow editorial/Udaypur_Book_Contents.md (Afterword, 12 units, numbered 13.1–13.12 for the tools).
Chapters 10–12 are not drafted: their items are cross-referenced and marked HELD in the notes."""
from pathlib import Path

CH = 13
VERSION = "v1"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch13"))
SECTIONS = [f"13.{i}" for i in range(1, 13)]
OUTLINE = D / "ch13_plan_v1.md"
PACK = D / "evidence_pack_v1.json"
LOG = D / "api_log_v1"
OUT = D / "ch13_draft_v1.md"
TITLE = "Conserving Udaypur: Community, Heritage and the Future"
CHAPTER_LABEL = "AFTERWORD"          # make_docx: printed in place of "CHAPTER 13"
NUMBERED_HEADINGS = False            # make_docx: unit headings print without "13.N"
DOCX_NAME = "Afterword - Conserving Udaypur - Draft v1.docx"
SUBTITLE = "Draft v1 · October 2026"
WMIN, WMAX, TOTAL_TARGET = 0, 10**9, 0   # user 17 Oct: no word targets; the outline's 2,750 (U2) is a guide, not a target
NO_LENGTH = True
BUDGET, RESERVE = 0.00, 0.00   # no API calls (user rule); in-session drafting and verification
BASELINE = None
BASELINE_MAP = {}
VOICE_SRC = None
OPEN_IN = ("Chapter 12 ends on the expectations of a tourist town, recorded as attitudes rather than plans. "
           "Open on the earliest dated proposal: the 2019 letter to a Collector.")
CLOSE_OUT = ("The book ends. Close on the village under the temple, by content; no exhortation, no question, "
             "no claim beyond the last record.")
ALLOW_EXTRA = ["Udayāditya", "Paramāra", "Paramāras", "Udayeśvara", "Udayapura", "Udaypur", "Vidisha", "Bhilsa", "Malwa",
               "Dhārā", "Bhoja", "Śiva", "Bhūmija", "Khajuraho", "Caulukya", "Candella", "Kalacuri", "Tiwari", "Pande",
               "Hardy", "Ganguly", "Patil", "Cunningham", "Beglar", "Bühler", "Kumārapāla", "Ajayapāla", "Devapāla",
               "Dhāmadeva", "Rājyapāla", "Lūṇapasāka", "Khande", "Rao", "Appaji", "Mahadji", "Scindia", "Tughluq",
               "Muhammad", "INTACH", "Udaysagar", "Udayasamudra", "Pisanhari", "Naṭarāja", "Ravan", "Tol", "Bija",
               "Mandal", "Vijay", "Mandir", "Kashi", "Vishwanath", "Bhopal", "Collector", "Suresh", "Mishra",
               "Upadhyay", "Madanmohan", "MGNREGA", "Mandi", "Bamora", "Ganj", "Basoda", "Bhojpur", "Rajasthan",
               "PPP", "Forest", "Department", "Geological", "Survey", "Tourism", "Archaeological", "India", "Indian",
               "Madhya", "Pradesh", "Bundelkhand", "Hindi", "English", "Sanskrit", "Persian", "Nāgarī", "Afterword",
               "Turasadasa", "Ustonatha", "Śivarātri", "Muslim", "Hindu", "Jain", "Sultanate", "Mughal", "Swachhta",
               "Abhiyan", "Ganguly", "Vyas", "Narayan", "Gwalior", "Garde", "Sanchi", "Bhimbetka", "UNESCO",
               "LR", "RR", "Chapters", "Chapter", "Chs", "HELD"]
TIWARI_FULL_NAME = False      # named in full in Chapter 1; here "Tiwari"
GAZ_MODERN_ONLY = False
GAZ_MAX_SHARE = 0.40          # user 2026-10-14
AUTHORED = True
HOUSE_VOICE = True
CONSOLIDATE_NOTES = True

CONFLICTS = {}

CHAPTER_BRIEF = """Afterword: reflective register, bounded. Reflection rests on the book's established history (ledger Chs 1-9) and the cited items; no new historical facts. Proposals told as proposals, attributed. One argument, labelled once (13.12); tests labelled once (13.11). No residents named; no living person accused; U7 (mining: one attributed sentence; palace order: administration only). Tiwari testimony; pp. 161-170 a contributor's voice (RR-30). Chs 10-12 not drafted: cross-references HELD."""

# residents and citizens (Tiwari pp. 63-70, 165), the official met in 2021, the ground reporter, and the palace plot number
RESIDENTS = (r"Praveen|Kaustubh|Shirhonkar|Kamlesh|Gagan|Dubey|Amit Shukla|Ramiskant|Shrivastava|Raja Miyan|Raja Mishra|"
             r"Hamid|Bashir|Ramesh|Rajkumar|Mallu|Khan Sahib|P\. ?K\. Mishra|Govind Saxena|khasra")


def extra_rules(text, P, smap):
    import re
    fails = []
    secs = re.split(r"(?m)^(?=## 13\.\d+)", text)
    for s in secs:
        m = re.match(r"## (13\.\d+)", s)
        sec = m.group(1) if m else "chapter"
        for para in [p for p in re.split(r"\n\s*\n", s) if p.strip() and not p.startswith("## ")]:
            ids = re.findall(r"C\d\d-[A-Z0-9-]+", para)
            if any(i.startswith(("C10-", "C11-", "C12-")) for i in ids) and "HELD" not in para:
                fails.append({"sec": sec, "rule": "Ch 10-12 cross-reference without HELD in the note", "detail": para.strip()[:120]})
        for sent in re.split(r"(?<=[.!?”\]}])\s+(?=[A-Z“{])", s):
            ids = re.findall(r"C\d\d-[A-Z0-9-]+", sent)
            plain = re.sub(r"\[[^\]]*\]", "", sent)
            unq = re.sub(r"“[^”]*”", "", plain)
            is_note = sent.lstrip().startswith("{{note")
            if ids and all("JAGTA-HI" in i for i in ids) and "“" in plain and not is_note:
                fails.append({"sec": sec, "rule": "JAGTA-HI gloss quoted (paraphrase it)", "detail": plain.strip()[:140]})
            if any("SAMAR" in i for i in ids) and re.search(r"[“\"]", sent):
                fails.append({"sec": sec, "rule": "SAMAR never quoted", "detail": sent.strip()[:140]})
            if any("TEMPLE-ECON" in i for i in ids):
                fails.append({"sec": sec, "rule": "Temple Economics excluded", "detail": plain.strip()[:140]})
            if re.search(r"\bKarṇa\b", plain) and not re.search(r"Kalacuri|Caulukya|unspecified", plain):
                fails.append({"sec": sec, "rule": "canon R2", "detail": plain.strip()[:120]})
            if re.search(r"\b1059\b", plain) and not re.search(r"read|reading|claim", plain):
                fails.append({"sec": sec, "rule": "canon R3", "detail": plain.strip()[:120]})
            if re.search(r"Mohammedan|Muhammadan|Mahomedan", unq):
                fails.append({"sec": sec, "rule": "period term outside quotation", "detail": plain.strip()[:120]})
            if re.search(RESIDENTS, plain):
                fails.append({"sec": sec, "rule": "living person named (residents, officials, claimants)", "detail": plain.strip()[:140]})
            if re.search(r"illegal (sandstone )?(mining|quarr)", unq, re.I) and not re.search(r"survey|alleg|attribut|lays", unq, re.I):
                fails.append({"sec": sec, "rule": "U7 mining sentence not attributed", "detail": plain.strip()[:140]})
            if re.search(r"\b(will|shall) (become|be|bring|attract|grow|draw|come)\b", unq) and not is_note:
                fails.append({"sec": sec, "rule": "narrator predicts a future (attribute it)", "detail": plain.strip()[:140]})
            if re.search(r"\b(masons|builders|quarrymen|labourers|workmen|craftsmen|traders|merchants|artisans)\b", unq, re.I) and not ids:
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
