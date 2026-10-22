"""Phase 0: learn the voice from the writing sample(s) — once, shared by every chapter.

  python -u -I drafting/_pipe/style.py "<sample1.pdf>" ["<sample2.pdf>"]

1 extract text (PyMuPDF); a page with almost no text layer is reported as image-only (OCR needed) rather than guessed
2 code statistics: sentence and paragraph length (mean, SD, distribution), short/long sentence mix, questions,
  first person, quotations, parentheses, numbers, diacritics and Indic terms, footnote markers
3 one flagship call: the style profile (stance; paragraph architecture with 3–4 patterns; evidence handling; rhythm;
  Indic terms; time and scale; openings and closings; register and what the author never does) — technique only, no
  copied wording — and the choice of 3 exemplar passages (200–300 words), returned as anchors and sliced by code
  verbatim from the sample. Two samples: profile both and base the voice on what they share.
Outputs: drafting/style/sample_text.txt (full text, for the 6-gram check), sample_stats.json, style_profile.md,
exemplars.md. Model: OPENAI_MODEL_FLAGSHIP (default gpt-6-astra). Log: drafting/style/api_log/.
"""
import json
import os
import re
import statistics as stt
import sys
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[2]))
OUT = ROOT / "drafting" / "style"
os.environ.setdefault("UDAY_CFG", str(ROOT / "drafting" / "style" / "cfg_style.py"))
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "cfg_style.py").write_text(
    "from pathlib import Path\nCH = 0\nVERSION = 'style'\nD = Path(r'%s')\nSECTIONS = []\nOUTLINE = D / 'none.md'\nPACK = D / 'none.json'\n"
    "LOG = D / 'api_log'\nOUT = D / 'none.md'\nWMIN, WMAX = 0, 0\nCONFLICTS = {}\nCHAPTER_BRIEF = ''\nBUDGET, RESERVE = 2.00, 0.0\n" % OUT, encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import run as rn  # noqa: E402


def extract(pdf):
    import pymupdf
    d = pymupdf.open(pdf)
    pages, image_only = [], []
    for i, p in enumerate(d):
        t = p.get_text()
        if len(t.strip()) < 80 and p.get_images():
            image_only.append(i + 1)
        pages.append(t)
    return pages, image_only


def clean(pages):
    txt = "\n".join(pages)
    txt = re.sub(r"(?m)^\s*\d{1,4}\s*$", "", txt)                    # page numbers
    txt = re.sub(r"-\n(?=[a-z])", "", txt)                             # hyphenated line breaks
    paras = [re.sub(r"\s*\n\s*", " ", p).strip() for p in re.split(r"\n\s*\n|(?<=[.!?”\"])\n(?=[A-Z“\"])", txt)]
    return [p for p in paras if len(p.split()) >= 8]


def stats(paras):
    sents = [s for p in paras for s in re.split(r"(?<=[.!?])\s+(?=[A-Z“\"‘'(])", p) if len(s.split()) >= 2]
    sl = [len(s.split()) for s in sents]
    pl = [len(p.split()) for p in paras]
    allw = " ".join(paras)
    nw = max(1, len(allw.split()))
    return {
        "words": nw, "paragraphs": len(paras), "sentences": len(sents),
        "sentence_len_mean": round(stt.mean(sl), 1) if sl else 0, "sentence_len_sd": round(stt.pstdev(sl), 1) if sl else 0,
        "sentence_len_median": stt.median(sl) if sl else 0,
        "share_short_le8": round(sum(x <= 8 for x in sl) / len(sl), 3) if sl else 0,
        "share_long_ge30": round(sum(x >= 30 for x in sl) / len(sl), 3) if sl else 0,
        "paragraph_len_mean": round(stt.mean(pl), 1) if pl else 0, "paragraph_len_sd": round(stt.pstdev(pl), 1) if pl else 0,
        "paragraph_len_min_max": [min(pl), max(pl)] if pl else [0, 0],
        "questions_per_1000w": round(1000 * allw.count("?") / nw, 2),
        "first_person_per_1000w": round(1000 * len(re.findall(r"\b(I|we|my|our|us)\b", allw)) / nw, 2),
        "quotations_per_1000w": round(1000 * len(re.findall(r"[“\"]", allw)) / 2 / nw, 2),
        "parentheses_per_1000w": round(1000 * allw.count("(") / nw, 2),
        "numbers_per_1000w": round(1000 * len(re.findall(r"\b\d[\d,.]*\b", allw)) / nw, 2),
        "diacritic_words_per_1000w": round(1000 * len(re.findall(r"\b\w*[āīūṛṝḷṅñṭḍṇśṣṃḥĀĪŪṚṬḌṆŚṢ]\w*", allw)) / nw, 2),
        "footnote_markers": len(re.findall(r"(?<=[a-z.,;])\d{1,3}(?=\s|$)", allw)),
    }


SYS = """You are a senior editor of non-fiction history. Analyse the writing sample(s) as craft, so that another writer can learn the technique without copying a word. If there are two samples, profile both briefly and base the shared voice on what they have in common, saying where they differ.
Write the STYLE PROFILE in Markdown with these headings, each concrete and grounded in the sample (describe moves; quote at most 3 words at a time):
1. Stance — the author's position relative to evidence and reader; how they move between narrative and argument.
2. Paragraph architecture — the typical sequence of moves (e.g. concrete detail → context → interpretation → implication); give 3–4 recurring patterns, each named, with its move sequence.
3. Evidence handling — how sources and inscriptions enter the prose; named in text vs left to notes; how disagreement is handled.
4. Rhythm — interpret the supplied code statistics (sentence-length mean and variance; long/short mixing; paragraph variation).
5. Indic terms — italics, diacritics, glossing on first use, translated quotation.
6. Time and scale — how the author moves between deep time, dynastic time and the present.
7. Openings and closings — of chapters and sections.
8. Register and vocabulary — and what the author never does (clichés, hedges, false drama).
9. Rules for imitation — 8–12 imperative rules a drafting model can follow.
Then choose 3 exemplar passages (each 200–300 words, contiguous, in the sample) that best show the patterns; give for each its first 8 words and last 8 words exactly as in the sample, and a one-line reason.
Return ONLY JSON: {"profile_markdown": "...", "exemplars": [{"first_words": "...", "last_words": "...", "shows": "..."}]}"""


def slice_exemplar(text, first, last):
    norm = lambda z: re.sub(r"\s+", " ", z).strip()  # noqa: E731
    t = norm(text)
    a = t.find(norm(first))
    if a < 0:
        return None
    b = t.find(norm(last), a)
    if b < 0:
        return None
    return t[a:b + len(norm(last))]


def main(pdfs):
    samples, report = [], {}
    for pdf in pdfs:
        pages, image_only = extract(pdf)
        paras = clean(pages)
        name = Path(pdf).name
        report[name] = {"pages": len(pages), "image_only_pages": image_only, **stats(paras)}
        if len(image_only) > len(pages) / 2:
            sys.exit(f"{name}: {len(image_only)} of {len(pages)} pages are image-only — OCR needed before profiling")
        samples.append((name, paras))
    full = "\n\n".join(f"### {n}\n\n" + "\n\n".join(p) for n, p in samples)
    (OUT / "sample_text.txt").write_text("\n\n".join("\n\n".join(p) for _, p in samples), encoding="utf-8")
    (OUT / "sample_stats.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=1), flush=True)
    budget = 380000                                         # characters of sample sent to the model (whole sample if smaller)
    body = full if len(full) <= budget else full[:budget]
    R = rn.Run(False)
    out = R.call("style_profile", 0, "judge", SYS, f"CODE STATISTICS:\n{json.dumps(report, ensure_ascii=False, indent=1)}\n\nSAMPLE TEXT:\n{body}",
                 4000, model=rn.FLAGSHIP, effort="high")
    j = rn.parse_json(out) or {}
    prof = j.get("profile_markdown", "").strip()
    ex = []
    for e in j.get("exemplars", [])[:3]:
        s = None
        for n, p in samples:
            s = slice_exemplar("\n\n".join(p), e.get("first_words", ""), e.get("last_words", ""))
            if s:
                ex.append({"sample": n, "text": s, "words": len(s.split()), "shows": e.get("shows", "")})
                break
        if not s:
            ex.append({"sample": "?", "text": "", "words": 0, "shows": f"NOT FOUND VERBATIM: {e}"})
    st = "\n".join(f"- **{n}**: {r['words']:,} words; sentences {r['sentence_len_mean']} ± {r['sentence_len_sd']} words "
                   f"(median {r['sentence_len_median']}; ≤ 8 words {r['share_short_le8']:.0%}; ≥ 30 words {r['share_long_ge30']:.0%}); "
                   f"paragraphs {r['paragraph_len_mean']} ± {r['paragraph_len_sd']} words (range {r['paragraph_len_min_max'][0]}–{r['paragraph_len_min_max'][1]})"
                   for n, r in report.items())
    (OUT / "style_profile.md").write_text("# Style profile\n\n*Technique only, learnt from the writing sample(s); it reproduces no wording. Drafting calls see this profile and the three exemplars, never the full sample.*\n\n"
                                          f"## Code statistics\n\n{st}\n\n{prof}\n", encoding="utf-8")
    (OUT / "exemplars.md").write_text("# Exemplars\n\n*Voice reference only — never reuse their phrases or content.*\n\n" + "\n\n".join(
        f"## Exemplar {k} ({e['words']} words) — {e['shows']}\n\n{e['text']}" for k, e in enumerate(ex, 1)) + "\n", encoding="utf-8")
    print(json.dumps({"spent": round(R.spent, 3), "exemplars": [(e["sample"], e["words"]) for e in ex]}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
