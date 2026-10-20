#!/usr/bin/env python3
"""Start a new question: the page, its tests folder, a figure generator and the README row.

    python tools/new_question.py --level junior --difficulty medium --slug cake-split \\
        --title "חלוקת עוגה" --tags math,sequences [--figures] [--code]

Takes the next free id, copies templates/question.md to docs/questions/<level>/<id>-<slug>.md
with the front matter filled in, and creates:

- tests/<id>/test_<id>.py: a stub test (with --figures, the "page blocks match the
  generator" test; with --code, a load_python() smoke test);
- tools/figures/q<id>.py with --figures: a generator with an empty blocks() list, and the
  first gen markers on the page (see tools/figures/fill.py);
- tests/<id>/tb.sv and tests/<id>/demo.py with --code: a testbench that pulls the page's
  SystemVerilog block and the starting code of the run panel;
- a row at the end of the README catalog, to be completed by hand.

Nothing is overwritten: the script stops if a file it would write already exists.
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path

LEVELS = ("student", "junior", "senior", "staff")
DIFFICULTIES = {"easy": "🟢 easy", "medium": "🟡 medium", "hard": "🔴 hard"}


def next_id(root: Path) -> int:
    ids = [int(p.name[:4]) for p in (root / "docs" / "questions").glob("*/[0-9][0-9][0-9][0-9]-*.md")]
    return max(ids, default=0) + 1


def page_text(template: str, qid: int, title: str, level: str, difficulty: str, tags: list[str],
              today: str, figures: bool) -> str:
    front = (f"---\nid: {qid}\ntitle: {title}\nlevel: {level}\ndifficulty: {difficulty}\n"
             f"tags: [{', '.join(tags)}]\nsource: \"\"\nadded: {today}\n---\n")
    body = "\n" + template[template.index("\n---", 3) + 4:].lstrip("\n")
    if figures:
        body = body.replace("    #### הרעיון { .sol-idea }\n",
                            "    #### הרעיון { .sol-idea }\n\n    <!-- gen 0 -->\n\n    <!-- /gen -->\n", 1)
    return front + body


FIGURES_TEST = '''"""Question {qid:04d}: checks of the page's numbers (to write) and of the generated blocks."""


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match({qid})
'''

NUMBERS_TEST = '''"""Question {qid:04d}: checks of the numbers the page states (to write)."""


def test_numbers():
    assert True  # TODO: recompute every number on the page
'''

CODE_TEST = '''"""Question {qid:04d}: tests of the page's Python code (it runs as published)."""

from extract_code import load_python


def test_page_code_loads():
    ns = load_python({qid})
    assert ns, "the page has no Python block yet"
'''

GENERATOR = '''#!/usr/bin/env python3
"""Figures and tables of question {qid:04d}.

    python tools/figures/fill.py {qid}        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. Shared chart helpers are in charts.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402,F401


def blocks():
    """The generated blocks, in page order."""
    return [
        "<!-- figure 0: replace with a drawing -->",
    ]


if __name__ == "__main__":
    print("\\n\\n".join(blocks()))
'''

TB = '''// Question {qid:04d}: testbench. //@page pulls the page's SystemVerilog block that contains
// the given text; the run must print a line starting with PASS.
module tb;
  //@page my_function
  initial begin
    $display("PASS");
    $finish;
  end
endmodule
'''

DEMO = '''# Starting code of the run panel of question {qid:04d}: the page's Python code is loaded
# as solution.py; call its functions here.
from solution import *  # noqa: F401,F403

print("ready")
'''


def catalog_row(qid: int, title: str, level: str, difficulty: str, tags: list[str]) -> str:
    return f"| {qid:04d} | TODO English title ({title}) | {level} | {DIFFICULTIES[difficulty]} | {', '.join(tags)} |"


def create(root: Path, level: str, difficulty: str, slug: str, title: str, tags: list[str],
           figures: bool = False, code: bool = False, today: str | None = None) -> list[Path]:
    if level not in LEVELS or difficulty not in DIFFICULTIES:
        raise ValueError(f"level must be one of {LEVELS}, difficulty one of {tuple(DIFFICULTIES)}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("slug: lower-case words joined by hyphens")
    qid = next_id(root)
    today = today or datetime.date.today().isoformat()
    tid = f"{qid:04d}"
    files = {root / "docs" / "questions" / level / f"{tid}-{slug}.md":
             page_text((root / "templates" / "question.md").read_text(encoding="utf-8"),
                       qid, title, level, difficulty, tags, today, figures)}
    test = FIGURES_TEST if figures else CODE_TEST if code else NUMBERS_TEST
    files[root / "tests" / tid / f"test_{tid}.py"] = test.format(qid=qid)
    if figures:
        files[root / "tools" / "figures" / f"q{tid}.py"] = GENERATOR.format(qid=qid)
    if code:
        if figures:   # both: keep the figures test and add the code test next to it
            files[root / "tests" / tid / f"test_{tid}_code.py"] = CODE_TEST.format(qid=qid)
        files[root / "tests" / tid / "tb.sv"] = TB.format(qid=qid)
        files[root / "tests" / tid / "demo.py"] = DEMO.format(qid=qid)
    existing = [p for p in files if p.exists()]
    if existing:
        raise FileExistsError(", ".join(str(p) for p in existing))
    for path, text in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    readme = root / "README.md"
    lines = readme.read_text(encoding="utf-8").split("\n")
    end = next(i for i, l in enumerate(lines) if l.startswith("Update this table"))
    last = max(i for i in range(end) if re.match(r"\| \d{4} \|", lines[i]))
    lines.insert(last + 1, catalog_row(qid, title, level, difficulty, tags))
    readme.write_text("\n".join(lines), encoding="utf-8")
    return list(files) + [readme]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--level", required=True, choices=LEVELS)
    ap.add_argument("--difficulty", required=True, choices=tuple(DIFFICULTIES))
    ap.add_argument("--slug", required=True, help="lower-case words joined by hyphens")
    ap.add_argument("--title", required=True, help="the Hebrew title")
    ap.add_argument("--tags", default="", help="comma-separated topic tags")
    ap.add_argument("--figures", action="store_true", help="add a figure generator and gen markers")
    ap.add_argument("--code", action="store_true", help="add tb.sv, demo.py and a code test")
    args = ap.parse_args(argv)
    root = Path(__file__).resolve().parent.parent
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    written = create(root, args.level, args.difficulty, args.slug, args.title, tags, args.figures, args.code)
    for p in written:
        print(f"wrote {p.relative_to(root)}")
    print("next: write the page, then python tools/lint_pages.py and python tools/run_tests.py <id>")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
