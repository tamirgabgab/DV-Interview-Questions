# The number of islands with four and with eight neighbours, and the size of every island
from solution import *  # noqa: F401,F403

GRID = ["110000", "110011", "000010", "000100", "000100"]
print("four directions:", count_islands(GRID))  # 3
print("eight directions:", count_islands8(GRID))  # 2
print("sizes:", island_sizes(GRID))  # [4, 3, 2]
print("sizes, eight directions:", island_sizes(GRID, diag=True))  # [5, 4]
print("the X, four:", count_islands(["101", "010", "101"]))  # 5
print("the X, eight:", count_islands8(["101", "010", "101"]))  # 1
