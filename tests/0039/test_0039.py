"""Question 0039: every number the page states (9 drops, the floors 37, 66, 88, 100, the
table of covered floors, 46 thresholds at the worst case, the answers table), the
generator's binomial reference against the page's capped table, the page plan against
every threshold (never more than the worst case, always ends on the threshold), the
optimum by exhaustive search on small cases, the explorer's JavaScript, and the page
copies of the generated blocks."""

import sys
from functools import lru_cache
from math import comb

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0039  # noqa: E402

ns = load_python(39)
egg_table, min_drops, egg_run = ns["egg_table"], ns["min_drops"], ns["egg_run"]


@lru_cache(None)
def optimum(e, m):
    """The fewest drops that settle m unknown floors with e eggs in the worst case, by
    trying every first floor (the textbook DP)."""
    if m == 0:
        return 0
    if e == 1:
        return m
    return 1 + min(max(optimum(e - 1, x - 1), optimum(e, m - x)) for x in range(1, m + 1))


def test_page_numbers():
    assert min_drops(3, 100) == 9 == q0039.min_drops(3, 100)
    assert q0039.first_egg_floors(3, 100) == [37, 66, 88, 100]
    assert [q0039.covered(3, t) for t in (8, 9)] == [92, 129]
    assert [q0039.covered(2, t) for t in (7, 8)] == [28, 36]
    assert q0039.run(3, 100, 36) == [(37, True)] + [(fl, False) for fl in (8, 15, 21, 26, 30, 33, 35, 36)]
    used = q0039.drops_per_threshold(3, 100)
    assert max(used) == 9 and sum(1 for d in used if d == 9) == 46
    assert abs(sum(used) / len(used) - 7.72) < 0.005                  # the follow-up's expectation
    assert q0039.min_drops(2, 100) == 14 and q0039.first_egg_floors(2, 100) == [14, 27, 39, 50, 60, 69, 77, 84, 90, 95, 99, 100]
    assert [q0039.min_drops(k, 100) for k in range(1, 11)] == [100, 14, 9, 8, 7, 7, 7, 7, 7, 7]
    assert [q0039.min_drops(k, 1000) for k in range(1, 11)] == [1000, 45, 19, 13, 11, 11, 11, 10, 10, 10]
    assert q0039.min_drops(3, 1000) == 19 and q0039.min_drops(3, 10000) == 40
    # the traps: binary search and equal jumps with three eggs
    assert 1 + q0039.min_drops(2, 49) == 11
    assert 4 + q0039.min_drops(2, 24) == 11


def test_capped_table_matches_the_binomial_sum():
    for k in range(1, 6):
        for n in (1, 2, 5, 14, 36, 100, 250):
            F = egg_table(k, n)
            for e in range(k + 1):
                for t in range(n + 1):
                    assert F[e][t] == min(n, sum(comb(t, i) for i in range(1, e + 1))), (k, n, e, t)
            assert min_drops(k, n) == q0039.min_drops(k, n)


def test_plan_never_exceeds_the_worst_case_and_ends_on_the_threshold():
    for k in range(1, 6):
        for n in (1, 2, 3, 7, 14, 36, 100, 137):
            t = min_drops(k, n)
            worst = 0
            for T in range(n + 1):
                drops = egg_run(k, n, T)
                assert drops == q0039.run(k, n, T)
                assert len(drops) <= t
                worst = max(worst, len(drops))
                low, high, eggs = 0, n + 1, k
                for fl, broke in drops:
                    assert low < fl < high and eggs >= 1
                    assert broke == (fl > T)
                    if broke:
                        high, eggs = fl, eggs - 1
                    else:
                        low = fl
                assert high == low + 1 and low == T
            assert worst == t                                           # the worst case is reached


def test_plan_is_optimal_on_small_cases():
    for k in range(1, 5):
        for n in range(1, 41):
            assert min_drops(k, n) == optimum(k, n), (k, n)


def test_tables():
    rows = q0039.covered_table().splitlines()[2:]
    assert len(rows) == 9 and rows[-1].endswith("| ‏9 | ‏45 | ‏**129** ✓ |")
    plan = q0039.plan_table().splitlines()[2:]
    assert [r.split("|")[2].strip().lstrip("‏") for r in plan] == ["37", "66", "88", "100"]
    answers = q0039.answers_table().splitlines()[2:]
    assert len(answers) == 10 and answers[2].endswith("| ‏9 | ‏19 |")
    ex = q0039.examples_table().splitlines()[2:]
    assert len(ex) == len(q0039.EXAMPLES)


def test_explorer_matches_the_page_code():
    from page_tests import explorer_require, node_json

    cases = [(3, 100), (2, 100), (1, 7), (3, 14), (4, 1000), (10, 1000), (2, 36), (5, 1)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({list(map(list, cases))}.map(([k, n]) => {{
        const used = m.eggsPerThreshold(k, n);
        return [m.eggsDrops(k, n), m.eggsRun(k, n, Math.min(36, n)), used, m.eggsFirst(k, n)];
      }})));""")
    for (k, n), (t, run, used, first) in zip(cases, got):
        assert t == min_drops(k, n)
        assert [[fl, broke] for fl, broke in egg_run(k, n, min(36, n))] == run
        assert used == q0039.drops_per_threshold(k, n)
        assert first == q0039.first_egg_floors(k, n)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(39)
