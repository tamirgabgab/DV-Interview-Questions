"""Question 0036: the generator's numbers (the two periods, every polynomial's period, the
count of maximal polynomials) and the generated blocks on the page."""

import sys

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0036  # noqa: E402


def test_periods():
    assert q0036.period((4, 3)) == 15 and q0036.period((4, 2)) == 6 and q0036.period((4, 1)) == 15
    seq = q0036.sequence((4, 3))
    assert len(seq) == 15 and sorted(seq) == list(range(1, 16))
    assert len(q0036.sequence((4, 2))) == 6


def test_every_polynomial():
    table = dict(q0036.all_polys())
    assert table == {(4,): 4, (4, 3): 15, (4, 2): 6, (4, 1): 15, (4, 3, 2): 7, (4, 3, 1): 6, (4, 2, 1): 7, (4, 3, 2, 1): 5}
    assert sum(p == 15 for p in table.values()) == 2        # phi(15) / 4
    assert q0036.mask_of((4, 3)) == 0b0011 and q0036.mask_of((4, 2)) == 0b0101 and q0036.mask_of((4, 1)) == 0b1001


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(36)


def test_explorer_widths():
    """The width select of the box (3 to 8 bits): the explorer's table of every polynomial
    agrees with a plain Python LFSR on the period from 0…01, its count of primitive
    polynomials equals phi(2^n - 1) / n and the number of period-(2^n - 1) rows, and the
    4-bit table is the page's."""
    from math import gcd

    from page_tests import explorer_require, node_json

    def period(mask, width):
        seen, s = {}, 1
        while s not in seen:
            seen[s] = len(seen)
            fb = bin(s & mask).count("1") & 1
            s = (s >> 1) | (fb << (width - 1))
        return len(seen) - seen[s]

    def phi(n):
        return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)

    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify([3, 4, 5, 6, 7, 8].map((w) => [m.lfsrTable(w), m.lfsrPrimitiveCount(w)])));""")
    for width, (table, count) in zip(range(3, 9), got):
        n = (1 << width) - 1
        assert [r["mask"] for r in table] == [1 | (m << 1) for m in range(1 << (width - 1))]
        for r in table:
            assert r["period"] == period(r["mask"], width), (width, r)
        assert count == phi(n) // width == sum(r["period"] == n for r in table), width
    four = {r["poly"]: r["period"] for r in got[1][0]}
    assert four["x^4 + x^3 + 1"] == 15 and four["x^4 + x^2 + 1"] == 6 and four["x^4 + x + 1"] == 15 and four["x^4 + 1"] == 4
    assert got[5][1] == 16                                   # the 8-bit follow-up: 16 primitive polynomials


def test_explorer_strip():
    """The timing strip of the box (X145): for every width and a primitive and a
    non-primitive mask, the slots are the states from 0…01 up to the step reached (the
    first state again after a full period), s[0] is the low bit of each and fb the parity
    of the tapped bits, which is the bit the next state takes at the top."""
    import json

    from page_tests import explorer_require, node_json

    cases = [(3, 0b011, 20), (4, 0b0011, 15), (4, 0b0101, 9), (5, 0b00101, 31), (6, 0b000011, 70), (8, 0b00011101, 300)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([w, mask, k]) => m.lfsrStrip(mask, w, k))));""")
    for (width, mask, k), sp in zip(cases, got):
        s, states = 1, []
        while True:
            states.append(s)
            fb = bin(s & mask).count("1") & 1
            s = (s >> 1) | (fb << (width - 1))
            if s in states:
                break
        period = len(states) - states.index(s)
        assert sp["total"] == period
        want = (states + [s])[: min(k, period) + 1]
        assert sp["states"] == want and sp["out"] == [v & 1 for v in want]
        assert sp["fb"] == [bin(v & mask).count("1") & 1 for v in want]
        assert all(nxt >> (width - 1) == fb for nxt, fb in zip(want[1:], sp["fb"]))


def test_explorer_cycles():
    """The picture of the cycles in the box: every polynomial of 3 to 8 bits splits the
    non-zero states into disjoint cycles (a plain Python step from every state), the seed's
    cycle first and in the order of the step; the page's x^4 + x^2 + 1 gives 6 + 6 + 3 and
    a primitive polynomial one cycle of all."""
    from page_tests import explorer_require, node_json

    def step(s, mask, width):
        return (s >> 1) | ((bin(s & mask).count("1") & 1) << (width - 1))

    got = node_json(f"""
      const m = {explorer_require()};
      const out = {{}};
      for (let w = 3; w <= 8; w++) out[w] = m.lfsrTable(w).map((r) => [r.mask, m.lfsrCycles(r.mask, w)]);
      console.log(JSON.stringify(out));""")
    for width in range(3, 9):
        n = (1 << width) - 1
        for mask, cycles in got[str(width)]:
            assert sorted(v for c in cycles for v in c) == list(range(1, n + 1)), (width, mask)
            assert 1 in cycles[0]
            for c in cycles:
                assert [step(v, mask, width) for v in c] == c[1:] + c[:1], (width, mask, c)
    four = dict((mask, [len(c) for c in cycles]) for mask, cycles in got["4"])
    assert four[0b0101] == [6, 6, 3] and four[0b0011] == [15] and four[0b1001] == [15]


def test_section_b_algebra():
    """Section b's algebra over GF(2), a polynomial as a bit mask (bit k is x^k): step 3's
    x^5 mod x^4 + x^3 + 1; hint 2 and step 2, the order 3 of x mod x^2 + x + 1, 6 mod its
    square, and the lcm for two coprime factors (x + 1)(x^3 + x + 1); the proof, the output
    bits of x^4 + x^3 + 1 follow x^4 + x + 1, its reciprocal, with the same order; and the
    XNOR trap, all ones stuck exactly when the taps are even, as in every maximal mask."""
    from math import lcm

    def mul(a, b):
        out = 0
        while b:
            if b & 1:
                out ^= a
            a, b = a << 1, b >> 1
        return out

    def mod(a, m):
        while a and a.bit_length() >= m.bit_length():
            a ^= m << (a.bit_length() - m.bit_length())
        return a

    def order(m):
        k, v = 1, mod(0b10, m)
        while v != 1:
            k, v = k + 1, mod(v << 1, m)
        return k

    page, recip, q = 0b11001, 0b10011, 0b111                  # x^4 + x^3 + 1, x^4 + x + 1, x^2 + x + 1
    assert mod(1 << 5, page) == 0b1011                         # x^5 = x^3 + x + 1, not 1
    assert mod(1 << 3, page) != 1 and order(page) == order(recip) == 15
    assert mul(q, q) == 0b10101 and order(q) == 3 and order(mul(q, q)) == 6
    assert mul(0b11, 0b1011) == 0b11101 and order(0b11101) == lcm(order(0b11), order(0b1011)) == 7
    # the bits that leave (s[0]) under x^4 + x^3 + 1 (taps s[0], s[1]) obey a(t+4) = a(t+1) + a(t)
    s, out = 1, []
    for _ in range(40):
        out.append(s & 1)
        s = (s >> 1) | ((bin(s & 0b0011).count("1") & 1) << 3)
    assert all(out[t + 4] == out[t + 1] ^ out[t] for t in range(len(out) - 4))
    for width in range(3, 9):
        ones, n = (1 << width) - 1, (1 << width) - 1
        for mask in range(1, 1 << width, 2):
            xnor = (ones >> 1) | ((1 ^ (bin(ones & mask).count("1") & 1)) << (width - 1))
            assert (xnor == ones) == (bin(mask).count("1") % 2 == 0), (width, mask)
            seen, v = set(), 1
            while v not in seen:
                seen.add(v)
                v = (v >> 1) | ((bin(v & mask).count("1") & 1) << (width - 1))
            if len(seen) == n:
                assert bin(mask).count("1") % 2 == 0, (width, mask)
