import re
import subprocess
import sys
from collections import deque

from extract_code import ROOT, load_python, question_path

ns = load_python(19)
solve = ns["solve"]


def step(A, B, a, b, fa, fb):
    """Apply the flips, wait for the next hourglass; return (wait, a, b) or None."""
    a2, b2 = (A - a if fa else a), (B - b if fb else b)
    if a2 == 0 and b2 == 0:
        return None
    w = min(s for s in (a2, b2) if s > 0)
    return w, max(a2 - w, 0), max(b2 - w, 0)


def replay(A, B, plan):
    """Replay a plan from rest; return the event times. Fails on an inconsistent plan."""
    t = a = b = 0
    events = [0]
    for when in sorted(plan):
        assert when == t, f"action at {when} but the next event is at {t}"
        res = step(A, B, a, b, "A" in plan[when], "B" in plan[when])
        assert res is not None, "nothing is running"
        w, a, b = res
        t += w
        events.append(t)
    return events


def reachable(A, B, limit):
    """All (t, a, b) event states reachable from rest with t <= limit."""
    seen = {(0, 0, 0)}
    todo = deque(seen)
    while todo:
        t, a, b = todo.popleft()
        for fa in (0, 1):
            for fb in (0, 1):
                res = step(A, B, a, b, fa, fb)
                if res and t + res[0] <= limit and (t + res[0], res[1], res[2]) not in seen:
                    seen.add((t + res[0], res[1], res[2]))
                    todo.append((t + res[0], res[1], res[2]))
    return seen


def can_measure_from(A, B, a, b, D):
    """Independent oracle: can exactly D minutes pass from configuration (a, b) to an event?"""
    seen = {(0, a, b)}
    todo = deque(seen)
    while todo:
        t, a, b = todo.popleft()
        if t == D:
            return True
        for fa in (0, 1):
            for fb in (0, 1):
                res = step(A, B, a, b, fa, fb)
                if res and t + res[0] <= D and (t + res[0], res[1], res[2]) not in seen:
                    seen.add((t + res[0], res[1], res[2]))
                    todo.append((t + res[0], res[1], res[2]))
    return False


def test_page_examples():
    assert solve(7, 11, 1) == (21, {0: "AB", 7: "A", 11: "B", 14: "A", 21: ""})
    assert solve(7, 11, 4) == (7, {0: "AB", 7: ""})
    assert solve(7, 11, 15) == (0, {0: "AB", 7: "A", 11: "A"})
    assert solve(4, 6, 3) is None          # not a multiple of gcd(4, 6)


def test_earliest_end_matches_oracle():
    for A in range(2, 9):
        for B in range(A + 1, 10):
            for D in range(1, 11):
                result = solve(A, B, D)
                bound = 4 * (A + B) + D
                candidates = [t + D for t, a, b in reachable(A, B, bound)
                              if can_measure_from(A, B, a, b, D)]
                if result is None:
                    assert not candidates, (A, B, D)
                    continue
                start, plan = result
                events = replay(A, B, plan)
                assert start in events and events[-1] == start + D, (A, B, D, result)
                assert start + D == min(candidates), (A, B, D, result)


def test_figures_up_to_date():
    # The step-through figure on the page is the output of tools/figures/q0019.py
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0019.py")],
                         capture_output=True, text=True, check=True).stdout
    text = question_path(19).read_text(encoding="utf-8")
    pattern = r'<div class="stepper".*?</div></div>'
    generated = re.findall(pattern, out)
    assert generated and re.findall(pattern, text) == generated
