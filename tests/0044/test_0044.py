"""Question 0044 has no code on the page; these tests check its numbers against a direct
simulation of the routine: the closed forms for the gap and for the digits after n steps
in every base from 2 to 16 (every number, n up to 59, and n = 1000), the page's tables and
examples, the explorer's model, and that the figures are the generator's output."""

import sys
from fractions import Fraction as Fr

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0044  # noqa: E402


def digits(x, B):
    return (x // (B * B), x // B % B, x % B)


def step(x, B):
    a, b, c = sorted(digits(x, B), reverse=True)
    return (a * B * B + b * B + c) - (c * B * B + b * B + a)


def run(x, B, n):
    for _ in range(n):
        x = step(x, B)
    return x


def gap(x, B):
    d = digits(x, B)
    return max(d) - min(d)


def formula(d0, n, B):
    """The page's cases for (a_n, c_n): parts a and b, and the bonus for any base."""
    m = abs(2 * d0 - (B + 1))
    if n == 1:
        return d0 - 1, B - d0
    if B % 2 == 0:
        if n <= Fr(3 + m, 2):
            return Fr(B + 1 - 2 * n + m, 2), Fr(B - 3 + 2 * n - m, 2)
        return B // 2 - 1, B // 2
    if n <= Fr(m + 4, 2):
        return Fr(B + 1 - 2 * n + m, 2), Fr(B - 3 + 2 * n - m, 2)
    if (n - m // 2) % 2 == 0:
        return Fr(B - 3, 2), Fr(B + 1, 2)
    return Fr(B - 1, 2), Fr(B - 1, 2)


def test_digits_after_n_steps_every_base():
    for B in range(2, 17):
        for x in range(B ** 3):
            d0 = gap(x, B)
            if d0 == 0:
                assert step(x, B) == 0 and step(0, B) == 0
                continue
            y = x
            for n in range(1, 60):
                y = step(y, B)
                a, b, c = digits(y, B)
                assert b == B - 1
                assert (a, c) == formula(d0, n, B), (B, x, n)


def test_gap_recursion_and_closed_forms():
    for B in range(2, 17):
        for d0 in range(1, B):
            m, D = abs(2 * d0 - (B + 1)), d0
            for k in range(1, 40):
                D = max(D - 1, B - D)
                if B % 2 == 0:
                    assert D == max(Fr(B, 2), Fr(B + 1 - 2 * k + m, 2))
    # part a: D_1 = (9 + |2 d0 - 11|) / 2; part b: D_1 = 2 + |d0 - 3| and the case formula
    for d0 in range(1, 10):
        assert max(d0 - 1, 10 - d0) == Fr(9 + abs(2 * d0 - 11), 2) >= 5
    for d0 in range(1, 5):
        t, D = abs(d0 - 3), d0
        assert max(d0 - 1, 5 - d0) == 2 + t
        for k in range(1, 30):
            D = max(D - 1, 5 - D)
            assert D == (2 + t - (k - 1) if k <= t + 1 else 2 + (k - 1 - t) % 2)


def test_after_1000_steps():
    for x in range(1000):
        if gap(x, 10):
            assert run(x, 10, 1000) == 495
            assert next(n for n in range(1, 10) if run(x, 10, n) == 495) <= 6
    assert max(next(n for n in range(1, 10) if run(x, 10, n) == 495) for x in range(1000) if gap(x, 10)) == 6
    for x in range(125):
        d0 = gap(x, 5)
        if d0:
            assert run(x, 5, 1000) == (48 if d0 in (1, 3) else 72)
    for B in range(2, 17):
        h = (B - 1) // 2
        for x in range(B ** 3):
            d0 = gap(x, B)
            if not d0:
                continue
            m = abs(2 * d0 - (B + 1))
            if B % 2 == 0:
                target = (B * B - 1) * B // 2
                assert run(x, B, 1000) == target
                assert next(n for n in range(1, 40) if run(x, B, n) == target) <= B // 2 + 1
                assert digits(target, B) == (B // 2 - 1, B - 1, B // 2)
            else:
                want = (B * B - 1) * h if (1000 - m // 2) % 2 == 0 else (B * B - 1) * (h + 1)
                assert run(x, B, 1000) == want
                assert digits((B * B - 1) * h, B) == (h - 1, B - 1, h + 1)
                assert digits((B * B - 1) * (h + 1), B) == (h, B - 1, h)


def test_page_tables_and_examples():
    # the maps D -> D' of parts a and b
    assert [max(D - 1, 10 - D) for D in range(1, 10)] == [9, 8, 7, 6, 5, 5, 6, 7, 8]
    assert [max(D - 1, 5 - D) for D in range(1, 5)] == [4, 3, 2, 3]
    # 211
    seq, y = [], 211
    for _ in range(7):
        y = step(y, 10)
        seq.append(digits(y, 10))
    assert seq == [(0, 9, 9), (8, 9, 1), (7, 9, 2), (6, 9, 3), (5, 9, 4), (4, 9, 5), (4, 9, 5)]
    assert all(formula(1, n, 10) == (a, c) for n, (a, b, c) in enumerate(seq, 1))
    assert [10 - n for n in range(2, 7)] == [a for a, _, _ in seq[1:6]]
    # base 5: the cycle, the checks and the two examples
    to5 = lambda s: int(s, 5)
    assert (to5("143"), to5("242")) == (48, 72) and 24 * 2 == 48 and 24 * 3 == 72
    assert to5("431") - to5("134") == 116 - 44 == 72 and to5("442") - to5("244") == 122 - 74 == 48
    ex = lambda s, k: ["".join(map(str, digits(run(to5(s), 5, n), 5))) for n in range(1, k + 1)]
    assert ex("401", 5) == ["341", "242", "143", "242", "143"]
    assert ex("300", 3) == ["242", "143", "242"]
    assert run(to5("401"), 5, 1000) == 72 and run(to5("300"), 5, 1000) == 48
    # the consistency table: m in base 5 is 2t, the line parts agree
    for d0 in range(1, 5):
        t = abs(d0 - 3)
        assert abs(2 * d0 - 6) == 2 * t
        for n in range(2, t + 3):
            assert formula(d0, n, 5)[0] == 3 + t - n
    for d0 in range(1, 10):
        m = abs(2 * d0 - 11)
        assert m % 2 == 1 and Fr(3 + m, 2) <= 6


def test_explorer_matches_simulation():
    """The kapn box: its step, its direct run, its gap and its case formula against the
    simulation for every base from 2 to 16, every starting gap and n up to 40 and 1000."""
    import json

    from page_tests import explorer_require, node_json

    cases = []
    for B in range(2, 17):
        for d0 in range(1, B):
            x = d0                                   # the digits (0, 0, d0): gap d0
            cases.append((B, x, d0))
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([B, x, d0]) => {{
        const out = [];
        for (let n = 1; n <= 40; n++) out.push([m.kapnFormula(d0, n, B), m.kapnGap(d0, n - 1, B), m.kapnRun(x, B, n)]);
        return {{ out, far: m.kapnRun(x, B, 1000), farF: m.kapnFormula(d0, 1000, B), step: m.kapnStep(x, B) }};
      }})));""")
    for (B, x, d0), r in zip(cases, got):
        assert r["step"] == step(x, B)
        D = d0
        for n, (f, g, y) in enumerate(r["out"], 1):
            assert g == D
            D = max(D - 1, B - D)
            assert y == run(x, B, n)
            assert (f["a"], f["c"]) == formula(d0, n, B) and f["b"] == B - 1
            assert digits(y, B) == (f["a"], f["b"], f["c"])
        assert r["far"] == run(x, B, 1000)
        assert digits(r["far"], B) == (r["farF"]["a"], r["farF"]["b"], r["farF"]["c"])


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(44)


def test_generator_gaps():
    assert q0044.gaps(1, 10, 6) == [1, 9, 8, 7, 6, 5, 5]
    assert q0044.gaps(4, 5, 5) == [4, 3, 2, 3, 2, 3]


def test_explorer_state_diagram():
    """The state diagram box (kapgraph): the chain of every number in every base from 2 to
    12, and of sampled numbers up to base 20, against the simulation: the nodes until a
    value comes back, the cycle (the fixed point, 000, or two values in an odd base), and
    the stage of each node from the rows of the closed form."""
    import json
    import random

    from page_tests import explorer_require, node_json

    rng = random.Random(44)
    cases = [(B, x) for B in range(2, 13) for x in range(B ** 3)]
    cases += [(B, rng.randrange(B ** 3)) for B in range(13, 21) for _ in range(150)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([B, x]) => {{
        const c = m.kapgChain(x, B), d = m.kapnDigits(x, B), d0 = Math.max(...d) - Math.min(...d);
        return [c.nodes, c.cycleStart, c.cycleLen, c.nodes.map((_, i) => m.kapgStage(d0, i, B))];
      }})));""")
    for (B, x), (nodes, start, length, stages) in zip(cases, got):
        want, y = [x], step(x, B)
        while y not in want:
            want.append(y)
            y = step(y, B)
        assert nodes == want and start == want.index(y) and length == len(want) - start
        d0 = gap(x, B)
        cyc = set(want[start:])
        if d0 == 0:
            assert cyc == {0}
        elif B % 2 == 0:
            assert cyc == {(B * B - 1) * B // 2}
        else:
            h = (B - 1) // 2
            assert cyc == {(B * B - 1) * h, (B * B - 1) * (h + 1)}
        assert stages[0] == "start"
        for n in range(1, len(want)):
            if d0 == 0:
                assert stages[n] == "zero"
            elif n == 1:
                assert stages[n] == "first"
            else:
                assert stages[n] in ("line", "fixed", "cycle")
                if stages[n] in ("fixed", "cycle"):
                    assert n >= start
