"""Final citation-support verification + fixes on ch02_draft_v1.md (after the hand-spliced 2.2), then footnotes/docx.

  python -u -I "drafting/ch02/final_verify.py"
"""
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import pipeline_ch02 as pc  # noqa: E402
import pipeline_v3 as pv  # noqa: E402

D = HERE
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    t0 = time.time()
    _, secs, targets, _ = pc.load_outline()
    P = {i["id"]: i for i in json.loads(pc.PACK.read_text(encoding="utf-8"))}
    shutil.copy(D / "ch02_verification.json", D / "ch02_verification_expansion.json")
    text = pc.OUT.read_text(encoding="utf-8")
    (D / "ch02_final_preverify.md").write_text(text, encoding="utf-8")
    R = pv.Run(False)
    before = R.spent
    chapter, vstate = pc.verify(text, P, R, targets)
    rep = pc.check(chapter, P, None, targets)
    st = {"spent_this_step": round(R.spent - before, 4), "spent_total_usd": round(R.spent, 4),
          "verdicts_before": vstate["verdicts_before"], "verdicts_after": vstate["verdicts_after"],
          "final_validation": pc.summ(rep), "final_validation_detail": rep, "seconds": round(time.time() - t0), "calls": R.calls}
    pc.OUT.write_text(chapter, encoding="utf-8")
    (D / "ch02_final_verify_state.json").write_text(json.dumps(st, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    for cmd in (["footnote.py", pc.OUT.name], ["make_docx.py", pc.OUT.stem + "_footnoted.md", pc.OUT.stem + ".docx"]):
        subprocess.run([sys.executable, "-I", str(D / cmd[0])] + cmd[1:])
    print(json.dumps({k: st[k] for k in ("spent_this_step", "spent_total_usd", "verdicts_before", "verdicts_after", "final_validation")}, ensure_ascii=False, indent=1))
