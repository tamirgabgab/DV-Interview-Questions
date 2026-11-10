"""Question 0027 has no code on the page; these tests split the cake with exact fractions,
check every number the page states, check the closed form and the single peak over a grid
of parameters (and the stated counterexample above d = 1/2), run the slider script under
Node against the same reference, and check that the figures and tables are the
generator's output."""

import json
import math
import shutil
import subprocess
import sys
from fractions import Fraction as Fr

import pytest

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import cake  # noqa: E402

A = cake.ARITH


def shares(a, d):
    """Independent split: walk the queue, cap the fraction at 1."""
    out, left, k = [], Fr(1), 0
    while True:
        p = min(a + k * d, Fr(1))
        out.append(p * left)
        if p == 1:
            return out
        left -= p * left
        k += 1


def closed_form(a, d):
    """The page's formula: k = max(1, ceil((T - a) / d) + 1), tie when a + (k - 1) d = T."""
    T = (math.sqrt(float(d * d + 4 * d)) - float(d)) / 2
    k = max(1, math.ceil((T - float(a)) / float(d) - 1e-12) + 1)
    p = a + (k - 1) * d
    tie = p * p + d * p - d == 0                 # exact: p is a root of p^2 + d p - d
    return k, tie


def test_part_a():
    s = shares(Fr(1, 100), Fr(1, 10))
    assert len(s) == 11
    assert max(s) == s[3] and cake.dec(s[3], 3) == "0.216" and cake.dec(s[3]) == "0.2158"
    assert all(s[i] < s[i + 1] for i in range(3)) and all(s[i] > s[i + 1] for i in range(3, 10))
    T = (math.sqrt(0.41) - 0.1) / 2
    assert f"{T:.4f}" == "0.2702"
    assert Fr(21, 100) < T <= Fr(31, 100)
    assert Fr(11, 100) < T and math.ceil((T - 0.01) / 0.1) + 1 == 4   # p_1, p_2, p_3 below T; part b's formula agrees
    assert cake.dec(Fr(99, 100) * Fr(89, 100) * Fr(79, 100)) == "0.6961"
    assert cake.dec(s[-1]) == "0.0003"
    # the ratio chart starts at 10.89
    assert s[1] / s[0] == Fr(1089, 100)


def test_examples_table():
    assert closed_form(Fr(1, 10), Fr(1, 10)) == (3, False)
    assert closed_form(Fr(1, 100), Fr(1, 100)) == (10, False)
    assert closed_form(Fr(1, 12), Fr(1, 12)) == (3, True)
    s = shares(Fr(1, 12), Fr(1, 12))
    assert s[2] == s[3] == max(s) and cake.dec(s[2], 3) == "0.191"
    # a = d: k(k + 1) >= 1/d, and the closed form with the square root
    for n in range(2, 400):
        d = Fr(1, n)
        k = next(k for k in range(1, n + 2) if k * (k + 1) >= n)
        assert closed_form(d, d)[0] == k
        assert math.ceil((math.sqrt(1 + 4 * n) - 1) / 2 - 1e-12) == k
    assert closed_form(Fr(1, 10000), Fr(1, 10000))[0] == 100


def test_closed_form_and_single_peak():
    for da in range(1, 61):
        for dd in range(1, 51):
            a, d = Fr(da, 100), Fr(dd, 100)
            s = shares(a, d)
            top = max(s)
            winners = [i + 1 for i, v in enumerate(s) if v == top]
            k, tie = closed_form(a, d)
            assert winners == ([k, k + 1] if tie else [k]), (a, d)
            peak = winners[0]
            assert all(s[i] < s[i + 1] for i in range(peak - 1))
            assert all(s[i] >= s[i + 1] for i in range(peak - 1, len(s) - 1))
            assert cake.formula(A, a, d) == k
            assert len(s) == math.ceil((1 - a) / d) + 1


def test_rounding_trap():
    """The trap "rounding the threshold too early": a = 0.27, d = 0.1, T = 0.27016..."""
    a, d = Fr(27, 100), Fr(1, 10)
    T = cake.threshold(A, d)
    assert f"{T:.5f}" == "0.27016" and a < T
    assert max(1, math.ceil((0.27 - 0.27) / 0.1) + 1) == 1         # T rounded to 0.27: person 1
    assert a * a + d * a - d == Fr(-1, 10000)                      # the exact sign: the next gets more
    s = shares(a, d)
    assert s[0] == Fr(27, 100) and s[1] == Fr(2701, 10000) and max(s) == s[1]
    assert closed_form(a, d) == (2, False)


def test_follow_ups():
    # d > 1/2: the formula says person 2, person 1 gets more
    s = shares(Fr(55, 100), Fr(8, 10))
    assert s == [Fr(55, 100), Fr(45, 100)] and closed_form(Fr(55, 100), Fr(8, 10))[0] == 2
    # the threshold: below 1, about sqrt(d) for a small d
    for d in (Fr(1, 10 ** 6), Fr(1, 10), Fr(1, 2), Fr(3)):
        T = cake.threshold(A, d)
        assert 0 < T < 1
    assert abs(cake.threshold(A, Fr(1, 10 ** 6)) / 1e-3 - 1) < 1e-3


def exact_peak(a, d):
    """The first person on or past the threshold, by the exact sign of p^2 + d p - d, and whether he is on it."""
    k = 1
    while True:
        p = a + (k - 1) * d
        v = p * p + d * p - d
        if v >= 0:
            return k, v == 0
        k += 1


def test_beyond_half():
    """Review round 7: the formula and the bars agree for every d <= 1/2 and stop agreeing only
    above it (the box paragraph); the corrected rule of the follow-up needs "no tie at p_k = T
    when d > 1/2"; the count of people is for a < 1; the last-person step of part b."""
    bad = []
    for ai in range(1, 601, 3):
        for di in range(1, 81):
            a, d = Fr(ai, 1000), Fr(di, 100)
            s = shares(a, d)
            winners = [i + 1 for i, v in enumerate(s) if v == max(s)]
            k, tie = exact_peak(a, d)
            if winners != ([k, k + 1] if tie else [k]):
                bad.append(d)
    assert bad and min(bad) > Fr(1, 2)
    # the follow-up's example: T = 0.6 = p_1 exactly, and still no tie
    a, d = Fr(3, 5), Fr(9, 10)
    assert exact_peak(a, d) == (1, True) and shares(a, d) == [Fr(3, 5), Fr(2, 5)]

    def corrected(a, d):
        k, tie = exact_peak(a, d)
        if d > Fr(1, 2):
            tie = False                                   # the added clause
        if k > 1 and k == len(shares(a, d)):              # the person of the formula is the last one
            before = a + (k - 2) * d
            if before >= Fr(1, 2):
                return k - 1, before == Fr(1, 2)
        return k, tie

    for den, amax, dmax in ((100, 100, 200), (30, 30, 60)):
        for an in range(1, amax):
            for dn in range(1, dmax):
                a, d = Fr(an, den), Fr(dn, den)
                s = shares(a, d)
                winners = [i + 1 for i, v in enumerate(s) if v == max(s)]
                k, tie = corrected(a, d)
                assert winners == ([k, k + 1] if tie else [k]), (a, d)
    # the count of people: the formula is for a < 1 (a = 1.5 is one person, the formula gives -4)
    assert len(shares(Fr(3, 2), Fr(1, 10))) == 1 and math.ceil((1 - Fr(3, 2)) / Fr(1, 10)) + 1 == -4
    # step 5 of part b: with d <= 1/2 the one before the last is at 1 - d >= 1/2 >= T or above
    for an in range(1, 200):
        for dn in range(1, 101):
            a, d = Fr(an, 200), Fr(dn, 200)
            n = len(shares(a, d))
            if n >= 2:
                p = a + (n - 2) * d
                assert p >= 1 - d >= Fr(1, 2) and p * p + d * p - d >= 0
    # the tie trap: d^2 + 4d = 49/144 = (7/12)^2 for d = 1/12
    d = Fr(1, 12)
    assert d * d + 4 * d == Fr(49, 144) == Fr(7, 12) ** 2
    # the geometric follow-up: its formula fails at q = 3 (a = 0.6: person 2, the shares 0.6 and 0.4)
    assert max(1, math.ceil(math.log(2 / 0.6, 3))) == 2 and cake.formula(cake.GEO, Fr(6, 10), Fr(3)) == 2


def test_box_tasks():
    """The cases the box paragraph names."""
    s = shares(Fr(1, 10), Fr(1, 10))
    assert [s[i + 1] / s[i] for i in range(3)] == [Fr(18, 10), Fr(12, 10), Fr(14, 15)]
    assert f"{float(Fr(14, 15)):.3f}" == "0.933" and max(s) == s[2] and cake.dec(s[2], 3) == "0.216"
    s = shares(Fr(27, 100), Fr(1, 10))
    assert (cake.dec(s[0]), cake.dec(s[1])) == ("0.2700", "0.2701") and max(s) == s[1]
    assert shares(Fr(1, 2), Fr(1, 2)) == [Fr(1, 2), Fr(1, 2)] and exact_peak(Fr(1, 2), Fr(1, 2)) == (1, True)
    assert shares(Fr(55, 100), Fr(8, 10)) == [Fr(55, 100), Fr(45, 100)] and exact_peak(Fr(55, 100), Fr(8, 10))[0] == 2


def test_js_matches_python():
    node = shutil.which("node")
    if not node:
        pytest.skip("node is not installed")
    params = [(a / 1000, d / 100) for a in range(5, 600, 37) for d in range(1, 51, 3)]
    script = (f"const m = require({json.dumps(str(ROOT / 'tools/explorer_node.js'))});"
              f"const ps = {json.dumps(params)};"
              "console.log(JSON.stringify(ps.map(([a, d]) => {"
              "  const rows = m.cakeSplit('arith', a, d);"
              "  return [rows.length, m.cakeBest(rows), m.cakeFormula('arith', a, d), m.cakeThreshold('arith', d)]; })));")
    out = json.loads(subprocess.run([node, "-e", script], capture_output=True, text=True, check=True).stdout)
    for (a, d), (n, best, f, T) in zip(params, out):
        s = shares(Fr(a).limit_denominator(10 ** 6), Fr(d).limit_denominator(10 ** 6))
        top = max(s)
        assert n == len(s)
        assert best == [i + 1 for i, v in enumerate(s) if v == top]
        assert f["k"] == best[0] and f["tie"] == (len(best) > 1)
        assert abs(T - cake.threshold(A, d)) < 1e-12


def test_js_proof_condition():
    """The proof panel of the box: "the next person gets more" is the condition curve against
    its level, person by person (the one before the last excluded, step 5), and the
    curve meets the level at the threshold."""
    from page_tests import explorer_require, node_json

    params = [(a / 1000, d / 100) for a in range(5, 600, 37) for d in range(1, 51, 3)]
    got = node_json(f"const m = {explorer_require()}; const ps = {json.dumps(params)};"
                    "console.log(JSON.stringify(ps.map(([a, d]) => {"
                    "  const rows = m.cakeSplit('arith', a, d);"
                    "  return [rows.map((r) => m.cakeCondition('arith', d, r.p).more),"
                    "          m.cakeCondition('arith', d, m.cakeThreshold('arith', d))]; })));")
    for (a, d), (more, at) in zip(params, got):
        a, d = Fr(a).limit_denominator(10 ** 6), Fr(d).limit_denominator(10 ** 6)
        s = shares(a, d)
        for k in range(len(s) - 2):
            if s[k + 1] != s[k]:
                assert more[k] == (s[k + 1] > s[k]), (a, d, k + 1)
        assert abs(at["g"] - at["level"]) < 1e-9


def test_js_trend_column():
    """The box's column "מול הקודם": every share's ratio to the one before and its side of
    1 (steps 2 and 3 of part a), against the exact split, ties included, for both laws."""
    from page_tests import explorer_require, node_json

    params = [(a / 1000, d / 100) for a in range(5, 600, 37) for d in range(1, 51, 3)] + [(1 / 12, 1 / 12), (0.27, 0.1)]
    got = node_json(f"const m = {explorer_require()}; const ps = {json.dumps(params)};"
                    "console.log(JSON.stringify(ps.map(([a, d]) => m.cakeTrend(m.cakeSplit('arith', a, d)))));")
    for (a, d), trend in zip(params, got):
        s = shares(Fr(a).limit_denominator(10 ** 6), Fr(d).limit_denominator(10 ** 6))
        assert len(trend) == len(s) and trend[0] is None
        for k in range(1, len(s)):
            assert trend[k]["dir"] == (s[k] > s[k - 1]) - (s[k] < s[k - 1]), (a, d, k + 1)
            assert abs(trend[k]["ratio"] - float(s[k] / s[k - 1])) < 1e-9 * float(s[k] / s[k - 1])
    assert got[-2][3]["dir"] == 0                   # a = d = 1/12: the tie of persons 3 and 4
    # part a: 10.89 for the second person, then above 1 up to the fourth and below 1 after
    part_a = node_json(f"const m = {explorer_require()}; console.log(JSON.stringify(m.cakeTrend(m.cakeSplit('arith', 0.01, 0.1))));")
    assert abs(part_a[1]["ratio"] - 10.89) < 1e-12 and [t["dir"] for t in part_a[1:]] == [1, 1, 1] + [-1] * 7


def test_js_wide_ranges():
    """The box's wide ranges: a negative d stops the queue at the first non-positive
    fraction, d = 0 never finishes (capped), and a tiny a = d lists 10,000 people with the
    hundredth on top, as the page's follow-up says."""
    from page_tests import explorer_require, node_json

    got = node_json(f"const m = {explorer_require()};"
                    "const r = (a, d) => { const rows = m.cakeSplit('arith', a, d); return [rows.length, m.cakeDone(rows), m.cakeBest(rows)]; };"
                    "console.log(JSON.stringify([r(0.01, -0.2), r(0.3, 0), r(0.0001, 0.0001), r(0.55, 0.8), m.CAKE_MAX]));")
    neg, zero, tiny, jump, cap = got
    assert neg == [1, False, [1]]
    assert zero == [cap, False, [1]]
    assert tiny == [10000, True, [100]]
    assert jump == [2, True, [1]]


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(27)
