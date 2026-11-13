"""Question 0107: the page's largest_number, largest_brute and smallest_number (as published)
against the references of tools/figures/q0107.py (the sort by the exact rational a / (10^|a| - 1)
and the brute force over every order) on random lists, the page's examples and the edge cases
(all zeros, one number, equal numbers, ties like 12 and 1212, long inputs)."""

import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0107  # noqa: E402

ns = load_python(107)
largest_number, largest_brute, smallest_number = ns["largest_number"], ns["largest_brute"], ns["smallest_number"]
concat_order = ns["concat_order"]

# numbers whose strings are prefixes of each other, with zeros, ties and repeats: the hard cases
POOL = [0, 1, 2, 3, 9, 10, 11, 12, 20, 21, 30, 31, 34, 100, 101, 110, 121, 1001, 1010, 1212, 12121, 2121, 9, 99, 98, 989]


def lists(seed, count, nmax, pool=True, vmax=1000):
    rng = random.Random(seed)
    for _ in range(count):
        n = rng.randint(1, nmax)
        yield [rng.choice(POOL) if pool and rng.random() < 0.7 else rng.randint(0, vmax) for _ in range(n)]


def test_page_examples():
    assert largest_number([3, 30, 34, 5, 9]) == "9534330" == largest_brute([3, 30, 34, 5, 9])
    assert largest_number([3, 30]) == "330"
    assert largest_number([12, 1212]) == largest_number([1212, 12]) == "121212"
    assert largest_number([0, 0]) == largest_brute([0, 0]) == "0"
    for nums, want in [([0, 1, 10], "1001"), ([3, 30, 34, 5, 9], "3033459"), ([0, 0, 1], "100"), ([20, 1, 0], "1020"),
                       ([0, 2, 21], "2021"), ([0, 11, 1], "1011"), ([0, 1, 1001], "100101")]:
        assert smallest_number(nums) == want == q0107.smallest_brute(nums), nums


def test_edge_cases():
    for f in (largest_number, largest_brute, smallest_number):
        assert f([0]) == "0"
        assert f([7]) == "7"
        assert f([0, 0, 0]) == "0"
        assert f([5, 5, 5]) == "555"
        assert f([12, 1212]) == "121212"
    assert largest_number([10, 2]) == "210" and smallest_number([10, 2]) == "102"
    assert largest_number([2147483647, 2147483646]) == "21474836472147483646"
    assert smallest_number([0, 0, 0, 5]) == "5000"
    assert concat_order("3", "30") == -1 and concat_order("30", "3") == 1 and concat_order("12", "1212") == 0


def test_largest_on_random_lists():
    for nums in lists(1070, 3000, 7):
        want = q0107.largest(nums)
        assert largest_number(nums) == want, nums
        assert largest_brute(nums) == want, nums


def test_smallest_on_random_lists():
    for nums in lists(1071, 3000, 7):
        assert smallest_number(nums) == q0107.smallest_brute(nums), nums
    for nums in lists(1072, 3000, 30, vmax=10 ** 6):
        assert smallest_number(nums) == q0107.smallest(nums), nums


def test_long_inputs():
    rng = random.Random(1073)
    for _ in range(5):
        nums = [rng.randint(0, 2 ** 31 - 1) for _ in range(1000)] + [0] * 20 + [rng.choice(POOL) for _ in range(200)]
        rng.shuffle(nums)
        assert largest_number(nums) == q0107.largest(nums)
        assert smallest_number(nums) == q0107.smallest(nums)
    assert len(largest_number([999999999] * 500)) == 4500
