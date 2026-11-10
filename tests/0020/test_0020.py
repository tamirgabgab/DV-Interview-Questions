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


def test_explorer_cuts_by_hand():
    """The box's hand-made split: every subset of the inner boundaries gives the completions
    between the cuts, valid exactly when the page's rules accept them, so the valid subsets
    are the page's splits (the count of the box)."""
    import json

    from page_tests import explorer_require, node_json

    cases = [(0x1010, 256, 256, 64), (0x1010, 256, 128, 64), (0x1000, 512, 256, 64), (0x1020, 128, 128, 64), (0x1004, 300, 128, 128)]
    jobs = []
    for addr, length, mps, rcb in cases:
        bounds = list(range((addr // rcb + 1) * rcb, addr + length, rcb))
        for k in range(len(bounds) + 1):
            for sub in combinations(bounds, k):
                jobs.append([addr, length, mps, rcb, list(sub)])
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(jobs)}.map(([a, l, p, r, c]) => m.pcieSplitOf(a, l, p, r, c))));")
    valid = {}
    for (addr, length, mps, rcb, sub), out in zip(jobs, got):
        pts = [addr, *sub, addr + length]
        assert out["sizes"] == [b - a for a, b in zip(pts, pts[1:])]
        assert out["ok"] == split_ok(addr, length, mps, rcb, out["sizes"])
        if out["ok"]:
            valid.setdefault((addr, length, mps, rcb), set()).add(tuple(out["sizes"]))
    for case in cases:
        assert valid.get(case, set()) == reference(*case), case


def test_random_split_follow_up():
    """The follow-up on a uniform random split: a uniform choice at every step favours few
    completions ([256] comes out with 1/5, not 1/16), while choosing the cut with probability
    ways(cut) / ways(pos) gives every legal split exactly 1 / ways(addr)."""
    from fractions import Fraction as Fr

    def cuts_from(pos, end, mps, rcb):
        out = [end] if pos + mps >= end else []
        b = (pos // rcb + 1) * rcb
        while b < end and b <= pos + mps:
            out.append(b)
            b += rcb
        return out

    def ways(pos, end, mps, rcb):
        return 1 if pos == end else sum(ways(c, end, mps, rcb) for c in cuts_from(pos, end, mps, rcb))

    def probabilities(addr, length, mps, rcb, weighted):
        end, out = addr + length, {}

        def walk(pos, sizes, p):
            if pos == end:
                out[tuple(sizes)] = p
                return
            cuts = cuts_from(pos, end, mps, rcb)
            for c in cuts:
                q = Fr(ways(c, end, mps, rcb), ways(pos, end, mps, rcb)) if weighted else Fr(1, len(cuts))
                walk(c, sizes + [c - pos], p * q)

        walk(addr, [], Fr(1))
        return out

    naive = probabilities(ADDR, LEN, MPS, RCB, weighted=False)
    assert len(cuts_from(ADDR, ADDR + LEN, MPS, RCB)) == 5 and naive[(256,)] == Fr(1, 5)
    assert ways(ADDR, ADDR + LEN, MPS, RCB) == 16
    for addr, length, mps, rcb in [(ADDR, LEN, MPS, RCB), (ADDR, LEN, 128, RCB), (0x1004, 300, 128, 128), (0x1000, 512, 256, 64)]:
        fair = probabilities(addr, length, mps, rcb, weighted=True)
        total = ways(addr, length + addr, mps, rcb)
        assert set(fair) == reference(addr, length, mps, rcb)
        assert set(fair.values()) == {Fr(1, total)} and sum(fair.values()) == 1


def test_explorer_notation():
    """0020's box speaks the page's c (data-notation="c"); 0021's keeps N, |B| and delta."""
    page20 = question_path(20).read_text(encoding="utf-8")
    page21 = question_path(21).read_text(encoding="utf-8")
    assert re.search(r'data-kind="pcie" data-notation="c"', page20)
    assert 'data-kind="pcie" data-notation' not in page21
    js = (ROOT / "docs" / "javascripts" / "explorer" / "pcie.js").read_text(encoding="utf-8")
    assert 'box.dataset.notation === "c"' in js and "2^c = " in js


def min_completions(addr, length, mps, rcb):
    """The min/max follow-up's closed form: one completion when the end is within MPS,
    else the greedy first cut g, then full MPS steps from one boundary to the next."""
    end = addr + length                                           # the first byte after the request
    if addr + mps >= end:
        return 1
    g = (addr + mps) // rcb * rcb
    return 1 + -(-(end - g) // mps)


def test_min_completions_closed_form():
    """The closed form against the page's enumeration (the fewest completions of all its
    splits, which is splits[0]) on small requests, and against the box's dynamic program
    (pcieByCompletions: its first non-zero count) on requests up to 4 KB; the page's
    example and the counterexamples of the trap and of the case split."""
    from page_tests import explorer_require, node_json

    assert min_completions(ADDR, LEN, 128, RCB) == 3                 # g = 0x1080, 1 + ceil(144 / 128)
    assert (ADDR + 128) // RCB * RCB == 0x1080
    assert min_completions(0x1010, 128, 128, 64) == 1                # the formula alone would say 2
    assert 1 + -(-(0x1090 - 0x1080) // 128) == 2
    assert min_completions(0x1010, 512, 128, 64) == 5                # an unaligned request needing five
    rng = random.Random(2020)
    for _ in range(1500):
        rcb = rng.choice([64, 128])
        mps = rng.choice([m for m in (128, 256, 512) if m >= rcb])
        length = 4 * rng.randint(1, 160)
        addr = 4 * rng.randrange(0, 1 << 12)
        splits = completion_splits(addr, length, mps, rcb)
        assert min(map(len, splits)) == len(splits[0]) == min_completions(addr, length, mps, rcb), (addr, length, mps, rcb)
    cases = []
    for _ in range(3000):
        rcb = rng.choice([64, 128])
        mps = rng.choice([m for m in (128, 256, 512, 1024, 2048, 4096) if m >= rcb])
        length = 4 * rng.randint(1, 1024)
        cases.append((4 * rng.randrange(0, 1 << 20), length, mps, rcb))
    got = node_json(f"const m = {explorer_require()}; const cases = {[list(c) for c in cases]};"
                    "console.log(JSON.stringify(cases.map(([a, l, p, r]) => m.pcieByCompletions(a, l, p, r).findIndex((w) => w > 0n))));")
    for case, k in zip(cases, got):
        assert k == min_completions(*case), case


def test_explorer_headers():
    """The box's header table (pcieHeaders) against the header follow-up: Length in DW,
    Byte Count (the bytes left, the completion's own included) and Lower Address for
    [48, 64, 64, 64, 16] from 0x1010, and on random splits of the page against the rules
    (the last completion is the one whose Byte Count equals its own size)."""
    import json

    from page_tests import explorer_require, node_json

    rng = random.Random(21)
    jobs = [[ADDR, LEN, [48, 64, 64, 64, 16]]]
    for _ in range(200):
        length = 4 * rng.randint(1, 128)
        addr = 4 * rng.randrange(0, 1 << 12)
        splits = completion_splits(addr, length, 256, 64)
        jobs.append([addr, length, splits[rng.randrange(len(splits))]])
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({json.dumps(jobs)}.map(([a, l, s]) => m.pcieHeaders(a, l, s))));")
    first = got[0]
    assert [h["dw"] for h in first] == [12, 16, 16, 16, 4]
    assert [h["la"] for h in first] == [0x10, 0x40, 0x00, 0x40, 0x00]
    assert [h["bc"] for h in first] == [256, 208, 144, 80, 16]
    for (addr, length, sizes), hs in zip(jobs, got):
        pos, left = addr, length
        for size, h in zip(sizes, hs):
            assert (h["addr"], h["size"], h["dw"], h["bc"], h["la"]) == (pos, size, size // 4, left, pos & 0x7F)
            pos, left = pos + size, left - size
        assert [h["bc"] == h["size"] for h in hs] == [False] * (len(hs) - 1) + [True]
