# The expected waits on a fair coin, a biased coin and a die; a three-way race; the moments
from fractions import Fraction
from solution import *  # noqa: F401,F403

for p in ("HT", "HH", "HHH"):
    print(p, "fair:", expected_tosses(p), " q = 3/4:", expected_tosses(p, {"H": Fraction(3, 4), "T": Fraction(1, 4)}))
die = {str(i): Fraction(1, 6) for i in range(1, 7)}
print("66 on a die:", expected_tosses("66", die))
wins, length = race(["HHH", "HTH", "THH"])
print("race HHH / HTH / THH:", wins, "length", length)
print("HH mean and variance:", wait_moments("HH"))
print("HH, P(T = t) for t < 8:", wait_dist("HH", FAIR, 8))
