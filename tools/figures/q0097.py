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

import json
import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

RLM = "‏"
NB = "\u00a0"
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


def hw_cycles(n, cycles=11):
    """isqrt_seq clock by clock, the way the waveform reads: one record per cycle (the time
    from one rising edge to the next), cycle 0 the one with start high. k, root, rem, busy and
    done are the registers through the cycle (None before the load: the waveform's x); trial,
    diff = rem - trial (negative when the 17-bit subtractor borrows), borrow and fits =
    !borrow are the combinational values while busy (None otherwise); load = start & !busy;
    set is the bit of root the decoder sets at the edge (None if none); the n* fields are the
    registers that edge writes, which the next record shows."""
    out = []
    k = root = rem = None
    busy = done = 0
    for c in range(cycles):
        start = int(c == 0)
        load = int(start and not busy)
        rec = {"cycle": c, "start": start, "load": load, "k": k, "root": root, "rem": rem, "busy": busy, "done": done,
               "trial": None, "diff": None, "borrow": None, "fits": None, "set": None}
        nk, nroot, nrem, nbusy, ndone = k, root, rem, busy, 0
        if load:
            nk, nroot, nrem, nbusy = 7, 0, n, 1
        elif busy:
            trial = (root << (k + 1)) | (1 << (2 * k))
            borrow = int(trial > rem)
            rec.update(trial=trial, diff=rem - trial, borrow=borrow, fits=1 - borrow)
            if not borrow:
                nrem, nroot, rec["set"] = rem - trial, root | (1 << k), k
            if k == 0:
                nbusy, ndone = 0, 1
            else:
                nk = k - 1
        rec.update(nk=nk, nroot=nroot, nrem=nrem, nbusy=nbusy, ndone=ndone)
        out.append(rec)
        k, root, rem, busy, done = nk, nroot, nrem, nbusy, ndone
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


# --- part c: the hardware -------------------------------------------------------------------------
# The block diagram of isqrt_seq. The box (docs/javascripts/explorer/isqrthw.js) draws the same
# blocks and wires, with this cycle's values in place of the second lines; the test compares the
# two geometries.

DP_W, DP_H = 410, 346
# (id, x, y, w, h, class, title, second line)
DP_BLOCKS = (
    ("k", 10, 14, 70, 44, "reg", "k", "3 bits"),
    ("root", 118, 14, 130, 44, "reg", "root", "8 bits"),
    ("rem", 284, 14, 108, 44, "reg", "rem", "16 bits"),
    ("shift", 118, 92, 126, 44, "mux", "trial", "a mux on k"),
    ("sub", 284, 92, 108, 44, "stage", "rem − trial", "diff and borrow"),
    ("dec", 118, 166, 124, 44, "mux", "decoder", "root[k] ← 1"),
    ("fits", 278, 166, 92, 40, "ctl", "fits", "= !borrow"),
    ("ctl", 10, 246, 238, 44, "ctl", "control", "load, busy, done, k ← k − 1"),
    ("mux", 284, 246, 108, 44, "mux", "rem mux", "n, diff or rem"),
)
# (id, points, arrow head, label, label x, label y, anchor)
DP_WIRES = (
    ("k_ctl", ((28, 58), (28, 246)), True, "k", 32, 232, "start"),
    ("ctl_k", ((62, 246), (62, 58)), True, "k − 1", 66, 232, "start"),
    ("k_dec", ((80, 36), (92, 36), (92, 180), (118, 180)), True, "", 0, 0, ""),
    ("k_sh", ((146, 74), (146, 92)), True, "k", 152, 84, "start"),
    ("root_sh", ((183, 58), (183, 92)), True, "", 0, 0, ""),
    ("sh_sub", ((244, 114), (284, 114)), True, "trial", 264, 105, "middle"),
    ("rem_sub", ((338, 58), (338, 92)), True, "", 0, 0, ""),
    ("borrow", ((304, 136), (304, 166)), True, "borrow", 299, 155, "end"),
    ("fits_dec", ((278, 194), (242, 194)), True, "fits", 260, 188, "middle"),
    ("fits_mux", ((316, 206), (316, 246)), True, "fits", 312, 232, "end"),
    ("diff", ((382, 136), (382, 246)), True, "diff", 378, 232, "end"),
    ("mux_rem", ((392, 268), (401, 268), (401, 36), (392, 36)), True, "", 0, 0, ""),
    ("dec_root", ((146, 166), (146, 150), (104, 150), (104, 66), (128, 66), (128, 58)), True, "", 0, 0, ""),
    ("ctl_dec", ((183, 246), (183, 210)), True, "load, busy", 187, 232, "start"),
    ("ctl_mux", ((248, 268), (284, 268)), True, "", 0, 0, ""),
    ("start", ((56, 318), (56, 290)), True, "start", 56, 332, "middle"),
    ("out", ((170, 290), (170, 318)), True, "busy, done", 170, 332, "middle"),
    ("n", ((338, 318), (338, 290)), True, "n", 338, 332, "middle"),
)


def dp_wire(pts, cls="isq-wire", arrow=True, marker="isq-hb"):
    d = "M" + " L".join(f"{x:g},{y:g}" for x, y in pts)
    return f'<path class="{cls}" d="{d}"' + (f' marker-end="url(#{marker})"' if arrow else "") + "/>"


def datapath_svg():
    """Part c: the block diagram of isqrt_seq. The registers k, root and rem; the shifter that
    makes the trial (a mux on k); one 17-bit subtractor whose borrow is the comparison
    (fits = !borrow); the decoder that sets root[k]; the multiplexer back into rem; the
    control (load, busy, done, k counting down)."""
    label = ("תרשים המלבנים של isqrt_seq" + NB + ": שלושה רגיסטרים, k של 3 ביטים, root של 8 ו-rem של 16. "
             "המזיז בוחר לפי k את הניסיון מתוך root. מחסר אחד מחשב rem פחות trial, וה-borrow שלו הוא ההשוואה" + NB + ": "
             "fits הוא ההפך של borrow. המפענח מדליק את root[k] כש-fits, והמרבב כותב ל-rem את n ב-load, את diff כש-fits, "
             "ואחרת את rem עצמו. הבקרה מחשבת load מ-start, מורידה את k ב-1 בכל מחזור של busy, ומעלה את done כש-k הוא 0")
    o = [f'<svg class="figure isq-fig isq-dp" viewBox="0 0 {DP_W} {DP_H}" direction="ltr" style="max-width:{DP_W / 16:g}rem" '
         f'role="img" aria-label="{escape(label)}">',
         '<defs><marker id="isq-hb" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" '
         'markerHeight="9" orient="auto"><path class="isq-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>']
    for _id, x, y, w, h, cls, title, sub in DP_BLOCKS:
        o.append(f'<g class="isq-blk isq-{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>'
                 f'<text x="{x + w / 2:g}" y="{y + h / 2 - 3:g}" text-anchor="middle">{escape(title)}</text>'
                 f'<text class="isq-sub" x="{x + w / 2:g}" y="{y + h / 2 + 13:g}" text-anchor="middle">{escape(sub)}</text></g>')
    for _id, pts, arrow, lab, lx, ly, anchor in DP_WIRES:
        o.append(dp_wire(pts, arrow=arrow))
        if lab:
            o.append(f'<text class="isq-wlab" x="{lx}" y="{ly}" text-anchor="{anchor}">{escape(lab)}</text>')
    return "".join(o) + "</svg>"


def cycles_table(n=N0):
    """Part c: isqrt_seq on n cycle by cycle, a row for each cycle of the waveform: the registers
    through the cycle, the trial and its fit computed in it (written at the edge that ends it)."""
    rows = ["| מחזור | ‏k | הניסיון ‏trial | נכנס? ‏fits | ‏root | ‏rem | ‏busy | ‏done |", "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    dash = lambda v: "–" if v is None else str(v)
    for c in hw_cycles(n):
        when = f"**{c['cycle']}**" if c["done"] else str(c["cycle"])
        fit = "–" if c["fits"] is None else "✓" if c["fits"] else "✗"
        trial = dash(c["trial"])
        if c["fits"]:
            trial = f"**{trial}**"
        mark = "**" if c["done"] else ""
        cells = [when, dash(c["k"]), trial, fit, f"{mark}{dash(c['root'])}{mark}", f"{mark}{dash(c['rem'])}{mark}",
                 str(c["busy"]), f"{mark}{c['done']}{mark}"]
        rows.append("| " + " | ".join(cells) + " |")
    return "\n".join(rows)


def wave_lane(values):
    """A WaveDrom lane of numbers: '=' where the value changes (with its text), '.' where it
    holds, 'x' where there is none."""
    wave, data, prev = "", [], object()
    for v in values:
        if v == prev:
            wave += "."
        elif v is None:
            wave += "x"
        else:
            wave += "="
            data.append(str(v))
        prev = v
    return wave, data


def bit_lane(values):
    wave, prev = "", object()
    for v in values:
        wave += "." if v == prev else "x" if v is None else str(v)
        prev = v
    return wave


def wavedrom_block(n=N0):
    """Part c: the waveform of isqrt_seq on n, a slot for each cycle of the table; the lane
    named cycle numbers them (the waveform viewer leaves it out of its log)."""
    cy = hw_cycles(n)
    lanes = [f'  {{ name: "clk",   wave: "p{"." * (len(cy) - 1)}" }}',
             f'  {{ name: "cycle", wave: "{"=" * len(cy)}", data: {json.dumps([str(c["cycle"]) for c in cy])} }}']
    for name in ("start", "busy"):
        lanes.append(f'  {{ name: "{name}",{" " * (6 - len(name))}wave: "{bit_lane([c[name] for c in cy])}" }}')
    for name in ("k", "trial"):
        w, d = wave_lane([c[name] for c in cy])
        lanes.append(f'  {{ name: "{name}",{" " * (6 - len(name))}wave: "{w}", data: {json.dumps(d)} }}')
    lanes.append(f'  {{ name: "fits",  wave: "{bit_lane([c["fits"] for c in cy])}" }}')
    for name in ("root", "rem"):
        w, d = wave_lane([c[name] for c in cy])
        lanes.append(f'  {{ name: "{name}",{" " * (6 - len(name))}wave: "{w}", data: {json.dumps(d)} }}')
    lanes.append(f'  {{ name: "done",  wave: "{bit_lane([c["done"] for c in cy])}" }}')
    return "```wavedrom\n{ signal: [\n" + ",\n".join(lanes) + "\n]}\n```"


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
    return [steps_table(), square_figure(), or_table(), datapath_svg(), cycles_table(), wavedrom_block(), div_table(),
            cbrt_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
