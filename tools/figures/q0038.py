#!/usr/bin/env python3
"""Figure of question 0038 (SVA for a req / ack handshake): the interface contract of the
statement as a machine over the sampled values. A state is one clock cycle's (req, ack);
a solid arrow is an allowed next sample, a dashed one ends in a cross with the number of
the rule that sample breaks; and its legend.

    python tools/figures/fill.py 38        # put the blocks on the page

STATES, MOVES and BAD are what the drawing shows; tests/0038 walks them against the page's
reference model check_handshake: every allowed walk passes, every forbidden sample fails
the rule it is marked with, in that cycle.
"""

from html import escape

STATES = {                                   # name: (req, ack) in that cycle
    "IDLE": (0, 0),
    "RISE": (1, 0),                          # the cycle req rises
    "WAIT 1": (1, 0),
    "WAIT 2": (1, 0),
    "ACK": (1, 1),
}
MOVES = [("IDLE", "IDLE"), ("IDLE", "RISE"), ("RISE", "WAIT 1"), ("WAIT 1", "WAIT 2"),
         ("RISE", "ACK"), ("WAIT 1", "ACK"), ("WAIT 2", "ACK"), ("ACK", "IDLE")]
# (from, the next sample (req, ack), the rule it breaks, the key in check_handshake)
BAD = [("RISE", (0, 0), 1, "hold"), ("WAIT 1", (0, 0), 1, "hold"), ("WAIT 2", (0, 0), 1, "hold"),
       ("WAIT 2", (1, 0), 2, "late"), ("IDLE", (1, 1), 2, "late"), ("IDLE", (0, 1), 3, "orphan"), ("ACK", (0, 1), 3, "orphan"),
       ("ACK", (1, 0), 4, "drop")]

NW, NH, TOP = 78, 62, 44
X = {"IDLE": 14, "RISE": 126, "WAIT 1": 238, "WAIT 2": 350, "ACK": 238}
Y = {"IDLE": TOP, "RISE": TOP, "WAIT 1": TOP, "WAIT 2": TOP, "ACK": 160}
W, H = 494, 272
MARK = "fc38-arrow"


def _move(d):
    return f'<path class="fc-move" d="{d}" marker-end="url(#{MARK})"/>'


def _bad(x1, y1, x2, y2, rule, bx, by):
    """A dashed stub from (x1, y1) to (x2, y2), a cross at its end and the rule's badge at (bx, by)."""
    dx = 5
    return (f'<line class="fc-bad" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'
            f'<line class="fc-x" x1="{x2 - dx}" y1="{y2 - dx}" x2="{x2 + dx}" y2="{y2 + dx}"/>'
            f'<line class="fc-x" x1="{x2 - dx}" y1="{y2 + dx}" x2="{x2 + dx}" y2="{y2 - dx}"/>'
            f'<circle class="fc-badge" cx="{bx}" cy="{by}" r="10"/>'
            f'<text class="fc-t fc-b" x="{bx}" y="{by + 5}" text-anchor="middle">{rule}</text>')


def figure():
    s = [f'<svg class="figure" viewBox="0 0 {W} {H}" style="max-width:{W / 16:.1f}rem" role="img" '
         f'aria-label="{escape(aria())}">',
         f'<defs><marker id="{MARK}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
         'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="fc-head"/></marker></defs>']
    for name, (req, ack) in STATES.items():
        x, y = X[name], Y[name]
        cls = "fc-node fc-ack" if ack else "fc-node"
        s.append(f'<rect class="{cls}" x="{x}" y="{y}" width="{NW}" height="{NH}" rx="8"/>'
                 f'<text class="fc-t fc-b" x="{x + NW / 2:g}" y="{y + 20}" text-anchor="middle">{name}</text>'
                 f'<text class="fc-sub" x="{x + NW / 2:g}" y="{y + 38}" text-anchor="middle">req {req}</text>'
                 f'<text class="fc-sub" x="{x + NW / 2:g}" y="{y + 54}" text-anchor="middle">ack {ack}</text>')
    cy = TOP + NH / 2
    cx = {n: X[n] + NW / 2 for n in STATES}
    # allowed moves
    s.append(_move(f"M{X['IDLE'] + 22},{TOP} C{X['IDLE'] + 18},{TOP - 34} {X['IDLE'] + 60},{TOP - 34} {X['IDLE'] + 56},{TOP - 1}"))
    for a, b in (("IDLE", "RISE"), ("RISE", "WAIT 1"), ("WAIT 1", "WAIT 2")):
        s.append(_move(f"M{X[a] + NW},{cy:g} L{X[b] - 1},{cy:g}"))
    ay = Y["ACK"]
    s.append(_move(f"M{cx['RISE']:g},{TOP + NH} L{X['ACK'] + 12},{ay - 1}"))
    s.append(_move(f"M{cx['WAIT 1']:g},{TOP + NH} L{cx['WAIT 1']:g},{ay - 1}"))
    s.append(_move(f"M{cx['WAIT 2']:g},{TOP + NH} L{X['ACK'] + NW - 12},{ay - 1}"))
    mid = ay + NH / 2
    s.append(_move(f"M{X['ACK']},{mid:g} L{cx['IDLE']:g},{mid:g} L{cx['IDLE']:g},{TOP + NH + 1}"))
    # forbidden samples
    for n in ("RISE", "WAIT 1", "WAIT 2"):
        s.append(_bad(cx[n], TOP, cx[n], 20, 1, cx[n] + 20, 18))
    s.append(_bad(X["WAIT 2"] + NW, cy, X["WAIT 2"] + NW + 26, cy, 2, X["WAIT 2"] + NW + 46, cy))
    ix = X["IDLE"] + 14
    s.append(_bad(ix, TOP + NH, ix, TOP + NH + 30, 3, ix, TOP + NH + 54))
    jx = X["IDLE"] + NW - 14                 # req and ack together in the rise cycle: ack too early
    s.append(_bad(jx, TOP + NH, jx, TOP + NH + 30, 2, jx, TOP + NH + 54))
    s.append(_bad(X["ACK"] + NW, mid, X["ACK"] + NW + 26, mid, 4, X["ACK"] + NW + 46, mid))
    s.append(_bad(cx["ACK"], ay + NH, cx["ACK"], ay + NH + 24, 3, cx["ACK"] + 22, ay + NH + 24))
    return "".join(s) + "</svg>"


def aria():
    moves = ", ".join(f"{a} ל-{b}" for a, b in MOVES)
    return ("החוזה כמכונת מצבים של הדגימות. מעברים מותרים : " + moves +
            ". מכל מצב המתנה, req שיורד מפר את חוק 1; WAIT 2 בלי ack, או req ו-ack שעולים יחד מ-IDLE, מפרים את חוק 2; "
            "ack בלי req מפר את חוק 3; req גבוה אחרי ACK מפר את חוק 4")


def legend():
    return ('<span class="viz-legend"><span><i class="fc-key-move"></i>הדגימה הבאה מותרת</span>'
            '<span><i class="fc-key-bad"></i>דגימה אסורה, עם מספר החוק שהיא מפרה</span>'
            '<span><i class="fc-key-ack"></i>מחזור של <code>ack</code></span></span>\n\n'
            '<span class="viz-legend">'
            '<span>חוק 1 : <code>req</code> יורד לפני <code>ack</code></span>'
            '<span>חוק 2 : <code>ack</code> כבר במחזור העלייה, או אין <code>ack</code> עד שלושה מחזורים אחריה</span>'
            '<span>חוק 3 : <code>ack</code> כש-<code>req</code> נמוך</span>'
            '<span>חוק 4 : <code>req</code> עדיין גבוה במחזור שאחרי <code>ack</code></span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [figure() + "\n\n" + legend()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
