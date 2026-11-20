#!/usr/bin/env python3
"""Figures and tables of question 0115, the monitor that sees mismatches the DUT does not have.

    python tools/figures/fill.py 115        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. Every value comes from run(), a model of one edge after another: at edge k
the driver writes row k - 1 of the stimulus, the DUT takes either that new row or the old one
(row k - 2), and the monitor reads the input and the output before or after the write. The
five readings the page names are VIEWS; tests/0115 checks each one against Verilator 5.053
(tb.sv) and cocotb 2.1 (the page's Python, run by run_cocotb).
"""

from __future__ import annotations

import json

NB = " "
RLM = "‏"

V = [1, 1, 1, 0, 0, 1, 1, 1, 0, 0]      # the stimulus of the page: in_valid of every cycle
D = [5, 9, 9, 9, 9, 2, 6, 6, 6, 6]      # in_data, held while in_valid is low
EDGES = 12                              # the edges the model runs (the benches run 13)
CYCLES = 10                             # the cycles the page shows

# (the DUT takes the new row, the monitor reads the new input, the monitor reads the output
# after the edge's update)
VIEWS = {
    "found": (1, 0, 0),     # = (or Immediate), the monitor first: Verilator's order
    "swap": (1, 1, 0),      # = (or Immediate), the driver first
    "after": (1, 1, 1),     # = (or Immediate), the monitor after the edge: negedge or ReadOnly()
    "fixed": (0, 0, 0),     # <=, a clocking block, the falling-edge driver, a plain cocotb write
    "fixed_after": (0, 1, 1),   # a plain cocotb write, the monitor in ReadOnly()
}


def row(i):
    """(in_valid, in_data) driven at edge i + 1; before the first edge both are 0."""
    if i < 0:
        return (0, 0)
    return (V[min(i, len(V) - 1)], D[min(i, len(D) - 1)])


def plus1(r):
    return (r[0], (r[1] + 1) % 256)


def item(r):
    return str(r[1]) if r[0] else "none"


def run(view="found"):
    """Edge by edge: what the monitor read, what the DUT took, what the monitor expected and
    got, and the mismatches as (cycle, expected, got)."""
    dut_new, mon_new, mon_after = VIEWS[view]
    out = [(0, 0)]                       # the output after edge k (Verilator starts at 0)
    for k in range(1, EDGES + 1):
        out.append(plus1(row(k - 1 if dut_new else k - 2)))
    exp, edges, mismatches = (0, 0), [], []
    for k in range(1, EDGES + 1):
        read = row(k - 1 if mon_new else k - 2)
        got = out[k] if mon_after else out[k - 1]
        bad = got[0] != exp[0] or (exp[0] and got[1] != exp[1])
        edges.append(dict(k=k, read=read, took=row(k - 1 if dut_new else k - 2), exp=exp, got=got, bad=bad,
                          wave_in=row(k - 1), wave_out=out[k]))
        if bad:
            mismatches.append((k, exp, got))
        exp = plus1(read)
    return dict(edges=edges, mismatches=mismatches)


def mismatch_cycles(view="found"):
    return [k for k, _, _ in run(view)["mismatches"]]


def log_lines(view="found"):
    r = run(view)
    lines = [f"cycle {k}: expected {item(e)}, got {item(g)}" for k, e, g in r["mismatches"]]
    return lines + [f"{len(lines)} mismatches"]


def wave_string(view="found"):
    """tb.sv's want string: input and output after every edge, as valid/data:valid/data."""
    return " ".join(f"{e['wave_in'][0]}/{e['wave_in'][1]}:{e['wave_out'][0]}/{e['wave_out'][1]}" for e in run(view)["edges"])


# --- block 0: the log ---------------------------------------------------------------------

def log_block():
    return "```text\n" + "\n".join(log_lines()) + "\n```"


# --- block 1: the waveform of the dump ------------------------------------------------------

def bit_lane(values):
    wave, prev = "", None
    for v in values:
        wave += "." if v == prev else str(v)
        prev = v
    return wave


def bus_lane(values):
    wave, data, prev = "", [], None
    for v in values:
        if v == prev:
            wave += "."
        else:
            wave += "="
            data.append(str(v))
        prev = v
    return wave, data


def wave_block():
    edges = run()["edges"][:CYCLES]
    n = len(edges)
    lanes = [f'  {{ name: "clk",       wave: "p{"." * (n - 1)}" }}',
             f'  {{ name: "cycle",     wave: "{"=" * n}", data: {json.dumps([str(e["k"]) for e in edges])} }}',
             f'  {{ name: "in_valid",  wave: "{bit_lane([e["wave_in"][0] for e in edges])}" }}']
    w, d = bus_lane([e["wave_in"][1] for e in edges])
    lanes.append(f'  {{ name: "in_data",   wave: "{w}", data: {json.dumps(d)} }}')
    lanes.append(f'  {{ name: "out_valid", wave: "{bit_lane([e["wave_out"][0] for e in edges])}" }}')
    w, d = bus_lane([e["wave_out"][1] for e in edges])
    lanes.append(f'  {{ name: "out_data",  wave: "{w}", data: {json.dumps(d)} }}')
    lanes.append(f'  {{ name: "mismatch",  wave: "{bit_lane([int(e["bad"]) for e in edges])}" }}')
    return "```wavedrom\n{ signal: [\n" + ",\n".join(lanes) + "\n]}\n```"


# --- blocks 2 and 3: one edge, enlarged ---------------------------------------------------

EDGE = 2                                 # the edge of the figure: 5 before the write, 9 after
W = 400
X0 = 74                                  # the lanes start here; their names end at X0 - 6
COLS = [("Preponed", 64), ("Active", 112), ("NBA", 72), ("Re-NBA", 72)]
PANEL = 132


def col(i, frac=0.5):
    """An x inside region i, at a fraction of its width."""
    x = X0
    for _, w in COLS[:i]:
        x += w
    return x + COLS[i][1] * frac


def bus(y, segments):
    """A bus lane: segments of (x from, x to, text), a slanted change between two."""
    out, h, s = [], 8, 4
    last = len(segments) - 1
    for n, (a, b, text) in enumerate(segments):
        left = [(a + s, y - h)] if n else [(a, y - h)]
        right = [(b - s, y - h), (b, y), (b - s, y + h)] if n < last else [(b, y - h), (b, y + h)]
        tail = [(a + s, y + h), (a, y)] if n else [(a, y + h)]
        pts = " ".join(f"{px:.0f},{py}" for px, py in left + right + tail)
        out.append(f'<polygon class="ink-line" fill="none" stroke-width="1.5" points="{pts}"/>'
                   f'<text class="tick" x="{(a + b) / 2:.0f}" y="{y + 5}" text-anchor="middle" style="font-size:14px">{text}</text>')
    return "".join(out)


def mark(x, y, cls, label):
    return (f'<circle class="{cls}" cx="{x:.0f}" cy="{y}" r="5"/>'
            f'<text class="tick" x="{x:.0f}" y="{y - 14}" text-anchor="middle" style="font-size:14px">{label}</text>')


def panel(y0, title, fixed):
    """One panel: the regions of the edge's time step, clk, in_data and out_data, and where
    the monitor reads, the driver writes and the DUT reads."""
    e = run("fixed" if fixed else "found")["edges"][EDGE - 1]
    old, new = row(EDGE - 2)[1], row(EDGE - 1)[1]
    before = run("fixed" if fixed else "found")["edges"][EDGE - 2]["wave_out"][1]
    after = e["wave_out"][1]
    s = [f'<text class="legend" x="6" y="{y0 + 15}" style="font-size:15px">{title}</text>']
    top, bottom = y0 + 24, y0 + PANEL - 6
    x = X0
    for name, w in COLS:
        s.append(f'<line class="grid" x1="{x}" x2="{x}" y1="{top}" y2="{bottom}" stroke-dasharray="3 3"/>'
                 f'<text class="tick" x="{x + w / 2:.0f}" y="{y0 + 38}" text-anchor="middle" style="font-size:13px">{name}</text>')
        x += w
    s.append(f'<line class="grid" x1="{x}" x2="{x}" y1="{top}" y2="{bottom}" stroke-dasharray="3 3"/>')
    yc, yi, yo = y0 + 56, y0 + 90, y0 + 116
    rise = col(1, 0.0) + 3
    s.append(f'<path class="ink-line" fill="none" stroke-width="1.5" d="M{X0},{yc + 7} L{rise:.0f},{yc + 7} '
             f'L{rise + 4:.0f},{yc - 7} L{x},{yc - 7}"/>')
    for name, y in (("clk", yc), ("in_data", yi), ("out_data", yo)):
        s.append(f'<text class="tick" x="{X0 - 6}" y="{y + 5}" text-anchor="end" style="font-size:14px">{name}</text>')
    write = col(3) if fixed else col(1)
    s.append(bus(yi, [(X0, write, old), (write, x, new)]))
    upd = col(2)
    s.append(bus(yo, [(X0, upd, before), (upd, x, after)]))
    if fixed:
        s += [mark(col(0), yi, "s1-dot", "mon"), mark(col(1), yi, "s2-dot", "DUT"), mark(write, yi, "ink-dot", "drv")]
    else:
        s += [mark(col(1, 0.18), yi, "s1-dot", "mon"), mark(write, yi, "ink-dot", "drv"), mark(col(1, 0.82), yi, "s2-dot", "DUT")]
    return "".join(s)


def edge_figure():
    h = 2 * PANEL + 8
    label = (f"הקצה של מחזור {EDGE} מוגדל לאזורי התזמון. למעלה, עם כתיבה חוסמת, ה-monitor קורא {row(EDGE - 2)[1]} "
             f"וה-DUT קורא {row(EDGE - 1)[1]}. למטה, עם clocking block, שניהם קוראים {row(EDGE - 2)[1]}")
    return (f'<svg class="perf-chart" viewBox="0 0 {W} {h}" style="max-width:30rem" role="img" aria-label="{label}">'
            + panel(0, "in_data = D[i]   (blocking, as found)", False)
            + panel(PANEL + 8, "drv_cb.in_data &lt;= D[i]   (clocking block)", True)
            + "</svg>")


def legend():
    return ('<span class="viz-legend">'
            '<span><i class="s1"></i>הקריאה של ה-monitor (mon)</span>'
            '<span><i class="ink"></i>הכתיבה של ה-driver (drv)</span>'
            '<span><i class="s2"></i>הקריאה של ה-<code>always_ff</code> של ה-DUT (DUT)</span>'
            '</span>')


# --- block 4: the mismatches, edge by edge --------------------------------------------------

def cell(r):
    return str(r[1]) if r[0] else "—"


def edge_table():
    out = ["| מחזור | ה-monitor קרא | ה-DUT לקח | ה-monitor מצפה | ביציאה | שגיאה |",
           "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for e in run()["edges"][:CYCLES]:
        mark_ = "✗" if e["bad"] else ""
        out.append(f"| {e['k']} | {cell(e['read'])} | {cell(e['took'])} | {cell(e['exp'])} | {cell(e['got'])} | {mark_} |")
    return "\n".join(out)


# --- block 5: every version ---------------------------------------------------------------

def verdict(view):
    cycles = mismatch_cycles(view)
    if not cycles:
        return "0"
    return f"{len(cycles)}{NB}: במחזורים {', '.join(map(str, cycles[:-1]))} ו-{cycles[-1]}"


# (the version, how the input is written at the edge, what the DUT takes, what the monitor
# reads, the view) -- tests/0115 maps every row to the run that checks it
VERSIONS = [
    ("ב-SystemVerilog, כמו שנמצאה", "‏`=` ב-Active, בין שני הקוראים", "החדש", "הישן", "found"),
    ("אותה סביבה, `drive()` ראשון ב-fork", "‏`=` ב-Active, לפני שני הקוראים", "החדש", "החדש", "swap"),
    ("רק ה-monitor דרך clocking block", "‏`=` ב-Active", "החדש", "הישן, מה-Preponed", "found"),
    ("רק ה-monitor בירידה של השעון", "‏`=` ב-Active", "החדש", "הכול אחרי הקצה", "after"),
    ("התיקון : clocking block, בשני הסדרים", "ב-Re-NBA", "הישן", "הישן, מה-Preponed", "fixed"),
    ("תיקון : `<=` ב-driver", "ב-NBA", "הישן", "הישן", "fixed"),
    ("תיקון : driver בירידה של השעון", "חצי מחזור לפני הקצה", "היחיד", "היחיד", "fixed"),
    ("ב-cocotb, כמו שנמצאה (`Immediate`)", "מיד, בתוך הקצה", "החדש", "הישן", "found"),
    ("אותה סביבה, ה-driver מתחיל ראשון", "מיד, לפני שני הקוראים", "החדש", "החדש", "swap"),
    ("אותה סביבה, ה-monitor ב-`ReadOnly()`", "מיד, בתוך הקצה", "החדש", "הכול אחרי הקצה", "after"),
    ("התיקון : כתיבה רגילה, בשני הסדרים", "ב-ReadWrite, אחרי הקצה", "הישן", "הישן", "fixed"),
    ("התיקון, ה-monitor ב-`ReadOnly()`", "ב-ReadWrite, אחרי הקצה", "הישן", "הכול אחרי הקצה", "fixed_after"),
]


def versions_table():
    out = ["| הגרסה | הכתיבה של ה-driver | ה-DUT לוקח | ה-monitor קורא | שגיאות |", "|---|---|:-:|:-:|---|"]
    for name, write, dut, mon, view in VERSIONS:
        out.append(f"| {name.replace(' :', NB + ':')} | {write} | {dut} | {mon} | {verdict(view)} |")
    return "\n".join(out)


def blocks():
    """The generated blocks, in page order."""
    return [log_block(), wave_block(), edge_figure(), legend(), edge_table(), versions_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
