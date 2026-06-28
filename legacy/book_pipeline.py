#!/usr/bin/env python3
"""
Local pipeline for finishing the book transcriptions with Claude Code subagents
(no Anthropic API credits used).

Modes
  prep      : (a) split File 2's already-done pages out of the existing
              Temple_Economics.md into per-page .md files, and
              (b) rasterize every still-missing page to a JPEG.
              Writes _pages/manifest.json listing every page that still needs
              a transcription (img path + target .md path) — this drives the
              subagent assignment.
  assemble  : rebuild each book's .md from the per-page .md files
              (_pages/fF/pN.md), in page order, with a placeholder for any
              page still lacking a transcription.

Per-page transcriptions live at _pages/f{file}/p{page}.md ; page images at
_pages/f{file}/p{page}.jpg . Needs poppler on PATH (for rasterize + page count).
"""

import argparse
import json
import os
import re

from pdf2image import convert_from_path
from pdf2image.pdf2image import pdfinfo_from_path

OUT_DIR = "output_books"
PAGES_DIR = "_pages"
DPI = 200

# file id -> (source pdf, output markdown)
FILES = {
    2: ("Temple Economics.pdf",       "Temple_Economics.md"),
    3: ("Temples of India.pdf",       "Temples_of_India.md"),
    4: ("The Hindu Temple Vol 2.pdf", "Hindu_Temple_Vol2.md"),
}


def page_count(pdf_path):
    return pdfinfo_from_path(pdf_path)["Pages"]


def split_existing_md(md_path, dest_dir):
    """Write each already-transcribed page of an existing book .md to
    dest/pN.md. Returns the set of pages that are still placeholders."""
    if not os.path.exists(md_path):
        return None
    text = open(md_path, encoding="utf-8").read()
    parts = re.split(r"(?m)^<!-- page (\d+) -->$", text)
    it = iter(parts[1:])                       # drop preamble
    missing = []
    for num, body in zip(it, it):
        n = int(num)
        body = body.strip()
        if "not yet transcribed" in body or not body:
            missing.append(n)
        else:
            with open(os.path.join(dest_dir, f"p{n}.md"), "w", encoding="utf-8") as f:
                f.write(body)
    return missing


def cmd_prep(args):
    os.makedirs(PAGES_DIR, exist_ok=True)
    manifest = []
    for fid, (pdf, outmd) in FILES.items():
        pdf_path = os.path.join(args.pdf_dir, pdf)
        dest = os.path.join(PAGES_DIR, f"f{fid}")
        os.makedirs(dest, exist_ok=True)
        total = page_count(pdf_path)

        existing_missing = split_existing_md(os.path.join(OUT_DIR, outmd), dest)
        missing = existing_missing if existing_missing is not None else list(range(1, total + 1))
        print(f"file {fid} ({pdf}): {total} pages, {len(missing)} to transcribe", flush=True)

        for p in missing:
            img = os.path.join(dest, f"p{p}.jpg")
            out = os.path.join(dest, f"p{p}.md")
            if os.path.exists(out):          # already transcribed by a subagent
                continue
            if not os.path.exists(img):
                im = convert_from_path(pdf_path, first_page=p, last_page=p, dpi=DPI, fmt="jpeg")[0]
                im.save(img, "JPEG", quality=85)
            manifest.append({
                "file": fid, "page": p,
                "img": img.replace("\\", "/"),
                "out": out.replace("\\", "/"),
            })
            if p % 25 == 0:
                print(f"  rasterized f{fid} p{p}", flush=True)

    with open(os.path.join(PAGES_DIR, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1)
    print(f"\nmanifest.json: {len(manifest)} page(s) still need transcription")


def cmd_assemble(args):
    for fid, (pdf, outmd) in FILES.items():
        pdf_path = os.path.join(args.pdf_dir, pdf)
        dest = os.path.join(PAGES_DIR, f"f{fid}")
        total = page_count(pdf_path)
        title = os.path.splitext(pdf)[0]
        out_path = os.path.join(OUT_DIR, outmd)
        missing = []
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"<!-- Markdown transcription of: {pdf} -->\n")
            f.write(f"<!-- {total} pages, transcribed via Claude Code -->\n")
            f.write(f"\n# {title}\n\n")
            for p in range(1, total + 1):
                f.write(f"<!-- page {p} -->\n\n")
                pm = os.path.join(dest, f"p{p}.md")
                if os.path.exists(pm):
                    body = open(pm, encoding="utf-8").read().strip()
                    if body and body != "<!-- no text content -->":
                        f.write(body + "\n\n")
                else:
                    missing.append(p)
                    f.write("<!-- page not yet transcribed -->\n\n")
        status = "COMPLETE" if not missing else f"{len(missing)} missing: {missing[:20]}"
        print(f"{outmd}: {status}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["prep", "assemble"])
    ap.add_argument("--pdf-dir", default="remaining texts")
    args = ap.parse_args()
    {"prep": cmd_prep, "assemble": cmd_assemble}[args.mode](args)


if __name__ == "__main__":
    main()
