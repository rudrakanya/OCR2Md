"""Coverage check for the refined outline (Phase 1, no API calls).
  python -I "drafting/ch01/coverage_check.py"
"""
import collections
import json
import re
import sys
from pathlib import Path

D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "ch01"))
SUBS = {"S1": "Names and identity", "S2": "Location / setting / approach", "S3": "References in texts and records",
        "S4": "Regional memory / legends", "S5": "Significance", "S6": "Historical questions"}


def main():
    pack = {i["id"]: i for i in json.loads((D / "evidence_pack.json").read_text(encoding="utf-8"))}
    text = (D / "ch01_outline_refined.md").read_text(encoding="utf-8")
    sections = re.split(r"\n(?=## 1\.\d)", text)
    used, per_sec = set(), {}
    for s in sections:
        m = re.match(r"## (1\.\d)", s)
        if not m:
            continue
        ids = set(re.findall(r"C\d\d-[A-Z0-9-]+?-\d{3}", s))
        per_sec[m.group(1)] = ids
        used |= ids
    missing = sorted(i for i in used if i not in pack)
    print("IDs in outline:", len(used), "| not in pack:", missing)
    # quoted phrases in the outline must be verbatim in a cited item of the same bullet
    bad = []
    for line in text.splitlines():
        ids = re.findall(r"C\d\d-[A-Z0-9-]+?-\d{3}", line)
        for q in re.findall(r"“([^”]{6,})”|\"([^\"]{6,})\"", line):
            q = q[0] or q[1]
            frag = [f.strip(" .,'") for f in re.split(r"…|\[[^\]]*\]", q) if len(f.strip()) > 4]
            ok = any(all(f in " ".join(pack[i]["quote"].split()) for f in frag) for i in ids if i in pack)
            if ids and not ok:
                bad.append((q[:70], ids[:3]))
    print("quoted phrases not verbatim in a cited item:", len(bad))
    for b in bad:
        print("   ", b)
    # sub-topic coverage
    print("\nSub-topic coverage (items used / available; direct used / direct available):")
    for s, name in SUBS.items():
        av = [i for i in pack.values() if i["sub"] == s]
        u = [i for i in av if i["id"] in used]
        secs = sorted(k for k, v in per_sec.items() if any(i["id"] in v for i in av))
        print(f"  {s} {name}: {len(u)}/{len(av)}; direct {sum(i['strength']=='direct' for i in u)}/"
              f"{sum(i['strength']=='direct' for i in av)}; sections {', '.join(secs)}")
    print("\nPer section:", {k: len(v) for k, v in per_sec.items()})
    unused = [i for i in pack.values() if i["id"] not in used and i["strength"] == "direct"]
    print(f"\nDirect items not used by any section: {len(unused)}")
    for i in unused:
        print(f"  {i['id']} [{i['sub']}] {' '.join(i['quote'].split())[:120]}")
    json.dump({"used": sorted(used), "per_section": {k: sorted(v) for k, v in per_sec.items()},
               "unused_direct": [i["id"] for i in unused]}, open(D / "coverage.json", "w"), indent=1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
