"""Worker D: rename C06-KBN-<CODE>-D<NN> to C06-KBN-<CODE>-D-0NN (validate.ID_RE needs a -NNN tail) in pack_D.json,
kbn_D.jsonl and run/ch6/6.15–6.19.md. Idempotent."""
import re
from pathlib import Path

W = Path(__file__).resolve().parent
DR = W.parent.parent
pat = re.compile(r"(C06-KBN-[A-Z0-9-]+?-D)(\d\d)(?!\d)")
files = [W / "pack_D.json", W / "kbn_D.jsonl"] + [DR / "run" / "ch6" / f"6.{i}.md" for i in range(15, 20)]
for f in files:
    if f.exists():
        t = f.read_text(encoding="utf-8")
        n = pat.sub(lambda m: f"{m.group(1)}-0{m.group(2)}", t)
        if n != t:
            f.write_text(n, encoding="utf-8")
            print("renamed in", f.name)
