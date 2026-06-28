#!/usr/bin/env python3
"""
Samaranganasūtradhāra Verse Extraction Script
==============================================
Automates extraction of Sanskrit verses from scanned PDFs using the Claude API.
Rasterizes each page, sends it to Claude for visual reading, and assembles
the results into Markdown files.

Requirements:
    pip install anthropic pdf2image Pillow

System requirement:
    poppler-utils (for pdftoppm)
    - macOS: brew install poppler
    - Ubuntu/Debian: sudo apt-get install poppler-utils
    - Windows: download from https://github.com/oschwartz10612/poppler-windows

Usage:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python extract_verses.py

    Or pass the key directly:
    python extract_verses.py --api-key "sk-ant-..."

    To resume from a specific file/page:
    python extract_verses.py --resume-file 1 --resume-page 10
"""

import anthropic
import base64
import json
import os
import sys
import time
import argparse
import re
from pathlib import Path
from io import BytesIO

try:
    from pdf2image import convert_from_path
except ImportError:
    print("ERROR: pdf2image not installed. Run: pip install pdf2image Pillow")
    sys.exit(1)


# ─── Configuration ────────────────────────────────────────────────────────────

MODEL = "claude-sonnet-4-6"  # Cost-effective for high-volume; use claude-opus-4-6 for higher accuracy
MAX_TOKENS = 8192
DPI = 200  # Resolution for rasterization; 200 is good balance of quality vs token cost

# Rate limiting
REQUESTS_PER_MINUTE = 30  # Conservative; adjust based on your API tier
DELAY_BETWEEN_REQUESTS = 60.0 / REQUESTS_PER_MINUTE

# File definitions
FILES = [
    {
        "id": 1,
        "pdf": "Samarangan_Vol2_Chapters_55-60.pdf",
        "output": "File1_Ch55-60.md",
        "chapters": {
            55: "The definition of Meru and other sixteen modes of mansions",
            56: "The Illustration of sixty four Prasadas headed by Rucaka",
            57: "A twenty counting of Meru and others",
            58: "The panegyric of palaces",
            59: "The Definition of vimanas amounting sixty four",
            60: "The Definition of Thirty six Prasadas headed by Sri Kuta",
        },
    },
    {
        "id": 2,
        "pdf": "Samarangan_Vol2_Chapters_66-67.pdf",
        "output": "File2_Ch66-67.md",
        "chapters": {
            66: "The Definition of a Mandapa i.e. a Pavilion",
            67: "The definition of 27 pavilions (Mandapas)",
        },
    },
    {
        "id": 3,
        "pdf": "Samarangan_Vol2_Chapters_71-72.pdf",
        "output": "File3_Ch71-72.md",
        "chapters": {
            71: "Cittroddesa — The Painting Art",
            72: "Bhūmibandha — Seasoning of the wall of painting",
        },
    },
]

# ─── System prompt for Claude ─────────────────────────────────────────────────

SYSTEM_PROMPT = r"""You are a Sanskrit scholar and expert document extraction assistant with deep knowledge of IAST transliteration standards.

You are processing a scanned page from **Samaranganasūtradhāra Volume 2** (Mahārājādhirāja Śrī Bhojadeva Paramāra), translated into English by Sudarshan Kumar Sharma.

## CRITICAL: THIS IS A SCANNED BOOK
The OCR text layer is **garbled for Devanagari**. You MUST visually read the page image. Do not rely on any embedded text layer for Devanagari.

## PAGE STRUCTURE
Each page contains:
1. **Devanagari** — the original Sanskrit text in bold Devanagari script
2. **English Translation** — printed directly below each verse in Roman type

There is **no IAST transliteration** in the source. You will generate it yourself.

Verses typically span two lines of Devanagari (one pāda per line). Verse numbers appear as Devanagari numerals within double daṇḍas (e.g. ॥२४॥).

## OUTPUT FORMAT
For EACH verse visible on this page, output EXACTLY this structure:

```
### Verse [CHAPTER].[VERSE_NUMBER]

**Sanskrit (Devanagari):**

[Exact Devanagari as it appears — do not alter]

**IAST Transliteration:**

[Your IAST transliteration of the above]

**English Translation:**

[Exact translation as it appears — do not alter]

> **Footnote [N]:** [footnote text, if any]

---
```

## IAST TRANSLITERATION RULES

| Devanagari | IAST |
|---|---|
| अ आ इ ई उ ऊ | a ā i ī u ū |
| ऋ ॠ ऌ | ṛ ṝ ḷ |
| ए ऐ ओ औ | e ai o au |
| क ख ग घ ङ | k kh g gh ṅ |
| च छ ज झ ञ | c ch j jh ñ |
| ट ठ ड ढ ण | ṭ ṭh ḍ ḍh ṇ |
| त थ द ध न | t th d dh n |
| प फ ब भ म | p ph b bh m |
| य र ल व | y r l v |
| श ष स ह | ś ṣ s h |
| ं | ṃ |
| ः | ḥ |
| ँ | m̐ |

- Preserve sandhi as written.
- Transliterate conjunct consonants correctly.
- Inherent vowel **a** is present unless virāma (्) suppresses it.
- Anusvāra (ं) → always **ṃ**.
- Visarga (ः) → always **ḥ**.
- Daṇḍa (।) and double daṇḍa (॥) → reproduce as-is.
- Convert Devanagari numerals to Arabic in verse labels.

## CONSTRAINTS
1. **Visually read** the page image. OCR is broken for Devanagari.
2. **Devanagari — verbatim.** Do not normalize or correct. Flag unclear as `[UNCLEAR: …]`.
3. **Translation — verbatim.** Do not paraphrase.
4. **IAST — flag uncertainty** with `[IAST UNCERTAIN: …]`.
5. **Preserve `(?)`** marks and **`+++`** marks exactly as they appear.
6. **No commentary.** Only flag genuine ambiguities with `[FLAG: …]`.
7. If a verse starts on a previous page and only the English translation is visible at the top, note `[FLAG: English continuation from previous page]` and include it.
8. If a verse's Devanagari is visible but its English continues on the next page, include the Devanagari and note `[FLAG: English continues on next page]`.
9. If the page contains a CHAPTER heading (e.g. "CHAPTER 56"), output a chapter header line: `# Chapter [N] — [Title]` before the first verse of that chapter.

## CHAPTER TITLES (for reference)
| Ch | Title |
|----|-------|
| 55 | The definition of Meru and other sixteen modes of mansions |
| 56 | The Illustration of sixty four Prasadas headed by Rucaka |
| 57 | A twenty counting of Meru and others |
| 58 | The panegyric of palaces |
| 59 | The Definition of vimanas amounting sixty four |
| 60 | The Definition of Thirty six Prasadas headed by Sri Kuta |
| 66 | The Definition of a Mandapa i.e. a Pavilion |
| 67 | The definition of 27 pavilions (Mandapas) |
| 71 | Cittroddesa — The Painting Art |
| 72 | Bhūmibandha — Seasoning of the wall of painting |

Respond ONLY with the extracted verses in the format above. No preamble, no summary.
"""


# ─── Helper functions ─────────────────────────────────────────────────────────

def rasterize_page(pdf_path: str, page_num: int, dpi: int = DPI) -> str:
    """Rasterize a single PDF page and return base64-encoded JPEG."""
    images = convert_from_path(
        pdf_path,
        first_page=page_num,
        last_page=page_num,
        dpi=dpi,
        fmt="jpeg",
    )
    if not images:
        raise RuntimeError(f"Failed to rasterize page {page_num} of {pdf_path}")

    buf = BytesIO()
    images[0].save(buf, format="JPEG", quality=85)
    return base64.standard_b64encode(buf.getvalue()).decode("utf-8")


def get_page_count(pdf_path: str) -> int:
    """Get total pages in a PDF."""
    from pdf2image.pdf2image import pdfinfo_from_path
    info = pdfinfo_from_path(pdf_path)
    return info["Pages"]


def extract_page(client: anthropic.Anthropic, image_b64: str, page_num: int,
                 book_page: int, context_hint: str = "") -> str:
    """Send a page image to Claude and get verse extraction."""
    user_content = [
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": image_b64,
            },
        },
        {
            "type": "text",
            "text": (
                f"This is book page {book_page} (PDF page {page_num}). "
                f"{context_hint}"
                f"Extract ALL verses visible on this page following the format in your instructions. "
                f"Read the Devanagari visually from the image — do NOT use OCR text."
            ),
        },
    ]

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )

    return response.content[0].text


def detect_book_page(pdf_path: str, page_num: int) -> int | None:
    """Try to detect the book page number from OCR text (top corners)."""
    import subprocess
    result = subprocess.run(
        ["pdftotext", "-f", str(page_num), "-l", str(page_num), pdf_path, "-"],
        capture_output=True, text=True
    )
    text = result.stdout.strip()
    # Look for page numbers (typically at top of page)
    numbers = re.findall(r'^\s*(\d{2,3})\s*$', text, re.MULTILINE)
    if numbers:
        return int(numbers[0])
    # Try first line
    first_lines = text.split('\n')[:3]
    for line in first_lines:
        match = re.search(r'\b(\d{2,3})\b', line)
        if match:
            return int(match.group(1))
    return None


def save_checkpoint(checkpoint_file: str, file_id: int, page_num: int):
    """Save progress checkpoint."""
    with open(checkpoint_file, 'w', encoding="utf-8") as f:
        json.dump({"file_id": file_id, "page_num": page_num}, f)


def load_checkpoint(checkpoint_file: str) -> dict | None:
    """Load progress checkpoint."""
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, encoding="utf-8") as f:
            return json.load(f)
    return None


# ─── Main processing ──────────────────────────────────────────────────────────

def process_file(client: anthropic.Anthropic, file_config: dict,
                 output_dir: str, resume_page: int = 1):
    """Process a single PDF file, extracting all verses."""
    pdf_path = file_config["pdf"]
    output_path = os.path.join(output_dir, file_config["output"])
    checkpoint_file = os.path.join(output_dir, f".checkpoint_file{file_config['id']}.json")

    if not os.path.exists(pdf_path):
        print(f"  ERROR: PDF not found: {pdf_path}")
        print(f"  Please place the PDF in the current directory or provide the full path.")
        return

    total_pages = get_page_count(pdf_path)
    print(f"  Total pages: {total_pages}")

    # Build chapter context hint
    chapters_str = ", ".join(
        f"Ch.{ch}: {title}" for ch, title in file_config["chapters"].items()
    )

    # Open output file (append if resuming, else write fresh)
    mode = 'a' if resume_page > 1 else 'w'
    if mode == 'w':
        # Write file header
        with open(output_path, 'w', encoding="utf-8") as f:
            ch_list = list(file_config["chapters"].keys())
            f.write(f"<!-- Samaranganasūtradhāra Vol.2 — Chapters {ch_list[0]}–{ch_list[-1]} -->\n")
            f.write(f"<!-- Extracted automatically via Claude API -->\n\n")

    errors = []
    for page_num in range(resume_page, total_pages + 1):
        book_page = detect_book_page(pdf_path, page_num)
        bp_str = f" (book p.{book_page})" if book_page else ""

        print(f"  Processing page {page_num}/{total_pages}{bp_str}...", end=" ", flush=True)

        try:
            # Rasterize
            image_b64 = rasterize_page(pdf_path, page_num)

            # Context hint
            context = f"This file covers chapters: {chapters_str}. "

            # Extract
            result = extract_page(
                client, image_b64, page_num, book_page or page_num, context
            )

            # Append to output
            with open(output_path, 'a', encoding="utf-8") as f:
                f.write(result)
                f.write("\n\n")

            # Save checkpoint
            save_checkpoint(checkpoint_file, file_config["id"], page_num + 1)

            print("OK")

        except anthropic.RateLimitError:
            print("RATE LIMITED — waiting 60s...")
            time.sleep(60)
            # Retry this page
            try:
                image_b64 = rasterize_page(pdf_path, page_num)
                context = f"This file covers chapters: {chapters_str}. "
                result = extract_page(client, image_b64, page_num, book_page or page_num, context)
                with open(output_path, 'a', encoding="utf-8") as f:
                    f.write(result)
                    f.write("\n\n")
                save_checkpoint(checkpoint_file, file_config["id"], page_num + 1)
                print("OK (retry)")
            except Exception as e2:
                print(f"FAILED on retry: {e2}")
                errors.append((page_num, str(e2)))

        except anthropic.APIError as e:
            print(f"API ERROR: {e}")
            errors.append((page_num, str(e)))
            time.sleep(5)

        except Exception as e:
            print(f"ERROR: {e}")
            errors.append((page_num, str(e)))

        # Rate limiting delay
        time.sleep(DELAY_BETWEEN_REQUESTS)

    # Append summary table
    with open(output_path, 'a') as f:
        f.write("\n\n## Extraction Summary\n\n")
        f.write("| Chapter | Title | Status |\n")
        f.write("|---------|-------|--------|\n")
        for ch, title in file_config["chapters"].items():
            f.write(f"| {ch} | {title} | Extracted |\n")
        if errors:
            f.write(f"\n**Pages with errors:** {', '.join(str(e[0]) for e in errors)}\n")
            for pg, err in errors:
                f.write(f"- Page {pg}: {err}\n")

    # Clean up checkpoint on completion
    if os.path.exists(checkpoint_file) and not errors:
        os.remove(checkpoint_file)

    print(f"  Output saved to: {output_path}")
    if errors:
        print(f"  WARNING: {len(errors)} pages had errors. Check the summary in the output file.")


def main():
    global MODEL, DPI
    parser = argparse.ArgumentParser(
        description="Extract Sanskrit verses from Samaranganasūtradhāra PDFs using Claude API"
    )
    parser.add_argument("--api-key", help="Anthropic API key (or set ANTHROPIC_API_KEY env var)")
    parser.add_argument("--resume-file", type=int, default=None,
                        help="Resume from file N (1, 2, or 3)")
    parser.add_argument("--resume-page", type=int, default=1,
                        help="Resume from page N within the file")
    parser.add_argument("--output-dir", default="./output",
                        help="Output directory (default: ./output)")
    parser.add_argument("--pdf-dir", default=".",
                        help="Directory containing the PDF files (default: current dir)")
    parser.add_argument("--model", default=MODEL,
                        help=f"Claude model to use (default: {MODEL})")
    parser.add_argument("--dpi", type=int, default=DPI,
                        help=f"DPI for page rasterization (default: {DPI})")
    parser.add_argument("--file", type=int, default=None,
                        help="Process only file N (1, 2, or 3)")
    args = parser.parse_args()

    # API key
    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: No API key provided.")
        print("Set ANTHROPIC_API_KEY environment variable or use --api-key flag.")
        sys.exit(1)

    # Update globals
    MODEL = args.model
    DPI = args.dpi

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Update PDF paths
    for f in FILES:
        f["pdf"] = os.path.join(args.pdf_dir, f["pdf"])

    # Initialize client
    client = anthropic.Anthropic(api_key=api_key)

    # Determine which files to process
    if args.file:
        files_to_process = [f for f in FILES if f["id"] == args.file]
    elif args.resume_file:
        files_to_process = [f for f in FILES if f["id"] >= args.resume_file]
    else:
        files_to_process = FILES

    print("=" * 60)
    print("Samaranganasūtradhāra Verse Extraction")
    print("=" * 60)
    print(f"Model: {MODEL}")
    print(f"DPI: {DPI}")
    print(f"Output: {args.output_dir}")
    print()

    for file_config in files_to_process:
        print(f"\n{'─' * 60}")
        print(f"File {file_config['id']}: {file_config['pdf']}")
        print(f"Chapters: {', '.join(str(ch) for ch in file_config['chapters'])}")
        print(f"{'─' * 60}")

        # Check for checkpoint
        checkpoint_file = os.path.join(args.output_dir, f".checkpoint_file{file_config['id']}.json")
        resume_page = 1

        if args.resume_file == file_config["id"] and args.resume_page > 1:
            resume_page = args.resume_page
        elif os.path.exists(checkpoint_file):
            cp = load_checkpoint(checkpoint_file)
            if cp and cp["file_id"] == file_config["id"]:
                resume_page = cp["page_num"]
                print(f"  Resuming from checkpoint: page {resume_page}")

        process_file(client, file_config, args.output_dir, resume_page)

    print("\n" + "=" * 60)
    print("DONE. Check the output directory for the Markdown files.")
    print("=" * 60)


if __name__ == "__main__":
    main()
