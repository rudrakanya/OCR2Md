"""Chapter 1, draft v4 (authored history) — configuration for the shared toolkit (drafting/_pipe). Set UDAY_CFG to this file."""
from pathlib import Path

CH = 1
VERSION = "v4"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch01"))
SECTIONS = ["1.1", "1.2", "1.3", "1.4", "1.5"]
OUTLINE = D / "ch01_outline_v4.md"
PACK = D / "evidence_pack_v4.json"
LOG = D / "api_log_v4"
OUT = D / "ch01_draft_v4.md"
TITLE = "Udaypur: A Small Town with a Long Memory"
DOCX_NAME = "Chapter 1 - Udaypur - Draft v4.docx"
WMIN, WMAX, TOTAL_TARGET = 3800, 4200, 4000
BUDGET, RESERVE = 5.00, 0.90
BASELINE = D / "ch01_draft_v3.md"
VOICE_SRC = None
OPEN_IN = "Chapter 1 opens the book: arrive at the ordinary town first and meet the monument through the village."
CLOSE_OUT = "Chapter 2 turns to the country that produced the town — the Betwa valley's geography, geology and natural environment."
ALLOW_EXTRA = ["Udayāditya", "Bhoja", "Paramāra", "Udayeśvara", "Devapāla"]
TIWARI_FULL_NAME = True
GAZ_MODERN_ONLY = True

CONFLICTS = {
    "1.1": [("Berni Mata legend", [r"Berni|Bedni|Benji", r"dancer", r"yak[sṣ]a"])],
    "1.2": [("Lūṇapasāka record date", [r"L[uū][nṇ]apas[aā]ka", r"117[123]"]),
            ("brass cover donor", [r"Appaji", r"Bappa"]),
            ("mosque: Tughluq vs Aurangzeb", [r"Tughl", r"Aurangzeb"])],
    "1.3": [("pre-Udayāditya settlement", [r"earlier|older|before", r"new town|began|from nothing|no inscription|no earlier|emergence as a town"])],
    "1.4": [("founding: when", [r"1059", r"1080"]),
            ("Udayasamudra identification", [r"cannot be identified|unidentified|uncertain|not (?:been )?identified|lost", r"Udaysagar|ruins|fields"])],
    "1.5": [("praśasti date", [r"undated|not bear any date|no date", r"1072|1059"]),
            ("accession as working position", [r"1070", r"1058|1059"])],
}

CHAPTER_BRIEF = """You are writing Chapter 1, "Udaypur: A Small Town with a Long Memory", of a history of Udaypur (Vidisha district, Madhya Pradesh, India) — the town of the Paramāra king Udayāditya and the Udayeśvara temple, NOT Udaipur in Rajasthan. The chapter introduces the place itself: the ordinary town and how one arrives at it, the layers of rule standing in it, how far back its record reaches, its name, and what kinds of evidence carry its story.

CHAPTER CANON (binding):
- Borrowed items (flag "borrowed", IDs from other chapters) are used ONLY in section 1.2 — except C04-PANDE-005 (accession) in 1.5.
- Do not mention a 1310 record or a 1645 slab.
- At most 3 attributed scholarly assessments of the temple's significance in the chapter, all in 1.2.
- Udayāditya's accession c. 1070 is the working position: give c. 1070 with the other datings beside it, framed around the event ("is dated variously to …").
- *Jagta Hua Kasba* (IDs with JAGTA) is testimony — present-day observation, folklore and an author's views: never the source of a medieval fact or a measurement; its pages are approximate. Its author is Vijay Manohar Tiwari: name him in full once, at his first mention in the chapter (1.1), then "Tiwari"; no citation needed for the name; avoid gendered pronouns. Present his material as testimony or tradition ("residents remember…", "a local tradition holds…") — name him only where the eyewitness matters.
- The district Gazetteer (GAZ) is for the modern setting only, the 1979 compilation. A praśasti is royal panegyric: its claims are the inscription's claims. Samarāṅgaṇasūtradhāra items are old OCR (never quote).
- Leave the Betwa valley's land and water to Chapter 2."""


def extra_rules(text, P, smap):
    import re
    fails = []
    for sec, rows in smap.items():
        for r in rows:
            bor = [x for x in r["ids"] if x in P and "borrowed" in P[x]["flags"]]
            bad = [x for x in bor if sec != "1.2" and not (sec == "1.5" and x == "C04-PANDE-005")]
            if bad:
                fails.append({"sid": r["sid"], "sec": sec, "rule": "borrowed item outside 1.2", "detail": ", ".join(bad)})
    for pat, what in ((r"\b1310\b", "the 1310 record"), (r"\b1645\b|Qanungo|Kanungo", "the 1645 Qanungo Baoli slab")):
        if re.search(pat, text):
            fails.append({"sec": "chapter", "rule": "dropped item reappears", "detail": what})
    if "1070" not in text:
        fails.append({"sec": "1.5", "rule": "accession", "detail": "c. 1070 not presented"})
    return fails

# ---- authored-history run (Phase 2): facts cited, interpretation marked [INT], debates in {note: … [IDs]}
AUTHORED = True
BUDGET, RESERVE = 8.50, 1.00
INTERP_BRIEF = D / "ch01_interpretive_brief.md"
SAMPLE_TXT = D.parent / "style" / "sample_text.txt"          # the writing sample's full text (6-gram overlap check)
SUBTITLE = "Draft v4 · October 2026"
KB_IN = D / "evidence_pack_v3.json"
KB_MAX_NEW = 25
# targeted queries from the interpretive brief (where the argument needed support the pack lacked)
KB_TOPIC = "Udaypur's founding or renaming: the earliest evidence of the place, the act of naming, memory organised around the founder, later regimes in the founder's precinct"
KB_SUBS = "S1 names/identity; S2 location/setting/approach; S3 references in texts/records; S4 memory/legends; S5 significance; S6 historical questions"
KB_GAP = {
    "1.1": ["what Udaypur villagers remember about Udayaditya and the founding of the town",
            "people of Udaypur unaware of or indifferent to the town's history and monuments",
            "उदयपुर के लोग अपने इतिहास के बारे में क्या जानते हैं"],
    "1.2": ["Udaypur as a pargana or administrative headquarters under the sultans or the Mughals",
            "mosque built inside the courtyard of the Udayeshvara temple demolished shrines"],
    "1.3": ["remains at Udaypur older than Udayaditya earlier settlement before the Paramaras",
            "reading of the eighth century inscription on Udaypur hill sutradhara",
            "Bhujariya talab date older than Udaysagar steps of the bund",
            "Udayaditya founded a new town at Udaypur no earlier inscription",
            "Bhringraj Bhringrajpur Gond rule before Udayaditya"],
    "1.4": ["Udayapura named after Udayaditya town temple and tank named after the king",
            "Nemaka dynasty Udayapura feudatory of Udayaditya"],
    "1.5": ["Udayaditya accession date ruling paternal territory before becoming king"],
}
KB_CONTRA = {"founded new town": "Udayaditya founded the new town of Udayapura where nothing existed before",
             "earliest date at Udaypur": "earliest inscription at Udaypur date"}

# settled ranges (never narrowed to one source's figure): (sentence trigger, required range wording, label)
SETTLED = [
    (r"(?:\d+|thirteen|sixteen)[^.]{0,40}(?:km|kilomet)[^.]{0,80}\bBasoda\b|\bBasoda\b[^.]{0,80}(?:\d+|thirteen|sixteen)[^.]{0,6}(?:km|kilomet)",
     r"13\s*[–-]\s*16|thirteen to sixteen|thirteen and sixteen", "Ganj Basoda 13–16 km"),
    (r"(?:\d+|fifty|seventy)[^.]{0,40}(?:km|kilomet)[^.]{0,80}\bVidisha\b|\bVidisha\b[^.]{0,80}(?:\d+|fifty|seventy)[^.]{0,6}(?:km|kilomet)",
     r"55\s*[–-]\s*70|fifty-five to seventy|fifty-five and seventy", "Vidisha 55–70 km"),
]
