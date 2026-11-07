"""Question 0098: check digits (Luhn, the Israeli ID, ISBN-10).

Every number the page states is recomputed (the sums, the check digit, the tables of the
figures, the counts of the schemes, the follow-ups); the generator agrees with the page's
code; the generated blocks are up to date; and the luhn box's models are compared under
Node with the page's code."""

import re
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0098  # noqa: E402

ns = load_python(98)
PAGE = (ROOT / "docs" / "questions" / "junior" / "0098-luhn-check-digit.md").read_text(encoding="utf-8")
TEXT = re.sub(r"\s+", " ", PAGE)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(98)


def test_generator_matches_the_page_code():
    for n in ("4111111111111111", "4111111111109115", "378282246310005", "000000018"):
        assert q0098.luhn_sum(n) == ns["luhn_sum"](n)
    assert [q0098.doubled(d) for d in range(10)] == [0, 2, 4, 6, 8, 1, 3, 5, 7, 9]
    for key, _ in q0098.SCHEMES:
        f, g, m = q0098.scheme_maps()[key]
        assert (q0098.single_misses(key), q0098.swap_misses(key)) == ns["misses"](f, g, m)
    assert q0098.swap_misses("luhn") == ns["missed_swaps"]() == [(0, 9)]


def test_part_a_numbers():
    assert ns["luhn_sum"]("4111111111111111") == 30 and "\\( 8 + 7 \\cdot 2 + 8 = 30 \\)" in PAGE
    assert ns["luhn_sum"]("4111111111111112") == 31 and "הוא 31" in TEXT
    assert ns["luhn_sum"]("4111111111111110") == 29 and "הוא 29" in TEXT
    assert ns["check_digit"]("411111111111111") == 1 and "הספרה החסרה היא 1" in TEXT
    # the doubled digits of 5 to 9
    assert [q0098.doubled(d) for d in range(5, 10)] == [1, 3, 5, 7, 9] and "היא 1, 3, 5, 7, 9" in TEXT
    # D(d) - d mod 10, and the one collision
    assert [(q0098.doubled(d) - d) % 10 for d in range(10)] == [0, 1, 2, 3, 4, 6, 7, 8, 9, 0]
    assert "\\( 0, 1, 2, 3, 4, 6, 7, 8, 9, 0 \\)" in PAGE
    # the 0 / 9 example
    assert ns["luhn_sum"]("4111111111109115") == 40 and ns["luhn_valid"]("4111111111190115")
    assert "4111 1111 1110 9115" in PAGE and "4111 1111 1119 0115" in PAGE
    # counting from the left gives 27 (the trap)
    wrong = sum(q0098.doubled(int(c)) if i % 2 == 1 else int(c) for i, c in enumerate("4111111111111111"))
    assert wrong == 27 and "נותן 27 ולא 30" in TEXT
    # 45 pairs of different digits, 144 single changes of 16 digits
    assert 10 * 9 // 2 == 45 and 16 * 9 == 144 and "כל 144 הטעויות" in TEXT


def test_part_b_numbers():
    assert ns["israeli_id_valid"]("000000018") and not ns["israeli_id_valid"]("000000019")
    assert "\\( 1 \\cdot 2 + 8 = 10 \\)" in PAGE and "הסכום 11" in TEXT
    terms = q0098.isbn_terms("0306406152")
    assert [p for _, _, p in terms] == [0, 27, 0, 42, 24, 0, 24, 3, 10, 2]
    assert sum(p for _, _, p in terms) == 132 == 12 * 11 and "132 = 12 \\cdot 11" in PAGE
    assert ns["isbn10_valid"]("0-8044-2957-X") and "0-8044-2957-X" in PAGE
    assert 10 * sum(range(1, 11)) == 550 and "10 \\cdot 55 = 550" in PAGE


def test_part_c_numbers():
    table = q0098.scheme_table()
    assert len(q0098.single_misses("w12")) == 10 and "10 מתוך 90" in table
    assert len(q0098.swap_misses("ean")) == 5 and "5 מתוך 45" in table
    assert q0098.swap_misses("ean")[1] == (1, 6) and "למשל 1 ו-6" in TEXT
    assert q0098.single_misses("isbn") == q0098.swap_misses("isbn") == []
    assert sum(range(10)) == 45 and 45 % 10 == 5 and sum(range(11)) == 55 and 55 % 11 == 0
    assert ns["no_perfect_weights"]()


def test_follow_ups():
    D = q0098.doubled
    twins = [(a, b) for a in range(10) for b in range(a + 1, 10) if (a + D(a) - b - D(b)) % 10 == 0]
    assert twins == [(2, 5), (3, 6), (4, 7)]
    assert "22 ↔ 55" in PAGE and "33 ↔ 66" in PAGE and "44 ↔ 77" in PAGE
    # 3d up to 4 and 3d - 9 from 5
    assert all(d + D(d) == (3 * d if d <= 4 else 3 * d - 9) for d in range(10))


def test_explorer_matches_the_page_code():
    from page_tests import explorer_require, node_json

    numbers = ["4111111111111111", "4111111111111112", "4012888888881881", "378282246310005",
               "4111111111109115", "000000018", "7", "12", "9999999999999999995"]
    got = node_json(f"const m = {explorer_require()};"
                    f"const ns = {numbers};"
                    "const kinds = ['swap', 'single'], schemes = ['luhn', 'w12', 'ean', 'isbn'];"
                    "console.log(JSON.stringify({"
                    "sums: ns.map((n) => m.luSum(m.luDigits(n))),"
                    "valid: ns.map((n) => m.luValid(m.luDigits(n))),"
                    "check: ns.filter((n) => n.length > 1).map((n) => m.luCheck(m.luDigits(n.slice(0, -1)))),"
                    "spaced: m.luSum(m.luDigits('4111 1111-1111 1111')), bad: [m.luDigits('41a1'), m.luDigits('')],"
                    "maps: schemes.map((s) => kinds.map((k) => m.luMap(s, k))),"
                    "single: m.luMutate([4, 1, 9], 'single', 2), swap: m.luMutate([4, 1, 9], 'swap', 0),"
                    "}));")
    for n, s, v in zip(numbers, got["sums"], got["valid"]):
        assert s == ns["luhn_sum"](n) and v == ns["luhn_valid"](n)
    assert got["check"] == [ns["check_digit"](n[:-1]) for n in numbers if len(n) > 1]
    assert got["spaced"] == 30 and got["bad"] == [None, None]
    assert got["single"] == [4, 1, 0] and got["swap"] == [1, 4, 9]
    for (key, _), by_kind in zip([("luhn", "")] + [(k, "") for k in ("w12", "ean", "isbn")], got["maps"]):
        f, g, m = q0098.scheme_maps()[key]
        singles, swaps = ns["misses"](f, g, m)
        swap_map, single_map = by_kind
        assert {(a, b) for a in range(10) for b in range(a + 1, 10) if swap_map[a][b] == "miss"} == set(swaps)
        assert all(swap_map[a][b] == swap_map[b][a] for a in range(10) for b in range(10))
        # the single map is the change in a doubled place only
        assert {(a, b) for a in range(10) for b in range(10) if single_map[a][b] == "miss"} == \
            {(a, b) for a in range(10) for b in range(10) if a != b and (g(a) - g(b)) % m == 0}
        assert all(swap_map[a][a] == single_map[a][a] == "same" for a in range(10))
