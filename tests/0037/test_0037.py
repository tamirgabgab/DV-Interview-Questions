"""Question 0037, the edit distance between two streams: the numbers the page states,
recomputed from the reference in tools/figures/q0037.py (the table, and a search over the
strings one edit apart that does not use it); every report rebuilds the actual stream and has
as many lines as the distance; the band of part c against the full table; the generated
blocks; the box's models under Node against the same reference."""

import json
import random
import sys

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0037  # noqa: E402


def streams(rng, n=400, letters="ABCD", top=6):
    for _ in range(n):
        yield ("".join(rng.choice(letters) for _ in range(rng.randint(0, top))),
               "".join(rng.choice(letters) for _ in range(rng.randint(0, top))))


def test_table_against_the_search():
    rng = random.Random(37)
    for a, b in streams(rng, 600, "ABC", 5):
        assert q0037.distance(a, b) == q0037.bfs(a, b), (a, b)
        # the swaps of part d: never above the plain distance, never below unrestricted Damerau
        assert q0037.bfs(a, b, True) <= q0037.distance(a, b, True) <= q0037.distance(a, b)


def test_reports_rebuild_the_stream():
    rng = random.Random(1)
    for a, b in streams(rng, 800):
        for swap in (False, True):
            dist = q0037.distance(a, b, swap)
            for prefer in ("gaps", "changed"):
                path = q0037.walk(a, b, prefer, swap)
                assert q0037.apply(a, b, path) == b
                assert sum(k != "same" for k, _, _ in path) == dist == len(q0037.report(a, b, prefer, swap))


def test_part_a_numbers():
    assert q0037.distance("ABCDEFGH", "ABDEYGHH") == 3
    assert sum(x != y for x, y in zip("ABCDEFGH", "ABDEYGHH")) == 5
    # two changes in place of C and F give neither stream
    assert {"ABCDEFGH".replace("C", x).replace("F", y) for x, y in ("YH", "HY")} == {"ABYDEHGH", "ABHDEYGH"}
    # neighbouring cells differ by at most 1, and d[i][j] >= |i - j|
    rng = random.Random(5)
    for a, b in streams(rng, 200):
        d = q0037.table(a, b)
        for i in range(len(a) + 1):
            for j in range(len(b) + 1):
                assert d[i][j] >= abs(i - j)
                if i:
                    assert abs(d[i][j] - d[i - 1][j]) <= 1
                if j:
                    assert abs(d[i][j] - d[i][j - 1]) <= 1
                if i and j and a[i - 1] == b[j - 1]:
                    assert d[i][j] == d[i - 1][j - 1]


def test_part_b_numbers():
    assert q0037.report("ABCDEFGH", "ABDEYGHH") == [("missing", "C", None), ("changed", "F", "Y"), ("extra", None, "H")]
    assert q0037.report("ABCDEF", "ABDXEF", "gaps") == [("missing", "C", None), ("extra", None, "X")]
    assert q0037.report("ABCDEF", "ABDXEF", "changed") == [("changed", "C", "D"), ("changed", "D", "X")]
    # the positions of the lines: the extra H is the one at actual position 7, not 8
    assert q0037.report_at("ABCDEFGH", "ABDEYGHH") == [("missing", "C", None, 3, 2), ("changed", "F", "Y", 6, 5), ("extra", None, "H", 7, 7)]
    # the tie at cell (4, 4), D against X: the left and the diagonal neighbours give 1, up gives 2
    d = q0037.table("ABCDEF", "ABDXEF")
    assert d[4][4] == 2 and d[4][3] == 1 and d[3][3] == 1 and d[3][4] == 2


def test_part_c_numbers():
    a, b = q0037.BAND_A, q0037.BAND_B
    # the memory of the cost: the band of two streams of a million packets with d = 10, about
    # 21 million cells of a byte (values up to d + 1)
    assert round(q0037.band_cells(10**6, 10) / 1e6) == 21 and 10 + 1 < 256
    assert q0037.within(a, b, 2) == 2 and q0037.within(a, b, 1) is None and q0037.distance(a, b) == 2
    assert q0037.band_cells(12, 2) == 54 and q0037.band_cells(1000, 3) == 6988 and q0037.band_cells(10**6, 10) == 20999890
    rng = random.Random(3)
    for x, y in streams(rng, 1500, "ABC", 8):
        for dd in range(0, 9):
            dist = q0037.distance(x, y)
            assert q0037.within(x, y, dd) == (dist if dist <= dd else None), (x, y, dd)


def test_part_c_report_inside_the_band():
    # the cost of part c: a report needs only the band, since walking back from the corner
    # with the band's values (a cell outside it counted as d + 1) gives part b's report
    def band_walk(a, b, d, prefer):
        big, t = d + 1, {}
        for i in range(len(a) + 1):
            for j in range(max(0, i - d), min(len(b), i + d) + 1):
                if i == 0 or j == 0:
                    t[i, j] = i + j
                else:
                    t[i, j] = min(t.get((i - 1, j), big) + 1, t.get((i, j - 1), big) + 1,
                                  t.get((i - 1, j - 1), big) + (a[i - 1] != b[j - 1]))
        g = lambda i, j: t.get((i, j), big)  # noqa: E731
        moves = [("missing", 1, 0), ("extra", 0, 1), ("changed", 1, 1)]
        if prefer == "changed":
            moves = moves[2:] + moves[:2]
        i, j, out = len(a), len(b), []
        while i or j:
            if i and j and a[i - 1] == b[j - 1] and g(i, j) == g(i - 1, j - 1):
                i, j = i - 1, j - 1
                continue
            kind, di, dj = next(mv for mv in moves if i >= mv[1] and j >= mv[2] and g(i, j) == g(i - mv[1], j - mv[2]) + 1)
            out.append((kind, i, j))
            i, j = i - di, j - dj
        return out[::-1]

    rng = random.Random(4)
    for a, b in streams(rng, 1500, "ABC", 8):
        dist = q0037.distance(a, b)
        for d in range(dist, 9):
            for prefer in ("gaps", "changed"):
                assert band_walk(a, b, d, prefer) == [s for s in q0037.walk(a, b, prefer) if s[0] != "same"], (a, b, d)


def test_part_d_numbers():
    assert q0037.distance("ABCDEFGH", "ABDCEFHG") == 4 and q0037.distance("ABCDEFGH", "ABDCEFHG", True) == 2
    assert q0037.report("ABCDEFGH", "ABDCEFHG", swap=True) == [("swapped", "CD", "DC"), ("swapped", "GH", "HG")]
    assert q0037.distance("ABCDEF", "ABDCEF", True) == 1 and q0037.distance("ABCD", "BCDA", True) == 2
    d = q0037.table("ABCDEFGH", "ABDCEFHG", True)
    assert d[4][4] == 1 and d[6][6] == 1 and d[8][8] == 2
    # the trap: CA and ABC, 3 with each packet edited once, 2 by unrestricted Damerau
    assert q0037.distance("CA", "ABC", True) == 3 and q0037.bfs("CA", "ABC", True) == 2


def test_follow_ups():
    # only missing and extra: m + n - 2 LCS
    def lcs(a, b):
        t = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
        for i in range(len(a)):
            for j in range(len(b)):
                t[i + 1][j + 1] = t[i][j] + 1 if a[i] == b[j] else max(t[i][j + 1], t[i + 1][j])
        return t[-1][-1]
    assert lcs("ABCDEFGH", "ABDEYGHH") == 6 == len("ABDEGH") and 8 + 8 - 2 * 6 == 4
    rng = random.Random(9)
    for a, b in streams(rng, 300, "ABC", 5):
        # with a change costing 2 the table gives m + n - 2 LCS
        d = [[i + j if i == 0 or j == 0 else 0 for j in range(len(b) + 1)] for i in range(len(a) + 1)]
        for i in range(1, len(a) + 1):
            for j in range(1, len(b) + 1):
                d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + 2 * (a[i - 1] != b[j - 1]))
        assert d[-1][-1] == len(a) + len(b) - 2 * lcs(a, b)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(37)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(11)
    cases = [[a, b, p, s] for a, b in streams(rng, 150, "ABCD", 9) for p, s in (("gaps", False), ("changed", True)) if a and b]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(cases)}.map(([a, b, p, s]) => [m.edTable(a, b, s), m.edWalk(a, b, p, s), m.edReport(a, b, p, s)])));")
    for (a, b, p, s), (tab, path, rep) in zip(cases, got):
        assert tab == q0037.table(a, b, s)
        assert [tuple(x) for x in path] == q0037.walk(a, b, p, s)
        assert [tuple(x) for x in rep] == q0037.report(a, b, p, s)
    parsed = node_json(f"const m = {explorer_require()};"
                       "console.log(JSON.stringify(['abc', 'A B C', 'ABCDEFGHIJKL', 'ABCDEFGHIJKLM', '', 'AB1', 'אב'].map(m.edParse)));")
    assert parsed == ["ABC", "ABC", "ABCDEFGHIJKL", None, None, None, None]
