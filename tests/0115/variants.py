#!/usr/bin/env python3
"""Question 0115: the benches the tests run, built from the page's blocks and the parts the page
leaves out (tests/0115/env.sv, tests/0115/env.py).

    python tests/0115/variants.py --write      # rewrite tb.sv after a change to the page

SystemVerilog (tb.sv, written here; test_0115.py fails when it is not what this script writes):
the DUT; race_tb, the page's bench as published; race_tb_fix, the page's fix (its clocking
blocks and driver, and the page's monitor reading through mon_cb, the change the page names);
race_cfg, one bench for every choice of the box that Verilator runs (four drivers, four
monitors, the monitor or the driver first in the fork), each driver and monitor the page's
code with one named change; a program-block check; and tb, which compares every bench's
mismatch cycles with tools/figures/q0115.py.

cocotb (py_variants): the page's stimulus, driver and monitor, or the fixed driver, with the
monitor right after RisingEdge, in ReadOnly() or on FallingEdge, started first or second.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "tools" / "figures")]
from extract_code import pick  # noqa: E402
import q0115  # noqa: E402

QID = 115
TB = HERE / "tb.sv"
CODE_LINE = "  // the page's code\n"


def page_sv():
    return {"bug": pick(QID, "systemverilog", "in_data  = D[i];"),
            "fix": pick(QID, "systemverilog", "clocking drv_cb")}


def page_py():
    return {"bug": pick(QID, "python", "Immediate(valid)"),
            "fix": pick(QID, "python", "dut.in_valid.value = valid ")}


# --- SystemVerilog ------------------------------------------------------------------------------

TASK = re.compile(r"^task automatic (\w+)\(\);[^\n]*\n.*?^endtask\n", re.M | re.S)
SIGNAL = re.compile(r"\b(in_valid|in_data|out_valid|out_data)\b")


def tasks(code):
    return {m.group(1): m.group(0) for m in TASK.finditer(code)}


def rename(task, new):
    old = TASK.match(task).group(1)
    return task.replace(f"task automatic {old}();", f"task automatic {new}();", 1)


def change(text, old, new):
    assert text.count(old) >= 1, old
    return text.replace(old, new)


def indent(code, by="  "):
    return "".join(by + line if line.strip() else line for line in code.splitlines(keepends=True))


def sv_parts():
    """The drivers, the monitors and the declarations of the benches, from the page's blocks."""
    p = page_sv()
    bug, fix = tasks(p["bug"]), tasks(p["fix"])
    stim = p["bug"][:p["bug"].index("task automatic")]
    clocking = p["fix"][:p["fix"].index("task automatic")]
    monitor = bug["monitor"]
    head, body = monitor.split("  forever begin\n")
    via_cb = head + "  forever begin\n" + SIGNAL.sub(r"mon_cb.\1", change(body, "@(posedge clk);", "@(mon_cb);"))
    mon_cb = re.search(r"^clocking mon_cb .*?^endclocking\n", clocking, re.M | re.S).group(0)
    return {
        "stim": stim, "clocking": clocking,
        "mon_cb0": change(change(mon_cb, "mon_cb", "mon_cb0"), "#1step", "#0").replace(" (2)", ""),
        "drive": {
            "blk": bug["drive"],
            "nba": change(change(bug["drive"], "in_valid = V[i];", "in_valid <= V[i];"), "in_data  = D[i];", "in_data  <= D[i];"),
            "cb": fix["drive"],
            "neg": change(bug["drive"], "@(posedge clk);", "@(negedge clk);"),
        },
        "monitor": {
            "edge": monitor,
            "s1": via_cb,
            "s0": via_cb.replace("mon_cb", "mon_cb0"),
            "neg": change(monitor, "@(posedge clk);", "@(negedge clk);"),
        },
    }


def env_sv():
    text = (HERE / "env.sv").read_text(encoding="utf-8")
    dut = re.search(r"^module add1 .*?^endmodule\n", text, re.M | re.S).group(0)
    bench = re.search(r"^module race_tb;\n.*?^endmodule\n", text, re.M | re.S).group(0)
    assert bench.count(CODE_LINE) == 1
    return dut, bench


def bench(name, code, header=None):
    _, b = env_sv()
    b = b.replace(CODE_LINE, indent(code), 1)
    return b.replace("module race_tb;", header or f"module {name};", 1)


FORK = "    fork\n      monitor();\n      drive();\n    join_any\n"
FORK_CFG = ("    if (DRV_FIRST)\n      fork\n        drive();\n        monitor();\n      join_any\n"
            "    else\n      fork\n        monitor();\n        drive();\n      join_any\n")
SV_DRV = q0115.DRIVERS["sv"]
SV_MON = q0115.MONITORS["sv"]


def cfg_bench():
    """race_cfg: every driver and monitor, picked by the parameters, the order by DRV_FIRST."""
    s = sv_parts()
    code = s["stim"] + "\n" + s["clocking"] + s["mon_cb0"] + "\n"
    code += "\n".join(rename(t, f"drive_{k}") for k, t in s["drive"].items()) + "\n"
    code += "\n".join(rename(t, f"monitor_{k}") for k, t in s["monitor"].items()) + "\n"
    for what, names, param in (("drive", SV_DRV, "DRV"), ("monitor", SV_MON, "MON")):
        cases = "".join(f"    {i}: {what}_{k}();\n" for i, k in enumerate(names))
        code += f"task automatic {what}();\n  case ({param})\n{cases}  endcase\nendtask\n\n"
    b = bench("race_cfg", code.rstrip("\n") + "\n", "module race_cfg #(int DRV = 0, int MON = 0, bit DRV_FIRST = 0);")
    assert b.count(FORK) == 1
    return b.replace(FORK, FORK_CFG)


def cfg_list():
    """(driver, monitor, order) of race_cfg's instances, in the order of m[g]."""
    return [(d, m, o) for d in SV_DRV for m in SV_MON for o in q0115.VERILATOR_ORDERS]


def cycles(view):
    return " ".join(map(str, q0115.mismatch_cycles(view)))


HEADER = """//@flags --timing
// Question 0115: written by tests/0115/variants.py --write from the page's blocks and
// tests/0115/env.sv; do not edit. The page's bench as published (race_tb) reports its six
// mismatches at cycles 2, 3, 5, 7, 8 and 10, the page's fix (race_tb_fix) none; race_cfg runs
// every choice of the box that Verilator runs, and tb compares the mismatch cycles of every
// bench, and the waveforms of the two page benches, with tools/figures/q0115.py. A blocking
// write from a program block is still taken by the DUT at the same edge (Verilator does not
// run program blocks in the Reactive region).
"""

PROGRAM = """// a driver in a program block, writing with = at the edge
program automatic prog_drive (input logic clk, output logic [7:0] d);
  initial begin
    d = 8'd5;
    @(posedge clk);
    d = 8'd9;
  end
endprogram

module prog_check;
  logic       clk = 0, v;
  logic [7:0] d, q;
  add1 dut (.clk, .in_valid(1'b1), .in_data(d), .out_valid(v), .out_data(q));
  always #5 clk = ~clk;
  prog_drive drv (.clk, .d);
endmodule
"""


def tb_module():
    cfgs = cfg_list()
    n = len(cfgs)
    want = "\n".join(f"    {'\"' + cycles(q0115.view_of('sv', *c)) + '\"' + (',' if g < n - 1 else ''):<18}// {g}: {' '.join(c)}"
                     for g, c in enumerate(cfgs))
    dn, mn = len(SV_MON) * len(q0115.VERILATOR_ORDERS), len(q0115.VERILATOR_ORDERS)
    return f"""module tb;
  race_tb     bug ();
  race_tb_fix fix ();
  prog_check  prog ();

  // the mismatch cycles of every choice (q0115.mismatch_cycles of q0115.view_of)
  string WANT[{n}] = '{{
{want}
  }};
  int bad = 0;
  for (genvar g = 0; g < {n}; g++) begin : m
    race_cfg #(.DRV(g / {dn}), .MON(g / {mn} % {len(SV_MON)}), .DRV_FIRST(g % {mn})) b ();
    initial begin
      #200;
      if (b.cycles != WANT[g]) begin
        bad++;
        $display("race_cfg %0d: mismatch cycles \\"%s\\", want \\"%s\\"", g, b.cycles, WANT[g]);
      end
    end
  end

  // the waveform of the dump: valid/data of the input and the output after every edge, read
  // half a cycle later (q0115.wave_string)
  string wave_bug = "", wave_fix = "";
  string WANT_WAVE_BUG = "{q0115.wave_string("found")}";
  string WANT_WAVE_FIX = "{q0115.wave_string("fixed")}";
  function automatic string snap(logic iv, logic [7:0] id, logic ov, logic [7:0] od);
    return $sformatf("%0d/%0d:%0d/%0d", iv, id, ov, od);
  endfunction
  function automatic string join1(string s, string c);
    return s == "" ? c : {{s, " ", c}};
  endfunction
  always @(negedge bug.clk) if ($time <= 120) wave_bug = join1(wave_bug, snap(bug.in_valid, bug.in_data, bug.out_valid, bug.out_data));
  always @(negedge fix.clk) if ($time <= 120) wave_fix = join1(wave_fix, snap(fix.in_valid, fix.in_data, fix.out_valid, fix.out_data));

  // the program block: what the DUT took at the first edge (10: the value written at that edge)
  int prog_q = -1;
  initial begin
    @(negedge prog.clk);
    prog_q = prog.q;
  end

  initial begin
    #250;
    if (bug.cycles != "{cycles("found")}") begin bad++; $display("race_tb: mismatch cycles %s", bug.cycles); end
    if (fix.cycles != "{cycles("fixed")}") begin bad++; $display("race_tb_fix: mismatch cycles %s", fix.cycles); end
    if (wave_bug != WANT_WAVE_BUG) begin bad++; $display("wave bug: %s", wave_bug); end
    if (wave_fix != WANT_WAVE_FIX) begin bad++; $display("wave fix: %s", wave_fix); end
    if (prog_q != 10) begin bad++; $display("program block: the DUT took %0d at the first edge", prog_q - 1); end
    if (bad == 0) $display("PASS: 0115 the page's bench, its fix and {n} choices of the box (%0d mismatches as found)", bug.mismatches);
    else $display("FAIL: 0115 %0d differences", bad);
    $finish;
  end
endmodule
"""


def tb_text():
    s = sv_parts()
    dut, _ = env_sv()
    page = page_sv()
    fix = s["stim"] + "\n" + page["fix"] + "\n" + s["monitor"]["s1"]
    return "\n".join([HEADER, dut, bench("race_tb", page["bug"]), bench("race_tb_fix", fix), cfg_bench(), PROGRAM, tb_module()])


# --- cocotb ----------------------------------------------------------------------------------

START = "    cocotb.start_soon(monitor(dut, errors))\n    await cocotb.start_soon(drive(dut))\n"
START_SWAPPED = "    driver = cocotb.start_soon(drive(dut))\n    cocotb.start_soon(monitor(dut, errors))\n    await driver\n"
EDGE = "        await RisingEdge(dut.clk)\n        cycle += 1\n"
PY_MON = {"edge": EDGE, "ro": "        await RisingEdge(dut.clk)\n        await ReadOnly()\n        cycle += 1\n",
          "neg": "        await FallingEdge(dut.clk)\n        cycle += 1\n"}


def py_module(drv, mon, order):
    """The cocotb module of one choice: env.py with the page's code, one change each."""
    p = page_py()
    bug = p["bug"]
    at = bug.index("async def monitor")
    code = bug if drv == "imm" else bug[:bug.index("async def drive")] + p["fix"] + "\n\n" + bug[at:]
    assert code.count(EDGE) == 1
    code = code.replace(EDGE, PY_MON[mon])
    env = (HERE / "env.py").read_text(encoding="utf-8")
    assert env.count("# the page's code\n") == 1 and env.count(START) == 1
    env = env.replace("# the page's code\n", code)
    return env if order == "mdx" else env.replace(START, START_SWAPPED)


def py_list():
    return [(d, m, o) for d in q0115.DRIVERS["py"] for m in q0115.MONITORS["py"] for o in q0115.VERILATOR_ORDERS]


if __name__ == "__main__":
    if "--write" in sys.argv:
        TB.write_text(tb_text(), encoding="utf-8")
    else:
        print(tb_text())
