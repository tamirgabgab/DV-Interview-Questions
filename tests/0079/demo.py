# A coin with p = 0.3: fair bits, a coin with p = 1/3 from a fair coin, and dice
from fractions import Fraction
from solution import *  # noqa: F401,F403

coin = make_coin(0.3, seed=79)
bits = [fair_bit(coin) for _ in range(2000)]
print("fair bits from p = 0.3: share of ones", sum(bits) / len(bits))
fair = make_coin(0.5, seed=7)
third = [biased_bit(Fraction(1, 3), fair) for _ in range(3000)]
print("p = 1/3 from a fair coin:", sum(third) / len(third))
faces = [die_roll(coin) for _ in range(6000)]
print("die from p = 0.3:", [faces.count(f) for f in range(1, 7)])
