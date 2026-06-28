#!/usr/bin/env python3
"""
Scanned-PDF -> Markdown, via the Anthropic Message Batches API
==============================================================
Page-level recovery edition.

For image-only (scanned) PDFs with no usable text layer. Each page is
rasterized to a JPEG and transcribed to clean Markdown by Claude, in chunked
batches, then reassembled in order into one .md per source PDF.

Robust resume: completion is tracked PER PAGE, not per batch. On every run the
script retrieves all known batches, computes which pages have actually
*succeeded*, and submits only the pages still missing (including pages that
errored inside an otherwise-"ended" batch). Safe to re-run after any failure —
nothing already transcribed is re-submitted, and partial batch failures heal.

State (batch IDs) is in <output>/.book_batch_ids.json, written as each batch
is created. Batch results are retained 29 days, so retrieval is free.

Flags:
    --files 2,3,4     only these file IDs
    --file N          only file N
    --no-submit       retrieve + write what already succeeded; submit nothing
                      (free; use to salvage partial results)

Requires: pip install anthropic pdf2image Pillow ; poppler on PATH.
"""

import argparse
import base64
import json
import os
import sys
import time
from io import BytesIO

import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request
from pdf2image import convert_from_path
from pdf2image.pdf2image import pdfinfo_from_path

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 8192
DPI = 200
CHUNK_SIZE = 100
POLL_INTERVAL = 30

FILES = [
    {"id": 1, "pdf": "Streamflow of the Betwa Rive.pdf", "output": "Betwa_Streamflow.md"},
    {"id": 2, "pdf": "Temple Economics.pdf",             "output": "Temple_Economics.md"},
    {"id": 3, "pdf": "Temples of India.pdf",             "output": "Temples_of_India.md"},
    {"id": 4, "pdf": "The Hindu Temple Vol 2.pdf",       "output": "Hindu_Temple_Vol2.md"},
]

SYSTEM_PROMPT = r"""You are an expert document transcriber. You convert a single scanned page from a scholarly book or journal article into clean, faithful GitHub-Flavored Markdown.

You are given ONE page image. Transcribe all of its textual content.

RULES
- Output ONLY the Markdown transcription of this page. No preamble, no commentary, no surrounding code fences.
- Transcribe verbatim. Do NOT summarize, paraphrase, translate, correct, or add anything.
- Structure faithfully: use #/##/### for headings as they appear; separate paragraphs with blank lines; use - or 1. for lists; use Markdown tables for tabular data.
- Preserve diacritics EXACTLY. These texts use IAST transliteration of Sanskrit — keep marks such as ā ī ū ṛ ṝ ḷ ṃ ḥ ṅ ñ ṭ ḍ ṇ ś ṣ and any others precisely as printed.
- Use *italics* and **bold** only where the source clearly emphasizes text (e.g. italicized Sanskrit terms, bold headings). Do not over-apply.
- Footnotes / endnotes: keep the printed numbers; render the notes as a short list at the end of the page's content (e.g. a line per note: "[^N]: text"). Reference markers in the body may be written inline as [N] or [^N].
- OMIT non-content furniture: repeated running headers/footers (book or chapter title at top/bottom) and the standalone printed page number. Keep genuine content only.
- Figures / plates / photographs: transcribe any caption verbatim and mark the image's place with a line like `*[Figure: <caption>]*` (or `*[Plate ...]*`). Do not otherwise describe the image.
- Multi-column pages: transcribe in natural reading order (full left column, then right column) unless the columns are actually a table.
- Illegible text: mark `[illegible]`. A word you can only partly read: give your best reading followed by `[?]`.
- If the page has NO readable text (blank page, or a full-page image with no caption), output exactly: <!-- no text content -->

Respond with only the Markdown transcription of this page."""


def get_page_count(pdf_path: str) -> int:
    return pdfinfo_from_path(pdf_path)["Pages"]


def rasterize_page(pdf_path: str, page_num: int) -> str:
    images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num, dpi=DPI, fmt="jpeg")
    if not images:
        raise RuntimeError(f"Failed to rasterize page {page_num} of {pdf_path}")
    buf = BytesIO()
    images[0].save(buf, format="JPEG", quality=85)
    return base64.standard_b64encode(buf.getvalue()).decode("utf-8")


def custom_id(fid: int, page: int) -> str:
    return f"f{fid}-p{page}"


def parse_page(cid: str) -> int:
    return int(cid.split("-p")[1])


def build_request(fid: int, page: int, image_b64: str) -> Request:
    return Request(
        custom_id=custom_id(fid, page),
        params=MessageCreateParamsNonStreaming(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_b64}},
                    {"type": "text", "text": "Transcribe this page to clean Markdown following your instructions. Read it visually; the PDF has no usable text layer."},
                ],
            }],
        ),
    )


def load_state(path: str) -> dict:
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_state(path: str, state: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def create_batch_with_retry(client, requests, label="", attempts=6):
    delay = 10
    for i in range(1, attempts + 1):
        try:
            return client.messages.batches.create(requests=requests)
        except anthropic.APIStatusError as e:
            if e.status_code < 500 and not isinstance(e, anthropic.RateLimitError):
                raise
            err = e
        except anthropic.APIConnectionError as e:
            err = e
        if i == attempts:
            raise err
        print(f"    submit {label} failed ({type(err).__name__}); retry {i}/{attempts - 1} in {delay}s", flush=True)
        time.sleep(delay)
        delay = min(delay * 2, 120)


def collect_results(client, batches):
    """Return {page: text} for succeeded pages across all of a file's batches."""
    succeeded = {}
    for b in batches:
        try:
            for result in client.messages.batches.results(b["id"]):
                if result.result.type == "succeeded":
                    page = parse_page(result.custom_id)
                    msg = result.result.message
                    succeeded[page] = "".join(bl.text for bl in msg.content if bl.type == "text").strip()
        except anthropic.APIError as e:
            print(f"    (could not read batch {b['id']}: {type(e).__name__})")
    return succeeded


def chunked(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i + size]


def process_file(client, fc, state, state_path, no_submit):
    fid = str(fc["id"])
    pdf_path = fc["pdf"]
    total = get_page_count(pdf_path)
    entry = state.setdefault(fid, {"pdf": os.path.basename(pdf_path), "pages": total, "batches": []})

    succeeded = collect_results(client, entry["batches"])
    missing = [p for p in range(1, total + 1) if p not in succeeded]
    print(f"  file {fid}: {len(succeeded)}/{total} pages done, {len(missing)} missing")

    new_batch_ids = []
    if missing and not no_submit:
        for chunk in chunked(missing, CHUNK_SIZE):
            lo, hi = chunk[0], chunk[-1]
            print(f"  [file {fid}] rasterizing {len(chunk)} missing pages ({lo}..{hi}) ...", flush=True)
            requests = [build_request(fc["id"], p, rasterize_page(pdf_path, p)) for p in chunk]
            batch = create_batch_with_retry(client, requests, label=f"file {fid} pages {lo}-{hi}")
            entry["batches"].append({"pages": chunk, "id": batch.id})
            save_state(state_path, state)
            new_batch_ids.append(batch.id)
            print(f"  [file {fid}] submitted {len(chunk)} pages -> {batch.id}")
    return new_batch_ids


def write_markdown(client, fc, state, output_dir):
    fid = str(fc["id"])
    entry = state[fid]
    total = entry["pages"]
    succeeded = collect_results(client, entry["batches"])
    missing = [p for p in range(1, total + 1) if p not in succeeded]

    out_path = os.path.join(output_dir, fc["output"])
    title = os.path.splitext(os.path.basename(fc["pdf"]))[0]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"<!-- Markdown transcription of: {os.path.basename(fc['pdf'])} -->\n")
        f.write(f"<!-- {total} pages, transcribed via Claude {MODEL} (Message Batches) -->\n")
        if missing:
            f.write(f"<!-- INCOMPLETE: {len(missing)} page(s) not yet transcribed: "
                    f"{', '.join(map(str, missing))} -->\n")
        f.write(f"\n# {title}\n\n")
        for page in range(1, total + 1):
            f.write(f"<!-- page {page} -->\n\n")
            if page in succeeded:
                body = succeeded[page]
                if body and body != "<!-- no text content -->":
                    f.write(body + "\n\n")
            else:
                f.write("<!-- page not yet transcribed (re-run after adding credits) -->\n\n")
    status = "COMPLETE" if not missing else f"INCOMPLETE ({len(missing)} pages left)"
    print(f"  wrote {out_path}  [{status}]")
    return missing


def main():
    ap = argparse.ArgumentParser(description="Scanned PDF -> Markdown via Message Batches (page-level recovery)")
    ap.add_argument("--api-key")
    ap.add_argument("--pdf-dir", default=".")
    ap.add_argument("--output-dir", default="./output_books")
    ap.add_argument("--file", type=int, default=None)
    ap.add_argument("--files", default=None, help="Comma-separated file IDs, e.g. 2,3,4")
    ap.add_argument("--no-submit", action="store_true", help="Only retrieve + write existing results")
    args = ap.parse_args()

    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: set ANTHROPIC_API_KEY or pass --api-key")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    for fc in FILES:
        fc["pdf"] = os.path.join(args.pdf_dir, fc["pdf"])

    if args.files:
        wanted = {int(x) for x in args.files.split(",")}
        targets = [f for f in FILES if f["id"] in wanted]
    else:
        targets = [f for f in FILES if (args.file is None or f["id"] == args.file)]
    for fc in targets:
        if not os.path.exists(fc["pdf"]):
            print(f"ERROR: missing {fc['pdf']}")
            sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key, max_retries=5)
    state_path = os.path.join(args.output_dir, ".book_batch_ids.json")
    state = load_state(state_path)

    print("=" * 60)
    print(f"PDF -> Markdown  |  model {MODEL}  |  out {args.output_dir}"
          + ("  |  NO-SUBMIT" if args.no_submit else ""))
    print("=" * 60)

    # 1. Submit missing pages per file.
    new_ids = []
    for fc in targets:
        print(f"\nFile {fc['id']}: {os.path.basename(fc['pdf'])}")
        new_ids += process_file(client, fc, state, state_path, args.no_submit)

    # 2. Poll only the batches submitted this run.
    if new_ids:
        print(f"\nPolling {len(new_ids)} new batch(es)...")
        while True:
            statuses = [client.messages.batches.retrieve(bid).processing_status for bid in new_ids]
            ended = sum(1 for s in statuses if s == "ended")
            print(f"  [{time.strftime('%H:%M:%S')}] {ended}/{len(new_ids)} ended", flush=True)
            if ended == len(new_ids):
                break
            time.sleep(POLL_INTERVAL)

    # 3. Write markdown for every target file.
    print("\nWriting markdown...")
    remaining = {}
    for fc in targets:
        miss = write_markdown(client, fc, state, args.output_dir)
        if miss:
            remaining[fc["output"]] = len(miss)

    print("\n" + "=" * 60)
    if remaining:
        print("DONE (with gaps):")
        for name, n in remaining.items():
            print(f"  {name}: {n} page(s) still missing")
    else:
        print("DONE — all target files complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
