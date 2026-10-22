"""Authored-history pipeline (active chapter from UDAY_CFG; cfg AUTHORED = True).

Facts stay cited exactly as before; the author's interpretation is written in the author's own voice and marked [INT];
source debates go to discursive notes {{note: explanation [IDs]}}.

Rounds:
  1  candidates — 2 per section in parallel (1 if the budget plan cuts it)        default model, effort CAND_EFFORT (high)
     prompt: writer brief + style brief (no exemplars) + thesis + the section's interpretive claims + evidence (with
     context excerpts) + covered elsewhere + planned transitions
  2  code checks, then a judge per section: A, B and BASE (the current draft's section); scores fidelity, argument,
     analysis_vs_summary, subject_focus, voice, prose, transition; fidelity < 6 is out regardless
  3  edit (judge improvements + check problems), kept only if no worse                  [cut 2nd]
  4  stitch — one thesis through all sections, one voice                                 kept only if no worse
  5  author's pass — flagship model, whole chapter (never cut)                         kept only if no worse
  6  verification — FACT-SUPPORTED / FACT-PARTIAL / FACT-UNSUPPORTED / INT-SOUND / INT-OVERREACH / NEW-FACT /
     MISREPRESENTED, sentence by sentence (and every note); one round of targeted fixes; re-verify the changed (never cut)
  7  polish — kept only if no worse                                                    [cut 1st]
Budget: cfg BUDGET (8.00) with cfg RESERVE (1.00). Models: OPENAI_MODEL (default gpt-6.1-sol), OPENAI_MODEL_FLAGSHIP.

  set UDAY_CFG=...; python -I drafting/_pipe/pipeline2.py --dry-run | (no flag = run)
"""
from __future__ import annotations

import argparse
import json
import os
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
import pipeline as p1  # noqa: E402

D, SECTIONS = C.D, C.SECTIONS
CAND = D / f"candidates_{C.VERSION}"
STEM = C.OUT.stem
STYLE = C.D.parent / "style"
rn.EFFORT.update({k: "high" for k in ("candidate", "judge", "edit", "stitch", "revise", "polish", "verify", "fix", "reverify", "author")})
CAND_EFFORT = os.getenv("CAND_EFFORT", "high")

AUTHORED_RULES = """FACTS AND INTERPRETATION (binding):
1. FACTS ARE CITED. Every statement of fact — a date, name, number, event, physical description or attributed view — ends with its evidence ID(s) in square brackets, exactly as supplied.
2. INTERPRETATION IS YOUR OWN VOICE. Interpretive sentences need no citation, provided they follow from facts cited in the same or the preceding paragraph and introduce NO new fact (no date, name, number or event not already cited there). Mark each one at its end, after the full stop, with its function: [INT:cause] (explains a cause or reason), [INT:consequence] (draws a consequence the facts imply but do not state), [INT:comparison] (compares or contrasts across time or place, using cited facts), [INT:tension] (names the tension between two pieces of evidence), or [INT:thesis] (connects the point to the chapter's thesis). Every paragraph has at least one; there is no quota beyond that.
3. INTERPRETATION ADDS INSIGHT. The restatement test: if a reader who had just read the cited facts would already know what the sentence says, cut it. These fail: "These hillocks give Udaypur a visible presence before arrival." "The temple adds a different kind of landmark to the hillocks." Every interpretive sentence names something concrete (this river, this inscription, this distance, this ruler); generic significance ("rich heritage", "stands as a reminder", "speaks volumes", "a testament", "shaped the destiny") is banned. No paragraph is pure interpretation.
3a. COMBINE FACTS. Facts that serve one point go into one sentence, with their IDs at the end of the clause or sentence they support (a sentence may carry several IDs). Never line facts up one per sentence: a paragraph in which most sentences are short single-ID statements fails.
3b. SETTLED RANGES. Where the canon gives a range (e.g. Udaypur lies about 13–16 km from Ganj Basoda and 55–70 km from Vidisha), give the range with both items cited; never narrow a settled range to one source's figure.
4. SOURCE DEBATES GO TO THE NOTES. Where sources disagree, the main text states the historical question and its stakes ("the date of Udayāditya's accession decides whether …"); who argues what goes into a discursive note written as {{note: explanation of the disagreement [IDs]}} placed right after the sentence. A note's explanation obeys the fact rules (only facts from its cited items).
5. OPENINGS AND CLOSINGS. The chapter opens on a concrete scene or object that carries its thesis; every section ends by moving the argument forward; the chapter's last paragraph leads into the next chapter.
6. The thesis runs through every section: each section makes its assigned interpretive claims, in its own words, grounded in its cited facts.
7. EACH PARAGRAPH DELIVERS ITS WRITTEN POINT. Every paragraph in the plan carries a **Point** (with its function). Build the paragraph so that its cited facts lead to that point, and express the point as the paragraph's [INT:function] sentence(s), with the function given. You may sharpen the wording; you may not change the claim, strengthen it, or replace it with another. Keep the plan's paragraph order, one plan paragraph per paragraph.
8. VARY THE INTERPRETATION. The interpretive sentence need not come last: put it where the argument turns, early as a governing claim, mid-paragraph between two pieces of evidence, or last as the consequence. A paragraph that turns on a tension may carry two interpretive sentences. Do not end every paragraph on a one-line [INT:consequence].
9. CALIBRATION FAILURES TO AVOID (do not reuse or imitate):
   - restatement: "The roads define a village through its neighbours; the temple gives arrival a focus of its own." (says only what the route facts already show)
   - overreach: "The inhabited mound's security therefore rests on land beyond its buildings." (no cited item speaks of security; "dependence" is what the facts support)
   - muddled: "Here, the exposed sandstone makes height a potential resource for building." (erosion exposes the stone, not height; the real link is the temple's stone quarried in the hill close by)
   - acceptable: "Missing inscriptions cannot turn royal foundation into first habitation." (names the tension between an absence and a claim)
10. Vijay Manohar Tiwari is a witness and the author of Jagta Hua Kasba (testimony): never call Tiwari "a visitor", "a traveller" or "a tourist"."""


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else ""


STYLE_PROFILE = _read(STYLE / "style_profile.md")
BRIEF_TEXT = _read(C.INTERP_BRIEF)


def brief_parts():
    thesis = (re.search(r"(?s)## Thesis\s*\n(.*?)(?=\n## )", BRIEF_TEXT) or [None, ""])[1].strip()
    secs = {}
    for part in re.split(rf"\n(?=## {C.CH}\.\d)", BRIEF_TEXT)[1:]:
        k = re.match(rf"## ({C.CH}\.\d)", part).group(1)
        secs[k] = re.split(r"\n## (?:Questions|Unsupported)", part)[0].strip()
    questions = (re.search(r"(?s)## Questions.*?\n(.*?)(?=\n## |\Z)", BRIEF_TEXT) or [None, ""])[1].strip()
    return thesis, secs, questions


THESIS, SEC_BRIEF, QUESTIONS = brief_parts()
POINT_RE = re.compile(r"\n\d\. \*\*(P\d) — ([^\n]*)\n\s*- \*\*Point\*\* \*\(([a-z]+)\)\*: ([^\n]+)")


def points_of(plan):
    """[(P1, paragraph title, function, point), ...] from a section plan"""
    return [(m.group(1), m.group(2).strip("*. "), m.group(3), m.group(4).strip()) for m in POINT_RE.finditer("\n" + plan)]


def points_block(plan):
    return "\n".join(f"- {k} ({t}) [INT:{f}]: {pt}" for k, t, f, pt in points_of(plan))
STYLE_BLOCK = f"STYLE BRIEF (craft for narrative history of India — binding):\n{STYLE_PROFILE}\n\n" if STYLE_PROFILE else ""   # no exemplars are fed to any drafting call
WRITER_BRIEF = f"{C.CHAPTER_BRIEF}\n\n{p1.BASE_BRIEF}\n\n{p1.SUBJECT_RULES}\n\n{AUTHORED_RULES}"

JUDGE_SYS = """You are the senior editor of a university-press history of India, choosing the best version of one section of a chapter about Udaypur (Vidisha district, Madhya Pradesh). A and B are new candidates; BASE is the same section of the current draft.
Score each entry 1–10 on:
- fidelity: every fact cited and supported by the supplied evidence; [INT] sentences add no new fact; disagreements set out fairly (in notes)
- argument: the section advances the chapter thesis and makes its assigned interpretive claims, AND each paragraph delivers its written POINT (listed below) through its [INT] sentence(s), led up to by its facts — not a different, weaker or stronger claim. Penalise each missing or altered point
- analysis_vs_summary: it interprets, connects and weighs rather than reporting what sources say in order; every paragraph has at least one interpretive sentence that explains a cause, draws an unstated consequence, compares across time or place, names a tension between pieces of evidence, or connects to the thesis. Penalise HEAVILY any INT-TRIVIAL sentence — an [INT] sentence that only restates what the cited facts already say (e.g. "These hillocks give Udaypur a visible presence before arrival") — and paragraphs that line facts up one per sentence
- subject_focus: Udaypur and its landscape are the grammatical subject; sources live in the notes
- voice: matches the style profile (stance, paragraph architecture, rhythm, Indic terms)
- prose: concrete, varied, exact; no generic significance, no clichés, no false drama
- transition: fits the planned transitions and stays out of material covered elsewhere
Also penalise interpretation that is always placed last and always labelled consequence, and any call of Tiwari "a visitor".
The automated check report for each entry is supplied (uncited claims, new facts in [INT] sentences, paragraphs without interpretation, fact-per-sentence paragraphs, narrowed settled ranges, source-led sentences) — weigh it. An entry with fidelity below 6 cannot win.
Return ONLY JSON: {"scores": {"A": {"fidelity":n,"argument":n,"analysis_vs_summary":n,"subject_focus":n,"voice":n,"prose":n,"transition":n,"total":n}, "B": {...}, "BASE": {...}}, "points_missed": {"A": ["P#: missing / weakened / changed / overstated"], "B": [], "BASE": []}, "best": "A|B|BASE", "improvements": ["5–8 concrete line-level changes: quote the phrase, say exactly how to change it"], "transplants": ["..."], "rationale": "..."}"""

EDIT_SYS = """You revise one section of a history chapter about Udaypur. Apply ONLY the listed improvements (and transplants) and fix the listed automated-check problems.
STRICT: no new facts, dates, names or numbers; every factual sentence keeps its bracketed evidence IDs; every interpretive sentence keeps its [INT:function] label and introduces no new fact; {{note: …}} blocks keep their wording and IDs unless a listed fix concerns them; quotations verbatim; keep the heading line; stay within the word range.
Return the full revised section in Markdown and nothing else."""

STITCH_SYS = """You are the final editor of a chapter of a university-press history of Udaypur. The sections were drafted in parallel: make the chapter's thesis run through every section and give the chapter one voice. Smooth the planned transitions; remove repetition across sections; keep each point where the coverage map assigns it.
STRICT: add no facts; keep every bracketed evidence ID attached to its claim; keep every [INT:function] label on its sentence (you may sharpen an interpretive sentence but it may not gain a new fact; drop or rewrite any that only restates facts); keep every {{note: …}} block unchanged; quotations unchanged; headings unchanged; keep each section's length (95–110%).
Return only the full chapter in Markdown."""

AUTHOR_SYS = """You are the author of this chapter of a history of Udaypur, reading it whole before it goes to press. Your thesis and the chapter's planned claims are given.
You may: sharpen interpretive ([INT:function]) sentences (each delivers its paragraph's written point; keep the point's claim) so each explains a cause, draws an unstated consequence, compares across time or place, names a tension or connects to the thesis — and cut any that only restates its facts; strengthen how the argument runs from section to section and how each section ends; vary rhythm and paragraph shape according to the style profile.
You may not: add or alter any fact, date, name or number; move, add or remove any bracketed evidence ID; change any quotation; change any {{note: …}} block; remove an [INT:function] label or put one on a factual sentence; change headings; change the length by more than 5%.
Return only the full chapter in Markdown."""

POLISH_SYS = """Polish this history chapter at sentence level: tighten rhythm, cut residual repetition, generic significance and stacked hedges.
STRICT: no new facts; every bracketed evidence ID, [INT:function] label and {{note: …}} block unchanged and in place; quotations unchanged; headings unchanged; do not shorten.
Return only the full chapter in Markdown."""

VERIFY_SYS = """You are a skeptical fact-checker of a history chapter. Each numbered item is a FACT sentence (with the evidence it cites), an INT sentence (the author's interpretation, with the facts cited in its paragraph and the one before), or a NOTE (a discursive footnote with its cited evidence). Judge each only against the evidence supplied for it.
Verdicts:
- FACT-SUPPORTED: the cited items state this (paraphrase, a range spanning two cited figures, or a fact stated without naming its source are fine).
- FACT-PARTIAL: goes beyond the evidence (an added date/number, stronger wording, certainty the source lacks, a merged unsupported claim).
- FACT-UNSUPPORTED: the cited items do not say this.
- INT-SOUND: a reasonable inference from the supplied facts that adds no new fact.
- INT-OVERREACH: the conclusion goes beyond what the facts allow (too strong, too general, causal where the facts are only sequential, or a concept no fact supports). Example: "The inhabited mound's security therefore rests on land beyond its buildings." (nothing cited speaks of security)
- INT-TRIVIAL: an interpretive sentence that only restates its facts — a reader who had just read the cited facts would already know what it says; or its function label (cause, consequence, comparison, tension, thesis) does not describe what it does. Example: "The roads define a village through its neighbours; the temple gives arrival a focus of its own."
- NEW-FACT: an interpretive sentence that slips in a fact (date, name, number, event, description) not in its supplied facts.
- MISREPRESENTED: a real disagreement presented as settled, a claim attributed to the wrong source, or tradition/panegyric/testimony presented as established fact.
Return ONLY JSON: {"results": [{"sid": "...", "verdict": "...", "evidence": "short exact phrase from the evidence (≤ 20 words)", "fix": "one-line fix unless FACT-SUPPORTED or INT-SOUND"}]}"""

FIX_SYS = """You correct flagged items in a history chapter about Udaypur. For each flagged sentence or note, return a replacement that: for FACT problems, narrows the claim to its cited evidence (keeping or correcting the bracketed IDs, only supplied IDs) or marks tradition as tradition; for INT-OVERREACH, makes the interpretation proportionate to the facts and specific; for INT-TRIVIAL, rewrites the sentence so that it explains a cause, draws an unstated consequence, compares across time or place, names a tension or connects to the thesis — with the matching [INT:function] label — or CUTs it if nothing in the facts supports such a point; for NEW-FACT, removes the slipped-in fact (or turns the sentence into a cited FACT sentence if the fact is in the supplied evidence); for MISREPRESENTED, frames the question around the event and moves the who-argues-what into a {{note: … [IDs]}}. Keep an [INT:function] label on interpretive sentences and off factual ones. Keep the place as the subject; never "[source] says", "the author" or "according to [title]". Never add facts.
Return ONLY JSON: {"replacements": [{"sid": "...", "new": "replacement text exactly as it should appear (a sentence with its [IDs] / [INT], or the full {{note: …}} block)" or "CUT", "note": "what changed"}]}"""


def ts():
    return time.strftime("%H:%M:%S")


def check(text, P, sec=None, targets=None):
    return p1.check(text, P, sec, targets)


def problems_of(rep):
    out = p1.problems_of(rep)
    out += [f"[INT] sentence uses generic significance (name something concrete): {g}" for g in rep.get("generic", [])]
    out += [f"interpretation: {x}" for x in rep.get("interpretive_issues", [])]
    out += [f"prose texture: {x}" for x in rep.get("fact_per_sentence", [])]
    out += [f"{x} — give the settled range with both items cited" for x in rep.get("settled_issues", [])]
    out += [f"copies 6+ words from the style sample (rewrite in your own words): {x}" for x in rep.get("ngram_hits", [])]
    out += [f"duplicate: {x}" for x in rep.get("duplicates", [])]
    return out


def score_rep(rep):
    return (p1.score_rep(rep) + 3 * len(rep.get("generic", [])) + 4 * len(rep.get("interpretive_issues", []))
            + 15 * len(rep.get("ngram_hits", [])) + 3 * len(rep.get("duplicates", []))
            + 4 * len(rep.get("fact_per_sentence", [])) + 5 * len(rep.get("settled_issues", [])))


def summ(rep):
    return p1.summ(rep)


def guards_ok(old, new):
    """conventions survive and no discursive note is lost (whole-chapter passes may not drop {{note}} blocks)"""
    return p1._guards_ok(old, new) and len(va.notes_in(new)) >= len(va.notes_in(old))


# ---------------------------------------------------------------- verification
PH = "⟦N{}⟧"


def protect(text):
    notes = []

    def rep(m):
        notes.append(m.group(0))
        return PH.format(len(notes) - 1)
    return re.sub(r"\{\{note:.*?\}\}", rep, text, flags=re.S), notes


def unprotect(s, notes):
    return re.sub(r"⟦N(\d+)⟧", lambda m: notes[int(m.group(1))], s)


def rows_of(text, P):
    """FACT / INT / NOTE items per section, each with the exact text to replace and the evidence IDs it is judged against"""
    out = {}
    for sec, part in va.split_sections(text).items():
        ptext, notes = protect(part)
        rows, prev = [], []
        for para in va.paragraphs(ptext):
            sents = va.sentences(para)
            para_ids = [x for s_ in sents for x in va.ids_in(va.strip_notes(unprotect(s_, notes)))]
            for s_ in sents:
                raw = unprotect(s_, notes).strip()
                main_ids = va.ids_in(va.strip_notes(raw))
                if va.is_int(raw):
                    rows.append({"sid": f"{sec}-{len(rows) + 1:02d}", "kind": "INT", "sentence": raw,
                                 "ids": [i for i in dict.fromkeys(main_ids + para_ids + prev) if i in P]})
                elif main_ids:
                    rows.append({"sid": f"{sec}-{len(rows) + 1:02d}", "kind": "FACT", "sentence": raw, "ids": [i for i in main_ids if i in P]})
                for nm in re.finditer(r"⟦N(\d+)⟧", s_):
                    nt = notes[int(nm.group(1))]
                    rows.append({"sid": f"{sec}-{len(rows) + 1:02d}", "kind": "NOTE", "sentence": nt, "ids": [i for i in va.ids_in(nt) if i in P]})
            prev = para_ids
        out[sec] = rows
    return out


def verify(text, P, R, targets):
    smap = rows_of(text, P)
    rules = vf.rule_checks(va.strip_int(va.strip_notes(text)), P, vf.cited_sentences(va.strip_int(va.strip_notes(text))))

    def vjob(sec, rows, name="verify", kind="verify"):
        def job():
            iids = sorted({i for r in rows for i in r["ids"]})
            u = (vf.CONVENTIONS + "EVIDENCE ITEMS:\n" + "\n\n".join(vf.item_text(P[i]) for i in iids) + "\n\nITEMS TO CHECK:\n"
                 + "\n".join(f"{r['sid']} [{r['kind']}; evidence: {', '.join(r['ids'])}]: {r['sentence']}" for r in rows))
            out = R.call(f"{name}_{sec}", 6, kind, VERIFY_SYS, u, 60 * len(rows))
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
    good = {"FACT-SUPPORTED", "INT-SOUND"}

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
        if v["verdict"] not in good:
            flagged.setdefault(sid.split("-")[0], []).append(sid)

    def fjob(sec, sids):
        def job():
            rows = [verdicts[s] for s in sids]
            iids = sorted({i for r in rows for i in r["ids"]})
            u = (vf.CONVENTIONS + "EVIDENCE ITEMS:\n" + "\n\n".join(vf.item_text(P[i]) for i in iids) + "\n\nFLAGGED:\n"
                 + "\n".join(f"{r['sid']} [{r['kind']}]: {r['sentence']}\n   verdict: {r['verdict']}; suggested fix: {r.get('fix', '')}; evidence: {r.get('evidence', '')}" for r in rows))
            out = R.call(f"fix_{sec}", 6, "fix", FIX_SYS, u, 70 * len(rows))
            j = rn.parse_json(out) if out else None
            return {x.get("sid"): x for x in (j or {}).get("replacements", [])}
        return job
    fixes = R.parallel([(sec, fjob(sec, sids)) for sec, sids in flagged.items()]) if flagged else {}
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
                open_items.append({"sid": sid, "reason": "text not found for replacement"})
                continue
            plain_new = va.clean(va.strip_notes(new_s))
            if any(k in old_s and k not in new_s for k in ("Tiwari", "1979")) or re.search(r"[ऀ-ॿ]", plain_new) \
                    or (new_s and row["kind"] != "NOTE" and sj.source_led(plain_new) and not sj.source_led(va.clean(va.strip_notes(old_s)))):
                open_items.append({"sid": sid, "reason": "fix dropped a convention, added Devanagari or made the sentence source-led; rejected"})
                continue
            cand = re.sub(r"[ \t]{2,}", " ", new_text.replace(old_s, new_s, 1))
            b, a = check(new_text, P, None, targets), check(cand, P, None, targets)
            if a["integrity_ok"] and score_rep(a) <= score_rep(b):
                new_text = cand
                changes.append({"sid": sid, "kind": row["kind"], "old": old_s, "new": new_s or "CUT", "verdict_before": row["verdict"]})
            else:
                open_items.append({"sid": sid, "reason": "fix made the code validation worse; reverted", "verdict": row["verdict"]})
    # re-verify the changed items (one round)
    changed = {}
    for c in changes:
        if c["new"] != "CUT":
            row = dict(verdicts[c["sid"]], sentence=c["new"])
            if c["kind"] != "INT":
                row["ids"] = [i for i in va.ids_in(va.strip_notes(c["new"])) if i in P] or row["ids"]
            changed.setdefault(c["sid"].split("-")[0], []).append(row)
    rres = R.parallel([(sec, vjob(sec, rows, "reverify", "reverify")) for sec, rows in changed.items()]) if changed else {}
    for sec, rows in changed.items():
        got = rres.get(sec) if isinstance(rres.get(sec), dict) else {}
        for r in rows:
            c = next(c for c in changes if c["sid"] == r["sid"])
            v = got.get(r["sid"])
            vv = str((v or {}).get("verdict", "UNVERIFIED")).upper()
            c["reverify"] = vv
            verdicts[r["sid"]] = dict(verdicts[r["sid"]], sentence=c["new"], verdict=vv)
    for c in changes:
        if c["new"] == "CUT":
            verdicts.pop(c["sid"], None)
    st.update(verdicts_after=counts(verdicts), changes=changes, open=open_items,
              remaining=[v for v in verdicts.values() if v["verdict"] not in good])
    (D / f"{STEM}_verification.json").write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")
    return new_text, st


# ---------------------------------------------------------------- main
def run(dry):
    t0 = time.time()
    print(f"[{ts()}] chapter {C.CH} {C.VERSION} authored pipeline start (dry={dry})", flush=True)
    outline, secs, targets, titles = va.load_outline()
    P = va.load_pack()
    info = p1.section_parts(secs)
    R = rn.Run(dry)
    stage_t, state = {}, {"chapter": C.CH, "version": C.VERSION, "model": rn.MODEL, "flagship": rn.FLAGSHIP, "budget": rn.BUDGET,
                          "reserve": rn.RESERVE, "spend_before": round(R.prior, 4), "sections": {}, "decisions": []}
    ids = {s: p1.section_ids(secs[s], P) for s in SECTIONS}
    base = {k: v.strip() for k, v in va.split_sections(C.BASELINE.read_text(encoding="utf-8")).items()} if getattr(C, "BASELINE", None) and C.BASELINE.exists() else {}
    if getattr(C, "BASELINE_MAP", None):          # earlier draft with a different section plan: judge against the closest section
        base = {new: re.sub(r"^## [^\n]*", f"## {titles[new]}", base[old], count=1) for new, old in C.BASELINE_MAP.items() if old and old in base}
    # budget plan (cut order: polish, edit, then one candidate per section); verification and the author's pass are never cut
    n_cand, skip_edit, skip_polish = 2, False, False
    if not dry:
        avail = rn.BUDGET - rn.RESERVE - R.spent
        est_core = 5 * 2 * 0.22 + 5 * 0.12 + 0.30 + 0.60 + 0.80        # candidates, judges, stitch, author, verification
        if est_core + 5 * 0.08 + 0.20 > avail:
            skip_polish = True
            state["decisions"].append("polish cut")
            if est_core + 5 * 0.08 > avail:
                skip_edit = True
                state["decisions"].append("edit pass cut")
                if est_core > avail:
                    n_cand = 1
                    state["decisions"].append("one candidate per section")

    def prompt(sec):
        inc, outg = p1.transitions(sec, info, titles)
        u = (STYLE_BLOCK + f"CHAPTER THESIS:\n{THESIS}\n\nTHIS SECTION'S INTERPRETIVE CLAIMS (make them, in your own words, from the cited facts):\n{SEC_BRIEF.get(sec, '')}\n\n"
             f"THE WHOLE CHAPTER OUTLINE:\n{outline}\n\nSECTION TO WRITE NOW: {titles[sec]}\nSection plan:\n{secs[sec]}\n\n"
             f"WORD TARGET: {targets[sec]} words (must land {int(targets[sec] * 0.95)}–{int(targets[sec] * 1.1)}), IDs, [INT:…] labels and notes excluded.\n\n"
             f"COVERED ELSEWHERE (do not develop):\n{p1.covered_elsewhere(sec, info, titles)}\n\nPLANNED INCOMING TRANSITION: {inc}\nPLANNED OUTGOING TRANSITION: {outg}\n\n"
             f"EVIDENCE FOR THIS SECTION ({len(ids[sec])} items):\n" + "\n\n".join(p1.fmt_item(P[i]) for i in ids[sec]))
        return WRITER_BRIEF, u

    # 1 candidates
    t = time.time()
    cands = {s: {} for s in SECTIONS}
    jobs = []
    for sec in SECTIONS:
        for L in "AB"[:n_cand]:
            pth = CAND / f"{sec}_{L}.md"
            if pth.exists() and not dry:
                cands[sec][L] = pth.read_text(encoding="utf-8")
                continue
            def job(sec=sec, L=L):
                system, u = prompt(sec)
                opening = {"A": "OPENING: open on a concrete scene, object or place that carries the section's first claim.",
                           "B": "OPENING: open with the section's central claim stated about the place, then ground it at once in a cited fact."}[L]
                out = R.call(f"cand_{sec}_{L}", 1, "candidate", system, u + "\n\n" + opening, targets[sec] + 300, effort=CAND_EFFORT)
                if out is None:
                    return f"## {titles[sec]}\n" + (f"Udaypur lorem [{ids[sec][0]}]. Ipsum dolor. [INT:thesis] " * (targets[sec] // 7))
                if out and not dry:
                    CAND.mkdir(exist_ok=True)
                    (CAND / f"{sec}_{L}.md").write_text(out.strip(), encoding="utf-8")
                return out.strip()
            jobs.append(((sec, L), job))
    for (sec, L), r in R.parallel(jobs).items():
        if isinstance(r, str) and r.strip():
            cands[sec][L] = r
    for sec in SECTIONS:
        if sec in base:
            cands[sec]["BASE"] = base[sec]
    stage_t["1_candidates"] = round(time.time() - t)

    # 2 judges
    t = time.time()
    jobs = []
    for sec in SECTIONS:
        labels = sorted(cands[sec])
        reps = {L: check(cands[sec][L], P, sec, targets) for L in labels}
        alive = [L for L in labels if reps[L]["integrity_ok"]] or labels
        state["sections"][sec] = {"entries": {L: {"words": reps[L]["words"].get(sec), "check": summ(reps[L])} for L in labels}, "alive": alive}
        def job(sec=sec, alive=alive, reps=reps):
            inc, outg = p1.transitions(sec, info, titles)
            ju = (STYLE_BLOCK + f"CHAPTER THESIS:\n{THESIS}\n\nSECTION CLAIMS:\n{SEC_BRIEF.get(sec, '')}\n\nWRITER BRIEF:\n{WRITER_BRIEF}\n\nSECTION PLAN:\n{secs[sec]}\n\n"
                  f"PARAGRAPH POINTS (each paragraph must deliver its point through its [INT] sentence(s)):\n{points_block(secs[sec])}\n\n"
                  f"WORD TARGET: {targets[sec]} (90–110%)\n\nPLANNED TRANSITIONS: in — {inc}; out — {outg}\n\nEVIDENCE:\n"
                  + "\n\n".join(p1.fmt_item(P[i], False) for i in dict.fromkeys(ids[sec] + [x for L in alive for x in va.ids_in(va.strip_notes(cands[sec][L])) if x in P]))
                  + "\n\n" + "\n\n".join(f"=== ENTRY {L} ===\nAUTOMATED CHECKS: {json.dumps(problems_of(reps[L])[:30], ensure_ascii=False)}\n\n{cands[sec][L]}" for L in alive))
            out = R.call(f"judge_{sec}", 2, "judge", JUDGE_SYS, ju, 900)
            return rn.parse_json(out) if out else None
        jobs.append((sec, job))
    res = R.parallel(jobs)
    verdicts = {}
    for sec in SECTIONS:
        alive = state["sections"][sec]["alive"]
        v = res.get(sec)
        v = v if isinstance(v, dict) else {"best": [L for L in alive if L != "BASE"][0], "improvements": [], "scores": {}, "rationale": "judge unavailable"}
        sc = v.get("scores", {})
        eligible = [L for L in alive if (sc.get(L) or {}).get("fidelity", 10) >= 6]
        if v.get("best") not in eligible:
            ranked = sorted(eligible, key=lambda L: -(sc.get(L) or {}).get("total", 0))
            v["fidelity_rule"] = f"{v.get('best')} excluded (fidelity < 6 or not eligible)"
            v["best"] = ranked[0] if ranked else alive[0]
        verdicts[sec] = v
        state["sections"][sec]["judge"] = v
        if not dry:
            (D / f"judge_{C.VERSION}_{sec}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
    stage_t["2_judges"] = round(time.time() - t)

    # 3 edits
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
            eu = (STYLE_BLOCK + f"WRITER BRIEF:\n{WRITER_BRIEF}\n\nSECTION CLAIMS:\n{SEC_BRIEF.get(sec, '')}\n\nWORD RANGE: {int(tg * 0.95)}–{int(tg * 1.1)}\n\nIMPROVEMENTS TO APPLY:\n"
                  + "\n".join(f"- {x}" for x in v.get("improvements", []))
                  + ("\nTRANSPLANTS:\n" + "\n".join(f"- {x}" for x in v.get("transplants", [])) if v.get("transplants") else "")
                  + ("\nPOINTS THE JUDGE FOUND MISSING OR ALTERED (restore each as the paragraph's [INT] sentence):\n" + "\n".join(f"- {x}" for x in (v.get("points_missed") or {}).get(best, []))
                     if (v.get("points_missed") or {}).get(best) else "")
                  + f"\nPARAGRAPH POINTS:\n{points_block(secs[sec])}"
                  + "\nAUTOMATED-CHECK PROBLEMS TO FIX:\n" + "\n".join(f"- {p}" for p in problems_of(freps[sec])[:30])
                  + "\n\nEVIDENCE:\n" + "\n\n".join(p1.fmt_item(P[i], False) for i in dict.fromkeys(ids[sec] + [x for x in va.ids_in(va.strip_notes(finals[sec])) if x in P]))
                  + f"\n\n=== SECTION TO REVISE ===\n{finals[sec]}\n\n{others}")
            return R.call(f"edit_{sec}", 3, "edit", EDIT_SYS, eu, tg + 150)
        jobs.append((sec, job))
    for sec, out in R.parallel(jobs).items():
        if isinstance(out, str) and out.strip():
            er = check(out.strip(), P, sec, targets)
            keep = er["integrity_ok"] and score_rep(er) <= score_rep(freps[sec]) and out.strip().startswith("## " + sec)
            state["sections"][sec]["edit"] = {"kept": keep, "before": summ(freps[sec]), "after": summ(er)}
            if keep:
                finals[sec], freps[sec] = out.strip(), er
    stage_t["3_edits"] = round(time.time() - t)
    chapter = "\n\n".join(finals[s].strip() for s in SECTIONS) + "\n"
    rep = check(chapter, P, None, targets)
    if not dry:
        (D / f"{STEM}_prestitch.md").write_text(chapter, encoding="utf-8")

    def whole(name, rnd, kind, system, extra, model=None):
        nonlocal chapter, rep
        try:
            out = R.call(name, rnd, kind, system, extra + f"\n\nCHAPTER:\n{chapter}", sum(targets.values()) + 400, model=model)
        except rn.BudgetStop as e:
            return {"kept": False, "reason": f"budget: {e}"}
        if not out:
            return {"kept": False, "reason": "call failed"}
        new = out.strip() + "\n"
        nr = check(new, P, None, targets)
        keep = nr["integrity_ok"] and score_rep(nr) <= score_rep(rep) and guards_ok(chapter, new)
        res_ = {"kept": keep, "before": summ(rep), "after": summ(nr)}
        if not dry:
            (D / f"{STEM}_{name}_raw.md").write_text(new, encoding="utf-8")
        if keep:
            chapter, rep = new, nr
        return res_

    cmap = "\n".join(f"- {titles[k]}: {info[k]['purpose']}" for k in SECTIONS)
    tmap = "\n".join(f"- after {titles[k]}: {info[k]['transition']}" for k in SECTIONS)
    # 4 stitch
    t = time.time()
    state["stitch"] = whole("stitch", 4, "stitch", STITCH_SYS, f"THESIS:\n{THESIS}\n\nCHAPTER OPENING: {C.OPEN_IN}\nCHAPTER CLOSING: {C.CLOSE_OUT}\n\nCOVERAGE MAP:\n{cmap}\n\nPLANNED TRANSITIONS:\n{tmap}")
    stage_t["4_stitch"] = round(time.time() - t)
    # 5 author's pass (flagship; never cut)
    t = time.time()
    state["author_pass"] = whole("author", 5, "author", AUTHOR_SYS, STYLE_BLOCK + f"THESIS:\n{THESIS}\n\nPLANNED CLAIMS BY SECTION:\n" + "\n\n".join(SEC_BRIEF.get(s, "") for s in SECTIONS)
                                 + "\n\nEACH PARAGRAPH'S WRITTEN POINT (keep every point; you may sharpen its wording, never change the claim):\n"
                                 + "\n\n".join(f"{titles[s]}\n{points_block(secs[s])}" for s in SECTIONS)
                                 + f"\n\nOPEN QUESTIONS THE CHAPTER RAISES:\n{QUESTIONS}\n\nCHAPTER OPENING: {C.OPEN_IN}\nCHAPTER CLOSING: {C.CLOSE_OUT}", model=rn.FLAGSHIP)
    stage_t["5_author_pass"] = round(time.time() - t)
    if not dry:
        (D / f"{STEM}_preverify.md").write_text(chapter, encoding="utf-8")
    # 6 verification (never cut)
    t = time.time()
    if not dry:
        chapter, vst = verify(chapter, P, R, targets)
        state["verification"] = {k: vst[k] for k in ("verdicts_before", "verdicts_after")}
        rep = check(chapter, P, None, targets)
    else:
        for sec in SECTIONS:
            R.call(f"verify_{sec}", 6, "verify", VERIFY_SYS, "x" * 30000, 2000)
            R.call(f"fix_{sec}", 6, "fix", FIX_SYS, "x" * 16000, 500)
            R.call(f"reverify_{sec}", 6, "reverify", VERIFY_SYS, "x" * 8000, 400)
    stage_t["6_verification"] = round(time.time() - t)
    # 7 polish
    t = time.time()
    state["polish"] = {"kept": False, "reason": "cut (budget)"} if skip_polish else whole("polish", 7, "polish", POLISH_SYS, STYLE_BLOCK)
    stage_t["7_polish"] = round(time.time() - t)
    state.update(final_validation=summ(rep), final_validation_detail=rep, stage_seconds=stage_t, wall_clock_seconds=round(time.time() - t0),
                 calls=R.calls, spent_usd=round(R.spent, 4), spend_by_stage={k: round(v, 4) for k, v in R.stage_spend.items()},
                 rule_checks_final=[] if dry else vf.rule_checks(va.strip_int(va.strip_notes(chapter)), P, vf.cited_sentences(va.strip_int(va.strip_notes(chapter)))))
    if not dry:
        C.OUT.write_text(chapter, encoding="utf-8")
    (D / (f"{STEM}_estimate.json" if dry else f"{STEM}_state.json")).write_text(json.dumps(state, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return state, R


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
                          "by_round": {r: {"calls": len(cs), "usd": round(sum(c["est_cost_usd"] for c in cs), 3), "model": cs[0]["model"]} for r, cs in sorted(by.items())},
                          "projected_wall_clock_min": round(wall / 60, 1)}, indent=1))
    else:
        for cmd in (["footnote.py", str(C.OUT)], ["make_docx.py"]):
            subprocess.run([sys.executable, "-I", str(HERE / cmd[0])] + cmd[1:])
    print(f"[{ts()}] CHAPTER {C.CH} AUTHORED PIPELINE FINISHED", flush=True)
