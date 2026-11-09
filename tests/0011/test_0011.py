import itertools
import random
from collections import Counter

from extract_code import load_python

ns = load_python(11)
X, O, EMPTY = ns["X"], ns["O"], ns["EMPTY"]
LINES, WRAP_LINES = ns["LINES"], ns["WRAP_LINES"]
final_result, final_boards, randomize = ns["final_result"], ns["final_boards"], ns["randomize"]


def game_tree_ends(lines):
    """Play every possible game (X first) and collect the boards where a game stops."""
    ends, seen = {}, set()

    def play(board, player):
        key = tuple(board)
        if key in seen:
            return
        seen.add(key)
        for p in (X, O):
            if any(all(board[i] == p for i in line) for line in lines):
                ends[key] = p
                return
        if EMPTY not in board:
            ends[key] = "draw"
            return
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = player
                play(board, O if player == X else X)
                board[i] = EMPTY

    play([EMPTY] * 9, X)
    return ends


def test_conditions_match_the_game_tree():
    for lines, counts in [(LINES, {"X": 626, "O": 316, "draw": 16}),
                          (WRAP_LINES, {"X": 882, "O": 432, "draw": 0})]:
        ends = game_tree_ends(lines)
        groups = final_boards(lines)
        assert {r: len(b) for r, b in groups.items()} == counts
        assert {b: r for r, bs in groups.items() for b in bs} == ends


def test_page_examples():
    assert final_result(tuple("XXXOXOOOX")) == "X"           # two lines with the last move
    assert final_result(tuple("XXOXO.O..")) == "O"
    assert final_result(tuple("XOXXOOOXX")) == "draw"
    assert final_result(tuple("XXXOOO...")) is None          # both have a line
    assert final_result(tuple("XXXOO.O..")) is None          # O moved after X won
    assert final_result(tuple("X........")) is None          # the game is not over


def test_steiner_system_and_no_draw():
    extra = WRAP_LINES[len(LINES):]
    assert sorted(map(sorted, extra)) == [[0, 5, 7], [1, 3, 8], [1, 5, 6], [2, 3, 7]]
    for a, b in itertools.combinations(range(9), 2):          # every pair on exactly one line
        assert sum(a in line and b in line for line in WRAP_LINES) == 1
    for cells in itertools.combinations(range(9), 5):         # every 5 cells contain a line
        assert any(set(line) <= set(cells) for line in WRAP_LINES)


def test_randomize_distribution():
    rng = random.Random(11)
    for lines, results in [(LINES, {"X", "O", "draw"}), (WRAP_LINES, {"X", "O"})]:
        seen = Counter()
        for _ in range(3000):
            result, board = randomize(lines, rng)
            assert final_result(board, lines) == result
            seen[result] += 1
        assert set(seen) == results
        for r in results:                                     # each result equally likely
            assert abs(seen[r] / 3000 - 1 / len(results)) < 0.04


def test_explorer_matches_page_code():
    """The board explorer: its verdict on every one of the 3^9 fillings against the page's
    final_result, for both line sets; its groups of final boards; and its random boards."""
    import json

    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      const verdicts = (wrap) => {{
        let out = "";
        for (let n = 0; n < 19683; n++) {{
          let b = [], v = n;
          for (let i = 0; i < 9; i++) {{ b.push(".XO"[v % 3]); v = Math.floor(v / 3); }}
          const c = m.tttCheck(b, wrap);
          out += c.result === "X" ? "X" : c.result === "O" ? "O" : c.result === "draw" ? "D" : "-";
        }}
        return out;
      }};
      const rnd = (() => {{ let a = 11; return () => {{ a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }}; }})();   // mulberry32: exact in doubles
      const g = m.tttFinalBoards(false), w = m.tttFinalBoards(true);
      console.log(JSON.stringify({{
        plain: verdicts(false), wrap: verdicts(true),
        counts: [[g.X.length, g.O.length, g.draw.length], [w.X.length, w.O.length, w.draw.length]],
        lines: [m.TTT_LINES, m.TTT_WRAP],
        random: Array.from({{length: 200}}, (_, k) => {{ const r = m.tttRandom(k % 2 === 1, rnd); return [k % 2, r.result, r.board.join("")]; }}),
        reasons: [m.tttCheck("XXX......".split("")).reason, m.tttCheck("XXXOOO...".split("")).reason, m.tttCheck("XXXOO.O..".split("")).reason,
                  m.tttCheck("OOOXX.X.X".split("")).reason, m.tttCheck("X........".split("")).reason, m.tttCheck("XXXOXOOOX".split("")).result],
      }}));""")
    assert [tuple(map(tuple, ls)) for ls in got["lines"]] == [LINES, WRAP_LINES]
    for key, lines in (("plain", LINES), ("wrap", WRAP_LINES)):
        for n in range(19683):
            board, v = [], n
            for _ in range(9):
                board.append(".XO"[v % 3])
                v //= 3
            want = ns["final_result"](tuple(board), lines)
            assert got[key][n] == {"X": "X", "O": "O", "draw": "D", None: "-"}[want], (key, board)
    assert got["counts"] == [[626, 316, 16], [882, 432, 0]]
    for wrap, result, board in got["random"]:
        assert ns["final_result"](tuple(board), WRAP_LINES if wrap else LINES) == result
    assert {r for w, r, _ in got["random"] if w} == {"X", "O"} and {r for w, r, _ in got["random"] if not w} == {"X", "O", "draw"}
    assert got["reasons"] == ["count", "both", "o_after", "x_after", "unfinished", "X"]


def test_explorer_five_cells_box():
    """The part b box: its four directions are the page's 12 wrap lines, three parallel
    lines each covering the board; for every set of up to five cells the pairs on a line
    add up to C(m, 2), five cells always hold a full line, and four cells with no line
    are completed by every empty cell. The page's example (the 2 x 2 square) has none."""
    from itertools import combinations
    from page_tests import explorer_require, node_json

    sets = [list(c) for m in range(6) for c in combinations(range(9), m)]
    got = node_json(f"const m = {explorer_require()};"
                    f"console.log(JSON.stringify({{ dirs: m.FIVE_DIRS, wrap: m.TTT_WRAP, r: {sets}.map((s) => m.tttFive(s)) }}));")
    lines = [sorted(l) for d in got["dirs"] for l in d["lines"]]
    assert sorted(lines) == sorted(sorted(l) for l in got["wrap"]) and len(lines) == 12
    for d in got["dirs"]:
        assert sorted(c for l in d["lines"] for c in l) == list(range(9))
    for a, b in combinations(range(9), 2):
        assert sum(a in l and b in l for l in lines) == 1
    for cells, r in zip(sets, got["r"]):
        m = len(cells)
        assert r["linePairs"] == r["pairs"] == m * (m - 1) // 2
        assert sorted(r["full"]) == sorted(l for l in lines if set(l) <= set(cells))
        if m == 5:
            assert r["full"]
        if m == 4 and not r["full"]:
            assert r["completers"] == [c for c in range(9) if c not in cells]
    ex = got["r"][sets.index([0, 1, 3, 4])]
    assert not ex["full"] and ex["completers"] == [2, 5, 6, 7, 8]


def test_explorer_batch_of_draws():
    """The box's "1,000 draws": with solve-before every feasible result gets a third (a
    half with the wrap lines); without it a board is uniform over all final boards, so the
    results follow their board counts (the page's 65.3 / 33.0 / 1.7 %). Every board drawn
    is legal for its result."""
    from page_tests import explorer_require, node_json

    got = node_json(f"""
      const m = {explorer_require()};
      const rnd = (() => {{ let a = 7; return () => {{ a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }}; }})();
      const out = [];
      for (const wrap of [false, true]) for (const before of [true, false]) {{
        const t = m.tttDraws(6000, wrap, before, rnd);
        const boards = Array.from({{length: 300}}, () => {{ const r = m.tttRandom(wrap, rnd, before); return [r.result, r.board.join("")]; }});
        out.push({{ wrap, before, counts: t.counts, expect: t.expect, last: [t.last.result, t.last.board.join("")], boards }});
      }}
      console.log(JSON.stringify(out));""")
    for case in got:
        lines = WRAP_LINES if case["wrap"] else LINES
        groups = final_boards(lines)
        total = sum(len(b) for b in groups.values())
        feasible = [r for r in groups if groups[r]]
        for r in ("X", "O", "draw"):
            want = (1 / len(feasible) if r in feasible else 0) if case["before"] else len(groups[r]) / total
            assert abs(case["expect"][r] - want) < 1e-12
            assert abs(case["counts"][r] / 6000 - want) < 0.025, case
        for result, board in case["boards"] + [case["last"]]:
            assert final_result(tuple(board), lines) == result
    plain = final_boards(LINES)
    assert [round(100 * len(plain[r]) / 958, 1) for r in ("X", "O", "draw")] == [65.3, 33.0, 1.7]   # the page


def test_bit_sum_trap():
    """Trap 3: a 1-bit sum counts two lines as 0. Every double-line board of X is full, so
    it then passes as a draw: 38 draws instead of 16 on the classic board, and 54 fake
    draws with the wrap lines, where a draw is impossible. Trap 1: without n_X = n_O + 1
    there are 942 "X won" boards instead of 626 (316 illegal)."""
    def results(lines, bits_mod=None, x_last=True):
        out = Counter()
        for board in itertools.product((X, O, EMPTY), repeat=9):
            n_x, n_o = board.count(X), board.count(O)
            xl = sum(all(board[i] == X for i in l) for l in lines)
            ol = sum(all(board[i] == O for i in l) for l in lines)
            if bits_mod:
                xl, ol = xl % bits_mod, ol % bits_mod
            if n_x not in (n_o, n_o + 1):
                continue
            out["X"] += xl > 0 and ol == 0 and (n_x == n_o + 1 or not x_last)
            out["O"] += ol > 0 and xl == 0 and n_x == n_o
            out["draw"] += xl == 0 and ol == 0 and n_x + n_o == 9
        return out

    for lines, double in ((LINES, 22), (WRAP_LINES, 54)):
        groups = final_boards(lines)
        doubles = [b for b in groups["X"] if count_lines(b, X, lines) == 2]
        assert len(doubles) == double and all(EMPTY not in b for b in doubles)
        assert max(count_lines(b, X, lines) for b in groups["X"]) == 2
        one_bit = results(lines, 2)
        assert one_bit["draw"] == len(groups["draw"]) + double and one_bit["X"] == len(groups["X"]) - double
    assert results(LINES, x_last=False)["X"] == 942
    assert round(100 * 22 / 626, 1) == 3.5 and round(3 * 626 / 22) == 85     # the coverage follow-up
    # any three lines cover at least 6 cells, two at least 5 (part b, step 2)
    for lines in (LINES, WRAP_LINES):
        assert min(len(set(a) | set(b) | set(c)) for a, b, c in itertools.combinations(lines, 3)) == 6
        assert min(len(set(a) | set(b)) for a, b in itertools.combinations(lines, 2)) == 5


count_lines = ns["count_lines"]


def test_four_by_four_needs_a_common_cell():
    """The 4 x 4 follow-up: the two diagonals share no cell, so X on both (8 X, 7 O and one
    empty cell, any of the 8) passes the four conditions as "X won", and O on both with X
    on the other 8 cells as "O won", though no single move completes two disjoint lines."""
    rows = [tuple(range(4 * r, 4 * r + 4)) for r in range(4)]
    lines4 = rows + [tuple(range(c, 16, 4)) for c in range(4)] + [(0, 5, 10, 15), (3, 6, 9, 12)]
    diag = set(lines4[8]) | set(lines4[9])
    assert len(diag) == 8

    def four_conditions(board):
        n_x, n_o = board.count(X), board.count(O)
        xl, ol = count_lines(board, X, lines4), count_lines(board, O, lines4)
        if n_x not in (n_o, n_o + 1):
            return None
        if xl and not ol and n_x == n_o + 1:
            return "X"
        if ol and not xl and n_x == n_o:
            return "O"
        return "draw" if not xl and not ol and n_x + n_o == 16 else None

    others = [c for c in range(16) if c not in diag]
    boards = []
    for empty in others:
        boards.append(("X", tuple(X if c in diag else EMPTY if c == empty else O for c in range(16))))
    boards.append(("O", tuple(O if c in diag else X for c in range(16))))
    for who, board in boards:
        assert four_conditions(board) == who
        won = [l for l in lines4 if all(board[i] == who for i in l)]
        assert len(won) == 2 and not set(won[0]) & set(won[1])     # no cell for a last move
    assert ("X", tuple("X.OXOXXOOXXOXOOX")) in boards               # one of them, cell 1 empty


def test_figures_up_to_date():
    from page_tests import assert_figures_match

    assert_figures_match(11)
