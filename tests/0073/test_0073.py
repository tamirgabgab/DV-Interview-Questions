"""Question 0073: the page's shuffles_to_return against shuffling a deck until it is back
(every n up to 120, both kinds); the formula p -> 2p mod M of each kind against the shuffle
itself; the page's numbers (8 and 52 for 52 cards, 6 for 64, the powers of 2 mod 51 and
53); interleave against the definition on every even length up to 200; the explorer's
JavaScript against the generator; and the page copies of the blocks."""

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

    cases = [(n, k) for n in range(2, 53) for k in ("out", "in")]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([n, k]) => ({{ deck: m.faroShuffle(Array.from({{ length: n }}, (_, i) => i), k), order: m.faroOrder(n, k), cycles: m.faroCycles(n, k) }}))));""")
    for (n, k), g in zip(cases, got):
        assert g["deck"] == q0073.shuffle(list(range(n)), k) and g["order"] == q0073.order_by_shuffling(n, k), (n, k)
        assert g["cycles"] == q0073.cycles(n, k)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(73)
