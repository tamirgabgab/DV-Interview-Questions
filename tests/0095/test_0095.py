"""Question 0095: the numbers the page states, the generated blocks, and the soldiers box.

Every number is recomputed exactly: the weights in p + q·σ with integers (the generator's
reference, apart from the page's Q5), the heaviest cells for rows 1 to 4 (the potential's
bounds 2, 4, 8 and 19, the 20 heaviest weighing 1 + σ^8), the three kinds of jumps, the
half plane for rows 1 to 5, the line of the follow-up and the diagonal jump. The box's
stored plays, its jump and its potential are compared with the page's code under Node."""

import random
import re
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0095  # noqa: E402

ns = load_python(95)
Q5, SIGMA, potential, half_plane, replay, jump = ns["Q5"], ns["SIGMA"], ns["potential"], ns["half_plane"], ns["replay"], ns["jump"]
PAGE = (ROOT / "docs" / "questions" / "senior" / "0095-conways-soldiers.md").read_text(encoding="utf-8")


def z(u):
    """p + q·σ as Q5."""
    return u[0] + u[1] * SIGMA


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(95)


def test_the_heaviest_cells():
    # the potential's bound: the fewest cells that weigh 1 together
    assert [q0095.fewest_by_weight(n) for n in (1, 2, 3, 4)] == [2, 4, 8, 19]
    assert z(q0095.top(1, 1)) < 1 and z(q0095.top(2, 3)) < 1 and z(q0095.top(3, 7)) < 1
    assert z(q0095.top(4, 18)) < 1 and z(q0095.top(4, 19)) == 1
    assert z(q0095.top(4, 20)) == 1 + SIGMA ** 8                      # 1 + σ^8 ≈ 1.0213
    assert f"{float(1 + SIGMA ** 8):.4f}" == "1.0213"
    # the same with the page's Q5, cell by cell
    for n, k in ((2, 3), (3, 7), (4, 19), (4, 20)):
        cells = sorted(((x, y) for x in range(-k, k + 1) for y in range(-k, 1)),
                       key=lambda c: abs(c[0]) + n - c[1])[:k]
        assert potential(cells, n) == z(q0095.top(n, k))


def test_half_plane_table():
    phi = 1 / SIGMA
    for n, shown in ((1, "6.854"), (2, "4.236"), (3, "2.618"), (4, "1.618")):
        assert half_plane(n) == phi ** (5 - n)
        assert f"{float(half_plane(n)):.3f}" == shown and shown in PAGE
    assert half_plane(5) == 1
    assert f"{(5 ** 0.5 - 1) / 2:.3f}" == "0.618"


def test_the_three_kinds_of_jumps():
    s = SIGMA
    for k in range(1, 12):
        assert s ** k - s ** (k + 1) - s ** (k + 2) == 0                 # toward the target
        assert s ** (k + 2) - s ** k - s ** (k + 1) == -2 * s ** (k + 1)  # away
        assert s ** k - s ** k - s ** (k - 1) == -(s ** (k - 1))          # across
    # the closed form, step by step as on the page
    assert s ** 5 * (1 / (1 - s)) * (1 + 2 * s / (1 - s)) == s ** 3 + 2 * s ** 2 == 1


def test_follow_ups():
    s = SIGMA
    assert s ** 2 / (1 - s) == 1                                          # the line, target x = 2
    assert 1 - s ** 2 - s ** 4 > 0                                        # a diagonal jump gains
    # on a line, two soldiers reach x = 1, and x = 2 is out of reach: 3 soldiers weigh < 1
    line = lambda xs: sum((s ** (2 - x) for x in xs), Q5(0))  # noqa: E731
    assert line([0, -1]) < 1 and line(range(-40, 1)) < 1


def test_row_4_play_on_the_page():
    army, moves = q0095.SOLUTIONS[4]
    boards = replay(set(army), moves)
    assert boards[-1] == {(0, 4)} and len(army) == 20
    rows = {y: sorted(x for x, yy in army if yy == y) for y in (0, -1, -2, -3)}
    assert rows == {0: list(range(-2, 5)), -1: list(range(-2, 4)), -2: list(range(-2, 3)), -3: [0, 2]}
    # the table of the 19 moves follows the play
    table = [l for l in PAGE.splitlines() if re.match(r"^\s*\| ‏\d+ \| ", l) and "שורה 3" in l]
    assert len(table) == 19
    for line, (a, b, c) in zip(table, moves):
        assert [tuple(map(int, m)) for m in re.findall(r"\((-?\d+), (-?\d+)\)", line)] == [a, b, c]


def test_page_text():
    assert "שבעה בשורה 0" in PAGE and "שישה בשורה" in PAGE and "חמישה בשורה" in PAGE
    assert "‏19 קפיצות" in PAGE
    # every Hebrew colon has a non-breaking space before it
    prose = re.sub(r"```.*?```", "", PAGE, flags=re.S)
    assert not re.search(r"[֐-׿\)\*] :", prose)


def test_explorer_matches_the_page():
    from page_tests import explorer_require, node_json

    rnd = random.Random(95)
    cases = []
    for _ in range(300):
        army = sorted({(rnd.randint(-3, 3), rnd.randint(-3, 3)) for _ in range(rnd.randint(1, 12))})
        src = rnd.choice(army)
        dst = (src[0] + rnd.choice((-2, 0, 2)), src[1] + rnd.choice((-2, 0, 2)))
        cases.append([[list(c) for c in army], list(src), list(dst)])
    got = node_json(f"const m = {explorer_require()};"
                    f"const cases = {cases};"
                    "console.log(JSON.stringify({"
                    "boards: [1, 2, 3, 4].map((n) => m.csBoards(n)),"
                    "pot: [1, 2, 3, 4, 5].map((n) => m.csPotential(m.csSolutions[Math.min(n, 4)][0], n)),"
                    "half: [1, 2, 3, 4, 5, 6].map((n) => m.csHalfPlane(n)),"
                    "jumps: cases.map(([a, s, d]) => m.csJump(a, s, d)),"
                    "}));")
    for n in (1, 2, 3, 4):
        army, moves = q0095.SOLUTIONS[n]
        want = replay(set(army), moves)
        assert [sorted(map(tuple, b)) for b in got["boards"][n - 1]] == [sorted(b) for b in want]
    for n, p in zip((1, 2, 3, 4, 5), got["pot"]):
        army = q0095.SOLUTIONS[min(n, 4)][0]
        assert abs(p - float(potential(army, n))) < 1e-12
    for n, h in zip(range(1, 7), got["half"]):
        assert abs(h - float(half_plane(n))) < 1e-9
    for (army, src, dst), res in zip(cases, got["jumps"]):
        a, s_, d = frozenset(map(tuple, army)), tuple(src), tuple(dst)
        over = ((s_[0] + d[0]) // 2, (s_[1] + d[1]) // 2)
        try:
            want = jump(a, s_, over, d) if (abs(d[0] - s_[0]) + abs(d[1] - s_[1]) == 2 and (d[0] == s_[0] or d[1] == s_[1])) else None
        except ValueError:
            want = None
        assert (None if res is None else frozenset(map(tuple, res))) == want, (army, src, dst)
