"""Question 0103, longest prefix match: the numbers the page states, recomputed from the
references in tools/figures/q0103.py (the lookups of the example, the 37 nodes of the binary
trie and how they split, the table of strides, the entries a prefix fills, the root of s = 8,
the pipeline clock by clock and the latency), the generated blocks, the per-clock trace the
testbench checks, and the box's models under Node against the same references."""

import json
import random
import re
import sys

from extract_code import ROOT
from page_tests import assert_figures_match, explorer_require, node_json

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0103  # noqa: E402


def test_example_lookups():
    routes = q0103.example_routes()
    got = [q0103.best(routes, q0103.quad_bits(a, 32)) for a in q0103.LOOKUPS]
    assert got == ["C", "B", "A", "E", "D", "D"]
    # 10.1.2.3 matches four rows: /0, /8, /16 and /24
    m = q0103.matching(routes, q0103.quad_bits("10.1.2.3", 32))
    assert sorted(len(p) for p, _ in m) == [0, 8, 16, 24]
    assert int(q0103.quad_bits("10.1.2.3", 32), 2) == 10 * 2**24 + 1 * 2**16 + 2 * 2**8 + 3
    # with no /0, 8.8.8.8 has no answer
    assert q0103.best(routes[:-1], q0103.quad_bits("8.8.8.8", 32)) is None
    # the mask: 2^32 - 2^(32 - k), 0 at k = 0 and 32 ones at k = 32
    mask = lambda k: 2**32 - 2 ** (32 - k)
    assert mask(0) == 0 and mask(32) == 2**32 - 1 and mask(8) == 0xFF000000
    # the trap: x86 takes the shift count mod 32, so ~0u << 32 keeps 32 ones; a 5-bit 32 - k is 0
    assert ((2**32 - 1) << (32 % 32)) & (2**32 - 1) == 2**32 - 1 and (32 - 0) % 32 == 0
    assert len(range(0, 33)) == 33 > 2**5 and 33 <= 2**6


def test_binary_trie_numbers():
    routes = q0103.example_routes()
    nodes = q0103.trie_nodes(routes)
    assert len(nodes) == 37
    # /8, /16 and /24 share the path of the /24 (24 nodes), the /12 splits at the first bit (12)
    p24 = q0103.quad_bits("10.1.2.0", 24)
    p12 = q0103.quad_bits("172.16.0.0", 12)
    assert p24[0] != p12[0]
    assert len({p24[:i] for i in range(1, 25)}) + len({p12[:i] for i in range(1, 13)}) + 1 == 37
    # the walk of 185 in the small table: D, A, (10), B, (1011), then no child 1
    path = q0103.trie_path(q0103.SMALL, format(185, "08b"))
    assert [(n, h, b) for n, h, b in path] == [("", "D", "D"), ("1", "A", "A"), ("10", None, "A"),
                                                ("101", "B", "B"), ("1011", None, "B")]
    assert format(185, "08b") == "10111001" and "10111" not in q0103.trie_nodes(q0103.SMALL)
    assert q0103.best(q0103.SMALL, format(182, "08b")) == "C"
    # N * W + 1 bounds the nodes
    assert len(nodes) <= len(routes) * 32 + 1
    # deleting 10.0.0.0/8 keeps its node: it has a child
    rest = [r for r in routes if len(r[0]) != 8]
    assert len(q0103.trie_nodes(rest)) == 37
    # the box's presets: the "no match" table with the address 0 walks the root and node 0
    none = q0103.SMALL[1:]
    assert [n for n, _, _ in q0103.trie_path(none, "00000000")] == ["", "0"]
    assert q0103.best(none, "00000000") is None
    dflt = [("", "D"), (format(200, "08b")[:5], "A"), (format(202, "08b")[:8], "B"), (format(48, "08b")[:4], "C")]
    assert q0103.best(dflt, format(100, "08b")) == "D"
    # 183/3 is 160/3, 101*
    assert format(183, "08b")[:3] == "101" and int("101" + "0" * 5, 2) == 160


def test_multibit_numbers():
    routes = q0103.example_routes()
    stats = [q0103.multibit_stats(routes, 32, s) for s in (1, 2, 4, 8)]
    assert stats == [(32, 35, 70, 6), (16, 17, 68, 8), (8, 8, 128, 20), (4, 4, 1024, 274)]
    for s in (1, 2, 4, 8):
        for a in q0103.LOOKUPS:
            bits = q0103.quad_bits(a, 32)
            assert q0103.multibit_lookup(routes, s, bits) == q0103.best(routes, bits)
    # s = 1: 35 nodes, not 37: the two leaves of the binary trie hold their hop in the parent's entry
    leaves = [n for n in q0103.trie_nodes(routes) if n + "0" not in q0103.trie_nodes(routes) and n + "1" not in q0103.trie_nodes(routes)]
    assert len(leaves) == 2 and 37 - len(leaves) == 35
    # s = 8: the root alone is 256 entries, 255 of them hold D
    ex = q0103.expand(routes, 8)
    root = [ex.get(format(j, "08b")) for j in range(256)]
    assert sum(1 for e in root if e and e[0] == "D") == 255
    # a /k prefix fills 2^(s - k mod s) entries, one when s divides k (k > 0), 2^s for /0
    for s in (1, 2, 4, 8):
        for k in range(0, 33):
            n = 1 << (q0103.target_len(k, s) - k)
            if k == 0:
                assert n == 2**s
            elif k % s:
                assert n == 2 ** (s - k % s) <= 2 ** (s - 1)
            else:
                assert n == 1
    # 101* with s = 2 is 1010* and 1011*
    assert sorted(q0103.expand([("101", "B")], 2)) == ["1010", "1011"]
    # the order of the rows does not change the expanded entries
    rng = random.Random(3)
    for _ in range(200):
        rows = [("".join(rng.choice("01") for _ in range(rng.randint(0, 8))), rng.choice("ABCD")) for _ in range(rng.randint(1, 6))]
        uniq = list(dict(rows).items())
        shuffled = uniq[:]
        rng.shuffle(shuffled)
        for s in (1, 2, 4):
            assert q0103.expand(uniq, s) == q0103.expand(shuffled, s)
    # the box's stride-2 walk of 185: entries 10, 11 and 10, stopping at an empty entry with B
    lv = q0103.multibit_levels(q0103.SMALL, 8, 2)
    assert lv[0][2] == ["A", 0] and lv[1][3] == ["B", 0] and lv[2][2] == [None, None]
    # with A as 128/2 (10*), the root's entry 11 keeps D
    changed = [("", "D"), ("10", "A")] + q0103.SMALL[2:]
    assert q0103.multibit_levels(changed, 8, 2)[0][3] == ["D", None]


def test_pipeline_numbers():
    tr = q0103.pipe_trace(q0103.SMALL, 8, 2, q0103.PIPE_IN)
    L = 8 // 2
    assert len(tr) == len(q0103.PIPE_IN) + L - 1 == 8
    # 185 enters at clock 1 and leaves stage 4 at the end of clock 4; it stopped going down in stage 3
    assert tr[3][1][3][0] == 185 and tr[3][1][3][1] == "B"
    assert tr[2][1][2] == (185, "B", False) and tr[1][1][1][2] is True
    # 64 stops in stage 1 with E
    assert tr[3][1][0] == (64, "E", False)
    outs = [st[L - 1] for _, st in tr]
    assert [o[:2] if o else None for o in outs[L - 1:]] == [(185, "B"), (182, "C"), None, (64, "E"), (3, "D")]


def test_tb_trace_matches_reference():
    tb = (ROOT / "tests" / "0103" / "tb.sv").read_text(encoding="utf-8")
    want = json.loads("[" + re.search(r"string want_trace\[8\] = '\{(.*?)\};", tb).group(1) + "]")
    got = []
    for _, st in q0103.pipe_trace(q0103.SMALL, 8, 2, q0103.PIPE_IN):
        got.append(" ".join("." if x is None else f"{x[0]}:{x[1] or '-'}" for x in st))
    assert want == got


def test_figures():
    assert_figures_match(103)


def test_explorer_models():
    rng = random.Random(103)
    tables = [q0103.SMALL, q0103.SMALL[1:], [("", "D"), ("11001", "A"), ("11001010", "B"), ("0011", "C")], []]
    for _ in range(40):
        tables.append([("".join(rng.choice("01") for _ in range(rng.randint(0, 8))), rng.choice("ABCDE")) for _ in range(rng.randint(1, 6))])
    addrs = [0, 3, 64, 100, 182, 185, 255] + [rng.randrange(256) for _ in range(10)]
    script = f"""
      const m = {explorer_require()};
      const tables = {json.dumps(tables)}, addrs = {json.dumps(addrs)};
      const bits = (a) => a.toString(2).padStart(8, "0");
      const out = tables.map((t) => ({{
        nodes: m.lpmNodes(t),
        layout: m.lpmLayout(m.lpmNodes(t)),
        best: addrs.map((a) => m.lpmBest(t, bits(a))),
        path: addrs.map((a) => m.lpmPath(t, bits(a))),
        levels: [1, 2, 4].map((s) => m.lpmLevels(t, 8, s).levels.map((lv) => lv.map((e) => [e[0], e[1]]))),
        multi: [1, 2, 4].map((s) => addrs.map((a) => {{ const w = m.lpmMultiPath(t, 8, s, a); return [w.length, w[w.length - 1].best]; }})),
      }}));
      const parse = ["183/3", "160/3", "101*", "*", "0/0", "255/8", "256/1", "1/9", "10/", "1x*", "", "  64 / 2 "].map((x) => m.lpmParse(x));
      console.log(JSON.stringify({{ out, parse, target: [[0, 2], [1, 2], [2, 2], [3, 2], [5, 4]].map(([k, s]) => m.lpmTarget(k, s)) }}));
    """
    got = node_json(script)
    for t, g in zip(tables, got["out"]):
        nodes = q0103.trie_nodes(t)
        assert sorted(g["nodes"]) == sorted(nodes)
        pos, width = q0103.layout(nodes)
        assert g["layout"]["width"] == width and g["layout"]["pos"] == pos
        for a, b, p in zip(addrs, g["best"], g["path"]):
            ab = format(a, "08b")
            assert b == q0103.best(t, ab)
            assert [tuple(x) for x in p] == q0103.trie_path(t, ab)
        for s, lv, walks in zip((1, 2, 4), g["levels"], g["multi"]):
            assert lv == q0103.multibit_levels(t, 8, s)
            for a, (n, b) in zip(addrs, walks):
                ab = format(a, "08b")
                assert b == q0103.multibit_lookup(t, s, ab) == q0103.best(t, ab)
                # the walk reads one entry a level until an entry with no child
                trace = q0103.pipe_trace(t, 8, s, [a])
                last = trace[8 // s - 1][1][8 // s - 1]
                assert last[1] == b
    p = got["parse"]
    assert p[0] == {"bits": "101", "len": 3, "value": 160, "norm": True, "given": 183}
    assert p[1] == {"bits": "101", "len": 3, "value": 160, "norm": False, "given": 160}
    assert p[2] == {"bits": "101", "len": 3, "value": 160, "norm": False}
    assert p[3]["bits"] == "" and p[4]["len"] == 0 and p[5]["bits"] == "11111111"
    assert all("error" in x for x in p[6:10]) and p[10] == {"empty": True}
    assert p[11]["bits"] == "01" and p[11]["value"] == 64
    assert got["target"] == [2, 2, 2, 4, 8] == [q0103.target_len(k, s) for k, s in [(0, 2), (1, 2), (2, 2), (3, 2), (5, 4)]]
