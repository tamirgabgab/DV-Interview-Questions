"""Question 0015 has no code on the page; these tests check its numbers by exhaustive
enumeration and that the figures and the value table are the generator's output."""

import re
import subprocess
import sys
from fractions import Fraction
from itertools import product

from extract_code import ROOT, question_path

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0015  # noqa: E402

HALF = Fraction(1, 2)


def enumerate_kinds(C, p, q):
    """P(all boys | at least one boy with the trait) by summing over every assignment of
    (boy?, trait?) to the C children."""
    child = {(True, True): p * q, (True, False): p * (1 - q),
             (False, True): (1 - p) * q, (False, False): (1 - p) * (1 - q)}
    cond = hit = Fraction(0)
    for kids in product(child, repeat=C):
        w = Fraction(1)
        for k in kids:
            w *= child[k]
        if any(boy and trait for boy, trait in kids):
            cond += w
            if all(boy for boy, _ in kids):
                hit += w
    return hit / cond


def test_part_a_counts():
    families = list(product("BG", repeat=2))
    cond = [f for f in families if "B" in f]
    assert len(cond) == 3 and sum(f == ("B", "B") for f in cond) == 1


def test_part_b_counts():
    # 14 kinds per child: (sex, weekday); Tuesday is day 2
    kinds = [(s, d) for s in "BG" for d in range(7)]
    tue_boy = lambda k: k == ("B", 2)
    pairs = list(product(kinds, repeat=2))
    cond = [x for x in pairs if tue_boy(x[0]) or tue_boy(x[1])]
    hit = [x for x in cond if x[0][0] == "B" and x[1][0] == "B"]
    both_boys = [x for x in pairs if x[0][0] == "B" and x[1][0] == "B"]
    assert (len(pairs), len(cond), len(hit), len(both_boys)) == (196, 27, 13, 49)
    assert Fraction(len(hit), len(cond)) == Fraction(13, 27)


def test_bayes_terms():
    p_a, p_t_a, p_t = Fraction(1, 4), 1 - Fraction(6, 7) ** 2, 1 - Fraction(13, 14) ** 2
    assert (p_t_a, p_t) == (Fraction(13, 49), Fraction(27, 196))
    assert p_t_a * p_a / p_t == Fraction(13, 27)


def test_general_formula():
    for C in range(1, 6):
        for p in (Fraction(1, 2), Fraction(1, 3), Fraction(3, 4)):
            for q in (Fraction(1), Fraction(1, 2), Fraction(1, 7), Fraction(2, 5)):
                assert q0015.answer(C, p, q) == enumerate_kinds(C, p, q), (C, p, q)
    assert q0015.answer(2, HALF, Fraction(1)) == Fraction(1, 3)
    assert q0015.answer(2, HALF, Fraction(1, 7)) == Fraction(13, 27)
    # q -> 0 gives p^(C-1)
    assert abs(float(q0015.answer(3, HALF, Fraction(1, 10 ** 9))) - 0.25) < 1e-6


def test_figures_up_to_date():
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0015.py")],
                         capture_output=True, text=True, check=True).stdout
    text = question_path(15).read_text(encoding="utf-8")
    pattern = r'<svg class="figure".*?</svg>|<span class="viz-legend">.*?</span></span>'
    assert re.findall(pattern, text) == re.findall(pattern, out)
    assert len(re.findall(pattern, out)) == 4
    page_rows = [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
    table_rows = [l for l in out.splitlines() if l.startswith("|")]
    assert page_rows == table_rows


def test_explorer_matches_formula():
    """probabilityAnswer of the explorer against the generator's formula and the enumeration."""
    from page_tests import explorer_require, node_json

    cases = [(C, p, q) for C in (1, 2, 3, 4, 6) for p in (Fraction(1, 2), Fraction(1, 4), Fraction(9, 10))
             for q in (Fraction(1), Fraction(1, 2), Fraction(1, 7), Fraction(1, 365))]
    got = node_json(f"const m = {explorer_require()}; const cases = {[[C, float(p), float(q)] for C, p, q in cases]};"
                    "console.log(JSON.stringify(cases.map(([C, p, q]) => m.probabilityAnswer(C, p, q))));")
    for (C, p, q), v in zip(cases, got):
        assert abs(v - float(q0015.answer(C, p, q))) < 1e-12, (C, p, q)
        if C <= 4:
            assert abs(v - float(enumerate_kinds(C, p, q))) < 1e-12, (C, p, q)
    assert abs(got[cases.index((2, Fraction(1, 2), Fraction(1, 7)))] - 13 / 27) < 1e-12


def test_explorer_tuesday_grid():
    """The grid box of part b (J300): for each kind of information and each weekday, the
    first child's rows, the second child's columns, the cells counted twice, the families
    that meet it and those with two boys, against enumerating the 196 families; the page's
    27 and 13 for a boy born on Tuesday, a third for part a and a half for the elder."""
    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      const out = {{}};
      for (const info of m.TU_INFOS) for (let day = 0; day < 7; day++) out[info + day] = m.tuesdayCount(info, day);
      console.log(JSON.stringify(out));""")
    kinds = [(s, d) for s in "BG" for d in range(7)]
    for info in ("any", "day", "elder"):
        for day in range(7):
            S = {k for k in kinds if k[0] == "B" and (info != "day" or k[1] == day)}
            meets = lambda a, b: a in S or (info != "elder" and b in S)
            pairs = list(product(kinds, repeat=2))
            cond = [x for x in pairs if meets(*x)]
            hit = [x for x in cond if x[0][0] == x[1][0] == "B"]
            r = got[info + str(day)]
            assert r["row"] == sum(a in S for a, _ in pairs)
            assert r["col"] == (0 if info == "elder" else sum(b in S for _, b in pairs))
            assert r["overlap"] == (0 if info == "elder" else sum(a in S and b in S for a, b in pairs))
            assert r["cond"] == len(cond) == r["row"] + r["col"] - r["overlap"]
            assert r["hit"] == len(hit) and r["quad"] == 49
            assert Fraction(r["num"], r["den"]) == Fraction(len(hit), len(cond))
            assert (r["num"], r["den"]) == {"any": (1, 3), "day": (13, 27), "elder": (1, 2)}[info]
    assert (got["day2"]["row"], got["day2"]["col"], got["day2"]["overlap"], got["day2"]["cond"], got["day2"]["hit"]) == (14, 14, 1, 27, 13)
