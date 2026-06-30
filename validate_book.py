import re, os
from pathlib import Path

d = Path("book")
print(f"{'ch':<4}{'body_w':>7}{'markers':>9}{'notes':>7}{'seq':>5}{'deva':>6}{'iast':>7}{'moji':>6}{'1st-person':>11}{'gaps':>6}")
for i in range(1, 8):
    t = (d / f"chapter-{i:02d}.md").read_text(encoding="utf-8")
    parts = re.split(r"(?m)^##\s+Notes\s*$", t)
    body = parts[0]
    notes = parts[1] if len(parts) > 1 else ""
    bmarks = [int(x) for x in re.findall(r"\[(\d+)\]", body)]
    nmarks = [int(m.group(1)) for m in re.finditer(r"(?m)^\[(\d+)\]", notes)]
    seq = bmarks == list(range(1, len(bmarks) + 1)) and nmarks == list(range(1, len(nmarks) + 1)) and len(bmarks) == len(nmarks)
    deva = len(re.findall(r"[ऀ-ॿ]", t))
    iast = len(re.findall(r"[āīūṛṝḷṃḥṅñṭḍṇśṣ]", t))
    moji = len(re.findall(r"[ÃÂ][\x80-\xbf]|â€", t))
    # first-person leakage in body (outside obvious quotes is hard to detect; count all)
    fp = len(re.findall(r"\bI\b|\bwe\b|\bus\b|\bour\b|\byou\b|\byour\b", body))
    gaps = body.count("[GAP")
    bw = len(body.split())
    print(f"{i:<4}{bw:>7}{len(bmarks):>9}{len(nmarks):>7}{str(seq):>5}{deva:>6}{iast:>7}{moji:>6}{fp:>11}{gaps:>6}")
