# -*- coding: utf-8 -*-
"""What does ADH page 25 actually hold?

The markdown attributes 205 of its 226 pipe blocks to this single page: 154 are
a header with no rows under it, and one garbled row repeats 45 times. So the
question is not "where is the table" but "how many rows does page 25 really
have, and how many reached the KB".

OCR'd at 400 dpi in both scripts and two page-segmentation modes, because the
row count is exactly what psm changes: psm 6 reads the page as one block and
runs columns together, psm 4 expects variable-width columns.
"""
import json
import os
import pathlib
import re
import subprocess
import tempfile

import pymupdf

TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
ROOT = pathlib.Path(__file__).resolve().parent.parent
PDF = ROOT / "remaining pdf" / "Some Paramara Templess.pdf"

env = dict(os.environ)
env["TESSDATA_PREFIX"] = str(pathlib.Path.home() / "tessdata")

doc = pymupdf.open(PDF)
print(f"{PDF.name}: {doc.page_count} pages")

out = {}
with tempfile.TemporaryDirectory() as td:
    img = pathlib.Path(td) / "p.png"
    for pno in (24, 25, 26):
        page = doc[pno - 1]
        layer = page.get_text("text").strip()
        img.write_bytes(page.get_pixmap(dpi=400).tobytes("png"))
        variants = {}
        for lang, psm in (("eng", "6"), ("eng", "4"), ("Devanagari+eng", "6")):
            r = subprocess.run([TESS, str(img), "stdout", "-l", lang, "--psm", psm],
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", env=env)
            t = (r.stdout or "").strip()
            variants[f"{lang}/psm{psm}"] = {"rc": r.returncode, "chars": len(t), "text": t}
        out[pno] = {"text_layer_chars": len(layer), "variants": variants}
        print(f"\n=== page {pno} | text layer {len(layer)} chars ===")
        for k, v in variants.items():
            print(f"  {k:18s} rc={v['rc']} chars={v['chars']}")
doc.close()

(ROOT / "kb_audit" / "adh_page25.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

# the best reading of page 25, printed in full so rows can be counted by eye
best = max(out[25]["variants"].items(), key=lambda kv: kv[1]["chars"])
print(f"\n########## PAGE 25, {best[0]} ({best[1]['chars']} chars) ##########")
print(best[1]["text"])
