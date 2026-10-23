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
    assert math.ceil((T - 0.01) / 0.1) + 1 == 4 and f"{(T - 0.01) / 0.1:.2f}" == "2.60"
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


def test_follow_ups():
    # d > 1/2: the formula says person 2, person 1 gets more
    s = shares(Fr(55, 100), Fr(8, 10))
    assert s == [Fr(55, 100), Fr(45, 100)] and closed_form(Fr(55, 100), Fr(8, 10))[0] == 2
    # the threshold: below 1, about sqrt(d) for a small d
    for d in (Fr(1, 10 ** 6), Fr(1, 10), Fr(1, 2), Fr(3)):
        T = cake.threshold(A, d)
        assert 0 < T < 1
    assert abs(cake.threshold(A, Fr(1, 10 ** 6)) / 1e-3 - 1) < 1e-3


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
