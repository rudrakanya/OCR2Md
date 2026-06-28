#!/usr/bin/env python3
"""
Samaranganasūtradhāra Verse Extraction — Message Batches edition
================================================================
Same extraction as extract_verses.py, but runs every page through the
Anthropic Message Batches API (50% cheaper, asynchronous).

Flow:
  1. Rasterize every page of each target PDF to a base64 JPEG (local, free).
  2. Submit ONE batch per file (all submitted up front so they run in parallel).
     Batch IDs are persisted immediately to <output>/.batch_ids.json.
  3. Poll all batches until they finish.
  4. Retrieve results, reassemble in page order, write the three Markdown files.

Re-running is safe: if .batch_ids.json already has a batch for a file, the
script skips submission for that file and goes straight to polling/retrieval —
it never resubmits an already-paid-for batch.

Requirements:
    pip install anthropic pdf2image Pillow
    poppler on PATH (pdftoppm / pdfinfo / pdftotext)

Usage:
    python extract_verses_batch.py --pdf-dir "input files" --output-dir ./output
    python extract_verses_batch.py --file 3 --pdf-dir "input files" --output-dir ./output
"""

import argparse
import json
import os
import sys
import time

import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

# Reuse the configuration and helpers from the streaming script so the prompt,
# model, chapter map and rasterization stay identical.
from extract_verses import (
    FILES,
    SYSTEM_PROMPT,
    MODEL,
    MAX_TOKENS,
    rasterize_page,
    get_page_count,
    detect_book_page,
)

POLL_INTERVAL = 30  # seconds between batch status checks


def custom_id(file_id: int, page_num: int) -> str:
    return f"f{file_id}-p{page_num}"


def parse_custom_id(cid: str) -> tuple[int, int]:
    file_part, page_part = cid.split("-")
    return int(file_part[1:]), int(page_part[1:])


def build_requests_for_file(file_config: dict) -> list[Request]:
    """Rasterize every page and build one batch Request per page."""
    pdf_path = file_config["pdf"]
    fid = file_config["id"]
    total_pages = get_page_count(pdf_path)
    chapters_str = ", ".join(
        f"Ch.{ch}: {title}" for ch, title in file_config["chapters"].items()
    )
    context = f"This file covers chapters: {chapters_str}. "

    requests: list[Request] = []
    for page_num in range(1, total_pages + 1):
        book_page = detect_book_page(pdf_path, page_num) or page_num
        print(f"  [file {fid}] rasterizing page {page_num}/{total_pages}", flush=True)
        image_b64 = rasterize_page(pdf_path, page_num)
        text = (
            f"This is book page {book_page} (PDF page {page_num}). {context}"
            "Extract ALL verses visible on this page following the format in your "
            "instructions. Read the Devanagari visually from the image — do NOT use OCR text."
        )
        requests.append(
            Request(
                custom_id=custom_id(fid, page_num),
                params=MessageCreateParamsNonStreaming(
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    system=SYSTEM_PROMPT,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/jpeg",
                                        "data": image_b64,
                                    },
                                },
                                {"type": "text", "text": text},
                            ],
                        }
                    ],
                ),
            )
        )
    return requests


def load_batch_ids(path: str) -> dict:
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_batch_ids(path: str, ids: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(ids, f, indent=2)


def write_output_file(file_config: dict, results_by_page: dict[int, str],
                      errors: list[str], output_dir: str):
    output_path = os.path.join(output_dir, file_config["output"])
    ch_list = list(file_config["chapters"].keys())
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(
            f"<!-- Samaranganasūtradhāra Vol.2 — Chapters {ch_list[0]}–{ch_list[-1]} -->\n"
        )
        f.write("<!-- Extracted via Claude API (Message Batches) -->\n\n")
        for page_num in sorted(results_by_page):
            f.write(results_by_page[page_num])
            f.write("\n\n")

        f.write("\n\n## Extraction Summary\n\n")
        f.write("| Chapter | Title | Status |\n")
        f.write("|---------|-------|--------|\n")
        for ch, title in file_config["chapters"].items():
            f.write(f"| {ch} | {title} | Extracted |\n")
        if errors:
            f.write(f"\n**Pages with errors:** {len(errors)}\n")
            for e in errors:
                f.write(f"- {e}\n")
    print(f"  Output saved to: {output_path}"
          + (f"  ({len(errors)} page errors)" if errors else ""))


def main():
    parser = argparse.ArgumentParser(
        description="Extract verses via the Anthropic Message Batches API"
    )
    parser.add_argument("--api-key", help="Anthropic API key (or ANTHROPIC_API_KEY env var)")
    parser.add_argument("--output-dir", default="./output")
    parser.add_argument("--pdf-dir", default=".")
    parser.add_argument("--file", type=int, default=None, help="Process only file N (1, 2, or 3)")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: No API key. Set ANTHROPIC_API_KEY or use --api-key.")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    for fc in FILES:
        fc["pdf"] = os.path.join(args.pdf_dir, fc["pdf"])

    files_to_process = [f for f in FILES if (args.file is None or f["id"] == args.file)]

    for fc in files_to_process:
        if not os.path.exists(fc["pdf"]):
            print(f"ERROR: PDF not found: {fc['pdf']}")
            sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    batch_ids_path = os.path.join(args.output_dir, ".batch_ids.json")
    batch_ids = load_batch_ids(batch_ids_path)

    print("=" * 60)
    print("Samaranganasūtradhāra — Batch Extraction")
    print(f"Model: {MODEL}  |  Output: {args.output_dir}")
    print("=" * 60)

    # ── 1 & 2. Submit a batch per file (skip files already submitted) ──
    for fc in files_to_process:
        key = str(fc["id"])
        if key in batch_ids:
            print(f"\nFile {fc['id']}: existing batch {batch_ids[key]} — skipping submission.")
            continue
        print(f"\nFile {fc['id']} ({os.path.basename(fc['pdf'])}): building requests...")
        requests = build_requests_for_file(fc)
        print(f"  Submitting batch with {len(requests)} pages...")
        batch = client.messages.batches.create(requests=requests)
        batch_ids[key] = batch.id
        save_batch_ids(batch_ids_path, batch_ids)  # persist immediately
        print(f"  Batch submitted: {batch.id} (status: {batch.processing_status})")

    # ── 3. Poll until all target batches finish ──
    target_keys = [str(fc["id"]) for fc in files_to_process]
    print("\nWaiting for batches to finish (this can take up to ~1 hour)...")
    while True:
        statuses = {}
        all_done = True
        for key in target_keys:
            b = client.messages.batches.retrieve(batch_ids[key])
            statuses[key] = b.processing_status
            if b.processing_status != "ended":
                all_done = False
        summary = ", ".join(f"file {k}: {v}" for k, v in statuses.items())
        print(f"  [{time.strftime('%H:%M:%S')}] {summary}", flush=True)
        if all_done:
            break
        time.sleep(POLL_INTERVAL)

    # ── 4. Retrieve results and write the markdown files ──
    print("\nAll batches ended. Retrieving results...")
    for fc in files_to_process:
        key = str(fc["id"])
        batch_id = batch_ids[key]
        results_by_page: dict[int, str] = {}
        errors: list[str] = []
        for result in client.messages.batches.results(batch_id):
            _, page_num = parse_custom_id(result.custom_id)
            rtype = result.result.type
            if rtype == "succeeded":
                msg = result.result.message
                text = "".join(b.text for b in msg.content if b.type == "text")
                results_by_page[page_num] = text
            else:
                detail = rtype
                if rtype == "errored":
                    detail = f"errored: {result.result.error.type}"
                errors.append(f"Page {page_num}: {detail}")
                results_by_page[page_num] = f"<!-- Page {page_num} {detail} -->"
        write_output_file(fc, results_by_page, errors, args.output_dir)

    print("\n" + "=" * 60)
    print("DONE.")
    print("=" * 60)


if __name__ == "__main__":
    main()
