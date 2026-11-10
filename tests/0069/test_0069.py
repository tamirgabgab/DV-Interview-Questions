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
                # the reorder buffer row of box c: what waits after each arrival, and for whom
                assert [(r["held"], r["head"]) for r in rows] == [(r["held"], r["head"]) for r in ref], done


def test_reorder_buffer_row():
    """Box c's buffer row (walk_live's held): after every arrival and delivery the buffer
    holds only responses sent after its head, and its largest occupancy is max(passed)."""
    rng = random.Random(6902)
    assert [(r["held"], r["head"]) for r in q0069.walk_live(q0069.DONE)] == [(1, 0), (2, 0), (1, 2), (0, 4)]
    assert [r["held"] for r in q0069.walk_live([4, 3, 2, 1])] == [1, 2, 3, 0]          # the box's "reversed" task
    assert [r["held"] for r in q0069.walk_live([1, 2, 3, 4])] == [0, 0, 0, 0]
    for _ in range(2000):
        done = [rng.randint(0, 9) for _ in range(rng.randint(1, 14))]
        live = q0069.walk_live(done)
        assert max(r["held"] for r in live) == max(ns["passed"](done)), done
        assert live[-1]["held"] == 0 and live[-1]["head"] == len(done)


def test_box_tasks():
    """The numbers the three "try it" paragraphs promise."""
    a = q0069.walk_passed([3, 3, 3, 3])
    assert len(a[0]["tree"]) == 1 and all(r["arg"] == 0 and r["qpath"] == [] and r["count"] == 0 for r in a)
    assert ns["passed"]([4, 3, 2, 1]) == [3, 2, 1, 0] and sum(ns["passed"]([4, 3, 2, 1])) == 6
    first = q0069.walk_passed([8, 7, 6, 5, 4, 3, 2, 1])[0]
    assert (first["i"], first["rank"], first["upath"]) == (7, 1, [1, 2, 4, 8])       # the second step of the box
    assert ns["overtook"]([3, 3, 1]) == [0, 0, 2]
    assert ns["overtook"]([3, 2, 1]) == [0, 1, 2] and sum(ns["passed"]([3, 2, 1])) == 3
    assert ns["disorder"]([1, 2, 3, 4]) == 0.0 and ns["disorder"]([4, 3, 2, 1]) == 1.0
    live = q0069.walk_live(q0069.DONE)
    assert live[2]["total"] == 3 and live[-1]["total"] == 4 and max(r["held"] for r in live) == 2


def test_monitor_table():
    """The RTL monitor clock by clock (the follow-up's table): passed per response is the
    page's passed, the registers are the running maximum and sum, and the example's rows."""
    rows = q0069.hw_rows(q0069.DONE)
    assert [(r["clk"], r["seq"], f"{r['before']:04b}", r["passed"], f"{r['after']:04b}", r["max"], r["total"]) for r in rows] == \
        [(1, 3, "0000", 0, "1000", 0, 0), (2, 1, "1000", 1, "1010", 1, 1), (5, 0, "1010", 2, "1011", 2, 3), (6, 2, "1011", 1, "1111", 2, 4)]
    rng = random.Random(6903)
    for _ in range(500):
        n = rng.randint(1, 14)
        done = rng.sample(range(1, 40), n)
        rows = q0069.hw_rows(done)
        want = ns["passed"](done)
        assert [r["passed"] for r in rows] == [want[r["seq"]] for r in rows]
        assert rows[-1]["max"] == max(want) and rows[-1]["total"] == ns["inversions"](done) and rows[-1]["after"] == (1 << n) - 1


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(69)
