"""Question 0029 has no code on the page; these tests recompute every number the page states
with exact fractions (pair counts, the 2,872 total, the triple-meeting proof, the last
meetings of the day, the minute without a meeting, the follow-ups), run the clock explorer
under Node against the same reference, and check that the figures and tables are the
generator's output."""

import bisect
import math
import sys
from fractions import Fraction as Fr

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0029  # noqa: E402

DAY, HALF = q0029.DAY, q0029.HALF


def meeting_times(periods, L):
    """The meetings in [0, L) of a clock with the given periods, with the hands at each one;
    found from the relative speed of every pair, independently of q0029."""
    out = {}
    names = sorted(periods, key=periods.get)
    for x in range(3):
        for y in range(x + 1, 3):
            i, j = names[x], names[y]
            rel = Fr(1, periods[i]) - Fr(1, periods[j])
            k = 0
            while k / rel < L:
                out.setdefault(k / rel, set()).update((i, j))
                k += 1
    return out


CLOCK = {"s": 60, "m": 3600, "h": 43200}


def test_pairs():
    assert q0029.gap("s", "m") == Fr(3600, 59)
    assert q0029.gap("s", "h") == Fr(43200, 719)
    assert q0029.gap("m", "h") == Fr(43200, 11)
    assert [len(q0029.meetings(i, j)) for i, j in q0029.PAIRS] == [1416, 1438, 22]
    assert [int(q0029.turns(i)) for i in "smh"] == [1440, 24, 2]
    assert 1440 - 24 == 1416 and 1440 - 2 == 1438 and 24 - 2 == 22
    for (i, j), (closed, opn, half) in zip(q0029.PAIRS, ((709, 707, 708), (720, 718, 719), (12, 10, 11))):
        times = q0029.meetings(i, j, HALF + 1)
        assert sum(1 for t in times if t <= HALF) == closed == q0029.count(1, 1, HALF, i, j)
        assert sum(1 for t in times if 0 < t < HALF) == opn == q0029.count(0, 0, HALF, i, j)
        assert sum(1 for t in times if t < HALF) == half == q0029.count(1, 0, HALF, i, j)
        assert HALF / q0029.gap(i, j) == half                 # 708, 719 and 11
    # the gap is one lap of the faster hand: the hands really point the same way
    for i, j in q0029.PAIRS:
        for t in q0029.meetings(i, j):
            assert q0029.angle(i, t) == q0029.angle(j, t)


def test_answer():
    ev = meeting_times(CLOCK, DAY)
    assert ev.keys() == q0029.events().keys()
    assert len(ev) == 2872
    assert sum(len(q0029.meetings(i, j)) for i, j in q0029.PAIRS) == 2876
    assert [t for t, hands in ev.items() if len(hands) == 3] == [0, HALF]
    inner = [t for t in ev if 0 < t < HALF]
    assert len(inner) == 1435 == 707 + 718 + 10
    assert 2 * 1435 + 2 == 2872 and 2 * 1435 == 2870 and 2872 + 1 == 2873


def test_triple_proof():
    assert 708 == 2 ** 2 * 3 * 59 and math.gcd(11, 708) == 1
    sols = [(a, b) for b in range(0, 34) for a in range(0, 2200) if 11 * a == 708 * b]
    assert sols == [(708 * c, 11 * c) for c in range(4)]
    assert all(Fr(3600 * a, 59) == 43200 * (b // 11) for a, b in sols)
    T = q0029.gap("m", "h")
    for k in range(23):
        t = k * T
        assert q0029.angle("m", t) == q0029.angle("h", t) == Fr(k % 11, 11)
        assert t / 60 == 65 * k + Fr(5 * k, 11)
        assert q0029.angle("s", t) == Fr(5 * k % 11, 11)
        assert (q0029.angle("s", t) == q0029.angle("m", t)) == (k % 11 == 0)


def test_page_numbers():
    T = q0029.gap("m", "h")
    assert q0029.clock(T) == "1:05:27.27" and q0029.dec(T) == "3927.27"
    assert q0029.dec(q0029.gap("s", "m")) == "61.02" and q0029.dec(q0029.gap("s", "h")) == "60.08"
    assert q0029.dec(Fr(60, 59), 3) == "1.017" and q0029.dec(Fr(60, 719), 3) == "0.083"
    assert 59 * 24 == 1416
    # the last meetings of the day, and nothing in the minute 23:59
    ev = q0029.events()
    last = list(ev.items())[-2:]
    assert [(q0029.clock(t), sorted(h)) for t, h in last] == [
        ("23:58:58.98", ["m", "s"]), ("23:58:59.92", ["h", "s"])]
    assert not [t for t in ev if t >= DAY - 60]
    # the second-minute meeting slides 60/59 s each minute; minute 59 of every hour has none
    first_hour = q0029.meetings("s", "m", 3600)
    assert [int(t // 60) for t in first_hour] == list(range(59))
    assert q0029.clock(first_hour[58]) == "0:58:58.98"
    minutes = {int(t // 60) for t in q0029.meetings("s", "m")}
    assert set(range(1440)) - minutes == {60 * h + 59 for h in range(24)}
    minutes = {int(t // 60) for t in q0029.meetings("s", "h")}
    assert set(range(1440)) - minutes == {719, 1439}            # 11:59 and 23:59
    # the zoom: the hour hand first, then the minute hand, two separate moments
    assert q0029.gap("s", "h") < q0029.gap("s", "m")
    # the closest second-minute and second-hour meetings: 3600 / 42421 s apart
    sm, sh = q0029.meetings("s", "m"), q0029.meetings("s", "h")
    gaps = [abs(a - b) for a in sm for b in sh[max(0, int(a / sh[1]) - 2):int(a / sh[1]) + 3] if a != b]
    assert min(gaps) == Fr(3600, 42421) and q0029.dec(Fr(3600, 42421), 3) == "0.085"
    # the clock-face table: the second hand mark equals the minute-hour mark only at k = 0, 11
    rows = [(60 * q0029.angle("m", k * T), 60 * q0029.angle("s", k * T)) for k in range(12)]
    assert [k for k, (a, b) in enumerate(rows) if a == b] == [0, 11]


def test_follow_ups():
    assert 7 * 2872 == 20104
    # a 24-hour dial
    ev = meeting_times({"s": 60, "m": 3600, "h": 86400}, DAY)
    pairs = [sum(1 for h in ev.values() if {a, b} <= h) for a, b in (("s", "m"), ("s", "h"), ("m", "h"))]
    assert pairs == [1416, 1439, 23] and len(ev) == 2876
    assert [t for t, h in ev.items() if len(h) == 3] == [0]
    # minute and hour opposite, and at right angles
    rel = Fr(1, 3600) - Fr(1, 43200)
    assert sum(1 for k in range(100) if (k + Fr(1, 2)) / rel < DAY) == 22
    assert sum(1 for k in range(100) for ph in (Fr(1, 4), Fr(3, 4)) if (k + ph) / rel < DAY) == 44
    # a ticking second hand: it points at mark n % 60 during [n, n + 1). The minute (hour) hand
    # is on a whole mark only at multiples of 60 s (720 s), which are whole seconds, so it is
    # enough to look at whole seconds.
    sm = {n for n in range(DAY) if Fr(n, 60) % 60 == n % 60}
    sh = {n for n in range(DAY) if Fr(n, 720) % 60 == n % 60}
    mh = set(q0029.meetings("m", "h"))
    assert sm == {3600 * h for h in range(24)} and sh == {0, HALF}
    assert len(sm | sh | mh) == 44


def test_explorer_matches_python():
    from page_tests import explorer_require, node_json

    ev = sorted(q0029.events())
    per_pair = [q0029.meetings(i, j) for i, j in q0029.PAIRS]
    secs = sorted(set(range(0, DAY, 97)) | {int(t) + d for t in ev[::7] for d in (-1, 0, 1)} | {DAY - 1})
    secs = [s for s in secs if 0 <= s < DAY]
    got = node_json(f"const m = {explorer_require()};"
                    f"const secs = {secs};"
                    "const counts = secs.map((s) => m.clockCounts(s));"
                    "const meets = []; for (let s = 0; s < 86400; s++) m.clockMeetsIn(s).forEach(([n, t]) => meets.push([s, n, t]));"
                    "const fwd = [0]; for (let v = m.clockNext(0); v !== null; v = m.clockNext(v)) fwd.push(v);"
                    "const back = []; for (let v = m.clockPrev(86400 - 1e-6); v !== null; v = m.clockPrev(v)) back.push(v);"
                    "console.log(JSON.stringify({counts, meets, fwd, back, labels: fwd.map(m.clockLabel)}));")
    for s, c in zip(secs, got["counts"]):
        end = Fr(s + 1)
        pairs = [bisect.bisect_left(p, end) for p in per_pair]
        triple = sum(1 for t in (0, HALF) if t < end)
        assert c == {"pairs": pairs, "triple": triple, "total": bisect.bisect_left(ev, end)}, s
        assert c["total"] == sum(pairs) - 2 * triple
    ref = sorted((math.floor(t), n, t) for n, p in enumerate(per_pair) for t in p)
    assert [(s, n) for s, n, _ in got["meets"]] == [(s, n) for s, n, _ in ref]
    assert all(abs(t - float(r)) < 1e-9 for (_, _, t), (_, _, r) in zip(got["meets"], ref))
    assert len(got["fwd"]) == 2872 and all(abs(a - float(b)) < 1e-9 for a, b in zip(got["fwd"], ev))
    assert len(got["back"]) == 2872 and all(abs(a - float(b)) < 1e-9 for a, b in zip(got["back"], ev[::-1]))
    assert got["labels"] == [q0029.clock(t) for t in ev]


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(29)


def test_explorer_pair_filter():
    """clockNext / clockPrev with a pair mask walk exactly the meetings of those pairs."""
    from page_tests import explorer_require, node_json

    got = node_json(f"const m = {explorer_require()}; const out = {{}};"
                    "for (const mask of [[2], [0], [1, 2]]) {"
                    "  const fwd = [0]; for (let v = m.clockNext(0, mask); v !== null; v = m.clockNext(v, mask)) fwd.push(v);"
                    "  const back = []; for (let v = m.clockPrev(86400 - 1e-6, mask); v !== null; v = m.clockPrev(v, mask)) back.push(v);"
                    "  out[mask.join()] = { fwd, back }; }"
                    "console.log(JSON.stringify(out));")
    per_pair = [q0029.meetings(i, j) for i, j in q0029.PAIRS]
    for key, r in got.items():
        pairs = [int(k) for k in key.split(",")]
        ref = sorted(set(t for n in pairs for t in per_pair[n]))
        assert len(r["fwd"]) == len(ref) and all(abs(a - float(b)) < 1e-9 for a, b in zip(r["fwd"], ref)), key
        assert all(abs(a - float(b)) < 1e-9 for a, b in zip(r["back"], ref[::-1])), key
    assert len(got["2"]["fwd"]) == 22 and len(got["0"]["fwd"]) == 1416 and len(got["1,2"]["fwd"]) == 1438 + 22 - 2


def test_explorer_gap_line():
    """The gap line box of part b (J298): T = ti tj / (tj - ti) and L / T as exact fractions,
    the three counts of formula 3 against counting the meetings k T in each interval, for
    the clock's pairs over 12 hours and a day (the page's table) and for every length in
    quarters of T up to 6 T with other periods; the box's dot test agrees with the counts."""
    import json

    from page_tests import explorer_require, node_json

    cases = [(60, 3600, 43200, 1), (60, 43200, 43200, 1), (3600, 43200, 43200, 1),
             (60, 3600, 86400, 1), (60, 43200, 86400, 1), (3600, 43200, 86400, 1)]
    for ti, tj in [(60, 3600), (60, 43200), (3600, 43200), (2, 3), (5, 7), (1, 1000)]:
        T = Fr(ti * tj, tj - ti)
        cases += [(ti, tj, (q * T).numerator, (q * T).denominator) for q in (Fr(n, 4) for n in range(1, 25))]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map(([ti, tj, Ln, Ld]) => {{
        const r = m.gapLine(ti, tj, Ln, Ld), dots = {{}};
        for (const mode of m.GAP_MODES) {{ let c = 0; for (let k = 0; k <= r.closed + 1; k++) if (m.gapIn(k, r.rn, r.rd, mode)) c++; dots[mode] = c; }}
        return {{ ...r, dots }};
      }})));""")
    for (ti, tj, Ln, Ld), r in zip(cases, got):
        T, L = Fr(ti * tj, tj - ti), Fr(Ln, Ld)
        assert Fr(r["Tn"], r["Td"]) == T and Fr(r["rn"], r["rd"]) == L / T and r["whole"] == ((L / T).denominator == 1)
        ks = range(0, int(L / T) + 2)
        want = {"closed": sum(0 <= k * T <= L for k in ks), "open": sum(0 < k * T < L for k in ks), "half": sum(0 <= k * T < L for k in ks)}
        assert {m: r[m] for m in want} == want == r["dots"]
        assert want == {"closed": math.floor(L / T) + 1, "open": math.ceil(L / T) - 1, "half": math.ceil(L / T)}
    table = [(r["closed"], r["open"], r["half"]) for r in got[:3]]
    assert table == [(709, 707, 708), (720, 718, 719), (12, 10, 11)]
    assert [r["half"] for r in got[3:6]] == [1416, 1438, 22]
