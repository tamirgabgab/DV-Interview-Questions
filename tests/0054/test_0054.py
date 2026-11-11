"""Question 0054: the page's fixed_priority, rr_pick / rr_run, check_trace and wrr_run
against the generator's plain-loop arbiters (tools/figures/q0054.py) on random traffic
that keeps a waiting request; the fairness bounds (N - 1, and the sum of the other weights)
reached and never passed; every bug of the generator caught by its own rule; the page's
numbers (the box's tasks, the trap of a pointer that turns every cycle, the matrix arbiter's
flops, the bits of used); the WRR clock-by-clock table against the page code; the explorer's
JavaScript; and the page copies of the generated blocks. The SystemVerilog modules and the
checker run in Verilator (tests/0054/tb.sv)."""

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
    # the extra examples: N - 1 = 3 and 7, 2 + 3 + 4 = 9
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


def rot(g, n):
    return (g << 1 | g >> (n - 1)) & ((1 << n) - 1)


def worst_wait(n, step, init, i):
    """The longest wait of requester i over every request sequence that keeps a waiting
    request (a search of the states: the arbiter's state, the requests that must stay, the
    wait so far)."""
    from collections import deque
    best, seen, todo = 0, set(), deque([(init, 0, 0)])
    while todo:
        state, held, w = todo.popleft()
        if (state, held, w) in seen:
            continue
        seen.add((state, held, w))
        assert w <= 4 * n
        for req in range(1 << n):
            if req & held != held:
                continue
            g, nxt = step(state, req)
            w2 = w + 1 if req >> i & 1 and not g >> i & 1 else 0
            best = max(best, w2)
            todo.append((nxt, req & ~g, w2))
    return best


def test_trap_pointer_every_cycle():
    # the pointer turned one place every cycle, whatever the grant: the bound N - 1 holds
    for n in (3, 4):
        every = lambda pri, req, n=n: (rr_pick(req, pri, n), rot(pri, n))   # noqa: E731
        idle = lambda pri, req, n=n: (lambda g: (g, rot(g, n) if g else rot(pri, n)))(rr_pick(req, pri, n))   # noqa: E731
        right = lambda pri, req, n=n: (lambda g: (g, rot(g, n) if g else pri))(rr_pick(req, pri, n))   # noqa: E731
        for step in (every, idle, right):
            assert [worst_wait(n, step, 1, i) for i in range(n)] == [n - 1] * n
    # but the share breaks: 0 and 1 always, N = 4, 0 gets 3 of every 4 grants
    pri, got = 1, [0] * 4
    for _ in range(400):
        g = rr_pick(0b0011, pri, 4)
        got[g.bit_length() - 1] += 1
        pri = rot(pri, 4)
    assert got == [300, 100, 0, 0]
    assert [sum(1 for g in rr_run([0b0011] * 400, 4) if g >> i & 1) for i in range(4)] == [200, 200, 0, 0]


def test_each_bug_fails_the_rule_the_page_names():
    full = [0b1111] * 16
    failing = {bug: {k for k, v in check_trace(full, q0054.rr(full, 4, bug), 4, 3).items() if v} for bug in ("stuck", "winner", "double")}
    assert failing == {"stuck": {"fair"}, "winner": {"fair"}, "double": {"onehot"}}


def test_wrr_bound_exhaustive_and_used_bits():
    def step(w):
        def f(state, req):
            pri, used = state
            g = rr_pick(req, pri, len(w))
            if g:
                i = g.bit_length() - 1
                used = used + 1 if g == pri else 1
                pri, used = (rot(g, len(w)), 0) if used == w[i] else (g, used)
            return g, (pri, used)
        return f
    for w in ([1, 2, 3], [3, 1, 1], [1, 1, 4], [1, 2, 3, 4], [4, 1, 2, 1]):
        assert [worst_wait(len(w), step(w), (1, 0), i) for i in range(len(w))] == [sum(w) - x for x in w], w
    # used holds 0 .. w_max - 1 between cycles: ceil(log2 w_max) bits (3 bits for w_max = 5)
    rng = random.Random(58)
    for w in ([1, 2, 3, 4], [5, 1], [5, 5, 5]):
        state, most = (1, 0), 0
        for _ in range(4000):
            _, state = step(w)(state, rng.randrange(1 << len(w)))
            most = max(most, state[1])
        assert most == max(w) - 1 and (most).bit_length() == (max(w) - 1).bit_length()
    assert (5 - 1).bit_length() == 3


def test_matrix_arbiter_flops():
    # one bit per pair (i < j): "i beats j"; a grant to i clears i's row and sets its column
    for n in (3, 4, 5):
        pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
        assert len(pairs) == n * (n - 1) // 2
        beats = {p: True for p in pairs}           # at reset the lower one beats the higher one
        wins = lambda i, j: beats[(i, j)] if i < j else not beats[(j, i)]   # noqa: E731
        last = [k - n for k in range(n)]           # the cycle of the last grant (0 the oldest at reset)
        rng = random.Random(n)
        for t in range(1, 500):
            req = rng.randrange(1, 1 << n)
            asking = [i for i in range(n) if req >> i & 1]
            win = [i for i in asking if all(wins(i, j) for j in asking if j != i)]
            assert len(win) == 1
            i = win[0]
            assert i == min(asking, key=lambda k: last[k])      # least recently granted
            for j in range(n):
                if j != i:
                    beats[(min(i, j), max(i, j))] = j < i      # j now beats i
            last[i] = t
    assert len([(i, j) for i in range(4) for j in range(i + 1, 4)]) == 6


def test_box_tasks():
    from page_tests import explorer_require, node_json

    full, both = [0b1111] * 16, [0b1001] * 16
    # 1: fixed 16/inf for requester 3; round robin 3/3; WRR 1, 2, 3, 4 gives 9/9 and 6/6
    assert q0054.max_wait(full, fixed_priority_all(full), 3) == 16
    assert [q0054.max_wait(full, rr_run(full, 4), i) for i in range(4)] == [3, 3, 3, 3]
    wg = wrr_run(full, [1, 2, 3, 4])
    assert q0054.max_wait(full, wg, 0) == 9 and q0054.max_wait(full, wg, 3) == 6
    # 2: 0 and 3 always, cycle 1: pri = 0010, dbl - pri = 10010111, requester 3 wins
    assert rr_run(both[:1], 4) == [0b0001]
    pri = rot(0b0001, 4)
    assert pri == 0b0010 and ((both[1] << 4 | both[1]) - pri) & 0xFF == 0b10010111 and rr_pick(both[1], pri, 4) == 0b1000
    # 3: the winner bug on 0 and 3: 0 wins every cycle, fairness fails from cycle 0;
    # the double bug on everybody: one-hot fails in 12 of the 16 cycles
    g = q0054.rr(both, 4, "winner")
    assert g == [1] * 16 and not any(g[u] >> 3 & 1 for u in range(0, 4))
    assert sum(1 for x in q0054.rr(full, 4, "double") if x & (x - 1)) == 12
    # 4: 0 and 3, requester 3 off at cycle 1 (it waited at cycle 0): the hold rule fails
    drawn = list(both)
    drawn[1] = 0b0001
    assert check_trace(drawn, rr_run(drawn, 4), 4, 3)["hold"] == 1
    # the box's WRR registers against the generator's trace
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify(m.arbWRRTrace({json.dumps(q0054.TRACE_REQS)}, [1, 2, 3, 4])));""")
    assert [(x["pri"], x["used"], x["g"]) for x in got] == [(p, u, g) for _, p, u, g in q0054.wrr_trace(q0054.TRACE_REQS, [1, 2, 3, 4])]


def fixed_priority_all(reqs):
    return [fixed_priority(r) for r in reqs]


def test_wrr_trace_table_is_the_page_code():
    rng = random.Random(59)
    for _ in range(40):
        n = rng.randint(2, 5)
        w = [rng.randint(1, 4) for _ in range(n)]
        reqs = [rng.randrange(1 << n) for _ in range(60)]
        assert [g for *_, g in q0054.wrr_trace(reqs, w)] == wrr_run(reqs, w) == q0054.wrr(reqs, w)
    trace = q0054.wrr_trace(q0054.TRACE_REQS, [1, 2, 3, 4])
    assert [g for *_, g in trace] == wrr_run(q0054.TRACE_REQS, [1, 2, 3, 4]) == [1, 2, 2, 4, 8, 8, 8, 8, 1]
    assert [u for _, _, u, _ in trace] == [0, 0, 1, 0, 1, 1, 2, 3, 0]


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
