#!/usr/bin/env python
"""Convert an image-only PDF to markdown with RapidOCR (ONNX, CPU, offline).

Used for "Art of Paramaras.pdf", a 62-page scan with no text layer. The
project's usual OCR routes are unavailable: the Mistral path needs a dead
quota and an uninstalled client, and the Baidu Unlimited-OCR stack costs
~322 s/page on this CPU (~5.5 h for this book).

KNOWN LIMITS OF THIS ROUTE — recorded in the output header too:
  * Diacritics are not preserved. The model emits "Pasupata" for Pāśupata,
    "Saivite" for Śaivite. Do not quote spellings from this file; check them
    against a better source before they reach prose.
  * Character-level errors are common ("remins", "pattera", "aloag").
  * RapidOCR returns boxes in no useful order, so this script reconstructs
    reading order geometrically (column detection, then top-to-bottom,
    left-to-right). That fixes the scrambling but cannot be perfect on
    complex layouts.
  * Stray CJK glyphs are hallucinations of the bilingual model on an
    English/Sanskrit page; they are stripped.

    python ocr_rapid_to_markdown.py "Art of Paramaras.pdf" -o "out.md"
"""
from __future__ import annotations

import argparse
import re
import sys
import time
import unicodedata
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

CJK = re.compile(r"[　-鿿가-힯＀-￯]")


def order_boxes(items, page_w):
    """Reconstruct reading order from OCR boxes.

    items: list of (box, text, score); box is 4 (x, y) corners.
    Detects a two-column layout by looking for a vertical gutter — a band in
    the middle of the page that no text box centre falls into — and reads
    the left column fully before the right. Otherwise reads top-to-bottom.
    """
    rows = []
    for box, text, score in items:
        xs = [p[0] for p in box]
        ys = [p[1] for p in box]
        rows.append({
            "text": text, "score": score,
            "x0": min(xs), "xc": sum(xs) / len(xs),
            "yc": sum(ys) / len(ys),
            "h": max(ys) - min(ys),
        })
    if not rows:
        return []

    # Look for a gutter between 35% and 65% of the page width.
    # This scan is of two-page spreads, so the "gutter" is the real binding
    # between two printed pages and sits close to the middle. The search band
    # is wide (30-70%) and the required void modest (5% of width): demanding
    # more than that missed the gutter entirely and let text from the facing
    # page interleave into the left page's lines.
    centres = sorted(r["xc"] for r in rows)
    split = None
    lo, hi = page_w * 0.30, page_w * 0.70
    best_gap = 0.0
    for a, b in zip(centres, centres[1:]):
        if a < lo or b > hi:
            continue
        if (b - a) > best_gap:
            best_gap, split = b - a, (a + b) / 2
    if split is None or best_gap < page_w * 0.05:
        split = None

    line_tol = max(8.0, (sum(r["h"] for r in rows) / len(rows)) * 0.6)

    def sort_col(col):
        """Group boxes into text lines, then order each line left-to-right.

        The band's reference y is the FIRST box in the band and never moves.
        An earlier version averaged it in as boxes were added, which let the
        reference drift down the page so every following line still fell
        inside the tolerance — collapsing the whole column into one line.
        """
        col.sort(key=lambda r: r["yc"])
        out, cur, band_y = [], [], None
        for r in col:
            if band_y is None or (r["yc"] - band_y) <= line_tol:
                if band_y is None:
                    band_y = r["yc"]
                cur.append(r)
            else:
                out.append(sorted(cur, key=lambda z: z["x0"]))
                cur, band_y = [r], r["yc"]
        if cur:
            out.append(sorted(cur, key=lambda z: z["x0"]))
        return out

    if split is None:
        groups = sort_col(rows)
    else:
        left = [r for r in rows if r["xc"] < split]
        right = [r for r in rows if r["xc"] >= split]
        groups = sort_col(left) + sort_col(right)

    lines = []
    for g in groups:
        txt = " ".join(r["text"].strip() for r in g if r["text"].strip())
        if txt:
            lines.append(txt)
    return lines


def clean(line: str) -> str:
    line = unicodedata.normalize("NFC", line)
    line = CJK.sub("", line)                   # bilingual-model hallucinations
    line = re.sub(r"[ \t]{2,}", " ", line)
    return line.strip()


def main(argv=None):
    ap = argparse.ArgumentParser(description="OCR an image-only PDF to markdown")
    ap.add_argument("pdf")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--rotate", type=int, default=270,
                    help="degrees to rotate each page before OCR. This scan is "
                         "sideways: unrotated, every text line is a 107x1100 px "
                         "vertical box and reading order cannot be recovered. "
                         "270 yields horizontal full-width lines.")
    ap.add_argument("--title", default=None)
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args(argv)

    import pymupdf
    from rapidocr_onnxruntime import RapidOCR

    src = Path(args.pdf)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.parent / f"._{out.stem}_page.png"

    ocr = RapidOCR()
    doc = pymupdf.open(str(src))
    n = min(doc.page_count, args.limit or doc.page_count)
    title = args.title or src.stem

    header = [
        f"<!-- OCR of {src.name} via RapidOCR (ONNX, CPU) at {args.dpi} dpi; "
        f"{n} pages. -->",
        "<!-- QUALITY WARNING: this route does NOT preserve diacritics — it "
        "writes 'Pasupata' for Pāśupata, 'Saivite' for Śaivite. Character "
        "errors are common. Reading order was reconstructed geometrically "
        "(column detection + top-to-bottom), not taken from the OCR output "
        "order. Do not quote spellings from this file without checking them "
        "against the page image. -->",
        "",
        f"# {title}",
        "",
    ]

    zoom = args.dpi / 72.0
    matrix = pymupdf.Matrix(zoom, zoom).prerotate(args.rotate)

    body, t0 = [], time.time()
    for i in range(n):
        pix = doc[i].get_pixmap(matrix=matrix)
        pix.save(str(tmp))
        try:
            res, _ = ocr(str(tmp))
        except Exception as exc:                       # keep going on a bad page
            body += [f"<!-- page {i + 1} -->", f"*[OCR failed: {exc}]*", ""]
            continue
        lines = [clean(l) for l in order_boxes(res or [], pix.width)]
        lines = [l for l in lines if l]
        body.append(f"<!-- page {i + 1} -->")
        body.append("")
        if lines:
            body += lines + [""]
        else:
            body += ["*[No machine-readable text detected on this page — "
                     "blank page or full-page plate.]*", ""]
        done = i + 1
        rate = (time.time() - t0) / done
        print(f"  page {done}/{n}  {len(lines):>3} lines  "
              f"{rate:.1f}s/page  eta {rate * (n - done) / 60:.1f} min",
              flush=True)

    out.write_text("\n".join(header + body), encoding="utf-8")
    if tmp.exists():
        tmp.unlink()
    words = len(" ".join(body).split())
    print(f"\nwrote {out}  ({n} pages, {words:,} words, "
          f"{time.time() - t0:.0f}s total)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
