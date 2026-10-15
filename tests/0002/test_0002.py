from extract_code import load_python

ns = load_python(2)
SWAPS = [ns["swap_temp"], ns["swap_arith"], ns["swap_xor"]]
PAIRS = [(5, 3), (-7, 12), (2**31 - 1, 1), (0, 0), (-2**31, -1), (123456789, -987654321)]


def test_all_methods_swap():
    for swap in SWAPS:
        for a, b in PAIRS:
            v = [a, b]
            swap(v, 0, 1)
            assert v == [b, a], (swap.__name__, a, b)


def test_same_variable_pitfall():
    # Documented on the page: arithmetic and XOR versions zero the variable.
    for swap, expected in zip(SWAPS, [9, 0, 0]):
        v = [9]
        swap(v, 0, 0)
        assert v == [expected], swap.__name__
