import random

from extract_code import load_python

mystery = load_python(3)["mystery"]


def test_page_example():
    a = [3, 1, 4, 2]
    mystery(a)
    assert a == [1, 2, 3, 4]


def test_sorts_ascending():
    rng = random.Random(3)
    for _ in range(500):
        a = [rng.randint(-20, 20) for _ in range(rng.randint(0, 12))]
        expected = sorted(a)
        mystery(a)
        assert a == expected
