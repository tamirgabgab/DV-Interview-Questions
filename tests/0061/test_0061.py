"""Question 0061: the page's tags_needed against a count of the open transactions at every
send time on random lists; the page's numbers (2 on the three transactions, 1 when a
response and a send meet at 10, the two pools with their peaks apart, 2 + 2 against 2, and
together, 4); pools against tags_needed on each kind alone; the explorer's JavaScript
against the generator's sweep; and the page copies of the blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0061  # noqa: E402

ns = load_python(61)
tags_needed, pools = ns["tags_needed"], ns["pools"]


def plain(txns):
    return [(s, e) for s, e, *_ in txns]


def test_page_examples():
    assert tags_needed(q0061.TXNS) == 2 == q0061.brute_tags(q0061.TXNS)
    assert tags_needed([(0, 10), (10, 20)]) == 1                      # a response frees its tag for a send at the same time
    assert tags_needed([(0, 10), (10, 20), (5, 15)]) == 2             # the self-check of part a
    assert tags_needed([]) == 0 and tags_needed([(3, 4)]) == 1
    assert pools(q0061.TXNS_B) == (2, 2, 2) == q0061.pools(q0061.TXNS_B)
    assert pools(q0061.TXNS_C) == (2, 2, 4) == q0061.pools(q0061.TXNS_C)
    assert pools([(s, e, "R") for s, e in q0061.TXNS]) == (2, 0, 2)
    rows = q0061.sweep(q0061.TXNS)
    assert [(r["t"], r["d"], r["total"]) for r in rows] == [(0, 1, 1), (5, 1, 2), (10, -1, 1), (15, 1, 2), (20, -1, 1), (30, -1, 0)]


def test_against_every_moment():
    rng = random.Random(61)
    for _ in range(300):
        txns = []
        for _ in range(rng.randint(0, 9)):
            s = rng.randint(0, 20)
            txns.append((s, s + rng.randint(1, 10), rng.choice("RW")))
        assert tags_needed(plain(txns)) == q0061.brute_tags(txns), txns
        r, w, a = pools(txns)
        assert a == tags_needed(plain(txns))
        assert r == tags_needed(plain(t for t in txns if t[2] == "R"))
        assert w == tags_needed(plain(t for t in txns if t[2] == "W"))
        assert max(r, w) <= a <= r + w
    assert tags_needed([(0, 5), (5, 9), (9, 12)]) == 1               # a chain of responses and sends at the same times


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(62)
    cases = [[list(t) + ["R"] for t in q0061.TXNS], [list(t) for t in q0061.TXNS_B], [list(t) for t in q0061.TXNS_C]]
    for _ in range(30):
        n = rng.randint(1, 10)
        cases.append([[s, s + rng.randint(1, 12), rng.choice("RW")] for s in (rng.randint(0, 30) for _ in range(n))])
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({json.dumps(cases)}.map((c) => [m.tpSweep(c).map((r) => [r.t, r.d, r.kind, r.i, r.total, r.best.R, r.best.W, r.best.all]), m.tpPools(c)])));""")
    for txns, (rows, pool) in zip(cases, got):
        ref = q0061.sweep([tuple(t) for t in txns])
        assert rows == [[r["t"], r["d"], r["kind"], r["i"], r["total"], r["best"]["R"], r["best"]["W"], r["best"]["all"]] for r in ref], txns
        assert tuple(pool) == q0061.pools([tuple(t) for t in txns]) == pools([tuple(t) for t in txns])


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(61)
