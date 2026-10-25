#!/usr/bin/env python3
r"""Lint the question pages for the site's writing conventions.

    python tools/lint_pages.py            # all pages
    python tools/lint_pages.py 12 14      # some pages

Checks, per page:
- RTL safety: outside code blocks, HTML and math, no paragraph, list item, heading or
  table cell starts with a Latin letter, inline code or inline math; such lines need the
  RLM mark (U+200F) first. Indented blocks (admonitions, list items) and the Markdown
  inside ``<div class="steps" markdown>`` are checked too; continuation lines of a
  paragraph are not, since only the first strong character sets the direction.
- Solution structure: every collapsed solution (``??? success``) starts with an
  ``!!! answer`` block; the solution block labels (h4 with ``.sol-*`` classes) use only the
  known names and appear in the fixed order; hints are numbered "רמז 1", "רמז 2", ...
- Cost chips: a solution with a complexity block (``.sol-cost``) has a chips line
  ``<!-- cost: זמן \( O(n) \) | זיכרון \( O(1) \) -->`` (rendered by the hook under the
  short answer), and every chip starts with a Hebrew label word.
- One ``??? interviewer`` block right after the question, and the end-of-page blocks use
  the ``trap`` / ``followup`` types (a top-level ``note`` / ``warning`` titled like an
  interviewer / trap / follow-up block is reported; other notes may keep their type).
- Code highlights: every line named in ``hl_lines=`` exists in the (dedented) block and is
  a code line, not a blank line, a comment alone or a bare ``end`` / ``endfunction``, so the
  highlights keep pointing at the code the explanation names after the block is edited.
Warnings (printed, exit status unchanged): an inline SVG colour written as a literal
(``fill="#..."``, ``stroke:#...``, ``fill="white"``) instead of a class whose colour is a CSS
variable, since such a figure does not follow the light / dark switch.
Exit status 1 when a problem (not a warning) is reported, so it can run in CI.
"""

from __future__ import annotations

import re
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_code import FENCE, QUESTIONS, question_path  # noqa: E402

LABELS = ["הרעיון", "השלבים", "הקוד", "למה זה נכון", "סיבוכיות"]
CLASSES = ["sol-idea", "sol-steps", "sol-code", "sol-proof", "sol-cost"]
LABEL_RE = re.compile(r"^\s*#### (.+?)\s*\{\s*\.(sol-\w+)\s*\}\s*$")
H4_RE = re.compile(r"^\s*#### ")
ADMON_RE = re.compile(r'^(\s*)(\?\?\?\+?|!!!)\s+(\w+)(?:\s+"([^"]*)")?')
COST_RE = re.compile(r"^<!--\s*cost:\s*(.+?)\s*-->$")
HEBREW_WORD = re.compile(r"^[\u05d0-\u05ea]")
RLM = "‏"
LITERAL_COLOUR = re.compile(r'(?:fill|stroke|color)\s*(?:=\s*"|:\s*)\s*(#[0-9a-fA-F]{3,8}|white|black|red|green|blue|gray|grey|orange)\b')
LATIN_START = re.compile(r"^[A-Za-z`\\]")
HL_LINES = re.compile(r'hl_lines="([^"]*)"')
CLOSERS = {"end", "endfunction", "endtask", "endclass", "endmodule", "begin", "else", "}", "{", "pass"}


def lint_highlights(text: str) -> list[str]:
    """Every ``hl_lines`` entry must name a code line of its (dedented) block."""
    problems = []
    for m in FENCE.finditer(text):
        header = text[m.start():text.find("\n", m.start())]
        h = HL_LINES.search(header)
        if not h:
            continue
        n = text.count("\n", 0, m.start()) + 1
        body = textwrap.dedent(m.group("body")).splitlines()
        wanted = []
        for part in h.group(1).split():
            a, _, b = part.partition("-")
            wanted.extend(range(int(a), int(b or a) + 1))
        for k in wanted:
            line = body[k - 1].strip() if 0 < k <= len(body) else None
            if line is None:
                problems.append(f"{n}: hl_lines names line {k}, the block has {len(body)} lines")
            elif not line or line.startswith(("//", "#")) or line in CLOSERS:
                problems.append(f"{n}: hl_lines names line {k}, which is not code: {line[:40]!r}")
    return problems


def topic_names() -> dict[str, str]:
    """The TOPICS table of hooks/questions.py (the Hebrew name of every topic), read
    without importing the hook."""
    import ast
    src = (Path(__file__).resolve().parents[1] / "hooks" / "questions.py").read_text(encoding="utf-8")
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "TOPICS" for t in node.targets):
            return ast.literal_eval(node.value)
    return {}


TOPICS = topic_names()
TAGS_RE = re.compile(r"^tags:\s*\[(.*?)\]", re.M)


def strip_front_matter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


def lint(path: Path, warnings: list[str] | None = None) -> list[str]:
    problems: list[str] = []
    warnings = warnings if warnings is not None else []
    text = path.read_text(encoding="utf-8")
    m = TAGS_RE.search(text[: text.find("\n---", 3)] if text.startswith("---") else "")
    for tag in (t.strip() for t in (m.group(1).split(",") if m else [])):
        if tag and tag not in TOPICS:
            warnings.append(f"front matter: the topic {tag!r} has no name in TOPICS (hooks/questions.py); it shows as written")
    lines = strip_front_matter(text).splitlines()

    in_code = False
    fence_indent = ""
    in_html = 0
    in_math = False
    solutions: list[dict] = []
    current: dict | None = None
    hint_numbers: list[int] = []
    interviewer = 0
    leftovers = []
    para_start = True            # the next text line starts a paragraph
    in_comment = False

    for n, raw in enumerate(lines, 1):
        line = raw.rstrip()
        stripped = line.strip()
        cost = COST_RE.match(stripped)
        if cost and not in_code:
            if current is not None:
                current["cost"] = n
            for chip in cost.group(1).split(" | "):
                if not HEBREW_WORD.match(chip.strip()):
                    problems.append(f"{n}: cost chip without a Hebrew label first: {chip.strip()[:30]!r}")

        # fenced code
        m = re.match(r"^(\s*)```", line)
        if m:
            if not in_code:
                in_code, fence_indent = True, m.group(1)
            elif m.group(1) == fence_indent:
                in_code = False
            para_start = True
            continue
        if in_code:
            continue
        # display math: a paragraph of its own, or Markdown eats the backslashes and the
        # formula shows as raw TeX between [ and ]
        if stripped.startswith("\\[") and not in_math:
            in_math = True
            before = lines[n - 2].strip() if n > 1 else ""
            if before and not re.match(r"^(!!!|\?\?\?\+?) ", before):
                problems.append(f"{n}: display math \\[ needs a blank line before it")
        if in_math:
            if stripped.endswith("\\]"):
                in_math = False
                if n < len(lines) and lines[n].strip():
                    problems.append(f"{n}: display math \\] needs a blank line after it")
            para_start = True
            continue
        # Markdown inside an HTML block (the steps timeline) is linted like the rest
        if re.match(r"<div\b[^>]*\bmarkdown\b[^>]*>$", stripped) or stripped == "</div>":
            para_start = True
            continue
        # html blocks (svg etc.)
        if stripped.startswith("<") or in_html:
            colours = sorted(set(LITERAL_COLOUR.findall(stripped)))
            if colours:
                warnings.append(f"{n}: literal SVG colour {', '.join(colours)}: use a class with a CSS variable")
        if stripped.startswith("<") and not stripped.startswith("</"):
            in_html += len(re.findall(r"<(?!/)(?!br)(?!!--)\w+(?![^>]*/>)", stripped))
        if in_html:
            in_html -= len(re.findall(r"</\w+>", stripped))
            in_html = max(in_html, 0)
            para_start = True
            continue
        if in_comment or stripped.startswith("<!--"):   # an HTML comment, maybe over several lines
            in_comment = "-->" not in stripped
            para_start = True
            continue
        if not stripped:
            para_start = True
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
            elif (typ in ("note", "warning") and kind.startswith("???") and len(indent) == 0
                  and any(w in title for w in ("מראיין", "המשך", "מלכודת", "נקודות חשובות"))):
                leftovers.append(f"{n}: top-level ??? {typ} {title!r}: use trap / followup / interviewer")
            if current is not None and typ != "success" and current["first"] is None:
                current["first"] = n
            para_start = True
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
            para_start = True
            continue

        # RTL: paragraph starts, list items, headings and table cells
        new_item = re.match(r"^\s*(?:[-*]|\d+\.|>|#{1,6})\s", line) is not None
        starts = para_start or new_item or stripped.startswith("|")
        para_start = stripped.startswith("|")
        if not starts:
            continue
        body = re.sub(r"^\s*(?:[-*]|\d+\.|>|#{1,6}|\|)\s*", "", line).lstrip()
        body = re.sub(r"^(\*\*|\*|_)", "", body)
        cells = [c.strip() for c in line.split("|")[1:-1]] if stripped.startswith("|") else [body]
        if stripped.startswith("|") and set(stripped) <= set("|-: "):
            continue
        for cell in cells:
            cell = re.sub(r"^(\*\*|\*|_)", "", cell)
            if cell and LATIN_START.match(cell) and not cell.startswith(RLM):
                problems.append(f"{n}: starts with Latin/code, add RLM (U+200F): {cell[:40]!r}")
                break

    for sol in solutions:
        if 4 in sol["labels"] and "cost" not in sol:
            problems.append(f"{sol['line']}: solution with a complexity block has no <!-- cost: ... --> chips line")
    if interviewer != 1:
        problems.append(f"expected one ??? interviewer block, found {interviewer}")
    if hint_numbers and hint_numbers != sorted(hint_numbers):
        pass  # numbering restarts per part; only the per-hint number check above matters
    problems.extend(leftovers)
    problems.extend(lint_highlights(path.read_text(encoding="utf-8")))
    return problems


def main(argv: list[str]) -> int:
    paths = [question_path(a) for a in argv] if argv else sorted(QUESTIONS.glob("*/0*.md"))
    bad = warned = 0
    for path in paths:
        warnings: list[str] = []
        problems = lint(path, warnings)
        if problems or warnings:
            print(f"{path.relative_to(QUESTIONS.parent.parent)}:")
            for p in problems:
                print(f"  {p}")
            for w in warnings:
                print(f"  warn {w}")
        bad += bool(problems)
        warned += bool(warnings)
    print(f"{len(paths) - bad}/{len(paths)} pages clean" + (f", {warned} with warnings" if warned else ""))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
