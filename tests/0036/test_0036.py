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
