# -*- coding: utf-8 -*-
"""Is the damage recoverable, and what settings recover it?

Phase 1 OCR'd every scan at 400 dpi with --psm 3 and no orientation check. For
ADH that was wrong twice over: the pages store one pixel per point (so 400 dpi
upscales a 72-dpi scan 5.6x) and they are bound sideways, which is why page 25
melted into 154 bodiless table headers. This measures, per book, what the old
settings recovered against what native-resolution-plus-orientation recovers, so
the re-OCR list rests on a demonstrated gain rather than a hypothesis.
"""
import json
import os
import pathlib
import re
import subprocess
import tempfile

import pymupdf
import yaml
from PIL import Image

TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
ROOT = pathlib.Path(__file__).resolve().parent.parent
env = dict(os.environ)
env["TESSDATA_PREFIX"] = str(pathlib.Path.home() / "tessdata")

COMMON = {"the", "and", "of", "in", "is", "are", "with", "temple", "image", "this",
          "from", "has", "have", "been", "its", "which", "that", "was", "were",
          "stone", "figure", "hand", "left", "right", "panel", "god", "siva",
          "century", "inscription", "king", "india", "north", "south", "period"}


def english(t):
    toks = re.findall(r"[A-Za-z]{2,}", t.lower())
    return round(sum(1 for x in toks if x in COMMON) / max(1, len(toks)), 3)


def tess(path, psm="3", lang="eng", extra=()):
    r = subprocess.run([TESS, str(path), "stdout", "-l", lang, "--psm", psm, *extra],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env)
    return (r.stdout or "").strip()


def osd_angle(path):
    out = tess(path, psm="0")
    m = re.search(r"Rotate: (\d+)", out)
    return int(m.group(1)) if m else 0


BOOKS = ROOT / "Udaypur Reference Markdown Files"
reg = yaml.safe_load(open(ROOT / "kb_audit/source_registry.yaml", encoding="utf-8"))
by_code = {s.get("code"): s for s in reg["sources"]}
pdfmap = yaml.safe_load(open(ROOT / "kb_audit/source_pdfs.yaml", encoding="utf-8"))["sources"]

WORD = re.compile(r"[A-Za-z\u0900-\u097F]{4,}")
report = {}

for code in ("ADH", "GUP", "INT-ARC", "SIN-T"):
    e = pdfmap[code]
    pdf = ROOT / e["pdf"]
    md = (BOOKS / by_code[code]["file"]).read_text(encoding="utf-8", errors="replace")
    md_tok = {w.lower() for w in WORD.findall(md)}

    doc = pymupdf.open(pdf)
    idxs = [int(doc.page_count * f) for f in (0.25, 0.45, 0.65, 0.85)]
    rows = []
    with tempfile.TemporaryDirectory() as td:
        td = pathlib.Path(td)
        for i in idxs:
            page = doc[min(i, doc.page_count - 1)]
            old = td / "old.png"
            old.write_bytes(page.get_pixmap(dpi=400).tobytes("png"))
            t_old = tess(old, psm="3")

            nat = td / "nat.png"
            nat.write_bytes(page.get_pixmap(dpi=72).tobytes("png"))
            ang = osd_angle(nat)
            im = Image.open(nat)
            if ang:
                im = im.rotate(-ang, expand=True)
            fix = td / "fix.png"
            im.resize((im.width * 2, im.height * 2), Image.LANCZOS).save(fix)
            t_new = tess(fix, psm="6")

            def recall(t):
                u = {w.lower() for w in WORD.findall(t)}
                return round(len(u & md_tok) / len(u), 3) if u else None

            rows.append({"page": i + 1, "osd_rotate": ang,
                         "old_chars": len(t_old), "old_english": english(t_old),
                         "old_recall": recall(t_old),
                         "new_chars": len(t_new), "new_english": english(t_new),
                         "new_recall": recall(t_new)})
    doc.close()
    report[code] = rows
    print(f"\n=== {code} ({pdf.name}) ===")
    print(f"{'page':>5} {'rot':>4} | {'old chars':>9} {'eng':>6} {'recall':>7} "
          f"| {'new chars':>9} {'eng':>6} {'recall':>7}")
    for r in rows:
        print(f"{r['page']:>5} {r['osd_rotate']:>4} | {r['old_chars']:>9} "
              f"{r['old_english']:>6.1%} {str(r['old_recall']):>7} "
              f"| {r['new_chars']:>9} {r['new_english']:>6.1%} {str(r['new_recall']):>7}")

(ROOT / "kb_audit" / "reocr_feasibility.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
print("\nwrote kb_audit/reocr_feasibility.json")
