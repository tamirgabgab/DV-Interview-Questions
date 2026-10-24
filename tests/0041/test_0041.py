"""Question 0041: every number the page states (54.1 and 518.7 expected, 90 and 754 tests
for 95 %, the waits table, the quantiles table, the examples of part b), the page's chain
against inclusion-exclusion with exact fractions, the page's integral against the k = 1
closed form and against the page's own simulation (within the statistical error), the
generator's reference, the explorer's JavaScript, and the page copies of the generated
blocks."""

import json
import math
import random
import sys
from fractions import Fraction

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0041  # noqa: E402

ns = load_python(41)
expected_uniform, cover_curve, quantile = ns["expected_uniform"], ns["cover_curve"], ns["tests_for"]   # not "tests_for": pytest would collect it
expected_tests, expected_k1, simulate_tests = ns["expected_tests"], ns["expected_k1"], ns["simulate_tests"]


def test_page_numbers():
    assert abs(expected_uniform(16) - 54.09) < 0.01 and abs(expected_uniform(100) - 518.74) < 0.01
    assert quantile(16, 0.95) == 90 and quantile(100, 0.95) == 754
    assert quantile(16, 0.5) == 51 and quantile(100, 0.5) == 497
    assert abs(expected_uniform(16) - 16 * sum(Fraction(1, i) for i in range(1, 17))) < 1e-9
    assert abs(cover_curve(16, 54)[54] - 0.59) < 0.005                       # the trap: 54 tests give ~59 %
    assert abs(cover_curve(100, 100)[100]) < 1e-6                             # 100 tests on 100 bins: hopeless
    assert abs(expected_k1([0.1, 0.2, 0.3, 0.4]) - 12.36) < 0.005
    assert abs(expected_tests([0.01] + [0.99 / 15] * 15, 1) - 111.8) < 0.05
    assert abs(expected_tests([1 / 16] * 16, 4) - 132.0) < 0.05
    assert abs(expected_uniform(256) - 1568) < 0.5 and quantile(256, 0.95) == 2176   # the cross follow-up
    assert abs(16 * math.log(16 * 20) - 92.3) < 0.1                           # the approximation n ln(20 n)
    assert abs(sum(16 / (16 - i) for i in range(14)) - 30.09) < 0.01          # 90 % of 16 bins


def test_chain_matches_exact_inclusion_exclusion():
    for n in (1, 2, 3, 5, 8, 12):
        curve = cover_curve(n, 60)
        for t in range(61):
            exact = sum((-1) ** j * math.comb(n, j) * Fraction(n - j, n) ** t for j in range(n + 1))
            assert abs(curve[t] - float(exact)) < 1e-12, (n, t)
            assert abs(curve[t] - q0041.covered_by_exact(n, t)) < 1e-12
        assert q0041.cover_curve(n, 60) == curve
        # the expectation is the sum of the tail
        assert abs(sum(1 - v for v in cover_curve(n, 4000)) - expected_uniform(n)) < 1e-6
        assert quantile(n, 0.95) == q0041.tests_for(n, 0.95)


def test_integral_matches_the_closed_form_and_the_uniform_case():
    rng = random.Random(41)
    for n in (1, 2, 4, 8):
        p = [1 / n] * n
        assert abs(expected_tests(p, 1) - expected_uniform(n)) < 0.02
        assert abs(expected_k1(p) - expected_uniform(n)) < 1e-9
    for _ in range(20):
        n = rng.randint(1, 8)
        w = [rng.random() + 0.05 for _ in range(n)]
        p = [x / sum(w) for x in w]
        assert abs(expected_tests(p, 1) - expected_k1(p)) < 0.02 + 0.001 * expected_k1(p), p
        assert abs(expected_tests(p, 1) - q0041.expected_general(p, 1)) < 0.02
        assert abs(expected_k1(p) - q0041.expected_k1(p)) < 1e-9


def test_simulation_agrees_with_the_integral():
    rng = random.Random(4141)
    cases = [([0.25] * 4, 1), ([0.1, 0.2, 0.3, 0.4], 1), ([0.25] * 4, 2), ([0.1, 0.2, 0.3, 0.4], 3), ([1 / 16] * 16, 1), ([1 / 8] * 8, 3)]
    for p, k in cases:
        runs = 4000
        samples = [simulate_tests(p, k, rng) for _ in range(runs)]
        mean = sum(samples) / runs
        sd = (sum((x - mean) ** 2 for x in samples) / runs) ** 0.5
        exact = expected_tests(p, k)
        assert abs(mean - exact) < 4 * sd / runs ** 0.5 + 0.05, (p, k, mean, exact)
        assert all(x >= k * len(p) for x in samples)


def test_tables():
    waits = q0041.waits_table().splitlines()[2:]
    assert waits[-1].endswith("‏**54.1** |") and waits[-2].startswith("| ‏15 | ‏1/16 | ‏16.00 |")
    rows = q0041.quantiles_table().splitlines()[2:]
    assert [r.split("|")[1].strip().lstrip("‏") for r in rows] == ["4", "8", "16", "32", "64", "100"]
    assert "| ‏54.1 | ‏51 | ‏90 | ‏115 |" in rows[2] and "| ‏518.7 | ‏497 | ‏754 | ‏916 |" in rows[5]
    ex = q0041.examples_table().splitlines()[2:]
    assert len(ex) == len(q0041.EXAMPLES)
    assert "‏12.36" in ex[1] and "‏111.79" in ex[5] and "‏132.00" in ex[6]


def test_explorer_matches_the_page_code():
    from page_tests import explorer_require, node_json

    cases = [[[1, 1, 1, 1], 1], [[1, 2, 3, 4], 1], [[1, 1, 1, 1], 2], [[1, 2, 3, 4], 3], [[1] * 10, 1], [[1, 9], 4]]
    got = node_json(f"""
      const m = {explorer_require()};
      const r = {json.dumps(cases)}.map(([w, k]) => {{ const p = m.covProbs(w); return [p, m.covExpected(p, k), k === 1 ? m.covK1(p) : null, m.covSimulate(p, k, m.mulberry32(7))]; }});
      console.log(JSON.stringify([r, m.covCurve(16, 90), m.covQuantile(16, 0.95), m.covQuantile(100, 0.95)]));""")
    runs, curve, q16, q100 = got
    for (w, k), (p, e, k1, sim) in zip(cases, runs):
        assert all(abs(x - y) < 1e-12 for x, y in zip(p, [x / sum(w) for x in w]))
        assert abs(e - expected_tests(p, k)) < 0.02 + 0.001 * e
        if k == 1:
            assert abs(k1 - expected_k1(p)) < 1e-9
        assert sim >= k * len(w)
    page = cover_curve(16, 90)
    assert all(abs(a - b) < 1e-12 for a, b in zip(curve, page))
    assert q16 == 90 and q100 == 754


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(41)


def test_explorer_stages():
    """The stage box of part a (J297): the expected wait of stage i -> i + 1 is n / (n - i)
    and the waits add up to the page's expected_uniform (54.1 for 16 bins, the page's
    table); a run's waits cut its tests exactly at the tests that find a new bin; and the
    mean wait per stage over many runs sits on n / (n - i)."""
    import json

    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      const rnd = m.mulberry32(41), out = {{ exp: {{}}, runs: [], avg: m.stageAverage(8, 20000, m.mulberry32(7)) }};
      for (let n = 2; n <= 20; n++) out.exp[n] = m.stageExpect(n);
      for (let r = 0; r < 200; r++) {{ const n = 2 + (r % 19); out.runs.push([n, m.stageRun(n, rnd)]); }}
      console.log(JSON.stringify(out));""")
    for n in range(2, 21):
        exp = got["exp"][str(n)]
        assert all(abs(e - n / (n - i)) < 1e-12 for i, e in enumerate(exp))
        assert abs(sum(exp) - expected_uniform(n)) < 1e-9
    assert round(sum(got["exp"]["16"]), 1) == 54.1
    assert [round(got["exp"]["16"][i], 2) for i in (0, 1, 2, 4, 8, 12, 14, 15)] == [1.0, 1.07, 1.14, 1.33, 2.0, 4.0, 8.0, 16.0]
    for n, r in got["runs"]:
        draws, waits = r["draws"], r["waits"]
        assert len(waits) == n and sum(waits) == len(draws) and all(0 <= b < n for b in draws)
        seen, t = set(), 0
        for w in waits:
            stage = draws[t:t + w]
            assert all(b in seen for b in stage[:-1]) and stage[-1] not in seen
            seen.add(stage[-1])
            t += w
        assert seen == set(range(n))
    for i, a in enumerate(got["avg"]):
        assert abs(a - 8 / (8 - i)) < 0.25, (i, a)
