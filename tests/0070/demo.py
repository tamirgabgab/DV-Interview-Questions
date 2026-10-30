# The shortest path in a grid: BFS, BFS with up to k walls broken, and Dijkstra with an
# entry cost for every cell
from solution import *  # noqa: F401,F403

GRID = ["001010000", "001001010", "001010010", "001001010", "001010010", "001001010", "000000010"]
steps, path = shortest_path(GRID, (3, 0), (3, 8))
print("part a:", steps)  # 20
print("part a, eight directions:", shortest_path(GRID, (3, 0), (3, 8), diag=True)[0])  # 15
print("the path starts:", path[:4])  # [(3, 0), (4, 0), (5, 0), (6, 0)]
print("part b, k = 0..4:", [shortest_with_breaks(GRID, (3, 0), (3, 8), k) for k in range(5)])  # [20, 14, 14, 8, 8]
print("the trap grid, k = 1:", shortest_with_breaks(["001", "101", "010"], (0, 0), (2, 2), 1))  # 4
TERRAIN = ["1111111", "1559551", "1599951", "1599951", "1559551", "1115111"]
print("part c:", cheapest_path(TERRAIN, (2, 0), (3, 6)))  # 11
print("part c, eight directions:", cheapest_path(TERRAIN, (2, 0), (3, 6), diag=True))  # 9
