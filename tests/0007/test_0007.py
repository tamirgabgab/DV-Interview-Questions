import itertools
import math
import random
from fractions import Fraction
from math import comb

from extract_code import load_python

ns = load_python(7)


def test_generated_triangles_contain_center():
    random.seed(7)
    for _ in range(5000):
        assert ns["center_inside"](ns["random_triangle_with_center"]())


def test_gap_rule_matches_cross_product():
    rng = random.Random(1)
    for _ in range(20000):
        angles = [rng.uniform(0, 2 * math.pi) for _ in range(3)]
        points = [(math.cos(t), math.sin(t)) for t in angles]
        assert ns["contains_center"](angles) == ns["center_inside"](points)


def test_continuous_probability_is_a_quarter():
    rng = random.Random(2)
    n = 40000
    hits = sum(ns["contains_center"]([rng.uniform(0, 2 * math.pi) for _ in range(3)]) for _ in range(n))
    assert abs(hits / n - 0.25) < 0.01


def p_formula(m):
    return Fraction(m + 1, 4 * (m - 2)) if m % 2 else Fraction(m - 4, 4 * (m - 1))


def test_discrete_formula():
    # Brute-force count of triangles whose arcs are all shorter than half a circle.
    for m in range(3, 41):
        good = sum(all(2 * g < m for g in (b - a, c - b, m - (c - a)))
                   for a, b, c in itertools.combinations(range(m), 3))
        assert good == comb(m, 3) - m * comb(m // 2, 2)
        assert Fraction(good, comb(m, 3)) == p_formula(m)
    assert p_formula(360) == Fraction(89, 359)


def test_generator_formula_and_examples():
    import sys

    from extract_code import ROOT

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import q0007

    assert all(q0007.p_formula(m) == p_formula(m) for m in range(3, 41))
    for angles, inside in q0007.EXAMPLES:
        gaps = [(angles[(i + 1) % 3] - angles[i]) % 360 for i in range(3)]
        assert (max(gaps) < 180) == inside
    a1, a2, a3 = q0007.HALF_POINTS
    assert 0 < (a2 - a1) % 360 < 180 and 0 < (a3 - a1) % 360 < 180   # P2, P3 in the half circle from P1


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(7)
