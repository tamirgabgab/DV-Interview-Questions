"""Question 0045: the page's three Python solvers against a hidden odd ball (every ball,
heavy and light; part a and b on 12 balls in at most 3 weighings, part c for every n from
3 to 364 in exactly the fewest weighings, equal pans in every weighing), the numbers the
page states (the table of k and N, the formula ceil(log3(2N + 3)), the codes of part b, the
unused vectors, the 13-ball argument), and the explorer's JavaScript: the same codes and
pans as the page's code, and a decision table that names every scenario."""

import json
import math
from itertools import product

import pytest

from extract_code import load_python
from page_tests import explorer_require, node_json

ns = load_python(45)
tree, fixed, general = ns["find_odd_ball_12_tree"], ns["find_odd_ball_12"], ns["find_odd_ball"]
CODES = ns["CODES"]


def make_scale(n, odd, heavy, log=None):
    w = {b: 10 for b in range(1, n + 1)}
    if odd:
        w[odd] = 11 if heavy else 9
    calls = [0]

    def weigh(left, right):
        calls[0] += 1
        assert len(set(left) | set(right)) == len(left) + len(right), "ball used twice"
        assert all(1 <= b <= n for b in left + right)
        assert len(left) == len(right), (n, odd, left, right)
        if log is not None:
            log.append((list(left), list(right)))
        lw, rw = sum(w[b] for b in left), sum(w[b] for b in right)
        return "left" if lw > rw else "right" if rw > lw else "equal"
    return weigh, calls


def fewest(n):
    k = 0
    while 3 ** k < 2 * n + 3:
        k += 1
    return k


def run(solver, n, odd, heavy):
    weigh, calls = make_scale(n, odd, heavy)
    return solver(weigh), calls[0]


@pytest.mark.parametrize("solver", [tree, fixed])
def test_parts_a_and_b(solver):
    for odd in range(1, 13):
        for heavy in (True, False):
            got, calls = run(solver, 12, odd, heavy)
            assert got == (odd, "heavy" if heavy else "light") and calls <= 3


def test_part_c_every_n():
    for n in range(3, 365):
        worst = 0
        for odd in range(1, n + 1):
            for heavy in (True, False):
                got, calls = run(lambda w: general(n, w), n, odd, heavy)
                assert got == (odd, "heavy" if heavy else "light"), (n, odd, heavy)
                worst = max(worst, calls)
        assert worst == fewest(n), n


def test_page_numbers():
    assert [(k, (3 ** k - 3) // 2) for k in range(2, 7)] == [(2, 3), (3, 12), (4, 39), (5, 120), (6, 363)]
    for n in range(3, 2000):            # k = ceil(log3(2N + 3)) is the smallest k with (3^k - 3)/2 >= N
        k = fewest(n)
        assert (3 ** k - 3) // 2 >= n > (3 ** (k - 1) - 3) // 2
        if 2 * n + 3 != 3 ** k:
            assert k == math.ceil(math.log(2 * n + 3, 3))
    assert math.ceil(math.log(26, 3)) == 3 and fewest(13) == 4      # the trap: ceil(log3(2N)) for N = 13
    assert 12 * 2 == 24 and 3 ** 3 == 27 and 3 ** 2 < 24
    # part b: 12 distinct codes, none zero, no code with its negation, 4 against 4 every time
    codes = list(CODES.values())
    assert len(set(codes)) == 12 and (0, 0, 0) not in codes
    assert all(tuple(-x for x in c) not in codes for c in codes)
    for j in range(3):
        assert sum(c[j] == 1 for c in codes) == sum(c[j] == -1 for c in codes) == 4
    assert [b for b, c in CODES.items() if c[1] == 1] == [1, 4, 8, 9]
    assert [b for b, c in CODES.items() if c[1] == -1] == [3, 6, 10, 11]
    nonzero = [c for c in product((-1, 0, 1), repeat=3) if any(c)]
    unused = [c for c in nonzero if c not in codes and tuple(-x for x in c) not in codes]
    assert sorted(unused) == [(-1, 1, -1), (1, -1, 1)]
    assert len(nonzero) == 26 and sum(c[0] != 0 for c in nonzero) // 2 == 9        # 13 balls: 9 per column, odd
    # the follow-ups: known heavy, 3^k balls; with a genuine ball, (3^k - 1) / 2 (13 for 3)
    assert 3 ** 3 == 27 and (3 ** 3 - 1) // 2 == 13


def recorded(n, odd, heavy):
    log = []
    weigh, _ = make_scale(n, odd, heavy, log)
    (fixed if n == 12 else (lambda w: general(n, w)))(weigh)
    return log


def test_explorer_matches_the_page():
    data = node_json(f"""
      const m = {explorer_require()};
      const out = {{}};
      for (let n = 3; n <= 39; n++) {{
        const {{ k, codes }} = m.obCodes(n);
        const runs = [];
        for (let b = 1; b <= n; b++) for (const h of [true, false]) {{
          const r = m.obWeigh(codes, k, b, h);
          runs.push({{ b, h, out: r.out, pans: r.pans.map((p) => [p.L, p.R]), who: m.obDecode(codes, r.out) }});
        }}
        const rows = m.obRows(codes, k);
        out[n] = {{ k, codes, runs, rows: rows.map((r) => [r.out, r.who]) }};
      }}
      console.log(JSON.stringify(out));
    """)
    for n in range(3, 40):
        d = data[str(n)]
        assert d["k"] == fewest(n)
        if n == 12:
            assert [tuple(c) for c in d["codes"]] == list(CODES.values())
        for r in d["runs"]:
            log = recorded(n, r["b"], r["h"])
            assert [(sorted(L), sorted(R)) for L, R in log] == [(sorted(L), sorted(R)) for L, R in r["pans"]], (n, r["b"])
            assert r["who"] == {"ball": r["b"], "heavy": r["h"]}
        # the decision table: every vector once, sorted L < = < R by weighing, 2n of them name a ball
        assert len(d["rows"]) == 3 ** d["k"]
        rank = {1: 0, 0: 1, -1: 2}
        keys = [[rank[v] for v in out] for out, _ in d["rows"]]
        assert keys == sorted(keys)
        named = [who for _, who in d["rows"] if who]
        assert len(named) == 2 * n and len({(w["ball"], w["heavy"]) for w in named}) == 2 * n
    unused12 = [out for out, who in data["12"]["rows"] if not who]
    assert sorted(map(tuple, unused12)) == [(-1, 1, -1), (0, 0, 0), (1, -1, 1)]
