#!/usr/bin/env python3
"""Figures and tables of question 0030 (spider and fly: the shortest path on a box).

    python tools/figures/fill.py 30        # put the blocks on the page

The box is [0, a] x [0, b] x [0, h]; the spider sits on the end face x = 0 and the fly on
the end face x = a. The four lateral faces are unrolled into a strip along x with the
perimeter coordinate p running bottom -> sideB -> top -> side0 (period 2(b + h)); an end
face folded flat on one of its edges puts the point at x = -distance (or a + distance).
That is the method of part b, and every figure here is drawn in those (x, p) coordinates.

blocks() returns, in page order: the box with S and F, the net of the route over the top
(42), the net of the best route (40), the table of all valid straight lines (the candidate
routes), the periodic strip with the images of S and F, and the table of those images.
tests/0030 checks the numbers and that the page copies match.
"""

import math
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

A, B, H = 30, 12, 12                      # the room of the question
S = (0, 6, 11)                            # the spider: on x = 0, one unit below the ceiling
F = (30, 6, 1)                            # the fly: on x = a, one unit above the floor
EDGES = ("bottom", "sideB", "top", "side0")
HEB = {"bottom": "הרצפה", "sideB": "הקיר הרחוק", "top": "התקרה", "side0": "הקיר הקרוב",
       "end0": "הקיר של העכביש", "enda": "הקיר של הזבוב"}


# --- the strip ----------------------------------------------------------------------------

def period(b=B, h=H):
    return 2 * (b + h)


def bands(b=B, h=H):
    """The p-range of each lateral face, in strip order."""
    return {"bottom": (0, b), "sideB": (b, b + h), "top": (b + h, 2 * b + h), "side0": (2 * b + h, 2 * (b + h))}


def images(y, z, b=B, h=H):
    """The four images of a point (y, z) of an end face, one per edge it can leave through:
    (edge, distance to the edge, p of the foot of the perpendicular, p-range of the edge)."""
    y, z = Fr(y), Fr(z)
    rng = bands(b, h)
    return [("bottom", z, y, *rng["bottom"]),
            ("sideB", b - y, b + z, *rng["sideB"]),
            ("top", h - z, b + h + (b - y), *rng["top"]),
            ("side0", y, 2 * b + h + (h - z), *rng["side0"])]


def edge_point(edge, p, b=B, h=H):
    """The point (y, z) of an end face at perimeter coordinate p (p inside the edge's range)."""
    p = Fr(p) % period(b, h)
    return {"bottom": (p, Fr(0)), "sideB": (Fr(b), p - b), "top": (b - (p - b - h), Fr(h)),
            "side0": (Fr(0), h - (p - 2 * b - h))}[edge]


def band_of(p, b=B, h=H):
    p = Fr(p) % period(b, h)
    for name, (lo, hi) in bands(b, h).items():
        if lo <= p < hi:
            return name
    raise ValueError(p)


def faces_between(p_from, p_to, b=B, h=H):
    """The lateral faces a straight strip line crosses from p_from to p_to, in order."""
    P = period(b, h)
    out, p = [], Fr(p_from)
    step = 1 if p_to >= p_from else -1
    cuts = sorted({lo + k * P for lo in (0, b, b + h, 2 * b + h) for k in range(-2, 3)})
    out.append(band_of(p if step > 0 else p - Fr(1, 10 ** 9), b, h))
    while True:
        nxt = min((c for c in cuts if c > p), default=None) if step > 0 else max((c for c in cuts if c < p), default=None)
        if nxt is None or (step > 0 and nxt >= p_to) or (step < 0 and nxt <= p_to):
            return out
        p = nxt
        out.append(band_of(p if step > 0 else p - Fr(1, 10 ** 9), b, h))


def candidates(a=A, b=B, h=H, s=S, f=F):
    """Every straight line of the strip method: (length, s_edge, f_edge, k, dx, dp, p_exit,
    p_enter, valid, faces). Exact fractions; the length is a float."""
    P = period(b, h)
    out = []
    for es, ds, ps, s_lo, s_hi in images(s[1], s[2], b, h):
        for ef, df, pf, f_lo, f_hi in images(f[1], f[2], b, h):
            for k in (-1, 0, 1):
                dx = a + df + ds
                dp = pf + k * P - ps
                p_exit = ps + dp * ds / dx
                p_enter = ps + dp * (ds + a) / dx
                valid = s_lo <= p_exit <= s_hi and f_lo + k * P <= p_enter <= f_hi + k * P
                seq = ["end0"] + (faces_between(p_exit, p_enter, b, h) if valid else []) + ["enda"]
                out.append(dict(length=math.hypot(dx, dp), s_edge=es, f_edge=ef, k=k, dx=dx, dp=dp,
                                p_exit=p_exit, p_enter=p_enter, valid=valid, faces=seq))
    return sorted(out, key=lambda c: (c["length"], len(c["faces"]), c["s_edge"], c["f_edge"], c["k"]))


def best(a=A, b=B, h=H, s=S, f=F):
    return next(c for c in candidates(a, b, h, s, f) if c["valid"])


def num(v, digits=2):
    """A number without trailing zeros: 40, 6.75, 40.72."""
    if isinstance(v, Fr) and v.denominator == 1:
        return str(v.numerator)
    s = f"{float(v):.{digits}f}".rstrip("0").rstrip(".")
    return s


# --- drawing helpers ------------------------------------------------------------------

def svg_open(w, h, label, cls="figure", max_rem=None):
    style = f' style="max-width:{max_rem}rem"' if max_rem else ""
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}"{style} role="img" aria-label="{label}">'


def text(x, y, s, cls="legend", anchor="middle", size=None, rtl=False, extra=""):
    st = f' style="font-size:{size}px"' if size else ""
    d = ' direction="rtl"' if rtl else ""
    return f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}"{st}{d}{extra}>{s}</text>'


def dot(x, y, cls, r=5, title=None):
    t = f"<title>{title}</title>" if title else ""
    return f'<circle class="{cls}-dot" cx="{x:.1f}" cy="{y:.1f}" r="{r}">{t}</circle>'


class Net:
    """A net drawn in (x, p) coordinates: x to the right, p upwards."""

    def __init__(self, x_lo, x_hi, p_lo, p_hi, scale, pad=(28, 16, 28, 22), label="", max_rem=40):
        self.scale = scale
        self.x_lo, self.p_lo = x_lo, p_lo
        l, t, r, b = pad
        self.w = int((x_hi - x_lo) * scale + l + r)
        self.h = int((p_hi - p_lo) * scale + t + b)
        self.l, self.t = l, t
        self.base = self.h - b
        self.parts = [svg_open(self.w, self.h, label, max_rem=max_rem)]

    def X(self, x):
        return self.l + (float(x) - self.x_lo) * self.scale

    def Y(self, p):
        return self.base - (float(p) - self.p_lo) * self.scale

    def add(self, s):
        self.parts.append(s)
        return self

    def rect(self, x0, x1, p0, p1, cls, name=None, title=None, label_size=16):
        """A face; its name sits in the top-left corner, away from the path."""
        X0, X1, Y0, Y1 = self.X(x0), self.X(x1), self.Y(p1), self.Y(p0)
        t = f"<title>{title}</title>" if title else ""
        self.add(f'<rect class="{cls}" x="{X0:.1f}" y="{Y0:.1f}" width="{X1 - X0:.1f}" height="{Y1 - Y0:.1f}">{t}</rect>')
        if name:
            self.add(text(X0 + 7, Y0 + label_size + 4, name, anchor="start", size=label_size))
        return self

    def line(self, x0, p0, x1, p1, cls="ink-line", width=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line class="{cls}" x1="{self.X(x0):.1f}" y1="{self.Y(p0):.1f}" x2="{self.X(x1):.1f}" '
                 f'y2="{self.Y(p1):.1f}" stroke-width="{width}"{d}/>')
        return self

    def point(self, x, p, cls, label=None, dx=0, dy=-11, r=5, title=None, size=18):
        self.add(dot(self.X(x), self.Y(p), cls, r, title))
        if label:
            self.add(text(self.X(x) + dx, self.Y(p) + dy, label, size=size))
        return self

    def label(self, x, p, s, dx=0, dy=0, size=None, anchor="middle", cls="legend", rtl=False):
        self.add(text(self.X(x) + dx, self.Y(p) + dy, s, cls=cls, anchor=anchor, size=size, rtl=rtl))
        return self

    def svg(self):
        return "".join(self.parts) + "</svg>"


# --- figures ----------------------------------------------------------------------------

def box_svg(a=A, b=B, h=H, s=S, f=F):
    """The room in an oblique view, with the spider and the fly and their offsets."""
    sc, ky = 12, 0.42                                  # px per unit, the receding y axis
    ox, oy = 50, 236
    P = lambda x, y, z: (ox + sc * x + sc * ky * y, oy - sc * z - sc * ky * y)
    w, hh = int(ox + sc * a + sc * ky * b + 60), int(oy + 30)
    out = [svg_open(w, hh, f"קופסה באורך {a}, רוחב {b} וגובה {h} : העכביש על הקיר השמאלי, {s[2]} מתחת לתקרה, "
                    f"והזבוב על הקיר הימני, {f[2]} מעל הרצפה, שניהם באמצע הרוחב", max_rem=36)]
    c = {k: P(*v) for k, v in dict(A=(0, 0, 0), Bc=(a, 0, 0), C=(a, b, 0), D=(0, b, 0),
                                   E=(0, 0, h), Fc=(a, 0, h), G=(a, b, h), Hc=(0, b, h)).items()}
    poly = lambda *ks: " ".join(f"{c[k][0]:.1f},{c[k][1]:.1f}" for k in ks)
    out.append(f'<polygon class="box-end" points="{poly("A", "D", "Hc", "E")}"><title>{HEB["end0"]} (x = 0)</title></polygon>')
    out.append(f'<polygon class="box-face" points="{poly("E", "Fc", "G", "Hc")}"><title>{HEB["top"]}</title></polygon>')
    out.append(f'<polygon class="box-face" points="{poly("A", "Bc", "Fc", "E")}"><title>{HEB["side0"]}</title></polygon>')
    out.append(f'<polygon class="box-end" points="{poly("Bc", "C", "G", "Fc")}" style="fill-opacity:0.25"><title>{HEB["enda"]} (x = {a})</title></polygon>')
    for u, v in (("A", "Bc"), ("Bc", "Fc"), ("Fc", "E"), ("E", "A"), ("E", "Hc"), ("Hc", "G"), ("G", "Fc"), ("A", "D"), ("D", "Hc")):
        out.append(f'<line class="box-edge" x1="{c[u][0]:.1f}" y1="{c[u][1]:.1f}" x2="{c[v][0]:.1f}" y2="{c[v][1]:.1f}"/>')
    for u, v in (("D", "C"), ("C", "Bc"), ("C", "G")):
        out.append(f'<line class="box-edge" x1="{c[u][0]:.1f}" y1="{c[u][1]:.1f}" x2="{c[v][0]:.1f}" y2="{c[v][1]:.1f}" stroke-dasharray="5 4"/>')
    # dimensions
    out.append(text((c["A"][0] + c["Bc"][0]) / 2, c["A"][1] + 18, f"a = {a}", size=14))
    out.append(text(c["Bc"][0] + 24, (c["Bc"][1] + c["Fc"][1]) / 2 + 5, f"h = {h}", size=14))
    out.append(text((c["Bc"][0] + c["C"][0]) / 2 + 26, (c["Bc"][1] + c["C"][1]) / 2 + 6, f"b = {b}", size=14))
    # the spider on x = 0 and the fly on x = a, with their offsets from ceiling and floor
    sx, sy = P(*s)
    fx, fy = P(*f)
    tx, ty = P(0, s[1], h)
    out.append(f'<line class="ink-line" x1="{sx:.1f}" y1="{sy:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke-width="1.2" stroke-dasharray="3 3"/>')
    out.append(text(sx + 7, (sy + ty) / 2 + 4, f"{h - s[2]}", anchor="start", size=13))
    bx, by = P(a, f[1], 0)
    out.append(f'<line class="ink-line" x1="{fx:.1f}" y1="{fy:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke-width="1.2" stroke-dasharray="3 3"/>')
    out.append(text(fx + 9, (fy + by) / 2 + 4, f"{f[2]}", anchor="start", size=13))
    out.append(dot(sx, sy, "s1", 6, f"העכביש S = ({s[0]}, {s[1]}, {s[2]})"))
    out.append(text(sx + 11, sy + 17, "S", size=18, anchor="start"))
    out.append(dot(fx, fy, "s2", 6, f"הזבוב F = ({f[0]}, {f[1]}, {f[2]})"))
    out.append(text(fx - 11, fy - 9, "F", size=18, anchor="end"))
    # axes at the corner A
    ax, ay = c["A"]
    for (x, y, z), lab in (((7, 0, 0), "x"), ((0, 7, 0), "y"), ((0, 0, 7), "z")):
        tx, ty = P(x, y, z)
        out.append(f'<line class="axis-c" x1="{ax:.1f}" y1="{ay:.1f}" x2="{tx:.1f}" y2="{ty:.1f}"/>')
        out.append(text(tx + (6 if lab != "z" else 0), ty + (5 if lab != "z" else -4), lab, size=14,
                        extra=' font-style="italic"'))
    return "".join(out) + "</svg>"


def box_legend():
    return ('<span class="viz-legend"><span><i class="s1"></i>העכביש S</span><span><i class="s2"></i>הזבוב F</span>'
            '<span><i class="box-end"></i>קירות הקצה, x = 0 ו-x = a</span><span><i class="box-face"></i>הפאות הצדדיות</span></span>')


def naive_net(a=A, b=B, h=H, s=S, f=F):
    """end0 folded on its top edge, the top, enda folded on its top edge: a 42 straight line."""
    lo, hi = bands(b, h)["top"]
    n = Net(-h, a + h, lo - 2, hi + 2, 9, label=f"פריסה של הקיר של העכביש, התקרה והקיר של הזבוב בשורה אחת : "
            f"קו ישר באורך {a + (h - s[2]) + (h - f[2])}", max_rem=36)
    n.rect(-h, 0, lo, hi, "box-end", "end0", title=HEB["end0"])
    n.rect(0, a, lo, hi, "box-face", "top", title=HEB["top"])
    n.rect(a, a + h, lo, hi, "box-end", "enda", title=HEB["enda"])
    ps = b + h + (b - s[1])
    pf = b + h + (b - f[1])
    xs, xf = -(h - s[2]), a + (h - f[2])
    n.line(xs, ps, xf, pf, "box-path", 3)
    n.point(xs, ps, "s1", "S", dy=-11)
    n.point(xf, pf, "s2", "F", dy=-11)
    d = math.hypot(xf - xs, pf - ps)
    n.label((xs + xf) / 2, ps, f"{num(h - s[2])} + {a} + {num(h - f[2])} = {num(d)}", dy=-10, size=17)
    n.label(0, lo, "x = 0", dy=17, size=14)
    n.label(a, lo, f"x = {a}", dy=17, size=14)
    return n.svg()


def best_net(a=A, b=B, h=H, s=S, f=F):
    """The best route: end0 on its top edge, top, sideB, bottom, enda on its bottom edge."""
    c = best(a, b, h, s, f)
    rng = bands(b, h)
    n = Net(-h, a + h, 0, 2 * b + h, 9, label=f"פריסה של חמש פאות במדרגות : הקיר של העכביש על התקרה, התקרה, הקיר הרחוק, "
            f"הרצפה והקיר של הזבוב על הרצפה. הקו הישר הוא היתר של משולש ישר-זווית עם ניצבים {num(c['dx'])} ו-{num(-c['dp'])}, "
            f"ואורכו {num(c['length'])}", max_rem=36)
    n.rect(-h, 0, *rng["top"], "box-end", "end0", title=HEB["end0"])
    for name in ("top", "sideB", "bottom"):
        n.rect(0, a, *rng[name], "box-face", name, title=HEB[name])
    n.rect(a, a + h, *rng["bottom"], "box-end", "enda", title=HEB["enda"])
    es = [i for i in images(s[1], s[2], b, h) if i[0] == c["s_edge"]][0]
    ef = [i for i in images(f[1], f[2], b, h) if i[0] == c["f_edge"]][0]
    xs, ps, xf, pf = -es[1], es[2], a + ef[1], ef[2] + c["k"] * period(b, h)
    # the right triangle
    n.line(xs, ps, xf, ps, "ink-line", 1.2, "5 4").line(xf, ps, xf, pf, "ink-line", 1.2, "5 4")
    n.label((xs + xf) / 2, ps, f"Δx = {num(c['dx'])}", dy=-8, size=16)
    n.label(xf, (ps + pf) / 2, f"Δp = {num(abs(c['dp']))}", dx=10, dy=5, size=16, anchor="start")
    n.line(xs, ps, xf, pf, "box-path", 3)
    # the crossings of the hinge lines
    for p in (rng["top"][0], rng["sideB"][0]):
        t = (p - ps) / (pf - ps)
        x = xs + t * (xf - xs)
        n.point(x, p, "ink", r=3.5, title=f"חוצה את הקפל בנקודה x = {num(x)}")
    n.point(0, c["p_exit"], "s3", r=4, title=f"יוצא מהקיר של העכביש ב-y = {num(edge_point(c['s_edge'], c['p_exit'], b, h)[0])}")
    n.point(a, c["p_enter"], "s3", r=4, title=f"נכנס לקיר של הזבוב ב-y = {num(edge_point(c['f_edge'], c['p_enter'], b, h)[0])}")
    n.point(xs, ps, "s1", "S", dy=-12)
    n.point(xf, pf, "s2", "F", dx=14, dy=6)
    mid = ((xs + xf) / 2, (ps + pf) / 2)
    n.label(mid[0], mid[1], f"d = {num(c['length'])}", dx=-36, dy=28, size=18)
    n.label(0, 0, "x = 0", dy=17, size=14)
    n.label(a, 0, f"x = {a}", dy=17, size=14)
    return n.svg()


def net_legend():
    return ('<span class="viz-legend"><span><i class="box-path"></i>המסלול, קו ישר בפריסה</span><span><i class="s1"></i>העכביש S</span>'
            '<span><i class="s2"></i>הזבוב F</span><span><i class="s3"></i>יציאה מקיר הקצה וכניסה אליו</span>'
            '<span><i class="ink"></i>חציית קפל</span></span>')


def candidates_table(a=A, b=B, h=H, s=S, f=F):
    rows = ["| הפאות שהמסלול עובר | ‏\\( \\Delta x \\) | ‏\\( \\Delta p \\) | האורך |", "|---|---|---|---|"]
    for c in candidates(a, b, h, s, f):
        if not c["valid"] or len(set(c["faces"])) < len(c["faces"]):
            continue                                   # winds around the box more than once
        seq = " → ".join(c["faces"])
        rows.append(f"| ‏{seq} | ‏{num(c['dx'])} | ‏{num(abs(c['dp']))} | ‏{num(c['length'])} |")
    return "\n".join(rows)


def strip_svg(a=A, b=B, h=H, s=S, f=F):
    """The periodic strip: the four images of S on the left, of F on the right (with one
    copy a period up and down), and the shortest valid line."""
    P = period(b, h)
    rng = bands(b, h)
    p_lo, p_hi = -b, P + b
    n = Net(-h - 2, a + h + 2, p_lo, p_hi, 7.2, pad=(30, 14, 30, 22),
            label="הרצועה המחזורית של ארבע הפאות הצדדיות, עם ארבע הדמויות של העכביש משמאל וארבע הדמויות של הזבוב "
                  "מימין, חלקן גם מחזור אחד למעלה ולמטה. הקו הישר הקצר ביותר שיוצא דרך צלע נכונה הוא המסלול", max_rem=40)
    for k in (-1, 0, 1):
        for name, (lo, hi) in rng.items():
            lo, hi = lo + k * P, hi + k * P
            if hi <= p_lo or lo >= p_hi:
                continue
            n.rect(0, a, max(lo, p_lo), min(hi, p_hi), "box-face" if k == 0 else "box-copy", name if k == 0 else None,
                   title=HEB[name] + ("" if k == 0 else " (עותק מחזורי)"), label_size=14)
    n.line(0, p_lo, 0, p_hi, "axis-c", 1.5).line(a, p_lo, a, p_hi, "axis-c", 1.5)
    n.line(-h - 2, 0, a + h + 2, 0, "ink-line", 1, "4 3").line(-h - 2, P, a + h + 2, P, "ink-line", 1, "4 3")
    n.label(a + 4, 0, "p = 0", dy=-4, size=11, anchor="start").label(a + 4, P, f"p = {P}", dy=-4, size=11, anchor="start")
    c = best(a, b, h, s, f)
    # images of S and of F
    for es, ds, ps, lo, hi in images(s[1], s[2], b, h):
        chosen = es == c["s_edge"]
        n.point(-ds, ps, "s1" if chosen else "ink", r=5 if chosen else 3.5,
                title=f"S דרך {HEB[es]} : x = −{num(ds)}, p = {num(ps)}")
        n.label(-ds, ps, es, dx=-8, dy=4, size=12, anchor="end")
    for ef, df, pf, lo, hi in images(f[1], f[2], b, h):
        for k in (-1, 0, 1):
            p = pf + k * P
            if not p_lo <= p <= p_hi:
                continue
            chosen = ef == c["f_edge"] and k == c["k"]
            n.point(a + df, p, "s2" if chosen else "ink", r=5 if chosen else 3.5,
                    title=f"F דרך {HEB[ef]}, k = {k} : x = {num(a + df)}, p = {num(p)}")
            n.label(a + df, p, ef if k == 0 else f"{ef}, k = {k:+d}", dx=8, dy=4, size=12, anchor="start")
    # the chosen hinge edges and the line
    es = [i for i in images(s[1], s[2], b, h) if i[0] == c["s_edge"]][0]
    ef = [i for i in images(f[1], f[2], b, h) if i[0] == c["f_edge"]][0]
    n.line(0, es[3], 0, es[4], "s3-line", 5).line(a, ef[3] + c["k"] * P, a, ef[4] + c["k"] * P, "s3-line", 5)
    xs, ps, xf, pf = -es[1], es[2], a + ef[1], ef[2] + c["k"] * P
    n.line(xs, ps, xf, pf, "box-path", 3)
    n.point(0, c["p_exit"], "s3", r=4, title=f"נקודת היציאה : p = {num(c['p_exit'])}")
    n.point(a, c["p_enter"], "s3", r=4, title=f"נקודת הכניסה : p = {num(c['p_enter'])}")
    n.label((xs + xf) / 2, (ps + pf) / 2, f"d = {num(c['length'])}", dx=-30, dy=24, size=17)
    n.label(0, p_lo, "x = 0", dy=16, size=13).label(a, p_lo, f"x = {a}", dy=16, size=13)
    n.label(-h - 2, (p_lo + p_hi) / 2, "p", dx=-14, size=15)
    return n.svg()


def strip_legend():
    return ('<span class="viz-legend"><span><i class="s1"></i>הדמות הנבחרת של S</span><span><i class="s2"></i>הדמות הנבחרת של F</span>'
            '<span><i class="ink"></i>שאר הדמויות</span><span><i class="s3"></i>צלעות היציאה והכניסה, והנקודות עליהן</span>'
            '<span><i class="box-path"></i>המסלול הקצר ביותר</span><span><i class="box-copy"></i>עותק מחזורי של הרצועה</span></span>')


def images_table(a=A, b=B, h=H, s=S, f=F):
    rows = ["| הנקודה | הצלע | המרחק לצלע | ‏\\( x \\) של הדמות | ‏\\( p \\) של הדמות | טווח ה-\\( p \\) של הצלע |", "|---|---|---|---|---|---|"]
    for who, (x, y, z), sign in (("S", s, -1), ("F", f, 1)):
        for edge, d, p, lo, hi in images(y, z, b, h):
            xi = f'<span dir="ltr">−{num(d)}</span>' if sign < 0 else num(a + d)   # a leading minus after an RLM reads "11−"
            rows.append(f"| ‏{who} | ‏{edge} | ‏{num(d)} | ‏{xi} | ‏{num(p)} | ‏{num(lo)} עד {num(hi)} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [
        box_svg(),
        box_legend(),
        naive_net(),
        best_net(),
        net_legend(),
        candidates_table(),
        strip_svg(),
        strip_legend(),
        images_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
