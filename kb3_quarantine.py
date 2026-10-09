#!/usr/bin/env python
"""Review, restore or quarantine chunks (spec C1, E). Reversible and logged.

    python kb3_quarantine.py list [--reason irrelevant] [--source gupte-1972] [-n 50]
    python kb3_quarantine.py show <chunk_id>
    python kb3_quarantine.py restore <chunk_id> --note "reviewed: relevant to C7"
    python kb3_quarantine.py quarantine <chunk_id> --reason "unsupported speculation" --note "..."

Every decision is appended to kb3/quarantine_overrides.jsonl. stage2_build.py
reads that file, so a human decision survives every rebuild, and the full
trail is kept in kb3/logs/quarantine.jsonl. The row is moved between the two
store files immediately. A restored chunk joins dense search at the next build.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sqlite3
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, ValueError):
    pass

K3 = Path(__file__).resolve().parent / "kb3"
OVR = K3 / "quarantine_overrides.jsonl"
LOG = K3 / "logs" / "quarantine.jsonl"


def cols(db):
    return [r[1] for r in db.execute("pragma table_info(chunks)") if r[1] not in ("rowid", "quarantined_at")]


def record(entry):
    entry["at"] = dt.datetime.now().isoformat(timespec="seconds")
    for p in (OVR, LOG):
        with open(p, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    l = sub.add_parser("list"); l.add_argument("--reason"); l.add_argument("--source"); l.add_argument("-n", type=int, default=40)
    s = sub.add_parser("show"); s.add_argument("chunk_id")
    r = sub.add_parser("restore"); r.add_argument("chunk_id"); r.add_argument("--note", required=True)
    q = sub.add_parser("quarantine"); q.add_argument("chunk_id"); q.add_argument("--reason", required=True); q.add_argument("--note", default="")
    a = ap.parse_args(argv)
    act, qua = sqlite3.connect(K3 / "kb_active.sqlite"), sqlite3.connect(K3 / "kb_quarantine.sqlite")

    if a.cmd == "list":
        sql, par = "select chunk_id, parent_source_id, quarantine_reason, substr(text,1,120) from chunks where 1=1", []
        if a.reason:
            sql += " and quarantine_reason like ?"; par.append(f"{a.reason}%")
        if a.source:
            sql += " and parent_source_id = ?"; par.append(a.source)
        for row in qua.execute(sql + f" limit {a.n}", par):
            print(f"{row[0]} | {row[1]} | {row[2]}\n    {row[3]!r}")
        print("total:", qua.execute("select count(*) from chunks").fetchone()[0])
    elif a.cmd == "show":
        for db, where in ((qua, "QUARANTINE"), (act, "ACTIVE")):
            row = db.execute("select * from chunks where chunk_id=?", (a.chunk_id,)).fetchone()
            if row:
                names = [d[0] for d in db.execute("select * from chunks limit 0").description]
                print(f"[{where}]"); [print(f"  {k}: {v}") for k, v in zip(names, row)]
                return 0
        print("not found")
    elif a.cmd == "restore":
        c = cols(qua)
        row = qua.execute(f"select {','.join(chr(34)+x+chr(34) for x in c)} from chunks where chunk_id=?", (a.chunk_id,)).fetchone()
        if not row:
            sys.exit("not in quarantine")
        rec = dict(zip(c, row)); prev = rec["quarantine_reason"]
        rec["is_quarantined"], rec["quarantine_reason"] = 0, None
        rec["review_status"] = f"restored by review: {a.note}"
        cur = act.execute(f"insert into chunks ({','.join(chr(34)+x+chr(34) for x in c)}) values ({','.join('?'*len(c))})",
                          [rec[x] for x in c])
        act.execute("insert into chunks_fts (rowid, text, aliases) values (?,?,?)",
                    (cur.lastrowid, rec["text"], " ".join(json.loads(rec["entities"] or "[]"))))
        qua.execute("delete from chunks where chunk_id=?", (a.chunk_id,))
        act.commit(); qua.commit()
        record({"action": "restore", "chunk_id": a.chunk_id, "previous_reason": prev, "note": a.note})
        print(f"restored {a.chunk_id} (was: {prev})")
    elif a.cmd == "quarantine":
        c = cols(act)
        row = act.execute(f"select rowid, {','.join(chr(34)+x+chr(34) for x in c)} from chunks where chunk_id=?", (a.chunk_id,)).fetchone()
        if not row:
            sys.exit("not in active store")
        rid, rec = row[0], dict(zip(c, row[1:]))
        rec["is_quarantined"], rec["quarantine_reason"] = 1, f"{a.reason} (manual review)"
        now = dt.datetime.now().isoformat(timespec="seconds")
        qua.execute(f"insert into chunks (quarantined_at, {','.join(chr(34)+x+chr(34) for x in c)}) values (?, {','.join('?'*len(c))})",
                    [now] + [rec[x] for x in c])
        act.execute("delete from chunks where rowid=?", (rid,))
        act.execute("delete from chunks_fts where rowid=?", (rid,))
        act.commit(); qua.commit()
        record({"action": "quarantine", "chunk_id": a.chunk_id, "reason": a.reason, "note": a.note})
        print(f"quarantined {a.chunk_id}: {a.reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
