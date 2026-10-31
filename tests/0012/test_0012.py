from extract_code import load_python

ns = load_python(12)
is_special, find_special = ns["is_special"], ns["find_special"]


def reference(x):
    """The definition, digit by digit, with no string formatting."""
    d = sorted([x // 100, x // 10 % 10, x % 10])
    small = 100 * d[0] + 10 * d[1] + d[2]
    big = 100 * d[2] + 10 * d[1] + d[0]
    return int(big - small == x)


def test_page_examples():
    for x in (352, 7, 45, 111, 99, 594):
        assert is_special(x) == 0, x
    assert is_special(0) == 1
    assert is_special(495) == 1


def test_matches_definition():
    for x in range(1000):
        assert is_special(x) == reference(x), x


def test_final_array():
    assert find_special() == [0, 495]


def test_difference_is_a_multiple_of_99():
    # Step 1 of the proof: only the ten multiples of 99 can be special
    for x in range(1000):
        d = sorted(f"{x:03d}")
        assert (int("".join(reversed(d))) - int("".join(d))) % 99 == 0
    assert [x for x in range(0, 1000, 99) if is_special(x)] == [0, 495]


def test_explorer_matches_page_code():
    """The Kaprekar explorer: its step against the page's is_special on every number,
    every chain ending at 495 (or 0 for repeated digits) within 6 steps, and the
    histogram summing to 1,000."""
    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      const chains = Array.from({{length: 1000}}, (_, x) => m.kapChain(x, 3));
      console.log(JSON.stringify({{
        special: chains.map((c) => c.steps[0].special), ends: chains.map((c) => [c.end, c.length, c.fixed]),
        first: chains.map((c) => [c.steps[0].largest, c.steps[0].smallest, c.steps[0].diff]),
        hist: m.kapHistogram(3),
      }}));""")
    for x in range(1000):
        assert got["special"][x] == bool(ns["is_special"](x))
        largest, smallest, diff = got["first"][x]
        digits = sorted(f"{x:03d}")
        assert (largest, smallest, diff) == (int("".join(reversed(digits))), int("".join(digits)), int("".join(reversed(digits))) - int("".join(digits)))
        end, length, fixed = got["ends"][x]
        assert fixed and length <= 6
        assert end == (0 if len(set(f"{x:03d}")) == 1 else 495), x
    assert got["hist"]["ends"] == {"0": 10, "495": 990}
    assert sum(got["hist"]["hist"]["495"]) == 990 and len(got["hist"]["hist"]["495"]) == 7
    assert got["ends"][352] == [495, 4, True]                        # 352 -> 297 -> 693 -> 594 -> 495


# --- part c: three digits in base b ---------------------------------------------------------

import sys  # noqa: E402

from extract_code import ROOT  # noqa: E402

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0012  # noqa: E402

step_b, attractor_b, chain_b = ns["kaprekar_step_b"], ns["kaprekar_attractor_b"], ns["kaprekar_chain_b"]


def test_base_b_page_numbers():
    assert attractor_b(10) == [495] and attractor_b(2) == [3] and attractor_b(12) == [858] and attractor_b(16) == [8 * 255]
    assert attractor_b(3) == [8, 16] and attractor_b(7) == [144, 192] and attractor_b(11) == [600, 720]
    assert [q0012.text(v, 7) for v in chain_b(301, 7)] == ["610", "561", "462", "363"]
    assert [step_b(v, 7) for v in (301, 288, 240, 192, 144)] == [288, 240, 192, 144, 192]
    assert [q0012.spread(v, 7) for v in (301, 288, 240, 192, 144)] == [6, 5, 4, 3, 4]
    assert step_b(495, 10) == 495 and step_b(11, 2) == 3 and step_b(3, 2) == 3
    assert chain_b(100, 10) == [100, 99, 891, 792, 693, 594, 495]              # the longest chain in base 10
    for b in range(2, 17):
        assert step_b(x := attractor_b(b)[0], b) == (x if b % 2 == 0 else attractor_b(b)[1])
        if b % 2:
            assert all(step_b(v, b) == attractor_b(b)[1 - i] for i, v in enumerate(attractor_b(b)))
    assert step_b(10 * 100 + 9 * 10 + 5, 10) == step_b(495, 10)                # the middle digit cancels


def test_base_b_every_number():
    """Exhaustive: in every base from 2 to 16 every number reaches the attractor (or 0 when
    its digits are equal), the step is d (b^2 - 1), the digits of the result are
    (d - 1, b - 1, b - d), the next d is max(b - d, d - 1), and the longest chain has
    floor(b / 2) + 1 steps (1 in bases 2 and 3)."""
    for b in range(2, 17):
        att = set(attractor_b(b))
        longest = 0
        for x in range(b ** 3):
            digits = sorted(q0012.digits(x, b))
            d = digits[2] - digits[0]
            y = step_b(x, b)
            assert y == d * (b * b - 1) == q0012.step(x, b)
            if d:
                assert q0012.digits(y, b) == [d - 1, b - 1, b - d]
                assert q0012.spread(y, b) == max(b - d, d - 1)
            c = chain_b(x, b)
            assert c == q0012.chain(x, b)
            assert c[-1] in att or (c[-1] == 0 and len(set(q0012.digits(x, b))) == 1)
            longest = max(longest, len(c) - 1)
        assert longest == (1 if b <= 3 else b // 2 + 1), b                   # d = 1 is already at the attractor in bases 2 and 3
        # the attractor is a fixed point or a 2-cycle, and the only one: every value that maps to itself
        # or to its image's image is in it
        own = {x for x in range(b ** 3) if step_b(step_b(x, b), b) == x and x != 0}
        assert own == att, b


def test_base_b_tables_and_figures():
    even = q0012.even_table().splitlines()[2:]
    assert len(even) == 8 and "**495**" in even[4] and "**5B6**" in even[5] and "**011**" in even[0]
    odd = q0012.odd_table().splitlines()[2:]
    assert len(odd) == 7 and "**022** ↔ **121**" in odd[0] and "**4A6** ↔ **5A5**" in odd[4]
    ex = q0012.example_table().splitlines()[2:]
    assert len(ex) == 5 and ex[0].endswith("| ‏6 |") and "**561**" in ex[0] and "**363**" in ex[2] and "**264**" in ex[3] and ex[4].endswith("| ‏4 |")
    assert q0012.chain_lengths(10) == {0: 2, 1: 158, 2: 144, 3: 270, 4: 222, 5: 150, 6: 54}
    assert sum(q0012.chain_lengths(7).values()) == 343
    from page_tests import assert_figures_match

    assert_figures_match(12)


def test_base_b_explorer_matches_page_code():
    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      const out = {{}};
      for (let b = 2; b <= 16; b++) {{
        const chains = [], steps = [];
        for (let x = 0; x < b * b * b; x++) {{ chains.push(m.kbChain(x, b)); const s = m.kbStep(x, b); steps.push([s.diff, s.d, s.dNext, s.digits]); }}
        out[b] = {{ att: m.kbAttractor(b), chains, steps, hist: m.kbHistogram(b), text: m.kbText(m.kbAttractor(b)[0], b), parse: [m.kbParse("610", b), m.kbParse("1F0", b), m.kbParse("12", b)], spread: m.kbSpreadCounts(b) }};
      }}
      console.log(JSON.stringify(out));""")
    for b in range(2, 17):
        r = got[str(b)]
        assert r["att"] == attractor_b(b) and r["text"] == q0012.text(attractor_b(b)[0], b)
        assert r["parse"] == [6 * b * b + b if b >= 7 else None, 496 if b == 16 else None, None]
        for x in range(b ** 3):
            assert r["chains"][x] == chain_b(x, b)
            diff, d, d_next, digits = r["steps"][x]
            assert diff == step_b(x, b) and d == q0012.spread(x, b)
            assert d_next == (max(b - d, d - 1) if d else 0) and digits == ([d - 1, b - 1, b - d] if d else [0, 0, 0])
        hist = q0012.chain_lengths(b)
        assert r["hist"]["hist"] == [hist.get(k, 0) for k in range(max(hist) + 1)]
        assert r["hist"]["zeros"] == b
        # the step line: every number with d gives the same difference, 6d(b - d) of them (b for d = 0)
        assert r["spread"] == [sum(1 for x in range(b ** 3) if q0012.spread(x, b) == d) for d in range(b)]
        assert r["spread"] == [b] + [6 * d * (b - d) for d in range(1, b)]
