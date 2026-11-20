"""Question 0110: the page's delay3, en_gate and avg8 (as published) against the references of
tools/figures/q0110.py, which tests/0110/tb.sv checks against Verilator: the page's inputs,
random inputs, and every pair of bytes for the average. The models also meet the designer's
intent where the fix does, and miss it exactly as the solutions say where the bug does."""

import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0110  # noqa: E402

ns = load_python(110)
delay3, en_gate, avg8 = ns["delay3"], ns["en_gate"], ns["avg8"]


def test_page_inputs():
    assert delay3(q0110.D_A, blocking=True) == q0110.delay_trace(q0110.D_A, True)
    assert delay3(q0110.D_A) == q0110.delay_trace(q0110.D_A)
    assert en_gate(q0110.EN_B, q0110.D_B, default=False) == q0110.gate_trace(q0110.EN_B, q0110.D_B, False)
    assert en_gate(q0110.EN_B, q0110.D_B) == q0110.gate_trace(q0110.EN_B, q0110.D_B)
    for a, b in zip(q0110.A_C, q0110.B_C):
        assert avg8(a, b, width=8) == q0110.avg(a, b, 8) and avg8(a, b) == q0110.avg(a, b)


def test_random_delay_line():
    rng = random.Random(110)
    for _ in range(500):
        d = [rng.randint(0, 1) for _ in range(rng.randint(1, 40))]
        bug, fix = delay3(d, blocking=True), delay3(d)
        assert bug == q0110.delay_trace(d, True) and fix == q0110.delay_trace(d)
        # the fix: q3 is d three cycles back; the bug: q1 = q2 = q3 = d one cycle back
        assert [r[2] for r in fix] == q0110.delay_want(d)
        assert all(r == (k and d[k - 1],) * 3 for k, r in enumerate(bug))


def test_random_gate():
    rng = random.Random(1100)
    for _ in range(500):
        n = rng.randint(1, 40)
        en, d = [rng.randint(0, 1) for _ in range(n)], [rng.randint(0, 15) for _ in range(n)]
        bug, fix = en_gate(en, d, default=False), en_gate(en, d)
        assert bug == q0110.gate_trace(en, d, False) and fix == q0110.gate_trace(en, d)
        assert fix == q0110.gate_want(en, d)
        for k in range(n):                     # the bug holds the d of the last cycle with en high
            last = max((j for j in range(k + 1) if en[j]), default=None)
            assert bug[k] == (0 if last is None else d[last])


def test_every_pair_of_bytes():
    wrong = 0
    for a in range(256):
        for b in range(256):
            assert avg8(a, b) == (a + b) // 2 == q0110.avg(a, b)
            got = avg8(a, b, width=8)
            assert got == q0110.avg(a, b, 8)
            if got != (a + b) // 2:
                wrong += 1
                assert a + b >= 256 and (a + b) // 2 - got == 128
            else:
                assert a + b < 256
    assert wrong == 32640
