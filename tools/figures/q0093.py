#!/usr/bin/env python3
"""Figures and tables of question 0093, stable matching (Gale–Shapley).

    python tools/figures/fill.py 93        # put the blocks on the page

blocks() returns them in page order; the page marks each one with <!-- gen n --> and
<!-- /gen -->. The functions above blocks() are the reference the question's tests use: the
proposal algorithm one proposal at a time and by rounds, the blocking pairs of a matching,
every stable matching by brute force, and a family of instances that needs n² − n + 1
proposals.

Candidates are A, B, C, ... (index 0, 1, 2, ...) and jobs 1, 2, 3, ... (index 0, 1, 2, ...).
A matching is a list: match[i] is the job of candidate i.
"""

from __future__ import annotations

import itertools
from collections import deque
from html import escape

RLM = "\u200f"
NB = "\u00a0"

# --- the example of the page: six candidates and six jobs, best first --------------------------------

CAND_TEXT = {"A": "615324", "B": "142356", "C": "213645", "D": "365241", "E": "341562", "F": "136425"}
JOB_TEXT = {1: "ECBAFD", 2: "ABFDEC", 3: "AFCDEB", 4: "ADCEFB", 5: "DCEFAB", 6: "FCDAEB"}

CAND = [[int(c) - 1 for c in CAND_TEXT[k]] for k in "ABCDEF"]          # candidate i: job indices
JOBS = [[ord(c) - 65 for c in JOB_TEXT[j]] for j in range(1, 7)]       # job j: candidate indices
N = 6


def cname(i):
    return chr(65 + i)


def jname(j):
    return str(j + 1)


# --- the reference -------------------------------------------------------------------------------------

def ranks(prefs):
    """rank[x][y]: where y stands on x's list (0 = first)."""
    n = len(prefs)
    r = [[0] * n for _ in range(n)]
    for x, lst in enumerate(prefs):
        for k, y in enumerate(lst):
            r[x][y] = k
    return r


def gs_steps(P, Q):
    """The proposal algorithm with a queue of free proposers. P[i]: proposer i's list, Q[j]:
    receiver j's list. Returns (match, steps): match[i] is proposer i's receiver, and each step
    is (proposer, receiver, kind, freed) with kind "take" (the receiver was free), "swap" (it
    trades up and frees `freed`) or "no" (it keeps its proposer and refuses)."""
    n = len(P)
    rq = ranks(Q)
    nxt, held, free, steps = [0] * n, [None] * n, deque(range(n)), []
    while free:
        i = free.popleft()
        j = P[i][nxt[i]]
        nxt[i] += 1
        if held[j] is None:
            held[j] = i
            steps.append((i, j, "take", None))
        elif rq[j][i] < rq[j][held[j]]:
            free.append(held[j])
            steps.append((i, j, "swap", held[j]))
            held[j] = i
        else:
            free.append(i)
            steps.append((i, j, "no", None))
    match = [None] * n
    for j, i in enumerate(held):
        match[i] = j
    return match, steps


def gs(P, Q):
    match, steps = gs_steps(P, Q)
    return match, len(steps)


def gs_rounds(P, Q):
    """The same algorithm by rounds: every free proposer proposes to its next receiver at once,
    and every receiver keeps the best of its proposer and the new ones. Returns the rounds as
    (proposals [(i, j)], refused [(i, j)], held after the round {j: i})."""
    n = len(P)
    rq = ranks(Q)
    nxt, held, free, rounds = [0] * n, {}, list(range(n)), []
    while free:
        props = []
        for i in free:
            props.append((i, P[i][nxt[i]]))
            nxt[i] += 1
        refused, newfree = [], []
        for j in sorted({j for _, j in props}):
            cands = [i for i, jj in props if jj == j] + ([held[j]] if j in held else [])
            best = min(cands, key=lambda i: rq[j][i])
            for i in cands:
                if i != best:
                    refused.append((i, j))
                    newfree.append(i)
            held[j] = best
        free = sorted(newfree)
        rounds.append((props, sorted(refused), dict(held)))
    return rounds


def blocking(P, Q, match):
    """Every pair (proposer i, receiver j) that prefer each other to their partners."""
    n = len(match)
    rp, rq = ranks(P), ranks(Q)
    partner = {j: i for i, j in enumerate(match)}
    return [(i, j) for i in range(n) for j in range(n)
            if rp[i][j] < rp[i][match[i]] and rq[j][i] < rq[j][partner[j]]]


def all_stable(P, Q):
    """Every stable matching, by trying all n! matchings."""
    n = len(P)
    return [list(m) for m in itertools.permutations(range(n)) if not blocking(P, Q, list(m))]


def flip(match):
    """A matching seen from the receivers: out[j] is the proposer of receiver j."""
    out = [None] * len(match)
    for i, j in enumerate(match):
        out[j] = i
    return out


def rank_sums(P, Q, match):
    """(the sum of the proposers' ranks of their partners, the same for the receivers), 1 = first."""
    rp, rq = ranks(P), ranks(Q)
    return (sum(rp[i][j] + 1 for i, j in enumerate(match)),
            sum(rq[j][i] + 1 for i, j in enumerate(match)))


def greedy_by_order(P):
    """Candidates choose in turn, A first: each takes the best job no one took yet."""
    taken, match = set(), []
    for lst in P:
        j = next(j for j in lst if j not in taken)
        taken.add(j)
        match.append(j)
    return match


def worst_case(n):
    """An instance with n proposers that needs n² − n + 1 proposals. Proposer i's list runs
    around the first n − 1 receivers from i % (n − 1) and ends with receiver n − 1; receiver
    j < n − 1 ranks proposer j + 1 first, then proposer n − 1, then the rest around the
    cycle."""
    m = n - 1
    P = [[(i + k) % m for k in range(m)] + [m] for i in range(n)]
    Q = []
    for j in range(n):
        if j == m:
            Q.append(list(range(n)))
            continue
        order = [(j + 1 + k) % m for k in range(m)]
        order.insert(1, m)
        Q.append(order)
    return P, Q


def restrict(n):
    """The example cut to the first n candidates and the first n jobs (the box's sizes 3 to 5)."""
    return ([[j for j in CAND[i] if j < n] for i in range(n)],
            [[i for i in JOBS[j] if i < n] for j in range(n)])


def immediate(P, Q):
    """Acceptance at once: by rounds, every free proposer proposes to its next receiver that is
    still free; a receiver takes the best of that round's proposals for good."""
    n = len(P)
    rq = ranks(Q)
    nxt, held, free = [0] * n, {}, list(range(n))
    while free:
        props = {}
        for i in free:
            while P[i][nxt[i]] in held:
                nxt[i] += 1
            props.setdefault(P[i][nxt[i]], []).append(i)
            nxt[i] += 1
        for j, cands in props.items():
            held[j] = min(cands, key=lambda i: rq[j][i])
        free = sorted(i for i in free if i not in held.values())
    return flip([held[j] for j in range(n)])


def best_lie(P, Q):
    """Receivers who gain by lying while the proposers propose: (j, the list it reports, its
    partner by the truth, its partner by the lie), the best lie of each receiver that gains."""
    rq = ranks(Q)
    honest = flip(gs(P, Q)[0])
    out = []
    for j in range(len(Q)):
        best = None
        for lie in itertools.permutations(Q[j]):
            Q2 = [list(lie) if k == j else q for k, q in enumerate(Q)]
            got = flip(gs(P, Q2)[0])[j]
            if rq[j][got] < rq[j][honest[j]] and (best is None or rq[j][got] < rq[j][best[3]]):
                best = (j, list(lie), honest[j], got)
        if best:
            out.append(best)
    return out


# --- the blocks -----------------------------------------------------------------------------------

def ltr(text):
    return f'<span dir="ltr">{text}</span>'


def rtl_cells(rows):
    """Markdown table rows with every cell that would start with a Latin letter, bold or math
    led by an RLM, so the cell starts right to left."""
    out = []
    for row in rows:
        if set(row) <= set("|:- "):
            out.append(row)
            continue
        cells = row.strip("|").split("|")
        fixed = []
        for c in cells:
            t = c.strip()
            fixed.append(f" {RLM}{t} " if t and (t[0].isascii() and (t[0].isalpha() or t[0] in "*\\")) else c)
        out.append("|" + "|".join(fixed) + "|")
    return "\n".join(out)


def pair(i, j):
    return f"{cname(i)}–{jname(j)}"


def pairs_text(match):
    return ltr(", ".join(pair(i, j) for i, j in enumerate(match)))


def prefs_tables():
    """The two preference lists as tables, first choice in the first column."""
    head = "| | " + " | ".join(f"מקום {k}" for k in range(1, N + 1)) + " |"
    sep = "|:-:|" + ":-:|" * N
    rows_c = [head.replace("| |", "| מועמד |", 1), sep]
    for i in range(N):
        rows_c.append(f"| **{cname(i)}** | " + " | ".join(jname(j) for j in CAND[i]) + " |")
    rows_j = [head.replace("| |", "| משרה |", 1), sep]
    for j in range(N):
        rows_j.append(f"| **{jname(j)}** | " + " | ".join(cname(i) for i in JOBS[j]) + " |")
    return ("**הדירוגים של המועמדים** (המשרות, מהטובה ביותר לפחות טובה)" + NB + ":\n\n" + rtl_cells(rows_c)
            + "\n\n**הדירוגים של המשרות** (המועמדים, מהטוב ביותר לפחות טוב)" + NB + ":\n\n" + rtl_cells(rows_j))


def greedy_table():
    """The matching of candidates choosing in turn, and its blocking pairs."""
    m = greedy_by_order(CAND)
    rp, rq = ranks(CAND), ranks(JOBS)
    partner = flip(m)
    rows = [f"| הזוג החוסם | המועמד{NB}: המשרה שקיבל | המשרה{NB}: המועמד שקיבלה |", "|:-:|:-:|:-:|"]
    for i, j in blocking(CAND, JOBS, m):
        rows.append(f"| {RLM}{ltr(pair(i, j))} | {cname(i)} מדרג את {jname(j)} במקום {rp[i][j] + 1}, "
                    f"ואת {jname(m[i])} שקיבל במקום {rp[i][m[i]] + 1} | "
                    f"{jname(j)} מדרגת את {cname(i)} במקום {rq[j][i] + 1}, ואת {cname(partner[j])} "
                    f"שקיבלה במקום {rq[j][partner[j]] + 1} |")
    return rtl_cells(rows)


def rounds_table():
    rows = ["| סבב | ההצעות | מי נדחה | מה כל משרה מחזיקה אחרי הסבב |", "|:-:|:-:|:-:|:-:|"]
    total = 0
    for k, (props, refused, held) in enumerate(gs_rounds(CAND, JOBS), 1):
        total += len(props)
        p = ltr(", ".join(f"{cname(i)}→{jname(j)}" for i, j in props))
        r = ltr(", ".join(f"{cname(i)}→{jname(j)}" for i, j in refused)) if refused else "אף אחד"
        h = ltr(", ".join(f"{jname(j)}:{cname(i)}" for j, i in sorted(held.items())))
        rows.append(f"| {k} | {RLM}{p} | {RLM}{r} | {RLM}{h} |")
    assert total == gs(CAND, JOBS)[1]
    return rtl_cells(rows)


def match_svg():
    """The result of part a: candidates on the right, jobs on the left; the final pairs solid,
    the proposals that were refused dashed."""
    match, steps = gs_steps(CAND, JOBS)
    W, H, top, gap = 300, 232, 22, 37
    xc, xj = 232, 68
    y = lambda k: top + k * gap
    parts = [f'<svg class="figure sm-match" viewBox="0 0 {W} {H}" style="max-width:19rem" role="img" '
             f'aria-label="{escape("התוצאה של סעיף א" + NB + ": " + ", ".join(pair(i, j) for i, j in enumerate(match)) + ". קו מקווקו הוא הצעה שנדחתה")}">']
    refused = {(i, j) for i, j, kind, _ in steps if kind == "no"} | {(f, j) for _, j, kind, f in steps if kind == "swap"}
    for i, j in sorted(refused):
        parts.append(f'<line class="sm-no" x1="{xc - 14}" y1="{y(i)}" x2="{xj + 14}" y2="{y(j)}"/>')
    for i, j in enumerate(match):
        parts.append(f'<line class="sm-pair" x1="{xc - 14}" y1="{y(i)}" x2="{xj + 14}" y2="{y(j)}"/>')
    for k in range(N):
        parts.append(f'<circle class="sm-cnode" cx="{xc}" cy="{y(k)}" r="13"/>'
                     f'<text class="sm-lab" x="{xc}" y="{y(k) + 5}" text-anchor="middle">{cname(k)}</text>')
        parts.append(f'<rect class="sm-jnode" x="{xj - 13}" y="{y(k) - 13}" width="26" height="26" rx="5"/>'
                     f'<text class="sm-lab" x="{xj}" y="{y(k) + 5}" text-anchor="middle">{jname(k)}</text>')
    parts.append("</svg>")
    legend = ('<span class="viz-legend"><span><i class="sm-key-c"></i><span>מועמד</span></span>'
              '<span><i class="sm-key-j"></i><span>משרה</span></span>'
              '<span><i class="sm-key-pair"></i><span>הזוגות בסוף</span></span>'
              '<span><i class="sm-key-no"></i><span>הצעה שנדחתה, מיד או אחר כך</span></span></span>')
    return "".join(parts) + "\n\n" + legend


TIGHT_N = 3


def tight_example():
    """The instance of worst_case(3) with the page's names (proposers A, B, C, receivers 1, 2,
    3): the lists of both sides, then its seven proposals one by one."""
    n = TIGHT_N
    P, Q = worst_case(n)
    head = "| מי מדרג | " + " | ".join(f"מקום {k}" for k in range(1, n + 1)) + " |"
    sep = "|:-:|" + ":-:|" * n
    rows = [head, sep]
    for i in range(n):
        rows.append(f"| **{cname(i)}** | " + " | ".join(jname(j) for j in P[i]) + " |")
    for j in range(n):
        rows.append(f"| **{jname(j)}** | " + " | ".join(cname(i) for i in Q[j]) + " |")
    _, steps = gs_steps(P, Q)
    trace = ["| הצעה | מי מציע למי | מה קורה |", "|:-:|:-:|---|"]
    for k, (i, j, kind, freed) in enumerate(steps, 1):
        what = {"take": f"מקבל {jname(j)} פנוי ומחזיק את {cname(i)}",
                "swap": f"מקבל {jname(j)} מעדיף את {cname(i)} ומשחרר את {cname(freed)}" if freed is not None else "",
                "no": f"מקבל {jname(j)} מעדיף את מי שהוא מחזיק, ו-{cname(i)} נדחה"}[kind]
        trace.append(f"| {k} | {RLM}{ltr(f'{cname(i)}→{jname(j)}')} | {what} |")
    return rtl_cells(rows) + "\n\n" + rtl_cells(trace)


BOUND_NS = range(2, 8)


def bound_table():
    rows = ["| \\( n \\) | הצעות במקרה הזה | \\( n^2 - n + 1 \\) | \\( n^2 \\) |", "|:-:|:-:|:-:|:-:|"]
    for n in BOUND_NS:
        P, Q = worst_case(n)
        rows.append(f"| {n} | {gs(P, Q)[1]} | {n * n - n + 1} | {n * n} |")
    return rtl_cells(rows)


def stable_sorted():
    """The stable matchings of the example, the candidates' best first (by their rank sum, then
    the jobs' rank sum)."""
    S = all_stable(CAND, JOBS)
    return sorted(S, key=lambda m: rank_sums(CAND, JOBS, m))


def stable_table():
    cm = gs(CAND, JOBS)[0]
    jm = flip(gs(JOBS, CAND)[0])
    rows = ["| השידוך | " + " | ".join(f"המשרה של {cname(i)}" for i in range(N)) + " | Σ מועמדים | Σ משרות |",
            "|:-:|" + ":-:|" * (N + 2)]
    for k, m in enumerate(stable_sorted(), 1):
        sc, sj = rank_sums(CAND, JOBS, m)
        tag = "המועמדים מציעים" if m == cm else "המשרות מציעות" if m == jm else ""
        rows.append(f"| {k}{(NB + ': ' + tag) if tag else ''} | " + " | ".join(jname(j) for j in m) + f" | {sc} | {sj} |")
    return rtl_cells(rows)


def extremes_table():
    """Per candidate: its partners over all stable matchings, best and worst, and what each side
    proposing gives it; then the same per job."""
    S = stable_sorted()
    rp, rq = ranks(CAND), ranks(JOBS)
    cm, jm = gs(CAND, JOBS)[0], flip(gs(JOBS, CAND)[0])
    rows = ["| | כל האפשרויות | הכי טוב | הכי גרוע | מועמדים מציעים | משרות מציעות |",
            "|:-:|:-:|:-:|:-:|:-:|:-:|"]
    for i in range(N):
        opts = sorted({m[i] for m in S}, key=lambda j: rp[i][j])
        rows.append(f"| **{cname(i)}** | {RLM}{ltr(', '.join(jname(j) for j in opts))} | {jname(opts[0])} | "
                    f"{jname(opts[-1])} | {jname(cm[i])} | {jname(jm[i])} |")
    for j in range(N):
        opts = sorted({flip(m)[j] for m in S}, key=lambda i: rq[j][i])
        rows.append(f"| **{jname(j)}** | {RLM}{ltr(', '.join(cname(i) for i in opts))} | {cname(opts[0])} | "
                    f"{cname(opts[-1])} | {cname(flip(cm)[j])} | {cname(flip(jm)[j])} |")
    return rtl_cells(rows)


def blocks():
    """The generated blocks, in page order."""
    return [
        prefs_tables(),
        greedy_table(),
        rounds_table(),
        match_svg(),
        tight_example(),
        bound_table(),
        stable_table(),
        extremes_table(),
    ]


if __name__ == "__main__":
    print("\n\n".join(blocks()))
