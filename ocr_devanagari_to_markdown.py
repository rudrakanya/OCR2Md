#!/usr/bin/env python
"""Convert a scanned Devanagari PDF to markdown with Tesseract (offline).

    python ocr_devanagari_to_markdown.py "book.pdf" -o "out.md"
    python ocr_devanagari_to_markdown.py "book.pdf" -o "out.md" --engine surya

Built for the Patañjala-Yogasūtra with Bhoja's Rājamārtaṇḍa (116 pages,
image-only, CC-0 eGangotri scan, clean and square at ~245 dpi native).

ENGINE CHOICE (measured on p. 27 of that scan, against the page image)
  tesseract -l Devanagari --psm 3, pages rendered at 400 dpi: best of the
  Tesseract configurations, ~3.1 s/page.
      -l san      loses letters:  शीलं → शीं,  प्रकाश → प्रकाल
      -l hin      loses visarga:  साधनपादः → साधनपाद:  and the numerals
      --psm 6     merges the header into the text block
      native dpi  drops lines and mangles the header
  The Devanagari script model keeps conjuncts and visarga; the residual
  errors are letter confusions (व/द, द्वि/ड्रि, दी/री), not dropped text.

RESUMABLE: each page's OCR is cached under <out>.pages/ as page_NNN.txt, so a
killed run resumes and costs only the pages it had not finished. (Two earlier
long jobs on this machine were stopped for low memory.)

QUALITY: OCR of Sanskrit conjuncts is imperfect. Verify any passage against
the page image before quoting it; the page markers below give the PDF page.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

TESS = next((p for p in (r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                         r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe")
             if Path(p).exists()), shutil.which("tesseract"))
TESSDATA = str(Path.home() / "tessdata")

# The digitiser's stamp is printed on every page and is not part of the book.
# OCR mangles it differently each time ("Digitized byeGangotri", "Jangamwadi
# Math र Digltized"), so match on the distinctive words, not the whole phrase.
STAMP = re.compile(r"Jangamwadi|[eE]\s?Gangotri|Digit[il]zed|CC-?0\.|JNANAMANDIR|JAGADGUR", re.I)
DEVA_NUM = "०१२३४५६७८९"
# A sūtra ends with its number after a daṇḍa: "॥ १९ ॥", "॥ १९ ।", "॥२०".
SUTRA_END = re.compile(r"॥\s*[" + DEVA_NUM + r"\d]{1,3}\s*[॥।]?\s*$")
# Running header: "साधनपादः  [२७]" — the pāda name and the printed page number.
RUNNING_HEAD = re.compile(r"^\s*[\[\(]?\s*[" + DEVA_NUM + r"\d]{1,4}\s*[\]\)]?\s*$")
#   recto: "साधनपादः  [२७]"      verso: "[३६]  पातञ्जलयोगसूत्र-भोजवृत्तिः"
PAGE_HEAD = re.compile(
    r"^(?P<name>[ऀ-ॿ\s\-:]{0,32}?)\s*[\[\(]\s*(?P<num>[" + DEVA_NUM + r"\d]{1,4})\s*[\]\)]\s*$"
    r"|^\s*[\[\(]\s*(?P<num2>[" + DEVA_NUM + r"\d]{1,4})\s*[\]\)]\s*(?P<name2>[ऀ-ॿ\s\-:।]{0,40})$")


def ocr_page_tesseract(png: Path, lang: str, psm: str) -> str:
    out = png.with_suffix("")
    subprocess.run([TESS, str(png), str(out), "-l", lang, "--psm", psm,
                    "--tessdata-dir", TESSDATA, "-c", "preserve_interword_spaces=1"],
                   check=True, capture_output=True)
    txt = out.with_suffix(".txt")
    s = txt.read_text(encoding="utf-8", errors="replace")
    txt.unlink(missing_ok=True)
    return s


def clean_page(raw: str) -> list[str]:
    """Drop the digitiser stamp and OCR noise; keep real lines."""
    lines = []
    for ln in raw.splitlines():
        ln = unicodedata.normalize("NFC", ln).rstrip()
        if not ln.strip() or STAMP.search(ln):
            continue
        letters = sum(1 for ch in ln if ch.isalpha())
        # noise rows from rules and page edges: "ss :", "----| स", "re ne"
        if letters < 3 and not RUNNING_HEAD.match(ln):
            continue
        if letters and sum(1 for ch in ln if "\u0900" <= ch <= "\u097F") / max(1, letters) < 0.35 and letters < 12:
            continue
        lines.append(re.sub(r"[ \t]{2,}", "  ", ln.strip()))
    return lines


def printed_page(lines: list[str]):
    """Pull the running header off the top of the page: it is the printed page
    number and the pāda name, not part of the text."""
    for i, ln in enumerate(lines[:2]):
        m = PAGE_HEAD.match(ln)
        if m:
            num = m.group("num") or m.group("num2")
            name = (m.group("name") or m.group("name2") or "").strip(" :-।")
            return lines[:i] + lines[i + 1:], num, name
    return lines, None, ""


def to_markdown(lines: list[str]) -> list[str]:
    """Wrapped Devanagari lines have no hyphens, so join a run of lines into a
    paragraph and break where the text closes with a daṇḍa. Sūtra lines (which
    end in their number between daṇḍas) become headings."""
    out, buf = [], []

    def flush():
        if buf:
            out.append(" ".join(buf))
            out.append("")
            buf.clear()

    for ln in lines:
        if SUTRA_END.search(ln):
            buf.append(ln)
            para = " ".join(buf)
            buf.clear()
            out += [f"### {para}", ""] if len(para) < 200 else [para, ""]
            continue
        buf.append(ln)
        if ln.endswith("।।") or ln.endswith("॥"):
            flush()
    flush()
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--dpi", type=int, default=400)
    ap.add_argument("--lang", default="Devanagari")
    ap.add_argument("--psm", default="3")
    ap.add_argument("--engine", choices=["tesseract", "surya"], default="tesseract")
    ap.add_argument("--title", default=None)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--cache-dir", default=None, help="where per-page OCR is cached (default ./ocr_cache)")
    ap.add_argument("--qc", default=None, help="qc json from ocr_qc.py; stamps each page marker with its gate")
    a = ap.parse_args(argv)

    import pymupdf
    src, out = Path(a.pdf), Path(a.out)
    # Kept OUTSIDE the output folder: the reference folder is corpus input for
    # the KB build, and per-page .txt files there would be picked up as sources.
    cache = Path(a.cache_dir or (Path(__file__).resolve().parent / "ocr_cache")) / (out.stem + ".pages")
    cache.mkdir(parents=True, exist_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(str(src))
    n = min(doc.page_count, (a.start + a.limit) if a.limit else doc.page_count)
    title = a.title or src.stem

    surya = None
    if a.engine == "surya":
        from surya.foundation import FoundationPredictor          # noqa: E402
        from surya.recognition import RecognitionPredictor        # noqa: E402
        from surya.detection import DetectionPredictor            # noqa: E402
        surya = (RecognitionPredictor(FoundationPredictor()), DetectionPredictor())

    qc = {}
    if a.qc:
        qc = {r["pdf_page"]: r for r in json.loads(Path(a.qc).read_text(encoding="utf-8"))}

    t0, done = time.time(), 0
    for i in range(a.start, n):
        cached = cache / f"page_{i + 1:03d}.txt"
        if cached.exists():
            continue
        png = cache / f"_page_{i + 1:03d}.png"
        doc[i].get_pixmap(dpi=a.dpi).save(str(png))
        try:
            if surya:
                from PIL import Image
                rec, det = surya
                pred = rec([Image.open(png)], det_predictor=det)[0]
                text = "\n".join(l.text for l in pred.text_lines)
            else:
                text = ocr_page_tesseract(png, a.lang, a.psm)
        except Exception as exc:                       # keep going; record the gap
            text = f"*[OCR failed on this page: {exc}]*"
        cached.write_text(text, encoding="utf-8")
        png.unlink(missing_ok=True)
        done += 1
        rate = (time.time() - t0) / done
        print(f"  page {i + 1}/{n}  {rate:.1f}s/page  eta {rate * (n - i - 1) / 60:.1f} min", flush=True)

    engine_note = (f"Tesseract {a.lang} --psm {a.psm}, pages rendered at {a.dpi} dpi"
                   if a.engine == "tesseract" else "Surya OCR")
    body = [
        f"<!-- OCR of {src.name} via {engine_note}; {n - a.start} pages. -->",
        "<!-- SOURCE: CC-0 scan, Jangamwadi Math Collection, digitized by eGangotri. "
        "The digitiser's footer stamp is stripped from every page. -->",
        "<!-- Page markers carry the gate from OCR_QC_*.md. 'printed page' is itself OCR-read and a "
        "numeral can be misread: pdf p. 64 prints [३०] and was read as [२०]. The pdf page is authoritative. -->",
        "<!-- QUALITY WARNING: Devanagari OCR of Sanskrit conjuncts is imperfect. Measured on "
        "p. 27, most lines are exact but letter confusions occur (व/द, द्वि/ड्रि, दी/री). "
        "Check any passage against the page image before quoting it; the page markers give the "
        "PDF page number. -->",
        "",
        f"# {title}",
        "",
    ]
    for i in range(a.start, n):
        cached = cache / f"page_{i + 1:03d}.txt"
        if not cached.exists():
            continue
        lines, printed, pada = printed_page(clean_page(cached.read_text(encoding="utf-8")))
        q = qc.get(i + 1, {})
        marker = f"<!-- page {i + 1}"
        if printed or q.get("printed_page"):
            marker += f" | printed page {printed or q['printed_page']}"
        if pada:
            marker += f" | {pada}"
        if q:
            marker += f" | gate: {q['status']}"
            if q["status"] != "pass":
                marker += f" ({'; '.join(q['reasons'])})"
            marker += f" | ocr confidence {q['conf_mean']}"
        body += [marker + " -->", ""]
        if q.get("status") == "illegible":
            body += ["*[illegible — not recovered; see the page image]*", ""]
            continue
        body += to_markdown(lines)
    out.write_text("\n".join(body).rstrip() + "\n", encoding="utf-8")
    words = len(" ".join(body).split())
    print(f"\nwrote {out}  ({n - a.start} pages, {words:,} words, {time.time() - t0:.0f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
