"""Round 4b (user decision, 2026-10-14): the production edit pass and the production verifier's fix round, applied to the
four round-4 host sections, with the corrected checks (inference rule, "Muslim", malformed notes), the 70–120% band and
the people-as-subject limit. Then one fresh judge reading (4B against R4) for comparison with the editor's re-score.

Inputs: drafting/editorial/round4/<sec>_draft.md and <sec>_judge.json (the round-4 judge's improvements, INT-TRIVIAL list,
missed Points and rule artefacts are exactly what the production edit pass consumes).

  set UDAY_CFG=<cfg>; python -u -I drafting/_pipe/calib4b.py <sec> [<sec> …] [--dry-run]
Output: drafting/editorial/round4b/<sec>_{draft.md,edit.json,verify.json,judge.json,footnoted.md}, metrics_chN.json
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cfg import C  # noqa: E402
import run as rn  # noqa: E402
import validate as va  # noqa: E402
import pipeline as p1  # noqa: E402
import pipeline3 as p3  # noqa: E402
import footnote as fn  # noqa: E402
import metrics  # noqa: E402
import calib4  # noqa: E402

IND = C.D.parent / "editorial" / "round4"
OUTD = C.D.parent / "editorial" / "round4b"


def main(secs_wanted, dry):
    OUTD.mkdir(parents=True, exist_ok=True)
    _, secs, targets, titles = va.load_outline()
    P = va.load_pack()
    old = va.split_sections(C.BASELINE.read_text(encoding="utf-8"))
    R = rn.Run(dry)
    s0 = R.spent

    def job_for(sec):
        def job():
            r4 = (IND / f"{sec}_draft.md").read_text(encoding="utf-8").strip()
            v = json.loads((IND / f"{sec}_judge.json").read_text(encoding="utf-8")) or {}
            best = "R4"
            so_far, _ = calib4.stand_in(sec)
            frep = p3.check(r4, P, sec, targets)
            base = old[C.BASELINE_MAP[sec]].strip()
            # 3 edit pass: the production prompt, verbatim in structure
            eu = (p3.STYLE_BLOCK + f"WRITER BRIEF:\n{p3.WRITER_SYS}\n\nTHE CHAPTER SO FAR:\n{so_far or '(none)'}\n\nSECTION PLAN:\n{secs[sec]}\n\n"
                  f"WORD RANGE: {int(targets[sec] * 0.7)}–{int(targets[sec] * 1.2)} (never pad)\n\n"
                  "IMPROVEMENTS TO APPLY:\n" + "\n".join(f"- {x}" for x in v.get("improvements", []))
                  + ("\nTRANSPLANTS:\n" + "\n".join(f"- {x}" for x in v.get("transplants", [])) if v.get("transplants") else "")
                  + "\nPOINTS FOUND MISSING OR ALTERED:\n" + "\n".join(f"- {x}" for x in (v.get("points_missed") or {}).get(best, []))
                  + "\nINT-TRIVIAL SENTENCES TO CUT:\n" + "\n".join(f"- {x}" for x in (v.get("int_trivial") or {}).get(best, []))
                  + "\nAUTOMATED-CHECK PROBLEMS TO FIX:\n" + "\n".join(f"- {x}" for x in p3.problems_of(frep)[:30])
                  + "\n\nEVIDENCE:\n" + p3.evidence_block(secs[sec], P, [x for x in va.ids_in(va.strip_notes(r4)) if x in P], False)[0]
                  + f"\n\n=== SECTION TO REVISE ===\n{r4}\n\n=== ENTRY BASE (transplant source only) ===\n{base}")
            out = R.call(f"r4b_edit_{sec}", 3, "edit", p3.EDIT_SYS, eu, targets[sec] + 200)
            text, edit = r4, {"kept": False, "reason": "call failed"}
            if isinstance(out, str) and out.strip():
                if not dry:
                    (OUTD / f"{sec}_edit_raw.md").write_text(out.strip() + "\n", encoding="utf-8")
                keep, txt, edit = p3.edit_gate(R, f"r4b_edit_{sec}", out.strip(), frep, sec, P, targets, r4, dry)
                if keep:
                    text = txt
            # 6 verification + one round of fixes + re-verify (production)
            text2, vst, _ = p3.verify_sections(text + "\n", P, R, prefix="r4b_verify", fix=not dry)
            text2 = text2.strip()
            # fresh judge reading, 4B against R4
            jr = p3.judge(R, f"r4b_judge_{sec}", sec, secs, titles, targets, P, {"R4B": text2, "R4": r4},
                          {"R4B": p3.check(text2, P, sec, targets), "R4": frep}, so_far)
            return {"text": text2, "edit": edit, "verify": vst, "judge": jr, "final_check": p1.summ(p3.check(text2, P, sec, targets)),
                    "final_problems": p3.problems_of(p3.check(text2, P, sec, targets))}
        return job
    res = R.parallel([(s, job_for(s)) for s in secs_wanted])
    met = {}
    for sec in secs_wanted:
        r = res.get(sec)
        if not isinstance(r, dict) or dry:
            continue
        (OUTD / f"{sec}_draft.md").write_text(r["text"] + "\n", encoding="utf-8")
        for k in ("edit", "verify", "judge"):
            (OUTD / f"{sec}_{k}.json").write_text(json.dumps(r[k], ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        (OUTD / f"{sec}_checks.json").write_text(json.dumps({"summary": r["final_check"], "problems": r["final_problems"]}, ensure_ascii=False, indent=1), encoding="utf-8")
        fn.convert_consolidated(OUTD / f"{sec}_draft.md", OUTD / f"{sec}_footnoted.md", P)
        met[sec] = metrics.section_stats(r["text"], consolidated=True)
    if met:
        (OUTD / f"metrics_ch{C.CH}.json").write_text(json.dumps(met, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"round 4b {secs_wanted}: spent ${R.spent - s0:.3f} (dry={dry}); calls {len(R.calls)}", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args, "--dry-run" in sys.argv)
