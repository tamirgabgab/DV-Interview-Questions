"""Question 0016 has no code on the page; these tests check the closed form against an
independent simulation and that the figures and tables are the generator's output."""

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


def recurrence(n):
    f = 0
    for m in range(2, n + 1):
        f = (f + 2) % m
    return f


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
    """The box's follow-ups: the general keep / remove rule agrees with the page's steps
    for keep 1, Josephus's own rule (keep 2, remove 1) agrees with a plain "every third
    leaves" simulation and with the recurrence, the linked-list survivor agrees with the
    list simulation, and the seat lookup lists exactly the first circles where the seat
    survives."""
    from page_tests import explorer_require, node_json

    def every_third(n):
        people, i = list(range(n)), 0
        while len(people) > 1:
            i = (i + 2) % len(people)
            people.pop(i)
        return people[0]

    def recurrence(n):
        f = 0
        for m in range(2, n + 1):
            f = (f + 3) % m
        return f

    got = node_json(f"const m = {explorer_require()};"
                    "const out = { kr: [], jos: [], fast: [], seats2: [], seats3: [], seatsJ: [] };"
                    "for (let n = 1; n <= 64; n++) { for (const L of [2, 3, 4]) out.kr.push([n, L, m.josephusKR(n, 1, L - 1), m.josephusSteps(n, L)]);"
                    "  out.jos.push([m.josephusKR(n, 2, 1).survivor, m.josephusSurvivor(n, 2, 1), m.josephusRecurrence(n)]);"
                    "  out.fast.push([m.josephusSurvivor(n, 1, 1), m.josephusSurvivor(n, 1, 2), m.josephusRun(n, 2), m.josephusRun(n, 3)]); }"
                    "for (let s = 0; s <= 40; s++) { out.seats2.push(m.josephusSeats(s, 2, 4, 5000)); out.seats3.push(m.josephusSeats(s, 3, 4, 5000)); out.seatsJ.push(m.josephusSeats(s, null, 4, 5000)); }"
                    "out.big = [m.josephusSurvivor(1000000, 1, 1), m.josephusFormula(1000000, 2), m.josephusSurvivor(1000000, 2, 1), m.josephusRecurrence(1000000), m.josephusRecurrence(41)];"
                    "console.log(JSON.stringify(out));")
    for n, L, kr, steps in got["kr"]:
        assert kr["survivor"] == steps["survivor"] and [[[a], b] for a, b in steps["steps"]] == kr["steps"], (n, L)
    for n, (sim, fast, rec) in enumerate(got["jos"], 1):
        assert sim == fast == rec == every_third(n) == recurrence(n), n
    for n, (f2, f3, r2, r3) in enumerate(got["fast"], 1):
        assert f2 == r2 == q0016.formula(n, 2) and f3 == r3 == q0016.formula(n, 3), n
    for s in range(41):
        want2 = [n for n in range(1, 5001) if q0016.formula(n, 2) == s][:4]
        want3 = [n for n in range(1, 5001) if q0016.formula(n, 3) == s][:4]
        wantj = [n for n in range(1, 5001) if recurrence(n) == s][:4]
        assert got["seats2"][s] == want2 and got["seats3"][s] == want3 and got["seatsJ"][s] == wantj, s
    big = got["big"]
    assert big[0] == big[1] == q0016.formula(1000000, 2) and big[2] == big[3] and big[4] == 30


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

    got = node_json(f"const m = {explorer_require()};"
                    "console.log(JSON.stringify([...Array(64).keys()].map((i) => "
                    "[m.josephusRun(i + 1, 2), m.josephusFormula(i + 1, 2)])));")
    for n, (sim, form) in enumerate(got, 1):
        assert sim == form == reference(n, 2) == q0016.formula(n, 2), n


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
