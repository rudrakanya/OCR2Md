"""Caption review sheets: each record's caption crop (a little context around the OCR box) under a header with
its label and the List wording, ~8 per sheet -> _work/review/capNN.jpg. And thumbnail sheets of the plate
crops with labels -> _work/review/imgNN.jpg."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "_work"
import sys
TH_ = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
R = [r for r in json.loads((W / "build_records.json").read_text(encoding="utf-8")) if r.get("file")]
RC = [r for r in R if (r.get("list_vs_page_similarity") or 0) < TH_]
(W / "review").mkdir(exist_ok=True)
try:
    F = ImageFont.truetype("arial.ttf", 20); FB = ImageFont.truetype("arialbd.ttf", 22)
except OSError:
    F = FB = ImageFont.load_default()

pages = {}
def page(n):
    if n not in pages:
        pages.clear(); pages[n] = Image.open(W / "pages" / f"p{n:03d}.png").convert("RGB")
    return pages[n]

WD = 1300
tiles = []
for r in RC:
    b = r.get("caption_box")
    head = f'{r["label"]}  (p{r["page"]}, sim {r.get("list_vs_page_similarity")})  LIST: {r["caption"]}'
    if b:
        x0, y0, x1, y1 = b
        im = page(r["page"]).crop((max(0, x0 - 60), max(0, y0 - 40), max(x1, x0 + 1250) + 60, y1 + 230))
        f = min(1.0, WD / im.width, 300 / im.height)
        im = im.resize((int(im.width * f), int(im.height * f)))
    else:
        im = Image.new("RGB", (WD, 60), "pink")
    # wrap the header
    words, lines, cur = head.split(), [], ""
    for w in words:
        if len(cur) + len(w) > 120:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    lines.append(cur)
    t = Image.new("RGB", (WD, 28 * len(lines) + im.height + 16), "white")
    d = ImageDraw.Draw(t)
    for k, ln in enumerate(lines):
        d.text((6, 4 + 28 * k), ln, fill=(160, 0, 0) if k == 0 else (0, 0, 0), font=FB if k == 0 else F)
    t.paste(im, (0, 28 * len(lines) + 8))
    tiles.append(t)

sheet, h, n = [], 0, 0
def flush():
    global sheet, h, n
    if not sheet:
        return
    S = Image.new("RGB", (WD, sum(t.height + 6 for t in sheet)), (200, 200, 200))
    y = 0
    for t in sheet:
        S.paste(t, (0, y)); y += t.height + 6
    S.save(W / "review" / f"cap{n:02d}.jpg", quality=88); n += 1; sheet, h = [], 0
for t in tiles:
    if h + t.height > 2400:
        flush()
    sheet.append(t); h += t.height + 6
flush()

# image thumbnails
TW, TH, C = 300, 330, 6
for k in range(0, len(R), 30):
    chunk = R[k:k + 30]
    S = Image.new("RGB", (TW * C, TH * ((len(chunk) + C - 1) // C)), "white")
    d = ImageDraw.Draw(S)
    for i, r in enumerate(chunk):
        im = Image.open(ROOT / r["file_rectified"]); im.thumbnail((TW - 10, TH - 40))
        x, y = (i % C) * TW, (i // C) * TH
        S.paste(im, (x + 5, y + 32)); d.text((x + 5, y + 4), f'{r["label"]} p{r["page"]}', fill=(160, 0, 0), font=FB)
    S.save(W / "review" / f"img{k // 30:02d}.jpg", quality=85)
print(n, "caption sheets")
