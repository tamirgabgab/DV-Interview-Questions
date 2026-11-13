#!/usr/bin/env python3
"""Figures and tables of question 0106, the number that appears once when every other number
appears three times.

    python tools/figures/fill.py 106        # put the blocks on the page

The references here are independent of the page code:

- counts(nums) counts every value (a dict, O(n) memory: the hash map the page rules out);
  odd_one(nums, k) is the value whose count is not a multiple of k.
- lane_counts(nums, width) counts the ones of every bit lane (bit b of every number, the sign
  bit repeated for a negative number), and machine(nums, width) runs the mod-3 state machine
  of one bit, lane by lane, from its state table (not from the two lines of the page), and
  returns ones and twos after every number as signed numbers of `width` bits.
- trace(nums, order) runs the two lines literally in the page's order ("good"), with twos
  first ("swap"), or both from the old values ("old"), on Python's unbounded integers; the
  last two are the trap of the order.
- sliced(nums, k) counts every lane modulo k with ceil(log2 k) words, written again here
  with a plain integer counter per lane.

blocks() returns, in page order: part a's table of the XOR, the state diagram of one bit and
its legend, the derivation table of the two lines, the table of ones and twos over
[2, 2, 3, 2] and its legend, and part c's lanes of the k = 5 example.
"""

from __future__ import annotations

import math
from collections import Counter

RLM = "‏"
NB = " "
MINUS = "−"

# the arrays of the page and of the box
TWICE = [4, 1, 2, 1, 2]                                  # part a: 4
EXAMPLE = [2, 2, 3, 2]                                   # part b: 3
NINETY_NINE = [0, 1, 0, 1, 0, 1, 99]                     # part b: 99
NEGATIVE = [-2, -2, 1, 1, -3, 1, -3, -3, -4, -2]         # part b: -4
TWO_OF_THREE = [5, 5, 7, 7, 7]                           # part c: 5 twice, ones 0 and twos 5
BROKEN = [2, 3, 2, 5, 2]                                 # the box: 3 and 5 once, the rule broken
K5 = [7, -1, 6, 7, -1, 7, 6, -1, 7, -1, 7, -1]           # part c: k = 5, 6 twice
STATE = {(0, 0): 0, (0, 1): 1, (1, 0): 2}                # (twos, ones) -> the count mod 3


# --- the references ------------------------------------------------------------------------

def counts(nums) -> dict:
    return dict(Counter(nums))


def odd_one(nums, k: int = 3):
    """The value whose count is not a multiple of k (None unless there is exactly one)."""
    odd = [v for v, c in Counter(nums).items() if c % k]
    return odd[0] if len(odd) == 1 else None


def bit(v: int, b: int) -> int:
    """Bit b of v in two's complement (a negative number has ones above its top bit)."""
    return (v >> b) & 1


def signed(u: int, width: int) -> int:
    return u - (1 << width) if u >> (width - 1) & 1 else u


def lane_counts(nums, width: int = 32) -> list[int]:
    """How many numbers have a 1 in every lane b, lane 0 first."""
    return [sum(bit(x, b) for x in nums) for b in range(width)]


def step_state(s: int, x: int) -> int:
    """The state table of one lane: a 1 counts up modulo 3, a 0 stays."""
    return (s + x) % 3


def machine(nums, width: int = 32) -> list[tuple[int, int]]:
    """ones and twos after every number, lane by lane from the state table: state 1 is a 1 in
    ones, state 2 a 1 in twos."""
    lanes, out = [0] * width, []
    for x in nums:
        lanes = [step_state(s, bit(x, b)) for b, s in enumerate(lanes)]
        ones = sum(1 << b for b, s in enumerate(lanes) if s == 1)
        twos = sum(1 << b for b, s in enumerate(lanes) if s == 2)
        out.append((signed(ones, width), signed(twos, width)))
    return out


def trace(nums, order: str = "good") -> list[tuple[int, int]]:
    """The two lines on Python's integers in the given order, ones and twos after every number."""
    ones = twos = 0
    out = []
    for x in nums:
        if order == "good":
            ones = (ones ^ x) & ~twos
            twos = (twos ^ x) & ~ones
        elif order == "swap":
            twos = (twos ^ x) & ~ones
            ones = (ones ^ x) & ~twos
        else:
            ones, twos = (ones ^ x) & ~twos, (twos ^ x) & ~ones
        out.append((ones, twos))
    return out


def sliced(nums, k: int, width: int = 32) -> tuple[list[int], int]:
    """Every lane counted modulo k: the words c[0..m-1] (bit j of every lane's counter, as
    signed numbers of `width` bits) and their OR, the bits whose count is not a multiple of k."""
    m = max(1, math.ceil(math.log2(k)))
    lanes = [sum(bit(x, b) for x in nums) % k for b in range(width)]
    words = [signed(sum(1 << b for b in range(width) if lanes[b] >> j & 1), width) for j in range(m)]
    orr = signed(sum(1 << b for b in range(width) if lanes[b]), width)
    return words, orr


# --- formatting ------------------------------------------------------------------------------

def num(v: int) -> str:
    return f"{MINUS}{-v}" if v < 0 else str(v)


def ltr(x) -> str:
    return f'<span dir="ltr">{x}</span>'


def bits_of(v: int, width: int) -> str:
    return "".join(str(bit(v, b)) for b in range(width - 1, -1, -1))


def bitcells(v: int, width: int, cls: str) -> str:
    """The bits of v, the top one on the left, a 1 in the class `cls`."""
    cells = "".join(f'<span class="m3-b{" " + cls if c == "1" else ""}">{c}</span>' for c in bits_of(v, width))
    return f'<span class="m3-w" dir="ltr">{cells}</span>'


def statecells(states: list[int]) -> str:
    """The count modulo 3 of every lane, the top lane on the left, tinted by the state."""
    cells = "".join(f'<span class="m3-b m3-st{s}">{s}</span>' for s in reversed(states))
    return f'<span class="m3-w" dir="ltr">{cells}</span>'


# --- part a: the XOR ---------------------------------------------------------------------------

def xor_table() -> str:
    acc = 0
    rows = ["| הצעד | המספר | בבינארי | ה-XOR עד עכשיו | בעשרוני |", "|:-:|:-:|:-:|:-:|:-:|"]
    for k, x in enumerate(TWICE, 1):
        acc ^= x
        rows.append(f"| {k} | {x} | {RLM}`{bits_of(x, 3)}` | {RLM}`{bits_of(acc, 3)}` | {acc} |")
    return "\n".join(rows)


# --- part b: the state diagram of one lane ----------------------------------------------------------

NODES = {0: (80, 170), 1: (190, 80), 2: (300, 170)}
BAD = (190, 152)
NR = 28


def _arc(a, b, bow):
    """A quadratic arc from node a to node b, bowed out by `bow`, its head at b's rim."""
    (x0, y0), (x1, y1) = NODES[a], NODES[b]
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    L = math.hypot(dx, dy)
    nx, ny = dy / L, -dx / L                     # the normal to the left of the direction
    cx, cy = mx + bow * nx, my + bow * ny
    ux, uy = x0 - cx, y0 - cy
    ul = math.hypot(ux, uy)
    sx, sy = x0 - NR * ux / ul, y0 - NR * uy / ul
    vx, vy = x1 - cx, y1 - cy
    vl = math.hypot(vx, vy)
    tx, ty = x1 - (NR + 1) * vx / vl, y1 - (NR + 1) * vy / vl
    ex, ey = tx - 9 * vx / vl, ty - 9 * vy / vl
    head = (f"M{tx:.1f},{ty:.1f} L{ex - 5 * vy / vl:.1f},{ey + 5 * vx / vl:.1f} "
            f"L{ex + 5 * vy / vl:.1f},{ey - 5 * vx / vl:.1f} Z")
    lx, ly = 0.25 * x0 + 0.5 * cx + 0.25 * x1, 0.25 * y0 + 0.5 * cy + 0.25 * y1
    lx, ly = lx + 13 * nx, ly + 13 * ny
    return f"M{sx:.1f},{sy:.1f} Q{cx:.1f},{cy:.1f} {ex:.1f},{ey:.1f}", head, (lx, ly)


def _loop(s, a):
    """A loop on node s, outward in the direction a (radians)."""
    x, y = NODES[s]
    p = lambda ang, r: (x + r * math.cos(ang), y + r * math.sin(ang))  # noqa: E731
    sx, sy = p(a - 0.5, NR)
    tx, ty = p(a + 0.5, NR + 1)
    c1x, c1y = p(a - 0.75, NR * 2.5)
    c2x, c2y = p(a + 0.75, NR * 2.5)
    vx, vy = tx - c2x, ty - c2y
    vl = math.hypot(vx, vy)
    ex, ey = tx - 9 * vx / vl, ty - 9 * vy / vl
    head = (f"M{tx:.1f},{ty:.1f} L{ex - 5 * vy / vl:.1f},{ey + 5 * vx / vl:.1f} "
            f"L{ex + 5 * vy / vl:.1f},{ey - 5 * vx / vl:.1f} Z")
    lx, ly = p(a, NR * 2.45)
    return f"M{sx:.1f},{sy:.1f} C{c1x:.1f},{c1y:.1f} {c2x:.1f},{c2y:.1f} {ex:.1f},{ey:.1f}", head, (lx, ly)


ARCS = {0: (0, 1, 26), 1: (1, 2, 26), 2: (2, 0, 110)}   # the move on a 1 from every state: from, to, bow
LOOPS = {0: math.pi, 1: -math.pi / 2, 2: 0.0}


def fsm_svg(label: str, now=None, taken=None) -> str:
    """The mod-3 counter of one lane: the states (twos, ones) 00, 01, 10 with the count they
    stand for, a 1 moving to the next state and a 0 staying; 11 is never reached. `now` lights
    a state (3 for 11) and `taken` the move just made, ("one", s) or ("zero", s)."""
    o = [f'<svg class="figure m3-fsm" viewBox="0 0 380 252" style="max-width:23.75rem" direction="ltr" role="img" aria-label="{label}">']
    for s, (a, b, bow) in ARCS.items():
        d, head, (lx, ly) = _arc(a, b, bow)
        cls = " is-taken" if taken == ("one", s) else ""
        o.append(f'<g class="m3-arc{cls}"><title>a 1: {s} → {(s + 1) % 3}</title><path d="{d}" fill="none"/>'
                 f'<path class="m3-head" d="{head}"/><text class="m3-lab" x="{lx:.1f}" y="{ly + 5:.1f}" text-anchor="middle">1</text></g>')
    for s, a in LOOPS.items():
        d, head, (lx, ly) = _loop(s, a)
        cls = " is-taken" if taken == ("zero", s) else ""
        o.append(f'<g class="m3-loop{cls}"><title>a 0: stays at {s}</title><path d="{d}" fill="none"/>'
                 f'<path class="m3-head" d="{head}"/><text class="m3-lab" x="{lx:.1f}" y="{ly + 5:.1f}" text-anchor="middle">0</text></g>')
    for s, (x, y) in NODES.items():
        code = {0: "00", 1: "01", 2: "10"}[s]
        cls = " is-now" if now == s else ""
        o.append(f'<g class="m3-node m3-n{s}{cls}"><title>twos {code[0]}, ones {code[1]}: count {s} mod 3</title>'
                 f'<circle cx="{x}" cy="{y}" r="{NR}"/><text class="m3-code" x="{x}" y="{y + 1}" text-anchor="middle">{code}</text>'
                 f'<text class="m3-cnt" x="{x}" y="{y + 17}" text-anchor="middle">≡{s}</text></g>')
    x, y = BAD
    cls = " is-now" if now == 3 else ""
    o.append(f'<g class="m3-node m3-n3{cls}"><title>twos 1, ones 1: never reached</title><circle cx="{x}" cy="{y}" r="20"/>'
             f'<text class="m3-code" x="{x}" y="{y + 5}" text-anchor="middle">11</text></g>')
    o.append("</svg>")
    return "".join(o)


def fsm_legend() -> str:
    return ('<span class="viz-legend"><span><i class="m3-key-n0"></i>המצב 00 : הספירה של הביט היא 0, מודולו 3</span>'
            '<span><i class="m3-key-n1"></i>המצב 01 : ‏1 ב-ones, הספירה 1</span>'
            '<span><i class="m3-key-n2"></i>המצב 10 : ‏1 ב-twos, הספירה 2</span>'
            '<span><i class="m3-key-one"></i>ביט 1 במספר שנכנס : למצב הבא</span>'
            '<span><i class="m3-key-zero"></i>ביט 0 : נשארים</span>'
            '<span><i class="m3-key-n3"></i>המצב 11 : לא מגיעים אליו</span></span>').replace(" :", f"{NB}:")


# --- part b: the derivation of the two lines ---------------------------------------------------------

def derive_rows() -> list[dict]:
    """Every state and input: the next state from the table, and the two XORs it is compared with."""
    rows = []
    for s in (0, 1, 2):
        t, o = (s >> 1) & 1, s & 1
        for x in (0, 1):
            n = step_state(s, x)
            t2, o2 = (n >> 1) & 1, n & 1
            rows.append(dict(s=s, t=t, o=o, x=x, n=n, t2=t2, o2=o2, ox=o ^ x, tx=t ^ x))
    return rows


def derive_table() -> str:
    out = [f"| המצב twos ones | {RLM}x | המצב הבא | {RLM}`ones ^ x` | הערך החדש של ones | {RLM}`twos ^ x` | הערך החדש של twos |",
           "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for r in derive_rows():
        ox = f"**{r['ox']}**" if r["ox"] != r["o2"] else str(r["ox"])
        tx = f"**{r['tx']}**" if r["tx"] != r["t2"] else str(r["tx"])
        out.append(f"| {r['t']}{r['o']} | {r['x']} | {r['t2']}{r['o2']} | {ox} | {r['o2']} | {tx} | {r['t2']} |")
    return "\n".join(out)


# --- part b: ones and twos over [2, 2, 3, 2] -----------------------------------------------------------

def trace_table(nums=EXAMPLE, width: int = 4) -> str:
    rows = machine(nums, width)
    head = ('<div class="m3-tracewrap" tabindex="0" role="region" aria-label="ones ו-twos אחרי כל מספר של הדוגמה">'
            f'<table class="m3-trace"><thead><tr><th>הצעד</th><th>המספר x</th><th>ones</th><th>twos</th>'
            f'<th>הספירה של כל ביט, מודולו 3</th></tr></thead><tbody>')
    body = [f'<tr><td>0</td><td>–</td><td>{bitcells(0, width, "m3-one")}</td><td>{bitcells(0, width, "m3-two")}</td>'
            f'<td>{statecells([0] * width)}</td></tr>']
    lanes = [0] * width
    for k, (x, (ones, twos)) in enumerate(zip(nums, rows), 1):
        lanes = [step_state(s, bit(x, b)) for b, s in enumerate(lanes)]
        body.append(f'<tr><td>{k}</td><td>{bitcells(x, width, "m3-x")} <span class="m3-v">{num(x)}</span></td>'
                    f'<td>{bitcells(ones, width, "m3-one")} <span class="m3-v">{num(ones)}</span></td>'
                    f'<td>{bitcells(twos, width, "m3-two")} <span class="m3-v">{num(twos)}</span></td>'
                    f'<td>{statecells(lanes)}</td></tr>')
    return head + "".join(body) + "</tbody></table></div>"


def trace_legend() -> str:
    return ('<span class="viz-legend"><span><i class="m3-key-x"></i>ביט 1 במספר שנכנס</span>'
            '<span><i class="m3-key-n1"></i>ביט 1 ב-ones : הספירה שלו 1</span>'
            '<span><i class="m3-key-n2"></i>ביט 1 ב-twos : הספירה שלו 2</span></span>').replace(" :", f"{NB}:")


# --- part c: the lanes of the k = 5 example -------------------------------------------------------------

def k5_table(width: int = 8) -> str:
    k = 5
    words, orr = sliced(K5, k, width)
    lanes = [c % k for c in lane_counts(K5, width)]
    cells = "".join(f'<span class="m3-b{" m3-nz" if c else ""}">{c}</span>' for c in reversed(lanes))
    rows = [f'<tr><th>הספירה מודולו 5</th><td><span class="m3-w" dir="ltr">{cells}</span></td><td></td></tr>']
    for j in range(len(words) - 1, -1, -1):
        rows.append(f'<tr><th>\u200fc[{j}]</th><td>{bitcells(words[j], width, "m3-one")}</td><td class="m3-v">{num(words[j])}</td></tr>')
    rows.append(f'<tr class="m3-or"><th>ה-OR של המילים</th><td>{bitcells(orr, width, "m3-x")}</td><td class="m3-v">{num(orr)}</td></tr>')
    return ('<div class="m3-tracewrap" tabindex="0" role="region" aria-label="המונים של הדוגמה עם k = 5, ביט לכל עמודה">'
            '<table class="m3-lanes"><tbody>' + "".join(rows) + "</tbody></table></div>")


# --- the blocks ------------------------------------------------------------------------------------------

def blocks():
    return [
        xor_table(),
        fsm_svg(f"המונה של ביט אחד{NB}: שלושה מצבים, 00, 01 ו-10, לספירה 0, 1 ו-2 מודולו 3. ביט 1 במספר שנכנס "
                f"מעביר למצב הבא, 10 חוזר ל-00, וביט 0 משאיר במקום. למצב 11 לא מגיעים"),
        fsm_legend(),
        derive_table(),
        trace_table(),
        trace_legend(),
        k5_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
