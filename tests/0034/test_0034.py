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


def test_explorer_widths():
    """The width selects of the two boxes: the sampled step on every value of 3 to 6 bits
    (every subset of arrived bits for the wrap step, where all bits change) against the
    page's conversions, and the flags of a FIFO of 8, 32 and 64 entries (pointers one bit
    wider) on every pointer pair against the page's fifo_empty / fifo_full."""
    import itertools
    import json

    from page_tests import explorer_require, node_json

    sizes = [8, 32, 64]
    got = node_json(f"""
      const m = {explorer_require()};
      const wraps = {{}}, flags = {{}};
      for (const bits of [3, 4, 5, 6]) {{
        const b = (1 << bits) - 1, out = [];
        for (let s = 0; s < (1 << bits); s++) {{ const arr = {{}}; for (let i = 0; i < bits; i++) arr[i] = (s >> i) & 1; out.push(m.graySample(b, bits, arr, arr)); }}
        wraps[bits] = out;
      }}
      for (const size of {json.dumps(sizes)}) {{
        const bits = Math.log2(size) + 1, out = [];
        for (let w = 0; w < 2 * size; w++) for (let r = 0; r < 2 * size; r++) out.push(m.grayFlags(w, r, bits));
        flags[size] = out;
      }}
      console.log(JSON.stringify({{ wraps, flags }}));""")
    for bits in (3, 4, 5, 6):
        b, size = (1 << bits) - 1, 1 << bits
        for s, sm in enumerate(got["wraps"][str(bits)]):
            assert sm["changedBin"] == list(range(bits)) and sm["changedGray"] == [bits - 1]
            seen = sum(((0 if s >> i & 1 else 1) << i) for i in range(bits))   # old bit 1 unless the new 0 arrived
            assert sm["seenBin"] == seen and sm["binValid"] == (s in (0, size - 1))
            assert sm["seenGrayAsBin"] in (b, 0) and sm["wrongCount"] == size - 2
    for size in sizes:
        bits = size.bit_length()                                   # log2(size) + 1
        for (w, r), fl in zip(itertools.product(range(2 * size), range(2 * size)), got["flags"][str(size)]):
            assert fl["empty"] == fifo_empty(bin2gray(w), bin2gray(r)) == ((w - r) % (2 * size) == 0)
            assert fl["full"] == fifo_full(bin2gray(w), bin2gray(r), bits) == ((w - r) % (2 * size) == size)
            assert fl["occupancy"] == (w - r) % (2 * size)


def test_explorer_flag_strip():
    """The timing strip of the FIFO box (X145): one column per write or read that the
    FIFO accepts (a write when full and a read when empty are refused, so a burst stops
    early), the pointers after it and the flags by the page's fifo_full / fifo_empty."""
    import json
    import random

    from page_tests import explorer_require, node_json

    rng = random.Random(34)
    runs = []
    for size in (8, 16, 32, 64):
        ops = []
        for _ in range(60):
            ops += [rng.choice("wr")] * rng.choice([1, 1, 2, size // 2])
        runs.append((size, ops))
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(runs)}.map(([size, ops]) => m.grayFlagsOps(ops, size))));""")
    for (size, ops), cols in zip(runs, got):
        bits, w, r = size.bit_length(), 0, 0
        want = [(None, 0, 0)]
        for op in ops:
            occ = (w - r) % (2 * size)
            if op == "w" and occ < size:
                w = (w + 1) % (2 * size)
                want.append(("w", w, r))
            elif op == "r" and occ > 0:
                r = (r + 1) % (2 * size)
                want.append(("r", w, r))
        assert [(c["op"], c["w"], c["r"]) for c in cols] == want
        for c in cols:
            assert c["wg"] == bin2gray(c["w"]) and c["rg"] == bin2gray(c["r"])
            assert c["full"] == fifo_full(c["wg"], c["rg"], bits) and c["empty"] == fifo_empty(c["wg"], c["rg"])
        assert any(c["full"] for c in cols) and any(c["empty"] for c in cols[1:])
