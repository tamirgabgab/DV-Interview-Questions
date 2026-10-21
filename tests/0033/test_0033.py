"""Question 0033: the generator's numbers (the page example and the cases table) and the
generated blocks on the page."""

import sys

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0033  # noqa: E402


def test_example():
    assert q0033.depth(120, 100, 80) == 24
    assert q0033.fill(120, q0033.T_WRITE, q0033.T_READ)[0] == 25
    assert q0033.depth(120, 100, 80, 0.75) == 48
    assert q0033.fill(120, q0033.T_WRITE, q0033.T_READ, 4)[0] == 48


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(33)
