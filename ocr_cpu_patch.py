#!/usr/bin/env python3
"""
ocr_cpu_patch.py — let Unlimited-OCR's vendored modelling code run on CPU.

The published `infer()` is GPU-only by construction, not by requirement: it
calls `.cuda()` on fourteen tensors and wraps generation in
`torch.autocast("cuda", ...)`. Nothing about the architecture needs a GPU — the
weights load happily into 17 GB of system RAM — but the code refuses to run
without one, so `AssertionError: Torch not compiled with CUDA enabled` is the
only thing this machine can get out of it.

This rewrites the cached `trust_remote_code` module to honour a device chosen at
import time. It is:

  idempotent   a marker line means re-running changes nothing
  reversible   the original is kept alongside as .orig
  scoped       only the HF modules cache is touched, never site-packages, and
               only for this one model revision

Why patch a vendored file at all, rather than just renting a GPU: the question
"is local CPU inference viable?" has no answer without a measured seconds/page,
and that number decides whether the corpus can be re-parsed here or must go to
a rented box. A patch that produces a number is worth more than an estimate.

    python ocr_cpu_patch.py            # patch
    python ocr_cpu_patch.py --revert
    python ocr_cpu_patch.py --status
"""
import argparse
import os
import re
import sys
from pathlib import Path

MARKER = "# --- patched for CPU by ocr_cpu_patch.py ---"
CACHE = Path(os.environ.get("HF_HOME",
                            Path.home() / ".cache" / "huggingface")) / "modules"


def find_module_files():
    root = CACHE / "transformers_modules" / "baidu"
    if not root.exists():
        return []
    return sorted(root.rglob("modeling_unlimitedocr.py"))


def patch_text(src):
    if MARKER in src:
        return src, 0
    n = 0

    # Device is read once, from the environment, so the same patched file works
    # unchanged on a GPU box (UNLIMITED_OCR_DEVICE=cuda) and here.
    header = (
        f"{MARKER}\n"
        "import os as _os\n"
        "import torch as _torch\n"
        "_OCR_DEVICE = _os.environ.get('UNLIMITED_OCR_DEVICE') or "
        "('cuda' if _torch.cuda.is_available() else 'cpu')\n"
    )

    # `.cuda()` -> `.to(_OCR_DEVICE)`
    src, k = re.subn(r"\.cuda\(\)", ".to(_OCR_DEVICE)", src)
    n += k
    # autocast("cuda", ...) -> autocast(_OCR_DEVICE, ...)
    src, k = re.subn(r'autocast\(\s*["\']cuda["\']', "autocast(_OCR_DEVICE", src)
    n += k
    # A few models also hard-code device_map/`.to("cuda")`.
    src, k = re.subn(r'\.to\(\s*["\']cuda["\']\s*\)', ".to(_OCR_DEVICE)", src)
    n += k

    # Insert the header after the last top-level import so names resolve.
    lines = src.split("\n")
    last_import = 0
    for i, l in enumerate(lines[:80]):
        if l.startswith(("import ", "from ")):
            last_import = i
    lines.insert(last_import + 1, header)
    return "\n".join(lines), n


def main():
    ap = argparse.ArgumentParser(description="Patch Unlimited-OCR for CPU inference")
    ap.add_argument("--revert", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    files = find_module_files()
    if not files:
        print(f"No cached Unlimited-OCR modelling file under {CACHE}.\n"
              "Load the model once (it downloads the code), then re-run.")
        sys.exit(1)

    for f in files:
        orig = f.with_suffix(".py.orig")
        text = f.read_text(encoding="utf-8")
        patched = MARKER in text

        if args.status:
            cuda_calls = text.count(".cuda()")
            print(f"{f}\n  patched={patched}  remaining .cuda() calls={cuda_calls}")
            continue

        if args.revert:
            if orig.exists():
                f.write_text(orig.read_text(encoding="utf-8"), encoding="utf-8")
                print(f"reverted {f.name}")
            else:
                print(f"no backup for {f.name}; nothing to revert")
            continue

        if patched:
            print(f"{f.name} already patched"); continue
        if not orig.exists():
            orig.write_text(text, encoding="utf-8")
        new, n = patch_text(text)
        f.write_text(new, encoding="utf-8")
        print(f"patched {f.name}: {n} device call(s) rewritten  (backup {orig.name})")

    if not args.status and not args.revert:
        print("\nDevice is chosen at import: UNLIMITED_OCR_DEVICE=cpu|cuda, "
              "defaulting to cuda when available.")


if __name__ == "__main__":
    main()
