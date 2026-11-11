import itertools
import random

from extract_code import load_python

ns = load_python(8)
cannot_win = ns["israel_cannot_win"]
earliest = ns["earliest_certain_loss"]

ABOVE_2026 = [("Poland", 133, 17), ("Italy", 134, 147), ("Finland", 141, 138),
              ("France", 144, 14), ("Denmark", 165, 78), ("Australia", 165, 122),
              ("Bulgaria", 204, 312)]


def test_page_example():
    assert not cannot_win(343, [133, 134, 141, 144, 165, 165, 204], 828)
    assert not cannot_win(343, [165, 165, 204], 495)       # exactly fills every cup
    assert cannot_win(343, [165, 165, 204], 512)
    assert cannot_win(343, [344], 0)                       # already ahead
    assert not cannot_win(343, [], 0)
    assert earliest(343, ABOVE_2026, 828) == 4             # France
    # The order between Denmark and Australia (165 each) does not change the answer
    swapped = ABOVE_2026[:4] + [ABOVE_2026[5], ABOVE_2026[4], ABOVE_2026[6]]
    assert earliest(343, swapped, 828) == 4


def can_still_win_brute(israel_total, jury, left):
    """Try every way to split `left` points among the countries (small inputs only)."""
    for split in itertools.product(range(left + 1), repeat=len(jury)):
        if sum(split) == left and all(j + p <= israel_total for j, p in zip(jury, split)):
            return True
    return not jury and left == 0


def test_check_matches_brute_force():
    rng = random.Random(8)
    for _ in range(400):
        israel_total = rng.randint(0, 8)
        jury = [rng.randint(0, 10) for _ in range(rng.randint(0, 3))]
        left = rng.randint(0, 9)
        assert cannot_win(israel_total, jury, left) == (not can_still_win_brute(israel_total, jury, left))


def earliest_reference(israel_total, above, points_left):
    """Call the check again after every announcement: O(k^2), obviously right."""
    for k in range(len(above) + 1):
        left = points_left - sum(p for _, _, p in above[:k])
        passed = any(j + p > israel_total for _, j, p in above[:k])
        if passed or cannot_win(israel_total, [j for _, j, _ in above[k:]], left):
            return k
    return None


def test_scan_matches_reference():
    rng = random.Random(80)
    for _ in range(3000):
        israel_total = rng.randint(50, 400)
        above = [(f"c{i}", rng.randint(0, israel_total + 20), rng.randint(0, 300))
                 for i in range(rng.randint(0, 8))]
        points_left = sum(p for _, _, p in above)
        assert earliest(israel_total, above, points_left) == earliest_reference(israel_total, above, points_left)


def test_explorer_matches_page_code():
    """The Eurovision explorer: its scan rows against the generator's steps() and the
    page's earliest_certain_loss, its check against israel_cannot_win on random inputs,
    and the what-if box against the page functions on the changed results."""
    import json
    import sys

    from extract_code import ROOT
    from page_tests import explorer_require, node_json

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import q0008

    rng = random.Random(8)
    checks = [[rng.randint(100, 400), [rng.randint(0, 420) for _ in range(rng.randint(0, 8))], rng.randint(0, 2088)] for _ in range(300)]
    whatif = [[123, 220], [123, 400], [300, 220], [0, 0], [204, 312], [150, 100], [140, 220], [165, 220],
              [250, 220], [123, 160], [123, 172], [123, 300], [123, 393], [123, 225], [123, 226], [123, 279], [145, 220]]
    whatif += [[rng.randint(0, 420), rng.randint(0, 432)] for _ in range(300)]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({{
        order: m.euroOrder(m.EURO_RESULTS), scan: m.euroScan(m.EURO_RESULTS),
        checks: {json.dumps(checks)}.map(([t, j, l]) => m.euroCannotWin(t, j, l)),
        whatif: {json.dumps(whatif)}.map(([j, p]) => {{ const s = m.euroScan(m.euroWithIsrael(j, p)); return [s.first, s.total, s.rows.map((r) => [r.country, r.left, r.room, r.lost]), s.ahead]; }}),
      }}));""")
    assert [tuple(r) for r in got["order"]] == q0008.ORDER
    sc = got["scan"]
    assert [(r["country"], r["left"], r["room"], r["lost"]) for r in sc["rows"]] == q0008.steps()
    assert sc["first"] == 4 == ns["earliest_certain_loss"](343, ABOVE_2026, 828) and sc["total"] == 343
    for (t, j, l), got_c in zip(checks, got["checks"]):
        assert got_c == ns["israel_cannot_win"](t, j, l)
    firsts = {}
    for (jury, pub), (first, total, rows, ahead) in zip(whatif, got["whatif"]):
        results = [("Israel", jury, pub) if c == "Israel" else (c, j, p) for c, j, p in q0008.RESULTS]
        order = sorted(results, key=lambda r: (r[1], r[0] == "Australia"))
        idx = next(i for i, r in enumerate(order) if r[0] == "Israel")
        above = order[idx + 1:]
        # the other countries keep their real public points: the points left after Israel
        # are theirs, and they end at 0 after the last announcement
        left = sum(r[2] for r in above)
        assert rows[-1][1] == 0 and rows[0][1] == left, (jury, pub)
        # earliest_certain_loss assumes nobody announced before Israel is ahead of it
        before = [(c, j + p) for c, j, p in order[:idx] if j + p > jury + pub or (j + p == jury + pub and p > pub)]
        want = 0 if before else ns["earliest_certain_loss"](jury + pub, above, left)
        assert total == jury + pub and first == (-1 if want is None else want), (jury, pub)
        assert (ahead is not None) == bool(before), (jury, pub)
        if before:
            assert (ahead["country"], ahead["total"]) == max(before, key=lambda b: b[1])
        assert [r[0] for r in rows] == ["Israel"] + [c for c, _, _ in above]
        firsts[(jury, pub)] = first
    # the cases the page's box tasks and the review name
    assert firsts[(250, 220)] == 0 and firsts[(123, 160)] == 0 and firsts[(123, 172)] == 0   # Bulgaria 516, Romania 296
    assert firsts[(123, 225)] == 4 and firsts[(123, 226)] == 5 and firsts[(123, 279)] == 6    # France, Denmark, Australia
    assert firsts[(123, 393)] == -1 and firsts[(145, 220)] == 1                               # a win by the tie-break; Denmark


def test_explorer_pouring():
    """The proof panel of the box: after every announcement the points left poured into the
    cups still to come, each to Israel's total; the spill is positive exactly when the
    page's israel_cannot_win says so for a country still below Israel (17 after France),
    and a part of the points (the animation) never overfills a cup."""
    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify([0, 1, 2, 3, 4, 5, 6, 7].map((k) => [m.euroPour(m.EURO_RESULTS, k), m.euroPour(m.EURO_RESULTS, k, 0.5)])));""")
    left = 828
    for k, (full, half) in enumerate(got):
        if k:
            left -= ABOVE_2026[k - 1][2]
        rest = ABOVE_2026[k:]
        assert [c["country"] for c in full["cups"]] == [c for c, _, _ in rest]
        assert [c["room"] for c in full["cups"]] == [max(0, 343 - j) for _, j, _ in rest]
        assert sum(c["fill"] for c in full["cups"]) + full["spill"] == full["left"] == left
        assert all(0 <= c["fill"] <= c["room"] for c in full["cups"] + half["cups"])
        assert (full["spill"] > 0) == cannot_win(343, [j for _, j, _ in rest], left)
    assert got[4][0]["spill"] == 17 and got[3][0]["spill"] == 0


def test_tie_needs_no_smaller_cup():
    """Part a: a country above Israel by the jury has at least Israel's jury score, so the
    public points that bring it exactly to Israel's total, total - jury_c, are at most
    Israel's own public points (in 2026 every one is below 220, Poland's 210 the largest)."""
    import sys

    from extract_code import ROOT

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import q0008

    assert max(343 - j for _, j, _ in ABOVE_2026) == 210 < 220
    for jury in range(0, 421, 7):
        for pub in range(0, 433, 9):
            results = [("Israel", jury, pub) if c == "Israel" else (c, j, p) for c, j, p in q0008.RESULTS]
            order = sorted(results, key=lambda r: (r[1], r[0] == "Australia"))
            idx = next(i for i, r in enumerate(order) if r[0] == "Israel")
            assert all(jury + pub - j <= pub for _, j, _ in order[idx + 1:])


def test_step_table_on_page():
    """The step table of part a is the generator's step_table(), and its last row says why
    the loss is certain although 0 <= 0 (Bulgaria passed 343)."""
    import sys

    from extract_code import ROOT, question_path

    sys.path.insert(0, str(ROOT / "tools" / "figures"))
    import q0008

    page = question_path(8).read_text(encoding="utf-8")
    table = q0008.step_table()
    assert "\n".join("    " + line for line in table.split("\n")) in page
    assert "| \u200fBulgaria | 312 | 516 | 0 | 0 | **לא** (בולגריה עברה את 343) |" in table
