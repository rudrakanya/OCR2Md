"""Detect printed photographs/plans on a page photograph (free, local).

The pages are handheld phone photos of the open book (3468 x 4624 px upright), so a page is a lit, slightly
tilted and curled sheet with desk, fingers and the facing page around it. Work at 1/8 scale:
1. Paper: the brightest large region; its local tone is estimated with a wide max-filter so the light falloff
   across the photo does not matter.
2. Picture pixels: well below the local paper tone after a blur that turns lines of text into a pale grey
   (a page of text stays light; a halftone photograph does not), or clearly saturated (colour plates).
3. Components inside the paper that are larger than a text block get a quadrilateral (the printed photo is a
   rectangle seen in perspective); the quad is mapped back to native pixels.

  detect(rgb_native) -> {"paper": quad, "figs": [{"quad": [[x,y]*4], "box": [x0,y0,x1,y1], "area_frac": f}]}
"""
import cv2
import numpy as np

from geometry import rect_from_component, refine, split_gutters

S = 8
Q = 4           # refinement scale (1/4 native)
PAPER = 230     # normalised paper level


def _quad(cnt):  # paper outline only
    hull = cv2.convexHull(cnt)
    peri = cv2.arcLength(hull, True)
    for eps in (0.01, 0.02, 0.03, 0.05, 0.08):
        ap = cv2.approxPolyDP(hull, eps * peri, True)
        if len(ap) == 4:
            return ap.reshape(4, 2).astype(float)
    r = cv2.minAreaRect(cnt)
    return cv2.boxPoints(r).astype(float)


def order(q):
    q = np.asarray(q, float)
    s = q.sum(1); d = q[:, 1] - q[:, 0]
    return np.array([q[np.argmin(s)], q[np.argmin(d)], q[np.argmax(s)], q[np.argmax(d)]])  # tl tr br bl


def paper_mask(g):
    """Largest bright connected region = the photographed page."""
    t = max(110, int(np.percentile(g, 60)) - 35)
    m = (g > t).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n < 2:
        return np.ones_like(m)
    k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
    pm = (lab == k).astype(np.uint8)
    # fill the holes (pictures, text) inside the page
    cnts, _ = cv2.findContours(pm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    full = np.zeros_like(pm)
    cv2.drawContours(full, [max(cnts, key=cv2.contourArea)], -1, 1, -1)
    return full


def snap(rgb, quad, fixed=(), do_refine=True):
    """Snap a hand-set quad (native px) to the photo edges, as detect() does for its own quads."""
    small = cv2.resize(rgb, (rgb.shape[1] // S, rgb.shape[0] // S), interpolation=cv2.INTER_AREA)
    g = cv2.cvtColor(small, cv2.COLOR_RGB2GRAY)
    pm = paper_mask(g)
    tone = cv2.GaussianBlur(cv2.dilate(np.where(pm > 0, g, 0).astype(np.uint8), np.ones((41, 41), np.uint8)),
                            (31, 31), 0)
    qrgb = cv2.resize(rgb, (rgb.shape[1] // Q, rgb.shape[0] // Q), interpolation=cv2.INTER_AREA)
    qg = cv2.cvtColor(qrgb, cv2.COLOR_RGB2GRAY).astype(np.float32)
    qtone = cv2.resize(tone.astype(np.float32), (qg.shape[1], qg.shape[0]), interpolation=cv2.INTER_LINEAR)
    qn = np.clip(qg * PAPER / np.maximum(qtone, 40), 0, 255).astype(np.uint8)
    q = np.asarray(quad, float) / Q
    sc = [None] * 4
    if do_refine:
        q, sc = refine(qn, q, fixed=fixed)
    qq = q * Q
    return {"quad": qq.round().astype(int).tolist(),
            "box": [int(qq[:, 0].min()), int(qq[:, 1].min()), int(qq[:, 0].max()), int(qq[:, 1].max())],
            "edge_scores": sc}


def detect(rgb, dark=38, sat=60, min_frac=0.012):
    small = cv2.resize(rgb, (rgb.shape[1] // S, rgb.shape[0] // S), interpolation=cv2.INTER_AREA)
    g = cv2.cvtColor(small, cv2.COLOR_RGB2GRAY).astype(np.int16)
    hsv = cv2.cvtColor(small, cv2.COLOR_RGB2HSV)
    pm = paper_mask(g.astype(np.uint8))
    paper_px = np.where(pm > 0, g, 0).astype(np.uint8)
    tone = cv2.dilate(paper_px, np.ones((41, 41), np.uint8))            # local paper brightness
    tone = cv2.GaussianBlur(tone, (31, 31), 0).astype(np.int16)
    gb = cv2.blur(g, (7, 7))
    pic = ((tone - gb) > dark) | ((hsv[..., 1] > sat) & (cv2.blur(hsv[..., 1], (5, 5)) > sat))
    inner = cv2.erode(pm, np.ones((9, 9), np.uint8))
    pic = (pic & (inner > 0)).astype(np.uint8)
    pic = cv2.morphologyEx(pic, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    pic = cv2.morphologyEx(pic, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    area = pm.sum()
    # quarter-scale, lighting-normalised gray for gutters and edge snapping
    qrgb = cv2.resize(rgb, (rgb.shape[1] // Q, rgb.shape[0] // Q), interpolation=cv2.INTER_AREA)
    qg = cv2.cvtColor(qrgb, cv2.COLOR_RGB2GRAY).astype(np.float32)
    qtone = cv2.resize(tone.astype(np.float32), (qg.shape[1], qg.shape[0]), interpolation=cv2.INTER_LINEAR)
    qn = np.clip(qg * PAPER / np.maximum(qtone, 40), 0, 255).astype(np.uint8)
    figs = []
    cnts, _ = cv2.findContours(pic, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in cnts:
        a = cv2.contourArea(c)
        if a < min_frac * area:
            continue
        x, y, w, h = cv2.boundingRect(c)
        if min(w, h) < 18:
            continue
        r0 = rect_from_component(c) * (S / Q)
        for part in split_gutters(qn, r0, PAPER - 22):
            pw = np.linalg.norm(part[1] - part[0]); ph = np.linalg.norm(part[3] - part[0])
            if min(pw, ph) < 30:
                continue
            rq, sc = refine(qn, part, r_in=50, r_out=10)
            qq = rq * Q
            xs, ys = qq[:, 0], qq[:, 1]
            figs.append({"quad": qq.round().astype(int).tolist(),
                         "box": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
                         "area_frac": round(float(cv2.contourArea(np.float32(rq)) * (Q / S) ** 2 / area), 4),
                         "edge_scores": sc})
    figs.sort(key=lambda f: (f["box"][1] // 600, f["box"][0]))
    pc, _ = cv2.findContours(pm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    paper = order(_quad(max(pc, key=cv2.contourArea))) * S
    return {"paper": paper.round().astype(int).tolist(), "figs": figs}
