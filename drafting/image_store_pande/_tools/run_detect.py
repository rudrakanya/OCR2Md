"""Run detect.py over the pages, write _work/detect.json and overlay thumbnails in _work/viz/."""
import json, sys
from pathlib import Path
import cv2
import numpy as np
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
from detect import detect, snap
OVR = json.loads((Path(__file__).parent / "overrides.json").read_text(encoding="utf-8"))

ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "_work"


def main(pages):
    out = W / "detect.json"
    res = json.loads(out.read_text()) if out.exists() else {}
    (W / "viz").mkdir(exist_ok=True)
    for n in pages:
        rgb = np.asarray(Image.open(W / "pages" / f"p{n:03d}.png").convert("RGB"))
        r = detect(rgb)
        o = OVR.get(str(n), {})
        for f in r["figs"]:
            f["source"] = "auto"
        r["figs"] = [f for i, f in enumerate(r["figs"]) if i not in o.get("drop", [])]
        for a in o.get("add", []):
            f = snap(rgb, a["quad"], tuple(a.get("fixed", [])), a.get("refine", True))
            f["source"] = "manual quad" + (", edge-snapped" if a.get("refine", True) else "")
            if a.get("fixed"):
                f["fixed_sides"] = a["fixed"]
            if a.get("note"):
                f["note"] = a["note"]
            r["figs"].append(f)
        r["figs"].sort(key=lambda f: (f["box"][1] // 600, f["box"][0]))
        res[str(n)] = r
        v = cv2.resize(rgb, (rgb.shape[1] // 6, rgb.shape[0] // 6)).copy()
        cv2.polylines(v, [np.int32(np.array(r["paper"]) / 6)], True, (0, 120, 255), 2)
        for i, f in enumerate(r["figs"]):
            q = np.int32(np.array(f["quad"]) / 6)
            cv2.polylines(v, [q], True, (255, 0, 0), 3)
            cv2.putText(v, str(i), tuple(int(t) for t in q[0] + 8), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)
        cv2.putText(v, f"p{n}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 0, 255), 3)
        Image.fromarray(v).save(W / "viz" / f"p{n:03d}.jpg", quality=80)
        print(n, len(r["figs"]), [f.get("source") for f in r["figs"]], flush=True)
    out.write_text(json.dumps(res, indent=0))


if __name__ == "__main__":
    a = sys.argv[1:]
    main(range(int(a[0]), int(a[1]) + 1) if len(a) == 2 else map(int, a))
