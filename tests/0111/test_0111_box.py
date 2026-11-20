"""Question 0111: the box's model (explorer/falsepass.js) under Node against the page's Python
model (run_bench): every combination of the four fixes, for the seeds the Verilator matrix
runs and 300 more, gives the same rows, errors, counts and items left; the log lines are the
figure generator's."""

import json
import random
import sys

from extract_code import ROOT, load_python
from page_tests import explorer_require, node_json

sys.path.insert(0, str(ROOT / "tools" / "figures"))
sys.path.insert(0, str(ROOT / "tests" / "0111"))
import matrix  # noqa: E402
import q0111  # noqa: E402

COMBOS = [(bp, sva, sb, fx) for bp in (0, 1) for sva in (0, 1) for sb in (0, 1) for fx in (0, 1)]
SEEDS = list(matrix.SEEDS) + random.Random(111).sample(range(1, 65536), 300)
FULL = list(matrix.SEEDS)     # the seeds whose rows are compared cycle by cycle


def js_runs():
    script = f"""
const m = {explorer_require()};
const seeds = {json.dumps(SEEDS)}, full = new Set({json.dumps(FULL)}), combos = {json.dumps(COMBOS)};
const out = [];
for (const s of seeds) for (const c of combos) {{
  const r = m.fpRun(s, ...c);
  out.push({{ errors: r.errors, n_in: r.n_in, n_out: r.n_out, left: r.left, stalls: r.stalls, holds: r.holds,
             checked: r.checked, rows: full.has(s) ? r.rows : null, log: m.fpLog(r), lost: m.fpLost(r) }});
}}
console.log(JSON.stringify(out));
"""
    return node_json(script)


def test_box_model_equals_page_model():
    ns = load_python(111)
    got = js_runs()
    i = 0
    for s in SEEDS:
        for c in COMBOS:
            r, j = ns["run_bench"](s, *c), got[i]
            i += 1
            assert [tuple(e) for e in j["errors"]] == r["errors"], (s, c)
            for key in ("n_in", "n_out", "left", "stalls", "holds", "checked"):
                assert j[key] == r[key], (s, c, key)
            if s in FULL:
                assert j["rows"] == r["rows"], (s, c)
            assert j["log"] == q0111.log_lines(r), (s, c)
            lost = [[w["t"], w["out_data"]] for w in r["rows"]
                    if w["rst_n"] and w["out_valid"] and not w["out_ready"] and w["in_valid"] and w["in_ready"]]
            assert j["lost"] == lost, (s, c)


def test_box_constants_and_messages():
    ns = load_python(111)
    got = node_json(f"const m = {explorer_require()}; console.log(JSON.stringify(m.FP));")
    assert got == {"CYCLES": ns["CYCLES"], "RESET": ns["RESET"], "DRAIN": ns["DRAIN"], "MAX_WAIT": ns["MAX_WAIT"], "SEED": q0111.SEED}
