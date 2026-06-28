#!/usr/bin/env python3
"""
Mistral OCR -> Markdown
=======================
Extracts a scanned/native PDF or image to Markdown using the Mistral OCR API
(default model: mistral-ocr-4). Reads MISTRAL_API_KEY from .env / environment.

Requirements: pip install mistralai python-dotenv

Usage:
    python mistral_ocr.py "input files/Samarangan_Vol2_Chapters_71-72.pdf"
    python mistral_ocr.py page.png -o page.md
    python mistral_ocr.py doc.pdf --model mistral-ocr-latest
"""

import argparse
import base64
import mimetypes
import os
import sys

from dotenv import load_dotenv
from mistralai.client import Mistral

load_dotenv()


def to_data_url(path: str):
    """Return (mime, data-url) for a local file."""
    mime, _ = mimetypes.guess_type(path)
    if path.lower().endswith(".pdf"):
        mime = "application/pdf"
    if not mime:
        mime = "application/octet-stream"
    with open(path, "rb") as f:
        b64 = base64.standard_b64encode(f.read()).decode("utf-8")
    return mime, f"data:{mime};base64,{b64}"


def ocr_file(client: "Mistral", path: str, model: str):
    mime, data_url = to_data_url(path)
    if mime.startswith("image/"):
        document = {"type": "image_url", "image_url": data_url}
    else:
        document = {"type": "document_url", "document_url": data_url}
    return client.ocr.process(model=model, document=document)


def main():
    ap = argparse.ArgumentParser(description="Mistral OCR -> Markdown")
    ap.add_argument("input", help="PDF or image file")
    ap.add_argument("-o", "--output", help="Output .md (default: <input>.ocr.md)")
    ap.add_argument("--model", default=os.environ.get("MISTRAL_OCR_MODEL", "mistral-ocr-4"),
                    help="OCR model id (default: mistral-ocr-4)")
    args = ap.parse_args()

    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        print("ERROR: MISTRAL_API_KEY not set (put it in .env)")
        sys.exit(1)
    if not os.path.exists(args.input):
        print(f"ERROR: file not found: {args.input}")
        sys.exit(1)

    client = Mistral(api_key=api_key)
    resp = ocr_file(client, args.input, args.model)
    pages = getattr(resp, "pages", []) or []
    md = "\n\n---\n\n".join((getattr(p, "markdown", "") or "") for p in pages)

    out = args.output or (os.path.splitext(args.input)[0] + ".ocr.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"OK: {len(pages)} page(s), model={args.model} -> {out}")


if __name__ == "__main__":
    main()
