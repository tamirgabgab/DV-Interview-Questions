"""Question 0081: N queens.

The page's count_queens against a brute force over permutations for N up to 8 and the known
counts to 12, the masks of the figure, the placements of the counts table and the first
solution's 113; part b: solutions, images (the 8 symmetries, as maps of (r, c)), distinct
against a brute-force grouping, Burnside's table, the class of 4, count_half and the halves;
part c: construct for every N from 4 to 1000 (an O(N) check), the plain lists failing
exactly when N mod 6 is 2 or 3, the pair (2, 4), (5, 1) of N = 8, and no solution for 2 and
3; the traps (2113 with one diagonal, the counts of the search space); the follow-ups (the
torus, rooks and bishops); the page's numbers; the generated blocks; and the boxes' models
under Node against the Python reference."""

import itertools
import json
import math
import sys
from pathlib import Path

from extract_code import load_python

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))

import q0081  # noqa: E402

PAGE = (ROOT / "docs" / "questions" / "junior" / "0081-n-queens.md").read_text(encoding="utf-8")
ns = load_python(81)
count_queens, solutions, images, distinct, count_half, construct = (
    ns["count_queens"], ns["solutions"], ns["images"], ns["distinct"], ns["count_half"], ns["construct"])

COUNTS = [1, 0, 0, 2, 10, 4, 40, 92, 352, 724, 2680, 14200]          # N = 1 .. 12
CLASSES = [1, 0, 0, 1, 2, 1, 6, 12, 46, 92]                          # N = 1 .. 10


def safe(p) -> bool:
    """p[r] = the column of row r: a solution when no two share a column or a diagonal."""
    n = len(p)
    return len(set(p)) == n and len({p[r] - r for r in range(n)}) == n and len({p[r] + r for r in range(n)}) == n


def test_part_a_counts():
    for n in range(1, 9):
        brute = sum(1 for p in itertools.permutations(range(n)) if safe(p))
        assert count_queens(n) == brute == COUNTS[n - 1]
    for n in range(9, 13):
        assert count_queens(n) == COUNTS[n - 1]
    assert count_queens(8) == 92


def test_part_a_figure_and_table():
    cols, left, right, free = q0081.masks(8, [0, 4, 7])
    assert (cols, left, right, free) == (0b10010001, 0b01001000, 0b01000100, 0b00100010) == (145, 72, 68, 34)
    assert [c for c in range(8) if free >> c & 1] == [1, 5]
    assert q0081.solutions(8)[0][:3] == (0, 4, 7)                       # the search's first three queens
    assert q0081.placements(8) == 2056
    assert [q0081.placements(n) for n in range(4, 13)] == [16, 53, 152, 551, 2056, 8393, 35538, 166925, 856188]
    for n in range(4, 13):
        assert len(q0081.solutions(n)) == COUNTS[n - 1]
    # the lowest bit: free & -free
    for x in range(1, 1 << 10):
        assert x & -x == 1 << (len(bin(x)) - len(bin(x).rstrip("0")))
    # the placements until the first solution of 8 queens
    full, count, found = 255, [0], [False]

    def place(row, cols, left, right):
        if row == 8:
            found[0] = True
            return
        free = full & ~(cols | left | right)
        while free and not found[0]:
            bit = free & -free
            free ^= bit
            count[0] += 1
            place(row + 1, cols | bit, ((left | bit) << 1) & full, (right | bit) >> 1)
    place(0, 0, 0, 0)
    assert count[0] == 113


def test_part_b_symmetries():
    for n in range(1, 11):
        sols = list(solutions(n))
        assert sols == q0081.solutions(n) and len(sols) == COUNTS[n - 1]
        sset = set(sols)
        for p in sols:
            ims = images(p)
            assert len(ims) == 8 and set(ims) <= sset and set(ims) == set(q0081.images(p))
            # the 8 maps of (r, c), by their action on the queens
            cells = {(r, c) for r, c in enumerate(p)}
            maps = [lambda r, c: (r, c), lambda r, c: (c, n - 1 - r), lambda r, c: (n - 1 - r, n - 1 - c),
                    lambda r, c: (n - 1 - c, r), lambda r, c: (r, n - 1 - c), lambda r, c: (c, r),
                    lambda r, c: (n - 1 - r, c), lambda r, c: (n - 1 - c, n - 1 - r)]
            for q, f in zip(ims, maps):
                assert {(r, c) for r, c in enumerate(q)} == {f(r, c) for r, c in cells}
        # distinct against a grouping by brute force
        groups, seen = 0, set()
        for p in sols:
            if p not in seen:
                groups += 1
                seen |= set(images(p))
        assert distinct(n) == groups == CLASSES[n - 1]
        assert count_half(n) == count_queens(n)
    cl = q0081.classes(8)
    assert len(cl) == 12 and sorted(len(c) for c in cl) == [4] + [8] * 11 and 11 * 8 + 4 == 92
    four = next(c for c in cl if len(c) == 4)
    assert all(q0081.images(p)[2] == p for p in four)                     # a half turn keeps them
    assert q0081.burnside(8) == [92, 0, 4, 0, 0, 0, 0, 0] and sum(q0081.burnside(8)) == 96 and 96 // 8 == 12
    # no reflection keeps a solution for N > 1
    for n in range(2, 11):
        assert q0081.burnside(n)[4:] == [0, 0, 0, 0]
    assert count_queens(8, (1 << 4) - 1) == 46 and 2 * 46 == 92
    assert [count_queens(n, (1 << (n // 2)) - 1) for n in range(4, 11)] == [1, 4, 2, 17, 46, 149, 362]


def fast_safe_1(cols) -> bool:
    """construct's output (1-based columns of rows 1 .. n) is a solution, in O(n)."""
    n = len(cols)
    return (sorted(cols) == list(range(1, n + 1)) and len({c - r for r, c in enumerate(cols)}) == n
            and len({c + r for r, c in enumerate(cols)}) == n)


def test_part_c_construction():
    for n in range(4, 1001):
        cols = construct(n)
        assert cols == q0081.construct(n) and fast_safe_1(cols), n
        plain = list(range(2, n + 1, 2)) + list(range(1, n + 1, 2))
        assert fast_safe_1(plain) == (n % 6 not in (2, 3)), n
        m = n // 2
        assert ((m - 1) % 3 == 0) == (n % 6 in (2, 3))
    plain8 = [2, 4, 6, 8, 1, 3, 5, 7]
    assert plain8[1] == 4 and plain8[4] == 1 and abs(4 - 1) == 5 - 2              # (2, 4) and (5, 1)
    assert construct(8) == [2, 4, 6, 8, 3, 1, 7, 5] and construct(9) == [4, 6, 8, 2, 5, 7, 9, 1, 3]
    assert construct(10) == [2, 4, 6, 8, 10, 1, 3, 5, 7, 9]
    for n in (2, 3):
        assert not any(safe(p) for p in itertools.permutations(range(n)))


def test_traps_and_follow_ups():
    one_diagonal = sum(1 for p in itertools.permutations(range(8)) if len({p[r] - r for r in range(8)}) == 8)
    assert one_diagonal == 2113
    assert math.comb(64, 8) == 4426165368 and 8 ** 8 == 16777216 and math.factorial(8) == 40320
    # the torus: a solution exactly when gcd(n, 6) = 1; 2r mod n works then
    for n in range(1, 10):
        torus = sum(1 for p in itertools.permutations(range(n))
                    if len({(p[r] - r) % n for r in range(n)}) == n and len({(p[r] + r) % n for r in range(n)}) == n)
        assert (torus > 0) == (math.gcd(n, 6) == 1)
        if n == 5:
            assert torus == 10
        if n == 7:
            assert torus == 28
    for n in (1, 5, 7, 11, 13, 25):
        p = [2 * r % n for r in range(n)]
        assert len({(p[r] - r) % n for r in range(n)}) == n and len({(p[r] + r) % n for r in range(n)}) == n
    # bishops: at most 2n - 2 (n >= 2), by brute force on small boards
    for n in (2, 3, 4):
        cells = [(r, c) for r in range(n) for c in range(n)]
        best = 0
        for mask in range(1 << len(cells)):
            chosen = [cells[i] for i in range(len(cells)) if mask >> i & 1]
            if len(chosen) <= best:
                continue
            if len({r - c for r, c in chosen}) == len(chosen) and len({r + c for r, c in chosen}) == len(chosen):
                best = len(chosen)
        assert best == 2 * n - 2
    assert sum(1 for p in itertools.permutations(range(5))) == math.factorial(5)


def test_page_numbers():
    for s in ["2,056", "2,113", "113 הצבות", "\\( 11 \\cdot 8 + 4 = 92 \\)", "\\( 2 \\cdot 46 = 92 \\)", "96 / 8 = 12",
              "`free = 00100010`", "4.4 \\cdot 10^9", "8! = 40{,}320", "3(i - j) = m - 1", "j = m + i + 1",
              "\\( (2, 4) \\) ו-\\( (5, 1) \\)", "עד 1,000", "2,680, 14,200", "ל-5 יש 10 פתרונות כאלה ול-7 יש 28",
              'data-kind="nqueens" data-n="8"', 'data-kind="nqplace" data-n="8" data-queens="0.0_1.4_2.7"']:
        assert s in PAGE, s


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(81)


def complete(n, qs):
    """The completions of the queens qs (a list of [r, c]): (count, the first in row order)."""
    fixed = {r: c for r, c in qs}
    sols = [p for p in q0081.solutions(n) if all(p[r] == c for r, c in fixed.items())]
    sols.sort()
    return len(sols), (list(sols[0]) if sols else None)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    got = node_json(f"const m = {explorer_require()};"
                    "console.log(JSON.stringify([4, 5, 6, 7, 8].map((n) => { const s = m.nqSteps(n);"
                    " return [n, s, [0, 1, 5, 17, s.length].filter((k) => k <= s.length).map((k) => [k, m.nqQueens(s, k), m.nqMasks(n, m.nqQueens(s, k))])]; })));")
    for n, steps, samples in got:
        assert len(steps) == q0081.placements(n)
        assert steps[-1]["count"] == COUNTS[n - 1]
        # replay the steps: every complete placement is the next solution of the search
        qs, found = [], []
        for s in steps:
            qs = qs[: s["row"]] + [s["col"]]
            if s["row"] == n - 1:
                found.append(tuple(qs))
                assert s["count"] == len(found)
        assert found == q0081.solutions(n)
        for k, queens, mk in samples:
            cols, left, right, free = q0081.masks(n, queens)
            assert mk == {"cols": cols, "left": left, "right": right, "free": free}
    cases = [(8, [[0, 0], [1, 4], [2, 7]]), (8, []), (8, [[0, 0], [1, 1]]), (6, [[0, 0]]), (6, [[0, 1]]),
             (8, [[3, 3], [4, 6]]), (4, [[0, 1], [1, 3], [2, 0], [3, 2]]), (10, [[9, 9]]), (5, [[2, 2]])]
    res = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps([list(c) for c in cases])}.map(([n, q]) => [m.nqConflicts(q), [...m.nqAttacked(n, q)].sort(),"
                    " m.nqConflicts(q).length || new Set(q.map(([r]) => r)).size !== q.length ? null : m.nqComplete(n, q)])));")
    for (n, qs), (conf, attacked, done) in zip(cases, res):
        want_conf = [[i, j] for i in range(len(qs)) for j in range(i + 1, len(qs))
                     if qs[i][0] == qs[j][0] or qs[i][1] == qs[j][1] or abs(qs[i][0] - qs[j][0]) == abs(qs[i][1] - qs[j][1])]
        assert conf == want_conf
        own = {tuple(q) for q in qs}
        want_hit = sorted(f"{r},{c}" for r in range(n) for c in range(n) if (r, c) not in own and any(
            r == a or c == b or abs(r - a) == abs(c - b) for a, b in qs))
        assert attacked == want_hit
        if done is not None:
            count, first = complete(n, qs)
            assert done["count"] == count and done["first"] == first
    # the page's example: the three queens of part a can be completed (the first solution among them)
    count, first = complete(8, [[0, 0], [1, 4], [2, 7]])
    assert count >= 1 and tuple(first) == q0081.solutions(8)[0]
