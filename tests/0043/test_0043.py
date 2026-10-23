"""Question 0043: every number the page states (9 races for 36 / 6 / 4, 7 for 30 / 6 / 3, 7
and 6 for the classic 25 / 5 / 3 and 25 / 5 / 1, the staircase counts), the page's plan
against the generator's race by race, the ranking against the hidden speeds on many
seeds, race 8 of part a as the six staircase candidates, the plan against every ordering
of the staircase candidates of both parts (768 and 16 linear extensions, always 9 and 7),
the explorer's JavaScript (the same seeds give the same races), and the page copies of
the generated blocks."""

import itertools
import json
import random
import sys
from math import ceil

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0043  # noqa: E402

ns = load_python(43)
horses_plan = ns["horses_plan"]


def oracle(speed):
    return lambda g: sorted(g, key=lambda x: speed[x])


def truth(speed, c):
    return sorted(range(len(speed)), key=lambda x: speed[x])[:c]


def test_page_numbers():
    for a, b, c, seed, want in ((36, 6, 4, q0043.SEED_A, 9), (30, 6, 3, q0043.SEED_B, 7), (25, 5, 3, 1, 7), (25, 5, 1, 1, 6), (9, 3, 2, 1, 5)):
        speed = q0043.speeds(a, seed)
        ranking, log = horses_plan(a, b, c, oracle(speed))
        assert len(log) == want and ranking == truth(speed, c), (a, b, c)
    assert [c * (c + 1) // 2 - 1 for c in (1, 2, 3, 4, 5)] == [0, 2, 5, 9, 14]
    # the example of part a: the eighth race holds A2, B1, A3, B2, C1, D1 in the winners' order
    speed = q0043.speeds(36, q0043.SEED_A)
    ranking, log = horses_plan(36, 6, 4, oracle(speed))
    w = log[6]
    group = lambda x: log[x // 6]            # noqa: E731  the group race of x, in finishing order
    assert sorted(log[7]) == sorted([group(w[0])[1], w[1], group(w[0])[2], group(w[1])[1], w[2], w[3]])
    assert len(log[8]) <= 4
    assert q0043.race_count(36, 6, 4) == 9 and q0043.race_count(30, 6, 3) == 7 and q0043.race_count(25, 5, 3) == 7


def test_plan_matches_the_generator_and_the_truth():
    rng = random.Random(43)
    cases = [(36, 6, 4), (30, 6, 3), (25, 5, 3), (25, 5, 1), (16, 4, 3), (9, 3, 2), (64, 8, 4), (49, 7, 5), (6, 6, 2), (7, 3, 1), (13, 4, 2)]
    for a, b, c in cases:
        for _ in range(6):
            speed = list(range(a))
            rng.shuffle(speed)
            ranking, log = horses_plan(a, b, c, oracle(speed))
            r2, log2 = q0043.plan(a, b, c, speed)
            assert ranking == r2 == truth(speed, c), (a, b, c)
            assert [e["order"] for e in log2] == log
            groups = ceil(a / b)
            assert [len(r) for r in log[:groups]] == [min(b, a - k * b) for k in range(groups)]
            if groups > 1:
                assert len(log[groups]) == groups
            assert all(1 <= len(r) <= b for r in log)
            assert all(speed[r[i]] < speed[r[i + 1]] for r in log for i in range(len(r) - 1))


def staircase_speeds(a, b, c, ext):
    """Hidden speeds that realise one linear extension of the staircase: horse x is in group
    x // b at position x % b; the winner of group 0 is fastest, the candidates follow the
    extension, every other horse is slower (group winners first, in the winners' order)."""
    speed = {(0, 0): 0}
    for k, p in enumerate(ext):
        speed[p] = k + 1
    nxt = len(ext) + 1
    groups = ceil(a / b)
    for j in range(groups):
        if (0, j) not in speed:
            speed[(0, j)] = nxt
            nxt += 1
    for j in range(groups):
        for i in range(b):
            if (i, j) not in speed and j * b + i < a:
                speed[(i, j)] = nxt
                nxt += 1
    return [speed[(x % b, x // b)] for x in range(a)]


def test_every_staircase_ordering():
    for a, b, c, want, count in ((36, 6, 4, 9, 768), (30, 6, 3, 7, 16)):
        cands = [(i, j) for j in range(c) for i in range(c - j) if i + j > 0]
        exts = [p for p in itertools.permutations(cands)
                if all(p.index((i, j)) < p.index((i2, j2)) for (i, j) in p for (i2, j2) in p if i <= i2 and j <= j2 and (i, j) != (i2, j2))]
        assert len(exts) == count
        worst = 0
        for ext in exts:
            speed = staircase_speeds(a, b, c, ext)
            ranking, log = horses_plan(a, b, c, oracle(speed))
            assert ranking == truth(speed, c)
            worst = max(worst, len(log))
        assert worst == want


def test_tables():
    rows = q0043.staircase_table().splitlines()[2:]
    assert len(rows) == 6 and rows[0].startswith("| ‏1 | ‏0 (מקום 1) | ‏**1** ✓ | ‏**2** ✓ | ‏**3** ✓ | ‏4 ✗ |")
    assert sum(cell.count("✓") for r in rows for cell in r.split("|")) == 9
    log_a = q0043.log_table(36, 6, 4, q0043.SEED_A).splitlines()[2:]
    assert len(log_a) == 9 and log_a[6].endswith("| ‏9 |") and log_a[8].endswith("| ‏0 |")
    log_b = q0043.log_table(30, 6, 3, q0043.SEED_B).splitlines()[2:]
    assert len(log_b) == 7 and log_b[5].endswith("| ‏5 |") and log_b[6].endswith("| ‏0 |")
    ex = q0043.examples_table().splitlines()[2:]
    assert len(ex) == len(q0043.EXAMPLES) and ex[0].endswith("| ‏**7** |") and ex[2].endswith("| ‏**9** |") and ex[3].endswith("| ‏**7** |")
    assert q0043.mulberry32(7)() == q0043.mulberry32(7)()


def test_explorer_matches_the_page_code():
    from page_tests import explorer_require, node_json

    cases = [[36, 6, 4, q0043.SEED_A], [30, 6, 3, q0043.SEED_B], [25, 5, 3, 5], [16, 4, 3, 8], [49, 7, 5, 2], [9, 3, 2, 4]]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([a, b, c, seed]) => {{
        const speed = m.horsesSpeeds(a, m.mulberry32(seed)), r = m.horsesPlan(a, b, c, speed);
        return [speed, r.ranking, r.log.map((e) => e.order), r.log.map((e) => [e.gone.slice().sort((u, v) => u - v), e.placed.slice().sort((u, v) => u - v), e.open.length])];
      }})));""")
    for (a, b, c, seed), (speed, ranking, orders, details) in zip(cases, got):
        assert speed == q0043.speeds(a, seed)
        r2, log2 = q0043.plan(a, b, c, speed)
        assert ranking == r2 and orders == [e["order"] for e in log2]
        assert details == [[sorted(e["gone"]), sorted(e["placed"]), len(e["open"])] for e in log2]


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(43)
