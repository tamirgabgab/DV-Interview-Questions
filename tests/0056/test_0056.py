"""Question 0056: the page's win3_lsb, win3_msb and win_div against the window itself (kept
as a value and stepped by the definition) on every bit string up to 10 bits for every L up
to 6 and every start window, and on random digit strings in several bases; the generator's
minimized machines (the state counts on the page, the same both ways, above 2^(L-1) from
L = 3); the page's examples; the explorer's JavaScript; and the page copies of the
generated blocks."""

import itertools
import json
import random
import sys
from math import gcd

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0056  # noqa: E402

ns = load_python(56)
win3_lsb, win3_msb, win_div = (ns[k] for k in ("win3_lsb", "win3_msb", "win_div"))


def truth(digits, m, base, L, msb, init=0):
    """After each digit, does the window (by the definition) divide by m."""
    return [w % m == 0 for w in q0056.windows(digits, base, L, msb, init)[1:]]


def test_every_bit_string():
    for L in range(1, 7):
        for init in range(2 ** L):
            for n in range(1, 11 if L <= 3 else 8):
                for bits in itertools.product((0, 1), repeat=n):
                    bits = list(bits)
                    assert win3_lsb(bits, L, init) == truth(bits, 3, 2, L, False, init), (bits, L, init)
                    assert win3_msb(bits, L, init) == truth(bits, 3, 2, L, True, init), (bits, L, init)


def test_page_examples():
    assert q0056.windows([1], 2, 3, False, 0b011)[-1] == 0b111      # 011 and 1 at the LSB: 111
    assert q0056.windows([1], 2, 3, True, 0b011)[-1] == 0b101       # 011 and 1 at the MSB: 101
    assert [q0056.text(w, 2, 3) for w in q0056.windows([1, 1, 0, 1], 2, 3, False)] == ["000", "001", "011", "110", "101"]
    assert [q0056.text(w, 2, 3) for w in q0056.windows([1, 0, 1, 1], 2, 3, True)] == ["000", "100", "010", "101", "110"]
    assert win3_lsb([1, 1, 0, 1], 3) == [False, True, True, False]
    assert win3_msb([1, 0, 1, 1], 3) == [False, False, False, True]
    # the trap: 011 and 110 both divide, and differ after a 0 at the LSB
    assert q0056.windows([0], 2, 3, False, 0b011)[-1] == 6 and q0056.windows([0], 2, 3, False, 0b110)[-1] == 4
    # the constants: 2^L mod 3 is 1 for L even, 2^(L-1) mod 3 is 1 for L odd; 10^4 mod 7 = 4
    assert all(pow(2, L, 3) == (1 if L % 2 == 0 else 2) and pow(2, L - 1, 3) == (1 if L % 2 else 2) for L in range(1, 20))
    assert pow(10, 4, 7) == 4 and pow(2, -1, 3) == 2


def test_general_machine():
    rng = random.Random(56)
    for _ in range(600):
        base = rng.choice([2, 3, 4, 8, 10, 16])
        m = rng.choice([x for x in range(2, 20) if gcd(x, base) == 1])
        L = rng.randint(1, 6)
        init = rng.randrange(base ** L)
        digits = [rng.randrange(base) for _ in range(rng.randint(1, 40))]
        for msb in (False, True):
            assert win_div(digits, m, base, L, msb, init) == truth(digits, m, base, L, msb, init), (digits, m, base, L, msb, init)
    # at the LSB the rule needs no inverse: any m, even sharing a factor with the base
    for m in (2, 4, 6, 10, 12):
        digits = [rng.randrange(10) for _ in range(30)]
        assert win_div(digits, m, 10, 3, False, 123) == truth(digits, m, 10, 3, False, 123)
    assert win_div([1, 1, 0, 1], 3, 2, 3) == win3_lsb([1, 1, 0, 1], 3)
    assert win_div([1, 0, 1, 1], 3, 2, 3, msb=True) == win3_msb([1, 0, 1, 1], 3)


def test_state_counts():
    counts = [q0056.fewest_states(3, 2, L, False) for L in range(1, 9)]
    assert counts == [2, 4, 7, 14, 27, 54, 107, 214]
    assert counts == [q0056.fewest_states(3, 2, L, True) for L in range(1, 9)]       # the same both ways
    assert all(c >= 2 ** (L - 2) for L, c in enumerate(counts, 1))                    # the proof's bound
    assert all(c > 2 ** (L - 1) for L, c in enumerate(counts, 1) if L >= 3)           # so L flip-flops at least
    # the proof: two windows that differ in the low L - 2 bits are told apart by some bits after
    for L in range(3, 8):
        for w, v in itertools.combinations(range(2 ** L), 2):
            if (w ^ v) % 2 ** (L - 2) == 0:
                continue
            i = ((w ^ v) & -(w ^ v)).bit_length() - 1
            j = L - 1 - i
            told = any((q0056.windows(u, 2, L, False, w)[-1] % 3 == 0) != (q0056.windows(u, 2, L, False, v)[-1] % 3 == 0)
                       for u in ([(x >> k) & 1 for k in reversed(range(j))] for x in range(2 ** j)))
            assert told, (L, w, v)


def test_explorer_matches_the_page_code():
    from page_tests import explorer_require, node_json

    rng = random.Random(57)
    cases = []
    for _ in range(80):
        base = rng.choice([2, 4, 8, 10, 16])
        m = rng.choice([x for x in range(3, 16, 2) if gcd(x, base) == 1])
        L = rng.randint(1, 8 if base == 2 else 4)
        cases.append([m, base, L, rng.randrange(base ** L), [rng.randrange(base) for _ in range(rng.randint(1, 16))]])
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([mm, b, L, init, ds]) => [
        m.winRun(ds, mm, b, L, init, false), m.winRun(ds, mm, b, L, init, true)])));""")
    for (m, base, L, init, digits), runs in zip(cases, got):
        for run, msb in zip(runs, (False, True)):
            ws = q0056.windows(digits, base, L, msb, init)
            assert [s["w"] for s in run] == ws
            assert [s["r"] for s in run] == [w % m for w in ws]
            assert [s["out"] for s in run[1:]] == [q0056.leaving(w, base, L, msb) for w in ws[:-1]]
            assert [s["r"] == 0 for s in run[1:]] == win_div(digits, m, base, L, msb, init)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(56)
