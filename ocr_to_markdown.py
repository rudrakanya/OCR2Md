#!/usr/bin/env python3
"""
ocr_to_markdown.py — general PDF/image -> Markdown via Mistral OCR
=================================================================
A single, configurable tool that turns documents into Markdown using the
Mistral OCR API (default model: mistral-ocr-4). Works for any supported file:

  * PDFs (native or scanned) — split into size-bounded page chunks (lossless
    pypdf splitting), uploaded via the Files API, OCR'd, and reassembled into
    one Markdown file with per-page markers preserving reading order.
  * Images (png/jpg/jpeg/webp/gif/bmp/tif/tiff) — OCR'd directly.
  * Unsupported types (docx, pptx, ...) — skipped and reported, never fatal.

Point it at files and/or folders. Outputs mirror the input layout under an
output directory (default ./output). Resumable via a content-keyed cache in
./.ocr_cache, so re-runs never re-bill completed work. Includes built-in
validation and a JSON run manifest.

Requirements:  pip install -r requirements.txt   (mistralai, python-dotenv, pypdf)
Config:        MISTRAL_API_KEY in .env (or environment).

Examples:
    python ocr_to_markdown.py report.pdf
    python ocr_to_markdown.py scans/ --recursive --output-dir out
    python ocr_to_markdown.py a.pdf b.png "my docs/" --workers 3
    python ocr_to_markdown.py book.pdf --model mistral-ocr-latest --chunk-mb 30
"""

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from dotenv import load_dotenv
from pypdf import PdfReader, PdfWriter
from mistralai.client import Mistral

# Load .env from CWD (searching upward) and from beside this script.
load_dotenv()
load_dotenv(Path(__file__).resolve().parent / ".env", override=False)

PDF_EXTS = {".pdf"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tif", ".tiff"}
IMAGE_MIME = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif", ".bmp": "image/bmp",
    ".tif": "image/tiff", ".tiff": "image/tiff",
}
CACHE_ROOT = Path(".ocr_cache")
EMPTY_NOTE = ("*[No machine-readable text detected on this page — "
              "blank page or full-page plate/illustration in the source.]*")


# ── discovery ──────────────────────────────────────────────────────────────
def discover(inputs, recursive, include, exclude):
    """Yield (root, path) pairs. root is the base used to mirror output layout."""
    import fnmatch
    out = []

    def keep(p: Path):
        name = p.name
        if include and not any(fnmatch.fnmatch(name, g) for g in include):
            return False
        if exclude and any(fnmatch.fnmatch(name, g) for g in exclude):
            return False
        return True

    for item in inputs:
        p = Path(item)
        if p.is_dir():
            it = p.rglob("*") if recursive else p.glob("*")
            for f in sorted(it):
                if f.is_file() and keep(f):
                    out.append((p, f))
        elif p.is_file():
            out.append((p.parent, p))     # mirror relative to the file's own folder
        else:
            print(f"WARNING: not found, skipping: {item}")
    return out


def output_path_for(root: Path, path: Path, output_dir: Path) -> Path:
    rel = path.relative_to(root)
    return (output_dir / rel).with_suffix(".md")


def cache_dir_for(path: Path, model: str, chunk_mb: int, page_cap: int) -> Path:
    st = path.stat()
    key = f"{path.resolve()}|{st.st_size}|{int(st.st_mtime)}|{model}|{chunk_mb}|{page_cap}"
    h = hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]
    d = CACHE_ROOT / f"{path.stem[:40]}-{h}"
    d.mkdir(parents=True, exist_ok=True)
    return d


# ── Mistral OCR calls (with retry) ─────────────────────────────────────────
def _ocr_with_retry(fn, attempts=5, label=""):
    delay = 10
    last = None
    for n in range(1, attempts + 1):
        try:
            return fn()
        except Exception as e:                       # noqa: BLE001 - retry transient API/network errors
            last = e
            print(f"    OCR attempt {n}/{attempts} failed ({label}): "
                  f"{type(e).__name__}: {str(e)[:160]}", flush=True)
            if n < attempts:
                time.sleep(delay)
                delay = min(delay * 2, 120)
    raise last


def ocr_pdf_chunk(client, model, chunk_pdf: Path):
    def _call():
        up = None
        try:
            up = client.files.upload(
                file={"file_name": chunk_pdf.name, "content": chunk_pdf.read_bytes()},
                purpose="ocr",
            )
            signed = client.files.get_signed_url(file_id=up.id, expiry=1)
            resp = client.ocr.process(
                model=model, document={"type": "document_url", "document_url": signed.url})
            return resp.pages
        finally:
            if up is not None:
                try:
                    client.files.delete(file_id=up.id)
                except Exception:
                    pass
    return _ocr_with_retry(_call, label=chunk_pdf.name)


def ocr_image(client, model, path: Path):
    mime = IMAGE_MIME.get(path.suffix.lower(), "image/png")
    b64 = base64.standard_b64encode(path.read_bytes()).decode("utf-8")
    data_url = f"data:{mime};base64,{b64}"
    resp = _ocr_with_retry(
        lambda: client.ocr.process(model=model, document={"type": "image_url", "image_url": data_url}),
        label=path.name,
    )
    return "".join((getattr(p, "markdown", "") or "") for p in (getattr(resp, "pages", []) or []))


# ── per-file processing ────────────────────────────────────────────────────
def open_pdf_reader(path: Path, password: str | None):
    reader = PdfReader(str(path))
    if reader.is_encrypted:
        ok = reader.decrypt(password or "")
        if not ok:
            raise ValueError("encrypted PDF (wrong/no password)")
    return reader


def process_pdf(client, model, path: Path, cache: Path, chunk_mb: int, page_cap: int, password):
    reader = open_pdf_reader(path, password)
    total = len(reader.pages)
    if total == 0:
        raise ValueError("PDF has 0 pages")
    avg = path.stat().st_size / total
    per = min(max(1, int(chunk_mb * 1024 * 1024 / avg)), page_cap)
    chunks = [(lo, min(lo + per, total)) for lo in range(0, total, per)]

    pages_md = {}
    for ci, (lo, hi) in enumerate(chunks):
        part = cache / f"part_{lo:05d}_{hi:05d}.json"
        if part.exists():
            data = json.loads(part.read_text(encoding="utf-8"))
        else:
            chunk_pdf = cache / f"chunk_{lo:05d}_{hi:05d}.pdf"
            w = PdfWriter()
            for i in range(lo, hi):
                w.add_page(reader.pages[i])
            with open(chunk_pdf, "wb") as fh:
                w.write(fh)
            ocr_pages = ocr_pdf_chunk(client, model, chunk_pdf)
            data = {}
            for k, p in enumerate(ocr_pages):
                local = p.index if getattr(p, "index", None) is not None else k
                data[str(lo + local)] = getattr(p, "markdown", "") or ""
            part.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            try:
                chunk_pdf.unlink()
            except OSError:
                pass
        for k, v in data.items():
            pages_md[int(k)] = v
        print(f"    chunk {ci+1}/{len(chunks)} (pages {lo+1}-{hi}) ok", flush=True)
    return total, pages_md


def assemble_pdf_markdown(path: Path, model: str, total: int, pages_md: dict) -> tuple[str, list]:
    lines = [f"<!-- OCR of {path.name} via Mistral {model}; {total} pages -->\n"]
    missing = []
    for gp in range(total):
        lines.append(f"\n\n<!-- page {gp+1} -->\n\n")
        body = pages_md.get(gp, None)
        if body is None:
            missing.append(gp + 1)
            lines.append(f"<!-- page {gp+1}: NOT PROCESSED -->")
        elif not body.strip():
            lines.append(EMPTY_NOTE)
        else:
            lines.append(body)
    return "".join(lines), missing


def validate_text(text: str) -> dict:
    import re
    return {
        "chars": len(text),
        "devanagari": len(re.findall(r"[ऀ-ॿ]", text)),
        "iast": len(re.findall(r"[āīūṛṝḷṃḥṅñṭḍṇśṣĀĪŪ]", text)),
        "mojibake": len(re.findall(r"[ÃÂ][\x80-\xbf]|â€", text)),
    }


_DEVA_RE = re.compile(r"[ऀ-ॿ]")


def transliterate_devanagari(text: str) -> str:
    """Insert an IAST transliteration line beneath every line that contains
    Devanagari (original kept). Requires the optional `indic-transliteration`."""
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate
    out = []
    for ln in text.split("\n"):
        out.append(ln)
        if _DEVA_RE.search(ln):
            out.append("*[IAST] " + transliterate(ln, sanscript.DEVANAGARI, sanscript.IAST).strip() + "*")
    return "\n".join(out)


def process_file(client, model, root: Path, path: Path, output_dir: Path,
                 chunk_mb: int, page_cap: int, force: bool, password,
                 transliterate: bool = False) -> dict:
    ext = path.suffix.lower()
    out = output_path_for(root, path, output_dir)
    res = {"input": str(path), "output": str(out), "type": ext, "status": "", "pages": 0, "missing": []}

    if ext not in PDF_EXTS and ext not in IMAGE_EXTS:
        res["status"] = "skipped:unsupported"
        return res
    if out.exists() and not force and out.stat().st_mtime >= path.stat().st_mtime:
        res["status"] = "skipped:up-to-date"
        return res

    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        if ext in PDF_EXTS:
            cache = cache_dir_for(path, model, chunk_mb, page_cap)
            total, pages_md = process_pdf(client, model, path, cache, chunk_mb, page_cap, password)
            text, missing = assemble_pdf_markdown(path, model, total, pages_md)
            res["pages"], res["missing"] = total, missing
        else:  # image
            md = ocr_image(client, model, path)
            text = f"<!-- OCR of {path.name} via Mistral {model}; image -->\n\n" + (md or EMPTY_NOTE)
            res["pages"] = 1
        if transliterate:
            text = transliterate_devanagari(text)
        out.write_text(text, encoding="utf-8")
        res.update(validate_text(text))
        res["status"] = "ok" if not res["missing"] else "incomplete"
    except Exception as e:                            # noqa: BLE001 - report and continue
        res["status"] = f"error:{type(e).__name__}"
        res["error"] = str(e)[:300]
    return res


# ── main ───────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="General PDF/image -> Markdown via Mistral OCR")
    ap.add_argument("inputs", nargs="+", help="Files and/or directories")
    ap.add_argument("--output-dir", default="output", help="Output root (default: ./output)")
    ap.add_argument("--recursive", action="store_true", help="Descend into subdirectories")
    ap.add_argument("--include", action="append", help="Only files matching this glob (repeatable)")
    ap.add_argument("--exclude", action="append", help="Skip files matching this glob (repeatable)")
    ap.add_argument("--model", default=os.environ.get("MISTRAL_OCR_MODEL", "mistral-ocr-4"))
    ap.add_argument("--chunk-mb", type=int, default=40, help="Target max chunk size in MB (PDFs)")
    ap.add_argument("--page-cap", type=int, default=60, help="Max pages per chunk (PDFs)")
    ap.add_argument("--workers", type=int, default=1, help="Parallel files (default 1)")
    ap.add_argument("--force", action="store_true", help="Reprocess even if output is up-to-date")
    ap.add_argument("--password", default=None, help="Password for encrypted PDFs")
    ap.add_argument("--transliterate", action="store_true",
                    help="Add an IAST transliteration line beneath each Devanagari line "
                         "(needs the 'indic-transliteration' package)")
    args = ap.parse_args()

    key = os.environ.get("MISTRAL_API_KEY")
    if not key:
        print("ERROR: MISTRAL_API_KEY not set (put it in .env or the environment)")
        sys.exit(1)

    if args.transliterate:
        try:
            import indic_transliteration  # noqa: F401
        except ImportError:
            print("ERROR: --transliterate needs the 'indic-transliteration' package.\n"
                  "  Install it with:  pip install indic-transliteration")
            sys.exit(1)

    files = discover(args.inputs, args.recursive, args.include, args.exclude)
    if not files:
        print("No input files found.")
        sys.exit(1)
    output_dir = Path(args.output_dir)
    client = Mistral(api_key=key)

    print("=" * 64)
    print(f"OCR -> Markdown | model={args.model} | {len(files)} file(s) | out={output_dir}")
    print("=" * 64)

    def run(item):
        root, path = item
        print(f"\n• {path}", flush=True)
        r = process_file(client, args.model, root, path, output_dir,
                         args.chunk_mb, args.page_cap, args.force, args.password,
                         args.transliterate)
        print(f"  -> {r['status']} ({r.get('pages', 0)} pg) {r['output']}", flush=True)
        return r

    results = []
    if args.workers > 1:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            for r in as_completed([ex.submit(run, it) for it in files]):
                results.append(r.result())
    else:
        results = [run(it) for it in files]

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "_ocr_manifest.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    print("\n" + "=" * 64)
    print("SUMMARY")
    by = {}
    for r in results:
        by[r["status"]] = by.get(r["status"], 0) + 1
        flag = ""
        if r["status"] in ("ok", "incomplete"):
            flag = (f" | {r.get('devanagari',0)} deva, {r.get('iast',0)} IAST,"
                    f" mojibake={r.get('mojibake',0)}")
            if r.get("missing"):
                flag += f" | MISSING {r['missing']}"
        print(f"  [{r['status']}] {Path(r['input']).name} ({r.get('pages',0)} pg){flag}")
    print("-" * 64)
    print("  totals: " + ", ".join(f"{k}={v}" for k, v in sorted(by.items())))
    print(f"  manifest: {output_dir / '_ocr_manifest.json'}")
    print("=" * 64)


if __name__ == "__main__":
    main()
