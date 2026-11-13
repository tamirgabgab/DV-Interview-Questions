# The page's functions: an order for tasks that depend on one another (Kahn, and DFS with
# three colours), and the critical path when the tasks run in parallel
from solution import *  # noqa: F401,F403

# the example: A..G are 0..6, (a, b) means "b after a"
edges = [(0, 1), (0, 2), (4, 2), (1, 3), (2, 3), (3, 5), (5, 6)]
print(topo_kahn(7, edges))                                    # [0, 4, 1, 2, 3, 5, 6]
print("".join("ABCDEFG"[v] for v in topo_kahn(7, edges)))     # AEBCDFG
print(topo_dfs(7, edges))                                     # ([4, 0, 2, 1, 3, 5, 6], None)
# one more edge, D -> E, closes the cycle C -> D -> E -> C
print(topo_kahn(7, edges + [(3, 4)]))                         # None
print(topo_dfs(7, edges + [(3, 4)]))                          # (None, [3, 4, 2])
# a self loop is a cycle too
print(topo_kahn(3, [(0, 1), (1, 1), (1, 2)]))                 # None
# part c: the durations in minutes
print(critical_path(7, edges, [3, 2, 4, 1, 5, 1, 4]))         # (15, [0, 3, 5, 9, 0, 10, 11], [2, 4, 0, 0, 0, 0, 0])
