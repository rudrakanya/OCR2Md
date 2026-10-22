"""API runner for the shared toolkit: background-mode Responses API with polling, a hard per-call wall-clock
deadline, keep-awake, one retry one effort level lower, exponential backoff on rate limits, budget accounting
from the chapter's own log folder (cfg LOG), and bounded parallelism.

Two chapters may run at once, so each process uses at most MAX_PAR = 5 concurrent calls (10 in total).
"""
from __future__ import annotations

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
from cfg import C, ROOT, PIPE  # noqa: E402

LOG = C.LOG
BUDGET = getattr(C, "BUDGET", 5.00)
RESERVE = getattr(C, "RESERVE", 0.90)
MAX_PAR = int(os.getenv("UDAY_MAX_PAR", "5"))
CALL_TIMEOUT = int(os.getenv("UDAY_CALL_TIMEOUT", "600"))     # orchestrator: 240
POLL = float(os.getenv("UDAY_POLL", "8"))                     # orchestrator: 2
MODEL = os.getenv("OPENAI_MODEL") or "gpt-6.1-sol"
FLAGSHIP = os.getenv("OPENAI_MODEL_FLAGSHIP") or "gpt-6-astra"   # style profile + author's pass
LOWER = {"max": "xhigh", "xhigh": "high", "high": "medium", "medium": "low", "low": "low"}
EFFORT = {"candidate": "high", "judge": "high", "stitch": "high", "edit": "medium", "revise": "medium", "polish": "medium",
          "verify": "medium", "fix": "medium", "reverify": "medium", "kbjudge": "medium", "expand": "medium"}
REASON = {"max": 23000, "xhigh": 17000, "high": 11000, "medium": 5000, "low": 2000}
SEC_PER_OUT_TOKEN = 0.0125      # observed in the Chapter 2 run (≈ 80 output tokens/s)


def ts():
    return time.strftime("%H:%M:%S")


def ntok(text: str) -> int:
    try:
        import tiktoken
        return len(tiktoken.get_encoding("o200k_base").encode(text))
    except Exception:  # noqa: BLE001
        return len(text) // 4


def load_key():
    if not os.getenv("OPENAI_API_KEY"):
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("OPENAI_API_KEY not found in the environment or .env")


class BudgetStop(Exception):
    pass


def keep_awake():
    try:
        import ctypes
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001)
        return True
    except Exception:  # noqa: BLE001
        return False


class Run:
    def __init__(self, dry):
        self.dry = dry
        choice = json.loads((PIPE / "model_choice.json").read_text(encoding="utf-8"))
        self.prices = choice["prices_per_1M"]
        self.price = self.prices[MODEL]
        self.lock = threading.Lock()
        self.calls, self.stage_spend = [], {}
        self.spent = self.prior = 0.0
        if not dry:
            for f in sorted(glob.glob(str(LOG / "*.json"))):
                self.prior += json.load(open(f, encoding="utf-8"))["meta"].get("cost_usd") or 0
            self.spent = self.prior
            load_key()
            from openai import OpenAI
            self.c = OpenAI(timeout=60, max_retries=0)
            keep_awake()

    def estimate(self, system, user, out_words, effort, model=None):
        pr = self.prices[model or MODEL]
        tin = ntok(system) + ntok(user)
        tout = int(out_words * 1.45) + REASON[effort]
        return tin, tout, tin / 1e6 * pr["input"] + tout / 1e6 * pr["output"], tout * SEC_PER_OUT_TOKEN

    def call(self, name, round_, kind, system, user, out_words, model=None, effort=None):
        model = model or MODEL
        effort = effort or EFFORT[kind]
        for attempt in (1, 2):
            tin, tout, est, secs = self.estimate(system, user, out_words, effort, model)
            rec = {"name": name, "stage": kind, "round": round_, "model": model, "effort": effort, "attempt": attempt,
                   "est_input_tokens": tin, "est_output_tokens": tout, "est_cost_usd": round(est, 4), "est_seconds": round(secs)}
            if self.dry:
                with self.lock:
                    self.calls.append(rec)
                    self.spent += est
                    self.stage_spend[kind] = self.stage_spend.get(kind, 0) + est
                return None
            with self.lock:
                if self.spent + est > BUDGET:
                    raise BudgetStop(f"before {name}: spent ${self.spent:.3f} + est ${est:.3f} > ${BUDGET}")
            try:
                return self._once(name, kind, system, user, effort, rec, est, model)
            except TimeoutError as e:
                print(f"[{ts()}] TIMEOUT {name} at effort {effort}: {e}; retrying once at {LOWER[effort]}", flush=True)
            except BudgetStop:
                raise
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
                    import random
                    d = delay * (0.5 + random.random())          # exponential backoff with jitter
                    print(f"[{ts()}] rate-limited; backing off {d:.1f}s", flush=True)
                    time.sleep(d)
                    delay = min(delay * 2, 120)
                    continue
                raise
        raise RuntimeError("rate-limited repeatedly")

    def _once(self, name, kind, system, user, effort, rec, est, model=None):
        params = {"model": model or MODEL, "reasoning": {"effort": effort},
                  "input": [{"role": "system", "content": system}, {"role": "user", "content": user}], "max_output_tokens": 64000}
        t0 = time.time()
        print(f"[{ts()}] calling {name} (effort {effort}; est ${est:.3f}; spent ${self.spent:.3f})", flush=True)
        r = self._create(params)
        rid = r.id
        deadline = t0 + CALL_TIMEOUT
        while r.status in ("queued", "in_progress"):
            if time.time() > deadline:
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
                raise TimeoutError(f"no result after {CALL_TIMEOUT}s (response {rid} cancelled)")
            time.sleep(POLL)
            for _ in range(5):
                if time.time() > deadline:
                    break
                try:
                    r = self.c.responses.retrieve(rid)
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
            pr = self.prices.get(params["model"], self.price)
            cost = u.input_tokens / 1e6 * pr["input"] + u.output_tokens / 1e6 * pr["output"]
            rec.update(input_tokens=u.input_tokens, output_tokens=u.output_tokens, reasoning_tokens=rt)
        else:
            cost = 0.0 if status == "failed" else est
        with self.lock:
            self.spent += cost
            self.stage_spend[kind] = self.stage_spend.get(kind, 0) + cost
            rec.update(cost_usd=round(cost, 4), seconds=round(time.time() - t0, 1), status=status, response_id=rid,
                       spent_so_far=round(self.spent, 4))
            LOG.mkdir(parents=True, exist_ok=True)
            n = len(list(LOG.glob("*.json"))) + 1
            sfx = "" if status == "completed" else f"_{status}"
            (LOG / f"{n:03d}_{name}{sfx}.json").write_text(json.dumps(
                {"meta": rec, "request": params, "response_text": text}, ensure_ascii=False, indent=1), encoding="utf-8")
            self.calls.append(rec)
            print(f"[{ts()}] done {name} ({status}, {rec['effort']}) in {time.time() - t0:.0f}s ${cost:.3f} — spent ${self.spent:.3f}", flush=True)
            if self.spent >= BUDGET:
                raise BudgetStop(f"after {name}: spend ${self.spent:.3f} reached ${BUDGET}")

    def parallel(self, jobs):
        out = {}
        with cf.ThreadPoolExecutor(max_workers=min(MAX_PAR, max(1, len(jobs)))) as ex:
            futs = {ex.submit(fn): k for k, fn in jobs}
            for f in cf.as_completed(futs):
                try:
                    out[futs[f]] = f.result()
                except Exception as e:  # noqa: BLE001
                    out[futs[f]] = e
        return out


def parse_json(text):
    m = re.search(r"\{.*\}", text or "", re.S)
    try:
        return json.loads(m.group(0)) if m else None
    except Exception:  # noqa: BLE001
        return None
