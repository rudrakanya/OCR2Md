"""Code checks for the shared toolkit (active chapter from UDAY_CFG).

  python -I drafting/_pipe/validate.py <draft.md> [--section 3.2]

 1 words (bracketed IDs excluded): sections 90–110% of the outline target; chapter within cfg WMIN–WMAX
 2 citations: every ID exists; every quotation verbatim in an item cited in the same (or next) sentence; no quote from ⚠
 3 uncited claims: sentences with a number / proper noun / "according to" and no ID
 4 fabrication scan: years/numbers and proper nouns not found in the cited items (quote, gloss, title, author, note)
 5 conflicts: each configured conflict appears with all its sides (regex sets)
 6 source-subject ratio (subject.py): sentences whose subject or main clause is a source/author; a section fails
   at > 10% flagged sentences or > 1 flagged sentence in any paragraph
Citation integrity (used to discard candidates) = 2.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cfg import C  # noqa: E402
import subject as sj  # noqa: E402

PFX = str(C.CH)
ID_RE = re.compile(r"C\d\d-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}")
BRACKET = re.compile(r"\[((?:C\d\d-[A-Z0-9-]+?-\d{3}|AUTHOR)(?:\s*[;,]\s*(?:C\d\d-[A-Z0-9-]+?-\d{3}|AUTHOR))*)\]")
QUOTE_RE = re.compile(r"[\"“]([^\"”]{2,}?)[\"”](\s*\(translation\))?")
ALLOW = {"udaypur", "udayapura", "chapter", "jagta", "hua", "kasba", "vijay", "manohar", "tiwari", "the", "in",
         "rajasthan", "ce", "ad", "bce", "vs", "v", "s", "a", "d", "hijra", "ah", "i", "ii", "iii",
         "gazetteer", "district", "geo", "heritage", "betwa", "vidisha", "malwa", "km", "mm", "msl", "c", "india", "central",
         "madhya", "pradesh"} | {w.lower() for w in getattr(C, "ALLOW_EXTRA", [])}
MONTHS = "january february march april may june july august september october november december".split()


def strip_dia(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def skel(s):
    s = strip_dia(s).lower()
    s = s.replace("sh", "s").replace("w", "v").replace("ee", "i").replace("oo", "u").replace("h", "")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"(.)\1+", r"\1", s)
    return " ".join(s.split())


ALLOW_SK = {skel(a) for a in ALLOW} | {skel(a) for a in ("Era", "Mothers", "Seven", "Sea", "Arabian", "Hindu", "Hindus", "Buddhist", "Buddhists", "Jain", "Jaina", "Brahmanical", "Mauryan", "Vaiṣṇava", "Śaiva", "Muslim", "Muslims")}


def cons(s):
    """consonant skeleton for transliteration variants (Nṛsiṃha ~ Nrisimha, Pratiṣṭhāna ~ Pratisthan)"""
    return re.sub(r"[aeiouy\s]", "", skel(s))


def load_pack():
    return {i["id"]: i for i in json.loads(C.PACK.read_text(encoding="utf-8"))}


def load_outline():
    text = C.OUTLINE.read_text(encoding="utf-8")
    parts = re.split(rf"\n(?=## {PFX}\.\d+)", text)
    secs = {}
    for p in parts[1:]:
        k = re.match(rf"## ({PFX}\.\d+)", p).group(1)
        secs[k] = re.split(r"\n## (?:Word targets|Self-review)", p)[0].strip()
    _tw = lambda s: re.search(r"(\d[\d,]*)\s*w\b", s.split("\n", 1)[0])
    # NO_LENGTH (user, 17 Oct 2026): no word targets; a unit is as long as its evidence carries
    targets = {k: (int(_tw(secs[k]).group(1).replace(",", "")) if _tw(secs[k]) and not getattr(C, "NO_LENGTH", False) else None)
               for k in secs}
    titles = {k: re.match(rf"## ({PFX}\.\d+ [^*\n]+?)\s*\*\(", secs[k]).group(1).strip() for k in secs}
    return text, secs, targets, titles


TARGETS = load_outline()[2] if C.OUTLINE.exists() else {}
HOUSE = getattr(C, "HOUSE_VOICE", False)        # editor-in-chief audit, approved 2026-10-14


NOTE_RE = re.compile(r"\{\{note:\s*(.*?)\}\}", re.S)
INT = "[INT]"                                   # legacy plain marker (still recognised)
INT_FUNCS = ("cause", "consequence", "comparison", "tension", "thesis")
INT_RE = re.compile(r"\[INT(?::(cause|consequence|comparison|tension|thesis))?\]")


def is_int(s):
    return bool(INT_RE.search(s))


def int_func(s):
    m = INT_RE.search(s)
    return (m.group(1) or "") if m else ""


def strip_int(s):
    return INT_RE.sub("", s)
GENERIC = re.compile(r"\b(rich heritage|stands as a reminder|speaks volumes|a testament|testament to|shaped the destiny|rich tapestry|"
                     r"bears? (?:silent )?witness|living legacy|glorious past|timeless|hidden gem|steeped in|stands as)\b", re.I)


def strip_notes(text):
    """{{note: TEXT [IDS]}} -> ' [IDS]' for main-text checks (the note's citations stay attached to its sentence)"""
    def rep(m):
        ids = ids_in(m.group(1))
        return (" [" + "; ".join(ids) + "]") if ids else ""
    return NOTE_RE.sub(rep, text)


def notes_in(text):
    return [m.group(1).strip() for m in NOTE_RE.finditer(text)]


def clean(s):
    return strip_int(BRACKET.sub("", s)).strip()


def words(text):
    t = strip_int(NOTE_RE.sub("", text))
    t = BRACKET.sub("", t)
    t = re.sub(r"^#.*$", "", t, flags=re.M)
    t = re.sub(r"[*_#>`]", "", t)
    return len(re.findall(r"[A-Za-zĀ-ſḀ-ỿऀ-ॿ0-9’'-]+", t))


def split_sections(text):
    out = {}
    for p in re.split(rf"(?m)^(?=## {PFX}\.\d+)", text):
        m = re.match(rf"## ({PFX}\.\d+)", p)
        if m:
            out[m.group(1)] = p
    return out


def sentences(text):
    body = re.sub(r"(?m)^#.*$", "", text)
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


def paragraphs(text):
    return [p for p in re.split(r"\n\s*\n", re.sub(r"(?m)^#.*$", "", text)) if p.strip()]


def ids_in(s):
    out = []
    for m in BRACKET.finditer(s):
        out += [x.strip() for x in re.split(r"[;,]", m.group(1))]
    return out


def subject_report(text):
    """per section: flagged sentences, ratio, worst paragraph count, pass/fail"""
    out = {}
    for k, t in (split_sections(text) or {"_": text}).items():
        n_s, flagged, worst = 0, [], 0
        for p in paragraphs(t):
            c = 0
            for s in sentences(p):
                n_s += 1
                why = sj.source_led(BRACKET.sub("", s))
                if why:
                    c += 1
                    flagged.append({"sentence": BRACKET.sub("", s).strip()[:220], "why": why})
            worst = max(worst, c)
        ratio = len(flagged) / n_s if n_s else 0
        out[k] = {"sentences": n_s, "flagged": len(flagged), "ratio": round(ratio, 3), "worst_paragraph": worst,
                  "pass": ratio <= 0.10 and worst <= 1, "detail": flagged}
    return out


def _opening(s):
    w = re.findall(r"[A-Za-zĀ-ſḀ-ỿ’'-]+", re.sub(r"^[*_“\"'(]+", "", s))[:2]
    if not w:
        return ""
    w0 = re.sub(r"[’']s$", "", w[0]).lower()
    return (w0 + " " + w[1].lower()) if w0 in ("the", "its", "a", "an", "in", "at", "on", "this", "these") and len(w) > 1 else w0


def monotony_report(text):
    """sentence-opening monotony: paragraphs where ≥ 3 sentences open alike; sections where > 20% open with 'Udaypur'"""
    out = []
    for k, t in (split_sections(text) or {"_": text}).items():
        n = u = 0
        for i, p in enumerate(paragraphs(t), 1):
            ops = [_opening(BRACKET.sub("", s)) for s in sentences(p)]
            n += len(ops)
            u += sum(o == "udaypur" for o in ops)
            for o in set(ops):
                if o and ops.count(o) >= 3:
                    out.append(f"{k} paragraph {i}: {ops.count(o)} of {len(ops)} sentences open with '{o}' — vary the openings (the temple, the hill, its lanes, the tank, a pronoun, a time phrase…)")
        if n and u / n > 0.20:
            out.append(f"{k}: {u} of {n} sentences open with 'Udaypur' — keep the place as subject but vary how it is named")
    return out


STOP = set("the and that with from into this were was its their which have been also there these those than then thus about after before under over between within while where when whose".split())


def _content(s):
    return {w for w in re.findall(r"[a-zāīūṛṇṭḍśṣṅñ]{4,}", strip_dia(BRACKET.sub("", s)).lower()) if w not in STOP}


def duplicates_report(text):
    """near-duplicate sentences within a section (content-word Jaccard ≥ 0.5, or ≥ 0.4 with a shared citation)"""
    out = []
    for k, t in (split_sections(text) or {"_": text}).items():
        ss = sentences(t)
        cw = [_content(s) for s in ss]
        ids = [set(ids_in(s)) for s in ss]
        for i in range(len(ss)):
            for j in range(i + 1, len(ss)):
                a, b = cw[i], cw[j]
                if len(a) < 4 or len(b) < 4:
                    continue
                jac = len(a & b) / len(a | b)
                if jac >= 0.45 or (jac >= 0.3 and ids[i] and ids[i] == ids[j]):
                    out.append(f"{k}: restates an earlier sentence — keep one: «{BRACKET.sub('', ss[i]).strip()[:120]}» / «{BRACKET.sub('', ss[j]).strip()[:120]}»")
    return out


_NGRAMS = None


def _sample_ngrams():
    global _NGRAMS
    if _NGRAMS is None:
        _NGRAMS = set()
        sp = getattr(C, "SAMPLE_TXT", None)
        if sp and Path(sp).exists():
            w = re.findall(r"[a-z0-9’']+", Path(sp).read_text(encoding="utf-8").lower())
            _NGRAMS = {tuple(w[k:k + 6]) for k in range(len(w) - 5)}
    return _NGRAMS


def ngram_hits(sentence):
    ng = _sample_ngrams()
    if not ng:
        return []
    w = re.findall(r"[a-z0-9’']+", clean(sentence).lower())
    return [" ".join(w[k:k + 6]) for k in range(len(w) - 5) if tuple(w[k:k + 6]) in ng]


def _fact_scan(plain, cited, rep, label=""):
    """years/numbers and proper nouns in `plain` must occur in the cited items (quote, gloss, title, author, note)"""
    qtext = " ".join(" ".join(c["quote"].split()) for c in cited)
    src = skel(qtext + " " + " ".join(" ".join(str(c.get(k) or "") for k in ("book_title", "author", "gloss", "note")) for c in cited))
    digits_src = re.sub(r"(?<=\d),(?=\d{3}\b)", "", qtext + " " + " ".join(c.get("gloss") or "" for c in cited))
    src_digits = set(re.findall(r"\d{3,4}", digits_src))
    if any(c["book_code"] == "GAZ" for c in cited):
        src_digits.add("1979")          # canon: the Gazetteer is date-stamped as the 1979 compilation
    plain_n = re.sub(r"(?<=\d),(?=\d{3}\b)", "", plain)
    for y in re.findall(r"\b(\d{3,4})\b", plain_n):
        if y not in src_digits:
            rep["fabrication"].append(f"{label}year/number {y} not in cited items: {plain[:120]}")
    srcw = src.split()
    cons_src = {cons(x) for x in srcw}
    cons_src_s = {c_.rstrip("s") for c_ in cons_src}
    for name in set(re.findall(r"(?<!^)(?<![.!?]\s)\b([A-Z][\wāīūṛṇṭḍśṣṅñ’'-]{2,}(?:\s+[A-Z][\wāīūṛṇṭḍśṣṅñ’'-]{2,})*)", plain)):
        for w in re.split(r"[\s-]+", name):
            w = re.sub(r"[’']s$", "", w)
            if not w[:1].isupper():          # the lower-case half of a compound ("Betwa-fed") is not a name
                continue
            sk = skel(w)
            if not sk or sk in ALLOW_SK or w.lower() in MONTHS:
                continue
            if sk not in src and cons(w) not in cons_src and cons(w).rstrip("s") not in cons_src_s:
                rep["fabrication"].append(f"{label}name '{w}' not in cited items: {plain[:120]}")


def _quote_scan(s, cited, ids, rep):
    qtext = " ".join(" ".join(c["quote"].split()) for c in cited)
    for m in QUOTE_RE.finditer(clean(s)):
        q, tr = m.group(1).strip(), m.group(2)
        if tr:
            continue
        if any("⚠" in c["flags"] for c in cited):
            rep["warn_quotes"].append(q[:80])
        frags = [f.strip(" .,;:'’") for f in re.split(r"…|\.\.\.|\[[^\]]*\]", q) if len(f.strip(" .,;:'’")) > 1]
        norm = lambda z: " ".join(z.replace("’", "'").replace("‘", "'").split())  # noqa: E731
        if not cited or not all(norm(f) in norm(qtext) for f in frags):
            rep["nonverbatim_quotes"].append({"quote": q[:120], "cited": ids})


is_int_ = is_int


def check(text, pack, section=None, targets=None):
    targets = targets or TARGETS
    authored = getattr(C, "AUTHORED", False) and not HOUSE     # house voice: no per-paragraph [INT] requirement or labels
    rep = {"invalid_ids": [], "author_uses": [], "nonverbatim_quotes": [], "warn_quotes": [],
           "uncited_claims": [], "fabrication": [], "conflicts": [], "words": {}, "word_issues": [],
           "generic": [], "ngram_hits": [], "interpretive": {}, "interpretive_issues": [], "fact_per_sentence": [], "settled_issues": [], "gaz_share": []}
    raw_secs = split_sections(text) if section is None else {section: text}
    total = 0
    for k, t in raw_secs.items():
        n = words(t)
        total += n
        rep["words"][k] = n
        lo, hi = (0.7, 1.2) if HOUSE else (0.9, 1.1)   # house voice: 70–120% (user, 2026-10-14; never pad)
        if targets.get(k) and not (targets[k] * lo <= n <= targets[k] * hi):
            rep["word_issues"].append(f"{k}: {n} words vs target {targets[k]} ({lo:.0%}–{hi:.0%})")
    rep["words"]["total"] = total
    if section is None and not getattr(C, "NO_LENGTH", False) and not (C.WMIN <= total <= C.WMAX):
        rep["word_issues"].append(f"total {total} words, outside {C.WMIN:,}–{C.WMAX:,}")
    # notes: citations valid, quotes verbatim, facts in the note's own items
    for nt in notes_in(text):
        nids = ids_in(nt)
        rep["invalid_ids"] += [x for x in nids if x != "AUTHOR" and x not in pack]
        cited = [pack[x] for x in nids if x in pack]
        _quote_scan(nt, cited, nids, rep)
        if not nids:
            rep["uncited_claims"].append("note without citation: " + clean(nt)[:160])
        else:
            _fact_scan(clean(nt), cited, rep, "note: ")
    main = strip_notes(text)
    secs = split_sections(main) if section is None else {section: main}
    for k, t in secs.items():
        n_s = n_int = 0
        prev_ids = []
        for pi, para in enumerate(paragraphs(t), 1):
            sents = sentences(para)
            para_ids = [x for s_ in sents for x in ids_in(s_)]
            ints = 0
            for i, s_ in enumerate(sents):
                n_s += 1
                is_int = is_int_(s_)
                ids = ids_in(s_)
                nxt = ids_in(sents[i + 1]) if i + 1 < len(sents) else []
                for x in ids:
                    if x == "AUTHOR":
                        rep["author_uses"].append(s_[:160])
                    elif x not in pack:
                        rep["invalid_ids"].append(x)
                plain = clean(s_)
                if is_int:
                    n_int += 1
                    ints += 1
                    basis = [pack[x] for x in dict.fromkeys(ids + para_ids + prev_ids) if x in pack]
                    _quote_scan(s_, basis, ids, rep)
                    _fact_scan(plain, basis, rep, "[INT] new fact? ")
                    if GENERIC.search(plain):
                        rep["generic"].append(plain[:160])
                else:
                    cited = [pack[x] for x in ids + nxt if x in pack]
                    _quote_scan(s_, cited, ids, rep)
                    has_claim = (re.search(r"\b\d{2,4}\b", plain) or re.search(r"according to", plain, re.I)
                                 or re.search(r"(?<![.!?]\s)(?<!^)\b[A-Z][a-zāīūṛṇṭḍśṣ]+", plain[1:]))
                    if has_claim and not ids and HOUSE:
                        # house voice: an uncited sentence is inference unless it brings a name or number its paragraph has not cited
                        probe = {"fabrication": []}
                        _fact_scan(plain, [pack[x] for x in dict.fromkeys(para_ids + prev_ids) if x in pack], probe)
                        if probe["fabrication"] or not (para_ids or prev_ids):
                            rep["uncited_claims"].append(plain[:200])
                    elif has_claim and not ids:
                        rep["uncited_claims"].append(plain[:200])
                    if ids:
                        _fact_scan(plain, cited, rep)
                for h in ([] if HOUSE else ngram_hits(s_)):
                    rep["ngram_hits"].append(f"{k}: '{h}' in: {plain[:120]}")
            if authored and len(sents) >= 2 and ints == 0:
                rep["interpretive_issues"].append(f"{k} paragraph {pi}: no interpretive sentence (each paragraph needs at least one: cause, consequence, comparison, tension or thesis)")
            if authored and len(sents) >= 3 and ints == len(sents):
                rep["interpretive_issues"].append(f"{k} paragraph {pi}: pure interpretation (no cited fact)")
            if authored or HOUSE:
                for s2 in ([] if HOUSE else sents):
                    if is_int_(s2) and not int_func(s2):
                        rep["interpretive_issues"].append(f"{k} paragraph {pi}: [INT] without a function label: {clean(s2)[:100]}")
                singles = [not is_int_(s2) and len(clean(s2).split()) <= 22 and len(ids_in(s2)) == 1 for s2 in sents]
                if len(sents) >= 4 and sum(singles) / len(sents) > 0.6:
                    rep["fact_per_sentence"].append(f"{k} paragraph {pi}: {sum(singles)} of {len(sents)} sentences are short single-ID facts — combine facts that serve one point into one sentence")
            prev_ids = para_ids
        ratio = n_int / n_s if n_s else 0
        rep["interpretive"][k] = {"int": n_int, "sentences": n_s, "ratio": round(ratio, 3)}
        for s3 in sentences(t):
            pl = clean(s3)
            for trig, need, label in getattr(C, "SETTLED", []):
                # a settled range is a distance FROM UDAYPUR: "after 96 km it enters Vidisha district" is not one
                if re.search(trig, pl, re.I) and not re.search(need, pl, re.I) and re.search(r"Udayp|Udaip|village|the town", pl, re.I):
                    rep["settled_issues"].append(f"{k}: settled range narrowed ({label}): {pl[:120]}")
    gmax = getattr(C, "GAZ_MAX_SHARE", None)        # user 2026-10-14 (Ch3): the Gazetteer supplies at most 40% of any section
    if gmax:
        for k, t in raw_secs.items():
            cited = [i for i in dict.fromkeys(ids_in(t)) if i in pack]
            g = sum(pack[i].get("book_code") == "GAZ" for i in cited)
            if cited and g / len(cited) > gmax:
                rep["gaz_share"].append(f"{k}: Gazetteer supplies {g} of {len(cited)} cited items ({g / len(cited):.0%}), above {gmax:.0%}: "
                                             "cite the non-Gazetteer items for the same facts, or cut the Gazetteer-only detail")
    for k in ([section] if section else list(C.CONFLICTS)):
        t = secs.get(k, main if section else "")
        for name, pats in C.CONFLICTS.get(k, []):
            ok = all(re.search(p, t + " " + " ".join(notes_in(raw_secs.get(k, text))), re.I | re.S) for p in pats)
            rep["conflicts"].append({"section": k, "conflict": name, "present": bool(ok)})
    view = strip_int(main) if section is None else f"## {section} x\n\n" + re.sub(r"(?m)^## .*$", "", strip_int(main))
    sub = subject_report(view)
    rep["subject"] = {k: {kk: vv for kk, vv in v.items() if kk != "detail"} for k, v in sub.items()}
    rep["subject_detail"] = {k: v["detail"] for k, v in sub.items()}
    rep["subject_fail"] = [k for k, v in sub.items() if not v["pass"]]
    rep["monotony"] = monotony_report(view)
    rep["duplicates"] = duplicates_report(view)
    rep["malformed_notes"] = text.count("{{note:") - len(NOTE_RE.findall(text))     # a {{note: …}} that does not close
    rep["integrity_ok"] = not (rep["invalid_ids"] or rep["nonverbatim_quotes"] or rep["warn_quotes"] or rep["malformed_notes"])
    rep["fabrication"] = sorted(set(rep["fabrication"]))
    return rep


def summary(rep):
    out = {k: (len(v) if isinstance(v, list) else v) for k, v in rep.items()
           if k not in ("conflicts", "subject", "subject_detail", "subject_fail", "monotony", "duplicates", "interpretive")}
    out["interpretive"] = {k: f"{v['int']}/{v['sentences']} ({v['ratio']:.0%})" for k, v in rep.get("interpretive", {}).items()}
    out["duplicates"] = len(rep.get("duplicates", []))
    out["monotony"] = len(rep.get("monotony", []))
    out["conflicts_missing"] = [c["conflict"] for c in rep["conflicts"] if not c["present"]]
    out["source_led"] = {k: f"{v['flagged']}/{v['sentences']}" for k, v in rep.get("subject", {}).items()}
    out["subject_fail"] = rep.get("subject_fail", [])
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    f = Path(sys.argv[1])
    f = f if f.is_absolute() else C.D / f
    sec = sys.argv[sys.argv.index("--section") + 1] if "--section" in sys.argv else None
    r = check(f.read_text(encoding="utf-8"), load_pack(), sec)
    print(json.dumps(summary(r), ensure_ascii=False, indent=1))
    print(json.dumps(r["subject_detail"], ensure_ascii=False, indent=1))
