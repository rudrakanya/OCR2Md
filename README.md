# Document → Markdown (Mistral OCR)

A general-purpose pipeline that converts **any supported document** (PDFs and
images) into high-fidelity Markdown using the Mistral OCR API.

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file with your Mistral API key:

```
MISTRAL_API_KEY=your_key_here
# optional: pin a model (default is mistral-ocr-4)
# MISTRAL_OCR_MODEL=mistral-ocr-4
```

## Usage

```bash
# one file
python ocr_to_markdown.py report.pdf

# several files and/or folders (recurse into subfolders)
python ocr_to_markdown.py a.pdf scan.png "my docs/" --recursive

# choose output location, process N files in parallel
python ocr_to_markdown.py docs/ --recursive --output-dir out --workers 3
```

Outputs are written under `--output-dir` (default `./output/`), **mirroring the
input folder structure**; source files are never modified. Each document becomes
`<name>.md` with `<!-- page N -->` markers; blank / image-only (plate) pages are
explicitly annotated. A run summary and per-file `_ocr_manifest.json` (page
counts, completeness, diacritic/mojibake checks) are written to the output dir.

### Supported inputs
- **PDF** — native or scanned; automatically split into size-bounded page chunks
  (lossless), so very large files work. Encrypted PDFs: pass `--password`.
- **Images** — `.png .jpg .jpeg .webp .gif .bmp .tif .tiff`.
- Other types (e.g. `.docx`, `.pptx`) are **skipped and reported**, never fatal.

### Useful options
| Flag | Purpose |
|------|---------|
| `--output-dir DIR` | Output root (default `output`) |
| `--recursive` | Descend into subdirectories |
| `--include GLOB` / `--exclude GLOB` | Filter files (repeatable) |
| `--model ID` | OCR model (default `mistral-ocr-4`) |
| `--chunk-mb N` / `--page-cap N` | PDF chunk size tuning |
| `--workers N` | Process N files in parallel |
| `--force` | Reprocess even if output is up-to-date |
| `--password PW` | Password for encrypted PDFs |

### Resumability
Completed chunks are cached in `./.ocr_cache/` (keyed by file size+mtime+model),
so interrupted runs resume without re-billing finished work. Delete `.ocr_cache/`
to clear it, or use `--force` to ignore existing outputs.

## Legacy scripts
Earlier, task-specific scripts (Claude-vision Sanskrit verse extraction and the
book-drafting pipeline) live under `legacy/` and are not part of this general
tool.
