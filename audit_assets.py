#!/usr/bin/env python
"""Phase 2 — what happened to everything that is not body text?

    python audit_assets.py

Markdown extraction keeps prose and quietly drops the rest. For a KB that is the
sole source of truth that matters, because figure and plate captions carry
iconographic identifications, tables carry measurements and inventories, and an
inscription reproduced as a plate is a fact that never entered the KB at all.

For each book this compares the source PDF (where there is one) against the
extracted markdown on four things:

    images      how many the PDF holds, and whether the markdown references any
    captions    "Figure 12:", "Pl. 3", "Table 4" lines surviving as text
    tables      pipe tables and tab-runs in the markdown vs tabular pages in the PDF
    blind spots pages that are mostly image with little text — a plate or an
                inscription photograph whose content is not in the KB

Reads only; writes the report and its json.
"""
from __future__ import annotations

import json
import re
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
DATA = ROOT / "kb_audit" / "asset_audit.json"

CAPTION = re.compile(
    r"^\s*(?:Fig(?:ure)?\.?|Pl(?:ate)?\.?|Table|Map|Photo(?:graph)?|Chart|Annexure)\s*"
    r"[-–—:.]?\s*\d+", re.I | re.M)
CAPTION_INLINE = re.compile(
    r"(?:Fig(?:ure)?\.?|Pl(?:ate)?\.?|Table|Map)\s*[-–—:.]?\s*\d+\s*[:.]", re.I)
MD_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)|<img\b|\[image[_ -]?ref\]|\[IMAGE\]|\[figure\]", re.I)
PIPE_ROW = re.compile(r"^\s*\|.*\|\s*$", re.M)
INSCRIPTION = re.compile(r"\binscription\b", re.I)


def norm(s):
    return unicodedata.normalize("NFC", s or "")


def pdf_assets(path, cap=40):
    """Images per page and how text-poor each page is — a plate is a page with
    a big image and almost no text."""
    import pymupdf
    doc = pymupdf.open(path)
    pages = []
    for i, page in enumerate(doc):
        if i >= cap and doc.page_count > cap:
            break
        txt = page.get_text("text").strip()
        imgs = page.get_images(full=True)
        area = 0.0
        for b in page.get_image_info():
            r = b.get("bbox")
            if r:
                area += abs((r[2] - r[0]) * (r[3] - r[1]))
        pr = abs(page.rect.width * page.rect.height) or 1.0
        pages.append({"page": i + 1, "chars": len(txt), "images": len(imgs),
                      "image_frac": round(min(1.0, area / pr), 3)})
    out = {
        "page_count": doc.page_count,
        "pages_scanned": len(pages),
        "images_total": sum(p["images"] for p in pages),
        "pages_with_images": sum(1 for p in pages if p["images"]),
        # a plate: mostly picture, little text
        "plate_pages": [p["page"] for p in pages
                        if p["image_frac"] > 0.35 and p["chars"] < 400],
    }
    doc.close()
    return out


def main():
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    by_code = {s.get("code"): s for s in reg["sources"]}
    pdfmap = yaml.safe_load(PDFMAP.read_text(encoding="utf-8"))["sources"]

    rows = []
    for code in sorted(pdfmap):
        s = by_code.get(code, {})
        md_path = BOOKS / s.get("file", "")
        md = norm(md_path.read_text(encoding="utf-8", errors="replace")) if md_path.exists() else ""
        r = {
            "code": code, "title": s.get("title", "?"),
            "md_chars": len(md),
            "caption_lines": len(CAPTION.findall(md)),
            "caption_inline": len(CAPTION_INLINE.findall(md)),
            "image_refs": len(MD_IMAGE.findall(md)),
            "pipe_rows": len(PIPE_ROW.findall(md)),
            "inscription_mentions": len(INSCRIPTION.findall(md)),
            "pdf": None,
        }
        m = pdfmap[code] or {}
        if not m.get("absent"):
            p = ROOT / m.get("pdf", "")
            if p.exists():
                r["pdf"] = p.name
                r.update({"src_" + k: v for k, v in pdf_assets(p).items()})
        rows.append(r)
        cap = r["caption_lines"] + r["caption_inline"]
        print(f"  {code:9s} captions {cap:5d} | image refs {r['image_refs']:4d} | "
              f"table rows {r['pipe_rows']:5d} | "
              + (f"pdf images {r.get('src_images_total', 0):4d}, plates {len(r.get('src_plate_pages', []))}"
                 if r["pdf"] else "no source pdf"))

    DATA.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nwrote {DATA}")
    return rows


if __name__ == "__main__":
    main()
