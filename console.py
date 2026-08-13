#!/usr/bin/env python3
"""
console.py — make stdout safe for IAST and Devanagari on Windows.

The Windows console defaults to cp1252, which cannot encode 'ā', let alone
'श्री'. Any script in this pipeline that prints a chapter title, a heading trail
or a retrieved excerpt will raise UnicodeEncodeError without this. Call
`use_utf8()` at the top of a CLI's main().
"""
import sys


def use_utf8():
    """Switch stdout/stderr to UTF-8, replacing anything the terminal can't draw."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except (ValueError, OSError):           # already detached / redirected oddly
                pass
