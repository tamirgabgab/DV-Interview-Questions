"""Question 0097, the integer square root in hardware: the numbers the page states, recomputed
from the reference in tools/figures/q0097.py and checked against math.isqrt and Python's / and
%; the module's trace and the WaveDrom diagram; the generated blocks; the box's models under
Node against the same reference."""

import json
import math
import re
import sys

from extract_code import ROOT, question_path

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0097  # noqa: E402

PAGE = question_path(97).read_text(encoding="utf-8")


def icbrt(n):
    c = round(n ** (1 / 3))
    while c ** 3 > n:
        c -= 1
    while (c + 1) ** 3 <= n:
        c += 1
    return c


def test_reference_against_math():
    for n in range(1 << 16):
        r = math.isqrt(n)
        assert q0097.isqrt_ref(n) == (r, n - r * r), n
    for width in (2, 8, 20, 32, 54):
        for n in [0, 1, (1 << width) - 1] + [s * s + e for s in range(1, 1 << (width // 2), max(1, (1 << (width // 2)) // 300)) for e in (-1, 0, 1)]:
            if 0 <= n < 1 << width:
                r = math.isqrt(n)
                assert q0097.isqrt_ref(n, width) == (r, n - r * r), (width, n)
    for n in range(1 << 15):
        assert q0097.icbrt_ref(n, 15) == (icbrt(n), n - icbrt(n) ** 3), n
    for c in range(1, 256):
        for n in (c ** 3 - 1, c ** 3, c ** 3 + 1):
            if n < 1 << 24:
                assert q0097.icbrt_ref(n, 24) == (icbrt(n), n - icbrt(n) ** 3), n
    for a in range(0, 1 << 16, 37):
        for d in (1, 2, 3, 7, 10, 255, 256, 1000, 40000, 65535):
            s = q0097.div_steps(a, d)[-1]
            assert (s["q"], s["rem"]) == divmod(a, d), (a, d)
    zero = q0097.div_steps(1000, 0)[-1]
    assert (zero["q"], zero["rem"]) == ((1 << 16) - 1, 1000)


def test_trial_is_the_square_difference_and_or_is_a_sum():
    """2rb + b² = (r << (k+1)) | (1 << 2k): the two never share a bit, so OR is the sum, and the
    trial of a 16-bit n stays below 255² (fits in 16 bits)."""
    for n in range(0, 1 << 16, 7):
        r = 0
        for s in q0097.isqrt_steps(n):
            k, b = s["k"], s["b"]
            assert (r << (k + 1)) & (1 << (2 * k)) == 0
            assert s["trial"] == 2 * r * b + b * b == (r + b) ** 2 - r * r < 255 ** 2 + 1
            r = s["r"]


def test_page_numbers():
    st = q0097.isqrt_steps(1000)
    assert [s["trial"] for s in st] == [16384, 4096, 1024, 256, 320, 208, 116, 61]
    assert [s["before"] for s in st] == [1000, 1000, 1000, 1000, 744, 424, 216, 100]
    assert [s["r"] for s in st] == [0, 0, 0, 16, 24, 28, 30, 31]
    assert q0097.isqrt_ref(1000) == (31, 39) and 31 ** 2 + 39 == 1000 and 32 ** 2 > 1000
    assert (2 * 30 + 1) * 1 == 61 and (2 * 30 + 2) * 2 == 124 and 100 - 61 == 39     # the pencil method
    assert 16 * 16 == 256 and 2 * 16 * 8 + 64 == 320 and 2 * 24 * 4 + 16 == 208 and 2 * 28 * 2 + 4 == 116
    assert q0097.isqrt_ref(65535) == (255, 510) and 255 ** 2 == 65025 and 256 ** 2 == 65536
    # part c: the corner inputs and the maximum of 32 bits
    assert math.isqrt(2 ** 32 - 1) == 65535 and 2 ** 32 - 1 - 65535 ** 2 == 2 ** 17 - 2
    assert 2 * 65535 == 131070
    assert 65536 * 9 == 589824
    # part d
    assert divmod(1000, 7) == (142, 6) and 7 * 256 == 1792 > 1000 and 7 * 128 == 896
    d = q0097.div_steps(1000, 7)
    assert [s["k"] for s in d if s["ok"]] == [7, 3, 2, 1]
    c = q0097.icbrt_steps(1000, 12)
    assert [s["trial"] for s in c] == [512, 1216, 488, 331] and q0097.icbrt_ref(1000, 12) == (10, 0)
    assert q0097.icbrt_ref(2 ** 24 - 1, 24)[0] == 255 and 255 ** 3 < 2 ** 24
    # the traps and follow-ups
    assert int(math.sqrt(9999999999999999)) == 100000000 and math.isqrt(9999999999999999) == 99999999
    for n in range(20000):                          # rounding to the nearest: + 1 when rem > r
        r, rem = q0097.isqrt_ref(n)
        assert r + (rem > r) == (r + 1 if 4 * n >= (2 * r + 1) ** 2 else r), n   # sqrt(n) >= r + 1/2 exactly


def test_module_trace_and_wavedrom():
    cyc = q0097.seq_cycles(1000)
    assert [(r, rem) for _, _, r, rem, _, _ in cyc] == [(0, 1000)] * 4 + [(16, 744), (24, 424), (28, 216), (30, 100), (31, 39)]
    assert [busy for *_, busy, _ in cyc] == [1] * 8 + [0] and [done for *_, done in cyc] == [0] * 8 + [1]
    wave = re.search(r"```wavedrom\n(.*?)```", PAGE, re.S).group(1)
    root = re.search(r'name: "root",\s*wave: "([^"]+)", data: (\[[^\]]*\])', wave)
    rem = re.search(r'name: "rem",\s*wave: "([^"]+)", data: (\[[^\]]*\])', wave)
    # slot c + 1 shows the registers after clock c; '=' marks a new value
    want_root = [str(r) for i, (_, _, r, _, _, _) in enumerate(cyc) if i == 0 or r != cyc[i - 1][2]]
    want_rem = [str(m) for i, (_, _, _, m, _, _) in enumerate(cyc) if i == 0 or m != cyc[i - 1][3]]
    assert json.loads(root.group(2)) == want_root and json.loads(rem.group(2)) == want_rem
    for wv, idx in ((root.group(1), 2), (rem.group(1), 3)):
        assert len(wv) == 11
        for c, regs in enumerate(cyc):
            changed = c == 0 or regs[idx] != cyc[c - 1][idx]
            assert (wv[c + 1] == "=") == changed, (wv, c)
    busy = re.search(r'name: "busy",\s*wave: "([^"]+)"', wave).group(1)
    done = re.search(r'name: "done",\s*wave: "([^"]+)"', wave).group(1)
    assert busy == "01.......0." and done == "0........10"


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(97)


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    ns = list(range(0, 1 << 16, 97)) + [0, 1, 2, 3, 4, 1000, 4095, 4096, 65024, 65025, 65535]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(ns)}.map((n) => [m.isqSteps(n), m.isqRoot(n)])))")
    for n, (steps, root) in zip(ns, got):
        want = q0097.isqrt_steps(n)
        assert steps == want, n
        assert tuple(root) == q0097.isqrt_ref(n), n
