#!/usr/bin/env python3
"""Figures and tables of question 0097, the integer square root in hardware, bit by bit.

    python tools/figures/fill.py 97        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. The functions above blocks() are the reference the question's tests use: the
square root decided one bit at a time with the remainder n - r^2 and the trial 2rb + b^2,
the sequential module's registers after every clock, restoring division by the shifted
divisor, and the cube root with r^2 kept in a register.
"""

from __future__ import annotations

import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

RLM = "‏"
NB = " "
N0 = 1000          # the question's example
A0, D0 = 1000, 7   # part d: 1000 / 7
C0 = 1000          # part d: the cube root of 1000


# --- the reference ---------------------------------------------------------------------------------

def isqrt_steps(n, width=16):
    """The square root of a width-bit n (width even), one result bit per step from the top:
    [{k, b, trial, before, ok, r, rem}] with r and rem after the step."""
    r, rem, out = 0, n, []
    for k in range(width // 2 - 1, -1, -1):
        b = 1 << k
        trial = (r << (k + 1)) | (1 << (2 * k))
        before, ok = rem, trial <= rem
        if ok:
            rem -= trial
            r |= b
        out.append({"k": k, "b": b, "trial": trial, "before": before, "ok": ok, "r": r, "rem": rem})
    return out


def isqrt_ref(n, width=16):
    s = isqrt_steps(n, width)[-1]
    return s["r"], s["rem"]


def seq_cycles(n, width=16):
    """The registers of the sequential module after start and after every clock while busy:
    [(cycle, k, r, rem, busy, done)]; cycle 0 is the clock that loads n."""
    half = width // 2
    out = [(0, half - 1, 0, n, 1, 0)]
    for i, s in enumerate(isqrt_steps(n, width), start=1):
        last = s["k"] == 0
        out.append((i, s["k"] - 1 if not last else 0, s["r"], s["rem"], 0 if last else 1, 1 if last else 0))
    return out


def div_steps(a, d, width=16):
    """Restoring division by the shifted divisor: quotient bit k is 1 when d << k fits in what
    is left. [{k, trial, before, ok, q, rem}]."""
    q, rem, out = 0, a, []
    for k in range(width - 1, -1, -1):
        trial = d << k
        before, ok = rem, trial <= rem
        if ok:
            rem -= trial
            q |= 1 << k
        out.append({"k": k, "trial": trial, "before": before, "ok": ok, "q": q, "rem": rem})
    return out


def icbrt_steps(n, width=24):
    """The cube root, one bit per step: the trial (r + b)^3 - r^3 = 3r^2 b + 3r b^2 + b^3 from
    shifts and adds, with r^2 kept in a register r2. [{k, trial, before, ok, r, r2, rem}]."""
    m = (width + 2) // 3
    r, r2, rem, out = 0, 0, n, []
    for k in range(m - 1, -1, -1):
        b = 1 << k
        t1 = ((r2 << 1) + r2) << k              # 3 r^2 b
        t2 = ((r << 1) + r) << (2 * k)          # 3 r b^2
        trial = t1 + t2 + (1 << (3 * k))
        before, ok = rem, trial <= rem
        if ok:
            rem -= trial
            r2 = r2 + (r << (k + 1)) + (1 << (2 * k))   # (r + b)^2, before r changes
            r |= b
        out.append({"k": k, "trial": trial, "before": before, "ok": ok, "r": r, "r2": r2, "rem": rem})
    return out


def icbrt_ref(n, width=24):
    s = icbrt_steps(n, width)[-1]
    return s["r"], s["rem"]


# --- blocks ----------------------------------------------------------------------------------------

def bits(v, w):
    return format(v, f"0{w}b")


def steps_table(n=N0):
    """Part a: n = 1000 bit by bit (four columns, so a phone keeps it a table)."""
    rows = ["| ביט ‏k | הניסיון ‏2rb + b² | השארית לפני | ‏r אחרי, בבינארי |", "|:-:|:-:|:-:|:-:|"]
    for s in isqrt_steps(n):
        trial = f"**{s['trial']}** ✓" if s["ok"] else f"{s['trial']} ✗"
        r = f"{RLM}<span dir=\"ltr\">{s['r']} = <code>{bits(s['r'], 8)}</code></span>"
        rows.append(f"| {s['k']} | {trial} | {s['before']} | {r} |")
    return "\n".join(rows)


def square_figure(n=N0, k=3):
    """Part b: the step of bit k of n as areas. The square r^2 that is already in, the two
    r x b rectangles and the b x b square that the trial adds, and the dashed square of side
    sqrt(n) that bounds them."""
    st = isqrt_steps(n)
    prev = next(s for s in st if s["k"] == k + 1) if k + 1 < 8 else None
    r = prev["r"] if prev else 0
    b = 1 << k
    side = max(r + b, n ** 0.5)
    W = H = 300
    pad = 24
    u = (W - 2 * pad - 30) / side
    f = lambda v: f"{v:.1f}".rstrip("0").rstrip(".")
    x0, y0 = pad + 30, pad
    label = (f"השלב של ביט {k} בחישוב השורש של {n}, כשטחים : הריבוע r² = {r}² = {r * r} כבר בפנים, "
             f"ונוספים לו שני מלבנים של {r} על {b} וריבוע קטן של {b} על {b}, יחד {2 * r * b + b * b}, "
             f"בתוך הריבוע המקווקו שהצלע שלו √{n}")
    s = (f'<svg class="figure isq-fig" viewBox="0 0 {W} {H}" style="max-width:20rem" role="img" '
         f'aria-label="{escape(label)}">')
    rr, bb, sq = r * u, b * u, (n ** 0.5) * u
    s += f'<rect class="isq-sq-old" x="{f(x0)}" y="{f(y0)}" width="{f(rr)}" height="{f(rr)}"/>'
    s += f'<rect class="isq-sq-add" x="{f(x0 + rr)}" y="{f(y0)}" width="{f(bb)}" height="{f(rr)}"/>'
    s += f'<rect class="isq-sq-add" x="{f(x0)}" y="{f(y0 + rr)}" width="{f(rr)}" height="{f(bb)}"/>'
    s += f'<rect class="isq-sq-small" x="{f(x0 + rr)}" y="{f(y0 + rr)}" width="{f(bb)}" height="{f(bb)}"/>'
    s += f'<rect class="isq-sq-bound" x="{f(x0)}" y="{f(y0)}" width="{f(sq)}" height="{f(sq)}"/>'
    s += (f'<text class="isq-lab" x="{f(x0 + rr / 2)}" y="{f(y0 + rr / 2 + 6)}" text-anchor="middle">r² = {r * r}</text>'
          f'<text class="isq-lab" x="{f(x0 + rr + bb / 2)}" y="{f(y0 + rr / 2 + 6)}" text-anchor="middle">{r * b}</text>'
          f'<text class="isq-lab" x="{f(x0 + rr / 2)}" y="{f(y0 + rr + bb / 2 + 6)}" text-anchor="middle">{r * b}</text>'
          f'<text class="isq-lab" x="{f(x0 + rr + bb / 2)}" y="{f(y0 + rr + bb / 2 + 6)}" text-anchor="middle">{b * b}</text>')
    # the side lengths along the top and the left
    s += (f'<text class="tick" x="{f(x0 + rr / 2)}" y="{f(y0 + rr + bb + 18)}" text-anchor="middle">r = {r}</text>'
          f'<text class="tick" x="{f(x0 + rr + bb / 2)}" y="{f(y0 + rr + bb + 18)}" text-anchor="middle">b = {b}</text>'
          f'<text class="tick" x="{f(x0 - 8)}" y="{f(y0 + rr / 2 + 5)}" text-anchor="end">{r}</text>'
          f'<text class="tick" x="{f(x0 - 8)}" y="{f(y0 + rr + bb / 2 + 5)}" text-anchor="end">{b}</text>')
    s += "</svg>"
    legend = ('<span class="viz-legend">'
              f'<span><i class="isq-key-old"></i><span>‏r² = {r * r}, מה שכבר בפנים</span></span>'
              f'<span><i class="isq-key-add"></i><span>שני מלבנים ‏rb, יחד ‏2rb = {2 * r * b}</span></span>'
              f'<span><i class="isq-key-small"></i><span>‏b² = {b * b}</span></span>'
              f'<span><i class="isq-key-bound"></i><span>הריבוע שהצלע שלו ‏√{n}, השטח {n}</span></span></span>')
    return f'<div class="isq-figwrap">{s}</div>\n\n{legend}'


def or_table(n=N0, k=3):
    """Part b: why OR is enough: r << (k + 1) and 1 << 2k never share a bit."""
    st = isqrt_steps(n)
    r = next(s for s in st if s["k"] == k + 1)["r"]
    a, c = r << (k + 1), 1 << (2 * k)
    label = (f"הניסיון בביט {k} כשהשורש עד עכשיו {r} : ‏r מוזז ב-{k + 1} הוא {a}, ‏1 מוזז ב-{2 * k} הוא {c}, "
             f"ואין להם ביט משותף, ולכן OR נותן את הסכום {a | c}")
    head = "".join(f'<td class="isq-ix">{i}</td>' for i in range(15, -1, -1))

    def row(name, v, cls):
        cells = "".join(f'<td class="gs-b {"isq-one " + cls if (v >> i) & 1 else "isq-zero"}">{(v >> i) & 1}</td>'
                        for i in range(15, -1, -1))
        return f"<tr><th>{name}</th>{cells}<td class=\"isq-val\">{v}</td></tr>"

    t = (f'<div class="gs-scroll" tabindex="0" role="region" aria-label="{escape(label)}">'
         f'<table class="gs-bits isq-bits" dir="ltr" aria-label="{escape(label)}"><tbody>'
         f"<tr><th></th>{head}<td></td></tr>"
         + row(f"r &lt;&lt; {k + 1}", a, "isq-r")
         + row(f"1 &lt;&lt; {2 * k}", c, "isq-b")
         + row("OR", a | c, "isq-t")
         + "</tbody></table></div>")
    legend = ('<span class="viz-legend">'
              f'<span><i class="isq-key-r"></i><span>הביטים של ‏r = {r}, מוזזים ב-{k + 1} (‏2rb)</span></span>'
              f'<span><i class="isq-key-b"></i><span>הביט {2 * k} (‏b²)</span></span>'
              f'<span><i class="isq-key-t"></i><span>הניסיון {a | c}</span></span></span>')
    return f"{t}\n\n{legend}"


def cycles_table(n=N0):
    """Part c: the registers of isqrt_seq after every clock (busy until the last, then done)."""
    rows = ["| אחרי השעון | ‏k | ‏root | ‏rem |", "|:-:|:-:|:-:|:-:|"]
    for c, k, r, rem, busy, done in seq_cycles(n):
        when = f"{c}, ‏`start`" if c == 0 else f"**{c}, ‏`done`**" if done else str(c)
        mark = "**" if done else ""
        rows.append(f"| {when} | {k} | {mark}{r}{mark} | {mark}{rem}{mark} |")
    return "\n".join(rows)


def div_table(a=A0, d=D0):
    """Part d: 1000 / 7 by the shifted divisor; the steps before the first fit are one row."""
    st = div_steps(a, d)
    first = next(i for i, s in enumerate(st) if s["ok"])
    rows = ["| ביט ‏k | הניסיון ‏d · 2ᵏ | השארית לפני | ‏q אחרי |", "|:-:|:-:|:-:|:-:|"]
    rows.append(f"| {st[0]['k']} עד {st[first - 1]['k']} | {st[first - 1]['trial']} ומעלה ✗ | {a} | 0 |")
    for s in st[first:]:
        trial = f"**{s['trial']}** ✓" if s["ok"] else f"{s['trial']} ✗"
        mark = "**" if s["ok"] else ""
        rows.append(f"| {s['k']} | {trial} | {s['before']} | {mark}{s['q']}{mark} |")
    return "\n".join(rows)


def cbrt_table(n=C0):
    """Part d: the cube root of 1000 (width 12, four result bits), r and r² after each step."""
    rows = ["| ביט ‏k | הניסיון ‏3r²b + 3rb² + b³ | השארית לפני | ‏r, r² אחרי |", "|:-:|:-:|:-:|:-:|"]
    for s in icbrt_steps(n, 12):
        trial = f"**{s['trial']}** ✓" if s["ok"] else f"{s['trial']} ✗"
        rows.append(f"| {s['k']} | {trial} | {s['before']} | {RLM}<span dir=\"ltr\">{s['r']}, {s['r2']}</span> |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [steps_table(), square_figure(), or_table(), cycles_table(), div_table(), cbrt_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
