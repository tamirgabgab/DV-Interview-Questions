"""Question 0107, the largest number from concatenation: the numbers the page states, recomputed from
the references of tools/figures/q0107.py; part b's theorem (a + b >= b + a exactly when
rho(a) >= rho(b), the exchange argument, every sorted order gives one string) checked on random
lists; part c's rule against the brute force, the shortcut's failures, the traps, the follow-ups
(the key, the checker without a reference, the hardware comparison, the faster first choice),
the generated blocks, and the box's models under Node against the same references."""

import json
import math
import random
import sys
from fractions import Fraction
from itertools import permutations

import pytest

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0107  # noqa: E402
from q0107 import EXAMPLE, rho  # noqa: E402

POOL = [0, 1, 2, 3, 9, 10, 11, 12, 20, 21, 30, 31, 34, 100, 101, 110, 121, 1001, 1010, 1212, 12121, 2121, 99, 98, 989,
        1100, 10010, 100100, 1001001, 201, 210, 2010, 120, 102]


def rand_list(rng, nmax, zeros=True, vmax=2000):
    n = rng.randint(1, nmax)
    return [rng.choice(POOL if zeros else POOL[1:]) if rng.random() < 0.7 else rng.randint(0 if zeros else 1, vmax) for _ in range(n)]


def test_statement():
    assert q0107.largest(EXAMPLE) == q0107.largest_brute(EXAMPLE) == "9534330"
    assert q0107.ascending(EXAMPLE)[::-1] == ["9", "5", "34", "3", "30"]
    assert "3" + "30" == "330" and "330" > "303"


def test_part_a():
    # numeric descending puts 34 and 30 before 9; string descending puts "30" before "3"
    assert "".join(q0107.num_sort(EXAMPLE)) == "3430953" and q0107.num_sort(EXAMPLE)[:3] == ["34", "30", "9"]
    assert "".join(q0107.str_sort(EXAMPLE)) == "9534303" and "30" > "3"
    assert "9534303" < "9534330" and "3430953" < "9534330"
    # the adjacent pairs of the answer
    assert [(a + b, b + a) for a, b in [("9", "5"), ("5", "34"), ("34", "3"), ("3", "30")]] == \
        [("95", "59"), ("534", "345"), ("343", "334"), ("330", "303")]
    # the swap of two neighbours changes only their block: the same prefix, suffix and length
    rng = random.Random(1)
    for _ in range(2000):
        s = [str(x) for x in rand_list(rng, 7)]
        if len(s) < 2:
            continue
        i = rng.randrange(len(s) - 1)
        t = s[:i] + [s[i + 1], s[i]] + s[i + 2:]
        a, b = "".join(s), "".join(t)
        assert len(a) == len(b) and (a > b) == (s[i] + s[i + 1] > s[i + 1] + s[i]) and (a == b) == (s[i] + s[i + 1] == s[i + 1] + s[i])


def test_part_b_rho():
    # a + b >= b + a exactly when rho(a) >= rho(b), on random pairs (the three lines of the page)
    rng = random.Random(2)
    for _ in range(20000):
        a, b = (str(rng.choice(POOL) if rng.random() < 0.5 else rng.randint(0, 10 ** rng.randint(1, 7))) for _ in range(2))
        A, B = int(a), int(b)
        assert (a + b >= b + a) == (A * 10 ** len(b) + B >= B * 10 ** len(a) + A) == \
            (A * (10 ** len(b) - 1) >= B * (10 ** len(a) - 1)) == (rho(a) >= rho(b))
        # rho(a) is 0.aaaa...: the first 12 digits of the expansion are a repeated
        if a != "0" and set(a) != {"9"}:
            assert math.floor(rho(a) * 10 ** (12 * len(a))) // 10 ** (11 * len(a)) == int(a * 12) // 10 ** (11 * len(a))
    # the table of the example
    assert [rho(a) for a in ("9", "5", "34", "3", "30")] == [1, Fraction(5, 9), Fraction(34, 99), Fraction(1, 3), Fraction(10, 33)]
    assert [q0107.dec(a) for a in ("9", "5", "34", "3", "30")] == ["1", "0.555555…", "0.343434…", "0.333333…", "0.303030…"]
    assert rho("12") == rho("1212") == Fraction(4, 33) and "12" + "1212" == "1212" + "12" == "121212"
    assert rho("0") == 0 and float(rho("3")) > float(rho("30")) and round(float(rho("30")), 4) == 0.303


def test_part_b_exchange_and_ties():
    rng = random.Random(3)
    for _ in range(1500):
        s = [str(x) for x in rand_list(rng, 6)]
        best = max("".join(p) for p in permutations(s))
        for p in set(permutations(s)):
            inverted = any(rho(p[i]) < rho(p[i + 1]) for i in range(len(p) - 1))
            if inverted:   # a swap of an inverted pair raises the number strictly
                i = next(i for i in range(len(p) - 1) if rho(p[i]) < rho(p[i + 1]))
                q = p[:i] + (p[i + 1], p[i]) + p[i + 2:]
                assert "".join(q) > "".join(p)
            else:          # every sorted order gives the maximum
                assert "".join(p) == best
        # equal rho: the two strings commute
        for a in s:
            for b in s:
                assert (rho(a) == rho(b)) == (a + b == b + a)
    assert math.factorial(8) == 40320


def test_part_c():
    # the lead's brute force and the table
    for nums, want in [([0, 1, 10], "1001"), ([3, 30, 34, 5, 9], "3033459"), ([0, 0, 1], "100"), ([20, 1, 0], "1020"), ([0, 2, 21], "2021")]:
        assert q0107.smallest_brute(nums) == q0107.smallest(nums) == want
    assert [q0107.shortcut(n) for n in q0107.SMALL] == ["1001", "3033459", "100", "1020", "2102"]
    assert ["".join(q0107.ascending(n)) for n in q0107.SMALL] == ["0101", "3033459", "001", "0120", "0212"]
    # the ascending order puts every zero first; stripping them drops digits
    assert "".join(q0107.ascending([0, 1, 10])).lstrip("0") == "101" and len("101") < len("1001")
    # 21 comes before 2 by the rule, but 2 wins as the first: 21 0 2 against 2 0 21
    assert "21" + "2" == "212" < "221" == "2" + "21" and q0107.ascending([2, 21]) == ["21", "2"]
    assert q0107.candidates([0, 2, 21]) == [("21", "2102"), ("2", "2021")] and "2021" < "2102"
    # zeros first: 0 + a < a + 0 for every a that does not start with 0
    for a in POOL[1:]:
        assert "0" + str(a) < str(a) + "0"
    # the rule against the brute force on random lists with zeros
    rng = random.Random(4)
    fails = 0
    for _ in range(6000):
        nums = rand_list(rng, 6)
        b = q0107.smallest_brute(nums)
        assert q0107.smallest(nums) == b, nums
        fails += q0107.shortcut(nums) != b
    assert fails > 0
    # the box's "try it": 0, 11, 1 keeps 11 first (a tie), and the shortcut gives 1101
    assert q0107.ascending([0, 11, 1]) == ["0", "11", "1"] and q0107.shortcut([0, 11, 1]) == "1101" and q0107.smallest([0, 11, 1]) == "1011"
    # without zeros the first candidate is the ascending order itself
    for _ in range(2000):
        nums = rand_list(rng, 7, zeros=False)
        assert q0107.candidates(nums)[0][1] == "".join(q0107.ascending(nums)) == q0107.smallest(nums)


def test_traps():
    from functools import cmp_to_key

    # a comparator that returns a bool is never negative: the sort keeps the input order
    for f in (lambda a, b: a + b > b + a, lambda a, b: a + b < b + a):
        assert "".join(sorted(map(str, EXAMPLE), key=cmp_to_key(f))) == "3303459"
    assert q0107.bool_cmp_sort(EXAMPLE) == "3303459"
    # "00", the trap of all zeros
    assert "".join(q0107.ascending([0, 0])[::-1]) == "00" and q0107.largest([0, 0]) == "0"
    # the result as a number: 20 digits do not fit a longint; Python refuses int() of over 4,300 digits
    s = "2147483647" + "2147483646"
    assert len(s) == 20 and int(s) > 2 ** 63 - 1 and round((2 ** 63 - 1) / 1e18, 1) == 9.2
    assert 500 * 9 == 4500 > 4300
    if sys.version_info >= (3, 11):
        assert sys.get_int_max_str_digits() in (0, 4300) or True
        old = sys.get_int_max_str_digits()
        sys.set_int_max_str_digits(4300)
        try:
            with pytest.raises(ValueError):
                int("9" * 4500)
        finally:
            sys.set_int_max_str_digits(old)
    # string sort is right on lists without a prefix pair, so short random tests can miss it
    assert "".join(q0107.str_sort([5, 34, 9])) == q0107.largest([5, 34, 9])


def test_followups():
    rng = random.Random(5)
    # the key: a repeated up to length 2L gives the same order as rho (Fine and Wilf)
    for _ in range(3000):
        s = [str(x) for x in rand_list(rng, 8, vmax=10 ** 6)]
        L = max(map(len, s))
        key = lambda a: (a * (2 * L))[: 2 * L]  # noqa: E731
        assert "".join(sorted(s, key=key, reverse=True)) == q0107.largest(s) or q0107.largest(s) == "0"
        for a in s:
            for b in s:
                assert (key(a) > key(b)) == (rho(a) > rho(b)) and (key(a) == key(b)) == (rho(a) == rho(b))
    # Fine and Wilf: two periodic strings that agree on |a| + |b| digits agree forever
    for _ in range(20000):
        a, b = (str(rng.choice(POOL[1:]) if rng.random() < 0.6 else rng.randint(1, 10 ** rng.randint(1, 4))) for _ in range(2))
        m = len(a) + len(b)
        if (a * m)[:m] == (b * m)[:m]:
            assert rho(a) == rho(b)
    # the checker without a reference: a permutation whose neighbours all satisfy a + b >= b + a is the maximum
    for _ in range(1500):
        s = [str(x) for x in rand_list(rng, 6)]
        best = max("".join(p) for p in permutations(s))
        for p in set(permutations(s)):
            if all(p[i] + p[i + 1] >= p[i + 1] + p[i] for i in range(len(p) - 1)):
                assert "".join(p) == best
    # the hardware comparison: a * (10^|b| - 1) against b * (10^|a| - 1), the product as wide as the sum of the widths
    for _ in range(20000):
        A, B = rng.randint(0, 2 ** 31 - 1), rng.randint(0, 2 ** 31 - 1)
        a, b = str(A), str(B)
        pa, pb = A * (10 ** len(b) - 1), B * (10 ** len(a) - 1)
        assert (pa > pb) == (a + b > b + a) and (pa == pb) == (a + b == b + a)
        assert pa.bit_length() <= A.bit_length() + (10 ** len(b) - 1).bit_length()
    # the faster first choice: the block x + 0^z smallest by rho, the longest on a tie (tens of thousands of lists)
    for _ in range(30000):
        nums = rand_list(rng, 8)
        assert q0107.block_rule(nums) == q0107.smallest(nums), nums
    for _ in range(3000):
        nums = rand_list(rng, 6)
        assert q0107.block_rule(nums) == q0107.smallest_brute(nums), nums
    # the shortest of a tie would be wrong: 10 and 10010 have the same block with one zero
    assert rho("10" + "0") == rho("10010" + "0") and q0107.smallest([0, 10, 10010, 1001]) == q0107.smallest_brute([0, 10, 10010, 1001])


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(107)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(107)
    cases = [EXAMPLE, [3, 30], [12, 1212], [0, 0], [0, 1, 10], [0, 0, 1], [20, 1, 0], [0, 2, 21], [0, 11, 1], [7]]
    for _ in range(400):
        cases.append(rand_list(rng, 8, vmax=999999))
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(cases)}.map((v) => {{ const s = v.map(String), sm = m.ccSmallest(v);"
                    " return [m.ccLargest(v), sm.best, sm.cands.map((c) => [c[0], c[2]]), sm.order.map((i) => s[i]).join(''),"
                    " m.ccShortcut(v).map((i) => s[i]).join(''), m.ccNumSort(v, true).map((i) => s[i]), m.ccStrSort(v, true).map((i) => s[i]),"
                    " m.ccNumSort(v, false).map((i) => s[i]), m.ccSorted(s, false).map((i) => s[i]), s.map((a) => m.ccDec(a))]; })));")
    for nums, (big, small, cands, order, short, nd, sd, na, up, decs) in zip(cases, got):
        assert big == q0107.largest(nums)
        assert small == q0107.smallest(nums) and (order == small or set(order) == {"0"} == set(small))
        assert [tuple(c) for c in cands] == q0107.candidates(nums)
        assert (short.lstrip("0") or "0") == q0107.shortcut(nums)
        assert nd == q0107.num_sort(nums) and sd == q0107.str_sort(nums)
        assert na == q0107.num_sort(nums, False) and up == q0107.ascending(nums)
        assert decs == [q0107.dec(str(x)) for x in nums]
    presets = node_json(f"const m = {explorer_require()};console.log(JSON.stringify(m.ccPresets));")
    assert [p[1] for p in presets] == [EXAMPLE, [3, 30], [12, 1212], [0, 0], [0, 1, 10], [0, 0, 1], [20, 1, 0], [0, 2, 21]]
    parsed = node_json(f"const m = {explorer_require()};"
                       "console.log(JSON.stringify(['3, 30, 34', '3.30.34', '7', '0 999999', '1,,2', '', '1, 1000000', '-1, 2', 'a, 2',"
                       " '1,2,3,4,5,6,7,8', '1,2,3,4,5,6,7,8,9', '007'].map((t) => m.ccParse(t))));")
    assert parsed == [[3, 30, 34], [3, 30, 34], [7], [0, 999999], [1, 2], None, None, None, None, list(range(1, 9)), None, [7]]
    # the box's "try it" lists: the string sort of the example, 3 against 30, the equal pair, and part c's lists
    assert "".join(q0107.str_sort(EXAMPLE)) == "9534303" and "3" + "30" > "30" + "3" and "12" + "1212" == "1212" + "12"
    assert q0107.shortcut([0, 2, 21]) == "2102" and q0107.smallest([0, 2, 21]) == "2021" and q0107.shortcut([0, 1, 10]) == "1001"
