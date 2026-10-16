#!/usr/bin/env python3
"""Inline SVG figure of question 0013 (sort four digits and subtract).

    python tools/figures/q0013.py > /tmp/q0013.html

Prints one figure: every possible difference 999p + 90q as a triangle (rows p = 1..9,
columns q = 0..p). Column q = 0 and the fixed point 6174 are highlighted.
"""

W, H = 46, 26                                  # cell size
X0, Y0 = 52, 26                                # top-left corner of the grid


def step(x):
    d = sorted(f"{x:04d}")
    return int("".join(reversed(d))) - int("".join(d))


def candidates():
    body = []
    for q in range(10):
        body.append(f'<text class="tick" x="{X0 + q * W + W / 2}" y="{Y0 - 9}" text-anchor="middle">q = {q}</text>')
    for p in range(1, 10):
        y = Y0 + (p - 1) * H
        body.append(f'<text class="tick" x="{X0 - 8}" y="{y + H / 2 + 5}" text-anchor="end">p = {p}</text>')
        for q in range(p + 1):
            x, v = X0 + q * W, 999 * p + 90 * q
            body.append(f'<rect class="box-node" x="{x}" y="{y}" width="{W}" height="{H}"/>')
            if step(v) == v:
                body.append(f'<rect class="cell-s2" x="{x}" y="{y}" width="{W}" height="{H}"/>')
            elif q == 0:
                body.append(f'<rect class="cell-s1" x="{x}" y="{y}" width="{W}" height="{H}"/>')
            body.append(f'<text class="box-num" x="{x + W / 2}" y="{y + H / 2 + 5}" '
                        f'text-anchor="middle">{v:04d}</text>')
    width, height = X0 + 10 * W + 6, Y0 + 9 * H + 6
    return (f'<svg class="figure" viewBox="0 0 {width} {height}" role="img" '
            f'aria-label="כל 54 ההפרשים האפשריים 999p + 90q, ורק 6174 חוזר לעצמו">{"".join(body)}</svg>')


if __name__ == "__main__":
    print(candidates())
