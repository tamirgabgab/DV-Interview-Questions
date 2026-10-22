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
