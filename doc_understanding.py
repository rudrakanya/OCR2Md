#!/usr/bin/env python3
"""
doc_understanding.py — one dossier per source (§2.1).

The corpus is 24 files and ~11 MB. That is small enough to read every document
in full with an LLM, once, and keep the understanding as data. Most RAG systems
cannot afford this; this one can, and it is the highest-value addition in the
plan because it converts judgement that currently lives only in the drafting
model's general knowledge into something inspectable.

The load-bearing fields are `stance` and `reliability_notes`. In a corpus mixing
19th-century ASI survey, an 11th-century Sanskrit śilpa treatise, modern
epigraphy and a 2022 INTACH conservation report, *who is asserting a thing*
determines how it should be weighed and how it must be presented in the prose.
"Cunningham says the temple was built in 1059" and "the praśasti dates it to
1059" are not the same sentence, and only the dossier knows why.

Each dossier is cached to kb/_docs/<source>.json, hand-editable, and never
regenerated silently — the blueprint.py hierarchy-cache precedent. Re-run with
--force to rebuild one.

Feeds:
  sources.py    proposes the (kind, contribution) rows it currently holds by hand
  kb_store      the `sources` table, which drives metadata filtering (§3.6)
  blueprint.py  conflict adjudication gains a "who is more authoritative here" axis
  draft_chapter the drafting prompt gains each source's stance

Usage:
    python doc_understanding.py                    # every source missing a dossier
    python doc_understanding.py --source bhojdev.md --force
    python doc_understanding.py --sync             # push metadata into kb_store
    python doc_understanding.py --report           # table of what is known
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

from config import CFG
from console import use_utf8
from llm import Truncated, complete_json, get_client, parallel

KB_DIR = Path(os.environ.get("KB_DIR", "kb"))
DOCS_DIR = KB_DIR / "_docs"
SRC_DIR = Path("Udaypur Reference Markdown Files")

SYSTEM = """You are a research librarian building a source dossier for a scholarly history of \
the Udayeśvara (Nīlakaṇṭheśvara) temple at Udaypur, Vidisha district, Madhya Pradesh, and the \
Paramāra dynasty of Malwa.

You will be shown a source document (possibly in windows). Produce a dossier describing WHAT \
THIS SOURCE IS and HOW IT SHOULD BE WEIGHED — not a summary of the subject matter.

Be precise about provenance and honest about uncertainty:
- If the author, date or publisher is not stated in the text, use null. Do NOT infer them from \
your general knowledge of the field, and do NOT guess.
- `kind`: "primary" only if the source is itself the historical object — a Sanskrit treatise, an \
edition of inscriptions, a colonial-era or government record compiled from direct survey, \
testimony gathered from residents, or measured field documentation. "secondary" is modern \
scholarly interpretation. "tertiary" is general reference or synthesis.
- `stance` is the single most useful field: one or two sentences on the source's viewpoint, era \
and characteristic biases, and on which of its claims are dependable versus superseded. \
E.g. "colonial-era survey; attributions often superseded, measurements reliable".
- `reliability_notes`: specific, checkable cautions. OCR damage, missing plates, a polemical \
agenda, dates that disagree with the consensus.
- `coverage.period_from` / `period_to`: the CE years the source's *content* covers, as integers \
(negative for BCE). Null if it has no meaningful period.
- `caveats`: anything that would mislead a reader who trusted this source uncritically.

Return JSON only, exactly this shape:
{"identity": {"author": null, "title": "...", "year": null, "publisher": null, "edition": null},
 "kind": "primary|secondary|tertiary",
 "genre": "survey report|epigraphic corpus|temple monograph|Sanskrit silpa text|gazetteer|\
conservation report|regional history|iconographic manual|hydrological study|oral history|other",
 "coverage": {"period_from": null, "period_to": null, "geography": ["..."], "monuments": ["..."]},
 "stance": "...",
 "reliability_notes": ["..."],
 "summary": "<= 400 words on what the document is and contains",
 "key_claims": ["the specific claims this source is cited FOR"],
 "caveats": ["..."]}"""

WINDOW_SYSTEM = """You are reading one window of a longer source document and taking notes that \
will be merged into a dossier. Return JSON only:
{"sections": [{"trail": "heading path as printed", "summary": "<= 40 words"}],
 "observations": ["provenance, dating, bias, OCR damage, or anything bearing on reliability"]}
Report only what this window shows. Do not speculate about the rest of the document."""


def read_windows(path, width):
    """Split a source into readable windows at heading boundaries where possible."""
    text = Path(path).read_text(encoding="utf-8")
    if len(text) <= width:
        return [text]
    out, buf = [], []
    size = 0
    for line in text.split("\n"):
        if size + len(line) > width and buf:
            out.append("\n".join(buf))
            buf, size = [], 0
        buf.append(line)
        size += len(line) + 1
    if buf:
        out.append("\n".join(buf))
    return out


def _window_notes(client, model, source, windows):
    """Skim every window; return (sections, observations)."""
    def one(job):
        i, w = job
        msgs = [{"role": "system", "content": WINDOW_SYSTEM},
                {"role": "user", "content": f"SOURCE: {source}\nWINDOW {i + 1}/{len(windows)}\n\n{w}"}]
        return complete_json(client, model, msgs, max_tokens=3000, temperature=0.1, quiet=True)

    def failed(job, e):
        print(f"    window {job[0] + 1} failed: {type(e).__name__}", file=sys.stderr)
        return {}

    got = parallel(one, list(enumerate(windows)), workers=4, stagger=0.4, on_error=failed)
    sections, obs = [], []
    for g in got:
        for s in (g or {}).get("sections", []):
            if s.get("trail"):
                sections.append({"trail": s["trail"][:200], "summary": (s.get("summary") or "")[:300]})
        obs += [o for o in (g or {}).get("observations", []) if o]
    return sections, obs


def build_dossier(client, source, path, cfg=None, force=False):
    """Produce (and cache) one source's dossier."""
    cfg = cfg or CFG
    out = DOCS_DIR / f"{source}.json"
    if out.exists() and not force:
        return json.loads(out.read_text(encoding="utf-8")), False

    model = cfg.comprehension.model
    windows = read_windows(path, cfg.comprehension.read_window_chars)
    print(f"  {source[:52]:54s} {len(windows):3d} window(s)", flush=True)

    sections, observations = _window_notes(client, model, source, windows)

    # The dossier call sees the head of the document (where provenance lives),
    # the section map, and the reliability observations — not the whole text,
    # which would not fit and would bury the identity fields.
    head = Path(path).read_text(encoding="utf-8")[:18000]
    brief = {
        "filename": source,
        "size_chars": Path(path).stat().st_size,
        "section_map": [s["trail"] for s in sections[:200]],
        "window_observations": observations[:60],
    }
    msgs = [{"role": "system", "content": SYSTEM},
            {"role": "user", "content":
                f"FILENAME: {source}\n\nWHAT THE SKIM FOUND:\n"
                f"{json.dumps(brief, ensure_ascii=False)[:14000]}\n\n"
                f"OPENING OF THE DOCUMENT:\n{head}"}]
    try:
        data = complete_json(client, model, msgs, max_tokens=6000, temperature=0.1)
    except Truncated:
        data = complete_json(client, model, msgs, max_tokens=12000, temperature=0.1)

    data["source"] = source
    data["structure"] = sections
    data["_generated"] = {"model": model, "windows": len(windows),
                          "config": cfg.section_hash("comprehension")}
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return data, True


def load_all(docs_dir=DOCS_DIR):
    """{source: dossier} for every dossier on disk."""
    if not Path(docs_dir).exists():
        return {}
    out = {}
    for p in sorted(Path(docs_dir).glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            out[d.get("source") or p.stem] = d
        except Exception as e:                        # noqa: BLE001
            print(f"  skipping unreadable dossier {p.name}: {e}", file=sys.stderr)
    return out


def sync_to_store(dossiers, store=None, report=True):
    """Push dossier metadata into kb_store.sources, which drives §3.6 filtering.

    `kind` is taken from sources.CLASSIFICATION where a human has set it, and
    from the dossier only where none exists. The dossier is a model's reading of
    a scanned book and it gets this wrong in ways that matter: it classed
    bhojdev.md — a Hindi study of Bhoja — as a primary Sanskrit śilpa text, and
    demoted both the epigraphic corpus and the Udaypur inscription edition to
    secondary. Since `kind` now filters retrieval, a sub-topic asking for
    inscriptional evidence would have been served modern commentary and denied
    the inscriptions themselves.

    Everything else (genre, period, geography, stance) comes from the dossier,
    where a wrong guess costs recall rather than misattributing evidence.
    """
    from kb_store import KBStore
    import sources as src_mod
    store = store or KBStore()
    disagreements = []
    for src, d in dossiers.items():
        cov = d.get("coverage") or {}
        curated = src_mod.CLASSIFICATION.get(src, (None, None))[0]
        proposed = d.get("kind")
        if curated and proposed and curated != proposed:
            disagreements.append((src, proposed, curated))
        store.set_source_meta(
            src,
            kind=curated or proposed,
            genre=d.get("genre"),
            period_from=cov.get("period_from"),
            period_to=cov.get("period_to"),
            geography=cov.get("geography") or [],
            stance=d.get("stance") or "",
            reliability=d.get("reliability_notes") or [],
            summary=(d.get("summary") or "")[:4000])
    if report and disagreements:
        print(f"\n{len(disagreements)} dossier(s) disagree with sources.CLASSIFICATION on "
              f"`kind`. The curated value was used; the dossier's is shown for review:")
        for src, proposed, curated in disagreements:
            print(f"    {src[:46]:48s} dossier={proposed:10s} curated={curated} (used)")
    return len(dossiers)


def propose_sources_entries(dossiers):
    """Draft sources.py rows from the dossiers, for human confirmation.

    Deliberately printed rather than written: sources.py is the citation
    authority, and a bibliography that a model edited without review is exactly
    the failure v1's lookup table was built to prevent.
    """
    lines = []
    for src, d in sorted(dossiers.items()):
        ident = d.get("identity") or {}
        author = (ident.get("author") or "").strip()
        title = (ident.get("title") or src).strip()
        year = ident.get("year")
        pub = (ident.get("publisher") or "").strip()
        short = f"{author.split(',')[0]}, *{title}*" if author else f"*{title}*"
        full = ", ".join(x for x in [author, f"*{title}*", pub, str(year) if year else ""] if x)
        lines.append(f'    {src!r}: (\n        {short!r},\n        {full + "."!r}),')
    return "\n".join(lines)


def main():
    use_utf8()
    ap = argparse.ArgumentParser(description="Build per-source dossiers")
    ap.add_argument("--src-dir", default=str(SRC_DIR))
    ap.add_argument("--source", help="one filename only")
    ap.add_argument("--force", action="store_true", help="rebuild even if cached")
    ap.add_argument("--sync", action="store_true", help="push metadata into kb_store")
    ap.add_argument("--report", action="store_true", help="table of what is known")
    ap.add_argument("--propose-sources", action="store_true",
                    help="draft sources.py rows for review")
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()

    if args.report or args.propose_sources or args.sync:
        dossiers = load_all()
        if not dossiers:
            print("No dossiers yet. Run: python doc_understanding.py"); return
        if args.report:
            print(f"{'source':46s} {'kind':10s} {'genre':22s} {'period':13s} secs")
            print("-" * 104)
            for src, d in sorted(dossiers.items()):
                cov = d.get("coverage") or {}
                per = f"{cov.get('period_from') or '?'}–{cov.get('period_to') or '?'}"
                print(f"{src[:45]:46s} {(d.get('kind') or '?'):10s} "
                      f"{(d.get('genre') or '?')[:21]:22s} {per:13s} {len(d.get('structure') or [])}")
            missing = [s for s, d in dossiers.items() if not d.get("stance")]
            if missing:
                print(f"\n{len(missing)} dossier(s) have no stance recorded: {missing}")
        if args.propose_sources:
            print("\n# Draft rows for sources.SOURCES — REVIEW before pasting.\n"
                  "# Anything the dossier could not establish is left as the filename.\n")
            print(propose_sources_entries(dossiers))
        if args.sync:
            n = sync_to_store(dossiers)
            print(f"\nSynced {n} source(s) into kb_store.sources — metadata filtering is live.")
        return

    files = sorted(Path(args.src_dir).glob("*.md"))
    if args.source:
        files = [f for f in files if f.name == args.source]
    if not files:
        print(f"ERROR: no matching .md files in {args.src_dir}"); sys.exit(1)

    client = get_client()
    built = cached = 0
    for f in files:
        try:
            _, fresh = build_dossier(client, f.name, f, force=args.force)
            built += fresh
            cached += (not fresh)
        except Exception as e:                        # noqa: BLE001 - one bad source must
            print(f"  FAILED {f.name}: {type(e).__name__}: {e}", file=sys.stderr)  # not stop the rest
    print(f"\n{built} dossier(s) built, {cached} already cached -> {DOCS_DIR}/")
    if built:
        print("Next: python doc_understanding.py --sync --report")


if __name__ == "__main__":
    main()
