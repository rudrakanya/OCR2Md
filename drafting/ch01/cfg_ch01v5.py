"""Chapter 1, draft v5 (house voice; editor-in-chief audit approved 2026-10-14) — configuration for drafting/_pipe.
Set UDAY_CFG to this file. Sections follow chapters.md (Plan changes, 14 Oct 2026)."""
from pathlib import Path

CH = 1
VERSION = "v5"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch01"))
SECTIONS = ["1.1", "1.2", "1.3", "1.4", "1.5"]
OUTLINE = D / "ch01_plan_v5.md"
PACK = D / "evidence_pack_v5.json"
LOG = D / "api_log_v5"
OUT = D / "ch01_draft_v5.md"
TITLE = "Udaypur: A Small Town with a Long Memory"
DOCX_NAME = "Chapter 1 - Udaypur - Draft v5.docx"
SUBTITLE = "Draft v5 · October 2026"
WMIN, WMAX, TOTAL_TARGET = 3200, 4400, 4000   # user 2026-10-14: sections 70–120%, chapter 3,200–4,400, never pad
BUDGET, RESERVE = 9.00, 1.00   # user 15 Oct: includes all sunk spend
BASELINE = D / "ch01_draft_v3.md"
# the closest v3 section for each v5 section ("before" metrics; judge baseline)
BASELINE_MAP = {"1.1": "1.1", "1.2": "1.4", "1.3": "1.2", "1.4": "1.5", "1.5": "1.3"}
VOICE_SRC = None
OPEN_IN = "Chapter 1 opens the book: the hill, then the temple, then the village, as anyone coming from Ganj Basoda meets them."
CLOSE_OUT = "Chapter 2 turns to the land both answers to the founding question stand on: the Betwa valley's water, stone and seasons."
ALLOW_EXTRA = ["Udayāditya", "Bhoja", "Paramāra", "Udayeśvara", "Devapāla", "Dhārā", "Malwa"]
TIWARI_FULL_NAME = True
GAZ_MODERN_ONLY = True
AUTHORED = True
HOUSE_VOICE = True            # validate.py: no per-paragraph [INT] requirement or labels, no n-gram check, section bands 70–120%
CONSOLIDATE_NOTES = True      # footnote.py: one reader-facing note per paragraph or claim cluster; IDs in hidden comments

CONFLICTS = {
    "1.1": [("Berni Mata legend", [r"Berni|Bedni|Benji", r"dancer|yak[sṣ]a"])],
    "1.2": [("Udayāditya: relation to Bhoja", [r"brother", r"disputed|bandhu|relative"]),
            ("accession as working position", [r"1070", r"1058|1059"])],
    "1.3": [("mosque: Tughluq vs Aurangzeb", [r"Tughl", r"Aurangzeb"])],
    "1.5": [("pre-Udayāditya settlement", [r"earlier|older|before", r"new town|no earlier|no inscription|absence"])],
}

CHAPTER_BRIEF = """You are writing Chapter 1, "Udaypur: A Small Town with a Long Memory", of a history of Udaypur (Vidisha district, Madhya Pradesh, India): the town of the Paramāra king Udayāditya and the Udayeśvara temple, NOT Udaipur in Rajasthan. The chapter shows how today's village came to hold the remains, records and memories of a far more important place, makes the Paramāras present as a polity in outline (Chapter 4 tells the full dynastic story), and leaves the founding question genuinely open before handing over to the land (Chapter 2).

CHAPTER CANON (binding):
- Udayāditya is "Bhoja's brother", as two inscriptions of his son Jagaddēva state (Dōngargāon, 1112; Jainād), cited (user decision D2, 16 Oct 2026). Never "nephew". The dissent (bandhu, Ganguly's junior branch, the sixteenth-century pedigree) goes in one note.
- Udayāditya's accession c. 1070 is the working position, given with the other datings beside it and framed around the event.
- Borrowed items (flag "borrowed", IDs from other chapters) are used only in 1.2 and 1.3, the sections that tell the dynasty and the later layers.
- Do not mention a 1310 record or a 1645 slab. At most 3 attributed scholarly assessments of the temple's significance in the chapter.
- *Jagta Hua Kasba* (JAGTA) is testimony by Vijay Manohar Tiwari: name in full once, at the first mention (1.1), then "Tiwari"; no gendered pronouns; never "a visitor"; evidence for memory and the present, never for a medieval fact or a measurement.
- The district Gazetteer (GAZ) is the 1979 compilation, for the modern setting. A praśasti is royal panegyric: what it claims and what happened are different propositions. Samarāṅgaṇasūtradhāra items (SAMAR) are old OCR: never quote.
- Compatibility is not identity: never merge two inscriptions, buildings, tanks, traditions, rulers, places, layers or hypotheses unless an item says they are the same. In particular the "tentatively" read two-line inscription on the hill and the survey's inscription that "remains to be deciphered" stay separate.
- Leave the Betwa valley's land and water to Chapter 2."""


def extra_rules(text, P, smap):
    import re
    fails = []
    for sec, rows in smap.items():
        for r in rows:
            bad = [x for x in r["ids"] if x in P and "borrowed" in P[x]["flags"] and sec not in ("1.2", "1.3")]
            if bad:
                fails.append({"sid": r["sid"], "sec": sec, "rule": "borrowed item outside 1.2–1.3", "detail": ", ".join(bad)})
    for pat, what in ((r"\b1310\b", "the 1310 record"), (r"\b1645\b|Qanungo|Kanungo", "the 1645 Qanungo Baoli slab"), (r"\bnephew\b", "'nephew' (canon: kinsman, relationship disputed)")):
        if re.search(pat, text):
            fails.append({"sec": "chapter", "rule": "canon", "detail": what})
    return fails


# ---- context retrieval (approved: contextual dynastic items citable for wider history; cap 45, existing corpus only)
KB_IN = D / "evidence_pack_v5_base.json"
KB_MAX_NEW = 45
KB_TOPIC = "Udaypur and the Paramāra polity: the kingdom centred on Dhārā, Bhoja's fall and Udayāditya's recovery, how the east was governed, the east after Udayāditya to 1305, and how the founder is known"
KB_SUBS = "S1 names/identity; S2 location/setting/approach; S3 references in texts/records; S4 memory/legends; S5 significance; S6 historical questions"
KB_SECTIONS = ["1.1", "1.2", "1.3", "1.4", "1.5"]
KB_GAP = {
    "1.2": ["the Paramara kingdom with its capital at Dhara and its extent, Bhilsa on the east",
            "Bhoja's last years and death, Malwa invaded by the Chaulukya Bhima and the Kalachuri Karna, Dhara occupied",
            "Jayasimha after Bhoja and the accession of Udayaditya, who recovered Malwa from Karna"],
    "1.2b": ["administration of the Paramara kingdom: mandala, pathaka, bhoga, visaya, officials and feudatories",
             "Udayapura as headquarters of a division of the Paramara kingdom, feudatory families ruling there",
             "Bhailasvamin Bhilsa under the Paramaras, eastern Malwa as a frontier province"],
    "1.3": ["Naravarman, Yasovarman and Jayavarman, the successors of Udayaditya, and the loss of Malwa to the Chaulukyas",
            "Chandella king residing at Bhailasvamin in 1134, Chandella conquest of eastern Malwa",
            "Mahakumara branch of the Paramaras ruling near Bhopal, Harischandra, Udayavarman grants"],
    "1.3b": ["Paramara kings Devapala and Jayasimha with inscriptions at Udayapur in the thirteenth century",
             "end of the Paramara dynasty, Alauddin Khalji's conquest of Malwa, Mahlakadeva, 1305",
             "Udaypur under the sultans of Malwa at Mandu"],
    "1.4": ["Udayapur prasasti genealogy of the Paramaras, the Agnikula origin at Mount Abu, the sage Vasistha",
            "victories and building claimed for Udayaditya in his inscriptions, praise verses",
            "first discovery, reading and publication of the Udaypur inscriptions in the nineteenth century"],
    "1.5": ["eastern frontier of Paramara territory before Udayaditya, earlier rulers of the Vidisha region in the tenth century"],
}
KB_CONTRA = {"Udayāditya: relation to Bhoja": "Udayaditya was Bhoja's nephew from a junior branch of the Paramara family",
             "accession of Udayāditya": "Udayaditya came to the throne immediately after Bhoja's death"}

SETTLED = [
    (r"(?:\d+|thirteen|sixteen)[^.]{0,40}(?:km|kilomet)[^.]{0,80}\bBasoda\b|\bBasoda\b[^.]{0,80}(?:\d+|thirteen|sixteen)[^.]{0,6}(?:km|kilomet)",
     r"13\s*[–-]\s*16|thirteen to sixteen|thirteen and sixteen", "Ganj Basoda 13–16 km"),
    (r"(?:\d+|fifty|seventy)[^.]{0,40}(?:km|kilomet)[^.]{0,80}\bVidisha\b|\bVidisha\b[^.]{0,80}(?:\d+|fifty|seventy)[^.]{0,6}(?:km|kilomet)",
     r"55\s*[–-]\s*70|fifty-five to seventy|fifty-five and seventy", "Vidisha 55–70 km"),
]
