"""Edge audit: for each region, its four borders at 1/2 scale (a 260-px strip across each side, quad drawn 1 px)
so a crop that runs onto text/caption or cuts into the photo shows. audit.py DETECT.json [pages] -> _work/audit/"""
import json, sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
W = Path(__file__).resolve().parents[1] / "_work"
det = json.loads((W / sys.argv[1]).read_text())
pages = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else sorted(map(int, det))
out = W / "audit"; out.mkdir(exist_ok=True)
F = ImageFont.truetype("arialbd.ttf", 22)
tiles = []
for p in pages:
    img = np.asarray(Image.open(W / "pages" / f"p{p:03d}.png").convert("RGB")).copy()
    H, Wd = img.shape[:2]
    figs = det[str(p)]["figs"]
    for f in figs:
        cv2.polylines(img, [np.int32(f["quad"])], True, (255, 0, 255), 3)
    for i, f in enumerate(figs):
        x0, y0, x1, y1 = f["box"]
        m = 110
        strips = [img[max(0, y0 - m):y0 + m, max(0, x0 - m):min(Wd, x1 + m)],       # top
                  img[max(0, y1 - m):min(H, y1 + m), max(0, x0 - m):min(Wd, x1 + m)],  # bottom
                  img[max(0, y0 - m):min(H, y1 + m), max(0, x0 - m):x0 + m],         # left
                  img[max(0, y0 - m):min(H, y1 + m), max(0, x1 - m):min(Wd, x1 + m)]]  # right
        # left/right strips turned to lie flat (left: top of page to the left; right: top to the right), so
        # every region is four horizontal strips: top, bottom, left, right
        strips[2] = np.rot90(strips[2], 1); strips[3] = np.rot90(strips[3], -1)
        WT = 1000
        rs = []
        for t in strips:
            sc = WT / t.shape[1]
            rs.append(cv2.resize(t, (WT, max(1, int(t.shape[0] * sc))), interpolation=cv2.INTER_AREA))
        hh = 30 + sum(r.shape[0] + 6 for r in rs)
        T = Image.new("RGB", (WT, hh), "white")
        y = 30
        for r in rs:
            T.paste(Image.fromarray(r), (0, y)); y += r.shape[0] + 6
        d = ImageDraw.Draw(T)
        d.text((4, 4), f"p{p} region {i}  {f.get('sides_from', '')}   strips: top / bottom / left / right", fill=(200, 0, 0), font=F)
        tiles.append(T)
k = 0
while tiles:
    batch, h = [], 0
    while tiles and h + tiles[0].height < 2600:
        t = tiles.pop(0); batch.append(t); h += t.height + 8
    if not batch:
        batch = [tiles.pop(0)]
    Wm = max(t.width for t in batch)
    S = Image.new("RGB", (Wm, sum(t.height + 8 for t in batch)), (120, 120, 120))
    y = 0
    for t in batch:
        S.paste(t, (0, y)); y += t.height + 8
    S.save(out / f"a{k:02d}.jpg", quality=85); k += 1
print(k, "audit sheets")
