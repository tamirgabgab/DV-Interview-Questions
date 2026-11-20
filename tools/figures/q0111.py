#!/usr/bin/env python3
"""Figures and tables of question 0111, the passing test and the broken register slice.

    python tools/figures/fill.py 111        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. Every value comes from the page's own cycle model (run_bench, loaded with
load_python): part d's log, the waveform around the lost item, and the table of the 16
combinations of the fixes. MESSAGES are the testbench's error texts (the matrix test and
the box print the same ones).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from extract_code import load_python  # noqa: E402

NB = " "
RLM = "‏"
SEED = 187                 # the bench's default seed, the page's example
WINDOW = range(8, 15)      # part d's waveform: the cycles around the lost item
FIXES = ("backpressure", "assert_fixed", "sb_fixed", "dut_fixed")


def page():
    return load_python(111)


def messages(max_wait):
    """checker -> the text of its error, given the item (the bench's error() strings)."""
    return {
        "a_hold": lambda d: "a_hold: out_data changed while out_ready was low",
        "unexpected": lambda d: f"scoreboard: unexpected item {d}",
        "wait": lambda d: f"scoreboard: item {d} still waiting after {max_wait} cycles",
        "missing": lambda d: f"scoreboard: item {d} never came out",
        "c_stall": lambda d: "c_stall: no cycle with out_valid && !out_ready",
        "c_hold": lambda d: "c_hold: a_hold never checked anything",
    }


def run(seed=SEED, backpressure=1, assert_fixed=1, sb_fixed=1, dut_fixed=0):
    return page()["run_bench"](seed, backpressure, assert_fixed, sb_fixed, dut_fixed)


def log_lines(r):
    """What the bench prints: an ERROR line per error, the verdict, the first error."""
    msg = messages(page()["MAX_WAIT"])
    lines = [f"ERROR at cycle {t}: {msg[who](d)}" for t, who, d in r["errors"]]
    n = len(r["errors"])
    lines.append(f"TEST {'FAILED' if n else 'PASSED'}: {r['n_in']} in, {r['n_out']} out, {n} errors")
    if n:
        t, who, d = r["errors"][0]
        lines.append(f"first error: cycle {t}: {msg[who](d)}")
    return lines


def log_block():
    """Part d: the log of the seed with the three testbench fixes and the broken DUT."""
    return "```text\n" + "\n".join(log_lines(run())) + "\n```"


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
    """Part d: the waveform of the run around the lost item, a slot per cycle."""
    rows = [r for r in run()["rows"] if r["t"] in WINDOW]
    lanes = [f'  {{ name: "clk",         wave: "p{"." * (len(rows) - 1)}" }}',
             f'  {{ name: "cycle",       wave: "{"=" * len(rows)}", data: {json.dumps([str(r["t"]) for r in rows])} }}']
    for name in ("in_valid", "in_ready"):
        lanes.append(f'  {{ name: "{name}",{" " * (12 - len(name))}wave: "{bit_lane([r[name] for r in rows])}" }}')
    w, d = bus_lane([r["in_data"] for r in rows])
    lanes.append(f'  {{ name: "in_data",     wave: "{w}", data: {json.dumps(d)} }}')
    lanes.append(f'  {{ name: "full_q",      wave: "{bit_lane([r["full_q"] for r in rows])}" }}')
    lanes.append(f'  {{ name: "out_ready",   wave: "{bit_lane([r["out_ready"] for r in rows])}" }}')
    w, d = bus_lane([r["out_data"] for r in rows])
    lanes.append(f'  {{ name: "out_data",    wave: "{w}", data: {json.dumps(d)} }}')
    lanes.append(f'  {{ name: "out_ready_q", wave: "{bit_lane([r["out_ready_q"] for r in rows])}" }}')
    return "```wavedrom\n{ signal: [\n" + ",\n".join(lanes) + "\n]}\n```"


def verdict_cell(r):
    """A cell of the table: the verdict, the counts of a pass, the first error of a fail."""
    if not r["errors"]:
        return f'עובר{NB}: <span dir="ltr">{r["n_in"]} in, {r["n_out"]} out</span>'
    t, who, _ = r["errors"][0]
    name = "scoreboard" if who in ("wait", "missing", "unexpected") else who
    n = len(r["errors"])
    if n == 1:
        return f"נכשל{NB}: שגיאה של `{name}` במחזור {t}"
    return f"נכשל{NB}: {n} שגיאות, הראשונה של `{name}` במחזור {t}"


def table_block():
    """Part d: the 16 combinations with the seed of the page, a row per testbench."""
    out = [f"| א{NB}: עצירות ויעד | ב{NB}: ה-assertion | ג{NB}: ה-scoreboard | ה-DUT השבור | ה-DUT המתוקן |",
           "|:-:|:-:|:-:|:--|:--|"]
    for code in range(8):
        bp, sva, sb = (code >> 2) & 1, (code >> 1) & 1, code & 1
        mark = lambda v: "✓" if v else "—"  # noqa: E731
        cells = [mark(bp), mark(sva), mark(sb), verdict_cell(run(SEED, bp, sva, sb, 0)), verdict_cell(run(SEED, bp, sva, sb, 1))]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def blocks():
    """The generated blocks, in page order."""
    return [log_block(), wave_block(), table_block()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
