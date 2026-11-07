"""Question 0100: the page's Python code (it runs as published) against the generator's
reference: count_ways and list_ways, count_ways_broken, count_multisets and count_ways_exact
on every small case and random ones."""

import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0100  # noqa: E402

ns = load_python(100)


def test_examples():
    assert ns["count_ways"](10, [1, 2]) == 89 and ns["count_ways"](10, {1, 2, 3}) == 274
    assert ns["count_ways_broken"](10, [1, 2], [5]) == 25 and ns["count_ways_broken"](10, [1, 2], [5, 6]) == 0
    assert ns["count_multisets"](10, [1, 2]) == 6 and ns["count_multisets"](10, [3, 1, 2]) == 14
    assert ns["count_ways_exact"](10, [1, 2], 7) == 35
    assert ns["list_ways"](3, [1, 2]) == [[1, 1, 1], [1, 2], [2, 1]]
    assert ns["count_ways"](0, [1, 2]) == 1 and ns["count_multisets"](0, [2]) == 1


def test_random():
    rng = random.Random(1)
    for _ in range(400):
        steps = rng.sample(range(1, 8), rng.randint(1, 4))
        n = rng.randint(0, 14)
        broken = [b for b in range(1, n + 1) if rng.random() < 0.2]
        assert ns["count_ways"](n, steps) == q0100.ways(n, steps)
        assert len(ns["list_ways"](n, steps)) == q0100.ways(n, steps)
        assert sorted(map(tuple, ns["list_ways"](n, steps))) == q0100.climbs(n, steps)
        assert ns["count_ways_broken"](n, steps, broken) == q0100.ways(n, steps, broken)
        assert ns["count_ways_broken"](n, steps) == ns["count_ways"](n, steps)
        assert ns["count_multisets"](n, steps) == len(q0100.multisets(n, steps))
        t = rng.randint(0, n + 1)
        assert ns["count_ways_exact"](n, steps, t) == q0100.exact(n, steps, t)
    # big n: exact integers
    assert ns["count_ways"](200, [1, 2]) == q0100.table(200, (1, 2))[200]
