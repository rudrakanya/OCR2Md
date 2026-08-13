#!/usr/bin/env python3
"""
coherence.py — cross-chapter consistency (§5.3).

The gap v1 did not close, and the most consequential one for a manuscript
rather than a Q&A system. Nineteen chapters totalling ~148,000 words are drafted
independently, four workers in parallel, each scoped to its own evidence brief.
Nothing compares chapter 7 against chapter 12. The consequences are structural:

  contradiction    two chapters date the temple's completion differently, both
                   correctly cited, because each retrieved a different source and
                   neither knows the other exists. claims.py detects conflicts
                   WITHIN the corpus; nothing detected them within the manuscript.
  redundancy       validate_book.py's `rep` check catches ten-word phrases inside
                   one chapter. The Paramāra genealogy can be explained from
                   scratch in six chapters with no shared phrasing and no flag.
  broken chains    "as discussed above" pointing at a later chapter; a term
                   introduced as new that the reader met three chapters ago.
  voice drift      nineteen independent runs, nineteen registers.

Four passes. The first three are REPORTS, not repairs — a redundancy the
pipeline flags may be deliberate reinforcement, and only the author can tell.
The fourth is a generation-time change.

  1. manuscript claim index      claims.py --extract-manuscript, grouped across
                                 chapters. Unlike a corpus conflict, a manuscript
                                 contradiction is not a matter for historical
                                 judgement: one of them is simply wrong.
  2. concept-introduction ledger first substantive treatment of each registry
                                 entity, by chapter. Flags entities explained
                                 substantively in 3+ chapters (redundancy) and
                                 entities used before their first explanation
                                 (forward dependency).
  3. cross-reference resolution  every "as we saw" / "discussed below" checked
                                 against the ledger and the outline order.
  4. style exemplars             a hand-approved set of passages in the target
                                 register, retrieved into each DRAFT prompt as
                                 voice anchors.

Usage:
    python coherence.py --all --dir chapter_drafts
    python coherence.py --ledger
    python coherence.py --xrefs
    python coherence.py --exemplars book/_style.json
"""
import argparse
import collections
import json
import re
import sys
from pathlib import Path

from book_outline import BY_NUMBER, CHAPTERS
from config import CFG
from console import use_utf8
from entities import EntityIndex
from kb_store import KBStore
from textnorm import WORD_RE, fold

OUT = Path("book/_coherence")

# Backward references must resolve to an EARLIER chapter, forward ones to a later.
_XREF_RE = re.compile(
    r"\b(as (?:we (?:saw|have seen)|noted|discussed|described|shown)"
    r"|discussed (?:above|below|earlier|later)"
    r"|the (?:previous|preceding|last|next|following) chapter"
    r"|see (?:above|below|chapter \d+)"
    r"|chapter \d+"
    r"|earlier in this (?:book|study)|later in this (?:book|study))\b",
    re.IGNORECASE)

_BACKWARD = ("saw", "have seen", "noted", "discussed above", "discussed earlier",
             "previous chapter", "preceding chapter", "last chapter", "see above",
             "earlier in this")
_FORWARD = ("below", "next chapter", "following chapter", "later in this")

# A mention is "substantive" if the entity is explained, not merely named.
_EXPLAIN_RE = re.compile(
    r"\b(is|was|were|are|refers to|means|denotes|known as|so called|that is|namely|"
    r"consists of|comprises|describes|designates)\b", re.IGNORECASE)


def load_chapters(dirpath):
    out = []
    for p in sorted(Path(dirpath).glob("chapter-*.md")):
        m = re.search(r"chapter-(\d+)", p.name)
        if m:
            out.append((int(m.group(1)), p, p.read_text(encoding="utf-8")))
    return out


def _paragraphs(text):
    body = text.split("## Notes")[0]
    return [p.strip() for p in re.split(r"\n\s*\n", body) if len(p.strip()) > 120]


def concept_ledger(chapters, entities, min_chapters=3):
    """First substantive treatment of each entity, by chapter."""
    ledger = collections.defaultdict(lambda: {"substantive": [], "mentioned": []})
    for n, _path, text in chapters:
        for para in _paragraphs(text):
            folded = {fold(w) for w in WORD_RE.findall(para)}
            explained = bool(_EXPLAIN_RE.search(para))
            for e in entities.entries:
                keys = {fold(a) for a in e["aliases"]} - {""}
                if not (keys & folded):
                    continue
                rec = ledger[e["id"]]
                if n not in rec["mentioned"]:
                    rec["mentioned"].append(n)
                # Substantive = explained AND given real room in this paragraph.
                if explained and len(para.split()) > 60 and n not in rec["substantive"]:
                    rec["substantive"].append(n)

    redundant, forward = [], []
    for eid, rec in ledger.items():
        e = entities.by_id.get(eid)
        if not e:
            continue
        subs = sorted(rec["substantive"])
        ments = sorted(rec["mentioned"])
        if len(subs) >= min_chapters:
            redundant.append({"entity": e["canonical"], "id": eid, "type": e["type"],
                              "explained_in": subs, "mentioned_in": ments})
        if subs and ments and ments[0] < subs[0]:
            forward.append({"entity": e["canonical"], "id": eid, "type": e["type"],
                            "first_mentioned": ments[0], "first_explained": subs[0]})
    redundant.sort(key=lambda r: -len(r["explained_in"]))
    forward.sort(key=lambda r: r["first_explained"] - r["first_mentioned"], reverse=True)
    return {"redundant": redundant, "forward_dependency": forward,
            "ledger": {k: {"substantive": sorted(v["substantive"]),
                           "mentioned": sorted(v["mentioned"])} for k, v in ledger.items()}}


def cross_references(chapters):
    """Every 'as we saw' / 'discussed below' with its direction and context."""
    order = [n for n, _, _ in chapters]
    found = []
    for n, _path, text in chapters:
        body = text.split("## Notes")[0]
        for m in _XREF_RE.finditer(body):
            phrase = m.group(0)
            low = phrase.lower()
            start = max(0, m.start() - 110)
            context = " ".join(body[start:m.end() + 110].split())
            direction = ("forward" if any(w in low for w in _FORWARD)
                         else "backward" if any(w in low for w in _BACKWARD)
                         else "explicit" if re.search(r"chapter (\d+)", low) else "unclear")
            target = None
            tm = re.search(r"chapter (\d+)", low)
            if tm:
                target = int(tm.group(1))
            problem = None
            if target is not None:
                if target == n:
                    problem = "refers to its own chapter"
                elif target not in order:
                    problem = f"refers to chapter {target}, which has not been drafted"
            elif direction == "backward" and n == min(order):
                problem = "backward reference in the first chapter"
            elif direction == "forward" and n == max(order):
                problem = "forward reference in the last chapter"
            found.append({"chapter": n, "phrase": phrase, "direction": direction,
                          "target": target, "problem": problem, "context": context})
    return found


def manuscript_contradictions(store, entities):
    """Conflicts between chapters — one of them is simply wrong."""
    from claims import brief_conflicts, find_conflicts
    from doc_understanding import load_all
    conflicts = find_conflicts(store, scope="manuscript", min_sources=1)
    cross = [c for c in conflicts
             if len({ch for s in c["sides"] for ch in s["chapters"]}) > 1]
    return brief_conflicts(cross, load_all(), entities)


def style_exemplars(chapters, n_per=2, min_words=90, max_words=190):
    """Candidate voice anchors: substantial, well-cited, self-contained paragraphs.

    Proposed, not adopted. §5.3 step 4 asks for a HAND-APPROVED set — a machine
    picking its own exemplars would just entrench whatever register it already
    produces, which is the drift this is meant to correct.
    """
    out = []
    for n, _path, text in chapters:
        scored = []
        for para in _paragraphs(text):
            w = len(para.split())
            if not (min_words <= w <= max_words):
                continue
            if para.lstrip().startswith(("#", ">", "-", "|", "*")):
                continue
            cites = len(re.findall(r"\[E\d+\]|\[\^?\d+\]", para))
            if not cites:
                continue
            # Prefer varied sentence length — the cadence the voice spec asks for.
            lens = [len(s.split()) for s in re.split(r"(?<=[.!?])\s+", para) if s.strip()]
            variance = (max(lens) - min(lens)) if len(lens) > 1 else 0
            scored.append((cites + variance / 10.0, para))
        scored.sort(key=lambda t: -t[0])
        for _s, para in scored[:n_per]:
            out.append({"chapter": n, "approved": False, "text": para})
    return out


def write_report(data, path=OUT):
    Path(path).mkdir(parents=True, exist_ok=True)
    (Path(path) / "coherence.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    lines = ["# Cross-chapter coherence report", "",
             "Generated by coherence.py (§5.3). Passes 1-3 are **reports, not repairs** — "
             "a redundancy flagged here may be deliberate reinforcement, and only you can tell.",
             ""]
    con = data.get("contradictions") or []
    lines += [f"## 1. Manuscript contradictions ({len(con)})", ""]
    if con:
        lines.append("Unlike a corpus conflict, these are not matters for historical "
                     "judgement: two chapters of one book assert incompatible things, "
                     "so one is wrong or they need explicit reconciliation in the text.\n")
        for c in con[:40]:
            lines.append(f"- **{c['subject_label']}** — {c['predicate']}")
            for s in c["sides"]:
                lines.append(f"    - `{s['object'][:90]}` — chapters {s['chapters']}")
    else:
        lines.append("None detected.")

    red = (data.get("ledger") or {}).get("redundant") or []
    lines += ["", f"## 2. Redundant explanation ({len(red)})", ""]
    if red:
        lines.append("Entities explained substantively in three or more chapters. "
                     "The reader meets the same introduction repeatedly.\n")
        for r in red[:40]:
            lines.append(f"- **{r['entity']}** ({r['type']}) explained in chapters "
                         f"{r['explained_in']}; mentioned in {r['mentioned_in']}")
    else:
        lines.append("None detected.")

    fwd = (data.get("ledger") or {}).get("forward_dependency") or []
    lines += ["", f"## 3. Forward dependency ({len(fwd)})", ""]
    if fwd:
        lines.append("Used before it is explained — the reader meets the term cold.\n")
        for r in fwd[:40]:
            lines.append(f"- **{r['entity']}** first mentioned ch {r['first_mentioned']}, "
                         f"first explained ch {r['first_explained']}")
    else:
        lines.append("None detected.")

    xr = data.get("xrefs") or []
    bad = [x for x in xr if x["problem"]]
    lines += ["", f"## 4. Cross-references ({len(xr)} found, {len(bad)} problematic)", ""]
    for x in bad[:40]:
        lines.append(f"- ch {x['chapter']}: **{x['problem']}** — \"{x['phrase']}\"")
        lines.append(f"    …{x['context'][:170]}…")
    if not bad:
        lines.append("No unresolvable cross-references.")

    ex = data.get("exemplars") or []
    lines += ["", f"## 5. Style exemplar candidates ({len(ex)})", "",
              "Proposed voice anchors. Set `approved: true` in coherence.json for the ones "
              "that genuinely represent the register you want; only approved passages are "
              "fed to the drafter.", ""]
    for e in ex[:8]:
        lines.append(f"> *(ch {e['chapter']})* {e['text'][:280]}…\n")

    (Path(path) / "coherence.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Cross-chapter coherence checks")
    ap.add_argument("--dir", default="chapter_drafts")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--ledger", action="store_true")
    ap.add_argument("--xrefs", action="store_true")
    ap.add_argument("--contradictions", action="store_true")
    ap.add_argument("--exemplars", action="store_true")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    chapters = load_chapters(args.dir)
    if not chapters:
        print(f"no chapter-NN.md in {args.dir}"); sys.exit(1)
    entities = EntityIndex.load()
    store = KBStore()
    do_all = args.all or not any([args.ledger, args.xrefs, args.contradictions, args.exemplars])

    data = {"chapters": [n for n, _, _ in chapters], "config_hash": CFG.hash()}

    if do_all or args.ledger:
        print("ledger: first substantive treatment of each entity ...", flush=True)
        data["ledger"] = concept_ledger(chapters, entities)
        print(f"  {len(data['ledger']['redundant'])} redundantly explained, "
              f"{len(data['ledger']['forward_dependency'])} used before explained")

    if do_all or args.xrefs:
        print("cross-references ...", flush=True)
        data["xrefs"] = cross_references(chapters)
        bad = [x for x in data["xrefs"] if x["problem"]]
        print(f"  {len(data['xrefs'])} found, {len(bad)} problematic")

    if do_all or args.contradictions:
        print("manuscript contradictions ...", flush=True)
        n_claims = store.db.execute(
            "SELECT COUNT(*) FROM claims WHERE scope='manuscript'").fetchone()[0]
        if not n_claims:
            print("  no manuscript claims yet — run:\n"
                  "    python claims.py --extract-manuscript --dir " + args.dir)
            data["contradictions"] = []
        else:
            data["contradictions"] = manuscript_contradictions(store, entities)
            print(f"  {len(data['contradictions'])} cross-chapter contradiction(s)")

    if do_all or args.exemplars:
        data["exemplars"] = style_exemplars(chapters)
        print(f"style exemplars: {len(data['exemplars'])} candidates (none approved yet)")

    write_report(data, args.out)
    print(f"\n-> {args.out}/coherence.md  and  coherence.json")


if __name__ == "__main__":
    main()
