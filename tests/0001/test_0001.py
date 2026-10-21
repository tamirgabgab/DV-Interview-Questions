"""Question 0001: the edge detector explorer against a Python replay of the module (sig_q
is the previous cycle's sig and 0 during reset; pulse = sig & ~sig_q, its mirror for a
falling edge, XOR for both) and against the page's own timing diagram."""

import json
import random
import re

from extract_code import question_path

MODES = {
    "rise": lambda s, q: int(s == 1 and q == 0),
    "fall": lambda s, q: int(s == 0 and q == 1),
    "both": lambda s, q: int(s != q),
}


def replay(sig, mode):
    sig_q = [0] + sig[:-1]                      # cycle 0 is the reset cycle
    return sig_q, [MODES[mode](s, q) for s, q in zip(sig, sig_q)]


def wave(text):
    """A WaveDrom wave string of 0, 1 and . as the value per cycle."""
    out = []
    for c in text:
        out.append(out[-1] if c == "." else int(c))
    return out


def test_page_diagram():
    page = question_path(1).read_text(encoding="utf-8")
    rows = dict(re.findall(r'name: "(\w+)",\s*wave: "([01.p]+)"', page))
    sig, sig_q, pulse = wave(rows["sig"]), wave(rows["sig_q"]), wave(rows["pulse"])
    assert replay(sig, "rise") == (sig_q, pulse)
    assert sum(pulse) == 2 and all(w == 1 for w in pulse_widths(pulse))


def pulse_widths(pulse):
    widths, w = [], 0
    for p in pulse + [0]:
        if p:
            w += 1
        elif w:
            widths.append(w)
            w = 0
    return widths


def test_explorer_matches_replay():
    from page_tests import explorer_require, node_json

    rng = random.Random(1)
    cases = [[0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0], [1, 1, 0, 1], [0] * 12, [1] * 12, [0, 1] * 6]
    cases += [[rng.randrange(2) for _ in range(12)] for _ in range(200)]
    for mode in MODES:
        got = node_json(f"""
          const m = {explorer_require()};
          console.log(JSON.stringify({json.dumps(cases)}.map((s) => m.edgeTrace(s, {json.dumps(mode)}))));""")
        for sig, g in zip(cases, got):
            sig_q, pulse = replay(sig, mode)
            assert g["sigQ"] == sig_q and g["pulse"] == pulse, (sig, mode)
            assert g["phantom"] == (pulse[0] == 1)
            edges = sum(MODES[mode](sig[i], sig[i - 1]) for i in range(1, len(sig)))
            assert sum(g["edges"]) == edges
            # one high cycle per edge, plus the phantom pulse of the reset trap
            assert sum(pulse) == edges + g["phantom"]
            if mode != "both":
                assert all(w == 1 for w in pulse_widths(pulse))
