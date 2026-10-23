"""Question 0040: the page's detect_1011 and run_fsm against the generator's brute-force
automaton (the longest suffix that is a prefix) and against a plain "last L bits equal
the pattern" check, Mealy and Moore, on random patterns up to 8 bits; the page's numbers
(two detections in 1011011, four states, the fall-back of S3 on 0 to S2); the WaveDrom
block of the page; the explorer's JavaScript; and the page copies of the generated
blocks."""

import json
import random
import re
import sys

from extract_code import ROOT, load_python, question_path

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0040  # noqa: E402

ns = load_python(40)
NEXT_1011, detect_1011, fsm_table, run_fsm = ns["NEXT_1011"], ns["detect_1011"], ns["fsm_table"], ns["run_fsm"]
NAMES = {"S0": 0, "S1": 1, "S10": 2, "S101": 3}


def bits_of(text):
    return [int(c) for c in text]


def test_page_numbers():
    states, out = detect_1011(bits_of("1011011"))
    assert out == [0, 0, 0, 1, 0, 0, 1]
    assert [NAMES[s] for s in states] == [0, 1, 2, 3, 1, 2, 3]
    assert q0040.run("1011", "1011011") == ([0, 1, 2, 3, 1, 2, 3], [0, 0, 0, 1, 0, 0, 1])
    assert q0040.table("1011") == [[0, 1], [2, 1], [0, 3], [2, 4], [2, 1]] and q0040.rest("1011") == 1
    assert NEXT_1011["S101"] == ("S10", "S1") and NEXT_1011["S10"] == ("S0", "S101")
    # the traps: back to start misses the overlap in 10101011; Moore is one cycle later
    assert q0040.run("1011", "10101011")[1][-1] == 1
    assert q0040.run("1011", "1011011", moore=True)[1] == [0, 0, 0, 0, 1, 0, 0]
    assert len(set(NEXT_1011)) == 4 and len(q0040.table("1011")) == 5


def test_part_a_matches_the_general_machine():
    rng = random.Random(40)
    for _ in range(300):
        bits = [rng.randrange(2) for _ in range(rng.randint(0, 40))]
        states, out = detect_1011(bits)
        g_states, g_out = run_fsm([1, 0, 1, 1], bits)
        assert out == g_out == q0040.brute("1011", "".join(map(str, bits)))
        assert [NAMES[s] for s in states] == g_states


def test_kmp_table_matches_brute_force():
    rng = random.Random(41)
    for L in range(1, 9):
        for _ in range(60):
            pattern = [rng.randrange(2) for _ in range(L)]
            text = "".join(map(str, pattern))
            nxt = fsm_table(pattern)
            assert nxt == q0040.table(text), text
            rest = next(s for s in range(L) if nxt[s] == nxt[L])
            assert rest == q0040.rest(text), text
            bits = [rng.randrange(2) for _ in range(rng.randint(0, 60))]
            for moore in (False, True):
                states, out = run_fsm(pattern, bits, moore)
                assert out == q0040.brute(text, "".join(map(str, bits)), moore), (text, bits, moore)
                assert all(0 <= s <= (L if moore else L - 1) for s in states)


def test_examples_table():
    rows = q0040.patterns_table().splitlines()[2:]
    assert len(rows) == len(q0040.EXAMPLES)
    assert "`1111`" in rows[2] and "S3" in rows[2].split("|")[3]


def test_wavedrom_block():
    page = question_path(40).read_text(encoding="utf-8")
    rows = dict(re.findall(r'name: "(\w+)",\s*wave: "([01.px=]+)"', page))
    data = re.search(r'data: \[([^\]]*)\]', page).group(1)
    names = [s.strip().strip('"') for s in data.split(",")]

    def decode(wave):
        out = []
        for c in wave:
            out.append(out[-1] if c == "." else c)
        return out

    assert rows["state"] == "=" * len(names)                 # one data entry per cycle
    bits = [int(c) for c in decode(rows["din"])[1:]]         # cycle 0 is the reset cycle
    assert bits == bits_of("1011011")
    states, out = detect_1011(bits)
    assert names[1:] == states and names[0] == "S0"
    assert [int(c) for c in decode(rows["found"])[1:]] == out


def test_explorer_matches_the_page_code():
    from page_tests import explorer_require, node_json

    rng = random.Random(42)
    cases = [("1011", "1011011", False), ("1011", "1011011", True), ("0110", "0110110", False), ("1111", "111111", True)]
    cases += [("".join(rng.choice("01") for _ in range(rng.randint(1, 8))), "".join(rng.choice("01") for _ in range(rng.randint(0, 30))), rng.random() < 0.5) for _ in range(80)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([p, s, moore]) => {{
        const pattern = [...p].map(Number), bits = [...s].map(Number);
        const t = m.seqTable(pattern), r = m.seqRun(pattern, bits, moore);
        return [t.nxt, t.rest, r.states, r.out, r.next];
      }})));""")
    for (p, s, moore), (nxt, rest, states, out, nxt_state) in zip(cases, got):
        pattern, bits = bits_of(p), bits_of(s)
        assert nxt == fsm_table(pattern) and rest == q0040.rest(p)
        g_states, g_out = run_fsm(pattern, bits, moore)
        assert states == g_states and out == g_out, (p, s, moore)
        more = run_fsm(pattern, bits + [0], moore)[0]
        assert nxt_state == more[-1]


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(40)


def test_explorer_fallback():
    """The box's build of an edge: for every pattern of up to 6 bits, every state and both
    bits, the longest prefix of the pattern that the text ends with is the KMP table's
    next state (the page's fsm_table for 1011), and the shift is the length difference."""
    from page_tests import explorer_require, node_json

    patterns = [[int(c) for c in format(v, f"0{w}b")] for w in range(1, 7) for v in range(1 << w)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(patterns)}.map((p) => [m.seqTable(p).nxt,
        [...Array(p.length + 1).keys()].map((s) => [0, 1].map((b) => m.seqFallback(p, s, b)))])));""")
    for p, (nxt, fbs) in zip(patterns, got):
        for s, pair in enumerate(fbs):
            for b, fb in enumerate(pair):
                text = p[:s] + [b]
                want = max(k for k in range(min(len(text), len(p)) + 1) if text[len(text) - k:] == p[:k])
                assert fb["text"] == text and fb["target"] == want and fb["shift"] == len(text) - want
                if s < len(p):
                    assert fb["target"] == nxt[s][b], (p, s, b)
