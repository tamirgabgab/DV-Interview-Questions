#!/usr/bin/env python3
"""Put the generated figures and tables of a question into its page, in place.

    python tools/figures/fill.py 26 27          # rewrite the generated blocks of 0026, 0027
    python tools/figures/fill.py --check 26     # exit 1 when a block is out of date

The generator ``tools/figures/q<id>.py`` defines ``blocks()``: a list of strings (an SVG,
a legend, a Markdown table...). The page marks where each block goes with two comments at
the block's indentation, so the block can sit inside an admonition or a list item:

        <!-- gen 3 -->

        <svg class="perf-chart" ...>...</svg>

        <!-- /gen -->

Everything between the markers is replaced; the rest of the page is never touched.
tools/page_tests.py uses check() so a question test fails when a page copy is stale.
"""

from __future__ import annotations

import importlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
from extract_code import question_path  # noqa: E402

MARK = re.compile(r"^(?P<ind>[ ]*)<!-- gen (?P<n>\d+) -->\n.*?^(?P=ind)<!-- /gen -->$", re.M | re.S)


def generated(qid: int) -> list[str]:
    return importlib.import_module(f"q{qid:04d}").blocks()


def render(ind: str, n: int, block: str) -> str:
    body = [ind + line if line.strip() else "" for line in block.strip("\n").splitlines()]
    return "\n".join([f"{ind}<!-- gen {n} -->", ""] + body + ["", f"{ind}<!-- /gen -->"])


def fill_text(text: str, blocks: list[str]) -> tuple[str, list[str]]:
    """The page with every marked block regenerated, and the list of problems found
    (blocks out of date, missing on the page, or marked but not generated)."""
    problems, seen = [], set()

    def sub(m):
        n = int(m.group("n"))
        seen.add(n)
        if n >= len(blocks):
            problems.append(f"block {n} is marked on the page but the generator has {len(blocks)}")
            return m.group(0)
        new = render(m.group("ind"), n, blocks[n])
        if new != m.group(0):
            problems.append(f"block {n} is out of date")
        return new

    out = MARK.sub(sub, text)
    problems += [f"block {n} has no marker on the page" for n in range(len(blocks)) if n not in seen]
    return out, problems


def check(qid: int) -> list[str]:
    path = question_path(qid)
    return fill_text(path.read_text(encoding="utf-8"), generated(qid))[1]


def fill(qid: int) -> list[str]:
    path = question_path(qid)
    text, problems = fill_text(path.read_text(encoding="utf-8"), generated(qid))
    path.write_text(text, encoding="utf-8")
    return [p for p in problems if "out of date" not in p]


def main(argv: list[str]) -> int:
    check_only = "--check" in argv
    ids = [int(a) for a in argv if a != "--check"]
    bad = 0
    for qid in ids:
        problems = check(qid) if check_only else fill(qid)
        for p in problems:
            print(f"{qid:04d}: {p}")
        bad += bool(problems)
        if not check_only and not problems:
            print(f"{qid:04d}: filled")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
