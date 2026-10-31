"""Question 0063: the page's window_max, longest_within and the cycle model WinMax (as
published) against every window on random arrays and streams; the page's examples, the
claims of the proofs (the invariant of the deque, its length, at most 2n operations, the
thermometer mask, the ages, no overflow of the K entries), the traps (front by value,
`<` against `<=`, `if` against `while`) and the numbers of the lower bound."""

import math
import random
import sys
from collections import deque

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0063  # noqa: E402

ns = load_python(63)
window_max, longest_within = ns["window_max"], ns["longest_within"]
WinMax, win_max_run = ns["WinMax"], ns["win_max_run"]


def test_page_examples():
    assert window_max(q0063.NUMS, 3) == [3, 3, 5, 5, 6, 7] == q0063.brute_max(q0063.NUMS, 3)
    assert window_max(q0063.NUMS, 1) == q0063.NUMS and window_max(q0063.NUMS, 8) == [7]
    assert longest_within([8, 2, 4, 7], 4) == 2
    assert longest_within([10, 1, 2, 4, 7, 2], 5) == 4
    assert longest_within([4, 2, 2, 2, 4, 4, 2, 2], 0) == 3
    assert longest_within([], 3) == 0 and longest_within([5], 0) == 1
    assert win_max_run(q0063.STREAM, 3) == [9, 9, 9, 7, 6, 6, 8, 8]
    # the windows of the statement and the walk of part b: [2 4 7 2] is the answer
    assert q0063.NUMS[0:3] == [1, 3, -1] and q0063.NUMS[1:4] == [3, -1, -3] and q0063.NUMS[2:5] == [-1, -3, 5]
    w = [10, 1, 2, 4, 7, 2][2:6]
    assert max(w) - min(w) == 5 and max([1, 2, 4, 7]) - min([1, 2, 4, 7]) == 6


def test_self_checks():
    # part a: [9 8 7 6 5 10], k = 4, the step of i = 5: one index from the front, three from the back
    ev = [e for e in q0063.trace_max([9, 8, 7, 6, 5, 10], 4) if e["i"] == 5 and e["kind"] != "push"]
    assert [e["kind"] for e in ev] == ["front", "pop", "pop", "pop"] and [e["idx"] for e in ev] == [1, 4, 3, 2]
    # part b: the longest window with max - min <= 4 is 6 7 8 10 6, places 2..6
    arr = [1, 5, 6, 7, 8, 10, 6, 5, 6]
    assert longest_within(arr, 4) == 5 == q0063.brute_limit(arr, 4)
    assert max(arr[1:6]) - min(arr[1:6]) == 5 and max(arr[2:7]) - min(arr[2:7]) == 4
    # part c: cycle 4 (x = 6): 5 and 3 compared out, 7 ages out
    r = q0063.hw_trace(q0063.STREAM, 3)[4]
    assert r["before"] == [(7, 2), (5, 1), (3, 0)] and r["keep"] == [True, False, False] and r["drop"] and r["after"] == [(6, 0)]
    assert len(r["before"]) - len(r["after"]) + 1 == 3       # three entries leave, x comes in


def test_against_every_window():
    rng = random.Random(63)
    for _ in range(3000):
        n = rng.randint(1, 14)
        nums = [rng.randint(-5, 5) for _ in range(n)]
        k = rng.randint(1, n)
        assert window_max(nums, k) == q0063.brute_max(nums, k), (nums, k)
        limit = rng.randint(0, 6)
        assert longest_within(nums, limit) == q0063.brute_limit(nums, limit), (nums, limit)
        samples = [rng.randint(0, 7) for _ in range(rng.randint(1, 30))]
        kk = rng.randint(1, 6)
        assert win_max_run(samples, kk) == [max(samples[max(0, t - kk + 1):t + 1]) for t in range(len(samples))], (samples, kk)


def test_deque_invariant_and_amortised_bound():
    rng = random.Random(631)
    for _ in range(500):
        n = rng.randint(1, 20)
        nums = [rng.randint(0, 6) for _ in range(n)]
        k = rng.randint(1, n)
        ev = q0063.trace_max(nums, k)
        assert len(ev) <= 2 * n                              # n pushes, at most n pops
        for e in ev:
            if e["kind"] == "push":
                i, q = e["i"], e["q"]
                want = [j for j in range(max(0, i - k + 1), i + 1) if all(nums[j] > nums[m] for m in range(j + 1, i + 1))]
                assert q == want and len(q) <= k, (nums, k, i)
                assert all(nums[a] > nums[b] for a, b in zip(q, q[1:]))      # strictly decreasing with <=
    # a strictly decreasing array fills the deque to k; equal values: <= keeps one, < keeps k
    assert max(len(e["q"]) for e in q0063.trace_max([9, 8, 7, 6, 5], 3)) == 3
    assert max(len(e["q"]) for e in q0063.trace_max([2] * 5, 3)) == 1
    assert max(len(e["q"]) for e in q0063.trace_max([2] * 5, 3, strict=True)) == 3
    # the example: step 4 takes out three indices (the front 1, then 3 and 2 from the back)
    assert [(e["kind"], e["idx"]) for e in q0063.trace_max(q0063.NUMS, 3) if e["i"] == 4] == [("front", 1), ("pop", 3), ("pop", 2), ("push", 4)]


def test_strict_pop_is_also_right():
    rng = random.Random(632)
    for _ in range(2000):
        n = rng.randint(1, 12)
        nums = [rng.randint(0, 3) for _ in range(n)]
        k = rng.randint(1, n)
        outs = [e["out"] for e in q0063.trace_max(nums, k, strict=True)]
        assert outs[-1] == q0063.brute_max(nums, k)


def by_value(nums, k):
    """The trap: a deque of values, the front taken out when it equals the value leaving."""
    q, out = deque(), []
    for i, x in enumerate(nums):
        if i >= k and q and q[0] == nums[i - k]:
            q.popleft()
        while q and q[-1] <= x:
            q.pop()
        q.append(x)
        if i >= k - 1:
            out.append(q[0])
    return out


def by_value_strict(nums, k):
    """Values with < at the back keep the copies, and then the front by value is right."""
    q, out = deque(), []
    for i, x in enumerate(nums):
        if i >= k and q and q[0] == nums[i - k]:
            q.popleft()
        while q and q[-1] < x:
            q.pop()
        q.append(x)
        if i >= k - 1:
            out.append(q[0])
    return out


def with_if(nums, limit):
    """The trap of part b: the left end moves one place at most per step. Returns the
    length found and whether a window it measured was not valid."""
    hi, lo, left, best, bad = deque(), deque(), 0, 0, False
    for right, x in enumerate(nums):
        while hi and nums[hi[-1]] <= x:
            hi.pop()
        while lo and nums[lo[-1]] >= x:
            lo.pop()
        hi.append(right)
        lo.append(right)
        if nums[hi[0]] - nums[lo[0]] > limit:
            if hi[0] == left:
                hi.popleft()
            if lo[0] == left:
                lo.popleft()
            left += 1
        w = nums[left:right + 1]
        bad |= max(w) - min(w) > limit
        best = max(best, right - left + 1)
    return best, bad


def test_traps():
    assert by_value([5, 5, 1], 2) == [5, 1] and window_max([5, 5, 1], 2) == [5, 5]
    rng = random.Random(633)
    for _ in range(2000):
        n = rng.randint(1, 12)
        nums = [rng.randint(0, 3) for _ in range(n)]
        k = rng.randint(1, n)
        assert by_value_strict(nums, k) == q0063.brute_max(nums, k)
        limit = rng.randint(0, 3)
        assert with_if(nums, limit)[0] == q0063.brute_limit(nums, limit)       # the length happens to be right
    # ... but the window is not valid: [1 2 3 10], limit 2, step 3 keeps 1..3 = 2 3 10
    assert with_if([1, 2, 3, 10], 2) == (3, True)
    # the cost of recomputing: n = 10**6, k = 10**3 is about a billion comparisons
    n, k = 10 ** 6, 10 ** 3
    assert (n - k + 1) * (k - 1) > 0.99e9


def test_hardware_model():
    """The cycle model as the proof states it: the mask is ones then zeros, the entries are
    part a's deque with the age of each index, at most one entry ages out, and p = K only
    when the front ages out."""
    rng = random.Random(634)
    for _ in range(400):
        k = rng.randint(1, 6)
        samples = [rng.randint(0, 9) for _ in range(rng.randint(1, 40))]
        rows = q0063.hw_trace(samples, k)
        ev = q0063.trace_max(samples, k)
        assert [r["out"] for r in rows] == win_max_run(samples, k)
        hw = WinMax(k)
        for r in rows:
            keep = r["keep"]
            assert keep == sorted(keep, reverse=True)                    # a thermometer
            assert r["p"] < k or r["drop"]                               # no overflow
            hw.clock(r["x"])
            push = next(e for e in ev if e["kind"] == "push" and e["i"] == r["t"])
            assert [s[:2] for s in hw.slots if s[2]] == r["after"] == [(samples[j], r["t"] - j) for j in push["q"]]
            assert all(a < k for _, a in r["after"])


def test_lower_bound_numbers():
    # log2 C(2^W, K) >= K (W - log2 K), close to K W bits
    for W, K in [(8, 3), (8, 4), (16, 8), (4, 4)]:
        bits = math.log2(math.comb(2 ** W, K))
        assert K * (W - math.log2(K)) <= bits <= K * W
    # a decreasing run then small samples: the outputs reveal every value of the run
    run = [9, 7, 5]
    assert win_max_run(run + [0, 0, 0], 3)[2:5] == run


def test_van_herk_follow_up():
    rng = random.Random(635)
    for _ in range(1000):
        n = rng.randint(1, 30)
        nums = [rng.randint(-9, 9) for _ in range(n)]
        k = rng.randint(1, n)
        out, cmp = q0063.van_herk(nums, k)
        assert out == q0063.brute_max(nums, k) and cmp <= 3 * n
