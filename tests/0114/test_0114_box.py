"""Question 0114: the box's model (explorer/seqarb.js) under Node against the Python reference
(tools/figures/q0114.py's sequencer running the page's traffic() and irq()): every setting of
the box (mode, I's priority, lock or grab, I's start) gives the same items, and every slot the
same queue, lock holders and choice; the general cases of the IEEE 1800.2 tests (a held lock,
a late grab) agree too, and the line of the box has room for the longest run."""

import json
import sys

from extract_code import ROOT
from page_tests import explorer_require, node_json

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0114  # noqa: E402

SETTINGS = [(mode, how, prio, start) for mode in ("FIFO", "STRICT_FIFO") for how in (None, "lock", "grab")
            for prio in (100, 500) for start in (0.5, 1.5, 2.5)]
SAME = ("queue", "locks", "out")      # what the Python snapshots hold


def js(script):
    return node_json(f"const m = {explorer_require()};\n{script}")


def test_box_model_equals_the_python_model():
    got = js(f"""
const settings = {json.dumps(SETTINGS)};
console.log(JSON.stringify(settings.map(([mode, how, prio, start]) => {{
  const r = m.saCase(mode, how, prio, start);
  return {{ out: r.out, snaps: r.snaps, together: m.saTogether(r.out) }};
}})));""")
    for (mode, how, prio, start), j in zip(SETTINGS, got):
        snaps = []
        out = q0114.run_case(mode, snaps, how=how, priority=prio, start=start)
        assert j["out"] == out, (mode, how, prio, start)
        assert [{k: s[k] for k in SAME} for s in j["snaps"]] == snaps, (mode, how, prio, start)
        assert j["together"] == q0114.together(out)


def test_box_model_general_cases():
    # a lock held by another sequence holds back a later lock or grab, and everyone else
    cases = []
    for how in ("lock", "grab"):
        cases.append([("L", [["lock"], ["item", "L0"], ["wait", 2], ["item", "L1"], ["unlock"]], 0, 100),
                      ("G", [[how], ["item", "G0"], ["un" + how]], 0.5, 100),
                      ("A", [["item", f"A{i}"] for i in range(3)], 0, 100)])
    got = js(f"""
const cases = {json.dumps(cases)};
console.log(JSON.stringify(cases.map((c) => m.saRun(c.map(([n, steps, start, p]) => m.saSeq(n, steps, start, p))).out)));""")
    for case, out in zip(cases, got):
        seqs = [q0114.Seq(n, [tuple(s) for s in steps], start, p) for n, steps, start, p in case]
        assert out == q0114.sequencer(seqs)


def test_box_line_has_room_for_every_setting():
    slots = js("console.log(JSON.stringify(m.SA_SLOTS));")
    assert slots == max(len(q0114.run_case(mode, how=how, priority=prio, start=start))
                        for mode, how, prio, start in SETTINGS)
