"""Rows of cells for the in-place questions (0072 to 0075): an array, a deck, the memory of
a matrix or the bits of a word, drawn as a small HTML table (class pm-cells) rather than an
SVG, so it wraps its text at the page's own size on a phone.

A row is (label, cells, value): the label in the first column, then a cell per entry, and
an optional value at the end. A cell is a text or a (text, classes) pair; the classes are
c1 .. c5 (the tint of a cycle or a group), is-hl (framed: the cells a step works on),
is-off (a cell that is not part of the drawing) and is-gap (an empty spacer column).
"""

from __future__ import annotations

from html import escape


def cell(c) -> str:
    text, cls = (c, "") if not isinstance(c, tuple) else c
    return f'<td class="pm-c{(" " + cls) if cls else ""}">{escape(str(text))}</td>'


def table(rows, aria: str, head: list[str] | None = None, value_head: str | None = None) -> str:
    """rows: [(label, [cells], value or None)]; head: the column titles over the cells
    (indices), shown in a first row when given."""
    out = [f'<div class="pm-scroll" tabindex="0" role="region" aria-label="{escape(aria)}"><table class="pm-cells" dir="ltr"><tbody>']
    if head is not None:
        has_val = any(v is not None for _, _, v in rows)
        out.append("<tr class=\"pm-head\"><th></th>" + "".join(f"<td>{escape(str(h))}</td>" for h in head)
                   + (f"<td class=\"pm-val\">{escape(value_head or '')}</td>" if has_val else "") + "</tr>")
    for label, cells, value in rows:
        out.append(f'<tr><th dir="rtl">{escape(label)}</th>' + "".join(cell(c) for c in cells)
                   + (f'<td class="pm-val">{escape(str(value))}</td>' if value is not None else "") + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def legend(items: list[tuple[str, str]]) -> str:
    """A legend line: (key class, text) pairs; the key classes are pm-key-c1 .. pm-key-hl."""
    spans = "".join(f'<span><i class="{k}"></i>{escape(t)}</span>' for k, t in items)
    return f'<span class="viz-legend">{spans}</span>'
