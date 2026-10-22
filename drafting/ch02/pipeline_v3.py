"""Chapter 1 pipeline v3 — speed first; quality held by judge, edit and code checks.

All sections are drafted in parallel (no sequential running summaries). Each section prompt gets the writer
brief, the full refined outline, its own evidence, a "covered elsewhere" list (other sections' key points),
its planned incoming/outgoing transitions, and the first ~600 words of cand_1.1_A as a voice sample.

Rounds (every call in a round runs concurrently, up to 10 at once):
  1 candidates  — 1.1 B (A exists) + 2 each for 1.2–1.5            effort high
  2 judges      — code checks first, then 1 judge per section          effort high
  3 edits       — revert-if-worse                                     effort medium
  4 stitch      — owns cross-section continuity/repetition            effort high
  5 validation  — Phase 3 code checks; revisions of failing sections  effort medium
  6 polish      — kept only if it validates no worse                  effort medium
Rules: 10-min timeout per call (background mode + polling; cancel on timeout) -> one retry one effort level
lower, logged; exponential backoff on rate limits; $5 hard stop; $0.90 finishing reserve; cut order
polish, then edits; ch01_draft_v1.md, footnoted version and report are always written.

  python -I "drafting/ch01/pipeline_v3.py" --dry-run
  python -u -I "drafting/ch01/pipeline_v3.py"
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import glob
import json
import os
import re
import subprocess
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import draft as dr  # noqa: E402
import validate as va  # noqa: E402

D = dr.D
LOG = D / "api_log"
CAND = D / "candidates"
BUDGET, RESERVE = 5.00, 0.90
MAX_PAR = 10
CALL_TIMEOUT = 600
# Three earlier synchronous requests never returned (OpenAI may still have billed them); counted
# conservatively against the $5 limit unless the user releases them (env CH01_UNACCOUNTED_USD=0).
UNACCOUNTED = 0.0
MODEL = os.getenv("OPENAI_MODEL") or "gpt-6.1-sol"
LOWER = {"max": "xhigh", "xhigh": "high", "high": "medium", "medium": "low", "low": "low"}
EFFORT = {"candidate": "high", "judge": "high", "edit": "medium", "stitch": "high", "revise": "medium", "polish": "medium"}
# Estimation model (from the one observed call: max effort, 22.8k reasoning, 694 s for 24.5k output tokens)
REASON = {"max": 23000, "xhigh": 17000, "high": 11000, "medium": 5000, "low": 2000}
SEC_PER_OUT_TOKEN = 694 / 24506
SECTIONS = dr.SECTIONS


def ts():
    return time.strftime("%H:%M:%S")


class BudgetStop(Exception):
    pass


def keep_awake():
    """Ask Windows not to sleep while the run is alive (ES_CONTINUOUS | ES_SYSTEM_REQUIRED). The Chapter 1 run
    stalled for hours when the machine slept between polls."""
    try:
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
        return True
    except Exception:  # noqa: BLE001
        return False


class Run:
    def __init__(self, dry):
        self.dry = dry
        choice = json.loads((D / "model_choice.json").read_text(encoding="utf-8"))
        self.price = choice["prices_per_1M"][MODEL]
        self.lock = threading.Lock()
        self.calls, self.stage_spend = [], {}
        self.spent = 0.0
        self.prior = 0.0
        self.est_seconds = {}
        if not dry:
            for f in sorted(glob.glob(str(LOG / "*.json"))):
                m = json.load(open(f, encoding="utf-8"))["meta"]
                self.prior += m.get("cost_usd") or 0
            self.spent = self.prior + UNACCOUNTED
            dr.load_key()
            from openai import OpenAI
            self.c = OpenAI(timeout=60, max_retries=0)     # every HTTP request bounded; retries are ours
            self.awake = keep_awake()

    def estimate(self, system, user, kind, out_words, effort):
        tin = dr.ntok(system) + dr.ntok(user)
        tout = int(out_words * 1.45) + REASON[effort]
        return tin, tout, tin / 1e6 * self.price["input"] + tout / 1e6 * self.price["output"], tout * SEC_PER_OUT_TOKEN

    def call(self, name, round_, kind, system, user, out_words):
        effort = EFFORT[kind]
        for attempt in (1, 2):
            tin, tout, est, secs = self.estimate(system, user, kind, out_words, effort)
            rec = {"name": name, "stage": kind, "round": round_, "kind": kind, "model": MODEL, "effort": effort,
                   "attempt": attempt, "est_input_tokens": tin, "est_output_tokens": tout, "est_cost_usd": round(est, 4),
                   "est_seconds": round(secs)}
            if self.dry:
                with self.lock:
                    self.calls.append(rec)
                    self.spent += est
                    self.stage_spend[kind] = self.stage_spend.get(kind, 0) + est
                    self.est_seconds[name] = secs
                return None
            with self.lock:
                if self.spent + est > BUDGET:
                    raise BudgetStop(f"before {name}: spent ${self.spent:.3f} + est ${est:.3f} > ${BUDGET}")
            try:
                return self._once(name, kind, system, user, effort, rec, est)
            except TimeoutError as e:
                print(f"[{ts()}] TIMEOUT {name} at effort {effort}: {e}; retrying once at {LOWER[effort]}", flush=True)
                effort = LOWER[effort]
            except Exception as e:  # noqa: BLE001
                print(f"[{ts()}] FAILED {name} attempt {attempt}: {type(e).__name__}: {str(e)[:200]}", flush=True)
                effort = LOWER[effort]
        return ""

    def _create(self, params):
        delay = 2
        for _ in range(7):
            try:
                return self.c.responses.create(background=True, **params)
            except Exception as e:  # noqa: BLE001
                if "rate" in type(e).__name__.lower() or "429" in str(e):
                    print(f"[{ts()}] rate-limited; backing off {delay}s", flush=True)
                    time.sleep(delay)
                    delay = min(delay * 2, 120)
                    continue
                raise
        raise RuntimeError("rate-limited repeatedly")

    def _once(self, name, kind, system, user, effort, rec, est):
        params = {"model": MODEL, "reasoning": {"effort": effort},
                  "input": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                  "max_output_tokens": 64000}
        t0 = time.time()
        print(f"[{ts()}] calling {name} (effort {effort}; est ${est:.3f}; spent ${self.spent:.3f})", flush=True)
        r = self._create(params)
        rid = r.id
        deadline = t0 + CALL_TIMEOUT
        while r.status in ("queued", "in_progress"):
            if time.time() > deadline:
                # one last look: after a stall (sleep, hung poll) the response may in fact be finished
                try:
                    r = self.c.responses.retrieve(rid)
                except Exception:  # noqa: BLE001
                    pass
                if r.status not in ("queued", "in_progress"):
                    break
                try:
                    self.c.responses.cancel(rid)
                except Exception:  # noqa: BLE001
                    pass
                self._charge(name, kind, params, dict(rec, effort=effort), None, est, t0, rid, "cancelled_timeout", "")
                raise TimeoutError(f"no result after {CALL_TIMEOUT}s (response {rid} cancelled; charged est ${est:.3f})")
            time.sleep(8)
            for _ in range(5):
                if time.time() > deadline:
                    break
                try:
                    r = self.c.responses.retrieve(rid)     # 60 s HTTP timeout, no client retries
                    break
                except Exception as e:  # noqa: BLE001
                    print(f"[{ts()}] poll error {type(e).__name__}; retrying", flush=True)
                    time.sleep(10)
        text = r.output_text if r.status == "completed" else ""
        self._charge(name, kind, params, dict(rec, effort=effort), r.usage, est, t0, rid, r.status, text)
        if r.status != "completed" or not text.strip():
            raise RuntimeError(f"status {r.status} ({getattr(r, 'incomplete_details', None)})")
        return text

    def _charge(self, name, kind, params, rec, u, est, t0, rid, status, text):
        if u is not None:
            rt = getattr(getattr(u, "output_tokens_details", None), "reasoning_tokens", None)
            cost = u.input_tokens / 1e6 * self.price["input"] + u.output_tokens / 1e6 * self.price["output"]
            rec.update(input_tokens=u.input_tokens, output_tokens=u.output_tokens, reasoning_tokens=rt)
        else:
            cost = est
        with self.lock:
            self.spent += cost
            self.stage_spend[kind] = self.stage_spend.get(kind, 0) + cost
            rec.update(cost_usd=round(cost, 4), seconds=round(time.time() - t0, 1), status=status, response_id=rid,
                       spent_so_far=round(self.spent, 4))
            LOG.mkdir(exist_ok=True)
            n = len(list(LOG.glob("*.json"))) + 1
            sfx = "" if status == "completed" else f"_{status}"
            (LOG / f"{n:03d}_v3_{name}{sfx}.json").write_text(json.dumps(
                {"meta": rec, "request": params, "response_text": text}, ensure_ascii=False, indent=1), encoding="utf-8")
            self.calls.append(rec)
            print(f"[{ts()}] done {name} ({status}, {rec['effort']}) in {time.time() - t0:.0f}s ${cost:.3f} — spent ${self.spent:.3f}", flush=True)
            if self.spent >= BUDGET:
                raise BudgetStop(f"after {name}: spend ${self.spent:.3f} reached ${BUDGET}")

    def parallel(self, jobs):
        """jobs: list of (key, fn). Runs concurrently (≤ MAX_PAR); returns {key: result or exception}."""
        out = {}
        with cf.ThreadPoolExecutor(max_workers=min(MAX_PAR, max(1, len(jobs)))) as ex:
            futs = {ex.submit(fn): k for k, fn in jobs}
            for f in cf.as_completed(futs):
                try:
                    out[futs[f]] = f.result()
                except Exception as e:  # noqa: BLE001
                    out[futs[f]] = e
        return out


# ------------------------------------------------------------------ prompt material
def section_parts(secs):
    info = {}
    for k, txt in secs.items():
        purpose = (re.search(r"\*\*Purpose:\*\*\s*(.+)", txt) or [None, ""])[1]
        points = re.findall(r"(?m)^\d+\.\s+\*\*(.+?)\*\*", txt)
        trans = (re.search(r"\*\*Transition:\*\*\s*(.+)", txt) or [None, ""])[1]
        info[k] = {"purpose": purpose.strip(), "points": points, "transition": trans.strip()}
    return info


def covered_elsewhere(sec, info, titles):
    lines = []
    for k in SECTIONS:
        if k == sec:
            continue
        lines.append(f"- {titles[k]}: {info[k]['purpose']} Key points: " + "; ".join(info[k]["points"]))
    return "\n".join(lines)


def transitions(sec, info, titles):
    i = SECTIONS.index(sec)
    inc = f"from {titles[SECTIONS[i - 1]]}: {info[SECTIONS[i - 1]]['transition']}" if i else "none — this section opens Chapter 2; Chapter 1 closed by asking what country produced this town"
    out = info[sec]["transition"] + (f" (leads into {titles[SECTIONS[i + 1]]})" if i + 1 < len(SECTIONS) else " (closing lead: Chapter 3 turns from water to rock — the stone of the hill)")
    return inc, out


def voice_sample():
    p = CAND / "1.1_A.md"
    if not p.exists():
        return "(none)"
    words = p.read_text(encoding="utf-8").split()
    return " ".join(words[:600])


V3_NOTES = """PARALLEL DRAFTING NOTES:
- Sections are drafted at the same time, so you cannot see the other sections. Do NOT develop anything on the "covered elsewhere" list; at most mention it in a clause and point to the section that develops it.
- Vijay Manohar Tiwari, author of *Jagta Hua Kasba*, is introduced by full name in section 1.1 only. In every other section write "Tiwari" or "the author of *Jagta Hua Kasba*". Ignore any instruction in the brief that refers to a running summary.
- Open with the planned incoming transition in mind and end so that the planned outgoing transition can follow.
- VOICE SAMPLE (from an earlier draft of 1.1): match its register, rhythm and citation style. Do not copy its content or sentences."""

OPENINGS = {
    "A": "OPENING FOR THIS CANDIDATE: lead with the place — a concrete physical scene drawn from the evidence.",
    "B": "OPENING FOR THIS CANDIDATE: lead with a source — a short, exactly quoted phrase from one evidence item, attributed.",
}

JUDGE_SYS = """You are a demanding editor judging candidate drafts of one section of a non-fiction chapter about Udaypur. The sections were drafted in parallel; each must stay inside its own lane (see "covered elsewhere").
Score each candidate 1–10 on: fidelity (only supplied evidence; correct citations; conflicts unresolved), coverage (the section's key points and conflicts), prose (specific, varied sentences; strong concrete opening line; no banned phrases), voice (matches the voice sample and writer brief), transition (fits the planned incoming and outgoing transitions; does not develop material covered elsewhere).
The automated check report for each candidate is supplied: weigh uncited claims and fabrication flags heavily under fidelity.
Pick the best candidate. Then give 5–8 concrete, line-level improvements to apply to it (quote the sentence or phrase to change and say exactly how). You may point to a stronger paragraph in the other candidate to transplant, saying why — every transplanted sentence keeps its bracketed IDs.
Improvements must not introduce any fact that is not in the evidence.
Return ONLY JSON: {"scores": {"A": {"fidelity":n,"coverage":n,"prose":n,"voice":n,"transition":n,"total":n}, ...}, "best": "A", "improvements": ["..."], "transplants": ["..."], "rationale": "..."}"""

EDIT_SYS = """You revise one section of a non-fiction chapter about Udaypur. Apply ONLY the listed improvements (and any listed transplant) and fix the listed automated-check problems.
STRICT: add no facts, dates, names or numbers; do not remove, alter or invent any bracketed evidence ID — every factual sentence keeps its IDs; do not change text inside quotation marks except to delete a whole quotation together with its sentence; keep the heading line exactly; stay within the word range given.
Return the full revised section in Markdown and nothing else."""

STITCH_SYS = """You are the final editor of Chapter 1 of a book on Udaypur. The five sections were drafted in parallel, so you own cross-section continuity: smooth transitions using the planned transitions, remove repetition across sections (keep each point in the section that owns it per the coverage map; elsewhere cut it or reduce it to a clause), make sure Vijay Manohar Tiwari is named in full once (first mention) and as "Tiwari"/"the author" afterwards, and keep one voice.
STRICT RULES: Do not add any fact, date, name or number. Do not remove, alter, move to another claim, or invent any bracketed evidence ID — every factual sentence keeps its IDs exactly. Do not change any text inside quotation marks. You may delete a repeated sentence together with its IDs, shorten, reorder within a section, and rewrite connective wording. Keep each section's heading and keep each section near its word target; total 3,800–4,200 words (IDs excluded). British/Indian English; keep all diacritics.
Return only the full chapter in Markdown."""

REVISE_SYS = """You fix specific validation problems in one section of a non-fiction chapter about Udaypur.
Fix ONLY the listed problems: cite uncited factual sentences with an ID from the supplied evidence or delete the claim; replace any non-verbatim quotation with the exact words of the cited item's QUOTE or paraphrase it; delete or re-cite any year or name that does not appear in the cited items; adjust length if asked. Add no new facts. Keep all other text, IDs and the heading unchanged.
Return the full corrected section in Markdown and nothing else."""

POLISH_SYS = """Polish this chapter at sentence level: cut repetition, tighten rhythm, vary sentence openings, remove any banned phrase ("nestled", "tapestry", "testament to", "stands as", "rich history", "steeped in", "delve", "bustling", "timeless", "hidden gem", "in conclusion") and filler rhetorical questions.
STRICT: no new facts, dates, names or numbers; every bracketed evidence ID stays attached to its claim, unchanged; text inside quotation marks unchanged; headings unchanged; keep total length within 3,800–4,200 words (IDs excluded).
Return only the full chapter in Markdown."""


def ev_block(ids, P):
    return "\n\n".join(dr.fmt_item(P[i]) for i in ids)


def problems_of(rep):
    out = [f"invalid ID {x}" for x in rep["invalid_ids"]]
    out += [f"quotation not verbatim in the cited item(s) {q['cited']}: \"{q['quote']}\"" for q in rep["nonverbatim_quotes"]]
    out += [f"uncited factual sentence: {s}" for s in rep["uncited_claims"]]
    out += [f"not supported by the cited items: {s}" for s in rep["fabrication"]]
    out += rep["word_issues"]
    out += [f"conflict not presented with both sides: {c['conflict']}" for c in rep["conflicts"] if not c["present"]]
    return out


def score_rep(rep):
    return (0 if rep["integrity_ok"] else 1000) + 3 * len(rep["uncited_claims"]) + 3 * len(rep["fabrication"]) \
        + 5 * len(rep["word_issues"]) + 5 * sum(not c["present"] for c in rep["conflicts"])


def parse_json(text):
    m = re.search(r"\{.*\}", text or "", re.S)
    try:
        return json.loads(m.group(0)) if m else None
    except Exception:  # noqa: BLE001
        return None


# ------------------------------------------------------------------ main
def run(dry):
    t_start = time.time()
    print(f"[{ts()}] pipeline v3 start (dry={dry})", flush=True)
    full_outline, head, secs, targets, titles = dr.outline_sections()
    P = dr.pack()
    cov = json.loads((D / "coverage.json").read_text(encoding="utf-8"))
    info = section_parts(secs)
    R = Run(dry)
    vs = voice_sample()
    state = {"pipeline": "v3", "model": MODEL, "effort": EFFORT, "n_candidates": 2, "budget": BUDGET, "reserve": RESERVE,
             "unaccounted_usd": UNACCOUNTED if not dry else 0, "prior_spend_usd": round(R.prior, 4), "sections": {},
             "decisions": [], "rounds": {}}
    skip_polish = skip_edit = False
    # ---- budget plan before round 1 (cut order: polish, then edits)
    if not dry:
        avail = BUDGET - RESERVE - R.spent
        est_r123 = 9 * 0.17 + 5 * 0.16 + 5 * 0.10
        if est_r123 > avail:
            skip_polish = True
            state["decisions"].append(f"rounds 1–3 est ${est_r123:.2f} > ${avail:.2f} available outside the reserve: polish will be skipped")
            if est_r123 - 5 * 0.10 > avail + 0.12:
                skip_edit = True
                state["decisions"].append("still short: edit round skipped")
        for d_ in state["decisions"]:
            print(f"[{ts()}] ADAPT: {d_}", flush=True)
    prompts = {}
    for sec in SECTIONS:
        system, base_user, ids = dr.section_prompt(sec, full_outline, secs, targets, titles, P, cov, "")
        inc, outg = transitions(sec, info, titles)
        base_user = base_user.replace("SUMMARY OF SECTIONS ALREADY DRAFTED:\n(none — this is the first section)\n\n", "")
        extra = (f"\n{V3_NOTES}\n\nCOVERED ELSEWHERE (do not develop):\n{covered_elsewhere(sec, info, titles)}\n\n"
                 f"PLANNED INCOMING TRANSITION: {inc}\nPLANNED OUTGOING TRANSITION: {outg}\n\nVOICE SAMPLE:\n{vs}\n")
        prompts[sec] = (system, base_user + extra, ids)
    # ================= round 1: candidates =================
    t1 = time.time()
    cands = {sec: {} for sec in SECTIONS}
    if (CAND / "1.1_A.md").exists():
        cands["1.1"]["A"] = (CAND / "1.1_A.md").read_text(encoding="utf-8")
    jobs = []
    for sec in SECTIONS:
        for L in "AB":
            if L in cands[sec] or (CAND / f"v3_{sec}_{L}.md").exists():
                if (CAND / f"v3_{sec}_{L}.md").exists():
                    cands[sec][L] = (CAND / f"v3_{sec}_{L}.md").read_text(encoding="utf-8")
                continue
            def job(sec=sec, L=L):
                system, user, _ = prompts[sec]
                out = R.call(f"cand_{sec}_{L}", 1, "candidate", system, user + "\n" + OPENINGS[L], targets[sec] + 250)
                if out is None:
                    return f"## {titles[sec]}\n" + ("Lorem ipsum dolor [C01-GANGULY-006]. " * (targets[sec] // 4))
                body, _ = dr.split_summary(out)
                if body and not dry:
                    CAND.mkdir(exist_ok=True)
                    (CAND / f"v3_{sec}_{L}.md").write_text(body, encoding="utf-8")
                return body
            jobs.append(((sec, L), job))
    res = R.parallel(jobs)
    for (sec, L), body in res.items():
        if isinstance(body, BudgetStop):
            state["budget_stop"] = str(body)
        elif isinstance(body, str) and body.strip():
            cands[sec][L] = body
    state["rounds"]["1_candidates"] = {"seconds": round(time.time() - t1), "calls": len(jobs)}
    # ================= round 2: code checks + judges =================
    t2 = time.time()
    checks, verdicts = {}, {}
    for sec in SECTIONS:
        checks[sec] = {L: va.check(c, P, sec) for L, c in cands[sec].items()}
    jobs = []
    for sec in SECTIONS:
        labels = sorted(cands[sec])
        if not labels:
            continue
        alive = [L for L in labels if checks[sec][L]["integrity_ok"]] or [min(labels, key=lambda L: score_rep(checks[sec][L]))]
        state["sections"][sec] = {"candidates": [{"label": L, "words": checks[sec][L]["words"].get(sec),
                                                  "integrity_ok": checks[sec][L]["integrity_ok"], "check": va.summary(checks[sec][L])}
                                                 for L in labels], "alive": alive}
        if len(alive) < len(labels):
            state["sections"][sec]["note"] = f"discarded for citation integrity: {', '.join(L for L in labels if L not in alive)}"
        def job(sec=sec, alive=alive):
            system, _, ids = prompts[sec]
            inc, outg = transitions(sec, info, titles)
            ju = (f"WRITER BRIEF:\n{dr.WRITER_BRIEF}\n{V3_NOTES}\n\nSECTION BRIEF:\n{secs[sec]}\n\nWORD TARGET: {targets[sec]} (±10%)\n\n"
                  f"COVERED ELSEWHERE:\n{covered_elsewhere(sec, info, titles)}\n\nPLANNED INCOMING TRANSITION: {inc}\nPLANNED OUTGOING TRANSITION: {outg}\n\n"
                  f"VOICE SAMPLE:\n{vs}\n\nEVIDENCE (for checking fidelity):\n{ev_block(ids, P)}\n\n"
                  + "\n\n".join(f"=== CANDIDATE {L} ===\nAUTOMATED CHECKS: {json.dumps(problems_of(checks[sec][L])[:25], ensure_ascii=False)}\n\n{cands[sec][L]}"
                                for L in alive))
            out = R.call(f"judge_{sec}", 2, "judge", JUDGE_SYS, ju, 700)
            return parse_json(out) if out else None
        jobs.append((sec, job))
    res = R.parallel(jobs)
    for sec in SECTIONS:
        if sec not in state["sections"]:
            continue
        alive = state["sections"][sec]["alive"]
        v = res.get(sec)
        if isinstance(v, BudgetStop):
            state["budget_stop"] = str(v)
            v = None
        v = v if isinstance(v, dict) else {"best": alive[0], "improvements": [], "scores": {}, "rationale": "judge unavailable; first surviving candidate used"}
        if v.get("best") not in alive:
            v["best"] = alive[0]
        verdicts[sec] = v
        state["sections"][sec]["judge"] = v
        if not dry:
            (D / f"judge_v3_{sec}.json").write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
    state["rounds"]["2_judges"] = {"seconds": round(time.time() - t2), "calls": len(jobs)}
    # ================= round 3: edits =================
    t3 = time.time()
    finals, final_reps = {}, {}
    jobs = []
    for sec, v in verdicts.items():
        best = v["best"]
        finals[sec], final_reps[sec] = cands[sec][best], checks[sec][best]
        if skip_edit:
            state["sections"][sec]["edit"] = {"kept": False, "reason": "edit round skipped to protect the finishing reserve"}
            continue
        def job(sec=sec, v=v, best=best):
            _, _, ids = prompts[sec]
            t = targets[sec]
            others = "\n\n".join(f"=== CANDIDATE {L} (source for transplants only) ===\n{cands[sec][L]}"
                                 for L in state["sections"][sec]["alive"] if L != best)
            pr = problems_of(checks[sec][best])
            eu = (f"WORD RANGE: {int(t * 0.9)}–{int(t * 1.1)} words (IDs excluded).\n\nIMPROVEMENTS TO APPLY:\n"
                  + "\n".join(f"- {x}" for x in v.get("improvements", []))
                  + ("\nTRANSPLANTS:\n" + "\n".join(f"- {x}" for x in v.get("transplants", [])) if v.get("transplants") else "")
                  + ("\nALSO FIX THESE AUTOMATED-CHECK PROBLEMS:\n" + "\n".join(f"- {p}" for p in pr[:20]) if pr else "")
                  + f"\n\nEVIDENCE (the only permitted facts):\n{ev_block(ids, P)}\n\n=== SECTION TO REVISE ===\n{cands[sec][best]}\n\n{others}")
            return R.call(f"edit_{sec}", 3, "edit", EDIT_SYS, eu, t + 100)
        jobs.append((sec, job))
    res = R.parallel(jobs)
    for sec, out in res.items():
        if isinstance(out, BudgetStop):
            state["budget_stop"] = str(out)
            out = None
        if isinstance(out, str) and out.strip():
            edited = out.strip()
            er = va.check(edited, P, sec)
            jr = final_reps[sec]
            if er["integrity_ok"] and score_rep(er) <= score_rep(jr):
                finals[sec], final_reps[sec] = edited, er
                state["sections"][sec]["edit"] = {"kept": True, "check_before": va.summary(jr), "check_after": va.summary(er)}
            else:
                state["sections"][sec]["edit"] = {"kept": False, "reason": "edited version failed integrity or scored worse",
                                                  "check_edited": va.summary(er), "check_judged": va.summary(jr)}
            if not dry:
                (D / f"section_v3_{sec}_edited.md").write_text(edited, encoding="utf-8")
        elif sec in state["sections"] and "edit" not in state["sections"][sec]:
            state["sections"][sec]["edit"] = {"kept": False, "reason": f"edit call failed: {out!r}"[:200]}
    for sec in finals:
        state["sections"][sec]["final_check"] = va.summary(final_reps[sec])
        if not dry:
            (D / f"section_v3_{sec}_final.md").write_text(finals[sec], encoding="utf-8")
    state["rounds"]["3_edits"] = {"seconds": round(time.time() - t3), "calls": len(jobs)}
    missing = [s for s in SECTIONS if s not in finals]
    if missing:
        state["missing_sections"] = missing
    joined = "\n\n".join(finals[s].strip() for s in SECTIONS if s in finals) + "\n"
    if not dry:
        (D / "ch01_draft_prestitch.md").write_text(joined, encoding="utf-8")
    # ================= round 4: stitch (never skipped while money remains) =================
    t4 = time.time()
    chapter, rep = joined, va.check(joined, P)
    pre = rep
    cmap = "\n".join(f"- {titles[k]} owns: {info[k]['purpose']} Key points: " + "; ".join(info[k]["points"]) for k in SECTIONS)
    tmap = "\n".join(f"- after {titles[k]}: {info[k]['transition']}" for k in SECTIONS)
    try:
        out = R.call("stitch", 4, "stitch", STITCH_SYS,
                     f"COVERAGE MAP (who owns what):\n{cmap}\n\nPLANNED TRANSITIONS:\n{tmap}\n\nCHAPTER OUTLINE (reference):\n{full_outline}\n\nDRAFT TO EDIT:\n{joined}",
                     sum(targets.values()) + 300)
        if out:
            st = out.strip() + "\n"
            sr = va.check(st, P)
            if sr["integrity_ok"] and score_rep(sr) <= score_rep(pre) + 10:
                chapter, rep = st, sr
                state["stitch"] = {"kept": True, "check_before": va.summary(pre), "check_after": va.summary(sr)}
            else:
                state["stitch"] = {"kept": False, "reason": "stitched text failed integrity or added problems", "check": va.summary(sr)}
            if not dry:
                (D / "ch01_draft_stitched_raw.md").write_text(st, encoding="utf-8")
        else:
            state["stitch"] = {"kept": False, "reason": "stitch call failed"}
    except BudgetStop as e:
        state["stitch"] = {"kept": False, "reason": f"budget: {e}"}
    state["rounds"]["4_stitch"] = {"seconds": round(time.time() - t4), "calls": 1}
    state["validation_before_revision"] = va.summary(rep)
    state["validation_before_revision_detail"] = rep
    # ================= round 5: validation + parallel revisions (≤ 2 rounds) =================
    t5 = time.time()
    state["revisions"] = []
    for rnd in (1, 2):
        parts = va.split_sections(chapter)
        reps = {s: va.check(parts[s], P, s) for s in SECTIONS if s in parts}
        bad = {s: r_ for s, r_ in reps.items() if problems_of(r_)}
        if not bad or dry:
            break
        if R.spent + 0.08 * len(bad) + (0.0 if skip_polish else 0.12) > BUDGET:
            state["revisions"].append({"round": rnd, "stopped": "no budget for revisions"})
            break
        def mk(s, r_):
            def job():
                _, _, ids = prompts[s]
                pr = problems_of(r_)
                ru = ("PROBLEMS TO FIX:\n" + "\n".join(f"- {p}" for p in pr[:30]) +
                      f"\n\nWORD RANGE: {int(targets[s] * 0.9)}–{int(targets[s] * 1.1)}\n\nEVIDENCE:\n{ev_block(ids, P)}\n\n=== SECTION ===\n{parts[s]}")
                return R.call(f"revise_r{rnd}_{s}", 5, "revise", REVISE_SYS, ru, targets[s])
            return job
        res = R.parallel([(s, mk(s, r_)) for s, r_ in bad.items()])
        for s, out in res.items():
            if isinstance(out, str) and out.strip():
                new = out.strip()
                nr = va.check(new, P, s)
                keep = nr["integrity_ok"] and score_rep(nr) < score_rep(bad[s])
                state["revisions"].append({"round": rnd, "section": s, "problems": len(problems_of(bad[s])),
                                           "after": len(problems_of(nr)), "kept": keep})
                if keep:
                    parts[s] = new.rstrip() + "\n"
            else:
                state["revisions"].append({"round": rnd, "section": s, "failed": repr(out)[:200]})
        chapter = "\n\n".join(parts[s].strip() for s in SECTIONS if s in parts) + "\n"
    rep = va.check(chapter, P)
    state["validation_after_revision"] = va.summary(rep)
    state["rounds"]["5_validation"] = {"seconds": round(time.time() - t5)}
    if not dry:
        (D / "ch01_draft_prepolish.md").write_text(chapter, encoding="utf-8")
    # ================= round 6: polish =================
    t6 = time.time()
    if skip_polish:
        state["polish"] = {"kept": False, "reason": "skipped to protect the budget (cut order: polish first)"}
    else:
        try:
            out = R.call("polish", 6, "polish", POLISH_SYS, chapter, sum(targets.values()))
            if out:
                pol = out.strip() + "\n"
                pr_ = va.check(pol, P)
                if pr_["integrity_ok"] and score_rep(pr_) <= score_rep(rep):
                    state["polish"] = {"kept": True, "check_before": va.summary(rep), "check_after": va.summary(pr_)}
                    chapter, rep = pol, pr_
                else:
                    state["polish"] = {"kept": False, "reason": "polished text failed integrity or scored worse",
                                       "check_polished": va.summary(pr_)}
                if not dry:
                    (D / "ch01_draft_polished_raw.md").write_text(pol, encoding="utf-8")
            else:
                state["polish"] = {"kept": False, "reason": "polish call failed"}
        except BudgetStop as e:
            state["polish"] = {"kept": False, "reason": f"budget: {e}"}
    state["rounds"]["6_polish"] = {"seconds": round(time.time() - t6)}
    state["final_validation"] = va.summary(rep)
    state["final_validation_detail"] = rep
    state["wall_clock_seconds"] = round(time.time() - t_start)
    if not dry:
        (D / "ch01_draft_v1.md").write_text(chapter, encoding="utf-8")
    state["calls"] = R.calls
    state["spent_usd"] = round(R.spent, 4)
    state["spend_by_stage"] = {k: round(v, 4) for k, v in R.stage_spend.items()}
    (D / ("pipeline_v3_estimate.json" if dry else "pipeline_state.json")).write_text(
        json.dumps(state, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return state, R


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    st, R = run(a.dry_run)
    if a.dry_run:
        by_round = {}
        for c in R.calls:
            by_round.setdefault(c["round"], []).append(c)
        wall = sum(max(c["est_seconds"] for c in cs) for cs in by_round.values())
        print(json.dumps({"projected_new_cost_usd": round(R.spent, 2),
                          "by_round": {r: {"calls": len(cs), "usd": round(sum(c["est_cost_usd"] for c in cs), 3),
                                           "longest_call_s": max(c["est_seconds"] for c in cs)} for r, cs in sorted(by_round.items())},
                          "projected_wall_clock_min": round(wall / 60, 1), "sequential_rounds": len(by_round)}, indent=1))
    else:
        for s in ("footnote.py", "make_report.py"):
            subprocess.run([sys.executable, "-I", str(D / s)])
        print(json.dumps({"spent_usd": st["spent_usd"], "wall_clock_min": round(st["wall_clock_seconds"] / 60, 1),
                          "budget_stop": st.get("budget_stop"), "decisions": st["decisions"]}, indent=1))
    print(f"[{ts()}] PIPELINE FINISHED", flush=True)
