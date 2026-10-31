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


def test_traps_and_follow_ups():
    """The conservative per-stage model N (T - t_su - t_cq): 3.4 ns, about 4.7e8 s (15
    years) for two flops and 3.6e8 years for three, e^3 less per stage after the first; a
    clock-like 50 MHz data signal makes 100 million transitions, half the MTBF (149 years);
    the log-scale gap per flop at 500 MHz, 20 / ln 10 = 8.7 decades."""
    import math

    den = q0037.T0 * q0037.F_CLK * q0037.F_DATA
    assert math.isclose(den, 1.25e6)
    per_stage = lambda n: math.exp(n * (1 / q0037.F_CLK - q0037.OVERHEAD) / q0037.TAU) / den
    assert abs(2 * (1 / q0037.F_CLK - q0037.OVERHEAD) - 3.4e-9) < 1e-15
    assert abs(per_stage(2) / 4.7e8 - 1) < 0.01 and round(per_stage(2) / q0037.YEAR) == 15
    assert abs(per_stage(3) / q0037.YEAR / 3.6e8 - 1) < 0.01
    for n in (2, 3):
        model = q0037.mtbf(q0037.F_CLK, q0037.F_DATA, q0037.TAU, q0037.T0, q0037.OVERHEAD, n)
        assert math.isclose(model / per_stage(n), math.exp(3 * (n - 1)), rel_tol=1e-9)
    clocklike = q0037.mtbf(q0037.F_CLK, 2 * q0037.F_DATA, q0037.TAU, q0037.T0, q0037.OVERHEAD, 2)
    assert round(clocklike / q0037.YEAR) == 149
    assert round(20 / math.log(10), 1) == 8.7


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(37)
