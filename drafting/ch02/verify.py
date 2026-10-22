"""Citation-support helpers for Chapter 2 (cited_sentences, rule_checks, VERIFY_SYS, FIX_SYS); used by pipeline_ch02.py.

1 extract every cited sentence (code) with the full text of each cited item
2 verifier: one call per section, all sections concurrently, effort medium, skeptical; verdict per sentence
  SUPPORTED / PARTIAL / UNSUPPORTED / MISREPRESENTED + exact evidence phrase + one-line fix
3 rule checks in code: borrowed items only in 1.2 (exception: C04-PANDE-005 in 1.5, per the user's decision
  on the accession); c. 1070 presented as a working position with the other dates beside it; no 1310 record /
  1645 slab; no narrator superlatives; no precise claims on approximate (≈) Jagta pages; conflicts present
4 one round of targeted fixes (sections concurrently, effort medium): flagged sentences only, sentence-level
  replacement or cut; each replacement kept only if the code validation is no worse
5 re-verify only the changed sentences; keep a fix only if its verdict is no worse, else revert and list open
6 rebuild ch01_draft_v1.md (+ footnoted), write ch01_spotcheck.md and verification_state.json

Budget: this step ≤ $0.70; if the run total would pass $5, up to $5.75 total for verification only.
  python -u -I "drafting/ch01/verify.py" [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import random
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import draft as dr  # noqa: E402
import pipeline_v3 as pv  # noqa: E402
import validate as va  # noqa: E402

D = dr.D
STEP_CAP = 0.70
TOTAL_CAP_VERIFY = 5.75
pv.EFFORT.update({"verify": "medium", "fix": "medium", "reverify": "medium"})
RANK = {"SUPPORTED": 3, "PARTIAL": 2, "MISREPRESENTED": 1, "UNSUPPORTED": 0}
SUPERLATIVE = re.compile(r"\b(finest|greatest|grandest|largest|best|most\s+\w+|unrivall?ed|supreme|unique|"
                         r"unparalleled|matchless|peerless|incomparable|magnificent|\w+est)\b", re.I)
NOT_SUPER = {"earliest", "latest", "nearest", "west", "interest", "honest", "forest", "harvest", "rest", "test",
             "contest", "request", "suggest", "protest", "invest", "manifest", "modest", "guest", "chest", "quest",
             "southwest", "northwest", "almost", "most", "eldest", "oldest", "smallest", "longest", "highest"}
ATTRIB = re.compile(r"\b(call(s|ed)?|describ(es|ed)|wr(ote|ites)|according to|in the words of|judg(es|ed)|"
                    r"rank(s|ed)|consider(s|ed)|deem(s|ed)|say(s)?|said|holds?|claims?|records?|reports?|states?|gives?|finds?|notes?|identif(?:y|ies|ied)|counts?)\b", re.I)


def ts():
    return time.strftime("%H:%M:%S")


def cited_sentences(text):
    out = {}
    for sec, part in va.split_sections(text).items():
        rows = []
        for s in va.sentences(part):
            ids = [i for i in va.ids_in(s) if i != "AUTHOR"]
            if ids:
                rows.append({"sid": f"{sec}-{len(rows) + 1:02d}", "sentence": s.strip(), "ids": ids})
        out[sec] = rows
    return out


def item_text(i):
    flags = [f for f in i["flags"] if not f.startswith("also")]
    s = f"[{i['id']}] {i['book_title']} · {i['page']}" + (f" · {', '.join(flags)}" if flags else "") + \
        f"\n  QUOTE: {' '.join(i['quote'].split())}"
    if i.get("gloss"):
        s += f"\n  ENGLISH RENDERING: {i['gloss']}"
    if i.get("note"):
        s += f"\n  MAPPING NOTE (attribution context only): {i['note']}"
    return s


def rule_checks(text, P, sent_map):
    """code rules; returns list of {sid?, sec, rule, detail}"""
    fails = []
    parts = va.split_sections(text)
    for sec, rows in sent_map.items():
        for r in rows:
            s = r["sentence"]
            plain = va.BRACKET.sub("", s)
            gaz = [x for x in r["ids"] if x in P and P[x]["book_code"] == "GAZ"]
            yrs = [int(y) for y in re.findall(r"(?<![\d,.])\b(\d{3,4})\b(?![.,]\d)", plain) if not re.search(y + r"\s*(?:mm|km|m\b|metres?|ha|hect|°|per)", plain)]
            if gaz and len(gaz) == len(r["ids"]) and any(y < 1700 for y in yrs):
                fails.append({"sid": r["sid"], "sec": sec, "rule": "Gazetteer used for a pre-modern date",
                              "detail": "the Gazetteer is for the modern setting only — cite a dynastic/epigraphic item or cut"})
            unq = re.sub(r"[\"“][^\"”]*[\"”]", "", plain)
            for m in SUPERLATIVE.finditer(unq):
                w = m.group(0).lower()
                if w in ("most likely", "most often", "most frequently", "most commonly"):
                    continue
                if w.startswith("most ") and (w.split()[1] in ("of", "part", "parts") or (w.endswith("s") and not w.endswith(("ous", "ss")))):
                    continue                     # "most quarries", "most of": quantity, not a superlative
                if w in NOT_SUPER or (w.endswith("est") and not re.match(r"(finest|greatest|grandest|largest|best|richest|purest|noblest|loftiest|tallest|biggest)$", w)):
                    continue
                if not ATTRIB.search(unq):
                    fails.append({"sid": r["sid"], "sec": sec, "rule": "narrator superlative", "detail": f"'{m.group(0)}' outside quotation marks and unattributed"})
            approx = [x for x in r["ids"] if x in P and "≈ (Hindi original)" in P[x]["flags"]]
            if approx and len(approx) == len(r["ids"]) and re.search(r"\b\d[\d,.]*\b", plain) \
                    and not re.search(r"Tiwari|the author|Jagta|resident|told|writes|records|reports|recalls|says", plain, re.I):
                fails.append({"sid": r["sid"], "sec": sec, "rule": "precise claim on approximate Jagta page",
                              "detail": "a number/date resting only on ≈-paged Jagta Hua Kasba items, not attributed as testimony"})
    # material owned by Chapter 3 (hill heights, the arch) and items excluded outright
    for pat, what in ((r"567\.66|582\.31", "hill heights (Chapter 3)"), (r"\b270\s*(?:m|metres)\b", "hill rise of 270 m (Chapter 3)"),
                      (r"Temple Economics", "Temple Economics (excluded)"), (r"Third Eye", "the natural arch (Chapter 3)")):
        if re.search(pat, text):
            fails.append({"sec": "chapter", "rule": "material owned elsewhere / excluded", "detail": what})
    if re.search(r"[\u0900-\u097F]", va.BRACKET.sub("", text)):
        fails.append({"sec": "chapter", "rule": "Devanagari in prose", "detail": "use 'Tiwari' / the English title"})
    if re.search(r"JAGTA", text) and not re.search(r"Vijay Manohar Tiwari", text):
        fails.append({"sec": "chapter", "rule": "Tiwari", "detail": "Jagta Hua Kasba cited but Vijay Manohar Tiwari never named in full"})
    if re.search(r"C02-GAZ-", text) and "1979" not in text:
        fails.append({"sec": "chapter", "rule": "Gazetteer date-stamp", "detail": "the district Gazetteer is never date-stamped as the 1979 compilation"})
    if re.search(r"Tiwari", text) and not re.search(r"Vijay Manohar Tiwari", text):
        fails.append({"sec": "chapter", "rule": "Tiwari", "detail": "Vijay Manohar Tiwari never named in full"})
    if len(re.findall(r"Vijay Manohar Tiwari", text)) > 1:
        fails.append({"sec": "chapter", "rule": "Tiwari", "detail": "full name used more than once"})
    rep = va.check(text, P)
    for c in rep["conflicts"]:
        if not c["present"]:
            fails.append({"sec": c["section"], "rule": "conflict missing", "detail": c["conflict"]})
    return fails


VERIFY_SYS = """You are a skeptical fact-checker. For each numbered sentence of a non-fiction chapter, compare it ONLY with the evidence items it cites (quotes, English renderings; mapping notes only tell you who is speaking).
Verdicts:
- SUPPORTED: the cited items state this (paraphrase is fine).
- PARTIAL: the sentence goes beyond the evidence — an added date or number, stronger wording, certainty the source does not have, or two claims merged so that one is unsupported.
- UNSUPPORTED: the cited items do not say this.
- MISREPRESENTED: a disagreement between sources is presented as settled, or a claim is attributed to the wrong source/person.
Attribution sentences ("Ganguly writes…") must match who actually says it. Purely transitional phrasing needs no support. Be strict about numbers, dates, names and certainty.
Return ONLY JSON: {"results": [{"sid": "2.1-01", "verdict": "SUPPORTED|PARTIAL|UNSUPPORTED|MISREPRESENTED", "evidence": "exact short phrase from the cited item that supports or contradicts it (≤ 20 words)", "fix": "one-line fix if not SUPPORTED, else empty"}]}"""

FIX_SYS = """You correct flagged sentences in a non-fiction chapter so that each is supported by its cited evidence.
For each flagged sentence, return a replacement that: uses only facts in the cited items; keeps or corrects the bracketed evidence IDs (only IDs from the supplied evidence); keeps quotations verbatim from an item's QUOTE; presents source disagreements as disagreements; turns an unsupportable claim into an attributed claim ("X writes that…") or an open question, or cuts it. Never add new facts. Keep the sentence's role in its paragraph and British/Indian English with diacritics.
Return ONLY JSON: {"replacements": [{"sid": "2.1-01", "new": "replacement sentence with [IDs]" or "CUT", "note": "what changed"}]}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    t0 = time.time()
    P = dr.pack()
    src = D / "ch01_draft_v1.md"
    text = src.read_text(encoding="utf-8")
    if not a.dry_run:
        shutil.copy(src, D / "ch01_draft_v1_preverify.md")
    R = pv.Run(a.dry_run)
    start_spent = R.spent
    cap_total = min(start_spent + STEP_CAP, max(pv.BUDGET, start_spent + STEP_CAP if start_spent + STEP_CAP <= TOTAL_CAP_VERIFY else TOTAL_CAP_VERIFY))
    cap_total = min(cap_total, TOTAL_CAP_VERIFY)
    pv.BUDGET = cap_total            # Run.call enforces this as the hard stop for this step
    print(f"[{ts()}] verify start: run spend so far ${start_spent:.3f}; this step may spend up to ${cap_total - start_spent:.2f} (cap total ${cap_total:.2f})", flush=True)
    state = {"start_spend": round(start_spent, 4), "cap_total": round(cap_total, 4), "sections": {}}
    smap = cited_sentences(text)
    rules = rule_checks(text, P, smap)
    state["rule_failures_before"] = rules
    # ---------- 2 verifier, sections concurrently
    def verify_job(sec, rows, name="verify", kind="verify"):
        def job():
            ids = sorted({i for r in rows for i in r["ids"] if i in P})
            u = "EVIDENCE ITEMS:\n" + "\n\n".join(item_text(P[i]) for i in ids) + "\n\nSENTENCES TO CHECK:\n" + \
                "\n".join(f"{r['sid']}: {r['sentence']}" for r in rows)
            out = R.call(f"{name}_{sec}", 7, kind, VERIFY_SYS, u, 60 * len(rows))
            if out is None:
                return {r["sid"]: {"verdict": "SUPPORTED", "evidence": "", "fix": ""} for r in rows}
            j = pv.parse_json(out) or {}
            return {x.get("sid"): x for x in j.get("results", [])}
        return job
    res = R.parallel([(sec, verify_job(sec, rows)) for sec, rows in smap.items() if rows])
    verdicts = {}
    for sec, rows in smap.items():
        got = res.get(sec)
        got = got if isinstance(got, dict) else {}
        for r in rows:
            v = got.get(r["sid"]) or {"verdict": "UNVERIFIED", "evidence": "", "fix": ""}
            v["verdict"] = str(v.get("verdict", "UNVERIFIED")).upper()
            verdicts[r["sid"]] = dict(r, **v)
    def counts(vs):
        out = {}
        for sec in smap:
            c = {}
            for k, v in vs.items():
                if k.startswith(sec + "-"):
                    c[v["verdict"]] = c.get(v["verdict"], 0) + 1
            out[sec] = c
        return out
    state["verdicts_before"] = counts(verdicts)
    print(f"[{ts()}] verdicts before: {state['verdicts_before']}", flush=True)
    # ---------- 4 targeted fixes
    flagged = {}
    for sid, v in verdicts.items():
        if v["verdict"] not in ("SUPPORTED",):
            flagged.setdefault(sid.split("-")[0], []).append((sid, v["verdict"], v.get("fix", ""), v.get("evidence", "")))
    for f in rules:
        if f.get("sid"):
            flagged.setdefault(f["sec"], []).append((f["sid"], "RULE: " + f["rule"], f["detail"], ""))
    def fix_job(sec, items):
        def job():
            rows = {sid: verdicts.get(sid) or next(r for r in smap[sec] if r["sid"] == sid) for sid, *_ in items}
            ids = sorted({i for sid in rows for i in rows[sid]["ids"] if i in P})
            u = "EVIDENCE ITEMS:\n" + "\n\n".join(item_text(P[i]) for i in ids) + "\n\nFLAGGED SENTENCES:\n" + \
                "\n".join(f"{sid}: {rows[sid]['sentence']}\n   problem: {verd}; suggested fix: {fx}; evidence: {ev}" for sid, verd, fx, ev in items)
            out = R.call(f"fix_{sec}", 8, "fix", FIX_SYS, u, 60 * len(items))
            j = pv.parse_json(out) if out else None
            return {x.get("sid"): x for x in (j or {}).get("replacements", [])}
        return job
    fixes = R.parallel([(sec, fix_job(sec, items)) for sec, items in flagged.items() if sec in smap]) if flagged else {}
    new_text = text
    changes, open_items = [], []
    for sec, reps in fixes.items():
        if not isinstance(reps, dict):
            continue
        for sid, x in reps.items():
            row = verdicts.get(sid) or next((r for r in smap.get(sec, []) if r["sid"] == sid), None)
            if not row or not x.get("new"):
                continue
            old_s = row["sentence"]
            new_s = "" if str(x["new"]).strip().upper() == "CUT" else str(x["new"]).strip()
            if old_s not in new_text:
                open_items.append({"sid": sid, "reason": "sentence not found verbatim for replacement", "sentence": old_s})
                continue
            cand = new_text.replace(old_s, new_s, 1)
            cand = re.sub(r"[ \t]{2,}", " ", cand)
            before, after = va.check(new_text, P), va.check(cand, P)
            if after["integrity_ok"] and pv.score_rep(after) <= pv.score_rep(before):
                new_text = cand
                changes.append({"sid": sid, "old": old_s, "new": new_s or "CUT", "note": x.get("note", ""),
                                "verdict_before": row.get("verdict", "RULE")})
            else:
                open_items.append({"sid": sid, "reason": "fix made the code validation worse; reverted", "sentence": old_s,
                                   "verdict": row.get("verdict")})
    # ---------- 5 re-verify changed sentences only
    changed_rows = {}
    for c in changes:
        if c["new"] != "CUT":
            sec = c["sid"].split("-")[0]
            ids = [i for i in va.ids_in(c["new"]) if i != "AUTHOR"]
            changed_rows.setdefault(sec, []).append({"sid": c["sid"], "sentence": c["new"], "ids": ids})
    rres = {}
    if changed_rows:
        try:
            rres = R.parallel([(sec, verify_job(sec, rows, "reverify", "reverify")) for sec, rows in changed_rows.items()])
        except pv.BudgetStop as e:
            state["reverify_stop"] = str(e)
    for sec, rows in changed_rows.items():
        got = rres.get(sec) if isinstance(rres.get(sec), dict) else {}
        for r in rows:
            v = got.get(r["sid"])
            c = next(c for c in changes if c["sid"] == r["sid"])
            before = RANK.get(c["verdict_before"], 0) if not c["verdict_before"].startswith("RULE") else 0
            if v is None:
                c["reverify"] = "not re-verified (budget or call failure)"
                verdicts[r["sid"]] = dict(verdicts.get(r["sid"], r), sentence=c["new"], verdict="UNVERIFIED")
                continue
            vv = str(v.get("verdict", "")).upper()
            c["reverify"] = vv
            if RANK.get(vv, -1) >= before:
                verdicts[r["sid"]] = dict(verdicts.get(r["sid"], r), sentence=c["new"], verdict=vv, evidence=v.get("evidence", ""))
            else:   # worse: revert this sentence
                new_text = new_text.replace(c["new"], c["old"], 1)
                c["reverted"] = True
                open_items.append({"sid": r["sid"], "reason": f"fix re-verified worse ({vv}); reverted", "sentence": c["old"],
                                   "verdict": c["verdict_before"]})
    for c in changes:
        if c["new"] == "CUT":
            verdicts.pop(c["sid"], None)
    state["verdicts_after"] = counts(verdicts)
    rules_after = rule_checks(new_text, P, cited_sentences(new_text))
    state["rule_failures_after"] = rules_after
    state["changes"] = changes
    state["validation_after"] = va.summary(va.check(new_text, P))
    state["validation_after_detail"] = va.check(new_text, P)
    remaining = [v for v in verdicts.values() if v["verdict"] not in ("SUPPORTED",)]
    state["remaining_flagged"] = remaining
    state["open"] = open_items
    state["seconds"] = round(time.time() - t0)
    state["step_spend_usd"] = round(R.spent - start_spent, 4)
    state["total_spend_usd"] = round(R.spent, 4)
    if not a.dry_run:
        (D / "ch01_draft_v1.md").write_text(new_text, encoding="utf-8")
        subprocess.run([sys.executable, "-I", str(D / "footnote.py")])
        write_spotcheck(new_text, P, verdicts, remaining)
        (D / "verification_state.json").write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: state[k] for k in ("verdicts_before", "verdicts_after", "step_spend_usd", "total_spend_usd", "seconds")}, indent=1), flush=True)
    print(f"[{ts()}] VERIFY FINISHED", flush=True)


def write_spotcheck(text, P, verdicts, remaining):
    smap = cited_sentences(text)
    rnd = random.Random(1080)
    pick = []
    for sec, rows in smap.items():
        pick += [(sec, r) for r in rnd.sample(rows, min(3, len(rows)))]
    L = ["# Chapter 1 spot-check\n", "Fifteen cited sentences chosen at random (three per section), each beside the exact evidence it cites. "
         "Then every sentence still marked PARTIAL, UNSUPPORTED or MISREPRESENTED after the fixes.\n"]
    for n, (sec, r) in enumerate(pick, 1):
        v = next((x for x in verdicts.values() if x.get("sentence") == r["sentence"]), {})
        L.append(f"## {n}. Section {sec} — verdict: {v.get('verdict', 'n/a')}\n")
        L.append(f"> {r['sentence']}\n")
        for i in r["ids"]:
            if i in P:
                it = P[i]
                L.append(f"- **{i}** — {it['book_title']}, {it['page']}"
                         + (" *(borrowed)*" if "borrowed" in it["flags"] else "") + f"\n  > {' '.join(it['quote'].split())}"
                         + (f"\n  *English rendering:* {it['gloss']}" if it.get("gloss") else ""))
        L.append("")
    L.append("## Sentences still flagged after the fixes\n")
    if not remaining:
        L.append("*None.*")
    for v in remaining:
        L.append(f"- **{v['sid']}** ({v['verdict']}): {v['sentence']}\n  - evidence: {v.get('evidence', '')}\n  - suggested fix: {v.get('fix', '')}")
    (D / "ch01_spotcheck.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
