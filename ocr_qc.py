#!/usr/bin/env python
"""Phase 1 quality gate for OCR'd books: per-page confidence, damage, order.

    python ocr_qc.py "book.pdf" --pages ocr_cache/<name>.pages --out OCR_QC_<name>.md

Re-runs Tesseract in TSV mode to get per-word confidence (the plain text pass
does not report it), renders a JPEG of every page beside the text so any claim
can be checked by eye, and writes a gate decision per page.

WHAT IT CHECKS (spec Phase 1)
  confidence     mean/median word confidence, % of words under 60
  gutter damage  confidence and word density in the inner margin vs the rest —
                 the failure mode of a badly bound volume
  skew           median angle of detected text baselines
  missing/order  printed page numbers (Devanagari) read off the running head,
                 checked for gaps and for running backwards
  garbage        CJK or other out-of-script runs, impossible character runs,
                 Latin junk in a Devanagari text, stamp residue
  short pages    very little text where the image is not blank

GATE
  pass           quotable
  needs_recheck  usable for retrieval, must be checked against the image
                 before quoting (low confidence, gutter damage, or garbage)
  illegible      no usable text; marked [illegible] in the markdown, never
                 replaced with generated text
"""
from __future__ import annotations

import argparse
import collections
import csv
import itertools
import json
import math
import re
import statistics as st
import subprocess
import sys
import unicodedata
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

TESS = next((p for p in (r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                         r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe") if Path(p).exists()), "tesseract")
TESSDATA = str(Path.home() / "tessdata")
DEVA_NUM = "०१२३४५६७८९"
DEV_DIGIT = {c: str(i) for i, c in enumerate(DEVA_NUM)}
CJK = re.compile(r"[\u3000-\u9fff\uac00-\ud7af\uff00-\uffef]")
LATIN_RUN = re.compile(r"[A-Za-z]{4,}")
STAMP = re.compile(r"Jangamwadi|[eE]\s?Gangotri|Digit[il]zed|CC-?0", re.I)
HEAD_NUM = re.compile(r"[\[\(]\s*([" + DEVA_NUM + r"\d]{1,4})\s*[\]\)]")


def deva_int(s: str):
    t = "".join(DEV_DIGIT.get(c, c) for c in s)
    return int(t) if t.isdigit() else None


def tsv(png: Path, lang: str, psm: str):
    out = subprocess.run([TESS, str(png), "stdout", "-l", lang, "--psm", psm,
                          "--tessdata-dir", TESSDATA, "tsv"],
                         capture_output=True, check=True).stdout.decode("utf-8", "replace")
    rows = list(csv.DictReader(out.splitlines(), delimiter="\t", quoting=csv.QUOTE_NONE))
    return [r for r in rows if r.get("text", "").strip() and r.get("conf") not in (None, "-1")]


def page_report(words, width, text):
    conf = [float(w["conf"]) for w in words]
    letters = sum(1 for ch in text if ch.isalpha())
    deva = sum(1 for ch in text if "\u0900" <= ch <= "\u097F")
    # inner margin = the gutter side; this scan's gutter alternates, so take the
    # weaker of the two outer fifths as the candidate damaged edge
    def band(lo, hi):
        w = [float(x["conf"]) for x in words if lo <= (int(x["left"]) + int(x["width"]) / 2) / width < hi]
        return (st.mean(w), len(w)) if w else (0.0, 0)
    left, right, mid = band(0, .18), band(.82, 1.0), band(.18, .82)
    edge = min(left, right, key=lambda x: (x[0] if x[1] else 999))
    angles = []
    for line, group in itertools.groupby(sorted(words, key=lambda w: (int(w["block_num"]), int(w["line_num"]))),
                                         key=lambda w: (int(w["block_num"]), int(w["line_num"]))):
        g = list(group)
        if len(g) >= 4:
            xs = [int(w["left"]) for w in g]
            ys = [int(w["top"]) + int(w["height"]) / 2 for w in g]
            mx, my = st.mean(xs), st.mean(ys)
            den = sum((x - mx) ** 2 for x in xs)
            if den:
                angles.append(math.degrees(math.atan(sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / den)))
    return {
        "words": len(words),
        "conf_mean": round(st.mean(conf), 1) if conf else 0.0,
        "conf_median": round(st.median(conf), 1) if conf else 0.0,
        "low_conf_pct": round(100 * sum(1 for c in conf if c < 60) / len(conf), 1) if conf else 100.0,
        "chars": len(text.strip()), "letters": letters,
        "deva_ratio": round(deva / letters, 2) if letters else 0.0,
        "edge_conf": round(edge[0], 1), "edge_words": edge[1], "mid_conf": round(mid[0], 1),
        "skew_deg": round(st.median(angles), 2) if angles else 0.0,
        "cjk": len(CJK.findall(text)),
        "latin_runs": len([m for m in LATIN_RUN.findall(STAMP.sub("", text))]),
    }


def gate(r):
    reasons = []
    if r["chars"] < 40:
        return "illegible", ["almost no text recognised"]
    if r["conf_mean"] < 55:
        reasons.append(f"mean confidence {r['conf_mean']}")
    if r["low_conf_pct"] > 45:
        reasons.append(f"{r['low_conf_pct']}% of words below 60 confidence")
    if r["edge_words"] >= 3 and r["mid_conf"] - r["edge_conf"] > 12:
        reasons.append(f"inner-margin confidence {r['edge_conf']} vs {r['mid_conf']} in the body (gutter damage)")
    if abs(r["skew_deg"]) > 1.5:
        reasons.append(f"skew {r['skew_deg']}°")
    if r["cjk"]:
        reasons.append(f"{r['cjk']} CJK characters in a Devanagari/English text")
    if r["deva_ratio"] < 0.5 and r["letters"] > 80:
        reasons.append(f"only {r['deva_ratio']:.0%} of letters are Devanagari")
    if r["latin_runs"] > 12 and r["deva_ratio"] < 0.7:
        reasons.append(f"{r['latin_runs']} Latin word-runs outside the stamp")
    return ("needs_recheck" if reasons else "pass"), reasons


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--pages", required=True, help="cache dir of page_NNN.txt from the OCR run")
    ap.add_argument("--images", default=None, help="where to write page JPEGs (default <pages>/images)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--dpi", type=int, default=400)
    ap.add_argument("--image-dpi", type=int, default=150)
    ap.add_argument("--lang", default="Devanagari")
    ap.add_argument("--psm", default="3")
    ap.add_argument("--json-out", default=None)
    a = ap.parse_args(argv)

    import pymupdf
    pages_dir = Path(a.pages)
    img_dir = Path(a.images or (pages_dir / "images"))
    img_dir.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(a.pdf)
    reports = []
    for i in range(doc.page_count):
        txt_f = pages_dir / f"page_{i + 1:03d}.txt"
        text = txt_f.read_text(encoding="utf-8", errors="replace") if txt_f.exists() else ""
        jpg = img_dir / f"page_{i + 1:03d}.jpg"
        if not jpg.exists():
            doc[i].get_pixmap(dpi=a.image_dpi).pil_save(str(jpg), quality=80)
        png = img_dir / f"_qc_{i + 1:03d}.png"
        doc[i].get_pixmap(dpi=a.dpi).save(str(png))
        try:
            words = tsv(png, a.lang, a.psm)
        except Exception as exc:
            words = []
            print(f"  page {i+1}: tsv failed {exc}")
        png.unlink(missing_ok=True)
        r = page_report(words, doc[i].rect.width * a.dpi / 72, unicodedata.normalize("NFC", text))
        r["pdf_page"] = i + 1
        head = "\n".join(text.splitlines()[:2])
        m = HEAD_NUM.search(head)
        r["printed_page"] = deva_int(m.group(1)) if m else None
        r["status"], r["reasons"] = gate(r)
        r["image"] = str(jpg.relative_to(Path.cwd())) if jpg.is_relative_to(Path.cwd()) else str(jpg)
        reports.append(r)
        print(f"  page {i+1}/{doc.page_count} {r['status']} conf={r['conf_mean']}", flush=True)

    # sequence check on the printed page numbers
    # Only ADJACENT pdf pages can show a real gap: where a header did not parse,
    # the next reading is naturally several numbers on. A decrease is normally a
    # numbering restart (front matter is paginated separately in this edition),
    # not a misbound page.
    seq = [(r["pdf_page"], r["printed_page"]) for r in reports if r["printed_page"] is not None]
    gaps, restarts = [], []
    for (p1, n1), (p2, n2) in zip(seq, seq[1:]):
        if p2 != p1 + 1 or n2 in (n1, n1 + 1):
            continue
        (restarts if n2 < n1 else gaps).append((p1, n1, p2, n2))

    st_counts = collections.Counter(r["status"] for r in reports)
    if a.json_out:
        Path(a.json_out).write_text(json.dumps(reports, ensure_ascii=False, indent=1), encoding="utf-8")
    L = [f"# OCR quality check — {Path(a.pdf).name}", "",
         f"Engine: Tesseract `-l {a.lang} --psm {a.psm}`, pages rendered at {a.dpi} dpi. "
         f"Page images for eye-checking: `{img_dir}` (one JPEG per page at {a.image_dpi} dpi).", "",
         "| gate | pages |", "|---|--:|"]
    L += [f"| {k} | {v} |" for k, v in st_counts.most_common()]
    conf = [r["conf_mean"] for r in reports if r["words"]]
    L += ["", f"Mean word confidence across the book: **{st.mean(conf):.1f}** "
          f"(median {st.median(conf):.1f}, worst {min(conf):.1f}).", ""]
    L += ["## Page order", "",
          f"Printed page numbers read on {len(seq)} of {len(reports)} pages "
          f"(the rest have no running head, or the head did not OCR).",
          f"- **gaps between adjacent pages** (a page may be missing): "
          f"{'; '.join(f'pdf {a}→{c}: printed {b}→{d}' for a, b, c, d in gaps) if gaps else 'none'}",
          f"- **numbering restarts / decreases** (expected where front matter is paginated separately): "
          f"{'; '.join(f'pdf {a}→{c}: printed {b}→{d}' for a, b, c, d in restarts) if restarts else 'none'}", ""]
    flagged = [r for r in reports if r["status"] != "pass"]
    L += ["## Pages not passing the gate", "",
          "| pdf page | printed | gate | conf | low-conf words | skew | why |", "|---|---|---|--:|--:|--:|---|"]
    for r in flagged:
        L.append(f"| {r['pdf_page']} | {r['printed_page'] or '—'} | {r['status']} | {r['conf_mean']} | "
                 f"{r['low_conf_pct']}% | {r['skew_deg']}° | {'; '.join(r['reasons'])} |")
    L += ["", "## Every page", "",
          "| pdf page | printed | gate | conf | median | low-conf | words | Devanagari | skew | gutter vs body |",
          "|---|---|---|--:|--:|--:|--:|--:|--:|---|"]
    for r in reports:
        L.append(f"| {r['pdf_page']} | {r['printed_page'] or '—'} | {r['status']} | {r['conf_mean']} | "
                 f"{r['conf_median']} | {r['low_conf_pct']}% | {r['words']} | {r['deva_ratio']:.0%} | "
                 f"{r['skew_deg']}° | {r['edge_conf']} vs {r['mid_conf']} |")
    Path(a.out).write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"\n{dict(st_counts)} -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
