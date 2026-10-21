"""Question 0034: the page's Python code (bin2gray, gray2bin, fifo_empty, fifo_full, as
published): the conversions are inverse, every step changes one bit (the wrap included),
the page table, and the full / empty rules against the true occupancy, exhaustively."""

from extract_code import load_python

ns = load_python(34)
bin2gray, gray2bin = ns["bin2gray"], ns["gray2bin"]
fifo_empty, fifo_full = ns["fifo_empty"], ns["fifo_full"]


def test_conversions_inverse_and_one_bit_steps():
    for bits in (1, 2, 3, 4, 5, 8):
        size = 1 << bits
        for b in range(size):
            g = bin2gray(b)
            assert gray2bin(g, bits) == b
            assert bin(g ^ bin2gray((b + 1) % size)).count("1") == 1


def test_page_table():
    grays = [bin2gray(b) for b in range(16)]
    assert grays == [0b0000, 0b0001, 0b0011, 0b0010, 0b0110, 0b0111, 0b0101, 0b0100,
                     0b1100, 0b1101, 0b1111, 0b1110, 0b1010, 0b1011, 0b1001, 0b1000]
    changed = [(grays[b] ^ grays[(b + 1) % 16]).bit_length() - 1 for b in range(16)]
    assert changed == [0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 3]
    # the bit that changes is the number of trailing zeros of b + 1
    assert all(c == ((((b + 1) % 16) & -((b + 1) % 16)).bit_length() - 1 if (b + 1) % 16 else 3) for b, c in enumerate(changed))


def test_full_empty_exhaustive():
    for bits in (2, 3, 5, 7):
        size, half = 1 << bits, 1 << (bits - 1)
        for w in range(size):
            for r in range(size):
                occupancy = (w - r) % size
                assert fifo_empty(bin2gray(w), bin2gray(r)) == (occupancy == 0)
                assert fifo_full(bin2gray(w), bin2gray(r), bits) == (occupancy == half)


def test_page_example():
    assert bin2gray(7) == 0b0100 and bin2gray(8) == 0b1100
    assert bin2gray(23) == 0b11100 and bin2gray(7) == 0b00100
    assert fifo_full(bin2gray(23), bin2gray(7), 5) and not fifo_empty(bin2gray(23), bin2gray(7))
