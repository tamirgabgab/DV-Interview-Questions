"""Question 0073: the page's shuffles_to_return against shuffling a deck until it is back
(every n up to 120, both kinds); the formula p -> 2p mod M of each kind against the shuffle
itself; the page's numbers (8 and 52 for 52 cards, 6 for 64, the powers of 2 mod 51 and
53, 2^4 = 16, the odd in-shuffle column of the table); the facts the page states about the
edge cases (M = 1, a wrong base matches no card, the stack of the interleave is O(log n),
the middle of the interleave is an in-shuffle with Jain's leaders, k piles); interleave
against the definition on every even length up to 200; the explorer's JavaScript against
the generator (decks up to 100, the powers of 2 past 2^53); and the page copies of the blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0073  # noqa: E402

ns = load_python(73)
shuffles_to_return, interleave = ns["shuffles_to_return"], ns["interleave"]


def test_the_count_matches_shuffling():
    for n in range(2, 121):
        for kind in ("out", "in"):
            assert shuffles_to_return(n, kind) == q0073.order_by_shuffling(n, kind), (n, kind)
    assert shuffles_to_return(52) == 8 and shuffles_to_return(52, "in") == 52 and shuffles_to_return(64) == 6
    assert [pow(2, e, 51) for e in range(1, 9)] == [2, 4, 8, 16, 32, 13, 26, 1]
    assert pow(2, 13, 53) == 30 and pow(2, 26, 53) == 52


def test_the_position_formulas():
    for n in range(2, 60):
        for kind in ("out", "in"):
            after = q0073.shuffle(list(range(n)), kind)
            where = {c: p for p, c in enumerate(after)}
            m = q0073.modulus(n, kind)
            for p in range(n):
                if n % 2 == 0 and kind == "out":
                    want = n - 1 if p == n - 1 else 2 * p % m              # 0-based, the bottom card stays
                elif n % 2 == 0:
                    want = 2 * (p + 1) % m - 1                             # 1-based q -> 2q mod (n + 1)
                elif kind == "out":
                    want = 2 * p % m                                       # odd, top half larger
                else:
                    want = (2 * (p + 1) % m or m) - 1                      # odd, bottom half larger
                assert where[p] == want, (n, kind, p)


def test_page_facts():
    # the odd rows of the table: both kinds, modulo n
    assert [shuffles_to_return(n, k) for n in (7, 51) for k in ("out", "in")] == [3, 3, 8, 8]
    # the proof of 52: of the divisors of 52, 26 (and so 1, 2, 13) fails, and 4 fails
    assert pow(2, 4, 53) == 16 and pow(2, 26, 53) == 52 and [e for e in (1, 2, 4, 13, 26, 52) if pow(2, e, 53) == 1] == [52]
    # M = 1 (two cards, out): e = 1, though 2 mod 1 = 0 and e > M - 1
    assert shuffles_to_return(2, "out") == 1 and 2 % 1 == 0
    # e <= M - 1 for every M > 1
    for n in range(3, 200):
        for k in ("out", "in"):
            m = q0073.modulus(n, k)
            assert m == 1 or shuffles_to_return(n, k) <= m - 1
    # the trap: in the wrong base the formula fits no card at all
    for n in (8, 10, 16, 52):
        out_after = {c: p for p, c in enumerate(q0073.shuffle(list(range(n)), "out"))}
        in_after = {c: p for p, c in enumerate(q0073.shuffle(list(range(n)), "in"))}
        assert not any(out_after[p] == 2 * (p + 1) % (n - 1) - 1 for p in range(n))     # out counted from 1
        assert not any(in_after[p] == 2 * p % (n + 1) for p in range(n))                # in counted from 0
    # k equal piles: k divides n, so k is coprime to n - 1 and the order exists
    from math import gcd
    assert all(gcd(k, n - 1) == 1 for n in range(2, 300) for k in range(2, n + 1) if n % k == 0)


def stack_depth(n):
    """The largest stack of the page's interleave on 2m = n elements."""
    stack, most = [(0, n // 2)], 1
    while stack:
        lo, m = stack.pop()
        if m <= 1:
            continue
        h = m // 2
        stack += [(lo, h), (lo + 2 * h, m - h)]
        most = max(most, len(stack))
    return most


def test_interleave_stack_and_jain():
    # the stack grows with log n (4, 8, 12, 16 for n = 16, 256, 4096, 65536): O(log n) memory
    assert [stack_depth(n) for n in (16, 256, 4096, 65536)] == [4, 8, 12, 16]
    # the interleave keeps the first and the last element; the 2m - 2 between them are an
    # in-shuffle, q -> 2q mod (2m - 1) counted from 1 (not 2q mod (n + 1))
    for n in (8, 10, 26, 28):
        a = list(range(n))
        interleave(a)
        where = {c: p for p, c in enumerate(a)}
        assert where[0] == 0 and where[n - 1] == n - 1
        assert all(where[q] == 2 * q % (n - 1) for q in range(1, n - 1))
        assert not all(where[q - 1] == 2 * q % (n + 1) - 1 for q in range(1, n + 1))
    # Jain's leaders: when 2m - 2 = 3^k - 1 the cycles start at 1, 3, ..., 3^(k-1)
    for k in (1, 2, 3, 4):
        n = 3 ** k + 1
        seen, leaders = set(), []
        for q in range(1, n - 1):
            if q not in seen:
                leaders.append(q)
                x = q
                while x not in seen:
                    seen.add(x)
                    x = 2 * x % (n - 1)
        assert leaders == [3 ** i for i in range(k)], n


def test_the_box_tasks():
    # 52: 8 out, 52 in with one cycle of 52; 10 out: cycles 2 and 6, back after 6, the long
    # one through place 1; 32 out: 5, six cycles of 5; 51 and 52 out: both 8
    lens = lambda n, k: sorted(len(c) for c in q0073.cycles(n, k) if len(c) > 1)   # noqa: E731
    assert shuffles_to_return(52) == 8 and shuffles_to_return(52, "in") == 52 and lens(52, "in") == [52]
    assert lens(10, "out") == [2, 6] and shuffles_to_return(10) == 6
    assert len(next(c for c in q0073.cycles(10, "out") if 1 in c)) == 6
    assert shuffles_to_return(32) == 5 and lens(32, "out") == [5] * 6
    assert shuffles_to_return(51) == shuffles_to_return(52) == 8


def test_interleave():
    for n in range(0, 201, 2):
        a = list(range(n))
        interleave(a)
        m = n // 2
        assert a == [x for i in range(m) for x in (i, m + i)], n
    rng = random.Random(73)
    for _ in range(50):
        m = rng.randint(1, 300)
        a = [rng.randint(0, 9) for _ in range(2 * m)]
        b = list(a)
        interleave(b)
        assert b == q0073.shuffle(a, "out")


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    cases = [(n, k) for n in range(2, 101) for k in ("out", "in")]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([n, k]) => ({{ deck: m.faroShuffle(Array.from({{ length: n }}, (_, i) => i), k), order: m.faroOrder(n, k), cycles: m.faroCycles(n, k) }}))));""")
    for (n, k), g in zip(cases, got):
        assert g["deck"] == q0073.shuffle(list(range(n)), k) and g["order"] == q0073.order_by_shuffling(n, k), (n, k)
        assert g["cycles"] == q0073.cycles(n, k)
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify([[100, 101], [64, 65], [52, 53], [3, 1]].map(([t, M]) => m.pow2mod(t, M))));""")
    assert got == [pow(2, 100, 101), pow(2, 64, 65), pow(2, 52, 53), 0]


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(73)
