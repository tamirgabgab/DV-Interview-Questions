"""Question 0105, HyperLogLog: the numbers the page states, recomputed from the references in
tools/figures/q0105.py (the single register's growth and its exact distribution, the estimates
of parts b and c, the small example, the small-range correction, the repeats, the merge of two
monitors, the memory of the exact count, of linear counting and of a Bloom filter), the error
of the estimate tested statistically over many seeded runs, the generated blocks, the constants
and the per-clock table the testbench checks, and the box's models under Node."""

import json
import math
import re
import sys
from fractions import Fraction

import pytest

from extract_code import ROOT
from page_tests import assert_figures_match, explorer_require, node_json

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0105  # noqa: E402

PAGE = next((ROOT / "docs" / "questions" / "senior").glob("0105-*.md")).read_text(encoding="utf-8")
TB = (ROOT / "tests" / "0105" / "tb.sv").read_text(encoding="utf-8")
# the prose without the generated blocks, its lines joined
PROSE = " ".join(re.sub(r"<!-- gen \d+ -->.*?<!-- /gen -->", "", PAGE, flags=re.S).split())


def says(*texts):
    for t in texts:
        assert t in PROSE, t


def test_figures_match():
    assert_figures_match(105)


def test_hash_and_streams():
    # the mixer is splitmix64's finalizer: a bijection, so distinct addresses never collide
    assert q0105.mix64(0) == 0xE220A8397B1DCDAF
    assert q0105.GOLD % 2 == 1
    s = q0105.stream("rand")
    assert len(set(s)) == q0105.N_BOX and all(a % 64 == 0 and a < 2**32 for a in s)
    assert len(set(q0105.stream("dup"))) == q0105.DUP_SET
    assert len(set(q0105.stream("seq"))) == q0105.N_BOX
    # the example address of the hash figures: rank 4 over 64 bits, register 1 and rank 4 with p = 4
    a = q0105.distinct(q0105.EXAMPLE_T)
    assert a == 877_363_008
    h = q0105.mix64(a)
    assert q0105.first_one(format(h, "064b")) == 4
    assert q0105.split(h, 4) == (1, 4) and format(h, "064b")[:4] == "0001"
    says("877,363,008", "‏0001, הם רגיסטר 1")
    # the rank of a zero hash is 65
    assert q0105.first_one("0" * 64) == 65
    says("ו-65 ל-hash שהוא 0")


def test_exact_count_memory():
    # a million 64-bit addresses in a set: 8,000,000 bytes before any overhead
    says("8,000,000 בתים")
    # the information bound: log2 C(2^64, n) bits, about 45.5 million for a million
    n = 10**6
    exact = sum(math.log2(2**64 - k) - math.log2(k + 1) for k in range(n))
    # 64 n - log2(n!) is the same to a millionth (2^64 is far larger than n)
    assert abs(64 * n - math.fsum(math.log2(k) for k in range(1, n + 1)) - exact) / exact < 1e-6
    assert round(exact / 1e6, 1) == 45.5 and round(exact / 8 / 2**20, 1) == 5.4 and round(exact / 8 / 1e6, 1) == 5.7
    says("כ-45.5 מיליון ביטים", "כ-5.7 MB")


def test_single_register():
    rows = q0105.grow_rows()
    assert [r for _, r, _ in rows] == [5, 7, 10, 13, 20, 20]
    # the exact distribution of the max rank over 1,000 random hashes sums to 1
    # the ranks 1..64 telescope to P(every rank <= 64)
    assert sum(q0105.single_dist(1000, r) for r in range(1, 65)) == (1 - Fraction(1, 2**64)) ** 1000
    p = {r: float(q0105.single_dist(1000, r)) for r in range(1, 14)}
    assert round(p[10] * 100, 1) == 23.5 and round(p[11] * 100, 1) == 23.7
    hi = 1 - (1 - Fraction(1, 2**13)) ** 1000
    tail = float(q0105.single_dist(1000, 13) + hi)
    assert round(tail * 100, 1) == 21.7
    says("ו-21.7% נותנים פי 8 או יותר", "רק כרבע מהמקרים נותנים את 1,024")
    assert abs(p[10] - 0.25) < 0.02


def test_estimates_and_small_example():
    rows = q0105.grow_rows()
    assert [round(e) for _, _, e in rows] == [10, 99, 1026, 10353, 106786, 992011]
    assert round(rows[4][2] / 100000 - 1, 3) == 0.068
    says("ב-100,000 השגיאה 6.8%")
    # 6.8% is more than twice the standard error of 1,024 registers
    assert 0.068 > 2 * q0105.std_error(1024)
    R = q0105.registers(q0105.stream("rand", q0105.SMALL_N), q0105.SMALL_P)
    assert R == [2, 4, 3, 1, 2, 4, 2, 3, 1, 4, 2, 4, 2, 3, 4, 2]
    e = q0105.raw_estimate(R)
    assert round(e, 1) == 54.3 and R.count(0) == 0 and e > 2.5 * 16 and q0105.estimate(R) == e
    assert round(e / 50 - 1, 3) == 0.085 and round(q0105.std_error(16), 2) == 0.26
    says("שגיאה של 8.5%, בתוך השגיאה התקנית של 16 רגיסטרים, 26%", "האומדן 54.3 גבוה מ-\\( 2.5m = 40 \\)")
    # alpha_m and the memory
    # the paper's constants for 16, 32 and 64 registers; the formula is within half a percent
    for m, paper in ((16, 0.673), (32, 0.697), (64, 0.709)):
        assert abs(q0105.alpha(m) / paper - 1) < 0.005
    assert round(q0105.alpha(1024) * 1024) == 738
    says("0.673", "0.697", "0.709", "כ-738 ל-1,024 רגיסטרים", "6,144 ביטים, 768 בתים")
    assert 1024 * 6 == 6144 and round(q0105.std_error(1024) * 100, 2) == 3.25
    says("3.25%")


def test_small_range_repeats_merge():
    raw, est, zeros = q0105.small_range_example()
    assert round(raw) == 784 and round(est, 1) == 98.6 and zeros == 930
    assert est == 1024 * math.log(1024 / 930)
    says("היא נותנת 784, והספירה הליניארית, עם 930 רגיסטרים ריקים, 98.6.")
    n, e = q0105.dup_example()
    assert n == 5000 and round(e) == 5115
    # the repeats change nothing: the same registers as the 5,000 distinct addresses alone
    s = [q0105.distinct(1 + (t * q0105.GOLD) % q0105.LINES % 5000) for t in range(1, 15001)]
    assert q0105.registers(s, 10) == q0105.registers(sorted(set(s)), 10)
    says("נותנות את האומדן 5,115")
    a, b, u, regs = q0105.merge_example()
    assert (round(a), round(b), round(u)) == (62702, 63234, 96382)
    assert regs == q0105.registers([q0105.distinct(t) for t in range(1, 90001)], 10)
    says("62,702", "63,234", "96,382", "30,001", "90,000")
    # the trap of the same bits for index and rank: 552 with 256 registers in the box
    assert round(q0105.box_series("rand", "same", 8)[-1][2]) == 552
    says("נותן 552 עם 256 רגיסטרים")


def test_other_structures():
    # linear counting alone at a million addresses and the error of 1,024 registers: about 109
    # thousand bits; its error sqrt(m (e^t - t - 1)) / n with t = n / m
    n, target = 10**6, q0105.std_error(1024)

    def err(m):
        t = n / m
        return math.sqrt(m * (math.exp(t) - t - 1)) / n

    lo, hi = 1000, 10**7
    while hi - lo > 1:
        mid = (lo + hi) // 2
        lo, hi = (lo, mid) if err(mid) <= target else (mid, hi)
    assert hi == 108926 and round(hi / 8 / 1000, 1) == 13.6
    says("כ-109 אלף ביטים, כ-13.6 KB")
    # a Bloom filter at 1%: -ln(0.01) / ln(2)^2 bits per element
    per = -math.log(0.01) / math.log(2) ** 2
    assert round(per, 1) == 9.6 and round(per * n / 8 / 1e6, 1) == 1.2
    says("כ-9.6 ביטים לכל כתובת")


def test_statistics():
    rows = q0105.error_rows()
    assert [p for p, *_ in rows] == [4, 6, 8, 10]
    for p, rms, arms, amax, out in rows:
        se = q0105.std_error(1 << p)
        # the rms over 200 runs within 15% of 1.04 / sqrt(m); at most 10% of runs outside 2 sigma
        assert abs(rms / se - 1) < 0.15, (p, rms, se)
        assert out <= q0105.RUNS // 10, (p, out)
        # the arithmetic mean is far worse
        assert arms > 10 * rms
    assert [round(r * 100, 2) for _, r, *_ in rows] == [28.34, 12.21, 6.77, 2.92]
    assert [o for *_, o in rows] == [14, 5, 10, 6]
    p10 = rows[-1]
    assert round(p10[2] * 100) == 2729 and p10[3] > 300
    says("2,729%", "2.92%", "יותר מפי 300")


def test_tb_constants():
    grow_r = [int(x) for x in re.search(r"int grow_r\[6\] = '\{([^}]*)\}", TB).group(1).split(",")]
    grow_e = [float(x) for x in re.search(r"real grow_e\[6\] = '\{([^}]*)\}", TB).group(1).split(",")]
    rows = q0105.grow_rows()
    assert grow_r == [r for _, r, _ in rows]
    assert grow_e == [e for _, _, e in rows]
    _, e = q0105.dup_example()
    assert repr(e) in TB
    raw, est, zeros = q0105.small_range_example()
    assert repr(est) in TB and f"n != {zeros}" in TB
    a, b, u, _ = q0105.merge_example()
    assert repr(a) in TB and repr(b) in TB and repr(u) in TB
    assert repr(q0105.grow_rows()[4][2]) in TB


def test_pipe_trace_matches_tb():
    good, bad = q0105.pipe_rows(True), q0105.pipe_rows(False)
    j = q0105.PIPE_J
    want = []
    for (a, st2, st3, R), (_, _, _, Rb) in zip(good, bad):
        want.append(f"{int(a is not None)} {int(st2 is not None)} {int(st3 is not None)} {R[j]} {Rb[j]}")
    got = re.search(r"string want_trace\[6\] = '\{([^}]*)\}", TB).group(1)
    assert [x.strip().strip('"') for x in got.split(",")] == want
    ins = [int(x) for x in re.search(r"longint pipe_in\[4\] = '\{([^}]*)\}", TB).group(1).split(",")]
    assert ins == [-1 if x is None else x for x in q0105.PIPE_IN]
    assert j == 12 and [q0105.split(q0105.mix64(x), 4)[1] for x in (q0105.PIPE_A, q0105.PIPE_B, q0105.PIPE_C)] == [4, 1, 2]
    # with forwarding register 12 ends at 4, without it B's write of 1 wins and C gives 2
    assert good[-1][3][j] == 4 and bad[-1][3][j] == 2


@pytest.fixture(scope="module")
def box():
    script = f"""
      const m = {explorer_require()};
      const out = {{}};
      for (const s of ["rand", "dup", "seq"]) for (const k of ["mix", "ident", "same"]) for (const p of [4, 6, 8, 10])
        out[`${{s}} ${{k}} ${{p}}`] = m.hllSeries(s, k, p).map((x) => [x.t, x.distinct, x.est, x.single, x.regs, x.changed, x.raw, x.zeros, x.linear]);
      const addrs = [0, 64, 877363008, 1984, 1280, 1472, 4294967232, 2147483712];
      const splits = [];
      for (const a of addrs) for (const p of [0, 4, 6, 8, 10]) for (const k of ["mix", "ident", "same"]) splits.push(m.hllSplit(m.hllHash(a, k), p, k));
      const lv = [];
      for (let vmax = 1; vmax <= 30; vmax++) for (let v = 0; v <= vmax; v++) lv.push(m.hllLevel(v, vmax));
      console.log(JSON.stringify({{ out, mix: addrs.map((a) => m.hllMix(BigInt(a)).toString()), splits, lv,
        cps: m.hllCheckpoints, alpha: [16, 64, 256, 1024].map((x) => m.hllAlpha(x)),
        streams: ["rand", "dup", "seq"].map((s) => m.hllStream(s).slice(0, 50).concat(m.hllStream(s).slice(-50))) }}));
    """
    return node_json(script)


def test_box_models(box):
    assert box["cps"] == q0105.CHECKPOINTS
    assert box["alpha"] == [q0105.alpha(m) for m in (16, 64, 256, 1024)]
    addrs = [0, 64, 877363008, 1984, 1280, 1472, 4294967232, 2147483712]
    assert box["mix"] == [str(q0105.mix64(a)) for a in addrs]
    want = [list(q0105.split(q0105.hash_of(a, k), p, k)) for a in addrs for p in (0, 4, 6, 8, 10) for k in ("mix", "ident", "same")]
    assert box["splits"] == want
    assert box["lv"] == [q0105.level(v, vmax) for vmax in range(1, 31) for v in range(vmax + 1)]
    for s, got in zip(("rand", "dup", "seq"), box["streams"]):
        full = q0105.stream(s)
        assert got == full[:50] + full[-50:]


@pytest.mark.parametrize("name", ["rand", "dup", "seq"])
def test_box_series(box, name):
    for kind in ("mix", "ident", "same"):
        for p in (4, 6, 8, 10):
            ref = q0105.box_series(name, kind, p)
            got = box["out"][f"{name} {kind} {p}"]
            assert len(got) == len(ref)
            prev = [0] * (1 << p)
            for (t, d, est, r1, regs), (gt, gd, gest, gr1, gregs, changed, raw, zeros, linear) in zip(ref, got):
                assert (gt, gd, gr1) == (t, d, r1)
                assert gregs == regs                                   # bit-exact registers
                assert abs(gest - est) <= 1e-12 * max(1, est)
                assert abs(raw - q0105.raw_estimate(regs)) <= 1e-12 * raw
                assert zeros == regs.count(0) and linear == (est != q0105.raw_estimate(regs))
                assert changed == [j for j in range(1 << p) if regs[j] != prev[j]]
                prev = regs
    # the box's last states that the page quotes
    if name == "rand":
        finals = [round(box["out"][f"rand mix {p}"][-1][2]) for p in (4, 6, 8, 10)]
        assert finals == [14153, 16255, 19383, 19836]
    if name == "seq":
        # the address itself as the hash: every sequential address lands in one register
        assert all(round(box["out"][f"seq ident {p}"][-1][2]) == 1 for p in (4, 6, 8, 10))


def test_tight_tolerance_fails_a_third():
    # trap 6: a check of |E - n| / n < 3% on one run fails in about a third of the correct runs
    bad = 0
    for k in range(q0105.RUNS):
        R = q0105.registers([q0105.distinct(t) for t in range(k * q0105.RUN_N + 1, (k + 1) * q0105.RUN_N + 1)], 10)
        bad += abs(q0105.estimate(R) / q0105.RUN_N - 1) > 0.03
    assert bad == 65 and 0.3 < bad / q0105.RUNS < 0.37
    says("תיכשל בכשליש מהריצות")
