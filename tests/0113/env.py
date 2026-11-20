"""Question 0113: the environment of the page's tests (pyuvm), the part of the testbench
the page describes in words. tests/0113/sim0113.py puts the page's blocks after it."""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge, RisingEdge, SimTimeoutError, Timer, with_timeout
from cocotb.utils import get_sim_time
import pyuvm
from pyuvm import *

N = 8                                       # items per test


class Item(uvm_sequence_item):
    def __init__(self, name="item", data=0):
        super().__init__(name)
        self.data = data


class ItemSeq(uvm_sequence):
    async def body(self):
        for k in range(N):
            item = Item("item", data=0x10 + k)
            await self.start_item(item)
            await self.finish_item(item)


class Driver(uvm_driver):
    async def run_phase(self):
        dut = cocotb.top
        dut.rst_n.value = 0
        dut.in_valid.value = 0
        await ClockCycles(dut.clk, 2)
        dut.rst_n.value = 1
        while True:
            item = await self.seq_item_port.get_next_item()
            dut.in_valid.value = 1
            dut.in_data.value = item.data
            await RisingEdge(dut.clk)           # the DUT takes the item here
            dut.in_valid.value = 0
            self.seq_item_port.item_done()


class InMonitor(uvm_monitor):
    PINS = ("in_valid", "in_data")

    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)

    async def run_phase(self):
        valid, data = (getattr(cocotb.top, p) for p in self.PINS)
        while True:
            await FallingEdge(cocotb.top.clk)
            if valid.value:
                self.ap.write(int(data.value))


class OutMonitor(InMonitor):
    PINS = ("out_valid", "out_data")


class Scoreboard(uvm_component):
    def build_phase(self):
        self.sent = uvm_tlm_analysis_fifo("sent", self)
        self.seen = uvm_tlm_analysis_fifo("seen", self)

    def check_phase(self):
        sent, seen = [], []
        for fifo, items in ((self.sent, sent), (self.seen, seen)):
            while fifo.can_get():
                items.append(fifo.try_get()[1])
        bad = sum(out != x + 1 for x, out in zip(sent, seen))
        missing = len(sent) - len(seen)
        self.logger.info(f"{get_sim_time('ns'):g} ns: {len(seen)} compared, "
                         f"{bad} mismatches, {missing} missing")
        if bad or missing:
            self.logger.error("TEST FAILED")
        else:
            self.logger.info("TEST PASSED")


class PipeEnv(uvm_env):
    def build_phase(self):
        self.seqr = uvm_sequencer("seqr", self)
        self.drv = Driver("drv", self)
        self.mon_in = InMonitor("mon_in", self)
        self.mon_out = OutMonitor("mon_out", self)
        self.sb = Scoreboard("sb", self)

    def connect_phase(self):
        self.drv.seq_item_port.connect(self.seqr.seq_item_export)
        self.mon_in.ap.connect(self.sb.sent.analysis_export)
        self.mon_out.ap.connect(self.sb.seen.analysis_export)
