#!/usr/bin/env python3
"""Is a change text only? The CI's fast lane (.github/workflows/deploy.yml).

    python tools/checks/text_only.py BASE HEAD          # prints the verdict, exits 0 either way
    python tools/checks/text_only.py BASE HEAD --github # also writes fast= and ids= to $GITHUB_OUTPUT

A change is text only when every file it touches is a question page
(docs/questions/<level>/<id>-<slug>.md) or a file the workflow ignores anyway (README,
HANDOFF and the like, or videos/), and in every page only prose changed: the front matter,
the fenced code blocks, the generated blocks between `<!-- gen n -->` and `<!-- /gen -->`,
and every line that carries HTML a script reads (an explorer box, a figure, a stepper) are
the same before and after. Such a change cannot touch the tested code, the figures or the
boxes, so the fast lane checks only what prose can break: the
lint, the build, the links, the touched questions' Python tests and the phone check of the
touched pages (CONTRIBUTING.md, "The fast lane").

Anything else (a new or deleted page, a tool, a test, a script, a stylesheet, the hook, a
workflow) is not text only and runs every check.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

PAGE = re.compile(r"^docs/questions/[a-z]+/(\d{4})-[^/]+\.md$")
# Files the workflow ignores (paths-ignore) or that are not part of the site.
IGNORED = re.compile(r"^(README\.md|CONTRIBUTING\.md|CLAUDE\.md|notes/.*|videos/.*)$")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
GEN_OPEN = re.compile(r"<!--\s*gen\s+\d+\s*-->")
GEN_CLOSE = re.compile(r"<!--\s*/gen\s*-->")
# A line with HTML that a script or the hook reads: its attributes and data must not change.
ACTIVE = re.compile(r"<(div|svg|section|figure|table|span|details)\b[^>]*"
                    r"(class=\"[^\"]*(explorer|stepper|steps-fig|sf-fig|figure)|data-)")


def protected(text: str) -> list[str]:
    """The lines of a page that prose edits must leave alone, in order."""
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    # the front matter
    if lines and lines[0].strip() == "---":
        j = 1
        while j < len(lines) and lines[j].strip() != "---":
            j += 1
        out += lines[: j + 1]
        i = j + 1
    fence = None
    in_gen = False
    for line in lines[i:]:
        if fence is not None:
            out.append(line)
            m = FENCE.match(line)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
                fence = None
            continue
        if in_gen:
            out.append(line)
            if GEN_CLOSE.search(line):
                in_gen = False
            continue
        m = FENCE.match(line)
        if m:
            fence = m.group(1)
            out.append(line)
        elif GEN_OPEN.search(line):
            out.append(line)
            in_gen = not GEN_CLOSE.search(line)
        elif ACTIVE.search(line) or GEN_CLOSE.search(line):
            out.append(line)
    return [line.strip() for line in out]


def verdict(files: dict[str, tuple[str | None, str | None]]) -> tuple[bool, list[str], str]:
    """files: path -> (old text or None, new text or None). Returns (text only, ids, why)."""
    ids: list[str] = []
    for path, (old, new) in sorted(files.items()):
        if IGNORED.match(path):
            continue
        m = PAGE.match(path)
        if not m:
            return False, [], f"{path} is not a question page"
        if old is None or new is None:
            return False, [], f"{path} was added or deleted"
        if protected(old) != protected(new):
            return False, [], f"{path} changes code, figures, front matter or a box"
        ids.append(m.group(1))
    if not ids:
        return True, [], "only files outside the site (videos, notes)"
    return True, ids, "only prose of " + ", ".join(ids)


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def _show(rev: str, path: str) -> str | None:
    r = subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    base, head = argv[0], argv[1]
    try:
        if not base or set(base) == {"0"}:
            raise ValueError("no base commit (a new branch)")
        names = [n for n in _git("diff", "--name-only", base, head).split("\n") if n]
        # ignored files (videos are binary) are not read
        files = {n: (None, None) if IGNORED.match(n) else (_show(base, n), _show(head, n)) for n in names}
        fast, ids, why = verdict(files)
    except (subprocess.CalledProcessError, ValueError) as e:
        fast, ids, why = False, [], f"cannot compare: {e}"
    print(f"text only: {fast} ({why})")
    if "--github" in argv and os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
            f.write(f"fast={'true' if fast else 'false'}\n")
            f.write(f"ids={' '.join(ids)}\n")
            f.write(f"pages={'|'.join(ids)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
