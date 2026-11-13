"""Question 0108, flips of k consecutive bits: the numbers the page states, recomputed from the
references of tools/figures/q0108.py (every set of starts by brute force, the forced scan with
the covering windows counted one by one): the examples, the uniqueness that makes "the fewest" a
red herring, the trace of the open windows, the grid example and its corners, the traps, the
follow-ups (rectangles, the ring by brute force, the streaming form, how many arrays can be
fixed), the try-it paragraphs, the generated blocks, and the boxes' models under Node."""

import json
import math
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0108  # noqa: E402
from q0108 import EXAMPLE, GRID, GRID_BAD, LONG, LONG_BAD  # noqa: E402

ns = load_python(108)


def test_statement_examples():
    assert q0108.brute(EXAMPLE, 3) == [(0, 4, 5)]
    assert q0108.brute([0, 1, 0], 1) == [(0, 2)] and q0108.brute([1, 1, 0], 2) == []
    assert q0108.answer(EXAMPLE, 3) == 3 and q0108.answer([0, 1, 0], 1) == 2 and q0108.answer([1, 1, 0], 2) == -1


def test_order_and_twice():
    # a set of starts in any order gives the same array; a window twice cancels
    rng = random.Random(1)
    for _ in range(300):
        n, k = rng.randint(1, 14), rng.randint(1, 5)
        if k > n:
            continue
        a = [rng.randint(0, 1) for _ in range(n)]
        starts = [rng.randint(0, n - k) for _ in range(rng.randint(0, 8))]
        rng.shuffle(starts)
        assert q0108.apply(a, k, starts) == q0108.apply(a, k, sorted(set(p for p in starts if starts.count(p) % 2)))


def test_forced_and_unique():
    # at most one solution for every array; the scan finds it; 2^(n-k+1) fixable arrays of 2^n
    for n in range(1, 12):
        for k in range(1, n + 1):
            t = q0108.table(n, k)
            assert all(len(v) == 1 for v in t.values())
            assert len(t) == 2 ** (n - k + 1)
            for m, (sol,) in list(t.items())[:200]:
                a = [m >> j & 1 for j in range(n)]
                assert q0108.scan(a, k) == list(sol)
    # the forcing figure: bit 4 of the example is covered by the windows 2, 3 and 4; bits 6 and 7 by none that starts there
    assert q0108.covers(4, 8, 3) == [2, 3, 4] and q0108.covers(0, 8, 3) == [0] and q0108.covers(1, 8, 3) == [0, 1]
    assert q0108.covers(6, 8, 3) == [4, 5] and q0108.covers(7, 8, 3) == [5]
    # n = 8, k = 3: 64 of 256, a random array fixable with probability 2^-(k-1)
    assert len(q0108.table(8, 3)) == 64 and 64 / 256 == 2 ** -(3 - 1)


def test_scan_table_and_trace():
    ev = q0108.events(EXAMPLE, 3)
    assert [e["act"] for e in ev] == ["start", "skip", "skip", "skip", "start", "start", "check", "check"]
    assert [e["open"] for e in ev] == [[], [0], [0], [], [], [4], [4, 5], [5]]
    assert [e["par"] for e in ev] == [0, 1, 1, 0, 0, 1, 0, 1]
    assert [e["now"] for e in ev] == [0, 1, 1, 1, 0, 0, 1, 1]
    # the rows of the scan: 11110110, 11111000, 11111111
    cur = list(EXAMPLE)
    rows = []
    for p in (0, 4, 5):
        cur = q0108.apply(cur, 3, [p])
        rows.append("".join(map(str, cur)))
    assert rows == ["11110110", "11111000", "11111111"]
    # 110 with k = 2: no window opens, bit 2 is left 0
    ev = q0108.events([1, 1, 0], 2)
    assert [e["act"] for e in ev] == ["skip", "skip", "fail"]
    # the queue holds at most k windows; in place the original bit stays in the low bit
    rng = random.Random(2)
    for _ in range(500):
        n, k = rng.randint(1, 30), rng.randint(1, 8)
        a = [rng.randint(0, 1) for _ in range(n)]
        assert all(len(e["open"]) <= k - 1 for e in q0108.events(a, k))


def test_truncated_window_trap():
    # flipping "what is left of the window" at the end fixes every array: 110 with k = 2 gives 1, not -1
    def truncated(a, k):
        a, flips = list(a), 0
        for i in range(len(a)):
            if a[i] == 0:
                for j in range(i, min(i + k, len(a))):
                    a[j] ^= 1
                flips += 1
        return flips
    assert truncated([1, 1, 0], 2) == 1 and q0108.answer([1, 1, 0], 2) == -1
    rng = random.Random(4)
    for _ in range(300):
        n, k = rng.randint(1, 12), rng.randint(1, 5)
        a = [rng.randint(0, 1) for _ in range(n)]
        if q0108.answer(a, k) != -1:
            assert truncated(a, k) == q0108.answer(a, k)


def test_naive_worst_case():
    # every window chosen: (n - k + 1) k flips of a bit; n = 10^5, k = n / 2: about 2.5 10^9
    for n, k in ((8, 3), (12, 6), (20, 4)):
        a = q0108.apply([1] * n, k, range(n - k + 1))
        assert q0108.scan(a, k) == list(range(n - k + 1))
    n = 10 ** 5
    k = n // 2
    assert (n - k + 1) * k == 2_500_050_000
    assert 2 ** 40 > 10 ** 12


def test_part_b():
    assert q0108.brute2(GRID, 2) == [q0108.GRID_STARTS] == [q0108.scan2(GRID, 2)]
    assert q0108.brute2(GRID_BAD, 2) == [] and q0108.answer2(GRID_BAD, 2) == -1
    # the corner flipped is the last cell; the scan picks the same squares; without the check: 4
    assert [(r, c) for r in range(4) for c in range(5) if GRID[r][c] != GRID_BAD[r][c]] == [(3, 4)]
    ev = q0108.events2(GRID_BAD, 2)
    assert len(ev) == 20 and ev[-1]["act"] == "fail" and (ev[-1]["r"], ev[-1]["c"]) == (3, 4)
    assert [(e["r"], e["c"]) for e in ev if e["act"] == "start"] == q0108.GRID_STARTS
    def no_check(g, k):
        R, C, chosen = len(g), len(g[0]), []
        for r in range(R - k + 1):
            for c in range(C - k + 1):
                over = sum(1 for (pr, pc) in chosen if pr <= r < pr + k and pc <= c < pc + k)
                if (g[r][c] ^ over % 2) == 0:
                    chosen.append((r, c))
        return len(chosen)
    assert no_check(GRID_BAD, 2) == 4
    # unique for every grid up to 3 x 4 and every k; 2^((R-k+1)(C-k+1)) fixable grids, 1 in 256 for 4 x 5, k = 2
    for R in range(1, 4):
        for C in range(1, 5):
            for k in range(1, min(R, C) + 1):
                t = q0108.table2(R, C, k)
                assert len(t) == 2 ** ((R - k + 1) * (C - k + 1)) and all(len(v) == 1 for v in t.values())
    assert 2 ** 20 // 2 ** ((4 - 2 + 1) * (5 - 2 + 1)) == 256
    # the corners: the prefix XOR of the four corners is 1 exactly on the square
    r0, c0 = q0108.CORNER
    for R, C, k in ((4, 5, 2), (6, 7, 3)):
        for r0 in range(R - k + 1):
            for c0 in range(C - k + 1):
                d = [[0] * (C + 1) for _ in range(R + 1)]
                for rr, cc in ((r0, c0), (r0, c0 + k), (r0 + k, c0), (r0 + k, c0 + k)):
                    d[rr][cc] ^= 1
                for r in range(R):
                    for c in range(C):
                        x = 0
                        for i in range(r + 1):
                            for j in range(c + 1):
                                x ^= d[i][j]
                        assert x == (r0 <= r < r0 + k and c0 <= c < c0 + k)


def test_try_it():
    ev = q0108.events(EXAMPLE, 3)
    # six steps: a window at bit 0, none at 1 to 3, bit 4 is 0 with no window open, bit 5 a 1 under the window of 4
    assert [e["act"] for e in ev[:6]] == ["start", "skip", "skip", "skip", "start", "start"]
    assert ev[4]["open"] == [] and ev[4]["now"] == 0 and ev[5]["a"] == 1 and ev[5]["open"] == [4]
    assert q0108.answer([1, 1, 0], 2) == -1 and q0108.events([1, 1, 0], 2)[-1]["i"] == 2
    assert q0108.answer(*LONG) == 7 and q0108.answer(*LONG_BAD) == -1 and len(LONG[0]) == 20
    assert q0108.events(*LONG_BAD)[-1]["i"] == 19
    ev2 = q0108.events2(GRID, 2)
    assert ev2[1]["act"] == "start" and (ev2[1]["r"], ev2[1]["c"]) == (0, 1)
    d, p = q0108.dp_after(GRID, 2, 2)
    assert sum(map(sum, d)) == 3
    assert len(ev2) == 20 and sum(e["act"] == "start" for e in ev2) == 4
    assert all(e["act"] == "check" for e in ev2 if e["r"] == 3 or e["c"] == 4)


def test_followups():
    rng = random.Random(3)
    # rectangles a x b: forced at the top left, unique, the same scan
    for _ in range(300):
        R, C = rng.randint(1, 4), rng.randint(1, 4)
        a, b = rng.randint(1, R), rng.randint(1, C)
        g = [[rng.randint(0, 1) for _ in range(C)] for _ in range(R)]
        sols = q0108.brute2(g, a, b)
        assert len(sols) <= 1
        assert (q0108.scan2(g, a, b) is None) == (not sols)
        if sols:
            assert sorted(sols[0]) == sorted(q0108.scan2(g, a, b))
    # the ring: 2^g or 2^(g-1) solutions, the fewest by the cheaper side of every cycle (n <= 9, every array)
    for n in range(1, 9):
        for k in range(1, n + 1):
            g = math.gcd(n, k)
            for m in range(1 << n):
                a = [m >> j & 1 for j in range(n)]
                sols = q0108.ring_brute(a, k)
                count, best = q0108.ring_solve(a, k)
                assert count == len(sols)
                if sols:
                    assert count == (2 ** g if (k // g) % 2 == 0 else 2 ** (g - 1))
                    assert best == min(map(len, sols)) == q0108.ring_min_by_switch(a, k)
                    # the differences of the page: x_p ^ x_(p-k) = a_p ^ a_(p-1)
                    x = [int(p in sols[0]) for p in range(n)]
                    assert all(x[p] ^ x[(p - k) % n] == a[p] ^ a[p - 1] for p in range(n))
    # the ring has an array with two solutions of different sizes: the fewest matters again there
    assert any(len(set(map(len, q0108.ring_brute([m >> j & 1 for j in range(6)], 2)))) > 1 for m in range(64))
    # streaming: a shift register of the last k - 1 decisions, the parity its XOR (or one flop)
    for _ in range(2000):
        n, k = rng.randint(1, 30), rng.randint(1, 8)
        a = [rng.randint(0, 1) for _ in range(n)]
        reg, flop, count, bad = [0] * max(k - 1, 0), 0, 0, False
        for i, bit in enumerate(a):
            parity = sum(reg) % 2
            assert parity == flop
            dec = 1 - (bit ^ parity)
            if dec and i > n - k:                  # a 0 in the last k - 1 bits
                bad, dec = True, 0
            count += dec
            out = reg[0] if reg else dec
            reg = (reg[1:] + [dec]) if reg else []
            flop ^= dec ^ out if k > 1 else 0
        assert (-1 if bad else count) == ns["min_flips"](a, k)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(108)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(108)
    rows = [(EXAMPLE, 3), ([0, 1, 0], 1), ([1, 1, 0], 2), LONG, LONG_BAD, ([1, 1, 1], 4)]
    for _ in range(300):
        n = rng.randint(1, 20)
        rows.append(([rng.randint(0, 1) for _ in range(n)], rng.randint(1, 8)))
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(rows)}.map(([a, k]) => m.kfScan(a, k))));")
    for (a, k), ev in zip(rows, got):
        assert ev == q0108.events(a, k), (a, k)
    grids = [(GRID, 2), (GRID_BAD, 2), ([[0]], 1), ([[1, 0]], 3)]
    for _ in range(150):
        R, C = rng.randint(1, 8), rng.randint(1, 8)
        grids.append(([[rng.randint(0, 1) for _ in range(C)] for _ in range(R)], rng.randint(1, 5)))
    for _ in range(100):                            # fixable ones, so the scan runs to the end
        R, C = rng.randint(2, 8), rng.randint(2, 8)
        k = rng.randint(1, min(R, C, 5))
        starts = [(r, c) for r in range(R - k + 1) for c in range(C - k + 1) if rng.random() < 0.35]
        grids.append((q0108.cover2([[1] * C for _ in range(R)], k, k, starts), k))
    steps = [rng.randint(0, len(g) * len(g[0])) for g, _ in grids]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(grids)}.map(([g, k], i) => [m.kf2Scan(g, k), m.kf2State(g, k, {json.dumps(steps)}[i])])));")
    for (g, k), s, (ev, state) in zip(grids, steps, got):
        assert ev == q0108.events2(g, k), (g, k)
        d, p = q0108.dp_after(g, k, s)
        assert state["d"] == d and state["p"] == p, (g, k, s)
        # the page's code holds the same d and p: its answer agrees with the scan
        assert ns["min_flips_2d"](g, k) == q0108.answer2(g, k)
    presets = node_json(f"const m = {explorer_require()};console.log(JSON.stringify([m.kfPresets, m.kf2Presets]));")
    assert [(p[1], p[2]) for p in presets[0]] == [(EXAMPLE, 3), ([0, 1, 0], 1), ([1, 1, 0], 2), tuple(LONG), tuple(LONG_BAD)]
    assert [q0108.answer(p[1], p[2]) for p in presets[0]] == [3, 2, -1, 7, -1]
    assert (presets[1][0][1], presets[1][0][2]) == (GRID, 2) and (presets[1][1][1], presets[1][1][2]) == (GRID_BAD, 2)
    assert [q0108.answer2(p[1], p[2]) for p in presets[1]] == [4, -1, 6, 19]
    parsed = node_json(f"const m = {explorer_require()};"
                       "console.log(JSON.stringify([['00010110', '0001 0110', '0,1', '012', '', '1'.repeat(20), '1'.repeat(21)].map(m.kfParse),"
                       " ['10011.10101', '10 01', '1/0', '10.1', '2', '', '1'.repeat(8), '1'.repeat(9), Array(9).fill('1').join('.')].map(m.kf2Parse)]));")
    assert parsed[0] == [EXAMPLE, EXAMPLE, [0, 1], None, None, [1] * 20, None]
    assert parsed[1] == [[[1, 0, 0, 1, 1], [1, 0, 1, 0, 1]], [[1, 0], [0, 1]], [[1], [0]], None, None, None, [[1] * 8], None, None]
