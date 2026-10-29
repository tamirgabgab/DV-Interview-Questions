"""Question 0069: the page's Fenwick, ranks, passed, passed_merge, overtook, inversions,
disorder, arrival_order and live_overtakes (as published) against every pair on random
arrays with and without ties; the page's examples and self-checks; the claims of the
proofs (the Fenwick invariant and the O(log n) walks, the sum identity, the reorder-buffer
depth, the bounds 0 and n(n - 1) / 2 of the disorder, the stream equals passed); the traps
(prefix(r) against prefix(r - 1), update before query, n instead of i, ranks with
duplicates); and the follow-ups (LIS, the fewest swaps, the largest distance)."""

import random
import sys
from itertools import combinations

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0069  # noqa: E402

ns = load_python(69)
Fenwick, ranks, passed, passed_merge = ns["Fenwick"], ns["ranks"], ns["passed"], ns["passed_merge"]
overtook, inversions, disorder = ns["overtook"], ns["inversions"], ns["disorder"]
arrival_order, live_overtakes = ns["arrival_order"], ns["live_overtakes"]

DONE = q0069.DONE
SELF = [7, 3, 9, 2, 8]


def arrays(seed, count, lo=0, hi=9, nmax=14):
    rng = random.Random(seed)
    for _ in range(count):
        n = rng.randint(0, nmax)
        yield [rng.randint(lo, hi) for _ in range(n)]


def test_page_examples():
    assert passed(DONE) == [2, 1, 1, 0] == passed_merge(DONE)
    assert overtook(DONE) == [0, 1, 0, 3]
    assert inversions(DONE) == 4 == sum(passed(DONE)) == sum(overtook(DONE))
    assert abs(disorder(DONE) - 4 / 6) < 1e-12
    assert arrival_order(DONE) == [3, 1, 0, 2]
    assert live_overtakes(arrival_order(DONE), 4) == [0, 1, 2, 1]        # per arrival: requests 3, 1, 0, 2
    assert ranks(DONE) == {1: 1, 2: 2, 5: 3, 6: 4}
    assert [ranks(DONE)[v] for v in DONE] == [3, 2, 4, 1]
    # the statement: request 3 overtook 0, 1 and 2; request 1 overtook 0
    assert {(i, j) for i in range(4) for j in range(i + 1, 4) if DONE[j] < DONE[i]} == {(0, 1), (0, 3), (1, 3), (2, 3)}
    # the hand-worked walk of part a: the cells read and raised
    assert [(r["qpath"], r["upath"], r["tree"]) for r in q0069.walk_passed(DONE)] == \
        [([], [1, 2, 4], [1, 1, 0, 1]), ([3, 2], [4], [1, 1, 0, 2]), ([1], [2, 4], [1, 2, 0, 3]), ([2], [3, 4], [1, 2, 1, 4])]
    # the idea's numbers: prefix(7) reads 7, 6, 4; add(3) raises 3, 4, 8; 12 & -12 = 4
    assert q0069.Fen(8).prefix(7)[1] == [7, 6, 4] and q0069.Fen(8).add(3) == [3, 4, 8]
    assert 12 & -12 == 4 and 6 & -6 == 2 and 8 & -8 == 8


def test_self_checks():
    assert passed(SELF) == [2, 1, 2, 0, 0] and passed(SELF)[0] == 2
    assert overtook(SELF) == [0, 1, 0, 3, 1] and overtook(SELF)[3] == 3
    assert inversions(SELF) == 5 and abs(disorder(SELF) - 0.5) < 1e-12
    assert {(i, j) for i in range(5) for j in range(i + 1, 5) if SELF[j] < SELF[i]} == {(0, 1), (0, 3), (1, 3), (2, 3), (2, 4)}


def test_against_every_pair():
    for done in arrays(69, 3000):
        n = len(done)
        assert passed(done) == q0069.brute_passed(done) == passed_merge(done), done
        assert overtook(done) == q0069.brute_overtook(done), done
        inv = q0069.brute_inversions(done)
        assert inversions(done) == inv == sum(passed(done)) == sum(overtook(done))
        pairs = n * (n - 1) // 2
        assert abs(disorder(done) - (inv / pairs if pairs else 0.0)) < 1e-12
        order = arrival_order(done)
        assert sorted(order) == list(range(n)) and all(done[a] <= done[b] for a, b in zip(order, order[1:]))
        live = live_overtakes(order, n)
        assert [live[k] for k in range(n)] == [passed(done)[i] for i in order]      # the live report is passed
    for done in arrays(690, 1000, 0, 10 ** 9, 30):                                  # large times: the compression
        assert passed(done) == q0069.brute_passed(done) and overtook(done) == q0069.brute_overtook(done)


def test_fenwick_invariant_and_walk_lengths():
    rng = random.Random(691)
    for _ in range(300):
        m = rng.randint(1, 40)
        ft, cnt = Fenwick(m), [0] * (m + 1)
        for _ in range(rng.randint(0, 60)):
            r = rng.randint(1, m)
            ft.add(r)
            cnt[r] += 1
            for i in range(1, m + 1):
                lb = i & -i
                assert ft.tree[i] == sum(cnt[i - lb + 1:i + 1])             # the block (i - lowbit, i]
            for i in range(0, m + 1):
                assert ft.prefix(i) == sum(cnt[1:i + 1])
        # both walks visit at most as many cells as the bits of m
        for i in range(1, m + 1):
            assert len(q0069.Fen(m).add(i)) <= m.bit_length() and len(q0069.Fen(m).prefix(i)[1]) <= m.bit_length()
            # the update path is exactly the cells whose block holds i, in increasing order
            assert q0069.Fen(m).add(i) == [j for j in range(i, m + 1) if j - (j & -j) < i <= j]
            # the query path's blocks are disjoint and cover 1..i
            covered = []
            for j in q0069.Fen(m).prefix(i)[1]:
                covered += list(range(j - (j & -j) + 1, j + 1))
            assert sorted(covered) == list(range(1, i + 1))


def test_dv_claims():
    """max(passed) is the depth of a reorder buffer that delivers in send order; the sum
    identity; the disorder is 0 in order and 1 fully reversed; all-equal times give zeros;
    strictly decreasing times give n - 1 - i."""
    for done in arrays(692, 2000):
        n = len(done)
        held, next_out, peak = set(), 0, 0
        for i in arrival_order(done):
            held.add(i)
            if i == next_out:
                peak = max(peak, len(held) - 1)                 # the younger responses that waited for i
            while next_out in held:
                held.remove(next_out)
                next_out += 1
        assert peak == (max(passed(done)) if n else 0), done
        assert not held
    for n in range(0, 12):
        assert inversions(list(range(n))) == 0 and disorder(list(range(n))) == 0.0
        assert inversions(list(range(n, 0, -1))) == n * (n - 1) // 2 and (disorder(list(range(n, 0, -1))) == 1.0 or n < 2)
        assert passed([4] * n) == [0] * n == overtook([4] * n)
        assert passed(list(range(n, 0, -1))) == [n - 1 - i for i in range(n)]
    # a non-decreasing sequence with ties is still "in order"
    assert inversions([1, 1, 2, 2, 2, 3]) == 0


def passed_prefix_r(done):
    """The tie trap of part a: prefix(r) counts equal times as overtakes."""
    rk = ranks(done)
    ft, out = Fenwick(len(rk)), [0] * len(done)
    for i in range(len(done) - 1, -1, -1):
        out[i] = ft.prefix(rk[done[i]])
        ft.add(rk[done[i]])
    return out


def overtook_update_first(done):
    """The order trap: the rank goes in before the query, so the request counts itself."""
    rk = ranks(done)
    ft, out = Fenwick(len(rk)), []
    for i, v in enumerate(done):
        ft.add(rk[v])
        out.append(i - ft.prefix(rk[v]))
    return out


def overtook_minus_n(done):
    """The n trap of part b: n - prefix(r) also counts the later requests."""
    rk = ranks(done)
    ft, out = Fenwick(len(rk)), []
    for v in done:
        out.append(len(done) - ft.prefix(rk[v]))
        ft.add(rk[v])
    return out


def ranks_with_duplicates(done):
    """A dict over sorted(done) with the duplicates: equal values share a rank, with gaps,
    and the tree still counts right (the test checks it equals ranks())."""
    seen = {}
    for v in sorted(done):
        if v not in seen:
            seen[v] = len(seen) + 1
    return seen


def passed_by_position(done):
    """The compression trap: the rank of every request is its position among all n times
    sorted (ties broken by the index, the later first), so two equal times get different
    ranks."""
    order = sorted(range(len(done)), key=lambda i: (done[i], -i))
    rk = {i: p + 1 for p, i in enumerate(order)}
    ft, out = Fenwick(len(done)), [0] * len(done)
    for i in range(len(done) - 1, -1, -1):
        out[i] = ft.prefix(rk[i] - 1)
        ft.add(rk[i])
    return out


def test_traps():
    # equal times: prefix(r) counts them, prefix(r - 1) does not
    assert passed_prefix_r([3, 3, 3]) == [2, 1, 0] and passed([3, 3, 3]) == [0, 0, 0]
    assert passed_prefix_r([1, 2, 3]) == passed([1, 2, 3])                   # the same without ties
    # update before query: every count one too small, negative for the first
    assert overtook_update_first(DONE) == [-1, 0, -1, 2]
    for done in arrays(693, 500):
        if done:
            assert overtook_update_first(done) == [c - 1 for c in overtook(done)]
    # n instead of the number inserted: the later requests are counted too
    assert overtook_minus_n(DONE) == [4, 4, 2, 4]
    for done in arrays(694, 500):
        n = len(done)
        assert overtook_minus_n(done) == [c + n - i for i, c in enumerate(overtook(done))]   # the later ones and itself
    # ranks by the position in the sorted list give two equal times different ranks, and
    # then one of them "overtakes" the other; a dict keyed by the value cannot do that
    assert passed_by_position([3, 3, 3]) == [2, 1, 0] and passed([3, 3, 3]) == [0, 0, 0]
    for done in arrays(697, 500, 0, 3):
        assert passed_by_position(done) == passed(done) or len(set(done)) < len(done)
    assert ranks_with_duplicates([3, 1, 3]) == {1: 1, 3: 2} == ranks([3, 1, 3])
    # the double loop at n = 10**6: about 5 * 10**11 comparisons
    n = 10 ** 6
    assert n * (n - 1) // 2 == 499999500000
    # an unsigned i & -i still gives the lowest set bit in 32 bits
    for i in range(1, 100):
        assert (i & (-i & 0xFFFFFFFF)) == i & -i


def test_follow_ups():
    assert q0069.lis_length(DONE) == 2 and q0069.min_swaps(DONE) == 2 and q0069.max_distance(DONE) == 3
    # the cycles of 3 1 0 2: 0 -> 3 -> 2 -> 0 and the fixed point 1
    order = arrival_order(DONE)
    assert order == [3, 1, 0, 2] and order[1] == 1 and order[order[order[0]]] == 0
    for done in arrays(695, 1500, 0, 12, 10):
        n = len(done)
        lis = max((len(c) for k in range(n + 1) for c in combinations(done, k) if all(a < b for a, b in zip(c, c[1:]))), default=0)
        assert q0069.lis_length(done) == lis
        assert q0069.max_distance(done) == max((j - i for i in range(n) for j in range(i + 1, n) if done[j] < done[i]), default=0)
    # the fewest swaps: n - cycles, against a breadth-first search over the permutations
    from collections import deque
    from itertools import permutations
    for n in range(1, 6):
        for perm in permutations(range(n)):
            goal, seen, dq = tuple(range(n)), {perm: 0}, deque([perm])
            while dq:
                s = dq.popleft()
                if s == goal:
                    break
                for a in range(n):
                    for b in range(a + 1, n):
                        t = list(s)
                        t[a], t[b] = t[b], t[a]
                        t = tuple(t)
                        if t not in seen:
                            seen[t] = seen[s] + 1
                            dq.append(t)
            assert q0069.min_swaps(list(perm)) == seen[goal], perm
    # ties: equal times in the stream, passed to the monitor in send order, are not overtakes
    for done in arrays(696, 500, 0, 3):
        assert sum(live_overtakes(arrival_order(done), len(done))) == inversions(done)
