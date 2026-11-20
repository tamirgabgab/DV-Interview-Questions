"""Question 0114: the page's virtual sequences of parts א and ב, spliced into the pyuvm
environment of tests/0114/env.py, run on Verilator against tests/0114/pkt_xor.sv as published
(the tests fail and pass as the page says, the logs on the page are the run's, and the pins of
every cycle are the cycle model's of tools/figures/q0114.py, from which the waveform is drawn);
the arbitration model of part ג (q0114.sequencer, running the page's sequences) follows the
rules of IEEE 1800.2 for lock, grab and the two modes it has; the SystemVerilog tabs, which no
test can run (Verilator has no UVM library), are checked against the Python: the same classes
and the same calls in the same order."""

import json
import re
import sys
import textwrap

import pytest

from extract_code import ROOT, pick, question_path

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0114  # noqa: E402

HERE = ROOT / "tests" / "0114"
PAGE = question_path(114).read_text(encoding="utf-8")
ENV = (HERE / "env.py").read_text(encoding="utf-8")
DUT = (HERE / "pkt_xor.sv").read_text(encoding="utf-8")
TESTS = {"BootTest": "boot_bug", "BootTestFixed": "boot_fix", "RekeyTest": "rekey_bug", "RekeyTestFixed": "rekey_fix"}

# a test for each virtual sequence of the page, and every test prints the pins of every cycle
TAIL = '''

@pyuvm.test()
class BootTest(BaseTest):
    vseq = BootVseq


@pyuvm.test()
class BootTestFixed(BaseTest):
    vseq = BootVseqFixed


@pyuvm.test()
class RekeyTest(BaseTest):
    vseq = RekeyVseq


@pyuvm.test()
class RekeyTestFixed(BaseTest):
    vseq = RekeyVseqFixed


import json as _json

_page_run_phase = BaseTest.run_phase
_PINS = ["cfg_valid", "cfg_addr", "cfg_data", "in_valid", "in_last", "in_data",
         "out_valid", "out_last", "out_data", "drops", "enable", "key"]


async def _record():
    dut = cocotb.top
    while True:
        await FallingEdge(dut.clk)
        if dut.rst_n.value:
            print("ROW", _json.dumps({n: int(getattr(dut, n).value) for n in _PINS}), flush=True)


async def _recorded_run_phase(self):
    cocotb.start_soon(_record())
    await _page_run_phase(self)

BaseTest.run_phase = _recorded_run_phase
'''


def sv(marker):
    return pick(114, "systemverilog", marker)


def py(marker):
    return pick(114, "python", marker)


@pytest.fixture(scope="module")
def run():
    """Each test: passed, its log lines and its recorded pins."""
    from page_tests import run_cocotb

    module = "\n\n".join([ENV] + [py(m) for m in ("class BootVseq(", "class BootVseqFixed(",
                                                  "class RekeyVseq(", "class Pause:")]) + TAIL
    results, log = run_cocotb("q0114", module, {"pkt_xor.sv": DUT}, "pkt_xor")
    out, name = {}, None
    for line in log.splitlines():
        m = re.search(r"running q0114_tb\.(\w+) ", line)
        if m:
            name = m.group(1)
            out[name] = dict(passed=results[name], lines=[], rows=[])
        elif name and line.startswith("ROW "):
            out[name]["rows"].append(json.loads(line[4:]))
        elif name:
            out[name]["lines"].append(line)
    return out


def test_the_page_tests_fail_and_pass_as_the_page_says(run):
    assert {n: r["passed"] for n, r in run.items()} == {"BootTest": False, "BootTestFixed": True,
                                                        "RekeyTest": False, "RekeyTestFixed": True}


def summary(r):
    found = [m.group(0) for line in r["lines"] for m in [re.search(r"\d+ packets in, .* errors", line)] if m]
    assert len(found) == 1
    return found[0]


def test_the_logs_on_the_page_are_the_runs(run):
    shown = re.findall(r'```text title="(\w+)"\n(.*?)```', PAGE, re.S)
    assert [t for t, _ in shown] == ["BootTest", "RekeyTest"]
    for test, text in shown:
        lines = [line.strip().split(None, 1) for line in textwrap.dedent(text).splitlines()]
        errors = [m.group(1) for line in run[test]["lines"]
                  for m in [re.search(r"ERROR .*\[uvm_test_top\.env\.checker\]: (.*)$", line)] if m]
        assert errors == [msg for level, msg in lines if level == "ERROR"]
        assert [msg for level, msg in lines if level == "INFO"] == [summary(run[test])]
        fails = [msg for level, msg in lines if level == "FAIL"]
        assert len(fails) == 1 and any(fails[0] in line for line in run[test]["lines"])


def test_the_fixed_runs(run):
    for test in ("BootTestFixed", "RekeyTestFixed"):
        assert summary(run[test]) == "8 packets in, 8 out, 0 dropped, 0 errors"
        assert not any("ERROR" in line and "checker" in line for line in run[test]["lines"])
    assert PAGE.count("`8 packets in, 8 out, 0 dropped, 0 errors`") == 2


def test_the_pins_are_the_cycle_models(run):
    for test, case in TESTS.items():
        assert run[test]["rows"] == q0114.trace(case), test


def test_the_environment_the_page_describes():
    assert "PACKETS, LENGTH = 8, 3" in ENV and (q0114.PACKETS, q0114.LENGTH) == (8, 3)
    assert "REKEY_AT = 10" in ENV and q0114.REKEY_AT == 10 and "# REKEY_AT = 10" in py("class RekeyVseq(")
    assert "writes=((KEY, 0x5A), (CTRL, 1))" in ENV and q0114.KEY_A == 0x5A
    assert "await ClockCycles(dut.clk, 2)  # the bus takes one write every three cycles" in ENV and q0114.GAP == 3
    assert "async def send(self, k):" in ENV
    assert "self.vseqr.reg_seqr = self.reg_agent.seqr" in ENV and "self.reg_seqr = self.pkt_seqr = None" in ENV
    assert 'f"a register write during packet {pkt[0]}"' in ENV
    assert "always_ff @(posedge clk or negedge rst_n)" in DUT and "if (!mid && !enable) drops <= drops + 1;" in DUT


def first(rows, cond):
    return next(t for t, r in enumerate(rows) if cond(r))


def test_part_a_numbers():
    bug, fix = q0114.trace("boot_bug"), q0114.trace("boot_fix")
    writes, starts = q0114.plan("boot_bug")
    assert writes == [(0, q0114.KEY, 0x5A), (3, q0114.CTRL, 1)]
    assert first(bug, lambda r: r["enable"]) == 4                 # "the block works from cycle 4"
    assert starts[:3] == [0, 3, 6]                                # packets 0 and 1 start before it
    assert [r["drops"] for r in bug[:5]] == [0, 1, 1, 1, 2]
    assert first(bug, lambda r: r["out_valid"]) == 7 and bug[7]["out_data"] == 0x20 ^ 0x5A
    assert bug[-1]["drops"] == 2 and sum(r["out_valid"] and r["out_last"] for r in bug) == 6
    assert first(fix, lambda r: r["in_valid"]) == 6 and fix[6]["enable"] == 1
    assert fix[-1]["drops"] == 0 and sum(r["out_valid"] and r["out_last"] for r in fix) == 8
    assert (len(bug), len(fix)) == (27, 33)


def test_part_b_numbers():
    bug, fix = q0114.trace("rekey_bug"), q0114.trace("rekey_fix")
    assert q0114.plan("rekey_bug")[0][-1] == (16, q0114.KEY, 0xC3)
    assert q0114.plan("rekey_bug")[1][3] == 15                    # packet 3: cycles 15 to 17
    assert bug[17]["key"] == 0xC3 and bug[17]["in_data"] == 0x32
    assert bug[18]["out_data"] == 0x32 ^ 0xC3 == 0xF1 and 0x32 ^ 0x5A == 0x68
    assert [f"{r['out_data']:02x}" for r in bug[16:19]] == ["6a", "6b", "f1"]
    writes, starts = q0114.plan("rekey_fix")
    assert writes[-1] == (18, q0114.KEY, 0xC3) and starts[3:5] == [15, 21]
    assert [fix[t]["in_valid"] for t in range(17, 22)] == [1, 0, 0, 0, 1]
    keys = []
    for k, s in enumerate(starts):
        keys.append({fix[s + i + 1]["out_data"] ^ (16 * k + i) for i in range(q0114.LENGTH)})
    assert keys == [{0x5A}] * 4 + [{0xC3}] * 4
    assert (len(bug), len(fix)) == (33, 36)


# --- part ג: the model against the rules of IEEE 1800.2 ---------------------------------------------

M = q0114.model()
Seq, sequencer, traffic, irq = M["Seq"], M["sequencer"], M["traffic"], M["irq"]


def ab():
    return [traffic("A"), traffic("B")]


def test_fifo_takes_the_oldest_request_and_ignores_priority():
    assert sequencer(ab()) == [x for i in range(6) for x in (f"A{i}", f"B{i}")]
    plain = sequencer(ab() + [irq()])
    assert plain == sequencer(ab() + [irq(priority=500)])
    assert plain[:11] == "A0 B0 A1 I0 B1 A2 B2 I1 A3 B3 I2".split()


def test_strict_fifo_takes_the_highest_priority_but_not_in_a_row():
    order = sequencer(ab() + [irq(priority=500)], "STRICT_FIFO")
    assert order[:7] == "A0 B0 I0 A1 I1 I2 B1".split()
    # with equal priorities STRICT_FIFO is FIFO
    assert sequencer(ab() + [irq()], "STRICT_FIFO") == sequencer(ab() + [irq()])


def test_lock_waits_for_the_requests_queued_before_it_then_serves_only_its_holder():
    order = sequencer(ab() + [irq("lock")])
    assert order[:8] == "A0 B0 A1 I0 - I1 I2 B1".split()
    # A1 asked at slot 1, before the lock (1.5): served first; B1 asked at slot 2: after unlock


def test_grab_goes_to_the_head_of_the_queue():
    order = sequencer(ab() + [irq("grab")])
    assert order[:8] == "A0 B0 I0 - I1 I2 A1 B1".split()


def test_a_lock_on_an_idle_sequencer_is_granted_at_once():
    assert sequencer([Seq("L", [("lock",), ("item", "L0"), ("unlock",)])]) == ["L0"]


@pytest.mark.parametrize("how", ["lock", "grab"])
def test_a_lock_or_grab_waits_while_another_sequence_holds_a_lock(how):
    holder = Seq("L", [("lock",), ("item", "L0"), ("wait", 2), ("item", "L1"), ("unlock",)])
    late = Seq("G", [(how,), ("item", "G0"), ("un" + how,)], start=0.5)
    order = sequencer([holder, late, traffic("A", 3)])
    assert order.index("G0") > order.index("L1")
    assert order[:4] == ["L0", "-", "-", "L1"]                    # nobody else while L holds it


def test_a_locked_sequencer_serves_the_children_of_its_holder():
    child = Seq("C", [("item", "C0"), ("item", "C1")])
    holder = Seq("I", [("lock",), ("item", "I0"), ("run", child), ("item", "I1"), ("unlock",)], start=1.5)
    order = sequencer(ab() + [holder])
    at = order.index("I0")
    assert order[at:at + 4] == ["I0", "C0", "C1", "I1"]
    # the same sequence started by someone else (no parent) is blocked by the lock
    other = Seq("C", [("item", "C0")], start=2.5)
    order = sequencer(ab() + [irq("lock"), other])
    i0, i2 = order.index("I0"), order.index("I2")
    assert "C0" not in order[i0:i2] and order.index("C0") > i2


def test_every_item_is_given_once():
    for _, _, order in q0114.orders():
        items = [x for x in order if x != "-"]
        assert sorted(items) == sorted([f"A{i}" for i in range(6)] + [f"B{i}" for i in range(6)] + ["I0", "I1", "I2"])


def test_the_snapshots_are_the_arbitrations():
    for mode in ("FIFO", "STRICT_FIFO"):
        for how in (None, "lock", "grab"):
            snaps = []
            order = q0114.run_case(mode, snaps, how=how, priority=500)
            assert [s["out"] for s in snaps] == order
            for s, x in zip(snaps, order):
                assert x == "-" or ["item", x[0], x] in s["queue"]


def test_the_table_of_part_c():
    got = {label: (mode, q0114.together(order)) for label, mode, order in q0114.orders()}
    assert [v for v in got.values()] == [("FIFO", False), ("FIFO", False), ("STRICT_FIFO", False),
                                         ("FIFO", True), ("FIFO", True)]
    for mode in ("FIFO", "STRICT_FIFO", "WEIGHTED", "RANDOM", "STRICT_RANDOM", "USER"):
        assert f"`UVM_SEQ_ARB_{mode}`" in PAGE


# --- the SystemVerilog tabs against the Python -------------------------------------------------------

def order_of(text, *calls):
    at = [text.index(c) for c in calls]
    return at == sorted(at)


def test_sv_boot_vseq():
    bug, fix = sv("class boot_vseq extends"), sv("class boot_vseq_fixed")
    p_bug, p_fix = py("class BootVseq("), py("class BootVseqFixed(")
    assert "fork" in bug and order_of(bug, "fork", "cfg.start(p_sequencer.reg_seqr, this);",
                                      "traffic.start(p_sequencer.pkt_seqr, this);", "join")
    assert "cocotb.start_soon(ConfigSeq(" in p_bug and "await TrafficSeq(" in p_bug
    assert "fork" not in fix and order_of(fix, "cfg.start(p_sequencer.reg_seqr, this);",
                                          "traffic.start(p_sequencer.pkt_seqr, this);")
    assert "start_soon" not in p_fix and order_of(p_fix, "await ConfigSeq(", "await TrafficSeq(")
    assert "uvm_sequencer #(reg_write) reg_seqr;" in fix and "uvm_sequencer #(packet)    pkt_seqr;" in fix
    assert "vseqr.reg_seqr = reg_agent.seqr" in fix


def test_sv_rekey():
    bug, fix = sv("class rekey_vseq extends"), sv("class pause_c")
    p_bug, p_fix = py("class RekeyVseq("), py("class Pause:")
    assert "int rekey_at = 10;" in bug
    assert order_of(bug, "boot.start(", "traffic.start(", "#(rekey_at * 10ns);", "rekey.start(", "wait fork;")
    assert order_of(p_bug, 'ConfigSeq("boot")', "TrafficSeq(", "ClockCycles(", 'ConfigSeq("rekey", [(KEY, 0xC3)])')
    assert "'{'{KEY, 8'hC3}}" in bug and "'{'{KEY, 8'hC3}}" in fix
    for name in ("task boundary();", "task request();", "function void resume();"):
        assert name in fix
    for name in ("async def boundary(self):", "async def request(self):", "def resume(self):"):
        assert name in p_fix
    assert order_of(fix, "pause.boundary();", "super.send(k);")
    assert order_of(p_fix, "await self.pause.boundary()", "await super().send(k)")
    assert order_of(fix, "#(rekey_at * 10ns);", "pause.request();", "rekey.start(", "pause.resume();", "wait fork;")
    assert order_of(p_fix, "ClockCycles(", "await pause.request()", 'ConfigSeq("rekey"', "pause.resume()", "await traffic")


def test_sv_irq_seq():
    s, p = sv("class irq_seq"), py("def irq(")
    assert order_of(s, "m_sequencer.grab(this);", "m_sequencer.lock(this);", 'send_one("I0");', "get_response(rsp);",
                    'send_one("I1");', 'send_one("I2");', "m_sequencer.ungrab(this);", "m_sequencer.unlock(this);")
    assert 'steps = [("item", "I0"), ("wait", 1), ("item", "I1"), ("item", "I2")]' in p
    assert 'steps = [(how,)] + steps + [("un" + how,)]' in p
    assert "`set_arbitration()`" in PAGE and "`irq.start(p_sequencer.pkt_seqr, this, 500)`" in PAGE


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(114)
