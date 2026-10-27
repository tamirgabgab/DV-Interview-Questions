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
k bits a cycle. tests/0055 checks the page code against these.
"""

import math

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
    a loop outside the ring for a state that stays."""
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
            lcls = "fs-label halo" + (" is-found" if d else "")
            (x0, y0), (x1, y1) = pos[i], pos[j]
            if i == j:
                ux, uy = (x0 - cx) / R, (y0 - cy) / R
                tx, ty = -uy, ux
                a = (x0 + r * (ux * 0.8 - tx * 0.6), y0 + r * (uy * 0.8 - ty * 0.6))
                b = (x0 + r * (ux * 0.8 + tx * 0.6), y0 + r * (uy * 0.8 + ty * 0.6))
                c1 = (x0 + ux * (r + 36) - tx * 22, y0 + uy * (r + 36) - ty * 22)
                c2 = (x0 + ux * (r + 36) + tx * 22, y0 + uy * (r + 36) + ty * 22)
                s += (f'<path class="{cls}" d="M{f(a[0])},{f(a[1])} C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(b[0])},{f(b[1])}" '
                      f'marker-end="url(#{mk})"><title>{i} --{d}--> {j}</title></path>')
                s += f'<text class="{lcls}" x="{f(x0 + ux * (r + 36))}" y="{f(y0 + uy * (r + 36) + 4)}" text-anchor="middle">{d}</text>'
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
            s += (f'<path class="{cls}" d="M{f(a[0])},{f(a[1])} Q{f(c[0])},{f(c[1])} {f(b[0])},{f(b[1])}" '
                  f'marker-end="url(#{mk})"><title>{i} --{d}--> {j}</title></path>')
            s += f'<text class="{lcls}" x="{f(q[0])}" y="{f(q[1])}" text-anchor="middle">{d}</text>'
    for i, (x, y) in enumerate(pos):
        s += f'<g class="fs-node{" is-start" if i == 0 else ""}"><circle cx="{f(x)}" cy="{f(y)}" r="{r}"/>'
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
    rows = ["| ‏m | מה-MSB | מה-LSB | המכונה הנאיבית מה-LSB |", "|:-:|:-:|:-:|:-:|"]
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


def blocks():
    """The generated blocks, in page order."""
    return [diagram(3, False, "מכונת המצבים של 3 מה-MSB : שלושה מצבים, השארית של המספר עד עכשיו"),
            legend(), msb_table(), merge_table(),
            diagram(3, True, "מכונת המצבים של 3 מה-LSB : שלושה מצבים, x הוא השארית כפול 2 בחזקת מינוס k"),
            states_table(), kbits_table()]


if __name__ == "__main__":
    print([(m, naive_msb(m), naive_lsb(m)) for m in range(2, 10)])
    print("\n\n".join(blocks()))
