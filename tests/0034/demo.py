# Gray codes of 0..15, and the full / empty rules with 5-bit pointers (16 entries)
from solution import *  # noqa: F401,F403

for b in range(16):
    print(f"{b:2d}  {b:04b}  {bin2gray(b):04b}  back: {gray2bin(bin2gray(b), 4)}")

BITS = 5
w, r = 23, 7                     # 16 words apart: full
print("full:", fifo_full(bin2gray(w), bin2gray(r), BITS), "empty:", fifo_empty(bin2gray(w), bin2gray(r)))  # True empty: False
