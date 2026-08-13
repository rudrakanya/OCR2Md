#!/usr/bin/env python3
"""
entities.py — the canonical entity registry and alias resolver.

For a manuscript organised around named persons, places and monuments, this is
the authority file. It does three jobs no similarity score can do:

  1. **Identity.** Udayeśvara and Nīlakaṇṭheśvara are one temple. No tokenizer,
     no bi-encoder and no edit distance can know that; it has to be asserted.
  2. **Disambiguation.** Udayapura in Vidisha district is not Udaipur in
     Rajasthan. Left to fuzzy matching the two fold together at any threshold
     loose enough to also catch 'Udaypur'.
  3. **Alias expansion.** A passage naming only one variant becomes retrievable
     by all of them, via the sparse index's `ents` stream (kb_store §3.1).

It retires v1's `difflib.get_close_matches(..., cutoff=0.86)` for every term the
registry knows: resolution becomes an exact lookup on a folded alias. The fuzzy
path survives only as a fallback for terms *not* in the registry, and every time
it fires is a signal that the registry needs another row — `--gaps` lists them.

Storage: kb/entities.json is the editable source of truth, mirrored into the
SQLite tables on `--sync`. Editing the JSON by hand is expected and supported;
`curated: true` marks a row a human has confirmed, and extraction never
overwrites a curated row.

    from entities import EntityIndex
    ents = EntityIndex.load()
    ents.resolve("Nilakantheshwar")        -> "E:MON:001"
    ents.mentions(passage_text)            -> {"E:MON:001": 3, ...}
    ents.unevidenced(question, passages)   -> ["Meghadūta"]

CLI:
    python entities.py --seed              # write the starter registry
    python entities.py --extract           # propose entities from the corpus
    python entities.py --sync              # JSON -> SQLite (+ rebuild ents stream)
    python entities.py --list --type place
    python entities.py --gaps              # terms that needed the fuzzy fallback
"""
import argparse
import collections
import difflib
import json
import os
import re
from pathlib import Path

from textnorm import WORD_RE, fold, proper_nouns
from kb_store import KBStore

KB_DIR = Path(os.environ.get("KB_DIR", "kb"))
REGISTRY = KB_DIR / "entities.json"

# The design doc's nine types, plus two the corpus forces. An architectural
# style (bhūmija, nāgara) and an administrative office (mahāsāmanta) are named
# entities that behave exactly like the others for retrieval and grounding, and
# filing them under "title" would make the type column lie.
ENTITY_TYPES = ("person", "dynasty", "place", "monument", "inscription",
                "text", "deity", "title", "date-event", "style", "office")

TYPE_CODE = {"person": "PER", "dynasty": "DYN", "place": "PLC", "monument": "MON",
             "inscription": "INS", "text": "TXT", "deity": "DEI", "title": "TTL",
             "date-event": "EVT", "style": "STY", "office": "OFC"}

# ---------------------------------------------------------------------------
# Seed registry.
#
# This is a STUB, not a finished authority file. It covers the entities the
# manuscript turns on and the confusions that have already cost this project
# something — but every row is `curated: false` until a human has checked it,
# and the `first_attested` values in particular are the loosest part. Run
# `--extract` to propose the rest from the corpus, then curate.
# ---------------------------------------------------------------------------
SEED = [
    # -- places --
    dict(id="E:PLC:001", canonical="Udayapura", type="place",
         aliases=["Udaypur", "Udayapur", "Udaipur (Vidisha)", "उदयपुर", "Udayapura",
                  "Udayapuram"],
         first_attested="1059 CE",
         notes="Vidisha district, Madhya Pradesh. NOT Udaipur, Rajasthan — the two "
               "fold together under any fuzzy matcher loose enough to catch 'Udaypur'."),
    dict(id="E:PLC:002", canonical="Vidiśā", type="place",
         aliases=["Vidisha", "Bhilsa", "Besnagar", "विदिशा", "Bhelsa", "Vidisa"],
         notes="District town; Bhilsa is the medieval/colonial name, Besnagar the ancient site."),
    dict(id="E:PLC:003", canonical="Betwā", type="place",
         aliases=["Betwa", "Vetravatī", "Vetravati", "बेतवा", "Betwa river"],
         notes="River; the valley that frames the site's hydrology chapters."),
    dict(id="E:PLC:004", canonical="Mālava", type="place",
         aliases=["Malwa", "Malava", "मालवा", "Mālwā", "Avanti", "Avantī"],
         notes="Region. Avanti is the ancient name for substantially the same territory."),
    dict(id="E:PLC:005", canonical="Dhārā", type="place",
         aliases=["Dhar", "Dhara", "धार", "Dhārānagarī"],
         notes="Paramāra capital under Bhoja."),
    dict(id="E:PLC:006", canonical="Sāñcī", type="place",
         aliases=["Sanchi", "Sānchī", "सांची", "Kakanaya", "Kākanāda"]),
    dict(id="E:PLC:007", canonical="Ujjayinī", type="place",
         aliases=["Ujjain", "Ujjayini", "उज्जैन", "Avantikā"]),

    # -- dynasty --
    dict(id="E:DYN:001", canonical="Paramāra", type="dynasty",
         aliases=["Paramara", "Parmar", "Pawar", "Powar", "परमार", "Pramāra", "Pramara"],
         notes="The Malwa dynasty; 'Parmar/Pawar' are the later Rajput clan forms."),
    dict(id="E:DYN:002", canonical="Caulukya", type="dynasty",
         aliases=["Chaulukya", "Solanki", "Chalukya of Gujarat", "चौलुक्य"],
         notes="Gujarat rivals. Distinguish from the Deccan Cālukyas where sources conflate them."),
    dict(id="E:DYN:003", canonical="Kacchapaghāta", type="dynasty",
         aliases=["Kachchhapaghata", "Kacchapaghata", "कच्छपघात"]),
    dict(id="E:DYN:004", canonical="Candella", type="dynasty",
         aliases=["Chandella", "Chandela", "चंदेल", "Candela"]),

    # -- persons --
    dict(id="E:PER:001", canonical="Bhoja", type="person",
         aliases=["Bhojadeva", "Bhoj", "Raja Bhoj", "Rājā Bhoja", "भोज", "भोजदेव",
                  "Bhojarāja", "Bhoja I"],
         first_attested="r. c. 1010–1055 CE",
         notes="Paramāra king; the reign the corpus is densest on."),
    dict(id="E:PER:002", canonical="Udayāditya", type="person",
         aliases=["Udayaditya", "उदयादित्य", "Udayāditya-deva", "Udayadityadeva"],
         first_attested="r. c. 1059–1087 CE",
         notes="Paramāra; builder of the Udayeśvara temple. Do not conflate with "
               "the place Udayapura, which folds close to the same key."),
    dict(id="E:PER:003", canonical="Muñja", type="person",
         aliases=["Munja", "Vākpati II", "Vakpati", "मुंज", "Vākpatirāja"]),
    dict(id="E:PER:004", canonical="Sindhurāja", type="person",
         aliases=["Sindhuraja", "सिंधुराज", "Sindhurajа"]),
    dict(id="E:PER:005", canonical="Jayasiṃha", type="person",
         aliases=["Jayasimha", "जयसिंह", "Jayasinha"]),
    dict(id="E:PER:006", canonical="Naravarman", type="person",
         aliases=["Naravarma", "नरवर्मन्", "Naravarmadeva"]),
    dict(id="E:PER:007", canonical="Lakṣmadeva", type="person",
         aliases=["Lakshmadeva", "लक्ष्मदेव", "Laksmadeva"]),
    dict(id="E:PER:008", canonical="Yaśovarman", type="person",
         aliases=["Yashovarman", "यशोवर्मन्", "Yasovarman"]),
    dict(id="E:PER:009", canonical="Kālidāsa", type="person",
         aliases=["Kalidasa", "कालिदास", "Kālidāsa"]),
    dict(id="E:PER:010", canonical="Alexander Cunningham", type="person",
         aliases=["Cunningham", "A. Cunningham", "Sir Alexander Cunningham"],
         notes="ASI surveyor; his attributions are often superseded, his measurements are not."),

    # -- monuments --
    dict(id="E:MON:001", canonical="Udayeśvara", type="monument",
         aliases=["Udayesvara", "Udayeshvara", "Nīlakaṇṭheśvara", "Nilakanthesvara",
                  "Nilkantheshwar", "Neelkantheshwar", "नीलकण्ठेश्वर", "उदयेश्वर",
                  "Udayeśvara temple", "Nilkanth temple"],
         first_attested="1059–1080 CE",
         notes="ONE structure under two names. This identity is the single most "
               "important row in the registry — a lexical matcher cannot infer it."),
    dict(id="E:MON:002", canonical="Heliodorus pillar", type="monument",
         aliases=["Heliodorus", "Heliodoros", "Garuda pillar", "Kham Baba", "Besnagar pillar"]),
    dict(id="E:MON:003", canonical="Bhojeśvara", type="monument",
         aliases=["Bhojeshwar", "Bhojpur temple", "भोजेश्वर", "Bhojesvara"]),

    # -- texts --
    dict(id="E:TXT:001", canonical="Samarāṅgaṇasūtradhāra", type="text",
         aliases=["Samarangana Sutradhara", "Samarāṅgaṇa-sūtradhāra", "समरांगणसूत्रधार",
                  "Samarangansutradhara", "Samarāṅgaṇa"],
         notes="Śilpa treatise attributed to Bhoja; in the corpus as a bilingual edition."),
    dict(id="E:TXT:002", canonical="Meghadūta", type="text",
         aliases=["Meghaduta", "मेघदूत", "Cloud Messenger"],
         notes="Kālidāsa. Present here BECAUSE chapter 1 once cited it with no "
               "supporting passage — registry membership does not imply corpus coverage."),

    # -- inscriptions --
    dict(id="E:INS:001", canonical="Udayapura praśasti", type="inscription",
         aliases=["Udayapur prashasti", "Udaypur inscription", "Udayapura inscription"]),
    dict(id="E:INS:002", canonical="varṇanāgakṛpāṇikā", type="inscription",
         aliases=["varnanagakrpanika", "serpentine scimitar", "nāgakṛpāṇikā",
                  "serpentine scimitar of letters"],
         notes="The Udaypur serpentine-scimitar inscription."),

    # -- deities --
    dict(id="E:DEI:001", canonical="Śiva", type="deity",
         aliases=["Shiva", "शिव", "Siva", "Mahādeva", "Mahadeva", "Nīlakaṇṭha", "Nilakantha"],
         notes="Nīlakaṇṭha is an epithet of Śiva AND part of the temple's name — "
               "resolution must not silently merge E:DEI:001 with E:MON:001."),
    dict(id="E:DEI:002", canonical="Viṣṇu", type="deity",
         aliases=["Vishnu", "विष्णु", "Visnu"]),

    # -- styles --
    dict(id="E:STY:001", canonical="Bhūmija", type="style",
         aliases=["Bhumija", "भूमिज", "bhūmija mode"],
         notes="The śikhara mode the Udayeśvara temple exemplifies."),
    dict(id="E:STY:002", canonical="Nāgara", type="style",
         aliases=["Nagara", "नागर"]),
    dict(id="E:STY:003", canonical="Śekharī", type="style",
         aliases=["Sekhari", "Shekhari", "शेखरी"]),
]


def _loose_key(folded):
    """Drop a trailing Sanskrit -a: 'udayesvara' and 'udayesvar' meet.

    Sanskrit keeps the final short a; Hindi and most anglicised spellings drop
    it, so the same name reaches the corpus both ways ('Udayeśvara' /
    'Udayeshwar', 'Nīlakaṇṭheśvara' / 'Nilkantheshwar'). This key is consulted
    only when resolving a surface form to an entity — never for the sparse
    index and never for grounding, where the looseness would let an
    unsupported name pass as attested.
    """
    return re.sub(r"a$", "", folded)


def _norm_entry(e):
    """Fill defaults and fold the alias set once."""
    aliases = list(dict.fromkeys([e["canonical"], *e.get("aliases", [])]))
    return {
        "id": e["id"],
        "canonical": e["canonical"],
        "type": e["type"],
        "aliases": aliases,
        "first_attested": e.get("first_attested", ""),
        "notes": e.get("notes", ""),
        "curated": bool(e.get("curated", False)),
    }


def write_seed(path=REGISTRY, force=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        print(f"{path} exists; use --force to overwrite (this discards curation).")
        return None
    entries = [_norm_entry(e) for e in SEED]
    path.write_text(json.dumps({"version": 1, "entities": entries},
                               ensure_ascii=False, indent=1), encoding="utf-8")
    return entries


class EntityIndex:
    """Loaded registry with folded-alias resolution."""

    def __init__(self, entries):
        self.entries = [_norm_entry(e) for e in entries]
        self.by_id = {e["id"]: e for e in self.entries}
        self._alias = collections.defaultdict(list)
        self._loose = collections.defaultdict(list)
        self._collisions = collections.defaultdict(set)
        for e in self.entries:
            for a in e["aliases"]:
                k = fold(a)
                if not k:
                    continue
                if e["id"] not in self._alias[k]:
                    self._alias[k].append(e["id"])
                if len(self._alias[k]) > 1:
                    self._collisions[k].update(self._alias[k])
                lk = _loose_key(k)
                if e["id"] not in self._loose[lk]:
                    self._loose[lk].append(e["id"])
        # Terms that fell through to the fuzzy fallback — a to-do list for curation.
        self.fuzzy_hits = collections.Counter()
        self.loose_hits = collections.Counter()

    # -- construction --------------------------------------------------------

    @classmethod
    def load(cls, path=REGISTRY, store=None):
        """Load from JSON if present, else from SQLite, else from the seed."""
        if Path(path).exists():
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            return cls(data["entities"])
        if store is not None:
            rows = store.db.execute("SELECT * FROM entities").fetchall()
            if rows:
                out = []
                for r in rows:
                    al = store.db.execute(
                        "SELECT alias FROM entity_aliases WHERE entity_id=?", (r["entity_id"],))
                    out.append(dict(id=r["entity_id"], canonical=r["canonical"],
                                    type=r["type"], first_attested=r["first_attested"],
                                    notes=r["notes"], curated=bool(r["curated"]),
                                    aliases=[a["alias"] for a in al]))
                return cls(out)
        return cls([_norm_entry(e) for e in SEED])

    # -- resolution ----------------------------------------------------------

    def alias_map(self):
        """{folded_alias: [entity_id, ...]} — what kb_store.build() indexes with.

        Strict keys only. A loose key here would tag chunks with entities they
        do not actually name, which is a fabrication vector in the index itself.
        """
        return dict(self._alias)

    def query_alias_map(self):
        """As alias_map, plus trailing-a variants — for expanding a *query*.

        Over-reaching on the query side costs recall of precision at worst: an
        extra candidate that the reranker then scores and the floor may drop.
        Over-reaching on the index side would be a silent corruption. The two
        maps are therefore deliberately different, and only this one is loose.
        """
        out = {k: list(v) for k, v in self._alias.items()}
        for k, ids in self._loose.items():
            out.setdefault(k, [])
            for i in ids:
                if i not in out[k]:
                    out[k].append(i)
        return out

    def collisions(self):
        """Folded aliases claimed by more than one entity — curation must fix these.

        Left alone, a collision makes the `ents` stream retrieve both entities
        for either name, which is precisely the Udayapura/Udaipur failure the
        registry exists to prevent.
        """
        return {k: sorted(v) for k, v in self._collisions.items()}

    def near_duplicates(self):
        """Pairs that are probably one entity recorded twice.

        Alias collisions catch identical folded forms. They do not catch
        'Bhūmija' vs 'Bhūmija style', or 'Vidiśā' vs 'Vidiśā district' — an
        extraction pass produces these routinely, and left in place they split
        one entity's mentions across two ids, so neither retrieves the whole of
        it. Containment on the folded key finds them; judgement resolves them.
        """
        keys = [(e, fold(e["canonical"])) for e in self.entries]
        pairs = []
        for i, (a, ka) in enumerate(keys):
            for b, kb in keys[i + 1:]:
                if not ka or not kb or ka == kb:
                    continue
                if (ka.startswith(kb) or kb.startswith(ka)) and abs(len(ka) - len(kb)) <= 12:
                    pairs.append((a, b))
        return pairs

    def merge_prefix_duplicates(self):
        """Auto-merge the mechanical duplicates; leave the judgement calls alone.

        An extraction pass reliably emits both 'Paramāra' and 'Paramāra
        dynasty', 'Bhūmija' and 'Bhūmija style'. Merging those is bookkeeping,
        not scholarship. Two guards keep it from merging anything real:

          same type   'Udayapura' (place) and 'Udayapura praśasti'
                      (inscription) are a town and a stone. Never merged.
          word bound  'Arjuna' is a prefix of 'Arjunavarman' and 'Agni' of
                      'Agnipurāṇa', but neither at a word boundary. Never merged.

        Returns the list of (kept, absorbed) pairs.
        """
        by_key = {fold(e["canonical"]): e for e in self.entries}
        merged, drop = [], set()
        for e in sorted(self.entries, key=lambda x: len(x["canonical"]), reverse=True):
            if e["id"] in drop or e["curated"]:
                continue
            words = e["canonical"].split()
            for i in range(len(words) - 1, 0, -1):       # longest prefix first
                host = by_key.get(fold(" ".join(words[:i])))
                if host and host["id"] != e["id"] and host["type"] == e["type"] \
                        and host["id"] not in drop:
                    for a in e["aliases"]:
                        if a not in host["aliases"]:
                            host["aliases"].append(a)
                    merged.append((host, e))
                    drop.add(e["id"])
                    break
        if drop:
            self.entries = [e for e in self.entries if e["id"] not in drop]
            self.__init__(self.entries)                  # rebuild the alias maps
        return merged

    def resolve(self, term, loose=True):
        """Entity id for a surface form, or None.

        Exact folded-alias lookup first. `loose` then allows the trailing-a
        variant, which is a spelling convention rather than a different name.
        Every loose hit is counted: it means the corpus (or the outline) uses a
        surface form the registry does not list, and `--gaps` reports it so the
        alias can be added and the lookup made exact.
        """
        k = fold(term)
        ids = self._alias.get(k)
        if ids:
            return ids[0]
        if loose:
            ids = self._loose.get(_loose_key(k))
            if ids:
                self.loose_hits[term] += 1
                return ids[0]
        return None

    def resolve_all(self, term):
        return list(self._alias.get(fold(term), ()))

    def mentions(self, text):
        """{entity_id: count} for one passage."""
        counts = collections.Counter()
        for w in WORD_RE.findall(text or ""):
            for eid in self._alias.get(fold(w), ()):
                counts[eid] += 1
        # Multi-word aliases ("Heliodorus pillar", "Raja Bhoj") never survive
        # word-by-word folding, so they are matched against the folded stream.
        folded_all = " ".join(fold(w) for w in WORD_RE.findall(text or ""))
        for e in self.entries:
            for a in e["aliases"]:
                if " " in a.strip():
                    k = " ".join(fold(w) for w in a.split())
                    if k.strip() and k in folded_all:
                        counts[e["id"]] += 1
        return dict(counts)

    # -- grounding (replaces v1's difflib path) ------------------------------

    def attested(self, term, tokens, folded_blob=""):
        """Is `term` supported by evidence whose folded tokens are `tokens`?

        Registry-first: if the term resolves to an entity, ANY alias of that
        entity counts as attestation — which is how a passage saying
        'Nīlakaṇṭheśvara' supports a sentence about 'Udayeśvara'.
        """
        # Strict resolution here: the loose trailing-a key is fine for deciding
        # *which* entity a query means, but using it to decide whether a claim
        # is supported would let a near-miss name count as attested.
        eid = self.resolve(term, loose=False)
        if eid:
            for a in self.by_id[eid]["aliases"]:
                k = fold(a)
                if not k:
                    continue
                if k in tokens:
                    return True
                if " " in a.strip():
                    multi = " ".join(fold(w) for w in a.split())
                    if multi.strip() and multi in folded_blob:
                        return True
            return False
        # Unregistered term: fall back to the v1 heuristic, and record it.
        k = fold(term)
        if not k:
            return True
        self.fuzzy_hits[term] += 1
        if any(k in t or t in k for t in tokens if len(t) >= 4):
            return True
        return bool(difflib.get_close_matches(k, list(tokens), n=1, cutoff=0.86))

    def unevidenced(self, question, passages, extra_text=""):
        """Proper nouns named in a question that no retrieved passage supports.

        `passages` may be dicts with a 'text' key or plain strings. Title Case
        headings must not be passed in as `question` — see textnorm.proper_nouns.
        """
        terms = proper_nouns(question)
        if not terms:
            return []
        blob = "\n".join(p["text"] if isinstance(p, dict) else str(p) for p in passages)
        blob = f"{blob}\n{extra_text}"
        toks = {fold(w) for w in WORD_RE.findall(blob)}
        toks.discard("")
        folded_blob = " ".join(fold(w) for w in WORD_RE.findall(blob))
        missing, seen = [], set()
        for t in terms:
            k = fold(t)
            if k and k not in seen and not self.attested(t, toks, folded_blob):
                seen.add(k)
                missing.append(t)
        return missing

    # -- persistence ---------------------------------------------------------

    def sync(self, store):
        """Mirror the registry into SQLite. Curated rows are never clobbered."""
        db = store.db
        with db:
            keep = {r["entity_id"] for r in
                    db.execute("SELECT entity_id FROM entities WHERE curated=1")}
            for e in self.entries:
                if e["id"] in keep and not e["curated"]:
                    continue                     # DB row is curated, JSON row is not
                db.execute(
                    "INSERT INTO entities (entity_id, canonical, type, first_attested,"
                    " notes, curated) VALUES (?,?,?,?,?,?) "
                    "ON CONFLICT(entity_id) DO UPDATE SET canonical=excluded.canonical,"
                    " type=excluded.type, first_attested=excluded.first_attested,"
                    " notes=excluded.notes, curated=excluded.curated",
                    (e["id"], e["canonical"], e["type"], e["first_attested"],
                     e["notes"], int(e["curated"])))
                db.execute("DELETE FROM entity_aliases WHERE entity_id=?", (e["id"],))
                for a in e["aliases"]:
                    db.execute("INSERT OR IGNORE INTO entity_aliases (entity_id, alias, folded)"
                               " VALUES (?,?,?)", (e["id"], a, fold(a)))
        return len(self.entries)

    def save(self, path=REGISTRY):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(
            json.dumps({"version": 1, "entities": self.entries}, ensure_ascii=False, indent=1),
            encoding="utf-8")

    def next_id(self, etype):
        code = TYPE_CODE.get(etype, "MSC")
        used = [int(m.group(1)) for e in self.entries
                for m in [re.match(rf"E:{code}:(\d+)$", e["id"])] if m]
        return f"E:{code}:{max(used, default=0) + 1:03d}"


# ---------------------------------------------------------------------------
# Extraction (§2.3): propose registry rows from the corpus.
# ---------------------------------------------------------------------------

EXTRACT_SYSTEM = """You are building an authority file for a scholarly history of the \
Udayeśvara (Nīlakaṇṭheśvara) temple at Udaypur, Vidisha district, and the Paramāra dynasty of Malwa.

You will be given surface forms found in the source corpus, with frequencies, and the entities \
already registered. Group the surface forms into distinct real-world entities.

Rules:
- Return ONLY entities that are genuine named things: persons, dynasties, places, monuments, \
inscriptions, texts, deities, titles, date-events, architectural styles, administrative offices.
- Do NOT return common nouns, adjectives, sentence fragments, OCR noise, or modern scholars' \
surnames unless they are cited authorities in this field.
- Group every spelling variant of one entity together, including Devanagari and IAST forms.
- NEVER merge two genuinely different entities that merely look alike. If unsure, keep separate \
and say so in `notes`.
- Do not re-propose an entity already registered; add missing aliases to it instead, via `add_aliases`.
- `canonical` must be the scholarly IAST form.

Return JSON only:
{"new": [{"canonical": "...", "type": "...", "aliases": ["..."], "notes": "..."}],
 "add_aliases": [{"id": "E:PER:001", "aliases": ["..."]}]}"""


def candidate_terms(store, min_count=8, limit=400, index=None):
    """Frequent capitalised terms in the corpus that the registry does not know."""
    counts = collections.Counter()
    for r in store.db.execute("SELECT text FROM chunks"):
        for w in proper_nouns(r["text"]):
            counts[w] += 1
    out = []
    for term, n in counts.most_common():
        if n < min_count:
            break
        if index and index.resolve(term):
            continue
        out.append((term, n))
        if len(out) >= limit:
            break
    return out


def extract(store, index, client=None, model=None, batch=120, min_count=8, limit=400):
    """Propose new entities and aliases from the corpus. Returns (n_new, n_alias)."""
    from llm import complete_json, get_client
    from config import CFG
    client = client or get_client()
    model = model or CFG.comprehension.model

    cands = candidate_terms(store, min_count=min_count, limit=limit, index=index)
    if not cands:
        print("No unregistered terms above the frequency floor.")
        return 0, 0
    print(f"{len(cands)} unregistered surface forms above {min_count} occurrences")

    known = [{"id": e["id"], "canonical": e["canonical"], "type": e["type"]}
             for e in index.entries]
    n_new = n_alias = 0
    for i in range(0, len(cands), batch):
        window = cands[i:i + batch]
        msg = [
            {"role": "system", "content": EXTRACT_SYSTEM},
            {"role": "user", "content":
                "Already registered:\n" + json.dumps(known, ensure_ascii=False) +
                "\n\nSurface forms (term, occurrences):\n" +
                json.dumps(window, ensure_ascii=False)},
        ]
        print(f"  batch {i // batch + 1}: {len(window)} terms ...", flush=True)
        data = complete_json(client, model, msg, max_tokens=8000, temperature=0.1)

        for e in data.get("new", []):
            etype = e.get("type", "").strip()
            if etype not in ENTITY_TYPES or not e.get("canonical"):
                continue
            if index.resolve(e["canonical"]):
                continue
            row = _norm_entry(dict(id=index.next_id(etype), canonical=e["canonical"],
                                   type=etype, aliases=e.get("aliases", []),
                                   notes=e.get("notes", ""), curated=False))
            index.entries.append(row)
            index.by_id[row["id"]] = row
            for a in row["aliases"]:
                k = fold(a)
                if k and row["id"] not in index._alias[k]:
                    index._alias[k].append(row["id"])
            n_new += 1

        for a in data.get("add_aliases", []):
            e = index.by_id.get(a.get("id", ""))
            if not e:
                continue
            for alias in a.get("aliases", []):
                if alias not in e["aliases"]:
                    e["aliases"].append(alias)
                    k = fold(alias)
                    if k and e["id"] not in index._alias[k]:
                        index._alias[k].append(e["id"])
                    n_alias += 1
    return n_new, n_alias


def main():
    from console import use_utf8
    use_utf8()
    ap = argparse.ArgumentParser(description="Build and query the entity registry")
    ap.add_argument("--seed", action="store_true", help="write the starter registry")
    ap.add_argument("--force", action="store_true", help="overwrite an existing registry")
    ap.add_argument("--extract", action="store_true", help="propose entities from the corpus")
    ap.add_argument("--sync", action="store_true", help="mirror JSON into SQLite")
    ap.add_argument("--reindex", action="store_true",
                    help="rebuild the sparse index's entity stream (needs chunks.jsonl)")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--type", help="filter --list by type")
    ap.add_argument("--resolve", help="resolve one surface form")
    ap.add_argument("--check", action="store_true", help="report alias collisions")
    ap.add_argument("--merge", action="store_true",
                    help="auto-merge mechanical duplicates ('X' + 'X dynasty')")
    ap.add_argument("--gaps", action="store_true",
                    help="surface forms in the corpus that only resolve loosely or not at all")
    ap.add_argument("--min-count", type=int, default=8)
    ap.add_argument("--limit", type=int, default=400)
    args = ap.parse_args()

    if args.seed:
        got = write_seed(force=args.force)
        if got:
            print(f"Wrote {len(got)} seed entities -> {REGISTRY}")
            print("Every row is curated:false. Review it — this is an authority file.")

    index = EntityIndex.load()
    store = KBStore()

    if args.extract:
        n_new, n_alias = extract(store, index, min_count=args.min_count, limit=args.limit)
        index.save()
        print(f"+{n_new} entities, +{n_alias} aliases -> {REGISTRY} (all curated:false)")

    if args.merge:
        pairs = index.merge_prefix_duplicates()
        for host, gone in pairs:
            print(f"  merged {gone['id']} '{gone['canonical']}' -> "
                  f"{host['id']} '{host['canonical']}'")
        index.save()
        print(f"{len(pairs)} mechanical duplicate(s) merged; "
              f"{len(index.entries)} entities remain")

    if args.check or args.extract or args.seed or args.merge:
        coll = index.collisions()
        if coll:
            print(f"\n⚠ {len(coll)} alias collision(s) — two entities share a folded form:")
            for k, ids in sorted(coll.items())[:20]:
                names = " / ".join(index.by_id[i]["canonical"] for i in ids)
                print(f"    {k:24s} {names}")
            print("  Curate these: an unresolved collision retrieves both entities for either name.")
        else:
            print("\nNo alias collisions.")

        dupes = index.near_duplicates()
        if dupes:
            print(f"\n⚠ {len(dupes)} probable duplicate pair(s) — one entity recorded twice "
                  f"splits its mentions across two ids:")
            for a, b in dupes[:25]:
                print(f"    {a['id']} {a['canonical']:26s} ({a['type']:10s})"
                      f"  ~  {b['id']} {b['canonical']} ({b['type']})")
            print("  Merge each pair by hand in kb/entities.json, then --sync --reindex.")

    if args.sync or args.extract or args.seed or args.merge:
        n = index.sync(store)
        print(f"Synced {n} entities into {store.path}")

    if args.reindex:
        chunks_path = KB_DIR / "chunks.jsonl"
        if not chunks_path.exists():
            print(f"ERROR: {chunks_path} not found — run build_kb.py first"); return
        chunks = [json.loads(l) for l in chunks_path.read_text(encoding="utf-8").splitlines()]
        n = store.build(chunks, alias_map=index.alias_map(), stamp=store.stamp())
        st = store.stats()
        print(f"Reindexed {n} chunks; {st['mentions']:,} entity mentions "
              f"across {st['entities']} entities")

    if args.gaps:
        # Two kinds of gap, reported separately because they need different fixes.
        cands = candidate_terms(store, min_count=args.min_count, limit=args.limit, index=None)
        loose, unknown = [], []
        for term, n in cands:
            if index.resolve(term, loose=False):
                continue
            (loose if index.resolve(term, loose=True) else unknown).append((term, n))
        print(f"\n{len(loose)} surface form(s) resolve only loosely — add each as an "
              f"explicit alias to make the lookup exact:")
        for term, n in loose[:40]:
            print(f"    {term:32s} {n:5d}×  -> {index.resolve(term)} "
                  f"({index.by_id[index.resolve(term)]['canonical']})")
        print(f"\n{len(unknown)} frequent surface form(s) the registry does not know at all. "
              f"Most will be common nouns or OCR noise; the named things among them belong "
              f"in the registry:")
        for term, n in unknown[:60]:
            print(f"    {term:32s} {n:5d}×")

    if args.resolve:
        eid = index.resolve(args.resolve)
        if eid:
            e = index.by_id[eid]
            print(f"{eid}  {e['canonical']}  ({e['type']})")
            print(f"  aliases: {', '.join(e['aliases'])}")
            if e["notes"]:
                print(f"  notes: {e['notes']}")
        else:
            print(f"'{args.resolve}' is not in the registry (folds to '{fold(args.resolve)}')")

    if args.list:
        rows = [e for e in index.entries if not args.type or e["type"] == args.type]
        for e in sorted(rows, key=lambda x: (x["type"], x["canonical"])):
            mark = "✓" if e["curated"] else " "
            print(f"{mark} {e['id']:12s} {e['type']:11s} {e['canonical']:28s} "
                  f"{len(e['aliases'])} aliases")
        print(f"\n{len(rows)} entities "
              f"({sum(1 for e in rows if e['curated'])} curated)")


if __name__ == "__main__":
    main()
