"""Draft head_chNN.md / tail_chNN.md for a unit from the master outline (free). Edit the results by hand.
  python -I -X utf8 drafting/_tools/draft_head_tail.py 05"""
import re
import sys
from pathlib import Path

DR = Path(__file__).resolve().parent.parent
O = (DR / "editorial" / "Chapter_4_to_Afterword_Master_Drafting_Outline.md").read_text(encoding="utf-8")
W = DR / "editorial" / "plan_work"
n = sys.argv[1]
head_pat = "# Afterword." if n == "13" else f"# Chapter {int(n)}."
a = O.index("\n" + head_pat)
nxt = re.search(r"\n# (Chapter \d+\.|Afterword\.|Part III)", O[a + 5:])
U = O[a:a + 5 + nxt.start()]
title = U.strip().split("\n")[0]
short = title.split(".")[0].lstrip("# ")
rul = re.search(r"(> \*\*Editor's merge rulings.*?)\n\n", U, re.S).group(1)


def grab(label):
    m = re.search(r"- \*\*" + re.escape(label) + r":\*\*\s*(.*?)(?=\n- \*\*|\n## |\n\*\*)", U, re.S)
    return m.group(1).strip() if m else ""


def flat(s):
    return re.sub(r"\s+", " ", s).strip()


tl = re.search(r"\*\*Through-line[^*]*\*\*\s*(.*?)\n\n", U, re.S)
arc = U[U.index("## 2. Chapter Arc") + len("## 2. Chapter Arc"):]
cuts = [arc.find(k) for k in ("**Why this order", "**Why this sequence", "**Through-line", "## 3.")]
arc = arc[:min(c for c in cuts if c >= 0)].strip()
secs = (W / f"sections_ch{n}.md").read_text(encoding="utf-8")
targets = [int(x) for x in re.findall(r"\*\*Word target:\*\* (\d+)", secs)]
names = re.findall(r"^## ((?:\d+|AW)\.\d)", secs, re.M)
plan = " · ".join(f"{x}: {y}" for x, y in zip(names, targets))
head = (f"{title}\n\n**Planned words:** {sum(targets):,} ({plan}). **Evidence:** `evidence_index/ch{n}.jsonl`.\n\n"
        f"**Historical question.** {grab('Central question')}\n\n**Through-line.** {tl.group(1).strip() if tl else ''}\n\n"
        f"**Arc.** {arc}\n\n**Scope.** TODO\n\n**Editor's merge rulings carried into this plan** (from the master outline):\n{rul}\n")
concl = U[U.index("## 4. Chapter Conclusion"):U.index("### Evidence Checklist")]
op = re.search(r"\*\*Opening move:?\*\*(.*?)\n\n", U, re.S)
i0 = U.index("### Research / Verification Flags")
i1 = U.index("### Cross-chapter notes") if "### Cross-chapter notes" in U else len(U)
heads = re.findall(r"^\d+\. \*\*(.*?)\*\*", U[i0:i1], re.M)
IN = flat(op.group(1))[:900] if op else "TODO"
k = concl.find("How the last paragraph")
OUT = flat(concl[k:])[:900] if k >= 0 else "TODO"
FL = "\n".join("- " + h for h in heads)
tail = (f"## {short}: conflicts to present, unresolved\n\nTODO\n\n## {short}: hand-offs\n\n- **In:** {IN}\n- **Out:** {OUT}\n\n"
        f"## {short}: changes from the master outline\n\nTODO\n\n## {short}: research and verification flags\n\n{FL}\n")
(W / f"head_ch{n}.md").write_text(head, encoding="utf-8")
(W / f"tail_ch{n}.md").write_text(tail, encoding="utf-8")
print(len(head.split()), len(tail.split()), names, targets)
