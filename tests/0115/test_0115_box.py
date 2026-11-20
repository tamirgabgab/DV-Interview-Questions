"""Question 0115: the box's model (explorer/edgerace.js) under Node against the page's model
(tools/figures/q0115.py), which tb.sv and the cocotb runs check against Verilator: every
choice of the box gives the same view and the same edges and mismatches; the events of every
edge happen in the order of the regions, and what each one reads is what the signals hold
at that moment (the values the events themselves wrote), and it is what the model says the
monitor and the DUT read."""

import json
import sys

from extract_code import ROOT
from page_tests import explorer_require, node_json

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0115  # noqa: E402

CHOICES = [(lang, d, m, o) for lang in ("sv", "py") for d in q0115.DRIVERS[lang]
           for m in q0115.MONITORS[lang] for o in q0115.ORDERS[lang]]


def js():
    script = f"""
const m = {explorer_require()};
const out = [];
for (const c of {json.dumps(CHOICES)}) {{
  const view = m.erView(...c), steps = m.erSteps(...c);
  out.push({{ view, edges: steps.run.edges, mismatches: steps.run.mismatches, steps: steps.steps }});
}}
console.log(JSON.stringify({{ out, ER: m.ER, D: m.ER_DRIVERS, M: m.ER_MONITORS, O: m.ER_ORDERS, VER: m.ER_VERILATOR, R: m.ER_REGIONS }}));
"""
    return node_json(script)


def test_box_constants():
    got = js()
    assert got["ER"] == {"V": q0115.V, "D": q0115.D, "EDGES": q0115.EDGES, "CYCLES": q0115.CYCLES}
    assert (got["D"], got["M"], got["O"], got["VER"]) == (q0115.DRIVERS, q0115.MONITORS, q0115.ORDERS, q0115.VERILATOR_ORDERS)
    assert len(CHOICES) == 64 + 12


def test_box_model_equals_page_model():
    got = js()["out"]
    for c, j in zip(CHOICES, got):
        view = q0115.view_of(*c)
        assert tuple(j["view"]) == view, c
        r = q0115.run(view)
        assert [[k, list(e), list(g)] for k, e, g in r["mismatches"]] == j["mismatches"], c
        for e, je in zip(r["edges"], j["edges"]):
            for key in ("read", "took", "exp", "got"):
                assert list(e[key]) == je[key], (c, e["k"], key)
            assert e["bad"] == je["bad"], (c, e["k"])


def test_box_events():
    """Per edge: one read of the monitor and one of the DUT, in the order of the regions;
    what they read is what the signals hold then, and what the model says; the verdict is
    the model's; the output is updated once, to what the DUT took plus 1."""
    got = js()
    for c, j in zip(CHOICES, got["out"]):
        lang = c[0]
        r = q0115.run(q0115.view_of(*c))
        steps = j["steps"]
        assert [e["k"] for e in steps] == sorted(e["k"] for e in steps), c
        inp, out = [0, 0], [0, 0]
        for k in range(1, q0115.CYCLES + 1):
            evs = [e for e in steps if e["k"] == k]
            assert [e["reg"] for e in evs] == sorted(e["reg"] for e in evs), (c, k)
            assert all(0 <= e["reg"] < len(got["R"][lang]) for e in evs)
            edge = r["edges"][k - 1]
            reads = [e for e in evs if e["act"] == "read"]
            takes = [e for e in evs if e["act"] == "take"]
            updates = [e for e in evs if e["act"] == "update"]
            writes = [e for e in evs if e["act"] == "write"]
            assert len(reads) == len(takes) == len(updates) == len(writes) == 1, (c, k)
            assert writes[0]["val"] == list(q0115.row(k - 1)), (c, k)
            for e in evs:
                if e["act"] == "read":
                    assert e["val"] == inp and e["out"] == out, (c, k, "the monitor reads what is there")
                    assert (e["val"], e["out"], e["exp"], e["bad"]) == (list(edge["read"]), list(edge["got"]), list(edge["exp"]), edge["bad"]), (c, k)
                if e["act"] == "take":
                    assert e["val"] == inp == list(edge["took"]), (c, k, "the DUT reads what is there")
                if e["act"] == "write":
                    inp = e["val"]
                if e["act"] == "update":
                    assert e["val"] == list(q0115.plus1(edge["took"])), (c, k)
                    out = e["val"]
                assert e["in"] == inp and e["outNow"] == out, (c, k)
            # the DUT's update comes after its read; a sampling at Preponed before everything
            assert evs.index(takes[0]) < evs.index(updates[0]), (c, k)
