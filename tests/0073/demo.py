# How many perfect shuffles bring a deck back, and the interleave in place
from solution import *  # noqa: F401,F403

print("52 cards:", shuffles_to_return(52), "out,", shuffles_to_return(52, "in"), "in")  # 8 out, 52 in
print("64 cards out:", shuffles_to_return(64))  # 6
a = [0, 1, 2, 3, 10, 11, 12, 13]
interleave(a)
print(a)  # [0, 10, 1, 11, 2, 12, 3, 13]
