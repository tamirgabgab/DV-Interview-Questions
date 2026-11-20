"""Question 0113: the generated blocks, every number the page states (from the timing model
of tools/figures/q0113.py, which test_0113_sim.py checks against the Verilator runs of the
page's pyuvm code), and the UVM SystemVerilog, which no simulator here runs, checked against
the Python by structure: the page's tabs with tests/0113/env.sv against the page's blocks
with tests/0113/env.py, the same classes and components, the same stimulus and timing, and
the call that is the bug or the fix in the same place."""

import re
import sys

from extract_code import ROOT, blocks, pick, question_path

HERE = ROOT / "tests" / "0113"
sys.path[:0] = [str(HERE), str(ROOT / "tools" / "figures")]
import q0113 as q  # noqa: E402
import sim0113 as sim  # noqa: E402


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(113)


def norm(text):
    """Text as read: no RLM, every run of white space (a no-break space too) one space."""
    return re.sub(r"\s+", " ", text.replace("\u200f", ""))


PAGE = norm(question_path(113).read_text(encoding="utf-8"))
PY = "\n".join([(HERE / "env.py").read_text(), *blocks(113, "python")])
SV = "\n".join([(HERE / "env.sv").read_text(), *blocks(113, "systemverilog")])
DUT = sim.dut()["pipe.sv"]


def on_page(*phrases):
    for p in phrases:
        assert norm(p) in PAGE, p


# --- the numbers -------------------------------------------------------------------------

def test_the_dut_and_the_environment_as_described():
    assert re.search(r"parameter int LAT = (\d+)", DUT)[1] == str(q.LAT) == "4"
    assert "d[0] <= in_data + 8'd1;" in DUT
    assert q.PERIOD == 10 and q.N == 8 and q.RESET_EDGES == 2
    on_page("צינור (pipeline) של ארבעה שלבים", "ארבעה מחזורים אחר כך, והנתון שלו גדל ב-1",
            "השעון 10 ns, והוא מתחיל בנמוך : עליות ב-5, 15, 25 ns",
            "ה-sequence שולחת 8 פריטים", "מחזיק את האיפוס בשתי העליות הראשונות, ואז מוסר פריט בכל מחזור",
            "דוגמים בירידת השעון", "ב-`check_phase`, ונכשל אם יש אי-התאמה או פריט שנכנס ולא יצא")


def test_timing_of_the_items():
    assert [q.rise(k) for k in range(3)] == [5, 15, 25]
    assert [q.taken(i) for i in range(q.N)] == [25 + 10 * i for i in range(q.N)]
    assert [q.seen_in(i) for i in range(q.N)] == [20 + 10 * i for i in range(q.N)]
    assert [q.seen_out(i) for i in range(q.N)] == [60 + 10 * i for i in range(q.N)]
    assert all(q.seen_out(i) - q.taken(i) == 35 for i in range(q.N))
    assert [q.taken(i) + (q.LAT - 1) * q.PERIOD for i in range(q.N)] == [55 + 10 * i for i in range(q.N)]
    on_page("בעליות של 5 ו-15 ns", r"את פריט \( i \) בעלייה של \( 25 + 10i \) ns, ואת האחרון, פריט 7, ב-95 ns",
            r"פריט שנכנס בעלייה של \( t \) נראה ביציאה ב-\( t + 35 \) ns",
            r"ולרביעי שלוש עליות אחר כך, ב-\( 55 + 10i \) ns", r"בירידה הבאה, ב-\( 60 + 10i \) ns",
            r"פריט \( i \) נראה ביציאה ב-\( 60 + 10i \) ns, והאחרון ב-130 ns")


def test_part_a():
    r = q.run("smoke")
    assert (r["end"], r["sent"], r["compared"], r["missing"], r["passed"]) == (0, 0, 0, 0, True)
    assert q.run("objection")["end"] == q.last_taken() == 95 and q.run("objection")["sent"] == q.N == 8
    on_page("‏`0 ns`, ‏`0 compared`. טסט ששולח 8 פריטים", "‏0 נכנסו ו-0 יצאו",
            "הריצה נגמרת עכשיו ב-95 ns, וכל 8 הפריטים נכנסו", "והריצה נגמרת ב-95 ns",
            "`You did not call self.raise_objection() in any run_phase`")


def test_part_b():
    r = q.run("objection")
    assert (r["compared"], r["missing"]) == (4, 4) and r["missing"] == q.LAT
    lost = [i for i in range(q.N) if q.seen_out(i) > q.last_taken()]
    assert lost == [4, 5, 6, 7] and [q.seen_out(i) for i in lost] == [100, 110, 120, 130]
    assert q.min_drain() == 35 and q.DRAIN_NS == 40 == q.LAT * q.PERIOD
    d = q.run("drain")
    assert (d["end"], d["compared"]) == (135, 8)
    assert [i for i in range(q.N) if q.seen_out(i) < q.run("drain", 0)["end"]] == [0, 1, 2, 3]
    on_page("ארבעת הפריטים האחרונים עוד בצינור, ויוצאים ב-100 עד 130 ns",
            "כאן יותר מ-35 ns, ולכן 40 ns", "ב-95 ns, כשהאחרון נכנס, פריטים 4 עד 7 עוד בצינור",
            "ארבעה, בדיוק מספר השלבים של הצינור", "מהורדת ה-objection, ב-95 ns, עד 130 ns, כלומר 35 ns",
            "‏drain של 40 ns, ארבעה מחזורים. הריצה נגמרת ב-135 ns, ו-8 פריטים נבדקים",
            r"הריצה נגמרת ב-\( 95 + D \) ns",
            r"\( 60 + 10i < 95 + D \). עם \( D = 0 \) אלה פריטים 0 עד 3, ועם \( D > 35 \) כל השמונה",
            "ארבעה פריטים שלא הגיעו", r"נגמרת ב-0, ב-95 ns או ב-\( 95 + D \)")


def test_follow_ups():
    assert q.LIMIT_US == 100 and q.HOLDER == "uvm_test_top.env.mon_out"
    on_page("‏timeout של 100 µs", "objection אחד שנשאר, של `uvm_test_top.env.mon_out`",
            "כי הוא 9200 s של זמן סימולציה", "אחרי שתי הרמות והורדה אחת המונה 1")


# --- the SystemVerilog against the Python ---------------------------------------------------

CLASSES = {"Item": "item", "ItemSeq": "item_seq", "Driver": "driver", "InMonitor": "in_monitor",
           "OutMonitor": "out_monitor", "Scoreboard": "scoreboard", "PipeEnv": "pipe_env",
           "SmokeTest": "smoke_test", "ObjectionTest": "objection_test", "DrainTest": "drain_test"}


def test_same_classes_and_components():
    py = set(re.findall(r"^class (\w+)\(", PY, re.M))
    sv = set(re.findall(r"^\s*class (\w+) extends", SV, re.M))
    assert py == set(CLASSES) and sv == set(CLASSES.values())
    for name in ("seqr", "drv", "mon_in", "mon_out", "sb"):
        assert re.search(rf'self\.{name} = \w+\("{name}", self\)', PY), name
        assert re.search(rf'{name}\s*= [\w:# ()]+::type_id::create\("{name}", this\)', SV), name
    for py_conn, sv_conn in (("self.mon_in.ap.connect(self.sb.sent.analysis_export)", "mon_in.ap.connect(sb.sent.analysis_export)"),
                             ("self.mon_out.ap.connect(self.sb.seen.analysis_export)", "mon_out.ap.connect(sb.seen.analysis_export)"),
                             ("self.drv.seq_item_port.connect(self.seqr.seq_item_export)", "drv.seq_item_port.connect(seqr.seq_item_export)")):
        assert py_conn in PY and sv_conn in SV


def test_same_stimulus_and_timing():
    assert f"N = {q.N} " in PY and f"k < {q.N}" in SV
    assert "data=0x10 + k" in PY and "8'h10 + k" in SV
    assert 'Clock(dut.clk, 10, "ns").start(start_high=False)' in PY and q.PERIOD == 10
    assert "logic clk = 0;" in SV and "always #5 clk = ~clk;" in SV
    assert f"ClockCycles(dut.clk, {q.RESET_EDGES})" in PY and f"repeat ({q.RESET_EDGES}) @(posedge vif.clk)" in SV
    assert PY.count("await FallingEdge(cocotb.top.clk)") == 1 and SV.count("@(negedge vif.clk)") == 2   # in, out
    # the scoreboard: data + 1, in order, the missing ones counted, the same two lines
    assert "out != x + 1" in PY and "out != 8'(x + 1)" in SV
    assert "compared, " in PY and "%0d compared, %0d mismatches, %0d missing" in SV
    assert "TEST FAILED" in SV and "TEST PASSED" in SV


def order(text, *calls):
    pos = [text.index(c) for c in calls]
    return pos == sorted(pos)


def test_the_bug_and_the_fix_of_each_part():
    smoke_py, smoke_sv = pick(113, "python", "class SmokeTest"), pick(113, "systemverilog", "class smoke_test")
    assert "objection" not in smoke_py and "objection" not in smoke_sv          # part a: nobody objects
    obj_py, obj_sv = pick(113, "python", "class ObjectionTest"), pick(113, "systemverilog", "class objection_test")
    assert order(obj_py, "self.raise_objection()", ".start(self.env.seqr)", "self.drop_objection()")
    assert order(obj_sv, "phase.raise_objection(this)", "seq.start(env.seqr)", "phase.drop_objection(this)")
    dr_py, dr_sv = pick(113, "python", "class DrainTest"), pick(113, "systemverilog", "class drain_test")
    assert f"DRAIN_NS = {q.DRAIN_NS}" in dr_py and f"set_drain_time(this, {q.DRAIN_NS}ns)" in dr_sv
    assert order(dr_py, "self.raise_objection()", ".start(self.env.seqr)", 'await Timer(DRAIN_NS, "ns")', "self.drop_objection()")
    assert order(dr_sv, "set_drain_time", "phase.raise_objection(this)", "seq.start(env.seqr)", "phase.drop_objection(this)")
    # the first follow-up, in the tests only: the monitor's objection around its endless loop
    col, to = sim.TEST_ONLY["colleague"], sim.TEST_ONLY["timeout"]
    assert order(col, "self.raise_objection()", "await super().run_phase()", "self.drop_objection()")
    in_mon = PY[PY.index("class InMonitor"):PY.index("class OutMonitor")]
    assert "while True:" in in_mon                                              # what super().run_phase() is
    assert f"limit_us={q.LIMIT_US}" in to and "ObjectionHandler()" in to


def test_pyuvm_has_no_drain_time():
    import pyuvm

    src = "".join(p.read_text(encoding="utf-8") for p in __import__("pathlib").Path(pyuvm.__file__).parent.glob("*.py"))
    assert "set_drain_time" not in src and pyuvm.__version__ == "5.0.0"
    on_page("‏pyuvm 5.0.0 לא מממש drain time : אין לו `set_drain_time`")
