"""Pair picture boxes with captions.

Automatic rule, per page: a minimum-distance one-to-one assignment (edge-to-edge distance between the picture
box and the caption region), then any further boxes join their nearest caption as parts of a multi-part figure.
Boxes left on a page without captions are paired with the facing page's captions that found no picture (the book
often prints a full-page photograph opposite its caption). Pages in overrides.json "assign" are set by hand;
"drop" removes boxes (page furniture, slivers, page tint); "boxes" adds hand-placed boxes (rough rectangles in pt,
tightened to the ink inside).

  figures(det, caps, ovr) -> list of {label, page, boxes: [[x0,y0,x1,y1] native px], parts: [...], how}
"""
import numpy as np
from scipy.optimize import linear_sum_assignment


def edge_dist(a, b):
    dx = max(0, max(a[0], b[0]) - min(a[2], b[2]))
    dy = max(0, max(a[1], b[1]) - min(a[3], b[3]))
    return (dx * dx + dy * dy) ** 0.5


def facing(p):
    return p + 1 if p % 2 == 0 else p - 1


MIN_PT = 12   # boxes narrower or shorter than this (page-edge slivers) are dropped


def page_boxes(det, ovr, p, tightened):
    dp = det.get(str(p), {})
    boxes = [list(b) for b in dp.get("boxes", [])]
    drop = set(ovr.get("drop", {}).get(str(p), []))
    if drop == {"all"}:
        boxes = []
    else:
        z = dp.get("zoom", 5.0)
        boxes = [b for i, b in enumerate(boxes) if i not in drop
                 and (b[2] - b[0]) / z >= MIN_PT and (b[3] - b[1]) / z >= MIN_PT]
    boxes += tightened.get(p, [])
    return boxes


def figures(det, caps, ovr, tightened):
    """tightened: {page: [boxes from overrides 'boxes', already tightened]} appended after detected ones."""
    out = []
    pages = sorted({int(k) for k in det} | set(tightened))
    leftover_boxes, leftover_caps = {}, {}
    for p in pages:
        boxes = page_boxes(det, ovr, p, tightened)
        pcaps = [c for c in caps if c["page"] == p and c.get("label") and c["kind"] in ("figure", "map")]
        man = ovr.get("assign", {}).get(str(p))
        sx = ovr.get("split_x", {}).get(str(p))
        if sx is not None:
            z = det[str(p)]["zoom"]
            cut = sx["x_pt"] * z
            left = [i for i, b in enumerate(boxes) if (b[0] + b[2]) / 2 < cut]
            right = [i for i, b in enumerate(boxes) if (b[0] + b[2]) / 2 >= cut]
            man = [{"label": sx["left"], "boxes": left}, {"label": sx["right"], "boxes": right}]
        if man is not None:
            used = set()
            for m in man:
                idx = m["boxes"]
                used |= set(idx)
                out.append({"label": m["label"], "page": p, "boxes": [boxes[i] for i in idx],
                            "box_ids": idx, "sub": m.get("sub"), "note": m.get("note"),
                            "how": "split at x" if sx is not None else "hand-assigned"})
            rest = [i for i in range(len(boxes)) if i not in used]
            if rest:
                leftover_boxes[p] = rest
            got = {m["label"] for m in man}
            lc = [c for c in pcaps if c["label"] not in got and c["label"] not in ovr.get("caption_elsewhere", {})]
            if lc:
                leftover_caps[p] = lc
            continue
        if not boxes:
            if pcaps:
                leftover_caps[p] = pcaps
            continue
        if not pcaps:
            leftover_boxes[p] = list(range(len(boxes)))
            continue
        C = np.array([[edge_dist(b, c["bbox_px"]) for c in pcaps] for b in boxes])
        r, k = linear_sum_assignment(C)
        groups = {j: [i] for i, j in zip(r, k)}
        for i in range(len(boxes)):
            if i not in r:
                groups[int(np.argmin(C[i]))].append(i)
        for j, idx in groups.items():
            out.append({"label": pcaps[j]["label"], "page": p, "boxes": [boxes[i] for i in sorted(idx)],
                        "box_ids": sorted(idx), "sub": None, "how": "auto (nearest caption)"})
        lc = [c for j, c in enumerate(pcaps) if j not in groups]
        if lc:
            leftover_caps[p] = lc
    for lab, p in ovr.get("caption_elsewhere", {}).items():
        if p in leftover_boxes:
            idx = leftover_boxes.pop(p)
            boxes = page_boxes(det, ovr, p, tightened)
            out.append({"label": lab, "page": p, "boxes": [boxes[i] for i in idx], "box_ids": idx, "sub": None,
                        "how": "hand-assigned (caption on another page)"})
            for q in list(leftover_caps):
                leftover_caps[q] = [c for c in leftover_caps[q] if c["label"] != lab]
                if not leftover_caps[q]:
                    del leftover_caps[q]
    for p, idx in sorted(leftover_boxes.items()):
        q = facing(p)
        boxes = page_boxes(det, ovr, p, tightened)
        if q in leftover_caps and len(leftover_caps[q]) == 1:
            c = leftover_caps.pop(q)[0]
            out.append({"label": c["label"], "page": p, "boxes": [boxes[i] for i in idx], "box_ids": idx,
                        "sub": None, "how": f"auto (caption on facing page {q})"})
        else:
            for i in idx:
                out.append({"label": None, "page": p, "boxes": [boxes[i]], "box_ids": [i], "sub": None,
                            "how": "UNMATCHED"})
    done = {f["label"] for f in out}
    for q, lc in leftover_caps.items():
        for c in lc:
            if c["label"] in done:
                continue
            out.append({"label": c["label"], "page": None, "caption_page": q, "boxes": [], "box_ids": [],
                        "sub": None, "how": "CAPTION WITHOUT PICTURE"})
    return out
