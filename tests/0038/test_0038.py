"""Question 0038: the page's reference model (check_handshake, as published) on the page
traces (one good transaction, three violations), on edge cases, and against a second,
independent formulation on random traffic."""

import random

from extract_code import load_python

check_handshake = load_python(38)["check_handshake"]


def wave(req: str, ack: str):
    return [int(c) for c in req], [int(c) for c in ack]


def only(fails, **expected):
    return {k: v for k, v in fails.items() if v} == expected


def test_page_traces():
    # cycle:                0 1 2 3 4 5 6 7
    assert only(check_handshake(*wave("01110000", "00010000")))                 # good
    assert only(check_handshake(*wave("01111100", "00000100")), late=[4])      # late ack (cycle 5)
    assert only(check_handshake(*wave("01100000", "00000000")), hold=[3], late=[4])   # req dropped
    assert only(check_handshake(*wave("00000000", "00100000")), orphan=[2])    # orphan ack
    assert only(check_handshake(*wave("01111100", "00010000")), drop=[4], hold=[6])   # req held after ack, then dropped without one


def test_window_and_edges():
    assert only(check_handshake(*wave("0110000", "0010000")))                   # ack after 1
    assert only(check_handshake(*wave("0111100", "0000100")))                   # ack after 3: still in time
    assert only(check_handshake(*wave("0111110", "0000010")), late=[4])        # ack after 4
    assert only(check_handshake(*wave("0111", "0000")))                         # window cut by the end: not counted
    assert only(check_handshake(*wave("1110", "0010")))                         # req high at cycle 0 is a rise
    assert only(check_handshake(*wave("011", "001"), max_wait=1))               # a shorter window
    assert only(check_handshake(*wave("0110", "0000"), max_wait=1), hold=[3], late=[2])


def independent(req, ack, max_wait=3):
    """A second formulation: walk the transactions as a state machine."""
    fails = {"hold": [], "late": [], "orphan": [], "drop": []}
    n = len(req)
    for t in range(n):
        if ack[t] and not req[t]:
            fails["orphan"].append(t)
        if t and ack[t - 1] and req[t]:
            fails["drop"].append(t)
        if t and req[t - 1] and not ack[t - 1] and not req[t]:
            fails["hold"].append(t)
        if req[t] and (t == 0 or not req[t - 1]) and t + max_wait < n and not any(ack[t + 1:t + 1 + max_wait]):
            fails["late"].append(t + max_wait)
    return fails


def test_random_against_independent_model():
    rng = random.Random(38)
    for _ in range(200):
        n = rng.randint(5, 40)
        req = [rng.random() < 0.6 for _ in range(n)]
        ack = [rng.random() < 0.3 for _ in range(n)]
        req, ack = [int(v) for v in req], [int(v) for v in ack]
        assert check_handshake(req, ack) == independent(req, ack)


def test_explorer_matches_page_model():
    """The handshake explorer: the page's four traces expanded from their WaveDrom strings,
    and random traffic, against check_handshake (max_wait 3 and 2)."""
    import json

    from page_tests import explorer_require, node_json

    rng = random.Random(38)
    cases = []
    for key, (r, a) in {"ok": ("01..0...", "0..10..."), "late": ("01....0.", "0....10."),
                        "drop": ("01.0....", "0......."), "orphan": ("0.......", "0.10....")}.items():
        cases.append((key, r, a))
    got = node_json(f"""
      const m = {explorer_require()};
      const presets = {json.dumps([[k, r, a] for k, r, a in cases])}.map(([k, r, a]) =>
        [m.hsWave(m.HS_PRESETS[k][0], 12), m.hsWave(m.HS_PRESETS[k][1], 12), m.hsCheck(m.hsWave(r, 12), m.hsWave(a, 12), 3)]);
      const rnd = (() => {{ let x = 38; return () => {{ x |= 0; x = (x + 0x6D2B79F5) | 0; let t = Math.imul(x ^ (x >>> 15), 1 | x); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }}; }})();
      const random = [];
      for (let c = 0; c < 400; c++) {{
        const n = 8 + Math.floor(rnd() * 9), req = [], ack = [];
        for (let i = 0; i < n; i++) {{ req.push(rnd() < 0.6 ? 1 : 0); ack.push(rnd() < 0.3 ? 1 : 0); }}
        random.push([req, ack, m.hsCheck(req, ack, 3), m.hsCheck(req, ack, 2)]);
      }}
      console.log(JSON.stringify({{ presets, random }}));""")
    expected = {"ok": {}, "late": {"late": [4]}, "drop": {"hold": [3], "late": [4]}, "orphan": {"orphan": [2]}}
    for (key, r, a), (req, ack, fails) in zip(cases, got["presets"]):
        exp = [int(c) if c != "." else None for c in r]
        assert req[:8] == [v if v is not None else req[i - 1] for i, v in enumerate(exp)]
        assert fails == check_handshake(req, ack, 3) and only(fails, **expected[key]), key
    for req, ack, f3, f2 in got["random"]:
        assert f3 == check_handshake(req, ack, 3)
        assert f2 == check_handshake(req, ack, 2)


def test_explorer_attempt_lanes():
    """The attempt box of part a (J296): every property starts one attempt per cycle; it is
    vacuous exactly where its antecedent does not match, its fails end at the cycles the
    page's check_handshake reports, a pass of rule 2 ends at the first ack of its window,
    and a window cut by the end of the trace stays open. On the page's four traces and on
    random ones."""
    import json
    import random

    from page_tests import explorer_require, node_json

    rng = random.Random(38)
    traces = [[[rng.randint(0, 1) for _ in range(12)] for _ in range(2)] for _ in range(300)]
    got = node_json(f"""
      const m = {explorer_require()};
      const pre = Object.keys(m.HS_PRESETS).map((k) => [m.hsWave(m.HS_PRESETS[k][0], 12), m.hsWave(m.HS_PRESETS[k][1], 12)]);
      const all = pre.concat({json.dumps(traces)});
      console.log(JSON.stringify(all.map(([req, ack]) => ({{ req, ack, att: m.hsAttempts(req, ack, 3) }}))));""")
    for r in got:
        req, ack, att = r["req"], r["ack"], r["att"]
        n = len(req)
        fails = check_handshake(req, ack, 3)
        ante = {
            "hold": lambda t: req[t] and not ack[t],
            "late": lambda t: req[t] and not (req[t - 1] if t else 0),
            "orphan": lambda t: ack[t],
            "drop": lambda t: ack[t],
        }
        for key in ("hold", "late", "orphan", "drop"):
            a = att[key]
            assert [x["t"] for x in a] == list(range(n))
            assert all((x["status"] == "vacuous") == (not ante[key](x["t"])) for x in a)
            assert sorted(x["end"] for x in a if x["status"] == "fail") == fails[key]
            for x in a:
                if key == "late" and x["status"] == "pass":
                    assert ack[x["end"]] and not any(ack[x["t"] + 1:x["end"]]) and x["end"] <= x["t"] + 3
                if x["status"] == "open":
                    assert x["end"] == n - 1
    assert [x["status"] for x in got[1]["att"]["late"] if x["status"] != "vacuous"] == ["fail"]
