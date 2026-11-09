"""Question 0045: the page's three Python solvers against a hidden odd ball (every ball,
heavy and light; part a and b on 12 balls in at most 3 weighings, part c for every n from
3 to 364 in exactly the fewest weighings, equal pans in every weighing), the numbers the
page states (the table of k and N, the formula ceil(log3(2N + 3)), the codes of part b, the
unused vectors, the 13-ball argument by an exact search over adaptive strategies, part c's
example orbits, the two-odd-ball count of the DV follow-up), and the explorer's JavaScript: the same codes and
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


def solvable(u, h, l, g, k, memo={}):
    """Exact search over adaptive strategies on class counts: u balls of unknown kind, h
    that can only be heavy, l only light, g known genuine; k weighings left. Solved when at
    most one (ball, kind) is left."""
    key = (u, h, l, g, k)
    if key in memo:
        return memo[key]
    poss = 2 * u + h + l
    ok = poss <= 1
    if not ok and k and poss <= 3 ** k:
        for u1, u2, h1, h2, l1, l2 in product(range(u + 1), range(u + 1), range(h + 1), range(h + 1), range(l + 1), range(l + 1)):
            n1, n2 = u1 + h1 + l1, u2 + h2 + l2
            if u1 + u2 > u or h1 + h2 > h or l1 + l2 > l or n1 + n2 == 0 or abs(n1 - n2) > g:
                continue
            tot = u + h + l + g
            branches = [(0, u1 + h1, u2 + l2), (0, u2 + h2, u1 + l1), (u - u1 - u2, h - h1 - h2, l - l1 - l2)]
            if all(solvable(*b, tot - sum(b), k - 1) for b in branches):
                ok = True
                break
    memo[key] = ok
    return ok


def test_bounds_by_search():
    """The short answer (N >= 3), trap 1 and follow-up 1: 13 balls need a fourth weighing
    because the first one has no genuine ball yet, not because of the all-balanced vector."""
    assert not solvable(1, 0, 0, 0, 5) and not solvable(2, 0, 0, 0, 5)       # N = 1, 2: never
    assert [n for n in range(1, 14) if solvable(n, 0, 0, 0, 3)] == list(range(3, 13))
    assert 2 * 13 <= 3 ** 3 - 1                                              # the count allows 13
    assert solvable(13, 0, 0, 1, 3) and not solvable(13, 0, 0, 0, 3)         # one helper decides
    assert solvable(4, 0, 0, 1, 2) and not solvable(5, 0, 0, 1, 2)           # two weighings with help: 4
    assert [solvable(n, 0, 0, 0, 2) for n in (3, 4)] == [True, False]


def test_two_odd_balls():
    """The DV follow-up: part b's table corrects one odd ball and does not detect two (each
    off by the same weight): 252 of the 264 cases decode to a single ball, 60 of them to one
    of the two with its kind; 12 land on the unused pair, none on (0, 0, 0)."""
    sign = lambda x: (x > 0) - (x < 0)
    unused, silent, one_of = [], 0, 0
    for (a, ca), (b, cb) in [(x, y) for i, x in enumerate(CODES.items()) for y in list(CODES.items())[i + 1:]]:
        for sa, sb in product((1, -1), repeat=2):
            out = tuple(sign(sa * ca[j] + sb * cb[j]) for j in range(3))
            hit = [(x, 1) for x, c in CODES.items() if c == out] + [(x, -1) for x, c in CODES.items() if tuple(-v for v in c) == out]
            if hit:
                silent += 1
                one_of += hit[0] in ((a, sa), (b, sb))
            else:
                unused.append(out)
    assert silent == 252 and len(unused) == 12 and one_of == 60
    assert sorted(set(unused)) == [(-1, 1, -1), (1, -1, 1)]


def test_part_c_example():
    """Part c's example: the four orbits for k = 3, each column of an orbit +1, -1 and 0
    once; they leave out +-(1, 1, 1), part b's table leaves out +-(1, -1, 1); and for 13
    balls the genuine balls of weighing 2 depend on weighing 1."""
    page = [((1, 1, -1), (-1, -1, 0), (0, 0, 1)), ((1, -1, 0), (-1, 0, 1), (0, 1, -1)),
            ((1, -1, 1), (-1, 0, -1), (0, 1, 0)), ((1, -1, -1), (-1, 0, 0), (0, 1, 1))]
    for orbit in page:
        for j in range(3):
            assert sorted(c[j] for c in orbit) == [-1, 0, 1]
        assert orbit[1] == tuple((x + 2) % 3 - 1 for x in orbit[0])        # c + 1 (mod 3)
    def pans(n, odd):
        log = []
        weigh, _ = make_scale(n, odd, True, log)
        general(n, weigh)
        return [(sorted(L), sorted(R)) for L, R in log]
    logs = [pans(12, b) for b in range(1, 13)]
    assert all(lg == logs[0] for lg in logs)                                  # 12: no helper
    built = {tuple(1 if b in L else -1 if b in R else 0 for L, R in logs[0]) for b in range(1, 13)}
    assert built == {c for orbit in page for c in orbit}                      # the page's example is the code's
    nonzero = [c for c in product((-1, 0, 1), repeat=3) if any(c)]
    assert sorted(c for c in nonzero if c not in built and tuple(-x for x in c) not in built) == [(-1, -1, -1), (1, 1, 1)]
    balanced, tipped = pans(13, 13), pans(13, 1)
    assert balanced[1] == ([4, 7, 10, 13], [2, 5, 8, 11])
    assert tipped[1] == ([1, 4, 7, 10, 13], [2, 3, 5, 8, 11])


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


def test_figure():
    """The figure of part a: eight cases are left after every result of the first weighing,
    and the page copy is up to date."""
    import sys
    from extract_code import ROOT
    from page_tests import assert_figures_match

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import q0045

    for res, _ in q0045.RESULTS:
        left = q0045.candidates(res).values()
        assert sum((v == "both") + (v is not None) for v in left) == 8, res
    assert_figures_match(45)
