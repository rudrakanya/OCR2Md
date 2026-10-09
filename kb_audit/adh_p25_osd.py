# -*- coding: utf-8 -*-
"""Page 25, oriented by Tesseract's own orientation detector.

Guessing the rotation produced upside-down text ("jo" for "of", "ayy" for
"the" - the 180-degree signature), so the angle is asked for rather than
assumed: --psm 0 reports it, and the page is then rotated by exactly that much
before being read. Rendering stays at dpi=72, the resolution these pages are
actually stored at.
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
    words = re.findall(r"[A-Za-z]{3,}", t)
    lines = [l for l in t.split("\n") if l.strip()]
    return round(len(words) / max(1, len(lines)), 2)


def real_words(t):
    """Fraction of tokens that are plausible English - the test upside-down
    text fails even when it looks line-like."""
    toks = re.findall(r"[A-Za-z]{3,}", t.lower())
    common = {"the", "and", "of", "in", "is", "are", "with", "temple", "image",
              "images", "hand", "right", "left", "panel", "stone", "figure",
              "damaged", "features", "attributes", "location", "other", "this",
              "which", "from", "has", "have", "been", "its", "upper", "lower"}
    hits = sum(1 for t_ in toks if t_ in common)
    return round(hits / max(1, len(toks)), 3)


def osd(path):
    r = subprocess.run([TESS, str(path), "stdout", "--psm", "0"],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env)
    m = re.search(r"Rotate: (\d+)", r.stdout or "")
    c = re.search(r"Orientation confidence: ([\d.]+)", r.stdout or "")
    return (int(m.group(1)) if m else None,
            float(c.group(1)) if c else None,
            (r.stdout or r.stderr or "").strip()[:160])


def run(path, psm="6"):
    r = subprocess.run([TESS, str(path), "stdout", "-l", "eng", "--psm", psm],
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
        angle, conf, raw = osd(base)
        print(f"\npage {pno}: OSD says rotate {angle} (confidence {conf}) | {raw[:90]}")

        variants = {}
        for deg in (0, 90, 180, 270):
            p = td / f"p{pno}_{deg}.png"
            # PIL rotates counter-clockwise; Tesseract reports the clockwise
            # rotation needed, so every quadrant is tried and scored.
            im.rotate(-deg, expand=True).save(p)
            t = run(p)
            variants[f"cw{deg}"] = t
            print(f"   cw{deg:<4d} chars={len(t):6d} words/line={quality(t):6.2f} "
                  f"english={real_words(t):6.1%}")
        out[pno] = {"osd_rotate": angle, "osd_conf": conf, "variants": variants}
doc.close()

(ROOT / "kb_audit" / "adh_p25_osd.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

best = max(out[25]["variants"], key=lambda k: real_words(out[25]["variants"][k]))
print(f"\n########## PAGE 25 — {best} (english {real_words(out[25]['variants'][best]):.1%}) ##########")
print(out[25]["variants"][best])
