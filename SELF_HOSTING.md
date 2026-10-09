# Self-hosting plan — GPU box for Unlimited-OCR, Ollama for embeddings and chat

*Written 16 August 2026. Companion to `SYSTEM_DESIGN.md` (v1) and `SYSTEMDESIGN2.md` (v2).*

The immediate trigger is a spent Mistral allowance, but the useful framing is
broader: this pipeline currently depends on **one vendor for five different
jobs**, and any one of them going unavailable degrades the others in ways that
are hard to see. The last run proved it — verification calls failed on quota,
were misread as "unsupported", and 127 well-evidenced claims were deleted from
a chapter that reported itself 45% faithful.

So this is not only a cost exercise. Splitting the dependencies is also what
makes each failure legible.

---

## 1. What the pipeline actually depends on

Measured from the code, not assumed. There are **two** embedding call sites and
**five** model settings:

| Job | Config key | Current | Call site |
|---|---|---|---|
| Embedding (index) | `embedding.model` | `mistral-embed` | `build_kb.embed_all` |
| Embedding (query) | same | `mistral-embed` | `kb_search.embed_texts` ← used by `retrieve._embed` |
| Dossiers, contextualisation, entity + claim extraction, labelling | `comprehension.model` | `mistral-large-latest` | `llm.complete_json` |
| Chapter planning, drafting, editorial | `generation.model` | `mistral-large-latest` | `llm.complete` |
| Claim decomposition + entailment | `verify.model` | `mistral-large-latest` | `llm.complete_json` |
| Eval judges | `eval.judge_model` | `mistral-large-latest` | `llm.complete_json` |
| Reranking | `rerank.backend` | `hosted` → **Jina** | `rerank.HostedReranker` |
| Layout OCR | — | Unlimited-OCR | `ocr_layout.LayoutClient` |

Two things follow immediately.

**Reranking is already off Mistral.** The Jina key works and the hosted
cross-encoder is both fast (48 passages in 0.9 s) and calibrated. Leave it
alone.

**Embeddings are the smallest surface to move** — two functions — but moving
them alone only restores *retrieval*. Drafting, verification and labelling are
four separate settings all pointing at chat models, and they are where the bulk
of the token spend goes. A plan that fixes embeddings and stops has fixed the
cheap half.

---

## 2. Topology: one services box, two servers

Both Unlimited-OCR (via vLLM) and Ollama expose **OpenAI-compatible HTTP APIs**.
That is the whole reason this is cheap to adopt: `ocr_layout.py` already speaks
that protocol via `UNLIMITED_OCR_URL`, and the embedding shim needs ~80 lines.

```
┌─────────────────────────── GPU machine ───────────────────────────┐
│                                                                    │
│  vLLM container        :8000   baidu/Unlimited-OCR   (~8-10 GB)   │
│  ollama serve          :11434  bge-m3     (embeddings, ~1.2 GB)   │
│                                qwen3:8b   (chat, ~5-6 GB Q4)      │
└────────────────────────────────────────────────────────────────────┘
                                 ▲
                       LAN / SSH tunnel
                                 │
┌─────────────────────── this laptop (pipeline) ────────────────────┐
│  kb/ (SQLite + .npy) · book/ · chapter_drafts/ · git              │
│  UNLIMITED_OCR_URL=http://gpu-box:8000/v1                         │
│  OLLAMA_URL=http://gpu-box:11434/v1                               │
└────────────────────────────────────────────────────────────────────┘
```

### Where should the pipeline itself run?

**Recommendation: keep the pipeline on the laptop, models on the GPU box.**

The pipeline is I/O- and API-bound, not compute-bound. Its state — the SQLite
store, the embedding matrix, the evidence packs, the git repo — is small and
already here, and moving it invites the two copies to drift. The GPU box becomes
a stateless appliance you can rebuild without losing anything.

The exception is the **initial embedding of 9,467 chunks**. That is one large
batch job, and if the LAN is slow it is worth running `build_kb.py` *on* the GPU
box once and copying `kb/` back. After that, query embedding is a handful of
vectors per sub-topic and latency is irrelevant.

### VRAM budget

| Component | Precision | VRAM (estimate) |
|---|---|---|
| Unlimited-OCR (3B, ~500M active) | BF16 | **≥8 GB** (documented minimum) |
| bge-m3 embeddings (567M) | F16 | ~1.2 GB |
| qwen3:8b chat | Q4_K_M | ~5–6 GB |
| **All three resident** | | **~15 GB** |

On a **24 GB** card (4090, A5000, L4) all three sit comfortably. On **16 GB**
they fit but leave little headroom; on **12 GB or less**, run OCR *or* chat, not
both — Ollama's `keep_alive` will evict an idle model, which makes serial
operation workable without manual intervention.

These are estimates from published model sizes, not measurements on your card.
Check with `nvidia-smi` after loading and adjust before planning a long run.

---

## 3. Unlimited-OCR on the GPU box

Source: the [official vLLM recipe](https://recipes.vllm.ai/baidu/Unlimited-OCR).
`python ocr_layout.py --serve-help` prints the short version; this section is the
full procedure with verification at each step, because three of the settings are
mandatory in a way that fails *silently* rather than loudly.

### 3.1 Prerequisites

| Requirement | Note |
|---|---|
| GPU | **≥8 GB VRAM** is enough for BF16, per the recipe |
| Docker | **Required — not optional.** The architecture "is not yet in a stable pip wheel", so `pip install vllm` will not serve this model |
| NVIDIA Container Toolkit | Docker must be able to see the GPU |
| Disk | ~10 GB for the image plus ~7 GB for weights |

Verify the host before pulling anything:

```bash
nvidia-smi                                    # driver alive, VRAM free?
docker --version
docker run --rm --gpus all nvidia/cuda:12.4.0-base-ubuntu22.04 nvidia-smi
```

That third command is the one that matters. If it fails, Docker cannot reach the
GPU and vLLM will fall back or refuse — install the NVIDIA Container Toolkit
before going further.

### 3.2 Start the server

```bash
docker run -d --name unlimited-ocr \
  --gpus all --network host --ipc host --restart unless-stopped \
  vllm/vllm-openai:unlimited-ocr \
  baidu/Unlimited-OCR \
  --trust-remote-code \
  --logits_processors vllm.model_executor.models.unlimited_ocr:NGramPerReqLogitsProcessor \
  --no-enable-prefix-caching \
  --mm-processor-cache-gb 0
```

Every flag earns its place:

| Flag | Why |
|---|---|
| `--gpus all` | exposes the GPU to the container |
| `--ipc host` | vLLM's workers need shared memory; without it you get obscure crashes under load |
| `--network host` | binds :8000 on the host directly |
| `--restart unless-stopped` | survives reboots |
| `--trust-remote-code` | the architecture ships as custom modelling code |
| `--logits_processors …NGramPerReqLogitsProcessor` | **mandatory.** The recipe is explicit: without it, long documents *loop on coordinate tokens*. This is the flag people omit and then blame the model for |
| `--no-enable-prefix-caching` | required for this architecture |
| `--mm-processor-cache-gb 0` | disables the multimodal processor cache |

First start downloads ~7 GB of weights and takes several minutes. Watch it:

```bash
docker logs -f unlimited-ocr
# wait for: "Application startup complete" / "Uvicorn running on http://0.0.0.0:8000"
```

### 3.3 Verify the server — four checks, in order

Each catches a different failure, and they get progressively more specific.

**1. Is it alive?**
```bash
curl -s http://localhost:8000/health && echo "  health OK"
```

**2. Is it serving the right model?**
```bash
curl -s http://localhost:8000/v1/models | python -m json.tool
# expect an entry whose "id" is baidu/Unlimited-OCR
```

**3. Does it actually parse an image?** Uses the recipe's own test asset, so a
failure here is the server, not your document:
```bash
curl -s http://localhost:8000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "baidu/Unlimited-OCR",
    "messages": [{"role": "user", "content": [
      {"type": "text", "text": "<image>document parsing."},
      {"type": "image_url", "image_url": {"url": "https://huggingface.co/baidu/Unlimited-OCR/resolve/main/assets/baidu.png"}}
    ]}],
    "max_tokens": 8192,
    "temperature": 0.0,
    "skip_special_tokens": false,
    "vllm_xargs": {"ngram_size": 35, "window_size": 128}
  }' | python -m json.tool
```

**4. THE CRITICAL CHECK — are the layout markers present?**
```bash
# ...pipe the response above through:
grep -c '<|det|>'
```

If that returns **0**, the server is running and returning text, and the entire
reason for using this model is gone. It is the failure this document exists to
prevent: you get plausible OCR, notice nothing, and index a corpus with no layout
information in it. See §3.5.

From the repo, the equivalent one-liner:

```bash
setx UNLIMITED_OCR_URL http://gpu-box:8000/v1     # Windows; export on Linux/macOS
python ocr_layout.py --check                       # confirms it serves Unlimited-OCR
```

### 3.4 Run it against a real document

```bash
python ocr_layout.py "remaining pdf/bhojdev.pdf" --out kb/_layout --first 30 --last 32
```

Start with three pages, not the whole book. Then inspect what came back before
committing GPU hours:

```bash
python -c "
import json
recs=[json.loads(l) for l in open('kb/_layout/bhojdev.layout.jsonl',encoding='utf-8')]
import collections
k=collections.Counter(e['type'] for r in recs for e in r['elements'])
print('pages:', len(recs), '| seconds/page:', round(sum(r['seconds'] for r in recs)/len(recs),1))
print('element types:', dict(k))
print('with bboxes:', sum(1 for r in recs for e in r['elements'] if e['bbox']))
"
```

A healthy result shows several distinct element types (`title`, `text`, `table`,
`footer`, `page_number`) and bounding boxes on most of them. All-`text` with no
bboxes means the markers were stripped — go back to §3.5.

Then convert and re-index:

```bash
python ocr_layout.py --to-markdown kb/_layout/bhojdev.layout.jsonl
# copy the .md into "Udaypur Reference Markdown Files/", then:
python build_kb.py --force
python label_chunks.py --all
```

### 3.5 The three settings that fail silently

All three are already handled in `ocr_layout.LayoutClient`, but they are the
first thing to check when output looks wrong — and the recipe names the first
two as the near-universal cause of empty output.

| Setting | Symptom if wrong |
|---|---|
| `skip_special_tokens: false` | `<\|det\|>` markers stripped — plain OCR, no layout, **no error** |
| Literal `<image>` prompt prefix | empty output |
| `ngram_size=35`, `window_size=128` | long documents loop on coordinate tokens |

Use `window_size=1024` for multi-page and PDF input — `ocr_layout.py` switches to
it automatically under `--multi`.

### 3.6 Troubleshooting

| Symptom | Likely cause |
|---|---|
| Empty response | Missing `<image>` prefix, or `skip_special_tokens` left `True` |
| Text returns but no `<\|det\|>` | `skip_special_tokens` — the single most damaging failure, because nothing errors |
| Output repeats coordinates forever | The logits processor was not registered on the serve command |
| CUDA OOM at startup | Another process holds VRAM (`nvidia-smi`); or reduce `--max-model-len` |
| Container exits immediately | Docker cannot see the GPU — re-run the §3.1 toolkit check |
| Crashes under concurrent load | `--ipc host` missing |
| `ocr_layout.py --check` says NOT SERVING | `UNLIMITED_OCR_URL` points elsewhere, or the model id differs |

### 3.7 Expected throughput

Local CPU measured **322 s/page** on this laptop. A GPU should land in the low
single-digit seconds per page — **100–300× faster** — which would take the
335-page Skanda Purāṇa from a 30-hour job to roughly 10–20 minutes. That ratio is
extrapolated, not measured; §3.4 prints the real figure from a three-page run,
and that number should drive the plan.

It also **reverses the earlier CPU-era advice**. At 322 s/page, OCR was worth
reserving for pages where layout carries meaning. On GPU, **re-ingesting the
whole corpus becomes reasonable** — a few GPU-hours for *observed* structural
labels across all 25 sources instead of inferred ones. That is the single largest
quality upgrade available to the labeling layer, and Phase 1 in §8 exists to test
whether the observed labels actually differ enough to justify it.

---

## 4. Ollama for embeddings

### Model choice

The corpus is the deciding factor. It carries Devanagari, IAST diacritics and
transliterated Sanskrit, so an English-centric embedder is the wrong tool
regardless of its benchmark scores.

| Model | Params | Dims | Multilingual | Verdict |
|---|---|---|---|---|
| **bge-m3** | 567M | **1024** | 100+ languages, MIT | **Recommended** |
| qwen3-embedding:4b | 4B | varies | yes | Upgrade path if VRAM allows |
| snowflake-arctic-embed2 | 568M | 1024 | yes | Reasonable alternative |
| mxbai-embed-large | 335M | 1024 | English-centric | No — wrong corpus |
| nomic-embed-text | 137M | 768 | English-centric | No — wrong corpus, and 768 dims |

**bge-m3** wins on three grounds beyond multilinguality:

- **1024 dimensions**, matching `mistral-embed`, so `kb/embeddings.npy` keeps
  its shape and nothing downstream changes size. (Vectors from different models
  are *not* comparable — a full re-embed is still required — but the storage
  and the code stay identical.)
- It is the **same family as the reranker** already validated on this corpus,
  where its multilingual handling of IAST was the deciding factor.
- MIT licence, self-hostable, no quota.

### Setup

```bash
# on the GPU box
ollama pull bge-m3
setx OLLAMA_HOST 0.0.0.0        # bind beyond localhost — see §7 on exposure
ollama serve
```

Ollama exposes both a native `/api/embed` and an **OpenAI-compatible
`/v1/embeddings`**. Use the latter: it accepts an array of inputs in one
request, which preserves the existing batching in `build_kb.embed_all`.

### Code change required

A provider shim following the pattern `rerank.py` already establishes —
pluggable backend, config-driven, graceful fallback, loud when it falls back:

```
embeddings.py   (new, ~120 lines)
  get_embedder()            honours CFG.embedding.backend
  MistralEmbedder           current behaviour, unchanged
  OllamaEmbedder            POST {OLLAMA_URL}/embeddings
  LocalEmbedder             sentence-transformers, already installed here
  embed(texts) -> [[float]]
```

Two call sites change:

- `build_kb.embed_all` — swap `client.embeddings.create` for `embedder.embed`
- `kb_search.embed_texts` — same

Config gains `embedding.backend` and `embedding.base_url`. **`embedding.model`
already participates in the KB fingerprint**, so switching models is detected
automatically and `build_kb.py` will refuse to serve a stale index. That safety
net already exists; nothing new is needed for it.

### The cost of switching: a full re-embed

Unavoidable and worth stating plainly.

| Consequence | Detail |
|---|---|
| All 9,467 vectors recomputed | `python build_kb.py --force` |
| Every evidence pack goes stale | `kb_stamp` changes → `make_evidence.py` for all 19 chapters |
| Retrieval quality changes | Not necessarily worse — but **unmeasured** |
| Sparse index unaffected | FTS5 and entity streams are text, not vectors |

That third row is the important one. There is no way to know whether bge-m3
retrieves better or worse on this corpus than mistral-embed without measuring
it, and the gold set is still empty. Which leads to §6.

---

## 5. Ollama for chat — the larger half

Four config keys point at `mistral-large-latest`, and they consume far more
tokens than embedding does. Ollama serves these through the same
OpenAI-compatible endpoint.

| Job | Demand | Suggested local model |
|---|---|---|
| Labelling, dossiers, claim extraction | High volume, structured JSON, undemanding | `qwen3:8b` or `gemma3:12b` |
| Claim decomposition + entailment | High volume, needs care | `qwen3:8b` minimum |
| Chapter drafting, editorial | Low volume, **quality-critical** | Largest that fits, or keep hosted |

**Recommendation: move the bulk jobs local, keep drafting hosted.**

Labelling 8,865 chunks and verifying hundreds of claims per chapter is where the
allowance goes, and those jobs want throughput and valid JSON rather than fine
prose. Chapter drafting is the opposite — a handful of calls whose output you
will actually read, where a weaker model shows immediately. Splitting them buys
most of the cost relief without putting the manuscript's prose on a smaller
model.

`llm.py` needs the same treatment as embeddings: a `backend` setting selecting
between the Mistral SDK and an OpenAI-compatible base URL. The retry classifier,
the AIMD rate limiter and `QuotaExhausted` are all provider-agnostic and stay
as they are — and a local Ollama has no quota, so `QuotaExhausted` simply never
fires.

---

## 6. Measure before and after — the gold set is the blocker

Switching embedding model and chat model at once changes retrieval *and*
generation simultaneously. If chapter quality moves, nothing will say which
change caused it.

`eval/` already has the harness — `eval_retrieval.py` (Recall@k, nDCG, empty-pack
accuracy), `eval_generation.py` (faithfulness, citation correctness),
`ablate.py` (config sweep with confidence intervals), `calibrate.py`
(RERANK_FLOOR). **The gold set is empty**, which makes all of it inert.

The sequence that keeps this honest:

```bash
# 1. baseline on the CURRENT stack, before changing anything
python -m eval.goldset --bootstrap 60 --negatives 15
python -m eval.goldset --review              # human pass — this is the real work
python -m eval.eval_retrieval --out eval/results/baseline_mistral.json

# 2. switch embeddings, rebuild, re-measure
python build_kb.py --force
python -m eval.eval_retrieval --out eval/results/bge_m3.json

# 3. compare
python -m eval.ablate --check-kill eval/results/bge_m3.json
```

Budget a day for the gold-set review. It is the least interesting work in the
project and the only thing that makes every number after it mean anything.

If the allowance is spent and the baseline cannot be measured on Mistral, the
honest fallback is to treat bge-m3 as the new baseline and measure *forward*
from it, accepting that the comparison to the old stack is lost.

---

## 7. Management and operations

### Keeping the services up

```bash
# vLLM: --restart unless-stopped handles reboots (already in the run command)
docker logs -f unlimited-ocr

# Ollama on Linux installs a systemd unit:
sudo systemctl enable --now ollama
sudo systemctl status ollama
journalctl -u ollama -f
```

### Model residency

Ollama unloads a model after ~5 minutes idle. For a long batch that means the
first call of each burst pays a reload.

```bash
setx OLLAMA_KEEP_ALIVE 30m        # hold models during a long labelling run
setx OLLAMA_MAX_LOADED_MODELS 2   # embeddings + chat resident together
```

### Health checks before a long run

Worth making a habit — each of these has already caught a real failure here:

```bash
python ocr_layout.py --check      # is the OCR endpoint serving the right model?
python rerank.py --check          # which reranker backends are usable?
python config.py --diff           # what differs from defaults, and the config hash
python make_evidence.py --check   # are the evidence packs stale?
```

### Network exposure

`OLLAMA_HOST=0.0.0.0` binds to every interface and **Ollama has no
authentication**. On a trusted LAN behind a router that is acceptable; on
anything else it is an open model server.

Prefer an SSH tunnel, which needs no firewall changes and no exposure:

```bash
ssh -N -L 11434:localhost:11434 -L 8000:localhost:8000 user@gpu-box
# then on the laptop, both services look local:
setx OLLAMA_URL http://localhost:11434/v1
setx UNLIMITED_OCR_URL http://localhost:8000/v1
```

### What must not leak

`.env` holds `MISTRAL_API_KEY` and `JINA_AI_API_KEY` and is gitignored. The run
records under `book/_runs/` are deliberately free of prompts and credentials —
there is a test asserting it (`test_record_holds_no_prompts_or_credentials`).
Keep both properties when adding providers: a `base_url` is fine to record, a
token is not.

---

## 8. Phased plan

Each phase is independently useful and independently revertible.

### Phase 0 — Baseline (do first, while the current stack still works)
Build the gold set and record baseline retrieval metrics. If the allowance is
already spent, skip and accept the lost comparison.

### Phase 1 — GPU box up, OCR working
Docker + vLLM, verify with `ocr_layout.py --check`, re-parse one book, compare
its structural labels against the heuristic ones already in `chunk_labels`.
**Deliverable:** observed layout labels, and a measured pages-per-minute figure.
**Kill criterion:** if observed labels do not disagree with the heuristics in any
material way, the corpus-wide re-ingest is not worth the GPU hours.

### Phase 2 — Ollama embeddings
`embeddings.py` shim, `build_kb.py --force`, regenerate all 19 evidence packs,
re-measure retrieval.
**Kill criterion:** if Recall@20 drops more than 5 points against baseline,
revert to Mistral embeddings — the shim makes that one config line.

### Phase 3 — Ollama chat for bulk jobs
Point `comprehension.model` and `verify.model` at the local model; leave
`generation.model` hosted. Re-run labelling on a 200-chunk sample and compare
against the existing labels before committing to the full pass.

### Phase 4 — Corpus re-ingest through Unlimited-OCR
Only if Phase 1 showed the observed labels are materially better. Re-OCR all 25
sources, rebuild, relabel, re-measure.

### Phase 5 — Optional: drafting local
Only with the eval harness live, and only if Phase 3 showed the local model
holds up on structured tasks. Chapter prose is the last thing to move.

---

## 9. Honest caveats

**The VRAM figures are estimates.** Derived from published model sizes and the
documented ≥8 GB for Unlimited-OCR, not measured on your card.

**GPU OCR throughput is extrapolated.** The 322 s/page CPU figure is measured
here; the GPU number is inference from typical CPU/GPU ratios for a 3B model.
Measure it in Phase 1 before planning a corpus-wide run.

**No embedding-quality comparison exists.** bge-m3 is recommended on corpus fit
and dimensional convenience, not on measured retrieval performance against this
corpus. Phase 2's kill criterion exists precisely because that is unknown.

**The `.cuda()` patch is CPU-only scaffolding.** `ocr_cpu_patch.py` rewrites the
vendored modelling code to honour `UNLIMITED_OCR_DEVICE`. On the GPU box, use
the vLLM container instead — it needs no patching, and running the patched
transformers path there would be slower and stranger for no gain.

**Local models are not drop-in equivalents.** A quantised 8B model is not
`mistral-large`. The plan splits jobs by tolerance for that difference rather
than pretending it does not exist, and Phase 3's sample-first step is there to
catch it.

---

## 10. Summary

| Concern | Answer |
|---|---|
| Fastest path to Baidu OCR on GPU | vLLM container; `ocr_layout.py` already speaks its API |
| Best embedding alternative | `bge-m3` on Ollama — multilingual, 1024 dims, MIT |
| Code to write | `embeddings.py` shim (~120 lines), `llm.py` backend switch |
| Code that already works | `ocr_layout.py`, `rerank.py` (Jina), the fingerprint staleness guard |
| Biggest hidden cost | Full re-embed → all 19 evidence packs regenerate |
| Biggest risk | Changing retrieval and generation together with no gold set to attribute the effect |
| Biggest opportunity | GPU OCR makes corpus-wide *observed* structural labels affordable |
