"""Question 0093: the page's Python code (it runs as published) against the generator's
reference: gale_shapley, blocking_pairs and all_stable on the example and on random
instances."""

import random
import sys

from extract_code import ROOT, load_python

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0093  # noqa: E402

ns = load_python(93)


def test_example():
    match, proposals = ns["gale_shapley"](q0093.CAND, q0093.JOBS)
    assert (match, proposals) == ([4, 0, 1, 5, 3, 2], 11)
    assert ns["blocking_pairs"](q0093.CAND, q0093.JOBS, match) == []
    assert ns["gale_shapley"](q0093.JOBS, q0093.CAND) == q0093.gs(q0093.JOBS, q0093.CAND)
    assert len(ns["all_stable"](q0093.CAND, q0093.JOBS)) == 5


def test_against_reference():
    rnd = random.Random(931)
    for _ in range(150):
        n = rnd.randint(1, 6)
        P = [rnd.sample(range(n), n) for _ in range(n)]
        Q = [rnd.sample(range(n), n) for _ in range(n)]
        assert ns["gale_shapley"](P, Q) == q0093.gs(P, Q)
        m = rnd.sample(range(n), n)
        assert ns["blocking_pairs"](P, Q, m) == q0093.blocking(P, Q, m)
        if n <= 5:
            assert ns["all_stable"](P, Q) == q0093.all_stable(P, Q)
