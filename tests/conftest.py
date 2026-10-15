import sys
from pathlib import Path

# Make tools/extract_code.py importable from every test.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
