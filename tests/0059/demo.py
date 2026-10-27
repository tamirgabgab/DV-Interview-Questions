# The next and previous numbers with as many ones, and their places in the list
from solution import *  # noqa: F401,F403

x = 92
print(f"{x:08b} -> next {next_same(x, 8):08b} ({next_same(x, 8)}), prev {prev_same(x, 8):08b} ({prev_same(x, 8)})")
print("smaller with four ones:", rank_same(x), "| the 25th of them:", unrank_same(24, 4))
y, out = 0b111, []
while y and y < 1 << 5:                  # every 3 of 5, in order
    out.append(f"{y:05b}")
    y = next_same(y, 5)
print(" ".join(out))
