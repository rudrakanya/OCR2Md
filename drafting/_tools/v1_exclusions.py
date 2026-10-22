"""Seed plan_v2/excl_chNN.tsv from the v1 outline's "Material … not used" lists (free).
Each bullet's IDs (full or abbreviated, with ranges such as "CII-027 to -046" or "KRAM-1-001…-030") get the bullet's
reason text. Only DIRECT items of the unit are written; existing lines in the tsv are kept (manual reasons win).

  python -I -X utf8 drafting/_tools/v1_exclusions.py 04
"""
import json
import re
import sys
from pathlib import Path

DR = Path(__file__).resolve().parent.parent
V1 = (DR / "editorial" / "Chapter_4_to_Afterword_Master_Drafting_Outline.md").read_text(encoding="utf-8")
W = DR / "editorial" / "plan_v2"


def unit_text(n):
    head = "# Afterword." if n == "13" else f"# Chapter {int(n)}."
    a = V1.index("\n" + head)
    m = re.search(r"\n# (Chapter \d+\.|Afterword\.|Part III)", V1[a + 5:])
    return V1[a:a + 5 + m.start()]


def expand(text, unit, known):
    """return the set of IDs named in text (abbreviations resolved against `known`)"""
    out = set()
    code = r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*?"
    for m in re.finditer(rf"(C\d\d-)?({code})-(\d{{3}})((?:\s*(?:,|/|and|to|…|\.\.\.|–|-)\s*-?\d{{3}})*)", text):
        pre = m.group(1) or f"C{unit}-"
        book = m.group(2)
        nums = [int(m.group(3))]
        rest = m.group(4) or ""
        parts = re.findall(r"(to|…|\.\.\.|–|,|/|and)?\s*-?(\d{3})", rest)
        last = nums[0]
        for sep, num in parts:
            v = int(num)
            if sep in ("to", "…", "...", "–"):
                nums += list(range(last + 1, v + 1))
            else:
                nums.append(v)
            last = v
        for v in nums:
            i = f"{pre}{book}-{v:03d}"
            if i in known:
                out.add(i)
    return out


def main():
    n = sys.argv[1]
    rows = [json.loads(l) for l in (DR / "evidence_index" / f"ch{n}.jsonl").open(encoding="utf-8")]
    direct = {r["id"] for r in rows if r["kind"] == "direct"}
    U = unit_text(n)
    m = re.search(r"\n- \*\*(?:Material[^*]*not used|Deliberately not used)[^\n]*\n(.*?)(?=\n- \*\*|\n## |\n# |\Z)", U, re.S)
    if not m:
        print("no not-used list found")
        return
    block = m.group(1)
    bullets = re.split(r"\n\s*- ", "\n" + block)
    W.mkdir(exist_ok=True)
    ef = W / f"excl_ch{n}.tsv"
    have = {}
    if ef.exists():
        for line in ef.read_text(encoding="utf-8").splitlines():
            if "\t" in line:
                have[line.split("\t", 1)[0]] = line
    added = 0
    for b in bullets:
        b = b.strip()
        if not b:
            continue
        ids = expand(b, n, direct)
        reason = re.sub(r"\(?\s*(C\d\d-)?[A-Z][A-Z0-9-]*-\d{3}[^():;]*\)?", "", b)
        reason = re.sub(r"\s+", " ", reason).strip(" :;,.-*")
        reason = (reason[:160] or "v1 outline: not used").replace("\t", " ")
        for i in sorted(ids):
            if i not in have:
                have[i] = f"{i}\tv1: {reason}"
                added += 1
    ef.write_text("# ID<TAB>reason (seeded from the v1 not-used list; edit freely)\n" + "\n".join(have[k] for k in sorted(have)) + "\n", encoding="utf-8")
    print(f"C{n}: {added} exclusions seeded from v1 ({len(have)} in file)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
