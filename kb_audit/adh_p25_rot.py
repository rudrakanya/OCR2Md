# -*- coding: utf-8 -*-
"""Page 25 read the right way up.

Straight OCR of page 25 returns stacked single letters: the page is a wide
iconographic inventory printed SIDEWAYS on a portrait leaf. Tesseract read the
columns as lines, which is exactly how 154 bodiless headers and a 45x repeated
row got into the markdown. Rotating the render first is the whole fix, so both
directions are tried and the better one kept.
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


def score(t):
    """Readable prose, not letter soup: how many real words per line."""
    words = re.findall(r"[A-Za-z\u0900-\u097F]{3,}", t)
    lines = [l for l in t.split("\n") if l.strip()]
    return len(words) / max(1, len(lines))


doc = pymupdf.open(PDF)
page = doc[24]
print("page 25 rect:", page.rect, "| rotation:", page.rotation)

results = {}
with tempfile.TemporaryDirectory() as td:
    img = pathlib.Path(td) / "p.png"
    for rot in (90, 270):
        pix = page.get_pixmap(dpi=400, matrix=pymupdf.Matrix(1, 1).prerotate(rot))
        img.write_bytes(pix.tobytes("png"))
        for lang, psm in (("eng", "6"), ("eng", "4")):
            r = subprocess.run([TESS, str(img), "stdout", "-l", lang, "--psm", psm],
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", env=env)
            t = (r.stdout or "").strip()
            key = f"rot{rot}/{lang}/psm{psm}"
            results[key] = t
            print(f"  {key:22s} chars={len(t):6d} words/line={score(t):5.2f}")
doc.close()

best_key = max(results, key=lambda k: score(results[k]))
best = results[best_key]
(ROOT / "kb_audit" / "adh_p25_rot.json").write_text(
    json.dumps({"best": best_key, "variants": results}, ensure_ascii=False, indent=1),
    encoding="utf-8")

print(f"\n########## PAGE 25, {best_key} ##########")
print(best)
