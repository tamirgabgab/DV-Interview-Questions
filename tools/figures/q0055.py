#!/usr/bin/env python3
"""Figures and tables of question 0055 (a state machine that says whether the number read
so far is divisible by m: bits from the MSB, bits from the LSB, any base and k bits a cycle).

    python tools/figures/fill.py 55        # put the blocks on the page

The reference here is independent of the page code: the naive machines are written from
the definition (the remainder, and for the LSB the remainder together with B^k mod m) and
minimized by partition refinement, so the state counts are found, not assumed. blocks()
returns, in page order: the MSB machine of 3 as a state diagram, its legend, its
transition table, the six naive LSB states and the three classes they merge into, the
LSB machine of 3, the table of the fewest states for m = 2 to 16, and the multipliers of
k bits a cycle; then, for part a, the implementation with two D flip-flops (the encoded
transition table, the Karnaugh maps of D1 and D0 with their groups, the equations and the
schematic of the circuit); for part b its encoded table and equations (the same circuit with
the flip-flops swapped); last the block diagram of the machine and part a's table of clocks
for 13 = 1101 (hw_clocks, the model of the divhw box). The flip-flop equations are found here
by a small Quine-McCluskey over the three inputs Q1, Q0, b with the unused code 11 as a don't
care, not written by hand. tests/0055 checks the page code and the box against these.
"""

import itertools
import math
from html import escape

from cells import legend as cells_legend

RLM = "‏"


# --- the machines -----------------------------------------------------------------------

def minimize(start, delta, accept, alphabet):
    """(the number of states of the minimal machine, the number of reachable states) of a
    Moore machine given by its start state, delta(s, d) and accept(s)."""
    seen, todo = {start}, [start]
    while todo:
        s = todo.pop()
        for d in alphabet:
            t = delta(s, d)
            if t not in seen:
                seen.add(t)
                todo.append(t)
    states = sorted(seen)
    cls = {s: int(accept(s)) for s in states}
    while True:
        sig = {s: (cls[s],) + tuple(cls[delta(s, d)] for d in alphabet) for s in states}
        ids = {}
        new = {s: ids.setdefault(sig[s], len(ids)) for s in states}
        if len(ids) == len(set(cls.values())):
            return len(ids), len(states)
        cls = new


def naive_msb(m, base=2):
    """The state is the remainder of the number read so far."""
    return minimize(0, lambda r, d: (r * base + d) % m, lambda r: r == 0, range(base))


def naive_lsb(m, base=2):
    """The state is (the remainder, base^k mod m): the weight of the next digit."""
    return minimize((0, 1 % m), lambda s, d: ((s[0] + d * s[1]) % m, s[1] * base % m),
                    lambda s: s[0] == 0, range(base))


def value(digits, base, lsb):
    """The number the digits spell when they arrive MSB first or LSB first."""
    seq = list(reversed(digits)) if lsb else digits
    v = 0
    for d in seq:
        v = v * base + d
    return v


def table(m, base, lsb):
    """next[s][d] of the m-state machine (gcd(base, m) = 1): r' = base*r + d from the MSB,
    x' = (x + d) / base from the LSB, where x = remainder / base^k."""
    inv = next(y for y in range(m) if base * y % m == 1 % m)
    return [[(s + d) * inv % m if lsb else (s * base + d) % m for d in range(base)] for s in range(m)]


# --- blocks ------------------------------------------------------------------------------

def diagram(m, lsb, label):
    """The machine of m (bits) on a ring: state 0 on top, a curved arrow per transition,
    a loop outside the ring for a state that stays. Every node and arc carries a key in
    data-fig (`n<i>`, `e<i>-<bit>-<j>`, an arc's label too), which a sticky figure's steps
    light (question-page.js)."""
    nxt = table(m, 2, lsb)
    W, H, R, r = 360, 272, 92, 24
    cx, cy = W / 2, 166
    pos = [(cx + R * math.sin(2 * math.pi * i / m), cy - R * math.cos(2 * math.pi * i / m)) for i in range(m)]
    mk = f"dv-arrow-{'l' if lsb else 'm'}{m}"
    s = (f'<svg class="figure dv-fig" viewBox="0 0 {W} {H}" style="max-width:24rem" role="img" aria-label="{label}">'
         f'<defs><marker id="{mk}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
         'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs>')
    f = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")
    for i in range(m):
        for d in (0, 1):
            j, cls = nxt[i][d], "fs-edge" + (" is-found" if d else "")
            key = f'data-fig="e{i}-{d}-{j}"'
            lcls = "fs-label halo" + (" is-found" if d else "")
            (x0, y0), (x1, y1) = pos[i], pos[j]
            if i == j:
                ux, uy = (x0 - cx) / R, (y0 - cy) / R
                tx, ty = -uy, ux
                a = (x0 + r * (ux * 0.8 - tx * 0.6), y0 + r * (uy * 0.8 - ty * 0.6))
                b = (x0 + r * (ux * 0.8 + tx * 0.6), y0 + r * (uy * 0.8 + ty * 0.6))
                c1 = (x0 + ux * (r + 36) - tx * 22, y0 + uy * (r + 36) - ty * 22)
                c2 = (x0 + ux * (r + 36) + tx * 22, y0 + uy * (r + 36) + ty * 22)
                s += (f'<path class="{cls}" {key} d="M{f(a[0])},{f(a[1])} C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(b[0])},{f(b[1])}" '
                      f'marker-end="url(#{mk})"><title>{i} --{d}--> {j}</title></path>')
                s += f'<text class="{lcls}" {key} x="{f(x0 + ux * (r + 36))}" y="{f(y0 + uy * (r + 36) + 4)}" text-anchor="middle">{d}</text>'
                continue
            dx, dy = x1 - x0, y1 - y0
            dist = math.hypot(dx, dy)
            nx, ny = dy / dist, -dx / dist                  # the right-hand side of the arrow
            bend = 0.22 * dist
            c = ((x0 + x1) / 2 + nx * bend, (y0 + y1) / 2 + ny * bend)
            def trim(px, py, k):
                vx, vy = c[0] - px, c[1] - py
                n = math.hypot(vx, vy)
                return px + vx / n * k, py + vy / n * k
            a, b = trim(x0, y0, r), trim(x1, y1, r + 2)
            q = (0.25 * a[0] + 0.5 * c[0] + 0.25 * b[0] + nx * 11, 0.25 * a[1] + 0.5 * c[1] + 0.25 * b[1] + ny * 11 + 4)
            s += (f'<path class="{cls}" {key} d="M{f(a[0])},{f(a[1])} Q{f(c[0])},{f(c[1])} {f(b[0])},{f(b[1])}" '
                  f'marker-end="url(#{mk})"><title>{i} --{d}--> {j}</title></path>')
            s += f'<text class="{lcls}" {key} x="{f(q[0])}" y="{f(q[1])}" text-anchor="middle">{d}</text>'
    for i, (x, y) in enumerate(pos):
        s += f'<g class="fs-node{" is-start" if i == 0 else ""}" data-fig="n{i}"><circle cx="{f(x)}" cy="{f(y)}" r="{r}"/>'
        if i == 0:
            s += f'<circle cx="{f(x)}" cy="{f(y)}" r="{r - 5}"/>'
        s += f'<text x="{f(x)}" y="{f(y + 5)}" text-anchor="middle">{"x" if lsb else "r"}={i}</text></g>'
    return s + "</svg>"


def legend():
    return ('<span class="viz-legend"><span><i class="fs-key"></i>הביט 0</span>'
            '<span><i class="fs-key-found"></i>הביט 1</span>'
            '<span><i class="dv-key-acc"></i>עיגול כפול : המספר מתחלק (ומשם מתחילים)</span></span>')


def msb_table():
    rows = ["| המצב (השארית) | הביט | ‏\\( 2r + b \\) | המצב הבא |", "|:-:|:-:|:-:|:-:|"]
    for r in range(3):
        for b in (0, 1):
            rows.append(f"| {RLM}{r} | {RLM}{b} | {RLM}{2 * r + b} | {RLM}{(2 * r + b) % 3} |")
    return "\n".join(rows)


def merge_table():
    """The six naive states (r, k mod 2) of the LSB machine of 3 and the x = r * 2^-k they
    carry: two states with the same x behave the same on every future bit."""
    rows = ["| השארית r | הביטים עד עכשיו k | המשקל של הביט הבא ‏\\( 2^k \\bmod 3 \\) | ‏\\( x = r \\cdot 2^{-k} \\bmod 3 \\) |", "|:-:|:-:|:-:|:-:|"]
    for r in range(3):
        for k in (0, 1):
            rows.append(f"| {RLM}{r} | {'זוגי' if k == 0 else 'אי-זוגי'} | {RLM}{pow(2, k, 3)} | {RLM}{r * pow(2, -k, 3) % 3} |")
    return "\n".join(rows)


def states_table():
    rows = ["| ‏m | ביט נכנס כ-LSB | ביט נכנס כ-MSB | הנאיבית, ביט נכנס כ-MSB |", "|:-:|:-:|:-:|:-:|"]
    for m in range(2, 17):
        a, b, c = naive_msb(m)[0], naive_lsb(m)[0], naive_lsb(m)[1]
        rows.append(f"| {RLM}{m} | {RLM}{a} | {RLM}{b} | {RLM}{c} |")
    return "\n".join(rows)


def kbits_table():
    rows = ["| ‏k ביטים במחזור | הבסיס ‏\\( B = 2^k \\) | ‏m = 3 | ‏m = 5 | ‏m = 7 |", "|:-:|:-:|:-:|:-:|:-:|"]
    for k in range(1, 5):
        B = 2 ** k
        cells = " | ".join(f"{RLM}{B % m}, {pow(B, -1, m)}" for m in (3, 5, 7))
        rows.append(f"| {RLM}{k} | {RLM}{B} | {cells} |")
    return "\n".join(rows)


# --- the implementation with D flip-flops (parts a and b) --------------------------------

ENC = {0: (0, 0), 1: (0, 1), 2: (1, 0)}          # the state's code Q1 Q0; 11 is unused
VARS = ("Q1", "Q0", "b")                           # the inputs of the next-state logic
GRAY = ((0, 0), (0, 1), (1, 1), (1, 0))            # the K-map's columns Q1 Q0


def next_code(lsb, q1, q0, b):
    """The code of the next state, or None for the unused code 11 (a don't care)."""
    state = {code: s for s, code in ENC.items()}.get((q1, q0))
    if state is None:
        return None
    return ENC[table(3, 2, lsb)[state][b]]


def truth(lsb):
    """{(q1, q0, b): (d1, d0) or None} over all eight input rows."""
    return {(q1, q0, b): next_code(lsb, q1, q0, b) for q1, q0, b in itertools.product((0, 1), repeat=3)}


def implicants(on, dc):
    """The prime implicants of a function of the three inputs: tuples of 0, 1 or None
    (None: the input is not in the term), by merging terms that differ in one input."""
    terms = {tuple(t) for t in on | dc}
    primes = set()
    while terms:
        merged, used = set(), set()
        for a, b in itertools.combinations(sorted(terms, key=str), 2):
            diff = [i for i in range(3) if a[i] != b[i]]
            if len(diff) == 1 and None not in (a[diff[0]], b[diff[0]]):
                t = tuple(None if i == diff[0] else a[i] for i in range(3))
                merged.add(t)
                used |= {a, b}
        primes |= terms - used
        terms = merged
    return primes


def covers(term, row):
    return all(t is None or t == r for t, r in zip(term, row))


def minimal_cover(on, dc):
    """The fewest prime implicants that cover every 1 (then the fewest literals); the terms
    in a fixed order: by the first input they use, Q1 before Q0 before b."""
    primes = sorted(implicants(on, dc), key=lambda t: [(v is None, v) for v in t])
    for n in range(1, len(primes) + 1):
        best = None
        for combo in itertools.combinations(primes, n):
            if all(any(covers(t, row) for t in combo) for row in on):
                lits = sum(v is not None for t in combo for v in t)
                if best is None or lits < best[0]:
                    best = (lits, combo)
        if best:
            return list(best[1])
    return []


def equations(lsb):
    """[(name, [terms])] for D1 and D0: each term a tuple (q1, q0, b) of 0, 1 or None."""
    tt = truth(lsb)
    out = []
    for k, name in enumerate(("D1", "D0")):
        on = {row for row, v in tt.items() if v is not None and v[k] == 1}
        dc = {row for row, v in tt.items() if v is None}
        out.append((name, minimal_cover(on, dc)))
    return out


def evaluate(terms, q1, q0, b):
    return int(any(covers(t, (q1, q0, b)) for t in terms))


def stuck(lsb):
    """Where the minimal equations take the unused code 11, for b = 0 and b = 1."""
    eqs = dict(equations(lsb))
    return [(evaluate(eqs["D1"], 1, 1, b), evaluate(eqs["D0"], 1, 1, b)) for b in (0, 1)]


SUB = {"Q1": "Q_1", "Q0": "Q_0", "b": "b"}
UNI = {"Q1": "Q₁", "Q0": "Q₀", "b": "b"}


def term_tex(term):
    lits = []
    for name, v in zip(VARS, term):
        if v is not None:
            lits.append(SUB[name] if v else f"\\overline{{{SUB[name]}}}")
    return "\\,".join(lits)


def term_uni(term):
    """The term in plain text for the legends and the schematic: Q̄₁·Q̄₀·b."""
    lits = []
    for name, v in zip(VARS, term):
        if v is not None:
            u = UNI[name]
            lits.append(u if v else u[0] + "\u0304" + u[1:])
    return "·".join(lits)


def equation_tex(name, terms):
    return f"{name[0]}_{name[1]} = " + " + ".join(term_tex(t) for t in terms)


def equations_block(lsb):
    """The minimal equations as display math (aligned, so it fits a phone)."""
    lines = [equation_tex(n, t).replace(" = ", " &= ", 1) for n, t in equations(lsb)]
    lines.append("\\mathrm{div} &= \\overline{Q_1}\\,\\overline{Q_0}")
    return "\\[\n\\begin{aligned}\n" + " \\\\\n".join(lines) + "\n\\end{aligned}\n\\]"


def ltr_bits(*bits):
    """Bits written apart ("0 1"): in a right-to-left line the space splits the digits into
    runs that the browser lays out from the right ("1 0"), so the pair is isolated LTR."""
    return '<span dir="ltr">' + " ".join(str(b) for b in bits) + "</span>"


def encoded_table(lsb):
    """Part a or b: the encoded transitions, a row per code and bit, the unused 11 too."""
    sym = "x" if lsb else "r"
    rows = [f"| המצב | ‏Q1 Q0 | ‏b | הבא ‏Q1 Q0, כלומר D1 D0 | ‏div |", "|:-:|:-:|:-:|:-:|:-:|"]
    inv = {code: s for s, code in ENC.items()}
    for q1, q0 in ((0, 0), (0, 1), (1, 0), (1, 1)):
        for b in (0, 1):
            nxt = next_code(lsb, q1, q0, b)
            if nxt is None:
                rows.append(f"| לא בשימוש | {RLM}{ltr_bits(1, 1)} | {RLM}{b} | {RLM}× × | {RLM}× |")
            else:
                div = int((q1, q0) == (0, 0))
                rows.append(f"| {RLM}{sym} = {inv[(q1, q0)]} | {RLM}{ltr_bits(q1, q0)} | {RLM}{b} | {RLM}{ltr_bits(*nxt)} | {RLM}{div} |")
    return "\n".join(rows)


def kmap(lsb, k, name, terms):
    """One Karnaugh map: rows b = 0, 1; columns Q1 Q0 in Gray order; a cell tinted by the
    group (term) that covers it, a don't care that no group uses dashed."""
    tt = truth(lsb)
    tints = ("c1", "c2", "c3")
    body = ""
    for b in (0, 1):
        body += f'<tr><th dir="ltr">b = {b}</th>'
        for q1, q0 in GRAY:
            v = tt[(q1, q0, b)]
            text = "×" if v is None else str(v[k])
            cls = [tints[i] for i, t in enumerate(terms) if covers(t, (q1, q0, b))]
            if v is None and not cls:
                cls = ["is-off"]
            body += f'<td class="pm-c{(" " + " ".join(cls[:1])) if cls else ""}">{text}</td>'
        body += "</tr>"
    head = '<tr class="pm-head"><th dir="ltr">Q₁Q₀</th>' + "".join(f"<td>{a}{c}</td>" for a, c in GRAY) + "</tr>"
    aria = f"מפת קרנו של {name} : השורות b, העמודות Q1 Q0 בסדר גריי, והקבוצות צבועות"
    title = f'<p class="ff-map-title" dir="ltr">{name[0]}{"₁" if name[1] == "1" else "₀"}</p>'
    tab = (f'<div class="pm-scroll" tabindex="0" role="region" aria-label="{escape(aria)}">'
           f'<table class="pm-cells ff-kmap" dir="ltr"><tbody>{head}{body}</tbody></table></div>')
    keys = cells_legend([(f"pm-key-{tints[i]}", term_uni(t)) for i, t in enumerate(terms)])
    return f'<div class="ff-map">{title}{tab}{keys}</div>'


def kmaps(lsb):
    eqs = equations(lsb)
    return '<div class="ff-maps">' + "".join(kmap(lsb, k, n, t) for k, (n, t) in enumerate(eqs)) + "</div>"


# The schematic: the six literals as vertical rails on the left (b̄ from an inverter, the
# others from the flip-flops' Q and Q̄ outputs, joined by name), an AND gate per term,
# an OR gate per equation into the D input of its flip-flop, and div = Q̄₁·Q̄₀.
RAILS = ("b", "b\u0304", "Q₁", "Q\u0304₁", "Q₀", "Q\u0304₀")


def _rail_of(name, v):
    return ("b", "Q1", "Q0").index(name) * 2 + (0 if v else 1)


def _f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _and(x, y, h):
    w = h / 2
    return (f'<path class="ff-gate" d="M{_f(x)},{_f(y - h / 2)} H{_f(x + w)} A{_f(h / 2)},{_f(h / 2)} 0 0 1 '
            f'{_f(x + w)},{_f(y + h / 2)} H{_f(x)} Z"/>'), x + w + h / 2


def _or(x, y, h):
    w = 1.15 * h
    return (f'<path class="ff-gate" d="M{_f(x)},{_f(y - h / 2)} Q{_f(x + 0.6 * w)},{_f(y - h / 2)} {_f(x + w)},{_f(y)} '
            f'Q{_f(x + 0.6 * w)},{_f(y + h / 2)} {_f(x)},{_f(y + h / 2)} Q{_f(x + 0.28 * w)},{_f(y)} {_f(x)},{_f(y - h / 2)} Z"/>'), x + w


def _svg_label(t):
    """A label with its bar drawn as an overline on the letter (Q̄₁, b̄): the combining
    macron sits off a lowercase b in the code font."""
    if "\u0304" not in t:
        return escape(t)
    head, rest = t.split("\u0304", 1)
    return f'<tspan text-decoration="overline">{escape(head)}</tspan>{escape(rest)}'


def _text(x, y, t, anchor="middle", cls="ff-text"):
    return f'<text class="{cls}" x="{_f(x)}" y="{_f(y)}" text-anchor="{anchor}">{_svg_label(t)}</text>'


def schematic(lsb):
    eqs = equations(lsb)
    rx = [34 + 40 * i for i in range(6)]               # the rails
    gx, ox, fx, fw = 300, 392, 488, 64                 # the AND gates, the OR gates, the flip-flops
    top, bottom = 58, 382
    W, H = 640, 420
    s = []
    s.append(f'<line class="ff-wire" x1="{rx[0]}" y1="20" x2="{rx[0]}" y2="{bottom}"/>')
    s.append(_text(rx[0] - 10, 26, "b", "end"))
    # the inverter that makes b̄, from the rail b to the top of the rail b̄
    y_inv = 36
    s.append(f'<line class="ff-wire" x1="{rx[0]}" y1="{y_inv}" x2="{rx[0] + 8}" y2="{y_inv}"/>')
    s.append(f'<path class="ff-gate" d="M{rx[0] + 8},{y_inv - 8} L{rx[0] + 22},{y_inv} L{rx[0] + 8},{y_inv + 8} Z"/>'
             f'<circle class="ff-gate" cx="{rx[0] + 25.5}" cy="{y_inv}" r="3.5"/>')
    s.append(f'<line class="ff-wire" x1="{rx[0] + 29}" y1="{y_inv}" x2="{rx[1]}" y2="{y_inv}"/>'
             f'<line class="ff-wire" x1="{rx[1]}" y1="{y_inv}" x2="{rx[1]}" y2="{bottom}"/>')
    s.append(f'<circle class="ink-dot" cx="{rx[0]}" cy="{y_inv}" r="3.5"/>')
    for i in range(2, 6):
        s.append(f'<line class="ff-wire" x1="{rx[i]}" y1="{top}" x2="{rx[i]}" y2="{bottom}"/>')
        s.append(_text(rx[i], top - 8, RAILS[i]))
    for i in range(6):
        s.append(_text(rx[i], bottom + 22, RAILS[i]))

    def gate_inputs(term, yc, h):
        lits = [(n, v) for n, v in zip(VARS, term) if v is not None]
        ys = [yc + (j - (len(lits) - 1) / 2) * 14 for j in range(len(lits))]
        for (n, v), y in zip(lits, ys):
            x = rx[_rail_of(n, v)]
            s.append(f'<line class="ff-wire" x1="{x}" y1="{_f(y)}" x2="{gx}" y2="{_f(y)}"/>'
                     f'<circle class="ink-dot" cx="{x}" cy="{_f(y)}" r="3.5"/>')
        g, out = _and(gx, yc, h)
        s.append(g)
        return out

    y = 92
    for k, (name, terms) in enumerate(eqs):
        ys = []
        for t in terms:
            h = 30 if sum(v is not None for v in t) <= 2 else 44
            ys.append(y)
            out = gate_inputs(t, y, h)
            ys[-1] = (y, out)
            y += 58
        oy = sum(a for a, _ in ys) / len(ys)
        for j, (ay, ax) in enumerate(ys):
            iy = oy + (j - (len(ys) - 1) / 2) * 14
            xm = ox - 14
            s.append(f'<polyline class="ff-wire" fill="none" points="{_f(ax)},{_f(ay)} {_f(xm)},{_f(ay)} {_f(xm)},{_f(iy)} {ox + 6},{_f(iy)}"/>')
        g, oout = _or(ox, oy, 34)
        s.append(g)
        # the flip-flop: D at oy, the clock 30 below, Q and Q̄ on the right
        fy0 = oy - 22
        s.append(f'<line class="ff-wire" x1="{_f(oout)}" y1="{_f(oy)}" x2="{fx}" y2="{_f(oy)}"/>')
        s.append(f'<rect class="ff-gate" x="{fx}" y="{_f(fy0)}" width="{fw}" height="74" rx="3"/>')
        s.append(_text(fx + 8, oy + 5, "D", "start", "ff-pin"))
        s.append(f'<path class="ff-wire" fill="none" d="M{fx},{_f(oy + 24)} L{fx + 9},{_f(oy + 30)} L{fx},{_f(oy + 36)}"/>')
        s.append(f'<line class="ff-wire" x1="{fx - 20}" y1="{_f(oy + 30)}" x2="{fx}" y2="{_f(oy + 30)}"/>')
        s.append(_text(fx - 23, oy + 35, "clk", "end", "ff-small"))
        s.append(_text(fx + fw - 6, oy + 5, "Q", "end", "ff-pin"))
        s.append(_text(fx + fw - 6, oy + 35, "Q\u0304", "end", "ff-pin"))
        qn, qb = (RAILS[2], RAILS[3]) if k == 0 else (RAILS[4], RAILS[5])
        s.append(f'<line class="ff-wire" x1="{fx + fw}" y1="{_f(oy)}" x2="{fx + fw + 22}" y2="{_f(oy)}"/>'
                 + _text(fx + fw + 26, oy + 5, qn, "start"))
        s.append(f'<line class="ff-wire" x1="{fx + fw}" y1="{_f(oy + 30)}" x2="{fx + fw + 22}" y2="{_f(oy + 30)}"/>'
                 + _text(fx + fw + 26, oy + 35, qb, "start"))
        # the asynchronous active-low reset to 0: a bubble under the box
        rb = fy0 + 74
        s.append(f'<circle class="ff-gate" cx="{fx + fw / 2}" cy="{_f(rb + 4)}" r="4"/>'
                 f'<line class="ff-wire" x1="{fx + fw / 2}" y1="{_f(rb + 8)}" x2="{fx + fw / 2}" y2="{_f(rb + 16)}"/>')
        s.append(_text(fx + fw / 2, rb + 30, "rst_n", "middle", "ff-small"))
        y += 22
    # div = Q̄₁·Q̄₀
    dy = max(y, bottom - 30)
    out = gate_inputs((0, 0, None), dy, 30)
    s.append(f'<line class="ff-wire" x1="{_f(out)}" y1="{_f(dy)}" x2="{fx + fw + 22}" y2="{_f(dy)}"/>'
             + _text(fx + fw + 26, dy + 5, "div", "start"))
    label = ("המעגל של סעיף ב" if lsb else "המעגל של סעיף א") + (
        " : שני פליפ-פלופים מסוג D עם איפוס אסינכרוני, שערי AND ו-OR לכל כניסת D, ו-div מ-AND של שני המשלימים")
    return (f'<svg class="figure ff-fig" viewBox="0 0 {W} {H}" style="max-width:40rem" role="img" '
            f'aria-label="{escape(label)}">' + "".join(s) + "</svg>")


def schematic_legend():
    return ('<span class="viz-legend"><span><i class="ff-key-dot"></i>נקודה : חיבור לקו האנכי</span>'
            '<span>קווים עם אותו שם מחוברים (‏Q₁ ו-Q̄₁ יוצאים מהפליפ-פלופ העליון)</span></span>')


# --- the machine clock by clock (part a's table, the divhw box) ----------------------------

NB = " "


def hw_clocks(bits, lsb=False, start=(0, 0)):
    """The circuit of part a (lsb False) or part b clock by clock, the way the table and the
    box read it: one record per clock, clock 0 the one after reset (or after power-up in
    `start`, the unused 11 for the trap). q1, q0 are the flip-flops through the clock; din
    the bit presented in it and d1, d0 the next-state logic (None after the last bit); div =
    Q̄1·Q̄0, the output through the clock; v the number the bits of the clocks before spell.
    The logic is the minimal equations, so the code 11 behaves as the page says."""
    eqs = dict(equations(lsb))
    q1, q0 = start
    out = []
    for t in range(len(bits) + 1):
        din = bits[t] if t < len(bits) else None
        d1 = d0 = None
        if din is not None:
            d1, d0 = evaluate(eqs["D1"], q1, q0, din), evaluate(eqs["D0"], q1, q0, din)
        out.append({"clock": t, "din": din, "q1": q1, "q0": q0, "d1": d1, "d0": d0,
                    "div": int(not q1 and not q0), "v": value(bits[:t], 2, lsb)})
        if din is not None:
            q1, q0 = d1, d0
    return out


def clocks_table(bits=(1, 1, 0, 1)):
    """Part a: 13 = 1101 through the circuit, a row per clock. div comes from the flip-flops
    only (Moore), so the answer for the bits up to clock t shows in clock t + 1."""
    rows = [f"| השעון | ‏din | ‏Q1 Q0 | ‏D1 D0 | ‏div | הביטים לפני השעון |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for c in hw_clocks(list(bits)):
        t = c["clock"]
        when = f"{RLM}0, אחרי reset" if t == 0 else f"{RLM}{t}"
        din = "–" if c["din"] is None else f"{RLM}{c['din']}"
        nxt = "–" if c["d1"] is None else f"{RLM}{ltr_bits(c['d1'], c['d0'])}"
        read = "אין עדיין, ‏0" if t == 0 else f'{RLM}<span dir="ltr">{"".join(map(str, bits[:t]))} = {c["v"]}</span>'
        div = f"**{c['div']}**" if c["div"] else str(c["div"])
        rows.append(f"| {when} | {din} | {RLM}{ltr_bits(c['q1'], c['q0'])} | {nxt} | {RLM}{div} | {read} |")
    return "\n".join(rows)


# The block diagram of parts a and b (the page's figure and the divhw box): the next-state
# logic, the state register of two D flip-flops, the output logic and the loop back.
HW_W, HW_H = 500, 224
# (id, x, y, w, h, class, title, second line)
HW_BLOCKS = (
    ("ns", 40, 50, 130, 110, "stage", "next state", "D = f(Q, din)"),
    ("reg", 220, 50, 110, 110, "reg", "register", ""),
    ("out", 380, 75, 90, 60, "out", "output", "!Q1 & !Q0"),
)
# the two flip-flops inside the register: (id, x, y, w, h, name)
HW_FFS = (("ff1", 236, 82, 36, 36, "Q1"), ("ff0", 278, 82, 36, 36, "Q0"))
# (id, points, label, label x, label y, anchor)
HW_WIRES = (
    ("din", ((6, 105), (40, 105)), "din", 8, 97, "start"),
    ("d", ((170, 105), (220, 105)), "D1 D0", 195, 97, "middle"),
    ("clk", ((252, 14), (252, 50)), "clk", 246, 26, "end"),
    ("rst", ((298, 14), (298, 50)), "rst_n", 304, 26, "start"),
    ("q", ((330, 105), (380, 105)), "Q1 Q0", 360, 97, "middle"),
    ("fb", ((346, 105), (346, 196), (105, 196), (105, 160)), "Q1 Q0", 225, 214, "middle"),
    ("div", ((470, 105), (496, 105)), "div", 483, 97, "middle"),
)


def hw_diagram():
    """Parts a and b: the block diagram of the machine, the same for both directions (only
    the next-state logic differs)."""
    label = ("תרשים המלבנים של המכונה" + NB + ": הלוגיקה של המצב הבא מקבלת את din ואת Q1 Q0 ומחשבת את D1 D0. "
             "רגיסטר המצב, שני פליפ-פלופים מסוג D עם clk ו-rst_n, כותב את D1 D0 ל-Q1 Q0 בקצה השעון. "
             "לוגיקת היציאה מחשבת div מ-Q1 Q0 בלבד, ו-Q1 Q0 חוזרים גם ללוגיקה של המצב הבא")
    o = [f'<svg class="figure dh-fig dh-dp" viewBox="0 0 {HW_W} {HW_H}" direction="ltr" style="max-width:{HW_W / 16:g}rem" '
         f'role="img" aria-label="{escape(label)}">',
         '<defs><marker id="dh-hb" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" '
         'markerHeight="9" orient="auto"><path class="dh-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>']
    for _id, x, y, w, h, cls, title, sub in HW_BLOCKS:
        ty = y + 18 if _id == "reg" else y + h / 2 - 3
        o.append(f'<g class="dh-blk dh-{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>'
                 f'<text x="{x + w / 2:g}" y="{ty:g}" text-anchor="middle">{escape(title)}</text>'
                 + (f'<text class="dh-sub" x="{x + w / 2:g}" y="{y + h / 2 + 13:g}" text-anchor="middle">{escape(sub)}</text>' if sub else "")
                 + "</g>")
    for _id, x, y, w, h, name in HW_FFS:
        o.append(f'<g class="dh-ff"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3"/>'
                 f'<text x="{x + w / 2:g}" y="{y + h / 2 + 5:g}" text-anchor="middle">{name}</text></g>')
    for _id, pts, lab, lx, ly, anchor in HW_WIRES:
        d = "M" + " L".join(f"{x:g},{y:g}" for x, y in pts)
        o.append(f'<path class="dh-wire" d="{d}" marker-end="url(#dh-hb)"/>')
        o.append(f'<text class="dh-wlab" x="{lx}" y="{ly}" text-anchor="{anchor}">{escape(lab)}</text>')
    o.append('<circle class="dh-dot" cx="346" cy="105" r="3.5"/>')
    return "".join(o) + "</svg>"


def blocks():
    """The generated blocks, in page order (12 to 14 sit earlier on the page: part b's
    equations, then part a's block diagram and table of clocks)."""
    return [diagram(3, False, "מכונת המצבים של 3 כשביט חדש נכנס כ-LSB : שלושה מצבים, השארית של המספר עד עכשיו"),
            legend(), msb_table(), merge_table(),
            diagram(3, True, "מכונת המצבים של 3 כשביט חדש נכנס כ-MSB : שלושה מצבים, x הוא השארית כפול 2 בחזקת מינוס k"),
            states_table(), kbits_table(),
            encoded_table(False), kmaps(False), equations_block(False), schematic(False) + "\n\n" + schematic_legend(),
            encoded_table(True), equations_block(True), hw_diagram(), clocks_table()]


if __name__ == "__main__":
    print([(m, naive_msb(m), naive_lsb(m)) for m in range(2, 10)])
    print("\n\n".join(blocks()))
