"""Validate judgment files: python -I drafting/_tools/check_judgments.py P0001 [P0002 ...] | --all

Checks: every chunk of the packet judged exactly once; ids resolve; spans within the
chunk's numbered sentences; unit/sub valid; strength/type valid; keep => items;
Temple Economics items contextual; no C01 items for pilot-judged chunks; xref units valid.
Prints OK or the problems. Exit code 1 on any problem.
"""
import json
import sys
from pathlib import Path

RUNS = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "_runs"))
TYPES = {"quote", "excerpt", "fact", "figure", "date", "inscription", "architectural detail"}


def load():
    idx = json.loads((RUNS / "packets" / "_index.json").read_text(encoding="utf-8"))
    nsent = {}
    for l in (RUNS / "packets" / "_sentences.jsonl").open(encoding="utf-8"):
        r = json.loads(l)
        nsent[r["chunk_id"]] = len(r["spans"])
    units = json.loads((RUNS / "units.json").read_text(encoding="utf-8"))
    pilot = {json.loads(l)["chunk_id"] for l in (RUNS / "C01_judgments.jsonl").open(encoding="utf-8")}
    src = {}
    for l in (RUNS / "candidates.jsonl").open(encoding="utf-8"):
        r = json.loads(l)
        src[r["chunk_id"]] = r["source_path"]
    return idx, nsent, units, pilot, src


def check(pid, idx, nsent, units, pilot, src):
    probs = []
    f = RUNS / "judgments" / f"{pid}.jsonl"
    if not f.exists():
        return [f"{pid}: no judgments file"]
    ids = idx[pid]
    seen = {}
    for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except Exception as e:
            probs.append(f"line {n}: bad JSON ({e})")
            continue
        m = [c for c in ids if c.startswith(str(r.get("c", "")))] if len(str(r.get("c", ""))) >= 8 else []
        if len(m) != 1:
            probs.append(f"line {n}: id {r.get('c')!r} matches {len(m)} chunks in {pid}")
            continue
        cid = m[0]
        if cid in seen:
            probs.append(f"line {n}: {cid[:10]} judged twice")
        seen[cid] = r
        items = r.get("items") or []
        if r.get("keep") is True and not items:
            probs.append(f"{cid[:10]}: keep without items")
        if r.get("keep") is False and not r.get("reject_reason"):
            probs.append(f"{cid[:10]}: reject without reject_reason")
        if r.get("keep") not in (True, False):
            probs.append(f"{cid[:10]}: keep must be true/false")
        for it in items:
            u, s = it.get("unit"), it.get("sub")
            if u not in units or s not in units[u]["subtopics"]:
                probs.append(f"{cid[:10]}: bad unit/sub {u}/{s}")
            for x in it.get("xref", []) or []:
                if x not in units or x == u:
                    probs.append(f"{cid[:10]}: bad xref {x}")
            if u == "C01" and cid in pilot:
                probs.append(f"{cid[:10]}: C01 item on a pilot-judged chunk")
            if it.get("type") not in TYPES:
                probs.append(f"{cid[:10]}: bad type {it.get('type')!r}")
            if it.get("strength") not in ("direct", "contextual"):
                probs.append(f"{cid[:10]}: bad strength {it.get('strength')!r}")
            sp = it.get("span")
            if not (isinstance(sp, list) and len(sp) == 2 and all(isinstance(v, int) for v in sp)
                    and 1 <= sp[0] <= sp[1] <= nsent[cid]):
                probs.append(f"{cid[:10]}: bad span {sp} (chunk has {nsent[cid]} sentences)")
            if src[cid] == "Temple Economics.md" and it.get("strength") != "contextual":
                probs.append(f"{cid[:10]}: Temple Economics items must be contextual")
            if not it.get("note"):
                probs.append(f"{cid[:10]}: item without note")
    for c in ids:
        if c not in seen:
            probs.append(f"{c[:10]}: not judged")
    return probs


def main(args):
    idx, nsent, units, pilot, src = load()
    pids = sorted(idx) if args == ["--all"] else args
    bad = 0
    for pid in pids:
        p = check(pid, idx, nsent, units, pilot, src)
        if p:
            bad += 1
            print(f"{pid}: {len(p)} problem(s)")
            for x in p[:40]:
                print("  ", x)
        elif args != ["--all"]:
            print(f"{pid}: OK")
    if args == ["--all"]:
        print(f"{len(pids) - bad} of {len(pids)} packets OK")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1:])
