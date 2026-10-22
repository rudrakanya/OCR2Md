"""Stitch a chapter's working draft from its section files (free).

  python -I -X utf8 drafting/_tools/stitch.py N [--check]
    N: chapter number; reads the cfg in CFG below, joins run/chN/<sec>.md for cfg.SECTIONS into cfg.OUT.
    --check: only report whether cfg.OUT already equals the joined sections (whitespace-normalised).
"""
import importlib.util
import re
import sys
from pathlib import Path

DR = Path(__file__).resolve().parent.parent
CFG = {1: "ch01/cfg_ch01v6.py", 2: "ch02/cfg_ch02v4.py", 3: "ch03/cfg_ch03v4.py", 4: "ch04/cfg_ch04v3.py",
       5: "ch05/cfg_ch05v1.py", 6: "ch06/cfg_ch06v3.py", 7: "ch07/cfg_ch07v1.py", 8: "ch08/cfg_ch08v1.py", 9: "ch09/cfg_ch09v1.py", 10: "ch10/cfg_ch10v1.py", 11: "ch11/cfg_ch11v1.py", 12: "ch12/cfg_ch12v1.py", 13: "ch13/cfg_ch13v1.py"}


def load(n):
    p = DR / CFG[n]
    s = importlib.util.spec_from_file_location(f"cfg{n}", p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def joined(n, C):
    return "\n\n".join((DR / "run" / f"ch{n}" / f"{sec}.md").read_text(encoding="utf-8").strip() for sec in C.SECTIONS) + "\n"


if __name__ == "__main__":
    n = int(sys.argv[1])
    C = load(n)
    j = joined(n, C)
    norm = lambda x: re.sub(r"\s+", " ", x).strip()
    if "--check" in sys.argv:
        cur = C.OUT.read_text(encoding="utf-8") if C.OUT.exists() else ""
        print(n, C.OUT.name, "equal" if norm(cur) == norm(j) else "DIFFERENT", len(cur), len(j))
    else:
        C.OUT.write_text(j, encoding="utf-8")
        print("wrote", C.OUT, len(j.split()), "words (raw)")
