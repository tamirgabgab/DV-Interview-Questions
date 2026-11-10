"""Question 0082: Nim.

The page's nim_move, misere_move, grundy and subtraction_move are run as published against a
brute-force solution of every small position (three heaps up to 9, four heaps up to 5) under
the three rules; the theorems of the page (XOR = 0, the misère rule, the Grundy XOR and its
period 7) are checked on the same positions; every number on the page is recomputed (the
generator's tables, the traps and the follow-ups: the winning moves of 3, 5, 6, 7, the
1..k heap, Staircase Nim and Lasker's Nim); the generated blocks are checked; and the nim
box's models are compared under Node with this reference."""

import re
import sys
from functools import lru_cache, reduce
from itertools import product
from operator import xor

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0082  # noqa: E402

ns = load_python(82)
nim_move, misere_move, grundy, subtraction_move = (ns["nim_move"], ns["misere_move"], ns["grundy"],
                                                   ns["subtraction_move"])
PAGE = (ROOT / "docs" / "questions" / "senior" / "0082-nim-xor-grundy.md").read_text(encoding="utf-8")
SUB = (1, 3, 4)


def options(h, rule):
    """Every position one move away (sorted tuples: the order of the heaps does not matter)."""
    for i, x in enumerate(h):
        for t in range(x):
            if rule == "sub" and x - t not in SUB:
                continue
            yield tuple(sorted(h[:i] + (t,) + h[i + 1:]))


@lru_cache(None)
def wins(h, rule):
    """The player to move wins (h sorted)."""
    if rule == "misere" and sum(h) == 0:
        return True                                   # the opponent took the last token
    return any(not wins(o, rule) for o in options(h, rule))


def positions():
    yield from product(range(10), repeat=3)
    yield from product(range(6), repeat=4)


def check_move(fn, h, rule):
    """fn's answer on h is right: None exactly when the position is lost, otherwise a legal
    move to a lost position."""
    w = wins(tuple(sorted(h)), rule)
    m = fn(list(h))
    if not w:
        assert m is None, (fn.__name__, h, m)
        return
    assert m is not None, (fn.__name__, h)
    i, new = m
    assert 0 <= new < h[i], (fn.__name__, h, m)
    if rule == "sub":
        assert h[i] - new in SUB
    after = list(h)
    after[i] = new
    assert not wins(tuple(sorted(after)), rule), (fn.__name__, h, m)


def test_normal_nim():
    for h in positions():
        check_move(nim_move, h, "normal")
        assert wins(tuple(sorted(h)), "normal") == (reduce(xor, h, 0) != 0)


def test_misere_nim():
    for h in positions():
        if sum(h) == 0:
            continue
        check_move(misere_move, h, "misere")
        x = reduce(xor, h, 0)
        lost = (max(h) > 1 and x == 0) or (max(h) <= 1 and sum(h) % 2 == 1)
        assert wins(tuple(sorted(h)), "misere") == (not lost)
        assert q0082.misere_lost(h) == lost


def test_subtraction_game():
    g = grundy(60)
    assert g[:7] == [0, 1, 0, 1, 2, 3, 2]
    assert all(g[n] == g[n % 7] for n in range(61))
    assert g == q0082.grundy(60)
    # the period: every value depends on the four before it, and g[7..10] = g[0..3]
    assert g[7:11] == g[0:4]
    for h in positions():
        check_move(subtraction_move, h, "sub")
        assert wins(tuple(sorted(h)), "sub") == (reduce(xor, (g[v] for v in h), 0) != 0)


def test_part_numbers():
    # part a: 3 ^ 4 ^ 5 = 2, and 3 -> 1 is the only winning move
    assert 3 ^ 4 ^ 5 == 2 and q0082.nim_moves((3, 4, 5)) == [(0, 1)] and nim_move([3, 4, 5]) == (0, 1)
    assert 1 ^ 4 ^ 5 == 0 and 5 ^ 2 == 7 and 4 ^ 2 == 6
    winning = [o for o in options((3, 4, 5), "normal") if not wins(o, "normal")]
    assert winning == [(1, 4, 5)]
    # the table of examples
    assert [reduce(xor, h, 0) for h in q0082.EXAMPLES] == [2, 0, 2, 1, 2, 12]
    assert q0082.nim_moves((5, 6, 7, 8)) == [(3, 4)] and q0082.nim_moves((1, 1, 2)) == [(2, 0)]
    # the number of winning moves is the number of heaps with the top bit of the XOR
    for h in product(range(12), repeat=3):
        x = reduce(xor, h, 0)
        n = sum(1 for o in set(options(tuple(sorted(h)), "normal")) if not wins(o, "normal"))
        top = x.bit_length() - 1
        if x:
            assert len(q0082.nim_moves(h)) == sum(1 for v in h if v >> top & 1)
        assert n <= len(q0082.nim_moves(h))           # equal heaps can give the same position
    # part b: (1, 1, 4) -> 0 loses, -> 1 wins; 1, 1, 4, 6 has XOR 2 and the first wins
    assert misere_move([1, 1, 4]) == (2, 1) and nim_move([1, 1, 4]) == (2, 0)
    assert wins((0, 1, 1), "misere") and not wins((1, 1, 1), "misere")
    assert 1 ^ 1 ^ 4 ^ 6 == 2 and wins((1, 1, 4, 6), "misere")
    assert misere_move([3, 4, 5]) == (0, 1)
    # part c: 3, 4, 5 has Grundy numbers 1, 2, 3, XOR 0, and is lost; 5, 6, 7 wins
    g = grundy(20)
    assert [g[3], g[4], g[5]] == [1, 2, 3] and not wins((3, 4, 5), "sub")
    assert subtraction_move([3, 4, 5]) is None and wins((5, 6, 7), "sub")
    assert subtraction_move([5, 6, 7]) == (0, 4)
    assert [q0082.sub_moves(h)[:1] for h in q0082.SUB_EXAMPLES] == [[], [(0, 4)], [(0, 9)], []]
    # the mex: g(7) = mex{g(6), g(4), g(3)} = mex{2, 2, 1} = 0, max + 1 = 3; 7 lost
    assert [g[6], g[4], g[3]] == [2, 2, 1] and g[7] == 0 and not wins((7,), "sub")
    # going up is allowed: from 7 (g = 0) to 6 (g = 2)
    assert g[6] > g[7]
    # the trap of max + 1: on the true values {2, 2, 1} it gives 3; used for the whole table,
    # the values only rise and no heap but 0 looks lost
    assert max(g[6], g[4], g[3]) + 1 == 3
    max_plus = [0]
    for k in range(1, 15):
        max_plus.append(max(max_plus[k - m] for m in SUB if m <= k) + 1)
    assert max_plus[7] == 7 and all(v > 0 for v in max_plus[1:])


def test_follow_ups():
    # 3, 5, 6, 7: XOR 7, three winning moves
    assert 3 ^ 5 ^ 6 ^ 7 == 7 and q0082.nim_moves((3, 5, 6, 7)) == [(1, 2), (2, 1), (3, 0)] and 3 ^ 7 == 4
    # one heap, take 1..k: lost iff n is divisible by k + 1, g(n) = n mod (k + 1)
    for k in range(1, 6):
        moves = tuple(range(1, k + 1))
        assert grundy(40, moves) == [n % (k + 1) for n in range(41)]

    # Staircase Nim: coins on steps 1..4 move down one step; lost iff the XOR of steps 1, 3 is 0
    @lru_cache(None)
    def stair(c):
        for i in range(len(c)):
            for t in range(1, c[i] + 1):
                n = list(c)
                n[i] -= t
                if i:
                    n[i - 1] += t
                if not stair(tuple(n)):
                    return True
        return False
    for c in product(range(4), repeat=4):
        assert stair(c) == ((c[0] ^ c[2]) != 0)

    # Lasker's Nim: take, or split a heap into two non-empty heaps
    @lru_cache(None)
    def lasker(n):
        opts = {lasker(n - t) for t in range(1, n + 1)} | {lasker(a) ^ lasker(n - a) for a in range(1, n)}
        v = 0
        while v in opts:
            v += 1
        return v
    assert [lasker(n) for n in range(9)] == [0, 1, 2, 4, 3, 5, 6, 8, 7]
    for n in range(1, 40):
        want = {1: n, 2: n, 3: n + 1, 0: n - 1}[n % 4]
        assert lasker(n) == want


def test_page_text():
    for s in ["\\( 3 \\oplus 4 \\oplus 5 = 2 \\)", "\\( 1 \\oplus 2 \\oplus 3 = 0 \\)", "0, 1, 0, 1, 2, 3, 2",
              "\\operatorname{mex}\\{2, 2, 1\\} = 0", '<span dir="ltr">5 → 2</span>, <span dir="ltr">6 → 1</span>', 'ו-<span dir="ltr">7 → 0</span>. ל-3', "0, 1, 2, 4, 3, 5, 6, 8",
              'data-kind="nim" data-heaps="3,4,5" data-rule="normal"',
              'data-kind="nim" data-heaps="1,1,4,6" data-rule="misere"',
              'data-kind="nim" data-heaps="5,6,7" data-rule="sub"']:
        assert s in PAGE, s
    assert re.search(r"g\(5\) = \\operatorname\{mex\}\\\{2, 0, 1\\\} = 3", PAGE)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(82)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    cases = [list(h) for h in product(range(7), repeat=3)] + [list(h) for h in product(range(4), repeat=4)]
    got = node_json(f"const m = {explorer_require()};"
                    f"const cases = {cases};"
                    "console.log(JSON.stringify({"
                    "nim: cases.map(m.nimMove),"
                    "mis: cases.map((h) => (h.some((v) => v > 0) ? m.misereMove(h) : 'empty')),"
                    "sub: cases.map((h) => m.subMove(h)),"
                    "pc: ['normal', 'misere', 'sub'].map((r) => cases.filter((h) => h.some((v) => v > 0)).map((h) => m.computerMove(r, h))),"
                    "g: m.grundy(40),"
                    "game: m.nimPlay('normal', [3, 4, 5], 'me', [[0, 1], [1, 2]]),"
                    "pcfirst: m.nimPlay('sub', [3, 4, 5], 'pc', []),"
                    "misgame: m.nimPlay('misere', [1, 1, 4], 'me', [[2, 1], [1, 0]]),"
                    "bad: m.nimPlay('sub', [5], 'me', [[0, 3]]),"
                    "}));")
    tup = lambda m: None if m is None else tuple(m)  # noqa: E731
    assert [tup(m) for m in got["nim"]] == [nim_move(h) for h in cases]
    assert [m if m == "empty" else tup(m) for m in got["mis"]] == [misere_move(h) if sum(h) else "empty" for h in cases]
    assert [tup(m) for m in got["sub"]] == [subtraction_move(h) for h in cases]
    assert got["g"] == grundy(40)
    # the computer: the winning move when there is one, else one token from the largest heap
    nonempty = [h for h in cases if sum(h)]
    for rule, fn, moves in zip(["normal", "misere", "sub"], [nim_move, misere_move, subtraction_move], got["pc"]):
        for h, m in zip(nonempty, moves):
            want = fn(h)
            if want is None:
                i = h.index(max(h))
                want = (i, h[i] - 1)
            assert tuple(m) == tuple(want), (rule, h, m)
    # a game: I take 3 -> 1, the computer answers, I play on
    game = got["game"]
    assert game["moves"][0] == [0, 0, 3, 1] and game["moves"][1][0] == 1
    after = [3, 4, 5]
    for who, i, frm, to in game["moves"]:
        assert after[i] == frm and to < frm
        after[i] = to
    assert game["heaps"] == after and game["used"] == 2
    # the computer starts on a lost position: one token from the largest heap
    assert got["pcfirst"]["moves"][0] == [1, 2, 5, 4]
    # misère, (1, 1, 4): I take 4 -> 1, three ones: the computer takes one, I take one, it takes the last and loses
    mis = got["misgame"]
    assert mis["over"] and mis["winner"] == 0 and len(mis["moves"]) == 4
    # an illegal move in the subtraction game (take 2) is refused
    assert got["bad"]["bad"] and got["bad"]["moves"] == []


def test_box_tasks_and_hints():
    """The tasks of the three "try it" paragraphs, played on the box's model, and the box's
    list of every winning move and its XOR column against the brute force."""
    from page_tests import explorer_require, node_json

    cases = {r: [list(h) for h in product(range(6), repeat=3) if sum(h)] for r in ("normal", "misere", "sub")}
    got = node_json(f"const m = {explorer_require()};"
                    f"const cases = {cases};"
                    "console.log(JSON.stringify({"
                    "all: Object.fromEntries(Object.entries(cases).map(([r, hs]) => [r, hs.map((h) => m.nimWinMoves(r, h))])),"
                    "bx: cases.sub.map((h) => m.nimBoardXor('sub', h)),"
                    "t1: m.nimPlay('normal', [3, 4, 5], 'me', [[2, 2]]),"
                    "t2: m.nimPlay('normal', [1, 2, 3], 'pc', []),"
                    "t3: m.nimWinMoves('normal', [3, 5, 6, 7]),"
                    "t4: m.nimPlay('misere', [1, 1, 4], 'me', [[2, 0]]),"
                    "t5: m.nimPlay('misere', [1, 1, 4], 'me', [[2, 1]]),"
                    "t6: m.nimPlay('sub', [5, 6, 7], 'me', [[1, 5]]),"
                    "t7: m.nimWinMoves('sub', [7]),"
                    "t8: m.nimPlay('sub', [3, 4, 5], 'pc', []),"
                    "t9: m.nimWinMoves('sub', [5, 6, 7]),"
                    "}));")
    # every winning move: exactly the legal moves to a lost position
    for rule, hs in cases.items():
        for h, mv in zip(hs, got["all"][rule]):
            want = []
            for i, x in enumerate(h):
                for nw in range(x):
                    if rule == "sub" and x - nw not in SUB:
                        continue
                    after = tuple(sorted(h[:i] + [nw] + h[i + 1:]))
                    if not wins(after, rule):
                        want.append([i, nw])
            assert mv == want, (rule, h, mv, want)
    g = grundy(10)
    assert got["bx"] == [reduce(xor, (g[v] for v in h), 0) for h in cases["sub"]]
    # box 1: 5 -> 2, the computer answers 4 -> 1 and leaves 3, 1, 2 (XOR 0)
    assert got["t1"]["moves"][:2] == [[0, 2, 5, 2], [1, 1, 4, 1]] and got["t1"]["heaps"] == [3, 1, 2]
    # 1, 2, 3 with the computer first: one token from the largest, and the position wins for me
    assert got["t2"]["moves"] == [[1, 2, 3, 2]] and wins((1, 2, 2), "normal")
    # 3, 5, 6, 7: three heaps with the bit 4, three winning moves
    assert got["t3"] == [[1, 2], [2, 1], [3, 0]]
    # misère 1, 1, 4: 4 -> 0 loses (the computer takes a 1), 4 -> 1 wins
    assert got["t4"]["moves"][1][0] == 1 and wins((0, 1, 1), "misere") and not wins((1, 1, 1), "misere")
    assert got["t5"]["moves"][0] == [0, 2, 4, 1]
    # sub 5, 6, 7: 6 -> 5 raises g from 2 to 3 and leaves XOR 0
    assert (g[6], g[5]) == (2, 3) and not wins((5, 5, 7), "sub") and got["t6"]["moves"][0] == [0, 1, 6, 5]
    # a heap of 7 alone: no winning move, the moves go to 6, 4 and 3, all winning for the opponent
    assert got["t7"] == [] and all(wins((v,), "sub") for v in (6, 4, 3))
    # 3, 4, 5 with the computer first: it is lost for the computer
    assert not wins((3, 4, 5), "sub") and got["t8"]["moves"][0][0] == 1
    # every winning move of 5, 6, 7 (the box's list and the gen-8 table)
    assert got["t9"] == [[0, 4], [1, 5], [2, 3]] == [list(m) for m in q0082.sub_moves((5, 6, 7))]
    assert [list(m) for m in q0082.sub_moves((10, 11, 6))] == [[0, 9], [0, 7], [2, 5]]
