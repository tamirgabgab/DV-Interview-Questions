# The page's functions: the shortest plan for 4 litres, what can be measured, the three jugs
from solution import *  # noqa: F401,F403

plan = jugs_shortest(3, 5, 4)
print(len(plan))                                       # 6
print([" ".join(step) for step, x, y in plan][:2])     # ['fill B', 'pour B A']
print(plan[-1][1:])                                    # (3, 4)
print([t for t in range(8) if can_measure(3, 5, t)])   # [0, 1, 2, 3, 4, 5]
print(can_measure(4, 6, 3), jugs_shortest(4, 6, 3))    # False None
print(len(split_shortest((8, 5, 3), (8, 0, 0), (4, 4, 0))))   # 7
