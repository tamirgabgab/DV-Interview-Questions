from extract_code import load_python

ns = load_python(13)
is_special, find_special = ns["is_special_4"], ns["find_special_4"]


def digits_sorted(x):
    """The four digits of x (with leading zeros), largest first."""
    return sorted([x // 1000, x // 100 % 10, x // 10 % 10, x % 10], reverse=True)


def step(x):
    a, b, c, d = digits_sorted(x)
    return (1000 * a + 100 * b + 10 * c + d) - (1000 * d + 100 * c + 10 * b + a)


def test_page_examples():
    assert step(3524) == 3087 and step(95) == 9441 and step(1000) == 999 and step(7777) == 0
    for x in (3524, 95, 1000, 7777, 9441, 495):
        assert is_special(x) == 0, x
    assert is_special(0) == 1
    assert is_special(6174) == 1


def test_matches_definition():
    for x in range(10000):
        assert is_special(x) == int(step(x) == x), x


def test_final_array():
    assert find_special() == [0, 6174]


def test_proof_steps():
    # Step 1: the difference is 999p + 90q with 0 <= q <= p <= 9 (55 values)
    for x in range(10000):
        a, b, c, d = digits_sorted(x)
        assert step(x) == 999 * (a - d) + 90 * (b - c)
    # Step 3: the digits of the difference from the column subtraction
    for p in range(1, 10):
        for q in range(p + 1):
            expected = [p, q - 1, 9 - q, 10 - p] if q >= 1 else [p - 1, 9, 9, 10 - p]
            assert [int(ch) for ch in f"{999 * p + 90 * q:04d}"] == expected, (p, q)
    # Steps 4-7: among the 55 candidates only 0 (p = 0) and 6174 (p = 6, q = 2) are fixed
    fixed = [(p, q) for p in range(10) for q in range(p + 1)
             if step(999 * p + 90 * q) == 999 * p + 90 * q]
    assert fixed == [(0, 0), (6, 2)]


def test_follow_up_steps():
    # Every number without four equal digits reaches 6174 in at most 7 steps
    counts = [0] * 8
    for x in range(10000):
        if len(set(f"{x:04d}")) == 1:
            continue
        n = 0
        while x != 6174:
            x, n = step(x), n + 1
        counts[n] += 1
    assert counts == [1, 383, 576, 2400, 1272, 1518, 1656, 2184]
