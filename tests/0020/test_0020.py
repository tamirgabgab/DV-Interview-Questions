import random
import re
import subprocess
import sys
from itertools import combinations

from extract_code import ROOT, load_python, question_path

ns = load_python(20)
completion_splits = ns["completion_splits"]

ADDR, LEN, RCB, MPS = 0x1010, 256, 64, 256


def split_ok(addr, length, mps, rcb, split):
    """Independent check of one split against the rules as the page states them."""
    if sum(split) != length or any(s <= 0 for s in split):
        return False
    pos = addr
    for s in split[:-1]:
        pos += s
        if pos % rcb:                # every cut between two completions is on an RCB boundary
            return False
    return max(split) <= mps


def reference(addr, length, mps, rcb):
    """Independent enumeration: every subset of the boundaries inside the request, kept
    when no completion is larger than MPS. Returned as a set of tuples."""
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


def greedy_count(addr, length, mps, rcb):
    """Fewest completions: always end at the furthest reachable boundary (or the end)."""
    pos, end, n = addr, addr + length, 0
    while pos < end:
        reach = pos + mps
        pos = end if reach >= end else (reach // rcb) * rcb
        n += 1
    return n


def test_page_example():
    splits = completion_splits(ADDR, LEN, MPS, RCB)
    assert len(splits) == 16
    assert splits[0] == [256]
    assert splits[1] == [240, 16]
    assert splits[2] == [176, 80]
    assert splits[-1] == [48, 64, 64, 64, 16]
    assert sorted(len(s) for s in splits) == [1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5]
    # the same request with MPS = 128 keeps 8 of them, and RCB = 128 gives 4 / 1
    assert len(completion_splits(ADDR, LEN, 128, RCB)) == 8
    assert completion_splits(ADDR, LEN, 256, 128) == [[256], [240, 16], [112, 144], [112, 128, 16]]
    assert completion_splits(ADDR, LEN, 128, 128) == [[112, 128, 16]]
    # aligned request: 2^3 subsets of three boundaries, [128, 128] with MPS = 128 among them
    assert len(completion_splits(0x1000, 256, 256, 64)) == 8
    assert completion_splits(0x1000, 256, 128, 64)[0] == [128, 128]
    # traps from the page
    assert [144, 64, 48] not in completion_splits(ADDR, LEN, MPS, RCB)
    assert [128, 128] not in completion_splits(ADDR, LEN, 128, RCB)


def test_matches_reference_and_rules():
    rng = random.Random(20)
    for _ in range(600):
        rcb = rng.choice([64, 128])
        mps = rng.choice([m for m in (128, 256, 512, 1024) if m >= rcb])
        length = rng.choice([4, 8, 16, 32, 64, 96, 128, 192, 256, 384, 512, 768, 1024])
        addr = rng.randrange(0, 4096 - length + 1, 4)           # inside one 4 KB page
        splits = completion_splits(addr, length, mps, rcb)
        assert all(split_ok(addr, length, mps, rcb, s) for s in splits), (addr, length, mps, rcb)
        as_tuples = [tuple(s) for s in splits]
        assert len(set(as_tuples)) == len(as_tuples)              # each split exactly once
        assert set(as_tuples) == reference(addr, length, mps, rcb), (addr, length, mps, rcb)


def test_order_and_counts():
    rng = random.Random(7)
    for _ in range(300):
        rcb = rng.choice([64, 128])
        mps = rng.choice([m for m in (128, 256, 512) if m >= rcb])
        length = rng.choice([16, 64, 128, 256, 512])
        addr = rng.randrange(0, 4096 - length + 1, 4)
        splits = completion_splits(addr, length, mps, rcb)
        end = addr + length
        c = (end - 1) // rcb - addr // rcb                        # boundaries inside the request
        assert len(splits[0]) == greedy_count(addr, length, mps, rcb)
        assert len(splits[-1]) == c + 1                           # a cut on every boundary
        if mps >= length:
            assert len(splits) == 2 ** c
        # every split is non-empty; the first and the last of each split follow the rules
        for s in splits:
            assert (addr + s[0]) % rcb == 0 or len(s) == 1
            assert all(m % rcb == 0 for m in s[1:-1])


def test_figures_up_to_date():
    # The figures and tables on the page are the output of tools/figures/q0020.py
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0020.py")],
                         capture_output=True, text=True, check=True).stdout
    text = question_path(20).read_text(encoding="utf-8")
    for pattern in (r'<svg class="figure cs-fig".*?</svg>', r'<span class="viz-legend">.*?</span></span>'):
        generated = re.findall(pattern, out)
        assert generated and re.findall(pattern, text) == generated, pattern
    for table_start in ("| מספר Completions | כמה פיצולים |", "| הפיצול | ה-Completion הגדול ביותר |"):
        block = out[out.index(table_start):]
        block = block[:block.index("\n\n")]
        assert "\n".join(line.strip() for line in block.splitlines()) in \
            "\n".join(line.strip() for line in text.splitlines()), table_start


def test_explorer_matches_page_code():
    """The JavaScript enumeration (docs/javascripts/explorer/pcie.js) returns the page's splits,
    in the page's order, on random requests."""
    from page_tests import explorer_require, node_json

    splits = load_python(20)["completion_splits"]
    rng = random.Random(20)
    cases = []
    for _ in range(60):
        rcb = rng.choice([64, 128])
        mps = rng.choice([128, 256, 512, 1024])
        if mps < rcb:
            continue
        addr = 0x1000 + rng.randrange(0, 512, 4)
        length = rng.randrange(4, 600, 4)
        cases.append((addr, length, mps, rcb))
    cases.append((0x1010, 256, 256, 64))
    cases.append((0x1010, 256, 128, 64))
    got = node_json(f"""
      const m = {explorer_require()};
      const cases = {[list(c) for c in cases]};
      console.log(JSON.stringify(cases.map(([a, l, mps, rcb]) => m.pcieSplits(a, l, mps, rcb))));
    """)
    for (addr, length, mps, rcb), js in zip(cases, got):
        assert js == splits(addr, length, mps, rcb), (addr, length, mps, rcb)
