#!/usr/bin/env python3
"""Figures and tables of question 0114 (a virtual sequence over two agents; lock, grab and
the sequencer's arbitration).

    python tools/figures/fill.py 114        # put the blocks on the page

trace(case) is a cycle model of the testbench of parts א and ב: the drivers' timing (a
register write every three cycles, packets of three bytes back to back), the order the
virtual sequence gives them in each case, and the DUT pkt_xor. tests/0114 checks it against
the pins of the Verilator run, cycle by cycle. orders() runs the page's arbitration model
of part ג (its Python block). blocks(), in page order: the testbench figure and its legend,
the waveform of part א's bug, the waveform of part ב's bug and the table of part ג.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from extract_code import pick  # noqa: E402

RLM, NB = "\u200f", "\u00a0"
CTRL, KEY = 0, 1
KEY_A, KEY_B = 0x5A, 0xC3
PACKETS, LENGTH, GAP, REKEY_AT, DRAIN = 8, 3, 3, 10, 3   # as on the page
CASES = ("boot_bug", "boot_fix", "rekey_bug", "rekey_fix")


# --- the cycle model of parts א and ב -----------------------------------------------------------

def plan(case):
    """The register writes (cycle, addr, data) and the first cycle of every packet, as the
    two drivers put them on the pins in each case. Cycle 0 is the first after reset."""
    writes = [(0, KEY, KEY_A), (GAP, CTRL, 1)]
    boot = len(writes) * GAP                   # the configuration sequence ends here
    first = 0 if case == "boot_bug" else boot  # the bug starts both at once (fork)
    starts = [first + LENGTH * k for k in range(PACKETS)]
    if case.startswith("rekey"):
        at = boot + REKEY_AT                   # the virtual sequence wants the new key here
        assert (at - boot) % LENGTH, "the request must fall inside a packet"
        if case == "rekey_bug":
            writes.append((at, KEY, KEY_B))
        else:                                  # the traffic stops after its current packet
            stop = next(s for s in starts if s > at)
            writes.append((stop, KEY, KEY_B))
            starts = [s if s < stop else s + GAP for s in starts]
    return writes, starts


def trace(case):
    """Every cycle's pins (and the DUT's enable and key), from the first cycle after reset
    to the end of the test, three cycles after the last byte."""
    writes, starts = plan(case)
    n = max(starts[-1] + LENGTH, writes[-1][0] + GAP) + DRAIN
    on_bus = {c: (a, d) for c, a, d in writes}
    on_in = {s + i: (k, i) for k, s in enumerate(starts) for i in range(LENGTH)}
    cfg = dict(cfg_valid=0, cfg_addr=0, cfg_data=0)
    pkt = dict(in_valid=0, in_last=0, in_data=0)
    enable = key = mid = keep = 0
    out = dict(out_valid=0, out_last=0, out_data=0, drops=0)
    rows = []
    for t in range(n):
        if t in on_bus:                        # a driver leaves the last values on the pins
            cfg = dict(cfg_valid=1, cfg_addr=on_bus[t][0], cfg_data=on_bus[t][1])
        else:
            cfg["cfg_valid"] = 0
        if t in on_in:
            k, i = on_in[t]
            pkt = dict(in_valid=1, in_last=int(i == LENGTH - 1), in_data=16 * k + i)
        else:
            pkt["in_valid"] = 0
        rows.append({**cfg, **pkt, **out, "enable": enable, "key": key})
        go = keep if mid else enable           # the clock edge at the end of cycle t
        out = dict(out_valid=int(pkt["in_valid"] and go), out_last=pkt["in_last"],
                   out_data=pkt["in_data"] ^ key,
                   drops=out["drops"] + int(pkt["in_valid"] and not mid and not enable))
        if pkt["in_valid"]:
            mid, keep = int(not pkt["in_last"]), go
        if cfg["cfg_valid"]:
            if cfg["cfg_addr"]:
                key = cfg["cfg_data"]
            else:
                enable = cfg["cfg_data"] & 1
    return rows


# --- the testbench figure -----------------------------------------------------------------------

W, H = 500, 440
# id: (label, x, y, w, h, container?)
LAYOUT = {
    "test":      ("test",              6,   6, 488, 340, True),
    "vseq":      ("virtual sequence", 167,  28, 166,  32, False),
    "env":       ("env",              14,  76, 472, 262, True),
    "vseqr":     ("virtual sequencer", 160, 98, 180,  38, False),
    "reg_agent": ("reg_agent",        24, 156, 170, 172, True),
    "reg_seqr":  ("sequencer",        44, 182, 110,  36, False),
    "reg_drv":   ("driver",           44, 276, 110,  36, False),
    "pkt_agent": ("pkt_agent",       306, 156, 170, 172, True),
    "pkt_seqr":  ("sequencer",       346, 182, 110,  36, False),
    "pkt_drv":   ("driver",          346, 276, 110,  36, False),
    "checker":   ("checker",         200, 276, 100,  36, False),
    "dut":       ("pkt_xor",         165, 372, 170,  56, False),
}
# (from, to, kind): tlm (items), handle (a reference to a sequencer), pin (signals)
ARROWS = [
    ("vseq", "vseqr", "tlm"),
    ("vseqr", "reg_seqr", "handle"),
    ("vseqr", "pkt_seqr", "handle"),
    ("reg_seqr", "reg_drv", "tlm"),
    ("pkt_seqr", "pkt_drv", "tlm"),
    ("reg_drv", "dut", "pin"),
    ("pkt_drv", "dut", "pin"),
    ("dut", "checker", "pin"),
]
LINE = {"tlm": "uv-arrow uv-tlm", "handle": "uv-arrow stream-c", "pin": "uv-arrow uv-pin"}


def center(c):
    _, x, y, w, h, _ = LAYOUT[c]
    return x + w / 2, y + h / 2


def edge_point(c, toward):
    """Where the line from the centre of c toward a point leaves the box of c."""
    _, x, y, w, h, _ = LAYOUT[c]
    cx, cy = center(c)
    dx, dy = toward[0] - cx, toward[1] - cy
    sx = (w / 2) / abs(dx) if dx else float("inf")
    sy = (h / 2) / abs(dy) if dy else float("inf")
    s = min(sx, sy)
    return cx + dx * s, cy + dy * s


def figure():
    s = (f'<svg class="figure uv-fig" viewBox="0 0 {W} {H}" style="max-width:32rem" role="img" '
         f'aria-label="הסביבה{NB}: virtual sequence על virtual sequencer שמחזיק handles לשני sequencers, '
         'של reg_agent ושל pkt_agent; שני drivers מחוברים ל-pkt_xor, ו-checker מסתכל על הפינים">'
         '<defs><marker id="vs-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
         'orient="auto"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs>')
    for c, (label, x, y, w, h, cont) in LAYOUT.items():
        if cont:
            # pkt_agent's name sits on the right, away from the line that crosses its corner
            at = f'x="{x + w - 8}" y="{y + 17}" text-anchor="end"' if c == "pkt_agent" else f'x="{x + 8}" y="{y + 17}"'
            s += (f'<g class="uv-box is-cont uv-{c}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>'
                  f'<text {at}>{label}</text></g>')
    for a, b, kind in ARROWS:
        (x1, y1), (x2, y2) = edge_point(a, center(b)), edge_point(b, center(a))
        s += (f'<line class="{LINE[kind]}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
              'marker-end="url(#vs-arrow)"/>')
    for c, (label, x, y, w, h, cont) in LAYOUT.items():
        if not cont:
            cx, cy = center(c)
            s += (f'<g class="uv-box uv-{c}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>'
                  f'<text x="{cx:.1f}" y="{cy + 5:.1f}" text-anchor="middle">{label}</text></g>')
    return s + "</svg>"


def legend():
    return ('<span class="viz-legend"><span><i class="uv-key-tlm"></i>פריטים : start ו-seq_item_port</span>'
            '<span><i class="by-bfs"></i>מצביע ל-sequencer, נקבע ב-connect_phase</span>'
            '<span><i class="uv-key-pin"></i>אותות</span></span>').replace(" :", NB + ":")


# --- the waveforms ------------------------------------------------------------------------------

def bit_lane(values):
    wave, prev = "", None
    for v in values:
        wave += "." if v == prev else str(v)
        prev = v
    return wave


def bus_lane(values):
    """None is a bus with nothing on it (z); a value repeats with "."."""
    wave, data, prev = "", [], object()
    for v in values:
        if v == prev:
            wave += "."
        elif v is None:
            wave += "z"
        else:
            wave += "="
            data.append(str(v))
        prev = v
    return wave, data


def wavedrom(cycles, lanes):
    """A ```wavedrom block over the given cycles: the clock, a lane that numbers the cycles
    (the waveform viewer leaves it out of its log), then (name, values, kind) lanes."""
    n = len(cycles)
    width = max(len(name) for name, _, _ in lanes + [("cycle", None, None)])
    pad = lambda name: f'"{name}",' + " " * (width - len(name))
    rows = [f'  {{ name: {pad("clk")} wave: "p{"." * (n - 1)}" }}',
            f'  {{ name: {pad("cycle")} wave: "{"=" * n}", data: {json.dumps([str(c) for c in cycles])} }}']
    for name, values, kind in lanes:
        if kind == "bit":
            rows.append(f'  {{ name: {pad(name)} wave: "{bit_lane(values)}" }}')
        else:
            w, data = bus_lane(values)
            rows.append(f'  {{ name: {pad(name)} wave: "{w}", data: {json.dumps(data)} }}')
    return "```wavedrom\n{ signal: [\n" + ",\n".join(rows) + "\n]}\n```"


def cfg_lane(rows):
    return [("KEY" if r["cfg_addr"] else "CTRL") if r["cfg_valid"] else None for r in rows]


def wave_boot():
    """Part א's bug, cycles 0 to 7: the first two packets start before enable rises."""
    rows = trace("boot_bug")[:8]
    return wavedrom(range(8), [
        ("cfg", cfg_lane(rows), "bus"),
        ("enable", [r["enable"] for r in rows], "bit"),
        ("in_valid", [r["in_valid"] for r in rows], "bit"),
        ("in_data", [f'{r["in_data"]:02x}' if r["in_valid"] else None for r in rows], "bus"),
        ("in_last", [r["in_last"] for r in rows], "bit"),
        ("drops", [r["drops"] for r in rows], "bus"),
        ("out_valid", [r["out_valid"] for r in rows], "bit"),
    ])


REKEY_WINDOW = range(14, 20)


def wave_rekey():
    """Part ב's bug: the new key lands in the middle of packet 3."""
    rows = trace("rekey_bug")
    rows = [rows[c] for c in REKEY_WINDOW]
    return wavedrom(REKEY_WINDOW, [
        ("cfg", cfg_lane(rows), "bus"),
        ("key", [f'{r["key"]:02x}' for r in rows], "bus"),
        ("in_data", [f'{r["in_data"]:02x}' if r["in_valid"] else None for r in rows], "bus"),
        ("in_last", [r["in_last"] for r in rows], "bit"),
        ("out_valid", [r["out_valid"] for r in rows], "bit"),
        ("out_data", [f'{r["out_data"]:02x}' if r["out_valid"] else None for r in rows], "bus"),
    ])


# --- part ג: the arbitration model of the page ----------------------------------------------------

def model():
    ns = {}
    exec(pick(114, "python", "def sequencer("), ns)
    return ns


SCENARIOS = [  # (the setting, how I starts, the arbitration mode)
    ("ברירת המחדל, `FIFO`", dict(), "FIFO"),
    (f"עדיפות 500 ל-I, {RLM}`FIFO`", dict(priority=500), "FIFO"),
    (f"עדיפות 500 ל-I, {RLM}`STRICT_FIFO`", dict(priority=500), "STRICT_FIFO"),
    (f"{RLM}`lock()`, {RLM}`FIFO`", dict(how="lock"), "FIFO"),
    (f"{RLM}`grab()`, {RLM}`FIFO`", dict(how="grab"), "FIFO"),
]


def orders():
    """The driver's items in each scenario of part ג, from the page's model."""
    ns = model()
    out = []
    for label, kw, mode in SCENARIOS:
        seqs = [ns["traffic"]("A"), ns["traffic"]("B"), ns["irq"](**kw)]
        out.append((label, mode, ns["sequencer"](seqs, mode)))
    return out


def together(order):
    """Whether I0, I1 and I2 reach the driver with no other item between them."""
    at = [i for i, x in enumerate(order) if x.startswith("I")]
    return all(order[i] in ("-",) or order[i].startswith("I") for i in range(at[0], at[-1] + 1))


def show(order):
    last = max(i for i, x in enumerate(order) if x.startswith("I"))
    cells = [f"<b>{x}</b>" if x.startswith("I") else ("·" if x == "-" else x) for x in order[:last + 2]]
    return f'{RLM}<span dir="ltr">{" ".join(cells)}{NB}…</span>'


def orders_table():
    rows = ["| ההגדרה | מה ה-driver מקבל | רצף של I? |", "|---|---|:-:|"]
    for label, _, order in orders():
        rows.append(f"| {label} | {show(order)} | {'כן' if together(order) else 'לא'} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [figure(), legend(), wave_boot(), wave_rekey(), orders_table()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
