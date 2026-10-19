"""Question 0018 has no code on the page; these tests check the closed forms for L = 3 and
for any L against an independent simulation, the zero-point characterization, and that
the figures and tables are the generator's output."""

import re
import subprocess
import sys

from extract_code import ROOT, question_path

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0016  # noqa: E402

sys.path.insert(0, str(ROOT / "tests" / "0016"))
from test_0016 import reference  # noqa: E402


def closed_form(n, L):
    """F_L(N) = L (N - M) / (L - 1) with M = r L^floor(log_L(N / r)), r = 1 + (N - 1) mod (L - 1)."""
    r = 1 + (n - 1) % (L - 1)
    M = r
    while M * L <= n:
        M *= L
    assert (n - M) % (L - 1) == 0
    return L * (n - M) // (L - 1)


def recurrence(n, L):
    f = {m: 0 for m in range(1, L)}
    for m in range(L, n + 1):
        f[m] = (f[m - L + 1] + L) % m
    return f[n]


def test_page_examples():
    assert reference(7, 3) == 6 and reference(30, 3) == 18 and reference(10, 3) == 6
    assert closed_form(30, 3) == 18 and closed_form(20, 3) == 3 and closed_form(21, 3) == 18
    assert closed_form(20, 4) == 16 == reference(20, 4)


def test_l3_against_simulation():
    for n in range(1, 3001):
        assert reference(n, 3) == closed_form(n, 3) == recurrence(n, 3) == q0016.formula(n, 3), n
    # the zero points: 3^m and 2 * 3^m, nothing else
    zeros = {n for n in range(1, 3001) if closed_form(n, 3) == 0}
    assert zeros == {b * 3 ** m for b in (1, 2) for m in range(8) if b * 3 ** m <= 3000}


def test_l3_parity_chains():
    for M in (1, 2, 3, 6, 9, 18, 27, 54):
        for j in range(M):
            assert closed_form(M + 2 * j, 3) == 3 * j
        assert closed_form(3 * M, 3) == 0


def test_any_l_against_simulation():
    for L in range(2, 8):
        for n in range(1, 1201):
            assert reference(n, L) == closed_form(n, L) == recurrence(n, L) == q0016.formula(n, L), (L, n)
        zeros = {n for n in range(1, 1201) if closed_form(n, L) == 0}
        assert zeros == {b * L ** m for b in range(1, L) for m in range(12) if b * L ** m <= 1200}, L


def test_l2_is_question_0016():
    for n in range(1, 2049):
        assert closed_form(n, 2) == 2 * (n - (1 << (n.bit_length() - 1)))


def test_rounds_of_thirty():
    groups, win = q0016.rounds(30, 3)
    assert win == 18
    assert [s for s, _ in groups[0]] == list(range(0, 30, 3))
    assert [v for _, leave in groups[1] for v in leave] == [3, 6, 12, 15, 21, 24, 0, 9]
    assert [v for _, leave in groups[2] for v in leave] == [27]


def test_figures_up_to_date():
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0018.py")],
                         capture_output=True, text=True, check=True).stdout
    text = question_path(18).read_text(encoding="utf-8")
    for pattern in (r'<div class="stepper".*?</div></div>', r'<svg class="(?:figure|perf-chart)".*?</svg>',
                    r'<span class="viz-legend">.*?</span></span>'):
        generated = re.findall(pattern, out)
        assert generated and re.findall(pattern, text) == generated, pattern
    page_rows = [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
    for row in (l for l in out.splitlines() if l.startswith("|")):
        assert row.strip() in page_rows, row
