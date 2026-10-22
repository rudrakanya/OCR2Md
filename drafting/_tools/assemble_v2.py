"""Assemble the master drafting outline v2 from its parts (free; no API).

  python -I -X utf8 drafting/_tools/assemble_v2.py
    -> editorial/Chapter_4_to_Afterword_Master_Drafting_Outline_v2.md
    -> editorial/plan_v2/qc_v2.md   (hand-off check: each entry's Opening/Closing against Part III, A; check summary)

Inputs in editorial/plan_v2/: front.md, baseline.md, part1.md, chNN.md (04-13), changes_v1.md, parts3_6.md, coverage_chNN.json.
Run coverage_v2.py for every unit first, so the status table and Appendix are current.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

DR = Path(__file__).resolve().parent.parent
W = DR / "editorial" / "plan_v2"
OUT = DR / "editorial" / "Chapter_4_to_Afterword_Master_Drafting_Outline_v2.md"
UNITS = ["04", "05", "06", "07", "08", "09", "10", "11", "12", "13"]
SUBS = json.loads((DR / "_runs" / "units.json").read_text(encoding="utf-8"))
TASK = re.compile(r"\b(?:RR-\d+|RR-K|LR-\d)\b")


def rd(name):
    return (W / name).read_text(encoding="utf-8").strip() + "\n"


def label(n):
    return "Afterword" if n == "13" else f"Ch {int(n)}"


changes = {}
parts = re.split(r"^## (ch\d\d)\s*$", rd("changes_v1.md"), flags=re.M)
for i in range(1, len(parts), 2):
    changes[parts[i][2:]] = parts[i + 1].strip()

entries, status_rows, contents, appendix, qc = {}, [], [], [], []
for n in UNITS:
    t = rd(f"ch{n}.md")
    cov = json.loads((W / f"coverage_ch{n}.json").read_text(encoding="utf-8"))
    secs = re.findall(r"^### ((?:\d+|AW)\.\d+) ([^\n]*?) \*\([^\n]*?(\d[\d,]*) w\)\*", t, flags=re.M)
    words = [int(s[2].replace(",", "")) for s in secs]
    tgt = re.search(r"\*\*Target:\*\* ([\d,]+) words", t).group(1)
    tasks = sorted(set(TASK.findall(t)), key=lambda x: (x[:2], int(re.sub(r"\D", "", x) or 0)))
    tot = cov["totals"]
    status_rows.append(f"| {label(n)} | {len(secs)} | {tgt} | {tot.get('assigned', 0)} / {tot.get('cross-reference', 0)} / "
                       f"{tot.get('excluded', 0)} (of {cov['direct']}) | {', '.join(tasks) or '—'} |")
    title = t.split("\n", 1)[0].lstrip("# ").strip()
    contents.append(f"- {title}")
    contents += [f"  - {s[0]} {s[1]}" for s in secs]
    # insert Changes from v1 after the header line (line 3)
    lines = t.split("\n")
    hdr_end = next(i for i, l in enumerate(lines) if l.startswith("**Target:**")) + 1
    lines[hdr_end:hdr_end] = ["", "### Changes from v1", "", changes[n], ""]
    entries[n] = "\n".join(lines)
    # appendix
    sub_names = SUBS[f"C{n}"]["subtopics"]
    a = [f"## A.{'AW' if n == '13' else int(n)} {title.split('.')[0]}", "",
         f"Direct items: {cov['direct']}. Contextual items cited: {cov.get('contextual_cited', 0)}.", "",
         "| Sub-topic | Assigned | Cross-reference | Excluded |", "|---|---|---|---|"]
    for k, v in cov["by_sub"].items():
        a.append(f"| {k} {sub_names.get(k, '(no sub-topic in the log)')} | {v.get('assigned', 0)} | "
                 f"{v.get('cross-reference', 0)} | {v.get('excluded', 0)} |")
    a.append(f"| **Total** | {tot.get('assigned', 0)} | {tot.get('cross-reference', 0)} | {tot.get('excluded', 0)} |")
    xr = [(i, s[1]) for i, s in cov["status"].items() if s[0] == "cross-reference"]
    ex = [(i, s[1]) for i, s in cov["status"].items() if s[0] == "excluded"]
    if xr:
        a += ["", "**Cross-references (item → home):** " + "; ".join(f"{i} → {h}" for i, h in sorted(xr)) + "."]
    a += ["", "**Exclusions:**", ""] + ([f"- {i}: {r}" for i, r in sorted(ex)] or ["- none"])
    appendix.append("\n".join(a))
    # QC: hand-offs and sum
    op = re.search(r"^\*\*Opening:\*\* (.*)$", t, flags=re.M)
    cl = re.search(r"^\*\*Closing:\*\* (.*)$", t, flags=re.M)
    qc.append(f"| {label(n)} | {sum(words)} / {tgt} | {(op.group(1) if op else 'MISSING')[:110]} | "
              f"{(cl.group(1) if cl else 'MISSING')[:110]} |")

status = ["## Status at v2", "",
          "| Unit | Sections | Target words | Direct items: assigned / cross-ref / excluded | Open tasks (Part V) |",
          "|---|---|---|---|---|"] + status_rows
doc = [rd("front.md"), "\n".join(status) + "\n",
       "## Contents\n\n- Baseline: what Chapters 1–3 have already told\n- Part I. Decisions, evidence rules and homes\n"
       + "".join(f"  - {h}\n" for h in re.findall(r"^## (I\.\d .*)$", rd("part1.md"), flags=re.M))
       + "- Part II. The chapter outlines\n"
       + "\n".join("  " + c for c in contents)
       + "\n- Part III. Cross-Chapter Architecture\n- Part IV. Downstream Drafting Protocol (v2)\n"
         "- Part V. Research Register\n- Part VI. Continuity and Duplication Checklist\n"
         "- Appendix. Coverage by chapter and exclusion lists\n",
       rd("baseline.md"),
       rd("part1.md"),
       "# Part II. The chapter outlines\n\nTen entries follow, Chapter 4 to the Afterword. Rules and decisions are cited "
       "by number (Part I); open tasks by register number (Part V). Section word targets are in each section heading.\n"]
doc += [entries[n].strip() + "\n" for n in UNITS]
doc += [rd("parts3_6.md"),
        "# Appendix. Coverage by chapter and exclusion lists\n\nGenerated from `plan_v2/coverage_chNN.json` "
        "(`_tools/coverage_v2.py`). Statuses: assigned (cited in the entry), cross-reference (cited in another "
        "entry or a delivered Ch 1–4 section), excluded (with its reason). No item is unreasoned.\n",
        "\n\n".join(appendix) + "\n"]
OUT.write_text("\n\n".join(d.strip("\n") for d in doc) + "\n", encoding="utf-8")

chk = subprocess.run([sys.executable, "-I", "-X", "utf8", str(DR / "_tools" / "checks_v2.py")],
                     capture_output=True, text=True, encoding="utf-8").stdout
(W / "qc_v2.md").write_text(
    "# v2 QC log\n\n## Hand-offs (entry Opening/Closing; compare with Part III, A)\n\n"
    "| Unit | Sections sum / target | Opening | Closing |\n|---|---|---|---|\n" + "\n".join(qc)
    + "\n\n## checks_v2.py\n\n```\n" + chk.strip() + "\n```\n", encoding="utf-8")
text = OUT.read_text(encoding="utf-8")
print("written", OUT.name, len(text.split()), "words;", "unreplaced placeholders:", len(re.findall(r"\{\{", text)))
