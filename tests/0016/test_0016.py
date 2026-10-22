"""Question 0016 has no code on the page; these tests check the closed forms for L = 2
(part a), L = 3 (part b) and any L (the bonus part) against an independent simulation, the
zero-point characterization, the base-3 digit rule of part b, and that the figures and
tables are the generator's output."""

import re
import subprocess
import sys

from extract_code import ROOT, question_path

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0016  # noqa: E402


def reference(n, L=2):
    """Plain list simulation of "one stays, L - 1 leave", written independently of the
    generator: the index of the one who stays, then L - 1 pops right after it."""
    people, i = list(range(n)), 0
    while len(people) > 1:
        for _ in range(L - 1):
            if len(people) == 1:
                break
            j = (i + 1) % len(people)
            people.pop(j)
            if j < i:
                i -= 1
        i = (i + 1) % len(people)
    return people[0]


def closed_form(n):
    top = 1 << (n.bit_length() - 1)
    return 2 * (n - top)


def closed_form_l(n, L):
    """F_L(N) = L (N - M) / (L - 1) with M = r L^floor(log_L(N / r)), r = 1 + (N - 1) mod (L - 1)."""
    r = 1 + (n - 1) % (L - 1)
    M = r
    while M * L <= n:
        M *= L
    assert (n - M) % (L - 1) == 0
    return L * (n - M) // (L - 1)


def recurrence(n, L=2):
    f = {m: 0 for m in range(1, L)}
    for m in range(L, n + 1):
        f[m] = (f[m - L + 1] + L) % m
    return f[n]


def base3(v):
    digits = ""
    while v:
        digits, v = str(v % 3) + digits, v // 3
    return digits or "0"


def test_page_examples():
    assert reference(5) == 2 and reference(20) == 8 and reference(41) == 18
    assert closed_form(20) == 8 and closed_form(41) == 18


def test_closed_form_against_simulation():
    for n in range(1, 4097):
        assert reference(n) == closed_form(n) == recurrence(n) == q0016.formula(n) == q0016.survivor(n), n
    assert all(closed_form(1 << m) == 0 for m in range(40))


def test_halving_and_odd_recurrences():
    for k in range(1, 600):
        assert closed_form(2 * k) == 2 * closed_form(k)
        assert closed_form(2 * k + 1) == 2 * closed_form(k) + 2


def test_binary_view():
    for n in range(1, 5000):
        b = f"{n:b}"
        assert closed_form(n) == int(b[1:] + "0", 2), n


def test_rounds_of_twenty():
    groups, win = q0016.rounds(20)
    assert win == 8
    assert [v for _, leave in groups[0] for v in leave] == list(range(1, 20, 2))
    assert [v for _, leave in groups[1] for v in leave] == [2, 6, 10, 14, 18]
    assert [v for _, leave in groups[2] for v in leave] == [4, 12, 0]
    assert [v for _, leave in groups[3] for v in leave] == [16]


def test_explorer_follow_ups():
    """The box's follow-ups: the linked-list survivor agrees with the step simulation for
    every L, and the seat lookup lists exactly the first circles where the seat survives."""
    from page_tests import explorer_require, node_json

    got = node_json(f"const m = {explorer_require()};"
                    "const out = { fast: [], seats: {} };"
                    "for (let n = 1; n <= 64; n++) for (const L of [2, 3, 4, 5, 6]) out.fast.push([n, L, m.josephusSurvivor(n, L), m.josephusSteps(n, L).survivor, m.josephusRun(n, L)]);"
                    "for (const L of [2, 3, 4]) out.seats[L] = [...Array(41).keys()].map((s) => m.josephusSeats(s, L, 4, 5000));"
                    "out.big = [m.josephusSurvivor(1000000, 2), m.josephusFormula(1000000, 2), m.josephusSurvivor(1000000, 3), m.josephusFormula(1000000, 3)];"
                    "console.log(JSON.stringify(out));")
    for n, L, fast, steps, run in got["fast"]:
        assert fast == steps == run == q0016.formula(n, L), (n, L)
    for L in (2, 3, 4):
        for s in range(41):
            want = [n for n in range(1, 5001) if q0016.formula(n, L) == s][:4]
            assert got["seats"][str(L)][s] == want, (L, s)
    big = got["big"]
    assert big[0] == big[1] == q0016.formula(1000000, 2) and big[2] == big[3] == q0016.formula(1000000, 3)


# --- part b: L = 3 -------------------------------------------------------------------------

def test_l3_page_examples():
    assert reference(7, 3) == 6 and reference(30, 3) == 18 and reference(10, 3) == 6
    assert closed_form_l(30, 3) == 18 and closed_form_l(20, 3) == 3 and closed_form_l(21, 3) == 18
    assert closed_form_l(20, 4) == 16 == reference(20, 4)


def test_l3_against_simulation():
    for n in range(1, 3001):
        assert reference(n, 3) == closed_form_l(n, 3) == recurrence(n, 3) == q0016.formula(n, 3), n
    # the zero points: 3^m and 2 * 3^m, nothing else
    zeros = {n for n in range(1, 3001) if closed_form_l(n, 3) == 0}
    assert zeros == {b * 3 ** m for b in (1, 2) for m in range(8) if b * 3 ** m <= 3000}


def test_l3_parity_chains():
    for M in (1, 2, 3, 6, 9, 18, 27, 54):
        for j in range(M):
            assert closed_form_l(M + 2 * j, 3) == 3 * j
        assert closed_form_l(3 * M, 3) == 0


def test_l3_base3_rule():
    """F_3(N) = 3 (floor(N/2) - floor(M/2)); floor(M/2) is 10..0 (N even, as long as
    floor(N/2)) or 11..1 (N odd, one digit shorter than N) in base 3; the page's examples."""
    for n in range(1, 2001):
        half, c, diff = q0016.half_rule(n)
        M = q0016.zero_below(n, 3)
        assert half == n // 2 and c == M // 2 and 3 * diff == closed_form_l(n, 3), n
        m = len(base3(n // 2 if n % 2 == 0 else n)) - 1
        if n % 2 == 0:
            assert c == 3 ** m and base3(c) == "1" + "0" * m, n
        else:
            assert c == (3 ** m - 1) // 2 and base3(c) == ("1" * m or "0"), n
        assert base3(3 * diff) == (base3(diff) + "0" if diff else "0")
    assert (q0016.half_rule(30), base3(15), base3(9), base3(6)) == ((15, 9, 6), "120", "100", "20")
    assert (q0016.half_rule(21), base3(10), base3(4), base3(6)) == ((10, 4, 6), "101", "11", "20")
    assert closed_form_l(30, 3) == closed_form_l(21, 3) == 18 and base3(18) == "200"


def test_rounds_of_thirty():
    groups, win = q0016.rounds(30, 3)
    assert win == 18
    assert [s for s, _ in groups[0]] == list(range(0, 30, 3))
    assert [v for _, leave in groups[1] for v in leave] == [3, 6, 12, 15, 21, 24, 0, 9]
    assert [v for _, leave in groups[2] for v in leave] == [27]


# --- the bonus part: any L -----------------------------------------------------------------

def test_any_l_against_simulation():
    for L in range(2, 8):
        for n in range(1, 1201):
            assert reference(n, L) == closed_form_l(n, L) == recurrence(n, L) == q0016.formula(n, L), (L, n)
        zeros = {n for n in range(1, 1201) if closed_form_l(n, L) == 0}
        assert zeros == {b * L ** m for b in range(1, L) for m in range(12) if b * L ** m <= 1200}, L


def test_l2_is_part_a():
    for n in range(1, 2049):
        assert closed_form_l(n, 2) == closed_form(n)


def test_josephus_rule_trap():
    """The trap: keep two, remove one (every third leaves) has the recurrence
    f(N) = (f(N - 1) + 3) mod N, and gives 30 for the 41 of the story."""
    def every_third(n):
        people, i = list(range(n)), 0
        while len(people) > 1:
            i = (i + 2) % len(people)
            people.pop(i)
        return people[0]

    f = 0
    for m in range(2, 42):
        f = (f + 3) % m
    assert f == every_third(41) == 30


def test_figures_up_to_date():
    out = subprocess.run([sys.executable, str(ROOT / "tools" / "figures" / "q0016.py")],
                         capture_output=True, text=True, check=True).stdout
    text = question_path(16).read_text(encoding="utf-8")
    for pattern in (r'<div class="stepper".*?</div></div>', r'<svg class="(?:figure|perf-chart)".*?</svg>',
                    r'<span class="viz-legend">.*?</span></span>'):
        generated = re.findall(pattern, out)
        assert generated and re.findall(pattern, text) == generated, pattern
    page_rows = [l.strip() for l in text.splitlines() if l.strip().startswith("|")]
    for row in (l for l in out.splitlines() if l.startswith("|")):
        assert row.strip() in page_rows, row


def test_explorer_matches_simulation():
    from page_tests import explorer_require, node_json

    got = node_json(f"const m = {explorer_require()}; const out = [];"
                    "for (let L = 2; L <= 6; L++) for (let n = 1; n <= 64; n++)"
                    " out.push([L, n, m.josephusRun(n, L), m.josephusFormula(n, L), m.josephusZero(n, L)]);"
                    "console.log(JSON.stringify(out));")
    for L, n, sim, form, zero in got:
        assert sim == form == reference(n, L) == closed_form_l(n, L), (L, n)
        assert zero == q0016.zero_below(n, L)


def test_explorer_steps_match_generator():
    """The step-by-step elimination of the explorer (who stays, who leaves, per step) is the
    generator's, for every N up to 64 and L = 2, 3, 4."""
    from page_tests import explorer_require, node_json

    got = node_json(f"const m = {explorer_require()};"
                    "const out = []; for (const L of [2, 3, 4]) for (let n = 1; n <= 64; n++) out.push([n, L, m.josephusSteps(n, L)]);"
                    "console.log(JSON.stringify(out));")
    for n, L, r in got:
        steps, win = q0016.run(n, L)
        assert r["survivor"] == win and [tuple(s) for s in r["steps"]] == [(a, list(b)) for a, b in steps] or \
            ([list(s) for s in r["steps"]] == [[a, list(b)] for a, b in steps] and r["survivor"] == win), (n, L)
        gone = [p for _, leave in r["steps"] for p in leave]
        assert len(gone) == n - 1 and len(set(gone)) == n - 1 and win not in gone
