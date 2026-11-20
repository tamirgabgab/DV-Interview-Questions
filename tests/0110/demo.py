# The page's cycle models of the three snippets: the code under review and its fix
from solution import *  # noqa: F401,F403

d = [0, 1, 1, 0, 1, 0, 0, 0]
# part a: q3 in every cycle, with = (one cycle late) and with <= (three cycles late)
print([q3 for q1, q2, q3 in delay3(d, blocking=True)])   # [0, 0, 1, 1, 0, 1, 0, 0]
print([q3 for q1, q2, q3 in delay3(d)])                  # [0, 0, 0, 0, 1, 1, 0, 1]

en = [0, 1, 1, 0, 0, 1, 0, 0]
x = [3, 5, 9, 12, 7, 6, 10, 1]
# part b: without the default line y keeps its value while en is low
print(en_gate(en, x, default=False))                     # [0, 5, 9, 9, 9, 6, 6, 6]
print(en_gate(en, x))                                    # [0, 5, 9, 0, 0, 6, 0, 0]

# part c: the average of 200 and 100 in 8 bits, then in 9
print(avg8(200, 100, width=8))                           # 22
print(avg8(200, 100))                                    # 150
