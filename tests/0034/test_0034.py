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


def test_explorer_matches_page_code():
    """The Gray explorer: its conversions and flags against the page's functions on every
    5-bit value and every pointer pair; its sampled step b -> b + 1 on every 4-bit value
    and every subset of arrived bits."""
    import itertools
    import json

    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      const conv = [], flags = [], samples = [];
      for (let v = 0; v < 32; v++) conv.push([m.grayOf(v), m.grayToBin(m.grayOf(v), 5)]);
      for (let w = 0; w < 32; w++) for (let r = 0; r < 32; r++) flags.push(m.grayFlags(w, r, 5));
      for (let b = 0; b < 16; b++) for (let s = 0; s < 16; s++) {{
        const arr = {{}}; for (let i = 0; i < 4; i++) arr[i] = (s >> i) & 1;
        samples.push(m.graySample(b, 4, arr, arr));
      }}
      console.log(JSON.stringify({{ conv, flags, samples }}));""")
    for v, (g, back) in enumerate(got["conv"]):
        assert g == bin2gray(v) and back == v and gray2bin(g, 5) == v
    for (w, r), fl in zip(itertools.product(range(32), range(32)), got["flags"]):
        assert fl["empty"] == fifo_empty(bin2gray(w), bin2gray(r))
        assert fl["full"] == fifo_full(bin2gray(w), bin2gray(r), 5)
        assert fl["occupancy"] == (w - r) % 32
    for (b, s), sm in zip(itertools.product(range(16), range(16)), got["samples"]):
        nb = (b + 1) % 16
        changed = [i for i in range(4) if (b ^ nb) >> i & 1]
        assert sm["changedBin"] == changed
        assert sm["changedGray"] == [(bin2gray(b) ^ bin2gray(nb)).bit_length() - 1]
        seen = b
        for i in changed:
            if s >> i & 1:
                seen = (seen & ~(1 << i)) | (nb & (1 << i))
        arrived = [s >> i & 1 for i in changed]
        assert sm["seenBin"] == seen
        assert sm["binValid"] == (seen in (b, nb)) == (all(arrived) or not any(arrived))
        assert sm["seenGray"] in (bin2gray(b), bin2gray(nb)) and sm["seenGrayAsBin"] in (b, nb)
        assert sm["wrongCount"] == 2 ** len(changed) - 2
