"""Question 0031: the page's Python code (the Dijkstra, as published) against brute force,
the greedy rule and the generator; the crossings it returns replay to its time."""

import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
sys.path.insert(0, str(ROOT / "tests" / "0031"))
import q0031  # noqa: E402
from test_0031 import brute  # noqa: E402

bridge = load_python(31)["bridge"]


def test_page_example():
    total, moves = bridge([1, 2, 5, 10])
    assert total == 17 and q0031.replay([1, 2, 5, 10], moves) == 17
    assert sorted(moves[2]) == [2, 3] and len(moves) == 5           # C and D cross together
    assert bridge([1, 2, 5, 10, 20])[0] == 33
    assert bridge([1, 2, 3, 4])[0] == 11
    assert bridge([4])[0] == 4 and bridge([4, 9])[0] == 9 and bridge([1, 5, 8])[0] == 14


def test_random_sets():
    rng = random.Random(1331)
    for _ in range(120):
        ts = [rng.randint(1, 12) for _ in range(rng.randint(1, 5))]
        total, moves = bridge(ts)
        assert total == brute(ts) and q0031.replay(ts, moves) == total, ts
    for _ in range(300):
        ts = [rng.randint(1, 40) for _ in range(rng.randint(1, 8))]
        total, moves = bridge(ts)
        assert total == q0031.greedy(ts) and q0031.replay(ts, moves) == total, ts
        assert len(moves) == 2 * len(ts) - 3 or len(ts) < 3
