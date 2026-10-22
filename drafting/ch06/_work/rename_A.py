"""Worker A: rename C06-KBN-<CODE>-A<NN> to C06-KBN-<CODE>-A-0NN (validator IDs must end in -ddd), in pack_A, kbn_A and 6.1-6.3."""
import json, re
from pathlib import Path
W = Path(__file__).resolve().parent
DR = W.parent.parent
pat = re.compile(r"(C06-KBN-[A-Z0-9-]+?)-A(\d\d)\b")
fix = lambda s: pat.sub(lambda m: f"{m.group(1)}-A-0{m.group(2)}", s)
for p in [W / "pack_A.json", W / "kbn_A.jsonl"] + [DR / "run/ch6" / f"6.{i}.md" for i in (1, 2, 3)]:
    t = p.read_text(encoding="utf-8")
    p.write_text(fix(t), encoding="utf-8")
print("renamed")
