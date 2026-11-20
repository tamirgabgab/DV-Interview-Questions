"""Question 0112: the part of the pyuvm testbench the page describes in words. test_0112.py
appends the page's Python blocks (ErrDriver, Agent, the tests) and the cocotb entries to this
file and runs the result on Verilator: the sequence item, the sequence, the plain driver, the
env and the base test that runs the sequences and prints the report lines."""

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
import pyuvm
from pyuvm import *


class ByteItem(uvm_sequence_item):
    def __init__(self, name="item"):
        super().__init__(name)
        self.data = 0


class Bytes(uvm_sequence):
    """Eight bytes on one channel."""

    async def body(self):
        for n in range(8):
            item = ByteItem.create(f"item{n}")
            await self.start_item(item)
            item.data = 37 * n % 256
            await self.finish_item(item)


class ParityDriver(uvm_driver):
    """A byte and its even parity bit, one item every two cycles."""

    def build_phase(self):
        # the channel's signals, as a virtual interface in SystemVerilog: the env sets them
        # for each agent
        self.valid, self.data, self.par, self.errs = ConfigDB().get(self, "", "BUS")
        self.sent = 0

    def parity(self, data):
        return bin(data).count("1") % 2

    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()
            await FallingEdge(cocotb.top.clk)
            self.valid.value = 1
            self.data.value = item.data
            self.par.value = self.parity(item.data)
            self.sent += 1
            await FallingEdge(cocotb.top.clk)
            self.valid.value = 0
            self.seq_item_port.item_done()


class Env(uvm_env):
    def build_phase(self):
        # pyuvm's run_test clears ConfigDB (and the factory's overrides) before it builds the
        # test, so the signals are set here, inside the tree, and not in the cocotb test
        dut = cocotb.top
        ConfigDB().set(self, "agt0.*", "BUS", (dut.valid0, dut.data0, dut.par0, dut.errs0))
        ConfigDB().set(self, "agt1.*", "BUS", (dut.valid1, dut.data1, dut.par1, dut.errs1))
        self.agt0 = Agent.create("agt0", self)
        self.agt1 = Agent.create("agt1", self)


class ParityTest(uvm_test):
    """Eight bytes on each channel, then one line per driver: its class and the DUT's count."""

    async def run_phase(self):
        self.raise_objection()
        for agt in (self.env.agt0, self.env.agt1):
            await Bytes.create("bytes").start(agt.seqr)
        self.drop_objection()

    def report_phase(self):
        for agt in (self.env.agt0, self.env.agt1):
            drv = agt.drv
            self.logger.info(f"{drv.get_full_name()}: {drv.get_type_name()}, "
                             f"{int(drv.errs.value)} parity errors")
