"""Question 0043: every number the page states (9 races for 36 / 6 / 4, 7 for 30 / 6 / 3, 7
and 6 for the classic 25 / 5 / 3 and 25 / 5 / 1, the staircase counts), the page's plan
against the generator's race by race, the ranking against the hidden speeds on many
seeds, race 8 of part a as the six staircase candidates, the plan against every ordering
of the staircase candidates of both parts (768 and 16 linear extensions, always 9 and 7),
the exact worst case of the examples table by an adversary search over the page code,
race 8 and race 9 of part a, the explorer's JavaScript (the same seeds give the same races), and the page copies of
the generated blocks."""

import itertools
import json
import random
import sys
from fractions import Fraction
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
    assert len(log[8]) <= 2
    # the letter mapping of the example: the winners' race orders the groups C, F, B, E, D, A,
    # so the explanation's A, B, C, D are C, F, B, E here; race 8 is C2, F1, C3, F2, B1, E1,
    # F1 and F2 finish first, and F3 (the explanation's B3) survives into race 9
    nm = q0043.names(36, 6, q0043.plan(36, 6, 4, speed)[1])
    assert "".join(nm[x][0] for x in w) == "CFBEDA"
    assert sorted(nm[x] for x in log[7]) == sorted(["C2", "F1", "C3", "F2", "B1", "E1"])
    assert [nm[x] for x in log[7][:2]] == ["F1", "F2"] and sorted(nm[x] for x in log[8]) == ["B1", "F3"]
    # the box of part a starts on seed 2, where race 9 is skipped
    assert len(horses_plan(36, 6, 4, oracle(q0043.speeds(36, 2)))[1]) == 8
    # the box task of part b: 64 / 8 / 4 on seed 42 needs 11 races
    assert len(horses_plan(64, 8, 4, oracle(q0043.speeds(64, 42)))[1]) == 11


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


def adversary(a, b, c):
    """The page's horses_plan against every result of every race after the winners: horse
    j * b + i is the i-th of the group whose winner came j-th (after the groups and the
    winners every input looks like this up to the names), and every race the plan asks for
    is answered with each finishing order that agrees with the results so far, depth first.
    Returns the race count of every branch, with the results of its candidate races."""
    g = a // b
    fixed = [list(range(j * b, j * b + b)) for j in range(g)] + ([[j * b for j in range(g)]] if g > 1 else [])

    class Ask(Exception):
        pass

    def faster_sets(orders):
        faster = [set() for _ in range(a)]
        for order in orders:
            for i, x in enumerate(order):
                for y in order[i + 1:]:
                    up = faster[x] | {x}
                    for v in range(a):
                        if v == y or y in faster[v]:
                            faster[v] |= up
        return faster

    leaves = []

    def search(prefix):
        asked = []

        def race(group):
            asked.append(sorted(group))
            k = len(asked) - 1
            if k < len(fixed):
                return fixed[k]
            if k - len(fixed) < len(prefix):
                return prefix[k - len(fixed)]
            raise Ask

        try:
            ranking, log = horses_plan(a, b, c, race)
        except Ask:
            faster = faster_sets(fixed + prefix)

            def orders(rest):
                if not rest:
                    yield []
                for x in rest:
                    if not any(y in faster[x] for y in rest if y != x):
                        for tail in orders([y for y in rest if y != x]):
                            yield [x] + tail
            for order in orders(asked[-1]):
                search(prefix + [order])
            return
        assert log[:len(fixed)] == fixed and log[len(fixed):] == prefix and ranking[0] == 0
        leaves.append((len(log), prefix))

    search([])
    return leaves


def test_exact_worst_case():
    """The examples table gives the exact worst case. Every input is one branch of the
    adversary search (the results of the candidate races decide everything after the
    winners), and every branch is an input, so the deepest branch is the worst case; the
    generator's worst_case() runs the same search on its own model and also counts the
    greedy picks a horse's number decided (none), so the names do not matter."""
    for a, b, c in q0043.EXAMPLES:
        leaves = adversary(a, b, c)
        races, branches, ties, deepest = q0043.worst_case(a, b, c)
        assert max(n for n, _ in leaves) == races and len(leaves) == branches and ties == 0, (a, b, c)
        fits = c * (c + 1) // 2 - 1 <= b
        g = ceil(a / b)
        assert races == (g + 1 if c == 1 else g + 2 if fits else g + 3), (a, b, c)
    rows = q0043.examples_table().splitlines()[2:]
    assert rows[q0043.EXAMPLES.index((64, 8, 4))].endswith("| לא | ‏**11** |")
    # 64 / 8 / 4: race 10 leaves A4 out, and 11 races exactly when A2 and A3 finish it first,
    # that is, when ranks 1, 2 and 3 are all in one group: 7/63 * 6/62 = 1/93 of the orders
    for n, prefix in adversary(64, 8, 4):
        assert sorted(prefix[0]) == [1, 2, 8, 9, 10, 16, 17, 24] and 3 not in prefix[0]
        assert (n == 11) == (prefix[0][:2] == [1, 2]) and (n == 10 or len(prefix[1]) == 2)
    assert Fraction(7, 63) * Fraction(6, 62) == Fraction(1, 93)
    # a found 11 is a real input: speeds that follow the deepest branch
    _, _, _, deepest = q0043.worst_case(64, 8, 4)
    results = [list(range(j * 8, j * 8 + 8)) for j in range(8)] + [list(range(0, 64, 8))] + deepest
    above = {x: {u for r in results for i, u in enumerate(r) if x in r[i + 1:]} for x in range(64)}
    order = []
    while len(order) < 64:                         # a total order that agrees with every result
        order.append(min(x for x in range(64) if x not in order and above[x] <= set(order)))
    speed = [order.index(x) for x in range(64)]
    ranking, log = horses_plan(64, 8, 4, oracle(speed))
    assert log[9:] == deepest and len(log) == 11 and ranking == truth(speed, 4)


def test_race_8_and_race_9():
    """Part a: race 8 is always A2, B1, A3, B2, C1, D1, and D1 gets its place by the third
    tie-break (most horses known slower), the other three keys tied; at most one of A4, B3,
    C2 survives it, so race 9 has two horses; race 9 is skipped exactly when the first two
    of race 8 are A2 and B1 (either way round), which is 30/119 of the random orders."""
    a, b, c = 36, 6, 4
    hid = lambda name: "ABCDEF".index(name[0]) * b + int(name[1:]) - 1   # noqa: E731
    leaves = adversary(a, b, c)
    for n, prefix in leaves:
        assert sorted(prefix[0]) == sorted(hid(h) for h in ["A2", "B1", "A3", "B2", "C1", "D1"])
        top = {tuple(prefix[0][:2])}
        survives = {("A2", "A3"): "A4", ("B1", "B2"): "B3", ("B1", "C1"): "C2"}
        alive = [h for pair, h in survives.items() if tuple(map(hid, pair)) in top]
        if alive:
            assert n == 9 and sorted(prefix[1]) == sorted([prefix[0][2], hid(alive[0])])
        else:
            assert n == 8 and {prefix[0][0], prefix[0][1]} == {hid("A2"), hid("B1")}
    # the greedy's last pick of race 8, after B1, A2, C1, B2, A3
    faster = {"A4": 3, "B3": 3, "C2": 3, "D1": 3}
    slower = {"A4": 2, "B3": 3, "C2": 4, "D1": 5 + 6 + 6}
    assert set(faster.values()) == {3} and max(slower, key=slower.get) == "D1" and slower["D1"] == 17
    speed = q0043.speeds(a, q0043.SEED_A)
    assert q0043.plan(a, b, c, speed)[1][7]["ties"] == 0      # the numbers of the horses never decide
    # the probability that race 9 is skipped: rank 2 in the group of rank 1 and rank 3 in
    # another, or the other way round, over every place of ranks 1 to 3 among the 36 slots
    skip = total = 0
    for p1, p2, p3 in itertools.permutations(range(a), 3):
        g1, g2, g3 = p1 // b, p2 // b, p3 // b
        total += 1
        skip += (g2 == g1) != (g3 == g1)            # exactly one of ranks 2 and 3 in the group of rank 1
    assert Fraction(skip, total) == Fraction(30, 119) == Fraction(5, 35) * Fraction(30, 34) + Fraction(30, 35) * Fraction(5, 34)


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


def test_explorer_chains():
    """The proof panel of the box: after every race, for every horse, the chains are made of
    direct results of the races so far (the faster horse ahead of the slower in that race),
    they reach exactly the horses known faster (the transitive closure), and each is as
    short as a plain BFS over the direct results says."""
    from page_tests import explorer_require, node_json

    cases = [[36, 6, 4, q0043.SEED_A], [30, 6, 3, q0043.SEED_B], [16, 4, 3, 8]]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([a, b, c, seed]) => {{
        const r = m.horsesPlan(a, b, c, m.horsesSpeeds(a, m.mulberry32(seed)));
        return [r.log.map((e) => e.order), r.log.map((_, k) => [...Array(a).keys()].map((x) => m.horsesChain(r.log, k + 1, x)))];
      }})));""")
    for (a, b, c, seed), (orders, per_step) in zip(cases, got):
        for k, chains in enumerate(per_step, 1):
            beat = {(u, v, r) for r, order in enumerate(orders[:k]) for i, u in enumerate(order) for v in order[i + 1:]}
            above = {}
            for u, v, _ in beat:
                above.setdefault(v, set()).add(u)
            for x, ch in enumerate(chains):
                dist, queue = {x: 0}, [x]          # a plain BFS up the direct results
                for h in queue:
                    for u in sorted(above.get(h, ())):
                        if u not in dist:
                            dist[u] = dist[h] + 1
                            queue.append(u)
                assert sorted(c["y"] for c in ch["chains"]) == sorted(dist.keys() - {x}), (seed, k, x)
                used = set()
                for chain in ch["chains"]:
                    links = chain["links"]
                    assert links[0][0] == chain["y"] and links[-1][1] == x
                    assert all(l1[1] == l2[0] for l1, l2 in zip(links, links[1:]))
                    assert all(tuple(link) in beat for link in links)
                    assert len(links) == dist[chain["y"]]
                    used |= {link[2] for link in links}
                assert ch["races"] == sorted(used)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(43)
