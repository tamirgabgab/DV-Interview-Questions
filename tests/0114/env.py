"""Question 0114: the pyuvm environment the page describes but does not show: the items, the
configuration and traffic sequences, the drivers, the agents, the virtual sequencer, the
checker and the base test. tests/0114/test_0114.py appends the page's virtual sequences to
this text, registers a test for each, and runs them on Verilator against the page's pkt_xor."""

import cocotb
import pyuvm
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Event, FallingEdge, RisingEdge
from pyuvm import *

CTRL, KEY = 0, 1                       # the two registers
PACKETS, LENGTH = 8, 3                 # the traffic: 8 packets of 3 bytes
REKEY_AT = 10                          # part ב: the new key, cycles after the traffic starts


class RegWrite(uvm_sequence_item):
    def __init__(self, name="write", addr=CTRL, data=0):
        super().__init__(name)
        self.addr, self.data = addr, data


class Packet(uvm_sequence_item):
    def __init__(self, name="packet", data=()):
        super().__init__(name)
        self.data = list(data)


class ConfigSeq(uvm_sequence):
    """Register writes in order: by default the key, then enable."""
    def __init__(self, name="config", writes=((KEY, 0x5A), (CTRL, 1))):
        super().__init__(name)
        self.writes = writes

    async def body(self):
        for addr, data in self.writes:
            w = RegWrite("write", addr, data)
            await self.start_item(w)
            await self.finish_item(w)


class TrafficSeq(uvm_sequence):
    """PACKETS packets of LENGTH bytes; packet k holds 16k, 16k + 1, ..."""
    async def body(self):
        for k in range(PACKETS):
            await self.send(k)

    async def send(self, k):
        p = Packet(f"p{k}", [16 * k + i for i in range(LENGTH)])
        await self.start_item(p)
        await self.finish_item(p)


class RegDriver(uvm_driver):
    async def run_phase(self):
        dut = cocotb.top
        while True:
            w = await self.seq_item_port.get_next_item()
            dut.cfg_valid.value, dut.cfg_addr.value, dut.cfg_data.value = 1, w.addr, w.data
            await RisingEdge(dut.clk)
            dut.cfg_valid.value = 0
            await ClockCycles(dut.clk, 2)  # the bus takes one write every three cycles
            self.seq_item_port.item_done()


class PktDriver(uvm_driver):
    async def run_phase(self):
        dut = cocotb.top
        while True:
            p = await self.seq_item_port.get_next_item()
            for i, byte in enumerate(p.data):
                dut.in_valid.value, dut.in_last.value, dut.in_data.value = 1, int(i == len(p.data) - 1), byte
                await RisingEdge(dut.clk)
            dut.in_valid.value = 0
            self.seq_item_port.item_done()


class Agent(uvm_agent):
    driver = None                      # the subclass names its driver

    def build_phase(self):
        self.seqr = uvm_sequencer("seqr", self)
        self.drv = self.driver.create("drv", self)

    def connect_phase(self):
        self.drv.seq_item_port.connect(self.seqr.seq_item_export)


class RegAgent(Agent):
    driver = RegDriver


class PktAgent(Agent):
    driver = PktDriver


class VirtualSequencer(uvm_sequencer):
    """No driver: only the handles of the two agents' sequencers."""
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.reg_seqr = self.pkt_seqr = None


def hexes(data):
    return " ".join(f"{b:02x}" for b in data)


class Checker(uvm_component):
    """Predicts every packet from the input pins and compares the output pins, in order."""
    def build_phase(self):
        self.sent = self.out = self.dropped = 0
        self.errors = []

    def error(self, cycle, msg):
        self.errors.append(f"cycle {cycle}: {msg}")
        self.logger.error(self.errors[-1])

    async def run_phase(self):
        dut = cocotb.top
        enable = key = 0                   # the model of the two registers
        pkt, expected, got, cycle = None, [], [], -1
        while True:
            await FallingEdge(dut.clk)     # mid-cycle: what the next rising edge samples
            if not dut.rst_n.value:
                continue
            cycle += 1
            if dut.out_valid.value:        # the output, a cycle behind the input
                got.append(int(dut.out_data.value))
                if dut.out_last.value:
                    k, want = expected.pop(0)
                    self.out += 1
                    if got != want:
                        self.error(cycle, f"packet {k} came out {hexes(got)}, expected {hexes(want)}")
                    got = []
            if dut.in_valid.value:
                if pkt is None:            # the first byte: kept or dropped, and its key
                    pkt = (self.sent, enable, key, [])
                pkt[3].append(int(dut.in_data.value) ^ pkt[2])
                if dut.in_last.value:
                    k, keep, _, data = pkt
                    self.sent += 1
                    if keep:
                        expected.append((k, data))
                    else:
                        self.dropped += 1
                    pkt = None
            if dut.cfg_valid.value:
                if pkt is not None:
                    self.error(cycle, f"a register write during packet {pkt[0]}")
                if dut.cfg_addr.value:
                    key = int(dut.cfg_data.value)
                else:
                    enable = int(dut.cfg_data.value) & 1


class Env(uvm_env):
    def build_phase(self):
        self.reg_agent = RegAgent.create("reg_agent", self)
        self.pkt_agent = PktAgent.create("pkt_agent", self)
        self.vseqr = VirtualSequencer.create("vseqr", self)
        self.checker = Checker.create("checker", self)

    def connect_phase(self):
        self.vseqr.reg_seqr = self.reg_agent.seqr
        self.vseqr.pkt_seqr = self.pkt_agent.seqr


class BaseTest(uvm_test):
    vseq = None                        # the subclass names its virtual sequence

    def build_phase(self):
        self.env = Env.create("env", self)

    async def run_phase(self):
        self.raise_objection()
        dut = cocotb.top
        for s in (dut.cfg_valid, dut.cfg_addr, dut.cfg_data, dut.in_valid, dut.in_last, dut.in_data):
            s.value = 0
        dut.rst_n.value = 0
        cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
        await ClockCycles(dut.clk, 2)
        dut.rst_n.value = 1
        await self.vseq("vseq").start(self.env.vseqr)
        await ClockCycles(dut.clk, 3)      # the last packet leaves the DUT
        self.drop_objection()

    def check_phase(self):
        c, drops = self.env.checker, int(cocotb.top.drops.value)
        self.logger.info(f"{c.sent} packets in, {c.out} out, {drops} dropped, {len(c.errors)} errors")
        assert drops == c.dropped, "the DUT and the model disagree on the dropped packets"
        assert c.out == c.sent and not c.errors, "packets were lost or changed"
