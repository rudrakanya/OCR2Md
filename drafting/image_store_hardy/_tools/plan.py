"""Load detection, captions and overrides; return the final list of figures (boxes paired with labels)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assign import figures  # noqa: E402
from common import WORK, native_zoom  # noqa: E402
from detect import colour_box, tighten  # noqa: E402

TOOLS = Path(__file__).resolve().parent


def load_all(d):
    ovr = json.loads((TOOLS / "overrides.json").read_text(encoding="utf-8"))
    det = json.loads((WORK / "detect.json").read_text(encoding="utf-8"))
    caps = json.loads((WORK / "caption_regions.json").read_text(encoding="utf-8"))
    tight = {}
    for p in ovr.get("colour_box_pages", []):
        tight.setdefault(p, []).append(colour_box(d[p - 1]))
        det[str(p)]["boxes"] = []
    for b in ovr.get("boxes", []):
        p = b["page"]
        z = native_zoom(d[p - 1])
        masks = [c["bbox_px"] for c in caps if c["page"] == p]
        rough = [v * z for v in b["rough_pt"]]
        t = rough if b.get("exact") else tighten(d[p - 1], rough, masks, sensitive=p in ovr.get("sensitive_pages", []))
        tight.setdefault(p, []).append([int(v) for v in t])
    return ovr, det, caps, tight


def plan(d):
    ovr, det, caps, tight = load_all(d)
    return ovr, det, caps, figures(det, caps, ovr, tight)
