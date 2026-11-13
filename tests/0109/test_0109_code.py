"""Question 0109: the page's car_fleets and collision_times (as published) against the
references of tools/figures/q0109.py (the exact event-driven simulation) on random roads, the
page's examples and the edge cases (one car, the same speed, ties at the target, a car absorbed
before it is reached)."""

import random
import sys
from fractions import Fraction

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0109  # noqa: E402

ns = load_python(109)
car_fleets, collision_times = ns["car_fleets"], ns["collision_times"]
F = Fraction


def sim_fleets(target, pos, speed):
    return len(set(q0109.simulate(pos, speed, target)[1]))


def sim_times(pos, speed):
    return [-1 if c is None else c for c in q0109.simulate(pos, speed)[0]]


def test_page_examples():
    assert car_fleets(*q0109.EXAMPLE) == 3
    assert car_fleets(*q0109.TWO) == 1
    assert car_fleets(*q0109.THREE) == 1
    assert car_fleets(*q0109.FLOAT) == 1
    assert car_fleets(q0109.CHAIN_TARGET, *q0109.CHAIN) == 1
    assert collision_times(*q0109.CHAIN) == [2, 1, F(3, 2), -1]
    assert collision_times([1, 2, 4, 7], [2, 1, 3, 1]) == [1, -1, F(3, 2), -1]   # LeetCode 1776, example 1


def test_edge_cases():
    assert car_fleets(5, [0], [1]) == 1
    assert car_fleets(10, [0, 2, 4], [2, 2, 2]) == 3
    assert car_fleets(10, [4, 2, 0], [3, 4, 5]) == 1                 # all at the target at once
    assert car_fleets(12, [10, 8], [2, 4]) == 1                      # a tie at the target
    assert car_fleets(10, [0, 1], [3, 3]) == 2                       # 10 / 3 and 9 / 3 differ
    assert car_fleets(20, [0, 1], [2, 2]) == 2
    assert collision_times([0], [1]) == [-1]
    assert collision_times([0, 1, 2], [1, 1, 1]) == [-1, -1, -1]
    assert collision_times([0, 1, 2], [3, 2, 1]) == sim_times([0, 1, 2], [3, 2, 1])


def test_random_roads():
    rng = random.Random(1094)
    for _ in range(4000):
        n = rng.randint(1, 8)
        pos = rng.sample(range(25), n)
        speed = [rng.randint(1, 7) for _ in range(n)]
        target = max(pos) + rng.randint(1, 15)
        assert car_fleets(target, pos, speed) == sim_fleets(target, pos, speed), (target, pos, speed)
        pos = sorted(pos)
        assert collision_times(pos, speed) == sim_times(pos, speed), (pos, speed)
