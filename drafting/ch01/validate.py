"""Phase 3 checks, in code. Used on candidates, edited sections, the stitched chapter and the polish.

  python -I "drafting/ch01/validate.py" ch01_draft_v1.md            # full chapter report
  python -I "drafting/ch01/validate.py" draft_section_1.3.md --section 1.3

Checks:
 1 word count (bracketed IDs excluded): chapter 3,800–4,200; each section within ±15% of target
 2 citations: every bracketed ID exists in the pack ([AUTHOR] accepted and listed); every quoted string
   appears verbatim in the quote of an item cited in the same sentence (or the next sentence); no quote
   from a ⚠ item; "(translation)"-marked quotations are exempt from the verbatim test but still need an ID
 3 uncited claims: sentences with a date/number/proper noun/"according to" and no ID
 4 fabrication scan: years and proper nouns not found in the cited items' quotes/titles (sentence scope)
 5 conflicts: each outline conflict appears with both sides (keyword pairs)
Citation integrity (used to discard candidates) = checks 2a + 2b + 2c.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch01"))
ID_RE = re.compile(r"C\d\d-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}")
BRACKET = re.compile(r"\[((?:C\d\d-[A-Z0-9-]+?-\d{3}|AUTHOR)(?:\s*[;,]\s*(?:C\d\d-[A-Z0-9-]+?-\d{3}|AUTHOR))*)\]")
QUOTE_RE = re.compile(r"[\"“]([^\"”]{2,}?)[\"”](\s*\(translation\))?")
TARGETS = {"1.1": 850, "1.2": 850, "1.3": 850, "1.4": 700, "1.5": 750}
# Names the narrator may use without evidence (the book's own conventions / editor's knowledge)
ALLOW = {"udaypur", "udayapura", "chapter", "jagta", "hua", "kasba", "vijay", "manohar", "tiwari", "the", "in",
         "rajasthan", "ce", "ad", "vs", "v", "s", "a", "d", "hijra", "ah", "i", "ii"}
MONTHS = "january february march april may june july august september october november december".split()

# conflicts per section: (name, [alternatives that must each be present])
CONFLICTS = {
    "1.1": [("Bedni/Berni Mata legend", [r"Berni|Bedni|Benji", r"dancer", r"yak[sṣ]a"])],
    "1.2": [("Lūṇapasāka record date", [r"L[uū][nṇ]apas[aā]ka", r"117[123]", r"117[123].*117[123]|117[123][^.]*117[123]"]),
            ("brass cover donor", [r"Appaji", r"Bappa"]),
            ("palace founder", [r"Jah[aā]ng[iī]r", r"Mahal|palace"]),
            ("Tughluq vs Aurangzeb", [r"Tughl", r"Aurangzeb"]),
            ("inscription count", [r"\b11\b|eleven", r"hundred"])],
    "1.3": [("pre-Udayāditya settlement", [r"before (his|Udayāditya)|prior to|earlier", r"came into existence|no inscription of (?:the|an) earlier|new town|began in"])],
    "1.4": [("founding: who", [r"N[eē]maka|feudatory"]), ("founding: when", [r"1059", r"1080"]),
            ("Udayasamudra identification", [r"cannot be identified|cannot identify|unidentified|uncertain identification", r"ruins|71 acres|fields"])],
    "1.5": [("praśasti location", [r"Gwalior", r"in front of"]), ("praśasti date", [r"undated|not bear any date", r"1072|1059"]),
            ("praśasti reliability", [r"much later date|Vaidya"]),
            ("accession as working position", [r"1070", r"1058|1059", r"1080"])],
}


def strip_dia(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def skel(s):
    s = strip_dia(s).lower()
    s = s.replace("sh", "s").replace("w", "v").replace("ee", "i").replace("oo", "u").replace("h", "")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"(.)\1+", r"\1", s)
    return " ".join(s.split())


def load_pack():
    return {i["id"]: i for i in json.loads((D / "evidence_pack.json").read_text(encoding="utf-8"))}


def words(text):
    t = BRACKET.sub("", text)
    t = re.sub(r"^#.*$", "", t, flags=re.M)
    t = re.sub(r"[*_#>`]", "", t)
    return len(re.findall(r"[A-Za-zĀ-ſḀ-ỿ\u0900-\u097F0-9’'-]+", t))


def split_sections(text):
    parts = re.split(r"(?m)^(?=## 1\.\d)", text)
    out = {}
    for p in parts:
        m = re.match(r"## (1\.\d)", p)
        if m:
            out[m.group(1)] = p
    return out


def sentences(text):
    body = re.sub(r"(?m)^#.*$", "", text)
    # keep bracketed IDs with the sentence they close
    raw = re.split(r"(?<=[.!?…])(?:\s*(?:\[[^\]]+\]))*\s+(?=[A-Z“\"*(‘'])", body)
    out, buf = [], ""
    for chunk in re.split(r"(?<=[.!?”\"])\s*((?:\[[^\]]+\]\s*)+)?\s+(?=[A-Z“\"*(‘'])", body):
        if chunk is None:
            continue
        buf += (" " if buf else "") + chunk
        if not re.fullmatch(r"(?:\[[^\]]+\]\s*)+", chunk.strip()):
            out.append(buf.strip())
            buf = ""
        else:
            out[-1] = (out[-1] + " " + chunk.strip()) if out else chunk
            buf = ""
    return [s for s in out if s and not re.fullmatch(r"\s*", s)]


def ids_in(s):
    out = []
    for m in BRACKET.finditer(s):
        out += [x.strip() for x in re.split(r"[;,]", m.group(1))]
    return out


def check(text, pack, section=None):
    rep = {"invalid_ids": [], "author_uses": [], "nonverbatim_quotes": [], "warn_quotes": [],
           "uncited_claims": [], "fabrication": [], "conflicts": [], "words": {}, "word_issues": []}
    sents = sentences(text)
    # 1 words
    secs = split_sections(text) if section is None else {section: text}
    total = 0
    for k, t in secs.items():
        n = words(t)
        total += n
        rep["words"][k] = n
        if k in TARGETS and not (TARGETS[k] * 0.85 <= n <= TARGETS[k] * 1.15):
            rep["word_issues"].append(f"{k}: {n} words vs target {TARGETS[k]} (±15%)")
    rep["words"]["total"] = total
    if section is None and not (3800 <= total <= 4200):
        rep["word_issues"].append(f"total {total} words, outside 3,800–4,200")
    # 2 citations, 3 uncited, 4 fabrication
    for i, s in enumerate(sents):
        ids = ids_in(s)
        nxt = ids_in(sents[i + 1]) if i + 1 < len(sents) else []
        for x in ids:
            if x == "AUTHOR":
                rep["author_uses"].append(s[:160])
            elif x not in pack:
                rep["invalid_ids"].append(x)
        cited = [pack[x] for x in ids + nxt if x in pack]
        qtext = " ".join(" ".join(c["quote"].split()) for c in cited)
        for m in QUOTE_RE.finditer(BRACKET.sub("", s)):
            q, tr = m.group(1).strip(), m.group(2)
            if tr:
                continue
            if any("⚠" in c["flags"] for c in cited):
                rep["warn_quotes"].append(q[:80])
            frags = [f.strip(" .,;:'’") for f in re.split(r"…|\.\.\.|\[[^\]]*\]", q) if len(f.strip(" .,;:'’")) > 1]
            norm = lambda z: " ".join(z.replace("’", "'").replace("‘", "'").split())
            if not cited or not all(norm(f) in norm(qtext) for f in frags):
                rep["nonverbatim_quotes"].append({"quote": q[:120], "cited": ids})
        plain = BRACKET.sub("", s)
        has_claim = (re.search(r"\b\d{2,4}\b", plain) or re.search(r"according to", plain, re.I)
                     or re.search(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-zāīūṛṇṭḍśṣ]+", plain.strip()[1:]))
        if has_claim and not ids:
            rep["uncited_claims"].append(plain.strip()[:200])
        if ids:
            # names may come from the quote, gloss, book title, author field or mapping note (attribution
            # context: e.g. 'Krishna Deva' for Temples of India); years must come from quotes/glosses only
            src = skel(qtext + " " + " ".join(" ".join(str(c.get(k) or "") for k in ("book_title", "author", "gloss", "note"))
                                                for c in cited))
            src_digits = set(re.findall(r"\d{3,4}", qtext + " " + " ".join(c.get("gloss") or "" for c in cited)))
            for y in re.findall(r"\b(\d{3,4})\b", plain):
                if y not in src_digits:
                    rep["fabrication"].append(f"year/number {y} not in cited items: {plain[:120]}")
            for name in set(re.findall(r"(?<!^)(?<![.!?]\s)\b([A-Z][\wāīūṛṇṭḍśṣṅñ’'-]{2,}(?:\s+[A-Z][\wāīūṛṇṭḍśṣṅñ’'-]{2,})*)", plain)):
                for w in name.split():
                    w = re.sub(r"[’']s$", "", w)          # possessive: Udaypur’s -> Udaypur
                    sk = skel(w)
                    if not sk or sk in {skel(a) for a in ALLOW} or w.lower() in MONTHS:
                        continue
                    if sk not in src:
                        rep["fabrication"].append(f"name '{w}' not in cited items: {plain[:120]}")
    # 5 conflicts
    for k in ([section] if section else list(CONFLICTS)):
        t = secs.get(k, text if section else "")
        for name, pats in CONFLICTS.get(k, []):
            ok = all(re.search(p, t, re.I | re.S) for p in pats)
            rep["conflicts"].append({"section": k, "conflict": name, "present": bool(ok)})
    rep["integrity_ok"] = not (rep["invalid_ids"] or rep["nonverbatim_quotes"] or rep["warn_quotes"])
    rep["fabrication"] = sorted(set(rep["fabrication"]))
    return rep


def summary(rep):
    return {k: (len(v) if isinstance(v, list) else v) for k, v in rep.items() if k != "conflicts"} | {
        "conflicts_missing": [c["conflict"] for c in rep["conflicts"] if not c["present"]]}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    f = Path(sys.argv[1])
    f = f if f.is_absolute() else D / f
    sec = sys.argv[sys.argv.index("--section") + 1] if "--section" in sys.argv else None
    r = check(f.read_text(encoding="utf-8"), load_pack(), sec)
    print(json.dumps(r, ensure_ascii=False, indent=1))
