import re
import subprocess
import sys

from extract_code import ROOT, load_python, question_path

ns = load_python(16)
sim, formula, bits = ns["josephus_sim"], ns["josephus_formula"], ns["josephus_bits"]
sim_k, rec_k = ns["josephus_sim_k"], ns["josephus_k"]


def reference(n, k):
    """Plain list simulation, written independently of the page."""
    people, i = list(range(1, n + 1)), 0
    while len(people) > 1:
        i = (i + k - 1) % len(people)
        people.pop(i)
    return people[0]


def test_page_examples():
    assert sim(5) == 3 and sim(10) == 5 and sim(41) == 19
    assert formula(41) == bits(41) == 19
    assert rec_k(41, 3) == sim_k(41, 3) == 31
    assert rec_k(7, 3) == 4


def test_k2_all_solutions_agree():
    for n in range(1, 2049):
        expected = reference(n, 2)
        assert sim(n) == formula(n) == bits(n) == sim_k(n, 2) == rec_k(n, 2) == expected, n
    # powers of two: the survivor is 1
    assert all(formula(1 << m) == 1 for m in range(40))


def test_any_k():
    for n in range(1, 120):
        for k in range(1, 12):
            assert sim_k(n, k) == rec_k(n, k) == reference(n, k), (n, k)


def test_bits_is_a_rotation():
    for n in range(1, 5000):
        b = f"{n:b}"
        assert bits(n) == int(b[1:] + b[0], 2), n


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
