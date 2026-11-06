"""Question 0086: the chameleons. Every number on the page is recomputed with the generator's
breadth-first search (part a: no single colour from 13, 15, 17, the residues turning
together; part b: the condition both ways and the construction; part c: the closed form for
every colour and every state with counts up to 12, the 16 meetings of 13, 16, 17, the
examples table, the triangle of 2, 5, 4, and the follow-ups: 14, 15, 17, and the reachable
states being exactly the states with the same residues); the generated blocks are checked;
and the box's model is compared under Node with this reference."""

import sys

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0086  # noqa: E402

PAGE = (ROOT / "docs" / "questions" / "junior" / "0086-chameleons.md").read_text(encoding="utf-8")
N = 12


def every_state(n_max=N):
    return [(r, g, b) for r in range(n_max + 1) for g in range(n_max + 1) for b in range(n_max + 1) if r + g + b]


def test_part_a():
    dist = q0086.distances(q0086.START)
    assert all(q0086.mono(45, c) not in dist for c in range(3))
    assert [v % 3 for v in q0086.START] == [1, 0, 2]
    # every meeting adds 2 to every count mod 3: the residues stay pairwise different
    for s in dist:
        assert sorted(v % 3 for v in s) == [0, 1, 2]
    rows = q0086.first_meetings()
    assert [tuple(v % 3 for v in s) for _, s in rows] == [(1, 0, 2), (0, 2, 1), (2, 1, 0), (1, 0, 2)]


def test_part_b_condition_both_ways():
    for s in every_state():
        dist = q0086.distances(s)
        some = any(q0086.mono(sum(s), c) in dist for c in range(3))
        assert some == any((s[i] - s[j]) % 3 == 0 for i, j in q0086.PAIRS), s
        for c in range(3):
            x, y = (s[k] for k in range(3) if k != c)
            if (x - y) % 3 == 0 and not (s[c] == 0 and min(x, y) == 0 and max(x, y) > 0):
                plan = q0086.construct(s, c)
                assert len(plan) == max(x, y) and (not plan or plan[-1][1] == q0086.mono(sum(s), c)), (s, c)


def test_part_b_example():
    plan = q0086.construct(q0086.CONSTRUCT, 2)
    assert [s for _, s in plan] == [(6, 0, 5), (5, 2, 4), (4, 1, 6), (3, 0, 8), (2, 2, 7), (1, 1, 9), (0, 0, 11)]
    assert 7 % 3 == 1 % 3


def test_part_c_closed_form():
    for s in every_state():
        dist = q0086.distances(s)
        for c in range(3):
            assert q0086.formula_to(s, c) == dist.get(q0086.mono(sum(s), c)), (s, c)
    assert q0086.formula_min((13, 16, 17)) == (16, 2)
    assert q0086.distances((13, 16, 17))[(0, 0, 46)] == 16
    # all three congruent: the most common colour, and the middle count
    for s in every_state():
        if len({v % 3 for v in s}) == 1 and sum(1 for v in s if v) >= 2:
            m, c = q0086.formula_min(s)
            assert m == sorted(s)[1] and q0086.formula_to(s, s.index(max(s))) == m, s


def test_triangle_and_examples():
    dist = q0086.distances(q0086.SMALL)
    assert len(dist) == 26 and len(q0086.states(11)) == 78 and 3 * 26 == 78
    assert q0086.mono(11, 2) in dist and q0086.mono(11, 0) not in dist and q0086.mono(11, 1) not in dist
    assert len(q0086.construct(q0086.SMALL, 2)) == 5
    want = [None, (16, 2), (17, 1), (4, 2), (3, 0), (8, 2), (3, 0), (0, 0)]
    for s, w in zip(q0086.EXAMPLES, want):
        assert q0086.formula_min(s) == w, s
        dist = q0086.distances(s)
        if w is not None:
            assert dist[q0086.mono(sum(s), w[1])] == w[0]


def test_follow_ups():
    assert q0086.formula_min((14, 15, 17)) == (17, 1)
    dist = q0086.distances(q0086.START)
    assert len(dist) == 360 and len(q0086.states(45)) == 1081
    # the reachable states are exactly the states with the same residues of the differences
    for n in range(1, 16):
        alls = q0086.states(n)
        for s in alls:
            if sum(1 for v in s if v) < 2:
                continue
            same = {t for t in alls if q0086.invariant(t) == q0086.invariant(s)}
            assert set(q0086.distances(s)) == same, s


def test_page_text():
    for words in ["\\( \\max(x, y) \\)", "16 פגישות", "360 מתוך 1,081", "\\( r - p - q + 2s = 0 \\)",
                  "\\( \\max(14, 17) = 17 \\)", "13, 15 ו-17", "סכום עד 15", "\\( r, g, b \\le 12 \\)"]:
        assert words in PAGE, words


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(86)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    cases = every_state(9)
    got = node_json(f"const m = {explorer_require()};"
                    f"const cases = {[list(c) for c in cases]};"
                    "console.log(JSON.stringify({"
                    "to: cases.map((s) => [0, 1, 2].map((c) => m.chTo(s, c))),"
                    "min: cases.map((s) => m.chMin(s)),"
                    "plan: cases.map((s) => [0, 1, 2].map((c) => m.chTo(s, c) === null ? null : m.chPlan(s, c))),"
                    "dist: m.chDist([2, 5, 4]),"
                    "meet: m.chMeet([13, 15, 17], 1, 2),"
                    "}));")
    for s, to, mn, plans in zip(cases, got["to"], got["min"], got["plan"]):
        assert to == [q0086.formula_to(s, c) for c in range(3)], s
        assert (None if mn is None else tuple(mn)) == q0086.formula_min(s), s
        for c, p in enumerate(plans):
            want = None if q0086.formula_to(s, c) is None else [list(x) for x, _ in q0086.construct(s, c)]
            assert p == want, (s, c)
    assert {tuple(map(int, k.split(","))): d for k, d in got["dist"].items()} == q0086.distances(q0086.SMALL)
    assert got["meet"] == [15, 14, 16]
