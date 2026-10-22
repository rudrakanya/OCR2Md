"""Shared drafting pipeline (active chapter from UDAY_CFG).

Rounds:
  1  candidates (A, B per section; all parallel)            high
  2  code checks + judges (A, B [+ BASE = earlier draft])   high    — scores include SUBJECT FOCUS
  3  edits (judge improvements + check problems)            medium  — kept only if no worse
  4  stitch                                                 high    — kept only if no worse
  5  code validation + revisions (≤ 2 rounds)               medium
  5b length guard: expand sections under 92% of target from their own unused evidence (hard minimum)  medium
  6  citation-support verification + targeted fixes          medium  — never cut
  7  polish                                                 medium  — kept only if no worse; first to be cut
Budget: cfg BUDGET for all API stages of the chapter (shared log cfg LOG); cfg RESERVE kept for finishing.

  set UDAY_CFG=drafting/ch03/cfg_ch03.py
  python -I drafting/_pipe/pipeline.py --dry-run | (no flag = run)
"""
from __future__ import annotations

import argparse
import json
import random
import re
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from cfg import C  # noqa: E402
import run as rn  # noqa: E402
import validate as va  # noqa: E402
import verify as vf  # noqa: E402
import subject as sj  # noqa: E402

D = C.D
SECTIONS = C.SECTIONS
CAND = D / f"candidates_{C.VERSION}"
STEM = C.OUT.stem
META = re.compile(
    r"\bwill not be\b|\bwill remain\b|\bwill be (?:treated|read|kept|retained|presented|accepted|rejected|settled)\b|\bthis book\b|"
    r"\bthis chapter\b|\bthe narrative\b|\bwe cannot\b|\bit must be noted\b|\bit is important to\b|\bthe reader\b|"
    r"\bthis section\b|\bthe account must\b|\bthe enquiry\b|\bthe book (?:will|must|commits|keeps|treats)\b|"
    r"\bneed not be\b|\bmust remain\b|\bwithout (?:deciding|choosing|resolving|settling)\b|"
    # narrated caution or method (round 4b, 2026-10-14): state the substance instead
    r"\bused here\b|\bnot to reconstruct\b|\bnot an established\b|\bshould not be confused\b|\bcannot safely be\b|"
    r"\bwhat needs explaining\b|\bis a proposed (?:sequence|model|reading)\b", re.I)
BANNED = re.compile(r"\b(nestled|tapestry|testament to|stands as|rich history|steeped in|delve|bustling|timeless|hidden gem|in conclusion)\b", re.I)

SUBJECT_RULES = """UDAYPUR IS THE SUBJECT (binding; overrides anything above that conflicts):
1. Make the place the grammatical subject. Most sentences are about Udaypur and its surroundings — land, water, buildings, people, rulers, events, names, memories. Not "The Gazetteer gives about thirteen kilometres to Basoda; the author gives sixteen" but "Udaypur lies some thirteen to sixteen kilometres from Ganj Basoda [IDs]".
2. Attribution goes in the footnote (the bracketed IDs) by default. Name a source or author in the text only when the identity of the source matters to the point — competing scholarly datings, a tradition versus an inscription, an eyewitness account — and then briefly ("a local tradition holds…", "the inscriptions record…", "one later historian dated it to…"). At most ONE named source in the text per paragraph; no paragraph built around a source.
3. Banned (except under rule 2): "[source/author] says / writes / describes / records / notes / reports / calls / gives / places …"; "according to [title]"; "the author" for any writer; any sentence whose main point is what a book contains rather than what happened or what exists.
4. Minor discrepancies become ranges: small differences in distances, areas or counts are given as a range or an approximate figure ("about 55–70 km"), citing both items in the same bracket. Debate them in prose only if the difference matters historically.
5. Real conflicts stay conflicts, framed around the event or object: "Udayāditya's accession is dated variously to 1058, 1059 and c. 1070 [IDs]" — not "Patil gives…, Ganguly gives…, Pande gives…".
6. Inscriptions, the praśasti, slabs and grants are objects of the place: "the inscription records…" is fine. Their modern editors and every later writer are sources (rule 2)."""

BASE_BRIEF = """REGISTER: authoritative and measured, a chapter of a university-press history for educated general readers. Past tense for historical events; present tense for what exists today.

NEVER NARRATE METHOD: no sentences about what "will" or "will not" be claimed; no "this book", "this chapter", "the narrative", "the reader", "the enquiry"; no "need not be…", "must remain…". Uncertainty is shown by precise verbs and calibrated hedging (one precise qualifier where the evidence requires it — "probably", "is said to", "a tradition holds"; never stacked).

PARAGRAPHS: 120–200 words, each opening with a topic sentence about the place and containing at least one concrete, cited detail. Follow the section's paragraph plan.

QUOTATIONS: at most 2 per section, short, chosen for wording that matters, character-for-character from an item's QUOTE, in double quotation marks, followed by the ID; attributed in the text only if the speaker matters. Hindi/Sanskrit items: paraphrase in English, or quote the English rendering marked "(translation)". Never quote an item flagged ⚠.

SECTION ENDINGS: close on content that leads into the next section. No summaries, no rhetorical questions.

FACTS: only facts in the supplied items' QUOTE (and ENGLISH RENDERING). CONTEXT excerpts only help you keep each source's meaning and qualifications — never take a fact from them. No dates, names or numbers from general knowledge.

CITATIONS: every sentence that states a fact ends with its evidence ID(s) in square brackets, e.g. [C03-GAZ-007] or [C03-GAZ-007; C03-KB-PANDE-002]. Only supplied IDs.

STYLE: British/Indian English. "Udaypur" throughout (never "Udaipur" except for Udaipur in Rajasthan). Consistent diacritics: Udayāditya, Paramāra, Udayeśvara, praśasti, Bhūmija. Italicise Indian-language terms on first use with a half-clause gloss. The narrator never uses superlatives. Banned: nestled, tapestry, testament to, stands as, rich history, steeped in, delve, bustling, timeless, hidden gem, in conclusion.

OUTPUT: the section in Markdown, starting with its heading line exactly as given ("## <number> <title>"), and nothing else."""

WRITER_BRIEF = f"{C.CHAPTER_BRIEF}\n\n{BASE_BRIEF}\n\n{SUBJECT_RULES}"

JUDGE_SYS = """You are a senior editor at a university press judging versions of one section of a history chapter about Udaypur (Vidisha district, Madhya Pradesh) for general readers. LABELS: A and B are new candidates; BASE, if present, is the section from the previous draft.
Score each entry 1–10 on: fidelity (only supplied evidence; correct citations; real conflicts set out fairly and unresolved), coverage (the section's paragraph plan, key points, conflicts), subject_focus (the place — its land, water, buildings, people, rulers, events, names, memories — is the grammatical subject; sources live in footnotes; penalise HEAVILY sentences built on "[source] says/records/describes/gives/places", "according to [title]", "the author", paragraphs organised source by source, and minor numeric discrepancies debated instead of given as ranges), prose (topic sentences, concrete detail, varied sentences, strong opening), register (no meta-commentary, no announced caution, no superlatives), transition (fits the planned transitions; stays out of material covered elsewhere).
The automated check report (including the source-led sentences the code found) is supplied for each entry — weigh uncited claims, fabrication flags, meta-commentary and source-led counts heavily.
Pick the best entry. Then give 5–8 concrete, line-level improvements (quote the phrase; say exactly how to change it), aimed first at subject focus. You may name a paragraph in another entry to transplant (it keeps its IDs).
Return ONLY JSON: {"scores": {"A": {"fidelity":n,"coverage":n,"subject_focus":n,"prose":n,"register":n,"transition":n,"total":n}, "B": {...}, "BASE": {...}}, "best": "A|B|BASE", "improvements": ["..."], "transplants": ["..."], "rationale": "..."}"""

EDIT_SYS = """You revise one section of a history chapter about Udaypur. Apply ONLY the listed improvements (and transplants) and fix the listed automated-check problems — every source-led sentence must be rewritten so the place is the subject (the source stays in the bracketed IDs); every meta-commentary sentence rewritten or cut.
STRICT: no new facts, dates, names or numbers; every factual sentence keeps its bracketed evidence IDs (do not invent IDs); quotations stay verbatim or are cut whole; keep the heading line exactly; stay within the word range (do not shorten below it).
Return the full revised section in Markdown and nothing else."""

STITCH_SYS = """You are the final editor of a chapter of a university-press history of Udaypur. The sections were drafted in parallel: you own cross-section continuity. Smooth transitions using the planned transitions; remove repetition across sections (keep each point where the coverage map assigns it); keep one voice; keep the place as the grammatical subject (sources stay in the bracketed IDs); remove any meta-commentary.
STRICT: add no facts, dates, names or numbers; keep every bracketed evidence ID attached to its claim, unchanged; never change text inside quotation marks; keep each section's heading and keep each section's length (do not shorten: each section within 95–110% of its current length). British/Indian English; keep diacritics.
Return only the full chapter in Markdown."""

REVISE_SYS = """You fix specific problems in one section of a history chapter about Udaypur.
Fix ONLY the listed problems: cite uncited factual sentences with a supplied ID or delete the claim; replace non-verbatim quotations with the exact words of the cited QUOTE or paraphrase; delete or re-cite years/names not in the cited items; rewrite source-led sentences so the place is the subject (the source stays in the IDs); rewrite meta-commentary; adjust length to the word range using only supplied evidence. Add no new facts. Keep all other text, IDs and the heading.
Return the full corrected section in Markdown and nothing else."""

EXPAND_SYS = """You expand one section of a history chapter about Udaypur that is too short.
KEEP every existing sentence and its bracketed IDs (connective wording may change). ADD new sentences using the listed UNUSED EVIDENCE first (each with its ID), in the paragraphs where they belong, with the place as the grammatical subject.
STRICT: only facts in the supplied items' QUOTE or ENGLISH RENDERING; quotations verbatim, at most 2 in the section; no restatement of facts already given; no meta-commentary; no superlatives; keep the heading line exactly; paragraphs 120–200 words.
LENGTH IS A HARD REQUIREMENT: at least MINW words (IDs excluded) and at most MAXW.
Return the full section in Markdown and nothing else."""

POLISH_SYS = """Polish this history chapter at sentence level for a university press: tighten rhythm, vary sentence openings, cut repetition and remaining meta-commentary or stacked hedges, turn any remaining source-led sentence into one about the place (the source stays in the IDs), remove banned phrases (nestled, tapestry, testament to, stands as, rich history, steeped in, delve, bustling, timeless, hidden gem, in conclusion).
STRICT: no new facts, dates, names or numbers; every bracketed evidence ID stays attached to its claim, unchanged; text inside quotation marks unchanged; headings unchanged; do not shorten (keep each section's length).
Return only the full chapter in Markdown."""


def ts():
    return time.strftime("%H:%M:%S")


def section_ids(sec_text, P):
    return [i for i in dict.fromkeys(re.findall(r"C\d\d-[A-Z0-9-]+?-\d{3}", sec_text)) if i in P]


def fmt_item(i, context=True):
    flags = [f for f in i["flags"] if not f.startswith("also")]
    s = (f"[{i['id']}] {i['strength'].upper()} · {i['book_title']} · {i['page']}" + (f" · flags: {', '.join(flags)}" if flags else "")
         + "\nQUOTE (only this text may be quoted or used for facts): " + " ".join(i["quote"].split()))
    if i.get("gloss"):
        s += "\nENGLISH RENDERING (translation): " + i["gloss"]
    if i.get("claim"):
        s += f"\nCONFLICT POSITION: {i['claim'].get('key')} → {i['claim'].get('value')}"
    if context and i.get("context"):
        s += "\nCONTEXT (meaning/attribution only; not a source of facts): " + i["context"][:700]
    return s


def section_parts(secs):
    info = {}
    for k, txt in secs.items():
        purpose = (re.search(r"\*\*Purpose:\*\*\s*(.+)", txt) or [None, ""])[1]
        points = re.findall(r"(?m)^\d+\.\s+\*\*(.+?)\*\*", txt)
        trans = (re.search(r"\*\*Transition:\*\*\s*(.+)", txt) or [None, ""])[1]
        info[k] = {"purpose": purpose.strip(), "points": points, "transition": trans.strip()}
    return info


def covered_elsewhere(sec, info, titles):
    return "\n".join(f"- {titles[k]}: {info[k]['purpose']} Key points: " + "; ".join(info[k]["points"]) for k in SECTIONS if k != sec)


def transitions(sec, info, titles):
    i = SECTIONS.index(sec)
    inc = f"from {titles[SECTIONS[i - 1]]}: {info[SECTIONS[i - 1]]['transition']}" if i else f"none — this section opens the chapter. {C.OPEN_IN}"
    out = info[sec]["transition"] + (f" (leads into {titles[SECTIONS[i + 1]]})" if i + 1 < len(SECTIONS) else f" (closing lead: {C.CLOSE_OUT})")
    return inc, out


# ---------------------------------------------------------------- checks
def check(text, P, sec=None, targets=None):
    rep = va.check(text, P, sec, targets)
    rep["meta"] = [va.BRACKET.sub("", s).strip()[:220] for s in va.sentences(text) if META.search(va.BRACKET.sub("", s))]
    rep["banned"] = sorted({m.group(0).lower() for m in BANNED.finditer(text)})
    return rep


def n_source_led(rep):
    return sum(v["flagged"] for v in rep.get("subject", {}).values())


def problems_of(rep):
    out = [f"invalid ID {x}" for x in rep["invalid_ids"]]
    out += [f"quotation not verbatim in the cited item(s) {q['cited']}: \"{q['quote']}\"" for q in rep["nonverbatim_quotes"]]
    out += [f"quotation from a ⚠ item: \"{q}\"" for q in rep["warn_quotes"]]
    out += [f"uncited factual sentence: {s}" for s in rep["uncited_claims"]]
    out += [f"not supported by the cited items: {s}" for s in rep["fabrication"]]
    out += rep["word_issues"]
    out += [f"conflict not presented with all sides: {c['conflict']}" for c in rep["conflicts"] if not c["present"]]
    out += [f"meta-commentary sentence (rewrite to state substance, or cut): {m}" for m in rep.get("meta", [])]
    out += [f"banned phrase: {b}" for b in rep.get("banned", [])]
    out += [f"monotony: {m}" for m in rep.get("monotony", [])]
    for k, rows in rep.get("subject_detail", {}).items():
        out += [f"source-led sentence (make the place the subject; the source stays in the IDs): {r['sentence']}" for r in rows]
    return out


def score_rep(rep):
    sub = rep.get("subject", {})
    return ((0 if rep["integrity_ok"] else 1000) + 3 * len(rep["uncited_claims"]) + 3 * len(rep["fabrication"])
            + 5 * len(rep["word_issues"]) + 5 * sum(not c["present"] for c in rep["conflicts"]) + 4 * len(rep.get("meta", []))
            + 2 * len(rep.get("banned", [])) + 3 * n_source_led(rep) + 8 * sum(not v["pass"] for v in sub.values())
            + 3 * len(rep.get("monotony", [])))


def summ(rep):
    s = va.summary(rep)
    s["meta"] = len(rep.get("meta", []))
    s["banned"] = rep.get("banned", [])
    return s


# ---------------------------------------------------------------- main
def run(dry):
    t_start = time.time()
    print(f"[{ts()}] chapter {C.CH} {C.VERSION} pipeline start (dry={dry})", flush=True)
    outline, secs, targets, titles = va.load_outline()
    P = va.load_pack()
    info = section_parts(secs)
    R = rn.Run(dry)
    stage_t = {}
    state = {"chapter": C.CH, "version": C.VERSION, "model": rn.MODEL, "effort": rn.EFFORT, "budget": rn.BUDGET,
             "reserve": rn.RESERVE, "spend_before_drafting": round(R.prior, 4), "sections": {}, "decisions": []}
    ids = {s: section_ids(secs[s], P) for s in SECTIONS}
    voice = ""
    if getattr(C, "VOICE_SRC", None) and C.VOICE_SRC.exists():
        vt = re.sub(r"(?m)^#.*$", "", C.VOICE_SRC.read_text(encoding="utf-8"))
        voice = " ".join(re.sub(r"\[[^\]]+\]", "", vt).split()[:350])
    base = {}
    if getattr(C, "BASELINE", None) and C.BASELINE.exists():
        base = {k: v.strip() for k, v in va.split_sections(C.BASELINE.read_text(encoding="utf-8")).items()}

    def prompt(sec):
        inc, outg = transitions(sec, info, titles)
        u = (f"THE WHOLE CHAPTER OUTLINE:\n{outline}\n\nSECTION TO WRITE NOW: {titles[sec]}\nSection plan:\n{secs[sec]}\n\n"
             f"WORD TARGET: {targets[sec]} words (must land {int(targets[sec] * 0.95)}–{int(targets[sec] * 1.1)}), IDs excluded. Do not fall short.\n\n"
             f"COVERED ELSEWHERE (do not develop):\n{covered_elsewhere(sec, info, titles)}\n\nPLANNED INCOMING TRANSITION: {inc}\nPLANNED OUTGOING TRANSITION: {outg}\n\n"
             + (f"VOICE SAMPLE (register and rhythm only; its source-led sentences are NOT a model — the subject rules win):\n{voice}\n\n" if voice else "")
             + f"EVIDENCE FOR THIS SECTION ({len(ids[sec])} items):\n" + "\n\n".join(fmt_item(P[i]) for i in ids[sec]))
        return WRITER_BRIEF, u

    # ===== round 1: candidates
    t = time.time()
    cands = {s: {} for s in SECTIONS}
    jobs = []
    for sec in SECTIONS:
        for L in "AB":
            p = CAND / f"{sec}_{L}.md"
            if p.exists() and not dry:
                cands[sec][L] = p.read_text(encoding="utf-8")
                continue
            def job(sec=sec, L=L):
                system, u = prompt(sec)
                opening = {"A": "OPENING: lead with a concrete fact or scene about the place, from the evidence.",
                           "B": "OPENING: lead with the section's central point stated as a claim about the place (not a rhetorical question)."}[L]
                out = R.call(f"cand_{sec}_{L}", 1, "candidate", system, u + "\n\n" + opening, targets[sec] + 200)
                if out is None:
                    return f"## {titles[sec]}\n" + (f"Udaypur lorem ipsum [{ids[sec][0]}]. " * (targets[sec] // 4))
                if out and not dry:
                    CAND.mkdir(exist_ok=True)
                    (CAND / f"{sec}_{L}.md").write_text(out.strip(), encoding="utf-8")
                return out.strip()
            jobs.append(((sec, L), job))
    for (sec, L), r in R.parallel(jobs).items():
        if isinstance(r, str) and r.strip():
            cands[sec][L] = r
        elif isinstance(r, rn.BudgetStop):
            state["budget_stop"] = str(r)
    for sec in SECTIONS:
        if sec in base:
            cands[sec]["BASE"] = base[sec]
    stage_t["1_candidates"] = round(time.time() - t)

    # ===== round 2: judges
    t = time.time()
    jobs = []
    reps_all = {}
    for sec in SECTIONS:
        labels = sorted(cands[sec])
        reps = {L: check(cands[sec][L], P, sec, targets) for L in labels}
        reps_all[sec] = reps
        alive = [L for L in labels if reps[L]["integrity_ok"] or L == "BASE"] or [min(labels, key=lambda L: score_rep(reps[L]))]
        state["sections"][sec] = {"entries": {L: {"words": reps[L]["words"].get(sec), "check": summ(reps[L])} for L in labels}, "alive": alive}
        def job(sec=sec, alive=alive, reps=reps):
            inc, outg = transitions(sec, info, titles)
            ju = (f"WRITER BRIEF:\n{WRITER_BRIEF}\n\nSECTION PLAN:\n{secs[sec]}\n\nWORD TARGET: {targets[sec]} (90–110%)\n\n"
                  f"COVERED ELSEWHERE:\n{covered_elsewhere(sec, info, titles)}\n\nPLANNED TRANSITIONS: in — {inc}; out — {outg}\n\n"
                  + "EVIDENCE:\n" + "\n\n".join(fmt_item(P[i], False) for i in dict.fromkeys(ids[sec] + [x for L in alive for x in va.ids_in(cands[sec][L]) if x in P])) + "\n\n"
                  + "\n\n".join(f"=== ENTRY {L} ===\nAUTOMATED CHECKS: {json.dumps(problems_of(reps[L])[:30], ensure_ascii=False)}\n\n{cands[sec][L]}" for L in alive))
            out = R.call(f"judge_{sec}", 2, "judge", JUDGE_SYS, ju, 900)
            return rn.parse_json(out) if out else None
        jobs.append((sec, job))
    res = R.parallel(jobs)
    verdicts = {}
    for sec in SECTIONS:
        alive = state["sections"][sec]["alive"]
        v = res.get(sec)
        v = v if isinstance(v, dict) else {"best": [L for L in alive if L != "BASE"][0] if [L for L in alive if L != "BASE"] else alive[0],
                                           "improvements": [], "scores": {}, "rationale": "judge unavailable"}
        if v.get("best") not in alive:
            v["best"] = alive[0]
        # baseline rule: a new candidate replaces BASE only if it scores higher on subject focus without losing on fidelity
        sc = v.get("scores", {})
        if "BASE" in alive and v["best"] != "BASE" and sc.get("BASE") and sc.get(v["best"]):
            b, n = sc["BASE"], sc[v["best"]]
            if not (n.get("subject_focus", 0) > b.get("subject_focus", 0) and n.get("fidelity", 0) >= b.get("fidelity", 0)):
                v["baseline_rule"] = f"{v['best']} did not beat BASE on subject focus with fidelity ≥ BASE; BASE kept"
                v["best"] = "BASE"
        elif "BASE" in alive and v["best"] == "BASE":
            v["baseline_rule"] = "judge preferred BASE"
        verdicts[sec] = v
        state["sections"][sec]["judge"] = v
        if not dry:
            (D / f"judge_{C.VERSION}_{sec}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
    stage_t["2_judges"] = round(time.time() - t)

    # ===== budget plan for the rest (cut order: polish, then edits; verification never cut)
    skip_polish = skip_edit = False
    if not dry:
        est_rest = 5 * 0.06 + 0.25 + 0.30 + 0.25 + 0.55 + 0.15
        avail = rn.BUDGET - R.spent
        if est_rest > avail:
            skip_polish = True
            state["decisions"].append(f"est ${est_rest:.2f} > ${avail:.2f} left: polish skipped")
            if est_rest - 0.15 > avail:
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
            eu = (f"WRITER BRIEF (for reference):\n{WRITER_BRIEF}\n\nWORD RANGE: {int(tg * 0.95)}–{int(tg * 1.1)} words (IDs excluded).\n\nIMPROVEMENTS TO APPLY:\n"
                  + "\n".join(f"- {x}" for x in v.get("improvements", []))
                  + ("\nTRANSPLANTS:\n" + "\n".join(f"- {x}" for x in v.get("transplants", [])) if v.get("transplants") else "")
                  + "\nAUTOMATED-CHECK PROBLEMS TO FIX:\n" + "\n".join(f"- {p}" for p in problems_of(freps[sec])[:30])
                  + "\n\nEVIDENCE (the only permitted facts):\n" + "\n\n".join(fmt_item(P[i], False) for i in dict.fromkeys(ids[sec] + [x for x in va.ids_in(finals[sec]) if x in P]))
                  + f"\n\n=== SECTION TO REVISE ===\n{finals[sec]}\n\n{others}")
            return R.call(f"edit_{sec}", 3, "edit", EDIT_SYS, eu, tg + 100)
        jobs.append((sec, job))
    for sec, out in R.parallel(jobs).items():
        if isinstance(out, str) and out.strip():
            er = check(out.strip(), P, sec, targets)
            keep = er["integrity_ok"] and score_rep(er) <= score_rep(freps[sec]) and out.strip().startswith("## " + sec)
            state["sections"][sec]["edit"] = {"kept": keep, "before": summ(freps[sec]), "after": summ(er)}
            if keep:
                finals[sec], freps[sec] = out.strip(), er
    stage_t["3_edits"] = round(time.time() - t)
    joined = "\n\n".join(finals[s].strip() for s in SECTIONS if s in finals) + "\n"
    if not dry:
        (D / f"{STEM}_prestitch.md").write_text(joined, encoding="utf-8")

    # ===== round 4: stitch
    t = time.time()
    chapter, rep = joined, check(joined, P, None, targets)
    cmap = "\n".join(f"- {titles[k]} owns: {info[k]['purpose']} Key points: " + "; ".join(info[k]["points"]) for k in SECTIONS)
    tmap = "\n".join(f"- after {titles[k]}: {info[k]['transition']}" for k in SECTIONS)
    try:
        out = R.call("stitch", 4, "stitch", STITCH_SYS, f"CHAPTER OPENING: {C.OPEN_IN}\nCHAPTER CLOSING: {C.CLOSE_OUT}\n\nCOVERAGE MAP:\n{cmap}\n\n"
                     f"PLANNED TRANSITIONS:\n{tmap}\n\nWORD TARGETS: " + ", ".join(f"{k} {targets[k]}" for k in SECTIONS) + f"\n\nDRAFT TO EDIT:\n{joined}",
                     sum(targets.values()) + 300)
        if out:
            st = out.strip() + "\n"
            sr = check(st, P, None, targets)
            keep = sr["integrity_ok"] and score_rep(sr) <= score_rep(rep)
            state["stitch"] = {"kept": keep, "before": summ(rep), "after": summ(sr)}
            if keep:
                chapter, rep = st, sr
            if not dry:
                (D / f"{STEM}_stitched_raw.md").write_text(st, encoding="utf-8")
    except rn.BudgetStop as e:
        state["stitch"] = {"kept": False, "reason": f"budget: {e}"}
    stage_t["4_stitch"] = round(time.time() - t)
    state["validation_before_revision"] = summ(rep)

    # ===== round 5: revisions (≤ 2) + length guard
    t = time.time()
    state["revisions"] = []
    for rnd in (1, 2):
        parts = va.split_sections(chapter)
        bad = {s: check(parts[s], P, s, targets) for s in SECTIONS if s in parts}
        bad = {s: r_ for s, r_ in bad.items() if problems_of(r_)}
        if not bad or dry:
            break
        def mk(s, r_, rnd=rnd):
            def job():
                tg = targets[s]
                ru = ("PROBLEMS TO FIX:\n" + "\n".join(f"- {p}" for p in problems_of(r_)[:30]) +
                      f"\n\nWORD RANGE: {int(tg * 0.95)}–{int(tg * 1.1)}\n\nEVIDENCE:\n" + "\n\n".join(fmt_item(P[i], False) for i in dict.fromkeys(ids[s] + [x for x in va.ids_in(parts[s]) if x in P]))
                      + f"\n\n=== SECTION ===\n{parts[s]}")
                return R.call(f"revise_r{rnd}_{s}", 5, "revise", REVISE_SYS, ru, tg)
            return job
        try:
            res = R.parallel([(s, mk(s, r_)) for s, r_ in bad.items()])
        except rn.BudgetStop:
            break
        for s, out in res.items():
            if isinstance(out, str) and out.strip():
                nr = check(out.strip(), P, s, targets)
                keep = nr["integrity_ok"] and score_rep(nr) < score_rep(bad[s]) and out.strip().startswith("## " + s)
                state["revisions"].append({"round": rnd, "section": s, "problems": len(problems_of(bad[s])), "after": len(problems_of(nr)), "kept": keep})
                if keep:
                    parts[s] = out.strip() + "\n"
        chapter = "\n\n".join(parts[s].strip() for s in SECTIONS if s in parts) + "\n"
    # length guard (Chapter 2 lesson: models undershoot and every later pass shortens)
    parts = va.split_sections(chapter)
    short = {s: va.words(parts[s]) for s in SECTIONS if s in parts and va.words(parts[s]) < targets[s] * 0.92}
    total = sum(va.words(parts[s]) for s in parts)
    if total < C.WMIN:
        for s in SECTIONS:
            if s in parts and va.words(parts[s]) < targets[s] * 0.97:
                short.setdefault(s, va.words(parts[s]))
    state["length_guard"] = {"short": short}
    if short and not dry:
        def ej(s):
            def job():
                lo, hi = int(targets[s] * 0.97), int(targets[s] * 1.07)
                used = set(va.ids_in(parts[s]))
                unused = [i for i in ids[s] if i not in used] + [i for i in getattr(C, "EXTRA_POOL", {}).get(s, []) if i in P and i not in used]
                u = (f"CURRENT LENGTH: {va.words(parts[s])} words. REQUIRED: {lo}–{hi}.\n\nUNUSED EVIDENCE (use these first):\n"
                     + "\n\n".join(fmt_item(P[i], False) for i in unused) + "\n\nOTHER EVIDENCE ALREADY CITED:\n"
                     + "\n\n".join(fmt_item(P[i], False) for i in used if i in P) + f"\n\nWRITER BRIEF:\n{WRITER_BRIEF}\n\n=== SECTION TO EXPAND ===\n{parts[s]}")
                return R.call(f"expand_{s}", 5, "expand", EXPAND_SYS.replace("MINW", str(lo)).replace("MAXW", str(hi)), u, hi + 60)
            return job
        try:
            res = R.parallel([(s, ej(s)) for s in short])
        except rn.BudgetStop:
            res = {}
        for s, out in res.items():
            if isinstance(out, str) and out.strip():
                b, nr = check(parts[s], P, s, targets), check(out.strip(), P, s, targets)
                keep = (nr["integrity_ok"] and va.words(out) > va.words(parts[s]) and out.strip().startswith("## " + s)
                        and score_rep(nr) <= score_rep(b) + 3)
                state["length_guard"][s] = {"before": va.words(parts[s]), "after": va.words(out), "kept": keep, "problems": problems_of(nr)[:8]}
                if keep:
                    parts[s] = out.strip() + "\n"
        chapter = "\n\n".join(parts[s].strip() for s in SECTIONS if s in parts) + "\n"
    rep = check(chapter, P, None, targets)
    state["validation_after_revision"] = summ(rep)
    stage_t["5_revisions_length"] = round(time.time() - t)
    if not dry:
        (D / f"{STEM}_preverify.md").write_text(chapter, encoding="utf-8")

    # ===== round 6: verification (never cut)
    t = time.time()
    if not dry:
        chapter, vstate = verify(chapter, P, R, targets)
        state["verification"] = {k: vstate[k] for k in ("verdicts_before", "verdicts_after")}
    else:
        for sec in SECTIONS:
            R.call(f"verify_{sec}", 6, "verify", vf.VERIFY_SYS, "x" * 26000, 1500)
            R.call(f"fix_{sec}", 6, "fix", vf.FIX_SYS, "x" * 14000, 300)
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
                keep = pr["integrity_ok"] and score_rep(pr) <= score_rep(rep) and _guards_ok(chapter, pol)
                state["polish"] = {"kept": keep, "before": summ(rep), "after": summ(pr)}
                if keep:
                    chapter, rep = pol, pr
                if not dry:
                    (D / f"{STEM}_polished_raw.md").write_text(pol, encoding="utf-8")
        except rn.BudgetStop as e:
            state["polish"] = {"kept": False, "reason": f"budget: {e}"}
    stage_t["7_polish"] = round(time.time() - t)
    state["final_validation"] = summ(rep)
    state["final_validation_detail"] = rep
    state["rule_checks_final"] = vf.rule_checks(chapter, P, vf.cited_sentences(chapter)) if not dry else []
    state["stage_seconds"] = stage_t
    state["wall_clock_seconds"] = round(time.time() - t_start)
    state["calls"] = R.calls
    state["spent_usd"] = round(R.spent, 4)
    state["spend_by_stage"] = {k: round(v, 4) for k, v in R.stage_spend.items()}
    if not dry:
        C.OUT.write_text(chapter, encoding="utf-8")
    (D / (f"{STEM}_estimate.json" if dry else f"{STEM}_state.json")).write_text(json.dumps(state, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return state, R


def _guards_ok(old, new):
    """editorial conventions a model pass must not drop or break"""
    for k in ("Vijay Manohar Tiwari", "1979"):
        if k in old and k not in new:
            return False
    if re.search(r"[ऀ-ॿ]", va.BRACKET.sub("", new)) and not re.search(r"[ऀ-ॿ]", va.BRACKET.sub("", old)):
        return False
    return True


def verify(text, P, R, targets):
    smap = vf.cited_sentences(text)
    rules = vf.rule_checks(text, P, smap)

    def vjob(sec, rows, name="verify", kind="verify"):
        def job():
            iids = sorted({i for r in rows for i in r["ids"] if i in P})
            u = vf.CONVENTIONS + "EVIDENCE ITEMS:\n" + "\n\n".join(vf.item_text(P[i]) for i in iids) + "\n\nSENTENCES TO CHECK:\n" + "\n".join(f"{r['sid']}: {r['sentence']}" for r in rows)
            out = R.call(f"{name}_{sec}", 6, kind, vf.VERIFY_SYS, u, 60 * len(rows))
            j = rn.parse_json(out) or {}
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
    flagged = {}
    for sid, v in verdicts.items():
        if v["verdict"] != "SUPPORTED":
            flagged.setdefault(sid.split("-")[0], []).append((sid, v["verdict"], v.get("fix", ""), v.get("evidence", "")))
    for f in rules:
        if f.get("sid"):
            flagged.setdefault(f["sec"], []).append((f["sid"], "RULE: " + f["rule"], f["detail"], ""))
    for sec, rows in smap.items():
        for r in rows:
            plain = va.BRACKET.sub("", r["sentence"])
            if META.search(plain):
                flagged.setdefault(sec, []).append((r["sid"], "META-COMMENTARY", "state the substance, or cut", ""))
            why = sj.source_led(plain)
            if why:
                flagged.setdefault(sec, []).append((r["sid"], "SOURCE-LED", f"{why}: make the place the subject; the source stays in the IDs", ""))

    def fjob(sec, items):
        def job():
            rows = {sid: verdicts.get(sid) for sid, *_ in items if verdicts.get(sid)}
            iids = sorted({i for sid in rows for i in rows[sid]["ids"] if i in P})
            u = vf.CONVENTIONS + "EVIDENCE ITEMS:\n" + "\n\n".join(vf.item_text(P[i]) for i in iids) + "\n\nFLAGGED SENTENCES:\n" + \
                "\n".join(f"{sid}: {rows[sid]['sentence']}\n   problem: {vd}; suggested fix: {fx}; evidence: {ev}" for sid, vd, fx, ev in items if sid in rows)
            out = R.call(f"fix_{sec}", 6, "fix", vf.FIX_SYS, u, 60 * len(items))
            j = rn.parse_json(out) if out else None
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
            if any(k in old_s and k not in new_s for k in ("Tiwari", "1979")) or (re.search(r"[ऀ-ॿ]", va.BRACKET.sub("", new_s))) \
                    or (new_s and sj.source_led(va.BRACKET.sub("", new_s)) and not sj.source_led(va.BRACKET.sub("", old_s))):
                open_items.append({"sid": sid, "reason": "fix dropped a convention, added Devanagari or made the sentence source-led; rejected", "sentence": old_s})
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
            if v is not None and vf.RANK.get(vv, -1) < vf.RANK.get(c["verdict_before"], 0):
                new_text = new_text.replace(c["new"], c["old"], 1)
                c["reverted"] = True
                open_items.append({"sid": r["sid"], "reason": f"re-verified worse ({vv}); reverted"})
            else:
                verdicts[r["sid"]] = dict(verdicts[r["sid"]], sentence=c["new"], verdict=vv if v is not None else verdicts[r["sid"]]["verdict"])
    for c in changes:
        if c["new"] == "CUT":
            verdicts.pop(c["sid"], None)
    st.update(verdicts_after=counts(verdicts), changes=changes, open=open_items,
              remaining=[v for v in verdicts.values() if v["verdict"] != "SUPPORTED"],
              rule_failures_after=vf.rule_checks(new_text, P, vf.cited_sentences(new_text)))
    (D / f"{STEM}_verification.json").write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")
    write_spotcheck(new_text, P, verdicts, st["remaining"])
    return new_text, st


def write_spotcheck(text, P, verdicts, remaining):
    smap = vf.cited_sentences(text)
    rnd = random.Random(2026)
    L = [f"# Chapter {C.CH} {C.VERSION} spot-check\n", "Fifteen cited sentences at random (three per section) beside their evidence; then every sentence still not SUPPORTED.\n"]
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
    (D / f"{STEM}_spotcheck.md").write_text("\n".join(L) + "\n", encoding="utf-8")


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
        print(json.dumps({"chapter": C.CH, "projected_cost_usd": round(R.spent, 2), "calls": len(R.calls),
                          "by_round": {r: {"calls": len(cs), "usd": round(sum(c["est_cost_usd"] for c in cs), 3)} for r, cs in sorted(by.items())},
                          "projected_wall_clock_min": round(wall / 60, 1)}, indent=1))
    else:
        for cmd in (["footnote.py", str(C.OUT)], ["make_docx.py"]):
            subprocess.run([sys.executable, "-I", str(HERE / cmd[0])] + cmd[1:])
    print(f"[{ts()}] CHAPTER {C.CH} PIPELINE FINISHED", flush=True)
