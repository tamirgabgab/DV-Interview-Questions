"""Question 0030: the page's Python code (the periodic strip, as published) against the
independent reference of reference.py: the distance and the exit point on a grid of
positions and on random boxes, the worked numbers of the page, and the edge cases (a point
on an edge or a corner, a very short or very flat box)."""

import math
import random
import sys
from pathlib import Path

from extract_code import load_python

sys.path.insert(0, str(Path(__file__).resolve().parent))
import reference  # noqa: E402

ns = load_python(30)
shortest_path, edge_images, edge_point = ns["shortest_path"], ns["edge_images"], ns["edge_point"]


def check(a, b, h, y0, z0, y1, z1):
    d, exit_pt = shortest_path(a, b, h, y0, z0, y1, z1)
    best, seqs, exits = reference.shortest(a, b, h, y0, z0, y1, z1)
    assert math.isclose(d, best, abs_tol=1e-7), (a, b, h, y0, z0, y1, z1, d, best)
    assert exit_pt[0] == 0
    assert any(math.dist(exit_pt, e) < 1e-6 for e in exits), (a, b, h, y0, z0, y1, z1, exit_pt, exits)
    on_edge = any(math.isclose(exit_pt[1], v, abs_tol=1e-9) for v in (0, b)) or \
        any(math.isclose(exit_pt[2], v, abs_tol=1e-9) for v in (0, h))
    assert on_edge and -1e-9 <= exit_pt[1] <= b + 1e-9 and -1e-9 <= exit_pt[2] <= h + 1e-9
    assert d >= math.hypot(a, y1 - y0, z1 - z0) - 1e-9      # never shorter than through the air
    return d, exit_pt


def test_page_example():
    d, exit_pt = shortest_path(30, 12, 12, 6, 11, 6, 1)
    assert math.isclose(d, 40) and exit_pt == (0, 6.75, 12)
    assert math.isclose(shortest_path(30, 12, 12, 6, 6, 6, 6)[0], 42)
    assert math.isclose(shortest_path(30, 12, 12, 6, 11, 6, 6)[0], 37)
    assert math.isclose(shortest_path(1, 1, 1, 0.5, 0.5, 0.5, 0.5)[0], 2)
    # the mirror image of the example: the exit point mirrors too
    d, exit_pt = shortest_path(30, 12, 12, 6, 1, 6, 11)
    assert math.isclose(d, 40) and exit_pt == (0, 5.25, 0)


def test_images_and_edge_points():
    imgs = {e: (d, p, lo, hi) for e, d, p, lo, hi in edge_images(6, 11, 12, 12)}
    assert imgs == {"bottom": (11, 6, 0, 12), "sideB": (6, 23, 12, 24), "top": (1, 30, 24, 36), "side0": (6, 37, 36, 48)}
    for edge, d, p, lo, hi in edge_images(6, 11, 12, 12):
        assert lo <= p <= hi
        assert edge_point(edge, p, 12, 12) in ((6, 0.0), (12, 11), (6, 12), (0.0, 11))
    assert edge_point("top", 29.25, 12, 12) == (6.75, 12)


def test_grid():
    for y0 in (0, 3, 6, 9, 12):
        for z0 in (0, 1, 6, 11, 12):
            for y1 in (0, 6, 12):
                for z1 in (0, 1, 6, 12):
                    check(30, 12, 12, y0, z0, y1, z1)


def test_random_boxes():
    rng = random.Random(3030)
    for _ in range(400):
        a, b, h = rng.choice([1, 2, 5, 10, 30, 100]), rng.choice([1, 3, 7, 12, 20]), rng.choice([1, 2, 6, 12, 25])
        check(a, b, h, rng.uniform(0, b), rng.uniform(0, h), rng.uniform(0, b), rng.uniform(0, h))


def test_corners_and_flat_boxes():
    check(30, 12, 12, 0, 0, 12, 12)          # corner to opposite corner
    check(30, 12, 12, 0, 12, 12, 0)
    check(30, 12, 12, 12, 11, 0, 1)
    check(0.5, 12, 12, 6, 11, 6, 1)          # a very short box: around the side is better
    check(30, 0.5, 12, 0.25, 11, 0.25, 1)    # a thin wall
    check(30, 12, 0.5, 6, 0.25, 6, 0.25)     # a flat box
