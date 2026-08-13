#!/usr/bin/env python3
r"""
draft_chapter.py — multi-stage, evidence-grounded chapter drafting.

The previous version was a single call: stuff one evidence pack into one prompt,
ask for "~3,500 words", write whatever came back. That instruction — not any
model limit — was what capped every chapter at three or four pages, and
max_tokens=8000 then truncated the endnotes mid-word.

This version runs seven stages per chapter. Each announces itself, records what
it found, and leaves an artefact on disk, so a finished chapter can account for
how it came to exist — and a failure names the stage that caused it.

  1. KB ACCESS   Load the evidence brief and refuse it if it predates the
                 knowledge base it claims to come from.
  2. RETRIEVAL   Surfaced, not re-run: make_evidence.py did the retrieving and
                 saved which channels found what, under which floor, from which
                 books. This stage reports it.
  3. EVIDENCE    verify.validate_pack() — deterministic. Sources resolve to real
     VALIDATION  citations, passages are non-empty and unique, coverage is
                 sufficient. Runs BEFORE any prose exists, because a pack with
                 nothing behind it should fail loudly rather than become fluent
                 paragraphs about nothing.
  4. FORMULATION The model proposes a section outline (book/_plan/chNN.json),
                 then writes each section from its own slice of evidence. No
                 single call holds the whole chapter, so length is additive.
  5. EDITORIAL   Continuity, clarity, flow, engagement and economy — a revision
                 of grounded prose, never a source of facts. Every edit is
                 checked mechanically for citation preservation and discarded
                 if it dropped or invented one.
  6. VERIFY      Each section is decomposed into atomic claims and each claim is
     /REPAIR     checked for entailment against that section's own evidence.
                 What is unsupported is revised away under a budget tied to the
                 input; what survives two rounds is cut to [GAP - not in
                 sources]. This is the stage v1 lacked, and the reason it could
                 ship a chapter that cited correctly, read well and was wrong.
  7. CITATION    Passage ids (E1, E2, ...) resolve into numbered endnotes via
     /PROVENANCE sources.py, and the result is audited: invented ids removed,
                 unmapped sources and missing page numbers reported.

The run record (book/_runs/chNN_<id>.json, or --json) holds the stages, counts,
warnings, sources and timings. It holds no prompts, no model responses and no
credentials — decisions and their evidence, never the private text behind them.

Length is derived per chapter from its sub-topic count and evidence volume
rather than fixed, and `finish_reason == "length"` triggers a real continuation
call instead of a warning.

Prereqs: build_kb.py, then make_evidence.py (which writes chNN.json).
Usage:
    python draft_chapter.py 1
    python draft_chapter.py 1 6 18
    python draft_chapter.py all
    python draft_chapter.py 1 --stage plan      # stop after planning
"""
import argparse
import collections
import glob
import json
import os
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from dotenv import load_dotenv
from mistralai.client import Mistral

import sources
from book_outline import BOOK_SUBTITLE, BOOK_TITLE, BY_NUMBER, NUMBERS
from config import CFG
from console import use_utf8

load_dotenv()
load_dotenv(Path(__file__).resolve().parent / ".env", override=False)

DEFAULT_MODEL = os.environ.get("MISTRAL_CHAT_MODEL", "mistral-large-latest")
EVID = Path("book/_evidence")
PLAN = Path("book/_plan")
OUT = Path("book")

WORDS_PER_SUBTOPIC = 800     # baseline weight of one sub-topic in the chapter
EVIDENCE_SHARE = 0.25        # plus a share of the evidence actually retrieved
MIN_WORDS, MAX_WORDS = 4000, 9000
SECTION_MAX_TOKENS = 4000    # ~2,300 words of diacritic-heavy prose; sections are ~900
CONTINUE_MAX_TOKENS = 2000

VOICE = (
    "Write in the THIRD PERSON throughout — never 'I', 'we', 'us', 'you'; no direct address, no "
    "diary voice. Adopt the register of a serious narrative history: analytical, contextualising, "
    "attentive to evidence and to scholarly disagreement. Carry a rich literary cadence — long, "
    "flowing, hypotactic sentences with em-dash asides and parenthetical qualifications, elevated "
    "and exact diction, vivid but restrained imagery, varied with the occasional short, weighted "
    "sentence (evocative, never purple). Preserve correct IAST diacritics and normalise OCR-style "
    "â/î/û to ā/ī/ū."
)

GROUNDING = (
    "Ground EVERY substantive claim in the supplied EVIDENCE. Do not invent dates, names, figures "
    "or quotations. After each such claim, cite the passage it rests on using its bracketed id "
    "exactly as given — [E12], or [E12][E15] for several. Cite ids only; never write a footnote, "
    "a source name, a filename or a page number into the prose. Where the evidence is silent on "
    "something the section needs, write [GAP — not in sources] in place of the detail rather than "
    "supplying it from general knowledge. Where sources disagree, say so and cite both.\n"
    "This applies with particular force to named things. Every text, work, inscription, person, "
    "dynasty, place and date you name must appear in the evidence you were given. If a subject "
    "invites a reference you happen to know — a Purāṇa, a poem, a king — and that reference is "
    "not in the evidence, you must leave it out. An unsupported name is a worse failure than a "
    "thinner paragraph."
)


# ── model plumbing ─────────────────────────────────────────────────────────
# `complete` lives in llm.py so that every call in the pipeline — drafting,
# verification, claim extraction, retrieval judging — passes the same shared
# rate limiter. The limit is per account, so a private copy here simply meant
# this module's traffic was invisible to the throttle and collided with
# everything else. That is what produced 19 retries and two lost chapters.
from llm import LIMITER, complete            # noqa: E402


def complete_long(client, model, messages, max_tokens, temperature=0.4, max_continuations=3):
    """As `complete`, but if the model runs out of tokens mid-sentence, continue it.

    The old code printed a warning and shipped the truncated text; six of nine
    chapters ended mid-word in their endnotes.
    """
    text, finish = complete(client, model, messages, max_tokens, temperature)
    rounds = 0
    while finish == "length" and rounds < max_continuations:
        rounds += 1
        print(f"      hit token ceiling — continuation {rounds}", flush=True)
        cont = messages + [
            {"role": "assistant", "content": text},
            {"role": "user", "content": "Continue from exactly where you stopped. Do not repeat "
                                        "any text you have already written, do not restate the "
                                        "section heading, and do not summarise. Resume mid-sentence "
                                        "if that is where you stopped."},
        ]
        more, finish = complete(client, model, cont, CONTINUE_MAX_TOKENS, temperature)
        text = text.rstrip() + (" " if not text.rstrip().endswith(("\n", "—")) else "") + more.lstrip()
    return text


def _parse_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


# ── evidence helpers ───────────────────────────────────────────────────────
def load_brief(n):
    p = EVID / f"ch{n:02d}.json"
    if not p.exists():
        raise FileNotFoundError(
            f"no evidence brief at {p} — run: python make_evidence.py --chapters {n}")
    return json.loads(p.read_text(encoding="utf-8"))


def check_fresh(brief):
    """Refuse to draft from a brief built against a different KB.

    The stamp must come from retrieve.py, the same module make_evidence.py used
    to write it. It briefly came from kb_search.py here — v1's stamp, which does
    not fold in the config hash — so the two computed different values for an
    identical KB and every brief looked stale. Two implementations of one
    identity is the same failure mode as two relevance floors in two modules.
    """
    from retrieve import kb_stamp
    now = kb_stamp()
    was = brief.get("kb", {})
    if was.get("hash") != now["hash"]:
        raise RuntimeError(
            f"evidence brief is stale: built against KB {was.get('hash')} "
            f"({was.get('count')} chunks), current KB is {now['hash']} ({now['count']} chunks).\n"
            f"    Rebuild it:  python make_evidence.py --chapters {brief['n']}")


def target_words(brief):
    """Per-chapter length, from sub-topic count and how much evidence was found."""
    subs = brief["subtopics"]
    ev = sum(len(p["text"].split()) for s in subs for p in s["passages"])
    raw = WORDS_PER_SUBTOPIC * len(subs) + EVIDENCE_SHARE * ev
    return int(max(MIN_WORDS, min(MAX_WORDS, raw)))


def passages_by_id(brief):
    return {p["id"]: p for s in brief["subtopics"] for p in s["passages"]}


def render_evidence(subs):
    """Evidence for a set of sub-topic keys, as the model sees it."""
    out = []
    for s in subs:
        out.append(f"### SUB-TOPIC: {s['key']} — {s['question']}")
        if s["status"] in ("GAP", "THIN"):
            out.append(f"*(Coverage {s['status']}: {s['note']}. Do not pad this out; "
                       f"mark missing detail as [GAP — not in sources].)*")
        if s.get("unevidenced"):
            out.append("*(NOT IN THE EVIDENCE — do not name, describe, quote or allude to any "
                       "of these, however confident you are about them; they are named in the "
                       "sub-topic but nothing retrieved supports them: "
                       + ", ".join(s["unevidenced"]) + ".)*")
        for p in s["passages"]:
            out.append(f"\n[{p['id']}] {p['text']}")
        if not s["passages"]:
            out.append("\n*(No passages retrieved for this sub-topic.)*")
        out.append("")
    return "\n".join(out)


# ── stage 1: plan ──────────────────────────────────────────────────────────
PLAN_SYSTEM = (
    "You are the editor of a scholarly reference book, planning one chapter. You are given the "
    "chapter's scope, its sub-topics, and a coverage report showing where the source material is "
    "strong and where it is thin. Propose a section structure that follows the evidence rather "
    "than an imagined ideal: sections where there is material, brevity where there is not.\n"
    'Reply with JSON only: {"sections": [{"title": "...", "subtopics": ["key", ...], '
    '"argument": "two or three sentences on what this section establishes and how it advances the '
    'chapter", "weight": 0.0-1.0}]}\n'
    "Use 5 to 8 sections. `weight` is the share of the chapter's length that section should take; "
    "weights must sum to about 1.0. Every sub-topic must appear in at least one section.\n"
    "Do not pad the structure. As a rule one section anchors one sub-topic; merge two sub-topics "
    "into a section, or split one across two, only where the material genuinely calls for it. "
    "Never create a section that revisits sub-topics already covered in order to restate their "
    "argument — a reader must not meet the same material twice under different titles. Section "
    "titles should be evocative but precise, in the register of a serious history book."
)


def plan_chapter(client, model, brief, words):
    subs = brief["subtopics"]
    coverage = "\n".join(
        f"- {s['key']} [{s['status']}]: {s['question']} ({len(s['passages'])} passages, {s['note']})"
        for s in subs)
    user = (
        f"BOOK: *{BOOK_TITLE}: {BOOK_SUBTITLE}*\n\n"
        f"CHAPTER {brief['n']}: {brief['title']}\n"
        + (f"THEME: {brief['theme']}\n" if brief.get("theme") else "")
        + f"\nSCOPE: {brief['scope']}\n\n"
        f"TARGET LENGTH: about {words:,} words.\n\n"
        f"SUB-TOPICS AND COVERAGE:\n{coverage}\n"
    )
    txt, _ = complete(client, model,
                      [{"role": "system", "content": PLAN_SYSTEM},
                       {"role": "user", "content": user}],
                      max_tokens=2000, temperature=0.3)
    data = _parse_json(txt)
    if not data or not data.get("sections"):
        raise RuntimeError("planner returned no usable sections")
    keys = {s["key"] for s in subs}
    for sec in data["sections"]:
        sec["subtopics"] = [k for k in sec.get("subtopics", []) if k in keys]
    missing = keys - {k for sec in data["sections"] for k in sec["subtopics"]}
    if missing:                                   # attach orphans to the nearest section
        data["sections"][-1]["subtopics"].extend(sorted(missing))
    return data["sections"]


# ── stage 2: draft sections ────────────────────────────────────────────────
def draft_section(client, model, brief, sections, i, words):
    sec = sections[i]
    subs = [s for s in brief["subtopics"] if s["key"] in sec["subtopics"]]
    outline = "\n".join(
        f"  {j+1}. {s['title']}" + ("   <-- you are writing this one" if j == i else "")
        for j, s in enumerate(sections))
    system = (
        f"You are writing one section of a chapter in a scholarly reference book.\n\n{VOICE}\n\n"
        f"{GROUNDING}\n\n"
        "Write continuous prose in paragraphs. Open with a single '## ' heading — the section "
        "title exactly as given — and no other headings. Do not write an introduction to the "
        "chapter as a whole, do not summarise at the end, and do not stray into the territory of "
        "the other sections listed in the outline. Do not write a Notes or Bibliography section; "
        "citations are the bracketed ids only."
    )
    user = (
        f"BOOK: *{BOOK_TITLE}: {BOOK_SUBTITLE}*\n"
        f"CHAPTER {brief['n']}: {brief['title']}\n"
        f"CHAPTER SCOPE: {brief['scope']}\n\n"
        + (f"EDITORIAL CONSTRAINTS (these override everything else — obey strictly, and silently "
           f"omit any evidence that would violate them):\n{brief['constraints']}\n\n"
           if brief.get("constraints") else "")
        + f"CHAPTER OUTLINE:\n{outline}\n\n"
        f"SECTION TO WRITE: {sec['title']}\n"
        f"WHAT IT MUST ESTABLISH: {sec['argument']}\n"
        f"TARGET LENGTH: about {words:,} words.\n\n"
        f"EVIDENCE AVAILABLE TO THIS SECTION:\n{render_evidence(subs)}\n"
        f"Now write the section."
    )
    return complete_long(client, model,
                         [{"role": "system", "content": system},
                          {"role": "user", "content": user}],
                         max_tokens=SECTION_MAX_TOKENS)


# ── stage 3: editorial ─────────────────────────────────────────────────────
_EID_RE = re.compile(r"\[(E\d+)\]")
_GAP_RE = re.compile(r"\[GAP[^\]]*\]")


def citation_delta(before, after):
    """What the editorial pass did to the citations and gap markers.

    The editorial layer is the one stage whose whole purpose is to change the
    prose, which makes it the easiest place to lose provenance without anyone
    noticing: a rewritten sentence that reads better and quietly drops its [E12]
    is indistinguishable from good editing until validation fails three stages
    later. Comparing the multisets before and after is cheap and exact, so there
    is no reason to infer it from a model.

    Returns {dropped, added, gaps_lost, gaps_added} as counts of ids.
    """
    b, a = collections.Counter(_EID_RE.findall(before)), collections.Counter(_EID_RE.findall(after))
    dropped = {k: n for k, n in (b - a).items()}
    added = {k: n for k, n in (a - b).items()}
    return {"dropped": dropped, "added": added,
            "gaps_lost": max(0, len(_GAP_RE.findall(before)) - len(_GAP_RE.findall(after))),
            "gaps_added": max(0, len(_GAP_RE.findall(after)) - len(_GAP_RE.findall(before)))}


def repetition_report(texts, n=10):
    """Phrases of n words that recur across different sections."""
    seen, dupes = {}, collections.Counter()
    for idx, t in enumerate(texts):
        words = re.findall(r"[^\W\d_]+", t.lower(), re.UNICODE)
        for k in range(len(words) - n):
            g = " ".join(words[k:k + n])
            if g in seen and seen[g] != idx:
                dupes[g] += 1
            else:
                seen.setdefault(g, idx)
    return [g for g, _ in dupes.most_common(12)]


def stitch_section(client, model, brief, sections, i, texts, dupes):
    """The editorial pass: continuity, flow, clarity and reader engagement.

    This began as a narrow continuity fix and now carries the whole editorial
    remit, deliberately rather than as a sixth model call per section. An
    unconstrained editing pass over already-grounded prose is the known-dangerous
    move here: the first version of this stage inflated a chapter 59% past target
    and invented temple comparanda that read beautifully and cited nothing. The
    guards below — input-proportional budget, no-new-names rule, and the
    citation_delta() check applied by the caller — are what make a wider brief
    safe, so widening the brief without them would be a regression.
    """
    prev_tail = texts[i - 1].strip()[-700:] if i > 0 else "(this is the first section)"
    next_head = texts[i + 1].strip()[:700] if i + 1 < len(texts) else "(this is the final section)"
    rep = ("\nPhrases that recur elsewhere in this chapter — rewrite them here if they appear:\n"
           + "\n".join(f"  - {d}" for d in dupes)) if dupes else ""
    words_in = len(texts[i].split())
    system = (
        f"You are the editor of one section of a chapter of a serious narrative history. "
        f"The facts are settled and sourced; your work is on the writing.\n\n{VOICE}\n\n"
        "Improve, in this order of priority:\n"
        "  - CONTINUITY: the opening should follow from what precedes, the close should lead "
        "into what follows, and any phrasing repeated from a neighbouring section should go.\n"
        "  - CLARITY: an explanation a reader would have to re-read should be rebuilt so they "
        "do not. Prefer the concrete to the abstract where the evidence allows it.\n"
        "  - FLOW: vary sentence length; break paragraphs that have become unreadable slabs; "
        "cut the throat-clearing that delays a paragraph's point.\n"
        "  - ENGAGEMENT: keep the reader moving. A section that states its findings without "
        "ever suggesting why they matter is doing half its job.\n"
        "  - ECONOMY: remove padding, hedging stacked on hedging, and any sentence that only "
        "restates the one before it. Shorter is usually better here.\n\n"
        "Preserve every bracketed citation id ([E12]) and every [GAP — not in sources] marker "
        "exactly as they appear — do not add, remove, renumber or relocate them relative to the "
        "claims they support. If you merge two sentences, the merged sentence carries both "
        "citations. THIS IS CHECKED MECHANICALLY after you reply, and an edit that loses or "
        "invents a citation is discarded in full, so a dropped [E12] costs the reader every "
        "other improvement you made.\n"
        "This is a revision, not a rewrite, and emphatically not an expansion. Introduce no new "
        "factual claim, no new named person, place, text or date, and no illustrative comparison "
        "to any site or work not already present — an elegant aside naming somewhere the sources "
        "never mention is a fabrication, however well it reads. Engagement comes from better "
        "sentences about the evidence you have, never from adding colour you do not. "
        "The result must be no longer than "
        f"the original: about {words_in:,} words, and never more than {int(words_in * 1.1):,}. "
        "Return the complete revised section, heading included, and nothing else."
    )
    user = (
        f"CHAPTER {brief['n']}: {brief['title']}\n\n"
        f"END OF THE PRECEDING SECTION:\n\"\"\"\n{prev_tail}\n\"\"\"\n\n"
        f"START OF THE FOLLOWING SECTION:\n\"\"\"\n{next_head}\n\"\"\"\n"
        f"{rep}\n\n"
        f"SECTION TO REVISE:\n\"\"\"\n{texts[i]}\n\"\"\"\n"
    )
    # Budget the revision against the text it is revising: given headroom, the
    # model elaborates rather than tightens, which is what pushed the first
    # Chapter 1 redraft 59% past its target.
    budget = min(SECTION_MAX_TOKENS, int(words_in * 2.2) + 400)
    return complete_long(client, model,
                         [{"role": "system", "content": system},
                          {"role": "user", "content": user}],
                         max_tokens=budget, temperature=0.3)


# ── stage 4: citations ─────────────────────────────────────────────────────
def resolve_citations(body, byid):
    """Turn [E12] ids into [1]-style endnote markers plus a Notes section.

    Ids the model invented (not present in the brief) are stripped and reported,
    so a hallucinated citation cannot masquerade as a real one.
    """
    order, mapping, bogus = [], {}, set()

    def repl(m):
        eid = m.group(1)
        if eid not in byid:
            bogus.add(eid)
            return ""
        if eid not in mapping:
            order.append(eid)
            mapping[eid] = len(order)
        return f"[{mapping[eid]}]"

    body = re.sub(r"\[(E\d+)\]", repl, body)
    body = re.sub(r"[ \t]+([,.;:])", r"\1", body)
    body = re.sub(r"[ \t]{2,}", " ", body)

    notes = ["## Notes", ""]
    for eid in order:
        notes.append(f"[{mapping[eid]}] {sources.endnote(byid[eid])}")
    return body.rstrip(), "\n".join(notes), order, sorted(bogus)


def write_bibliography(used_files):
    lines = ["# Bibliography", ""]
    for f in sorted(used_files, key=lambda x: sources.full(x).lower()):
        lines.append(f"- {sources.full(f)}")
    return "\n".join(lines)


# ── orchestration ──────────────────────────────────────────────────────────
def _parallel(fn, jobs, workers, fallback=None):
    """Run `fn` over `jobs` concurrently, returning results in job order.

    Sections within a chapter do not depend on one another — each is written
    from the shared plan and its own slice of evidence — and neither do the
    continuity revisions, which all read the same pre-revision text. Only the
    plan -> draft -> stitch boundaries are real dependencies, so the fifteen
    calls a chapter needs collapse into three waves.

    `fallback(job) -> text` makes a wave fail-soft. Without it one exhausted
    retry budget on one section discards the whole chapter: a sustained 429
    during the continuity pass threw away seven fully drafted sections twice
    over. A chapter with one unstitched section is worth far more than no
    chapter, and the loss is visible in the log rather than silent.
    """
    jobs = list(jobs)
    if workers <= 1 or len(jobs) <= 1:
        out = []
        for j in jobs:
            try:
                out.append(fn(j)[1])
            except Exception as e:                   # noqa: BLE001
                if fallback is None:
                    raise
                print(f"      ! job failed ({type(e).__name__}); keeping previous text",
                      flush=True)
                out.append(fallback(j))
        return out
    out = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {}
        for k, j in enumerate(jobs):
            # No stagger here any more: llm.LIMITER paces every call globally,
            # so submitting together just queues rather than colliding. Workers
            # now control how many requests are IN FLIGHT, not how fast they
            # start — which is the thing that actually helps, since each call
            # spends 10-30s on the server.
            futures[ex.submit(fn, j)] = (k, j)
        for f in as_completed(futures):
            k, j = futures[f]
            try:
                i, text = f.result()
                out[i] = text
            except Exception as e:                   # noqa: BLE001
                if fallback is None:
                    raise
                print(f"      ! job {k + 1} failed ({type(e).__name__}); "
                      f"keeping previous text", flush=True)
                out[k] = fallback(j)
    return [out[i] for i in sorted(out)]


TOTAL_STAGES = 7


def draft(client, model, n, stage="all", outdir=None, workers=1, no_verify=False,
          run=None, show_sources=False):
    """Draft one chapter through the seven pipeline stages.

    `run` is a run.GenerationRun that records what each stage did. It is
    optional so that existing callers and tests keep working unchanged; when
    absent a throwaway record is used and only the usual CLI lines appear.
    """
    from run import GenerationRun
    from verify import validate_pack

    own_run = run is None
    if own_run:
        run = GenerationRun.start(chapter=n)

    # ── [1/7] knowledge base ────────────────────────────────────────────────
    with run.stage("Accessing knowledge base", TOTAL_STAGES) as st:
        brief = load_brief(n)
        check_fresh(brief)                       # raises if the pack predates the KB
        kb = brief.get("kb") or {}
        run.title = brief.get("title", "")
        run.kb, run.config_hash = kb, kb.get("config", "")
        st.metric("chunks in knowledge base", kb.get("count", 0))
        st.note(f"evidence pack matches KB {kb.get('hash', '?')}"
                + ("  [contextualized]" if kb.get("contextualized") else ""))
        words = target_words(brief)
        byid = passages_by_id(brief)
        st.data("kb", kb)

    # ── [2/7] retrieval (already performed by make_evidence; surfaced here) ──
    with run.stage("Retrieving evidence", TOTAL_STAGES) as st:
        subs = brief["subtopics"]
        per_source = collections.Counter(p["source"] for s in subs for p in s["passages"])
        st.metric("passages retrieved", len(byid))
        st.metric("sub-topics", len(subs))
        st.metric("reference books represented", len(per_source))
        for src, cnt in per_source.most_common():
            st.source(src, passages=cnt)
        # Why these passages: the channels and floor that produced them, saved
        # by make_evidence rather than recomputed.
        modes = {s.get("retrieval", {}).get("floor_mode") for s in subs} - {None}
        backends = {s.get("retrieval", {}).get("reranker") for s in subs} - {None}
        if backends:
            st.note(f"reranked by {', '.join(sorted(backends))}"
                    + (f"; floor {', '.join(sorted(modes))}" if modes else ""))
        cands = sum(s.get("n_candidates") or 0 for s in subs)
        if cands:
            st.note(f"{cands:,} candidates considered, {len(byid)} kept")
        st.data("per_source", dict(per_source))
        st.data("queries", {s["key"]: s.get("queries", []) for s in subs})

    # ── [3/7] evidence validation (deterministic, before any prose) ──────────
    with run.stage("Validating evidence", TOTAL_STAGES) as st:
        pack = validate_pack(brief)
        st.metric("usable passages", pack.usable_passages)
        st.note(pack.summary())
        for w in pack.warnings:
            st.warn(w)
        for e in pack.errors:
            st.error(e)
        st.data("validation", pack.to_dict())
        if pack.errors:
            raise RuntimeError("; ".join(pack.errors))

    flagged = pack.gap_subtopics + pack.thin_subtopics

    # ── [4/7] formulation: plan, then draft each section ────────────────────
    PLAN.mkdir(parents=True, exist_ok=True)
    plan_path = PLAN / f"ch{n:02d}.json"
    with run.stage("Formulating chapter", TOTAL_STAGES) as st:
        sections = plan_chapter(client, model, brief, words)
        plan_path.write_text(json.dumps(sections, ensure_ascii=False, indent=1),
                             encoding="utf-8")
        st.metric("sections planned", len(sections))
        st.note(f"target {words:,} words; plan -> {plan_path}")
        for s in sections:
            st.note(f"  {s['title']}  ({', '.join(s['subtopics'])})")
        covered = {k for s in sections for k in s.get("subtopics", [])}
        missing = [s["key"] for s in brief["subtopics"] if s["key"] not in covered]
        if missing:
            st.warn(f"{len(missing)} sub-topic(s) not assigned to any section: "
                    f"{', '.join(missing[:4])}")
        if flagged:
            st.warn(f"{len(flagged)} sub-topic(s) will be written as gaps: "
                    f"{', '.join(flagged[:4])}")
        st.data("plan", sections)
    if stage == "plan":
        return None

    total_w = sum(max(0.05, float(s.get("weight", 1 / len(sections)))) for s in sections)
    print(f"      drafting {len(sections)} sections ({workers} at a time) ...", flush=True)
    plans = []
    for i, s in enumerate(sections):
        share = max(0.05, float(s.get("weight", 1 / len(sections)))) / total_w
        plans.append((i, int(words * share)))

    def _draft(job):
        i, sw = job
        t = draft_section(client, model, brief, sections, i, sw)
        print(f"        done {i+1}/{len(sections)} {sections[i]['title'][:46]} "
              f"({len(t.split()):,}w of ~{sw:,})", flush=True)
        return i, t

    def _draft_failed(job):
        """A section that could not be drafted becomes an explicit, visible gap.

        Not silence: validate_book.py counts gap markers, so an undrafted
        section shows up in the report instead of the chapter merely being
        short by a thousand words for no stated reason.
        """
        title = sections[job[0]]["title"]
        return (f"### {title}\n\n{CFG.verify.gap_marker} "
                f"(this section could not be drafted — the model call failed "
                f"after every retry; re-run this chapter)")

    texts = _parallel(_draft, plans, workers, fallback=_draft_failed)
    drafted = list(texts)
    run.stages[-1].metric("words drafted", sum(len(t.split()) for t in texts))
    run.stages[-1].metric("source-backed claims",
                          len(set(_EID_RE.findall("\n".join(texts)))))

    # ── [5/7] editorial ─────────────────────────────────────────────────────
    with run.stage("Refining prose", TOTAL_STAGES) as st:
        dupes = repetition_report(texts)
        if dupes:
            st.note(f"{len(dupes)} cross-section repeat(s) found")

        def _stitch(i):
            return i, stitch_section(client, model, brief, sections, i, texts, dupes)

        edited = _parallel(_stitch, range(len(texts)), workers,
                           fallback=lambda i: texts[i])

        # An editorial pass that drops or invents a citation is discarded for
        # that section. The check is exact and costs nothing, and it is what
        # makes it safe to give this stage a wide brief: the model is told it
        # will be checked, and it is.
        kept_edits, reverted, deltas = 0, [], []
        for i, (before, after) in enumerate(zip(texts, edited)):
            d = citation_delta(before, after)
            if d["dropped"] or d["added"] or d["gaps_lost"]:
                reverted.append((i, d))
                edited[i] = before
            else:
                kept_edits += 1
            deltas.append(d)
        texts = edited

        st.metric("sections refined", kept_edits)
        before_w = sum(len(t.split()) for t in drafted)
        after_w = sum(len(t.split()) for t in texts)
        st.note(f"{before_w:,} -> {after_w:,} words "
                f"({(after_w - before_w) / max(before_w, 1) * 100:+.0f}%)")
        if reverted:
            for i, d in reverted:
                why = []
                if d["dropped"]:
                    why.append(f"dropped {', '.join(sorted(d['dropped']))}")
                if d["added"]:
                    why.append(f"invented {', '.join(sorted(d['added']))}")
                if d["gaps_lost"]:
                    why.append(f"lost {d['gaps_lost']} gap marker(s)")
                st.warn(f"s{i+1} edit discarded — {'; '.join(why)}; original kept")
        else:
            st.note("citations and gap markers preserved in every section")
        st.data("citation_deltas", deltas)

    # ── VERIFY -> REPAIR (§5.1) ────────────────────────────────────────────
    # The stage v1 lacked. Grounding was measured after the fact and nothing
    # acted on it, so a chapter that cited correctly, read well and was still
    # wrong reached the manuscript unimpeded. Each section is checked against
    # its OWN slice of evidence — the pack the section was written from — because
    # checking against the whole chapter's pack would let a passage retrieved
    # for sub-topic 3 excuse an invention in sub-topic 7.
    verify_stage = run.stage("Validating chapter against evidence", TOTAL_STAGES)
    if CFG.verify.enabled and not no_verify:
        from verify import cut_unsupported, repair, verify_section
        from entities import EntityIndex
        ix = EntityIndex.load()
        vst = verify_stage.__enter__()

        def _verify(i):
            keys = set(sections[i].get("subtopics") or [])
            psg = [p for s in brief["subtopics"] if not keys or s["key"] in keys
                   for p in s["passages"]]
            if not psg:                      # a section with no evidence of its own
                return i, texts[i], None     # is a planning problem, not a grounding one
            try:
                rep = verify_section(client, texts[i], psg, entities=ix, model=model)
                before = rep.rate
                text, rep, _hist = repair(client, texts[i], rep, psg, entities=ix, model=model)
                n_cut = 0
                if rep.unsupported and CFG.verify.cut_unsupported:
                    text, n_cut = cut_unsupported(text, rep)
                print(f"        s{i+1} {sections[i]['title'][:34]:36s} "
                      f"faithful {before*100:.0f}% -> {rep.rate*100:.0f}%  "
                      f"({len(rep.unsupported)} unsupported, "
                      f"{len(rep.contradicted)} contradicted"
                      + (f", {n_cut} cut" if n_cut else "") + ")", flush=True)
                return i, text, rep
            except Exception as e:           # noqa: BLE001
                # The gate must not destroy the thing it is gating. A chapter
                # that has been planned, drafted and stitched is expensive; if
                # verification breaks, ship the unverified text and say so
                # loudly rather than discarding the work. validate_book.py is
                # strict by default and will refuse to assemble it, so the
                # failure still cannot reach the manuscript silently.
                vst.warn(f"s{i+1} verification failed ({type(e).__name__}) — "
                         f"section kept UNVERIFIED")
                return i, texts[i], None

        out_v = {}
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = []
            for i in range(len(texts)):
                if i:
                    time.sleep(1.5)
                futs.append(ex.submit(_verify, i))
            for f in as_completed(futs):
                i, text, rep = f.result()
                out_v[i] = (text, rep)
        texts = [out_v[i][0] for i in sorted(out_v)]
        reps = [out_v[i][1] for i in sorted(out_v)]
        checked = [r for r in reps if r]
        if checked:
            tot = sum(r.checked for r in checked)
            sup = sum(len(r.supported) for r in checked)
            unv = sum(len(r.unverified) for r in checked)
            vst.metric("factual claims judged", tot)
            vst.note(f"{sup}/{tot} judged claims supported by their own evidence "
                     f"({sup / tot * 100:.0f}% faithful)" if tot
                     else "no claims could be judged")
            if unv:
                # Loud, because the faithfulness figure above is only as
                # meaningful as the share of claims behind it.
                cov = tot / (tot + unv) * 100
                vst.warn(f"{unv} claim(s) COULD NOT BE VERIFIED — the verifier "
                         f"failed on them, so only {cov:.0f}% of this chapter's "
                         f"claims were judged. They are NOT cut; grounding here "
                         f"is unknown, not disproven.")
            uns = sum(len(r.unsupported) for r in checked)
            con = sum(len(r.contradicted) for r in checked)
            if uns:
                vst.warn(f"{uns} claim(s) still unsupported after repair; cut to "
                         f"{CFG.verify.gap_marker}")
            if con:
                vst.warn(f"{con} claim(s) CONTRADICTED by the sources — these need "
                         f"correcting, not deleting")
            vst.data("faithfulness", {"supported": sup, "judged": tot,
                                      "unverified": unv})
        verify_stage.__exit__(None, None, None)
    else:
        with run.stage("Validating chapter against evidence", TOTAL_STAGES) as st:
            st.status = "skipped"
            st.warn("verification skipped (--no-verify); grounding is unchecked")

    # ── [7/7] citation resolution + provenance audit ────────────────────────
    with run.stage("Resolving citations and provenance", TOTAL_STAGES) as st:
        body = f"# Chapter {n}\n\n## {brief['title']}\n\n" + "\n\n".join(texts)
        body, notes, order, bogus = resolve_citations(body, byid)
        used = {byid[e]["source"] for e in order}

        st.metric("endnotes resolved", len(order))
        st.metric("reference books cited", len(used))
        if bogus:
            st.warn(f"{len(bogus)} invented citation id(s) removed: "
                    f"{', '.join(sorted(bogus)[:6])}")
        else:
            st.note("every citation resolves to a retrieved passage")

        # Provenance audit. A citation that resolves to a bare filename with no
        # page is traceable in principle and useless in practice, so the two
        # failures are reported separately.
        thin = [e for e in order if not byid[e].get("page_start")]
        unmapped = sorted({s for s in used if s in sources.unmapped([s])})
        if unmapped:
            st.warn(f"{len(unmapped)} cited source(s) missing from sources.py; their "
                    f"endnotes fall back to filenames: {', '.join(unmapped[:3])}")
        if thin:
            st.note(f"{len(thin)} endnote(s) carry no page number "
                    f"(none survived that source's OCR)")
        for src in sorted(used):
            st.source(src, cited=sum(1 for e in order if byid[e]["source"] == src))
        st.data("endnotes", [{"marker": i + 1, "id": e, "source": byid[e]["source"],
                              "trail": byid[e].get("trail", ""),
                              "page_start": byid[e].get("page_start")}
                             for i, e in enumerate(order)])

        out = Path(outdir) if outdir else OUT
        out.mkdir(parents=True, exist_ok=True)
        path = out / f"chapter-{n:02d}.md"
        path.write_text(body + "\n\n" + notes + "\n", encoding="utf-8")
        words_out = len(re.split(r"\s+", body.split("## Notes")[0]))

    run.finish(words=words_out, endnotes=len(order), sources=len(used),
               path=str(path), pacing=LIMITER.stats())
    return used


def run_tail(run, show_sources=False):
    """The closing summary for one chapter.

    The per-stage lines were already printed live by run.stage() as each stage
    finished — a chapter takes many minutes and a user watching it needs to see
    progress, not a report at the end. This adds only what can be known once
    everything is done.
    """
    out = [""]
    if show_sources:
        srcs = run.all_sources()
        if srcs:
            out.append(f"Reference books drawn on ({len(srcs)}):")
            for s in srcs:
                bits = [f"{s.get('passages', 0)} passages retrieved"]
                if s.get("cited"):
                    bits.append(f"{s['cited']} cited")
                out.append(f"  {s['source'][:54]:56s} {', '.join(bits)}")
            out.append("")
    o = run.output
    out.append(f"✓ Chapter draft generated — {o.get('words', 0):,} words, "
               f"{o.get('endnotes', 0)} endnotes, {o.get('sources', 0)} sources cited")
    if run.warnings:
        out.append(f"  ⚠ {len(run.warnings)} warning(s) across "
                   f"{len({s for s, _ in run.warnings})} stage(s)")
    if o.get("path"):
        out.append(f"  {o['path']}")
    pac = o.get("pacing") or {}
    if pac.get("throttles"):
        out.append(f"  pacing: settled at {pac['rps']} req/s after "
                   f"{pac['throttles']} throttle event(s)")
    out.append(f"  run {run.run_id} · {run.seconds:.0f}s · book/_runs/")
    return "\n".join(out)


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Draft book chapter(s) from KB evidence briefs")
    ap.add_argument("chapters", nargs="+", help=f"chapter numbers {NUMBERS} or 'all'")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--stage", choices=["plan", "all"], default="all")
    ap.add_argument("--no-verify", action="store_true",
                    help="skip the VERIFY/REPAIR gate (faster; ships ungrounded prose)")
    ap.add_argument("--out", help="directory for the drafted chapters (default: book/)")
    ap.add_argument("--workers", type=int, default=4,
                    help="sections written concurrently (default 4; 1 = sequential)")
    ap.add_argument("--skip-existing", action="store_true",
                    help="leave chapters that are already drafted in --out alone")
    # Observability. Deliberately few: the stage view is ON by default because a
    # run nobody can see is how this pipeline shipped a fabricated chapter, and
    # burying that behind --verbose would keep the default opaque.
    ap.add_argument("--show-sources", action="store_true",
                    help="list the reference books each chapter drew on")
    ap.add_argument("--verbose", action="store_true",
                    help="include per-stage structured detail")
    ap.add_argument("--json", dest="as_json", action="store_true",
                    help="emit the run record as JSON on stdout (implies --quiet)")
    ap.add_argument("--no-run-log", action="store_true",
                    help="do not write the run record to book/_runs/")
    args = ap.parse_args()

    key = os.environ.get("MISTRAL_API_KEY")
    if not key:
        print("ERROR: MISTRAL_API_KEY not set (put it in .env)"); sys.exit(1)

    nums = NUMBERS if args.chapters == ["all"] else None
    if nums is None:
        try:
            nums = [int(x) for x in args.chapters]
        except ValueError:
            print("ERROR: chapters must be numbers or 'all'"); sys.exit(1)

    from run import GenerationRun, render, summary_line

    client = Mistral(api_key=key)
    ok, used, runs = 0, set(), []
    echo = not args.as_json
    for n in nums:
        if n not in BY_NUMBER:
            print(f"  ! no chapter {n} in book_outline.py"); continue
        dest = Path(args.out) if args.out else OUT
        if args.skip_existing and (dest / f"chapter-{n:02d}.md").exists():
            if echo:
                print(f"\nChapter {n}: already drafted in {dest}/ — skipping")
            continue
        run = GenerationRun.start(chapter=n, title=BY_NUMBER[n]["title"])
        runs.append(run)
        if echo:
            print(f"\nChapter {n} generation — {BY_NUMBER[n]['title']}")
            print("─" * 60)
        try:
            u = draft(client, args.model, n, args.stage, args.out, args.workers,
                      no_verify=args.no_verify, run=run)
            if u is not None:
                used |= u; ok += 1
        except Exception as e:                       # noqa: BLE001 - report, continue
            # The stage that failed is already recorded by run.stage(); this
            # only reports it. "chapter 6 failed: SDKError" named no stage and
            # left the user guessing which of seven had died.
            run.finish()
            stage = run.stages[-1].name if run.stages else "startup"
            if echo:
                print(f"\n  ✗ FAILED in stage «{stage}» — "
                      f"{type(e).__name__}: {str(e)[:200]}")
        else:
            if echo:
                print(run_tail(run, show_sources=args.show_sources))
        finally:
            if not args.no_run_log:
                try:
                    run.save()
                except OSError as e:
                    if echo:
                        print(f"  (could not write run log: {e})")

    if args.as_json:
        print(json.dumps([r.to_dict() for r in runs], ensure_ascii=False, indent=1))

    if used:
        dest = Path(args.out) if args.out else OUT
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "Bibliography.md").write_text(write_bibliography(used) + "\n", encoding="utf-8")
        miss = sources.unmapped(used)
        if miss and echo:
            print(f"\n! sources with no bibliography entry (add to sources.py): {miss}")
    if echo:
        if len(runs) > 1:
            print("\nRun summary")
            print("─" * 60)
            for r in runs:
                print(summary_line(r))
        print(f"\nDone: {ok}/{len(nums)} chapter(s). Next: python validate_book.py")


if __name__ == "__main__":
    main()
