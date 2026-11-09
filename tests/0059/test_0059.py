"""Question 0059: the page's best_total against the generator's minimax and parity_move as
the first player against every reply (it collects exactly its colour, at least half); the
page's examples (6 by the trick and 5 by greedy on 1, 2, 5, 3; 19 against 11 on
1, 1, 9, 1, 1, 9; 2 on 1, 5, 1) and that 1, 2, 5, 3 is the first row of four distinct coins
up to 5 where greedy loses; the explorer's JavaScript; and the page copies of the blocks."""

import itertools
import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0059  # noqa: E402

ns = load_python(59)
parity_move, best_total = ns["parity_move"], ns["best_total"]


def test_page_examples():
    assert best_total([1, 2, 5, 3]) == 6 and q0059.play([1, 2, 5, 3], "greedy", "optimal")[1] == [5, 6]
    assert max(1 + 5, 2 + 3) == 6 and q0059.play([1, 2, 5, 3], "parity", "optimal")[1] == [6, 5]
    assert best_total([1, 1, 9, 1, 1, 9]) == 19 and q0059.play([1, 1, 9, 1, 1, 9], "parity", "optimal")[1] == [11, 11]
    assert best_total([1, 5, 1]) == 2
    first = next(c for c in itertools.permutations(range(1, 6), 4) if 2 * q0059.play(list(c), "greedy", "optimal")[1][0] < sum(c))
    assert first == (1, 2, 5, 3)
    assert all(2 * q0059.play(list(c), "greedy", "optimal")[1][0] >= sum(c) for c in itertools.product(range(1, 6), repeat=2))
    assert best_total([5]) == 5
    # part b's proof: with distinct values the smallest losing sum is 11, by six rows (1, 2, 5, 3
    # first); with repeated values 1, 1, 3, 2 (sum 7) already loses, 3 against 4
    losing = [c for c in itertools.permutations(range(1, 9), 4) if 2 * q0059.play(list(c), "greedy", "optimal")[1][0] < sum(c)]
    low = min(map(sum, losing))
    assert low == 11 and sorted(c for c in losing if sum(c) == low) == [
        (1, 2, 5, 3), (1, 3, 5, 2), (2, 1, 5, 3), (2, 5, 3, 1), (3, 5, 1, 2), (3, 5, 2, 1)]
    assert q0059.play([1, 1, 3, 2], "greedy", "optimal")[1] == [3, 4]
    # part e: one more coin is sometimes enough
    assert best_total([5, 1, 1]) == 6


def test_follow_ups():
    """The O(n) memory follow-up needs i ascending; the three-player game needs a tie rule."""
    from functools import lru_cache

    def one_array(coins, ascending):
        n, d = len(coins), list(coins)
        for length in range(2, n + 1):
            order = range(n - length + 1)
            for i in (order if ascending else reversed(order)):
                j = i + length - 1
                d[i] = max(coins[i] - d[i + 1], coins[j] - d[i])
        return d[0]

    rng, wrong = random.Random(61), 0
    for _ in range(300):
        coins = [rng.randint(1, 30) for _ in range(rng.randint(2, 10))]
        lead = 2 * best_total(coins) - sum(coins)
        assert one_array(coins, True) == lead
        wrong += one_array(coins, False) != lead
    assert wrong > 0

    def three(coins, tie):
        @lru_cache(None)
        def f(i, j, w):                     # the three totals from coins[i..j], player w to move
            if i > j:
                return (0, 0, 0)
            opts = []
            for k, rest in ((i, (i + 1, j)), (j, (i, j - 1)))[: 1 if i == j else 2]:
                r = list(f(*rest, (w + 1) % 3))
                r[w] += coins[k]
                opts.append(tuple(r))
            if len(opts) == 1 or opts[0][w] != opts[1][w]:
                return max(opts, key=lambda r: r[w])
            return opts[0] if tie == "L" else opts[1]
        return f(0, len(coins) - 1, 0)

    assert three((1, 1, 1, 2, 1), "L") == (3, 2, 1) and three((1, 1, 1, 2, 1), "R") == (2, 3, 1)


def test_against_minimax():
    rng = random.Random(58)
    for _ in range(400):
        coins = [rng.randint(1, 30) for _ in range(rng.randint(1, 11))]
        assert best_total(coins) == q0059.best(coins), coins


def test_parity_against_every_reply():
    """The trick as the first player collects its whole colour whatever the second does."""
    rng = random.Random(59)
    for _ in range(60):
        n = rng.choice([2, 4, 6, 8])
        coins = [rng.randint(1, 20) for _ in range(n)]
        colour = max(sum(coins[0::2]), sum(coins[1::2]))

        def worst(i, j, mine):              # the first player's total against the worst replies
            if i > j:
                return mine
            k = i if parity_move(coins, i, j) in ("L", 0) else j
            mine += coins[k]
            i, j = (i + 1, j) if k == i else (i, j - 1)
            if i > j:
                return mine
            return min(worst(i + 1, j, mine), worst(i, j - 1, mine))
        assert worst(0, n - 1, 0) == colour >= sum(coins) / 2


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(60)
    rows = [[1, 2, 5, 3], [1, 1, 9, 1, 1, 9], [1, 5, 1]] + [[rng.randint(1, 20) for _ in range(rng.randint(1, 10))] for _ in range(40)]
    pairs = [(a, b) for a in ("greedy", "parity", "optimal") for b in ("greedy", "parity", "optimal")]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(rows)}.map((c) => [m.crDiff(c), {json.dumps(pairs)}.map(([a, b]) => m.crPlay(c, a, b))])));""")
    for coins, (d, games) in zip(rows, got):
        assert d == q0059.diff_table(coins)
        for (a, b), g in zip(pairs, games):
            moves, tot = q0059.play(coins, a, b)
            assert g["tot"] == tot and [[w, s, c] for w, s, c in moves] == g["moves"], (coins, a, b)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(59)
