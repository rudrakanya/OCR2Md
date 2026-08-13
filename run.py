#!/usr/bin/env python3
"""
run.py — a record of what a generation run actually did, and how to show it.

The pipeline already made every decision this module reports: retrieval scored
and floored its candidates, verification classified every claim, citation
resolution rejected invented ids. What it did not do was *keep* any of that. It
printed a few lines to stdout and moved on, so a finished chapter carried no
account of how it came to exist, and a failure said only which exception was
raised — never which stage raised it.

This adds the record and the renderer, and nothing else. It performs no
retrieval, calls no model, and makes no decisions of its own; every number it
displays is handed to it by the stage that computed it. That is deliberate — an
observability layer that recomputes anything can disagree with the pipeline it
claims to describe.

Two audiences, one record:

    render(run)          the CLI view: stages, counts, warnings, sources
    run.to_dict()        the machine view, for --json and for book/_runs/

What is deliberately NOT recorded: prompts, model responses, API keys, or any
reasoning the model did internally. The record holds decisions and their
evidence — passage ids, source names, scores, verdicts — never the private
intermediate text that produced them.

    from run import GenerationRun
    run = GenerationRun.start(chapter=6, pipeline_version="2.0")
    with run.stage("Retrieving evidence") as st:
        st.metric("passages", 60)
        st.source("Kramrisch, The Hindu Temple", passages=12)
        st.warn("2 sub-topics below the coverage floor")
    print(render(run))
"""
import json
import os
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

RUNS_DIR = Path("book/_runs")
PIPELINE_VERSION = "2.0"

OK, WARN, FAIL, SKIP = "ok", "warn", "fail", "skipped"

# Plain ASCII fallbacks: this pipeline already lost a 22-minute model load to a
# cp1252 console, and console.use_utf8() is not always in effect when a caller
# imports this module directly.
_GLYPHS = {True: {"ok": "✓", "warn": "⚠", "fail": "✗", "skip": "–", "rule": "─"},
           False: {"ok": "+", "warn": "!", "fail": "x", "skip": "-", "rule": "-"}}


def _unicode_ok():
    enc = (getattr(os.sys.stdout, "encoding", "") or "").lower()
    return "utf" in enc


@dataclass
class Stage:
    """One pipeline stage: what it did, what it found, what went wrong."""
    name: str
    index: int = 0
    total: int = 0
    status: str = OK
    started: float = field(default_factory=time.monotonic)
    seconds: float = 0.0
    metrics: dict = field(default_factory=dict)
    notes: list = field(default_factory=list)
    warnings: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    sources: list = field(default_factory=list)
    detail: dict = field(default_factory=dict)

    # -- recording -----------------------------------------------------------

    def metric(self, key, value):
        self.metrics[key] = value
        return self

    def note(self, text):
        """A line the user should see under this stage when it succeeded."""
        self.notes.append(str(text))
        return self

    def warn(self, text):
        self.warnings.append(str(text))
        if self.status == OK:
            self.status = WARN
        return self

    def error(self, text):
        self.errors.append(str(text))
        self.status = FAIL
        return self

    def source(self, name, **fields):
        """A reference book this stage drew on, with whatever is known of it."""
        self.sources.append({"source": name, **fields})
        return self

    def data(self, key, value):
        """Structured detail for --json / the run file, not for the CLI."""
        self.detail[key] = value
        return self

    def to_dict(self):
        return {"name": self.name, "index": self.index, "total": self.total,
                "status": self.status, "seconds": round(self.seconds, 2),
                "metrics": self.metrics, "notes": self.notes,
                "warnings": self.warnings, "errors": self.errors,
                "sources": self.sources, "detail": self.detail}


@dataclass
class GenerationRun:
    """The whole run: stages in order, plus what came out of it."""
    run_id: str
    chapter: int = 0
    title: str = ""
    pipeline_version: str = PIPELINE_VERSION
    started_at: str = ""
    kb: dict = field(default_factory=dict)
    config_hash: str = ""
    stages: list = field(default_factory=list)
    output: dict = field(default_factory=dict)
    seconds: float = 0.0
    _t0: float = field(default=0.0, repr=False)

    @classmethod
    def start(cls, chapter, title="", kb=None, config_hash="", version=PIPELINE_VERSION):
        return cls(run_id=uuid.uuid4().hex[:12], chapter=chapter, title=title,
                   pipeline_version=version, kb=kb or {}, config_hash=config_hash,
                   started_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                   _t0=time.monotonic())

    @contextmanager
    def stage(self, name, total=None, echo=True):
        """Record a stage. Exceptions are attributed to it and re-raised.

        Attribution is the point: `! chapter 6 failed: SDKError` told nobody
        which of five stages died. `[3/7] Validating evidence — FAILED` does.
        """
        st = Stage(name=name, index=len(self.stages) + 1, total=total or 0)
        self.stages.append(st)
        if echo:
            print(_stage_header(st), flush=True)
        try:
            yield st
        except Exception as e:                       # noqa: BLE001 - recorded, re-raised
            st.error(f"{type(e).__name__}: {e}")
            st.seconds = time.monotonic() - st.started
            if echo:
                print(_stage_body(st), end="", flush=True)
            raise
        else:
            st.seconds = time.monotonic() - st.started
            if echo:
                print(_stage_body(st), end="", flush=True)

    # -- accessors -----------------------------------------------------------

    def finish(self, **output):
        self.seconds = time.monotonic() - self._t0 if self._t0 else 0.0
        self.output.update(output)
        return self

    @property
    def failed(self):
        return any(s.status == FAIL for s in self.stages)

    @property
    def warnings(self):
        return [(s.name, w) for s in self.stages for w in s.warnings]

    @property
    def errors(self):
        return [(s.name, e) for s in self.stages for e in s.errors]

    def all_sources(self):
        """Every reference book the run touched, merged across stages."""
        merged = {}
        for s in self.stages:
            for rec in s.sources:
                key = rec["source"]
                cur = merged.setdefault(key, {"source": key})
                for k, v in rec.items():
                    if k == "source":
                        continue
                    if isinstance(v, (int, float)) and isinstance(cur.get(k), (int, float)):
                        cur[k] += v
                    else:
                        cur[k] = v
        return sorted(merged.values(), key=lambda r: -(r.get("passages") or 0))

    def to_dict(self):
        return {"run_id": self.run_id, "chapter": self.chapter, "title": self.title,
                "pipeline_version": self.pipeline_version, "started_at": self.started_at,
                "seconds": round(self.seconds, 2), "kb": self.kb,
                "config_hash": self.config_hash,
                "status": "failed" if self.failed else
                          ("warn" if self.warnings else "ok"),
                "stages": [s.to_dict() for s in self.stages],
                "sources": self.all_sources(),
                "warnings": [{"stage": n, "message": m} for n, m in self.warnings],
                "errors": [{"stage": n, "message": m} for n, m in self.errors],
                "output": self.output}

    def save(self, dirpath=RUNS_DIR):
        """Persist the record next to the chapter it produced."""
        d = Path(dirpath)
        d.mkdir(parents=True, exist_ok=True)
        p = d / f"ch{self.chapter:02d}_{self.run_id}.json"
        p.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=1),
                     encoding="utf-8")
        return p


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def _g():
    return _GLYPHS[_unicode_ok()]


def _stage_header(st):
    n = f"[{st.index}/{st.total}] " if st.total else f"[{st.index}] "
    return f"{n}{st.name}"


def _stage_body(st, verbose=False):
    """The indented lines under a stage header."""
    g = _g()
    out = []
    for k, v in st.metrics.items():
        val = f"{v:,}" if isinstance(v, int) else v
        out.append(f"      {g['ok']} {val} {k}")
    for t in st.notes:
        out.append(f"      {g['ok']} {t}")
    for w in st.warnings:
        out.append(f"      {g['warn']} {w}")
    for e in st.errors:
        out.append(f"      {g['fail']} {e}")
    if st.status == FAIL and not st.errors:
        out.append(f"      {g['fail']} failed")
    if verbose and st.detail:
        for k, v in st.detail.items():
            out.append(f"        {k}: {json.dumps(v, ensure_ascii=False)[:160]}")
    return ("\n".join(out) + "\n") if out else ""


def render(run, verbose=False, show_sources=False):
    """The full run as the CLI shows it. Used for the final summary."""
    g = _g()
    lines = [f"Chapter {run.chapter} generation" + (f" — {run.title}" if run.title else ""),
             g["rule"] * 60]
    for st in run.stages:
        lines.append(_stage_header(st))
        body = _stage_body(st, verbose)
        if body:
            lines.append(body.rstrip("\n"))
    lines.append("")

    if show_sources:
        srcs = run.all_sources()
        if srcs:
            lines.append(f"Reference books drawn on ({len(srcs)}):")
            for s in srcs:
                bits = [f"{s.get('passages', 0)} passages"]
                if s.get("cited"):
                    bits.append(f"{s['cited']} cited")
                if s.get("kind"):
                    bits.append(s["kind"])
                lines.append(f"  {g['ok']} {s['source'][:56]:58s} {', '.join(bits)}")
            lines.append("")

    if run.failed:
        lines.append(f"{g['fail']} Chapter generation FAILED")
        for stage, msg in run.errors:
            lines.append(f"    {stage}: {msg}")
    else:
        out = run.output
        tail = ""
        if out.get("words"):
            tail = (f" — {out['words']:,} words, {out.get('endnotes', 0)} endnotes, "
                    f"{out.get('sources', 0)} sources")
        lines.append(f"{g['ok']} Chapter draft generated{tail}")
        if run.warnings:
            lines.append(f"  {g['warn']} {len(run.warnings)} warning(s); "
                         f"see the stages above")
        if out.get("path"):
            lines.append(f"  {out['path']}")
    if run.seconds:
        lines.append(f"  run {run.run_id} · {run.seconds:.0f}s")
    return "\n".join(lines)


def summary_line(run):
    """One line, for a multi-chapter loop."""
    g = _g()
    mark = g["fail"] if run.failed else (g["warn"] if run.warnings else g["ok"])
    out = run.output
    return (f"{mark} ch{run.chapter:02d} {out.get('words', 0):>6,}w "
            f"{out.get('endnotes', 0):>3} notes  {run.seconds:>5.0f}s")
