#!/usr/bin/env python3
"""Figures and tables of question 0041 (how many random tests close coverage: the coupon
collector with n equal bins, then unequal bins and at_least k).

    python tools/figures/fill.py 41        # put the blocks on the page

The reference here is independent of the page code: the expectation n H_n, the chance of
full coverage within t tests by the chain on the number of covered bins (and by
inclusion-exclusion with exact fractions, for the tests), the general
case by the Poisson embedding integrated with Simpson's rule, and the k = 1 closed form
over the subsets. blocks() returns, in page order: the table of expectation, median and
95 % quantile for several n, the chart of P(all covered by t) for n = 16 with the median
and the 95 % line, the table of the waiting times of the 16 bins, and the examples table
of part b (unequal bins, at_least k). tests/0041 checks every number against the page
code and the page's simulation.
"""

import math
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path

N = 16
RLM = "‏"


# --- the model --------------------------------------------------------------------------

def harmonic(n):
    return sum(Fraction(1, i) for i in range(1, n + 1))


def expected_uniform(n):
    return float(n * harmonic(n))


def cover_curve(n, tmax):
    """P(every one of n equal bins is hit within t tests) for t = 0..tmax, by the chain on
    the number of covered bins (stable, unlike the alternating inclusion-exclusion sum)."""
    prob, out = [1.0] + [0.0] * n, []
    for _ in range(tmax + 1):
        out.append(prob[n])
        prob = [prob[c] * c / n + (prob[c - 1] * (n - c + 1) / n if c else 0.0) for c in range(n + 1)]
    return out


def covered_by_exact(n, t):
    """The same by inclusion-exclusion with exact fractions (small n only)."""
    return float(sum((-1) ** j * math.comb(n, j) * Fraction(n - j, n) ** t for j in range(n + 1)))


def tests_for(n, q):
    """The fewest tests that cover everything with probability at least q."""
    prob, t = [1.0] + [0.0] * n, 0
    while prob[n] < q:
        prob = [prob[c] * c / n + (prob[c - 1] * (n - c + 1) / n if c else 0.0) for c in range(n + 1)]
        t += 1
    return t


def poisson_at_least(lam, k):
    """P(Poisson(lam) >= k)."""
    if lam == 0:
        return 0.0 if k > 0 else 1.0
    term, cdf = math.exp(-lam), 0.0
    for j in range(k):
        cdf += term
        term *= lam / (j + 1)
    return max(0.0, 1.0 - cdf)


def expected_general(p, k, h=0.02):
    """E[tests] until every bin i (probability p[i]) has at least k hits: the integral of
    1 - prod P(Poisson(p_i t) >= k) over t, by Simpson's rule until the integrand vanishes."""
    def g(t):
        prod = 1.0
        for pi in p:
            prod *= poisson_at_least(pi * t, k)
        return 1.0 - prod

    total, t = 0.0, 0.0
    while True:
        a, m, b = g(t), g(t + h / 2), g(t + h)
        total += h * (a + 4 * m + b) / 6
        t += h
        if t > 1 and b < 1e-12:
            return total


def expected_k1(p):
    """The k = 1 closed form: sum over the non-empty subsets of (-1)^(|S|+1) / p(S)."""
    total = 0.0
    for r in range(1, len(p) + 1):
        for s in combinations(p, r):
            total += (-1) ** (r + 1) / sum(s)
    return total


# --- tables ------------------------------------------------------------------------------

def quantiles_table(ns=(4, 8, 16, 32, 64, 100)):
    lines = ["| ‏bins | התוחלת ‏n·H_n | חציון | ‏95% | ‏99% | ‏95% לעומת n |", "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for n in ns:
        e, q50, q95, q99 = expected_uniform(n), tests_for(n, 0.5), tests_for(n, 0.95), tests_for(n, 0.99)
        lines.append(f"| {RLM}{n} | {RLM}{e:.1f} | {RLM}{q50} | {RLM}{q95} | {RLM}{q99} | {RLM}×{q95 / n:.1f} |")
    return "\n".join(lines)


def waits_table(n=N):
    lines = ["| ‏bins שכבר כוסו | הסיכוי שטסט פוגע בחדש | טסטים בממוצע עד הפגיעה הבאה |", "|:-:|:-:|:-:|"]
    shown = [0, 1, 2, 4, 8, 12, 14, 15]
    for i in shown:
        lines.append(f"| {RLM}{i} | {RLM}{n - i}/{n} | {RLM}{n / (n - i):.2f} |")
    lines.append(f"| **סך הכול** | | {RLM}**{expected_uniform(n):.1f}** |")
    return "\n".join(lines)


EXAMPLES = [
    ("ארבעה bins שווים", [0.25] * 4, 1),
    ("ארבעה bins, 0.1 / 0.2 / 0.3 / 0.4", [0.1, 0.2, 0.3, 0.4], 1),
    ("ארבעה bins שווים, לפחות 2 פגיעות", [0.25] * 4, 2),
    ("ארבעה bins, 0.1 / 0.2 / 0.3 / 0.4, לפחות 3", [0.1, 0.2, 0.3, 0.4], 3),
    ("‏16 bins שווים", [1 / 16] * 16, 1),
    ("‏16 bins : אחד נדיר (0.01), השאר שווים", [0.01] + [0.99 / 15] * 15, 1),
    ("‏16 bins שווים, לפחות 4 פגיעות", [1 / 16] * 16, 4),
]


def examples_table():
    lines = ["| המקרה | ‏k | התוחלת (האינטגרל) | הנוסחה הסגורה ל-k = 1 |", "|---|:-:|:-:|:-:|"]
    for name, p, k in EXAMPLES:
        closed = f"{RLM}{expected_k1(p):.2f}" if k == 1 and len(p) <= 16 else "—"
        if k == 1 and len(p) == 16 and all(abs(x - 1 / 16) < 1e-12 for x in p):
            closed = f"{RLM}{expected_uniform(16):.2f} = 16·H₁₆"
        lines.append(f"| {name} | {RLM}{k} | {RLM}{expected_general(p, k):.2f} | {closed} |")
    return "\n".join(lines)


# --- the chart ----------------------------------------------------------------------------

def coverage_chart(n=N):
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from charts import Chart

    tmax = tests_for(n, 0.995)
    q50, q95, e = tests_for(n, 0.5), tests_for(n, 0.95), expected_uniform(n)
    c = Chart(f"הסיכוי שכל {n} ה-bins כוסו אחרי t טסטים, עם החציון {q50}, התוחלת {e:.1f} והטסט ה-{q95} שבו מגיעים ל-95%", x_max=tmax, y_max=1, h=250, base=216)
    c.grid_y([0, 0.25, 0.5, 0.75, 1])
    c.grid_x([0, 25, 50, 75, 100, 125], dashed=True)
    c.hline(0.95, "95%", label_at="end")
    c.hline(0.5, "50%", label_at="end", cls="grid", width=1)
    curve = cover_curve(n, tmax)
    c.path([(t, v) for t, v in enumerate(curve)], "s1-line")
    c.vline(q50, 0.5, f"חציון {q50}")
    c.vline(e, curve[round(e)], f"תוחלת {e:.1f}")
    c.vline(q95, 0.95, f"95% : {q95}")
    c.axis("טסטים")
    return c.svg()


def chart_legend(n=N):
    return (f'<span class="viz-legend"><span><i class="by-multiples"></i>‏P(כל {n} ה-bins כוסו אחרי t טסטים)</span>'
            f'<span><i class="ink"></i>החציון, התוחלת והטסט שבו מגיעים ל-95%</span></span>')


def blocks():
    """The generated blocks, in page order."""
    return [waits_table(), quantiles_table(), coverage_chart(), chart_legend(), examples_table()]


if __name__ == "__main__":
    print(expected_uniform(16), tests_for(16, 0.5), tests_for(16, 0.95), expected_general([0.1, 0.2, 0.3, 0.4], 1), expected_k1([0.1, 0.2, 0.3, 0.4]))
    print("\n\n".join(blocks()))
