import sys
from pathlib import Path

# Make the tools importable from every test: extract_code and page_tests in tools/, and
# the modules of tools/checks/, tools/build/ and tools/authoring/.
sys.path[:0] = [str(Path(__file__).resolve().parent.parent / "tools" / d) for d in ("", "checks", "build", "authoring")]
