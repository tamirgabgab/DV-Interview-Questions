import itertools
import random

from extract_code import load_python

ns = load_python(4)
LABELS = ["RED", "BLACK", "MIXED"]


def cases():
    """Every label order with every content where all labels are wrong (12 cases)."""
    for labels in itertools.permutations(LABELS):
        for content in itertools.permutations(LABELS):
            if all(l != c for l, c in zip(labels, content)):
                yield list(labels), list(content)


def use_boxes(content):
    rng = random.Random(4)
    ns["draw"] = lambda i: rng.choice(["RED", "BLACK"]) if content[i] == "MIXED" else content[i]


def test_twelve_cases():
    assert len(list(cases())) == 12


def test_simple_solution():
    for labels, content in cases():
        use_boxes(content)
        for _ in range(5):
            assert ns["fix_labels_simple"](list(labels)) == content


def test_two_swap_solution():
    for labels, content in cases():
        use_boxes(content)
        for _ in range(5):
            assert ns["fix_labels"](list(labels)) == content


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(4)


def test_explorer_matches_page_code():
    """The boxes explorer: its twelve cases, its rule against the page's fix_labels_simple
    for every case and both ball colours, and its deduction after a draw."""
    import json

    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      const cases = m.boxesCases();
      console.log(JSON.stringify({{
        cases,
        fixed: cases.flatMap((c) => ["RED", "BLACK"].map((ball) => [c.labels, ball, m.boxesFix(c.labels, ball)])),
        deduce: cases.flatMap((c) => [0, 1, 2].flatMap((i) => ["RED", "BLACK"].map((ball) => [c.labels, i, ball, m.boxesDeduce(c.labels, i, ball)]))),
        draws: cases.map((c) => [0, 1, 2].map((i) => m.boxesDraw(c.content, i, () => 0.3))),
      }}));""")
    assert sorted((tuple(c["labels"]), tuple(c["content"])) for c in got["cases"]) == sorted((tuple(l), tuple(c)) for l, c in cases())
    for labels, ball, fixed in got["fixed"]:
        ns["draw"] = lambda i, b=ball: b
        assert fixed == ns["fix_labels_simple"](list(labels)) == ns["fix_labels"](list(labels))
    for labels, i, ball, left in got["deduce"]:
        possible = [c for l, c in cases() if l == list(labels)]
        assert left == [c for c in possible if c[i] == ball or c[i] == "MIXED"]
        if i == list(labels).index("MIXED"):
            assert len(left) == 1
    for c, drawn in zip(got["cases"], got["draws"]):
        assert drawn == ["RED" if x == "MIXED" else x for x in c["content"]]


def test_explorer_labels_fix_box():
    """The part b box: for each of the twelve cases, k, the ball drawn from it, n1, n2,
    same and other, and the labels after each swap are the page's fix_labels; the second
    swap leaves the true contents, and the page's example is the table above the box."""
    from page_tests import explorer_require, node_json

    all_cases = list(cases())
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({[[l, c] for l, c in all_cases]}.map(([l, c]) => m.labelSwaps(l, c[l.indexOf('MIXED')]))));")
    for (labels, content), r in zip(all_cases, got):
        use_boxes(content)
        assert ns["fix_labels"](list(labels)) == r["after2"] == content
        k = labels.index("MIXED")
        ball = content[k]
        n1, n2 = (k + 1) % 3, (k + 2) % 3
        assert (r["k"], r["n1"], r["n2"]) == (k, n1, n2)
        assert labels[r["same"]] == ball and {r["same"], r["other"]} == {n1, n2}
        after1 = list(labels)
        after1[k], after1[r["same"]] = after1[r["same"]], after1[k]
        assert r["after1"] == after1 and after1[k] == content[k]
    ex = got[all_cases.index((["RED", "BLACK", "MIXED"], ["BLACK", "MIXED", "RED"]))]
    assert (ex["k"], ex["same"], ex["other"]) == (2, 0, 1)
    assert ex["after1"] == ["MIXED", "BLACK", "RED"] and ex["after2"] == ["BLACK", "MIXED", "RED"]
