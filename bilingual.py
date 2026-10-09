#!/usr/bin/env python
"""Bilingual query expansion — reach the Devanagari sources from an English query.

    from bilingual import second_form, merge_candidates, cost_report

The vector map measured a 4.8x language island: a Devanagari chunk's fifteen
nearest neighbours are 86.6% Devanagari against an 18% base rate, so an English
query's neighbourhood is almost entirely English chunks. Four sources -- RAJM
(Bhoja's own Rājamārtaṇḍa), BHJ-H, TIW-H and SAM -- were unreachable from
English, while the SAME collection returned all four when queried in Hindi.

No re-embedding fixes that; it is a property of where the query lands. Issuing
the query in both scripts does fix it, which is what this module provides.

TRANSLATION is generated at query time, never hard-coded, and cached on disk so
a repeated query is free. A local MT model was preferred but none is available
here: no argostranslate, no sentencepiece, and nothing translation-capable in
the HF cache (the cached `mms-tts-hin` is speech synthesis). Installing
Helsinki-NLP/opus-mt-en-hi would mean sentencepiece plus a ~300 MB resident
model on a machine with ~3 GB free, so the cheapest chat model is used instead
and every call is accounted for. Set BILINGUAL=0 to disable entirely.

MERGE is deliberately asymmetric. The second query must make the Devanagari
sources *reachable*, not let them flood a result set the English query already
answers well, so:

  * a chunk's merged similarity is max(sim_primary, W * sim_second), W<1, so a
    chunk found by both keeps its better score and one found only by the second
    form is slightly discounted;
  * at most SECOND_CAP of the final list may be chunks that ONLY the second form
    found. Beyond that they are demoted, not dropped.

Both knobs live in kb3/retrieval.yaml and are editable per chapter.
"""
from __future__ import annotations

import json
import os
import re
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "kb3" / "query_translations.json"
CONFIG = ROOT / "kb3" / "retrieval.yaml"
DEVA = re.compile(r"[ऀ-ॿ]")
MODEL = "gpt-4.1-nano"          # cheapest capable; $0.10/M in, $0.40/M out
PRICE_IN, PRICE_OUT = 0.10 / 1e6, 0.40 / 1e6

_lock = threading.Lock()
_cache = None
_usage = {"calls": 0, "in": 0, "out": 0, "cache_hits": 0}


def enabled():
    return os.environ.get("BILINGUAL", "1") not in ("0", "false", "no")


def config():
    """Retrieval knobs, with defaults if the file is absent."""
    d = {"second_weight": 0.95, "second_cap": 0.35,
         "source_cap": {"default": 0.30}, "translate_model": MODEL}
    if CONFIG.exists():
        import yaml
        got = yaml.safe_load(CONFIG.read_text(encoding="utf-8")) or {}
        d.update({k: v for k, v in got.items() if v is not None})
    return d


def _load_cache():
    global _cache
    if _cache is None:
        try:
            _cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
        except (OSError, ValueError):
            _cache = {}
    return _cache


def _save_cache():
    try:
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        tmp = CACHE.with_suffix(".tmp")
        tmp.write_text(json.dumps(_cache, ensure_ascii=False, indent=1), encoding="utf-8")
        tmp.replace(CACHE)
    except OSError:
        pass


def script_of(q):
    return "devanagari" if DEVA.search(q or "") else "latin"


def second_form(query, model=None):
    """The same question in the other script, or None if not applicable.

    A Devanagari query gets an English form and vice versa, so the expansion
    works in both directions rather than privileging English input.
    """
    if not query or not query.strip() or not enabled():
        return None
    model = model or config().get("translate_model", MODEL)
    want = "English" if script_of(query) == "devanagari" else "Hindi (Devanagari script)"
    key = f"{model}|{want}|{query.strip()}"
    cache = _load_cache()
    with _lock:
        if key in cache:
            _usage["cache_hits"] += 1
            return cache[key]
    try:
        from openai import OpenAI
        from phase4_embed_v2 import load_key
        client = OpenAI(api_key=load_key())
        r = client.chat.completions.create(
            model=model, temperature=0, max_tokens=120,
            messages=[
                {"role": "system",
                 "content": ("You translate short search queries for a history "
                             "corpus about the Paramāra dynasty, Bhoja, and the "
                             "Udayeśvara temple at Udaypur (Vidisha, Madhya "
                             f"Pradesh). Reply ONLY with the query in {want}. "
                             "Keep proper nouns and technical terms "
                             "(śikhara, bhūmija, Rājamārtaṇḍa) in their usual "
                             "form for that script. No explanation.")},
                {"role": "user", "content": query.strip()},
            ])
        out = (r.choices[0].message.content or "").strip()
        with _lock:
            _usage["calls"] += 1
            _usage["in"] += r.usage.prompt_tokens
            _usage["out"] += r.usage.completion_tokens
            cache[key] = out
            _save_cache()
        return out or None
    except Exception as e:                       # never let retrieval fail on this
        print(f"  [bilingual] translation unavailable ({type(e).__name__}); "
              f"continuing with the single query", file=sys.stderr)
        return None


def merge_candidates(primary, second, second_weight=None, second_cap=None, k=None):
    """Merge two {chunk_id: similarity} maps into one ranked list.

    Returns [(chunk_id, merged_sim, origin)] where origin is 'both',
    'primary' or 'second'. Demotion for exceeding the second-form cap is applied
    by the caller when it truncates to k, so nothing is lost -- only reordered.
    """
    cfg = config()
    w = cfg["second_weight"] if second_weight is None else second_weight
    cap = cfg["second_cap"] if second_cap is None else second_cap

    # Each query's similarities are normalised WITHIN that query before they are
    # compared. Raw cosines from two different queries are not on a common scale:
    # for "yoga sutra commentary attributed to Bhoja" the English form's best
    # match scored 0.594 while the Hindi form's best was 0.573, so taking a raw
    # max systematically demoted every Devanagari chunk no matter how well it
    # answered the Hindi query -- RAJM's own passages landed 13th and never
    # reached a top-8. Normalising per query asks the right question: how good is
    # this chunk FOR ITS OWN QUERY, relative to that query's other candidates.
    def _norm(d):
        if not d:
            return {}
        vals = list(d.values())
        lo, hi = min(vals), max(vals)
        if hi - lo < 1e-9:
            return {c: 1.0 for c in d}
        return {c: (v - lo) / (hi - lo) for c, v in d.items()}

    np_, ns_ = _norm(primary or {}), _norm(second or {})
    merged = {}
    for cid, s in np_.items():
        merged[cid] = [s, None]
    for cid, s in ns_.items():
        if cid in merged:
            merged[cid][1] = s
        else:
            merged[cid] = [None, s]

    rows = []
    for cid, (a, b) in merged.items():
        cand = [x for x in (a, (w * b) if b is not None else None) if x is not None]
        origin = "both" if (a is not None and b is not None) else ("primary" if a is not None else "second")
        rows.append((cid, max(cand), origin))
    rows.sort(key=lambda r: -r[1])

    if k and cap is not None and cap < 1.0:
        allowed = max(1, int(round(cap * k)))
        kept, demoted, n_second = [], [], 0
        for r in rows:
            if r[2] == "second":
                if n_second >= allowed:
                    demoted.append(r)
                    continue
                n_second += 1
            kept.append(r)
        rows = kept + demoted
    return rows


def cost_report():
    u = dict(_usage)
    u["cost_usd"] = round(u["in"] * PRICE_IN + u["out"] * PRICE_OUT, 6)
    u["model"] = MODEL
    u["cached_queries"] = len(_load_cache())
    return u


if __name__ == "__main__":
    qs = sys.argv[1:] or ["yoga sutra commentary attributed to Bhoja",
                          "Udayesvara temple inscription date"]
    for q in qs:
        print(f"{q!r}\n  -> {second_form(q)!r}")
    print("\ncost:", json.dumps(cost_report(), ensure_ascii=False))
