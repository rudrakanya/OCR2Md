"""Worker B, batch 2: Tiwari's English renderings of the praśasti verses, and CII context slices (free)."""
import subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent / "kbn_local.py"
S = [
 ("CII", 6812, "The inscription is a prasasti, a laudatory account, as shown by the use of this word in its v. 60.", "in whose reign the record was set up."),
 ("CII", 7710, "The date of the record", "21st September, 1161 A.C."),
]
for ln in (1544, 1552, 1560, 1570, 1580, 1588, 1596, 1604, 1630, 1640, 1648, 1656, 1664, 1676, 1684, 1692, 1700, 1712, 1720):
    S.append(("JAGTA-EN", ln, None, None))
for code, line, a, b in S:
    args = [sys.executable, "-I", "-X", "utf8", str(H), "B", code, str(line)] + ([a, b] if a else [])
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
    print(line, (r.stdout.strip() or r.stderr.strip()[-200:])[:170])
