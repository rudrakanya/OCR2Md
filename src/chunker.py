"""Markdown-aware chunking (§4).

Two-stage, as specified: split on headings first so a chunk never straddles a
section boundary, then split long sections recursively until they fit the token
budget.

The header parsing is hand-rolled rather than using LangChain's
MarkdownHeaderTextSplitter for one concrete reason: this corpus is OCR output
containing ```sanskrit fenced blocks whose verse lines begin with '#'-like
noise, plus `<!-- page N -->` provenance markers and library-stamp junk
headings that must be filtered — none of which that splitter models. The
recursive within-section split, which is the genuinely fiddly part, does use
LangChain's RecursiveCharacterTextSplitter.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Callable, Iterable

from langchain_text_splitters import RecursiveCharacterTextSplitter

from . import textutil

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
PAGE_RE = re.compile(r"<!--\s*page\s+(\d+)\s*-->", re.I)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
TABLE_ROW_RE = re.compile(r"^\s*\|.*\|\s*$")
FOOTNOTE_RE = re.compile(r"^\s*(\[\^[^\]]+\]:|\[\d+\]\s|\*{1,2}\d+\.?\s|\d+\.\s{2,})")
# A "letter" in any script this corpus uses. Anything with none of these is
# markdown furniture (---, ***, |---|---|, page numbers), not content.
LETTER_RE = re.compile(r"[A-Za-zÀ-ɏḀ-ỿऀ-ॿ]")


def has_content(block: str) -> bool:
    """True if a block carries text rather than markdown scaffolding.

    Without this, every `---` rule in the corpus became its own one-token
    chunk: samarangana-sutradhara.md alone contributed dozens of them, each a
    perfectly retrievable embedding of the string "---".
    """
    stripped = COMMENT_RE.sub("", block)
    stripped = re.sub(r"^\s*[-*_=~|:\s]+$", "", stripped, flags=re.M)
    return bool(LETTER_RE.search(stripped))


class ChunkingError(RuntimeError):
    """§3: a book that produces zero chunks is a failure, not an empty result."""


@dataclass
class Chunk:
    chunk_id: str
    text: str                       # original, diacritics intact (§5)
    embed_text: str                 # with contextual header prepended (§4.3)
    text_folded: str                # lexical layer only, sidecar (§5, §6)
    source_path: str
    book_title: str
    heading_path: str
    chunk_index: int
    token_count: int
    language: str
    page_start: int | None = None
    extra: dict = field(default_factory=dict)


@dataclass
class Section:
    heading_path: list[str]
    lines: list[str]
    page_start: int | None


def _compile_junk(patterns: Iterable[str]) -> list[re.Pattern]:
    return [re.compile(p) for p in patterns]


def split_sections(text: str, split_levels: int, junk: list[re.Pattern]) -> list[Section]:
    """Walk the document once, tracking heading stack, fences and page markers."""
    sections: list[Section] = []
    stack: list[str] = []
    current = Section(heading_path=[], lines=[], page_start=None)
    in_fence = False
    page: int | None = None

    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            current.lines.append(line)
            continue

        if not in_fence:
            m_page = PAGE_RE.search(line)
            if m_page:
                page = int(m_page.group(1))
                if current.page_start is None and not any(l.strip() for l in current.lines):
                    current.page_start = page

            m = HEADING_RE.match(line)
            if m:
                level, title = len(m.group(1)), m.group(2).strip()
                title = COMMENT_RE.sub("", title).strip()
                # A junk heading is not a section boundary and never enters the
                # heading path — otherwise every ASI library stamp in the corpus
                # would start a new section named "ACCESSION NO. 52987".
                if not title or any(p.search(title) for p in junk):
                    current.lines.append(line)
                    continue
                if level <= split_levels:
                    if any(l.strip() for l in current.lines):
                        sections.append(current)
                    stack = stack[: level - 1]
                    while len(stack) < level - 1:
                        stack.append("")
                    stack.append(title)
                    current = Section(heading_path=[h for h in stack if h],
                                      lines=[], page_start=page)
                    continue
        current.lines.append(line)

    if any(l.strip() for l in current.lines):
        sections.append(current)
    return sections


def _atomic_blocks(lines: list[str], keep_tables_whole: bool,
                   attach_footnotes: bool) -> list[str]:
    """Group lines into units that must not be split internally: fenced blocks,
    contiguous table rows, and paragraphs (with their trailing footnotes)."""
    blocks: list[str] = []
    buf: list[str] = []
    in_fence = False
    in_table = False

    def flush() -> None:
        if buf and any(l.strip() for l in buf):
            block = "\n".join(buf).strip("\n")
            if has_content(block):
                blocks.append(block)
        buf.clear()

    for line in lines:
        if FENCE_RE.match(line):
            if in_fence:
                buf.append(line)
                in_fence = False
                flush()
            else:
                flush()
                in_fence = True
                buf.append(line)
            continue
        if in_fence:
            buf.append(line)
            continue

        is_row = bool(TABLE_ROW_RE.match(line)) and keep_tables_whole
        if is_row and not in_table:
            flush()
            in_table = True
        elif in_table and not is_row:
            flush()
            in_table = False

        if not line.strip() and not in_table:
            flush()
            continue
        if attach_footnotes and FOOTNOTE_RE.match(line) and blocks and not buf:
            # A footnote line belongs with the passage above it, not alone.
            blocks[-1] = blocks[-1] + "\n" + line
            continue
        buf.append(line)

    flush()
    return blocks


def chunk_document(text: str, *, book_title: str, source_path: str, cfg,
                   token_len: Callable[[str], int]) -> list[Chunk]:
    ck = cfg["chunking"]
    target, overlap = int(ck["target_tokens"]), int(ck["overlap_tokens"])
    min_tok, max_tok = int(ck["min_tokens"]), int(ck["max_tokens"])
    junk = _compile_junk(ck.get("junk_heading_patterns", []))
    split_levels = len(ck.get("split_headers", ["#", "##", "###"]))

    text = textutil.nfc(text)
    if not text.strip():
        raise ChunkingError(f"{source_path}: file is empty")

    recursive = RecursiveCharacterTextSplitter(
        chunk_size=target,
        chunk_overlap=overlap,
        length_function=token_len,
        # Ordered coarse -> fine. The Devanagari danda characters matter: a
        # Sanskrit verse has no full stops, so without them a long ```sanskrit
        # block has no legal split point above the character level.
        separators=["\n\n", "\n", "। ", "॥ ", "। ", ". ", "; ", ", ", " ", ""],
        keep_separator=True,
    )

    pieces: list[tuple[str, list[str], int | None]] = []  # (text, headings, page)
    for sec in split_sections(text, split_levels, junk):
        blocks = _atomic_blocks(sec.lines, bool(ck.get("keep_tables_whole", True)),
                                bool(ck.get("attach_footnotes", True)))
        buf: list[str] = []
        buf_tokens = 0
        for block in blocks:
            btok = token_len(block)
            if btok > max_tok:
                if buf:
                    pieces.append(("\n\n".join(buf), sec.heading_path, sec.page_start))
                    buf, buf_tokens = [], 0
                for part in recursive.split_text(block):
                    if part.strip():
                        pieces.append((part, sec.heading_path, sec.page_start))
                continue
            if buf_tokens + btok > target and buf:
                pieces.append(("\n\n".join(buf), sec.heading_path, sec.page_start))
                # Carry the tail of the previous chunk forward as overlap.
                buf, buf_tokens = _overlap_tail(buf, overlap, token_len)
            buf.append(block)
            buf_tokens += btok
        if buf:
            pieces.append(("\n\n".join(buf), sec.heading_path, sec.page_start))

    pieces = _merge_orphans(pieces, min_tok, max_tok, token_len)

    header_tpl = ck.get("context_header", "[Book: {book} > {headings}]")
    use_header = bool(ck.get("context_header_enabled", True))
    chunks: list[Chunk] = []
    for i, (body, headings, page) in enumerate(pieces):
        body = body.strip()
        if not body:
            continue
        heading_path = " > ".join(headings)
        if use_header:
            head = header_tpl.format(book=book_title,
                                     headings=heading_path or "(no heading)")
            embed_text = f"{head} {body}"
        else:
            embed_text = body
        chunks.append(Chunk(
            chunk_id=make_id(source_path, i),
            text=body,
            embed_text=embed_text,
            text_folded=textutil.fold(body),
            source_path=source_path,
            book_title=book_title,
            heading_path=heading_path,
            chunk_index=i,
            token_count=token_len(body),
            language=textutil.detect_language(body),
            page_start=page,
        ))

    if not chunks:
        raise ChunkingError(f"{source_path}: produced zero chunks")
    return chunks


def _overlap_tail(buf: list[str], overlap: int,
                  token_len: Callable[[str], int]) -> tuple[list[str], int]:
    """Keep whole trailing blocks totalling <= overlap tokens as the next
    chunk's lead-in. Block-level rather than character-level overlap so the
    repeated text is always a complete paragraph."""
    tail: list[str] = []
    total = 0
    for block in reversed(buf):
        t = token_len(block)
        if total + t > overlap:
            break
        tail.insert(0, block)
        total += t
    return tail, total


def _merge_orphans(pieces, min_tok: int, max_tok: int,
                   token_len: Callable[[str], int]):
    """§4.2: fragments under min_tokens are merged into a neighbour rather than
    left as orphan snippets, which retrieve badly and pollute precision.

    Two passes. The first merges only within an identical heading path, which
    keeps `heading_path` honest. The second relaxes that and merges across
    section boundaries, because a short section whose neighbours are also short
    would otherwise never merge at all — that restriction alone left 10.8% of
    chunks under the floor.
    """
    if len(pieces) < 2:
        return pieces
    out: list[list] = [list(p) for p in pieces]
    for strict in (True, False):
        i = 0
        while i < len(out) and len(out) > 1:
            body, headings, page = out[i]
            if token_len(body) >= min_tok:
                i += 1
                continue
            cand: list[tuple[int, int]] = []
            for j in (i - 1, i + 1):
                if not (0 <= j < len(out)):
                    continue
                if strict and out[j][1] != headings:
                    continue
                size = token_len(out[j][0])
                if size + token_len(body) <= max_tok:
                    cand.append((size, j))
            if not cand:
                i += 1
                continue
            # Prefer the smaller neighbour so merging never creates a giant chunk.
            _, j = min(cand)
            if j < i:
                out[j][0] = out[j][0] + "\n\n" + body
            else:
                out[j][0] = body + "\n\n" + out[j][0]
                # The merged chunk starts on the earlier page.
                if page is not None:
                    out[j][2] = page if out[j][2] is None else min(page, out[j][2])
            del out[i]
            if j < i:
                i = j + 1
    return [tuple(p) for p in out]


def make_id(relative_path: str, chunk_index: int) -> str:
    """§3: deterministic id, so re-running upserts instead of duplicating."""
    return hashlib.sha1(
        f"{relative_path}:{chunk_index}".encode("utf-8")
    ).hexdigest()
