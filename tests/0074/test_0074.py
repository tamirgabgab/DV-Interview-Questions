"""Question 0074: the page's rotate90 against new[i][j] = old[n-1-j][i] on every n up to 12;
transpose and transpose_no_marks against the definition on every m, n up to 12 (and some
larger and random shapes); the formula k -> k m mod (mn - 1); the page's numbers (20 swaps
for 5 x 5, the cycles of 2 x 3 and 3 x 5); the explorer's JavaScript against the generator;
and the page copies of the blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0074  # noqa: E402

ns = load_python(74)
rotate90, transpose, transpose_no_marks = ns["rotate90"], ns["transpose"], ns["transpose_no_marks"]


def test_rotate90():
    for n in range(0, 13):
        a = [[i * n + j for j in range(n)] for i in range(n)]
        want = q0074.rotated90(a)
        rotate90(a)
        assert a == want, n
    assert 5 * 4 // 2 + 5 * (5 // 2) == 20


def test_both_transposes_match_the_definition():
    shapes = [(m, n) for m in range(1, 13) for n in range(1, 13)] + [(64, 48), (100, 37), (1, 200)]
    rng = random.Random(74)
    shapes += [(rng.randint(1, 60), rng.randint(1, 60)) for _ in range(40)]
    for m, n in shapes:
        a = [rng.randint(0, 999) for _ in range(m * n)]
        want = q0074.transposed(a, m, n)
        for f in (transpose, transpose_no_marks):
            b = list(a)
            f(b, m, n)
            assert b == want, (f.__name__, m, n)


def test_the_formula_and_the_cycles():
    for m in range(1, 10):
        for n in range(1, 10):
            size = m * n
            where = {v: p for p, v in enumerate(q0074.transposed(list(range(size)), m, n))}
            assert all(where[k] == k * m % (size - 1) for k in range(1, size - 1))
    assert q0074.cycles(2, 3) == [[0], [1, 2, 4, 3], [5]]
    long = [c for c in q0074.cycles(3, 5) if len(c) > 1]
    assert long == [[1, 3, 9, 13, 11, 5], [2, 6, 4, 12, 8, 10]]


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    cases = [(m, n, leader) for m in range(1, 9) for n in range(1, 9) for leader in (False, True)]
    got = node_json(f"""
      const x = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([m, n, l]) => {{
        const f = x.tpSteps(m, n, l);
        return {{ arr: f[f.length - 1].arr, steps: f.length - 1, checks: x.tpChecks(m, n), cycles: x.tpCycles(m, n) }};
      }})));""")
    for (m, n, _), g in zip(cases, got):
        assert g["arr"] == q0074.transposed(list(range(m * n)), m, n), (m, n)
        assert g["steps"] == max(m * n - 2, 0) and g["checks"] == q0074.leader_checks(m, n)
        assert g["cycles"] == q0074.cycles(m, n)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(74)
