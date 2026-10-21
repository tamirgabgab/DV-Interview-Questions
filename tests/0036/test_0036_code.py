"""Question 0036: the page's Python code (lfsr_next and lfsr_period, as published) against
the generator on every 4-bit mask and seed, the zero fixed point, and a maximal 8-bit
polynomial."""

import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0036  # noqa: E402

ns = load_python(36)
lfsr_next, lfsr_period = ns["lfsr_next"], ns["lfsr_period"]


def test_against_generator():
    for mask in range(1, 16):
        for seed in range(1, 16):
            taps = tuple(4 - i for i in range(4) if (mask >> i) & 1)
            assert lfsr_period(mask, 4, seed) == q0036.period(taps, seed)
            assert lfsr_next(seed, mask, 4) == q0036.step(seed, taps)


def test_page_numbers():
    assert lfsr_period(0b0011, 4) == 15 and lfsr_period(0b0101, 4) == 6 and lfsr_period(0b1001, 4) == 15
    assert lfsr_next(0, 0b0011, 4) == 0
    s, states = 1, []
    for _ in range(15):
        states.append(s)
        s = lfsr_next(s, 0b0011, 4)
    assert s == 1 and sorted(states) == list(range(1, 16))
    assert lfsr_period(0b00011101, 8) == 255          # x^8 + x^6 + x^5 + x^4 + 1
    assert lfsr_period(0b1011, 4, 5) == 2             # a short cycle of a reducible polynomial, seed 0101
