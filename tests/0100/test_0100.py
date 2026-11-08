"""Question 0100, the ways to climb the stairs: the numbers the page states, recomputed from the
reference in tools/figures/q0100.py (every climb listed as the stairs it lands on, every
multiset of jumps, math.comb); the generated blocks; the box's models under Node against the
same reference."""

import json
import random
import sys
from math import comb

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0100  # noqa: E402

SETS = [(1, 2), (1, 2, 3), (1, 3, 5), (2, 3), (1, 2, 3, 4, 5, 6), (3,), (2, 5), (1, 4, 6)]


def test_table_against_the_listing():
    for steps in SETS:
        for n in range(0, 15):
            assert q0100.table(n, steps)[n] == q0100.ways(n, steps), (steps, n)
    rng = random.Random(100)
    for _ in range(300):
        steps = tuple(sorted(rng.sample(range(1, 7), rng.randint(1, 4))))
        n = rng.randint(1, 14)
        broken = tuple(b for b in range(1, n + 1) if rng.random() < 0.2)
        assert q0100.table(n, steps, broken)[n] == q0100.ways(n, steps, broken), (steps, n, broken)


def test_part_a_numbers():
    assert q0100.table(10, (1, 2)) == [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
    fib = [0, 1]
    for _ in range(100):
        fib.append(fib[-1] + fib[-2])
    assert all(q0100.table(40, (1, 2))[n] == fib[n + 1] for n in range(41))
    assert q0100.ways(10, (1, 2, 3)) == 274 and q0100.ways(10, (1, 3, 5)) == 47
    # the growth and the 64-bit limit of the trap: F(93) fits, F(94) does not; n = 92
    assert fib[93] < 2**64 < fib[94] and 1.2e19 < fib[93] < 1.3e19
    assert 1.6 < fib[51] / fib[50] < 1.62 and 2 * fib[51] - 1 > 10**10


def test_part_b_numbers():
    assert q0100.table(10, (1, 2), (5,)) == [1, 1, 2, 3, 5, 0, 5, 5, 10, 15, 25]
    assert q0100.ways(10, (1, 2), (5,)) == 25 == 5 * 5
    assert q0100.ways(10, (1, 2), (5, 6)) == 0
    # one broken stair b with {1, 2}: w(b - 1) times the climbs of the n - b - 1 stairs after it
    for n in range(3, 16):
        for b in range(1, n):
            assert q0100.ways(n, (1, 2), (b,)) == q0100.ways(b - 1, (1, 2)) * q0100.ways(n - b - 1, (1, 2))
    assert q0100.ways(10, (1, 2), (10,)) == 0
    # two adjacent broken stairs block only {1, 2}: {1, 3} jumps from 4 to 7; a run of max S blocks
    assert q0100.table(10, (1, 3), (5, 6)) == [1, 1, 1, 2, 3, 0, 0, 3, 3, 3, 6]
    assert q0100.ways(10, (1, 3), (5, 6, 7)) == 0
    for steps in SETS:
        for b in range(1, 8):
            assert q0100.ways(14, steps, tuple(range(b, b + max(steps)))) == 0, (steps, b)
    # the box's first trap: S = {2, 3}, stair 1 has no way, 7 ways to stair 10 from 8 and 7
    assert q0100.table(10, (2, 3)) == [1, 0, 1, 1, 1, 2, 2, 3, 4, 5, 7]


# the page's cycle table of stairs_ways (stair 5 broken); tests/0100/tb.sv has the same rows
CYCLES = {"b1": [0, 1, 1, 2, 3, 5, 0, 5, 5, 10, 15, 25], "b2": [0, 0, 1, 1, 2, 3, 5, 0, 5, 5, 10, 15],
          "sum": [0, 1, 2, 3, 5, 8, 5, 5, 10, 15, 25, 40], "ways": [0, 1, 1, 2, 3, 5, 0, 5, 5, 10, 15, 25]}


def test_module_trace():
    rows = q0100.module_trace(10, (1, 2), (5,))
    for key, want in CYCLES.items():
        assert [r[key] for r in rows] == want, key
    # ways is a register: in the cycle of stair i it still holds stair i - 1, then w(i)
    rng = random.Random(3)
    for _ in range(100):
        steps = tuple(sorted(rng.sample(range(1, 7), rng.randint(1, 4))))
        n = rng.randint(1, 14)
        broken = tuple(b for b in range(1, n + 1) if rng.random() < 0.2)
        w, rows = q0100.table(n, steps, broken), q0100.module_trace(n, steps, broken)
        assert [r["ways"] for r in rows[1:]] == w and rows[-1]["ways"] == q0100.ways(n, steps, broken)


def test_part_c_numbers():
    assert len(q0100.multisets(10, (1, 2))) == 6 and len(q0100.multisets(10, (1, 2, 3))) == 14
    assert q0100.unordered_rows(10, (1, 2, 3))[-1][10] == 14
    for steps in SETS:
        for n in range(0, 16):
            assert q0100.unordered_rows(n, steps)[-1][n] == len(q0100.multisets(n, steps))
            # every multiset has exactly one non-decreasing order
            sorted_climbs = [c for c in q0100.climbs(n, steps) if list(c) == sorted(c)]
            assert len(sorted_climbs) == len(q0100.multisets(n, steps))
    # with {1, 2}: k twos, C(10 - k, k) orders each, 89 in all
    assert sum(comb(10 - k, k) for k in range(6)) == 89
    assert q0100.unordered_rows(6, (1, 2, 3)) == [[1] * 7, [1, 1, 2, 2, 3, 3, 4], [1, 1, 2, 3, 4, 5, 7]]
    assert q0100.table(6, (1, 2, 3))[6] == 24
    # the follow-up: coins 1, 2, 5 for 10
    assert len(q0100.multisets(10, (1, 2, 5))) == 10 and q0100.ways(10, (1, 2, 5)) == 128


def test_part_d_numbers():
    assert q0100.exact(10, (1, 2), 7) == 35 == comb(7, 3)
    for n in range(0, 15):
        for t in range(0, 16):
            assert q0100.exact(n, (1, 2), t) == (comb(t, n - t) if 0 <= n - t <= t else 0)
    assert [q0100.exact(10, (1, 2), t) for t in range(5, 11)] == [1, 15, 35, 28, 9, 1]
    for steps in SETS:
        for n in range(0, 13):
            rows = q0100.exact_table(n, steps, n)
            assert all(rows[t][n] == q0100.exact(n, steps, t) for t in range(n + 1))
            assert sum(rows[t][n] for t in range(n + 1)) == q0100.ways(n, steps)
    # the table of the page: row t, column i is C(t, i - t); the columns sum to part a's table
    rows = q0100.exact_table(10, (1, 2), 10)
    assert all(rows[t][i] == (comb(t, i - t) if 0 <= i - t <= t else 0) for t in range(11) for i in range(11))
    assert [sum(r[i] for r in rows) for i in range(11)] == q0100.table(10, (1, 2))
    assert [rows[t][6] for t in range(3, 7)] == [1, 6, 5, 1] and rows[7][10] == 35


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(100)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(7)
    cases = []
    for _ in range(150):
        steps = sorted(rng.sample(range(1, 7), rng.randint(1, 4)))
        n = rng.randint(1, 30)
        broken = [b for b in range(1, n + 1) if rng.random() < 0.15]
        cases.append([n, steps, broken])
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(cases)}.map(([n, s, b]) => [m.swTable(n, s, b).map(String), String(m.swMultisets(n, s))])));")
    for (n, steps, broken), (tab, multi) in zip(cases, got):
        assert [int(x) for x in tab] == q0100.table(n, steps, broken)
        assert int(multi) == q0100.unordered_rows(n, steps)[-1][n]
    parsed = node_json(f"const m = {explorer_require()};"
                       "console.log(JSON.stringify(['1.2', '2.1', '1.2.3.4.5.6', '7', '1.1', '', '0.2', '3'].map(m.swSteps)));")
    assert parsed == [[1, 2], [1, 2], [1, 2, 3, 4, 5, 6], None, None, None, None, [3]]
    traps = node_json(f"const m = {explorer_require()};console.log(JSON.stringify(m.swTraps));")
    assert set(traps) == {"s23", "b56", "s13"}
    got = {k: q0100.table(t["n"], tuple(t["steps"]), tuple(t["broken"])) for k, t in traps.items()}
    assert got["s23"][1] == 0 and got["s23"][10] == 7 and traps["s23"]["pick"] == 1
    assert got["b56"][7:] == [0, 0, 0, 0] and traps["b56"]["pick"] == 7
    assert got["s13"][7] == 3 and got["s13"][10] == 6 and traps["s13"]["pick"] == 7
    short = node_json(f"const m = {explorer_require()};console.log(JSON.stringify([1n, 89n, 99999n, 832040n, 1346269n].map(m.swShort)));")
    assert short == ["1", "89", "99999", "8.3e5", "1.3e6"]
