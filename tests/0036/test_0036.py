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
    """The proof panel of the box: every polynomial of 3 to 8 bits splits the non-zero states
    into disjoint cycles (a plain Python step from every state), the seed's cycle first;
    the page's x^4 + x^2 + 1 gives 6 + 6 + 3 and a primitive polynomial one cycle of all."""
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


# --- GF(2) polynomials as integers (bit k is the coefficient of x^k), for the claims of part b

def _pmod(a, p):
    dp = p.bit_length() - 1
    while a and a.bit_length() - 1 >= dp:
        a ^= p << (a.bit_length() - 1 - dp)
    return a


def _pmul(a, b, p):
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
    return _pmod(r, p)


def _xpow(e, p):
    r = 1
    for _ in range(e):
        r = _pmul(r, 2, p)
    return r


def _order(p):
    k, v = 1, _pmod(2, p)
    while v != 1:
        v, k = _pmul(v, 2, p), k + 1
    return k


def _page_poly(mask, width):
    """The polynomial the page writes for a mask: x^width + 1, and x^k for the bit width - k."""
    return (1 << width) | 1 | sum(1 << k for k in range(1, width) if (mask >> (width - k)) & 1)


def _next(s, mask, width, xnor=0):
    return (s >> 1) | (((bin(s & mask).count("1") & 1) ^ xnor) << (width - 1))


def _cycle(s, mask, width, xnor=0):
    out = [s]
    while (s := _next(s, mask, width, xnor)) != out[0]:
        out.append(s)
    return out


def test_part_b_arithmetic():
    """The numbers of part b's steps (review round 7): x^5 modulo x^4 + x^3 + 1, the orders
    3 and 6 of the factor and its square, the rule for a polynomial that factors (the lcm
    alone is wrong for a repeated factor), and the period from 0…01 as the order of x modulo
    the page's polynomial and modulo its reciprocal."""
    p = 0b11001                                              # x^4 + x^3 + 1
    assert _xpow(3, p) == 0b1000 and _xpow(5, p) == 0b1011   # x^3, and x^5 = x^3 + x + 1
    assert _xpow(5, 0b10011) == 0b110                        # x^2 + x is x^5 modulo x^4 + x + 1
    assert _order(p) == 15 and _order(0b10011) == 15
    assert _order(0b111) == 3 and _order(0b10101) == 6       # x^2 + x + 1 and its square
    assert _pmul(0b111, 0b111, 1 << 9) == 0b10101
    assert _pmod(0b1001, 0b10101) != 0 and _pmod(0b1000001, 0b10101) == 0   # x^3 - 1, x^6 - 1
    assert sorted(len(_cycle(s, 0b0101, 4)) for s in (1, 3, 6)) == [3, 6, 6] and len(_cycle(6, 0b0101, 4)) == 3
    # distinct factors: the lcm; a repeated one doubles it (the table of the page)
    assert _pmul(0b11, 0b1011, 1 << 9) == _page_poly(0b0111, 4) and q0036.period((4, 3, 2)) == 7       # (x+1)(x^3+x+1)
    assert _pmul(_pmul(0b11, 0b11, 1 << 9), 0b111, 1 << 9) == _page_poly(0b1011, 4) and q0036.period((4, 3, 1)) == 6
    assert _order(0b11111) == 5 and _pmod((1 << 5) | 1, 0b11111) == 0       # irreducible, divides x^5 - 1
    for width in range(2, 9):
        for mask in range(1, 1 << width, 2):
            poly = _page_poly(mask, width)
            recip = int(format(poly, "b")[::-1], 2)
            assert len(_cycle(1, mask, width)) == _order(poly) == _order(recip), (width, mask)


def test_traps():
    """The XNOR trap: all ones is stuck exactly when the number of taps is even, which every
    maximal polynomial has. The reciprocal pair: the output of x^4 + x + 1 is the output of
    x^4 + x^3 + 1 in reverse time order; the states are not the reversed sequence."""
    for width in range(2, 9):
        ones = (1 << width) - 1
        for mask in range(1, 1 << width, 2):
            even = bin(mask).count("1") % 2 == 0
            assert (_next(ones, mask, width, 1) == ones) == even
            if len(_cycle(1, mask, width)) == ones:
                assert even
    a = [s & 1 for s in _cycle(1, 0b0011, 4)]
    b = [s & 1 for s in _cycle(1, 0b1001, 4)]
    assert "".join(map(str, a)) == "100010011010111" and "".join(map(str, b)) == "100011110101100"
    assert any(b[::-1] == a[k:] + a[:k] for k in range(15))
    sa, sb = _cycle(1, 0b0011, 4), _cycle(1, 0b1001, 4)[::-1]
    assert not any(sb == sa[k:] + sa[:k] for k in range(15))


def test_explorer_seed_and_xnor():
    """The seed and the XNOR switch of the box: its step with XNOR, its walk from every seed
    and its picture of every cycle (the stuck states included) against a plain Python
    step, for every mask of 3 to 6 bits; the cases the page names (0110 under
    x^4 + x^2 + 1 has a cycle of 3; with XNOR 1111 is stuck and 0000 moves)."""
    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      const out = {{}};
      for (let w = 3; w <= 6; w++) out[w] = m.lfsrTable(w).map((r) => [r.mask,
        [0, 1].map((x) => m.lfsrAllCycles(r.mask, w, x === 1)),
        [0, 1].map((x) => Array.from({{ length: 1 << w }}, (_, s) => m.lfsrWalk(r.mask, w, s, x === 1))),
        m.lfsrStrip(r.mask, w, 5, 3, true)]);
      console.log(JSON.stringify(out));""")
    for width in range(3, 7):
        for mask, cycles, walks, strip in got[str(width)]:
            for xnor in (0, 1):
                assert sorted(v for c in cycles[xnor] for v in c) == list(range(1 << width))
                assert [c[0] for c in cycles[xnor]] == sorted(c[0] for c in cycles[xnor])
                for c in cycles[xnor]:
                    assert c == _cycle(c[0], mask, width, xnor), (width, mask, xnor)
                for seed, walk in enumerate(walks[xnor]):
                    assert walk["states"] == _cycle(seed, mask, width, xnor) and walk["back"] == 0
                    assert walk["period"] == len(walk["states"])
            want = (_cycle(3, mask, width, 1) * 6)[:min(5, len(_cycle(3, mask, width, 1))) + 1]
            assert strip["states"] == want
            assert strip["fb"] == [_next(v, mask, width, 1) >> (width - 1) for v in want]
    four = {mask: (cycles, walks) for mask, cycles, walks, _ in got["4"]}
    assert four[0b0101][1][0][6]["period"] == 3 and four[0b0101][1][0][0]["period"] == 1
    assert [len(c) for c in four[0b0101][0][0]] == [1, 6, 6, 3]
    assert [len(c) for c in four[0b1111][0][0]] == [1, 5, 5, 5]
    assert four[0b0011][1][1][15]["period"] == 1 and four[0b0011][1][1][0]["period"] == 15
