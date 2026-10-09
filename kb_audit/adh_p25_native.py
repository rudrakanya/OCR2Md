# -*- coding: utf-8 -*-
"""Page 25 at the resolution it was actually scanned at.

Every page of this PDF stores exactly one pixel per point, so the stored scan
IS a 72-dpi-equivalent render; asking PyMuPDF for 400 dpi upscales it 5.6x and
OCR returns letter soup. Rendering at dpi=72 maps 1:1 onto the stored pixels.
A 2x PIL upscale is also tried because Tesseract prefers ~300 dpi of glyph
height, and that is an interpolation of real pixels rather than invented ones.
"""
import json
import os
import pathlib
import re
import subprocess
import tempfile

import pymupdf
from PIL import Image

TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
ROOT = pathlib.Path(__file__).resolve().parent.parent
PDF = ROOT / "remaining pdf" / "Some Paramara Templess.pdf"

env = dict(os.environ)
env["TESSDATA_PREFIX"] = str(pathlib.Path.home() / "tessdata")


def quality(t):
    """Words per non-blank line: letter soup scores under ~1.5, prose over 5."""
    words = re.findall(r"[A-Za-z\u0900-\u097F]{3,}", t)
    lines = [l for l in t.split("\n") if l.strip()]
    return round(len(words) / max(1, len(lines)), 2)


def run(img, lang, psm):
    r = subprocess.run([TESS, str(img), "stdout", "-l", lang, "--psm", psm],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env)
    return (r.stdout or "").strip()


doc = pymupdf.open(PDF)
out = {}
with tempfile.TemporaryDirectory() as td:
    td = pathlib.Path(td)
    for pno in (24, 25, 26):
        page = doc[pno - 1]
        base = td / f"p{pno}.png"
        base.write_bytes(page.get_pixmap(dpi=72).tobytes("png"))
        im = Image.open(base)
        up = td / f"p{pno}_2x.png"
        im.resize((im.width * 2, im.height * 2), Image.LANCZOS).save(up)
        rot = td / f"p{pno}_rot.png"
        im.rotate(270, expand=True).save(rot)

        variants = {}
        for label, path, lang, psm in (
                ("native/psm6", base, "eng", "6"),
                ("native/psm4", base, "eng", "4"),
                ("2x/psm6", up, "eng", "6"),
                ("2x/psm4", up, "eng", "4"),
                ("rot270/psm6", rot, "eng", "6")):
            t = run(path, lang, psm)
            variants[label] = t
        out[pno] = variants
        print(f"\npage {pno} ({im.width}x{im.height} px native)")
        for k, v in variants.items():
            print(f"   {k:14s} chars={len(v):6d} words/line={quality(v):6.2f}")
doc.close()

(ROOT / "kb_audit" / "adh_p25_native.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

best = max(out[25], key=lambda k: quality(out[25][k]))
print(f"\n########## PAGE 25 — {best} ##########")
print(out[25][best])
