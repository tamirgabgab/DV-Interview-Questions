#!/usr/bin/env python3
"""Figures and tables of question 0110: three RTL snippets, each with its bug and its fix.

    python tools/figures/fill.py 110        # put the blocks on the page

The references below are the cycle-by-cycle traces that tests/0110/tb.sv takes from
Verilator (its want strings) and that the page's Python models and the rtlbug box compute:

- part a, delay3: q1, q2, q3 in every cycle, with blocking (=) or nonblocking (<=) lines;
- part b, en_gate: y in every cycle, without or with the default assignment;
- part c, avg8: (a + b) >> 1 in a context of 8 bits (the bug) or 9 bits (the fix).

A cycle starts at a rising edge of clk; the inputs of cycle k change just after that edge
(they come from registers), so the edge that starts cycle k + 1 samples them. Verilator
starts every variable at 0. blocks() returns the waveforms and the tables in page order.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

RLM = "‏"
N = 8                                          # cycles 0 .. 7 in every part
D_A = [0, 1, 1, 0, 1, 0, 0, 0]                 # part a: d
EN_B = [0, 1, 1, 0, 0, 1, 0, 0]                # part b: en
D_B = [3, 5, 9, 12, 7, 6, 10, 1]               # part b: d (4 bits)
A_C = [10, 100, 200, 127, 128, 255, 255, 60]   # part c: a
B_C = [20, 50, 100, 128, 128, 255, 1, 61]      # part c: b


# --- the references -----------------------------------------------------------------------

def delay_trace(d, blocking=False):
    """(q1, q2, q3) during every cycle. At each edge the three lines run in order: with =
    each line reads what the line above has just written, with <= every right-hand side is
    read before any register is written."""
    q1 = q2 = q3 = 0
    out = []
    for x in d:
        out.append((q1, q2, q3))
        if blocking:
            q1 = x
            q2 = q1
            q3 = q2
        else:
            q1, q2, q3 = x, q1, q2
    return out


def delay_want(d):
    """What the designer meant: q3 is d three cycles earlier (0 before the first cycle)."""
    return [d[k - 3] if k >= 3 else 0 for k in range(len(d))]


def gate_trace(en, d, default=True):
    """y during every cycle. Without the default line, a cycle with en low writes nothing to y,
    and y keeps the value it had (a latch)."""
    y, out = 0, []
    for e, x in zip(en, d):
        if default:
            y = 0
        if e:
            y = x
        out.append(y)
    return out


def gate_want(en, d):
    return [x if e else 0 for e, x in zip(en, d)]


def avg(a, b, width=9):
    """(a + b) >> 1 evaluated in a context of `width` bits, the result kept to 8 bits."""
    return (((a + b) % (1 << width)) >> 1) % 256


def avg_want(a, b):
    return (a + b) // 2


def lost_pairs():
    """How many of the 65,536 pairs the bug gets wrong, and by how much."""
    diffs = {avg(a, b) - avg(a, b, 8) for a in range(256) for b in range(256) if a + b >= 256}
    wrong = sum(1 for a in range(256) for b in range(256) if avg(a, b, 8) != avg_want(a, b))
    return wrong, diffs


# --- the want strings of the testbench ------------------------------------------------------

def want_strings():
    """The traces in the format of tests/0110/tb.sv: a string of bits per register for part a,
    the values joined by spaces for parts b and c."""
    bits = lambda rows, i: "".join(str(r[i]) for r in rows)
    nums = lambda vals: " ".join(str(v) for v in vals)
    a_bug, a_fix = delay_trace(D_A, True), delay_trace(D_A)
    return {
        "WANT_A_BUG": [bits(a_bug, i) for i in range(3)],
        "WANT_A_FIX": [bits(a_fix, i) for i in range(3)],
        "WANT_B_BUG": nums(gate_trace(EN_B, D_B, False)),
        "WANT_B_FIX": nums(gate_trace(EN_B, D_B)),
        "WANT_C_BUG": nums(avg(a, b, 8) for a, b in zip(A_C, B_C)),
        "WANT_C_FIX": nums(avg(a, b) for a, b in zip(A_C, B_C)),
    }


# --- waveforms (WaveDrom) -------------------------------------------------------------------

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


def wavedrom(lanes):
    """A ```wavedrom block: the clock, a lane that numbers the cycles (the waveform viewer
    leaves it out of its log), then the lanes, (name, values, kind) with kind bit or bus."""
    width = max(len(n) for n, _, _ in lanes + [("cycle", None, None)])
    pad = lambda name: f'"{name}",' + " " * (width - len(name))
    rows = [f'  {{ name: {pad("clk")} wave: "p{"." * (N - 1)}" }}',
            f'  {{ name: {pad("cycle")} wave: "{"=" * N}", data: {json.dumps([str(k) for k in range(N)])} }}']
    for name, values, kind in lanes:
        if kind == "bit":
            rows.append(f'  {{ name: {pad(name)} wave: "{bit_lane(values)}" }}')
        else:
            w, data = bus_lane(values)
            rows.append(f'  {{ name: {pad(name)} wave: "{w}", data: {json.dumps(data)} }}')
    return "```wavedrom\n{ signal: [\n" + ",\n".join(rows) + "\n]}\n```"


def wave_a(blocking):
    tr = delay_trace(D_A, blocking)
    return wavedrom([("d", D_A, "bit")] + [(f"q{i + 1}", [r[i] for r in tr], "bit") for i in range(3)])


def wave_b(default):
    return wavedrom([("en", EN_B, "bit"), ("d", D_B, "bus"), ("y", gate_trace(EN_B, D_B, default), "bus")])


def wave_c(width):
    return wavedrom([("a", A_C, "bus"), ("b", B_C, "bus"), ("avg", [avg(a, b, width) for a, b in zip(A_C, B_C)], "bus")])


# --- the tables of the solutions --------------------------------------------------------------

def table(rows, want=None):
    """A Markdown table with a column per cycle; rows are (name, values, check): the values of
    a row with check set are bold where they differ from `want`."""
    out = ["| מחזור | " + " | ".join(str(k) for k in range(N)) + " |", "|:-:|" + ":-:|" * N]
    for name, values, check in rows:
        cells = [f"**{v}**" if check and v != want[k] else str(v) for k, v in enumerate(values)]
        out.append(f"| {name} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def table_a():
    bug, fix = delay_trace(D_A, True), delay_trace(D_A)
    want = delay_want(D_A)
    rows = [(f"{RLM}`d`", D_A, False)]
    rows += [(f"הבאג, {RLM}`q{i + 1}`", [r[i] for r in bug], i == 2) for i in range(3)]
    rows += [(f"התיקון, {RLM}`q{i + 1}`", [r[i] for r in fix], i == 2) for i in range(3)]
    return table(rows, want)


def table_b():
    want = gate_want(EN_B, D_B)
    return table([(f"{RLM}`en`", EN_B, False), (f"{RLM}`d`", D_B, False),
                  (f"הבאג, {RLM}`y`", gate_trace(EN_B, D_B, False), True),
                  (f"התיקון, {RLM}`y`", gate_trace(EN_B, D_B), True)], want)


def table_c():
    want = [avg_want(a, b) for a, b in zip(A_C, B_C)]
    return table([(f"{RLM}`a`", A_C, False), (f"{RLM}`b`", B_C, False),
                  (f"{RLM}`a + b`", [a + b for a, b in zip(A_C, B_C)], False),
                  ("הסכום ב-8 ביטים", [(a + b) % 256 for a, b in zip(A_C, B_C)], False),
                  (f"הבאג, {RLM}`avg`", [avg(a, b, 8) for a, b in zip(A_C, B_C)], True),
                  (f"התיקון, {RLM}`avg`", [avg(a, b) for a, b in zip(A_C, B_C)], True)], want)


def blocks():
    """The generated blocks, in page order: per part the bug's waveform in the statement,
    then the table and the fixed waveform in the solution."""
    return [wave_a(True), wave_b(False), wave_c(8),
            table_a(), wave_a(False),
            table_b(), wave_b(True),
            table_c(), wave_c(9)]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
