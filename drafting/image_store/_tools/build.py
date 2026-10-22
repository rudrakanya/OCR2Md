"""Build the image store for CII VII.2, *Inscriptions of the Paramāras* (free, local; no API).

  python -I -X utf8 drafting/image_store/_tools/build.py

Inputs: _work/pages/pNNNN.png (native embedded scans, from survey.py), _work/detections.json (detect.py),
the existing layout OCR of the same PDF (kb/_layout/Inscriptions Corpus.layout.jsonl, produced earlier by a
local layout model) and Tesseract (local).
Outputs (in drafting/image_store/): plates/ (image files), image_manifest.jsonl; publish.py then writes
image_index.md, list_of_plates.md and PROVENANCE.md.
"""
from __future__ import annotations

import datetime
import difflib
import html
import io
import json
import os
import re
import shutil
import subprocess
import unicodedata
from pathlib import Path

import numpy as np
from PIL import Image

T = Path(__file__).resolve().parent
STORE = T.parent
WORK = STORE / "_work"
ROOT = STORE.parents[1]
PDF = ROOT / "PDF Originals" / "Inscriptions of the Paramaras.pdf"
LAYOUT = ROOT / "kb" / "_layout" / "Inscriptions Corpus.layout.jsonl"
TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSDATA = T / "tessdata"
LANG = os.environ.get("IMG_OCR_LANG", "Latin" if (TESSDATA / "Latin.traineddata").exists() else "eng")
OUT = Path(os.environ.get("IMG_OUT", str(STORE / "plates")))
MANIFEST = Path(os.environ.get("IMG_MANIFEST", str(STORE / "image_manifest.jsonl")))
CONF_MIN = 80          # mean word confidence below this -> ocr_verify
SIM_MIN = 0.90         # folded similarity between on-page title and List of Plates below this -> ocr_verify

# physical plate pages in page order; Plate LXVII (Ajhari, "Facing page 238") is a blank page (357) in this scan
PLATE_PAGES = [26, 27, 30, 36, 48, 49, 54, 60, 61, 66, 67, 72, 78, 82, 88, 94, 95, 102, 103, 110, 114, 118, 122,
               128, 136, 137, 144, 145, 148, 149, 154, 160, 166, 172, 182, 190, 191, 196, 200, 206, 216, 222, 228,
               230, 238, 250, 251, 266, 276, 277, 282, 286, 292, 296, 302, 310, 312, 318, 319, 330, 331, 336, 337,
               342, 348, 356, 362, 366, 370, 376, 380, 384, 390, 391, 394, 395, 400, 401, 406, 407, 416, 426, 438,
               439, 446, 452, 460, 470, 484, 488, 494]
MISSING = {67: 357}
EMBLEMS = []           # filled from layout boxes on pages 6-7 (the Survey's printed device), see emblems()


def roman(n):
    s = ""
    for a, r in [(90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while n >= a:
            s += r
            n -= a
    return s


ROMAN = {roman(i): i for i in range(1, 100)}


def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def sim(a, b):
    return difflib.SequenceMatcher(None, fold(a), fold(b)).ratio()


def tess_tsv(img, psm="3", lang=None):
    lang = lang or LANG
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    args = [TESS, "stdin", "stdout", "--psm", psm, "-l", lang]
    if (TESSDATA / f"{lang}.traineddata").exists():
        args += ["--tessdata-dir", str(TESSDATA)]
    args.append("tsv")
    r = subprocess.run(args, input=buf.getvalue(), capture_output=True)
    rows = r.stdout.decode("utf-8", "replace").splitlines()
    words = []
    for line in rows[1:]:
        f = line.split("\t")
        if len(f) < 12 or not f[11].strip():
            continue
        words.append({"block": int(f[2]), "par": int(f[3]), "line": int(f[4]), "x": int(f[6]), "y": int(f[7]),
                      "w": int(f[8]), "h": int(f[9]), "conf": float(f[10]), "text": f[11]})
    lines = {}
    for wd in words:
        k = (wd["block"], wd["par"], wd["line"])
        lines.setdefault(k, []).append(wd)
    out = []
    for ws in lines.values():
        x0 = min(w["x"] for w in ws); y0 = min(w["y"] for w in ws)
        x1 = max(w["x"] + w["w"] for w in ws); y1 = max(w["y"] + w["h"] for w in ws)
        out.append({"text": " ".join(w["text"] for w in ws), "bbox": [x0, y0, x1, y1], "words": ws,
                    "conf": round(sum(w["conf"] for w in ws) / len(ws), 1), "n": len(ws)})
    out.sort(key=lambda l: (l["bbox"][1], l["bbox"][0]))
    return out


# ---------------------------------------------------------------- authorities from the front matter and texts
def layout_pages():
    return {json.loads(l)["page"]: json.loads(l) for l in LAYOUT.open(encoding="utf-8")}


def table_rows(md):
    rows = []
    for r in re.findall(r"<tr>(.*?)</tr>", md, re.S):
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)]
        rows.append([c for c in cells])
    return rows


def expand_label(lab):
    """'XVIII-XIX-A' -> ['XVIII', 'XIX-A']; 'I & II' -> ['I', 'II']; 'V-VI' -> ['V', 'VI']; 'LX-LXIII' -> LX..LXIII;
    'XVI-B-XVII' -> ['XVI-B', 'XVII']."""
    lab = lab.replace("&amp;", "&").replace(" ", "").replace("–", "-").replace("—", "-")
    parts = [p for p in re.split(r"[-&]|AND", lab) if p]
    out = []
    for p in parts:
        if p in ("A", "B") and out:
            out[-1] = out[-1] + "-" + p
        elif p in ROMAN:
            out.append(p)
    # a two-numeral range like LX-LXIII means every plate in between
    nums = [o for o in out if "-" not in o]
    if len(out) == 2 and len(nums) == 2 and ROMAN[nums[1]] - ROMAN[nums[0]] > 1:
        out = [roman(i) for i in range(ROMAN[nums[0]], ROMAN[nums[1]] + 1)]
    return out


def list_of_plates(L):
    """The List of Plates (PDF pp. 12-15), from the layout OCR, plus Tesseract's reading of the same pages."""
    entries = []
    for p in (12, 13, 14, 15):
        for row in table_rows(L[p]["markdown"]):
            if not row or not re.match(r"^[IVXLC]", row[0] or ""):
                continue
            where = " ".join(c for c in row[2:] if c).strip()
            entries.append({"label_as_printed": row[0], "title": row[1], "location": where, "list_page": p,
                            "plates": expand_label(row[0])})
    # the layout OCR sometimes drops a numeral letter (it reads 'XXI' for the Dongargaon plate after XXX);
    # where a label falls out of the List's own ascending order, take the nearest following numeral that the
    # printed reading is a subsequence of, and record both.
    prev = 0
    for e in entries:
        nums = [ROMAN[p.split("-")[0]] for p in e["plates"] if p.split("-")[0] in ROMAN]
        if nums and nums[0] < prev:
            for cand in range(prev, prev + 4):
                r = roman(cand)
                if _subseq(e["plates"][0].split("-")[0], r):
                    fixed = [p.replace(e["plates"][0].split("-")[0], r, 1) if i == 0 else p for i, p in enumerate(e["plates"])]
                    e["label_correction"] = {"ocr_read": e["label_as_printed"], "corrected_to": "-".join(fixed),
                                             "why": "out of the List's ascending order; nearest numeral consistent with the reading"}
                    e["plates"] = fixed
                    nums = [cand]
                    break
        if nums:
            prev = max(prev, max(nums))
    tess = {p: (WORK / "frontmatter" / f"p{p:04d}.txt").read_text(encoding="utf-8", errors="replace")
            for p in (12, 13, 14, 15) if (WORK / "frontmatter" / f"p{p:04d}.txt").exists()}
    return entries, tess


def _subseq(s, r):
    it = iter(r)
    return all(c in it for c in s)


def lop_str(e):
    lab = e["label_correction"]["corrected_to"] + f' [OCR read "{e["label_as_printed"]}"]' if e.get("label_correction") else e["label_as_printed"]
    return f'{lab}: {e["title"]} ({e["location"]})'


def contents_and_headings(L):
    """Inscription numbers per plate, from the Contents (pp. 8-11) and from each edition's heading
    ('No. 19; PLATE XXI-A')."""
    cont = []
    for p in (8, 9, 10, 11):
        for row in table_rows(L[p]["markdown"]):
            if row and re.match(r"^\d", row[0] or "") and len(row) > 2:
                cont.append({"nos": row[0], "plate": row[1], "title": row[2], "page": p})
    heads = []
    for p in sorted(L):
        for m in re.finditer(r"(?im)^\s*(?:#+\s*)?(Nos?\.?\s*([\d\- ]+)\s*[;:,]\s*(PLATES?\s*([^\n]{0,40})|No PLATE))",
                             L[p]["markdown"]):
            heads.append({"page": p, "text": m.group(1).strip(), "nos": m.group(2).strip(),
                          "plates": m.group(4) or ""})
    return cont, heads


def nos_final(nos):
    """Contents number(s) when they lie within the edition heading's numbers (a combined heading such as
    'Nos. 25-27; PLATES XXVII-XXX' names several); otherwise both, and the caller flags the conflict."""
    c, h = set(nos["contents"]), set(nos["headings"])
    if c and h and c <= h:
        return sorted(c), False
    return sorted(c | h), bool(c and h and (c - h) and (h - c))


def nos_for(label, cont, heads):
    """Inscription numbers that the Contents and the headings give for one plate label ('XXI-A' or 'XIX')."""
    found = {"contents": set(), "headings": set()}
    base = label.split("-")[0]
    for c in cont:
        labs = expand_label(c["plate"]) if not c["plate"].startswith("(") else []
        if label in labs or (base in labs and "-" not in label) or any(l.split("-")[0] == base and "-" not in label for l in labs):
            found["contents"].update(_nums(c["nos"]))
    hits = []
    for h in heads:
        labs = expand_label(h["plates"].replace(" ", "").replace("AND", "-"))
        labs = [l for l in labs] + [l.replace("-", "") for l in labs]
        if label in labs or label.replace("-", "") in labs or (("-" not in label) and any(l.split("-")[0] == base for l in labs)):
            hits.append((len(expand_label(h["plates"].replace(" ", ""))), h))
    if hits:   # the most specific heading wins over a combined one ("Nos. 25-27; PLATES XXVII-XXX")
        m = min(n for n, _ in hits)
        for n, h in hits:
            if n == m:
                found["headings"].update(_nums(h["nos"]))
    return {k: sorted(v) for k, v in found.items()}


def _nums(s):
    s = s.replace(" ", "")
    m = re.match(r"(\d+)-(\d+)", s)
    if m:
        return list(range(int(m.group(1)), int(m.group(2)) + 1))
    return [int(x) for x in re.findall(r"\d+", s)]


# ---------------------------------------------------------------- captions on a plate page
HEADER_RE = re.compile(r"CORPU|INSCRIPTIONUM|INDICARUM|^\W*VOL\b|^\W*PLATE\s*\S{0,9}\W*$", re.I)


def mask(img, boxes):
    a = np.array(img.convert("L"))
    for x0, y0, x1, y1 in boxes:
        a[max(0, y0 - 6):y1 + 6, max(0, x0 - 6):x1 + 6] = 255
    return Image.fromarray(a)


def rot_box(b, k, w, h):
    """Box in a page rotated by k*90 degrees counter-clockwise (PIL ROTATE_90 = CCW)."""
    x0, y0, x1, y1 = b
    for _ in range(k % 4):
        x0, y0, x1, y1 = y0, w - x1, y1, w - x0
        w, h = h, w
    return [x0, y0, x1, y1]


def wordy(lines):
    """Score of real caption text in OCR lines: confident alphabetic words outside the running header."""
    s = 0
    for l in lines:
        if HEADER_RE.search(l["text"]):
            continue
        for t in l["text"].split():
            if len(re.sub(r"[^A-Za-z]", "", t)) >= 4:
                s += l["conf"] / 100
    return s


HEADER_WORD = re.compile(r"^\W*(CORPU\S*|INSCRI\S*IONUM|INDICARU\S*|V[O0]I?L?\.?|OL\.?|V[OI]L\.|PLATE|[IVXLCN\\|l1]{1,9}\]?)\W*$", re.I)


def horizontal(l):
    x0, y0, x1, y1 = l["bbox"]
    return (x1 - x0) >= 1.2 * (y1 - y0)


def clean_line(l):
    """Drop running-header words ('CORPUS INSCRIPTIONUM INDICARUM', 'VOL. VII', 'PLATE XC') and very low-confidence
    noise at the start of a line (Tesseract sometimes joins the header row to the title); None if nothing is left."""
    ws = list(l["words"])
    while ws and (HEADER_WORD.match(ws[0]["text"]) or
                  (ws[0]["conf"] < 35 and len(re.sub(r"[^A-Za-z]", "", ws[0]["text"])) < 4)):
        ws.pop(0)
    while ws and HEADER_WORD.match(ws[-1]["text"]) and len(ws) > 1 and ws[-1]["conf"] < 35:
        ws.pop()
    if not ws or all(HEADER_WORD.match(w["text"]) for w in ws):
        return None
    x0 = min(w["x"] for w in ws); y0 = min(w["y"] for w in ws)
    x1 = max(w["x"] + w["w"] for w in ws); y1 = max(w["y"] + w["h"] for w in ws)
    return {"text": " ".join(w["text"] for w in ws), "bbox": [x0, y0, x1, y1],
            "conf": round(sum(w["conf"] for w in ws) / len(ws), 1), "n": len(ws), "words": ws}


def page_captions(pno, boxes):
    """Orientation by geometry: if the long caption lines of the upright reading are tall and thin, the plate is
    printed sideways; then both sideways readings are tried and the more confident one kept. In the chosen frame only
    horizontal lines count, and header words are removed word by word."""
    img = Image.open(WORK / "pages" / f"p{pno:04d}.png")
    w, h = img.size
    m = mask(img, boxes)
    lines0 = tess_tsv(m)
    longl = [l for l in lines0 if len(re.sub(r"[^A-Za-z]", "", l["text"])) >= 10 and not HEADER_RE.search(l["text"])]
    vert = sum(len(l["text"]) for l in longl if not horizontal(l))
    hori = sum(len(l["text"]) for l in longl if horizontal(l))
    k, lines, rimg = 0, lines0, m
    if vert > hori:
        best = None
        for kk in (1, 3):
            r = m.transpose({1: Image.ROTATE_90, 3: Image.ROTATE_270}[kk])
            ls = tess_tsv(r)
            sc = wordy([l for l in ls if horizontal(l)])
            if best is None or sc > best[0]:
                best = (sc, kk, ls, r)
        _, k, lines, rimg = best
    rw, rh = (w, h) if k % 2 == 0 else (h, w)
    rboxes = [rot_box(b, k, w, h) for b in boxes]
    out = []
    for l in lines:
        if not horizontal(l) or re.fullmatch(r"[\d\s.,|il]+", l["text"]):
            continue
        c = clean_line(l)
        if c:
            out.append(c)
    return k, out, rboxes, (rw, rh), rimg


def zone_text(rimg, lines, lang="eng"):
    """Second reading of the same caption lines with another model (the zone is the lines' union box)."""
    if not lines:
        return None
    x0 = min(l["bbox"][0] for l in lines) - 10; y0 = min(l["bbox"][1] for l in lines) - 10
    x1 = max(l["bbox"][2] for l in lines) + 10; y1 = max(l["bbox"][3] for l in lines) + 10
    ls = tess_tsv(rimg.crop((max(0, x0), max(0, y0), x1, y1)), psm="6", lang=lang)
    return " ".join(l["text"] for l in ls).strip() or None


def caption_for_region(lines, rb, prev_bottom, next_top):
    above = [l for l in lines if prev_bottom - 5 <= l["bbox"][3] <= rb[1] + 25 and l["bbox"][1] < rb[1]
             and l["bbox"][2] > rb[0] - 150 and l["bbox"][0] < rb[2] + 150 and not HEADER_RE.search(l["text"])]
    below = [l for l in lines if rb[3] - 25 <= l["bbox"][1] <= min(next_top, rb[3] + 260)]
    return above, below


HEADER_BAND = 0.105    # the running header ('CORPUS INSCRIPTIONUM INDICARUM / VOL. VII  PLATE N') sits above this
FACE_RE = re.compile(r"^\s*((?:i{1,3}|iv|vi?)\b(?:\s*\(\w\))?|\([ab]\)|(?:Left|Right)\s+side)\s*$", re.I)
SRC_RE = re.compile(r"(From\s+\w+.*|Scale\s*[:;.]?.*)", re.I)


def classify(note):
    n = (note or "").lower()
    if "photograph" in n:
        return "photograph"
    if "facsimile" in n:
        return "facsimile"
    if "scale" in n:
        return "estampage"
    return "estampage-or-photograph (unstated)"


# ---------------------------------------------------------------- main
def main():
    L = layout_pages()
    lop, lop_tess = list_of_plates(L)
    cont, heads = contents_and_headings(L)
    det = json.loads((WORK / "detections.json").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    labels = [roman(i) for i in range(1, 93) if i not in MISSING]
    assert len(labels) == len(PLATE_PAGES)
    only = {x for x in os.environ.get("IMG_ONLY", "").split(",") if x}
    for lab, pno in zip(labels, PLATE_PAGES):
        if only and lab not in only:
            continue
        n = ROMAN[lab]
        src = WORK / "pages" / f"p{pno:04d}.png"
        im = Image.open(src)
        w, h = im.size
        boxes = [r["bbox"] for r in det[str(pno)]]
        k, lines, rboxes, (rw, rh), rimg = page_captions(pno, boxes)
        # list-of-plates rows that cover this plate (with or without sub-letter)
        rows = [e for e in lop if any(p.split("-")[0] == lab for p in e["plates"])]
        lay = [e["text"].replace("\n", " ") for e in L[pno]["elements"] if e["type"] in ("header", "title", "text")
               and not HEADER_RE.search(e["text"].strip()) and len(e["text"].strip()) > 3]
        # page title: text lines above the first image (reading orientation), excluding the running header
        first_top = min(b[1] for b in rboxes) if rboxes else rh
        title_lines = [l for l in lines if l["bbox"][3] <= first_top + 20 and not HEADER_RE.search(l["text"])
                       and not FACE_RE.match(l["text"])]
        notes_all = [l for l in lines if SRC_RE.match(l["text"].strip())]
        page_title = " ".join(l["text"] for l in title_lines).strip()
        tail_face = re.search(r"\s+((?:[ivt]{1,3}\s*)?\(\w\)|ii|iii)\s*$", page_title)
        if tail_face:      # a face label ('ii (b)') read on the title's last line belongs to the first image
            page_title = page_title[:tail_face.start()].rstrip()
        page_title_eng = zone_text(rimg, title_lines) if LANG != "eng" else None
        title_conf = round(sum(l["conf"] for l in title_lines) / len(title_lines), 1) if title_lines else 0.0
        list_title = " | ".join(lop_str(e) for e in rows)
        s = max([sim(page_title, e["title"]) for e in rows] or [0])
        nos = nos_for(lab, cont, heads)
        parts = [nos_for(f"{lab}-{s}", cont, heads) for s in "AB"]
        if any(p["contents"] or p["headings"] for p in parts):      # a plate in A/B parts carries both parts' numbers
            nos = {k: sorted(set(nos[k]).union(*[p[k] for p in parts])) for k in nos}
        reasons = []
        if title_conf < CONF_MIN:
            reasons.append(f"title OCR mean confidence {title_conf}")
        if s < SIM_MIN:
            reasons.append(f"on-page title differs from List of Plates (similarity {s:.2f})")
        if any(ord(c) > 127 for e in rows for c in e["title"]):
            reasons.append("diacritics: the printed title has IAST marks that the OCR cannot confirm")
        all_nos, conflict = nos_final(nos)
        if conflict:
            reasons.append(f"inscription number differs: Contents {nos['contents']} vs edition heading {nos['headings']}")
        if not page_title:
            reasons.append("no title line read on the page")
        pid = f"CII7.2-P{n:03d}"
        fn = f"plate_{n:03d}.png"
        bi = Image.open(src)
        a = np.array(bi.convert("L"))
        if set(np.unique(a)) <= {0, 255}:
            bi = bi.convert("1")      # bilevel scan: store as 1-bit, lossless
        bi.save(OUT / fn, optimize=True)
        manifest.append({
            "id": pid, "file": f"{OUT.name}/{fn}", "kind": "plate", "label": f"Plate {lab}", "plate_roman": lab,
            "plate_number": n, "sub_label": None,
            "caption": page_title, "caption_source": f"Tesseract ({LANG}) on the plate page, images masked",
            "caption_ocr_eng": page_title_eng,
            "caption_ocr_conf": title_conf,
            "caption_layout_ocr": " | ".join(lay[:4]),
            "list_of_plates": list_title,
            "list_vs_page_similarity": round(s, 2),
            "source_notes": [l["text"] for l in notes_all],
            "page": pno, "orientation_on_page": {0: "upright", 1: "sideways (title reads bottom-to-top)",
                                                 3: "sideways (title reads top-to-bottom)"}[k],
            "image_type": "plate (whole page)", "inscription_nos": all_nos, "inscription_nos_by_source": nos,
            "extraction": "embedded page scan (PDF image XObject), saved losslessly, uncropped",
            "pixels": [w, h], "approx_dpi": round(w / (666 / 72)),
            "ocr_verify": bool(reasons), "ocr_verify_reasons": reasons,
            "page_image": f"_work/pages/p{pno:04d}.png",
        })
        # sub-images
        order = sorted(range(len(rboxes)), key=lambda i: (rboxes[i][1] // 300, rboxes[i][0]))
        title_bottom = max([l["bbox"][3] for l in title_lines] or [0])
        title_is_a = bool(re.match(r"^\s*A\s*[—\-–_.]", page_title))
        cur_sub, used = ("A" if title_is_a else None), set()
        prev_bottom = title_bottom
        for j, i in enumerate(order):
            rb = rboxes[i]
            nxt = min([rboxes[q][1] for q in order[j + 1:]] or [rh])
            above, below = caption_for_region(lines, rb, max(0, prev_bottom - 5), nxt)
            above = [l for l in above if l not in title_lines and not SRC_RE.match(l["text"].strip())]
            prev_bottom = rb[3]
            above_txt = " ".join(l["text"] for l in above).strip()
            leak = re.match(r"^((?:Scale\s*:?\s*)?(?:One|Two|Three|Four|Five|Six|Seven|Same)[\s\-]+\w+)\s+(?=[A-Z])", above_txt)
            scale_leak = None
            if leak:      # the tail of the previous image's 'Scale: ...' line, read as part of this caption
                scale_leak, above_txt = leak.group(1), above_txt[leak.end():]
            mm = re.search(r"(?:^|\s)([AB])\s*(?:[—\-–_]+\s*\S|\s(?=[A-Z]{3}))", above_txt)
            inferred = False
            if mm:
                cur_sub = mm.group(1)
            elif (cur_sub == "A" and j > 0 and re.search(r"INSCRIPTION|GRANT", above_txt)
                  and any(f"{lab}-B" in e["plates"] for e in lop)):
                cur_sub, inferred = "B", True      # the printed 'B' was not read; the List of Plates has a B part
            face = re.match(r"^\s*((?:i{1,3}|iv|vi?)\b(?:\s*\(\w\))?|\([ab]\)|(?:Left|Right)\s+side)", above_txt, re.I)
            face_label = face.group(1) if face else None
            sub = cur_sub
            sublabel = f"{lab}-{sub}" if sub else None
            if j == 0 and title_is_a:
                cap, cconf, cap_eng = page_title, title_conf, page_title_eng
            else:
                cap = above_txt
                cconf = round(sum(l["conf"] for l in above) / len(above), 1) if above else None
                cap_eng = zone_text(rimg, above) if (above and LANG != "eng") else None
            note = " ".join(l["text"] for l in below if SRC_RE.match(l["text"].strip()))
            x0, y0, x1, y1 = boxes[i]
            crop = Image.open(src).crop((x0, y0, x1, y1))
            if k:
                crop = crop.transpose({1: Image.ROTATE_90, 3: Image.ROTATE_270}[k])
            a = np.array(crop.convert("L"))
            if set(np.unique(a)) <= {0, 255}:
                crop = crop.convert("1")
            fl = re.sub(r"[^A-Za-z0-9]+", "", face_label or "")
            suffix = "_".join(x for x in (sub, fl) if x) or str(j + 1)
            if suffix in used:
                suffix = f"{suffix}_{j + 1}"
            used.add(suffix)
            fn2 = f"plate_{n:03d}_{suffix}.png"
            crop.save(OUT / fn2, optimize=True)
            sub_nos = nos_for(sublabel, cont, heads) if sublabel else nos
            sub_all, sub_conflict = nos_final(sub_nos)
            rs = []
            if inferred:
                rs.append("sub-letter B inferred: the printed letter was not read, the List of Plates has a B part")
            if scale_leak and manifest and manifest[-1].get("kind") == "image" and manifest[-1].get("page") == pno:
                manifest[-1]["source_notes"].append(scale_leak)   # belongs to the image above
            if cap and cconf is not None and cconf < CONF_MIN:
                rs.append(f"sub-caption OCR mean confidence {cconf}")
            if sub_conflict:
                rs.append(f"inscription number differs: Contents {sub_nos['contents']} vs edition heading {sub_nos['headings']}")
            if sub and (j == 0 or mm or inferred):
                lrow = [e for e in lop if sublabel in e["plates"]]
                if lrow:
                    s2 = sim(re.sub(r"^.*?\b[AB]\s*[—\-–_.]+\s*", "", cap), lrow[0]["title"])
                    if s2 < SIM_MIN:
                        rs.append(f"sub-caption differs from List of Plates entry for {sublabel} (similarity {s2:.2f})")
                    if any(ord(c) > 127 for c in lrow[0]["title"]):
                        rs.append("diacritics: the printed title has IAST marks that the OCR cannot confirm")
            manifest.append({
                "id": f"{pid}-{suffix}", "file": f"{OUT.name}/{fn2}", "kind": "image", "parent": pid,
                "label": f"Plate {sublabel or lab}" + (f" ({face_label.strip('()')})" if face_label else ""),
                "plate_roman": lab, "plate_number": n, "sub_label": sub or face_label,
                "caption": cap or None, "caption_ocr_conf": cconf, "caption_ocr_eng": cap_eng,
                "plate_caption": page_title,
                "list_of_plates": " | ".join(lop_str(e) for e in lop if (sublabel in e["plates"] if sublabel else
                                                                          any(p.split("-")[0] == lab for p in e["plates"]))),
                "source_notes": [note] if note else [],
                "page": pno, "bbox_on_page": [x0, y0, x1, y1],
                "image_type": classify(note or " ".join(l["text"] for l in notes_all)),
                "inscription_nos": sub_all, "inscription_nos_by_source": sub_nos,
                "extraction": "region detected on the embedded page scan (ink-density core grown to the image's "
                              "own border, captions excluded), cropped losslessly"
                              + (", rotated 90° losslessly to reading orientation" if k else ""),
                "pixels": list(crop.size), "approx_dpi": round(w / (666 / 72)),
                "ocr_verify": bool(rs), "ocr_verify_reasons": rs,
                "page_image": f"_work/pages/p{pno:04d}.png",
            })
        print(lab, pno, k, len(boxes), page_title[:70], flush=True)
    # the missing plate
    for n, pno in MISSING.items():
        lab = roman(n)
        rows = [e for e in lop if any(p.split("-")[0] == lab for p in e["plates"])]
        manifest.append({"id": f"CII7.2-P{n:03d}", "file": None, "kind": "plate", "label": f"Plate {lab}",
                         "plate_roman": lab, "plate_number": n, "caption": None,
                         "list_of_plates": " | ".join(lop_str(e) for e in rows),
                         "page": pno, "image_type": "missing from scan",
                         "inscription_nos": nos_final(nos_for(lab, cont, heads))[0],
                         "ocr_verify": True,
                         "ocr_verify_reasons": [f"plate not present: PDF page {pno} is blank where the List of Plates puts it"]})
    # the Survey's printed device on the title page (p. 6); library stamps (pp. 4, 6, 7, 92, 493, 496) are not the book's
    if not only:
        src = WORK / "pages" / "p0006.png"
        im = Image.open(src); w, h = im.size
        b = (434, 770, 560, 845)                       # layout-model box, 0-1000 page scale
        box = (int(b[0] * w / 1000) - 20, int(b[1] * h / 1000) - 20, int(b[2] * w / 1000) + 20, int(b[3] * h / 1000) + 20)
        c = im.crop(box)
        if set(np.unique(np.array(c.convert("L")))) <= {0, 255}:
            c = c.convert("1")
        c.save(OUT / "emblem_p006.png", optimize=True)
        manifest.append({"id": "CII7.2-E001", "file": f"{OUT.name}/emblem_p006.png", "kind": "emblem",
                         "label": "Emblem of the Archaeological Survey of India (title page)", "plate_roman": None,
                         "plate_number": 999, "sub_label": None, "caption": None,
                         "note": "No printed caption. The device carries a Devanagari motto inside the image, which Tesseract (no Devanagari model installed) does not read.",
                         "page": 6, "bbox_on_page": list(box), "image_type": "emblem (publisher's device)",
                         "inscription_nos": [], "extraction": "box from the existing layout OCR, cropped losslessly with 20 px margin",
                         "pixels": list(c.size), "approx_dpi": round(w / (666 / 72)), "ocr_verify": False,
                         "ocr_verify_reasons": [], "page_image": "_work/pages/p0006.png"})
    manifest.sort(key=lambda r: (r["plate_number"], r["kind"] != "plate", r["id"]))
    with MANIFEST.open("w", encoding="utf-8") as f:
        for r in manifest:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    json.dump({"list_of_plates": lop, "list_of_plates_tesseract": lop_tess, "contents": cont, "headings": heads},
              (WORK / "authorities.json").open("w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("records", len(manifest))


if __name__ == "__main__":
    main()
