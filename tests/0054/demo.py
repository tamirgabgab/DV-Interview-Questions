# Fixed priority starves; round robin and weighted round robin under full load
from solution import *  # noqa: F401,F403

full = [0b1111] * 12
print("fixed:", [fixed_priority(r) for r in full])  # [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
print("round robin:", rr_run(full, 4))  # [1, 2, 4, 8, 1, 2, 4, 8, 1, 2, 4, 8]
print("weighted 1,2,3,4:", wrr_run(full, [1, 2, 3, 4]))  # [1, 2, 2, 4, 4, 4, 8, 8, 8, 8, 1, 2]
print("rules on the round robin:", check_trace(full, rr_run(full, 4), 4, 3))  # {'onehot': 0, 'spurious': 0, 'hold': 0, 'fair': 0}
