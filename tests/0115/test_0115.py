"""Question 0115, the monitor that sees mismatches the DUT does not have: the page's numbers
against the edge model of tools/figures/q0115.py, tb.sv's want strings against the same model
(tb.sv runs the page's SystemVerilog on Verilator), the copies in tb.sv against the page, and
the page's cocotb benches run on Verilator: as found (six mismatches, the same lines as the
SystemVerilog), fixed (none), each with the driver started first and with the monitor in
ReadOnly(), plus a probe of what cocotb 2.1 shows right after RisingEdge and in ReadOnly()."""

import ast
import inspect
import json
import re
import sys

import pytest

from extract_code import ROOT, question_path

sys.path[:0] = [str(ROOT / "tools" / "figures"), str(ROOT / "tests" / "0115")]
import q0115  # noqa: E402
import variants  # noqa: E402

TB = (ROOT / "tests" / "0115" / "tb.sv").read_text(encoding="utf-8")


def norm(text):
    """Text as read: no RLM, a no-break space as a space, every run of white space one space."""
    return re.sub(r"\s+", " ", text.replace("‏", "").replace(" ", " "))


PAGE = norm(question_path(115).read_text(encoding="utf-8"))


def on_page(*phrases):
    for p in phrases:
        assert norm(p) in PAGE, p


def he(ks):
    """A Hebrew list of numbers: "2, 3 ו-5"."""
    ks = [str(k) for k in ks]
    return ks[0] if len(ks) == 1 else f"{', '.join(ks[:-1])} ו-{ks[-1]}"


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(115)


# --- the stimulus and the model -------------------------------------------------------------

def test_stimulus_is_the_pages():
    sv = variants.page_sv()
    for name in ("race_tb", "race_tb_cb"):
        v = re.search(r"bit\s+V\[N\] = '\{([^}]*)\};", sv[name])[1]
        d = re.search(r"logic \[7:0\] D\[N\] = '\{([^}]*)\};", sv[name])[1]
        assert [int(x) for x in v.split(",")] == q0115.V and [int(x) for x in d.split(",")] == q0115.D
        assert re.search(r"localparam int N = (\d+);", sv[name])[1] == str(len(q0115.V))
    for code in variants.page_py().values():
        stim = ast.literal_eval(re.search(r"^STIM = (\[.*\])", code, re.M)[1])
        assert stim == list(zip(q0115.V, q0115.D))


def test_model_as_found():
    r = q0115.run()
    bad = [k for k, _, _ in r["mismatches"]]
    assert bad == [2, 3, 5, 7, 8, 10]
    clean = [k for k in range(1, q0115.CYCLES + 1) if k not in bad]
    assert clean == [1, 4, 6, 9]
    on_page(f"השגיאות נופלות בדיוק על המחזורים {he(bad)}, ולמה לא על {he(clean)}",
            f"מדווחות על אותן שש שגיאות")
    assert len(bad) == 6
    # an error at edge k exactly when at edge k - 1 the monitor read a row the DUT did not take
    edges = r["edges"]
    for k in range(2, q0115.EDGES + 1):
        e = edges[k - 2]
        assert (k in bad) == (q0115.plus1(e["read"]) != q0115.plus1(e["took"]) and (e["read"][0] or e["took"][0]))
    # before the clean cycles 4, 6 and 9 the two rows are the same: 9 after 9, low after low, 6 after 6
    assert [(q0115.row(k - 3), q0115.row(k - 2)) for k in (4, 6, 9)] == [((1, 9), (1, 9)), ((0, 9), (0, 9)), ((1, 6), (1, 6))]
    on_page("9 אחרי 9, `in_valid` נמוך אחרי נמוך, 6 אחרי 6")


def test_the_edge_of_cycle_2():
    e2, e3 = q0115.run()["edges"][1], q0115.run()["edges"][2]
    assert (e2["read"], e2["took"]) == ((1, 5), (1, 9))
    assert (e3["exp"], e3["got"]) == ((1, 6), (1, 10))
    on_page("5 לפני שה-driver כותב, ו-9 אחרי",
            "ולכן הוא קורא 5, ה-driver כותב 9, וה-DUT לוקח 9",
            "מצפה ל-6 בקצה הבא, ומקבל 10")
    fix = q0115.run("fixed")["edges"][1]
    assert fix["read"] == fix["took"] == (1, 5)


def test_queue_scoreboard_sees_the_same_sequence():
    r = q0115.run()
    seen = [q0115.plus1(e["read"])[1] for e in r["edges"] if e["read"][0]]
    out = [e["wave_out"][1] for e in r["edges"] if e["wave_out"][0]]
    assert seen == out == [6, 10, 10, 3, 7, 7]
    on_page("רואים את אותו רצף, 6, 10, 10, 3, 7, 7")


def test_log_on_page():
    on_page(*q0115.log_lines())


# --- tb.sv: the want strings, the copies ---------------------------------------------------

BENCHES = ["found", "swap", "fixed", "fixed", "after", "fixed", "fixed", "found"]   # the order of tb's WANT


def test_testbench_want_strings():
    body = re.search(r"string WANT\[8\] = '\{(.*?)\};", TB, re.S)[1]
    want = re.findall(r'"([^"]*)"', body)
    assert want == [" ".join(map(str, q0115.mismatch_cycles(v))) for v in BENCHES]
    assert re.search(r'string WANT_WAVE_BUG = "([^"]*)";', TB)[1] == q0115.wave_string("found")
    assert re.search(r'string WANT_WAVE_FIX = "([^"]*)";', TB)[1] == q0115.wave_string("fixed")
    assert len(q0115.run()["edges"]) == 12 == len(q0115.wave_string().split())


def test_testbench_copies_are_the_page():
    assert variants.tb_copies() == variants.copies_block(), "run: python tests/0115/variants.py --write"
    for name in variants.sv_variants():
        assert re.search(rf"^\s*{name}\s+\w+ \(\);", TB, re.M), name


def test_versions_table_rows():
    """Every row of the table of versions is a bench that the tests run."""
    views = [v for *_, v in q0115.VERSIONS]
    sv = dict(zip(["found", "swap", "cb_mon", "negmon", "cb", "nba", "neg"], views[:7]))
    assert sv == {"found": "found", "swap": "swap", "cb_mon": "found", "negmon": "after", "cb": "fixed",
                  "nba": "fixed", "neg": "fixed"}
    assert views[7:] == [PY_VIEWS[k] for k in ("bug", "bug_swap", "bug_ro", "fix", "fix_ro")]


# --- cocotb: the page's Python on Verilator ---------------------------------------------------

PY_VIEWS = {"bug": "found", "bug_swap": "swap", "bug_ro": "after", "fix": "fixed", "fix_swap": "fixed", "fix_ro": "fixed_after"}

PROBE = '''

@cocotb.test()
async def probe(dut):
    """What a coroutine reads right after RisingEdge and in ReadOnly(), after a plain write and
    after an Immediate one (test only)."""
    import json

    from cocotb.handle import Immediate
    from cocotb.triggers import ReadOnly

    facts = {}
    dut.in_valid.value = 1
    dut.in_data.value = 10
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start(start_high=False))
    await RisingEdge(dut.clk)                       # edge 1: the DUT takes 10
    dut.in_data.value = 20
    facts["plain_read_back"] = int(dut.in_data.value)
    await ReadOnly()
    facts["edge1_readonly_out"] = int(dut.out_data.value)
    await RisingEdge(dut.clk)                       # edge 2: the DUT takes 20
    facts["edge2_out"] = int(dut.out_data.value)
    facts["edge2_in"] = int(dut.in_data.value)
    await ReadOnly()
    facts["edge2_readonly_out"] = int(dut.out_data.value)
    await RisingEdge(dut.clk)                       # edge 3: an Immediate write
    dut.in_data.value = Immediate(30)
    facts["immediate_read_back"] = int(dut.in_data.value)
    await ReadOnly()
    facts["edge3_readonly_out"] = int(dut.out_data.value)
    dut._log.info("PROBE " + json.dumps(facts))
'''


def cocotb_run(code, tests=None):
    from page_tests import run_cocotb

    dut = variants.pick(115, "systemverilog", "module add1 (")
    return run_cocotb("q0115", code, {"add1.sv": dut}, "add1", tests=tests)


@pytest.fixture(scope="module")
def py_runs():
    out = {}
    for name, code in variants.py_variants().items():
        results, log = cocotb_run(code, ["race_tb"])
        lines = re.findall(r"INFO +\S+ +(cycle \d+: expected \S+, got \S+)", log)
        out[name] = (results, lines, log)
    return out


def test_cocotb_benches(py_runs):
    for name, view in PY_VIEWS.items():
        results, lines, log = py_runs[name]
        want = q0115.log_lines(view)[:-1]
        assert results == {"race_tb": not want}, (name, log[-2000:])
        assert lines == want, name
    # the page's log is the cocotb run's, word for word, and the SystemVerilog's (tb.sv)
    assert py_runs["bug"][1] == q0115.log_lines()[:-1]
    assert "AssertionError: 6 mismatches" in py_runs["bug"][2]


def test_cocotb_probe():
    results, log = cocotb_run(variants.page_py()["fix"] + PROBE, ["probe"])
    assert results == {"probe": True}, log[-2000:]
    facts = json.loads(re.search(r"PROBE (\{.*\})", log)[1])
    assert facts == {
        "plain_read_back": 10,          # a plain write is not visible in the same step
        "edge1_readonly_out": 11,       # and the DUT took the old 10 at that edge
        "edge2_out": 11,                # right after RisingEdge: the output from before the edge
        "edge2_in": 20,                 # and the input the DUT takes at this edge
        "edge2_readonly_out": 21,       # in ReadOnly(): after the edge's update
        "immediate_read_back": 30,      # Immediate is visible at once
        "edge3_readonly_out": 31,       # and the DUT takes it at the same edge
    }


def test_cocotb_queues_plain_writes():
    """The page names the function of cocotb 2.1 that queues a plain write for ReadWrite."""
    pytest.importorskip("cocotb")
    import cocotb
    import cocotb.handle as h

    assert cocotb.__version__ == "2.1.0"
    src = inspect.getsource(h)
    assert "def _schedule_write(" in src and "Queue write for the beginning of the next ReadWrite phase" in src
    assert "non-deterministic" in h.Immediate.__doc__
    on_page("`_schedule_write` ב-`cocotb/handle.py`")
