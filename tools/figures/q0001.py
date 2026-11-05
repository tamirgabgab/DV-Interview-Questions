#!/usr/bin/env python3
"""Figure of question 0001 (the rising edge detector): the schematic of the page's module,
one D flip-flop that keeps the previous cycle's sig (sig_q, reset to 0 by rst_n, active
low), an inverter and an AND gate, pulse = sig & ~sig_q, and its legend.

    python tools/figures/fill.py 1        # put the blocks on the page

NETLIST is what the drawing shows; tests/0001 checks it against the page's SystemVerilog
(the flip-flop's input, reset value and the assign of pulse) by simulating both.
"""

# net: (kind, inputs...) -- dff: (d, clock, active-low reset, reset value)
NETLIST = {
    "sig_q": ("dff", "sig", "clk", "rst_n", 0),
    "sig_q_n": ("not", "sig_q"),
    "pulse": ("and", "sig", "sig_q_n"),
}
INPUTS = ("sig", "clk", "rst_n")

X_IN = 68                                  # where the input wires start (labels end left of it)
Y_SIG, Y_D, Y_CLK = 44, 116, 150
JX = 128                                   # the junction that sends sig to the flip-flop
FX, FY, FW, FH = 178, 96, 70, 80           # the flip-flop
NX = 318                                   # the inverter
AX, AY, AH = 408, 58, 44                   # the AND gate: inputs at AY -+ 14
OUT_X = 510
W, H = 580, 212


def _t(x, y, s, anchor="middle", cls="ff-text"):
    return f'<text class="{cls}" x="{x:g}" y="{y:g}" text-anchor="{anchor}">{s}</text>'


def _wire(*pts):
    return '<polyline class="ff-wire" points="' + " ".join(f"{x:g},{y:g}" for x, y in pts) + '"/>'


def figure():
    s = []
    # inputs
    s.append(_t(X_IN - 6, Y_SIG + 6, "sig", "end"))
    s.append(_t(X_IN - 6, Y_CLK + 6, "clk", "end"))
    rx, ry = FX + FW / 2, FY + FH
    s.append(_t(X_IN - 6, ry + 26, "rst_n", "end"))
    # sig to the AND gate and, from the junction, to D
    a2 = AY + 14                           # sig enters the AND gate at AY - 14 = Y_SIG
    s.append(_wire((X_IN, Y_SIG), (AX, Y_SIG)))
    s.append(_wire((JX, Y_SIG), (JX, Y_D), (FX, Y_D)))
    s.append(f'<circle class="ink-dot" cx="{JX}" cy="{Y_SIG}" r="4"/>')
    # the flip-flop: D, the clock's triangle, Q, the active-low reset as a bubble below
    s.append(f'<rect class="ff-gate" x="{FX}" y="{FY}" width="{FW}" height="{FH}" rx="3"/>')
    s.append(_t(FX + 8, Y_D + 6, "D", "start", "ff-pin"))
    s.append(_t(FX + FW - 8, Y_D + 6, "Q", "end", "ff-pin"))
    s.append(_wire((X_IN, Y_CLK), (FX, Y_CLK)))
    s.append(f'<path class="ff-wire" d="M{FX},{Y_CLK - 7} L{FX + 10},{Y_CLK} L{FX},{Y_CLK + 7}"/>')
    s.append(f'<circle class="ff-gate" cx="{rx:g}" cy="{ry + 4}" r="4"/>')
    s.append(_wire((rx, ry + 8), (rx, ry + 20), (X_IN, ry + 20)))
    # Q -> sig_q -> the inverter -> the second input of the AND gate
    s.append(_wire((FX + FW, Y_D), (NX, Y_D)))
    s.append(_t((FX + FW + NX) / 2, Y_D - 10, "sig_q", "middle", "ff-small"))
    s.append(f'<path class="ff-gate" d="M{NX},{Y_D - 12} L{NX + 22},{Y_D} L{NX},{Y_D + 12} Z"/>'
             f'<circle class="ff-gate" cx="{NX + 26}" cy="{Y_D}" r="4"/>')
    bend = AX - 26
    s.append(_wire((NX + 30, Y_D), (bend, Y_D), (bend, a2), (AX, a2)))
    # the AND gate and pulse
    w = AH / 2
    s.append(f'<path class="ff-gate" d="M{AX},{AY - AH / 2} H{AX + w} A{AH / 2},{AH / 2} 0 0 1 '
             f'{AX + w},{AY + AH / 2} H{AX} Z"/>')
    s.append(_wire((AX + w + AH / 2, AY), (OUT_X, AY)))
    s.append(_t(OUT_X + 6, AY + 6, "pulse", "start"))
    label = ("המעגל : sig נכנס לפליפ-פלופ D שמוציא את sig_q, הערך של המחזור הקודם, עם איפוס rst_n "
             "פעיל בנמוך. sig_q עובר דרך מהפך, ושער AND מחבר אותו עם sig ומוציא את pulse")
    return (f'<svg class="figure ff-fig" viewBox="0 0 {W} {H}" style="max-width:36rem" role="img" '
            f'aria-label="{label}">' + "".join(s) + "</svg>")


def legend():
    return ('<span class="viz-legend"><span><i class="ff-key-dot"></i>נקודה : <code>sig</code> מתפצל לשער ולפליפ-פלופ</span>'
            '<span>העיגול מתחת לפליפ-פלופ : איפוס אסינכרוני פעיל בנמוך</span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [figure() + "\n\n" + legend()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
