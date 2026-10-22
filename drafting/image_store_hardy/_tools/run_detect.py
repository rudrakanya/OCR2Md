"""Run detect() on every page -> _work/detect.json  {page: {zoom, paper, boxes}}

Second and later runs blank the caption regions in _work/caption_regions.json first, and use the sensitive
(pale-ink) threshold on the pages listed in overrides.json "sensitive_pages".
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WORK, open_pdf  # noqa: E402
from detect import detect  # noqa: E402

ovr_p = Path(__file__).resolve().parent / "overrides.json"
ovr = json.loads(ovr_p.read_text(encoding="utf-8")) if ovr_p.exists() else {}
cf = WORK / "caption_regions.json"
caps = json.loads(cf.read_text(encoding="utf-8")) if cf.exists() else []
d = open_pdf()
out = {}
for i in range(d.page_count):
    p = i + 1
    masks = [c["bbox_px"] for c in caps if c["page"] == p]
    out[str(p)] = detect(d[i], masks=masks, sensitive=p in ovr.get("sensitive_pages", []))
(WORK / "detect.json").write_text(json.dumps(out), encoding="utf-8")
print(sum(len(v["boxes"]) for v in out.values()), "boxes")
