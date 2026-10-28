"""The Python side of the run panel.

docs/javascripts/py-worker.js loads this file into Pyodide, and tests/tools/test_run_panel.py
runs it in CPython on every question's starting code, so the browser and the tests run a
panel the same way.

run(solution, code) runs the page's Python code as solution.py, makes it importable as the
module `solution` (the starting code says `from solution import *`) and leaves its names in
the namespace too, then runs the reader's code as your_code.py. It returns the output check
of W352: every print() whose line carries a comment is compared with that comment, the
expected value ("print(f(3))  # 7"); a print with a label before the value may give only the
value ("print("max:", f(3))  # 7"). A note after the value is allowed: two spaces and a
parenthesis ("# 8   (part a)") or a colon and words ("# (3, 1): no pyramids").
"""

import ast
import builtins
import io
import re
import sys
import tokenize
import types

ANNOTATION = re.compile(r"(\s{2,}\([^()]*\)|:\s+[^\W\d][^:]*)$")


def value_of(expected: str) -> str:
    """The expected value of a comment, without its note."""
    return ANNOTATION.sub("", expected.strip()).rstrip()


def is_label(head: str) -> bool:
    """One label before a value: it ends with ":" or "=" and a space ("long only: ",
    "f(2) = ", "N = 5: "), but is not a comparison ("5 != 7", "a <= 3") and holds no other
    label of its kind with its value ("a = 1, b = 3", "x: 1, y: 3")."""
    sep = head.rstrip()
    if sep == head or not sep.endswith((":", "=")):
        return False
    label = sep[:-1]
    return (not label.endswith(("!", "<", ">", "=", ":"))
            and not re.search(re.escape(sep[-1]) + r"\s", label))


def matches(expected: str, got: str) -> bool:
    """The whole printed line, or what follows its one label ("long only: (6, 2, 3)" matches
    the comment "(6, 2, 3)", see is_label)."""
    got = got.rstrip()
    for e in (expected.strip(), value_of(expected)):
        if not e:
            continue
        if got == e or got.endswith(e) and is_label(got[: -len(e)]):
            return True
    return False


def expected_values(code: str) -> list[tuple[int, int, int, str]]:
    """(first line, last line, comment line, comment) of every print() call with a comment
    on one of its lines (the last one wins); [] when the code does not parse."""
    comments: dict[int, str] = {}
    try:
        for tok in tokenize.generate_tokens(io.StringIO(code).readline):
            if tok.type == tokenize.COMMENT:
                comments[tok.start[0]] = tok.string[1:].strip()
        tree = ast.parse(code)
    except (SyntaxError, tokenize.TokenError):
        return []
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "print":
            lines = [n for n in range(node.lineno, node.end_lineno + 1) if n in comments]
            if lines and comments[lines[-1]]:
                found.append((node.lineno, node.end_lineno, lines[-1], comments[lines[-1]]))
    return sorted(found)


def checks(code: str, records: list[tuple[int, str]]) -> list[dict]:
    """One check per commented print() that ran exactly once (a print in a loop is skipped)."""
    out = []
    for first, last, line, expected in expected_values(code):
        got = [text for n, text in records if first <= n <= last]
        if len(got) == 1:
            out.append({"line": line, "ok": matches(expected, got[0]), "got": got[0].rstrip(),
                        "expected": value_of(expected)})
    return out


def run(solution: str, code: str) -> list[dict]:
    ns: dict = {}
    exec(compile(solution, "solution.py", "exec"), ns)
    module = types.ModuleType("solution")
    module.__dict__.update({k: v for k, v in ns.items() if k != "__builtins__"})
    module.__file__ = "solution.py"
    sys.modules["solution"] = module

    records: list[tuple[int, str]] = []
    original = builtins.print

    def recording_print(*args, sep=" ", end="\n", file=None, flush=False):
        if file is None or file is sys.stdout:
            caller = sys._getframe(1)
            if caller.f_code.co_filename == "your_code.py":
                records.append((caller.f_lineno, (" " if sep is None else sep).join(map(str, args))))
        original(*args, sep=sep, end=end, file=file, flush=flush)

    ns["print"] = recording_print
    try:
        exec(compile(code, "your_code.py", "exec"), ns)
    finally:
        sys.modules.pop("solution", None)
    return checks(code, records)
