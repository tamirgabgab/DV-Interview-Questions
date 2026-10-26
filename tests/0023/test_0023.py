"""Question 0023: the PCIe endpoint reference model. The page's Python classes run against
an independent byte-level shadow memory and the protocol rules as the page states them;
the SystemVerilog classes run the same way in tests/0023/tb.sv."""

import random
import re
import subprocess
import sys
from itertools import combinations

from extract_code import ROOT, load_python, question_path

ns = load_python(23)
MemWriteReq, MemReadReq = ns["MemWriteReq"], ns["MemReadReq"]
Aligned, Unaligned = ns["EndpointRefModel"], ns["UnalignedEndpointModel"]
RCB, MPS, MRRS = ns["RCB"], ns["MPS"], ns["MRRS"]


class Checker:
    """Shadow memory at byte resolution, one record per open read, and the checks a
    scoreboard would run on every completion."""

    def __init__(self):
        self.shadow = {}
        self.open = {}
        self.last_key = None
        self.interleaved = 0
        self.shapes = set()            # (address % RCB, length, sizes) of every finished read

    def write(self, address, data):
        for i, b in enumerate(data):
            self.shadow[address + i] = b

    def read(self, req, cycle):
        key = (req.requester_id, req.tag)
        assert key not in self.open, "tag reused while open"
        snap = bytes(self.shadow.get(req.address + i, 0) for i in range(req.length_bytes))
        self.open[key] = {"next": req.address, "left": req.length_bytes, "snap": snap,
                          "start": req.address, "cycle": cycle, "sizes": []}

    def completion(self, c, cycle):
        key = (c.requester_id, c.tag)
        e = self.open[key]
        assert c.start_address == e["next"], "completions of one read must be contiguous and ascending"
        assert c.byte_count == e["left"], "byte count is what is left, this payload included"
        assert 0 < len(c.data) <= MPS
        assert c.start_address == e["start"] or c.start_address % RCB == 0, "a cut must be on an RCB boundary"
        off = c.start_address - e["start"]
        assert c.data == e["snap"][off:off + len(c.data)], "payload must be the memory at request time"
        assert cycle > e["cycle"], "a completion needs at least one cycle of delay"
        if e["sizes"] and self.last_key not in (None, key):
            self.interleaved += 1
        self.last_key = key
        e["sizes"].append(len(c.data))
        e["next"] += len(c.data)
        e["left"] -= len(c.data)
        if e["left"] == 0:
            self.shapes.add((e["start"] % RCB, sum(e["sizes"]), tuple(e["sizes"])))
            del self.open[key]


def drive(model_cls, aligned, seed, steps=80):
    """Random traffic for `steps` cycles, then drain. Returns the checker."""
    rng = random.Random(seed)
    m = model_cls(random.Random(seed + 1))
    chk = Checker()
    tags = list(range(64))

    def place():
        if aligned:
            return 0x10000 + rng.randrange(8) * RCB, rng.choice([RCB, 2 * RCB])
        return 0x10000 + rng.randrange(1024), rng.randint(1, MRRS)

    for _ in range(steps):
        m.tick()
        if rng.random() < 0.4:
            a, n = place()
            data = bytes(rng.randrange(256) for _ in range(n))
            m.process_write(MemWriteReq(a, data))
            chk.write(a, data)
        if rng.random() < 0.4 and tags:
            a, n = place()
            req = MemReadReq(a, n, 0x0200 + rng.randrange(2), tags.pop(rng.randrange(len(tags))))
            m.process_read(req)
            chk.read(req, m.current_cycle)
        c = m.get_next_completion()
        if c is not None:
            chk.completion(c, m.current_cycle)
    for _ in range(600):
        if not m.pending_reads:
            break
        m.tick()
        c = m.get_next_completion()
        if c is not None:
            chk.completion(c, m.current_cycle)
    assert not m.pending_reads and not chk.open, "every read must finish"
    return chk


def answer(model_cls, write, req, seed):
    """One write, one read, drained: the completions of the read in order."""
    m = model_cls(random.Random(seed))
    m.process_write(write)
    m.process_read(req)
    out = []
    while m.pending_reads:
        m.tick()
        c = m.get_next_completion()
        if c is not None:
            out.append(c)
    return out


def test_part_a_example():
    write = MemWriteReq(0x10000, bytes(range(256)))
    req = MemReadReq(0x10000, 256, 0x0200, 0x15)
    seen = {}
    for seed in range(60):
        cpls = answer(Aligned, write, req, seed)
        sizes = tuple(len(c.data) for c in cpls)
        seen[sizes] = [c.byte_count for c in cpls]
        assert b"".join(c.data for c in cpls) == bytes(range(256))
        assert [c.start_address for c in cpls] == [0x10000, 0x10080][:len(cpls)]
        assert all((c.requester_id, c.tag) == (0x0200, 0x15) for c in cpls)
    assert seen == {(256,): [256], (128, 128): [256, 128]}


def test_part_b_example():
    write = MemWriteReq(0x10020, bytes(0x20 + i & 0xFF for i in range(256)))
    req = MemReadReq(0x10020, 256, 0x0300, 0x22)
    seen = {}
    for seed in range(80):
        cpls = answer(Unaligned, write, req, seed)
        sizes = tuple(len(c.data) for c in cpls)
        seen[sizes] = ([c.start_address for c in cpls], [c.byte_count for c in cpls])
        assert b"".join(c.data for c in cpls) == write.data
    assert seen == {
        (256,): ([0x10020], [256]),
        (96, 160): ([0x10020, 0x10080], [256, 160]),
        (224, 32): ([0x10020, 0x10100], [256, 32]),
        (96, 128, 32): ([0x10020, 0x10080, 0x10100], [256, 160, 32]),
    }


def test_illegal_requests_are_rejected():
    for cls in (Aligned, Unaligned):
        m = cls(random.Random(0))
        for n in (0, MRRS + 1, 4096):
            try:
                m.process_read(MemReadReq(0x10000, n, 1, 1))
            except ValueError:
                continue
            raise AssertionError(f"{cls.__name__} accepted a read of {n} bytes")
        assert not m.pending_reads
    m = Aligned(random.Random(0))
    for address, data in ((0x10020, bytes(RCB)), (0x10000, bytes(100))):
        try:
            m.process_write(MemWriteReq(address, data))
        except ValueError:
            continue
        raise AssertionError("the aligned model accepted an unaligned write")


def test_unaligned_write_keeps_the_neighbours():
    m = Unaligned(random.Random(0))
    m.process_write(MemWriteReq(0x10000, bytes(range(256))))
    m.process_write(MemWriteReq(0x10070, bytes([0xAA] * 32)))          # crosses 0x10080
    m.process_write(MemWriteReq(0x10200, bytes([0x55])))                # one byte in a fresh block
    expect = bytearray(range(256))
    expect[0x70:0x90] = [0xAA] * 32
    assert m.read_bytes(0x10000, 256) == bytes(expect)
    assert m.read_bytes(0x101F0, 32) == bytes(16) + bytes([0x55]) + bytes(15)
    assert set(m.memory) == {0x10000, 0x10080, 0x10200} and all(len(b) == RCB for b in m.memory.values())


def test_random_aligned_traffic():
    shapes, interleaved = set(), 0
    for seed in range(40):
        chk = drive(Aligned, True, seed)
        shapes |= chk.shapes
        interleaved += chk.interleaved
    assert shapes == {(0, 128, (128,)), (0, 256, (256,)), (0, 256, (128, 128))}
    assert interleaved > 50


def test_random_unaligned_traffic():
    shapes, interleaved = set(), 0
    for seed in range(40):
        chk = drive(Unaligned, False, seed)
        shapes |= chk.shapes
        interleaved += chk.interleaved
    assert interleaved > 50
    assert any(len(s) == 3 for _, _, s in shapes) and any(len(s) == 1 for _, _, s in shapes)
    assert any(off != 0 for off, _, _ in shapes)


def reference_splits(address, length):
    """Independent enumeration (as in question 0020): every subset of the RCB boundaries
    strictly inside the request."""
    end = address + length
    bounds = list(range((address // RCB + 1) * RCB, end, RCB))
    out = set()
    for k in range(len(bounds) + 1):
        for sub in combinations(bounds, k):
            pts = [address, *sub, end]
            out.add(tuple(b - a for a, b in zip(pts, pts[1:])))
    return out


def test_fragments_cover_exactly_the_legal_splits():
    rng = random.Random(5)
    for _ in range(60):
        address, length = 0x10000 + rng.randrange(1024), rng.randint(1, MRRS)
        seen = set()
        for seed in range(40):
            m = Unaligned(random.Random(seed))
            sizes = m.create_fragments(address, length)
            assert sum(sizes) == length and all(s > 0 for s in sizes)
            seen.add(tuple(sizes))
        assert seen == reference_splits(address, length), (hex(address), length)
    for length in (RCB, 2 * RCB):
        got = {tuple(Unaligned(random.Random(s)).create_fragments(0x20000, length)) for s in range(40)}
        want = {tuple(Aligned(random.Random(s)).create_fragments(0x20000, length)) for s in range(40)}
        assert got == want == reference_splits(0x20000, length)


def test_scheduler_waits_and_sends_one_per_cycle():
    m = Unaligned(random.Random(11))
    m.process_write(MemWriteReq(0x10000, bytes(512)))
    for tag in range(8):
        m.process_read(MemReadReq(0x10000 + 7 * tag, 200, 0x0200, tag))
    first = None
    per_cycle = {}
    while m.pending_reads:
        m.tick()
        c = m.get_next_completion()
        if c is not None:
            first = first or m.current_cycle
            per_cycle[m.current_cycle] = per_cycle.get(m.current_cycle, 0) + 1
    assert first >= 1 and all(v == 1 for v in per_cycle.values())
    assert first <= Unaligned.MAX_DELAY


def test_figures_up_to_date():
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0023.py")],
                         capture_output=True, text=True, check=True).stdout
    text = question_path(23).read_text(encoding="utf-8")
    for pattern in (r'<div class="stepper".*?</div></div>', r'<svg class="figure.*?</svg>',
                    r'<span class="viz-legend">.*?</span></span>'):
        generated = re.findall(pattern, out)
        assert generated and re.findall(pattern, text) == generated, pattern
    page_rows = [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
    for row in (l for l in out.splitlines() if l.startswith("|")):
        assert row.strip() in page_rows, row


def test_explorer_matches_page_model():
    """The endpoint explorer: its model against UnalignedEndpointModel with the same random
    draws (unit values mapped the same way on both sides) on random writes and reads run
    to completion; the page's two examples with their exact draws."""
    import json
    import random

    from page_tests import explorer_require, node_json

    rng = random.Random(23)
    reqs = []
    for _ in range(40):
        length = rng.randint(1, 256)
        address = 0x20000 + rng.randrange(0, 4096 - length)
        if rng.random() < 0.4:
            reqs.append(["write", address, length])
        else:
            reqs.append(["read", address, length, 0x0200 + rng.randint(0, 3), len(reqs)])
    units = [rng.random() for _ in range(4000)]
    got = node_json(f"""
      const m = {explorer_require()};
      const units = {json.dumps(units)}, rng = m.epUnitRng(units);
      const s = m.epInit();
      let w = 1;
      for (const r of {json.dumps(reqs)}) {{
        if (r[0] === "write") {{ m.epWrite(s, r[1], Array.from({{ length: r[2] }}, (_, i) => (i + 0x10 * w) & 0xFF)); w++; }}
        else m.epRead(s, {{ address: r[1], length: r[2], rid: r[3], tag: r[4] }}, rng);
      }}
      let guard = 0;
      while (s.pending.length && guard++ < 600) m.epCycle(s, rng);
      const mem = Object.fromEntries(Object.entries(s.memory).map(([k, v]) => [k, v]));
      const ea = m.epRunScript(m.EP_SCRIPTS.a), eb = m.epRunScript(m.EP_SCRIPTS.b);
      const rows = (st) => st.out.map((c) => [c.cycle, c.rid, c.tag, c.address, c.size, c.bc, c.first, c.last]);
      console.log(JSON.stringify({{ out: rows(s), mem, cycles: s.cycle, used: 4000 - units.length, a: rows(ea), b: rows(eb) }}));""")

    class Units:
        def __init__(self, values):
            self.values = list(values)

        def randint(self, a, b):
            return a + int(self.values.pop(0) * (b - a + 1))

        def choice(self, seq):
            return seq[int(self.values.pop(0) * len(seq))]

    units_py = Units(units)
    model = Unaligned(units_py)
    w = 1
    for r in reqs:
        if r[0] == "write":
            model.process_write(MemWriteReq(r[1], bytes((i + 0x10 * w) & 0xFF for i in range(r[2]))))
            w += 1
        else:
            model.process_read(MemReadReq(r[1], r[2], r[3], r[4]))
    out = []
    while model.pending_reads and model.current_cycle < 600:
        model.tick()
        cpl = model.get_next_completion()
        if cpl:
            out.append([model.current_cycle, cpl.requester_id, cpl.tag, cpl.start_address, len(cpl.data), cpl.byte_count, cpl.data[0], cpl.data[-1]])
    assert got["out"] == out and got["cycles"] == model.current_cycle
    assert 4000 - len(units_py.values) == got["used"]
    assert {int(k): list(v) for k, v in got["mem"].items()} == {k: list(v) for k, v in model.memory.items()}
    # the page's tables
    assert got["a"] == [[3, 0x0200, 0x16, 0x10100, 128, 256, 0x00, 0x7F], [5, 0x0200, 0x15, 0x10000, 128, 256, 0x00, 0x7F],
                        [6, 0x0200, 0x16, 0x10180, 128, 128, 0x80, 0xFF], [7, 0x0200, 0x15, 0x10080, 128, 128, 0x80, 0xFF]]
    assert got["b"] == [[2, 0x0300, 0x22, 0x10020, 96, 256, 0x20, 0x7F], [4, 0x0200, 0x15, 0x10000, 128, 256, 0x00, 0x7F],
                        [5, 0x0300, 0x22, 0x10080, 128, 160, 0x80, 0xFF], [6, 0x0200, 0x15, 0x10080, 128, 128, 0x80, 0xFF],
                        [7, 0x0300, 0x22, 0x10100, 32, 32, 0x00, 0x1F]]


def test_explorer_read_timeline():
    """The timeline the box draws (U136): every read's record carries the cycle it was
    issued at and its wait windows; the k-th window starts at the issue (k = 0) or at the
    k-th completion, ends at the ready cycle the draw gave, and the k-th completion goes
    out at or after that ready cycle; a finished read has one window per completion."""
    import json
    import random

    from page_tests import explorer_require, node_json

    rng = random.Random(230)
    reqs = [["read", 0x20000 + rng.randrange(0, 3800), rng.randint(1, 256), 0x0200, i] for i in range(12)]
    got = node_json(f"""
      const m = {explorer_require()};
      const rng = m.epUnitRng({json.dumps([rng.random() for _ in range(2000)])});
      const s = m.epInit();
      const issued = [];
      for (const r of {json.dumps(reqs)}) {{ if (r[4] % 3 === 2) m.epCycle(s, rng); m.epRead(s, {{ address: r[1], length: r[2], rid: r[3], tag: r[4] }}, rng); issued.push(s.cycle); }}
      const mid = JSON.parse(JSON.stringify(s.reads));
      let guard = 0;
      while (s.pending.length && guard++ < 600) m.epCycle(s, rng);
      const a = m.epRunScript(m.EP_SCRIPTS.a);
      console.log(JSON.stringify({{ issued, mid, reads: s.reads, out: s.out, a: a.reads, aout: a.out }}));""")
    assert [r["issued"] for r in got["reads"]] == got["issued"]
    for reads, out in ((got["reads"], got["out"]), (got["a"], got["aout"])):
        for r in reads:
            outs = [c["cycle"] for c in out if c["read"] == r["id"]]
            assert len(r["waits"]) == len(r["sizes"]) == len(outs), r
            for k, (start, ready) in enumerate(r["waits"]):
                assert start == (r["issued"] if k == 0 else outs[k - 1]), (r, k)
                assert start < ready <= outs[k], (r, k)
    assert all(r["waits"][0][0] == r["issued"] and 1 <= len(r["waits"]) <= len(r["sizes"]) for r in got["mid"])


def test_explorer_cycle_axis():
    """The cycle axis of the box (X146): a slot per cycle up to now with the completion
    that went out in it (none in the others), and for the last six reads a ready level
    that is high from each wait window's ready cycle to the completion that closes it
    (to now while it is open)."""
    import json
    import random

    from page_tests import explorer_require, node_json

    rng = random.Random(2323)
    reqs = [[0x20000 + rng.randrange(0, 3800), rng.randint(1, 256), i] for i in range(9)]
    got = node_json(f"""
      const m = {explorer_require()};
      const rng = m.epUnitRng({json.dumps([rng.random() for _ in range(3000)])});
      const s = m.epInit();
      for (const [a, l, t] of {json.dumps(reqs)}) {{ m.epRead(s, {{ address: a, length: l, rid: 0x200, tag: t }}, rng); m.epCycle(s, rng); }}
      for (let i = 0; i < 6; i++) m.epCycle(s, rng);
      console.log(JSON.stringify({{ s, strip: m.epStrip(s) }}));""")
    s, st = got["s"], got["strip"]
    assert st["n"] == s["cycle"] + 1
    by = {c["cycle"]: c for c in s["out"]}
    assert [c and (c["cycle"], c["tag"]) for c in st["cpl"]] == [(k, by[k]["tag"]) if k in by else None for k in range(st["n"])]
    assert [r["id"] for r in st["reads"]] == [r["id"] for r in s["reads"][-6:]]
    for r in st["reads"]:
        rec = next(x for x in s["reads"] if x["id"] == r["id"])
        outs = [c["cycle"] for c in s["out"] if c["read"] == r["id"]]
        want = [0] * st["n"]
        for k, (_, ready) in enumerate(rec["waits"]):
            end = outs[k] if k < len(outs) else s["cycle"]
            for c in range(ready, min(end, st["n"] - 1) + 1):
                want[c] = 1
        assert r["ready"] == want, r["id"]
        assert all(r["ready"][c] for c in outs)       # a completion goes out only when ready


def test_explorer_manual_read_after_example():
    """A read of the reader's own sent after the page's example (whose scripted draws were
    made for other moments) and then cycled to the end: no pick out of range, every
    completion goes out (the box once threw here)."""
    from page_tests import explorer_require, node_json

    got = node_json(f"""
const m = {explorer_require()};
const out = [];
for (const name of ["a", "b"]) {{
  for (let keep = 0; keep <= 13; keep++) {{
    const script = m.EP_SCRIPTS[name], s = m.epInit();
    const rng = m.epValueRng([...script.draws].slice(0, keep), m.epUnitRng([], () => 0.999));
    m.epWrite(s, 0x10000, Array.from({{ length: 512 }}, (_, i) => i & 0xFF));
    script.reads.forEach(([address, length, rid, tag]) => m.epRead(s, {{ address, length, rid, tag }}, rng));
    m.epRead(s, {{ address: 0x10040, length: 200, rid: 0x0200, tag: 0x30 }}, rng);
    let guard = 0;
    while (s.pending.length && guard++ < 400) m.epCycle(s, rng);
    out.push([s.pending.length, s.reads.reduce((n, r) => n + r.waits.length, 0) > 0, s.out.length]);
  }}
}}
console.log(JSON.stringify(out));
""")
    assert all(pending == 0 and n > 0 for pending, _, n in got)
