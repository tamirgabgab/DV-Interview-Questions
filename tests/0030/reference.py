"""Independent reference for question 0030: the shortest surface path between two points
on a box, found the long way. Every face sequence from the spider's face to the fly's face
is unfolded into the plane with 2D frames (the way the owner's tool does it), the straight
line between the two images is checked against every hinge it must cross and against the
faces it runs through, and the shortest valid line wins. Nothing here is shared with the
page code (the periodic strip) or with the figure generator."""

from __future__ import annotations

import math

EPS = 1e-9


def faces(a, b, h):
    """Each face: origin, the two unit directions along it, and its two sizes."""
    return {"end0": ((0, 0, 0), (0, 1, 0), (0, 0, 1), b, h), "enda": ((a, 0, 0), (0, 1, 0), (0, 0, 1), b, h),
            "top": ((0, 0, h), (1, 0, 0), (0, 1, 0), a, b), "bottom": ((0, 0, 0), (1, 0, 0), (0, 1, 0), a, b),
            "side0": ((0, 0, 0), (1, 0, 0), (0, 0, 1), a, h), "sideB": ((0, b, 0), (1, 0, 0), (0, 0, 1), a, h)}


def _add(p, q):
    return tuple(x + y for x, y in zip(p, q))


def _sub(p, q):
    return tuple(x - y for x, y in zip(p, q))


def _mul(p, t):
    return tuple(x * t for x in p)


def _dot(p, q):
    return sum(x * y for x, y in zip(p, q))


def _norm(p):
    return math.sqrt(_dot(p, p))


def _cross2(d, e):
    return d[0] * e[1] - d[1] * e[0]


def corners(face):
    o, u, v, w, hh = face
    return [o, _add(o, _mul(u, w)), _add(_add(o, _mul(u, w)), _mul(v, hh)), _add(o, _mul(v, hh))]


def centre(face):
    o, u, v, w, hh = face
    return _add(o, _add(_mul(u, w / 2), _mul(v, hh / 2)))


class Part:
    """A face placed in the plane: its 2D origin and the 2D images of its two directions."""

    def __init__(self, name, model, o2=(0.0, 0.0), u2=(1.0, 0.0), v2=(0.0, 1.0)):
        self.name, self.model, self.o2, self.u2, self.v2 = name, model, o2, u2, v2

    def to2(self, q):
        o, u, v, _, _ = self.model
        d = _sub(q, o)
        return _add(self.o2, _add(_mul(self.u2, _dot(d, u)), _mul(self.v2, _dot(d, v))))

    def to3(self, q2):
        o, u, v, _, _ = self.model
        d = _sub(q2, self.o2)
        return _add(o, _add(_mul(u, _dot(d, self.u2)), _mul(v, _dot(d, self.v2))))

    def inside(self, q2):
        cs = [self.to2(c) for c in corners(self.model)]
        xs, ys = [c[0] for c in cs], [c[1] for c in cs]
        return min(xs) - EPS <= q2[0] <= max(xs) + EPS and min(ys) - EPS <= q2[1] <= max(ys) + EPS


def shared_edge(fa, fb):
    return [q for q in corners(fa) if any(_norm(_sub(q, r)) < EPS for r in corners(fb))]


def unfold(part, name, model):
    """Place `model` next to `part` in the plane, hinged on their shared edge, on the far
    side from `part`. Returns the new part and the hinge as a 2D segment."""
    edge = shared_edge(part.model, model)
    if len(edge) != 2:
        return None
    A, B = edge
    A2, B2 = part.to2(A), part.to2(B)
    L = _norm(_sub(B, A))
    t3, t2 = _mul(_sub(B, A), 1 / L), _mul(_sub(B2, A2), 1 / L)
    c = _sub(centre(model), A)
    n3 = _sub(c, _mul(t3, _dot(c, t3)))
    n3 = _mul(n3, 1 / _norm(n3))
    n2 = (-t2[1], t2[0])
    if _dot(_sub(part.to2(centre(part.model)), A2), n2) > 0:
        n2 = _mul(n2, -1)

    def place(q):
        d = _sub(q, A)
        return _add(A2, _add(_mul(t2, _dot(d, t3)), _mul(n2, _dot(d, n3))))

    o, u, v, _, _ = model
    o2 = place(o)
    return Part(name, model, o2, _sub(place(_add(o, u)), o2), _sub(place(_add(o, v)), o2)), (A2, B2)


def routes(a, b, h, S, F, start="end0", end="enda"):
    """Every valid straight line, as (length, face names, 3D points along the path)."""
    FS = faces(a, b, h)
    out = []

    def walk(parts, hinges):
        last = parts[-1]
        if last.name == end:
            s, f = parts[0].to2(S), last.to2(F)
            d = _sub(f, s)
            prev, pts = 0.0, [s]
            for A, B in hinges:
                e, q = _sub(B, A), _sub(A, s)
                det = _cross2(d, e)
                if abs(det) < 1e-12:
                    return
                t, u = _cross2(q, e) / det, _cross2(q, d) / det
                if not (prev - EPS <= t <= 1 + EPS and -EPS <= u <= 1 + EPS):
                    return
                prev = t
                pts.append(_add(s, _mul(d, t)))
            pts.append(f)
            for i, part in enumerate(parts):
                if not part.inside(pts[i]) or not part.inside(pts[i + 1]):
                    return
            pts3 = [S] + [parts[i].to3(pts[i + 1]) for i in range(len(hinges))] + [F]
            out.append((_norm(d), [p.name for p in parts], pts3))
            return
        for name, model in FS.items():
            if any(p.name == name for p in parts):
                continue
            r = unfold(last, name, model)
            if r:
                walk(parts + [r[0]], hinges + [r[1]])

    walk([Part(start, FS[start])], [])
    out.sort(key=lambda r: (r[0], len(r[1]), r[1]))
    return out


def shortest(a, b, h, y0, z0, y1, z1):
    """The shortest distance, the best face sequences (ties) and the exit points from end0."""
    rs = routes(a, b, h, (0, y0, z0), (a, y1, z1))
    best = rs[0][0]
    ties = [r for r in rs if abs(r[0] - best) < 1e-7]
    return best, [r[1] for r in ties], [r[2][1] for r in ties]
