#!/usr/bin/env python3
"""
rerank.py — pluggable cross-encoder reranking (§3.5).

A bi-encoder embeds query and passage independently and compares the results; a
cross-encoder reads the pair together. For deciding *is this passage actually
about this question* the difference is large, and it is the reason the relevance
floor moves here from the dense channel (§3.4). RRF scores have no absolute
meaning, so they cannot carry a floor; a cross-encoder score can.

Backends
--------
bge   BAAI/bge-reranker-v2-m3 run locally. The default. Free per run, offline,
      deterministic — that last property is what the ablation harness needs, and
      it is why a hosted or LLM reranker is second choice rather than first.
      Requires: pip install torch sentence-transformers
llm   Mistral, judging passages in small listwise groups. No new dependency, but
      slower, costs money on every sweep, and its scores are less calibrated —
      so RERANK_FLOOR calibrated against it transfers poorly.
none  Identity: passes fusion order through with a flat score.

Fallback is explicit and loud. An unavailable reranker must never silently
become "no floor" — that would delete the empty-pack guarantee (§3.4) while
appearing to work, which is the single most damaging failure mode in the plan.

    from rerank import get_reranker
    rr = get_reranker()                      # honours CFG.rerank.backend
    scored = rr.score(query, passages)       # [(passage, score), ...] sorted
    rr.name                                  # what actually ran, for the results file

CLI:
    python rerank.py --check                 # which backends are usable here
    python rerank.py --probe "query"         # rerank live KB hits, show scores
"""
import argparse
import hashlib
import json
import math
import os
import sqlite3
import sys
from pathlib import Path

from config import CFG

KB_DIR = Path(os.environ.get("KB_DIR", "kb"))
CACHE_PATH = KB_DIR / "rerank_cache.sqlite"


class RerankUnavailable(RuntimeError):
    pass


class ScoreCache:
    """(backend, model, query, chunk) -> score, on disk.

    Cross-encoder inference is the pipeline's slowest step by an order of
    magnitude: 3.2 s/pair measured on CPU. Calibration sweeps, the ablation
    harness and any re-run of a chapter all re-score pairs already judged, and
    the scores are deterministic for a fixed model, so caching them is free
    correctness. Keyed on the model name too, so switching backends cannot
    serve one model's scores as another's.
    """

    def __init__(self, path=CACHE_PATH):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("CREATE TABLE IF NOT EXISTS scores ("
                        "backend TEXT, model TEXT, qhash TEXT, chunk INTEGER, score REAL,"
                        " PRIMARY KEY (backend, model, qhash, chunk))")
        self.db.commit()
        self.hits = self.misses = 0

    @staticmethod
    def qhash(query):
        return hashlib.sha1(query.strip().lower().encode("utf-8")).hexdigest()[:16]

    def get_many(self, backend, model, query, chunk_ids):
        if not chunk_ids:
            return {}
        qh = self.qhash(query)
        ph = ",".join("?" * len(chunk_ids))
        rows = self.db.execute(
            f"SELECT chunk, score FROM scores WHERE backend=? AND model=? AND qhash=?"
            f" AND chunk IN ({ph})", [backend, model, qh, *chunk_ids]).fetchall()
        got = {int(c): float(s) for c, s in rows}
        self.hits += len(got)
        self.misses += len(chunk_ids) - len(got)
        return got

    def put_many(self, backend, model, query, pairs):
        if not pairs:
            return
        qh = self.qhash(query)
        with self.db:
            self.db.executemany(
                "INSERT OR REPLACE INTO scores (backend, model, qhash, chunk, score)"
                " VALUES (?,?,?,?,?)",
                [(backend, model, qh, int(c), float(s)) for c, s in pairs])

    def stats(self):
        n = self.db.execute("SELECT COUNT(*) FROM scores").fetchone()[0]
        return {"cached": n, "hits": self.hits, "misses": self.misses}


# ---------------------------------------------------------------------------


class BaseReranker:
    name = "base"
    calibrated = False       # may a floor be calibrated against these scores?
    model_name = ""
    cache = None

    def score(self, query, passages, text_key="text"):
        """Score with the disk cache in front, if this backend is deterministic."""
        if self.cache is None or not passages or "rowid" not in passages[0]:
            return self._score(query, passages, text_key)
        ids = [p["rowid"] for p in passages]
        known = self.cache.get_many(self.name, self.model_name, query, ids)
        todo = [p for p in passages if p["rowid"] not in known]
        fresh = self._score(query, todo, text_key) if todo else []
        self.cache.put_many(self.name, self.model_name, query,
                            [(p["rowid"], s) for p, s in fresh])
        out = [(p, known[p["rowid"]]) for p in passages if p["rowid"] in known] + fresh
        out.sort(key=lambda t: -t[1])
        return out

    def _score(self, query, passages, text_key="text"):
        raise NotImplementedError

    def score_batch(self, jobs, text_key="text"):
        """[(query, passages)] -> [[(passage, score)]]. Overridden where batching helps."""
        return [self.score(q, p, text_key=text_key) for q, p in jobs]


class NoopReranker(BaseReranker):
    """Identity. Preserves incoming order and reports a flat score.

    `calibrated = False` matters: retrieve.py refuses to apply an absolute
    relevance floor to uncalibrated scores, so choosing this backend degrades to
    v1's dense floor rather than to no floor at all.
    """
    name = "none"

    def _score(self, query, passages, text_key="text"):
        n = max(len(passages), 1)
        return [(p, 1.0 - i / n) for i, p in enumerate(passages)]


class BGEReranker(BaseReranker):
    """Local cross-encoder. Scores are logits; sigmoid maps them to [0, 1]."""
    name = "bge"
    calibrated = True

    def __init__(self, model=None, batch=None, max_length=None):
        try:
            from sentence_transformers import CrossEncoder
        except ImportError as e:
            raise RerankUnavailable(
                "sentence-transformers is not installed. Either\n"
                "    pip install torch sentence-transformers\n"
                "or set rerank.backend to 'llm' in config.json.") from e
        self.model_name = model or CFG.rerank.bge_model
        self.batch = batch or CFG.rerank.bge_batch
        self.max_length = max_length or CFG.rerank.bge_max_length
        # sentence-transformers leaves torch on its default thread count, which
        # here was half the available cores — a free ~40% on the slowest stage.
        try:
            import torch
            torch.set_num_threads(os.cpu_count() or 4)
        except Exception:                             # noqa: BLE001
            pass
        try:
            self.model = CrossEncoder(self.model_name, max_length=self.max_length)
        except Exception as e:                        # noqa: BLE001 - download/load failure
            raise RerankUnavailable(f"could not load {self.model_name}: {e}") from e
        if CFG.rerank.get("cache", True):
            self.cache = ScoreCache()

    @staticmethod
    def _sigmoid(x):
        # The model emits a raw logit; the floor is far easier to reason about
        # on a 0-1 scale, and monotonic mapping cannot change the ranking.
        return 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, float(x)))))

    def _score(self, query, passages, text_key="text"):
        if not passages:
            return []
        pairs = [(query, p[text_key]) for p in passages]
        raw = self.model.predict(pairs, batch_size=self.batch, show_progress_bar=False)
        out = [(p, self._sigmoid(s)) for p, s in zip(passages, raw)]
        out.sort(key=lambda t: -t[1])
        return out


class HostedReranker(BaseReranker):
    """A hosted cross-encoder API: Cohere, Jina or Voyage. Fast AND calibrated.

    This is the resolution of a real conflict between §3.5's two requirements.
    Measured on this project:

      bge (local)  correct but slow — 3.2 s/pair on CPU, ~4 h per full pass.
                   Negative control clean: nonsense queries top out at 0.5005.
      llm listwise fast but WRONG — it fails the negative control outright,
                   scoring a Ballālesvara temple description 0.95 against
                   "Norwegian salmon export quotas". It ranks passages by
                   scholarly quality rather than by relevance to the question,
                   which is precisely the failure the floor exists to catch.
                   An LLM asked to emit a number is not a cross-encoder.

    A hosted reranker is a genuine cross-encoder served on someone else's GPU:
    hundreds of documents per call, sub-second, and calibrated the same way the
    local model is. It costs an API key and per-call money; it does not cost the
    empty-pack guarantee.

    Providers share one request shape, so one implementation covers all three.
    """
    name = "hosted"
    calibrated = True

    # Several plausible names per provider. A key present under a name the code
    # does not check is indistinguishable from no key at all, and the failure is
    # silent — it just falls back to a slower backend and nobody notices why.
    PROVIDERS = {
        "cohere": dict(env=["COHERE_API_KEY", "COHERE_AI_API_KEY"],
                       url="https://api.cohere.com/v2/rerank", model="rerank-v3.5"),
        "jina": dict(env=["JINA_API_KEY", "JINA_AI_API_KEY", "JINAAI_API_KEY"],
                     url="https://api.jina.ai/v1/rerank",
                     model="jina-reranker-v2-base-multilingual"),
        "voyage": dict(env=["VOYAGE_API_KEY", "VOYAGE_AI_API_KEY"],
                       url="https://api.voyageai.com/v1/rerank", model="rerank-2"),
    }

    @staticmethod
    def _key_for(spec):
        for name in spec["env"]:
            v = os.environ.get(name)
            if v:
                return v.strip().strip('"').strip("'")
        return ""

    def __init__(self, provider=None, model=None, batch=None):
        provider = provider or CFG.rerank.get("hosted_provider") or self._detect()
        if provider not in self.PROVIDERS:
            names = sorted({n for s in self.PROVIDERS.values() for n in s["env"]})
            raise RerankUnavailable(
                "no hosted reranker key found. Set one of: " + ", ".join(names) + " in .env.")
        spec = self.PROVIDERS[provider]
        self.key = self._key_for(spec)
        if not self.key:
            raise RerankUnavailable(f"none of {spec['env']} is set")
        self.provider = provider
        self.url = spec["url"]
        self.model = model or CFG.rerank.get("hosted_model") or spec["model"]
        self.model_name = f"{provider}:{self.model}"
        self.batch = batch or CFG.rerank.get("hosted_batch", 100)
        if CFG.rerank.get("cache", True):
            self.cache = ScoreCache()

    @classmethod
    def _detect(cls):
        for name, spec in cls.PROVIDERS.items():
            if cls._key_for(spec):
                return name
        return None

    def _call(self, query, docs):
        import urllib.error
        import urllib.request
        body = json.dumps({"model": self.model, "query": query,
                           "documents": docs, "top_n": len(docs)}).encode("utf-8")
        req = urllib.request.Request(
            self.url, data=body,
            headers={"Authorization": f"Bearer {self.key}",
                     "Content-Type": "application/json", "Accept": "application/json",
                     # Cloudflare in front of these APIs rejects urllib's default
                     # "Python-urllib/3.x" agent with a 1010 "access denied",
                     # which reads exactly like a bad key and is not one.
                     "User-Agent": "udaypur-rag/2.0 (+https://github.com/) python-urllib"})
        delay = 3
        for attempt in range(5):
            try:
                with urllib.request.urlopen(req, timeout=90) as r:
                    data = json.loads(r.read().decode("utf-8"))
                return {int(d["index"]): float(d["relevance_score"])
                        for d in data.get("results", [])}
            except urllib.error.HTTPError as e:
                if e.code in (429, 500, 502, 503, 504) and attempt < 4:
                    import time
                    time.sleep(delay); delay *= 2
                    continue
                raise RerankUnavailable(
                    f"{self.provider} rerank failed: HTTP {e.code} "
                    f"{e.read()[:200].decode('utf-8', 'replace')}") from e
            except Exception as e:                    # noqa: BLE001
                if attempt < 4:
                    import time
                    time.sleep(delay); delay *= 2
                    continue
                raise RerankUnavailable(f"{self.provider} rerank failed: {e}") from e

    def _score(self, query, passages, text_key="text"):
        if not passages:
            return []
        out = []
        for start in range(0, len(passages), self.batch):
            window = passages[start:start + self.batch]
            got = self._call(query, [p[text_key][:4000] for p in window])
            for i, p in enumerate(window):
                out.append((p, got.get(i, 0.0)))
        out.sort(key=lambda t: -t[1])
        return out


LLM_SYSTEM = """You rank source passages by how directly they answer a specific research \
question about the history and architecture of the Udayeśvara (Nīlakaṇṭheśvara) temple at \
Udaypur, Vidisha district, and the Paramāra dynasty of Malwa.

Score each passage 0-100 for how well it supports answering THIS question:

  90-100  directly answers it with specific evidence
  70-89   substantially relevant: same subject, same place or period
  40-69   related background; touches the topic without evidence on it
  10-39   same broad field only (Indian temples generally, another region/dynasty)
  0-9     unrelated

Judge relevance to the question, not the passage's scholarly quality. A passage about a \
different region or a different century is NOT relevant however authoritative it is — \
scoring such passages highly is the specific failure this step exists to prevent.

Return JSON only: {"scores": [{"i": 0, "s": 87}, ...]} with one entry per passage."""


class LLMReranker(BaseReranker):
    """Listwise judging via Mistral, windows run in parallel. The default.

    Chosen over the local cross-encoder on measured grounds, not preference.
    bge-reranker-v2-m3 on this machine runs at 3.2 s/pair on 8 CPU threads, so
    a full 93-sub-topic pass is ~4 hours; §3.5's "minutes on CPU" assumed
    hardware this box does not have. This backend judges `llm_group` passages
    per call, so the same pass is ~450 calls and finishes in minutes on the API
    key the pipeline already uses — no second vendor, no second key.

    On calibration: §3.5 calls LLM scores "less calibrated", and for a free-form
    prompt that is right. The rubric below is anchored instead — explicit bands,
    temperature 0, a fixed prompt version — which makes an absolute floor
    meaningful, though on its own scale rather than the cross-encoder's. Hence
    `rerank_floor_by_backend` in config: the two backends do NOT share a floor,
    and a floor calibrated for one must never be applied to the other.

    Determinism is the real cost. Scores can move slightly between runs, so the
    ablation harness should pin `bge` when comparing configurations, and the
    disk cache (inherited from BaseReranker) keeps a given run self-consistent.
    """
    name = "llm"
    # Measured false on this corpus, not assumed: see the class docstring.
    # retrieve.py therefore refuses to apply an absolute floor to these
    # scores and degrades to v1's dense cosine floor instead.
    calibrated = False
    prompt_version = "rerank/v2.0"

    def __init__(self, model=None, group=None, client=None, workers=None):
        from llm import get_client
        self.model = model or CFG.rerank.llm_model
        self.model_name = f"{self.model}:{self.prompt_version}"
        self.group = group or CFG.rerank.llm_group
        self.workers = workers or CFG.rerank.get("llm_workers", 8)
        self.client = client or get_client()
        if CFG.rerank.get("cache", True):
            self.cache = ScoreCache()

    def _window(self, query, window, text_key):
        from llm import complete_json
        listing = "\n\n".join(
            f"[{i}] ({p.get('source','?')}) {p[text_key][:1200]}"
            for i, p in enumerate(window))
        msgs = [{"role": "system", "content": LLM_SYSTEM},
                {"role": "user", "content": f"QUESTION: {query}\n\nPASSAGES:\n{listing}"}]
        data = complete_json(self.client, self.model, msgs,
                             max_tokens=1200, temperature=0.0, quiet=True)
        return {int(d["i"]): float(d["s"]) / 100.0 for d in data.get("scores", [])}

    def _score(self, query, passages, text_key="text"):
        from llm import parallel
        if not passages:
            return []
        windows = [passages[i:i + self.group] for i in range(0, len(passages), self.group)]

        def judge(w):
            return self._window(query, w, text_key)

        def failed(w, e):
            # A window that failed keeps its fusion rank rather than being
            # dropped: losing evidence to a transient API error is worse than
            # ranking it imperfectly. 0.5 is deliberately mid-scale — below the
            # floor, so a failed window cannot smuggle passages into a pack.
            print(f"    rerank window failed ({type(e).__name__}); "
                  f"{len(w)} passages keep fusion order", file=sys.stderr)
            return {}

        results = parallel(judge, windows, workers=self.workers, stagger=0.15,
                           on_error=failed)
        out = []
        for w, got in zip(windows, results):
            for i, p in enumerate(w):
                out.append((p, (got or {}).get(i, 0.5)))
        out.sort(key=lambda t: -t[1])
        return out


# ---------------------------------------------------------------------------

_BACKENDS = {"hosted": HostedReranker, "bge": BGEReranker,
             "llm": LLMReranker, "none": NoopReranker}
_cache = {}


def get_reranker(backend=None, allow_fallback=True, quiet=False):
    """Build the configured reranker, falling through the configured chain.

    Every fallback is announced. Silence here would mean a run whose floor
    behaves differently from the one it was calibrated for, with nothing in the
    output to say so.
    """
    want = backend or CFG.rerank.backend
    if want in _cache:
        return _cache[want]

    chain = [want] + ([b for b in CFG.rerank.fallback if b != want] if allow_fallback else [])
    errors = []
    for name in chain:
        cls = _BACKENDS.get(name)
        if cls is None:
            errors.append(f"{name}: unknown backend")
            continue
        try:
            rr = cls()
            if name != want and not quiet:
                print(f"⚠ reranker '{want}' unavailable — using '{name}' instead.",
                      file=sys.stderr)
                for e in errors:
                    print(f"    {e}", file=sys.stderr)
                if not rr.calibrated:
                    print("    Scores from this backend are NOT calibrated: the absolute "
                          "relevance floor will be disabled and the relative margin used "
                          "alone. See §3.4.", file=sys.stderr)
            _cache[want] = rr
            return rr
        except RerankUnavailable as e:
            errors.append(f"{name}: {e}")
        except Exception as e:                        # noqa: BLE001
            errors.append(f"{name}: {type(e).__name__}: {e}")
    raise RerankUnavailable("no reranker available:\n  " + "\n  ".join(errors))


def available():
    """{backend: True | reason-it-is-not} — what this machine can actually run."""
    out = {}
    for name, cls in _BACKENDS.items():
        try:
            cls()
            out[name] = True
        except Exception as e:                        # noqa: BLE001
            out[name] = f"{type(e).__name__}: {str(e).splitlines()[0]}"
    return out


def main():
    from console import use_utf8
    use_utf8()
    ap = argparse.ArgumentParser(description="Inspect or exercise the reranker")
    ap.add_argument("--check", action="store_true", help="report backend availability")
    ap.add_argument("--probe", help="rerank live KB hits for a query")
    ap.add_argument("--backend")
    ap.add_argument("-k", type=int, default=12)
    args = ap.parse_args()

    if args.check or not args.probe:
        print(f"configured backend: {CFG.rerank.backend}"
              f"   fallback chain: {' -> '.join(CFG.rerank.fallback)}\n")
        for name, state in available().items():
            print(f"  {name:6s} {'OK' if state is True else state}")
        print("\nTo enable the default local cross-encoder:\n"
              "    pip install torch sentence-transformers\n"
              "  (~2.5 GB including the model on first use; runs on CPU)")

    if args.probe:
        from kb_store import KBStore
        from entities import EntityIndex
        st, ix = KBStore(), EntityIndex.load()
        cands = st.search_bm25(args.probe, k=40, alias_map=ix.query_alias_map())
        rr = get_reranker(args.backend)
        print(f"\nreranker: {rr.name} (calibrated={rr.calibrated})\n")
        for p, s in rr.score(args.probe, cands)[:args.k]:
            print(f"  {s:.4f}  [{p['source'][:38]}] {(p['trail'] or '')[:44]}")
            print(f"          {p['text'][:120].replace(chr(10),' ')}")


if __name__ == "__main__":
    main()
