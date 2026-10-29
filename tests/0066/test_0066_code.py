"""Question 0066: the page's merge, skyline, above and peak (as published) against the
references of the generator (the overlap graph, the total height read at every integer
point) on random inputs; the page's examples and self-checks; the claims of the proofs
(after sorting only the last merged interval can overlap, the merged output is disjoint and
sorted, the pieces are maximal and canonical, the order at equal positions does not matter);
the corollary that part a is part b with height 1; the traps (no sort, the previous input
interval, `<` for closed intervals, zero-length pieces, unjoined pieces, pair overlaps); and
the follow-ups (insert, intersection, covered length, stabbing points)."""

import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0066  # noqa: E402

ns = load_python(66)
merge, skyline, above, peak = ns["merge"], ns["skyline"], ns["above"], ns["peak"]


def rand_intervals(rng, n, lo=0, hi=20, span=6, point=True):
    return [(s, s + rng.randint(0 if point else 1, span)) for s in (rng.randint(lo, hi) for _ in range(n))]


def rand_triples(rng, n, hmax=4):
    return [(s, e, rng.randint(1, hmax)) for s, e in rand_intervals(rng, n, point=False)]


def test_page_examples():
    assert merge(q0066.IVS) == [(1, 6), (8, 10), (15, 18)] == q0066.brute_merge(q0066.IVS)
    assert merge([(1, 4), (4, 5)]) == [(1, 5)]                       # touching closed intervals merge
    assert merge([(8, 10), (1, 3), (2, 6)]) == [(1, 6), (8, 10)]      # unsorted input
    assert merge([(1, 10), (2, 3), (4, 5)]) == [(1, 10)]              # nested, compared with the output
    assert merge([]) == [] and merge([(4, 4)]) == [(4, 4)]
    assert skyline(q0066.TRIPLES) == [(1, 2, 7), (2, 6, 11), (6, 7, 7)] == q0066.brute_skyline(q0066.TRIPLES)
    assert skyline([(0, 2, 3), (2, 4, 3)]) == [(0, 4, 3)]             # touching, same total: one piece
    assert skyline([(0, 4, 2), (4, 8, 2)]) == [(0, 8, 2)]             # the zero-length piece of the trap is gone
    assert skyline([(0, 2, 1), (5, 7, 1)]) == [(0, 2, 1), (5, 7, 1)]  # a gap is not reported
    assert skyline([(0, 4, 1), (0, 4, 2)]) == [(0, 4, 3)]             # the same start: one jump
    assert skyline([]) == [] and skyline([(3, 3, 5)]) == []           # an empty half-open interval
    # part a's example as half-open intervals of height 1, and the join of the neighbours
    one = [(s, e, 1) for s, e in q0066.IVS]
    assert skyline(one) == [(1, 2, 1), (2, 3, 2), (3, 6, 1), (8, 10, 1), (15, 18, 1)]
    assert above(skyline(one), 1) == [(1, 6), (8, 10), (15, 18)]
    assert above(skyline([(1, 4, 1), (4, 5, 1)]), 1) == [(1, 5)]
    # part c's example
    pc = skyline(q0066.TRIPLES_C)
    assert pc == [(0, 1, 2), (1, 2, 5), (2, 3, 6), (3, 4, 3), (4, 5, 1), (5, 6, 5), (6, 8, 4)]
    assert peak(pc) == (6, [(2, 3)]) and above(pc, 4) == [(1, 3), (5, 8)] == q0066.brute_above(q0066.TRIPLES_C, 4)
    assert above(pc, 5) == [(1, 3), (5, 6)] and above(pc, 7) == [] and above(pc, 1) == [(0, 8)]
    assert peak([]) == (0, [])
    # the statement's claims: 2 is in both [1, 3] and [2, 6]; the peak 6 = 2 + 3 + 1 on [2, 3)
    assert 1 <= 2 <= 3 and 2 <= 2 <= 6
    assert sum(h for s, e, h in q0066.TRIPLES_C if s <= 2 < e) == 6 == 2 + 3 + 1


def test_self_checks():
    assert len(merge([(2, 5), (1, 3), (6, 9), (9, 10), (12, 14)])) == 3
    assert merge([(2, 5), (1, 3), (6, 9), (9, 10), (12, 14)]) == [(1, 5), (6, 10), (12, 14)]
    assert skyline([(0, 4, 2), (2, 6, 3), (4, 8, 2)]) == [(0, 2, 2), (2, 6, 5), (6, 8, 2)]   # 3 pieces
    assert peak(skyline(q0066.TRIPLES_C))[0] == 6


def test_against_the_references():
    rng = random.Random(66)
    for _ in range(3000):
        n = rng.randint(0, 9)
        ivs = rand_intervals(rng, n)
        rng.shuffle(ivs)
        assert merge(ivs) == q0066.brute_merge(ivs), ivs
        tr = rand_triples(rng, n)
        pieces = skyline(tr)
        assert pieces == q0066.brute_skyline(tr), tr
        t = rng.randint(1, 10)
        assert above(pieces, t) == q0066.brute_above(tr, t), (tr, t)
        top, where = peak(pieces)
        pts = q0066.heights(tr)
        assert top == max(pts.values(), default=0)
        assert where == (q0066.brute_above(tr, top) if top else []), tr


def test_merged_output_is_canonical():
    """Disjoint, sorted, and every input interval inside exactly one output interval; the
    output does not depend on the input order."""
    rng = random.Random(661)
    for _ in range(1000):
        ivs = rand_intervals(rng, rng.randint(1, 8))
        out = merge(ivs)
        assert all(a[1] < b[0] for a, b in zip(out, out[1:]))          # disjoint and sorted, no touching pair left
        for s, e in ivs:
            assert sum(1 for a, b in out if a <= s and e <= b) == 1
        shuffled = list(ivs)
        rng.shuffle(shuffled)
        assert merge(shuffled) == out


def test_only_the_last_merged_interval_can_overlap():
    """The claim of the proof: in sorted order, an interval that does not overlap the last
    merged one overlaps none of the earlier ones either."""
    rng = random.Random(662)
    for _ in range(1000):
        ivs = sorted(rand_intervals(rng, rng.randint(1, 8)))
        for r in q0066.trace_merge(ivs):
            earlier = r["before"][:-1]
            assert all(b < r["s"] for _, b in earlier), (ivs, r)        # they end before the interval starts
            if r["kind"] == "new" and earlier:
                assert all(b < r["s"] for _, b in r["before"])


def test_pieces_are_maximal_and_canonical():
    rng = random.Random(663)
    for _ in range(1000):
        tr = rand_triples(rng, rng.randint(1, 8))
        pieces = skyline(tr)
        pts = q0066.heights(tr)
        for (s, e, t), nxt in zip(pieces, pieces[1:] + [None]):
            assert s < e and t > 0                                         # no zero-length piece, no gap
            assert all(pts[x] == t for x in range(s, e))                   # constant inside
            assert pts.get(s - 1, 0) != t and pts.get(e, 0) != t           # maximal: a neighbour differs
            if nxt:
                assert e <= nxt[0] and (e < nxt[0] or t != nxt[2])         # sorted, neighbours never share a total
        assert len(pieces) <= 2 * len(tr) - 1
        # the order of the input does not matter
        shuffled = list(tr)
        rng.shuffle(shuffled)
        assert skyline(shuffled) == pieces


def test_part_a_is_part_b_with_height_one():
    rng = random.Random(664)
    for _ in range(2000):
        ivs = rand_intervals(rng, rng.randint(1, 8), point=False)
        assert above(skyline([(s, e, 1) for s, e in ivs]), 1) == merge(ivs), ivs
    # the total height with height 1 is the count of intervals covering the point (0062)
    tx = [(0, 30, 1), (5, 10, 1), (15, 20, 1)]
    assert peak(skyline(tx)) == (2, [(5, 10), (15, 20)])


def test_event_order_at_equal_positions():
    """Emitting before all the events of a position gives the same pieces in any order of
    the events; emitting after every event needs -h before +h or a zero-length piece appears."""
    def per_event(triples, minus_first):
        events = sorted(((p, d) for s, e, h in triples for p, d in ((s, h), (e, -h))), key=lambda x: (x[0], x[1] if minus_first else -x[1]))
        out, total, prev = [], 0, None
        for p, d in events:
            if prev is not None and total != 0:
                out.append((prev, p, total))                               # no p > prev check, no join
            total += d
            prev = p
        return out

    assert (4, 4, 4) in per_event([(0, 4, 2), (4, 8, 2)], False)         # the trap: +h first
    assert all(a < b for a, b, _ in per_event([(0, 4, 2), (4, 8, 2)], True))
    assert (0, 0, 1) in per_event([(0, 4, 1), (0, 4, 2)], True)          # two starts at one position: -h first does not help
    rng = random.Random(665)
    for _ in range(500):
        tr = rand_triples(rng, rng.randint(1, 7))
        # the coalesced sweep from events sorted with +h first gives the same pieces
        events = sorted(((p, d) for s, e, h in tr for p, d in ((s, h), (e, -h))), key=lambda x: (x[0], -x[1]))
        out, total, prev = [], 0, None
        for p, d in events:
            if prev is not None and p > prev and total != 0:
                if out and out[-1][1] == prev and out[-1][2] == total:
                    out[-1][1] = p
                else:
                    out.append([prev, p, total])
            total += d
            prev = p
        assert [tuple(x) for x in out] == skyline(tr)


def test_difference_array_variant():
    rng = random.Random(666)
    for _ in range(500):
        tr = rand_triples(rng, rng.randint(1, 8))
        L = max(e for _, e, _ in tr)
        diff = [0] * (L + 1)
        for s, e, h in tr:
            diff[s] += h
            diff[e] -= h
        run, out = 0, []
        for x in range(L):
            run += diff[x]
            if run and out and out[-1][1] == x and out[-1][2] == run:
                out[-1][1] = x + 1
            elif run:
                out.append([x, x + 1, run])
        assert [tuple(p) for p in out] == skyline(tr)


def no_sort(intervals):
    out = []
    for s, e in intervals:
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [tuple(x) for x in out]


def previous_input(intervals):
    """The trap: compared with the previous input interval, not the last merged one."""
    ivs = sorted(intervals)
    out = []
    for i, (s, e) in enumerate(ivs):
        if i and s <= ivs[i - 1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [tuple(x) for x in out]


def strict(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s < out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return [tuple(x) for x in out]


def test_traps():
    assert no_sort([(8, 10), (1, 3), (2, 6)]) == [(8, 10)]              # the two later intervals vanish
    assert previous_input([(1, 10), (2, 3), (4, 5)]) == [(1, 10), (4, 5)]
    assert strict([(1, 4), (4, 5)]) == [(1, 4), (4, 5)] and merge([(1, 4), (4, 5)]) == [(1, 5)]
    # pair overlaps against the height at a point
    tx = [(0, 30, 1), (5, 10, 1), (15, 20, 1)]
    pairs = max(sum(1 for b in tx if a is not b and a[0] < b[1] and b[0] < a[1]) for a in tx) + 1
    assert pairs == 3 and peak(skyline(tx))[0] == 2
    # the unjoined pieces describe the same height but are not the canonical list
    assert [(0, 2, 3), (2, 4, 3)] != skyline([(0, 2, 3), (2, 4, 3)])
    rng = random.Random(667)
    bad_prev = bad_strict = 0
    for _ in range(500):
        ivs = rand_intervals(rng, rng.randint(2, 7))
        bad_prev += previous_input(ivs) != merge(ivs)
        bad_strict += strict(ivs) != merge(ivs)
    assert bad_prev > 20 and bad_strict > 20


# --- follow-ups ----------------------------------------------------------------------------

def insert(merged, new):
    """LC 57 in one pass: copy what ends before, absorb what overlaps, copy the rest."""
    s, e = new
    out, i = [], 0
    while i < len(merged) and merged[i][1] < s:
        out.append(merged[i])
        i += 1
    while i < len(merged) and merged[i][0] <= e:
        s, e = min(s, merged[i][0]), max(e, merged[i][1])
        i += 1
    out.append((s, e))
    return out + merged[i:]


def intersection(a, b):
    """LC 986 with two pointers."""
    out, i, j = [], 0, 0
    while i < len(a) and j < len(b):
        s, e = max(a[i][0], b[j][0]), min(a[i][1], b[j][1])
        if s <= e:
            out.append((s, e))
        if a[i][1] < b[j][1]:
            i += 1
        else:
            j += 1
    return out


def stab(intervals):
    """Greedy by end: the fewest points that hit every closed interval."""
    pts, last = [], None
    for s, e in sorted(intervals, key=lambda x: x[1]):
        if last is None or s > last:
            pts.append(e)
            last = e
    return pts


def test_follow_ups():
    rng = random.Random(668)
    from itertools import combinations
    for _ in range(500):
        ivs = rand_intervals(rng, rng.randint(1, 7))
        m = merge(ivs)
        new = rand_intervals(rng, 1)[0]
        assert insert(m, new) == merge(ivs + [new])
        other = merge(rand_intervals(rng, rng.randint(1, 7)))
        got = intersection(m, other)
        want = {x for x in range(0, 30) if any(s <= x <= e for s, e in m) and any(s <= x <= e for s, e in other)}
        assert {x for s, e in got for x in range(s, e + 1)} == want
        assert all(a[1] < b[0] for a, b in zip(got, got[1:]))         # disjoint and sorted
        # the covered length (integer points, closed) is the sum over the merged output
        assert sum(e - s + 1 for s, e in m) == len({x for s, e in ivs for x in range(s, e + 1)})
        # stabbing: every interval hit, and no smaller set of points does it
        pts = stab(ivs)
        assert all(any(s <= p <= e for p in pts) for s, e in ivs)
        cands = sorted({e for _, e in ivs})
        for k in range(len(pts)):
            assert not any(all(any(s <= p <= e for p in c) for s, e in ivs) for c in combinations(cands, k))
