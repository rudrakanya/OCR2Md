"""Assemble the complete book outline (Chapter 1 to the Afterword) from editorial/wholebook/ (free; no API).

  set UDAY_OUTLINE_DIR=wholebook; run _tools/coverage_v2.py NN for NN in 01..13 first (writes wholebook/coverage_chNN.json)
  python -I -X utf8 drafting/_tools/assemble_wholebook.py
    -> editorial/Udaypur_Complete_Book_Outline.md
    -> editorial/wholebook/qc_wholebook.md  (joins: each entry's opening/closing; checks_v2 output; placeholder and reference checks)

Inputs: front.md, part1.md, chNN.md (01-13; 01-04 from delivered_entries.py), parts3_6.md, coverage_chNN.json,
delivered_chNN.json (01-04, words as written).
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

DR = Path(__file__).resolve().parent.parent
W = DR / "editorial" / "wholebook"
OUT = DR / "editorial" / "wholebook" / "Udaypur_Complete_Book_Outline_detailed_16Oct.md"   # the team edition (editorial/Udaypur_Complete_Book_Outline.md) is hand-written
UNITS = [f"{i:02d}" for i in range(1, 14)]
SUBS = json.loads((DR / "_runs" / "units.json").read_text(encoding="utf-8"))
sys.path.insert(0, str(DR / "_tools"))
import dynasty_spelling  # noqa: E402  (U10: sub-topic labels in IAST)
TASK = re.compile(r"\b(?:RR-\d+|RR-K|LR-\d)\b")


def rd(name):
    return (W / name).read_text(encoding="utf-8").strip() + "\n"


def label(n):
    return "Afterword" if n == "13" else f"Ch {int(n)}"


rows, contents, appendix, qc = [], [], [], []
entries = {}
for n in UNITS:
    t = rd(f"ch{n}.md")
    entries[n] = t
    cov = json.loads((W / f"coverage_ch{n}.json").read_text(encoding="utf-8"))
    secs = re.findall(r"^### ((?:\d+|AW)\.\d+) ([^\n]*?) \*\(([^\n]*?)\)\*", t, flags=re.M)
    tgts = [int(re.search(r"(\d[\d,]*) w\b", s[2]).group(1).replace(",", "")) for s in secs]
    tgt = re.search(r"\*\*Target:\*\* ([\d,]+) words", t).group(1)
    written = "—"
    if (W / f"delivered_ch{n}.json").exists():
        d = json.loads((W / f"delivered_ch{n}.json").read_text(encoding="utf-8"))
        written = f"{sum(s['words'] for s in d['sections']):,}"
    status = "written" if written != "—" else "planned"
    tasks = sorted(set(TASK.findall(t.split("## Research and verification")[-1])), key=lambda x: (x[:2], int(re.sub(r"\D", "", x) or 0)))
    tot = cov["totals"]
    rows.append(f"| {label(n)} | {status} | {len(secs)} | {tgt} | {written} | {tot.get('assigned', 0)} / {tot.get('cross-reference', 0)} / "
                f"{tot.get('excluded', 0)} (of {cov['direct']}) | {', '.join(tasks) or '—'} |")
    title = t.split("\n", 1)[0].lstrip("# ").strip()
    contents.append(f"  - {title}")
    contents += [f"    - {s[0]} {s[1]}" for s in secs]
    if sum(tgts) != int(tgt.replace(",", "")) and status == "planned":
        qc.append(f"- **{label(n)}:** section targets sum to {sum(tgts)}, chapter target {tgt}")
    sub_names = SUBS[f"C{n}"]["subtopics"]
    a = [f"## A.{'AW' if n == '13' else int(n)} {title.split('.')[0]}", "",
         f"Direct items: {cov['direct']}. Contextual items cited: {cov.get('contextual_cited', 0)}.", "",
         "| Sub-topic | Assigned | Cross-reference | Excluded |", "|---|---|---|---|"]
    for k, v in cov["by_sub"].items():
        a.append(f"| {k} {dynasty_spelling.fix(sub_names.get(k, '(no sub-topic in the log)'))[0]} | {v.get('assigned', 0)} | {v.get('cross-reference', 0)} | {v.get('excluded', 0)} |")
    a.append(f"| **Total** | {tot.get('assigned', 0)} | {tot.get('cross-reference', 0)} | {tot.get('excluded', 0)} |")
    xr = sorted((i, s[1]) for i, s in cov["status"].items() if s[0] == "cross-reference")
    ex = sorted((i, s[1]) for i, s in cov["status"].items() if s[0] == "excluded")
    if xr:
        a += ["", "**Cross-references (item → home):** " + "; ".join(f"{i} → {h}" for i, h in xr) + "."]
    a += ["", "**Exclusions:**", ""] + ([f"- {i}: {r}" for i, r in ex] or ["- none"])
    appendix.append("\n".join(a))
    op = re.search(r"^\*\*Opening:\*\* (.*)$", t, flags=re.M)
    cl = re.search(r"^\*\*Closing:\*\* (.*)$", t, flags=re.M)
    qc.append(f"| {label(n)} | {(op.group(1) if op else 'MISSING')[:120]} | {(cl.group(1) if cl else 'MISSING')[:120]} |")

status = ["## Status of the units", "",
          "Targets are the chapter targets in Part I, I.6. \"As written\" is the validator's count of the text, with notes and IDs excluded.", "",
          "| Unit | Status | Sections | Target words | As written | Direct items: assigned / cross-ref / excluded | Open tasks (Part V) |",
          "|---|---|---|---|---|---|---|"] + rows
part1_heads = re.findall(r"^## (I\.\d .*)$", rd("part1.md"), flags=re.M)
cont = ["## Contents", "", "- Part I. Decisions, evidence rules and homes"] + [f"  - {h}" for h in part1_heads] + \
       ["- Part II. The chapter entries"] + contents + \
       ["- Part III. Cross-Chapter Architecture", "- Part IV. Downstream Drafting Protocol", "- Part V. Research Register",
        "- Part VI. Continuity and Duplication Checklist", "- Appendix. Coverage by chapter and exclusion lists"]
doc = [rd("front.md"), "\n".join(status) + "\n", "\n".join(cont) + "\n", rd("part1.md"),
       "# Part II. The chapter entries\n\nThirteen entries follow, Chapter 1 to the Afterword. Rules and decisions are cited by number "
       "(Part I); open tasks by register number (Part V). Each section heading gives its scope and its target.\n"]
doc += [entries[n].strip() + "\n" for n in UNITS]
doc += [rd("parts3_6.md"),
        "# Appendix. Coverage by chapter and exclusion lists\n\nGenerated from `wholebook/coverage_chNN.json` (`_tools/coverage_v2.py`). "
        "Statuses: assigned (cited in the entry), cross-reference (cited in another entry or in the written text of Chs 1–4), "
        "excluded (with its reason). No direct item is unreasoned.\n", "\n\n".join(appendix) + "\n"]
text = "\n\n".join(d.strip("\n") for d in doc) + "\n"
OUT.write_text(text, encoding="utf-8")

env = dict(os.environ, UDAY_OUTLINE_DIR="wholebook", PYTHONIOENCODING="utf-8")
chk = subprocess.run([sys.executable, "-I", "-X", "utf8", str(DR / "_tools" / "checks_v2.py")] + UNITS[4:],
                     capture_output=True, text=True, encoding="utf-8", env=env).stdout
have = set(re.findall(r"^### ((?:\d+|AW)\.\d+) ", text, flags=re.M))
refs = sorted({r for r in re.findall(r"§((?:\d+|AW)\.\d+)\b", text) if r not in have})
ph = re.findall(r"\{\{(?!note)", text)
(W / "qc_wholebook.md").write_text(
    "# Whole-book QC log\n\n## Joins (each entry's opening and closing; compare Part III, A)\n\n| Unit | Opening | Closing |\n|---|---|---|\n"
    + "\n".join(q for q in qc if q.startswith("|")) + "\n\n## Target sums (planned units)\n\n"
    + ("\n".join(q for q in qc if q.startswith("- ")) or "- all planned units sum to their chapter targets")
    + f"\n\n## References\n\n- section references to sections that do not exist: {refs or 'none'}\n- unfilled placeholders: {len(ph)}\n\n"
    "## checks_v2.py (Chs 5–13; Chs 1–4 are checked by the text's own validator)\n\n```\n" + chk.strip() + "\n```\n", encoding="utf-8")
print("written", OUT.name, len(text.split()), "words; missing refs:", refs or "none", "; placeholders:", len(ph))
