"""Coverage and gap report (§11).

    python -m src.report                  # writes ./corpus_report.md
    python -m src.report --stdout

The point of this report is the gap flags. Before you start writing C15 you
want to know that it rests on four chunks from one book, and you want to know
it now rather than three paragraphs into the draft.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import statistics
import sys
from pathlib import Path

from . import settings as st
from .store import Store, open_aligned


def build_report(cfg) -> str:
    # Align to the model that actually built the collection, or the header
    # will name whatever config.yaml happens to say — which is exactly the
    # provenance error this report exists to prevent.
    cfg, store = open_aligned(cfg, verbose=False)
    chapters = st.load_chapters(cfg)
    manifest = st.load_manifest(cfg)
    rows = store.all_chunks()
    if not rows:
        raise RuntimeError("collection is empty — run `python -m src.ingest --rebuild`")

    prov = st.provenance(cfg)
    thin_chunks = int(cfg.get_path("reporting.thin_chapter_chunks", 40))
    thin_books = int(cfg.get_path("reporting.thin_chapter_books", 2))

    by_book: dict[str, list[dict]] = collections.defaultdict(list)
    for r in rows:
        by_book[r["metadata"].get("source_path", "?")].append(r)

    out: list[str] = []
    w = out.append

    w("# Udaypur corpus — coverage report\n")
    w(f"Generated {dt.datetime.now():%Y-%m-%d %H:%M}  ·  "
      f"config `{prov['config_hash']}`  ·  model `{prov['embedding_model']}`  ·  "
      f"chunk target {prov['chunk_target_tokens']} tokens\n")

    # ── 1. chunk counts ─────────────────────────────────────────────────────
    total_tokens = sum(r["metadata"].get("token_count", 0) for r in rows)
    dupes = sum(1 for r in rows if r["metadata"].get("is_duplicate"))
    w("## 1. Corpus\n")
    w(f"**{len(rows):,} chunks** from **{len(by_book)} books**, "
      f"{total_tokens:,} tokens total. "
      f"{dupes:,} chunks ({dupes/len(rows):.1%}) are flagged as near-duplicates "
      f"of another chunk and are demoted at query time.\n")

    w("| Book | Chunks | Tokens | Median | Lang | Dup |")
    w("|---|---:|---:|---:|---|---:|")
    for src in sorted(by_book, key=lambda s: -len(by_book[s])):
        chunks = by_book[src]
        toks = [c["metadata"].get("token_count", 0) for c in chunks]
        langs = collections.Counter(c["metadata"].get("language", "?") for c in chunks)
        d = sum(1 for c in chunks if c["metadata"].get("is_duplicate"))
        title = manifest.get(src, {}).get("title", src)
        w(f"| {title[:58]} | {len(chunks):,} | {sum(toks):,} | "
          f"{int(statistics.median(toks))} | "
          f"{'/'.join(f'{k}:{v}' for k, v in langs.most_common(2))} | {d} |")
    w("")

    all_toks = sorted(r["metadata"].get("token_count", 0) for r in rows)
    def pct(p): return all_toks[min(len(all_toks) - 1, int(len(all_toks) * p))]
    w(f"Token distribution: min {all_toks[0]} · p05 {pct(.05)} · median {pct(.5)} · "
      f"p95 {pct(.95)} · max {all_toks[-1]}\n")

    langs = collections.Counter(r["metadata"].get("language", "?") for r in rows)
    w("Script/language mix: " + " · ".join(
        f"**{k}** {v:,} ({v/len(rows):.0%})" for k, v in langs.most_common()) + "\n")

    # ── 2. chapter coverage ────────────────────────────────────────────────
    w("## 2. Chapter coverage\n")
    w("`Chunks` counts every chunk tagged to the chapter; `Primary` counts those "
      "for which it is the single best match. `Books` is how many distinct "
      "sources feed it.\n")
    w("| Chapter | Title | Chunks | Primary | Books | Top sources |")
    w("|---|---|---:|---:|---:|---|")

    coverage: dict[str, dict] = {}
    for ch in chapters:
        cid = ch["id"]
        field = st.chapter_field(cid)
        tagged = [r for r in rows if r["metadata"].get(field)]
        primary = [r for r in rows if r["metadata"].get("primary_chapter") == cid]
        books = collections.Counter(r["metadata"].get("source_path", "?") for r in tagged)
        coverage[cid] = {"tagged": len(tagged), "primary": len(primary),
                         "books": books, "title": ch["title"]}
        top = ", ".join(f"{manifest.get(b, {}).get('title', b)[:26]} ({n})"
                        for b, n in books.most_common(3))
        w(f"| **{cid}** | {ch['title'][:38]} | {len(tagged):,} | {len(primary):,} | "
          f"{len(books)} | {top} |")
    w("")

    # ── 3. gap flags ───────────────────────────────────────────────────────
    w("## 3. Gap flags\n")
    gaps = []
    for cid, c in coverage.items():
        reasons = []
        if c["tagged"] < thin_chunks:
            reasons.append(f"only {c['tagged']} chunks tagged (threshold {thin_chunks})")
        if len(c["books"]) < thin_books:
            reasons.append(f"fed by only {len(c['books'])} book(s)")
        if c["primary"] == 0:
            reasons.append("**no chunk has this as its primary chapter** — "
                           "nothing in the corpus is mainly about it")
        elif c["primary"] < 10:
            reasons.append(f"only {c['primary']} chunks are primarily about it")
        # Concentration: one book supplying most of the evidence.
        if c["books"]:
            top_book, top_n = c["books"].most_common(1)[0]
            share = top_n / max(1, c["tagged"])
            if share > 0.6 and c["tagged"] > 0:
                reasons.append(
                    f"{share:.0%} of its chunks come from a single source "
                    f"(*{manifest.get(top_book, {}).get('title', top_book)[:40]}*) "
                    "— concentration risk")
        if reasons:
            gaps.append((cid, c["title"], reasons))

    if not gaps:
        w("No chapter tripped a gap flag.\n")
    else:
        for cid, title, reasons in gaps:
            w(f"- **{cid} {title}** — " + "; ".join(reasons))
        w("")
    w(f"*{len(gaps)} of {len(chapters)} chapters flagged. A flag is a prompt to "
      "look, not a verdict: run `python -m src.tag --explain "
      f"{gaps[0][0] if gaps else 'C08'}` to see what was actually caught.*\n")

    # ── 4. cross-book overlap ──────────────────────────────────────────────
    w("## 4. Cross-book concentration\n")
    w("Chapters drawing on many books are well corroborated; a chapter resting "
      "on one book inherits that book's blind spots.\n")
    ranked = sorted(coverage.items(), key=lambda kv: -len(kv[1]["books"]))
    w("| Chapter | Distinct books | Top source share |")
    w("|---|---:|---:|")
    for cid, c in ranked:
        if not c["books"]:
            w(f"| {cid} | 0 | — |")
            continue
        _, top_n = c["books"].most_common(1)[0]
        w(f"| {cid} | {len(c['books'])} | {top_n / max(1, c['tagged']):.0%} |")
    w("")

    # Which books are doing the work overall.
    w("### Books by chapter reach\n")
    reach: dict[str, set] = collections.defaultdict(set)
    for r in rows:
        src = r["metadata"].get("source_path", "?")
        for cid in (r["metadata"].get("chapters_str") or "").split(","):
            if cid:
                reach[src].add(cid)
    w("| Book | Chapters it feeds |")
    w("|---|---|")
    for src, cids in sorted(reach.items(), key=lambda kv: -len(kv[1])):
        w(f"| {manifest.get(src, {}).get('title', src)[:50]} | "
          f"{len(cids)} — {', '.join(sorted(cids))} |")
    w("")

    # ── 5. tagging confidence ──────────────────────────────────────────────
    low = [r for r in rows if r["metadata"].get("chap_low_confidence")]
    w("## 5. Tagging confidence\n")
    w(f"{len(low):,} chunks ({len(low)/len(rows):.1%}) have their top two "
      "chapters within the low-confidence margin — the assignment between those "
      "two is close to arbitrary. These are the chunks an optional LLM "
      "verification pass would target (`tagging.llm_verification`, off by "
      "default).\n")
    scores = [r["metadata"].get("chap_score_primary", 0.0) for r in rows]
    if scores:
        s = sorted(scores)
        w(f"Primary-match similarity: min {s[0]:.3f} · median {s[len(s)//2]:.3f} · "
          f"max {s[-1]:.3f}\n")

    w("---\n")
    w(f"*Libraries: " + ", ".join(f"{k} {v}" for k, v in prov["libraries"].items()
                                  if v != "not-installed") + "*")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Coverage and gap report")
    ap.add_argument("--stdout", action="store_true", help="print instead of writing")
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)

    cfg = st.load()
    text = build_report(cfg)
    if args.stdout:
        print(text)
        return 0
    path = Path(args.out) if args.out else st.resolve(cfg, "reporting.out_path")
    path.write_text(text, encoding="utf-8")
    print(f"wrote {path}  ({len(text.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
