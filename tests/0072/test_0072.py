"""Question 0072: the page's rotate_reversals, rotate_cycles and linearize against the
definition a[i] = old[(i + k) mod n] on every small n and k (k >= n and negative k too);
the number of swaps, of cycles (gcd) and of memory accesses against the generator; the
page's numbers (6 swaps, 4 cycles, 16 accesses); the explorer's JavaScript against the
generator; and the page copies of the blocks."""

import json
import random
import sys
from math import gcd

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0072  # noqa: E402

ns = load_python(72)
rotate_reversals, rotate_cycles, linearize, Ram = ns["rotate_reversals"], ns["rotate_cycles"], ns["linearize"], ns["Ram"]


def test_both_rotations_match_the_definition():
    for n in range(0, 14):
        for k in range(-n - 2, 2 * n + 3):
            a = list(range(100, 100 + n))
            want = q0072.rotated(a, k) if n else []
            for f in (rotate_reversals, rotate_cycles):
                b = list(a)
                assert f(b, k) is None and b == want, (f.__name__, n, k)
    rng = random.Random(72)
    for _ in range(300):
        a = [rng.randint(-9, 9) for _ in range(rng.randint(1, 60))]
        k = rng.randint(0, 200)
        for f in (rotate_reversals, rotate_cycles):
            b = list(a)
            f(b, k)
            assert b == q0072.rotated(a, k)


def test_counts_and_cycles():
    assert q0072.swaps(7, 3) == 6 == 1 + 2 + 3
    for n in range(1, 40):
        for k in range(n):
            cs = q0072.cycles(n, k)
            g = gcd(n, k) if k else n
            assert len(cs) == g and all(len(c) == n // g for c in cs)
            assert sorted(c[0] for c in cs) == list(range(g))                    # the starts 0..g-1
            assert all(len({i % g for i in c}) == 1 for c in cs)                 # one residue mod g each
    assert len(q0072.cycles(12, 8)) == 4 and q0072.cycles(12, 8)[0] == [0, 8, 4]


def test_linearize_and_its_accesses():
    for n in range(1, 30):
        for h in range(n):
            fifo = [f"e{(i - h) % n}" for i in range(n)]       # the oldest, e0, sits at h
            ram = Ram(fifo)
            linearize(ram, h)
            assert ram.mem == [f"e{i}" for i in range(n)]
            assert ram.cycles == q0072.accesses_cycles(n, h) == (2 * n if h else 0)
            assert q0072.accesses_reversals(n, h) == 4 * q0072.swaps(n, h)
    assert q0072.accesses_cycles(8, 3) == 16 and q0072.accesses_reversals(8, 3) == 28


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    cases = [(n, k) for n in range(1, 17) for k in range(n)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([n, k]) => {{
        const a = Array.from({{ length: n }}, (_, i) => i);
        const rev = m.rkReversalSteps(n, k), cyc = m.rkCycleSteps(n, k);
        return {{ rev: rev[rev.length - 1].arr, cyc: cyc[cyc.length - 1].arr, swaps: rev.length - 1, moves: cyc.length - 1, cycles: m.rkCycles(n, k).length }};
      }})));""")
    for (n, k), g in zip(cases, got):
        want = q0072.rotated(list(range(n)), k)
        assert g["rev"] == want and g["cyc"] == want, (n, k)
        assert g["swaps"] == q0072.swaps(n, k) and g["cycles"] == len(q0072.cycles(n, k))
        assert g["moves"] == (0 if k == 0 else n + gcd(n, k))                  # n - g pulls, g saves, g closes


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(72)
