#!/usr/bin/env python3
"""
contextualize.py — situating preambles for chunks (§2.2).

Before embedding, each chunk gets a 1-3 sentence preamble locating it in its
document:

    From Cunningham's 1880 ASI report on the Bhilsa region, in the section
    describing the Udayeśvara temple's plan; this passage gives the measured
    dimensions of the maṇḍapa.

A chunk that begins "It is 42 feet across at the base" is nearly unretrievable
on its own: no query mentions "it". The preamble restores what the surrounding
document made obvious and chunking threw away. It is prepended at embed time
only — v1's heading-trail pattern, stored once rather than twice — and stripped
from what the drafter sees as evidence.

THE NO-NEW-FACTS CHECK IS NOT OPTIONAL
--------------------------------------
§8 names this the plan's sharpest risk, and it is right: a hallucinated preamble
is worse than no preamble, because it is invisible at draft time and carries the
index's authority. If a preamble invents "Cunningham's 1880 report" for a source
that is neither Cunningham's nor 1880, that fabrication becomes a retrievable,
citable part of the knowledge base.

So every proper noun and numeral in a generated preamble must already appear in
the dossier, the heading trail, or the chunk itself. Anything else is rejected,
and the chunk falls back to a deterministic preamble built purely from metadata
the pipeline already holds. Rejections are counted and reported — a high rate
means the prompt is drifting, not that the check is too strict.

Usage:
    python contextualize.py --sample 40      # try it, inspect, spend nothing else
    python contextualize.py --all            # the full pass (an overnight run)
    python contextualize.py --report
    # then, to make them count:
    python build_kb.py --force
"""
import argparse
import json
import os
import sys
from pathlib import Path

from config import CFG
from console import use_utf8
from doc_understanding import load_all
from llm import complete_json, get_client, parallel
from textnorm import WORD_RE, fold, numerals, proper_nouns

KB_DIR = Path(os.environ.get("KB_DIR", "kb"))
CONTEXT_PATH = KB_DIR / "contexts.json"

SYSTEM = """You write one short situating preamble for a passage extracted from a scholarly \
source, so that the passage can be found and understood on its own.

HARD CONSTRAINT — you may ONLY restate information given to you in the dossier, the heading \
trail, or the passage itself. You must NOT add any fact from your own knowledge: no author, no \
date, no place, no monument, no measurement that is not already in the material provided. If \
you do not know who wrote the source, do not say. A preamble containing an invented detail is \
worse than no preamble at all, because it will be indexed and cited as if it were the source's.

Write 1-3 sentences, at most 55 words. Say: which source this is from, where in it this passage \
sits, and what the passage is about. Plain declarative prose, no bullet points, no quotation.

Return JSON only: {"context": "..."}"""


def deterministic_context(source, chunk, dossier=None):
    """A preamble assembled from metadata only. Cannot hallucinate.

    Used as the fallback whenever generation is rejected or unavailable, so a
    failed check degrades to something correct rather than to nothing.
    """
    bits = []
    title = ((dossier or {}).get("identity") or {}).get("title") or source
    genre = (dossier or {}).get("genre")
    bits.append(f"From {title}" + (f", a {genre}" if genre else "") + ".")
    trail = (chunk.get("trail") or "").strip()
    if trail:
        bits.append(f"Section: {trail}.")
    if chunk.get("page_start"):
        pe = chunk.get("page_end")
        bits.append(f"Page {chunk['page_start']}." if pe in (None, chunk["page_start"])
                    else f"Pages {chunk['page_start']}-{pe}.")
    return " ".join(bits)


def allowed_vocabulary(source, chunk, dossier):
    """Folded tokens the preamble is permitted to draw proper nouns from."""
    parts = [source.replace("_", " ").replace("-", " "), chunk.get("trail") or "",
             chunk.get("heading") or "", chunk.get("text") or ""]
    if dossier:
        ident = dossier.get("identity") or {}
        cov = dossier.get("coverage") or {}
        parts += [str(ident.get(k) or "") for k in ("author", "title", "publisher", "year")]
        parts += [dossier.get("genre") or "", dossier.get("stance") or "",
                  dossier.get("summary") or ""]
        parts += [str(x) for x in (cov.get("geography") or [])]
        parts += [str(x) for x in (cov.get("monuments") or [])]
        parts += [str(cov.get("period_from") or ""), str(cov.get("period_to") or "")]
        parts += [s.get("trail", "") for s in (dossier.get("structure") or [])]
    blob = "\n".join(parts)
    return {fold(w) for w in WORD_RE.findall(blob)} - {""}, set(numerals(blob))


def check_no_new_facts(context, source, chunk, dossier):
    """Return the list of unsupported terms in a preamble. Empty means clean."""
    vocab, nums = allowed_vocabulary(source, chunk, dossier)
    bad = []
    for t in proper_nouns(context):
        k = fold(t)
        if k and k not in vocab:
            bad.append(t)
    for n in numerals(context):
        if n not in nums:
            bad.append(n)
    return bad


def generate(client, model, source, chunk, dossier, cfg=None):
    """One preamble. Returns (text, 'llm' | 'rejected' | 'fallback', rejected_terms)."""
    cfg = cfg or CFG
    d = dossier or {}
    brief = {
        "filename": source,
        "identity": d.get("identity"),
        "genre": d.get("genre"),
        "kind": d.get("kind"),
        "stance": (d.get("stance") or "")[:400],
        "document_summary": (d.get("summary") or "")[:1200],
    }
    msgs = [{"role": "system", "content": SYSTEM},
            {"role": "user", "content":
                f"DOSSIER:\n{json.dumps(brief, ensure_ascii=False)}\n\n"
                f"HEADING TRAIL: {chunk.get('trail') or '(none)'}\n"
                f"PAGE: {chunk.get('page_start')}\n\n"
                f"PASSAGE:\n{(chunk.get('text') or '')[:2400]}"}]
    try:
        data = complete_json(client, model, msgs, max_tokens=400, temperature=0.1, quiet=True)
        text = " ".join((data.get("context") or "").split())
    except Exception:                                 # noqa: BLE001
        return deterministic_context(source, chunk, dossier), "fallback", []
    if not text:
        return deterministic_context(source, chunk, dossier), "fallback", []
    if cfg.comprehension.enforce_no_new_facts:
        bad = check_no_new_facts(text, source, chunk, dossier)
        if bad:
            return deterministic_context(source, chunk, dossier), "rejected", bad
    return text, "llm", []


def load_contexts(path=CONTEXT_PATH):
    if Path(path).exists():
        return json.loads(Path(path).read_text(encoding="utf-8"))
    return {}


def save_contexts(ctx, path=CONTEXT_PATH):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(ctx, ensure_ascii=False, indent=0), encoding="utf-8")


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Generate situating preambles for chunks")
    ap.add_argument("--all", action="store_true", help="every chunk (an overnight run)")
    ap.add_argument("--sample", type=int, help="only N chunks, spread across sources")
    ap.add_argument("--source", help="one source only")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--force", action="store_true", help="regenerate existing preambles")
    args = ap.parse_args()

    chunks_path = KB_DIR / "chunks.jsonl"
    if not chunks_path.exists():
        print(f"ERROR: {chunks_path} not found — run build_kb.py first"); sys.exit(1)
    chunks = [json.loads(l) for l in chunks_path.read_text(encoding="utf-8").splitlines()]
    ctx = load_contexts()

    if args.report:
        print(f"{len(ctx):,} of {len(chunks):,} chunks have a preamble "
              f"({len(ctx) / max(len(chunks), 1) * 100:.1f}%)")
        kinds = {}
        for v in ctx.values():
            kinds[v.get("how", "?")] = kinds.get(v.get("how", "?"), 0) + 1
        for k, n in sorted(kinds.items()):
            print(f"  {k:10s} {n:6,}")
        rej = [v for v in ctx.values() if v.get("how") == "rejected"]
        if rej:
            print(f"\n{len(rej)} preamble(s) rejected by the no-new-facts check. Sample of "
                  f"what they tried to introduce:")
            for v in rej[:12]:
                print(f"    {', '.join(v.get('rejected', []))[:100]}")
        return

    targets = list(enumerate(chunks))
    if args.source:
        targets = [(i, c) for i, c in targets if c["source"] == args.source]
    if not args.force:
        targets = [(i, c) for i, c in targets if str(i) not in ctx]
    if args.sample:
        step = max(1, len(targets) // args.sample)
        targets = targets[::step][:args.sample]
    elif not args.all and not args.source:
        print("Refusing to run the full pass implicitly — it is thousands of API calls.\n"
              "Try it first:   python contextualize.py --sample 40\n"
              "Then commit:    python contextualize.py --all")
        return
    if not targets:
        print("Nothing to do — every selected chunk already has a preamble."); return

    dossiers = load_all()
    if not dossiers:
        print("WARNING: no dossiers found. Preambles will be much weaker without them.\n"
              "         Run doc_understanding.py first.", file=sys.stderr)
    client = get_client()
    model = CFG.comprehension.model
    print(f"generating {len(targets):,} preamble(s) with {model} ...", flush=True)

    def one(job):
        i, c = job
        text, how, bad = generate(client, model, c["source"], c, dossiers.get(c["source"]))
        return i, {"context": text, "how": how, "rejected": bad}

    def failed(job, e):
        i, c = job
        return i, {"context": deterministic_context(c["source"], c, dossiers.get(c["source"])),
                   "how": "fallback", "rejected": [], "error": type(e).__name__}

    done = 0
    for start in range(0, len(targets), 200):          # checkpoint every 200
        batch = targets[start:start + 200]
        for i, rec in parallel(one, batch, workers=args.workers, stagger=0.2, on_error=failed):
            ctx[str(i)] = rec
        done += len(batch)
        save_contexts(ctx)
        counts = {}
        for v in ctx.values():
            counts[v.get("how")] = counts.get(v.get("how"), 0) + 1
        print(f"  {done:,}/{len(targets):,}  {counts}", flush=True)

    save_contexts(ctx)
    rejected = sum(1 for v in ctx.values() if v.get("how") == "rejected")
    print(f"\nWrote {len(ctx):,} preambles -> {CONTEXT_PATH}")
    if rejected:
        rate = rejected / max(len(ctx), 1) * 100
        print(f"{rejected:,} ({rate:.1f}%) were REJECTED for introducing facts not in the "
              f"dossier, trail or passage, and fell back to metadata-only preambles.")
        if rate > 15:
            print("That rate is high enough to suspect the prompt rather than the check. "
                  "Inspect with --report before embedding.")
    print("\nTo make these count: python build_kb.py --force")


if __name__ == "__main__":
    main()
