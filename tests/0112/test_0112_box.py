"""Question 0112: the box's model (explorer/factory.js) under Node against the reference,
tools/figures/q0112.py (whose build test_0112.py checks against pyuvm runs): the glob of
an instance path against Python's fnmatch on random patterns, why() on every component, and
the whole build (the class of every component, the override that matched and the reason a
path did not, the log lines) for every combination of create and new, both kinds of
override, every time, and the page's paths with random ones."""

import fnmatch
import itertools
import json
import random
import sys

from extract_code import ROOT
from page_tests import explorer_require, node_json

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0112  # noqa: E402

RNG = random.Random(112)
ALPHABET = "ab.*?_1"
PAIRS = [("".join(RNG.choice(ALPHABET) for _ in range(RNG.randint(0, 7))),
          "".join(RNG.choice("ab._1") for _ in range(RNG.randint(0, 7)))) for _ in range(3000)]
PARTS = ["uvm_test_top", "env", "agt0", "agt1", "agt*", "agt?", "drv", "seqr", "*", "?rv", "uvm_*", "agt[01]"]
PATHS = sorted({p for p, _ in q0112.ROWS} | {"*", "drv", "agt1.drv", "*.drv", "*agt1*", "uvm_test_top.env.agt1*",
                                              "uvm_test_top.env.agt2.drv", "Uvm_test_top.env.agt1.drv"}
               | {".".join(RNG.choice(PARTS) for _ in range(RNG.randint(1, 5))) for _ in range(150)})
PATHS = [p for p in PATHS if "[" not in p]      # the box takes letters, digits, _ . * ? only
HOWS = [dict(zip(q0112.LINES, c)) for c in itertools.product(("create", "new"), repeat=len(q0112.LINES))]
CASES = ([(h, "type", "", w) for h in HOWS for w in q0112.TIMES] + [(h, "none", "", "build") for h in HOWS]
         + [(h, "inst", p, w) for h in (HOWS[0], HOWS[-1], dict(zip(q0112.LINES, ["new"] * 4 + ["create"])))
            for p in PATHS for w in q0112.TIMES])


def test_glob_is_fnmatch():
    got = node_json(f"const m = {explorer_require()}; console.log(JSON.stringify("
                    f"{json.dumps(PAIRS)}.map(([p, n]) => m.foMatch(n, p))));")
    assert got == [fnmatch.fnmatchcase(n, p) for p, n in PAIRS]


def test_why_on_every_component():
    names = q0112.NAMES[1:]
    got = node_json(f"const m = {explorer_require()}; const names = {json.dumps(names)};"
                    f"console.log(JSON.stringify({json.dumps(PATHS)}.map((p) => names.map((n) => m.foWhy(n, p)))));")
    assert got == [[list(q0112.why(n, p)) for n in names] for p in PATHS]


def test_build_equals_reference():
    # sent compactly (the script is a command-line argument): indexes into HOWS and PATHS
    hows = [[h[line] for line in q0112.LINES] for h in HOWS]
    cases = [[HOWS.index(h), mode, PATHS.index(p) if p else -1, w] for h, mode, p, w in CASES]
    got = node_json(f"""const m = {explorer_require()};
const lines = {json.dumps(list(q0112.LINES))}, hows = {json.dumps(hows)}, paths = {json.dumps(PATHS)};
console.log(JSON.stringify({json.dumps(cases)}.map(([h, mode, p, w]) => {{
  const how = Object.fromEntries(lines.map((l, i) => [l, hows[h][i]]));
  const s = mode === "inst" ? m.foBuild(how, mode, paths[p], w) : m.foBuild(how, mode, "", w);
  return [s, m.foLog(s)];
}})));""")
    assert len(got) == len(CASES)
    for (how, mode, path, when), (steps, log) in zip(CASES, got):
        ref = q0112.factory_build(how, mode, path, when)
        assert steps == json.loads(json.dumps(ref)), (how, mode, path, when)
        assert log == q0112.log_lines([s["cls"] for s in ref if s["full"] in q0112.DRIVERS])


def test_box_constants():
    got = node_json(f"const m = {explorer_require()}; console.log(JSON.stringify(m.FO));")
    assert got["TREE"] == [list(t) for t in q0112.TREE] and got["LINES"] == list(q0112.LINES)
    assert got["TIMES"] == list(q0112.TIMES) and got["DRIVERS"] == q0112.DRIVERS and got["ITEMS"] == q0112.ITEMS
