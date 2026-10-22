"""Read-only retrieval wrapper for the drafting evidence map.

Reuses the project's own Store / LexicalIndex / RRF settings (src/retrieval.py)
but adds a `source_path` filter for the per-book sweep, and guarantees that
nothing under ./chroma_db is written:
  - query embeddings are cached in drafting/_tools/query_cache.sqlite3,
    not chroma_db/embed_cache.sqlite3;
  - the BM25 index is loaded from chroma_db/sidecar.bm25.pkl only if its stamp
    matches, otherwise built in memory and never pickled back.

Usage (from the project root):
  python drafting/_tools/kb.py run   <chapter>          # all passes in drafting/_runs/<chapter>_queries.json
  python drafting/_tools/kb.py more  <chapter> <pass> --book <source_path> --offset 5 --n 10
  python drafting/_tools/kb.py more  <chapter> <pass> --global --offset 40 --n 40
  python drafting/_tools/kb.py dump  <chapter> [--unjudged] [--limit N]   # chunk texts for reading
"""
from __future__ import annotations

import argparse
import json
import os
import pickle
import sys
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[2]))
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
os.environ["COLLECTION"] = "udaypur_corpus_openai_large"

from src import settings as st  # noqa: E402
from src.retrieval import LexicalIndex, rrf  # noqa: E402
from src.store import open_aligned  # noqa: E402
from src.textutil import tokenize_folded  # noqa: E402

TOOLS = ROOT / "drafting" / "_tools"
RUNS = ROOT / "drafting" / "_runs"
COLLECTION = "udaypur_corpus_openai_large"
GLOBAL_K = 40
BOOK_K = 5


class ReadOnlyLexical(LexicalIndex):
    def build(self, force: bool = False):
        from rank_bm25 import BM25Okapi
        ids, folded = self.store.folded_corpus()
        stamp = (len(ids), ids[0], ids[-1])
        if self.cache_path.exists():
            with self.cache_path.open("rb") as fh:
                cached = pickle.load(fh)
            if cached.get("stamp") == stamp:
                self.ids, self.bm25 = cached["ids"], cached["bm25"]
                return self
        self.ids, self.bm25 = ids, BM25Okapi([tokenize_folded(t) for t in folded])
        return self


class KB:
    def __init__(self):
        cfg = st.load()
        assert cfg["storage"]["collection"] == COLLECTION, cfg["storage"]["collection"]
        cfg["embedding"]["cache_path"] = str(TOOLS / "query_cache.sqlite3")
        cfg, self.store = open_aligned(cfg, verbose=False)
        cfg["embedding"]["cache_path"] = str(TOOLS / "query_cache.sqlite3")
        assert self.store.collection.name == COLLECTION
        self.cfg = cfg
        from src.embedder import get_embedder
        self.embedder = get_embedder(cfg)
        assert str(self.embedder.cache.path).startswith(str(TOOLS)), "cache must not live in chroma_db"
        self.lex = ReadOnlyLexical(self.store).build()
        got = self.store.collection.get(include=["metadatas"])
        self.meta = dict(zip(got["ids"], got["metadatas"]))
        self.by_source: dict[str, set[str]] = {}
        for cid, m in self.meta.items():
            self.by_source.setdefault(m["source_path"], set()).add(cid)
        self._qvec: dict[str, list[float]] = {}
        r = cfg["retrieval"]
        self.rrf_k = int(r["hybrid"].get("rrf_k", 60))
        self.w_d = float(r["hybrid"].get("weight_dense", 1.0))
        self.w_l = float(r["hybrid"].get("weight_lexical", 1.0))
        self.embed_calls = 0

    def qvec(self, q: str):
        if q not in self._qvec:
            self._qvec[q] = self.embedder.embed_queries([q])[0]
            self.embed_calls += 1
        return self._qvec[q]

    def ranked(self, q: str, depth: int, source: str | None = None) -> list[dict]:
        """Full RRF ranking (same formula as Retriever.search) down to `depth`."""
        where = {"source_path": source} if source else None
        n = depth if not source else min(depth, len(self.by_source[source]))
        dense = self.store.query(self.qvec(q), n, where=where)
        pool: dict[str, dict] = {}
        for i, d in enumerate(dense):
            pool[d["chunk_id"]] = {"chunk_id": d["chunk_id"], "dense_rank": i + 1,
                                   "dense": round(d["score"], 4), "lex_rank": None}
        allowed = self.by_source[source] if source else None
        for i, (cid, s) in enumerate(self.lex.search(q, depth, allowed)):
            h = pool.setdefault(cid, {"chunk_id": cid, "dense_rank": None, "dense": None})
            h["lex_rank"] = i + 1
        for h in pool.values():
            t = 0.0
            if h["dense_rank"]:
                t += self.w_d * rrf(h["dense_rank"], self.rrf_k)
            if h.get("lex_rank"):
                t += self.w_l * rrf(h["lex_rank"], self.rrf_k)
            if self.meta[h["chunk_id"]].get("is_duplicate"):
                t *= 0.5
            h["fused"] = t
            h["source_path"] = self.meta[h["chunk_id"]]["source_path"]
        out = sorted(pool.values(), key=lambda h: -h["fused"])
        for i, h in enumerate(out):
            h["rank"] = i + 1
        return out


def load_queries(ch: str) -> list[dict]:
    return json.loads((RUNS / f"{ch}_queries.json").read_text(encoding="utf-8"))["passes"]


def append(path: Path, rows: list[dict]):
    with path.open("a", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def cmd_run(kb: KB, ch: str):
    hits_path = RUNS / f"{ch}_hits.jsonl"
    if hits_path.exists():
        sys.exit(f"{hits_path} exists; refusing to overwrite")
    rows = []
    for p in load_queries(ch):
        g = kb.ranked(p["q"], max(GLOBAL_K, 50))[:GLOBAL_K]
        rows += [dict(h, pass_id=p["id"], scope="global") for h in g]
        for src in sorted(kb.by_source):
            b = kb.ranked(p["q"], 50, source=src)[:BOOK_K]
            rows += [dict(h, pass_id=p["id"], scope="book") for h in b]
    append(hits_path, rows)
    print(f"passes={len(load_queries(ch))} hits={len(rows)} unique={len({r['chunk_id'] for r in rows})} embed_calls={kb.embed_calls}")


def cmd_more(kb: KB, ch: str, pass_id: str, book: str | None, offset: int, n: int):
    p = next(p for p in load_queries(ch) if p["id"] == pass_id)
    depth = max(50, offset + n)
    res = kb.ranked(p["q"], depth, source=book)[offset:offset + n]
    scope = "book-deepen" if book else "global-deepen"
    rows = [dict(h, pass_id=pass_id, scope=scope) for h in res]
    append(RUNS / f"{ch}_hits.jsonl", rows)
    seen = judged_ids(ch)
    print(f"{scope} {pass_id} {book or ''} ranks {offset+1}-{offset+len(rows)}: "
          f"{len(rows)} hits, {sum(r['chunk_id'] not in seen for r in rows)} not yet judged")


def judged_ids(ch: str) -> set[str]:
    p = RUNS / f"{ch}_judgments.jsonl"
    if not p.exists():
        return set()
    return {json.loads(l)["chunk_id"] for l in p.read_text(encoding="utf-8").splitlines() if l.strip()}


def cmd_dump(kb: KB, ch: str, unjudged: bool, limit: int, source: str | None):
    hits = [json.loads(l) for l in (RUNS / f"{ch}_hits.jsonl").read_text(encoding="utf-8").splitlines()]
    order: list[str] = []
    for h in sorted(hits, key=lambda h: (h["source_path"], h["chunk_id"])):
        if h["chunk_id"] not in order:
            order.append(h["chunk_id"])
    done = judged_ids(ch) if unjudged else set()
    order = [c for c in order if c not in done and (not source or kb.meta[c]["source_path"] == source)]
    for cid in order[:limit]:
        m = kb.meta[cid]
        row = kb.store.sidecar_row(cid)
        print(f"===== {cid} | {m['source_path']} | p.{m.get('page_start')} | {m.get('heading_path','')}")
        print(row["text"])
    print(f"##### shown {min(limit, len(order))} of {len(order)} remaining")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "more", "dump"])
    ap.add_argument("chapter")
    ap.add_argument("pass_id", nargs="?")
    ap.add_argument("--book")
    ap.add_argument("--global", dest="glob", action="store_true")
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--unjudged", action="store_true")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--source")
    a = ap.parse_args()
    kb = KB()
    if a.cmd == "run":
        cmd_run(kb, a.chapter)
    elif a.cmd == "more":
        cmd_more(kb, a.chapter, a.pass_id, None if a.glob else a.book, a.offset, a.n)
    else:
        cmd_dump(kb, a.chapter, a.unjudged, a.limit, a.source)
