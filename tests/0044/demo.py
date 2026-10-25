# Starting code of the run panel of question 0044: the page's Python code is loaded
# as solution.py (part b's double loop runs while it loads, a few seconds); call its
# functions here.
from solution import *  # noqa: F401,F403

print(kaprekar_step(5, 10, 3))           # 495
print(kaprekar_step(211, 10, 3))         # 99
print(num)                   # {0: 10, 495: 990}

x = 211
for n in range(1, 8):        # the chain of 211: 099, 891, 792, 693, 594, 495, 495
    x = kaprekar_step(x, 10, 3)
    print(n, f"{x:03d}")
