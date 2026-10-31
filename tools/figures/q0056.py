#!/usr/bin/env python3
"""Figures and tables of question 0056 (is a window of the last L digits divisible by m: a
digit enters as the window's LSB and the highest leaves, or as its MSB and the lowest
leaves; any base and any m).

    python tools/figures/fill.py 56        # put the blocks on the page

The reference here is independent of the page code: a window is its value w below B^L,
stepped by the definition, and the direct machine (a state per window) is minimized by
partition refinement, so the state counts are found, not assumed. blocks() returns, in page
order: the direct machine of L = 2 bits and m = 3 as a state diagram, its legend, the trace
of part a, the table of the fewest states for L = 1 to 8, the trace of part b, and the
constants of part c. tests/0056 checks the page code against these.
"""

import math

RLM = "‏"


# --- the window ---------------------------------------------------------------------------

def step(w, d, base, L, msb):
    """The window after the digit d: at the MSB the lowest digit leaves, at the LSB the highest."""
    return d * base ** (L - 1) + w // base if msb else (w * base + d) % base ** L


def leaving(w, base, L, msb):
    """The digit that leaves the window when the next one enters."""
    return w % base if msb else w // base ** (L - 1)


def windows(digits, base, L, msb, init=0):
    """The window before the first digit and after each one."""
    out = [init]
    for d in digits:
        out.append(step(out[-1], d, base, L, msb))
    return out


def fewest_states(m, base, L, msb):
    """The states of the minimal machine that says whether the window divides by m (every
    window is reachable from any start in L digits)."""
    n = base ** L
    cls = [int(w % m == 0) for w in range(n)]
    while True:
        sig = [(cls[w],) + tuple(cls[step(w, d, base, L, msb)] for d in range(base)) for w in range(n)]
        ids = {}
        new = [ids.setdefault(s, len(ids)) for s in sig]
        if len(ids) == len(set(cls)):
            return len(ids)
        cls = new


def digits_of(w, base, L):
    """The window's L digits, the highest first."""
    return [w // base ** i % base for i in reversed(range(L))]


def text(w, base, L):
    return "".join("0123456789abcdef"[d] for d in digits_of(w, base, L))


# --- blocks ------------------------------------------------------------------------------

def diagram(L, m, msb, label):
    """The direct machine of L bits on a ring: a state per window, the window 0 on top, a
    curved arrow per transition, a loop outside the ring for a window that stays; a double
    circle for a window that divides by m."""
    n = 2 ** L
    W, H, R, r = 360, 272, 92, 24
    cx, cy = W / 2, 166
    pos = [(cx + R * math.sin(2 * math.pi * i / n), cy - R * math.cos(2 * math.pi * i / n)) for i in range(n)]
    mk = f"wf-arrow-{'m' if msb else 'l'}{L}"
    s = (f'<svg class="figure dv-fig" viewBox="0 0 {W} {H}" style="max-width:24rem" role="img" aria-label="{label}">'
         f'<defs><marker id="{mk}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
         'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs>')
    f = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")
    for i in range(n):
        for d in (0, 1):
            j, cls = step(i, d, 2, L, msb), "fs-edge" + (" is-found" if d else "")
            lcls = "fs-label halo" + (" is-found" if d else "")
            (x0, y0), (x1, y1) = pos[i], pos[j]
            title = f"{text(i, 2, L)} --{d}--> {text(j, 2, L)}"
            if i == j:
                ux, uy = (x0 - cx) / R, (y0 - cy) / R
                tx, ty = -uy, ux
                a = (x0 + r * (ux * 0.8 - tx * 0.6), y0 + r * (uy * 0.8 - ty * 0.6))
                b = (x0 + r * (ux * 0.8 + tx * 0.6), y0 + r * (uy * 0.8 + ty * 0.6))
                c1 = (x0 + ux * (r + 36) - tx * 22, y0 + uy * (r + 36) - ty * 22)
                c2 = (x0 + ux * (r + 36) + tx * 22, y0 + uy * (r + 36) + ty * 22)
                s += (f'<path class="{cls}" d="M{f(a[0])},{f(a[1])} C{f(c1[0])},{f(c1[1])} {f(c2[0])},{f(c2[1])} {f(b[0])},{f(b[1])}" '
                      f'marker-end="url(#{mk})"><title>{title}</title></path>')
                s += f'<text class="{lcls}" x="{f(x0 + ux * (r + 36))}" y="{f(y0 + uy * (r + 36) + 4)}" text-anchor="middle">{d}</text>'
                continue
            dx, dy = x1 - x0, y1 - y0
            dist = math.hypot(dx, dy)
            nx, ny = dy / dist, -dx / dist                  # the right-hand side of the arrow
            bend = 0.22 * dist
            c = ((x0 + x1) / 2 + nx * bend, (y0 + y1) / 2 + ny * bend)

            def trim(px, py, k):
                vx, vy = c[0] - px, c[1] - py
                k2 = math.hypot(vx, vy)
                return px + vx / k2 * k, py + vy / k2 * k
            a, b = trim(x0, y0, r), trim(x1, y1, r + 2)
            q = (0.25 * a[0] + 0.5 * c[0] + 0.25 * b[0] + nx * 11, 0.25 * a[1] + 0.5 * c[1] + 0.25 * b[1] + ny * 11 + 4)
            s += (f'<path class="{cls}" d="M{f(a[0])},{f(a[1])} Q{f(c[0])},{f(c[1])} {f(b[0])},{f(b[1])}" '
                  f'marker-end="url(#{mk})"><title>{title}</title></path>')
            s += f'<text class="{lcls}" x="{f(q[0])}" y="{f(q[1])}" text-anchor="middle">{d}</text>'
    for i, (x, y) in enumerate(pos):
        acc = i % m == 0
        s += f'<g class="fs-node{" is-start" if acc else ""}"><circle cx="{f(x)}" cy="{f(y)}" r="{r}"/>'
        if acc:
            s += f'<circle cx="{f(x)}" cy="{f(y)}" r="{r - 5}"/>'
        s += f'<text x="{f(x)}" y="{f(y + 5)}" text-anchor="middle">{text(i, 2, L)}</text></g>'
    return s + "</svg>"


def legend():
    return ('<span class="viz-legend"><span><i class="fs-key"></i>הביט 0</span>'
            '<span><i class="fs-key-found"></i>הביט 1</span>'
            '<span><i class="dv-key-acc"></i>עיגול כפול : החלון מתחלק ב-3</span></span>')


def trace(bits, L, msb):
    """The steps of part a (msb False) or b (msb True) for m = 3, from the window 0."""
    if msb:
        rule = "‏\\( r' = (2(r - out) + 2^{L-1} b) \\bmod 3 \\)"
    else:
        rule = "‏\\( r' = (2r + b - 2^L out) \\bmod 3 \\)"
    rows = [f"| הביט שנכנס | הביט שיוצא | החלון | {rule} | מתחלק |", "|:-:|:-:|:-:|:-:|:-:|",
            f"| אחרי reset | אין | {RLM}`{text(0, 2, L)}` | {RLM}0 | ✓ |"]
    w, r = 0, 0
    c = pow(2, L - 1 if msb else L, 3)
    for b in bits:
        out = leaving(w, 2, L, msb)
        r2 = (2 * (r - out) + c * b) % 3 if msb else (2 * r + b - c * out) % 3
        w = step(w, b, 2, L, msb)
        assert r2 == w % 3
        calc = f"(2·({r} − {out}) + {c}·{b}) mod 3 = {r2}" if msb else f"(2·{r} + {b} − {c}·{out}) mod 3 = {r2}"
        rows.append(f"| {RLM}{b} | {RLM}{out} | {RLM}`{text(w, 2, L)}` | <span dir=\"ltr\">{calc}</span> | {'✓' if r2 == 0 else '✗'} |")
        r = r2
    return "\n".join(rows)


def states_table():
    rows = ["| ‏L | החלונות ‏\\( 2^L \\) | שרשור ל-LSB | שרשור ל-MSB | חסם תחתון ‏\\( 2^{L-2} \\) |", "|:-:|:-:|:-:|:-:|:-:|"]
    for L in range(1, 9):
        a, b = fewest_states(3, 2, L, False), fewest_states(3, 2, L, True)
        low = 2 ** (L - 2) if L >= 2 else 1
        rows.append(f"| {RLM}{L} | {RLM}{2 ** L} | {RLM}{a} | {RLM}{b} | {RLM}{low} |")
    return "\n".join(rows)


CASES = [(2, 8, 3), (2, 8, 7), (8, 3, 7), (16, 2, 5), (10, 3, 3), (10, 4, 7)]


def constants_table():
    rows = ["| הבסיס B | ‏L | ‏m | ‏\\( B^L \\bmod m \\) (LSB) | ‏\\( B^{L-1} \\bmod m \\) (MSB) | ‏\\( B^{-1} \\bmod m \\) (MSB) |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for B, L, m in CASES:
        rows.append(f"| {RLM}{B} | {RLM}{L} | {RLM}{m} | {RLM}{pow(B, L, m)} | {RLM}{pow(B, L - 1, m)} | {RLM}{pow(B, -1, m)} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [diagram(2, 3, False, "המכונה הישירה של חלון של 2 ביטים, ביט חדש נכנס כ-LSB : מצב לכל חלון, 00 ו-11 מתחלקים ב-3"),
            legend(), trace([1, 1, 0, 1], 3, False), states_table(), trace([1, 0, 1, 1], 3, True), constants_table()]


if __name__ == "__main__":
    print([(L, fewest_states(3, 2, L, False), fewest_states(3, 2, L, True)) for L in range(1, 9)])
    print("\n\n".join(blocks()))
