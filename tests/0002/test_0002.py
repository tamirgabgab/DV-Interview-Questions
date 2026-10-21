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


def test_explorer_matches_page_code():
    """The tracer box: its three swaps against the page's swap_temp, swap_arith and
    swap_xor on random pairs (the 8-bit mode modulo 256), the aliased call, and the
    symbolic expressions (a0 ^ b0 and the like) evaluated on the numbers."""
    import json
    import random

    from page_tests import explorer_require, node_json

    rng = random.Random(2)
    cases = [[5, 3], [3, 5], [7, 7], [0, 9], [200, 100], [-4, 11]] + [[rng.randint(-50, 300), rng.randint(-50, 300)] for _ in range(100)]
    got = node_json(f"""
      const m = {explorer_require()};
      const out = [];
      for (const [a, b] of {json.dumps(cases)}) for (const kind of ["temp", "arith", "xor"]) for (const bits of [0, 8]) for (const same of [false, true]) {{
        if (bits && (a < 0 || b < 0)) continue;
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
        mod = (1 << bits) if bits else None
        wrap = (lambda x: x % mod) if mod else (lambda x: x)
        assert fa == wrap(v[0]) and fb == wrap(v[0] if same else v[1]), (a, b, kind, bits, same)
        assert ok == (not same and fa == wrap(b) and fb == wrap(a))
        for a_sym, b_sym, va, vb in frames:
            assert wrap(evaluate(a_sym, a, b, kind)) == va and wrap(evaluate(b_sym, a, b, kind)) == vb, (a, b, kind, bits, same, a_sym, b_sym)
