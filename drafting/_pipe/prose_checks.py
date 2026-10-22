"""Prose checks (user brief, 2026-10-15). Code only, no API.

  agent_nouns(text, P)        quarrymen/masons/builders/... as actors with no cited item containing the noun → verifier warning
  narrator_terms(text)        period terms ("Mohammedan", ...) outside verbatim quotation marks → problem (use "Muslim")
  passive_runs(text)          three or more consecutive sentences of the same grammatical shape → warning
  style_mechanics(text)       -ize forms, straight quotes, numerals under 100, a word repeated within two sentences,
                              every sentence of a paragraph opening the same way → warnings
  ai_shape(text)              per-1,000-word counts: "not X but Y", triplets, colon reveals, paragraph-final aphorisms,
                              "This mattered because…", symmetrical contrasts → warnings
  report(text, P)             all of the above as one dict

  python -I prose_checks.py <draft.md> [...]   (uses the active UDAY_CFG pack if set)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ID = r"C\d\d-[A-Z0-9-]+?-\d{3}"
BR = re.compile(rf"\[(?:{ID}|AUTHOR)(?:\s*[;,]\s*(?:{ID}|AUTHOR))*\]")
NOTE = re.compile(r"\{\{note:.*?\}\}", re.S)
INT = re.compile(r"\[INT(?::[a-z]+)?\]")
QUOTED = re.compile(r"[\"“][^\"”]{1,600}[\"”]")

AGENTS = r"quarrymen|quarryman|quarry-workers|stonecutters|stone-cutters|masons|mason|builders|artisans|artisan|labourers|labourer|workmen|workers|craftsmen|craftsman|engineers"
AGENT_RE = re.compile(rf"\b({AGENTS})\b", re.I)
# narrator-voice terms: allowed only inside verbatim quotation (style sheet)
NARRATOR = {r"\bMohammedans?\b|\bMuhammadans?\b|\bMahomedans?\b": "Muslim", r"\bHindoos?\b": "Hindu",
            r"\bnatives?\b(?= (?:of|chief|rulers?|people))": "local / named people", r"\baboriginals?\b": "name the people (e.g. Gond)"}
IZE_OK = {"size", "seize", "prize", "capsize", "baize", "maize", "assize"}
SPELLED_EXCEPT = re.compile(r"\d+(?:\.\d+)?\s*(?:km|m|cm|mm|ha|per cent|%|feet|ft|inches|miles|kg|metres?|kilomet\w*|hectares?|acres?|°)|\b1[0-9]{3}\b|\b[0-9]{3,}\b")


def _plain(t):
    return re.sub(r"[ \t]{2,}", " ", INT.sub("", BR.sub("", NOTE.sub("", t))))


def paragraphs(t):
    return [p for p in re.split(r"\n\s*\n", t) if p.strip() and not p.lstrip().startswith("#")]


def sentences(t):
    return [s.strip() for s in re.split(r"(?<=[.!?”])\s+(?=[A-Z‘“\"'*(])", _plain(t)) if len(s.split()) > 2]


def _cited_text(sent_raw, P):
    return " ".join((P[i].get("quote", "") + " " + (P[i].get("gloss") or "")) for b in BR.finditer(sent_raw)
                    for i in re.findall(ID, b.group(0)) if i in P)


def agent_nouns(text, P):
    """an agent noun in the narrator's voice that no item cited in its paragraph contains"""
    out = []
    for para in paragraphs(NOTE.sub("", text)):
        cited = _cited_text(para, P).lower() if P else ""
        for s in re.split(r"(?<=[.!?])\s+", para):
            plain = QUOTED.sub("", _plain(s))
            for m in AGENT_RE.finditer(plain):
                w = m.group(1).lower()
                stem = w.rstrip("s").replace("men", "m").replace("man", "m")
                if w not in cited and stem not in cited:
                    out.append({"noun": m.group(1), "sentence": plain.strip()[:220]})
    return out


def narrator_terms(text):
    out = []
    for s in sentences(text):
        bare = QUOTED.sub("", s)
        for pat, use in NARRATOR.items():
            for m in re.finditer(pat, bare, re.I):
                out.append({"term": m.group(0), "use": use, "sentence": s[:220]})
    return out


def _shape(s):
    """'hedged-passive' = a passive (adverbs allowed between auxiliary and participle) or a modal hedge (may/might/could + verb)"""
    low = s.lower()
    if re.search(r"\b(?:provisionally|tentative(?:ly)?|proposed|assigned|interpreted|attributed|believed|read as|ascribed)\b", low) \
            or re.search(r"\b(?:is|are|was|were|has|have|had|be|been)(?:\s+\w+ly|\s+also|\s+not|\s+been){0,3}\s+\w+(?:ed|en|wn|lt|ught|id|ead)\b", low) or re.search(r"\b(?:may|might|could)\s+(?:\w+ly\s+)?(?:have\s+)?\w+", low):
        return ("hedged-passive", "")
    return ("active", "")


def passive_runs(text, n=3):
    out = []
    for para in paragraphs(text):
        ss = sentences(para)
        sh = [_shape(s) for s in ss]
        i = 0
        while i < len(ss):
            j = i
            while j + 1 < len(ss) and sh[j + 1] == sh[i] and sh[i][0] == "hedged-passive":
                j += 1
            if j - i + 1 >= n:
                out.append({"run": j - i + 1, "shape": sh[i][0], "first": ss[i][:140]})
            i = j + 1
    return out


def style_mechanics(text):
    out = []
    plain = _plain(text)
    for m in re.finditer(r"\b(\w+?)(iz)(e|es|ed|ing|ation|ations)\b", plain):
        w = m.group(0).lower()
        if w not in IZE_OK and not w.startswith(("siz", "seiz", "priz", "maiz")):
            out.append(f"-ize form: {m.group(0)}")
    if re.search(r"(?<![=\w])\"[A-Za-z]", plain):
        out.append("straight double quotation marks (use curly “ ”)")
    bare = SPELLED_EXCEPT.sub("", QUOTED.sub("", plain))
    for m in re.finditer(r"(?<![\d.,–-])\b([1-9][0-9]?)\b(?![\d.,–-])", bare):
        out.append(f"numeral under 100 (spell out unless a measurement, date or percentage): {bare[max(0, m.start() - 30):m.end() + 20].strip()}")
    ss = sentences(text)
    freq = {}
    for w in plain.lower().split():
        freq[w.strip(",.;:()")] = freq.get(w.strip(",.;:()"), 0) + 1
    stop = set("the a an and of in on to at by for with from as was were is are its it his her their that this which be been had has have not but or".split())
    for k in range(1, len(ss)):
        prev = {w.lower().strip(",.;:()") for w in ss[k - 1].split() + (ss[k - 2].split() if k > 1 else [])}
        rep = [w for w in {w.lower().strip(",.;:()") for w in ss[k].split()} if len(w) > 6 and w not in stop and w in prev
               and not w[0].isupper() and freq.get(w, 0) < 4]      # a topic word (village, district) recurs by design
        for w in rep[:1]:
            out.append(f"word repeated within two sentences: '{w}': {ss[k][:100]}")
    for para in paragraphs(text):
        ps = sentences(para)
        if len(ps) >= 3 and len({s.split()[0].lower() for s in ps}) == 1:
            out.append(f"every sentence opens with '{ps[0].split()[0]}': {ps[0][:80]}")
    return out


AI = {
    "not X but Y": r"\bnot\b[^.;:]{1,60}?\bbut\b",
    "triplet": r"\b\w+(?: \w+)?, \w+(?: \w+)?,? and \w+(?: \w+)?[.;]",
    "colon reveal": r"[a-z]: [a-z]",
    "this mattered because": r"\b(?:this|that|it) mattered\b|\bthis is why\b|\bthe significance\b|\bwhat mattered\b",
    "symmetrical contrast": r"\b(?:less|more) (?:a|an|the)? ?\w+ than (?:a|an|the)? ?\w+\b|\bas much (?:a|an)? ?\w+ as\b|\bwhere [^.]{3,40}, [^.]{3,40} (?:did|was|is)\b",
}


def ai_shape(text):
    plain = _plain(text)
    words = max(1, len(plain.split()))
    ss = sentences(text)
    out = {k: round(1000 * sum(len(re.findall(p, s)) for s in ss) / words, 1) for k, p in AI.items()}
    fin = 0
    for para in paragraphs(text):
        ps = sentences(para)
        if ps and not BR.search(re.split(r"(?<=[.!?])\s+", para.strip())[-1]) and len(ps[-1].split()) <= 18:
            fin += 1          # an uncited short closing sentence: the aphorism shape
    out["paragraph-final aphorism"] = round(1000 * fin / words, 1)
    return out


MEASURE = re.compile(r"\b\d+(?:\.\d+)?\s*(?:km|kilomet\w*|m\b|metres?|feet|ft|miles?|hectares?|acres?|per cent|%)|\b\d{3,4}\b(?:\s*(?:CE|BCE|AD|BC))?|\b(?:V\.S\.|Saṃvat|Samvat)\s*\d+", re.I)


def testimony_measures(text, P):
    """a sentence with a measurement/date whose only cited support is testimony or tradition (JAGTA items)"""
    out = []
    for para in paragraphs(NOTE.sub("", text)):
        for s in re.split(r"(?<=[.!?\]])\s+(?=[A-Z‘“\"'*(])", para):
            ids = [i for b in BR.finditer(s) for i in re.findall(ID, b.group(0))]
            if not ids:
                continue
            if all((P.get(i, {}).get("book_code", "") or i).startswith("JAGTA") or "-JAGTA-" in i for i in ids):
                plain = _plain(s)
                if MEASURE.search(QUOTED.sub("", plain)):
                    out.append(plain.strip()[:200])
    return out


STOPW = set("the a an and of in on to at by for with from as was were is are its it his her their that this which be been had has have not but or into than also".split())


def _content(s):
    return {w for w in re.findall(r"[a-zāīūṛṃḥśṣṇṭḍñ]+", _plain(s).lower()) if len(w) > 2 and w not in STOPW}


def duplicates_other(new_sentence, section_text, threshold=0.6):
    """True if new_sentence shares >= threshold of its content words with any other sentence of the section"""
    a = _content(new_sentence)
    if len(a) < 4:
        return False
    ss = sentences(section_text)
    for k, s in enumerate(ss):
        b = _content(s)
        if b and len(a & b) / len(a) >= threshold:
            return True
        if k + 1 < len(ss) and len(a & (b | _content(ss[k + 1]))) / len(a) >= 0.65:
            return True                     # a fix that merges two sentences the section already has
    return False


def dynasty_spelling(text):
    """D1 (user, 16 Oct): IAST dynasty names (Kalacuri, Candella, Caulukya, Cālukya) outside verbatim quotations."""
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_tools"))
    import dynasty_spelling as ds
    return [f"non-IAST dynasty name outside quotation: {w}" for w, pos, q in ds.scan(text) if not q]


def report(text, P=None):
    return {"agent_nouns": agent_nouns(text, P or {}), "narrator_terms": narrator_terms(text), "passive_runs": passive_runs(text),
            "testimony_measures": testimony_measures(text, P or {}), "dynasty_spelling": dynasty_spelling(text),
            "style": style_mechanics(text), "ai_shape_per_1000w": ai_shape(text)}


if __name__ == "__main__":
    import json
    sys.stdout.reconfigure(encoding="utf-8")
    P = {}
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        import validate as va
        P = va.load_pack()
    except SystemExit:
        pass
    for f in sys.argv[1:]:
        print("==", f)
        print(json.dumps(report(Path(f).read_text(encoding="utf-8"), P), ensure_ascii=False, indent=1))
