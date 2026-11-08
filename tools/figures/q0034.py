#!/usr/bin/env python3
"""Figures of question 0034, Gray-code pointers of an asynchronous FIFO.

    python tools/figures/fill.py 34        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. The functions above blocks() are the reference the question's tests and the
hardware box (docs/javascripts/explorer/grayhw.js) use: a FIFO of 16 entries with pointers of
5 bits, its two clocks, the wires that cross between them (every bit with its own delay) and
the two-flop synchronizers, edge by edge.

Time is counted in ticks: wclk has a period of 20 ticks, rclk of 30, and a WaveDrom slot is
10 ticks. A bit of a pointer register reaches the other domain DELAY[i] ticks after the edge
that changed it (its clock-to-q and its wire; bit 4 the fastest). An edge that falls on the
very tick a bit changes catches that bit metastable; the bit then settles to its old or its
new value (the scenario says which), and every other bit is sampled as it is.
"""

from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

RLM = "‏"
NB = " "

BITS = 5                     # the pointers: 4 address bits and the extra bit (part c)
SIZE = 1 << BITS             # 32 values
ENTRIES = 16
FULL_FLIP = 3 << (BITS - 2)  # the two top bits of a Gray pointer, inverted for full
PW, PR = 20, 30              # the clock periods in ticks
SLOT = 10                    # ticks in a WaveDrom slot
DELAY = (9, 7, 5, 3, 1)      # bit i reaches the other domain DELAY[i] ticks after its edge


# --- the reference ---------------------------------------------------------------------------------

def gray(b: int) -> int:
    return b ^ (b >> 1)


def gray2bin(g: int, bits: int = BITS) -> int:
    b = acc = 0
    for i in range(bits - 1, -1, -1):
        acc ^= (g >> i) & 1
        b |= acc << i
    return b


def place(old: int, bits: int, seen: int) -> tuple[str, int]:
    """Where a value seen in place of the step old -> old + 1 lies: "old", "new", "behind"
    (a value the pointer held before, d steps before old) or "ahead" (one it has not reached,
    d steps after new). The changing bits are the k low ones; the values they can make are a
    window of 2^k around the step, half on each side (the wrap to 0 included)."""
    size = 1 << bits
    k = bin(old ^ ((old + 1) % size)).count("1")
    d = (seen - old) % size
    if d > 1 << (k - 1):
        d -= size
    if d == 0:
        return "old", 0
    if d == 1:
        return "new", 0
    return ("ahead", d - 1) if d > 1 else ("behind", -d)


SCENARIOS = {
    # the page's example: three words into an empty FIFO; the second word's Gray bit changes
    # on an rclk edge, is caught metastable and settles to its new value
    "page": {"mode": "gray", "p0": 0, "r0": 29, "writes": [1, 2, 3], "read_from": 1, "reads": None, "settle": "new", "end": 230},
    # the same, the metastable bit settles to its old value
    "old": {"mode": "gray", "p0": 0, "r0": 29, "writes": [1, 2, 3], "read_from": 1, "reads": None, "settle": "old", "end": 230},
    # the binary pointer through the synchronizer: 7 -> 8 with an rclk edge in the middle
    "bin": {"mode": "bin", "p0": 7, "r0": 24, "writes": [1], "read_from": 1, "reads": None, "settle": "new", "end": 170},
    # the Gray value of the binary register, computed by XORs and synchronized unregistered
    "comb": {"mode": "comb", "p0": 7, "r0": 24, "writes": [1], "read_from": 1, "reads": None, "settle": "new", "end": 170},
    # writes on every wclk edge, the reader stopped until it reads one word: full and back
    "full": {"mode": "gray", "p0": 0, "r0": 29, "writes": list(range(1, 23)), "read_from": 11, "reads": 1, "settle": "new", "end": 450},
}


class Wire:
    """The bits of a register as the other domain sees them: each bit's changes, in time."""

    def __init__(self, value: int):
        self.hist = [[(-10 ** 9, (value >> i) & 1)] for i in range(BITS)]

    def change(self, t: int, old: int, new: int):
        for i in range(BITS):
            if (old ^ new) >> i & 1:
                self.hist[i].append((t + DELAY[i], (new >> i) & 1))

    def at(self, t: int, inclusive: bool) -> int:
        v = 0
        for i, h in enumerate(self.hist):
            bit = [b for c, b in h if (c <= t if inclusive else c < t)][-1]
            v |= bit << i
        return v


def sample(wire: Wire, mode: str, t: int, settle: str) -> tuple[int, int]:
    """The value a synchronizer's first flop takes at edge t, and the mask of the bits it
    caught metastable (those that change on tick t, after the XORs in mode comb)."""
    after, before = wire.at(t, True), wire.at(t, False)
    if mode == "comb":
        after, before = gray(after), gray(before)
    return (after if settle == "new" else before), after ^ before


def edges(sc: dict) -> list[tuple[int, str, int]]:
    """Every clock edge up to the scenario's end: (tick, "w" or "r", the clock's edge number)."""
    out = [(PW * k, "w", k) for k in range(1, sc["end"] // PW + 1)]
    out += [(PR * k + sc["r0"], "r", k + 1) for k in range(0, (sc["end"] - sc["r0"]) // PR + 1)]
    out.sort()
    assert len({t for t, _, _ in out}) == len(out), "two edges on one tick"
    return out


def hw_trace(name: str | dict = "page") -> list[dict]:
    """The FIFO edge by edge. Every record has the clock that ticked (clk, t, k) and every
    register after the edge: the write side's wbin, wgray, wfull and the synchronizer wq1, wq2
    (the read pointer as the writer sees it), the read side's rbin, rgray, rempty, rq1, rq2.
    The edge's own signals: inc (winc or rinc), want (the writer has a word), meta (the bits the
    first flop caught metastable), cmp (the value the flag compares the far pointer with),
    seen (the words the side believes it has: written for the reader, in use for the writer,
    from its synchronized copy) and true (the words really in the FIFO at that tick). name is
    a key of SCENARIOS or a scenario of the same shape."""
    sc = SCENARIOS[name] if isinstance(name, str) else name
    mode, settle = sc["mode"], sc["settle"]
    p0 = sc["p0"]
    far = (lambda b: b) if mode == "bin" else gray              # what crosses: the binary or the Gray
    as_bin = (lambda v: v) if mode == "bin" else gray2bin
    s = {"wbin": p0, "wgray": gray(p0), "wfull": 0, "wq1": far(p0), "wq2": far(p0),
         "rbin": p0, "rgray": gray(p0), "rempty": 1, "rq1": far(p0), "rq2": far(p0)}
    wwire, rwire = Wire(s["wgray"] if mode == "gray" else p0), Wire(s["rgray"] if mode == "gray" else p0)
    reads, out = 0, []
    for t, clk, k in edges(sc):
        rec = {"clk": clk, "t": t, "k": k}
        if clk == "w":
            want = k in sc["writes"]
            inc = int(want and not s["wfull"])
            wbin = (s["wbin"] + inc) % SIZE
            wg = gray(wbin)
            cmp = wbin if mode == "bin" else wg
            far_r = s["wq2"] ^ (ENTRIES if mode == "bin" else FULL_FLIP)
            q1, meta = sample(rwire, mode, t, settle)
            wwire.change(t, s["wgray"] if mode == "gray" else s["wbin"], wg if mode == "gray" else wbin)
            s.update(wbin=wbin, wgray=wg, wfull=int(cmp == far_r), wq2=s["wq1"], wq1=q1)
            rec.update(want=int(want), inc=inc, meta=meta, cmp=far_r,
                       seen=(s["wbin"] - as_bin(s["wq2"])) % SIZE, true=(s["wbin"] - s["rbin"]) % SIZE)
        else:
            inc = int(not s["rempty"] and k >= sc["read_from"] and (sc["reads"] is None or reads < sc["reads"]))
            reads += inc
            rbin = (s["rbin"] + inc) % SIZE
            rg = gray(rbin)
            cmp = rbin if mode == "bin" else rg
            q1, meta = sample(wwire, mode, t, settle)
            rwire.change(t, s["rgray"] if mode == "gray" else s["rbin"], rg if mode == "gray" else rbin)
            far_w = s["rq2"]
            s.update(rbin=rbin, rgray=rg, rempty=int(cmp == far_w), rq2=s["rq1"], rq1=q1)
            rec.update(want=0, inc=inc, meta=meta, cmp=far_w,
                       seen=(as_bin(s["rq2"]) - s["rbin"]) % SIZE, true=(s["wbin"] - s["rbin"]) % SIZE)
        rec.update(s)
        out.append(rec)
    return out


def first_word_latency(name: str = "page") -> tuple[int, int, int]:
    """The first write's wire change (the tick its Gray bit reaches rclk's domain), the edge
    where rempty falls, and the rclk edges between them."""
    tr = hw_trace(name)
    w = next(r for r in tr if r["clk"] == "w" and r["inc"])
    change = w["t"] + max(DELAY[i] for i in range(BITS) if (gray(w["wbin"]) ^ gray(w["wbin"] - 1)) >> i & 1)
    fall = next(r for r in tr if r["clk"] == "r" and not r["rempty"])
    n = sum(1 for r in tr if r["clk"] == "r" and change <= r["t"] <= fall["t"])
    return change, fall["t"], n


# --- the block diagram -------------------------------------------------------------------------------
# Drawn left to right (direction="ltr"): the write domain above the dashed line, the read domain
# under it. The box draws the same blocks and wires with this edge's values; the test compares
# the two geometries.

DP_W, DP_H = 420, 352
COLS = (20, 122, 224, 326)
BW, BH = 76, 44
ROWS = {"w1": 30, "w2": 110, "r2": 206, "r1": 286}
BOUNDARY = 180
# (id, column, row, class, title, second line, domain)
DP_BLOCKS = (
    ("wbin", 0, "w1", "reg", "wbin", "+1 on winc", "w"),
    ("wb2g", 1, "w1", "mux", "bin2gray", "b^(b>>1)", "w"),
    ("wgray", 2, "w1", "reg", "wgray", "5 flops", "w"),
    ("wq1", 0, "w2", "sync", "wq1_rgray", "flop 1", "w"),
    ("wq2", 1, "w2", "sync", "wq2_rgray", "flop 2", "w"),
    ("full", 2, "w2", "stage", "full ?", "top 2 inv.", "w"),
    ("wfull", 3, "w2", "out", "wfull", "1 flop", "w"),
    ("rempty", 0, "r2", "out", "rempty", "1 flop", "r"),
    ("empty", 1, "r2", "stage", "empty ?", "all equal", "r"),
    ("rq2", 2, "r2", "sync", "rq2_wgray", "flop 2", "r"),
    ("rq1", 3, "r2", "sync", "rq1_wgray", "flop 1", "r"),
    ("rgray", 0, "r1", "reg", "rgray", "5 flops", "r"),
    ("rb2g", 1, "r1", "mux", "bin2gray", "b^(b>>1)", "r"),
    ("rbin", 2, "r1", "reg", "rbin", "+1 on rinc", "r"),
)


def _x(c):
    return COLS[c]


def _mid(c):
    return COLS[c] + BW // 2


def _y(row):
    return ROWS[row] + BH // 2


# (id, points, label, label x, label y, anchor, domain)
DP_WIRES = (
    ("winc", ((_mid(0), 8), (_mid(0), ROWS["w1"])), "winc", _mid(0) + 6, 18, "start", "w"),
    ("wnext", ((_x(0) + BW, _y("w1")), (_x(1), _y("w1"))), "", 0, 0, "", "w"),
    ("wgnext", ((_x(1) + BW, _y("w1")), (_x(2), _y("w1"))), "", 0, 0, "", "w"),
    ("wgfull", ((_mid(1), ROWS["w1"] + BH), (_mid(1), 92), (_mid(2), 92), (_mid(2), ROWS["w2"])), "wgray_next", (_mid(1) + _mid(2)) // 2, 88, "middle", "w"),
    ("wcross", ((_x(2) + BW, _y("w1")), (412, _y("w1")), (412, _y("r2")), (_x(3) + BW, _y("r2"))), "wgray", 406, 96, "end", "r"),
    ("wq12", ((_x(0) + BW, _y("w2")), (_x(1), _y("w2"))), "", 0, 0, "", "w"),
    ("wq2full", ((_x(1) + BW, _y("w2")), (_x(2), _y("w2"))), "", 0, 0, "", "w"),
    ("fullreg", ((_x(2) + BW, _y("w2")), (_x(3), _y("w2"))), "", 0, 0, "", "w"),
    ("rq12", ((_x(3), _y("r2")), (_x(2) + BW, _y("r2"))), "", 0, 0, "", "r"),
    ("rq2empty", ((_x(2), _y("r2")), (_x(1) + BW, _y("r2"))), "", 0, 0, "", "r"),
    ("emptyreg", ((_x(1), _y("r2")), (_x(0) + BW, _y("r2"))), "", 0, 0, "", "r"),
    ("rcross", ((_x(0), _y("r1")), (8, _y("r1")), (8, _y("w2")), (_x(0), _y("w2"))), "rgray", 14, 270, "start", "w"),
    ("rnext", ((_x(2), _y("r1")), (_x(1) + BW, _y("r1"))), "", 0, 0, "", "r"),
    ("rgnext", ((_x(1), _y("r1")), (_x(0) + BW, _y("r1"))), "", 0, 0, "", "r"),
    ("rgempty", ((_mid(1), ROWS["r1"]), (_mid(1), ROWS["r2"] + BH)), "rgray_next", _mid(1) + 6, 272, "start", "r"),
    ("rinc", ((_mid(2), DP_H - 4), (_mid(2), ROWS["r1"] + BH)), "rinc", _mid(2) + 6, DP_H - 8, "start", "r"),
)


def dp_wire(pts, cls="gh-wire", marker="gh-hb"):
    d = "M" + " L".join(f"{x:g},{y:g}" for x, y in pts)
    return f'<path class="{cls}" d="{d}" marker-end="url(#{marker})"/>'


def datapath_svg() -> str:
    """The pointer paths of the FIFO: the write side's wbin, bin2gray, wgray, the two flops
    that carry wgray into rclk's domain, the empty comparison and rempty; under them the
    mirror, rbin, bin2gray, rgray, the two flops into wclk's domain, the full comparison and
    wfull."""
    label = ("תרשים המלבנים של מצביעי ה-FIFO" + NB + ": למעלה הדומיין של wclk, למטה של rclk, וקו מקווקו ביניהם. "
             "בצד הכותב wbin של 5 ביטים עולה ב-1 על winc, bin2gray מחשב ממנו את wgray_next, והרגיסטר wgray שומר אותו. "
             "החוט wgray חוצה את הקו לשני פלופים בדומיין של הקורא, rq1_wgray ו-rq2_wgray. המשווה empty משווה את rq2_wgray "
             "עם rgray_next, והתוצאה נרשמת ב-rempty. בכיוון ההפוך rbin, bin2gray ו-rgray, החוט rgray חוצה לשני פלופים "
             "wq1_rgray ו-wq2_rgray, והמשווה full בודק ששני הביטים העליונים הפוכים והשאר שווים, ונרשם ב-wfull")
    o = [f'<svg class="figure gh-fig gh-dp" viewBox="0 0 {DP_W} {DP_H}" direction="ltr" style="max-width:{DP_W / 16:g}rem" '
         f'role="img" aria-label="{escape(label)}">',
         '<defs><marker id="gh-hb" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" '
         'markerHeight="9" orient="auto"><path class="gh-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>',
         f'<path class="gh-cdc" d="M0,{BOUNDARY} L{DP_W},{BOUNDARY}"/>',
         f'<text class="gh-dom" x="{DP_W // 2}" y="{BOUNDARY - 7}" text-anchor="middle">wclk domain</text>',
         f'<text class="gh-dom" x="{DP_W // 2}" y="{BOUNDARY + 16}" text-anchor="middle">rclk domain</text>']
    for _id, c, row, cls, title, sub, _dom in DP_BLOCKS:
        x, y = COLS[c], ROWS[row]
        o.append(f'<g class="gh-blk gh-{cls}"><rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="5"/>'
                 f'<text x="{x + BW / 2:g}" y="{y + BH / 2 - 3:g}" text-anchor="middle">{escape(title)}</text>'
                 f'<text class="gh-sub" x="{x + BW / 2:g}" y="{y + BH / 2 + 13:g}" text-anchor="middle">{escape(sub)}</text></g>')
    for _id, pts, lab, lx, ly, anchor, _dom in DP_WIRES:
        o.append(dp_wire(pts))
        if lab:
            o.append(f'<text class="gh-wlab" x="{lx}" y="{ly}" text-anchor="{anchor}">{escape(lab)}</text>')
    return "".join(o) + "</svg>"


# --- the waveforms ---------------------------------------------------------------------------------

def bits4(v: int) -> str:
    return format(v & 15, "04b")


def sample_wave() -> str:
    """Part a: the step 0111 -> 1000 as a bus, binary and Gray, with an rclk edge on the very
    moment of the change; rq1 takes 1110 in binary (every bit decides alone), and in Gray the
    old or the new value; the next rclk edge takes the settled value."""
    return """```wavedrom
{ signal: [
  { name: "wclk",          wave: "p......." },
  { name: "wptr (binary)", wave: "=.=.....", data: ["0111", "1000"] },
  { name: "wptr (Gray)",   wave: "=.=.....", data: ["0100", "1100"] },
  {},
  { name: "rclk",          wave: "p..", period: 3, phase: 1 },
  { name: "rq1 (binary)",  wave: "===", period: 3, phase: 1, data: ["0111", "1110 ?", "1000"] },
  { name: "rq1 (Gray)",    wave: "===", period: 3, phase: 1, data: ["0100", "0100 / 1100", "1100"] }
]}
```"""


def _lane(values, kind):
    """A WaveDrom wave string from one value per slot of the lane: '.' where it holds."""
    wave, data, prev = "", [], object()
    for v in values:
        if v == prev:
            wave += "."
        elif kind == "bit":
            wave += str(v)
        elif v == "x":
            wave += "x"
        else:
            wave += "="
            data.append(str(v))
        prev = v
    return wave, data


WAVE_T0, WAVE_SLOTS = 20, 10        # part c's waveform: ticks 20 to 120, ten slots (a phone shows 10)


def latency_wave(name: str = "page") -> str:
    """Part c: the FIFO of the page's example edge by edge as a WaveDrom diagram, from the
    first write (tick 20) for ten slots. wgray's bits reach rclk's domain each with its own
    delay (a phase per lane); rq1's bits are drawn in half rclk periods, so a bit caught
    metastable is x for the first half and its settled value after; rq2 and rempty change on
    rclk edges. The fifth bit stays 0 and is left out. Every lane ends by slot 10: WaveDrom
    sizes the drawing by its longest lane, and a phone shrinks a wider one past 9 px."""
    sc = SCENARIOS[name]
    tr = hw_trace(name)
    p0, r0 = sc["p0"], sc["r0"]
    init = {"wbin": p0, "wgray": gray(p0), "rq1": gray(p0), "rq2": gray(p0), "rempty": 1}

    def at(field, t):
        """A register's value after the last edge at or before tick t."""
        v = init[field]
        for r in tr:
            if r["t"] <= t:
                v = r[field]
        return v

    def lane(period, phase, value):
        n = int((WAVE_SLOTS + phase) / period + 1e-9)
        return [value(WAVE_T0 + round((k * period - phase) * SLOT)) for k in range(n)]

    lanes = [f'  {{ name: "wclk", wave: "p{"." * (WAVE_SLOTS // 2 - 1)}", period: 2 }}']
    w, d = _lane(lane(2, 0, lambda t: at("wbin", t)), "bus")
    lanes.append(f'  {{ name: "wbin", wave: "{w}", period: 2, data: {json.dumps(d)} }}')
    for i in range(3, -1, -1):
        ph = 1 - DELAY[i] / SLOT                    # one slot early, for the value before the first edge
        w, _ = _lane(lane(1, ph, lambda t, i=i: at("wgray", t - DELAY[i]) >> i & 1), "bit")
        lanes.append(f'  {{ name: "wgray[{i}]", wave: "{w}", phase: {ph:g} }}')
    lanes.append("  {}")
    ph = (WAVE_T0 - (r0 - PR)) / SLOT                # from one rclk period before its first edge
    redges = {r["t"]: r for r in tr if r["clk"] == "r"}
    n = int((WAVE_SLOTS + ph) / 3 + 1e-9)
    lanes.append(f'  {{ name: "rclk", wave: "0p{"." * (n - 2)}", period: 3, phase: {ph:g} }}')
    for i in range(3, -1, -1):
        def half(t, i=i):
            e = redges.get(t)
            return "x" if e and e["meta"] >> i & 1 else at("rq1", t) >> i & 1
        w, _ = _lane(lane(1.5, ph, half), "bit")
        lanes.append(f'  {{ name: "rq1[{i}]", wave: "{w}", period: 1.5, phase: {ph:g} }}')
    w, d = _lane(lane(3, ph, lambda t: bits4(at("rq2", t))), "bus")
    lanes.append(f'  {{ name: "rq2", wave: "{w}", period: 3, phase: {ph:g}, data: {json.dumps(d)} }}')
    w, _ = _lane(lane(3, ph, lambda t: at("rempty", t)), "bit")
    lanes.append(f'  {{ name: "rempty", wave: "{w}", period: 3, phase: {ph:g} }}')
    return "```wavedrom\n{ signal: [\n" + ",\n".join(lanes) + "\n]}\n```"


# --- the glitch sketch -----------------------------------------------------------------------------

GLITCH_T0, GLITCH_T1, GLITCH_EDGE = 20, 34, 24      # the window drawn, and the rclk edge in it


def glitch_values() -> list[tuple[int, int, int]]:
    """wbin's step 0111 -> 1000 at the wclk edge of tick 20, every bit at the XORs DELAY[i]
    later: (from tick, wbin as the XORs see it, its Gray) for every stretch between changes."""
    w = Wire(7)
    w.change(GLITCH_T0, 7, 8)
    times = sorted({c for h in w.hist for c, _ in h if c > GLITCH_T0})
    out = [(GLITCH_T0, 7, gray(7))]
    for c in times:
        b = w.at(c, True)
        out.append((c, b, gray(b)))
    return out


def glitch_svg() -> str:
    """The trap of a Gray computed by XORs and synchronized as is: wbin's bits reach the XORs at
    different ticks, so bin2gray(wbin) passes 1000, 1110 and 1101 on its way from 0100 to 1100;
    an rclk edge at tick 24 takes 1000, which is 15 in binary. The registered wgray changes one
    bit only."""
    X0, S, W = 104, 22, 420
    X = lambda t: X0 + (t - GLITCH_T0) * S
    vals = glitch_values()
    reg_change = GLITCH_T0 + DELAY[3]
    y = 26
    o = []
    label = ("שרטוט הגליץ'" + NB + ": ארבעת הביטים של wbin עוברים מ-0111 ל-1000, כל אחד בזמן אחר. "
             "ה-Gray שמחושב מהם ב-XOR עובר בדרך דרך 1000, 1110 ו-1101 לפני 1100, ושפה של rclk באמצע תופסת 1000, "
             "שהוא 15 בבינארי. ה-wgray הרשום משנה רק ביט אחד, מ-0100 ל-1100")
    o.append(f'<svg class="figure gh-fig gh-glitch" viewBox="0 0 {W} 222" direction="ltr" style="max-width:{W / 16:g}rem" '
             f'role="img" aria-label="{escape(label)}">')
    # the bits of wbin as the XORs see them
    for i in range(3, -1, -1):
        pts, level = [], None
        for t0, b, _g in vals:
            v = b >> i & 1
            yy = y + (4 if v else 18)
            if level is None:
                pts.append((X(t0), yy))
            elif v != level:
                pts += [(X(t0), y + (4 if level else 18)), (X(t0), yy)]
            level = v
        pts.append((X(GLITCH_T1), y + (4 if level else 18)))
        d = "M" + " L".join(f"{a:g},{c:g}" for a, c in pts)
        o.append(f'<text class="gh-lane" x="{X0 - 8}" y="{y + 16}" text-anchor="end">wbin[{i}]</text>')
        o.append(f'<path class="gh-bitline" d="{d}"/>')
        y += 26
    # the combinational Gray: a bus, a segment per stretch, the binary value under it
    y += 4
    bus = y
    o.append(f'<text class="gh-lane" x="{X0 - 8}" y="{y + 16}" text-anchor="end">bin2gray</text>')
    o.append(f'<text class="gh-lane gh-lane2" x="{X0 - 8}" y="{y + 30}" text-anchor="end">(wbin)</text>')
    ends = [t for t, _, _ in vals[1:]] + [GLITCH_T1]
    for (t0, b, g), t1 in zip(vals, ends):
        bad = b not in (7, 8)
        o.append(f'<rect class="gh-seg{" gh-bad" if bad else ""}" x="{X(t0) + 1}" y="{y}" width="{X(t1) - X(t0) - 2}" height="36" rx="3"/>')
        o.append(f'<text class="gh-segv" x="{(X(t0) + X(t1)) / 2:g}" y="{y + 15}" text-anchor="middle">{bits4(g)}</text>')
        o.append(f'<text class="gh-segn" x="{(X(t0) + X(t1)) / 2:g}" y="{y + 30}" text-anchor="middle">= {b}</text>')
    y += 46
    # the registered Gray: one bit changes
    o.append(f'<text class="gh-lane" x="{X0 - 8}" y="{y + 16}" text-anchor="end">wgray</text>')
    o.append(f'<text class="gh-lane gh-lane2" x="{X0 - 8}" y="{y + 30}" text-anchor="end">(register)</text>')
    for t0, t1, g, b in ((GLITCH_T0, reg_change, gray(7), 7), (reg_change, GLITCH_T1, gray(8), 8)):
        o.append(f'<rect class="gh-seg" x="{X(t0) + 1}" y="{y}" width="{X(t1) - X(t0) - 2}" height="36" rx="3"/>')
        o.append(f'<text class="gh-segv" x="{(X(t0) + X(t1)) / 2:g}" y="{y + 15}" text-anchor="middle">{bits4(g)}</text>')
        o.append(f'<text class="gh-segn" x="{(X(t0) + X(t1)) / 2:g}" y="{y + 30}" text-anchor="middle">= {b}</text>')
    y += 44
    # the wclk edge and the rclk edge, their names on top; the rclk line stops at the bus it
    # samples, so the value it takes stays readable
    o.append(f'<path class="gh-edge" d="M{X(GLITCH_T0)},16 L{X(GLITCH_T0)},{y - 4}"/>')
    o.append(f'<text class="gh-elab" x="{X(GLITCH_T0)}" y="11" text-anchor="middle">wclk ↑</text>')
    xe = X(GLITCH_EDGE)
    o.append(f'<path class="gh-edge gh-redge" d="M{xe},16 L{xe},{bus - 2} M{xe},{bus + 38} L{xe},{y - 4}"/>')
    o.append(f'<text class="gh-elab gh-relab" x="{xe}" y="11" text-anchor="middle">rclk ↑</text>')
    o.append("</svg>")
    legend = ('<span class="viz-legend">'
              '<span><i class="gh-key-bad"></i><span>ערך ביניים, לא הישן ולא החדש</span></span>'
              '<span><i class="gh-key-ok"></i><span>ערך שהמצביע באמת מחזיק</span></span>'
              '<span><i class="gh-key-edge"></i><span>השפה של rclk</span></span></span>')
    return "".join(o) + "\n\n" + legend


def blocks():
    """The generated blocks, in page order."""
    return [sample_wave(), datapath_svg(), latency_wave(), glitch_svg()]


if __name__ == "__main__":
    for name in SCENARIOS:
        print(name, first_word_latency(name) if name != "full" else "")
        for r in hw_trace(name):
            print(" ", r)
