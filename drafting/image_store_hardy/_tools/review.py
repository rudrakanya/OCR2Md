"""Review sheets: picture boxes labelled "index:figure-label" (red; magenta when unmatched), caption regions
(blue), and a 50-pt grid (green ticks) for placing hand boxes in overrides.json.

  python -I -X utf8 drafting/image_store_hardy/_tools/review.py 1 264 [--scale 0.16] [--per 8] [--pages 12,76]
"""
import argparse
import json
import sys
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WORK, native_zoom, open_pdf, render  # noqa: E402
from plan import plan  # noqa: E402
from viz import sheet  # noqa: E402

TOOLS = Path(__file__).resolve().parent


def overlay(page, p, figs, caps, sc):
    z = native_zoom(page)
    img = render(page, z * sc)
    H, W = img.shape[:2]
    for g in range(0, int(W / (z * sc)) + 1, 50):
        x = int(g * z * sc)
        cv2.line(img, (x, 0), (x, 6), (0, 160, 0), 1)
        cv2.putText(img, str(g), (x + 1, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 140, 0), 1)
    for g in range(0, int(H / (z * sc)) + 1, 50):
        y = int(g * z * sc)
        cv2.line(img, (0, y), (6, y), (0, 160, 0), 1)
        cv2.putText(img, str(g), (1, y - 1), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 140, 0), 1)
    for c in caps:
        if c["page"] != p:
            continue
        b = [int(v * sc) for v in c["bbox_px"]]
        col = (0, 0, 230) if c["kind"] != "orphan" else (230, 140, 0)
        cv2.rectangle(img, (b[0], b[1]), (b[2], b[3]), col, 1)
        cv2.putText(img, c.get("label") or c["kind"][:4], (b[0], b[3] + 11), cv2.FONT_HERSHEY_SIMPLEX, 0.4, col, 1)
    for f in figs:
        if f["page"] != p:
            continue
        col = (230, 0, 0) if f["label"] else (200, 0, 200)
        for i, b in zip(f["box_ids"], f["boxes"]):
            b = [int(v * sc) for v in b]
            cv2.rectangle(img, (b[0], b[1]), (b[2], b[3]), col, 2)
            cv2.putText(img, f"{i}:{f['label'] or '?'}", (b[0] + 3, b[1] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, col, 2)
    cv2.putText(img, f"p{p}", (W - 60, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 140, 0), 2)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a", type=int)
    ap.add_argument("b", type=int)
    ap.add_argument("--scale", type=float, default=0.16)
    ap.add_argument("--per", type=int, default=8)
    ap.add_argument("--pages")
    ap.add_argument("--out", default=str(WORK / "review"))
    a = ap.parse_args()
    d = open_pdf()
    ovr, det, caps, figs = plan(d)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    if a.pages:
        pages = [int(x) for x in a.pages.split(",")]
    else:
        pages = [p for p in range(a.a, a.b + 1) if any(f["page"] == p for f in figs) or any(c["page"] == p for c in caps)]
    for s in range(0, len(pages), a.per):
        chunk = pages[s:s + a.per]
        imgs = [overlay(d[p - 1], p, figs, caps, a.scale) for p in chunk]
        path = out / f"r_{chunk[0]:03d}_{chunk[-1]:03d}.png"
        sheet(imgs, path, per_row=min(4, a.per))
        print(path)
    for f in figs:
        if f["how"] in ("UNMATCHED", "CAPTION WITHOUT PICTURE"):
            print(f["how"], f.get("page") or f.get("caption_page"), f["label"], f["box_ids"])


if __name__ == "__main__":
    main()
