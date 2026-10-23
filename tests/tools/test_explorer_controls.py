"""The shared explorer controls of round V: the seeded generator exported by
explorer/core.js is the mulberry32 the question tests replay in Python, and a seeded
draw of the random models is reproducible from its seed."""

from page_tests import explorer_require, node_json


def mulberry32(seed):
    """The JS recurrence in unsigned 32-bit arithmetic (every step is exact in doubles)."""
    a = seed & 0xFFFFFFFF

    def imul(x, y):
        return ((x & 0xFFFFFFFF) * (y & 0xFFFFFFFF)) & 0xFFFFFFFF

    def nxt():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = imul(a ^ (a >> 15), 1 | a)
        t = ((t + imul(t ^ (t >> 7), 61 | t)) & 0xFFFFFFFF) ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296

    return nxt


def test_mulberry32_matches_python():
    got = node_json(
        f"""
      const m = {explorer_require()};
      const out = {{}};
      for (const seed of [1, 7, 4242, 99999]) {{ const r = m.mulberry32(seed); out[seed] = Array.from({{length: 25}}, () => r()); }}
      console.log(JSON.stringify(out));
    """
    )
    for seed in (1, 7, 4242, 99999):
        r = mulberry32(seed)
        assert got[str(seed)] == [r() for _ in range(25)]


def test_seeded_draws_replay():
    got = node_json(
        f"""
      const m = {explorer_require()};
      const draw = (seed) => {{
        const r = m.mulberry32(seed);
        return {{ poly: m.polyRandom(6, r), stock: m.stockRandom(10, r), perm: m.permShuffle(8, r), ttt: m.tttRandom(false, r).board, floyd: m.floydRandom(6, r) }};
      }};
      console.log(JSON.stringify({{ a: draw(4242), b: draw(4242), c: draw(777) }}));
    """
    )
    assert got["a"] == got["b"]
    assert got["a"] != got["c"]
    assert len(set(got["a"]["poly"])) == 6 and all(0 <= v < 360 for v in got["a"]["poly"])
    assert len(got["a"]["stock"]) == 10 and all(1 <= v <= 20 for v in got["a"]["stock"])
    assert sorted(got["a"]["perm"][1:]) == list(range(1, 9))


def test_wavedrom_export():
    """The WaveDrom export of a timing strip (U133): a lane per row, "." for a repeated
    level or bus value, bus values in data, a "p…" clock (or "h"/"l" per half-cycle slot),
    a flag as a level, names without markup, a shorter lane for frames not reached yet;
    the text form parses back to the same object."""
    import json

    got = node_json(
        f"""
      const m = {explorer_require()};
      const rows = [{{ name: "clk", kind: "clock" }}, {{ name: "<code>sig</code> &amp; &#8207;x", kind: "bit", values: [0, 0, 1, 1, 1, 0, 0, 1] }},
        {{ name: "cnt", kind: "bus", values: [0, 1, 2, 2, 0, 1, null, null] }}, {{ name: "a_rule", kind: "flag", values: [0, 0, 0, 1, 0, 0, 0, 0] }}];
      const full = m.waveDromOf(rows, 8, {{ ticks: (k) => k }}), late = m.waveDromOf(rows.slice(0, 1), 1, {{ ticks: (k) => 40 + k }}), half = m.waveDromOf(rows.slice(0, 1), 6, {{ half: true }});
      console.log(JSON.stringify({{ full, late, half, text: m.waveDromText(full) }}));
    """
    )
    assert got["full"] == {"signal": [
        {"name": "clk", "wave": "p......."},
        {"name": "sig & x", "wave": "0.1..0.1"},
        {"name": "cnt", "wave": "===.==", "data": ["0", "1", "2", "0", "1"]},
        {"name": "a_rule", "wave": "0..10..."},
    ], "head": {"tick": "0"}}
    assert got["half"] == {"signal": [{"name": "clk", "wave": "hlhlhl"}]}
    assert got["late"] == {"signal": [{"name": "clk", "wave": "p"}], "head": {"tick": "40"}}   # a window, one slot
    assert json.loads(got["text"]) == got["full"]
