"""Question 0037: the page's Python code (sync_mtbf, as published) against the generator,
the exp(T / tau) ratio per flop, the edge case, and the explorer's JavaScript."""

import math
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0037  # noqa: E402

sync_mtbf = load_python(37)["sync_mtbf"]
ARGS = (50e6, 100e-12, 50e-12, 0.3e-9)


def test_against_generator():
    for f in (200e6, 500e6, 1e9, 2e9):
        for n in (1, 2, 3, 4):
            assert sync_mtbf(f, *ARGS, n) == q0037.mtbf(f, *ARGS, n)


def test_ratio_and_edge():
    for f in (500e6, 1e9):
        for n in (1, 2):
            assert math.isclose(sync_mtbf(f, *ARGS, n + 1) / sync_mtbf(f, *ARGS, n), math.exp(1 / f / 100e-12), rel_tol=1e-9)
    assert sync_mtbf(1e9, 50e6, 100e-12, 50e-12, 1.2e-9, 1) == 0.0
    assert sync_mtbf(500e6, 50e6, 50e-12, 50e-12, 0.3e-9, 2) > sync_mtbf(500e6, 50e6, 100e-12, 50e-12, 0.3e-9, 2)


def test_explorer_matches_python():
    from page_tests import explorer_require, node_json

    cases = [(500, 50, 100, 50, 0.3, 1), (500, 50, 100, 50, 0.3, 2), (1000, 50, 100, 50, 0.3, 3), (1000, 500, 20, 100, 0.5, 2), (2000, 10, 30, 50, 0.6, 1)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({[list(c) for c in cases]}.map((c) => m.mtbfSeconds(...c))));
    """)
    for (fclk, fdata, tau, t0, ov, n), js in zip(cases, got):
        py = sync_mtbf(fclk * 1e6, fdata * 1e6, tau * 1e-12, t0 * 1e-12, ov * 1e-9, n)
        assert math.isclose(js, py, rel_tol=1e-9), (fclk, fdata, tau, t0, ov, n)


def test_explorer_monte_carlo():
    """The Monte Carlo box of part a (J295): its two factors multiply back to the page's
    sync_mtbf (19 seconds for one flop on the page's numbers); in a large seeded draw
    the share of edges inside the T0 window is T0 / T_clk, the settling times have mean
    tau, and the share still unsettled after a time t is exp(-t / tau)."""
    from page_tests import explorer_require, node_json

    cases = [(100, 50, 1), (100, 50, 2), (100, 50, 3), (300, 300, 1), (20, 10, 2)]
    got = node_json(f"""
      const m = {explorer_require()};
      const f = {[list(c) for c in cases]}.map(([tau, t0, n]) => m.metaFactors(500, 50, tau, t0, 0.3, n));
      const d = m.metaDraw(200000, 2000, 300, 100, m.mulberry32(37));
      console.log(JSON.stringify({{ f, n: d.phases.length, k: d.settle.length, maxPhase: d.phases.reduce((a, b) => Math.max(a, Math.abs(b)), 0),
        inside: d.meta.every((i) => Math.abs(d.phases[i]) < 150), mean: d.settle.reduce((a, b) => a + b, 0) / d.settle.length,
        tail: d.settle.filter((t) => t >= 200).length / d.settle.length }}));""")
    for (tau, t0, n), r in zip(cases, got["f"]):
        py = sync_mtbf(500e6, 50e6, tau * 1e-12, t0 * 1e-12, 0.3e-9, n)
        assert math.isclose(r["mtbf"], py, rel_tol=1e-9)
        assert math.isclose(r["pEnter"], t0 * 1e-12 * 500e6, rel_tol=1e-12) and r["tRes"] == n * 2000 - 300
        assert math.isclose(r["pStay"], math.exp(-r["tRes"] / tau), rel_tol=1e-12)
    assert round(got["f"][0]["mtbf"]) == 19
    assert got["n"] == 200000 and got["maxPhase"] <= 1000 and got["inside"]
    assert abs(got["k"] / got["n"] - 0.15) < 0.005
    assert abs(got["mean"] - 100) < 2.5 and abs(got["tail"] - math.exp(-2)) < 0.01
