"""Quad geometry for printed photos on a page photograph (free, local).

  rect_from_component(cnt)            rotated bounding rectangle (tl, tr, br, bl), so a pale sky that the
                                      darkness mask misses does not cut a corner off the quad
  split_gutters(gray, quad, tone)     split a quad at a white gutter (two plates printed side by side)
  refine(gray, quad)                  snap each side to the printed photo's edge: both endpoints of a side move
                                      independently along the side's normal (perspective makes trapezoids) and
                                      the line with the strongest paper-outside / picture-inside contrast wins
All coordinates are in the pixel space of the gray image passed in.
"""
import cv2
import numpy as np


def order(q):
    q = np.asarray(q, float)
    s = q.sum(1); d = q[:, 1] - q[:, 0]
    return np.array([q[np.argmin(s)], q[np.argmin(d)], q[np.argmax(s)], q[np.argmax(d)]])


def rect_from_component(cnt, max_tilt=4.0):
    """Rotated bounding rectangle when the tilt is small; otherwise the upright bounding box (a cut-out image
    or a pale sky makes the dark blob lean, and printed photos are set square to the page)."""
    (cx, cy), (w, h), ang = cv2.minAreaRect(cnt)
    tilt = min(abs(ang) % 90, 90 - abs(ang) % 90)
    if tilt <= max_tilt:
        return order(cv2.boxPoints(((cx, cy), (w, h), ang)))
    x, y, w, h = cv2.boundingRect(cnt)
    return np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], float)


def warp(gray, quad, w, h):
    M = cv2.getPerspectiveTransform(np.float32(quad), np.float32([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]]))
    return cv2.warpPerspective(gray, M, (w, h), flags=cv2.INTER_AREA), M


def _lerp(a, b, t):
    return a + (b - a) * t


def split_gutters(gray, quad, paper_level, min_gap=4, frac=0.95, max_gap=0.07):
    """Return a list of quads: the input, or its parts if a clean white gutter runs through it.
    paper_level: gray value above which a pixel reads as paper. Gutters are searched in the middle 15-85%."""
    q = order(quad)
    w = int(max(np.linalg.norm(q[1] - q[0]), np.linalg.norm(q[2] - q[3])))
    h = int(max(np.linalg.norm(q[3] - q[0]), np.linalg.norm(q[2] - q[1])))
    if w < 20 or h < 20:
        return [q]
    flat, _ = warp(gray, q, w, h)
    paper = flat >= paper_level
    for axis in (0, 1):   # 0: vertical gutter (columns), 1: horizontal gutter (rows)
        prof = paper.mean(axis=axis)
        n = len(prof)
        good = prof >= frac
        best = None
        i = int(n * 0.15)
        while i < int(n * 0.85):
            if good[i]:
                j = i
                while j < n and good[j]:
                    j += 1
                # a gutter is narrow paper with a picture edge on both sides (a bright sky fades instead)
                side = lambda k0, k1: prof[max(0, k0):max(0, k1)].mean() if k1 > k0 else 1.0
                sharp = side(i - 4, i - 1) < 0.5 and side(j + 1, j + 4) < 0.5
                if min_gap <= j - i <= max_gap * n and sharp and (best is None or j - i > best[1] - best[0]):
                    best = (i, j)
                i = j
            i += 1
        if best:
            a, b = best[0] / n, best[1] / n
            tl, tr, br, bl = q
            if axis == 0:
                left = [tl, _lerp(tl, tr, a), _lerp(bl, br, a), bl]
                right = [_lerp(tl, tr, b), tr, br, _lerp(bl, br, b)]
                parts = [left, right]
            else:
                top = [tl, tr, _lerp(tr, br, a), _lerp(tl, bl, a)]
                bot = [_lerp(tl, bl, b), _lerp(tr, br, b), br, bl]
                parts = [top, bot]
            out = []
            for p in parts:
                out += split_gutters(gray, np.array(p), paper_level, min_gap, frac)
            return out
    return [q]


def _bilinear(img, pts):
    return cv2.remap(img, pts[..., 0].astype(np.float32), pts[..., 1].astype(np.float32), cv2.INTER_LINEAR,
                     borderMode=cv2.BORDER_REPLICATE)


def refine(gray, quad, R=24, off=2.0, iters=3, fixed=(), r_in=None, r_out=None, paper=200,
           out_min=0.92, in_max=0.72):
    """Snap each side to the printed photo's edge. Both endpoints of a side move independently along the side's
    outward normal (r_in px inward, r_out px outward; default +-R). A candidate line counts only if the band just
    outside it (3-14 px) is clean paper (>= out_min of samples brighter than `paper`) and the band just inside is
    not paper or text (<= in_max), so a text line or caption next to a pale photo edge cannot capture the side;
    among valid lines the strongest outside-minus-inside contrast wins. If no line is valid the side stays.
    One wide pass, then (iters - 1) polishing passes at +-4 px. Returns (quad, per-side scores; None = kept)."""
    g = cv2.GaussianBlur(gray, (3, 3), 0).astype(np.float32)
    q = order(quad).astype(float)
    scores = [None] * 4
    ts = np.linspace(0.08, 0.92, 80)
    band = np.arange(3, 15, 2, dtype=float)
    for it in range(iters):
        ri, ro = ((r_in if r_in is not None else R), (r_out if r_out is not None else R)) if it == 0 else (4, 4)
        c = q.mean(0)
        for s in range(4):
            if s in fixed:
                continue
            P, Q = q[s].copy(), q[(s + 1) % 4].copy()
            d = (Q - P) / max(1e-6, np.linalg.norm(Q - P))
            n = np.array([d[1], -d[0]])
            if np.dot(_lerp(P, Q, 0.5) - c, n) < 0:
                n = -n
            ab = np.arange(-ri, ro + 1, dtype=float)
            A, B = np.meshgrid(ab, ab, indexing="ij")
            P2 = P[None, None, :] + A[..., None] * n
            Q2 = Q[None, None, :] + B[..., None] * n
            pts = (P2[..., None, :] + (Q2 - P2)[..., None, :] * ts[None, None, :, None]).reshape(-1, len(ts), 2)
            out = _bilinear(g, pts + off * n)
            inn = _bilinear(g, pts - off * n)
            con = np.median(out - inn, axis=1)
            po = np.mean([(_bilinear(g, pts + b * n) > paper).mean(1) for b in band], axis=0)
            pi = np.mean([(_bilinear(g, pts - b * n) > paper).mean(1) for b in band], axis=0)
            con = np.where((po >= out_min) & (pi <= in_max), con, -np.inf)
            k = int(np.argmax(con))
            if not np.isfinite(con[k]):
                continue
            ka, kb = np.unravel_index(k, A.shape)
            scores[s] = round(float(con[k]), 1)
            q[s], q[(s + 1) % 4] = P + A[ka, kb] * n, Q + B[ka, kb] * n
    return q, scores
