# The next and previous numbers with as many ones, and their places in the list
from solution import *  # noqa: F401,F403

x = 92
print(f"{x:08b} -> next {next_same(x, 8):08b} ({next_same(x, 8)}), prev {prev_same(x, 8):08b} ({prev_same(x, 8)})")  # 01011100 -> next 01100011 (99), prev 01011010 (90)
print("three zeros after 120:", next_zeros(120), f"= {next_zeros(120):b}", "| before 143:", prev_zeros(143))  # 143 = 10001111 | before 143: 120
y, out = 0b111, []
while y and y < 1 << 5:                  # every 3 of 5, in order
    out.append(f"{y:05b}")
    y = next_same(y, 5)
print(" ".join(out))  # 00111 01011 01101 01110 10011 10101 10110 11001 11010 11100
