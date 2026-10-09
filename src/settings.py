"""Config loading, hashing and provenance.

Everything tunable lives in config.yaml (§3). This module is the only place
that reads it, so there is exactly one answer to "what settings am I running?".

Named `settings.py`, not `config.py`, on purpose: the project root already
contains an unrelated `config.py` from the v2 pipeline, and a `src/config.py`
would shadow it for anything that does `import config`.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.metadata as md
import json
import os
import platform
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config.yaml"

# Windows consoles default to cp1252 and will kill a run mid-write the first
# time a Devanagari character reaches stdout. This corpus is 40% Devanagari in
# places, so force UTF-8 before anything prints.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):  # pragma: no cover - non-tty
        pass


class ConfigError(RuntimeError):
    """Raised loudly rather than falling back to a default (§3: fail loudly)."""


class Config(dict):
    """dict with dotted access, so `cfg.chunking.target_tokens` reads cleanly."""

    def __getattr__(self, item: str) -> Any:
        try:
            value = self[item]
        except KeyError:
            raise AttributeError(
                f"no config key {item!r}; known keys here: {sorted(self)}"
            ) from None
        return Config(value) if isinstance(value, dict) else value

    def get_path(self, dotted: str, default: Any = ...) -> Any:
        node: Any = self
        for part in dotted.split("."):
            if not isinstance(node, dict) or part not in node:
                if default is ...:
                    raise ConfigError(f"missing config key: {dotted}")
                return default
            node = node[part]
        return node


def load(path: Path | str | None = None) -> Config:
    path = Path(path) if path else CONFIG_PATH
    if not path.is_file():
        raise ConfigError(f"config not found: {path}")
    with path.open("r", encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    if not isinstance(raw, dict):
        raise ConfigError(f"{path} did not parse to a mapping")
    return Config(raw)


def apply_overrides(cfg: Config, *, embed_preset: str | None = None,
                    chunk_tokens: int | None = None) -> Config:
    """Return a copy of cfg with CLI overrides applied.

    Overrides exist so an ablation (§10.3) can sweep models and chunk sizes
    without editing config.yaml, while the file keeps recording the settings
    you actually intend to ship.
    """
    cfg = Config(copy.deepcopy(dict(cfg)))
    if embed_preset:
        alts = cfg["embedding"].get("alternatives", {})
        if embed_preset not in alts:
            raise ConfigError(
                f"unknown embedding preset {embed_preset!r}; "
                f"available: {sorted(alts)}"
            )
        cfg["embedding"].update(alts[embed_preset])
        cfg["embedding"]["preset"] = embed_preset
    if chunk_tokens:
        cfg["chunking"]["target_tokens"] = int(chunk_tokens)
    return cfg


def config_hash(cfg: Config) -> str:
    """Stable short hash of the settings that affect stored artefacts.

    Deliberately excludes `logging` and `reporting`: changing a report
    threshold must not make every previous ingest look like it came from a
    different configuration.
    """
    material = {k: v for k, v in cfg.items() if k not in ("logging", "reporting")}
    blob = json.dumps(material, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:12]


def section_hash(cfg: Config, *sections: str) -> str:
    """Hash of named sections only — for narrower staleness checks."""
    material = {s: cfg.get(s) for s in sections}
    blob = json.dumps(material, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:12]


def library_versions() -> dict[str, str]:
    out: dict[str, str] = {"python": platform.python_version()}
    for pkg in ("chromadb", "sentence-transformers", "transformers", "torch",
                "rank_bm25", "langchain-text-splitters", "numpy", "PyYAML"):
        try:
            out[pkg] = md.version(pkg)
        except md.PackageNotFoundError:
            out[pkg] = "not-installed"
    return out


def provenance(cfg: Config) -> dict[str, Any]:
    """The block stamped into every run output so results stay comparable."""
    return {
        "config_hash": config_hash(cfg),
        "embedding_model": cfg.get_path("embedding.model"),
        "embedding_preset": cfg.get_path("embedding.preset", "default"),
        "chunk_target_tokens": cfg.get_path("chunking.target_tokens"),
        "chunk_overlap_tokens": cfg.get_path("chunking.overlap_tokens"),
        "libraries": library_versions(),
    }


def resolve(cfg: Config, dotted: str) -> Path:
    """Resolve a config path value against the project root."""
    raw = cfg.get_path(dotted)
    p = Path(os.path.expandvars(str(raw))).expanduser()
    return p if p.is_absolute() else (ROOT / p).resolve()


def load_chapters(cfg: Config) -> list[dict[str, Any]]:
    path = resolve(cfg, "storage.chapters")
    if not path.is_file():
        raise ConfigError(f"chapters file not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    chapters = data.get("chapters") or []
    if not chapters:
        raise ConfigError(f"{path} contains no chapters")
    seen: set[str] = set()
    for ch in chapters:
        cid = ch.get("id")
        if not cid:
            raise ConfigError(f"chapter without an id in {path}: {ch}")
        if cid in seen:
            raise ConfigError(f"duplicate chapter id {cid!r} in {path}")
        seen.add(cid)
        if not ch.get("descriptor"):
            raise ConfigError(f"chapter {cid} has no descriptor")
    data["_keyword_weight"] = data.get("keyword_weight", 1)
    for ch in chapters:
        ch["_keyword_weight"] = data["_keyword_weight"]
    return chapters


def load_manifest(cfg: Config) -> dict[str, dict[str, Any]]:
    """filename -> metadata. Keys with unknown/None values are dropped, because
    ChromaDB rejects a None metadata value outright (§6)."""
    path = resolve(cfg, "storage.manifest")
    if not path.is_file():
        raise ConfigError(f"manifest not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out: dict[str, dict[str, Any]] = {}
    for row in data.get("books") or []:
        fname = row.get("file")
        if not fname:
            raise ConfigError(f"manifest row without a `file` key: {row}")
        clean = {k: v for k, v in row.items()
                 if not k.startswith("_") and k != "needs_review" and v is not None}
        out[fname] = clean
    if not out:
        raise ConfigError(f"{path} lists no books")
    return out


def chapter_field(chapter_id: str) -> str:
    """C08 -> chap_C08. One boolean column per chapter is the only thing Chroma
    can actually filter on, since metadata values may not be lists (§6)."""
    return f"chap_{chapter_id}"


if __name__ == "__main__":  # `python -m src.settings --hash`
    _cfg = load()
    if "--hash" in sys.argv:
        print(config_hash(_cfg))
    else:
        print(json.dumps(provenance(_cfg), indent=2, ensure_ascii=False))
