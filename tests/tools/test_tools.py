"""Tests of the authoring tools: tools/new_question.py, tools/figures/fill.py and the
shared chart helpers in tools/figures/charts.py."""

import shutil
import sys

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tools" / "figures"))
import charts  # noqa: E402
import fill  # noqa: E402
import lint_pages  # noqa: E402
import new_question  # noqa: E402


def make_root(tmp_path):
    (tmp_path / "templates").mkdir()
    shutil.copy(ROOT / "templates" / "question.md", tmp_path / "templates" / "question.md")
    shutil.copy(ROOT / "README.md", tmp_path / "README.md")
    (tmp_path / "docs" / "questions" / "junior").mkdir(parents=True)
    (tmp_path / "docs" / "questions" / "junior" / "0041-old.md").write_text("---\nid: 41\n---\n")
    return tmp_path


def test_new_question_with_figures_and_code(tmp_path):
    root = make_root(tmp_path)
    written = new_question.create(root, "junior", "medium", "cake-split", "חלוקת עוגה",
                                  ["math", "sequences"], figures=True, code=True, today="2026-10-20")
    names = {p.relative_to(root).as_posix() for p in written}
    assert names == {"docs/questions/junior/0042-cake-split.md", "tests/0042/test_0042.py",
                     "tests/0042/test_0042_code.py", "tests/0042/tb.sv", "tests/0042/demo.py",
                     "tools/figures/q0042.py", "README.md"}
    page = (root / "docs/questions/junior/0042-cake-split.md").read_text(encoding="utf-8")
    assert page.startswith("---\nid: 42\ntitle: חלוקת עוגה\nlevel: junior\ndifficulty: medium\n"
                           "tags: [math, sequences]\nsource: \"\"\nadded: 2026-10-20\n---\n\n## השאלה\n")
    assert "    <!-- gen 0 -->" in page
    assert lint_pages.lint(root / "docs/questions/junior/0042-cake-split.md") == []
    # the generator stub fills the page
    gen = root / "tools/figures/q0042.py"
    ns = {"__file__": str(gen), "__name__": "q0042"}
    exec(gen.read_text(encoding="utf-8"), ns)
    text, problems = fill.fill_text(page, ns["blocks"]())
    assert problems == ["block 0 is out of date"] and "<!-- figure 0" in text
    readme = (root / "README.md").read_text(encoding="utf-8").split("\n")
    row = next(i for i, l in enumerate(readme) if l.startswith("| 0042 |"))
    assert readme[row - 1].startswith("| 00") and "junior | 🟡 medium | math, sequences |" in readme[row]


def test_new_question_refuses_to_overwrite(tmp_path):
    root = make_root(tmp_path)
    (root / "tests" / "0042").mkdir(parents=True)
    (root / "tests" / "0042" / "test_0042.py").write_text("keep")
    try:
        new_question.create(root, "junior", "easy", "x", "שאלה", [])
    except FileExistsError:
        pass
    else:
        raise AssertionError("expected FileExistsError")
    assert (root / "tests" / "0042" / "test_0042.py").read_text() == "keep"
    assert not (root / "docs/questions/junior/0042-x.md").exists()


def test_fill_markers():
    page = "intro\n\n    <!-- gen 0 -->\n\n    old\n\n    <!-- /gen -->\n\nmiddle\n<!-- gen 1 -->\n\nx\n\n<!-- /gen -->\n"
    text, problems = fill.fill_text(page, ["new\nlines", "x"])
    assert problems == ["block 0 is out of date"]
    assert text == ("intro\n\n    <!-- gen 0 -->\n\n    new\n    lines\n\n    <!-- /gen -->\n\nmiddle\n"
                    "<!-- gen 1 -->\n\nx\n\n<!-- /gen -->\n")
    assert fill.fill_text(text, ["new\nlines", "x"])[1] == []
    assert fill.fill_text(text, ["new\nlines", "x", "y"])[1] == ["block 2 has no marker on the page"]


def test_chart_mapping():
    c = charts.Chart("t", slots=10, y_max=2)
    assert c.X(0.5) == c.x0 and abs(c.X(10.5) - c.x1) < 1e-9
    assert c.Y(0) == c.base and c.Y(2) == c.top
    lg = charts.Chart("t", x_max=1, log=True, y_min=0.1, y_max=10)
    assert abs(lg.Y(1) - (lg.base + lg.top) / 2) < 1e-9 and lg.X(1) == lg.x1
    svg = c.grid_y([0, 1, 2]).bar(3, 1.5, "by-enum", title="t").axis("k").svg()
    assert svg.startswith('<svg class="perf-chart"') and svg.endswith("</svg>") and "#" not in svg
