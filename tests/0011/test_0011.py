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
      let seed = 11;
      const rnd = () => {{ seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; }};
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
