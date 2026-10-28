# How many tags the transactions need, with one pool and with two
from solution import *  # noqa: F401,F403

print("one pool:", tags_needed([(0, 30), (5, 10), (15, 20)]))  # 2
print("a response and a send at 10:", tags_needed([(0, 10), (10, 20)]))  # 1
print("peaks apart (reads, writes, shared):", pools([(0, 10, "R"), (2, 12, "R"), (20, 30, "W"), (22, 32, "W")]))  # (2, 2, 2)
print("peaks together:", pools([(0, 10, "R"), (2, 12, "R"), (3, 13, "W"), (5, 15, "W")]))  # (2, 2, 4)
