"""Detect image regions (estampages, photographs, drawings) on a page scan (free, local).

The scans are bilevel. Inked rubbings and photographs are dense fields of black; printed text is sparse lines.
1. Core: the page is reduced to a density map (fraction of black per 16 x 16 px cell); cells above DENS are
   marked, closed, and connected components larger than MIN_FRAC of the page are kept as cores.
2. Growth: each core's box is grown outward, side by side, across every row (or column) that carries ink,
   and stops at the first clear white gap of GAP px. Captions, scale notes and margin line numbers are set
   off from the image by such a gap, so they stay outside; the light lines of a drawing continue row after
   row, so a drawing is kept whole. The box is never shrunk into the image.
3. Overlapping boxes are merged; PAD px of margin is kept.

  detect(page_png) -> list of dicts {bbox: [x0, y0, x1, y1] (native px), area_frac, density}
"""
import cv2
import numpy as np

CELL = 16
DENS = 0.18        # a cell counts as "image core" when > 18 % of its pixels are black
CLOSE = 5          # closing kernel, in cells (80 px)
MIN_FRAC = 0.012   # a core must cover at least 1.2 % of the page
GAP = 22           # px of clear white that ends an image (captions sit further off than this)
INK = 0.0025       # a row/column is "inked" if more than 0.25 % of its span is black (ignores dust)
PAD = 8


def density_map(g):
    h, w = g.shape
    hh, ww = h // CELL, w // CELL
    b = (g[: hh * CELL, : ww * CELL] < 128).astype(np.float32)
    return b.reshape(hh, CELL, ww, CELL).mean(axis=(1, 3))


def _grow(B, box, h, w):
    x0, y0, x1, y1 = box
    for _ in range(12):
        changed = False
        # down
        rows = B[y1:min(h, y1 + 3000), x0:x1].mean(axis=1) > INK
        n = _extent(rows)
        if n:
            y1 += n; changed = True
        # up
        rows = B[max(0, y0 - 3000):y0, x0:x1].mean(axis=1)[::-1] > INK
        n = _extent(rows)
        if n:
            y0 -= n; changed = True
        # right
        cols = B[y0:y1, x1:min(w, x1 + 3000)].mean(axis=0) > INK
        n = _extent(cols)
        if n:
            x1 += n; changed = True
        # left
        cols = B[y0:y1, max(0, x0 - 3000):x0].mean(axis=0)[::-1] > INK
        n = _extent(cols)
        if n:
            x0 -= n; changed = True
        if not changed:
            break
    return [x0, y0, x1, y1]


def _extent(flags):
    """Number of leading positions to absorb: up to the last inked one before a run of GAP blanks."""
    last, blank = 0, 0
    for i, f in enumerate(flags):
        if f:
            last, blank = i + 1, 0
        else:
            blank += 1
            if blank >= GAP:
                break
    return last


SPLIT = 10        # px of white that separates bands inside a grown box
TEXT_H = 130      # an edge band thinner than this ...
TEXT_D = 0.20     # ... and sparser than this is text (caption, scale note, line numbers), not image


def _bands(flags):
    """Runs of inked positions separated by >= SPLIT blank positions: list of (start, end)."""
    out, start, blank = [], None, 0
    for i, f in enumerate(flags):
        if f:
            if start is None:
                start = i
            blank, end = 0, i + 1
        elif start is not None:
            blank += 1
            if blank >= SPLIT:
                out.append((start, end)); start = None
    if start is not None:
        out.append((start, end))
    return out


def _trim(B, box):
    """Drop thin, sparse bands at the box's edges (captions, scale lines, margin numbers); never cut into a
    dense or tall band."""
    x0, y0, x1, y1 = box
    for _ in range(6):
        sub = B[y0:y1, x0:x1]
        rb = _bands(sub.mean(axis=1) > INK)
        cb = _bands(sub.mean(axis=0) > INK)
        changed = False
        def textlike(a, b, axis):
            band = sub[a:b, :] if axis == 0 else sub[:, a:b]
            return (b - a) < TEXT_H and band.mean() < TEXT_D
        if len(rb) > 1 and textlike(*rb[0], 0):
            y0 += rb[1][0]; changed = True
        elif len(rb) > 1 and textlike(*rb[-1], 0):
            y1 = y0 + rb[-2][1]; changed = True
        elif len(cb) > 1 and textlike(*cb[0], 1):
            x0 += cb[1][0]; changed = True
        elif len(cb) > 1 and textlike(*cb[-1], 1):
            x1 = x0 + cb[-2][1]; changed = True
        elif rb:
            y0, y1 = y0 + rb[0][0], y0 + rb[-1][1]
        if not changed:
            break
    return [x0, y0, x1, y1]


def _merge(boxes):
    boxes = [list(b) for b in boxes]
    merged = True
    while merged:
        merged = False
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
                    boxes[i] = [min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])]
                    del boxes[j]
                    merged = True
                    break
            if merged:
                break
    return boxes


def detect(path):
    g = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    h, w = g.shape
    B = (g < 128)
    d = density_map(g)
    m = (d > DENS).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (CLOSE, CLOSE)))
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(m, 8)
    cores = []
    for i in range(1, n):
        x, y, cw, ch, area = stats[i]
        if area * CELL * CELL / (h * w) < MIN_FRAC or cw < 6 or ch < 6:
            continue
        cores.append([x * CELL, y * CELL, min(w, (x + cw) * CELL), min(h, (y + ch) * CELL)])
    boxes = _merge([_trim(B, _grow(B, c, h, w)) for c in cores])
    out = []
    for x0, y0, x1, y1 in boxes:
        if min(x1 - x0, y1 - y0) < 150 and B[y0:y1, x0:x1].mean() < 0.2:
            continue   # a single bold caption line, not an image
        x0, y0, x1, y1 = max(0, x0 - PAD), max(0, y0 - PAD), min(w, x1 + PAD), min(h, y1 + PAD)
        out.append({"bbox": [int(x0), int(y0), int(x1), int(y1)],
                    "area_frac": round((x1 - x0) * (y1 - y0) / (h * w), 4),
                    "density": round(float(B[y0:y1, x0:x1].mean()), 3)})
    out.sort(key=lambda r: (r["bbox"][1] // 200, r["bbox"][0]))
    return out
