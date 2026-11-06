"""Question 0096: the Kelly criterion.

Every number the page states is recomputed here (the parts, the generated tables, the
traps and the follow-ups); the generator's formulas agree with the page's code; the
generated blocks are up to date; and the kelly box's models are compared under Node with
the formulas and with a Python copy of its seeded paths."""

import math
import re
import sys
from fractions import Fraction as Fr
from math import comb

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0096  # noqa: E402

ns = load_python(96)
PAGE = (ROOT / "docs" / "questions" / "junior" / "0096-kelly-criterion.md").read_text(encoding="utf-8")
P = [Fr(1, 2), Fr(3, 10), Fr(3, 20), Fr(1, 20)]
O = [Fr(11, 5), Fr(7, 2), Fr(5), Fr(10)]


def test_generator_matches_the_page_code():
    for p, a, b in q0096.PC_ROWS + [(Fr(k, 20), 1, 1) for k in range(1, 20)]:
        assert q0096.best(p, a, b) == ns["kelly_fraction"](p, a, b)
    for f in (0.05, 0.1, 0.2, 0.3, 0.5):
        assert math.isclose(q0096.growth(f, 0.6), ns["growth"](f, 0.6))
    assert math.isclose(q0096.F_ZERO, ns["zero_growth"](0.6, 0.2), abs_tol=1e-10)
    assert q0096.race(P, O) == ns["kelly_race"](P, O)
    # the figure's paths are the page's simulate() draws
    finals = sorted(path[-1] for path in q0096.wealth_paths(0.2, 0.6, 100, 12))
    assert finals == ns["simulate"](0.2, 0.6, 100, 12, seed=q0096.PATH_SEED)


def test_part_a_numbers():
    g = ns["growth"](0.2, 0.6)
    assert f"{g:.4f}" == "0.0201" and "0.0201" in PAGE
    # the median of Bin(100, 0.6) is 60, and the wealth at 60 wins is 100 e^(100 g)
    cdf, k = 0.0, 0
    while True:
        cdf += comb(100, k) * 0.6 ** k * 0.4 ** (100 - k)
        if cdf >= 0.5:
            break
        k += 1
    assert k == 60 and cdf - comb(100, 60) * 0.6 ** 60 * 0.4 ** 40 < 0.5
    med = 100 * 1.2 ** 60 * 0.8 ** 40
    assert math.isclose(med, 100 * math.exp(100 * g)) and round(med) == 749 and "749" in PAGE
    assert f"{0.6 ** 100:.1e}" == "6.5e-23" and "6.5 \\cdot 10^{-23}" in PAGE
    assert f"{100 * 1.2 ** 100:.1e}" == "8.3e+09" and "8.3 \\cdot 10^9" in PAGE
    root = ns["zero_growth"](0.6, 0.2)
    assert f"{root:.3f}" == "0.389" and "0.389" in PAGE
    # near the peak: g ~ 0.2 f - f^2 / 2, peak 0.02 at 0.2, zero at 0.4
    assert math.isclose(0.2 ** 2 / 2, 0.02)
    # half Kelly keeps about three quarters of the growth: 0.0150 against 0.0201
    half = ns["growth"](0.1, 0.6)
    assert f"{half:.4f}" == "0.0150" and 0.74 < half / g < 0.76
    # the expectation of the factor, 1 + 0.2 f
    for f in (0.1, 0.5, 1.0):
        assert math.isclose(0.6 * (1 + f) + 0.4 * (1 - f), 1 + 0.2 * f)


def test_part_b_numbers():
    f = ns["kelly_fraction"](Fr(11, 20))
    g = ns["best_growth"](Fr(11, 20))
    assert f == Fr(1, 10) and f"{g:.4f}" == "0.0050" and round(math.log(2) / g) == 138
    # ln 2 - H(0.6) = 0.6931 - 0.6730 = 0.0201
    H = -(0.6 * math.log(0.6) + 0.4 * math.log(0.4))
    assert f"{math.log(2):.4f}" == "0.6931" and f"{H:.4f}" == "0.6730" and f"{math.log(2) - H:.4f}" == "0.0201"
    # p = 0.51 doubles after about 3,466 rounds
    g51 = ns["best_growth"](Fr(51, 100))
    assert f"{math.log(2) / g51:,.0f}" == "3,466" and "3,466" in PAGE
    # near 1/2 the growth is about (p - q)^2 / 2
    for k in (51, 52, 55):
        p = Fr(k, 100)
        assert abs(ns["best_growth"](p) / (float(2 * p - 1) ** 2 / 2) - 1) < 0.02


def test_part_c_numbers():
    assert ns["kelly_fraction"](Fr(2, 5), 3, 1) == Fr(1, 5)
    assert f"{ns['best_growth'](Fr(2, 5), 3, 1):.4f}" == "0.0541" and "0.0541" in PAGE
    assert Fr(2, 5) * 3 - Fr(3, 5) == Fr(3, 5)                 # the edge 0.6
    assert ns["kelly_fraction"](Fr(3, 5), 1, Fr(1, 4)) == 2    # more than the wealth
    # without borrowing, g rises on all of [0, 1] in that case
    gs = [q0096.growth(i / 100, 0.6, 1, 0.25) for i in range(101)]
    assert all(x < y for x, y in zip(gs, gs[1:]))
    assert ns["kelly_fraction"](Fr(3, 10), 2, 1) == 0          # no edge: 0.6 < 0.7


def test_part_d_numbers():
    cash, bets = ns["kelly_race"](P, O)
    assert (cash, bets[0], bets[1]) == (Fr(77, 100), Fr(15, 100), Fr(8, 100))
    # the steps of the example: R = 11/12, then 77/100
    assert Fr(1, 2) / (1 - Fr(5, 11)) == Fr(11, 12)
    assert Fr(1, 5) / (1 - Fr(5, 11) - Fr(2, 7)) == Fr(77, 100)
    assert [p * o for p, o in zip(P, O)] == [Fr(11, 10), Fr(21, 20), Fr(3, 4), Fr(1, 2)]
    g_kelly = ns["race_growth"](cash, bets, P, O)
    g_all = ns["race_growth"](0, P, P, O)
    assert f"{g_kelly:.4f}" == "0.0100" and f"{g_all:.4f}" == "-0.0155"
    assert "0.0155" in PAGE and "0.0100" in PAGE
    assert f"{float(sum(1 / o for o in O)):.2f}" == "1.04"
    # at the optimum c + o_i b_i = p_i o_i for the horses bet on
    for i in (0, 1):
        assert cash + O[i] * bets[i] == P[i] * O[i]


def test_traps_and_follow_ups():
    assert math.isclose(100 * 1.2 * 0.8, 96)
    assert f"{ns['growth'](0.4, 0.6):.4f}" == "-0.0024" and "-0.0024" in PAGE
    cash6, bets6 = ns["kelly_race"](P, [Fr(11, 5), Fr(7, 2), Fr(6), Fr(10)])
    assert cash6 == Fr(231, 430) and f"{float(cash6):.3f}" == "0.537" and "231/430" in PAGE
    assert f"{float(bets6[2]) * 100:.1f}" == "6.0" and P[2] * 6 == Fr(9, 10)
    # an estimated 0.6 against a true 0.55
    wrong = ns["growth"](0.2, 0.55)
    assert f"{wrong:.5f}" == "-0.00014" and "-0.00014" in PAGE
    assert f"{math.log(2) / ns['growth'](0.2, 0.6):.1f}" == "34.4" and "34.4" in PAGE


def test_page_skeleton():
    assert PAGE.count('data-kind="kelly"') == 2
    boxes = [dict(re.findall(r'data-([a-z]+)="([^"]*)"', m.group(1)))
             for m in re.finditer(r'<div class="explorer" data-kind="kelly" ([^>]*)>', PAGE)]
    assert boxes == [{"p": "0.6", "a": "1", "b": "1", "f": "0.2"}, {"p": "0.4", "a": "3", "b": "1", "f": "0.2"}]


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(96)


def mulberry32(seed):
    a = seed & 0xFFFFFFFF

    def rnd():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = ((a ^ (a >> 15)) * (1 | a)) & 0xFFFFFFFF
        t = (t + (((t ^ (t >> 7)) * (61 | t)) & 0xFFFFFFFF)) & 0xFFFFFFFF ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return rnd


def py_paths(seed, f, p, a, b, rounds=100, n=30):
    rnd, out = mulberry32(seed), []
    for _ in range(n):
        w, path = 100.0, [100.0]
        for _ in range(rounds):
            w *= 1 + a * f if rnd() < p else max(0.0, 1 - b * f)
            path.append(w)
        out.append(path)
    return out


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    cases = [(0.6, 1, 1), (0.4, 3, 1), (0.5, 1, 0.5), (0.3, 2, 1), (0.6, 1, 0.25), (0.95, 0.2, 0.1), (0.05, 5, 1)]
    fs = [0, 0.1, 0.2, 0.5, 0.99, 1]
    runs = [(96, 0.2, 0.6, 1, 1), (7, 0.5, 0.4, 3, 1), (3, 1, 0.6, 1, 1), (12, 0.3, 0.55, 1.5, 0.5)]
    got = node_json(f"const m = {explorer_require()};"
                    f"const cases = {[list(c) for c in cases]}; const fs = {fs};"
                    f"const runs = {[list(r) for r in runs]};"
                    "const fin = (v) => (Number.isFinite(v) ? v : null);"
                    "console.log(JSON.stringify({"
                    "best: cases.map(([p, a, b]) => m.kyBest(p, a, b)),"
                    "growth: cases.map(([p, a, b]) => fs.map((f) => fin(m.kyGrowth(f, p, a, b)))),"
                    "paths: runs.map(([s, f, p, a, b]) => m.kyPaths(s, f, p, a, b, 100, 30)),"
                    "med: runs.map(([s, f, p, a, b]) => m.kyMedian(m.kyPaths(s, f, p, a, b, 100, 30))),"
                    "}));")
    for (p, a, b), best, gs in zip(cases, got["best"], got["growth"]):
        assert math.isclose(best, float(q0096.best(Fr(p), Fr(a), Fr(b))), abs_tol=1e-12)
        for f, g in zip(fs, gs):
            want = q0096.growth(f, p, a, b)
            assert (g is None and want == -math.inf) or math.isclose(g, want, rel_tol=1e-9, abs_tol=1e-12)
    for (seed, f, p, a, b), paths, med in zip(runs, got["paths"], got["med"]):
        ref = py_paths(seed, f, p, a, b)
        assert len(paths) == 30 and all(len(x) == 101 for x in paths)
        for x, y in zip(paths, ref):
            assert all(math.isclose(u, v, rel_tol=1e-12, abs_tol=1e-300) for u, v in zip(x, y))
        for t in (0, 50, 100):
            col = sorted(path[t] for path in ref)
            assert math.isclose(med[t], (col[14] + col[15]) / 2, rel_tol=1e-12, abs_tol=1e-300)
