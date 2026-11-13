"""Question 0103: the page's Python code (it runs as published) against the references of
tools/figures/q0103.py, which work on strings of bits: lpm_naive, Trie (insert, delete with the
pruning, lookup) and MultiTrie (every stride, any order of the rows) on random tables of 8, 16
and 32 bits, and the pipeline clock by clock against pipe_trace."""

import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0103  # noqa: E402

ns = load_python(103)


def bits(v, w):
    return format(v, f"0{w}b")


def random_table(rng, w, n, default=None):
    """n rows (value, k, hop) with random lengths, some nested, the values not normalized."""
    rows = []
    for _ in range(n):
        k = rng.choice([0, w, rng.randint(1, w), rng.randint(1, w)])
        if rows and rng.random() < 0.4:            # nested under an earlier row
            v0, k0, _ = rng.choice(rows)
            k = rng.randint(k0, w)
            v = v0 & ns["mask"](k0, w) | rng.getrandbits(w) & ~ns["mask"](k0, w) & ((1 << w) - 1)
        else:
            v = rng.getrandbits(w)
        rows.append((v, k, rng.choice("ABCDEFGH")))
    if default is not None:
        rows.append((rng.getrandbits(w), 0, default))
    return rows


def ref_routes(rows, w):
    return [(bits(v, w)[:k], hop) for v, k, hop in rows]


def probes(rng, rows, w, n):
    """Random addresses, and the first and last address of every row and their neighbours."""
    out = [rng.getrandbits(w) for _ in range(n)]
    for v, k, _ in rows:
        lo = v & ns["mask"](k, w)
        hi = lo | ((1 << (w - k)) - 1)
        out += [lo, hi, (lo - 1) % (1 << w), (hi + 1) % (1 << w)]
    return out


def test_example():
    routes = [ns["route"](f"{q}/{k}", hop) for q, k, hop in q0103.EXAMPLE]
    got = [ns["lpm_naive"](routes, ns["ip"](a)) for a in q0103.LOOKUPS]
    assert got == ["C", "B", "A", "E", "D", "D"]
    assert ns["ip"]("10.1.2.3") == 10 * 2**24 + 1 * 2**16 + 2 * 2**8 + 3 == 167838211
    assert ns["route"]("10.1.2.3/16", "B") == (ns["ip"]("10.1.0.0"), 16, "B")
    assert ns["mask"](0) == 0 and ns["mask"](32) == 2**32 - 1 and ns["mask"](8) == 0xFF000000
    assert ns["lpm_naive"](routes[:-1], ns["ip"]("8.8.8.8")) is None          # no default: no answer
    # a prefix given twice: the later row wins, in the scan and in both tries
    dup = routes + [ns["route"]("10.1.0.0/16", "X")]
    assert ns["lpm_naive"](dup, ns["ip"]("10.1.3.4")) == "X"


def test_naive_against_reference():
    rng = random.Random(103)
    for w in (8, 16, 32):
        for _ in range(150):
            rows = random_table(rng, w, rng.randint(0, 9), rng.choice([None, "D"]))
            ref = ref_routes(rows, w)
            for a in probes(rng, rows, w, 20):
                assert ns["lpm_naive"](rows, a, w) == q0103.best(ref, bits(a, w)), (w, rows, a)


def test_trie():
    rng = random.Random(7)
    for w in (8, 16, 32):
        for _ in range(120):
            rows = random_table(rng, w, rng.randint(0, 10), rng.choice([None, "D"]))
            t = ns["Trie"](w)
            for v, k, hop in rows:
                t.insert(v, k, hop)
            ref = ref_routes(rows, w)
            assert t.nodes == len(q0103.trie_nodes(ref))
            for a in probes(rng, rows, w, 20):
                assert t.lookup(a) == q0103.best(ref, bits(a, w))
            # delete the prefixes one by one, in a random order; the rest keep their answers
            live = dict((p, hop) for p, hop in ref)
            order = list(live)
            rng.shuffle(order)
            for p in order:
                assert t.delete(int(p + "0" * (w - len(p)), 2), len(p))
                assert not t.delete(int(p + "0" * (w - len(p)), 2), len(p))    # gone already
                del live[p]
                left = list(live.items())
                assert t.nodes == len(q0103.trie_nodes(left)), (rows, p)
                for a in probes(rng, rows, w, 5):
                    assert t.lookup(a) == q0103.best(left, bits(a, w))
            assert t.nodes == 1 and t.root == [None, None, None]


def test_trie_example():
    routes = [ns["route"](f"{q}/{k}", hop) for q, k, hop in q0103.EXAMPLE]
    t = ns["Trie"]()
    for v, k, hop in routes:
        t.insert(v, k, hop)
    assert t.nodes == 37 == len(q0103.trie_nodes(q0103.example_routes()))
    assert [t.lookup(ns["ip"](a)) for a in q0103.LOOKUPS] == ["C", "B", "A", "E", "D", "D"]
    assert t.delete(ns["ip"]("10.0.0.0"), 8) and t.nodes == 37            # the /8 node is needed
    assert t.lookup(ns["ip"]("10.200.0.1")) == "D" and t.lookup(ns["ip"]("10.1.2.3")) == "C"
    small = ns["Trie"](8)
    for p, hop in q0103.SMALL:
        small.insert(int(p.ljust(8, "0"), 2), len(p), hop)
    assert small.lookup(185) == "B" and small.lookup(182) == "C" and small.lookup(64) == "E"


def test_multitrie():
    rng = random.Random(11)
    for w in (8, 16, 32):
        for s in [x for x in (1, 2, 4, 8) if w % x == 0]:
            for _ in range(40):
                rows = random_table(rng, w, rng.randint(0, 9), rng.choice([None, "D"]))
                rng.shuffle(rows)                       # the order of the rows must not matter
                t = ns["MultiTrie"](w, s)
                for v, k, hop in rows:
                    t.insert(v, k, hop)
                ref = ref_routes(rows, w)
                assert t.entries() == len(q0103.multibit_nodes(ref, s)) << s
                assert sum(e[0] is not None for lv in t.levels for e in lv) == len(q0103.expand(ref, s))
                for a in probes(rng, rows, w, 15):
                    assert t.lookup(a) == q0103.best(ref, bits(a, w)), (w, s, rows, a)


def test_multitrie_example():
    routes = [ns["route"](f"{q}/{k}", hop) for q, k, hop in q0103.EXAMPLE]
    stats = []
    for s in (1, 2, 4, 8):
        t = ns["MultiTrie"](32, s)
        for v, k, hop in routes:
            t.insert(v, k, hop)
        filled = sum(e[0] is not None for lv in t.levels for e in lv)
        stats.append((len(t.levels), t.entries() >> s, t.entries(), filled))
        assert [t.lookup(ns["ip"](a)) for a in q0103.LOOKUPS] == ["C", "B", "A", "E", "D", "D"]
    assert stats == [(32, 35, 70, 6), (16, 17, 68, 8), (8, 8, 128, 20), (4, 4, 1024, 274)]
    # the memories are those of the reference, node by node, for the small table and s = 2
    t = ns["MultiTrie"](8, 2)
    for p, hop in q0103.SMALL:
        t.insert(int(p.ljust(8, "0"), 2), len(p), hop)
    assert [[[e[0], e[2]] for e in lv] for lv in t.levels] == q0103.multibit_levels(q0103.SMALL, 8, 2)


def test_pipeline():
    rng = random.Random(5)
    t = ns["MultiTrie"](8, 2)
    for p, hop in q0103.SMALL:
        t.insert(int(p.ljust(8, "0"), 2), len(p), hop)
    want = [st for _, st in q0103.pipe_trace(q0103.SMALL, 8, 2, q0103.PIPE_IN)]
    assert ns["pipeline"](t, q0103.PIPE_IN) == want
    for w, s in ((8, 1), (8, 2), (16, 4), (32, 8)):
        for _ in range(20):
            rows = random_table(rng, w, rng.randint(0, 8), rng.choice([None, "D"]))
            ref = ref_routes(rows, w)
            mt = ns["MultiTrie"](w, s)
            for v, k, hop in rows:
                mt.insert(v, k, hop)
            ins = [None if rng.random() < 0.2 else rng.getrandbits(w) for _ in range(30)]
            tr = ns["pipeline"](mt, ins)
            assert tr == [st for _, st in q0103.pipe_trace([(p, h) for p, h in ref], w, s, ins)]
            L = w // s
            for c, a in enumerate(ins):                  # each lookup leaves L - 1 clocks later
                out = tr[c + L - 1][L - 1]
                if a is None:
                    assert out is None
                else:
                    assert out[0] == a and out[1] == q0103.best(ref, bits(a, w)) and not out[2]
