"""Question 0111: the numbers the page states, recomputed from the page's cycle model
(run_bench; tests/0111/tb.sv runs the same combinations under Verilator), and the generated
blocks."""

import re
import sys

from extract_code import ROOT, load_python, pick, question_path

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0111  # noqa: E402

NS = load_python(111)
RUN = NS["run_bench"]
SEED = 187
PAGE = question_path(111).read_text(encoding="utf-8")


def run(bp=0, sva=0, sb=0, fx=0, seed=SEED):
    return RUN(seed, bp, sva, sb, fx)


def log(r):
    return q0111.log_lines(r)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(111)


def test_statement():
    bench = pick(111, "systemverilog", "module slice_tb")
    # 40 cycles: 2 of reset, 32 of traffic, 6 that drain; the default seed is the page's
    assert NS["CYCLES"] == 40 and NS["RESET"] == 2 and NS["DRAIN"] == 6 and 40 - 2 - 6 == 32
    assert "localparam int CYCLES = 40;" in bench and "rst_n     = cycle >= 2;" in bench and "cycle < CYCLES - 6" in bench
    assert "parameter logic [15:0] SEED         = 187" in bench and "BACKPRESSURE = 0," in bench
    assert "MAX_WAIT = 10;" in pick(111, "systemverilog", "localparam int MAX_WAIT") and NS["MAX_WAIT"] == 10
    # the regression's line, with either DUT
    assert log(run())[-1] == "TEST PASSED: 24 in, 24 out, 0 errors" == log(run(fx=1))[-1]
    assert "`TEST PASSED: 24 in, 24 out, 0 errors`" in PAGE


def test_part_a():
    asis, bp = run(), run(bp=1)
    # backpressure off: out_ready is 1 in every cycle, no item ever waits, the two DUTs run alike
    assert all(w["out_ready"] for w in asis["rows"])
    assert not any(w["out_valid"] and not w["out_ready"] for w in asis["rows"])
    assert asis["rows"] == run(fx=1)["rows"]
    # with the fix: 6 cycles where an item waits, the bug in cycle 11, and still a pass
    waits = [w["t"] for w in bp["rows"] if w["rst_n"] and w["out_valid"] and not w["out_ready"]]
    assert waits == [3, 11, 14, 27, 31, 32] and bp["stalls"] == 6
    w = bp["rows"][11]
    assert (w["out_valid"], w["out_data"], w["out_ready"], w["in_valid"], w["in_ready"], w["in_data"]) == (1, 5, 0, 1, 1, 6)
    assert bp["errors"] == [] and log(bp)[-1] == "TEST PASSED: 21 in, 20 out, 0 errors" and bp["left"] == [5]


def test_part_b():
    ab = run(bp=1, sva=1)
    assert log(ab)[0] == "ERROR at cycle 12: a_hold: out_data changed while out_ready was low"
    assert ab["holds"] == 6 and ab["checked"] == 6 and ab["errors"] == [(12, "a_hold", 5)]
    r = ab["rows"]
    assert (r[11]["out_valid"], r[11]["out_ready"], r[11]["out_data"], r[12]["out_data"]) == (1, 0, 5, 6)
    # as found: rst_n is low in cycles 0 and 1 only, where out_valid is low
    assert [w["t"] for w in r if not w["rst_n"]] == [0, 1] and not any(w["out_valid"] for w in r[:2])
    # the assertion fixed without stalls: c_hold stays 0 and the test fails at the end
    b = run(sva=1)
    assert b["holds"] == 0 and log(b)[0] == "ERROR at cycle 40: c_hold: a_hold never checked anything"


def test_part_c():
    ac = run(bp=1, sb=1)
    assert log(ac)[:2] == ["ERROR at cycle 20: scoreboard: item 5 still waiting after 10 cycles",
                           "ERROR at cycle 40: scoreboard: item 5 never came out"]
    r = run(bp=1)["rows"]
    # item 5 went in at the edge of cycle 10 and was overwritten at the edge of cycle 11; 20 = 10 + 10
    assert (r[10]["in_valid"], r[10]["in_ready"], r[10]["in_data"]) == (1, 1, 5) and r[11]["out_data"] == 5
    assert r[12]["out_data"] == 6 and 5 not in [w["out_data"] for w in r if w["out_valid"] and w["out_ready"]]


def longest_wait(rows):
    """The longest time from the edge an item went in to the edge it went out."""
    went_in, longest = {}, 0
    for w in rows:
        if w["out_valid"] and w["out_ready"]:
            longest = max(longest, w["t"] - went_in.pop(w["out_data"]))
        if w["in_valid"] and w["in_ready"]:
            went_in[w["in_data"]] = w["t"]
    assert not went_in
    return longest


def test_part_c_no_false_alarm_in_any_seed():
    # every seed of the 16-bit LFSR, the fixed DUT: no wait of more than 8 cycles, and the
    # scoreboard's bound and end check never fire (an assertion or cover goal may, see below)
    worst = 0
    for seed in range(1, 65536):
        r = RUN(seed, 1, 0, 1, 1)
        assert r["errors"] == [] or {who for _, who, _ in r["errors"]} == {"c_stall"}, seed
        worst = max(worst, longest_wait(r["rows"]))
    assert worst == 8 and "65,535" in PAGE


def test_part_d():
    r = run(bp=1, sva=1, sb=1)
    assert log(r) == ["ERROR at cycle 12: a_hold: out_data changed while out_ready was low",
                      "ERROR at cycle 20: scoreboard: item 5 still waiting after 10 cycles",
                      "ERROR at cycle 40: scoreboard: item 5 never came out",
                      "TEST FAILED: 21 in, 20 out, 3 errors",
                      "first error: cycle 12: a_hold: out_data changed while out_ready was low"]
    rows = r["rows"]
    w = rows[11]
    assert (w["in_ready"], w["full_q"], w["out_ready"], w["out_ready_q"]) == (1, 1, 0, 1) and rows[10]["out_ready"] == 1
    assert q0111.WINDOW == range(8, 15)
    assert log(run(1, 1, 1, 1))[-1] == "TEST PASSED: 23 in, 23 out, 0 errors"
    # the bug loses an item only in the first cycle of a stall with a new item waiting: cycle 11 of 6
    lost = [w["t"] for w in rows if w["full_q"] and not w["out_ready"] and w["out_ready_q"] and w["in_valid"]]
    assert lost == [11] and r["stalls"] == 6
    # and costs throughput: full, out_ready high, out_ready_q low (cycle 4, for one)
    w = rows[4]
    assert (w["full_q"], w["out_ready"], w["out_ready_q"], w["in_ready"], w["in_valid"]) == (1, 1, 0, 0, 1)
    # out_ready always 1: out_ready_q is 1 in every cycle where the slice is full
    asis = run()["rows"]
    assert all(w["out_ready_q"] for w in asis if w["full_q"]) and min(w["t"] for w in asis if w["full_q"]) == 3
    assert [w["t"] for w in asis if w["out_ready_q"]][0] == 3


def test_follow_ups():
    rows = run(bp=1)["rows"]
    # the cover of the bug's condition: an item waits at the output and a new one at the input
    assert [w["t"] for w in rows if w["rst_n"] and w["out_valid"] and not w["out_ready"] and w["in_valid"]] == [11]
    # an in-order scoreboard: the first mismatch is in cycle 12, item 6 against 5
    queue, first = [], None
    for w in rows:
        if w["rst_n"] and w["out_valid"] and w["out_ready"] and first is None:
            head = queue.pop(0)
            if head != w["out_data"]:
                first = (w["t"], w["out_data"], head)
        if w["rst_n"] and w["in_valid"] and w["in_ready"]:
            queue.append(w["in_data"])
    assert first == (12, 6, 5)


def test_table_rows():
    # the table's claims in the text: c_hold at 40 without stalls, the scoreboard at 20 with 2 errors
    assert run(sva=1, sb=1)["errors"] == [(40, "c_hold", 0)]
    assert run(bp=1, sb=1)["errors"] == [(20, "wait", 5), (40, "missing", 5)]
    assert all(run(bp, sva, sb, 1)["errors"] == [] for bp in (1,) for sva in (0, 1) for sb in (0, 1))
    assert len(re.findall(r"^    \| [—✓] \|", PAGE, re.M)) == 8
