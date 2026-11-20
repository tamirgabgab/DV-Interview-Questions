"""Question 0113: the box's model (explorer/objrun.js) under Node against the timing model of
tools/figures/q0113.py, which test_0113_sim.py checks against the page's pyuvm code on
Verilator: for every switch and drain of the box, the end of the run, the items sent,
compared and missing, the verdict and the lines the run ends with; column by column, what
each monitor samples, the pipeline's stages and the objections held."""

import json
import sys

from extract_code import ROOT
from page_tests import explorer_require, node_json

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0113 as q  # noqa: E402

DRAINS = list(range(0, 61, 10))
CASES = [(raise_, hold, d) for raise_ in (0, 1) for hold in (0, 1) for d in DRAINS]


def js_runs():
    script = f"""
const m = {explorer_require()};
const out = {json.dumps(CASES)}.map(([r, h, d]) => {{
  const run = m.orRun(r, h, d);
  return {{ ...run, log: m.orLog(run), endCol: m.orEndCol(run) }};
}});
console.log(JSON.stringify({{ OR: m.OR, runs: out }}));
"""
    return node_json(script)


GOT = None


def got():
    global GOT
    if GOT is None:
        GOT = js_runs()
    return GOT


def model(raise_, hold, d):
    """The page's tests: no raise is SmokeTest, a raise with no drain ObjectionTest, else DrainTest."""
    if not raise_:
        return q.run("smoke")
    return q.run("objection") if d == 0 else q.run("drain", d)


def test_box_constants():
    c = got()["OR"]
    assert (c["PERIOD"], c["LAT"], c["N"], c["RESET_EDGES"], c["LIMIT_US"]) == (q.PERIOD, q.LAT, q.N, q.RESET_EDGES, q.LIMIT_US)
    assert (c["SB"], c["HOLDER"], c["TIMEOUT_SRC"]) == (q.SB, q.HOLDER, q.TIMEOUT_SRC)
    assert c["DRAIN_MAX"] == DRAINS[-1] and c["COLS"] * q.PERIOD > q.run("drain", DRAINS[-1])["end"]
    assert q.T_MAX <= (c["COLS"] - 1) * q.PERIOD                   # the box shows all the page's timeline


def test_box_runs_equal_the_model():
    for (r, h, d), j in zip(CASES, got()["runs"]):
        if h:       # the monitor never drops: no end, no check_phase, the timeout's lines
            assert j["end"] is None and j["passed"] is None and j["endCol"] is None, (r, h, d)
            assert [tuple(x) for x in j["log"]] == q.timeout_lines(), (r, h, d)
            assert (j["sent"], j["compared"], j["missing"]) == (q.N, q.N, 0)
            continue
        m = model(r, h, d)
        for key in ("end", "sent", "compared", "missing", "passed"):
            assert j[key] == m[key], (r, h, d, key)
        assert [tuple(x) for x in j["log"]] == q.sb_lines(m), (r, h, d)
        assert j["lost"] == [i for i in range(q.N) if q.seen_in(i) < m["end"] <= q.seen_out(i)]
        # the end column: the last falling edge before the end (its sample counts)
        assert j["endCol"] == (-1 if m["end"] == 0 else (m["end"] - 1) // q.PERIOD)


def test_box_columns():
    for (r, h, d), j in zip(CASES, got()["runs"]):
        end = None if h else model(r, h, d)["end"]
        for k, c in enumerate(j["cols"]):
            t = k * q.PERIOD
            assert c["t"] == t
            assert c["in_item"] == next((i for i in range(q.N) if q.seen_in(i) == t), None)
            assert c["out_item"] == next((i for i in range(q.N) if q.seen_out(i) == t), None)
            assert c["stages"] == [next((i for i in range(q.N) if q.taken(i) + q.PERIOD * s <= t < q.taken(i) + q.PERIOD * (s + 1)), None)
                                   for s in range(q.LAT)]
            assert c["rst_n"] == (t > q.rise(q.RESET_EDGES - 1))
            assert c["running"] == (end is None or t < end)
            holders = (["uvm_test_top"] if r and t < q.last_taken() else []) + ([q.HOLDER] if h else [])
            assert c["holders"] == holders
            assert c["drain"] == (not h and r and d > 0 and q.last_taken() < t < end)
            assert c["sent"] == [i for i in range(q.N) if q.seen_in(i) <= t and (end is None or q.seen_in(i) < end)]
            assert c["seen"] == [i for i in range(q.N) if q.seen_out(i) <= t and (end is None or q.seen_out(i) < end)]
        # the out monitor at the falling edge is the 4th stage's item, half a cycle after it was written
        assert [c["out_item"] for c in j["cols"]] == [c["stages"][q.LAT - 1] for c in j["cols"]]
