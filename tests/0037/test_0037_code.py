"""Question 0037: the page's Python code (it runs as published) against the generator's
reference: edit_distance, diff with both rules for ties, edit_distance_within for every d,
and edit_distance_swaps, on the page's examples and random streams."""

import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0037  # noqa: E402

ns = load_python(37)


def test_examples():
    assert ns["edit_distance"]("ABCDEFGH", "ABDEYGHH") == 3
    assert ns["diff"]("ABCDEFGH", "ABDEYGHH") == [("missing", "C", None), ("changed", "F", "Y"), ("extra", None, "H")]
    assert ns["diff"]("ABCDEF", "ABDXEF") == [("missing", "C", None), ("extra", None, "X")]
    assert ns["diff"]("ABCDEF", "ABDXEF", "changed") == [("changed", "C", "D"), ("changed", "D", "X")]
    assert ns["edit_distance_within"]("ABCDEFGHIJKL", "ABCEFGHIXJKL", 2) == 2
    assert ns["edit_distance_within"]("ABCDEFGHIJKL", "ABCEFGHIXJKL", 1) is None
    assert ns["edit_distance_within"]("ABC", "ABCDEF", 2) is None
    assert ns["edit_distance_swaps"]("ABCDEFGH", "ABDCEFHG") == 2 and ns["edit_distance"]("ABCDEFGH", "ABDCEFHG") == 4
    assert ns["edit_distance_swaps"]("CA", "ABC") == 3
    # the trap of the page: row and column 0 left at 0
    assert ns["edit_distance"]("AB", "XAB") == 1 and ns["edit_distance"]("ABC", "") == 3


def test_random():
    rng = random.Random(2)
    for _ in range(1500):
        a = "".join(rng.choice("ABCD") for _ in range(rng.randint(0, 9)))
        b = "".join(rng.choice("ABCD") for _ in range(rng.randint(0, 9)))
        dist = q0037.distance(a, b)
        assert ns["edit_distance"](a, b) == dist
        for prefer in ("gaps", "changed"):
            assert ns["diff"](a, b, prefer) == q0037.report(a, b, prefer)
        for d in range(0, 10):
            assert ns["edit_distance_within"](a, b, d) == (dist if dist <= d else None)
        assert ns["edit_distance_swaps"](a, b) == q0037.distance(a, b, swap=True)
    # long streams with a few differences: the band against the full table
    for _ in range(20):
        a = "".join(rng.choice("ABCDEFGH") for _ in range(400))
        b = list(a)
        for _ in range(rng.randint(0, 5)):
            k = rng.randrange(len(b))
            rng.choice([lambda: b.pop(k), lambda: b.insert(k, "Z"), lambda: b.__setitem__(k, "Y")])()
        b = "".join(b)
        dist = ns["edit_distance"](a, b)
        assert ns["edit_distance_within"](a, b, 5) == (dist if dist <= 5 else None)
