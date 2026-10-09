#!/usr/bin/env python3
"""
combine_page_markdowns.py — join per-image OCR Markdown into one book file.

ocr_to_markdown.py writes one .md per input image, which is right for photos of
book pages but leaves a photographed book as N loose files. This joins them back
into a single document in page order.

The output is byte-for-byte the shape ocr_to_markdown.py produces for a PDF —
a provenance header followed by `<!-- page N -->` markers — so a photographed
book and a scanned PDF are indistinguishable downstream, and md_clean.py /
build_kb.py ingest it with no special case. Each marker also carries the source
photo (`<!-- page 7 src=20260817_154624.jpg -->`); md_clean.PAGE_RE tolerates
the extra attribute, so page provenance survives all the way into a chunk.

Page order is filename order. Camera timestamps sort chronologically, which is
capture order, which is page order — provided the book was shot front to back.

    python combine_page_markdowns.py output/book1_pages -o "out/Book.md" --title "..."
"""
import argparse
import re
from pathlib import Path

import md_clean

HEADER_RE = re.compile(r"^<!--\s*OCR of .*?-->\s*", re.S)
EMPTY_NOTE = ("*[No machine-readable text detected on this page — "
              "blank page or full-page plate/illustration in the source.]*")


def combine(pages_dir: Path, title: str, model: str, strip_slivers: bool = True,
            wide_slivers: bool = False):
    files = sorted(p for p in pages_dir.glob("*.md") if not p.name.startswith("_"))
    if not files:
        raise SystemExit(f"No page Markdown found in {pages_dir}")

    out = [f"<!-- OCR of {title} via Mistral {model}; {len(files)} pages -->\n"]
    empty, stripped = [], 0
    for n, f in enumerate(files, 1):
        body = HEADER_RE.sub("", f.read_text(encoding="utf-8")).strip()
        # Slivers are stripped per page, so a run can never be joined across a
        # page boundary, and a page reduced to nothing but sliver is reported
        # as empty rather than left holding debris.
        if strip_slivers:
            body, dropped = md_clean.strip_sliver_runs(body, wide=wide_slivers)
            body = body.strip()
            stripped += dropped
        src = f.with_suffix(".jpg").name
        out.append(f"\n\n<!-- page {n} src={src} -->\n\n")
        if not body or body == EMPTY_NOTE:
            empty.append(n)
            out.append(EMPTY_NOTE)
        else:
            out.append(body)
    return "".join(out), files, empty, stripped


def main():
    ap = argparse.ArgumentParser(description="Join per-image OCR Markdown into one book file")
    ap.add_argument("pages_dir", help="Directory of per-image .md files")
    ap.add_argument("-o", "--output", required=True, help="Combined .md path")
    ap.add_argument("--title", required=True, help="Source name recorded in the header")
    ap.add_argument("--model", default="mistral-ocr-4", help="Model recorded in the header")
    ap.add_argument("--keep-slivers", action="store_true",
                    help="Keep the facing-page strips the camera caught (default: strip them)")
    ap.add_argument("--wide-slivers", action="store_true",
                    help="Also strip wider strips (short words, not just <=4-char stems). "
                         "Catches far more debris in a photographed book, but a table of "
                         "short cells can look the same — check the diff before trusting it")
    args = ap.parse_args()

    text, files, empty, stripped = combine(Path(args.pages_dir), args.title, args.model,
                                           strip_slivers=not args.keep_slivers,
                                           wide_slivers=args.wide_slivers)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")

    print(f"pages combined : {len(files)}  ({files[0].stem} -> {files[-1].stem})")
    print(f"pages with no text: {len(empty)}" + (f"  {empty}" if empty else ""))
    if not args.keep_slivers:
        print(f"sliver lines removed: {stripped}")
    print(f"written        : {out}  ({out.stat().st_size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
