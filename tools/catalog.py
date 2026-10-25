#!/usr/bin/env python3
"""Write CATALOG.md: every question's id, its Hebrew title as a link to its page on the
live site, and its level, read from the pages' front matter.

    python tools/catalog.py           # rewrite CATALOG.md
    python tools/catalog.py --check   # exit 1 when CATALOG.md is out of date

tools/new_question.py rewrites it when it adds a page; a test checks it is up to date.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://tamirgabgab.github.io/DV-Interview-Questions/"
LEVELS = {"student": "student (סטודנט)", "junior": "junior (ג'וניור)", "senior": "senior (סניור)"}
FIELD = re.compile(r"^(id|title|level):\s*(.+?)\s*$", re.M)


def pages(root: Path) -> list[tuple[int, str, str, str]]:
    """(id, title, level, path on the site) of every question page, by id."""
    out = []
    for p in sorted((root / "docs" / "questions").glob("*/[0-9][0-9][0-9][0-9]-*.md")):
        text = p.read_text(encoding="utf-8")
        front = dict(FIELD.findall(text[:text.index("\n---", 3)]))
        out.append((int(front["id"]), front["title"], front["level"],
                    p.relative_to(root / "docs").with_suffix("").as_posix() + "/"))
    return sorted(out)


def render(root: Path) -> str:
    rows = [f"| {qid:04d} | [{title}]({SITE}{path}) | {LEVELS.get(level, level)} |"
            for qid, title, level, path in pages(root)]
    return ("# Catalog\n\n"
            f"All {len(rows)} questions, with links to their pages on the [live site]({SITE}). Written by\n"
            "`python tools/catalog.py` from the pages' front matter; do not edit by hand.\n\n"
            "| Id | Question | Level |\n|----|----------|-------|\n" + "\n".join(rows) + "\n")


def write(root: Path = ROOT) -> Path:
    path = root / "CATALOG.md"
    path.write_text(render(root), encoding="utf-8")
    return path


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="only check that CATALOG.md is up to date")
    if ap.parse_args(argv).check:
        path = ROOT / "CATALOG.md"
        if not path.exists() or path.read_text(encoding="utf-8") != render(ROOT):
            print("CATALOG.md is out of date: run python tools/catalog.py")
            return 1
        print("CATALOG.md is up to date")
        return 0
    print(f"wrote {write().relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
