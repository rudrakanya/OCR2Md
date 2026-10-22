"""Verify only section 2.2 (hand-spliced after expansion 2) with the convention-aware checker; splice back; rebuild notes/docx.

  python -u -I "drafting/ch02/verify_22.py"
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import pipeline_ch02 as pc  # noqa: E402
import pipeline_v3 as pv  # noqa: E402
import validate as va  # noqa: E402

D = HERE
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    _, secs, targets, _ = pc.load_outline()
    P = {i["id"]: i for i in json.loads(pc.PACK.read_text(encoding="utf-8"))}
    t = pc.OUT.read_text(encoding="utf-8")
    t = t.replace("the district Gazetteer of 1979 records generally unsatisfactory", "the district Gazetteer records generally unsatisfactory", 1)
    parts = va.split_sections(t)
    full_ver = json.loads((D / "ch02_verification.json").read_text(encoding="utf-8"))
    (D / "ch02_verification_fullchapter.json").write_text(json.dumps(full_ver, ensure_ascii=False, indent=1), encoding="utf-8")
    R = pv.Run(False)
    s0 = R.spent
    new22, vst = pc.verify(parts["2.2"], P, R, targets)
    parts["2.2"] = new22.strip() + "\n"
    chapter = "\n\n".join(parts[s].strip() for s in pc.SECTIONS) + "\n"
    pc.OUT.write_text(chapter, encoding="utf-8")
    # combine: full-chapter verdicts for 2.1, 2.3–2.5 + this run for 2.2
    vst22 = json.loads((D / "ch02_verification.json").read_text(encoding="utf-8"))
    comb = {"note": "2.1 and 2.3–2.5: final full-chapter verification (expand2_ch02.py); 2.2: re-verified alone after the hand-spliced expansion (verify_22.py).",
            "verdicts_before": {**full_ver["verdicts_before"], "2.2": vst22["verdicts_before"].get("2.2")},
            "verdicts_after": {**full_ver["verdicts_after"], "2.2": vst22["verdicts_after"].get("2.2")},
            "changes": [c for c in full_ver["changes"] if not c["sid"].startswith("2.2")] + vst22["changes"],
            "open": [o for o in full_ver["open"] if not o["sid"].startswith("2.2")] + vst22["open"],
            "remaining": [x for x in full_ver["remaining"] if not x["sid"].startswith("2.2")] + vst22["remaining"],
            "rule_failures_before": vst22.get("rule_failures_before"), "rule_failures_after": vst22.get("rule_failures_after")}
    (D / "ch02_verification.json").write_text(json.dumps(comb, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"spent_this_step": round(R.spent - s0, 4), "spent_total": round(R.spent, 4), "2.2": comb["verdicts_after"]["2.2"],
                      "open": vst22["open"], "remaining": [(x["sid"], x["verdict"]) for x in vst22["remaining"]]}, ensure_ascii=False, indent=1))
