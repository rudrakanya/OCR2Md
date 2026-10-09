#!/usr/bin/env python
"""Step C — cut the drafting and sourcebook paths over to v2, reversibly.

    python phase4_cutover.py --preflight          # check only, changes nothing
    python phase4_cutover.py --to v2-openai       # the cutover (gated)
    python phase4_cutover.py --rollback           # back to v1, one command

WHAT A CUTOVER IS HERE: one line in kb3/active_store.txt. Every module resolves
the live store through kb_target, so the switch is atomic and the rollback is
the same switch in reverse. Nothing is copied, renamed or deleted; v1's sqlite
and its Chroma collections are untouched and stay queryable by name.

ROLLBACK IS ONE COMMAND:  python phase4_cutover.py --rollback

Preflight refuses the cutover unless the target store is actually sound:
collection present and non-empty, sqlite present, counts agreeing, the merged
Patil source resolving to one code, and the quarantine held in a separate file
that the active collection does not contain.
"""
from __future__ import annotations

import argparse
import collections
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

import kb_target as T

ROOT = T.ROOT
POINTER = T.POINTER
LOG = ROOT / "kb_audit" / "cutover_log.jsonl"


def preflight(store):
    """Every check that must pass before the live pointer may move."""
    c = T.cfg(store)
    print(f"preflight for {T.describe(store)}\n")
    ok = True

    def chk(label, good, detail=""):
        nonlocal ok
        ok &= bool(good)
        print(f"  [{'ok ' if good else 'FAIL'}] {label}{(' — ' + detail) if detail else ''}")

    sq = T.sqlite_path(store)
    chk("sqlite present", sq.exists(), str(sq.name))
    n_sql = 0
    if sq.exists():
        db = sqlite3.connect(f"file:{sq}?mode=ro", uri=True)
        n_sql = db.execute("select count(*) from chunks").fetchone()[0]
        has_fts = bool(db.execute("select count(*) from sqlite_master "
                                  "where name='chunks_fts'").fetchone()[0])
        quar = db.execute("select count(*) from chunks where is_quarantined=1").fetchone()[0]
        chk("sqlite has chunks", n_sql > 0, f"{n_sql} rows")
        chk("full-text index present", has_fts)
        chk("no quarantined rows left in the ACTIVE sqlite", quar == 0,
            f"{quar} found" if quar else "quarantine is a separate file")
        db.close()

    qp = T.quarantine_path(store)
    n_q = 0
    if qp.exists():
        dq = sqlite3.connect(f"file:{qp}?mode=ro", uri=True)
        n_q = dq.execute("select count(*) from chunks").fetchone()[0]
        dq.close()
    chk("quarantine file present and separate", qp.exists(), f"{n_q} chunks")

    import chromadb
    client = chromadb.PersistentClient(path=str(ROOT / "kb3" / "chroma"))
    names = {x.name for x in client.list_collections()}
    chk("collection exists", c["collection"] in names, c["collection"])
    n_vec = 0
    if c["collection"] in names:
        col = client.get_collection(c["collection"])
        n_vec = col.count()
        probe = col.get(limit=1, include=["embeddings"])
        dim = len(probe["embeddings"][0]) if len(probe["embeddings"]) else 0
        chk("vectors present", n_vec > 0, f"{n_vec}")
        chk("dimension matches the declared embedder", dim == c["dim"],
            f"{dim}-d vs expected {c['dim']}-d")
        chk("sqlite and collection agree", abs(n_sql - n_vec) <= 0.02 * max(1, n_sql),
            f"sqlite {n_sql} vs vectors {n_vec}")

        # the fabrications must not be reachable in the live collection
        got = col.get(limit=n_vec + 10, include=["documents", "metadatas"])
        fab = sum(1 for d in got["documents"]
                  if "rāhīna" in (d or "") or "Island | Attribution" in (d or ""))
        arch = sum(1 for m in got["metadatas"] if m.get("is_archived"))
        chk("no fabricated ADH rows in the live collection", fab == 0, f"{fab} found")
        chk("no archived rows in the live collection", arch == 0, f"{arch} found")

        srcs = collections.Counter(m.get("parent_source_id") for m in got["metadatas"])
        comp = [s for s in srcs if s and s.startswith("patil-composite")]
        chk("Patil merged to one source", not comp,
            f"still separate: {comp}" if comp else f"patil-1952: {srcs.get('patil-1952', 0)} chunks")

    reg = yaml.safe_load((ROOT / "kb_audit" / "source_registry.yaml").read_text(encoding="utf-8"))
    codes = [s.get("code") for s in reg["sources"] if s.get("code")]
    dups = [x for x, n in collections.Counter(codes).items() if n > 1]
    chk("one code per source, no collisions", not dups, f"{len(codes)} codes")

    print(f"\n  v1 remains intact: "
          f"{'yes' if (ROOT / 'kb3' / 'kb_active.sqlite').exists() and 'udaypur_kb' in names else 'NO'}")
    backups = sorted((ROOT / "kb3" / "backup").glob("phase4-*"))
    print(f"  backup present: {backups[-1].name if backups else 'NONE'}")
    return ok


def switch(store, reason):
    prev = T.active()
    POINTER.parent.mkdir(parents=True, exist_ok=True)
    POINTER.write_text(
        f"{store}\n"
        f"# Active knowledge-base store, read by kb_target.\n"
        f"# Switched {datetime.now().isoformat(timespec='seconds')} from {prev}.\n"
        f"# Roll back with:  python phase4_cutover.py --rollback\n",
        encoding="utf-8")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({"at": datetime.now().isoformat(timespec="seconds"),
                            "from": prev, "to": store, "reason": reason}) + "\n")
    print(f"\nactive store: {prev} -> {store}")
    print(f"  {T.describe(store)}")
    print(f"  rollback: python phase4_cutover.py --rollback")


def main():
    ap = argparse.ArgumentParser()
    # --preflight is a MODE, not an alternative target: you want to preflight a
    # specific store, so it combines with --to rather than excluding it.
    ap.add_argument("--preflight", action="store_true",
                    help="run the checks for --to and change nothing")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--to", choices=sorted(T.STORES))
    g.add_argument("--rollback", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="switch even if preflight fails (not advised)")
    a = ap.parse_args()

    if a.rollback and not a.preflight:
        print(f"current: {T.describe()}")
        switch("v1", "rollback")
        return 0

    target = a.to or T.active()
    ok = preflight(target)
    print("\n" + ("PREFLIGHT PASSED" if ok else "PREFLIGHT FAILED"))
    if a.preflight:
        print("(no changes made)")
        return 0 if ok else 1
    if not ok and not a.force:
        print("refusing to cut over; re-run with --force only if you mean it")
        return 1
    switch(target, "phase 4 step C cutover")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
