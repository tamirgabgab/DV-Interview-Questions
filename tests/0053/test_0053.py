"""Question 0053: the page's AluCoverage and expected_closure against the generator's
independent bins and its exact closure times (inclusion-exclusion with fractions,
tools/figures/q0053.py); a seeded simulation of the closure; the constants the
SystemVerilog testbench checks (the covergroup itself runs in Verilator there); the
explorer's JavaScript; and the page copies of the generated blocks."""

import json
import random
import re
import sys
from fractions import Fraction as Fr

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0053  # noqa: E402

ns = load_python(53)
AluCoverage, value_bin, cell_probs, expected_closure, OPS = (ns[k] for k in ("AluCoverage", "value_bin", "cell_probs", "expected_closure", "OPS"))
DIST_F = {d: {k: float(v) for k, v in q0053.DISTS[d].items()} for d in q0053.DISTS}


def test_page_numbers():
    assert sum(AluCoverage.SIZES.values()) == 87 and AluCoverage.SIZES["cross"] == 72 == len(q0053.CELLS)
    assert sum(v for k, v in AluCoverage.SIZES.items() if k != "cross") == 15
    cov = AluCoverage()
    cov.sample("ADD", 0, 0, 0)
    assert abs(cov.coverage() - 24.277777777777) < 1e-9 and q0053.coverage([("ADD", 0, 0, 0)]) == Fr(874, 36)
    for op in OPS:
        for a in (0, 255, 128, 7):
            for b in (0, 255, 128, 7):
                cov.sample(op, a, b, (a + b) % 2)
    assert cov.coverage() == 100
    try:
        AluCoverage().sample("MUL", 0, 0, 0)
        raise AssertionError("an illegal op must raise")
    except ValueError:
        pass
    # part c: 39 rarest cells at 1/327680; the exact times; 80 H_72 for equal bins
    ps = q0053.cell_probs("uniform")
    assert min(ps) == Fr(1, 327680) and ps.count(min(ps)) == 39
    e = {d: q0053.expected_closure(q0053.cell_probs(d)) for d in q0053.DISTS}
    assert round(float(e["uniform"])) == 1393801 and round(float(e["dist"])) == 534 and round(float(e["equal"])) == 389
    assert e["equal"] == 80 * sum(Fr(1, k) for k in range(1, 73))
    assert 2600 < e["uniform"] / e["dist"] < 2620


def test_model_matches_the_generator():
    rng = random.Random(53)
    specials = [0, 255, 128, 1, 127, 129, 254]
    for _ in range(200):
        cov, samples = AluCoverage(), []
        for _ in range(rng.randint(1, 60)):
            s = (rng.choice(OPS), rng.choice(specials + [rng.randrange(256)]), rng.choice(specials + [rng.randrange(256)]), rng.randrange(2))
            cov.sample(*s)
            samples.append(s)
        assert abs(cov.coverage() - float(q0053.coverage(samples))) < 1e-9


def test_closure_matches_the_exact_value():
    for d in q0053.DISTS:
        ps = cell_probs(DIST_F[d])
        assert all(abs(x - float(y)) < 1e-15 for x, y in zip(sorted(ps), sorted(q0053.cell_probs(d))))
        exact = float(q0053.expected_closure(q0053.cell_probs(d)))
        assert abs(expected_closure(ps) - exact) < 1e-6 * exact, d
    for n in (1, 5, 30):
        assert abs(expected_closure([1 / n] * n) - n * sum(1 / k for k in range(1, n + 1))) < 1e-6 * n


def test_closure_by_simulation():
    rng = random.Random(54)
    cells = q0053.CELLS
    pa = DIST_F["dist"]
    classes, weights = zip(*pa.items())
    runs, total = 600, 0
    for _ in range(runs):
        seen, n = set(), 0
        while len(seen) < len(cells):
            op, xa, xb = rng.choice(OPS), rng.choices(classes, weights)[0], rng.choices(classes, weights)[0]
            n += 1
            if not q0053.ignored(op, xa, xb):
                seen.add((op, xa, xb))
        total += n
    e = float(q0053.expected_closure(q0053.cell_probs("dist")))
    assert abs(total / runs - e) < 0.06 * e


def test_testbench_constants():
    tb = (ROOT / "tests" / "0053" / "tb.sv").read_text(encoding="utf-8")
    for d, name in (("uniform", "UNIFORM"), ("dist", "DIST"), ("equal", "EQUAL")):
        v = float(re.search(rf"localparam real {name} = ([0-9.]+);", tb).group(1))
        assert abs(v - float(q0053.expected_closure(q0053.cell_probs(d)))) < 1e-3, d


def test_explorer_matches_the_page_code():
    from page_tests import explorer_require, node_json

    rng = random.Random(55)
    seqs = [[(rng.randrange(5), rng.choice([0, 255, 128, rng.randrange(256)]), rng.choice([0, 255, 128, rng.randrange(256)]), rng.randrange(2)) for _ in range(rng.randint(1, 80))] for _ in range(40)]
    got = node_json(f"""
      const m = {explorer_require()};
      const S = {json.dumps(seqs)};
      console.log(JSON.stringify([
        S.map((seq) => {{ const st = m.cgNew(); seq.forEach(([o, a, b, c]) => m.cgSample(st, o, a, b, c)); return [m.cgCoverage(st, false), m.cgCoverage(st, true)]; }}),
        ["uniform", "dist", "equal"].map((d) => m.cgExpected(m.cgCellProbs(d))),
      ]));""")
    for seq, (cov, cov_all) in zip(seqs, got[0]):
        model = AluCoverage()
        for o, a, b, c in seq:
            model.sample(OPS[o], a, b, c)
        assert abs(cov - model.coverage()) < 1e-9
        # counting the ignored cells too: 80 cells in the cross, the 8 extra ones never closed by SHL alone
        hits = {(OPS[o], value_bin(a), value_bin(b)) for o, a, b, c in seq}
        sizes = dict(AluCoverage.SIZES, cross=80)
        want = 100 * (sum(len(model.hit[k]) / n for k, n in sizes.items() if k != "cross") + len(hits) / 80) / 5
        assert abs(cov_all - want) < 1e-9
    for d, e in zip(("uniform", "dist", "equal"), got[1]):
        exact = float(q0053.expected_closure(q0053.cell_probs(d)))
        assert abs(e - exact) < 1e-4 * exact, d


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(53)
