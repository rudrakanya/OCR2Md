"""Scripted checks for the master outline v2 chapter entries (free; no API).

  python -I -X utf8 drafting/_tools/checks_v2.py [NN ...]      default: every plan_v2/chNN.md present

Checks per unit:
  ids       every cited ID exists (evidence index, kb_new, Ch 1-3 KB packs)
  quotes    every “…” quotation inside a paragraph Point is found verbatim in one of that paragraph's cited items
  primary   no item is E (establishing) in two units
  gaz       Gazetteer <= 40% of a section's cited E/C/X items (warning)
  length    section targets sum to the unit target in the entry header
  rules     R2: "Karṇa" without Kalachuri/Caulukya/Gujarat/Dāhala/Chedi within 60 characters (unless marked "unspecified");
            R4: Bhāillasvāmi / Bhṛṅgārikā / mahādvādaśaka / "eastern division" within a sentence naming Udayāditya without a
                twelfth-century date marker; R1/R3: "1513" and "1562" or "1116" called one record ("same record")
"""
import os
import json
import re
import sys
from pathlib import Path

DR = Path(__file__).resolve().parent.parent
W = DR / "editorial" / os.environ.get("UDAY_OUTLINE_DIR", "plan_v2")   
ID = re.compile(r"\bC\d\d-[A-Z0-9]+(?:-[A-Z0-9]+)*?-\d{3}\b")


def known():
    q, book = {}, {}
    for f in list((DR / "evidence_index").glob("ch*.jsonl")) + [DR / "evidence_index" / "kb_new.jsonl"]:
        if f.exists():
            for l in f.open(encoding="utf-8"):
                r = json.loads(l)
                q[r["id"]] = r["quote"]
                book[r["id"]] = r["book_code"]
    for f in DR.glob("ch0[1-3]/evidence_pack*.json"):
        try:
            for it in json.loads(f.read_text(encoding="utf-8")):
                if isinstance(it, dict) and "id" in it:
                    q.setdefault(it["id"], it.get("quote", ""))
                    book.setdefault(it["id"], it.get("book_code"))
        except Exception:
            pass
    return q, book


def norm(s):
    return re.sub(r"\s+", " ", s.replace("’", "'").replace("‘", "'")).strip().lower()


def check(n, Q, B, primary):
    t = (W / f"ch{n}.md").read_text(encoding="utf-8")
    probs, warns = [], []
    bad = sorted({i for i in ID.findall(t) if i not in Q})
    if bad:
        probs.append("unknown IDs: " + ", ".join(bad))
    # paragraphs: a numbered Point block followed by its role line(s)
    secs = re.split(r"\n(?=### (?:\d+|AW)\.\d+ )", t)
    targets = []
    for s in secs[1:]:
        h = s.split("\n", 1)[0]
        m = re.search(r"·\s*([\d,]+)\s*w\b", h)
        targets.append(int(m.group(1).replace(",", "")) if m else 0)
        cited = []
        for para in re.split(r"\n\s*\d+\.\s+\*\*", s)[1:]:
            ids = ID.findall(para)
            for role_line in re.findall(r"- (?:E|C|X):.*", para):
                for part in role_line.split(" · "):
                    mm = re.match(r"-?\s*(E|C|X)\s*:\s*(.*)", part.strip())
                    if mm:
                        cited += ID.findall(mm.group(2))
                        if mm.group(1) == "E":
                            for i in ID.findall(mm.group(2)):
                                primary.setdefault(i, set()).add(n)
            point = para.split("\n     -")[0]
            for qt in re.findall(r"“([^”]{6,})”", point):
                if not any(norm(qt) in norm(Q.get(i, "")) for i in ids):
                    probs.append(f"{h[4:12]} quotation not verbatim in the paragraph's items: “{qt[:60]}”")
        if cited:
            g = sum(1 for i in cited if B.get(i) == "GAZ")
            if g / len(cited) > 0.40:
                warns.append(f"{h[4:40]}: Gazetteer {g}/{len(cited)} of cited items (R8)")
    m = re.search(r"\*\*Target:\*\*\s*([\d,]+)", t)
    total = int(m.group(1).replace(",", "")) if m else None
    if total is not None and total != sum(targets):
        probs.append(f"length: section targets sum {sum(targets)} vs target {total}")
    plain = re.sub(r"`[^`]*`", "", t)
    for mm in re.finditer(r"Karṇa\b", plain):
        ctx = plain[max(0, mm.start() - 60): mm.end() + 60]
        if not re.search(r"Kalachuri|Kalacuri|Caulukya|Chaulukya|Gujarat|Gurjara|Dāhala|Chedi|unspecified|R2", ctx):
            probs.append(f"R2: Karṇa without dynasty: …{ctx.strip()[:100]}…")
    for sent in re.split(r"(?<=[.;])\s+", plain):
        if re.search(r"Bhāillasvāmi|Bhṛṅgārikā|ahādvādaśaka|eastern division", sent) and re.search(r"Udayāditya", sent) \
                and not re.search(r"11[67]\d|twelfth|1160s|1170s|R4|U1|later|eighty years", sent):
            probs.append(f"R4: twelfth-century term near Udayāditya without a date: {sent.strip()[:110]}")
        if re.search(r"same record|one record", sent) and re.search(r"1513|1562|1116", sent) and not re.search(r"never|not|no item|R1|R3", sent):
            probs.append(f"R1/R3: records merged? {sent.strip()[:110]}")
    return probs, warns, targets, total


def main():
    Q, B = known()
    units = sys.argv[1:] or sorted(f.stem[2:] for f in W.glob("ch[0-9][0-9].md"))
    primary, out = {}, []
    allu = sorted(f.stem[2:] for f in W.glob("ch[0-9][0-9].md"))
    res = {}
    for n in allu:
        res[n] = check(n, Q, B, primary)
    for n in units:
        probs, warns, targets, total = res[n]
        out.append(f"C{n}: sections {targets} = {sum(targets)} (target {total}); problems {len(probs)}; warnings {len(warns)}")
        out += ["  PROBLEM " + p for p in probs] + ["  warn " + w for w in warns]
    multi = {i: u for i, u in primary.items() if len(u) > 1}
    out.append("primary in two units: " + (", ".join(f"{i} {sorted(u)}" for i, u in sorted(multi.items())) or "none"))
    print("\n".join(out))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
