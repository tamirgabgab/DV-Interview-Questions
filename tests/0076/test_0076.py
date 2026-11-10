"""Question 0076: a strictly increasing f on the positive integers with f(f(n)) = 3n.

Every number on the page is recomputed here with exact integers: the forced f(1) = 2, the
chain, f(14) = 23 by counting, the formula of part b against a brute-force search that
builds every strictly increasing f with f(f(n)) = 3n on a window (there is exactly one),
the base-3 rule, f(2027) = 3894 and its check, the follow-ups (f(n) = 2n only at powers of
3, 100 is no value of f, no f with f(f(n)) = 2n); the generated blocks; and the ffn box's
models under Node against the Python reference."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))

import q0076  # noqa: E402

PAGE = (ROOT / "docs" / "questions" / "junior" / "0076-f-of-f-is-3n.md").read_text(encoding="utf-8")
f, base3 = q0076.f, q0076.base3


def increasing_solutions(m: int, k: int = 3) -> list[dict]:
    """Every strictly increasing f on 1..m with f(f(n)) = k n wherever both sides are in the
    window. f(n) >= n (strictly increasing on the positive integers), so f(n) <= f(f(n)) = kn."""
    out, g = [], {}

    def ok(n, v):
        if v == n:
            return False                      # f(n) = n gives f(f(n)) = n, not kn
        if v in g and g[v] != k * n:
            return False
        return all(v == k * a for a, b in g.items() if b == n)

    def rec(n, lo):
        if n > m:
            out.append(dict(g))
            return
        for v in range(lo, k * n + 1):
            if ok(n, v):
                g[n] = v
                rec(n + 1, v + 1)
                del g[n]

    rec(1, 1)
    return out


def test_f1_is_forced():
    # f(1) = 1 gives f(f(1)) = 1; f(1) = a >= 3 needs f(a) = 3 < a < f(a)
    firsts = {s[1] for s in increasing_solutions(12)}
    assert firsts == {2}


def test_chain_and_counting():
    chain = [1]
    while chain[-1] < 27:
        chain.append(f(chain[-1]))
    assert chain == [1, 2, 3, 6, 9, 18, 27]
    for a, b in zip(chain, chain[1:]):
        assert f(b) == 3 * a                          # f(f(a)) = 3a
    # nine steps from 9 to 18 and nine numbers from 18 to 27: each step rises by one
    assert [f(n) for n in range(9, 19)] == list(range(18, 28))
    assert f(14) == 23 and f(23) == 42 == 3 * 14
    assert (f(4), f(5)) == (7, 8)
    assert 27 + 3 * 5 == 42 and f(27) == 54


def test_formula_is_the_unique_solution():
    sols = increasing_solutions(60)
    assert len(sols) == 1
    assert all(sols[0][n] == f(n) for n in range(1, 61))


def test_formula_properties():
    vals = [f(n) for n in range(1, 30001)]
    assert all(a < b for a, b in zip(vals, vals[1:]))
    assert all(f(f(n)) == 3 * n for n in range(1, 30001))
    for k in range(0, 15):
        p = 3 ** k
        assert f(p) == 2 * p and f(2 * p) == 3 * p
        # both formulas meet at the boundaries
        assert 2 * p + p == 3 * (2 * p) - 3 * p
        assert 3 * (3 * p) - 3 * p == 3 * p + 3 * p


def test_base3_rule():
    for n in range(1, 30001):
        b = base3(n)
        rule = "2" + b[1:] if b[0] == "1" else "1" + b[1:] + "0"
        assert base3(f(n)) == rule
        assert base3(f(f(n))) == b + "0"
    assert (base3(14), base3(23), base3(42)) == ("112", "212", "1120")
    assert (base3(2027), base3(3894)) == ("2210002", "12100020")


def test_part_c():
    assert (3 ** 6, 2 * 3 ** 6, 3 ** 7) == (729, 1458, 2187)
    assert 1458 <= 2027 <= 2187 and 3 * 2027 == 6081
    assert f(2027) == 6081 - 2187 == 3894
    assert 2187 <= 3894 <= 4374 and f(3894) == 3894 + 2187 == 6081


def test_follow_ups():
    # f(n) = 2n exactly at the powers of 3
    assert [n for n in range(1, 100001) if f(n) == 2 * n] == [3 ** k for k in range(11)]
    # 100 is no value of f: the values in [81, 162] are 3m - 81
    values = {f(m) for m in range(1, 200)}
    assert 100 not in values and all(v % 3 == 0 for v in values if 81 <= v <= 162)
    # no strictly increasing f with f(f(n)) = 2n, not even on 1..6
    assert increasing_solutions(6, k=2) == []


def test_page_numbers():
    for s in ["f(14) = 23", "f(2027) = 3894", "6081 - 2187 = 3894", "f(3894) = 3894 + 2187 = 6081",
              "2 \\cdot 3^6 = 1458", "3^7 = 2187", "2027 = 2210002", "12100020"]:
        assert s in PAGE, s
    rows = re.findall(r"^\s*\| (\d+) \|", PAGE, re.M)
    assert [int(r) for r in rows] == q0076.BASE3_EXAMPLES


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(76)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    ns = list(range(1, 3001)) + [6560, 6561, 6562, 13122, 2027, 3894, 999999999, 387420489, 774840978]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({ns}.map((n) => [m.ffSplit(n), m.ffValue(n), m.ffBase3(n), m.ffRule(n)])));")
    for n, (s, v, b, r) in zip(ns, got):
        p = 1
        while 3 * p <= n:
            p *= 3
        assert s["p"] == p and 3 ** s["k"] == p and s["mid"] == 2 * p and s["top"] == 3 * p
        assert s["half"] == (1 if n <= 2 * p else 2)
        assert v == s["value"] == f(n)
        assert b == base3(n) and r == base3(f(n))


def test_ratio_and_box_tasks():
    """f(n)/n swings between exactly 3/2 (at 2·3^k) and 2 (at 3^k), on both sides of sqrt(3);
    the numbers of the "try it" paragraph next to the box."""
    from fractions import Fraction

    ratios = [Fraction(f(n), n) for n in range(1, 100001)]
    assert min(ratios) == Fraction(3, 2) and max(ratios) == 2
    assert all(Fraction(f(2 * 3 ** k), 2 * 3 ** k) == Fraction(3, 2) for k in range(12))
    chain = [14]
    for _ in range(4):
        chain.append(f(chain[-1]))
    assert chain == [14, 23, 42, 69, 126]
    assert [base3(x) for x in chain] == ["112", "212", "1120", "2120", "11200"]
    assert [f(n) for n in (17, 18, 19)] == [26, 27, 30]
    assert [f(n) for n in (26, 27, 28)] == [51, 54, 55] and (base3(26), base3(27)) == ("222", "1000")
    assert (f(60), f(61)) == (99, 102)
    # part a's check: 21 = f(12) with 12 and 21 in the same interval [9, 27]
    assert f(12) == 21 and f(27) == f(f(18)) == 54
