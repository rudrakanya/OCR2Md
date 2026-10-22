"""Chapter 1, draft v3 — configuration for the shared toolkit (drafting/_pipe). Set UDAY_CFG to this file."""
from pathlib import Path

CH = 1
VERSION = "v3"
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch01"))
SECTIONS = ["1.1", "1.2", "1.3", "1.4", "1.5"]
OUTLINE = D / "ch01_outline_v3.md"
PACK = D / "evidence_pack_v3.json"
LOG = D / "api_log_v3"
OUT = D / "ch01_draft_v3.md"
TITLE = "Udaypur: A Small Town with a Long Memory"
DOCX_NAME = "Chapter 1 - Udaypur - Draft v3 (footnoted).docx"
WMIN, WMAX, TOTAL_TARGET = 3800, 4200, 4000
BUDGET, RESERVE = 5.00, 0.90
BASELINE = D / "ch01_draft_v2.md"
VOICE_SRC = None
OPEN_IN = "Chapter 1 opens the book: arrive at the ordinary town first and meet the monument through the village."
CLOSE_OUT = "Chapter 2 turns to the country that produced the town — the Betwa valley's land, rivers and seasons."
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

# ---- knowledge-base gap fill for v3 (place-focused details; at most 15 new items)
KB_IN = D / "evidence_pack_v2.json"
KB_MAX_NEW = 15
KB_TOPIC = "Udaypur as a place: the village today, its streets, buildings, names, memories, records and founding"
KB_SUBS = "S1 names/identity; S2 location/setting/approach; S3 references in texts/records; S4 memory/legends; S5 significance; S6 historical questions"
KB_GAP = {
    "1.1": ["Udaypur village market houses streets daily life today", "people of Udaypur village occupations residents",
            "उदयपुर गांव के लोग बाजार और रोज़मर्रा का जीवन"],
    "1.2": ["Udaypur mosques palace Mughal period buildings in the village", "Udaypur temple brass kalash Scindia Gwalior patronage"],
    "1.3": ["Udaypur earliest remains older than the eleventh century", "Bhujariya talab older reservoir Udaypur steps"],
    "1.4": ["Udaypur town named after Udayaditya Udayapura name", "Nilakantheshwar name of Udayeshvara temple origin"],
    "1.5": ["legend of the temple built in one night Udaypur", "Udaypur temple escaped destruction tradition villagers"],
}
KB_CONTRA = {"distance to Basoda": "Udaypur distance from Basoda kilometres road",
             "population": "Udaypur village population census households"}

REPORT_OUTLINE_NOTES = """**Outline v3 (`ch01_outline_v3.md`)** keeps your five section names and their order, all v2 evidence assignments and every earlier content decision (borrowed items only in 1.2; 1310/1645 dropped; ≤3 attributed assessments; c. 1070 as working position; Tiwari named once). What changed: every section purpose, key point and paragraph topic sentence is now a statement about Udaypur, not about a source; small numeric differences (distances 13–16 km, 55–70 km) are planned as ranges; conflicts are framed around the object or event. The knowledge base added 15 `kb-new` items (village today: houses, census by sex and literacy, schools, Monday market, living shops, a twelve-courtyard house; the walled town and Sher Khan's mosque; the liṅga's brass sheet; and — most consequential — a two-line hill inscription tentatively assigned to the eighth century and a proposed 8th–9th-century date for Bhujariya Talab, which reframe 1.3's opening).

**After the pipeline.** The pipeline draft (4,100 words, zero source-led sentences) met the subject rule mechanically: "Udaypur…" opened up to six of eight sentences in a paragraph, and some attributions hid in passives ("dated … by Patil", "in Ganguly's hypothesis"). The detector was tightened to catch those, a sentence-opening monotony check and a near-duplicate check were added to the code checks, and a rhythm-and-sense line edit ran on every section (1.2 and 1.5 needed a second, targeted round), each kept only if no check got worse, followed by re-verification. Two hand fixes restored the distance ranges and cut a stray sentence; two PARTIAL sentences in 1.3 were narrowed by the editor after the OpenAI account ran out of credits."""
