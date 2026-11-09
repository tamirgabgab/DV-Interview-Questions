"""Question 0058: the page's missing_one, missing_two, missing_and_dup and missing_k against
the generator's counting reference (tools/figures/q0058.py) on random runs with tags out of
order; the page's numbers (tag 4, the split of 5 and 12, tag 7 and duplicate 3, 72 bits);
XOR fooled by a duplicate; the explorer's JavaScript; and the page copies of the blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0058  # noqa: E402

ns = load_python(58)
missing_one, missing_two, missing_and_dup, missing_k = (ns[k] for k in ("missing_one", "missing_two", "missing_and_dup", "missing_k"))


def run(rng, n, missing=(), dup=()):
    sent = list(range(n))
    ret = [t for t in sent if t not in missing] + list(dup)
    rng.shuffle(ret)
    return sent, ret


def test_page_examples():
    assert missing_one(q0058.A_SENT, q0058.A_RET) == 4
    sent, ret = list(range(16)), [t for t in range(16) if t not in (5, 12)]
    assert missing_two(sent, ret, 4) == [5, 12]
    sent, ret = list(range(10)), [t for t in range(10) if t != 7] + [3]
    assert missing_and_dup(sent, ret) == (7, 3)
    assert sum(sent) - sum(ret) == 4 and sum(t * t for t in sent) - sum(t * t for t in ret) == 40
    assert missing_one(sent, ret) == 4                          # XOR names a tag that came back
    assert 8 + 8 * 8 == 72


def test_against_counting():
    rng = random.Random(57)
    for _ in range(300):
        w = rng.randint(2, 8)
        n = 1 << w
        a, b = rng.sample(range(n), 2)
        sent, ret = run(rng, n, (a,))
        assert missing_one(sent, ret) == a == q0058.truth(sent, ret)[0][0]
        sent, ret = run(rng, n, (a, b))
        assert missing_two(sent, ret, w) == sorted((a, b)) == q0058.truth(sent, ret)[0]
        sent, ret = run(rng, n, (a,), (b,))
        assert missing_and_dup(sent, ret) == (a, b)
        assert q0058.truth(sent, ret) == ([a], [b])
        k = rng.randint(1, min(5, n - 1))
        miss = rng.sample(range(n), k)
        sent, ret = run(rng, n, miss)
        assert missing_k(sent, ret, k, n) == sorted(miss)


def test_reused_tags():
    """Tags sent again after they come back: the accumulators describe what is out now."""
    rng = random.Random(58)
    for _ in range(100):
        n = 32
        sent, ret = [], []
        for _ in range(5):
            s, r = run(rng, n)
            sent += s
            ret += r
        a = rng.randrange(n)
        sent.append(a)
        assert missing_one(sent, ret) == a


def test_memory_table():
    t = q0058.memory_table()
    assert "| ‏72 |" in t and '| ‏26 (<span dir="ltr">9 + 17</span>) |' in t
    assert '| ‏88 (<span dir="ltr">10 + 18 + 26 + 34</span>) |' in t
    assert q0058.final_bits() == {"sums": [9, 17], 2: [9, 17], 3: [10, 18, 26], 4: [10, 18, 26, 34]}
    # the general forms of the page: s, q in W + 1 and 2W + 1 bits; p_i in at most
    # iW + ceil(log2 k) bits (exactly that for 8-bit tags)
    for w in range(2, 11):
        fb = q0058.final_bits(w)
        assert fb["sums"] == [w + 1, 2 * w + 1]
        for k in (2, 3, 4):
            bound = [i * w + (k - 1).bit_length() for i in range(1, k + 1)]
            assert all(f <= g for f, g in zip(fb[k], bound)) and (w != 8 or fb[k] == bound)


def _wrap(v, b):
    v &= (1 << b) - 1
    return v - (1 << b) if v >> (b - 1) else v


def test_wrapping_accumulators():
    """Trap 3 and the memory table: the running sums may wrap; registers of the final
    value's width (with a sign bit for s and q) give the right answer, with every tag out at
    once mid-run; without the sign bit (W and 2W bits) the division of part c fails."""
    rng = random.Random(580)
    wrong_narrow = 0
    for _ in range(1500):
        w = rng.choice([4, 6, 8])
        n = 1 << w
        a, d = rng.sample(range(n), 2)
        sent, ret = run(rng, n, (a,), (d,))
        for sb, qb in ((w + 1, 2 * w + 1), (w, 2 * w)):
            s = q = 0
            for t in sent:                                  # every tag out before any response
                s, q = _wrap(s + t, sb), _wrap(q + t * t, qb)
            for t in ret:
                s, q = _wrap(s - t, sb), _wrap(q - t * t, qb)
            ok = s != 0 and q % s == 0 and ((q // s + s) // 2, (q // s - s) // 2) == (a, d)
            if sb == w + 1:
                assert ok and (s, q) == (a - d, a * a - d * d)
            else:
                wrong_narrow += not ok
        k = rng.randint(1, 4)
        miss = rng.sample(range(n), k)
        sent, ret = run(rng, n, miss)
        widths = [i * w + (k - 1).bit_length() for i in range(1, k + 1)]
        p = [0] * k
        for sign, tags in ((1, sent), (-1, ret)):
            for t in tags:
                p = [(p[i] + sign * t ** (i + 1)) % (1 << widths[i]) for i in range(k)]
        assert p == [sum(m ** (i + 1) for m in miss) for i in range(k)]
    assert wrong_narrow > 100


def test_page_text_numbers():
    """Part a's start at 0, part b's W^2 remark, the worked example of part d, k from the
    counter, and the trap of two missing and two duplicated."""
    for m in range(1, 9):
        x = 0
        for t in range(4 * m):
            x ^= t
        assert x == 0
    rng = random.Random(581)
    for _ in range(300):                                    # bit j of part[j] is bit j of x
        w = rng.randint(2, 8)
        miss = rng.sample(range(1 << w), rng.randint(1, 4))
        x, part, *_ = q0058.accumulators(miss, [], w)
        assert all((part[j] >> j & 1) == (x >> j & 1) for j in range(w))
    assert 8 * 8 == 64
    miss = [1, 8, 14]
    p = [sum(a ** i for a in miss) for i in (1, 2, 3)]
    assert p == [23, 261, 3257]
    e1 = p[0]
    e2 = (e1 * p[0] - p[1]) // 2
    e3 = (e2 * p[0] - e1 * p[1] + p[2]) // 3
    assert (e1 * p[0], e2 * p[0], e1 * p[1]) == (529, 3082, 6003)
    assert (e1, e2, e3) == (23, 134, 112)
    assert all(z ** 3 - 23 * z * z + 134 * z - 112 == (z - 1) * (z - 8) * (z - 14) for z in range(-5, 30))
    sent = list(range(16))
    assert missing_k(sent, [t for t in sent if t not in miss], 3, 16) == miss
    assert missing_k(sent, [t for t in sent if t not in (5, 12)], 3, 16) == [0, 5, 12]   # k too big: root 0
    ret = [t for t in sent if t not in (0, 6)] + [1, 4]
    x, _, s, q, out = q0058.accumulators(sent, ret, 4)
    assert (x, s, q, out) == (3, 1, 19, 0)
    assert missing_and_dup(sent, ret) == (10, 9) and 10 ^ 9 == x
    assert sum(t ** 3 for t in sent) - sum(t ** 3 for t in ret) != 10 ** 3 - 9 ** 3
    assert sum(sent) == 120                                 # s before any response
    assert _wrap(120, 5) == -8
    assert (sum(range(256)).bit_length(), sum(t * t for t in range(256)).bit_length()) == (15, 23)


def test_two_and_two_caught_by_cubes():
    """The trap: two missing and two duplicated give out = 0 and, often, a confident answer of
    part c inside the tags (with a XOR d = x too); the sum of cubes always tells."""
    import itertools

    for n in (16, 32):
        confident = with_xor = 0
        for m in itertools.combinations(range(n), 2):
            rest = [t for t in range(n) if t not in m]
            for d in itertools.combinations_with_replacement(rest, 2):
                s = sum(m) - sum(d)
                q = sum(t * t for t in m) - sum(t * t for t in d)
                if s == 0 or q % s or (q // s + s) % 2:
                    continue
                a, b = (q // s + s) // 2, (q // s - s) // 2
                if not (0 <= a < n and 0 <= b < n and a != b):
                    continue
                confident += 1
                with_xor += (a ^ b) == (m[0] ^ m[1] ^ d[0] ^ d[1])
                assert sum(t ** 3 for t in m) - sum(t ** 3 for t in d) != a ** 3 - b ** 3
        assert confident > 0 and with_xor > 0


def test_explorer_matches_the_page_code():
    from page_tests import explorer_require, node_json

    rng = random.Random(59)
    cases = []
    for _ in range(60):
        w = rng.choice([3, 4, 5])
        n = 1 << w
        miss = rng.sample(range(n), rng.randint(0, 3))
        dup = rng.sample([t for t in range(n) if t not in miss], rng.randint(0, 1))
        sent, ret = run(rng, n, miss, dup)
        cases.append([n, w, sent, ret])
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([n, w, s, r]) => m.tcDecode(s, r, w, n))));""")
    for (n, w, sent, ret), res in zip(cases, got):
        x, part, s, q, out = q0058.accumulators(sent, ret, w)
        assert [res["x"], res["part"], res["s"], res["q"], res["out"]] == [x, part, s, q, out]
        assert res["one"] == missing_one(sent, ret)
        miss, dup = q0058.truth(sent, ret)
        if x:
            assert res["two"] == missing_two(sent, ret, w)
        if s:
            assert res["sums"] == list(missing_and_dup(sent, ret))
        if out > 0:
            assert res["k"] == missing_k(sent, ret, out, n)


def test_explorer_widths():
    """The box's width select: s and q wrapped to W + 1 and 2W + 1 bits (signed) decode as
    the full sums; at W and 2W bits the page's case (3 missing, 12 twice of 16) goes wrong,
    and before any response s = 120 reads as -8 in five bits."""
    from page_tests import explorer_require, node_json

    rng = random.Random(582)
    cases = []
    for _ in range(80):
        w = rng.choice([3, 4, 5])
        n = 1 << w
        a, d = rng.sample(range(n), 2)
        sent, ret = run(rng, n, (a,), (d,))
        cases.append([n, w, sent, ret, a, d])
    got = node_json(f"""
      const m = {explorer_require()};
      const cs = {json.dumps(cases)};
      const r16 = Array.from({{ length: 16 }}, (_, t) => t);
      console.log(JSON.stringify({{ rnd: cs.map(([n, w, s, r]) => [0, 1, 2].map((v) => m.tcDecode(s, r, w, n, v))),
        page: [1, 2].map((v) => m.tcDecode(r16, r16.filter((t) => t !== 3).concat([12]), 4, 16, v).sums),
        start: m.tcAcc(r16, [], 4, 1).s }}));""")
    for (n, w, sent, ret, a, d), (full, ok, narrow) in zip(cases, got["rnd"]):
        assert full["sums"] == ok["sums"] == [a, d]
        assert [narrow["s"], narrow["q"]] == [_wrap(a - d, w), _wrap(a * a - d * d, 2 * w)]
    assert got["page"] == [[3, 12], [12, 5]] and got["start"] == -8


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(58)
