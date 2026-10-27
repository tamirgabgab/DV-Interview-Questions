#!/usr/bin/env python3
"""Figures and tables of question 0058 (coins in a row, each player takes an end: the
parity trick, the greedy player that loses, the optimal play by intervals, how much the
trick gives away, and an odd number of coins).

    python tools/figures/fill.py 58        # put the blocks on the page

The reference here is independent of the page code: best() is a plain minimax over the
remaining interval (memoized), and play() runs two strategies against each other move by
move. blocks() returns, in page order: the row of part a coloured by the parity of the
place, its legend, the moves of the greedy player against the optimal one and of the
parity trick, the table of the interval values of part c, and the moves of the trick
against the optimal play on the row of part d.
"""

from functools import lru_cache

RLM = "‏"
ROW_A = [1, 2, 5, 3]
ROW_D = [1, 1, 9, 1, 1, 9]
ROW_E = [1, 5, 1]


def best(coins):
    """The most the player to move collects from the whole row, both sides playing their best."""
    c = tuple(coins)

    @lru_cache(maxsize=None)
    def gain(i, j):                       # the most the mover collects on c[i..j]
        if i > j:
            return 0
        rest = sum(c[i:j + 1])
        return max(c[i] + (rest - c[i]) - gain(i + 1, j), c[j] + (rest - c[j]) - gain(i, j - 1))
    return gain(0, len(c) - 1)


def diff_table(coins):
    """d[i][j]: the mover's best lead (own minus the other's) on coins i..j, by minimax."""
    n = len(coins)
    return [[(2 * best(coins[i:j + 1]) - sum(coins[i:j + 1])) if j >= i else None for j in range(n)] for i in range(n)]


# --- strategies: (coins, i, j, state) -> "L" or "R" ------------------------------------------

def greedy(c, i, j, st):
    return "L" if c[i] >= c[j] else "R"


def optimal(c, i, j, st):
    """The move that keeps the most, left on a tie."""
    left = c[i] + sum(c[i + 1:j + 1]) - best(c[i + 1:j + 1])
    right = c[j] + sum(c[i:j]) - best(c[i:j])
    return "L" if left >= right else "R"


def parity(c, i, j, st):
    """The parity trick: on the first even row this player sees, fix the parity of the places
    that sum more (0, 2, 4, ... or 1, 3, 5, ...) and always take the end of that parity; on
    an odd row the two ends share a parity, so take the larger end."""
    if (j - i + 1) % 2:
        return greedy(c, i, j, st)
    if "want" not in st:
        st["want"] = 0 if sum(c[k] for k in range(i, j + 1) if k % 2 == 0) >= sum(c[k] for k in range(i, j + 1) if k % 2 == 1) else 1
    return "L" if i % 2 == st["want"] else "R"


STRATS = {"greedy": greedy, "parity": parity, "optimal": optimal}


def play(coins, first, second):
    """Run two strategies; returns the moves as (player, side, coin) and the two totals."""
    i, j, tot, moves, states = 0, len(coins) - 1, [0, 0], [], [{}, {}]
    who = 0
    while i <= j:
        side = STRATS[(first, second)[who]](coins, i, j, states[who])
        coin = coins[i] if side == "L" else coins[j]
        if side == "L":
            i += 1
        else:
            j -= 1
        tot[who] += coin
        moves.append((who, side, coin))
        who ^= 1
    return moves, tot


# --- blocks ------------------------------------------------------------------------------

def row_svg(coins):
    """The row of part a: each coin by the parity of its place."""
    W, R, gap = 400, 26, 70
    x0 = W / 2 - gap * (len(coins) - 1) / 2
    s = (f'<svg class="figure cr-fig" viewBox="0 0 {W} 110" style="max-width:26rem" role="img" '
         f'aria-label="השורה {", ".join(map(str, coins))} : המקומות הזוגיים בצבע אחד והאי-זוגיים בצבע אחר">')
    for k, v in enumerate(coins):
        x = x0 + k * gap
        s += (f'<g class="cr-coin cr-p{k % 2}"><title>place {k + 1}, value {v}</title><circle cx="{x:g}" cy="50" r="{R}"/>'
              f'<text x="{x:g}" y="57" text-anchor="middle">{v}</text></g>'
              f'<text class="tick" x="{x:g}" y="100" text-anchor="middle">{k + 1}</text>')
    return s + "</svg>"


def legend():
    return ('<span class="viz-legend"><span><i class="cr-key-p0"></i>מקום אי-זוגי (1, 3, ...)</span>'
            '<span><i class="cr-key-p1"></i>מקום זוגי (2, 4, ...)</span></span>')


def moves_table(coins, pairs):
    """The moves of two games side by side on the same row."""
    side = {"L": "שמאל", "R": "ימין"}
    name = {"greedy": "חמדן", "parity": "זוגיות", "optimal": "אופטימלי"}
    games = [play(coins, a, b) for a, b in pairs]
    head = " | ".join(f"{name[a]} מול {name[b]}" for a, b in pairs)
    rows = [f"| המהלך | {head} |", "|:-:|" + ":-:|" * len(pairs)]
    for k in range(len(coins)):
        cells = []
        for moves, _ in games:
            who, sd, coin = moves[k]
            cells.append(f"{'הראשון' if who == 0 else 'השני'} : {side[sd]}, {RLM}{coin}")
        rows.append(f"| {RLM}{k + 1} | " + " | ".join(cells) + " |")
    rows.append("| **סך הכול** | " + " | ".join(f"**{RLM}{t[0]} מול {t[1]}**" for _, t in games) + " |")
    return "\n".join(rows)


def dp_table(coins):
    d = diff_table(coins)
    n = len(coins)
    rows = ["| ‏i \\\\ j | " + " | ".join(f"{RLM}{j + 1} ({coins[j]})" for j in range(n)) + " |", "|:-:|" + ":-:|" * n]
    for i in range(n):
        rows.append(f"| {RLM}{i + 1} ({coins[i]}) | " + " | ".join("" if d[i][j] is None else f"{RLM}{d[i][j]}" for j in range(n)) + " |")
    return "\n".join(rows)


def blocks():
    """The generated blocks, in page order."""
    return [row_svg(ROW_A), legend(), moves_table(ROW_A, [("greedy", "optimal"), ("parity", "optimal")]),
            dp_table(ROW_A), moves_table(ROW_D, [("parity", "optimal"), ("optimal", "optimal")])]


if __name__ == "__main__":
    print(best(ROW_A), best(ROW_D), best(ROW_E), play(ROW_A, "greedy", "optimal")[1], play(ROW_D, "parity", "optimal")[1])
    print("\n\n".join(blocks()))
