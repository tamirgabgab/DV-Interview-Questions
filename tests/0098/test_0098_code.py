"""Question 0098: the page's Python code (luhn_sum, luhn_valid, check_digit, missed_swaps,
israeli_id_valid, isbn10_valid, misses, no_perfect_weights, random_card, mutations), run as
published, against independent definitions and exhaustive enumerations."""

import random
from itertools import permutations

from extract_code import load_python

ns = load_python(98)
luhn_sum, luhn_valid, check_digit = ns["luhn_sum"], ns["luhn_valid"], ns["check_digit"]
missed_swaps, misses, no_perfect_weights = ns["missed_swaps"], ns["misses"], ns["no_perfect_weights"]
israeli_id_valid, isbn10_valid = ns["israeli_id_valid"], ns["isbn10_valid"]
random_card, mutations = ns["random_card"], ns["mutations"]

TEST_CARDS = ["4111111111111111", "4012888888881881", "5555555555554444", "378282246310005",
              "6011111111111117", "4242424242424242", "4111111111109115"]


def ref_sum(number):
    """Luhn by the textbook: from the right, double every second digit and add the digits of
    the product."""
    total = 0
    for i, c in enumerate(reversed(number)):
        d = int(c) * (2 if i % 2 else 1)
        total += d // 10 + d % 10
    return total


def test_luhn_on_the_test_numbers():
    for n in TEST_CARDS:
        assert luhn_valid(n) and luhn_sum(n) == ref_sum(n)
    assert luhn_sum("4111111111111111") == 30 and luhn_sum("4111111111111112") == 31
    assert luhn_sum("4111 1111 1111 1111") == 30 and luhn_valid("4111-1111-1111-1111")
    assert not luhn_valid("4111111111111112")
    assert luhn_sum("4111111111109115") == 40


def test_against_the_reference_on_random_numbers():
    rng = random.Random(98)
    for _ in range(3000):
        n = "".join(rng.choice("0123456789") for _ in range(rng.randint(1, 19)))
        assert luhn_sum(n) == ref_sum(n)


def test_check_digit_is_the_only_completion():
    rng = random.Random(1)
    for _ in range(500):
        body = "".join(rng.choice("0123456789") for _ in range(rng.randint(1, 18)))
        good = [d for d in range(10) if luhn_valid(body + str(d))]
        assert good == [check_digit(body)]
    assert check_digit("411111111111111") == 1 and luhn_sum("4111111111111110") == 29


def test_every_single_error_is_caught():
    rng = random.Random(2)
    for _ in range(300):
        n = random_card(True, rng, rng.randint(2, 19))
        for kind, i, m in mutations(n):
            if kind == "single":
                assert not luhn_valid(m), (n, i, m)


def test_the_only_slipping_swap_is_0_9():
    assert missed_swaps() == [(0, 9)]
    rng = random.Random(3)
    for _ in range(300):
        n = random_card(True, rng)
        for kind, i, m in mutations(n):
            if kind == "swap":
                assert luhn_valid(m) == ({n[i], n[i + 1]} == {"0", "9"}), (n, i, m)
    swaps = [m for kind, _, m in mutations("4111111111109115") if kind == "swap"]
    assert [m for m in swaps if luhn_valid(m)] == ["4111111111190115"]


def test_twin_and_jump_errors_of_the_follow_ups():
    D = [2 * d - 9 if d > 4 else 2 * d for d in range(10)]
    twins = [(a, b) for a in range(10) for b in range(a + 1, 10) if (a + D[a] - b - D[b]) % 10 == 0]
    assert twins == [(2, 5), (3, 6), (4, 7)]
    # a jump swap abc -> cba never changes the Luhn sum
    rng = random.Random(4)
    for _ in range(200):
        n = random_card(True, rng)
        i = rng.randrange(14)
        m = n[:i] + n[i + 2] + n[i + 1] + n[i] + n[i + 3:]
        assert luhn_valid(m)


def test_israeli_id_is_luhn():
    assert israeli_id_valid("000000018") and not israeli_id_valid("000000019")
    assert israeli_id_valid("18") and israeli_id_valid(" 000000018 ")
    assert not israeli_id_valid("1234567890") and not israeli_id_valid("12a")
    rng = random.Random(5)
    for _ in range(3000):
        s = "".join(rng.choice("0123456789") for _ in range(9))
        assert israeli_id_valid(s) == luhn_valid(s)
    # the sum of the example: 1 * 2 + 8 = 10, and with 9 at the end 11
    assert luhn_sum("000000018") == 10 and luhn_sum("000000019") == 11


def isbn_sum(s):
    v = [10 if c == "X" else int(c) for c in s]
    return sum((10 - i) * x for i, x in enumerate(v))


def test_isbn():
    assert isbn10_valid("0-306-40615-2") and isbn10_valid("0306406152") and isbn_sum("0306406152") == 132
    assert isbn10_valid("0-8044-2957-X") and isbn10_valid("080442957x")
    assert not isbn10_valid("0306406153") and not isbn10_valid("030640615") and not isbn10_valid("X306406152")
    # the products of the page's figure
    assert [(10 - i) * int(c) for i, c in enumerate("0306406152")] == [0, 27, 0, 42, 24, 0, 24, 3, 10, 2]


def test_isbn_catches_every_single_error_and_every_swap():
    for isbn in ("0306406152", "080442957X"):
        chars = list(isbn)
        alphabet = "0123456789"
        for i in range(10):
            for b in alphabet + ("X" if i == 9 else ""):
                if b != chars[i]:
                    m = chars[:]
                    m[i] = b
                    assert isbn_sum("".join(m)) % 11 != 0
        for i in range(10):
            for j in range(i + 1, 10):
                if chars[i] != chars[j] and "X" not in (chars[i], chars[j]):
                    m = chars[:]
                    m[i], m[j] = m[j], m[i]
                    assert isbn_sum("".join(m)) % 11 != 0
    # in general: every weight pair and every digit pair
    for wi in range(1, 11):
        for wj in range(1, 11):
            for a in range(11):
                for b in range(11):
                    if a != b:
                        assert (wi * (b - a)) % 11 != 0
                        if wi != wj:
                            assert ((wi - wj) * (b - a)) % 11 != 0


def test_the_schemes_of_part_c():
    D = lambda d: 2 * d - 9 if d > 4 else 2 * d  # noqa: E731
    s, w = misses(lambda d: d, D)
    assert s == [] and w == [(0, 9)]
    s, w = misses(lambda d: d, lambda d: 2 * d)
    assert len(s) == 10 and all(abs(a - b) == 5 for a, b in s) and w == []
    s, w = misses(lambda d: d, lambda d: 3 * d)
    assert s == [] and w == [(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)]
    s, w = misses(lambda d: d, lambda d: 2 * d, 11)
    assert s == [] and w == []
    assert no_perfect_weights()


def test_no_permutation_scheme_mod_10_catches_every_swap():
    # WLOG the second place adds d itself (relabel the digits); then the first place's sigma
    # would need sigma(d) - d to be a permutation of the residues: none exists mod 10
    def complete(n):
        found = []

        def go(d, used, diffs, sigma):
            if d == n:
                found.append(tuple(sigma))
                return True
            for v in range(n):
                if v not in used and (v - d) % n not in diffs:
                    used.add(v)
                    diffs.add((v - d) % n)
                    sigma.append(v)
                    if go(d + 1, used, diffs, sigma):
                        return True
                    sigma.pop()
                    used.discard(v)
                    diffs.discard((v - d) % n)
            return False

        go(0, set(), set(), [])
        return found

    assert complete(10) == []
    assert complete(11)          # mod 11 such a map exists (2d is one)
    assert sorted((2 * d - d) % 11 for d in range(11)) == list(range(11))
    # the sum argument: 0 + ... + 9 = 45 = 5 mod 10, but sum(sigma) - sum(d) = 0
    assert sum(range(10)) % 10 == 5 and sum(range(11)) % 11 == 0
    # a brute check on a smaller even modulus agrees
    assert not any(sorted((p[d] - d) % 6 for d in range(6)) == list(range(6)) for p in permutations(range(6)))


def test_random_card_and_mutations():
    rng = random.Random(6)
    for _ in range(2000):
        v = rng.random() < 0.5
        n = random_card(v, rng)
        assert len(n) == 16 and n.isdigit() and luhn_valid(n) == v
    muts = mutations("4111111111111111")
    assert sum(1 for k, _, _ in muts if k == "single") == 144
    assert [i for k, i, _ in muts if k == "swap"] == [0]
    muts = mutations("4111111111109115")
    assert [i for k, i, _ in muts if k == "swap"] == [0, 10, 11, 12, 14]


def test_no_digits_and_digit_like_characters():
    # an empty number is not valid, though its sum is 0
    for n in ("", " ", "abc", "-"):
        assert luhn_sum(n) == 0 and not luhn_valid(n)
    # str.isdigit accepts characters that int() refuses: they are skipped or rejected, not raised on
    assert luhn_sum("41\u00b2") == luhn_sum("41") and luhn_valid("4111 1111 1111 1111\u00b2")
    assert not israeli_id_valid("12345678\u00b2") and not israeli_id_valid("\u0661" * 9)
    assert not isbn10_valid("030640615\u00b2") and not isbn10_valid("03064061\u00b22")
    assert israeli_id_valid("18") and isbn10_valid("0306406152") and isbn10_valid("080442957x")
