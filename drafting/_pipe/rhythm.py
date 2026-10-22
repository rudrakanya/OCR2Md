"""Final rhythm-and-sense line edit (active chapter from UDAY_CFG), then citation-support verification, footnotes, docx.

Why: under the subject rule, models made "Udaypur" open most sentences, hid attributions in passives ("dated … by
Patil", "in Ganguly's hypothesis") and left stray sentences in the wrong paragraph. One medium-effort call per
section, in parallel; kept only if citation integrity holds, source-led and monotony counts do not rise, the section
stays within 90–110% of target, editorial conventions survive, and the code score is no worse. Then pipeline.verify.

  set UDAY_CFG=...; python -u -I drafting/_pipe/rhythm.py [--dry-run]
"""
import json
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

SYS = """You are the line editor of one section of a university-press history chapter about Udaypur (Vidisha district, Madhya Pradesh). The section already keeps the place as its subject; your job is rhythm and sense.
DO:
- Vary sentence openings: no more than one sentence per paragraph may open with "Udaypur"/"Udaypur's". Keep the PLACE as the subject by naming its parts and people instead — the temple, the hill, the village, its lanes, the tank, the inscription, the town's founders, residents — or open with a time or place phrase, or a pronoun where the reference is clear.
- Remove hidden attributions where the source's identity does not matter: "dated … by Patil", "in Ganguly's hypothesis", ", while Hardy treats …", "in Tiwari's reading/account" → state the fact or the range about the object; the source stays in the bracketed IDs. Keep a named source only where identity matters (competing scholarly datings, tradition vs inscription, an eyewitness) — at most one per paragraph, briefly.
- Merge or cut sentences that restate the previous one; move a sentence that sits in the wrong paragraph to where it belongs, or cut it.
- Keep paragraphs 120–200 words with a topic sentence about the place.
STRICT: no new facts, dates, names or numbers; every factual sentence keeps its bracketed evidence IDs (you may merge two sentences and their IDs); quotations unchanged; the heading line unchanged; keep "Vijay Manohar Tiwari" (if present) and "1979" (if present); never "the author", never "according to [title]"; length within the given range.
Return the full revised section in Markdown and nothing else."""


def ts():
    return time.strftime("%H:%M:%S")


def main(dry):
    t0 = time.time()
    _, secs, targets, titles = va.load_outline()
    P = va.load_pack()
    text = C.OUT.read_text(encoding="utf-8")
    if not dry:
        shutil.copy(C.OUT, C.OUT.with_name(C.OUT.stem + "_prerhythm.md"))
    parts = va.split_sections(text)
    R = rn.Run(dry)
    s0 = R.spent

    def job(sec):
        def f():
            rep = pl.check(parts[sec], P, sec, targets)
            n = va.words(parts[sec])
            lo, hi = max(int(targets[sec] * 0.95), n), int(max(targets[sec] * 1.08, n * 1.04))
            probs = rep.get("monotony", []) + [f"source-led: {r['sentence']}" for rows in rep["subject_detail"].values() for r in rows]
            ids = [i for i in dict.fromkeys(va.ids_in(parts[sec])) if i in P]
            u = (f"WORD RANGE: {lo}–{hi} words (IDs excluded). The current section is {n} words: DO NOT SHORTEN IT — "
                 f"an output under {lo} words is rejected. Rewrite openings and attributions in place; merge only true repetitions.\n\nCODE FINDINGS TO FIX:\n" + "\n".join(f"- {p}" for p in probs)
                 + f"\n\nCHAPTER BRIEF (for reference):\n{C.CHAPTER_BRIEF}\n\nSUBJECT RULES:\n{pl.SUBJECT_RULES}\n\n"
                 + "EVIDENCE CITED IN THIS SECTION (for sense only; add nothing):\n" + "\n\n".join(pl.fmt_item(P[i], False) for i in ids)
                 + f"\n\n=== SECTION ===\n{parts[sec].strip()}")
            return R.call(f"rhythm_{sec}", 8, "edit", SYS, u, n + 80)
        return f

    only = [a for a in sys.argv[1:] if a in C.SECTIONS] or C.SECTIONS
    res = R.parallel([(s, job(s)) for s in only])
    state = {"sections": {}, "round": "targeted" if only != C.SECTIONS else "all"}
    new = dict(parts)
    for s in only:
        out = res.get(s)
        b = pl.check(parts[s], P, s, targets)
        rec = {"before": pl.summ(b)}
        if isinstance(out, str) and out.strip():
            cand = out.strip() + "\n"
            a = pl.check(cand, P, s, targets)
            n = a["words"].get(s, 0)
            keep = (a["integrity_ok"] and cand.startswith("## " + s) and targets[s] * 0.9 <= n <= targets[s] * 1.1
                    and pl.n_source_led(a) <= pl.n_source_led(b) and len(a["monotony"]) <= len(b["monotony"])
                    and pl._guards_ok(parts[s], cand) and pl.score_rep(a) <= pl.score_rep(b))
            rec.update(after=pl.summ(a), kept=keep)
            if not dry:
                (pl.CAND / f"{s}_rhythm.md").write_text(cand, encoding="utf-8")
            if keep:
                new[s] = cand
        else:
            rec.update(kept=False, reason=repr(out)[:200])
        state["sections"][s] = rec
        print(f"[{ts()}] {s}: kept={rec.get('kept')} source-led {rec['before']['source_led'].get(s)} -> {rec.get('after', {}).get('source_led', {}).get(s)}; "
              f"monotony {rec['before']['monotony']} -> {rec.get('after', {}).get('monotony')}; words {rec.get('after', {}).get('words', {}).get(s)}", flush=True)
    chapter = "\n\n".join(new[s].strip() for s in C.SECTIONS) + "\n"
    tot = va.words(chapter)
    if not (C.WMIN <= tot <= C.WMAX):
        state["total_note"] = f"total {tot} outside range; reverting the longest/shortest changed sections"
        for s in sorted([s for s in C.SECTIONS if new[s] != parts[s]], key=lambda s: -abs(va.words(new[s]) - va.words(parts[s]))):
            new[s] = parts[s]
            chapter = "\n\n".join(new[x].strip() for x in C.SECTIONS) + "\n"
            if C.WMIN <= va.words(chapter) <= C.WMAX:
                break
    if dry:
        print(json.dumps({"projected_usd": round(R.spent - s0, 3)}))
        return
    changed = [s for s in C.SECTIONS if new[s] != parts[s]]
    vpath = C.D / f"{C.OUT.stem}_verification.json"
    prev = json.loads(vpath.read_text(encoding="utf-8")) if vpath.exists() else {}
    if only != C.SECTIONS and prev:
        # verify only the sections changed in this targeted round; merge with the earlier full verification
        if changed:
            sub = "\n\n".join(new[s].strip() for s in changed) + "\n"
            sub, vs = pl.verify(sub, P, R, targets)
            for s, part in va.split_sections(sub).items():
                new[s] = part.strip() + "\n"
            for k in ("verdicts_before", "verdicts_after"):
                prev[k] = {**prev.get(k, {}), **vs[k]}
            for k in ("changes", "open", "remaining"):
                prev[k] = [x for x in prev.get(k, []) if x.get("sid", "").split("-")[0] not in changed] + vs.get(k, [])
            prev["note"] = f"sections {', '.join(changed)} re-verified after a targeted rhythm round; others from the previous full verification"
        chapter = "\n\n".join(new[s].strip() for s in C.SECTIONS) + "\n"
        prev["rule_failures_after"] = __import__("verify").rule_checks(chapter, P, __import__("verify").cited_sentences(chapter))
        vpath.write_text(json.dumps(prev, ensure_ascii=False, indent=1), encoding="utf-8")
        vstate = prev
        bad = {v["sentence"] for v in prev.get("remaining", [])}
        vmap = {f"{s}-{n}": {"sentence": r["sentence"], "verdict": "NOT SUPPORTED" if r["sentence"] in bad else "SUPPORTED"}
                for s, rows in __import__("verify").cited_sentences(chapter).items() for n, r in enumerate(rows)}
        pl.write_spotcheck(chapter, P, vmap, prev.get("remaining", []))
    else:
        chapter, vstate = pl.verify(chapter, P, R, targets)
    rep = pl.check(chapter, P, None, targets)
    import verify as vf
    state.update(verdicts_before=vstate["verdicts_before"], verdicts_after=vstate["verdicts_after"], final_validation=pl.summ(rep),
                 rule_checks_final=vf.rule_checks(chapter, P, vf.cited_sentences(chapter)),
                 spent_this_step=round(R.spent - s0, 4), spent_total=round(R.spent, 4), seconds=round(time.time() - t0), calls=R.calls)
    C.OUT.write_text(chapter, encoding="utf-8")
    (C.D / f"{C.OUT.stem}_rhythm{'_targeted' if only != C.SECTIONS else ''}_state.json").write_text(json.dumps(state, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    # keep the pipeline state's final fields in step with the delivered text (the report reads them)
    stp = C.D / f"{C.OUT.stem}_state.json"
    st = json.loads(stp.read_text(encoding="utf-8"))
    st["final_validation"], st["rule_checks_final"], st["rhythm"] = state["final_validation"], state["rule_checks_final"], {k: v.get("kept") for k, v in state["sections"].items()}
    st.setdefault("stage_seconds", {})["8_rhythm_and_reverify"] = state["seconds"]
    stp.write_text(json.dumps(st, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    for cmd in (["footnote.py", str(C.OUT)], ["make_docx.py"]):
        subprocess.run([sys.executable, "-I", str(HERE / cmd[0])] + cmd[1:])
    print(json.dumps({"final": state["final_validation"], "spent_total": state["spent_total"]}, ensure_ascii=False), flush=True)
    print(f"[{ts()}] RHYTHM PASS FINISHED (chapter {C.CH})", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main("--dry-run" in sys.argv)
