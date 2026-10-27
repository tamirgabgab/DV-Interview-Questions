"""Question 0050: the page's OooScoreboard against the generator's checkers
(tools/figures/q0050.py) on the scenarios of part b and on random streams, legal ones (no
error) and ones with one injected bug (at least one error of the right kind); the
scenario table; the explorer's JavaScript (its checkers and its random streams); and the
page copies of the generated blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0050  # noqa: E402

OooScoreboard = load_python(50)["OooScoreboard"]
BUGS = ("swap", "data", "drop", "dup", "late")


def run(events, timeout=q0050.TIMEOUT):
    """The page's scoreboard on events (t, op, id, data); the errors as (kind, id)."""
    sb = OooScoreboard(timeout)
    for t, op, i, d in events:
        sb.check_timeouts(t)
        if op == "req":
            sb.on_request(i, d, t)
        elif op == "rsp":
            sb.on_response(i, d, t)
        elif op == "reset":
            sb.on_reset()
        else:
            sb.final_check()
    return [(e.split()[0], int(e.split("id=")[1].split(":")[0].split(",")[0].split()[0])) for e in sb.errors]


def legal_stream(rng, n=30, ids=4):
    """Requests and responses interleaved at random; each ID answered in its own order."""
    events, pend, t, nxt = [], {i: [] for i in range(ids)}, 0, 100
    sent = 0
    while sent < n or any(pend.values()):
        busy = [i for i in pend if pend[i]]
        if sent < n and (not busy or rng.random() < 0.55):
            i = rng.randrange(ids)
            events.append((t, "req", i, nxt))
            pend[i].append(nxt)
            nxt, sent = nxt + 1, sent + 1
        else:
            i = rng.choice(busy)
            events.append((t, "rsp", i, pend[i].pop(0)))
        t += 1
    return events + [(t, "end", 0, 0)]


def mutate(rng, events, bug):
    ev = events[:-1]
    rsp = [k for k, e in enumerate(ev) if e[1] == "rsp"]
    if bug == "swap":                     # two responses of one ID trade places
        pairs = [(a, b) for a in rsp for b in rsp if a < b and ev[a][2] == ev[b][2]]
        if not pairs:
            return None
        a, b = rng.choice(pairs)
        ev[a], ev[b] = (ev[a][0], "rsp", ev[a][2], ev[b][3]), (ev[b][0], "rsp", ev[b][2], ev[a][3])
    elif bug == "data":
        k = rng.choice(rsp)
        ev[k] = ev[k][:3] + (ev[k][3] + 1000,)
    elif bug == "drop":
        ev.pop(rng.choice(rsp))
    elif bug == "dup":
        k = rng.choice(rsp)
        ev.insert(k + 1, ev[k])
    elif bug == "late":                   # everything from one response on comes much later
        k = rng.choice(rsp)
        ev = ev[:k] + [(e[0] + 3 * q0050.TIMEOUT,) + e[1:] for e in ev[k:]]
    end_t = (ev[-1][0] if ev else 0) + 1
    return ev + [(end_t, "end", 0, 0)]


def test_scenarios():
    for name, legal, ev in q0050.SCENARIOS:
        got = run(ev)
        assert sorted(set(got)) == sorted(set(q0050.check(ev, "per_id"))), name
        assert (not got) == legal, name


def test_scenario_table_claims():
    rows = {name: [q0050.check(ev, k) for k in ("per_id", "fifo", "any")] for name, legal, ev in q0050.SCENARIOS}
    assert rows["ערבוב חוקי בין IDs"][0] == [] and rows["ערבוב חוקי בין IDs"][1] and rows["ערבוב חוקי בין IDs"][2] == []
    assert rows["החלפת סדר בתוך ID"][0] and rows["החלפת סדר בתוך ID"][2] == []
    assert rows["תשובה חסרה"][1][0] == ("mismatch", 1)          # the single FIFO blames ID 1 first


def test_random_streams():
    rng = random.Random(50)
    for _ in range(400):
        ev = legal_stream(rng, n=rng.randint(1, 40), ids=rng.randint(1, 5))
        assert run(ev, 10_000) == [] and q0050.check(ev, "per_id", 10_000) == []
        for bug in BUGS:
            bad = mutate(rng, ev, bug)
            if bad is None:
                continue
            timeout = q0050.TIMEOUT if bug == "late" else 10_000
            got = run(bad, timeout)
            assert got, (bug, bad)
            assert sorted(set(got)) == sorted(set(q0050.check(bad, "per_id", timeout))), (bug, bad)
            want = {"swap": "mismatch", "data": "mismatch", "drop": "missing", "dup": "unexpected", "late": "timeout"}[bug]
            assert want in {k for k, _ in got}, (bug, got)


def test_explorer_matches_the_checkers():
    from page_tests import explorer_require, node_json

    rng = random.Random(51)
    streams = [ev for _, _, ev in q0050.SCENARIOS] + [legal_stream(rng, n=rng.randint(1, 25), ids=3) for _ in range(30)]
    streams += [s for s in (mutate(rng, legal_stream(rng, 20, 3), b) for b in BUGS * 4) if s]
    got = node_json(f"""
      const m = {explorer_require()};
      const S = {json.dumps(streams)};
      console.log(JSON.stringify([
        S.map((ev) => ["per_id", "fifo", "any"].map((k) => m.sbCheck(ev.map(([t, op, id, data]) => ({{ t, op, id, data }})), k, {q0050.TIMEOUT}).errors)),
        [1, 2, 3, 4, 5, 6].map((seed) => ["none", "swap", "data", "drop", "dup", "late"].map((bug) => m.sbCheck(m.sbTraffic(seed, bug, 16, 3), "per_id", {q0050.TIMEOUT}).errors.length)),
      ]));""")
    for ev, per_kind in zip(streams, got[0]):
        for k, errs in zip(("per_id", "fifo", "any"), per_kind):
            assert [tuple(e) for e in errs] == q0050.check(ev, k), (k, ev)
    for row in got[1]:
        assert row[0] == 0 and all(n > 0 for n in row[1:]), row


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(50)
