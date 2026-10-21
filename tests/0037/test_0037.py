"""Question 0037: the generator's numbers (the page example) and the generated blocks."""

import sys

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0037  # noqa: E402


def test_example():
    args = (q0037.F_DATA, q0037.TAU, q0037.T0, q0037.OVERHEAD)
    assert abs(q0037.mtbf(500e6, *args, 1) - 19.3) < 0.1
    assert abs(q0037.mtbf(500e6, *args, 2) / q0037.YEAR - 297) < 1
    assert abs(q0037.mtbf(500e6, *args, 3) / q0037.YEAR / 1.44e11 - 1) < 0.01
    assert abs(q0037.mtbf(1e9, *args, 1) / 0.439e-3 - 1) < 0.01
    assert abs(q0037.mtbf(1e9, *args, 2) - 9.66) < 0.05
    assert abs(q0037.mtbf(1e9, *args, 3) / 86400 - 2.46) < 0.01
    assert q0037.human(19.3) == "19.3 שניות" and q0037.human(297 * q0037.YEAR).startswith("297")


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(37)
