"""Question 0105: the page's Python code (it runs as published) against the references of
tools/figures/q0105.py, which work on strings of bits: mix64, rank, distinct_exact,
one_register, the HLL class (its registers bit-exact, its estimate, the merge equal to the union)
on every stream and register count, and the pipeline clock by clock: with forwarding it gives
the registers of the reference on random streams with bubbles and a hot register; without it,
it differs exactly when two updates of one register come back to back."""

import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0105  # noqa: E402

ns = load_python(105)


def test_mix64_and_rank():
    rng = random.Random(105)
    xs = [0, 1, 64, q0105.MASK, 877_363_008] + [rng.getrandbits(64) for _ in range(2000)]
    assert [ns["mix64"](x) for x in xs] == [q0105.mix64(x) for x in xs]
    for w in (1, 4, 54, 60, 64):
        vals = [0, 1, (1 << w) - 1, 1 << (w - 1)] + [rng.getrandbits(w) >> rng.randrange(w) for _ in range(200)]
        for v in vals:
            assert ns["rank"](v, w) == q0105.first_one(format(v, f"0{w}b"))
    assert ns["rank"](0, 64) == 65


def test_exact_and_one_register():
    for name in ("rand", "dup", "seq"):
        s = q0105.stream(name)
        assert ns["distinct_exact"](s) == len(set(s))
    for n, r, _ in q0105.grow_rows()[:5]:
        assert ns["one_register"]([q0105.distinct(t) for t in range(1, n + 1)]) == r
    assert ns["one_register"]([]) == 0


def run_hll(addrs, p):
    h = ns["HLL"](p)
    for a in addrs:
        h.add(a)
    return h


def test_hll_against_reference():
    for name in ("rand", "dup", "seq"):
        s = q0105.stream(name)
        for p in (4, 6, 8, 10, 12):
            h = run_hll(s, p)
            ref = q0105.registers(s, p)
            assert h.regs == ref and h.m == 1 << p
            assert h.estimate() == q0105.estimate(ref)
    for n, _, e in q0105.grow_rows()[:5]:
        assert run_hll([q0105.distinct(t) for t in range(1, n + 1)], 10).estimate() == e
    # empty: every register empty, linear counting gives 0
    assert run_hll([], 10).estimate() == 0
    raw, est, zeros = q0105.small_range_example()
    assert run_hll(q0105.stream("rand", 100), 10).estimate() == est


def test_merge_is_union():
    rng = random.Random(1050)
    for _ in range(20):
        p = rng.choice((4, 6, 8, 10))
        a = [rng.getrandbits(32) * 64 for _ in range(rng.randint(0, 3000))]
        b = rng.sample(a, len(a) // 2) + [rng.getrandbits(32) * 64 for _ in range(rng.randint(0, 3000))]
        ha, hb = run_hll(a, p), run_hll(b, p)
        ha.merge(hb)
        assert ha.regs == q0105.registers(a + b, p) == run_hll(b + a, p).regs
    _, _, u, regs = q0105.merge_example()
    ha = run_hll([q0105.distinct(t) for t in range(1, 60001)], 10)
    ha.merge(run_hll([q0105.distinct(t) for t in range(30001, 90001)], 10))
    assert ha.regs == regs and ha.estimate() == u


def back_to_back(inputs, p):
    """Whether two valid inputs in a row update the same register."""
    js = [None if a is None else q0105.split(q0105.mix64(a), p)[0] for a in inputs]
    return any(x is not None and x == y for x, y in zip(js, js[1:]))


def test_pipeline():
    # the page's table: A, B, a bubble, C into register 12
    regs = ns["pipeline"](q0105.PIPE_IN, 4)
    bad = ns["pipeline"](q0105.PIPE_IN, 4, forward=False)
    assert regs == q0105.pipe_rows(True)[-1][3] and bad == q0105.pipe_rows(False)[-1][3]
    assert regs[12] == 4 and bad[12] == 2
    assert ns["pipeline"]([q0105.PIPE_A, q0105.PIPE_B], 4, forward=False)[12] == 1
    rng = random.Random(10500)
    caught = 0
    for _ in range(300):
        p = rng.choice((2, 4, 6))
        hot = [rng.getrandbits(32) * 64 for _ in range(rng.randint(1, 4))]
        n = rng.randint(0, 60)
        inputs = [None if rng.random() < 0.25 else rng.choice(hot) if rng.random() < 0.5 else rng.getrandbits(32) * 64
                  for _ in range(n)]
        ref = q0105.registers([a for a in inputs if a is not None], p)
        assert ns["pipeline"](inputs, p) == ref
        assert [st[3] for st in q0105.pipe_trace(inputs, p)][-1] == ref if n else True
        nofwd = ns["pipeline"](inputs, p, forward=False)
        assert nofwd == [st[3] for st in q0105.pipe_trace(inputs, p, forward=False)][-1] if n else True
        if not back_to_back(inputs, p):
            assert nofwd == ref                    # no hazard: forwarding changes nothing
        caught += nofwd != ref
    assert caught > 30                             # the mutant is caught often
