#!/usr/bin/env python3
"""The model and the log of question 0115, the monitor that sees mismatches the DUT does not have.

    python tools/figures/fill.py 115        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. Every value comes from run(), a model of one edge after another: at edge k
the driver writes row k - 1 of the stimulus, the DUT takes either that new row or the old
one (row k - 2), and the monitor reads the input (old or new) and the output (before or after
the edge's update). view_of() says which, for every choice of the box
(explorer/edgerace.js): the language, the driver's write, the monitor's sampling and the order
of the processes. tests/0115 runs every choice that Verilator 5.053 can run, in tb.sv and in
cocotb 2.1, and checks the mismatches against this model; the box's model is checked against
it under Node.
"""

from __future__ import annotations

V = [1, 1, 1, 0, 0, 1, 1, 1, 0, 0]      # the stimulus of the page: in_valid of every cycle
D = [5, 9, 9, 9, 9, 2, 6, 6, 6, 6]      # in_data, held while in_valid is low
EDGES = 12                              # the edges the model runs (the benches run 13)
CYCLES = 10                             # the cycles the page and the box show

# The box's choices. The driver: = at the rising edge, <=, a clocking block's output #0, = at
# the falling edge; in cocotb an Immediate write or a plain one (a deposit). The monitor:
# at the rising edge (in cocotb: right after RisingEdge), a clocking block's input #1step or
# #0, ReadOnly() (cocotb), the falling edge. The order of the monitor (m), the driver (d) and
# the DUT's always_ff (x) in the Active region of the edge: Verilator 5.053 runs the DUT
# after the processes of the testbench, in the order they started waiting; the orders with
# the DUT first are what another simulator may do (the standard leaves the order open).
DRIVERS = {"sv": ["blk", "nba", "cb", "neg"], "py": ["imm", "dep"]}
MONITORS = {"sv": ["edge", "s1", "s0", "neg"], "py": ["edge", "ro", "neg"]}
ORDERS = {"sv": ["mdx", "dmx", "xmd", "xdm"], "py": ["mdx", "dmx"]}
VERILATOR_ORDERS = ["mdx", "dmx"]


def view_of(lang, drv, mon, order):
    """(the DUT takes the new row, the monitor reads the new input, the monitor reads the
    output after the edge's update) for one choice of the box."""
    assert drv in DRIVERS[lang] and mon in MONITORS[lang] and order in ORDERS[lang]
    at = {p: order.index(p) for p in "mdx"}
    active = drv in ("blk", "imm")              # the write runs among the Active processes
    dut_new = int(active and at["d"] < at["x"])
    if mon == "edge":                           # in the Active region, in the order
        mon_new = int(active and at["d"] < at["m"])
    elif mon == "s1":                           # Preponed: before anything of the edge
        mon_new = 0
    elif mon == "s0":                           # Observed: after NBA, before Re-NBA
        mon_new = int(drv in ("blk", "nba"))
    elif mon == "ro":                           # ReadOnly: after the plain writes of ReadWrite
        mon_new = 1
    else:                                       # the falling edge: the driver there races again
        mon_new = int(drv != "neg" or at["d"] < at["m"])
    return dut_new, mon_new, int(mon in ("s0", "ro", "neg"))


VIEWS = {   # the views the page names
    "found": view_of("sv", "blk", "edge", "mdx"),       # = (or Immediate), the monitor first
    "swap": view_of("sv", "blk", "edge", "dmx"),        # = (or Immediate), the driver first
    "after": view_of("sv", "blk", "neg", "mdx"),        # = (or Immediate), the monitor after the edge
    "fixed": view_of("sv", "cb", "s1", "mdx"),          # the clocking blocks
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
    got, and the mismatches as (cycle, expected, got). view is a name of VIEWS or a triple."""
    dut_new, mon_new, mon_after = VIEWS[view] if isinstance(view, str) else view
    out = [(0, 0)]                       # the output after edge k (Verilator starts at 0)
    for k in range(1, EDGES + 1):
        out.append(plus1(row(k - 1 if dut_new else k - 2)))
    exp, edges, mismatches = (0, 0), [], []
    for k in range(1, EDGES + 1):
        read = row(k - 1 if mon_new else k - 2)
        got = out[k] if mon_after else out[k - 1]
        bad = bool(got[0] != exp[0] or (exp[0] and got[1] != exp[1]))
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


def blocks():
    return [log_block()]


if __name__ == "__main__":
    for b in blocks():
        print(b, end="\n\n")
