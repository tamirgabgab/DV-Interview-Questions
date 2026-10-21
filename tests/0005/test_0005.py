from extract_code import load_python

ns = load_python(5)
bfs, enum = ns["smallest_01_multiple"], ns["by_enumeration"]


def test_page_examples():
    assert bfs(7) == "1001"
    assert bfs(9) == "111111111"
    assert bfs(1) == "1"
    assert len(bfs(9999)) == 36


def test_bfs_is_a_01_multiple():
    for x in range(1, 2000):
        y = bfs(x)
        assert set(y) <= {"0", "1"} and y[0] == "1" and int(y) % x == 0, x


def test_bfs_is_minimal():
    # The enumeration is minimal by construction; compare where it is fast enough.
    for x in range(1, 300):
        y = bfs(x)
        if len(y) <= 16:
            assert y == enum(x), x


def test_chart_steps_match_page_code():
    """The step counts behind the chart: the generator's BFS equals the page code, and the
    other two counts follow from the answer (y / x multiples, y read as binary)."""
    import sys

    from extract_code import ROOT

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import q0005

    for x in q0005.XS:
        y = bfs(x)
        assert q0005.smallest_01_multiple(x)[0] == y
        assert q0005.steps(x)[:2] == (int(y) // x, int(y, 2))
    assert [q0005.steps(x)[2] for x in q0005.XS] == [4, 8, 89, 899, 8999]   # the page table


def test_explorer_digit_sets():
    """The box's follow-ups: with another digit set (3 and 7) the BFS finds the smallest
    multiple over those digits, or reports none when the queue empties (an even x with
    odd digits); the enumerated count is the answer's rank among the numbers over the
    set, and the layer of every remainder is the length of its number."""
    import json
    from itertools import product

    from page_tests import explorer_require, node_json

    def rank(x, digits, y):
        """y's place among the numbers over the digit set in increasing order, checking
        that no smaller one is a multiple of x."""
        count = 0
        for length in range(1, len(y) + 1):
            for tup in product(digits, repeat=length):
                if tup[0] == 0:
                    continue
                count += 1
                n = int("".join(map(str, tup)))
                if n % x == 0:
                    assert str(n) == y, (x, digits, n, y)
                    return count
        raise AssertionError((x, digits, y))

    def reachable(x, digits):
        """The remainders a number over the digit set can have (closed under appending)."""
        seen = {d % x for d in digits if d > 0}
        frontier = set(seen)
        while frontier:
            nxt = {(r * 10 + d) % x for r in frontier for d in digits} - seen
            seen |= nxt
            frontier = nxt
        return seen

    sets = [[3, 7], [1, 2], [4, 7], [0, 1], [1, 8, 9], [0, 5]]
    cases = [[x, ds] for ds in sets for x in range(1, 41)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([x, ds]) => {{ const t = m.bfs01Trace(x, ds); const c = m.bfs01Counts(x, ds);
        return [t.answer, c.enumerated, c.multiples, t.depth, t.path, t.starts, t.frames.length]; }})));""")
    for (x, ds), (answer, enumerated, multiples, depth, path, starts, frames) in zip(cases, got):
        if answer is None:
            assert 0 not in reachable(x, ds) and enumerated is None and path == [], (x, ds)
            continue
        assert 0 in reachable(x, ds) and int(answer) % x == 0 and set(map(int, answer)) <= set(ds), (x, ds, answer)
        assert int(enumerated) == rank(x, ds, answer) and int(multiples) == int(answer) // x, (x, ds)
        assert depth[0] == len(answer) and len(path) == len(answer)
        assert starts == sorted({d % x for d in ds if d > 0}, key=lambda r: [d for d in ds if d > 0 and d % x == r][0])
        assert all(depth[r] == i + 1 for i, r in enumerate(path))


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(5)


def test_explorer_matches_page_code():
    """The remainders explorer: every frame of its BFS against a replay of the page's loop
    (the remainder dequeued, the fate of each child, the queue), its answer against the
    page function, and its three counts against the generator's steps()."""
    import json
    import sys
    from collections import deque

    from extract_code import ROOT
    from page_tests import explorer_require, node_json

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import q0005

    xs = list(range(1, 41)) + [99, 999]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(xs)}.map((x) => [m.bfs01Trace(x), m.bfs01Counts(x)])));""")
    for x, (tr, counts) in zip(xs, got):
        y = bfs(x)
        assert tr["answer"] == y == counts["answer"]
        assert (int(counts["multiples"]), int(counts["enumerated"]), counts["dequeues"]) == q0005.steps(x)
        # the replay of the page's loop, frame by frame
        parent, digit, visited = [-1] * x, [""] * x, [False] * x
        start = 1 % x
        visited[start], digit[start] = True, "1"
        queue, frames = deque([start]), []
        while not visited[0]:
            r = queue.popleft()
            kids = []
            for d in (0, 1):
                nr = (r * 10 + d) % x
                if not visited[nr]:
                    visited[nr], parent[nr], digit[nr] = True, r, str(d)
                    queue.append(nr)
                    kids.append({"d": d, "nr": nr, "status": "found" if nr == 0 else "new"})
                else:
                    kids.append({"d": d, "nr": nr, "status": "seen"})
            number, q = "", r
            while q != -1:
                number, q = digit[q] + number, parent[q]
            frames.append({"r": r, "number": number, "kids": kids, "queue": list(queue)})
        assert tr["frames"] == frames and tr["dequeues"] == len(frames)
        path, q = [], 0
        while q != -1:
            path.insert(0, q)
            q = parent[q]
        assert tr["path"] == path and tr["start"] == start
        assert tr["parent"] == parent and tr["digit"] == digit
        assert "".join(digit[r] for r in path) == y
