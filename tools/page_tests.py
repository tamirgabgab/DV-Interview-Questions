"""Helpers shared by the question tests.

- ``node_json(script)`` runs a Node script and returns its JSON output; the test is
  skipped when Node is not installed (CI installs it).
- ``explorer_require()`` is the ``require`` expression of the explorer models: the core and
  every kind file of docs/javascripts/explorer/, merged by tools/explorer_node.js.
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
    return f"require({json.dumps(str(ROOT / 'tools' / 'explorer_node.js'))})"


def assert_figures_match(qid: int) -> None:
    import sys

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import fill  # noqa: E402

    stale = fill.check(qid)
    assert not stale, f"blocks out of date on page {qid:04d}: {stale} (run python tools/figures/fill.py {qid})"


def fig_steps(qid: int) -> list[tuple[list[str], set[str]]]:
    """The figures beside the steps on a question's page (div.steps-fig): per box, what each
    step lights (one string per step, "a b>c d" for a walk) and the keys (data-fig) of the
    figure in the box."""
    import re

    page = next((ROOT / "docs" / "questions").rglob(f"{qid:04d}-*.md")).read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r"<div class=\"steps-fig\" data-fig-steps='([^']+)' markdown>(.*?)<div class=\"steps\"", page, re.S):
        out.append((json.loads(m.group(1)), set(re.findall(r'data-fig="([^"]+)"', m.group(2)))))
    return out


def lit(plan: list[str]) -> set[str]:
    """Every key a list of steps lights."""
    return {k for step in plan for group in step.split(">") for k in group.split()}

