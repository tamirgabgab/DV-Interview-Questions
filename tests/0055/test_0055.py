"""Question 0055: the page's div3_msb, div3_lsb and div_fsm against the value itself on every
bit string up to 12 bits and on random digit strings in several bases; the generator's
minimized machines (the state counts on the page, the LSB machine of 3 being the MSB one
with 1 and 2 swapped); the page's numbers; the explorer's JavaScript; and the page copies
of the generated blocks."""

import itertools
import json
import random
import sys
from math import gcd

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0055  # noqa: E402

ns = load_python(55)
div3_msb, div3_lsb, div_fsm = (ns[k] for k in ("div3_msb", "div3_lsb", "div_fsm"))


def truth(digits, m, base, lsb):
    """After each digit, is the number read so far divisible by m (from its value)."""
    return [q0055.value(digits[:i + 1], base, lsb) % m == 0 for i in range(len(digits))]


def test_every_bit_string():
    for n in range(1, 13):
        for bits in itertools.product((0, 1), repeat=n):
            bits = list(bits)
            assert div3_msb(bits) == truth(bits, 3, 2, False), bits
            assert div3_lsb(bits) == truth(bits, 3, 2, True), bits


def test_page_examples():
    assert div3_msb([1, 1, 0]) == [False, True, True]           # 1, 3, 6
    assert div3_lsb([0, 1, 1]) == [True, False, True]           # 0, 2, 6
    assert int("1011", 2) == 11 and 11 % 3 == 2
    assert pow(10, -1, 7) == 5 and pow(2, -1, 3) == 2


def test_general_machine():
    rng = random.Random(55)
    for _ in range(400):
        base = rng.choice([2, 3, 4, 8, 10, 16])
        m = rng.choice([x for x in range(2, 20) if gcd(x, base) == 1])
        digits = [rng.randrange(base) for _ in range(rng.randint(1, 40))]
        for lsb in (False, True):
            assert div_fsm(digits, m, base, lsb) == truth(digits, m, base, lsb), (digits, m, base, lsb)
    assert div_fsm([1, 1, 0], 3) == div3_msb([1, 1, 0])
    assert div_fsm([0, 1, 1], 3, lsb=True) == div3_lsb([0, 1, 1])


def test_state_counts():
    # odd m: m states both ways; the naive LSB machine is m times the order of 2 mod m
    for m in range(3, 17, 2):
        order = next(k for k in range(1, m) if pow(2, k, m) == 1)
        assert q0055.naive_msb(m) == (m, m) and q0055.naive_lsb(m) == (m, m * order), m
    assert q0055.naive_lsb(3) == (3, 6) and q0055.naive_lsb(5) == (5, 20)
    # even m = 2^a m': m' + a from the MSB, m' + a + 1 from the LSB (the follow-up)
    for m in range(2, 17, 2):
        a = (m & -m).bit_length() - 1
        odd = m >> a
        assert q0055.naive_msb(m)[0] == odd + a and q0055.naive_lsb(m)[0] == odd + a + 1, m
    assert [q0055.naive_msb(m)[0] for m in (6, 12)] == [4, 5] and [q0055.naive_lsb(m)[0] for m in (6, 12)] == [5, 6]
    # base 10 and m = 5 (the trap): 2 from the MSB, 3 from the LSB
    assert q0055.naive_msb(5, 10)[0] == 2 and q0055.naive_lsb(5, 10)[0] == 3
    # the remainder itself from the LSB needs every naive state: they all differ in output or next
    for m in (3, 5, 7):
        order = next(k for k in range(1, m) if pow(2, k, m) == 1)
        states = {(r, pow(2, k, m)) for r in range(m) for k in range(order)}
        sig = {s: (s[0], (s[0] + s[1]) % m) for s in states}
        assert len(set(sig.values())) == len(states) == m * order


def test_lsb_three_is_msb_three_mirrored():
    msb, lsb = q0055.table(3, 2, False), q0055.table(3, 2, True)
    swap = [0, 2, 1]
    assert all(lsb[swap[s]][d] == swap[msb[s][d]] for s in range(3) for d in (0, 1))
    assert q0055.table(5, 2, False) != q0055.table(5, 2, True)
    # the multipliers of k bits a cycle: 4 = 1 mod 3 and 8 = 1 mod 7, a digit sum
    assert pow(4, 1, 3) == pow(4, -1, 3) == 1 and pow(8, 1, 7) == pow(8, -1, 7) == 1


def test_explorer_matches_the_page_code():
    from page_tests import explorer_require, node_json

    rng = random.Random(56)
    cases = []
    for _ in range(80):
        base = rng.choice([2, 4, 8, 10, 16])
        m = rng.choice([x for x in range(3, 16, 2) if gcd(x, base) == 1])
        cases.append([m, base, [rng.randrange(base) for _ in range(rng.randint(1, 20))]])
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([mm, b, ds]) => [
        m.divTable(mm, b, false), m.divTable(mm, b, true), m.divRun(ds, mm, b, false), m.divRun(ds, mm, b, true)])));""")
    for (m, base, digits), (tm, tl, rm, rl) in zip(cases, got):
        assert tm == q0055.table(m, base, False) and tl == q0055.table(m, base, True)
        for run, lsb in ((rm, False), (rl, True)):
            seq = list(reversed(digits)) if lsb else digits      # the box feeds the number's digits
            assert [s == 0 for s in run[1:]] == div_fsm(seq, m, base, lsb)
            assert run[0] == 0 and len(run) == len(digits) + 1


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(55)
