"""Question 0052: the page's corr, expected_tosses, race, generating, wait_dist and
wait_moments against the generator's exact Markov chains (tools/figures/q0052.py): every
pattern of up to 8 letters on a fair coin, patterns on biased coins and on a die, every
race of two patterns of up to 4 letters and races of three and four, the distribution and
the first two moments; a seeded simulation; the page's numbers; the explorer's
JavaScript; and the page copies of the generated blocks."""

import json
import random
import sys
from fractions import Fraction as Fr
from itertools import combinations, product

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0052  # noqa: E402

ns = load_python(52)
corr, expected_tosses, race = ns["corr"], ns["expected_tosses"], ns["race"]
generating, wait_dist, wait_moments, FAIR = ns["generating"], ns["wait_dist"], ns["wait_moments"], ns["FAIR"]
DIE = {str(i): Fr(1, 6) for i in range(1, 7)}


def coin(q):
    return {"H": Fr(q), "T": 1 - Fr(q)}


def words(L, letters="HT"):
    return ["".join(t) for t in product(letters, repeat=L)]


def free(pats):
    """Distinct patterns, none inside another (the condition of the race)."""
    return len(set(pats)) == len(pats) and all(not (a in b) for a in pats for b in pats if a != b)


def test_page_numbers():
    assert (expected_tosses("HH"), expected_tosses("HT"), expected_tosses("HHH")) == (6, 4, 14)
    assert (corr("HH", "HH"), corr("HH", "HT"), corr("HT", "HT"), corr("HT", "HH")) == (6, 2, 4, 0)
    assert race(["HT", "HH"]) == ([Fr(1, 2), Fr(1, 2)], 3)
    assert race(["THH", "HHH"])[0] == [Fr(7, 8), Fr(1, 8)]
    assert race(["HHH", "HTH", "THH"]) == ([Fr(1, 8), Fr(5, 12), Fr(11, 24)], Fr(16, 3))
    # a biased coin: HH is 1/q + 1/q^2, HT is 1/(q(1 - q)); the table's rows
    for q in q0052.BIASED:
        assert expected_tosses("HH", coin(q)) == 1 / q + 1 / q ** 2
        assert expected_tosses("HT", coin(q)) == 1 / (q * (1 - q))
    assert expected_tosses("HH", coin(Fr(2, 3))) == Fr(15, 4) and expected_tosses("TT", coin(Fr(2, 3))) == 12
    # the moments: 4 and 22 for the variances of HT and HH; the table's rows
    assert wait_moments("HT") == (4, 4) and wait_moments("HH") == (6, 22)
    assert [wait_moments(p)[1] for p in q0052.MOMENT_PATTERNS] == [4, 22, 58, 142, 734]
    # HH: C(z) = 1 + z/2, D(z) = 1 - z/2 - z^2/4
    num, d = generating("HH")
    assert num == [0, 0, Fr(1, 4)] and d == [1, Fr(-1, 2), Fr(-1, 4), 0]
    # the follow-ups: the die, 1011 and 1111, the race of 1011 and 0110, the extremes
    assert expected_tosses("66", DIE) == 42 and expected_tosses("12", DIE) == 36
    B = {"1": Fr(1, 2), "0": Fr(1, 2)}
    assert expected_tosses("1011", B) == 18 and expected_tosses("1111", B) == 30
    wins, length = race(["1011", "0110"], B)
    assert wins == [Fr(7, 12), Fr(5, 12)] and length == Fr(73, 6) and 18 + 18 - length == Fr(143, 6)
    for L in range(1, 9):
        es = [expected_tosses(w) for w in words(L)]
        assert max(es) == 2 ** (L + 1) - 2 and min(es) == 2 ** L


def test_expected_matches_the_chain():
    for L in range(1, 9):
        for w in words(L):
            assert expected_tosses(w) == q0052.expected(w), w
    for q in (Fr(1, 3), Fr(3, 4), Fr(1, 10)):
        for L in range(1, 6):
            for w in words(L):
                assert expected_tosses(w, coin(q)) == q0052.expected(w, coin(q)), (w, q)
    rng = random.Random(52)
    for _ in range(60):
        w = "".join(rng.choice("123456") for _ in range(rng.randint(1, 4)))
        assert expected_tosses(w, DIE) == q0052.expected(w, DIE), w


def test_race_matches_the_chain():
    for La in range(1, 5):
        for Lb in range(1, 5):
            for a in words(La):
                for b in words(Lb):
                    if free([a, b]):
                        assert race([a, b]) == q0052.race([a, b]), (a, b)
    for m in (3, 4):
        for pats in combinations(words(3), m):
            assert race(list(pats)) == q0052.race(list(pats)), pats
    for pats in (["HH", "HT", "TT"], ["HT", "TH", "HHH"]):
        for q in (Fr(1, 3), Fr(2, 3)):
            if free(pats):
                assert race(pats, coin(q)) == q0052.race(pats, coin(q)), (pats, q)


def test_generating_function():
    for L in range(1, 6):
        for w in words(L):
            assert wait_dist(w, FAIR, 30) == [Fr(0)] + q0052.dist(w, 29), w
            assert wait_moments(w) == q0052.moments(w), w
    for q in (Fr(1, 3), Fr(4, 5)):
        for w in ("HH", "HTH", "TTH"):
            assert wait_dist(w, coin(q), 25) == [Fr(0)] + q0052.dist(w, 24, coin(q))
            assert wait_moments(w, coin(q)) == q0052.moments(w, coin(q))
    for w in ("66", "121", "3"):
        assert wait_moments(w, DIE) == q0052.moments(w, DIE)
        num, d = generating(w, DIE)
        assert d[0] == 1 and sum(num) == sum(d)                 # G(1) = 1


def test_penney_table():
    for a in words(3):
        b, p = q0052.best_reply(a)
        assert p == race([b, a])[0][0] and p >= Fr(2, 3)
        assert b == ("T" if a[1] == "H" else "H") + a[:2]       # the recipe on the page


def test_simulation():
    rng = random.Random(52)
    for p, probs in (("HH", FAIR), ("HT", FAIR), ("HTH", FAIR), ("HH", coin(Fr(3, 4))), ("66", DIE)):
        letters, weights = zip(*probs.items())
        runs, total = 20000, 0
        for _ in range(runs):
            seen = ""
            while not seen.endswith(p):
                seen = (seen + rng.choices(letters, [float(w) for w in weights])[0])[-len(p):]
                total += 1
        e = float(expected_tosses(p, probs))
        assert abs(total / runs - e) < 0.05 * e, p


def test_explorer_matches_the_page_code():
    from page_tests import explorer_require, node_json

    cases = [(p, "coin", 0.5) for p in words(1) + words(2) + words(3) + ["HTHH", "HHHH"]]
    cases += [(p, "coin", q) for p in ("HH", "HT", "THT") for q in (0.3, 0.8)] + [(p, "die", 0) for p in ("66", "12", "616", "3")]
    pairs = [(a, b) for a in words(2) + words(3) for b in words(2) + words(3) if free([a, b])]
    got = node_json(f"""
      const m = {explorer_require()};
      const P = (kind, q) => m.coinProbs(kind, q);
      console.log(JSON.stringify([
        {json.dumps(cases)}.map(([p, kind, q]) => [m.coinExpected(p, P(kind, q)), m.coinTable(p, Object.keys(P(kind, q))), m.coinDist(p, 12, P(kind, q))]),
        {json.dumps(pairs)}.map(([a, b]) => m.coinRace([a, b], P("coin", 0.5))),
      ]));""")
    for (p, kind, q), (e, table, d) in zip(cases, got[0]):
        probs = DIE if kind == "die" else coin(Fr(q).limit_denominator(100))
        letters = sorted(probs) if kind == "die" else ["H", "T"]
        assert abs(e - float(expected_tosses(p, probs))) < 1e-9 * max(1, e), (p, kind, q)
        assert table == [[q0052.step(p, s, c) for c in letters] for s in range(len(p) + 1)], p
        assert all(abs(x - float(y)) < 1e-12 for x, y in zip(d, q0052.dist(p, 12, probs))), p
    for (a, b), (wins, length) in zip(pairs, got[1]):
        w, n = race([a, b])
        assert abs(wins[0] - float(w[0])) < 1e-12 and abs(length - float(n)) < 1e-9, (a, b)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(52)
