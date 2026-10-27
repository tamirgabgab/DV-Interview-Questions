"""Question 0054: the page's fixed_priority, rr_pick / rr_run, check_trace and wrr_run
against the generator's plain-loop arbiters (tools/figures/q0054.py) on random traffic
that keeps a waiting request; the fairness bounds (N - 1, and the sum of the other weights)
reached and never passed; every bug of the generator caught by its own rule; the page's
numbers; the explorer's JavaScript; and the page copies of the generated blocks. The
SystemVerilog modules and the checker run in Verilator (tests/0054/tb.sv)."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0054  # noqa: E402

ns = load_python(54)
fixed_priority, rr_pick, rr_run, check_trace, wrr_run = (ns[k] for k in ("fixed_priority", "rr_pick", "rr_run", "check_trace", "wrr_run"))


def traffic(rng, n, T, p=0.6, arb=None):
    """Random requests that keep a waiting request (the environment rule): the grants come
    from arb, run one cycle at a time."""
    reqs, grants, cur = [], [], 0
    state = arb()
    for _ in range(T):
        nxt = 0
        for i in range(n):
            waiting = cur >> i & 1 and not (grants and grants[-1] >> i & 1)
            if waiting or rng.random() < p:
                nxt |= 1 << i
        cur = nxt
        reqs.append(cur)
        grants.append(state(cur))
    return reqs, grants


def stepper(run, *args):
    """Turn a whole-trace arbiter into a cycle-by-cycle one (it is rerun on the prefix)."""
    def make():
        seen = []

        def step(req):
            seen.append(req)
            return run(seen, *args)[-1]
        return step
    return make


def test_page_numbers():
    assert fixed_priority(0b1011) == 0b0001 and fixed_priority(0) == 0 and fixed_priority(0b1000) == 0b1000
    assert rr_pick(0b1011, 0b0100, 4) == 0b1000 and rr_pick(0, 0b0100, 4) == 0
    full = [0b1111] * 8
    assert rr_run(full, 4) == [1, 2, 4, 8, 1, 2, 4, 8] and q0054.fixed(full) == [1] * 8
    assert max(q0054.max_wait(full, rr_run(full, 4), i) for i in range(4)) == 3
    grants = wrr_run([0b1111] * 400, [1, 2, 3, 4])
    assert [sum(1 for g in grants if g >> i & 1) for i in range(4)] == [40, 80, 120, 160]
    assert [q0054.max_wait([0b1111] * 400, grants, i) for i in range(4)] == [9, 8, 7, 6]
    # the self-checks: N - 1 = 3 and 7, 2 + 3 + 4 = 9
    assert max(q0054.max_wait([255] * 64, rr_run([255] * 64, 8), i) for i in range(8)) == 7


def test_pick_matches_the_loop():
    for n in range(1, 7):
        for req in range(1 << n):
            for p in range(n):
                want = next(((p + k) % n for k in range(n) if req >> ((p + k) % n) & 1), None)
                assert rr_pick(req, 1 << p, n) == (0 if want is None else 1 << want), (n, req, p)
        for req in range(1 << n):
            assert fixed_priority(req) == q0054.fixed([req], n)[0]


def test_round_robin_and_its_bound():
    rng = random.Random(54)
    for n in (2, 3, 4, 5, 8):
        for _ in range(20):
            reqs = [rng.randrange(1 << n) for _ in range(60)]
            assert rr_run(reqs, n) == q0054.rr(reqs, n)
        reqs, grants = traffic(rng, n, 300, 0.7, stepper(rr_run, n))
        assert grants == q0054.rr(reqs, n)
        v = check_trace(reqs, grants, n, n - 1)
        assert v == q0054.violations(reqs, grants, n, n - 1) == {"onehot": 0, "spurious": 0, "hold": 0, "fair": 0}
        assert check_trace(reqs, grants, n, n - 2)["fair"] > 0 if n > 1 else True   # N - 2 is too tight


def test_bugs_are_caught():
    rng = random.Random(55)
    n = 4
    for bug, rule in (("stuck", "fair"), ("winner", "fair"), ("double", "onehot")):
        reqs, grants = traffic(rng, n, 400, 0.7, stepper(q0054.rr, n, bug))
        v = check_trace(reqs, grants, n, n - 1)
        assert v == q0054.violations(reqs, grants, n, n - 1)
        assert v[rule] > 0, (bug, v)
        assert v["spurious"] == 0 and v["hold"] == 0


def test_weighted():
    rng = random.Random(56)
    for _ in range(30):
        n = rng.randint(2, 5)
        w = [rng.randint(1, 4) for _ in range(n)]
        reqs = [rng.randrange(1 << n) for _ in range(80)]
        assert wrr_run(reqs, w) == q0054.wrr(reqs, w), w
        reqs, grants = traffic(rng, n, 300, 0.75, stepper(wrr_run, w))
        bound = sum(w) - min(w)
        assert check_trace(reqs, grants, n, bound)["fair"] == 0, w
        full = wrr_run([(1 << n) - 1] * (sum(w) * 20), w)
        for i in range(n):
            assert sum(1 for g in full if g >> i & 1) == 20 * w[i]
            assert q0054.max_wait([(1 << n) - 1] * len(full), full, i) == sum(w) - w[i]
    assert wrr_run([0b1111] * 12, [1, 1, 1, 1]) == rr_run([0b1111] * 12, 4)


def test_explorer_matches_the_page_code():
    from page_tests import explorer_require, node_json

    rng = random.Random(57)
    cases = [[rng.randrange(16) for _ in range(16)] for _ in range(30)] + [[15] * 16, [9] * 16]
    w = [1, 2, 3, 4]
    got = node_json(f"""
      const m = {explorer_require()};
      const C = {json.dumps(cases)};
      console.log(JSON.stringify(C.map((r) => [m.arbFixed(r, 4), m.arbRR(r, 4), m.arbWRR(r, {json.dumps(w)}),
        ["stuck", "winner", "double"].map((b) => m.arbRR(r, 4, b)), m.arbCheck(r, m.arbRR(r, 4, "double"), 4, 3)])));""")
    for reqs, (fx, rr, wr, bugs, chk) in zip(cases, got):
        assert fx == q0054.fixed(reqs) and rr == rr_run(reqs, 4) == q0054.rr(reqs) and wr == wrr_run(reqs, w)
        assert bugs == [q0054.rr(reqs, 4, b) for b in ("stuck", "winner", "double")]
        assert chk == check_trace(reqs, q0054.rr(reqs, 4, "double"), 4, 3)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(54)
