# The page's functions: the mirror on a square board, the search with memo, the 2-row strategy
from solution import *  # noqa: F401,F403

print(mirror_move((4, 4, 4, 4)))                      # (1, 1)
print(mirror_move((4, 1, 0, 0)))                      # (0, 2)
print(winning_moves(4, 4), winning_moves(8, 8))       # [(1, 1)] [(1, 1)]
print(winning_moves(3, 5))                            # [(3, 2)]
print(wins((1, 0, 0)), wins((3, 3, 3)))               # False True
print(two_rows_move(6, 6), two_rows_move(3, 2))       # (5, 1) None
