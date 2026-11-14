"""tools/figures/site_flow.py: the diagrams of docs/how-built.md stay true to the page and to
the workflow they draw."""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "figures"))
import fill  # noqa: E402
import site_flow  # noqa: E402


def test_the_page_has_the_generators_copy():
    assert not fill.check("how-built"), "run python tools/figures/fill.py how-built"


def test_the_ci_diagram_follows_the_workflow():
    jobs = yaml.safe_load((ROOT / ".github" / "workflows" / "deploy.yml").read_text(encoding="utf-8"))["jobs"]
    needs = {j: set([v["needs"]] if isinstance(v.get("needs"), str) else v.get("needs", [])) for j, v in jobs.items()}
    assert set(site_flow.CI_NODES) - {"push"} == set(jobs), "every job is a node, and nothing else but the push"

    def ancestors(j):
        seen, todo = set(), list(needs[j])
        while todo:
            a = todo.pop()
            if a not in seen:
                seen.add(a)
                todo += needs[a]
        return seen

    drawn = {}
    for a, b, *_ in site_flow.CI_EDGES:
        if a != "push":
            assert a in needs[b], f"{a} -> {b} is drawn, but {b} does not need {a}"
            drawn.setdefault(b, set()).add(a)
    for j, ns in needs.items():
        reached = set().union(*(ancestors(p) | {p} for p in drawn.get(j, set())))
        assert ns <= reached, f"{j} needs {sorted(ns - reached)}, which the diagram does not lead to it from"


def test_routes_are_orthogonal_and_end_on_their_boxes():
    for nodes, edges in ((site_flow.CI_NODES, site_flow.CI_EDGES), (site_flow.PAGE_NODES, site_flow.PAGE_EDGES)):
        for a, b, *_, pts in edges:
            assert all(x0 == x1 or y0 == y1 for (x0, y0), (x1, y1) in zip(pts, pts[1:])), (a, b)
            for name, (x, y) in ((a, pts[0]), (b, pts[-1])):
                bx, by, bw, bh = nodes[name][3]
                on_edge = (bx <= x <= bx + bw and y in (by, by + bh)) or (by <= y <= by + bh and x in (bx, bx + bw))
                assert on_edge, f"{a} -> {b} does not touch {name} at {(x, y)}"
