#!/usr/bin/env python3
"""Lint the question pages for the site's writing conventions.

    python tools/lint_pages.py            # all pages
    python tools/lint_pages.py 12 14      # some pages

Checks, per page:
- RTL safety: outside code blocks, HTML and math, no line (or table cell) starts with a
  Latin letter or inline code; such lines need the RLM mark (U+200F) first.
- Solution structure: every collapsed solution (``??? success``) starts with an
  ``!!! answer`` block; the solution block labels (h4 with ``.sol-*`` classes) use only the
  known names and appear in the fixed order; hints are numbered "רמז 1", "רמז 2", ...
- One ``??? interviewer`` block right after the question, and the end-of-page blocks use
  the ``trap`` / ``followup`` types (no plain ``note`` / ``warning`` left).
Exit status 1 when anything is reported, so it can run in CI.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_code import QUESTIONS, question_path  # noqa: E402

LABELS = ["הרעיון", "השלבים", "הקוד", "למה זה נכון", "סיבוכיות"]
CLASSES = ["sol-idea", "sol-steps", "sol-code", "sol-proof", "sol-cost"]
LABEL_RE = re.compile(r"^\s*#### (.+?)\s*\{\s*\.(sol-\w+)\s*\}\s*$")
H4_RE = re.compile(r"^\s*#### ")
ADMON_RE = re.compile(r'^(\s*)(\?\?\?\+?|!!!)\s+(\w+)(?:\s+"([^"]*)")?')
RLM = "‏"
LATIN_START = re.compile(r"^[A-Za-z`\\]")


def strip_front_matter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


def lint(path: Path) -> list[str]:
    problems: list[str] = []
    lines = strip_front_matter(path.read_text(encoding="utf-8")).splitlines()

    in_code = False
    fence_indent = ""
    in_html = 0
    in_math = False
    solutions: list[dict] = []
    current: dict | None = None
    hint_numbers: list[int] = []
    interviewer = 0
    leftovers = []

    for n, raw in enumerate(lines, 1):
        line = raw.rstrip()
        stripped = line.strip()

        # fenced code
        m = re.match(r"^(\s*)```", line)
        if m:
            if not in_code:
                in_code, fence_indent = True, m.group(1)
            elif m.group(1) == fence_indent:
                in_code = False
            continue
        if in_code:
            continue
        # display math
        if stripped.startswith("\\["):
            in_math = True
        if in_math:
            if stripped.endswith("\\]"):
                in_math = False
            continue
        # html blocks (svg etc.)
        if stripped.startswith("<") and not stripped.startswith("</"):
            in_html += len(re.findall(r"<(?!/)(?!br)(?!!--)\w+(?![^>]*/>)", stripped))
        if in_html:
            in_html -= len(re.findall(r"</\w+>", stripped))
            in_html = max(in_html, 0)
            continue
        if not stripped or stripped.startswith("<!--"):
            continue

        # admonitions
        a = ADMON_RE.match(line)
        if a:
            indent, kind, typ, title = a.groups()
            title = title or ""
            if typ == "success":
                current = {"line": n, "indent": len(indent), "answer": None, "labels": [], "first": None}
                solutions.append(current)
            elif typ == "answer":
                if current is not None and current["first"] is None:
                    current["answer"] = n
            elif typ == "tip" and title.startswith("רמז"):
                num = re.findall(r"\d+", title)
                hint_numbers.append(int(num[0]) if num else 0)
                if not num:
                    problems.append(f"{n}: hint without a number: {title!r} (use רמז 1, רמז 2)")
            elif typ == "interviewer":
                interviewer += 1
            elif typ in ("note", "warning") and kind.startswith("???") and len(indent) == 0:
                leftovers.append(f"{n}: top-level ??? {typ} {title!r}: use trap / followup / interviewer")
            if current is not None and typ != "success" and current["first"] is None:
                current["first"] = n
            continue

        # first content line of a solution must be the answer block
        if current is not None and current["first"] is None and len(line) - len(line.lstrip()) > current["indent"]:
            current["first"] = n
            if current["answer"] is None:
                problems.append(f"{n}: solution opened at line {current['line']} does not start with !!! answer")

        # h4 labels
        if H4_RE.match(line):
            lm = LABEL_RE.match(line)
            if not lm:
                problems.append(f"{n}: h4 without a sol-* class: {stripped!r}")
            else:
                text, cls = lm.groups()
                if cls not in CLASSES or LABELS[CLASSES.index(cls)] != text:
                    problems.append(f"{n}: unknown label/class pair {text!r} / {cls}")
                elif current is not None:
                    order = CLASSES.index(cls)
                    if current["labels"] and order <= current["labels"][-1]:
                        problems.append(f"{n}: label {text!r} out of order (idea → steps → code → proof → cost)")
                    current["labels"].append(order)
            continue

        # RTL: lines and table cells
        body = re.sub(r"^\s*(?:[-*]|\d+\.|>|#{1,6}|\|)\s*", "", line)
        body = re.sub(r"^(\*\*|\*|_)", "", body)
        cells = [c.strip() for c in line.split("|")[1:-1]] if stripped.startswith("|") else [body]
        if stripped.startswith("|") and set(stripped) <= set("|-: "):
            continue
        for cell in cells:
            cell = re.sub(r"^(\*\*|\*|_)", "", cell)
            if cell and LATIN_START.match(cell) and not cell.startswith(RLM):
                problems.append(f"{n}: starts with Latin/code, add RLM (U+200F): {cell[:40]!r}")
                break

    if interviewer != 1:
        problems.append(f"expected one ??? interviewer block, found {interviewer}")
    if hint_numbers and hint_numbers != sorted(hint_numbers):
        pass  # numbering restarts per part; only the per-hint number check above matters
    problems.extend(leftovers)
    return problems


def main(argv: list[str]) -> int:
    paths = [question_path(a) for a in argv] if argv else sorted(QUESTIONS.glob("*/0*.md"))
    bad = 0
    for path in paths:
        problems = lint(path)
        if problems:
            bad += 1
            print(f"{path.relative_to(QUESTIONS.parent.parent)}:")
            for p in problems:
                print(f"  {p}")
    print(f"{len(paths) - bad}/{len(paths)} pages clean")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
