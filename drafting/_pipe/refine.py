"""Dedupe-and-enrich pass (active chapter from UDAY_CFG), then citation-support verification, footnotes, docx.

Why: the length guard and earlier passes padded sections with restatements (Chapter 3 v1: the same fact up to five
times in a paragraph). Per section, in parallel (effort medium): the code's near-duplicate pairs, the verifier's
remaining non-SUPPORTED sentences with their suggested fixes, and the section's UNUSED evidence (outline items not
cited + cfg EXTRA_POOL + cfg REFINE_EXTRA) go to one call: cut every restatement, fix the flagged sentences, and
replace the cut words with new facts from the unused evidence (hard word floor). Kept only if integrity holds,
duplicates fall, source-led and monotony counts do not rise, the section is within 90–110% of target and the code
score is no worse. Then pipeline.verify on the whole chapter.

  set UDAY_CFG=...; python -u -I drafting/_pipe/refine.py [sections…]
"""
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from cfg import C  # noqa: E402
import run as rn  # noqa: E402
import validate as va  # noqa: E402
import pipeline as pl  # noqa: E402
import verify as vf  # noqa: E402

SYS = """You revise one section of a university-press history chapter about Udaypur (Vidisha district, Madhya Pradesh).
1. CUT every sentence that restates a fact already given in the section (the code's duplicate pairs are listed — keep the better sentence of each pair, merging its IDs if needed). No paragraph may say the same thing twice.
2. FIX each flagged sentence as its suggested fix says (narrow the claim to the cited evidence, or cut it). Never claim Udaypur's proximity to a place unless a cited item states it.
3. ADD new facts from the UNUSED EVIDENCE to replace the words cut: each new sentence carries its bracketed ID; put it in the paragraph where it belongs; keep the place (the country around Udaypur, its towns, roads, shrines, rulers) as the grammatical subject; tie material back to Udaypur only where the evidence allows.
STRICT: only facts in the supplied items' QUOTE or ENGLISH RENDERING; quotations verbatim (at most 2 in the section); no meta-commentary ("must be distinguished", "provides a narrower basis", "this section"); no superlatives in the narrator's voice; never "the author" or "according to [title]"; source names in the text only where identity matters, at most one per paragraph; Vijay Manohar Tiwari is named in full only in the chapter's first section — elsewhere "Tiwari"; keep the heading line exactly; paragraphs 120–200 words with topic sentences.
LENGTH IS A HARD REQUIREMENT: between MINW and MAXW words (IDs excluded).
Return the full section in Markdown and nothing else."""


def ts():
    return time.strftime("%H:%M:%S")


def main():
    t0 = time.time()
    outline, secs, targets, titles = va.load_outline()
    P = va.load_pack()
    text = C.OUT.read_text(encoding="utf-8")
    shutil.copy(C.OUT, C.OUT.with_name(C.OUT.stem + "_prerefine.md"))
    parts = va.split_sections(text)
    vprev = json.loads((C.D / f"{C.OUT.stem}_verification.json").read_text(encoding="utf-8"))
    remaining = {}
    for v in vprev.get("remaining", []):
        remaining.setdefault(v["sid"].split("-")[0], []).append(v)
    only = [a for a in sys.argv[1:] if a in C.SECTIONS] or C.SECTIONS
    R = rn.Run(False)
    s0 = R.spent

    def job(sec):
        def f():
            rep = pl.check(parts[sec], P, sec, targets)
            used = set(va.ids_in(parts[sec]))
            pool = [i for i in dict.fromkeys(pl.section_ids(secs[sec], P) + getattr(C, "EXTRA_POOL", {}).get(sec, [])
                                              + getattr(C, "REFINE_EXTRA", {}).get(sec, [])) if i in P and i not in used]
            lo, hi = int(targets[sec] * 0.95), int(targets[sec] * 1.07)
            first = sec == C.SECTIONS[0]
            u = (f"WORD RANGE: {lo}–{hi} words (IDs excluded); the section is now {va.words(parts[sec])} words.\n\n"
                 "DUPLICATE PAIRS (code):\n" + ("\n".join(f"- {d}" for d in rep["duplicates"]) or "- none found by code; still remove any restatement you see") +
                 "\n\nFLAGGED SENTENCES (fact-checker):\n" + ("\n".join(f"- {v['sentence']}\n  verdict: {v['verdict']}; fix: {v.get('fix', '')}" for v in remaining.get(sec, [])) or "- none") +
                 ("\n\nOTHER CODE FINDINGS:\n" + "\n".join(f"- {p}" for p in rep["monotony"] + [f"source-led: {r['sentence']}" for rows in rep["subject_detail"].values() for r in rows]) if rep["monotony"] or rep["subject_fail"] else "") +
                 f"\n\nTIWARI: {'name him in full (Vijay Manohar Tiwari) at his first mention in this section' if first else 'write Tiwari, never the full name'}.\n\n"
                 f"SECTION PLAN:\n{secs[sec]}\n\nCHAPTER BRIEF:\n{C.CHAPTER_BRIEF}\n\nSUBJECT RULES:\n{pl.SUBJECT_RULES}\n\n"
                 "UNUSED EVIDENCE (add from these):\n" + "\n\n".join(pl.fmt_item(P[i], False) for i in pool) +
                 "\n\nEVIDENCE ALREADY CITED:\n" + "\n\n".join(pl.fmt_item(P[i], False) for i in used if i in P) +
                 f"\n\n=== SECTION ===\n{parts[sec].strip()}")
            return R.call(f"refine_{sec}", 9, "edit", SYS.replace("MINW", str(lo)).replace("MAXW", str(hi)), u, hi + 80)
        return f

    res = R.parallel([(s, job(s)) for s in only])
    state = {"sections": {}}
    new = dict(parts)
    for s in only:
        out = res.get(s)
        b = pl.check(parts[s], P, s, targets)
        rec = {"before": pl.summ(b)}
        if isinstance(out, str) and out.strip():
            cand = out.strip() + "\n"
            (pl.CAND / f"{s}_refine.md").write_text(cand, encoding="utf-8")
            a = pl.check(cand, P, s, targets)
            n = a["words"].get(s, 0)
            keep = (a["integrity_ok"] and cand.startswith("## " + s) and targets[s] * 0.9 <= n <= targets[s] * 1.1
                    and len(a["duplicates"]) < max(1, len(b["duplicates"])) + (0 if b["duplicates"] else 1)
                    and pl.n_source_led(a) <= pl.n_source_led(b) and len(a["monotony"]) <= len(b["monotony"])
                    and pl.score_rep(a) <= pl.score_rep(b) + 3 and not re.search(r"[ऀ-ॿ]", va.BRACKET.sub("", cand)))
            rec.update(after=pl.summ(a), kept=keep, problems=pl.problems_of(a)[:10])
            if keep:
                new[s] = cand
        else:
            rec.update(kept=False, reason=repr(out)[:200])
        state["sections"][s] = rec
        print(f"[{ts()}] {s}: kept={rec.get('kept')} dup {rec['before']['duplicates']} -> {rec.get('after', {}).get('duplicates')}; "
              f"words {rec['before']['words'].get(s)} -> {rec.get('after', {}).get('words', {}).get(s)}; problems {rec.get('problems')}", flush=True)
    chapter = "\n\n".join(new[s].strip() for s in C.SECTIONS) + "\n"
    chapter, vstate = pl.verify(chapter, P, R, targets)
    rep = pl.check(chapter, P, None, targets)
    state.update(verdicts_before=vstate["verdicts_before"], verdicts_after=vstate["verdicts_after"], final_validation=pl.summ(rep),
                 rule_checks_final=vf.rule_checks(chapter, P, vf.cited_sentences(chapter)),
                 spent_this_step=round(R.spent - s0, 4), spent_total=round(R.spent, 4), seconds=round(time.time() - t0), calls=R.calls)
    C.OUT.write_text(chapter, encoding="utf-8")
    (C.D / f"{C.OUT.stem}_refine_state.json").write_text(json.dumps(state, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    stp = C.D / f"{C.OUT.stem}_state.json"
    st = json.loads(stp.read_text(encoding="utf-8"))
    st["final_validation"], st["rule_checks_final"] = state["final_validation"], state["rule_checks_final"]
    st["refine"] = {k: v.get("kept") for k, v in state["sections"].items()}
    st.setdefault("stage_seconds", {})["9_refine_and_reverify"] = state["seconds"]
    stp.write_text(json.dumps(st, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    for cmd in (["footnote.py", str(C.OUT)], ["make_docx.py"]):
        subprocess.run([sys.executable, "-I", str(HERE / cmd[0])] + cmd[1:])
    print(json.dumps({"final": state["final_validation"], "rules": [(r["rule"], r.get("sid") or r.get("sec")) for r in state["rule_checks_final"]],
                      "spent_total": state["spent_total"]}, ensure_ascii=False), flush=True)
    print(f"[{ts()}] REFINE FINISHED (chapter {C.CH})", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
