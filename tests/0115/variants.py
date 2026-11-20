"""Question 0115: the variants of the page's benches that tests/0115/tb.sv and the cocotb test
run besides the page's own code. Each one is the page's code with one change named on the
page (the order of the fork, a driver from a fix snippet, the monitor on the other edge, a
monitor in ReadOnly), made here by text so the tests can check that tb.sv holds exactly
these copies.

    python tests/0115/variants.py      # print the SystemVerilog copies for tb.sv
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from extract_code import pick  # noqa: E402

QID = 115


def page_sv():
    """The page's SystemVerilog: the bench as found, the clocking-block fix, two drivers."""
    return {
        "race_tb": pick(QID, "systemverilog", "module race_tb;"),
        "race_tb_cb": pick(QID, "systemverilog", "module race_tb_cb;"),
        "drive_nba": pick(QID, "systemverilog", "// written in the NBA region"),
        "drive_neg": pick(QID, "systemverilog", "@(negedge clk);"),
    }


def page_py():
    """The page's cocotb benches: as found (Immediate) and fixed (plain writes)."""
    return {
        "bug": pick(QID, "python", "Immediate(valid)"),
        "fix": pick(QID, "python", "dut.in_valid.value = valid "),
    }


DRIVE = re.compile(r"^  task automatic drive\(\);\n.*?^  endtask\n", re.M | re.S)
FORK = "      monitor();\n      drive();\n"
SWAPPED = "      drive();\n      monitor();\n"


def rename(module: str, old: str, new: str) -> str:
    head = f"module {old};"
    assert module.startswith(head)
    return f"module {new};" + module[len(head):]


def indent(code: str, by: str = "  ") -> str:
    return "".join(by + line if line.strip() else line for line in code.splitlines(keepends=True))


def swap(module: str) -> str:
    assert module.count(FORK) == 1
    return module.replace(FORK, SWAPPED)


def with_drive(module: str, task: str) -> str:
    assert len(DRIVE.findall(module)) == 1
    return DRIVE.sub(lambda _: task, module)


def sv_variants() -> dict[str, str]:
    """Module name -> text of every SystemVerilog copy in tb.sv."""
    p = page_sv()
    bug, cb = p["race_tb"], p["race_tb_cb"]
    negmon = bug.replace("      @(posedge clk);\n      cycle++;", "      @(negedge clk);\n      cycle++;")
    assert negmon != bug
    return {
        "race_tb_swap": swap(rename(bug, "race_tb", "race_tb_swap")),
        "race_tb_nba": with_drive(rename(bug, "race_tb", "race_tb_nba"), indent(p["drive_nba"])),
        "race_tb_neg": with_drive(rename(bug, "race_tb", "race_tb_neg"), indent(p["drive_neg"])),
        "race_tb_negmon": rename(negmon, "race_tb", "race_tb_negmon"),
        "race_tb_cb_swap": swap(rename(cb, "race_tb_cb", "race_tb_cb_swap")),
        "race_tb_cb_mon": with_drive(rename(cb, "race_tb_cb", "race_tb_cb_mon"), DRIVE.search(bug).group(0)),
    }


START = "    cocotb.start_soon(monitor(dut, errors))\n    await cocotb.start_soon(drive(dut))\n"
START_SWAPPED = "    driver = cocotb.start_soon(drive(dut))\n    cocotb.start_soon(monitor(dut, errors))\n    await driver\n"
EDGE = "        await RisingEdge(dut.clk)\n        cycle += 1\n"
EDGE_RO = "        await RisingEdge(dut.clk)\n        await ReadOnly()\n        cycle += 1\n"


def py_variants() -> dict[str, str]:
    """Scenario -> cocotb module: the page's two benches, each also with the driver started
    first, and each with the monitor reading in ReadOnly()."""
    p = page_py()
    out = {}
    for name, code in p.items():
        assert code.count(START) == 1 and code.count(EDGE) == 1
        out[name] = code
        out[name + "_swap"] = code.replace(START, START_SWAPPED)
        out[name + "_ro"] = code.replace(EDGE, EDGE_RO).replace(
            "from cocotb.triggers import ClockCycles, RisingEdge", "from cocotb.triggers import ClockCycles, ReadOnly, RisingEdge")
    return out


TB = ROOT / "tests" / "0115" / "tb.sv"
COPIES = re.compile(r"(// ---- the copies: [^\n]*\n)(.*?)(// ---- end of the copies ----\n)", re.S)


def copies_block() -> str:
    return "\n".join(sv_variants().values())


def tb_copies() -> str:
    """The copies section of tb.sv as it is."""
    return COPIES.search(TB.read_text(encoding="utf-8")).group(2)


if __name__ == "__main__":
    if "--write" in sys.argv:
        text = TB.read_text(encoding="utf-8")
        TB.write_text(COPIES.sub(lambda m: m.group(1) + copies_block() + m.group(3), text), encoding="utf-8")
    else:
        print(copies_block())
