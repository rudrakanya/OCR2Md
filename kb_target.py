#!/usr/bin/env python
"""Which knowledge-base store everything reads. One source of truth.

    from kb_target import active, sqlite_path, collection

Before this existed the live store was named in five modules independently
(`chapter_pipeline`, `build_sourcebook`, `kb3_query`, `kb3_chroma_query`,
`kb_inventory`), so a cutover meant five edits and any one of them could be
missed -- a drafting path silently reading v1 while the sourcebook read v2 is
exactly the kind of split-brain this project cannot afford.

Resolution order, first wins:
    1. the KB_STORE environment variable (per-process override, for testing)
    2. kb3/active_store.txt                (the committed, deliberate setting)
    3. "v1"                                (the safe default)

A store is a sqlite file plus a Chroma collection plus the embedder that
collection's vectors were made with. They travel together: a collection holds
exactly one vector space, so reading v2's collection with v1's embedder would
return nonsense rather than an error.
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
K3 = ROOT / "kb3"
POINTER = K3 / "active_store.txt"

STORES = {
    "v1": {
        "sqlite": "kb_active.sqlite",
        "quarantine": "kb_quarantine.sqlite",
        "collection": "udaypur_kb",
        "archive": "udaypur_kb_archive",
        "embedder": "local",
        "embed_model": "intfloat/multilingual-e5-small",
        "dim": 384,
        "note": "original store, 14,702 chunks, local e5-small",
    },
    "v2": {
        "sqlite": "kb_active_v2.sqlite",
        "quarantine": "kb_quarantine_v2.sqlite",
        "collection": "udaypur_kb_v2",
        "archive": "udaypur_kb_v2_archive",
        "embedder": "local",
        "embed_model": "intfloat/multilingual-e5-small",
        "dim": 384,
        "note": "re-chunked store with LOCAL vectors (not built)",
    },
    "v2-openai": {
        "sqlite": "kb_active_v2.sqlite",
        "quarantine": "kb_quarantine_v2.sqlite",
        "collection": "udaypur_kb_v2_openai",
        "archive": "udaypur_kb_v2_openai_archive",
        "embedder": "openai",
        "embed_model": "text-embedding-3-large",
        "dim": 1536,
        "note": "re-chunked, Patil merged, fabrications quarantined; OpenAI 1536-d",
    },
}


def active() -> str:
    env = os.environ.get("KB_STORE")
    if env in STORES:
        return env
    try:
        name = POINTER.read_text(encoding="utf-8").strip().split("\n")[0].strip()
        if name in STORES:
            return name
    except OSError:
        pass
    return "v1"


def cfg(store=None) -> dict:
    return STORES[store or active()]


def sqlite_path(store=None) -> Path:
    return K3 / cfg(store)["sqlite"]


def quarantine_path(store=None) -> Path:
    return K3 / cfg(store)["quarantine"]


def collection(store=None) -> str:
    return cfg(store)["collection"]


def archive(store=None) -> str:
    return cfg(store)["archive"]


def describe(store=None) -> str:
    s = store or active()
    c = cfg(s)
    return (f"{s}: {c['sqlite']} + {c['collection']} "
            f"({c['embed_model']} @ {c['dim']}-d)")


if __name__ == "__main__":
    print(f"active store: {describe()}")
    print(f"pointer file: {POINTER} "
          f"({'present' if POINTER.exists() else 'absent — defaulting to v1'})")
    for name in STORES:
        mark = "  <= active" if name == active() else ""
        print(f"  {name:10s} {describe(name)}{mark}")
