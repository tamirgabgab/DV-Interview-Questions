"""Question 0112: the page's pyuvm code runs on Verilator through cocotb, exactly as
published, spliced into the rest of the testbench (tests/0112/env.py: the item, the sequence,
ParityDriver, the env and the base test) with the DUT of tests/0112/tb.sv. Every scenario the
page states runs: the bug of part a and its fix (the page's fixed line put in place of the
buggy one), the colleague's instance path of part b and its fix, every row of part b's table,
and the follow-ups' type override with an instance override and the override set late. The
lines each run prints are compared with tools/figures/q0112.py, which writes the page's logs
and table and is the reference of the box. The UVM SystemVerilog does not run (Verilator has
no UVM library): the page's blocks and tests/0112/env.sv are checked against the Python."""

import functools
import re
import sys

from extract_code import ROOT, pick

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0112  # noqa: E402

ID = 112
HERE = ROOT / "tests" / "0112"


def py(marker):
    return pick(ID, "python", marker)


def sv(marker):
    return pick(ID, "systemverilog", marker)


ENV = (HERE / "env.py").read_text(encoding="utf-8")
ENV_SV = (HERE / "env.sv").read_text(encoding="utf-8")
DUT = re.search(r"^module parity_rx \(.*?^endmodule\n", (HERE / "tb.sv").read_text(encoding="utf-8"), re.S | re.M)[0]

STMT = py("class ErrDriver(ParityDriver)")                   # the statement: ErrDriver, Agent, ErrTest
AGENT_FIX = py('self.drv = ParityDriver.create("drv", self)')  # part a's fix: the driver's line
CHAN1 = py('ErrDriver, "env.agt1.drv")')                     # part b: the colleague's test
CHAN1_FIX = py('path = f"{self.get_full_name()}.env.agt1.drv"')  # part b's fix: the override's line
BUG_LINE = 'self.drv = ParityDriver("drv", self)'
CHAN1_LINE = 'uvm_factory().set_inst_override_by_type(ParityDriver, ErrDriver, "env.agt1.drv")'
PATH_EXPR = 'f"{self.get_full_name()}.env.agt1.drv"'


def splice(code, line, block):
    """code with its one line `line` replaced by the page's block, at that line's indent."""
    assert code.count(line) == 1, line
    indent = re.search(rf"^([ ]*){re.escape(line)}", code, re.M)[1]
    return code.replace(line, ("\n" + indent).join(block.strip().splitlines()))


FIXED = splice(STMT, BUG_LINE, AGENT_FIX)                     # the statement after part a
CHAN1_FIXED = splice(CHAN1, CHAN1_LINE, CHAN1_FIX)            # part b's test after the fix

ERR_ENTRY = '''

@cocotb.test()
async def err_test(dut):
    Clock(dut.clk, 10, unit="ns").start()
    await uvm_root().run_test(ErrTest)
'''
CHAN1_ENTRY = '''

@cocotb.test()
async def chan1_test(dut):
    Clock(dut.clk, 10, unit="ns").start()
    await uvm_root().run_test(Chan1Test)
'''
# Test-only code. What the factory holds once the test is over (run_test clears the
# overrides only when it starts):
PRINT = '''

@cocotb.test()
async def factory_after(dut):
    uvm_factory().print(0)
'''
# part b, step 2: the print in the colleague's end_of_elaboration_phase
PRINT_ELAB = '''

def _print_overrides(self):
    uvm_factory().print(0)


Chan1Test.end_of_elaboration_phase = _print_overrides
'''
# the factory asked about agt1's driver once the test is over
PROBE = '''

@cocotb.test()
async def probe(dut):
    found = uvm_factory().find_override_by_type(ParityDriver, "uvm_test_top.env.agt1.drv")
    print("PROBE", found.__name__)
'''
# every component under the test, in the order it is built (the box's order)
TRACE = '''

_init = uvm_component.__init__


def _traced(self, name, parent=None):
    _init(self, name, parent)
    if self.get_full_name().startswith("uvm_test_top."):
        print("BUILT", self.get_full_name())


uvm_component.__init__ = _traced
'''
# the follow-up on time: the same instance override made at other times
LATE = '''

WHEN, PATH = {when!r}, {path!r}


class LateTest(ParityTest):
    def build_phase(self):
        self.env = Env.create("env", self)
        if WHEN == "build_after":
            uvm_factory().set_inst_override_by_type(ParityDriver, ErrDriver, PATH)

    def connect_phase(self):
        if WHEN == "connect":
            uvm_factory().set_inst_override_by_type(ParityDriver, ErrDriver, PATH)


@cocotb.test()
async def late_test(dut):
    Clock(dut.clk, 10, unit="ns").start()
    if WHEN == "before_run":
        uvm_factory().set_inst_override_by_type(ParityDriver, ErrDriver, PATH)
    await uvm_root().run_test(LateTest)
'''
# the follow-up on a type override and an instance override of the same type
BOTH = '''

class QuietDriver(ParityDriver):
    pass


class BothTest(ParityTest):
    def build_phase(self):
        uvm_factory().set_type_override_by_type(ParityDriver, ErrDriver)
        uvm_factory().set_inst_override_by_type(ParityDriver, QuietDriver, "uvm_test_top.env.agt0.drv")
        self.env = Env.create("env", self)


@cocotb.test()
async def both_test(dut):
    Clock(dut.clk, 10, unit="ns").start()
    await uvm_root().run_test(BothTest)
'''


def with_path(path):
    """Part b's fixed test with another instance path in place of the full name."""
    assert CHAN1_FIXED.count(PATH_EXPR) == 1
    return CHAN1_FIXED.replace(PATH_EXPR, repr(path))


def scenarios():
    """name -> (module source, the cocotb tests to run in one simulation)."""
    bug, fixed = ENV + STMT, ENV + FIXED
    out = {
        "bug": (bug + ERR_ENTRY + PRINT, ["err_test", "factory_after"]),
        "fixed": (fixed + ERR_ENTRY + PRINT + TRACE, ["err_test", "factory_after"]),
        "colleague": (fixed + CHAN1 + CHAN1_ENTRY + PRINT_ELAB, ["chan1_test"]),
        "both": (fixed + BOTH, ["both_test"]),
    }
    for path, when in q0112.ROWS:
        if when == "build":
            out[f"{when} {path}"] = (fixed + with_path(path) + CHAN1_ENTRY + PRINT_ELAB + PROBE, ["chan1_test", "probe"])
        else:
            out[f"{when} {path}"] = (fixed + LATE.format(when=when, path=path), ["late_test"])
    return out


@functools.cache
def run(name):
    """Run one scenario: (report lines, factory print lines, probe, built components)."""
    from page_tests import run_cocotb

    module, tests = scenarios()[name]
    results, log = run_cocotb("q0112", module, {"parity_rx.sv": DUT}, "parity_rx", tests)
    assert results and all(results.values()), f"{name}: {results}\n{log[-3000:]}"
    lines = re.findall(r"(uvm_test_top\.env\.agt[01]\.drv: \w+, \d+ parity errors)$", log, re.M)
    text = log.splitlines()
    factory = []
    if "--- overrides ---" in text:
        i = text.index("--- overrides ---")
        factory = [line.rstrip() for line in text[i:i + 4]]
    probe = re.findall(r"^PROBE (\w+)$", log, re.M)
    order = re.findall(r"^BUILT (\S+)$", log, re.M)
    return lines, factory, probe, order


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(ID)


# --- the runs ------------------------------------------------------------------------------

def test_statement_bug():
    """The statement's log: new builds ParityDriver, the DUT counts nothing, and the type
    override was registered all the same (part a, step 1)."""
    lines, factory, _, _ = run("bug")
    assert lines == q0112.log_lines(q0112.built(type_override=True, drv="new"))
    assert lines == q0112.log_lines(["ParityDriver", "ParityDriver"])
    assert factory == ["--- overrides ---", "", "Overrides:",
                       f"{'ParityDriver':25}: {'Type Override: ErrDriver':25} ||"]


def test_part_a_fix():
    lines, _, _, order = run("fixed")
    assert lines == q0112.log_lines(q0112.built(type_override=True))
    assert lines == [f"{p}: ErrDriver, 2 parity errors" for p in q0112.DRIVERS]   # 2 of 8 per channel
    tree = [full for full, _, _ in q0112.TREE]             # the box's build order is pyuvm's
    assert [n for n in order if n in tree] == tree           # (the ports are components too)


def test_part_b_colleague():
    """The colleague's test as published: nothing changes, no error; the factory print of
    the colleague's log."""
    lines, factory, _, _ = run("colleague")
    assert lines == q0112.log_lines(["ParityDriver", "ParityDriver"])
    assert lines == q0112.log_lines(q0112.built(inst=(q0112.BAD_PATH, "build")))
    assert factory == q0112.factory_lines(q0112.BAD_PATH)
    assert q0112.colleague_log() == q0112.text_block(factory + [""] + lines)


def test_part_b_colleague_probe():
    """The factory asked about the driver's full name with the colleague's path answers
    ParityDriver."""
    _, factory, probe, _ = run(f"build {q0112.BAD_PATH}")
    assert factory == q0112.factory_lines(q0112.BAD_PATH)
    assert probe == ["ParityDriver"]


def test_part_b_fix():
    """The fixed test: only agt1 is overridden, and find_override_by_type on its driver's
    full name says ErrDriver."""
    lines, factory, probe, _ = run(f"build {q0112.GOOD_PATH}")
    assert factory == q0112.factory_lines("uvm_test_top.env.agt1.drv")
    assert lines == ["uvm_test_top.env.agt0.drv: ParityDriver, 0 parity errors",
                     "uvm_test_top.env.agt1.drv: ErrDriver, 2 parity errors"]
    assert probe == ["ErrDriver"]


def test_part_b_table_and_times():
    """Every row of the table (and of the follow-up on time) is a run of the page's code
    with that path, at that time."""
    for path, when in q0112.ROWS:
        lines, _, _, _ = run(f"{when} {path}")
        assert lines == q0112.log_lines(q0112.built(inst=(path, when))), (path, when)
    # the follow-up and the trap: after Env.create still works, connect_phase and before
    # run_test do not
    late = {when: q0112.built(inst=(q0112.GOOD_PATH, when)) for when in q0112.TIMES}
    assert late["build"] == late["build_after"] == ["ParityDriver", "ErrDriver"]
    assert late["connect"] == late["before_run"] == ["ParityDriver", "ParityDriver"]


def test_instance_and_type_override():
    """The follow-up: the instance override decides on its path, the type override
    everywhere else."""
    lines, _, _, _ = run("both")
    assert lines == ["uvm_test_top.env.agt0.drv: QuietDriver, 0 parity errors",
                     "uvm_test_top.env.agt1.drv: ErrDriver, 2 parity errors"]


# --- the model and the page's numbers ------------------------------------------------------

def test_model():
    assert [s for s in range(q0112.ITEMS) if s % 4 == 3] == [3, 7]       # the items that flip
    assert q0112.wrong_items("ErrDriver") == 2 and q0112.wrong_items("ParityDriver") == 0
    assert "for n in range(8):" in ENV and q0112.ITEMS == 8
    assert "self.sent % 4 == 3" in STMT and ENV.index("self.parity(item.data)") < ENV.index("self.sent += 1")
    # the table: two paths reach agt1 only, one reaches both, the agent's path and the
    # colleague's nothing
    cells = [tuple(q0112.built(inst=row)) for row in q0112.ROWS if row[1] == "build"]
    assert cells == [("ParityDriver", "ErrDriver"), ("ParityDriver", "ParityDriver"), ("ParityDriver", "ParityDriver"),
                     ("ParityDriver", "ErrDriver"), ("ErrDriver", "ErrDriver")]
    # the reasons the box gives for the page's paths, on agt1's driver
    drv1 = q0112.DRIVERS[1]
    assert q0112.why(drv1, q0112.BAD_PATH) == ("suffix", "uvm_test_top")
    assert q0112.why(drv1, "uvm_test_top.env.agt1") == ("ancestor", "uvm_test_top.env.agt1")
    assert q0112.why(q0112.DRIVERS[0], q0112.GOOD_PATH) == ("other", drv1)
    assert q0112.why(q0112.DRIVERS[0], "*.agt1.*") == ("other", drv1)
    assert q0112.why(drv1, "uvm_test_top.env.agt2.drv") == ("none", "")


def test_factory_rules():
    """The follow-ups, on pyuvm's factory itself: a chain of overrides is followed to its
    end, the first instance override registered wins, and a loop is reported."""
    import logging

    from pyuvm import uvm_factory, uvm_object

    class A(uvm_object):
        pass

    class B(A):
        pass

    class C(B):
        pass

    f = uvm_factory()
    f.clear_overrides()
    try:
        f.set_type_override_by_type(A, B)
        f.set_type_override_by_type(B, C)
        assert type(A.create("a")) is C
        f.clear_overrides()
        f.set_inst_override_by_type(A, B, "top.*")
        f.set_inst_override_by_type(A, C, "top.x")
        assert f.find_override_by_type(A, "top.x") is B
        f.clear_overrides()
        f.set_type_override_by_type(A, B)
        f.set_type_override_by_type(B, A)
        seen = []
        handler = logging.Handler()
        handler.emit = seen.append
        logging.getLogger("Factory").addHandler(handler)
        try:
            f.find_override_by_type(A, "")
        finally:
            logging.getLogger("Factory").removeHandler(handler)
        assert any("already overridden" in r.getMessage() for r in seen)
    finally:
        f.clear_overrides()


# --- the SystemVerilog against the Python --------------------------------------------------

NAMES = {"ByteItem": "byte_item", "Bytes": "bytes_seq", "ParityDriver": "parity_driver",
         "ErrDriver": "err_driver", "Agent": "agent", "Env": "tb_env", "ParityTest": "parity_test",
         "ErrTest": "err_test", "Chan1Test": "chan1_test"}


def test_sv_mirrors_python():
    all_py = ENV + STMT + CHAN1
    stmt_sv = sv("function bit err_driver::parity")
    fix_sv = sv('drv  = parity_driver::type_id::create("drv", this);')
    chan1_sv = sv('"env.agt1.drv");')
    chan1_fix_sv = sv('string path = {get_full_name(), ".env.agt1.drv"};')
    for p, s in NAMES.items():
        assert f"class {p}(" in all_py and f"class {s} extends" in ENV_SV, p
        assert f"`uvm_component_utils({s})" in ENV_SV or f"`uvm_object_utils({s})" in ENV_SV, s
    # every function the page defines out of its class is declared extern in env.sv
    for code in (stmt_sv, chan1_sv):
        for ret, cls, name, args in re.findall(r"^function (bit|void) (\w+)::(\w+)\((.*?)\);", code, re.M):
            body = ENV_SV.split(f"class {cls} extends", 1)[1].split("endclass", 1)[0]
            assert f"extern function {ret} {name}({args});" in body, (cls, name)
    # the stimulus and the error injection
    assert "for (int n = 0; n < 8; n++)" in ENV_SV and ENV_SV.count("37 * n % 256") == 1 and "37 * n % 256" in ENV
    assert "super.parity(data) ^ (sent % 4 == 3)" in stmt_sv and "virtual function bit parity" in ENV_SV
    assert "super().parity(data) ^ (self.sent % 4 == 3)" in STMT
    # part a: the bug and the fix, the type override
    assert BUG_LINE in STMT and 'drv  = new("drv", this);' in stmt_sv
    assert 'self.drv = ParityDriver.create("drv", self)' in FIXED
    assert stmt_sv.replace('drv  = new("drv", this);', fix_sv.split("//")[0].strip()) != stmt_sv
    assert "uvm_factory().set_type_override_by_type(ParityDriver, ErrDriver)" in STMT
    assert "parity_driver::type_id::set_type_override(err_driver::get_type());" in stmt_sv
    # the buses: the env's relative paths are the top's full ones
    assert 'ConfigDB().set(self, "agt0.*", "BUS"' in ENV and '"uvm_test_top.env.agt0.*", "BUS", ch0' in ENV_SV
    assert 'ConfigDB().set(self, "agt1.*", "BUS"' in ENV and '"uvm_test_top.env.agt1.*", "BUS", ch1' in ENV_SV
    # part b: the colleague's call and the fix, the same factory method in both languages
    assert CHAN1_LINE in CHAN1
    assert ('factory.set_inst_override_by_type(parity_driver::get_type(), err_driver::get_type(), "env.agt1.drv");'
            in chan1_sv)
    assert PATH_EXPR in CHAN1_FIX and "set_inst_override_by_type(ParityDriver, ErrDriver, path)" in CHAN1_FIX
    assert "factory.set_inst_override_by_type(parity_driver::get_type(), err_driver::get_type(), path);" in chan1_fix_sv
    assert "uvm_factory factory = uvm_factory::get();" in chan1_sv      # the fix's factory
    assert "function void end_of_elaboration_phase" in ENV_SV and "factory.print(0);" in ENV_SV
    for code in (CHAN1, CHAN1_FIXED, chan1_sv, chan1_fix_sv):            # no type override in part b
        assert "set_type_override" not in code and "super" not in code
