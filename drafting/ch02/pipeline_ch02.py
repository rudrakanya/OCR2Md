"""Chapter 2 drafting pipeline (the Chapter 1 v2 approach, adapted).

Rounds:
  1  candidates 2.1–2.5 (A, B each; all parallel)  high    — voice sample = opening of Chapter 1 v2
  2  judges 2.1–2.5 (A vs B; + register score)      high
  3  edits (all sections, parallel)                 medium  — revert if worse
  4  stitch                                         high
  5  code validation + revisions (≤2 rounds)        medium
  6  citation-support verification + fixes          medium  — never cut
  7  polish                                         medium  — kept only if no worse; first to be cut
Budget: $5 for all Chapter 2 API stages (incl. the KB step, same api_log_ch02/); $0.90 finishing reserve.
Words: 4,750–5,250 total (5,000 ±5%); sections 90–110% of target. Meta-commentary sentences count as failures.

  python -I "drafting/ch02/pipeline_ch02.py" --dry-run
  python -u -I "drafting/ch02/pipeline_ch02.py"
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import draft as dr  # noqa: E402
import pipeline_v3 as pv  # noqa: E402
import validate as va  # noqa: E402
import verify as vf  # noqa: E402

D = HERE
pv.LOG = D / "api_log_ch02"
pv.UNACCOUNTED = 0.0
pv.BUDGET = 5.00
pv.EFFORT.update({"candidate": "high", "judge": "high", "edit": "medium", "stitch": "high", "revise": "medium",
                  "polish": "medium", "verify": "medium", "fix": "medium", "reverify": "medium"})
RESERVE = 0.90
OUTLINE = D / "ch02_outline.md"
PACK = D / "evidence_pack_v2.json"
VOICE_SRC = D.parent / "ch01" / "ch01_draft_v2.md"
CAND = D / "candidates"
SECTIONS = ["2.1", "2.2", "2.3", "2.4", "2.5"]
WMIN, WMAX = 4750, 5250
OUT = D / "ch02_draft_v1.md"

META = re.compile(
    r"\bwill not be\b|\bwill remain\b|\bwill be (?:treated|read|kept|retained|presented|accepted|rejected|settled)\b|\bthis book\b|"
    r"\bthis chapter\b|\bthe narrative\b|\bwe cannot\b|\bit must be noted\b|\bit is important to\b|\bthe reader\b|"
    r"\bthis section\b|\bthe account must\b|\bthe enquiry\b|\bthe book (?:will|must|commits|keeps|treats)\b|"
    r"\bneed not be\b|\bmust remain\b|\bwithout (?:deciding|choosing|resolving|settling)\b", re.I)
SCORE_WEIGHTS = {"meta": 4}

WRITER_BRIEF = """You are writing Chapter 2, "The Betwa Valley: Land, Rivers and Seasons", of a history of Udaypur (Vidisha district, Madhya Pradesh, India) — the town of the Paramāra king Udayāditya and the Udayeśvara temple, NOT Udaipur in Rajasthan. The chapter must read like a chapter from a university-press history written for educated general readers: physical geography told as the ground on which a town's history was made. Its premise: Udaypur sits in a river basin that does not water it, and that contradiction shapes everything built here.

REGISTER: authoritative and measured. Present tense for the land, the climate and what sources record or argue ("the Gazetteer records…", "Geo-Heritage finds…"); past tense for historical events.

THE RULES ARE FOR YOU, NEVER FOR THE TEXT: never describe the book's own method, caution or intentions. No sentences about what "will" or "will not" be claimed, presented or resolved; no reflections on "the narrative", "this book", "this chapter", "the reader", "the enquiry"; no "need not be…", "must remain…". Uncertainty is shown through attribution and precise verbs, not announced.

CALIBRATED HEDGING: one precise qualifier where the evidence requires it ("probably", "according to", "the survey suggests"); never stack qualifiers; state well-attested facts plainly.

SYNTHESISE, DON'T LIST SOURCES: write about the land and bring sources in where they matter. Never write one sentence per source. Name a source in the text only when the attribution matters (a figure that differs between sources, a judgement, testimony); otherwise the bracketed ID (later a footnote) carries it. Numbers: give the figures that carry the argument; do not pile up statistics — two or three figures per paragraph at most, each with its unit.

PARAGRAPHS: 120–200 words, each opening with a topic sentence and containing at least one concrete, cited detail. Follow the section's paragraph plan.

CONFLICTS: set out competing positions or figures fairly and say what each rests on (source, area, period), without choosing one. Where figures differ because they measure different things (a district vs a basin; different periods), say so plainly. End on the substance, not on commentary about uncertainty.

QUOTATIONS: at most 2 per section, short, worked into the sentence, chosen for wording that matters; copied character-for-character from an item's QUOTE, in double quotation marks, followed by the ID. Hindi/Sanskrit items: paraphrase in English, or quote the English rendering marked "(translation)". Never quote an item flagged ⚠.

SECTION ENDINGS: close on content that leads into the next section. No summaries, no "this chapter will", no rhetorical questions.

FACTS: only facts in the supplied items' QUOTE (and ENGLISH RENDERING). The CONTEXT excerpts are there so your paraphrase keeps each source's meaning, qualifications and attribution — never take a fact from a context excerpt that is not in the item's QUOTE. No dates, names or numbers from general knowledge.

CITATIONS: every sentence that states a fact ends with its evidence ID(s) in square brackets, e.g. [C02-GAZ-016] or [C02-GEOHER-005; C02-KB-GAZ-008]. Only supplied IDs.

ROUTING AND CANON (binding): Geo-Heritage (GEOHER, the INTACH survey) carries this chapter for the land and the site; never adopt its superlatives. The district Gazetteer (GAZ) is for the modern setting — climate, rivers, soils, agriculture — never for medieval events; when the chapter first cites it, date-stamp it once as the 1979 compilation (e.g. "the district Gazetteer of 1979"). *Jagta Hua Kasba* (IDs with JAGTA) is testimony — present-day observation, folklore and the author's views, attributed in the sentence; never the source of a medieval fact or a measurement; its pages are approximate. The author of *Jagta Hua Kasba* is Vijay Manohar Tiwari: name him in full once, at his first mention in the chapter (section 2.2), then "Tiwari"; no citation is needed for the name; avoid gendered pronouns for Tiwari. A praśasti is royal panegyric. Samarāṅgaṇasūtradhāra material is prescriptive norm, attributed to the text, and SAMAR-* items are old OCR (never quote). Temple Economics is excluded entirely. Committed figures: Udaypur's ground lies at 340–480 m above sea level, mean 410 m; the Kewtan runs 1.8 km from the hill (Shiva Pindi). Leave to Chapter 3: hill heights, the mesa/butte/arch, sandstone petrology and colour, caves, bats, forests, flora and fauna. Leave to Chapter 7 the Udaysagar/Udayasamudra tank (a clause at most) and to Chapter 11 the fort fabric (a clause at most). At most 3 attributed scholarly assessments in the chapter; the narrator never uses superlatives (a source's ranking, e.g. "third largest river of Malwa", only as attributed).

STYLE: British/Indian English. "Udaypur" throughout. Diacritics: Udayāditya, Paramāra, Udayeśvara, Vētravatī (the inscriptions' spelling), praśasti, Samarāṅgaṇasūtradhāra, jāṅgala, anūpa, sādhāraṇa. Italicise Indian-language terms on first use with a half-clause gloss (talav, tekro, baoli, kund, kharif, rabi, mar). Units as the sources give them (keep a source's miles where it gives miles). Banned: nestled, tapestry, testament to, stands as, rich history, steeped in, delve, bustling, timeless, hidden gem, in conclusion.

OUTPUT: the section in Markdown, starting with its heading line exactly as given ("## <number> <title>"), and nothing else."""

JUDGE_SYS = """You are a senior editor at a university press judging two candidate versions (A, B) of one section of a history chapter about Udaypur for general readers.
Score each entry 1–10 on: fidelity (only supplied evidence; correct citations; conflicts set out fairly and unresolved), coverage (the section's paragraph plan, key points and conflicts), prose (topic sentences, concrete detail, varied sentences, strong opening), register (professional history: penalise HEAVILY any meta-commentary about the book/narrative/method, future-tense hedging such as "will remain"/"will not be", announced caution, and one-sentence-per-source listing), voice (matches the voice sample and brief), transition (fits the planned transitions; stays out of material covered elsewhere).
The automated check report for each entry is supplied — weigh uncited claims, fabrication flags and meta-commentary flags heavily.
Pick the best entry. Then give 5–8 concrete, line-level improvements (quote the phrase; say exactly how to change it), aimed especially at register and synthesis. You may name a paragraph in another entry to transplant (it keeps its IDs).
Return ONLY JSON: {"scores": {"A": {"fidelity":n,"coverage":n,"prose":n,"register":n,"voice":n,"transition":n,"total":n}, "B": {...}}, "best": "A|B", "improvements": ["..."], "transplants": ["..."], "rationale": "..."}"""

EDIT_SYS = """You revise one section of a history chapter about Udaypur. Apply ONLY the listed improvements (and transplants) and fix the listed automated-check problems, including every meta-commentary sentence (rewrite it to state the substance through attribution and precise verbs, or cut it).
STRICT: no new facts, dates, names or numbers; every factual sentence keeps its bracketed evidence IDs (do not invent IDs); quotations stay verbatim or are cut whole; keep the heading line exactly; stay within the word range.
Return the full revised section in Markdown and nothing else."""

STITCH_SYS = """You are the final editor of Chapter 2 ("The Betwa Valley: Land, Rivers and Seasons") of a university-press history of Udaypur. The sections were drafted in parallel: you own cross-section continuity. Smooth transitions using the planned transitions; remove repetition across sections (keep each point where the coverage map assigns it; elsewhere cut it or reduce it to a clause); make sure Vijay Manohar Tiwari is named in full once (his first mention in the chapter) and "Tiwari" afterwards; make sure the district Gazetteer is date-stamped once as the 1979 compilation; keep one voice; remove any meta-commentary about the book, chapter, narrative or method.
STRICT: add no facts, dates, names or numbers; keep every bracketed evidence ID attached to its claim, unchanged; never change text inside quotation marks; keep each section's heading and each section within 90–110% of its word target; total 4,750–5,250 words (IDs excluded). British/Indian English; keep diacritics.
Return only the full chapter in Markdown."""

REVISE_SYS = """You fix specific problems in one section of a history chapter about Udaypur.
Fix ONLY the listed problems: cite uncited factual sentences with a supplied ID or delete the claim; replace non-verbatim quotations with the exact words of the cited QUOTE or paraphrase; delete or re-cite years/names not in the cited items; rewrite meta-commentary sentences to state substance (or cut them); adjust length to the word range using only supplied evidence. Add no new facts. Keep all other text, IDs and the heading.
Return the full corrected section in Markdown and nothing else."""

POLISH_SYS = """Polish this history chapter at sentence level for a university press: tighten rhythm, vary sentence openings, cut repetition and any remaining meta-commentary or stacked hedges, remove banned phrases (nestled, tapestry, testament to, stands as, rich history, steeped in, delve, bustling, timeless, hidden gem, in conclusion).
STRICT: no new facts, dates, names or numbers; every bracketed evidence ID stays attached to its claim, unchanged; text inside quotation marks unchanged; headings unchanged; keep each section's length (total 4,750–5,250 words, IDs excluded).
Return only the full chapter in Markdown."""


CONVENTIONS = ("EDITORIAL CONVENTIONS (supplied by the editor, not evidence claims — treat as supported and never remove): "
               "the author of *Jagta Hua Kasba* is Vijay Manohar Tiwari ('Tiwari'); the district Gazetteer is the 1979 compilation "
               "('the district Gazetteer of 1979'). Book titles in Devanagari are never written in the prose.\n\n")


def ts():
    return time.strftime("%H:%M:%S")


# ---------------------------------------------------------------- outline v2 parsing
def load_outline():
    text = OUTLINE.read_text(encoding="utf-8")
    parts = re.split(r"\n(?=## 2\.\d)", text)
    secs = {}
    for p in parts[1:]:
        k = re.match(r"## (2\.\d)", p).group(1)
        secs[k] = p.split("\n## Word targets")[0].strip()
    targets = {k: int(re.search(r"(\d[\d,]*)\s*w\b", secs[k]).group(1).replace(",", "")) for k in secs}
    titles = {k: re.match(r"## (2\.\d [^*\n]+?)\s*\*\(", secs[k]).group(1).strip() for k in secs}
    return text, secs, targets, titles


def section_ids(sec_text, P):
    ids = list(dict.fromkeys(re.findall(r"C\d\d-[A-Z0-9-]+?-\d{3}", sec_text)))
    return [i for i in ids if i in P]


def fmt_item(i):
    flags = [f for f in i["flags"] if not f.startswith("also")]
    s = (f"[{i['id']}] {i['strength'].upper()} · {i['book_title']} · {i['page']}" + (f" · flags: {', '.join(flags)}" if flags else "")
         + "\nQUOTE (only this text may be quoted or used for facts): " + " ".join(i["quote"].split()))
    if i.get("gloss"):
        s += "\nENGLISH RENDERING (translation): " + i["gloss"]
    if i.get("claim"):
        s += f"\nCONFLICT POSITION: {i['claim'].get('key')} → {i['claim'].get('value')}"
    if i.get("context"):
        s += "\nCONTEXT (meaning/attribution only; not a source of facts): " + i["context"][:900]
    return s


# ---------------------------------------------------------------- checks
def check(text, P, sec=None, targets=None):
    rep = va.check(text, P, sec)
    # word ranges: sections 90–110%, chapter 3,800–4,200
    rep["word_issues"] = []
    for k, n in rep["words"].items():
        if k != "total" and targets and k in targets and not (targets[k] * 0.9 <= n <= targets[k] * 1.1):
            rep["word_issues"].append(f"{k}: {n} words vs target {targets[k]} (90–110%)")
    rep["word_issues"] = [w for w in rep["word_issues"] if not w.startswith("total")]
    if sec is None and not (WMIN <= rep["words"]["total"] <= WMAX):
        rep["word_issues"].append(f"total {rep['words']['total']} words, outside {WMIN:,}–{WMAX:,}")
    meta = []
    for s in va.sentences(text):
        if META.search(va.BRACKET.sub("", s)):
            meta.append(va.BRACKET.sub("", s).strip()[:220])
    rep["meta"] = meta
    return rep


def problems_of(rep):
    out = pv.problems_of(rep)
    out += [f"meta-commentary sentence (rewrite to state substance, or cut): {m}" for m in rep.get("meta", [])]
    return out


def score_rep(rep):
    return pv.score_rep(rep) + SCORE_WEIGHTS["meta"] * len(rep.get("meta", []))


def summ(rep):
    s = va.summary(rep)
    s["meta"] = len(rep.get("meta", []))
    return s


# ---------------------------------------------------------------- main
def run(dry):
    t_start = time.time()
    print(f"[{ts()}] ch02 pipeline start (dry={dry})", flush=True)
    outline, secs, targets, titles = load_outline()
    P = {i["id"]: i for i in json.loads(PACK.read_text(encoding="utf-8"))}
    voice_txt = VOICE_SRC.read_text(encoding="utf-8")
    voice_txt = re.sub(r"(?m)^#.*$", "", voice_txt)
    voice0 = " ".join(re.sub(r"\[[^\]]+\]", "", voice_txt).split()[:420])
    info = pv.section_parts(secs)
    R = pv.Run(dry)
    stage_t = {}
    state = {"version": "ch02 v1", "model": pv.MODEL, "effort": pv.EFFORT, "budget": pv.BUDGET, "reserve": RESERVE,
             "kb_spend_before_drafting": round(R.prior, 4), "sections": {}, "decisions": []}
    if not dry:
        R.spent = R.prior   # no unaccounted carry-over in v2
    ids = {s: section_ids(secs[s], P) for s in SECTIONS}

    def prompt(sec, voice):
        inc, outg = pv.transitions(sec, info, titles)
        cov = pv.covered_elsewhere(sec, info, titles)
        u = (f"THE WHOLE CHAPTER OUTLINE (v2):\n{outline}\n\nSECTION TO WRITE NOW: {titles[sec]}\nSection plan:\n{secs[sec]}\n\n"
             f"WORD TARGET: {targets[sec]} words (must land {int(targets[sec] * 0.9)}–{int(targets[sec] * 1.1)}), IDs excluded.\n\n"
             f"COVERED ELSEWHERE (do not develop):\n{cov}\n\nPLANNED INCOMING TRANSITION: {inc}\nPLANNED OUTGOING TRANSITION: {outg}\n\n"
             + (f"VOICE SAMPLE (opening of the book's Chapter 1, final draft — match register and rhythm; do not copy content):\n{voice}\n\n" if voice else "")
             + f"EVIDENCE FOR THIS SECTION ({len(ids[sec])} items):\n" + "\n\n".join(fmt_item(P[i]) for i in ids[sec]))
        return WRITER_BRIEF, u

    def gen_cands(sec_list, voice):
        jobs = []
        for sec in sec_list:
            for L in "AB":
                p = CAND / f"{sec}_{L}.md"
                if p.exists() and not dry:
                    continue
                def job(sec=sec, L=L):
                    system, u = prompt(sec, voice)
                    opening = {"A": "OPENING: lead with a concrete fact or scene from the evidence.",
                               "B": "OPENING: lead with the section's central question stated as a claim about the subject (not a rhetorical question)."}[L]
                    out = R.call(f"cand_{sec}_{L}", 1, "candidate", system, u + "\n\n" + opening, targets[sec] + 200)
                    if out is None:
                        return f"## {titles[sec]}\n" + ("Lorem ipsum dolor sit amet [C02-GAZ-001]. " * (targets[sec] // 6))
                    if out and not dry:
                        CAND.mkdir(exist_ok=True)
                        (CAND / f"{sec}_{L}.md").write_text(out.strip(), encoding="utf-8")
                    return out.strip()
                jobs.append(((sec, L), job))
        res = R.parallel(jobs)
        out = {}
        for sec in sec_list:
            out[sec] = {}
            for L in "AB":
                p = CAND / f"{sec}_{L}.md"
                r = res.get((sec, L))
                if isinstance(r, str) and r.strip():
                    out[sec][L] = r
                elif p.exists():
                    out[sec][L] = p.read_text(encoding="utf-8")
                elif isinstance(r, pv.BudgetStop):
                    state["budget_stop"] = str(r)
        return out

    def judge(sec_list, cands, voice):
        jobs = []
        for sec in sec_list:
            labels = sorted(cands[sec])
            reps = {L: check(cands[sec][L], P, sec, targets) for L in labels}
            alive = [L for L in labels if reps[L]["integrity_ok"]] or [min(labels, key=lambda L: score_rep(reps[L]))]
            state["sections"][sec] = {"entries": {L: {"words": reps[L]["words"].get(sec), "integrity_ok": reps[L]["integrity_ok"],
                                                      "check": summ(reps[L])} for L in labels}, "alive": alive}
            def job(sec=sec, alive=alive, reps=reps):
                inc, outg = pv.transitions(sec, info, titles)
                ju = (f"WRITER BRIEF:\n{WRITER_BRIEF}\n\nSECTION PLAN:\n{secs[sec]}\n\nWORD TARGET: {targets[sec]} (90–110%)\n\n"
                      f"COVERED ELSEWHERE:\n{pv.covered_elsewhere(sec, info, titles)}\n\nPLANNED TRANSITIONS: in — {inc}; out — {outg}\n\n"
                      + (f"VOICE SAMPLE:\n{voice}\n\n" if voice else "")
                      + "EVIDENCE:\n" + "\n\n".join(fmt_item(P[i]).split("\nCONTEXT")[0] for i in ids[sec]) + "\n\n"
                      + "\n\n".join(f"=== ENTRY {L} ===\nAUTOMATED CHECKS: {json.dumps(problems_of(reps[L])[:25], ensure_ascii=False)}\n\n{cands[sec][L]}" for L in alive))
                out = R.call(f"judge_{sec}", 2, "judge", JUDGE_SYS, ju, 800)
                return pv.parse_json(out) if out else None
            jobs.append((sec, job))
        res = R.parallel(jobs)
        verdicts = {}
        for sec in sec_list:
            alive = state["sections"][sec]["alive"]
            v = res.get(sec)
            v = v if isinstance(v, dict) else {"best": alive[0], "improvements": [], "scores": {}, "rationale": "judge unavailable"}
            if v.get("best") not in alive:
                v["best"] = alive[0]
            verdicts[sec] = v
            state["sections"][sec]["judge"] = v
            if not dry:
                (D / f"judge_ch02_{sec}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
        return verdicts

    # ===== round 1: all candidates in parallel (voice = Chapter 1 v2 opening); round 2: judges
    t = time.time()
    voice = voice0
    cands = gen_cands(SECTIONS, voice)
    stage_t["1_candidates"] = round(time.time() - t)
    t = time.time()
    verdicts = judge(SECTIONS, cands, voice)
    stage_t["2_judges"] = round(time.time() - t)
    # ===== budget plan for the rest (cut order: polish, then edits; verification never cut)
    skip_polish = skip_edit = False
    if not dry:
        est_rest = 5 * 0.07 + 0.25 + 0.30 + 0.55 + 0.15      # edits, stitch, revisions, verification+fixes, polish
        avail = pv.BUDGET - R.spent
        if est_rest > avail:
            skip_polish = True
            state["decisions"].append(f"est ${est_rest:.2f} > ${avail:.2f} left: polish skipped")
            if est_rest - 0.12 > avail:
                skip_edit = True
                state["decisions"].append("still short: edit round skipped")
    # ===== round 3: edits
    t = time.time()
    finals, freps = {}, {}
    jobs = []
    for sec, v in verdicts.items():
        best = v["best"]
        finals[sec] = cands[sec][best]
        freps[sec] = check(finals[sec], P, sec, targets)
        state["sections"][sec]["chosen"] = best
        if skip_edit:
            continue
        def job(sec=sec, v=v, best=best):
            tg = targets[sec]
            others = "\n\n".join(f"=== ENTRY {L} (transplant source only) ===\n{cands[sec][L]}" for L in state["sections"][sec]["alive"] if L != best)
            eu = (f"WRITER BRIEF (for reference):\n{WRITER_BRIEF}\n\nWORD RANGE: {int(tg * 0.9)}–{int(tg * 1.1)} words (IDs excluded).\n\nIMPROVEMENTS TO APPLY:\n"
                  + "\n".join(f"- {x}" for x in v.get("improvements", []))
                  + ("\nTRANSPLANTS:\n" + "\n".join(f"- {x}" for x in v.get("transplants", [])) if v.get("transplants") else "")
                  + "\nAUTOMATED-CHECK PROBLEMS TO FIX:\n" + "\n".join(f"- {p}" for p in problems_of(freps[sec])[:25])
                  + "\n\nEVIDENCE (the only permitted facts):\n" + "\n\n".join(fmt_item(P[i]).split("\nCONTEXT")[0] for i in ids[sec])
                  + f"\n\n=== SECTION TO REVISE ===\n{finals[sec]}\n\n{others}")
            return R.call(f"edit_{sec}", 3, "edit", EDIT_SYS, eu, tg + 100)
        jobs.append((sec, job))
    res = R.parallel(jobs)
    for sec, out in res.items():
        if isinstance(out, str) and out.strip():
            er = check(out.strip(), P, sec, targets)
            keep = er["integrity_ok"] and score_rep(er) <= score_rep(freps[sec])
            state["sections"][sec]["edit"] = {"kept": keep, "before": summ(freps[sec]), "after": summ(er)}
            if keep:
                finals[sec], freps[sec] = out.strip(), er
    stage_t["3_edits"] = round(time.time() - t)
    joined = "\n\n".join(finals[s].strip() for s in SECTIONS if s in finals) + "\n"
    if not dry:
        (D / "ch02_prestitch.md").write_text(joined, encoding="utf-8")
    # ===== round 4: stitch
    t = time.time()
    chapter, rep = joined, check(joined, P, None, targets)
    cmap = "\n".join(f"- {titles[k]} owns: {info[k]['purpose']} Key points: " + "; ".join(info[k]["points"]) for k in SECTIONS)
    tmap = "\n".join(f"- after {titles[k]}: {info[k]['transition']}" for k in SECTIONS)
    out = R.call("stitch", 4, "stitch", STITCH_SYS, f"COVERAGE MAP:\n{cmap}\n\nPLANNED TRANSITIONS:\n{tmap}\n\nWORD TARGETS: "
                 + ", ".join(f"{k} {targets[k]}" for k in SECTIONS) + f"\n\nDRAFT TO EDIT:\n{joined}", sum(targets.values()) + 300)
    if out:
        st = out.strip() + "\n"
        sr = check(st, P, None, targets)
        keep = sr["integrity_ok"] and score_rep(sr) <= score_rep(rep) + 10
        state["stitch"] = {"kept": keep, "before": summ(rep), "after": summ(sr)}
        if keep:
            chapter, rep = st, sr
    stage_t["4_stitch"] = round(time.time() - t)
    state["validation_before_revision"] = summ(rep)
    # ===== round 5: code validation + revisions (≤ 2 rounds)
    t = time.time()
    state["revisions"] = []
    for rnd in (1, 2):
        parts = va.split_sections(chapter)
        bad = {s: check(parts[s], P, s, targets) for s in SECTIONS if s in parts}
        bad = {s: r_ for s, r_ in bad.items() if problems_of(r_)}
        if not bad or dry:
            break
        def mk(s, r_):
            def job():
                tg = targets[s]
                ru = ("PROBLEMS TO FIX:\n" + "\n".join(f"- {p}" for p in problems_of(r_)[:30]) +
                      f"\n\nWORD RANGE: {int(tg * 0.9)}–{int(tg * 1.1)}\n\nEVIDENCE:\n" + "\n\n".join(fmt_item(P[i]).split("\nCONTEXT")[0] for i in ids[s])
                      + f"\n\n=== SECTION ===\n{parts[s]}")
                return R.call(f"revise_r{rnd}_{s}", 5, "revise", REVISE_SYS, ru, tg)
            return job
        res = R.parallel([(s, mk(s, r_)) for s, r_ in bad.items()])
        for s, out in res.items():
            if isinstance(out, str) and out.strip():
                nr = check(out.strip(), P, s, targets)
                keep = nr["integrity_ok"] and score_rep(nr) < score_rep(bad[s])
                state["revisions"].append({"round": rnd, "section": s, "problems": len(problems_of(bad[s])), "after": len(problems_of(nr)), "kept": keep})
                if keep:
                    parts[s] = out.strip() + "\n"
        chapter = "\n\n".join(parts[s].strip() for s in SECTIONS if s in parts) + "\n"
    rep = check(chapter, P, None, targets)
    state["validation_after_revision"] = summ(rep)
    stage_t["5_validation_revisions"] = round(time.time() - t)
    if not dry:
        (D / "ch02_preverify.md").write_text(chapter, encoding="utf-8")
    # ===== round 6: citation-support verification + targeted fixes (never cut)
    t = time.time()
    if not dry:
        chapter, vstate = verify(chapter, P, R, targets)
        state["verification"] = vstate
    else:
        for sec in SECTIONS:
            R.call(f"verify_{sec}", 6, "verify", vf.VERIFY_SYS, "x" * 24000, 1500)
        for sec in SECTIONS:
            R.call(f"fix_{sec}", 6, "fix", vf.FIX_SYS, "x" * 16000, 300)
        for sec in SECTIONS[:3]:
            R.call(f"reverify_{sec}", 6, "reverify", vf.VERIFY_SYS, "x" * 6000, 300)
    rep = check(chapter, P, None, targets)
    stage_t["6_verification"] = round(time.time() - t)
    # ===== round 7: polish
    t = time.time()
    if skip_polish:
        state["polish"] = {"kept": False, "reason": "skipped (cut order)"}
    else:
        try:
            out = R.call("polish", 7, "polish", POLISH_SYS, chapter, sum(targets.values()))
            if out:
                pol = out.strip() + "\n"
                pr = check(pol, P, None, targets)
                keep = pr["integrity_ok"] and score_rep(pr) <= score_rep(rep)
                state["polish"] = {"kept": keep, "before": summ(rep), "after": summ(pr)}
                if keep:
                    chapter, rep = pol, pr
                if not dry:
                    (D / "ch02_polished_raw.md").write_text(pol, encoding="utf-8")
        except pv.BudgetStop as e:
            state["polish"] = {"kept": False, "reason": f"budget: {e}"}
    stage_t["7_polish"] = round(time.time() - t)
    state["final_validation"] = summ(rep)
    state["final_validation_detail"] = rep
    state["stage_seconds"] = stage_t
    state["wall_clock_seconds"] = round(time.time() - t_start)
    state["calls"] = R.calls
    state["spent_usd"] = round(R.spent, 4)
    state["spend_by_stage"] = {k: round(v, 4) for k, v in R.stage_spend.items()}
    if not dry:
        OUT.write_text(chapter, encoding="utf-8")
    (D / ("ch02_estimate.json" if dry else "ch02_state.json")).write_text(json.dumps(state, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return state, R


def verify(text, P, R, targets):
    """citation-support verification (verify.py logic) on the v2 text, sections concurrently, medium effort."""
    smap = vf.cited_sentences(text)
    rules = vf.rule_checks(text, P, smap)
    def vjob(sec, rows, name="verify", kind="verify"):
        def job():
            iids = sorted({i for r in rows for i in r["ids"] if i in P})
            u = CONVENTIONS + "EVIDENCE ITEMS:\n" + "\n\n".join(vf.item_text(P[i]) for i in iids) + "\n\nSENTENCES TO CHECK:\n" + "\n".join(f"{r['sid']}: {r['sentence']}" for r in rows)
            out = R.call(f"{name}_{sec}", 6, kind, vf.VERIFY_SYS, u, 60 * len(rows))
            j = pv.parse_json(out) or {}
            return {x.get("sid"): x for x in j.get("results", [])}
        return job
    res = R.parallel([(sec, vjob(sec, rows)) for sec, rows in smap.items() if rows])
    verdicts = {}
    for sec, rows in smap.items():
        got = res.get(sec) if isinstance(res.get(sec), dict) else {}
        for r in rows:
            v = got.get(r["sid"]) or {"verdict": "UNVERIFIED"}
            verdicts[r["sid"]] = dict(r, verdict=str(v.get("verdict", "UNVERIFIED")).upper(), evidence=v.get("evidence", ""), fix=v.get("fix", ""))
    def counts(vs):
        out = {}
        for sec in smap:
            c = {}
            for k, v in vs.items():
                if k.startswith(sec + "-"):
                    c[v["verdict"]] = c.get(v["verdict"], 0) + 1
            out[sec] = c
        return out
    st = {"verdicts_before": counts(verdicts), "rule_failures_before": rules}
    # flagged: verifier + code rules + meta-commentary sentences
    flagged = {}
    for sid, v in verdicts.items():
        if v["verdict"] != "SUPPORTED":
            flagged.setdefault(sid.split("-")[0], []).append((sid, v["verdict"], v.get("fix", ""), v.get("evidence", "")))
    for f in rules:
        if f.get("sid"):
            flagged.setdefault(f["sec"], []).append((f["sid"], "RULE: " + f["rule"], f["detail"], ""))
    for sec, rows in smap.items():
        for r in rows:
            if META.search(va.BRACKET.sub("", r["sentence"])):
                flagged.setdefault(sec, []).append((r["sid"], "META-COMMENTARY", "state the substance through attribution and precise verbs, or cut", ""))
    def fjob(sec, items):
        def job():
            rows = {sid: verdicts.get(sid) for sid, *_ in items if verdicts.get(sid)}
            iids = sorted({i for sid in rows for i in rows[sid]["ids"] if i in P})
            u = CONVENTIONS + "EVIDENCE ITEMS:\n" + "\n\n".join(vf.item_text(P[i]) for i in iids) + "\n\nFLAGGED SENTENCES:\n" + \
                "\n".join(f"{sid}: {rows[sid]['sentence']}\n   problem: {vd}; suggested fix: {fx}; evidence: {ev}" for sid, vd, fx, ev in items if sid in rows)
            out = R.call(f"fix_{sec}", 6, "fix", vf.FIX_SYS + "\nAlso: never write meta-commentary about the book, chapter, narrative or method; no future-tense hedging.", u, 60 * len(items))
            j = pv.parse_json(out) if out else None
            return {x.get("sid"): x for x in (j or {}).get("replacements", [])}
        return job
    fixes = R.parallel([(sec, fjob(sec, items)) for sec, items in flagged.items() if sec in smap]) if flagged else {}
    new_text, changes, open_items = text, [], []
    for sec, reps in fixes.items():
        if not isinstance(reps, dict):
            continue
        for sid, x in reps.items():
            row = verdicts.get(sid)
            if not row or not x.get("new"):
                continue
            old_s, new_s = row["sentence"], ("" if str(x["new"]).strip().upper() == "CUT" else str(x["new"]).strip())
            if old_s not in new_text:
                open_items.append({"sid": sid, "reason": "sentence not found for replacement"})
                continue
            if any(k in old_s and k not in new_s for k in ("Tiwari", "1979")) or re.search(r"[\u0900-\u097F]", va.BRACKET.sub("", new_s)):
                open_items.append({"sid": sid, "reason": "fix dropped an editorial convention (Tiwari / 1979) or added Devanagari; rejected", "sentence": old_s})
                continue
            cand = re.sub(r"[ \t]{2,}", " ", new_text.replace(old_s, new_s, 1))
            b, a = check(new_text, P, None, targets), check(cand, P, None, targets)
            if a["integrity_ok"] and score_rep(a) <= score_rep(b):
                new_text = cand
                changes.append({"sid": sid, "old": old_s, "new": new_s or "CUT", "verdict_before": row["verdict"], "note": x.get("note", "")})
            else:
                open_items.append({"sid": sid, "reason": "fix made the code validation worse; reverted", "sentence": old_s, "verdict": row["verdict"]})
    changed = {}
    for c in changes:
        if c["new"] != "CUT":
            changed.setdefault(c["sid"].split("-")[0], []).append({"sid": c["sid"], "sentence": c["new"], "ids": [i for i in va.ids_in(c["new"]) if i != "AUTHOR"]})
    rres = R.parallel([(sec, vjob(sec, rows, "reverify", "reverify")) for sec, rows in changed.items()]) if changed else {}
    for sec, rows in changed.items():
        got = rres.get(sec) if isinstance(rres.get(sec), dict) else {}
        for r in rows:
            c = next(c for c in changes if c["sid"] == r["sid"])
            v = got.get(r["sid"])
            vv = str((v or {}).get("verdict", "UNVERIFIED")).upper()
            c["reverify"] = vv
            before = vf.RANK.get(c["verdict_before"], 0)
            if v is not None and vf.RANK.get(vv, -1) < before:
                new_text = new_text.replace(c["new"], c["old"], 1)
                c["reverted"] = True
                open_items.append({"sid": r["sid"], "reason": f"re-verified worse ({vv}); reverted"})
            else:
                verdicts[r["sid"]] = dict(verdicts[r["sid"]], sentence=c["new"], verdict=vv)
    for c in changes:
        if c["new"] == "CUT":
            verdicts.pop(c["sid"], None)
    st.update(verdicts_after=counts(verdicts), changes=changes, open=open_items,
              remaining=[v for v in verdicts.values() if v["verdict"] != "SUPPORTED"],
              rule_failures_after=vf.rule_checks(new_text, P, vf.cited_sentences(new_text)))
    (D / "ch02_verification.json").write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")
    write_spotcheck(new_text, P, verdicts, st["remaining"])
    return new_text, st


def write_spotcheck(text, P, verdicts, remaining):
    import random
    smap = vf.cited_sentences(text)
    rnd = random.Random(2026)
    L = ["# Chapter 2 spot-check\n", "Fifteen cited sentences at random (three per section) beside their evidence; then every sentence still not SUPPORTED.\n"]
    n = 0
    for sec, rows in smap.items():
        for r in rnd.sample(rows, min(3, len(rows))):
            n += 1
            v = next((x for x in verdicts.values() if x.get("sentence") == r["sentence"]), {})
            L.append(f"## {n}. Section {sec} — verdict: {v.get('verdict', 'n/a')}\n\n> {r['sentence']}\n")
            for i in r["ids"]:
                if i in P:
                    it = P[i]
                    L.append(f"- **{i}** — {it['book_title']}, {it['page']}" + (" *(kb-new)*" if "kb-new" in it["flags"] else "")
                             + f"\n  > {' '.join(it['quote'].split())}" + (f"\n  *English rendering:* {it['gloss']}" if it.get("gloss") else ""))
            L.append("")
    L.append("## Still flagged after fixes\n")
    L += [f"- **{v['sid']}** ({v['verdict']}): {v['sentence']}" for v in remaining] or ["*None.*"]
    (D / "ch02_spotcheck.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    st, R = run(a.dry_run)
    if a.dry_run:
        by = {}
        for c in R.calls:
            by.setdefault(c["round"], []).append(c)
        wall = sum(max(c["est_seconds"] for c in cs) for cs in by.values())
        print(json.dumps({"projected_cost_usd": round(R.spent, 2), "calls": len(R.calls),
                          "by_round": {r: {"calls": len(cs), "usd": round(sum(c["est_cost_usd"] for c in cs), 3)} for r, cs in sorted(by.items())},
                          "projected_wall_clock_min": round(wall / 60, 1)}, indent=1))
    else:
        for cmd in (["footnote.py", OUT.name], ["make_docx.py", OUT.stem + "_footnoted.md", OUT.stem + ".docx"]):
            subprocess.run([sys.executable, "-I", str(D / cmd[0])] + cmd[1:])
    print(f"[{ts()}] CH02 PIPELINE FINISHED", flush=True)
