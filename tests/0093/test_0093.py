"""Question 0093, stable matching: the reference of tools/figures/q0093.py against a brute force
over all matchings (stable, best for every proposer, worst for every receiver), the proposal
bound and the instances that reach it, every number the page states, the generated blocks,
and the box's models under Node against the same reference."""

import itertools
import json
import math
import random
import sys

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0093  # noqa: E402


def random_instance(rnd, n):
    return [rnd.sample(range(n), n) for _ in range(n)], [rnd.sample(range(n), n) for _ in range(n)]


def instances():
    rnd = random.Random(93)
    out = [(q0093.CAND, q0093.JOBS)] + [q0093.restrict(n) for n in (3, 4, 5)]
    for n in range(1, 7):
        out += [random_instance(rnd, n) for _ in range(40 if n < 6 else 25)]
    return out


def test_algorithm_against_brute_force():
    """Stable, perfect, best for every proposer among all stable matchings, worst for every
    receiver; the rounds give the same matching with the same proposals."""
    for P, Q in instances():
        n = len(P)
        match, steps = q0093.gs_steps(P, Q)
        assert sorted(match) == list(range(n))
        assert not q0093.blocking(P, Q, match)
        assert len(steps) <= n * n - n + 1
        S = q0093.all_stable(P, Q)
        assert match in S
        rp, rq = q0093.ranks(P), q0093.ranks(Q)
        for i in range(n):
            assert rp[i][match[i]] == min(rp[i][m[i]] for m in S)
        back = q0093.flip(match)
        for j in range(n):
            assert rq[j][back[j]] == max(rq[j][q0093.flip(m)[j]] for m in S)
        rounds = q0093.gs_rounds(P, Q)
        held = rounds[-1][2]
        assert q0093.flip([held[j] for j in range(n)]) == match
        assert sum(len(r[0]) for r in rounds) == len(steps)


def test_blocking_against_definition():
    rnd = random.Random(7)
    for _ in range(60):
        n = rnd.randint(2, 5)
        P, Q = random_instance(rnd, n)
        m = rnd.sample(range(n), n)
        partner = q0093.flip(m)
        want = [(i, j) for i in range(n) for j in range(n)
                if P[i].index(j) < P[i].index(m[i]) and Q[j].index(i) < Q[j].index(partner[j])]
        assert q0093.blocking(P, Q, m) == want


def test_bound_is_reached():
    for n in range(2, 10):
        P, Q = q0093.worst_case(n)
        assert all(sorted(r) == list(range(n)) for r in P + Q)
        assert q0093.gs(P, Q)[1] == n * n - n + 1
    # no instance of 3 goes beyond it (every instance of 3)
    perms = list(itertools.permutations(range(3)))
    worst = 0
    for P in itertools.product(perms, repeat=3):
        for Q in itertools.product(perms, repeat=3):
            worst = max(worst, q0093.gs([list(p) for p in P], [list(q) for q in Q])[1])
    assert worst == 7


def test_page_numbers():
    C, J = q0093.CAND, q0093.JOBS
    # part a: the greedy choice in turn and its three blocking pairs, all of F
    g = q0093.greedy_by_order(C)
    assert g == [5, 0, 1, 2, 3, 4]                                    # A6 B1 C2 D3 E4 F5
    assert q0093.blocking(C, J, g) == [(5, 1), (5, 2), (5, 5)]        # F-2, F-3, F-6
    assert q0093.immediate(C, J) == g                                  # the trap: commit at once
    match, steps = q0093.gs_steps(C, J)
    assert match == [4, 0, 1, 5, 3, 2] and len(steps) == 11           # A5 B1 C2 D6 E4 F3
    assert [k for _, _, k, _ in steps].count("no") == 3 and [k for _, _, k, _ in steps].count("swap") == 2
    rounds = q0093.gs_rounds(C, J)
    assert len(rounds) == 5 and [len(r[0]) for r in rounds] == [6, 2, 1, 1, 1]
    # B and C got their first job; A prefers 6 and 1, which hold D and B
    assert C[1][0] == match[1] and C[2][0] == match[2]
    assert C[0][:3] == [5, 0, 4] and J[5].index(3) < J[5].index(0) and J[0].index(1) < J[0].index(0)
    # jobs proposing
    jm, jp = q0093.gs(J, C)
    assert q0093.flip(jm) == [2, 1, 3, 4, 0, 5] and jp == 9            # A3 B2 C4 D5 E1 F6
    # part c: five stable matchings, the sums and the join of 2 and 3
    S = q0093.stable_sorted()
    assert len(S) == 5 and S[0] == match and S[-1] == q0093.flip(jm)
    assert [q0093.rank_sums(C, J, m) for m in S] == [(11, 23), (14, 16), (14, 18), (17, 11), (21, 9)]
    rp = q0093.ranks(C)
    join = [min(S[1][i], S[2][i], key=lambda j: rp[i][j]) for i in range(6)]
    assert join == S[0]
    assert sum(1 for _ in itertools.permutations(range(6))) == 720 and 720 * 36 == 25920
    assert math.factorial(12) == 479001600
    # the follow-ups: job 1 gains by putting A above B (C instead of B)
    lie = q0093.best_lie(C, J)
    assert lie[0] == (0, [4, 2, 0, 1, 5, 3], 1, 2)
    Q2 = [list(lie[0][1])] + J[1:]
    assert q0093.flip(q0093.gs(C, Q2)[0])[0] == 2 and J[0].index(2) == 1 and J[0].index(1) == 2
    # the proposers never gain by lying (Dubins-Freedman), on the example: every lie of every candidate
    for i in range(6):
        for lie_i in itertools.permutations(C[i]):
            C2 = [list(lie_i) if k == i else c for k, c in enumerate(C)]
            assert rp[i][q0093.gs(C2, J)[0][i]] >= rp[i][match[i]]


def test_roommates_example():
    """A: B > C > D, B: C > A > D, C: A > B > D, D last for all: no split into pairs is stable."""
    pref = {"A": "BCD", "B": "CAD", "C": "ABD", "D": "ABC"}
    splits = [[("A", "B"), ("C", "D")], [("A", "C"), ("B", "D")], [("A", "D"), ("B", "C")]]
    for split in splits:
        mate = {}
        for x, y in split:
            mate[x], mate[y] = y, x
        blocking = [(x, y) for x in pref for y in pref[x]
                    if y != mate[x] and pref[x].index(y) < pref[x].index(mate[x])
                    and pref[y].index(x) < pref[y].index(mate[y])]
        assert blocking, split


def test_average_proposals():
    rnd = random.Random(1)
    total = sum(q0093.gs(*random_instance(rnd, 6))[1] for _ in range(1000))
    assert 11.0 < total / 1000 < 12.3 < 6 * sum(1 / k for k in range(1, 7))


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(93)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    cases = instances()[:60] + [q0093.restrict(n) for n in (3, 4, 5, 6)]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(cases)}.map(([P, Q]) => [m.smGS(P, Q), m.smAll(P, Q), m.smBlocking(P, Q, P.map((_, i) => i))])));")
    for (P, Q), (g, alls, blk) in zip(cases, got):
        match, steps = q0093.gs_steps(P, Q)
        assert g["match"] == match
        assert [(s["p"], s["r"], s["kind"], s["freed"]) for s in g["steps"]] == steps
        assert alls == q0093.all_stable(P, Q)
        assert [tuple(b) for b in blk] == q0093.blocking(P, Q, list(range(len(P))))
    rest = node_json(f"const m = {explorer_require()};console.log(JSON.stringify([3, 4, 5, 6].map((n) => m.smRestrict(n))));")
    assert rest == [list(q0093.restrict(n)) for n in (3, 4, 5, 6)]
    codec = node_json(f"const m = {explorer_require()};const [C, J] = m.smRestrict(6);"
                      "console.log(JSON.stringify([m.smEncode(C, J), m.smDecode(m.smEncode(C, J), 6), m.smDecode('012_012', 3), m.smDecode('00-12-21_012-012-012', 3)]));")
    assert codec[0] == "504213-031245-102534-254130-230451-025314_421053-015342-052341-032451-324501-523041"
    assert codec[1] == [q0093.CAND, q0093.JOBS]
    assert codec[2] is None and codec[3] is None
