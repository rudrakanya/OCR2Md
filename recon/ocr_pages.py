#!/usr/bin/env python3
"""Stage 2: OCR each page derivative, keeping the position of every word.

The book already has an excellent transcript from the Mistral pass, but that
transcript has no coordinates, and a PDF text layer needs to know where on the
page each phrase sits. So the derivatives are read again locally with RapidOCR,
which returns a quadrilateral per line. Nothing leaves the machine.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
OCR_WIDTH = 1800          # detection size; boxes are scaled back to page pixels


def run(paths, out_path):
    from rapidocr_onnxruntime import RapidOCR
    ocr = RapidOCR()
    results = {}
    for i, p in enumerate(paths, 1):
        p = Path(p)
        im = Image.open(p).convert("RGB")
        W, H = im.size
        small = im.copy()
        small.thumbnail((OCR_WIDTH, OCR_WIDTH))
        sx, sy = W / small.width, H / small.height
        try:
            res, _ = ocr(np.array(small))
        except Exception as e:                      # noqa: BLE001
            results[p.stem] = {"error": f"{type(e).__name__}: {e}"[:200], "lines": []}
            print(f"[{i}/{len(paths)}] {p.stem}: ERROR", flush=True)
            continue
        lines = []
        for box, text, conf in (res or []):
            xs = [pt[0] * sx for pt in box]
            ys = [pt[1] * sy for pt in box]
            lines.append({"text": text, "conf": round(float(conf), 3),
                          "x0": min(xs), "y0": min(ys), "x1": max(xs), "y1": max(ys)})
        results[p.stem] = {"width": W, "height": H, "lines": lines}
        print(f"[{i}/{len(paths)}] {p.stem}: {len(lines)} lines", flush=True)
    Path(out_path).write_text(json.dumps(results), encoding="utf-8")
    print("written:", out_path)


if __name__ == "__main__":
    run(json.loads(Path(sys.argv[1]).read_text()), sys.argv[2])
