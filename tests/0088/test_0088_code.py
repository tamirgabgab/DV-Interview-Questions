"""Question 0088: the page's Python code (it runs as published) against the generator's
reference: ducci_step and steps_to_zero on every start of 4 numbers with small values,
always_zero for n up to 64, and ducci_orbit on every start of 3 to 7 numbers with small
values."""

import itertools
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0088  # noqa: E402

ns = load_python(88)
ducci_step, steps_to_zero = ns["ducci_step"], ns["steps_to_zero"]
parity_step, always_zero, ducci_orbit = ns["parity_step"], ns["always_zero"], ns["ducci_orbit"]


def test_step_and_steps_to_zero():
    for v in itertools.product(range(7), repeat=4):
        assert tuple(ducci_step(list(v))) == q0088.step(v)
        assert steps_to_zero(list(v)) == q0088.steps_to_zero(v), v
    assert steps_to_zero([2, 6, 11, 4]) == 6
    assert steps_to_zero([0, 1705, 4841, 10609]) == 25


def test_always_zero():
    for n in range(1, 65):
        assert always_zero(n) == q0088.power_of_two(n), n
    for n in range(2, 12):
        for b in range(1 << n):
            assert parity_step(b, n) == q0088.parity_step(b, n)


def test_orbit():
    for n in range(3, 8):
        vals = range(4) if n <= 5 else range(3)
        for v in itertools.product(vals, repeat=n):
            assert ducci_orbit(v) == q0088.orbit(v)[:2], v
    assert ducci_orbit((1, 2, 3)) == (2, 3)
    assert ducci_orbit((1, 2, 3, 4, 5)) == (2, 15)
