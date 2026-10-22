from extract_code import load_python

ns = load_python(5)
bfs, enum = ns["smallest_01_multiple"], ns["by_enumeration"]
ab, has_ab = ns["smallest_ab_multiple"], ns["has_ab_solution"]
PAIRS = [(a, b) for a in range(10) for b in range(a + 1, 10)]


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


def test_ab_page_examples():
    """The example table of the two-digit follow-up."""
    table = [(7, 0, 1, "1001"), (13, 3, 7, "377"), (9999, 3, 7, "3" * 12), (28, 1, 2, "112"),
             (75, 5, 7, "75"), (2, 3, 7, None), (4, 2, 6, None), (125, 2, 5, None)]
    for x, a, b, y in table:
        assert ab(x, a, b) == y and has_ab(x, a, b) == (y is not None), (x, a, b)
    assert len("3" * 12) == 12 and len(bfs(9999)) == 36


def test_ab_generalises_01():
    for x in range(1, 2000):
        assert ab(x, 0, 1) == bfs(x), x


def test_ab_search_agrees_with_the_theorem():
    """For every pair a < b and x < 1500: a multiple exists exactly when has_ab_solution says
    so, it is built from a and b, it does not start with 0, and it has at most x digits."""
    for a, b in PAIRS:
        for x in range(1, 1500):
            y = ab(x, a, b)
            assert (y is not None) == has_ab(x, a, b), (x, a, b)
            if y is not None:
                assert set(y) <= {str(a), str(b)} and y[0] != "0" and int(y) % x == 0, (x, a, b, y)
                assert len(y) <= x, (x, a, b)


def test_ab_is_minimal():
    """Against an enumeration of the numbers over {a, b} in increasing order."""
    from itertools import product

    def smallest(x, a, b, limit):
        for length in range(1, limit + 1):
            for tup in product((a, b), repeat=length):
                if tup[0] and int("".join(map(str, tup))) % x == 0:
                    return "".join(map(str, tup))
        return None

    for a, b in PAIRS:
        for x in range(1, 120):
            y = ab(x, a, b)
            if y is None:
                assert smallest(x, a, b, 10) is None, (x, a, b)
            elif len(y) <= 12:
                assert smallest(x, a, b, len(y)) == y, (x, a, b)


def test_ab_proof_steps():
    """The facts the proof uses, recomputed."""
    from itertools import product

    # step 3: the page's example of repeating a block
    assert 12 % 4 == 0 and 121212 == 28 * 4329 and 1212 % 7 != 0 and ab(28, 1, 2) == "112"
    # step 3: R_i - R_j = 10^(jL) R_(i-j)
    R = lambda k, L: sum(10 ** (n * L) for n in range(k))
    assert all(R(i, L) - R(j, L) == 10 ** (j * L) * R(i - j, L) for L in range(1, 4) for i in range(2, 8) for j in range(1, i))
    # step 5: mixed parity reaches every power of 2 with as many digits; {2, 6} stops at 2^1
    for a, b in PAIRS:
        if a and a % 2 != b % 2:
            for n in range(1, 13):
                assert any(int("".join(t)) % 2 ** n == 0 for t in product(str(a) + str(b), repeat=n)), (a, b, n)
    even = [(a, b) for a, b in PAIRS if a and a % 2 == 0 and b % 2 == 0]
    assert len(even) == 6 and [p for p in even if not has_ab(2 ** 10, *p)] == [(2, 6)]
    assert has_ab(2, 2, 6) and not has_ab(4, 2, 6)
    # step 6: the endings of multiples of 25 and 125 without the digit 0
    assert [e for e in range(100) if e % 25 == 0 and "0" not in f"{e:02d}"] == [25, 75]
    assert [e for e in range(1000) if e % 125 == 0 and "0" not in f"{e:03d}"] == [125, 375, 625, 875]
    assert all(len(set(str(e))) == 3 for e in (125, 375, 625, 875))
    # the conclusion: only the nine pairs with 0 work for every x; x = 10 already fails the rest
    assert [p for p in PAIRS if all(has_ab(x, *p) for x in range(1, 1000))] == [(0, b) for b in range(1, 10)]
    assert all(not has_ab(10, a, b) for a, b in PAIRS if a)


def test_explorer_ab_map():
    """The map of the pairs: the box's BFS and existence check against the page functions,
    and the rule it names against the case of the theorem."""
    import json

    from page_tests import explorer_require, node_json

    xs = list(range(1, 130)) + [256, 625, 1000, 2048, 3125, 9999]
    got = node_json(f"""
      const m = {explorer_require()};
      const out = [];
      for (const x of {json.dumps(xs)}) for (let a = 0; a <= 8; a++) for (let b = a + 1; b <= 9; b++) {{
        const r = m.abMultiple(x, a, b), e = m.abExists(x, a, b);
        out.push([x, a, b, r.answer, e.ok, e.rule, e.s, e.t, e.m]);
      }}
      console.log(JSON.stringify(out));""")
    rules = {"zero", "coprime", "ten", "no5", "five", "twentyfive", "no25", "no125", "mixed", "halved", "odd"}
    for x, a, b, answer, ok, rule, s, t, m in got:
        assert answer == ab(x, a, b) and ok == has_ab(x, a, b), (x, a, b)
        assert 2 ** s * 5 ** t * m == x and m % 2 and m % 5 and rule in rules, (x, a, b)
        assert ok == (rule in {"zero", "coprime", "five", "twentyfive", "mixed", "halved"}), (x, a, b, rule)
        if a == 0:
            assert rule == "zero"
        elif s and t:
            assert rule == "ten"


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
