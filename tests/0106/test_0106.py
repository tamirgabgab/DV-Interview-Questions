"""Question 0106, the number that appears once among threes: the numbers the page states,
recomputed from the references of tools/figures/q0106.py (a count of every value, the lanes
counted one by one, the state table of one lane), the derivation of the two lines from the
state table, the traps of the order and of the sign, the follow-ups, the generated blocks,
and the box's models under Node against the same references."""

import json
import random
import sys
from collections import Counter
from functools import reduce

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0106  # noqa: E402
from q0106 import BROKEN, EXAMPLE, K5, NEGATIVE, NINETY_NINE, TWICE, TWO_OF_THREE  # noqa: E402

ns = load_python(106)
xor = lambda nums: reduce(lambda a, b: a ^ b, nums, 0)  # noqa: E731


def thrice_arrays(rng, count, vmin=-128, vmax=127, p=1):
    for _ in range(count):
        vals = rng.sample(range(vmin, vmax + 1), rng.randint(1, 5))
        nums = [vals[0]] * p + [v for v in vals[1:] for _ in range(3)]
        rng.shuffle(nums)
        yield nums


def test_statement():
    assert q0106.odd_one(EXAMPLE) == 3 and q0106.odd_one(NINETY_NINE) == 99
    assert Counter(EXAMPLE) == {2: 3, 3: 1} and Counter(NINETY_NINE) == {0: 3, 1: 3, 99: 1}


def test_part_a():
    assert q0106.odd_one(TWICE, 2) == 4 and xor(TWICE) == 4
    acc, seen = 0, []
    for x in TWICE:
        acc ^= x
        seen.append(acc)
    assert seen == [4, 5, 7, 6, 4] and seen[1] == 4 ^ 1 and seen[3] == 4 ^ 2
    assert max(TWICE) < 8                       # three bits are enough for the table


def test_part_b_counting():
    # XOR alone gives 1, the XOR of 2 and 3
    assert xor(EXAMPLE) == 1 == 2 ^ 3
    # every lane: 3 m_b + s_b
    rng = random.Random(1)
    for nums in thrice_arrays(rng, 500, -(1 << 31), (1 << 31) - 1):
        single = q0106.odd_one(nums)
        for b, c in enumerate(q0106.lane_counts(nums)):
            assert c % 3 == q0106.bit(single, b)


def test_part_b_derivation():
    rows = q0106.derive_rows()
    assert len(rows) == 6
    for r in rows:
        assert r["o2"] == r["ox"] & (1 - r["t"])                   # ones = (ones ^ x) & ~twos
        assert r["t2"] == r["tx"] & (1 - r["o2"])                  # twos = (twos ^ x) & ~ones, the new ones
    wrong_o = [(r["t"], r["o"], r["x"]) for r in rows if r["ox"] != r["o2"]]
    wrong_t = [(r["t"], r["o"], r["x"]) for r in rows if r["tx"] != r["t2"]]
    assert wrong_o == [(1, 0, 1)] and wrong_t == [(0, 0, 1)]       # the last row and the second row
    assert [r["o2"] for r in rows if (r["t2"], r["o2"]) == (1, 0)] == [0, 0]
    assert {(r["t"], r["o"], r["x"]) for r in rows if r["t2"]} == {(0, 1, 1), (1, 0, 0)}
    # with the old ones the row 01 with a 1 loses its twos
    old = [(r["t"], r["o"], r["x"]) for r in rows if (r["tx"] & (1 - r["o"])) != r["t2"]]
    assert (0, 1, 1) in old and old == [(0, 0, 1), (0, 1, 1)]


def test_part_b_trace():
    rows = q0106.machine(EXAMPLE, 4)
    assert rows == [(2, 0), (0, 2), (1, 0), (3, 0)] == q0106.trace(EXAMPLE)
    # lane 1 counts 1, 2, 0, 1 and lane 0 only lights at the 3
    lane = lambda b: [(t >> b & 1) * 2 + (o >> b & 1) for o, t in rows]  # noqa: E731
    assert lane(1) == [1, 2, 0, 1] and lane(0) == [0, 0, 1, 1]
    assert rows[-1] == (0b0011, 0)
    # the machine of the state table and the two lines agree everywhere, negatives included
    rng = random.Random(2)
    for nums in thrice_arrays(rng, 400, -(1 << 31), (1 << 31) - 1):
        assert q0106.machine(nums) == q0106.trace(nums)
    for nums in thrice_arrays(rng, 400, p=2):
        assert q0106.machine(nums, 8) == q0106.trace(nums)


def test_part_b_negative():
    assert q0106.odd_one(NEGATIVE) == -4 and q0106.trace(NEGATIVE)[-1] == (-4, 0)
    assert ns["single_thrice"](NEGATIVE) == -4 == ns["single_thrice_count"](NEGATIVE)
    # every lane above 31 holds the state of the sign: the words are sign-extended numbers of 32 bits
    rng = random.Random(3)
    for nums in thrice_arrays(rng, 300, -(1 << 31), (1 << 31) - 1):
        for o, t in q0106.trace(nums):
            assert -(1 << 31) <= o < (1 << 31) and -(1 << 31) <= t < (1 << 31)


def test_try_it_paragraph():
    lane1 = [(t >> 1 & 1) * 2 + (o >> 1 & 1) for o, t in q0106.trace(EXAMPLE)]
    assert lane1 == [1, 2, 0, 1] and q0106.trace(EXAMPLE)[-1][0] == 3
    assert q0106.machine(NEGATIVE, 8)[-1] == (-4, 0)
    assert all(c % 3 == q0106.bit(-4, b) for b, c in enumerate(q0106.lane_counts(NEGATIVE, 8)))
    assert q0106.trace(EXAMPLE, "swap")[-1] == (0, 3)
    assert len(EXAMPLE) == 4


def test_part_c():
    # the count of a bit of the special number is p mod k
    rng = random.Random(4)
    for k in range(2, 10):
        for p in range(1, 2 * k):
            for _ in range(20):
                vals = rng.sample(range(-500, 500), rng.randint(1, 5))
                nums = [vals[0]] * p + [v for v in vals[1:] for _ in range(k)]
                words, orr = q0106.sliced(nums, k)
                assert all(c % k == q0106.bit(vals[0], b) * (p % k) for b, c in enumerate(q0106.lane_counts(nums)))
                if p % k:
                    assert orr == vals[0] and ns["single_mod_k"](nums, k) == vals[0]
                else:
                    assert orr == 0 and ns["single_mod_k"](nums, k) == 0
    # one number twice among threes: ones 0 and twos the number
    assert q0106.trace(TWO_OF_THREE)[-1] == (0, 5) and ns["single_thrice_any"](TWO_OF_THREE) == 5
    # k = 3 sliced: the same encoding as ones and twos
    for nums in thrice_arrays(rng, 300, -1000, 1000, p=rng.choice([1, 2])):
        assert q0106.sliced(nums, 3)[0] == list(q0106.trace(nums)[-1])
    # the words: ceil(log2 k)
    assert [(k - 1).bit_length() for k in (5, 3, 4, 2)] == [3, 2, 2, 1]
    # the k = 5 example
    assert Counter(K5) == {7: 5, -1: 5, 6: 2}
    c = q0106.lane_counts(K5, 32)
    assert c[0] == 10 and c[1] == c[2] == 12 and all(v == 5 for v in c[3:])
    assert [v % 5 for v in c[:8]] == [0, 2, 2, 0, 0, 0, 0, 0]
    words, orr = q0106.sliced(K5, 5)
    assert words == [0, 6, 0] and orr == 6 and ns["single_mod_k"](K5, 5) == 6
    # k = 4: the counter wraps by itself; at most 3m operations a number
    assert (3 + 1) % 4 == 0


def test_traps():
    # XOR alone: the XOR of the distinct values
    assert xor(EXAMPLE) == 1 and xor(NINETY_NINE) == 98 == 0 ^ 1 ^ 99
    rng = random.Random(5)
    for nums in thrice_arrays(rng, 300):
        assert xor(nums) == xor(set(nums))
    # the order: twos first runs the counter backwards, 00, 10, 01, 00
    lane = [(t & 1) * 2 + (o & 1) for o, t in q0106.trace([1, 1, 1], "swap")]
    assert lane == [2, 1, 0]
    assert q0106.trace(EXAMPLE, "swap")[-1] == (0, 3)
    for nums in thrice_arrays(rng, 300):
        assert q0106.trace(nums, "swap")[-1] == (0, q0106.odd_one(nums))
    # both from the old values: 11 after the first number, both 0 at the end
    old = q0106.trace(EXAMPLE, "old")
    assert old[0] == (2, 2) and old[-1] == (0, 0)
    # the sign: without the last line, -4 + 2^32; a mask on single_thrice does the same
    def count_unsigned(nums):
        res = 0
        for b in range(32):
            if sum((x >> b) & 1 for x in nums) % 3:
                res |= 1 << b
        return res

    def masked(nums):
        ones = twos = 0
        for x in nums:
            ones = (ones ^ x) & ~twos & 0xFFFFFFFF
            twos = (twos ^ x) & ~ones & 0xFFFFFFFF
        return ones

    assert count_unsigned(NEGATIVE) == 4294967292 == -4 + 2 ** 32 == masked(NEGATIVE)
    # the dictionary holds every distinct value, about a third of the array
    for nums in thrice_arrays(rng, 300):
        assert len(Counter(nums)) == (len(nums) - 1) // 3 + 1
    assert len(Counter(NEGATIVE)) == 4


def test_followups():
    rng = random.Random(6)
    # the hardware: the mux form from the old values, lane by lane, gives the same words
    for nums in thrice_arrays(rng, 300, -(1 << 31), (1 << 31) - 1, p=rng.choice([1, 2])):
        ones = twos = 0
        for x in nums:
            ones, twos = (~ones & ~twos & x) | (ones & ~x), (ones & x) | (twos & ~x)
        assert (ones, twos) == q0106.trace(nums)[-1]
    assert 2 * 32 == 64
    # two singles among pairs
    for _ in range(500):
        vals = rng.sample(range(-1000, 1000), rng.randint(2, 7))
        a, b = vals[0], vals[1]
        nums = [a, b] + [v for v in vals[2:] for _ in range(2)]
        rng.shuffle(nums)
        d = xor(nums)
        assert d == a ^ b != 0
        low = d & -d
        x = xor([v for v in nums if v & low])
        assert {x, d ^ x} == {a, b}
    # checking the answer: a second pass catches [2, 3, 2, 5, 2] but not [1, 4, 4]
    assert ns["single_thrice"](BROKEN) == 6 and 6 not in BROKEN and Counter(BROKEN) == {2: 3, 3: 1, 5: 1}
    assert ns["single_thrice"]([1, 4, 4]) == 1 and Counter([1, 4, 4]) == {1: 1, 4: 2}


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(106)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(106)
    cases = [EXAMPLE, NINETY_NINE, NEGATIVE, TWO_OF_THREE, BROKEN, [1, 4, 4], [-128, 127, -128, 127, -128, 127, 0]]
    for _ in range(300):
        cases.append([rng.randint(-128, 127) for _ in range(rng.randint(1, 16))])
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(cases)}.map((a) => [m.thTrace(a), m.thTrace(a, 'swap'), m.thTrace(a, 'old'), m.thLanes(a), m.thOdd(a), m.thLane(a)])));")
    for nums, (good, swap, old, lanes, odd, lane) in zip(cases, got):
        assert [tuple(r) for r in good] == q0106.trace(nums) == q0106.machine(nums, 8)
        assert [tuple(r) for r in swap] == q0106.trace(nums, "swap")
        assert [tuple(r) for r in old] == q0106.trace(nums, "old")
        assert lanes == q0106.lane_counts(nums, 8)
        assert odd == [[v, c] for v, c in Counter(nums).items() if c % 3]
        assert lane == lanes.index(max(lanes))
    presets = node_json(f"const m = {explorer_require()};console.log(JSON.stringify(m.thPresets));")
    assert [p[1] for p in presets] == [EXAMPLE, NINETY_NINE, NEGATIVE, TWO_OF_THREE, BROKEN]
    assert [p[1] for p in presets][4] == BROKEN and len(Counter(BROKEN)) == 3
    assert [lanes.index(max(lanes)) for lanes in (q0106.lane_counts(EXAMPLE, 8),)] == [1]
    parsed = node_json(f"const m = {explorer_require()};"
                       "console.log(JSON.stringify(['2, 2, 3, 2', '2.2.3.2', '-2 −3', '127,-128', '128', '-129', '', '1,,2', 'a', '1.5',"
                       " Array(16).fill(1).join(','), Array(17).fill(1).join(',')].map((t) => m.thParse(t))));")
    assert parsed == [[2, 2, 3, 2], [2, 2, 3, 2], [-2, -3], [127, -128], None, None, None, [1, 2], None, [1, 5], [1] * 16, None]
