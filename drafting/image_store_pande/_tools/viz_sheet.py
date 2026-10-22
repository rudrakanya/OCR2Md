"""Tile _work/viz/pNNN.jpg overlays into review sheets: viz_sheet.py OUT first last [cols]."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
W = Path(__file__).resolve().parents[1] / "_work"
out = sys.argv[1]
if sys.argv[2].startswith("@"):     # explicit page list: @11,13,16
    pages, cols = [int(x) for x in sys.argv[2][1:].split(",")], 6
else:
    pages = range(int(sys.argv[2]), int(sys.argv[3]) + 1)
    cols = int(sys.argv[4]) if len(sys.argv) > 4 else 6
fs = [W / "viz" / f"p{n:03d}.jpg" for n in pages if (W / "viz" / f"p{n:03d}.jpg").exists()]
TW, TH = 330, 440
rows = (len(fs) + cols - 1) // cols
sh = Image.new("RGB", (cols * TW, rows * TH), "white")
for k, f in enumerate(fs):
    im = Image.open(f); im.thumbnail((TW - 4, TH - 4)); sh.paste(im, ((k % cols) * TW, (k // cols) * TH))
sh.save(W / out, quality=85)
