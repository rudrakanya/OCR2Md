"""One entry point for the Chapters 1–3 run (user brief, 2026-10-15).

  python -u -I orchestrator.py preflight     one short call per (model, effort) used + a priority-tier probe → run/preflight.json
  python -u -I orchestrator.py --dry-run     task graph, critical path, projected wall clock (measured latencies) and cost
  python -u -I orchestrator.py run          ledger build (3 in parallel) + merge, then one chapter_flow process per chapter
                                            (4 concurrent calls each: 12 in all), live status, time rules, gate hold

Every _pipe module binds one chapter's cfg at import, so chapters run as separate processes; this parent schedules them,
aggregates drafting/run/state.json and status.md every 10 s, re-projects the finish and applies the time rules
(drafting/run/overrides.json): 1 copyedit → low, 2 judge → medium, 3 author → medium, 4 drafting → medium (sections not
yet started). Verification, copyedit, the author's pass and the gate are never skipped.
Clock: T0 = the moment the editor started this phase (UDAY_T0, epoch seconds), so projections are against the user's 30 minutes.
"""
from __future__ import annotations

import json
import os
import re
import statistics as stt
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
DR = HERE.parent
RUN = DR / "run"
CFGS = {1: DR / "ch01" / "cfg_ch01v5.py", 2: DR / "ch02" / "cfg_ch02v3.py", 3: DR / "ch03" / "cfg_ch03v2.py"}
BUDGETS = {1: 9.00, 2: 8.25, 3: 8.00}
TARGET_MIN, HARD_MIN = 40, 50          # run 2 (user, 15 Oct)
GATE_MIN, LINE_EDIT_MIN, OUTPUT_MIN = 3.0, 5.0, 1.0
PY = sys.executable
ENV = dict(os.environ, UDAY_MAX_PAR="4", UDAY_CALL_TIMEOUT="360", UDAY_POLL="2", PYTHONIOENCODING="utf-8")   # run 2: 6-minute timeout
T0 = float(os.getenv("UDAY_T0", "0")) or time.time()

# measured medians (seconds) from the project's API logs (all chapters, 2026-10-12…14; 8 s polling), stage@effort
HIST = {"draft@high": 200, "expand@high": 120,      # draft@high = flagship (run 2; est. from tokens, no history)
        "draft@high_sol": 114, "draft@medium": 60, "judge@high": 137, "judge@medium": 55, "edit@medium": 36, "edit@high": 46,
        "verify@medium": 43, "fix@medium": 15, "reverify@medium": 10, "author@high": 330, "author@medium": 200,
        "postverify@medium": 40, "copyedit@medium": 45, "copyedit@low": 25}
STEPS = [("copyedit", "low"), ("judge", "medium"), ("author", "medium")]      # run 2: drafting never reduced


def lat(stage, eff, pre):
    base = HIST.get(f"{stage}@{eff}", 60)
    adj = pre.get("overhead_delta_s", 0) if pre else 0          # today's measured overhead vs the logs' typical overhead
    return max(5, base + adj)


def projection(status, ovr, pre):
    """minutes from T0 to final delivery, given each chapter's task status"""
    eff = lambda k, d: ovr.get(k, d)
    chap_gate = []
    for ch, st in status.items():
        tasks = st.get("tasks", {}) if st else {}
        secs = [f"{ch}.{i}" for i in range(1, 6)]
        t = time.time()
        rem_drafts = [s for s in secs if tasks.get(f"draft_{s}", {}).get("status") != "done"]
        run_d = tasks.get(f"draft_{rem_drafts[0]}", {}) if rem_drafts else {}
        d = sum(lat("draft", "high", pre) + 0.5 * lat("expand", "high", pre) for _ in rem_drafts)
        if run_d.get("status") == "running":
            d -= min(lat("draft", eff("draft", "high"), pre), t - run_d.get("start", t))
        last = secs[-1]
        tail = 0
        for k, e in (("judge", eff("judge", "high")), ("edit", "medium"), ("verify", "medium"), ("fix", "medium"), ("reverify", "medium")):
            key = k if k in ("judge", "edit", "verify") else "verify"
            if tasks.get(f"{key}_{last}", {}).get("status") != "done":
                tail += lat(k, e, pre)
        chap_gate.append(t + d + tail)
    gate_at = max(chap_gate) if chap_gate else time.time()
    if any((st or {}).get("tasks", {}).get("gate", {}).get("status") == "done" for st in status.values()):
        gate_at = time.time()
    else:
        gate_at += GATE_MIN * 60
    after = lat("author", eff("author", "high"), pre) + lat("postverify", "medium", pre) + lat("copyedit", eff("copyedit", "medium"), pre)
    return (gate_at + after + (LINE_EDIT_MIN + OUTPUT_MIN) * 60 - T0) / 60


def read_status():
    out = {}
    for ch in CFGS:
        f = RUN / f"status_ch{ch}.json"
        out[ch] = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    return out


def write_status(status, proj, ovr, procs=None, note=""):
    el = (time.time() - T0) / 60
    lines = [f"# Run status — {time.strftime('%H:%M:%S')}", "",
             f"- **Elapsed since start of phase:** {el:.1f} min · **projected finish:** {proj:.1f} min (target {TARGET_MIN}, hard {HARD_MIN})",
             f"- **Effort overrides (time rules):** {ovr or 'none'}", ""]
    if note:
        lines += [f"- {note}", ""]
    lines += ["| Chapter | Spent this run | Total in log | Budget | Done | Running | Waiting |", "|---|---|---|---|---|---|---|"]
    allt = {}
    for ch, st in status.items():
        tasks = st.get("tasks", {}) if st else {}
        allt[ch] = tasks
        done = [k for k, v in tasks.items() if v.get("status") == "done"]
        runn = [k for k, v in tasks.items() if v.get("status") == "running"]
        wait = [k for k, v in tasks.items() if v.get("status") == "waiting"]
        lines.append(f"| {ch} | ${st.get('spent_this_run', 0):.2f} | ${st.get('spent', 0):.2f} | ${BUDGETS[ch]:.2f} | {len(done)} | {', '.join(runn) or '—'} | {', '.join(wait) or '—'} |")
    if procs:
        lines += ["", "Processes: " + ", ".join(f"ch{c} {'running' if p.poll() is None else f'exit {p.returncode}'}" for c, p in procs.items())]
    lines += ["", "## Task timings (s)", ""]
    for ch, tasks in allt.items():
        row = [f"{k} {v['end'] - v['start']:.0f}" for k, v in tasks.items() if v.get("start") and v.get("end")]
        lines.append(f"- ch{ch}: " + (", ".join(row) or "—"))
    (RUN / "status.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (RUN / "state.json").write_text(json.dumps({"t0": T0, "elapsed_min": round(el, 2), "projected_min": round(proj, 2), "overrides": ovr,
                                                "chapters": status}, ensure_ascii=False, indent=1, default=str), encoding="utf-8")


def time_rules(status, pre, ovr):
    applied = dict(ovr)
    for k, e in STEPS:
        if projection(status, applied, pre) <= TARGET_MIN:
            break
        applied[k] = e
    return applied


def preflight():
    os.environ["UDAY_CFG"] = str(CFGS[1])
    sys.path.insert(0, str(HERE))
    import run as rn
    R = rn.Run(False)
    res = {}
    import concurrent.futures as cf

    def one(model, eff):
        t = time.time()
        R.call(f"preflight_{model[:9]}_{eff}", 0, "fix", "Reply with the single word OK.", "OK?", 3, model=model, effort=eff)
        return time.time() - t
    jobs = {(m, e): None for m, e in ((rn.MODEL, "low"), (rn.MODEL, "medium"), (rn.MODEL, "high"), (rn.FLAGSHIP, "medium"), (rn.FLAGSHIP, "high"))}
    with cf.ThreadPoolExecutor(5) as ex:
        futs = {ex.submit(one, m, e): (m, e) for (m, e) in jobs}
        for f in futs:
            res[f"{futs[f][0]}@{futs[f][1]}"] = round(f.result(), 1)
    tier = {}
    try:                                                   # faster processing tier: availability and latency only
        t = time.time()
        r = R.c.responses.create(model=rn.MODEL, input="Reply with the single word OK.", reasoning={"effort": "low"}, service_tier="priority", max_output_tokens=200)
        tier = {"priority": {"available": True, "seconds": round(time.time() - t, 1), "service_tier_returned": getattr(r, "service_tier", None)}}
    except Exception as e:  # noqa: BLE001
        tier = {"priority": {"available": False, "error": f"{type(e).__name__}: {str(e)[:160]}"}}
    # the logs' overhead for a near-empty call at 8 s polling was ~10–12 s; today's (2 s polling) shows the delta
    base = res.get(f"{rn.MODEL}@low", 10)
    out = {"measured_s": res, "tier": tier, "overhead_delta_s": round(min(0, base - 11), 1), "spent": round(R.spent - R.prior, 4)}
    (RUN / "preflight.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(json.dumps(out, indent=1))


def dry():
    pre = json.loads((RUN / "preflight.json").read_text(encoding="utf-8")) if (RUN / "preflight.json").exists() else {}
    cost = {}
    for ch, cfg in CFGS.items():
        r = subprocess.run([PY, "-u", "-I", str(HERE / "chapter_flow.py"), "--dry-run"], env=dict(ENV, UDAY_CFG=str(cfg)),
                           capture_output=True, text=True, encoding="utf-8")
        m = re.search(r'(?s)\{\s*"chapter".*\}\s*\Z', r.stdout.strip()) if r.returncode == 0 else None
        j = json.loads(m.group(0)) if m else {"error": (r.stderr or r.stdout)[-600:]}
        cost[ch] = j
    empty = {ch: {} for ch in CFGS}
    p0 = projection(empty, {}, pre)
    ovr = time_rules(empty, pre, {})
    p1 = projection(empty, ovr, pre)
    graph = ("per chapter: draft_N.1 → draft_N.2 → … → draft_N.5 (sequential chain)\n"
             "  each draft_N.s → judge → edit (+repair) → verify → fix → re-verify (runs as soon as its draft lands)\n"
             "  all verify_* (all chapters) → GATE (editor reads 1.1 P1, 1.5 P1, 2.1 P5, 2.3 P2) → author (flagship) → post-verify → copyedit ×5 → finish\n"
             "  then: editor line edit (3 subagents + joins) → ledger update ×3 → build_outputs")
    crit = "critical path: the slowest chapter's draft chain (5 drafts) + its last section's judge/edit/verify/fix/reverify → gate → author → post-verify → copyedit → line edit → outputs"
    print(graph + "\n" + crit)
    print(json.dumps({"projected_cost_by_chapter": {c: v.get("projected_cost_usd", v) for c, v in cost.items()},
                      "projected_finish_min_from_T0_no_rules": round(p0, 1), "time_rules_applied": ovr,
                      "projected_finish_min_from_T0_with_rules": round(p1, 1), "elapsed_at_launch_min": round((time.time() - T0) / 60, 1),
                      "latencies_used_s": {k: lat(*k.split("@"), pre) for k in HIST}}, indent=1))
    return ovr


def run():
    RUN.mkdir(parents=True, exist_ok=True)
    pre = json.loads((RUN / "preflight.json").read_text(encoding="utf-8")) if (RUN / "preflight.json").exists() else {}
    ovr = json.loads((RUN / "overrides.json").read_text(encoding="utf-8")) if (RUN / "overrides.json").exists() else {}
    if not (DR / "editorial" / "book_ledger.json").exists():
        ps = [subprocess.Popen([PY, "-u", "-I", str(HERE / "ledger.py"), "build"], env=dict(ENV, UDAY_CFG=str(c)),
                               stdout=open(RUN / f"ledger_ch{ch}.log", "w", encoding="utf-8"), stderr=subprocess.STDOUT) for ch, c in CFGS.items()]
        for p in ps:
            p.wait()
        subprocess.run([PY, "-I", str(HERE / "ledger.py"), "merge"], env=ENV)
    procs = {ch: subprocess.Popen([PY, "-u", "-I", str(HERE / "chapter_flow.py")], env=dict(ENV, UDAY_CFG=str(c)),
                                  stdout=open(RUN / f"ch{ch}.log", "a", encoding="utf-8"), stderr=subprocess.STDOUT) for ch, c in CFGS.items()}
    while any(p.poll() is None for p in procs.values()):
        st = read_status()
        new = time_rules(st, pre, ovr)
        if new != ovr:
            ovr = new
            (RUN / "overrides.json").write_text(json.dumps(ovr), encoding="utf-8")
        proj = projection(st, ovr, pre)
        note = "GATE: waiting for the editor (drafting/run/gate.json)" if any(v.get("tasks", {}).get("gate", {}).get("status") == "waiting" for v in st.values() if v) else ""
        write_status(st, proj, ovr, procs, note)
        time.sleep(10)
    st = read_status()
    write_status(st, projection(st, ovr, pre), ovr, procs, "all chapter flows finished")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    RUN.mkdir(parents=True, exist_ok=True)
    cmd = sys.argv[1] if len(sys.argv) > 1 else "--dry-run"
    if cmd == "preflight":
        preflight()
    elif cmd == "--dry-run":
        o = dry()
        if "--write-overrides" in sys.argv:
            (RUN / "overrides.json").write_text(json.dumps(o), encoding="utf-8")
    elif cmd == "run":
        run()
