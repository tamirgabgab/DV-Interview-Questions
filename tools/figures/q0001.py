#!/usr/bin/env python3
"""Figures of question 0001 (the rising edge detector): the table of the four cases of
(sig, sig_q); the schematic of the page's module, one D flip-flop that keeps the previous
cycle's sig (sig_q, reset to 0 by rst_n, active low), an inverter and an AND gate,
pulse = sig & ~sig_q, and its legend; and the trap's synchronizer chain, two flip-flops in
the clk domain before the same detector.

    python tools/figures/fill.py 1        # put the blocks on the page

NETLIST is what the drawing shows; tests/0001 checks it against the page's SystemVerilog
(the flip-flop's input, reset value and the assign of pulse) by simulating both.
figure(mode) also draws the follow-ups' circuits (a falling edge: the inverter on sig; any
edge: one XOR gate); the edge box (docs/javascripts/explorer/edge.js, edgeDiagram) draws
the same shapes with the values of a clock on them, and tests/0001 compares the two.
"""

# net: (kind, inputs...) -- dff: (d, clock, active-low reset, reset value)
NETLIST = {
    "sig_q": ("dff", "sig", "clk", "rst_n", 0),
    "sig_q_n": ("not", "sig_q"),
    "pulse": ("and", "sig", "sig_q_n"),
}
# the follow-ups: the same flip-flop, another gate
NETLISTS = {
    "rise": NETLIST,
    "fall": {"sig_q": NETLIST["sig_q"], "sig_n": ("not", "sig"), "pulse": ("and", "sig_n", "sig_q")},
    "both": {"sig_q": NETLIST["sig_q"], "pulse": ("xor", "sig", "sig_q")},
}
# the trap's chain: sig from another clock domain through two flip-flops of clk (meta may be
# metastable for a while, sig_s is safe), then the detector on sig_s
SYNC_NETLIST = {
    "meta": ("dff", "sig", "clk", "rst_n", 0),
    "sig_s": ("dff", "meta", "clk", "rst_n", 0),
    "sig_q": ("dff", "sig_s", "clk", "rst_n", 0),
    "sig_q_n": ("not", "sig_q"),
    "pulse": ("and", "sig_s", "sig_q_n"),
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


def _inverter(x, y):
    return (f'<path class="ff-gate" d="M{x},{y - 12} L{x + 22},{y} L{x},{y + 12} Z"/>'
            f'<circle class="ff-gate" cx="{x + 26}" cy="{y}" r="4"/>')


def _and(x, y, h):
    w = h / 2
    return f'<path class="ff-gate" d="M{x},{y - h / 2} H{x + w} A{h / 2},{h / 2} 0 0 1 {x + w},{y + h / 2} H{x} Z"/>'


def _xor(x, y, h):
    """An XOR gate whose inputs end at x (the back arc a little to the left of it)."""
    r = h / 2
    return (f'<path class="ff-gate" d="M{x - 4},{y - r} Q{x + 10},{y} {x - 4},{y + r} '
            f'Q{x + 26},{y + r} {x + h},{y} Q{x + 26},{y - r} {x - 4},{y - r} Z"/>'
            f'<path class="ff-wire" d="M{x - 11},{y - r} Q{x + 3},{y} {x - 11},{y + r}"/>')


def figure(mode="rise"):
    """The schematic: rise is the page's module; fall and both the follow-ups' circuits."""
    s = []
    # inputs
    s.append(_t(X_IN - 6, Y_SIG + 6, "sig", "end"))
    s.append(_t(X_IN - 6, Y_CLK + 6, "clk", "end"))
    rx, ry = FX + FW / 2, FY + FH
    s.append(_t(X_IN - 6, ry + 26, "rst_n", "end"))
    # sig to the AND gate and, from the junction, to D; a falling edge inverts it on the way
    a2 = AY + 14                           # sig enters the AND gate at AY - 14 = Y_SIG
    if mode == "fall":
        s.append(_wire((X_IN, Y_SIG), (NX, Y_SIG)))
        s.append(_inverter(NX, Y_SIG))
        s.append(_wire((NX + 30, Y_SIG), (AX, Y_SIG)))
    else:
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
    # Q -> sig_q -> (the inverter of a rising edge) -> the second input of the gate
    bend = AX - 26
    s.append(_t((FX + FW + NX) / 2, Y_D - 10, "sig_q", "middle", "ff-small"))
    if mode == "rise":
        s.append(_wire((FX + FW, Y_D), (NX, Y_D)))
        s.append(_inverter(NX, Y_D))
        s.append(_wire((NX + 30, Y_D), (bend, Y_D), (bend, a2), (AX, a2)))
    else:
        s.append(_wire((FX + FW, Y_D), (bend, Y_D), (bend, a2), (AX, a2)))
    # the gate and pulse
    w = AH / 2
    s.append(_xor(AX, AY, AH) if mode == "both" else _and(AX, AY, AH))
    s.append(_wire((AX + w + AH / 2, AY), (OUT_X, AY)))
    s.append(_t(OUT_X + 6, AY + 6, "pulse", "start"))
    label = ("המעגל : sig נכנס לפליפ-פלופ D שמוציא את sig_q, הערך של המחזור הקודם, עם איפוס rst_n "
             "פעיל בנמוך. sig_q עובר דרך מהפך, ושער AND מחבר אותו עם sig ומוציא את pulse")
    return (f'<svg class="figure ff-fig" viewBox="0 0 {W} {H}" style="max-width:36rem" role="img" '
            f'aria-label="{label}">' + "".join(s) + "</svg>")


def legend():
    return ('<span class="viz-legend"><span><i class="ff-key-dot"></i>נקודה : <code>sig</code> מתפצל לשער ולפליפ-פלופ</span>'
            '<span>העיגול מתחת לפליפ-פלופ : איפוס אסינכרוני פעיל בנמוך</span></span>')


def truth_table():
    """The four cases of (sig, sig_q) and pulse, the edge row in bold."""
    what = {(0, 0): "נמוך, וגם קודם היה נמוך", (0, 1): "ירידת שפה",
            (1, 0): "**עליית שפה**", (1, 1): "גבוה כבר מהמחזור הקודם"}
    rows = ["| עכשיו, `sig` | במחזור הקודם, `sig_q` | מה קרה | המוצא, `pulse` |", "|:-:|:-:|:-:|:-:|"]
    for s in (0, 1):
        for q in (0, 1):
            p = int(s == 1 and q == 0)
            out = f"**‏{p}**" if p else f"‏{p}"
            rows.append(f"| ‏{s} | ‏{q} | {what[s, q]} | {out} |")
    return "\n".join(rows)


# the synchronizer chain: three flip-flops in a row on the data line, clk under them
SY_W, SY_H = 680, 236
SY_D, SY_TOP, SY_CLK = 128, 52, 222        # the data line, sig_s to the AND gate, the clock bus
SY_FY, SY_FW, SY_FH = 98, 56, 80           # the flip-flops (D at SY_D, the clock pin at SY_FY + 66)
SY_FX = (80, 184, 366)                     # meta, sig_s, sig_q
SY_J = 286                                 # the junction of sig_s
SY_NX = 486                                # the inverter
SY_AX, SY_AY = 566, 66                     # the AND gate: inputs at 52 and 80
SY_OUT = 640


def sync_figure():
    """sig from another clock domain -> two flip-flops (meta, sig_s) -> the edge detector."""
    s = []
    clk_y = SY_FY + 62
    s.append(f'<rect class="ed-group" x="{SY_FX[0] - 30}" y="{SY_FY - 26}" width="{SY_FX[1] + SY_FW - SY_FX[0] + 44}" '
             f'height="{SY_CLK - SY_FY + 14}" rx="6"/>')
    s.append(_t((SY_FX[0] + SY_FX[1] + SY_FW) / 2 - 8, SY_FY - 34, "synchronizer", "middle", "ff-small"))
    s.append(f'<rect class="ed-group" x="{SY_J - 14}" y="{SY_TOP - 30}" width="{SY_W - SY_J + 8}" '
             f'height="{SY_CLK - SY_TOP + 18}" rx="6"/>')
    s.append(_t((SY_J + SY_OUT) / 2 + 30, SY_CLK - 18, "edge detector", "middle", "ff-small"))
    s.append(_t(SY_FX[0] - 36, SY_D + 6, "sig", "end"))   # the input from the other domain
    s.append(_wire((SY_FX[0] - 30, SY_D), (SY_FX[0], SY_D)))
    for i, fx in enumerate(SY_FX):
        s.append(f'<rect class="ff-gate" x="{fx}" y="{SY_FY}" width="{SY_FW}" height="{SY_FH}" rx="3"/>')
        s.append(_t(fx + 7, SY_D + 6, "D", "start", "ff-pin"))
        s.append(_t(fx + SY_FW - 7, SY_D + 6, "Q", "end", "ff-pin"))
        s.append(f'<path class="ff-wire" d="M{fx},{clk_y - 7} L{fx + 10},{clk_y} L{fx},{clk_y + 7}"/>')
        s.append(_wire((fx - 14, SY_CLK), (fx - 14, clk_y), (fx, clk_y)))
    s.append(_t(SY_FX[0] - 36, SY_CLK + 6, "clk", "end"))
    s.append(_wire((SY_FX[0] - 30, SY_CLK), (SY_FX[2] - 14, SY_CLK)))
    # meta, sig_s with its junction, sig_q through the inverter, the AND gate, pulse
    s.append(_wire((SY_FX[0] + SY_FW, SY_D), (SY_FX[1], SY_D)))
    s.append(_t((SY_FX[0] + SY_FW + SY_FX[1]) / 2, SY_D - 10, "meta", "middle", "ff-small"))
    s.append(_wire((SY_FX[1] + SY_FW, SY_D), (SY_FX[2], SY_D)))
    s.append(_t(SY_J + 8, SY_D - 32, "sig_s", "start", "ff-small"))
    s.append(_wire((SY_J, SY_D), (SY_J, SY_TOP), (SY_AX, SY_TOP)))
    s.append(f'<circle class="ink-dot" cx="{SY_J}" cy="{SY_D}" r="4"/>')
    s.append(_wire((SY_FX[2] + SY_FW, SY_D), (SY_NX, SY_D)))
    s.append(_t((SY_FX[2] + SY_FW + SY_NX) / 2, SY_D - 10, "sig_q", "middle", "ff-small"))
    s.append(_inverter(SY_NX, SY_D))
    bend = SY_AX - 20
    s.append(_wire((SY_NX + 30, SY_D), (bend, SY_D), (bend, SY_AY + 14), (SY_AX, SY_AY + 14)))
    s.append(_and(SY_AX, SY_AY, 44))
    s.append(_wire((SY_AX + 44, SY_AY), (SY_OUT, SY_AY)))
    s.append(_t(SY_AX + 50, SY_AY + 28, "pulse", "start"))
    label = ("שרשרת הסנכרון : sig מדומיין שעון אחר עובר שני פליפ-פלופים של clk, meta ו-sig_s, "
             "ורק sig_s נכנס לגלאי השפה : פליפ-פלופ שלישי sig_q, מהפך ושער AND שמוציא את pulse")
    return (f'<svg class="figure ff-fig" viewBox="0 0 {SY_W} {SY_H}" style="max-width:40rem" role="img" '
            f'aria-label="{label}">' + "".join(s) + "</svg>")


def sync_legend():
    return ('<span class="viz-legend"><span><code>meta</code> : עלול להיות במטא-יציבות</span>'
            '<span><code>sig_s</code> : יציב, וממנו מזהים את השפה</span><span>האיפוס לא מצויר</span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [truth_table(), figure() + "\n\n" + legend(), sync_figure() + "\n\n" + sync_legend()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
