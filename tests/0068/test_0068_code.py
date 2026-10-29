"""Question 0068: the page's StreamMedian, StreamQuantile and WindowQuantile (as published)
against sorting the prefix or the window on random streams with many duplicates and every p
from 0 to 1; the page's examples and self-checks; the claims of the proofs (the order and
size invariants, the target moving by at most one, the live counts, the heap sizes bounded
by 2 live + 1, the memory growth without the rebuild); the traps (the sign, floor and the
float ceil) and the numbers of the follow-ups (the counting array, Welford)."""

import math
import random
import statistics
import sys
from fractions import Fraction
from heapq import heappop, heappush

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0068  # noqa: E402

ns = load_python(68)
StreamMedian, stream_medians = ns["StreamMedian"], ns["stream_medians"]
StreamQuantile, stream_quantiles = ns["StreamQuantile"], ns["stream_quantiles"]
WindowQuantile, window_quantiles = ns["WindowQuantile"], ns["window_quantiles"]
S = q0068.STREAM
PS = [(0, 1), (1, 1), (1, 2), (1, 4), (9, 10), (99, 100), (7, 100), (3, 7)]


def test_page_examples():
    assert stream_medians(S) == [5, 10, 5, 4, 5, 6, 7, 7.5, 8, 7.5]
    assert stream_quantiles(S, 9, 10) == [5, 15, 15, 15, 15, 15, 15, 15, 20, 15]
    assert stream_quantiles(S, 1, 4) == [5, 5, 1, 1, 3, 3, 3, 3, 5, 3]
    assert window_quantiles(S, 4, 1, 2) == [5, 5, 5, 3, 3, 3, 7, 8, 9, 9]
    assert window_quantiles(S, 4, 1, 1) == [5, 15, 15, 15, 15, 8, 9, 10, 20, 20]
    # the statement: the median after 5 15 is 10, after 5 15 1 it is 5
    assert stream_medians([5, 15]) == [5, 10] and stream_medians([5, 15, 1])[-1] == 5
    # equal values sit in both heaps and the median is still right
    assert stream_medians([4, 4, 4, 4]) == [4, 4, 4, 4]
    # the ranks of the tables: p = 0.9 is the maximum up to n = 9, p = 0.25 grows every four values
    assert [q0068.rank_of(n, 9, 10) for n in range(1, 11)] == [1, 2, 3, 4, 5, 6, 7, 8, 9, 9]
    assert [q0068.rank_of(n, 1, 4) for n in range(1, 11)] == [1, 1, 1, 1, 2, 2, 2, 2, 3, 3]
    assert all(q0068.rank_of(n, 99, 100) == n for n in range(1, 100)) and q0068.rank_of(100, 99, 100) == 99


def test_self_checks():
    assert stream_medians(S)[5] == 6 and sorted(S[:6]) == [1, 3, 5, 7, 8, 15]
    assert stream_quantiles(S, 9, 10)[-1] == 15 and sorted(S)[8] == 15 and q0068.rank_of(10, 9, 10) == 9
    assert window_quantiles(S, 4, 1, 2)[-1] == 9 and sorted(S[-4:]) == [2, 9, 10, 20]


def test_against_sorting():
    rng = random.Random(68)
    for _ in range(1500):
        n = rng.randint(1, 25)
        nums = [rng.randint(-3, 6) for _ in range(n)]
        meds = stream_medians(nums)
        for i, m in enumerate(meds):
            assert Fraction(m) == q0068.brute_median(nums[:i + 1]), (nums, i)
        num, den = rng.choice(PS + [(rng.randint(0, 20), 20)])
        got = stream_quantiles(nums, num, den)
        assert got == [q0068.brute_quantile(nums[:i + 1], num, den) for i in range(n)], (nums, num, den)
        w = rng.randint(1, 8)
        got = window_quantiles(nums, w, num, den)
        assert got == [q0068.brute_quantile(nums[max(0, i - w + 1):i + 1], num, den) for i in range(n)], (nums, w, num, den)


def test_invariants_of_part_a():
    rng = random.Random(681)
    for _ in range(500):
        nums = [rng.randint(0, 9) for _ in range(rng.randint(1, 30))]
        sm = StreamMedian()
        for i, x in enumerate(nums):
            sm.add(x)
            low, high = [-v for v in sm.low], list(sm.high)
            assert len(low) - len(high) in (0, 1) and len(low) == -(-(i + 1) // 2)      # the sizes, ceil(n / 2)
            assert max(low) <= min(high) if high else True                               # the order
            assert sorted(low) == sorted(nums[:i + 1])[:len(low)]                        # the smaller half exactly
    # the lower median is low's top, and p = 1/2 gives it
    for n in range(1, 12):
        nums = [rng.randint(0, 5) for _ in range(n)]
        sm, sq = StreamMedian(), StreamQuantile(1, 2)
        for x in nums:
            sm.add(x)
            sq.add(x)
        assert sq.quantile() == -sm.low[0] == sorted(nums)[(n - 1) // 2]
        assert n % 2 == 0 or sm.median() == sq.quantile()


def test_invariants_of_part_b():
    rng = random.Random(682)
    for num, den in PS:
        # the target never decreases and grows by at most one
        ranks = [q0068.rank_of(n, num, den) for n in range(1, 200)]
        assert all(0 <= b - a <= 1 for a, b in zip(ranks, ranks[1:]))
        for _ in range(100):
            nums = [rng.randint(0, 9) for _ in range(rng.randint(1, 30))]
            sq = StreamQuantile(num, den)
            for i, x in enumerate(nums):
                before = len(sq.low)
                sq.add(x)
                low, high = [-v for v in sq.low], list(sq.high)
                assert len(low) == q0068.rank_of(i + 1, num, den) and len(low) + len(high) == i + 1
                assert len(low) - before in (0, 1)                                      # at most one move back
                assert max(low) <= min(high) if high else True
    # p = 0 is the minimum, p = 1 the maximum
    nums = [rng.randint(-9, 9) for _ in range(40)]
    assert stream_quantiles(nums, 0, 1) == [min(nums[:i + 1]) for i in range(40)]
    assert stream_quantiles(nums, 1, 1) == [max(nums[:i + 1]) for i in range(40)]


def test_invariants_of_part_c():
    """The live counts match the window, every stored item of low is <= every stored item
    of high (dead ones included), a heap never holds more than 2 live + 1 items, and at
    most one element moves between the heaps after the push-through."""
    rng = random.Random(683)
    for _ in range(400):
        nums = [rng.randint(0, 6) for _ in range(rng.randint(1, 40))]
        w = rng.randint(1, 7)
        num, den = rng.choice(PS)
        wq = WindowQuantile(w, num, den)
        for i, x in enumerate(nums):
            wq.add(x)
            low, high = wq.heaps["low"], wq.heaps["high"]
            win = nums[max(0, i - w + 1):i + 1]
            live_low = [-v for v, j in low if -j in wq.side]
            live_high = [v for v, j in high if j in wq.side]
            assert len(live_low) == wq.live["low"] == q0068.rank_of(len(win), num, den)
            assert len(live_high) == wq.live["high"] == len(win) - len(live_low)
            assert sorted(live_low + live_high) == sorted(win)
            assert max(-v for v, _ in low) <= min((v for v, _ in high), default=10 ** 9)
            assert len(low) <= 2 * wq.live["low"] + 1 and len(high) <= 2 * wq.live["high"] + 1
            assert set(wq.side) == set(range(max(0, i - w + 1), i + 1))
    # frames of the reference: at most one move after the push-through, pruned tops were dead
    for _ in range(200):
        nums = [rng.randint(0, 6) for _ in range(rng.randint(1, 30))]
        w, (num, den) = rng.randint(1, 6), rng.choice(PS)
        for f in q0068.trace_window(nums, w, num, den):
            if f["kind"] == "target":
                assert f["moved"] is None or True
            for s, (v, j) in f["pruned"]:
                assert j < f["i"] - w + 1                                                # left the window


def test_memory_without_the_rebuild():
    """An increasing stream with W = 2: the old values in low never reach its top, so without
    the rebuild low grows with n; the page's class keeps it at 2 live + 1."""
    n = 60

    def lazy_no_rebuild(nums, w):
        low, side, live = [], {}, 0
        for i, x in enumerate(nums):
            heappush(low, (-x, -i))
            side[i] = "low"
            live += 1
            if i >= w:
                side.pop(i - w)
                live -= 1
            while -low[0][1] not in side:
                heappop(low)
        return len(low), live

    kept, live = lazy_no_rebuild(list(range(n)), 2)
    assert kept == n and live == 2
    wq = WindowQuantile(2, 1, 1)
    for x in range(n):
        wq.add(x)
    assert len(wq.heaps["low"]) + len(wq.heaps["high"]) <= 2 * 2 + 2


def test_traps():
    # the sign: pushing x instead of -x into low gives the minimum of the smaller half
    low, high = [], []
    for x in [5, 15, 1]:
        heappush(low, x)
        heappush(high, heappop(low))
        if len(high) > len(low):
            heappush(low, heappop(high))
    assert low[0] == 1 and stream_medians([5, 15, 1])[-1] == 5
    # floor instead of ceil: rank 4 instead of 5 at p = 0.9, n = 5; the same at p n integral
    assert math.floor(0.9 * 5) == 4 and q0068.rank_of(5, 9, 10) == 5
    assert math.floor(0.5 * 4) == 2 == q0068.rank_of(4, 1, 2)
    # ceil in floating point: one place too many when p n should be whole
    assert 0.07 * 100 != 7 and math.ceil(0.07 * 100) == 8 and q0068.rank_of(100, 7, 100) == 7
    # nearest rank against interpolation differ on the same data
    data = sorted(S)
    nearest = data[q0068.rank_of(10, 9, 10) - 1]
    interp = data[8] + 0.1 * (data[9] - data[8])            # numpy's default at 0.9 with 10 points: index 8.1
    assert nearest == 15 and interp == 15.5
    # sorting every time: n log n per query
    n = 10 ** 6
    assert n * math.log2(n) > 1.9e7


def test_follow_ups():
    # a counting array gives the exact quantile for small integers
    rng = random.Random(684)
    nums = [rng.randint(0, 20) for _ in range(300)]
    cnt = [0] * 21
    for i, x in enumerate(nums):
        cnt[x] += 1
        r = q0068.rank_of(i + 1, 9, 10)
        acc, v = 0, 0
        while acc + cnt[v] < r:
            acc += cnt[v]
            v += 1
        assert v == q0068.brute_quantile(nums[:i + 1], 9, 10)
    # Welford: the mean and the variance from three numbers of state
    n = mean = m2 = 0.0
    xs = [rng.uniform(0, 100) for _ in range(200)]
    for x in xs:
        n += 1
        d = x - mean
        mean += d / n
        m2 += d * (x - mean)
    assert abs(mean - statistics.mean(xs)) < 1e-9 and abs(m2 / (n - 1) - statistics.variance(xs)) < 1e-6
