# The Kelly criterion: the best fraction in every part, the growth rate, and a simulation
from fractions import Fraction
from solution import *  # noqa: F401,F403

print("part a: g(0.2) =", round(growth(0.2, 0.6), 4), "zero at", round(zero_growth(0.6, 0.2), 3))
finals = simulate(0.2, 0.6, 100, 101, seed=96)
print("median of 101 paths after 100 rounds:", round(finals[50]))
print("part b: p = 0.55 ->", kelly_fraction(Fraction(11, 20)), round(best_growth(Fraction(11, 20)), 4))
print("part c: p = 0.4, a = 3, b = 1 ->", kelly_fraction(Fraction(2, 5), 3, 1), round(best_growth(Fraction(2, 5), 3, 1), 4))
probs = [Fraction(1, 2), Fraction(3, 10), Fraction(3, 20), Fraction(1, 20)]
odds = [Fraction(11, 5), Fraction(7, 2), 5, 10]
cash, bets = kelly_race(probs, odds)
print("part d: cash", cash, "bets", [str(b) for b in bets], "growth", round(race_growth(cash, bets, probs, odds), 4))
