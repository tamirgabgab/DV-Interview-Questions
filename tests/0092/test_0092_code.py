"""Question 0092: the page's Python code (it runs as published) against the generator's
reference: regions_by_chords and the formula for n up to 14, euler_regions, and
count_regions on random points, on the regular polygons and on the figures' points."""

import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0092  # noqa: E402

ns = load_python(92)
crosses, regions_by_chords = ns["crosses"], ns["regions_by_chords"]
regions, euler_regions, count_regions = ns["regions"], ns["euler_regions"], ns["count_regions"]


def test_counting():
    for n in range(0, 15):
        assert regions_by_chords(n) == regions(n) == euler_regions(n) == q0092.moser(n), n
    assert regions_by_chords(5) == 16 and regions(6) == 31
    for a, b, c, d in [(0, 2, 1, 3), (0, 2, 1, 2), (0, 3, 1, 2), (1, 3, 0, 2), (0, 1, 2, 3)]:
        assert crosses(a, b, c, d) == q0092.crosses(a, b, c, d)


def test_count_regions():
    rnd = random.Random(920)
    for n in range(0, 11):
        for _ in range(3):
            a = [rnd.uniform(0, 360) for _ in range(n)]
            assert count_regions(a) == q0092.regions(a), (n, a)
    for n in range(1, 13):
        a = [90 + 360 * k / n for k in range(n)]
        assert count_regions(a) == q0092.regions(a), n
    assert count_regions(q0092.REG6) == 30 and count_regions(q0092.N6) == 31 and count_regions(q0092.N5) == 16
