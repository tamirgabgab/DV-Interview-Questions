"""Question 0064: the page's one_pan, two_pans, placement and balances on every load each
mode can weigh (and None just above it), against a search over every coefficient vector;
the bounds and the uniqueness claims by an exhaustive search over the weight sets of small
k (1, 2, 4, 8 on one pan; 1, 3, 9, 27 the only four weights reaching 40; 1, 5, 25 with two
copies; 1, 7 with three); random large loads for the conversion; the numbers of the
solutions and of the follow-ups; the explorer's JavaScript against the generator; and the
page copies of the blocks."""

import json
import random
import sys
from itertools import combinations_with_replacement, product

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0064  # noqa: E402

ns = load_python(64)
one_pan, two_pans, placement, balances = ns["one_pan"], ns["two_pans"], ns["placement"], ns["balances"]


def values(weights, lo, hi):
    """Every load the weights weigh with a coefficient lo..hi each, as a bit mask of the
    values shifted by an offset (fast enough for every set of three values up to 62)."""
    off = -lo * sum(weights)
    mask = 1 << off
    for w in weights:
        new = 0
        for e in range(lo, hi + 1):
            new |= mask << (e - lo) * w
        mask = new >> (-lo * w)
    return mask, off


def reach(weights, lo, hi):
    """The largest N with every load 1..N weighed."""
    mask, off = values(weights, lo, hi)
    n = 0
    while mask >> (off + n + 1) & 1:
        n += 1
    return n


def best_sets(k, lo, hi, vmax):
    best, arg = 0, []
    for ws in combinations_with_replacement(range(1, vmax + 1), k):
        r = reach(ws, lo, hi)
        if r > best:
            best, arg = r, [ws]
        elif r == best:
            arg.append(ws)
    return best, arg


def test_reach_by_bitmask_matches_a_direct_search():
    rng = random.Random(64)
    for _ in range(200):
        ws = [rng.randint(1, 30) for _ in range(rng.randint(1, 4))]
        c, two = rng.randint(1, 3), rng.random() < 0.5
        lo = -c if two else 0
        vals = {sum(e * w for e, w in zip(v, ws)) for v in product(range(lo, c + 1), repeat=len(ws))}
        n = 0
        while n + 1 in vals:
            n += 1
        assert reach(ws, lo, c) == n, (ws, c, two)


def test_page_examples():
    assert one_pan(40, 6) == [0, 0, 0, 1, 0, 1]                    # 40 = 32 + 8
    assert one_pan(64, 6) is None and one_pan(63, 6) == [1] * 6
    assert two_pans(25, 4) == [1, -1, 0, 1]                        # 25 = 27 - 3 + 1
    assert two_pans(40, 4) == [1, 1, 1, 1] and two_pans(41, 4) is None
    assert placement(40, 3, 2) == [0, -2, 2]                       # 40 + 5 + 5 = 25 + 25
    assert balances(40, 2, True, [0, -2, 2]) and not balances(40, 2, True, [0, -3, 2])
    assert not balances(5, 1, False, [-1, 2])                      # nothing beside the load on one pan
    assert [r[4] for r in q0064.convert(25, 4, 1, True)] == [1, -1, 0, 1]
    assert [r[6] for r in q0064.convert(25, 4, 1, True)] == [8, 3, 1, 0]
    assert [r[2] for r in q0064.convert(40, 6, 1, False)] == [40, 20, 10, 5, 2, 1]
    assert [r[3] for r in q0064.convert(40, 3, 2, True)] == [0, 3, 2]
    assert int("221", 3) == 25                                     # the trap: ordinary base 3
    assert reach([1, 2, 4, 8, 16, 9], 0, 1) == 40 == sum([1, 2, 4, 8, 16, 9])    # six pieces of the 40 kg stone, one pan
    assert reach([1, 2, 4, 8, 16], 0, 1) == 31 < 40


def test_every_load_in_every_mode():
    for c in (1, 2, 3, 4):
        for two in (False, True):
            for k in range(1, 6 if c == 1 else 4):
                top = q0064.reach_bound(k, c, two)
                assert top == (((2 * c + 1) ** k - 1) // 2 if two else (c + 1) ** k - 1)
                for n in range(0, top + 1):
                    d = placement(n, k, c, two)
                    assert d is not None and balances(n, c, two, d), (n, k, c, two)
                    if k <= 4:
                        assert d == q0064.coefficients(n, k, c, two), (n, k, c, two)
                    if c == 1:
                        assert d == (two_pans(n, k) if two else one_pan(n, k))
                assert placement(top + 1, k, c, two) is None
                if c == 1:
                    assert (two_pans if two else one_pan)(top + 1, k) is None


def test_bounds_and_uniqueness_by_search():
    for k in range(1, 5):                                          # one pan: 2^k - 1, by 1, 2, 4, ... only
        assert best_sets(k, 0, 1, 2 ** k) == (2 ** k - 1, [tuple(2 ** i for i in range(k))])
    for k in range(1, 5):                                          # two pans: (3^k - 1) / 2, by 1, 3, 9, ... only
        assert best_sets(k, -1, 1, (3 ** k - 1) // 2 + 1) == ((3 ** k - 1) // 2, [tuple(3 ** i for i in range(k))])
    assert best_sets(2, -2, 2, 13) == (12, [(1, 5)])
    assert best_sets(3, -2, 2, 63) == (62, [(1, 5, 25)])
    assert best_sets(2, -3, 3, 25) == (24, [(1, 7)])
    assert best_sets(2, 0, 2, 9) == (8, [(1, 3)])
    # a weight above the bound plus one never helps: the search ranges above are complete
    for k, lo, hi in [(3, -1, 1), (2, -2, 2), (2, 0, 1)]:
        b = q0064.reach_bound(k, hi, lo < 0)
        for ws in combinations_with_replacement(range(1, b + 4), k):
            if max(ws) > b + 1:
                assert reach(ws, lo, hi) < b


def test_physical_pieces():
    for c in range(1, 8):
        assert 2 * c + 1 <= 3 ** c                                 # copies never weigh further per piece
    assert (3 ** 3 - 1) // 2 == 13 < 40 <= (3 ** 4 - 1) // 2       # so 4 pieces at least, in any model
    assert reach([1, 1, 5, 5, 25, 25], -1, 1) == 62                # two copies of 1, 5, 25 as six single pieces


def test_random_large_loads():
    rng = random.Random(6464)
    for _ in range(2000):
        c, two = rng.randint(1, 5), rng.random() < 0.5
        k = rng.randint(1, 18)
        n = rng.randint(0, q0064.reach_bound(k, c, two))
        d = placement(n, k, c, two)
        b = q0064.base_of(c, two)
        assert d is not None and len(d) == k and balances(n, c, two, d)
        assert sum(x * b ** i for i, x in enumerate(d)) == n
    for _ in range(500):
        n = rng.randint(0, (3 ** 30 - 1) // 2)
        d = two_pans(n, 30)
        assert sum(x * 3 ** i for i, x in enumerate(d)) == n and set(d) <= {-1, 0, 1}
        assert one_pan(n, 48) == [int(b) for b in reversed(format(n, "048b"))]


def test_follow_ups():
    # half kilos: 80 loads in halves, five weights 1, 3, 9, 27, 81 halves
    assert min(k for k in range(1, 9) if (3 ** k - 1) // 2 >= 80) == 5
    assert reach([1, 3, 9, 27, 81], -1, 1) >= 80
    # an unknown load 1..40: q weighings tell at most 2^(q+1) - 1 loads apart, and 5 do it
    from functools import lru_cache

    @lru_cache(None)
    def weighings(m):                                              # m candidates in a row
        if m <= 1:
            return 0
        return 1 + min(max(weighings(v), weighings(m - 1 - v)) for v in range(m))
    assert weighings(40) == 5 and weighings(31) == 4 and weighings(32) == 5
    assert all(two_pans(v, 4) is not None for v in range(1, 41))   # every comparison value can be set up
    # CSD of 23: 32 - 8 - 1, three nonzero digits against four ones in binary

    def csd(n):
        out = []
        while n:
            d = 0 if n % 2 == 0 else 2 - n % 4
            out.append(d)
            n = (n - d) // 2
        return out
    assert csd(23) == [-1, 0, 0, -1, 0, 1] and bin(23).count("1") == 4
    assert csd(7) == [-1, 0, 0, 1]
    for n in range(1, 2000):
        d = csd(n)
        assert sum(x * 2 ** i for i, x in enumerate(d)) == n
        assert all(not (d[i] and d[i + 1]) for i in range(len(d) - 1))
        assert sum(map(bool, d)) <= bin(n).count("1")
    # a stone of 100 kg in five pieces: 1, 3, 9, 27 and a fifth from 60 to 81
    assert [w for w in range(1, 200) if reach([1, 3, 9, 27, w], -1, 1) >= 100] == list(range(60, 82))
    assert sum([1, 3, 9, 27, 60]) == 100


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    cases = []
    for c in (1, 2, 3, 4):
        for two in (False, True):
            for k in range(1, 5):
                for n in range(1, q0064.reach_bound(k, c, two) + 2, 7):
                    cases.append([n, k, c, two])
    got = node_json(f"""
      const m = {explorer_require()};
      const cases = {json.dumps(cases)};
      console.log(JSON.stringify({{
        steps: cases.map(([n, k, c, two]) => m.wtSteps(n, k, c, two).map((r) => [r.i, r.w, r.before, r.r, r.d, r.carry, r.after])),
        digits: cases.map(([n, k, c, two]) => m.wtDigits(n, k, c, two)),
        bound: cases.map(([n, k, c, two]) => m.wtBound(k, c, two)),
        reach: cases.map(([n, k, c, two]) => m.wtReach(Array.from({{ length: k }}, (_, i) => (two ? 2 * c + 1 : c + 1) ** i), two ? -c : 0, c)),
        odd: [m.wtReach([1, 2, 4, 8], -1, 1), m.wtReach([1, 2, 4, 8, 16, 9], 0, 1)],
      }}));""")
    for (n, k, c, two), steps, digits, bound, r in zip(cases, got["steps"], got["digits"], got["bound"], got["reach"]):
        assert [tuple(s) for s in steps] == q0064.convert(n, k, c, two)
        assert digits == placement(n, k, c, two)
        assert bound == r == q0064.reach_bound(k, c, two)
    assert got["odd"] == [reach([1, 2, 4, 8], -1, 1), 40]


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(64)
