#!/usr/bin/env python3
"""Turn a photograph of a page into a rectified page image.

The photographs show a page lying on a desk: dark background around it, often a
strip of the facing page at one edge, and the page itself slightly skewed and
keystoned. This module finds the page, straightens it, and trims the background,
falling back progressively rather than ever guessing aggressively:

    1. a convincing four-cornered page  -> perspective-warp it flat
    2. a convincing bright region       -> axis-aligned crop with a small margin
    3. neither                          -> keep the whole frame, and say so

Every outcome is reported so the manifest records which pages were rectified,
which were merely cropped, and which were left alone for a human to look at.
"""
import cv2
import numpy as np
from PIL import Image

MIN_PAGE_AREA = 0.30      # a real page fills at least this much of the frame
MAX_PAGE_AREA = 0.995     # ~the whole frame means nothing was actually found
DETECT_WIDTH = 1000       # detection runs small; the warp is applied full size
MARGIN = 0.004            # keep a hair of background so nothing is shaved off


def _order_corners(pts):  # retained: useful if perspective is ever revisited
    """Corners as top-left, top-right, bottom-right, bottom-left."""
    s, d = pts.sum(1), np.diff(pts, axis=1).ravel()
    return np.array([pts[np.argmin(s)],    # top-left     has the smallest x+y
                     pts[np.argmin(d)],    # top-right    has the smallest y-x
                     pts[np.argmax(s)],    # bottom-right has the largest x+y
                     pts[np.argmax(d)]],   # bottom-left  has the largest y-x
                    dtype=np.float32)


def _page_mask(gray):
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    th = cv2.morphologyEx(th, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    return cv2.morphologyEx(th, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))


def rectify(pil_img):
    """Return (image, method, note). Never raises on odd input."""
    full = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    H, W = full.shape[:2]
    scale = DETECT_WIDTH / max(W, 1)
    small = cv2.resize(full, (DETECT_WIDTH, max(1, int(H * scale))))
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    mask = _page_mask(gray)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return pil_img, "full-frame", "no page region found"

    c = max(contours, key=cv2.contourArea)
    frac = cv2.contourArea(c) / float(small.shape[0] * small.shape[1])
    if not (MIN_PAGE_AREA <= frac <= MAX_PAGE_AREA):
        return pil_img, "full-frame", f"page region {frac:.0%} of frame"

    # Perspective correction is deliberately NOT attempted. A homography built
    # from an approximate page quad keeps straight lines straight but changes
    # how parallel lines relate, and on a test page it left the body paragraph
    # and the signature block visibly out of parallel — distortion introduced by
    # the "correction" itself. Cropping and rotating only ever resample the
    # original geometry, so that is what an archival copy gets.
    inv = 1.0 / scale
    x, y, w, h = cv2.boundingRect(c)
    mx, my = int(w * MARGIN * inv), int(h * MARGIN * inv)
    x0 = max(0, int(x * inv) - mx); y0 = max(0, int(y * inv) - my)
    x1 = min(W, int((x + w) * inv) + mx); y1 = min(H, int((y + h) * inv) + my)
    if (x1 - x0) < 50 or (y1 - y0) < 50:
        return pil_img, "full-frame", "crop degenerate"
    return pil_img.crop((x0, y0, x1, y1)), "crop", f"page {frac:.0%} of frame"


MAX_DESKEW = 8.0          # a page photo is never more than a few degrees off


def deskew(pil_img):
    """Rotate so the printed lines run horizontally. Returns (image, degrees).

    Rectifying the page straightens its edges, but the text can still sit a
    couple of degrees off — enough to hurt OCR and to look wrong in a PDF. The
    angle is measured from the text itself: smear each line into a blob, take
    the orientation of every blob wide enough to be a line of type, and use the
    median. Anything beyond MAX_DESKEW is treated as a measurement failure and
    ignored rather than applied.
    """
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2GRAY)
    h, w = img.shape
    scale = 1200.0 / max(w, 1)
    small = cv2.resize(img, (1200, max(1, int(h * scale)))) if scale < 1 else img
    th = cv2.adaptiveThreshold(small, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 31, 15)
    smear = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_RECT, (25, 3)), iterations=2)
    contours, _ = cv2.findContours(smear, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    angles = []
    for c in contours:
        (_, _), (bw, bh), _ = cv2.minAreaRect(c)
        long_side, short_side = max(bw, bh), min(bw, bh)
        if long_side < 80 or short_side < 3 or long_side / max(short_side, 1) < 4:
            continue                           # not the shape of a line of type
        # Take the direction from a fitted line rather than the rect's own angle:
        # minAreaRect's angle convention has changed between OpenCV releases, and
        # a fitted direction means the same thing in every version.
        vx, vy, _, _ = cv2.fitLine(c, cv2.DIST_L2, 0, 0.01, 0.01).ravel()
        if abs(vx) < 1e-6:
            continue                           # vertical: a rule or a margin, not text
        ang = np.degrees(np.arctan2(vy, vx))
        if ang > 45:
            ang -= 90
        elif ang < -45:
            ang += 90
        if abs(ang) <= MAX_DESKEW:
            angles.append(float(ang))

    if len(angles) < 5:
        return pil_img, 0.0
    angle = float(np.median(angles))
    if abs(angle) < 0.15:                      # already straight; don't resample
        return pil_img, 0.0
    return pil_img.rotate(angle, resample=Image.BICUBIC, expand=True,
                          fillcolor=(255, 255, 255)), angle
