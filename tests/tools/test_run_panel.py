"""The run panel's Python side (docs/javascripts/py_run.py) on every question's starting
code: the page code and tests/<id>/demo.py run as the browser runs them, without an error,
and every print() with an expected value in its comment prints that value."""

import contextlib
import importlib.util
import io

import pytest

import extract_code
from extract_code import ROOT

spec = importlib.util.spec_from_file_location("py_run", ROOT / "docs" / "javascripts" / "py_run.py")
py_run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(py_run)

DEMOS = sorted(ROOT.glob("tests/*/demo.py"))


@pytest.mark.parametrize("demo", DEMOS, ids=[d.parent.name for d in DEMOS])
def test_starting_code_runs_and_prints_its_comments(demo):
    page = extract_code.question_path(demo.parent.name).read_text(encoding="utf-8")
    solution = "\n".join(extract_code.blocks_from_text(page, "python"))
    code = demo.read_text(encoding="utf-8")
    with contextlib.redirect_stdout(io.StringIO()):
        result = py_run.run(solution, code)
    assert [c for c in result if not c["ok"]] == []
    # every commented print that runs once is checked
    assert len(result) == sum(1 for e in py_run.expected_values(code)
                              if code.splitlines()[e[0] - 1].lstrip().startswith("print("))


def test_values_and_notes():
    assert py_run.matches("8   (part a)", "8")
    assert py_run.matches("(3, (1, 1)): no pyramids", "(3, (1, 1))")
    assert py_run.matches("{0: 10, 495: 990}", "{0: 10, 495: 990}")
    assert not py_run.matches("495", "49")
    assert not py_run.matches("(9, (0, 2), (2, 4))", "(9,")
    assert py_run.value_of("{0: 10, 495: 990}") == "{0: 10, 495: 990}"
    assert py_run.value_of("(3, 1): no pyramids") == "(3, 1)"
    # a label before the value
    assert py_run.matches("(6, 2, 3)", "long only, fast:  (6, 2, 3)")
    assert not py_run.matches("3)", "long only: (6, 2, 3)")
    assert not py_run.matches("3", "x: 13")
    assert py_run.matches("0.5", "P(X=1) = 0.5")
    assert py_run.matches("0110", "N = 5:   0110")
    # a comparison or a second label is not a label
    for got in ("5 != 7", "5 == 7", "5 <= 7", "5 >= 7", "a = 5 b = 7", "a = 5, b = 7", "x: 5, y: 7"):
        assert not py_run.matches("7", got), got


def test_checks_by_line():
    code = "x = 3\nprint(x)  # 3\nprint(x + 1)  # 5\nfor i in range(2):\n    print(i)  # 0\nprint(\n  x)  # 3\n"
    with contextlib.redirect_stdout(io.StringIO()):
        result = py_run.run("", code)
    assert [(c["line"], c["ok"]) for c in result] == [(2, True), (3, False), (7, True)]
    assert result[1]["got"] == "4" and result[1]["expected"] == "5"


def test_solution_is_a_module_and_a_namespace():
    with contextlib.redirect_stdout(io.StringIO()) as out:
        py_run.run("def f():\n    return 7\n", "from solution import f as g\nprint(g(), f())\n")
    assert out.getvalue() == "7 7\n"
