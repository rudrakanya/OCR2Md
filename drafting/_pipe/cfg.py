"""Chapter configuration for the shared drafting toolkit.

Every _pipe module reads the active chapter's settings from the Python file named in the environment variable
UDAY_CFG (e.g. drafting/ch03/cfg_ch03.py). One chapter per process, so chapters can run concurrently.

Required attributes of a chapter config:
  CH (int), D (Path: chapter folder), SECTIONS (["3.1", ...]), OUTLINE, PACK (Paths), LOG (Path), OUT (Path: working draft),
  VERSION ("v1"), TITLE, DOCX_NAME, WMIN, WMAX, TOTAL_TARGET, CONFLICTS ({sec: [(name, [regex, ...])]}),
  CHAPTER_BRIEF (str: chapter-specific routing and content rules), OPEN_IN, CLOSE_OUT (str),
  BASELINE (Path or None: earlier draft whose sections enter the judge as a candidate), VOICE_SRC (Path or None),
  BUDGET (float), RESERVE (float), extra_rules(text, P, smap) -> list of rule failures (optional).
"""
import importlib.util
import os
import sys
from pathlib import Path

ROOT = Path(str(Path(__file__).resolve().parents[2]))
PIPE = Path(__file__).parent


def _load():
    p = os.environ.get("UDAY_CFG")
    if not p:
        sys.exit("set UDAY_CFG to a chapter config file (e.g. drafting/ch03/cfg_ch03.py)")
    spec = importlib.util.spec_from_file_location("uday_cfg", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


C = _load()
