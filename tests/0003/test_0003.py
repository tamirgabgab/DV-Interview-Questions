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
