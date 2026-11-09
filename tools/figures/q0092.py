#!/usr/bin/env python3
"""Figures and tables of question 0092: points on a circle, every pair joined by a chord, and
the number of regions of the disc (Moser's circle problem).

    python tools/figures/fill.py 92        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. The reference here is independent of the page's code (the tests compare the
two). Counting: points labelled 0..n-1 around the circle; chords (a, b) and (c, d) cross
inside the disc exactly when one of c, d lies strictly between a and b and the other does
not. Geometry: the points at given angles, every pair of chords intersected, points closer
than 1e-7 merged (three chords through one point in a regular polygon), then Euler's formula
on the planar graph of the points, the crossings, the chord pieces and the arcs: regions
inside = E - V + 1. The faces themselves are traced by a half-edge walk (each region is
convex, so its centroid labels it). The same model is in the box
(docs/javascripts/explorer/circlecut.js).
"""

import itertools
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from charts import Chart  # noqa: E402

N5 = [90 + 72 * k for k in range(5)]                     # part a: five points (a regular pentagon)
N6 = [85, 152, 203, 271, 324, 32]                        # part b: six points in general position
REG6 = [90 + 60 * k for k in range(6)]                   # part c: the regular hexagon (30 regions)
MERGE = 1e-7


# --- counting ------------------------------------------------------------------------------------

def moser(n):
    return math.comb(n, 4) + math.comb(n, 2) + 1


def crosses(a, b, c, d):
    """Do chords (a, b) and (c, d), labels around the circle with a < b, cross inside?"""
    return (a < c < b) != (a < d < b) and len({a, b, c, d}) == 4


def chord_increments(n):
    """[(a, b, k, added)]: the chords in the order (0, 1), (0, 2), ..., each with the number of
    earlier chords it crosses and the regions it adds (k + 1)."""
    out, done = [], []
    for a, b in itertools.combinations(range(n), 2):
        k = sum(crosses(a, b, c, d) for c, d in done)
        out.append((a, b, k, k + 1))
        done.append((a, b))
    return out


# --- geometry ------------------------------------------------------------------------------------

def points(angles):
    return [(math.cos(math.radians(t)), math.sin(math.radians(t))) for t in angles]


def _cut(p, q, r, s):
    """The crossing of segments pq and rs strictly inside both: (x, y, t along pq), or None."""
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p, q, r, s
    den = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
    if abs(den) < 1e-14:
        return None
    t = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / den
    u = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / den
    if 1e-9 < t < 1 - 1e-9 and 1e-9 < u < 1 - 1e-9:
        return x1 + t * (x2 - x1), y1 + t * (y2 - y1), t
    return None


def arrangement(angles):
    """(P, chords, inner, on): the points, the chords as index pairs, the distinct crossing
    points, and for every chord {crossing index: position t along the chord}."""
    P = points(angles)
    chords = list(itertools.combinations(range(len(P)), 2))
    inner, on = [], {c: {} for c in chords}

    def index(x, y):
        for k, (a, b) in enumerate(inner):
            if abs(a - x) < MERGE and abs(b - y) < MERGE:
                return k
        inner.append((x, y))
        return len(inner) - 1

    for c1, c2 in itertools.combinations(chords, 2):
        if len(set(c1) | set(c2)) < 4:
            continue
        hit = _cut(P[c1[0]], P[c1[1]], P[c2[0]], P[c2[1]])
        if hit:
            k = index(hit[0], hit[1])
            on[c1][k] = hit[2]
            on[c2][k] = _cut(P[c2[0]], P[c2[1]], P[c1[0]], P[c1[1]])[2]
    return P, chords, inner, on


def counts(angles):
    """(V, E, regions): the planar graph of points, crossings, chord pieces and arcs."""
    n = len(angles)
    if n == 0:
        return 0, 0, 1
    _, chords, inner, on = arrangement(angles)
    V = n + len(inner)
    E = n + sum(len(on[c]) + 1 for c in chords)          # n arcs; a chord through k points is k + 1 pieces
    return V, E, E - V + 1


def regions(angles):
    return counts(angles)[2]


def triple_points(angles):
    """The crossing points where three or more chords meet, with how many chords."""
    _, chords, inner, on = arrangement(angles)
    through = [sum(k in on[c] for c in chords) for k in range(len(inner))]
    return [(inner[k], m) for k, m in enumerate(through) if m >= 3]


def faces(angles):
    """The regions as closed walks: lists of (kind, from, to) with kind "chord" or "arc"
    (an arc goes counter-clockwise from point i to point i + 1 around the circle). The walk
    keeps every region on its left; the outside of the disc is dropped."""
    n = len(angles)
    P, chords, inner, on = arrangement(angles)
    order = sorted(range(n), key=lambda i: angles[i] % 360)
    pos = list(P) + list(inner)                           # vertex positions: points, then crossings
    edges = []                                             # (kind, u, v)
    for k in range(n):
        edges.append(("arc", order[k], order[(k + 1) % n]))
    for a, b in chords:
        seq = [a] + [n + k for k, _ in sorted(on[(a, b)].items(), key=lambda kv: kv[1])] + [b]
        edges.extend(("chord", u, v) for u, v in zip(seq, seq[1:]))
    theta = {i: math.radians(angles[i]) for i in range(n)}

    def out_angle(e, forward):
        kind, u, v = edges[e]
        start = u if forward else v
        if kind == "arc":                                  # the tangent: +90° going counter-clockwise
            return theta[start] + (math.pi / 2 if forward else -math.pi / 2)
        end = v if forward else u
        return math.atan2(pos[end][1] - pos[start][1], pos[end][0] - pos[start][0])

    outgoing = {}
    for e, (_, u, v) in enumerate(edges):
        outgoing.setdefault(u, []).append((e, True))
        outgoing.setdefault(v, []).append((e, False))
    for vtx in outgoing:
        outgoing[vtx].sort(key=lambda h: out_angle(*h) % (2 * math.pi))
    seen, found = set(), []
    for start in [(e, f) for e in range(len(edges)) for f in (True, False)]:
        if start in seen:
            continue
        walk, h = [], start
        while h not in seen:
            seen.add(h)
            e, f = h
            kind, u, v = edges[e]
            a, b = (u, v) if f else (v, u)
            walk.append((kind, a, b, f))
            ring = outgoing[b]                             # turn: the next edge clockwise after the way back
            i = ring.index((e, not f))
            h = ring[(i - 1) % len(ring)]
        found.append(walk)

    def area(walk):
        pts = sample(walk, angles, pos)
        return sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1])) / 2

    inside = [w for w in found if area(w) > 1e-12]

    def where(w):                                          # number the regions from the centre outwards
        pts = sample(w, angles, pos)
        gx, gy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
        return round(math.hypot(gx, gy), 3), round((math.pi / 2 - math.atan2(gy, gx)) % (2 * math.pi), 3)

    return sorted(inside, key=where), pos


def sample(walk, angles, pos):
    """A face as a polygon: chord pieces as their ends, arcs sampled every few degrees."""
    out = []
    for kind, a, b, forward in walk:
        if kind == "chord":
            out.append(pos[a])
            continue
        t0, t1 = math.radians(angles[a]), math.radians(angles[b])
        span = (t1 - t0) % (2 * math.pi) if forward else -((t0 - t1) % (2 * math.pi))
        if abs(span) < 1e-12:
            span = 2 * math.pi if forward else -2 * math.pi
        steps = max(2, int(abs(span) / 0.08))
        out.extend((math.cos(t0 + span * s / steps), math.sin(t0 + span * s / steps)) for s in range(steps))
    return out


# --- drawing -------------------------------------------------------------------------------------

COLOURS = 6


def colour_faces(fs, angles, pos):
    """A colour per region, neighbours (sharing a piece of chord) different. Two colours would
    do (the map of chords is two-colourable), so each region starts at its own turn of a
    palette of six and skips the colours of its neighbours."""
    side = {}
    for i, w in enumerate(fs):
        for kind, a, b, _ in w:
            side.setdefault((kind, min(a, b), max(a, b)), []).append(i)
    nb = {i: set() for i in range(len(fs))}
    for owners in side.values():
        for i, j in itertools.combinations(owners, 2):
            nb[i].add(j)
            nb[j].add(i)
    col = {}
    for v in sorted(nb):                                   # spread the colours: start each region at its own
        used = {col[u] for u in nb[v] if u in col}         # turn of the palette, skip a neighbour's colour
        col[v] = next((v + j) % COLOURS for j in range(COLOURS) if (v + j) % COLOURS not in used)
    return [col[i] for i in range(len(fs))]


def disc_svg(angles, *, R=110, pad=26, labels=False, label_points=True, cls="", aria="", triple=False):
    cx = cy = R + pad
    size = 2 * (R + pad)

    def xy(p):
        return cx + R * p[0], cy - R * p[1]

    fs, pos = faces(angles)
    cols = colour_faces(fs, angles, pos)
    out = [f'<svg class="figure mc-fig{(" " + cls) if cls else ""}" viewBox="0 0 {size} {size}" '
           f'style="max-width:{size / 16:.1f}rem" role="img" aria-label="{aria}">']
    for i, (w, c) in enumerate(zip(fs, cols)):
        d = []
        for kind, a, b, forward in w:
            x0, y0 = xy(pos[a])
            if not d:
                d.append(f"M{x0:.1f},{y0:.1f}")
            x1, y1 = xy(pos[b])
            if kind == "chord":
                d.append(f"L{x1:.1f},{y1:.1f}")
            else:
                t0, t1 = angles[a] % 360, angles[b] % 360
                span = (t1 - t0) % 360 if forward else (t0 - t1) % 360
                if span == 0:
                    span = 360
                large = 1 if span > 180 else 0
                sweep = 0 if forward else 1                 # counter-clockwise on screen is sweep 0
                if span == 360:                             # a whole circle: two halves
                    xm, ym = cx - (x0 - cx), cy - (y0 - cy)
                    d.append(f"A{R},{R} 0 0 {sweep} {xm:.1f},{ym:.1f}A{R},{R} 0 0 {sweep} {x1:.1f},{y1:.1f}")
                else:
                    d.append(f"A{R},{R} 0 {large} {sweep} {x1:.1f},{y1:.1f}")
        out.append(f'<path class="mc-reg mc-c{c}" d="{"".join(d)}Z"/>')
    out.append(f'<circle class="mc-ring" cx="{cx}" cy="{cy}" r="{R}"/>')
    P = points(angles)
    for a, b in itertools.combinations(range(len(P)), 2):
        (x1, y1), (x2, y2) = xy(P[a]), xy(P[b])
        out.append(f'<line class="mc-chord" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    if triple:
        for (x, y), _ in triple_points(angles):
            X, Y = xy((x, y))
            out.append(f'<circle class="mc-triple" cx="{X:.1f}" cy="{Y:.1f}" r="7"/>')
    if labels:
        for i, w in enumerate(fs):
            pts = sample(w, angles, pos)
            gx = sum(p[0] for p in pts) / len(pts)
            gy = sum(p[1] for p in pts) / len(pts)
            X, Y = xy((gx, gy))
            out.append(f'<text class="mc-num" x="{X:.1f}" y="{Y + 4:.1f}" text-anchor="middle">{i + 1}</text>')
    for k, p in enumerate(P):
        X, Y = xy(p)
        out.append(f'<circle class="mc-pt" cx="{X:.1f}" cy="{Y:.1f}" r="5.5"/>')
        if label_points:
            lx, ly = cx + (R + 15) * p[0], cy - (R + 15) * p[1]
            out.append(f'<text class="mc-plab" x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="middle">{k + 1}</text>')
    out.append("</svg>")
    return "".join(out)


# --- the statement: one to four points ----------------------------------------------------------

SMALL = {1: [90], 2: [90, 270], 3: [90, 210, 330], 4: [60, 150, 240, 330]}


def statement_figure():
    R, pad, gap = 46, 12, 18
    cell = 2 * (R + pad)
    W, H = 4 * cell + 3 * gap, cell + 30
    out = [f'<svg class="figure mc-fig mc-row" viewBox="0 0 {W} {H}" style="max-width:{W / 16:.1f}rem" role="img" '
           f'aria-label="עיגולים עם נקודה אחת, שתיים, שלוש וארבע, וכל זוג נקודות מחובר בקו. מספר החלקים : 1, 2, 4 ו-8">']
    for i, n in enumerate((1, 2, 3, 4)):
        ox = W - (i + 1) * cell - i * gap                 # right to left: the page reads from the right
        inner = disc_svg(SMALL[n], R=R, pad=pad, label_points=False, aria="")
        body = inner[inner.index(">") + 1:-len("</svg>")]
        out.append(f'<g transform="translate({ox},0)">{body}</g>')
        out.append(f'<text class="mc-count" x="{ox + cell / 2:.1f}" y="{H - 6}" text-anchor="middle">n = {n} : {regions(SMALL[n])}</text>')
    out.append("</svg>")
    return "".join(out)


def statement_legend():
    return ('<span class="viz-legend"><span><i class="mc-key-pt"></i>נקודה על המעגל</span>'
            '<span><i class="mc-key-reg"></i>חלק של העיגול, כל חלק בצבע משלו</span></span>')


# --- part a: five points --------------------------------------------------------------------------

def five_figure():
    return disc_svg(N5, labels=True, aria="חמש נקודות על מעגל וכל עשרת הקווים ביניהן. העיגול מתחלק ל-16 חלקים, ממוספרים 1 עד 16 : מחומש באמצע, חמישה משולשים סביבו, עוד חמישה ליד הצלעות, וחמש קשתות")


def five_table():
    rows = ["| הקו | חוצה קווים קודמים | חלקים שהוא מוסיף | חלקים אחריו |", "|:-:|:-:|:-:|:-:|"]
    total = 1
    for a, b, k, add in chord_increments(5):
        total += add
        rows.append(f"| {a + 1} ו-{b + 1} | {k} | {add} | {total} |")
    return "\n".join(rows)


# --- part b: six points, the formula ----------------------------------------------------------------

def six_figure():
    return disc_svg(N6, aria="שש נקודות במצב כללי וכל חמישה-עשר הקווים ביניהן. 15 נקודות חיתוך, ו-31 חלקים, לא 32")


def euler_table():
    rows = ["| ‏n | נקודות על המעגל | נקודות חיתוך | קודקודים V | צלעות E | חלקים E − V + 1 | 2 בחזקת n − 1 |",
            "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for n in range(1, 11):
        V = n + math.comb(n, 4)
        E = n + math.comb(n, 2) + 2 * math.comb(n, 4)
        rows.append(f"| {n} | {n} | {math.comb(n, 4)} | {V} | {E} | {E - V + 1} | {2 ** (n - 1)} |")
    return "\n".join(rows)


def pattern_chart():
    c = Chart("מספר החלקים לפי n, מול 2 בחזקת n פחות 1 : עד n = 5 הם שווים, ומ-6 החלקים מפגרים : 31 מול 32, 57 מול 64, 256 מול 512",
              slots=10, y_max=520, h=250, base=210)
    c.grid_y([0, 128, 256, 384, 512])
    for n in range(1, 11):
        c.add(f'<rect class="mc-bar-pow" x="{c.X(n) - c.slot * 0.36:.1f}" y="{c.Y(2 ** (n - 1)):.1f}" '
              f'width="{c.slot * 0.34:.1f}" height="{c.base - c.Y(2 ** (n - 1)):.1f}" rx="2"/>')
        c.add(f'<rect class="mc-bar-reg" x="{c.X(n) + c.slot * 0.02:.1f}" y="{c.Y(moser(n)):.1f}" '
              f'width="{c.slot * 0.34:.1f}" height="{c.base - c.Y(moser(n)):.1f}" rx="2"/>')
        if n >= 6:
            c.add(f'<text class="tick" x="{c.X(n) + c.slot * 0.19:.1f}" y="{c.Y(moser(n)) - 5:.1f}" text-anchor="middle">{moser(n)}</text>')
    c.x_ticks(range(1, 11))
    c.axis("n")
    return c.svg().replace('class="perf-chart"', 'class="perf-chart mc-chart"', 1)


def pattern_legend():
    return ('<span class="viz-legend"><span><i class="mc-key-reg2"></i>מספר החלקים</span>'
            '<span><i class="mc-key-pow"></i>2 בחזקת n − 1, הדפוס של 1, 2, 4, 8, 16</span></span>')


# --- part c: the regular hexagon -------------------------------------------------------------------

def regular_figure():
    return disc_svg(REG6, triple=True, aria="משושה משוכלל וכל הקווים בין קודקודיו. שלושת הקטרים נפגשים במרכז, ולכן יש רק 13 נקודות חיתוך ו-30 חלקים במקום 31")


def regular_legend():
    return ('<span class="viz-legend"><span><i class="mc-key-triple"></i>נקודה שבה שלושה קווים נפגשים</span></span>')


def regular_table():
    rows = ["| ‏n | נקודות במצב כללי | מצולע משוכלל | ההפרש |", "|:-:|:-:|:-:|:-:|"]
    for n in range(3, 13):
        reg = regions([90 + 360 * k / n for k in range(n)])
        rows.append(f"| {n} | {moser(n)} | {reg} | {moser(n) - reg} |")
    return "\n".join(rows)


def blocks():
    return [statement_figure(), statement_legend(), five_figure(), five_table(), six_figure(), euler_table(),
            pattern_chart(), pattern_legend(), regular_figure(), regular_legend(), regular_table()]


if __name__ == "__main__":
    for b in blocks():
        print(b[:200], "...\n")
