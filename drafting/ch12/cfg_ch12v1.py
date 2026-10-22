"""Chapter 12, draft v1 (21 Oct 2026; in-session, no API) — configuration for drafting/_pipe.
Set UDAY_CFG to this file. Sections follow editorial/Udaypur_Book_Contents.md (10 units, one section each)."""
from pathlib import Path

CH = 12
VERSION = "v1"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch12"))
SECTIONS = [f"12.{i}" for i in range(1, 11)]
OUTLINE = D / "ch12_plan_v1.md"
PACK = D / "evidence_pack_v1.json"
LOG = D / "api_log_v1"
OUT = D / "ch12_draft_v1.md"
TITLE = "Udaypur Today: A Living Community and Its Historic Environment"
DOCX_NAME = "Chapter 12 - Udaypur Today - Draft v1.docx"
SUBTITLE = "Draft v1 · October 2026"
WMIN, WMAX, TOTAL_TARGET = 0, 10**9, 0   # user 17 Oct: no word targets; each unit as long as its evidence carries
NO_LENGTH = True
BUDGET, RESERVE = 0.00, 0.00   # no API calls (user rule); in-session drafting and verification
BASELINE = None
BASELINE_MAP = {}
VOICE_SRC = None
OPEN_IN = ("Chapter 11 ended on the threats to the hill and its fortification wall. Open below the hill on the census count of houses.")
CLOSE_OUT = ("The Afterword turns to conservation and the future. End on residents expecting visitors and outsiders predicting a destination; no recommendation.")
ALLOW_EXTRA = ["Udayāditya", "Paramāra", "Paramāras", "Udayeśvara", "Udayapura", "Udaypur", "Udaipura", "Vidisha", "Bhilsa", "Malwa",
               "Bhoja", "Śiva", "Mahadev", "Mahādeva", "Nīlakaṇṭheśvara", "Neelkantheshwar", "Caulukya", "Caulukyas", "Kumārapāla", "Ajayapāla",
               "Tughluq", "Muhammad", "Tiwari", "Mishra", "Suresh", "Saxena", "Govind", "Upadhyay", "Vadnerkar", "Ajit", "Vivek", "Shivkumar",
               "Narayan", "Vyas", "Ganj", "Basoda", "Bareth", "Bina", "Bhopal", "Mandi", "Bamora", "Kurwai", "Basuda", "Gyaraspur", "Mahuli",
               "Bhilsa", "Basoda", "INTACH", "ASI", "Archaeological", "Survey", "Patrika", "Tribal", "Museum", "Shyamla", "Ravan", "Tol",
               "Pisanhārī", "Pisanhari", "Śivarātri", "Sarus", "Painted", "Stork", "Oriental", "White-backed", "Long-billed", "Red-headed",
               "Indo-Malayan", "BirdLife", "International", "Akashvani", "Radio", "Madhya", "Bharat", "Pradesh", "Gazetteer", "Geo-Heritage",
               "Betwa", "Patil", "Sharma", "Mandu", "Delhi", "Persian", "Indian", "India", "Ganj Basoda", "Facebook", "Naidunia", "Dainik",
               "Bhaskar", "Kohinoor", "Parliament", "Collector", "Sunday", "Mondays", "Monday", "January", "February", "March", "April",
               "Jama", "Masjid", "Dasharna", "Van", "Tulsi", "Udaysagar", "Shiv", "Pindi", "Afterword", "Jain", "Hindu", "Muslim", "Teen", "Darwaza"]
TIWARI_FULL_NAME = False      # named in full in Chapter 1; here "Tiwari"
GAZ_MODERN_ONLY = False
GAZ_MAX_SHARE = 0.40          # user 2026-10-14
AUTHORED = True
HOUSE_VOICE = True
CONSOLIDATE_NOTES = True

CONFLICTS = {}

CHAPTER_BRIEF = """Chapter 12: Udaypur today, at the last record (2020-22). The present told as what the sources record, with dates of observation;
no advocacy (the Afterword's). Living people: no residents or signboard claimants named (U7); officials as offices; every passage touching a
living person or contested matter flagged for legal review. Tiwari testimony gives no counts, distances, widths or dates. Guest voices at
pp. 161-166 are Vivek's and Vadnerkar's, not Tiwari's. Wildlife from Ch 2 belongs to 12.5. Boundaries: Ch 9 (social fabric),
Ch 11 (heritage administration, the palace, thefts, threats), Afterword (proposals and future)."""


def extra_rules(text, P, smap):
    import re
    fails = []
    secs = re.split(r"(?m)^(?=## 12\.\d+)", text)
    mining = len(re.findall(r"C12-JAGTA-EN-003", re.sub(r"\{\{note:.*?\}\}", "", text, flags=re.S)))
    for s in secs:
        m = re.match(r"## (12\.\d+)", s)
        sec = m.group(1) if m else "chapter"
        sents = re.split(r"(?<=[.!?”\]}])\s+(?=[A-Z“{])", s)
        for n, sent in enumerate(sents):
            nxt = sents[n + 1] if n + 1 < len(sents) else ""
            ids = re.findall(r"C\d\d-[A-Z0-9-]+", sent)
            plain = re.sub(r"\[[^\]]*\]", "", sent)
            unq = re.sub(r"“[^”]*”", "", plain)
            # U7 and living residents: no resident, volunteer, claimant or family named
            if re.search(r"Raja Miyan|Raja Mishra|Hamid|Bashir|Ramesh|Rajkumar|Mallu|Praveen|Kaustubh|Kamlesh|Gagan|Amit Shukla|Ramakant|Ramiskant|Qazi|Khasra|Sanjeev|Ajay Upadhyay|Ward No", plain):
                fails.append({"sec": sec, "rule": "living resident or claimant named (U7)", "detail": plain.strip()[:140]})
            if re.search(r"green cloth|\bpīr\b|\bpir\b|maulvi|mazar", plain, re.I):
                fails.append({"sec": sec, "rule": "excluded passage (C12-JAGTA-EN-007) used", "detail": plain.strip()[:140]})
            if re.search(r"Jama Masjid", plain):
                fails.append({"sec": sec, "rule": "lane house identified by its signboard", "detail": plain.strip()[:140]})
            # R5: testimony gives no counts, widths or distances
            jag = [i for i in ids if "JAGTA" in i]
            if jag and len(jag) == len(ids) and re.search(r"\blakh|\bhundred\b|\bthousand\b|\b\d+\s*(?:km|kilomet|feet|foot|ft|m\b)|\bforty\b|\b40\b|four hundred|\b400\b|eight feet|ten feet|year-old|\b57\b", unq, re.I):
                fails.append({"sec": sec, "rule": "testimony count/measurement (R5)", "detail": plain.strip()[:140]})
            if re.search(r"Mohammedan|Muhammadan|Mahomedan", unq):
                fails.append({"sec": sec, "rule": "period term outside quotation", "detail": plain.strip()[:120]})
            if re.search(r"\b1059\b", plain) and not re.search(r"read|reading|1116", plain):
                fails.append({"sec": sec, "rule": "canon R3", "detail": plain.strip()[:120]})
            if re.search(r"\bKarṇa\b", plain) and not re.search(r"Kalacuri|Caulukya", plain):
                fails.append({"sec": sec, "rule": "canon R2", "detail": plain.strip()[:120]})
            if re.search(r"\b(masons|builders|quarrymen|labourers|workmen|craftsmen|farmers|peasants|cultivators|traders|merchants|artisans|shopkeepers|villagers|residents)\b", unq, re.I) and not ids and not re.findall(r"C\d\d-[A-Z0-9-]+", nxt) and not sent.strip().startswith("{{"):
                fails.append({"sec": sec, "rule": "anonymous people without evidence", "detail": plain.strip()[:120]})
    if mining > 1:
        fails.append({"sec": "chapter", "rule": "U7: the mining allegation in more than one sentence", "detail": f"{mining} sentences cite C12-JAGTA-EN-003"})
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
