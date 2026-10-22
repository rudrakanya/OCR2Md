"""One chapter's task graph (user brief, 2026-10-15). Launched by orchestrator.py, one process per chapter (cfg binds at import).

Per section, a task starts the moment its inputs exist:
  draft_<s>   (needs draft_<s-1>: its full text + ledger digest; the first section takes the previous chapter's PLANNED closing)
  judge_<s>   (needs draft_<s>)           code checks + judge (DRAFT vs BASE)
  edit_<s>    (needs judge_<s>)           edit pass, with the targeted repair before any revert (pipeline3.edit_gate)
  verify_<s>  (needs edit_<s>)            verify → fix → re-verify (pipeline3.verify_sections)
Then, per chapter:
  gate        (needs every verify_<s>)    waits for drafting/run/gate.json {"status": "pass"} (the editor's in-line gate)
  author      (needs gate)                flagship, whole chapter; kept only if no worse and every guard holds
  postverify  (needs author)              targeted verification of sentences the author's pass changed (flags go to the line edit)
  copyedit_<s>(needs postverify)          section by section against the style sheet; kept only if no worse
  finish      (needs every copyedit)      working draft written to cfg OUT

State: drafting/run/state_ch<N>.json after every task (resume: finished tasks are skipped). Status: drafting/run/status_ch<N>.json.
Effort overrides: drafting/run/overrides.json (written by the orchestrator's time rules), read before every call.

  set UDAY_CFG=<cfg>; python -u -I chapter_flow.py [--dry-run]
"""
from __future__ import annotations

import concurrent.futures as cf
import json
import os
import re
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from cfg import C  # noqa: E402
import run as rn  # noqa: E402
import validate as va  # noqa: E402
import pipeline as p1  # noqa: E402
import pipeline3 as p3  # noqa: E402
import ledger  # noqa: E402

RUN = HERE.parent / "run"
CACHE = RUN / "cache"
SEC_DIR = RUN / f"ch{C.CH}"
STATE = RUN / f"state_ch{C.CH}.json"
STATUS = RUN / f"status_ch{C.CH}.json"
GATE = RUN / "gate.json"
OVR = RUN / "overrides.json"
SEM = threading.Semaphore(int(os.getenv("UDAY_MAX_PAR", "4")))
EFF = {"draft": "high", "expand": "high", "judge": "high", "edit": "medium", "verify": "medium", "fix": "medium", "reverify": "medium",
       "author": "high", "postverify": "medium", "copyedit": "medium"}
PREV_PLAN = {2: HERE.parent / "ch01" / "ch01_plan_v5.md", 3: HERE.parent / "ch02" / "ch02_plan_v3.md"}
LOCK = threading.Lock()
EXPAND_SYS = """You expand one section of a history of Udaypur towards its target length. Use ONLY the ASSIGNED EVIDENCE: draw on items the draft leaves unused or underused where they serve the paragraph Points of the SECTION PLAN. Every added fact ends with its evidence ID(s); only assigned IDs.
NEVER PAD: no restatement of what the draft already says, no summary or closing sentences, no general context, no method narration, no hedges for their own sake. If the assigned evidence cannot honestly support more, add less.
Keep everything already in the draft (wording, IDs, {{note: …}} blocks, quotations, heading). Return the full section in Markdown and nothing else."""


def now():
    return time.time()


class Flow:
    def __init__(self, dry):
        self.dry = dry
        self.R = rn.Run(dry)
        _, self.secs, self.targets, self.titles = va.load_outline()
        self.P = va.load_pack()
        self.S = SECTIONS = C.SECTIONS
        self.state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() and not dry else {"tasks": {}, "t0": now()}
        self.state.setdefault("t0", now())
        self.text = {}          # sec -> current text
        for s in SECTIONS:
            for stage in ("copyedit", "verify", "edit", "draft"):
                f = SEC_DIR / f"{s}_{stage}.md"
                if f.exists() and self.done(f"{stage}_{s}"):
                    self.text[s] = f.read_text(encoding="utf-8").strip()
                    break
        old = va.split_sections(C.BASELINE.read_text(encoding="utf-8")) if getattr(C, "BASELINE", None) and C.BASELINE.exists() else {}
        self.base = {n: re.sub(r"^## [^\n]*", f"## {self.titles[n]}", old[o].strip(), count=1) for n, o in getattr(C, "BASELINE_MAP", {}).items() if o in old}
        SEC_DIR.mkdir(parents=True, exist_ok=True)
        CACHE.mkdir(parents=True, exist_ok=True)
        self.ev = {}
        for s in SECTIONS:                                   # evidence blocks built once, cached
            f = CACHE / f"ch{C.CH}_{s}_evidence.txt"
            if not f.exists():
                f.write_text(p3.evidence_block(self.secs[s], self.P)[0], encoding="utf-8")
            self.ev[s] = f.read_text(encoding="utf-8")

    # ------------------------------------------------------------ bookkeeping
    def done(self, task):
        return self.state["tasks"].get(task, {}).get("status") == "done"

    def mark(self, task, status, **kw):
        with LOCK:
            rec = self.state["tasks"].setdefault(task, {})
            if status == "running":
                rec["start"] = now()
            if status in ("done", "failed", "skipped"):
                rec["end"] = now()
            rec["status"] = status
            rec.update(kw)
            if not self.dry:
                STATE.write_text(json.dumps(self.state, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
                STATUS.write_text(json.dumps({"chapter": C.CH, "t0": self.state["t0"], "now": now(), "spent": round(self.R.spent, 4),
                                              "spent_this_run": round(self.R.spent - self.R.prior, 4), "budget": rn.BUDGET,
                                              "tasks": self.state["tasks"]}, ensure_ascii=False, indent=1, default=str), encoding="utf-8")

    def effort(self, kind):
        e = EFF[kind]
        if kind in ("draft", "expand"):
            return "high"                      # user, run 2: drafting never below high, for any reason
        if OVR.exists():
            try:
                o = json.loads(OVR.read_text(encoding="utf-8"))
                e = o.get(kind, e)
            except Exception:  # noqa: BLE001
                pass
        return e

    def call(self, name, rnd, kind, system, user, out_words, model=None, stage=None):
        with SEM:
            return self.R.call(name, rnd, kind, system, user, out_words, model=model, effort=self.effort(stage or kind))

    def save(self, sec, stage, text):
        self.text[sec] = text.strip()
        if not self.dry:
            (SEC_DIR / f"{sec}_{stage}.md").write_text(text.strip() + "\n", encoding="utf-8")

    # ------------------------------------------------------------ prompts (fixed prefix first, for prompt caching)
    def prev_closing(self):
        p = PREV_PLAN.get(C.CH)
        if not p or not p.exists():
            return ""
        t = p.read_text(encoding="utf-8")
        last = re.split(r"(?m)^## \d+\.\d+ ", t)[-1]
        stmt = p3.statement("**Section statement:**" + last.split("**Section statement:**", 1)[-1]) if "**Section statement:**" in last else ""
        pts = p3.points(re.sub(r"(?s)^.*?\*\*Paragraph plan:\*\*", "", last))
        lastp = pts[-1][2] if pts else ""
        tl = (re.search(r"\*\*Through-line\.\*\*\s*(.+)", t) or [None, ""])[1]
        return (f"PREVIOUS CHAPTER'S PLANNED CLOSING (from its approved plan; the chapters are drafted in parallel, so this is the plan, not the text):\n"
                f"Through-line: {tl}\nLast section: {stmt}\nLast paragraph: {lastp}\n"
                "Continue the argument and the place from here; never recap it.")

    def writer_prompt(self, sec):
        i = self.S.index(sec)
        tg = self.targets[sec]
        fixed = (p3.STYLE_BLOCK + f"CHAPTER PLAN (question, through-line and arc):\n{p3.PLAN_HEAD}\n\nSECTIONS AND WHAT EACH ACHIEVES:\n{p3.arc(self.titles, self.secs)}\n\n")
        var = (f"{ledger.digest(sec, self.secs[sec] + self.ev[sec])}\n\nEVIDENCE FOR THIS SECTION (role and tier given for each):\n{self.ev[sec]}\n\n")
        if i == 0:
            prev = self.prev_closing() or f"(none: this section opens the book. {C.OPEN_IN})"
            prev += f"\nOpening instruction: {C.OPEN_IN}"
        else:
            prev = "THE CHAPTER SO FAR (drafted; continue from it, never repeat it):\n" + "\n\n".join(self.text[s] for s in self.S[:i])
        task = (f"\n\nSECTION TO WRITE NOW: {self.titles[sec]}\nSECTION PLAN:\n{self.secs[sec]}\n\n"
                f"LENGTH: aim at about {tg} words (IDs and notes excluded), using the evidence the plan assigns; {int(tg * 0.7)} is a floor, not a target; never pad.\n"
                + (f"CHAPTER CLOSING: {C.CLOSE_OUT}\n" if sec == self.S[-1] else ""))
        return fixed + var + prev + task

    # ------------------------------------------------------------ section tasks
    def t_draft(self, sec):
        if self.done(f"draft_{sec}"):
            return
        self.mark(f"draft_{sec}", "running")
        out = self.call(f"draft_{sec}", 1, "candidate", p3.WRITER_SYS, self.writer_prompt(sec), self.targets[sec] + 400, model=rn.FLAGSHIP, stage="draft")
        txt = (out or "").strip() if not self.dry else f"## {self.titles[sec]}\n\nx [{list(p3.roles(self.secs[sec]))[0]}]."
        if not txt.startswith("## "):
            txt = f"## {self.titles[sec]}\n\n" + txt
        w0, expanded = va.words(txt), None
        if self.dry or w0 < 0.85 * self.targets[sec]:            # user, run 2: one expand-from-assigned-evidence call
            txt, expanded = self.expand(sec, txt)
        self.save(sec, "draft", txt)
        self.mark(f"draft_{sec}", "done", words=va.words(txt), words_first=w0, expanded=expanded)

    def expand(self, sec, txt):
        tg = self.targets[sec]
        rep = p3.check(txt, self.P, sec, self.targets)
        u = (p3.STYLE_BLOCK + f"SECTION PLAN:\n{self.secs[sec]}\n\nASSIGNED EVIDENCE (the only source of any added material):\n{self.ev[sec]}\n\n"
             f"TARGET: about {tg} words (the draft has {va.words(txt)}).\n\n=== DRAFT ===\n{txt}")
        out = self.call(f"expand_{sec}", 1, "expand", EXPAND_SYS, u, tg + 300, model=rn.FLAGSHIP, stage="expand")
        if self.dry or not isinstance(out, str) or not out.strip().startswith("## " + sec):
            return txt, {"kept": False, "reason": "no usable output"}
        new = out.strip()
        nr = p3.check(new, self.P, sec, self.targets)
        assigned = set(p3.roles(self.secs[sec]))
        added_ids = set(va.ids_in(va.strip_notes(new))) - set(va.ids_in(va.strip_notes(txt)))
        ok = (nr["integrity_ok"] and va.words(new) > va.words(txt) and added_ids <= assigned
              and p3.score_rep(dict(nr, word_issues=[])) <= p3.score_rep(dict(rep, word_issues=[])))
        return (new if ok else txt), {"kept": ok, "before": va.words(txt), "after": va.words(new), "new_ids_outside_plan": sorted(added_ids - assigned)}

    def so_far(self, sec):
        i = self.S.index(sec)
        return "\n\n".join(self.text[s] for s in self.S[:i] if s in self.text) or self.prev_closing()

    def t_judge(self, sec):
        if self.done(f"judge_{sec}"):
            return
        self.mark(f"judge_{sec}", "running")
        entries = {"DRAFT": self.text[sec]}
        if sec in self.base:
            entries["BASE"] = self.base[sec]
        reps = {L: p3.check(t, self.P, sec, self.targets) for L, t in entries.items()}
        lead = ledger.digest(sec, self.secs[sec] + self.ev[sec])
        old = self.R.call
        v = None
        with SEM:
            v = p3.judge(_EffR(self.R, self.effort("judge")), f"judge_{sec}", sec, self.secs, self.titles, self.targets, self.P, entries, reps,
                         (lead + "\n\n" if lead else "") + self.so_far(sec))
        self.R.call = old
        v = v or {}
        if not self.dry:
            (SEC_DIR / f"{sec}_judge.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
        sc = v.get("scores", {})
        self.mark(f"judge_{sec}", "done", scores={L: (sc.get(L) or {}).get("total") for L in entries})

    def t_edit(self, sec):
        if self.done(f"edit_{sec}"):
            return
        self.mark(f"edit_{sec}", "running")
        v = json.loads((SEC_DIR / f"{sec}_judge.json").read_text(encoding="utf-8")) if (SEC_DIR / f"{sec}_judge.json").exists() else {}
        L = "DRAFT"
        cur = self.text[sec]
        frep = p3.check(cur, self.P, sec, self.targets)
        tg = self.targets[sec]
        eu = (p3.STYLE_BLOCK + f"WRITER BRIEF:\n{p3.WRITER_SYS}\n\n{ledger.digest(sec, self.secs[sec] + self.ev[sec])}\n\nTHE CHAPTER SO FAR:\n{self.so_far(sec) or '(none)'}\n\n"
              f"SECTION PLAN:\n{self.secs[sec]}\n\nWORD RANGE: aim at about {tg}; {int(tg * 0.7)}–{int(tg * 1.2)} (never pad)\n\n"
              "IMPROVEMENTS TO APPLY:\n" + "\n".join(f"- {x}" for x in v.get("improvements", []))
              + "\nPOINTS FOUND MISSING OR ALTERED:\n" + "\n".join(f"- {x}" for x in (v.get("points_missed") or {}).get(L, []))
              + "\nINT-TRIVIAL SENTENCES TO CUT:\n" + "\n".join(f"- {x}" for x in (v.get("int_trivial") or {}).get(L, []))
              + "\nDIGRESSIONS TO CUT OR REDUCE TO A CLAUSE:\n" + "\n".join(f"- {x}" for x in (v.get("digressions") or {}).get(L, []))
              + "\nRULE ARTEFACTS TO REMOVE:\n" + "\n".join(f"- {x}" for x in (v.get("rule_artefacts") or {}).get(L, []))
              + "\nAUTOMATED-CHECK PROBLEMS TO FIX:\n" + "\n".join(f"- {x}" for x in (p3.problems_of(frep) + ledger.check(sec, cur))[:30])
              + "\n\nEVIDENCE:\n" + self.ev[sec] + f"\n\n=== SECTION TO REVISE ===\n{cur}"
              + (f"\n\n=== ENTRY BASE (transplant source only) ===\n{self.base[sec]}" if sec in self.base else ""))
        out = self.call(f"edit_{sec}", 3, "edit", p3.EDIT_SYS, eu, tg + 200, stage="edit")
        info = {"kept": False, "reason": "no output"}
        if isinstance(out, str) and out.strip():
            with SEM:
                ok, txt, info = p3.edit_gate(_EffR(self.R, self.effort("edit")), f"edit_{sec}", out.strip(), frep, sec, self.P, self.targets, cur, self.dry)
            if ok:
                cur = txt
        self.save(sec, "edit", cur)
        self.mark(f"edit_{sec}", "done", kept=info.get("kept"), repaired=info.get("repaired", False), words=va.words(cur))

    def t_verify(self, sec):
        if self.done(f"verify_{sec}"):
            return
        self.mark(f"verify_{sec}", "running")
        if self.dry:
            for k in ("verify", "fix", "reverify"):
                self.call(f"{k}_{sec}", 6, k, p3.VERIFY_SYS, "x" * 30000, 2000, stage=k)
            self.save(sec, "verify", self.text[sec])
            self.mark(f"verify_{sec}", "done")
            return
        warn = p3.check(self.text[sec], self.P, sec, self.targets).get("agent_nouns", [])
        R = _EffR(self.R, self.effort("verify"), sem=SEM)
        txt, st, _ = p3.verify_sections(self.text[sec] + "\n", self.P, R, prefix="verify", fix=True,
                                        extra_context=("CODE WARNINGS (check each; AGENT-INVENTED if no cited item attributes the action):\n" + "\n".join(warn) + "\n\n") if warn else "")
        (SEC_DIR / f"{sec}_verify.json").write_text(json.dumps(st, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
        self.save(sec, "verify", txt)
        self.mark(f"verify_{sec}", "done", before=st.get("verdicts_before"), after=st.get("verdicts_after"), remaining=len(st.get("remaining", [])))

    # ------------------------------------------------------------ chapter tasks
    def t_gate(self):
        if self.done("gate"):
            return True
        self.mark("gate", "waiting")
        while not self.dry:
            if GATE.exists():
                g = json.loads(GATE.read_text(encoding="utf-8"))
                if g.get("status") in ("pass", "prose"):
                    self.mark("gate", "done", result=g.get("status"))
                    return True
                if g.get("status") == "fail":
                    self.mark("gate", "failed", result="fail")
                    return False
            time.sleep(5)
        self.mark("gate", "done", result="dry")
        return True

    def chapter(self):
        return "\n\n".join(self.text[s] for s in self.S) + "\n"

    def t_author(self):
        if self.done("author"):
            return
        self.mark("author", "running")
        ch = self.chapter()
        rep = p3.check(ch, self.P, None, self.targets)
        extra = (p3.STYLE_BLOCK + f"CHAPTER PLAN:\n{p3.PLAN_HEAD}\n\nSECTIONS:\n{p3.arc(self.titles, self.secs)}\n\nPARAGRAPH POINTS:\n"
                 + "\n\n".join(f"{self.titles[s]}\n{p3.points_block(self.secs[s])}" for s in self.S)
                 + f"\n\n{self.prev_closing()}\n\nCHAPTER OPENING: {C.OPEN_IN}\nCHAPTER CLOSING: {C.CLOSE_OUT}\n\nCHAPTER:\n{ch}")
        out = self.call("author", 5, "author", p3.AUTHOR_SYS, extra, sum(self.targets.values()) + 500, model=rn.FLAGSHIP, stage="author")
        kept, why = False, "no output"
        if isinstance(out, str) and out.strip() and not self.dry:
            new = out.strip() + "\n"
            nr = p3.check(new, self.P, None, self.targets)
            parts = va.split_sections(new)
            kept = nr["integrity_ok"] and p3.score_rep(nr) <= p3.score_rep(rep) and p3.guards_ok(ch, new) and all(s in parts for s in self.S)
            why = "kept" if kept else f"rejected: integrity {nr['integrity_ok']}, score {p3.score_rep(nr)} vs {p3.score_rep(rep)}, guards {p3.guards_ok(ch, new)}"
            (SEC_DIR / "author_raw.md").write_text(new, encoding="utf-8")
            (SEC_DIR / "preauthor.md").write_text(ch, encoding="utf-8")
            if kept:
                for s in self.S:
                    self.save(s, "author", parts[s])
        self.mark("author", "done", kept=kept, why=why)

    def t_postverify(self):
        """verify only the sentences the author's pass changed; flags go to the editor's line edit (no automatic fix)"""
        if self.done("postverify"):
            return
        self.mark("postverify", "running")
        pre = (SEC_DIR / "preauthor.md")
        if self.dry or not pre.exists() or not self.state["tasks"].get("author", {}).get("kept"):
            self.mark("postverify", "done", changed=0)
            return
        old = {r["sentence"] for p in p3.rows_of(pre.read_text(encoding="utf-8"), self.P).values() for para in p for r in para["rows"]}
        smap = p3.rows_of(self.chapter(), self.P)
        rows = [r for sec, paras in smap.items() for para in paras for r in para["rows"] if r["sentence"] not in old]
        flags = []
        if rows:
            import verify as vf
            iids = sorted({i for r in rows for i in r["ids"]})
            u = (p3.CONVENTIONS + "EVIDENCE ITEMS:\n" + "\n\n".join(vf.item_text(self.P[i]) for i in iids)
                 + "\n\nTHE SECTION, PARAGRAPH BY PARAGRAPH:\n--- PARAGRAPH (sentences changed by the author's pass) ---\nITEMS:\n"
                 + "\n".join(f"{r['sid']} [{r['kind']}; evidence: {', '.join(r['ids']) if r['kind'] != 'INT' else 'paragraph facts'}]: {r['sentence']}" for r in rows))
            out = self.call("postverify", 6, "verify", p3.VERIFY_SYS, u, 70 * len(rows), stage="postverify")
            j = rn.parse_json(out) or {}
            flags = [x for x in j.get("results", []) if str(x.get("verdict", "")).upper() not in p3.GOOD]
        (SEC_DIR / "postverify.json").write_text(json.dumps({"changed": len(rows), "flags": flags,
                                                             "rows": {r["sid"]: r["sentence"] for r in rows}}, ensure_ascii=False, indent=1), encoding="utf-8")
        self.mark("postverify", "done", changed=len(rows), flags=len(flags))

    def t_copyedit(self, sec):
        if self.done(f"copyedit_{sec}"):
            return
        self.mark(f"copyedit_{sec}", "running")
        cur = self.text[sec]
        rep = p3.check(cur, self.P, sec, self.targets)
        import prose_checks as pc
        mech = pc.style_mechanics(cur)
        u = (p3.STYLE_BLOCK + f"{ledger.digest(sec, self.secs[sec] + self.ev[sec])}\n\nMECHANICAL STYLE WARNINGS FROM CODE (fix where the style sheet requires):\n" + "\n".join(f"- {x}" for x in mech[:25])
             + f"\n\n=== SECTION ===\n{cur}")
        out = self.call(f"copyedit_{sec}", 8, "polish", p3.COPYEDIT_SYS, u, self.targets[sec] + 200, stage="copyedit")
        kept = False
        if isinstance(out, str) and out.strip().startswith("## " + sec) and not self.dry:
            nr = p3.check(out.strip(), self.P, sec, self.targets)
            same_ids = sorted(va.ids_in(out)) == sorted(va.ids_in(cur)) and va.notes_in(out) == va.notes_in(cur)
            kept = nr["integrity_ok"] and p3.score_rep(nr) <= p3.score_rep(rep) and same_ids and va.words(out) >= 0.97 * va.words(cur)
            if kept:
                self.save(sec, "copyedit", out.strip())
        if not kept:
            self.save(sec, "copyedit", cur)
        self.mark(f"copyedit_{sec}", "done", kept=kept)

    def t_finish(self):
        ch = self.chapter()
        if not self.dry:
            C.OUT.write_text(ch, encoding="utf-8")
        rep = p3.check(ch, self.P, None, self.targets)
        self.mark("finish", "done", words=rep["words"], summary=p1.summ(rep))

    # ------------------------------------------------------------ scheduler
    def run(self):
        ex = cf.ThreadPoolExecutor(max_workers=12)
        post = {}

        def section_tail(s):
            self.t_judge(s)
            self.t_edit(s)
            self.t_verify(s)

        for s in self.S:                                   # drafting chain; each section's tail runs as soon as its draft lands
            self.t_draft(s)
            post[s] = ex.submit(section_tail, s)
        for s, f in post.items():
            f.result()
        if not self.t_gate():
            print(f"[{rn.ts()}] chapter {C.CH}: gate failed; stopping", flush=True)
            return
        self.t_author()
        self.t_postverify()
        list(ex.map(self.t_copyedit, self.S))
        self.t_finish()
        print(f"[{rn.ts()}] CHAPTER {C.CH} FLOW FINISHED; spent this run ${self.R.spent - self.R.prior:.3f}", flush=True)


class _EffR:
    """wraps Run so calls made inside pipeline3 helpers use the flow's effort (and, optionally, its semaphore)"""
    def __init__(self, R, effort, sem=None):
        self.R, self.e, self.sem = R, effort, sem

    def call(self, name, rnd, kind, system, user, out_words, model=None, effort=None):
        if self.sem:
            with self.sem:
                return self.R.call(name, rnd, kind, system, user, out_words, model=model, effort=self.e)
        return self.R.call(name, rnd, kind, system, user, out_words, model=model, effort=self.e)

    def parallel(self, jobs):
        return self.R.parallel(jobs)

    def __getattr__(self, k):
        return getattr(self.R, k)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    F = Flow("--dry-run" in sys.argv)
    F.run()
    if F.dry:
        print(json.dumps({"chapter": C.CH, "calls": len(F.R.calls), "projected_cost_usd": round(F.R.spent, 3),
                          "by_stage": {k: round(v, 3) for k, v in F.R.stage_spend.items()}}, indent=1))
