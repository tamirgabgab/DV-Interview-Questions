"""Question 0083: the water jugs. Every number on the page is recomputed with the generator's
breadth-first search (the 6 and 8 steps of part a, the 16 of 24 states on the edge of the
grid, the gcd rule both ways, the examples table, the 7 and 8 pours of part c and the
follow-ups: the total in both jugs, the two keep-pouring plans against the BFS, the depth-first
search of the trap); the generated blocks are checked; and the jugs box's model is compared
under Node with this reference."""

import sys
from math import gcd

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0083  # noqa: E402

PAGE = (ROOT / "docs" / "questions" / "student" / "0083-water-jugs.md").read_text(encoding="utf-8")


def test_part_a():
    assert len(q0083.PLAN) == 6 and q0083.PLAN[-1][1] == (3, 4)
    assert [m for m, _ in q0083.PLAN] == [("fill", 1), ("pour", 1, 0), ("empty", 0), ("pour", 1, 0), ("fill", 1), ("pour", 1, 0)]
    assert len(q0083.OTHER) == 8 and q0083.OTHER[-1][1] == (0, 4)
    assert q0083.keep_pouring(3, 5, 4, from_a=False) == q0083.PLAN
    assert q0083.count_shortest((3, 5), 4) == 1                       # only one plan of six
    dist = q0083.distances((3, 5))
    assert len(dist) == 16 and 4 * 6 == 24
    assert min(d for s, d in dist.items() if 4 in s) == 6
    assert 2 * 5 - 2 * 3 == 4 and 3 * 3 - 5 == 4


def test_states_on_the_edge_and_the_gcd_rule():
    for a in range(1, 10):
        for b in range(1, 13):
            dist = q0083.distances((a, b))
            assert all(x in (0, a) or y in (0, b) for x, y in dist), (a, b)
            reach = {v for s in dist for v in s}
            for t in range(0, 15):
                assert (t in reach) == (t <= max(a, b) and t % gcd(a, b) == 0), (a, b, t)
            # the keep-pouring construction: k jugs of the smaller poured leave k*a mod b
            lo, hi = min(a, b), max(a, b)
            g = gcd(a, b)
            assert {k * lo % hi for k in range(hi // g)} == set(range(0, hi, g))


def test_examples_table():
    rows = {(a, b, t): q0083.shortest(a, b, t) for a, b, t in q0083.EXAMPLES}
    assert [None if p is None else len(p) for p in rows.values()] == [6, 4, 2, 2, None, 6, 10, None]
    table = q0083.examples_table()
    assert table.count("| כן |") == 6 and table.count("| לא |") == 2


def test_part_c():
    assert len(q0083.PLAN3) == 7 and q0083.PLAN3[-1][1] == (4, 4, 0)
    assert [(q0083.CAPS3[m[1]], q0083.CAPS3[m[2]]) for m, _ in q0083.PLAN3] == [(8, 5), (5, 3), (3, 8), (5, 3), (8, 5), (5, 3), (3, 8)]
    assert len(q0083.OTHER3) == 8 and q0083.OTHER3[0][0] == ("pour", 0, 2) and q0083.OTHER3[-1][1] == (4, 4, 0)
    dist = q0083.distances(q0083.CAPS3, q0083.START3, tap=False)
    assert len(dist) == 16 and 6 * 4 == 24 and all(sum(s) == 8 for s in dist)
    assert all(y in (0, 5) or z in (0, 3) or x in (0, 8) for x, y, z in dist)
    assert q0083.count_shortest(q0083.CAPS3, q0083.GOAL3, q0083.START3, tap=False) == 1


def test_follow_ups_and_traps():
    # the total in both jugs: every multiple of gcd up to a + b; 7 with 3 and 5 in five steps
    for a in range(1, 9):
        for b in range(1, 11):
            sums = {sum(s) for s in q0083.distances((a, b))}
            assert sums == {t for t in range(a + b + 1) if t % gcd(a, b) == 0}, (a, b)
    seven = q0083.bfs((3, 5), lambda s: sum(s) == 7)
    assert len(seven) == 5 and seven == q0083.PLAN[:5] and seven[-1][1] == (2, 5)
    # without BFS: the shorter of the two keep-pouring plans is the minimum
    for a in range(1, 10):
        for b in range(1, 13):
            for t in range(1, max(a, b) + 1):
                p = q0083.shortest(a, b, t)
                if p is None:
                    continue
                plans = [q0083.keep_pouring(a, b, t, f) for f in (True, False)]
                assert min(len(x) for x in plans if x is not None) == len(p), (a, b, t)
    # the trap: a depth-first search that tries "fill A" first stops after eight steps
    seen, path = {(0, 0)}, []

    def go(s):
        if 4 in s:
            return True
        for m, n in q0083.moves((3, 5), s):
            if n not in seen:
                seen.add(n)
                path.append(n)
                if go(n):
                    return True
                path.pop()
        return False

    assert go((0, 0)) and len(path) == 8
    # 7 litres: gcd 1 divides it, but no jug holds 7
    assert q0083.shortest(3, 5, 7) is None


def test_page_text():
    for words in ["שישה צעדים", "שמונה צעדים", "16 מתוך 24", "שבע מזיגות", "צריך שמונה", "\\( 2 \\cdot 5 - 2 \\cdot 3 = 4 \\)",
                  "\\( 3 \\cdot 3 - 5 = 4 \\)", "ב-3 ו-5 אלה 8 ו-6 צעדים", "חמשת הצעדים הראשונים של סעיף א"]:
        assert words in PAGE, words


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(83)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    cases = [(a, b, t) for a in range(1, 8) for b in range(1, 10) for t in range(0, 11)]
    got = node_json(f"const m = {explorer_require()};"
                    f"const cases = {[list(c) for c in cases]};"
                    "console.log(JSON.stringify({"
                    "bfs: cases.map(([a, b, t]) => m.jugBfs([a, b], [0, 0], t, true)),"
                    "can: cases.map(([a, b, t]) => m.jugCan(a, b, t)),"
                    "dist: m.jugDist([3, 5], [0, 0], true),"
                    "three: m.jugBfs([8, 5, 3], [8, 0, 0], [4, 4, 0], false),"
                    "three2: m.jugBfs([10, 7, 3], [10, 0, 0], [5, 5, 0], false),"
                    "dist3: m.jugDist([8, 5, 3], [8, 0, 0], false),"
                    "pour: m.jugApply([3, 5], [0, 5], ['pour', 1, 0]),"
                    "}));")
    tup = lambda path: None if path is None else [(tuple(m), tuple(s)) for m, s in path]  # noqa: E731
    for (a, b, t), path in zip(cases, got["bfs"]):
        assert tup(path) == q0083.shortest(a, b, t), (a, b, t)
    assert got["can"] == [q0083.measurable(a, b, t) for a, b, t in cases]
    assert {tuple(map(int, k.split(","))): d for k, d in got["dist"].items()} == q0083.distances((3, 5))
    assert tup(got["three"]) == q0083.PLAN3
    assert tup(got["three2"]) == q0083.bfs((10, 7, 3), lambda s: s == (5, 5, 0), (10, 0, 0), tap=False)
    assert {tuple(map(int, k.split(","))): d for k, d in got["dist3"].items()} == q0083.distances(q0083.CAPS3, q0083.START3, tap=False)
    assert got["pour"] == [3, 2]
