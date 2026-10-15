"""Extract the code blocks of a question page.

The question pages are the single source of truth: tests and the in-browser "run" panel
use the code exactly as it is published. Fenced blocks are found at any indentation
(inside tabs, admonitions or collapsible solutions) and returned dedented.
"""

from __future__ import annotations

import hashlib
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / "docs" / "questions"

FENCE = re.compile(r"^(?P<indent>[ \t]*)```(?P<lang>[\w+-]+)[^\n]*\n(?P<body>.*?)^(?P=indent)```[ \t]*$",
                   re.M | re.S)


def question_path(qid: str | int) -> Path:
    """Return the page of question `qid` (e.g. 6 or "0006")."""
    prefix = f"{int(qid):04d}-"
    matches = sorted(QUESTIONS.glob(f"*/{prefix}*.md"))
    if len(matches) != 1:
        raise FileNotFoundError(f"expected one page for question {prefix[:-1]}, found {matches}")
    return matches[0]


def blocks_from_text(text: str, lang: str) -> list[str]:
    """All fenced blocks of language `lang` in `text`, in page order, dedented."""
    out = []
    for m in FENCE.finditer(text):
        if m.group("lang") == lang:
            body = m.group("body")
            out.append(textwrap.dedent(body).rstrip("\n") + "\n")
    return out


def blocks(qid: str | int, lang: str) -> list[str]:
    return blocks_from_text(question_path(qid).read_text(encoding="utf-8"), lang)


def pick(qid: str | int, lang: str, marker: str) -> str:
    """The single block of `lang` that contains `marker`."""
    found = [b for b in blocks(qid, lang) if marker in b]
    if len(found) != 1:
        raise LookupError(f"question {qid}: expected one {lang} block containing {marker!r}, "
                          f"found {len(found)}")
    return found[0]


def fingerprint(code: str) -> str:
    """Short, whitespace-insensitive hash of a code block."""
    normalized = "\n".join(line.rstrip() for line in code.strip().splitlines())
    return hashlib.sha256(normalized.encode()).hexdigest()[:12]


def load_python(qid: str | int, skip: tuple[str, ...] = ()) -> dict:
    """Execute every Python block of the page (except blocks containing a `skip` marker)
    in one namespace and return it, so tests can call the published functions."""
    namespace: dict = {"__name__": f"question_{int(qid):04d}"}
    for code in blocks(qid, "python"):
        if any(s in code for s in skip):
            continue
        exec(compile(code, f"<question {int(qid):04d}>", "exec"), namespace)
    return namespace
