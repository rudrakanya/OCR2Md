"""Write as-delivered chapter entries (Chapters 1-4) for the whole-book outline (free; no API).

  python -I -X utf8 drafting/_tools/delivered_entries.py
    reads  editorial/wholebook/delivered_chNN.json (from reconcile.py), the chapter plans, editorial/wholebook/entry_text_chNN.md
    writes editorial/wholebook/chNN.md (01-04)

The structure (sections, words, paragraphs, cited IDs and roles, opening, closing) comes from the delivered text.
Function, arc, statements and paragraph points come from the hand-reconciled file entry_text_chNN.md, which states the
delivered content (written after rereading each section); its keys are:
  ## function / ## arc / ## conclusion / ## research / ## crossrefs / ## sec N.x  (statement, then "- P<n>: point" lines,
  then "transition: …")
"""
import json
import re
import sys
from pathlib import Path

DR = Path(__file__).resolve().parent.parent
W = DR / "editorial" / "wholebook"
sys.path.insert(0, str(DR / "_tools"))
import reconcile  # noqa: E402  (tier lookup)

ORDER = ["E", "C", "X", "Note"]
PACK_TIERS = {}
for _pk in DR.glob("ch0[1-4]/evidence_pack_v*.json"):
    for _it in json.loads(_pk.read_text(encoding="utf-8")):
        if isinstance(_it, dict) and _it.get("id") and _it.get("tier"):
            PACK_TIERS.setdefault(_it["id"], _it["tier"])


def tier(i):
    t = reconcile.tier(i)
    return t if t != "T?" else (f"T{PACK_TIERS[i]}" if i in PACK_TIERS else "T?")


def parse_text(n):
    t = (W / f"entry_text_ch{n:02d}.md").read_text(encoding="utf-8")
    blocks = {}
    for part in re.split(r"^## ", t, flags=re.M)[1:]:
        k, _, body = part.partition("\n")
        blocks[k.strip()] = body.strip()
    return blocks


def sec_text(block):
    stmt, points, trans, scope, title = [], {}, "", "", ""
    for line in block.split("\n"):
        m = re.match(r"- P(\d+):\s*(.+)", line)
        if m:
            points[int(m.group(1))] = m.group(2).strip()
        elif line.startswith("transition:"):
            trans = line.split(":", 1)[1].strip()
        elif line.startswith("scope:"):
            scope = line.split(":", 1)[1].strip()
        elif line.startswith("title:"):
            title = line.split(":", 1)[1].strip()
        elif line.strip():
            stmt.append(line.rstrip())
    return "\n".join(stmt).strip(), points, trans, scope, title


def role_line(roles):
    by = {r: [] for r in ORDER}
    for i, r in roles.items():
        by.setdefault(r if r in by else "C", []).append(f"{i} ({tier(i)})")
    return " · ".join(f"{r}: {', '.join(v)}" for r, v in by.items() if v)


LATER_E = {}
for _f in sorted(W.glob("ch*.md")):
    if _f.stem >= "ch05" and re.match(r"ch\d\d$", _f.stem):
        for _line in _f.read_text(encoding="utf-8").splitlines():
            _m = re.search(r"- E:\s*([^·]*)", _line)
            if _m:
                for _i in reconcile.ID.findall(_m.group(1)):
                    LATER_E.setdefault(_i, _f.stem)


def home_role(i, role, n):
    """R6: in a written chapter an item establishes (E) only if it belongs to this unit and no later entry tells it in full."""
    if role != "E":
        return role
    if not i.startswith(f"C{n:02d}-") or i in LATER_E:
        return "C"
    return "E"


def main():
    for n in (1, 2, 3, 4):
        d = json.loads((W / f"delivered_ch{n:02d}.json").read_text(encoding="utf-8"))
        b = parse_text(n)
        total = sum(s["words"] for s in d["sections"])
        L = [f"# Chapter {n}. {d['title']}", "", b["header"].replace("{WORDS}", f"{total:,}").replace("{SECTIONS}", str(len(d["sections"]))), "",
             "## 1. Chapter function", "", b["function"], "", "## 2. Arc", "", b["arc"], "",
             f"**Opening:** “{d['opening']}”", "", f"**Closing:** “{d['closing']}”", "", "## 3. Sections", ""]
        for s in d["sections"]:
            stmt, points, trans, scope, title = sec_text(b[f"sec {s['sec']}"])
            L.append(f"### {s['sec']} {title or s['title']} *({scope} · {s['target']:,} w; as written {s['words']:,})*")
            L.append(f"- **Statement:** {stmt}")
            L.append("- **Paragraphs:**")
            for p in s["paras"]:
                pt = points.get(p["n"])
                assert pt, f"{s['sec']} P{p['n']} has no point in entry_text_ch{n:02d}.md"
                head, _, rest = pt.partition(" | ")
                L.append(f"  {p['n']}. **{head}.** *Point:* {rest}")
                if p["roles"]:
                    L.append(f"     - {role_line({i: home_role(i, r, n) for i, r in p['roles'].items()})}")
            L.append(f"- **Transition:** {trans}")
            L.append("")
        L += ["## 4. Conclusion", "", b["conclusion"], "", "## Evidence checklist", ""]
        for s in d["sections"]:
            es = [i for p in s["paras"] for i, r in p["roles"].items() if home_role(i, r, n) == "E"]
            es = list(dict.fromkeys(es))[:8]
            L.append(f"- **{s['sec']}:** {', '.join(es)}.")
        L += ["", "## Research and verification (this chapter; see the Research Register)", "", b["research"], "", "## Cross-chapter notes", "", b["crossrefs"], ""]
        (W / f"ch{n:02d}.md").write_text("\n".join(L), encoding="utf-8")
        print(f"ch{n:02d}: {len(d['sections'])} sections, {total} words")


if __name__ == "__main__":
    main()
