"""Question 0066: the generator's references and traces against the page code, the
explorer's JavaScript (the three modes of intervals) against the generator's traces, and
the page copies of the generated blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0066  # noqa: E402

ns = load_python(66)


def cases(seed, count, heights):
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        n = rng.randint(1, 8)
        starts = [rng.randint(0, 20) for _ in range(n)]
        if heights:
            out.append([[s, s + rng.randint(1, 6), rng.randint(1, 4)] for s in starts])
        else:
            out.append([[s, s + rng.randint(0, 6)] for s in starts])
    return out


def test_generator_matches_the_page_code():
    for ivs in [q0066.IVS] + cases(6600, 300, False):
        assert [tuple(x) for x in q0066.trace_merge(ivs)[-1]["after"]] == ns["merge"](ivs) == q0066.brute_merge(ivs)
    for tr in [q0066.TRIPLES, q0066.TRIPLES_C] + cases(6601, 300, True):
        pieces = ns["skyline"](tr)
        assert q0066.skyline_ref(tr) == pieces == q0066.brute_skyline(tr)
        for t in (1, 2, 4):
            assert [tuple(r) for r in q0066.trace_above(pieces, t)[-1]["ranges"]] == ns["above"](pieces, t)
        top, where = ns["peak"](pieces)
        last = q0066.trace_above(pieces, 1)[-1] if pieces else None
        assert (top, where) == ((last["peak"], [tuple(w) for w in last["where"]]) if last else (0, []))


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    acases = [list(map(list, q0066.IVS)), [[1, 4], [4, 5]], [[8, 10], [1, 3], [2, 6]], [[1, 10], [2, 3], [4, 5]]] + cases(6602, 25, False)
    bcases = [list(map(list, q0066.TRIPLES)), list(map(list, q0066.TRIPLES_C)), [[0, 2, 3], [2, 4, 3]], [[0, 4, 1], [0, 4, 2]], [[0, 2, 1], [5, 7, 1]]] + cases(6603, 25, True)
    ccases = [(list(map(list, q0066.TRIPLES_C)), q0066.T_C), (list(map(list, q0066.TRIPLES)), 7)] + [(tr, random.Random(i).randint(1, 8)) for i, tr in enumerate(cases(6604, 25, True))]
    got = node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify([{json.dumps(acases)}.map((a) => m.ivMerge(a)),
        {json.dumps(bcases)}.map((a) => m.ivSkyline(a)),
        {json.dumps(ccases)}.map(([a, t]) => m.ivAbove(m.ivPieces(a), t))]));""")
    for ivs, ev in zip(acases, got[0]):
        ref = q0066.trace_merge(ivs)
        keys = ("i", "s", "e", "kind", "prev_end", "before", "after")
        assert [tuple(json.dumps(e[k]) for k in keys) for e in ev] == [tuple(json.dumps(e[k]) for k in keys) for e in ref], ivs
    for tr, ev in zip(bcases, got[1]):
        ref = q0066.trace_skyline(tr)
        keys = ("p", "events", "before", "after", "prev", "piece", "joined", "pieces")
        assert [tuple(json.dumps(e[k]) for k in keys) for e in ev] == [tuple(json.dumps(e[k]) for k in keys) for e in ref], tr
    for (tr, t), ev in zip(ccases, got[2]):
        ref = q0066.trace_above(q0066.skyline_ref(tr), t)
        keys = ("j", "s", "e", "h", "ok", "joined", "ranges", "peak", "where")
        assert [tuple(json.dumps(e[k]) for k in keys) for e in ev] == [tuple(json.dumps(e[k]) for k in keys) for e in ref], (tr, t)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(66)
