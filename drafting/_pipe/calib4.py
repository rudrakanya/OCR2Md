"""Round-4 calibration (editor-in-chief audit §10, approved 2026-10-14): the four calibration paragraphs written INSIDE their
host sections by the production writer (pipeline3, sequential mode), then code checks (one repair pass only if a fidelity
check fails), the production judge (round 4 against the previous draft's section) and the production verifier (no fixes:
the point is to see what it flags).

Host sections: 1.1 (1.1 P1), 1.5 (old 1.3 P2 → 1.5 P1), 2.1 (old 2.1 P5 → 2.1 P5), 2.3 (old 2.3 P2 → 2.3 P2).
"Chapter so far" stand-ins (the sections before them are not yet written in v5/v3):
  1.1 none · 1.5 v3's 1.5 (closest to new 1.4) · 2.1 the last paragraph of Chapter 1 v3 · 2.3 v1's 2.3 (closest to new 2.2)

  set UDAY_CFG=<cfg>; python -u -I drafting/_pipe/calib4.py <sec> [<sec> …] [--dry-run]
Output: drafting/editorial/round4/<sec>_{draft,checks,judge,verify}.*
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cfg import C  # noqa: E402
import run as rn  # noqa: E402
import validate as va  # noqa: E402
import pipeline as p1  # noqa: E402
import pipeline3 as p3  # noqa: E402

OUTD = C.D.parent / "editorial" / "round4"
REPAIR = """Revise this section to fix ONLY the listed fidelity problems (uncited claims, unsupported names or numbers, non-verbatim quotations, narrowed ranges). Keep its argument, voice, paragraphing and length. Add no facts; cite each name and number with an item that contains it, or remove it.
Return the full section in Markdown and nothing else."""


def stand_in(sec):
    if C.CH == 1 and sec == "1.5":
        v3 = va.split_sections((C.D / "ch01_draft_v3.md").read_text(encoding="utf-8"))
        return v3["1.5"].strip(), "THE CHAPTER SO FAR (stand-in: the previous draft's section on the praśasti, dates and legends, which the new 1.4 will replace; continue from it)"
    if C.CH == 2 and sec == "2.1":
        t = (C.D.parent / "ch01" / "ch01_draft_v3.md").read_text(encoding="utf-8")
        last = [p for p in va.paragraphs(t) if p.strip()][-1]
        return last.strip(), "END OF CHAPTER 1 (stand-in: the previous draft's last paragraph; this section opens Chapter 2)"
    if C.CH == 2 and sec == "2.3":
        v1 = va.split_sections((C.D / "ch02_draft_v1.md").read_text(encoding="utf-8"))
        return v1["2.3"].strip(), "THE CHAPTER SO FAR (stand-in: the previous draft's monsoon section, closest to the new 2.2; continue from it)"
    return "", "THE CHAPTER SO FAR"


def main(secs_wanted, dry):
    OUTD.mkdir(parents=True, exist_ok=True)
    _, secs, targets, titles = va.load_outline()
    P = va.load_pack()
    old = va.split_sections(C.BASELINE.read_text(encoding="utf-8"))
    R = rn.Run(dry)
    s0 = R.spent
    drafts, reps, so = {}, {}, {}

    def wjob(sec):
        def job():
            so_far, label = stand_in(sec)
            so[sec] = so_far
            u, _ = p3.writer_prompt(sec, secs, titles, targets, P, so_far, label)
            return R.call(f"r4_cand_{sec}", 1, "candidate", p3.WRITER_SYS, u, targets[sec] + 400)
        return job
    res = R.parallel([(s, wjob(s)) for s in secs_wanted])
    for sec in secs_wanted:
        txt = (res.get(sec) or "").strip() if isinstance(res.get(sec), str) else ""
        if dry:
            txt = f"## {titles[sec]}\n\nx [{p3.roles(secs[sec]) and list(p3.roles(secs[sec]))[0]}]."
        rep = p3.check(txt, P, sec, targets)
        probs = p3.fidelity_problems(rep)
        repaired = None
        if probs and not dry:
            ev = p3.evidence_block(secs[sec], P, [x for x in va.ids_in(va.strip_notes(txt)) if x in P], False)[0]
            fixed = (R.call(f"r4_repair_{sec}", 1, "edit", REPAIR, "PROBLEMS:\n" + "\n".join(f"- {x}" for x in probs)
                            + f"\n\nEVIDENCE:\n{ev}\n\n=== SECTION ===\n{txt}", targets[sec] + 300) or "").strip()
            r2 = p3.check(fixed, P, sec, targets) if fixed else None
            if fixed and r2["integrity_ok"] and len(p3.fidelity_problems(r2)) < len(probs) and fixed.startswith("## " + sec):
                repaired = {"before": probs, "after": p3.fidelity_problems(r2)}
                txt, rep = fixed, r2
            else:
                repaired = {"before": probs, "after": "repair not kept"}
        drafts[sec], reps[sec] = txt, rep
        if not dry:
            (OUTD / f"{sec}_draft.md").write_text(txt + "\n", encoding="utf-8")
            (OUTD / f"{sec}_checks.json").write_text(json.dumps({"summary": p1.summ(rep), "problems": p3.problems_of(rep), "repair": repaired,
                                                                 "subject_detail": rep.get("subject_detail"), "monotony": rep.get("monotony")},
                                                                ensure_ascii=False, indent=1), encoding="utf-8")

    def jjob(sec):
        def job():
            base = re.sub(r"^## [^\n]*", f"## {titles[sec]}", old[C.BASELINE_MAP[sec]].strip(), count=1)
            entries = {"R4": drafts[sec], "BASE": base}
            erep = {"R4": reps[sec], "BASE": p3.check(base, P, sec, targets)}
            return p3.judge(R, f"r4_judge_{sec}", sec, secs, titles, targets, P, entries, erep, so.get(sec, ""))
        return job

    def vjob(sec):
        def job():
            _, st, verdicts = p3.verify_sections(drafts[sec] + "\n", P, R, prefix="r4_verify", fix=False)
            return {"counts": st["verdicts_before"], "flagged": st["flagged_before"]}
        return job
    res2 = R.parallel([(("j", s), jjob(s)) for s in secs_wanted] + [(("v", s), vjob(s)) for s in secs_wanted])
    for (k, sec), r in res2.items():
        if not dry:
            (OUTD / f"{sec}_{'judge' if k == 'j' else 'verify'}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(f"round 4 {secs_wanted}: spent ${R.spent - s0:.3f} (dry={dry}); calls {len(R.calls)}", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args, "--dry-run" in sys.argv)
