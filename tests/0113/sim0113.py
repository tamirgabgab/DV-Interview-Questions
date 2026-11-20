"""Question 0113: run the page's pyuvm testbench on Verilator (helpers of test_0113_sim.py).

Every scenario is a module made of the page's own Python blocks, in page order, plus a few
test-only lines; each runs in its own simulation (run_cocotb with tests=[...]), so every run
starts at time 0 with a fresh DUT. The build is shared: the SystemVerilog is the page's
module pipe, the same for every run."""

from __future__ import annotations

import json
import re
import shutil
from functools import lru_cache

from extract_code import ROOT, pick
from page_tests import run_cocotb

MARKERS = {
    "env": "class PipeEnv(uvm_env)",
    "smoke": "class SmokeTest(uvm_test)",
    "objection": "class ObjectionTest(SmokeTest)",
    "drain": "class DrainTest(SmokeTest)",
    "colleague": "await super().run_phase()",
    "timeout": "with_timeout(uvm_root().run_test",
}

LINE = re.compile(r"^\s*(?P<t>[\d.]+)ns (?P<lvl>[A-Z]+)\s+(?P<src>\S+)(?: \[(?P<who>[^\]]*)\]:)?\s+(?P<msg>.*)$")


def page(*parts: str) -> str:
    return "\n\n".join(pick(113, "python", MARKERS[p]) for p in parts)


def dut() -> dict[str, str]:
    return {"pipe.sv": pick(113, "systemverilog", "module pipe #(")}


# Test-only cocotb tests: the traps of the page, each with its numbers printed as JSON.
EXTRA = '''

import json as _json


def _report(**kv):
    print("Q113 " + _json.dumps(kv), flush=True)


class LateTest(SmokeTest):
    async def run_phase(self):
        await ClockCycles(cocotb.top.clk, 1)
        self.raise_objection()
        await ItemSeq("seq").start(self.env.seqr)
        self.drop_objection()


class ForkTest(SmokeTest):
    async def run_phase(self):
        self.raise_objection()
        cocotb.start_soon(ItemSeq("seq").start(self.env.seqr))
        self.drop_objection()


class TwiceTest(SmokeTest):
    async def run_phase(self):
        self.raise_objection()
        self.raise_objection()
        await ItemSeq("seq").start(self.env.seqr)
        self.drop_objection()


class DropOnlyTest(SmokeTest):
    async def run_phase(self):
        self.drop_objection()
        await ItemSeq("seq").start(self.env.seqr)


async def _bounded(dut, test, limit_ns=2000):
    cocotb.start_soon(Clock(dut.clk, 10, "ns").start(start_high=False))
    try:
        await with_timeout(uvm_root().run_test(test), limit_ns, "ns")
        done = True
    except SimTimeoutError:
        done = False
    _report(test=test.__name__, done=done, end=get_sim_time("ns"),
            count=ObjectionHandler().get_objection_count())


@cocotb.test()
async def late(dut):
    await _bounded(dut, LateTest)


@cocotb.test()
async def fork(dut):
    await _bounded(dut, ForkTest)


@cocotb.test()
async def twice(dut):
    await _bounded(dut, TwiceTest)


@cocotb.test()
async def drop_only(dut):
    await _bounded(dut, DropOnlyTest)
'''


@lru_cache(maxsize=None)
def run(module: str, test: str) -> tuple[bool, str]:
    # run_cocotb rewrites the module file in place: two modules of the same size written in
    # the same second (DRAIN_NS = 10, then 20) would reuse the first one's cached bytecode
    shutil.rmtree(ROOT / ".cache" / "cocotb" / "q0113" / "__pycache__", ignore_errors=True)
    results, log = run_cocotb("q0113", module, dut(), "pipe", tests=[test])
    return results[test], log


def records(log: str) -> list[dict]:
    """The log lines of the run: time, level, source, the component in brackets, message."""
    out = []
    for line in log.splitlines():
        m = LINE.match(line)
        if m:
            out.append({**m.groupdict(), "t": float(m["t"])})
    return out


def scoreboard(log: str) -> list[tuple[float, str, str, str]]:
    """The scoreboard's lines: (time, level, component, message)."""
    return [(r["t"], r["lvl"], r["who"], r["msg"]) for r in records(log) if r["who"] == "uvm_test_top.env.sb"]


def reports(log: str) -> list[dict]:
    return [json.loads(line.split("Q113 ", 1)[1]) for line in log.splitlines() if "Q113 {" in line]


def end_time(log: str) -> float:
    """The simulation time at the end of the cocotb test (its PASS / FAIL line)."""
    m = re.search(r"^\s*([\d.]+)ns \w+\s+cocotb\.regression\s+\S+ (?:passed|failed)", log, re.M)
    return float(m[1])
