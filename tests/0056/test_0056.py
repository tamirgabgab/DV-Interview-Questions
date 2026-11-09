"""Question 0056: the page's win3_lsb, win3_msb and win_div against the window itself (kept
as a value and stepped by the definition) on every bit string up to 10 bits for every L up
to 6 and every start window, and on random digit strings in several bases; the generator's
minimized machines (the state counts on the page, the same both ways for m = 3 by bit
reversal and not for m = 7, exactly 2^L - floor(2^L / 6), above the proof's 2^(L-1) + 1);
the page's examples, its traps, the filling-window follow-up and the box tasks; the
explorer's JavaScript; and the page copies of the generated blocks."""

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
    # trap 2: the rule of 0055 parts from the window only when a 1 leaves (L = 3, bits 1, 0, 0, 0)
    r55 = []
    for b in [1, 0, 0, 0]:
        r55.append((2 * (r55[-1] if r55 else 0) + b) % 3)
    assert r55 == [1, 2, 1, 2] and q0056.windows([1, 0, 0, 0], 2, 3, False)[-1] == 0
    assert win3_lsb([1, 0, 0, 0], 3) == [False, False, False, True]
    for L in range(1, 6):
        for bits in itertools.product((0, 1), repeat=9):
            r, ones = 0, [i for i, b in enumerate(bits) if b]
            for i, (b, ok) in enumerate(zip(bits, win3_lsb(list(bits), L))):
                r = (2 * r + b) % 3
                if (r == 0) != ok:
                    assert i >= ones[0] + L          # never before the first 1 has left
                    break


def test_filling_window():
    """The follow-up: no reset to zeros. r and the counter start at 0, and until the counter
    reaches L the digit that leaves counts as 0; without that mask r stays wrong."""
    def run(w, bits, L, mask):
        r, cnt, c = 0, 0, pow(2, L, 3)
        for b in bits:
            out = 0 if mask and cnt < L else w >> (L - 1)
            w, r, cnt = (w << 1 | b) % 2 ** L, (2 * r + b - c * out) % 3, min(cnt + 1, L)
        return r
    rng = random.Random(4)
    wrong = {False: 0, True: 0}
    for _ in range(1000):
        w, bits = rng.randrange(16), [rng.randrange(2) for _ in range(12)]
        for mask in (False, True):
            wrong[mask] += run(w, bits, 4, mask) != int("".join(map(str, bits[-4:])), 2) % 3
    assert wrong[True] == 0 and wrong[False] > 500
    for L in range(1, 5):
        for w in range(2 ** L):
            for bits in itertools.product((0, 1), repeat=L + 3):
                assert run(w, bits, L, True) == int("".join(map(str, bits[-L:])), 2) % 3


def test_box_tasks():
    """The tasks of the page's box paragraph."""
    def lsb(ds, L, init=0, b=2):
        return q0056.windows(ds, b, L, False, init)

    def msb(ds, L, init=0, b=2):
        return q0056.windows(ds, b, L, True, init)
    # the remainder is not enough: 011 then 0, 0: r 0, 0, 1; the bit that leaves is 0, then 1
    assert [w % 3 for w in lsb([0, 0], 3, 0b011)] == [0, 0, 1]
    assert [q0056.leaving(w, 2, 3, False) for w in lsb([0, 0], 3, 0b011)[:2]] == [0, 1]
    # the two directions: 10011 ends 10011 = 19 at the LSB and 11001 = 25 at the MSB
    assert lsb([1, 0, 0, 1, 1], 5)[-1] == 19 and msb([1, 0, 0, 1, 1], 5)[-1] == 25
    assert 19 % 3 and 25 % 3 and 19 % 5 and 25 % 5 == 0
    # merged states: 0010 and 1010 (and 0101, 1101) have the same next windows, neither divides
    for a, b in ((0b0010, 0b1010), (0b0101, 0b1101)):
        assert [q0056.step(a, d, 2, 4, False) for d in (0, 1)] == [q0056.step(b, d, 2, 4, False) for d in (0, 1)]
        assert a % 3 and b % 3
    assert [q0056.text(q0056.step(0b0010, d, 2, 4, False), 2, 4) for d in (0, 1)] == ["0100", "0101"]
    assert q0056.fewest_states(3, 2, 4, False) == 16 - 2
    # m = 6: fine at the LSB, no 2^-1 mod 6 at the MSB
    assert win_div([1, 1, 0, 1, 1, 0], 6, 2, 3) == truth([1, 1, 0, 1, 1, 0], 6, 2, 3, False)
    try:
        win_div([1], 6, 2, 3, msb=True)
        raise AssertionError("2 has an inverse mod 6?")
    except ValueError:
        pass
    # decimal: 1234 and 5 give 2345 = 7 * 335, and r' = (10*2 + 5 - 1*4) mod 7 = 0, C = 4
    assert lsb([5], 4, 1234, 10)[-1] == 2345 == 7 * 335
    assert 1234 % 7 == 2 and pow(10, 4, 7) == 4 and (10 * 2 + 5 - 1 * 4) % 7 == 0


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
    assert all(c >= 2 ** (L - 1) + 1 for L, c in enumerate(counts, 1))                # the proof's bound
    assert all(c > 2 ** (L - 1) for L, c in enumerate(counts, 1))                     # so L flip-flops at least
    # the exact count, both ways
    for L in range(1, 13):
        assert q0056.fewest_states(3, 2, L, False) == q0056.fewest_states(3, 2, L, True) == 2 ** L - 2 ** L // 6
    # the proof: two windows that differ in the low L - 1 bits are told apart by j >= 1 bits
    # after, the last of them u = 0 or 1; the windows 0 and 2^(L-1) share the low bits but
    # not the output
    for L in range(1, 8):
        for w, v in itertools.combinations(range(2 ** L), 2):
            if (w ^ v) % 2 ** (L - 1) == 0:
                continue
            i = ((w ^ v) & -(w ^ v)).bit_length() - 1
            j = L - 1 - i
            assert j >= 1
            told = any((q0056.windows([0] * (j - 1) + [u], 2, L, False, w)[-1] % 3 == 0)
                       != (q0056.windows([0] * (j - 1) + [u], 2, L, False, v)[-1] % 3 == 0) for u in (0, 1))
            assert told, (L, w, v)
        assert 2 ** (L - 1) % 3
    # the merges: the windows a and a + 2^(L-1) have the same next windows, and floor(2^L / 6)
    # of these pairs have neither window divisible
    for L in range(1, 10):
        n = 2 ** L
        for a in range(n // 2):
            assert all(q0056.step(a, d, 2, L, False) == q0056.step(a + n // 2, d, 2, L, False) for d in (0, 1))
        assert sum(1 for a in range(n // 2) if a % 3 and (a + n // 2) % 3) == n // 6
    # the same count both ways for m = 3: reversing the bits maps one machine onto the other
    # and keeps divisibility by 3 (2 = -1 mod 3); not for m = 7
    def rev(w, L):
        return int(format(w, f"0{L}b")[::-1], 2)
    for L in range(1, 10):
        for w in range(2 ** L):
            assert (w % 3 == 0) == (rev(w, L) % 3 == 0)
            for d in (0, 1):
                assert rev(q0056.step(w, d, 2, L, False), L) == q0056.step(rev(w, L), d, 2, L, True)
    assert (q0056.fewest_states(7, 2, 7, False), q0056.fewest_states(7, 2, 7, True)) == (61, 63)


def test_explorer_matches_the_page_code():
    from page_tests import explorer_require, node_json

    rng = random.Random(57)
    cases = []
    for _ in range(80):
        base = rng.choice([2, 4, 8, 10, 16])
        m = rng.choice([x for x in range(3, 16, 2) if gcd(x, base) == 1])
        L = rng.randint(1, 8 if base == 2 else 4)
        cases.append([m, base, L, rng.randrange(base ** L), [rng.randrange(base) for _ in range(rng.randint(1, 16))]])
    # at the LSB the box takes any m, even one that shares a factor with the base
    lsb_cases = []
    for _ in range(40):
        base = rng.choice([2, 4, 8, 10, 16])
        m, L = rng.choice([2, 4, 5, 6, 8, 10, 12, 15]), rng.randint(1, 4)
        lsb_cases.append([m, base, L, rng.randrange(base ** L), [rng.randrange(base) for _ in range(rng.randint(1, 16))]])
    # the size of the smallest machine, shown over the ring
    few = [[m, b, L, msb] for m in (3, 5, 7) for b in (2, 4) for L in range(1, 7 if b == 2 else 4) for msb in (False, True)]
    few += [[6, 2, 5, False], [4, 10, 2, False], [7, 10, 3, True], [15, 8, 2, False]]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify([{json.dumps(cases)}.map(([mm, b, L, init, ds]) => [
        m.winRun(ds, mm, b, L, init, false), m.winRun(ds, mm, b, L, init, true)]),
        {json.dumps(lsb_cases)}.map(([mm, b, L, init, ds]) => m.winRun(ds, mm, b, L, init, false)),
        {json.dumps(few)}.map(([mm, b, L, msb]) => m.winFewest(mm, b, L, msb)),
        m.winFewest(3, 16, 4, false)]));""")
    got, lsb_got, few_got, too_many = got
    assert too_many is None                              # above 4096 windows the box gives no count
    assert few_got == [q0056.fewest_states(m, b, L, msb) for m, b, L, msb in few]
    for (m, base, L, init, digits), run in zip(lsb_cases, lsb_got):
        ws = q0056.windows(digits, base, L, False, init)
        assert [s["w"] for s in run] == ws and [s["r"] for s in run] == [w % m for w in ws]
        assert [s["r"] == 0 for s in run[1:]] == win_div(digits, m, base, L, False, init)
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
