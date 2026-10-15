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
