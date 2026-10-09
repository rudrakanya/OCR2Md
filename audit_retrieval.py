#!/usr/bin/env python
"""Phase 3 — is the knowledge base ready to be retrieved from?

    python audit_retrieval.py

Two questions, because they fail differently:

  1. COHERENCE (no model needed). A chunk is the unit a chapter quotes. One that
     starts mid-sentence, is a bare table row, or is a running head reads as
     authoritative evidence while saying nothing. This counts those corpus-wide.

  2. BEHAVIOUR (live queries). Whether the defects Phases 1-2 found actually
     reach a drafter: do ADH's fabricated iconography chunks surface for a
     sculpture query, and do the duplicated Patil passages come back together in
     one top-k, which is what would let one source look like two?

Reads only: no store writes, no re-embed, no paid API. The embedding model is
the one already cached locally (intfloat/multilingual-e5-small).
"""
from __future__ import annotations

import collections
import json
import re
import sqlite3
import sys
import unicodedata
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
SQLITE = ROOT / "kb3" / "kb_active.sqlite"
REGISTRY = ROOT / "kb_audit" / "source_registry.yaml"
DATA = ROOT / "kb_audit" / "retrieval_readiness.json"

# The questions this book actually has to answer, spread across its chapters.
QUERIES = [
    ("udayesvara temple inscription date of consecration", "C5"),
    ("Udayaditya accession date and reign", "C5"),
    ("Sapta Matrka iconography niches four handed goddess attributes", "C7"),
    ("bhumija temple shikhara form and latas", "C6"),
    ("Betwa river seasonal flow and rainfall", "C2"),
    ("Udaypur town market lanes and houses today", "C1"),
    ("Paramara dynasty genealogy Bhoja successors", "C4"),
    ("stepwell baoli water structures at Udaypur", "C3"),
    ("temple land grants and endowment economy", "C10"),
    ("Vidisha district monuments and archaeological places", "C1"),
    ("Samaranganasutradhara on temple proportions", "C6"),
    ("sculpture on the jangha of the temple exterior", "C7"),
]

# Only a genuinely lower-case or punctuation-initial start counts. An earlier
# version also matched a leading "the"/"and"/"that" case-insensitively, which
# flagged thousands of perfectly good chunk openings and put the corpus at 26%
# clean instead of its real 75%.
MIDSENT_START = re.compile(r"^[a-z,;:)\]]")
ENDS_OPEN = re.compile(r"[a-z,;:(\[]$")
PIPE_HEAVY = re.compile(r"^\s*\|")
RUNNING_HEAD = re.compile(r"^[A-Z ‘’'\-.]{12,}$")


def norm(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s or "")).strip()


def coherence_flags(t):
    """What is wrong with this chunk as a quotable unit."""
    t = (t or "").strip()
    flags = []
    if len(t) < 200:
        flags.append("short")
    first = t.split("\n", 1)[0]
    if MIDSENT_START.match(t):
        flags.append("starts mid-sentence")
    if ENDS_OPEN.search(t):
        flags.append("ends mid-sentence")
    lines = [l for l in t.split("\n") if l.strip()]
    if lines and sum(1 for l in lines if PIPE_HEAVY.match(l)) / len(lines) > 0.6:
        flags.append("table fragment")
    if RUNNING_HEAD.match(first) and len(lines) <= 2:
        flags.append("running head")
    letters = sum(c.isalpha() for c in t)
    if t and letters / max(1, len(t)) < 0.45:
        flags.append("mostly non-letters")
    return flags


def main():
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    code = {s["source_id"]: s.get("code", "?") for s in reg["sources"]}

    db = sqlite3.connect(f"file:{SQLITE}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row

    # ---- 1. coherence, corpus-wide -----------------------------------------
    print("=" * 72)
    print("1. CHUNK COHERENCE (all chunks, no model needed)")
    print("=" * 72)
    tally = collections.Counter()
    per_src = collections.defaultdict(collections.Counter)
    total = 0
    lens = []
    for r in db.execute("select parent_source_id, text, n_chars from chunks"):
        total += 1
        lens.append(r["n_chars"] or len(r["text"] or ""))
        fl = coherence_flags(r["text"])
        c = code.get(r["parent_source_id"], r["parent_source_id"])
        if not fl:
            tally["clean"] += 1
        for f in fl:
            tally[f] += 1
            per_src[c][f] += 1
    lens.sort()
    print(f"chunks: {total} | median {lens[len(lens)//2]} chars | "
          f"p10 {lens[len(lens)//10]} | p90 {lens[9*len(lens)//10]}")
    print(f"\n{'flag':22s} {'chunks':>7s} {'share':>7s}")
    for f, n in tally.most_common():
        print(f"{f:22s} {n:7d} {n/total:7.1%}")

    # Flags, not flagged chunks: one chunk can carry several, so this ratio can
    # exceed 1. It ranks where the trouble is concentrated, not a clean rate.
    print(f"\nworst sources by flags per chunk:")
    rows = []
    for c, fl in per_src.items():
        n = db.execute("select count(*) from chunks where parent_source_id=?",
                       (next(k for k, v in code.items() if v == c),)).fetchone()[0] \
            if c in code.values() else 0
        flagged = sum(v for k, v in fl.items())
        rows.append((c, n, flagged, dict(fl)))
    for c, n, flagged, fl in sorted(rows, key=lambda x: -(x[2] / max(1, x[1])))[:8]:
        if n:
            top = ", ".join(f"{k} {v}" for k, v in sorted(fl.items(), key=lambda x: -x[1])[:3])
            print(f"   {c:9s} {flagged:5d} flags over {n:5d} chunks ({flagged/n:5.0%})  {top}")

    # ---- 2. live retrieval --------------------------------------------------
    print("\n" + "=" * 72)
    print("2. LIVE RETRIEVAL (intfloat/multilingual-e5-small, cached)")
    print("=" * 72)
    from kb3_chroma_query import search

    adh_bad = {r["chunk_id"] for r in db.execute(
        """select chunk_id from chunks where parent_source_id='adhikari-2013-un'
           and (text like '%Island | Attribution%' or text like '%rāhīna%'
                or text like '%Jñābhadras%')""")}
    # duplicate text shared across the three Patil registrations
    hashes = collections.defaultdict(set)
    for r in db.execute("select content_hash, parent_source_id, chunk_id from chunks"):
        hashes[r["content_hash"]].add((r["parent_source_id"], r["chunk_id"]))
    dup_hash = {h for h, v in hashes.items() if len({s for s, _ in v}) > 1}
    chunk_hash = {r["chunk_id"]: r["content_hash"]
                  for r in db.execute("select chunk_id, content_hash from chunks")}

    results = []
    for q, chap in QUERIES:
        hits = search(query=q, k=8)
        codes = [code.get(h.get("parent_source_id"), "?") for h in hits]
        bad = [h["chunk_id"] for h in hits if h.get("chunk_id") in adh_bad]
        seen = collections.Counter(chunk_hash.get(h.get("chunk_id")) for h in hits)
        dup_pairs = [h for h, n in seen.items() if n > 1 and h in dup_hash]
        flagged = sum(1 for h in hits if coherence_flags(h.get("text")))
        results.append({"query": q, "chapter": chap, "codes": codes,
                        "adh_fabricated_hits": bad,
                        "duplicate_text_in_topk": len(dup_pairs),
                        "incoherent_of_8": flagged})
        print(f"\nQ: {q}")
        print(f"   sources: {' '.join(codes)}")
        print(f"   incoherent chunks in top-8: {flagged}/8"
              + (f" | ADH FABRICATED CHUNKS RETURNED: {len(bad)}" if bad else "")
              + (f" | duplicate text twice in top-8: {len(dup_pairs)}" if dup_pairs else ""))

    # how often do two of the three Patil codes co-occur in one top-k?
    pat = {"PAT-CH", "PAT-TEM", "PAT-INS"}
    co = sum(1 for r in results if len(pat & set(r["codes"])) > 1)
    print("\n" + "-" * 72)
    print(f"queries whose top-8 held more than one Patil registration: {co}/{len(results)}")
    print(f"queries that returned a fabricated ADH chunk: "
          f"{sum(1 for r in results if r['adh_fabricated_hits'])}/{len(results)}")
    print(f"mean incoherent chunks per top-8: "
          f"{sum(r['incoherent_of_8'] for r in results)/len(results):.1f}")

    DATA.write_text(json.dumps(
        {"coherence": dict(tally), "total_chunks": total,
         "median_chars": lens[len(lens)//2], "queries": results},
        ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nwrote {DATA}")


if __name__ == "__main__":
    main()
