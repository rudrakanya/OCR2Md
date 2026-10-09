#!/usr/bin/env python3
"""Trim the strip of the facing page that the camera caught at the frame edge.

Many photographs include a band of the opposite page down one side. The two
pages are both bright, so they threshold into a single region and no amount of
morphology separates them — but the gutter between them is a dark valley running
the height of the frame, and that is what this finds.

The trim is deliberately timid. It only cuts within the outer OUTER_ZONE of the
width, only at a valley clearly darker than the page around it, and only when
the strip it removes is narrow. Anything else is left in place: keeping a bit of
the neighbouring page costs nothing, while shaving a column off the real page
would destroy content.
"""
import cv2
import numpy as np

OUTER_ZONE = 0.32       # only look for a gutter this far in from either edge
MIN_DEPTH = 0.62        # valley must be this much darker than the page median
MIN_STRIP = 0.02        # ignore slivers thinner than this (nothing to gain)


def find_gutter(pil_img):
    """Return (left, right) crop bounds in pixels, plus a note."""
    g = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2GRAY)
    h, w = g.shape
    band = g[int(h * 0.12):int(h * 0.88), :]           # skip top/bottom shadows
    col = cv2.GaussianBlur(band.mean(axis=0).astype(np.float32).reshape(1, -1), (31, 1), 0).ravel()
    page_level = float(np.median(col))
    zone = int(w * OUTER_ZONE)

    left, right, notes = 0, w, []
    dark = col < page_level * MIN_DEPTH
    # The cut belongs at the INNERMOST dark column, not the darkest one: the
    # darkest is usually the frame's own border, with the facing page sitting
    # between it and the gutter we actually want.
    inner = [i for i in range(zone) if dark[i]]
    if inner:
        i = max(inner)
        if i > w * MIN_STRIP:
            left = i
            notes.append(f"left gutter at {i/w:.0%}")
    inner = [j for j in range(w - zone, w) if dark[j]]
    if inner:
        j = min(inner)
        if (w - j) > w * MIN_STRIP:
            right = j
            notes.append(f"right gutter at {j/w:.0%}")

    if right - left < w * 0.5:            # would remove half the page: refuse
        return 0, w, "gutter rejected (would cut too much)"
    return left, right, "; ".join(notes) or "no gutter found"
