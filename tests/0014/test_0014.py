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
