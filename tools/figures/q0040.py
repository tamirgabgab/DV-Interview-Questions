#!/usr/bin/env python3
"""Figures and tables of question 0040 (a sequence detector for 1011 with overlap, then
any pattern through the KMP automaton).

    python tools/figures/fill.py 40        # put the blocks on the page

The reference here is independent of the page code: table(pattern) builds the automaton
by brute force (the next state is the longest suffix of "what was seen so far plus the
bit" that is a prefix of the pattern), and the page's KMP construction must agree.
blocks() returns: the Mealy state diagram of 1011 and its legend, its transition table,
the bit-by-bit table of the stream 1011011, the Moore transition table, the tables of the
automata of several patterns for part b, the block diagram of part a's circuit (state
register, next-state logic, output logic; din -> found combinational in Mealy) and its
legend, and the trace of the fail recurrence for 1011. The page's markers carry these
indices (not in page order). tests/0040 checks the numbers against the page code and
against brute force.
"""

PATTERN = "1011"
STREAM = "1011011"
RLM = "‏"


# --- the model (brute force) -------------------------------------------------------------

def longest_prefix_suffix(seen, pattern):
    """The length of the longest suffix of `seen` that is a prefix of `pattern`, at most
    len(pattern) (state len(pattern) is "the pattern just ended")."""
    for s in range(min(len(seen), len(pattern)), -1, -1):
        if seen.endswith(pattern[:s]):
            return s
    return 0


def table(pattern):
    """nxt[s][b] for the states 0..L (L is the full match) by brute force."""
    L = len(pattern)
    nxt = []
    for s in range(L + 1):
        nxt.append([longest_prefix_suffix(pattern[:s] + b, pattern) for b in "01"])
    return nxt


def rest(pattern):
    """The Mealy state the full match collapses to: the longest proper suffix of the
    pattern that is a prefix of it."""
    return longest_prefix_suffix(pattern[1:], pattern) if len(pattern) > 1 else 0


def run(pattern, bits, moore=False):
    """The state before every bit and the output per bit (Mealy: on the bit that completes
    the pattern; Moore: one cycle later, from the full-match state)."""
    L, nxt, state, states, out = len(pattern), table(pattern), 0, [], []
    for b in bits:
        states.append(state)
        nstate = nxt[state][int(b)]
        out.append(int(state == L) if moore else int(nstate == L))
        state = nstate if (moore or nstate < L) else rest(pattern)
    return states, out


def brute(pattern, bits, moore=False):
    """Found at every position where the last L bits equal the pattern (Moore: a cycle later)."""
    L = len(pattern)
    hit = [int(i + 1 >= L and bits[i + 1 - L:i + 1] == pattern) for i in range(len(bits))]
    return ([0] + hit)[:len(bits)] if moore else hit


# --- tables ------------------------------------------------------------------------------

def name(s, pattern, L):
    return f"S{s}"


def meaning(s, pattern):
    return "התחלה" if s == 0 else f"{RLM}`{pattern[:s]}`"


def mealy_table(pattern=PATTERN):
    L, nxt = len(pattern), table(pattern)
    lines = ["| המצב | מה נראה עד כה | הביט הבא 0 | הביט הבא 1 |", "|:-:|:-:|:-:|:-:|"]
    for s in range(L):
        cells = []
        for b in (0, 1):
            n = nxt[s][b]
            cells.append(f"{RLM}S{rest(pattern)}, **הפלט 1**" if n == L else f"{RLM}S{n}")
        lines.append(f"| {RLM}S{s} | {meaning(s, pattern)} | {cells[0]} | {cells[1]} |")
    return "\n".join(lines)


def moore_table(pattern=PATTERN):
    L, nxt = len(pattern), table(pattern)
    lines = ["| המצב | מה נראה עד כה | הפלט | הביט הבא 0 | הביט הבא 1 |", "|:-:|:-:|:-:|:-:|:-:|"]
    for s in range(L + 1):
        lines.append(f"| {RLM}S{s} | {meaning(s, pattern)} | {RLM}{int(s == L)} | {RLM}S{nxt[s][0]} | {RLM}S{nxt[s][1]} |")
    return "\n".join(lines)


def stream_table(pattern=PATTERN, bits=STREAM):
    states, out = run(pattern, bits)
    lines = ["| מחזור | הביט | המצב לפני | המצב אחרי | הפלט |", "|:-:|:-:|:-:|:-:|:-:|"]
    for i, b in enumerate(bits):
        after = states[i + 1] if i + 1 < len(states) else run(pattern, bits + "0")[0][-1]
        lines.append(f"| {RLM}{i + 1} | {RLM}{b} | {RLM}S{states[i]} | {RLM}S{after} | {RLM}{'**1** ✓' if out[i] else '0'} |")
    return "\n".join(lines)


EXAMPLES = ["1011", "0110", "1111", "10101", "1101"]


def patterns_table():
    lines = ["| התבנית | המצבים | כישלון של המצב המלא | מעברים (מהמצב, בביט 0 / בביט 1) |", "|:-:|:-:|:-:|---|"]
    for p in EXAMPLES:
        nxt = table(p)
        moves = "; ".join(f"S{s} : {nxt[s][0]} / {nxt[s][1]}" for s in range(len(p)))
        lines.append(f"| {RLM}`{p}` | {RLM}{len(p)} ‏(Mealy), {len(p) + 1} ‏(Moore) | {RLM}S{rest(p)} | {RLM}{moves} |")
    return "\n".join(lines)


# --- the state diagram ---------------------------------------------------------------------

def diagram(pattern=PATTERN):
    """Mealy states in a row: the advancing edges on the line, the self loops above, the
    fall-back edges below, the detecting edge marked. Every state and edge carries a key in
    data-fig (`n<s>`, `e<s>-<bit>-<target>`, an edge's label too), which the steps beside
    the figure light (question-page.js)."""
    L, nxt = len(pattern), table(pattern)
    W, H, Y, R = 660, 240, 118, 26
    xs = [70 + k * (W - 140) / (L - 1) for k in range(L)]
    p = [f'<svg class="figure fs-fig" viewBox="0 0 {W} {H}" style="max-width:41rem" role="img" aria-label="דיאגרמת המצבים של גלאי {pattern} : {L} מצבים, הקשתות מסומנות בביט ובפלט">',
         '<defs><marker id="fs-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 Z" class="fs-arrowhead"/></marker></defs>']
    labels = []
    for s in range(L):
        for b in (0, 1):
            n = nxt[s][b]
            found = n == L
            target = rest(pattern) if found else n
            lab = f"{b} / 1" if found else str(b)
            cls = "fs-edge is-found" if found else "fs-edge"
            key = f'data-fig="e{s}-{b}-{target}"'
            x0, x1 = xs[s], xs[target]
            if target == s + 1:                                     # forward, on the line
                p.append(f'<line class="{cls}" {key} x1="{x0 + R:.1f}" y1="{Y}" x2="{x1 - R - 2:.1f}" y2="{Y}" marker-end="url(#fs-arrow)"/>')
                labels.append((f"{(x0 + x1) / 2:.1f}", Y - 8, lab, found, key))
            elif target == s:                                       # a self loop above
                p.append(f'<path class="{cls}" {key} d="M{x0 - 10:.1f},{Y - R + 4} C{x0 - 34:.1f},{Y - R - 44} {x0 + 34:.1f},{Y - R - 44} {x0 + 10:.1f},{Y - R + 2}" marker-end="url(#fs-arrow)"/>')
                labels.append((f"{x0:.1f}", Y - R - 32, lab, found, key))
            else:                                                   # back (or far forward), below
                depth = 34 + 22 * abs(s - target)
                p.append(f'<path class="{cls}" {key} d="M{x0:.1f},{Y + R} Q{(x0 + x1) / 2:.1f},{Y + R + depth} {x1:.1f},{Y + R + 2}" marker-end="url(#fs-arrow)"/>')
                labels.append((f"{(x0 + x1) / 2:.1f}", Y + R + depth / 2 + 16, lab, found, key))
    for s in range(L):
        p.append(f'<g class="fs-node{" is-start" if s == 0 else ""}" data-fig="n{s}"><circle cx="{xs[s]:.1f}" cy="{Y}" r="{R}"/>'
                 f'<text x="{xs[s]:.1f}" y="{Y + 5}" text-anchor="middle">S{s}</text></g>'
                 f'<text class="fs-meaning" data-fig="n{s}" x="{xs[s]:.1f}" y="{Y + R + 16}" text-anchor="middle">{"start" if s == 0 else pattern[:s]}</text>')
    for x, y, lab, found, key in labels:
        p.append(f'<text class="fs-label{" is-found" if found else ""} halo" {key} x="{x}" y="{y}" text-anchor="middle">{lab}</text>')
    p.append(f'<text class="legend" x="{W - 8}" y="{H - 8}" text-anchor="end">{pattern}, Mealy</text></svg>')
    return "".join(p)


def legend():
    return ('<span class="viz-legend"><span><i class="fs-key"></i>מעבר : הביט שמתקבל</span>'
            '<span><i class="fs-key-found"></i>המעבר שמזהה : הביט / הפלט 1</span></span>')


# --- the circuit of part a: the block diagram --------------------------------------------------

def _arrow_defs(idn):
    return (f'<defs><marker id="{idn}" viewBox="0 0 8 8" refX="7" refY="4" markerUnits="userSpaceOnUse" markerWidth="9" markerHeight="9" orient="auto">'
            '<path class="shw-headp" d="M0,0 L8,4 L0,8 z"/></marker></defs>')


def circuit_svg():
    """The module of part a as blocks: din into the next-state logic (the always_comb case),
    next[1:0] into the state register (two D flip-flops on clk, reset by rst_n), state[1:0]
    back into the next-state logic and into the output logic. In Mealy din also goes straight
    into the output logic (found = (state == S3) & din): a combinational path from din to
    found, drawn in its own colour. explorer/seqhw.js draws the same blocks with the values of
    one clock."""
    W, H = 440, 356

    def box(x, y, w, h, text, cls, sub):
        return (f'<g class="shw-blk {cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>'
                f'<text x="{x + w / 2:g}" y="{y + h / 2 - 3:g}" text-anchor="middle">{text}</text>'
                f'<text class="shw-sub" x="{x + w / 2:g}" y="{y + h / 2 + 14:g}" text-anchor="middle">{sub}</text></g>')

    def line(pts, cls="shw-wire", arrow=True):
        d = "M" + " L".join(f"{x:g},{y:g}" for x, y in pts)
        return f'<path class="{cls}" d="{d}"' + (' marker-end="url(#shw-hb)"' if arrow else "") + "/>"

    def lab(x, y, t, anchor="start", cls="shw-wlab"):
        return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{t}</text>'

    o = [f'<svg class="figure shw-fig shw-dp" viewBox="0 0 {W} {H}" direction="ltr" style="max-width:{W / 16:g}rem" role="img" '
         'aria-label="תרשים המלבנים של הגלאי : din נכנס ללוגיקת המצב הבא, שמחשבת את next משני ביטים. '
         'רגיסטר המצב, שני פליפ-פלופים על clk עם איפוס rst_n, שומר את next בעליית השעון, ו-state חוזר ללוגיקת המצב הבא '
         'ונכנס ללוגיקת המוצא. ב-Mealy גם din נכנס ישר ללוגיקת המוצא : found = (state == S3) & din, '
         'מסלול צירופי מ-din ל-found בלי פליפ-פלופ באמצע">', _arrow_defs("shw-hb")]
    o.append(lab(200, 14, "din", "middle"))
    o.append(line([(200, 20), (200, 58)]))
    o.append(line([(200, 38), (410, 38), (410, 285), (322, 285)], "shw-wire shw-mealy"))
    o.append('<circle class="shw-dot" cx="200" cy="38" r="3"/>')
    o.append(lab(404, 160, "Mealy", "end", "shw-wlab shw-mlab"))
    o.append(box(80, 60, 240, 50, "next-state logic", "shw-logic", "next = f(state, din)"))
    o.append(line([(200, 110), (200, 158)]))
    o.append(lab(208, 140, "next[1:0]"))
    o.append(box(110, 160, 180, 50, "state register", "shw-reg", "2 D flip-flops"))
    o.append(line([(370, 185), (292, 185)]))
    o.append(lab(298, 178, "clk, rst_n"))
    o.append(line([(200, 210), (200, 258)]))
    o.append('<circle class="shw-dot" cx="200" cy="235" r="3"/>')
    o.append(line([(200, 235), (40, 235), (40, 85), (78, 85)]))
    o.append(lab(208, 250, "state[1:0]"))
    o.append(box(80, 260, 240, 50, "output logic", "shw-out", "found = (state == S3) &amp; din"))
    o.append(line([(200, 310), (200, 343)]))
    o.append(lab(208, 338, "found"))
    return "".join(o) + "</svg>"


def circuit_legend():
    return ('<span class="viz-legend"><span><i class="shw-key-reg"></i>רגיסטר המצב : פליפ-פלופים</span>'
            '<span><i class="shw-key-logic"></i>לוגיקה צירופית</span>'
            '<span><i class="shw-key-mealy"></i>‏din → found : מסלול צירופי, רק ב-Mealy</span></span>')


# --- part b: the fail recurrence, row by row -----------------------------------------------------

def fails(pattern=PATTERN):
    """fail(s) for s = 1..L by the recurrence of the page: fail(1) = 0 and
    fail(s + 1) = next[fail(s)][P[s]], on the brute-force table."""
    nxt, out = table(pattern), [0]
    for s in range(1, len(pattern)):
        out.append(nxt[out[-1]][int(pattern[s])])
    return out


def fail_table(pattern=PATTERN):
    """The four rows of 1011: what matched, without its first bit, fail(s), how the
    recurrence gives it, and the edge on the bit that does not match."""
    L, nxt, fl = len(pattern), table(pattern), fails(pattern)
    for s in range(1, L + 1):                        # fail(s) is the state of P[1..s-1]
        assert fl[s - 1] == longest_prefix_suffix(pattern[1:s], pattern)
    lines = ["| המצב | התאים | בלי הביט הראשון | ‏fail | איך מקבלים את fail | הביט שלא מתאים |", "|:-:|:-:|:-:|:-:|---|---|"]
    for s in range(1, L + 1):
        f = fl[s - 1]
        how = "התחלה : שום ביט" if s == 1 else f"{RLM}`next[{fl[s - 2]}][P[{s - 1}]] = next[{fl[s - 2]}][{pattern[s - 1]}]`"
        if s < L:
            b = 1 - int(pattern[s])
            miss = f"{RLM}`{b} → next[{f}][{b}] = {nxt[f][b]}`"
        else:
            miss = f"שניהם, כמו ב-{RLM}`S{f}` : `next[{L}] = next[{f}]`"
        rest_cell = f"{RLM}`{pattern[1:s]}`" if s > 1 else "ריק"
        lines.append(f"| {RLM}S{s} | {RLM}`{pattern[:s]}` | {rest_cell} | {RLM}{f} | {how} | {miss} |")
    return "\n".join(lines)


# --- the follow-up: two patterns at once ----------------------------------------------------------

def product_states(pa, pb, moore):
    """The states of the product machine reachable from (0, 0): Moore keeps the full-match
    states (5 x 5 pairs for two patterns of 4), Mealy merges each into its rest (4 x 4)."""
    def step(p, s, b):
        n = table(p)[s][b]
        return n if moore or n < len(p) else rest(p)
    seen, todo = {(0, 0)}, [(0, 0)]
    while todo:
        a, c = todo.pop()
        for b in (0, 1):
            t = (step(pa, a, b), step(pb, c, b))
            if t not in seen:
                seen.add(t)
                todo.append(t)
    return seen


def blocks():
    """The generated blocks; the page's markers carry these indices."""
    return [diagram(), legend(), mealy_table(), stream_table(), moore_table(), patterns_table(),
            circuit_svg(), circuit_legend(), fail_table()]


if __name__ == "__main__":
    print(table(PATTERN), rest(PATTERN), run(PATTERN, STREAM))
    print("\n\n".join(blocks()))
