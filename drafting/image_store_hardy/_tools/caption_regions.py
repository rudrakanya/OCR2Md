"""Fix each caption's region on the page image, find captions the text layer missed, and OCR them all.

1. Region: from the caption's first line (text layer), the box is grown over the page image: down through rows
   that carry ink in the caption column, until a blank band taller than GAP_PT, a picture box or the next caption;
   then right until a blank column band wider than COLGAP_PT (the gutter). Never into a picture box.
2. Orphans: small-set, word-like text-layer lines next to a picture (within NEAR_PT) that no caption covers are
   grouped into blocks and treated as captions whose number the text layer misread; the number is read by OCR.
3. Every region is read by Tesseract 5 (eng, LSTM, psm 6) at the scan's native resolution.

  python -I -X utf8 drafting/image_store_hardy/_tools/caption_regions.py  -> _work/caption_regions.json, _work/cap/*.png
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import CAP_MAX_H, CAP_RE, WORK, is_texty, lines, native_zoom, open_pdf, render  # noqa: E402

TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
GAP_PT = 5.0
COLGAP_PT = 9.0
MAXW_PT = 230
NEAR_PT = 40
FOOT_Y = 680          # running heads / folios sit below this
OVR_PATH = Path(__file__).resolve().parent / "overrides.json"
OVR = json.loads(OVR_PATH.read_text(encoding="utf-8")) if OVR_PATH.exists() else {}


def ink_mask(rgb, paper):
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    return (g < paper - 45).astype(np.uint8)


def inside(b, boxes, pad=0):
    x0, y0, x1, y1 = b
    for c in boxes:
        if x0 < c[2] + pad and c[0] - pad < x1 and y0 < c[3] + pad and c[1] - pad < y1:
            return c
    return None


def grow(ink, box, pics, stops, z, upleft=False):
    """box in native px; pics = picture boxes; stops = y of other caption heads in the same column.
    upleft: also grow up and left (orphan blocks, whose first line the text layer missed)."""
    H, W = ink.shape
    x0, y0, x1, y1 = box
    gap = int(GAP_PT * z)
    colgap = int(COLGAP_PT * z)
    maxw = int(MAXW_PT * z)
    for _ in range(3):
        if upleft:
            y, blank = y0 - 1, 0
            while y > 0:
                if inside((x0, y, x1, y + 1), pics):
                    break
                if ink[y, x0:x1].sum() > 2:
                    y0, blank = y, 0
                else:
                    blank += 1
                    if blank > gap:
                        break
                y -= 1
            x, blank = x0 - 1, 0
            while x > 0 and x > x1 - maxw:
                if inside((x, y0, x + 1, y1), pics):
                    break
                if ink[y0:y1, x].sum() > 1:
                    x0, blank = x, 0
                else:
                    blank += 1
                    if blank > colgap:
                        break
                x -= 1
        # down
        y = y1
        blank = 0
        while y < H - 1:
            if any(s - 4 <= y for s in stops if s > y0 + 5) or inside((x0, y, x1, y + 1), pics):
                break
            if ink[y, x0:x1].sum() > 2:
                y1 = y + 1
                blank = 0
            else:
                blank += 1
                if blank > gap:
                    break
            y += 1
        # right
        x = x1
        blank = 0
        while x < min(W - 1, x0 + maxw):
            if inside((x, y0, x + 1, y1), pics):
                break
            if ink[y0:y1, x].sum() > 1:
                x1 = x + 1
                blank = 0
            else:
                blank += 1
                if blank > colgap:
                    break
            x += 1
    return [x0, y0, x1, y1]


def ocr(img):
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "c.png"
        cv2.imwrite(str(p), cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        r = subprocess.run([TESS, str(p), "stdout", "-l", "eng", "--psm", "6", "tsv"], capture_output=True,
                           text=True, encoding="utf-8")
    words, confs = [], []
    lines_ = {}
    for row in r.stdout.splitlines()[1:]:
        f = row.split("\t")
        if len(f) < 12 or not f[11].strip():
            continue
        key = (int(f[2]), int(f[3]), int(f[4]))
        lines_.setdefault(key, []).append(f[11])
        confs.append(float(f[10]))
    text_lines = [" ".join(v) for k, v in sorted(lines_.items())]
    return text_lines, (sum(confs) / len(confs) if confs else 0.0), min(confs) if confs else 0.0


def main():
    d = open_pdf()
    caps = json.loads((WORK / "captions.json").read_text(encoding="utf-8"))
    det = json.loads((WORK / "detect.json").read_text(encoding="utf-8"))
    capdir = WORK / "cap"
    capdir.mkdir(exist_ok=True)
    out = []
    for pno in range(1, d.page_count + 1):
        page = d[pno - 1]
        pcaps = [c for c in caps if c["page"] == pno]
        pics = det[str(pno)]["boxes"]
        if not pcaps and not pics and not any(m["page"] == pno for m in OVR.get("captions", [])):
            continue
        z = native_zoom(page)
        rgb = render(page, z)
        ink = ink_mask(rgb, det[str(pno)]["paper"])
        L = lines(page)
        # orphan small-text blocks next to pictures
        notes_y = min([l[1] for l in L if l[4].strip() in ("Notes", "NOTES")] or [9e9])
        covered = [c["bbox_pt"] for c in pcaps]
        small = [l for l in L if (l[3] - l[1]) <= CAP_MAX_H + 0.6 and l[1] < FOOT_Y and l[1] < notes_y
                 and is_texty(l[4]) and not inside(l[:4], covered, 1)]
        small.sort(key=lambda l: (round(l[0] / 4), l[1]))
        blocks = []
        for l in small:
            for bl in blocks:
                if abs(bl[-1][0] - l[0]) <= 3.5 and 0 <= l[1] - bl[-1][3] <= GAP_PT + 3:
                    bl.append(l)
                    break
            else:
                blocks.append([l])
        for bl in blocks:
            bb = [min(l[0] for l in bl), min(l[1] for l in bl), max(l[2] for l in bl), max(l[3] for l in bl)]
            near = inside([v * z for v in bb], pics, NEAR_PT * z)
            if near and (len(bl) >= 2 or len(bl[0][4]) > 25):
                pcaps.append({"page": pno, "label": None, "kind": "orphan", "chapter": None, "number": None,
                              "lines": [l[4] for l in bl], "credit_lines": [], "dropped_noise": [],
                              "bbox_pt": [round(v, 1) for v in bb], "caption_textlayer": " ".join(l[4] for l in bl),
                              "credit": None})
        heads = [(c["bbox_pt"][0] * z, c["bbox_pt"][1] * z) for c in pcaps]
        for c in pcaps:
            b = [int(c["bbox_pt"][0] * z) - 4, int(c["bbox_pt"][1] * z) - 3, int(c["bbox_pt"][2] * z) + 3,
                 int(c["bbox_pt"][3] * z) + 3]
            stops = [hy for hx, hy in heads if abs(hx - b[0]) < 20 * z and hy > b[1] + 5]
            c["bbox_px"] = grow(ink, b, pics, stops, z, upleft=c["kind"] == "orphan")
        # hand-placed captions (heads the text layer missed entirely, captions of part-opener photos,
        # continuation blocks): the region is the ink inside the rough rectangle
        for m in OVR.get("captions", []):
            if m["page"] != pno:
                continue
            r = [int(v * z) for v in m["rough_pt"]]
            sub = ink[r[1]:r[3], r[0]:r[2]]
            ys, xs = np.nonzero(sub)
            bb = [r[0] + int(xs.min()), r[1] + int(ys.min()), r[0] + int(xs.max()) + 1, r[1] + int(ys.max()) + 1]
            lab = m.get("label")
            pcaps = [c for c in pcaps if not (lab and c["label"] == lab and m.get("kind", "figure") not in ("continuation", "append"))]
            pcaps.append({"page": pno, "label": lab, "kind": m.get("kind", "figure"), "of": m.get("of"),
                          "chapter": int(lab.split(".")[0]) if lab and lab[0].isdigit() else None,
                          "number": int(lab.split(".")[1]) if lab and lab[0].isdigit() else None,
                          "lines": [], "credit_lines": [], "dropped_noise": [], "bbox_pt": m["rough_pt"],
                          "caption_textlayer": None, "credit": None, "bbox_px": bb, "manual": True})
        # an orphan block lying inside another caption's region is a duplicate; one that starts just under
        # a caption, on the same left edge, is that caption's continuation
        keep = []
        for c in sorted(pcaps, key=lambda c: (c["kind"] == "orphan", c["bbox_px"][1])):
            if c["kind"] == "orphan" and not c.get("manual"):
                host = None
                for k in keep:
                    kb, cb = k["bbox_px"], c["bbox_px"]
                    if inside(cb, [kb], -int(1 * z)):
                        host = k
                        break
                    if 0 <= cb[1] - kb[3] <= 14 * z and abs(cb[0] - kb[0]) <= 8 * z:
                        host = k
                        break
                if host is not None:
                    hb, cb = host["bbox_px"], c["bbox_px"]
                    host["bbox_px"] = [min(hb[0], cb[0]), min(hb[1], cb[1]), max(hb[2], cb[2]), max(hb[3], cb[3])]
                    continue
            keep.append(c)
        pcaps = keep
        for c in pcaps:
            b = c["bbox_px"]
            pad = int(2 * z)
            b = [max(0, b[0] - pad), max(0, b[1] - pad), min(rgb.shape[1], b[2] + pad), min(rgb.shape[0], b[3] + pad)]
            crop = rgb[b[1]:b[3], b[0]:b[2]]
            tl, conf, mn = ocr(crop)
            c["bbox_px"] = b
            c["zoom"] = z
            c["ocr_lines"] = tl
            c["ocr_conf"] = round(conf, 1)
            c["ocr_minconf"] = round(mn, 1)
            tag = (c["label"] or f"{c['kind']}_{int(b[1])}").replace(" ", "_")
            if c["label"] and c["kind"] in ("append", "continuation"):
                tag += f"_{c['kind']}_{int(b[1])}"
            c["crop"] = f"cap/p{pno:03d}_{tag}.png"
            cv2.imwrite(str(WORK / c["crop"]), cv2.cvtColor(crop, cv2.COLOR_RGB2BGR))
            if c["kind"] == "orphan":
                m = CAP_RE.match(tl[0]) if tl else None
                if m and 1 <= int(m.group(1)) <= 27:
                    c["label"] = f"{int(m.group(1))}.{int(m.group(2))}"
                    c["chapter"], c["number"] = int(m.group(1)), int(m.group(2))
                    c["kind"] = "figure"
                    c["label_source"] = "OCR of the caption block (text layer missed its first line)"
            rk = f"{pno}:{c.get('label')}"
            if rk in OVR.get("relabel", {}):
                c["label_printed_as"] = c["label"]
                c["label"] = OVR["relabel"][rk]
                c["chapter"], c["number"] = (int(v) for v in c["label"].split("."))
            out.append(c)
        print(pno, len(pcaps), flush=True)
    (WORK / "caption_regions.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
