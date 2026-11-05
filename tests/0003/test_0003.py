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
