"""Merge two detection runs side by side, keeping for every side the line further OUT from the picture's centre
(_work/detect_v1.json: ungated edge snapping; _work/detect.json: paper/text-gated snapping). Cutting into a
photograph is worse than keeping a strip of paper, and each run fails in a different place (v1 is pulled onto
text lines beside pale photo edges; v2 is pulled into pale skies). Residual overshoot is trimmed by hand
(overrides.json "sides"). Writes _work/detect_merged.json and overlays in _work/viz/."""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from geometry import order

W = Path(__file__).resolve().parents[1] / "_work"


def line(p, q):
    a = np.array([p[0], p[1], 1.0]); b = np.array([q[0], q[1], 1.0])
    return np.cross(a, b)


def meet(l1, l2):
    x = np.cross(l1, l2)
    return x[:2] / x[2]


def merge_quad(qa, qb):
    qa, qb = order(qa), order(qb)
    c = (qa.mean(0) + qb.mean(0)) / 2
    sides, pick = [], []
    for s in range(4):
        cand = []
        for q, tag in ((qa, "v1"), (qb, "v2")):
            P, Q = q[s], q[(s + 1) % 4]
            d = (Q - P) / np.linalg.norm(Q - P)
            n = np.array([d[1], -d[0]])
            if np.dot((P + Q) / 2 - c, n) < 0:
                n = -n
            cand.append((float(np.dot((P + Q) / 2 - c, n)), P, Q, tag))
        best = max(cand, key=lambda t: t[0])
        sides.append(line(best[1], best[2])); pick.append(best[3])
    corners = [meet(sides[(s - 1) % 4], sides[s]) for s in range(4)]   # corner s joins side s-1 and side s
    return order(np.array(corners)), pick


def main():
    a = json.loads((W / "detect_v1.json").read_text())
    b = json.loads((W / "detect.json").read_text())
    out = {}
    for p in b:
        fa, fb = a.get(p, {"figs": []})["figs"], b[p]["figs"]
        figs = []
        for f in fb:
            # partner in v1: the figure whose box overlaps most
            def ov(g):
                x0, y0 = max(f["box"][0], g["box"][0]), max(f["box"][1], g["box"][1])
                x1, y1 = min(f["box"][2], g["box"][2]), min(f["box"][3], g["box"][3])
                return max(0, x1 - x0) * max(0, y1 - y0)
            g = max(fa, key=ov, default=None)
            m = dict(f)
            if g is not None and ov(g) > 0:
                q, pick = merge_quad(g["quad"], f["quad"])
                m["quad"] = q.round().astype(int).tolist()
                m["box"] = [int(q[:, 0].min()), int(q[:, 1].min()), int(q[:, 0].max()), int(q[:, 1].max())]
                m["sides_from"] = pick
            figs.append(m)
        out[p] = {"paper": b[p]["paper"], "figs": figs}
    sides = {k: v for k, v in json.loads((Path(__file__).parent / "overrides.json").read_text(encoding="utf-8"))
             .get("sides", {}).items() if not k.startswith("_")}
    for lab, sv in sides.items():
        figs = out[str(sv["page"])]["figs"]
        x, y = sv["inside"]
        f = next(g for g in figs if g["box"][0] <= x <= g["box"][2] and g["box"][1] <= y <= g["box"][3])
        q = order(f["quad"])
        ls = [line(q[s], q[(s + 1) % 4]) for s in range(4)]
        for s, name in enumerate(("top", "right", "bottom", "left")):
            if name in sv:
                ls[s] = line(*sv[name])
        q = order(np.array([meet(ls[(s - 1) % 4], ls[s]) for s in range(4)]))
        f["quad"] = q.round().astype(int).tolist()
        f["box"] = [int(q[:, 0].min()), int(q[:, 1].min()), int(q[:, 0].max()), int(q[:, 1].max())]
        f["sides_by_hand"] = [n for n in ("top", "right", "bottom", "left") if n in sv]
        if sv.get("note"):
            f["note"] = sv["note"]
    (W / "detect_merged.json").write_text(json.dumps(out, indent=0))
    print("merged", sum(len(v["figs"]) for v in out.values()), "regions")


if __name__ == "__main__":
    main()
