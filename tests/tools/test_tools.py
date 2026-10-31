"""Tests of the authoring tools: tools/new_question.py, tools/catalog.py, tools/figures/fill.py
and the shared chart helpers in tools/figures/charts.py."""

import shutil
import sys

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tools" / "figures"))
import catalog  # noqa: E402
import charts  # noqa: E402
import fill  # noqa: E402
import lint_pages  # noqa: E402
import new_question  # noqa: E402


def make_root(tmp_path):
    (tmp_path / "templates").mkdir()
    shutil.copy(ROOT / "templates" / "question.md", tmp_path / "templates" / "question.md")
    (tmp_path / "docs" / "questions" / "junior").mkdir(parents=True)
    (tmp_path / "docs" / "questions" / "junior" / "0041-old.md").write_text("---\nid: 41\ntitle: ישנה\nlevel: junior\n---\n", encoding="utf-8")
    return tmp_path


def test_new_question_with_figures_and_code(tmp_path):
    root = make_root(tmp_path)
    written = new_question.create(root, "junior", "medium", "cake-split", "חלוקת עוגה",
                                  ["math", "sequences"], figures=True, code=True, today="2026-10-20",
                                  kind="math")
    names = {p.relative_to(root).as_posix() for p in written}
    assert names == {"docs/questions/junior/0042-cake-split.md", "tests/0042/test_0042.py",
                     "tests/0042/test_0042_code.py", "tests/0042/tb.sv", "tests/0042/demo.py",
                     "tools/figures/q0042.py", "CATALOG.md"}
    page = (root / "docs/questions/junior/0042-cake-split.md").read_text(encoding="utf-8")
    assert page.startswith("---\nid: 42\ntitle: חלוקת עוגה\nlevel: junior\ndifficulty: medium\nkind: math\n"
                           "tags: [math, sequences]\nsource: \"\"\nadded: 2026-10-20\n---\n\n## השאלה\n")
    assert "    <!-- gen 0 -->" in page
    assert lint_pages.lint(root / "docs/questions/junior/0042-cake-split.md") == []
    # the generator stub fills the page
    gen = root / "tools/figures/q0042.py"
    ns = {"__file__": str(gen), "__name__": "q0042"}
    exec(gen.read_text(encoding="utf-8"), ns)
    text, problems = fill.fill_text(page, ns["blocks"]())
    assert problems == ["block 0 is out of date"] and "<!-- figure 0" in text
    rows = [l for l in (root / "CATALOG.md").read_text(encoding="utf-8").split("\n") if l.startswith("| 00")]
    assert rows == ["| 0041 | [ישנה](https://tamirgabgab.github.io/DV-Interview-Questions/questions/junior/0041-old/) | junior (ג'וניור) |",
                    "| 0042 | [חלוקת עוגה](https://tamirgabgab.github.io/DV-Interview-Questions/questions/junior/0042-cake-split/) | junior (ג'וניור) |"]


def test_catalog_is_up_to_date():
    assert (ROOT / "CATALOG.md").read_text(encoding="utf-8") == catalog.render(ROOT), "run python tools/catalog.py"
    assert (ROOT / "README.md").read_text(encoding="utf-8") == catalog.render_readme(ROOT), "run python tools/catalog.py"


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


def test_lint_cost_chips(tmp_path):
    page = (ROOT / "templates/question.md").read_text(encoding="utf-8").replace("id: 0 ", "id: 42 ")
    path = tmp_path / "0042-x.md"
    path.write_text(page, encoding="utf-8")
    assert lint_pages.lint(path) == []
    path.write_text(page.replace("<!-- cost: זמן", "<!-- cost: O(n) זמן"), encoding="utf-8")
    assert any("Hebrew label" in p for p in lint_pages.lint(path))
    path.write_text(page.replace("    <!-- cost: זמן \\( O(n) \\) | זיכרון \\( O(1) \\) -->\n", ""), encoding="utf-8")
    assert any("no <!-- cost" in p for p in lint_pages.lint(path))


def test_lint_topic_names(tmp_path):
    # every topic of the site has a Hebrew name; an unknown one is a warning, not a problem
    page = (ROOT / "templates/question.md").read_text(encoding="utf-8").replace("id: 0 ", "id: 42 ")
    path = tmp_path / "0042-x.md"
    path.write_text(page, encoding="utf-8")
    warnings: list[str] = []
    assert lint_pages.lint(path, warnings) == [] and not [w for w in warnings if "TOPICS" in w]
    path.write_text(page.replace("tags: [", "tags: [no-such-topic, ", 1), encoding="utf-8")
    warnings = []
    assert lint_pages.lint(path, warnings) == []
    assert any("'no-such-topic'" in w for w in warnings)


def test_display_math_is_a_paragraph_of_its_own(tmp_path):
    """Display math run into the next line shows as raw TeX (0041's short answer did)."""
    root = make_root(tmp_path)
    new_question.create(root, "junior", "medium", "cake-split", "חלוקת עוגה", ["math"],
                        figures=False, code=False, today="2026-10-20", kind="math")
    path = root / "docs/questions/junior/0042-cake-split.md"
    page = path.read_text(encoding="utf-8")
    path.write_text(page.replace("## השאלה\n", "## השאלה\n\n\\[\nE = 1\n\\]\nול- הסכום.\n", 1), encoding="utf-8")
    assert any("needs a blank line after it" in p for p in lint_pages.lint(path))
    path.write_text(page.replace("## השאלה\n", "## השאלה\n\n\\[\nE = 1\n\\]\n\nול- הסכום.\n", 1), encoding="utf-8")
    assert not any("display math" in p for p in lint_pages.lint(path))


def test_every_question_in_a_study_path(monkeypatch, tmp_path):
    """lint_pages names a question that is in no study path; today there is none."""
    import lint_pages

    assert lint_pages.lint_paths() == []
    # a copy of the questions with an extra page that no path lists is named
    q = tmp_path / "questions"
    shutil.copytree(lint_pages.QUESTIONS, q)
    shutil.copytree(lint_pages.QUESTIONS.parent / "paths", tmp_path / "paths")
    (q / "student" / "0999-orphan.md").write_text("---\nid: 999\n---\n", encoding="utf-8")
    monkeypatch.setattr(lint_pages, "QUESTIONS", q)
    assert lint_pages.lint_paths() == ["0999-orphan.md: in no study path (add it to a docs/paths/*.md)"]
