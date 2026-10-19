#!/usr/bin/env python3
"""Shared building blocks of the inline SVG charts (bars, stems against a threshold, a
ratio against y = 1, a curve against a line, position-time paths).

    from charts import Chart
    c = Chart("aria label", y_max=1, slots=12)       # x in slots 1..12, or x_max for a value axis
    c.grid_y([0, 0.5, 1]); c.hline(0.27, "T ≈ 0.27"); c.stem(4, 0.31, "s2", title="p(4)")
    c.x_ticks(range(1, 13)); svg = c.svg()

Coordinates: the plot area is [x0, w - right] x [top, base] in the viewBox; values map to it
with ``X`` and ``Y`` (``log=True`` for a log-scale y axis). Colours come only from the site's
CSS classes (``grid``, ``axis``, ``tick``, ``legend``, ``s1``/``s2``/``s3``/``ink`` lines and
dots, ``by-*`` bars), so every chart follows the light / dark switch. Used by cake.py
(0027, 0028) and q0026.py.
"""

from __future__ import annotations

import math


class Chart:
    def __init__(self, label, *, w=640, h=250, x0=46, right=12, top=16, base=216,
                 slots=None, x_max=None, x_min=0.0, y_max=1.0, y_min=0.0, log=False, style=None):
        self.w, self.h, self.x0, self.right, self.top, self.base = w, h, x0, right, top, base
        self.slots, self.x_min, self.x_max = slots, x_min, x_max
        self.y_min, self.y_max, self.log = y_min, y_max, log
        style = f' style="{style}"' if style else ""
        self.parts = [f'<svg class="perf-chart" viewBox="0 0 {w} {h}"{style} role="img" aria-label="{label}">']

    # --- mapping ---------------------------------------------------------------------------

    @property
    def x1(self):
        return self.w - self.right

    def X(self, x):
        """A slot number (1..slots, centred) or a value on [x_min, x_max]."""
        if self.slots:
            return self.x0 + (float(x) - 0.5) * (self.x1 - self.x0) / self.slots
        return self.x0 + (float(x) - self.x_min) / (self.x_max - self.x_min) * (self.x1 - self.x0)

    def Y(self, v):
        if self.log:
            lo, hi = math.log10(self.y_min), math.log10(self.y_max)
            return self.base - (math.log10(float(v)) - lo) / (hi - lo) * (self.base - self.top)
        return self.base - (float(v) - self.y_min) / (self.y_max - self.y_min) * (self.base - self.top)

    @property
    def slot(self):
        return (self.x1 - self.x0) / self.slots

    # --- scaffolding -------------------------------------------------------------------------

    def add(self, s):
        self.parts.append(s)
        return self

    def grid_y(self, ticks, fmt="{:g}", labels=None):
        for i, v in enumerate(ticks):
            y = self.Y(v)
            lab = labels[i] if labels else fmt.format(v)
            self.add(f'<line class="grid" x1="{self.x0}" x2="{self.x1}" y1="{y:.1f}" y2="{y:.1f}"/>'
                     f'<text class="tick" x="{self.x0 - 8}" y="{y + 4:.1f}" text-anchor="end">{lab}</text>')
        return self

    def grid_x(self, xs, labels=None, dashed=True):
        """Vertical grid lines with tick labels below the axis."""
        for i, x in enumerate(xs):
            X = self.X(x)
            dash = ' stroke-dasharray="4 4"' if dashed else ""
            lab = labels[i] if labels else f"{x:g}"
            self.add(f'<line class="grid" x1="{X:.1f}" x2="{X:.1f}" y1="{self.top - 6}" y2="{self.base}"{dash}/>'
                     f'<text class="tick" x="{X:.1f}" y="{self.base + 18}" text-anchor="middle">{lab}</text>')
        return self

    def x_ticks(self, xs, labels=None):
        for i, x in enumerate(xs):
            lab = labels[i] if labels else x
            self.add(f'<text class="tick" x="{self.X(x):.1f}" y="{self.base + 18}" text-anchor="middle">{lab}</text>')
        return self

    def hline(self, v, label=None, cls="ink-line", width=1.5, dash="6 4", label_at="start"):
        y = self.Y(v)
        self.add(f'<line class="{cls}" x1="{self.x0}" x2="{self.x1}" y1="{y:.1f}" y2="{y:.1f}" '
                 f'stroke-width="{width}" stroke-dasharray="{dash}"/>')
        if label:
            if label_at == "start":
                self.add(f'<text class="legend" x="{self.x0 + 6}" y="{y - 6:.1f}">{label}</text>')
            else:
                self.add(f'<text class="legend" x="{self.x1 - 4}" y="{y - 6:.1f}" text-anchor="end">{label}</text>')
        return self

    def vline(self, x, y_to, label=None, dash="3 3"):
        """A thin dashed drop from (x, y_to) to the axis, labelled next to its foot."""
        X = self.X(x)
        self.add(f'<line class="ink-line" x1="{X:.1f}" x2="{X:.1f}" y1="{self.Y(y_to):.1f}" y2="{self.base}" '
                 f'stroke-width="1" stroke-dasharray="{dash}"/>')
        if label:
            self.add(f'<text class="legend" x="{X + 6:.1f}" y="{self.base - 6}">{label}</text>')
        return self

    def axis(self, x_label=None, at="start"):
        self.add(f'<line class="axis" x1="{self.x0}" x2="{self.x1}" y1="{self.base}" y2="{self.base}"/>')
        if x_label:
            if at == "start":
                self.add(f'<text class="tick" x="{self.x0 - 8}" y="{self.base + 18}" text-anchor="end">{x_label}</text>')
            else:
                self.add(f'<text class="tick" x="{self.x1}" y="{self.base + 18}" text-anchor="end">{x_label}</text>')
        return self

    def svg(self):
        return "".join(self.parts) + "</svg>"

    # --- marks -------------------------------------------------------------------------------

    def bar(self, x, v, cls, title=None, value_label=None, frac=0.68):
        bw = self.slot * frac
        X, Y = self.X(x), self.Y(v)
        t = f"<title>{title}</title>" if title else ""
        self.add(f'<rect class="bar {cls}" x="{X - bw / 2:.1f}" y="{Y:.1f}" width="{bw:.1f}" '
                 f'height="{self.base - Y:.1f}" rx="2">{t}</rect>')
        if value_label is not None:
            self.add(f'<text class="tick" x="{X:.1f}" y="{Y - 5:.1f}" text-anchor="middle">{value_label}</text>')
        return self

    def dot(self, x, v, cls, r=4.5, title=None, label=None, dx=0, dy=-9, label_size=None):
        X, Y = self.X(x), self.Y(v)
        t = f"<title>{title}</title>" if title else ""
        self.add(f'<circle class="{cls}-dot" cx="{X:.1f}" cy="{Y:.1f}" r="{r}">{t}</circle>')
        if label is not None:
            size = f' style="font-size:{label_size}px"' if label_size else ""
            self.add(f'<text class="legend" x="{X + dx:.1f}" y="{Y + dy:.1f}" text-anchor="middle"{size}>{label}</text>')
        return self

    def stem(self, x, v, cls, r=4.5, title=None, width=2):
        X = self.X(x)
        self.add(f'<line class="{cls}-line" x1="{X:.1f}" x2="{X:.1f}" y1="{self.base}" y2="{self.Y(v):.1f}" stroke-width="{width}"/>')
        return self.dot(x, v, cls, r=r, title=title)

    def path(self, points, cls, width=2, extra=""):
        pts = " ".join(f"{self.X(x):.1f},{self.Y(v):.1f}" for x, v in points)
        self.add(f'<polyline class="{cls}" points="{pts}" fill="none" stroke-width="{width}"{extra}/>')
        return self

    def segment(self, a, b, cls, width=2.5):
        (xa, va), (xb, vb) = a, b
        self.add(f'<line class="{cls}" x1="{self.X(xa):.1f}" y1="{self.Y(va):.1f}" '
                 f'x2="{self.X(xb):.1f}" y2="{self.Y(vb):.1f}" stroke-width="{width}"/>')
        return self

    def text(self, x, v, s, cls="legend", anchor="middle", dx=0, dy=0, rtl=False):
        d = ' direction="rtl"' if rtl else ""
        self.add(f'<text class="{cls}" x="{self.X(x) + dx:.1f}" y="{self.Y(v) + dy:.1f}" '
                 f'text-anchor="{anchor}"{d}>{s}</text>')
        return self
