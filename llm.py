#!/usr/bin/env python3
"""
llm.py — one chat client, one retry policy, one JSON parser.

v1's `complete()` lived inside draft_chapter.py. v2 adds six more modules that
all need the same call — dossiers, contextualisation, entity extraction, claim
extraction, verification, the eval judges — and copying a backoff classifier
seven times is how they drift apart. It lives here; draft_chapter.py imports it
rather than defining its own.

The retry classifier is the part worth preserving verbatim. Running sections
concurrently makes HTTP 429 the normal case rather than an exception, so
throttling gets its own budget: more attempts, a longer ceiling, and jitter so
parallel workers backing off together do not retry in lockstep and collide
again. Timeouts and dropped connections are as transient as throttling — a
ReadTimeout lost chapter 3 of v1's first parallel run by falling through to the
short non-transient budget.

    from llm import get_client, complete, complete_json, parallel

    text, finish = complete(client, model, msgs, max_tokens=2000)
    data = complete_json(client, model, msgs, max_tokens=8000)   # dict or list
    results = parallel(fn, jobs, workers=4)
"""
import json
import os
import random
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()
load_dotenv(Path(__file__).resolve().parent / ".env", override=False)

DEFAULT_MODEL = os.environ.get("MISTRAL_CHAT_MODEL", "mistral-large-latest")


class LLMError(RuntimeError):
    pass


class Truncated(LLMError):
    """The model hit its token ceiling. Distinct from a parse failure.

    v1 surfaced this as an opaque ValueError from json.loads when a 6,000-token
    ceiling cut a 25,643-character hierarchy mid-object. Naming it means the
    caller can raise the ceiling instead of guessing at the prompt.
    """


def get_client():
    key = os.environ.get("MISTRAL_API_KEY")
    if not key:
        raise LLMError("MISTRAL_API_KEY is not set. Put it in a .env file (see .env.example).")
    return Mistral(api_key=key)


class QuotaExhausted(LLMError):
    """The account is out of credit or the plan's allowance is spent.

    Emphatically NOT a rate limit, though both can arrive as 429. Throttling
    clears in seconds; an exhausted quota clears when the billing period does.
    Retrying it is pure waste, and — worse — it degrades results silently: a
    verification pass whose calls all fail marks every claim unverified, and a
    pipeline that treats unverified as unsupported will delete correct prose
    because the account ran out of money. That is exactly what happened to
    chapter 1, and nothing in the log said so, because the retry handler
    recorded only the exception's class name.
    """


_QUOTA_MARKERS = (
    "quota", "insufficient", "credit", "billing", "payment required",
    "exhausted", "usage limit", "plan limit", "subscription",
    "service_tier_capacity", "no capacity", "402",
)


def _classify(exc):
    """(is_transient, is_throttled, is_quota) for one exception."""
    msg = str(exc).lower()
    quota = any(w in msg for w in _QUOTA_MARKERS) or "401" in msg or "403" in msg
    throttled = (not quota) and ("429" in msg or "rate limit" in msg
                                 or "rate_limit" in msg)
    transient = (not quota) and (throttled or any(w in msg for w in (
        "timeout", "timed out", "connection", "reset", "temporarily",
        "502", "503", "504", "overloaded", "unavailable")))
    return transient, throttled, quota


def _transient(exc):
    """Back-compat shim: (is_transient, is_throttled)."""
    t, th, _q = _classify(exc)
    return t, th


_RETRY_AFTER_RE = re.compile(r"retry[-_ ]?after[\"'\s:=]+(\d+(?:\.\d+)?)", re.I)


def _retry_after(exc):
    """Seconds the server asked us to wait, if it said. Beats guessing."""
    m = _RETRY_AFTER_RE.search(str(exc))
    if m:
        try:
            return max(0.0, min(300.0, float(m.group(1))))
        except ValueError:
            pass
    return None


class RateLimiter:
    """One process-wide adaptive throttle in front of every model call.

    Backoff alone is the wrong shape for this problem. It is *reactive*: each
    429 costs a wasted request, a wasted round trip and then a sleep, and with
    several workers the failures arrive in bursts because everyone retries into
    the same wall. Drafting one chapter took 19 retries and still lost the
    chapter twice.

    The limit is per ACCOUNT, not per module, so throttling inside each caller
    cannot work either — retrieval judging, claim extraction and drafting all
    draw on the same budget. Hence a single shared limiter.

    The control law is AIMD, the same idea TCP uses for congestion:

        additive increase       every `probe_after` consecutive successes, allow
                                a little more throughput (+`step` req/s)
        multiplicative decrease on a 429, halve the rate immediately

    That converges on whatever the account actually permits without being told,
    and it holds there — so in steady state requests are *paced* rather than
    rejected, and a 429 becomes rare instead of routine.
    """

    def __init__(self, rps=None, min_rps=0.15, max_rps=None, step=0.05, probe_after=12):
        env = os.environ.get("LLM_MAX_RPS")
        self.rps = float(rps if rps is not None else (env or 1.2))
        self.min_rps = min_rps
        self.max_rps = float(max_rps if max_rps is not None else max(self.rps, 4.0))
        self.step = step
        self.probe_after = probe_after
        self._lock = threading.Lock()
        self._next_at = 0.0
        self._ok_streak = 0
        self.waited = 0.0
        self.throttles = 0

    def acquire(self):
        """Block until this caller's turn. Serialises the whole process."""
        while True:
            with self._lock:
                now = time.monotonic()
                gap = 1.0 / max(self.rps, 1e-6)
                start = max(now, self._next_at)
                self._next_at = start + gap
                delay = start - now
            if delay > 0:
                self.waited += delay
                time.sleep(delay)
            return

    def on_success(self):
        with self._lock:
            self._ok_streak += 1
            if self._ok_streak >= self.probe_after and self.rps < self.max_rps:
                self.rps = min(self.max_rps, self.rps + self.step)
                self._ok_streak = 0

    def on_throttle(self, retry_after=None):
        """Halve the rate, and hold off for what the server asked."""
        with self._lock:
            self.throttles += 1
            self._ok_streak = 0
            self.rps = max(self.min_rps, self.rps * 0.5)
            # Push the next slot out so every waiting worker is delayed, not
            # just the one that got the 429. Without this the others march
            # straight into the same wall.
            hold = retry_after if retry_after is not None else min(30.0, 2.0 / self.rps)
            self._next_at = max(self._next_at, time.monotonic() + hold)

    def stats(self):
        return {"rps": round(self.rps, 3), "throttles": self.throttles,
                "waited_s": round(self.waited, 1)}


LIMITER = RateLimiter()


def complete(client, model, messages, max_tokens, temperature=0.4, attempts=12, quiet=False):
    """One chat call, paced by the shared limiter, with classified retry.

    Every call in the pipeline goes through here, so LIMITER sees the whole
    account's traffic and can hold it under the real ceiling. Retries remain as
    the backstop for what pacing cannot prevent — timeouts, dropped connections,
    and the first 429 that discovers a new ceiling.
    """
    delay = 6
    for n in range(1, attempts + 1):
        LIMITER.acquire()
        try:
            resp = client.chat.complete(model=model, messages=messages,
                                        max_tokens=max_tokens, temperature=temperature)
            if not resp.choices:
                raise LLMError("no choices in response")
            text = (resp.choices[0].message.content or "").strip()
            if not text:
                raise LLMError("empty response from model")
            LIMITER.on_success()
            return text, getattr(resp.choices[0], "finish_reason", None)
        except QuotaExhausted:
            raise
        except Exception as e:                       # noqa: BLE001 - retry transient errors
            transient, throttled, quota = _classify(e)
            if quota:
                # Fail immediately and say why. Twenty retries against an
                # exhausted account cost twenty minutes and produced a chapter
                # with 127 claims cut for lack of evidence they actually had.
                raise QuotaExhausted(
                    f"the API rejected this call for quota/billing reasons, not "
                    f"throttling — retrying will not help until the allowance "
                    f"resets.\n    {type(e).__name__}: {str(e)[:300]}") from e
            if throttled:
                LIMITER.on_throttle(_retry_after(e))
            if n == attempts:
                raise
            if not transient and n >= 4:             # a real error: stop burning attempts
                raise
            if throttled:
                # The limiter has already slowed the whole process and pushed
                # the next slot out; sleeping the full exponential on top would
                # double-count the penalty and stall a run that is now paced.
                wait = min(4.0 * n, 20.0) * (0.75 + random.random() * 0.5)
            else:
                wait = min(delay * 2, 120) * (0.75 + random.random() * 0.5)
                delay = min(delay * 1.7, 120)
            if not quiet and (not transient or n == 1 or n % 4 == 0):
                print(f"      retry {n}/{attempts - 1} "
                      f"({'rate limit -> ' + str(round(LIMITER.rps, 2)) + ' req/s'
                         if throttled else type(e).__name__}), "
                      f"waiting {wait:.0f}s", file=sys.stderr, flush=True)
            time.sleep(wait)


_FENCE_RE = re.compile(r"^\s*```(?:json)?\s*|\s*```\s*$", re.MULTILINE)


def parse_json(text):
    """Parse a model's JSON, tolerating fences and surrounding chatter."""
    s = _FENCE_RE.sub("", text).strip()
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass
    # Fall back to the outermost balanced object or array.
    start = min([i for i in (s.find("{"), s.find("[")) if i >= 0], default=-1)
    if start < 0:
        raise LLMError(f"no JSON found in response: {s[:200]}")
    opener = s[start]
    closer = "}" if opener == "{" else "]"
    depth, in_str, esc = 0, False, False
    for i in range(start, len(s)):
        ch = s[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                return json.loads(s[start:i + 1])
    raise Truncated(f"JSON never closed — response ran to {len(s)} chars and was cut")


def complete_json(client, model, messages, max_tokens, temperature=0.2, attempts=8,
                  quiet=False, repairs=2):
    """Chat call whose response must parse as JSON.

    Truncation is detected explicitly rather than surfacing as a parse error,
    because the two have different fixes: raise max_tokens vs fix the prompt.

    A response that is complete but malformed gets `repairs` corrective rounds.
    This is worth doing rather than failing: the commonest cause here is an
    unescaped quote inside a passage of IAST or Devanagari, and losing an entire
    source dossier to one stray quotation mark is a bad trade.
    """
    text, finish = complete(client, model, messages, max_tokens,
                            temperature=temperature, attempts=attempts, quiet=quiet)
    if finish == "length":
        raise Truncated(f"response hit the {max_tokens}-token ceiling "
                        f"({len(text)} chars); raise max_tokens")
    last = None
    for _ in range(repairs + 1):
        try:
            return parse_json(text)
        except Truncated:
            raise
        except Exception as e:                       # noqa: BLE001 - malformed, try to fix
            last = e
            fix = messages + [
                {"role": "assistant", "content": text[:12000]},
                {"role": "user", "content":
                    f"That response is not valid JSON ({e}). Return the SAME content again as "
                    f"strictly valid JSON and nothing else. Escape every double quote inside a "
                    f"string value as \\\", escape backslashes, and use no trailing commas and "
                    f"no comments. Do not add or remove any information."},
            ]
            text, finish = complete(client, model, fix, max_tokens,
                                    temperature=0.0, attempts=attempts, quiet=True)
            if finish == "length":
                raise Truncated("JSON repair hit the token ceiling") from e
    raise LLMError(f"could not obtain valid JSON after {repairs} repair(s): {last}")


def parallel(fn, jobs, workers=4, stagger=0.0, on_error=None):
    """Run `fn` over `jobs` concurrently, preserving input order in the result.

    Pacing is LIMITER's job, not this function's — `stagger` defaults to 0 and
    exists only for non-LLM work. An exception is returned in place of a result
    when `on_error` is given, so one failed unit cannot lose a whole chapter.
    """
    out = [None] * len(jobs)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {}
        for i, job in enumerate(jobs):
            futures[pool.submit(fn, job)] = i
            if stagger and i < len(jobs) - 1:
                time.sleep(stagger)
        for fut in as_completed(futures):
            i = futures[fut]
            try:
                out[i] = fut.result()
            except Exception as e:                   # noqa: BLE001 - reported, not swallowed
                if on_error is None:
                    raise
                out[i] = on_error(jobs[i], e)
    return out
