"""Build the Pande image store from the detections (free, local).

Inputs: _work/pages/pNNN.png (upright page photos), _work/detect.json (run_detect.py), _work/tsv/*.tsv
(ocr_pages.py), list_of_illustrations.json, the PDF's own text layer.

1. Book page <-> PDF page from the printed folios: four openings were not photographed (book pp. 8-9, 34-35,
   58-59, 82-83), so the offset steps down by two after each gap.
2. Each region gets the label the List gives for that book page; within a page, labels follow reading order
   (rows top to bottom, left to right), which is the author's numbering order. The nearest "Pl. N" caption
   anchor found by OCR is recorded as a cross-check and any disagreement is flagged.
3. On-page caption: the "Pl. N" anchor is searched in Tesseract `Latin` and `eng` page readings and in the
   PDF text layer; its paragraph (to the next anchor or Left:/Right: marker) gives the caption box, which is
   then OCR'd on its own (Tesseract `Latin`, with `eng` and the text layer kept alongside).
4. Files: plates/<name>.png = lossless crop of the photo's bounding box from the decoded camera JPEG (no
   resampling); rectified/<name>.png = the same picture perspective-corrected to a rectangle (resampled,
   Lanczos, at the picture's own pixel size; a convenience copy). _work/cap/<name>.png = caption crop.
"""
import csv
import difflib
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

import cv2
import numpy as np
import pymupdf
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "_work"
PDF = ROOT.parents[1] / "PDF Originals" / "The Udayesvara Temple - Anupa Pande (scanned).pdf"
BOOK = "PANDE-UDT"
PT2PX = 3468 / 624.24        # PDF points -> upright photo pixels

# (first book page, last book page, PDF page - book page)
SEGMENTS = [(1, 7, 7), (10, 33, 5), (36, 57, 3), (60, 81, 1), (84, 199, -1)]
MISSING_OPENINGS = ["8-9", "34-35", "58-59", "82-83"]


def book_to_pdf(bp):
    for a, b, off in SEGMENTS:
        if a <= bp <= b:
            return bp + off
    return None


def pdf_to_book(pp):
    for a, b, off in SEGMENTS:
        if a <= pp - off <= b:
            return pp - off
    return None


def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    return re.sub(r"\s+", " ", "".join(c for c in s if not unicodedata.combining(c))).lower().strip()


def has_iast(s):
    return any(unicodedata.decomposition(c) and not c.isascii() for c in s or "")


def sim(a, b):
    return difflib.SequenceMatcher(None, fold(a), fold(b), autojunk=False).ratio()


# ---------------------------------------------------------------- OCR words
def read_tsv(p):
    rows = []
    with open(p, encoding="utf-8", errors="replace") as f:
        for r in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
            if r.get("level") == "5" and (r.get("text") or "").strip():
                rows.append({"block": int(r["block_num"]), "par": int(r["par_num"]), "line": int(r["line_num"]),
                             "x": int(r["left"]), "y": int(r["top"]), "w": int(r["width"]), "h": int(r["height"]),
                             "conf": float(r["conf"]), "text": r["text"]})
    return rows


def layer_words(page):
    out = []
    for x0, y0, x1, y1, t, b, l, _ in page.get_text("words"):
        out.append({"block": b, "par": 0, "line": l, "x": int(x0 * PT2PX), "y": int(y0 * PT2PX),
                    "w": int((x1 - x0) * PT2PX), "h": int((y1 - y0) * PT2PX), "conf": -1.0, "text": t})
    return out


TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSDATA = ROOT.parents[1] / "drafting" / "image_store" / "_tools" / "tessdata"


def ocr_crop(img, box, lang="Latin"):
    """Tesseract on the caption crop alone (2x upscaled for OCR only; nothing saved). Returns (text, conf)."""
    import subprocess, tempfile
    x0, y0, x1, y1 = box
    crop = img[y0:y1, x0:x1]
    crop = cv2.resize(crop, (crop.shape[1] * 2, crop.shape[0] * 2), interpolation=cv2.INTER_CUBIC)
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "c.png"
        Image.fromarray(crop).save(p)
        r = subprocess.run([TESS, str(p), str(Path(td) / "o"), "--tessdata-dir", str(TESSDATA), "-l", lang,
                            "--psm", "6", "tsv"], capture_output=True)
        rows = read_tsv(Path(td) / "o.tsv") if (Path(td) / "o.tsv").exists() else []
    lines = {}
    for w in rows:
        lines.setdefault((w["block"], w["par"], w["line"]), []).append(w["text"])
    txt = " ".join(" ".join(v) for _, v in sorted(lines.items()))
    conf = round(float(np.mean([w["conf"] for w in rows])), 1) if rows else None
    return txt, conf


ANCHOR = re.compile(r"^(P[lI1|i]|Fig)\.?,?$", re.I)
NUM = re.compile(r"^(\d{1,3})[.,:]?$")


def anchors(words):
    """[(kind, number, word index)] for 'Pl. N' / 'Fig. N' in OCR word order (also 'Pl.N' run together)."""
    out = []
    for i, w in enumerate(words):
        t = w["text"]
        m = re.match(r"^(P[lI1|i]|Fig)\.?(\d{1,3})[.,]?$", t, re.I)
        if m:
            out.append(("figure" if m.group(1).lower() == "fig" else "plate", int(m.group(2)), i))
            continue
        if ANCHOR.match(t) and i + 1 < len(words):
            m2 = NUM.match(words[i + 1]["text"])
            if m2:
                out.append(("figure" if t.lower().startswith("fig") else "plate", int(m2.group(1)), i))
    return out


def _is_stop(words, w):
    if re.match(r"^(Left|Right):?$", w["text"], re.I):
        return True
    if re.match(r"^(P[lI1|i]|Fig)\.?\d", w["text"], re.I):
        return True
    if ANCHOR.match(w["text"]):
        k = words.index(w)
        return k + 1 < len(words) and bool(NUM.match(words[k + 1]["text"]))
    return False


def _run_right(cands, start, h):
    """From start, take words to the right on the same visual line while the gap stays below a column gap."""
    seg, x_end = [start], start["x"] + start["w"]
    yc = start["y"] + start["h"] / 2
    for w in sorted(cands, key=lambda w: w["x"]):
        if w is start or w["x"] < start["x"]:
            continue
        if abs(w["y"] + w["h"] / 2 - yc) > 0.6 * h:
            continue
        if w["x"] - x_end > 2.2 * h:
            break
        seg.append(w); x_end = max(x_end, w["x"] + w["w"]); yc = w["y"] + w["h"] / 2
    return seg


def caption_from(words, i0, max_lines=6):
    """Words of one caption, by geometry: the anchor's line segment, then each next line that starts under the
    caption's left edge at caption line spacing; stops at a Left:/Right: marker or the next anchor, or where the
    lines end. Column gaps (> ~2 x-heights) end a line, so body text beside a caption is not taken.
    Returns (text, [word dicts])."""
    w0 = words[i0]
    h = float(np.median([w["h"] for w in words[i0:i0 + 6]]))
    lines = [_run_right(words, w0, h)]
    left = w0["x"]
    for _ in range(max_lines - 1):
        prev = lines[-1]
        yc = float(np.mean([w["y"] + w["h"] / 2 for w in prev]))
        nxt = [w for w in words if 0.6 * h < (w["y"] + w["h"] / 2 - yc) < 2.4 * h
               and left - 2.0 * h < w["x"] < left + 3.0 * h and w["h"] < 1.8 * h]
        if not nxt:
            break
        first = min(nxt, key=lambda w: (w["y"], w["x"]))
        if _is_stop(words, first):
            break
        seg = _run_right(words, first, h)
        cut = next((k for k, w in enumerate(seg) if k and _is_stop(words, w)), None)
        if cut is not None:
            lines.append(seg[:cut]); break
        lines.append(seg)
    # stop inside the first line too (two captions run on one line are rare but possible)
    first_line = lines[0]
    cut = next((k for k, w in enumerate(first_line) if k > 1 and _is_stop(words, w)), None)
    if cut is not None:
        lines = [first_line[:cut]]
    sel = [w for ln in lines for w in ln]
    return " ".join(w["text"] for w in sel), sel


def box_of(ws, pad=14):
    x0 = min(w["x"] for w in ws) - pad; y0 = min(w["y"] for w in ws) - pad
    x1 = max(w["x"] + w["w"] for w in ws) + pad; y1 = max(w["y"] + w["h"] for w in ws) + pad
    return [max(0, x0), max(0, y0), x1, y1]


def words_in(words, box):
    x0, y0, x1, y1 = box
    return [w for w in words if x0 <= w["x"] + w["w"] / 2 <= x1 and y0 <= w["y"] + w["h"] / 2 <= y1]


# ---------------------------------------------------------------- geometry helpers
def reading_order(figs):
    """Indexes in reading order: rows (vertical overlap) top to bottom, then left to right."""
    idx = sorted(range(len(figs)), key=lambda i: figs[i]["box"][1])
    rows = []
    for i in idx:
        y0, y1 = figs[i]["box"][1], figs[i]["box"][3]
        for r in rows:
            ry0, ry1 = r["y"]
            ov = min(y1, ry1) - max(y0, ry0)
            if ov > 0.4 * min(y1 - y0, ry1 - ry0):
                r["m"].append(i); r["y"] = (min(y0, ry0), max(y1, ry1)); break
        else:
            rows.append({"y": (y0, y1), "m": [i]})
    return [i for r in rows for i in sorted(r["m"], key=lambda k: figs[k]["box"][0])]


def dist_to_box(pt, box):
    x, y = pt
    dx = max(box[0] - x, 0, x - box[2]); dy = max(box[1] - y, 0, y - box[3])
    return float(np.hypot(dx, dy))


def rectify(img, quad):
    q = np.float32(quad)
    w = int(round((np.linalg.norm(q[1] - q[0]) + np.linalg.norm(q[2] - q[3])) / 2))
    h = int(round((np.linalg.norm(q[3] - q[0]) + np.linalg.norm(q[2] - q[1])) / 2))
    M = cv2.getPerspectiveTransform(q, np.float32([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]]))
    return cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)


def tilt_deg(quad):
    q = np.float32(quad)
    a = np.degrees(np.arctan2(q[1][1] - q[0][1], q[1][0] - q[0][0]))
    b = np.degrees(np.arctan2(q[2][1] - q[3][1], q[2][0] - q[3][0]))
    return round(float((a + b) / 2), 2)


CAPBOX = {k: v for k, v in json.loads((ROOT / "_tools" / "overrides.json").read_text(encoding="utf-8"))
          .get("caption_boxes", {}).items() if not k.startswith("_")}

IMAGE_TYPE = {  # by the List wording; photographs unless the List says otherwise
    ("figure", 1): "plan",
}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    det = json.loads((W / "detect_merged.json").read_text())
    lst = json.loads((ROOT / "list_of_illustrations.json").read_text(encoding="utf-8"))
    entries = lst["entries"]
    by_pdf = {}
    missing = []
    for e in entries:
        bp = int(e["book_page"].split("-")[0])
        pp = book_to_pdf(bp)
        e["pdf_page"] = pp
        if pp is None:
            missing.append(e)
        else:
            by_pdf.setdefault(pp, []).append(e)
    doc = pymupdf.open(PDF)
    for d in ("plates", "rectified"):
        (ROOT / d).mkdir(exist_ok=True)
    (W / "cap").mkdir(exist_ok=True)
    records, problems = [], []
    for pp in sorted(set(by_pdf) | {int(k) for k in det}):
        exp = by_pdf.get(pp, [])
        figs = det.get(str(pp), {"figs": []})["figs"]
        if len(exp) != len(figs):
            problems.append(f"p{pp}: {len(figs)} regions, List expects {len(exp)}")
        if not figs:
            continue
        order = reading_order(figs)
        img = np.asarray(Image.open(W / "pages" / f"p{pp:03d}.png").convert("RGB"))
        H, Wd = img.shape[:2]
        wl = read_tsv(W / "tsv" / f"p{pp:03d}.Latin.tsv")
        we = read_tsv(W / "tsv" / f"p{pp:03d}.eng.tsv")
        anc_l, anc_e = anchors(wl), anchors(we)
        layer = doc[pp - 1].get_text("words")
        lw = layer_words(doc[pp - 1])
        anc_t = anchors(lw)
        for k, fi in enumerate(order):
            f = figs[fi]
            e = exp[k] if k < len(exp) else None
            kind, num = (e["kind"], e["number"]) if e else ("unassigned", None)
            name = (f"fig_{num:02d}" if kind == "figure" else f"plate_{num:03d}") if e else f"p{pp:03d}_region{k}"
            rid = f"{BOOK}-" + (f"FIG{num:02d}" if kind == "figure" else f"PL{num:03d}") if e else f"{BOOK}-P{pp:03d}-R{k}"
            # --- caption from OCR
            cap_l = cap_e = layer_txt = None
            cap_box = conf = anchor_xy = None
            anchor_src = None
            found = None
            if e:
                expected_nums = {(x["kind"], x["number"]) for x in exp}
                for src, ws_all, anc in (("Tesseract Latin (page)", wl, anc_l), ("Tesseract eng (page)", we, anc_e),
                                         ("PDF text layer", lw, anc_t)):
                    hits = [a for a in anc if a[0] == kind and a[1] == num]
                    if hits:
                        best = min(hits, key=lambda a: dist_to_box((ws_all[a[2]]["x"], ws_all[a[2]]["y"]), f["box"]))
                        found = (src, ws_all, best[2], False); break
                if not found:   # a misread number: an anchor not expected on this page whose text matches the List
                    cands = []
                    for src, ws_all, anc in (("Tesseract Latin (page)", wl, anc_l), ("Tesseract eng (page)", we, anc_e),
                                             ("PDF text layer", lw, anc_t)):
                        for a in anc:
                            if (a[0], a[1]) in expected_nums:
                                continue
                            t, _ = caption_from(ws_all, a[2])
                            body = re.sub(r"^\S+\s*\S+\s*", "", t)
                            sc = sim(e["list_caption"], body)
                            if sc > 0.55:
                                cands.append((sc, src, ws_all, a))
                    if cands:
                        sc, src, ws_all, a = max(cands, key=lambda c: c[0])
                        found = (src + f", number misread as {a[1]}", ws_all, a[2], True)
            if not found and e and e["label"] in CAPBOX and CAPBOX[e["label"]][0] == pp:
                cap_box = CAPBOX[e["label"]][1]
                anchor_src = "caption box set by hand (no OCR reading found the label)"
            if found:
                anchor_src, ws_all, i0, _ = found
                _, ws = caption_from(ws_all, i0)
                cap_box = box_of(ws)
                anchor_xy = (ws_all[i0]["x"], ws_all[i0]["y"])
            if cap_box:
                cap_l, conf = ocr_crop(img, cap_box, "Latin")
                cap_e, _ = ocr_crop(img, cap_box, "eng")
                bx = [v / PT2PX for v in cap_box]
                layer_txt = " ".join(w[4] for w in layer if bx[0] <= (w[0] + w[2]) / 2 <= bx[2]
                                     and bx[1] <= (w[1] + w[3]) / 2 <= bx[3]) or None
            # nearest anchor overall (cross-check of the reading-order assignment)
            near = None
            if anc_l:
                cand = [a for a in anc_l if a[0] in ("plate", "figure")]
                near = min(cand, key=lambda a: dist_to_box((wl[a[2]]["x"], wl[a[2]]["y"]), f["box"]))
                near = f"{'Fig.' if near[0] == 'figure' else 'Pl.'} {near[1]}"
            # --- files
            x0, y0, x1, y1 = f["box"]
            x0, y0, x1, y1 = max(0, x0), max(0, y0), min(Wd, x1), min(H, y1)
            Image.fromarray(img[y0:y1, x0:x1]).save(ROOT / "plates" / f"{name}.png", compress_level=6)
            quad = np.clip(np.array(f["quad"], float), [0, 0], [Wd - 1, H - 1])
            Image.fromarray(rectify(img, quad)).save(ROOT / "rectified" / f"{name}.png", compress_level=6)
            if cap_box:
                cx0, cy0, cx1, cy1 = cap_box
                Image.fromarray(img[cy0:min(H, cy1), cx0:min(Wd, cx1)]).save(W / "cap" / f"{name}.png")
            # --- strip the label from the OCR caption for comparison with the List
            cap_body = re.sub(r"^(P[lI1|i]|Fig)\.?\s*\d{1,3}[.,]?\s*", "", cap_l or "", flags=re.I).strip()
            s_list = round(sim(e["list_caption"], cap_body), 3) if (e and cap_l) else None
            rec = {
                "id": rid, "book": BOOK, "file": f"plates/{name}.png", "file_rectified": f"rectified/{name}.png",
                "kind": kind, "number": num,
                "label": e["label"] if e else None,
                "label_long": (f"Figure {num}" if kind == "figure" else f"Plate {num}") if e else None,
                "sub_label": None,
                "caption": e["list_caption"] if e else None,
                "caption_source": "List of Illustrations (book pp. xi-xiv), transcribed by eye" if e else None,
                "caption_on_page_ocr": cap_l, "caption_on_page_ocr_eng": cap_e, "caption_on_page_text_layer": layer_txt,
                "caption_ocr_conf": conf, "caption_anchor_source": anchor_src, "list_vs_page_similarity": s_list,
                "caption_box": cap_box,
                "book_page": e["book_page"] if e else str(pdf_to_book(pp)),
                "page": pp, "pdf_page": pp,
                "image_type": IMAGE_TYPE.get((kind, num), "photograph"),
                "colour": None,
                "quad": f["quad"], "box": [x0, y0, x1, y1], "tilt_deg": tilt_deg(f["quad"]),
                "region_source": f.get("source"), "region_note": f.get("note"),
                "sides_from_run": f.get("sides_from"), "sides_by_hand": f.get("sides_by_hand"),
                "fixed_sides": f.get("fixed_sides"), "edge_scores": f.get("edge_scores"),
                "pixels": [x1 - x0, y1 - y0],
                "extraction": "lossless crop (bounding box of the detected picture) from the decoded camera JPEG "
                              "embedded in the PDF, rotated upright by an exact 90-degree turn; not resampled",
                "extraction_rectified": "perspective-corrected copy (Lanczos resampling) at the picture's own size",
                "nearest_anchor": near, "anchor_xy": anchor_xy,
                "page_image": f"_work/pages/p{pp:03d}.png",
                "caption_image": f"_work/cap/{name}.png" if cap_box else None,
            }
            # colour or monochrome, from the crop's chroma
            hsv = cv2.cvtColor(img[y0:y1, x0:x1], cv2.COLOR_RGB2HSV)
            rec["colour"] = "colour" if float(np.percentile(hsv[..., 1], 75)) > 60 else "black-and-white"
            records.append(rec)
    for e in missing:
        records.append({
            "id": f"{BOOK}-PL{e['number']:03d}", "book": BOOK, "file": None, "file_rectified": None,
            "kind": e["kind"], "number": e["number"], "label": e["label"], "label_long": f"Plate {e['number']}",
            "sub_label": None, "caption": e["list_caption"],
            "caption_source": "List of Illustrations (book pp. xi-xiv), transcribed by eye",
            "book_page": e["book_page"], "page": None, "pdf_page": None,
            "image_type": "photograph", "not_in_pdf": True,
            "notes": [f"book p. {e['book_page']} is on an opening that was not photographed "
                      f"(missing openings: {', '.join('pp. ' + m for m in MISSING_OPENINGS)})"],
        })
    records.sort(key=lambda r: (0 if r["kind"] == "figure" else 1, r["number"] or 0))
    (W / "build_records.json").write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(records), "records;", sum(1 for r in records if r.get("file")), "with files")
    for p in problems:
        print("COUNT", p)
    for r in records:
        if r.get("file") and r["nearest_anchor"] and r["nearest_anchor"] != r["label"]:
            print("ANCHOR", r["id"], "assigned", r["label"], "nearest anchor", r["nearest_anchor"], "p", r["page"])
        if r.get("file") and not r.get("caption_on_page_ocr"):
            print("NOCAP", r["id"], "p", r["page"])


if __name__ == "__main__":
    main()
