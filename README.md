# OCR2Md — Document → Markdown (Mistral OCR)

A general-purpose pipeline that converts **any supported document** (PDFs and
images) into high-fidelity Markdown using the [Mistral OCR](https://console.mistral.ai/)
API — preserving headings, tables, footnotes, reading order, and Unicode
(Devanagari, IAST diacritics, etc.).

---

## Quick start

**Prerequisites:** Python **3.10+**, and a Mistral API key (free to create at
<https://console.mistral.ai/> → *API Keys*).

```bash
# 1. Clone
git clone https://github.com/rudrakanya/OCR2Md.git
cd OCR2Md

# 2. (recommended) create & activate a virtual environment
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your API key
cp .env.example .env            # Windows: Copy-Item .env.example .env
# then edit .env and paste your key after MISTRAL_API_KEY=

# 5. Run it
python ocr_to_markdown.py path/to/document.pdf
```

That's it. Your Markdown appears under `./output/`.

> **Note:** `.env` is git-ignored — never commit your API key. Source PDFs,
> outputs, caches, and the bundled `poppler/` are also git-ignored, so a fresh
> clone is small and you bring your own documents.

---

## Usage

```bash
# one file
python ocr_to_markdown.py report.pdf

# several files and/or whole folders (recurse into subfolders)
python ocr_to_markdown.py a.pdf scan.png "my docs/" --recursive

# choose output location, process N files in parallel
python ocr_to_markdown.py docs/ --recursive --output-dir out --workers 3
```

Outputs are written under `--output-dir` (default `./output/`), **mirroring the
input folder structure**; source files are never modified. Each document becomes
`<name>.md` with `<!-- page N -->` markers; blank / image-only (plate) pages are
explicitly annotated. A run summary plus a per-run `_ocr_manifest.json` (page
counts, completeness, diacritic/mojibake checks) are written to the output dir.

### Supported inputs
- **PDF** — native or scanned; automatically split into size-bounded page chunks
  (lossless), so very large files work. Encrypted PDFs: pass `--password`.
- **Images** — `.png .jpg .jpeg .webp .gif .bmp .tif .tiff`.
- Other types (e.g. `.docx`, `.pptx`) are **skipped and reported**, never fatal.

### Options
| Flag | Purpose |
|------|---------|
| `--output-dir DIR` | Output root (default `output`) |
| `--recursive` | Descend into subdirectories |
| `--include GLOB` / `--exclude GLOB` | Filter files (repeatable) |
| `--model ID` | OCR model (default `mistral-ocr-4`) |
| `--chunk-mb N` / `--page-cap N` | PDF chunk-size tuning |
| `--workers N` | Process N files in parallel |
| `--force` | Reprocess even if output is up-to-date |
| `--password PW` | Password for encrypted PDFs |

### Resumability
Completed chunks are cached in `./.ocr_cache/` (keyed by file size + mtime +
model), so interrupted runs resume without re-billing finished work. Delete
`.ocr_cache/` to clear it, or use `--force` to ignore existing outputs.

---

## Troubleshooting

- **`MISTRAL_API_KEY not set`** — you haven't created `.env` (step 4), or it's
  empty. The tool reads `.env` from the current directory or next to the script.
- **`ModuleNotFoundError`** — activate your virtual environment and re-run
  `pip install -r requirements.txt`.
- **A file is `skipped:unsupported`** — only PDFs and the image types above are
  OCR-able; convert other formats to PDF first.
- No internet / API errors are retried automatically with backoff; a single
  file's failure never aborts the batch (see the run summary / manifest).

---

## Project layout

| Path | What it is |
|------|------------|
| `ocr_to_markdown.py` | The OCR → Markdown tool (the thing you run) |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for your `.env` |
| `legacy/` | Older, task-specific scripts (Claude-vision Sanskrit verse extraction and a book-drafting pipeline). **Not** needed for OCR; they have extra dependencies (`anthropic`, `pdf2image`, `Pillow`) and require the `poppler` binary. |

---

## License / data note
You are responsible for the documents you process and for complying with the
copyright of any source material. Outputs and source files stay local (git-ignored).
