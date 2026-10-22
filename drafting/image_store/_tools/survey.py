"""Survey the Paramāra inscriptions PDF (free, local): cache each page's embedded scan losslessly and
Tesseract the header strip, to find the plate pages and their printed labels.

  python -I -X utf8 drafting/image_store/_tools/survey.py
Writes _work/pages/pNNNN.png (native embedded scan, lossless) and _work/survey.jsonl.
"""
import io
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
PDF = ROOT / "PDF Originals" / "Inscriptions of the Paramaras.pdf"
STORE = Path(__file__).resolve().parents[1]
WORK = STORE / "_work"
PAGES = WORK / "pages"
TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def tess(img, psm="6"):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    r = subprocess.run([TESS, "stdin", "stdout", "--psm", psm, "-l", "eng"], input=buf.getvalue(),
                       capture_output=True)
    return r.stdout.decode("utf-8", "replace").strip()


def main():
    PAGES.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(PDF)
    out = (WORK / "survey.jsonl").open("w", encoding="utf-8")
    for i in range(doc.page_count):
        pno = i + 1
        imgs = doc[i].get_images(full=True)
        x = doc.extract_image(imgs[0][0])
        im = Image.open(io.BytesIO(x["image"]))
        p = PAGES / f"p{pno:04d}.png"
        if not p.exists():
            im.save(p, optimize=True)
        g = np.asarray(im.convert("L"))
        h, w = g.shape
        ink = float((g < 128).mean())
        head = tess(im.crop((0, 0, w, int(h * 0.12))))
        rec = {"page": pno, "w": w, "h": h, "mode": im.mode, "n_images": len(imgs), "bpc": x.get("bpc"),
               "ink": round(ink, 4), "header_ocr": head}
        out.write(json.dumps(rec, ensure_ascii=False) + "\n")
        out.flush()
        if pno % 50 == 0:
            print(pno, file=sys.stderr)
    out.close()


if __name__ == "__main__":
    main()
