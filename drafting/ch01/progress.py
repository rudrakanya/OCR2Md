"""One-line progress report: spend, calls done / expected, current stage, projected final cost and finish time.
  python -I "drafting/ch01/progress.py" [--candidates 2]
"""
import glob
import json
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch01"))
SECTIONS = ["1.1", "1.2", "1.3", "1.4", "1.5"]


def main():
    n_c = int(sys.argv[sys.argv.index("--candidates") + 1]) if "--candidates" in sys.argv else 2
    calls = [json.load(open(f, encoding="utf-8"))["meta"] for f in sorted(glob.glob(str(D / "api_log" / "*.json")))]
    spent = sum(c.get("cost_usd") or 0 for c in calls)
    log = (D / "pipeline_run.log").read_text(encoding="utf-8") if (D / "pipeline_run.log").exists() else ""
    adapt = re.findall(r"ADAPT: .*", log)
    if any("1 candidate" in a for a in adapt):
        n_c = 1
    names = {c["name"] for c in calls}
    # expected calls: per section candidates+judge+edit+summary, then stitch + ~2 revisions + polish
    exp = []
    for s in SECTIONS:
        exp += [f"cand_{s}_{L}" for L in "AB"[:n_c]] + [f"judge_{s}", f"edit_{s}", f"summary_{s}"]
    exp += ["stitch", "revise_1", "revise_2", "polish"]
    done = len(calls)
    remaining = [e for e in exp if e not in names and not (e.startswith("revise") and any(n.startswith("revise") for n in names))]
    inflight = re.findall(r"\] calling (\S+)", log)
    finished = re.findall(r"\] done (\S+)", log)
    current = [x for x in inflight if x not in finished]
    def avg(kind, cost=True, fb=0.2):
        xs = [c["cost_usd" if cost else "seconds"] for c in calls if c.get("kind") == kind and c.get("cost_usd")]
        return sum(xs) / len(xs) if xs else fb
    kind_of = lambda e: ("candidate" if e.startswith("cand") else e.split("_")[0])
    fb_cost = {"candidate": 0.27, "judge": 0.25, "edit": 0.12, "summary": 0.03, "stitch": 0.20, "revise": 0.10, "polish": 0.20}
    fb_secs = {"candidate": 700, "judge": 600, "edit": 300, "summary": 60, "stitch": 400, "revise": 300, "polish": 400}
    rem_cost = sum(avg(kind_of(e), True, fb_cost[kind_of(e)]) for e in remaining)
    # time: candidates of a section run in parallel -> count one candidate slot per section
    secs_left = 0.0
    seen_cand_sec = set()
    for e in remaining:
        k = kind_of(e)
        if k == "candidate":
            s = e.split("_")[1]
            if s in seen_cand_sec:
                continue
            seen_cand_sec.add(s)
        secs_left += avg(k, False, fb_secs[k])
    eta = datetime.now() + timedelta(seconds=secs_left)
    stage = current[-1] if current else ("finished" if "PIPELINE FINISHED" in log else "between calls")
    print(json.dumps({"time": time.strftime("%H:%M"), "spent_usd": round(spent, 3), "calls_done": done,
                      "calls_expected_total": done + len(remaining), "current": stage,
                      "projected_final_usd": round(spent + rem_cost, 2), "projected_finish": eta.strftime("%H:%M"),
                      "adaptations": adapt, "finished": "PIPELINE FINISHED" in log}, ensure_ascii=False))


if __name__ == "__main__":
    main()
