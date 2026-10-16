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
