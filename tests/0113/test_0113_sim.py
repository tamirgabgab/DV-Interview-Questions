"""Question 0113: the page's pyuvm testbench on Verilator against the timing model of
tools/figures/q0113.py: every test's end time, the scoreboard's lines (what the page's logs
show), the drain times of part b's table, the run that never ends (the first follow-up), its timeout, and
the traps (a late raise, a sequence started in the background, the objection counted)."""

import sys

import pytest

from extract_code import ROOT

sys.path[:0] = [str(ROOT / "tests" / "0113"), str(ROOT / "tools" / "figures")]
import q0113 as q  # noqa: E402
import sim0113 as sim  # noqa: E402


def lines_of(r):
    return [(lvl, who, msg) for _, lvl, who, msg in r]


def check_run(module, test, model):
    passed, log = sim.run(module, test)
    assert passed, log[-3000:]
    sb = sim.scoreboard(log)
    assert lines_of(sb) == q.sb_lines(model)
    assert {t for t, *_ in sb} == {model["end"]} and sim.end_time(log) == model["end"]
    return log


def test_smoke_ends_at_time_0_and_passes_on_nothing():
    log = check_run(sim.page("smoke"), "smoke", q.run("smoke"))
    assert "You did not call self.raise_objection() in any run_phase" in log      # pyuvm warns


def test_objection_runs_until_the_last_item_is_taken():
    model = q.run("objection")
    assert model == {"end": 95, "sent": 8, "compared": 4, "missing": 4, "passed": False}
    log = check_run(sim.page("smoke", "objection"), "objection", model)
    assert "You did not call" not in log


@pytest.mark.parametrize("drain", q.DRAINS)
def test_drain_times(drain):
    module = sim.page("smoke", "objection", "drain")
    if drain == 0:          # cocotb has no Timer(0): no drain is ObjectionTest
        assert q.run("drain", 0) == q.run("objection")
        check_run(module, "objection", q.run("objection"))
        return
    if drain != q.DRAIN_NS:
        module += f"\n\nDRAIN_NS = {drain}\n"
    check_run(module, "drain", q.run("drain", drain))


def test_drain_of_the_page_checks_every_item():
    assert q.run("drain") == {"end": 135, "sent": 8, "compared": 8, "missing": 0, "passed": True}
    assert q.min_drain() == 35
    assert [q.run("drain", d)["passed"] for d in q.DRAINS] == [d > q.min_drain() for d in q.DRAINS]


def test_the_colleagues_monitor_never_ends_and_the_timeout_names_it():
    passed, log = sim.run(sim.page("smoke", "objection", "drain", "colleague", "timeout"), "drain")
    assert not passed                                              # SimTimeoutError fails the test
    assert sim.end_time(log) == q.LIMIT_US * 1000
    assert sim.scoreboard(log) == []                               # check_phase never ran
    crit = [r for r in sim.records(log) if r["lvl"] == "CRITICAL"]
    assert len(crit) == 1 and crit[0]["src"] == q.TIMEOUT_SRC
    assert crit[0]["msg"] == q.timeout_lines()[0][2]
    tail = log[log.index(crit[0]["msg"]):].splitlines()[1:4]
    assert [l.strip() for l in tail[:1]] == ["Active objections:"]
    assert tail[1].strip().startswith(q.timeout_lines()[2][2].strip() + ", raised at ")
    assert log.count("raised by ") == 1                            # one objection left: mon_out's


def test_the_timeout_changes_nothing_in_a_run_that_ends():
    check_run(sim.page("smoke", "objection", "drain", "timeout"), "drain", q.run("drain"))


# --- the traps ---------------------------------------------------------------------------

EXTRA_MODULE = sim.page("smoke", "objection", "drain", "timeout") + sim.EXTRA


def trap(test):
    passed, log = sim.run(EXTRA_MODULE, test)
    assert passed, log[-3000:]
    (rep,) = sim.reports(log)
    return rep, log


def test_late_raise_is_too_late():
    rep, log = trap("late")
    assert rep == {"test": "LateTest", "done": True, "end": 0.0, "count": 0}
    assert sim.scoreboard(log)[0][3] == q.sb_lines(q.run("smoke"))[0][2]


def test_sequence_in_the_background_ends_at_0_without_a_warning():
    rep, log = trap("fork")
    assert rep == {"test": "ForkTest", "done": True, "end": 0.0, "count": 0}
    assert sim.scoreboard(log)[0][3] == q.sb_lines(q.run("smoke"))[0][2]
    assert "You did not call" not in log


def test_two_raises_one_drop_never_ends():
    rep, _ = trap("twice")
    assert rep == {"test": "TwiceTest", "done": False, "end": 2000.0, "count": 1}


def test_drop_without_raise_warns_and_stays_at_0():
    rep, log = trap("drop_only")
    assert rep == {"test": "DropOnlyTest", "done": True, "end": 0.0, "count": 0}
    assert "Dropped objection for 'uvm_test_top' with no matching raise" in log
