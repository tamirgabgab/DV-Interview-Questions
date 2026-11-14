#!/usr/bin/env python3
"""The two diagrams of docs/how-built.md: the CI run of a push (.github/workflows/deploy.yml)
and how a question page becomes the site.

    python tools/figures/fill.py how-built       # rewrite the page's generated blocks

Each diagram is a static, complete SVG (nodes, connectors with their arrowheads, labels), and
over it a decorative copy (``sf-anim``, aria-hidden) that SMIL draws stage by stage: a
connector's copy is drawn in its time window, a node's frame lights when the run reaches it,
and the whole copy fades out at the end of the cycle and starts again. 28-site-flow.css hides
the copy under reduced motion and when the box's animation switch is off, and the CI
diagram's lane buttons (pure CSS, :has) pick which lane the copy runs on. Colours come only
from the stylesheet's classes.

Every element belongs to a lane: ``all`` (every push), ``full`` (a code change), ``fast``
(prose only) or ``done`` (a commit of main that already passed on its branch).
tests/tools/test_site_flow.py checks the CI diagram's edges against the workflow's ``needs``.
"""

from __future__ import annotations

STEP = 0.5          # seconds per stage
STAGES = 12         # one cycle: nine stages (0..8), then the full run holds, then it fades
DUR = STEP * STAGES

# --- the CI run -----------------------------------------------------------------------------
# name, Hebrew sub-label, lane, stage, (x, y, w, h)
CI_NODES = {
    "push": ("קומיט לענף", "all", 0, (130, 8, 100, 44)),
    "gate": ("מה השתנה?", "all", 2, (100, 92, 160, 44)),
    "test": ("כל הבדיקות", "full", 4, (244, 184, 108, 44)),
    "quick": ("רק מה שנגע", "fast", 4, (126, 184, 108, 44)),
    "build": ("בנייה, קישורים, טלפון", "all", 6, (8, 276, 228, 44)),
    "explorers": ("לוחצים על התיבות", "full", 6, (244, 276, 108, 44)),
    "deploy": ("רק ב-main", "all", 8, (100, 368, 160, 44)),
}
# from, to, lane, first stage, stages, points of the orthogonal route
CI_EDGES = [
    ("push", "gate", "all", 1, 1, [(180, 52), (180, 92)]),
    ("gate", "test", "full", 3, 1, [(216, 136), (216, 152), (298, 152), (298, 184)]),
    ("gate", "quick", "fast", 3, 1, [(180, 136), (180, 184)]),
    ("gate", "build", "done", 3, 3, [(144, 136), (144, 152), (40, 152), (40, 276)]),
    ("quick", "build", "fast", 5, 1, [(180, 228), (180, 276)]),
    ("test", "build", "full", 5, 1, [(280, 228), (280, 248), (212, 248), (212, 276)]),
    ("test", "explorers", "full", 5, 1, [(316, 228), (316, 276)]),
    ("build", "deploy", "all", 7, 1, [(150, 320), (150, 368)]),
    ("explorers", "deploy", "full", 7, 1, [(298, 320), (298, 390), (260, 390)]),
]
# a label beside a connector: text, lane, centre x, baseline y, mask width
CI_LABELS = [("כבר עבר בענף", "done", 86, 216, 76)]
CI_SIZE = (360, 420)

# --- a page into the site -------------------------------------------------------------------
PAGE_NODES = {
    "q‹id›.py": ("מחולל השרטוטים", "all", 0, (48, 8, 168, 44)),
    "‹id›-‹slug›.md": ("דף השאלה, טקסט וקוד", "all", 2, (48, 96, 168, 44)),
    "tests": ("מריצים את קוד הדף", "all", 4, (240, 96, 112, 44)),
    "hooks/questions.py": ("MkDocs וה-hook", "all", 4, (48, 184, 168, 44)),
    "explorer/*.js": ("קוד התיבות", "all", 4, (240, 184, 112, 44)),
    "site/": ("HTML, site.css ו-JS", "all", 6, (48, 272, 168, 44)),
    "check_*.py": ("טלפון, קישורים, תיבות", "all", 8, (48, 360, 168, 44)),
}
PAGE_EDGES = [
    ("q‹id›.py", "‹id›-‹slug›.md", "all", 1, 1, [(132, 52), (132, 96)]),
    ("‹id›-‹slug›.md", "tests", "all", 3, 1, [(216, 118), (240, 118)]),
    ("‹id›-‹slug›.md", "hooks/questions.py", "all", 3, 1, [(132, 140), (132, 184)]),
    ("hooks/questions.py", "site/", "all", 5, 1, [(132, 228), (132, 272)]),
    ("explorer/*.js", "site/", "all", 5, 1, [(296, 228), (296, 294), (216, 294)]),
    ("site/", "check_*.py", "all", 7, 1, [(132, 316), (132, 360)]),
]
PAGE_LABELS = [("fill.py", "all", 168, 78, 52)]
PAGE_SIZE = (360, 416)


def f(v: float) -> str:
    return f"{v:g}"


def route(pts, r=8):
    """An orthogonal polyline with its corners rounded by r."""
    d = f"M{f(pts[0][0])},{f(pts[0][1])}"
    for (x0, y0), (x1, y1), (x2, y2) in zip(pts, pts[1:], pts[2:]):
        sx, sy = (x1 > x0) - (x1 < x0), (y1 > y0) - (y1 < y0)       # into the corner
        tx, ty = (x2 > x1) - (x2 < x1), (y2 > y1) - (y2 < y1)       # out of it
        d += f" L{f(x1 - sx * r)},{f(y1 - sy * r)} Q{f(x1)},{f(y1)} {f(x1 + tx * r)},{f(y1 + ty * r)}"
    return d + f" L{f(pts[-1][0])},{f(pts[-1][1])}"


def head(pts):
    """The arrowhead at the route's end, pointing along its last segment."""
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    dx, dy = (x1 > x0) - (x1 < x0), (y1 > y0) - (y1 < y0)
    px, py = -dy, dx                                                 # across the segment
    a = (x1 - 8 * dx + 4 * px, y1 - 8 * dy + 4 * py)
    b = (x1 - 8 * dx - 4 * px, y1 - 8 * dy - 4 * py)
    return f"M{f(x1)},{f(y1)} L{f(a[0])},{f(a[1])} L{f(b[0])},{f(b[1])} Z"


def times(first: int, n: int) -> tuple[str, str]:
    """The key times of a window that starts at stage `first` and lasts `n` stages."""
    a, b = first / STAGES, (first + n) / STAGES
    return f"{a:.4f}", f"{b:.4f}"


def diagram(slug, label, desc, nodes, edges, labels, size) -> str:
    w, h = size
    out = [f'<svg class="figure sf-fig sf-{slug}" viewBox="0 0 {w} {h}" style="max-width:{w / 16:g}rem" role="img" '
           f'aria-labelledby="sf-{slug}-title sf-{slug}-desc">',
           f'<title id="sf-{slug}-title">{label}</title>', f'<desc id="sf-{slug}-desc">{desc}</desc>']
    for a, b, lane, *_rest, pts in edges:                            # connectors under the boxes
        out.append(f'<g class="sf-L-{lane}"><path class="sf-edge" d="{route(pts)}"/>'
                   f'<path class="sf-head" d="{head(pts)}"/></g>')
    for text, lane, x, y, mw in labels:
        out.append(f'<g class="sf-lab sf-L-{lane}"><rect x="{f(x - mw / 2)}" y="{f(y - 13)}" width="{mw}" height="18" rx="3"/>'
                   f'<text x="{f(x)}" y="{f(y)}" text-anchor="middle" direction="rtl">{text}</text></g>')
    for name, (sub, lane, _k, (x, y, bw, bh)) in nodes.items():
        cx = x + bw / 2
        out.append(f'<g class="sf-node sf-L-{lane}"><rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="6"/>'
                   f'<text class="sf-name" x="{f(cx)}" y="{y + 19}" text-anchor="middle">{name}</text>'
                   f'<text class="sf-sub" x="{f(cx)}" y="{y + 35}" text-anchor="middle" direction="rtl">{sub}</text></g>')
    # the decorative run: drawn connectors and lit frames, faded together at the cycle's end
    out.append(f'<g class="sf-anim" aria-hidden="true">'
               f'<animate attributeName="opacity" dur="{DUR:g}s" repeatCount="indefinite" '
               f'values="1;1;0;0" keyTimes="0;{(STAGES - 1.6) / STAGES:.4f};{(STAGES - 0.6) / STAGES:.4f};1"/>')
    for a, b, lane, first, n, pts in edges:
        t0, t1 = times(first, n)
        out.append(f'<path class="sf-run sf-L-{lane}" d="{route(pts)}" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1">'
                   f'<animate attributeName="stroke-dashoffset" dur="{DUR:g}s" repeatCount="indefinite" '
                   f'values="1;1;0;0" keyTimes="0;{t0};{t1};1"/></path>')
    for name, (sub, lane, k, (x, y, bw, bh)) in nodes.items():
        t0, t1 = times(k, 0.4)
        out.append(f'<rect class="sf-lit sf-L-{lane}" x="{x}" y="{y}" width="{bw}" height="{bh}" rx="6" opacity="0">'
                   f'<animate attributeName="opacity" dur="{DUR:g}s" repeatCount="indefinite" '
                   f'values="0;0;1;1" keyTimes="0;{t0};{t1};1"/></rect>')
    out.append("</g></svg>")
    return "\n".join(out)


CI_LANES = [
    ("full", "שינוי בקוד", True),
    ("fast", "רק טקסט", False),
    ("done", "כבר עבר בענף", False),
]


def controls(slug: str, lanes: bool) -> str:
    """The box's buttons: the lanes (CI only) and the animation switch."""
    s = '<div class="sf-controls">'
    if lanes:
        s += ('<fieldset class="sf-lanes"><legend>איזו דחיפה :</legend>'
              + "".join(f'<label><input type="radio" name="sf-{slug}-lane" value="{v}"{" checked" if on else ""}>'
                        f'<span>{t}</span></label>' for v, t, on in CI_LANES)
              + "</fieldset>")
    s += '<label class="sf-play"><input type="checkbox" checked><span>הנפשה</span></label></div>'
    return s


def blocks() -> list[str]:
    ci = diagram("ci", "ריצת ה-CI של דחיפה",
                 "דחיפה עוברת ב-gate, שבוחר אחד משלושה מסלולים: שינוי קוד מריץ את test ואחריו build "
                 "ו-explorers במקביל, שינוי טקסט בלבד מריץ את quick ואחריו build, וקומיט שכבר עבר בענף "
                 "הולך ישר ל-build. deploy מפרסם את האתר, רק ב-main.",
                 CI_NODES, CI_EDGES, CI_LABELS, CI_SIZE)
    page = diagram("page", "איך דף שאלה נעשה לאתר",
                   "מחולל השרטוטים כותב את השרטוטים לתוך דף השאלה עם fill.py. הבדיקות מריצות את קוד הדף, "
                   "MkDocs וה-hook בונים ממנו את האתר יחד עם קוד התיבות, ובדיקות האתר עוברות על הדפים הבנויים.",
                   PAGE_NODES, PAGE_EDGES, PAGE_LABELS, PAGE_SIZE)
    return [
        f'<div class="sf-box" data-sf="ci">\n{controls("ci", True)}\n<div class="sf-scroll">\n{ci}\n</div>\n</div>',
        f'<div class="sf-box" data-sf="page">\n{controls("page", False)}\n<div class="sf-scroll">\n{page}\n</div>\n</div>',
    ]


if __name__ == "__main__":
    for b in blocks():
        print(b, "\n")
