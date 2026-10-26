# Starting code of the run panel of question 0016: the page's Python code is loaded as
# solution.py; call its functions here.
from solution import *  # noqa: F401,F403

print(josephus_closed(20, 2))    # 8   (part a)
print(josephus_closed(30, 3))    # 18  (part b)
print(josephus_closed(20, 4))    # 16  (part c)

for n in range(1, 17):           # L = 2: zero at the powers of two, then up by 2
    print(n, josephus_chain(n, 2), josephus_closed(n, 2))
