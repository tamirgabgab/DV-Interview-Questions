#!/usr/bin/env python3
"""Figures and tables of question 0060 (the longest run of ones with up to k zeros flipped,
and the longest window of one value on a bus with up to k replacements).

    python tools/figures/fill.py 60        # put the blocks on the page

The reference here is independent of the page code: brute_ones() and brute_same() try every
window, trace_ones() and trace_same() replay the sliding window step by step (the rows of
the table and what the onesk explorer draws). blocks() returns, in page order: the strip of
part a with its best window, its legend, the table of the window's steps on the page's
example, the strip of part b and its legend.
"""

RLM = "‏"
BITS = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0]
K = 2
BUS = "AAABBCBABA"
K_BUS = 2


def brute_ones(bits, k):
    """The longest window with at most k zeros, every window tried."""
    best = 0
    for i in range(len(bits)):
        for j in range(i, len(bits)):
            if bits[i:j + 1].count(0) <= k:
                best = max(best, j - i + 1)
    return best


def brute_same(values, k):
    """The longest window that is one value after at most k replacements, every window tried."""
    best = 0
    for i in range(len(values)):
        for j in range(i, len(values)):
            w = values[i:j + 1]
            if len(w) - max(w.count(v) for v in set(w)) <= k:
                best = max(best, j - i + 1)
    return best


def trace_ones(bits, k):
    """The sliding window of part a, one row per step: the right end just added, the zeros
    in the window, the left end after the window shrank, the best so far and its window."""
    rows, left, zeros, best, win = [], 0, 0, 0, None
    for right, b in enumerate(bits):
        zeros += b == 0
        moved = 0
        while zeros > k:
            zeros -= bits[left] == 0
            left += 1
            moved += 1
        if right - left + 1 > best:
            best, win = right - left + 1, (left, right)
        rows.append({"right": right, "bit": b, "zeros": zeros, "left": left, "moved": moved, "best": best, "win": win})
    return rows


def trace_same(values, k):
    """The sliding window of part b, one row per step: the counts in the window, the most
    frequent value, the left end after the window shrank, the best so far and its window."""
    rows, left, best, win, count = [], 0, 0, None, {}
    for right, v in enumerate(values):
        count[v] = count.get(v, 0) + 1
        moved = 0
        while right - left + 1 - max(count.values()) > k:
            count[values[left]] -= 1
            left += 1
            moved += 1
        if right - left + 1 > best:
            best, win = right - left + 1, (left, right)
        window = values[left:right + 1]
        top = max(window, key=lambda c: (count[c], -window.index(c)))      # the first in the window on a tie
        rows.append({"right": right, "value": v, "count": dict(count), "top": top, "left": left, "moved": moved, "best": best, "win": win})
    return rows


def best_window(rows):
    """The best window of a trace and the places in it that are flipped or replaced."""
    last = rows[-1]
    return last["win"], last["best"]


# --- blocks ------------------------------------------------------------------------------

def strip_svg(values, win, flips, label, cell=34):
    """A row of cells, drawn left to right: the best window outlined, the cells that are
    flipped (or replaced) in orange, the cells that already hold the value in blue."""
    n = len(values)
    W, H, top = n * cell + 16, 92, 22
    s = (f'<svg class="figure ok-fig" viewBox="0 0 {W} {H}" style="max-width:{W / 16:g}rem" role="img" aria-label="{label}">')
    i, j = win
    s += f'<rect class="ok-win" x="{8 + i * cell - 4}" y="{top - 5}" width="{(j - i + 1) * cell + 8}" height="{cell + 10}" rx="6"/>'
    for p, v in enumerate(values):
        x = 8 + p * cell
        kind = "is-flip" if p in flips else "is-one" if i <= p <= j else "is-off"
        s += (f'<g class="ok-cell {kind}"><title>place {p}, value {v}</title>'
              f'<rect x="{x + 2}" y="{top}" width="{cell - 4}" height="{cell}" rx="4"/>'
              f'<text x="{x + cell / 2:g}" y="{top + cell / 2 + 6}" text-anchor="middle">{v}</text></g>'
              f'<text class="tick" x="{x + cell / 2:g}" y="{H - 8}" text-anchor="middle">{p}</text>')
    return s + "</svg>"


def legend(flip_text):
    return ('<span class="viz-legend"><span><i class="ok-key-one"></i>כבר בערך הרצוי</span>'
            f'<span><i class="ok-key-flip"></i>{flip_text}</span>'
            '<span><i class="ok-key-win"></i>החלון הארוך ביותר</span></span>')


def strip_a():
    rows = trace_ones(BITS, K)
    win, best = best_window(rows)
    flips = [p for p in range(win[0], win[1] + 1) if BITS[p] == 0]
    return strip_svg(BITS, win, flips, f"הווקטור {''.join(map(str, BITS))} : החלון הארוך ביותר עם לכל היותר {K} אפסים הוא באורך {best}")


def strip_b():
    rows = trace_same(BUS, K_BUS)
    win, best = best_window(rows)
    i, j = win
    w = BUS[i:j + 1]
    top = max(set(w), key=w.count)
    flips = [p for p in range(i, j + 1) if BUS[p] != top]
    return strip_svg(list(BUS), win, flips, f"הערכים {' '.join(BUS)} על ה-bus : החלון הארוך ביותר של ערך אחד אחרי לכל היותר {K_BUS} החלפות הוא באורך {best}")


def steps_table(bits, k):
    rows = trace_ones(bits, k)
    out = ["| הצעד | הביט שנכנס | אפסים בחלון | הקצה השמאלי | החלון | הטוב עד עכשיו |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for r in rows:
        moved = f" (זז {RLM}{r['moved']})" if r["moved"] else ""
        out.append(f"| {RLM}{r['right']} | {RLM}{r['bit']} | {RLM}{r['zeros']} | {RLM}{r['left']}{moved} | {RLM}{r['left']}..{r['right']} | **{RLM}{r['best']}** |")
    return "\n".join(out)


def blocks():
    """The generated blocks, in page order."""
    return [strip_a(), legend("אפס שהופך לאחד"), steps_table(BITS, K), strip_b(), legend("ערך שמוחלף")]


if __name__ == "__main__":
    print(brute_ones(BITS, K), trace_ones(BITS, K)[-1]["best"], brute_same(BUS, K_BUS), trace_same(BUS, K_BUS)[-1]["best"])
    print("\n\n".join(blocks()))
