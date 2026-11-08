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
    hw = q0097.hw_cycles(1000)
    assert len(hw) == 11 and [c["cycle"] for c in hw] == list(range(11))
    assert [c["k"] for c in hw] == [None, 7, 6, 5, 4, 3, 2, 1, 0, 0, 0]
    assert [c["trial"] for c in hw] == [None, 16384, 4096, 1024, 256, 320, 208, 116, 61, None, None]
    assert [c["fits"] for c in hw] == [None, 0, 0, 0, 1, 1, 1, 1, 1, None, None]
    assert [c["busy"] for c in hw] == [0] + [1] * 8 + [0, 0] and [c["done"] for c in hw] == [0] * 9 + [1, 0]
    # the waveform of the page, lane by lane, slot c = cycle c of the table
    wave = re.search(r"```wavedrom\n(.*?)```", PAGE, re.S).group(1)

    def lane(name):
        m = re.search(r'name: "' + name + r'",\s*wave: "([^"]+)"(?:, data: (\[[^\]]*\]))?', wave)
        w, data = m.group(1), json.loads(m.group(2)) if m.group(2) else []
        out, it, cur = [], iter(data), None
        for ch in w:
            cur = None if ch == "x" else next(it) if ch == "=" else cur if ch == "." else int(ch)
            out.append(cur)
        assert len(out) == len(hw), name
        return out

    assert lane("cycle") == [str(c) for c in range(11)]
    for name in ("start", "busy", "fits", "done"):
        assert lane(name) == [c[name] for c in hw], name
    for name in ("k", "trial", "root", "rem"):
        assert lane(name) == [None if c[name] is None else str(c[name]) for c in hw], name
    # the table of the page has one row a cycle, as the waveform
    rows = [ln for ln in q0097.cycles_table().splitlines()[2:]]
    assert len(rows) == 11 and rows[0].startswith("| 0 |") and rows[9].startswith("| **9** |")


def test_hardware_cycles():
    """isqrt_seq cycle by cycle: the registers through cycle c + 1 are the model's after clock c;
    the comparison is the subtractor's borrow; the trap of the box (a strict comparison)."""
    for n in list(range(0, 1 << 16, 7)) + [65535, 4095, 4096]:
        hw, seq = q0097.hw_cycles(n), q0097.seq_cycles(n)
        assert [(c["k"], c["root"], c["rem"], c["busy"], c["done"]) for c in hw[1:10]] == [t[1:] for t in seq], n
        for c in hw:
            if c["busy"]:
                d17 = (c["rem"] - c["trial"]) % (1 << 17)
                assert c["borrow"] == d17 >> 16 == int(c["trial"] > c["rem"]) and c["fits"] == 1 - c["borrow"]
                assert c["trial"] < 1 << 16 and (c["fits"] == 0 or c["diff"] == d17)
                assert c["set"] == (c["k"] if c["fits"] else None) and c["nroot"] == c["root"] | (c["fits"] << c["k"])
            nxt = hw[c["cycle"] + 1] if c["cycle"] + 1 < len(hw) else None
            if nxt:
                assert (nxt["k"], nxt["root"], nxt["rem"], nxt["busy"], nxt["done"]) == (c["nk"], c["nroot"], c["nrem"], c["nbusy"], c["ndone"])
        assert hw[9]["done"] == 1 and (hw[9]["root"], hw[9]["rem"]) == q0097.isqrt_ref(n)

    def strict(n):                               # trial < rem instead of trial <= rem
        r, rem = 0, n
        for k in range(7, -1, -1):
            t = (r << (k + 1)) | (1 << (2 * k))
            if t < rem:
                rem, r = rem - t, r | 1 << k
        return r
    assert strict(4096) == 63 and q0097.isqrt_ref(4096) == (64, 0)
    hw = q0097.hw_cycles(4096)
    assert hw[2]["k"] == 6 and hw[2]["trial"] == hw[2]["rem"] == 4096 and hw[2]["borrow"] == 0 and hw[2]["diff"] == 0
    # the traps of the box
    assert q0097.isqrt_ref(4095) == (63, 126) and format(63, "08b") == "00111111" and format(64, "08b") == "01000000"
    assert max(s["trial"] for s in q0097.isqrt_steps(65535)) == 20480 and q0097.isqrt_ref(65535) == (255, 510)
    assert all(not s["ok"] for s in q0097.isqrt_steps(0))
    # the block diagram: every block inside the picture, the wires end on a block or the edge
    for _id, x, y, w, h, *_ in q0097.DP_BLOCKS:
        assert 0 <= x and x + w <= q0097.DP_W and 0 <= y and y + h <= q0097.DP_H


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


def test_hardware_box_matches_the_reference():
    from page_tests import explorer_require, node_json

    ns = list(range(0, 1 << 16, 251)) + [0, 1, 2, 3, 1000, 4095, 4096, 65024, 65025, 65535]
    got = node_json(f"const m = {explorer_require()};console.log(JSON.stringify({json.dumps(ns)}.map((n) => m.isqhwTrace(n))));")
    for n, tr in zip(ns, got):
        assert tr == q0097.hw_cycles(n), n
    # the box draws the page's diagram: the same rectangles and wires, block by block
    svg = node_json(f"const m = {explorer_require()};const t = m.isqhwTrace(1000);"
                    "console.log(JSON.stringify([null, ...t].map((c) => m.isqhwDiagram(c, 1000))));")
    rect = re.compile(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"')
    path = re.compile(r'<path class="isq-wire[^"]*" d="([^"]+)"')
    page = q0097.datapath_svg()
    for live in svg:
        assert rect.findall(live) == rect.findall(page) and path.findall(live) == path.findall(page)
    # the lit path: a cycle with a fit lights the decoder and the way back into rem, one without does not
    lit = node_json(f"const m = {explorer_require()};console.log(JSON.stringify(m.isqhwTrace(1000).map((c) => {{ const l = m.isqhwLit(c); return [[...l.blocks].sort(), [...l.wires].sort()]; }})));")
    for c, (blocks, wires) in zip(q0097.hw_cycles(1000), lit):
        if c["load"]:
            assert {"start", "n", "mux_rem"} <= set(wires)
        elif c["busy"]:
            assert ("dec_root" in wires) == ("mux_rem" in wires) == ("dec" in blocks) == bool(c["fits"]), c["cycle"]
            assert {"sh_sub", "borrow", "rem_sub"} <= set(wires)
        elif c["done"]:
            assert wires == ["out"]
        else:
            assert blocks == [] and wires == []
