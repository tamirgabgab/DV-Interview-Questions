import re
import subprocess
import sys

from extract_code import ROOT, load_python, question_path

ns = load_python(18)
solve = ns["solve"]


def replay(A, B, plan):
    """Replay a plan from rest; return the event times. Fails on an inconsistent plan."""
    t = a = b = 0
    events = [0]
    for when in sorted(plan):
        assert when == t, f"action at {when} but the next event is at {t}"
        if "A" in plan[when]:
            a = A - a
        if "B" in plan[when]:
            b = B - b
        running = [s for s in (a, b) if s > 0]
        assert running, "nothing is running"
        wait = min(running)
        t, a, b = t + wait, max(a - wait, 0), max(b - wait, 0)
        events.append(t)
    return events


def measurable(A, B, D):
    """Independent oracle: exhaustive search over every flip sequence (no visited set)."""
    def rec(t, a, b):
        if t == D:
            return True
        for fa in (0, 1):
            for fb in (0, 1):
                a2, b2 = (A - a if fa else a), (B - b if fb else b)
                if a2 == 0 and b2 == 0:
                    continue
                w = min(s for s in (a2, b2) if s > 0)
                if t + w <= D and rec(t + w, max(a2 - w, 0), max(b2 - w, 0)):
                    return True
        return False
    return rec(0, 0, 0)


def test_page_example():
    assert solve(7, 11, 15) == {0: "AB", 7: "A", 11: "A"}
    assert solve(4, 7, 9) == {0: "AB", 4: "A", 7: "B", 8: "B"}
    assert solve(7, 11, 0) == {}


def test_impossible_from_zero():
    for D in (1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 16):
        assert solve(7, 11, D) is None, D
    assert solve(4, 6, 3) is None          # not a multiple of gcd(4, 6)


def test_plans_replay_to_d_and_match_oracle():
    for A in range(2, 9):
        for B in range(A + 1, 12):
            for D in range(1, 25):
                plan = solve(A, B, D)
                assert (plan is not None) == measurable(A, B, D), (A, B, D)
                if plan is not None:
                    assert replay(A, B, plan)[-1] == D, (A, B, D, plan)


def test_figures_up_to_date():
    # The step-through figure and the branching figure are the output of tools/figures/q0018.py
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0018.py")],
                         capture_output=True, text=True, check=True).stdout
    text = question_path(18).read_text(encoding="utf-8")
    for pattern in (r'<div class="stepper".*?</div></div>', r'<svg class="figure hourglass-fig".*?</svg>'):
        generated = re.findall(pattern, out)
        assert generated and re.findall(pattern, text) == generated, pattern
