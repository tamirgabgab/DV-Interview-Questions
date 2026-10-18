"""Drawing helpers for the two-hourglass questions (0018, 0019).

    from hourglass import event_frame, branches

``event_frame`` draws one event of a plan: the time, the two hourglasses on arrival, the
action and the two hourglasses after it. ``branches`` draws one state and its four options.
The page scripts (``q0018.py``, ``q0019.py``) put the frames in a step-through figure.
Colours come from the ``sand-a`` / ``sand-b`` / ``glass`` / ``frame`` / ``measure`` classes
in ``docs/stylesheets/extra.css``. Text inside the SVG stays English; the Hebrew goes in
the captions and tables next to the figure.
"""

# Hourglass glyph geometry (px, in the SVG viewBox).
W, H, NECK = 30, 50, 3
_uid = 0


def hourglass(x: float, y: float, top: int, total: int, kind: str) -> str:
    """One hourglass at (x, y) with `top` of `total` minutes of sand still on top."""
    global _uid
    _uid += 1
    cx, mid = x + W / 2, y + H / 2
    bulb_top = f"{x},{y} {x + W},{y} {cx + NECK},{mid} {cx - NECK},{mid}"
    bulb_bot = f"{cx - NECK},{mid} {cx + NECK},{mid} {x + W},{y + H} {x},{y + H}"
    top_h = H / 2 * top / total
    bot_h = H / 2 * (total - top) / total
    out = [f'<clipPath id="hg{_uid}t"><polygon points="{bulb_top}"/></clipPath>',
           f'<clipPath id="hg{_uid}b"><polygon points="{bulb_bot}"/></clipPath>']
    if top:
        out.append(f'<rect class="sand-{kind}" clip-path="url(#hg{_uid}t)" x="{x}" y="{mid - top_h:.1f}" '
                   f'width="{W}" height="{top_h:.1f}"/>')
        # a thin stream through the neck shows that this hourglass is running
        out.append(f'<line class="stream-{kind}" x1="{cx}" y1="{mid}" x2="{cx}" y2="{y + H - bot_h - 1:.1f}"/>')
    if total - top:
        out.append(f'<rect class="sand-{kind}" clip-path="url(#hg{_uid}b)" x="{x}" y="{y + H - bot_h:.1f}" '
                   f'width="{W}" height="{bot_h:.1f}"/>')
    out.append(f'<polygon class="glass" points="{bulb_top}"/><polygon class="glass" points="{bulb_bot}"/>')
    out.append(f'<line class="frame" x1="{x - 4}" y1="{y}" x2="{x + W + 4}" y2="{y}"/>'
               f'<line class="frame" x1="{x - 4}" y1="{y + H}" x2="{x + W + 4}" y2="{y + H}"/>')
    out.append(f'<text class="tick" x="{x + W + 7}" y="{y + 12}">{top}</text>'
               f'<text class="tick" x="{x + W + 7}" y="{y + H - 2}">{total - top}</text>')
    out.append(f'<text class="legend" x="{cx}" y="{y + H + 15}" text-anchor="middle">{kind.upper()}</text>')
    return "".join(out)


def pair(x: float, y: float, a: int, b: int, A: int, B: int) -> str:
    """Hourglasses A and B side by side."""
    return hourglass(x, y, a, A, "a") + hourglass(x + W + 34, y, b, B, "b")


PAIR_W = 2 * W + 34 + 18


def arrow(x1: float, y: float, x2: float) -> str:
    return (f'<line class="ink-line" x1="{x1}" y1="{y}" x2="{x2 - 6}" y2="{y}" stroke-width="1.5"/>'
            f'<polygon class="ink-fill" points="{x2},{y} {x2 - 8},{y - 4} {x2 - 8},{y + 4}"/>')


FRAME_W, FRAME_H = 460, 92


def event_frame(A: int, B: int, t: int, event: str, before, action: str, after, label: str,
                measuring: bool = False) -> str:
    """One event: time and what happened (left), the hourglasses on arrival, the action,
    the hourglasses after it. `after` is None for the final frame (the action is a verdict)."""
    y, cy = 12, 12 + H / 2
    out = [f'<svg class="figure hourglass-fig" viewBox="0 0 {FRAME_W} {FRAME_H}" '
           f'style="max-width:{FRAME_W / 16:.0f}rem" role="img" aria-label="{label}">']
    if measuring:
        out.append(f'<rect class="measure" x="2" y="2" width="{FRAME_W - 4}" height="{FRAME_H - 4}" rx="6"/>')
    out.append(f'<text class="legend" x="10" y="{cy - 4}" font-weight="700">t = {t}</text>'
               f'<text class="tick" x="10" y="{cy + 14}">{event}</text>')
    out.append(pair(92, y, before[0], before[1], A, B))
    if after is None:
        out.append(f'<text class="legend" x="226" y="{cy + 5}" font-weight="700">{action}</text>')
    else:
        out.append(arrow(222, cy, 312))
        out.append(f'<text class="legend" x="267" y="{cy - 8}" text-anchor="middle">{action}</text>')
        out.append(pair(336, y, after[0], after[1], A, B))
    out.append("</svg>")
    return "".join(out)


def branches(A: int, B: int, t: int, a: int, b: int, children: list, label: str) -> str:
    """The parent state on top and its four options (flip nothing / A / B / both) below.

    children: (option text, wait, (t2, a2, b2), verdict text, verdict class)
    """
    out = [f'<svg class="figure hourglass-fig" viewBox="0 0 640 300" role="img" aria-label="{label}">']
    out.append(f'<text class="legend" x="320" y="16" text-anchor="middle" font-weight="700">t = {t}</text>')
    out.append(pair(270, 26, a, b, A, B))
    cols = [60, 220, 380, 540]
    for (text, wait, (t2, a2, b2), verdict, cls), cx in zip(children, cols):
        out.append(f'<g class="{cls}">')
        out.append(f'<line class="ink-line" x1="320" y1="104" x2="{cx}" y2="150" stroke-width="1.2"/>')
        out.append(f'<text class="legend" x="{cx}" y="170" text-anchor="middle">{text}</text>'
                   f'<text class="tick" x="{cx}" y="186" text-anchor="middle">wait {wait} → t = {t2}</text>')
        out.append(pair(cx - PAIR_W / 2 + 4, 196, a2, b2, A, B))
        out.append(f'<text class="tick" x="{cx}" y="286" text-anchor="middle">{verdict}</text>')
        out.append("</g>")
    out.append("</svg>")
    return "".join(out)
