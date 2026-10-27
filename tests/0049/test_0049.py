"""Question 0049 has no code on the page; these tests check that the explorer
(docs/javascripts/explorer/uvmarch.js) draws the same components and arrows as the figure
generator (tools/figures/q0049.py), that every stage of the transaction follows an
arrow of the figure in the generator's order, that every component has its card and every
quiz answer is a component, and the page copies of the generated blocks."""

import json
import sys

from extract_code import ROOT

sys.path.insert(0, str(ROOT / "tools" / "figures"))
import q0049  # noqa: E402


def models():
    from page_tests import explorer_require, node_json

    return node_json(f"""
      const m = {explorer_require()};
      console.log(JSON.stringify({{ layout: m.UV_LAYOUT, arrows: m.UV_ARROWS, path: m.UV_PATH, info: m.UV_INFO, quiz: m.UV_QUIZ, stages: m.UV_STAGES }}));""")


def test_explorer_draws_the_figure():
    m = models()
    assert {k: list(v) for k, v in q0049.LAYOUT.items()} == m["layout"]
    assert [list(a) for a in q0049.ARROWS] == m["arrows"]


def test_path_follows_the_arrows():
    m = models()
    arrows = {(a, b) for a, b, _ in q0049.ARROWS}
    assert [tuple(e) for e in m["path"]] == q0049.PATH
    assert all(e in arrows for e in q0049.PATH)
    # the path starts at the sequence and ends at the scoreboard, and the lit component of
    # every stage with an arrow is one of its ends
    assert q0049.PATH[0][0] == "sequence" and q0049.PATH[-1][1] == "scoreboard"
    for edge, lit, text in m["stages"]:
        assert text
        if edge:
            assert lit in edge, (edge, lit)


def test_cards_and_quiz():
    m = models()
    assert set(m["info"]) == set(q0049.LAYOUT)
    assert all(len(v) == 3 and all(v) for v in m["info"].values())
    assert len(m["quiz"]) >= 8
    for q, answers in m["quiz"]:
        assert q and answers and all(a in q0049.LAYOUT for a in answers), q


def test_figure_arrows_meet_the_boxes():
    """Every arrow starts on the edge of its source box and ends on the edge of its target."""
    for a, b, _ in q0049.ARROWS:
        (x1, y1), (x2, y2) = q0049.arrow_line(a, b)
        for (x, y), c in (((x1, y1), a), ((x2, y2), b)):
            _, bx, by, w, h, _ = q0049.LAYOUT[c]
            on_x = abs(x - bx) < 1e-6 or abs(x - bx - w) < 1e-6
            on_y = abs(y - by) < 1e-6 or abs(y - by - h) < 1e-6
            assert (on_x and by - 1e-6 <= y <= by + h + 1e-6) or (on_y and bx - 1e-6 <= x <= bx + w + 1e-6), (a, b, c)


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(49)
