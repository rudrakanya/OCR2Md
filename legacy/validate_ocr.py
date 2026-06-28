import re, os

docs = {
    "Vol 1": ("remaining texts/The Hindu Temple Vol 1 Stella Kramrisch.md", 310),
    "Vol 2": ("remaining texts/The Hindu Temple Vol 2.md", 350),
}
note = "No machine-readable text detected"
for name, (md, exp) in docs.items():
    t = open(md, encoding="utf-8").read()
    markers = [int(m.group(1)) for m in re.finditer(r"(?m)^<!-- page (\d+) -->$", t)]
    segs = re.split(r"(?m)^<!-- page \d+ -->$", t)[1:]
    empty = sum(1 for s in segs if not s.strip())
    moji = len(re.findall(r"[ÃÂ][-¿]", t))
    deva = len(re.findall(r"[ऀ-ॿ]", t))
    iast = len(re.findall(r"[āīūṛṃḥṅñṭḍṇśṣ]", t))
    seq = markers == list(range(1, exp + 1))
    print(f"{name}: {os.path.getsize(md)//1024} KB | markers {len(markers)}/{exp} sequential={seq} "
          f"| empty-body {empty} | blank/plate annotated {t.count(note)} "
          f"| NOT-PROCESSED {t.count('NOT PROCESSED')} | Devanagari {deva} | IAST {iast} | mojibake {moji}")
