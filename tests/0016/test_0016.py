"""Question 0016 has no code on the page; these tests check the closed form against an
independent simulation and that the figures and tables are the generator's output."""

import re
import subprocess
import sys

from extract_code import ROOT, question_path

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0016  # noqa: E402


def reference(n, L=2):
    """Plain list simulation of "one stays, L - 1 leave", written independently of the
    generator: the index of the one who stays, then L - 1 pops right after it."""
    people, i = list(range(n)), 0
    while len(people) > 1:
        for _ in range(L - 1):
            if len(people) == 1:
                break
            j = (i + 1) % len(people)
            people.pop(j)
            if j < i:
                i -= 1
        i = (i + 1) % len(people)
    return people[0]


def closed_form(n):
    top = 1 << (n.bit_length() - 1)
    return 2 * (n - top)


def recurrence(n):
    f = 0
    for m in range(2, n + 1):
        f = (f + 2) % m
    return f


def test_page_examples():
    assert reference(5) == 2 and reference(20) == 8 and reference(41) == 18
    assert closed_form(20) == 8 and closed_form(41) == 18


def test_closed_form_against_simulation():
    for n in range(1, 4097):
        assert reference(n) == closed_form(n) == recurrence(n) == q0016.formula(n) == q0016.survivor(n), n
    assert all(closed_form(1 << m) == 0 for m in range(40))


def test_halving_and_odd_recurrences():
    for k in range(1, 600):
        assert closed_form(2 * k) == 2 * closed_form(k)
        assert closed_form(2 * k + 1) == 2 * closed_form(k) + 2


def test_binary_view():
    for n in range(1, 5000):
        b = f"{n:b}"
        assert closed_form(n) == int(b[1:] + "0", 2), n


def test_rounds_of_twenty():
    groups, win = q0016.rounds(20)
    assert win == 8
    assert [v for _, leave in groups[0] for v in leave] == list(range(1, 20, 2))
    assert [v for _, leave in groups[1] for v in leave] == [2, 6, 10, 14, 18]
    assert [v for _, leave in groups[2] for v in leave] == [4, 12, 0]
    assert [v for _, leave in groups[3] for v in leave] == [16]


def test_figures_up_to_date():
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0016.py")],
                         capture_output=True, text=True, check=True).stdout
    text = question_path(16).read_text(encoding="utf-8")
    for pattern in (r'<div class="stepper".*?</div></div>', r'<svg class="(?:figure|perf-chart)".*?</svg>',
                    r'<span class="viz-legend">.*?</span></span>'):
        generated = re.findall(pattern, out)
        assert generated and re.findall(pattern, text) == generated, pattern
    page_rows = [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
    for row in (l for l in out.splitlines() if l.startswith("|")):
        assert row.strip() in page_rows, row
