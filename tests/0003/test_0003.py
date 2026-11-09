import random

from extract_code import load_python

mystery = load_python(3)["mystery"]


def test_page_example():
    a = [3, 1, 4, 2]
    mystery(a)
    assert a == [1, 2, 3, 4]


def test_sorts_ascending():
    rng = random.Random(3)
    for _ in range(500):
        a = [rng.randint(-20, 20) for _ in range(rng.randint(0, 12))]
        expected = sorted(a)
        mystery(a)
        assert a == expected


def test_explorer_matches_page_code():
    """The tracer box: its comparison-by-comparison replay against the page's mystery on
    the page example and random arrays (the result, n² comparisons, the swap count from
    an instrumented copy of the loop, and the invariant at the end of every i)."""
    import json

    from page_tests import explorer_require, node_json

    rng = random.Random(3)
    cases = [[3, 1, 4, 2], [1, 2, 3], [9, 8, 7, 6, 5], [2, 2, 2]] + [[rng.randint(0, 20) for _ in range(rng.randint(3, 8))] for _ in range(150)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map((A) => {{ const t = m.loopTrace(A); return [t.result, t.comparisons, t.swaps, t.frames.filter((f) => f.endOfI).map((f) => f.after)]; }})));""")
    for A, (result, comparisons, swaps, ends) in zip(cases, got):
        a = list(A)
        mystery(a)
        assert result == a and comparisons == len(A) ** 2
        # the same loop, counting the swaps and keeping the array after every i
        b, count, after = list(A), 0, []
        for i in range(len(b)):
            for j in range(len(b)):
                if b[i] < b[j]:
                    b[i], b[j] = b[j], b[i]
                    count += 1
            after.append(list(b))
        assert swaps == count and ends == after
        for i, arr in enumerate(ends):
            assert arr[:i + 1] == sorted(arr[:i + 1]) and arr[i] == max(arr)


def test_explorer_trap_from_next():
    """The box's trap (V4): the inner loop from j = i + 1 against the same loop in Python,
    which sorts in descending order with n(n - 1)/2 comparisons; the end of every i has
    the maximum of the rest at i."""
    import json

    from page_tests import explorer_require, node_json

    rng = random.Random(30)
    cases = [[3, 1, 4, 2], [1, 2, 3], [2, 2, 2]] + [[rng.randint(0, 20) for _ in range(rng.randint(3, 8))] for _ in range(100)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map((A) => {{ const t = m.loopTrace(A, true); return [t.result, t.comparisons, t.code[2], t.frames.filter((f) => f.endOfI).map((f) => f.after)]; }})));""")
    for A, (result, comparisons, line, ends) in zip(cases, got):
        b, after = list(A), []
        for i in range(len(b)):
            for j in range(i + 1, len(b)):
                if b[i] < b[j]:
                    b[i], b[j] = b[j], b[i]
            if i + 1 < len(b):
                after.append(list(b))
        assert result == b == sorted(A, reverse=True)
        assert comparisons == len(A) * (len(A) - 1) // 2 and line.strip() == "for j in range(i + 1, n):"
        assert ends == after


def test_passes_figure():
    """The passes figure (tools/figures/q0003.py), recorded from the page's mystery: the
    array after every i and the swaps of every pass against a plain replay of the loop,
    one arc per swap and a frame on every cell a pass changed."""
    import sys

    from extract_code import ROOT

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import q0003

    rng = random.Random(33)
    for A in [q0003.EXAMPLE, [5, 4, 3, 2, 1], [2, 2, 1]] + [[rng.randint(0, 9) for _ in range(rng.randint(2, 7))] for _ in range(60)]:
        b, want = list(A), []
        for i in range(len(b)):
            sw = []
            for j in range(len(b)):
                if b[i] < b[j]:
                    b[i], b[j] = b[j], b[i]
                    sw.append((i, j))
            want.append((i, sw, list(b)))
        assert q0003.passes(A) == want
    p = q0003.passes()
    assert [a for _, _, a in p] == [[4, 1, 3, 2], [1, 4, 3, 2], [1, 3, 4, 2], [1, 2, 3, 4]]   # the page's table
    svg = q0003.figure()
    assert svg.count('class="fc-arc"') == sum(len(s) for _, s, _ in p) == 5
    rows = [q0003.EXAMPLE] + [a for _, _, a in p]
    assert svg.count('class="fc-chg"') == sum(x != y for r, s in zip(rows, rows[1:]) for x, y in zip(r, s))


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(3)


class _Counted(list):
    """A list that counts item writes: the page's swap writes two."""

    writes = 0

    def __setitem__(self, k, v):
        self.writes += 1
        super().__setitem__(k, v)


def swaps_of(a):
    c = _Counted(a)
    mystery(c)
    assert c == sorted(a)
    return c.writes // 2


def test_swap_counts():
    """The cost section: over every permutation of 1..n (n = 2..8) at most n(n - 1)/2 + 1
    swaps and at least n - 1; n = 4: 7 on [2, 3, 4, 1] and [3, 4, 2, 1], 3 only on
    [4, 1, 2, 3]; a sorted array 2(n - 1) swaps (6 for n = 4, the example 5)."""
    import itertools

    for n in range(2, 9):
        counts = {p: swaps_of(list(p)) for p in itertools.permutations(range(1, n + 1))}
        assert max(counts.values()) == n * (n - 1) // 2 + 1 and min(counts.values()) == n - 1
        assert swaps_of(list(range(1, n + 1))) == 2 * (n - 1)
        if n == 4:
            assert sorted(p for p, c in counts.items() if c == 7) == [(2, 3, 4, 1), (3, 4, 2, 1)]
            assert [p for p, c in counts.items() if c == 3] == [(4, 1, 2, 3)]
    assert swaps_of([3, 1, 4, 2]) == 5


def test_comparator_networks():
    """The hardware follow-up: the unrolled loop as compare-exchange units (i, j), which put
    the larger value at i. With the i = 0 pass, 9 units of depth 8; without it, the 6 units
    j < i (insertion sort) of depth 5; both sort every 0/1 input (so every input), and the
    known optimal network has 5 units in 3 layers."""
    import itertools

    def run(net, a):
        a = list(a)
        for i, j in net:
            if a[i] < a[j]:
                a[i], a[j] = a[j], a[i]
        return a

    def depth(net, n):
        level, d = [0] * n, 0
        for i, j in net:
            level[i] = level[j] = max(level[i], level[j]) + 1
            d = max(d, level[i])
        return d

    nine = [(0, j) for j in range(1, 4)] + [(i, j) for i in range(1, 4) for j in range(i)]
    six = nine[3:]
    best = [(1, 0), (3, 2), (2, 0), (3, 1), (2, 1)]
    for net, size, d in ((nine, 9, 8), (six, 6, 5), (best, 5, 3)):
        assert len(net) == size and depth(net, 4) == d
        assert all(run(net, a) == sorted(a) for a in itertools.product((0, 1), repeat=4))


def test_explorer_tags_and_end():
    """The box: the letters on equal values follow the page's mystery on values that compare
    by value only, (0a, 0b, 1) ends as (0b, 0a, 1); the trap's frames end at i = n - 2."""
    import json

    from page_tests import explorer_require, node_json

    class V:
        def __init__(self, v, tag):
            self.v, self.tag = v, tag

        def __lt__(self, other):
            return self.v < other.v

    rng = random.Random(4)
    cases = [[0, 0, 1], [2, 2, 2], [3, 1, 4, 2]] + [[rng.randint(0, 3) for _ in range(rng.randint(3, 8))] for _ in range(100)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map((A) => {{ const t = m.loopTrace(A), u = m.loopTrace(A, true); return [t.tags, t.frames[t.frames.length - 1].tags, u.frames[u.frames.length - 1].i]; }})));""")
    for A, (tags, last, trap_i) in zip(cases, got):
        a = [V(v, k) for k, v in enumerate(A)]
        mystery(a)
        assert tags == last == [x.tag for x in a]
        assert trap_i == len(A) - 2
    assert got[0][0] == [1, 0, 2]
