"""Question 0094: the credit counter as a random walk.

Every number the page states is recomputed here with exact fractions (the parts, the tables
of the generator, the traps and the follow-ups); the generator's formulas agree with the
page's code; the generated blocks are up to date; and the creditwalk box's models are
compared under Node with the exact formulas and with a Python copy of its seeded runs."""

import math
import re
import sys
from fractions import Fraction as Fr

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0094  # noqa: E402

ns = load_python(94)
walk_odds = ns["walk_odds"]
PAGE = (ROOT / "docs" / "questions" / "junior" / "0094-credit-counter-random-walk.md").read_text(encoding="utf-8")


def test_generator_matches_the_page_code():
    for N in (3, 10, 21):
        for p, q in [(Fr(1, 2), Fr(1, 2)), (Fr(3, 5), Fr(2, 5)), (Fr(3, 10), Fr(1, 5)), (Fr(1, 20), Fr(9, 10))]:
            for k in range(N + 1):
                assert q0094.odds(k, N, p, q) == walk_odds(k, N, p, q)
    assert q0094.rates(Fr(1, 2), Fr(1, 4)) == ns["rates_to_steps"](Fr(1, 2), Fr(1, 4))


def test_the_runs_of_the_figure():
    full, empty = q0094.fair_run(q0094.RUN_FULL), q0094.fair_run(q0094.RUN_EMPTY)
    assert full[0] == empty[0] == 3 and full[-1] == 10 and empty[-1] == 0
    assert all(abs(a - b) == 1 for path in (full, empty) for a, b in zip(path, path[1:]))
    assert all(0 < v < 10 for v in full[:-1] + empty[:-1])
    assert (len(full) - 1, len(empty) - 1) == (29, 11)
    assert "אחרי 29 מחזורים" in PAGE and "אחרי 11 מחזורים" in PAGE


def test_page_numbers():
    nums = {
        "3/10": Fr(3, 10), "7/10": Fr(7, 10),
        "41553/58025": walk_odds(3, 10, Fr(3, 5), Fr(2, 5))[0],
        "48291/2321": walk_odds(3, 10, Fr(3, 5), Fr(2, 5))[2],
        "96582/2321": walk_odds(3, 10, Fr(3, 10), Fr(1, 5))[2],
        "28431/29524": walk_odds(3, 10, Fr(3, 8), Fr(1, 8))[0],
        "195738/7381": walk_odds(3, 10, Fr(3, 8), Fr(1, 8))[2],
    }
    for text, v in nums.items():
        assert text in PAGE
        a, b = map(int, text.split("/"))
        assert Fr(a, b) == v
    assert walk_odds(3, 10, Fr(1, 2), Fr(1, 2))[2] == 21
    # the rounded values in the text
    assert f"{float(nums['41553/58025']):.3f}" == "0.716" and f"{float(1 - nums['41553/58025']):.3f}" == "0.284"
    assert f"{float(nums['48291/2321']):.2f}" == "20.81" and f"{float(nums['96582/2321']):.2f}" == "41.61"
    assert f"{float(nums['28431/29524']):.3f}" == "0.963" and f"{float(1 - nums['28431/29524']):.3f}" == "0.037"
    assert f"{float(nums['195738/7381']):.2f}" == "26.52"
    # part a's sum: E(10) = 10c - 2 * 45 = 0 gives c = 9, and sum_{j<=k} (9 - 2(j - 1)) = k(10 - k)
    for k in range(11):
        assert sum(9 - 2 * (j - 1) for j in range(1, k + 1)) == 9 * k - k * (k - 1) == k * (10 - k)
    # the longest mean time from 3 among the rows of part b's table is at p = 0.55, 22.25
    rows = {p: walk_odds(3, 10, p, 1 - p)[2] for p in q0094.P_ROWS}
    best = max(rows, key=rows.get)
    assert best == Fr(11, 20) and f"{float(rows[best]):.2f}" == "22.25" and "22.25" in PAGE
    # over every p the maximum is a little before 0.55: about 22.27, near p = 0.545
    scan = {Fr(i, 4000): walk_odds(3, 10, Fr(i, 4000), 1 - Fr(i, 4000))[2] for i in range(2000, 2400)}
    top = max(scan, key=scan.get)
    assert f"{float(scan[top]):.2f}" == "22.27" and abs(float(top) - 0.545) < 0.001
    assert scan[top] > rows[Fr(11, 20)] and "כ-22.27" in PAGE and "p = 0.545" in PAGE
    # part d, equal rates of 1/2: 21 / 0.5 = 42
    assert walk_odds(3, 10, Fr(1, 4), Fr(1, 4))[2] == 42 and "= 42" in PAGE


def test_proof_steps():
    # the particular solution k/(q - p) of E(k) = 1 + pE(k+1) + qE(k-1)
    for p in (Fr(3, 5), Fr(1, 3), Fr(9, 10)):
        q = 1 - p
        for k in range(1, 9):
            E = lambda x: Fr(x) / (q - p)     # noqa: E731
            assert E(k) == 1 + p * E(k + 1) + q * E(k - 1)
    # the sums form of P(k) and its limit k/N
    for rho in (Fr(2, 3), Fr(3, 2), Fr(99, 100), Fr(101, 100)):
        for k in range(11):
            closed = (1 - rho ** k) / (1 - rho ** 10)
            assert closed == sum(rho ** j for j in range(k)) / sum(rho ** j for j in range(10))
    near = walk_odds(3, 10, Fr(500001, 1000000), Fr(499999, 1000000))
    assert abs(float(near[0]) - 0.3) < 1e-4 and abs(float(near[2]) - 21) < 1e-3
    # the form against overflow: (rho^-N - rho^(k-N)) / (rho^-N - 1)
    for rho in (Fr(3, 2), Fr(5, 2)):
        for k in range(11):
            assert (rho ** -10 - rho ** (k - 10)) / (rho ** -10 - 1) == (1 - rho ** k) / (1 - rho ** 10)


def page_floats(k, n, p, q, divide=True):
    """p_full and mean_cycles of the page's SystemVerilog, in IEEE doubles as `real` is: a
    power that overflows is infinite (Python raises instead), and with divide=False p_full
    uses the plain form for every rho."""
    def pw(x, e):
        try:
            return x ** e
        except OverflowError:
            return math.inf
    a, b = p / (p + q), q / (p + q)
    rho = b / a
    if rho < 1.0 or not divide:
        full = (1.0 - pw(rho, k)) / (1.0 - pw(rho, n))
    else:
        full = (pw(rho, -n) - pw(rho, k - n)) / (pw(rho, -n) - 1.0)
    return full, (k - n * full) / (b - a) / (p + q)


def test_traps_and_follow_ups():
    # the near-fair trap: at p = 0.5 + 1e-8 the float P is right to nine digits, E is 21.05
    p = 0.5 + 1e-8
    full, cycles = page_floats(3, 10, p, 1 - p)
    F, _, C = walk_odds(3, 10, Fr(p), Fr(1 - p))
    assert abs(full - float(F)) / float(F) < 1e-9 and f"{cycles:.2f}" == "21.05" and f"{float(C):.2f}" == "21.00"
    assert "21.05 במקום 21.00" in PAGE and "10^{-8}" in PAGE
    # the overflow trap: from 1990 with N = 2000 and p = 0.4 the plain form gives NaN, the
    # divided form (the page's p_full) 0.0173
    assert math.isnan(page_floats(1990, 2000, 0.4, 0.6, divide=False)[0])
    got = page_floats(1990, 2000, 0.4, 0.6)[0]
    assert math.isclose(got, float(walk_odds(1990, 2000, Fr(2, 5), Fr(3, 5))[0]), rel_tol=1e-12)
    assert f"{got:.4f}" == "0.0173" and "NaN במקום 0.0173" in PAGE
    # trap: p = lambda1 and q = lambda2 sum to 1.7; the right split
    assert Fr(9, 10) + Fr(8, 10) == Fr(17, 10)
    p, q = ns["rates_to_steps"](Fr(9, 10), Fr(4, 5))
    assert (p, q, 1 - p - q) == (Fr(18, 100), Fr(8, 100), Fr(74, 100))
    # no upper wall: 1 - (q/p)^k, the limit of P(full) as N grows
    assert 1 - Fr(2, 3) ** 3 == Fr(19, 27) and f"{19 / 27:.2f}" == "0.70"
    for N in (40, 80):
        assert abs(float(walk_odds(3, N, Fr(3, 5), Fr(2, 5))[0]) - 19 / 27) < (2 / 3) ** N
    # a wall that keeps the counter: E(k) = k(2N + 1 - k), 54 from 3 with N = 10
    sys.path.insert(0, str(ROOT / "tests" / "0094"))
    from test_0094_code import chain
    for N in (1, 2, 5, 10):
        _, cycles = chain(N, Fr(1, 2), Fr(1, 2), upper="reflect")
        for k in range(1, N + 1):
            assert cycles[k] == k * (2 * N + 1 - k)
    assert 3 * (2 * 10 + 1 - 3) == 54
    # the chance to end within 21 cycles in part a: about 0.65
    d, done = {3: Fr(1)}, Fr(0)
    for _ in range(21):
        nd = {}
        for k, v in d.items():
            for kk in (k - 1, k + 1):
                nd[kk] = nd.get(kk, 0) + v / 2
        done += nd.pop(0, 0) + nd.pop(10, 0)
        d = nd
    assert f"{float(done):.2f}" == "0.65" and "בערך 0.65" in PAGE


def test_box_tasks():
    """The numbers the "נסו" paragraphs ask the reader to see in the boxes."""
    def show(k, N, p, q):
        f, _, c = walk_odds(k, N, p, q)
        return f"{float(f):.3f}", f"{float(c):.2f}"
    assert show(3, 10, Fr(11, 20), Fr(9, 20)) == ("0.523", "22.25")
    assert show(3, 10, Fr(3, 5), Fr(2, 5)) == ("0.716", "20.81")
    assert show(10, 20, Fr(1, 2), Fr(1, 2)) == ("0.500", "100.00") and 10 * (20 - 10) == 100
    assert show(3, 10, *q0094.rates(Fr(1, 2), Fr(1, 4))) == ("0.963", "26.52")
    assert show(3, 10, *q0094.rates(Fr(1, 2), Fr(1, 2))) == ("0.300", "42.00")
    assert show(3, 10, *q0094.rates(Fr(1, 10), Fr(1, 10))) == ("0.300", "116.67")
    assert 21 / (2 * Fr(1, 10) * Fr(9, 10)) == Fr(350, 3)
    p, q = q0094.rates(Fr(9, 10), Fr(4, 5))
    assert (f"{float(p):.3f}", f"{float(q):.3f}", f"{float(1 - p - q):.3f}") == ("0.180", "0.080", "0.740")
    assert show(3, 10, p, q) == ("0.912", "61.25")
    for text in ("ל-0.523 ול-0.716", "ל-22.25 ורק אז", "ל-20.81", "הסיכוי 0.500 והזמן 100", "כ-0.963",
                 "קרוב ל-26.5", "מ-42 ל-116.67", "\\( p = 0.180 \\)", "0.912 ו-61.25"):
        assert text in PAGE, text


def test_per_clock_table():
    """The table under part d's code: the generator's model of credit_counter, the cases it
    shows, and the same rows in the testbench, which drives the page's module through them."""
    rows = q0094.counter_trace()
    assert [r[2] for r in rows] == [4, 4, 3, 3, 2, 1, 0, 0]
    assert rows[1][:2] == (1, 1) and rows[1][2] == rows[0][2]          # both at once: no change
    assert rows[3][:2] == (0, 0) and rows[3][2] == rows[2][2]          # neither
    assert rows[6][4] == 1 and rows[7][:2] == (1, 0) and rows[7][2] == 0   # empty, then frozen
    tb = (ROOT / "tests" / "0094" / "tb.sv").read_text(encoding="utf-8")
    arr = {name: [int(v) for v in re.search(rf"{name}\[8\]\s*=\s*'\{{([^}}]*)\}}", tb).group(1).split(",")]
           for name in ("TRET", "TTAKE", "TCOUNT", "TFULL", "TEMPTY")}
    assert list(zip(arr["TRET"], arr["TTAKE"], arr["TCOUNT"], arr["TFULL"], arr["TEMPTY"])) == rows


def test_page_skeleton():
    assert PAGE.count('data-kind="creditwalk"') == 2
    for m in re.finditer(r'<div class="explorer" data-kind="creditwalk" ([^>]*)>', PAGE):
        attrs = dict(re.findall(r'data-([a-z]+)="([^"]*)"', m.group(1)))
        assert attrs["mode"] in ("pq", "rates") and attrs["n"] == "10" and attrs["k"] == "3"


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(94)


def mulberry32(seed):
    a = seed & 0xFFFFFFFF

    def rnd():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = ((a ^ (a >> 15)) * (1 | a)) & 0xFFFFFFFF
        t = (t + (((t ^ (t >> 7)) * (61 | t)) & 0xFFFFFFFF)) & 0xFFFFFFFF ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return rnd


def py_run(seed, mode, a, b, k, N):
    rnd, path = mulberry32(seed), [k]
    while 0 < path[-1] < N:
        if mode == "rates":
            back, used = rnd() < a, rnd() < b
            step = int(back) - int(used)
        else:
            p, q = (a, 1 - a) if mode == "pq" else (a, b)
            u = rnd()
            step = 1 if u < p else -1 if u < p + q else 0
        path.append(path[-1] + step)
    return path


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    cases = [("pq", 0.5, 0.5), ("pq", 0.6, 0.4), ("pqr", 0.3, 0.2), ("pqr", 0.05, 0.9), ("rates", 0.5, 0.25),
             ("rates", 0.9, 0.8), ("rates", 0.4, 0.4)]
    runs = [(1, "pq", 0.5, 0.5, 3, 10), (94, "pqr", 0.3, 0.2, 3, 10), (7, "rates", 0.5, 0.25, 3, 10),
            (12, "rates", 0.35, 0.6, 5, 12), (3, "pq", 0.45, 0.55, 1, 2)]
    got = node_json(f"const m = {explorer_require()};"
                    f"const cases = {[list(c) for c in cases]};"
                    f"const runs = {[list(r) for r in runs]};"
                    "console.log(JSON.stringify({"
                    "steps: cases.map(([mo, a, b]) => m.cwSteps(mo, a, b)),"
                    "odds: cases.map(([mo, a, b]) => { const s = m.cwSteps(mo, a, b); return [3, 1, 9, 0, 10].map((k) => m.cwOdds(k, 10, s.p, s.q)); }),"
                    "big: [m.cwOdds(3, 300, 0.4, 0.6), m.cwOdds(297, 300, 0.6, 0.4)],"
                    "curves: m.cwCurves(10, 0.6, 0.4),"
                    "runs: runs.map(([s, mo, a, b, k, n]) => m.cwRun(s, mo, a, b, k, n)),"
                    "}));")
    for (mode, a, b), st, odds in zip(cases, got["steps"], got["odds"]):
        if mode == "rates":
            p, q = q0094.rates(Fr(a), Fr(b))
        elif mode == "pqr":
            p, q = Fr(a), Fr(b)
        else:
            p, q = Fr(a), 1 - Fr(a)
        assert math.isclose(st["p"], float(p)) and math.isclose(st["q"], float(q))
        for k, o in zip([3, 1, 9, 0, 10], odds):
            f, e, c = q0094.odds(k, 10, p, q)
            assert math.isclose(o["full"], float(f), abs_tol=1e-12) and math.isclose(o["empty"], float(e), abs_tol=1e-12)
            assert math.isclose(o["cycles"], float(c), rel_tol=1e-9, abs_tol=1e-9)
    # large N: no overflow, the same numbers as the exact formula
    f1, _, c1 = q0094.odds(3, 300, Fr(2, 5), Fr(3, 5))
    assert math.isclose(got["big"][0]["full"], float(f1), abs_tol=1e-15) and math.isclose(got["big"][0]["cycles"], float(c1), rel_tol=1e-9)
    f2, _, c2 = q0094.odds(297, 300, Fr(3, 5), Fr(2, 5))
    assert math.isclose(got["big"][1]["full"], float(f2), rel_tol=1e-12) and math.isclose(got["big"][1]["cycles"], float(c2), rel_tol=1e-9)
    for k in range(11):
        f, _, c = q0094.odds(k, 10, Fr(3, 5), Fr(2, 5))
        assert math.isclose(got["curves"]["full"][k], float(f), abs_tol=1e-12)
        assert math.isclose(got["curves"]["cycles"][k], float(c), rel_tol=1e-9, abs_tol=1e-9)
    for (seed, mode, a, b, k, n), path in zip(runs, got["runs"]):
        assert path == py_run(seed, mode, a, b, k, n)
        assert path[-1] in (0, n) and all(0 < v < n for v in path[:-1])
