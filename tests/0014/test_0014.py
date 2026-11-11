import math
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


def test_explorer_matches_page_code():
    """The shapes explorer: its candidates and overlap test against the page's, every
    draw it makes accepted by shapes_ok and by the painting check, its rejection draw
    uniform among the free candidates, and its heat map consistent with its draws."""
    import json

    from page_tests import explorer_require, node_json

    rng = random.Random(14)
    pairs = [[[rng.randint(1, 9), rng.randint(1, 7), 0, 0] for _ in range(2)] for _ in range(300)]
    for p in pairs:
        for s in p:
            s[2], s[3] = s[0] + rng.randint(1, 10 - s[0]), s[1] + rng.randint(1, 8 - s[1])
    got = node_json(f"""
      const m = {explorer_require()};
      const rnd = (() => {{ let a = 14; return () => {{ a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }}; }})();   // mulberry32: exact in doubles
      const draws = [];
      for (const [N, M, mx, sq] of [[10, 8, 6, true], [10, 8, 6, false], [4, 4, 8, true], [3, 3, 4, false], [12, 10, 10, true]])
        for (let r = 0; r < 30; r++) draws.push([N, M, sq, m.shapesRandom(N, M, mx, sq, rnd)]);
      const tries = Array.from({{length: 200}}, () => m.shapesTry(10, 8, [[1, 1, 5, 5], [6, 2, 10, 6]], true, rnd));
      const heat = m.shapesHeat(10, 8, 6, true, 40, rnd);
      console.log(JSON.stringify({{
        counts: [m.shapesCandidates(10, 8, true).length, m.shapesCandidates(10, 8, false).length, m.shapesCandidates(4, 4, true).length],
        overlap: {json.dumps(pairs)}.map(([a, b]) => m.shapesOverlap(a, b)),
        draws, tries, heat,
        ok: [m.shapesOk(10, 8, [[1, 1, 3, 3], [3, 3, 5, 5]], true), m.shapesOk(10, 8, [[1, 1, 3, 3], [2, 2, 4, 4]], true), m.shapesOk(10, 8, [[1, 1, 3, 4]], true), m.shapesOk(10, 8, [[1, 1, 3, 4]], false)],
      }}));""")
    assert got["counts"] == [len(list(ns["candidates"](10, 8, True))), len(list(ns["candidates"](10, 8, False))), len(list(ns["candidates"](4, 4, True)))]
    assert got["counts"][:2] == [196, 1260]
    for (a, b), o in zip(pairs, got["overlap"]):
        assert o == ns["overlap"](tuple(a), tuple(b))
    assert got["ok"] == [True, False, False, True]
    for N, M, sq, shapes in got["draws"]:
        shapes = [tuple(s) for s in shapes]
        assert 1 <= len(shapes) and ns["shapes_ok"](N, M, shapes, sq) and painted_ok(N, M, shapes, sq)
    fixed = [(1, 1, 5, 5), (6, 2, 10, 6)]
    free = [c for c in ns["candidates"](10, 8, True) if not any(ns["overlap"](c, s) for s in fixed)]
    for t in got["tries"]:
        assert t["free"] == len(free) and t["all"] == 196
        assert tuple(t["shape"]) in free and tuple(t["tries"][-1]) == tuple(t["shape"])
        for c in t["tries"][:-1]:
            assert any(ns["overlap"](tuple(c), s) for s in fixed)
    h = got["heat"]
    assert h["rounds"] == 40 and sum(h["sides"]) == h["count"] and len(h["cells"]) == 7 and all(len(r) == 9 for r in h["cells"])
    assert sum(map(sum, h["cells"])) >= h["count"]            # every shape covers at least one cell


def test_explorer_four_cases():
    """The box's projections and sandbox: the four cases of "no overlap" (b left of, right
    of, below or above a) hold none exactly when the page's overlap() says the two
    rectangles overlap, on every pair of small rectangles."""
    import json

    from page_tests import explorer_require, node_json

    rects = [[x1, y1, x2, y2] for x1 in range(1, 5) for x2 in range(x1 + 1, 6) for y1 in range(1, 4) for y2 in range(y1 + 1, 5)]
    pairs = [[a, b] for a in rects[::3] for b in rects[::2]]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(pairs)}.map(([a, b]) => m.shapesWhy(a, b))));")
    for (a, b), w in zip(pairs, got):
        assert w["left"] == (b[2] <= a[0]) and w["right"] == (b[0] >= a[2])
        assert w["below"] == (b[3] <= a[1]) and w["above"] == (b[1] >= a[3])
        assert w["overlap"] == bool(overlap(tuple(a), tuple(b))) == (not (w["left"] or w["right"] or w["below"] or w["above"]))


def test_corner_check_fails_for_squares_too():
    """Part b's proof and the trap: the corner check is wrong already for squares. With
    "a corner strictly inside" it misses squares shifted along an edge (and equal ones);
    with "inside or on the boundary" it rejects squares that only touch. The cross of the
    box's preset overlaps with no corner inside."""
    sq = list(candidates(10, 8, True))

    def corners(s):
        return [(s[0], s[1]), (s[0], s[3]), (s[2], s[1]), (s[2], s[3])]

    def hit(a, b, closed):
        inside = (lambda p, s: s[0] <= p[0] <= s[2] and s[1] <= p[1] <= s[3]) if closed else \
                 (lambda p, s: s[0] < p[0] < s[2] and s[1] < p[1] < s[3])
        return any(inside(p, b) for p in corners(a)) or any(inside(p, a) for p in corners(b))

    missed = [(a, b) for a in sq for b in sq if a != b and overlap(a, b) and not hit(a, b, False)]
    wrong = [(a, b) for a in sq for b in sq if not overlap(a, b) and hit(a, b, True)]
    assert len(missed) == 668 and ((1, 1, 3, 3), (2, 1, 4, 3)) in missed
    assert overlap((1, 1, 3, 3), (1, 1, 3, 3)) and not hit((1, 1, 3, 3), (1, 1, 3, 3), False)
    assert len(wrong) == 7000 and ((1, 1, 2, 2), (1, 2, 2, 3)) in wrong
    cross = ((1, 3, 9, 5), (4, 1, 6, 7))
    assert overlap(*cross) and not hit(*cross, False)


def mean_restarts(N, M, squares):
    """The exact mean number of restarts of random_shapes when it draws n = (N-1)(M-1):
    every shape must then be a single cell, and one attempt succeeds with probability p,
    so the restarts are geometric with mean 1/p - 1."""
    from functools import lru_cache

    masks = [sum(1 << ((y - 1) * (N - 1) + x - 1) for x in range(x1, x2) for y in range(y1, y2))
             for x1, y1, x2, y2 in candidates(N, M, squares)]
    full, units = (1 << (N - 1) * (M - 1)) - 1, [k for k in masks if k & (k - 1) == 0]

    @lru_cache(None)
    def p(used):
        if used == full:
            return 1.0
        return sum(p(used | k) for k in units if not k & used) / sum(1 for k in masks if not k & used)
    return 1 / p(0) - 1


def test_restarts_in_a_dense_grid():
    """The costs: 20 squares on 5 x 6 points restart about 15 times on average, 10
    rectangles on 3 x 6 points about 475 times; a run of the page's own loop agrees."""
    assert round(mean_restarts(5, 6, True), 1) == 15.5
    assert round(mean_restarts(3, 6, False)) == 476 and 470 < mean_restarts(3, 6, False) < 480
    rng = random.Random(14)

    def restarts_once(N, M, n, squares):
        all_ = list(candidates(N, M, squares))
        for k in range(10 ** 6):
            shapes = []
            for _ in range(n):
                free = [c for c in all_ if not any(overlap(c, s) for s in shapes)]
                if not free:
                    break
                shapes.append(rng.choice(free))
            if len(shapes) == n:
                return k
    runs = [restarts_once(3, 6, 10, False) for _ in range(60)]
    assert 250 < sum(runs) / len(runs) < 800


def test_small_shapes_dominate():
    """The box's heat note: side 1 is about 48% of the drawn squares (10 x 8, up to 6),
    though only 63 of the 196 candidates."""
    rng = random.Random(15)
    tot = ones = 0
    for _ in range(1500):
        for x1, y1, x2, y2 in random_shapes(10, 8, 6, rng=rng):
            tot += 1
            ones += x2 - x1 == 1
    assert sum(1 for c in candidates(10, 8, True) if c[2] - c[0] == 1) == 63
    assert 0.44 < ones / tot < 0.51


def test_distribution_follow_up():
    """The follow-up on the distribution: 5 x 5 points, two squares. Of the 272 legal sets,
    those with a 3 x 3 square come out about 1.7 times as often as uniform, two unit
    squares far apart only 0.72 to 0.86 times (exact, with the restart when the 4 x 4
    square leaves no room)."""
    from fractions import Fraction

    all_ = list(candidates(5, 5, True))
    d = {}
    for a in all_:
        free = [c for c in all_ if not overlap(c, a)]
        for b in free:
            k = frozenset((a, b))
            d[k] = d.get(k, 0) + Fraction(1, len(all_)) / len(free)
    total = sum(d.values())
    ratio = {k: v / total * len(d) for k, v in d.items()}
    assert len(d) == 272 and total == Fraction(29, 30)
    big = [r for k, r in ratio.items() if any(s[2] - s[0] == 3 for s in k)]
    assert 1.69 < min(big) and max(big) < 1.74
    far = [r for k, r in ratio.items() if all(s[2] - s[0] == 1 for s in k)
           and max(abs(a - b) for a, b in zip(*[sorted(k)[0][:2], sorted(k)[1][:2]])) >= 2]
    assert round(float(min(far)), 2) == 0.72 and round(float(max(far)), 2) == 0.86


def test_gap_is_per_axis():
    """The follow-up on a gap: G added to each case is a gap of G on one axis at least,
    stricter than a straight-line distance G (axis gaps 3 and 3 give about 4.24)."""
    a, b, G = (1, 1, 2, 2), (5, 5, 6, 6), 4
    sep = b[0] >= a[2] + G or a[0] >= b[2] + G or b[1] >= a[3] + G or a[1] >= b[3] + G
    assert not sep and round(math.hypot(b[0] - a[2], b[1] - a[3]), 2) == 4.24


def test_explorer_restarts_and_cap():
    """The box: n is drawn from 1 to min(max, (N-1)(M-1)) (3 x 3 points hold 4 shapes, so
    max 10 draws at most 4), and a whole draw reports its restarts."""
    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      let a = 7; const rnd = () => {{ a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }};
      const runs = [];
      for (let k = 0; k < 60; k++) {{ const info = {{}}; const s = m.shapesRandom(3, 6, 10, false, rnd, info); runs.push([s, info.restarts]); }}
      const small = Array.from({{length: 200}}, () => m.shapesRandom(3, 3, 10, true, rnd).length);
      console.log(JSON.stringify({{ cap: [m.shapesMaxN(3, 3, 10), m.shapesMaxN(10, 8, 6)], runs, small }}));""")
    assert got["cap"] == [4, 6] and max(got["small"]) == 4 and min(got["small"]) == 1
    for shapes, r in got["runs"]:
        assert painted_ok(3, 6, [tuple(s) for s in shapes], False) and isinstance(r, int) and r >= 0
    assert max(r for s, r in got["runs"] if len(s) == 10) > 50
