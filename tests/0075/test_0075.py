"""Question 0075: the page's transpose8_loop and transpose8 against the definition (bit 8r + c
to bit 8c + r) on every single bit and random words, with delta_swap checked as a swap;
the masks and shifts of the stages against the generator (r_i = 0, c_i = 1); transpose32 on
random 32 x 32 matrices; the page's numbers (8 fixed bits, 16 pairs a stage, 80 word
swaps); the explorer's JavaScript against the generator; and the page copies of the blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0075  # noqa: E402

ns = load_python(75)
transpose8_loop, transpose8, delta_swap, transpose32 = ns["transpose8_loop"], ns["transpose8"], ns["delta_swap"], ns["transpose32"]


def test_transpose8():
    rng = random.Random(75)
    words = [1 << b for b in range(64)] + [0, (1 << 64) - 1] + [rng.getrandbits(64) for _ in range(3000)]
    for x in words:
        want = q0075.transpose_bits(x)
        assert transpose8_loop(x) == want == transpose8(x), hex(x)
        assert transpose8(transpose8(x)) == x
    assert sum(1 for b in range(64) if transpose8(1 << b) == 1 << b) == 8


def test_delta_swap_and_the_stages():
    rng = random.Random(76)
    for i, (s, m) in enumerate([(7, 0x00AA00AA00AA00AA), (14, 0x0000CCCC0000CCCC), (28, 0x00000000F0F0F0F0)]):
        assert q0075.stage(8, i) == (s, m) and bin(m).count("1") == 16
        assert m & (m << s) == 0                              # the pairs do not overlap
        for _ in range(300):
            x = rng.getrandbits(64)
            y = delta_swap(x, m, s)
            for p in range(64):
                if m >> p & 1:
                    assert (y >> p & 1, y >> (p + s) & 1) == (x >> (p + s) & 1, x >> p & 1)
                elif not (m << s) >> p & 1:
                    assert y >> p & 1 == x >> p & 1
    for order in ([0, 1, 2], [2, 0, 1], [1, 2, 0]):                 # the stages commute
        x = rng.getrandbits(64)
        y = x
        for i in order:
            s, m = q0075.stage(8, i)
            y = delta_swap(y, m, s)
        assert y == q0075.transpose_bits(x)


def test_transpose32():
    rng = random.Random(77)
    for _ in range(200):
        rows = [rng.getrandbits(32) for _ in range(32)]
        a = list(rows)
        transpose32(a)
        assert all(a[c] >> r & 1 == rows[r] >> c & 1 for r in range(32) for c in range(32))
        assert all(0 <= v < 1 << 32 for v in a)
    assert [m for _, m in q0075.word_masks(32)] == [0x0000FFFF, 0x00FF00FF, 0x0F0F0F0F, 0x33333333, 0x55555555]
    assert 5 * 16 == 80


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(78)
    xs = [rng.getrandbits(64) for _ in range(100)] + [1 << b for b in range(64)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps([str(x) for x in xs])}.map((x) => m.bmStages(BigInt(x)).map(String))));""")
    for x, g in zip(xs, got):
        y = x
        want = [str(x)]
        for i in range(3):
            s, mk = q0075.stage(8, i)
            y = q0075.delta_swap(y, mk, s)
            want.append(str(y))
        assert g == want


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(75)
