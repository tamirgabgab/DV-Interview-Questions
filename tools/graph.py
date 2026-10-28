#!/usr/bin/env python3
"""Write docs/graph.html: an interactive knowledge graph of the questions and the
techniques their solutions use, drawn with graphify (https://pypi.org/project/graphifyy/).

    pip install graphifyy          # not a site dependency; only this script needs it
    python tools/graph.py          # rewrite docs/graph.html from tools/graph_concepts.json

tools/graph_concepts.json is the data: for every question its core concepts (the idea the
solution is built on), its secondary concepts, and the questions it is related to (explicit:
the page links to it). It was written by reading every page (graphify's semantic pass);
update it by hand when a question is added. Question titles and levels come from the pages'
front matter, so they never go stale.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from catalog import ROOT, pages  # noqa: E402

DATA = ROOT / "tools" / "graph_concepts.json"
OUT = ROOT / "docs" / "graph.html"
GROUP_HE = {"algorithms": "אלגוריתמים", "math": "מתמטיקה", "probability": "הסתברות",
            "puzzles": "חידות", "digital design": "תכנון לוגי", "verification": "אימות",
            "protocols": "פרוטוקולים"}


def extraction(data: dict) -> dict:
    """graphify's extraction dict: a node per question and per concept, and the edges."""
    nodes, edges = [], []
    known = {}
    for qid, title, level, path in pages(ROOT):
        key = f"{qid:04d}"
        known[key] = f"q{key}"
        nodes.append({"id": f"q{key}", "label": f"{key} {title.split(' – ')[0]}",
                      "file_type": "document", "source_file": path})
    for cid, c in data["concepts"].items():
        nodes.append({"id": f"c_{cid}", "label": c["label"], "file_type": "concept",
                      "source_file": GROUP_HE.get(c["group"], c["group"])})

    def edge(a, b, relation, weight, confidence):
        edges.append({"source": a, "target": b, "relation": relation, "weight": weight,
                      "confidence": "EXTRACTED" if confidence == 1.0 else "INFERRED",
                      "confidence_score": confidence, "source_file": "tools/graph_concepts.json"})

    for key, q in data["questions"].items():
        for cid in q["core"]:
            edge(known[key], f"c_{cid}", "uses", 2.0, 1.0)
        for cid in q["secondary"]:
            edge(known[key], f"c_{cid}", "uses", 1.0, 0.85)
        for r in q["related"]:
            if r["id"] in known and r["id"] != key:
                edge(known[key], known[r["id"]], "references" if r["explicit"]
                     else "semantically_similar_to", 1.0, 1.0 if r["explicit"] else 0.75)
    return {"nodes": nodes, "edges": edges, "hyperedges": []}


def community_names(G, communities: dict[int, list[str]]) -> dict[int, str]:
    """Name each community after its two most connected concepts."""
    names = {}
    for cid, members in communities.items():
        concepts = sorted((n for n in members if n.startswith("c_")),
                          key=lambda n: (-G.degree(n), n))
        names[cid] = " / ".join(G.nodes[n]["label"] for n in concepts[:2]) or f"Group {cid}"
    return names


# The page opens a question when its node is clicked: the side panel shows its link.
SOURCE_JS = "html += `<div class=\"field\">Source: ${esc(n.source_file || '-')}</div>`;"
LINK_JS = ("html += n.file_type === 'document'"
           " ? `<div class=\"field\"><a href=\"${esc(n.source_file)}\" style=\"color:#7cc4ff\">"
           "לעמוד השאלה</a></div>`"
           " : `<div class=\"field\">${esc(n.source_file || '-')}</div>`;")

# Hebrew labels: the canvas draws right to left, and every text in the side panel takes
# its direction from its first letter. Below 700 px the side panel moves under the graph.
EXTRA_CSS = """
  #graph { direction: rtl; }
  #info-content .field, .neighbor-link, .search-item, .legend-label { unicode-bidi: plaintext; text-align: start; }
  #map-head { padding: 10px 14px; border-bottom: 1px solid var(--border); font-size: 12px; color: var(--text-2); line-height: 1.5; direction: rtl; }
  #map-head b { display: block; font-size: 14px; color: var(--text); }
  #map-head a { color: #7cc4ff; }
  @media (max-width: 700px) {
    body { flex-direction: column; height: auto; min-height: 100vh; overflow: auto; }
    #graph { flex: none; height: 62vh; }
    #sidebar { width: 100%; border-left: 0; border-top: 1px solid var(--border); }
  }
"""
HEADER = ('<div id="map-head"><b>מפת השאלות</b>כל שאלה מחוברת לטכניקות שהפתרון שלה משתמש בהן.'
          ' לחיצה על שאלה מראה קישור לעמוד שלה. <a href="./">חזרה לאתר</a></div>')


def main() -> int:
    from graphify.build import build_from_json
    from graphify.cluster import cluster
    from graphify.exporters.html import to_html

    data = json.loads(DATA.read_text(encoding="utf-8"))
    G = build_from_json(extraction(data), directed=False, dedup=False)
    communities = cluster(G)
    to_html(G, communities, str(OUT), community_labels=community_names(G, communities))
    html = OUT.read_text(encoding="utf-8")
    if SOURCE_JS not in html:
        print("graph.py: graphify's side panel changed; the question links were not added")
        return 1
    html = html.replace(SOURCE_JS, LINK_JS)
    html = html.replace("</style>", EXTRA_CSS + "</style>", 1)
    html = html.replace('<div id="sidebar">', '<div id="sidebar">' + HEADER, 1)
    html = re.sub(r"<title>.*?</title>", "<title>מפת השאלות – DV Interview Questions</title>", html, count=1)
    OUT.write_text(html, encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)}: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges,"
          f" {len(communities)} groups")
    return 0


if __name__ == "__main__":
    sys.exit(main())
