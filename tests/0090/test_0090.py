"""Question 0090: pancake sorting. The page's Python code (it runs as published) against the
generator's independent reference (tools/figures/q0090.py): the simple algorithm on every
stack up to 7 (sorted, at most 2n - 3 flips, the same flips), the exact worst case by BFS
up to 8 (0, 1, 3, 4, 5, 7, 8, 9), a shortest sorting of the page's stack, the burnt
pancakes (at most 3n - 2 flips, the worst case 1, 4, 6, 8, 10, 12 up to 6, the sorted
stack with every burnt side up among the hardest), every number written on the page, the
breakpoints of the follow-up, and the box's model under Node."""

import sys
from itertools import permutations, product

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0090  # noqa: E402

ns = load_python(90)
PAGE = (ROOT / "docs" / "questions" / "senior" / "0090-pancake-sorting.md").read_text(encoding="utf-8")


def signed(n):
    for p in permutations(range(1, n + 1)):
        for signs in product((1, -1), repeat=n):
            yield [sg * v for sg, v in zip(signs, p)]


def test_simple_sort_on_every_stack():
    simple_sort = ns["simple_sort"]
    for n in range(1, 8):
        worst = 0
        for p in permutations(range(1, n + 1)):
            s, flips = simple_sort(list(p))
            assert s == list(range(1, n + 1)), p
            assert flips == [k for k, _ in q0090.simple(p)], p
            worst = max(worst, len(flips))
        assert worst == (2 * n - 3 if n >= 2 else 0), n


def test_the_page_example():
    s, flips = ns["simple_sort"]([3, 1, 5, 4, 2])
    assert flips == [3, 5, 2, 4, 2, 3, 2] and len(flips) == 7
    assert ns["flip"]([3, 1, 5, 4, 2], 3) == [5, 1, 3, 4, 2]
    d = ns["pancake_distances"](5)
    assert d[(3, 1, 5, 4, 2)] == 5
    best = ns["best_flips"]((3, 1, 5, 4, 2), d)
    assert best == [k for k, _ in q0090.best_path(q0090.EXAMPLE, q0090.distances(5))] == [2, 4, 2, 5, 2]
    s = (3, 1, 5, 4, 2)
    for k in best:
        s = s[:k][::-1] + s[k:]
    assert s == (1, 2, 3, 4, 5)


def test_pancake_numbers():
    want = [0, 1, 3, 4, 5, 7, 8, 9]
    assert [ns["pancake_number"](n) for n in range(1, 9)] == want
    rows = q0090.plain_table()
    assert [r["worst"] for r in rows] == want
    assert [r["count"] for r in rows] == [1, 1, 1, 3, 20, 2, 35, 455]
    for n in range(1, 8):
        assert ns["pancake_distances"](n) == q0090.distances(n)


def test_best_flips_are_shortest():
    for n in range(2, 7):
        d = ns["pancake_distances"](n)
        for p in permutations(range(1, n + 1)):
            flips = ns["best_flips"](p, d)
            assert len(flips) == d[p]
            s = p
            for k in flips:
                s = s[:k][::-1] + s[k:]
            assert s == tuple(range(1, n + 1))


def test_burnt_simple():
    burnt_simple, burnt_flip = ns["burnt_simple"], ns["burnt_flip"]
    assert burnt_flip([1, -2, 3], 2) == [2, -1, 3]
    for n in range(1, 7):
        worst = 0
        for st in signed(n):
            s, flips = burnt_simple(list(st))
            assert s == list(range(1, n + 1)), st
            assert flips == [k for k, _ in q0090.burnt_simple(st)], st
            worst = max(worst, len(flips))
        assert worst == 3 * n - 2, n
    assert burnt_simple([-1, -2, -3])[1] == [3, 1, 3, 2, 1, 2, 1]


def test_burnt_worst_case():
    want = [1, 4, 6, 8, 10, 12]
    for n in range(1, 7):
        d = ns["burnt_distances"](n)
        assert d == q0090.distances(n, burnt=True)
        assert max(d.values()) == want[n - 1]
        neg = tuple(-x for x in range(1, n + 1))
        assert d[neg] == max(d.values()), n
        assert len(d) == 2 ** n * q0090.factorial(n)
    rows = q0090.burnt_table()
    assert [r["worst"] for r in rows] == want + [14]
    assert [r["neg"] for r in rows] == want + [14]
    assert [r["count"] for r in rows] == [1, 1, 2, 3, 4, 1, 1]
    assert [r["simple"] for r in rows[:6]] == [3 * n - 2 for n in range(1, 7)]
    assert all(r["worst"] == 2 * r["n"] for r in rows[1:])
    path = q0090.best_path(q0090.BURNT, q0090.distances(3, burnt=True), burnt=True)
    assert len(path) == 6 and path[-1][1] == (1, 2, 3)


def test_breakpoints_follow_up():
    assert q0090.breakpoints((3, 1, 5, 4, 2)) == 4
    for n in range(2, 7):
        d = q0090.distances(n)
        assert all(q0090.breakpoints(p) <= d[p] for p in d)


def test_tight_examples():
    """Part a: from [2, 1, 3, ..., n], flips of k then 2 for k = 3..n give a stack that takes the
    simple algorithm exactly 2n - 3 flips; part c: the sorted stack with every burnt side up
    takes the burnt algorithm exactly 3n - 2, three flips a round."""
    for n in range(2, 13):
        s = [2, 1] + list(range(3, n + 1))
        for k in range(3, n + 1):
            s = ns["flip"](ns["flip"](s, k), 2)
        flips = ns["simple_sort"](s)[1]
        assert flips == [f for k in range(n, 2, -1) for f in (2, k)] + [2]        # each round undoes a step
        assert len(flips) == 2 * n - 3
        if n == 5:
            assert s == [1, 5, 3, 4, 2]
        neg = [-x for x in range(1, n + 1)]
        assert len(ns["burnt_simple"](neg)[1]) == 3 * n - 2
    assert "`[1,\u00a05,\u00a03,\u00a04,\u00a02]`" in PAGE


def test_box_tasks():
    """The numbers of the boxes' tasks."""
    d5 = ns["pancake_distances"](5)

    def shortest(s, d):
        if d[s] == 0:
            return 1
        return sum(shortest(t, d) for k in range(2, len(s) + 1)
                   for t in [s[:k][::-1] + s[k:]] if d[t] == d[s] - 1)

    assert shortest((3, 1, 5, 4, 2), d5) == 5 and "יש בדיוק 5 מיונים קצרים שונים" in PAGE
    d6 = ns["pancake_distances"](6)
    hard = sorted(p for p, v in d6.items() if v == max(d6.values()))
    assert len(hard) == 2 and hard[0] == (4, 6, 2, 5, 1, 3)
    assert "`[4,\u00a06,\u00a02,\u00a05,\u00a01,\u00a03]`" in PAGE
    neg6 = tuple(-x for x in range(1, 7))
    assert ns["burnt_distances"](6)[neg6] == 12 and len(ns["burnt_simple"](list(neg6))[1]) == 16
    assert "המינימום 12, והאלגוריתם הפשוט עושה עליה 16" in PAGE


def test_numbers_on_the_page():
    for words in ["7 הפיכות", "ב-5 הפיכות במקום 7", "0, 1, 3, 4, 5, 7, 8, 9", "13 מול 9", "40,320 ערימות",
                  "645,120 ערימות", "1, 4, 6, 8, 10, 12, 14", "יש 4, ולכן צריך לפחות 4 הפיכות. האמת היא 5",
                  "בדיוק 20 ערימות של 5", "צריך שש הפיכות", "\\( 3n - 2 \\)", "\\( 2n - 3 \\)",
                  "`[5,\u00a01,\u00a03,\u00a04,\u00a02]`"]:
        assert words in PAGE, words


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(90)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    got = node_json(f"const m = {explorer_require()};"
                    "const D = {};"
                    "for (let n = 2; n <= 6; n++) D['p' + n] = m.pkDist(n, false);"
                    "for (let n = 1; n <= 5; n++) D['b' + n] = m.pkDist(n, true);"
                    "console.log(JSON.stringify({ D,"
                    "flip: m.pkFlip([3, 1, 5, 4, 2], 3, false), bflip: m.pkFlip([1, -2, 3], 2, true),"
                    "best: m.pkBest([3, 1, 5, 4, 2], m.pkDist(5, false), false),"
                    "bbest: m.pkBest([-1, -2, -3], m.pkDist(3, true), true),"
                    "parse: [m.pkParse('3,1,5,4,2', false), m.pkParse('-1,-2,-3', true), m.pkParse('-1,2', false),"
                    "        m.pkParse('1,1,2', false), m.pkParse('2,3', false)],"
                    "hard: [3, 4, 5, 6, 7, 8].map((n) => m.pkHardest(n, false)), bhard: [2, 3, 4, 5, 6].map((n) => m.pkHardest(n, true)),"
                    "breaks: Object.keys(m.pkDist(5, false)).map((k) => [k, m.pkBreaks(k.split(',').map(Number), false)]),"
                    "bbreaks: Object.keys(m.pkDist(4, true)).map((k) => [k, m.pkBreaks(k.split(',').map(Number), true)]),"
                    "}));")
    for n in range(2, 7):
        assert {tuple(map(int, k.split(","))): v for k, v in got["D"][f"p{n}"].items()} == q0090.distances(n)
    for n in range(1, 6):
        assert {tuple(map(int, k.split(","))): v for k, v in got["D"][f"b{n}"].items()} == q0090.distances(n, burnt=True)
    assert got["flip"] == [5, 1, 3, 4, 2] and got["bflip"] == [2, -1, 3]
    assert got["best"] == [k for k, _ in q0090.best_path(q0090.EXAMPLE, q0090.distances(5))]
    assert got["bbest"] == [k for k, _ in q0090.best_path(q0090.BURNT, q0090.distances(3, burnt=True), burnt=True)]
    assert got["parse"] == [[3, 1, 5, 4, 2], [-1, -2, -3], None, None, None]
    for n, s in zip([3, 4, 5, 6, 7, 8], got["hard"]):
        d = q0090.distances(n)
        assert d[tuple(s)] == max(d.values()) and tuple(s) == min(p for p, v in d.items() if v == max(d.values()))
    for n, s in zip([2, 3, 4, 5, 6], got["bhard"]):
        assert s == [-x for x in range(1, n + 1)]
    # the box's broken adjacencies: the follow-up's count on plain stacks, and on burnt ones a
    # lower bound that is 0 only on the sorted stack
    d5 = q0090.distances(5)
    for k, b in got["breaks"]:
        p = tuple(map(int, k.split(",")))
        assert b == q0090.breakpoints(p) <= d5[p]
    d4 = q0090.distances(4, burnt=True)
    for k, b in got["bbreaks"]:
        p = tuple(map(int, k.split(",")))
        assert b <= d4[p] and (b == 0) == (p == (1, 2, 3, 4))
