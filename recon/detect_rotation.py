#!/usr/bin/env python3
"""Decide which way to turn the page photographs that carry no EXIF rotation.

Most of the photographs record their orientation in EXIF, but 61 of Book 2's do
not: they are stored landscape with the flag set to "normal", so nothing in the
file says which edge is the top. The page itself is the only evidence, so each
candidate rotation is put through OCR and scored on how much confident text it
yields — text read the right way up scores far higher than text read sideways.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps
from rapidocr_onnxruntime import RapidOCR

THUMB = 1100          # enough for the detector, small enough to stay quick


def score(ocr, img):
    """Confidence-weighted character count: how much real text this way up."""
    res, _ = ocr(np.array(img))
    if not res:
        return 0.0
    return sum(float(conf) * len(text) for _, text, conf in res)


def main():
    targets = json.loads(Path(sys.argv[1]).read_text())
    out = {}
    ocr = RapidOCR()
    for i, path in enumerate(targets, 1):
        im = ImageOps.exif_transpose(Image.open(path))
        thumb = im.copy()
        thumb.thumbnail((THUMB, THUMB))
        cw = thumb.transpose(Image.ROTATE_270)     # 90 clockwise
        ccw = thumb.transpose(Image.ROTATE_90)     # 90 counter-clockwise
        s_cw, s_ccw = score(ocr, cw), score(ocr, ccw)
        winner = "cw" if s_cw >= s_ccw else "ccw"
        margin = abs(s_cw - s_ccw) / max(s_cw, s_ccw, 1)
        out[Path(path).stem] = {"rotate": winner, "score_cw": round(s_cw, 1),
                                "score_ccw": round(s_ccw, 1), "margin": round(margin, 3)}
        print(f"[{i}/{len(targets)}] {Path(path).name}: {winner} "
              f"(cw={s_cw:.0f} ccw={s_ccw:.0f} margin={margin:.2f})", flush=True)
    Path(sys.argv[2]).write_text(json.dumps(out, indent=1))
    print("written:", sys.argv[2])


if __name__ == "__main__":
    main()
