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
