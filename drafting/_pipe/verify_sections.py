"""Re-verify selected sections of the working draft (after hand edits), merge with the existing verification record,
rewrite the spot-check, rebuild footnotes and docx.

  set UDAY_CFG=...; python -u -I drafting/_pipe/verify_sections.py 3.2 3.4
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from cfg import C  # noqa: E402
import run as rn  # noqa: E402
import validate as va  # noqa: E402
import pipeline as pl  # noqa: E402
import verify as vf  # noqa: E402

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    secs = [a for a in sys.argv[1:] if a in C.SECTIONS]
    _, _, targets, _ = va.load_outline()
    P = va.load_pack()
    parts = va.split_sections(C.OUT.read_text(encoding="utf-8"))
    vpath = C.D / f"{C.OUT.stem}_verification.json"
    prev = json.loads(vpath.read_text(encoding="utf-8"))
    R = rn.Run(False)
    s0 = R.spent
    sub = "\n\n".join(parts[s].strip() for s in secs) + "\n"
    sub, vs = pl.verify(sub, P, R, targets)
    for s, part in va.split_sections(sub).items():
        parts[s] = part.strip() + "\n"
    chapter = "\n\n".join(parts[s].strip() for s in C.SECTIONS) + "\n"
    for k in ("verdicts_before", "verdicts_after"):
        prev[k] = {**prev.get(k, {}), **vs[k]}
    for k in ("changes", "open", "remaining"):
        prev[k] = [x for x in prev.get(k, []) if x.get("sid", "").split("-")[0] not in secs] + vs.get(k, [])
    prev["note"] = (prev.get("note", "") + f" Sections {', '.join(secs)} re-verified after hand edits.").strip()
    prev["rule_failures_after"] = vf.rule_checks(chapter, P, vf.cited_sentences(chapter))
    vpath.write_text(json.dumps(prev, ensure_ascii=False, indent=1), encoding="utf-8")
    C.OUT.write_text(chapter, encoding="utf-8")
    bad = {v["sentence"] for v in prev["remaining"]}
    vmap = {f"{s}-{n}": {"sentence": r["sentence"], "verdict": "NOT SUPPORTED" if r["sentence"] in bad else "SUPPORTED"}
            for s, rows in vf.cited_sentences(chapter).items() for n, r in enumerate(rows)}
    pl.write_spotcheck(chapter, P, vmap, prev["remaining"])
    rep = pl.check(chapter, P, None, targets)
    stp = C.D / f"{C.OUT.stem}_state.json"
    st = json.loads(stp.read_text(encoding="utf-8"))
    st["final_validation"], st["rule_checks_final"] = pl.summ(rep), prev["rule_failures_after"]
    stp.write_text(json.dumps(st, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    for cmd in (["footnote.py", str(C.OUT)], ["make_docx.py"]):
        subprocess.run([sys.executable, "-I", str(HERE / cmd[0])] + cmd[1:])
    print(json.dumps({"spent_step": round(R.spent - s0, 4), "spent_total": round(R.spent, 4), "verdicts_after": prev["verdicts_after"],
                      "remaining": [(v["sid"], v["verdict"]) for v in prev["remaining"]], "final": pl.summ(rep),
                      "rules": [(r["rule"], r.get("sid") or r.get("sec")) for r in prev["rule_failures_after"]]}, ensure_ascii=False))
