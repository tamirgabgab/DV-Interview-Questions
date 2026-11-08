"""Question 0034: the page's Python code (bin2gray, gray2bin, fifo_empty, fifo_full, as
published): the conversions are inverse, every step changes one bit (the wrap included),
the page table, and the full / empty rules against the true occupancy, exhaustively. The
boxes' models against the page code; the figures of tools/figures/q0034.py (the waveforms'
edges, the block diagram, the glitch) and its edge-by-edge model of the FIFO's pointer paths,
which the hardware box (grayhw.js) replays."""

from extract_code import load_python

ns = load_python(34)
bin2gray, gray2bin = ns["bin2gray"], ns["gray2bin"]
fifo_empty, fifo_full = ns["fifo_empty"], ns["fifo_full"]


def test_conversions_inverse_and_one_bit_steps():
    for bits in (1, 2, 3, 4, 5, 8):
        size = 1 << bits
        for b in range(size):
            g = bin2gray(b)
            assert gray2bin(g, bits) == b
            assert bin(g ^ bin2gray((b + 1) % size)).count("1") == 1


def test_page_table():
    grays = [bin2gray(b) for b in range(16)]
    assert grays == [0b0000, 0b0001, 0b0011, 0b0010, 0b0110, 0b0111, 0b0101, 0b0100,
                     0b1100, 0b1101, 0b1111, 0b1110, 0b1010, 0b1011, 0b1001, 0b1000]
    changed = [(grays[b] ^ grays[(b + 1) % 16]).bit_length() - 1 for b in range(16)]
    assert changed == [0, 1, 0, 2, 0, 1, 0, 3, 0, 1, 0, 2, 0, 1, 0, 3]
    # the bit that changes is the number of trailing zeros of b + 1
    assert all(c == ((((b + 1) % 16) & -((b + 1) % 16)).bit_length() - 1 if (b + 1) % 16 else 3) for b, c in enumerate(changed))


def test_full_empty_exhaustive():
    for bits in (2, 3, 5, 7):
        size, half = 1 << bits, 1 << (bits - 1)
        for w in range(size):
            for r in range(size):
                occupancy = (w - r) % size
                assert fifo_empty(bin2gray(w), bin2gray(r)) == (occupancy == 0)
                assert fifo_full(bin2gray(w), bin2gray(r), bits) == (occupancy == half)


def test_page_example():
    assert bin2gray(7) == 0b0100 and bin2gray(8) == 0b1100
    assert bin2gray(23) == 0b11100 and bin2gray(7) == 0b00100
    assert fifo_full(bin2gray(23), bin2gray(7), 5) and not fifo_empty(bin2gray(23), bin2gray(7))


def test_explorer_matches_page_code():
    """The Gray explorer: its conversions and flags against the page's functions on every
    5-bit value and every pointer pair; its sampled step b -> b + 1 on every 4-bit value
    and every subset of arrived bits."""
    import itertools
    import json

    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      const conv = [], flags = [], samples = [];
      for (let v = 0; v < 32; v++) conv.push([m.grayOf(v), m.grayToBin(m.grayOf(v), 5)]);
      for (let w = 0; w < 32; w++) for (let r = 0; r < 32; r++) flags.push(m.grayFlags(w, r, 5));
      for (let b = 0; b < 16; b++) for (let s = 0; s < 16; s++) {{
        const arr = {{}}; for (let i = 0; i < 4; i++) arr[i] = (s >> i) & 1;
        samples.push(m.graySample(b, 4, arr, arr));
      }}
      console.log(JSON.stringify({{ conv, flags, samples }}));""")
    for v, (g, back) in enumerate(got["conv"]):
        assert g == bin2gray(v) and back == v and gray2bin(g, 5) == v
    for (w, r), fl in zip(itertools.product(range(32), range(32)), got["flags"]):
        assert fl["empty"] == fifo_empty(bin2gray(w), bin2gray(r))
        assert fl["full"] == fifo_full(bin2gray(w), bin2gray(r), 5)
        assert fl["occupancy"] == (w - r) % 32
    for (b, s), sm in zip(itertools.product(range(16), range(16)), got["samples"]):
        nb = (b + 1) % 16
        changed = [i for i in range(4) if (b ^ nb) >> i & 1]
        assert sm["changedBin"] == changed
        assert sm["changedGray"] == [(bin2gray(b) ^ bin2gray(nb)).bit_length() - 1]
        seen = b
        for i in changed:
            if s >> i & 1:
                seen = (seen & ~(1 << i)) | (nb & (1 << i))
        arrived = [s >> i & 1 for i in changed]
        assert sm["seenBin"] == seen
        assert sm["binValid"] == (seen in (b, nb)) == (all(arrived) or not any(arrived))
        assert sm["seenGray"] in (bin2gray(b), bin2gray(nb)) and sm["seenGrayAsBin"] in (b, nb)
        assert sm["wrongCount"] == 2 ** len(changed) - 2


def test_explorer_widths():
    """The width selects of the two boxes: the sampled step on every value of 3 to 6 bits
    (every subset of arrived bits for the wrap step, where all bits change) against the
    page's conversions, and the flags of a FIFO of 8, 32 and 64 entries (pointers one bit
    wider) on every pointer pair against the page's fifo_empty / fifo_full."""
    import itertools
    import json

    from page_tests import explorer_require, node_json

    sizes = [8, 32, 64]
    got = node_json(f"""
      const m = {explorer_require()};
      const wraps = {{}}, flags = {{}};
      for (const bits of [3, 4, 5, 6]) {{
        const b = (1 << bits) - 1, out = [];
        for (let s = 0; s < (1 << bits); s++) {{ const arr = {{}}; for (let i = 0; i < bits; i++) arr[i] = (s >> i) & 1; out.push(m.graySample(b, bits, arr, arr)); }}
        wraps[bits] = out;
      }}
      for (const size of {json.dumps(sizes)}) {{
        const bits = Math.log2(size) + 1, out = [];
        for (let w = 0; w < 2 * size; w++) for (let r = 0; r < 2 * size; r++) out.push(m.grayFlags(w, r, bits));
        flags[size] = out;
      }}
      console.log(JSON.stringify({{ wraps, flags }}));""")
    for bits in (3, 4, 5, 6):
        b, size = (1 << bits) - 1, 1 << bits
        for s, sm in enumerate(got["wraps"][str(bits)]):
            assert sm["changedBin"] == list(range(bits)) and sm["changedGray"] == [bits - 1]
            seen = sum(((0 if s >> i & 1 else 1) << i) for i in range(bits))   # old bit 1 unless the new 0 arrived
            assert sm["seenBin"] == seen and sm["binValid"] == (s in (0, size - 1))
            assert sm["seenGrayAsBin"] in (b, 0) and sm["wrongCount"] == size - 2
    for size in sizes:
        bits = size.bit_length()                                   # log2(size) + 1
        for (w, r), fl in zip(itertools.product(range(2 * size), range(2 * size)), got["flags"][str(size)]):
            assert fl["empty"] == fifo_empty(bin2gray(w), bin2gray(r)) == ((w - r) % (2 * size) == 0)
            assert fl["full"] == fifo_full(bin2gray(w), bin2gray(r), bits) == ((w - r) % (2 * size) == size)
            assert fl["occupancy"] == (w - r) % (2 * size)


def test_explorer_flag_strip():
    """The timing strip of the FIFO box (X145): one column per write or read that the
    FIFO accepts (a write when full and a read when empty are refused, so a burst stops
    early), the pointers after it and the flags by the page's fifo_full / fifo_empty."""
    import json
    import random

    from page_tests import explorer_require, node_json

    rng = random.Random(34)
    runs = []
    for size in (8, 16, 32, 64):
        ops = []
        for _ in range(60):
            ops += [rng.choice("wr")] * rng.choice([1, 1, 2, size // 2])
        runs.append((size, ops))
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(runs)}.map(([size, ops]) => m.grayFlagsOps(ops, size))));""")
    for (size, ops), cols in zip(runs, got):
        bits, w, r = size.bit_length(), 0, 0
        want = [(None, 0, 0)]
        for op in ops:
            occ = (w - r) % (2 * size)
            if op == "w" and occ < size:
                w = (w + 1) % (2 * size)
                want.append(("w", w, r))
            elif op == "r" and occ > 0:
                r = (r + 1) % (2 * size)
                want.append(("r", w, r))
        assert [(c["op"], c["w"], c["r"]) for c in cols] == want
        for c in cols:
            assert c["wg"] == bin2gray(c["w"]) and c["rg"] == bin2gray(c["r"])
            assert c["full"] == fifo_full(c["wg"], c["rg"], bits) and c["empty"] == fifo_empty(c["wg"], c["rg"])
        assert any(c["full"] for c in cols) and any(c["empty"] for c in cols[1:])


def test_explorer_conversion_steps():
    """The conversion box of part b (J294): forward every Gray bit is the XOR of the bit
    above (0 over the top) and its own, back every binary bit is the bit found before XOR
    its Gray bit, both against the page's bin2gray / gray2bin on every value of 3 to 6
    bits; the counter walk changes one Gray bit per step, the trailing zeros of b + 1, and
    the top bit on the wrap to 0."""
    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      const out = {{}};
      for (const bits of [3, 4, 5, 6]) {{
        const steps = [];
        for (let b = 0; b < (1 << bits); b++) steps.push(m.grayConvertSteps(b, bits));
        out[bits] = {{ steps, walk: m.grayWalk(bits) }};
      }}
      console.log(JSON.stringify(out));""")
    for bits in (3, 4, 5, 6):
        size = 1 << bits
        steps, walk = got[str(bits)]["steps"], got[str(bits)]["walk"]
        for b, r in enumerate(steps):
            g = bin2gray(b)
            assert r["g"] == g and gray2bin(g, bits) == b
            assert [s["i"] for s in r["fwd"]] == [s["i"] for s in r["back"]] == list(range(bits - 1, -1, -1))
            for s in r["fwd"]:
                i = s["i"]
                assert s["bit"] == b >> i & 1 and s["above"] == b >> (i + 1) & 1 and s["g"] == g >> i & 1
            prev = 0
            for s in r["back"]:
                i = s["i"]
                assert s["prev"] == prev and s["g"] == g >> i & 1 and s["b"] == prev ^ s["g"] == b >> i & 1
                prev = s["b"]
        for b, w in enumerate(walk):
            nb = (b + 1) % size
            assert w["g"] == bin2gray(b) and w["grayChanges"] == 1
            assert w["binChanges"] == bin(b ^ nb).count("1")
            assert w["bit"] == ((nb & -nb).bit_length() - 1 if nb else bits - 1)


# --- session 35: the figures, the hardware model and its box -----------------------------------

import itertools  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import sys  # noqa: E402

from extract_code import ROOT, question_path  # noqa: E402

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0034  # noqa: E402

PAGE = question_path(34).read_text(encoding="utf-8")


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(34)


def test_reference_matches_page_code():
    for v in range(32):
        assert q0034.gray(v) == bin2gray(v) and q0034.gray2bin(bin2gray(v)) == gray2bin(bin2gray(v), 5) == v


def test_step_7_to_8_behind_and_ahead():
    """Part a: the step 0111 -> 1000 sampled bit by bit gives all 16 values; besides the old
    (7) and the new (8), seven are behind (0..6, values the pointer held before) and seven
    ahead (9..15). A value ahead makes the reader count words that were not written; one
    behind is conservative only while it is not below the read pointer r: then the
    difference wraps past the size of the FIFO."""
    seen = {sum(((8 if s >> i & 1 else 7) >> i & 1) << i for i in range(4)) for s in range(16)}
    assert seen == set(range(16))
    places = {v: q0034.place(7, 4, v) for v in seen}
    assert [v for v, (w, _) in places.items() if w == "behind"] == list(range(7))
    assert [v for v, (w, _) in places.items() if w == "ahead"] == list(range(9, 16))
    assert places[15] == ("ahead", 7) and places[0] == ("behind", 7)
    for r in range(8):                                          # the read pointer, at most the old value
        for v in range(16):
            if v in (7, 8):
                continue
            harmful = (v - r) % 32 > 8 - r                      # 5-bit pointers, the extra bit 0 here
            assert harmful == (v > 8 or v < r), (r, v)
    # the wrap 1111 -> 0000 splits the same way, 7 and 7
    wrap = [q0034.place(15, 4, v)[0] for v in range(16)]
    assert wrap.count("behind") == wrap.count("ahead") == 7 and wrap[15] == "old" and wrap[0] == "new"


def test_explorer_place_and_binary_full_rule():
    """The sync box's verdict (behind or ahead, and how far) against q0034.place on every
    step and every value of 3 to 6 bits; the flags box's trap: the binary full rule copied
    onto Gray (only the top bit differs) fires at an occupancy other than 16 (23 and 8)."""
    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      const out = {{}};
      for (const bits of [3, 4, 5, 6]) {{
        const rows = [];
        for (let b = 0; b < (1 << bits); b++) for (let v = 0; v < (1 << bits); v++) rows.push(m.grayPlace(b, bits, v));
        out[bits] = rows;
      }}
      const flags = [];
      for (let w = 0; w < 32; w++) for (let r = 0; r < 32; r++) flags.push(m.grayFlags(w, r, 5).naiveFull);
      console.log(JSON.stringify({{ out, flags }}));""")
    for bits in (3, 4, 5, 6):
        rows = iter(got["out"][str(bits)])
        for b in range(1 << bits):
            for v in range(1 << bits):
                assert tuple(next(rows)) == q0034.place(b, bits, v), (bits, b, v)
    for (w, r), naive in zip(itertools.product(range(32), range(32)), got["flags"]):
        assert naive == (bin2gray(w) ^ bin2gray(r) == 16)
    assert got["flags"][23 * 32 + 8] and not fifo_full(bin2gray(23), bin2gray(8), 5) and (23 - 8) % 32 == 15


def _wave_blocks():
    return re.findall(r"```wavedrom\n(.*?)\n\s*```", PAGE, re.S)


def _lanes(src):
    lanes = {}
    for m in re.finditer(r'\{ name: "([^"]+)",\s*wave: "([^"]+)"([^}]*)\}', src):
        name, wave, rest = m.groups()
        per = re.search(r"period: ([\d.]+)", rest)
        ph = re.search(r"phase: (-?[\d.]+)", rest)
        lanes[name] = (wave, float(per.group(1)) if per else 1.0, float(ph.group(1)) if ph else 0.0)
    return lanes


def _changes(wave, period, phase):
    """The times a lane changes (a new character that is not '.'), as the waveform viewer
    computes them: t = k * period - phase."""
    return [round(k * period - phase, 6) for k, c in enumerate(wave) if k and c != "."]


def _rises(wave, period, phase):
    """The rising edges of a clock lane: every period of a 'p', and a '1' after a '0'."""
    out, level = [], None
    for k, c in enumerate(wave):
        t = round(k * period - phase, 6)
        if c == "p" or (c == "." and level == "p") or (c == "1" and level == "0"):
            out.append(t)
        if c != ".":
            level = c
    return out


def test_sample_wave_edges():
    """Part a's waveform: an rclk edge falls on the change of wptr, and the rq1 rows change
    only on rclk edges (the old diagram's rclk, "0.1.0.1" with period 1.5, rose at 3 and 9
    while the sync rows changed at 5)."""
    lanes = _lanes(_wave_blocks()[0])
    rclk = _rises(*lanes["rclk"])
    assert _changes(*lanes["wptr (binary)"]) == _changes(*lanes["wptr (Gray)"]) == [2.0]
    assert 2.0 in rclk
    for name in ("rq1 (binary)", "rq1 (Gray)"):
        assert set(_changes(*lanes[name])) <= set(rclk) and 2.0 in _changes(*lanes[name])
    assert _rises("0.1.0.1", 1.5, 0) == [3.0, 9.0]          # the old diagram, for the record


def test_latency_wave():
    """Part c's waveform, from tick 20 (slot 0) for ten slots: each wgray bit changes DELAY[i]
    ticks after its wclk edge; rclk rises on bit 0's change (the metastable x on rq1[0]); rq2
    and rempty change on rclk edges; rempty falls two rclk periods after the bit arrived;
    no lane runs past slot 10."""
    src = _wave_blocks()[1]
    lanes = _lanes(src)
    rclk = _rises(*lanes["rclk"])
    assert rclk == [0.9, 3.9, 6.9]
    assert _changes(*lanes["wgray[0]"]) == [0.9, 4.9] and _changes(*lanes["wgray[1]"]) == [2.7]
    assert lanes["rq1[0]"][0].startswith("0.x1")
    for name in ("rq2", "rempty"):
        assert set(_changes(*lanes[name])) <= set(rclk)
    fall = _changes(*lanes["rempty"])[0]
    assert round(fall - 0.9, 6) == 6.0 == 2 * q0034.PR / q0034.SLOT
    for wave, period, phase in lanes.values():
        assert len(wave) * period - phase <= q0034.WAVE_SLOTS + 1e-9


def _scenario(**kw):
    sc = dict(q0034.SCENARIOS["page"])
    sc.update(kw)
    return sc


def test_hw_model_scenarios():
    tr = {n: q0034.hw_trace(n) for n in q0034.SCENARIOS}
    # the page: bit 0 of the first word arrives on the rclk edge of tick 29 (metastable, settles
    # new), rempty falls at 89, two periods later; settling old makes it three
    assert q0034.first_word_latency("page") == (29, 89, 3) and q0034.first_word_latency("old") == (29, 119, 4)
    first = next(r for r in tr["page"] if r["clk"] == "r")
    assert first["t"] == 29 and first["meta"] == 1 and first["rq1"] == 1
    assert next(r for r in tr["old"] if r["clk"] == "r")["rq1"] == 0
    # the binary trap: 7 -> 8 with bit 3 first, rq1 takes 01111 = 15 at tick 24, and the
    # reader believes 8 words when one was written; the XOR trap takes Gray 01000, also 15
    for name in ("bin", "comb"):
        r24 = next(r for r in tr[name] if r["t"] == 24)
        assert (r24["rq1"] if name == "bin" else q0034.gray2bin(r24["rq1"])) == 15
        r54 = next(r for r in tr[name] if r["t"] == 54)
        assert r54["seen"] == 8 and r54["true"] == 1
    assert [g for _, _, g in q0034.glitch_values()] == [0b0100, 0b1000, 0b1110, 0b1101, 0b1100]
    # full: up at 320 with 16 words, the read of tick 329 reaches wclk's domain at 338, full
    # falls at 380 and the next write goes in at 400
    full = tr["full"]
    up = next(r for r in full if r["clk"] == "w" and r["wfull"])
    down = next(r for r in full if r["clk"] == "w" and r["t"] > up["t"] and not r["wfull"])
    write = next(r for r in full if r["clk"] == "w" and r["t"] > down["t"] and r["inc"])
    assert (up["t"], up["true"], down["t"], write["t"]) == (320, 16, 380, 400)
    assert all(not r["inc"] for r in full if r["clk"] == "w" and up["t"] < r["t"] < write["t"])


def test_hw_model_gray_is_safe_for_every_phase():
    """With registered Gray pointers, for every phase of rclk and both ways a metastable bit
    settles: the reader never counts more words than are in the FIFO and the writer never
    fewer; every synchronized value is one the far register held; rempty falls between 2 and
    3 rclk periods after the first word's bit arrived. The binary pointer breaks the first
    rule at some phase."""
    broke = False
    for r0 in range(1, 30):
        if r0 % 10 == 0:
            continue                                            # an rclk edge on a wclk edge
        for settle in ("new", "old"):
            sc = _scenario(r0=r0, settle=settle, writes=[1, 2, 3, 5, 6], end=400)
            tr = q0034.hw_trace(sc)
            held_w, held_r = {0}, {0}
            for r in tr:
                held_w.add(r["wgray"])
                held_r.add(r["rgray"])
                assert r["rq1"] in held_w and r["rq2"] in held_w and r["wq1"] in held_r and r["wq2"] in held_r
                if r["clk"] == "r":
                    assert r["seen"] <= r["true"]
                else:
                    assert r["seen"] >= r["true"]
            arrive = 20 + q0034.DELAY[0]
            fall = next(r["t"] for r in tr if r["clk"] == "r" and not r["rempty"])
            assert 2 * q0034.PR <= fall - arrive <= 3 * q0034.PR, (r0, settle)
            assert tr[-1]["rbin"] == tr[-1]["wbin"] == 5 and tr[-1]["rempty"] == 1   # every word read, no more
        bad = [r for r in q0034.hw_trace(_scenario(mode="bin", p0=7, r0=r0, writes=[1], end=200))
               if r["clk"] == "r" and r["seen"] > r["true"]]
        broke |= bool(bad)
    assert broke


def test_hardware_box_matches_the_reference():
    """The box (grayhw.js): its trace of every scenario equals hw_trace; its diagram has the
    page's rectangles and wires; the domain of the edge is lit, a register that changed is
    framed, and a bit caught metastable is marked."""
    from page_tests import explorer_require, node_json

    names = list(q0034.SCENARIOS)
    got = node_json(f"const m = {explorer_require()};console.log(JSON.stringify({json.dumps(names)}.map((n) => m.ghTrace(n))));")
    for name, t in zip(names, got):
        assert t == q0034.hw_trace(name), name
    svgs = node_json(f"const m = {explorer_require()};const t = m.ghTrace('page');"
                     "console.log(JSON.stringify([m.ghDiagram(null), ...t.map((c, i) => m.ghDiagram(c, t[i - 1] || null))]));")
    rect = re.compile(r'<rect x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"')
    path = re.compile(r'<path class="gh-wire[^"]*" d="([^"]+)"')
    page = q0034.datapath_svg()
    assert len(rect.findall(page)) == len(q0034.DP_BLOCKS) and len(path.findall(page)) == len(q0034.DP_WIRES)
    for live in svgs:
        assert rect.findall(live) == rect.findall(page) and path.findall(live) == path.findall(page)
    norm = lambda d: d.replace("M", "").replace("L", "").replace(",", " ").split()
    for live, c in zip(svgs[1:], q0034.hw_trace("page")):
        on = re.findall(r'class="gh-blk gh-\w+ is-on[^"]*" data-b="(\w+)"', live)
        assert sorted(on) == sorted(b[0] for b in q0034.DP_BLOCKS if b[6] == c["clk"])
        assert ("is-meta" in live) == bool(c["meta"]) and ("gh-xbit" in live) == bool(c["meta"])
    for _id, pts, *_ in q0034.DP_WIRES:
        for x, y in pts:
            assert 0 <= x <= q0034.DP_W and 0 <= y <= q0034.DP_H
    assert all(norm(d) for d in path.findall(page))
