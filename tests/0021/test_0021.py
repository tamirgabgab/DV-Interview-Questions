"""Question 0021 has no code on the page; these tests check every number of the page (the
four counts, the recursion table, the counts by number of completions, the closed form,
the delta exception, the special cases and the numeric sweep) against independent
references, and that the figures and tables are the generator's output."""

import re
import subprocess
import sys
from itertools import combinations

from extract_code import ROOT, question_path

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0021 as q  # noqa: E402


def enumerate_splits(addr, length, mps, rcb):
    """Independent reference: every subset of the interior boundaries, kept when no
    completion is longer than MPS. Returns a set of size tuples."""
    end = addr + length
    bounds = list(range((addr // rcb + 1) * rcb, end, rcb))
    out = set()
    for k in range(len(bounds) + 1):
        for sub in combinations(bounds, k):
            pts = [addr, *sub, end]
            sizes = tuple(b - a for a, b in zip(pts, pts[1:]))
            if max(sizes) <= mps:
                out.add(sizes)
    return out


def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def test_page_counts():
    expect = {"a1": 8, "a2": 16, "b1": 108, "b2": 208}
    for key, (addr, length) in q.CASES.items():
        full = enumerate_splits(addr, length, q.MPS, q.RCB)
        assert len(full) == expect[key] == q.count(addr, length, q.MPS, q.RCB) == q.formula(addr, length, q.MPS, q.RCB)
        assert {tuple(s) for s in q.splits(addr, length, q.MPS, q.RCB)} == full
    assert q.blocks(0x1000, 256, 64) == [64] * 4
    assert q.blocks(0x1010, 256, 64) == [48, 64, 64, 64, 16]
    assert q.blocks(0x1010, 512, 64) == [48] + [64] * 7 + [16]
    assert q.delta(0x1010, 256, 256, 64) == 1 and q.delta(0x1000, 256, 256, 64) == 0
    # the delta example of the proof: 0x1020, 128 bytes, MPS = 128
    assert enumerate_splits(*q.DELTA_CASE) == {(128,), (96, 32), (32, 96), (32, 64, 32)}
    assert q.formula(*q.DELTA_CASE) == 4 and q.delta(*q.DELTA_CASE) == 1


def test_recursion_and_closed_form():
    assert [q.compositions(n, 4) for n in range(10)] == [1, 1, 2, 4, 8, 15, 29, 56, 108, 208]
    assert [q.S(n, 4) for n in range(11)] == [1, 2, 4, 8, 16, 31, 60, 116, 224, 432, 833]
    for m in (1, 2, 3, 4, 8):
        for n in range(0, 16):
            assert q.S(n, m) - q.S(n - 1, m) == q.compositions(n, m), (m, n)
    # special cases: one block per completion, Fibonacci, no bound
    for n in range(1, 12):
        assert q.compositions(n, 1) == 1
        assert q.compositions(n, 2) == fib(n + 1)
        assert q.compositions(n, n) == q.compositions(n, n + 3) == 2 ** (n - 1)


def test_count_by_completions():
    # T(N, k) against the enumeration, grouped by the number of completions
    for key in ("b1", "b2"):
        addr, length = q.CASES[key]
        N = len(q.blocks(addr, length, q.RCB))
        by_k = {}
        for s in enumerate_splits(addr, length, q.MPS, q.RCB):
            by_k[len(s)] = by_k.get(len(s), 0) + 1
        assert {k: q.T(N, k, 4) for k in by_k} == by_k
        assert sum(by_k.values()) == q.compositions(N, 4)
    assert {k: q.T(8, k, 4) for k in range(2, 9)} == {2: 1, 3: 12, 4: 31, 5: 35, 6: 21, 7: 7, 8: 1}
    assert {k: q.T(9, k, 4) for k in range(3, 10)} == {3: 10, 4: 40, 5: 65, 6: 56, 7: 28, 8: 8, 9: 1}
    assert q.T(8, 3, 4) == 12                       # the worked example on the page: 21 - 9
    avg = sum(k * q.T(8, k, 4) for k in range(2, 9)) / q.compositions(8, 4)
    assert abs(avg - 4.8) < 0.05                    # the follow-up: about 4.8 completions
    # the follow-up with RCB = 128 (m = 2): 2, 4, 5, 8
    assert [q.formula(a, n, 256, 128) for a, n in q.CASES.values()] == [2, 4, 5, 8]
    assert [q.count(a, n, 256, 128) for a, n in q.CASES.values()] == [2, 4, 5, 8]


def test_formula_against_random_enumeration():
    import random
    rng = random.Random(21)
    for _ in range(400):
        rcb = rng.choice([64, 128])
        mps = rng.choice([m for m in (128, 256, 512, 1024) if m >= rcb])
        length = rng.randrange(4, 1025, 4)
        addr = rng.randrange(0, 4096 - length + 1, 4)
        if (addr + length - 1) // rcb - addr // rcb > 14:
            continue                                # keep the subset enumeration small
        full = enumerate_splits(addr, length, mps, rcb)
        assert len(full) == q.count(addr, length, mps, rcb) == q.formula(addr, length, mps, rcb), (addr, length, mps, rcb)


def test_numeric_sweep():
    # The sweep quoted on the page: every DW offset, every DW length up to 1596, 0 mismatches
    cases = 0
    for rcb in (64, 128):
        for mps in (128, 256, 512, 1024):
            for a in range(0, rcb, 4):
                for length in range(4, 1597, 4):
                    assert q.count(a, length, mps, rcb) == q.formula(a, length, mps, rcb), (a, length, mps, rcb)
                    cases += 1
    assert cases == 76608


def test_figures_up_to_date():
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0021.py")],
                         capture_output=True, text=True, check=True).stdout
    text = question_path(21).read_text(encoding="utf-8")
    for pattern in (r'<svg class="figure cs-fig".*?</svg>', r'<span class="viz-legend">.*?</span></span>'):
        generated = re.findall(pattern, out)
        assert generated and re.findall(pattern, text) == generated, pattern
    flat = "\n".join(line.strip() for line in text.splitlines())
    for table_start in ("| ‏\\( N \\) | החישוב |", "| מספר Completions ‏\\( k \\) | ‏\\( T(8, k) \\) |",
                        "| מספר Completions ‏\\( k \\) | ‏\\( T(9, k) \\) |", "| ‏\\( n \\) | האיברים של",
                        "| הבקשה | ‏\\( a \\) |"):
        block = out[out.index(table_start):]
        block = block[:block.index("\n\n")]
        assert "\n".join(line.strip() for line in block.splitlines()) in flat, table_start
