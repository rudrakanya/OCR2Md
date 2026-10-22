"""Shape diagnostics for one section of prose (reported, never enforced): reader-facing footnote density (per-bracket notes
for old drafts; consolidated notes for house-voice drafts), people-as-subject rate, paragraph and sentence length
spread, and the frequency of 'AI-shaped' constructions.

  import metrics; metrics.section_stats(text, consolidated=True)
"""
import re
import statistics as stt

NOTE = re.compile(r"\{\{note:.*?\}\}", re.S)
BR = re.compile(r"\[(?:C\d\d-[A-Z0-9-]+?-\d{3}|AUTHOR)(?:\s*[;,]\s*(?:C\d\d-[A-Z0-9-]+?-\d{3}|AUTHOR))*\]")
INT = re.compile(r"\[INT(?::[a-z]+)?\]")
PEOPLE = (r"udayāditya|udayaditya|bhoja|bhoj|jayasi[mṃ]ha|karṇa|karna|bhīma|bhima|naravarman|yaśovarman|yasovarman|jayavarman|lakṣmīvarman|"
          r"lakshmivarman|devapāla|devapala|lūṇapasāka|lunapasaka|rājyapāla|madanavarman|muhammad|aurangzeb|sher khan|tiwari|vijay|cunningham|beglar|garde|"
          r"bühler|kielhorn|ganguly|khande|bappa|appaji|the king|kings?|the founder|his successor|the sultan|sultans|governors?|residents|villagers|"
          r"pilgrims|priests|patrons|builders|masons|craftsmen|farmers|cultivators|quarrymen|people|the paramāras|the paramaras|the chaulukyas|"
          r"the caulukyas|the candellas|the chandellas|the kalachuris|the scindias|he|they|his enemies|the dynasty|the nēmaka|scholars?|archaeologists?|ain-ul-mulk|mahlak|alauddin|hoshang|dilawar")
SUBJ = re.compile(rf"^(?:in [^,]{{1,60}}, |when [^,]{{1,80}}, |by [^,]{{1,40}}, |after [^,]{{1,60}}, |under [^,]{{1,60}}, )?(?:{PEOPLE})\b", re.I)
TEMPLATES = {
    "not X but Y": r"\bnot\b[^.;:]{1,60}?\bbut\b",
    "both X and Y": r"\bboth\b[^.;:]{1,60}?\band\b",
    "the same X that": r"\bthe same\b[^.;:]{1,40}?\b(?:that|which|who)\b",
    "colon in sentence": r"[a-z]: [a-z]",
    "this/that is why; mattered": r"\b(?:this|that) is why\b|\bmattered\b|\bthe significance\b|\bthe result was\b",
}


def _plain(t):
    return INT.sub("", BR.sub("", NOTE.sub("", t)))


def sentences(t):
    t = re.sub(r"(?m)^#.*$", "", _plain(t))
    return [s.strip() for s in re.split(r"(?<=[.!?”])\s+(?=[A-Z‘“\"'*(])", t) if len(s.split()) > 2]


def paragraphs(t):
    return [p for p in re.split(r"\n\s*\n", re.sub(r"(?m)^#.*$", "", t)) if len(_plain(p).split()) > 15]


def consolidated_notes(p):
    """notes the reader sees after consolidation: one per paragraph cluster (a {{note}} closes a cluster)"""
    n, rest = 0, p
    for m in NOTE.finditer(p):
        n += 1
    tail = NOTE.split(p)[-1]
    if BR.search(tail):
        n += 1
    return n


def section_stats(text, consolidated):
    paras = paragraphs(text)
    pw = [len(_plain(p).split()) for p in paras]
    ss = sentences(text)
    sl = [len(s.split()) for s in ss]
    words = sum(pw)
    notes = sum(consolidated_notes(p) for p in paras) if consolidated else len(BR.findall(text)) + len(NOTE.findall(text))
    people = sum(bool(SUBJ.match(s.lstrip("*_“\"‘("))) for s in ss)
    out = {"words": words, "paragraphs": len(paras), "notes": notes,
           "notes_per_paragraph": round(notes / len(paras), 1) if paras else 0,
           "words_per_note": round(words / notes) if notes else None,
           "people_subject_pct": round(100 * people / len(ss)) if ss else 0,
           "para_words_mean": round(stt.mean(pw)) if pw else 0, "para_words_sd": round(stt.pstdev(pw)) if pw else 0,
           "para_words_range": f"{min(pw)}–{max(pw)}" if pw else "",
           "sentences": len(ss), "sent_words_mean": round(stt.mean(sl), 1) if sl else 0, "sent_words_sd": round(stt.pstdev(sl), 1) if sl else 0,
           "sent_le10_pct": round(100 * sum(x <= 10 for x in sl) / len(sl)) if sl else 0,
           "sent_ge35_pct": round(100 * sum(x >= 35 for x in sl) / len(sl)) if sl else 0}
    out["templates_per_1000w"] = {k: round(1000 * sum(len(re.findall(p, s, re.I)) for s in ss) / words, 1) for k, p in TEMPLATES.items()} if words else {}
    return out
