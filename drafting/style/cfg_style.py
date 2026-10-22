from pathlib import Path
CH = 0
VERSION = 'style'
D = Path(str(Path(__file__).resolve().parents[2] / "drafting" / "style"))
SECTIONS = []
OUTLINE = D / 'none.md'
PACK = D / 'none.json'
LOG = D / 'api_log'
OUT = D / 'none.md'
WMIN, WMAX = 0, 0
CONFLICTS = {}
CHAPTER_BRIEF = ''
BUDGET, RESERVE = 2.00, 0.0
