"""The tutorial video of question 0055, the divide-by-3 state machine (script: script.md).

Render with `python videos/render.py 0055` (see VIDEOS.md). No code is typed (the owner,
2026-11-01): in parts א and ב the machine is built from D flip-flops instead. Each part
draws the three states and their six edges, encodes them in two bits (00, 01, 10; 11 is a
don't care), fills the encoded transition table, reads the minimal equations off two
Karnaugh maps, and builds the circuit (the input and its complement, the flip-flops'
outputs on rails, AND and OR gates, two D flip-flops with an asynchronous reset to 00,
div = Q1'·Q0'), then steps the page's example through it cycle by cycle (a wire that
carries 1 is amber) and plays the page's divfsm box. Part א also shows the one weak spot
of the minimal equations: the unused state 11 stays 11 while b = 0, so the reset matters.
Part ג is short: the transitions for any m and base, and the box on 343 in base 10.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from manim import *  # noqa: E402,F403
from dvq import C, TX, BoxView, DVQScene, M, T, cost_chips  # noqa: E402

QID = 55
SCENES = [
    ("Opening", "פתיחה"),
    ("ChapterA", "סעיף א – הביטים מגיעים מה-MSB"),
    ("ChapterB", "סעיף ב – הביטים מגיעים מה-LSB"),
    ("ChapterC", "סעיף ג – כל m, כל בסיס, ו-k ביטים במחזור"),
    ("Closing", "סיכום"),
]

# The page's box (data-kind="divfsm", m = 3, one bit a cycle). "msb": 1101 (13) concatenated
# at the LSB, i.e. read from the MSB (part א), a picture before the first bit and after
# each bit. "lsb": 110 (6) concatenated at the MSB, read from the LSB (part ב). "dec" and
# "declsb": m = 7, one decimal digit a cycle, 343 read from each end (part ג).
BOXES = {
    "msb": {"box": 0, "width": 480, "region": [".dv-digits", ".dv-ring", ".dv-read"],
            "hide": [".dv-head"],
            "steps": [[["fill", ".dv-num", "1101"]], {"do": [["click", ".ex-next"]], "repeat": 4}]},
    "lsb": {"box": 0, "width": 480, "region": [".dv-digits", ".dv-ring", ".dv-read"],
            "hide": [".dv-head"],
            "steps": [[["set", ".dv-dir", "msb"], ["fill", ".dv-num", "110"]],
                      {"do": [["click", ".ex-next"]], "repeat": 3}]},
    "dec": {"box": 0, "width": 480, "region": [".dv-digits", ".dv-ring", ".dv-read"],
            "hide": [".dv-head"],
            "steps": [[["set", ".dv-m", "7"], ["set", ".dv-b", "10"], ["fill", ".dv-num", "343"]],
                      {"do": [["click", ".ex-next"]], "repeat": 3}]},
    "declsb": {"box": 0, "width": 480, "region": [".dv-digits", ".dv-ring", ".dv-read"],
               "hide": [".dv-head"],
               "steps": [[["set", ".dv-dir", "msb"], ["set", ".dv-m", "7"], ["set", ".dv-b", "10"],
                          ["fill", ".dv-num", "343"]],
                         {"do": [["click", ".ex-next"]], "repeat": 3}]},
}

# --------------------------------------------------------------------------------------
# The machines and their flip-flop implementation (checked against the definitions)
# --------------------------------------------------------------------------------------

ENC = {0: (0, 0), 1: (0, 1), 2: (1, 0)}           # state -> (Q1, Q0); 11 is unused
STATE = {v: k for k, v in ENC.items()}
NEXT = {"A": lambda r, b: (2 * r + b) % 3,       # part א: the remainder, bits from the MSB
        "B": lambda x, b: (2 * (x + b)) % 3}     # part ב: x = r * 2^-k, bits from the LSB

# The minimal sum-of-products terms (a literal "Q1'" is the complement), per flip-flop input.
TERMS = {
    "A": {"D1": [["Q0", "b'"], ["Q1", "b"]], "D0": [["Q1", "b'"], ["Q1'", "Q0'", "b"]]},
    "B": {"D1": [["Q0", "b'"], ["Q1'", "Q0'", "b"]], "D0": [["Q0", "b"], ["Q1", "b'"]]},
}
DIV = ["Q1'", "Q0'"]


def literals(q1: int, q0: int, b: int) -> dict:
    return {"b": b, "b'": 1 - b, "Q1": q1, "Q1'": 1 - q1, "Q0": q0, "Q0'": 1 - q0}


def evaluate(part: str, q1: int, q0: int, b: int) -> dict:
    """Every net of the circuit for the state (q1, q0) and the input b."""
    v = literals(q1, q0, b)
    out = dict(v)
    k = 0
    for d in ("D1", "D0"):
        acc = 0
        for term in TERMS[part][d]:
            t = int(all(v[x] for x in term))
            out[f"t{k}"] = t
            acc |= t
            k += 1
        out[d] = acc
    out["div"] = int(all(v[x] for x in DIV))
    return out


for _p in ("A", "B"):
    for _r in range(3):
        for _b in (0, 1):
            _e = evaluate(_p, *ENC[_r], _b)
            assert (_e["D1"], _e["D0"]) == ENC[NEXT[_p](_r, _b)], (_p, _r, _b)
        assert evaluate(_p, *ENC[_r], 0)["div"] == int(_r == 0)
assert (evaluate("A", 1, 1, 0)["D1"], evaluate("A", 1, 1, 0)["D0"]) == (1, 1)   # 11 stays 11


def run(part: str, bits: list[int]) -> list[int]:
    s, out = 0, []
    for b in bits:
        s = NEXT[part](s, b)
        out.append(s)
    return out


assert run("A", [1, 1, 0, 1]) == [1, 0, 0, 1]            # 13 = 1101 from the MSB: 1, 3, 6, 13
assert run("B", [0, 1, 1]) == [0, 2, 0]                  # 6 = 110 from the LSB: 0, 2, 6


def run_gen(digits: list[int], m: int, base: int, lsb: bool) -> list[int]:
    inv = pow(base, -1, m)
    s, out = 0, []
    for d in digits:
        s = (s + d) * inv % m if lsb else (s * base + d) % m
        out.append(s)
    return out


assert pow(10, -1, 7) == 5 and 10 % 7 == 3
assert run_gen([3, 4, 3], 7, 10, False) == [3, 6, 0]     # 3, 34, 343 from the MSB
assert run_gen([3, 4, 3], 7, 10, True) == [1, 4, 0]      # 3, 43, 343 from the LSB
assert 343 % 7 == 0 and 34 % 7 == 6 and 43 * pow(10, -2, 7) % 7 == 4

ON, OFF = C.AMBER, C.MUTED
BIT = {0: C.BLUE, 1: C.ORANGE}                           # the page's colours of the bits


def unit(v):
    return v / np.linalg.norm(v)


def rot(v, a):
    c, s = np.cos(a), np.sin(a)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], 0.0])


# --------------------------------------------------------------------------------------
# The state diagram
# --------------------------------------------------------------------------------------


class Machine(VGroup):
    """Three states on a triangle (0 on top, 1 lower right, 2 lower left, as in the page's
    box), state 0 with a double ring (div = 1). An edge per (state, bit), blue for 0 and
    orange for 1, drawn behind the states."""

    def __init__(self, centre=ORIGIN, r: float = 0.55, spread: float = 1.0):
        super().__init__()
        c = np.array(centre, dtype=float)
        self.r = r
        self.pos = {0: c + UP * 1.45 * spread, 1: c + (DOWN * 0.95 + RIGHT * 2.1) * spread,
                    2: c + (DOWN * 0.95 + LEFT * 2.1) * spread}
        self.mid = (self.pos[0] + self.pos[1] + self.pos[2]) / 3
        self.nodes = VGroup()
        for k in range(3):
            g = VGroup(Circle(radius=r, stroke_color=C.WHITE, stroke_width=4,
                              fill_color=C.NAVY_DARK, fill_opacity=1),
                       M(str(k), 44)).move_to(self.pos[k])
            if k == 0:
                g.add(Circle(radius=r - 0.1, stroke_color=C.WHITE, stroke_width=3).move_to(g))
            g.set_z_index(2)
            self.nodes.add(g)
        self.edges = {}
        self.add(self.nodes)

    def edge(self, s: int, t: int, b: int) -> VGroup:
        color = BIT[b]
        p, q, r = self.pos[s], self.pos[t], self.r
        if s == t:
            out = unit(p - self.mid)
            arrow = CurvedArrow(p + rot(out, 0.6) * r, p + rot(out, -0.6) * r, angle=-1.6 * PI,
                                color=color, stroke_width=5, tip_length=0.22)
            lab = M(str(b), 36, color).move_to(p + out * (r + 0.6) + rot(out, -PI / 2) * 1.0)
        else:
            d = unit(q - p)
            n = rot(d, -PI / 2)
            arrow = CurvedArrow(p + rot(d, -0.45) * r, q + rot(-d, 0.45) * r, angle=0.6,
                                color=color, stroke_width=5, tip_length=0.24)
            lab = M(str(b), 36, color).move_to(arrow.point_from_proportion(0.3) + n * 0.38)
        g = VGroup(arrow, lab)
        g.set_z_index(1)
        self.edges[(s, t, b)] = g
        return g

    def ring(self, k: int) -> Circle:
        return Circle(radius=self.r + 0.13, stroke_color=C.AMBER, stroke_width=7) \
            .move_to(self.pos[k]).set_z_index(3)

    def codes(self, size: float = 38) -> VGroup:
        """The two-bit code of each state, as a key on the right of the diagram."""
        rows = [M(f"{k}  ->  {ENC[k][0]}{ENC[k][1]}", size, C.GREEN) for k in range(3)]
        rows.append(M("    11  unused", size, C.MUTED))
        g = VGroup(*rows).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        return g.move_to([5.15, self.mid[1] + 1.55, 0])


def machine(part: str, centre=ORIGIN, spread: float = 1.0) -> Machine:
    m = Machine(centre, spread=spread)
    for s in range(3):
        for b in (0, 1):
            m.edge(s, NEXT[part](s, b), b)
    return m


# --------------------------------------------------------------------------------------
# The encoded table and the Karnaugh maps
# --------------------------------------------------------------------------------------


class Table(VGroup):
    """The encoded transition table: r, Q1Q0, b | r', D1D0, with the two rows of 11."""

    XS = [0.0, 1.25, 2.4, 3.5, 4.75]

    def __init__(self, part: str, size: float = 32, pitch: float = 0.46):
        super().__init__()
        nxt = "r'" if part == "A" else "x'"
        cols = ["r" if part == "A" else "x", "Q1Q0", "b", nxt, "D1D0"]
        self.head = VGroup(*[M(c, size, C.MUTED).move_to([x, 0, 0]) for c, x in zip(cols, self.XS)])
        self.rows = VGroup()
        for k, (s, b) in enumerate([(s, b) for s in range(3) for b in (0, 1)] + [(None, 0), (None, 1)]):
            y = -(k + 1) * pitch - (0.12 if s is None else 0)
            if s is None:
                cells = ["-", "11", str(b), "-", "xx"]
                color = C.MUTED
            else:
                t = NEXT[part](s, b)
                cells = [str(s), "%d%d" % ENC[s], str(b), str(t), "%d%d" % ENC[t]]
                color = C.WHITE
            row = VGroup(*[M(c, size, color).move_to([x, y, 0]) for c, x in zip(cells, self.XS)])
            self.rows.add(row)
        top, bottom = 0.3, -8 * pitch - 0.35
        self.rule = Line([2.95, top, 0], [2.95, bottom, 0], stroke_color=C.FAINT, stroke_width=2)
        self.hline = Line([-0.45, -pitch / 2, 0], [5.45, -pitch / 2, 0], stroke_color=C.FAINT,
                          stroke_width=2)
        self.add(self.head, self.hline, self.rule, self.rows)


GRAY = [(0, 0), (0, 1), (1, 1), (1, 0)]


class KMap(VGroup):
    """A Karnaugh map of one flip-flop input: rows Q1Q0 in Gray order, columns b."""

    def __init__(self, part: str, which: str, cw: float = 0.8, ch: float = 0.58, size: float = 32):
        super().__init__()
        self.cw, self.ch = cw, ch
        idx = 0 if which == "D1" else 1
        self.cells = {}
        grid = VGroup()
        for i, (q1, q0) in enumerate(GRAY):
            for j in (0, 1):
                box = Rectangle(width=cw, height=ch, stroke_color=C.FAINT, stroke_width=2) \
                    .move_to([j * cw, -i * ch, 0])
                if (q1, q0) == (1, 1):
                    val = M("x", size, C.MUTED)
                else:
                    t = NEXT[part](STATE[(q1, q0)], j)
                    v = ENC[t][idx]
                    val = M(str(v), size, C.AMBER if v else C.WHITE)
                val.move_to(box)
                self.cells[(i, j)] = box
                grid.add(VGroup(box, val))
        self.grid = grid
        self.rlabels = VGroup(*[M(f"{q1}{q0}", 28, C.MUTED).next_to(self.cells[(i, 0)], LEFT, buff=0.15)
                                for i, (q1, q0) in enumerate(GRAY)])
        self.clabels = VGroup(*[M(str(j), 28, C.MUTED).next_to(self.cells[(0, j)], UP, buff=0.12)
                                for j in (0, 1)])
        self.bname = M("b", 28, C.MUTED).next_to(self.clabels, UP, buff=0.08)
        self.qname = M("Q1Q0", 28, C.MUTED).next_to(self.rlabels[0], UP, buff=0.35)
        self.title = M(which, 36, C.GREEN).next_to(VGroup(self.bname, self.qname), UP, buff=0.2)
        self.add(self.grid, self.rlabels, self.clabels, self.bname, self.qname, self.title)

    def group(self, rows: list[int], col: int, color: str) -> RoundedRectangle:
        a, b = self.cells[(rows[0], col)], self.cells[(rows[-1], col)]
        g = RoundedRectangle(width=self.cw - 0.12, height=abs(a.get_y() - b.get_y()) + self.ch - 0.12,
                             corner_radius=0.18, stroke_color=color, stroke_width=5)
        return g.move_to((a.get_center() + b.get_center()) / 2)


# --------------------------------------------------------------------------------------
# The circuit: rails, AND and OR gates, two D flip-flops
# --------------------------------------------------------------------------------------

RAILS = ["b", "b'", "Q1", "Q1'", "Q0", "Q0'"]
RAIL_X = {n: -6.45 + 0.7 * k for k, n in enumerate(RAILS)}
RAIL_TOP, RAIL_BOTTOM, LABEL_Y = 3.15, -2.2, 3.5
AND_X = -1.95
AND_Y = [2.35, 1.4, 0.15, -0.8, -1.8]          # the D1 terms, the D0 terms, div
OR_X = -0.25
OR_Y = {"D1": 1.875, "D0": -0.325}
FF_X = 2.45
FF_Y = {"D1": 1.525, "D0": -0.675}             # the D pin at y + 0.35
WIRE = dict(stroke_color=OFF, stroke_width=4)


def and_gate(x0: float, y: float, h: float = 0.72) -> VGroup:
    body = VGroup(Line([x0, y + h / 2, 0], [x0 + 0.4, y + h / 2, 0]),
                  ArcBetweenPoints([x0 + 0.4, y + h / 2, 0], [x0 + 0.4, y - h / 2, 0], angle=-PI),
                  Line([x0 + 0.4, y - h / 2, 0], [x0, y - h / 2, 0]),
                  Line([x0, y - h / 2, 0], [x0, y + h / 2, 0]))
    return body.set_stroke(C.WHITE, 4)


def or_gate(x0: float, y: float, h: float = 0.72, w: float = 0.9) -> VGroup:
    top, bot, tip = np.array([x0, y + h / 2, 0]), np.array([x0, y - h / 2, 0]), np.array([x0 + w, y, 0])
    body = VGroup(ArcBetweenPoints(top, bot, angle=-0.7),
                  ArcBetweenPoints(top, tip, angle=-0.55),
                  ArcBetweenPoints(bot, tip, angle=0.55))
    return body.set_stroke(C.WHITE, 4)


def not_gate_down(x: float, y0: float) -> VGroup:
    """A NOT gate pointing down, its input at (x, y0)."""
    tri = Polygon([x - 0.2, y0, 0], [x + 0.2, y0, 0], [x, y0 - 0.34, 0], stroke_color=C.WHITE,
                  stroke_width=4, fill_color=C.NAVY, fill_opacity=1)
    bubble = Circle(radius=0.07, stroke_color=C.WHITE, stroke_width=4, fill_color=C.NAVY,
                    fill_opacity=1).move_to([x, y0 - 0.41, 0])
    return VGroup(tri, bubble)


class Circuit(VGroup):
    """The machine of part `part` in gates and D flip-flops, about 13 wide, from y = 3.6
    down to -2.2. Nets are VGroups of wires (`self.nets[name]`) so a net's value can be
    shown by its colour; the flip-flops show their bit, div its value."""

    def __init__(self, part: str):
        super().__init__()
        self.part = part
        self.nets = {n: VGroup() for n in RAILS + ["t0", "t1", "t2", "t3", "div", "D1", "D0"]}
        dots = VGroup()
        self.rail_lines, self.in_wires, self.stubs, self.in_dots = VGroup(), VGroup(), VGroup(), VGroup()
        # the rails (b' starts under its NOT gate) and their names
        for n in RAILS:
            top = 2.52 if n == "b'" else RAIL_TOP
            line = Line([RAIL_X[n], top, 0], [RAIL_X[n], RAIL_BOTTOM, 0], **WIRE)
            self.nets[n].add(line)
            self.rail_lines.add(line)
        self.rail_names = VGroup(*[M(n, 28, C.WHITE if n in ("b", "b'") else C.GREEN)
                                   .move_to([RAIL_X[n], LABEL_Y, 0]) for n in RAILS])
        tap_y = 3.0
        tap = Line([RAIL_X["b"], tap_y, 0], [RAIL_X["b'"], tap_y, 0], **WIRE)
        self.nets["b"].add(tap)
        self.rail_lines.add(tap)
        dots.add(Dot([RAIL_X["b"], tap_y, 0], radius=0.07, color=C.WHITE))
        self.inv = not_gate_down(RAIL_X["b'"], tap_y)
        # the AND gates and their inputs
        terms = TERMS[part]["D1"] + TERMS[part]["D0"] + [DIV]
        self.ands = VGroup()
        self.inputs = VGroup()
        for k, (term, y) in enumerate(zip(terms, AND_Y)):
            self.ands.add(and_gate(AND_X, y))
            offs = [0.17, -0.17] if len(term) == 2 else [0.22, 0.0, -0.22]
            for lit, dy in zip(term, offs):
                w = Line([RAIL_X[lit], y + dy, 0], [AND_X, y + dy, 0], **WIRE)
                self.nets[lit].add(w)
                self.in_wires.add(w)
                self.in_dots.add(Dot([RAIL_X[lit], y + dy, 0], radius=0.07, color=C.WHITE))
        # AND outputs to the OR gates; div out
        ax = AND_X + 0.76
        for k, d in enumerate(["D1", "D1", "D0", "D0"]):
            y = AND_Y[k]
            yin = OR_Y[d] + (0.17 if k % 2 == 0 else -0.17)
            self.nets[f"t{k}"].add(VMobject(**WIRE).set_points_as_corners(
                [[ax, y, 0], [OR_X - 0.45, y, 0], [OR_X - 0.45, yin, 0], [OR_X + 0.1, yin, 0]]))
        self.nets["div"].add(Line([ax, AND_Y[4], 0], [ax + 0.75, AND_Y[4], 0], **WIRE))
        self.div_label = M("div", 34, C.GREEN).move_to([ax + 1.2, AND_Y[4], 0])
        self.ors = VGroup(*[or_gate(OR_X, OR_Y[d]) for d in ("D1", "D0")])
        # the flip-flops
        self.ffs, self.ff_text, self.ff_vals = VGroup(), VGroup(), {}
        self.outs = VGroup()
        for d, q in (("D1", "Q1"), ("D0", "Q0")):
            cy = FF_Y[d]
            box = Rectangle(width=1.4, height=1.5, stroke_color=C.WHITE, stroke_width=4,
                            fill_color=C.NAVY_LIGHT, fill_opacity=1).move_to([FF_X, cy, 0])
            left, right = FF_X - 0.7, FF_X + 0.7
            self.nets[d].add(Line([OR_X + 0.9, OR_Y[d], 0], [left, cy + 0.35, 0], **WIRE))
            notch = Polygon([left, cy - 0.17, 0], [left, cy - 0.53, 0], [left + 0.24, cy - 0.35, 0],
                            stroke_color=C.MUTED, stroke_width=3)
            clk = VGroup(Line([left - 0.35, cy - 0.35, 0], [left, cy - 0.35, 0], stroke_color=C.MUTED,
                              stroke_width=3),
                         M("clk", 28, C.MUTED).move_to([left - 0.75, cy - 0.35, 0]))
            rst = VGroup(Line([FF_X, cy - 0.75, 0], [FF_X, cy - 0.97, 0], stroke_color=C.MUTED,
                              stroke_width=3),
                         M("rst_n", 28, C.MUTED).move_to([FF_X + 0.78, cy - 0.98, 0]))
            pins = VGroup(M("D", 28, C.MUTED).move_to([left + 0.2, cy + 0.35, 0]),
                          M("Q", 28, C.MUTED).move_to([right - 0.2, cy + 0.35, 0]),
                          M("Q'", 28, C.MUTED).move_to([right - 0.25, cy - 0.35, 0]))
            name = M("FF1" if d == "D1" else "FF0", 28, C.MUTED).next_to(box, UP, buff=0.08)
            self.ffs.add(VGroup(box, notch, pins, name))
            self.ff_text.add(VGroup(clk, rst))
            for name, dy in ((q, 0.35), (q + "'", -0.35)):
                stub = Line([right, cy + dy, 0], [right + 0.45, cy + dy, 0], **WIRE)
                self.nets[name].add(stub)
                self.stubs.add(stub)
            self.outs.add(M(q, 30, C.GREEN).move_to([right + 0.85, cy + 0.35, 0]),
                          M(q + "'", 30, C.GREEN).move_to([right + 0.9, cy - 0.35, 0]))
            self.ff_vals[q] = M("0", 46, C.AMBER, weight="BOLD").move_to([FF_X, cy - 0.02, 0])
        self.dots = dots
        self.wires = VGroup(*self.nets.values())
        self.add(self.wires, dots, self.in_dots, self.inv, self.ands, self.ors, self.ffs, self.ff_text, self.outs,
                 self.rail_names, self.div_label)
        self.div_val = M("1", 40, C.AMBER, weight="BOLD").next_to(self.div_label, RIGHT, buff=0.25)

    def colour(self, values: dict) -> list:
        """The animations that colour every net by its value (1 amber, 0 muted)."""
        return [self.nets[n].animate.set_stroke(ON if values[n] else OFF)
                for n in self.nets if n in values]


# --------------------------------------------------------------------------------------
# Shared scene helpers
# --------------------------------------------------------------------------------------


class FsmScene(DVQScene):

    def value(self, old: Mobject, text: str, color: str = C.AMBER, size: float = 46):
        new = M(text, size, color, weight="BOLD").move_to(old)
        return Transform(old, new)

    def bits_panel(self, bits: list[int], x: float, y: float, side: float = 0.6) -> VGroup:
        cells = VGroup()
        for b in bits:
            box = RoundedRectangle(width=side * 0.9, height=side, corner_radius=0.1, stroke_color=C.MUTED,
                                   stroke_width=2.5, fill_color=C.NAVY_LIGHT, fill_opacity=1)
            cells.add(VGroup(box, M(str(b), 34 * side / 0.6, BIT[b]).move_to(box)))
        return cells.arrange(RIGHT, buff=0.1).move_to([x, y, 0])

    def diagram(self, part: str, centre, caption_nodes: str, caption_edges: list[tuple],
                spread: float = 1.2) -> Machine:
        """The three states, then the edges of each state under its caption."""
        mc = machine(part, centre, spread)
        self.say(caption_nodes, FadeIn(mc.nodes, lag_ratio=0.2), run_time=1.2)
        for states, caption in caption_edges:
            edges = [g for (s, t, b), g in mc.edges.items() if s in states]
            self.say(caption, *[Create(g[0]) for g in edges], *[FadeIn(g[1]) for g in edges],
                     run_time=1.4)
        return mc

    def kmaps(self, part: str, groups: dict, captions: list[str], eqs: list[str]):
        """The table on the left, the two maps on the right, their groups circled."""
        tb = Table(part, size=36, pitch=0.52).to_edge(LEFT, buff=0.5)
        tb.shift(UP * (3.2 - tb.get_top()[1]))
        k1 = KMap(part, "D1", cw=0.95, ch=0.66, size=36).move_to([2.2, 1.45, 0])
        k0 = KMap(part, "D0", cw=0.95, ch=0.66, size=36).move_to([5.45, 1.45, 0])
        self.say(captions[0], FadeIn(tb.head), Create(tb.hline), Create(tb.rule),
                 FadeIn(tb.rows[:6], lag_ratio=0.15), run_time=2.0)
        self.say(captions[1], FadeIn(tb.rows[6:]))
        self.say(captions[2], FadeIn(k1), FadeIn(k0), run_time=1.2)
        rings1 = VGroup(*[k1.group(rows, col, color) for rows, col, color in groups["D1"]])
        e1 = TX(eqs[0], size=44, color=C.WHITE).next_to(VGroup(k1, k0), DOWN, buff=0.45)
        self.say(captions[3], Create(rings1), Write(e1), run_time=1.6)
        rings0 = VGroup(*[k0.group(rows, col, color) for rows, col, color in groups["D0"]])
        e0 = TX(eqs[1], size=44, color=C.WHITE).next_to(e1, DOWN, buff=0.3)
        self.say(captions[4], Create(rings0), Write(e0), run_time=1.6)
        return tb, k1, k0, e1, e0

    def build(self, cc: Circuit, captions: list[str]):
        """The circuit in four beats: the rails, the AND gates, the ORs, the flip-flops."""
        self.say(captions[0], Create(cc.rail_lines), FadeIn(cc.dots), FadeIn(cc.inv),
                 FadeIn(cc.rail_names), run_time=1.8)
        self.say(captions[1], Create(cc.in_wires), FadeIn(cc.in_dots), Create(cc.ands[:4]),
                 *[Create(cc.nets[f"t{k}"]) for k in range(4)], run_time=1.8)
        self.say(captions[2], Create(cc.ors), Create(cc.nets["D1"]), Create(cc.nets["D0"]),
                 run_time=1.4)
        self.say(captions[3], FadeIn(cc.ffs), FadeIn(cc.ff_text), FadeIn(cc.outs), Create(cc.stubs),
                 FadeIn(cc.ff_vals["Q1"]), FadeIn(cc.ff_vals["Q0"]), run_time=1.4)
        self.say(captions[4], Create(cc.ands[4]), Create(cc.nets["div"]), FadeIn(cc.div_label),
                 FadeIn(cc.div_val),
                 *cc.colour(evaluate(cc.part, 0, 0, 0)), run_time=1.2)

    def step(self, cc: Circuit, state: list, b: int, panel: VGroup, k: int, info: dict,
             caption_in: str, caption_edge: str):
        """One cycle: the bit arrives (the nets settle, D shows the next state), then the
        clock edge (the flip-flops take D, Q and div follow)."""
        q1, q0 = state
        v = evaluate(cc.part, q1, q0, b)
        mark = SurroundingRectangle(panel[k], color=C.AMBER, buff=0.06, stroke_width=5)
        self.say(caption_in, Create(mark), *cc.colour(v), run_time=1.2)
        n1, n0 = v["D1"], v["D0"]
        after = evaluate(cc.part, n1, n0, b)
        flash = [Indicate(cc.ffs[0][0], color=C.AMBER, scale_factor=1.05),
                 Indicate(cc.ffs[1][0], color=C.AMBER, scale_factor=1.05)]
        texts = [self.value(cc.ff_vals["Q1"], str(n1)), self.value(cc.ff_vals["Q0"], str(n0)),
                 self.value(cc.div_val, str(after["div"]), size=40)]
        for name, val in info.items():
            texts.append(self.value(name, val, C.WHITE, 36))
        self.say(caption_edge, *flash, *texts, *cc.colour(after), run_time=1.2)
        self.play(FadeOut(mark), run_time=0.3)
        state[0], state[1] = n1, n0


# --------------------------------------------------------------------------------------
# The scenes
# --------------------------------------------------------------------------------------


class Opening(FsmScene):
    def construct(self):
        self.opening(QID, "ג'וניור", "מכונת מצבים לחלוקה ב-3",
                     ["א · מה-MSB", "ב · מה-LSB", "ג · כל m וכל בסיס"],
                     ["שאלה 0055 : מכונת מצבים לחלוקה ב-3,\nשאלה ברמת ג'וניור.",
                      "שלושה סעיפים : ביטים מה-MSB, ביטים מה-LSB,\nואז כל m וכל בסיס."])
        self.fade_all()
        panel = self.bits_panel([1, 1, 0], 0.6, 1.9, side=1.0)
        panel.arrange(RIGHT, buff=0.5).move_to([0.6, 1.9, 0])
        nums = VGroup(*[M(s, 52, C.WHITE).next_to(panel[k], DOWN, buff=0.6)
                        for k, s in enumerate(["1", "3", "6"])])
        divs = VGroup(*[M(s, 52, C.AMBER if s == "1" else C.MUTED).next_to(nums[k], DOWN, buff=0.6)
                        for k, s in enumerate(["0", "1", "1"])])
        names = VGroup(*[M(n, 44, C.MUTED).move_to([0, row.get_y(), 0])
                         for n, row in zip(["din", "v", "div"], [panel, nums, divs])])
        for n in names:
            n.align_to([panel.get_left()[0] - 0.7, 0, 0], RIGHT)
        self.say("בכל מחזור שעון נכנס ביט אחד, din.\nהמספר יכול להיות ארוך כרצוננו.",
                 FadeIn(panel, lag_ratio=0.3), FadeIn(names[0]), run_time=1.4)
        self.say("אחרי כל ביט, div אומר אם המספר\nשנקרא עד עכשיו מתחלק ב-3.",
                 FadeIn(nums, lag_ratio=0.3), FadeIn(divs, lag_ratio=0.3), FadeIn(names[1:]),
                 run_time=1.4)
        self.fade_all()


class ChapterA(FsmScene):
    def construct(self):
        self.chapter_card("סעיף א", "הביטים מגיעים מה-MSB",
                          "סעיף א : הביט החדש הוא הביט הנמוך\nשל המספר, כמו בקריאה רגילה.")
        self.idea()
        mc = self.states()
        self.encode(mc)
        self.equations()
        cc = self.circuit()
        self.simulate(cc)
        self.unused(cc)
        self.box()
        self.cost()

    def idea(self):
        v = TX(r"v \;\to\; 2v + b", size=56).move_to(UP * 1.6)
        r = TX(r"r' = (2r + b) \bmod 3", size=56, color=C.AMBER).move_to(DOWN * 0.2)
        self.say("ביט חדש מכפיל את המספר ב-2\nומוסיף את הביט : v הופך ל-2v + b.", Write(v))
        self.say("את v אי אפשר לשמור. אבל השארית\nשל 2v + b תלויה רק בשארית של v.", Write(r))
        self.say("לכן המצב הוא השארית r : 0, 1 או 2.\nשלושה מצבים, ו-div דולק כש-r = 0.")
        self.fade_all()

    def states(self) -> Machine:
        mc = self.diagram("A", DOWN * 0.05, "שלושת המצבים. המצב 0 בעיגול כפול :\nשם המספר מתחלק, ו-div = 1.", [
            ([0], "ממצב 0 : הביט 0 משאיר אותו ב-0,\nוהביט 1 מעביר ל-1."),
            ([1], "ממצב 1 : 2 · 1 + 0 = 2, ו-2 · 1 + 1 = 3,\nשהוא 0. לכן ל-2 או ל-0."),
            ([2], "ממצב 2 : 4 שהוא 1, ו-5 שהוא 2.\nשישה מעברים בסך הכול."),
        ])
        ring = mc.ring(0)
        panel = self.bits_panel([1, 1, 0, 1], 4.9, 3.1)
        self.say("הדוגמה מהעמוד : 13, כלומר 1101,\nמגיע ביט אחרי ביט. מתחילים ב-0.",
                 FadeIn(panel, lag_ratio=0.2), Create(ring))
        path = [0] + run("A", [1, 1, 0, 1])
        caps = ["הביט 1 : המספר 1, שארית 1.", "הביט 1 : המספר 3, שארית 0. div = 1.",
                "הביט 0 : המספר 6, שארית 0. div = 1.", "הביט 1 : המספר 13, שארית 1."]
        for k in range(4):
            new = mc.ring(path[k + 1])
            mark = SurroundingRectangle(panel[k], color=C.AMBER, buff=0.06, stroke_width=5)
            self.say(caps[k], Create(mark), Transform(ring, new), run_time=1.0)
            self.remove(mark)
        self.play(FadeOut(ring), FadeOut(panel), run_time=0.5)
        self.mc = mc
        return mc

    def encode(self, mc: Machine):
        codes = mc.codes()
        self.say("עכשיו לחומרה. שלושה מצבים הם שני ביטים,\n‏Q1 ו-Q0 : 0 הוא 00, 1 הוא 01, 2 הוא 10.",
                 FadeIn(codes, lag_ratio=0.3))
        self.say("הקוד 11 לא בשימוש. בטבלאות הוא\n‏Don't care : אפשר לבחור בו מה שנוח.")
        self.fade_all()

    def equations(self):
        groups = {"D1": [([1, 2], 0, C.AMBER), ([2, 3], 1, C.GREEN)],
                  "D0": [([2, 3], 0, C.AMBER), ([0], 1, C.GREEN)]}
        self.eqs = self.kmaps("A", groups, [
            "טבלת המעברים עם הקידוד : כל מצב וביט,\nוהמצב הבא, שהוא הכניסה D1D0.",
            "ושתי שורות של 11 : לא מגיעים אליהן,\nולכן המצב הבא שלהן xx.",
            "מפת קרנו לכל כניסה של Flip-Flop :\nהשורות Q1Q0 בסדר Gray, והעמודות b.",
            "‏D1 : שתי קבוצות, בעזרת ה-x.\n‏Q0·b' ועוד Q1·b.",
            "‏D0 : Q1·b' ועוד תא בודד,\n‏Q1'·Q0'·b, שאין לו שכן.",
        ], [r"D_1 = Q_0\,\overline{b} + Q_1\,b",
            r"D_0 = Q_1\,\overline{b} + \overline{Q_1}\,\overline{Q_0}\,b"])
        tb, k1, k0, e1, e0 = self.eqs
        div = TX(r"\mathit{div} = \overline{Q_1}\,\overline{Q_0}", size=40, color=C.AMBER) \
            .next_to(e0, DOWN, buff=0.3)
        self.say("והיציאה תלויה רק במצב : div דולק\nב-00, כלומר div = Q1'·Q0'.", Write(div))
        self.fade_all()

    def circuit(self) -> Circuit:
        cc = Circuit("A")
        self.build(cc, [
            "המעגל. משמאל המסילות : b, ההיפוך שלו\nדרך שער NOT, וארבעת המוצאים של המצב.",
            "שער AND לכל מכפלה של המשוואות,\nונקודה מסמנת חיבור למסילה.",
            "שערי OR מחברים את המכפלות\nלכניסות D1 ו-D0.",
            "שני Flip-Flops מסוג D, עם שעון ואיפוס\nאסינכרוני ל-00. Q ו-Q' חוזרים למסילות.",
            "ושער AND אחרון : div = Q1'·Q0'.\nחוט כתום נושא 1, חוט אפור נושא 0.",
        ])
        return cc

    def simulate(self, cc: Circuit):
        panel = self.bits_panel([1, 1, 0, 1], 5.85, 0.65)
        vlab = M("v = 0", 36, C.WHITE).move_to([5.85, -0.05, 0])
        self.say("אחרי האיפוס המצב 00 ו-div = 1 :\nהמספר 0 מתחלק. עכשיו 1101.",
                 FadeIn(panel, lag_ratio=0.2), FadeIn(vlab))
        state = [0, 0]
        steps = [
            ("הביט 1 : Q1'·Q0'·b דולק,\nולכן D0 = 1 ו-D1 = 0. המצב הבא 01.",
             "עליית שעון : המצב 01, כלומר שארית 1.\n‏div = 0, כי 1 לא מתחלק."),
            ("שוב הביט 1. עכשיו אף מכפלה לא דולקת :\n‏D1D0 = 00.",
             "המצב 00 ו-div = 1 : המספר 3 מתחלק."),
            ("הביט 0 במצב 00 : כל המכפלות כבויות,\nוהמצב נשאר 00.",
             "המספר 6, ו-div נשאר 1."),
            ("הביט 1 במצב 00 : שוב Q1'·Q0'·b,\nוהמצב הבא 01.",
             "המספר 13 : שארית 1, ו-div = 0.\nבדיוק כמו בדיאגרמה."),
        ]
        vals = ["v = 1", "v = 3", "v = 6", "v = 13"]
        for k, (b, (c1, c2)) in enumerate(zip([1, 1, 0, 1], steps)):
            self.step(cc, state, b, panel, k, {vlab: vals[k]}, c1, c2)
        self.cleanup = [panel, vlab]

    def unused(self, cc: Circuit):
        bad = [self.value(cc.ff_vals["Q1"], "1", C.RED), self.value(cc.ff_vals["Q0"], "1", C.RED)]
        self.say("מה אם הפליפ-פלופים מתחילים ב-11?\nעם b = 0 : D1 = Q0·b' = 1, וגם D0 = 1.",
                 *bad, *cc.colour(evaluate("A", 1, 1, 0)), run_time=1.2)
        self.say("המצב 11 נשאר 11 כל עוד b = 0, ו-div\nתקוע ב-0. לכן האיפוס ל-00 חשוב.")
        self.fade_all()

    def box(self):
        view = BoxView(QID, "msb", height=5.7).move_to(UP * 0.62)
        self.say("וכך זה נראה בתיבה שבעמוד,\nעל אותו 1101.", FadeIn(view))
        self.box_beat(view, [
            (1, "הביט 1 : מ-0 ל-1, בחץ הכתום."),
            (2, "הביט 1 : מ-1 ל-0. ‏3 מתחלק."),
            (3, "הביט 0 : נשארים ב-0. ‏6 מתחלק."),
            (4, "הביט 1 : ל-1. ‏13 לא מתחלק."),
        ])
        self.fade_all()

    def cost(self):
        chips = cost_chips(("flip-flops", "2"), ("AND / OR", "5 / 2"), ("NOT", "1"),
                           notes=("three states", "the equations", "b'"))
        self.say("העלות : שני Flip-Flops, חמישה שערי AND,\nשני OR ו-NOT אחד, בלי קשר לאורך המספר.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()


class ChapterB(FsmScene):
    def construct(self):
        self.chapter_card("סעיף ב", "הביטים מגיעים מה-LSB",
                          "סעיף ב : הביט החדש הוא הביט הגבוה\nשל המספר. 6 = 110 מגיע כ-0, 1, 1.")
        self.idea()
        self.states()
        self.equations()
        cc = self.circuit()
        self.simulate(cc)
        self.box()
        self.cost()

    def idea(self):
        add = TX(r"v \;\to\; v + b \cdot 2^k", size=52).move_to(UP * 2.0)
        self.say("עכשיו הביט ה-k מוסיף b · 2^k, ו-2^k\nמודולו 3 מתחלף : 1, 2, 1, 2.", Write(add))
        naive = M("(r, k mod 2)  ->  6 states", 38, C.MUTED).move_to(UP * 0.8)
        self.say("הניסיון הראשון : לשמור את השארית\nוגם את הזוגיות של k. שישה מצבים.", FadeIn(naive))
        x = TX(r"x = r \cdot 2^{-k} \bmod 3", size=48, color=C.WHITE).move_to(DOWN * 0.35)
        xn = TX(r"x' = 2\,(x + b) \bmod 3", size=52, color=C.AMBER).move_to(DOWN * 1.5)
        self.say("אבל העתיד תלוי רק ב-x = r · 2^-k.\nב-3 הפכי של 2 הוא 2.", Write(x))
        self.say("ואז x' = 2(x + b) mod 3 : המיקום k נעלם.\nשוב שלושה מצבים, ו-div דולק כש-x = 0.",
                 Write(xn))
        self.fade_all()

    def states(self):
        mc = self.diagram("B", DOWN * 0.05, "שוב שלושה מצבים, עם מעברים אחרים.\nהמצב 0 בעיגול כפול.", [
            ([0], "ממצב 0 : הביט 0 נשאר ב-0,\nוהביט 1 נותן 2 · 1 = 2."),
            ([1], "ממצב 1 : 2 · 1 = 2, ו-2 · 2 = 4,\nשהוא 1. לכן ל-2 או ל-1."),
            ([2], "ממצב 2 : 2 · 2 = 4 שהוא 1,\nו-2 · 3 = 6 שהוא 0."),
        ])
        codes = mc.codes()
        self.say("זו המכונה של סעיף א, עם 1 ו-2\nבתפקידים הפוכים. אותו קידוד : 00, 01, 10.",
                 FadeIn(codes, lag_ratio=0.3))
        self.fade_all()

    def equations(self):
        groups = {"D1": [([1, 2], 0, C.AMBER), ([0], 1, C.GREEN)],
                  "D0": [([1, 2], 1, C.AMBER), ([2, 3], 0, C.GREEN)]}
        self.eqs = self.kmaps("B", groups, [
            "הטבלה המקודדת של סעיף ב : x, הביט,\nוהמצב הבא x' = 2(x + b) mod 3.",
            "ושוב 11 הוא Don't care.",
            "שתי מפות קרנו, באותו סדר Gray.",
            "‏D1 : Q0·b' בעזרת ה-x,\nועוד התא הבודד Q1'·Q0'·b.",
            "‏D0 : Q0·b ועוד Q1·b'.\nאותן מכפלות, רק במקומות אחרים.",
        ], [r"D_1 = Q_0\,\overline{b} + \overline{Q_1}\,\overline{Q_0}\,b",
            r"D_0 = Q_0\,b + Q_1\,\overline{b}"])
        tb, k1, k0, e1, e0 = self.eqs
        div = TX(r"\mathit{div} = \overline{Q_1}\,\overline{Q_0}", size=40, color=C.AMBER) \
            .next_to(e0, DOWN, buff=0.3)
        self.say("והיציאה כמו בסעיף א : div = Q1'·Q0',\nכי x = 0 בדיוק כשהמספר מתחלק.", Write(div))
        self.fade_all()

    def circuit(self) -> Circuit:
        cc = Circuit("B")
        self.build(cc, [
            "אותן מסילות : b ו-b', ו-Q1, Q1', Q0, Q0'\nשחוזרים מהפליפ-פלופים.",
            "ארבעה שערי AND למכפלות של סעיף ב.",
            "שני OR, ל-D1 ול-D0.",
            "אותם שני Flip-Flops, עם איפוס ל-00.\nגם כאן 11 נשאר 11 כש-b = 0.",
            "‏div = Q1'·Q0', כמו קודם.",
        ])
        return cc

    def simulate(self, cc: Circuit):
        panel = self.bits_panel([0, 1, 1], 5.85, 0.65)
        vlab = M("v = 0", 36, C.WHITE).move_to([5.85, -0.05, 0])
        self.say("עכשיו 6 = 110, מה-LSB : 0, 1, 1.\nאחרי האיפוס x = 0.",
                 FadeIn(panel, lag_ratio=0.2), FadeIn(vlab))
        state = [0, 0]
        steps = [
            ("הביט 0 במצב 00 : אף מכפלה לא דולקת,\nוהמצב הבא 00.",
             "המספר 0 מתחלק : div = 1."),
            ("הביט 1 : Q1'·Q0'·b דולק,\nולכן D1 = 1. המצב הבא 10.",
             "‏x = 2 : המספר 2 לא מתחלק, div = 0."),
            ("הביט 1 במצב 10 : Q1·b' כבוי, ו-Q0·b כבוי.\nהמצב הבא 00.",
             "‏x = 0 : המספר 6 מתחלק, div = 1."),
        ]
        vals = ["v = 0", "v = 2", "v = 6"]
        for k, (b, (c1, c2)) in enumerate(zip([0, 1, 1], steps)):
            self.step(cc, state, b, panel, k, {vlab: vals[k]}, c1, c2)
        self.fade_all()

    def box(self):
        view = BoxView(QID, "lsb", height=5.7).move_to(UP * 0.62)
        self.say("בתיבה בוחרים שרשור ל-MSB : הספרה\nהחדשה נכנסת משמאל. שוב 110.", FadeIn(view))
        self.box_beat(view, [
            (1, "הביט 0 : נשארים ב-0."),
            (2, "הביט 1 : ל-2. המספר 2."),
            (3, "הביט 1 : חזרה ל-0. ‏6 מתחלק."),
        ])
        self.fade_all()

    def cost(self):
        chips = cost_chips(("flip-flops", "2"), ("AND / OR", "5 / 2"), ("NOT", "1"),
                           notes=("three states", "the equations", "b'"))
        self.say("אותה עלות בדיוק : גם מה-LSB\nמספיקים שלושה מצבים ושני Flip-Flops.",
                 FadeIn(chips, lag_ratio=0.3))
        self.fade_all()


class ChapterC(FsmScene):
    def construct(self):
        self.chapter_card("סעיף ג", "כל m, כל בסיס, ו-k ביטים במחזור",
                          "סעיף ג : חלוקה ב-m, כשבכל מחזור נכנסת\nספרה בבסיס B, ו-B ו-m זרים.")
        msb = TX(r"\text{MSB first: } r' = (B\,r + d) \bmod m", size=46).move_to(UP * 1.9)
        lsb = TX(r"\text{LSB first: } x' = (x + d)\,B^{-1} \bmod m", size=46).move_to(UP * 0.7)
        kb = TX(r"k \text{ bits a cycle: } B = 2^k", size=46, color=C.MUTED).move_to(DOWN * 0.5)
        self.say("מה-MSB ספרה חדשה הופכת את v ל-Bv + d,\nוהמצב הוא השארית : m מצבים.", Write(msb))
        self.say("מה-LSB אותו טריק של סעיף ב, עם B^-1 :\nגם כאן m מצבים.", Write(lsb))
        self.say("‏k ביטים במחזור הם ספרה בבסיס 2^k :\nאותם m מצבים, רק המכפילים משתנים.", Write(kb))
        ex = TX(r"m = 7,\; B = 10:\quad B \bmod 7 = 3,\quad 10 \cdot 5 = 50 \equiv 1",
                size=42, color=C.AMBER).move_to(DOWN * 1.7)
        self.say("דוגמה : חלוקה ב-7, ספרה עשרונית במחזור.\nהמכפיל 3, וההפכי של 10 הוא 5.", Write(ex))
        self.fade_all()
        view = BoxView(QID, "dec", height=5.7).move_to(UP * 0.62)
        self.say("בתיבה : 343 = 7³, מה-MSB.\nשבעה מצבים על הטבעת.", FadeIn(view))
        self.box_beat(view, [
            (1, "הספרה 3 : שארית 3."),
            (2, "הספרה 4 : 3 · 3 + 4 = 13, שארית 6."),
            (3, "הספרה 3 : 3 · 6 + 3 = 21, שארית 0.\n‏343 מתחלק ב-7."),
        ])
        new = BoxView(QID, "declsb", height=5.7).move_to(view)
        self.play(FadeOut(view), FadeIn(new), run_time=0.8)
        self.box_beat(new, [
            (1, "ועכשיו מה-LSB, הספרה 3 קודם :\n‏(0 + 3) · 5 = 15, כלומר 1."),
            (2, "הספרה 4 : (1 + 4) · 5 = 25, כלומר 4."),
            (3, "הספרה 3 : (4 + 3) · 5 = 35, כלומר 0.\nשוב מתחלק, מהכיוון השני."),
        ])
        self.fade_all()


class Closing(FsmScene):
    def construct(self):
        self.closing(QID, [("א", M("r' = (2r + b) mod 3", 34)),
                           ("ב", M("x' = 2(x + b) mod 3", 34)),
                           ("ג", M("r' = (B·r + d) mod m", 34))],
                     ["לסיכום : שלושה מצבים בשני הכיוונים,\nשני Flip-Flops ומעט שערים.",
                      "נסו מספרים משלכם בתיבה\nשבעמוד של שאלה 0055 באתר."],
                     holds=(4.0, 4.5))
