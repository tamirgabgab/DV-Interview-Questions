"""Question 0115: what the page leaves out of its cocotb bench. tests/0115/variants.py puts the
page's code at the line "# the page's code" (the stimulus, the driver and the monitor, as
published or with one named change) and runs the module with run_cocotb. The page's bench
starts the monitor first; a variant may start the driver first."""

import cocotb
from cocotb.clock import Clock
from cocotb.handle import Immediate
from cocotb.triggers import ClockCycles, FallingEdge, ReadOnly, RisingEdge


def item(valid, data):
    return str(data) if valid else "none"


# the page's code


@cocotb.test()
async def race_tb(dut):
    dut.in_valid.value = 0
    dut.in_data.value = 0
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start(start_high=False))
    errors = []
    cocotb.start_soon(monitor(dut, errors))
    await cocotb.start_soon(drive(dut))
    await ClockCycles(dut.clk, 3)
    assert not errors, f"{len(errors)} mismatches"
