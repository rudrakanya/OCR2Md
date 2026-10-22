"""Replace hard-wired repository paths (r"C:\\Users\\User\\Desktop\\Anugrah\\OCR2Md\\...") in the drafting code with
paths computed from each file's own location, so the pipeline runs from any checkout.

  python -I -X utf8 drafting/_tools/make_portable.py            dry run: list files and replacements
  python -I -X utf8 drafting/_tools/make_portable.py --write    rewrite, then verify every file

A literal r"<repo>\\a\\b" in a file k folders below the repo root becomes
    str(Path(__file__).resolve().parents[k] / "a" / "b")
(str() so it works both inside Path(...) and in sys.path.insert(...)). `from pathlib import Path` is added at the top
of a file that lacks it. Verification: each rewritten expression is evaluated with the file's real __file__ and must
equal the old literal on this machine; every file must still compile.
"""
import ast
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OLD = r"C:\Users\User\Desktop\Anugrah\OCR2Md"
LIT = re.compile(r'r(["\'])C:\\Users\\User\\Desktop\\Anugrah\\OCR2Md((?:\\[^"\'\\]+)*)\\?\1')
SKIP = ("vendor", "__pycache__", "_archive", "run_1_failed_2026-10-15")


def files():
    for p in sorted((REPO / "drafting").rglob("*.py")):
        if any(s in p.parts for s in SKIP) or p.name == Path(__file__).name:
            continue
        if OLD in p.read_text(encoding="utf-8", errors="replace"):
            yield p


def expr_for(p, rest):
    k = len(p.relative_to(REPO).parts) - 1          # folders between the repo root and the file
    parts = [x for x in rest.split("\\") if x]
    e = f"Path(__file__).resolve().parents[{k}]"
    for x in parts:
        e += f" / {x!r}".replace("'", '"')
    return f"str({e})", parts


def add_import(src):
    if re.search(r"^from pathlib import (.*\b)?Path\b", src, re.M) or re.search(r"^import pathlib", src, re.M):
        return src
    tree = ast.parse(src)
    line = 0
    if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(getattr(tree.body[0], "value", None), ast.Constant) \
            and isinstance(tree.body[0].value.value, str):
        line = tree.body[0].end_lineno               # after the module docstring
    lines = src.split("\n")
    # keep `from __future__` imports first
    while line < len(lines) and lines[line].startswith("from __future__"):
        line += 1
    lines.insert(line, "from pathlib import Path")
    return "\n".join(lines)


def main(write):
    total = 0
    for p in files():
        src = p.read_text(encoding="utf-8")
        reps = []

        def sub(m):
            e, parts = expr_for(p, m.group(2))
            reps.append((m.group(0), e, Path(OLD, *parts)))
            return e
        new = LIT.sub(sub, src)
        left = new.count(OLD)
        print(f"{p.relative_to(REPO)}: {len(reps)} replaced" + (f", {left} LEFT (not a plain literal)" if left else ""))
        total += len(reps)
        if not write or not reps:
            continue
        new = add_import(new)
        compile(new, str(p), "exec")
        for old, e, want in reps:
            got = Path(eval(e, {"Path": Path, "__file__": str(p)}))
            assert got == want, (p, old, got, want)
        p.write_text(new, encoding="utf-8")
    print("replacements:", total, "(written)" if write else "(dry run)")


if __name__ == "__main__":
    main("--write" in sys.argv)
