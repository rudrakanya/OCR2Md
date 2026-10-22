"""Shared helpers for the Hardy image store (free, local).

The PDF is an Internet Archive scan: each page is a colour JPEG-2000 scan (2700 px wide, MRC: a hi-res layer
with a soft mask over a low-res background) with a hidden OCR text layer. We render the page at the scan's
native pixel width, so crops keep the full available resolution.
"""
import re
import unicodedata
from pathlib import Path

import numpy as np
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PDF = REPO / "PDF Originals" / "806955603-The-Temple-Architecture-of-India-Adam-Hardy.pdf"
WORK = ROOT / "_work"
BOOK = "HARDY2007"

# a caption opens with the chapter.figure number: "1.8 Stele at Parel ..." (OCR sometimes gives "1,8" / "1 .8")
CAP_RE = re.compile(r"^\s*(\d{1,2})\s?[.,·]\s?(\d{1,2})\s+(\S.*)$")
MAP_RE = re.compile(r"\bMap\s+(\d)\.\s")
CAP_MAX_H = 7.9      # caption lines are set small (line box ~6.4-7.2 pt); body text is ~8.8-9.0 pt


def open_pdf():
    return pymupdf.open(PDF)


def native_zoom(page):
    """Zoom that renders the page at the hi-res scan layer's own pixel width."""
    best = None
    for im in page.get_images(full=True):
        rects = page.get_image_rects(im[0])
        if rects and (best is None or im[2] > best[0]):
            best = (im[2], rects[0])
    w_px, r = best
    return w_px / r.width


def render(page, zoom):
    pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), colorspace=pymupdf.csRGB, alpha=False)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, 3).copy()


def lines(page):
    """Text-layer lines: (x0, y0, x1, y1, text, size)."""
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            s = "".join(sp["text"] for sp in l["spans"]).strip()
            if s:
                sz = max(sp["size"] for sp in l["spans"])
                out.append((*l["bbox"], s, sz))
    return out


def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def is_texty(s):
    """A line that reads as words (not OCR noise from inside a picture)."""
    words = s.split()
    if not words:
        return False
    good = sum(1 for w in words if re.fullmatch(r"[\(\[‘'\"“]?[A-Za-z][a-z]+[\)\]’'\"”,.;:!?]*|[a-z]{1,3}|\d+[a-z]{0,2}[,.;)]?|[A-Z]{2,}[,.]?|—|–|&", w))
    return good / len(words) >= 0.7 and sum(len(w) for w in words) >= 6
