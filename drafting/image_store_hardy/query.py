"""Query the Hardy image store (free, local).

  python -I -X utf8 drafting/image_store_hardy/query.py "Fig. 2.3"       by the author's label ("2.3", "fig 2.3", "Figure 2.3")
  python -I -X utf8 drafting/image_store_hardy/query.py "Map 4"          a map; also "cover", "frontispiece", "part 3 opener", "tailpiece"
  python -I -X utf8 drafting/image_store_hardy/query.py "10.18b"         a sub-figure, where the parts are saved separately
  python -I -X utf8 drafting/image_store_hardy/query.py --chapter 20     every figure in a chapter
  python -I -X utf8 drafting/image_store_hardy/query.py --page 125       by PDF page (picture page or caption page)
  python -I -X utf8 drafting/image_store_hardy/query.py --text "bhumija" caption substring (case- and diacritic-insensitive)
  python -I -X utf8 drafting/image_store_hardy/query.py --type plan      by image type (photograph, drawing, plan, elevation, section, map)
  python -I -X utf8 drafting/image_store_hardy/query.py --semantic "Bhumija tower drawings"   by meaning (top 10;
                                                                     --top N). Uses caption_embeddings.npz; each new
                                                                     query is one embedding call (~$0.000003), cached
  add --whole to list whole figures only (no separate parts), --flagged for records marked ocr_verify, --json for raw records.
  Filters combine: --chapter 20 --type photograph --text udayapur
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent


def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def load():
    return [json.loads(l) for l in (HERE / "image_manifest.jsonl").open(encoding="utf-8")]


def parse_label(q):
    """'Fig. 2.3' / 'figure 2.3b' / '2.3' -> ('2.3', 'b' or None); 'Map 4' -> ('Map 4', None); else the folded text."""
    q = q.strip()
    m = re.match(r"^(?:fig(?:ure)?s?\.?\s*)?(\d{1,2})\s*[.,]\s*(\d{1,2})\s*([a-z])?$", q, re.I)
    if m:
        return f"{int(m.group(1))}.{int(m.group(2))}", (m.group(3) or "").lower() or None
    m = re.match(r"^map\s*(\d)$", q, re.I)
    if m:
        return f"Map {m.group(1)}", None
    m = re.match(r"^part\s*(\d)(?:\s*opener)?$", q, re.I)
    if m:
        return f"Part {m.group(1)} opener", None
    return q, None


def search(recs, a):
    out = recs
    if a.label:
        lab, sub = parse_label(a.label)
        out = [r for r in out if fold(r["label"]) == fold(lab)]
        if sub:
            out = [r for r in out if r["kind"] == "whole" or (r.get("sub_label") or "") == sub]
    if a.chapter is not None:
        out = [r for r in out if r.get("chapter") == a.chapter]
    if a.page is not None:
        out = [r for r in out if a.page in (r.get("page"), r.get("caption_page")) or a.page in (r.get("all_pages") or [])]
    if a.text:
        q = fold(a.text)
        out = [r for r in out if q in fold(" ".join(str(r.get(k) or "") for k in
                                                   ("caption", "label", "chapter_title", "notes")))]
    if a.type:
        out = [r for r in out if fold(a.type) in fold(r.get("image_type"))]
    if a.whole:
        out = [r for r in out if r["kind"] == "whole"]
    if a.flagged:
        out = [r for r in out if r.get("ocr_verify")]
    return out


def semantic(q, top):
    """labels ranked by cosine similarity of the query to the stored caption embeddings."""
    import hashlib
    import numpy as np
    z = np.load(HERE / "caption_embeddings.npz", allow_pickle=False)
    meta = json.loads((HERE / "caption_embeddings.json").read_text(encoding="utf-8"))
    cache_p = HERE / "_work" / "query_cache.json"
    cache = json.loads(cache_p.read_text(encoding="utf-8")) if cache_p.exists() else {}
    key = hashlib.sha256(f"{meta['model']}|{meta['dimensions']}|{q}".encode()).hexdigest()
    if key not in cache:
        sys.path.insert(0, str(HERE / "_tools"))
        from embed import load_key
        from openai import OpenAI
        r = OpenAI(api_key=load_key()).embeddings.create(model=meta["model"], input=[q], dimensions=meta["dimensions"])
        cache[key] = r.data[0].embedding
        cache_p.write_text(json.dumps(cache), encoding="utf-8")
    v = np.array(cache[key], dtype=np.float32)
    v /= np.linalg.norm(v)
    s = z["vecs"] @ v
    order = np.argsort(-s)[:top]
    return [(str(z["labels"][i]), float(s[i])) for i in order]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("label", nargs="?")
    ap.add_argument("--chapter", type=int)
    ap.add_argument("--page", type=int)
    ap.add_argument("--text")
    ap.add_argument("--type")
    ap.add_argument("--whole", action="store_true")
    ap.add_argument("--flagged", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--semantic")
    ap.add_argument("--top", type=int, default=10)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    res = search(load(), a)
    score = {}
    if a.semantic:
        ranked = semantic(a.semantic, a.top)
        score = dict(ranked)
        order = {l: i for i, (l, _) in enumerate(ranked)}
        res = sorted((r for r in res if r["label"] in score), key=lambda r: (order[r["label"]], r["kind"] != "whole"))
    shown = set()
    for r in res:
        if a.json:
            print(json.dumps(r, ensure_ascii=False))
            continue
        part = f" ({r['sub_label'] or 'part ' + str(r['part_index'])})" if r["kind"] == "part" else ""
        sc = f"[{score[r['label']]:.3f}]  " if r["label"] in score and r["kind"] == "whole" else ""
        print(f'{sc}{r["id"]}  {r["label_ref"]}{part}  ch.{r.get("chapter") or "-"}  p.{r["page"]}  '
              f'{r["image_type"]}  {r["file"]}')
        if r["label"] not in shown:      # print each caption once
            shown.add(r["label"])
            if r.get("caption"):
                print(f'    caption: {r["caption"]}')
            if r.get("caption_page") and r["caption_page"] != r["page"]:
                print(f'    (caption printed on p.{r["caption_page"]})')
            if r.get("ocr_verify"):
                print("    [CHECK: " + "; ".join(r.get("ocr_verify_reasons") or []) + "]")
    print(f"{len(res)} record(s)")


if __name__ == "__main__":
    main()
