#!/usr/bin/env python
"""A visual map of the v2 vector database, plus the diagnostics behind it.

    python phase4_vector_map.py --store v2-openai
    python phase4_vector_map.py --store v2            # the local e5 collection

Writes a self-contained HTML scatter (no external requests, no CDN, no fonts
fetched) and a JSON of measurements for VECTOR_MAP_NOTES.md.

TOOLING. Chroma ships no offline explorer, so this builds the projection here:
cosine-normalised vectors -> PCA to 50 components -> UMAP to 2-D. The PCA step
is not cosmetic: UMAP on raw 1536-d needs far more memory than this machine has
spare, and reducing first is standard practice that also speeds the neighbour
search up substantially.

WHAT IS MEASURED IN THE FULL SPACE, NOT THE PICTURE
---------------------------------------------------
A 2-D projection distorts distance, so every claim in the notes is measured on
the real vectors and the map is only the lens for seeing it:

  script separation   of each chunk's k nearest neighbours, what fraction share
                      its script (Devanagari vs Latin). High purity means the
                      model is clustering by LANGUAGE rather than by TOPIC --
                      the English-to-Devanagari retrieval weakness, quantified.
  bucket coherence    same purity test for chapter buckets: do chunks sharing a
                      chapter actually sit together?
  source domination   per chapter bucket, the share held by its largest source
  quarantine check    confirms the fabricated and archived rows are absent
"""
from __future__ import annotations

import argparse
import collections
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

ROOT = Path(__file__).resolve().parent
CHROMA = ROOT / "kb3" / "chroma"
REGISTRY = ROOT / "kb_audit" / "source_registry.yaml"
STORES = {"v2-openai": "udaypur_kb_v2_openai", "v2": "udaypur_kb_v2", "v1": "udaypur_kb"}
DEVA = re.compile(r"[ऀ-ॿ]")
K = 15


def fetch(collection):
    import chromadb
    col = chromadb.PersistentClient(path=str(CHROMA)).get_collection(collection)
    n = col.count()
    print(f"{collection}: {n} vectors")
    ids, docs, metas, V = [], [], [], None
    step = 2000
    got_all = col.get(limit=n + 10, include=["documents", "metadatas", "embeddings"])
    ids = got_all["ids"]
    docs = got_all["documents"]
    metas = got_all["metadatas"]
    V = np.asarray(got_all["embeddings"], dtype=np.float32)
    return ids, docs, metas, V


def knn_purity(V, labels, k=K, block=512):
    """For each row, the share of its k nearest neighbours carrying the same label.

    Cosine on L2-normalised rows. Blocked so the full 10k x 10k similarity matrix
    is never held at once.
    """
    n = V.shape[0]
    lab = np.asarray(labels)
    out = np.zeros(n, dtype=np.float32)
    Vn = V / np.clip(np.linalg.norm(V, axis=1, keepdims=True), 1e-9, None)
    for s in range(0, n, block):
        e = min(s + block, n)
        sim = Vn[s:e] @ Vn.T
        for i in range(e - s):
            sim[i, s + i] = -2.0                      # exclude self
        idx = np.argpartition(-sim, k, axis=1)[:, :k]
        same = (lab[idx] == lab[s:e, None]).mean(axis=1)
        out[s:e] = same
    return out


def project(V, seed=11):
    """L2 normalise -> PCA 50 -> UMAP 2."""
    Vn = V / np.clip(np.linalg.norm(V, axis=1, keepdims=True), 1e-9, None)
    from sklearn.decomposition import PCA
    k = min(50, Vn.shape[1], Vn.shape[0] - 1)
    P = PCA(n_components=k, random_state=seed).fit_transform(Vn)
    print(f"  PCA -> {P.shape}, explains "
          f"{PCA(n_components=k, random_state=seed).fit(Vn).explained_variance_ratio_.sum():.1%}")
    import umap
    U = umap.UMAP(n_neighbors=15, min_dist=0.12, metric="cosine",
                  random_state=seed, verbose=False).fit_transform(P)
    return np.asarray(U, dtype=np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", choices=sorted(STORES), default="v2-openai")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    coll = STORES[a.store]

    import yaml
    reg = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    code = {s["source_id"]: s.get("code") or s["source_id"] for s in reg["sources"]}

    ids, docs, metas, V = fetch(coll)
    print(f"  vectors {V.shape} | finite {bool(np.isfinite(V).all())}")

    codes = [code.get(m.get("parent_source_id"), m.get("parent_source_id", "?")) for m in metas]
    stypes = [m.get("source_type") or "?" for m in metas]
    estat = [m.get("epistemic_status") or "?" for m in metas]
    quot = ["quotable" if m.get("is_quotable") else "not quotable" for m in metas]
    script = ["devanagari" if len(DEVA.findall(d or "")) > 20 else "latin" for d in docs]
    buckets = [(m.get("chapter_buckets") or "") for m in metas]
    first_bucket = [b.split(",")[0] if b else "(none)" for b in buckets]

    print("\n--- diagnostics in the FULL vector space ---")
    sp = knn_purity(V, script)
    bp = knn_purity(V, first_bucket)
    cp = knn_purity(V, codes)
    base_script = max(collections.Counter(script).values()) / len(script)
    print(f"  script purity  mean {sp.mean():.3f}  (chance {base_script:.3f})")
    for s in sorted(set(script)):
        m = np.asarray([x == s for x in script])
        print(f"      {s:12s} n={m.sum():5d}  own-script neighbours {sp[m].mean():.3f}")
    print(f"  bucket purity  mean {bp.mean():.3f}")
    print(f"  source purity  mean {cp.mean():.3f}")

    dom = {}
    for b in sorted({x for bs in buckets for x in bs.split(",") if x}):
        sel = [i for i, bs in enumerate(buckets) if b in bs.split(",")]
        c = collections.Counter(codes[i] for i in sel)
        top, n = c.most_common(1)[0]
        dom[b] = {"n": len(sel), "top": top, "share": round(n / max(1, len(sel)), 3),
                  "sources": len(c)}
    print("\n  source domination per chapter bucket (top source's share):")
    for b, d in sorted(dom.items(), key=lambda x: -x[1]["share"])[:8]:
        print(f"      {b:5s} n={d['n']:5d}  {d['top']:8s} {d['share']:5.0%}  "
              f"({d['sources']} sources)")

    fab = sum(1 for d in docs if "rāhīna" in (d or "") or "Island | Attribution" in (d or ""))
    ai = sum(1 for m in metas if m.get("parent_source_id") == "ai-derived")
    arch = sum(1 for m in metas if m.get("is_archived"))
    print(f"\n  quarantine check: fabricated-marker docs {fab} | ai-derived {ai} | archived {arch}")

    print("\nprojecting...")
    XY = project(V)

    # ---- compact payload --------------------------------------------------
    def vocab(vals):
        v = sorted(set(vals))
        ix = {x: i for i, x in enumerate(v)}
        return v, [ix[x] for x in vals]

    v_code, i_code = vocab(codes)
    v_type, i_type = vocab(stypes)
    v_stat, i_stat = vocab(estat)
    v_quot, i_quot = vocab(quot)
    v_scr, i_scr = vocab(script)
    v_buck, i_buck = vocab(first_bucket)
    allb = sorted({x for bs in buckets for x in bs.split(",") if x})
    bix = {b: i for i, b in enumerate(allb)}
    bmask = [[bix[x] for x in bs.split(",") if x] for bs in buckets]

    pay = {
        "collection": coll,
        "x": [round(float(v), 3) for v in XY[:, 0]],
        "y": [round(float(v), 3) for v in XY[:, 1]],
        "dims": {
            "source": {"vocab": v_code, "idx": i_code},
            "source_type": {"vocab": v_type, "idx": i_type},
            "epistemic_status": {"vocab": v_stat, "idx": i_stat},
            "is_quotable": {"vocab": v_quot, "idx": i_quot},
            "script": {"vocab": v_scr, "idx": i_scr},
            "chapter (first)": {"vocab": v_buck, "idx": i_buck},
        },
        "buckets": {"vocab": allb, "per": bmask},
        "text": [(d or "")[:200] for d in docs],
        "ids": ids,
        "purity": {"script": [round(float(x), 2) for x in sp],
                   "bucket": [round(float(x), 2) for x in bp]},
    }
    out = Path(a.out or f"VECTOR_MAP_{a.store.replace('-', '_')}.html")
    out.write_text(render(pay), encoding="utf-8")
    print(f"\nwrote {out}  ({out.stat().st_size/1e6:.1f} MB) — open it in a browser")

    stats = {
        "collection": coll, "n": len(ids),
        "script_purity_mean": float(sp.mean()),
        "script_chance": float(base_script),
        "script_by_group": {s: float(sp[np.asarray([x == s for x in script])].mean())
                            for s in sorted(set(script))},
        "script_counts": dict(collections.Counter(script)),
        "bucket_purity_mean": float(bp.mean()),
        "source_purity_mean": float(cp.mean()),
        "domination": dom,
        "fabricated_docs": fab, "ai_derived": ai, "archived": arch,
    }
    p = ROOT / "kb_audit" / f"vector_map_{a.store.replace('-', '_')}.json"
    p.write_text(json.dumps(stats, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {p}")
    return 0


def render(pay):
    """One self-contained file: no network, no CDN, system fonts only."""
    data = json.dumps(pay, ensure_ascii=False, separators=(",", ":"))
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Vector Map</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{--bg:#faf8f4;--fg:#1d1b18;--mut:#6b6358;--line:#e0d9cc;--card:#fff;--accent:#8a5a2b}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#171614;--fg:#ece7df;--mut:#9c948a;--line:#2e2a25;--card:#1f1d1a;--accent:#d8a05e}}
:root[data-theme="dark"]{--bg:#171614;--fg:#ece7df;--mut:#9c948a;--line:#2e2a25;--card:#1f1d1a;--accent:#d8a05e}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
 font:14px/1.5 "Segoe UI",system-ui,-apple-system,"Nirmala UI","Noto Sans Devanagari",sans-serif}
header{padding:14px 16px;border-bottom:1px solid var(--line)}
h1{margin:0 0 2px;font-size:17px;letter-spacing:.01em}
.sub{color:var(--mut);font-size:12px}
.wrap{display:flex;gap:0;height:calc(100vh - 62px);min-height:460px}
#side{width:260px;flex:0 0 260px;border-right:1px solid var(--line);overflow:auto;padding:12px}
#main{flex:1;position:relative;min-width:0}
canvas{display:block;width:100%;height:100%;cursor:crosshair}
label{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);margin:12px 0 4px}
select,input{width:100%;padding:6px 8px;background:var(--card);color:var(--fg);
 border:1px solid var(--line);border-radius:6px;font:inherit}
#legend{margin-top:10px;max-height:46vh;overflow:auto}
.it{display:flex;align-items:center;gap:7px;padding:2px 3px;border-radius:5px;cursor:pointer;font-size:12px}
.it:hover{background:var(--card)}
.it.off{opacity:.33}
.sw{width:11px;height:11px;border-radius:3px;flex:0 0 11px}
.it .n{margin-left:auto;color:var(--mut);font-variant-numeric:tabular-nums;font-size:11px}
#tip{position:absolute;pointer-events:none;max-width:330px;background:var(--card);
 border:1px solid var(--line);border-radius:8px;padding:8px 10px;font-size:12px;
 box-shadow:0 6px 22px rgba(0,0,0,.17);opacity:0;transition:opacity .08s}
#tip b{color:var(--accent)}
#tip .t{color:var(--mut);margin-top:4px;max-height:140px;overflow:hidden}
.row{display:flex;gap:6px;margin-top:8px}
button{flex:1;padding:5px;background:var(--card);color:var(--fg);border:1px solid var(--line);
 border-radius:6px;font:inherit;font-size:12px;cursor:pointer}
button:hover{border-color:var(--accent)}
.note{margin-top:14px;padding-top:10px;border-top:1px solid var(--line);color:var(--mut);font-size:11px}
@media (max-width:760px){.wrap{flex-direction:column;height:auto}
 #side{width:100%;flex:none;border-right:none;border-bottom:1px solid var(--line)}
 #main{height:66vh}}
</style></head><body>
<header><h1>Udaypur knowledge base &mdash; vector map</h1>
<div class="sub" id="hdr"></div></header>
<div class="wrap">
 <div id="side">
  <label for="dim">Colour by</label><select id="dim"></select>
  <label for="q">Search text</label><input id="q" placeholder="e.g. Udaye&#347;vara">
  <div class="row"><button id="all">All</button><button id="none">None</button></div>
  <div id="legend"></div>
  <div class="note">A 2-D projection is lossy: distances are approximate and
   apparent clusters can mislead. Use it to form questions, then check them
   against the store.</div>
 </div>
 <div id="main"><canvas id="c"></canvas><div id="tip"></div></div>
</div>
<script id="payload" type="application/json">__DATA__</script>
<script>
const P=JSON.parse(document.getElementById('payload').textContent);
const N=P.x.length;
document.getElementById('hdr').textContent=
 P.collection+' \\u00b7 '+N.toLocaleString()+' chunks \\u00b7 PCA 50 \\u2192 UMAP 2-D';
const PAL=['#4e79a7','#f28e2b','#e15759','#76b7b2','#59a14f','#edc948','#b07aa1','#ff9da7',
 '#9c755f','#bab0ac','#1f78b4','#a6cee3','#33a02c','#b2df8a','#fb9a99','#fdbf6f',
 '#cab2d6','#6a3d9a','#ffff99','#b15928','#8dd3c7','#bebada','#fb8072','#80b1d3',
 '#fdb462','#b3de69','#fccde5','#d9d9d9'];
const dimNames=Object.keys(P.dims);
const sel=document.getElementById('dim');
dimNames.forEach(d=>{const o=document.createElement('option');o.value=d;o.textContent=d;sel.append(o)});
sel.value=dimNames.includes('source')?'source':dimNames[0];
let cur=sel.value, hidden=new Set(), query='';
const cv=document.getElementById('c'), ctx=cv.getContext('2d'), tip=document.getElementById('tip');
let W=0,H=0,DPR=1,minx,maxx,miny,maxy;
function bounds(){minx=Math.min(...P.x);maxx=Math.max(...P.x);miny=Math.min(...P.y);maxy=Math.max(...P.y);
 const px=(maxx-minx)*0.04,py=(maxy-miny)*0.04;minx-=px;maxx+=px;miny-=py;maxy+=py;}
bounds();
function resize(){DPR=window.devicePixelRatio||1;const r=cv.getBoundingClientRect();
 W=Math.max(1,r.width);H=Math.max(1,r.height);cv.width=W*DPR;cv.height=H*DPR;
 ctx.setTransform(DPR,0,0,DPR,0,0);draw();}
const sx=v=>(v-minx)/(maxx-minx)*W, sy=v=>H-(v-miny)/(maxy-miny)*H;
function visible(i){
 const d=P.dims[cur];
 if(hidden.has(d.vocab[d.idx[i]]))return false;
 if(query&&!P.text[i].toLowerCase().includes(query))return false;
 return true;}
function draw(){
 ctx.clearRect(0,0,W,H);
 const d=P.dims[cur];
 ctx.globalAlpha=.30;ctx.fillStyle=getComputedStyle(document.body).color;
 for(let i=0;i<N;i++){if(visible(i))continue;
  ctx.fillRect(sx(P.x[i])-1,sy(P.y[i])-1,2,2);}
 ctx.globalAlpha=.85;
 for(let i=0;i<N;i++){if(!visible(i))continue;
  ctx.fillStyle=PAL[d.idx[i]%PAL.length];
  ctx.beginPath();ctx.arc(sx(P.x[i]),sy(P.y[i]),2.4,0,6.2832);ctx.fill();}
 ctx.globalAlpha=1;}
function legend(){
 const d=P.dims[cur],cnt={};
 for(let i=0;i<N;i++){const k=d.vocab[d.idx[i]];cnt[k]=(cnt[k]||0)+1;}
 const box=document.getElementById('legend');box.innerHTML='';
 Object.keys(cnt).sort((a,b)=>cnt[b]-cnt[a]).forEach(k=>{
  const row=document.createElement('div');row.className='it'+(hidden.has(k)?' off':'');
  const ci=d.vocab.indexOf(k);
  row.innerHTML='<span class="sw" style="background:'+PAL[ci%PAL.length]+'"></span>'+
   '<span>'+k.replace(/&/g,'&amp;').replace(/</g,'&lt;')+'</span><span class="n">'+cnt[k]+'</span>';
  row.onclick=()=>{hidden.has(k)?hidden.delete(k):hidden.add(k);legend();draw();};
  box.append(row);});}
sel.onchange=()=>{cur=sel.value;hidden.clear();legend();draw();};
document.getElementById('q').oninput=e=>{query=e.target.value.toLowerCase();draw();};
document.getElementById('all').onclick=()=>{hidden.clear();legend();draw();};
document.getElementById('none').onclick=()=>{const d=P.dims[cur];d.vocab.forEach(v=>hidden.add(v));legend();draw();};
cv.onmousemove=e=>{
 const r=cv.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top;
 let best=-1,bd=100;
 for(let i=0;i<N;i++){if(!visible(i))continue;
  const dx=sx(P.x[i])-mx,dy=sy(P.y[i])-my,dd=dx*dx+dy*dy;
  if(dd<bd){bd=dd;best=i;}}
 if(best<0){tip.style.opacity=0;return;}
 const parts=dimNames.map(n=>n+': <b>'+P.dims[n].vocab[P.dims[n].idx[best]]+'</b>');
 tip.innerHTML=parts.join('<br>')+
  '<div class="t">'+P.text[best].replace(/&/g,'&amp;').replace(/</g,'&lt;')+'</div>';
 tip.style.opacity=1;
 const tw=tip.offsetWidth,th=tip.offsetHeight;
 tip.style.left=Math.min(mx+14,W-tw-8)+'px';
 tip.style.top=Math.max(4,Math.min(my+14,H-th-8))+'px';};
cv.onmouseleave=()=>{tip.style.opacity=0;};
window.addEventListener('resize',resize);
legend();resize();
</script></body></html>
""".replace("__DATA__", data.replace("</", "<\\/"))


if __name__ == "__main__":
    raise SystemExit(main())
