"""local_embed.py — embeddings via a local Ollama server, replacing the
mistral-embed API (billing-blocked: 402 Payment Required on this account,
same wall the OCR pipeline hit earlier).

Default model is bge-m3: multilingual (this corpus mixes English, Sanskrit
and Devanagari), 1024-dim, already pulled locally (`ollama list`). Swap via
OLLAMA_EMBED_MODEL if needed.

Used by both build_kb.py (indexing) and kb_search.py (query time) so the two
can never drift onto different embedding spaces.
"""
import os
import time

import requests

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("OLLAMA_EMBED_MODEL", "bge-m3")


def embed_batch(model, texts, attempts=5):
    """Embed a list of texts in one request, with retry/backoff. Returns a
    list of float lists, same order as `texts`."""
    delay = 5
    last_err = None
    for n in range(1, attempts + 1):
        try:
            r = requests.post(f"{OLLAMA_URL}/api/embed",
                               json={"model": model, "input": texts},
                               timeout=120)
            r.raise_for_status()
            data = r.json()
            embs = data.get("embeddings")
            if not embs or len(embs) != len(texts):
                raise RuntimeError(f"Ollama returned {len(embs) if embs else 0} "
                                    f"embeddings for {len(texts)} inputs")
            return embs
        except Exception as e:                       # noqa: BLE001 retry transient
            last_err = e
            if n == attempts:
                raise
            print(f"    embed retry {n}/{attempts - 1}: {type(e).__name__}: {e}", flush=True)
            time.sleep(delay)
            delay = min(delay * 2, 60)
    raise last_err  # pragma: no cover
