"""Question 0055: the page's div3_msb, div3_lsb and div_fsm against the value itself on every
bit string up to 12 bits and on random digit strings in several bases; the generator's
minimized machines (the state counts on the page, the LSB machine of 3 being the MSB one
with 1 and 2 swapped); the page's numbers; the explorer's JavaScript; the page copies
of the generated blocks; and the keys the steps light in the figure beside them."""

import itertools
import json
import random
import sys
from math import gcd

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0055  # noqa: E402

ns = load_python(55)
div3_msb, div3_lsb, div_fsm = (ns[k] for k in ("div3_msb", "div3_lsb", "div_fsm"))


def truth(digits, m, base, lsb):
    """After each digit, is the number read so far divisible by m (from its value)."""
    return [q0055.value(digits[:i + 1], base, lsb) % m == 0 for i in range(len(digits))]


def test_every_bit_string():
    for n in range(1, 13):
        for bits in itertools.product((0, 1), repeat=n):
            bits = list(bits)
            assert div3_msb(bits) == truth(bits, 3, 2, False), bits
            assert div3_lsb(bits) == truth(bits, 3, 2, True), bits


def test_page_examples():
    assert div3_msb([1, 1, 0]) == [False, True, True]           # 1, 3, 6
    assert div3_msb([1, 1, 0, 1]) == [False, True, True, False]  # 1, 3, 6, 13 (part a, step 4)
    assert div3_lsb([0, 1, 1]) == [True, False, True]           # 0, 2, 6
    assert int("1011", 2) == 11 and 11 % 3 == 2
    assert pow(10, -1, 7) == 5 and pow(2, -1, 3) == 2


def test_general_machine():
    rng = random.Random(55)
    for _ in range(400):
        base = rng.choice([2, 3, 4, 8, 10, 16])
        m = rng.choice([x for x in range(2, 20) if gcd(x, base) == 1])
        digits = [rng.randrange(base) for _ in range(rng.randint(1, 40))]
        for lsb in (False, True):
            assert div_fsm(digits, m, base, lsb) == truth(digits, m, base, lsb), (digits, m, base, lsb)
    assert div_fsm([1, 1, 0], 3) == div3_msb([1, 1, 0])
    assert div_fsm([0, 1, 1], 3, lsb=True) == div3_lsb([0, 1, 1])


def test_state_counts():
    # odd m: m states both ways; the naive LSB machine is m times the order of 2 mod m
    for m in range(3, 17, 2):
        order = next(k for k in range(1, m) if pow(2, k, m) == 1)
        assert q0055.naive_msb(m) == (m, m) and q0055.naive_lsb(m) == (m, m * order), m
    assert q0055.naive_lsb(3) == (3, 6) and q0055.naive_lsb(5) == (5, 20)
    # even m = 2^a m': m' + a from the MSB, m' + a + 1 from the LSB (the follow-up)
    for m in range(2, 17, 2):
        a = (m & -m).bit_length() - 1
        odd = m >> a
        assert q0055.naive_msb(m)[0] == odd + a and q0055.naive_lsb(m)[0] == odd + a + 1, m
    assert [q0055.naive_msb(m)[0] for m in (6, 12)] == [4, 5] and [q0055.naive_lsb(m)[0] for m in (6, 12)] == [5, 6]
    # base 10 and m = 5 (the trap): 2 from the MSB, 3 from the LSB
    assert q0055.naive_msb(5, 10)[0] == 2 and q0055.naive_lsb(5, 10)[0] == 3
    # the remainder itself from the LSB needs every naive state: they all differ in output or next
    for m in (3, 5, 7):
        order = next(k for k in range(1, m) if pow(2, k, m) == 1)
        states = {(r, pow(2, k, m)) for r in range(m) for k in range(order)}
        sig = {s: (s[0], (s[0] + s[1]) % m) for s in states}
        assert len(set(sig.values())) == len(states) == m * order


def test_lsb_three_is_msb_three_mirrored():
    msb, lsb = q0055.table(3, 2, False), q0055.table(3, 2, True)
    swap = [0, 2, 1]
    assert all(lsb[swap[s]][d] == swap[msb[s][d]] for s in range(3) for d in (0, 1))
    assert q0055.table(5, 2, False) != q0055.table(5, 2, True)
    # the multipliers of k bits a cycle: 4 = 1 mod 3 and 8 = 1 mod 7, a digit sum
    assert pow(4, 1, 3) == pow(4, -1, 3) == 1 and pow(8, 1, 7) == pow(8, -1, 7) == 1


def test_explorer_matches_the_page_code():
    from page_tests import explorer_require, node_json

    rng = random.Random(56)
    cases = []
    for _ in range(80):
        base = rng.choice([2, 4, 8, 10, 16])
        m = rng.choice([x for x in range(3, 16, 2) if gcd(x, base) == 1])
        cases.append([m, base, [rng.randrange(base) for _ in range(rng.randint(1, 20))]])
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([mm, b, ds]) => [
        m.divTable(mm, b, false), m.divTable(mm, b, true), m.divRun(ds, mm, b, false), m.divRun(ds, mm, b, true)])));""")
    for (m, base, digits), (tm, tl, rm, rl) in zip(cases, got):
        assert tm == q0055.table(m, base, False) and tl == q0055.table(m, base, True)
        for run, lsb in ((rm, False), (rl, True)):
            seq = list(reversed(digits)) if lsb else digits      # the box feeds the number's digits
            assert [s == 0 for s in run[1:]] == div_fsm(seq, m, base, lsb)
            assert run[0] == 0 and len(run) == len(digits) + 1


def test_steps_light_the_right_parts():
    """Each figure beside the steps (div.steps-fig): every key a step lights exists in the
    figure, and the example step walks the machine's own arcs, ending in the states the
    text names."""
    import re

    page = next((ROOT / "docs" / "questions").rglob("0055-*.md")).read_text(encoding="utf-8")
    plans = [json.loads(m) for m in re.findall(r"data-fig-steps='([^']+)'", page)]
    assert len(plans) == 2
    for plan, (fig, lsb, bits, path) in zip(plans, ((0, False, [1, 1, 0, 1], [1, 0, 0, 1]), (4, True, [0, 1, 1], [0, 2, 0]))):
        keys = set(re.findall(r'data-fig="([^"]+)"', q0055.blocks()[fig]))
        lit = {k for step in plan for group in step.split(">") for k in group.split()}
        assert lit <= keys, lit - keys
        nxt, state, walk = q0055.table(3, 2, lsb), 0, []
        for b in bits:
            j = nxt[state][b]
            walk.append(f"e{state}-{b}-{j} n{j}")
            state = j
        assert plan[3].split(">") == walk
        assert [int(g.split()[1][1:]) for g in walk] == path


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(55)


def test_flip_flop_equations():
    """The D flip-flop implementation of parts a and b: the minimal equations the generator
    finds from the K-maps (11 a don't care) give the page's machines on every state and
    bit, they are the ones the page shows, 11 behaves as the page says, and part b is part
    a with the two flip-flops swapped."""
    page = next((ROOT / "docs" / "questions").rglob("0055-*.md")).read_text(encoding="utf-8")
    want = {False: {"D1": ["Q₁·b", "Q₀·b̄"], "D0": ["Q̄₁·Q̄₀·b", "Q₁·b̄"]},
            True: {"D1": ["Q̄₁·Q̄₀·b", "Q₀·b̄"], "D0": ["Q₁·b̄", "Q₀·b"]}}
    for lsb in (False, True):
        eqs = dict(q0055.equations(lsb))
        assert {n: [q0055.term_uni(t) for t in ts] for n, ts in eqs.items()} == want[lsb]
        step = ns["div3_lsb" if lsb else "div3_msb"]
        for state in range(3):
            q1, q0 = q0055.ENC[state]
            for b in (0, 1):
                nxt = (q0055.evaluate(eqs["D1"], q1, q0, b), q0055.evaluate(eqs["D0"], q1, q0, b))
                assert nxt == q0055.ENC[q0055.table(3, 2, lsb)[state][b]]
        # the circuit, run on bit strings, against the page's function
        for n in range(1, 9):
            for bits in itertools.product((0, 1), repeat=n):
                q1 = q0 = 0
                out = []
                for b in bits:
                    q1, q0 = q0055.evaluate(eqs["D1"], q1, q0, b), q0055.evaluate(eqs["D0"], q1, q0, b)
                    out.append(not q1 and not q0)
                assert out == step(list(bits)), (lsb, bits)
        for n, ts in eqs.items():
            assert q0055.equation_tex(n, ts).replace(" = ", " &= ", 1) in page
    assert q0055.stuck(False) == [(1, 1), (1, 0)] and q0055.stuck(True) == [(1, 1), (0, 1)]
    a, b = dict(q0055.equations(False)), dict(q0055.equations(True))
    swap = lambda t: (t[1], t[0], t[2])
    assert sorted(map(swap, a["D0"]), key=str) == sorted(b["D1"], key=str)
    assert sorted(map(swap, a["D1"]), key=str) == sorted(b["D0"], key=str)
