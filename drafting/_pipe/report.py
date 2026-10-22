"""Chapter report for the shared toolkit (active chapter from UDAY_CFG).

  python -I drafting/_pipe/report.py issues.json      # issues.json: ["issue 1", "issue 2", "issue 3"]

Sections: documents; open issues; outline changes (cfg REPORT_OUTLINE_NOTES); KB additions; judge scores (with BASE);
source-subject ratio per section (baseline → chosen candidate → final); verifier verdicts; word counts; evidence
balance by book (draft citations); incomplete bibliography entries; spend and time per stage.
"""
import collections
import glob
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cfg import C  # noqa: E402
import validate as va  # noqa: E402
import footnote as fn  # noqa: E402

D, STEM = C.D, C.OUT.stem


def j(p):
    p = Path(p)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def main(issues):
    st = j(D / f"{STEM}_state.json")
    vr = j(D / f"{STEM}_verification.json")
    kb = j(D / f"kb_state_{C.VERSION}.json")
    todo = j(D / f"{STEM}_footnoted.bibliography_todo.json") or []
    P = va.load_pack()
    draft = C.OUT.read_text(encoding="utf-8")
    _, secs, targets, titles = va.load_outline()
    final = va.check(draft, P, None, targets)
    used = va.ids_in(draft)
    L = [f"# Chapter {C.CH} {C.VERSION} report — {C.TITLE}\n", "## Documents\n"]
    L += [f"- `{C.OUT.relative_to(C.D.parent.parent)}` — working draft with evidence IDs",
          f"- `{C.OUT.with_name(STEM + '_footnoted.md').relative_to(C.D.parent.parent)}` — Chicago notes-bibliography (17th ed.); IDs in HTML comments",
          f"- `{(C.D / C.DOCX_NAME).relative_to(C.D.parent.parent)}` — Word, real footnotes (A4, Georgia 11 pt, 1.25 spacing; Heading 1; notes 9 pt with grey evidence IDs; bibliography on its own page, hanging indent; page numbers)",
          f"- `{STEM}_report.md` (this report), `{C.OUTLINE.name}`, `{C.PACK.name}`, `{STEM}_spotcheck.md`, `{STEM}_state.json`, `{STEM}_verification.json`\n"]
    L.append("## The 3 most important open issues\n")
    L += [f"{k}. {x}" for k, x in enumerate(issues, 1)] + [""]
    L.append("## Outline\n")
    L.append(getattr(C, "REPORT_OUTLINE_NOTES", "") + "\n")
    # KB
    L.append("## Knowledge-base additions\n")
    if kb:
        prior = {x["id"] for x in json.loads(C.KB_IN.read_text(encoding="utf-8"))} if getattr(C, "KB_IN", None) and C.KB_IN.exists() else set()
        mine = [i for i in P.values() if "kb-new" in i["flags"] and i["id"] not in prior]
        L.append(f"- {kb.get('B_queries')} gap queries and {kb.get('C_queries')} contradiction queries (hybrid dense+BM25 with per-book sweeps over the read-only "
                 f"snapshot of `udaypur_corpus_openai_large`); {kb.get('new_items')} new items verified verbatim (quotes sliced by code from the stored chunk, "
                 f"checked against the source Markdown); KB spend ${kb.get('spent_usd')}, {kb.get('seconds')} s.")
        L.append(f"- Cited in the final text: {len([i for i in mine if i['id'] in used])} of {len(mine)}.\n")
        L.append("| Item | Step | Section | Page | What it adds | Cited |\n|---|---|---|---|---|---|")
        for i in mine:
            L.append(f"| {i['id']} | {i.get('kb_step')} | {i.get('kb_section') or '—'} | {i['page'][:24]} | {i['note'][:130].replace('|', '/')} | {'yes' if i['id'] in used else 'no'} |")
        L.append("")
    # judges
    L.append("## Judge scores\n")
    L.append("A, B = new candidates" + ("; BASE = the same section of the previous draft (`" + C.BASELINE.name + "`). A new candidate replaces BASE only if it scores higher on subject focus without losing on fidelity." if getattr(C, "BASELINE", None) else "") + "\n")
    for s in C.SECTIONS:
        sec = st.get("sections", {}).get(s, {})
        jd = sec.get("judge", {})
        L.append(f"### {titles.get(s, s)} — chosen: {sec.get('chosen', jd.get('best'))}\n")
        L.append("| Entry | Fidelity | Coverage | Subject focus | Prose | Register | Transition | Total | Source-led (code) |\n|---|---|---|---|---|---|---|---|---|")
        for lab, sc in (jd.get("scores") or {}).items():
            sl = sec.get("entries", {}).get(lab, {}).get("check", {}).get("source_led", {})
            L.append(f"| {lab} | " + " | ".join(str(sc.get(k)) for k in ("fidelity", "coverage", "subject_focus", "prose", "register", "transition", "total"))
                     + f" | {', '.join(sl.values()) if sl else '—'} |")
        if jd.get("baseline_rule"):
            L.append(f"\nBaseline rule: {jd['baseline_rule']}")
        L.append(f"\n*{jd.get('rationale', '')}*\n")
        ed = sec.get("edit")
        if ed:
            L.append(f"Edit: {'kept' if ed.get('kept') else 'reverted'}.\n")
    # source-subject ratio
    L.append("## Source-subject ratio (sentences whose subject or main clause is a source/author)\n")
    L.append("A section fails at > 10% flagged sentences or > 1 flagged sentence in any paragraph.\n")
    base = va.subject_report(C.BASELINE.read_text(encoding="utf-8")) if getattr(C, "BASELINE", None) and C.BASELINE.exists() else {}
    hdr = "| Section |" + (" Previous draft |" if base else "") + " Chosen candidate (before edits) | Final | Final pass? |"
    L.append(hdr + "\n|" + "---|" * (hdr.count("|") - 1))
    for s in C.SECTIONS:
        sec = st.get("sections", {}).get(s, {})
        ch = sec.get("chosen")
        bef = sec.get("entries", {}).get(ch, {}).get("check", {}).get("source_led", {}).get(s, "—")
        f = final["subject"].get(s, {})
        row = f"| {s} |" + (f" {base[s]['flagged']}/{base[s]['sentences']} ({base[s]['ratio']:.0%}) |" if base and s in base else "")
        row += f" {bef} | {f.get('flagged')}/{f.get('sentences')} ({f.get('ratio', 0):.0%}), worst paragraph {f.get('worst_paragraph')} | {'yes' if f.get('pass') else 'NO'} |"
        L.append(row)
    rest = [(s, r) for s, rows in final["subject_detail"].items() for r in rows]
    if rest:
        L.append("\nRemaining flagged sentences:")
        L += [f"- {s}: {r['sentence'][:200]}" for s, r in rest]
    L.append("")
    # verification
    L.append("## Citation-support verification (before → after targeted fixes)\n")
    L.append("| Section | Before | After |\n|---|---|---|")
    for s in C.SECTIONS:
        L.append(f"| {s} | {vr.get('verdicts_before', {}).get(s)} | {vr.get('verdicts_after', {}).get(s)} |")
    L.append(f"\nChanged sentences: {len(vr.get('changes', []))}; rejected or reverted fixes: {len(vr.get('open', []))}; still not SUPPORTED: {len(vr.get('remaining', []))}.")
    for v in vr.get("remaining", []):
        L.append(f"- **{v['sid']}** ({v['verdict']}): {v['sentence'][:220]}")
    rules = st.get("rule_checks_final", [])
    L.append(f"\nCode rule checks on the final text: {[(r['rule'], r.get('sid') or r.get('sec')) for r in rules] or 'none failing'}\n")
    # words
    L.append("## Word counts (IDs excluded)\n\n| Section | Target | Words | Within 90–110% |\n|---|---|---|---|")
    for s in C.SECTIONS:
        n = final["words"].get(s)
        L.append(f"| {titles.get(s, s)} | {targets[s]} | {n} | {'yes' if n and targets[s] * 0.9 <= n <= targets[s] * 1.1 else 'NO'} |")
    tot = final["words"]["total"]
    L.append(f"| **Total** | {C.TOTAL_TARGET:,} | **{tot:,}** | {'yes' if C.WMIN <= tot <= C.WMAX else 'NO'} ({C.WMIN:,}–{C.WMAX:,}) |\n")
    # evidence balance
    L.append("## Evidence balance by book (citations in the final draft)\n")
    for s, part in va.split_sections(draft).items():
        c = collections.Counter(P[i]["book_code"] for i in va.ids_in(part) if i in P)
        n = sum(c.values())
        L.append(f"- **{s}** ({n} citations): " + ", ".join(f"{k} {v} ({v / n:.0%})" for k, v in c.most_common()))
    c = collections.Counter(P[i]["book_code"] for i in used if i in P)
    L.append(f"- **Chapter**: " + ", ".join(f"{k} {v}" for k, v in c.most_common()) + "\n")
    pc = collections.Counter(i["book_code"] for i in P.values())
    L.append("Evidence pack by book: " + ", ".join(f"{k} {v}" for k, v in pc.most_common()) + "\n")
    # final code validation
    L.append("## Final code validation\n")
    L.append("```\n" + json.dumps(va.summary(final), ensure_ascii=False, indent=1) + "\n```\n")
    # bibliography
    L.append("## Incomplete bibliography entries (to-do for the editor)\n")
    for t in todo:
        L.append(f"- **{t['book']}** (`{t['code']}`): missing {', '.join(t['missing']) or '—'}" + (f"; confirm: {t['confirm']}" if t.get("confirm") else "") + f" — source: {t['source']}")
    L.append("")
    # spend and time
    spend = collections.Counter()
    for f in sorted(glob.glob(str(C.LOG / "*.json"))):
        m = json.load(open(f, encoding="utf-8"))["meta"]
        spend[m["stage"]] += m.get("cost_usd") or 0
    L.append(f"## Spend and time\n\n| Stage | USD |\n|---|---|")
    for k, v in spend.items():
        L.append(f"| {k} | {v:.3f} |")
    L.append(f"| **total** | **{sum(spend.values()):.2f}** of ${C.BUDGET:.2f} |\n")
    L.append("| Stage | Seconds |\n|---|---|")
    if kb:
        L.append(f"| knowledge base | {kb.get('seconds')} |")
    for k, v in st.get("stage_seconds", {}).items():
        L.append(f"| {k} | {v} |")
    L.append(f"| **pipeline wall clock** | **{st.get('wall_clock_seconds')}** |\n")
    L.append(f"Stitch: {'kept' if st.get('stitch', {}).get('kept') else 'not kept'}; polish: {'kept' if st.get('polish', {}).get('kept') else 'not kept'}"
             f"; length guard: {json.dumps({k: v for k, v in st.get('length_guard', {}).items() if k != 'short'}, ensure_ascii=False)[:400]}; budget decisions: {st.get('decisions') or 'none'}\n")
    out = D / f"{STEM}_report.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("wrote", out.name)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")) if len(sys.argv) > 1 else ["(fill in)"])
