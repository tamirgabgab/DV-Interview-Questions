#!/usr/bin/env python3
"""Figure of question 0004 (three mislabeled boxes).

    python tools/figures/fill.py 4         # put the block on the page

blocks() returns the one figure of the statement: three closed crates with the labels
"red", "black" and "red and black", each with a question mark on its lid. Colours come
from the crate-* CSS classes in docs/stylesheets/extra.css.
"""

LABELS = [("אדום",), ("שחור",), ("אדום", "ושחור")]
ARIA = "שלוש קופסאות סגורות עם התוויות אדום, שחור, ואדום ושחור"


def crate(i, label):
    """One crate at slot i (0..2): lid, side, front, the label and the box number."""
    x = 20 + 200 * i
    cx = x + 75
    p = [f'<polygon class="crate-top" points="{x},50 {x + 30},20 {x + 180},20 {x + 150},50"/>',
         f'<polygon class="crate-side" points="{x + 150},50 {x + 180},20 {x + 180},120 {x + 150},150"/>',
         f'<rect class="crate-front" x="{x}" y="50" width="150" height="100"/>',
         f'<text class="crate-text" x="{cx + 30}" y="42" font-size="20">?</text>']
    if len(label) == 1:
        p.append(f'<text class="crate-text" x="{cx}" y="108" font-size="22">{label[0]}</text>')
    else:
        p.append(f'<text class="crate-text" x="{cx}" y="94" font-size="22">{label[0]}</text>'
                 f'<text class="crate-text" x="{cx}" y="124" font-size="22">{label[1]}</text>')
    p.append(f'<text class="tick" x="{cx}" y="178" font-size="14" direction="rtl">קופסה {i}</text>')
    return "<g>" + "".join(p) + "</g>"


def statement_figure():
    body = "".join(crate(i, label) for i, label in enumerate(LABELS))
    return (f'<svg class="figure" viewBox="0 0 600 190" role="img" aria-label="{ARIA}">'
            f'<g text-anchor="middle">{body}</g></svg>')


def blocks():
    """The generated blocks, in page order."""
    return [statement_figure()]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
