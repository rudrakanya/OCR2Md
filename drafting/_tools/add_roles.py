"""Add evidence IDs to a paragraph's role line in a v2 entry (free).
  python -I -X utf8 drafting/_tools/add_roles.py NN "<paragraph title substring>" ROLE "ID (Tn)[, ID (Tn)]"
The role line is the first '- E:/C:/X:/Note:' line after the paragraph line whose bold title contains the substring."""
import re
import sys
from pathlib import Path

W = Path(__file__).resolve().parent.parent / "editorial" / "plan_v2"
n, key, role, ids = sys.argv[1:5]
f = W / f"ch{n}.md"
lines = f.read_text(encoding="utf-8").split("\n")
hits = [i for i, l in enumerate(lines) if re.match(r"\s+\d+\. \*\*", l) and key in l]
assert len(hits) == 1, f"{key!r}: {len(hits)} matches"
j = hits[0] + 1
while not re.match(r"\s*- (?:E|C|X|Note):", lines[j]):
    j += 1
    assert not re.match(r"\s+\d+\. \*\*|###", lines[j]), "no role line"
line = lines[j]
if re.search(rf"(?:^\s*- | · ){role}: ", line):
    line = re.sub(rf"((?:^\s*- | · ){role}: )", rf"\g<1>{ids}, ", line, count=1)
else:
    line += f" · {role}: {ids}"
lines[j] = line
f.write_text("\n".join(lines), encoding="utf-8")
print(f"ch{n} {key}: {line.strip()[:160]}")
