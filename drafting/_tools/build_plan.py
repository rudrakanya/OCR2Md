"""Draft the per-unit section blocks of PLAN_CH04-AW.md from the master outline (free; no API).

For each unit it extracts, per section: the word target, the section statement, the purpose, the paragraph plan
(Points and E/C/X/Note roles, verbatim), the drafting guidance and the transition, and annotates every evidence ID
with its tier (from the evidence log's book code via _pipe/tiers.py; KB items from the code in the ID).
Editor's merge rulings that replace outline text are applied here (REPLACE below).

  python -I -X utf8 drafting/_tools/build_plan.py            # writes drafting/editorial/plan_work/sections_chNN.md
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DR = Path(__file__).resolve().parent.parent
OUTLINE = DR / "editorial" / "Chapter_4_to_Afterword_Master_Drafting_Outline.md"
WORK = DR / "editorial" / "plan_work"
LOG = DR / "_evidence_log.jsonl"
sys.path.insert(0, str(DR / "_pipe"))
import tiers  # noqa: E402

ID = re.compile(r"\bC\d\d-[A-Z0-9]+(?:-[A-Z0-9]+)*?-\d{3}\b")
UNITS = [("04", "# Chapter 4."), ("05", "# Chapter 5."), ("06", "# Chapter 6."), ("07", "# Chapter 7."), ("08", "# Chapter 8."),
         ("09", "# Chapter 9."), ("10", "# Chapter 10."), ("11", "# Chapter 11."), ("12", "# Chapter 12."), ("13", "# Afterword.")]

# merge rulings applied to the outline text (Part I, I.5 and the chapter rulings blocks)
REPLACE = {
    "10": [
        (re.compile(r"  1\. \*\[Superseded at merge.*?(?=\n  2\. \*\*P2)", re.S),
         "  1. **P1 — A Gujarat king named at Udaypur.** **Point:** Open on the inscription at Udaypur dated V.S. 1220 (1163), which shows "
         "the place governed by the *mahāsādhanika* Rājyapāla while Kumārapāla of Aṇahilapāṭaka, a Caulukya king of Gujarat, was reigning: "
         "the first stone at Udaypur to name a king of another house, some seventy years after the founder's last dated record. Pose the "
         "chapter's question from it (who held Udaypur after its founder's line, and did the town's rank change with its masters?), then step "
         "back to the 1090s. About 120 words; 1.2 now names Rājyapāla with his Caulukya master (U1), so recall in a clause and add the "
         "question.\n     - E: C10-PARTEMPLES-001, C10-CII-002 · C: C08-GANGULY-016 · Note: C06-GANGULY-034 (Ganguly's Kumārapāla record "
         "of 1163; possibly the same stone; not merged), C01-GANGULY-015 (Ganguly's \"eastern division\" framing, attributed)\n"),
        ("     - \"Some time subsequently\" the region passed to Kumārapāla.\n     - An inscription at Udaypur of V.S. 1220 (1163) shows the place governed by the *mahāsādhanika* Rājyapāla under Kumārapāla of Aṇahilapāṭaka. In that year one Vasantapāla made donations for the upkeep of a temple of Udaleśvara in the town.\n",
         "     - (P1 has given the V.S. 1220 record.) In 1163 one Vasantapāla made donations for the upkeep of a temple of Udaleśvara in the town.\n"),
        ("     - Introduce the record inside the temple's east entrance (fresh at merge, not a return to an opening): Ganguly reads",
         "     - Introduce the record inside the temple's east entrance (fresh, not a return to an opening): Ganguly reads"),
    ],
}


def tier_map():
    m = {}
    for line in LOG.open(encoding="utf-8"):
        r = json.loads(line)
        m[r["id"]] = tiers.tier_of(r)[0]
    return m


def code_of(i):
    parts = i.split("-")[1:-1]
    if parts and parts[0] == "KB":
        parts = parts[1:]
    return "-".join(parts)


def annotate(text, tm):
    def rep(mm):
        i = mm.group(0)
        t = tm.get(i)
        if t is None:
            t = tiers.tier_of({"book_code": code_of(i)})[0]
        return f"{i} (T{t})"
    return ID.sub(rep, text)


def field(sec, label, stop_labels):
    m = re.search(r"^- \*\*" + re.escape(label) + r"[^\n]*", sec, re.M)
    if not m:
        return ""
    start = m.start()
    rest = sec[m.end():]
    ends = [rest.find("\n- **" + s) for s in stop_labels]
    ends = [e for e in ends if e >= 0]
    end = m.end() + (min(ends) if ends else len(rest))
    return sec[start:end].strip()


def main():
    t = OUTLINE.read_text(encoding="utf-8")
    t = t[:t.index("\n# Part III.")]
    tm = tier_map()
    WORK.mkdir(exist_ok=True)
    labels = ["Section statement", "Purpose", "Core claim", "Paragraph plan", "Evidence to deploy", "Evidence sequence",
              "Analytical payoff", "Drafting guidance", "Classification", "Transition"]
    for k, (n, head) in enumerate(UNITS):
        a = t.index("\n" + head)
        b = t.index("\n" + UNITS[k + 1][1]) if k + 1 < len(UNITS) else len(t)
        unit = t[a:b]
        for old, new in REPLACE.get(n, []):
            if isinstance(old, re.Pattern):
                unit, c = old.subn(new, unit, count=1)
            else:
                c = unit.count(old)
                unit = unit.replace(old, new, 1)
            assert c, (n, str(old)[:60])
        body = unit[unit.index("## 3. Sections"):unit.index("## 4. Chapter Conclusion")]
        secs = re.split(r"\n(?=### (?:\d+|AW)\.\d )", body)[1:]
        out = []
        for s in secs:
            h = s.split("\n", 1)[0]
            w = re.search(r"~([\d,]+) w", h)
            words = int(w.group(1).replace(",", "")) if w else None
            title = re.sub(r"\s*\*\(.*$", "", h[4:]).strip()
            scope = re.search(r"\*\((.*?)\)\*", h)
            parts = [f"## {title} *({scope.group(1) if scope else ''})*", "", f"**Word target:** {words}", ""]
            for lab in ("Section statement", "Purpose"):
                parts.append(field(s, lab, [x for x in labels if x != lab]))
            pp = field(s, "Paragraph plan", ["Evidence to deploy", "Evidence sequence", "Analytical payoff", "Drafting guidance",
                                             "Classification", "Transition"])
            parts.append(annotate(pp, tm))
            dg = field(s, "Drafting guidance", ["Classification", "Transition"])
            if dg:
                parts.append(annotate(dg, tm))
            parts.append(field(s, "Transition", []))
            out.append("\n".join(p for p in parts if p is not None) + "\n")
        (WORK / f"sections_ch{n}.md").write_text("\n---\n\n".join(out), encoding="utf-8")
        print(n, len(secs), "sections")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
