"""Two independent OCR readings of the List of Illustrations (PDF pp. 4-7), compared entry by entry with the
by-eye transcription (list_of_illustrations.json):
  A. Tesseract 5 `Latin` (tessdata_best) on the page photos, each 360-px band levelled first (psm 6)
  B. the PDF's own invisible text layer (Tesseract `eng`, made when the PDF was assembled)
Writes ../_work/list_ocr.json and prints entries where either reading departs from the transcription."""
import difflib, json, re, subprocess, sys, unicodedata
from pathlib import Path
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
PDF = REPO / "PDF Originals" / "The Udayesvara Temple - Anupa Pande (scanned).pdf"
TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSDATA = REPO / "drafting" / "image_store" / "_tools" / "tessdata"


def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    return re.sub(r"\s+", " ", "".join(c for c in s if not unicodedata.combining(c))).lower().strip()


def tess(png, lang="Latin", psm=4):
    r = subprocess.run([TESS, str(png), "stdout", "--tessdata-dir", str(TESSDATA), "-l", lang, "--psm", str(psm)],
                       capture_output=True)
    return r.stdout.decode("utf-8", "replace")


def banded_deskew(png, band=360, overlap=60):
    """The List photos are tilted and the paper curls, so lines are not straight across the page. Cut the page
    into horizontal bands, find each band's skew by the sharpest row profile (-8..8 deg), rotate it level and
    stack the bands. Only for OCR; nothing here is saved to the store."""
    import cv2, numpy as np
    g = cv2.imread(str(png), cv2.IMREAD_GRAYSCALE)
    h, w = g.shape
    out = []
    for y in range(0, h, band):
        y0, y1 = max(0, y - overlap), min(h, y + band + overlap)
        b = g[y0:y1]
        inv = 255 - cv2.threshold(b, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        small = cv2.resize(inv, (w // 4, (y1 - y0) // 4))
        best = (0, 0.0)
        for a in np.arange(-8, 8.01, 0.25):
            M = cv2.getRotationMatrix2D((small.shape[1] / 2, small.shape[0] / 2), a, 1)
            r = cv2.warpAffine(small, M, small.shape[::-1])
            v = float(np.var(r.sum(1)))
            if v > best[1]:
                best = (a, v)
        M = cv2.getRotationMatrix2D((w / 2, (y1 - y0) / 2), best[0], 1)
        rb = cv2.warpAffine(b, M, (w, y1 - y0), borderValue=255)
        out.append(rb[(y - y0):(y - y0) + band])
    tmp = ROOT / "_work" / f"deskew_{png.stem}.png"
    cv2.imwrite(str(tmp), np.vstack(out))
    return tmp


def entries(text):
    """Split OCR text into numbered entries; page numbers in the right column are stripped."""
    out, cur = {}, None
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r"^(\d{1,3})\s*[.,]\s+(.*)$", line)
        if m and 1 <= int(m.group(1)) <= 130 and (cur is None or int(m.group(1)) > cur):
            cur = int(m.group(1)); out[cur] = m.group(2)
        elif cur is not None and line and not re.match(r"^(LIST OF|xi|xii|xiii|xiv|Page No)", line, re.I):
            out[cur] += " " + line
    return {k: re.sub(r"\s+\d{1,2}(-\d{1,2})?\s*$", "", re.sub(r"\s+\d{1,2}(-\d{1,2})?(?=\s)", " ", v)).strip()
            for k, v in out.items()}


def best_window(ref, text):
    """Best fuzzy match of ref anywhere in text (token windows), so column/order scrambles do not matter."""
    rt, tt = fold(ref).split(), fold(text).split()
    n = len(rt)
    best = (0.0, "")
    target = " ".join(rt)
    for w in range(max(1, n - 3), n + 4):
        for i in range(0, max(1, len(tt) - w + 1)):
            cand = " ".join(tt[i:i + w])
            r = difflib.SequenceMatcher(None, target, cand, autojunk=False).quick_ratio()
            if r > best[0] - 0.02:
                r = difflib.SequenceMatcher(None, target, cand, autojunk=False).ratio()
                if r > best[0]:
                    best = (r, cand)
    return best


def main():
    d = pymupdf.open(PDF)
    A, B = {}, {}
    raw = {}
    for p in (4, 5, 6, 7):
        ta = tess(banded_deskew(ROOT / "_work" / "pages" / f"p{p:03d}.png"), psm=6)
        tb = d[p - 1].get_text()
        raw[p] = {"tesseract_latin": ta, "text_layer_eng": tb}
        for k, v in entries(ta).items():
            A.setdefault(k, v)
        for k, v in entries(tb).items():
            B.setdefault(k, v)
    lst = json.loads((ROOT / "list_of_illustrations.json").read_text(encoding="utf-8"))["entries"]
    rows = []
    for e in lst:
        if e["kind"] != "plate":
            continue
        n, ref = e["number"], e["list_caption"]
        pg = e["list_pdf_page"]
        ra, a = best_window(ref, raw[pg]["tesseract_latin"])
        rb, b = best_window(ref, raw[pg]["text_layer_eng"])
        rows.append({"number": n, "transcription": ref, "ocr_A_tesseract_latin": a, "ocr_B_text_layer": b,
                     "sim_A": round(ra, 3), "sim_B": round(rb, 3)})
    (ROOT / "_work" / "list_ocr.json").write_text(json.dumps({"rows": rows, "raw": raw}, ensure_ascii=False,
                                                             indent=1), encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("entries found: A", len(A), " B", len(B))
    low = [r for r in rows if min(r["sim_A"], r["sim_B"]) < 0.9]
    print("mean sim A %.3f  B %.3f; entries below 0.9 on either: %d" % (
        sum(r["sim_A"] for r in rows) / len(rows), sum(r["sim_B"] for r in rows) / len(rows), len(low)))
    for r in low:
        print(f'{r["number"]:>3} A={r["sim_A"]} B={r["sim_B"]}\n    T: {r["transcription"]}\n    A: {r["ocr_A_tesseract_latin"]}\n    B: {r["ocr_B_text_layer"]}')


if __name__ == "__main__":
    main()
