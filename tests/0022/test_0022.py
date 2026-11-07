"""Question 0022, counting the paths in a grid: the numbers the page states, recomputed from the
reference in tools/figures/q0022.py (the DP over the cells, the closed forms and a brute-force
search that never visits a cell twice); the generated blocks; the box's models under Node
against the same reference."""

import json
import random
import sys
from math import comb

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0022  # noqa: E402

E = q0022.empty
B = q0022.parse(q0022.BOARD_B)
Z = q0022.parse(q0022.ZIGZAG)


def rand_grid(rng, m, n, p=0.25):
    g = [[1 if rng.random() < p else 0 for _ in range(n)] for _ in range(m)]
    g[0][0] = g[m - 1][n - 1] = 0
    return g


def test_closed_forms_against_the_search():
    for m in range(1, 6):
        for n in range(1, 7):
            g = E(m, n)
            assert q0022.count(g) == q0022.count_walks(g, q0022.RD) == comb(m + n - 2, m - 1) == q0022.paths_rd(m, n)
            assert q0022.count(g, True) == q0022.count_walks(g, q0022.RUD) == m ** (n - 1) == q0022.paths_rud(m, n)
            # the table of part a is Pascal's triangle turned: C(r + c, r)
            assert q0022.counts(g) == [[comb(r + c, r) for c in range(n)] for r in range(m)]


def test_obstacles_against_the_search():
    rng = random.Random(22)
    for _ in range(600):
        m, n = rng.randint(1, 5), rng.randint(1, 6)
        g = rand_grid(rng, m, n, rng.choice((0.15, 0.3, 0.45)))
        assert q0022.count(g) == q0022.count_walks(g, q0022.RD), g
        assert q0022.count(g, True) == q0022.count_walks(g, q0022.RUD), g
        # every cell: the paths that end there, both kinds
        for r in range(m):
            for c in range(n):
                if g[r][c]:
                    continue
                sub = [row[:c + 1] for row in g[:r + 1]]
                assert q0022.counts(g)[r][c] == q0022.count_walks(sub, q0022.RD)
        # a blocked target has no path
        h = [row[:] for row in g]
        h[m - 1][n - 1] = 1
        assert q0022.count(h) == q0022.count(h, True) == 0


def test_part_a_numbers():
    assert q0022.paths_rd(3, 7) == 28 == comb(8, 2) == 8 * 7 // 2
    assert [q0022.arrows(p) for p in q0022.walks(E(3, 3))] == ["→→↓↓", "→↓→↓", "→↓↓→", "↓→→↓", "↓→↓→", "↓↓→→"]
    # 64 bits: square boards up to 34 x 34 fit, 35 x 35 does not
    assert comb(66, 33) < 2**64 < comb(68, 34)
    assert 7.1e18 < comb(66, 33) < 7.3e18 and 2.8e19 < comb(68, 34) < 2.9e19
    # the trap: multiplying before dividing overflows first at 33 x 33 (1.8e18 fits)
    def overflows(k):
        top, kk, r = 2 * k - 2, k - 1, 1
        for i in range(1, kk + 1):
            if r * (top - kk + i) >= 2**64:
                return True
            r = r * (top - kk + i) // i
        return False
    assert [k for k in range(2, 36) if overflows(k)] == [33, 34, 35]
    assert 1.8e18 < comb(64, 32) < 1.9e18
    # p = 10^9 + 7 is prime and larger than m + n - 2 for the boards of LeetCode
    p = 10**9 + 7
    assert all(p % d for d in range(2, int(p**0.5) + 1))


def test_part_b_numbers():
    assert q0022.BOARD_B == ["0000010", "0100000", "0001000"]
    assert {(r, c) for r in range(3) for c in range(7) if B[r][c]} == {(0, 5), (1, 1), (2, 3)}
    assert q0022.count(B) == 9 == q0022.count_walks(B, q0022.RD)
    # 19 of the 28 orders go through an obstacle
    walks = q0022.walks(E(3, 7))
    through = [w for w in walks if any(B[r][c] for r, c in w)]
    assert len(walks) == 28 and len(through) == 19


def test_part_c_numbers():
    assert q0022.paths_rud(3, 7) == 729 == 3**6
    assert len(q0022.walks(E(3, 3), q0022.RUD)) == 9
    assert q0022.paths_rud(10, 10) == 10**9 and q0022.paths_rd(10, 10) == 48620
    assert 2**29 < 10**9 < 2**30 and 16**15 > 10**18
    # the bijection: every path is its exit rows, and every list of exit rows is one path
    for m, n in ((3, 3), (2, 5), (4, 3), (3, 4)):
        rows = [tuple(q0022.exit_rows(w, n)) for w in q0022.walks(E(m, n), q0022.RUD)]
        assert len(set(rows)) == len(rows) == m ** (n - 1)
    # four directions: no formula, the search's numbers on the page
    assert [q0022.count_walks(E(k, k), q0022.ALL) for k in range(1, 6)] == [1, 2, 12, 184, 8512]
    assert q0022.count_walks(E(3, 7), q0022.ALL) == 1369


def test_part_d_numbers():
    assert q0022.count(B, True) == 32 == q0022.count_walks(B, q0022.RUD)
    assert q0022.ZIGZAG == ["0100000", "0101000", "0001000"]
    assert [r for r in range(3) if not Z[r][1]] == [2] and [r for r in range(3) if not Z[r][3]] == [0]
    assert q0022.count(Z) == 0 and q0022.count(Z, True) == 9 == 3 * 3 and q0022.count_walks(Z, q0022.ALL) == 12
    # every zigzag path goes up in column 2, from row 2 to row 0
    for w in q0022.walks(Z, q0022.RUD):
        col2 = [r for r, c in w if c == 2]
        assert col2 == [2, 1, 0]


def test_follow_ups():
    # anywhere to anywhere with up, c1 > c0: m^(c1 - c0) whatever the rows
    for m in range(1, 5):
        for n in range(2, 6):
            for r0 in range(m):
                for r1 in range(m):
                    for c0 in range(n):
                        for c1 in range(c0 + 1, n):
                            # cut the board to the columns c0..c1, move the start and the end
                            cnt = walks_between(m, n, (r0, c0), (r1, c1))
                            assert cnt == m ** (c1 - c0), (m, n, r0, c0, r1, c1)
    # inclusion-exclusion over the obstacles gives the DP's count
    rng = random.Random(5)
    for _ in range(200):
        m, n = rng.randint(2, 7), rng.randint(2, 7)
        g = rand_grid(rng, m, n, 0.2)
        obs = sorted(((r, c) for r in range(m) for c in range(n) if g[r][c]), key=lambda x: x[0] + x[1])
        pts = obs + [(m - 1, n - 1)]
        gs = []
        for i, (r, c) in enumerate(pts):
            v = comb(r + c, r)
            for j in range(i):
                a, b = pts[j]
                if a <= r and b <= c:
                    v -= gs[j] * comb(r - a + c - b, r - a)
            gs.append(v)
        assert gs[-1] == q0022.count(g)


def walks_between(m, n, s, t):
    """The paths with right, up and down from s to t that never visit a cell twice."""
    seen, total = {s}, 0

    def go(r, c):
        nonlocal total
        if (r, c) == t:
            total += 1
            return
        for dr, dc in q0022.RUD:
            a, b = r + dr, c + dc
            if 0 <= a < m and 0 <= b < n and (a, b) not in seen:
                seen.add((a, b))
                go(a, b)
                seen.remove((a, b))

    go(*s)
    return total


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(22)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(9)
    grids = [q0022.BOARD_B, q0022.ZIGZAG, ["00", "00"]]
    for _ in range(80):
        m, n = rng.randint(2, 10), rng.randint(2, 10)
        g = rand_grid(rng, m, n, rng.choice((0.1, 0.25, 0.4)))
        grids.append(["".join(map(str, row)) for row in g])
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(grids)}.map((g) => [false, true].map((up) => m.lpCounts(g, up).map((row) => row.map(String))))));")
    for g, (rd, rud) in zip(grids, got):
        p = q0022.parse(g)
        assert [[int(x) for x in row] for row in rd] == [[v if not p[r][c] else 0 for c, v in enumerate(row)] for r, row in enumerate(q0022.counts(p))]
        assert [[int(x) for x in row] for row in rud] == q0022.counts(p, True)
    forms = node_json(f"const m = {explorer_require()};"
                      "const out = []; for (let a = 2; a <= 10; a++) for (let b = 2; b <= 10; b++) out.push([String(m.lpFormula(a, b, false)), String(m.lpFormula(a, b, true))]);"
                      "console.log(JSON.stringify(out));")
    assert forms == [[str(comb(a + b - 2, a - 1)), str(a ** (b - 1))] for a in range(2, 11) for b in range(2, 11)]
    cases = ["0000010.0100000.0001000", "00.00", "0", "000.00", "100.000", "000.001", "012.000", "00.00.00.00.00.00.00.00.00.00.00", ""]
    parsed = node_json(f"const m = {explorer_require()};console.log(JSON.stringify({json.dumps(cases)}.map((t) => m.lpParse(t))));")
    assert parsed == [q0022.BOARD_B, ["00", "00"], None, None, None, None, None, None, None]
    short = node_json(f"const m = {explorer_require()};console.log(JSON.stringify([1n, 28n, 9999n, 48620n, 1000000000n, 7400000000000n].map(m.lpShort)));")
    assert short == ["1", "28", "9999", "4.8e4", "1.0e9", "7.4e12"]


def test_explorer_random_path_is_uniform():
    """The box's random path: always a valid path, and on small boards every path about as
    often as every other (a seeded generator, many draws)."""
    from page_tests import explorer_require, node_json

    boards = [(["000", "000", "000"], False), (["000", "000", "000"], True), (q0022.BOARD_B, False), (q0022.BOARD_B, True),
              (q0022.ZIGZAG, True), (["0000", "0100", "0000"], True)]
    draws = 6000
    got = node_json(f"const m = {explorer_require()};"
                    "let a = 12345; const rnd = () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);"
                    " t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };"
                    f"console.log(JSON.stringify({json.dumps(boards)}.map(([g, up]) => {{ const c = {{}};"
                    f" for (let i = 0; i < {draws}; i++) {{ const p = m.lpSample(g, up, rnd); const k = JSON.stringify(p); c[k] = (c[k] || 0) + 1; }} return c; }})));")
    for (g, up), hist in zip(boards, got):
        grid = q0022.parse(g)
        allp = {json.dumps([list(x) for x in w], separators=(",", ":")) for w in q0022.walks(grid, q0022.RUD if up else q0022.RD)}
        assert set(hist) == allp, (g, up)
        expect = draws / len(allp)
        assert all(abs(v - expect) < 5 * expect ** 0.5 + 3 for v in hist.values()), (g, up, hist)
    none = node_json(f"const m = {explorer_require()};console.log(JSON.stringify(m.lpSample({json.dumps(q0022.ZIGZAG)}, false, Math.random)));")
    assert none is None
