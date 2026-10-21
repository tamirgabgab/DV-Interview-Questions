"""Question 0028 has no code on the page; these tests split the cake with exact fractions,
check every number the page states, check the closed form and the single peak over a grid
of parameters (and the stated counterexample above q = 2), run the slider script under
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

G = cake.GEO


def shares(a, q):
    """Independent split: walk the queue, cap the fraction at 1."""
    out, left, p = [], Fr(1), Fr(a)
    while True:
        take = min(p, Fr(1))
        out.append(take * left)
        if take == 1:
            return out
        left -= take * left
        p *= q


def closed_form(a, q):
    """The page's formula: k = max(1, ceil(log_q((q - 1) / a))), tie when q^k = (q - 1) / a;
    the logarithm is settled exactly by comparing powers."""
    k = 1
    while a * q ** k < q - 1:
        k += 1
    return k, a * q ** k == q - 1


def test_part_a():
    a, q = Fr(1, 100), Fr(3, 2)
    s = shares(a, q)
    assert len(s) == 13
    assert max(s) == s[9] and cake.dec(s[9], 3) == "0.170" and cake.dec(s[9]) == "0.1697"
    assert all(s[i] < s[i + 1] for i in range(9)) and all(s[i] > s[i + 1] for i in range(9, 12))
    assert 1 - 1 / q == Fr(1, 3) and (q - 1) / a == 50
    x = math.log(50) / math.log(1.5)
    assert f"{x:.2f}" == "9.65" and math.ceil(x) == 10
    assert cake.dec(a * q ** 8, 3) == "0.256" and cake.dec(a * q ** 9, 3) == "0.384"
    assert a * q ** 8 < Fr(1, 3) <= a * q ** 9
    R10 = 1 - sum(s[:9])
    assert cake.dec(R10) == "0.4415" and R10 < Fr(6, 10) * 1 and 1 - R10 < Fr(6, 10)
    assert cake.dec(s[-1]) == "0.0155"
    assert a * q ** 12 > 1 and cake.dec(a * q ** 12, 1) == "1.3"
    # the wrong logarithm finds the last person
    assert math.ceil(math.log(100) / math.log(1.5)) + 1 == 13


def test_statement_example():
    s = shares(Fr(1, 10), Fr(2))
    assert len(s) == 5 and Fr(1, 10) * 2 ** 4 == Fr(8, 5)


def test_q_table():
    a = Fr(1, 100)
    for q, k, share in ((Fr(2), 7, "0.313"), (Fr(3, 2), 10, "0.170"), (Fr(11, 10), 25, "0.040")):
        s = shares(a, q)
        assert s.index(max(s)) + 1 == k == closed_form(a, q)[0]
        assert cake.dec(max(s), 3) == share


def test_tie_example():
    s = shares(Fr(1, 4), Fr(2))
    assert s[1] == s[2] == max(s) == Fr(3, 8)
    assert closed_form(Fr(1, 4), Fr(2)) == (2, True)


def test_closed_form_and_single_peak():
    qs = [Fr(n, 20) for n in range(21, 41)]                 # 1.05 .. 2
    for da in range(1, 201, 3):
        for q in qs:
            a = Fr(da, 400)
            s = shares(a, q)
            top = max(s)
            winners = [i + 1 for i, v in enumerate(s) if v == top]
            k, tie = closed_form(a, q)
            assert winners == ([k, k + 1] if tie else [k]), (a, q)
            peak = winners[0]
            assert all(s[i] < s[i + 1] for i in range(peak - 1))
            assert all(s[i] >= s[i + 1] for i in range(peak - 1, len(s) - 1))
            assert cake.formula(G, a, q) == k
            n = 0
            while a * q ** n < 1:
                n += 1
            assert len(s) == n + 1                           # ceil(log_q(1/a)) + 1


def test_follow_ups():
    # q > 2: the formula says person 2, person 1 gets more
    s = shares(Fr(6, 10), Fr(3))
    assert s == [Fr(6, 10), Fr(4, 10)] and closed_form(Fr(6, 10), Fr(3))[0] == 2
    # q <= 1: the first person gets the most
    for q in (Fr(1), Fr(9, 10), Fr(1, 2)):
        s = []
        left, p = Fr(1), Fr(1, 10)
        for _ in range(30):
            s.append(p * left)
            left -= p * left
            p *= q
        assert s.index(max(s)) == 0


def test_js_matches_python():
    node = shutil.which("node")
    if not node:
        pytest.skip("node is not installed")
    params = [(a / 1000, q / 100) for a in range(1, 500, 23) for q in range(105, 201, 5)]
    script = (f"const m = require({json.dumps(str(ROOT / 'docs/javascripts/explorer.js'))});"
              f"const ps = {json.dumps(params)};"
              "console.log(JSON.stringify(ps.map(([a, q]) => {"
              "  const rows = m.cakeSplit('geo', a, q);"
              "  return [rows.length, m.cakeBest(rows), m.cakeFormula('geo', a, q)]; })));")
    out = json.loads(subprocess.run([node, "-e", script], capture_output=True, text=True, check=True).stdout)
    for (a, q), (n, best, f) in zip(params, out):
        A, Q = Fr(a).limit_denominator(10 ** 6), Fr(q).limit_denominator(10 ** 6)
        s = shares(A, Q)
        top = max(s)
        assert n == len(s)
        assert best == [i + 1 for i, v in enumerate(s) if v == top], (a, q)
        assert (f["k"], f["tie"]) == closed_form(A, Q), (a, q)


def test_js_wide_ranges():
    """The box's wide ranges: q below 1 never finishes (the queue stops at a negligible
    fraction, the first person on top), q = 3 with a = 0.6 is the page's two-person case."""
    from page_tests import explorer_require, node_json

    got = node_json(f"const m = {explorer_require()};"
                    "const r = (a, q) => { const rows = m.cakeSplit('geo', a, q); return [rows.length, m.cakeDone(rows), m.cakeBest(rows), rows[rows.length - 1].p]; };"
                    "console.log(JSON.stringify([r(0.01, 0.9), r(0.5, 1), r(0.6, 3), m.CAKE_MAX]));")
    below, one, three, cap = got
    assert below[1] is False and below[2] == [1] and below[3] < 1e-8 and below[0] < cap
    assert one == [cap, False, [1], 0.5]
    assert three[:3] == [2, True, [1]]


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(28)
