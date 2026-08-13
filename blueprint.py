#!/usr/bin/env python3
"""
blueprint.py — build the book's research architecture, not its prose.

Produces, per chapter, a structure detailed enough that any one research unit
can later be written independently from its own evidence and citations:

    Chapter -> Units -> Sub-units -> Topics -> Research questions
            -> Evidence required -> Reference mapping -> Citation plan

Phases
------
1-2  HIERARCHY   One structured call per chapter expands the outline's
                 sub-topics into units, sub-units, topics and per-sub-unit
                 research questions, plus chapter purpose, narrative flow,
                 dependencies and suggested figures. Cached to
                 book/_blueprint/hierarchy/chNN.json so it is editable by hand
                 and never regenerated silently.

3-4  MAPPING     Every sub-unit is retrieved against the KB independently, the
                 same way make_evidence.py retrieves a sub-topic: derived
                 queries, relevance floor, source-diversity cap. What comes back
                 is a reference table — source, heading trail, page range,
                 similarity, and what that source contributes (from
                 sources.CLASSIFICATION) — so the citation list is observed,
                 not guessed.

5    CITATIONS   Primary/secondary/tertiary split per unit; named entities the
                 unit's own questions raise that nothing retrieved supports;
                 sub-units where the corpus is thin or single-sourced; and
                 candidate conflicts, where two sources give different dates or
                 figures on the same sub-unit.

6    OUTPUT      book/_blueprint/chNN.md  (readable)
                 book/_blueprint/chNN.json (machine-readable, for the writer)
                 book/_blueprint/INDEX.md (whole-book coverage table)

Prereqs: build_kb.py, then this. Does not require make_evidence.py.
Usage:
    python blueprint.py --chapters 6          # one chapter (start here)
    python blueprint.py                       # all 19
    python blueprint.py --hierarchy-only      # phases 1-2, no retrieval
    python blueprint.py --refresh             # re-expand hierarchies
"""
import argparse
import collections
import json
import random
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import sources
from book_outline import BOOK_ANCHORS, BOOK_SUBTITLE, BOOK_TITLE, BY_NUMBER, CHAPTERS
from console import use_utf8
from kb_search import KBError, get_client, kb_stamp, search_batch
from make_evidence import (ABS_FLOOR, REL_MARGIN, apply_floor, diversify,
                           retrieve_subtopic, unevidenced_terms)
from query_gen import _anchor_for

OUT = Path("book/_blueprint")
HIER = OUT / "hierarchy"
MODEL_ENV = "MISTRAL_CHAT_MODEL"

KEEP_PER_SUBUNIT = 6      # references retained per sub-unit after filtering

HIER_SYSTEM = (
    "You are the research director for an academic monograph, designing one chapter's research "
    "architecture. You are given the chapter's title, theme, scope, and the sub-topics already "
    "settled for it. Expand it into a hierarchy that another researcher could execute unit by "
    "unit without further instruction.\n\n"
    "Each of the given sub-topics becomes one UNIT. Do not invent extra units and do not drop "
    "any. Within each unit, define 2-4 SUB-UNITS, each a single research topic that can be "
    "researched and written independently. For each sub-unit give the specific topics it covers, "
    "the research questions it must answer, and the kinds of evidence that would answer them "
    "(inscription, measured survey, gazetteer table, śāstric text, oral testimony, comparative "
    "example, and so on).\n\n"
    "Also give, for the chapter as a whole: its purpose; the questions the whole chapter answers; "
    "its narrative objective; the order the units should be read in and why; which earlier "
    "chapters it depends on; and any maps, figures, tables or timelines that would serve it.\n\n"
    "Reply with JSON only, in exactly this shape:\n"
    '{"purpose": "...", "narrative_objective": "...", "narrative_flow": "...",\n'
    ' "research_questions": ["..."], "dependencies": ["C6 — why"],\n'
    ' "figures": [{"kind": "map|figure|table|timeline", "title": "...", "purpose": "..."}],\n'
    ' "units": [{"key": "<the sub-topic key, verbatim>", "title": "...", "role": "what this unit '
    'establishes and how it sets up the next",\n'
    '   "sub_units": [{"title": "...", "topics": ["..."], "questions": ["..."],\n'
    '                  "evidence_required": ["..."]}]}]}'
)


# ── phases 1-2: hierarchy ──────────────────────────────────────────────────
def _parse_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def expand_chapter(client, model, ch, attempts=8):
    listing = "\n".join(f"- {s['key']}: {s['question']}" for s in ch["subtopics"])
    user = (
        f"BOOK: *{BOOK_TITLE}: {BOOK_SUBTITLE}* — a reference history of the Udayeśvara "
        f"(Nīlakaṇṭheśvara) temple at Udaypur, Vidisha district, Madhya Pradesh, and the "
        f"Paramāra dynasty of Malwa.\n\n"
        f"CHAPTER {ch['n']}: {ch['title']}\n"
        + (f"THEME: {ch['theme']}\n" if ch.get("theme") else "")
        + f"\nSCOPE: {ch['scope']}\n\n"
        + (f"EDITORIAL CONSTRAINTS: {ch['constraints']}\n\n" if ch.get("constraints") else "")
        + f"SUB-TOPICS (each becomes one unit, keys verbatim):\n{listing}\n\n"
        f"OTHER CHAPTERS (for dependencies): "
        + "; ".join(f"C{c['n']} {c['title']}" for c in CHAPTERS) + "\n"
    )
    delay = 6
    for n in range(1, attempts + 1):
        try:
            resp = client.chat.complete(
                model=model,
                messages=[{"role": "system", "content": HIER_SYSTEM},
                          {"role": "user", "content": user}],
                # A six-unit chapter's hierarchy runs to ~33k characters. At a
                # smaller budget the reply is cut mid-object and the JSON will
                # not parse — which surfaces as an opaque ValueError, so the
                # truncation case is named explicitly below.
                max_tokens=16000, temperature=0.3,
                response_format={"type": "json_object"})
            if getattr(resp.choices[0], "finish_reason", None) == "length":
                raise ValueError("hierarchy JSON truncated — raise max_tokens")
            data = _parse_json(resp.choices[0].message.content or "")
            if data and data.get("units"):
                return data
            raise ValueError("unusable hierarchy JSON")
        except Exception as e:                       # noqa: BLE001 - retry then fail loudly
            if n == attempts:
                raise RuntimeError(f"hierarchy expansion failed for ch{ch['n']}: {e}") from e
            wait = min(delay * 1.8, 120) * (0.75 + random.random() * 0.5)
            print(f"      retry {n}/{attempts - 1} ({type(e).__name__}), waiting {wait:.0f}s",
                  flush=True)
            time.sleep(wait)
            delay = min(delay * 1.8, 120)


def get_hierarchy(client, model, ch, refresh=False):
    HIER.mkdir(parents=True, exist_ok=True)
    p = HIER / f"ch{ch['n']:02d}.json"
    if p.exists() and not refresh:
        return json.loads(p.read_text(encoding="utf-8"))
    print(f"  [1-2] expanding hierarchy for ch{ch['n']} ...", flush=True)
    data = expand_chapter(client, model, ch)
    # Keep the outline authoritative: units must match its sub-topic keys.
    keys = [s["key"] for s in ch["subtopics"]]
    byk = {u.get("key"): u for u in data["units"]}
    data["units"] = [byk[k] for k in keys if k in byk] + \
                    [u for u in data["units"] if u.get("key") not in keys]
    p.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return data


# ── phases 3-4: reference mapping ──────────────────────────────────────────
def subunit_queries(ch, unit, sub):
    """Queries for one sub-unit: its title, its topics, and a regional anchor."""
    base = f"{sub['title']} — {'; '.join(sub.get('topics', [])[:4])}".strip(" —")
    qs = [base or sub["title"], f"{sub['title']} {_anchor_for(ch)}"]
    for q in sub.get("questions", [])[:2]:
        qs.append(q)
    seen, out = set(), []
    for q in qs:
        k = q.lower().strip()
        if k and k not in seen:
            seen.add(k); out.append(q)
    return out


def map_subunit(ch, unit, sub, client):
    qs = subunit_queries(ch, unit, sub)
    cands = retrieve_subtopic(qs, client)
    floored, cut = apply_floor(cands)
    kept = diversify(floored, keep=KEEP_PER_SUBUNIT)
    # One row per (source, section): several retrieved chunks from the same
    # section are one citation, not six. Page ranges merge, the best score is
    # kept, and `passages` records how much of the section actually matched.
    rows = {}
    for h in kept:
        key = (h["source"], h.get("trail", ""))
        r = rows.get(key)
        if r is None:
            rows[key] = {
                "source": h["source"],
                "short": sources.short(h["source"]),
                "kind": sources.kind(h["source"]),
                "contribution": sources.contribution(h["source"]),
                "locator": h.get("trail", ""),
                "page_start": h.get("page_start"),
                "page_end": h.get("page_end"),
                "score": round(h["score"], 3),
                "passages": 1,
                "excerpt": h["text"][:400],
            }
            continue
        r["passages"] += 1
        r["score"] = max(r["score"], round(h["score"], 3))
        for k, agg in (("page_start", min), ("page_end", max)):
            vals = [v for v in (r[k], h.get(k)) if v is not None]
            r[k] = agg(vals) if vals else None
        r["excerpt"] = (r["excerpt"] + " … " + h["text"][:200])[:800]
    refs = sorted(rows.values(), key=lambda r: -r["score"])
    # Questions only. Sub-unit titles are Title Case, so including them would
    # report every capitalised word as an unevidenced proper noun.
    question_blob = " ".join(sub.get("questions", []))
    return {
        "title": sub["title"],
        "topics": sub.get("topics", []),
        "questions": sub.get("questions", []),
        "evidence_required": sub.get("evidence_required", []),
        "queries": qs,
        "n_candidates": len(cands),
        "floor": round(cut, 3),
        "references": refs,
        "unevidenced": unevidenced_terms(question_blob, kept),
    }


# ── phase 5: citation planning ─────────────────────────────────────────────
_NUM_RE = re.compile(r"\b(?:1[0-9]{3}|[89][0-9]{2})\b")     # plausible year-like figures


def citation_plan(unit_map):
    """Split references by kind, and surface gaps and candidate conflicts."""
    refs = [r for su in unit_map["sub_units"] for r in su["references"]]
    by_kind = collections.defaultdict(list)
    seen = set()
    for r in refs:
        if r["source"] in seen:
            continue
        seen.add(r["source"])
        by_kind[r["kind"]].append(r)

    gaps = []
    for su in unit_map["sub_units"]:
        if not su["references"]:
            gaps.append(f"{su['title']}: nothing in the KB cleared the relevance floor")
        elif len(su["references"]) < 3:
            gaps.append(f"{su['title']}: only {len(su['references'])} passage(s) above the floor")
        elif len({r['source'] for r in su['references']}) == 1:
            gaps.append(f"{su['title']}: single-sourced ({su['references'][0]['short']})")
        if su["unevidenced"]:
            gaps.append(f"{su['title']}: nothing retrieved mentions "
                        f"{', '.join(su['unevidenced'])}")

    # Candidate conflicts: two sources giving different year-like figures within
    # one sub-unit. Flagged for a human to adjudicate, never resolved here.
    conflicts = []
    for su in unit_map["sub_units"]:
        years = collections.defaultdict(set)
        for r in su["references"]:
            for y in _NUM_RE.findall(r["excerpt"]):
                years[y].add(r["short"])
        distinct = {y: s for y, s in years.items() if s}
        if len(distinct) > 1 and len({frozenset(s) for s in distinct.values()}) > 1:
            pairs = ", ".join(f"{y} ({'; '.join(sorted(s))})" for y, s in sorted(distinct.items())[:6])
            conflicts.append(f"{su['title']}: differing dates across sources — {pairs}")

    return {
        "primary": [{"short": r["short"], "contribution": r["contribution"]} for r in by_kind["primary"]],
        "secondary": [{"short": r["short"], "contribution": r["contribution"]} for r in by_kind["secondary"]],
        "tertiary": [{"short": r["short"], "contribution": r["contribution"]} for r in by_kind["tertiary"]],
        "recommended": [r["short"] for r in sorted(refs, key=lambda x: -x["score"])[:5]],
        "conflicts": conflicts,
        "gaps": gaps,
    }


def figure_candidates(unit_map):
    """Figure/plate/map captions occurring in this unit's retrieved passages —
    a shot list of what the sources illustrate. The repository holds no image
    files, so these are pointers into the books, not assets."""
    out = []
    for su in unit_map["sub_units"]:
        for r in su["references"]:
            for m in re.finditer(r"(?i)\b((?:fig|figure|plate|pl|map|table)\.?\s*[0-9IVXivx]+[^\n.;]{0,70})",
                                 r["excerpt"]):
                out.append({"caption": m.group(1).strip(), "in": r["short"],
                            "page": r["page_start"]})
    seen, uniq = set(), []
    for f in out:
        k = f["caption"].lower()
        if k not in seen:
            seen.add(k); uniq.append(f)
    return uniq[:8]


# ── phase 6: output ────────────────────────────────────────────────────────
def build_chapter(ch, hier, client, do_retrieval=True):
    units = []
    for i, u in enumerate(hier["units"], 1):
        uid = f"{ch['n']}.{i}"
        sub_maps = []
        for j, su in enumerate(u.get("sub_units", []), 1):
            if do_retrieval:
                m = map_subunit(ch, u, su, client)
            else:
                m = {"title": su["title"], "topics": su.get("topics", []),
                     "questions": su.get("questions", []),
                     "evidence_required": su.get("evidence_required", []),
                     "queries": [], "n_candidates": 0, "floor": ABS_FLOOR,
                     "references": [], "unevidenced": []}
            m["id"] = f"{uid}.{j}"
            sub_maps.append(m)
        um = {"id": uid, "key": u.get("key"), "title": u.get("title", u.get("key")),
              "role": u.get("role", ""), "sub_units": sub_maps}
        um["citation_plan"] = citation_plan(um) if do_retrieval else {}
        um["figures"] = figure_candidates(um) if do_retrieval else []
        units.append(um)
        print(f"        unit {uid} {um['title'][:44]:46s} "
              f"{len(sub_maps)} sub-units, "
              f"{sum(len(s['references']) for s in sub_maps)} refs", flush=True)
    return units


def render_md(ch, hier, units, stamp):
    L = []
    a = L.append
    a(f"# Chapter {ch['n']} — {ch['title']}")
    if ch.get("theme"):
        a(f"\n*{ch['theme']}*")
    a(f"\n<!-- blueprint generated {datetime.now(timezone.utc).isoformat(timespec='seconds')}; "
      f"kb {stamp['hash']} ({stamp['count']} chunks) -->\n")

    a("## Purpose\n")
    a(hier.get("purpose", "—") + "\n")
    a("## Narrative objective\n")
    a(hier.get("narrative_objective", "—") + "\n")
    a("## Chapter research questions\n")
    for q in hier.get("research_questions", []):
        a(f"- {q}")
    a("\n## Narrative flow\n")
    a(hier.get("narrative_flow", "—") + "\n")
    a("## Dependencies on earlier chapters\n")
    deps = hier.get("dependencies", [])
    for d in deps or ["— none"]:
        a(f"- {d}")
    a("\n## Suggested maps, figures, tables and timelines\n")
    figs = hier.get("figures", [])
    if figs:
        a("| kind | title | purpose |")
        a("|---|---|---|")
        for f in figs:
            a(f"| {f.get('kind','')} | {f.get('title','')} | {f.get('purpose','')} |")
    else:
        a("— none proposed")

    a("\n## Coverage summary\n")
    a("| unit | title | sub-units | refs | primary | secondary | gaps |")
    a("|---|---|---:|---:|---:|---:|---:|")
    for u in units:
        cp = u.get("citation_plan", {})
        nref = sum(len(s["references"]) for s in u["sub_units"])
        a(f"| {u['id']} | {u['title']} | {len(u['sub_units'])} | {nref} | "
          f"{len(cp.get('primary', []))} | {len(cp.get('secondary', []))} | "
          f"{len(cp.get('gaps', []))} |")

    for u in units:
        a(f"\n---\n\n## Unit {u['id']} — {u['title']}\n")
        if u.get("role"):
            a(f"**Role in the chapter.** {u['role']}\n")
        for su in u["sub_units"]:
            a(f"### Sub-unit {su['id']} — {su['title']}\n")
            if su["topics"]:
                a("**Topics covered**\n")
                for t in su["topics"]:
                    a(f"- {t}")
                a("")
            if su["questions"]:
                a("**Research questions**\n")
                for q in su["questions"]:
                    a(f"- {q}")
                a("")
            if su["evidence_required"]:
                a("**Evidence required**\n")
                for e in su["evidence_required"]:
                    a(f"- {e}")
                a("")
            a("**Reference mapping**\n")
            if su["references"]:
                a("| source | kind | locator | pages | psg | sim | key contribution |")
                a("|---|---|---|---|---:|---:|---|")
                for r in su["references"]:
                    pg = ("—" if not r["page_start"]
                          else (str(r["page_start"]) if r["page_start"] == r["page_end"]
                                else f"{r['page_start']}–{r['page_end']}"))
                    loc = (r["locator"] or "—")[:60]
                    a(f"| {r['short']} | {r['kind']} | {loc} | {pg} | {r.get('passages', 1)} | "
                      f"{r['score']:.3f} | {r['contribution']} |")
            else:
                a("*No KB material cleared the relevance floor for this sub-unit.*")
            if su["unevidenced"]:
                a(f"\n> **Not in the corpus:** {', '.join(su['unevidenced'])}. "
                  f"Do not assert these when writing; either source them externally or mark "
                  f"them as gaps.")
            a("")

        cp = u.get("citation_plan", {})
        a(f"### Citation plan — Unit {u['id']}\n")
        for label in ("primary", "secondary", "tertiary"):
            items = cp.get(label, [])
            a(f"**{label.capitalize()} sources**\n")
            if items:
                for it in items:
                    a(f"- {it['short']} — {it['contribution']}")
            else:
                a("- —")
            a("")
        if cp.get("recommended"):
            a("**Recommended citations when writing**\n")
            for r in dict.fromkeys(cp["recommended"]):
                a(f"- {r}")
            a("")
        a("**Conflicting interpretations**\n")
        for c in cp.get("conflicts", []) or ["- none detected automatically"]:
            a(f"- {c}" if not c.startswith("-") else c)
        a("")
        a("**Missing evidence**\n")
        for g in cp.get("gaps", []) or ["- none"]:
            a(f"- {g}" if not g.startswith("-") else g)
        a("")
        if u.get("figures"):
            a("**Figure candidates in the sources** *(captions only — the repository holds no "
              "image files)*\n")
            for f in u["figures"]:
                a(f"- {f['caption']} — {f['in']}" + (f", p. {f['page']}" if f["page"] else ""))
            a("")
    return "\n".join(L)


def write_index(stamp):
    """Rebuild INDEX.md from whatever chapter blueprints exist on disk."""
    rows = []
    for p in sorted(OUT.glob("ch*.json")):
        b = json.loads(p.read_text(encoding="utf-8"))
        nu = len(b["units"])
        ns = sum(len(u["sub_units"]) for u in b["units"])
        nr = sum(len(s["references"]) for u in b["units"] for s in u["sub_units"])
        ng = sum(len(u.get("citation_plan", {}).get("gaps", [])) for u in b["units"])
        nc = sum(len(u.get("citation_plan", {}).get("conflicts", [])) for u in b["units"])
        npri = len({r["short"] for u in b["units"] for s in u["sub_units"]
                    for r in s["references"] if r["kind"] == "primary"})
        rows.append((b["n"], b["title"], nu, ns, nr, npri, ng, nc))
    if not rows:
        return
    L = ["# Research blueprint — coverage index", "",
         f"<!-- kb {stamp['hash']}, {stamp['count']} chunks; "
         f"{len(rows)} of {len(CHAPTERS)} chapters -->", "",
         "| ch | title | units | sub-units | refs | primary srcs | gaps | conflicts |",
         "|---:|---|---:|---:|---:|---:|---:|---:|"]
    for n, t, nu, ns, nr, npri, ng, nc in rows:
        L.append(f"| {n} | {t} | {nu} | {ns} | {nr} | {npri} | {ng} | {nc} |")
    tot = [sum(r[i] for r in rows) for i in (2, 3, 4, 6, 7)]
    L.append(f"| | **total** | **{tot[0]}** | **{tot[1]}** | **{tot[2]}** | | "
             f"**{tot[3]}** | **{tot[4]}** |")
    L += ["", "`gaps` = sub-units that are unsourced, thin, single-sourced, or name something "
              "the corpus never mentions. `conflicts` = sub-units where sources give differing "
              "dates — flagged for adjudication, never resolved automatically."]
    (OUT / "INDEX.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    use_utf8()
    import os
    ap = argparse.ArgumentParser(description="Build the book's research blueprint")
    ap.add_argument("--chapters", help="comma-separated chapter numbers (default: all)")
    ap.add_argument("--hierarchy-only", action="store_true", help="phases 1-2 only, no retrieval")
    ap.add_argument("--refresh", action="store_true", help="re-expand cached hierarchies")
    ap.add_argument("--model", default=os.environ.get(MODEL_ENV, "mistral-large-latest"))
    args = ap.parse_args()

    wanted = ({int(x) for x in args.chapters.split(",")} if args.chapters else None)
    chs = [c for c in CHAPTERS if not wanted or c["n"] in wanted]
    OUT.mkdir(parents=True, exist_ok=True)

    try:
        stamp = kb_stamp()
    except KBError as e:
        print(f"ERROR: {e}"); sys.exit(1)
    print(f"KB: {stamp['count']} chunks, hash {stamp['hash']}\n")

    client = get_client()
    summary = []
    for ch in chs:
        print(f"Chapter {ch['n']}: {ch['title'][:56]}")
        hier = get_hierarchy(client, args.model, ch, args.refresh)
        print(f"  [3-5] mapping references ...", flush=True)
        units = build_chapter(ch, hier, client, do_retrieval=not args.hierarchy_only)
        payload = {"n": ch["n"], "title": ch["title"], "theme": ch.get("theme"),
                   "scope": ch["scope"], "constraints": ch.get("constraints"),
                   "kb": stamp, "chapter": hier, "units": units}
        (OUT / f"ch{ch['n']:02d}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
        (OUT / f"ch{ch['n']:02d}.md").write_text(
            render_md(ch, hier, units, stamp), encoding="utf-8")
        nsub = sum(len(u["sub_units"]) for u in units)
        nref = sum(len(s["references"]) for u in units for s in u["sub_units"])
        ngap = sum(len(u.get("citation_plan", {}).get("gaps", [])) for u in units)
        summary.append((ch["n"], ch["title"], len(units), nsub, nref, ngap))
        print(f"  -> {OUT}/ch{ch['n']:02d}.md  ({len(units)} units, {nsub} sub-units, "
              f"{nref} refs, {ngap} gaps)\n", flush=True)

        write_index(stamp)          # after every chapter, so an interrupted
                                    # run still leaves a usable index behind


if __name__ == "__main__":
    main()
