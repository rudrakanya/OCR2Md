#!/usr/bin/env python3
"""
query_gen.py — derive retrieval queries from the outline's sub-topics.

The old pipeline hard-coded a flat list of query strings per chapter. They went
stale whenever the corpus or the outline moved, and nothing could regenerate
them. Here the sub-topic is the stable artefact and the queries are derived:

  1. the sub-topic question itself, verbatim — a clean semantic query;
  2. anchored variants, pairing the question with the book's regional anchors
     ("Udayapur Vidisha", "Betwa valley", "Malwa Avanti", "Paramara"), so a
     generic sub-topic such as "crafts" or "festivals" pulls *this* region's
     material rather than the corpus's general treatment of the subject;
  3. LLM-expanded paraphrases and keyword sets, which matter most for the
     chapters with no prior coverage, where the obvious phrasing may not match
     how the sources actually talk.

Stage 3 is cached to disk (book/_queries.json), so it costs one pass and is
afterwards inspectable and editable by hand. If the API is unavailable or the
response will not parse, generation degrades to stages 1-2 rather than failing.

    from query_gen import build_queries
    qmap = build_queries(CHAPTERS)          # {(chapter_n, subtopic_key): [str, ...]}

CLI:
    python query_gen.py                     # build/refresh the cache, print a summary
    python query_gen.py --chapters 6,15,18 --show
    python query_gen.py --no-llm            # deterministic queries only
"""
import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

from book_outline import BOOK_ANCHORS, BOOK_TITLE, CHAPTERS
from console import use_utf8

load_dotenv()
load_dotenv(Path(__file__).resolve().parent / ".env", override=False)

CACHE = Path(os.environ.get("QUERY_CACHE", "book/_queries.json"))
MODEL = os.environ.get("MISTRAL_CHAT_MODEL", "mistral-large-latest")
N_LLM_QUERIES = 3

_EXPAND_SYSTEM = (
    "You generate search queries for a semantic (vector) retrieval system. The corpus is a set of "
    "scholarly books and reports in English: histories of the Paramāra dynasty of Malwa, studies of "
    "Indian temple architecture and iconography, district gazetteers, archaeological survey reports, "
    "and English translations of two Hindi local histories of the town of Udaypur in Vidisha "
    "district, Madhya Pradesh.\n"
    "For each sub-topic you are given, write exactly "
    f"{N_LLM_QUERIES} alternative retrieval queries. Vary them deliberately: one close paraphrase "
    "using different vocabulary; one that names the specific technical terms, proper nouns, "
    "Sanskrit/IAST terminology or people a source would actually use; and one broader query that "
    "would match a general discussion of the theme. Do not simply restate the sub-topic. "
    "Do not include instructions, quotation marks, or numbering inside a query.\n"
    'Reply with JSON only: {"subtopic_key": ["query", "query", "query"], ...}'
)


def _anchor_for(chapter):
    """Pick the anchor that best fits a chapter's altitude.

    Site-level chapters want the town named; regional chapters want the region.
    Getting this wrong is how the old pipeline pulled Thanjavur into a chapter
    about Udaypur's economy.
    """
    n = chapter["n"]
    if n in (1, 7, 8, 9, 10, 11, 15, 17, 18, 19):
        return BOOK_ANCHORS[0]                      # Udayapur / Udaypur / Vidisha
    if n in (2, 3):
        return BOOK_ANCHORS[1]                      # Betwa / Vetravati valley
    if n in (5, 6, 12, 16):
        return BOOK_ANCHORS[3]                      # Paramara
    return BOOK_ANCHORS[2]                          # Malwa / Avanti plateau


def deterministic_queries(chapter, sub):
    """Stages 1-2: the question itself, plus a regionally anchored variant."""
    q = sub["question"].strip()
    return [q, f"{q} — {_anchor_for(chapter)}"]


def _parse_json(text):
    """Pull the JSON object out of a model reply that may be fenced or prefaced."""
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return None


def _expand_chapter(client, chapter, attempts=3):
    """One call per chapter: LLM paraphrases for all of its sub-topics."""
    listing = "\n".join(f"- {s['key']}: {s['question']}" for s in chapter["subtopics"])
    user = (
        f"BOOK: {BOOK_TITLE} — a reference history of the Udayeśvara (Nīlakaṇṭheśvara) temple at "
        f"Udaypur, Vidisha district, Madhya Pradesh, and the Paramāra dynasty of Malwa.\n\n"
        f"CHAPTER {chapter['n']}: {chapter['title']}\n\n"
        f"CHAPTER SCOPE: {chapter['scope']}\n\n"
        f"SUB-TOPICS:\n{listing}\n"
    )
    delay = 6
    for n in range(1, attempts + 1):
        try:
            resp = client.chat.complete(
                model=MODEL,
                messages=[{"role": "system", "content": _EXPAND_SYSTEM},
                          {"role": "user", "content": user}],
                max_tokens=1500, temperature=0.3,
                response_format={"type": "json_object"},
            )
            data = _parse_json(resp.choices[0].message.content or "")
            if data:
                return data
            raise ValueError("unparseable JSON")
        except Exception as e:                       # noqa: BLE001 - retry, then degrade
            if n == attempts:
                print(f"  ! ch{chapter['n']} LLM expansion failed ({type(e).__name__}); "
                      f"using deterministic queries only", file=sys.stderr)
                return {}
            time.sleep(delay)
            delay = min(delay * 2, 45)


def _save_cache(cache):
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    tmp = CACHE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(CACHE)


def _load_cache():
    if CACHE.exists():
        try:
            return json.loads(CACHE.read_text(encoding="utf-8"))
        except Exception:                            # noqa: BLE001 - corrupt cache is not fatal
            pass
    return {}


def _fingerprint(sub):
    """Changing a sub-topic's wording invalidates just that entry.
    hashlib, not hash(): the builtin is salted per process and would expire the
    whole cache on every run."""
    return hashlib.sha1(sub["question"].encode("utf-8")).hexdigest()[:16]


def build_queries(chapters=None, client=None, use_llm=True, refresh=False):
    """Return {(chapter_n, subtopic_key): [query, ...]}, refreshing the cache as needed."""
    chapters = chapters or CHAPTERS
    cache = {} if refresh else _load_cache()

    if use_llm:
        need = [c for c in chapters
                if any(cache.get(f"{c['n']}:{s['key']}", {}).get("fp") != _fingerprint(s)
                       for s in c["subtopics"])]
        if need and client is None:
            from kb_search import get_client
            client = get_client()
        for i, c in enumerate(need, 1):
            print(f"  expanding queries {i}/{len(need)} — ch{c['n']}: {c['title'][:48]}", flush=True)
            data = _expand_chapter(client, c)
            for s in c["subtopics"]:
                extra = [q.strip() for q in (data.get(s["key"]) or []) if isinstance(q, str) and q.strip()]
                cache[f"{c['n']}:{s['key']}"] = {"fp": _fingerprint(s), "llm": extra[:N_LLM_QUERIES]}
            _save_cache(cache)      # per chapter: an interrupted run keeps what it paid for

    out = {}
    for c in chapters:
        for s in c["subtopics"]:
            qs = deterministic_queries(c, s)
            qs += cache.get(f"{c['n']}:{s['key']}", {}).get("llm", [])
            seen, uniq = set(), []
            for q in qs:
                k = q.lower()
                if k not in seen:
                    seen.add(k); uniq.append(q)
            out[(c["n"], s["key"])] = uniq
    return out


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Derive retrieval queries from the outline's sub-topics")
    ap.add_argument("--chapters", help="comma-separated chapter numbers (default: all)")
    ap.add_argument("--no-llm", action="store_true", help="deterministic queries only")
    ap.add_argument("--refresh", action="store_true", help="ignore the cache and re-expand")
    ap.add_argument("--show", action="store_true", help="print every derived query")
    args = ap.parse_args()

    chs = CHAPTERS
    if args.chapters:
        want = {int(x) for x in args.chapters.split(",")}
        chs = [c for c in CHAPTERS if c["n"] in want]

    qmap = build_queries(chs, use_llm=not args.no_llm, refresh=args.refresh)
    total = sum(len(v) for v in qmap.values())
    print(f"\n{len(qmap)} sub-topics across {len(chs)} chapters -> {total} queries "
          f"({total / max(len(qmap), 1):.1f} per sub-topic)")
    if args.show:
        for c in chs:
            print(f"\n=== Chapter {c['n']}: {c['title']}")
            for s in c["subtopics"]:
                print(f"  [{s['key']}]")
                for q in qmap[(c["n"], s["key"])]:
                    print(f"     - {q}")
    else:
        print(f"cache: {CACHE}   (run with --show to print them)")


if __name__ == "__main__":
    main()
