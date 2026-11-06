"""Question 0091: Chomp.

The page's mirror_move, eat, moves, wins, winning_moves and two_rows_move run as published.
They are checked against an independent brute force (a position as a set of squares, not
as a staircase) on every board up to 4 x 4, and against the generator's reference on every
staircase of the boards up to 6 x 7; the mirror strategy is played against every answer on
the square boards up to 7 x 7; the 2-row strategy on every position up to 2 x 9; strategy
stealing's claim (the first player wins every board but 1 x 1) on every board up to 7 x 8;
the number of staircases is C(m + n, n); every number of the page is recomputed; the
generated blocks are checked; and the chomp box's models are compared under Node."""

import re
import sys
from functools import lru_cache
from itertools import product
from math import comb

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0091  # noqa: E402

ns = load_python(91)
mirror_move, eat, moves, wins, winning_moves, two_rows_move = (
    ns["mirror_move"], ns["eat"], ns["moves"], ns["wins"], ns["winning_moves"], ns["two_rows_move"])
PAGE = (ROOT / "docs" / "questions" / "senior" / "0091-chomp.md").read_text(encoding="utf-8")


# --- an independent model: a position is the set of squares left -----------------------------

def set_moves(sq: frozenset):
    for (c, r) in sq:
        if (c, r) != (0, 0):
            yield (c, r), frozenset(s for s in sq if not (s[0] >= c and s[1] >= r))


@lru_cache(maxsize=None)
def set_wins(sq: frozenset) -> bool:
    return any(not set_wins(t) for _, t in set_moves(sq))


def to_set(h):
    return frozenset((c, r) for c, x in enumerate(h) for r in range(x))


def staircases(m, n):
    """Every non-increasing list of n heights from 0 to m."""
    def rec(prefix, top):
        if len(prefix) == n:
            yield tuple(prefix)
            return
        for x in range(top, -1, -1):
            yield from rec(prefix + [x], x)
    yield from rec([], m)


def test_against_the_set_model():
    for m in range(1, 5):
        for n in range(1, 5):
            for h in staircases(m, n):
                if h[0] == 0:
                    continue
                assert wins(h) == set_wins(to_set(h)), h
                assert to_set(eat(h, 1, 1)) <= to_set(h)
            full = (m,) * n
            want = sorted(mv for mv, t in set_moves(to_set(full)) if not set_wins(t))
            assert sorted(winning_moves(m, n)) == want, (m, n)


def test_every_staircase_against_the_reference():
    for m in range(1, 7):
        for n in range(1, 8):
            hs = list(staircases(m, n))
            assert len(hs) == comb(m + n, n)                      # the lattice paths
            for h in hs:
                if h[0]:
                    assert wins(h) == q0091.wins(h), h
                    assert sorted(mv for mv, _ in moves(h)) == sorted(mv for mv, _ in q0091.moves(h))
            assert winning_moves(m, n) == q0091.first_moves(m, n)


def test_strategy_stealing_claim():
    for m in range(1, 8):
        for n in range(1, 9):
            assert wins((m,) * n) == ((m, n) != (1, 1)), (m, n)
            # the winning first move is unique on all these boards
            assert len(winning_moves(m, n)) == (0 if (m, n) == (1, 1) else 1), (m, n)
    # the corner T is not always good: on 3 x 3 it loses, and so does it on 4 x 4
    assert wins(eat((3, 3, 3), 2, 2)) and wins(eat((4,) * 4, 3, 3))
    # the stealing step: T then X is the same position as X alone, for every X
    for m, n in [(3, 5), (4, 4), (2, 6)]:
        full = (m,) * n
        corner = eat(full, n - 1, m - 1)
        for (c, r), t in moves(corner):
            assert t == eat(full, c, r)


def test_mirror():
    for n in range(2, 8):
        assert q0091.mirror_always_wins(n)
        assert mirror_move((n,) * n) == (1, 1)
        # the L with equal arms loses, with unequal arms the mirror move evens them
        for up in range(n):
            for right in range(n):
                h = (up + 1,) + (1,) * right + (0,) * (n - 1 - right)
                mv = mirror_move(h)
                assert wins(h) == (up != right)
                if up == right:
                    assert mv is None
                else:
                    t = eat(h, *mv)
                    assert t[0] - 1 == sum(1 for x in t if x) - 1 and not wins(t)
    # the page's code is the generator's
    for n in range(2, 8):
        for h in staircases(n, n):
            if h[0] and (len(h) < 2 or h[1] <= 1):
                assert mirror_move(h) == q0091.mirror_move(h)
    # the game of part a: b2, d1, a4, b1, a2 leaves a1 alone
    h = (4,) * 4
    for who, sq in q0091.GAME_A:
        if who == "אתם":
            assert mirror_move(h) == sq
        h = eat(h, *sq)
    assert h == (1, 0, 0, 0)


def test_two_rows():
    for n in range(1, 10):
        for b in range(1, n + 1):
            for t in range(0, b + 1):
                h = (2,) * t + (1,) * (b - t) + (0,) * (n - b)
                mv = two_rows_move(b, t)
                assert (mv is not None) == wins(h), (n, b, t)
                if mv is not None:
                    after = eat(h, *mv)
                    assert not wins(after)
                    assert after[0] >= 1 and sum(1 for x in after if x >= 1) == sum(1 for x in after if x >= 2) + 1
        # the first move is the top-right square
        assert winning_moves(2, n) == [(n - 1, 1)]
    # the game of part c
    h = (2,) * 6
    for who, sq in q0091.GAME_2:
        if who == "אתם":
            b, t = sum(1 for x in h if x >= 1), sum(1 for x in h if x >= 2)
            assert two_rows_move(b, t) == sq
        h = eat(h, *sq)
    assert h == (1, 0, 0, 0, 0, 0)


def test_page_numbers():
    # part a: b2 is the only winning first move on 4 x 4; the move c3 eats four squares
    assert winning_moves(4, 4) == [(1, 1)]
    assert sum((4,) * 4) - sum(eat((4,) * 4, 2, 2)) == 4
    # part b: 12,869 positions with the poison on 8 x 8, all reached; b2 the only winning move
    assert comb(16, 8) - 1 == 12869 and q0091.reachable(8, 8) == 12869 and winning_moves(8, 8) == [(1, 1)]
    # part c: 3 x 5 -> d3; after b2 the arms are 2 and 4; 1 x n -> b1, m x 1 -> a2
    assert winning_moves(3, 5) == [(3, 2)]
    b2 = eat((3,) * 5, 1, 1)
    assert b2[0] - 1 == 2 and sum(1 for x in b2 if x) - 1 == 4
    assert all(winning_moves(1, n) == [(1, 0)] for n in range(2, 9))
    assert all(winning_moves(m, 1) == [(0, 1)] for m in range(2, 8))
    # the states: 10 x 10 and 20 x 20
    assert comb(20, 10) == 184756 and comb(40, 20) > 10 ** 11
    # 72 = 2^3 * 3^2: 3 rows (powers of 3) x 4 columns (powers of 2), c2 = 2^2 * 3 = 12
    assert winning_moves(3, 4) == [(2, 1)] and 2 ** 2 * 3 ** 1 == 12
    # the trap of the reversed end: with "the empty table loses" and a1 a normal move, the
    # results flip on every board but 1 x 1
    @lru_cache(None)
    def wrong(h):
        return any(not wrong(eat(h, c, r)) for c, x in enumerate(h) for r in range(x))
    assert not wrong((0, 0)) and wrong((1, 0))                    # a1 alone "wins": eat it
    assert all(wrong((m,) * n) for m in range(1, 5) for n in range(1, 5))   # it says even 1 x 1 wins
    for s in ["12,869", "184,756", "\\binom{16}{8} - 1 = 12{,}869", 'data-kind="chomp" data-mode="mirror" data-n="4"',
              'data-kind="chomp" data-mode="play" data-m="8" data-n="8"', 'data-kind="chomp" data-mode="play" data-m="3" data-n="5"',
              "המהלך המנצח היחיד הוא d3"]:
        assert s in PAGE, s


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(91)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    cases = [list(h) for m in range(1, 5) for n in range(1, 6) for h in staircases(m, n) if h[0]]
    squares = [[m, n] for m in range(1, 8) for n in range(2, 8)] + [[2, 1], [3, 1]]
    got = node_json(f"const m = {explorer_require()};"
                    f"const cases = {cases};"
                    f"const sizes = {squares};"
                    "console.log(JSON.stringify({"
                    "wins: cases.map((h) => m.chompWins(h)),"
                    "moves: cases.map((h) => m.chompWinningMoves(h)),"
                    "pc: cases.map((h) => m.chompComputerMove(h)),"
                    "mir: cases.map((h) => m.chompMirrorMove(h)),"
                    "first: sizes.map(([a, b]) => m.chompWinningMoves(new Array(b).fill(a))),"
                    "game: m.chompPlay('play', 4, 4, 'me', [[1, 1], [0, 3]]),"
                    "pcfirst: m.chompPlay('play', 3, 5, 'pc', []),"
                    "mirror: m.chompPlay('mirror', 4, 4, 'me', [[3, 0], [1, 0]]),"
                    "poison: m.chompPlay('play', 3, 3, 'me', [[0, 0]]),"
                    "bad: m.chompPlay('play', 3, 3, 'me', [[5, 5]]),"
                    "}));")
    tup = lambda v: None if v is None else tuple(v)  # noqa: E731
    for h, w, mv, pc, mir in zip(cases, got["wins"], got["moves"], got["pc"], got["mir"]):
        t = tuple(h)
        assert w == wins(t), h
        assert [tuple(x) for x in mv] == [x for x, after in moves(t) if not wins(after)], h
        if t == (1,) + (0,) * (len(t) - 1):
            assert tuple(pc) == (0, 0)
        elif wins(t):
            assert not wins(eat(t, *pc))                           # the computer plays to win
        else:                                                      # it eats the fewest squares
            least = min(sum(t) - sum(a) for _, a in moves(t))
            assert sum(t) - sum(eat(t, *pc)) == least
        assert tup(mir) == mirror_move(t), h
    assert [[tuple(x) for x in f] for f in got["first"]] == [winning_moves(a, b) for a, b in squares]
    # I play b2 on 4 x 4, the computer answers, I mirror: the game goes on, the moves legal
    g = got["game"]
    assert g["moves"][0]["c"] == 1 and g["moves"][0]["r"] == 1 and g["moves"][1]["who"] == 1 and g["used"] == 2
    # the computer starts on 3 x 5 with d3
    assert (got["pcfirst"]["moves"][0]["c"], got["pcfirst"]["moves"][0]["r"]) == (3, 2)
    # the mirror box: the computer opens b2, then mirrors d1 with a4 and b1 with a2; I face a1
    mi = got["mirror"]
    assert [(x["who"], x["c"], x["r"]) for x in mi["moves"]] == [(1, 1, 1), (0, 3, 0), (1, 0, 3), (0, 1, 0), (1, 0, 1)]
    assert mi["over"] and mi["loser"] == 0
    # eating a1 ends the game at once; an illegal square is refused
    assert got["poison"]["over"] and got["poison"]["loser"] == 0
    assert got["bad"]["bad"] and got["bad"]["moves"] == []


def test_page_text_ltr():
    # every square named in prose is a single Latin token; the tables start their cells with RLM
    for line in PAGE.splitlines():
        if line.startswith("| ‏") and "×" in line:
            assert re.match(r"\| ‏\d+ × \d+ \|", line)
