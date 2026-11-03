"""Question 0079: biased coins.

The page's fair_bit, biased_bit and die_roll are run as published: exactly, on every flip
sequence up to a length (a coin that reads a given sequence), with fractions for the
probabilities; and statistically, with the page's make_coin under fixed seeds. Every number
on the page is recomputed here (the tables of the generator, the traps and the follow-ups);
the generated blocks are checked; and the vncoin and cmpcoin boxes' models are compared under
Node with this reference (the seeded generator included)."""

import math
import re
import sys
from fractions import Fraction as Fr
from itertools import product

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0079  # noqa: E402

ns = load_python(79)
make_coin, fair_bit, biased_bit, die_roll = ns["make_coin"], ns["fair_bit"], ns["biased_bit"], ns["die_roll"]
PAGE = (ROOT / "docs" / "questions" / "junior" / "0079-biased-coin.md").read_text(encoding="utf-8")


class OutOfFlips(Exception):
    pass


def feeder(seq):
    """A coin that returns the flips of `seq` in order, and stops the run when they end."""
    it = iter(seq)
    used = [0]

    def coin():
        try:
            v = next(it)
        except StopIteration:
            raise OutOfFlips from None
        used[0] += 1
        return v
    return coin, used


def outcomes(fn, n):
    """fn(coin) on every 0/1 sequence of length n: {sequence: (result, flips used)}, or None
    when the sequence ran out before fn decided."""
    out = {}
    for seq in product((0, 1), repeat=n):
        coin, used = feeder(seq)
        try:
            out[seq] = (fn(coin), used[0])
        except OutOfFlips:
            out[seq] = None
    return out


def weight(seq, p):
    """P(the first len(seq) flips are seq) for a coin with P(1) = p."""
    ones = sum(seq)
    return p ** ones * (1 - p) ** (len(seq) - ones)


def masses(table, p, upto=None):
    """P(result r and decided) for each r, and P(decided), from the flip-sequence table: a
    decided run that used k flips is counted once, on the sequences that share its prefix."""
    res, seen = {}, set()
    for seq, v in table.items():
        if v is None:
            continue
        r, k = v
        pre = seq[:k]
        if pre in seen:
            continue
        seen.add(pre)
        res[r] = res.get(r, 0) + weight(pre, p)
    return res, sum(res.values(), Fr(0))


P_EXACT = [Fr(1, 2), Fr(1, 3), Fr(1, 10), Fr(7, 9), Fr(2, 5)]


def test_fair_bit_exact():
    table = outcomes(fair_bit, 12)
    for p in P_EXACT:
        q = 1 - p
        res, done = masses(table, p)
        assert res[0] == res[1]                         # 1 and 0 equally likely at every depth
        assert done == 1 - (1 - 2 * p * q) ** 6
    # a run decides on a pair that differs, and returns its first flip
    for seq, v in table.items():
        if v is not None:
            r, k = v
            assert k % 2 == 0 and seq[k - 2] != seq[k - 1] and r == seq[k - 2]
            assert all(seq[i] == seq[i + 1] for i in range(0, k - 2, 2))


def test_biased_bit_exact():
    n = 14
    for p in [Fr(1, 3), Fr(2, 3), Fr(1, 5), Fr(2, 5), Fr(3, 4), Fr(5, 8), Fr(1, 2), Fr(7, 16), Fr(1, 7)]:
        table = outcomes(lambda c, p=p: biased_bit(p, c), n)
        res, done = masses(table, Fr(1, 2))
        digits = q0079.digits(p, n)
        # P(1, decided within n flips) is p's expansion cut after n digits
        assert res.get(1, 0) == sum(Fr(int(d), 2 ** (i + 1)) for i, d in enumerate(digits))
        k = q0079.dyadic_len(p)
        if k is None:
            assert done == 1 - Fr(1, 2 ** n)
        else:
            assert done == 1 and res[1] == p
            used = max(v[1] for v in table.values())
            assert used == k                            # a dyadic p never needs more than k flips
        # the expected flips, from the table: the tail after n flips is 2^-n x 2 more
        prefixes = {s[:v[1]] for s in table for v in [table[s]] if v is not None}
        mean = sum((Fr(1, 2 ** len(pre)) * len(pre) for pre in prefixes), Fr(0))
        if k is not None:
            assert mean == q0079.cmp_flips(p) == 2 - Fr(2) ** (1 - k)
        else:
            assert mean + Fr(1, 2 ** n) * (n + 2) == 2 == q0079.cmp_flips(p)
    # a float p is a dyadic fraction: the same answers as the exact one
    for x in (0.75, 0.625, 0.5):
        for seq in product((0, 1), repeat=4):
            assert biased_bit(x, feeder(seq)[0]) == biased_bit(Fr(x), feeder(seq)[0])


def test_die_roll_exact():
    feed = {}
    original = ns["fair_bit"]
    try:
        ns["fair_bit"] = lambda coin: coin()            # the coin is already fair: count fair bits
        table = outcomes(die_roll, 6)
    finally:
        ns["fair_bit"] = original
    for seq, v in table.items():
        first = 4 * seq[0] + 2 * seq[1] + seq[2]
        if first < 6:
            assert v == (first + 1, 3)
        else:
            second = 4 * seq[3] + 2 * seq[4] + seq[5]
            assert v == ((second + 1, 6) if second < 6 else None)
        feed[seq] = v
    res, done = masses(feed, Fr(1, 2))
    assert set(res) == {1, 2, 3, 4, 5, 6} and len(set(res.values())) == 1
    assert done == 1 - Fr(1, 16)
    # expected fair bits 3 x 8/6 = 4; expected biased flips 4 / (p(1 - p))
    assert 3 * Fr(8, 6) == 4
    for p in q0079.P_ROWS:
        assert q0079.die_flips(p) == 4 / (p * (1 - p))


def stats_coin(p, seed):
    """The page's make_coin, counted."""
    coin, n = make_coin(p, seed), [0]

    def c():
        n[0] += 1
        return coin()
    return c, n


def test_simulated():
    for p, seed in ((0.5, 1), (0.3, 2), (0.1, 3), (0.8, 4)):
        coin, n = stats_coin(p, seed)
        runs = 20000
        ones = sum(fair_bit(coin) for _ in range(runs))
        assert abs(ones / runs - 0.5) < 4 * math.sqrt(0.25 / runs)
        e = 1 / (p * (1 - p))
        s = 2 * p * (1 - p)
        var = 4 * (1 - s) / s ** 2                  # 2 x a geometric count of rounds
        assert abs(n[0] / runs - e) < 4 * math.sqrt(var / runs) + 1e-9
    fair, n = stats_coin(0.5, 5)
    for p in (Fr(1, 3), Fr(5, 8), 1 / math.sqrt(2)):
        runs = 20000
        start = n[0]
        ones = sum(biased_bit(p, fair) for _ in range(runs))
        assert abs(ones / runs - float(p)) < 4 * math.sqrt(float(p) * (1 - float(p)) / runs)
        assert abs((n[0] - start) / runs - float(q0079.cmp_flips(Fr(p)))) < 0.06
    coin, n = stats_coin(0.3, 6)
    runs = 12000
    faces = [die_roll(coin) for _ in range(runs)]
    assert set(faces) == {1, 2, 3, 4, 5, 6}
    for f in range(1, 7):
        assert abs(faces.count(f) / runs - 1 / 6) < 4 * math.sqrt((1 / 6) * (5 / 6) / runs)
    assert abs(n[0] / runs - 4 / (0.3 * 0.7)) < 0.6


def test_tables():
    # part a: 2p(1 - p), 1/(p(1 - p)) and 100 p(1 - p) bits per 100 flips
    assert [q0079.vn_flips(p) for p in q0079.P_ROWS] == [4, Fr(9, 2), Fr(16, 3), Fr(100, 9)]
    assert [100 / q0079.vn_flips(p) for p in q0079.P_ROWS] == [25, Fr(200, 9), Fr(75, 4), 9]
    # part b: the expansions and the flips
    assert q0079.digits(Fr(1, 3), 8) == "01010101" and q0079.digits(Fr(2, 5), 8) == "01100110"
    assert [q0079.cmp_flips(p) for p in q0079.B_ROWS] == [1, Fr(3, 2), Fr(7, 4), 2, 2]
    assert [q0079.dyadic_len(p) for p in q0079.B_ROWS] == [1, 2, 3, None, None]
    # part c: four fair bits; 16, 18, 64/3 and 400/9 biased flips
    assert [q0079.die_flips(p) for p in q0079.P_ROWS] == [16, 18, Fr(64, 3), Fr(400, 9)]


def test_traps_and_follow_ups():
    # XOR of two flips: 2p(1 - p), 0.18 for p = 1/10
    assert 2 * Fr(1, 10) * Fr(9, 10) == Fr(18, 100)
    # overlapping pairs: the first differing window returns the first flip, and the next
    # windows alternate
    for seq in product((0, 1), repeat=10):
        outs = [seq[i] for i in range(9) if seq[i] != seq[i + 1]]
        if outs:
            assert outs[0] == seq[0]
            assert all(outs[i] != outs[i + 1] for i in range(len(outs) - 1))
    # ten flips compared with 1/3: 342/1024
    assert sum(1 for m in range(1024) if Fr(m, 1024) < Fr(1, 3)) == 342
    # mod 6 of three bits: 0 and 1 twice
    counts = [sum(1 for v in range(8) if v % 6 == r) for r in range(6)]
    assert counts == [2, 2, 1, 1, 1, 1]
    # entropy: 1/H(p) against von Neumann's 1/(p(1 - p))
    H = lambda p: -p * math.log2(p) - (1 - p) * math.log2(1 - p)  # noqa: E731
    assert 1 / H(0.5) == 1 and round(1 / H(1 / 3), 2) == 1.09 and q0079.vn_flips(Fr(1, 3)) == Fr(9, 2)
    # a coin from a die: each roll decides with 5/6
    assert 1 / (1 - Fr(1, 6)) == Fr(6, 5)
    # the die reusing the rejected bit: E = 3 + E'/4, E' = 2 + E'/4
    e2 = Fr(2) / (1 - Fr(1, 4))
    assert e2 == Fr(8, 3) and 3 + e2 / 4 == Fr(11, 3)
    assert round(math.log2(6), 2) == 2.58
    # the SystemVerilog loop on a double: at most 1074 digits (the smallest subnormal)
    x, k = 5e-324, 0
    while x > 0:
        x *= 2
        d = x >= 1
        x -= d
        k += 1
    assert k == 1074
    # the polynomial argument: with n flips, a set of sequences gives 0 or 1 at p -> 0
    assert PAGE.count("פון נוימן") >= 2


def test_page_numbers():
    for s in ["\\frac{1}{p(1-p)}", "\\frac{2}{2pq} = \\frac{1}{p(1-p)}", "\\frac{pq}{2pq} = \\frac12",
              "2 - 2^{1-k}", "P(1) = \\sum_{i=1}^{\\infty} p_i \\, 2^{-i} = p", "3 \\cdot \\frac{8}{6} = 4",
              "\\frac{4}{p(1-p)}", "342/1024", "11/3", "6/5", "1074", "0.18",
              'data-kind="vncoin" data-p="0.3"', 'data-kind="cmpcoin" data-p="1/3"']:
        assert s in PAGE, s
    assert re.search(r"‏16 במטבע הוגן", PAGE)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(79)


def mulberry32(seed):
    a = seed & 0xFFFFFFFF

    def rnd():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = ((a ^ (a >> 15)) * (1 | a)) & 0xFFFFFFFF
        t = ((t + (((t ^ (t >> 7)) * (61 | t)) & 0xFFFFFFFF)) & 0xFFFFFFFF) ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return rnd


def compare(digits, flips, ends):
    """The reference of bcCompare: (done, out, stop)."""
    i = 0
    while True:
        if ends and i == len(digits):
            return True, 0, i
        if i >= len(flips):
            return False, None, -1
        d = int(digits[i]) if i < len(digits) else 0
        if flips[i] != d:
            return True, d, i
        i += 1


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    got = node_json(f"const m = {explorer_require()};"
                    "const ps = [0.05, 0.3, 0.5, 0.95];"
                    "console.log(JSON.stringify({"
                    "pairs: [[0,0],[0,1],[1,0],[1,1]].map(([a, b]) => m.vnPair(a, b)),"
                    "exp: ps.map(m.vnExpected),"
                    "runs: [[1, 0.3, 50], [79, 0.5, 40], [123, 0.1, 30]].map(([s, p, n]) => m.vnRun(s, p, n)),"
                    "digits: [[1,3],[2,3],[1,5],[2,5],[3,4],[5,8],[7,16]].map(([a, b]) => m.bcDigits(a, b, 30)),"
                    "sqrt: m.bcOf('1/√2'),"
                    "ofs: ['1/3','2/3','1/5','2/5','3/4','5/8'].map((k) => m.bcOf(k)),"
                    "exps: [null, 1, 2, 3].map(m.bcExpected),"
                    "cmps: [['0101', [0,1,0,0], false], ['0101', [0,1,1], false], ['11', [1,1], true], ['11', [1], true], ['101', [1,0,1], true], ['0101', [0,1], false]]"
                    ".map(([d, f, e]) => m.bcCompare(d, f, e)),"
                    "run: m.bcRun(7, '1/3', 4000), run2: m.bcRun(8, '3/4', 4000),"
                    "}));")
    assert got["pairs"] == [None, 0, 1, None]
    for p, e in zip([0.05, 0.3, 0.5, 0.95], got["exp"]):
        assert math.isclose(e, 1 / (p * (1 - p)))
    for (seed, p, n), run in zip([(1, 0.3, 50), (79, 0.5, 40), (123, 0.1, 30)], got["runs"]):
        rnd = mulberry32(seed)
        flips = [1 if rnd() < p else 0 for _ in range(2 * n)]
        assert run["flips"] == flips
        assert run["bits"] == [flips[i] for i in range(0, 2 * n, 2) if flips[i] != flips[i + 1]]
        # the same bits as the page's fair_bit on that sequence
        coin, _ = feeder(flips)
        bits = []
        try:
            while True:
                bits.append(fair_bit(coin))
        except OutOfFlips:
            pass
        assert bits == run["bits"]
    for (a, b), d in zip([(1, 3), (2, 3), (1, 5), (2, 5), (3, 4), (5, 8), (7, 16)], got["digits"]):
        k = q0079.dyadic_len(Fr(a, b))
        assert d == q0079.digits(Fr(a, b), k if k else 30)
    s = got["sqrt"]
    assert s["ends"] is False and s["k"] is None and s["digits"] == q0079.digits(Fr(0.7071067811865476), 53)   # Math.SQRT1_2
    for o, key in zip(got["ofs"], ["1/3", "2/3", "1/5", "2/5", "3/4", "5/8"]):
        p = Fr(key)
        assert math.isclose(o["value"], float(p)) and o["k"] == q0079.dyadic_len(p)
        assert o["digits"] == q0079.digits(p, o["k"] if o["k"] else 1100)
    assert got["exps"] == [2, 1, 1.5, 1.75]
    for (d, f, e), c in zip([("0101", [0, 1, 0, 0], False), ("0101", [0, 1, 1], False), ("11", [1, 1], True),
                             ("11", [1], True), ("101", [1, 0, 1], True), ("0101", [0, 1], False)], got["cmps"]):
        done, out, stop = compare(d, f, e)
        assert (c["done"], c["out"], c["stop"]) == (done, out, stop)
    assert got["cmps"][0] == {"done": True, "out": 1, "stop": 3}       # the page's example
    # the seeded comparisons: the same counts as the reference, near p and near 2 flips
    for (seed, key, trials), run in zip([(7, "1/3", 4000), (8, "3/4", 4000)], [got["run"], got["run2"]]):
        p = Fr(key)
        k = q0079.dyadic_len(p)
        dig = q0079.digits(p, k if k else 200)
        rnd, ones, flips = mulberry32(seed), 0, 0
        for _ in range(trials):
            fl = []
            while True:
                done, out, _ = compare(dig, fl, k is not None)
                if done:
                    ones += out
                    break
                fl.append(1 if rnd() < 0.5 else 0)
                flips += 1
        assert run == {"ones": ones, "flips": flips}
        assert abs(ones / trials - float(p)) < 4 * math.sqrt(float(p) * (1 - float(p)) / trials)
        assert abs(flips / trials - float(q0079.cmp_flips(p))) < 0.1
