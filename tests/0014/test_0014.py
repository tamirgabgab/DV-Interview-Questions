import random
import re
import subprocess
import sys

from extract_code import ROOT, load_python, question_path

ns = load_python(14)
overlap, candidates, shapes_ok = ns["overlap"], ns["candidates"], ns["shapes_ok"]
random_shapes, random_rectangles = ns["random_shapes"], ns["random_rectangles"]


def cells(s):
    """The unit cells a shape covers (cell (x, y) is the square from (x, y) to (x+1, y+1))."""
    x1, y1, x2, y2 = s
    return {(x, y) for x in range(x1, x2) for y in range(y1, y2)}


def painted_ok(N, M, shapes, squares):
    """Independent reference: every shape on the grid, no cell painted twice."""
    used = set()
    for x1, y1, x2, y2 in shapes:
        if not (1 <= x1 < x2 <= N and 1 <= y1 < y2 <= M):
            return False
        if squares and x2 - x1 != y2 - y1:
            return False
        c = cells((x1, y1, x2, y2))
        if used & c:
            return False
        used |= c
    return True


def touching(shapes):
    return sum(1 for k, a in enumerate(shapes) for b in shapes[:k]
               if min(a[2], b[2]) >= max(a[0], b[0]) and min(a[3], b[3]) >= max(a[1], b[1]))


def test_candidate_counts():
    # The numbers quoted on the page
    assert len(list(candidates(10, 8, True))) == 196
    assert len(list(candidates(10, 8, False))) == 1260


def test_overlap_every_pair():
    shapes = list(candidates(6, 5, False))
    for a in shapes:
        for b in shapes:
            assert overlap(a, b) == bool(cells(a) & cells(b)), (a, b)


def test_page_cases():
    a = (1, 1, 3, 3)
    assert not overlap(a, (4, 2, 6, 4))          # apart
    assert not overlap(a, (3, 1, 5, 3))          # shared edge
    assert not overlap(a, (3, 2, 6, 5))          # part of an edge
    assert not overlap(a, (3, 3, 5, 5))          # shared corner
    assert overlap((1, 1, 4, 4), (3, 2, 5, 4))   # overlap
    assert overlap((1, 1, 5, 5), (2, 2, 4, 4))   # one inside the other
    assert overlap((1, 4, 9, 6), (4, 1, 6, 8))   # the cross: no corner inside, still overlap


def test_checker_against_painting():
    rng = random.Random(14)
    for _ in range(20000):
        shapes = []
        for _ in range(rng.randint(1, 4)):
            x1, y1 = rng.randint(0, 6), rng.randint(0, 5)
            shapes.append((x1, y1, rng.randint(x1, 8), rng.randint(y1, 7)))   # may be illegal
        for squares in (True, False):
            assert shapes_ok(7, 6, shapes, squares) == painted_ok(7, 6, shapes, squares), shapes


def test_random_squares_and_rectangles():
    for squares in (True, False):
        seen, touch, non_square = set(), 0, 0
        for seed in range(400):
            rng = random.Random(seed)
            s = (random_shapes(10, 8, 6, squares=True, rng=rng) if squares
                 else random_rectangles(10, 8, 6, rng=rng))
            assert painted_ok(10, 8, s, squares) and shapes_ok(10, 8, s, squares), s
            seen.add(len(s))
            touch += touching(s)
            non_square += sum(x2 - x1 != y2 - y1 for x1, y1, x2, y2 in s)
        assert seen == {1, 2, 3, 4, 5, 6}
        assert touch > 0
        assert (non_square == 0) == squares


def test_dense_grid():
    # A full 3x3-point grid holds exactly 4 unit squares; asking for up to 4 always succeeds
    for seed in range(200):
        s = random_shapes(3, 3, 4, rng=random.Random(seed))
        assert painted_ok(3, 3, s, True)


def test_figures_up_to_date():
    # The SVG figures on the page are the output of tools/figures/q0014.py
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0014.py")],
                         capture_output=True, text=True, check=True).stdout
    generated = [line.strip() for line in out.splitlines() if line.strip().startswith("<svg")]
    page = re.findall(r'<svg class="figure".*?</svg>', question_path(14).read_text(encoding="utf-8"))
    assert page == generated
