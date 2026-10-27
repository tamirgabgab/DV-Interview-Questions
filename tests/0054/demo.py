# Fixed priority starves; round robin and weighted round robin under full load
from solution import *  # noqa: F401,F403

full = [0b1111] * 12
print("fixed:", [fixed_priority(r) for r in full])
print("round robin:", rr_run(full, 4))
print("weighted 1,2,3,4:", wrr_run(full, [1, 2, 3, 4]))
print("rules on the round robin:", check_trace(full, rr_run(full, 4), 4, 3))
