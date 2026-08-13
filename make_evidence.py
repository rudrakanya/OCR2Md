#!/usr/bin/env python3
"""
make_evidence.py — build a per-chapter evidence brief from the vector KB.

This is the reasoning stage that runs before any drafting. For each chapter in
book_outline.py it works *sub-topic by sub-topic* rather than doing one flat
pass per chapter:

  1. query_gen.py derives several retrieval queries per sub-topic;
  2. retrieve.py runs each through the hybrid funnel — dense + BM25 + entity
     channels, fused by RRF, reranked by a cross-encoder;
  3. a relevance floor on the reranker's score discards weak matches instead of
     blindly filling top-k;
  4. a source cap stops one book supplying a whole sub-topic when others have
     material on it — with a translation and its original counting as one
     source, so the same testimony cannot fill a pack twice in two languages;
  5. what survives is written to book/_evidence/chNN.md, grouped under its
     sub-topic, with a coverage table and an explicit flag wherever the KB is
     thin — so gaps reach the writer as gaps, not as silence.

Where the floor lives
---------------------
In v1 it lived here, as a cosine cut (ABS_FLOOR 0.76) on mistral-embed scores.
In v2 the funnel ends in a cross-encoder, whose judgement of a (query, passage)
pair is a strictly better relevance signal than bi-encoder cosine, so the floor
moved to retrieve.py with it. This module no longer decides what is relevant;
it decides how to *present* what retrieval returned.

The guarantee is unchanged and is the point: a sub-topic with no regional
coverage must return nothing rather than eight confident passages about
somewhere else. An empty pack is a correct output and flows to
`[GAP — not in sources]`.

Staleness
---------
Each pack records the KB's build stamp. `--check` reports any pack that no
longer matches the current KB, and draft_chapter.py refuses to write from a
stale one. The old pipeline had no such link: every pack in book/_evidence/
predated the KB it was supposedly drawn from.

Prereqs: build_kb.py has been run. MISTRAL_API_KEY in .env.
Usage:
    python make_evidence.py                       # all 19 chapters
    python make_evidence.py --chapters 6,15,18
    python make_evidence.py --check               # report staleness, write nothing
    python make_evidence.py --no-llm              # deterministic queries only
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from book_outline import BOOK_TITLE, CHAPTERS
from config import CFG
from console import use_utf8
from entities import EntityIndex
from llm import get_client
from query_gen import build_queries
from retrieve import KBError, Retriever, kb_stamp

# Retrieval, the relevance floor and source diversity now live in retrieve.py,
# which runs the full hybrid funnel (dense + BM25 + entity -> RRF -> rerank).
# v1's ABS_FLOOR / REL_MARGIN / diversify() were removed rather than kept in
# parallel: two floors in two modules is how they drift apart.
THIN_KEEP = CFG.retrieval.thin_keep


def _cite(r):
    """The block header — the single place source/trail/page is written out.
    `r['text']` is the body only, so nothing here is repeated inside the block."""
    pages = ""
    if r.get("page_start"):
        pages = (f", p. {r['page_start']}" if r["page_start"] == r.get("page_end")
                 else f", pp. {r['page_start']}-{r['page_end']}")
    return f"[{r['source']}{pages}] {r.get('trail') or r.get('heading', '')}".strip()


def build_pack(chapter, qmap, retriever, entities):
    """Run every sub-topic of one chapter through the hybrid funnel.

    Metadata filters (§3.6) are read from the outline, not from retrieval code:
    a sub-topic may carry `filters` ({"kind": "primary"}, a period window, a
    genre) and a chapter may carry chapter-wide defaults. Keeping scope in
    book_outline.py means the single source of truth stays single.
    """
    out = []
    chapter_filters = chapter.get("filters") or {}
    for s in chapter["subtopics"]:
        queries = qmap[(chapter["n"], s["key"])]
        filters = {**chapter_filters, **(s.get("filters") or {})} or None
        pack = retriever.subtopic(queries, question=s["question"], filters=filters)

        # The check a similarity score cannot make, now backed by the entity
        # registry rather than difflib: a passage naming only 'Nīlakaṇṭheśvara'
        # attests a sub-topic asking about 'Udayeśvara'.
        absent = entities.unevidenced(s["question"], pack.kept)
        status, note = pack.status, pack.note
        if absent and status == "OK":
            status = "PARTIAL"
            note = f"{note}; but nothing retrieved mentions {', '.join(absent)}"

        out.append({"sub": s, "queries": queries, "n_cand": pack.n_candidates,
                    "cut": pack.floor, "kept": pack.kept, "status": status,
                    "note": note, "unevidenced": absent,
                    "filters": filters, "diagnostics": pack.diagnostics})
    return out


def write_pack(path, chapter, results, stamp):
    seen_global = set()
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Evidence brief — Chapter {chapter['n']}: {chapter['title']}\n\n")
        f.write("<!-- generated by make_evidence.py; do not edit by hand -->\n")
        f.write(f"<!-- kb: built_at={stamp['built_at']} count={stamp['count']} "
                f"hash={stamp['hash']} -->\n")
        f.write(f"<!-- generated_at={datetime.now(timezone.utc).isoformat(timespec='seconds')} -->\n\n")

        if chapter.get("theme"):
            f.write(f"**Theme:** {chapter['theme']}\n\n")
        f.write(f"**Scope.** {chapter['scope']}\n\n")
        if chapter.get("constraints"):
            f.write(f"**Editorial constraints.** {chapter['constraints']}\n\n")

        f.write("## Coverage summary\n\n")
        f.write("| sub-topic | queries | candidates | kept | sources | best | status |\n")
        f.write("|---|---:|---:|---:|---:|---:|---|\n")
        for r in results:
            srcs = len({h['source'] for h in r['kept']})
            best = f"{r['kept'][0]['score']:.3f}" if r['kept'] else "—"
            f.write(f"| {r['sub']['key']} | {len(r['queries'])} | {r['n_cand']} | "
                    f"{len(r['kept'])} | {srcs} | {best} | **{r['status']}** |\n")
        absent_any = [r for r in results if r.get("unevidenced")]
        if absent_any:
            f.write("\n> **Named in a sub-topic but absent from the evidence.** The knowledge "
                    "base says nothing about the following. They must not be written about "
                    "from general knowledge — mark them `[GAP — not in sources]` or omit them:\n>\n")
            for r in absent_any:
                f.write(f"> - **{r['sub']['key']}**: {', '.join(r['unevidenced'])}\n")

        flagged = [r for r in results if r["status"] in ("GAP", "THIN")]
        if flagged:
            f.write("\n> **Gaps for review.** The knowledge base is thin on the following "
                    "sub-topics. Do not invent material to cover them — mark them "
                    "`[GAP — not in sources]` in the draft:\n>\n")
            for r in flagged:
                f.write(f"> - **{r['sub']['key']}** ({r['status']}): {r['note']}\n")
        f.write("\n")

        for r in results:
            s = r["sub"]
            f.write(f"\n---\n\n## Sub-topic: {s['key']}\n\n")
            f.write(f"**Question.** {s['question']}\n\n")
            f.write(f"**Status.** {r['status']} — {r['note']}. "
                    f"Floor {r['cut']:.3f}; {r['n_cand']} candidates from "
                    f"{len(r['queries'])} queries.\n\n")
            if not r["kept"]:
                f.write("*No supporting passages. Treat this sub-topic as a gap.*\n\n")
                continue
            for h in r["kept"]:
                kid = (h["source"], h["chunk"])
                if kid in seen_global:
                    f.write(f"### {_cite(h)}  (score {h['score']:.3f})\n\n"
                            f"*[Repeated from an earlier sub-topic in this chapter.]*\n\n")
                    continue
                seen_global.add(kid)
                f.write(f"### {_cite(h)}  (score {h['score']:.3f})\n\n{h['text']}\n\n")


def _retrieval_record(r):
    """What retrieval actually did for one sub-topic, kept for later inspection.

    `Pack.diagnostics` carries which channels found what, which floor rule
    applied, which entities drove the entity channel, and what fell just below
    the cut. All of it was computed and then thrown away when the pack was
    written, so by the time a chapter was drafted nobody could say why a passage
    was there — or why an expected one was not. Persisting it is what makes the
    retrieval stage explainable without re-running retrieval.
    """
    d = r.get("diagnostics") or {}
    return {
        "channels": d.get("channels"),          # which channel found the top hits
        "entity_ids": d.get("entity_ids"),      # entity-exact channel drivers
        "filters": d.get("filters"),            # §3.6 metadata/label scoping
        "counts": {"dense": d.get("n_dense"), "sparse": d.get("n_sparse"),
                   "entity": d.get("n_entity"), "fused": d.get("n_fused")},
        "reranker": d.get("rerank_backend"),
        "floor_mode": d.get("floor_mode"),
        "n_above_floor": d.get("n_above_floor"),
        "capped_backfilled": d.get("capped_backfilled"),
        "just_below_floor": d.get("cut"),       # present only with --explain
    }


def write_pack_json(path, chapter, results, stamp):
    """Machine-readable twin of the brief.

    The .md is for you to read; this is what draft_chapter.py consumes. Passages
    carry stable ids (E1, E2, ...) which the drafting model cites and which are
    resolved back into numbered endnotes, so every citation is traceable to a
    specific retrieved chunk instead of being invented.

    Each passage also carries `chunk_id` and `retrieval`, so a claim in the
    finished chapter can be walked all the way back to the row in the knowledge
    base and to the reason that row was chosen.
    """
    eid = 0
    subs = []
    for r in results:
        passages = []
        for h in r["kept"]:
            eid += 1
            passages.append({
                "id": f"E{eid}",
                "chunk_id": h.get("rowid"),      # the join key back into kb_store
                "source": h["source"],
                "trail": h.get("trail", ""),
                "heading": h.get("heading", ""),
                "page_start": h.get("page_start"), "page_end": h.get("page_end"),
                "score": round(h["score"], 4),
                # Per-channel scores, so "why this passage" is answerable.
                "channels": sorted(h.get("ranks", {})) or None,
                "rrf": round(h["rrf"], 5) if h.get("rrf") is not None else None,
                "text": h["text"]})
        subs.append({"key": r["sub"]["key"], "question": r["sub"]["question"],
                     "status": r["status"], "note": r["note"], "cut": round(r["cut"], 4),
                     "unevidenced": r.get("unevidenced", []),
                     "n_candidates": r["n_cand"], "queries": r["queries"],
                     "filters": r.get("filters"),
                     "retrieval": _retrieval_record(r),
                     "passages": passages})
    payload = {"n": chapter["n"], "title": chapter["title"], "theme": chapter.get("theme"),
               "scope": chapter["scope"], "constraints": chapter.get("constraints"),
               "kb": stamp, "subtopics": subs}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")


def read_pack_stamp(path):
    """Recover the KB stamp a pack was built against, if any."""
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines()[:8]:
        if "kb:" in line and "hash=" in line:
            bits = dict(p.split("=", 1) for p in line.split() if "=" in p)
            return bits.get("hash", "").rstrip("-->").strip()
    return None


def check_staleness(outdir, stamp, chapters):
    """Report packs that are missing or built against a different KB."""
    stale, missing, ok = [], [], []
    for c in chapters:
        p = outdir / f"ch{c['n']:02d}.md"
        if not p.exists():
            missing.append(c["n"])
        elif read_pack_stamp(p) != stamp["hash"]:
            stale.append(c["n"])
        else:
            ok.append(c["n"])
    return ok, stale, missing


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Build per-chapter evidence briefs from the vector KB")
    ap.add_argument("--out", default="book/_evidence", help="output directory")
    ap.add_argument("--chapters", help="comma-separated chapter numbers (default: all)")
    ap.add_argument("--check", action="store_true", help="report pack staleness and exit")
    ap.add_argument("--no-llm", action="store_true", help="deterministic queries only")
    args = ap.parse_args()

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)
    wanted = ({int(x) for x in args.chapters.split(",")} if args.chapters else None)
    chapters = [c for c in CHAPTERS if not wanted or c["n"] in wanted]

    try:
        stamp = kb_stamp()
    except KBError as e:
        print(f"ERROR: {e}"); sys.exit(1)

    if args.check:
        ok, stale, missing = check_staleness(outdir, stamp, CHAPTERS)
        print(f"KB built_at={stamp['built_at']} count={stamp['count']} hash={stamp['hash']}\n")
        print(f"  current : {ok if ok else '—'}")
        print(f"  STALE   : {stale if stale else '—'}")
        print(f"  MISSING : {missing if missing else '—'}")
        sys.exit(1 if (stale or missing) else 0)

    print(f"KB: {stamp['count']} chunks, built {stamp['built_at']}, hash {stamp['hash']}, "
          f"config {stamp['config']}"
          + ("  [contextualized]" if stamp.get("contextualized") else ""))
    try:
        client = get_client()
        entities = EntityIndex.load()
        retriever = Retriever(entities=entities, client=client)
        print(f"retrieval: hybrid (dense+sparse+entity -> RRF -> "
              f"{retriever.reranker.name}), {len(entities.entries)} entities")
        qmap = build_queries(chapters, client=client, use_llm=not args.no_llm)
        for c in chapters:
            results = build_pack(c, qmap, retriever, entities)
            path = outdir / f"ch{c['n']:02d}.md"
            write_pack(path, c, results, stamp)
            write_pack_json(outdir / f"ch{c['n']:02d}.json", c, results, stamp)
            kept = sum(len(r["kept"]) for r in results)
            words = sum(len(h["text"].split()) for r in results for h in r["kept"])
            flags = [r["sub"]["key"] for r in results if r["status"] in ("GAP", "THIN")]
            tail = f"  ⚠ thin: {', '.join(flags)}" if flags else ""
            print(f"ch{c['n']:02d}: {len(results)} sub-topics, {kept} passages, "
                  f"~{words} words -> {path}{tail}")
    except KBError as e:
        print(f"ERROR: {e}"); sys.exit(1)
    print("\nDone. Inspect the briefs, then: python draft_chapter.py <n>")


if __name__ == "__main__":
    main()
