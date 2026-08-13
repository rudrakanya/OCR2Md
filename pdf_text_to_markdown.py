#!/usr/bin/env python3
"""
pdf_text_to_markdown.py — extract a born-digital PDF's text layer to Markdown.

Not every source needs OCR. A PDF that already carries a text layer has the
characters exactly right, and running a vision model over it can only introduce
errors while costing hours — Unlimited-OCR measured 322 s/page on this machine,
so a 335-page book is a 30-hour job to recover text that pymupdf reads in ten
seconds. What OCR buys for such a file is *layout* (`<|det|>` element types and
bounding boxes), which is worth having on pages where layout carries meaning and
worth nothing on running prose.

So this handles the text, `ocr_layout.py --local` handles the pages that need
labels, and the two write the same conventions:

    <!-- page N -->     page provenance md_clean.py reads and strips
    ## Heading          from font size, not guesswork about capitalisation
    <!-- element:X -->  structural labels, where known

Heading detection is by type size relative to the document's body text, which
is the one signal a text layer gives that a plain string dump throws away.

Usage:
    python pdf_text_to_markdown.py book.pdf --out "Udaypur Reference Markdown Files"
    python pdf_text_to_markdown.py book.pdf --report        # inspect, write nothing
"""
import argparse
import re
import statistics
import sys
from collections import Counter
from pathlib import Path


def _load(path):
    try:
        import pymupdf
    except ImportError:
        try:
            import fitz as pymupdf                    # older name
        except ImportError as e:
            raise SystemExit(
                "pymupdf is required:\n    pip install pymupdf\n"
                "(or run this with .venv-ocr\\Scripts\\python.exe, which has it)") from e
    return pymupdf.open(path)


# A line of an AITM-style translation: "7-8." or "23." opening a verse block.
VERSE_RE = re.compile(r"^\s*\d{1,3}(?:\s*[-–]\s*\d{1,3})?\s*[.:]")
# Running heads and folios: a bare number, or a short line repeated per page.
FOLIO_RE = re.compile(r"^\s*\d{1,4}\s*$")


def page_lines(page):
    """Lines with their dominant font size, in reading order."""
    out = []
    data = page.get_text("dict")
    for block in data.get("blocks", []):
        if block.get("type") != 0:                    # 0 = text
            continue
        for line in block.get("lines", []):
            spans = [s for s in line.get("spans", []) if (s.get("text") or "").strip()]
            if not spans:
                continue
            text = "".join(s["text"] for s in line["spans"])
            size = max(s.get("size", 0) for s in spans)
            bold = any("bold" in (s.get("font", "").lower()) for s in spans)
            out.append({"text": text.rstrip(), "size": round(size, 1), "bold": bold})
    return out


def body_size(doc, sample=40):
    """The document's body type size — the mode of all line sizes."""
    sizes = Counter()
    step = max(1, doc.page_count // sample)
    for i in range(0, doc.page_count, step):
        for ln in page_lines(doc.load_page(i)):
            if len(ln["text"].strip()) > 30:          # ignore headings and folios
                sizes[ln["size"]] += 1
    return sizes.most_common(1)[0][0] if sizes else 10.0


def find_running_heads(doc, sample=60):
    """Short lines that recur across many pages — the running head and folio."""
    seen = Counter()
    step = max(1, doc.page_count // sample)
    for i in range(0, doc.page_count, step):
        lines = page_lines(doc.load_page(i))
        for ln in (lines[:1] + lines[-1:]):
            s = ln["text"].strip()
            if 0 < len(s) <= 60 and not FOLIO_RE.match(s):
                seen[s] += 1
    return {s for s, n in seen.items() if n >= 4}


def dehyphenate(text):
    """Rejoin words the typesetter broke across a line ending in '-'.

    The AITM setting hyphenates heavily ('sa-\\ncred'), and leaving those breaks
    in would put 'sa' and 'cred' into the index as separate tokens.
    """
    text = re.sub(r"(\w)[-­]\s*\n\s*(\w)", r"\1\2", text)
    return text


def page_to_markdown(page, pno, body, heads, verse_min=2):
    """One page -> markdown lines, plus whether it looks verse-dense."""
    lines = page_lines(page)
    out, verse_hits = [], 0
    for ln in lines:
        s = ln["text"].strip()
        if not s or s in heads or FOLIO_RE.match(s):
            continue                                  # page furniture
        if VERSE_RE.match(s):
            verse_hits += 1
        # A heading is meaningfully larger than body text, or bold and short.
        if ln["size"] >= body + 1.2 or (ln["bold"] and len(s) < 70):
            level = "#" if ln["size"] >= body + 3 else "##"
            out.append(f"\n{level} {s}\n")
        else:
            out.append(ln["text"])
    md = dehyphenate("\n".join(out))
    # Rejoin wrapped prose: a line not ending in sentence punctuation continues.
    md = re.sub(r"(?<![.!?:;\"'\)\]])\n(?=[a-zà-ɏ])", " ", md)
    return md.strip(), verse_hits >= verse_min


def convert(pdf_path, out_dir=None, report=False):
    doc = _load(pdf_path)
    body = body_size(doc)
    heads = find_running_heads(doc)
    print(f"{Path(pdf_path).name}: {doc.page_count} pages, body type {body}pt, "
          f"{len(heads)} running head(s) detected", flush=True)

    parts, verse_pages, empty = [], [], []
    for i in range(doc.page_count):
        md, is_verse = page_to_markdown(doc.load_page(i), i + 1, body, heads)
        if not md.strip():
            empty.append(i + 1)
            continue
        if is_verse:
            verse_pages.append(i + 1)
        parts.append(f"<!-- page {i + 1} -->\n{md}")
    doc.close()

    body_md = "\n\n".join(parts)
    print(f"  {len(body_md):,} chars, {len(verse_pages)} verse-dense page(s), "
          f"{len(empty)} empty page(s)")
    if report:
        print(f"  verse pages: {_ranges(verse_pages)}")
        return None, verse_pages

    out_dir = Path(out_dir or ".")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / (Path(pdf_path).stem + ".md")
    out.write_text(body_md + "\n", encoding="utf-8")
    print(f"  -> {out}")
    return out, verse_pages


def _ranges(nums):
    """Compact a page list: [1,2,3,7,8] -> '1-3, 7-8'."""
    if not nums:
        return "(none)"
    runs, start, prev = [], nums[0], nums[0]
    for n in nums[1:]:
        if n != prev + 1:
            runs.append((start, prev)); start = n
        prev = n
    runs.append((start, prev))
    return ", ".join(f"{a}" if a == b else f"{a}-{b}" for a, b in runs)


def main():
    from console import use_utf8
    use_utf8()
    ap = argparse.ArgumentParser(description="Extract a PDF's text layer to Markdown")
    ap.add_argument("pdf")
    ap.add_argument("--out", default="Udaypur Reference Markdown Files")
    ap.add_argument("--report", action="store_true", help="inspect only, write nothing")
    ap.add_argument("--verse-list", help="write the verse-dense page list here")
    args = ap.parse_args()

    if not Path(args.pdf).exists():
        print(f"ERROR: {args.pdf} not found"); sys.exit(1)
    out, verse = convert(args.pdf, args.out, args.report)
    if args.verse_list and verse:
        Path(args.verse_list).write_text(_ranges(verse), encoding="utf-8")
        print(f"  verse pages -> {args.verse_list}")
    if out:
        print("\nNext:\n"
              "  python build_kb.py            # re-index (fingerprint will change)\n"
              "  python label_chunks.py --all  # label the new chunks\n"
              f"  python ocr_layout.py --local \"{args.pdf}\" --first N --last M   "
              "# layout for the verse pages")


if __name__ == "__main__":
    main()
