"""Citation-support helpers for the shared toolkit: cited_sentences, item_text, rule_checks, VERIFY_SYS, FIX_SYS, RANK."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cfg import C  # noqa: E402
import validate as va  # noqa: E402

RANK = {"SUPPORTED": 3, "PARTIAL": 2, "MISREPRESENTED": 1, "UNSUPPORTED": 0}
SUPERLATIVE = re.compile(r"\b(finest|greatest|grandest|largest|best|most\s+\w+|unrivall?ed|supreme|unique|"
                         r"unparalleled|matchless|peerless|incomparable|magnificent|\w+est)\b", re.I)
NOT_SUPER = {"earliest", "latest", "nearest", "west", "interest", "honest", "forest", "harvest", "rest", "test", "contest",
             "request", "suggest", "protest", "invest", "manifest", "modest", "guest", "chest", "quest", "southwest", "northwest",
             "almost", "most", "eldest", "oldest", "smallest", "longest", "highest", "lowest", "biggest"}
ATTRIB = re.compile(r"\b(call(s|ed)?|describ(es|ed)|wr(ote|ites)|according to|in the words of|judg(es|ed)|rank(s|ed)|"
                    r"consider(s|ed)|deem(s|ed)|say(s)?|said|holds?|claims?|records?|reports?|states?|gives?|finds?|notes?|"
                    r"identif(?:y|ies|ied)|counts?|tradition|praised|praises)\b", re.I)
CONVENTIONS = ("EDITORIAL CONVENTIONS (supplied by the editor, not evidence claims — treat as supported and never remove): "
               "the author of *Jagta Hua Kasba* is Vijay Manohar Tiwari ('Tiwari'); the district Gazetteer is the 1979 compilation; "
               "Udayāditya's accession c. 1070 is the book's working position. Book titles in Devanagari are never written in the prose.\n\n")

VERIFY_SYS = """You are a skeptical fact-checker. For each numbered sentence of a non-fiction chapter, compare it ONLY with the evidence items it cites (quotes, English renderings; mapping notes only tell you who is speaking).
Verdicts:
- SUPPORTED: the cited items state this (paraphrase is fine; a range that spans two cited figures is fine; a fact stated without naming its source is fine — sources sit in the footnotes).
- PARTIAL: the sentence goes beyond the evidence — an added date or number, stronger wording, certainty the source does not have, or two claims merged so that one is unsupported.
- UNSUPPORTED: the cited items do not say this.
- MISREPRESENTED: a real disagreement between sources is presented as settled, or a claim is attributed to the wrong source/person, or a tradition/testimony/panegyric is presented as established fact.
Where a sentence names a source, it must be the right one. Purely transitional phrasing needs no support. Be strict about numbers, dates, names and certainty.
Return ONLY JSON: {"results": [{"sid": "X.Y-01", "verdict": "SUPPORTED|PARTIAL|UNSUPPORTED|MISREPRESENTED", "evidence": "exact short phrase from the cited item that supports or contradicts it (≤ 20 words)", "fix": "one-line fix if not SUPPORTED, else empty"}]}"""

FIX_SYS = """You correct flagged sentences in a non-fiction chapter about Udaypur so that each is supported by its cited evidence.
For each flagged sentence, return a replacement that: uses only facts in the cited items; keeps or corrects the bracketed evidence IDs (only IDs from the supplied evidence); keeps quotations verbatim from an item's QUOTE; presents real source disagreements as disagreements about the subject ("X is dated variously to …"); narrows an over-strong claim to what the evidence supports, or marks a tradition as tradition, or cuts it.
Keep the place as the grammatical subject: do NOT turn sentences into "[source] says/records/describes…" — name a source in the text only if its identity matters (competing datings, tradition vs inscription, eyewitness). Never write "the author" or "according to [title]". Never add new facts. Keep the sentence's role in its paragraph and British/Indian English with diacritics.
Return ONLY JSON: {"replacements": [{"sid": "X.Y-01", "new": "replacement sentence with [IDs]" or "CUT", "note": "what changed"}]}"""


def cited_sentences(text):
    out = {}
    for sec, part in va.split_sections(text).items():
        rows = []
        for s in va.sentences(part):
            ids = [i for i in va.ids_in(s) if i != "AUTHOR"]
            if ids:
                rows.append({"sid": f"{sec}-{len(rows) + 1:02d}", "sentence": s.strip(), "ids": ids})
        out[sec] = rows
    return out


def item_text(i):
    flags = [f for f in i["flags"] if not f.startswith("also")]
    s = f"[{i['id']}] {i['book_title']} · {i['page']}" + (f" · {', '.join(flags)}" if flags else "") + \
        f"\n  QUOTE: {' '.join(i['quote'].split())}"
    if i.get("gloss"):
        s += f"\n  ENGLISH RENDERING: {i['gloss']}"
    if i.get("note"):
        s += f"\n  MAPPING NOTE (attribution context only): {i['note']}"
    return s


def rule_checks(text, P, sent_map):
    """code rules; returns list of {sid?, sec, rule, detail}"""
    fails = []
    for sec, rows in sent_map.items():
        for r in rows:
            plain = va.BRACKET.sub("", r["sentence"])
            gaz = [x for x in r["ids"] if x in P and P[x]["book_code"] == "GAZ"]
            yrs = [int(y) for y in re.findall(r"(?<![\d,.])\b(\d{3,4})\b(?![.,]\d)", plain)
                   if not re.search(y + r"\s*(?:mm|km|m\b|metres?|ha|hect|°|per)", plain)]
            if getattr(C, "GAZ_MODERN_ONLY", True) and gaz and len(gaz) == len(r["ids"]) and any(y < 1700 for y in yrs):
                fails.append({"sid": r["sid"], "sec": sec, "rule": "Gazetteer used for a pre-modern date",
                              "detail": "the Gazetteer is for the modern setting — cite a dynastic/epigraphic/archaeological item, attribute, or cut"})
            unq = re.sub(r"[\"“][^\"”]*[\"”]", "", plain)
            for m in SUPERLATIVE.finditer(unq):
                w = m.group(0).lower()
                if w in ("most likely", "most often", "most frequently", "most commonly"):
                    continue
                if w.startswith("most ") and (w.split()[1] in ("of", "part", "parts") or (w.endswith("s") and not w.endswith(("ous", "ss")))):
                    continue
                if w in NOT_SUPER or (w.endswith("est") and not re.match(r"(finest|greatest|grandest|largest|best|richest|purest|noblest|loftiest|tallest)$", w)):
                    continue
                if not ATTRIB.search(unq):
                    fails.append({"sid": r["sid"], "sec": sec, "rule": "narrator superlative", "detail": f"'{m.group(0)}' outside quotation marks and unattributed"})
            approx = [x for x in r["ids"] if x in P and "≈ (Hindi original)" in P[x]["flags"]]
            if approx and len(approx) == len(r["ids"]) and re.search(r"\b\d[\d,.]*\b", plain) \
                    and not re.search(r"Tiwari|Jagta|resident|told|tradition|remember|recall|local", plain, re.I):
                fails.append({"sid": r["sid"], "sec": sec, "rule": "precise claim on approximate Jagta page",
                              "detail": "a number/date resting only on ≈-paged Jagta Hua Kasba items, not marked as testimony"})
            if re.search(r"\bthe author\b", plain, re.I):
                fails.append({"sid": r["sid"], "sec": sec, "rule": "'the author'", "detail": "banned construction"})
    if re.search(r"[ऀ-ॿ]", va.BRACKET.sub("", text)):
        fails.append({"sec": "chapter", "rule": "Devanagari in prose", "detail": "use the English title / a paraphrase"})
    if re.search(r"JAGTA", text) and not re.search(r"Vijay Manohar Tiwari", text) and getattr(C, "TIWARI_FULL_NAME", True):
        fails.append({"sec": "chapter", "rule": "Tiwari", "detail": "Jagta Hua Kasba cited but Vijay Manohar Tiwari never named in full"})
    if len(re.findall(r"Vijay Manohar Tiwari", text)) > 1:
        fails.append({"sec": "chapter", "rule": "Tiwari", "detail": "full name used more than once"})
    if re.search(r"Udaipur(?! in Rajasthan| of Rajasthan|,? Rajasthan)", va.BRACKET.sub("", re.sub(r"[\"“][^\"”]*[\"”]", "", text))):
        fails.append({"sec": "chapter", "rule": "spelling", "detail": "'Udaipur' used for Udaypur (allowed only for Udaipur in Rajasthan)"})
    if hasattr(C, "extra_rules"):
        fails += C.extra_rules(text, P, sent_map)
    rep = va.check(text, P)
    for c in rep["conflicts"]:
        if not c["present"]:
            fails.append({"sec": c["section"], "rule": "conflict missing", "detail": c["conflict"]})
    for k in rep.get("subject_fail", []):
        fails.append({"sec": k, "rule": "source-subject ratio", "detail": f"{rep['subject'][k]['flagged']}/{rep['subject'][k]['sentences']} source-led sentences; worst paragraph {rep['subject'][k]['worst_paragraph']}"})
    return fails
