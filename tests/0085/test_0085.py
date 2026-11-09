"""Question 0085: the self-describing number.

The generator's search against a brute force over every string of b digits (b <= 6) and
against the list of part c (b <= 16), the two sums, part b's case analysis, the numbers of
the page (980 candidates and 4,845 cuts in base 10, 184,746 with the first sum only, 32,523
up to base 16, base 16's number), guess and fix (the counts copied as the new number: the
cycle from 9000000000, base 4 from 3000), the follow-ups on n digits in base 10 and on
starting d[0] from 1, the one-bit sum of the SV trap, the generated blocks, and the box's
models under Node against the reference."""

import itertools
import json
import random
import sys

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))

import q0085  # noqa: E402

PAGE = (ROOT / "docs" / "questions" / "junior" / "0085-self-describing-number.md").read_text(encoding="utf-8")


def brute(b):
    return [list(d) for d in itertools.product(range(b), repeat=b) if q0085.is_self(d)]


def test_search_against_brute_force():
    for b in range(2, 7):
        assert q0085.search(b)[0] == brute(b), b


def test_search_against_the_list():
    for b in q0085.BASES:
        assert q0085.search(b)[0] == q0085.family(b), b
    assert [q0085.text(d) for d in q0085.family(10)] == ["6210001000"]
    assert [q0085.text(d) for d in q0085.family(4)] == ["1210", "2020"]
    assert [q0085.text(d) for d in q0085.family(5)] == ["21200"]
    assert [q0085.text(d) for d in q0085.family(7)] == ["3211000"]
    assert [q0085.text(d) for d in q0085.family(11)] == ["72100001000"]
    assert all(q0085.family(b) == [] for b in (2, 3, 6))


def test_the_two_sums():
    for b in q0085.BASES:
        for d in q0085.family(b):
            assert sum(d) == b and sum(i * x for i, x in enumerate(d)) == b
            # (*): sum over i >= 2 of (i - 1) d[i] is the number of zeros
            assert sum((i - 1) * x for i, x in enumerate(d) if i >= 2) == d[0]


def test_part_b_cases():
    assert q0085.cases(10) == [(1, 8, False), (2, 6, False), ("≥ 3", 2, True)]
    # by base: z = 1 only in base 4 (1210), z = 2 in bases 4 and 5, z >= 3 from base 7
    for b in q0085.BASES:
        z = {d[0] for d in q0085.family(b)}
        assert (1 in z) == (b == 4) and (2 in z) == (b in (4, 5)) and any(x >= 3 for x in z) == (b >= 7)


def without_weight(b):
    """The full candidates of the search that cuts by the first sum only."""
    n = 0

    def rec(i, total):
        nonlocal n
        if i == b:
            n += 1
            return
        for v in range(b):
            if total + v > b:
                break
            rec(i + 1, total + v)

    rec(0, 0)
    return n


def test_page_numbers():
    sols, checked, cuts = q0085.search(10)
    assert (checked, cuts) == (980, 4845)
    assert "980 מועמדים" in PAGE and "מועמדים מלאים 980 | חיתוכים 4,845" in PAGE
    assert without_weight(10) == 184746 and "184,746" in PAGE
    assert round(184746 / 980) == 189 and "בערך פי 190" in PAGE
    total = sum(q0085.search(b)[1] for b in q0085.BASES)
    assert total == 32523 and "32,523" in PAGE
    assert q0085.search(16)[1] == 10459 and "10,459" in PAGE
    assert q0085.text(q0085.family(16)[0]) == "C210000000001000" and "C210000000001000" in PAGE
    assert q0085.family(16)[0][12] == 1


def copies(d):
    """Guess and fix: d replaced by its counts until a number comes back (or a count is
    not a digit); the numbers in order, the repeated one last."""
    out = [list(d)]
    while True:
        c = q0085.counts(out[-1])
        if max(c) >= len(d):
            return out
        seen = c in out
        out.append(c)
        if seen:
            return out


def test_guess_and_fix():
    walk = [q0085.text(d) for d in copies([9] + [0] * 9)]
    assert walk == ["9000000000", "9000000001", "8100000001", "7200000010", "7110000100",
                    "6300000100", "7101001000", "6300000100"]
    assert "אחרי חמש\n    העתקות ל-6300000100, משם ל-7101001000, ומשם שוב ל-6300000100" in PAGE
    assert "אחרי שבע העתקות" in PAGE
    assert [q0085.text(d) for d in copies([3, 0, 0, 0])] == ["3000", "3001", "2101", "1210", "1210"]
    assert "מ-3000, והעתיקו שלוש פעמים" in PAGE
    # "fewer than a third" of 20,000 random starts reach 6210001000
    rng = random.Random(1)
    hits = sum(copies([rng.randrange(10) for _ in range(10)])[-1] == q0085.family(10)[0] for _ in range(20000))
    assert 0.25 < hits / 20000 < 1 / 3 and "פחות משליש" in PAGE


def test_start_from_one_zero():
    """The follow-up: d[0] >= 1 in every solution (part b), so the search may start d[0] at 1."""
    def checked(b, low):
        n = 0

        def rec(i, total, weight):
            nonlocal n
            if i == b:
                n += 1
                return
            for v in range(low if i == 0 else 0, b):
                if total + v > b or weight + i * v > b:
                    break
                rec(i + 1, total + v, weight + i * v)

        rec(0, 0, 0)
        return n

    assert (checked(10, 1), checked(10, 0)) == (843, 980) and "843 מועמדים" in PAGE
    first = next(k for k, e in enumerate(q0085.events(4)) if e[1] and e[1][0] >= 1)
    assert first == 22 and "כל 22 הצעדים הראשונים" in PAGE


def test_one_bit_sum():
    """The SV trap: with the counts taken modulo 2 every digit is 0 or 1, and the only string
    of 10 such digits whose digit i is its count of i modulo 2 is 0000000000."""
    mod2 = [d for d in itertools.product(range(2), repeat=10) if all(d[i] == d.count(i) % 2 for i in range(10))]
    assert mod2 == [(0,) * 10] and "0000000000" in PAGE


def test_search_box_task():
    """The numbers of the search box's task: the first cut at step 3, 1210 at step 39, 2020
    at step 50, base 6 in 425 steps."""
    ev = q0085.events(4)
    assert ev[2] == ("cut", (0, 0, 0), 2)
    assert [k + 1 for k, e in enumerate(ev) if e[0] == "check" and e[2]] == [39, 50]
    assert len(q0085.events(6)) == 425
    for t in ("בצעד 3", "בצעד 39", "בצעד 50", "425 צעדים"):
        assert t in PAGE, t


def test_n_digits_in_base_10():
    """The follow-up: an n-digit number in base 10 whose digit i counts the i's (i < n) is
    a number of base n: a digit v >= n would make every digit equal, and then v = j < n."""
    for n in range(1, 8):
        found = []

        def rec(pre, total):
            if len(pre) == n:
                if all(pre.count(i) == pre[i] for i in range(n)):
                    found.append(list(pre))
                return
            for v in range(10):
                t = total + (v if v < n else 0)
                if t <= n:
                    rec(pre + [v], t)

        rec([], 0)
        assert found == (q0085.family(n) if n >= 2 else []), n


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(85)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    bases = list(range(2, 9))
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(bases)}.map((b) => m.sdEvents(b))));")
    for b, ev in zip(bases, got):
        want = q0085.events(b)
        assert [(e["kind"], tuple(e["pre"]), e["v"]) if e["kind"] == "cut" else (e["kind"], tuple(e["d"]), e["ok"])
                for e in ev] == list(want), b
    all_b = list(q0085.BASES)
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(all_b)}.map((b) => [m.sdSearch(b), m.sdFamily(b)])));")
    for b, (res, fam) in zip(all_b, got):
        sols, checked, cuts = q0085.search(b)
        assert res == {"sols": sols, "checked": checked, "cuts": cuts}, b
        assert fam == q0085.family(b), b
    cases = [["6210001000", 10], ["1210", 4], ["c210000000001000", 16], ["12 10", 4], ["1240", 4], ["121", 4], ["", 2], ["2A", 10]]
    parsed = node_json(f"const m = {explorer_require()};console.log(JSON.stringify({json.dumps(cases)}.map(([t, b]) => m.sdParse(t, b))));")
    assert parsed == [[6, 2, 1, 0, 0, 0, 1, 0, 0, 0], [1, 2, 1, 0], q0085.family(16)[0], [1, 2, 1, 0], None, None, None, None]
    counts = node_json(f"const m = {explorer_require()};console.log(JSON.stringify(m.sdCounts([9, 0, 0, 0, 0, 0, 0, 0, 0, 0])));")
    assert counts == q0085.counts([9, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == [9, 0, 0, 0, 0, 0, 0, 0, 0, 1]
