"""Question 0069: the generator's references against the page code, the explorer's
JavaScript (the three modes of overtakes) against the generator's walks, and the page
copies of the generated blocks."""

import json
import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0069  # noqa: E402

ns = load_python(69)


def test_generator_matches_the_page_code():
    rng = random.Random(6900)
    for _ in range(500):
        n = rng.randint(0, 14)
        done = [rng.randint(0, 9) for _ in range(n)]
        by_i = sorted(q0069.walk_passed(done), key=lambda r: r["i"])
        assert [r["count"] for r in by_i] == ns["passed"](done) == q0069.brute_passed(done)
        assert [r["count"] for r in q0069.walk_overtook(done)] == ns["overtook"](done) == q0069.brute_overtook(done)
        live = q0069.walk_live(done)
        assert [r["i"] for r in live] == ns["arrival_order"](done)
        assert [r["count"] for r in live] == ns["live_overtakes"](ns["arrival_order"](done), n)
        assert (live[-1]["total"] if live else 0) == ns["inversions"](done) == q0069.brute_inversions(done)
        if live:
            assert abs(live[-1]["disorder"] - ns["disorder"](done)) < 1e-12


def test_explorer_matches_the_reference():
    from page_tests import explorer_require, node_json

    rng = random.Random(6901)
    cases = [q0069.DONE, [7, 3, 9, 2, 8], [4, 4, 4], [1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [3], [2, 2, 1, 5, 2]]
    cases += [[rng.randint(0, 20) for _ in range(rng.randint(1, 16))] for _ in range(30)]
    got = node_json(f"""
      const m = {explorer_require()};
      const C = {json.dumps(cases)};
      console.log(JSON.stringify(["a", "b", "c"].map((mode) => C.map((d) => m.ovWalk(d, mode)))));""")
    keys = ("k", "i", "v", "rank", "inserted", "arg", "q", "qpath", "upath", "count", "total", "tree")
    walks = {"a": q0069.walk_passed, "b": q0069.walk_overtook, "c": q0069.walk_live}
    for mode, per_case in zip("abc", got):
        for done, rows in zip(cases, per_case):
            ref = walks[mode](done)
            if mode != "c":
                total = 0
                for r in ref:
                    total += r["count"]
                    r["total"] = total
            assert [tuple(r[x] for x in keys) for r in rows] == [tuple(r[x] for x in keys) for r in ref], (mode, done)
            if mode == "c":
                assert [round(r["disorder"], 9) for r in rows] == [round(r["disorder"], 9) for r in ref]


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(69)
