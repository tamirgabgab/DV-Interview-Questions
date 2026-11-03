"""Question 0077: f(1) = 1, f(3) = 3, f(2n) = f(n), f(4n+1) = 2f(2n+1) - f(n),
f(4n+3) = 3f(2n+1) - 2f(n).

Every number on the page is recomputed here with exact integers: f(2027) = 1727 by the rules
and the 13 values on the way, the table up to 16, f = R (the reversed binary digits) by the
rules up to a bound, the lemma R(2m + c) = c 2^l(m) + R(m), d(m) = f(2m+1) - f(m) = 2^l(m),
the unrolling of 13, the palindromes (f(n) = n exactly for them, 92 up to 1988, P(k), 2015
and 2047), the follow-ups; the generated blocks; and the bitrev box's models under Node
against the Python reference."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))

import q0077  # noqa: E402

PAGE = (ROOT / "docs" / "questions" / "junior" / "0077-f-of-2n-4n1-4n3.md").read_text(encoding="utf-8")
f, rev = q0077.f, q0077.rev
ell = lambda n: n.bit_length()  # noqa: E731


def test_rules_define_one_function():
    # every n >= 1 falls in exactly one case, and each case uses smaller arguments only
    for n in range(1, 5000):
        cases = [n in (1, 3), n % 2 == 0, n % 4 == 1 and n >= 5, n % 4 == 3 and n >= 7]
        assert sum(cases) == 1, n
        if n % 2 == 1 and n >= 5:
            m = n // 4
            assert m >= 1 and m < n and 2 * m + 1 < n


def test_part_a():
    assert f(2027) == 1727
    assert q0077.needed(2027) == [1, 3, 7, 15, 31, 63, 126, 127, 253, 506, 507, 1013, 2027]
    assert [f(k) for k in (7, 15, 31, 63, 127)] == [7, 15, 31, 63, 127]
    assert 2 * 127 - 63 == 191 == f(253)
    assert 3 * 191 - 2 * 63 == 447 == f(507) and 573 - 126 == 447
    assert 2 * 447 - 191 == 703 == f(1013) and 894 - 191 == 703
    assert 3 * 703 - 2 * 191 == 1727 and 2109 - 382 == 1727
    assert f(126) == 63 and f(506) == 191
    assert 2027 == 4 * 506 + 3 and 1013 == 4 * 253 + 1 and 507 == 4 * 126 + 3
    assert bin(2027)[2:] == "11111101011" and bin(1727)[2:] == "11010111111"
    assert 1024 + 512 + 128 + 32 + 16 + 8 + 4 + 2 + 1 == 1727


def test_f_is_bit_reversal():
    assert all(f(n) == rev(n) for n in range(1, 20000))
    assert [f(n) for n in range(1, 17)] == [1, 1, 3, 1, 5, 3, 7, 1, 9, 5, 13, 3, 11, 7, 15, 1]


def test_way_one_lemma_and_rules():
    for m in range(1, 3000):
        L = ell(m)
        assert rev(2 * m) == rev(m)
        assert rev(2 * m + 1) == 2 ** L + rev(m)
        assert rev(4 * m + 1) == 2 ** (L + 1) + rev(m) == 2 * rev(2 * m + 1) - rev(m)
        assert rev(4 * m + 3) == 3 * 2 ** L + rev(m) == 3 * rev(2 * m + 1) - 2 * rev(m)
    assert rev(1) == 1 and rev(3) == 3
    assert all(rev(n) >= 1 for n in range(1, 2000))


def test_way_two_d():
    d = lambda m: f(2 * m + 1) - f(m)  # noqa: E731
    assert d(1) == 2
    for m in range(1, 5000):
        assert d(2 * m) == 2 * d(m) and d(2 * m + 1) == 2 * d(m)
        assert d(m) == 2 ** ell(m)
        for c in (0, 1):
            assert f(2 * m + c) == f(m) + c * 2 ** ell(m)
    # the unrolling of 13 = 1101
    assert (f(13), f(6), f(3)) == (f(6) + 8, f(3), f(1) + 2) and f(13) == 8 + 0 + 2 + 1 == 11
    assert (ell(6), ell(3), ell(1)) == (3, 2, 1)
    # the general unrolling: f(n) = sum b_i 2^(L-1-i)
    for n in range(1, 3000):
        L = ell(n)
        assert f(n) == sum(((n >> i) & 1) << (L - 1 - i) for i in range(L))


def test_part_c():
    pals = [n for n in range(1, 1989) if f(n) == n]
    assert len(pals) == 92
    assert all(bin(n)[2:] == bin(n)[2:][::-1] for n in pals)
    assert all(n % 2 == 1 for n in pals)
    for L in range(1, 15):
        assert sum(1 for n in range(2 ** (L - 1), 2 ** L) if f(n) == n) == q0077.palindromes(L) == 2 ** ((L + 1) // 2 - 1)
    P = lambda k: sum(q0077.palindromes(L) for L in range(1, k + 1))  # noqa: E731
    for t in range(1, 8):
        assert P(2 * t) == 2 ** (t + 1) - 2 and P(2 * t + 1) == 3 * 2 ** t - 2
    assert P(10) == 62 and P(11) == 94
    big = [n for n in range(1024, 2048) if f(n) == n and n > 1988]
    assert big == [2015, 2047]
    assert bin(1988)[2:] == "11111000100" and bin(2015)[2:] == "11111011111" and int("11110111111", 2) == 1983
    assert 62 + (32 - 2) == 92
    # even n: f(n) < 2^(L-1) <= n
    assert all(f(n) < 2 ** (ell(n) - 1) <= n for n in range(2, 3000, 2))


def test_follow_ups():
    # f is one-to-one on the odd numbers, and f(f(n)) = n there
    odd = [f(n) for n in range(1, 4096, 2)]
    assert len(set(odd)) == len(odd) and all(f(f(n)) == n for n in range(1, 4096, 2))
    # f(f(n)) is the odd part of n
    for n in range(1, 4096):
        k = n
        while k % 2 == 0:
            k //= 2
        assert f(f(n)) == k
    assert f(f(12)) == f(3) == 3 and f(f(6)) == 3 and f(11) == 13
    assert f(1) == f(2) == f(4) == f(8) == 1
    # base 3: reversing the base-3 digits satisfies g(3n) = g(n), g(3n + c) = g(n) + c 3^l3(n)
    def g(n):
        d = []
        while n:
            d.append(n % 3)
            n //= 3
        v = 0
        for x in d:
            v = 3 * v + x
        return v

    def l3(n):
        k = 0
        while n:
            k, n = k + 1, n // 3
        return k
    for n in range(1, 2000):
        assert g(3 * n) == g(n)
        for c in (1, 2):
            assert g(3 * n + c) == g(n) + c * 3 ** l3(n)
    # 16-bit hardware: reverse all 16 bits, then shift right by 16 - L
    for n in range(1, 2 ** 16):
        r16 = int(format(n, "016b")[::-1], 2)
        assert r16 >> (16 - ell(n)) == rev(n)


def test_page_numbers():
    for s in ["f(2027) = 1727", "2109 - 382 = 1727", "894 - 191 = 703", "573 - 126 = 447", "254 - 63 = 191",
              "11111101011", "11010111111", "1024 + 512 + 128 + 32 + 16 + 8 + 4 + 2 + 1 = 1727",
              "f(13) = 8 + 0 + 2 + 1 = 11", "11111000100", "11111111111 = 2047", "11111011111 = 2015",
              "11110111111 = 1983", "62 + (32 − 2) = 92", "1 + 1 + 2 + 2 + 4 + 4 + 8 + 8 + 16 + 16 = 62",
              "P(10) = 2^6 - 2 = 62", "P(11) = 3 \\cdot 32 - 2 = 94", "f(11) = 13", "f(f(6)) = f(3) = 3",
              "f(f(12)) = f(3) = 3", 'data-kind="bitrev" data-n="2027"']:
        assert s in PAGE, s


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(77)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    ns = list(range(1, 4096))
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({ns}.map((n) => [m.brValue(n), m.brReverse(n), m.brIsPal(n), m.brNextPal(n)])));")
    pals = [n for n in range(1, 4096) if rev(n) == n]
    for n, (v, r, p, nxt) in zip(ns, got):
        assert v == r == f(n) == rev(n)
        assert p == (rev(n) == n)
        assert nxt == next((k for k in pals if k > n), 0)
    sample = [1, 2, 3, 6, 13, 2027, 4095, 1988, 1024]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({sample}.map((n) => [m.brRules(n), m.brSteps(n)])));")
    for n, (rules, steps) in zip(sample, got):
        assert [r["n"] for r in rules] == q0077.needed(n)
        for r in rules:
            k = r["n"]
            assert r["value"] == f(k)
            if k in (1, 3):
                assert r["rule"] == "base"
            elif k % 2 == 0:
                assert r["rule"] == "even" and r["m"] == k // 2
            else:
                m = k // 4
                assert r["rule"] == ("4m+1" if k % 4 == 1 else "4m+3") and r["m"] == m
                assert r["a"] == f(2 * m + 1) and r["b"] == f(m)
        L = ell(n)
        assert len(steps) == L + 1 and steps[-1]["acc"] == rev(n)
        for s in steps[:-1]:
            j = s["j"]
            assert s["m"] == n >> j
            assert s["acc"] + f(s["m"]) == f(n)
    # the page's example in the table: 13 rows for 2027
    assert len(got[5][0]) == 13
    assert re.search(r"‏13 ערכים|13 ערכים|נשארים רק 13", PAGE)
