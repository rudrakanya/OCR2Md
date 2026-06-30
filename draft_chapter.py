#!/usr/bin/env python3
r"""
draft_chapter.py — retrieval-augmented chapter drafting via Mistral chat.

For each chapter it:
  1. reads that chapter's evidence pack (book/_evidence/chNN.md) made by
     make_evidence.py from the vector knowledge base,
  2. reads a writing-style reference (the OCR'd writing sample, auto-detected),
  3. asks a Mistral chat model to write the chapter in third-person narrative
     history voice, grounded ONLY in the evidence, with numbered endnotes, and
  4. saves it to book/chapter-NN.md.

The chapter titles/scope come from book_outline.py (the single source of truth).

Requires: mistralai, python-dotenv ; MISTRAL_API_KEY in .env.
Prereqs : run build_kb.py then make_evidence.py first.

Usage (VSCode PowerShell):
    python draft_chapter.py 1
    python draft_chapter.py 1 2 3            # several chapters
    python draft_chapter.py all              # every chapter
    python draft_chapter.py 4 --style-file "writing sample ocr\<name>.md"
"""
import argparse
import glob
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from mistralai.client import Mistral

from book_outline import BOOK_TITLE, BOOK_SUBTITLE, CHAPTERS, BY_NUMBER, NUMBERS

load_dotenv()
load_dotenv(Path(__file__).resolve().parent / ".env", override=False)

DEFAULT_MODEL = os.environ.get("MISTRAL_CHAT_MODEL", "mistral-large-latest")
EVID = Path("book/_evidence")
OUT = Path("book")

SYSTEM = (
    "You are a historian writing a chapter of a serious narrative history book. "
    "Write in the THIRD PERSON throughout — never use 'I', 'we', 'us', 'you', no direct address, no diary voice. "
    "Adopt the register and complexity of a serious history book: analytical, contextualizing, attentive to evidence "
    "and scholarly judgement. Carry a rich literary cadence — long, flowing, hypotactic sentences with em-dash asides "
    "and parenthetical qualifications, elevated and exact diction, vivid but restrained imagery, varied with the "
    "occasional short, weighted sentence (evocative, never purple). "
    "Ground EVERY substantive claim in the supplied EVIDENCE only; do not invent dates, names, or quotations; mark "
    "anything you cannot support as '[GAP — not in sources]'; where the evidence disagrees, say so. "
    "Preserve correct IAST diacritics (normalize OCR-style â/î/û to ā/ī/ū). "
    "Use numbered in-text endnote markers [1], [2], … and end with a '## Notes' section citing the real scholarly "
    "works named inside the evidence (authors/titles), never file names. Aim for ~3,500 words; use section subheadings. "
    "Output only the chapter (its title heading, the body with markers, and the ## Notes)."
)


def find_style_file():
    """Locate the OCR'd writing-style sample (.md)."""
    patterns = ["writing sample ocr/*.md", "output/**/*.md", "**/writing sample*/*.md"]
    for pat in patterns:
        for h in sorted(glob.glob(pat, recursive=True)):
            low = h.lower()
            if "manifest" in low:
                continue
            if "writing sample" in low or "whatsapp" in low:
                return h
    return None


def complete_with_retry(client, model, messages, attempts=4):
    delay = 8
    for n in range(1, attempts + 1):
        try:
            resp = client.chat.complete(model=model, messages=messages, max_tokens=8000, temperature=0.4)
            content = (resp.choices[0].message.content or "").strip() if resp.choices else ""
            if not content:
                raise RuntimeError("empty response from model")
            finish = getattr(resp.choices[0], "finish_reason", None)
            return content, finish
        except Exception as e:                       # noqa: BLE001 - retry transient errors
            if n == attempts:
                raise
            print(f"    chat retry {n}/{attempts - 1}: {type(e).__name__}: {str(e)[:120]}", flush=True)
            time.sleep(delay)
            delay = min(delay * 2, 90)


def draft(client, n, style_text, model):
    ch = BY_NUMBER[n]
    pack = EVID / f"ch{n:02d}.md"
    if not pack.exists():
        print(f"  ! missing evidence pack {pack} — run: python make_evidence.py")
        return False
    evidence = pack.read_text(encoding="utf-8")
    user = (
        f"Write Chapter {n} of the book *{BOOK_TITLE}: {BOOK_SUBTITLE}*.\n\n"
        f"CHAPTER TITLE: {ch['title']}\n\nCHAPTER SCOPE: {ch['scope']}\n\n"
        + (f"WRITING-STYLE REFERENCE (match the rhythm and texture of this prose, NOT its first-person voice "
           f"and NOT its subject):\n\"\"\"\n{style_text[:2500]}\n\"\"\"\n\n" if style_text else "")
        + "EVIDENCE (your only source of facts — each block is headed by its source):\n"
        + "\"\"\"\n" + evidence + "\n\"\"\"\n\nNow write the chapter."
    )
    text, finish = complete_with_retry(
        client, model,
        [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
    )
    OUT.mkdir(exist_ok=True)
    (OUT / f"chapter-{n:02d}.md").write_text(text, encoding="utf-8")
    warn = "  ⚠ output may be truncated (hit max_tokens)" if finish == "length" else ""
    print(f"  chapter-{n:02d}.md written ({len(text.split())} words){warn}")
    return True


def main():
    ap = argparse.ArgumentParser(description="Draft book chapter(s) from KB evidence packs (Mistral chat)")
    ap.add_argument("chapters", nargs="+", help=f"chapter numbers {NUMBERS} or 'all'")
    ap.add_argument("--style-file", help="path to the OCR'd writing-sample .md (auto-detected if omitted)")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    args = ap.parse_args()

    key = os.environ.get("MISTRAL_API_KEY")
    if not key:
        print("ERROR: MISTRAL_API_KEY not set (put it in .env)"); sys.exit(1)

    if args.chapters == ["all"]:
        nums = NUMBERS
    else:
        try:
            nums = [int(x) for x in args.chapters]
        except ValueError:
            print("ERROR: chapters must be numbers or 'all'"); sys.exit(1)

    sf = args.style_file or find_style_file()
    style_text = ""
    if sf and Path(sf).exists():
        style_text = Path(sf).read_text(encoding="utf-8")
        print(f"style reference: {sf}")
    else:
        print("style reference: none found — using the built-in voice spec only.\n"
              "  (tip: OCR the 'writing sample ocr' folder with ocr_to_markdown.py, or pass --style-file)")

    client = Mistral(api_key=key)
    ok = 0
    for n in nums:
        if n not in BY_NUMBER:
            print(f"  ! no chapter {n} in book_outline.py"); continue
        print(f"Chapter {n}: {BY_NUMBER[n]['title']}")
        try:
            ok += 1 if draft(client, n, style_text, args.model) else 0
        except Exception as e:                       # noqa: BLE001 - report, continue with next chapter
            print(f"  ! chapter {n} failed: {type(e).__name__}: {str(e)[:160]}")
    print(f"\nDone: {ok}/{len(nums)} chapter(s) written. Next: python assemble_book.py")


if __name__ == "__main__":
    main()
