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
and the table of a weighted round robin. tests/0054 checks the page code (Python, and the
SystemVerilog modules and checker in Verilator) against these.
"""

N = 4
RLM = "‏"


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
         'aria-label="ארבעה מבקשים שמבקשים כל הזמן : ב-fixed priority רק מבקש 0 מקבל, ב-round robin כל אחד מקבל פעם בארבעה מחזורים">')
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


def blocks():
    """The generated blocks, in page order."""
    return [grids(), grids_legend(), trick_table(), wrr_table()]


if __name__ == "__main__":
    print([bin(g) for g in rr(FULL)], [bin(g) for g in wrr([0b1111] * 12, WEIGHTS)])
    print("\n\n".join(blocks()))
