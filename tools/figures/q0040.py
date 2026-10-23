#!/usr/bin/env python3
"""Figures and tables of question 0040 (a sequence detector for 1011 with overlap, then
any pattern through the KMP automaton).

    python tools/figures/fill.py 40        # put the blocks on the page

The reference here is independent of the page code: table(pattern) builds the automaton
by brute force (the next state is the longest suffix of "what was seen so far plus the
bit" that is a prefix of the pattern), and the page's KMP construction must agree.
blocks() returns, in page order: the Mealy state diagram of 1011, its transition table,
the bit-by-bit table of the stream 1011011, the Moore transition table, and the tables
of the automata of several patterns for part b. tests/0040 checks the numbers against the
page code and against brute force.
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
    fall-back edges below, the detecting edge marked."""
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
            x0, x1 = xs[s], xs[target]
            if target == s + 1:                                     # forward, on the line
                p.append(f'<line class="{cls}" x1="{x0 + R:.1f}" y1="{Y}" x2="{x1 - R - 2:.1f}" y2="{Y}" marker-end="url(#fs-arrow)"/>')
                labels.append((f"{(x0 + x1) / 2:.1f}", Y - 8, lab, found))
            elif target == s:                                       # a self loop above
                p.append(f'<path class="{cls}" d="M{x0 - 10:.1f},{Y - R + 4} C{x0 - 34:.1f},{Y - R - 44} {x0 + 34:.1f},{Y - R - 44} {x0 + 10:.1f},{Y - R + 2}" marker-end="url(#fs-arrow)"/>')
                labels.append((f"{x0:.1f}", Y - R - 32, lab, found))
            else:                                                   # back (or far forward), below
                depth = 34 + 22 * abs(s - target)
                p.append(f'<path class="{cls}" d="M{x0:.1f},{Y + R} Q{(x0 + x1) / 2:.1f},{Y + R + depth} {x1:.1f},{Y + R + 2}" marker-end="url(#fs-arrow)"/>')
                labels.append((f"{(x0 + x1) / 2:.1f}", Y + R + depth / 2 + 16, lab, found))
    for s in range(L):
        p.append(f'<g class="fs-node{" is-start" if s == 0 else ""}"><circle cx="{xs[s]:.1f}" cy="{Y}" r="{R}"/>'
                 f'<text x="{xs[s]:.1f}" y="{Y + 5}" text-anchor="middle">S{s}</text></g>'
                 f'<text class="fs-meaning" x="{xs[s]:.1f}" y="{Y + R + 16}" text-anchor="middle">{"start" if s == 0 else pattern[:s]}</text>')
    for x, y, lab, found in labels:
        p.append(f'<text class="fs-label{" is-found" if found else ""} halo" x="{x}" y="{y}" text-anchor="middle">{lab}</text>')
    p.append(f'<text class="legend" x="{W - 8}" y="{H - 8}" text-anchor="end">{pattern}, Mealy</text></svg>')
    return "".join(p)


def legend():
    return ('<span class="viz-legend"><span><i class="fs-key"></i>מעבר : הביט שמתקבל</span>'
            '<span><i class="fs-key-found"></i>המעבר שמזהה : הביט / הפלט 1</span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [diagram(), legend(), mealy_table(), stream_table(), moore_table(), patterns_table()]


if __name__ == "__main__":
    print(table(PATTERN), rest(PATTERN), run(PATTERN, STREAM))
    print("\n\n".join(blocks()))
