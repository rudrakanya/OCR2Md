# -*- coding: utf-8 -*-
"""Find the iconographic inventory table in ADH's 51-page image-only scan.

The markdown holds that table only as ~51 one-row stubs, 45 of them identical.
To say what was lost we have to read the pages themselves. Every page is OCR'd
at 250 dpi and scored for the table's own vocabulary; pages that score are kept
in full so the rows can be counted.
"""
import json
import os
import pathlib
import re
import subprocess
import tempfile

import pymupdf

TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "kb_audit" / "adh_sweep.json"
MARKERS = ("attribution", "posture", "other features", "dhyanamudra", "padma",
           "four handed", "location", "u.k.", "u.l.", "image")

env = dict(os.environ)
env["TESSDATA_PREFIX"] = str(pathlib.Path.home() / "tessdata")

doc = pymupdf.open(ROOT / "remaining pdf" / "Some Paramara Templess.pdf")
rows = []
with tempfile.TemporaryDirectory() as td:
    img = pathlib.Path(td) / "page.png"
    for i in range(doc.page_count):
        img.write_bytes(doc[i].get_pixmap(dpi=250).tobytes("png"))
        r = subprocess.run([TESS, str(img), "stdout", "-l", "eng", "--psm", "6"],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", env=env)
        t = r.stdout or ""
        tl = t.lower()
        score = sum(m in tl for m in MARKERS)
        # a column-ish line: three or more runs separated by wide gaps
        cols = len(re.findall(r"(?m)^\S.*?\s{3,}\S.*?\s{3,}\S", t))
        rows.append({"page": i + 1, "chars": len(t.strip()), "markers": score,
                     "col_lines": cols, "text": t if score >= 4 else ""})
        print(f"p{i+1:3d} chars {len(t.strip()):5d} markers {score} cols {cols:3d}", flush=True)
doc.close()

OUT.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
hits = sorted((r for r in rows if r["markers"] >= 4), key=lambda r: -r["col_lines"])
print("\ncandidate table pages:", [(r["page"], r["markers"], r["col_lines"]) for r in hits[:8]])
print("wrote", OUT)
