"""Question 0095: the page's Python code (jump, replay, SOLUTIONS, search, Q5, weight,
potential, half_plane) runs as published.

The plays of part a are replayed; illegal jumps are refused; the backward search finds rows
1 to 3 with 2, 4 and 8 soldiers and not with fewer, and row 4 with 20 soldiers, the play the
generator and the box store; Q5 is checked against floats and against an independent
representation p + q·σ in integers; a jump never raises the potential, exactly, on random
armies and every target; the half plane weighs σ^(n − 5), exactly 1 for row 5, and every
finite part of it less than 1."""

import os
import random
import sys
from fractions import Fraction

import pytest
from extract_code import ROOT, blocks, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0095  # noqa: E402

ns = load_python(95)
jump, replay, SOLUTIONS, search = ns["jump"], ns["replay"], ns["SOLUTIONS"], ns["search"]
Q5, SIGMA, weight, potential, half_plane = ns["Q5"], ns["SIGMA"], ns["weight"], ns["potential"], ns["half_plane"]
NEED = ns["NEED"]


def test_part_a_plays():
    for n, (army, moves) in SOLUTIONS.items():
        boards = replay(army, moves)
        assert len(army) == {1: 2, 2: 4, 3: 8}[n] and len(moves) == len(army) - 1
        assert boards[-1] == {(0, n)}, n
        assert [len(b) for b in boards] == list(range(len(army), 0, -1))
        # the generator draws the same plays
        g_army, g_moves = q0095.SOLUTIONS[n]
        assert set(g_army) == army and g_moves == moves


def test_illegal_jumps():
    army = frozenset({(0, 0), (0, -1), (1, 0)})
    for bad in [((0, -1), (0, 0), (0, 2)),      # lands too far
                ((0, -1), (1, 0), (2, 1)),      # not in a row or a column
                ((1, 0), (2, 0), (3, 0)),       # nothing to jump over
                ((5, 5), (5, 6), (5, 7))]:      # no soldier to jump
        with pytest.raises(ValueError):
            jump(army, *bad)
    with pytest.raises(ValueError):
        jump(frozenset({(0, 0), (0, -1), (0, 1)}), (0, -1), (0, 0), (0, 1))     # dst taken
    with pytest.raises(ValueError):
        replay({(0, 1), (0, 0)}, [])                                            # above the line
    assert jump(army, (1, 0), (0, 0), (-1, 0)) == {(0, -1), (-1, 0)}


def test_search_rows_1_to_3():
    for n in (1, 2, 3):
        found = search(n, NEED[n])
        assert found is not None, n
        army, moves = found
        assert len(army) <= NEED[n] and (0, n) in replay(army, moves)[-1]
        assert search(n, NEED[n] - 1) is None, n          # and not with fewer


def test_search_row_4():
    army, moves = search(4, 20)
    assert len(army) == 20 and len(moves) == 19
    boards = replay(army, moves)
    assert boards[-1] == {(0, 4)}
    g_army, g_moves = q0095.SOLUTIONS[4]
    assert army == set(g_army) and moves == g_moves
    # after 12 moves: the army of row 3, one row up
    up = {(x, y + 1) for x, y in SOLUTIONS[3][0]}
    assert boards[q0095.PHASE] == up
    # the potential stays exactly 1 on every board: every jump goes straight to the target
    assert all(potential(b, 4) == 1 for b in boards)
    assert search(4, 18) is None                           # the potential alone forbids 18


def test_search_size():
    """The page says the row 4 search goes through about 150 thousand states."""
    code = next(b for b in blocks(95, "python") if "def search" in b)
    code = code.replace("seen, path = set(), []", "seen, path = set(), []\n    SEEN.append(seen)")
    space = {"DIRS": ns["DIRS"], "SEEN": []}
    exec(code, space)
    space["search"](4, 20)
    assert 140_000 < len(space["SEEN"][0]) < 160_000


@pytest.mark.skipif(not os.environ.get("DVQ_SLOW"), reason="about 8 minutes; set DVQ_SLOW=1 to run")
def test_no_army_of_19():
    """The follow-up "why not 19": the page's search with 19 soldiers and width 8 is
    exhaustive (with 19 every jump goes toward (0, 4), so no cell beyond distance 8 is ever
    used) and finds nothing, after about 7.5 million states."""
    code = next(b for b in blocks(95, "python") if "def search" in b)
    code = code.replace("seen, path = set(), []", "seen, path = set(), []\n    SEEN.append(seen)")
    space = {"DIRS": ns["DIRS"], "SEEN": []}
    exec(code, space)
    assert space["search"](4, 19, width=8) is None
    assert 7_000_000 < len(space["SEEN"][0]) < 8_000_000


def test_q5_arithmetic():
    s = SIGMA
    assert s * s + s == 1 and 1 - s == s * s
    assert abs(float(s) - (5 ** 0.5 - 1) / 2) < 1e-15
    rnd = random.Random(95)
    for _ in range(2000):
        a, b = Fraction(rnd.randint(-50, 50), rnd.randint(1, 9)), Fraction(rnd.randint(-50, 50), rnd.randint(1, 9))
        x = Q5(a, b)
        f = float(a) + float(b) * 5 ** 0.5
        assert x.sign() == (f > 0) - (f < 0)
        if x.sign():
            assert abs(float(Q5(1) / x) - 1 / f) < 1e-9 * max(1, abs(1 / f))
    # against p + q·σ in integers (the generator's own representation)
    for d in range(0, 30):
        p, q = q0095.zpow(d)
        assert s ** d == p + q * s
        assert s ** -d * s ** d == 1


def test_half_plane():
    for n in range(0, 10):
        assert half_plane(n) == SIGMA ** (n - 5)
    assert half_plane(5) == 1
    assert half_plane(4) > 1 and half_plane(4) == 1 / SIGMA        # φ
    # every finite part of the half plane weighs less than 1, and creeps up to it
    prev = Q5(0)
    for w in range(1, 11):
        part = sum((weight((x, y), 5) for x in range(-w, w + 1) for y in range(-w, 1)), Q5(0))
        assert prev < part < 1
        prev = part
    assert 1 - prev < Fraction(2, 100)


def test_a_jump_never_raises_the_potential():
    rnd = random.Random(1961)
    dirs = ((0, 1), (0, -1), (1, 0), (-1, 0))
    seen_kinds = set()
    for _ in range(3000):
        target = (rnd.randint(-3, 3), rnd.randint(-2, 6))
        n = target[1]
        army = frozenset((rnd.randint(-4, 4), rnd.randint(-4, 6)) for _ in range(rnd.randint(2, 14)))
        options = [(c, (c[0] + dx, c[1] + dy), (c[0] + 2 * dx, c[1] + 2 * dy)) for c in army for dx, dy in dirs
                   if (c[0] + dx, c[1] + dy) in army and (c[0] + 2 * dx, c[1] + 2 * dy) not in army]
        if not options:
            continue
        src, over, dst = rnd.choice(options)
        # shift so that the target is (0, n): weight measures from (0, n)
        sh = lambda c: (c[0] - target[0], c[1])  # noqa: E731
        before = potential({sh(c) for c in army}, n)
        after = potential({sh(c) for c in jump(army, src, over, dst)}, n)
        dist = lambda c: abs(c[0] - target[0]) + abs(c[1] - target[1])  # noqa: E731
        da, db, dc = dist(src), dist(over), dist(dst)
        if (da, db) == (dc + 2, dc + 1):
            assert after == before
            seen_kinds.add("toward")
        elif (db, dc) == (da + 1, da + 2):
            assert before - after == 2 * SIGMA ** (da + 1)
            seen_kinds.add("away")
        else:
            assert da == dc and db == da - 1 and before - after == SIGMA ** (da - 1)
            seen_kinds.add("across")
    assert seen_kinds == {"toward", "away", "across"}


def test_demo_runs(capsys):
    demo = (ROOT / "tests" / "0095" / "demo.py").read_text(encoding="utf-8")
    space = dict(ns)
    exec(demo.replace("from solution import *  # noqa: F401,F403", ""), space)
    out = capsys.readouterr().out
    assert "row 3" in out and "1.0" in out
