"""Helpers shared by the question tests.

- ``node_json(script)`` runs a Node script and returns its JSON output; the test is
  skipped when Node is not installed (CI installs it).
- ``explorer_require()`` is the ``require`` expression of docs/javascripts/explorer.js.
- ``assert_figures_match(qid)`` checks that every generated block on the page equals the
  generator output (see tools/figures/fill.py).
"""

from __future__ import annotations

import json
import shutil
import subprocess

from extract_code import ROOT


def node_json(script: str):
    import pytest

    node = shutil.which("node")
    if not node:
        pytest.skip("node is not installed")
    out = subprocess.run([node, "-e", script], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def explorer_require() -> str:
    return f"require({json.dumps(str(ROOT / 'docs' / 'javascripts' / 'explorer.js'))})"


def assert_figures_match(qid: int) -> None:
    import sys

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import fill  # noqa: E402

    stale = fill.check(qid)
    assert not stale, f"blocks out of date on page {qid:04d}: {stale} (run python tools/figures/fill.py {qid})"
