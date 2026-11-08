"""Question 0001: the edge detector explorer against a Python replay of the module (sig_q
is the previous cycle's sig and 0 during reset; pulse = sig & ~sig_q, its mirror for a
falling edge, XOR for both) and against the page's own timing diagram; the figures of
tools/figures/q0001.py (the table of the four cases, the schematic and its follow-up
variants, the trap's synchronizer chain) simulated as netlists; the follow-up's registered
output; and the box's live circuit against the generator's figure, cycle by cycle."""

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


def _sim(netlist, sig):
    """Simulate a netlist of tools/figures/q0001.py on sig, cycle 0 being the reset cycle:
    every flip-flop holds its reset value in cycle 0, then the previous cycle's input."""
    regs = {n: spec[4] for n, spec in netlist.items() if spec[0] == "dff"}
    out = []
    for k, s in enumerate(sig):
        vals = {"sig": s, "rst_n": int(k > 0), **regs}
        for name, (kind, *ins) in netlist.items():
            if kind == "not":
                vals[name] = 1 - vals[ins[0]]
            elif kind == "and":
                vals[name] = vals[ins[0]] & vals[ins[1]]
            elif kind == "xor":
                vals[name] = vals[ins[0]] ^ vals[ins[1]]
        out.append(vals)
        regs = {n: vals[spec[1]] for n, spec in netlist.items() if spec[0] == "dff"}
    return out


def test_truth_table():
    """The page's table of the four cases (generated; test_figures_up_to_date checks the
    page's copy) against the formula."""
    q = _fig()
    rows = re.findall(r"^\| ‏([01]) \| ‏([01]) \| [^|]+ \| (?:\*\*)?‏([01])(?:\*\*)? \|$", q.truth_table(), re.M)
    assert sorted((int(s), int(sq)) for s, sq, _ in rows) == [(0, 0), (0, 1), (1, 0), (1, 1)]
    for s, sq, p in rows:
        assert int(p) == MODES["rise"](int(s), int(sq))


def test_follow_up_netlists():
    """The circuits of the follow-ups (falling edge, any edge) give the modes' pulse."""
    q = _fig()
    rng = random.Random(5)
    for mode, net in q.NETLISTS.items():
        for _ in range(100):
            sig = [rng.randrange(2) for _ in range(12)]
            assert [v["pulse"] for v in _sim(net, sig)] == replay(sig, mode)[1], mode


def test_sync_chain():
    """The trap's chain: two flip-flops, then the detector on sig_s, gives the plain
    detector's pulse two cycles later (from a reset where sig was 0)."""
    q = _fig()
    rng = random.Random(7)
    for _ in range(200):
        sig = [0, 0] + [rng.randrange(2) for _ in range(14)]
        got = [v["pulse"] for v in _sim(q.SYNC_NETLIST, sig)]
        assert got == [0, 0] + replay(sig, "rise")[1][:-2]
    svg = q.sync_figure()
    for label in ("sig", "clk", "meta", "sig_s", "sig_q", "pulse", "synchronizer", "edge detector"):
        assert f">{label}<" in svg
    assert svg.count('<rect class="ff-gate"') == 3


def test_registered_output():
    """The follow-up's registered output: pulse_q <= sig & ~sig_q is pulse one cycle later,
    the same as sig_q & ~sig_qq with sig_qq the second flip-flop of a chain."""
    page = question_path(1).read_text(encoding="utf-8")
    assert "`pulse_q <= sig & ~sig_q;`" in page and "`pulse_q = sig_q & ~sig_qq`" in page
    rng = random.Random(3)
    for _ in range(200):
        sig = [rng.randrange(2) for _ in range(12)]
        sig_q, pulse = replay(sig, "rise")
        pulse_q = [0] + pulse[:-1]
        sig_qq = [0] + sig_q[:-1]
        assert pulse_q == [a & (1 - b) for a, b in zip(sig_q, sig_qq)]


_GEOM = re.compile(r"<(polyline|path|circle|rect)\b([^>]*?)/>")
_ATTR = re.compile(r'\b(points|d|cx|cy|r|x|y|width|height|rx)="([^"]*)"')
_NUM = re.compile(r"-?\d+(?:\.\d+)?")


def _shapes(svg):
    """The shapes of a schematic in order: tag, base class and geometry (numbers normalised),
    and its texts but the box's values."""
    shapes = []
    for tag, attrs in _GEOM.findall(svg):
        cls = re.search(r'class="([\w-]+)', attrs).group(1)
        geo = [(a, _NUM.sub(lambda m: f"{float(m.group()):g}", v)) for a, v in _ATTR.findall(attrs)]
        shapes.append((tag, cls, geo))
    texts = [t for t in re.findall(r'<text class="([\w-]+)[^"]*" x="([\d.]+)" y="([\d.]+)"[^>]*>([^<]*)<', svg) if t[0] != "ed-val"]
    return shapes, texts


def test_box_circuit_matches_figure():
    """The box's live circuit (edge.js edgeDiagram) has the shapes and names of the
    generator's figure for each mode; on every cycle of random traces a wire is lit exactly
    when its net is 1 in the netlist's simulation, the gate when pulse is 1, and the
    flip-flop when it took a new value."""
    from page_tests import explorer_require, node_json

    q = _fig()
    rng = random.Random(9)
    traces = [[0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0], [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]]
    traces += [[rng.randrange(2) for _ in range(12)] for _ in range(20)]
    got = node_json(f"""
      const m = {explorer_require()};
      const out = {{}};
      for (const mode of ["rise", "fall", "both"]) {{
        out[mode] = {{ bare: m.edgeDiagram(mode, null),
          live: {json.dumps(traces)}.map((sig) => {{ const tr = m.edgeTrace(sig, mode);
            return sig.map((_, k) => ({{ v: m.edgeAt(sig, tr, k), svg: m.edgeDiagram(mode, m.edgeAt(sig, tr, k)) }})); }}) }};
      }}
      console.log(JSON.stringify(out));""")
    # the nets of each mode's wires, in the order the figure draws them (None: never lit)
    nets = {
        "rise": ["sig", "sig", None, "rst_n", "sig_q", "sig_q_n", "pulse"],
        "fall": ["sig", "sig_n", "sig", None, "rst_n", "sig_q", "pulse"],
        "both": ["sig", "sig", None, "rst_n", "sig_q", "pulse"],
    }
    for mode in ("rise", "fall", "both"):
        ref = _shapes(q.figure(mode))
        assert _shapes(got[mode]["bare"]) == ref, mode
        for sig, cycles in zip(traces, got[mode]["live"]):
            sim = _sim(q.NETLISTS[mode], sig)
            for k, c in enumerate(cycles):
                assert _shapes(c["svg"]) == ref
                vals = sim[k]
                assert (c["v"]["sig"], c["v"]["q"], c["v"]["pulse"], c["v"]["rst"]) == (sig[k], vals["sig_q"], vals["pulse"], vals["rst_n"])
                lines = re.findall(r'<polyline class="ff-wire( is-hi)?"', c["svg"])
                assert [bool(h) for h in lines] == [net is not None and vals[net] == 1 for net in nets[mode]], (mode, sig, k)
                gate = re.search(r'<path class="ff-gate( is-on)?" d="M408', c["svg"]) or re.search(r'<path class="ff-gate( is-on)?" d="M404', c["svg"])
                assert bool(gate.group(1)) == (vals["pulse"] == 1)
                took = k > 0 and sim[k]["sig_q"] != sim[k - 1]["sig_q"]
                assert ('<rect class="ff-gate is-on"' in c["svg"]) == took
                shown = re.findall(r'<text class="ed-val[^"]*"[^>]*>([01])<', c["svg"])
                assert len(shown) == {"rise": 5, "fall": 5, "both": 4}[mode]
