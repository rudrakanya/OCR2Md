#!/usr/bin/env python3
"""
config.py — every tunable in the pipeline, in one versioned place.

v1 scattered its constants across module bodies: ABS_FLOOR in make_evidence,
MAX_CHARS in build_kb, SECTION_MAX_TOKENS in draft_chapter. That is fine while
a human is the only one changing them, and useless the moment you want to sweep
configurations and attribute a metrics run to the settings that produced it.

Here the settings are data. A config is a plain dict tree with a stable hash;
the hash is folded into the KB stamp, so an evidence pack, a draft and a metrics
row all carry the identity of the configuration they came from. `eval/ablate.py`
sweeps variants by overlaying dicts, never by editing code.

    from config import CFG
    CFG.retrieval.rerank_floor          # attribute access
    CFG["retrieval"]["rerank_floor"]    # or subscript

    from config import load, overlay
    cfg = overlay(CFG, {"retrieval": {"rerank_floor": 0.42}})
    cfg.hash()                          # differs from CFG.hash()

Overrides, in increasing precedence:
    1. the DEFAULTS below
    2. config.json in the project root, if present
    3. the file named by PIPELINE_CONFIG
    4. an explicit overlay dict (used by the ablation harness)

CLI:
    python config.py              # print the resolved config and its hash
    python config.py --diff       # show only what differs from DEFAULTS
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path

# Load .env here, not in each module that happens to need a key.
#
# This is the one module every other module imports, which makes it the only
# place guaranteed to run before anything reads os.environ. Leaving it to
# individual modules is how JINA_AI_API_KEY sat correctly in .env while
# rerank.py reported "no hosted reranker key found" and silently fell back to a
# backend three orders of magnitude slower — a missing key and an unloaded key
# are indistinguishable at the point of use.
try:
    from dotenv import load_dotenv

    load_dotenv()
    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)
except ImportError:                    # dotenv is optional; real env vars still work
    pass

CONFIG_VERSION = "2.0"

DEFAULTS = {
    "version": CONFIG_VERSION,

    # ---- corpus and chunking (build_kb.py) --------------------------------
    "chunking": {
        "max_chars": 1800,
        "min_chars": 200,
        "overlap_frac": 0.15,
        "min_flush_frac": 0.60,
        "cleaner": "md_clean/1",
        # Bilingual sources carry Sanskrit/Hindi and English line by line.
        # Below this many Latin characters the split is not attempted.
        "min_latin_for_split": 200,
    },

    # ---- embedding --------------------------------------------------------
    "embedding": {
        "model": "mistral-embed",
        "batch_tokens": 12000,
        "batch_items": 64,
        # §2.2 — embed chunks with an LLM-written situating preamble.
        #
        # Off by default, deliberately. It is the plan's highest-leverage change
        # to chunk quality, but it costs a full generation pass over 9,467
        # chunks (an overnight run) and invalidates every downstream artefact at
        # once, so it belongs to Phase 2 with a measured Recall@20 behind it —
        # not to the first run that has to produce chapters.
        #     python contextualize.py --all      then    python build_kb.py --force
        "contextualize": False,
    },

    # ---- comprehension layer (§2) ----------------------------------------
    "comprehension": {
        "model": "mistral-large-latest",
        "dossier_summary_words": 400,
        "section_summary_words": 60,
        # A dossier reads the source in windows this wide (characters).
        "read_window_chars": 60000,
        "preamble_max_sentences": 3,
        # §2.2 risk control: a preamble may only restate what is already in the
        # dossier, the heading trail, or the chunk. Never disable this.
        "enforce_no_new_facts": True,
    },

    # ---- retrieval funnel (§3) -------------------------------------------
    "retrieval": {
        "queries_per_subtopic": 5,
        "dense_k": 30,              # per query
        "sparse_k": 30,             # per query
        "entity_k": 30,             # per sub-topic
        "rrf_k": 60,
        "rrf_weights": {"dense": 1.0, "sparse": 1.0, "entity": 1.0},
        # How many survive fusion into the reranker.
        #
        # §3.5 estimated "~11k pairs per full run — minutes on CPU". Measured on
        # this machine (8 threads, bge-reranker-v2-m3, max_length 512) it is
        # 3.2 s/pair, so the plan's 120 candidates x 93 sub-topics would be
        # ~10 hours per retrieval pass. 48 keeps a full pass near 4 hours, and
        # the score cache makes every pass after the first nearly free.
        # Raise it if you move to GPU, where the original 120 is cheap.
        "rerank_candidates": 48,
        # §3.4 — replaces v1's ABS_FLOOR. Still provisional: it must be
        # calibrated on the gold set, and `eval/calibrate.py` overwrites it.
        #
        # 0.55 is not a guess, though. bge-reranker-v2-m3 emits a logit, and
        # sigmoid(0) = 0.5 is its "no relationship" resting point. Negative
        # controls against this corpus confirm it: "Norwegian salmon export
        # quotas" tops out at 0.5005 and "JavaScript async await" at 0.5001,
        # while a strong on-topic query reaches 0.7206. So the noise band is
        # 0.50-0.51 and a floor below that (the 0.30 first written here) would
        # admit literally everything — the exact failure the floor exists to
        # prevent.
        # The two backends emit scores on different scales, so they do NOT share
        # a floor. Applying one's calibrated floor to the other is a silent way
        # to lose the empty-pack guarantee, so retrieve.py looks the floor up by
        # the backend that actually ran.
        #   bge  sigmoid of a logit; 0.50 is "no relationship". Negative controls
        #        ("Norwegian salmon export quotas") top out at 0.5005 against
        #        this corpus, a strong on-topic query reaches 0.7206.
        #   llm  the rubric's own 0-100 bands over 100. 0.40 sits at the top of
        #        "related background", below "substantially relevant" (0.70).
        #   hosted  jina-reranker-v2 spreads scores across nearly the whole range:
        #           nonsense tops out at 0.053, a thin-but-real sub-topic at 0.315,
        #           a strong on-topic query at 0.868. 0.20 sits well clear of the
        #           noise band and below genuinely thin coverage, which must be
        #           reported as THIN rather than silently emptied.
        "rerank_floor_by_backend": {"hosted": 0.20, "bge": 0.55, "llm": 0.40, "none": 0.0},
        "rerank_floor": 0.55,           # fallback when a backend has no entry
        "rerank_floor_calibrated": False,
        # ...and within this of the sub-topic's best hit. Per-backend for the
        # same reason the floor is: an absolute margin of 0.15 is mild on bge's
        # compressed 0.50-0.72 band and brutal on jina's 0.03-0.87 spread, where
        # it would cut everything below the top two or three passages.
        "rel_margin_by_backend": {"hosted": 0.45, "bge": 0.15, "llm": 0.25, "none": 0.15},
        "rel_margin": 0.15,
        "keep_per_sub": 10,
        "source_cap": 0.50,
        "source_cap_min": 3,
        "thin_keep": 3,
        "thin_score": 0.35,         # on reranker scale, not cosine
        # §3.7 — strongest passages at the head and tail of the pack.
        "lost_in_middle_reorder": True,
        # Editorial (§3.2): the Hindi original is retrievable as corroboration
        # of its English translation. The pair counts as one source against the
        # diversity cap, so a sub-topic cannot be filled by the same testimony
        # twice in two languages.
        "translation_pairs": [
            ["Jagta_Hua_Kasba_OCR_text.md", "Jagta_Hua_Kasba_EN.md"],
            ["Raja_Bhoj_Aur_Parmarkaleen_EN.md", "bhojdev.md"],
        ],
    },

    # ---- reranking (§3.5) -------------------------------------------------
    "rerank": {
        # "llm" (Mistral listwise, parallel) | "bge" (local cross-encoder) | "none"
        #
        # Default is "llm" on measured grounds: bge runs at 3.2 s/pair on this
        # machine's CPU (~4 h per full pass), where the listwise LLM backend
        # judges 10 passages per call and finishes the same pass in minutes.
        # Switch to "bge" on a GPU box, or when the ablation harness needs
        # deterministic scores to compare configurations.
        "backend": "hosted",
        # v2-m3 is kept over the ~3x faster bge-reranker-base because
        # multilingual capability is the deciding factor for a corpus carrying
        # Devanagari, IAST and transliterated Sanskrit (§3.5, §8).
        "bge_model": "BAAI/bge-reranker-v2-m3",
        "bge_batch": 16,
        # 512, not 1024: a 1800-char chunk is ~450 tokens, so 512 covers a whole
        # passage, and the cost is quadratic in length for no benefit.
        "bge_max_length": 512,
        # Persist scores so re-runs, ablations and calibration sweeps do not
        # re-pay CPU inference for pairs already judged.
        "cache": True,
        "llm_model": "mistral-large-latest",
        "llm_group": 10,            # passages judged per listwise call
        "llm_workers": 8,           # windows judged concurrently
        # Hosted cross-encoder (§3.5 cloud option). Provider is auto-detected
        # from whichever of COHERE_API_KEY / JINA_API_KEY / VOYAGE_API_KEY is
        # set; override here to pin one.
        "hosted_provider": "jina",
        "hosted_model": None,
        "hosted_batch": 100,
        # If the chosen backend is unavailable, fall through in this order.
        # An unavailable reranker must never silently become "no floor".
        "fallback": ["bge", "llm", "none"],
    },

    # ---- generation (§5.1) ------------------------------------------------
    "generation": {
        "model": "mistral-large-latest",
        "words_per_subtopic": 800,
        "min_words": 4000,
        "max_words": 9000,
        "section_max_tokens": 4000,
        "continue_max_tokens": 2000,
        "stitch_token_ratio": 2.2,   # budget = words_in * ratio + 400
        "stitch_token_floor": 400,
        "temperature": 0.4,
        "workers": 4,
        "evidence_share": 0.25,
        "style_exemplars": 3,        # §5.3 step 4, voice anchors per section
    },

    # ---- verification gate (§5) ------------------------------------------
    "verify": {
        "enabled": True,
        "model": "mistral-large-latest",
        "max_repairs": 2,
        "claims_per_call": 12,
        # A repair is a revision, not a redraft: v1 measured a 59% overshoot and
        # invented comparanda when an editing pass was given a free budget.
        "repair_token_ratio": 1.3,
        # Unsupported claims still standing after max_repairs are cut.
        "cut_unsupported": True,
        # A repair adding more markers than this is rejected and the previous
        # text kept. The gate exists to make a chapter trustworthy, not to
        # perforate it: the first unbounded run produced 133 markers in 7,483
        # words, one every 56 words, including one inside a heading.
        "max_gaps_per_section": 6,
        "gap_marker": "[GAP — not in sources]",
    },

    # ---- evaluation (§4) --------------------------------------------------
    "eval": {
        "judge_model": "mistral-large-latest",
        "judge_prompt_version": "v2.0",
        "bootstrap_samples": 2000,   # for confidence intervals
        "ci": 0.95,
        "recall_k": [10, 20, 50],
        "randomize_candidate_order": True,
    },
}


class Config(dict):
    """A dict that also allows attribute access and knows its own hash."""

    def __getattr__(self, name):
        try:
            v = self[name]
        except KeyError as e:
            raise AttributeError(name) from e
        return Config(v) if isinstance(v, dict) else v

    def hash(self):
        """Stable short hash of the whole tree — folded into the KB stamp."""
        blob = json.dumps(self, sort_keys=True, ensure_ascii=False, default=str)
        return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:12]

    def section_hash(self, *names):
        """Hash of selected sections only.

        Rebuilding the index should not be forced by a change to, say, the
        drafting temperature. build_kb.py fingerprints on
        section_hash('chunking', 'embedding', 'comprehension').
        """
        sub = {n: self.get(n) for n in names}
        blob = json.dumps(sub, sort_keys=True, ensure_ascii=False, default=str)
        return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:12]


def overlay(base, *patches):
    """Deep-merge patches over a base config, returning a new Config."""
    out = copy.deepcopy(dict(base))

    def merge(dst, src):
        for k, v in src.items():
            if isinstance(v, dict) and isinstance(dst.get(k), dict):
                merge(dst[k], v)
            else:
                dst[k] = copy.deepcopy(v)

    for p in patches:
        if p:
            merge(out, p)
    return Config(out)


def load(path=None):
    """Resolve the config from DEFAULTS + config.json + $PIPELINE_CONFIG + path."""
    patches = []
    # Empty strings would become Path('.') — a directory that exists, which is
    # why this tests is_file() rather than exists().
    for raw in ("config.json", os.environ.get("PIPELINE_CONFIG", ""), path or ""):
        if not raw:
            continue
        cand = Path(raw)
        if cand.is_file():
            patches.append(json.loads(cand.read_text(encoding="utf-8")))
    cfg = overlay(DEFAULTS, *patches)
    if cfg.get("version") != CONFIG_VERSION:
        print(f"WARNING: config version {cfg.get('version')} != {CONFIG_VERSION}; "
              f"settings may have moved.")
    return cfg


def diff(cfg, base=None):
    """What differs from DEFAULTS — the useful thing to print in a results file."""
    base = base if base is not None else DEFAULTS
    out = {}
    for k, v in cfg.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            d = diff(v, base[k])
            if d:
                out[k] = d
        elif base.get(k) != v:
            out[k] = v
    return out


CFG = load()


def main():
    ap = argparse.ArgumentParser(description="Show the resolved pipeline config")
    ap.add_argument("--diff", action="store_true", help="only what differs from DEFAULTS")
    ap.add_argument("--section", help="print one section")
    args = ap.parse_args()

    cfg = load()
    body = diff(cfg) if args.diff else cfg
    if args.section:
        body = body.get(args.section, {})
    print(json.dumps(body, indent=2, ensure_ascii=False))
    print(f"\nconfig hash: {cfg.hash()}   "
          f"index sections: {cfg.section_hash('chunking', 'embedding', 'comprehension')}")


if __name__ == "__main__":
    main()
