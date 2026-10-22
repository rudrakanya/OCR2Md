"""Gridded view of a page for reading native pixel coordinates: grid.py PAGE [x0 y0 x1 y1] [step]."""
import sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
W = Path(__file__).resolve().parents[1] / "_work"
n = int(sys.argv[1])
im = np.asarray(Image.open(W / "pages" / f"p{n:03d}.png").convert("RGB"))
x0, y0, x1, y1 = map(int, sys.argv[2:6]) if len(sys.argv) >= 6 else (0, 0, im.shape[1], im.shape[0])
step = int(sys.argv[6]) if len(sys.argv) > 6 else 200
crop = im[y0:y1, x0:x1]
f = min(1400 / crop.shape[1], 1400 / crop.shape[0], 1.0)
v = cv2.resize(crop, (int(crop.shape[1] * f), int(crop.shape[0] * f)), interpolation=cv2.INTER_AREA).copy()
for x in range((x0 // step + 1) * step, x1, step):
    X = int((x - x0) * f); cv2.line(v, (X, 0), (X, v.shape[0]), (255, 0, 255), 1)
    cv2.putText(v, str(x), (X + 2, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 255), 1)
for y in range((y0 // step + 1) * step, y1, step):
    Y = int((y - y0) * f); cv2.line(v, (0, Y), (v.shape[1], Y), (0, 160, 255), 1)
    cv2.putText(v, str(y), (2, Y - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 120, 255), 1)
Image.fromarray(v).save(W / f"grid_p{n:03d}.jpg", quality=88)
