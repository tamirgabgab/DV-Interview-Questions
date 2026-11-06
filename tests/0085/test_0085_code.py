"""Question 0085: the page's Python code (it runs as published) against the generator's
reference: is_self_describing on every string of a few digits, self_describing base by base
(the same numbers in the same order), predicted and differ."""

import itertools
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0085  # noqa: E402

ns = load_python(85)
is_self_describing, self_describing = ns["is_self_describing"], ns["self_describing"]
predicted, differ = ns["predicted"], ns["differ"]


def test_is_self_describing():
    for b in range(1, 6):
        for d in itertools.product(range(b), repeat=b):
            assert is_self_describing(list(d)) == q0085.is_self(d), d
    assert is_self_describing([6, 2, 1, 0, 0, 0, 1, 0, 0, 0])
    assert not is_self_describing([9, 0, 0, 0, 0, 0, 0, 0, 0, 0])


def test_self_describing_matches_the_reference():
    for b in range(2, 13):
        assert self_describing(b) == q0085.search(b)[0], b
    assert self_describing(10) == [[6, 2, 1, 0, 0, 0, 1, 0, 0, 0]]


def test_predicted_and_differ():
    for b in q0085.BASES:
        assert predicted(b) == q0085.family(b), b
    assert differ(12) == []
