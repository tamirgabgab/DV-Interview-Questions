"""Question 0057: the page's missing_one, missing_two, missing_and_dup and missing_k against
the generator's counting reference (tools/figures/q0057.py) on random runs with tags out of
order; the page's numbers (tag 4, the split of 5 and 12, tag 7 and duplicate 3, 72 bits);
XOR fooled by a duplicate; the explorer's JavaScript; and the page copies of the blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0057  # noqa: E402

ns = load_python(57)
missing_one, missing_two, missing_and_dup, missing_k = (ns[k] for k in ("missing_one", "missing_two", "missing_and_dup", "missing_k"))


def run(rng, n, missing=(), dup=()):
    sent = list(range(n))
    ret = [t for t in sent if t not in missing] + list(dup)
    rng.shuffle(ret)
    return sent, ret


def test_page_examples():
    assert missing_one(q0057.A_SENT, q0057.A_RET) == 4
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
        assert missing_one(sent, ret) == a == q0057.truth(sent, ret)[0][0]
        sent, ret = run(rng, n, (a, b))
        assert missing_two(sent, ret, w) == sorted((a, b)) == q0057.truth(sent, ret)[0]
        sent, ret = run(rng, n, (a,), (b,))
        assert missing_and_dup(sent, ret) == (a, b)
        assert q0057.truth(sent, ret) == ([a], [b])
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
    assert "| ‏72 |" in q0057.memory_table() and "| ‏40 |" in q0057.memory_table()


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
        x, part, s, q, out = q0057.accumulators(sent, ret, w)
        assert [res["x"], res["part"], res["s"], res["q"], res["out"]] == [x, part, s, q, out]
        assert res["one"] == missing_one(sent, ret)
        miss, dup = q0057.truth(sent, ret)
        if x:
            assert res["two"] == missing_two(sent, ret, w)
        if s:
            assert res["sums"] == list(missing_and_dup(sent, ret))
        if out > 0:
            assert res["k"] == missing_k(sent, ret, out, n)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(57)
