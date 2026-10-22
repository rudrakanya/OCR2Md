"""House-voice pipeline (editor-in-chief audit, approved 2026-10-14). Active chapter from UDAY_CFG (cfg HOUSE_VOICE = True).

Changes from pipeline2:
- Sections are drafted SEQUENTIALLY: each is written with the chapter plan and the chosen text of the sections before it.
  There is no stitch step.
- Writer rules are a few principles. No per-paragraph interpretive sentence, no function labels, no paragraph template.
  [INT] is an optional internal tag on uncited inference, stripped from output.
- Points are historical work, delivered by the paragraph as a whole.
- Evidence is tiered: E establishing / C corroborating / X context per paragraph, plus each item's evidence tier.
- The judge scores history, not compliance. It reports missed Points, INT-TRIVIAL sentences, conflations, misreadings
  and rule artefacts.
- The verifier sees each paragraph whole. MISREPRESENTED has subtypes (conflation, hardened proposal,
  tradition as event, praśasti as event, determinism, unattributed interpretation, disagreement as settled, wrong source).
- The author's pass is the developmental and voice pass (flagship model).
- The reader-facing notes are consolidated by footnote.py (cfg CONSOLIDATE_NOTES). The working draft keeps per-claim IDs.

Rounds: per section in order: 1 candidates (2) → 2 code checks + judge (A, B, BASE) → 3 edit (kept only if no worse);
then 5 author's pass (flagship, never cut) → 6 verification + one round of fixes + re-verify (never cut) → 7 polish
(kept only if no worse; cut first).

  set UDAY_CFG=...; python -u -I drafting/_pipe/pipeline3.py --dry-run | (no flag = run)
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
from cfg import C  # noqa: E402
import run as rn  # noqa: E402
import validate as va  # noqa: E402
import verify as vf  # noqa: E402
import subject as sj  # noqa: E402
import pipeline as p1  # noqa: E402
import tiers  # noqa: E402
import prose_checks as pc  # noqa: E402

D, SECTIONS = C.D, C.SECTIONS
CAND = D / f"candidates_{C.VERSION}"
STEM = C.OUT.stem
rn.EFFORT.update({k: "high" for k in ("candidate", "judge", "edit", "polish", "verify", "fix", "reverify", "author")})


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else ""


STYLE = _read(C.D.parent / "style" / "style_profile.md")
SHEET = _read(C.D.parent / "style" / "style_sheet.md")
STYLE_BLOCK = f"HOUSE-VOICE BRIEF (binding):\n{STYLE}\n\nSTYLE SHEET (binding conventions):\n{SHEET}\n\n"

BASE_RULES = """REGISTER: a chapter of a serious narrative history for intelligent general readers. Past tense for history; present tense for what exists today. British English. "Udaypur" throughout ("Udaipur" only for the city in Rajasthan). Consistent diacritics: Udayāditya, Paramāra, Udayeśvara, praśasti, Dhārā, Bhūmija. Italicise an Indian-language term on first use with a half-clause gloss.

FACTS: only facts in the supplied items' QUOTE (and ENGLISH RENDERING). CONTEXT excerpts and mapping notes only help you keep a source's meaning; never take a fact from them. No dates, names or numbers from general knowledge.

CITATIONS (working draft): every sentence that states a fact ends with its evidence ID(s) in square brackets, e.g. [C01-GAZ-007] or [C01-GAZ-007; C01-KB-PANDE-002], placed at the end of the clause or sentence it supports. Only supplied IDs. (Reader-facing notes are consolidated later; cite every claim here.)

QUOTATIONS: few and short, chosen for wording that matters, character for character from an item's QUOTE, in double quotation marks, followed by the ID. Hindi/Sanskrit items: paraphrase in English, or quote the English rendering marked "(translation)". Never quote an item flagged ⚠.

NEVER NARRATE METHOD: no "this chapter", "this book", "the reader", "we", "the narrative", "will be argued".

OUTPUT: the section in Markdown, starting with its heading line exactly as given ("## <number> <title>"), and nothing else."""

WRITER_RULES = """PRINCIPLES (binding):
1. Write history. Tell what happened, to whom, where and when, with people as agents wherever the evidence names them. A person or group may be the subject of a sentence only where a cited item describes that person or group or its action (people cultivating, a king building, villagers storing water, a named surveyor). Never invent anonymous agents (builders, quarrymen, masons, labourers, engineers) from a passive mention: where an item says only that stone "is quarried", write that the stone was quarried. Keep time visible: say which layer you mean (before Udayāditya, his reign, later Paramāras, Sultanate, Mughal, Scindia, colonial, today).
2. Never fictionalise: no invented thoughts, motives, conversations, scenes, weather, emotions, gestures, sensory detail, journeys, chronology or causation.
3. Every factual claim is cited. Your own inference needs no citation if it follows from facts cited in the same or the previous paragraph and adds no fact. You MAY mark such a sentence with [INT] at its end (internal only, removed before print). Nothing requires one.
4. Each paragraph in the plan has a Point: the historical work it must do. The paragraph as a whole must deliver its assigned Point, directly or cumulatively. No sentence should merely repeat a claim already established elsewhere in the paragraph. The Point is not a sentence to paraphrase, and it need not open or close the paragraph. Interpretation may live in how the paragraph is built.
5. Evidence tiers. Use the E (establishing) items, add C (corroborating) where it matters, and X (context) only if it helps; not every item must appear. A praśasti or royal inscription is evidence of what the dynasty claimed: present its claims as claims. A tradition or Tiwari's testimony is evidence for memory, not for the event it tells. For dynastic facts, CII VII.2's editor outranks Ganguly. Where Ganguly gives his own interpretation, attribute it to him (in a note) as his reading. Modern surveys propose; present proposals as proposals.
6. Compatibility is not identity. Never merge two inscriptions, buildings, tanks, traditions, rulers, places, layers or hypotheses unless an item says they are the same.
7. Disagreements: the text keeps the question and what hangs on it; who argues what goes in a discursive note written {{note: explanation [IDs]}} right after the sentence. A note obeys the fact rules.
8. Settled ranges stay ranges with both items cited (Udaypur lies about 13–16 km from Ganj Basoda and 55–70 km from Vidisha). Grade confidence on the clause it qualifies; never stack hedges.
9. Sources are not the subject: no "[source] says/writes/records/gives/places", "according to [title]" or "the author". Name a scholar in the text only when the scholar is an actor in the story or the disagreement changes the answer.
10. Shape follows the job: paragraphs and sentences vary in length. Avoid a house rhythm (closing aphorisms, "not X but Y", "both X and Y", colon reversals, triplets). The land is a setting people worked with, never the cause of a founding.
11. Continue the chapter. You are given the text that precedes this section: do not repeat what it has already told the reader; pick up from where it leaves off; end the section by content that leads into the next, never by announcing it.
13. Stay on Udaypur and the paragraph's Point: context that does not bear on either (a regional classification, a list of formations, a dynasty's wider campaigns) is a digression: one clause at most.
14. Narrator's voice uses the style sheet's terms ("Muslim", never "Mohammedan" outside a verbatim quotation).
12. Vijay Manohar Tiwari is a witness and the author of testimony (Jagta Hua Kasba): never "a visitor", "a traveller" or "a tourist"; no gendered pronouns."""

WRITER_SYS = f"{C.CHAPTER_BRIEF}\n\n{BASE_RULES}\n\n{WRITER_RULES}"

CONVENTIONS = ("EDITORIAL CONVENTIONS (supplied by the editor, not evidence claims; treat as supported and never remove): "
               "the author of *Jagta Hua Kasba* is Vijay Manohar Tiwari ('Tiwari'); the district Gazetteer is the 1979 compilation; "
               "Udayāditya's accession c. 1070 is the book's working position; Udayāditya is 'Bhoja's brother', as two inscriptions of his son "
               "Jagaddēva state (user decision D2, 16 Oct 2026; the dissent goes in a note). Book titles in Devanagari are never written in the prose.\n\n")

JUDGE_SYS = """You are the editor-in-chief of a serious narrative history of India, reading versions of one section of a chapter about Udaypur (Vidisha district, Madhya Pradesh). Entries are labelled; BASE, if present, is the same material from the previous draft.
Score each entry 1–10 on:
- fidelity: every fact cited and supported by the supplied evidence; inference adds no fact; nothing fictionalised; disagreements fair (in notes)
- historical_narrative: it reads as history: what happened, to whom, when, where; people act where the evidence names them; time is visible; place is a place, not a list of features
- historical_work: each paragraph accomplishes its Point (by the paragraph as a whole: directly or cumulatively), and the section achieves its SECTION STATEMENT; the Points' claims are neither weakened nor overstated
- coherence: it continues the CHAPTER SO FAR without repeating it, moves the section forward and hands on to the next section by content
- evidence_discipline: tiers respected (praśasti claims as claims; tradition and testimony as memory; proposals as proposals; Ganguly's interpretations attributed; CII above Ganguly on dynastic facts); no conflation of distinct objects or hypotheses; uncertainty proportionate, neither inflated nor erased; context relevant, not encyclopedic; no environmental determinism
- voice: one historian's voice as in the house-voice brief; sources are not the subject
- continuity: it continues the previous section and agrees with the BOOK LEDGER (no second gloss of a term, no re-introduced full name, no figure that conflicts)
- prose_poise: grammar, syntax, rhythm and clarity; no awkward appositives or stacked clauses
- digression: 10 = nothing that fails to bear on Udaypur or the paragraph's Point (e.g. a regional stone classification); list any digression in rule_artefacts
- passive_runs: 10 = no run of three or more sentences of the same passive or hedged shape (e.g. four proposals in a row: "has been assigned… may belong… are assigned… have been read")
- prose: natural syntactic and rhetorical variation; no house rhythm (closing aphorisms, binary templates, colon reversals); varied paragraph and sentence shape; no sentence that merely repeats a claim already made in its paragraph (INT-TRIVIAL); nothing present only because a pipeline rule demanded it
The automated code report for each entry is supplied (uncited claims, fabrication flags, quotation checks, source-led sentences, narrowed ranges): weigh it. An entry with fidelity below 6 cannot win.
Return ONLY JSON: {"scores": {"<label>": {"fidelity":n,"historical_narrative":n,"historical_work":n,"coherence":n,"evidence_discipline":n,"voice":n,"prose":n,"continuity":n,"prose_poise":n,"digression":n,"passive_runs":n,"total":n}, ...},
 "points_missed": {"<label>": ["P#: missing / weakened / overstated, and why"]},
 "int_trivial": {"<label>": ["exact sentence that only repeats its paragraph"]},
 "conflations": {"<label>": ["..."]}, "digressions": {"<label>": ["exact phrase"]}, "misreadings": {"<label>": ["tier / praśasti / tradition / determinism / attribution problems"]},
 "rule_artefacts": {"<label>": ["anything present mainly because a rule demanded it"]},
 "best": "<label>", "improvements": ["5–8 concrete line-level changes for the best entry: quote the phrase, say exactly how to change it"], "transplants": ["..."], "rationale": "..."}"""

EDIT_SYS = """You revise one section of a history chapter about Udaypur. Apply ONLY the listed improvements (and transplants), restore any Point the editor found missing (by the paragraph as a whole, not by adding a summary sentence), cut the listed INT-TRIVIAL sentences, cut each listed digression or reduce it to a clause, break any run of same-shaped passive or hedged sentences (vary the subject and construction, never the claim), and fix the listed automated-check problems.
STRICT: no new facts, dates, names or numbers; every factual sentence keeps its bracketed evidence IDs; {{note: …}} blocks keep their wording and IDs unless a listed fix concerns them; quotations verbatim; keep the heading line; stay within the word range.
Return the full revised section in Markdown and nothing else."""

AUTHOR_SYS = """You are the author of this chapter of a history of Udaypur, reading it whole before it goes to press: the developmental and voice pass.
You may: strengthen the chapter's arc and the hand-offs between sections; make people the agents where the cited facts name them or their action (never invent anonymous builders, quarrymen or engineers from a passive mention); vary paragraph and sentence shape; remove repetition across and within sections (including sentences that merely restate their paragraph); remove house-rhythm templates and closing aphorisms; make time visible; reorder sentences within a paragraph; merge or split paragraphs within a section.
You may not: add or alter any fact, date, name or number; move, add or remove any bracketed evidence ID (each stays attached to the claim it supports); change any quotation; change any {{note: …}} block; change headings; drop any paragraph's Point; change the length by more than 8%.
Return only the full chapter in Markdown."""

POLISH_SYS = """Polish this history chapter at sentence level: tighten, cut residual repetition, generic significance and stacked hedges; vary openings.
STRICT: no new facts; every bracketed evidence ID and {{note: …}} block unchanged and in place; quotations unchanged; headings unchanged; do not shorten.
Return only the full chapter in Markdown."""

COPYEDIT_SYS = """You are the copy-editor of a history book about Udaypur. Copyedit ONE section against the STYLE SHEET: grammar, agreement, tense (past for events; present for surviving objects, for what sources say, and for the village today), dangling or misplaced modifiers, pronoun reference, parallelism, a word repeated within two sentences, punctuation, quotation marks, numbers and spelling conventions, and any unclear sentence.
STRICT: do not change any fact, date, name, number, claim or its strength; every bracketed evidence ID stays attached to its claim; {{note: …}} blocks unchanged; quotations unchanged; heading unchanged; do not add or remove sentences except to split one that is unclear; do not shorten by more than 3%.
Return the full section in Markdown and nothing else."""

VERIFY_SYS = """You are a skeptical fact-checker of a history chapter. The chapter is given paragraph by paragraph. Under each paragraph, numbered items are its sentences:
FACT (a sentence with evidence IDs; judge it against the items it cites; BUT if the sentence interprets, compares, concludes or draws an implication from its items rather than reporting what they say, judge it as inference: INT-SOUND, INT-OVERREACH or INT-TRIVIAL, never FACT-PARTIAL), INT (a sentence without IDs: the author's own inference or narrative linking; judge it against the facts cited in its paragraph and the one before), NOTE (a discursive footnote with its evidence). Read every item in the context of its WHOLE paragraph.
Verdicts:
- FACT-SUPPORTED: the cited items state this (paraphrase, a range spanning two cited figures, a fact stated without naming its source: all fine).
- FACT-PARTIAL: goes beyond the evidence (an added date/number, stronger wording, certainty the source lacks, a merged unsupported claim).
- FACT-UNSUPPORTED: the cited items do not say this.
- INT-SOUND: a reasonable inference or link from the paragraph's facts that adds no new fact.
- INT-OVERREACH: the conclusion goes beyond what the facts allow (too strong, too general, causal where the facts are only sequential).
- INT-TRIVIAL: the sentence only repeats or rhetorically repackages a claim already established elsewhere in its paragraph (judge the meaning, not the words).
- NEW-FACT: an uncited sentence that slips in a fact not in its paragraph's supplied facts.
- TESTIMONY-AS-MEASURE: a distance, measurement, count or date whose only support is Tiwari's testimony (Jagta Hua Kasba, JAGTA items) or an oral tradition. Testimony is evidence for memory, never for a measurement.
- AGENT-INVENTED: a person or group (quarrymen, masons, builders, engineers, villagers…) is made the subject of an action that no cited item attributes to them (e.g. the item says stone "is quarried"; the sentence says quarrymen quarried it).
- MISREPRESENTED, with a subtype: conflation (two distinct inscriptions, buildings, tanks, traditions, rulers, places, layers or hypotheses merged without an item saying they are the same) | hardened-proposal (a proposal or tentative reading presented as fact) | tradition-as-event (a tradition or testimony presented as evidence that the event it tells happened) | prasasti-as-event (a royal panegyric's claim presented as a plain event) | determinism (land or climate presented as the cause of a human decision) | unattributed-interpretation (a scholar's own interpretation, e.g. Ganguly's, presented as fact without attribution) | disagreement-as-settled | wrong-source | fiction (invented thought, motive, scene, sensory detail or causation, or an invented agent: builders, quarrymen, masons or engineers made the subject where the items only say something was built or quarried).
Return ONLY JSON: {"results": [{"sid": "...", "verdict": "...", "subtype": "only for MISREPRESENTED", "evidence": "short exact phrase from the evidence (≤ 20 words)", "fix": "one-line fix unless FACT-SUPPORTED or INT-SOUND"}]}"""

FIX_SYS = """You correct flagged items in a history chapter about Udaypur. For each flagged sentence or note return a replacement that: for FACT problems narrows the claim to its cited evidence (keeping or correcting the bracketed IDs; only supplied IDs) or marks tradition as tradition and a praśasti's claim as its claim; for INT-OVERREACH makes the inference proportionate (keep it an inference: trim it; never replace it with a restated fact); for INT-TRIVIAL returns CUT; for TESTIMONY-AS-MEASURE removes the measurement and keeps the testimony as testimony (e.g. Tiwari's sight of the temple, without a distance) unless the sentence can carry something the paragraph has not said (from its facts only); for AGENT-INVENTED rewrites to the source's own construction (passive or the thing as subject; no invented actor); for NEW-FACT removes the slipped-in fact or cites it if it is in the supplied evidence; for MISREPRESENTED corrects the subtype's problem (separate the conflated objects; restore the proposal's status; tell the tradition as memory; read the praśasti as claim; remove the causal claim; attribute the interpretation in a {{note: … [IDs]}}; frame the disagreement around the event; fix the source; remove the invention). Never add facts; never make a sentence source-led; NEVER restate a fact the section already gives (if the only correction is a fact already stated elsewhere in the section, return CUT).
Return ONLY JSON: {"replacements": [{"sid": "...", "new": "replacement text exactly as it should appear, or CUT", "note": "what changed"}]}"""


def ts():
    return time.strftime("%H:%M:%S")


# ---------------------------------------------------------------- plan
PLAN = _read(C.OUTLINE)
PLAN_HEAD = PLAN.split(f"\n## {C.CH}.1")[0].strip()
PT_RE = re.compile(r"(?ms)^\d+\.\s+\*\*(P\d+) — (.+?)\*\*\s*\n\s*- \*\*Point:\*\*\s*(.*?)(?=^\s*- (?:E|C|X|Note|Lineage note|Accession note):|^\d+\.\s+\*\*P|\Z)")
ROLE_RE = re.compile(r"(?:^|\.\s+|\s)(E|C|X|Note|Lineage note|Accession note):\s*((?:C\d\d-[A-Z0-9-]+?-\d{3}(?:,\s*)?)+)")


def statement(sec_plan):
    m = re.search(r"\*\*Section statement:\*\*\s*(.+?)(?=\n\n\*\*Purpose)", sec_plan, re.S)
    return m.group(1).strip() if m else ""


def points(sec_plan):
    return [(m.group(1), m.group(2).strip(" ."), " ".join(m.group(3).split())) for m in PT_RE.finditer(sec_plan)]


def points_block(sec_plan):
    return "\n".join(f"- {k} ({t}): {pt}" for k, t, pt in points(sec_plan))


def roles(sec_plan):
    """{id: (paragraph, role)} from the plan's evidence lines"""
    out = {}
    for para in re.split(r"(?m)^(?=\d+\.\s+\*\*P)", sec_plan):
        pm = re.match(r"\d+\.\s+\*\*(P\d+)", para)
        if not pm:
            continue
        for line in re.findall(r"(?m)^\s*- (?:E|C|X|Note|Lineage note|Accession note):.*$", para):
            for m in ROLE_RE.finditer(line):
                role = {"E": "establishing", "C": "corroborating", "X": "context"}.get(m.group(1), "for the note")
                for i in re.findall(r"C\d\d-[A-Z0-9-]+?-\d{3}", m.group(2)):
                    out.setdefault(i, (pm.group(1), role))
    return out


def fmt(item, role=None, context=True):
    t, note = tiers.tier_of(item)
    s = p1.fmt_item(item, context)
    head, rest = s.split("\n", 1)
    return f"{head} · {note}" + (f" · role: {role[0]} {role[1]}" if role else "") + "\n" + rest


def evidence_block(sec_plan, P, extra_ids=(), context=True):
    r = roles(sec_plan)
    ids = [i for i in dict.fromkeys(list(r) + [x for x in extra_ids]) if i in P]
    return "\n\n".join(fmt(P[i], r.get(i), context) for i in ids), ids


def arc(titles, secs):
    return "\n".join(f"- {titles[k]}: {statement(secs[k])}" for k in SECTIONS)


def writer_prompt(sec, secs, titles, targets, P, so_far, so_far_label="THE CHAPTER SO FAR (already written; continue from it)"):
    ev, ids = evidence_block(secs[sec], P)
    tg = targets[sec]
    u = (STYLE_BLOCK + f"CHAPTER PLAN (question and arc):\n{PLAN_HEAD}\n\nSECTIONS AND WHAT EACH ACHIEVES:\n{arc(titles, secs)}\n\n"
         f"{so_far_label}:\n{so_far.strip() if so_far.strip() else '(none: this section opens the chapter. ' + C.OPEN_IN + ')'}\n\n"
         f"SECTION TO WRITE NOW: {titles[sec]}\nSECTION PLAN:\n{secs[sec]}\n\n"
         f"LENGTH: about {tg} words at most; anywhere in {int(tg * 0.7)}–{int(tg * 1.2)} is right, IDs and notes excluded. Never pad: stop when the Points are delivered. Paragraph count and length follow the plan's jobs, not a template.\n"
         + (f"CHAPTER CLOSING: {C.CLOSE_OUT}\n" if sec == SECTIONS[-1] else "")
         + f"\nEVIDENCE FOR THIS SECTION ({len(ids)} items; role and tier given for each):\n{ev}")
    return u, ids


# ---------------------------------------------------------------- checks
def check(text, P, sec=None, targets=None):
    rep = p1.check(text, P, sec, targets)
    pr = pc.report(text, P)
    rep["narrator_terms"] = [f"narrator term '{x['term']}' outside quotation (use {x['use']}): {x['sentence'][:140]}" for x in pr["narrator_terms"]]
    rep["agent_nouns"] = [f"agent noun '{x['noun']}' not in any cited item: rewrite to the source's construction unless an item names them: {x['sentence'][:140]}" for x in pr["agent_nouns"]]
    rep["passive_runs"] = [f"{x['run']} {x['shape']} sentences in a row, from: {x['first'][:100]}" for x in pr["passive_runs"]]
    rep["testimony_measures"] = [f"testimony as measurement (Tiwari or tradition is the only support for a distance, measure or date; keep the testimony, drop the figure): {x}" for x in pc.testimony_measures(text, P)]
    rep["prose_report"] = pr
    return rep


def problems_of(rep):
    out = p1.problems_of(rep)
    out = [x for x in out if not x.startswith("monotony")]          # diagnostics, not fixes
    out += [f"{x}: give the settled range with both items cited" for x in rep.get("settled_issues", [])]
    out += [f"generic significance: {x}" for x in rep.get("generic", [])]
    out += list(rep.get("gaz_share", []))
    out += list(rep.get("narrator_terms", [])) + list(rep.get("agent_nouns", [])) + list(rep.get("testimony_measures", []))
    out += [f"MUST FIX, passive run: rewrite so no three consecutive sentences share the passive or hedged shape (vary subject and construction; keep each claim and its strength): {x}" for x in rep.get("passive_runs", [])]
    return out


def fidelity_problems(rep):
    return ([f"invalid ID {x}" for x in rep["invalid_ids"]] + [f"quotation not verbatim: {q['quote']}" for q in rep["nonverbatim_quotes"]]
            + [f"quotation from a ⚠ item: {q}" for q in rep["warn_quotes"]] + [f"uncited factual sentence: {s}" for s in rep["uncited_claims"]]
            + [f"not supported by the cited items: {s}" for s in rep["fabrication"]] + [f"{x}" for x in rep.get("settled_issues", [])])


def score_rep(rep):
    return ((0 if rep["integrity_ok"] else 1000) + 3 * len(rep["uncited_claims"]) + 3 * len(rep["fabrication"])
            + 5 * len(rep["word_issues"]) + 5 * sum(not c["present"] for c in rep["conflicts"]) + 4 * len(rep.get("meta", []))
            + 2 * len(rep.get("banned", [])) + 3 * p1.n_source_led(rep) + 5 * len(rep.get("settled_issues", [])) + 4 * len(rep.get("gaz_share", [])) + 4 * len(rep.get("narrator_terms", [])) + 3 * len(rep.get("agent_nouns", []))
            + 4 * len(rep.get("passive_runs", [])) + 6 * len(rep.get("testimony_measures", [])))


def guards_ok(old, new):
    return p1._guards_ok(old, new) and len(va.notes_in(new)) >= len(va.notes_in(old))


EDIT_REPAIR_SYS = """The revised section below introduced the listed automated-check problems. Fix ONLY those problems in the revised section, keeping every other change the revision made. No new facts; every factual sentence keeps its bracketed evidence IDs (only supplied IDs); {{note: …}} blocks unchanged unless a listed problem concerns them; quotations verbatim; keep the heading line; stay within the word range (never pad: if the section is short, restore cut material from the PREVIOUS VERSION rather than inventing).
Return the full section in Markdown and nothing else."""


def edit_gate(R, name, out, frep, sec, P, targets, prev, dry=False):
    """keep an edit only if it is no worse by the code checks; if it is worse, one targeted repair of the edit (round 4b
    lesson, 2026-10-14: the gate threw away whole edit passes over one or two new problems) before discarding it"""
    er = check(out, P, sec, targets)
    ok = er["integrity_ok"] and score_rep(er) <= score_rep(frep) and out.startswith("## " + sec)
    info = {"kept": ok, "before": p1.summ(frep), "after": p1.summ(er)}
    if ok or dry or not out.startswith("## " + sec):
        return ok, out, info
    new = [x for x in problems_of(er) + fidelity_problems(er) if x not in problems_of(frep) + fidelity_problems(frep)]
    if not er["integrity_ok"]:
        new.append("integrity: invalid ID, non-verbatim quotation, ⚠ quotation or unclosed {{note:")
    ev = evidence_block("", P, [x for x in va.ids_in(va.strip_notes(prev + out)) if x in P], False)[0]
    fixed = R.call(f"{name}_repair", 3, "edit", EDIT_REPAIR_SYS, "PROBLEMS INTRODUCED BY THE REVISION:\n" + "\n".join(f"- {x}" for x in dict.fromkeys(new))
                   + f"\n\nWORD RANGE: {int(targets[sec] * 0.7)}–{int(targets[sec] * 1.2)}\n\nEVIDENCE:\n{ev}\n\n=== PREVIOUS VERSION ===\n{prev}\n\n=== REVISED SECTION ===\n{out}",
                   targets[sec] + 200)
    if isinstance(fixed, str) and fixed.strip().startswith("## " + sec):
        fr = check(fixed.strip(), P, sec, targets)
        if fr["integrity_ok"] and score_rep(fr) <= score_rep(frep):
            return True, fixed.strip(), dict(info, kept=True, repaired=True, after=p1.summ(fr))
        info["repair"] = {"kept": False, "after": p1.summ(fr)}
    return False, out, info


# ---------------------------------------------------------------- judge
def judge(R, name, sec, secs, titles, targets, P, entries, reps, so_far):
    ids = list(dict.fromkeys([i for i in roles(secs[sec]) if i in P] + [x for t in entries.values() for x in va.ids_in(va.strip_notes(t)) if x in P]))
    ju = (STYLE_BLOCK + f"WRITER BRIEF:\n{WRITER_SYS}\n\nCHAPTER PLAN:\n{PLAN_HEAD}\n\nSECTIONS:\n{arc(titles, secs)}\n\n"
          f"THE CHAPTER SO FAR:\n{so_far.strip() or '(none: this section opens the chapter)'}\n\n"
          f"SECTION PLAN:\n{secs[sec]}\n\nSECTION STATEMENT: {statement(secs[sec])}\n\nPARAGRAPH POINTS (historical work; delivered by each paragraph as a whole):\n{points_block(secs[sec])}\n\n"
          f"LENGTH: about {targets[sec]} words (70–120%; shorter is fine, padding is a fault)\n\nEVIDENCE:\n" + "\n\n".join(fmt(P[i], None, False) for i in ids)
          + "\n\n" + "\n\n".join(f"=== ENTRY {L} ===\nAUTOMATED CHECKS: {json.dumps(problems_of(reps[L])[:30], ensure_ascii=False)}\n\n{t}" for L, t in entries.items()))
    out = R.call(name, 2, "judge", JUDGE_SYS, ju, 1100)
    return rn.parse_json(out) if out else None


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
    """per section: paragraphs, each with FACT / INT / NOTE rows (every sentence is checked; uncited ones as INT)"""
    out = {}
    for sec, part in va.split_sections(text).items():
        ptext, notes = protect(part)
        paras, prev, n = [], [], 0
        for para in va.paragraphs(ptext):
            # a placeholder note ends a sentence: without this split, "…[ID] {{note}} Next sentence" became one row whose
            # note-stripped text no longer exists in the draft, and its fix was lost (round 4b, 2026-10-14)
            sents = [x for s_ in va.sentences(para) for x in re.split(r"(?<=⟧)\s+(?=[A-Z‘“\"'*(])", s_) if x.strip()]
            para_ids = [x for s_ in sents for x in va.ids_in(va.strip_notes(unprotect(s_, notes)))]
            rows = []
            for s_ in sents:
                raw = unprotect(s_, notes).strip()
                main_ids = va.ids_in(va.strip_notes(re.sub(r"\{\{note:.*?\}\}", "", raw, flags=re.S)))
                n += 1
                if main_ids:
                    rows.append({"sid": f"{sec}-{n:02d}", "kind": "FACT", "sentence": re.sub(r"\s*\{\{note:.*?\}\}", "", raw, flags=re.S), "ids": [i for i in main_ids if i in P]})
                else:
                    rows.append({"sid": f"{sec}-{n:02d}", "kind": "INT", "sentence": re.sub(r"\s*\{\{note:.*?\}\}", "", raw, flags=re.S),
                                 "ids": [i for i in dict.fromkeys(para_ids + prev) if i in P]})
                for nm in re.finditer(r"⟦N(\d+)⟧", s_):
                    nt = notes[int(nm.group(1))]
                    n += 1
                    rows.append({"sid": f"{sec}-{n:02d}", "kind": "NOTE", "sentence": nt, "ids": [i for i in va.ids_in(nt) if i in P]})
            paras.append({"text": va.strip_int(unprotect(para, notes)).strip(), "rows": rows})
            prev = para_ids
        out[sec] = paras
    return out


def verify_sections(text, P, R, prefix="verify", fix=True, extra_context=""):
    smap = rows_of(text, P)

    def vjob(sec, paras, name):
        def job():
            iids = sorted({i for p in paras for r in p["rows"] for i in r["ids"]})
            body = []
            for k, p in enumerate(paras, 1):
                body.append(f"--- PARAGRAPH {k} ---\n{p['text']}\nITEMS:\n" + "\n".join(
                    f"{r['sid']} [{r['kind']}; evidence: {', '.join(r['ids']) if r['kind'] != 'INT' else 'paragraph facts'}]: {va.strip_int(r['sentence'])}" for r in p["rows"]))
            u = CONVENTIONS + extra_context + "EVIDENCE ITEMS:\n" + "\n\n".join(vf.item_text(P[i]) + f"\n  TIER: {tiers.tier_of(P[i])[1]}" for i in iids) + "\n\nTHE SECTION, PARAGRAPH BY PARAGRAPH:\n" + "\n\n".join(body)
            out = R.call(f"{name}_{sec}", 6, "verify", VERIFY_SYS, u, 70 * sum(len(p["rows"]) for p in paras))
            j = rn.parse_json(out) or {}
            return {x.get("sid"): x for x in j.get("results", [])}
        return job
    res = R.parallel([(sec, vjob(sec, paras, prefix)) for sec, paras in smap.items() if paras])
    verdicts = {}
    for sec, paras in smap.items():
        got = res.get(sec) if isinstance(res.get(sec), dict) else {}
        for p in paras:
            for r in p["rows"]:
                v = got.get(r["sid"]) or {"verdict": "UNVERIFIED"}
                verdicts[r["sid"]] = dict(r, verdict=str(v.get("verdict", "UNVERIFIED")).upper(), subtype=v.get("subtype", ""),
                                          evidence=v.get("evidence", ""), fix=v.get("fix", ""))
    st = {"verdicts_before": counts(verdicts, smap), "flagged_before": [v for v in verdicts.values() if v["verdict"] not in GOOD]}
    if not fix:
        return text, st, verdicts
    flagged = {}
    for sid, v in verdicts.items():
        if v["verdict"] not in GOOD:
            flagged.setdefault(sid.rsplit("-", 1)[0], []).append(sid)

    def fjob(sec, sids):
        def job():
            rows = [verdicts[s] for s in sids]
            iids = sorted({i for r in rows for i in r["ids"]})
            u = (CONVENTIONS + "EVIDENCE ITEMS:\n" + "\n\n".join(vf.item_text(P[i]) for i in iids) + "\n\nFLAGGED:\n"
                 + "\n".join(f"{r['sid']} [{r['kind']}]: {r['sentence']}\n   verdict: {r['verdict']} {r.get('subtype', '')}; suggested fix: {r.get('fix', '')}; evidence: {r.get('evidence', '')}" for r in rows))
            out = R.call(f"fix_{sec}", 6, "fix", FIX_SYS, u, 80 * len(rows))
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
            if new_s and pc.duplicates_other(new_s, new_text.replace(old_s, "", 1)):
                open_items.append({"sid": sid, "reason": "fix restated a sentence the section already has; rejected"})
                continue
            if any(k in old_s and k not in new_s for k in ("Tiwari", "1979")) or re.search(r"[ऀ-ॿ]", plain_new) \
                    or (new_s and row["kind"] != "NOTE" and sj.source_led(plain_new) and not sj.source_led(va.clean(va.strip_notes(old_s)))):
                open_items.append({"sid": sid, "reason": "fix dropped a convention, added Devanagari or made the sentence source-led; rejected"})
                continue
            cand = re.sub(r"[ \t]{2,}", " ", new_text.replace(old_s, new_s, 1))
            b, a = check(new_text, P), check(cand, P)
            # length is the edit pass's job: a cut of a repeated sentence must not be reverted for taking a section under the
            # 70% floor (round 4b: 1.5's INT-TRIVIAL cut was lost that way)
            if a["integrity_ok"] and score_rep(dict(a, word_issues=[])) <= score_rep(dict(b, word_issues=[])):
                new_text = cand
                changes.append({"sid": sid, "kind": row["kind"], "old": old_s, "new": new_s or "CUT", "verdict_before": row["verdict"]})
            else:
                open_items.append({"sid": sid, "reason": "fix made the code validation worse; reverted", "verdict": row["verdict"]})
    changed = {}
    for c in changes:
        if c["new"] != "CUT":
            row = dict(verdicts[c["sid"]], sentence=c["new"])
            if c["kind"] == "FACT":
                row["ids"] = [i for i in va.ids_in(va.strip_notes(c["new"])) if i in P] or row["ids"]
            changed.setdefault(c["sid"].rsplit("-", 1)[0], []).append(row)

    def rjob(sec, rows):
        def job():
            iids = sorted({i for r in rows for i in r["ids"]})
            u = (CONVENTIONS + "EVIDENCE ITEMS:\n" + "\n\n".join(vf.item_text(P[i]) for i in iids) + "\n\nTHE SECTION, PARAGRAPH BY PARAGRAPH:\n--- PARAGRAPH (revised items only) ---\nITEMS:\n"
                 + "\n".join(f"{r['sid']} [{r['kind']}; evidence: {', '.join(r['ids'])}]: {r['sentence']}" for r in rows))
            out = R.call(f"reverify_{sec}", 6, "reverify", VERIFY_SYS, u, 70 * len(rows))
            j = rn.parse_json(out) or {}
            return {x.get("sid"): x for x in j.get("results", [])}
        return job
    rres = R.parallel([(sec, rjob(sec, rows)) for sec, rows in changed.items()]) if changed else {}
    for sec, rows in changed.items():
        got = rres.get(sec) if isinstance(rres.get(sec), dict) else {}
        for r in rows:
            c = next(c for c in changes if c["sid"] == r["sid"])
            vv = str((got.get(r["sid"]) or {}).get("verdict", "UNVERIFIED")).upper()
            c["reverify"] = vv
            verdicts[r["sid"]] = dict(verdicts[r["sid"]], sentence=c["new"], verdict=vv)
    for c in changes:
        if c["new"] == "CUT":
            verdicts.pop(c["sid"], None)
    st.update(verdicts_after=counts(verdicts, smap), changes=changes, open=open_items, remaining=[v for v in verdicts.values() if v["verdict"] not in GOOD])
    return new_text, st, verdicts


GOOD = {"FACT-SUPPORTED", "INT-SOUND"}


def counts(vs, smap):
    out = {}
    for sec in smap:
        c = {}
        for k, v in vs.items():
            if k.rsplit("-", 1)[0] == sec:
                key = v["verdict"] + (f":{v['subtype']}" if v.get("subtype") and v["verdict"] == "MISREPRESENTED" else "")
                c[key] = c.get(key, 0) + 1
        out[sec] = c
    return out


# ---------------------------------------------------------------- main
def run(dry):
    t0 = time.time()
    print(f"[{ts()}] chapter {C.CH} {C.VERSION} house-voice pipeline start (dry={dry})", flush=True)
    _, secs, targets, titles = va.load_outline()
    P = va.load_pack()
    R = rn.Run(dry)
    state = {"chapter": C.CH, "version": C.VERSION, "model": rn.MODEL, "flagship": rn.FLAGSHIP, "budget": rn.BUDGET, "reserve": rn.RESERVE,
             "spend_before": round(R.prior, 4), "sections": {}, "decisions": []}
    old = va.split_sections(C.BASELINE.read_text(encoding="utf-8")) if getattr(C, "BASELINE", None) and C.BASELINE.exists() else {}
    base = {new: re.sub(r"^## [^\n]*", f"## {titles[new]}", old[o].strip(), count=1) for new, o in getattr(C, "BASELINE_MAP", {}).items() if o and o in old}
    n_cand, skip_edit, skip_polish = 2, False, False
    if not dry:
        avail = rn.BUDGET - rn.RESERVE - R.spent
        est_core = 5 * 2 * 0.24 + 5 * 0.16 + 0.70 + 0.90
        if est_core + 5 * 0.10 + 0.25 > avail:
            skip_polish = True
            state["decisions"].append("polish cut")
            if est_core + 5 * 0.10 > avail:
                skip_edit = True
                state["decisions"].append("edit pass cut")
                if est_core > avail:
                    n_cand = 1
                    state["decisions"].append("one candidate per section")
    stage_t, chosen = {}, {}
    t = time.time()
    for sec in SECTIONS:                                       # 1–3 sequential: candidates, judge, edit
        so_far = "\n\n".join(chosen[s] for s in SECTIONS if s in chosen)
        u, ids = writer_prompt(sec, secs, titles, targets, P, so_far)
        cands = {}

        def cjob(L, sec=sec, u=u):
            def job():
                pth = CAND / f"{sec}_{L}.md"
                if pth.exists() and not dry:
                    return pth.read_text(encoding="utf-8")
                out = R.call(f"cand_{sec}_{L}", 1, "candidate", WRITER_SYS, u, targets[sec] + 400)
                if out is None:
                    return f"## {titles[sec]}\n\n" + (f"Udaypur lorem [{ids[0]}]. " * (targets[sec] // 3))
                if out and not dry:
                    CAND.mkdir(exist_ok=True)
                    pth.write_text(out.strip(), encoding="utf-8")
                return out.strip()
            return job
        for L, r in R.parallel([(L, cjob(L)) for L in "AB"[:n_cand]]).items():
            if isinstance(r, str) and r.strip():
                cands[L] = r
        if sec in base:
            cands["BASE"] = base[sec]
        reps = {L: check(x, P, sec, targets) for L, x in cands.items()}
        alive = {L: cands[L] for L in cands if reps[L]["integrity_ok"]} or cands
        v = judge(R, f"judge_{sec}", sec, secs, titles, targets, P, alive, reps, so_far) or {}
        sc = v.get("scores", {})
        elig = [L for L in alive if L != "BASE" and (sc.get(L) or {}).get("fidelity", 10) >= 6] or [L for L in alive if L != "BASE"] or list(alive)
        best = v.get("best") if v.get("best") in elig else max(elig, key=lambda L: (sc.get(L) or {}).get("total", 0))
        final, frep = cands[best], reps[best]
        st = {"entries": {L: {"words": reps[L]["words"].get(sec), "check": p1.summ(reps[L])} for L in cands}, "judge": v, "chosen": best}
        if not skip_edit:
            others = "\n\n".join(f"=== ENTRY {L} (transplant source only) ===\n{alive[L]}" for L in alive if L != best)
            eu = (STYLE_BLOCK + f"WRITER BRIEF:\n{WRITER_SYS}\n\nTHE CHAPTER SO FAR:\n{so_far or '(none)'}\n\nSECTION PLAN:\n{secs[sec]}\n\nWORD RANGE: {int(targets[sec] * 0.7)}–{int(targets[sec] * 1.2)} (never pad)\n\n"
                  "IMPROVEMENTS TO APPLY:\n" + "\n".join(f"- {x}" for x in v.get("improvements", []))
                  + ("\nTRANSPLANTS:\n" + "\n".join(f"- {x}" for x in v.get("transplants", [])) if v.get("transplants") else "")
                  + "\nPOINTS FOUND MISSING OR ALTERED:\n" + "\n".join(f"- {x}" for x in (v.get("points_missed") or {}).get(best, []))
                  + "\nINT-TRIVIAL SENTENCES TO CUT:\n" + "\n".join(f"- {x}" for x in (v.get("int_trivial") or {}).get(best, []))
                  + "\nAUTOMATED-CHECK PROBLEMS TO FIX:\n" + "\n".join(f"- {x}" for x in problems_of(frep)[:30])
                  + "\n\nEVIDENCE:\n" + evidence_block(secs[sec], P, [x for x in va.ids_in(va.strip_notes(final)) if x in P], False)[0]
                  + f"\n\n=== SECTION TO REVISE ===\n{final}\n\n{others}")
            out = R.call(f"edit_{sec}", 3, "edit", EDIT_SYS, eu, targets[sec] + 200)
            if isinstance(out, str) and out.strip():
                ok, txt, info = edit_gate(R, f"edit_{sec}", out.strip(), frep, sec, P, targets, final, dry)
                st["edit"] = info
                if ok:
                    final = txt
        chosen[sec] = final.strip()
        state["sections"][sec] = st
        if not dry:
            (D / f"judge_{C.VERSION}_{sec}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
    stage_t["1_3_sections"] = round(time.time() - t)
    chapter = "\n\n".join(chosen[s] for s in SECTIONS) + "\n"
    rep = check(chapter, P, None, targets)
    if not dry:
        (D / f"{STEM}_preauthor.md").write_text(chapter, encoding="utf-8")

    def whole(name, rnd, kind, system, extra, model=None):
        nonlocal chapter, rep
        try:
            out = R.call(name, rnd, kind, system, extra + f"\n\nCHAPTER:\n{chapter}", sum(targets.values()) + 500, model=model)
        except rn.BudgetStop as e:
            return {"kept": False, "reason": f"budget: {e}"}
        if not out:
            return {"kept": False, "reason": "call failed"}
        new = out.strip() + "\n"
        nr = check(new, P, None, targets)
        keep = nr["integrity_ok"] and score_rep(nr) <= score_rep(rep) and guards_ok(chapter, new)
        if not dry:
            (D / f"{STEM}_{name}_raw.md").write_text(new, encoding="utf-8")
        if keep:
            chapter, rep = new, nr
        return {"kept": keep, "before": p1.summ(rep), "after": p1.summ(nr)}
    t = time.time()
    state["author_pass"] = whole("author", 5, "author", AUTHOR_SYS, STYLE_BLOCK + f"CHAPTER PLAN:\n{PLAN_HEAD}\n\nSECTIONS:\n{arc(titles, secs)}\n\nPARAGRAPH POINTS:\n"
                                 + "\n\n".join(f"{titles[s]}\n{points_block(secs[s])}" for s in SECTIONS)
                                 + f"\n\nCHAPTER OPENING: {C.OPEN_IN}\nCHAPTER CLOSING: {C.CLOSE_OUT}", model=rn.FLAGSHIP)
    stage_t["5_author"] = round(time.time() - t)
    if not dry:
        (D / f"{STEM}_preverify.md").write_text(chapter, encoding="utf-8")
    t = time.time()
    if not dry:
        chapter, vst, _ = verify_sections(chapter, P, R)
        state["verification"] = {k: vst[k] for k in ("verdicts_before", "verdicts_after")}
        (D / f"{STEM}_verification.json").write_text(json.dumps(vst, ensure_ascii=False, indent=1), encoding="utf-8")
        rep = check(chapter, P, None, targets)
    else:
        for sec in SECTIONS:
            R.call(f"verify_{sec}", 6, "verify", VERIFY_SYS, "x" * 36000, 2600)
            R.call(f"fix_{sec}", 6, "fix", FIX_SYS, "x" * 16000, 600)
            R.call(f"reverify_{sec}", 6, "reverify", VERIFY_SYS, "x" * 8000, 400)
    stage_t["6_verification"] = round(time.time() - t)
    t = time.time()
    state["polish"] = {"kept": False, "reason": "cut (budget)"} if skip_polish else whole("polish", 7, "polish", POLISH_SYS, STYLE_BLOCK)
    stage_t["7_polish"] = round(time.time() - t)
    state.update(final_validation=p1.summ(rep), stage_seconds=stage_t, wall_clock_seconds=round(time.time() - t0), calls=R.calls,
                 spent_usd=round(R.spent, 4), spend_by_stage={k: round(v, 4) for k, v in R.stage_spend.items()},
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
        # sections run in sequence: wall clock is the sum over sections of (max candidate + judge + edit), then the whole-chapter rounds
        wall = sum(c["est_seconds"] for c in R.calls if c["round"] in (2, 3)) + sum(
            max(c["est_seconds"] for c in R.calls if c["round"] == 1 and c["name"].startswith(f"cand_{s}_")) for s in SECTIONS) + sum(
            max(c["est_seconds"] for c in cs) for r, cs in by.items() if r not in (1, 2, 3))
        print(json.dumps({"chapter": C.CH, "projected_cost_usd": round(R.spent, 2), "calls": len(R.calls),
                          "by_round": {r: {"calls": len(cs), "usd": round(sum(c["est_cost_usd"] for c in cs), 3)} for r, cs in sorted(by.items())},
                          "projected_wall_clock_min": round(wall / 60, 1)}, indent=1))
    else:
        for cmd in (["footnote.py", str(C.OUT)], ["make_docx.py"]):
            subprocess.run([sys.executable, "-I", str(HERE / cmd[0])] + cmd[1:])
    print(f"[{ts()}] CHAPTER {C.CH} HOUSE-VOICE PIPELINE FINISHED", flush=True)
