#!/usr/bin/env python3
"""
unit_outline.py — the Chapter-Wise Unit Outline, a first-class planning
artifact generated BEFORE any prose, distinct from (and richer than)
draft_chapter.py's plan_chapter().

Why this exists as its own stage rather than a bigger plan_chapter() prompt:
plan_chapter() answers "what sections, in what order, what share of the
chapter's length" -- a structural question, cheap to get right in one 2000-
token call. This module answers a different, source-aware question for each
of those sections: which sources actually speak to it, what each contributes,
where two sources disagree, which evidence ids are load-bearing, what belongs
here versus in a neighbouring unit. That needs the sources' actual content in
front of the model, not just their titles -- a bigger, once-per-chapter call,
not a repeatable per-regeneration one. Keeping it separate means a plan_chapter()
re-run (cheap, sometimes wanted) doesn't force a re-run of this (pricier, and
should stay stable once the evidence pack is fixed).

The chapter's existing subtopics (book_outline.py, already retrieval-scoped in
the evidence pack -- see draft_chapter.py's load_brief) are the seed units:
retrieval is already organised around them, so re-deriving unit boundaries
from scratch would either duplicate that work or drift out of sync with it.
This stage elaborates each subtopic into a full research/writing brief; it
does not re-retrieve or re-chunk anything.

    from unit_outline import build_coverage, plan_outline, render_outline_md, render_coverage_md

    coverage = build_coverage(brief)                       # deterministic, free
    outline = plan_outline(client, model, brief, coverage)  # one LLM call
"""
import json
from collections import defaultdict
from pathlib import Path

import sources as src_mod
from llm import complete_json

OUTLINE = Path("book/_plan")


# ── source coverage matrix (deterministic -- no LLM call) ──────────────────
def build_coverage(brief):
    """Source x unit matrix, computed straight from the evidence pack already
    on disk. No retrieval, no LLM call -- point #16's own principle applied to
    point #10's requirement: this is arithmetic over data the pipeline already
    has, not a judgement call a model needs to make.

    Returns a list of rows: {source, kind, contribution, units: [keys],
    passages: {unit_key: count}, required}. `required` is a heuristic, not a
    mandate -- see plan_outline's system prompt, which is told explicitly not
    to force marginal sources into the prose just to raise this number.
    """
    by_source = defaultdict(lambda: {"units": [], "passages": {}})
    for s in brief["subtopics"]:
        # Per SOURCE, not per unit key: a set shared across every source in
        # this subtopic's passage list, keyed only on s["key"], marked that
        # key "seen" after the first passage regardless of which source it
        # belonged to -- every other source appearing later in the SAME
        # subtopic then silently failed the `not in` check and never got its
        # unit recorded at all. Confirmed live: every row except whichever
        # source happened to hold the first passage of a subtopic came back
        # with an empty units list despite having real passages there.
        sources_seen_here = set()
        for p in s["passages"]:
            src = p["source"]
            row = by_source[src]
            if src not in sources_seen_here:
                row["units"].append(s["key"])
                sources_seen_here.add(src)
            row["passages"][s["key"]] = row["passages"].get(s["key"], 0) + 1

    rows = []
    for src, data in by_source.items():
        kind = src_mod.kind(src)
        total = sum(data["passages"].values())
        rows.append({
            "source": src,
            "kind": kind,
            "contribution": src_mod.contribution(src),
            "units": data["units"],
            "passages": data["passages"],
            "total_passages": total,
            # A source cited from >=2 units or classified primary/secondary
            # with real passage weight is doing real work; one stray passage
            # from a tertiary survey is exactly the "don't force it" case
            # point #10 warns about -- flagged, not excluded.
            "required": kind != "tertiary" or total >= 3 or len(data["units"]) >= 2,
        })
    rows.sort(key=lambda r: (-r["total_passages"], r["source"]))
    return rows


def render_coverage_md(brief, rows):
    unit_titles = {s["key"]: s["question"][:40] for s in brief["subtopics"]}
    lines = [f"# Source Coverage Matrix — Chapter {brief['n']}: {brief['title']}", ""]
    lines.append("| Source | Kind | Units | Passages | Required? | Contribution |")
    lines.append("|---|---|---|---|---|---|")
    for r in rows:
        units = ", ".join(r["units"])
        lines.append(f"| {src_mod.short(r['source'])} | {r['kind']} | {units} | "
                     f"{r['total_passages']} | {'Yes' if r['required'] else 'Optional'} | "
                     f"{r['contribution']} |")
    lines.append("")
    lines.append("Units:")
    for k, t in unit_titles.items():
        lines.append(f"- `{k}` — {t}")
    return "\n".join(lines) + "\n"


# ── the outline itself (one LLM call, source-grounded) ──────────────────────
OUTLINE_SYSTEM = """You are the research editor of a scholarly reference book about a historic \
temple town, preparing the WRITING PLAN for one chapter -- not the chapter's prose.

You are given the chapter's specification, its planned units (each tied to a sub-topic already \
retrieved from the knowledge base), and for each unit the actual evidence passages available, \
each tagged with a source and an evidence id like [E4].

For EACH unit, produce:
  - purpose: one or two sentences on what this unit must establish and how it advances the \
chapter's argument
  - key_questions: 2-4 concrete questions this unit must answer
  - topics: the specific topics/claims this unit should cover, in a sensible order
  - sources: for each source that is actually load-bearing for this unit, its filename and what \
it specifically contributes (chronology? architecture? testimony? a contested claim?) -- do not \
list a source here unless its passages genuinely inform this unit
  - required_evidence: the evidence ids (e.g. "E4") from the supplied passages that are essential \
to ground this unit's key claims -- only ids that actually appear in this unit's passages
  - conflicts: places where two sources disagree or where the evidence is incomplete/ambiguous -- \
each with the issue, the positions (which source says what), and how the prose should handle it \
(present both and explain the basis; prefer the primary source; flag as unresolved). Empty list \
if there is no real conflict -- do not invent one.
  - entities: proper nouns (people, places, dynasties, structures) central to this unit
  - boundaries: one sentence on what this unit should NOT cover because it belongs to a different \
unit -- name that unit's key

Also produce a chapter-level `thesis`: two or three sentences on the chapter's central argument, \
tying the units together.

Ground every field in the supplied evidence. Do not invent sources, evidence ids, dates, or \
claims not present in what you were given. If a unit's evidence is thin, say so in `purpose` or \
`conflicts` rather than inventing coverage.

Reply with JSON only:
{"thesis": "...",
 "units": [{"key": "<the sub-topic key exactly as given>", "purpose": "...",
            "key_questions": ["..."], "topics": ["..."],
            "sources": [{"source": "<filename>", "contribution": "..."}],
            "required_evidence": ["E4", "E9"],
            "conflicts": [{"issue": "...", "positions": ["..."], "treatment": "..."}],
            "entities": ["..."], "boundaries": "..."}]}"""


def _unit_evidence_block(s, max_chars=260):
    """Condensed passages for one sub-topic: id, source, a short excerpt.
    Full passage text isn't needed here -- the outline reasons about WHICH
    sources say WHAT in general, not the exact wording, and sending all ~50
    full passages (the whole chapter's evidence pack) would make this call as
    context-heavy as the thing it's meant to prevent (§16's own principle)."""
    lines = [f"### UNIT: {s['key']} — {s['question']}"]
    for p in s["passages"]:
        excerpt = p["text"][:max_chars].replace("\n", " ")
        lines.append(f"[{p['id']}] ({p['source']}) {excerpt}...")
    return "\n".join(lines)


def plan_outline(client, model, brief, coverage):
    coverage_summary = "\n".join(
        f"- {src_mod.short(r['source'])} [{r['kind']}] -- {r['contribution']} "
        f"(used in: {', '.join(r['units'])}, {r['total_passages']} passage(s))"
        for r in coverage)
    units_block = "\n\n".join(_unit_evidence_block(s) for s in brief["subtopics"])
    user = (
        f"CHAPTER {brief['n']}: {brief['title']}\n"
        + (f"THEME: {brief['theme']}\n" if brief.get("theme") else "")
        + f"SCOPE: {brief['scope']}\n\n"
        f"SOURCE COVERAGE (whole chapter):\n{coverage_summary}\n\n"
        f"EVIDENCE BY UNIT:\n{units_block}\n"
    )
    # think=True: this call has to notice cross-source disagreement and thin
    # coverage, not just restate the sub-topic questions -- the same reasoning
    # verify.py's decompose()/entail() rely think=True for (see llm.complete's
    # docstring), applied to an analytical task instead of an extraction one.
    data = complete_json(client, model,
                         [{"role": "system", "content": OUTLINE_SYSTEM},
                          {"role": "user", "content": user}],
                         max_tokens=6000, temperature=0.3, think=True, stage="plan_outline")
    if not data or not data.get("units"):
        raise RuntimeError("outline planner returned no usable units")
    by_key = {u["key"]: u for u in data["units"] if u.get("key")}
    order = [s["key"] for s in brief["subtopics"]]     # the chapter's own order, not a set's
    # Keep only units tied to a real sub-topic, in the chapter's own order --
    # a model that invents an extra "unit" or drops one silently must not
    # silently reshape the chapter; missing units are visible gaps, not a
    # smaller chapter nobody asked for.
    data["units"] = [by_key[k] for k in order if k in by_key]
    missing = [k for k in order if k not in by_key]
    if missing:
        data["_missing_units"] = missing
    return data


def render_outline_md(brief, outline):
    lines = [f"# Chapter-Wise Unit Outline — Chapter {brief['n']}: {brief['title']}", ""]
    lines.append(f"**Chapter thesis:** {outline.get('thesis', '(none produced)')}")
    lines.append("")
    if outline.get("_missing_units"):
        lines.append(f"> ⚠ units with no outline produced: {', '.join(outline['_missing_units'])}"
                     " -- fell back to the bare sub-topic question at draft time.")
        lines.append("")
    titles = {s["key"]: s["question"] for s in brief["subtopics"]}
    for i, u in enumerate(outline["units"], 1):
        lines.append(f"## Unit {i}: {u['key']} — {titles.get(u['key'], '')}")
        lines.append(f"**Purpose:** {u.get('purpose', '')}")
        lines.append("")
        if u.get("key_questions"):
            lines.append("**Key questions:**")
            lines += [f"- {q}" for q in u["key_questions"]]
            lines.append("")
        if u.get("topics"):
            lines.append("**Topics to cover:**")
            lines += [f"- {t}" for t in u["topics"]]
            lines.append("")
        if u.get("sources"):
            lines.append("**Relevant sources:**")
            for s in u["sources"]:
                lines.append(f"- {src_mod.short(s.get('source', ''))} — {s.get('contribution', '')}")
            lines.append("")
        if u.get("required_evidence"):
            lines.append(f"**Required evidence:** {', '.join(u['required_evidence'])}")
            lines.append("")
        if u.get("entities"):
            lines.append(f"**Important entities:** {', '.join(u['entities'])}")
            lines.append("")
        if u.get("conflicts"):
            lines.append("**Potential scholarly disagreements:**")
            for c in u["conflicts"]:
                positions = "; ".join(c.get("positions", []))
                lines.append(f"- {c.get('issue', '')} — {positions} "
                             f"→ *treatment:* {c.get('treatment', '')}")
            lines.append("")
        if u.get("boundaries"):
            lines.append(f"**Boundaries:** {u['boundaries']}")
        lines.append("")
    return "\n".join(lines) + "\n"


def save(n, brief, coverage, outline):
    OUTLINE.mkdir(parents=True, exist_ok=True)
    (OUTLINE / f"ch{n:02d}_coverage.json").write_text(
        json.dumps(coverage, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUTLINE / f"ch{n:02d}_coverage.md").write_text(
        render_coverage_md(brief, coverage), encoding="utf-8")
    (OUTLINE / f"ch{n:02d}_outline.json").write_text(
        json.dumps(outline, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUTLINE / f"ch{n:02d}_outline.md").write_text(
        render_outline_md(brief, outline), encoding="utf-8")


def load_outline(n):
    p = OUTLINE / f"ch{n:02d}_outline.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def main():
    import argparse
    from console import use_utf8
    from llm import get_writing_client, WRITING_MODEL
    from draft_chapter import load_brief, check_fresh

    use_utf8()
    ap = argparse.ArgumentParser(description="Generate the Chapter-Wise Unit Outline for a chapter")
    ap.add_argument("chapter", type=int)
    args = ap.parse_args()

    brief = load_brief(args.chapter)
    check_fresh(brief)
    coverage = build_coverage(brief)
    client = get_writing_client()
    print(f"Planning units for chapter {args.chapter}: {brief['title']} ...")
    outline = plan_outline(client, WRITING_MODEL, brief, coverage)
    save(args.chapter, brief, coverage, outline)
    print(f"  -> {OUTLINE}/ch{args.chapter:02d}_outline.md")
    print(f"  -> {OUTLINE}/ch{args.chapter:02d}_coverage.md")
    if outline.get("_missing_units"):
        print(f"  ⚠ missing units: {outline['_missing_units']}")


if __name__ == "__main__":
    main()
