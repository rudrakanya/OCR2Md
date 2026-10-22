"""Which packets still need judging? python -I drafting/_tools/packet_status.py [--batches N]

A packet is done when its judgments file passes check_judgments.py. Partial files
(from an interrupted judge) fail the check and are listed as to-do; a new judge
simply overwrites them. Writes drafting/_runs/_packet_status.json.
--batches N  also prints the to-do list split into groups of N packets.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[2]))
R = ROOT / "drafting" / "_runs"


def main():
    idx = json.loads((R / "packets" / "_index.json").read_text(encoding="utf-8"))
    ok, partial, missing = [], [], []
    for p in sorted(idx):
        f = R / "judgments" / f"{p}.jsonl"
        if not f.exists():
            missing.append(p)
            continue
        r = subprocess.run([sys.executable, "-I", str(ROOT / "drafting/_tools/check_judgments.py"), p],
                           capture_output=True, text=True, encoding="utf-8")
        (ok if r.returncode == 0 else partial).append(p)
    todo = partial + missing
    (R / "_packet_status.json").write_text(json.dumps({"ok": ok, "partial": partial, "missing": missing}, indent=0))
    print(f"done {len(ok)} / {len(idx)}; partial {len(partial)}; missing {len(missing)}; to do {len(todo)}")
    if "--batches" in sys.argv:
        n = int(sys.argv[sys.argv.index("--batches") + 1])
        for i in range(0, len(todo), n):
            print(", ".join(todo[i:i + n]))


if __name__ == "__main__":
    main()
