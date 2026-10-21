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
