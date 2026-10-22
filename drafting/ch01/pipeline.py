"""Quality pipeline for Chapter 1 (v2: resumable, parallel candidates, budget reserve).

Per section (sections sequential): N candidates in parallel -> code checks (discard failed citation
integrity) -> judge -> edit (revert if checks get worse) -> running summary from the final text.
Then: stitch -> full validation -> up to 2 revision rounds for failing sections -> polish (kept only if it
validates no worse) -> ch01_draft_v1.md, footnoted version, report data.

Budget rules (user, 2026-10-13):
  * hard stop when actual spend reaches $5.00;
  * $0.90 held in reserve for stitch + validation + footnotes + polish;
  * before each section, re-project from actual spend; if finishing would eat into the reserve, the
    remaining sections drop to a single candidate (still judged and edited);
  * if money still runs short: first skip the polish, then skip the edit pass on remaining sections;
    never skip the stitch, the validation, or writing the three output files.
Effort: candidates and judge "max"; edit, summary, stitch, revise, polish "high".
Resume: candidates/<sec>_<L>.md, judge_<sec>.json, section_<sec>_final.md and summary_<sec>.txt are
reused if present; prior spend is read back from api_log/.

  python -I "drafting/ch01/pipeline.py" --dry-run
  python -u -I "drafting/ch01/pipeline.py"
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import glob
import json
import os
import re
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
BUDGET = 5.00
RESERVE = 0.90
MAX_CALL_SECONDS = 2400
# Three earlier synchronous requests (one in the first run, two attempts of cand_1.1_B) never returned;
# OpenAI may have billed them. Counted conservatively against the $5 hard limit until the user confirms
# otherwise (override with env CH01_UNACCOUNTED_USD).
UNACCOUNTED = float(os.getenv("CH01_UNACCOUNTED_USD", "0.82"))
MODEL_DEFAULT = "gpt-6.1-sol"
EFFORT = {"candidate": "max", "judge": "max", "edit": "high", "summary": "high", "stitch": "high",
          "revise": "high", "polish": "high"}
# hidden reasoning allowance per kind (estimates only). candidate/judge from the first real call (22.8k).
ALLOW = {"candidate": 23000, "judge": 20000, "edit": 9000, "summary": 2500, "stitch": 12000,
         "revise": 9000, "polish": 12000}
OPENINGS = [
    "OPENING FOR THIS CANDIDATE: lead with the place — a concrete physical scene drawn from the evidence.",
    "OPENING FOR THIS CANDIDATE: lead with a source — a short, exactly quoted phrase from one evidence item, attributed.",
    "OPENING FOR THIS CANDIDATE: lead with a dated fact from the evidence, stated plainly in one short sentence.",
]


def ts():
    return time.strftime("%H:%M:%S")


class BudgetStop(Exception):
    pass


class CallFailed(Exception):
    pass


class Run:
    def __init__(self, dry):
        self.dry = dry
        self.model = os.getenv("OPENAI_MODEL") or MODEL_DEFAULT
        choice = json.loads((D / "model_choice.json").read_text(encoding="utf-8"))
        self.price = choice["prices_per_1M"].get(self.model)
        if self.price is None:
            sys.exit(f"no price on record for {self.model}")
        self.lock = threading.Lock()
        self.calls, self.stage_spend = [], {}
        self.spent = 0.0 if dry else UNACCOUNTED
        if not dry:
            for f in sorted(glob.glob(str(LOG / "*.json"))):     # resume: count prior spend
                m = json.load(open(f, encoding="utf-8"))["meta"]
                self.spent += m.get("cost_usd") or 0
                self.stage_spend[m["stage"]] = self.stage_spend.get(m["stage"], 0) + (m.get("cost_usd") or 0)
                self.calls.append(m)
            dr.load_key()
            from openai import OpenAI
            self.c = OpenAI(timeout=120, max_retries=2)   # short timeouts: create/retrieve/cancel are quick in background mode

    # average actual cost per kind (falls back to the estimate)
    def avg_cost(self, kind, fallback):
        xs = [c["cost_usd"] for c in self.calls if c.get("kind") == kind and c.get("cost_usd")]
        if kind in ("edit", "summary", "stitch", "revise", "polish"):   # only count calls made at "high"
            xs = [c["cost_usd"] for c in self.calls if c.get("kind") == kind and c.get("cost_usd") and c.get("effort") == EFFORT[kind]]
        return sum(xs) / len(xs) if xs else fallback

    def est(self, system, user, kind, out_words):
        tin = dr.ntok(system) + dr.ntok(user)
        tout = int(out_words * 1.45) + ALLOW[kind]
        return tin, tout, tin / 1e6 * self.price["input"] + tout / 1e6 * self.price["output"]

    def call(self, name, stage, kind, system, user, out_words, max_out=64000):
        tin, tout, est = self.est(system, user, kind, out_words)
        rec = {"name": name, "stage": stage, "kind": kind, "model": self.model, "effort": EFFORT[kind],
               "est_input_tokens": tin, "est_output_tokens": tout, "est_cost_usd": round(est, 4)}
        if self.dry:
            with self.lock:
                self.calls.append(rec)
                self.stage_spend[stage] = self.stage_spend.get(stage, 0) + est
                self.spent += est
            return None
        with self.lock:
            if self.spent + est > BUDGET:
                raise BudgetStop(f"before {name}: spent ${self.spent:.3f}, next call est ${est:.3f}, budget ${BUDGET}")
        params = {"model": self.model, "reasoning": {"effort": EFFORT[kind]},
                  "input": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                  "max_output_tokens": max_out}
        for attempt in (1, 2):
            try:
                return self._once(name, stage, kind, params, rec, est, attempt)
            except CallFailed as e:
                print(f"[{ts()}] FAILED {name} attempt {attempt}: {e}", flush=True)
                with self.lock:
                    if self.spent + est > BUDGET:
                        raise BudgetStop(f"{name} failed and no budget for a retry (spent ${self.spent:.3f})")
        return ""   # failed twice: callers degrade gracefully (candidate dropped, edit/polish skipped, …)

    def _once(self, name, stage, kind, params, rec, est, attempt):
        t0 = time.time()
        print(f"[{ts()}] calling {name} (effort {EFFORT[kind]}; est ${est:.3f}; spent ${self.spent:.3f})", flush=True)
        # Background mode: the request returns an id at once and we poll, so no long-held connection can
        # hang (two synchronous max-effort calls hung for 15+ min). A call still running after
        # MAX_CALL_SECONDS is cancelled explicitly and charged at its estimate.
        r = self.c.responses.create(background=True, **params)
        rid = r.id
        while r.status in ("queued", "in_progress"):
            if time.time() - t0 > MAX_CALL_SECONDS:
                try:
                    self.c.responses.cancel(rid)
                except Exception:
                    pass
                self._charge(name, stage, kind, params, dict(rec), None, est, t0, rid, "cancelled_timeout", "")
                raise CallFailed(f"no result after {MAX_CALL_SECONDS}s (response {rid} cancelled; charged est ${est:.3f})")
            time.sleep(10)
            for _ in range(5):
                try:
                    r = self.c.responses.retrieve(rid)
                    break
                except Exception as e:  # transient network error while polling
                    print(f"[{ts()}] poll error {type(e).__name__}; retrying", flush=True)
                    time.sleep(15)
        text = r.output_text if r.status == "completed" else ""
        self._charge(name, stage, kind, params, rec, r.usage, est, t0, rid, r.status, text)
        if r.status != "completed" or not text.strip():
            raise CallFailed(f"status {r.status} ({getattr(r, 'incomplete_details', None)})")
        return text

    def _charge(self, name, stage, kind, params, rec, u, est, t0, rid, status, text):
        if u is not None:
            rt = getattr(getattr(u, "output_tokens_details", None), "reasoning_tokens", None)
            cost = u.input_tokens / 1e6 * self.price["input"] + u.output_tokens / 1e6 * self.price["output"]
            rec.update(input_tokens=u.input_tokens, output_tokens=u.output_tokens, reasoning_tokens=rt)
        else:
            cost = est
        with self.lock:
            self.spent += cost
            self.stage_spend[stage] = self.stage_spend.get(stage, 0) + cost
            rec.update(cost_usd=round(cost, 4), seconds=round(time.time() - t0, 1), status=status,
                       response_id=rid, spent_so_far=round(self.spent, 4))
            LOG.mkdir(exist_ok=True)
            n = len(list(LOG.glob("*.json"))) + 1
            suffix = "" if status == "completed" else f"_{status}"
            (LOG / f"{n:03d}_{name}{suffix}.json").write_text(json.dumps(
                {"meta": rec, "request": params, "response_text": text}, ensure_ascii=False, indent=1), encoding="utf-8")
            self.calls.append(rec)
            print(f"[{ts()}] done {name} ({status}) in {time.time() - t0:.0f}s, ${cost:.3f} (spent ${self.spent:.3f})", flush=True)
            if self.spent >= BUDGET:
                raise BudgetStop(f"after {name}: spend ${self.spent:.3f} reached the ${BUDGET} budget")


# ---------------------------------------------------------------------------------------------
JUDGE_SYS = """You are a demanding editor judging candidate drafts of one section of a non-fiction chapter about Udaypur.
Score each candidate 1–10 on: fidelity (only supplied evidence; correct citations; conflicts unresolved), coverage (the section's key points and conflicts), prose (specific, varied sentences; strong concrete opening line; no banned phrases), voice (consistent with the earlier sections' summary and the writer brief), transition (into the next section).
The automated check report for each candidate is supplied: weigh uncited claims and fabrication flags heavily under fidelity.
Pick the best candidate (if only one is supplied, judge it alone). Then give 5–8 concrete, line-level improvements to apply to it (quote the sentence or phrase to change and say exactly how). You may point to a stronger paragraph in another candidate to transplant, saying why — but every transplanted sentence must keep its bracketed IDs.
Improvements must not introduce any fact that is not in the evidence.
Return ONLY JSON: {"scores": {"A": {"fidelity":n,"coverage":n,"prose":n,"voice":n,"transition":n,"total":n}, ...}, "best": "A", "improvements": ["...", ...], "transplants": ["..."], "rationale": "..."}"""

EDIT_SYS = """You revise one section of a non-fiction chapter about Udaypur. Apply ONLY the listed improvements (and any listed transplant).
STRICT: add no facts, dates, names or numbers; do not remove, alter or invent any bracketed evidence ID — every factual sentence keeps its IDs; do not change text inside quotation marks except to delete a whole quotation together with its sentence; keep the heading line exactly; stay within the word range given.
Return the full revised section in Markdown and nothing else."""

SUMMARY_SYS = """Summarise the given section of a chapter in 150–250 words of plain prose for the writer of the next section: what it established, which sources and conflicts it presented, which names it introduced (including whether Vijay Manohar Tiwari has been named), its closing note. No evidence IDs. Return only the summary."""

REVISE_SYS = """You fix specific validation problems in one section of a non-fiction chapter about Udaypur.
Fix ONLY the listed problems: cite uncited factual sentences with an ID from the supplied evidence or delete the claim; replace any non-verbatim quotation with the exact words of the cited item's QUOTE or paraphrase it; delete or re-cite any year or name that does not appear in the cited items; adjust length if asked. Add no new facts. Keep all other text, IDs and the heading unchanged.
Return the full corrected section in Markdown and nothing else."""

POLISH_SYS = """Polish this chapter at sentence level: cut repetition, tighten rhythm, vary sentence openings, remove any banned phrase ("nestled", "tapestry", "testament to", "stands as", "rich history", "steeped in", "delve", "bustling", "timeless", "hidden gem", "in conclusion") and filler rhetorical questions.
STRICT: no new facts, dates, names or numbers; every bracketed evidence ID stays attached to its claim, unchanged; text inside quotation marks unchanged; headings unchanged; keep total length within 3,800–4,200 words (IDs excluded).
Return only the full chapter in Markdown."""


def ev_block(ids, P):
    return "\n\n".join(dr.fmt_item(P[i]) for i in ids)


def problems_of(rep):
    out = []
    out += [f"invalid ID {x}" for x in rep["invalid_ids"]]
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
    except Exception:
        return None


def rd(p):
    return p.read_text(encoding="utf-8") if p.exists() else None


def wr(p, t, dry):
    if not dry:
        p.write_text(t, encoding="utf-8")


def recover_judge(sec):
    """judge verdict for a section: judge_<sec>.json, else the latest logged judge call (resume)."""
    j = D / f"judge_{sec}.json"
    if j.exists():
        return json.loads(j.read_text(encoding="utf-8"))
    logs = sorted(glob.glob(str(LOG / f"*_judge_{sec}.json")))
    if logs:
        v = parse_json(json.load(open(logs[-1], encoding="utf-8"))["response_text"])
        if v:
            j.write_text(json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
            return v
    return None


def recover_candidates(sec, labels, dry):
    """candidate texts for a section: candidates/<sec>_<L>.md, else logged responses (resume)."""
    out = {}
    for L in labels:
        p = CAND / f"{sec}_{L}.md"
        if p.exists():
            out[L] = p.read_text(encoding="utf-8")
            continue
        logs = sorted(glob.glob(str(LOG / f"*_cand_{sec}_{L}.json")))
        if logs and not dry:
            body, _ = dr.split_summary(json.load(open(logs[-1], encoding="utf-8"))["response_text"])
            CAND.mkdir(exist_ok=True)
            p.write_text(body, encoding="utf-8")
            out[L] = body
    return out


# ---------------------------------------------------------------------------------------------
def project(R, sections_left, n_cand, targets, P, cov, secs, titles, full_outline):
    """projected cost to finish all remaining sections with n_cand candidates (excluding finishing)."""
    c = R.avg_cost("candidate", 0.27)
    j = R.avg_cost("judge", 0.25)
    e = R.avg_cost("edit", 0.12)
    s = R.avg_cost("summary", 0.03)
    return sum(n_cand * c + j + e + s for _ in sections_left), (c, j, e, s)


def finishing_cost(R):
    return R.avg_cost("stitch", 0.20) + 2 * R.avg_cost("revise", 0.10) + R.avg_cost("polish", 0.20)


def run(dry, n_cand):
    print(f"[{ts()}] pipeline v2 start (dry={dry}, candidates={n_cand})", flush=True)
    full_outline, head, secs, targets, titles = dr.outline_sections()
    P = dr.pack()
    cov = json.loads((D / "coverage.json").read_text(encoding="utf-8"))
    R = Run(dry)
    prev = json.loads(rd(D / "pipeline_state.json") or "{}") if not dry else {}
    state = {"model": R.model, "effort": EFFORT, "sections": prev.get("sections", {}), "n_candidates": n_cand,
             "budget": BUDGET, "reserve": RESERVE, "decisions": prev.get("decisions", []), "resumed_from_spend": round(R.spent, 4)}
    skip_polish = False
    skip_edit = False
    finals, summaries = {}, []
    order = dr.SECTIONS
    try:
        for si, sec in enumerate(order):
            t = targets[sec]
            final_p, summ_p = D / f"section_{sec}_final.md", D / f"summary_{sec}.txt"
            if not dry and final_p.exists() and summ_p.exists():          # resume a finished section
                finals[sec] = final_p.read_text(encoding="utf-8")
                summaries.append(f"{titles[sec]}: {summ_p.read_text(encoding='utf-8').strip()}")
                print(f"[{ts()}] section {sec}: resumed from saved final", flush=True)
                continue
            # ---- budget re-projection before the section
            left = order[si:]
            need2, unit = project(R, left, n_cand, targets, P, cov, secs, titles, full_outline)
            avail = BUDGET - RESERVE - R.spent
            if not dry and need2 > avail and n_cand > 1:
                need1, _ = project(R, left, 1, targets, P, cov, secs, titles, full_outline)
                msg = (f"before {sec}: spent ${R.spent:.2f}; projected ${need2:.2f} for {len(left)} section(s) at {n_cand} candidates "
                       f"> ${avail:.2f} available outside the ${RESERVE} reserve -> 1 candidate for sections {', '.join(left)} "
                       f"(projected ${need1:.2f})")
                n_cand = 1
                state["decisions"].append(msg)
                print(f"[{ts()}] ADAPT: {msg}", flush=True)
                if need1 > avail and not skip_polish:
                    skip_polish = True
                    m2 = f"before {sec}: even 1 candidate projects ${need1:.2f} > ${avail:.2f}; polish will be skipped"
                    state["decisions"].append(m2)
                    print(f"[{ts()}] ADAPT: {m2}", flush=True)
                    if need1 > avail + R.avg_cost("polish", 0.20):
                        skip_edit = True
                        m3 = f"before {sec}: still short; edit pass skipped for sections {', '.join(left)}"
                        state["decisions"].append(m3)
                        print(f"[{ts()}] ADAPT: {m3}", flush=True)
            system, base_user, ids = dr.section_prompt(sec, full_outline, secs, targets, titles, P, cov, "\n\n".join(summaries))
            labels = list("ABC"[:n_cand])
            have = recover_candidates(sec, labels, dry)
            # keep any extra candidates that already exist (e.g. B written before a downgrade)
            for L in "ABC":
                if L not in labels and (CAND / f"{sec}_{L}.md").exists():
                    labels.append(L)
                    have[L] = (CAND / f"{sec}_{L}.md").read_text(encoding="utf-8")
            todo = [L for L in labels if L not in have]
            if todo:
                def gen(L):
                    out = R.call(f"cand_{sec}_{L}", "candidates", "candidate", system,
                                 base_user + "\n" + OPENINGS["ABC".index(L)], t + 250)
                    if out is None:
                        return L, f"## {titles[sec]}\n" + ("Lorem ipsum dolor [C01-GANGULY-006]. " * (t // 4))
                    body, _ = dr.split_summary(out)
                    if not dry:
                        CAND.mkdir(exist_ok=True)
                        (CAND / f"{sec}_{L}.md").write_text(body, encoding="utf-8")
                    return L, body
                with cf.ThreadPoolExecutor(max_workers=len(todo)) as ex:      # candidates in parallel
                    for L, body in ex.map(gen, todo):
                        if body is not None:
                            have[L] = body
                if not have:
                    raise BudgetStop(f"no candidate could be generated for section {sec}")
            labels = sorted(have)
            cands = [have[L] for L in labels]
            reps = [va.check(c, P, sec) for c in cands]
            sec_state = {"candidates": [{"label": labels[k], "words": reps[k]["words"].get(sec),
                                         "integrity_ok": reps[k]["integrity_ok"], "check": va.summary(reps[k])}
                                        for k in range(len(cands))]}
            alive = [k for k in range(len(cands)) if reps[k]["integrity_ok"]]
            if not alive:
                alive = [min(range(len(cands)), key=lambda k: score_rep(reps[k]))]
                sec_state["note"] = "no candidate passed citation integrity; best-scoring one kept and its problems passed to the editor"
            # ---- judge
            verdict = None if dry else recover_judge(sec)
            if verdict is None:
                prev_tail = list(finals.values())[-1][-2500:] if finals else ""
                nxt = titles[order[si + 1]] if si + 1 < len(order) else "none — last section; lead to Chapter 2"
                judge_user = (f"WRITER BRIEF:\n{dr.WRITER_BRIEF}\n\nSECTION BRIEF:\n{secs[sec]}\n\nWORD TARGET: {t} (±10%)\n\n"
                              f"SUMMARY OF EARLIER SECTIONS:\n{chr(10).join(summaries) or '(none)'}\n\n"
                              f"END OF PREVIOUS SECTION (for voice and transition):\n{prev_tail or '(none)'}\n\n"
                              f"NEXT SECTION: {nxt}\n\nEVIDENCE (for checking fidelity):\n{ev_block(ids, P)}\n\n"
                              + "\n\n".join(f"=== CANDIDATE {labels[k]} ===\nAUTOMATED CHECKS: {json.dumps(problems_of(reps[k])[:25], ensure_ascii=False)}\n\n{cands[k]}"
                                            for k in alive))
                jout = R.call(f"judge_{sec}", "judge", "judge", JUDGE_SYS, judge_user, 700)
                verdict = parse_json(jout) if jout else None
                if verdict and not dry:
                    (D / f"judge_{sec}.json").write_text(json.dumps(verdict, ensure_ascii=False, indent=1), encoding="utf-8")
            verdict = verdict or {"best": labels[alive[0]], "improvements": [], "scores": {}}
            best = verdict.get("best", labels[alive[0]])
            best_k = labels.index(best) if best in labels else alive[0]
            if best_k not in alive:
                best_k = alive[0]
            sec_state["judge"] = verdict
            judged, jrep = cands[best_k], reps[best_k]
            # ---- edit (skippable only under the money-short rule)
            final, erep = judged, jrep
            if skip_edit:
                sec_state["edit"] = {"kept": False, "reason": "edit pass skipped to protect the finishing reserve"}
            else:
                transplant_src = "\n\n".join(f"=== CANDIDATE {labels[k]} (source for transplants only) ===\n{cands[k]}"
                                             for k in alive if k != best_k)
                edit_user = (f"WORD RANGE: {int(t * 0.9)}–{int(t * 1.1)} words (IDs excluded).\n\nIMPROVEMENTS TO APPLY:\n"
                             + "\n".join(f"- {x}" for x in verdict.get("improvements", []))
                             + ("\nTRANSPLANTS:\n" + "\n".join(f"- {x}" for x in verdict.get("transplants", [])) if verdict.get("transplants") else "")
                             + ("\nALSO FIX THESE AUTOMATED-CHECK PROBLEMS:\n" + "\n".join(f"- {p}" for p in problems_of(jrep)[:20]) if problems_of(jrep) else "")
                             + f"\n\nEVIDENCE (the only permitted facts):\n{ev_block(ids, P)}\n\n=== SECTION TO REVISE ===\n{judged}\n\n{transplant_src}")
                eout = R.call(f"edit_{sec}", "edit", "edit", EDIT_SYS, edit_user, t + 100)
                if eout:
                    edited = eout.strip()
                    er = va.check(edited, P, sec)
                    if er["integrity_ok"] and score_rep(er) <= score_rep(jrep):
                        final, erep = edited, er
                        sec_state["edit"] = {"kept": True, "check_before": va.summary(jrep), "check_after": va.summary(er)}
                    else:
                        sec_state["edit"] = {"kept": False, "reason": "edited version failed integrity or scored worse on the checks",
                                             "check_edited": va.summary(er)}
                    wr(D / f"section_{sec}_edited.md", edited, dry)
            finals[sec] = final
            wr(final_p, final, dry)
            sec_state["final_check"] = va.summary(erep)
            sout = R.call(f"summary_{sec}", "summary", "summary", SUMMARY_SYS, final, 230)
            summ = (sout or "(summary unavailable — next section drafted without it)").strip()
            wr(summ_p, summ, dry)
            summaries.append(f"{titles[sec]}: {summ}")
            state["sections"][sec] = sec_state
            save_state(state, R)
    except BudgetStop as e:
        state["budget_stop"] = str(e)
        print(f"[{ts()}] BUDGET STOP: {e}", flush=True)
    # ===================== finishing (always produces the three files) =====================
    missing = [s for s in order if s not in finals]
    if missing:
        state["missing_sections"] = missing
    joined = "\n\n".join(finals[s].strip() for s in order if s in finals) + "\n"
    wr(D / "ch01_draft_prestitch.md", joined, dry)
    chapter, rep = joined, va.check(joined, P)
    pre_rep = rep
    # ---- stitch (never skipped while any money remains)
    try:
        sout = R.call("stitch", "stitch", "stitch", dr.STITCH_BRIEF,
                      f"CHAPTER OUTLINE (reference):\n{full_outline}\n\nDRAFT TO EDIT:\n{joined}", sum(targets.values()) + 300)
        if sout:
            st_text = sout.strip() + "\n"
            srep = va.check(st_text, P)
            if srep["integrity_ok"] and score_rep(srep) <= score_rep(pre_rep) + 10:
                chapter, rep = st_text, srep
                state["stitch"] = {"kept": True, "check_before": va.summary(pre_rep), "check_after": va.summary(srep)}
            else:
                state["stitch"] = {"kept": False, "reason": "stitched text failed integrity or added problems", "check": va.summary(srep)}
    except BudgetStop as e:
        state["stitch"] = {"kept": False, "reason": f"budget: {e}"}
    state["validation_before_revision"] = va.summary(rep)
    state["validation_before_revision_detail"] = rep
    # ---- Phase 3 revisions: failing sections only, max 2 rounds, only while money remains
    state["revisions"] = state.get("revisions", [])
    for rnd in (1, 2):
        parts = va.split_sections(chapter)
        bad = {s: va.check(parts[s], P, s) for s in order if s in parts}
        bad = {s: r_ for s, r_ in bad.items() if problems_of(r_)}
        if not bad or dry:
            break
        try:
            for s, r_ in bad.items():
                reserve_left = R.avg_cost("polish", 0.20) if not skip_polish else 0
                if R.spent + R.avg_cost("revise", 0.10) + reserve_left > BUDGET:
                    raise BudgetStop("no money left for further revision calls")
                _, _, ids = dr.section_prompt(s, full_outline, secs, targets, titles, P, cov, "")
                pr = problems_of(r_)
                ru = ("PROBLEMS TO FIX:\n" + "\n".join(f"- {p}" for p in pr[:30]) +
                      f"\n\nWORD RANGE: {int(targets[s] * 0.9)}–{int(targets[s] * 1.1)}\n\nEVIDENCE:\n{ev_block(ids, P)}\n\n=== SECTION ===\n{parts[s]}")
                out = R.call(f"revise_r{rnd}_{s}", "revise", "revise", REVISE_SYS, ru, targets[s])
                if out:
                    new = out.strip()
                    nr = va.check(new, P, s)
                    keep = nr["integrity_ok"] and score_rep(nr) < score_rep(r_)
                    state["revisions"].append({"round": rnd, "section": s, "problems": len(pr),
                                               "after": len(problems_of(nr)), "kept": keep})
                    if keep:
                        parts[s] = new.rstrip() + "\n"
        except BudgetStop as e:
            state["revisions"].append({"round": rnd, "stopped": str(e)})
            chapter = "\n\n".join(parts[s].strip() for s in order if s in parts) + "\n"
            break
        chapter = "\n\n".join(parts[s].strip() for s in order if s in parts) + "\n"
    rep = va.check(chapter, P)
    state["validation_after_revision"] = va.summary(rep)
    wr(D / "ch01_draft_prepolish.md", chapter, dry)
    # ---- polish (first thing cut when money is short)
    if skip_polish:
        state["polish"] = {"kept": False, "reason": "skipped to protect the budget"}
    else:
        try:
            pout = R.call("polish", "polish", "polish", POLISH_SYS, chapter, sum(targets.values()))
            if pout:
                pol = pout.strip() + "\n"
                prep = va.check(pol, P)
                if prep["integrity_ok"] and score_rep(prep) <= score_rep(rep):
                    state["polish"] = {"kept": True, "check_before": va.summary(rep), "check_after": va.summary(prep)}
                    chapter, rep = pol, prep
                else:
                    state["polish"] = {"kept": False, "reason": "polished text failed integrity or scored worse",
                                       "check_polished": va.summary(prep)}
        except BudgetStop as e:
            state["polish"] = {"kept": False, "reason": f"budget: {e}"}
    state["final_validation"] = va.summary(rep)
    state["final_validation_detail"] = rep
    wr(D / "ch01_draft_v1.md", chapter, dry)
    save_state(state, R)
    return state, R


def save_state(state, R):
    state["calls"] = R.calls
    state["spent_usd"] = round(R.spent, 4)
    state["spend_by_stage"] = {k: round(v, 4) for k, v in R.stage_spend.items()}
    name = "pipeline_estimate.json" if R.dry else "pipeline_state.json"
    (D / name).write_text(json.dumps(state, ensure_ascii=False, indent=1, default=str), encoding="utf-8")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--candidates", type=int, default=2)
    a = ap.parse_args()
    st, R = run(a.dry_run, a.candidates)
    if not a.dry_run:
        import subprocess
        for s in ("footnote.py", "make_report.py"):
            subprocess.run([sys.executable, "-I", str(D / s)])
    print(json.dumps({"model": R.model, "spent_or_estimate_usd": round(R.spent, 3), "by_stage": st["spend_by_stage"],
                      "calls": len(R.calls), "budget_stop": st.get("budget_stop"), "decisions": st.get("decisions")}, indent=1))
    print(f"[{ts()}] PIPELINE FINISHED", flush=True)
