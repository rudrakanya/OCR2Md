"""Run a chapter cfg's extra_rules over its run/chN section files (free).  python -I -X utf8 _tools/ch_rules.py ch04/cfg_ch04v3.py"""
import importlib.util, sys
from pathlib import Path
DR = Path(__file__).resolve().parent.parent
s = importlib.util.spec_from_file_location("c", DR / sys.argv[1]); C = importlib.util.module_from_spec(s); s.loader.exec_module(C)
text = "\n\n".join((DR / "run" / f"ch{C.CH}" / f"{x}.md").read_text(encoding="utf-8") for x in C.SECTIONS if (DR / "run" / f"ch{C.CH}" / f"{x}.md").exists())
fails = C.extra_rules(text, {}, {})
for f in fails: print(f)
print(len(fails), "rule failures")
