"""Draw detected boxes on a page thumbnail for visual checking (free).
  python -I -X utf8 viz.py OUTDIR PAGE [PAGE ...]"""
import sys
from pathlib import Path

import cv2

from detect import detect

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
W = Path(__file__).resolve().parents[1] / "_work" / "pages"
for p in map(int, sys.argv[2:]):
    f = W / f"p{p:04d}.png"
    g = cv2.imread(str(f))
    for i, r in enumerate(detect(f)):
        x0, y0, x1, y1 = r["bbox"]
        cv2.rectangle(g, (x0, y0), (x1, y1), (0, 0, 255), 12)
        cv2.putText(g, str(i), (x0 + 20, y0 + 120), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 255), 10)
    s = 0.22
    cv2.imwrite(str(out / f"v{p:04d}.png"), cv2.resize(g, None, fx=s, fy=s, interpolation=cv2.INTER_AREA))
