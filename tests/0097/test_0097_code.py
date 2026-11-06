"""Question 0097: the page's Python code (it runs as published) against math.isqrt, the
reference of tools/figures/q0097.py, divmod and an integer cube root: isqrt_bits on every
16-bit n and on wide inputs, isqrt_seq_model clock by clock, corner_inputs, divide_bits and
icbrt_bits."""

import math
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0097  # noqa: E402

ns = load_python(97)


def icbrt(n):
    c = round(n ** (1 / 3))
    while c ** 3 > n:
        c -= 1
    while (c + 1) ** 3 <= n:
        c += 1
    return c


def test_isqrt_bits():
    f = ns["isqrt_bits"]
    for n in range(1 << 16):
        r = math.isqrt(n)
        assert f(n) == (r, n - r * r), n
    assert f(1000) == (31, 39) and f(65535) == (255, 510)
    rng = random.Random(97)
    for width in (32, 54, 64):
        for n in [0, 1, (1 << width) - 1] + [rng.randrange(1 << width) for _ in range(2000)]:
            r = math.isqrt(n)
            assert f(n, width) == (r, n - r * r), (width, n)
    assert f(10 ** 16 - 1, 54) == (99999999, 199999998)


def test_seq_model():
    m = ns["isqrt_seq_model"]
    for n in list(range(0, 1 << 16, 13)) + [1000, 65535, 0]:
        tr = m(n)
        assert len(tr) == 9, n
        want = q0097.seq_cycles(n)
        assert tr == [(k, r, rem, busy, done) for _, k, r, rem, busy, done in want], n
        assert tr[-1][1:3] == (math.isqrt(n), n - math.isqrt(n) ** 2)


def test_corner_inputs():
    c = ns["corner_inputs"]
    cases = c(32)
    assert cases == sorted(set(cases)) and cases[0] == 0 and cases[-1] == 2 ** 32 - 1
    squares = set(s * s for s in range(1, 1 << 16))
    assert squares <= set(cases) and set(s - 1 for s in squares) <= set(cases)
    assert all((1 << i) in cases and (1 << i) - 1 in cases for i in range(32))
    edges = c(16, 0)
    assert len(edges) == len({0, 1, 65535} | {s * s for s in range(1, 256)} | {s * s - 1 for s in range(1, 256)}
                             | {1 << i for i in range(16)} | {(1 << i) - 1 for i in range(16)})
    f = ns["isqrt_bits"]
    for n in cases:                                   # the page's own 32-bit isqrt on its own cases
        r = math.isqrt(n)
        assert f(n, 32) == (r, n - r * r), n


def test_divide_bits():
    f = ns["divide_bits"]
    for a in range(0, 1 << 16, 11):
        for d in (1, 2, 3, 7, 10, 255, 256, 1000, 40000, 65535):
            assert f(a, d) == divmod(a, d), (a, d)
    rng = random.Random(7)
    for _ in range(20000):
        a, d = rng.randrange(1 << 16), rng.randrange(1, 1 << 16)
        assert f(a, d) == divmod(a, d)
    assert f(1000, 7) == (142, 6) and f(1000, 0) == ((1 << 16) - 1, 1000)
    for a in range(0, 1 << 16, 37):
        s = q0097.div_steps(a, 7)[-1]
        assert f(a, 7) == (s["q"], s["rem"])


def test_icbrt_bits():
    f = ns["icbrt_bits"]
    for n in range(1 << 16):
        assert f(n) == (icbrt(n), n - icbrt(n) ** 3), n
    for c in range(1, 256):
        for n in (c ** 3 - 1, c ** 3, c ** 3 + 1):
            if n < 1 << 24:
                assert f(n) == (icbrt(n), n - icbrt(n) ** 3), n
    assert f(1000) == (10, 0) and f(2 ** 24 - 1) == (255, 2 ** 24 - 1 - 255 ** 3)
    for n in range(0, 1 << 12):
        assert f(n, 12) == q0097.icbrt_ref(n, 12)
