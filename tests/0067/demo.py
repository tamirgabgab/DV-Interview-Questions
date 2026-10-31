# The time until every node has the signal: BFS without weights, Dijkstra with weights,
# and the same Dijkstra on one-directional links
from solution import *  # noqa: F401,F403

edges = [[1, 2, 1], [1, 3, 5], [3, 2, 1], [3, 4, 2], [2, 5, 6], [4, 5, 1], [6, 5, 1]]
print("part a:", delay_bfs(6, [[u, v] for u, v, _ in edges], 1))  # 3
print("part b:", delay_dijkstra(6, edges, 1))  # 6
print("part c:", delay_directed(6, edges, 1))  # -1
print("part c, without node 6:", delay_directed(5, edges[:6], 1))  # 7
