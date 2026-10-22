"""Detect picture regions (photographs, drawings, plans, maps) on a colour page scan (free, local).

Works on a quarter-scale copy of the native render (~90 dpi), then maps boxes back to native pixels.
1. Foreground: pixels that differ from the page's paper tone (darker ink or tone, brighter photo highlights,
   or saturated colour).
2. Text removal: every text-layer line that reads as words and is set at text size is blanked, so running text,
   captions and headings drop out; OCR noise read off pictures stays (it is not word-like).
3. Components of the closed foreground that are larger than a few text lines are picture candidates; nearby
   candidates are merged (a drawing's separate parts), and small specks are discarded.

  detect(page) -> {"zoom", "size", "boxes": [[x0, y0, x1, y1] native px], "small": [...]}
"""
import cv2
import numpy as np

from common import is_texty, lines, native_zoom, render

S = 0.25
MERGE = 10        # px at quarter scale (~0.11 in) between parts of one picture
MIN_SIDE = 28     # px at quarter scale (~0.3 in)
MIN_FILL = 600    # foreground px at quarter scale
ATTACH = 26       # px at quarter scale (~0.29 in): detached part of a drawing


def paper_tone(g):
    h = np.bincount(g.ravel(), minlength=256)
    return int(np.argmax(h[120:])) + 120


def foreground(rgb, sensitive=False):
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    bg = paper_tone(g)
    if sensitive:   # pale line drawings (ch. 12): smooth the paper grain, then take faint ink too
        gb = cv2.GaussianBlur(g, (3, 3), 0)
        fg = (gb < bg - 13) | (g > min(bg + 14, 250)) | (hsv[..., 1] > 70)
    else:
        fg = (g < bg - 28) | (g > min(bg + 14, 250)) | (hsv[..., 1] > 70)
    return fg.astype(np.uint8), bg


def _prepare(page, masks, sensitive):
    z = native_zoom(page)
    zs = z * S
    rgb = render(page, zs)
    fg, bg = foreground(rgb, sensitive)
    text_lines = []
    for x0, y0, x1, y1, s, sz in lines(page):
        if (y1 - y0) <= 11.5 and sz <= 10 and is_texty(s):
            a0, b0, a1, b1 = int(x0 * zs) - 1, int(y0 * zs) - 1, int(x1 * zs) + 2, int(y1 * zs) + 2
            fg[max(0, b0):b1, max(0, a0):a1] = 0
            if (y1 - y0) <= 8.6:
                text_lines.append([a0, b0, a1, b1])
    for m in masks or []:
        a0, b0, a1, b1 = [int(v * S) for v in m]
        fg[max(0, b0 - 2):b1 + 2, max(0, a0 - 2):a1 + 2] = 0
    e = 6   # thin page-edge band (scanner shadow, page curl)
    fg[:e, :] = 0; fg[-e:, :] = 0; fg[:, :e] = 0; fg[:, -e:] = 0
    return z, bg, fg, text_lines


def _hits(a, b, pad=0):
    return a[0] - pad < b[2] and b[0] - pad < a[2] and a[1] - pad < b[3] and b[1] - pad < a[3]


def detect(page, masks=None, sensitive=False):
    """masks: native-px rects (caption regions) blanked before detection."""
    z, bg, fg, small_text = _prepare(page, masks, sensitive)
    k = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    cl = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, k)
    n, lab, st, _ = cv2.connectedComponentsWithStats(cl, 8)
    cands, specks = [], []
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if (w >= MIN_SIDE and h >= MIN_SIDE and a >= MIN_FILL) or (max(w, h) >= 90 and a >= 300):
            cands.append([x, y, x + w, y + h])
        elif max(w, h) >= 4 and a >= 8:
            specks.append([x, y, x + w, y + h])
    boxes = merge(cands, MERGE)
    boxes = [b for b in boxes if (b[2] - b[0]) >= MIN_SIDE and (b[3] - b[1]) >= MIN_SIDE]
    mk = [[v * S for v in m] for m in masks or []]
    # detached parts of a drawing (finials, small elements): specks lying just above/below a box within its
    # width, or beside it within its height, are absorbed, unless that would reach into a caption region
    for _ in range(3):
        grown = False
        for b in boxes:
            for sp in specks:
                if _hits(sp, b):
                    continue
                xo = sp[0] < b[2] and b[0] < sp[2]
                yo = sp[1] < b[3] and b[1] < sp[3]
                gap_v = max(b[1] - sp[3], sp[1] - b[3])
                gap_h = max(b[0] - sp[2], sp[0] - b[2])
                if (xo and gap_v <= ATTACH) or (yo and gap_h <= ATTACH):
                    u = [min(b[0], sp[0]), min(b[1], sp[1]), max(b[2], sp[2]), max(b[3], sp[3])]
                    if not any(_hits(u, m) for m in mk) and not any(_hits(u, o) for o in boxes if o is not b):
                        b[:] = u
                        grown = True
        if not grown:
            break
    # labels printed on a drawing (shikhara, griva ...) are word-like and were blanked: take back small-set
    # text lines that touch a box, unless they belong to a caption
    for b in boxes:
        for t in small_text:
            if _hits(t, b, 3) and not any(_hits(t, m) for m in mk):
                b[:] = [min(b[0], t[0]), min(b[1], t[1]), max(b[2], t[2]), max(b[3], t[3])]
    boxes = merge(boxes, 0)
    nat = [[int(round(v / S)) for v in b] for b in boxes]
    return {"zoom": z, "paper": bg, "boxes": nat}


def tighten(page, rough_px, masks=None, sensitive=False):
    """Tight box of the picture ink inside a hand-given rough rectangle (native px)."""
    z, bg, fg, _ = _prepare(page, masks, sensitive)
    a0, b0, a1, b1 = [int(v * S) for v in rough_px]
    sub = cv2.morphologyEx(fg[b0:b1, a0:a1], cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    ys, xs = np.nonzero(sub)
    if not len(xs):
        return None
    return [int(round((a0 + xs.min()) / S)), int(round((b0 + ys.min()) / S)),
            int(round((a0 + xs.max() + 1) / S)), int(round((b0 + ys.max() + 1) / S))]


def merge(boxes, gap):
    boxes = [list(b) for b in boxes]
    changed = True
    while changed:
        changed = False
        out = []
        while boxes:
            b = boxes.pop()
            i = 0
            while i < len(boxes):
                c = boxes[i]
                if b[0] - gap <= c[2] and c[0] - gap <= b[2] and b[1] - gap <= c[3] and c[1] - gap <= b[3]:
                    b = [min(b[0], c[0]), min(b[1], c[1]), max(b[2], c[2]), max(b[3], c[3])]
                    boxes.pop(i)
                    changed = True
                else:
                    i += 1
            out.append(b)
        boxes = out
    return sorted(boxes, key=lambda b: (b[1], b[0]))


def colour_box(page):
    """Part-opener pages: a photograph on a full-page colour tint (with a lighting gradient, so colour
    distance alone fails). The tint is smooth and the photograph is textured: the box is the largest region of
    high local detail (gradient magnitude, smoothed), excluding small text."""
    z = native_zoom(page)
    rgb = render(page, z * S)
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1)
    mag = cv2.blur(np.hypot(gx, gy), (15, 15))
    m = (mag > 12).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    i = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    x, y, w, h, _ = st[i]
    # the blur spreads the region by about half the kernel; take it back
    k = 7
    return [int(round(v / S)) for v in (x + k, y + k, x + w - k, y + h - k)]
