from pathlib import Path
p = Path(__file__).resolve().parent.parent.parent / "run/ch6/6.2.md"
t = p.read_text(encoding="utf-8")
R = [
    ("That descent sets Udayāditya in a branch of the house of its own, at odds with the inscriptions that call him Bhoja's brother. [C06-KBN-JAGTA-EN-A-010; C04-CII-131]",
     "From that descent a junior branch of the house, not the line of Sindhurāja, has been inferred for Udayāditya, a view that Chapter 4 weighs. [C06-KBN-JAGTA-EN-A-011; C06-KBN-JAGTA-EN-A-010]"),
    ("The fragmentary record dated 1513 is a separate object, “very perfunctorily executed”, which says that Udayāditya built the temple in that year;",
     "The fragmentary record dated 1513, carelessly executed and full of gross mistakes, is a separate object, which says that Udayāditya built the temple in V.S. 1116;"),
    ("; C06-KBN-JAGTA-EN-A-006; C06-KBN-JAGTA-EN-A-010; C06-INTACH-001]}}", "; C06-KBN-JAGTA-EN-A-006; C06-KBN-JAGTA-EN-A-011; C06-INTACH-001]}}"),
]
for a, b in R:
    assert t.count(a) == 1, a[:60]
    t = t.replace(a, b)
p.write_text(t, encoding="utf-8")
print("ok")
