"""Question 0084: the longest increasing subsequence.

The page's lis_dp, lis_from_dp, lis and count_lis against a brute force over all
subsequences (every array of length up to 7 over a few values, and random arrays), the
example's dp, prev, tails, parent and counts, the comparisons (28 against 10), the traps
([3, 4, 5, 1], bisect_right on [2, 2, 2], dp[-1] on [3, 4, 1], the greedy examples), the
follow-ups (non-decreasing, patience piles, envelopes, Erdős–Szekeres, 2^(n/2) LIS), the
page's numbers, the generated blocks, and the box's models under Node against the Python
reference."""

import bisect
import itertools
import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))

import q0084  # noqa: E402

PAGE = (ROOT / "docs" / "questions" / "junior" / "0084-longest-increasing-subsequence.md").read_text(encoding="utf-8")
ns = load_python(84)
lis_dp, lis_from_dp, lis, count_lis = ns["lis_dp"], ns["lis_from_dp"], ns["lis"], ns["count_lis"]
A = [10, 9, 2, 5, 3, 7, 101, 18]


def increasing(s) -> bool:
    return all(x < y for x, y in zip(s, s[1:]))


def brute(a):
    """(the LIS length, how many index sets give it) over all subsequences."""
    best, count = 0, 0
    for mask in range(1 << len(a)):
        s = [a[i] for i in range(len(a)) if mask >> i & 1]
        if increasing(s):
            if len(s) > best:
                best, count = len(s), 1
            elif len(s) == best:
                count += 1
    return best, count


def is_subsequence(s, a) -> bool:
    it = iter(a)
    return all(any(x == y for y in it) for x in s)


def check(a):
    best, count = brute(a)
    n, dp, prev = lis_dp(a)
    assert n == best
    s1, s2 = lis_from_dp(a, dp, prev), lis(a)
    for s in (s1, s2):
        assert len(s) == best and increasing(s) and is_subsequence(s, a)
    if a:
        assert count_lis(a) == count


def test_against_brute_force():
    for n in range(0, 7):
        for a in itertools.product(range(4), repeat=n):
            check(list(a))
    rng = random.Random(84)
    for _ in range(400):
        check([rng.randint(-20, 40) for _ in range(rng.randint(1, 12))])


def test_example():
    n, dp, prev = lis_dp(A)
    assert (n, dp, prev) == (4, [1, 1, 1, 2, 2, 3, 4, 4], [-1, -1, -1, 2, 2, 3, 5, 5])
    assert lis_from_dp(A, dp, prev) == [2, 5, 7, 101]
    assert lis(A) == [2, 3, 7, 18]
    trace = q0084.tails_trace(A)
    assert trace[-1][5] == [2, 3, 7, 18]
    assert [t[2] for t in trace] == [0, 0, 0, 1, 1, 2, 3, 3]
    assert q0084.parents(A) == ([-1, -1, -1, 2, 2, 4, 5, 5], 7)
    assert len(A) * (len(A) - 1) // 2 == 28 and q0084.probes(A) == 10
    assert count_lis(A) == 4 and count_lis([1, 3, 5, 4, 7]) == 2
    assert q0084.pairs([1, 3, 5, 4, 7]) == ([1, 2, 3, 3, 4], [1, 1, 1, 1, 2])
    assert q0084.pairs(A) == ([1, 1, 1, 2, 2, 3, 4, 4], [1, 1, 1, 1, 1, 2, 2, 2])
    # the four of the example: two end at 101 and two at 18
    fours = [s for s in itertools.combinations(range(8), 4) if increasing([A[i] for i in s])]
    assert len(fours) == 4 and sorted(s[-1] for s in fours) == [6, 6, 7, 7]
    assert sorted([A[i] for i in s] for s in fours) == [[2, 3, 7, 18], [2, 3, 7, 101], [2, 5, 7, 18], [2, 5, 7, 101]]


def test_traps():
    trace = q0084.tails_trace([3, 4, 5, 1])
    assert trace[-1][5] == [1, 4, 5] and not is_subsequence([1, 4, 5], [3, 4, 5, 1])
    assert lis([3, 4, 5, 1]) == [3, 4, 5]
    # bisect_right counts the non-decreasing ones
    tails = []
    for x in [2, 2, 2]:
        k = bisect.bisect_right(tails, x)
        tails[k:k + 1] = [x]
    assert len(tails) == 3 and lis_dp([2, 2, 2])[0] == 1
    assert lis_dp([3, 4, 1])[1][-1] == 1 and lis_dp([3, 4, 1])[0] == 2
    # the tasks of the boxes: "יורד" and "ערכים שווים" have five LIS of length 1, tails stays at
    # one value on equal values, and in part c's array cnt[4] = 2 after the tie of a[3] = 4
    assert lis_dp([5, 4, 3, 2, 1])[0] == 1 and count_lis([5, 4, 3, 2, 1]) == 5
    assert count_lis([2] * 5) == 5 and q0084.tails_trace([2] * 5)[-1][5] == [2]
    assert q0084.pairs([1, 3, 5, 4, 7])[1][4] == 2
    # part c's steps: a[5] = 7 of part a reaches length 3 after 5 and after 3, count[5] = 2
    A = [10, 9, 2, 5, 3, 7, 101, 18]
    assert [j for j in range(5) if A[j] < A[5] and q0084.pairs(A)[0][j] == 2] == [3, 4] and q0084.pairs(A)[1][5] == 2

    def greedy(a):
        out = []
        for x in a:
            if not out or x > out[-1]:
                out.append(x)
        return out
    assert greedy([10, 1, 2, 3]) == [10] and lis([10, 1, 2, 3]) == [1, 2, 3]
    assert greedy([1, 5, 2, 3]) == [1, 5] and len(lis([1, 5, 2, 3])) == 3


def test_follow_ups():
    # non-decreasing with bisect_right, against a brute force
    rng = random.Random(7)
    for _ in range(200):
        a = [rng.randint(0, 5) for _ in range(rng.randint(1, 9))]
        tails = []
        for x in a:
            k = bisect.bisect_right(tails, x)
            tails[k:k + 1] = [x]
        best = max(len(s) for r in range(len(a) + 1) for s in itertools.combinations(a, r)
                   if all(x <= y for x, y in zip(s, s[1:])))
        assert len(tails) == best
        # patience: the leftmost pile whose top is >= the card; the tops are tails, piles = LIS
        piles = []
        for x in a:
            k = next((p for p, pile in enumerate(piles) if pile[-1] >= x), len(piles))
            if k == len(piles):
                piles.append([x])
            else:
                piles[k].append(x)
        assert len(piles) == lis_dp(a)[0]
        assert all(all(x >= y for x, y in zip(p, p[1:])) for p in piles)
    # envelopes: sort by width up, height down, then LIS on the heights
    for _ in range(100):
        env = [(rng.randint(1, 6), rng.randint(1, 6)) for _ in range(rng.randint(1, 7))]
        heights = [h for w, h in sorted(env, key=lambda e: (e[0], -e[1]))]
        best = 0
        for r in range(1, len(env) + 1):
            for s in itertools.permutations(env, r):
                if all(x[0] < y[0] and x[1] < y[1] for x, y in zip(s, s[1:])):
                    best = max(best, r)
        assert lis_dp(heights)[0] == best
    # Erdős–Szekeres: n^2 + 1 distinct numbers have a monotone subsequence of n + 1; n^2 can fail
    for n in (2, 3):
        for p in itertools.permutations(range(n * n + 1)):
            assert lis_dp(list(p))[0] >= n + 1 or lis_dp([-x for x in p])[0] >= n + 1
        bad = [x for b in range(n) for x in range(n * (n - 1 - b), n * (n - b))]   # n blocks, each increasing, the blocks decreasing
        assert lis_dp(bad)[0] == n and lis_dp([-x for x in bad])[0] == n and len(bad) == n * n
    # 2, 1, 4, 3, 6, 5, ...: 2^(n/2) longest ones
    for half in range(1, 9):
        a = [x for k in range(half) for x in (2 * k + 2, 2 * k + 1)]
        assert count_lis(a) == 2 ** half


def test_page_numbers():
    for s in ["`dp = [1, 1, 1, 2, 2, 3, 4, 4]`", "`[2, 5, 7, 101]`", "`tails = [2, 3, 7, 18]`", "‏28", "10 השוואות",
              "`[1, 3, 5, 7]`", "`[1, 3, 4, 7]`", "זה 2, ובדוגמה של סעיף א\n        זה 4", "`tails = [1, 4, 5]`",
              "`tail_at[3] = 7`", "שתיים נגמרות ב-101 ושתיים ב-18", "\\( 2^{n/2} \\)", "`[3, 4, 1]`",
              'data-kind="lis" data-mode="dp" data-nums="10 9 2 5 3 7 101 18"',
              'data-kind="lis" data-mode="tails" data-nums="10 9 2 5 3 7 101 18"',
              'data-kind="lis" data-mode="dp" data-nums="1 3 5 4 7"']:
        assert s in PAGE, s


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(84)


def dp_steps(a):
    """The box's dp steps by the page's rule: one per (i, j) comparison, an init per i."""
    n = len(a)
    length, count, prev, out = [0] * n, [0] * n, [-1] * n, []
    for i in range(n):
        length[i], count[i] = 1, 1
        out.append((i, -1, "init", list(length), list(count), list(prev)))
        for j in range(i):
            kind = "skip"
            if a[j] < a[i]:
                if length[j] + 1 > length[i]:
                    length[i], count[i], prev[i], kind = length[j] + 1, count[j], j, "longer"
                elif length[j] + 1 == length[i]:
                    count[i] += count[j]
                    kind = "tie"
                else:
                    kind = "shorter"
            out.append((i, j, kind, list(length), list(count), list(prev)))
    return out


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(840)
    arrays = [A, [1, 3, 5, 4, 7], [3, 4, 5, 1], [2, 2, 2, 2, 2], [5, 4, 3, 2, 1], [7], [-5, 0, -99, 999, 3]]
    arrays += [[rng.randint(-10, 30) for _ in range(rng.randint(1, 12))] for _ in range(40)]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(arrays)}.map((a) => [m.lisDpSteps(a), m.lisDpResult(a), m.lisTailsSteps(a), m.lisTailsSeq(a)])));")
    for a, (dsteps, res, tsteps, tseq) in zip(arrays, got):
        want = dp_steps(a)
        assert [(s["i"], s["j"], s["kind"], s["len"], s["cnt"], s["prev"]) for s in dsteps] == [
            (i, j, k, l, c, p) for i, j, k, l, c, p in want]
        n, dp, prev = lis_dp(a)
        assert res["best"] == n and res["count"] == count_lis(a)
        assert [a[i] for i in res["seq"]] == lis_from_dp(a, dp, prev)
        assert [a[i] for i in tseq] == lis(a)
        # the tails steps: the probes of each element, then its insertion, as q0084's trace
        inserts = [s for s in tsteps if s["kind"] != "probe"]
        trace = q0084.tails_trace(a)
        assert [(s["i"], s["x"], s["k"], s["kind"] == "append", s["old"], s["tails"]) for s in inserts] == [
            (i, x, k, app, old, t) for i, x, k, app, old, t in trace]
        assert sum(1 for s in tsteps if s["kind"] == "probe") == q0084.probes(a)
        assert inserts[-1]["parent"] == q0084.parents(a)[0]
        for s in tsteps:
            if s["kind"] == "probe":
                assert s["lo"] <= s["mid"] < s["hi"] and s["less"] == (s["tails"][s["mid"]] < s["x"])
    # the parser: 1 to 12 integers in [-99, 999], spaces or commas
    cases = ["10 9 2 5", "1,2, 3", "  4  ", "", "1 2 x", "1000", "-100", " ".join(["1"] * 13), "-99 999"]
    parsed = node_json(f"const m = {explorer_require()};console.log(JSON.stringify({json.dumps(cases)}.map((t) => m.lisParse(t))));")
    assert parsed == [[10, 9, 2, 5], [1, 2, 3], [4], None, None, None, None, None, [-99, 999]]
