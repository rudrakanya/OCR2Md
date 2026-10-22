"""Coverage audit for the master outline v2 (free; no API).

Every DIRECT item of a unit gets exactly one status:
  assigned         cited in this unit's v2 entry (role E/C/X/Note recorded; the strongest role wins)
  cross-reference  not cited here, but cited in another unit's v2 entry, or in a delivered Ch 1-4 section (run/chN/)
  excluded         listed in plan_v2/excl_chNN.tsv (ID<TAB>reason), or matched by an automatic rule below
  UNREASONED       none of the above (must be zero before the unit is saved)

Automatic exclusion rules (each states its reason):
  - book TEMPLE-ECON: excluded source (its "Udaipur" is in Rajasthan)
  - JAGTA-HI item whose page also carries a JAGTA-EN item of the same unit that is assigned or cross-referenced:
    "Hindi original of the English rendering used (EN items …)"
  - near-duplicate (token Jaccard >= 0.75) of an item of the same unit that is assigned or cross-referenced

  python -I -X utf8 drafting/_tools/coverage_v2.py 04 [--list]      writes plan_v2/coverage_ch04.json (+ prints summary)
"""
import os
import collections
import json
import re
import sys
from pathlib import Path

DR = Path(__file__).resolve().parent.parent
W = DR / "editorial" / os.environ.get("UDAY_OUTLINE_DIR", "plan_v2")   
ID = re.compile(r"\bC\d\d-[A-Z0-9]+(?:-[A-Z0-9]+)*?-\d{3}\b")
ROLE_RANK = {"E": 0, "C": 1, "X": 2, "Note": 3}


def load(n):
    return [json.loads(l) for l in (DR / "evidence_index" / f"ch{n}.jsonl").open(encoding="utf-8")]


def roles_in(text):
    """map ID -> best role from '- E: … · C: … · X: … · Note: …' lines"""
    out = {}
    for line in text.split("\n"):
        s = line.strip().lstrip(">").strip()
        if not re.match(r"^-?\s*(E|C|X|Note)\s*:", s):
            continue
        for part in re.split(r" · ", s.lstrip("- ")):
            m = re.match(r"^(E|C|X|Note)\s*:\s*(.*)$", part.strip())
            if not m:
                continue
            for i in ID.findall(m.group(2)):
                r = m.group(1)
                if i not in out or ROLE_RANK[r] < ROLE_RANK[out[i]]:
                    out[i] = r
    return out


def toks(s):
    return set(re.findall(r"\w{4,}", s.lower()))


def main():
    n = sys.argv[1]
    entry = (W / f"ch{n}.md").read_text(encoding="utf-8")
    here = roles_in(entry)
    elsewhere = {}
    for f in W.glob("ch*.md"):
        if f.stem != f"ch{n}" and re.match(r"ch\d\d$", f.stem):
            for i in roles_in(f.read_text(encoding="utf-8")):
                elsewhere.setdefault(i, f.stem)
    for f in (DR / "run").glob("ch[1-4]/[0-9].[0-9].md"):
        for i in ID.findall(f.read_text(encoding="utf-8")):
            elsewhere.setdefault(i, "delivered " + f.stem)
    excl = {}
    ef = W / f"excl_ch{n}.tsv"
    if ef.exists():
        for line in ef.read_text(encoding="utf-8").splitlines():
            if "\t" in line and not line.startswith("#"):
                i, r = line.split("\t", 1)
                excl[i.strip()] = r.strip()
    rows = load(n)
    direct = [r for r in rows if r["kind"] == "direct"]
    used = {r["id"] for r in direct if r["id"] in here or r["id"] in elsewhere}
    en_by_page = collections.defaultdict(list)
    for r in direct:
        if r["book_code"] == "JAGTA-EN" and r["id"] in used:
            pg = re.sub(r"[^\d]", "", r["page"].split("(")[0])
            en_by_page[pg].append(r["id"])
    used_rows = [r for r in direct if r["id"] in used]
    status = {}
    for r in direct:
        i = r["id"]
        if i in here:
            status[i] = ("assigned", here[i])
        elif i in elsewhere:
            status[i] = ("cross-reference", elsewhere[i])
        elif i in excl:
            status[i] = ("excluded", excl[i])
        elif r["book_code"] == "TEMPLE-ECON":
            status[i] = ("excluded", "excluded source: Temple Economics (its Udaipur is in Rajasthan)")
        else:
            pg = re.sub(r"[^\d]", "", r["page"].split("(")[0])
            if r["book_code"] == "JAGTA-HI" and en_by_page.get(pg):
                status[i] = ("excluded", "Hindi original; the English rendering of the same page is used (" + ", ".join(en_by_page[pg][:3]) + ")")
                continue
            t = toks(r["quote"])
            dup = None
            for u in used_rows:
                tu = toks(u["quote"])
                if t and tu and len(t & tu) / len(t | tu) >= 0.75:
                    dup = u["id"]
                    break
            status[i] = ("excluded", f"near-duplicate of {dup}") if dup else ("UNREASONED", "")
    by_sub = collections.defaultdict(collections.Counter)
    for r in direct:
        by_sub[r.get("sub")][status[r["id"]][0]] += 1
    tot = collections.Counter(s[0] for s in status.values())
    res = {"unit": n, "direct": len(direct), "totals": dict(tot),
           "by_sub": {k: dict(v) for k, v in sorted(by_sub.items(), key=lambda x: str(x[0]))},
           "status": {k: list(v) for k, v in status.items()},
           "contextual_cited": sum(1 for r in rows if r["kind"] == "contextual" and r["id"] in here)}
    (W / f"coverage_ch{n}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"C{n}: direct {len(direct)} -> {dict(tot)}; contextual cited {res['contextual_cited']}")
    if "--list" in sys.argv:
        for r in direct:
            if status[r["id"]][0] == "UNREASONED":
                print(" ", r["id"], r["sub"], r["page"], "|", re.sub(r"\s+", " ", r["quote"])[:140])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
