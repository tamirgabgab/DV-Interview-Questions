"""The self-checks (docs/javascripts/selfcheck.js): every page's data-answer against an
independent computation here, and the lint rule for a malformed one. A self-check without
an expected value below fails, so a new one comes with its computation."""

import heapq
import re
import sys
from collections import deque
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import lint_pages  # noqa: E402

CHECK = re.compile(r'<div class="selfcheck" data-answer="([^"]+)"')


def two_children(day: bool) -> Fraction:
    kinds = [(s, d) for s in "BG" for d in range(7 if day else 1)]
    fams = [(x, y) for x in kinds for y in kinds]
    told = [f for f in fams if any(c == ("B", 2 if day else 0) for c in f)]
    return Fraction(sum(1 for f in told if f[0][0] == f[1][0] == "B"), len(told))


def josephus(n: int) -> int:
    ring, i = list(range(n)), 0
    while len(ring) > 1:
        i = (i + 1) % len(ring)
        ring.pop(i)
    return ring[0]


def splits(blocks: int, most: int) -> int:
    c = [1] + [0] * blocks
    for n in range(1, blocks + 1):
        c[n] = sum(c[n - j] for j in range(1, most + 1) if n - j >= 0)
    return c[blocks]


def motorcycle(walk: float, ride: float) -> float:
    """Three people, one two-seat bike: the passenger is dropped at d and walks on, the
    driver fetches the walker; d is chosen so that all three arrive together."""
    v, u = 1 / walk, 1 / ride

    def times(d):
        back = d * (u - v) / u / (u + v)               # the driver meets the walker
        meet = v * (d / u + back)
        rider = d / u + back + (1 - meet) / u
        return rider, d / u + (1 - d) / v

    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        a, b = times(mid)
        lo, hi = (mid, hi) if b > a else (lo, mid)
    return times(lo)[0] * 1.0


def cake(first: float, grow, n_max: int = 10_000) -> int:
    rest, best, who, p, k = 1.0, -1.0, 0, first, 1
    while rest > 1e-15 and k <= n_max:
        share = min(p, 1.0) * rest
        if share > best + 1e-12:
            best, who = share, k
        rest -= share
        p, k = grow(p), k + 1
    return who


def clock_meetings() -> int:
    day = 86_400
    pairs = [(3600, 59), (43_200, 719), (43_200, 11)]   # the period of a pair is P / q seconds
    counts = [-(-day * q // P) for P, q in pairs]
    triple = 2                                          # 00:00 and 12:00
    return sum(counts) - 2 * triple


def bridge(times) -> int:
    n, full = len(times), (1 << len(times)) - 1
    dist, heap = {(0, 0): 0}, [(0, 0, 0)]               # (time, who is across, torch side)
    while heap:
        t, s, side = heapq.heappop(heap)
        if s == full:
            return t
        if t > dist[(s, side)]:
            continue
        here = [i for i in range(n) if ((s >> i) & 1) == side]
        groups = [(i, j) for i in here for j in here if i < j] if side == 0 else [(i,) for i in here]
        for g in groups:
            ns = s
            for i in g:
                ns ^= 1 << i
            nt = t + max(times[i] for i in g)
            if nt < dist.get((ns, 1 - side), 1 << 30):
                dist[(ns, 1 - side)] = nt
                heapq.heappush(heap, (nt, ns, 1 - side))
    raise AssertionError


def river() -> int:
    safe = lambda s: not (((s >> 1) & 1) == ((s >> 2) & 1) != (s & 1)) and not (((s >> 2) & 1) == ((s >> 3) & 1) != (s & 1))
    dist, q = {0: 0}, deque([0])
    while q:
        s = q.popleft()
        if s == 15:
            return dist[s]
        for item in (0, 1, 2, 3):
            if item and ((s >> item) & 1) != (s & 1):
                continue
            ns = s ^ 1 ^ ((1 << item) if item else 0)
            if safe(ns) and ns not in dist:
                dist[ns] = dist[s] + 1
                q.append(ns)
    raise AssertionError


def lfsr_period() -> int:
    s, n = 0b0001, 0
    while True:                                         # x^4 + x^3 + 1, Fibonacci form
        bit = ((s >> 3) ^ (s >> 2)) & 1
        s, n = ((s << 1) | bit) & 0xF, n + 1
        if s == 0b0001:
            return n


def eggs(k: int, floors: int) -> int:
    m = 0
    f = [0] * (k + 1)
    while f[k] < floors:
        m += 1
        for e in range(k, 0, -1):
            f[e] = f[e - 1] + 1 + f[e]
    return m


def camel(a: float, c: float, w: float, keep: float) -> float:
    dist = 0.0
    while w > c:
        loads = -(-w // c)
        cost = (2 * loads - 1) * a
        drop = w - (loads - 1) * c
        dist += drop / cost
        w -= drop
    return dist + (w - keep) / a


def mice(n: int, rounds: int) -> int:
    """Each mouse ends in one of rounds + 1 ways; the fewest mice whose outcomes cover n bottles."""
    return next(m for m in range(64) if (rounds + 1) ** m >= n)


def coin_runs(a: str, b: str = "", steps: int = 3000) -> tuple[float, float]:
    """The mean wait until a (or b) shows, and the chance that a shows first, by pushing the
    distribution of the last few tosses forward until almost nothing is left."""
    keep = max(len(a), len(b)) - 1
    now, mean, first = {"": 1.0}, 0.0, 0.0
    for t in range(1, steps + 1):
        nxt = {}
        for seen, p in now.items():
            for c in "HT":
                s = seen + c
                if s.endswith(a):
                    mean += t * p / 2
                    first += p / 2
                elif b and s.endswith(b):
                    mean += t * p / 2
                else:
                    k = s[-keep:] if keep else ""
                    nxt[k] = nxt.get(k, 0.0) + p / 2
        now = nxt
    return mean, first


def coin_var(a: str, steps: int = 3000) -> float:
    """The variance of the wait for a, from the same push of the distribution forward."""
    keep, now, m1, m2 = len(a) - 1, {"": 1.0}, 0.0, 0.0
    for t in range(1, steps + 1):
        nxt = {}
        for seen, p in now.items():
            for c in "HT":
                s = seen + c
                if s.endswith(a):
                    m1, m2 = m1 + t * p / 2, m2 + t * t * p / 2
                else:
                    k = s[-keep:] if keep else ""
                    nxt[k] = nxt.get(k, 0.0) + p / 2
        now = nxt
    return m2 - m1 * m1


def alu_bins() -> tuple[int, int, int]:
    """The ALU covergroup: the coverpoint bins, the cross cells kept, and 1 over the rarest
    cell's probability with uniform operands."""
    ops, classes = 5, 4                                       # zero, max, msb, mid
    cross = sum(1 for o in range(ops) for a in range(classes) for b in range(classes) if not (o == 4 and b in (1, 2)))
    return ops + classes + classes + 2, cross, ops * 256 * 256


def rr_bound(n: int, weights=None) -> int:
    """The longest wait of a requester under full load, by running the arbiter."""
    weights = weights or [1] * n
    ptr, used, run, best = 0, 0, [0] * n, [0] * n
    for _ in range(50 * sum(weights)):
        win = ptr
        for i in range(n):
            if i != win:
                run[i] += 1
                best[i] = max(best[i], run[i])
        run[win] = 0
        used += 1
        if used == weights[win]:
            ptr, used = (ptr + 1) % n, 0
    return max(best) if weights == [1] * n else best[0]


def fsm_answers() -> list[int]:
    """The divisible-by-m machines: the remainder of 1011 read from the MSB; the fewest
    states from the LSB for 3, counted as the prefixes with different futures (every suffix
    up to 8 bits); and 10^-1 mod 7."""
    def future(prefix):
        k, v = len(prefix), sum(b << i for i, b in enumerate(prefix))
        return tuple((v + (w << k)) % 3 == 0 for n in range(9) for w in range(1 << n))
    prefixes = [[(x >> i) & 1 for i in range(n)] for n in range(7) for x in range(1 << n)]
    return [int("1011", 2) % 3, len({future(p) for p in prefixes}), next(y for y in range(7) if 10 * y % 7 == 1)]


def window_answers() -> list[int]:
    """The divisible window of L digits: the window of 3 bits after 1, 1, 0, 1 entered at the
    LSB (its remainder by 3) and 1, 0, 1, 1 entered at the MSB (its value), shifted as bit
    strings; and 10^4 mod 7, the weight of a decimal digit that leaves a window of 4."""
    lsb = "000"
    for b in "1101":
        lsb = (lsb + b)[1:]
    msb = "000"
    for b in "1011":
        msb = (b + msb)[:-1]
    return [int(lsb, 2) % 3, int(msb, 2), 10 ** 4 % 7]


def ants_answers() -> list[int]:
    """Ants on a pole: the longest time, by every configuration of up to three ants on a pole
    of 8 (it is the length) scaled to 100; the most collisions of 100 ants by a dynamic
    program over the ants from the left (the number going right so far); and the page's six
    ants simulated in half seconds, turning at every meeting."""
    def run(pos, dirs, length):
        x, d, t, last = [2 * p for p in pos], list(dirs), 0, 0
        alive = set(range(len(x)))
        while alive:
            for k in [k for k in alive if (x[k] <= 0 and d[k] < 0) or (x[k] >= 2 * length and d[k] > 0)]:
                alive.discard(k)
                last = t
            for k in alive:
                x[k] += d[k]
            t += 1
            for a in alive:
                for b in alive:
                    if a < b and x[a] == x[b]:
                        d[a], d[b] = -d[a], -d[b]
        return last / 2
    longest = 0
    for n in (1, 2, 3):
        for pos in __import__("itertools").combinations(range(9), n):
            for dirs in __import__("itertools").product((1, -1), repeat=n):
                longest = max(longest, run(pos, dirs, 8))
    best = {0: 0}                                         # ants going right so far -> most pairs
    for _ in range(100):
        nxt = {}
        for r, c in best.items():
            nxt[r + 1] = max(nxt.get(r + 1, -1), c)        # this ant goes right
            nxt[r] = max(nxt.get(r, -1), c + r)            # this ant goes left: meets them all
        best = nxt
    def ring_home(pos, dirs, length):
        """Laps of the ring simulated until every ant is back at its start with its direction."""
        x, d, ticks = [2 * p for p in pos], list(dirs), 0
        while True:
            x = [(v + dd) % (2 * length) for v, dd in zip(x, d)]
            ticks += 1
            for a in range(len(x)):
                for b in range(a + 1, len(x)):
                    if x[a] == x[b]:
                        d[a], d[b] = -d[a], -d[b]
            if ticks % (2 * length) == 0 and x == [2 * p for p in pos] and d == list(dirs):
                return ticks // 2
    return [int(longest * 100 / 8), max(best.values()), int(run([10, 25, 40, 60, 75, 90], [1, -1, 1, -1, -1, 1], 100)),
            ring_home([10, 25, 40, 60, 75, 90], [1, 1, 1, -1, -1, 1], 100)]


def tag_answers() -> list[int]:
    """Missing tags: part a's missing tag by a set difference; part b's register bits for 8-bit
    tags (x plus one per bit); part c's missing tag by trying every pair (a, d) of 0..9."""
    a = sorted(set(range(8)) - {3, 0, 6, 1, 7, 2, 5})[0]
    c = next(m for m in range(10) for d in range(10) if m != d and m - d == 4 and m * m - d * d == 40)
    return [a, 8 + 8 * 8, c]


def coin_answers() -> list[int]:
    """Coins in a row: the colour of 1, 2, 5, 3; greedy against the best reply on it; the best
    play on 1, 1, 9, 1, 1, 9 and on 1, 5, 1 by minimax over (left, right) choices."""
    def best(c):
        if not c:
            return 0
        return max(c[0] + sum(c[1:]) - best(c[1:]), c[-1] + sum(c[:-1]) - best(c[:-1]))

    def greedy_vs_best(c):
        mine = 0
        while c:
            k = 0 if c[0] >= c[-1] else -1
            mine += c[k]
            c = c[1:] if k == 0 else c[:-1]
            if c:                                  # the reply that leaves greedy the least
                c = c[1:] if c[0] + sum(c[1:]) - best(c[1:]) >= c[-1] + sum(c[:-1]) - best(c[:-1]) else c[:-1]
        return mine
    row = [1, 2, 5, 3]
    return [max(sum(row[0::2]), sum(row[1::2])), greedy_vs_best(row), best([1, 1, 9, 1, 1, 9]), best([1, 5, 1])]


def popcount_answers() -> list[int]:
    """Same number of ones: the next above 92 and the previous below 96 by a search number by
    number; the next above 120 with as many zeros (no leading zeros), also by a search."""
    k = lambda v: bin(v).count("1")  # noqa: E731
    z = lambda v: v.bit_length() - k(v)  # noqa: E731
    nxt = next(y for y in range(93, 256) if k(y) == k(92))
    prv = next(y for y in range(95, 0, -1) if k(y) == k(96))
    return [nxt, prv, next(y for y in range(121, 1024) if z(y) == z(120))]


def comparisons(n: int) -> int:
    """0003: both loops of the mystery code run over the whole array, with no early exit."""
    return sum(1 for i in range(n) for j in range(n))


def mislabeled_samples() -> int:
    """0004: one ball is enough when some box holds a pure colour that differs between every
    arrangement where no label is right."""
    from itertools import permutations
    labels = "RBM"
    arrangements = [p for p in permutations("RBM") if all(c != l for c, l in zip(p, labels))]
    one = any(len({a[i] for a in arrangements}) == len(arrangements) and all(a[i] != "M" for a in arrangements)
              for i in range(3))
    return 1 if one else 2


def center_inside(m: int) -> Fraction:
    """0007: three distinct points of m on a circle; the centre is inside when every gap
    between neighbours is under half the circle (counted by the three gaps)."""
    good = sum(1 for g1 in range(1, m) for g2 in range(1, m - g1) if 2 * max(g1, g2, m - g1 - g2) < m)
    from math import comb
    return Fraction(good * m, 3) / comb(m, 3)


def kaprekar_fixed(digits: int) -> int:
    """0012, 0013: the fixed point other than 0 of "largest minus smallest of the digits"."""
    fixed = [x for x in range(10 ** digits)
             if int("".join(sorted(f"{x:0{digits}d}", reverse=True))) - int("".join(sorted(f"{x:0{digits}d}"))) == x]
    return max(fixed)


def josephus_keep_one(n: int) -> int:
    """0016 part b: one stays, the next two leave, around the circle."""
    ring, i = list(range(n)), 0
    while len(ring) > 1:
        for _ in range(2):
            if len(ring) == 1:
                break
            j = (i + 1) % len(ring)
            ring.pop(j)
            if j < i:
                i -= 1
        i = (i + 1) % len(ring)
    return ring[0]


def kaprekar_keys() -> int:
    """0044: the keys after many Kaprekar steps from every three-digit number."""
    def step(x):
        d = sorted(f"{x:03d}")
        return int("".join(reversed(d))) - int("".join(d))
    keys = set()
    for x in range(1000):
        for _ in range(20):
            x = step(x)
        keys.add(x)
    return len(keys)


def ones_answers() -> list:
    """0061: the longest window with at most k zeros (part a), and with at most k cells that
    are not its most frequent value (part b), every window tried."""
    def longest(seq, k, same):
        best = 0
        for i in range(len(seq)):
            for j in range(i, len(seq)):
                w = seq[i:j + 1]
                bad = len(w) - max(w.count(c) for c in set(w)) if same else w.count(0)
                if bad <= k:
                    best = max(best, len(w))
        return best
    return [longest([1, 0, 1, 1, 0, 1, 0, 1, 1, 1], 1, False), longest("ABAACAAB", 2, True)]


def tag_pool_answers() -> list:
    """0062: the most transactions open at once (open from the send up to the response), and
    what one shared pool saves against a pool per kind."""
    def most(txns):
        return max(sum(1 for s, e in txns if s <= t < e) for t, _ in txns)
    reads, writes = [(0, 10), (2, 12)], [(20, 30), (22, 32)]
    return [most([(0, 10), (10, 20), (5, 15)]), most(reads) + most(writes) - most(reads + writes)]


EXPECTED = {
    "0003": [comparisons(5)],
    "0004": [mislabeled_samples()],
    "0007": [Fraction(1) - Fraction(3, 4), center_inside(360)],
    "0012": [kaprekar_fixed(3)],
    "0013": [kaprekar_fixed(4)],
    "0015": [two_children(False), two_children(True)],
    "0016": [josephus(20), josephus_keep_one(30)],
    "0021": [splits(4, 4), splits(8, 4)],
    "0023": [2 ** sum(1 for b in range(0x10020 + 1, 0x10020 + 256) if b % 128 == 0)],   # cuts at multiples of the RCB
    "0026": [motorcycle(13, 1)],
    "0027": [cake(0.01, lambda p: p + 0.1)],
    "0028": [cake(0.01, lambda p: p * 1.5)],
    "0029": [clock_meetings()],
    "0030": [40],                                       # tests/0030 derives it from the nets
    "0031": [bridge([1, 2, 5, 10])],
    "0032": [river()],
    "0036": [lfsr_period()],
    "0033": [120 * (1 - Fraction(3, 4) * 80 / 100)],        # the burst times one minus the read rate over the write rate
    "0039": [eggs(3, 100)],
    "0040": [len("1011")],                                  # one state per prefix seen: none, 1, 10, 101
    "0041": [16 * sum(Fraction(1, k) for k in range(1, 17))],
    "0043": [9, 7],                                         # tests/0043 runs the plan on every ordering
    "0044": [kaprekar_keys()],
    "0042": [camel(0.5, 150, 450, 30)],
    "0051": [mice(1000, 1), mice(1000, 2), mice(1000, 3)],
    "0052": [coin_runs("HH")[0], coin_runs("HHH")[0], coin_runs("HT", "HH")[1], coin_var("HH")],
    "0053": list(alu_bins()),
    "0054": [rr_bound(4), rr_bound(8), rr_bound(4, [1, 2, 3, 4])],
    "0055": fsm_answers(),
    "0056": window_answers(),
    "0057": ants_answers(),
    "0058": tag_answers(),
    "0059": coin_answers(),
    "0060": popcount_answers(),
    "0061": ones_answers(),
    "0062": tag_pool_answers(),
}


def value(text: str) -> Fraction:
    return Fraction(text)


def test_every_answer():
    found = {}
    for page in sorted((ROOT / "docs" / "questions").glob("*/*.md")):
        answers = CHECK.findall(page.read_text(encoding="utf-8"))
        if answers:
            found[page.name[:4]] = [value(a) for a in answers]
    assert set(found) == set(EXPECTED), "a self-check without an expected value, or the other way round"
    for qid, got in found.items():
        want = EXPECTED[qid]
        assert len(got) == len(want), qid
        for g, w in zip(got, want):
            assert abs(float(g) - float(w)) < 1e-6, (qid, g, w)


def test_lint_rule():
    good = '<div class="selfcheck" data-answer="1/3" data-show="1/3" data-hint="רמז" markdown>\nשאלה\n</div>\n\n??? success "פתרון"\n'
    assert lint_pages.lint_selfchecks(good) == []
    bad = '<div class="selfcheck" data-answer="שליש" data-hint="" markdown>\nשאלה\n</div>\n'
    problems = lint_pages.lint_selfchecks(bad)
    assert len(problems) == 3                           # the answer, the hint, no solution after it
