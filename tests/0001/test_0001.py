"""Question 0001: the edge detector explorer against a Python replay of the module (sig_q
is the previous cycle's sig and 0 during reset; pulse = sig & ~sig_q, its mirror for a
falling edge, XOR for both) and against the page's own timing diagram."""

import json
import random
import re

from extract_code import question_path

MODES = {
    "rise": lambda s, q: int(s == 1 and q == 0),
    "fall": lambda s, q: int(s == 0 and q == 1),
    "both": lambda s, q: int(s != q),
}


def replay(sig, mode):
    sig_q = [0] + sig[:-1]                      # cycle 0 is the reset cycle
    return sig_q, [MODES[mode](s, q) for s, q in zip(sig, sig_q)]


def wave(text):
    """A WaveDrom wave string of 0, 1 and . as the value per cycle."""
    out = []
    for c in text:
        out.append(out[-1] if c == "." else int(c))
    return out


def test_page_diagram():
    page = question_path(1).read_text(encoding="utf-8")
    rows = dict(re.findall(r'name: "(\w+)",\s*wave: "([01.p]+)"', page))
    sig, sig_q, pulse = wave(rows["sig"]), wave(rows["sig_q"]), wave(rows["pulse"])
    assert replay(sig, "rise") == (sig_q, pulse)
    assert sum(pulse) == 2 and all(w == 1 for w in pulse_widths(pulse))


def pulse_widths(pulse):
    widths, w = [], 0
    for p in pulse + [0]:
        if p:
            w += 1
        elif w:
            widths.append(w)
            w = 0
    return widths


def test_explorer_matches_replay():
    from page_tests import explorer_require, node_json

    rng = random.Random(1)
    cases = [[0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0], [1, 1, 0, 1], [0] * 12, [1] * 12, [0, 1] * 6]
    cases += [[rng.randrange(2) for _ in range(12)] for _ in range(200)]
    for mode in MODES:
        got = node_json(f"""
          const m = {explorer_require()};
          console.log(JSON.stringify({json.dumps(cases)}.map((s) => m.edgeTrace(s, {json.dumps(mode)}))));""")
        for sig, g in zip(cases, got):
            sig_q, pulse = replay(sig, mode)
            assert g["sigQ"] == sig_q and g["pulse"] == pulse, (sig, mode)
            assert g["phantom"] == (pulse[0] == 1)
            edges = sum(MODES[mode](sig[i], sig[i - 1]) for i in range(1, len(sig)))
            assert sum(g["edges"]) == edges
            # one high cycle per edge, plus the phantom pulse of the reset trap
            assert sum(pulse) == edges + g["phantom"]
            if mode != "both":
                assert all(w == 1 for w in pulse_widths(pulse))


def _fig():
    import sys

    from extract_code import ROOT

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import q0001

    return q0001


def test_schematic_matches_module():
    """The schematic's netlist (tools/figures/q0001.py) against the page's module: the
    flip-flop samples sig, resets to the page's value, and pulse is the page's assign; both
    simulated on random sig traces with the reset held in cycle 0."""
    q = _fig()
    page = question_path(1).read_text(encoding="utf-8")
    assert re.search(r"if \(!rst_n\) sig_q <= 1'b0;", page) and re.search(r"else\s+sig_q <= sig;", page)
    expr = re.search(r"assign pulse = (.+?);", page).group(1)
    assert q.NETLIST["sig_q"] == ("dff", "sig", "clk", "rst_n", 0)

    def page_pulse(sig, sig_q):                 # the assign, ~ on one bit
        return int(eval(expr.replace("~sig_q", "(1 - sig_q)"), {}, {"sig": sig, "sig_q": sig_q}))

    def net(sig, sig_q):
        vals = {"sig": sig, "sig_q": sig_q}
        for name, (kind, *ins) in q.NETLIST.items():
            if kind == "not":
                vals[name] = 1 - vals[ins[0]]
            elif kind == "and":
                vals[name] = vals[ins[0]] & vals[ins[1]]
        return vals["pulse"]

    rng = random.Random(11)
    for _ in range(200):
        sig = [rng.randrange(2) for _ in range(12)]
        sig_q, pulse = replay(sig, "rise")
        assert [net(s, p) for s, p in zip(sig, sig_q)] == [page_pulse(s, p) for s, p in zip(sig, sig_q)] == pulse
    svg = q.figure()
    for label in ("sig", "clk", "rst_n", "sig_q", "pulse", ">D<", ">Q<"):
        assert label in svg


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(1)
