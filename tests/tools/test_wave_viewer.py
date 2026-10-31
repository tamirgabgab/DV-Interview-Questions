"""The waveform viewer's log (docs/javascripts/wave-viewer.js): the changes it writes from a
```wavedrom source, run under Node, against expectations read off the diagrams by hand;
and every diagram on the site parses and has something to tell."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from page_tests import node_json  # noqa: E402

LIB = json.dumps(str(ROOT / "docs" / "javascripts" / "wave-viewer.js"))
BLOCK = re.compile(r"```wavedrom\n(.*?)```", re.S)


def log(source: str) -> list[str]:
    """The viewer's log lines for a source, as "t: item, item"."""
    return node_json(f"const W = require({LIB}); const src = W.parse({json.dumps(source)});"
                     "process.stdout.write(JSON.stringify(src ? W.changes(src).map((e) => W.fmtT(e.t) + ': ' + e.items.join(', ')) : null));")


def blocks(rel: str) -> list[str]:
    return BLOCK.findall((ROOT / "docs" / "questions" / rel).read_text(encoding="utf-8"))


def test_handshake_and_its_cases():
    ok, cases = blocks("junior/0038-sva-handshake.md")
    # the clock and the lane that only numbers the cycles are left out
    assert log(ok) == ["1: req עולה", "3: ack עולה", "4: req יורד, ack יורד"]
    # three cases split by empty rows, named from the head text
    got = log(cases)
    assert got[0] == "1: req (late ack) עולה, req (req dropped) עולה"
    assert got[-1] == "6: req (late ack) יורד, ack (late ack) יורד"


def test_edge_detector():
    (src,) = blocks("student/0001-rising-edge-detector.md")
    assert log(src) == ["2: sig עולה, pulse עולה", "3: sig_q עולה, pulse יורד", "6: sig יורד",
                        "7: sig_q יורד", "8: sig עולה, pulse עולה", "9: sig_q עולה, pulse יורד"]


def test_half_cycles_and_data():
    (src,) = blocks("junior/0035-divide-by-three-fifty-duty.md")
    got = log(src)
    # b is a with a phase of half a cycle; cnt is data; clk_out is a clock by its name
    assert got[:3] == ["1: cnt = 1, a יורד", "1.5: b יורד", "2: cnt = 2"]
    assert not any("clk_out" in line for line in got)


def test_inline_sources():
    assert log('{ signal: [{ name: "v", wave: "0.1x.z", data: [] }] }') == ["2: v עולה", "3: v לא מוגדר (x)", "5: v מנותק (z)"]
    assert log('{ signal: [{ name: "d", wave: "=.==", data: "A B B" }] }') == ["2: d = B"]
    assert log("not a diagram (") is None


def test_every_diagram_on_the_site():
    found = 0
    for page in sorted((ROOT / "docs" / "questions").rglob("*.md")):
        for src in BLOCK.findall(page.read_text(encoding="utf-8")):
            found += 1
            got = log(src)
            assert got, f"{page.name}: the viewer has nothing to tell about a diagram"
    assert found >= 6
