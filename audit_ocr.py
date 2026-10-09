#!/usr/bin/env python
"""Phase 1 — is the extracted text faithful to the source pages?

    python audit_ocr.py              # sample pages per book
    python audit_ocr.py --pages 14   # sample harder
    python audit_ocr.py --book RAJM  # one book

Method, per sampled page:

  1. Read the PDF's own text layer (PyMuPDF). For a born-digital PDF that layer
     IS the page, so it is the ground truth to measure the markdown against.
  2. Where the layer is empty or near-empty the page is a scan, so render it and
     read it with RapidOCR instead — an independent reading, not the same
     extraction being compared with itself.
  3. Measure TOKEN RECALL: of the distinctive tokens on that page, how many
     appear anywhere in the book's markdown. Recall is the number that catches
     dropped text — gutter loss, margins, footnotes — without needing the
     markdown to be page-aligned.
  4. Measure script integrity separately: Devanagari on the page vs Devanagari
     in the markdown, because a pipeline can score well on Latin text while
     mangling every Sanskrit word.

Nothing here writes to the stores and nothing calls a paid API.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import os
import shutil
import statistics
import sys
import unicodedata
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
BOOKS = ROOT / "Udaypur Reference Markdown Files"
REGISTRY = ROOT / "kb_audit" / "source_registry.yaml"
PDFMAP = ROOT / "kb_audit" / "source_pdfs.yaml"
OUT = ROOT / "OCR_AUDIT.md"
DATA = ROOT / "kb_audit" / "ocr_audit.json"

DEVA = re.compile(r"[ऀ-ॿ]")
IAST = re.compile(r"[āīūṛṝḷṅñṭḍṇśṣḥṃṁēōĀĪŪṚṄÑṬḌṇŚṢḤṂ]")
WORD = re.compile(r"[A-Za-zऀ-ॿÀ-ɏ]{4,}")
# a four-digit year that cannot belong to this material
IMPOSSIBLE = re.compile(r"\b(?:19[5-9]\d|20[0-4]\d)\b")
RISKY_MIN_PAGES = 12


def norm(s):
    return unicodedata.normalize("NFC", s or "")


def tokens(s):
    return [w.lower() for w in WORD.findall(norm(s))]


def load_maps():
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    by_code = {s.get("code"): s for s in reg["sources"]}
    pdfmap = yaml.safe_load(PDFMAP.read_text(encoding="utf-8"))["sources"]
    return by_code, pdfmap


def page_text(page):
    """The page's own text layer, and whether it is substantial enough to trust."""
    t = norm(page.get_text("text"))
    return t, len(t.strip()) >= 120


TESS = next((q for q in (r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                         r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe")
             if Path(q).exists()), shutil.which("tesseract"))
TESSDATA = Path.home() / "tessdata"


def ocr_page(page, lang, dpi=400):
    """An independent reading of a scanned page, in the script it is written in.

    400 dpi and -l Devanagari match ocr_devanagari_to_markdown.py. RapidOCR is
    not used here: its default model has no Devanagari, and on a Sanskrit page it
    silently returns a handful of stray Latin tokens."""
    if not TESS:
        return "", "tesseract-missing"
    import subprocess, tempfile
    pix = page.get_pixmap(dpi=dpi)
    env = dict(os.environ)
    if TESSDATA.is_dir():
        env["TESSDATA_PREFIX"] = str(TESSDATA)
    with tempfile.TemporaryDirectory() as td:
        img = Path(td) / "page.png"
        img.write_bytes(pix.tobytes("png"))
        r = subprocess.run([TESS, str(img), "stdout", "-l", lang, "--psm", "3"],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", env=env)
    if r.returncode != 0:
        # a language pack problem is a fault in this audit, not in the book
        return "", f"tesseract-FAILED:{lang}:{(r.stderr or '').strip()[:80]}"
    return norm((r.stdout or "").strip()), f"tesseract:{lang}"


def script_of(md):
    """Which language pack this book needs, from what its markdown contains."""
    deva = len(DEVA.findall(md))
    return "Devanagari+eng" if deva > max(400, 0.01 * len(md)) else "eng"


# Books whose markdown is a TRANSLATION of the source pages. Token recall
# compares page words with markdown words, so for these it measures translation
# distance, not OCR fidelity, and must not be read as a fidelity grade.
TRANSLATIONS = {"RAJ-E", "TIW-E"}


def audit_book(code, src, mapping, n_pages):
    import pymupdf

    md_path = BOOKS / src.get("file", "")
    if not md_path.exists():
        return {"code": code, "status": "markdown missing", "pages": []}
    md = norm(md_path.read_text(encoding="utf-8", errors="replace"))
    md_tok = set(tokens(md))
    md_deva = len(DEVA.findall(md))
    lang = script_of(md)

    paths = [ROOT / mapping["pdf"]] + [ROOT / p for p in mapping.get("also", [])]
    paths = [p for p in paths if p.exists()]
    if not paths:
        return {"code": code, "status": "pdf missing on disk", "pages": []}

    results, scanned, digital = [], 0, 0
    for path in paths:
        doc = pymupdf.open(path)
        total = doc.page_count
        want = min(n_pages, total)
        # skip front matter, spread the sample across the body
        idxs = sorted({int(total * (0.08 + 0.84 * i / max(1, want - 1))) for i in range(want)})
        for i in idxs:
            page = doc[min(i, total - 1)]
            txt, solid = page_text(page)
            how = "text-layer"
            if not solid:
                txt, how = ocr_page(page, lang)
                scanned += 1
            else:
                digital += 1
            ptok = [t for t in tokens(txt) if t not in ("page", "fig", "plate")]
            uniq = set(ptok)
            recall = (len(uniq & md_tok) / len(uniq)) if uniq else None
            results.append({
                "pdf": path.name, "page": i + 1, "how": how,
                "chars": len(txt.strip()), "tokens": len(uniq),
                "recall": round(recall, 3) if recall is not None else None,
                "deva_page": len(DEVA.findall(txt)),
            })
        doc.close()

    rec = [r["recall"] for r in results if r["recall"] is not None]
    empty = [r for r in results if r["tokens"] < 12]
    low = [r for r in results if r["recall"] is not None and r["recall"] < 0.60]
    page_deva = sum(r["deva_page"] for r in results)
    return {
        "code": code, "status": "audited", "pages": results,
        "n_pages": len(results), "digital": digital, "scanned": scanned,
        "recall_mean": round(statistics.mean(rec), 3) if rec else None,
        "recall_min": round(min(rec), 3) if rec else None,
        "low_recall_pages": [r["page"] for r in low],
        "empty_pages": [r["page"] for r in empty],
        "page_devanagari": page_deva,
        "md_devanagari": md_deva,
        "md_iast": len(IAST.findall(md)),
        "md_chars": len(md),
        "impossible_dates": sorted(set(IMPOSSIBLE.findall(md)))[:12],
        "cite_markers": len(re.findall(r"\[cite:\s*\d+\]", md)),
        "illegible_markers": len(re.findall(r"\[illegible\]", md, re.I)),
        "ocr_lang": lang,
        "partial": bool(mapping.get("partial")),
        "risk": mapping.get("risk", ""),
    }


def grade(a):
    """pass / needs-recheck / re-OCR, from the measurements."""
    if a["status"] != "audited":
        return "unverifiable", "no source document to compare against"
    if a["code"] in TRANSLATIONS:
        return ("not-comparable",
                "the markdown is a translation of these pages, so token recall measures "
                f"translation distance, not OCR fidelity (measured {a['recall_mean']:.0%})"
                if a.get("recall_mean") is not None else
                "the markdown is a translation of these pages; fidelity is not measurable this way")
    r, lo = a["recall_mean"], len(a["low_recall_pages"])
    why = []
    if any(str(pg.get("how", "")).startswith("tesseract-FAILED") for pg in a["pages"]):
        return "tool-error", ("the OCR engine failed on these pages, so nothing about the book "
                              "is established: " + next(pg["how"] for pg in a["pages"]
                                                        if str(pg.get("how","")).startswith("tesseract-FAILED")))
    if r is None:
        return "re-OCR", "no readable text recovered from the sampled pages"
    if a["empty_pages"]:
        why.append(f"{len(a['empty_pages'])} sampled page(s) yielded almost no text")
    if a["page_devanagari"] > 40 and a["md_devanagari"] == 0:
        why.append("the pages carry Devanagari and the markdown has none")
    if r < 0.55:
        why.append(f"token recall {r:.0%}")
        return "re-OCR", "; ".join(why)
    if r < 0.78 or lo:
        if r < 0.78:
            why.append(f"token recall {r:.0%}")
        if lo:
            why.append(f"{lo} page(s) below 60% recall")
        return "needs-recheck", "; ".join(why)
    return "pass", f"token recall {r:.0%} across {a['n_pages']} sampled pages"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=8)
    ap.add_argument("--book")
    n = ap.parse_args()

    by_code, pdfmap = load_maps()
    audits = []
    for code in sorted(pdfmap):
        if n.book and code != n.book:
            continue
        m = pdfmap[code] or {}
        src = by_code.get(code, {})
        if m.get("absent"):
            audits.append({"code": code, "status": "source absent", "pages": [],
                           "risk": m.get("risk", ""), "md_chars": 0})
            print(f"  {code:9s} source absent — cannot verify")
            continue
        pages = max(n.pages, RISKY_MIN_PAGES) if m.get("risk") else n.pages
        a = audit_book(code, src, m, pages)
        a["title"] = src.get("title", "?")
        g, why = grade(a)
        a["grade"], a["why"] = g, why
        audits.append(a)
        print(f"  {code:9s} {g:14s} {why[:72]}")

    DATA.write_text(json.dumps(audits, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nwrote {DATA}")
    return audits


if __name__ == "__main__":
    main()
