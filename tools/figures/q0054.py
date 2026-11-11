#!/usr/bin/env python3
"""Figures and tables of question 0054 (arbiters: fixed priority and starvation, round
robin with the double-request trick, the SVA rules with the fairness bound, weighted round
robin).

    python tools/figures/fill.py 54        # put the blocks on the page

The reference here is independent of the page code (which uses the bit trick): the
arbiters written as plain loops over the requesters from the priority pointer, three
buggy round-robin variants, and the rules of part c counted on a trace the way the
assertions count them. blocks() returns, in page order: the grant grids of a fixed and a
round-robin arbiter under full load, their legend, the table of the trick on one example,
the block diagram of rr_arbiter with its legend, the table of a weighted round robin, and
the weighted round robin clock by clock (pri, used and the grant). tests/0054 checks the page code (Python, and the
SystemVerilog modules and checker in Verilator) against these.
"""

from html import escape

N = 4
RLM = "‏"
NB = "\u00a0"


# --- the arbiters (plain loops) -------------------------------------------------------------

def fixed(reqs, n=N):
    """The lowest requester wins, every cycle."""
    return [next((1 << i for i in range(n) if r >> i & 1), 0) for r in reqs]


def rr(reqs, n=N, bug=None):
    """Round robin: the first requester at or after the pointer wins, and the pointer moves
    to the one after it. bug: "stuck" (the pointer never moves), "winner" (it moves onto the
    winner, not past it), "double" (the first requester at or after the pointer and the first
    from 0 both win)."""
    ptr, out = 0, []
    for r in reqs:
        win = next(((ptr + k) % n for k in range(n) if r >> ((ptr + k) % n) & 1), None)
        g = 0 if win is None else 1 << win
        if bug == "double" and win is not None:
            first = next(i for i in range(n) if r >> i & 1)
            g |= 1 << first
        out.append(g)
        if win is not None and bug != "stuck":
            ptr = win if bug == "winner" else (win + 1) % n
    return out


def wrr(reqs, weights):
    """Weighted round robin: the holder of the pointer keeps winning while it requests, up to
    its weight in a row; then the pointer moves past it."""
    n, ptr, used, out = len(weights), 0, 0, []
    for r in reqs:
        win = next(((ptr + k) % n for k in range(n) if r >> ((ptr + k) % n) & 1), None)
        if win is None:
            out.append(0)
            continue
        used = used + 1 if win == ptr else 1
        if used == weights[win]:
            ptr, used = (win + 1) % n, 0
        else:
            ptr = win
        out.append(1 << win)
    return out


def wrr_trace(reqs, weights):
    """The weighted round robin clock by clock: per cycle the request, the registers at the
    start of the cycle (the pointer as a one-hot, used) and the grant."""
    n, ptr, used, out = len(weights), 0, 0, []
    for r in reqs:
        pri, used0 = 1 << ptr, used
        win = next(((ptr + k) % n for k in range(n) if r >> ((ptr + k) % n) & 1), None)
        if win is not None:
            used = used + 1 if win == ptr else 1
            if used == weights[win]:
                ptr, used = (win + 1) % n, 0
            else:
                ptr = win
        out.append((r, pri, used0, 0 if win is None else 1 << win))
    return out


# --- the rules of part c ----------------------------------------------------------------------

def violations(reqs, grants, n, maxw):
    """How many times each assertion fails on the trace, counted as a simulator counts them:
    one-hot (per cycle), no grant without a request (per cycle), the hold rule (per
    requester and cycle: a waiting request stays), fairness (per requester and cycle with
    req: a grant within maxw cycles, attempts that run past the end not counted)."""
    T = len(reqs)
    onehot = sum(1 for g in grants if g & (g - 1))
    spurious = sum(1 for r, g in zip(reqs, grants) if g & ~r)
    hold = sum(1 for t in range(T - 1) for i in range(n) if reqs[t] >> i & 1 and not grants[t] >> i & 1 and not reqs[t + 1] >> i & 1)
    fair = 0
    for i in range(n):
        for t in range(T):
            if reqs[t] >> i & 1 and t + maxw < T and not any(grants[u] >> i & 1 for u in range(t, t + maxw + 1)):
                fair += 1
    return {"onehot": onehot, "spurious": spurious, "hold": hold, "fair": fair}


def max_wait(reqs, grants, i):
    """The longest run of cycles requester i requested without a grant."""
    best = run = 0
    for r, g in zip(reqs, grants):
        if r >> i & 1 and not g >> i & 1:
            run += 1
            best = max(best, run)
        else:
            run = 0
    return best


# --- blocks ------------------------------------------------------------------------------

FULL = [0b1111] * 8


def grids():
    """Fixed priority and round robin, N = 4, everybody requesting for 8 cycles."""
    rows = [("fixed", fixed(FULL)), ("round robin", rr(FULL))]
    W, S, x0, top, gap = 660, 34, 150, 30, 26
    H = top + len(rows) * (N * S + gap) + 10
    s = (f'<svg class="figure arb-fig" viewBox="0 0 {W} {H}" style="max-width:41rem" role="img" '
         'aria-label="ארבעה מבקשים שמבקשים כל הזמן : ב-fixed priority רק מבקש 0 מקבל, ב-round robin כל אחד מקבל פעם בארבעה מחזורים">')
    for c in range(len(FULL)):
        s += f'<text class="tick" x="{x0 + c * S + S / 2}" y="{top - 10}" text-anchor="middle">{c}</text>'
    for k, (name, grants) in enumerate(rows):
        y0 = top + k * (N * S + gap)
        s += f'<text class="arb-name" x="{x0 - 70}" y="{y0 + N * S / 2 + 5}" text-anchor="middle">{name}</text>'
        for i in range(N):
            y = y0 + i * S
            s += f'<text class="tick" x="{x0 - 8}" y="{y + S / 2 + 4}" text-anchor="end">req {i}</text>'
            for c, g in enumerate(grants):
                win = g >> i & 1
                s += f'<rect class="arb-cell {"is-gnt" if win else "is-wait"}" x="{x0 + c * S}" y="{y}" width="{S - 3}" height="{S - 3}" rx="3"/>'
                if win:
                    s += f'<text class="arb-mark" x="{x0 + c * S + S / 2 - 1}" y="{y + S / 2 + 4}" text-anchor="middle">G</text>'
    s += f'<text class="legend" x="{W - 8}" y="{H - 4}" text-anchor="end">cycle →</text>'
    return s + "</svg>"


def grids_legend():
    return ('<span class="viz-legend"><span><i class="arb-key-gnt"></i>מענק (G)</span>'
            '<span><i class="arb-key-wait"></i>מבקש ומחכה</span></span>')


def bits(v, n):
    return format(v & ((1 << n) - 1), f"0{n}b")


def trick_table(req=0b1011, ptr=2):
    """The double-request trick on one example: req, the pointer as a one-hot, and each step."""
    n = N
    pri = 1 << ptr
    dbl = req << n | req
    minus = (dbl - pri) & ((1 << 2 * n) - 1)
    inv = ~minus & ((1 << 2 * n) - 1)
    sel = dbl & inv
    gnt = (sel | sel >> n) & ((1 << n) - 1)
    rows = ["| השלב | הביטים (3 עד 0, או 7 עד 0) | מה זה |", "|---|:-:|---|"]
    rows.append(f"| ‏`req` | {RLM}`{bits(req, n)}` | מבקשים 0, 1 ו-3 |")
    rows.append(f"| ‏`pri` | {RLM}`{bits(pri, n)}` | העדיפות אצל מבקש {ptr} |")
    rows.append(f"| ‏`dbl = {{req, req}}` | {RLM}`{bits(dbl, 2 * n)}` | הבקשות פעמיים, כדי לעבור את הקצה |")
    rows.append(f"| ‏`dbl - pri` | {RLM}`{bits(minus, 2 * n)}` | הלווה רץ מ-`pri` עד הבקשה הראשונה ומאפס אותה |")
    rows.append(f"| ‏`~(dbl - pri)` | {RLM}`{bits(inv, 2 * n)}` | עכשיו רק היא דולקת מבין הבקשות שמעל `pri` |")
    rows.append(f"| ‏`sel = dbl & ~(dbl - pri)` | {RLM}`{bits(sel, 2 * n)}` | הבקשה הראשונה מ-`pri` והלאה, במעגל |")
    rows.append(f"| ‏`gnt` : ‏OR של שני החצאים | {RLM}`{bits(gnt, n)}` | מבקש {gnt.bit_length() - 1} זוכה |")
    return "\n".join(rows)


WEIGHTS = [1, 2, 3, 4]


def wrr_table():
    T = 400
    grants = wrr([0b1111] * T, WEIGHTS)
    rows = ["| המבקש | המשקל | החלק שלו בעומס מלא | ההמתנה הארוכה ביותר | ‏\\( \\sum_{j \\ne i} w_j \\) |", "|:-:|:-:|:-:|:-:|:-:|"]
    total = sum(WEIGHTS)
    for i, w in enumerate(WEIGHTS):
        share = sum(1 for g in grants if g >> i & 1) / T
        rows.append(f"| {RLM}{i} | {RLM}{w} | {RLM}{w}/{total} = {share:.0%} | {RLM}{max_wait([0b1111] * T, grants, i)} | {RLM}{total - w} |")
    return "\n".join(rows)


# the block diagram of rr_arbiter, left to right: the doubled requests, the subtraction of the
# pointer, the AND with the inverse, the fold of the halves; under them the pointer register
# loaded from the rotated grant when there is a grant
HW_W, HW_H = 580, 218
HW_BLOCKS = (   # x, y, w, h, stage (1 the pick, 2 the fold, 3 the pointer, 0 wires only), title, sub
    (40, 44, 108, 48, 0, "{req,req}", ""),
    (180, 44, 92, 48, 1, "dbl−pri", ""),
    (300, 44, 74, 48, 1, "dbl&~", ""),
    (402, 44, 74, 48, 2, "lo|hi", ""),
    (402, 156, 74, 48, 3, "rotl", ""),
    (180, 150, 92, 60, 3, "pri", "en=|gnt"),
)
HW_WIRES = (    # points, arrow, label, label x, label y, anchor
    (((2, 68), (40, 68)), True, "req", 4, 58, "start"),
    (((148, 68), (180, 68)), True, "", 0, 0, ""),
    (((164, 68), (164, 24), (337, 24), (337, 44)), True, "dbl", 172, 19, "start"),
    (((272, 68), (300, 68)), True, "", 0, 0, ""),
    (((374, 68), (402, 68)), True, "", 0, 0, ""),
    (((476, 68), (576, 68)), True, "gnt", 574, 58, "end"),
    (((504, 68), (504, 180), (476, 180)), True, "", 0, 0, ""),
    (((402, 180), (272, 180)), True, "", 0, 0, ""),
    (((226, 150), (226, 92)), True, "pri", 234, 127, "start"),
)
HW_DOTS = ((164, 68), (504, 68))


def hw_diagram():
    """The block diagram of rr_arbiter."""
    label = ("תרשים המלבנים של rr_arbiter" + NB + ": הבקשות משוכפלות ל-{req, req}, המחסר מוריד מהן את pri, "
             "ההיפוך וה-AND עם dbl משאירים את הבקשה הראשונה מהמצביע, ו-OR של שני החצאים נותן את gnt. "
             "מתחת, הרגיסטר pri נטען מהסיבוב של gnt שמאלה כשיש מענק")
    o = [f'<svg class="figure ab-dp" viewBox="0 0 {HW_W} {HW_H}" direction="ltr" style="max-width:{HW_W / 16:g}rem" '
         f'role="img" aria-label="{escape(label)}">',
         '<defs><marker id="ab-hb" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" '
         'markerHeight="9" orient="auto"><path class="ab-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>']
    for x, y, w, h, stage, title, sub in HW_BLOCKS:
        ty = y + h / 2 + (-4 if sub else 6)
        cls = f" ab-st{stage}" if stage else ""
        o.append(f'<g class="ab-blk{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>'
                 f'<text x="{x + w / 2:g}" y="{ty:g}" text-anchor="middle">{escape(title)}</text>'
                 + (f'<text class="ab-sub" x="{x + w / 2:g}" y="{y + h / 2 + 17:g}" text-anchor="middle">{escape(sub)}</text>' if sub else "")
                 + "</g>")
    for pts, arrow, lab, lx, ly, anchor in HW_WIRES:
        d = "M" + " L".join(f"{x:g},{y:g}" for x, y in pts)
        head = ' marker-end="url(#ab-hb)"' if arrow else ""
        o.append(f'<path class="ab-wire" d="{d}"{head}/>')
        if lab:
            o.append(f'<text class="ab-wlab" x="{lx}" y="{ly}" text-anchor="{anchor}">{escape(lab)}</text>')
    o += [f'<circle class="ab-dot" cx="{x}" cy="{y}" r="3.5"/>' for x, y in HW_DOTS]
    return "".join(o) + "</svg>"


def hw_legend():
    return ('<span class="viz-legend"><span><i class="ab-key-0"></i>השכפול' + NB + ': חוטים בלבד</span>'
            '<span><i class="ab-key-1"></i>הבחירה' + NB + ': מחסר, היפוך ו-AND</span>'
            '<span><i class="ab-key-2"></i>הקיפול' + NB + ': ‏OR של שני החצאים</span>'
            '<span><i class="ab-key-3"></i>המצביע' + NB + ': סיבוב של gnt ורגיסטר</span></span>')


# the weighted round robin clock by clock: weights 1, 2, 3, 4 under full load, and
# requester 2 drops its request in the middle of its turn (cycle 4)
TRACE_REQS = [0b1111] * 4 + [0b1011] + [0b1111] * 4


def wrr_trace_table(reqs=TRACE_REQS, weights=WEIGHTS):
    n = len(weights)
    rows = [f"| מחזור | {RLM}`req` | {RLM}`pri` | {RLM}`used` | {RLM}`gnt` | מה קורה |", "|:-:|:-:|:-:|:-:|:-:|---|"]
    trace = wrr_trace(reqs, weights)
    for t, (r, pri, used, g) in enumerate(trace):
        holder, win = pri.bit_length() - 1, g.bit_length() - 1
        now = used + 1 if win == holder else 1
        what = "" if win == holder else f"מבקש {holder} הפסיק לבקש{NB}: {win} זוכה ופותח תור חדש, "
        what += f"מענק {now} מתוך {weights[win]}"
        if now == weights[win]:
            what += f", והמצביע עובר ל-{(win + 1) % n}"
        else:
            what += ", והמצביע נשאר" if win == holder else f", והמצביע עובר אל {win}"
        rows.append(f"| {RLM}{t} | {RLM}`{bits(r, n)}` | {RLM}`{bits(pri, n)}` | {RLM}{used} | {RLM}`{bits(g, n)}` | {what} |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [grids(), grids_legend(), trick_table(), hw_diagram(), hw_legend(), wrr_table(), wrr_trace_table()]


if __name__ == "__main__":
    print([bin(g) for g in rr(FULL)], [bin(g) for g in wrr([0b1111] * 12, WEIGHTS)])
    print("\n\n".join(blocks()))
