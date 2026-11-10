"""Question 0074: the page's rotate90 against new[i][j] = old[n-1-j][i] on every n up to 12;
transpose and transpose_no_marks against the definition on every m, n up to 12 (and some
larger and random shapes); the formula k -> k m mod (mn - 1); the page's numbers (20 swaps
for 5 x 5, the cycles of 2 x 3 and 3 x 5, the mn - 2 writes of the page's code counted on
the array, the walk steps and their largest ratio, the first square matrix whose k * m
overflows a signed 32-bit int, the assignments of the two rotations at n = 100); the
streaming transposer's read order; the explorer's JavaScript against the generator (the
walks of the method without marks, one frame each); and the page copies of the blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0074  # noqa: E402

ns = load_python(74)
rotate90, transpose, transpose_no_marks = ns["rotate90"], ns["transpose"], ns["transpose_no_marks"]
PAGE = (ROOT / "docs" / "questions" / "junior" / "0074-transpose-matrix-in-place.md").read_text(encoding="utf-8")


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
        return {{ arr: f[f.length - 1].arr, steps: f.length - 1, checks: x.tpChecks(m, n), cycles: x.tpCycles(m, n),
                  puts: f.filter((q) => q.at !== null).map((q) => [q.s, q.put, q.at]),
                  walks: f.filter((q) => q.walk).map((q) => [q.s, q.walk, q.leader, q.checks]) }};
      }})));""")
    for (m, n, leader), g in zip(cases, got):
        size = m * n
        assert g["arr"] == q0074.transposed(list(range(size)), m, n), (m, n)
        assert g["checks"] == q0074.leader_checks(m, n)
        assert g["cycles"] == q0074.cycles(m, n)
        # the placements are the reference's, with marks and without
        assert [tuple(x) for x in g["puts"]] == [(s, hand, k) for s, hand, k, _ in q0074.placements(m, n)], (m, n)
        assert len(g["puts"]) == max(size - 2, 0)
        if not leader:
            assert g["steps"] == max(size - 2, 0) and g["walks"] == []
            continue
        # without marks every s from 1 to mn - 2 has a walk of its own: it starts at s, follows
        # k -> k m mod (mn - 1), ends at the first index that is not above s, and s is a leader
        # exactly when it is the smallest index of its cycle
        assert g["steps"] == 2 * max(size - 2, 0)
        assert [w[0] for w in g["walks"]] == list(range(1, size - 1))
        leaders = {c[0] for c in q0074.cycles(m, n)}
        total = 0
        for s, path, lead, checks in g["walks"]:
            assert path[0] == s and all(b == a * m % (size - 1) for a, b in zip(path, path[1:]))
            assert all(k > s for k in path[1:-1]) and path[-1] <= s
            assert lead == (path[-1] == s) == (s in leaders)
            total += len(path) - 1
            assert checks == total
        assert total == q0074.leader_checks(m, n)


class Counting(list):
    """A list that counts its writes."""
    writes = 0

    def __setitem__(self, k, v):
        Counting.writes += 1
        list.__setitem__(self, k, v)


def test_the_numbers_of_the_cost():
    # the page's code writes the array mn - 2 times, with marks and without
    for (m, n), want in zip(q0074.SIZES, (4, 13, 94, 3070, 3698)):
        for f in (transpose, transpose_no_marks):
            Counting.writes = 0
            f(Counting(range(m * n)), m, n)
            assert Counting.writes == want == m * n - 2 == len(q0074.placements(m, n)), (f.__name__, m, n)
    # the table's columns: the cycles that move, the places that stay, the walk steps
    rows = [(sum(len(c) > 1 for c in q0074.cycles(m, n)), sum(len(c) == 1 for c in q0074.cycles(m, n)),
             q0074.leader_checks(m, n)) for m, n in q0074.SIZES]
    assert rows == [(1, 2, 9), (2, 3, 33), (10, 2, 285), (20, 2, 20666), (516, 10, 10244)]
    # the box's tasks: 4 x 4 six cycles of 2, 2 x 7 one cycle of 12, 3 x 5 and 6 x 8 without marks
    assert [len(c) for c in q0074.cycles(4, 4) if len(c) > 1] == [2] * 6
    assert [len(c) for c in q0074.cycles(2, 7) if len(c) > 1] == [12]
    assert (len(q0074.placements(3, 5)), q0074.leader_checks(3, 5)) == (13, 33)
    assert (len(q0074.placements(6, 8)), q0074.leader_checks(6, 8)) == (46, 160)
    k, walk = 3 * 3 % 14, []
    while k > 3:
        walk.append(k)
        k = k * 3 % 14
    assert (walk, k) == ([9, 13, 11, 5], 1)
    # the walk steps per entry: at most 14.9 on every shape from 2 x 2 to 120 x 120, at 98 x 78
    best = max((q0074.leader_checks(m, n) / (m * n), m, n) for m in range(2, 121) for n in range(2, 121))
    assert best[1:] == (98, 78) and q0074.leader_checks(98, 78) == 113605 and 14.8 < best[0] < 14.9
    # k * m in a signed 32-bit int: the largest product on n x n is (n^2 - 2) n
    assert (1290 ** 2 - 2) * 1290 < 2 ** 31 <= (1291 ** 2 - 2) * 1291 and 1291 ** 3 > 2 ** 31
    # the two rotations at n = 100: 3 assignments a swap, 5 assignments for every 4 cells
    n = 100
    assert 3 * (n * (n - 1) // 2 + n * (n // 2)) == 29850 and 5 * n * n // 4 == 12500
    for text in ("14.9", "98×78", "1291×1291", "1290×1290", "29,850", "12,500", "‏\\( mn - 2 \\) הנחות"):
        assert text in PAGE, text


def test_the_streaming_transposer():
    for m in range(1, 9):
        for n in range(1, 9):
            order = q0074.read_order(m, n)
            assert order == [i * n + j for j in range(n) for i in range(m)]
            a = list(range(100, 100 + m * n))
            assert [a[k] for k in order] == q0074.transposed(a, m, n)
    assert [(r[1], r[3], r[4]) for r in q0074.hw_rows(2, 3)] == [(0, 0, "a"), (1, 3, "d"), (2, 1, "b"), (3, 4, "e"), (4, 2, "c"), (5, 5, "f")]


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(74)
