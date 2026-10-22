"""In-session production (user plan of 15 Oct, "finish Ch 1–3 within the remaining OpenAI credit").
Drafting, revision, fixes, author's pass, copyedit and line edit are done in-session (no API). This tool gives the writers
their inputs and checks for free, and makes the few permitted API calls under a hard cap.

FREE (no API):
  set UDAY_CFG=<cfg>; python -I -X utf8 inhouse.py inputs <sec>          plan entry, through-line, ledger digest, cached evidence, previous section
  set UDAY_CFG=<cfg>; python -I -X utf8 inhouse.py check <sec> [file]    validator + prose checks + ledger check (default file: run/chN/<sec>.md)
  python -I -X utf8 inhouse.py spend                                     new OpenAI spend vs the $12 cap (logged + unlogged orphans)
  python -I -X utf8 inhouse.py dryrun                                    projected cost of every remaining permitted call
PAID (default model gpt-6.1-sol; refuses any call that could pass the cap):
  set UDAY_CFG=<cfg>; inhouse.py judge <sec>        medium   → run/chN/<sec>_judge.json
  set UDAY_CFG=<cfg>; inhouse.py verify <sec>       medium   → run/chN/<sec>_verify.json (proposals only; nothing applied)
  set UDAY_CFG=<cfg>; inhouse.py reverify           low      → run/chN/reverify.json (sentences changed since verification, one call)
  set UDAY_CFG=<cfg>; inhouse.py finalread          medium   → run/chN/finalread.json (independent read of the whole chapter)

Section files: run/chN/<sec>.md is the current working text (IDs and {{note}} blocks). run/chN/<sec>_verified.md is the
snapshot the verifier saw. State: run/inhouse_state.json (section → stage).
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
DR = HERE.parent
RUN = DR / "run"
LOGS = {1: DR / "ch01" / "api_log_v5", 2: DR / "ch02" / "api_log_v3", 3: DR / "ch03" / "api_log_v2"}
CFGS = {1: DR / "ch01" / "cfg_ch01v5.py", 2: DR / "ch02" / "cfg_ch02v3.py", 3: DR / "ch03" / "cfg_ch03v2.py"}
# spend baseline: each log's total when the workers were frozen (13:27:09); everything after counts against the cap
BASELINE = {1: 4.469, 2: 3.762, 3: 2.503}
UNLOGGED = {"edit_1.1": 0.123, "edit_2.1": 0.110, "expand_2.2": 0.806, "edit_3.1_repair": 0.068}   # orphaned at termination: worst case (estimates)
CAP, NOTIFY = 12.00, 9.00
STATE = RUN / "inhouse_state.json"


def log_total(c):
    return sum((json.load(open(f, encoding="utf-8"))["meta"].get("cost_usd") or 0) for f in glob.glob(str(LOGS[c] / "*.json")))


def new_spend():
    by = {c: round(log_total(c) - BASELINE[c], 4) for c in LOGS}
    return {"by_chapter_logged": by, "logged": round(sum(by.values()), 4), "unlogged_worst_case": round(sum(UNLOGGED.values()), 4),
            "total_conservative": round(sum(by.values()) + sum(UNLOGGED.values()), 4), "cap": CAP, "headroom": round(CAP - sum(by.values()) - sum(UNLOGGED.values()), 4)}


def state():
    return json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"sections": {}, "events": []}


def save_state(st):
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=1), encoding="utf-8")


def mark(sec, stage, **kw):
    st = state()
    st["sections"].setdefault(sec, {})[stage] = dict(kw, at=time.strftime("%H:%M:%S"))
    st["spend"] = new_spend()
    save_state(st)
    write_status(st)


def write_status(st):
    sp = st.get("spend") or new_spend()
    lines = [f"# In-session run — {time.strftime('%H:%M:%S')}", "",
             f"- **New OpenAI spend (since the freeze):** ${sp['total_conservative']:.2f} conservative (logged ${sp['logged']:.2f} + worst-case unlogged orphans ${sp['unlogged_worst_case']:.2f}) of the ${CAP:.0f} cap; headroom ${sp['headroom']:.2f}; the last $4 of credit is never touched.",
             f"- Logged new spend by chapter: {sp['by_chapter_logged']}", "", "| Section | Stages done |", "|---|---|"]
    for sec in sorted(st["sections"], key=lambda s: tuple(int(x) for x in s.split("."))):
        done = ", ".join("%s (%s)" % (k, v.get("at", "")) for k, v in st["sections"][sec].items())
        lines.append(f"| {sec} | {done} |")
    (RUN / "status.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- free commands
def _mods():
    sys.path.insert(0, str(HERE))
    from cfg import C
    import validate as va
    import pipeline3 as p3
    import ledger
    import prose_checks as pc
    return C, va, p3, ledger, pc


def sec_file(C, sec):
    return RUN / f"ch{C.CH}" / f"{sec}.md"


def inputs(sec):
    C, va, p3, ledger, pc = _mods()
    _, secs, targets, titles = va.load_outline()
    i = C.SECTIONS.index(sec)
    ev = (RUN / "cache" / f"ch{C.CH}_{sec}_evidence.txt").read_text(encoding="utf-8")
    tl = (re.search(r"\*\*Through-line\.\*\*\s*(.+)", p3.PLAN) or [None, ""])[1]
    prev = sec_file(C, C.SECTIONS[i - 1]).read_text(encoding="utf-8") if i > 0 and sec_file(C, C.SECTIONS[i - 1]).exists() else ""
    if i == 0:
        prev = "(first section of the chapter) OPENING: " + C.OPEN_IN
    print(f"# INPUTS FOR {titles[sec]} " + (f"(target {targets[sec]} words; floor {int(targets[sec] * 0.7)}; aim at the target)\n"
                                            if targets[sec] else "(no length target: use all the unit's evidence; pad nothing)\n"))
    print(f"## Through-line\n{tl}\n\n## Chapter question and arc\n{p3.PLAN_HEAD}\n\n## Section plan\n{secs[sec]}\n")
    if sec == C.SECTIONS[-1]:
        print(f"## Chapter closing\n{C.CLOSE_OUT}\n")
    print(f"## Ledger digest\n{ledger.digest(sec, secs[sec] + ev)}\n\n## Previous section (continue from it; never repeat it)\n{prev}\n\n## Evidence (role, tier, QUOTE; facts only from QUOTE / ENGLISH RENDERING)\n{ev}")


def check(sec, path=None):
    C, va, p3, ledger, pc = _mods()
    _, secs, targets, titles = va.load_outline()
    P = va.load_pack()
    f = Path(path) if path else sec_file(C, sec)
    t = f.read_text(encoding="utf-8")
    rep = p3.check(t, P, sec, targets)
    probs = p3.problems_of(rep) + p3.fidelity_problems(rep)
    led = ledger.check(sec, t)
    pr = pc.report(t, P)
    probs += pr["dynasty_spelling"]          # D1, 16 Oct
    probs = list(dict.fromkeys(probs))
    words = rep["words"].get(sec)
    out = {"section": sec, "words": words, "target": targets[sec], "share": round(words / targets[sec], 2) if words and targets[sec] else None,
           "integrity_ok": rep["integrity_ok"], "score": p3.score_rep(rep), "problems": probs, "ledger": led,
           "style_warnings": pr["style"][:15], "ai_shape_per_1000w": pr["ai_shape_per_1000w"],
           "clean": rep["integrity_ok"] and not probs and not [x for x in led if not x.startswith("figure")]}   # figure flags are review items (noisy)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return out


# ---------------------------------------------------------------- paid commands
EST = {"judge": 0.09, "verify": 0.11, "reverify": 0.05, "finalread": 0.16}


def guard(kind):
    sp = new_spend()
    if sp["total_conservative"] + EST[kind] * 1.5 > CAP:
        sys.exit(f"REFUSED: {kind} could take new spend past the ${CAP:.0f} cap ({sp})")
    return sp


def _run(effort):
    os.environ["UDAY_CALL_TIMEOUT"] = "360"
    os.environ["UDAY_POLL"] = "2"
    C, va, p3, ledger, pc = _mods()
    import run as rn
    R = rn.Run(False)

    class E:
        def __init__(self):
            self.R = R

        def call(self, name, rnd, kind, system, user, out_words, model=None, effort_=None, **kw):
            return R.call(name, rnd, kind, system, user, out_words, model=rn.MODEL, effort=effort)

        def parallel(self, jobs):
            return R.parallel(jobs)

        def __getattr__(self, k):
            return getattr(R, k)
    return C, va, p3, ledger, R, E()


def judge(sec):
    guard("judge")
    C, va, p3, ledger, R, E = _run("medium")
    _, secs, targets, titles = va.load_outline()
    P = va.load_pack()
    t = sec_file(C, sec).read_text(encoding="utf-8")
    i = C.SECTIONS.index(sec)
    prev = sec_file(C, C.SECTIONS[i - 1]).read_text(encoding="utf-8") if i > 0 else C.OPEN_IN
    v = p3.judge(E, f"ih_judge_{sec}", sec, secs, titles, targets, P, {"DRAFT": t}, {"DRAFT": p3.check(t, P, sec, targets)},
                 ledger.digest(sec, secs[sec]) + "\n\n" + prev) or {}
    (RUN / f"ch{C.CH}" / f"{sec}_judge.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
    mark(sec, "judge", total=(v.get("scores", {}).get("DRAFT") or {}).get("total"))
    print(json.dumps(v, ensure_ascii=False, indent=1)[:6000])


def verify(sec):
    guard("verify")
    C, va, p3, ledger, R, E = _run("medium")
    P = va.load_pack()
    f = sec_file(C, sec)
    t = f.read_text(encoding="utf-8")
    import prose_checks as pc
    warn = pc.agent_nouns(t, P)
    tm = pc.testimony_measures(t, P)
    extra = ""
    if warn or tm:
        extra = "CODE WARNINGS (check each):\n" + "\n".join(f"- agent noun '{x['noun']}': {x['sentence']}" for x in warn) + "\n" + \
                "\n".join(f"- testimony as measurement: {x}" for x in tm) + "\n\n"
    _, st, verdicts = p3.verify_sections(t + "\n", P, E, prefix="ih_verify", fix=False, extra_context=extra)
    (RUN / f"ch{C.CH}" / f"{sec}_verified.md").write_text(t, encoding="utf-8")
    flagged = [v for v in verdicts.values() if v["verdict"] not in p3.GOOD]
    out = {"counts": st["verdicts_before"], "flagged": flagged}
    (RUN / f"ch{C.CH}" / f"{sec}_verify.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    mark(sec, "verify", counts=st["verdicts_before"].get(sec), flagged=len(flagged))
    print(json.dumps(out, ensure_ascii=False, indent=1, default=str)[:8000])


def reverify():
    guard("reverify")
    C, va, p3, ledger, R, E = _run("low")
    P = va.load_pack()
    import verify as vf
    rows = []
    for sec in C.SECTIONS:
        snap = RUN / f"ch{C.CH}" / f"{sec}_verified.md"
        if not snap.exists() or not sec_file(C, sec).exists():
            continue
        old = {r["sentence"] for paras in p3.rows_of(snap.read_text(encoding="utf-8"), P).values() for p in paras for r in p["rows"]}
        rows += [r for paras in p3.rows_of(sec_file(C, sec).read_text(encoding="utf-8"), P).values() for p in paras for r in p["rows"] if r["sentence"] not in old]
    if not rows:
        print("nothing changed since verification")
        return
    iids = sorted({i for r in rows for i in r["ids"]})
    u = (p3.CONVENTIONS + "EVIDENCE ITEMS:\n" + "\n\n".join(vf.item_text(P[i]) for i in iids)
         + "\n\nTHE SECTION, PARAGRAPH BY PARAGRAPH:\n--- PARAGRAPH (sentences revised after verification; judge each in its own right) ---\nITEMS:\n"
         + "\n".join(f"{r['sid']} [{r['kind']}; evidence: {', '.join(r['ids']) if r['kind'] != 'INT' else 'paragraph facts'}]: {r['sentence']}" for r in rows))
    out = E.call(f"ih_reverify_ch{C.CH}", 6, "reverify", p3.VERIFY_SYS, u, 60 * len(rows))
    import run as rn
    j = rn.parse_json(out) or {}
    res = {"rows": len(rows), "results": j.get("results", []), "sentences": {r["sid"]: r["sentence"] for r in rows}}
    (RUN / f"ch{C.CH}" / "reverify.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    bad = [x for x in res["results"] if str(x.get("verdict", "")).upper() not in p3.GOOD]
    mark(f"{C.CH}.0", "reverify", rows=len(rows), flagged=len(bad))
    print(json.dumps({"rows": len(rows), "flagged": bad}, ensure_ascii=False, indent=1)[:6000])


FINAL_SYS = """You are an independent reader of one chapter of a serious narrative history of Udaypur (Vidisha district, Madhya Pradesh), checking it before it goes to the publisher. The working text carries evidence IDs in brackets and {{note: …}} blocks; the cited evidence items are supplied.
Report ONLY real problems, each tied to an exact phrase: (1) a claim the cited items do not support, or a measurement/date supported only by testimony (Jagta Hua Kasba) or tradition; (2) inference presented as fact, a proposal hardened, a tradition told as event, a praśasti claim told as plain event, or two distinct objects merged; (3) uncertainty out of proportion (inflated or erased); (4) repetition of a fact already given in the chapter, a closing sentence that restates its paragraph, or a run of same-shaped sentences; (5) prose that a careful editor would mark: unclear, ungrammatical, awkward, source-led ("[source] says"), method narration, or encyclopedic digression; (6) continuity: a term glossed twice, a full name re-introduced, a contradiction between sections.
Return ONLY JSON: {"problems": [{"section": "N.N", "kind": "1–6", "phrase": "exact words ≤ 25", "why": "…", "fix": "…"}], "overall": "two sentences"}"""


def finalread():
    guard("finalread")
    C, va, p3, ledger, R, E = _run("medium")
    P = va.load_pack()
    import verify as vf
    ch = "\n\n".join(sec_file(C, s).read_text(encoding="utf-8").strip() for s in C.SECTIONS)
    ids = sorted({i for i in va.ids_in(ch) if i in P})
    u = p3.STYLE_BLOCK + f"CHAPTER PLAN:\n{p3.PLAN_HEAD}\n\nEVIDENCE ITEMS:\n" + "\n\n".join(vf.item_text(P[i]) for i in ids) + f"\n\nCHAPTER:\n{ch}"
    out = E.call(f"ih_finalread_ch{C.CH}", 9, "verify", FINAL_SYS, u, 1500)
    import run as rn
    j = rn.parse_json(out) or {}
    (RUN / f"ch{C.CH}" / "finalread.json").write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
    mark(f"{C.CH}.0", "finalread", problems=len(j.get("problems", [])))
    print(json.dumps(j, ensure_ascii=False, indent=1)[:8000])


def dryrun():
    st = state()
    n_judge = n_verify = 0
    for c in (1, 2, 3):
        for i in range(1, 6):
            s = f"{c}.{i}"
            d = st["sections"].get(s, {})
            n_judge += "judge" not in d and not (c in (1, 2, 3) and i == 1 and (RUN / f"ch{c}" / f"{s}_judge.json").exists())
            n_verify += "verify" not in d
    cost = n_judge * EST["judge"] + n_verify * EST["verify"] + 3 * EST["reverify"] + 3 * EST["finalread"]
    sp = new_spend()
    print(json.dumps({"remaining_calls": {"judge": n_judge, "verify": n_verify, "reverify": 3, "finalread": 3},
                      "projected_new_cost_usd": round(cost, 2), "spent_so_far_conservative": sp["total_conservative"],
                      "projected_total_new_spend": round(cost + sp["total_conservative"], 2), "cap": CAP, "notify_threshold": NOTIFY}, indent=1))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cmd = sys.argv[1]
    if cmd == "inputs":
        inputs(sys.argv[2])
    elif cmd == "check":
        check(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    elif cmd == "spend":
        print(json.dumps(new_spend(), indent=1))
    elif cmd == "dryrun":
        dryrun()
    elif cmd == "judge":
        judge(sys.argv[2])
    elif cmd == "verify":
        verify(sys.argv[2])
    elif cmd == "reverify":
        reverify()
    elif cmd == "finalread":
        finalread()
