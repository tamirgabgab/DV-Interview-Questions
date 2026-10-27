"""Question 0051: the page's mice_needed, drink_round, experiment and find_bottle against
the generator's independent model (tools/figures/q0051.py) for every bottle of small
cellars and one to four rounds, and against brute force for the lower bound (no smaller
number of mice gives every bottle its own outcome); the page's numbers (10, 7 and 5 mice
for 1000 bottles, bottle 613 in one and two rounds); the explorer's JavaScript; and the
page copies of the generated blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0051  # noqa: E402

ns = load_python(51)
mice_needed, drink_round, experiment, find_bottle = (ns[k] for k in ("mice_needed", "drink_round", "experiment", "find_bottle"))


def test_page_numbers():
    assert [mice_needed(1000, b) for b in (1, 2, 3)] == [10, 7, 5]
    assert [mice_needed(1000, b) for b in range(1, 10)] == [10, 7, 5, 5, 4, 4, 4, 4, 3]
    assert 2 ** 9 < 1000 <= 2 ** 10 and 3 ** 6 < 1000 <= 3 ** 7 and 4 ** 4 < 1000 <= 4 ** 5
    assert format(613, "b") == "1001100101"
    assert experiment(613, 1000, 1) == [1, 0, 1, 0, 0, 1, 1, 0, 0, 1]          # mice 0, 2, 5, 6, 9 die
    assert experiment(613, 1000, 2) == [1, 0, 2, 1, 1, 2, 0] == q0051.digits(613, 3, 7)
    assert find_bottle([1, 0, 2, 1, 1, 2, 0], 2) == 613 == 1 + 2 * 9 + 27 + 81 + 2 * 243
    # the follow-ups: 5 mice and 1000 bottles take 3 rounds; 4 machines bisect 1000 commits in 5 hours
    assert min(b for b in range(1, 20) if mice_needed(1000, b) <= 5) == 3
    assert mice_needed(1000, 4) == 5 and 5 ** 4 < 1000
    assert 1000 * 999 // 2 == 499_500 and 2 ** 18 < 499_500 <= 2 ** 19
    # edge cases: one bottle needs no mouse; n a power exactly
    assert mice_needed(1, 1) == 0 and mice_needed(1024, 1) == 10 and mice_needed(1025, 1) == 11


def test_every_bottle_is_found():
    for b in range(1, 5):
        for n in list(range(1, 90)) + [243, 244, 1000]:
            m = mice_needed(n, b)
            assert m == q0051.needed(n, b), (n, b)
            for x in range(n):
                death = experiment(x, n, b)
                assert death == q0051.outcome(x, m, b), (x, n, b)
                assert find_bottle(death, b) == x == q0051.decode(death, b)


def test_drink_rounds_and_dead_mice():
    """drink_round is the digit; a mouse dies in the round of its digit and only drank from
    bottles with smaller digits before, so it never dies early."""
    rng = random.Random(51)
    for _ in range(300):
        b, n = rng.randint(1, 4), rng.randint(2, 3000)
        m, x = mice_needed(n, b), rng.randrange(n)
        death = experiment(x, n, b)
        for i in range(m):
            assert drink_round(x, i, b) == q0051.digits(x, b + 1, m)[i] == death[i]


def test_lower_bound_by_brute_force():
    """With one mouse fewer, two bottles share an outcome under the page's plan, and no
    plan at all can do better: (b + 1)^(m - 1) < n outcomes."""
    for b in range(1, 4):
        for n in range(2, 200):
            m = mice_needed(n, b)
            assert (b + 1) ** (m - 1) < n <= (b + 1) ** m


def test_explorer_matches_the_page_code():
    from page_tests import explorer_require, node_json

    rng = random.Random(52)
    cases = [(1000, 1, 613), (1000, 2, 613), (1000, 3, 999), (1, 1, 0), (1024, 1, 1023)]
    cases += [(n, b, rng.randrange(n)) for n, b in ((rng.randint(1, 2000), rng.randint(1, 5)) for _ in range(60))]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([n, b, x]) => {{
        const k = m.miceNeeded(n, b), d = m.miceDeath(x, k, b);
        return [k, d, m.miceFind(d, b), m.miceDigits(x, b, k)];
      }})));""")
    for (n, b, x), (k, death, found, digits) in zip(cases, got):
        assert k == mice_needed(n, b) and death == experiment(x, n, b) and found == x
        assert digits == [drink_round(x, i, b) for i in range(k)]


def test_explorer_candidates():
    """The bottles still possible after each round: all of them before the first, only the
    poisoned one after the last, and after round r the ones whose digits agree with every
    death so far and are 0 or above r for every mouse still alive."""
    from page_tests import explorer_require, node_json

    cases = [(27, 2, 13), (100, 1, 37), (64, 3, 50), (120, 4, 7)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([n, b, x]) => {{
        const d = m.miceDeath(x, m.miceNeeded(n, b), b);
        return [...Array(b + 1).keys()].map((r) => m.miceCands(n, b, d, r));
      }})));""")
    for (n, b, x), rounds in zip(cases, got):
        m = mice_needed(n, b)
        death = experiment(x, n, b)
        assert rounds[0] == list(range(n)) and rounds[-1] == [x]
        for r, cands in enumerate(rounds):
            want = [y for y in range(n) if all((d <= r and d and drink_round(y, i, b) == d) or
                                               (not (d and d <= r) and drink_round(y, i, b) in [0] + list(range(r + 1, b + 1)))
                                               for i, d in enumerate(death))]
            assert cands == want and x in cands, (n, b, x, r)
        assert m == len(death)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(51)
