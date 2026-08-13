#!/usr/bin/env python3
"""
ocr_layout.py — run Baidu Unlimited-OCR to get LAYOUT-LABELLED source text.

Why this exists
---------------
Every structural label in labels.py is currently inferred from markdown shape,
because the corpus was OCR'd by a text-only model that threw the page geometry
away. Unlimited-OCR (github.com/baidu/Unlimited-OCR, MIT) emits the layout
directly, as `<|det|>type [bbox]<|/det|>` spans over exactly the taxonomy
labels.py already adopts. Re-ingesting through it upgrades every structural
label from a guess to an observation, and nothing downstream has to change.

How to actually run it
----------------------
Measured facts, not assumptions:

  * 3B parameters total, ~500M active per token (sparse), MIT licence.
  * ">=8 GB VRAM is enough for BF16 inference" — a cheap cloud GPU, not an A100.
  * There is **no official hosted API**. Self-hosting is the only path.
  * The reference implementation calls `.cuda()`; the pinned stack is
    torch 2.10 / transformers 4.57.1.

Both routes work here and are measured, not guessed:

  LOCAL CPU   works, after `ocr_cpu_patch.py` rewrites the vendored `.cuda()`
              calls. 322 s per page on 8 cores. Fine for targeted pages
              (inscription plates, tables, one chapter); a 121-page book is
              ~11 hours, so not for bulk.
  GPU SERVER  the vLLM container, >=8 GB VRAM, OpenAI-compatible API. The route
              for re-parsing the whole corpus.

That choice is what makes this module worth having: the SAME client code talks
to a container on your own GPU, a rented GPU, or an HF Inference Endpoint. Point
`UNLIMITED_OCR_URL` at whichever exists.

    python ocr_layout.py --serve-help          # exact commands to stand one up
    python ocr_layout.py --check               # is an endpoint reachable?
    python ocr_layout.py scans/book.pdf --out kb/_layout
    python ocr_layout.py --to-markdown kb/_layout/book.layout.jsonl

Output: one .layout.jsonl per document, a record per page:
    {"page": 1, "raw": "...", "elements": [{"type": "title", "bbox": [...],
     "text": "..."}], "markdown": "..."}
"""
import argparse
import base64
import json
import os
import re
import sys
import time
from pathlib import Path

from labels import STRUCTURAL, parse_det_markers

ENV_URL = "UNLIMITED_OCR_URL"
ENV_KEY = "UNLIMITED_OCR_KEY"
MODEL = os.environ.get("UNLIMITED_OCR_MODEL", "baidu/Unlimited-OCR")

# From the vLLM recipe. These are not decorative:
#   the '<image>' prefix is required by the prompt template;
#   skip_special_tokens=False is mandatory or the <|det|> markers are stripped
#   out of the response — which would silently reduce this to plain OCR;
#   the n-gram window suppresses the repetition loops long documents provoke.
PROMPT_SINGLE = "<image>document parsing."
PROMPT_MULTI = "<image>Multi page parsing."
NGRAM_SIZE = 35
WINDOW_SINGLE = 128
WINDOW_MULTI = 1024

SERVE_HELP = f"""
Unlimited-OCR needs a GPU with >= 8 GB VRAM. Three ways to get one:

1. YOUR OWN GPU (or any box with docker + nvidia runtime)

   docker run --rm --gpus all --network host --ipc host \\
     vllm/vllm-openai:unlimited-ocr \\
     baidu/Unlimited-OCR \\
     --trust-remote-code \\
     --logits_processors vllm.model_executor.models.unlimited_ocr:NGramPerReqLogitsProcessor \\
     --no-enable-prefix-caching \\
     --mm-processor-cache-gb 0

   then:  set {ENV_URL}=http://localhost:8000/v1

2. A RENTED GPU (RunPod / Vast.ai / Lambda — an L4, A10 or T4 is plenty)

   Launch the same container, expose port 8000, then:
     set {ENV_URL}=https://<your-host>:8000/v1
     set {ENV_KEY}=<token if your provider fronts it with auth>

   At ~8 GB VRAM this is the cheapest tier on every provider. The whole
   24-source corpus is a single-digit number of GPU-hours.

3. HUGGING FACE INFERENCE ENDPOINTS

   Deploy baidu/Unlimited-OCR from the model page onto a small GPU instance,
   then point {ENV_URL} at the endpoint's /v1 URL and set {ENV_KEY}.

Whichever you choose, verify with:   python ocr_layout.py --check

NOT RECOMMENDED — local CPU (`--local`):
   3B weights (~6 GB in BF16) fit in this machine's 17 GB RAM, and only ~500M
   parameters activate per token, so it will run. It will also be slow enough
   that re-parsing a 600-page book is not a realistic plan, and the pinned
   stack (torch 2.10 / transformers 4.57.1) does not match what is installed
   here (transformers 5.14.1). Use it for a handful of important pages —
   inscription plates, tables, a figure-heavy chapter — not for the corpus.
   If you do, isolate it:
       python -m venv .venv-ocr && .venv-ocr\\Scripts\\pip install \\
         torch==2.10.0 torchvision==0.25.0 transformers==4.57.1 \\
         pymupdf einops addict easydict
"""


# ---------------------------------------------------------------------------
# Page rendering
# ---------------------------------------------------------------------------

def pdf_to_images(pdf_path, out_dir, dpi=200, first=None, last=None):
    """Render PDF pages to PNG. Needs pymupdf (the project's OCR extra)."""
    try:
        import fitz                                   # pymupdf
    except ImportError as e:
        raise SystemExit("pymupdf is required to rasterise PDFs:\n"
                         "    pip install pymupdf") from e
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    paths = []
    lo = (first or 1) - 1
    hi = min(last or doc.page_count, doc.page_count)
    for i in range(lo, hi):
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=mat)
        p = out_dir / f"{Path(pdf_path).stem}_p{i + 1:04d}.png"
        pix.save(p)
        paths.append((i + 1, p))
    doc.close()
    return paths


def _data_url(path):
    b = Path(path).read_bytes()
    ext = Path(path).suffix.lower().lstrip(".") or "png"
    mime = {"jpg": "jpeg", "tif": "tiff"}.get(ext, ext)
    return f"data:image/{mime};base64," + base64.b64encode(b).decode("ascii")


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

class LayoutClient:
    """Talks to any OpenAI-compatible Unlimited-OCR server (vLLM or SGLang)."""

    def __init__(self, base_url=None, api_key=None, model=None, timeout=3600):
        self.base_url = (base_url or os.environ.get(ENV_URL, "")).rstrip("/")
        if not self.base_url:
            raise SystemExit(
                f"{ENV_URL} is not set — no Unlimited-OCR endpoint to talk to.\n"
                f"Run:  python ocr_layout.py --serve-help")
        self.api_key = api_key or os.environ.get(ENV_KEY) or "EMPTY"
        self.model = model or MODEL
        self.timeout = timeout

    def _post(self, payload, attempts=4):
        import urllib.error
        import urllib.request
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}",
                     "Content-Type": "application/json",
                     "User-Agent": "udaypur-rag/2.0"})
        delay = 4
        for n in range(attempts):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    return json.loads(r.read().decode("utf-8"))
            except urllib.error.HTTPError as e:
                body = e.read()[:300].decode("utf-8", "replace")
                if e.code in (429, 500, 502, 503, 504) and n < attempts - 1:
                    time.sleep(delay); delay *= 2; continue
                raise SystemExit(f"Unlimited-OCR endpoint returned HTTP {e.code}: {body}")
            except Exception as e:                    # noqa: BLE001
                if n < attempts - 1:
                    time.sleep(delay); delay *= 2; continue
                raise SystemExit(f"could not reach {self.base_url}: {e}")

    def parse_page(self, image_path, multi=False, max_tokens=8192):
        """One page -> raw model output, special tokens intact."""
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": PROMPT_MULTI if multi else PROMPT_SINGLE},
                {"type": "image_url", "image_url": {"url": _data_url(image_path)}},
            ]}],
            "max_tokens": max_tokens,
            "temperature": 0.0,
            # Both keys matter. Without skip_special_tokens=False the server
            # strips <|det|> from the response and this becomes ordinary OCR
            # with none of the layout information that justifies the model.
            "skip_special_tokens": False,
            "vllm_xargs": {"ngram_size": NGRAM_SIZE,
                           "window_size": WINDOW_MULTI if multi else WINDOW_SINGLE},
        }
        data = self._post(payload)
        try:
            return data["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError):
            raise SystemExit(f"unexpected response shape: {json.dumps(data)[:300]}")

    def close(self):
        pass

    def check(self):
        """Is the endpoint alive and is it actually serving this model?"""
        import urllib.error
        import urllib.request
        req = urllib.request.Request(
            f"{self.base_url}/models",
            headers={"Authorization": f"Bearer {self.api_key}",
                     "User-Agent": "udaypur-rag/2.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode("utf-8"))
        except Exception as e:                        # noqa: BLE001
            return False, f"unreachable: {e}"
        served = [m.get("id") for m in data.get("data", [])]
        ok = any("unlimited" in (m or "").lower() for m in served)
        return ok, f"serving {served}"


class LocalLayoutClient:
    """Run the model in-process on CPU (or a local GPU). Measured, not assumed.

    This works because of two fixes, both non-obvious:

      1. `infer()` calls `.cuda()` on fourteen tensors and wraps generation in
         `autocast("cuda")`. Nothing needs a GPU — the weights load into 17 GB
         of RAM — but the code refuses without one. `ocr_cpu_patch.py` rewrites
         those calls to honour UNLIMITED_OCR_DEVICE.
      2. The model STREAMS decoded tokens to stdout and returns nothing useful;
         `result.md` on disk holds the plain text with the <|det|> markers
         already stripped. The layout information — the entire reason for using
         this model — exists only in the stream, so it is captured here.

    Measured on this machine (8 cores, bf16, 200 dpi page, max_length 4096):
    weights load 7.5 s warm, and ONE PAGE takes 322 s. That is the number that
    matters: a 121-page book is ~11 hours and the full corpus is weeks, so this
    path is for targeted pages — inscription plates, tables, a chapter whose
    layout matters — and a rented GPU is the answer for bulk work.
    """
    name = "local"

    def __init__(self, device=None, model_name=None, max_length=4096, dtype=None):
        self.device = device or os.environ.get("UNLIMITED_OCR_DEVICE") or "cpu"
        os.environ.setdefault("UNLIMITED_OCR_DEVICE", self.device)
        self.model_name = model_name or MODEL
        self.max_length = max_length
        try:
            import torch
            from transformers import AutoModel, AutoTokenizer
        except ImportError as e:
            raise SystemExit(
                "The local backend needs the pinned stack in its own venv:\n"
                "    python -m venv .venv-ocr\n"
                "    .venv-ocr\\Scripts\\pip install torch==2.10.0 torchvision==0.25.0 "
                "transformers==4.57.1 pymupdf matplotlib einops addict easydict\n"
                "then run this script with .venv-ocr\\Scripts\\python.exe") from e
        torch.set_num_threads(os.cpu_count() or 4)
        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name,
                                                       trust_remote_code=True)
        self.model = AutoModel.from_pretrained(
            self.model_name, trust_remote_code=True, use_safetensors=True,
            dtype=dtype or torch.bfloat16).eval()
        if self.device != "cpu":
            self.model = self.model.to(self.device)

    def parse_page(self, image_path, multi=False, max_tokens=None):
        import contextlib
        import io
        import tempfile
        buf = io.StringIO()
        with tempfile.TemporaryDirectory() as tmp:
            with contextlib.redirect_stdout(buf):
                try:
                    self.model.infer(
                        self.tokenizer,
                        prompt=PROMPT_MULTI if multi else PROMPT_SINGLE,
                        image_file=str(image_path), output_path=tmp,
                        base_size=1024, image_size=640, crop_mode=True,
                        max_length=max_tokens or self.max_length,
                        no_repeat_ngram_size=NGRAM_SIZE,
                        ngram_window=WINDOW_MULTI if multi else WINDOW_SINGLE,
                        save_results=True)
                except Exception as e:                # noqa: BLE001
                    print(f"\n[infer failed: {type(e).__name__}: {e}]")
        raw = buf.getvalue()
        # Strip the progress bars the save step writes into the same stream.
        raw = re.sub(r"^(?:image|other):.*$", "", raw, flags=re.M)
        raw = raw.split("===============save results")[0]
        return raw.strip()

    def check(self):
        return True, f"local {self.model_name} on {self.device}"

    def close(self):
        del self.model


# ---------------------------------------------------------------------------
# Output shaping
# ---------------------------------------------------------------------------

_BBOX_RE = re.compile(r"\[([\d.,\s]+)\]")


def elements_from_raw(raw):
    """Turn one page's raw output into typed elements.

    Falls back to a single `text` element when the response carries no markers,
    which is how a server misconfigured with skip_special_tokens=True shows up.
    """
    spans = parse_det_markers(raw)
    if not spans:
        cleaned = re.sub(r"<\|[^|]*\|>", "", raw).strip()
        return ([{"type": "text", "bbox": None, "text": cleaned}] if cleaned else [])
    out = []
    for typ, bbox, text in spans:
        nums = None
        if bbox:
            m = _BBOX_RE.search(bbox)
            if m:
                try:
                    nums = [float(x) for x in re.split(r"[,\s]+", m.group(1).strip()) if x]
                except ValueError:
                    nums = None
        out.append({"type": typ if typ in STRUCTURAL else "text",
                    "bbox": nums, "text": text.strip()})
    return out


def elements_to_markdown(elements, page=None):
    """Render typed elements back to markdown, preserving the layout as labels.

    Page furniture is dropped rather than emitted, which is the same decision
    md_clean.py makes heuristically — except here it is the model's judgement
    about a region, not a guess from repetition counts.
    """
    lines = []
    if page:
        lines.append(f"<!-- page {page} -->")
    for e in elements:
        t, text = e["type"], (e["text"] or "").strip()
        if not text or t in ("header", "footer", "image", "page_number"):
            continue
        if t == "title":
            lines.append(f"\n## {text}\n")
        elif t == "caption":
            lines.append(f"\n*{text}*\n")
        elif t in ("table", "formula", "list"):
            # Keep verbatim: a reflowed table is a destroyed table. The label is
            # carried in an HTML comment so build_kb can read it without it
            # reaching the embedder.
            lines.append(f"\n<!-- element:{t} -->\n{text}\n")
        else:
            lines.append(text)
    return "\n".join(lines).strip()


def parse_document(client, images, out_path, multi=False, quiet=False):
    """Parse every page of one document; stream results to .layout.jsonl."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out_path.exists():                             # resumable
        for line in out_path.read_text(encoding="utf-8").splitlines():
            try:
                done.add(json.loads(line)["page"])
            except Exception:                          # noqa: BLE001
                pass
    with open(out_path, "a", encoding="utf-8") as fh:
        for page, img in images:
            if page in done:
                continue
            t0 = time.time()
            raw = client.parse_page(img, multi=multi)
            els = elements_from_raw(raw)
            rec = {"page": page, "image": str(img), "raw": raw, "elements": els,
                   "markdown": elements_to_markdown(els, page),
                   "seconds": round(time.time() - t0, 1)}
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fh.flush()
            if not quiet:
                kinds = {}
                for e in els:
                    kinds[e["type"]] = kinds.get(e["type"], 0) + 1
                print(f"  p{page:>4}  {rec['seconds']:5.1f}s  {kinds}", flush=True)
    return out_path


def layout_to_markdown(layout_path, out_path=None):
    """Concatenate a .layout.jsonl into one markdown file for build_kb.py."""
    layout_path = Path(layout_path)
    recs = [json.loads(l) for l in layout_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    recs.sort(key=lambda r: r["page"])
    body = "\n\n".join(r["markdown"] for r in recs if r.get("markdown"))
    out = Path(out_path) if out_path else layout_path.with_suffix("").with_suffix(".md")
    out.write_text(body, encoding="utf-8")
    kinds = {}
    for r in recs:
        for e in r.get("elements", []):
            kinds[e["type"]] = kinds.get(e["type"], 0) + 1
    return out, len(recs), kinds


def main():
    from console import use_utf8
    use_utf8()
    ap = argparse.ArgumentParser(description="Run Unlimited-OCR for layout-labelled text")
    ap.add_argument("inputs", nargs="*", help="PDF or image files")
    ap.add_argument("--out", default="kb/_layout")
    ap.add_argument("--serve-help", action="store_true", help="how to stand up an endpoint")
    ap.add_argument("--check", action="store_true", help="test the configured endpoint")
    ap.add_argument("--to-markdown", help="convert a .layout.jsonl into markdown")
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--first", type=int, help="first page")
    ap.add_argument("--last", type=int, help="last page")
    ap.add_argument("--multi", action="store_true",
                    help="multi-page prompt + wider n-gram window (long PDFs)")
    ap.add_argument("--url", help=f"override ${ENV_URL}")
    ap.add_argument("--local", action="store_true",
                    help="run the model in-process instead of calling a server "
                         "(measured 322s/page on this CPU — targeted pages only)")
    ap.add_argument("--device", default=None, help="--local: cpu | cuda")
    args = ap.parse_args()

    if args.serve_help:
        print(SERVE_HELP); return

    if args.to_markdown:
        out, pages, kinds = layout_to_markdown(args.to_markdown)
        print(f"{pages} page(s) -> {out}")
        print(f"elements: {kinds}")
        print("\nNow re-index it:\n"
              f"    copy \"{out}\" \"Udaypur Reference Markdown Files\\\"\n"
              "    python build_kb.py --force\n"
              "    python label_chunks.py --all")
        return

    if args.check:
        c = LocalLayoutClient(device=args.device) if args.local else LayoutClient(args.url)
        ok, msg = c.check()
        print(f"{c.base_url}\n  {'OK' if ok else 'NOT SERVING Unlimited-OCR'} — {msg}")
        if ok:
            print("  Ready. Parse a document:\n"
                  "    python ocr_layout.py scans/book.pdf --out kb/_layout")
        sys.exit(0 if ok else 1)

    if not args.inputs:
        ap.error("give one or more PDF/image files, or --serve-help / --check")

    client = (LocalLayoutClient(device=args.device) if args.local
              else LayoutClient(args.url))
    outdir = Path(args.out)
    for src in args.inputs:
        src = Path(src)
        if not src.exists():
            print(f"skipping missing {src}", file=sys.stderr); continue
        print(f"\n{src.name}")
        if src.suffix.lower() == ".pdf":
            images = pdf_to_images(src, outdir / "_pages", args.dpi, args.first, args.last)
        else:
            images = [(1, src)]
        target = outdir / f"{src.stem}.layout.jsonl"
        parse_document(client, images, target, multi=args.multi)
        print(f"  -> {target}")
        out, pages, kinds = layout_to_markdown(target)
        print(f"  -> {out}  ({pages} pages, elements {kinds})")


if __name__ == "__main__":
    main()
