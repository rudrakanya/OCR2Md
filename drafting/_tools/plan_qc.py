"""Assemble drafting/editorial/PLAN_CH04-AW.md from plan_work/ and run the scripted QC (free; no API).

Per unit present in plan_work (head_chNN.md + sections_chNN_edited.md + tail_chNN.md):
  - ID validity: every ID exists in the evidence log, the Ch 1-3 KB packs, or the evidence index
  - one primary home: no ID is E (establishing) in two units
  - Gazetteer share: GAZ items <= 40% of the E/C/X items cited in any section
  - lengths: section word targets sum to the head's "Planned words"
  - hand-offs: the unit's Out and the next unit's In are both present (printed side by side for review)
Writes plan_work/QC_REPORT.md and the assembled plan.

  python -I -X utf8 drafting/_tools/plan_qc.py
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

DR = Path(__file__).resolve().parent.parent
W = DR / "editorial" / "plan_work"
PLAN = DR / "editorial" / "PLAN_CH04-AW.md"
ID = re.compile(r"\bC\d\d-[A-Z0-9]+(?:-[A-Z0-9]+)*?-\d{3}\b")
UNITS = ["04", "05", "06", "07", "08", "09", "10", "11", "12", "13"]
TITLES = {"04": "Ch 4", "05": "Ch 5", "06": "Ch 6", "07": "Ch 7", "08": "Ch 8", "09": "Ch 9", "10": "Ch 10", "11": "Ch 11",
          "12": "Ch 12", "13": "Afterword"}


def known_ids():
    ids, book = set(), {}
    for line in (DR / "_evidence_log.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        ids.add(r["id"])
        book[r["id"]] = r["book_code"]
    for f in DR.glob("ch0[1-3]/evidence_pack*.json"):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        items = d if isinstance(d, list) else d.get("items", [])
        for it in items:
            if isinstance(it, dict) and "id" in it:
                ids.add(it["id"])
                book.setdefault(it["id"], it.get("book_code"))
    kn = DR / "evidence_index" / "kb_new.jsonl"
    if kn.exists():
        for line in kn.open(encoding="utf-8"):
            r = json.loads(line)
            ids.add(r["id"])
            book[r["id"]] = r["book_code"]
    return ids, book


def roles(text):
    """yield (role, [ids]) for each '- E: … · C: … · X: … · Note: …' line"""
    for line in text.split("\n"):
        s = line.strip().lstrip(">").strip()
        if not re.match(r"^- (E|C|X):", s):
            continue
        for part in re.split(r" · ", s[2:]):
            m = re.match(r"^(E|C|X|Note|Lineage note|Accession note)\s*:\s*(.*)$", part.strip())
            if m:
                yield m.group(1), ID.findall(m.group(2))


def main():
    ids, book = known_ids()
    report = ["# Plan QC report", ""]
    status = []
    primary = collections.defaultdict(set)
    units_text = {}
    for n in UNITS:
        files = [W / f"head_ch{n}.md", W / f"sections_ch{n}_edited.md", W / f"tail_ch{n}.md"]
        if not all(f.exists() for f in files):
            status.append((n, None, False, False, "not planned"))
            continue
        head, secs, tail = (f.read_text(encoding="utf-8") for f in files)
        units_text[n] = (head, secs, tail)
        probs = []
        bad = sorted({i for i in ID.findall(head + secs + tail) if i not in ids})
        if bad:
            probs.append(f"unknown IDs: {', '.join(bad)}")
        for role, l in roles(secs):
            if role == "E":
                for i in l:
                    primary[i].add(n)
        for sec in re.split(r"\n(?=## (?:\d+|AW)\.\d )", secs):
            h = sec.split("\n", 1)[0]
            cited = [i for role, l in roles(sec) if role in ("E", "C", "X") for i in l]
            if cited:
                g = sum(1 for i in cited if book.get(i) == "GAZ")
                if g / len(cited) > 0.40:
                    probs.append(f"Gazetteer share {g}/{len(cited)} in {h[3:40]}")
        targets = [int(x) for x in re.findall(r"\*\*Word target:\*\* (\d+)", secs)]
        m = re.search(r"\*\*Planned words:\*\* ([\d,]+)", head)
        planned = int(m.group(1).replace(",", "")) if m else None
        if planned != sum(targets):
            probs.append(f"length: sections sum {sum(targets)} vs planned {planned}")
        if "**In" not in tail or "**Out" not in tail:
            probs.append("hand-off In/Out missing")
        report += [f"## {TITLES[n]}", "", f"- IDs cited: {len(set(ID.findall(head + secs + tail)))}; section targets {targets} = {sum(targets)}"]
        report += [f"- PROBLEM: {p}" for p in probs] or ["- no problems"]
        report.append("")
        status.append((n, planned, True, not probs, "; ".join(probs)))
    multi = {i: u for i, u in primary.items() if len(u) > 1}
    report += ["## One primary home (E in more than one unit)", ""]
    report += [f"- {i}: E in {', '.join(TITLES[x] for x in sorted(u))}" for i, u in sorted(multi.items())] or ["- none"]
    report += ["", "## Hand-offs (Out of each unit beside In of the next)", ""]
    keys = [n for n in UNITS if n in units_text]
    for a, b in zip(keys, keys[1:]):
        out = re.search(r"\*\*Out[^\n]*", units_text[a][2])
        inn = re.search(r"\*\*In[^\n]*", units_text[b][2])
        report += [f"- {TITLES[a]} → {TITLES[b]}", f"  - OUT: {out.group(0)[:300] if out else '—'}", f"  - IN: {inn.group(0)[:300] if inn else '—'}"]
    (W / "QC_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    # status table + assembly
    multi_units = {x for u in multi.values() for x in u}
    rows = ["| Unit | Planned words | Planned | QC passed | Notes |", "|---|---|---|---|---|"]
    for n, planned, done, ok, note in status:
        ok2 = ok and n not in multi_units
        rows.append(f"| {TITLES[n]} | {planned or '—'} | {'yes' if done else 'no'} | {'yes' if (done and ok2) else ('no' if done else '—')} | "
                    f"{note if note and note != 'not planned' else ('primary-home overlap: see QC report' if done and n in multi_units else '')} |")
    front = (W / "plan_front.md").read_text(encoding="utf-8") if (W / "plan_front.md").exists() else "# Unified drafting plan, Chapter 4 to the Afterword\n"
    parts = [front.replace("{{STATUS}}", "\n".join(rows))]
    for n in keys:
        h, s, t = units_text[n]
        parts.append(h.strip() + "\n\n" + s.strip() + "\n\n" + t.strip() + "\n")
    closing = W / "plan_closing.md"
    if closing.exists():
        parts.append(closing.read_text(encoding="utf-8"))
    PLAN.write_text("\n\n---\n\n".join(p.strip() for p in parts) + "\n", encoding="utf-8")
    print("\n".join(report[:200]))
    print("\nstatus:\n" + "\n".join(rows))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
