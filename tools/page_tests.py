"""Helpers shared by the question tests.

- ``node_json(script)`` runs a Node script and returns its JSON output; the test is
  skipped when Node is not installed (CI installs it).
- ``explorer_require()`` is the ``require`` expression of the explorer models: the core and
  every kind file of docs/javascripts/explorer/, merged by tools/explorer_node.js.
- ``assert_figures_match(qid)`` checks that every generated block on the page equals the
  generator output (see tools/figures/fill.py).
- ``run_cocotb(...)`` runs a cocotb testbench (a page's Python, with pyuvm or plain cocotb)
  on Verilator against SystemVerilog sources and returns each test's result and the log;
  the test is skipped when cocotb or Verilator is not installed (CI installs both).
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



def run_cocotb(name: str, module: str, sources: dict[str, str], toplevel: str, tests: list[str] | None = None,
               timescale: tuple[str, str] = ("1ns", "1ps")) -> tuple[dict[str, bool], str]:
    """Run the cocotb tests of ``module`` (Python source, written as ``<name>_tb.py``) on
    Verilator against ``sources`` (file name -> SystemVerilog text), top level ``toplevel``.
    Returns ({test name: passed}, the log). The build lives in .cache/cocotb/<name>/ and is
    rebuilt only when the sources change; ``tests`` picks some of the module's tests."""
    import hashlib
    import importlib.util
    import os
    import xml.etree.ElementTree as ET

    import pytest

    if importlib.util.find_spec("cocotb") is None:
        pytest.skip("cocotb is not installed (pip install -r requirements/dev.txt)")
    if not shutil.which("verilator"):
        pytest.skip("verilator is not installed")
    from cocotb_tools.runner import get_runner

    work = ROOT / ".cache" / "cocotb" / name
    work.mkdir(parents=True, exist_ok=True)
    for f, text in sources.items():
        path = work / f
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            path.write_text(text, encoding="utf-8")
    mod = f"{name}_tb"
    (work / f"{mod}.py").write_text(module, encoding="utf-8")
    key = hashlib.sha256("".join(f + t for f, t in sorted(sources.items())).encode()).hexdigest()[:16]
    stamp = work / "build" / "sources.sha"
    fresh = not (stamp.exists() and stamp.read_text() == key)
    runner = get_runner("verilator")
    log = work / "run.log"
    with open(log, "w", encoding="utf-8") as out:
        fd, err = os.dup(1), os.dup(2)
        os.dup2(out.fileno(), 1)
        os.dup2(out.fileno(), 2)
        try:
            runner.build(sources=[work / f for f in sources], hdl_toplevel=toplevel, build_dir=work / "build",
                         always=fresh, timescale=timescale, build_args=["-Wno-fatal", "-Wno-lint", "-Wno-style"])
            stamp.write_text(key)
            xml = work / "results.xml"
            xml.unlink(missing_ok=True)
            try:    # the runner exits when a test fails; the results file still says which
                runner.test(hdl_toplevel=toplevel, test_module=mod, testcase=tests, build_dir=work / "build",
                            test_dir=work, results_xml=str(xml))
            except SystemExit:
                pass
        finally:
            os.dup2(fd, 1)
            os.dup2(err, 2)
            os.close(fd)
            os.close(err)
    text = log.read_text(encoding="utf-8", errors="replace")
    if not xml.exists():
        raise AssertionError("cocotb produced no results:\n" + "\n".join(text.splitlines()[-30:]))
    results = {}
    for case in ET.parse(xml).getroot().iter("testcase"):
        results[case.get("name")] = case.find("failure") is None and case.find("error") is None
    return results, text
