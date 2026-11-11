from extract_code import load_python

ns = load_python(2)
SWAPS = [ns["swap_temp"], ns["swap_arith"], ns["swap_xor"]]
PAIRS = [(5, 3), (-7, 12), (2**31 - 1, 1), (0, 0), (-2**31, -1), (123456789, -987654321)]


def test_all_methods_swap():
    for swap in SWAPS:
        for a, b in PAIRS:
            v = [a, b]
            swap(v, 0, 1)
            assert v == [b, a], (swap.__name__, a, b)


def test_same_variable_pitfall():
    # Documented on the page: arithmetic and XOR versions zero the variable.
    for swap, expected in zip(SWAPS, [9, 0, 0]):
        v = [9]
        swap(v, 0, 0)
        assert v == [expected], swap.__name__


WRAP = {0: lambda x: x, 8: lambda x: x % 256, 32: lambda x: (x + 2**31) % 2**32 - 2**31}


def test_explorer_matches_page_code():
    """The tracer box: its three swaps against the page's swap_temp, swap_arith and
    swap_xor on random pairs (the 8-bit mode modulo 256, the 32-bit mode as a signed int,
    the inputs wrapped too), the aliased call, and the symbolic expressions (a0 ^ b0 and the
    like) evaluated on the numbers."""
    import json
    import random

    from page_tests import explorer_require, node_json

    rng = random.Random(2)
    cases = [[5, 3], [3, 5], [7, 7], [0, 9], [200, 100], [-4, 11], [-5, 3], [2**31 - 1, 1], [-2**31, -1], [2**31, 5]]
    cases += [[rng.randint(-50, 300), rng.randint(-50, 300)] for _ in range(100)]
    cases += [[rng.randint(-2**31, 2**31 - 1), rng.randint(-2**31, 2**31 - 1)] for _ in range(40)]
    got = node_json(f"""
      const m = {explorer_require()};
      const out = [];
      for (const [a, b] of {json.dumps(cases)}) for (const kind of ["temp", "arith", "xor"]) for (const bits of [0, 8, 32]) for (const same of [false, true]) {{
        if (!bits && Math.max(Math.abs(a), Math.abs(b)) > 1e9) continue;   // the box keeps unbounded values within 1e9
        const t = m.swapTrace(kind, a, b, same, bits);
        const f = t.frames[t.frames.length - 1];
        out.push([a, b, kind, bits, same, f.a, f.b, t.ok, t.frames.map((g) => [g.aSym, g.bSym, g.a, g.b])]);
      }}
      console.log(JSON.stringify(out));""")
    fns = {"temp": ns["swap_temp"], "arith": ns["swap_arith"], "xor": ns["swap_xor"]}

    def evaluate(sym, a0, b0, kind):
        # "a0", "b0", "0", "a0 + b0", "2·a0", "a0 ^ b0", "-1·b0" ...
        if sym == "0":
            return 0
        total = 0
        for term in sym.split(" ^ " if kind == "xor" else " + "):
            coef, name = (term.split("·") if "·" in term else ("1", term))
            v = (a0 if name == "a0" else b0) * int(coef)
            total = (total ^ v) if kind == "xor" else total + v
        return total

    for a, b, kind, bits, same, fa, fb, ok, frames in got:
        v = [a, b]
        fns[kind](v, 0, 0 if same else 1)
        wrap = WRAP[bits]
        assert fa == wrap(v[0]) and fb == wrap(v[0] if same else v[1]), (a, b, kind, bits, same)
        assert ok == (not same and fa == wrap(b) and fb == wrap(a))
        for a_sym, b_sym, va, vb in frames:
            assert wrap(evaluate(a_sym, a, b, kind)) == va and wrap(evaluate(b_sym, a, b, kind)) == vb, (a, b, kind, bits, same, a_sym, b_sym)


def test_explorer_rotation():
    """The follow-up in the box: the XOR rotation a <- b, b <- c, c <- a as two swaps; its
    six frames evaluate their a0 ^ b0 ^ c0 expressions to the values, and the end state
    is the rotation (modulo 256 in the 8-bit mode)."""
    import json
    import random

    from page_tests import explorer_require, node_json

    rng = random.Random(3)
    cases = [[5, 3, 7], [0, 0, 0], [9, 9, 9], [200, 100, 255], [-4, 11, -30], [1, 2, 4], [2**31, -1, 300]] + [[rng.randint(-50, 300) for _ in range(3)] for _ in range(60)]
    got = node_json(f"""
      const m = {explorer_require()};
      const out = [];
      for (const [a, b, c] of {json.dumps(cases)}) for (const bits of [0, 8, 32]) {{
        if (!bits && Math.max(Math.abs(a), Math.abs(b), Math.abs(c)) > 1e9) continue;   // the box keeps unbounded values within 1e9
        const t = m.rotTrace(a, b, c, bits);
        out.push([a, b, c, bits, t.ok, t.code, t.frames.map((g) => [g.line, g.a, g.b, g.c, g.aSym, g.bSym, g.cSym])]);
      }}
      console.log(JSON.stringify(out));""")

    def evaluate(sym, a0, b0, c0):
        if sym == "0":
            return 0
        total = 0
        for term in sym.split(" ^ "):
            total ^= {"a0": a0, "b0": b0, "c0": c0}[term]
        return total

    for a, b, c, bits, ok, code, frames in got:
        wrap = WRAP[bits]
        assert code == ["a = a ^ b", "b = a ^ b", "a = a ^ b", "b = b ^ c", "c = b ^ c", "b = b ^ c"]
        assert [fr[0] for fr in frames] == list(range(-1, 6))
        assert ok and frames[-1][1:4] == [wrap(b), wrap(c), wrap(a)], (a, b, c, bits)
        for _line, va, vb, vc, a_sym, b_sym, c_sym in frames:
            assert (wrap(evaluate(a_sym, a, b, c)), wrap(evaluate(b_sym, a, b, c)), wrap(evaluate(c_sym, a, b, c))) == (va, vb, vc), (a, b, c, bits, a_sym, b_sym, c_sym)
        assert frames[3][4:] == ["b0", "a0", "c0"] and frames[-1][4:] == ["b0", "c0", "a0"]


def test_xor_figure():
    """The bit figure of part c (tools/figures/q0002.py): its rows against the page's
    swap_xor and the page's numeric example table, and a frame exactly on the bits each
    step changed."""
    import re
    import sys

    from extract_code import ROOT, question_path

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import q0002

    rows = q0002.rows()
    v = [q0002.A0, q0002.B0]
    load_python(2)["swap_xor"](v, 0, 1)
    assert (rows[-1][2], rows[-1][3]) == tuple(v) == (q0002.B0, q0002.A0)
    page = question_path(2).read_text(encoding="utf-8")
    table = re.findall(r"\| ‏`([01]{4})` \((\d+)\) \| ‏`([01]{4})` \((\d+)\) \|", page)
    assert [(int(a, 2), int(b, 2)) for a, _, b, _ in table] == [(a, b) for _, _, a, b in rows]
    assert all(int(a, 2) == int(da) and int(b, 2) == int(db) for a, da, b, db in table)
    svg = q0002.figure()
    changed = sum(bin(p[2] ^ r[2]).count("1") + bin(p[3] ^ r[3]).count("1") for p, r in zip(rows, rows[1:]))
    assert svg.count('class="fc-chg"') == changed == 6
    assert q0002.bits(6) == [0, 1, 1, 0]                 # the most significant bit is drawn first (left)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(2)


def test_explorer_page_tasks():
    """The numbers the page's "try it" tasks name: the 8-bit sum 300 -> 44 and the two
    subtractions -56 -> 200 and -156 -> 100, the page's 32-bit example 2^31 - 1 and 1 (the
    sum wraps to -2^31), swap(v, i, i) with 9 (18, then 0), the temp version after line 2
    (a = b = 3, temp = 5), -5 typed in 8 bits (251), and the rotation of 1, 2, 4."""
    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      const t = (k, a, b, same, bits) => m.swapTrace(k, a, b, same, bits).frames.map((f) => [f.text, f.a, f.b, f.temp]);
      console.log(JSON.stringify({{
        arith8: t("arith", 200, 100, false, 8), arith32: t("arith", 2147483647, 1, false, 32),
        same: t("arith", 9, 9, true, 0), temp: t("temp", 5, 3, false, 0), neg8: t("xor", -5, 3, false, 8),
        rot: m.rotTrace(1, 2, 4, 0).frames.map((f) => [f.a, f.b, f.c]),
      }}));""")
    assert [f[0] for f in got["arith8"][1:]] == ["200 + 100 = 300 → 44 (mod 256)", "44 - 100 = -56 → 200 (mod 256)", "44 - 200 = -156 → 100 (mod 256)"]
    assert got["arith8"][-1][1:3] == [100, 200]
    assert got["arith32"][1][1] == -2**31 and got["arith32"][-1][1:3] == [1, 2**31 - 1]
    assert [f[1] for f in got["same"]] == [9, 18, 0, 0]
    assert got["temp"][2][1:] == [3, 3, 5] and got["temp"][-1][1:3] == [3, 5]
    assert got["neg8"][0][1:3] == [251, 3]
    assert got["rot"][3] == [2, 1, 4] and got["rot"][-1] == [2, 4, 1]


def test_xor_in_javascript_truncates():
    """The overflow trap: JavaScript's ^ cuts a number to 32 bits, so the XOR swap of
    2^32 + 1 and 5 ends with 5 and 1 (the page says XOR is safe only where it works on all
    the bits of the type)."""
    from page_tests import node_json

    assert node_json("let a = 2 ** 32 + 1, b = 5; a ^= b; b ^= a; a ^= b; console.log(JSON.stringify([a, b]))") == [5, 1]


def test_python_tuple_swap_needs_no_helper_name():
    """Part a: v[i], v[j] = v[j], v[i] evaluates the right side first, so it swaps."""
    v = [5, 3]
    v[0], v[1] = v[1], v[0]
    assert v == [3, 5]
