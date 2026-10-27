# The page's four checkers on 16 tags returned out of order
import random
from solution import *  # noqa: F401,F403

sent = list(range(16))
ret = [t for t in sent if t not in (5, 12)]
random.shuffle(ret)
print("two missing:", missing_two(sent, ret, 4))  # [5, 12]
print("one missing, one twice:", missing_and_dup(sent, [t for t in sent if t != 7] + [3]))  # (7, 3)
print("three missing:", missing_k(sent, [t for t in sent if t not in (1, 8, 14)], 3, 16))  # [1, 8, 14]
