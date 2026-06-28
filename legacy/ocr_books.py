#!/usr/bin/env python3
"""
High-fidelity PDF -> Markdown via Mistral OCR 4.

For large scanned PDFs. Splits each PDF into size-bounded page-range chunks
(original page content copied losslessly with pypdf), uploads each chunk to the
Mistral Files API, runs OCR (model mistral-ocr-4) on it, and reassembles one
Markdown file per source PDF with per-page markers preserving reading order.

Resumable: each chunk's OCR result is cached as JSON under
<dir>/_ocr_work/<stem>/ ; re-running skips completed chunks (no re-billing).

Validation: compares pages OCR'd against the PDF's page count and reports.

Requires: mistralai, python-dotenv, pypdf, pdf2image (+ poppler on PATH).
MISTRAL_API_KEY in .env.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from pypdf import PdfReader, PdfWriter
from pdf2image.pdf2image import pdfinfo_from_path
from mistralai.client import Mistral

load_dotenv()

MODEL = os.environ.get("MISTRAL_OCR_MODEL", "mistral-ocr-4")
SIZE_BUDGET = 40 * 1024 * 1024   # target max chunk size (under Mistral's ~50MB limit)
PAGE_CAP = 60                    # max pages per chunk
DOCS = [
    "remaining texts/The Hindu Temple Vol 1 Stella Kramrisch.pdf",
    "remaining texts/The Hindu Temple Vol 2.pdf",
]


def page_count(path):
    return pdfinfo_from_path(path)["Pages"]


def chunk_size_for(path, total):
    avg = os.path.getsize(path) / max(total, 1)
    per = max(1, int(SIZE_BUDGET / avg))
    return min(per, PAGE_CAP)


def write_chunk_pdf(reader, lo, hi, out_path):
    w = PdfWriter()
    for i in range(lo, hi):
        w.add_page(reader.pages[i])
    with open(out_path, "wb") as f:
        w.write(f)


def ocr_chunk_with_retry(client, chunk_pdf, attempts=5):
    delay = 10
    last = None
    for n in range(1, attempts + 1):
        up = None
        try:
            with open(chunk_pdf, "rb") as fh:
                up = client.files.upload(
                    file={"file_name": os.path.basename(chunk_pdf), "content": fh.read()},
                    purpose="ocr",
                )
            signed = client.files.get_signed_url(file_id=up.id, expiry=1)
            resp = client.ocr.process(
                model=MODEL,
                document={"type": "document_url", "document_url": signed.url},
            )
            return resp.pages
        except Exception as e:                       # noqa: BLE001 - retry transient API/network errors
            last = e
            print(f"    OCR attempt {n}/{attempts} failed: {type(e).__name__}: {str(e)[:160]}", flush=True)
            if n < attempts:
                time.sleep(delay)
                delay = min(delay * 2, 120)
        finally:
            if up is not None:
                try:
                    client.files.delete(file_id=up.id)
                except Exception:
                    pass
    raise last


def process_pdf(client, pdf_path):
    if not os.path.exists(pdf_path):
        print(f"ERROR: not found: {pdf_path}")
        return None
    total = page_count(pdf_path)
    per = chunk_size_for(pdf_path, total)
    stem = Path(pdf_path).stem
    workdir = os.path.join(os.path.dirname(pdf_path), "_ocr_work", stem)
    os.makedirs(workdir, exist_ok=True)
    chunks = [(lo, min(lo + per, total)) for lo in range(0, total, per)]
    print(f"\n{stem}: {total} pages, {per} pages/chunk -> {len(chunks)} chunks", flush=True)

    reader = PdfReader(pdf_path)
    pages_md = {}                # global 0-based page index -> markdown
    for ci, (lo, hi) in enumerate(chunks):
        part = os.path.join(workdir, f"part_{lo:04d}_{hi:04d}.json")
        if os.path.exists(part):
            data = json.load(open(part, encoding="utf-8"))
            print(f"  chunk {ci+1}/{len(chunks)} pages {lo}-{hi-1}: cached ({len(data)} pages)", flush=True)
        else:
            chunk_pdf = os.path.join(workdir, f"chunk_{lo:04d}_{hi:04d}.pdf")
            write_chunk_pdf(reader, lo, hi, chunk_pdf)
            ocr_pages = ocr_chunk_with_retry(client, chunk_pdf)
            data = {}
            for k, p in enumerate(ocr_pages):
                local = p.index if getattr(p, "index", None) is not None else k
                data[str(lo + local)] = getattr(p, "markdown", "") or ""
            json.dump(data, open(part, "w", encoding="utf-8"), ensure_ascii=False)
            try:
                os.remove(chunk_pdf)
            except OSError:
                pass
            print(f"  chunk {ci+1}/{len(chunks)} pages {lo}-{hi-1}: OCR'd {len(data)} pages", flush=True)
        for k, v in data.items():
            pages_md[int(k)] = v

    out_path = os.path.splitext(pdf_path)[0] + ".md"
    missing = []
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"<!-- OCR of {os.path.basename(pdf_path)} via Mistral {MODEL}; {total} pages -->\n")
        for gp in range(total):
            f.write(f"\n\n<!-- page {gp+1} -->\n\n")
            if gp in pages_md:
                f.write(pages_md[gp])
            else:
                missing.append(gp + 1)
                f.write(f"<!-- page {gp+1}: NOT PROCESSED -->")
    got = len(pages_md)
    print(f"{stem}: {got}/{total} pages OCR'd -> {out_path}"
          + (f"  MISSING: {missing}" if missing else "  (complete)"), flush=True)
    return {"stem": stem, "total": total, "got": got, "out": out_path, "missing": missing}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", type=int, choices=[1, 2], help="Process only volume 1 or 2")
    args = ap.parse_args()
    key = os.environ.get("MISTRAL_API_KEY")
    if not key:
        print("ERROR: MISTRAL_API_KEY not set")
        sys.exit(1)
    client = Mistral(api_key=key)

    docs = DOCS if not args.only else [DOCS[args.only - 1]]
    print("=" * 60)
    print(f"Mistral OCR -> Markdown | model={MODEL}")
    print("=" * 60)
    results = [process_pdf(client, d) for d in docs]

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    for r in results:
        if not r:
            continue
        status = "OK" if not r["missing"] else f"INCOMPLETE ({len(r['missing'])} missing)"
        print(f"  {r['stem']}: {r['got']}/{r['total']} pages [{status}] -> {r['out']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
