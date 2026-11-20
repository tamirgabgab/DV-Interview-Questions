"""Question 0112: the page's pyuvm testbench runs on Verilator through cocotb, exactly as
published, in every scenario the page states (the bug of part a and its fix, the colleague's
instance path of part b and its fix, every row of part b's table, an instance override with a
type override). The lines each run prints are compared with tools/figures/q0112.py, which
writes the page's logs and table. The UVM SystemVerilog of the page does not run (Verilator
has no UVM library): its classes and the calls the question is about are checked against the
Python. tests/0112/tb.sv runs the DUT on its own."""

import functools
import re
import sys

from extract_code import ROOT, pick

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0112  # noqa: E402

ID = 112


def py(marker):
    return pick(ID, "python", marker)


def sv(marker):
    return pick(ID, "systemverilog", marker)


DUT = sv("module parity_rx (")
DRIVERS = py("class ErrDriver(ParityDriver)")          # statement: item, sequence, drivers
BENCH = py("class ErrTest(uvm_test)")                  # statement: agent (the bug), env, test
AGENT_FIX = py('ParityDriver.create("drv", self)')     # part a's fix
CHAN1 = py('ErrDriver, "env.agt1.drv")')               # part b: the colleague's test
CHAN1_FIX = py("uvm_factory().print(0)")               # part b's fix
PATH_EXPR = 'f"{self.get_full_name()}.env.agt1.drv"'

# Test-only cocotb tests, run after a published one in the same simulation: what the
# factory holds once that test is over (run_test clears the overrides only when it starts).
PRINT = '''

@cocotb.test()
async def factory_after(dut):
    uvm_factory().print(0)
'''
PROBE = '''

@cocotb.test()
async def probe(dut):
    found = uvm_factory().find_override_by_type(ParityDriver, "uvm_test_top.env.agt1.drv")
    print("PROBE", found.__name__)
'''
# Part b's table: the same instance override made at other times.
LATE = '''

WHEN, PATH = {when!r}, {path!r}


class LateTest(ErrTest):
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
# Part b's note: a type override and an instance override of the same type.
BOTH = '''

class QuietDriver(ParityDriver):
    pass


class BothTest(ErrTest):
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
    assert CHAN1_FIX.count(PATH_EXPR) == 1
    return CHAN1_FIX.replace(PATH_EXPR, repr(path))


def scenarios():
    """name -> (module source, the cocotb tests to run in one simulation)."""
    fixed = DRIVERS + BENCH + AGENT_FIX
    out = {
        "bug": (DRIVERS + BENCH + PRINT, ["err_test", "factory_after"]),
        "fixed": (fixed + PRINT, ["err_test", "factory_after"]),
        "colleague": (fixed + CHAN1, ["chan1_test"]),
        "both": (fixed + BOTH, ["both_test"]),
    }
    for path, when in q0112.ROWS:
        if when == "build":
            fix = CHAN1_FIX if path == q0112.GOOD_PATH else with_path(path)
            out[f"{when} {path}"] = (fixed + CHAN1 + fix + PROBE, ["chan1_test", "probe"])
        else:
            out[f"{when} {path}"] = (fixed + LATE.format(when=when, path=path), ["late_test"])
    return out


@functools.cache
def run(name):
    """Run one scenario: (results, report lines, factory print lines, probe)."""
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
    return results, lines, factory, probe


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(ID)


# --- the runs ------------------------------------------------------------------------------

def test_statement_bug():
    """The statement's log: new() builds ParityDriver, the DUT counts nothing, and the type
    override was registered all the same (part a, step 2)."""
    _, lines, factory, _ = run("bug")
    assert lines == q0112.log_lines(["ParityDriver", "ParityDriver"])
    assert factory == ["--- overrides ---", "", "Overrides:",
                       f"{'ParityDriver':25}: {'Type Override: ErrDriver':25} ||"]


def test_part_a_fix():
    _, lines, _, _ = run("fixed")
    assert lines == q0112.log_lines(q0112.built(type_override=True))
    assert lines == [f"{p}: ErrDriver, 2 parity errors" for p in q0112.DRIVERS]   # 2 of 8 per channel


def test_part_b_colleague():
    """The colleague's test as published: nothing changes, no error."""
    _, lines, _, _ = run("colleague")
    assert lines == q0112.log_lines(["ParityDriver", "ParityDriver"])
    assert lines == q0112.log_lines(q0112.built(inst=(q0112.BAD_PATH, "build")))


def test_part_b_colleague_debug():
    """Part b's log: the factory print with the colleague's path, and the factory asked
    about the driver's full name answers ParityDriver."""
    _, lines, factory, probe = run(f"build {q0112.BAD_PATH}")
    assert factory == q0112.factory_lines(q0112.BAD_PATH)
    assert q0112.colleague_log() == q0112.text_block(factory + [""] + lines)
    assert probe == ["ParityDriver"]


def test_part_b_fix():
    """The fixed test: the full name is uvm_test_top.env.agt1.drv, only agt1 is overridden,
    and find_override_by_type on that path says ErrDriver."""
    _, lines, factory, probe = run(f"build {q0112.GOOD_PATH}")
    assert factory == q0112.factory_lines("uvm_test_top.env.agt1.drv")
    assert lines == ["uvm_test_top.env.agt0.drv: ParityDriver, 0 parity errors",
                     "uvm_test_top.env.agt1.drv: ErrDriver, 2 parity errors"]
    assert probe == ["ErrDriver"]


def test_part_b_table():
    """Every row of the table is a run of the page's code with that path, at that time."""
    for path, when in q0112.ROWS:
        _, lines, _, _ = run(f"{when} {path}")
        assert lines == q0112.log_lines(q0112.built(inst=(path, when))), (path, when)


def test_instance_and_type_override():
    """The instance override decides on its path, the type override everywhere else."""
    _, lines, _, _ = run("both")
    assert lines == ["uvm_test_top.env.agt0.drv: QuietDriver, 0 parity errors",
                     "uvm_test_top.env.agt1.drv: ErrDriver, 2 parity errors"]


# --- the model and the page's numbers ------------------------------------------------------

def test_model():
    assert [s for s in range(q0112.ITEMS) if s % 4 == 3] == [3, 7]       # the items that flip
    assert q0112.wrong_items("ErrDriver") == 2 and q0112.wrong_items("ParityDriver") == 0
    assert "for n in range(8):" in DRIVERS and q0112.ITEMS == 8
    assert "self.sent % 4 == 3" in DRIVERS and DRIVERS.index("self.parity(item.data)") < DRIVERS.index("self.sent += 1")
    # the table: two paths reach agt1 only, one reaches both, the rest nothing
    cells = [tuple(q0112.built(inst=row)) for row in q0112.ROWS]
    assert cells.count(("ParityDriver", "ErrDriver")) == 3 and cells.count(("ErrDriver", "ErrDriver")) == 1
    assert cells.count(("ParityDriver", "ParityDriver")) == 4


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


# --- the SystemVerilog tabs against the Python ---------------------------------------------

NAMES = {"ByteItem": "byte_item", "Bytes": "bytes_seq", "ParityDriver": "parity_driver",
         "ErrDriver": "err_driver", "Agent": "agent", "Env": "tb_env", "ErrTest": "err_test",
         "Chan1Test": "chan1_test"}


def test_sv_mirrors_python():
    page_py = "\n".join(q for q in (DRIVERS, BENCH, AGENT_FIX, CHAN1, CHAN1_FIX))
    page_sv = "\n".join(sv(m) for m in ("class err_driver", "class err_test", "drv  = parity_driver",
                                         '"env.agt1.drv");', "factory.print(0)"))
    for p, s in NAMES.items():
        assert f"class {p}(" in page_py and f"class {s} extends" in page_sv, p
        assert f"`uvm_component_utils({s})" in page_sv or f"`uvm_object_utils({s})" in page_sv, s
    stmt_sv = sv("class err_test") + sv("class err_driver")
    # the stimulus and the error injection
    assert "for (int n = 0; n < 8; n++)" in stmt_sv and stmt_sv.count("37 * n % 256") == 1
    assert "super.parity(data) ^ (sent % 4 == 3)" in stmt_sv and "virtual function bit parity" in stmt_sv
    assert "super().parity(data) ^ (self.sent % 4 == 3)" in DRIVERS
    # part a: the bug and the fix, the type override
    assert 'self.drv = ParityDriver("drv", self)' in BENCH and 'drv  = new("drv", this);' in stmt_sv
    assert 'self.drv = ParityDriver.create("drv", self)' in AGENT_FIX
    assert 'drv  = parity_driver::type_id::create("drv", this);' in sv("drv  = parity_driver")
    assert "uvm_factory().set_type_override_by_type(ParityDriver, ErrDriver)" in BENCH
    assert "parity_driver::type_id::set_type_override(err_driver::get_type());" in stmt_sv
    # the buses: the env's relative paths are the top's full ones
    assert 'ConfigDB().set(self, "agt0.*", "BUS"' in BENCH and '"uvm_test_top.env.agt0.*", "BUS", ch0' in stmt_sv
    assert 'ConfigDB().set(self, "agt1.*", "BUS"' in BENCH and '"uvm_test_top.env.agt1.*", "BUS", ch1' in stmt_sv
    # part b: the colleague's call and the fix, the same factory method in both languages
    assert 'uvm_factory().set_inst_override_by_type(ParityDriver, ErrDriver, "env.agt1.drv")' in CHAN1
    assert ('factory.set_inst_override_by_type(parity_driver::get_type(), err_driver::get_type(), "env.agt1.drv");'
            in sv('"env.agt1.drv");'))
    fix_sv = sv("factory.print(0)")
    assert PATH_EXPR in CHAN1_FIX and 'string path = {get_full_name(), ".env.agt1.drv"};' in fix_sv
    assert "set_inst_override_by_type(ParityDriver, ErrDriver, path)" in CHAN1_FIX
    assert "factory.set_inst_override_by_type(parity_driver::get_type(), err_driver::get_type(), path);" in fix_sv
    assert "def end_of_elaboration_phase" in CHAN1_FIX and "function void end_of_elaboration_phase" in fix_sv
    for code in (CHAN1, CHAN1_FIX, fix_sv, sv('"env.agt1.drv");')):    # no type override in part b
        assert "set_type_override" not in code and "super" not in code.split("build_phase")[1].split("\n")[1]
