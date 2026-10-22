"""Contact sheets of pages with detected picture boxes (red) and caption boxes (blue), for checking by eye.

  python -I -X utf8 drafting/image_store_hardy/_tools/viz.py 14 40 [OUT_DIR]   pages 14..40, 8 per sheet
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WORK, native_zoom, open_pdf, render  # noqa: E402
from detect import detect  # noqa: E402

SC = 0.16


def overlay(page, pno, caps, boxes=None):
    z = native_zoom(page)
    img = render(page, z * SC)
    if boxes is None:
        boxes = detect(page)["boxes"]
    for k, b in enumerate(boxes):
        b = [int(v * SC) for v in b]
        cv2.rectangle(img, (b[0], b[1]), (b[2], b[3]), (230, 0, 0), 2)
        cv2.putText(img, str(k), (b[0] + 3, b[1] + 14), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (230, 0, 0), 2)
    for c in caps:
        if c["page"] != pno:
            continue
        b = [int(v * SC) for v in c["bbox_px"]] if "bbox_px" in c else [int(v * z * SC) for v in c["bbox_pt"]]
        col = (0, 0, 230) if c["kind"] != "orphan" else (230, 140, 0)
        cv2.rectangle(img, (b[0], b[1]), (b[2], b[3]), col, 1)
        cv2.putText(img, c["label"] or "?", (b[0], b[1] - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.45, col, 1)
    cv2.putText(img, f"p{pno}", (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 140, 0), 2)
    return img


def sheet(imgs, path, per_row=4):
    h = max(i.shape[0] for i in imgs); w = max(i.shape[1] for i in imgs)
    rows = (len(imgs) + per_row - 1) // per_row
    S = np.full((h * rows, w * per_row, 3), 255, np.uint8)
    for k, i in enumerate(imgs):
        r, c = divmod(k, per_row)
        S[r * h:r * h + i.shape[0], c * w:c * w + i.shape[1]] = i
    cv2.imwrite(str(path), cv2.cvtColor(S, cv2.COLOR_RGB2BGR))


def main():
    a, b = int(sys.argv[1]), int(sys.argv[2])
    out = Path(sys.argv[3]) if len(sys.argv) > 3 else WORK / "viz"
    out.mkdir(parents=True, exist_ok=True)
    cf = WORK / "caption_regions.json"
    caps = json.loads((cf if cf.exists() else WORK / "captions.json").read_text(encoding="utf-8"))
    boxes = {}
    for name in ("detect.json", "boxes.json"):
        bf = WORK / name
        if bf.exists():
            j = json.loads(bf.read_text(encoding="utf-8"))
            boxes = {k: (v["boxes"] if isinstance(v, dict) else v) for k, v in j.items()}
    d = open_pdf()
    pages = [p for p in range(a, b + 1) if boxes.get(str(p)) or any(c["page"] == p for c in caps)]
    for s in range(0, len(pages), 8):
        chunk = pages[s:s + 8]
        imgs = [overlay(d[p - 1], p, caps, boxes.get(str(p))) for p in chunk]
        sheet(imgs, out / f"sheet_{chunk[0]:03d}_{chunk[-1]:03d}.png")
        print(out / f"sheet_{chunk[0]:03d}_{chunk[-1]:03d}.png")


if __name__ == "__main__":
    main()
